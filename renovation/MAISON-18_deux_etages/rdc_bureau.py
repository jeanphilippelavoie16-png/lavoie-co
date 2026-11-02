"""MAISON-18 — RDC : la CHAMBRE AVANT devient le BUREAU (travail et gaming, deux postes assis côte à côte).

Demande du client : « La chambre avant devient un bureau de travail et de gaming (2 stations assis), idéalement face à la
fenêtre qui a une vue vers le fleuve. »

Fenêtre « vers le fleuve » : la pièce n'a qu'UNE fenêtre, ouv-RDC-001 sur la façade avant (y = 5 ; 75 po, axe à x = 98,
baie x 60,5 → 135,5). Le mur de gauche (x = 5) n'a pas de fenêtre dans cette pièce (ouv-RDC-006 est celle de la salle de
bain). La façade regarde vers le sud-sud-est (nord à 9,8° de +y, sens horaire) : c'est le côté du fleuve (HYPOTHÈSE à
confirmer avec le client).

Parti : un PLAN DE TRAVAIL CONTINU DE CHÊNE de mur à mur (132 × 30 po, dessus à 29,5 po) contre la façade, sous la fenêtre
(allège présumée à 34 po) ; deux postes de 54 po d'axe en axe (x = 60 et x = 114), tous deux tournés vers la fenêtre.
Par poste : un écran principal de 27 po droit devant, BAS (bas à 31,5 po, haut à 45,8 po, sous la hauteur des yeux), et
un écran de 24 po vertical sur le côté extérieur, pivoté de 28° ; les deux écrans principaux laissent libre le centre de la
fenêtre (x 72 → 102). Ordinateurs suspendus sous le plan aux deux bouts, caisson à 3 tiroirs au centre (il porte aussi
le plan), goulotte à câbles sous le bord arrière, ruban DEL blanc chaud sous le plan. Chaises ergonomiques (assise et
dossier de tissu anthracite, piètement noir). Dégagement de 36 po derrière les chaises (y 72 → 108).
Mur de gauche : lattes de chêne acoustiques sur feutre noir, du plancher au plafond. Mur arrière (salle de bain) peint
ardoise : crédence flottante de chêne (consoles, manettes, casques, jeux), ruban DEL dessous, deux panneaux de feutre
sable. Coin détente : fauteuil de cuir cognac, table d'appoint, liseuse. Toile solaire dans la fenêtre (contre-jour).

On reste DANS la pièce : la cloison de la garde-robe (x = 146) et sa porte (ouv-RDC-021) appartiennent au module de
l'entrée ; rien ici ne touche aux murs ni aux ouvertures. Pouces, repère de la maison.
"""
import math

PIECE = "piece-RDC-CH2"
NOM = "Bureau"

# --------------------------------------------------------------------------------------- repères de la pièce
XG, XD = 10.0, 143.75          # nu du mur gauche (extérieur, x = 5) ; nu de la cloison de la garde-robe (x = 146)
YF, YA = 10.0, 139.75          # nu de la façade (y = 5) ; nu de la cloison de la salle de bain (mur-RDC-R01, y = 142)
NICHE = (110.25, 139.75, 143.75, 154.75)     # renfoncement de la porte du dégagement (ouv-RDC-014, x 112 → 142)
FEN = (60.5, 135.5)            # baie de la fenêtre de façade ouv-RDC-001
ZONE = [(9.5, 9.5, 144.0, 140.4), (110.0, 139.5, 144.0, 155.0)]   # emprise : mobilier présumé de RDC-01 retiré

