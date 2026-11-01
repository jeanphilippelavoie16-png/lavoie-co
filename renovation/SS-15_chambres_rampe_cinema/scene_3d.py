"""Maquette 3D de SS-15 (chambres agrandies, caveau en walk-in, rampe de métal à l'escalier, divan en L avec projecteur
et toile, rangement sous l'escalier), reprise de SS-14 et SS-07 : vestiaire près de l'entrée, coin frigo dans le séjour, escalier à marches tournantes, gym
(tapis roulant et vélo de route dans le même sens, poids au sol), bain sur pied. Matériaux réels (catalogue_materiaux.py) et modèles 3D (catalogue_modeles.py).

Coordonnées en pouces, repère de la maison. Le mobilier sert à juger les volumes et l'ambiance ; ce n'est pas un choix
de produit.
"""
import math

TITRE = "SS-15 — Chambres, rampe, coin cinéma"


def B(x0, y0, x1, y1, z0, z1, mat, r=None):
    o = {"forme": "boite", "x0": x0, "y0": y0, "x1": x1, "y1": y1, "z0": z0, "z1": z1, "mat": mat}
    if r:
        o["r"] = r
    return o


def A(x0, y0, x1, y1, z0, z1, mat, r=3, b=0.5, trou=None):
    """Bloc à coins arrondis en plan et arêtes adoucies (trou = paroi d'épaisseur donnée)."""
    o = {"forme": "arrondi", "x0": x0, "y0": y0, "x1": x1, "y1": y1, "z0": z0, "z1": z1, "mat": mat, "r": r, "b": b}
    if trou:
        o["trou"] = trou
    return o


def C(x, y, r, z0, z1, mat, **k):
    return dict({"forme": "cylindre", "x": x, "y": y, "r": r, "z0": z0, "z1": z1, "mat": mat}, **k)


def CY(x, y0, y1, z, r, mat, **k):
    return dict({"forme": "cylindre", "axe": "y", "x": x, "y0": y0, "y1": y1, "z": z, "r": r, "mat": mat}, **k)


def CX(x0, x1, y, z, r, mat, **k):
    return dict({"forme": "cylindre", "axe": "x", "x0": x0, "x1": x1, "y": y, "z": z, "r": r, "mat": mat}, **k)


def T(pts, r, mat, **k):
    return dict({"forme": "tube", "pts": [list(p) for p in pts], "r": r, "mat": mat}, **k)


def SPH(x, y, z, r, mat, **k):
    return dict({"forme": "sphere", "x": x, "y": y, "z": z, "r": r, "mat": mat}, **k)


def TOR(x, y, z, R, r, mat, **k):
    return dict({"forme": "tore", "x": x, "y": y, "z": z, "R": R, "r": r, "mat": mat}, **k)


def MOD(cle, x, y, rot=0, z=0, **k):
    return dict({"forme": "modele", "cle": cle, "x": x, "y": y, "z": z, "rot": rot}, **k)


# ---------------------------------------------------------------------------------------------------- meubles
def sofa(x0, y0, x1, y1, dos):
    out = [A(x0, y0, x1, y1, 0, 17, "tissu", r=2, b=1.5)]
    e = 8
    out.append({"+y": A(x0, y1 - e, x1, y1, 17, 32, "tissu", r=2, b=1.5), "-y": A(x0, y0, x1, y0 + e, 17, 32, "tissu", r=2, b=1.5),
                "+x": A(x1 - e, y0, x1, y1, 17, 32, "tissu", r=2, b=1.5), "-x": A(x0, y0, x0 + e, y1, 17, 32, "tissu", r=2, b=1.5)}[dos])
    return out


def fauteuil(x, y, dos):
    out = sofa(x - 15, y - 15, x + 15, y + 15, dos) + [A(x - 15, y - 15, x - 11, y + 15, 17, 24, "tissu", r=1.5, b=1.2),
                                                         A(x + 11, y - 15, x + 15, y + 15, 17, 24, "tissu", r=1.5, b=1.2)]
    for o in out:
        o["mat"] = "cuir"
    return out


def lit(x0, y0, x1, y1):
    """Lit queen, tête de lit rembourrée contre le mur arrière (y1)."""
    xm = (x0 + x1) / 2
    return [A(x0, y0, x1, y1 - 4, 2, 13, "placage", r=1, b=0.4),
            A(x0 + 1, y0 + 1, x1 - 1, y1 - 5, 13, 22, "draps", r=3, b=2.5),
            A(x0 + 0.5, y0 + 0.5, x1 - 0.5, y0 + 30, 21, 23.5, "jete", r=2, b=1),
            A(x0 + 5, y1 - 22, xm - 2, y1 - 6, 21, 28, "draps", r=4, b=3), A(xm + 2, y1 - 22, x1 - 5, y1 - 6, 21, 28, "draps", r=4, b=3),
            A(x0 - 6, y1 - 4, x1 + 6, y1, 0, 48, "tissu", r=1.5, b=1.5)]


def table_chevet(x, y):
    return [A(x - 10, y - 8, x + 10, y + 8, 6, 22, "placage", r=1, b=0.4)] + \
           [C(x + dx, y + dy, 0.5, 0, 6, "metal") for dx in (-8, 8) for dy in (-6, 6)] + \
           [C(x, y, 3.5, 22, 23, "metal"), C(x, y, 0.4, 23, 33, "laiton"), C(x, y, 7, 31, 39, "abat-jour", r2=5)]


