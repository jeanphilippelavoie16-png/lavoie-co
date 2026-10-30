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


def eventail(tr):
    """Rayons des marches tournantes (voir generer_plans.eventail) : [(pivot, point)] pour j = 0..nb."""
    x0, y0, x1, y1 = tr["carre"]
    px, py = tr["pivot"]
    xf, yf = (x0 if abs(px - x1) < 0.01 else x1), (y0 if abs(py - y1) < 0.01 else y1)
    hx, vy = math.copysign(1, xf - px), math.copysign(1, yf - py)
    out = []
    for j in range(int(tr["nb"]) + 1):
        f = math.radians(90 * j / tr["nb"])
        dx, dy = math.cos(f) * hx, math.sin(f) * vy
        t = min(abs((xf - px) / dx) if abs(dx) > 1e-9 else 1e9, abs((yf - py) / dy) if abs(dy) > 1e-9 else 1e9)
        out.append(((px, py), (px + dx * t, py + dy * t)))
    return out


def escalier(e, H, etage):
    """Volée droite : girons de chêne, contremarches blanches, dessous fermé ; trémie et cage au-dessus du plafond.
    Retourne (boîtes, trémie [x0, y0, x1, y1], obstacle)."""
    es = e.get("escalier") or {}
    n = int(round(es["nb_contremarches"]["valeur"]))
    L, W = e["dimensions"]["longueur"]["valeur"], e["dimensions"]["largeur"]["valeur"]
    cx, cy = e["position"]["x"], e["position"]["y"]
    d = {"+y": (0, 1), "-y": (0, -1), "+x": (1, 0), "-x": (-1, 0)}[es.get("direction", "+y")]
    total, depart = int(es.get("total", n)), int(es.get("depart", 0))   # escalier en L : volée qui part d'un palier
    r = etage / total
    girons = int(es.get("girons", n - 1))
    pas = L / girons
    z0v = depart * r

    def rect(s0, s1, z0, z1, mat, t0=None, t1=None):
        # s le long de la montée depuis le pied ; t en travers (par défaut toute la largeur)
        t0 = -W / 2 if t0 is None else t0
        t1 = W / 2 if t1 is None else t1
        if d[0] == 0:
            ya, yb = sorted([cy - d[1] * L / 2 + d[1] * s0, cy - d[1] * L / 2 + d[1] * s1])
            return {"x0": cx + t0, "x1": cx + t1, "y0": ya, "y1": yb, "z0": z0, "z1": z1, "mat": mat}
        xa, xb = sorted([cx - d[0] * L / 2 + d[0] * s0, cx - d[0] * L / 2 + d[0] * s1])
        return {"x0": xa, "x1": xb, "y0": cy + t0, "y1": cy + t1, "z0": z0, "z1": z1, "mat": mat}

    out, obst = [], []
    tr = es.get("tournant")
    nd = girons - (int(tr["nb"]) if tr else 0)
    if tr:                                       # marches tournantes en haut : la volée droite s'arrête au carré
        pas = (L - (tr["carre"][3] - tr["carre"][1] if d[0] == 0 else tr["carre"][2] - tr["carre"][0])) / nd
    flottant = es.get("style") == "flottant"
    for i in range(nd):
        z = z0v + (i + 1) * r
        if flottant:
            # marche de chêne de 2 po posée sur un limon central en acier noir (crémaillère) : on voit à travers
            out.append(rect(max(0, i * pas - 1), (i + 1) * pas, z - 2, z, "placage"))
            out.append(rect(i * pas, (i + 1) * pas, z - 3, z - 2, "metal", -2.5, 2.5))
            out.append(rect(i * pas, i * pas + 1, max(0, z - r - 3), z - 2, "metal", -2.5, 2.5))
            if z - 2 < 72:
                q = rect(i * pas, (i + 1) * pas, 0, 1, "")
                obst.append({k: q[k] for k in ("x0", "x1", "y0", "y1")})
            continue
        bas = 0 if z < 60 else z - 12            # dessous fermé jusqu'au sol, ou sous-face de 1 pi quand on passe dessous
        out.append(rect(i * pas, (i + 1) * pas, bas, z - 1.25, "gypse"))
        out.append(rect(max(0, i * pas - 1), (i + 1) * pas, z - 1.25, z, "placage"))   # giron (nez de 1 po)
        out.append(rect(i * pas - 0.75, i * pas, z - r, z - 1.25, "porte"))           # contremarche, devant le dessous
        if bas < 72:
            q = rect(i * pas, (i + 1) * pas, 0, 1, "")
            obst.append({k: q[k] for k in ("x0", "x1", "y0", "y1")})
    if tr:
        rayons = eventail(tr)
        coin = (rayons[0][1][0], rayons[-1][1][1])          # coin du carré opposé au pivot
        for j in range(int(tr["nb"])):
            (p0, a_), (_, b_) = rayons[j], rayons[j + 1]
            entoure = abs(a_[0] - coin[0]) < 0.01 and abs(b_[1] - coin[1]) < 0.01 and a_ != coin and b_ != coin
            pts = [p0, a_] + ([coin] if entoure else []) + [b_]
            z = (nd + j + 1) * r
            if flottant:
                out.append({"pts": [list(q) for q in pts], "z0": z - 2, "z1": z, "mat": "placage"})
            else:
                out.append({"pts": [list(q) for q in pts], "z0": 0, "z1": z - 1.25, "mat": "gypse"})
                out.append({"pts": [list(q) for q in pts], "z0": z - 1.25, "z1": z, "mat": "placage"})
        if flottant:                             # poteau d'acier au pivot des marches tournantes
            px, py = tr["pivot"]
            out.append({"x0": px - 1.5, "x1": px + 1.5, "y0": py - 1.5, "y1": py + 1.5, "z0": 0, "z1": (nd + int(tr["nb"])) * r + 36, "mat": "metal"})
    # trémie : dès que l'échappée (77 po au-dessus du nez) dépasse le plafond fini
    s_tr = max(0.0, min(L, ((H - 77 - z0v) / r - 1) * pas))
    t0 = rect(s_tr, L, 0, 1, "")
    return out, [t0["x0"], t0["y0"], t0["x1"], t0["y1"]], obst