# plan de travail et postes
LAT = 11.1                     # face des lattes de chêne du mur gauche
PX0, PX1, PY1 = 11.25, 143.25, 40.0          # plan de travail : x de 11,25 à 143,25, y de la façade à 40
PZ0, PZ1 = 28.0, 29.5                        # dessous et dessus du plan
POSTES = (60.0, 114.0)                       # axes des deux postes (54 po d'axe en axe)
YCH = 57.5                                   # centre des chaises (bord avant de l'assise à 7 po du plan)
ZE0, ZE1 = 31.5, 45.8                        # écran 27 po : bas et haut (sous la hauteur des yeux, ≈ 46–48 po assis)
YE = 24.0                                    # dos des écrans principaux (bras articulés : on les avance ou recule)
CREDENCE = (60.0, 108.0, 121.75)             # crédence flottante : x0, x1, devant (dos au mur arrière)


# =============================================================================================== plan (P-130)
def _dim(v, note=None):
    d = {"valeur": v, "source": "PROPOSÉ", "photo": None}
    if note:
        d["note"] = note
    return d


ELEMENTS = [  # id, type, nom, libellé, x, y, rotation (dos vers −y à 0°), (longueur, largeur)
    ("elem-RDC-P-BUR-PLAN", "comptoir", "Plan de travail continu en chêne 132 × 30 po (dessus à 29,5 po), deux postes de 54 po "
     "face à la fenêtre ; ordinateurs suspendus dessous aux deux bouts, caisson à 3 tiroirs au centre, goulotte à câbles, "
     "ruban DEL blanc chaud", "2 POSTES", (PX0 + PX1) / 2, (YF + PY1) / 2, 0, (PX1 - PX0, PY1 - YF)),
    ("elem-RDC-P-BUR-CH1", "autre", "Chaise ergonomique, poste 1 (gauche)", "", POSTES[0], YCH, 180, (26, 26)),
    ("elem-RDC-P-BUR-CH2", "autre", "Chaise ergonomique, poste 2 (droite)", "", POSTES[1], YCH, 180, (26, 26)),
    ("elem-RDC-P-BUR-CRED", "armoires", "Crédence flottante de chêne 48 × 18 po (consoles, manettes, casques, jeux), DEL dessous",
     "", (CREDENCE[0] + CREDENCE[1]) / 2, (CREDENCE[2] + YA) / 2, 180, (CREDENCE[1] - CREDENCE[0], YA - CREDENCE[2])),
    ("elem-RDC-P-BUR-FAUT", "autre", "Fauteuil de détente en cuir cognac (coin détente), table d'appoint et liseuse", "",
     28.5, 118.5, 195, (26, 31)),
    ("elem-RDC-P-BUR-LATTES", "autre", "Mur de lattes de chêne acoustiques sur feutre noir (plancher au plafond)", "",
     XG + 0.6, (YF + YA) / 2, 90, (YA - YF, 1.2)),
]


def _element(eid, typ, nom, lib, x, y, rot, LW):
    e = {"id": eid, "type": typ, "nom": nom, "nom_original": None, "etat": "nouveau",
         "position": {"x": round(x, 2), "y": round(y, 2), "rotation_deg": rot, "source": "PROPOSÉ"},
         "dimensions": {"longueur": _dim(LW[0]), "largeur": _dim(LW[1])},
         "note": "bureau-gaming de MAISON-18 (rdc_bureau.py) ; mobilier proposé, chambre avant non photographiée : à mesurer"}
    e["libelle"] = lib
    return e


