"""MAISON-18 — l'extérieur : terrain, enveloppe de la maison et cour arrière (plan DAG du 17-12-2025).

Données seulement (le moteur ne marche pas encore dehors). Pouces, repère de la maison : x le long de la façade (0 à 456 au
nu extérieur), y vers l'arrière (façade 0, mur arrière 380), z vers le haut DEPUIS LE PLANCHER DU SOUS-SOL (le RDC est à 105).

Sources
- Plan « PLAN D'AMÉNAGEMENT — COUR ARRIÈRE », Design Action Gestion (DAG), 17-12-2025, 3/16" = 1'-0" (PNG 2550 × 1650 px à 150 ppp :
  2,34 px par pouce, mesuré sur la largeur de la maison, 38'-0" = 1067 px). Le dessin est tourné de 180° par
  rapport aux plans du dépôt : x_maison = 456 - (x_px - 625) / 2,34 ; y_maison = 380 + (y_px - 171) / 2,34 (171 = nu du mur
  arrière, 625 = coin arrière droit, x = 456). Contrôles : l'entrée arrière tombe à x 219-327 (relevé : 219-327), le palier fait
  129 × 60 (« ±10'-9" × 4'-11" »), la piscine est à 6'-2⅝" du cabanon, 9'-10⅜" de la ligne de lot oblique et 3'-4¼" de la ligne
  arrière (écarts < 1 po), les lignes de lot recoupent le plan d'implantation de 1957 (P7) à 4 po près.
- Vidéo DAG « C-1329 Aménagement extérieur » (vignettes) : cabanon blanc en planches verticales, toit à deux versants, portes
  doubles noires de grange avec impostes vitrées ; pas japonais de dalles blanches ; deck à garde-corps d'aluminium noir sur une
  jupe blanche en déclin horizontal ; piscine hors-terre grise ; maison de brique rouge, toit en croupe gris foncé, fascias
  blancs, fenêtres noires, cheminée, fondation blanche apparente, allée sur le côté.
- donnees/maison.json (murs extérieurs, ouvertures, cheminée, perron, entrée arrière), lu à l'import : les fenêtres et portes
  suivent les changements des autres modules (repli : les valeurs du relevé si le fichier manque).

CONTRAT (pour le moteur, qui l'ajoutera ensuite) — EXTERIEUR = {
  "sol": 48,                 terrain naturel (z, repère du plancher du sous-sol) : le plan de gazon actuel du moteur ;
  "terrain": [[x, y], ...],  lignes de lot (polygone, sens horaire vu de dessus) : ce qu'on montre comme terrain ;
  "objets": [...],           objets du mobilier (formes du moteur : boite, arrondi, cylindre, tube, sphere, tore ; "pts" =
                             prisme vertical) en z ABSOLU ; matériaux du catalogue ou alias de EXTERIEUR["peintures"] ;
  "planchers": [{"nom", "pts", "z"}],   surfaces où l'on marche au-dessus du terrain (palier, marches, patio, deck, dalles…) ;
                             z = dessus ; une marche = un plancher ; la descente de la porte de côté est SOUS le terrain (z < 48) ;
  "obstacles": [{"nom", "pts"}],        emprises où l'on ne passe pas (piscine, cabanon, muret, garde-corps, haies, troncs…) ;
  "trous": [[[x, y], ...]],  où couper le plan du terrain (descente extérieure de la porte de côté du sous-sol) ;
  "visites": [{"nom", "x", "y", "cap", "z"}],  arrêts dehors (z = dessus du sol sous les pieds) ;
  "lumieres": [{"x", "y", "z", "i"}],   appliques et lanterne (même format que les lumières d'étage, z absolu) ;
  "peintures": {nom: [couleur, description, alias]}  couleurs des alias employés par les objets ("ext-blanc"…) }.
Aperçu dans le moteur actuel : EXT_APERCU=1 (voir scene_3d.py) pose ces objets dans le mobilier du sous-sol.
"""
import json
import math
import os

ICI = os.path.dirname(os.path.abspath(__file__))

SOL = 48.0                 # terrain : 8 po sous l'allège des fenêtres du sous-sol (valeur du moteur)
Z_RDC = 105.0              # plancher du RDC (hauteur d'étage du sous-sol)
Z_TERRASSE = 97.5          # palier, patio et deck : une marche de 7½ po sous le seuil de la porte arrière (49½ po du sol)
Z_PERRON = 98.0            # dessus du perron avant (une marche sous le seuil)
SOFFITE = 202.0            # dessous des soffites (plafond du RDC à 201)
PENTE = 5 / 12             # toit en croupe : fermes 5/12 (croquis P1 2016), « faible pente »
DEBORD = 16                # débord de toit (soffite)

PEINTURES = {   # nom : [couleur à l'écran, description, alias employé par les objets]
    "Blanc extérieur": ["#F1F0EB", "fascias, soffites, jupe du deck en déclin, cabanon (planches verticales)", "ext-blanc"],
    "Bardeau gris foncé": ["#3F4245", "toit en croupe et toit du cabanon (bardeau d'asphalte)", "ext-bardeau"],
    "Asphalte": ["#45474A", "allée", "ext-asphalte"],
    "Gazon": ["#6E8A4E", "pelouse", "ext-gazon"],
    "Toile de piscine": ["#3E8DB5", "fond de la piscine (toile bleue)", "ext-toile"],
    "Gris piscine": ["#9A9EA2", "paroi de la piscine hors-terre", "ext-piscine"],
    "Gris foncé": ["#5C5F63", "montants de la piscine, appareils", "ext-gris"],
    "Dalle blanche": ["#E6E3DC", "pas japonais (interblocs blancs)", "ext-dalle"],
    "Épinette": ["#3E5A3F", "épinettes et haie de cèdres", "ext-sapin"],
    "Écorce de bouleau": ["#E9E6DE", "troncs de bouleaux", "ext-bouleau"],
}


# ------------------------------------------------------------------------------------------------- formes du moteur
def B(x0, y0, x1, y1, z0, z1, mat):
    return {"forme": "boite", "x0": min(x0, x1), "y0": min(y0, y1), "x1": max(x0, x1), "y1": max(y0, y1),
            "z0": z0, "z1": z1, "mat": mat}


def P(pts, z0, z1, mat):                     # prisme vertical (polygone en plan)
    return {"forme": "boite", "pts": [[round(x, 2), round(y, 2)] for x, y in pts], "z0": z0, "z1": z1, "mat": mat}


