"""Maquette 3D de SS-05 : matériaux, peinture, mobilier indicatif, éclairage, arrêts de la visite guidée.

Direction : moderne chaleureux (voir DESIGN.md). Coordonnées en pouces, repère de la maison.
Le mobilier sert à juger les volumes et l'ambiance ; il n'est pas un choix de produit.
"""

TITRE = "SS-05 — Salle de bain revue, matériaux réels"


def B(x0, y0, x1, y1, z0, z1, mat):
    return {"forme": "boite", "x0": x0, "y0": y0, "x1": x1, "y1": y1, "z0": z0, "z1": z1, "mat": mat}


def C(x, y, r, z0, z1, mat):
    return {"forme": "cylindre", "x": x, "y": y, "r": r, "z0": z0, "z1": z1, "mat": mat}


def CY(x, y0, y1, z, r, mat):
    """Cylindre couché le long de y (hublot de laveuse, volant de vélo)."""
    return {"forme": "cylindre", "axe": "y", "x": x, "y0": y0, "y1": y1, "z": z, "r": r, "mat": mat}


def CX(x0, x1, y, z, r, mat):
    """Cylindre couché le long de x (tringle, haltère)."""
    return {"forme": "cylindre", "axe": "x", "x0": x0, "x1": x1, "y": y, "z": z, "r": r, "mat": mat}


def sofa(x0, y0, x1, y1, dos):
    out = [B(x0, y0, x1, y1, 0, 17, "tissu")]
    e = 8
    out.append({"+y": B(x0, y1 - e, x1, y1, 17, 32, "tissu"), "-y": B(x0, y0, x1, y0 + e, 17, 32, "tissu"),
                "+x": B(x1 - e, y0, x1, y1, 17, 32, "tissu"), "-x": B(x0, y0, x0 + e, y1, 17, 32, "tissu")}[dos])
    return out


def fauteuil(x, y, dos):
    out = sofa(x - 15, y - 15, x + 15, y + 15, dos) + [B(x - 15, y - 15, x - 11, y + 15, 17, 24, "tissu"), B(x + 11, y - 15, x + 15, y + 15, 17, 24, "tissu")]
    for o in out:
        o["mat"] = "cuir"
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


def appareil(x0, x1, y_dos, y_face):
    """Laveuse ou sécheuse frontale : caisse blanche, hublot, bandeau de commandes."""
    xc = (x0 + x1) / 2
    return [B(x0, y_dos, x1, y_face, 0, 36, "blanc"), CY(xc, y_face, y_face + 0.4, 18, 8.5, "inox"),
            CY(xc, y_face + 0.3, y_face + 0.8, 18, 7, "ecran"), B(x0 + 1, y_face - 0.2, x1 - 1, y_face + 0.2, 31, 35, "gris")]


M = []
# --- séjour : mur de lattes de chêne, télé, sofa en L ; coin lecture près de la fenêtre (plus de table à manger)
M += [B(234 + 3 * i, 10, 236 + 3 * i, 11.6, 0, 89, "placage") for i in range(33)]
M += [B(250, 11.6, 322, 27, 0, 18, "placage"), B(258, 11.7, 314, 13, 30, 62, "ecran")]
M += [B(238, 40, 350, 132, 0, 0.4, "tapis")]
M += sofa(244, 98, 340, 136, "+y") + sofa(340, 66, 378, 136, "+x")
M += [B(268, 58, 318, 82, 13, 15, "placage"), B(270, 60, 272, 80, 0, 13, "metal"), B(314, 60, 316, 80, 0, 13, "metal")]
M += fauteuil(422, 52, "-y") + fauteuil(422, 124, "+y")
M += [C(422, 88, 10, 20, 22, "placage"), C(422, 88, 2, 0, 20, "metal"), C(440, 88, 1, 0, 60, "metal"), C(440, 88, 7, 54, 64, "abat-jour")]
M += [C(436, 20, 7, 0, 14, "osier"), C(436, 20, 9, 14, 44, "plante")]
# --- coin bar : armoires vert forêt, quartz veiné, zellige crème, tablettes de chêne éclairées, frigo pleine hauteur
M += [B(358, 207, 414, 227.75, 0, 4, "metal"), B(358, 205.75, 414, 227.75, 4, 34.5, "laque-vert"),
      B(357.5, 205, 414, 227.75, 34.5, 36, "quartz"),
      B(370, 210, 386, 222, 35.8, 36.1, "inox"),                                     # lavabo de bar
      B(377.5, 223.5, 378.5, 225, 36, 47, "laiton"), B(377.5, 217, 378.5, 225, 46, 47, "laiton"),
      B(357.5, 227.2, 414, 227.75, 36, 86, "zellige-vert"),
      B(360, 218, 412, 227.2, 52, 53.5, "placage"), B(360, 218, 412, 227.2, 68, 69.5, "placage"),
      B(360, 218.5, 412, 219, 51.5, 52, "spot"), B(360, 218.5, 412, 219, 67.5, 68, "spot")]
