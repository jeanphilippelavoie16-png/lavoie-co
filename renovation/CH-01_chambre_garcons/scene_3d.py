"""Maquette 3D de CH-01 : la chambre des garçons TOUTE SEULE (chambre avant du rez-de-chaussée et sa garde-robe), telle
qu'elle est aujourd'hui d'après les 12 photos du client (2026-11-09, renovation/prive/chambre_avant/, hors du dépôt).
Aucune photo n'est reproduite dans la page.

VERSION 2 (révision B, 2026-11-09), réponse du client : « Non mais je veux pas nécessairement de table, là tu m'as donné de
quoi de prémâché. Je veux de l'espace de rangement et un coin jeu. Je veux aussi changer les couleurs et mettre un thème plus
genre enfant [4 et 6] ans. » et « enfant mais genre moderne, pas genre Avengers... mais que ça reste enfant, cool mais
moderne ».

Gardé de l'existant : les lits superposés (le long du mur arrière, tête au mur de gauche) et la commode blanche (mur de
droite, près de la fenêtre), l'enveloppe (fenêtre à 3 châssis et petits carreaux, chambranles et portes de pin teint,
plinthes chauffantes, plancher d'érable, suspension cage) et les deux enseignes de bois à leurs noms (remontées dans le ciel
de la murale). Enlevés : la table à Lego et les tabourets de la version 1, le panache d'orignal (il ne va pas avec le thème),
le vert forêt du mur de gauche.
Proposé (voir DESIGN.md, « Version 2 ») : thème « Camp de base » (murale graphique de montagnes en aplats, jour côté
fenêtre, nuit étoilée côté lits : murale.py) ; RANGEMENT : 3 bacs roulants sous le lit du bas (on les touche : ils sortent),
armoires fermées au-dessus de la commode (parents), livres de face à leur hauteur, tablette haute de chêne et ses boîtes,
tour aux albums au coin de la porte, patères, garde-robe aménagée (gardée) ; COIN JEU OUVERT : grand tapis plat, deux
coussins de sol, des Lego au plancher.

Repères et dimensions : geometrie.py (partagé avec modifs.py et le plan P-131). Pouces, repère de la maison (x le long de
la façade, y vers l'arrière, z depuis le plancher). Toutes les dimensions de l'existant sont ESTIMÉES sur les photos.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geometrie as G  # noqa: E402
import murale as MU  # noqa: E402

TITRE = "CH-01 — Chambre des garçons"




# --------------------------------------------------------------------------------------------------- formes
def B(x0, y0, x1, y1, z0, z1, mat, **k):
    return dict({"forme": "boite", "x0": x0, "y0": y0, "x1": x1, "y1": y1, "z0": z0, "z1": z1, "mat": mat}, **k)


def A(x0, y0, x1, y1, z0, z1, mat, r=3, b=0.5, trou=None, **k):
    """Bloc à coins arrondis en plan et arêtes adoucies ; trou = épaisseur de paroi (bac creux)."""
    o = {"forme": "arrondi", "x0": x0, "y0": y0, "x1": x1, "y1": y1, "z0": z0, "z1": z1, "mat": mat, "r": r, "b": b}
    if trou:
        o["trou"] = trou
    return dict(o, **k)


def C(x, y, r, z0, z1, mat, **k):
    return dict({"forme": "cylindre", "x": x, "y": y, "r": r, "z0": z0, "z1": z1, "mat": mat}, **k)


def CX(x0, x1, y, z, r, mat, **k):
    return dict({"forme": "cylindre", "axe": "x", "x0": x0, "x1": x1, "y": y, "z": z, "r": r, "mat": mat}, **k)


def CY(x, y0, y1, z, r, mat, **k):
    return dict({"forme": "cylindre", "axe": "y", "x": x, "y0": y0, "y1": y1, "z": z, "r": r, "mat": mat}, **k)


def T(pts, r, mat, **k):
    return dict({"forme": "tube", "pts": [list(p) for p in pts], "r": r, "mat": mat}, **k)


def SPH(x, y, z, r, mat, **k):
    return dict({"forme": "sphere", "x": x, "y": y, "z": z, "r": r, "mat": mat}, **k)


def TOR(x, y, z, R, r, mat, **k):
    return dict({"forme": "tore", "x": x, "y": y, "z": z, "R": R, "r": r, "mat": mat}, **k)


def TXT(texte, x, y, z0, z1, larg, face, couleur, police="sans", **k):
    """Texte peint ou gravé (forme « texte » du moteur, voir generer_3d.textes_mobilier)."""
    return dict({"forme": "texte", "texte": texte, "x": x, "y": y, "z0": z0, "z1": z1, "larg": larg, "face": face,
                 "couleur": couleur, "police": police}, **k)



PIN = "pin_teint"          # portes, chambranles, plinthes de pin teint foncé (catalogue, comme RDC-01)
CHENE = "placage"          # chêne pâle du rangement (et du lit superposé, bois naturel)
NOIR = "noir-mat"
BLANC = "blanc"            # commode, caissons et cadres de fenêtre (blanc satiné)
BLANC_MAT = "blanc-mat"    # panneaux du lit superposé
COUL_BACS = ("sauge", "sable", "terracotta", "ciel-matin", "moutarde", "bleu-fjord")
COUL_LIVRES = ("corail", "ciel", "pomme", "prune", "moutarde", "bleu-fjord", "terracotta", "sauge")

M = []


# =============================================================================================== enveloppe (existant)
# --- fenêtre de façade : chambranle plat de pin teint (coins d'onglet), embrasure blanche, deux caissons de stores noirs
F0, F1, AL, TE, CH = G.FEN[0], G.FEN[1], G.ALLEGE, G.TETE, G.CHAMBRANLE
YM = G.YF                                                  # nu intérieur de la façade
M += [A(F0 - CH, YM, F0, YM + 1.0, AL - CH, TE + CH, PIN, r=0.15, b=0.12),            # montants
      A(F1, YM, F1 + CH, YM + 1.0, AL - CH, TE + CH, PIN, r=0.15, b=0.12),
      A(F0 - CH, YM, F1 + CH, YM + 1.0, TE, TE + CH, PIN, r=0.15, b=0.12),              # tête
      A(F0 - CH, YM, F1 + CH, YM + 1.3, AL - CH, AL, PIN, r=0.15, b=0.12)]              # bas (couvre la tablette)
for xa, xb, za, zb, y in ((F0 - CH, F0, TE + CH, TE, YM + 1.02), (F1 + CH, F1, TE + CH, TE, YM + 1.02),
                          (F0 - CH, F0, AL - CH, AL, YM + 1.32), (F1 + CH, F1, AL - CH, AL, YM + 1.32)):
    M.append(T([(xa, y, za), (xb, y, zb)], 0.05, "carbone"))                              # joints d'onglet
# embrasure blanche (les retours de pin du moteur et sa tablette restent derrière)
M += [B(F0 + 0.5, YM - 3.75, F0 + 0.6, YM, AL + 0.1, TE - 0.5, BLANC), B(F1 - 0.6, YM - 3.75, F1 - 0.5, YM, AL + 0.1, TE - 0.5, BLANC),
      B(F0, YM - 3.75, F1, YM, TE - 0.6, TE - 0.5, BLANC), B(F0, YM - 3.75, F1, YM + 0.02, AL, AL + 0.08, BLANC)]
# manivelle du châssis de droite vu de l'intérieur (x bas) et levier de verrouillage
xm = F0 + (F1 - F0) / 3
M += [B(F0 + 6, YM - 3.2, F0 + 9.5, YM - 2.6, AL + 1.6, AL + 2.6, BLANC), B(F0 + 7, YM - 2.7, F0 + 8.2, YM - 1.3, AL + 1.8, AL + 2.4, BLANC),
      B(xm - 1.6, YM - 3.4, xm - 1.0, YM - 2.7, AL + 18, AL + 22.5, BLANC)]
# caissons de stores enrouleurs noirs (photos 02, 10, 12), au-dessus du chambranle
M += [A(F0 - 8.0, YM, F1 + 7.5, YM + 4.5, TE + CH + 0.6, TE + CH + 5.0, NOIR, r=0.6, b=0.3),
      A(F0 - 9.0, YM, F1 + 7.75, YM + 3.5, TE + CH + 6.4, TE + CH + 8.7, NOIR, r=0.6, b=0.3)]
M += [B(x, YM, x + 0.6, YM + 1.6, TE + CH + 5.0, TE + CH + 6.4, NOIR) for x in (F0 - 4, (F0 + F1) / 2, F1 + 3.5)]


# --- plinthes chauffantes électriques blanches (≈ 3 po de profond, 7½ po de haut)
def plinthe_chauffante(x0, y0, x1, y1):
    le_long_x = (x1 - x0) > (y1 - y0)
    z0, z1 = G.PC_Z
    out = [A(x0, y0, x1, y1, z0, z1, BLANC, r=0.4, b=0.3)]
    if le_long_x:                                            # grille du dessus et embouts
        out += [B(x0 + 3, y0 + 0.7, x1 - 3, y1 - 0.9, z1 - 0.02, z1 + 0.02, "carbone"),
                A(x0 - 0.2, y0 - 0.1, x0 + 2.2, y1 + 0.2, z0 - 0.1, z1 + 0.2, BLANC, r=0.3, b=0.2),
                A(x1 - 2.2, y0 - 0.1, x1 + 0.2, y1 + 0.2, z0 - 0.1, z1 + 0.2, BLANC, r=0.3, b=0.2),
                B(x0 + 3, y1, x1 - 3, y1 + 0.05, z0 + 0.6, z0 + 1.1, "gris")]
    else:
        out += [B(x0 + 0.7, y0 + 3, x1 - 0.9, y1 - 3, z1 - 0.02, z1 + 0.02, "carbone"),
                A(x0 - 0.1, y0 - 0.2, x1 + 0.2, y0 + 2.2, z0 - 0.1, z1 + 0.2, BLANC, r=0.3, b=0.2),
                A(x0 - 0.1, y1 - 2.2, x1 + 0.2, y1 + 0.2, z0 - 0.1, z1 + 0.2, BLANC, r=0.3, b=0.2),
                B(x1, y0 + 3, x1 + 0.05, y1 - 3, z0 + 0.6, z0 + 1.1, "gris")]
    return out


M += plinthe_chauffante(*G.PC_AVANT) + plinthe_chauffante(*G.PC_GAUCHE)


# --- portes de pin teint à panneaux horizontaux, bouton rond et pentures noirs (photos 04, 05, 11, 12) ; ces objets
#     portent "porte" : ils pivotent avec le vantail du moteur (décrits porte fermée)
RAILS = ((0.5, 9.5), (19.9, 23.4), (33.8, 37.3), (47.7, 51.2), (61.6, 65.1), (75.5, 80.0))   # 5 panneaux horizontaux


def moulures(face, a0, a1, mat=PIN):
    """Montants et traverses en saillie de ¼ po sur une face du vantail : face(s0, s1, z0, z1) construit la boîte entre
    s0 et s1 le long de la porte ; a0, a1 = bords du vantail."""
    out = [face(a0, a0 + 4.5, 0.5, 80), face(a1 - 4.5, a1, 0.5, 80)]
    out += [face(a0 + 4.5, a1 - 4.5, z0, z1) for z0, z1 in RAILS]
    return out


def bouton(axe, s, c0, sens, z=37.0):
    """Bouton rond noir : rosace sur la face (c0), col, boule ; sens = +1 ou -1 (vers où il dépasse) ; il enferme la
    béquille dessinée par le moteur."""
    if axe == "y":       # porte dans un mur parallèle à x : le bouton dépasse en y
        return [CY(s, *sorted((c0, c0 + sens * 0.5)), z, 1.3, NOIR), CY(s, *sorted((c0 + sens * 0.5, c0 + sens * 1.25)), z, 1.15, NOIR),
                SPH(s, c0 + sens * 2.05, z, 1.25, NOIR)]
    return [CX(*sorted((c0, c0 + sens * 0.5)), s, z, 1.3, NOIR), CX(*sorted((c0 + sens * 0.5, c0 + sens * 1.25)), s, z, 1.15, NOIR),
            SPH(c0 + sens * 2.05, s, z, 1.25, NOIR)]


def porte_chambre():
    """Porte de la chambre (ouv-RDC-014) : vantail du moteur x 112,5 → 141,5, y 154,75 → 156,55 ; charnière à x = 142."""
    pid, a0, a1 = "ouv-RDC-014", 112.5, 141.5
    out = moulures(lambda s0, s1, z0, z1: B(s0, 154.5, s1, 154.75, z0, z1, PIN), a0, a1)
    out += moulures(lambda s0, s1, z0, z1: B(s0, 156.55, s1, 156.8, z0, z1, PIN), a0, a1)
    out += bouton("y", 116.0, 154.75, -1) + bouton("y", 116.0, 156.55, +1)
    out += [B(140.9, 154.35, 141.9, 154.75, z, z + 3.5, NOIR) for z in (8, 38, 69)]           # pentures
    return [dict(o, porte=pid) for o in out]


def porte_garde_robe():
    """Porte de la garde-robe (ouv-RDC-021) : vantail x 143,75 → 145,55, y 78,5 → 107,5 ; charnière à y = 78."""
    pid, a0, a1 = "ouv-RDC-021", 78.5, 107.5
    out = moulures(lambda s0, s1, z0, z1: B(143.5, s0, 143.75, s1, z0, z1, PIN), a0, a1)
    out += moulures(lambda s0, s1, z0, z1: B(145.55, s0, 145.8, s1, z0, z1, PIN), a0, a1)
    out += bouton("x", 104.0, 143.75, -1) + bouton("x", 104.0, 145.55, +1)
    out += [B(143.35, 78.1, 143.75, 79.1, z, z + 3.5, NOIR) for z in (8, 38, 69)]
    return [dict(o, porte=pid) for o in out]


M += porte_chambre() + porte_garde_robe()
# chambranles larges de pin teint (≈ 4½ po, photos 05, 06) par-dessus ceux de 2½ po du moteur, côté chambre
y0g, y1g = G.PORTE_GR
M += [A(143.0, y0g - CH, 143.75, y0g, 0, 80 + CH, PIN, r=0.15, b=0.12), A(143.0, y1g, 143.75, y1g + CH, 0, 80 + CH, PIN, r=0.15, b=0.12),
      A(143.0, y0g - CH, 143.75, y1g + CH, 80, 80 + CH, PIN, r=0.15, b=0.12)]
M += [T([(142.98, y0g - CH, 80 + CH), (142.98, y0g, 80)], 0.05, "carbone"), T([(142.98, y1g + CH, 80 + CH), (142.98, y1g, 80)], 0.05, "carbone")]
M += [A(G.NICHE[0], 154.0, G.NICHE[2], 154.75, 80, 80 + CH, PIN, r=0.15, b=0.12),                # tête de la porte de la chambre
      A(G.NICHE[0], 154.0, 112.0, 154.75, 0, 80, PIN, r=0.15, b=0.12), A(142.0, 154.0, G.NICHE[2], 154.75, 0, 80, PIN, r=0.15, b=0.12)]

# fond du dégagement vu par la porte ouverte (décor neutre, hors du plan) : plancher, murs et plafond
M += [B(104, 159.25, 152, 190, -0.4, 0, "erable"), B(102, 159.25, 104, 190, 0, 86, "blanc-chaud"),
      B(152, 159.25, 154, 190, 0, 86, "blanc-chaud"), B(102, 190, 154, 192, 0, 86, "blanc-chaud"),
      B(102, 159.25, 154, 192, 86, 86.5, "blanc-chaud"), B(104, 189.5, 152, 190, 0, 4, PIN)]

# --- suspension cage de fil noir à chapeau de bois, au centre (photos 06 à 10)
XC, YC = (G.XG + G.XD) / 2, (G.YF + G.YA) / 2
M += [C(XC, YC, 2.4, 95.2, 96, NOIR), C(XC, YC, 0.15, 85.5, 95.2, "carbone"),
      C(XC, YC, 2.2, 84.6, 86.0, CHENE, r2=1.0), C(XC, YC, 3.3, 83.2, 84.6, CHENE),
      SPH(XC, YC, 80.3, 1.7, "abat-jour"), C(XC, YC, 0.7, 81.6, 83.2, "laiton")]
M += [TOR(XC, YC, 83.0, 3.3, 0.12, "carbone", axe="z"), TOR(XC, YC, 77.0, 5.0, 0.12, "carbone", axe="z"),
      TOR(XC, YC, 73.2, 4.4, 0.12, "carbone", axe="z")]
for k in range(8):
    a = k * math.pi / 4 + math.pi / 8
    M.append(T([(XC + 3.3 * math.cos(a), YC + 3.3 * math.sin(a), 83.0), (XC + 5.0 * math.cos(a), YC + 5.0 * math.sin(a), 77.0),
                (XC + 4.4 * math.cos(a), YC + 4.4 * math.sin(a), 73.2)], 0.11, "carbone"))
M += [T([(XC - 4.4, YC, 73.2), (XC + 4.4, YC, 73.2)], 0.11, "carbone"), T([(XC, YC - 4.4, 73.2), (XC, YC + 4.4, 73.2)], 0.11, "carbone")]


# --- mur de gauche (l'ancien mur vert) : murale « Camp de base » peinte (image plane, dessinée par murale.py) ; les deux
#     enseignes de planches gravées (photos 03, 07 à 09) sont gardées et remontées dans le ciel de la murale ; le panache
#     d'orignal est retiré (il ne va pas avec le thème : voir DESIGN.md)
IMAGE_MURALE = MU.ecrire()
my0, my1, mz0, mz1 = G.MURALE
M.append({"forme": "image", "cle": "murale_camp", "x": G.XG + 0.25, "y": (my0 + my1) / 2, "z0": mz0, "z1": mz1,
          "larg": my1 - my0, "face": "+x"})
DY, DZ = G.ENSEIGNES_DY, G.ENSEIGNES_DZ
PLANCHES_PA = ((66.5, 100.5, 66.6, 69.9), (64.5, 102.5, 63.2, 66.5), (65.5, 101.0, 59.8, 63.1), (67.5, 101.5, 56.4, 59.7))
PLANCHES_LC = ((57.5, 94.5, 46.3, 50.5), (56.0, 95.5, 42.0, 46.2), (58.0, 93.5, 37.7, 41.9))
M += [A(G.XG, a + DY, G.XG + 0.75, b + DY, c + DZ, d + DZ, PIN, r=0.2, b=0.12) for a, b, c, d in PLANCHES_PA]
M += [A(G.XG, a + DY, G.XG + 0.75, b + DY, c + DZ, d + DZ, CHENE, r=0.2, b=0.12) for a, b, c, d in PLANCHES_LC]
M += [TXT("Pierre-Alexis", G.XG + 0.8, 84.0 + DY, 57.6 + DZ, 68.6 + DZ, 32.0, "+x", "#ECDCBC", "script", gras=True),
      TXT("Louis-Charles", G.XG + 0.8, 75.7 + DY, 38.6 + DZ, 49.4 + DZ, 34.0, "+x", "#4A2C1B", "script", gras=True)]
M += [B(G.XG + 0.75, y + DY, G.XG + 0.85, y + DY + 0.5, z + DZ, z + DZ + 0.5, "laiton")
      for y, z in ((70, 68.5), (98, 68.5), (61, 49.2), (91, 49.2))]

# =============================================================================================== lits superposés (gardés)
X0, Y0, X1, Y1 = G.LITS


def lits_superposes():
    """Simple sur simple, panneaux blancs et montants de bois naturel, échelle de bois inclinée (photos 05 à 09, 12).
    Dimensions ESTIMÉES : ≈ 80½ × 43 po, garde-corps du haut à ≈ 63 po."""
    out = []
    for x, y in ((X0, Y0), (X0, Y1 - 2.75), (X1 - 2.25, Y0), (X1 - 2.25, Y1 - 2.75)):           # montants
        out.append(A(x, y, x + 2.25, y + 2.75, 0, 48.5, CHENE, r=0.5, b=0.3))
    for z0, z1 in ((8.0, 12.5), (44.0, 48.5)):                                                    # cadres des deux lits
        out += [B(X0 + 2.25, Y0 + 0.25, X1 - 2.25, Y0 + 1.75, z0, z1, CHENE), B(X0 + 2.25, Y1 - 1.75, X1 - 2.25, Y1 - 0.25, z0, z1, CHENE),
                B(X0 + 0.25, Y0 + 2.75, X0 + 1.75, Y1 - 2.75, z0, z1, CHENE), B(X1 - 1.75, Y0 + 2.75, X1 - 0.25, Y1 - 2.75, z0, z1, CHENE),
                B(X0 + 2.25, Y0 + 1.75, X1 - 2.25, Y1 - 1.75, z1 - 1.5, z1 - 0.5, CHENE)]
    # panneaux blancs : bouts du lit du bas, bouts du lit du haut (plus hauts, avec une fente), garde-corps du haut
    out += [A(X0 + 0.5, Y0 + 2.75, X0 + 1.25, Y1 - 2.75, 12.5, 29.5, BLANC_MAT, r=0.3, b=0.15),
            A(X1 - 1.25, Y0 + 2.75, X1 - 0.5, Y1 - 2.75, 12.5, 26.5, BLANC_MAT, r=0.3, b=0.15),
            A(X0 + 0.5, Y0, X0 + 1.25, Y1, 46.0, 64.5, BLANC_MAT, r=0.3, b=0.15),
            A(X1 - 1.25, Y0, X1 - 0.5, Y1, 46.0, 64.5, BLANC_MAT, r=0.3, b=0.15),
            A(X0 + 2.25, Y0 + 0.25, 60.0, Y0 + 1.0, 48.5, 63.0, BLANC_MAT, r=0.3, b=0.15),
            A(78.0, Y0 + 0.25, X1 - 2.25, Y0 + 1.0, 48.5, 64.5, BLANC_MAT, r=0.3, b=0.15),
            A(X0 + 2.25, Y1 - 1.0, X1 - 2.25, Y1 - 0.25, 48.5, 63.0, BLANC_MAT, r=0.3, b=0.15)]
    out += [B(X0 + 0.45, Y0 + 9, X0 + 1.3, Y0 + 25, 22.5, 24.8, "carbone"),                       # fentes (deux faces)
            B(X0 + 0.45, Y0 + 7, X0 + 1.3, Y0 + 24, 59.0, 61.2, "carbone"),
            B(X0 + 6, Y0 + 0.2, X0 + 27, Y0 + 1.05, 58.4, 60.4, "carbone"),
            CY(51.5, Y0 + 0.1, Y0 + 1.15, 56.0, 0.45, "bleu-brume"), CX(X0 + 0.4, X0 + 1.35, Y0 + 32, 55.5, 0.45, "bleu-brume")]
    # matelas (draps-housses moutarde), oreillers, couettes pliées au pied
    for zm, couette in ((12.0, "jete"), (48.0, "sable")):
        out += [A(X0 + 2.5, Y0 + 2.0, X1 - 2.5, Y1 - 2.0, zm, zm + 6.0, "moutarde", r=2, b=1.2),
                A(X0 + 3.0, Y0 + 9.0, X0 + 16.0, Y1 - 9.0, zm + 6.0, zm + 9.5, "draps", r=3, b=1.4),
                A(X1 - 24.0, Y0 + 2.5, X1 - 3.5, Y1 - 2.5, zm + 6.0, zm + 9.0, couette, r=2.5, b=1.2)]
    # échelle de bois inclinée : pied à y = 74,5, haut accroché au cadre du lit du haut
    e0, e1, yp = G.ECHELLE
    xa, xb, zh, yh = e0 + 0.75, e1 - 0.75, 58.5, Y0 + 0.75
    out += [T([(xa, yp, 0.4), (xa, yh, zh)], 0.85, CHENE, bouts=True), T([(xb, yp, 0.4), (xb, yh, zh)], 0.85, CHENE, bouts=True)]
    for z in (12, 24, 36, 48):
        y = yp + (yh - yp) * z / zh
        out.append(B(xa, y - 1.3, xb, y + 1.3, z - 0.55, z + 0.55, CHENE))
    out += [B(x - 0.7, Y0 + 0.2, x + 0.7, Y0 + 2.0, 47.6, 49.4, "metal") for x in (xa, xb)]          # crochets
    return out


M += lits_superposes()

# =============================================================================================== commode blanche (gardée)
cx0, cy0, cx1, cy1 = G.COMMODE


def commode():
    """Commode blanche basse : 2 colonnes de 3 tiroirs à poignées encastrées, pattes de métal gris (photos 04, 05, 12).
    ≈ 48 × 16 × 27 po (ESTIMÉ). À ancrer au mur (courroie anti-basculement)."""
    h = G.COMMODE_H
    out = [A(cx0 + 0.5, cy0, cx1 - 0.25, cy1, 3.5, h, BLANC, r=0.25, b=0.2)]
    for ya, yb in ((cy0 + 0.4, (cy0 + cy1) / 2 - 0.2), ((cy0 + cy1) / 2 + 0.2, cy1 - 0.4)):
        for za, zb in ((4.0, 11.4), (11.8, 19.2), (19.6, 26.6)):
            yc = (ya + yb) / 2
            out += [A(cx0, ya, cx0 + 0.55, yb, za, zb, BLANC, r=0.15, b=0.1),
                    B(cx0 - 0.05, yc - 3.2, cx0 + 0.05, yc + 3.2, zb - 1.15, zb - 0.35, "carbone")]
    for x, y in ((cx0 + 1.8, cy0 + 1.6), (cx0 + 1.8, cy1 - 1.6), (cx1 - 1.8, cy0 + 1.6), (cx1 - 1.8, cy1 - 1.6)):
        out.append(C(x, y, 0.55, 0, 3.5, "gris"))
    # dessus : un album posé, une veilleuse
    out += [B(cx0 + 2.5, 50, cx0 + 11.5, 59, h, h + 0.45, "ciel"), B(cx0 + 3, 50.5, cx0 + 11, 58.5, h + 0.45, h + 0.5, "blanc-chaud"),
            C(cx0 + 8, 25, 1.6, h, h + 0.6, CHENE), SPH(cx0 + 8, 25, h + 2.2, 1.7, "abat-jour")]
    return out


M += commode()

# =============================================================================================== livres, briques, étiquettes
rng = random.Random(131)
LEGO = ("lego-rouge", "lego-bleu", "lego-jaune", "lego-vert", "lego-blanc", "lego-orange")


def couverture(xf, y0, y1, z0, z1, c1, c2):
    """Album présenté de face (couverture vers −x, sur un rebord du mur de droite) : couleur, illustration, titre."""
    yc = (y0 + y1) / 2
    return [B(xf, y0, xf + 0.45, y1, z0, z1, c1),
            B(xf - 0.04, y0 + 0.9, xf, y1 - 0.9, z0 + 1.5, z1 - 3.0, c2),
            B(xf - 0.06, y0 + 1.2, xf - 0.02, y1 - 1.2, z1 - 2.4, z1 - 1.2, "blanc-chaud"),
            CX(xf - 0.09, xf - 0.04, yc + rng.uniform(-1.5, 1.5), z0 + rng.uniform(3.5, 5.5), rng.uniform(1.0, 1.8), rng.choice(COUL_LIVRES))]


def rebords_livres():
    """Deux rebords à livres de face en chêne (48 × 4 po, lèvre de 1½ po) au-dessus de la commode, à 34 et 45½ po :
    couvertures à la hauteur des gars ; le dessus de la commode sert de comptoir pour poser le livre choisi."""
    x0, x1, zs = G.REBORDS
    ya, yb = G.REBORDS_Y
    out = []
    for z in zs:
        out += [A(x0, ya, x1, yb, z - 0.75, z, CHENE, r=0.2, b=0.12), A(x0, ya, x0 + 0.75, yb, z, z + 1.6, CHENE, r=0.2, b=0.12),
                B(x1 - 0.5, ya + 0.5, x1, yb - 0.5, z - 2.5, z - 0.75, CHENE)]
        y = ya + rng.uniform(0.8, 2.0)
        while True:
            w, hh = rng.uniform(8.0, 10.5), rng.uniform(8.5, 11.0)
            if y + w > yb - 0.6:
                break
            c1, c2 = rng.sample(COUL_LIVRES, 2)
            out += couverture(x0 + 0.85, y, y + w, z, z + hh, c1, c2)
            y += w + rng.uniform(0.6, 2.2)
    return out


def brique(x, y, z, nx, ny, mat, h=0.45):
    """Brique de Lego : nx × ny tenons (5/16 po), quelques tenons dessus."""
    p = 0.315
    out = [B(x, y, x + nx * p, y + ny * p, z, z + h, mat)]
    if nx * ny <= 8:
        out += [C(x + (i + 0.5) * p, y + (j + 0.5) * p, 0.1, z + h, z + h + 0.07, mat) for i in range(nx) for j in range(ny)]
    return out



def etiquette(x, y, z, face, texte, larg=7.0):
    """Étiquette blanche avec pictogramme et mot, sur la face avant d'un bac (face = "-x" ou "-y")."""
    if face == "-y":
        return [B(x - larg / 2, y - 0.08, x + larg / 2, y, z - 1.25, z + 1.25, "blanc"),
                TXT(texte, x, y - 0.13, z - 1.05, z + 1.05, larg - 0.6, "-y", "#2B2D30", "sans", gras=True)]
    return [B(x - 0.08, y - larg / 2, x, y + larg / 2, z - 1.25, z + 1.25, "blanc"),
            TXT(texte, x - 0.13, y, z - 1.05, z + 1.05, larg - 0.6, "-x", "#2B2D30", "sans", gras=True)]