def appliquer_modifs_rdc(maison, ctx):
    rdc = ctx["rdc"]
    for p in rdc["pieces"]:
        if p["id"] == PIECE:
            p["nom"] = NOM
            p["description"] = ("Bureau de travail et de gaming (ancienne chambre avant) : deux postes assis face à la fenêtre "
                                "de façade (vue vers le fleuve), coin détente ; la garde-robe est conservée.")
            xs = [q[0] for q in p["polygone"]]
            ys = [q[1] for q in p["polygone"]]
            if abs(min(xs) - XG) > 0.5 or abs(max(xs) - XD) > 0.5 or abs(min(ys) - YF) > 0.5:
                print(f"  [rdc_bureau] ATTENTION : la pièce {PIECE} a changé ({min(xs)}..{max(xs)} × {min(ys)}..{max(ys)}) ; "
                      "revoir le plan de travail (prévu de x = 11,25 à 143,25)")
    rdc["elements"] = [e for e in rdc["elements"] if not e["id"].startswith("elem-RDC-P-BUR-")]
    rdc["elements"] += [_element(*t) for t in ELEMENTS]
    rdc["elements"].sort(key=lambda e: e["id"])
    rdc.setdefault("notes", []).append(
        {"id": "note-RDC-B01", "texte_original": None, "photo": None,
         "interpretation": "Bureau (ancienne chambre avant) : 2 postes assis face à la fenêtre de façade, plan continu "
                           "de chêne, écrans bas ; lattes acoustiques, crédence, coin détente."})


# =============================================================================================== maquette 3D
def _centre(o):
    f = o.get("forme", "boite")
    if "pts" in o and f in ("boite", "tube"):
        pts = o["pts"]
        return sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
    if f in ("boite", "arrondi"):
        return (o["x0"] + o["x1"]) / 2, (o["y0"] + o["y1"]) / 2
    if f == "cylindre" and o.get("axe") == "y":
        return o["x"], (o["y0"] + o["y1"]) / 2
    if f == "cylindre" and o.get("axe") == "x":
        return (o["x0"] + o["x1"]) / 2, o["y"]
    return o.get("x", -1e9), o.get("y", -1e9)


def _dans_zone(x, y):
    return any(a <= x <= c and b <= y <= d for a, b, c, d in ZONE)


def _dalle(h, p0, u, larg, ep, z0, z1, mat, cote=1):
    """Plaque mince inclinée en plan : bord p0, direction u (unitaire), largeur larg, épaisseur ep vers l'arrière
    (normale −n, n = u tourné de 90° du côté « cote ») ; prisme de z0 à z1."""
    n = (-u[1] * cote, u[0] * cote)
    a = p0
    b = (p0[0] + u[0] * larg, p0[1] + u[1] * larg)
    c = (b[0] - n[0] * ep, b[1] - n[1] * ep)
    d = (a[0] - n[0] * ep, a[1] - n[1] * ep)
    pts = [a, b, c, d]
    # sens antihoraire pour l'extrusion
    s = sum(pts[i][0] * pts[(i + 1) % 4][1] - pts[(i + 1) % 4][0] * pts[i][1] for i in range(4))
    if s < 0:
        pts.reverse()
    return {"forme": "boite", "pts": [[round(x, 3), round(y, 3)] for x, y in pts], "z0": z0, "z1": z1, "mat": mat}


def _ecran27(h, xc):
    """Écran 27 po (24,4 × 14,3 po) sur bras, droit devant le poste, émission animée ; bras à pince sur le bord arrière."""
    B, A, C, T = h.B, h.A, h.C, h.T
    return [A(xc - 12.2, YE, xc + 12.2, YE + 1.0, ZE0, ZE1, "carbone", r=0.25, b=0.15),
            {"forme": "ecran", "x": xc, "y": YE + 1.06, "z0": ZE0 + 0.5, "z1": ZE1 - 0.5, "larg": 23.6, "face": "+y"},
            B(xc - 2.2, YE - 0.6, xc + 2.2, YE, 36.5, 41.0, "metal"),
            C(xc, 13.5, 0.75, PZ1, 42.5, "metal"), B(xc - 1.6, 11.2, xc + 1.6, 15.8, 26.2, PZ0, "metal"),
            T([(xc, 13.5, 40.5), (xc, 18.5, 39.8), (xc, YE - 0.6, 38.8)], 0.55, "metal", bouts=True)]


