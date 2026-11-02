"""Maquette 3D de RDC-01 : le rez-de-chaussée TEL QU'IL EST aujourd'hui, d'après les 15 photos du propriétaire
(2026-11-01, renovation/prive/rdc_actuel/, hors du dépôt). Ce n'est pas une proposition.

Positions et dimensions estimées sur les photos (grand-angle) et le plan de base ; hauteur de plafond PRÉSUMÉE (8 pi).
Les cadres et tableaux sont génériques : aucune photo de famille ni œuvre du client n'est reproduite.
La chambre avant n'a pas été photographiée : mobilier présumé, sobre.
Coordonnées en pouces, repère de la maison (x le long de la façade, y vers l'arrière, z vers le haut).
"""

TITRE = "RDC-01 — Rez-de-chaussée actuel"


def B(x0, y0, x1, y1, z0, z1, mat, r=None):
    o = {"forme": "boite", "x0": x0, "y0": y0, "x1": x1, "y1": y1, "z0": z0, "z1": z1, "mat": mat}
    if r:
        o["r"] = r
    return o


def A(x0, y0, x1, y1, z0, z1, mat, r=3, b=0.5, trou=None):
    """Bloc à coins arrondis en plan et arêtes adoucies."""
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


def TOR(x, y, z, R, r, mat, **k):
    return dict({"forme": "tore", "x": x, "y": y, "z": z, "R": R, "r": r, "mat": mat}, **k)


def MOD(cle, x, y, rot=0, z=0, **k):
    return dict({"forme": "modele", "cle": cle, "x": x, "y": y, "z": z, "rot": rot}, **k)


NOIR = "noir-mat"          # armoires peintes noir mat (alias de la peinture « Noir mat »)
CUIR = "carbone"           # coques de cuir noir des tabourets et des chaises


def cadre_mur_x(xm, y0, y1, z0, z1, toile, sens=1, cadre="metal", ep=1.2, bord=1.2):
    """Cadre générique accroché à un mur parallèle à y (face en xm, saillie vers sens = +1 ou -1)."""
    xa, xb = sorted([xm, xm + sens * ep])
    xc, xd = sorted([xm + sens * ep, xm + sens * (ep + 0.2)])
    return [B(xa, y0, xb, y1, z0, z1, cadre), B(xc, y0 + bord, xd, y1 - bord, z0 + bord, z1 - bord, toile)]


def tabouret(x, y):
    """Tabouret de comptoir : coque de cuir noir, quatre pattes d'acier fines, repose-pieds ; regarde vers +x."""
    out = [A(x - 8, y - 8, x + 8, y + 8, 24, 26.5, CUIR, r=4, b=1), A(x - 9.5, y - 8.5, x - 7, y + 8.5, 26, 38, CUIR, r=2, b=1)]
    for dx, dy in ((-6, -6), (-6, 6), (6, -6), (6, 6)):
        out.append(T([(x + dx * 1.15, y + dy * 1.15, 0), (x + dx * 0.8, y + dy * 0.8, 24)], 0.35, "metal"))
    out += [T([(x - 6.5, y - 6.5, 9), (x + 6.5, y - 6.5, 9)], 0.3, "metal"), T([(x - 6.5, y + 6.5, 9), (x + 6.5, y + 6.5, 9)], 0.3, "metal"),
            T([(x + 6.5, y - 6.5, 9), (x + 6.5, y + 6.5, 9)], 0.3, "metal")]
    return out


def chaise(x, y, face):
    """Chaise de salle à manger : coque noire, dossier enveloppant, quatre pattes noires inclinées."""
    out = [A(x - 9, y - 9, x + 9, y + 9, 16.5, 18.5, CUIR, r=4, b=1)]
    d = {"+x": (-1, 0), "-x": (1, 0), "+y": (0, -1), "-y": (0, 1)}[face]          # côté du dossier
    if d[0]:
        xb = x + d[0] * 8.5
        out.append(A(min(xb, xb + d[0] * 2.2), y - 9, max(xb, xb + d[0] * 2.2), y + 9, 18, 33, CUIR, r=1.5, b=0.8))
    else:
        yb = y + d[1] * 8.5
        out.append(A(x - 9, min(yb, yb + d[1] * 2.2), x + 9, max(yb, yb + d[1] * 2.2), 18, 33, CUIR, r=1.5, b=0.8))
    for dx, dy in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
        out.append(T([(x + dx * 8.5, y + dy * 8.5, 0), (x + dx * 6, y + dy * 6, 16.5)], 0.45, "metal"))
    return out


def appareil(x0, x1, y_dos, y_face, z0):
    """Laveuse ou sécheuse frontale blanche (devant vers +y), hublot chromé."""
    xc = (x0 + x1) / 2
    return [A(x0, y_dos, x1, y_face, z0, z0 + 36, "blanc", r=1.5, b=0.6), CY(xc, y_face, y_face + 0.5, z0 + 17, 8.5, "inox"),
            CY(xc, y_face + 0.3, y_face + 0.9, z0 + 17, 7, "ecran"), B(x0 + 1, y_face - 0.2, x1 - 1, y_face + 0.2, z0 + 30, z0 + 34.5, "gris"),
            C(x0 + 7, y_face + 0.4, 1.6, z0 + 31, z0 + 33.5, "inox", axe="y", y0=y_face, y1=y_face + 0.8, z=z0 + 32.2)]


M = []
R = []      # revêtements (brique, papier peint, crépi, bandes d'ardoise)

# =============================================================================================== cuisine
# brique rouge à joints pâles : mur arrière (du poteau au coin) et mur de droite (photos 01, 02, 07, 08)
YB = 369.45
R += [B(266, YB, 276.5, 370, 0, 96, "brique_rouge"), B(276.5, YB, 313.5, 370, 82.5, 96, "brique_rouge"),
      B(313.5, YB, 337.5, 370, 0, 96, "brique_rouge"), B(337.5, YB, 412.5, 370, 0, 34, "brique_rouge"),
      B(337.5, YB, 412.5, 370, 82, 96, "brique_rouge"), B(412.5, YB, 446, 370, 0, 96, "brique_rouge")]
