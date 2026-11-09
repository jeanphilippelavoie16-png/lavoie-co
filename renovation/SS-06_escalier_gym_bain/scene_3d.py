"""Maquette 3D de SS-06 : nouvel escalier, sous-sol repensé, bain sur pied, gym (tapis roulant, vélo de route sur base
d'entraînement, poids au sol). Matériaux réels (catalogue_materiaux.py) et modèles 3D (catalogue_modeles.py).

Coordonnées en pouces, repère de la maison. Le mobilier sert à juger les volumes et l'ambiance ; ce n'est pas un choix
de produit.
"""
import math

TITRE = "SS-06 — Nouvel escalier, bain sur pied, gym"


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
    out += [B(x0, y0, x1, y1, z, z + 1, "placage") for z in (4, 22, 40, 58, 76)]
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
    """Tapis roulant de maison (30 × 68 po), console vers −y (vers le miroir)."""
    x1, y1 = x0 + 30, y0 + 68
    return [A(x0, y0 + 10, x1, y1, 1.5, 7.5, "carbone", r=2, b=0.8),                     # plateau
            B(x0 + 4, y0 + 12, x1 - 4, y1 - 1, 7.5, 7.9, "caoutchouc-noir"),               # bande
            A(x0, y0 + 14, x0 + 3.5, y1 - 2, 6.5, 8.6, "gris", r=1, b=0.5), A(x1 - 3.5, y0 + 14, x1, y1 - 2, 6.5, 8.6, "gris", r=1, b=0.5),
            A(x0 + 1, y0, x1 - 1, y0 + 14, 1.5, 11, "carbone", r=4, b=1.5),               # capot du moteur
            T([(x0 + 2, y0 + 8, 10), (x0 + 1.5, y0 + 4, 46)], 1.1, "carbone"), T([(x1 - 2, y0 + 8, 10), (x1 - 1.5, y0 + 4, 46)], 1.1, "carbone"),
            A(x0 - 0.5, y0 - 1, x1 + 0.5, y0 + 9, 44, 50, "carbone", r=3, b=1.2),        # console
            B(x0 + 7, y0 + 5.6, x1 - 7, y0 + 6.2, 46, 49.5, "ecran"),
            T([(x0 + 0.5, y0 + 6, 46.5), (x0 + 0.5, y0 + 18, 41)], 0.75, "pneu", bouts=True),
            T([(x1 - 0.5, y0 + 6, 46.5), (x1 - 0.5, y0 + 18, 41)], 0.75, "pneu", bouts=True)]


def haltere(x, y, r, l=12):
    """Haltère hexagonal couché le long de x."""
    return [CX(x - l / 2 + 2.6, x + l / 2 - 2.6, y, r, 0.6, "inox"),
            CX(x - l / 2, x - l / 2 + 2.6, y, r, r, "caoutchouc-noir", pans=6), CX(x + l / 2 - 2.6, x + l / 2, y, r, r, "caoutchouc-noir", pans=6)]


def kettlebell(x, y, r, mat="carbone"):
    return [SPH(x, y, r * 0.95, r, mat, ecrase=0.95), C(x, y, r * 0.55, 0, 0.6, mat),
            TOR(x, y, r * 1.75, r * 0.62, r * 0.14, mat, arc=math.pi)]


# ---------------------------------------------------------------------------------------------------- scène
M = []
# --- séjour : mur de lattes de chêne, télé, sofa en L, coin lecture
M += [B(234 + 3 * i, 10, 236 + 3 * i, 11.6, 0, 89, "placage") for i in range(33)]
M += [A(250, 11.6, 322, 27, 4, 18, "placage", r=1, b=0.4), B(258, 11.7, 314, 13, 30, 62, "ecran", r=0.4)]
M += [A(238, 40, 350, 132, 0, 0.5, "tapis", r=2, b=0.2)]
M += sofa(244, 98, 340, 136, "+y") + sofa(340, 66, 378, 136, "+x")
M += [A(268, 56, 318, 84, 13, 15, "placage", r=4, b=0.6), C(271, 59, 0.8, 0, 13, "metal"), C(315, 59, 0.8, 0, 13, "metal"),
      C(271, 81, 0.8, 0, 13, "metal"), C(315, 81, 0.8, 0, 13, "metal")]