def _ecran_vertical(h, xc, sens):
    """Écran 24 po vertical (12,6 × 21,4 po) sur le côté extérieur du poste (sens −1 : à gauche, +1 : à droite), pivoté
    de 28° vers l'usager ; éteint (verre noir). Bras secondaire depuis le même poteau."""
    T = h.T
    a = math.radians(28)
    u = (sens * math.cos(a), math.sin(a))
    p0 = (xc + sens * 12.9, YE + 0.6)
    cote = sens                                   # n = u tourné vers l'usager (face de l'écran)
    z0, z1 = ZE0, ZE0 + 21.4
    out = [_dalle(h, p0, u, 12.6, 0.8, z0, z1, "carbone", cote)]
    q0 = (p0[0] + u[0] * 0.45, p0[1] + u[1] * 0.45)
    n = (-u[1] * cote, u[0] * cote)
    q0 = (q0[0] + n[0] * 0.06, q0[1] + n[1] * 0.06)
    out.append(_dalle(h, q0, u, 11.7, 0.05, z0 + 0.5, z1 - 0.5, "ecran", cote))
    # écran allumé en mode sombre (clavardage, guide, musique) : bandeau et lignes de texte stylisées
    def ligne(d0, larg, za, zb, mat):
        p = (p0[0] + u[0] * d0 + n[0] * 0.11, p0[1] + u[1] * d0 + n[1] * 0.11)
        return _dalle(h, p, u, larg, 0.04, za, zb, mat, cote)
    out.append(ligne(1.0, 10.6, z1 - 2.6, z1 - 1.3, "jete"))
    for k, (d0, larg, mat) in enumerate(((1.0, 8.5, "gris"), (1.0, 6.0, "gris"), (2.2, 7.8, "blanc"), (1.0, 9.2, "gris"),
                                         (1.0, 5.0, "gris"), (2.2, 6.6, "blanc"), (1.0, 8.0, "gris"), (1.0, 7.2, "gris"),
                                         (2.2, 5.4, "blanc"), (1.0, 9.0, "gris"))):
        za = z1 - 4.4 - k * 1.55
        out.append(ligne(d0, larg, za, za + 0.5, mat))
    out.append(ligne(1.0, 10.6, z0 + 1.4, z0 + 2.3, "gris"))
    m =(p0[0] + u[0] * 6.3 - n[0] * 0.8, p0[1] + u[1] * 6.3 - n[1] * 0.8)
    out.append(T([(xc, 13.5, 42.0), ((xc + m[0]) / 2, 15.5, 42.5), (m[0] - n[0] * 1.2, m[1] - n[1] * 1.2, 42.0)], 0.5, "metal", bouts=True))
    return out


def _poste(h, xc, sens):
    """Un poste : écrans, tapis de bureau, clavier, souris, passe-câble."""
    A, B = h.A, h.B
    out = _ecran27(h, xc) + _ecran_vertical(h, xc, sens)
    out += [A(xc - 17, 27.5, xc + 17, 39.0, PZ1, PZ1 + 0.15, "anthracite", r=1, b=0.05),
            A(xc - 8.5, 30.0, xc + 5.5, 34.8, PZ1 + 0.15, PZ1 + 1.0, "carbone", r=0.4, b=0.2),
            B(xc - 8.0, 30.4, xc + 5.0, 34.4, PZ1 + 1.0, PZ1 + 1.05, "gris"),
            A(xc + 9.5, 30.5, xc + 12.0, 34.6, PZ1 + 0.15, PZ1 + 1.4, "carbone", r=1.2, b=0.45),
            B(xc + sens * 20 - 3, 11.2, xc + sens * 20 + 3, 12.8, PZ1, PZ1 + 0.05, "carbone")]       # passe-câble
    return out