XB = 445.45
R += [B(XB, 198, 446, 369.45, 0, 96, "brique_rouge"), B(XB, 159, 446, 162, 0, 96, "brique_rouge"),
      B(XB, 162, 446, 198, 0, 34, "brique_rouge"), B(XB, 162, 446, 198, 82, 96, "brique_rouge")]
# poteau de bois brut contre le mur arrière (photo 07) et chambranle noir de la baie de l'entrée arrière
M += [B(263.5, 364.5, 270, 370, 0, 96, "bois_brut")]
M += [B(276.2, 369.0, 279.2, 369.5, 0, 82.8, NOIR), B(310.8, 369.0, 313.8, 369.5, 0, 82.8, NOIR), B(276.2, 369.0, 313.8, 369.5, 80, 82.8, NOIR)]
# ... et noir aussi dans l'épaisseur de la baie (photos 01, 07, 08) : par-dessus le doublage de pin que pose le moteur
M += [B(278.95, 369.95, 279.55, 380.05, 0, 80.05, NOIR), B(310.45, 369.95, 311.05, 380.05, 0, 80.05, NOIR),
      B(278.95, 369.95, 311.05, 380.05, 79.45, 80.05, NOIR)]
# cadrage noir de la fenêtre de l'évier, store cellulaire noir à demi baissé
M += [B(334.5, 369.0, 337.5, 369.5, 31, 85, NOIR), B(412.5, 369.0, 415.5, 369.5, 31, 85, NOIR), B(334.5, 369.0, 415.5, 369.5, 82, 85, NOIR),
      B(338, 371, 412, 372, 68, 81.5, "carbone"), B(337.5, 370.2, 412.5, 372.5, 81, 82, NOIR)]
M += [B(445.0, 159, 445.5, 162, 31, 85, NOIR), B(445.0, 198, 445.5, 201, 31, 85, NOIR), B(445.0, 159, 445.5, 201, 82, 85, NOIR)]
# armoires du bas noir mat, comptoir de bois de grange (mur arrière : évier double noir sous la fenêtre, lave-vaisselle)
M += [A(318, 345.5, 446, 369.4, 4, 34.5, NOIR, r=0.3, b=0.3), B(319, 347.5, 446, 369.4, 0, 4, "carbone"),
      A(317, 343.5, 446, 374.4, 34.5, 36.25, "bois_grange", r=0.4, b=0.3)]
M += [B(336, 345.2, 360, 345.6, 4.5, 34, "inox"), CX(338, 358, 344.6, 31.5, 0.45, "inox")]                   # lave-vaisselle
M += [B(x - 0.12, 345.3, x + 0.12, 345.5, 5, 34, "carbone") for x in (336, 360, 378, 396, 420)]                # joints des portes
M += [B(x, 345.0, x + 0.6, 345.5, 27, 32, "metal") for x in (333, 362.5, 375.5, 393, 399, 416.5)]             # poignées
M += [B(359, 347, 374, 366, 35.9, 36.3, "carbone"), B(376, 347, 391, 366, 35.9, 36.3, "carbone"),            # évier double noir
      C(375, 368.2, 1.2, 36.25, 37.5, "metal"),
      T([(375, 368.2, 37.5), (375, 368.2, 52), (375, 366.5, 55.5), (375, 362, 55.5), (375, 360, 51)], 0.6, "metal"),
      T([(377.5, 368.2, 37), (377.5, 368.2, 41), (378.5, 366, 42)], 0.25, "metal")]
# mur de droite : coin, cuisinière inox avec hotte cheminée, petit comptoir, tablettes flottantes de bois
M += [A(421.6, 336, 446, 345.5, 4, 34.5, NOIR, r=0.3, b=0.3), A(421.6, 290, 446, 306, 4, 34.5, NOIR, r=0.3, b=0.3),
      B(423.6, 290, 446, 306, 0, 4, "carbone"), B(423.6, 336, 446, 345.5, 0, 4, "carbone"),
      A(419.5, 336, 446, 343.6, 34.5, 36.25, "bois_grange", r=0.4, b=0.3), A(419.5, 290, 446, 306, 34.5, 36.25, "bois_grange", r=0.4, b=0.3)]
M += [A(420.5, 306.2, 446, 335.8, 0.5, 36, "inox", r=0.6, b=0.4), B(421.5, 306.6, 445.5, 335.4, 36, 36.4, "ecran"),        # cuisinière
      A(441.5, 306.2, 446, 335.8, 36, 43, "inox", r=0.6, b=0.4), B(441.3, 309, 441.6, 318, 38.5, 41.5, "ecran"),
      B(420.2, 309, 420.6, 333, 9, 27, "ecran"), CY(418.8, 309, 333, 30.5, 0.55, "inox"),
      B(418.9, 309, 420.5, 309.6, 30, 31, "inox"), B(418.9, 332.4, 420.5, 333, 30, 31, "inox"), B(420.4, 309, 420.6, 333, 2, 6, "carbone")]
M += [C(420.3, y, 0.9, 33, 34.2, "carbone", axe="x", x0=419.3, x1=420.5, z=33.6) for y in (311, 315, 327, 331)]
M += [A(424, 305, 446, 337, 62, 64.5, "inox", r=0.5, b=0.3), A(429, 309, 446, 333, 64.5, 69, "inox", r=0.5, b=0.3),
      A(433, 313, 446, 329, 69, 71, "inox", r=0.5, b=0.3), B(435, 314.5, 446, 327.5, 71, 96, "inox")]                     # hotte