# =============================================================================================== rangement (proposé, version 2)
def bac_roulant(cid, x0, x1, mot, coul, contenu):
    """Bac roulant bas sous le lit du bas : caisse de bouleau, façade de couleur à prise ronde, étiquette (pictogramme + mot),
    4 roulettes. Décrit RANGÉ (face avant sous la traverse du lit) ; on le touche : il sort de BACS_COURSE vers le tapis."""
    y0, y1 = G.BACS_Y
    h, zr = G.BACS_H, 1.0                                                    # roulettes de 1 po
    xc = (x0 + x1) / 2
    out = [A(x0, y0 + 0.75, x1, y1, zr, h, CHENE, r=0.4, b=0.15, trou=0.5),                  # caisse creuse
           B(x0 + 0.4, y0 + 0.9, x1 - 0.4, y1 - 0.4, zr, zr + 0.5, CHENE),                   # fond
           A(x0, y0, x1, y0 + 0.75, zr - 0.2, h, coul, r=0.35, b=0.15),                      # façade de couleur
           CY(xc, y0 - 0.1, y0 + 0.3, h - 1.25, 0.85, "carbone")]                             # prise ronde
    out += etiquette(xc, y0 - 0.02, zr + 1.9, "-y", mot, min(9.0, x1 - x0 - 2.0))
    for x in (x0 + 1.6, x1 - 1.6):
        for y in (y0 + 2.2, y1 - 2.2):
            out += [CX(x - 0.45, x + 0.45, y, 0.5, 0.5, NOIR), B(x - 0.6, y - 0.6, x + 0.6, y + 0.6, 0.95, zr, "gris")]
    out += contenu(x0 + 1.0, y0 + 1.6, x1 - 1.0, y1 - 1.0, zr + 0.5)
    return [dict(o, commande=cid, anim="glisser") for o in out]


