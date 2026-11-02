#!/usr/bin/env python3
"""Maquette 3D visitable d'un projet de rénovation : <projet>/3d/visite.html (un seul fichier, three.js).

Lit <projet>/donnees/maison.json (produit par construire_projet.py) et, s'il existe, <projet>/scene_3d.py
(mobilier, matériaux par pièce, hauteur de plafond). Les textures (Poly Haven, CC0) sont intégrées au fichier.
Facultatif : SCENE["commandes"] (toile motorisée, stores...) rend des objets du mobilier mobiles dans la visite (voir commandes()).

Portes : chaque porte battante ou coulissante devient un objet qu'on ouvre et ferme en le touchant (voir battant()) ; état de
départ = celui dessiné (« fermee » ou ouverte à 90°). Un objet du mobilier qui porte "porte": id d'ouverture pivote avec elle.

Plusieurs étages (opt-in) : SCENE = {"titre", "etages": [scène SS, scène RDC], "depart": {..., "etage": "SS"}}, chaque scène
d'étage complète (comme aujourd'hui, avec son "niveau"). Chaque étage est construit avec la géométrie de son niveau de
maison.json, le RDC est posé à la hauteur d'étage du sous-sol (SCENE SS "hauteur_etage"), puis tout est fusionné en une
seule scène : S["etages"] (géométrie par étage), visites, palettes, peintures, commandes, images, modèles et matériaux.
L'escalier du sous-sol devient praticable (grille de hauteurs + ligne de foulée), le plancher du RDC est troué à la trémie
avec un garde-corps de verre. Un projet sans "etages" garde exactement la même scène (à part les portes interactives).

Fenêtres (opt-in) : SCENE["fenetres"] = {id d'ouverture: {"allege": z, "tete": z}} donne à une fenêtre sa propre allège
et sa propre tête (sinon SCENE["allege_fenetre"] / "tete_fenetre" de l'étage) ; une fenêtre descendue sous le terrain reçoit
une margelle et le terrain est troué au ras de la maison (voir reglages_fenetres). Sans "fenetres", rien ne change.

Poids et mémoire : images de couleur des matériaux à 512 px au plus (TEX_COULEUR=1024 pour les garder plus fines), cartes de
relief à 512 px (TEX_RELIEF), de rugosité à 256 px (TEX_RUGOSITE), photos à 720 px (PHOTO_MAX). La scène est passée à JSON.parse (chaîne JSON).

Extérieur (opt-in, plusieurs étages) : SCENE["exterieur"] (terrain, cour, enveloppe de la maison ; voir preparer_exterieur) :
on marche dehors et on entre par les portes extérieures ; la maquette gagne une vue « Extérieur ».

Usage : python3 renovation/outils/generer_3d.py renovation/SS-02_aire_ouverte_gym_vitre [sortie.html]
(sortie facultative : par défaut <projet>/3d/visite.html)
"""
import base64, copy, importlib.util, io, json, math, os, sys

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


def reglages_fenetres(S, niv, sill, head, H):
    """Allège et tête par fenêtre (opt-in) : SCENE["fenetres"] = {id d'ouverture: {"allege": z, "tete": z}} (pouces,
    repère du plancher), pour une fenêtre agrandie ou réduite ; les autres gardent SCENE["allege_fenetre"] / "tete_fenetre".
    Servent partout : trou dans le mur, vitre, cadre, meneaux, tablette, jambages, lumière du jour (la visionneuse suit la
    vitre) et terrain extérieur. Clés facultatives :
    - "sections" : nombre de châssis (meneaux verticaux également répartis ; défaut 2 = un meneau au centre, comme avant) ;
    - "traverses" : [z, ...] traverses horizontales (ex. un panneau fixe en bas) ;
    - "margelle" : puits de fenêtre devant une fenêtre dont l'allège tombe sous le terrain (sol_exterieur + 2 po) :
      ajoutée d'office dans ce cas ; False = jamais ; True ou {"saillie": 36, "debord": 6, "fond": allège - 8,
      "dessus": terrain + 4, "mat": "beton", "mat_fond": "beton"} pour la forcer ou la régler (saillie depuis la face
      extérieure du mur, débord de chaque côté de la fenêtre). Le terrain est alors troué au ras de la maison et des margelles.
    Retourne {id: réglages complets} ; erreur explicite si les données ne respectent pas ce contrat. Sans "fenetres" : {}."""
    reg = S.get("fenetres")
    if not reg:
        return {}

    def err(msg):
        raise SystemExit(f'scene_3d.py, fenetres (niveau {niv["id"]}) : ' + msg)
    if not isinstance(reg, dict):
        err('SCENE["fenetres"] doit être un dictionnaire {"<id de fenêtre>": {"allege": z, "tete": z}}')
    ids = [o["id"] for o in niv["ouvertures"] if o["type"] == "fenetre"]
    num = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
    out = {}
    for oid, r in reg.items():
        if oid not in ids:
            err(f'"{oid}" n\'est pas une fenêtre de ce niveau (fenêtres : {", ".join(ids) or "aucune"})')
        if not isinstance(r, dict):
            err(f'"{oid}" : réglages attendus sous forme de dictionnaire, reçu {r!r}')
        inconnues = set(r) - {"allege", "tete", "sections", "traverses", "margelle", "note"}
        if inconnues:
            err(f'"{oid}" : clé(s) inconnue(s) {", ".join(sorted(inconnues))}')
        a, t = r.get("allege", sill), r.get("tete", head)
        if not num(a) or not num(t) or not 0 <= a < t <= H:
            err(f'"{oid}" : il faut 0 <= allège < tête <= plafond ({H} po), reçu allège {a!r}, tête {t!r}')
        n = r.get("sections", 2)
        if not isinstance(n, int) or isinstance(n, bool) or n < 1:
            err(f'"{oid}" : "sections" doit être un entier >= 1, reçu {n!r}')
        tr = r.get("traverses", [])
        if not isinstance(tr, list) or not all(num(z) and a + 2 < z < t - 2 for z in tr):
            err(f'"{oid}" : "traverses" doit être une liste de z entre l\'allège et la tête (à 2 po près), reçu {tr!r}')
        mg = r.get("margelle")
        if mg is not None and not isinstance(mg, (bool, dict)):
            err(f'"{oid}" : "margelle" doit valoir True, False ou un dictionnaire, reçu {mg!r}')
        if isinstance(mg, dict):
            for k, v in mg.items():
                if k in ("mat", "mat_fond"):
                    if not isinstance(v, str):
                        err(f'"{oid}" : margelle, "{k}" doit être une clé de matériau, reçu {v!r}')
                elif k not in ("saillie", "debord", "fond", "dessus") or not num(v):
                    err(f'"{oid}" : margelle, clé "{k}" inconnue ou valeur non numérique ({v!r})')
        out[oid] = dict(r, allege=a, tete=t, sections=n, traverses=list(tr))
    return out


def allege_tete(o, sill, head, fen):
    """(allège, tête) d'une ouverture : réglage de SCENE["fenetres"] s'il y en a un, sinon ceux de l'étage."""
    r = (fen or {}).get(o.get("id")) if o.get("type") == "fenetre" else None
    return (r["allege"], r["tete"]) if r else (sill, head)


def fonction_relief(R):
    """Relief du terrain (SCENE["exterieur"]["relief"] = {"xs", "ys", "z"}, grille non uniforme, z absolu) : fonction
    (x, y) -> z, ou None hors de la grille. Chaque case est coupée en deux triangles par sa diagonale (xs[i], ys[j]) ->
    (xs[i+1], ys[j+1]) : les mêmes triangles que le rendu et la marche de la visionneuse (zTerrain du gabarit)."""
    if not R:
        return None
    import bisect
    xs, ys, Z = R["xs"], R["ys"], R["z"]

    def f(x, y):
        if not (xs[0] <= x <= xs[-1] and ys[0] <= y <= ys[-1]):
            return None
        i = min(max(bisect.bisect_right(xs, x) - 1, 0), len(xs) - 2)
        j = min(max(bisect.bisect_right(ys, y) - 1, 0), len(ys) - 2)
        u, v = (x - xs[i]) / (xs[i + 1] - xs[i]), (y - ys[j]) / (ys[j + 1] - ys[j])
        z00, z10, z01, z11 = Z[j][i], Z[j][i + 1], Z[j + 1][i], Z[j + 1][i + 1]
        return z00 + u * (z10 - z00) + v * (z11 - z10) if u >= v else z00 + v * (z01 - z00) + u * (z11 - z01)
    return f