def etagere(x0, y0, x1, y1):
    out = [B(x0, y0, x0 + 1.5, y1, 0, 84, "metal"), B(x1 - 1.5, y0, x1, y1, 0, 84, "metal")]
    out += [B(x0 + 1.5, y0, x1 - 1.5, y1, z, z + 1, "placage") for z in (4, 22, 40, 58, 76)]
    return out


def appareil(x0, x1, y_dos, y_face):
    """Laveuse ou sécheuse frontale : caisse blanche, hublot, bandeau de commandes."""
    xc = (x0 + x1) / 2
    return [A(x0, y_dos, x1, y_face, 0, 36, "blanc", r=1.5, b=0.6), CY(xc, y_face, y_face + 0.4, 18, 8.5, "inox"),
            CY(xc, y_face + 0.3, y_face + 0.8, 18, 7, "ecran"), B(x0 + 1, y_face - 0.2, x1 - 1, y_face + 0.2, 31, 35, "gris")]


# ---------------------------------------------------------------------------------------------------- gym
def velo_route(xa, y, sens=1, mat_cadre="rouge-velo"):
    """Vélo de route monté sur une base d'entraînement à transmission directe (roue arrière enlevée).
    xa : axe arrière ; le vélo regarde vers +x (sens=1). Géométrie d'un cadre de 56 cm, roues 700c."""
    X = lambda dx: xa + sens * dx
    zr = 13.2                                    # hauteur des axes
    bb, st, ht0, ht1 = (X(16), 10.6), (X(10.2), 30.4), (X(37.2), 27.0), (X(35.9), 32.6)
    out = []
    tubes = [(bb, st, 0.75), (st, ht1, 0.6), (bb, ht0, 0.85), (ht0, ht1, 0.8)]
    out += [T([(a[0], y, a[1]), (b[0], y, b[1])], r, mat_cadre, bouts=True) for a, b, r in tubes]
    for dy in (-2.3, 2.3):                       # haubans et bases
        out.append(T([(bb[0], y + dy / 3, bb[1]), (X(0), y + dy, zr)], 0.45, mat_cadre, bouts=True))
        out.append(T([(X(9.6), y + dy / 3, 28.4), (X(0), y + dy, zr)], 0.4, mat_cadre, bouts=True))
        out.append(T([(ht0[0], y + dy / 4, ht0[1]), (X(39.4), y + dy * 0.9, zr)], 0.45, "carbone", bouts=True))  # fourche
    xf = X(39.4)
    out += [T([(st[0], y, st[1]), (X(8.6), y, 36.5)], 0.5, "carbone"),                                         # tige de selle
            A(min(X(3), X(14)), y - 1.4, max(X(3), X(14)), y + 1.4, 36.4, 38, "cuir", r=1.3, b=0.6),             # selle
            T([(ht1[0], y, ht1[1]), (X(39.6), y, 33.6)], 0.55, "carbone"),                                     # potence
            T([(X(39.6), y - 8.5, 33.6), (X(39.6), y + 8.5, 33.6)], 0.5, "carbone")]                           # cintre
    for dy in (-8.5, 8.5):                       # cocottes et drops
        out.append(T([(X(39.6), y + dy, 33.6), (X(42.5), y + dy, 33.4), (X(44.2), y + dy, 30.6), (X(43.1), y + dy, 27.4),
                      (X(39.4), y + dy, 27.6)], 0.5, "pneu"))
        out.append(A(min(X(41), X(44)), y + dy - 0.8, max(X(41), X(44)), y + dy + 0.8, 33.4, 35.6, "pneu", r=0.7, b=0.5))
    out += [TOR(xf, y, zr, 12.6, 0.62, "pneu"), TOR(xf, y, zr, 11.7, 0.75, "carbone"), CY(xf, y - 2, y + 2, zr, 0.8, "metal")]
    out += [T([(xf, y, zr), (xf + 11.2 * math.cos(a), y + (0.9 if i % 2 else -0.9), zr + 11.2 * math.sin(a))], 0.07, "inox")
            for i, a in enumerate(i * math.pi / 9 for i in range(18))]
    # pédalier : plateau, manivelles, pédales
    out += [TOR(bb[0], y - 3, bb[1], 4.1, 0.22, "inox"), CY(bb[0], y - 3.2, y + 3.2, bb[1], 0.8, "metal")]
    for s, (dx, dz) in ((-1, (2.1, 6.5)), (1, (-2.1, -6.5))):
        out.append(T([(bb[0], y + s * 3.4, bb[1]), (bb[0] + dx, y + s * 3.4, bb[1] + dz)], 0.45, "carbone"))
        out.append(A(bb[0] + dx - 1.8, y + s * 4.3 - 1.4, bb[0] + dx + 1.8, y + s * 4.3 + 1.4, bb[1] + dz - 0.4, bb[1] + dz + 0.4, "metal", r=0.5, b=0.2))
    # base d'entraînement : boîtier, volant d'inertie, cassette, pattes
    out += [A(xa - 9, y - 4.5, xa + 7, y + 4.5, 3.5, 17, "metal", r=3, b=1), CY(xa - 2, y - 7.2, y - 4.4, 12, 9.5, "carbone"),
            CY(xa, y - 4.5, y - 2.4, zr, 2.4, "inox", pans=24), CY(xa, y - 2.5, y + 2.5, zr, 0.6, "inox")]
    out += [A(xa - 6 + dx - 1.2, y - 15, xa - 6 + dx + 1.2, y + 15, 0, 2.4, "metal", r=1, b=0.5) for dx in (-6, 8)]
    out += [A(min(X(34), X(45)), y - 6, max(X(34), X(45)), y + 6, 0, 1.2, "pneu", r=3, b=0.5)]                   # cale avant
    return out