def _lego_vrac(x0, y0, x1, y1, z):
    out = []
    for k in range(26):
        out += brique(rng.uniform(x0, x1 - 2.6), rng.uniform(y0, y1 - 1.4), z + 0.45 * (k % 4), rng.choice((2, 4, 6)), 2, rng.choice(LEGO))
    return out


def _autos(x0, y0, x1, y1, z):
    out = []
    for k, (u, v) in enumerate(((0.25, 0.2), (0.7, 0.35), (0.3, 0.6), (0.68, 0.78), (0.35, 0.88))):
        x, y = x0 + u * (x1 - x0), y0 + v * (y1 - y0)
        c = ("lego-rouge", "bleu-fjord", "moutarde", "lego-vert", "terracotta")[k]
        out += [A(x - 1.3, y - 2.6, x + 1.3, y + 2.6, z + 0.4, z + 1.5, c, r=0.5, b=0.25),
                A(x - 1.1, y - 1.2, x + 1.1, y + 1.0, z + 1.5, z + 2.3, c, r=0.4, b=0.2)]
        out += [CX(x - 1.45, x + 1.45, y + dy, z + 0.45, 0.45, NOIR) for dy in (-1.6, 1.6)]
    out += [B(x0 + 0.5, y0 + 6, x1 - 0.5, y0 + 10, z, z + 0.3, "carbone")]                    # bout de piste
    return out