M += [A(435.5, 338, 446, 369.4, z, z + 1.75, "bois_grange", r=0.3, b=0.25) for z in (52, 64)]
M += [C(441, 344, 2.2, 53.75, 57, "blanc"), C(440, 352, 1.8, 65.75, 69, "blanc"), A(438, 356, 444, 364, 53.75, 56, "osier", r=1, b=0.5)]
# colonne d'armoires pleine hauteur noir mat avec frigo inox encastré (photos 01, 02)
M += [A(421.4, 276, 446, 290, 0, 95.8, NOIR, r=0.2, b=0.2), A(421.4, 206, 446, 240, 0, 95.8, NOIR, r=0.2, b=0.2),
      A(421.4, 240, 446, 276, 72, 95.8, NOIR, r=0.2, b=0.2),
      A(419.5, 240.6, 446, 275.4, 0.5, 71.5, "inox", r=0.8, b=0.4), T([(418.4, 272.5, 30), (418.4, 272.5, 62)], 0.6, "inox", bouts=True),
      B(419.0, 272, 419.6, 273, 30, 31, "inox"), B(419.0, 272, 419.6, 273, 61, 62, "inox")]
M += [B(421.1, y - 0.12, 421.4, y + 0.12, 1, 95.5, "carbone") for y in (223, 240, 276)] + \
     [B(421.1, 206, 421.4, 240, 49.9, 50.1, "carbone"), B(421.1, 240, 421.4, 276, 83.9, 84.1, "carbone")]
M += [B(421.0, y, 421.4, y + 0.6, 40, 46, "metal") for y in (221, 225.5, 287)]
# deuxième frigo à portes françaises 36 po, devant la fenêtre du mur de droite (photos 01 à 03) : construit en blocs, car le
# modèle frigo_30 (30 × 24 × 69 po) agrandi par L=36 l'était dans les trois sens (≈ 83 po de haut). Ici 36 × 29 × 70 po.
def frigo_36(xf, y0, y1, H=70):
    """Frigo inox à portes françaises, devant vers -x en xf (face des portes), dos au mur de droite ; congélateur en tiroir."""
    yc = (y0 + y1) / 2
    out = [A(xf + 1.6, y0, 445.6, y1, 0.6, H - 0.4, "inox", r=0.8, b=0.4),                  # caisse
           B(xf + 1.3, y0 + 0.3, xf + 1.7, y1 - 0.3, 3.4, H - 0.6, "carbone"),               # joints sombres entre les portes
           A(xf, y0, xf + 1.6, yc - 0.15, 31.2, H, "inox", r=0.5, b=0.3), A(xf, yc + 0.15, xf + 1.6, y1, 31.2, H, "inox", r=0.5, b=0.3),
           A(xf, y0, xf + 1.6, y1, 3.6, 30.9, "inox", r=0.5, b=0.3),                          # tiroir du congélateur
           B(xf + 1.8, y0 + 0.6, xf + 2.2, y1 - 0.6, 0.6, 3.4, "carbone")]                   # grille du socle
    for yp in (yc - 2.2, yc + 2.2):                                                              # poignées verticales
        out += [T([(xf - 1.4, yp, 40), (xf - 1.4, yp, 64)], 0.42, "inox", bouts=True),
                B(xf - 1.4, yp - 0.3, xf, yp + 0.3, 41, 42, "inox"), B(xf - 1.4, yp - 0.3, xf, yp + 0.3, 62, 63, "inox")]
    out += [T([(xf - 1.4, y0 + 5, 27.5), (xf - 1.4, y1 - 5, 27.5)], 0.42, "inox", bouts=True),
            B(xf - 1.4, y0 + 6, xf, y0 + 6.6, 27, 28, "inox"), B(xf - 1.4, y1 - 6.6, xf, y1 - 6, 27, 28, "inox")]
    return out


# (2026-11-02) le 2e frigo est retiré à la demande du client : la fenêtre du mur de droite est dégagée
# îlot noir, dessus de bois de grange, 3 tabourets côté salle à manger, poubelles inox au bout
M += [A(352, 218, 380, 298, 4, 34.5, NOIR, r=0.3, b=0.3), B(354, 220, 378, 296, 0, 4, "carbone"),
      A(340, 214, 384, 302, 34.5, 36.5, "bois_grange", r=0.5, b=0.35)]
M += [B(380.0, y - 0.12, 380.4, y + 0.12, 5, 34, "carbone") for y in (238, 258, 278)]
for y in (232, 258, 284):
    M += tabouret(328, y)
M += [A(386, 212, 398, 226, 0, 27, "inox", r=1.5, b=0.6), A(386, 212, 398, 226, 27, 28.5, "carbone", r=1.5, b=0.5),
      A(400, 214, 410, 224, 0, 22, "gris", r=1.5, b=0.6)]

# =============================================================================================== salle à manger
# grande table de bois de récupération foncé, 8 chaises noires, luminaire linéaire noir suspendu (photos 06, 07)
M += [A(202, 248, 248, 342, 29, 31, "bois_recupere", r=0.6, b=0.4), B(206, 253, 244, 337, 25, 29, "bois_recupere")]
M += [B(x, y, x + 4, y + 4, 0, 25, "bois_recupere") for x in (206, 240) for y in (253, 333)]
M += chaise(190, 266, "+x") + chaise(190, 295, "+x") + chaise(190, 324, "+x") + \
     chaise(260, 266, "-x") + chaise(260, 295, "-x") + chaise(260, 324, "-x") + chaise(225, 236, "+y") + chaise(225, 354, "-y")
M += [B(220, 290, 230, 302, 94.6, 96, "carbone"), A(222.6, 270, 227.4, 322, 64, 65.6, "carbone", r=0.5, b=0.3),
      B(223.6, 271, 226.4, 321, 63.85, 64, "spot")]