def tapis_roulant(x0, y0):
    """Tapis roulant de maison (68 × 30 po) le long de x, console vers +x (même sens que le vélo, face au séjour)."""
    x1, y1 = x0 + 68, y0 + 30
    return [A(x0, y0, x1 - 10, y1, 1.5, 7.5, "carbone", r=2, b=0.8),                       # plateau
            B(x0 + 1, y0 + 4, x1 - 12, y1 - 4, 7.5, 7.9, "caoutchouc-noir"),                # bande
            A(x0 + 2, y0, x1 - 14, y0 + 3.5, 6.5, 8.6, "gris", r=1, b=0.5), A(x0 + 2, y1 - 3.5, x1 - 14, y1, 6.5, 8.6, "gris", r=1, b=0.5),
            A(x1 - 14, y0 + 1, x1, y1 - 1, 1.5, 11, "carbone", r=4, b=1.5),                  # capot du moteur
            T([(x1 - 8, y0 + 2, 10), (x1 - 4, y0 + 1.5, 46)], 1.1, "carbone"), T([(x1 - 8, y1 - 2, 10), (x1 - 4, y1 - 1.5, 46)], 1.1, "carbone"),
            A(x1 - 9, y0 - 0.5, x1 + 1, y1 + 0.5, 44, 50, "carbone", r=3, b=1.2),           # console
            B(x1 - 6.2, y0 + 7, x1 - 5.6, y1 - 7, 46, 49.5, "ecran"),
            T([(x1 - 6, y0 + 0.5, 46.5), (x1 - 18, y0 + 0.5, 41)], 0.75, "pneu", bouts=True),
            T([(x1 - 6, y1 - 0.5, 46.5), (x1 - 18, y1 - 0.5, 41)], 0.75, "pneu", bouts=True)]


def haltere(x, y, r, l=12):
    """Haltère hexagonal couché le long de x."""
    return [CX(x - l / 2 + 2.6, x + l / 2 - 2.6, y, r, 0.6, "inox"),
            CX(x - l / 2, x - l / 2 + 2.6, y, r, r, "caoutchouc-noir", pans=6), CX(x + l / 2 - 2.6, x + l / 2, y, r, r, "caoutchouc-noir", pans=6)]


def kettlebell(x, y, r, mat="carbone"):
    return [SPH(x, y, r * 0.95, r, mat, ecrase=0.95), C(x, y, r * 0.55, 0, 0.6, mat),
            TOR(x, y, r * 1.75, r * 0.62, r * 0.14, mat, arc=math.pi)]


# ---------------------------------------------------------------------------------------------------- scène
M = []
# --- séjour : coin cinéma. Divan en L dos à l'escalier, projecteur sur un guéridon au bout du divan, toile motorisée
#     au plafond devant le mur de droite (là où était la télé), meuble bas et barre de son dessous
def divan_L(x0, y0, x1, y1, xr, yr):
    """Divan en L : section principale x0–x1 (dossier à x0), méridienne x1–xr le long de y0–yr (dossier à y0)."""
    out = [A(x0, y0, x1, y1, 3, 15, "tissu", r=2, b=1.5), A(x1 - 1, y0, xr, yr, 3, 15, "tissu", r=2, b=1.5),        # bases
           A(x0, y0, x0 + 9, y1, 15, 31, "tissu", r=2.5, b=2), A(x0, y0, xr, y0 + 9, 15, 31, "tissu", r=2.5, b=2),     # dossiers
           A(x0 + 9, y1 - 6, x1, y1, 15, 23, "tissu", r=2, b=1.8)]                                                    # accoudoir
    ys = [y0 + 9, y0 + 9 + (y1 - 6 - y0 - 9) / 2, y1 - 6]
    out += [A(x0 + 9, a + 0.3, x1, b - 0.3, 15, 20, "tissu", r=2.5, b=2.2) for a, b in zip(ys, ys[1:])]           # coussins
    out += [A(x1 + 0.3, y0 + 9, xr, yr, 15, 20, "tissu", r=2.5, b=2.2)]
    out += [A(x0 + 9, y + 0.5, x0 + 15, y + 17, 20, 34, "tissu", r=3, b=2.5) for y in (y0 + 12, y0 + 34, y0 + 56)]  # coussins de dos
    out += [A(x0 + 3, y0 + 3, x0 + 6, y0 + 6, 0, 3, "metal", r=0.5, b=0.3), A(xr - 6, y0 + 3, xr - 3, y0 + 6, 0, 3, "metal", r=0.5, b=0.3),
            A(x0 + 3, y1 - 6, x0 + 6, y1 - 3, 0, 3, "metal", r=0.5, b=0.3), A(x1 - 6, y1 - 6, x1 - 3, y1 - 3, 0, 3, "metal", r=0.5, b=0.3)]
    return out