def margelles(niv, par_mur, fen, sol_ext, centre):
    """Margelles (puits de fenêtre) devant les fenêtres de SCENE["fenetres"] dont l'allège tombe sous le terrain :
    fond de gravier, trois parois, et leurs rectangles (pour trouer le terrain). Retourne (boîtes, rectangles).
    sol_ext : z du terrain (repère de l'étage), un nombre ou une fonction (x, y) -> z (relief de l'extérieur, lu devant
    chaque fenêtre ; None hors du relief : on prend alors son attribut « defaut »)."""
    boites, rects = [], []
    murs = {m["id"]: m for m in niv["murs"]}
    for mid, ouvs in par_mur.items():
        m = murs.get(mid)
        if not m or m["type"] not in ("fondation", "ext"):
            continue
        t = (m.get("epaisseur") or {}).get("valeur") or 4.5
        L = math.hypot(m["x2"] - m["x1"], m["y2"] - m["y1"])
        ux, uy = (m["x2"] - m["x1"]) / L, (m["y2"] - m["y1"]) / L
        horiz = abs(ux) > 0.5
        nx, ny = (0, math.copysign(1, m["y1"] - centre[1])) if horiz else (math.copysign(1, m["x1"] - centre[0]), 0)   # vers l'extérieur
        for o in ouvs:
            r = fen.get(o["id"]) if o["type"] == "fenetre" else None
            if not r:
                continue
            c, w = o["position"]["valeur"], o["largeur"]["valeur"]
            sol = sol_ext
            if callable(sol_ext):                   # relief : sol devant le milieu de la fenêtre, à 6 po du mur
                q = sol_ext(m["x1"] + ux * c + nx * (t / 2 + 6), m["y1"] + uy * c + ny * (t / 2 + 6))
                sol = q if q is not None else getattr(sol_ext, "defaut", 48)
            if r.get("margelle") is False or (r.get("margelle") is None and r["allege"] >= sol + 2):
                continue
            g = r["margelle"] if isinstance(r.get("margelle"), dict) else {}
            P, e, ep = g.get("saillie", 36), g.get("debord", 6), 1.5
            zf, zh = g.get("fond", r["allege"] - 8), g.get("dessus", sol + 4)
            a, b, f = c - w / 2 - e, c + w / 2 + e, t / 2          # le long du mur ; face extérieure à t/2 de l'axe

            def bx(s0, s1, q0, q1, z0, z1, mat):                    # s le long du mur, q vers l'extérieur depuis l'axe
                pa = (m["x1"] + ux * s0 + nx * q0, m["y1"] + uy * s0 + ny * q0)
                pb = (m["x1"] + ux * s1 + nx * q1, m["y1"] + uy * s1 + ny * q1)
                return {"x0": round(min(pa[0], pb[0]), 3), "x1": round(max(pa[0], pb[0]), 3), "y0": round(min(pa[1], pb[1]), 3),
                        "y1": round(max(pa[1], pb[1]), 3), "z0": z0, "z1": z1, "mat": mat}
            mat, fond = g.get("mat", "beton"), g.get("mat_fond", g.get("mat", "beton"))
            boites += [bx(a, b, f, f + P, zf - 2, zf, fond),                                   # fond (gravier drainant)
                       bx(a - ep, a, f, f + P + ep, zf - 2, zh, mat), bx(b, b + ep, f, f + P + ep, zf - 2, zh, mat),   # côtés
                       bx(a, b, f + P, f + P + ep, zf - 2, zh, mat)]                           # paroi du fond
            q = bx(a - ep, b + ep, f - 0.5, f + P + ep, 0, 0, "")
            rects.append([[q["x0"], q["y0"]], [q["x1"], q["y0"]], [q["x1"], q["y1"]], [q["x0"], q["y1"]]])
    return boites, rects


def empreinte(niv):
    """Emprise d'un niveau (géométrie shapely) : intérieur et murs extérieurs jusqu'à leur face extérieure (murs de fondation,
    sinon murs « ext »). Sert à trouer le terrain et, dehors, à savoir si un point est dans la maison."""
    from shapely.geometry import LineString, Polygon
    from shapely.ops import unary_union
    murs = [m for m in niv["murs"] if m["type"] == "fondation"] or [m for m in niv["murs"] if m["type"] == "ext"]
    U = unary_union([LineString([(m["x1"], m["y1"]), (m["x2"], m["y2"])]).buffer(
        ((m.get("epaisseur") or {}).get("valeur") or 4.5) / 2, cap_style=3, join_style=2) for m in murs])
    return unary_union([Polygon(p.exterior) for p in (U.geoms if hasattr(U, "geoms") else [U])])


def contours(G, mini=1):
    """Contours extérieurs (listes de [x, y] arrondis) des polygones d'une géométrie shapely."""
    return [[[round(x, 2), round(y, 2)] for x, y in list(p.exterior.coords)[:-1]]
            for p in (G.geoms if hasattr(G, "geoms") else [G]) if p.geom_type == "Polygon" and p.area > mini]


def terrain_trou(niv, rects):
    """Contour(s) du trou du terrain : emprise de la maison (faces extérieures des murs) plus les margelles."""
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    return contours(unary_union([empreinte(niv)] + [Polygon(r) for r in rects]))


def boites_mur(m, ouvs, H, sill, head, fen=None):
    """Découpe un mur (axe, épaisseur) en boîtes pleines autour de ses ouvertures. Pouces, repère maison.
    fen : {id de fenêtre: {"allege", "tete", ...}} (SCENE["fenetres"], voir reglages_fenetres) ; sinon sill / head."""
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
        sl, hd = allege_tete(o, sill, head, fen)
        trous.append((c - w / 2, c + w / 2, 0 if porte else sl, 80 if porte else hd, o))
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


def cage_tremie(rects, H, etage, multi=False):
    """Réunit les trémies (rectangles qui se touchent) en polygones ; murs de la cage au-dessus du plafond.
    multi (maquette à plusieurs étages) : la cage s'arrête au plancher de l'étage du dessus, sans couvercle."""
    from shapely.geometry import box
    from shapely.ops import unary_union
    from shapely.geometry.polygon import orient
    u = unary_union([box(*r) for r in rects]).buffer(0)
    polys, boites = [], []
    for p in (u.geoms if hasattr(u, "geoms") else [u]):
        p = orient(p.simplify(0.01), 1.0)
        pts = [list(q) for q in list(p.exterior.coords)[:-1]]
        polys.append(pts)
        zh = etage if multi else H + etage
        for (xa, ya), (xb, yb) in zip(pts, pts[1:] + pts[:1]):   # sens antihoraire : l'extérieur est à droite
            if abs(ya - yb) < 0.01:
                y = ya - 2 if xb > xa else ya
                boites.append({"x0": min(xa, xb) - 2, "x1": max(xa, xb) + 2, "y0": y, "y1": y + 2, "z0": H + 0.2, "z1": zh, "mat": "gypse"})
            else:
                x = xa if yb > ya else xa - 2
                boites.append({"x0": x, "x1": x + 2, "y0": min(ya, yb) - 2, "y1": max(ya, yb) + 2, "z0": H + 0.2, "z1": zh, "mat": "gypse"})
        if not multi:
            mx0, my0, mx1, my1 = p.bounds
            boites.append({"x0": mx0 - 2, "x1": mx1 + 2, "y0": my0 - 2, "y1": my1 + 2, "z0": H + etage, "z1": H + etage + 1, "mat": "plafond"})
    return polys, boites


TEX_COULEUR = int(os.environ.get("TEX_COULEUR", 512))     # côté max. des images de couleur des matériaux (px)
TEX_RELIEF = int(os.environ.get("TEX_RELIEF", 512))       # côté max. des cartes de relief (px)
TEX_RUGOSITE = int(os.environ.get("TEX_RUGOSITE", 256))   # côté max. des cartes de rugosité (variations douces : 256 px suffisent)
PHOTO_MAX = int(os.environ.get("PHOTO_MAX", 720))         # côté max. des photos accrochées aux murs (px)


def reduire(octets, max_px, qualite=84):
    """Image ramenée à max_px de côté au plus (JPEG). Déjà assez petite : octets inchangés."""
    from PIL import Image
    im = Image.open(io.BytesIO(octets))
    if max(im.size) <= max_px:
        return octets
    if im.mode in ("RGBA", "LA", "P") and "A" in im.getbands():
        return octets                                          # transparence : on n'y touche pas
    f = max_px / max(im.size)
    im = im.convert("RGB").resize((max(1, round(im.size[0] * f)), max(1, round(im.size[1] * f))), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=qualite, optimize=True)
    return buf.getvalue() if len(buf.getvalue()) < len(octets) else octets


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
        # couleur : TEX_COULEUR px au plus (512 par défaut : 4 fois moins de mémoire graphique, page plus légère) ;
        # relief : 512 px au plus ; rugosité : 256 px
        uri = lambda f, mx=TEX_RELIEF: "data:image/jpeg;base64," + base64.b64encode(reduire(open(os.path.join(d, f), "rb").read(), mx)).decode()
        m = {"taille_m": e["taille_m"], "relief": uri("relief.jpg"), "metal": e.get("metal", 0)}
        for k in ("vernis", "vernis_rugosite", "duvet"):      # fini de rendu (clearcoat, sheen), optionnel
            if k in e:
                m[k] = e[k]
        if e.get("relief_seul"):
            m["relief_seul"] = True
        else:
            m["couleur"] = uri("couleur.jpg", TEX_COULEUR)
        if "rugosite" in e:
            m["rugosite"] = e["rugosite"]
        elif os.path.isfile(os.path.join(d, "rugosite.jpg")):
            m["carte_rugosite"] = uri("rugosite.jpg", TEX_RUGOSITE)
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
                                b[kk] = v - s_ * (o[k + "1"] - o[k + "0"]) / 2   # le bout de cloison s'arrête au milieu du mur traversé (plus de ligne aux jonctions en T)