def palier(e, H, etage):
    """Palier d'un escalier en L : bloc fermé jusqu'au sol, dessus en chêne. Retourne (boîtes, trémie, obstacle)."""
    pa = e["palier"]
    z = int(pa["niveau"]) * etage / int(pa["total"])
    L, W = e["dimensions"]["longueur"]["valeur"], e["dimensions"]["largeur"]["valeur"]
    x0, y0 = e["position"]["x"] - L / 2, e["position"]["y"] - W / 2
    b = {"x0": x0, "x1": x0 + L, "y0": y0, "y1": y0 + W}
    tr = [x0, y0, x0 + L, y0 + W] if z + 77 > H else None
    return [dict(b, z0=0, z1=z - 1.25, mat="gypse"), dict(b, z0=z - 1.25, z1=z, mat="placage")], tr, b


def cage_tremie(rects, H, etage):
    """Réunit les trémies (rectangles qui se touchent) en polygones ; murs de la cage au-dessus du plafond."""
    from shapely.geometry import box
    from shapely.ops import unary_union
    from shapely.geometry.polygon import orient
    u = unary_union([box(*r) for r in rects]).buffer(0)
    polys, boites = [], []
    for p in (u.geoms if hasattr(u, "geoms") else [u]):
        p = orient(p.simplify(0.01), 1.0)
        pts = [list(q) for q in list(p.exterior.coords)[:-1]]
        polys.append(pts)
        for (xa, ya), (xb, yb) in zip(pts, pts[1:] + pts[:1]):   # sens antihoraire : l'extérieur est à droite
            if abs(ya - yb) < 0.01:
                y = ya - 2 if xb > xa else ya
                boites.append({"x0": min(xa, xb) - 2, "x1": max(xa, xb) + 2, "y0": y, "y1": y + 2, "z0": H + 0.2, "z1": H + etage, "mat": "gypse"})
            else:
                x = xa if yb > ya else xa - 2
                boites.append({"x0": x, "x1": x + 2, "y0": min(ya, yb) - 2, "y1": max(ya, yb) + 2, "z0": H + 0.2, "z1": H + etage, "mat": "gypse"})
        mx0, my0, mx1, my1 = p.bounds
        boites.append({"x0": mx0 - 2, "x1": mx1 + 2, "y0": my0 - 2, "y1": my1 + 2, "z0": H + etage, "z1": H + etage + 1, "mat": "plafond"})
    return polys, boites