M += [C(363 + 4 * i, 223, 1.5, 53.5, 65, "verre-bouteille") for i in range(5)]
M += [C(392 + 4 * i, 223, 1.6, 69.5, 74, "verre-clair") for i in range(5)] + [C(392 + 4 * i, 223, 1.6, 53.5, 58, "verre-clair") for i in range(4)]
M += [B(414.5, 200, 444.5, 229, 0, 72, "inox"), B(414.5, 205, 444.5, 229, 72, 86, "laque-vert"), B(441, 199.5, 442, 200, 36, 66, "metal")]
# --- niche sous le palier du haut : banc et crochets (manteaux, sacs)
M += [B(280, 352, 312, 368, 0, 17, "placage"), B(280, 368.5, 312, 369.5, 60, 61, "metal")]
M += [B(284 + 8 * i, 366, 285 + 8 * i, 369.5, 58, 62, "laiton") for i in range(4)]
# --- salle d'entraînement vitrée : support à squat, banc, haltères, vélo face au séjour
M += [B(118, 10.2, 224, 10.8, 6, 84, "miroir")]
M += [B(x - 1.5, y - 1.5, x + 1.5, y + 1.5, 0, 86, "metal") for x in (168, 214) for y in (30, 74)]
M += [B(166.5, 28.5, 215.5, 31.5, 83, 86, "metal"), B(166.5, 72.5, 215.5, 75.5, 83, 86, "metal"),
      B(164, 22, 218, 82, 0, 1, "caoutchouc-noir"),
      B(184, 40, 198, 86, 14, 17, "caoutchouc-noir"), B(189, 48, 193, 80, 0, 14, "metal"), CX(160, 222, 52, 46, 0.6, "metal")]
M += [B(116, 30, 132, 100, 0, 6, "metal"), B(116, 30, 132, 100, 16, 17.5, "metal"), B(116, 30, 132, 100, 30, 31.5, "metal"),
      B(116, 30, 117, 100, 0, 31.5, "metal"), B(131, 30, 132, 100, 0, 31.5, "metal")]
M += [CX(118, 130, y, z, 2.4, "caoutchouc-noir") for y in range(36, 98, 9) for z in (20, 34)]
M += [B(206, 112, 216, 148, 0, 4, "metal"), B(210, 136, 212, 140, 4, 34, "metal"), C(211, 140, 5, 34, 38, "caoutchouc-noir"),
      B(210, 116, 212, 120, 4, 42, "metal"), B(203, 115, 219, 118, 42, 44, "caoutchouc-noir"), CY(211, 120, 124, 14, 10, "metal")]
