"""Maquette 3D de SS-02 : matériaux, mobilier indicatif, éclairage, points de visite.

Direction de design : moderne chaleureux. Plancher de chêne pâle en lames larges partout (vinyle de luxe),
murs blanc chaud, accents noir mat (cadres vitrés, quincaillerie), mur de lattes de chêne au salon,
salle de bain en porcelaine grand format pâle et tuile blanche verticale à la douche, caoutchouc noir au gym.
Coordonnées en pouces, repère de la maison. Le mobilier sert seulement à visualiser les volumes.
"""

TITRE = "SS-02 — Aire ouverte et gym vitré"


def B(x0, y0, x1, y1, z0, z1, mat, nom=None):
    return {"forme": "boite", "x0": x0, "y0": y0, "x1": x1, "y1": y1, "z0": z0, "z1": z1, "mat": mat, "nom": nom}


def C(x, y, r, z0, z1, mat):
    return {"forme": "cylindre", "x": x, "y": y, "r": r, "z0": z0, "z1": z1, "mat": mat}


def sofa(x0, y0, x1, y1, dos):
    """dos : côté du dossier ('+y', '-y', '+x', '-x')."""
    out = [B(x0, y0, x1, y1, 0, 17, "tissu")]
    e = 8
    if dos == "+y":
        out.append(B(x0, y1 - e, x1, y1, 17, 32, "tissu"))
    elif dos == "-y":
        out.append(B(x0, y0, x1, y0 + e, 17, 32, "tissu"))
    elif dos == "+x":
        out.append(B(x1 - e, y0, x1, y1, 17, 32, "tissu"))
    else:
        out.append(B(x0, y0, x0 + e, y1, 17, 32, "tissu"))
    return out


def lit(x0, y0, x1, y1):
    """Tête de lit contre le mur arrière (y1)."""
    return [B(x0, y0, x1, y1 - 4, 0, 13, "placage"), B(x0 + 1, y0 + 1, x1 - 1, y1 - 5, 13, 23, "draps"),
            B(x0 + 1, y0 + 1, x1 - 1, y0 + 34, 23, 24, "jete"),
            B(x0 + 6, y1 - 20, (x0 + x1) / 2 - 2, y1 - 6, 23, 28, "draps"), B((x0 + x1) / 2 + 2, y1 - 20, x1 - 6, y1 - 6, 23, 28, "draps"),
            B(x0 - 6, y1 - 4, x1 + 6, y1, 0, 46, "tissu")]


def table_chevet(x, y):
    return [B(x - 10, y - 8, x + 10, y + 8, 0, 22, "placage"), C(x, y, 4, 22, 34, "metal"), C(x, y, 6, 34, 40, "abat-jour")]


MOBILIER = []
# --- salon / salle de jeu (aire ouverte)
MOBILIER += [B(234 + 3 * i, 10, 236 + 3 * i, 11.6, 0, 89, "placage") for i in range(33)]          # mur de lattes de chêne
MOBILIER += [B(250, 11.6, 322, 27, 0, 18, "placage"), B(258, 11.7, 314, 13, 30, 62, "ecran")]     # meuble télé, téléviseur
MOBILIER += [B(238, 40, 350, 132, 0, 0.4, "tapis")]
MOBILIER += sofa(244, 98, 340, 136, "+y") + sofa(340, 66, 378, 136, "+x")
MOBILIER += [B(268, 58, 318, 82, 13, 15, "placage"), B(270, 60, 272, 80, 0, 13, "metal"), B(314, 60, 316, 80, 0, 13, "metal")]
MOBILIER += [C(404, 108, 21, 28, 30, "placage"), C(404, 108, 3, 0, 28, "metal")] + \
            [B(404 + dx - 8, 108 + dy - 8, 404 + dx + 8, 108 + dy + 8, 0, 18, "tissu") for dx, dy in ((0, 30), (0, -30), (30, 0), (-30, 0))]
# --- salle d'entraînement vitrée
MOBILIER += [B(112, 10.2, 216, 10.8, 6, 84, "miroir")]
MOBILIER += [B(112, 62, 142, 134, 0, 8, "caoutchouc-noir"), B(113, 60, 116, 64, 8, 50, "metal"), B(138, 60, 141, 64, 8, 50, "metal"),
             B(112, 58, 142, 66, 46, 52, "ecran")]