def bibliotheque(scene, S):
    """Matériaux du catalogue (catalogue_materiaux.py) employés par la scène, intégrés au fichier en data URI."""
    sys.path.insert(0, ICI)
    from catalogue_materiaux import CATALOGUE
    employes = {"platre", S.get("mat_colonne", "placage")}
    for groupe in ("boites", "portes", "mobilier", "sols", "revetements"):
        employes |= {o.get("mat") for o in scene[groupe]}
    out = {}
    for cle in sorted(employes & set(CATALOGUE)):
        e, d = CATALOGUE[cle], os.path.join(ICI, "materiaux", cle)
        if not os.path.isfile(os.path.join(d, "relief.jpg")):
            print(f"  matériau {cle} absent : python3 renovation/outils/materiaux.py telecharger {cle}")
            continue
        uri = lambda f: "data:image/jpeg;base64," + base64.b64encode(open(os.path.join(d, f), "rb").read()).decode()
        m = {"taille_m": e["taille_m"], "relief": uri("relief.jpg"), "metal": e.get("metal", 0)}
        if e.get("relief_seul"):
            m["relief_seul"] = True
        else:
            m["couleur"] = uri("couleur.jpg")
        if "rugosite" in e:
            m["rugosite"] = e["rugosite"]
        elif os.path.isfile(os.path.join(d, "rugosite.jpg")):
            m["carte_rugosite"] = uri("rugosite.jpg")
        out[cle] = m
    return out


def modeles(scene):
    """Modèles GLB du catalogue (catalogue_modeles.py) employés par le mobilier, intégrés en data URI."""
    sys.path.insert(0, ICI)
    from catalogue_modeles import CATALOGUE
    out, info, credits = {}, {}, []
    for cle in sorted({o["cle"] for o in scene["mobilier"] if o.get("forme") == "modele"}):
        e = CATALOGUE[cle]
        f = os.path.join(ICI, "modeles", e["fichier"])
        if not os.path.isfile(f):
            print(f"  modèle {cle} absent : {f}")
            continue
        out[cle] = "data:model/gltf-binary;base64," + base64.b64encode(open(f, "rb").read()).decode()
        info[cle] = {"avant": e.get("avant", "+z")}
        credits.append([e["usage"], e["attribution"], e["licence"]])
    from catalogue_materiaux import CATALOGUE as MATS
    for cle in sorted(scene.get("materiaux") or {}):
        m = MATS.get(cle) or {}
        if m.get("source") in ("ambientcg", "polyhaven"):
            credits.append([m["usage"], {"ambientcg": "ambientCG", "polyhaven": "Poly Haven"}[m["source"]] + " " + m["id"], "CC0 1.0"])
    return out, info, credits