def _dinos(x0, y0, x1, y1, z):
    out = []
    for k, (u, v, c) in enumerate(((0.5, 0.18, "pomme"), (0.45, 0.48, "terracotta"), (0.55, 0.78, "moutarde"))):
        x, y = x0 + u * (x1 - x0), y0 + v * (y1 - y0)
        out += [SPH(x, y, z + 1.4, 1.5, c, ecrase=0.7), SPH(x, y - 2.0, z + 2.2, 0.75, c),            # corps, tête
                T([(x, y + 1.2, z + 1.4), (x + 0.3, y + 3.4, z + 0.7)], 0.4, c, bouts=True)]          # queue
        out += [C(x + dx, y + dy, 0.3, z, z + 1.0, c) for dx in (-0.7, 0.7) for dy in (-0.6, 0.6)]
    return out


def bacs_sous_le_lit():
    noms = (("bac-lego", "🧱 LEGO", "moutarde", _lego_vrac), ("bac-autos", "🚗 AUTOS", "terracotta", _autos),
            ("bac-dinos", "🦕 DINOS", "sauge", _dinos))
    out = []
    for (x0, x1), (cid, mot, coul, contenu) in zip(G.BACS_X, noms):
        out += bac_roulant(cid, x0, x1, mot, coul, contenu)
    return out