def C(x, y, r, z0, z1, mat, **k):
    return dict({"forme": "cylindre", "x": x, "y": y, "r": r, "z0": z0, "z1": z1, "mat": mat}, **k)


def T(pts, r, mat, **k):
    return dict({"forme": "tube", "pts": [list(p) for p in pts], "r": r, "mat": mat}, **k)


def SPH(x, y, z, r, mat, **k):
    return dict({"forme": "sphere", "x": x, "y": y, "z": z, "r": r, "mat": mat}, **k)


def TOR(x, y, z, R, r, mat, **k):
    return dict({"forme": "tore", "x": x, "y": y, "z": z, "R": R, "r": r, "mat": mat}, **k)


def rect(x0, y0, x1, y1):
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]


def cercle(cx, cy, r, n=48):
    return [[cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)] for i in range(n)]


# ------------------------------------------------------------------------------------------------- relevé (maison.json)
MURS_REPLI = {   # niveau : [(id, type, x1, y1, x2, y2, épaisseur)] — relevé R0 (si donnees/maison.json manque)
    "SS": [("mur-SS-001", "fondation", 5, 5, 451, 5, 10), ("mur-SS-002", "fondation", 451, 5, 451, 375, 10),
           ("mur-SS-003", "fondation", 451, 375, 5, 375, 10), ("mur-SS-004", "fondation", 5, 375, 5, 5, 10),
           ("mur-SS-005", "fondation", 224, 375, 224, 435, 10), ("mur-SS-006", "fondation", 224, 435, 322, 435, 10),
           ("mur-SS-007", "fondation", 322, 435, 322, 375, 10), ("mur-SS-008", "fondation", 165, 5, 165, -45, 6),
           ("mur-SS-009", "fondation", 165, -45, 231, -45, 6), ("mur-SS-010", "fondation", 231, -45, 231, 5, 6)],
    "RDC": [("mur-RDC-001", "ext", 5, 5, 451, 5, 10), ("mur-RDC-002", "ext", 451, 5, 451, 375, 10),
            ("mur-RDC-003", "ext", 5, 375, 451, 375, 10), ("mur-RDC-004", "ext", 5, 5, 5, 375, 10),
            ("mur-RDC-005", "ext", 224, 375, 224, 435, 10), ("mur-RDC-006", "ext", 224, 435, 322, 435, 10),
            ("mur-RDC-007", "ext", 322, 435, 322, 375, 10)],
}
OUV_REPLI = {    # niveau : [(mur, type, position depuis le 1er point, largeur)]
    "SS": [("mur-SS-001", "fenetre", 377, 75), ("mur-SS-002", "fenetre", 303, 80), ("mur-SS-002", "fenetre", 70, 36),
           ("mur-SS-002", "porte", 175, 36), ("mur-SS-004", "fenetre", 195, 36), ("mur-SS-004", "fenetre", 327, 36),
           ("mur-SS-003", "porte", 190, 30), ("mur-SS-003", "fenetre", 275, 40), ("mur-SS-003", "fenetre", 339, 40)],
    "RDC": [("mur-RDC-001", "fenetre", 93, 75), ("mur-RDC-001", "fenetre", 372, 108), ("mur-RDC-003", "fenetre", 93, 75),
            ("mur-RDC-003", "fenetre", 192, 36), ("mur-RDC-003", "fenetre", 370, 75), ("mur-RDC-004", "fenetre", 186, 36),
            ("mur-RDC-002", "fenetre", 175, 36), ("mur-RDC-006", "fenetre", 69, 42), ("mur-RDC-001", "porte", 194, 34),
            ("mur-RDC-003", "porte", 290, 32), ("mur-RDC-007", "porte", 26, 34)],
}


def releve():
    """{niveau: (murs extérieurs, ouvertures)} depuis donnees/maison.json (construit avant la maquette), sinon le repli."""
    f = os.path.join(ICI, "donnees", "maison.json")
    out = {}
    try:
        M = json.load(open(f, encoding="utf-8"))
        for n in M["niveaux"]:
            if n["id"] not in ("SS", "RDC"):
                continue
            murs = [(m["id"], m["type"], m["x1"], m["y1"], m["x2"], m["y2"], (m.get("epaisseur") or {}).get("valeur") or 10)
                    for m in n["murs"] if m["type"] in ("fondation", "ext") and m.get("materiau") not in ("verre", "lattes")]
            ids = {m[0] for m in murs}
            ouvs = [(o["mur_id"], o["type"], (o.get("position") or {}).get("valeur"), (o.get("largeur") or {}).get("valeur"))
                    for o in n["ouvertures"] if o["mur_id"] in ids]
            out[n["id"]] = (murs, [o for o in ouvs if o[2] is not None and o[3] is not None])
    except (OSError, ValueError, KeyError):
        pass
    for nid in ("SS", "RDC"):
        out.setdefault(nid, (MURS_REPLI[nid], OUV_REPLI[nid]))
    return out


# emprises (nu extérieur) : corps de la maison, entrée arrière (caveau dessous), excroissance sous le perron
CORPS, ENTREE_ARR, PERRON = (0, 0, 456, 380), (219, 380, 327, 440), (162, -48, 234, 0)
CHEMINEE = (-20.3, 132.0, 0.0, 153.6)      # massif de maçonnerie hors du mur gauche (elem-SS-CHEM / elem-RDC-CHEM)


def _dans(x, y, rects):
    return any(a <= x <= c and b <= y <= d for a, b, c, d in rects)