def _chaise(h, xc, yc):
    """Chaise ergonomique (travail et jeu) qui regarde vers −y : piètement 5 branches à roulettes, assise et haut dossier
    de tissu anthracite, appui-tête, accoudoirs réglables (ils passent sous le plan, dessous à 28 po)."""
    A, B, C, T = h.A, h.B, h.C, h.T
    out = []
    for k in range(5):
        a = math.radians(90 + 72 * k)
        px, py = xc + 12 * math.cos(a), yc + 12 * math.sin(a)
        out += [T([(xc, yc, 3.6), (px, py, 2.6)], 0.75, "carbone"), {"forme": "sphere", "x": px, "y": py, "z": 1.3, "r": 1.3, "mat": "carbone"}]
    out += [C(xc, yc, 2.0, 2.4, 4.4, "carbone"), C(xc, yc, 1.0, 4.4, 16.5, "metal"), C(xc, yc, 1.5, 4.4, 10, "carbone"),
            B(xc - 5, yc - 4, xc + 5, yc + 6, 16.2, 18.2, "carbone")]
    out += [A(xc - 10.25, yc - 10.5, xc + 10.25, yc + 9.0, 18.0, 21.4, "anthracite", r=3, b=1.2),            # assise
            B(xc - 1.2, yc + 8.0, xc + 1.2, yc + 13.0, 16.5, 19.0, "carbone"),
            B(xc - 1.2, yc + 12.0, xc + 1.2, yc + 13.6, 18.0, 30.0, "carbone"),                              # dosseret
            A(xc - 9.5, yc + 9.6, xc + 9.5, yc + 12.4, 22.5, 35.0, "anthracite", r=2.5, b=1.0),
            A(xc - 9.0, yc + 10.6, xc + 9.0, yc + 13.4, 34.5, 47.0, "anthracite", r=2.5, b=1.0),
            A(xc - 6.0, yc + 11.6, xc + 6.0, yc + 14.2, 48.0, 53.5, "anthracite", r=2.0, b=0.8),             # appui-tête
            B(xc - 1.0, yc + 12.6, xc + 1.0, yc + 13.8, 46.5, 48.5, "carbone"),
            A(xc - 7.5, yc + 9.2, xc + 7.5, yc + 10.0, 25.0, 31.0, "carbone", r=1.5, b=0.3)]                # appui lombaire
    for s in (-1, 1):
        xa = xc + s * 11.2
        out += [B(xa - 0.7, yc - 1.0, xa + 0.7, yc + 2.0, 19.0, 26.0, "carbone"),
                B(xa - 0.5, yc + 1.0, xa + 0.5, yc + 6.0, 19.0, 20.0, "carbone"),
                A(xa - 1.6, yc - 6.0, xa + 1.6, yc + 4.0, 26.0, 27.4, "carbone", r=1.2, b=0.4)]
    return out


def _ordinateur(h, x0, vitre):
    """Tour (8,5 × 18 × 18,5 po) suspendue sous le plan dans deux sangles d'acier noir ; panneau vitré côté chaise."""
    A, B = h.A, h.B
    x1 = x0 + 8.5
    out = [A(x0, 13.5, x1, 31.5, 8.5, 27.0, "carbone", r=0.5, b=0.3)]
    xv = x1 if vitre > 0 else x0
    out += [B(min(xv, xv + vitre * 0.15), 14.5, max(xv, xv + vitre * 0.15), 30.5, 9.5, 26.0, "ecran"),
            B((x0 + x1) / 2 - 0.3, 31.5, (x0 + x1) / 2 + 0.3, 31.7, 11.0, 25.0, "abat-jour"),            # liseré DEL
            B((x0 + x1) / 2 - 0.6, 31.5, (x0 + x1) / 2 + 0.6, 31.7, 25.6, 26.2, "spot")]
    for y in (17.0, 28.0):
        out += [B(x0 - 0.4, y, x0, y + 1.2, 8.1, PZ0, "metal"), B(x1, y, x1 + 0.4, y + 1.2, 8.1, PZ0, "metal"),
                B(x0 - 0.4, y, x1 + 0.4, y + 1.2, 8.1, 8.5, "metal")]
    return out


