"""Maquette 3D de SS-03 : matériaux, mobilier indicatif, éclairage, points de visite.

Direction : moderne chaleureux (voir DESIGN.md). Coordonnées en pouces, repère de la maison.
Le mobilier sert à juger les volumes et l'ambiance ; il n'est pas un choix de produit.
"""

TITRE = "SS-03 — Grande salle de bain, cuisine, gym vitré"


def B(x0, y0, x1, y1, z0, z1, mat):
    return {"forme": "boite", "x0": x0, "y0": y0, "x1": x1, "y1": y1, "z0": z0, "z1": z1, "mat": mat}


def C(x, y, r, z0, z1, mat):
    return {"forme": "cylindre", "x": x, "y": y, "r": r, "z0": z0, "z1": z1, "mat": mat}


def sofa(x0, y0, x1, y1, dos):
    out = [B(x0, y0, x1, y1, 0, 17, "tissu")]
    e = 8
    out.append({"+y": B(x0, y1 - e, x1, y1, 17, 32, "tissu"), "-y": B(x0, y0, x1, y0 + e, 17, 32, "tissu"),
                "+x": B(x1 - e, y0, x1, y1, 17, 32, "tissu"), "-x": B(x0, y0, x0 + e, y1, 17, 32, "tissu")}[dos])
    return out


def lit(x0, y0, x1, y1):
    """Tête de lit contre le mur arrière (y1)."""
    return [B(x0, y0, x1, y1 - 4, 0, 13, "placage"), B(x0 + 1, y0 + 1, x1 - 1, y1 - 5, 13, 23, "draps"),
            B(x0 + 1, y0 + 1, x1 - 1, y0 + 34, 23, 24, "jete"),
            B(x0 + 6, y1 - 20, (x0 + x1) / 2 - 2, y1 - 6, 23, 28, "draps"), B((x0 + x1) / 2 + 2, y1 - 20, x1 - 6, y1 - 6, 23, 28, "draps"),
            B(x0 - 6, y1 - 4, x1 + 6, y1, 0, 46, "tissu")]


def table_chevet(x, y):
    return [B(x - 10, y - 8, x + 10, y + 8, 0, 22, "placage"), C(x, y, 4, 22, 34, "metal"), C(x, y, 6, 34, 40, "abat-jour")]


def etagere(x0, y0, x1, y1):
    out = [B(x0, y0, x0 + 1.5, y1, 0, 84, "metal"), B(x1 - 1.5, y0, x1, y1, 0, 84, "metal")]
    out += [B(x0, y0, x1, y1, z, z + 1, "placage") for z in (4, 22, 40, 58, 76)]
    return out


M = []
# --- séjour / salle à manger
M += [B(234 + 3 * i, 10, 236 + 3 * i, 11.6, 0, 89, "placage") for i in range(33)]            # mur de lattes de chêne
M += [B(250, 11.6, 322, 27, 0, 18, "placage"), B(258, 11.7, 314, 13, 30, 62, "ecran")]
M += [B(238, 40, 350, 132, 0, 0.4, "tapis")]
M += sofa(244, 98, 340, 136, "+y") + sofa(340, 66, 378, 136, "+x")
M += [B(268, 58, 318, 82, 13, 15, "placage"), B(270, 60, 272, 80, 0, 13, "metal"), B(314, 60, 316, 80, 0, 13, "metal")]
M += [C(404, 108, 22, 28, 30, "placage"), C(404, 108, 3, 0, 28, "metal"), C(404, 108, 9, 64, 72, "metal"), C(404, 108, 0.3, 72, 90, "metal")]
M += [B(404 + dx - 8, 108 + dy - 8, 404 + dx + 8, 108 + dy + 8, 0, 18, "tissu") for dx, dy in ((0, 30), (0, -30), (30, 0), (-30, 0))]
# --- cuisine en ligne (10 pi) : bas en chêne, haut blanc mat, quartz blanc, dosseret de tuile, frigo inox
M += [B(330, 205.75, 414, 227.75, 0, 34.5, "placage"), B(330, 205, 414, 227.75, 34.5, 36, "comptoir"),
      B(333, 207, 363, 226, 36, 36.4, "ecran"),                           # plaque de cuisson
      B(380, 208, 404, 224, 35.8, 36.1, "metal"),                          # évier
      B(390, 223, 392, 225, 36, 48, "metal"),                              # robinet
      B(330, 227.2, 414, 227.7, 36, 54, "tuile_blanche"),
      B(330, 215.75, 414, 227.75, 54, 86, "porte"), B(330, 215.5, 414, 216, 53.4, 54, "spot"),
      B(414.5, 200, 444.5, 229, 0, 72, "inox"), B(414.5, 200, 444.5, 229, 72, 86, "porte")]