def finitions(niv, par_mur, H, sill, head, S, fen=None):
    """Plinthes, chambranles et seuils des portes, cadres, meneaux et tablettes des fenêtres (fen : voir reglages_fenetres)."""
    sol = S.get("sol_defaut", "chene")
    sill0, head0 = sill, head
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
                sill, head = allege_tete(o, sill0, head0, fen)
                r = (fen or {}).get(o["id"]) or {}
                n = r.get("sections", 2)
                meneaux = [(a + b) / 2] if n == 2 else [a + (b - a) * k / n for k in range(1, n)]
                out += [b_(a, b, -d / 2, d / 2, sill, sill + f, "metal"), b_(a, b, -d / 2, d / 2, head - f, head, "metal"),
                        b_(a, a + f, -d / 2, d / 2, sill, head, "metal"), b_(b - f, b, -d / 2, d / 2, sill, head, "metal")]
                out += [b_(xm - 0.75, xm + 0.75, -d / 2, d / 2, sill, head, "metal") for xm in meneaux]
                out += [b_(a, b, -d / 2, d / 2, z - 0.75, z + 0.75, "metal") for z in r.get("traverses", [])]
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


def bbox_objet(o):
    """Emprise (x0, y0, x1, y1, z0, z1) d'un objet du mobilier aux coordonnées explicites, sinon None."""
    f = o.get("forme", "boite")
    if f in ("boite", "arrondi") and all(k in o for k in ("x0", "x1", "y0", "y1", "z0", "z1")) and not o.get("pts"):
        return o["x0"], o["y0"], o["x1"], o["y1"], o["z0"], o["z1"]
    if f == "cylindre" and "r" in o:
        if o.get("axe") == "y":
            return o["x"] - o["r"], o["y0"], o["x"] + o["r"], o["y1"], o["z"] - o["r"], o["z"] + o["r"]
        if o.get("axe") == "x":
            return o["x0"], o["y"] - o["r"], o["x1"], o["y"] + o["r"], o["z"] - o["r"], o["z"] + o["r"]
        if "z0" in o:
            return o["x"] - o["r"], o["y"] - o["r"], o["x"] + o["r"], o["y"] + o["r"], o["z0"], o["z1"]
    if f == "sphere" and "r" in o:
        return o["x"] - o["r"], o["y"] - o["r"], o["x"] + o["r"], o["y"] + o["r"], o["z"] - o["r"], o["z"] + o["r"]
    if f == "tube" and o.get("pts"):
        xs, ys, zs = zip(*[(p[0], p[1], p[2]) for p in o["pts"]])
        r = o.get("r", 0)
        return min(xs) - r, min(ys) - r, max(xs) + r, max(ys) + r, min(zs) - r, max(zs) + r
    return None


def battant(m, o, t, mobilier):
    """Porte interactive : vantail à l'état FERMÉ (boîtes, repère maison) et son mouvement.
    Battante : rotation de "angle" degrés (sens antihoraire en plan) autour de "pivot" (charnière, au nu du mur du côté où
    la porte pousse) ; coulissante : translation "glisse" [dx, dy] (dans le mur si la place y est : porte escamotable,
    sinon le long de la face du mur ou de la cloison vitrée). "etat" de départ = celui dessiné (« fermee » ou ouverte) ;
    "zone" = baie dans le mur (une porte fermée y bloque la marche). Porte « fermee » cachée derrière un meuble qui la
    couvre (porte-bibliothèque) : ce mobilier pivote avec elle (clé "porte" ajoutée à l'objet). Retourne None sans porte."""
    op = o.get("operation") or "battante"
    if op == "aucune" or o.get("position", {}).get("valeur") is None or o.get("largeur", {}).get("valeur") is None:
        return None
    x1, y1, x2, y2 = m["x1"], m["y1"], m["x2"], m["y2"]
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    nx, ny = -uy, ux
    c, w = o["position"]["valeur"], o["largeur"]["valeur"]
    a, b = c - w / 2, c + w / 2
    s = o.get("sens") or {}
    side = 1 if s.get("ouvre_vers", "gauche") == "gauche" else -1
    pt = lambda al, ac: (x1 + ux * al + nx * ac, y1 + uy * al + ny * ac)

    def bx(al0, al1, ac0, ac1, z0, z1, mat):
        p0, p1 = pt(al0, ac0), pt(al1, ac1)
        return {"x0": round(min(p0[0], p1[0]), 3), "x1": round(max(p0[0], p1[0]), 3), "y0": round(min(p0[1], p1[1]), 3),
                "y1": round(max(p0[1], p1[1]), 3), "z0": z0, "z1": z1, "mat": mat}
    z = bx(a, b, -t / 2 - 0.5, t / 2 + 0.5, 0, 0, "")
    zone = [z["x0"], z["y0"], z["x1"], z["y1"]]
    verre = o.get("materiau") == "verre"
    exterieure = m["type"] != "int" and not o.get("interieure")
    mat = "porte-verre" if verre else "porte" if o.get("fermee") or not exterieure else "porte-ext"
    out = {"id": o["id"], "zone": zone, "etat": "fermee" if (o.get("fermee") or (exterieure and not verre)) else "ouverte"}

    def vantail(al0, al1, ac0, ac1):
        """Vantail (porte pleine, ou vitrée dans un cadre noir de 1½ po) entre al0 < al1 et ac0 < ac1."""
        if not verre:
            return [bx(al0, al1, ac0, ac1, 0.5, 80, mat)]
        k = 1.5
        mi = (ac0 + ac1) / 2
        return [bx(al0 + k, al1 - k, mi - 0.3, mi + 0.3, 2, 78.5, "porte-verre"),
                bx(al0, al0 + k, ac0, ac1, 0.5, 80, "metal"), bx(al1 - k, al1, ac0, ac1, 0.5, 80, "metal"),
                bx(al0, al1, ac0, ac1, 0.5, 2, "metal"), bx(al0, al1, ac0, ac1, 78.5, 80, "metal")]

    if op == "coulissante":
        # place libre dans le mur de chaque côté de la baie (jusqu'à la prochaine ouverture ou au bout du mur)
        out["type"] = "coulissante"
        autres = [((q["position"]["valeur"] - q["largeur"]["valeur"] / 2), (q["position"]["valeur"] + q["largeur"]["valeur"] / 2))
                  for q in m.get("_ouvertures", []) if q is not o and q.get("position", {}).get("valeur") is not None]
        lib_d = a - max([q1 for q0, q1 in autres if q1 <= a + 0.1] + [0])
        lib_f = min([q0 for q0, q1 in autres if q0 >= b - 0.1] + [L]) - b
        dirg = 1 if lib_f >= lib_d else -1
        dans_mur = m.get("materiau") != "verre" and not verre and max(lib_d, lib_f) >= w and t >= 3.5
        ac0, ac1 = (-0.7, 0.7) if dans_mur else sorted([side * (t / 2 + 0.6), side * (t / 2 + 2.0)])
        al0, al1 = (a + 0.25, b - 0.25) if dans_mur else (a - 1, b + 1)
        out["boites"] = vantail(al0, al1, ac0, ac1)
        if not dans_mur:                                       # poignée creuse côté pièce
            out["boites"].append(bx(*sorted([b - 4 if dirg > 0 else a + 3, b - 3 if dirg > 0 else a + 4]),
                                    *sorted([side * (t / 2 + 2.0), side * (t / 2 + 2.6)]), 34, 42, "metal"))
        d = (w - 0.5) if dans_mur else (w - 1)
        out["pivot"] = [round(v, 3) for v in pt(c, 0)]
        out["glisse"] = [round(ux * dirg * d, 3), round(uy * dirg * d, 3)]
        return out

    out["type"] = "battante"
    sgn = 1 if s.get("charniere", "debut") == "debut" else -1
    ah = a if sgn > 0 else b                                   # charnière (le long du mur)
    e = 1.8
    acs = sorted([side * (t / 2 - e), side * t / 2])
    als = sorted([ah + sgn * 0.5, ah + sgn * (w - 0.5)])
    boites = vantail(als[0], als[1], acs[0], acs[1])
    # béquilles des deux côtés, à 4 po du bord libre
    q = ah + sgn * (w - 4)
    pm = "inox" if mat == "porte-ext" else "metal"
    boites += [bx(q - 0.5, q + 0.5, *sorted([side * t / 2, side * (t / 2 + 2.2)]), 36, 38, pm),
               bx(q - 0.5, q + 0.5, *sorted([side * (t / 2 - e), side * (t / 2 - e - 2.2)]), 36, 38, pm)]
    pivot = pt(ah + sgn * 0.5, side * t / 2)
    # porte « fermee » couverte par un meuble (porte-bibliothèque) : le meuble fait partie du battant
    lies = [ob for ob in mobilier if ob.get("porte") == o["id"]]
    if o.get("fermee") and not lies:
        cand = []
        for ob in mobilier:
            bb = bbox_objet(ob)
            if not bb or ob.get("commande") or ob.get("porte"):
                continue
            p0, p1 = (bb[0] - x1) * ux + (bb[1] - y1) * uy, (bb[2] - x1) * ux + (bb[3] - y1) * uy
            q0, q1 = (bb[0] - x1) * nx + (bb[1] - y1) * ny, (bb[2] - x1) * nx + (bb[3] - y1) * ny
            al_lo, al_hi, ac_lo, ac_hi = min(p0, p1), max(p0, p1), min(q0, q1), max(q0, q1)
            if al_lo >= a - 1.5 and al_hi <= b + 1.5 and bb[4] < 80 and bb[5] <= 84 and ac_lo >= -t / 2 - 12 and ac_hi <= t / 2 + 12:
                cand.append((ob, al_lo, al_hi, side * ac_lo, side * ac_hi, bb))
        # couvre la baie du côté où la porte pousse, sur au moins 70 % de la largeur et 60 po de haut
        devant = sorted((max(a, c_[1]), min(b, c_[2])) for c_ in cand if min(c_[3], c_[4]) >= t / 2 - 0.5 and c_[5][5] >= 60)
        couvert, fin = 0, a
        for lo, hi in devant:
            if hi > fin:
                couvert += hi - max(lo, fin); fin = hi
        if couvert >= 0.7 * w:
            lies = [c_[0] for c_ in cand]
            for ob in lies:
                ob["porte"] = o["id"]
    if lies:
        # pivot au coin de l'ensemble (côté charnière, côté où il pousse), pour qu'il tourne sans frotter le cadre
        al_e, ac_e = [], []
        for ob in lies:
            bb = bbox_objet(ob)
            if bb:
                for xx, yy in ((bb[0], bb[1]), (bb[2], bb[3])):
                    al_e.append((xx - x1) * ux + (yy - y1) * uy); ac_e.append(side * ((xx - x1) * nx + (yy - y1) * ny))
        pal = min(al_e + [ah + sgn * 0.5]) if sgn > 0 else max(al_e + [ah + sgn * 0.5])
        pivot = pt(pal, side * max(ac_e + [t / 2]))
    out.update({"pivot": [round(pivot[0], 3), round(pivot[1], 3)], "angle": 90 * side * sgn, "boites": boites})
    return out