M += [A(296, 22, 424, 150, 0, 0.5, "tapis", r=2, b=0.2)] + divan_L(302, 40, 340, 128, 370, 76)
M += [A(344, 48, 366, 70, 20, 21.5, "jete", r=3, b=1)]                                                         # jeté sur la méridienne
M += [C(372, 98, 15, 14, 15.5, "placage", pans=48), C(372, 98, 12, 0, 14, "carbone", pans=48),                 # table basse ronde
      A(364, 92, 376, 100, 15.5, 17, "draps", r=0.4, b=0.3), C(380, 102, 3, 15.5, 19, "blanc")]
# guéridon et projecteur au bout du divan, objectif vers la toile
M += [C(318, 140, 7, 0, 1, "metal", pans=32), C(318, 140, 0.9, 1, 27, "metal"), C(318, 140, 8.5, 27, 28.5, "placage", pans=40),
      A(310.5, 133, 325, 147, 28.5, 33.5, "blanc", r=1.8, b=1), A(324.5, 136, 325.5, 144, 29.5, 32.5, "carbone", r=0.5, b=0.3),
      CX(325, 327, 137.5, 31, 1.6, "carbone", pans=32), CX(326.6, 327.2, 137.5, 31, 1.2, "ecran", pans=32),
      B(311, 133.2, 316, 133.6, 29.5, 32.5, "carbone")]
# toile motorisée : boîtier noir au plafond, toile mate blanche de 96 po (16:9), bordure noire ; meuble bas et barre de son
M += [B(438.5, 64, 443.5, 156, 91.5, 96, "carbone"), B(440.8, 68, 441.2, 152, 41, 86.5, "blanc"),
      B(440.8, 68, 441.2, 152, 86.5, 91.5, "carbone"), B(440.4, 67.5, 441.6, 152.5, 40, 41, "carbone")]
M += [A(428, 82, 446, 138, 4, 17, "placage", r=1, b=0.4), A(434, 92, 443, 128, 17, 20, "carbone", r=1, b=0.6),
      MOD("plante_sansevieria", 438, 72)]
# grand cadre photo sur le mur avant, au-dessus du dossier du divan : cadre noir, passe-partout blanc, lampe laiton
Z = 10
M += [B(288.5, 10, 325.5, 10.8, 21.5 + Z, 80.25 + Z, "blanc"),
      B(287, 10, 288.5, 11.5, 20 + Z, 81.75 + Z, "metal"), B(325.5, 10, 327, 11.5, 20 + Z, 81.75 + Z, "metal"),
      B(287, 10, 327, 11.5, 20 + Z, 21.5 + Z, "metal"), B(287, 10, 327, 11.5, 80.25 + Z, 81.75 + Z, "metal"),
      {"forme": "image", "cle": "photo_salon", "x": 307, "y": 10.85, "z0": 25.5 + Z, "z1": 76.25 + Z, "larg": 29, "face": "+y"}]
# --- escalier : rampe de métal simple côté séjour (barreaux carrés de ¾ po à 4½ po, main courante noire)
XR = 271
zl = lambda y: 0.75 * (150 - y) + 7.5                       # ligne des nez de marche le long du côté séjour
y = 148.0
while y > 16:
    z0, z1 = zl(y) - 3, min(zl(y) + 36, 95.75)
    if z1 - z0 > 2:
        M.append(B(XR - 0.375, y - 0.375, XR + 0.375, y + 0.375, z0, z1, "metal"))
    y -= 4.5
yc = 150 - (95.75 - 43.5) / 0.75                            # la main courante rejoint le plafond
M += [T([(XR, 151, 43.5), (XR, yc, 95.75)], 0.85, "metal", bouts=True),
      T([(XR, 150, 4.5), (XR, 150 - (95 - 4.5) / 0.75, 95)], 0.5, "metal", bouts=True),
      B(XR - 0.75, 16, XR + 0.75, yc, 95, 96, "metal"),
      B(XR - 1.25, 149.75, XR + 1.25, 152.25, 0, 44, "metal"), B(XR - 1.75, 149.25, XR + 1.75, 152.75, 0, 0.5, "metal")]
# rangement encastré sous les marches (derrière le divan) : trois caissons de chêne en escalier, portes côté séjour
for ya, yb, h in ((20, 48, 74), (50, 74, 54), (76, 100, 33)):
    M += [A(236, ya, 270, yb, 0, h, "placage", r=0.3, b=0.25), B(236.5, ya + 0.5, 269.5, yb - 0.5, 0, 3, "carbone")]
    ym = (ya + yb) / 2
    M += [B(270, ym - 0.15, 270.2, ym + 0.15, 3.5, h - 0.5, "carbone")]                                    # joint des portes
    M += [B(270, ym - 2.5, 270.6, ym - 1.5, h / 2 - 5, h / 2 + 5, "metal"), B(270, ym + 1.5, 270.6, ym + 2.5, h / 2 - 5, h / 2 + 5, "metal")]
# --- vestiaire près de l'entrée : banc, cases à souliers, crochets, tablette ; armoire à manteaux fermée
M += [B(334, 210, 402, 227.75, 0, 3, "metal"), A(334, 209.75, 402, 227.75, 15.5, 17.5, "placage", r=0.3, b=0.3),
      A(334, 211, 402, 227.75, 66, 67.5, "placage", r=0.3, b=0.3), A(334, 209.75, 402, 227.75, 70, 88, "laque-vert", r=0.3, b=0.3),
      B(334, 214, 402, 214.5, 65.5, 66, "spot"), A(336, 212, 400, 227, 17.5, 19.5, "tissu", r=1, b=0.8)]