# --- salle d'entraînement vitrée
M += [B(112, 10.2, 216, 10.8, 6, 84, "miroir")]
M += [B(112, 62, 142, 134, 0, 8, "caoutchouc-noir"), B(113, 60, 116, 64, 8, 50, "metal"), B(138, 60, 141, 64, 8, 50, "metal"),
      B(112, 58, 142, 66, 46, 52, "ecran")]
M += [B(x - 1.5, y - 1.5, x + 1.5, y + 1.5, 0, 86, "metal") for x in (172, 214) for y in (60, 104)]
M += [B(170.5, 58.5, 215.5, 61.5, 83, 86, "metal"), B(170.5, 102.5, 215.5, 105.5, 83, 86, "metal"),
      B(186, 72, 198, 118, 14, 17, "caoutchouc-noir"), B(190, 80, 194, 110, 0, 14, "metal"), B(150, 140, 202, 153, 0, 26, "metal")]
# --- utilité et buanderie
M += [C(34, 138, 11, 0, 58, "blanc"), B(10.2, 99, 14, 119, 40, 70, "gris"),
      B(14.5, 11, 41.5, 38, 0, 38, "blanc"), C(28, 38.2, 7, 14, 28, "ecran"),
      B(44.5, 11, 71.5, 38, 0, 38, "blanc"), C(58, 38.2, 7, 14, 28, "ecran"),
      B(12, 11, 74, 37, 38, 39.5, "comptoir"), B(76, 12, 96, 26, 0, 72, "metal")]
# --- salle de bain : bain sous la fenêtre, toilette murale devant un muret, douche walk-in, double vanité suspendue
M += [B(10.5, 160, 40, 220, 0, 20, "blanc"), B(14, 164, 36.5, 216, 19, 20.2, "eau")]
M += [B(44, 214, 78, 222.25, 0, 42, "gypse"), B(43.5, 213.5, 78.5, 222.75, 42, 43.5, "comptoir"),
      B(53, 196, 67, 214, 10, 16, "blanc"), B(56, 212.5, 64, 213.5, 32, 36, "metal")]
M += [B(84, 159.3, 144, 159.8, 0, 84, "tuile_blanche"), B(143.2, 159.25, 143.7, 195, 0, 84, "tuile_blanche"),
      B(84, 159.25, 144, 195, 0, 0.5, "tuile_blanche"),
      B(110, 194.5, 144, 195.5, 0, 76, "verre"), B(110, 194.2, 111, 195.8, 0, 76, "metal"),
      C(126, 166, 4, 76, 77, "metal"), B(125.5, 159.8, 126.5, 166, 76.5, 77.5, "metal")]
M += [B(151, 225.75, 223, 247.75, 12, 32, "placage"), B(150.5, 225.25, 223.5, 247.75, 32, 33.5, "comptoir"),
      C(169, 236, 7, 33.5, 38, "blanc"), C(205, 236, 7, 33.5, 38, "blanc"),
      B(168.5, 243, 169.5, 246, 33.5, 44, "metal"), B(204.5, 243, 205.5, 246, 33.5, 44, "metal"),
      B(157, 247.2, 181, 247.7, 42, 74, "miroir"), B(193, 247.2, 217, 247.7, 42, 74, "miroir")]