def garde_corps(segments):
    """Garde-corps de verre de 36 po : poteaux d'acier noir (au plus 48 po d'entraxe), panneaux de verre clair, main
    courante de chêne. segments = [((xa, ya), (xb, yb))] axe du garde-corps, horizontaux ou verticaux."""
    out = []
    for (xa, ya), (xb, yb) in segments:
        horiz = abs(ya - yb) < 0.01
        lo, hi = sorted([xa, xb] if horiz else [ya, yb])
        f = ya if horiz else xa
        if hi - lo < 4:
            continue
        r = lambda u0, u1, v0, v1, z0, z1, mat: ({"x0": u0, "x1": u1, "y0": f + v0, "y1": f + v1, "z0": z0, "z1": z1, "mat": mat} if horiz else
                                                 {"x0": f + v0, "x1": f + v1, "y0": u0, "y1": u1, "z0": z0, "z1": z1, "mat": mat})
        n = max(1, math.ceil((hi - lo) / 48))
        for k in range(n + 1):
            u = lo + (hi - lo) * k / n
            out.append(r(max(lo, u - 1), min(hi, u + 1), -1, 1, 0, 34.5, "metal"))
        out.append(r(lo, hi, -0.25, 0.25, 2, 34, "verre-clair"))
        out.append(r(lo, hi, -0.6, 0.6, 1, 2, "metal"))
        out.append(r(lo, hi, -1.25, 1.25, 34.5, 36, "placage"))
    return out


def garde_corps_tremies(polys, niv, sorties, largeur=36):
    """Garde-corps autour des trémies d'un étage (polygones antihoraires), sauf le long d'un mur (à moins de 7 po) et à
    l'arrivée de l'escalier (sorties : points où la ligne de foulée franchit le bord)."""
    segs = []
    for pts in polys:
        for (xa, ya), (xb, yb) in zip(pts, pts[1:] + pts[:1]):
            horiz = abs(ya - yb) < 0.01
            if not horiz and abs(xa - xb) > 0.01:
                continue
            Lg = math.hypot(xb - xa, yb - ya)
            rx, ry = (yb - ya) / Lg, -(xb - xa) / Lg              # à droite du bord : le plancher
            lo, hi = sorted([xa, xb] if horiz else [ya, yb])
            f = (ya if horiz else xa) + (ry if horiz else rx) * 1.25
            trous = []
            for mm in niv["murs"]:
                mh = abs(mm["y1"] - mm["y2"]) < 0.01
                if mh != horiz or mm.get("materiau") == "garde-corps":
                    continue
                tm = (mm.get("epaisseur") or {}).get("valeur") or 4.5
                mf = mm["y1"] if mh else mm["x1"]
                m0, m1 = sorted([mm["x1"], mm["x2"]] if mh else [mm["y1"], mm["y2"]])
                if abs(mf - f) <= tm / 2 + 7 and m1 > lo and m0 < hi:
                    trous.append((m0 - 2, m1 + 2))
            for sx, sy in sorties:
                d = abs((sy if horiz else sx) - (ya if horiz else xa))
                u = sx if horiz else sy
                if d < 4 and lo - 2 <= u <= hi + 2:
                    trous.append((u - largeur / 2 - 2, u + largeur / 2 + 2))
            morceaux = [(lo, hi)]
            for t0, t1 in trous:
                morceaux = [q for (m0, m1) in morceaux for q in ((m0, min(m1, t0)), (max(m0, t1), m1)) if q[1] - q[0] > 0.01]
            for m0, m1 in morceaux:
                if m1 - m0 >= 6:
                    segs.append(((m0, f), (m1, f)) if horiz else ((f, m0), (f, m1)))
    return garde_corps(segs)


def marche_escalier(e, etage):
    """Escalier praticable (une volée droite, avec ou sans marches tournantes en haut) : grille de hauteurs de 2 po
    (hauteur du pas en pouces au-dessus du plancher du bas, rampe régulière d'un nez de marche au suivant ; -1 hors de
    l'escalier) et ligne de foulée du pied (sur l'étage du bas) jusqu'au palier d'arrivée (sur l'étage du haut)."""
    es = e.get("escalier") or {}
    n = int(round(es["nb_contremarches"]["valeur"]))
    L, W = e["dimensions"]["longueur"]["valeur"], e["dimensions"]["largeur"]["valeur"]
    cx, cy = e["position"]["x"], e["position"]["y"]
    d = {"+y": (0, 1), "-y": (0, -1), "+x": (1, 0), "-x": (-1, 0)}[es.get("direction", "+y")]
    total, depart = int(es.get("total", n)), int(es.get("depart", 0))
    if depart:
        return None                                           # volées en L (palier) : pas encore praticables
    r = etage / total
    girons = int(es.get("girons", n - 1))
    tr = es.get("tournant")
    nb = int(tr["nb"]) if tr else 0
    nd = girons - nb
    pied = (cx - d[0] * L / 2, cy - d[1] * L / 2)
    if tr:
        Lc = (tr["carre"][3] - tr["carre"][1]) if d[0] == 0 else (tr["carre"][2] - tr["carre"][0])
        pas = (L - Lc) / nd
        Ls = nd * pas
        px, py = tr["pivot"]
        ray = eventail(tr)
        fin_droit = (pied[0] + d[0] * Ls, pied[1] + d[1] * Ls)
        # le rayon d'entrée est celui qui touche le bout de la volée droite
        def dist(j):                                          # écart angulaire entre le rayon j et le bout de la volée
            vx, vy, fx, fy = ray[j][1][0] - px, ray[j][1][1] - py, fin_droit[0] - px, fin_droit[1] - py
            return abs(math.atan2(vx * fy - vy * fx, vx * fx + vy * fy))
        if dist(len(ray) - 1) < dist(0):
            ray = ray[::-1]
        a0 = math.atan2(ray[0][1][1] - py, ray[0][1][0] - px)
        a1 = math.atan2(ray[-1][1][1] - py, ray[-1][1][0] - px)
        sw = math.atan2(math.sin(a1 - a0), math.cos(a1 - a0))      # ± 90°
        R = math.hypot(fin_droit[0] - px, fin_droit[1] - py)
    else:
        Ls, pas = L, L / max(1, girons)
    x0 = cx - (W / 2 if d[0] == 0 else L / 2); x1 = cx + (W / 2 if d[0] == 0 else L / 2)
    y0 = cy - (L / 2 if d[0] == 0 else W / 2); y1 = cy + (L / 2 if d[0] == 0 else W / 2)
    if tr:
        x0, y0 = min(x0, tr["carre"][0]), min(y0, tr["carre"][1]); x1, y1 = max(x1, tr["carre"][2]), max(y1, tr["carre"][3])
    g = 2.0
    NX, NY = int(math.ceil((x1 - x0) / g)), int(math.ceil((y1 - y0) / g))
    zs = []
    for j in range(NY):
        for i in range(NX):
            x, y = x0 + (i + .5) * g, y0 + (j + .5) * g
            s_ = (x - pied[0]) * d[0] + (y - pied[1]) * d[1]
            t_ = (x - cx) * (-d[1]) + (y - cy) * d[0]
            v = -1
            if -0.01 <= s_ <= Ls + 0.01 and abs(t_) <= W / 2 + 0.01:
                u = s_ / pas if tr else s_ / L * n
                v = u * r
            elif tr and tr["carre"][0] - 0.01 <= x <= tr["carre"][2] + 0.01 and tr["carre"][1] - 0.01 <= y <= tr["carre"][3] + 0.01:
                an = math.atan2(y - py, x - px)
                th = max(0.0, min(1.0, math.atan2(math.sin(an - a0), math.cos(an - a0)) / sw))
                v = (nd + th * (nb + 1)) * r
            zs.append(round(v, 1))
    chemin = [(pied[0] - d[0] * 16, pied[1] - d[1] * 16), pied]
    if tr:
        chemin.append(fin_droit)
        for k in range(1, 7):
            an = a0 + sw * k / 6
            chemin.append((px + R * math.cos(an), py + R * math.sin(an)))
        an = a1 if abs(math.atan2(math.sin(a0 + sw - a1), math.cos(a0 + sw - a1))) < 1e-6 else a0 + sw
        tg = (-math.sin(an) * math.copysign(1, sw), math.cos(an) * math.copysign(1, sw))
        bord = (px + R * math.cos(an), py + R * math.sin(an))
        sortie = (bord[0] + tg[0] * 2, bord[1] + tg[1] * 2)
        chemin.append((bord[0] + tg[0] * 18, bord[1] + tg[1] * 18))
    else:
        haut = (pied[0] + d[0] * L, pied[1] + d[1] * L)
        chemin += [haut, (haut[0] + d[0] * 18, haut[1] + d[1] * 18)]
        sortie = (haut[0] + d[0] * 2, haut[1] + d[1] * 2)
    return {"id": e["id"], "grille": {"x0": round(x0, 3), "y0": round(y0, 3), "pas": g, "nx": NX, "ny": NY, "z": zs},
            "chemin": [[round(p[0], 2), round(p[1], 2)] for p in chemin], "emprise": [x0, y0, x1, y1],
            "sortie": [round(sortie[0], 2), round(sortie[1], 2)], "largeur": W}