def armoires_hautes():
    """Deux armoires murales au-dessus de la commode (2 portes de 24 po, 12 po de profond, z 57 → 84) : le rangement fermé
    des parents (jouets en rotation, grandeur suivante, souvenirs). Caisson blanc comme la commode, portes bleu fjord, petits
    boutons noirs, loquets de sécurité ; vissées dans les montants. Les livres de face restent dessous, à leur hauteur."""
    x0, y0, x1, y1 = G.ARMOIRES
    z0, z1 = G.ARMOIRES_Z
    ym = (y0 + y1) / 2
    out = [A(x0 + 0.75, y0, x1, y1, z0, z1, BLANC, r=0.2, b=0.12)]
    for ya, yb, yb_ in ((y0 + 0.12, ym - 0.06, ym - 2.2), (ym + 0.06, y1 - 0.12, ym + 2.2)):
        out += [A(x0, ya, x0 + 0.8, yb, z0 + 0.12, z1 - 0.12, "bleu-fjord", r=0.25, b=0.15),
                CX(x0 - 0.6, x0, yb_, z0 + 2.6, 0.3, NOIR), SPH(x0 - 0.75, yb_, z0 + 2.6, 0.45, NOIR)]
    return out


def tablette_haute():
    """Tablette haute de chêne (11 po, flottante sur supports cachés) de la fenêtre à la porte de la chambre, au-dessus des
    armoires et de la porte de la garde-robe : 6 boîtes de lin à couvercle (parents : souvenirs, jeux en rotation)."""
    x0, y0, x1, y1 = G.TABLETTE_HAUTE
    z = G.TABLETTE_HAUTE_Z
    out = [A(x0, y0, x1, y1, z, z + 1.5, CHENE, r=0.3, b=0.15)]
    for ya in (19.0, 34.5, 50.0, 71.0, 86.0, 101.0):
        yb = ya + 14.0
        out += [A(x0 + 0.75, ya, x1 - 0.5, yb, z + 1.5, z + 8.4, "sable", r=0.6, b=0.25),
                A(x0 + 0.6, ya - 0.1, x1 - 0.4, yb + 0.1, z + 8.4, z + 9.0, "sable", r=0.6, b=0.2),
                B(x0 + 0.55, (ya + yb) / 2 - 1.6, x0 + 0.8, (ya + yb) / 2 + 1.6, z + 5.6, z + 6.6, "terracotta")]
    return out