def porte_fermee(m, o, t):
    """Porte extérieure fermée dans l'épaisseur du mur, avec poignée côté intérieur."""
    L = math.hypot(m["x2"] - m["x1"], m["y2"] - m["y1"])
    ux, uy = (m["x2"] - m["x1"]) / L, (m["y2"] - m["y1"]) / L
    c, w = o["position"]["valeur"], o["largeur"]["valeur"]
    pa = (m["x1"] + ux * (c - w / 2), m["y1"] + uy * (c - w / 2)); pb = (m["x1"] + ux * (c + w / 2), m["y1"] + uy * (c + w / 2))
    if abs(ux) > 0.5:
        f = {"x0": min(pa[0], pb[0]), "x1": max(pa[0], pb[0]), "y0": m["y1"] - 0.9, "y1": m["y1"] + 0.9}
        cy = m["y1"] + (2 if m["y1"] < 190 else -2)
        poignee = {"x0": f["x1"] - 4, "x1": f["x1"] - 3, "y0": min(cy, m["y1"]), "y1": max(cy, m["y1"])}
    else:
        f = {"x0": m["x1"] - 0.9, "x1": m["x1"] + 0.9, "y0": min(pa[1], pb[1]), "y1": max(pa[1], pb[1])}
        cx = m["x1"] + (2 if m["x1"] < 228 else -2)
        poignee = {"x0": min(cx, m["x1"]), "x1": max(cx, m["x1"]), "y0": f["y1"] - 4, "y1": f["y1"] - 3}
    return [dict(f, z0=0.5, z1=80, mat="porte-ext"), dict(poignee, z0=37, z1=39, mat="inox")]


def reculer_bouts_de_murs(boites):
    """Un bout de mur qui aboutit sur la face d'un autre mur est reculé de 0,05 po : plus de faces confondues
    (scintillement aux jonctions en T, surtout quand les deux faces ont des peintures différentes)."""
    murs = [b for b in boites if "mur" in b]
    for b in murs:
        for k in ("x", "y"):
            autre = "y" if k == "x" else "x"
            for s_, kk in ((-1, k + "0"), (1, k + "1")):
                v = b[kk]
                for o in murs:
                    if o is b or o["mur"] == b["mur"]:
                        continue
                    for ok in (k + "0", k + "1"):
                        if abs(o[ok] - v) < 0.02 and ((ok.endswith("0") and s_ < 0) or (ok.endswith("1") and s_ > 0)):
                            chev = min(b[autre + "1"], o[autre + "1"]) - max(b[autre + "0"], o[autre + "0"])
                            if chev > 0.3 and (b[autre + "1"] - b[autre + "0"]) < (o[autre + "1"] - o[autre + "0"]):
                                b[kk] = v - s_ * 0.05