M += [A(x - 0.4, 209.75, x + 0.4, 227.75, 0, 70, "placage", r=0.2, b=0.15) for x in (334.4, 357, 379.5, 401.6)]
M += [T([(x, 227.6, 58), (x, 225, 59)], 0.35, "laiton", bouts=True) for x in (341, 350, 363, 372, 386, 395)]
M += [A(337, 220, 352, 226, 27, 58, "jete", r=2, b=1.5), A(359, 219.5, 375, 226, 30, 58, "cuir", r=2, b=1.5),
      A(383, 220, 397, 226, 34, 58, "tissu", r=2, b=1.5)]                                     # manteaux accrochés
M += [A(337 + 11 * k, 212, 346 + 11 * k, 224, 3, 7, "cuir" if k % 2 else "carbone", r=2, b=1) for k in range(6)]  # souliers
M += [A(404, 203.75, 444, 227.75, 0, 88, "laque-vert", r=0.3, b=0.3), B(423.6, 203.4, 424.4, 203.75, 0.5, 87.5, "carbone"),
      T([(422, 203.2, 34), (422, 203.2, 54)], 0.35, "laiton"), T([(426, 203.2, 34), (426, 203.2, 54)], 0.35, "laiton")]
# --- hall : tapis de passage
M += [A(158, 166, 214, 202, 0, 0.5, "tapis", r=2, b=0.2)]
# --- salle d'entraînement : tapis roulant, vélo de route sur base d'entraînement, petits poids au sol, miroir
M += [B(118, 10.2, 224, 10.8, 6, 84, "miroir")]
M += [MOD("tapis_roulant", 186, 37, face="+x")]
M += [A(116, 84, 206, 120, 0, 0.35, "caoutchouc-noir", r=2, b=0.15), MOD("velo_route_base", 160, 101, face="+x")]
M += [A(118, 60, 214, 80, 0, 0.35, "caoutchouc-noir", r=2, b=0.15)]
M += [MOD("haltere_a", 128, 65), MOD("haltere_a", 128, 71), MOD("haltere_b", 142, 65), MOD("haltere_b", 142, 71),
      MOD("haltere_c", 157, 65), MOD("haltere_c", 157, 71), ] + kettlebell(178, 70, 3.6) + kettlebell(192, 70, 4.2)
# --- salle de lavage : laveuse neuve à chargement par le dessus et sécheuse (rien au-dessus), bac dégagé, comptoir de
#     pliage avec rangement le long du mur du gym, tablettes ouvertes, séchoir suspendu
M += [A(12, 10.5, 39, 37, 0, 36, "blanc", r=1.5, b=0.6), A(13.5, 14.5, 37.5, 35.5, 36, 36.5, "ecran", r=3, b=0.2),   # laveuse, couvercle vitré
      A(12, 10.5, 39, 15.5, 36, 42, "blanc", r=1, b=0.5), B(20, 15.4, 31, 15.8, 38, 41, "ecran")]                 # console arrière
M += appareil(41, 68, 10.5, 36.5) + [A(41, 10.5, 68, 15.5, 36, 42, "blanc", r=1, b=0.5), B(49, 15.4, 60, 15.8, 38, 41, "ecran")]
M += [A(70, 11, 109.75, 35, 4, 34.5, "laque-marine", r=0.3, b=0.3), B(70, 13, 109.75, 35, 0, 4, "metal"),
      A(69, 10, 109.75, 36, 34.5, 36, "placage", r=0.3, b=0.3)]                                                   # retour du L (mur avant)
M += [C(78 + 10 * k, 22, 4.5, 6, 16, "osier") for k in range(3)]                                                 # paniers à linge dessous
M += [A(10, 10, 68, 22, 66, 67.5, "placage", r=0.3, b=0.3), C(20, 16, 3, 67.5, 76, "blanc"), C(28, 16, 3, 67.5, 74, "laque-marine"),
      C(48, 16, 5, 67.5, 75, "osier"), C(60, 16, 5, 67.5, 75, "osier")]                                             # tablette, produits, paniers
M += [A(85.75, 35, 109.75, 110, 4, 34.5, "laque-marine", r=0.3, b=0.3), B(85.75, 37, 109.75, 108, 0, 4, "metal"),
      A(84.75, 35, 109.75, 111, 34.5, 36, "placage", r=0.3, b=0.3),                                                # comptoir de pliage
      A(89, 71, 107, 89, 35.7, 36.1, "inox", r=2.5, b=0.1), B(90, 72, 106, 88, 26, 35.7, "inox"),                  # bac encastré
      T([(108.5, 80, 36), (108.5, 80, 50), (105.5, 80, 52.5), (101, 80, 50)], 0.45, "metal"),                        # robinet col-de-cygne
      C(108.4, 85, 0.6, 36, 39, "metal")]