# ------------------------------------------------------------------------------------------------- enveloppe de la maison
def enveloppe():
    """Parement de brique sur le RDC, crépi blanc sur la fondation apparente, fenêtres noires vues de dehors, cadres de portes."""
    out = []
    R = releve()
    niveaux = {"SS": dict(emprise=[CORPS, ENTREE_ARR, PERRON], z0=SOL - 4, z1=97.0, mat="crepi",
                          fen=(56, 86), porte=(0, 80)),
               "RDC": dict(emprise=[CORPS, ENTREE_ARR], z0=97.0, z1=SOFFITE + 0.5, mat="brique_rouge",
                           fen=(Z_RDC + 34, Z_RDC + 82), porte=(Z_RDC, Z_RDC + 80))}
    for nid, cfg in niveaux.items():
        murs, ouvs = R[nid]
        for (mid, typ, x1, y1, x2, y2, t) in murs:
            L = math.hypot(x2 - x1, y2 - y1)
            if L < 1:
                continue
            ux, uy = (x2 - x1) / L, (y2 - y1) / L
            nx, ny = -uy, ux
            # normale vers l'extérieur : le côté où le plus de points (le long du mur) tombent hors de l'emprise
            cote = sum((0 if _dans(x1 + ux * L * s + nx * (t / 2 + 1), y1 + uy * L * s + ny * (t / 2 + 1), cfg["emprise"]) else 1)
                       - (0 if _dans(x1 + ux * L * s - nx * (t / 2 + 1), y1 + uy * L * s - ny * (t / 2 + 1), cfg["emprise"]) else 1)
                       for s in (0.1, 0.3, 0.5, 0.7, 0.9))
            if cote < 0:
                nx, ny = -nx, -ny
            f = t / 2                                      # nu extérieur, depuis l'axe

            def pt(a, d):
                return x1 + ux * a + nx * d, y1 + uy * a + ny * d

            def bx(a0, a1, d0, d1, z0, z1, mat):
                (xa, ya), (xb, yb) = pt(a0, d0), pt(a1, d1)
                return B(xa, ya, xb, yb, z0, z1, mat)
            # parties du nu extérieur qui donnent dehors (pas contre l'entrée arrière ni dans le perron)
            pas = 1.0
            libres, a, debut = [], -f - 0.5, None
            while a <= L + f + 0.5 + 1e-6:
                x, y = pt(a, f + 0.8)
                dehors = not _dans(x, y, cfg["emprise"])
                if dehors and debut is None:
                    debut = a
                if (not dehors or a + pas > L + f + 0.5) and debut is not None:
                    libres.append((debut, a if not dehors else L + f + 0.5))
                    debut = None
                a += pas
            trous = []
            for (mur, typ_o, c, w) in ouvs:
                if mur != mid:
                    continue
                z0o, z1o = cfg["fen"] if typ_o == "fenetre" else cfg["porte"]
                trous.append((c - w / 2, c + w / 2, z0o, z1o, typ_o))
            trous.sort()
            for (a0, a1) in libres:
                coupe = [tr for tr in trous if tr[1] > a0 and tr[0] < a1]
                pos = a0
                for (o0, o1, z0o, z1o, _) in coupe:
                    if o0 > pos:
                        out.append(bx(pos, o0, f - 0.5, f + 0.5, cfg["z0"], cfg["z1"], cfg["mat"]))
                    if z0o > cfg["z0"]:
                        out.append(bx(max(o0, a0), min(o1, a1), f - 0.5, f + 0.5, cfg["z0"], z0o, cfg["mat"]))
                    if z1o < cfg["z1"]:
                        out.append(bx(max(o0, a0), min(o1, a1), f - 0.5, f + 0.5, z1o, cfg["z1"], cfg["mat"]))
                    pos = max(pos, o1)
                if pos < a1:
                    out.append(bx(pos, a1, f - 0.5, f + 0.5, cfg["z0"], cfg["z1"], cfg["mat"]))
                # fenêtres (cadre noir, vitre, allège) et cadres de portes, vus de dehors
                for (o0, o1, z0o, z1o, typ_o) in coupe:
                    if typ_o == "fenetre":
                        k = 2.5
                        out += [bx(o0, o0 + k, f - 3, f + 0.2, z0o, z1o, "metal"), bx(o1 - k, o1, f - 3, f + 0.2, z0o, z1o, "metal"),
                                bx(o0, o1, f - 3, f + 0.2, z1o - k, z1o, "metal"), bx(o0, o1, f - 3, f + 0.2, z0o, z0o + k, "metal"),
                                bx(o0 + k, o1 - k, f - 2, f - 1.6, z0o + k, z1o - k, "vitre"),
                                bx(o0 - 1.5, o1 + 1.5, f - 0.5, f + 2.0, z0o - 2.5, z0o, "beton" if nid == "RDC" else "metal")]
                        n_mont = 2 if o1 - o0 > 90 else (1 if o1 - o0 > 50 else 0)
                        for j in range(n_mont):
                            am = o0 + (o1 - o0) * (j + 1) / (n_mont + 1)
                            out.append(bx(am - 1, am + 1, f - 2.6, f - 0.5, z0o + k, z1o - k, "metal"))
                    else:
                        zb = max(z0o, cfg["z0"])
                        if z1o <= zb:
                            continue
                        out += [bx(o0 - 3, o0, f + 0.4, f + 1.4, zb, z1o + 3, "metal"),
                                bx(o1, o1 + 3, f + 0.4, f + 1.4, zb, z1o + 3, "metal"),
                                bx(o0, o1, f + 0.4, f + 1.4, z1o, z1o + 3, "metal")]
    # cheminée de brique hors du mur gauche, du sol au-dessus du toit, couronnement de béton, conduit
    x0, y0, x1, y1 = CHEMINEE
    out += [B(x0, y0, x1 - 0.2, y1, SOL - 4, 290, "brique_rouge"), B(x0 - 1, y0 - 1, x1 + 0.8, y1 + 1, 290, 293, "beton"),
            C((x0 + x1) / 2, (y0 + y1) / 2, 4, 293, 299, "gris")]
    return out