def commandes(S):
    """Commandes interactives (opt-in) : SCENE["commandes"] = [{"id", "nom", "libelle_bas", "libelle_haut", "pivot_z",
    "fraction_min", "depart", "duree"}]. Un objet du mobilier porte "commande": id et "anim": "etirer" (défaut, mise à
    l'échelle verticale autour de pivot_z) ou "suivre" (translation, suit le bas de la partie étirée) ; un arrêt de visite
    peut porter "commandes": {id: "haut" | "bas"}. Les données décrivent l'état « bas » (ex. toile déroulée).
    Retourne la liste complétée (valeurs par défaut) ; erreur explicite si les données ne respectent pas ce contrat."""
    def err(msg):
        raise SystemExit("scene_3d.py, commandes : " + msg)
    liste = S.get("commandes") or []
    if not isinstance(liste, list):
        err('SCENE["commandes"] doit être une liste d\'objets {"id": ..., "pivot_z": ...}')
    out, ids = [], set()
    for i, c in enumerate(liste):
        if not isinstance(c, dict) or not c.get("id") or not isinstance(c["id"], str):
            err(f'commande n° {i + 1} sans "id" (texte)')
        cid = c["id"]
        if cid in ids:
            err(f'id "{cid}" en double')
        if not isinstance(c.get("pivot_z"), (int, float)):
            err(f'commande "{cid}" : "pivot_z" manquant ou non numérique (z en pouces du haut de la partie mobile, '
                f'c.-à-d. le bas du boîtier)')
        fmin = c.get("fraction_min", 0.03)
        if not isinstance(fmin, (int, float)) or not 0 < fmin < 1:
            err(f'commande "{cid}" : "fraction_min" doit être entre 0 et 1 (exclus), reçu {fmin!r}')
        if c.get("depart", "haut") not in ("haut", "bas"):
            err(f'commande "{cid}" : "depart" doit valoir "haut" ou "bas", reçu {c.get("depart")!r}')
        duree = c.get("duree", 3.0)
        if not isinstance(duree, (int, float)) or duree < 0:
            err(f'commande "{cid}" : "duree" doit être un nombre de secondes >= 0, reçu {duree!r}')
        ids.add(cid)
        out.append(dict(c, nom=c.get("nom") or cid, libelle_bas=c.get("libelle_bas") or "Descendre",
                        libelle_haut=c.get("libelle_haut") or "Monter", pivot_z=float(c["pivot_z"]),
                        fraction_min=float(fmin), depart=c.get("depart", "haut"), duree=float(duree)))
    lies = {}
    for o in S.get("mobilier", []):
        if "commande" not in o:
            if "anim" in o:
                err(f'objet {o.get("forme", "boite")} avec "anim" sans "commande" : {o}')
            continue
        if o["commande"] not in ids:
            err(f'objet {o.get("forme", "boite")} lié à la commande inconnue "{o["commande"]}" '
                f'(déclarées : {", ".join(sorted(ids)) or "aucune"})')
        if o.get("anim", "etirer") not in ("etirer", "suivre"):
            err(f'objet de la commande "{o["commande"]}" : "anim" doit valoir "etirer" ou "suivre", reçu {o.get("anim")!r}')
        lies[o["commande"]] = lies.get(o["commande"], 0) + 1
    for v in S.get("visites", []):
        for cid, etat in (v.get("commandes") or {}).items():
            if cid not in ids:
                err(f'arrêt de visite « {v.get("nom")} » : commande inconnue "{cid}"')
            if etat not in ("haut", "bas"):
                err(f'arrêt de visite « {v.get("nom")} » : état "{etat}" pour "{cid}" (attendu "haut" ou "bas")')
    for c in out:
        if not lies.get(c["id"]):
            print(f'  commande {c["id"]} : aucun objet du mobilier n\'y est lié ("commande": "{c["id"]}")')
    return out


NOMS_ETAGES = {"SS": "Sous-sol", "RDC": "Rez-de-chaussée", "ETAGE": "Étage", "COMBLES": "Combles"}