M += [B(85.2, 37, 85.75, 109, z, z + 0.4, "carbone") for z in (14, 24)] + [T([(85.3, y, 30), (85.3, y + 8, 30)], 0.3, "laiton") for y in (44, 95)]
M += [A(97.75, 92, 109.75, 110, z, z + 1.5, "placage", r=0.3, b=0.3) for z in (54, 68)] + \
     [C(103, 98 + 7 * k, 3, 55.5, 63, "osier") for k in range(2)] + [A(90, 44, 104, 62, 36, 39, "draps", r=1.5, b=0.8)]
M += [CX(30, 80, y, 80, 0.5, "placage") for y in (66, 72, 78, 84)] + [B(30, 64, 31, 86, 80, 89.5, "metal"), B(79, 64, 80, 86, 80, 89.5, "metal")]
M += [MOD("chauffe_eau", 34, 138, face="+x", H=66), A(10.2, 99, 14, 119, 40, 70, "gris", r=0.5, b=0.3)]
# --- salle de bain : on entre par le hall ; vanité simple et toilette le long du mur de la salle de lavage, bain sur pied
#     sous la fenêtre, douche de 7 pi le long du mur de la chambre 1
M += [MOD("bain_autoportant", 32, 199, face="+x")]
M += [C(32, 239, 1.8, 0, 0.5, "metal"), T([(32, 239, 0.5), (32, 239, 37), (32, 238.6, 40.2), (32, 236.6, 41.4), (32, 234.2, 40.4),
                                           (32, 233.2, 38.4)], 0.55, "metal"),                               # robinet sur pied, au bout du bain
      C(32, 239, 0.9, 30, 31.5, "metal"), C(34.4, 240, 0.75, 19, 27, "metal"), C(34.4, 240, 1.1, 27, 28.5, "metal")]
M += [MOD("toilette_suspendue", 64, 166, face="+y", z=15), MOD("plaque_chasse", 64, 159.6, face="+y", z=40)]
M += [A(86, 159.25, 122, 181.25, 12, 32, "placage", r=0.5, b=0.4), A(85.5, 159.25, 122.5, 181.75, 32, 33.5, "quartz", r=0.6, b=0.4),
      MOD("vasque_carree", 104, 171.5, face="+y", z=33.5), MOD("robinet_vasque_noir", 104, 162, face="+y", z=33.5),
      CY(104, 159.3, 159.8, 59, 12, "miroir"), TOR(104, 159.6, 59, 12, 0.45, "metal"),
      MOD("distributeurs_marbre", 116, 165, z=33.5), MOD("serviettes_pliees", 91, 172, z=33.5)]
M += [B(54, 247.25, 139.75, 247.75, 0, 84, "tuile_blanche"), B(139.25, 211.75, 139.75, 247.75, 0, 84, "tuile_blanche"),
      B(54, 211.75, 139.75, 247.75, 0, 0.5, "porcelaine"), B(54.5, 211.75, 55, 247.75, 0, 84, "tuile_blanche"),
      B(80, 211.25, 139.75, 212.25, 0, 76, "verre"), B(79.3, 211, 80.7, 212.5, 0, 76, "metal"), B(80, 211, 139.75, 212.5, 75, 76, "metal"),
      MOD("colonne_douche_noire", 110, 247, face="-y", z=30), MOD("colonne_douche_noire", 70, 247, face="-y", z=30),
      B(86, 244, 100, 247.25, 44, 45, "metal")]                                                                  # niche
M += [A(60, 190, 86, 208, 0, 0.5, "tapis", r=2, b=0.2)]
def commode(x0, y0, x1, y1, face, h=32):
    """Commode de chêne à trois tiroirs, poignées noires ; face = côté des tiroirs."""
    out = [A(x0, y0, x1, y1, 3, h, "placage", r=0.4, b=0.3), B(x0 + 1, y0 + 1, x1 - 1, y1 - 1, 0, 3, "carbone")]
    for k in (1, 2):
        z = 3 + k * (h - 3) / 3
        out.append({"+y": B(x0 + 0.5, y1, x1 - 0.5, y1 + 0.2, z - 0.15, z + 0.15, "carbone"),
                    "-x": B(x0 - 0.2, y0 + 0.5, x0, y1 - 0.5, z - 0.15, z + 0.15, "carbone")}[face])
    for k in range(3):
        z = 3 + (k + 0.5) * (h - 3) / 3
        out.append({"+y": B((x0 + x1) / 2 - 5, y1, (x0 + x1) / 2 + 5, y1 + 0.6, z - 0.4, z + 0.4, "metal"),
                    "-x": B(x0 - 0.6, (y0 + y1) / 2 - 5, x0, (y0 + y1) / 2 + 5, z - 0.4, z + 0.4, "metal")}[face])
    return out


# --- chambre 1 (agrandie : reprend la moitié de l'ancien coin commun) : lit entre les deux fenêtres, bureau, commode
M += [MOD("lit_queen", 144, 325, face="-y"), MOD("table_chevet", 91, 357, face="-y"), MOD("table_chevet", 197, 357, face="-y"),
      MOD("lampe_chevet", 91, 357, z=24), MOD("lampe_chevet", 197, 357, z=24), A(96, 262, 192, 368, 0, 0.5, "tapis", r=2, b=0.2)]
M += [B(37.5, 295, 39, 355, 0, 80, "placage")]
M += [MOD("bureau", 75, 265.25, face="+y"), MOD("chaise_bureau", 75, 289, face="-y"),
      B(64, 255, 86, 256, 36, 50, "ecran", r=0.3), B(74, 256, 76, 258, 30, 36, "metal")]