M += [T([(221, 291, 94.6), (223.5, 272, 65.6)], 0.08, "metal"), T([(229, 291, 94.6), (226.5, 272, 65.6)], 0.08, "metal"),
      T([(221, 301, 94.6), (223.5, 320, 65.6)], 0.08, "metal"), T([(229, 301, 94.6), (226.5, 320, 65.6)], 0.08, "metal")]
M += [MOD("plante_sansevieria", 225, 300, z=31, H=14)]
# tableau noir (ardoise) encadré de pin au mur arrière, entre la fenêtre et le poteau (photos 06, 07, 08)
M += [B(222.5, 369.0, 257.5, 369.6, 30.5, 87.5, "ardoise-tableau"),
      B(220, 368.6, 222.5, 370, 28, 90, "pin_teint"), B(257.5, 368.6, 260, 370, 28, 90, "pin_teint"),
      B(220, 368.6, 260, 370, 28, 30.5, "pin_teint"), B(220, 368.6, 260, 370, 87.5, 90, "pin_teint")]
# buffet de bois sous un grand tableau (générique) contre le mur des garde-robes ; plantes
M += [A(177.6, 312, 194, 364, 5, 32, "bois_recupere", r=0.4, b=0.3)] + [B(x, y, x + 1.5, y + 1.5, 0, 5, "bois_recupere") for x in (179, 191) for y in (314, 361)]
M += [B(194, 314, 194.2, 362, 18.4, 18.6, "carbone"), B(194, 337.9, 194.2, 338.1, 6, 31, "carbone")]
M += cadre_mur_x(177.25, 321, 349, 45, 83, "carbone", sens=1)
M += [B(178.7, 327, 178.9, 333, 52, 74, "cuir"), B(178.7, 337, 178.9, 342, 50, 70, "cuir"), B(178.7, 324, 178.9, 346, 47, 50, "jete")]
M += [MOD("plante_sansevieria", 186, 354, z=32, H=22), C(186, 325, 3.5, 32, 37, "blanc")]
# coin bureau dans le renfoncement (photos 05, 06) : bureau flottant, écran large, petit écran au mur, chaise
M += [A(148.4, 207, 170, 248, 28.5, 30, "bois_recupere", r=0.4, b=0.3), B(148.4, 210, 150, 212, 22, 28.5, "metal"), B(148.4, 243, 150, 245, 22, 28.5, "metal"),
      A(150.5, 212, 152, 243, 33, 47, "ecran", r=0.6, b=0.3), B(152, 226, 155, 229, 30, 33.5, "metal"), B(152, 222, 160, 233, 30, 30.5, "metal"),
      B(148.4, 215, 149.6, 240, 54, 69, "ecran", r=0.3), B(158, 222, 166, 236, 30, 30.6, "carbone")]
M += [MOD("chaise_bureau", 170, 228, face="-x", mat="carbone")]

# =============================================================================================== salon
# sectionnel gris pâle en L à inclinables (dos au mur du hall, retour face à la fenêtre), tableau générique au mur
def sectionnel():
    out = [A(226, 12, 264, 134, 3, 17, "tissu", r=2, b=1.5), A(264, 96, 322, 134, 3, 17, "tissu", r=2, b=1.5),
           A(226, 12, 236, 134, 17, 34, "tissu", r=2.5, b=2), A(236, 125, 322, 134, 17, 34, "tissu", r=2.5, b=2),
           A(236, 12, 264, 18, 17, 24, "tissu", r=2, b=1.8), A(315, 96, 322, 125, 17, 24, "tissu", r=2, b=1.8)]
    out += [A(236, a + 0.3, 264, b - 0.3, 17, 21, "tissu", r=2.5, b=2.2) for a, b in ((18, 46), (46, 74), (74, 96), (96, 125))]
    out += [A(264.3, 96, 290, 125, 17, 21, "tissu", r=2.5, b=2.2), A(290.3, 96, 315, 125, 17, 21, "tissu", r=2.5, b=2.2)]
    out += [A(236, a + 0.5, 242, b - 0.5, 21, 36, "tissu", r=2.5, b=2.2) for a, b in ((18, 46), (46, 74), (74, 100))]   # têtières
    out += [A(266, 119, 290, 125, 21, 36, "tissu", r=2.5, b=2.2), A(291, 119, 314, 125, 21, 36, "tissu", r=2.5, b=2.2)]
    out += [A(264, 20, 279, 44, 9, 15.5, "tissu", r=2, b=1.5), B(262, 24, 266, 40, 9, 11, "metal")]                  # repose-pieds sorti
    out += [A(268, 106, 286, 120, 21, 27, "osier", r=3, b=2)]                                                       # coussin moutarde
    return out


M += sectionnel()
M += cadre_mur_x(224.25, 24, 86, 48, 86, "toile-ocre", sens=1)
M += [B(225.6, 30, 225.8, 44, 52, 80, "carbone"), B(225.6, 46, 225.8, 54, 50, 72, "ecran"), B(225.6, 60, 225.8, 72, 50, 66, "cuir"),
      B(225.6, 74, 225.8, 82, 56, 82, "jete"), B(225.6, 26, 225.8, 84, 50, 53, "carbone")]
# télé murale, meuble flottant gris-bois, thermopompe murale au-dessus (photos 02, 03)
M += [A(443.2, 66, 445.6, 124, 47, 80, "ecran", r=0.4, b=0.3), B(445.6, 80, 446, 110, 55, 72, "metal")]
M += [A(431, 68, 446, 124, 14, 29, "bois_grange", r=0.4, b=0.3), B(430.8, 72, 431, 84, 17, 26, "carbone"), B(430.8, 108, 431, 120, 17, 26, "carbone"),
      C(431, 78, 3, 19, 25, "gris", axe="x", x0=430.6, x1=431.2, z=21.5)]