M += fauteuil(422, 52, "-y") + fauteuil(422, 124, "+y")
M += [C(422, 88, 10, 20, 22, "placage"), C(422, 88, 1.5, 0, 20, "laiton"), C(422, 88, 6, 0, 0.6, "laiton"),
      C(440, 88, 0.6, 0, 60, "metal"), C(440, 88, 5, 0, 0.8, "metal"), C(440, 88, 7, 54, 64, "abat-jour", r2=5)]
M += [C(436, 20, 6, 0, 13, "osier", r2=7.5), SPH(436, 20, 26, 11, "plante", ecrase=1.3)]
# --- coin bar : armoires vert forêt, quartz veiné, zellige vert, tablettes de chêne éclairées, frigo pleine hauteur
M += [B(332, 207, 414, 227.75, 0, 4, "metal"), A(332, 205.75, 414, 227.75, 4, 34.5, "laque-vert", r=0.4, b=0.3),
      A(331.5, 205, 414, 227.75, 34.5, 36, "quartz", r=0.5, b=0.4),
      A(355, 210, 369, 222, 35.7, 36.1, "inox", r=2, b=0.1),
      T([(362, 225, 36), (362, 225, 46.5), (362, 222, 47.5), (362, 218.5, 45)], 0.45, "laiton"),
      B(331.5, 227.2, 414, 227.75, 36, 86, "zellige-vert"),
      A(334, 218, 412, 227.2, 52, 53.5, "placage", r=0.3, b=0.3), A(334, 218, 412, 227.2, 68, 69.5, "placage", r=0.3, b=0.3),
      B(334, 218.5, 412, 219, 51.5, 52, "spot"), B(334, 218.5, 412, 219, 67.5, 68, "spot")]
M += [C(338 + 4 * i, 223, 1.5, 53.5, 63, "verre-bouteille") for i in range(6)] + [C(338 + 4 * i, 223, 0.6, 63, 66, "verre-bouteille") for i in range(6)]
M += [C(372 + 4 * i, 223, 1.6, 69.5, 74, "verre-clair") for i in range(9)] + [C(380 + 4 * i, 223, 1.6, 53.5, 58, "verre-clair") for i in range(7)]
M += [A(414.5, 200, 444.5, 229, 0, 72, "inox", r=0.8, b=0.4), A(414.5, 205, 444.5, 229, 72, 86, "laque-vert", r=0.4, b=0.3),
      T([(441, 199.6, 38), (441, 199.6, 66)], 0.45, "metal")]