def _plan_de_travail(h):
    A, B = h.A, h.B
    out = [A(PX0, YF + 0.25, PX1, PY1, PZ0, PZ1, "placage", r=0.4, b=0.3)]
    for xa in (12.6, 140.6):                                                    # pattes en U d'acier noir mat
        out += [B(xa, 12.0, xa + 2.0, 14.0, 0, PZ0, "noir-mat"), B(xa, 36.0, xa + 2.0, 38.0, 0, PZ0, "noir-mat"),
                B(xa, 12.0, xa + 2.0, 38.0, PZ0 - 1.5, PZ0, "noir-mat"), B(xa, 12.0, xa + 2.0, 38.0, 0, 1.2, "noir-mat")]
    # caisson suspendu à 3 tiroirs, entre les postes (il porte aussi le milieu du plan) ; tirettes de laiton
    out += [A(79.0, 12.0, 97.0, 37.5, 6.0, PZ0, "noir-mat", r=0.3, b=0.2)]
    out += [B(79.4, 37.5, 96.6, 37.65, z - 0.12, z + 0.12, "carbone") for z in (13.4, 20.7)]
    out += [B(84.0, 37.6, 92.0, 38.0, z, z + 0.45, "laiton") for z in (11.4, 18.7, 25.9)]
    # goulotte à câbles sous le bord arrière, entre les deux ordinateurs ; ruban DEL blanc chaud sous le plan, contre le mur
    out += [B(38.5, 11.0, 130.5, 16.0, 22.0, 22.4, "metal"), B(38.5, 15.6, 130.5, 16.0, 22.0, 25.5, "metal"),
            B(38.5, 11.0, 39.0, 16.0, 22.0, 25.5, "metal"), B(130.0, 11.0, 130.5, 16.0, 22.0, 25.5, "metal")]
    out += [B(15.0, 10.2, 140.0, 10.8, 27.3, 27.8, "abat-jour")]
    out += _ordinateur(h, 28.0, +1) + _ordinateur(h, 131.0, -1)
    return out