def construire(M, S, ctx=None):
    """Scène d'un étage (repère de son plancher). ctx (maquette à plusieurs étages, sinon None) :
    {"bas": True} pour l'étage qui porte l'escalier (escalier praticable, cage arrêtée au plancher du dessus),
    {"trous": [polygones], "sorties": [points]} pour l'étage du dessus (plancher troué à la trémie, garde-corps)."""
    multi = ctx is not None
    niv = next(n for n in M["niveaux"] if n["id"] == S.get("niveau", "SS"))
    H = S.get("plafond", 90)
    sill, head = S.get("allege_fenetre", 56), S.get("tete_fenetre", 86)
    fen = reglages_fenetres(S, niv, sill, head, H)        # allège et tête par fenêtre (opt-in)
    mobilier = S.get("mobilier", [])
    par_mur = {}
    for o in niv["ouvertures"]:
        par_mur.setdefault(o["mur_id"], []).append(o)
    boites, portes, battants = [], [], []
    for m in niv["murs"]:
        if m.get("materiau") == "lattes":
            boites += lattes(m, H)
            continue
        if m.get("materiau") == "garde-corps" or m["type"] == "garde-corps":   # garde-corps dessiné dans les données
            boites += garde_corps([((m["x1"], m["y1"]), (m["x2"], m["y2"]))])
            continue
        bx, t = boites_mur(m, par_mur.get(m["id"], []), H, sill, head, fen)
        boites += bx
        for o in par_mur.get(m["id"], []):
            if o["type"] == "fenetre":
                c, w = o["position"]["valeur"], o["largeur"]["valeur"]
                sl, hd = allege_tete(o, sill, head, fen)
                # vitre de fenêtre : une boîte mince au centre du mur, entre allège et tête
                L = math.hypot(m["x2"] - m["x1"], m["y2"] - m["y1"])
                ux, uy = (m["x2"] - m["x1"]) / L, (m["y2"] - m["y1"]) / L
                a, b = c - w / 2, c + w / 2
                pa = (m["x1"] + ux * a, m["y1"] + uy * a); pb = (m["x1"] + ux * b, m["y1"] + uy * b)
                if abs(ux) > 0.5:
                    boites.append({"x0": min(pa[0], pb[0]), "x1": max(pa[0], pb[0]), "y0": m["y1"] - 0.5, "y1": m["y1"] + 0.5, "z0": sl, "z1": hd, "mat": "vitre"})
                else:
                    boites.append({"x0": m["x1"] - 0.5, "x1": m["x1"] + 0.5, "y0": min(pa[1], pb[1]), "y1": max(pa[1], pb[1]), "z0": sl, "z1": hd, "mat": "vitre"})
            else:
                # porte battante ou coulissante : objet interactif (ouvrir, fermer), dessiné dans l'état du plan
                bt = battant(dict(m, _ouvertures=par_mur.get(m["id"], [])), o, t, mobilier)
                if bt:
                    battants.append(bt)
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
                           "z0": H - 10.03, "z1": H, "mat": S.get("mat_poutre", "gypse")})
    # escaliers projetés : marches, trémie dans le plafond, cage au-dessus, obstacle pour la visite
    rects, obstacles, escaliers, descentes = [], [], [], []
    etage = S.get("hauteur_etage", 105)
    trous = (ctx or {}).get("trous") or []
    for e in niv["elements"]:
        if e["type"] == "escalier" and e.get("etat") == "nouveau":
            if trous and ((e.get("escalier") or {}).get("fleche") == "DESCEND" or any(
                    _dans_poly(p, e["position"]["x"], e["position"]["y"]) for p in trous)):
                continue                             # arrivée de l'escalier du dessous : le plancher est troué (plus bas)
            if not multi and (e.get("escalier") or {}).get("fleche") == "DESCEND":
                descentes.append(e)                  # étage seul : l'escalier descend sous le plancher (voir plus bas)
                continue
            bx, tr, ob = escalier(e, H, etage)
            if multi:                                # marches et obstacles de l'escalier n° k (praticable dans la visite)
                k = len(escaliers)
                for q in bx + ob:
                    q["esc"] = k
                me = marche_escalier(e, etage)
                if me:
                    escaliers.append(me)
            boites += bx; rects.append(tr); obstacles += ob
        elif e.get("palier") and e.get("etat") == "nouveau":
            bx, tr, ob = palier(e, H, etage)
            boites += bx; obstacles.append(ob)
            if tr:
                rects.append(tr)
    tremies, cage = cage_tremie(rects, H, etage, multi) if rects else ([], [])
    boites += cage
    if descentes:
        # étage seul (ETAGE=RDC) avec l'arrivée d'un escalier qui descend : plancher troué, garde-corps, et l'escalier
        # dessiné sous le plancher dans une cage fermée (comme le construira l'étage du dessous)
        rd, sorties = [], []
        hb = S.get("plafond_dessous", 96)
        for e in descentes:
            e2 = copy.deepcopy(e)
            e2["escalier"]["direction"] = {"+y": "-y", "-y": "+y", "+x": "-x", "-x": "+x"}[e2["escalier"].get("direction", "+y")]
            bx, tr, _ = escalier(e2, hb, etage)
            me = marche_escalier(e2, etage)
            if me:
                sorties.append(me["sortie"])
            xs_ = [q for b in bx for q in ([b["x0"], b["x1"]] if "x0" in b else [p_[0] for p_ in b["pts"]])]
            ys_ = [q for b in bx for q in ([b["y0"], b["y1"]] if "y0" in b else [p_[1] for p_ in b["pts"]])]
            x0_, y0_, x1_, y1_ = min(xs_), min(ys_), max(xs_), max(ys_)
            for b in bx:
                b["z0"] -= etage; b["z1"] -= etage
            boites += bx + [dict(q, z0=-etage, z1=-0.2, mat="gypse") for q in (
                {"x0": x0_ - 2, "x1": x1_ + 2, "y0": y0_ - 2, "y1": y0_}, {"x0": x0_ - 2, "x1": x1_ + 2, "y0": y1_, "y1": y1_ + 2},
                {"x0": x0_ - 2, "x1": x0_, "y0": y0_, "y1": y1_}, {"x0": x1_, "x1": x1_ + 2, "y0": y0_, "y1": y1_})]
            boites.append({"x0": x0_, "x1": x1_, "y0": y0_, "y1": y1_, "z0": -etage - 1, "z1": -etage, "mat": "beton"})
            rd.append(tr)
        trous, cage_d = cage_tremie(rd, hb, etage, True)
        for b in cage_d:
            b["z0"] -= etage; b["z1"] -= etage
        boites += cage_d
        ctx_sorties = sorties
    else:
        ctx_sorties = (ctx or {}).get("sorties") or []
    if trous:                                         # étage du dessus : garde-corps autour de la trémie
        boites += garde_corps_tremies(trous, niv, ctx_sorties)
    boites = couper_aux_cloisons(boites, niv)
    reculer_bouts_de_murs(boites)
    finis = finitions(niv, par_mur, H, sill, head, S, fen)
    # SCENE["mats_finitions"] = {matériau de base: matériau du catalogue} : portes, chambranles, plinthes et cadres de
    # fenêtres d'une autre essence (ex. pin teint au rez-de-chaussée) ; absent = rendu inchangé
    for b in finis + portes + [q for bt in battants for q in bt["boites"]]:
        b["mat"] = (S.get("mats_finitions") or {}).get(b["mat"], b["mat"])
    peindre(boites, niv["pieces"], S)
    mats = S.get("sols", {})
    sols = []
    for p in niv["pieces"]:
        pts = p["polygone"]
        s = {"id": p["id"], "nom": p["nom"], "pts": pts, "mat": mats.get(p["id"], S.get("sol_defaut", "chene")),
             "cx": sum(q[0] for q in pts) / len(pts), "cy": sum(q[1] for q in pts) / len(pts)}
        sols += _trouer_sol(s, trous) if trous else [s]
    empreinte = []
    for m in niv["murs"]:
        if m["type"] == "fondation":
            empreinte += [[m["x1"], m["y1"]], [m["x2"], m["y2"]]]
    if not empreinte:                                     # rez-de-chaussée : murs extérieurs (« ext ») au lieu de la fondation
        empreinte = [q for m in niv["murs"] if m["type"] == "ext" for q in ([m["x1"], m["y1"]], [m["x2"], m["y2"]])]
    xs = [q[0] for q in empreinte]; ys = [q[1] for q in empreinte]
    scene = {"H": H, "boites": boites + finis, "portes": portes, "sols": sols, "mobilier": mobilier,
             "revetements": S.get("revetements", []), "lumieres": S.get("lumieres", []),
             "visites": S.get("visites", []), "depart": S.get("depart", {"x": 400, "y": 180, "cap": 200}),
             "bornes": [min(xs), min(ys), max(xs), max(ys)], "titre": S.get("titre", M["projet"].get("proposition", "")),
             "projet": M["projet"]["nom"], "palette": S.get("palette", []),
             "tremies": tremies, "obstacles": obstacles, "peintures": S.get("peintures", {})}
    if battants:
        scene["battants"] = battants
    if multi or trous:
        scene["trous"] = [[list(q) for q in p] for p in trous]
    if multi:
        scene["escaliers"] = escaliers
    # terrain extérieur vu par les fenêtres (pouces, repère du plancher) : un peu sous l'allège au sous-sol
    scene["sol_exterieur"] = S.get("sol_exterieur", sill - 8 if niv["id"] == "SS" else -30)
    if fen:
        # fenêtres descendues sous le terrain : margelles, et terrain troué au ras de la maison et des margelles
        mb, mr = margelles(niv, par_mur, fen, (ctx or {}).get("sol_relief") or scene["sol_exterieur"], ((xs and (min(xs) + max(xs)) / 2) or 228,
                                                                         (ys and (min(ys) + max(ys)) / 2) or 190))
        if mb:
            scene["boites"] += mb
            scene["terrain_trou"] = terrain_trou(niv, mr)
    return scene


def _dans_poly(pts, x, y):
    c = False
    for i in range(len(pts)):
        (xi, yi), (xj, yj) = pts[i], pts[i - 1]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            c = not c
    return c


def _trouer_sol(s, trous):
    """Plancher d'une pièce moins les trémies : un ou plusieurs morceaux, avec leurs trous."""
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    P = Polygon(s["pts"]).buffer(0)
    T = unary_union([Polygon(t) for t in trous])
    if not P.intersects(T) or P.intersection(T).area < 1:
        return [s]
    D = P.difference(T)
    out = []
    for g in (D.geoms if hasattr(D, "geoms") else [D]):
        if g.area < 4:
            continue
        q = dict(s, pts=[[round(x, 3), round(y, 3)] for x, y in list(g.exterior.coords)[:-1]])
        if g.interiors:
            q["trous"] = [[[round(x, 3), round(y, 3)] for x, y in list(i.coords)[:-1]] for i in g.interiors]
        out.append(q)
    return out


def valider_relief(R):
    """Relief de l'extérieur (facultatif) : {"xs": [x croissants], "ys": [y croissants], "z": [[z(xs[i], ys[j]) pour i]
    pour j]}, z absolu. Retourne le relief (nombres) ou None ; erreur explicite s'il ne respecte pas ce contrat."""
    if R is None:
        return None
    def err(msg):
        raise SystemExit("scene_3d.py, exterieur, relief : " + msg)
    num = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
    if not isinstance(R, dict) or set(R) - {"xs", "ys", "z", "note"}:
        err('{"xs": [...], "ys": [...], "z": [[...], ...]} attendu')
    xs, ys, Z = R.get("xs"), R.get("ys"), R.get("z")
    for nom, a in (("xs", xs), ("ys", ys)):
        if not isinstance(a, list) or len(a) < 2 or not all(num(v) for v in a) or any(b <= a_ for a_, b in zip(a, a[1:])):
            err(f'"{nom}" : au moins 2 nombres strictement croissants')
    if not isinstance(Z, list) or len(Z) != len(ys) or not all(isinstance(r, list) and len(r) == len(xs) and all(num(v) for v in r) for r in Z):
        err(f'"z" : {len(ys)} rangées (une par y) de {len(xs)} nombres (un par x)')
    return {"xs": [float(v) for v in xs], "ys": [float(v) for v in ys], "z": [[round(float(v), 2) for v in r] for r in Z]}