def pateres():
    """Latte de chêne et 3 patères à leur hauteur (pyjamas, tuques, sac d'école), entre la garde-robe et la porte."""
    y0, y1, z = G.PATERES
    out = [A(G.XD - 0.75, y0, G.XD, y1, z - 1.75, z + 1.75, CHENE, r=0.2, b=0.12)]
    for y in (y0 + 1.5, (y0 + y1) / 2, y1 - 1.5):
        out += [CX(G.XD - 3.0, G.XD - 0.75, y, z, 0.45, CHENE), SPH(G.XD - 3.1, y, z, 0.62, CHENE)]
    out += [SPH(G.XD - 3.4, y0 + 1.5, z - 2.9, 2.5, "moutarde", ecrase=0.85), SPH(G.XD - 3.4, y0 + 1.5, z - 0.7, 0.8, "neige")]   # tuque
    return out


def tour_albums():
    """Tour aux albums (17½ × 12¾ × 42 po) au coin de la porte, contre le mur des lits : en bas, le bac à toutous ; deux
    rangs d'albums debout (≈ 60 à 70 albums) ; dessus, la veilleuse. Ancrée au mur. Les livres de la semaine vont de face
    au-dessus de la commode ; les autres dorment ici (rotation)."""
    x0, y0, x1, y1 = G.ALBUMS
    h = G.ALBUMS_H
    out = [B(x0, y0, x0 + 0.75, y1, 0, h, CHENE), B(x1 - 0.75, y0, x1, y1, 0, h, CHENE), B(x0 + 0.75, y1 - 0.5, x1 - 0.75, y1, 0, h, BLANC),
           A(x0, y0, x1, y1, h - 0.75, h, CHENE, r=0.2, b=0.12), B(x0 + 0.75, y0 + 1.0, x1 - 0.75, y1 - 0.5, 0, 1.5, "carbone")]
    out += [B(x0 + 0.75, y0, x1 - 0.75, y1 - 0.5, z, z + 0.75, CHENE) for z in (1.5, 14.0, 28.0)]
    out += [A(x0 + 1.2, y0 + 0.6, x1 - 1.2, y1 - 1.0, 2.4, 13.2, "terracotta", r=0.9, b=0.3, trou=0.35),
            B(x0 + 1.5, y0 + 0.9, x1 - 1.5, y1 - 1.3, 2.25, 2.7, "terracotta")]
    out += etiquette((x0 + x1) / 2, y0 + 0.55, 8.8, "-y", "🧸 TOUTOUS", 9.0)
    out += [SPH(x0 + 5.0, y0 + 5.5, 13.3, 2.4, "sable"), SPH(x0 + 5.0, y0 + 4.2, 15.3, 1.5, "sable")]       # un toutou qui dépasse
    for zr in (14.75, 28.75):                                                                              # albums debout, dos vers −y
        x = x0 + 0.9
        while True:
            t, hh, dd = rng.uniform(0.3, 0.75), rng.uniform(8.0, min(12.0, 41.0 - zr if zr > 20 else 12.5)), rng.uniform(8.5, 11.0)
            if x + t > x1 - 0.9:
                break
            out.append(B(x, y0 + 0.9, x + t - 0.04, y0 + 0.9 + dd, zr, zr + hh, rng.choice(COUL_LIVRES + ("blanc-chaud", "sable"))))
            x += t
    out += [C(x1 - 4.5, y0 + 6.0, 1.6, h, h + 0.6, CHENE), SPH(x1 - 4.5, y0 + 6.0, h + 2.2, 1.7, "abat-jour")]
    return out


def tapis_jeu():
    """Le coin jeu ouvert : grand tapis plat 4½ × 7 pi (laine tissée ou coton lavable), champ sable uni pour bâtir, bordure
    terracotta ; deux coussins de sol ronds (moutarde, bleu fjord). Bordure et champ côte à côte, à la même hauteur."""
    x0, y0, x1, y1 = G.TAPIS
    out = [A(x0, y0, x1, y1, 0, 0.5, "terracotta", r=1.0, b=0.1, trou=2.2),
           A(x0 + 2.2, y0 + 2.2, x1 - 2.2, y1 - 2.2, 0, 0.5, "tapis", r=0.4, b=0.05)]
    for (x, y, r), coul in zip(G.COUSSINS, ("moutarde", "bleu-fjord")):
        out += [A(x - r, y - r, x + r, y + r, 0.5, 4.6, coul, r=r - 0.01, b=1.5),
                C(x, y, 0.8, 4.4, 4.75, coul)]
    return out


def jeu_au_sol():
    """Des Lego au plancher : une plaque de construction, une petite tour, des briques ; une auto."""
    zp = 0.8                                                                               # dessus de la plaque
    out = [B(70.0, 44.0, 80.0, 54.0, 0.5, zp, "lego-vert")]
    for r_ in range(5):
        out += brique(73.0, 47.0, zp + 0.45 * r_, 4, 2, ("lego-rouge", "lego-blanc", "lego-jaune", "lego-bleu", "lego-rouge")[r_])
    out += brique(76.0, 50.5, zp, 2, 4, "lego-orange") + brique(71.0, 51.0, zp, 2, 2, "lego-blanc")
    for k in range(9):
        out += brique(rng.uniform(62, 90), rng.uniform(36, 60), 0.5, rng.choice((2, 4)), 2, rng.choice(LEGO))
    x, y = 92.0, 40.0
    out += [A(x - 2.6, y - 1.3, x + 2.6, y + 1.3, 0.95, 1.95, "lego-rouge", r=0.5, b=0.25),
            A(x - 1.2, y - 1.1, x + 1.0, y + 1.1, 1.95, 2.75, "lego-rouge", r=0.4, b=0.2)]
    out += [CY(x + dx, y - 1.45, y + 1.45, 0.95, 0.45, NOIR) for dx in (-1.6, 1.6)]
    return out


M += rebords_livres() + armoires_hautes() + tablette_haute() + pateres() + tour_albums() + tapis_jeu() + jeu_au_sol()
M += bacs_sous_le_lit()

# =============================================================================================== garde-robe aménagée (gardée de la version 1)
gx0, gy0, gx1, gy1 = G.GR