MOBILIER += [B(x - 1.5, y - 1.5, x + 1.5, y + 1.5, 0, 86, "metal") for x in (172, 214) for y in (60, 104)] + \
            [B(170.5, 58.5, 215.5, 61.5, 83, 86, "metal"), B(170.5, 102.5, 215.5, 105.5, 83, 86, "metal"),
             B(186, 72, 198, 118, 14, 17, "caoutchouc-noir"), B(190, 80, 194, 110, 0, 14, "metal")]
MOBILIER += [B(150, 140, 202, 153, 0, 26, "metal")]
# --- salle d'utilité
MOBILIER += [C(34, 136, 11, 0, 58, "blanc"), B(10.2, 99, 14, 119, 40, 70, "gris"), B(60, 14, 96, 30, 0, 72, "metal")]
# --- salle de bain
MOBILIER += [B(10.5, 190, 40, 248, 0, 20, "blanc"), B(14, 194, 36.5, 244, 19, 20.2, "eau")]
MOBILIER += [B(52, 213, 68, 222, 15, 31, "blanc"), C(60, 204, 8, 0, 15, "blanc")]
MOBILIER += [B(56, 159.5, 100, 181, 4, 32, "placage"), B(55, 159.5, 101, 182, 32, 33.5, "comptoir"), C(78, 172, 7, 33.5, 38, "blanc"),
             B(60, 159.5, 96, 160.2, 40, 74, "miroir")]
MOBILIER += [B(107.5, 212, 108.5, 248, 0, 76, "verre"), B(108, 211.5, 126, 212.5, 0, 76, "verre"),
             B(108, 212, 144, 248, 0, 0.6, "tuile_blanche")]
# --- chambres
MOBILIER += lit(110, 288, 170, 366) + table_chevet(92, 356) + table_chevet(188, 356) + [B(96, 270, 184, 368, 0, 0.4, "tapis")]
MOBILIER += lit(345, 288, 405, 366) + table_chevet(327, 356) + table_chevet(423, 356) + \
            [B(418, 222, 444, 270, 29, 30.5, "placage"), B(420, 224, 422, 268, 0, 29, "metal"), B(424, 238, 440, 254, 0, 18, "tissu")]

REVETEMENTS = [  # tuile murale de la douche (sur les faces intérieures des cloisons)
    B(108, 247.2, 144, 247.7, 0, 84, "tuile_blanche"),
    B(143.2, 212, 143.7, 248, 0, 84, "tuile_blanche"),
]

SCENE = {
    "niveau": "SS",
    "titre": TITRE,
    "plafond": 90,            # 7'-6" fini (hypothèse : hauteur réelle non mesurée)
    "allege_fenetre": 56, "tete_fenetre": 86,
    "sol_defaut": "chene",
    "sols": {"piece-SS-UTIL": "beton", "piece-SS-GYM": "caoutchouc", "piece-SS-SDB": "porcelaine",
             "piece-SS-LEG": "beton", "piece-SS-PERRON": "beton"},
    "mat_colonne": "placage",
    "mobilier": MOBILIER,
    "revetements": REVETEMENTS,
    "lumieres": [{"x": 300, "y": 80}, {"x": 400, "y": 120}, {"x": 330, "y": 182}, {"x": 200, "y": 182}, {"x": 164, "y": 84},
                 {"x": 55, "y": 85}, {"x": 78, "y": 205}, {"x": 118, "y": 310}, {"x": 373, "y": 287}, {"x": 264, "y": 290}],
    "visites": [{"nom": "Entrée", "x": 428, "y": 180, "cap": 195}, {"nom": "Salon", "x": 300, "y": 150, "cap": 270},
                {"nom": "Gym vitré", "x": 250, "y": 190, "cap": 215}, {"nom": "Salle de bain", "x": 128, "y": 180, "cap": 135},
                {"nom": "Chambre 1", "x": 40, "y": 266, "cap": 40}, {"nom": "Chambre 2", "x": 320, "y": 230, "cap": 30},
                {"nom": "Utilité", "x": 80, "y": 120, "cap": 225}],
    "depart": {"x": 428, "y": 180, "cap": 195},
    "palette": [["Plancher", "chêne pâle, lames larges (vinyle de luxe)", "#C9A97E"],
                ["Murs et plafonds", "blanc chaud mat", "#F1EEE8"],
                ["Accents", "noir mat : cadres vitrés, poignées, luminaires", "#1E1E1E"],
                ["Mur télé", "lattes de chêne verticales", "#B98E5E"],
                ["Salle de bain", "porcelaine 24×48 gris pâle, tuile blanche verticale à la douche", "#D9D6D0"],
                ["Gym", "dalles de caoutchouc noir, miroir pleine largeur", "#2A2A2A"]],
}