M += [A(437, 116, 446, 152, 81, 92.5, "blanc", r=2.5, b=1), B(436.8, 118, 437.2, 150, 82, 84, "gris")]
M += [MOD("plante_sansevieria", 418, 26, H=40), C(418, 26, 7, 0, 9, "osier")]
# grande fenêtre de façade : store cellulaire gris remonté
M += [B(323.5, 6.5, 430.5, 8, 75, 81.5, "gris"), B(323, 6, 431, 9, 81, 82, "blanc")]
# plafond texturé (crépi) au salon seulement (photos 03, 04)
R += [B(224.25, 10, 446, 152, 95.6, 96, "crepi")]

# =============================================================================================== hall et entrée
# murs vert sauge, mur de cadres (génériques), banc blanc, vieille porte blanche décorative (photos 04, 05)
CADRES = [(70, 72, 8, 10, "metal"), (82, 80, 10, 8, "blanc"), (96, 74, 10, 12, "laiton"), (108, 86, 12, 9, "gris"),
          (122, 78, 8, 10, "blanc"), (136, 84, 10, 10, "metal"), (148, 74, 8, 12, "gris"), (76, 60, 14, 12, "gris"),
          (92, 56, 9, 12, "metal"), (140, 62, 12, 9, "laiton"), (150, 52, 8, 10, "blanc"), (72, 46, 8, 10, "metal"),
          (86, 42, 10, 8, "blanc"), (138, 48, 12, 10, "metal"), (116, 90, 8, 6, "blanc"), (96, 90, 9, 7, "metal")]
for yc, zc, w, h, mat in CADRES:
    M += cadre_mur_x(177.25, yc - w / 2, yc + w / 2, zc - h / 2, zc + h / 2, "comptoir", sens=1, cadre=mat, ep=0.9, bord=1.0)
    M += [B(178.35, yc - w / 2 + 2.2, 178.5, yc + w / 2 - 2.2, zc - h / 2 + 2.2, zc + h / 2 - 2.2, "carbone" if (yc + zc) % 3 else "gris")]
M += [A(177.6, 104, 180.2, 132, 0.5, 80, "blanc", r=0.3, b=0.2)]
M += [B(180.2, y0, 180.5, y1, z0, z1, "comptoir") for y0, y1, z0, z1 in ((107, 129, 50, 77), (107, 129, 22, 46), (107, 129, 4, 18))]
M += [T([(180.6, 110, 66), (182.5, 110, 66)], 0.35, "metal"), T([(180.6, 126, 66), (182.5, 126, 66)], 0.35, "metal")]
M += [A(180.4, 102, 195, 134, 15.5, 17.5, "blanc", r=0.4, b=0.3), B(181, 103, 183, 105, 0, 15.5, "blanc"), B(181, 131, 183, 133, 0, 15.5, "blanc"),
      B(192.5, 103, 194.5, 105, 0, 15.5, "blanc"), B(192.5, 131, 194.5, 133, 0, 15.5, "blanc"), B(181.5, 104, 194, 132, 5, 6, "blanc")]
M += [A(181 + 6 * k, 136, 186 + 6 * k, 146, 0.1, 4, "carbone" if k % 2 else "cuir", r=1.5, b=0.8) for k in range(4)]   # souliers
# habillage de bois brut au bout de la cloison du hall (poteau sous la poutre de l'ouverture, photo 05)
M += [B(218.5, 94.6, 225.5, 100, 0, 96, "bois_brut")]
# entrée avant : tapis, crochets à manteaux
M += [A(184, 14, 214, 40, 0, 0.4, "tapis", r=2, b=0.2)]
M += [B(177.3, 20, 178.3, 56, 64, 68, "pin_teint")] + [T([(178.3, y, 66), (181, y, 67)], 0.3, "metal") for y in (26, 34, 42, 50)]
M += [A(178.3, 24, 186, 34, 34, 64, "jete", r=2, b=1.5), A(178.3, 38, 186, 48, 38, 64, "carbone", r=2, b=1.5)]

# =============================================================================================== dégagement
M += [B(116, 170, 142, 198, 95.3, 96, "blanc"), B(118, 172, 140, 196, 95.1, 95.3, "gypse")]           # trappe du grenier (photo 09)

# =============================================================================================== salle de bain
# laveuse et sécheuse frontales empilées (à gauche en entrant), muret tuilé, douche vitrée coulissante à cadre noir,
# toilette sous la fenêtre, vanité noire à deux vasques, miroirs ronds, tablettes de fil noir (photos 13, 14, 15)
M += appareil(77, 104.5, 144.5, 172, 0) + appareil(77, 104.5, 144.5, 172, 36)
M += [B(71.8, 144.25, 76.2, 178.5, 0, 96, "gypse"), B(71.3, 144.25, 71.8, 178, 0, 84, "tuile_blanche"),
      B(71.8, 178.5, 76.2, 179, 0, 84, "tuile_blanche")]
M += [B(10, 144.25, 71.3, 144.8, 0, 84, "tuile_blanche"), B(10, 144.8, 10.625, 172.5, 0, 84, "tuile_blanche"),
      B(10.5, 144.8, 71.3, 178, 0, 0.6, "porcelaine"), B(10.5, 177.5, 71.3, 178.2, 0, 2.5, "tuile_blanche")]
M += [B(30, 144.8, 46, 145.2, 50, 62, "gris")]                                                              # niche
M += [B(12, 176.9, 44, 177.3, 2.5, 76, "verre"), B(40, 177.6, 71, 178, 2.5, 76, "verre"),
      B(10.5, 176.5, 71.3, 178.4, 76, 77.2, "metal"), B(10.5, 176.6, 12, 178.2, 2.5, 76, "metal"),
      B(69.8, 177.4, 71.3, 178.3, 2.5, 76, "metal"), T([(43, 178.6, 36), (43, 178.6, 52)], 0.45, "metal"),
      B(42.6, 177.6, 43.4, 178.6, 36, 37, "metal"), B(42.6, 177.6, 43.4, 178.6, 51, 52, "metal")]