def preparer_exterieur(X, M, etages, scene):
    """Extérieur (opt-in, maquette à plusieurs étages) : SCENE["exterieur"] = {"sol", "terrain", "objets", "planchers",
    "obstacles", "trous", "visites", "lumieres", "peintures"} (contrat détaillé dans le docstring d'exterieur.py de MAISON-18),
    pouces, z ABSOLU (repère du plancher de l'étage le plus bas). Clés facultatives : "palette" ([nom, description, couleur]) ;
    "relief" (terrain non plat, voir valider_relief : chaque case en deux triangles, diagonale (xs[i], ys[j]) -> (xs[i+1],
    ys[j+1]) ; une case dont le centre tombe dans un trou n'est pas dessinée ; sans relief, terrain plat à "sol") ;
    "revetements" ([{"nom", "pts", "mat"}] : asphalte, gravier, dalles... drapés sur le relief, 0,3 po au-dessus, découpés
    case par case ; on y marche comme sur le terrain).
    Prépare pour la visionneuse :
    - l'emprise de chaque étage (E["empreinte"] : dedans / dehors) et les portes extérieures (une porte dont un côté est dans
      l'emprise de son étage et l'autre dehors reçoit "dedans" et "dehors" : points de passage de part et d'autre du mur) ;
    - les trous du terrain : emprise de la maison, margelles et EXTERIEUR["trous"] réunis ;
    - les vitres minces des objets (fenêtres vues de dehors) : "forme": "vitre_ext" et "face" (côté dehors), une seule face ;
    - les arrêts de visite dehors (étage "EXT") et les peintures « ext-… » ajoutés à ceux de la scène.
    Erreur explicite si les données ne respectent pas le contrat."""
    from shapely.geometry import Point, Polygon
    from shapely.ops import unary_union

    def err(msg):
        raise SystemExit("scene_3d.py, exterieur : " + msg)
    num = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)

    def poly(p, quoi):
        if not isinstance(p, list) or len(p) < 3 or not all(isinstance(q, (list, tuple)) and len(q) >= 2 and num(q[0]) and num(q[1]) for q in p):
            err(f"{quoi} : polygone attendu ([[x, y], ...], au moins 3 points), reçu {str(p)[:80]}")
        return [[round(float(q[0]), 2), round(float(q[1]), 2)] for q in p]
    if not isinstance(X, dict):
        err('SCENE["exterieur"] doit être un dictionnaire (voir le contrat dans exterieur.py)')
    inconnues = set(X) - {"sol", "terrain", "objets", "planchers", "obstacles", "trous", "visites", "lumieres", "peintures", "palette",
                          "relief", "revetements"}
    if inconnues:
        err(f'clé(s) inconnue(s) {", ".join(sorted(inconnues))}')
    sol = X.get("sol")
    if not num(sol):
        err('"sol" (z du terrain, pouces) manquant ou non numérique')
    terrain = poly(X.get("terrain"), '"terrain"')
    planchers = []
    for i, p in enumerate(X.get("planchers") or []):
        if not isinstance(p, dict) or not num(p.get("z")):
            err(f'plancher n° {i + 1} : {{"nom", "pts", "z"}} attendu, "z" numérique')
        planchers.append({"nom": str(p.get("nom") or f"plancher {i + 1}"), "pts": poly(p.get("pts"), f'plancher « {p.get("nom")} »'), "z": float(p["z"])})
    obstacles = [{"nom": str(o.get("nom") or f"obstacle {i + 1}"), "pts": poly(o.get("pts"), f'obstacle « {o.get("nom")} »')}
                 for i, o in enumerate(X.get("obstacles") or []) if isinstance(o, dict) or err(f"obstacle n° {i + 1} : dictionnaire attendu")]
    trous = [poly(t, f"trou n° {i + 1}") for i, t in enumerate(X.get("trous") or [])]
    relief = valider_relief(X.get("relief"))
    revetements = []
    for i, r in enumerate(X.get("revetements") or []):
        if not isinstance(r, dict) or not isinstance(r.get("mat"), str):
            err(f'revêtement n° {i + 1} : {{"nom", "pts", "mat"}} attendu ("mat" : matériau du catalogue ou alias de "peintures")')
        revetements.append({"nom": str(r.get("nom") or f"revêtement {i + 1}"), "pts": poly(r.get("pts"), f'revêtement « {r.get("nom")} »'), "mat": r["mat"]})
    # emprise de chaque étage ; la maison au sol = leur réunion
    nivs = {n["id"]: n for n in M["niveaux"]}
    emp = {}
    for E in etages:
        g = empreinte(nivs[E["id"]])
        E["empreinte"] = contours(g)
        emp[E["id"]] = g
    maison = unary_union(list(emp.values()))
    # portes extérieures : un côté du mur dans l'emprise de l'étage, l'autre dehors (la porte-bibliothèque du walk-in, sous
    # l'entrée arrière, a ses deux côtés dans l'emprise du sous-sol : elle reste une porte intérieure)
    for E in etages:
        for bt in E.get("battants", []):
            x0, y0, x1, y1 = bt["zone"]
            cx, cy, enX = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) < (y1 - y0)
            d = min(x1 - x0, y1 - y0) / 2 + 12                  # 12 po au-delà de chaque face du mur
            pts = [(cx + d, cy), (cx - d, cy)] if enX else [(cx, cy + d), (cx, cy - d)]
            dans = [emp[E["id"]].contains(Point(p)) for p in pts]
            if dans[0] != dans[1]:
                k = 0 if dans[0] else 1
                bt["dedans"] = [round(v, 2) for v in pts[k]]
                bt["dehors"] = [round(v, 2) for v in pts[1 - k]]
    # objets : vitres minces des fenêtres (vues de dehors) en une seule face tournée vers l'extérieur
    bloque = [maison] + [Polygon(o["pts"]) for o in obstacles]
    objets = []
    for i, o in enumerate(X.get("objets") or []):
        if not isinstance(o, dict) or not isinstance(o.get("mat"), str):
            err(f'objet n° {i + 1} : dictionnaire avec "mat" (matériau du catalogue ou alias de "peintures") attendu')
        o = dict(o)
        if o["mat"] == "vitre" and o.get("forme", "boite") == "boite" and not o.get("pts") and all(num(o.get(k)) for k in ("x0", "x1", "y0", "y1", "z0", "z1")):
            ex, ey = o["x1"] - o["x0"], o["y1"] - o["y0"]
            if min(ex, ey) < 1.5:
                enX = ex < ey
                cx, cy = (o["x0"] + o["x1"]) / 2, (o["y0"] + o["y1"]) / 2
                ip, im = [any(g.contains(Point(p)) for g in bloque) for p in (((cx + 8, cy), (cx - 8, cy)) if enX else ((cx, cy + 8), (cx, cy - 8)))]
                if ip != im:
                    o["forme"], o["face"] = "vitre_ext", ("-" if ip else "+") + ("x" if enX else "y")
        objets.append(o)
    # terrain : troué à la maison, aux margelles (terrain_trou du sous-sol) et aux trous du contrat
    tt = [Polygon(t) for t in scene.get("terrain_trou") or []] + [Polygon(t) for t in trous]
    trous_terrain = contours(unary_union([maison] + tt).buffer(0))
    for v in X.get("visites") or []:
        if not isinstance(v, dict) or not all(num(v.get(k)) for k in ("x", "y", "cap", "z")):
            err(f'arrêt de visite « {v.get("nom") if isinstance(v, dict) else v} » : "x", "y", "cap" et "z" numériques attendus')
        scene["visites"].append(dict(v, etage="EXT"))
    lumieres = []
    for l in X.get("lumieres") or []:
        if not isinstance(l, dict) or not all(num(l.get(k)) for k in ("x", "y", "z")):
            err(f'lumière {l!r} : "x", "y", "z" numériques attendus')
        lumieres.append(l)
    # peintures « ext-… » : ajoutées à celles des étages (un nom déjà pris d'une autre couleur est préfixé)
    alias = {v[2]: str(v[0]).lower() for v in scene["peintures"].values() if len(v) > 2 and v[2]}
    for nom, v in (X.get("peintures") or {}).items():
        if not isinstance(v, (list, tuple)) or not v or not isinstance(v[0], str):
            err(f'peinture « {nom} » : [couleur, description, alias] attendu')
        if len(v) > 2 and v[2] in alias and alias[v[2]] != str(v[0]).lower():
            err(f'peinture « {nom} » : l\'alias « {v[2]} » est déjà employé par un étage avec une autre couleur')
        n2 = nom if nom not in scene["peintures"] or str(scene["peintures"][nom][0]).lower() == str(v[0]).lower() else "Extérieur · " + nom
        scene["peintures"][n2] = list(v)
    if X.get("palette"):
        scene["palettes"].append({"titre": "Extérieur", "items": X["palette"]})
    out = {"sol": float(sol), "terrain": terrain, "trous_terrain": trous_terrain, "objets": objets, "planchers": planchers,
           "obstacles": obstacles, "lumieres": lumieres}
    if relief:
        out["relief"] = relief
    if revetements:
        out["revetements"] = revetements
    return out