M += [B(138, 104, 162, 136, 0, 0.3, "jete")]
# --- salle de lavage : laveuse et sécheuse frontales sous un comptoir de pliage en chêne de 8 pi, bac, armoires marine
M += appareil(12, 39, 10.5, 36.5) + appareil(41, 68, 10.5, 36.5)
M += [B(10, 10, 109.75, 37.5, 37, 38.5, "placage"),
      B(70, 11, 102, 35, 4, 37, "laque-marine"), B(70, 13, 102, 35, 0, 4, "metal"),
      B(76, 14, 96, 32, 38.4, 38.7, "inox"), B(85.5, 11, 86.5, 13, 38.5, 52, "metal"), B(85.5, 11, 86.5, 21, 51, 52, "metal"),
      B(10, 10, 70, 23, 54, 86, "laque-marine"), B(70, 10, 109.75, 20, 58, 59.5, "placage"), B(70, 10, 109.75, 20, 72, 73.5, "placage")]
M += [C(80, 15, 4.5, 59.5, 68, "osier"), C(92, 15, 4.5, 59.5, 68, "osier"), C(101, 15, 4.5, 73.5, 80, "osier")]
M += [B(85.75, 44, 109.75, 112, 0, 86, "laque-marine")] + [B(85.2, y, 85.75, y + 1, 30, 54, "laiton") for y in (76, 80)]
M += [C(28, 24, 7, 38.5, 48, "osier"), B(44, 16, 64, 32, 38.5, 42, "draps")]          # panier et linge plié
M += [CX(30, 80, y, 80, 0.5, "placage") for y in (66, 72, 78, 84)] + [B(30, 64, 31, 86, 80, 89.5, "metal"), B(79, 64, 80, 86, 80, 89.5, "metal")]
M += [C(34, 138, 11, 0, 58, "blanc"), B(10.2, 99, 14, 119, 40, 70, "gris")]            # chauffe-eau, panneau électrique
# --- salle de bain : bain en coin sous la fenêtre, douche walk-in de 6 pi, toilette contre la cloison, double vanité
M += [B(10.5, 159.5, 70, 189, 0, 20, "blanc"), B(13.5, 162.5, 67, 186, 19, 20.2, "eau"),             # bain 60 × 30
      B(10.5, 172, 13, 177, 24, 27, "metal"), B(10.5, 173.5, 16, 175.5, 25, 27, "metal"),            # bec mural noir
      B(10.25, 159.25, 70.25, 159.75, 20, 84, "tuile_blanche"), B(10.25, 159.25, 10.75, 189.25, 20, 56, "tuile_blanche"),
      B(10.25, 189, 70.25, 189.5, 0, 20, "tuile_blanche")]                                             # tablier carrelé
M += [B(70.25, 159.25, 72.25, 189.25, 0, 40, "tuile_blanche"), B(70.75, 159.5, 71.75, 189, 40, 76, "verre"),
      B(72, 159.3, 144, 159.8, 0, 84, "tuile_blanche"), B(143.2, 159.25, 143.7, 195, 0, 84, "tuile_blanche"),
      B(72, 159.25, 144, 195, 0, 0.5, "porcelaine"),
      B(72, 194.5, 112, 195.5, 0, 76, "verre"), B(111, 194.2, 112, 195.8, 0, 76, "metal"),
      C(108, 168, 5, 77, 77.6, "metal"), B(107.5, 159.8, 108.5, 168, 77, 78, "metal"),                  # pomme de douche
      B(112, 159.8, 124, 163.5, 44, 45, "metal")]                                                       # tablette
M += [B(31, 240, 49, 247.6, 14, 29, "blanc"), C(40, 230, 8, 0, 15, "blanc"), C(40, 230, 8.3, 15, 16, "blanc"),
      B(38, 240.5, 42, 241, 26, 28, "metal")]                                                           # toilette