# --- hall : tapis de passage
M += [A(158, 166, 214, 202, 0, 0.5, "tapis", r=2, b=0.2)]
# --- passage du caveau : banc et crochets
M += [A(262, 282, 275.5, 330, 0, 17, "placage", r=1, b=0.5)] + [T([(275.6, y, 62), (273.5, y, 63)], 0.35, "laiton") for y in (288, 298, 308, 318)]
# --- salle d'entraînement : tapis roulant, vélo de route sur base d'entraînement, petits poids au sol, miroir
M += [B(118, 10.2, 224, 10.8, 6, 84, "miroir")]
M += tapis_roulant(190, 18)
M += [A(116, 86, 200, 122, 0, 0.35, "caoutchouc-noir", r=2, b=0.15)] + velo_route(136, 104)
M += [A(120, 16, 176, 56, 0, 0.35, "caoutchouc-noir", r=2, b=0.15)]
M += haltere(132, 24, 1.9) + haltere(132, 30, 1.9) + haltere(148, 24, 2.3) + haltere(148, 30, 2.3) + haltere(164, 24, 2.7) + haltere(164, 30, 2.7)
M += kettlebell(128, 46, 3.6) + kettlebell(142, 46, 4.2) + kettlebell(158, 46, 4.6)
M += [CX(150, 170, 64, 3, 3, "jete")]
# --- salle de lavage : laveuse et sécheuse frontales sous un comptoir de pliage en chêne de 8 pi, bac, armoires marine
M += appareil(12, 39, 10.5, 36.5) + appareil(41, 68, 10.5, 36.5)
M += [A(10, 10, 109.75, 37.5, 37, 38.5, "placage", r=0.3, b=0.3),
      A(70, 11, 102, 35, 4, 37, "laque-marine", r=0.3, b=0.3), B(70, 13, 102, 35, 0, 4, "metal"),
      A(76, 14, 96, 32, 38.3, 38.7, "inox", r=2, b=0.1), T([(86, 12, 38.5), (86, 12, 51), (86, 15, 52), (86, 20, 50)], 0.45, "metal"),
      A(10, 10, 70, 23, 54, 86, "laque-marine", r=0.3, b=0.3), B(70, 10, 109.75, 20, 58, 59.5, "placage"), B(70, 10, 109.75, 20, 72, 73.5, "placage")]
M += [C(80, 15, 4.5, 59.5, 68, "osier"), C(92, 15, 4.5, 59.5, 68, "osier"), C(101, 15, 4.5, 73.5, 80, "osier")]
M += [A(85.75, 44, 109.75, 112, 0, 86, "laque-marine", r=0.3, b=0.3)] + [T([(85.3, y, 32), (85.3, y, 52)], 0.3, "laiton") for y in (76, 80)]
M += [C(28, 24, 7, 38.5, 48, "osier", r2=8), A(44, 16, 64, 32, 38.5, 42, "draps", r=1.5, b=0.8)]
M += [CX(30, 80, y, 80, 0.5, "placage") for y in (66, 72, 78, 84)] + [B(30, 64, 31, 86, 80, 89.5, "metal"), B(79, 64, 80, 86, 80, 89.5, "metal")]
M += [C(34, 138, 11, 0, 58, "blanc"), A(10.2, 99, 14, 119, 40, 70, "gris", r=0.5, b=0.3)]
# --- salle de bain : bain autoportant sous la fenêtre, robinet sur pied noir, douche vitrée, toilette, double vanité
M += [A(16, 166, 48, 232, 0, 3, "blanc", r=14, b=1), A(16, 166, 48, 232, 0, 22, "blanc", r=14, b=1, trou=1.8),
      A(18.2, 168.2, 45.8, 229.8, 14.8, 15, "eau", r=12, b=0)]
M += [C(54, 199, 1.8, 0, 0.5, "metal"), T([(54, 199, 0.5), (54, 199, 37), (53.6, 199, 40.2), (51.6, 199, 41.4), (49.2, 199, 40.4),
                                           (48.2, 199, 38.4)], 0.55, "metal"),
      C(54, 199, 0.9, 30, 31.5, "metal"), T([(54, 199, 31), (56.5, 199, 31.5)], 0.25, "metal"),
      C(55.6, 201.2, 0.75, 19, 27, "metal"), C(55.6, 201.2, 1.1, 27, 28.5, "metal")]
M += [A(50, 188, 78, 210, 0, 0.5, "tapis", r=2, b=0.2)]
M += [B(80, 159.3, 139.75, 159.8, 0, 84, "tuile_blanche"), B(139.25, 159.25, 139.75, 195, 0, 84, "tuile_blanche"),
      B(80, 159.25, 139.75, 195, 0, 0.5, "porcelaine"),
      B(79.5, 159.5, 80.5, 195, 0, 76, "verre"), B(79.3, 159.5, 80.7, 195.5, 75, 76, "metal"),
      B(80, 194.5, 110, 195.5, 0, 76, "verre"), B(109, 194.2, 110, 195.8, 0, 76, "metal"),
      C(110, 168, 5, 77, 77.5, "metal"), T([(110, 159.8, 78), (110, 168, 78)], 0.4, "metal"),
      B(112, 159.8, 124, 163.5, 44, 45, "metal")]