def garde_robe():
    """Garde-robe (24½ × 75½ po) : face à la porte, étagère de 6 bacs étiquetés surmontée de 6 tiroirs à Lego triés par
    couleur et d'une tablette pour exposer les constructions ; aile gauche : penderie double (tringles à 42 et 78 po) ;
    aile droite : tablettes des bacs saisonniers et bac « hiver » au sol ; tablette haute et DEL sous la tablette."""
    out = []
    ex0, ey0, ex1, ey1 = G.GR_ETAGERE
    out += [B(ex0, ey0, ex1, ey0 + 0.75, 0, 37, CHENE), B(ex0, ey1 - 0.75, ex1, ey1, 0, 37, CHENE),
            A(ex0 - 0.25, ey0, ex1, ey1, 36.25, 37, CHENE, r=0.2, b=0.12), B(ex0 + 0.75, ey0 + 0.75, ex1, ey1 - 0.75, 0, 1.5, "carbone")]
    out += [B(ex0, ey0 + 0.75, ex1, ey1 - 0.75, z, z + 0.75, CHENE) for z in (1.5, 13.0, 24.75)]
    mots = (("🚂 TRAINS", "🧩 CASSE-TÊTES"), ("🐻 ANIMAUX", "🎨 BRICOLAGE"), ("🎭 COSTUMES", "🎲 JEUX"))
    k = 0
    for r_, z0 in enumerate((2.3, 13.8, 25.55)):
        for c_, (ya, yb) in enumerate(((ey0 + 1.2, (ey0 + ey1) / 2 - 0.25), ((ey0 + ey1) / 2 + 0.25, ey1 - 1.2))):
            out.append(A(ex0 + 0.5, ya, ex1 - 0.5, yb, z0, z0 + 10.2, COUL_BACS[k], r=0.9, b=0.3, trou=0.35))
            out += etiquette(ex0 + 0.45, (ya + yb) / 2, z0 + 6.4, "-x", mots[r_][c_], 9.6)
            k += 1
    # tiroirs à Lego triés par couleur : caisson noir mat, façades blanches à pastille de couleur
    out.append(B(ex0 + 0.75, ey0 + 0.5, ex1 - 0.25, ey1 - 0.5, 37, 51.6, NOIR))
    k = 0
    for za, zb in ((37.4, 42.0), (42.4, 46.9), (47.3, 51.3)):
        for ya, yb in ((ey0 + 0.9, (ey0 + ey1) / 2 - 0.2), ((ey0 + ey1) / 2 + 0.2, ey1 - 0.9)):
            yc, zc = (ya + yb) / 2, (za + zb) / 2
            out += [A(ex0 + 0.4, ya, ex0 + 0.85, yb, za, zb, "blanc", r=0.2, b=0.1),
                    CX(ex0 + 0.3, ex0 + 0.4, yc, zc - 0.3, 1.35, LEGO[k] if LEGO[k] != "lego-blanc" else "lego-noir"),
                    B(ex0 + 0.32, yc - 2.5, ex0 + 0.4, yc + 2.5, zb - 0.75, zb - 0.4, "carbone")]
            k += 1
    # tablette des constructions (les modèles finis se montrent ici, hors de portée du robot... et des petits frères)
    out.append(A(gx1 - 12, ey0, gx1, ey1, 55.25, 56, CHENE, r=0.2, b=0.12))
    fx, fy = gx1 - 7.5, ey0 + 5                                                                     # fusée
    for i, m_ in enumerate(("lego-blanc", "lego-blanc", "lego-rouge", "lego-blanc", "lego-bleu")):
        out += brique(fx, fy, 56 + i * 0.45, 4, 4, m_)
    out += [C(fx + 0.63, fy + 0.63, 0.55, 58.25, 59.6, "lego-rouge", r2=0.0)]
    out += brique(gx1 - 9.0, ey0 + 12.0, 56, 6, 3, "lego-jaune") + brique(gx1 - 8.5, ey0 + 12.3, 56.45, 3, 2, "lego-noir")
    out += brique(gx1 - 9.0, ey0 + 19.5, 56, 4, 2, "lego-vert") + brique(gx1 - 8.8, ey0 + 19.6, 56.45, 3, 2, "lego-vert") + \
        brique(gx1 - 8.6, ey0 + 19.7, 56.9, 2, 2, "lego-orange")
    # aile gauche : penderie double à la hauteur des gars (tringle basse à 42 po, haute à 78 po)
    py0, py1 = G.GR_PENDERIE
    xr = gx1 - 11.75
    out += [CY(xr, py0, py1, 42, 0.55, NOIR), CY(xr, py0, py1, 78, 0.55, NOIR)]
    out += [B(xr - 0.4, y, xr + 11.75, y + 0.6, z - 0.6, z + 0.8, NOIR) for y in (py0, py1 - 0.6) for z in (42, 78)]
    coul_vet = ("bleu-brume", "terracotta", "blanc-chaud", "sauge", "moutarde", "ciel", "prune", "sable", "corail", "pomme")

    def vetement(y, ep, zb, zt, mat):
        xc, yc = xr, y + ep / 2
        return [A(xc - 6.8, y, xc + 6.8, y + ep, zb, zt - 0.7, mat, r=0.3, b=0.25),
                A(xc - 5.6, y + 0.1, xc + 5.6, y + ep - 0.1, zt - 0.7, zt, mat, r=0.3, b=0.25),
                B(xc - 6.0, yc - 0.2, xc + 6.0, yc + 0.2, zt, zt + 0.45, CHENE),
                T([(xc, yc, zt + 0.45), (xc, yc, zt + 1.3), (xc + 0.6, yc, zt + 1.9)], 0.09, "metal")]
    y, k = py0 + 1.2, 0
    while y < py1 - 2.5:
        ep = rng.uniform(0.9, 1.5)
        out += vetement(y, ep, rng.uniform(20, 25), 40.6, coul_vet[k % len(coul_vet)])
        y += ep + rng.uniform(0.4, 1.1)
        k += 1
    for y in (py0 + 3, py0 + 7.5, py0 + 11):                                                    # tringle haute : 3 vestes
        out += vetement(y, 2.0, rng.uniform(52, 57), 76.6, ("bleu-brume", "terracotta", "sable")[int(y) % 3])
    out += [A(gx0 + 1.5, py0 + 2, gx0 + 9.5, py0 + 7, 0, 3.6, "terracotta", r=1.6, b=0.8), A(gx0 + 1.5, py0 + 8, gx0 + 9.5, py0 + 13, 0, 3.6, "terracotta", r=1.6, b=0.8)]
    # aile droite : tablettes et bacs saisonniers, bac « hiver » au sol
    ay0, ay1 = G.GR_AILE_D
    out += [A(gx1 - 12, ay0, gx1, ay1, z - 0.75, z, CHENE, r=0.2, b=0.12) for z in (30, 52)]
    out += [A(gx1 - 11.5, ay0 + 1, gx1 - 0.5, ay0 + 11.5, 30, 39, "sable", r=1, b=0.4), A(gx1 - 11.5, ay0 + 12.5, gx1 - 0.5, ay1 - 1, 30, 39, "sauge", r=1, b=0.4),
            A(gx1 - 11.5, ay0 + 1, gx1 - 0.5, ay0 + 11.5, 52, 60, "bleu-brume", r=1, b=0.4), A(gx1 - 11.5, ay0 + 12.5, gx1 - 0.5, ay1 - 1, 52, 60, "sable", r=1, b=0.4)]
    out += [A(gx0 + 2.5, ay0 + 1.5, gx1 - 1, ay1 - 1.5, 0, 14, "sable", r=1.2, b=0.4, trou=0.35)]
    out += etiquette(gx0 + 2.45, (ay0 + ay1) / 2, 9.5, "-x", "🧤 HIVER", 9.0)
    out += [SPH(gx0 + 10, ay0 + 8, 13.2, 3.2, "terracotta", ecrase=0.8), SPH(gx0 + 10, ay0 + 8, 16.0, 1.0, "blanc-chaud")]   # tuque
    # tablette haute (rangement des parents), DEL dessous
    out += [A(gx1 - 12, gy0, gx1, gy1, 82.25, 83, CHENE, r=0.2, b=0.12), B(gx1 - 11.7, gy0 + 1, gx1 - 11.2, gy1 - 1, 81.95, 82.25, "spot")]
    out += [A(gx1 - 11, gy0 + 3, gx1 - 0.5, gy0 + 18, 83, 91, "sable", r=1, b=0.4), A(gx1 - 11, gy1 - 18, gx1 - 0.5, gy1 - 3, 83, 91, "sauge", r=1, b=0.4)]
    return out