M += [MOD("colonne_douche_noire", 56, 154.6, face="+y", z=30)]
M += [A(10.5, 182, 18.5, 198, 14, 30, "blanc", r=2, b=1), A(16, 183, 37, 197, 0, 15.5, "blanc", r=6.5, b=2),
      A(16.5, 183.5, 36.5, 196.5, 15.5, 16.8, "blanc", r=6.5, b=0.6), B(12, 187, 14, 193, 30, 30.4, "inox")]
M += [C(13.5, 203, 2.2, 25, 29, "blanc", axe="x", x0=10.5, x1=16, z=27), B(10.5, 202, 15, 203, 27, 28, "metal")]          # papier, sous l'allège (photo 14)
M += [A(42, 200, 104, 219.75, 32, 34, NOIR, r=0.4, b=0.3), A(43, 201.5, 103, 219.5, 22, 32, NOIR, r=0.3, b=0.3),
      B(44, 202, 102, 219, 6, 7, NOIR)] + [B(x, y, x + 1.5, y + 1.5, 0, 32, NOIR) for x in (43, 101.5) for y in (201, 218)]
for xs in (58, 88):
    M += [C(xs, 209, 5.5, 34, 39.5, "blanc", r2=7.5, pans=40), C(xs, 209, 6.6, 39.3, 39.5, "draps", pans=40),
          C(xs, 209, 0.9, 39.5, 39.6, "metal"),
          T([(xs, 217, 34), (xs, 217, 47), (xs, 215.5, 48.5), (xs, 212.5, 48.5)], 0.6, "metal"), B(xs - 0.3, 217.4, xs + 0.3, 219, 44, 45, "metal")]
M += [CY(58, 219.2, 219.7, 60, 10.5, "miroir"), TOR(58, 219.4, 60, 10.6, 0.55, "spot"),
      CY(88, 219.2, 219.7, 61, 13.5, "miroir"), TOR(88, 219.4, 61, 13.7, 0.55, "metal")]
for x0, x1, z in ((20, 36, 70), (20, 36, 58), (62, 74, 80), (78, 90, 76), (96, 104, 86)):
    M += [B(x0, 213, x1, 219.7, z, z + 0.5, "metal"), B(x0, 213, x0 + 0.3, 219.7, z, z + 5, "metal"), B(x1 - 0.3, 213, x1, 219.7, z, z + 5, "metal")]
M += [A(21, 213.5, 35, 219.5, 70.5, 75, "osier", r=1, b=0.6), A(21, 213.5, 35, 219.5, 58.5, 63.5, "osier", r=1, b=0.6),
      C(68, 216.5, 2.2, 80.5, 85, "carbone"), C(84, 216.5, 2.4, 76.5, 80, "osier")]
M += [B(10.6, 173, 12, 209, 70, 82, "gris")]                                                                 # store cellulaire

# =============================================================================================== chambre arrière
# papier peint imitation planches grises au mur de tête de lit, lit queen, table de chevet blanche, cadres de paysages
# brumeux (génériques), suspension cage noire, commode blanche, vélo de route sur base d'entraînement (photos 10 à 12)
R += [B(10, 226, 110.25, 226.4, 4.1, 96, "papier_planches")]
M += [MOD("lit_queen", 60, 268, face="+y")]
M += [A(11, 228, 27, 244, 0, 21, "blanc", r=0.4, b=0.3), B(11.5, 244, 26.5, 244.2, 10, 10.4, "gris"), B(17, 244, 21, 244.6, 13, 13.6, "laiton")]
for y0, y1, z0, z1, ton in ((246, 282, 58, 82, "jete"), (284, 296, 64, 82, "draps"), (298, 312, 66, 80, "jete"), (314, 326, 66, 82, "jete"),
                            (246, 256, 44, 56, "carbone"), (258, 268, 44, 56, "jete"), (270, 282, 44, 56, "draps"),
                            (284, 300, 38, 62, "jete"), (302, 326, 38, 62, "jete")):
    M += [B(10, y0, 11.5, y1, z0, z1, "draps"), B(11.5, y0 + 1, 11.7, y1 - 1, z0 + 1, (z0 + z1) / 2, ton),
          B(11.5, y0 + 1, 11.7, y1 - 1, (z0 + z1) / 2, z1 - 1, "draps")]
XC, YC = 77, 296                                                                                          # suspension cage
M += [C(XC, YC, 2.5, 95, 96, "carbone"), C(XC, YC, 0.15, 84, 95, "carbone"), C(XC, YC, 3.5, 82, 84.5, "placage"),
      {"forme": "sphere", "x": XC, "y": YC, "z": 79.5, "r": 2.2, "mat": "abat-jour"},
      TOR(XC, YC, 84, 3.8, 0.18, "carbone", axe="z"), TOR(XC, YC, 76, 7, 0.18, "carbone", axe="z"), TOR(XC, YC, 71, 5, 0.18, "carbone", axe="z")]
import math as _m
for k in range(8):
    a = k * _m.pi / 4
    M.append(T([(XC + 3.8 * _m.cos(a), YC + 3.8 * _m.sin(a), 84), (XC + 7 * _m.cos(a), YC + 7 * _m.sin(a), 76),
                (XC + 5 * _m.cos(a), YC + 5 * _m.sin(a), 71)], 0.16, "carbone"))
M += [A(14, 351, 50, 369.5, 0.5, 40, "blanc", r=0.4, b=0.3)] + [B(15, 350.8, 49, 351, z, z + 0.3, "gris") for z in (10, 20, 30)] + \
     [B(31, 350.4, 33, 351, z, z + 1, "laiton") for z in (5, 15, 25, 35)]