M += [A(54, 240.5, 72, 247.6, 15, 29, "blanc", r=2, b=0.8), A(55.5, 222, 70.5, 242, 0, 15, "blanc", r=7, b=1.2),
      A(55.3, 221.6, 70.7, 242, 15, 16, "blanc", r=7, b=0.5), B(62, 247, 64, 247.6, 31, 33, "metal")]
M += [A(79, 226, 139, 247.75, 12, 32, "placage", r=0.5, b=0.4), A(78.5, 225.5, 139.5, 247.75, 32, 33.5, "quartz", r=0.6, b=0.4)]
for xs in (94, 124):
    M += [A(xs - 7.5, 229, xs + 7.5, 244, 33.5, 34.5, "blanc", r=7, b=0.4), A(xs - 7.5, 229, xs + 7.5, 244, 33.5, 38.5, "blanc", r=7, b=0.6, trou=0.7),
          T([(xs, 247.6, 45), (xs, 242, 45), (xs, 241, 44)], 0.45, "metal"),
          CY(xs, 247.2, 247.7, 59, 11, "miroir"), TOR(xs, 247.5, 59, 11, 0.45, "metal")]
# --- chambre 1 (réduite par l'escalier)
M += lit(78, 288, 138, 366) + table_chevet(64, 356) + table_chevet(152, 356) + [A(62, 270, 154, 368, 0, 0.5, "tapis", r=2, b=0.2)]
M += [B(37.5, 295, 39, 355, 0, 80, "placage")]
# --- chambre 2 (agrandie)
M += lit(333, 288, 393, 366) + table_chevet(319, 356) + table_chevet(407, 356) + [A(317, 270, 409, 368, 0, 0.5, "tapis", r=2, b=0.2)]
M += [B(391, 257.5, 439, 259, 0, 80, "placage")]
M += [A(420, 282, 445, 330, 28.5, 30, "placage", r=0.5, b=0.4)] + [T([(422, y, 0), (422, y, 28.5)], 0.6, "metal") for y in (284, 328)] + \
     [T([(443, y, 0), (443, y, 28.5)], 0.6, "metal") for y in (284, 328)]
# --- rangement (ancien caveau)
M += etagere(230, 384, 246, 430) + etagere(300, 384, 316, 430) + etagere(250, 414, 296, 430)