# --- chambres
M += lit(110, 288, 170, 366) + table_chevet(92, 356) + table_chevet(188, 356) + [B(96, 270, 184, 368, 0, 0.4, "tapis")]
M += [B(37.5, 295, 39, 355, 0, 80, "placage")]                                   # portes coulissantes de la G.-R.
M += lit(345, 288, 405, 366) + table_chevet(327, 356) + table_chevet(423, 356)
M += [B(391, 257.5, 439, 259, 0, 80, "placage")]
M += [B(418, 280, 444, 328, 29, 30.5, "placage"), B(420, 282, 422, 326, 0, 29, "metal"), B(424, 296, 440, 312, 0, 18, "tissu")]
# --- rangement (ancien caveau) : étagères sur trois côtés
M += etagere(230, 384, 246, 430) + etagere(300, 384, 316, 430) + etagere(250, 414, 296, 430)

SCENE = {
    "niveau": "SS",
    "titre": TITRE,
    "plafond": 90,
    "allege_fenetre": 56, "tete_fenetre": 86,
    "sol_defaut": "chene",
    "sols": {"piece-SS-UTIL": "beton", "piece-SS-GYM": "caoutchouc", "piece-SS-SDB": "porcelaine",
             "piece-SS-LEG": "beton", "piece-SS-PERRON": "beton"},
    "mat_colonne": "placage",
    "mobilier": M,
    "revetements": [],
    "lumieres": [{"x": 300, "y": 80}, {"x": 404, "y": 108}, {"x": 372, "y": 195}, {"x": 190, "y": 182}, {"x": 164, "y": 84},
                 {"x": 55, "y": 85}, {"x": 70, "y": 185}, {"x": 187, "y": 228}, {"x": 118, "y": 310}, {"x": 360, "y": 300},
                 {"x": 264, "y": 300}, {"x": 273, "y": 408}],
    "visites": [{"nom": "Entrée", "x": 428, "y": 180, "cap": 195}, {"nom": "Séjour", "x": 300, "y": 150, "cap": 270},
                {"nom": "Cuisine", "x": 330, "y": 120, "cap": 60}, {"nom": "Gym (porte vitrée)", "x": 190, "y": 196, "cap": 270},
                {"nom": "Salle de bain", "x": 132, "y": 236, "cap": 205}, {"nom": "Double vanité", "x": 110, "y": 205, "cap": 20}, {"nom": "Chambre 1", "x": 66, "y": 262, "cap": 35},
                {"nom": "Chambre 2", "x": 320, "y": 245, "cap": 30}, {"nom": "Utilité", "x": 82, "y": 128, "cap": 235},
                {"nom": "Rangement", "x": 264, "y": 350, "cap": 90}],
    "depart": {"x": 428, "y": 180, "cap": 195},
    "palette": [["Plancher", "chêne pâle, lames larges (vinyle de luxe)", "#C9A97E"],
                ["Murs et plafonds", "blanc chaud mat", "#F1EEE8"],
                ["Accents", "noir mat : cadres vitrés, robinetterie, luminaires", "#1E1E1E"],
                ["Séjour", "mur télé en lattes de chêne, tissu gris chaud", "#B98E5E"],
                ["Cuisine", "bas en chêne, haut blanc mat sans poignée, quartz blanc, dosseret de tuile blanche, inox", "#E9E7E2"],
                ["Salle de bain", "porcelaine 24×48 gris pâle, tuile blanche verticale, vanité de chêne suspendue, toilette murale", "#D9D6D0"],
                ["Gym", "dalles de caoutchouc noir, miroir pleine largeur, verre à cadre noir", "#2A2A2A"]],
}