def toit():
    """Toit en croupe 5/12 en rangs de bardeaux (gradins de 2 po : le moteur n'a que des formes verticales), débord de 16 po,
    fascias et soffites blancs ; petite croupe sur l'entrée arrière ; ventilateur de toit."""
    out = []
    h = 2.0
    d = h / PENTE                                  # 4,8 po de recul par rang
    x0, y0, x1, y1 = CORPS[0] - DEBORD, CORPS[1] - DEBORD, CORPS[2] + DEBORD, CORPS[3] + DEBORD
    ze = SOFFITE + 6                               # bord du toit (au-dessus du fascia)
    k = 0
    while (y1 - y0) - 2 * k * d > 0.5:
        out.append(B(x0 + k * d, y0 + k * d, x1 - k * d, y1 - k * d, ze + k * h, ze + (k + 1) * h, "ext-bardeau"))
        k += 1
    faite = ze + k * h
    out.append(B(x0 + (k - 1) * d - 1, y0 + (k - 1) * d - 1, x1 - (k - 1) * d + 1, y1 - (k - 1) * d + 1, faite - 0.5, faite + 1, "ext-bardeau"))
    # croupe de l'entrée arrière (x 219-327) qui rejoint le versant arrière
    ex0, ex1, ey1 = ENTREE_ARR[0] - DEBORD, ENTREE_ARR[2] + DEBORD, ENTREE_ARR[3] + DEBORD
    k = 0
    while (ex1 - ex0) - 2 * k * d > 0.5:
        out.append(B(ex0 + k * d, y1 - k * d - 2, ex1 - k * d, ey1 - k * d, ze + k * h, ze + (k + 1) * h, "ext-bardeau"))
        k += 1
    # fascias (8 po) et soffites blancs
    F = "ext-blanc"
    out += [B(x0, y0 - 1, x1, y0, SOFFITE, ze + h, F), B(x0 - 1, y0 - 1, x0, y1 + 1, SOFFITE, ze + h, F),
            B(x1, y0 - 1, x1 + 1, y1 + 1, SOFFITE, ze + h, F),
            B(x0, y1, ex0, y1 + 1, SOFFITE, ze + h, F), B(ex1, y1, x1, y1 + 1, SOFFITE, ze + h, F),
            B(ex0 - 1, y1, ex0, ey1 + 1, SOFFITE, ze + h, F), B(ex1, y1, ex1 + 1, ey1 + 1, SOFFITE, ze + h, F),
            B(ex0, ey1, ex1, ey1 + 1, SOFFITE, ze + h, F)]
    out += [B(x0, y0, x1, 0, SOFFITE, SOFFITE + 1, F), B(x0, 0, 0, 380, SOFFITE, SOFFITE + 1, F), B(456, 0, x1, 380, SOFFITE, SOFFITE + 1, F),
            B(x0, 380, ENTREE_ARR[0], y1, SOFFITE, SOFFITE + 1, F), B(ENTREE_ARR[2], 380, x1, y1, SOFFITE, SOFFITE + 1, F),
            B(ex0, y1, ENTREE_ARR[0], ey1, SOFFITE, SOFFITE + 1, F), B(ENTREE_ARR[2], y1, ex1, ey1, SOFFITE, SOFFITE + 1, F),
            B(ENTREE_ARR[0], 440, ENTREE_ARR[2], ey1, SOFFITE, SOFFITE + 1, F)]
    out.append(B(300, 250, 312, 262, ze + (396 - 262) * PENTE - 2, ze + (396 - 262) * PENTE + 8, "ext-gris"))   # ventilateur
    return out


def perron_avant():
    """Perron de béton devant la porte avant (sur l'excroissance du sous-sol), 6 marches vers la rue, garde-corps noirs."""
    out = [B(161, -49, 235, 0, 92, Z_PERRON, "beton")]
    r = (Z_PERRON - SOL) / 7
    for i in range(1, 7):
        out.append(B(162, -48 - 11 * i, 234, -48, SOL - 4, Z_PERRON - r * i, "beton"))
    for x in (163.5, 232.5):
        out += garde_corps_pente((x, 0), (x, -48), Z_PERRON, Z_PERRON, 36)
        out += garde_corps_pente((x, -48), (x, -114), Z_PERRON - r, SOL + r, 36)
    out.append(B(168, -150, 462, -114, SOL - 0.5, SOL + 0.75, "beton"))         # trottoir vers l'allée
    return out


# ------------------------------------------------------------------------------------------------- garde-corps d'aluminium
def garde_corps(a, b, z, h, genre="barreaux", porte=None):
    """Garde-corps d'aluminium noir horizontal de a à b (segment parallèle à x ou à y), plancher à z, hauteur h :
    poteaux (≤ 60 po), main courante, lisse basse ; barreaux (4¾ po) ou verre clair. porte = (début, fin) le long du segment."""
    (xa, ya), (xb, yb) = a, b
    L = math.hypot(xb - xa, yb - ya)
    ux, uy = (xb - xa) / L, (yb - ya) / L
    q = lambda s: (xa + ux * s, ya + uy * s)
    out = []

    def bar(s0, s1, e, z0, z1, mat="metal"):
        (p, r), (pp, rr) = q(s0), q(s1)
        if abs(ux) > 0.5:
            return B(p, r - e / 2, pp, rr + e / 2, z0, z1, mat)
        return B(p - e / 2, r, pp + e / 2, rr, z0, z1, mat)
    n = max(1, math.ceil(L / 60))
    poteaux = [L * i / n for i in range(n + 1)]
    if porte:
        poteaux = sorted(set(poteaux + [porte[0], porte[1]]))
        poteaux = [s for s in poteaux if not (porte[0] + 1 < s < porte[1] - 1)]
    for s in poteaux:
        s = min(max(s, 1.25), L - 1.25)
        out.append(bar(s - 1.25, s + 1.25, 2.5, z, z + h))
    for s0, s1 in zip(poteaux, poteaux[1:]):
        if porte and s0 >= porte[0] - 1 and s1 <= porte[1] + 1:      # portillon à fermeture automatique
            out += [bar(s0 + 2, s1 - 2, 1.6, z + 2, z + 3.5), bar(s0 + 2, s1 - 2, 1.6, z + h - 4, z + h - 2.5),
                    bar(s0 + 2, s0 + 3.5, 1.6, z + 2, z + h - 2.5), bar(s1 - 3.5, s1 - 2, 1.6, z + 2, z + h - 2.5)]
            out.append(bar(s0 + 3.5, s1 - 3.5, 0.5, z + 3.5, z + h - 4, "verre-clair" if genre == "verre" else "metal"))
            out.append(bar(s1 - 6, s1 - 2.5, 3, z + h - 9, z + h - 5))                             # ferme-porte
            continue
        out += [bar(s0, s1, 2.5, z + h - 1.75, z + h), bar(s0, s1, 1.5, z + 2.5, z + 4)]
        if genre == "verre":
            out.append(bar(s0 + 2, s1 - 2, 0.5, z + 4.5, z + h - 2.5, "verre-clair"))
        else:
            m = max(1, round((s1 - s0) / 4.75))
            for j in range(1, m):
                s = s0 + (s1 - s0) * j / m
                out.append(bar(s - 0.375, s + 0.375, 0.75, z + 4, z + h - 1.75))
    return out


def garde_corps_pente(a, b, za, zb, h):
    """Garde-corps d'escalier (barreaux) de a (haut, plancher za) à b (bas, nez de marche zb) : poteaux, main courante en pente."""
    (xa, ya), (xb, yb) = a, b
    L = math.hypot(xb - xa, yb - ya)
    out = [B(xa - 1.25, ya - 1.25, xa + 1.25, ya + 1.25, za, za + h + 2, "metal"),
           B(xb - 1.25, yb - 1.25, xb + 1.25, yb + 1.25, SOL if zb < SOL + 10 else zb, zb + h + 2, "metal"),
           T([(xa, ya, za + h), (xb, yb, zb + h)], 1.1, "metal", pans=8), T([(xa, ya, za + 3.5), (xb, yb, zb + 3.5)], 0.7, "metal", pans=8)]
    m = max(1, round(L / 4.75))
    for j in range(1, m):
        t = j / m
        x, y, zz = xa + (xb - xa) * t, ya + (yb - ya) * t, za + (zb - za) * t
        out.append(B(x - 0.375, y - 0.375, x + 0.375, y + 0.375, zz + 3.5, zz + h, "metal"))
    return out