M += commode(217.5, 280, 237.5, 340, "-x") + [MOD("plante_sansevieria", 228, 290, z=32), C(228, 328, 2.5, 32, 33, "laiton"),
      C(228, 328, 0.3, 33, 45, "laiton"), C(228, 328, 4.5, 42, 47, "abat-jour", r2=3.5),
      CX(236.6, 237.4, 310, 58, 14.6, "metal", pans=48), CX(236.2, 236.8, 310, 58, 14, "miroir", pans=48)]
# --- chambre 2 (agrandie jusqu'au mur des chambres ; sa garde-robe est le walk-in du caveau)
M += [MOD("lit_queen", 352, 325, face="-y"), MOD("table_chevet", 299, 357, face="-y"), MOD("table_chevet", 405, 357, face="-y"),
      MOD("lampe_chevet", 299, 357, z=24), MOD("lampe_chevet", 405, 357, z=24), A(304, 262, 400, 368, 0, 0.5, "tapis", r=2, b=0.2),
      MOD("cadre_monstera_1", 242.4, 292, face="+x", z=48), MOD("cadre_monstera_2", 242.4, 312, face="+x", z=48),
      MOD("plante_sansevieria", 436, 250)]
M += commode(300, 232.25, 360, 252.25, "+y") + [C(312, 242, 4, 32, 40, "blanc", r2=3), A(336, 236, 352, 248, 32, 33.5, "draps", r=0.3, b=0.2)]
M += [A(420, 282, 445, 330, 28.5, 30, "placage", r=0.5, b=0.4)] + [T([(422, y, 0), (422, y, 28.5)], 0.6, "metal") for y in (284, 328)] + \
     [T([(443, y, 0), (443, y, 28.5)], 0.6, "metal") for y in (284, 328)]
M += [MOD("chaise_bureau", 409, 306, face="+x"), B(442, 296, 443, 316, 36, 49, "ecran", r=0.3), B(440, 305, 442, 307, 30, 36, "metal")]
# --- walk-in (ancien caveau, isolé et chauffé) : tringle et tablette au fond, tablettes de côté, souliers
M += [CX(231, 315, 419, 66, 0.6, "metal"), A(229, 412, 317, 430, 70, 71.5, "placage", r=0.3, b=0.3),
      A(229, 380, 243, 410, 0, 84, "placage", r=0.3, b=0.3, trou=0.75), A(303, 380, 317, 410, 0, 84, "placage", r=0.3, b=0.3, trou=0.75)]
M += [A(229.75, 380.5, 242.25, 409.5, z, z + 0.75, "placage", r=0.2, b=0.15) for z in (14, 30, 46, 62)]
M += [A(303.75, 380.5, 316.25, 409.5, z, z + 0.75, "placage", r=0.2, b=0.15) for z in (14, 30, 46, 62)]
TONS_V = ["jete", "carbone", "draps", "laque-marine", "tissu", "cuir", "laque-vert", "draps"]
x = 233.0
k = 0
while x < 312:
    ep = 2.2 + (k * 7 % 5) * 0.5
    M.append(A(x, 411, x + ep, 427, 30 + (k * 11 % 4) * 4, 65, TONS_V[k % len(TONS_V)], r=0.6, b=0.4))
    x += ep + 0.4
    k += 1