M += [B(20, 368.6, 40, 369.5, 52, 78, "metal"), B(21.5, 368.4, 38.5, 368.6, 53.5, 76.5, "carbone")]                # affiche céleste
M += [A(56, 334, 134, 368, 0, 0.35, "caoutchouc-noir", r=2, b=0.15), MOD("velo_route_base", 94, 352, face="+x")]
M += [B(56, 368.5, 140, 370, 82, 84.5, "ecran"), B(61, 371, 135, 372, 70, 82, "ecran")]                     # cantonnière et store marine
M += [A(124, 270, 142, 286, 0, 12, "blanc", r=2, b=0.8, trou=0.8)]                                             # panier à linge

# =============================================================================================== chambre avant (non photographiée)
M += [MOD("lit_queen", 52, 85, face="+x"), MOD("table_chevet", 19, 39, face="+x"), MOD("table_chevet", 19, 131, face="+x"),
      A(14, 11, 50, 29, 0.5, 34, "blanc", r=0.4, b=0.3)]

# =============================================================================================== entrée arrière
# palier au niveau du RDC devant la porte extérieure (x ≥ 292) ; volée qui descend vers la gauche le long du mur du fond
# (y 398 → 430), main courante de bois au mur (photos 01, 07, 08). ESTIMÉ : nombre de marches, largeur, giron à mesurer.
# Sous le plancher (z < 0) : visible seulement quand la visionneuse perce le plancher (SCENE["tremies_plancher"]).
EAR_X0, EAR_XN, EAR_Y0, EAR_Y1, GIRON, CM = 229, 284, 398, 430, 10.5, 7.5     # nez du palier à x = 284 : la porte
# extérieure (pentures côté mur du fond, battant de 34 po jusqu'à x ≈ 285½) ne balaie pas la volée
M += [A(294, 395, 315.5, 425, 0, 0.4, "tapis", r=2, b=0.2)]                                   # devant la porte extérieure
# Volée de 6 marches qui descend vers la porte extérieure : NON dessinée dans la maquette des deux étages (elle plongerait
# dans le walk-in du sous-sol, sous le perron) ; niveau réel de l'entrée arrière, nombre de marches et garde à mesurer.

# portes d'une autre finition que le pin (portes plates blanches des garde-robes de la chambre arrière, photo 10) : l'ouverture
# porte "finition": "<matériau>" dans maison.json (base_rdc01_modifs.py ou un module rdc_*.py). Le moteur ne connaît qu'un
# matériau de battant ("porte" → mats_finitions) : on habille le battant, à l'état FERMÉ calculé par le moteur (battant()),
# d'une pellicule de 0,08 po de ce matériau, liée à la porte ("porte": id) pour qu'elle pivote avec elle quand on l'ouvre.
# Moteur plus ancien (sans battant()) : battant dessiné tel quel (feuille_porte / porte_fermee), sans lien.
# Objets marqués "role": "finition_porte" ; rien n'est ajouté si maison.json ou le moteur manquent.
def portes_finies(niveau="RDC"):
    import importlib.util, json, os, sys
    ici = os.path.dirname(os.path.abspath(__file__))
    try:
        mj = json.load(open(os.path.join(ici, "donnees", "maison.json"), encoding="utf-8"))
        niv = next(n for n in mj["niveaux"] if n["id"] == niveau)
        g = sys.modules.get("__main__")                # le moteur qui nous charge (generer_3d.py), sinon son fichier
        if not any(hasattr(g, f) for f in ("battant", "feuille_porte")):
            f = next(p for p in (os.path.join(ici, "..", "outils", "generer_3d.py"),
                                 os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "generer_3d.py")) if os.path.isfile(p))
            spec = importlib.util.spec_from_file_location("m18_moteur_portes", f)
            g = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(g)
    except Exception as err:                       # maison.json pas encore construit, moteur introuvable : battants en pin
        print("  portes finies ignorées :", err)
        return []
    murs, out, e = {m["id"]: m for m in niv["murs"]}, [], 0.08
    par_mur = {}
    for o in niv["ouvertures"]:
        par_mur.setdefault(o["mur_id"], []).append(o)
    for o in niv["ouvertures"]:
        m = murs.get(o["mur_id"])
        if not o.get("finition") or not m or o["type"] == "fenetre" or o.get("operation") in ("coulissante", "aucune") \
                or o.get("materiau") == "verre" or (o.get("position") or {}).get("valeur") is None:
            continue
        t = (m.get("epaisseur") or {}).get("valeur") or 4.5
        lien = {}
        try:
            if hasattr(g, "battant"):
                bt = g.battant(dict(m, _ouvertures=par_mur.get(m["id"], [])), o, t, [])
                f = next(b for b in bt["boites"] if b["mat"] in ("porte", "porte-ext"))
                lien = {"porte": o["id"]}
            elif o.get("fermee"):
                f = g.porte_fermee(m, o, t)[0]
            else:
                f = dict(g.feuille_porte(m, o, t), z0=0.5, z1=80)
        except Exception as err:
            print("  porte", o["id"], "laissée en pin :", err)
            continue
        out.append(dict(B(f["x0"] - e, f["y0"] - e, f["x1"] + e, f["y1"] + e, f["z0"] - e, f["z1"] + e, o["finition"]),
                        role="finition_porte", ouverture=o["id"], **lien))
    return out


M += portes_finies()

# bande d'ardoise devant la baie de l'entrée arrière, prolongement du plancher de la cuisine (photo 07), et barres de seuil
R += [B(262, 336, 316.1, 370, 0, 0.12, "ardoise_noire"), B(261.5, 335.5, 316.5, 336.2, 0, 0.3, "inox"),
      B(261.5, 335.5, 262.2, 370, 0, 0.3, "inox"), B(315.8, 157, 316.5, 335.5, 0, 0.3, "inox")]