def jupe(x0, y0, x1, y1, z0, z1):
    """Jupe blanche en déclin horizontal (planches de 6 po, ombre de 0,4 po) sur une face mince (x0 = x1 ou y0 = y1 ± épaisseur)."""
    out, z, i = [], z0, 0
    while z < z1 - 0.1:
        e = 0.4 if i % 2 else 0.0
        zz = min(z + 6, z1)
        if x1 - x0 < y1 - y0:
            out.append(B(x0 - e / 2, y0, x1 + e / 2, y1, z, zz, "ext-blanc"))
        else:
            out.append(B(x0, y0 - e / 2, x1, y1 + e / 2, z, zz, "ext-blanc"))
        z, i = zz, i + 1
    return out


# ------------------------------------------------------------------------------------------------- cour arrière (plan DAG)
PALIER = (327, 380, 456, 440)              # ±10'-9" × 4'-11", contre le mur arrière, à côté de l'entrée arrière
ESC = (386, 440, 456, 494)                 # escalier de 5'-9½" de large, 6 girons de 9 po, 7 contremarches de 7,07 po
PATIO = (159, 440, 386, 560)               # ±19' × 10'
DECK = (159, 560, 314, 701)                # ±13' × 11'-9", entaillé par la piscine
PISC = (190.6, 724.3, 126.0)               # piscine hors-terre de 21' de diamètre (centre, rayon)
GRAVIER_R = 140.0                          # anneau de gravier
CAB = (391, 681, 511, 825)                 # cabanon 10' × 12' (murs) ; débord de toit 12 po ; à 3'-0" des lignes de lot
CAB_TOIT = (379, 669, 523, 837)
ROCHE = [(457, 380, 505, 560), (386, 494, 445, 560)]       # bande de roche de 4'-0" et pied de l'escalier
MURET = (445, 494, 457, 560)               # muret de soutènement (hachuré au plan)
DALLES = [[(486.5, 598.4), (495.4, 575.5), (461.2, 562.2), (452.3, 585.2)],      # pas japonais (interblocs) 36 × 24 po
          [(473.6, 632.1), (482.5, 609.1), (448.3, 595.9), (439.4, 618.8)],
          [(433.4, 665.9), (469.7, 665.9), (469.7, 641.5), (433.4, 641.5)]]
APPAREILS = [(33.8, 780.0), (0.4, 790.7), (25.2, 857.4), (59.4, 847.5)]          # dalle des appareils de la piscine (3' × 6')
ALLEE = (462, -480, 556, 60)               # allée d'asphalte le long du côté droit (hors plan DAG : supposée)
DESCENTE = (456, 94, 504, 212)             # descente de la porte de côté du sous-sol (hors plan : supposée)
# lignes de lot : arrière et côtés mesurés sur le plan DAG ; devant prolongé avec le plan d'implantation de 1957 (marge avant
# de 40', ligne droite ⟂ à la rue, façade du lot 57,23')
TERRAIN = [[560, -480], [560, 871], [-43, 903], [-128, -480]]


def _ligne_gauche(y):                       # ligne de lot oblique (côté x bas), mesurée sur le plan DAG
    return -75.5 + (32.1 / 523.3) * (y - 380)


def _deck_pts():
    from shapely.geometry import Point, Polygon
    g = Polygon(rect(*DECK)).difference(Point(PISC[0], PISC[1]).buffer(PISC[2] + 1, 24))
    if g.geom_type != "Polygon":
        g = max(g.geoms, key=lambda q: q.area)
    return [list(p) for p in list(g.exterior.coords)[:-1]]


def cour():
    out, Z = [], Z_TERRASSE
    r_esc = (Z - SOL) / 7
    # palier, patio, deck : platelage composite beige (érable comme teinte), jupe blanche en déclin
    deck_pts = _deck_pts()
    out += [B(*PALIER, Z - 1.5, Z, "erable"), B(*PATIO, Z - 1.5, Z, "erable"), P(deck_pts, Z - 1.5, Z, "erable")]
    out += jupe(455.5, 380, 456, 440, SOL, Z - 1.5)                        # palier, côté droit
    out += jupe(159, 440, 159.5, 560, SOL, Z - 1.5) + jupe(159, 440, 219, 440.5, SOL, Z - 1.5)
    out += jupe(314, 559.5, 386, 560, SOL, Z - 1.5) + jupe(385.5, 494, 386, 560, SOL, Z - 1.5)
    yd = PISC[1] - math.sqrt(PISC[2] ** 2 - (PISC[0] - 314) ** 2)
    yg = PISC[1] - math.sqrt(PISC[2] ** 2 - (PISC[0] - 159) ** 2)
    out += jupe(313.5, 560, 314, yd, SOL, Z - 1.5) + jupe(159, 560, 159.5, yg, SOL, Z - 1.5)
    # escalier vers la cour : girons de composite, contremarches et limon blancs
    for i in range(1, 7):
        y = ESC[1] + 9 * (i - 1)
        zt = Z - r_esc * i
        out += [B(ESC[0], y, ESC[2], ESC[3], SOL, zt - 1.25, "ext-blanc"), B(ESC[0], y - 0.75, ESC[2], y + 9, zt - 1.25, zt, "erable")]
    # garde-corps (couleurs du plan DAG) : vert = barreaux 36 po, rouge = barreaux 48 po, bleu = verre pur 48 po
    out += garde_corps((454.75, 380), (454.75, 440), Z, 36)                                        # vert, palier
    out += garde_corps_pente((454.75, 440), (454.75, 494), Z - r_esc, SOL + r_esc, 36)            # vert, escalier
    out += garde_corps((386, 440), (386, 560), Z, 36)                                              # vert, patio / escalier
    out += garde_corps((386, 558.75), (314, 558.75), Z, 36)                                        # vert
    out += garde_corps((219, 441.25), (159, 441.25), Z, 36)                                        # vert, devant le mur
    out += garde_corps((160.25, 440), (160.25, 560), Z, 36)                                        # vert
    out += garde_corps((314, 560), (159, 560), Z, 48, "verre", porte=(4, 40))                     # bleu + portillon
    out += garde_corps((312.75, 560), (312.75, yd - 1), Z, 48)                                    # rouge
    out += garde_corps((160.25, 560), (160.25, yg - 1), Z, 48)                                    # rouge
    # piscine hors-terre 21' : gravier, paroi grise, montants, toile, eau, margelle
    cx, cy, R = PISC
    out += [C(cx, cy, GRAVIER_R, SOL - 0.5, SOL + 0.8, "terrazzo", pans=64),
            C(cx, cy, R, SOL, 98.5, "ext-piscine", pans=72), C(cx, cy, R - 2.5, 98.5, 98.7, "ext-toile", pans=72),
            C(cx, cy, R - 2.5, 98.7, 99.2, "eau", pans=72), TOR(cx, cy, 100.5, R - 1, 2.6, "ext-piscine", axe="z")]
    for j in range(24):
        a = 2 * math.pi * j / 24
        x, y = cx + (R + 0.6) * math.cos(a), cy + (R + 0.6) * math.sin(a)
        out.append(B(x - 2.2, y - 2.2, x + 2.2, y + 2.2, SOL, 99, "ext-gris"))
    # appareils de la piscine : dalle, filtre au sable, pompe, thermopompe
    out.append(P(APPAREILS, SOL - 0.5, SOL + 4, "beton"))
    out += [B(12.5, 791, 36.5, 815, SOL + 4, SOL + 34, "ext-gris"), B(13.5, 790.5, 35.5, 791, SOL + 8, SOL + 30, "metal"),
            C(33.2, 828.3, 8, SOL + 4, SOL + 34, "ext-gris"), C(33.2, 828.3, 3.5, SOL + 34, SOL + 39, "metal"),
            B(33.7, 837.3, 43.7, 849.3, SOL + 4, SOL + 15, "metal")]
    # roche, muret de soutènement, pas japonais
    out += [B(*r, SOL - 0.5, SOL + 0.9, "terrazzo") for r in ROCHE]
    out += [B(*MURET, SOL - 2, SOL + 18, "beton"), B(MURET[0] - 0.75, MURET[1] - 0.75, MURET[2] + 0.75, MURET[3] + 0.75, SOL + 18, SOL + 20, "beton")]
    out += [P(d, SOL - 0.5, SOL + 1.5, "ext-dalle") for d in DALLES]
    out += cabanon()
    out += mobilier_patio()
    return out