def finitions(niv, par_mur, H, sill, head, S):
    """Plinthes, chambranles et seuils des portes, cadres, meneaux et tablettes des fenêtres."""
    sol = S.get("sol_defaut", "chene")
    out = []
    cx0, cy0 = 228, 190                                   # vers l'intérieur de la maison
    for m in niv["murs"]:
        if m.get("materiau") in ("verre", "lattes"):
            continue
        t = (m.get("epaisseur") or {}).get("valeur") or 4.5
        L = math.hypot(m["x2"] - m["x1"], m["y2"] - m["y1"])
        ux, uy = (m["x2"] - m["x1"]) / L, (m["y2"] - m["y1"]) / L
        horiz = abs(ux) > 0.5
        ext = m["type"] in ("fondation", "ext")
        cotes = [1, -1]
        if ext:                                           # mur extérieur : seulement la face intérieure
            cotes = [1 if ((cy0 - m["y1"]) if horiz else (cx0 - m["x1"])) > 0 else -1]

        def b_(a, b, n0, n1, z0, z1, mat):
            # a, b le long de l'axe ; n0, n1 décalage perpendiculaire depuis l'axe
            pa = (m["x1"] + ux * a, m["y1"] + uy * a); pb = (m["x1"] + ux * b, m["y1"] + uy * b)
            if horiz:
                return {"x0": min(pa[0], pb[0]), "x1": max(pa[0], pb[0]), "y0": m["y1"] + min(n0, n1), "y1": m["y1"] + max(n0, n1), "z0": z0, "z1": z1, "mat": mat}
            return {"x0": m["x1"] + min(n0, n1), "x1": m["x1"] + max(n0, n1), "y0": min(pa[1], pb[1]), "y1": max(pa[1], pb[1]), "z0": z0, "z1": z1, "mat": mat}

        trous = sorted(((o["position"]["valeur"] - o["largeur"]["valeur"] / 2, o["position"]["valeur"] + o["largeur"]["valeur"] / 2, o)
                        for o in par_mur.get(m["id"], []) if o.get("position", {}).get("valeur") is not None), key=lambda z: z[0])
        # plinthes de 4 po entre les portes (sous les fenêtres aussi)
        pos = -t / 2 if not ext else 0
        bouts = []
        for a, b, o in trous:
            if o["type"] != "fenetre":
                bouts.append((pos, a)); pos = b
        bouts.append((pos, L + (t / 2 if not ext else 0)))
        for a, b in bouts:
            if b - a < 1:
                continue
            for s_ in cotes:
                out.append(b_(a, b, s_ * t / 2, s_ * (t / 2 + 0.5), 0, 4, "plinthe"))
        for a, b, o in trous:
            if o["type"] == "fenetre":
                # cadre noir et meneau dans le plan de la vitre, jambages blancs, tablette de chêne
                f, d = 1.5, 2.5
                out += [b_(a, b, -d / 2, d / 2, sill, sill + f, "metal"), b_(a, b, -d / 2, d / 2, head - f, head, "metal"),
                        b_(a, a + f, -d / 2, d / 2, sill, head, "metal"), b_(b - f, b, -d / 2, d / 2, sill, head, "metal"),
                        b_((a + b) / 2 - 0.75, (a + b) / 2 + 0.75, -d / 2, d / 2, sill, head, "metal")]
                for s_ in cotes:
                    out += [b_(a, a + 0.5, s_ * d / 2, s_ * t / 2, sill, head, "porte"), b_(b - 0.5, b, s_ * d / 2, s_ * t / 2, sill, head, "porte"),
                            b_(a, b, s_ * d / 2, s_ * t / 2, head - 0.5, head, "porte"),
                            b_(a - 1.5, b + 1.5, s_ * d / 2, s_ * (t / 2 + 1.25), sill - 0.75, sill, "placage")]
                continue
            # porte : seuil, doublage de l'ouverture et chambranles de 2½ po des deux côtés
            out.append(b_(a, b, -t / 2, t / 2, 0, 0.06, sol))
            out += [b_(a, a + 0.5, -t / 2, t / 2, 0, 80, "porte"), b_(b - 0.5, b, -t / 2, t / 2, 0, 80, "porte"),
                    b_(a, b, -t / 2, t / 2, 79.5, 80, "porte")]
            for s_ in cotes:
                out += [b_(a - 2.5, a, s_ * t / 2, s_ * (t / 2 + 0.6), 0, 82.5, "porte"), b_(b, b + 2.5, s_ * t / 2, s_ * (t / 2 + 0.6), 0, 82.5, "porte"),
                        b_(a - 2.5, b + 2.5, s_ * t / 2, s_ * (t / 2 + 0.6), 80, 82.5, "porte")]
    return out