def fusionner(M, S, dossier):
    """Plusieurs étages (SCENE["etages"]) : chaque étage est construit dans le repère de son plancher, posé à la somme
    des hauteurs d'étage des niveaux du dessous, puis fusionné en une scène (voir le gabarit : S.etages)."""
    ordre = {"SS": 0, "RDC": 1, "ETAGE": 2, "COMBLES": 3}
    etages = sorted(S["etages"], key=lambda e: ordre.get(e.get("niveau", "SS"), 9))
    if len({e.get("niveau", "SS") for e in etages}) != len(etages):
        raise SystemExit('scene_3d.py, etages : deux scènes du même "niveau"')
    # renommer les peintures (et alias) homonymes de couleurs différentes : « Sous-sol · Blanc », « Rez-de-chaussée · Blanc »
    couleurs, alias = {}, {}
    for e in etages:
        for nom, v in (e.get("peintures") or {}).items():
            couleurs.setdefault(nom, set()).add(str(v[0]).lower())
            if len(v) > 2 and v[2]:
                alias.setdefault(v[2], set()).add(str(v[0]).lower())
    conflits = {n for n, c in couleurs.items() if len(c) > 1}
    conflits_alias = {n for n, c in alias.items() if len(c) > 1}
    out_etages, z, peintures, palettes, visites, cmds, images, ctx = [], 0.0, {}, [], [], [], {}, {}
    relief = fonction_relief(valider_relief((S.get("exterieur") or {}).get("relief")))
    for idx, Se in enumerate(etages):
        nid = Se.get("niveau", "SS")
        nom = NOMS_ETAGES.get(nid, nid)
        Se = dict(Se)
        ren = {n: f"{nom} · {n}" for n in (Se.get("peintures") or {}) if n in conflits}
        ren_al = {a: f"{a}@{nid}" for a in conflits_alias}
        if ren or ren_al:
            Se["peintures"] = {ren.get(n, n): ([v[0], v[1] if len(v) > 1 else ""] + ([ren_al.get(v[2], v[2])] if len(v) > 2 else []))
                               for n, v in Se["peintures"].items()}
            Se["peinture"] = {p: ren.get(n, n) for p, n in (Se.get("peinture") or {}).items()}
            Se["accents"] = [dict(a, peinture=ren.get(a["peinture"], a["peinture"])) for a in Se.get("accents", [])]

            def remat(o):
                m = o.get("mat")
                if isinstance(m, str):
                    if m in ren_al:
                        o = dict(o, mat=ren_al[m])
                    elif m.startswith("peinture:") and m[9:] in ren:
                        o = dict(o, mat="peinture:" + ren[m[9:]])
                return o
            Se["mobilier"] = [remat(o) for o in Se.get("mobilier", [])]
            Se["revetements"] = [remat(o) for o in Se.get("revetements", [])]
        if relief:                                     # extérieur avec relief : les margelles lisent le sol devant chaque fenêtre
            def sol_relief(x, y, dz=z):
                q = relief(x, y)
                return None if q is None else q - dz
            sol_relief.defaut = S["exterieur"].get("sol", 48) - z
            ctx = dict(ctx, sol_relief=sol_relief)
        sc = construire(M, Se, ctx)
        for k, v in sc["peintures"].items():
            peintures.setdefault(k, v)
        palettes.append({"titre": nom, "items": sc["palette"]})
        visites += [dict(v, etage=nid) for v in sc["visites"]]
        for c in Se.get("commandes") or []:
            if any(c["id"] == q["id"] for q in cmds):
                raise SystemExit(f'scene_3d.py, etages : commande "{c["id"]}" déclarée dans deux étages')
            cmds.append(c)
        for k, rel in (Se.get("images") or {}).items():
            if k in images and images[k] != rel:
                print(f"  image {k} : deux étages la déclarent avec des fichiers différents ; on garde {images[k]}")
            images.setdefault(k, rel)
        e_out = {"id": nid, "nom": nom, "z": z, "H": sc["H"], "bornes": sc["bornes"]}
        for k in ("boites", "portes", "battants", "sols", "mobilier", "revetements", "lumieres", "tremies", "trous",
                  "obstacles", "escaliers"):
            e_out[k] = sc.get(k, [])
        e_out["sol_exterieur"] = sc["sol_exterieur"]
        if sc.get("terrain_trou"):
            e_out["terrain_trou"] = sc["terrain_trou"]
        out_etages.append(e_out)
        # étage suivant : trémies et sorties de cet escalier (plancher troué, garde-corps), posé à la hauteur d'étage
        ctx = {"trous": sc["tremies"], "sorties": [es["sortie"] for es in sc.get("escaliers", [])]}
        z += Se.get("hauteur_etage", 105)
    escaliers = []
    for i, E in enumerate(out_etages):
        for es in E.pop("escaliers"):
            if i + 1 < len(out_etages):
                escaliers.append(dict(es, bas=i, haut=i + 1))
    xs = [E["bornes"][0] for E in out_etages] + [E["bornes"][2] for E in out_etages]
    ys = [E["bornes"][1] for E in out_etages] + [E["bornes"][3] for E in out_etages]
    dep = dict(S.get("depart") or etages[0].get("depart") or {"x": 400, "y": 180, "cap": 200})
    dep.setdefault("etage", etages[0].get("niveau", "SS"))
    scene = {"titre": S.get("titre") or etages[0].get("titre", ""), "projet": M["projet"]["nom"],
             "etages": out_etages, "escaliers": escaliers, "visites": visites, "depart": dep,
             "bornes": [min(xs), min(ys), max(xs), max(ys)], "palette": [], "palettes": palettes, "peintures": peintures,
             # un seul terrain : celui de l'étage le plus bas (le sous-sol est enterré jusque sous ses fenêtres)
             "sol_exterieur": out_etages[0]["sol_exterieur"] + out_etages[0]["z"]}
    if out_etages[0].get("terrain_trou"):                 # margelles du sous-sol : terrain troué au ras de la maison
        scene["terrain_trou"] = out_etages[0].pop("terrain_trou")
    for E in out_etages:
        E.pop("terrain_trou", None)
    # extérieur (opt-in) : terrain, cour, enveloppe de la maison ; on y marche (voir preparer_exterieur)
    if S.get("exterieur"):
        scene["exterieur"] = preparer_exterieur(S["exterieur"], M, out_etages, scene)
    # matériaux, modèles, commandes et images : une seule fois chacun, pour tous les étages
    tous = {"boites": [], "portes": [], "mobilier": [], "sols": [], "revetements": [], "materiaux": None}
    for E in out_etages:
        for k in ("boites", "portes", "mobilier", "sols", "revetements"):
            tous[k] += E[k]
        tous["portes"] += [q for bt in E["battants"] for q in bt["boites"]]
    if scene.get("exterieur"):
        tous["mobilier"] += scene["exterieur"]["objets"] + [{"mat": r["mat"]} for r in scene["exterieur"].get("revetements", [])]
    Sf = {"commandes": cmds, "mobilier": tous["mobilier"], "visites": visites, "images": images,
          "mat_colonne": etages[0].get("mat_colonne", "placage")}
    cmd = commandes(Sf)
    if cmd:
        scene["commandes"] = cmd
    scene["materiaux"] = bibliotheque(tous, Sf)
    tous["materiaux"] = scene["materiaux"]
    scene["modeles_glb"], scene["modeles_info"], scene["credits"] = modeles(tous)
    sc_img = {}
    completer_images(sc_img, images, dossier)
    scene["images"] = sc_img["images"]
    return scene


def completer_images(scene, images, dossier):
    scene["images"] = {}
    for cle, rel in (images or {}).items():
        f = os.path.normpath(os.path.join(dossier, rel))
        if os.path.isfile(f) and not os.environ.get("SANS_PRIVE"):
            brut = open(f, "rb").read(); octets = reduire(brut, PHOTO_MAX)
            mime = "image/png" if octets is brut and f.lower().endswith(".png") else "image/jpeg"
            scene["images"][cle] = f"data:{mime};base64," + base64.b64encode(octets).decode()
        else:
            print(f"  image {cle} omise ({rel})")


BUDGET = float(os.environ.get("BUDGET_MO", 13.6)) * 1024 * 1024        # la page publiée doit rester sous 14 Mo


def alleger(scene, html_len):
    """Page trop lourde : les images de couleur des matériaux les plus lourds sont réenregistrées (JPEG qualité 78,
    2048 px ramenés à 1024) jusqu'à passer sous le budget. Sans effet sur une page qui y est déjà."""
    if html_len <= BUDGET:
        return False
    from PIL import Image
    reste = html_len - BUDGET
    for cle in sorted(scene["materiaux"], key=lambda k: -len(scene["materiaux"][k].get("couleur", ""))):
        m = scene["materiaux"][cle]
        if "couleur" not in m:
            continue
        im = Image.open(io.BytesIO(base64.b64decode(m["couleur"].split(",", 1)[1]))).convert("RGB")
        if max(im.size) > 1024:
            im = im.resize((im.size[0] * 1024 // max(im.size), im.size[1] * 1024 // max(im.size)), Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=78, optimize=True)
        nouv = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
        if len(nouv) < len(m["couleur"]):
            reste -= len(m["couleur"]) - len(nouv); m["couleur"] = nouv
            print(f"  matériau {cle} allégé (page sous 14 Mo)")
        if reste <= 0:
            break
    return True


def main(dossier, sortie=None):
    dossier = os.path.abspath(dossier)
    M = json.load(open(os.path.join(dossier, "donnees", "maison.json"), encoding="utf-8"))
    S = charger_scene(dossier)
    if S.get("etages"):
        scene = fusionner(M, S, dossier)
    else:
        scene = construire(M, S)
        sol_ext = scene.pop("sol_exterieur")
        cmd = commandes(S)
        if cmd:
            scene["commandes"] = cmd
        scene["sol_exterieur"] = sol_ext
        scene["materiaux"] = bibliotheque(scene, S)
        scene["modeles_glb"], scene["modeles_info"], scene["credits"] = modeles(scene)
        completer_images(scene, S.get("images"), dossier)
    textures = {}
    for f in sorted(os.listdir(TEX)):
        if f.endswith(".jpg"):
            textures[f[:-4]] = "data:image/jpeg;base64," + base64.b64encode(open(os.path.join(TEX, f), "rb").read()).decode()
    gab = open(os.path.join(ICI, "visite3d_gabarit.html"), encoding="utf-8").read()

    def page():
        # scène et textures en chaînes passées à JSON.parse : analysées bien plus vite qu'un littéral JavaScript de 10 Mo
        lit = lambda o: json.dumps(json.dumps(o, ensure_ascii=False), ensure_ascii=False).replace("</", "<\\/")
        return (gab.replace('/*__SCENE__*/"null"', lit(scene))
                   .replace('/*__TEXTURES__*/"null"', lit(textures))
                   .replace("__TITRE__", scene["titre"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")))
    html = page()
    if alleger(scene, len(html.encode("utf-8"))):
        html = page()
    if len(html.encode("utf-8")) > 14 * 1024 * 1024:
        print("  ATTENTION : page de plus de 14 Mo (trop lourde pour être publiée) : moins de matériaux ou de modèles")
    out = os.path.abspath(sortie) if sortie else os.path.join(dossier, "3d", "visite.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)
    print("maquette 3D :", out, f"({len(html) // 1024} Ko)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
