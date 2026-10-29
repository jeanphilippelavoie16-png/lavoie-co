#!/usr/bin/env python3
"""Maquette 3D visitable d'un projet de rénovation : <projet>/3d/visite.html (un seul fichier, three.js).

Lit <projet>/donnees/maison.json (produit par construire_projet.py) et, s'il existe, <projet>/scene_3d.py
(mobilier, matériaux par pièce, hauteur de plafond). Les textures (Poly Haven, CC0) sont intégrées au fichier.

Usage : python3 renovation/outils/generer_3d.py renovation/SS-02_aire_ouverte_gym_vitre
"""
import base64, importlib.util, json, math, os, sys

ICI = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(ICI, "textures")


def charger_scene(dossier):
    p = os.path.join(dossier, "scene_3d.py")
    if not os.path.isfile(p):
        return {}
    spec = importlib.util.spec_from_file_location("scene_3d", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.SCENE


def boites_mur(m, ouvs, H, sill, head):
    """Découpe un mur (axe, épaisseur) en boîtes pleines autour de ses ouvertures. Pouces, repère maison."""
    x1, y1, x2, y2 = m["x1"], m["y1"], m["x2"], m["y2"]
    t = (m.get("epaisseur") or {}).get("valeur") or 4.5
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    ext = t / 2
    verre = m.get("materiau") == "verre"
    mat = "verre" if verre else ("fondation" if m["type"] in ("fondation", "ext") else "gypse")
    trous = []
    for o in ouvs:
        c = (o.get("position") or {}).get("valeur")
        w = (o.get("largeur") or {}).get("valeur")
        if c is None or w is None:
            continue
        porte = o["type"] != "fenetre"
        trous.append((c - w / 2, c + w / 2, 0 if porte else sill, 80 if porte else head, o))
    trous.sort(key=lambda z: z[0])

    def boite(a, b, z0, z1, matiere):
        # segment [a, b] le long de l'axe (depuis p1), sur toute l'épaisseur
        pa = (x1 + ux * a, y1 + uy * a)
        pb = (x1 + ux * b, y1 + uy * b)
        xs = sorted([pa[0], pb[0]]); ys = sorted([pa[1], pb[1]])
        if abs(ux) > 0.5:
            ys = [y1 - t / 2, y1 + t / 2]
        else:
            xs = [x1 - t / 2, x1 + t / 2]
        return {"x0": xs[0], "x1": xs[1], "y0": ys[0], "y1": ys[1], "z0": z0, "z1": z1, "mat": matiere, "mur": m["id"]}

    out = []
    pos = -ext
    for a, b, z0, z1, o in trous:
        if a > pos:
            out.append(boite(pos, a, 0, H, mat))
        if z0 > 0:
            out.append(boite(a, b, 0, z0, mat))
        if z1 < H:
            out.append(boite(a, b, z1, H, "verre-cadre" if verre else mat))
        pos = max(pos, b)
    if pos < L + ext:
        out.append(boite(pos, L + ext, 0, H, mat))
    return out, t


def lattes(m, H, pas=3.5, larg=1.5, ep=1.5):
    """Claustra : lattes de chêne verticales du plancher au plafond, lisses haute et basse."""
    x1, y1, x2, y2 = m["x1"], m["y1"], m["x2"], m["y2"]
    L = math.hypot(x2 - x1, y2 - y1)
    horiz = abs(y2 - y1) < 0.01
    n = max(1, int(L // pas))
    out = []
    for i in range(n + 1):
        a = min(L, i * pas)
        x, y = x1 + (x2 - x1) * a / L, y1 + (y2 - y1) * a / L
        if horiz:
            out.append({"x0": x - larg / 2, "x1": x + larg / 2, "y0": y - ep / 2, "y1": y + ep / 2, "z0": 0, "z1": H, "mat": "placage"})
        else:
            out.append({"x0": x - ep / 2, "x1": x + ep / 2, "y0": y - larg / 2, "y1": y + larg / 2, "z0": 0, "z1": H, "mat": "placage"})
    for z0, z1 in ((0, 3), (H - 3, H)):
        out.append({"x0": min(x1, x2) - (0 if horiz else ep / 2), "x1": max(x1, x2) + (0 if horiz else ep / 2),
                    "y0": min(y1, y2) - (ep / 2 if horiz else 0), "y1": max(y1, y2) + (ep / 2 if horiz else 0),
                    "z0": z0, "z1": z1, "mat": "placage"})
    return out


def escalier(e, H, etage):
    """Volée droite : girons de chêne, contremarches blanches, dessous fermé ; trémie et cage au-dessus du plafond.
    Retourne (boîtes, trémie [x0, y0, x1, y1], obstacle)."""
    es = e.get("escalier") or {}
    n = int(round(es["nb_contremarches"]["valeur"]))
    L, W = e["dimensions"]["longueur"]["valeur"], e["dimensions"]["largeur"]["valeur"]
    cx, cy = e["position"]["x"], e["position"]["y"]
    d = {"+y": (0, 1), "-y": (0, -1), "+x": (1, 0), "-x": (-1, 0)}[es.get("direction", "+y")]
    r, pas = etage / n, L / (n - 1)

    def rect(s0, s1, z0, z1, mat):
        # s le long de la montée depuis le pied, sur toute la largeur
        if d[0] == 0:
            ya, yb = sorted([cy - d[1] * L / 2 + d[1] * s0, cy - d[1] * L / 2 + d[1] * s1])
            return {"x0": cx - W / 2, "x1": cx + W / 2, "y0": ya, "y1": yb, "z0": z0, "z1": z1, "mat": mat}
        xa, xb = sorted([cx - d[0] * L / 2 + d[0] * s0, cx - d[0] * L / 2 + d[0] * s1])
        return {"x0": xa, "x1": xb, "y0": cy - W / 2, "y1": cy + W / 2, "z0": z0, "z1": z1, "mat": mat}

    out = []
    for i in range(n - 1):
        z = (i + 1) * r
        out.append(rect(i * pas, (i + 1) * pas, 0, z - 1.25, "gypse"))                 # dessous fermé
        out.append(rect(max(0, i * pas - 1), (i + 1) * pas, z - 1.25, z, "placage"))   # giron (nez de 1 po)
        out.append(rect(i * pas, i * pas + 0.75, i * r, z - 1.25, "porte"))           # contremarche
    # trémie : dès que l'échappée (77 po au-dessus du nez) dépasse le plafond fini
    s_tr = max(0.0, min(L, ((H - 77) / r - 1) * pas))
    t0 = rect(s_tr, L, 0, 1, "")
    tremie = [t0["x0"], t0["y0"], t0["x1"], t0["y1"]]
    haut = H + etage
    cage = [{"x0": tremie[0] - 2, "x1": tremie[0], "y0": tremie[1] - 2, "y1": tremie[3] + 2, "z0": H, "z1": haut, "mat": "gypse"},
            {"x0": tremie[2], "x1": tremie[2] + 2, "y0": tremie[1] - 2, "y1": tremie[3] + 2, "z0": H, "z1": haut, "mat": "gypse"},
            {"x0": tremie[0], "x1": tremie[2], "y0": tremie[1] - 2, "y1": tremie[1], "z0": H, "z1": haut, "mat": "gypse"},
            {"x0": tremie[0], "x1": tremie[2], "y0": tremie[3], "y1": tremie[3] + 2, "z0": H, "z1": haut, "mat": "gypse"},
            {"x0": tremie[0] - 2, "x1": tremie[2] + 2, "y0": tremie[1] - 2, "y1": tremie[3] + 2, "z0": haut, "z1": haut + 1, "mat": "plafond"}]
    tout = rect(0, L, 0, 1, "")
    return out + cage, tremie, {k: tout[k] for k in ("x0", "x1", "y0", "y1")}


def peindre(boites, pieces, S):
    """Peinture par pièce : chaque grande face de mur prend la couleur de la pièce qu'elle regarde.
    SCENE["peinture"] = {id de pièce: nom de couleur}, SCENE["accents"] = [{"piece", "mur", "peinture"}]."""
    from shapely.geometry import Point, Polygon
    couleurs = S.get("peinture") or {}
    accents = {(a["piece"], a["mur"]): a["peinture"] for a in S.get("accents", [])}
    if not couleurs and not accents:
        return
    polys = [(p["id"], Polygon(p["polygone"])) for p in pieces]
    for b in boites:
        if b.get("mat") not in ("gypse", "fondation") or "mur" not in b:
            continue
        cx, cy = (b["x0"] + b["x1"]) / 2, (b["y0"] + b["y1"]) / 2
        horiz = (b["x1"] - b["x0"]) >= (b["y1"] - b["y0"])
        faces = {}
        for cote, (px, py) in ((("+y", (cx, b["y1"] + 2)), ("-y", (cx, b["y0"] - 2))) if horiz else
                               (("+x", (b["x1"] + 2, cy)), ("-x", (b["x0"] - 2, cy)))):
            pid = next((i for i, P in polys if P.contains(Point(px, py))), None)
            nom = accents.get((pid, b["mur"])) or couleurs.get(pid)
            if nom:
                faces[cote] = nom
        if faces:
            b["faces"] = faces


def feuille_porte(m, o, t):
    """Vantail ouvert à 90° (porte battante) : boîte mince depuis la charnière, du côté où la porte pousse."""
    x1, y1, x2, y2 = m["x1"], m["y1"], m["x2"], m["y2"]
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    nx, ny = -uy, ux
    c = o["position"]["valeur"]; w = o["largeur"]["valeur"]
    s = o.get("sens") or {}
    a = c - w / 2 if s.get("charniere", "debut") == "debut" else c + w / 2
    hx, hy = x1 + ux * a, y1 + uy * a
    side = 1 if s.get("ouvre_vers", "gauche") == "gauche" else -1
    fx, fy = hx + nx * side * (t / 2 + w), hy + ny * side * (t / 2 + w)
    e = 0.9
    if abs(nx) > 0.5:
        return {"x0": min(hx, fx), "x1": max(hx, fx), "y0": hy - e, "y1": hy + e}
    return {"x0": hx - e, "x1": hx + e, "y0": min(hy, fy), "y1": max(hy, fy)}


def main(dossier):
    dossier = os.path.abspath(dossier)
    M = json.load(open(os.path.join(dossier, "donnees", "maison.json"), encoding="utf-8"))
    S = charger_scene(dossier)
    niv = next(n for n in M["niveaux"] if n["id"] == S.get("niveau", "SS"))
    H = S.get("plafond", 90)
    sill, head = S.get("allege_fenetre", 56), S.get("tete_fenetre", 86)
    par_mur = {}
    for o in niv["ouvertures"]:
        par_mur.setdefault(o["mur_id"], []).append(o)
    boites, portes = [], []
    for m in niv["murs"]:
        if m.get("materiau") == "lattes":
            boites += lattes(m, H)
            continue
        bx, t = boites_mur(m, par_mur.get(m["id"], []), H, sill, head)
        boites += bx
        for o in par_mur.get(m["id"], []):
            if o["type"] == "fenetre":
                c, w = o["position"]["valeur"], o["largeur"]["valeur"]
                # vitre de fenêtre : une boîte mince au centre du mur, entre allège et tête
                L = math.hypot(m["x2"] - m["x1"], m["y2"] - m["y1"])
                ux, uy = (m["x2"] - m["x1"]) / L, (m["y2"] - m["y1"]) / L
                a, b = c - w / 2, c + w / 2
                pa = (m["x1"] + ux * a, m["y1"] + uy * a); pb = (m["x1"] + ux * b, m["y1"] + uy * b)
                if abs(ux) > 0.5:
                    boites.append({"x0": min(pa[0], pb[0]), "x1": max(pa[0], pb[0]), "y0": m["y1"] - 0.5, "y1": m["y1"] + 0.5, "z0": sill, "z1": head, "mat": "vitre"})
                else:
                    boites.append({"x0": m["x1"] - 0.5, "x1": m["x1"] + 0.5, "y0": min(pa[1], pb[1]), "y1": max(pa[1], pb[1]), "z0": sill, "z1": head, "mat": "vitre"})
            elif o.get("operation") == "coulissante":
                pass                      # porte coulissante : représentée ouverte (dans le mur)
            elif o.get("operation") != "aucune":
                f = feuille_porte(m, o, t)
                if o.get("materiau") == "verre":
                    # porte vitrée : panneau de verre dans un cadre noir de 1½ po
                    f.update({"z0": 0.5, "z1": 80, "mat": "porte-verre"})
                    portes.append(f)
                    long_x = (f["x1"] - f["x0"]) > (f["y1"] - f["y0"])
                    c = 1.5
                    if long_x:
                        cadres = [(f["x0"], f["x0"] + c, 0.5, 80), (f["x1"] - c, f["x1"], 0.5, 80), (f["x0"], f["x1"], 0.5, 2), (f["x0"], f["x1"], 78.5, 80)]
                        portes += [{"x0": a0, "x1": a1, "y0": f["y0"] - 0.2, "y1": f["y1"] + 0.2, "z0": z0, "z1": z1, "mat": "metal"} for a0, a1, z0, z1 in cadres]
                    else:
                        cadres = [(f["y0"], f["y0"] + c, 0.5, 80), (f["y1"] - c, f["y1"], 0.5, 80), (f["y0"], f["y1"], 0.5, 2), (f["y0"], f["y1"], 78.5, 80)]
                        portes += [{"x0": f["x0"] - 0.2, "x1": f["x1"] + 0.2, "y0": a0, "y1": a1, "z0": z0, "z1": z1, "mat": "metal"} for a0, a1, z0, z1 in cadres]
                    portes.append({**f, "z0": 38, "z1": 40, "mat": "metal", **({"x0": f["x1"] - 4, "x1": f["x1"] - 3} if long_x else {"y0": f["y1"] - 4, "y1": f["y1"] - 3})})
                else:
                    f.update({"z0": 0.5, "z1": 80, "mat": "porte-ext" if m["type"] != "int" else "porte"})
                    portes.append(f)
    # meneaux des cloisons vitrées
    for m in niv["murs"]:
        if m.get("materiau") != "verre":
            continue
        L = math.hypot(m["x2"] - m["x1"], m["y2"] - m["y1"])
        n = max(1, round(L / 36))
        for i in range(n + 1):
            a = L * i / n
            x = m["x1"] + (m["x2"] - m["x1"]) * a / L; y = m["y1"] + (m["y2"] - m["y1"]) * a / L
            ouvert = any(abs(a - o["position"]["valeur"]) < o["largeur"]["valeur"] / 2 + 1 for o in par_mur.get(m["id"], []))
            if not ouvert:
                boites.append({"x0": x - 0.9, "x1": x + 0.9, "y0": y - 1.2, "y1": y + 1.2, "z0": 0, "z1": H, "mat": "metal"})
        horiz = abs(m["y2"] - m["y1"]) < 0.01
        for z0, z1 in ((0, 2.5), (H - 2.5, H)):
            boites.append({"x0": min(m["x1"], m["x2"]) - (0 if horiz else 1.2), "x1": max(m["x1"], m["x2"]) + (0 if horiz else 1.2),
                           "y0": min(m["y1"], m["y2"]) - (1.2 if horiz else 0), "y1": max(m["y1"], m["y2"]) + (1.2 if horiz else 0),
                           "z0": z0, "z1": z1, "mat": "metal"})
    # colonnes et retombées de poutres
    for s in niv["structure"]:
        g = s.get("geometrie") or {}
        if s["type"] == "colonne":
            w = g.get("largeur", 8) + 2
            boites.append({"x0": g["x"] - w / 2, "x1": g["x"] + w / 2, "y0": g["y"] - w / 2, "y1": g["y"] + w / 2, "z0": 0, "z1": H,
                           "mat": S.get("mat_colonne", "placage")})
        elif s["type"] == "poutre" and "x1" in g:
            horiz = abs(g["y2"] - g["y1"]) < 0.01
            e = 5
            boites.append({"x0": min(g["x1"], g["x2"]) - (0 if horiz else e), "x1": max(g["x1"], g["x2"]) + (0 if horiz else e),
                           "y0": min(g["y1"], g["y2"]) - (e if horiz else 0), "y1": max(g["y1"], g["y2"]) + (e if horiz else 0),
                           "z0": H - 10, "z1": H, "mat": "gypse"})
    # escaliers projetés : marches, trémie dans le plafond, cage au-dessus, obstacle pour la visite
    tremies, obstacles = [], []
    for e in niv["elements"]:
        if e["type"] == "escalier" and e.get("etat") == "nouveau":
            bx, tr, ob = escalier(e, H, S.get("hauteur_etage", 105))
            boites += bx; tremies.append(tr); obstacles.append(ob)
    peindre(boites, niv["pieces"], S)
    mats = S.get("sols", {})
    sols = []
    for p in niv["pieces"]:
        pts = p["polygone"]
        sols.append({"id": p["id"], "nom": p["nom"], "pts": pts, "mat": mats.get(p["id"], S.get("sol_defaut", "chene")),
                     "cx": sum(q[0] for q in pts) / len(pts), "cy": sum(q[1] for q in pts) / len(pts)})
    empreinte = []
    for m in niv["murs"]:
        if m["type"] == "fondation":
            empreinte += [[m["x1"], m["y1"]], [m["x2"], m["y2"]]]
    xs = [q[0] for q in empreinte]; ys = [q[1] for q in empreinte]
    scene = {"H": H, "boites": boites, "portes": portes, "sols": sols, "mobilier": S.get("mobilier", []),
             "revetements": S.get("revetements", []), "lumieres": S.get("lumieres", []),
             "visites": S.get("visites", []), "depart": S.get("depart", {"x": 400, "y": 180, "cap": 200}),
             "bornes": [min(xs), min(ys), max(xs), max(ys)], "titre": S.get("titre", M["projet"].get("proposition", "")),
             "projet": M["projet"]["nom"], "palette": S.get("palette", []),
             "tremies": tremies, "obstacles": obstacles, "peintures": S.get("peintures", {})}
    textures = {}
    for f in sorted(os.listdir(TEX)):
        if f.endswith(".jpg"):
            textures[f[:-4]] = "data:image/jpeg;base64," + base64.b64encode(open(os.path.join(TEX, f), "rb").read()).decode()
    gab = open(os.path.join(ICI, "visite3d_gabarit.html"), encoding="utf-8").read()
    html = (gab.replace("/*__SCENE__*/null", json.dumps(scene, ensure_ascii=False).replace("</", "<\\/"))
               .replace("/*__TEXTURES__*/null", json.dumps(textures))
               .replace("__TITRE__", scene["titre"]))
    os.makedirs(os.path.join(dossier, "3d"), exist_ok=True)
    out = os.path.join(dossier, "3d", "visite.html")
    open(out, "w", encoding="utf-8").write(html)
    print("maquette 3D :", out, f"({len(html) // 1024} Ko)")


if __name__ == "__main__":
    main(sys.argv[1])