def couper_aux_cloisons(boites, niv):
    """Coupe les boîtes des murs de fondation là où une cloison les rejoint, pour que chaque pièce ait sa peinture
    (sinon un long mur prend la couleur de la pièce où tombe son milieu)."""
    cloisons = [m for m in niv["murs"] if m["type"] == "int"]
    out = []
    for b in boites:
        mur = next((m for m in niv["murs"] if m["id"] == b.get("mur")), None)
        if not mur or mur["type"] not in ("fondation", "ext") or b.get("mat") not in ("gypse", "fondation"):
            out.append(b); continue
        horiz = (b["x1"] - b["x0"]) >= (b["y1"] - b["y0"])
        k, autre = ("x", "y") if horiz else ("y", "x")
        coupes = []
        for c in cloisons:
            for (cx, cy) in ((c["x1"], c["y1"]), (c["x2"], c["y2"])):
                v, w = (cx, cy) if horiz else (cy, cx)
                if b[k + "0"] + 1 < v < b[k + "1"] - 1 and b[autre + "0"] - 8 < w < b[autre + "1"] + 8:
                    coupes.append(v)
        bords = [b[k + "0"]] + sorted(set(coupes)) + [b[k + "1"]]
        for a0, a1 in zip(bords, bords[1:]):
            out.append(dict(b, **{k + "0": a0, k + "1": a1}))
    return out


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
                elif m["type"] != "int":
                    portes += porte_fermee(m, o, t)
                else:
                    f.update({"z0": 0.5, "z1": 80, "mat": "porte"})
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
            w = g.get("largeur", 8) + 2.5            # habillage de 1¼ po : dépasse la retombée de poutre
            boites.append({"x0": g["x"] - w / 2, "x1": g["x"] + w / 2, "y0": g["y"] - w / 2, "y1": g["y"] + w / 2, "z0": 0, "z1": H,
                           "mat": S.get("mat_colonne", "placage")})
        elif s["type"] == "poutre" and "x1" in g:
            horiz = abs(g["y2"] - g["y1"]) < 0.01
            e = 5
            boites.append({"x0": min(g["x1"], g["x2"]) - (0 if horiz else e), "x1": max(g["x1"], g["x2"]) + (0 if horiz else e),
                           "y0": min(g["y1"], g["y2"]) - (e if horiz else 0), "y1": max(g["y1"], g["y2"]) + (e if horiz else 0),
                           "z0": H - 10.03, "z1": H, "mat": "gypse"})
    # escaliers projetés : marches, trémie dans le plafond, cage au-dessus, obstacle pour la visite
    rects, obstacles = [], []
    for e in niv["elements"]:
        if e["type"] == "escalier" and e.get("etat") == "nouveau":
            bx, tr, ob = escalier(e, H, S.get("hauteur_etage", 105))
            boites += bx; rects.append(tr); obstacles += ob
        elif e.get("palier") and e.get("etat") == "nouveau":
            bx, tr, ob = palier(e, H, S.get("hauteur_etage", 105))
            boites += bx; obstacles.append(ob)
            if tr:
                rects.append(tr)
    tremies, cage = cage_tremie(rects, H, S.get("hauteur_etage", 105)) if rects else ([], [])
    boites += cage
    boites = couper_aux_cloisons(boites, niv)
    reculer_bouts_de_murs(boites)
    finis = finitions(niv, par_mur, H, sill, head, S)
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
    scene = {"H": H, "boites": boites + finis, "portes": portes, "sols": sols, "mobilier": S.get("mobilier", []),
             "revetements": S.get("revetements", []), "lumieres": S.get("lumieres", []),
             "visites": S.get("visites", []), "depart": S.get("depart", {"x": 400, "y": 180, "cap": 200}),
             "bornes": [min(xs), min(ys), max(xs), max(ys)], "titre": S.get("titre", M["projet"].get("proposition", "")),
             "projet": M["projet"]["nom"], "palette": S.get("palette", []),
             "tremies": tremies, "obstacles": obstacles, "peintures": S.get("peintures", {})}
    scene["materiaux"] = bibliotheque(scene, S)
    scene["modeles_glb"], scene["modeles_info"], scene["credits"] = modeles(scene)
    # photos et cadres : SCENE["images"] = {clé: chemin relatif au projet}. Un fichier absent (ex. dossier renovation/prive/,
    # gardé hors du dépôt) est simplement omis : le cadre reste, vide. SANS_PRIVE=1 force l'omission (version à committer).
    scene["images"] = {}
    for cle, rel in (S.get("images") or {}).items():
        f = os.path.normpath(os.path.join(dossier, rel))
        if os.path.isfile(f) and not os.environ.get("SANS_PRIVE"):
            mime = "image/png" if f.lower().endswith(".png") else "image/jpeg"
            scene["images"][cle] = f"data:{mime};base64," + base64.b64encode(open(f, "rb").read()).decode()
        else:
            print(f"  image {cle} omise ({rel})")
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