M += garde_robe()

BACS = (("bac-lego", "Bac des Lego"), ("bac-autos", "Bac des autos"), ("bac-dinos", "Bac des dinos"))
PEINTURES = {nom: [hx, usage + " — teinte d'écran, à valider sur échantillon", alias] for nom, (hx, alias, usage) in MU.PALETTE.items()}
PEINTURES.update({
    "Blanc chaud": ["#EEEAE2", "corridor (décor), pages des albums", "blanc-chaud"],
    "Blanc pur mat": ["#F5F5F1", "panneaux des lits superposés (existants), plafond", "blanc-mat"],
    "Bleu brume": ["#93A6B6", "vêtements, détails", "bleu-brume"],
    "Corail": ["#E07A5F", "couvertures d'albums", "corail"],
    "Bleu ciel (albums)": ["#8EC5E6", "couvertures d'albums", "ciel"],
    "Pomme": ["#9BC46B", "couvertures d'albums, un dino", "pomme"],
    "Prune": ["#7D5A80", "couvertures d'albums", "prune"],
    "Lego rouge": ["#C4281C", "briques, une auto", "lego-rouge"], "Lego bleu": ["#0D69AB", "briques", "lego-bleu"],
    "Lego jaune": ["#F5CD2F", "briques", "lego-jaune"], "Lego vert": ["#4B974A", "briques, plaque", "lego-vert"],
    "Lego blanc": ["#F2F3F2", "briques", "lego-blanc"], "Lego orange": ["#DA8541", "briques", "lego-orange"],
    "Lego noir": ["#1B2A34", "briques", "lego-noir"],
})

SCENE = {
    "niveau": "RDC",
    "titre": TITRE,
    "plafond": G.PLAFOND,               # PRÉSUMÉ (8 pi) : à mesurer
    "allege_fenetre": G.ALLEGE, "tete_fenetre": G.TETE,
    # fenêtre de façade : 3 châssis égaux, bande de petits carreaux (2 rangs × 3 colonnes) en haut de chaque châssis
    "fenetres": {"ouv-RDC-001": {"allege": G.ALLEGE, "tete": G.TETE, "sections": G.SECTIONS, "carreaux": dict(G.CARREAUX),
                                 "note": "photos du 2026-11-09 (sections, carreaux) ; allège et tête : vidéo DAG"}},
    "bornes": [0, 0, 177.25, 159.25],   # la chambre et sa garde-robe (qui dépasse le mur de façade coupé)
    "sol_defaut": "erable",
    "mats_finitions": {"porte": PIN, "plinthe": PIN, "placage": PIN, "metal": "blanc"},
    "peintures": PEINTURES,
    "peinture": {"piece-RDC-CH2": "Blanc nuage", "piece-RDC-GRA": "Blanc nuage"},
    # mur de gauche : le ciel du matin sous la murale (elle le couvre en entier ; la couleur sert aux bords et au plan)
    "accents": [{"piece": "piece-RDC-CH2", "mur": "mur-RDC-004", "peinture": "Ciel du matin"}],
    "images": {"murale_camp": IMAGE_MURALE},
    "mobilier": M,
    "revetements": [],
    # bacs roulants : on les touche, ils sortent vers le tapis (moteur : commande « glisser », voir renovation/README.md)
    "commandes": [{"id": cid, "nom": nom, "libelle_haut": "Sortir le bac", "libelle_bas": "Rentrer le bac",
                   "course": [0, -G.BACS_COURSE, 0], "depart": "bas", "duree": 0.9, "invite": "Touche le bac"}
                  for cid, nom in BACS],
    "lumieres": [{"x": XC, "y": YC, "z": 80, "i": 6}, {"x": 153, "y": 93, "z": 78, "i": 1.2}],
    "visites": [{"nom": "Depuis la porte", "x": 127, "y": 147, "cap": 258,
                 "commandes": {"bac-lego": "bas", "bac-autos": "bas", "bac-dinos": "bas"}},
                {"nom": "Le coin jeu (le tapis)", "x": 118, "y": 90, "cap": 207, "tangage": -16,
                 "commandes": {"bac-lego": "haut", "bac-autos": "bas", "bac-dinos": "bas"}},
                {"nom": "Les bacs sous le lit (touche un bac)", "x": 52, "y": 40, "cap": 84, "tangage": -30,
                 "commandes": {"bac-lego": "haut", "bac-autos": "haut", "bac-dinos": "haut"}},
                {"nom": "Le mur de rangement", "x": 54, "y": 62, "cap": 0, "tangage": 2,
                 "commandes": {"bac-lego": "bas", "bac-autos": "bas", "bac-dinos": "bas"}},
                {"nom": "La murale et les lits", "x": 114, "y": 32, "cap": 158, "tangage": -2},
                {"nom": "La garde-robe aménagée", "x": 116, "y": 94, "cap": 0},
                {"nom": "De la fenêtre vers la porte", "x": 62, "y": 28, "cap": 58}],
    "depart": {"x": 127, "y": 147, "cap": 258},
    "palette": [["Thème", "« Camp de base » : expédition nordique en aplats (proposé, à valider sur échantillon)", "#77A6C8"],
                ["Murale", "mur de gauche : ciel du matin, montagnes bleu fjord et sauge, collines terracotta, soleil "
                           "moutarde ; nuit bleu nuit doux et étoiles au-dessus des lits", "#CDE5F1"],
                ["Murs", "blanc nuage (3 murs et garde-robe) ; plafond blanc pur mat", "#F3EFE7"],
                ["Rangement", "chêne naturel (comme les lits), caissons blancs, portes bleu fjord, quincaillerie noir mat", "#C9A97B"],
                ["Accents", "bacs moutarde, terracotta et sauge ; tapis sable bordé de terracotta", "#E2A93F"],
                ["Gardés", "plancher d'érable, boiseries de pin teint, lits superposés, commode blanche, enseignes", "#5A3A26"]],
}