SCENE = {
    "niveau": "RDC",
    "titre": TITRE,
    "plafond": 96,               # PRÉSUMÉ (8 pi) : à mesurer
    # trou dans le plancher [x0, y0, x1, y1] : volée qui descend de l'entrée arrière (demande au moteur ; ignoré tant que la
    # visionneuse ne perce pas le plancher, le sous-plancher de béton cache alors tout ce qui est sous z = 0)
    "tremies_plancher": [[EAR_X0, EAR_Y0, EAR_XN, EAR_Y1]],
    "allege_fenetre": 34, "tete_fenetre": 82,     # ESTIMÉ sur les photos
    # MAISON-18 (client, 2026-11-02 : « la fenêtre du salon en haut est aussi plus grande vers le bas ») : grande fenêtre de
    # façade du salon (3 sections) descendue à 20 po (HYPOTHÈSE à mesurer), tête et linteau 2-2×10 inchangés
    "fenetres": {"ouv-RDC-002": {"allege": 20, "sections": 3}},
    "sol_defaut": "erable",
    "sols": {"piece-RDC-CUI": "ardoise_noire", "piece-RDC-ENT": "ardoise_noire", "piece-RDC-EAR": "ardoise_noire",
             "piece-RDC-SDB": "porcelaine"},
    "mat_colonne": "bois_brut",
    "mat_poutre": "bois_brut",
    "mats_finitions": {"porte": "pin_teint", "plinthe": "pin_teint", "placage": "pin_teint", "metal": "blanc"},
    "peintures": {  # nom : [couleur à l'écran, description, alias pour le mobilier]
        "Blanc cassé": ["#EFEBE3", "murs et plafonds (teinte estimée sur les photos)"],
        "Vert sauge": ["#8B9A85", "hall et entrée avant (teinte estimée sur la photo 04 ; à comparer au nuancier)"],
        "Noir mat": ["#1E1F20", "armoires de cuisine, îlot, chambranle de la baie arrière, vanité", "noir-mat"],
        "Ardoise": ["#2C302F", "tableau noir de la salle à manger", "ardoise-tableau"],
    },
    "peinture": {"piece-RDC-HALL": "Vert sauge", "piece-RDC-ENT": "Vert sauge"},
    "accents": [],
    "mobilier": M,
    "revetements": R,
    # encastrés de la cuisine : devant la hotte et devant la colonne d'armoires (avant : au-dessus de la hotte et cachés
    # au-dessus de la colonne pleine hauteur, qui ne laisse que 0,2 po sous le plafond)
    "lumieres": [{"x": 340, "y": 356}, {"x": 375, "y": 356}, {"x": 410, "y": 356}, {"x": 414, "y": 322}, {"x": 406, "y": 262},
                 {"x": 406, "y": 222}, {"x": 362, "y": 236}, {"x": 362, "y": 282}, {"x": 395, "y": 190},
                 {"x": 225, "y": 296, "z": 70, "i": 5}, {"x": 186, "y": 214}, {"x": 290, "y": 360, "i": 6},
                 {"x": 198, "y": 180}, {"x": 200, "y": 112}, {"x": 198, "y": 36}, {"x": 128, "y": 186},
                 {"x": 42, "y": 190}, {"x": 82, "y": 190},
                 {"x": 77, "y": 296, "z": 82, "i": 5}, {"x": 77, "y": 75, "z": 92, "i": 5},
                 {"x": 300, "y": 80, "z": 92, "i": 4}, {"x": 390, "y": 80, "z": 92, "i": 4}, {"x": 273, "y": 405}],
    "visites": [{"nom": "Entrée avant", "x": 198, "y": 34, "cap": 90},
                {"nom": "Hall (mur de cadres)", "x": 300, "y": 146, "cap": 184},
                {"nom": "Salon", "x": 300, "y": 80, "cap": 25},
                {"nom": "Salon vers le hall", "x": 362, "y": 196, "cap": 198},
                {"nom": "Cuisine", "x": 262, "y": 232, "cap": 32},
                {"nom": "Îlot et cuisinière", "x": 318, "y": 318, "cap": 350},
                {"nom": "Cuisine vers le salon", "x": 336, "y": 206, "cap": 262},
                {"nom": "Salle à manger", "x": 305, "y": 212, "cap": 145},
                {"nom": "Coin bureau", "x": 296, "y": 268, "cap": 192},
                {"nom": "Corridor", "x": 150, "y": 186, "cap": 180},
                {"nom": "Salle de bain", "x": 118, "y": 188, "cap": 180},
                {"nom": "Vanité", "x": 102, "y": 178, "cap": 140},
                {"nom": "Chambre arrière", "x": 127, "y": 220, "cap": 100},
                {"nom": "Chambre arrière, tête de lit", "x": 112, "y": 336, "cap": 222},
                {"nom": "Chambre avant (présumée)", "x": 126, "y": 126, "cap": 212},
                {"nom": "Entrée arrière", "x": 295, "y": 352, "cap": 90}],
    "depart": {"x": 198, "y": 34, "cap": 90},
    "palette": [["Plancher", "érable naturel clair, lames étroites (salon, salle à manger, chambres, corridor)", "#D8C29A"],
                ["Cuisine", "tuile d'ardoise noire 24 po, mur de brique rouge à joints pâles, armoires noir mat, comptoirs et îlot en bois de grange, électros inox", "#2B2F2E"],
                ["Bois", "poutres et poteaux de bois brut teint brun-roux ; portes de pin teint à panneaux horizontaux, gros cadrages", "#8A4B2A"],
                ["Hall", "murs vert sauge, mur de cadres, banc blanc et vieille porte blanche", "#8B9A85"],
                ["Salle de bain", "porcelaine grise, douche vitrée à cadre noir, vanité noire à deux vasques, robinetterie noire", "#7D7F80"],
                ["Chambre arrière", "papier peint imitation planches grises, suspension cage noire", "#A7A39B"],
                ["Plafonds", "blancs ; crépi au salon", "#EFEBE3"]],
}