def _credence(h):
    """Crédence flottante de chêne (48 × 18 × 18 po, dessous à 9 po) : deux portes à poussoir (consoles, manettes,
    casques) et une niche ouverte (jeux, panier) ; ruban DEL sous le meuble. Dessus : 2 supports à casque, socle de
    recharge des manettes."""
    A, B, C, T, TOR, CX = h.A, h.B, h.C, h.T, h.TOR, h.CX
    x0, x1, y0 = CREDENCE
    y1, z0, z1 = YA - 0.15, 9.0, 27.0
    xn = x1 - 16.0                                       # début de la niche ouverte
    out = [A(x0, y0, xn, y1, z0, z1, "placage", r=0.3, b=0.2)]
    out += [B(xn, y0, x1, y1, z0, z0 + 1.5, "placage"), B(xn, y0, x1, y1, z1 - 1.5, z1, "placage"),
            B(x1 - 1.0, y0, x1, y1, z0, z1, "placage"), B(xn, y1 - 1.0, x1, y1, z0, z1, "carbone"),
            B(xn, y0 + 0.5, x1 - 1.0, y1 - 1.0, 18.3, 19.1, "placage")]
    out += [B((x0 + xn) / 2 - 0.1, y0 - 0.1, (x0 + xn) / 2 + 0.1, y0, z0 + 0.4, z1 - 0.4, "carbone"),
            B(xn - 0.1, y0 - 0.1, xn + 0.1, y0, z0 + 0.4, z1 - 0.4, "carbone")]
    # jeux (boîtiers debout) et panier des manettes dans la niche
    tons = ("carbone", "blanc", "rouge-velo", "jete", "carbone", "gris", "blanc", "osier", "carbone", "rouge-velo",
            "gris", "blanc", "jete", "carbone", "cuir", "blanc")
    for k, t in enumerate(tons):
        xa = xn + 0.6 + k * 0.62
        out.append(B(xa, y0 + 4.5, xa + 0.56, y0 + 11.5, z0 + 1.5, z0 + 1.5 + 6.7, t))
    out.append(A(xn + 1.0, y0 + 2.0, x1 - 2.0, y1 - 2.0, 19.1, 24.6, "osier", r=1.0, b=0.4, trou=0.6))
    out += [B(x0 + 2.0, y1 - 6.0, x1 - 2.0, y1 - 0.2, z0 - 1.2, z0, "noir-mat"),                  # rail d'appui au mur
            B(x0 + 2.0, y1 - 6.5, x1 - 2.0, y1 - 5.9, z0 - 0.9, z0 - 0.5, "abat-jour")]           # DEL sous la crédence
    # dessus : deux supports à casque, socle de recharge et deux manettes
    for xs in (x0 + 7.0, x0 + 15.0):
        ys = (y0 + y1) / 2 + 1.0
        out += [C(xs, ys, 2.2, z1, z1 + 0.5, "metal"), C(xs, ys, 0.35, z1 + 0.5, z1 + 10.0, "metal"),
                B(xs - 1.6, ys - 0.5, xs + 1.6, ys + 0.5, z1 + 9.6, z1 + 10.2, "metal"),
                TOR(xs, ys, z1 + 7.0, 3.7, 0.55, "carbone", arc=math.pi),
                CX(xs - 4.5, xs - 3.0, ys, z1 + 6.0, 1.9, "carbone"), CX(xs + 3.0, xs + 4.5, ys, z1 + 6.0, 1.9, "carbone")]
    xd = x0 + 26.0
    out += [A(xd, y0 + 4.0, xd + 11.0, y0 + 9.0, z1, z1 + 1.0, "carbone", r=1.0, b=0.3),
            A(xd + 0.6, y0 + 4.6, xd + 5.0, y0 + 8.4, z1 + 1.0, z1 + 2.6, "blanc", r=1.5, b=0.6),
            A(xd + 6.0, y0 + 4.6, xd + 10.4, y0 + 8.4, z1 + 1.0, z1 + 2.6, "carbone", r=1.5, b=0.6)]
    out += [h.MOD("plante_sansevieria", x1 - 6.5, (y0 + y1) / 2, z=z1, H=20)]
    return out


def _lattes(h):
    """Mur gauche : panneaux de lattes de chêne (1,1 po, pas de 1,75 po) sur feutre noir, 94,5 po de haut."""
    B = h.B
    R = [B(XG, YF, XG + 0.35, YA, 0.75, 95.25, "feutre-noir")]
    M = []
    y = YF + 0.6
    while y + 1.1 <= YA - 0.3:
        M.append(B(XG + 0.35, y, LAT, y + 1.1, 0.75, 95.25, "placage"))
        y += 1.75
    return R, M


def _detente(h):
    A, B, C, MOD = h.A, h.B, h.C, h.MOD
    return [MOD("fauteuil_cuir", 29.0, 117.5, face="-y", rot=15),
            MOD("table_appoint", 50.5, 129.0, face="-y"),
            MOD("lampe_pied", 16.5, 133.0, face="-y", rot=35)]