SCENE = {
    "niveau": "SS",
    "titre": TITRE,
    "plafond": 90,
    "hauteur_etage": 105,        # plancher à plancher PRÉSUMÉ (non mesuré) : 14 contremarches de 7½ po
    "allege_fenetre": 56, "tete_fenetre": 86,
    "sol_defaut": "chene",
    "sols": {"piece-SS-LAVAGE": "terrazzo", "piece-SS-GYM": "caoutchouc", "piece-SS-SDB": "porcelaine",
             "piece-SS-LEG": "beton", "piece-SS-PERRON": "beton"},
    "mat_colonne": "placage",
    "peintures": {  # nom : [couleur à l'écran, description, alias pour le mobilier]
        "Blanc chaud": ["#F1EEE8", "murs et plafonds partout ailleurs (≈ Benjamin Moore White Dove OC-17)"],
        "Vert forêt": ["#34473B", "mur et armoires du coin bar (≈ Benjamin Moore Tarrytown Green HC-134)", "laque-vert"],
        "Bleu-gris": ["#8FA1A8", "murs de la salle de lavage (≈ Benjamin Moore Boothbay Gray HC-165)"],
        "Marine": ["#2E3B4E", "armoires de la salle de lavage (≈ Benjamin Moore Hale Navy HC-154)", "laque-marine"],
        "Anthracite": ["#3E4042", "murs pleins de la salle d'entraînement (≈ Benjamin Moore Wrought Iron 2124-10)"],
        "Sauge": ["#A6AF9A", "chambre 2 (≈ Benjamin Moore October Mist 1495)"],
        "Argile": ["#C39A82", "mur de tête de lit de la chambre 1 (terracotta adouci, à choisir sur nuancier)"],
        "Greige": ["#D9D2C8", "murs de la salle de bain hors céramique"],
    },
    "peinture": {"piece-SS-LAVAGE": "Bleu-gris", "piece-SS-GYM": "Anthracite", "piece-SS-CH2": "Sauge",
                 "piece-SS-GR2": "Sauge", "piece-SS-SDB": "Greige"},
    "accents": [{"piece": "piece-SS-BAR", "mur": "mur-SS-P11", "peinture": "Vert forêt"},
                {"piece": "piece-SS-CH1", "mur": "mur-SS-003", "peinture": "Argile"}],
    "mobilier": M,
    "revetements": [],
    "lumieres": [{"x": 300, "y": 80}, {"x": 404, "y": 90}, {"x": 350, "y": 186}, {"x": 404, "y": 186}, {"x": 190, "y": 182},
                 {"x": 198, "y": 214}, {"x": 170, "y": 50}, {"x": 160, "y": 120}, {"x": 50, "y": 60}, {"x": 60, "y": 120},
                 {"x": 50, "y": 200}, {"x": 110, "y": 215}, {"x": 100, "y": 310}, {"x": 360, "y": 300}, {"x": 248, "y": 300},
                 {"x": 273, "y": 408}, {"x": 200, "y": 300, "z": 185, "i": 7}],
    "visites": [{"nom": "Entrée", "x": 430, "y": 178, "cap": 168},
                {"nom": "Coin bar", "x": 372, "y": 164, "cap": 72},
                {"nom": "Escalier", "x": 198, "y": 180, "cap": 90},
                {"nom": "Séjour", "x": 300, "y": 150, "cap": 270},
                {"nom": "Gym (porte vitrée)", "x": 168, "y": 192, "cap": 270},
                {"nom": "Vélo et tapis roulant", "x": 128, "y": 146, "cap": 315},
                {"nom": "Salle de lavage", "x": 70, "y": 128, "cap": 262},
                {"nom": "Salle de bain", "x": 128, "y": 214, "cap": 185},
                {"nom": "Bain sur pied", "x": 100, "y": 205, "cap": 170},
                {"nom": "Double vanité", "x": 110, "y": 203, "cap": 90},
                {"nom": "Chambre 1", "x": 160, "y": 262, "cap": 140},
                {"nom": "Chambre 2", "x": 300, "y": 248, "cap": 35},
                {"nom": "Passage et caveau", "x": 248, "y": 240, "cap": 90}],
    "depart": {"x": 430, "y": 178, "cap": 168},
    "palette": [["Plancher", "chêne pâle, lames larges (vinyle de luxe) ; escalier en chêne massif, contremarches blanches", "#C9A97E"],
                ["Claustra de l'escalier", "lattes de chêne 1×2 du plancher au plafond : garde et lumière", "#B98E5E"],
                ["Coin bar", "armoires vert forêt, quartz blanc veiné, zellige vert lustré, tablettes de chêne éclairées, robinet laiton", "#34473B"],
                ["Salle de bain", "porcelaine pâle, bain autoportant, robinet sur pied noir mat, douche vitrée, vasques sur vanité de chêne", "#D9D6D0"],
                ["Gym", "dalles de caoutchouc noir, murs anthracite, miroir, tapis roulant, vélo de route sur base d'entraînement", "#2A2A2A"],
                ["Salle de lavage", "terrazzo pâle, comptoir de pliage en chêne, armoires marine, bac inox, séchoir suspendu", "#2E3B4E"],
                ["Séjour", "sofa en tissu gris chaud, fauteuils en cuir cognac, tapis de laine crème", "#9A5B32"],
                ["Accents", "noir mat : cadres vitrés, robinetterie, luminaires ; laiton au bar", "#1E1E1E"]],
}