def cabanon():
    """Cabanon 10' × 12' : dalle, planches verticales blanches (couvre-joints), toit à deux versants 6/12 (faîte selon y,
    pignon et portes vers la maison), débord 12 po, portes doubles noires de grange à impostes vitrées."""
    x0, y0, x1, y1 = CAB
    out = [B(x0 - 4, y0 - 4, x1 + 4, y1 + 4, SOL - 1, SOL + 4, "beton")]
    zs, zm = SOL + 4, SOL + 4 + 96                  # dalle, haut des murs
    out.append(B(x0, y0, x1, y1, zs, zm + 1, "ext-blanc"))
    xm = (x0 + x1) / 2
    porte = (xm - 32, xm + 32)
    for x in range(x0 + 6, x1, 12):                 # couvre-joints des planches verticales
        out += [B(x - 0.75, y1, x + 0.75, y1 + 0.6, zs, zm, "ext-blanc")]
        if not (porte[0] - 4 < x < porte[1] + 4):
            out.append(B(x - 0.75, y0 - 0.6, x + 0.75, y0, zs, zm, "ext-blanc"))
    for y in range(y0 + 6, y1, 12):
        out += [B(x0 - 0.6, y - 0.75, x0, y + 0.75, zs, zm, "ext-blanc"), B(x1, y - 0.75, x1 + 0.6, y + 0.75, zs, zm, "ext-blanc")]
    tx0, ty0, tx1, ty1 = CAB_TOIT
    h, d = 1.5, 3.0                                 # 6/12
    n = int(((tx1 - tx0) / 2) // d)
    ze = zm - 12 * 0.5                              # bord du toit (12 po de débord à 6/12)
    for k in range(n):
        out += [B(tx0 + k * d, ty0, tx0 + k * d + d + 1, ty1, ze + k * h, ze + k * h + 2, "ext-bardeau"),
                B(tx1 - k * d - d - 1, ty0, tx1 - k * d, ty1, ze + k * h, ze + k * h + 2, "ext-bardeau"),
                B(tx0 + k * d, ty0 - 1.2, tx0 + k * d + d + 1, ty0, ze + k * h - 1.5, ze + k * h + 2, "ext-blanc"),
                B(tx1 - k * d - d - 1, ty0 - 1.2, tx1 - k * d, ty0, ze + k * h - 1.5, ze + k * h + 2, "ext-blanc"),
                B(tx0 + k * d, ty1, tx0 + k * d + d + 1, ty1 + 1.2, ze + k * h - 1.5, ze + k * h + 2, "ext-blanc"),
                B(tx1 - k * d - d - 1, ty1, tx1 - k * d, ty1 + 1.2, ze + k * h - 1.5, ze + k * h + 2, "ext-blanc")]
    zf = ze + n * h
    out.append(B(xm - 4, ty0 - 1.2, xm + 4, ty1 + 1.2, zf - 1, zf + 1.5, "ext-bardeau"))
    out += [B(tx0 - 1, ty0, tx0, ty1, ze - 6, ze + 1, "ext-blanc"), B(tx1, ty0, tx1 + 1, ty1, ze - 6, ze + 1, "ext-blanc")]
    for j in range(int((x1 - x0) / 2 // d)):        # pignons blancs sous les versants
        out.append(B(x0 + j * d, y0, x1 - j * d, y1, zm + j * h, zm + j * h + 1.6, "ext-blanc"))
    # portes doubles noires de grange (2 × 32 po × 76 po), impostes à 4 carreaux, écharpes en X
    ya, yb = y0 - 1.5, y0 + 0.2
    zp, zi = zs, zs + 76
    out += [B(porte[0] - 3, ya - 0.3, porte[0], yb, zp, zi + 14, "metal"), B(porte[1], ya - 0.3, porte[1] + 3, yb, zp, zi + 14, "metal"),
            B(porte[0] - 3, ya - 0.3, porte[1] + 3, yb, zi + 12, zi + 15, "metal")]
    for (a, b) in ((porte[0], xm - 0.25), (xm + 0.25, porte[1])):
        out.append(B(a, ya, b, yb, zp, zi, "porte-ext"))
        out += [B(a, ya - 0.8, b, ya, zp, zp + 4, "metal"), B(a, ya - 0.8, b, ya, zi - 4, zi, "metal"),
                B(a, ya - 0.8, b, ya, (zp + zi) / 2 - 2, (zp + zi) / 2 + 2, "metal"),
                B(a, ya - 0.8, a + 4, ya, zp, zi, "metal"), B(b - 4, ya - 0.8, b, ya, zp, zi, "metal")]
        zc = (zp + zi) / 2
        out += [T([(a + 4, ya - 0.5, zp + 4), (b - 4, ya - 0.5, zc - 2)], 1.0, "metal", pans=6),
                T([(a + 4, ya - 0.5, zc + 2), (b - 4, ya - 0.5, zi - 4)], 1.0, "metal", pans=6)]
        out += [B(a, ya + 0.6, b, ya + 1.0, zi, zi + 12, "vitre"), B(a, ya + 1.0, b, yb, zi, zi + 12, "ecran")]
        for j in range(5):
            xx = a + (b - a) * j / 4
            out.append(B(xx - 0.6, ya - 0.2, xx + 0.6, yb, zi, zi + 12, "metal"))
        out.append(B(a, ya - 0.2, b, yb, zi - 0.5, zi + 1, "metal"))
    out += [B(xm - 3, y0 - 6, xm + 3, y0, zi + 18, zi + 26, "metal"), B(xm - 2, y0 - 5, xm + 2, y0 - 1, zi + 19, zi + 25, "abat-jour")]
    return out


def mobilier_patio():
    """Sobre : table de 6 pi et 4 chaises (aluminium noir, dessus de bois), BBQ, deux bacs à plantes."""
    Z = Z_TERRASSE
    out = [B(236, 487, 308, 523, Z + 28.5, Z + 30, "placage"), B(238, 489, 306, 521, Z + 26.5, Z + 28.5, "metal")]
    out += [B(x - 1, y - 1, x + 1, y + 1, Z, Z + 26.5, "metal") for x in (240, 304) for y in (491, 519)]
    for (cx, cy, s) in ((254, 478, -1), (290, 478, -1), (254, 532, 1), (290, 532, 1)):
        out += [B(cx - 9, cy - 8, cx + 9, cy + 8, Z + 16.5, Z + 18, "metal"), {"forme": "arrondi", "x0": cx - 8.5, "y0": cy - 7.5,
                "x1": cx + 8.5, "y1": cy + 7.5, "z0": Z + 18, "z1": Z + 20, "mat": "tissu", "r": 2, "b": 0.6}]
        yb = cy + s * 8
        out += [B(cx - 9, yb - 0.75, cx + 9, yb + 0.75, Z + 18, Z + 33, "metal")]
        out += [B(x - 0.75, y - 0.75, x + 0.75, y + 0.75, Z, Z + 16.5, "metal") for x in (cx - 8, cx + 8) for y in (cy - 7, cy + 7)]
    # BBQ au gaz contre le garde-corps de l'escalier, face vers -x
    out += [B(361, 506, 381, 546, Z + 6, Z + 34, "metal"), B(360, 504, 382, 548, Z + 34, Z + 36, "inox"),
            {"forme": "cylindre", "axe": "y", "x": 371, "y0": 508, "y1": 544, "z": Z + 38, "r": 9, "mat": "inox"},
            B(361, 548, 381, 556, Z + 33, Z + 34.5, "metal"), B(361, 496, 381, 504, Z + 33, Z + 34.5, "metal"),
            {"forme": "cylindre", "axe": "x", "x0": 361, "x1": 381, "y": 508, "z": Z + 3, "r": 3, "mat": "pneu"}]
    out += [B(x - 1, y - 1, x + 1, y + 1, Z, Z + 6, "metal") for x in (362, 380) for y in (540, 545)]
    for (x, y) in ((172, 547), (172, 453)):
        out += [C(x, y, 9, Z, Z + 20, "ext-blanc", r2=10), SPH(x, y, Z + 27, 11, "plante", ecrase=0.8),
                SPH(x + 3, y - 2, Z + 34, 7, "plante")]
    return out


# ------------------------------------------------------------------------------------------------- terrain, allée, végétation
def terrain_et_vegetation():
    from shapely.geometry import Polygon, box
    from shapely.ops import unary_union
    out = []
    lot = Polygon(TERRAIN)
    maison = unary_union([box(*CORPS), box(*ENTREE_ARR), box(*PERRON), box(*CHEMINEE), box(*DESCENTE)])
    gazon = lot.difference(maison)
    for zone in (box(-500, -600, 700, 0), box(-500, 380, 700, 1000), box(-500, 0, 0, 380), box(456, 0, 700, 380)):
        g = gazon.intersection(zone)
        for q in (g.geoms if hasattr(g, "geoms") else [g]):
            if q.geom_type == "Polygon" and q.area > 10:
                out.append(P(list(q.exterior.coords)[:-1], SOL - 1, SOL + 0.25, "ext-gazon"))
    out.append(B(*ALLEE, SOL - 0.5, SOL + 0.6, "ext-asphalte"))
    # descente extérieure de la porte de côté (sous le terrain : visible quand le moteur coupera le gazon, EXTERIEUR["trous"])
    x0, y0, x1, y1 = DESCENTE
    r = SOL / 7
    out += [B(x1 - 6, y0, x1, y1, -6, SOL + 4, "beton"), B(x0, y1 - 6, x1, y1, -6, SOL + 4, "beton"),
            B(x0, y0 + 6 + 60, x1 - 6, y1 - 6, -6, 0, "beton")]
    for i in range(1, 7):
        out.append(B(x0, y0 + 6 + 10 * (i - 1), x1 - 6, y0 + 66, -6, SOL - r * i, "beton"))
    out += garde_corps((x1 - 3, y0), (x1 - 3, y1), SOL + 4, 36) + garde_corps((x0 + 1, y1 - 3), (x1, y1 - 3), SOL + 4, 36)
    # haie de cèdres le long de la ligne de lot oblique (cour arrière), 6 pi
    ys = [380 + 20 * i for i in range(26)] + [895]
    gauche = [(_ligne_gauche(y) + 6, y) for y in ys]
    droite = [(_ligne_gauche(y) + 32, y) for y in reversed(ys)]
    out.append(P(gauche + droite, SOL, SOL + 72, "ext-sapin"))
    # fond de lot : épinettes et bouleaux (au-delà de la ligne arrière), un érable sur le devant
    for (x, y, hh) in ((-20, 960, 330), (130, 985, 380), (330, 955, 300), (520, 975, 360), (620, 930, 320), (-120, 900, 300)):
        out += [C(x, y, 5, SOL, SOL + 40, "bois_brut"), C(x, y, hh * 0.15, SOL + 30, SOL + hh, "ext-sapin", r2=0, pans=10)]
    for (x, y) in ((40, 940), (250, 1000), (430, 945)):
        out += [C(x, y, 4, SOL, SOL + 260, "ext-bouleau", pans=10), SPH(x, y, SOL + 250, 55, "plante", ecrase=1.2),
                SPH(x + 25, y - 10, SOL + 205, 38, "plante")]
    out += [C(60, -250, 6, SOL, SOL + 110, "bois_brut"), SPH(60, -250, SOL + 160, 70, "plante", ecrase=0.9)]
    return out


def _planchers():
    Z = Z_TERRASSE
    r_esc = (Z - SOL) / 7
    out = [{"nom": "Palier de la porte arrière", "pts": rect(*PALIER), "z": Z},
           {"nom": "Patio", "pts": rect(*PATIO), "z": Z},
           {"nom": "Deck de la piscine", "pts": [[round(x, 1), round(y, 1)] for x, y in _deck_pts()], "z": Z}]
    out += [{"nom": f"Escalier de la cour, marche {i}", "pts": rect(ESC[0], ESC[1] + 9 * (i - 1), ESC[2], ESC[1] + 9 * i),
             "z": round(Z - r_esc * i, 2)} for i in range(1, 7)]
    r = (Z_PERRON - SOL) / 7
    out.append({"nom": "Perron avant", "pts": rect(*PERRON), "z": Z_PERRON})
    out += [{"nom": f"Marches du perron, marche {i}", "pts": rect(162, -48 - 11 * i, 234, -48 - 11 * (i - 1)),
             "z": round(Z_PERRON - r * i, 2)} for i in range(1, 7)]
    out.append({"nom": "Dalle du cabanon (devant les portes)", "pts": rect(CAB[0] - 4, CAB[1] - 4, CAB[2] + 4, CAB[1]), "z": SOL + 4})
    out += [{"nom": f"Pas japonais {i + 1}", "pts": [list(p) for p in d], "z": SOL + 1.5} for i, d in enumerate(DALLES)]
    x0, y0, x1, y1 = DESCENTE
    out += [{"nom": f"Descente de la porte de côté, marche {i}", "pts": rect(x0, y0 + 6 + 10 * (i - 1), x1 - 6, y0 + 6 + 10 * i),
             "z": round(SOL - SOL / 7 * i, 2)} for i in range(1, 7)]
    out.append({"nom": "Descente de la porte de côté, palier", "pts": rect(x0, y0 + 66, x1 - 6, y1 - 6), "z": 0})
    return out


def _obstacles():
    cx, cy, R = PISC
    yd = cy - math.sqrt(R ** 2 - (cx - 314) ** 2)
    return [{"nom": "Piscine", "pts": [[round(x, 1), round(y, 1)] for x, y in cercle(cx, cy, R + 1, 32)]},
            {"nom": "Cabanon", "pts": rect(*CAB)}, {"nom": "Muret", "pts": rect(*MURET)},
            {"nom": "Garde-corps du palier et de l'escalier", "pts": rect(453.5, 380, 456, 494)},
            {"nom": "Garde-corps patio / escalier", "pts": rect(385, 440, 387, 560)},
            {"nom": "Garde-corps du patio (bas)", "pts": rect(314, 557.5, 386, 560)},
            {"nom": "Garde-corps du patio (devant le mur)", "pts": rect(159, 440, 219, 442.5)},
            {"nom": "Garde-corps du patio (gauche)", "pts": rect(159, 440, 161.5, 560)},
            {"nom": "Verre patio / deck (le portillon, x 274-310, s'ouvre)", "pts": rect(159, 559, 274, 561)},
            {"nom": "Verre patio / deck, bout droit", "pts": rect(310, 559, 314, 561)},
            {"nom": "Garde-corps du deck (droite)", "pts": rect(311.5, 560, 314, yd)},
            {"nom": "Appareils de la piscine", "pts": [list(p) for p in APPAREILS]},
            {"nom": "Haie de cèdres", "pts": [[round(_ligne_gauche(380) + 6, 1), 380], [round(_ligne_gauche(380) + 32, 1), 380],
                                               [round(_ligne_gauche(895) + 32, 1), 895], [round(_ligne_gauche(895) + 6, 1), 895]]},
            {"nom": "Table du patio", "pts": rect(236, 487, 308, 523)}, {"nom": "BBQ", "pts": rect(360, 494, 382, 558)}]


EXTERIEUR = {
    "sol": SOL,
    "terrain": TERRAIN,
    "objets": enveloppe() + toit() + perron_avant() + cour() + terrain_et_vegetation(),
    "planchers": _planchers(),
    "obstacles": _obstacles(),
    "trous": [rect(DESCENTE[0], DESCENTE[1] + 6, DESCENTE[2] - 6, DESCENTE[3] - 6)],
    "visites": [
        {"nom": "Cour arrière — vue d'ensemble", "x": 535, "y": 640, "cap": 207, "z": SOL},
        {"nom": "Le patio", "x": 372, "y": 452, "cap": 123, "z": Z_TERRASSE},
        {"nom": "Le deck et la piscine", "x": 300, "y": 586, "cap": 140, "z": Z_TERRASSE},
        {"nom": "Le cabanon et les pas japonais", "x": 420, "y": 515, "cap": 80, "z": SOL},
        {"nom": "La piscine vue de la cour", "x": 60, "y": 560, "cap": 45, "z": SOL},
        {"nom": "Façade avant", "x": 300, "y": -390, "cap": 98, "z": SOL},
        {"nom": "L'allée et le côté", "x": 530, "y": -430, "cap": 100, "z": SOL},
    ],
    "lumieres": [{"x": 328.5, "y": 432, "z": 178, "i": 2}, {"x": 240, "y": -1.5, "z": 170, "i": 2},
                 {"x": 451, "y": 674, "z": 150, "i": 1.5}],
    "peintures": PEINTURES,
}
# appliques des portes (les lumières ci-dessus y sont placées)
EXTERIEUR["objets"] += [B(327.5, 429, 333, 435, 172, 184, "metal"), B(328.5, 430, 332, 434, 174, 182, "abat-jour"),
                        B(237, -5.5, 243, -0.5, 164, 176, "metal"), B(238, -4.5, 242, -1.5, 166, 174, "abat-jour")]