M += [A(232 + 12 * k, 414, 241 + 12 * k, 428, 71.5, 77, "osier" if k % 2 else "draps", r=1, b=0.6) for k in range(7)]
M += [A(231 + 7 * k, 382, 237 + 7 * k, 392, 0.5, 4.5, "cuir" if k % 2 else "carbone", r=1.5, b=0.8) for k in range(2)]
M += [A(230.5, 382, 241.5, 408, z + 0.75, z + 5, TONS_V[(z // 16) % len(TONS_V)], r=0.5, b=0.4) for z in (14, 30, 46)]
M += [A(304.5, 382, 315.5, 408, z + 0.75, z + 5, TONS_V[(z // 16 + 3) % len(TONS_V)], r=0.5, b=0.4) for z in (14, 30, 46)]

SCENE = {
    "niveau": "SS",
    "titre": TITRE,
    "plafond": 96,               # 8 pi, donné par le propriétaire (2026-10-29)
    "hauteur_etage": 105,        # plancher à plancher DÉDUIT : 8 pi + ~9 po de plancher (solives, sous-plancher, fini) ; 14 × 7½ po
    "allege_fenetre": 56, "tete_fenetre": 86,
    "sol_defaut": "chene",
    "sols": {"piece-SS-LAVAGE": "terrazzo", "piece-SS-GYM": "caoutchouc", "piece-SS-SDB": "porcelaine",
             "piece-SS-PERRON": "beton"},
    "mat_colonne": "placage",
    "peintures": {  # nom : [couleur à l'écran, description, alias pour le mobilier]
        "Blanc chaud": ["#F1EEE8", "murs et plafonds partout ailleurs (≈ Benjamin Moore White Dove OC-17)"],
        "Vert forêt": ["#34473B", "mur et armoires du vestiaire (≈ Benjamin Moore Tarrytown Green HC-134)", "laque-vert"],
        "Bleu-gris": ["#8FA1A8", "murs de la salle de lavage (≈ Benjamin Moore Boothbay Gray HC-165)"],
        "Marine": ["#2E3B4E", "armoires de la salle de lavage (≈ Benjamin Moore Hale Navy HC-154)", "laque-marine"],
        "Anthracite": ["#3E4042", "murs pleins de la salle d'entraînement (≈ Benjamin Moore Wrought Iron 2124-10)"],
        "Sauge": ["#A6AF9A", "chambre 2 (≈ Benjamin Moore October Mist 1495)"],
        "Argile": ["#C39A82", "mur de tête de lit de la chambre 1 (terracotta adouci, à choisir sur nuancier)"],
        "Greige": ["#D9D2C8", "murs de la salle de bain hors céramique"],
    },
    "peinture": {"piece-SS-LAVAGE": "Bleu-gris", "piece-SS-GYM": "Anthracite", "piece-SS-CH2": "Sauge",
                 "piece-SS-GR2": "Sauge", "piece-SS-SDB": "Greige"},
    "accents": [{"piece": "piece-SS-VEST", "mur": "mur-SS-P11", "peinture": "Vert forêt"},
                {"piece": "piece-SS-CH1", "mur": "mur-SS-003", "peinture": "Argile"}],
    "images": {"photo_salon": "../prive/photo_salon.jpg"},    # photo personnelle : hors du dépôt (renovation/prive/)
    "mobilier": M,
    "revetements": [],
    "lumieres": [{"x": 300, "y": 80}, {"x": 404, "y": 90}, {"x": 368, "y": 196}, {"x": 424, "y": 190}, {"x": 400, "y": 126}, {"x": 190, "y": 182},
                 {"x": 198, "y": 214}, {"x": 170, "y": 50}, {"x": 160, "y": 120}, {"x": 50, "y": 60}, {"x": 60, "y": 120},
                 {"x": 50, "y": 200}, {"x": 110, "y": 215}, {"x": 100, "y": 310}, {"x": 360, "y": 300}, {"x": 190, "y": 300}, {"x": 330, "y": 80},
                 {"x": 273, "y": 408}, {"x": 252, "y": 60, "z": 185, "i": 7}],
    "visites": [{"nom": "Entrée", "x": 430, "y": 178, "cap": 168},
                {"nom": "Vestiaire", "x": 350, "y": 172, "cap": 50},
                {"nom": "Escalier", "x": 252, "y": 196, "cap": 270},
                {"nom": "Séjour", "x": 424, "y": 146, "cap": 200},
                {"nom": "Coin cinéma (toile)", "x": 286, "y": 112, "cap": 352},
                {"nom": "Rangement sous l'escalier", "x": 336, "y": 146, "cap": 215},
                {"nom": "Gym (porte vitrée)", "x": 168, "y": 192, "cap": 270},
                {"nom": "Vélo et tapis roulant", "x": 126, "y": 146, "cap": 320},
                {"nom": "Salle de lavage", "x": 70, "y": 128, "cap": 262},
                {"nom": "Salle de bain", "x": 133, "y": 192, "cap": 180},
                {"nom": "Bain sur pied", "x": 100, "y": 196, "cap": 175},
                {"nom": "Douche", "x": 96, "y": 194, "cap": 90},
                {"nom": "Vanité", "x": 104, "y": 207, "cap": 270},
                {"nom": "Chambre 1", "x": 222, "y": 246, "cap": 132},
                {"nom": "Chambre 2", "x": 262, "y": 250, "cap": 40},
                {"nom": "Walk-in (caveau)", "x": 270, "y": 330, "cap": 100},
                {"nom": "Escalier vu du séjour", "x": 330, "y": 112, "cap": 185}],
    "depart": {"x": 430, "y": 178, "cap": 168},
    "palette": [["Plancher", "chêne pâle, lames larges (vinyle de luxe) ; escalier en chêne massif, contremarches blanches", "#C9A97E"],
                                ["Vestiaire", "banc et cases en chêne, crochets laiton, armoire à manteaux et armoires du haut vert forêt", "#34473B"],
                ["Escalier flottant", "limon central en acier noir, marches de chêne de 2 po ; verre côté gym, rampe à barreaux d'acier noir côté séjour ; rangement de chêne dessous", "#1E1E1E"],
                ["Chambres", "chambre 1 : lit entre les deux fenêtres, bureau, commode de chêne ; chambre 2 (sauge) : bureau sous la fenêtre, walk-in dans l'ancien caveau", "#A6AF9A"],
                ["Salle de bain", "porcelaine pâle, bain autoportant, robinet sur pied noir mat, douche de 7 pi vitrée à deux pommes, vanité de chêne suspendue", "#D9D6D0"],
                ["Gym", "dalles de caoutchouc noir, murs anthracite, miroir, tapis roulant, vélo de route sur base d'entraînement", "#2A2A2A"],
                ["Salle de lavage", "terrazzo pâle, laveuse à chargement par le dessus, comptoir de pliage en L en chêne avec bac inox encastré, armoires marine, séchoir suspendu", "#2E3B4E"],
                ["Séjour", "divan en L en tissu gris chaud, projecteur sur guéridon, toile motorisée de 96 po au plafond, table basse ronde en chêne, tapis de laine crème", "#9A5B32"],
                ["Accents", "noir mat : cadres vitrés, robinetterie, luminaires ; laiton au bar", "#1E1E1E"]],
}