M += [B(104, 233.75, 134, 247.75, 0, 84, "placage"), B(118.6, 233.2, 119.4, 233.75, 30, 54, "metal")]  # armoire à serviettes
M += [B(151, 225.75, 223, 247.75, 12, 32, "placage"), B(150.5, 225.25, 223.5, 247.75, 32, 33.5, "quartz"),
      C(169, 236, 7, 33.5, 38, "blanc"), C(205, 236, 7, 33.5, 38, "blanc"),
      B(168.5, 243, 169.5, 246, 33.5, 44, "metal"), B(204.5, 243, 205.5, 246, 33.5, 44, "metal"),
      B(157, 247.2, 181, 247.7, 42, 74, "miroir"), B(193, 247.2, 217, 247.7, 42, 74, "miroir")]
M += [B(60, 200, 100, 224, 0, 0.4, "tapis")]
# --- chambres
M += lit(110, 288, 170, 366) + table_chevet(92, 356) + table_chevet(188, 356) + [B(96, 270, 184, 368, 0, 0.4, "tapis")]
M += [B(37.5, 295, 39, 355, 0, 80, "placage")]
M += lit(352, 288, 412, 366) + table_chevet(340, 356) + table_chevet(424, 356) + [B(338, 272, 426, 368, 0, 0.4, "tapis")]
M += [B(391, 257.5, 439, 259, 0, 80, "placage")]
# --- rangement (ancien caveau) : étagères sur trois côtés
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
                 {"x": 170, "y": 60}, {"x": 170, "y": 125}, {"x": 50, "y": 60}, {"x": 60, "y": 120}, {"x": 70, "y": 185},
                 {"x": 187, "y": 228}, {"x": 118, "y": 310}, {"x": 380, "y": 300}, {"x": 252, "y": 280}, {"x": 296, "y": 350},
                 {"x": 273, "y": 408}, {"x": 296, "y": 270, "z": 185, "i": 7}],
    "visites": [{"nom": "Entrée", "x": 430, "y": 178, "cap": 168},
                {"nom": "Coin bar", "x": 372, "y": 164, "cap": 72},
                {"nom": "Escalier", "x": 296, "y": 168, "cap": 90},
                {"nom": "Séjour", "x": 300, "y": 150, "cap": 270},
                {"nom": "Gym (porte vitrée)", "x": 168, "y": 190, "cap": 270},
                {"nom": "Salle de lavage", "x": 70, "y": 128, "cap": 262},
                {"nom": "Salle de bain", "x": 132, "y": 206, "cap": 170},
                {"nom": "Bain et douche", "x": 92, "y": 228, "cap": 245},
                {"nom": "Double vanité", "x": 110, "y": 205, "cap": 20},
                {"nom": "Chambre 1", "x": 66, "y": 262, "cap": 35},
                {"nom": "Chambre 2", "x": 340, "y": 248, "cap": 40},
                {"nom": "Passage et rangement", "x": 252, "y": 300, "cap": 80}],
    "depart": {"x": 430, "y": 178, "cap": 168},
    "palette": [["Plancher", "chêne pâle, lames larges (vinyle de luxe) ; escalier en chêne massif, contremarches blanches", "#C9A97E"],
                ["Claustra de l'escalier", "lattes de chêne 1×2 du plancher au plafond : garde et lumière", "#B98E5E"],
                ["Coin bar", "armoires vert forêt, quartz blanc veiné, zellige vert lustré, tablettes de chêne éclairées, robinet laiton", "#34473B"],
                ["Salle de lavage", "terrazzo pâle, comptoir de pliage en chêne, armoires marine, bac inox, séchoir suspendu", "#2E3B4E"],
                ["Salle de bain", "porcelaine 24×24 pâle, tuile blanche lustrée, bain en coin, douche de 6 pi vitrée, vanité de chêne suspendue", "#D9D6D0"],
                ["Gym", "dalles de caoutchouc noir, murs anthracite, miroir pleine largeur, verre à cadre noir", "#2A2A2A"],
                ["Séjour", "sofa en tissu gris chaud, fauteuils en cuir cognac, tapis de laine crème", "#9A5B32"],
                ["Accents", "noir mat : cadres vitrés, robinetterie, luminaires ; laiton au bar", "#1E1E1E"]],
}