def appliquer_scene_rdc(S, h):
    A, B = h.A, h.B
    # 1) retirer le mobilier présumé de RDC-01 (lit, chevets, commode) et sa lumière
    garder = lambda o: o.get("role") or o.get("ouverture") or not _dans_zone(*_centre(o))   # battants de portes : jamais
    S["mobilier"] = [o for o in S["mobilier"] if garder(o)]
    S["revetements"] = [o for o in S["revetements"] if garder(o)]
    S["lumieres"] = [l for l in S["lumieres"] if not _dans_zone(l["x"], l["y"])]
    # 2) couleurs : feutres et tissu (alias pour le mobilier), mur arrière ardoise
    S.setdefault("peintures", {}).update({
        "Anthracite": ["#2F3134", "tissu des chaises et tapis de bureau (bureau du RDC)", "anthracite"],
        "Feutre sable": ["#B9A88B", "panneaux acoustiques de feutre du bureau (à choisir sur échantillon)", "feutre-sable"],
        "Feutre noir": ["#1C1D1F", "feutre sous les lattes de chêne du bureau", "feutre-noir"],
    })
    if "Ardoise" not in S["peintures"]:
        S["peintures"]["Ardoise"] = ["#2C302F", "mur arrière du bureau", "ardoise-tableau"]
    S.setdefault("accents", []).append({"piece": PIECE, "mur": "mur-RDC-R01", "peinture": "Ardoise"})
    # 3) mobilier
    M = []
    M += _plan_de_travail(h)
    M += _poste(h, POSTES[0], -1) + _poste(h, POSTES[1], +1)
    M += _chaise(h, POSTES[0], YCH) + _chaise(h, POSTES[1], YCH)
    M += _credence(h)
    M += _detente(h)
    R, lat = _lattes(h)
    M += lat
    # panneaux de feutre sable au mur ardoise, au-dessus de la crédence
    xm = (CREDENCE[0] + CREDENCE[1]) / 2
    M += [A(xm - 22.0, YA - 1.4, xm - 1.5, YA, 44.0, 80.0, "feutre-sable", r=0.4, b=0.35),
          A(xm + 1.5, YA - 1.4, xm + 22.0, YA, 44.0, 80.0, "feutre-sable", r=0.4, b=0.35)]
    # tapis à poils ras sous les chaises (roulettes) ; toile solaire enroulée en haut de la fenêtre
    M += [A(34.0, 34.0, 139.0, 104.0, 0, 0.35, "tapis", r=1.5, b=0.12)]
    # (2026-11-02) la toile suit la tête de la fenêtre : 80 po dans la vidéo DAG (SCENE["fenetres"]), 82 avant
    dz = 82 - ((S.get("fenetres") or {}).get("ouv-RDC-001") or {}).get("tete", S.get("tete_fenetre", 82))
    M += [B(FEN[0] + 0.5, 6.3, FEN[1] - 0.5, 8.2, 77.6 - dz, 81.8 - dz, "gris"),
          B(FEN[0] + 1.0, 7.0, FEN[1] - 1.0, 7.3, 75.5 - dz, 77.6 - dz, "gris")]
    # petite plante au bout gauche du plan
    M += [h.MOD("plante_syngonium", 21.0, 21.0, z=PZ1, H=17)]
    S["mobilier"] += M
    S["revetements"] += R
    # 4) éclairage : 2 encastrés à gradateur, lueur du ruban DEL sous le plan, liseuse du coin détente
    S["lumieres"] += [{"x": 46, "y": 92}, {"x": 112, "y": 92},
                      {"x": 87, "y": 18, "z": 30, "i": 2}, {"x": 22, "y": 126, "z": 66, "i": 2.5}]
    # 5) arrêts de visite (à la place de « Chambre avant (présumée) »)
    arrets = [{"nom": "Bureau et gaming", "x": 128, "y": 134, "cap": 238},
              {"nom": "Bureau et gaming, coin détente", "x": 104, "y": 62, "cap": 148}]
    v = S.get("visites", [])
    i = next((k for k, a in enumerate(v) if "Chambre avant" in a.get("nom", "")), len(v))
    S["visites"] = v[:i] + arrets + [a for a in v[i:] if "Chambre avant" not in a.get("nom", "")]
    S.setdefault("palette", []).append(
        ["Bureau", "plan de travail continu de chêne sur acier noir mat, lattes de chêne acoustiques, mur ardoise, "
                   "feutre sable, chaises anthracite, DEL blanc chaud 2700 K", "#B9A88B"])
