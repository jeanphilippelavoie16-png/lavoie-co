# -*- coding: utf-8 -*-
"""Génère extraction/RDC.json (feuille REZ-DE-CHAUSSÉE) — extracteur Phase 1."""
import json, math

OUT = '/home/user/lavoie-co/releve/travail/extraction/RDC.json'

def D(v, src, photo='P3', ref=None, note=None):
    d = {"valeur": v, "source": src, "photo": photo}
    if ref: d["ref"] = ref
    if note: d["note"] = note
    return d

def pi(p, po=0):
    return p * 12 + po

T_EXT = 11.0   # épaisseur mur ext. ESTIMÉE (dessin)
T_INT = 6.0    # épaisseur cloison ESTIMÉE (dessin)
h = T_EXT / 2

# ---------------------------------------------------------------- COTES
C = []
def cote(n, txt, val, photo, px, empl, mesure, alt=None, note=None):
    c = {"id": "cote-RDC-%03d" % n, "texte_original": txt, "valeur": val,
         "lecture_1": txt, "lecture_2": None, "statut": "provisoire",
         "photo": photo, "px": px, "emplacement": empl, "mesure": mesure}
    if alt: c["alternatives"] = alt
    if note: c["note"] = note
    C.append(c)

V3 = "vérifiée sur P3, P4 et P6"
cote(1, "31'-8\"", pi(31, 8), "P3", [232, 1019], "chaîne ext. côté gauche, rang 3 (la plus éloignée du mur), hors-tout",
     "profondeur hors-tout : nu ext. mur avant → nu ext. mur arrière", note=V3)
cote(2, "15'-9\"", pi(15, 9), "P3", [358, 586], "chaîne ext. côté gauche, rang 2, segment arrière",
     "nu ext. mur arrière → axe (centre) de la fenêtre de la S. de bain (ouv-RDC-006)", note=V3 + " ; 15'-9\" + 15'-11\" = 31'-8\" (ferme)")
cote(3, "15'-11\"", pi(15, 11), "P3", [327, 1250], "chaîne ext. côté gauche, rang 2, segment avant",
     "nu ext. mur avant → axe de la fenêtre de la S. de bain (ouv-RDC-006)", note=V3)
cote(4, "3'-0\"", pi(3), "P3", [399, 892], "chaîne ext. côté gauche, rang 1 (ouvertures)",
     "largeur de la fenêtre de la S. de bain (ouv-RDC-006), entre ses jambages", note=V3)
cote(5, "31'-8\"", pi(31, 8), "P3", [2257, 916], "chaîne ext. côté droit, rang 3, hors-tout",
     "profondeur hors-tout : nu ext. mur avant → nu ext. mur arrière", note=V3)
cote(6, "16'-8\"", pi(16, 8), "P3", [2157, 651], "chaîne ext. côté droit, rang 2, segment arrière",
     "nu ext. mur arrière → axe de la fenêtre latérale de la cuisine (ouv-RDC-007)", note=V3 + " ; 16'-8\" + 15'-0\" = 31'-8\" (ferme)")
cote(7, "15'-0\"", pi(15), "P3", [2167, 1238], "chaîne ext. côté droit, rang 2, segment avant",
     "nu ext. mur avant → axe de la fenêtre latérale de la cuisine (ouv-RDC-007)", note=V3)
cote(8, "3'-0\"", pi(3), "P3", [2105, 970], "chaîne ext. côté droit, rang 1 (ouvertures)",
     "largeur de la fenêtre latérale de la cuisine (ouv-RDC-007)", note=V3)
cote(9, "38'-0\"", pi(38), "P3", [1296, 1894], "chaîne ext. avant, rang 3, hors-tout",
     "largeur hors-tout : nu ext. mur gauche → nu ext. mur droit", note=V3)
cote(10, "8'-2\"", pi(8, 2), "P3", [620, 1740], "chaîne ext. avant, rang 2, 1er segment depuis la gauche",
     "nu ext. mur gauche → axe de la fenêtre de la chambre avant (ouv-RDC-001)", note=V3 + " ; 8'-2\"+8'-5\"+14'-10\"+6'-7\" = 38'-0\" (ferme)")
cote(11, "8'-5\"", pi(8, 5), "P3", [987, 1750], "chaîne ext. avant, rang 2, 2e segment",
     "axe fenêtre chambre avant (ouv-RDC-001) → axe de la porte d'entrée avant (ouv-RDC-010)", note=V3)
cote(12, "14'-10\"", pi(14, 10), "P3", [1565, 1750], "chaîne ext. avant, rang 2, 3e segment",
     "axe porte d'entrée avant (ouv-RDC-010) → axe fenêtre du salon (ouv-RDC-002)", note=V3)
cote(13, "6'-7\"", pi(6, 7), "P3", [1937, 1725], "chaîne ext. avant, rang 2, 4e segment (droite)",
     "axe fenêtre du salon (ouv-RDC-002) → nu ext. mur droit", note=V3)
cote(14, "6'-3\"", pi(6, 3), "P3", [775, 1672], "chaîne ext. avant, rang 1 (ouvertures), gauche",
     "largeur de la fenêtre de la chambre avant (ouv-RDC-001)",
     alt=["6'-8\""], note="3 à tête plate, lu 3 sur P3/P4/P6 ; largeur mesurée au dessin ≈ 76 po (ESTIMÉ) compatible avec 6'-3\"")
cote(15, "9'-0\"", pi(9), "P3", [1817, 1662], "chaîne ext. avant, rang 1 (ouvertures), droite",
     "largeur de la fenêtre du salon (ouv-RDC-002)",
     alt=["5'-0\""], note="le 9 de cette main ressemble à un S/5 ; largeur mesurée au dessin ≈ 106 po (ESTIMÉ) → 9'-0\"")
cote(16, "18'-3\"", pi(18, 3), "P6", [850, 19], "chaîne ext. arrière, rang 3 (le plus éloigné), 1er segment depuis la gauche — absente de P3 (haut coupé)",
     "nu ext. mur gauche → nu ext. du mur gauche du volume de l'entrée arrière", note="lue sur P6, confirmée sur P4")
cote(17, "9'-0\"", pi(9), "P6", [1332, 22], "chaîne ext. arrière, rang 3, 2e segment — absente de P3",
     "largeur hors-tout du volume de l'entrée arrière (nu ext. gauche → nu ext. droit)", note="lue sur P6, confirmée sur P4")
cote(18, "10'-9\"", pi(10, 9), "P6", [1692, 32], "chaîne ext. arrière, rang 3, 3e segment (droite) — absente de P3",
     "nu ext. droit du volume de l'entrée arrière → nu ext. mur droit",
     alt=["10'-5\""], note="dernier chiffre : même glyphe que le 9 de « 9'-0\" » de la même chaîne (forme S/9). Avec 10'-9\" la chaîne 18'-3\"+9'-0\"+10'-9\" = 38'-0\" ; avec 10'-5\" = 37'-8\". Lue sur P6 et P4.")
cote(19, "8'-2\"", pi(8, 2), "P3", [679, 84], "chaîne ext. arrière, rang 2 (axes des ouvertures), 1er segment depuis la gauche",
     "nu ext. mur gauche → axe de la fenêtre de la chambre arrière (ouv-RDC-003)", note=V3)
cote(20, "8'-3\"", pi(8, 3), "P3", [1029, 75], "chaîne ext. arrière, rang 2, 2e segment",
     "axe fenêtre chambre arrière (ouv-RDC-003) → axe fenêtre chambre d'utilité (ouv-RDC-004)", note=V3)
cote(21, "8'-0\"", pi(8), "P3", [1406, 106], "chaîne ext. arrière, rang 2, 3e segment (écrit dans l'entrée arrière, à côté de « ARMOIRES »)",
     "axe fenêtre chambre d'utilité (ouv-RDC-004) → axe fenêtre de l'entrée arrière (ouv-RDC-008)",
     note="rattachement déduit de l'alignement des points de cote sur P6 (même ligne que 8'-2\", 8'-3\", 6'-10\", 6'-9\") ; pourrait être lu par erreur comme une dimension des armoires. Lue sur P3, P4, P6.")
cote(22, "6'-10\"", pi(6, 10), "P3", [1687, 115], "chaîne ext. arrière, rang 2, 4e segment (écrit sur les marches arrière)",
     "axe fenêtre de l'entrée arrière (ouv-RDC-008) → axe fenêtre de la cuisine (ouv-RDC-005)", note=V3)
cote(23, "6'-9\"", pi(6, 9), "P3", [1940, 145], "chaîne ext. arrière, rang 2, 5e segment (droite)",
     "axe fenêtre de la cuisine (ouv-RDC-005) → nu ext. mur droit",
     alt=["6'-5\""], note="glyphe S/9 ambigu (identique au 9 de « 9'-0\" » arrière). Avec 6'-9\" : 8'-2\"+8'-3\"+8'-0\"+6'-10\"+6'-9\" = 38'-0\" ; avec 6'-5\" = 37'-8\". Lue sur P3, P4, P6.")
cote(24, "6'-3\"", pi(6, 3), "P3", [843, 156], "chaîne ext. arrière, rang 1 (ouvertures), gauche",
     "largeur de la fenêtre de la chambre arrière (ouv-RDC-003)", note=V3)
cote(25, "3'-0\"", pi(3), "P3", [1175, 191], "chaîne ext. arrière, rang 1 (ouvertures)",
     "largeur de la fenêtre de la chambre d'utilité (ouv-RDC-004)", note=V3)
cote(26, "3'-6\"", pi(3, 6), "P6", [1402, 54], "chaîne ext. arrière (entrée arrière), rang 1 (ouvertures) — absente/coupée sur P3",
     "largeur de la fenêtre du mur arrière de l'entrée arrière (ouv-RDC-008)",
     alt=["3'-0\""], note="le 2e chiffre est traversé par le trait d'attache de la cote 2'-9\" (forme « b ») : 6 ou 0 ; largeur ESTIMÉE au dessin ≈ 39 po. Lue sur P6 et P4.")
cote(27, "2'-9\"", pi(2, 9), "P6", [1462, 35], "chaîne ext. arrière (entrée arrière), rang 2 — absente de P3",
     "axe fenêtre de l'entrée arrière (ouv-RDC-008) → nu ext. du mur droit de l'entrée arrière",
     alt=["6'-9\"", "1'-9\""], note="1er chiffre mal formé (« L ») ; 2'-9\" retenu car 8'-2\"+8'-3\"+8'-0\"+2'-9\" = 27'-2\" ≈ 18'-3\"+9'-0\" = 27'-3\" (écart 1\"). Lue sur P6 et P4.")
cote(28, "6'-3\"", pi(6, 3), "P3", [1800, 212], "chaîne ext. arrière, rang 1 (ouvertures), droite",
     "largeur de la fenêtre de la cuisine (ouv-RDC-005)", note=V3)
# chaîne intérieure en x (y ≈ 18'), de gauche à droite : 9'-0" 3'-2" 2'-5" 8'-4" 3'-5" 11'-8" = 38'-0"
NOTE_CHX = "chaîne intérieure en x tracée à travers la S. de bain, le dégagement, la ch. d'utilité, le BALAIS et la cuisine ; 9'-0\"+3'-2\"+2'-5\"+8'-4\"+3'-5\"+11'-8\" = 38'-0\" (ferme sur le hors-tout → extrémités au nu ext., points intermédiaires sur les cloisons, axe ou nu à confirmer)"
cote(29, "9'-0\"", pi(9), "P3", [675, 805], "chaîne int. en x (y≈18'), 1er segment depuis la gauche (écrit dans un petit cadre dans la S. de bain)",
     "nu ext. mur gauche → cloison droite de la S. de bain (mur-RDC-011)", note=NOTE_CHX)
cote(30, "3'-2\"", pi(3, 2), "P3", [910, 804], "chaîne int. en x, 2e segment",
     "cloison droite S. de bain (mur-RDC-011) → cloison gauche de la colonne des G.R. (mur-RDC-013/014)", note=NOTE_CHX)
cote(31, "2'-5\"", pi(2, 5), "P3", [1062, 800], "chaîne int. en x, 3e segment (alcôve / porte de la ch. d'utilité)",
     "cloison gauche colonne G.R. (mur-RDC-013) → cloison droite colonne G.R. (mur-RDC-015)", note=NOTE_CHX)
cote(32, "8'-4\"", pi(8, 4), "P3", [1250, 823], "chaîne int. en x, 4e segment (ch. d'utilité)",
     "cloison mur-RDC-015 → cloison gauche de l'escalier (mur-RDC-021)", note=NOTE_CHX)
cote(33, "3'-5\"", pi(3, 5), "P3", [1519, 803], "chaîne int. en x, 5e segment (écrit sous « BALAIS »)",
     "cloison gauche escalier (mur-RDC-021) → cloison droite escalier (mur-RDC-022) : largeur escalier/BALAIS", note=NOTE_CHX)
cote(34, "11'-8\"", pi(11, 8), "P3", [1815, 820], "chaîne int. en x, 6e segment (cuisine)",
     "cloison droite escalier (mur-RDC-022) → nu ext. mur droit", note=NOTE_CHX)
NOTE_CHG = "chaîne int. en y côté gauche : 13'-1\"+5'-6\"+13'-1\" = 31'-8\" (ferme sur le hors-tout)"
cote(35, "13'-1\"", pi(13, 1), "P3", [617, 617], "chaîne int. en y (x≈5'), segment arrière (chambre arrière)",
     "nu ext. mur arrière → cloison chambre arr./S. de bain (mur-RDC-010)", note=NOTE_CHG)
cote(36, "5'-6\"", pi(5, 6), "P3", [600, 923], "chaîne int. en y (x≈5'), segment du milieu (S. de bain)",
     "cloison mur-RDC-010 → cloison mur-RDC-012 (profondeur S. de bain)", note=NOTE_CHG + " ; lue 5'-6\" sur P3 et P4")
cote(37, "13'-1\"", pi(13, 1), "P3", [589, 1275], "chaîne int. en y (x≈5'), segment avant (chambre avant)",
     "nu ext. mur avant → cloison S. de bain/chambre avant (mur-RDC-012)", note=NOTE_CHG)
NOTE_CHA = "chaîne int. en x côté avant : 12'-2\"+2'-5\"+3'-11\"+19'-6\" = 38'-0\" (ferme)"
cote(38, "12'-2\"", pi(12, 2), "P3", [705, 1344], "chaîne int. en x (y≈7'), 1er segment (chambre avant)",
     "nu ext. mur gauche → cloison droite de la chambre avant (mur-RDC-026)", note=NOTE_CHA)
cote(39, "2'-5\"", pi(2, 5), "P3", [1050, 1350], "chaîne int. en x (y≈7'), 2e segment (G.R. avant)",
     "cloison mur-RDC-026 → cloison mur-RDC-027 (profondeur G.R./LIN./VEST.)", note=NOTE_CHA)
cote(40, "3'-11\"", pi(3, 11), "P3", [1190, 1342], "chaîne int. en x (y≈7'), 3e segment (hall)",
     "cloison mur-RDC-027 → cloison hall/salon (mur-RDC-025) : largeur du hall", note=NOTE_CHA)
cote(41, "19'-6\"", pi(19, 6), "P3", [1713, 1347], "chaîne int. en x (y≈7'), 4e segment (salon)",
     "cloison hall/salon (mur-RDC-025) → nu ext. mur droit", note=NOTE_CHA)
NOTE_CHM = "chaîne int. en y au milieu : 13'-1\"+3'-11\"+14'-8\" = 31'-8\" (ferme)"
cote(42, "14'-8\"", pi(14, 8), "P3", [1325, 608], "chaîne int. en y (x≈23'), segment arrière (ch. d'utilité)",
     "nu ext. mur arrière → cloison avant de la ch. d'utilité (mur-RDC-020)", note=NOTE_CHM)
cote(43, "3'-11\"", pi(3, 11), "P3", [1322, 962], "chaîne int. en y (x≈23'), segment du milieu (PASSAGE)",
     "cloison mur-RDC-020 → cloison salon/passage (mur-RDC-024) : largeur du passage", note=NOTE_CHM)
cote(44, "13'-1\"", pi(13, 1), "P3", [1320, 1303], "chaîne int. en y (x≈23'), segment avant (salon, côté gauche)",
     "nu ext. mur avant → cloison salon/passage (mur-RDC-024)", note=NOTE_CHM)
NOTE_CHD = "chaîne int. en y côté droit : 13'-1\"+18'-7\" = 31'-8\" (ferme)"
cote(45, "18'-7\"", pi(18, 7), "P3", [1870, 772], "chaîne int. en y (x≈35'), segment arrière (cuisine)",
     "nu ext. mur arrière → cloison salon/cuisine avec arche (mur-RDC-024)", alt=["16'-7\""],
     note=NOTE_CHD + " ; 1er chiffre 8 net sur P3/P4/P6")
cote(46, "13'-1\"", pi(13, 1), "P3", [1877, 1293], "chaîne int. en y (x≈35'), segment avant (salon, côté droit)",
     "nu ext. mur avant → cloison salon/cuisine (mur-RDC-024)", note=NOTE_CHD)
cote(47, "9\"", 9, "P3", [713, 750], "petite cote verticale au-dessus de la cloison chambre arr./S. de bain, à x≈14'",
     "épaisseur de la cloison chambre arrière / S. de bain (mur-RDC-010) : deux points de cote sur ses deux faces",
     alt=["6\" (si le texte est écrit tête-bêche)"],
     note="écrit « \"9 » (guillemets à gauche) sur P3, P4, P6 ; épaisseur dessinée ≈ 5 po (ESTIMÉ)")
cote(48, "ARCHE 4'-0\"", pi(4), "P3", [1258, 1200], "texte vertical dans la cloison hall/salon (mur-RDC-025)",
     "largeur de l'arche hall/salon (ouv-RDC-012)", alt=["ARCHE 6'-0\""],
     note="glyphe « 4 » ouvert, différent du 6 de « ARCHE 6'-0\" » (P3, P4, P6) ; mais l'ouverture dessinée mesure ≈ 74 po (ESTIMÉ)")
cote(49, "ARCHE 6'-0\"", pi(6), "P3", [1890, 1047], "texte horizontal dans la cloison salon/cuisine (mur-RDC-024)",
     "largeur de l'arche salon/cuisine (ouv-RDC-013)", note=V3)

def cid(n): return "cote-RDC-%03d" % n

# ---------------------------------------------------------------- MURS
M = []
def mur(n, typ, x1, y1, x2, y2, ep, cl, note, src_geo, indices=None):
    m = {"id": "mur-RDC-%03d" % n, "type": typ, "porteur": "inconnu",
         "indices_porteur": indices or [],
         "epaisseur": ep, "x1": x1, "y1": y1, "x2": x2, "y2": y2,
         "source_geometrie": src_geo, "cotes_liees": [cid(i) for i in cl], "note": note}
    M.append(m)

E_EXT = D(T_EXT, "ESTIMÉ", note="épaisseur non cotée ; mesurée au dessin (≈ 39-42 px sur P3 ≈ 11 po)")
E_INT = D(T_INT, "ESTIMÉ", note="épaisseur non cotée ; mesurée au dessin (≈ 18-25 px sur P3 ≈ 5-7 po)")
GEO_D = "DÉDUIT des cotes (axes = nu ext. ± épaisseur/2 ESTIMÉE)"
GEO_E = "ESTIMÉ (mesuré dans P3 par homographie calée sur les 4 coins ext. 38'-0\" x 31'-8\")"

mur(1, "ext", h, h, 456 - h, h, E_EXT, [9, 10, 11, 12, 13, 14, 15, 1, 5, 3, 7, 37, 44, 46],
    "mur avant (façade, rue) ; fenêtres chambre avant et salon, porte d'entrée", GEO_D)
mur(2, "ext", 456 - h, h, 456 - h, 380 - h, E_EXT, [5, 6, 7, 8, 9, 13, 18, 23, 34, 41],
    "mur latéral droit (salon, cuisine) ; fenêtre latérale cuisine", GEO_D)
mur(3, "ext", h, 380 - h, 456 - h, 380 - h, E_EXT, [1, 5, 2, 6, 19, 20, 21, 22, 23, 24, 25, 28, 16, 17, 18, 35, 42, 45],
    "mur arrière ; fenêtres chambre arr., ch. d'utilité, cuisine ; porte entrée arr. → palier (x≈23'-1\" à 25'-11\") ; le volume de l'entrée arrière s'y adosse entre x=219 et x=327",
    GEO_D)
mur(4, "ext", h, h, h, 380 - h, E_EXT, [1, 2, 3, 4, 9, 10, 16, 19, 29, 38],
    "mur latéral gauche (chambres, S. de bain) ; fenêtre S. de bain ; cheminée accolée à l'extérieur", GEO_D)
D_ENT = 67  # profondeur hors-tout ESTIMÉE de l'entrée arrière
mur(5, "ext", 219 + h, 380, 219 + h, 380 + D_ENT - h, E_EXT, [16, 17],
    "entrée arrière (volume en saillie) : mur gauche ; nu ext. à x=18'-3\" (LU) ; profondeur du volume NON cotée (≈ 5'-7\" ESTIMÉ)",
    "x DÉDUIT (cote-RDC-016) ; y ESTIMÉ")
mur(6, "ext", 219 + h, 380 + D_ENT - h, 327 - h, 380 + D_ENT - h, E_EXT, [17, 26, 27, 21, 22],
    "entrée arrière : mur arrière (fenêtre ouv-RDC-008)", "x DÉDUIT (cote-RDC-016, -017) ; y ESTIMÉ")
mur(7, "ext", 327 - h, 380, 327 - h, 380 + D_ENT - h, E_EXT, [17, 18, 27],
    "entrée arrière : mur droit avec la porte extérieure 2'-10\"x6'-10\" vers les marches arrière ; nu ext. à x=27'-3\" (18'-3\"+9'-0\")",
    "x DÉDUIT ; y ESTIMÉ")
mur(10, "int", h, 223, 108, 223, D(9, "LU", ref=cid(47), note="« 9\" » (alt. 6\") — à confirmer ; dessiné ≈ 5 po"),
    [35, 36, 47], "cloison chambre arrière / S. de bain", GEO_D + " (y = 31'-8\" − 13'-1\")")
mur(11, "int", 108, 157, 108, 223, E_INT, [29, 30, 36],
    "cloison droite de la S. de bain (porte S. de bain)", GEO_D + " (x = 9'-0\")")
mur(12, "int", h, 157, 146, 157, E_INT, [37, 36, 38],
    "cloison S. de bain / chambre avant ; prolongée jusqu'à x=146 par la baie de la porte de la chambre avant",
    GEO_D + " (y = 13'-1\")")
mur(13, "int", 146, 206, 146, 296, E_INT, [30, 31],
    "cloison gauche de la colonne des G.R. (côté dégagement), face au G.R. de la ch. d'utilité ; se termine à y≈206 (ESTIMÉ) par un montant",
    "x DÉDUIT (9'-0\"+3'-2\") ; y ESTIMÉ")
mur(14, "int", 146, 296, 146, 380 - h, E_INT, [30, 38],
    "façade des 2 G.R. de la chambre arrière : seulement un montant central (y≈332-345 ESTIMÉ) entre deux portes 2'-4\"x6'-8\" — pas de mur plein",
    "x DÉDUIT ; y ESTIMÉ")
mur(15, "int", 175, 253, 175, 380 - h, E_INT, [31, 32],
    "cloison arrière des G.R. / ch. d'utilité (porte du G.R. de la ch. d'utilité y≈253-285)",
    "x DÉDUIT (9'-0\"+3'-2\"+2'-5\") ; y ESTIMÉ")
mur(16, "int", 146, 337.5, 175, 337.5, E_INT, [], "cloison entre les 2 G.R. de la chambre arrière", GEO_E)
mur(17, "int", 146, 296, 175, 296, E_INT, [], "cloison entre G.R. de la chambre arr. et G.R. de la ch. d'utilité", GEO_E)
mur(18, "int", 146, 253, 175, 253, E_INT, [], "cloison avant du G.R. de la ch. d'utilité (avec ressaut dessiné)", GEO_E)
mur(19, "int", 108, 212, 175, 212, D(None, "ILLISIBLE", photo=None, note="aucun mur plein : ligne de portes"), [30, 31],
    "ligne de portes (aucun mur plein) : porte chambre arrière (x≈111-143) et porte ch. d'utilité (x≈149-172) ; ~11 po en avant de la cloison mur-RDC-010",
    "x DÉDUIT ; y ESTIMÉ")
mur(20, "int", 175, 204, 316, 204, E_INT, [42, 43],
    "cloison ch. d'utilité / passage, prolongée devant le BALAIS (porte BALAIS x≈279-312)", GEO_D + " (y = 31'-8\" − 14'-8\")")
mur(21, "int", 275, 204, 275, 380 - h, E_INT, [32, 33],
    "cloison ch. d'utilité / escalier-BALAIS", GEO_D + " (x = 9'-0\"+3'-2\"+2'-5\"+8'-4\")")
mur(22, "int", 316, 157, 316, 380 - h, E_INT, [33, 34],
    "cloison escalier / cuisine (laveuse-sécheuse adossées côté cuisine) ; porte palier→cuisine (y≈338-372) et porte passage→cuisine (y≈166-198)",
    GEO_D + " (x = 38'-0\" − 11'-8\")")
mur(23, "int", 275, 241.5, 316, 241.5, E_INT, [], "cloison bas de l'escalier / BALAIS", GEO_E)
mur(24, "int", 222, 157, 456 - h, 157, E_INT, [44, 46, 43, 45, 41],
    "cloison salon / passage et salon / cuisine-s.-à-manger ; ARCHE 6'-0\" côté cuisine", GEO_D + " (y = 13'-1\")")
mur(25, "int", 222, h, 222, 157, E_INT, [40, 41],
    "cloison hall-entrée / salon ; ARCHE 4'-0\" (?) côté hall ; montant de la porte du hall à y≈63",
    GEO_D + " (x = 12'-2\"+2'-5\"+3'-11\")")
mur(26, "int", 146, h, 146, 160, E_INT, [38, 39],
    "cloison chambre avant / G.R. avant / LIN. (porte G.R. avant y≈78-107)", GEO_D + " (x = 12'-2\")")
mur(27, "int", 175, 54, 175, 160, E_INT, [39, 40],
    "cloison LIN. / G.R. avant côté hall ; s'arrête à y≈54 (le VEST. est ouvert sur l'entrée)", "x DÉDUIT ; y ESTIMÉ")
mur(28, "int", 146, 160, 175, 160, E_INT, [],
    "cloison arrière du LIN. (porte LIN.) ; presque alignée sur mur-RDC-012 (y=157)", GEO_E)
mur(29, "int", 146, 134, 175, 134, E_INT, [], "cloison LIN. / G.R. avant", GEO_E)
mur(30, "int", 146, 54, 175, 54, E_INT, [], "cloison G.R. avant / VEST.", GEO_E)
mur(31, "int", 175, 63, 222, 63, D(None, "ILLISIBLE", photo=None, note="aucun mur plein : montants de porte"), [40],
    "ligne de porte hall / entrée (montants seulement, aucun mur plein) : porte 2'-8\"x6'-8\"", "x DÉDUIT ; y ESTIMÉ")

# ---------------------------------------------------------------- OUVERTURES
mur_by = {m["id"]: m for m in M}
O = []
def pos_along(mid, x, y):
    m = mur_by[mid]
    dx, dy = m["x2"] - m["x1"], m["y2"] - m["y1"]
    L = math.hypot(dx, dy)
    return round(((x - m["x1"]) * dx + (y - m["y1"]) * dy) / L, 1)

def ouv(n, typ, op, mid, cx, cy, possrc, posnote, larg, haut, txt, sens=None, note=None, photo="P3"):
    o = {"id": "ouv-RDC-%03d" % n, "type": typ, "operation": op, "mur_id": mid,
         "position": D(pos_along(mid, cx, cy), possrc, note=posnote),
         "centre_xy": [cx, cy],
         "largeur": larg, "hauteur": haut,
         "allege": D(None, "ILLISIBLE", photo=None, note="non écrite"),
         "sens": sens, "texte_original": txt}
    if note: o["note"] = note
    O.append(o)

NOH = D(None, "ILLISIBLE", photo=None, note="hauteur non écrite pour les fenêtres")
# fenêtres
ouv(1, "fenetre", "fixe", "mur-RDC-001", 98, h, "DÉDUIT", "centre à 8'-2\" du nu ext. gauche (cote-RDC-010)",
    D(75, "LU", ref=cid(14), note="alt. 6'-8\""), NOH, "6'-3\" ; LINTEAU 2-2\"x8\"",
    note="fenêtre chambre avant ; type d'ouvrant non indiqué (operation 'fixe' = inconnu, 3 carreaux dessinés) ; linteau str-RDC-L01")
ouv(2, "fenetre", "fixe", "mur-RDC-001", 456 - 79, h, "DÉDUIT", "centre à 6'-7\" du nu ext. droit (cote-RDC-013) ; = 8'-2\"+8'-5\"+14'-10\" depuis la gauche",
    D(108, "LU", ref=cid(15)), NOH, "9'-0\" ; LINTEAU 2-2\"x10\"",
    note="fenêtre salon (3 sections dessinées) ; ouvrant non indiqué ; linteau str-RDC-L02")
ouv(3, "fenetre", "fixe", "mur-RDC-003", 98, 380 - h, "DÉDUIT", "centre à 8'-2\" du nu ext. gauche (cote-RDC-019)",
    D(75, "LU", ref=cid(24)), NOH, "6'-3\" ; LINTEAU 2-2\"x8\"",
    note="fenêtre chambre arrière ; linteau str-RDC-L03")
ouv(4, "fenetre", "fixe", "mur-RDC-003", 98 + 99, 380 - h, "DÉDUIT", "centre à 8'-2\"+8'-3\" = 16'-5\" (cotes 019, 020)",
    D(36, "LU", ref=cid(25)), NOH, "3'-0\" ; LIN. 2-2\"x6\"",
    note="fenêtre chambre d'utilité ; linteau str-RDC-L04")
ouv(5, "fenetre", "fixe", "mur-RDC-003", 456 - 81, 380 - h, "DÉDUIT",
    "centre à 6'-9\" du nu ext. droit (cote-RDC-023) ; = 8'-2\"+8'-3\"+8'-0\"+6'-10\" = 31'-3\" depuis la gauche ; si 6'-5\" : 31'-7\"",
    D(75, "LU", ref=cid(28)), NOH, "6'-3\" ; LINTEAU 2-2\"x8\"",
    note="fenêtre cuisine au-dessus de l'évier ; linteau str-RDC-L05")
ouv(6, "fenetre", "fixe", "mur-RDC-004", h, 191, "DÉDUIT", "centre à 15'-11\" du nu ext. avant (cote-RDC-003)",
    D(36, "LU", ref=cid(4)), NOH, "3'-0\" ; LIN. 2-2\"x6\"",
    note="fenêtre S. de bain (mur gauche) ; linteau str-RDC-L06")
ouv(7, "fenetre", "fixe", "mur-RDC-002", 456 - h, 180, "DÉDUIT", "centre à 15'-0\" du nu ext. avant (cote-RDC-007)",
    D(36, "LU", ref=cid(8)), NOH, "3'-0\" ; LIN. 2-2\"x6\"",
    note="fenêtre latérale cuisine / s.-à-manger (mur droit) ; linteau str-RDC-L07")
ouv(8, "fenetre", "fixe", "mur-RDC-006", 293, 380 + D_ENT - h, "DÉDUIT",
    "centre à 8'-2\"+8'-3\"+8'-0\" = 24'-5\" du nu ext. gauche (cotes 019-021) ; 2'-9\" du nu ext. droit de l'entrée (cote-RDC-027 → 294)",
    D(42, "LU", photo="P6", ref=cid(26), note="alt. 3'-0\" ; largeur ESTIMÉE au dessin ≈ 39 po"), NOH, "3'-6\"",
    note="fenêtre de l'entrée arrière ; aucun linteau écrit (haut de P3 coupé, rien sur P4/P6)", photo="P6")
# arches
ouv(12, "arche", "aucune", "mur-RDC-025", 222, 118.6, "ESTIMÉ", "centre mesuré au dessin (ouverture dessinée y≈82-156)",
    D(48, "LU", ref=cid(48), note="alt. 6'-0\" ; ouverture dessinée ≈ 74 po (ESTIMÉ) — voir observations"),
    D(None, "ILLISIBLE", photo=None), "ARCHE 4'-0\"", note="arche hall / salon")
ouv(13, "arche", "aucune", "mur-RDC-024", 403.5, 157, "ESTIMÉ", "centre mesuré au dessin (ouverture dessinée x≈367-440, ≈ 73 po)",
    D(72, "LU", ref=cid(49)), D(None, "ILLISIBLE", photo=None), "ARCHE 6'-0\"", note="arche salon / cuisine-s.-à-manger")
# portes
H68 = lambda: D(80, "LU", note="6'-8\" de l'étiquette")
H610 = lambda: D(82, "LU", note="6'-10\" de l'étiquette")
ouv(10, "porte", "battante", "mur-RDC-001", 199, h, "DÉDUIT", "centre à 8'-2\"+8'-5\" = 16'-7\" du nu ext. gauche (cotes 010, 011)",
    D(34, "LU"), H610(), "2'-10\"x6'-10\"",
    {"charniere": "fin", "ouvre_vers": "gauche"},
    note="porte d'entrée avant (hall/entrée) ; pentures côté droit (côté salon, x≈216), le vantail s'ouvre vers l'intérieur et se range le long de la cloison du salon ; donne sur le perron de béton")
ouv(11, "porte", "battante", "mur-RDC-031", 199, 63, "ESTIMÉ", "baie entre cloisons x=175 et x=222 (DÉDUIT) ; y ESTIMÉ",
    D(32, "LU"), H68(), "2'-8\"x6'-8\"",
    {"charniere": "debut", "ouvre_vers": "gauche"},
    note="porte entre l'entrée (côté porte avant) et le HALL ; pentures côté gauche (x≈178), ouvre vers le hall (+y)")
ouv(14, "porte", "battante", "mur-RDC-012", 127, 157, "DÉDUIT", "baie entre cloison S. de bain x=108 et cloison x=146 (cotes 029, 030)",
    D(30, "LU"), H68(), "2'-6\"x6'-8\"",
    {"charniere": "fin", "ouvre_vers": "droite"},
    note="porte de la chambre avant depuis le dégagement ; pentures côté droit (x≈143), ouvre dans la chambre (vers l'avant, -y)")
ouv(15, "porte", "battante", "mur-RDC-011", 108, 178, "ESTIMÉ", "baie dessinée y≈164-192",
    D(30, "LU"), H68(), "2'-6\"x6'-8\"",
    {"charniere": "debut", "ouvre_vers": "gauche"},
    note="porte de la S. de bain ; pentures côté avant (y≈164), ouvre dans la S. de bain (-x)")
ouv(16, "porte", "battante", "mur-RDC-019", 127, 212, "ESTIMÉ", "x DÉDUIT (baie 108-146) ; y ESTIMÉ",
    D(30, "LU"), H68(), "2'-6\"x6'-8\"",
    {"charniere": "fin", "ouvre_vers": "gauche"},
    note="porte de la chambre arrière au bout du dégagement ; pentures côté droit (x≈143, contre la colonne des G.R.), ouvre dans la chambre (+y)")
ouv(17, "porte", "battante", "mur-RDC-019", 160.5, 212, "ESTIMÉ", "x DÉDUIT (baie 146-175 = 2'-5\" d'axe en axe) ; y ESTIMÉ",
    D(30, "LU", note="alt. 2'-4\" ; ne peut pas tenir dans une baie de 2'-5\" d'axe en axe — voir observations"), H68(),
    "2'-6\"x6'-8\"", {"charniere": "debut", "ouvre_vers": "gauche"},
    note="porte de la chambre d'utilité (alcôve sous le G.R.) ; pentures côté gauche (x≈149), ouvre vers la ch. d'utilité (+y)")
ouv(18, "porte", "battante", "mur-RDC-015", 175, 269, "ESTIMÉ", "baie dessinée y≈253-285",
    D(28, "LU"), H68(), "2'-4\"x6'-8\"",
    {"charniere": "debut", "ouvre_vers": "droite"},
    note="porte du G.R. de la chambre d'utilité ; pentures côté avant (y≈253), ouvre dans la ch. d'utilité (+x)")
ouv(19, "porte", "battante", "mur-RDC-014", 146, 360, "ESTIMÉ", "baie dessinée y≈345-377",
    D(28, "LU"), H68(), "2'-4\"x6'-8\"",
    {"charniere": "debut", "ouvre_vers": "gauche"},
    note="porte du G.R. arrière de la chambre arrière ; pentures sur le montant central (côté avant, y≈345), ouvre dans la chambre (-x)")
ouv(20, "porte", "battante", "mur-RDC-014", 146, 316, "ESTIMÉ", "baie dessinée y≈300-332",
    D(28, "LU"), H68(), "2'-4\"x6'-8\"",
    {"charniere": "fin", "ouvre_vers": "gauche"},
    note="porte du 2e G.R. de la chambre arrière ; pentures sur le montant central (côté arrière, y≈332), ouvre dans la chambre (-x)")
ouv(21, "porte", "battante", "mur-RDC-026", 146, 93, "ESTIMÉ", "baie dessinée y≈78-107",
    D(30, "LU"), H68(), "2'-6\"x6'-8\"",
    {"charniere": "debut", "ouvre_vers": "gauche"},
    note="porte du G.R. de la chambre avant ; pentures côté avant (y≈78), ouvre dans la chambre (-x)")
ouv(22, "porte", "battante", "mur-RDC-028", 163.5, 160, "ESTIMÉ", "baie dessinée x≈152-175",
    D(18, "LU"), H68(), "1'-6\"x6'-8\"",
    {"charniere": "fin", "ouvre_vers": "gauche"},
    note="porte de la lingerie (LIN.) ; pentures côté droit (x≈175), ouvre vers le dégagement (+y)")
ouv(23, "porte", "battante", "mur-RDC-020", 295.5, 204, "ESTIMÉ", "baie dessinée x≈279-312 (entre cloisons 275 et 316, DÉDUIT)",
    D(28, "LU"), H68(), "2'-4\"x6'-8\"",
    {"charniere": "debut", "ouvre_vers": "droite"},
    note="porte du BALAIS (sous l'escalier) ; pentures côté gauche (x≈279), ouvre vers le passage (-y)")
ouv(24, "porte", "battante", "mur-RDC-022", 316, 182, "ESTIMÉ", "baie dessinée y≈166-198 (entre bout de la cloison d'escalier et la cloison du salon)",
    D(32, "LU"), H68(), "2'-8\"x6'-8\"",
    {"charniere": "debut", "ouvre_vers": "gauche"},
    note="porte passage → cuisine ; pentures côté avant (y≈166), ouvre vers le passage (-x)")
ouv(25, "porte", "battante", "mur-RDC-022", 316, 355, "ESTIMÉ", "baie dessinée y≈338-372",
    D(32, "LU"), H68(), "2'-8\"x6'-8\"",
    {"charniere": "fin", "ouvre_vers": "droite"},
    note="porte palier d'escalier → cuisine ; pentures côté arrière (y≈372), ouvre dans la cuisine (+x)")
ouv(26, "porte", "battante", "mur-RDC-003", 295, 380 - h, "ESTIMÉ", "baie dessinée x≈278-311 (entre cloison 275 et le coin de la cuisine)",
    D(32, "LU"), H68(), "2'-8\"x6'-8\"",
    {"charniere": "debut", "ouvre_vers": "droite"},
    note="porte entrée arrière → palier de l'escalier (dans l'alignement du mur arrière principal) ; pentures côté gauche (x≈278), ouvre vers le palier (-y)")
ouv(27, "porte", "battante", "mur-RDC-007", 327 - h, 409, "ESTIMÉ", "baie dessinée y≈393-425",
    D(34, "LU"), H610(), "2'-10\"x6'-10\"",
    {"charniere": "fin", "ouvre_vers": "gauche"},
    note="porte extérieure arrière (de l'entrée arrière vers les marches arrière) ; pentures côté arrière (y≈425), ouvre vers l'intérieur de l'entrée (-x)")
O.sort(key=lambda o: o["id"])

# ---------------------------------------------------------------- PIÈCES
P = []
def area(poly):
    s = 0
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        s += x1 * y2 - x2 * y1
    return s / 2

def piece(code, nom, orig, poly, dims=None, note=None, src="DÉDUIT"):
    a = area(poly)
    assert a > 0, code
    p = {"id": "piece-RDC-" + code, "nom": nom, "nom_original": orig, "polygone": poly,
         "superficie": D(round(a / 144, 1), "ESTIMÉ" if src != "DÉDUIT" else "DÉDUIT", photo=None,
                         note="calculée sur le polygone (nu int., épaisseurs ESTIMÉES : ext. 11 po, cloisons 6 po)"),
         "hauteur_plafond": D(None, "ILLISIBLE", photo=None, note="non écrite sur la feuille")}
    if dims: p["dimensions"] = dims
    if note: p["note"] = note
    P.append(p)

i_ = T_EXT; c = T_INT / 2
piece("CH1", "Chambre arrière", "CHAMBRE",
      [[i_, 223 + c], [108 + c, 223 + c], [108 + c, 212], [146 - c, 212], [146 - c, 380 - i_], [i_, 380 - i_]],
      {"x": D(146, "DÉDUIT", note="9'-0\"+3'-2\" = 12'-2\" (nu ext. gauche → cloison des G.R.) ; aucune cote x écrite pour cette chambre"),
       "y": D(157, "LU", ref=cid(35), note="13'-1\" mesuré du nu ext. arrière à la cloison (pas une cote nette)")},
      note="inclut la baie de porte au bout du dégagement (x 111-143, y 212-226) ; 2 G.R. sur le côté droit")
piece("SDB", "Salle de bain", "S. DE BAIN",
      [[i_, 157 + c], [108 - c, 157 + c], [108 - c, 223 - c], [i_, 223 - c]],
      {"x": D(108, "LU", ref=cid(29), note="9'-0\" du nu ext. gauche à la cloison"),
       "y": D(66, "LU", ref=cid(36), note="5'-6\" entre cloisons (axe ou nu ?)")})
piece("CH2", "Chambre avant", "CHAMBRE",
      [[i_, i_], [146 - c, i_], [146 - c, 157 - c], [i_, 157 - c]],
      {"x": D(146, "LU", ref=cid(38), note="12'-2\" du nu ext. gauche à la cloison"),
       "y": D(157, "LU", ref=cid(37), note="13'-1\" du nu ext. avant à la cloison")})
piece("GR1", "Garde-robe 1 (chambre arrière)", "G.R.",
      [[146, 337.5 + c], [175 - c, 337.5 + c], [175 - c, 380 - i_], [146, 380 - i_]],
      {"x": D(29, "DÉDUIT", note="2'-5\" d'axe en axe (cote-RDC-031, même alignement)")}, src="ESTIMÉ",
      note="limite avant (y) ESTIMÉE ; façade = portes (pas de mur) ; barre & tablette (note-RDC-03)")
piece("GR2", "Garde-robe 2 (chambre arrière)", "G.R.",
      [[146, 296 + c], [175 - c, 296 + c], [175 - c, 337.5 - c], [146, 337.5 - c]], src="ESTIMÉ",
      note="limites y ESTIMÉES ; barre & tablette")
piece("GRU", "Garde-robe de la chambre d'utilité", "G.R.",
      [[146 + c, 253 + c], [175 - c, 253 + c], [175 - c, 296 - c], [146 + c, 296 - c]], src="ESTIMÉ",
      note="porte sur la ch. d'utilité ; barre & tablette")
piece("UTI", "Chambre d'utilité", "CHAMBRE D'UTILITÉ",
      [[146 + c, 212], [175, 212], [175, 204 + c], [275 - c, 204 + c], [275 - c, 380 - i_], [175 + c, 380 - i_],
       [175 + c, 253 - c], [146 + c, 253 - c]],
      {"x": D(100, "LU", ref=cid(32), note="8'-4\" entre cloisons (hors alcôve)"),
       "y": D(176, "LU", ref=cid(42), note="14'-8\" du nu ext. arrière à la cloison avant")},
      note="inclut l'alcôve d'entrée sous le G.R. (x 149-175, y 212-250) ; solives 2\"x7\" @ 16\" c/c notées ici")
piece("DEG", "Dégagement (sans nom au plan)", "(aucun)",
      [[108 + c, 157 + c], [146, 157 + c], [146, 160 + c], [175 + c, 160 + c], [175 + c, 157 + c], [222, 157 + c],
       [222, 204 - c], [175 + c, 204 - c], [175 + c, 212], [108 + c, 212]],
      {"x": D(38, "LU", ref=cid(30), note="3'-2\" (partie entre S. de bain et colonne des G.R.)")}, src="ESTIMÉ",
      note="corridor des chambres + carrefour avec le hall et le passage ; pas de nom écrit")
piece("HALL", "Hall", "HALL",
      [[175 + c, 63 + c], [222 - c, 63 + c], [222 - c, 157 + c], [175 + c, 157 + c]],
      {"x": D(47, "LU", ref=cid(40), note="3'-11\" d'axe en axe (ou nu ?)")},
      note="limite arrière arbitraire à y≈160 (continu avec le dégagement)")
piece("ENT", "Entrée avant (sans nom au plan)", "(aucun)",
      [[175 + c, i_], [222 - c, i_], [222 - c, 63 - c], [175 + c, 63 - c]], src="ESTIMÉ",
      note="espace entre la porte d'entrée et la porte du hall ; ouvert sur le VEST.")
piece("LIN", "Lingerie", "LIN.",
      [[146 + c, 134 + c], [175 - c, 134 + c], [175 - c, 160 - c], [146 + c, 160 - c]], src="ESTIMÉ")
piece("GRA", "Garde-robe (chambre avant)", "G.R.",
      [[146 + c, 54 + c], [175 - c, 54 + c], [175 - c, 134 - c], [146 + c, 134 - c]],
      {"x": D(29, "LU", ref=cid(39), note="2'-5\" d'axe en axe")}, src="ESTIMÉ", note="barre & tablette")
piece("VES", "Vestiaire (garde-robe d'entrée)", "VEST.",
      [[146 + c, i_], [175 + c, i_], [175 + c, 54 - c], [146 + c, 54 - c]], src="ESTIMÉ",
      note="« VEST. » = vestiaire (une tringle est dessinée) ; ouvert sur l'entrée avant, aucune porte dessinée")
piece("SAL", "Salon", "SALON",
      [[222 + c, i_], [456 - i_, i_], [456 - i_, 157 - c], [222 + c, 157 - c]],
      {"x": D(234, "LU", ref=cid(41), note="19'-6\" de la cloison du hall au nu ext. droit"),
       "y": D(157, "LU", ref=cid(44), note="13'-1\" (écrit 2 fois : cote-RDC-044 et -046)")})
piece("PAS", "Passage", "PASSAGE",
      [[222, 157 + c], [316 - c, 157 + c], [316 - c, 204 - c], [222, 204 - c]],
      {"y": D(47, "LU", ref=cid(43), note="3'-11\"")},
      note="mot « PASSAGE » écrit près du luminaire ; relie hall, BALAIS et cuisine")
piece("CUI", "Cuisine / salle à manger", "CUISINE S.-À-MANGER",
      [[316 + c, 157 + c], [456 - i_, 157 + c], [456 - i_, 380 - i_], [316 + c, 380 - i_]],
      {"x": D(140, "LU", ref=cid(34), note="11'-8\" de la cloison d'escalier au nu ext. droit"),
       "y": D(223, "LU", ref=cid(45), note="18'-7\" du nu ext. arrière à la cloison du salon")})
piece("BAL", "Placard à balais", "BALAIS",
      [[275 + c, 204 + c], [316 - c, 204 + c], [316 - c, 241.5 - c], [275 + c, 241.5 - c]],
      {"x": D(41, "LU", ref=cid(33), note="3'-5\" (largeur commune escalier/BALAIS)")}, src="ESTIMÉ")
piece("ESC", "Escalier du sous-sol et palier (sans nom au plan)", "(aucun)",
      [[275 + c, 241.5 + c], [316 - c, 241.5 + c], [316 - c, 380 - i_], [275 + c, 380 - i_]],
      {"x": D(41, "LU", ref=cid(33))}, src="ESTIMÉ",
      note="volées vers le sous-sol (y≈244-335) + palier en haut (y≈335-369) desservant l'entrée arrière et la cuisine")
piece("EAR", "Entrée arrière", "(aucun nom ; « ARMOIRES » écrit)",
      [[219 + i_, 380], [327 - i_, 380], [327 - i_, 380 + D_ENT - i_], [219 + i_, 380 + D_ENT - i_]],
      {"x": D(108, "LU", photo="P6", ref=cid(17), note="9'-0\" hors-tout (nu ext.)")}, src="ESTIMÉ",
      note="volume en saillie à l'arrière ; profondeur NON cotée (ESTIMÉE ≈ 5'-7\" hors-tout) ; armoires le long du mur gauche")
P = [p for p in P]
for p in P:
    if p.get("dimensions") is None and "dimensions" in p:
        del p["dimensions"]

# ---------------------------------------------------------------- ELEMENTS
EL = []
def el(code, typ, nom, orig, x, y, Lx=None, Ly=None, txt=None, note=None, rot=0, extra=None, src="ESTIMÉ", photo="P3"):
    e = {"id": "elem-RDC-" + code, "type": typ, "nom": nom, "nom_original": orig,
         "position": {"x": x, "y": y, "rotation_deg": rot, "source": src},
         "dimensions": {"longueur": D(Lx, "ESTIMÉ" if Lx is not None else "ILLISIBLE", photo=photo if Lx is not None else None),
                        "largeur": D(Ly, "ESTIMÉ" if Ly is not None else "ILLISIBLE", photo=photo if Ly is not None else None)},
         "texte_original": txt, "photo": photo}
    if extra: e.update(extra)
    if note: e["note"] = note
    EL.append(e)

el("ESC1", "escalier", "Escalier vers le sous-sol", "(flèche) + « 2.R. 14 C.M. » + « RAMPE »", 295.5, 289.5, 35, 91,
   "2.R. 14 C.M.",
   extra={"escalier": {"nb_contremarches": D(14, "LU", note="« 14 C.M. » = 14 contremarches ; préfixe « 2.R. » de lecture incertaine (alt. « E.R. », « 2.B. »), sens inconnu ; seulement ~10 girons dessinés à cet étage (ligne de coupe)"),
                       "fleche": "DESCEND", "direction": "-y", "texte_original": "2.R. 14 C.M."}},
   note="largeur 3'-5\" d'axe en axe (cote-RDC-033) ; descend vers l'avant depuis le palier arrière ; « RAMPE » (main courante) avec flèche vers le mur gauche (mur-RDC-021) ; « 3W » (interrupteur 3 voies) en haut")
el("MAR-AV", "marches-ext", "Marches extérieures avant", "(non écrit)", 257.5, -26.5, 53, 53, None,
   note="5 girons dessinés (6 traits), parallèles à la façade, descendant vers la droite (+x) depuis le perron ; nb de contremarches NON écrit",
   extra={"escalier": {"nb_contremarches": D(None, "ILLISIBLE", photo=None, note="non écrit ; 5 girons dessinés"),
                       "fleche": None, "direction": "+x", "texte_original": None}})
el("PERRON", "perron", "Perron de béton armé", "BÉTON REN. AVEC BARRE ½\"Ø @ 10\" c/c", 197.5, -26.5, 67, 53,
   "BETON / REN. AVEC BARRE / 1/2 Ø @ 10\" c/c",
   note="dalle devant la porte d'entrée ; « REN. » = renforcé (armé) de barres ½ po à 10 po c/c ; dimensions non cotées (ESTIMÉ)")
el("MAR-AR", "marches-ext", "Marches extérieures arrière", "(non écrit)", 367, 407, 76, 53, None,
   note="le long du mur arrière de la cuisine, depuis la porte extérieure de l'entrée arrière ; 7 intervalles dessinés (traits verticaux) ; nb de contremarches NON écrit ; probablement descend vers +x",
   extra={"escalier": {"nb_contremarches": D(None, "ILLISIBLE", photo=None, note="non écrit"),
                       "fleche": None, "direction": "+x", "texte_original": None}})
el("CHEM", "cheminee", "Cheminée (maçonnerie) avec conduit", "(non écrit)", -10.5, 142, 20, 20, None,
   note="massif hachuré accolé à l'extérieur du mur gauche, vis-à-vis de la cloison S. de bain / chambre avant ; un conduit (rectangle blanc) dedans")
el("BAIN", "baignoire", "Baignoire", "(non écrit)", 24.5, 190, 25, 54, None, rot=90,
   note="rectangle le long du mur gauche sous la fenêtre de la S. de bain")
el("LAVABO", "lavabo", "Lavabo", "(non écrit)", 57, 206.5, 11, 11, None,
   note="trapèze contre la cloison arrière de la S. de bain ; petit cadre au-dessus contenant la cote « 9'-0\" » (miroir/tablette ?)")
el("WC", "toilette", "Toilette (probable)", "(non écrit)", 59, 166, 20, 16, None,
   note="contour arrondi contre la cloison avant de la S. de bain avec un cercle-croix : interprété comme cuvette ; pourrait être un luminaire")
el("PHARM", "autre", "Armoire à pharmacie (?)", "TAB. À MÉD.", 90, 212, 22, 20, "TAB. À MÉD.",
   note="lecture incertaine (« TAN. À MÉD. » / « TAB. À MÉN. ») ; cadre contre la cloison droite de la S. de bain")
el("TRAPPE", "trappe", "Trappe d'accès (plafond ?)", "TRAPPE", 61, 188, 27, 17, "TRAPPE",
   note="rectangle en tirets dans la S. de bain (tirets = au-dessus, probablement trappe d'entretoit)")
el("EVIER", "evier", "Évier", "ÉVIER", 374, 360.5, 31, 19, "EVIER", note="sous la fenêtre de la cuisine")
el("ARM-AR", "armoires", "Armoires bas et haut (mur arrière)", "ARMOIRES BAS / HAUT", 387.5, 360, 66, 29, "ARMOIRES BAS HAUT",
   note="comptoir/armoires le long du mur arrière de la cuisine ; « HAUT » avec flèche vers le mur droit")
el("ARM-DR", "armoires", "Armoires (mur droit)", "(voir ARMOIRES BAS / HAUT)", 432, 323.5, 22, 93, None,
   note="bande d'armoires le long du mur droit contenant le poêle et le réfrigérateur")
el("POELE", "cuisiniere", "Cuisinière (poêle) 220 V", "POÊLE 220", 431.5, 330.5, 25, 31, "POELE 220",
   note="« 220 » = prise 220 V")
el("REF", "refrigerateur", "Réfrigérateur", "RÉF.", 432.5, 290.5, 22, 27, "REF.")
el("COMPT", "comptoir", "Comptoir (bout arrondi)", "COMPTOIR", 412.5, 259, 63, 21, "COMPTOIR",
   note="contre le mur droit, bout gauche arrondi (presqu'île)")
el("LAV", "laveuse", "Laveuse", "LAV.", 332, 273, 28, 29, "LAV.", note="adossée à la cloison d'escalier côté cuisine")
el("SEC", "secheuse", "Sécheuse 220 V", "SEC. 220", 332, 304.5, 28, 32, "220 SEC.", note="« 220 » = prise 220 V")
el("ARM-EAR", "armoires", "Armoires de l'entrée arrière", "ARMOIRES", 243, 409, 32, 50, "ARMOIRES",
   note="le long du mur gauche de l'entrée arrière")
LUM = [("L01", 73, 301, "chambre arrière", "croix sans cercle"), ("L02", 78, 84, "chambre avant", None),
       ("L03", 224, 293, "chambre d'utilité", None), ("L04", 197, 180, "dégagement / passage (près du mot PASSAGE)", None),
       ("L05", 196, 34, "entrée avant", None), ("L06", 293, 355, "palier de l'escalier", None),
       ("L07", 293, 412, "entrée arrière", "croix"), ("L08", 336, 411, "extérieur, au-dessus des marches arrière", None),
       ("L09", 381, 311, "cuisine", None), ("L10", 380, 210, "cuisine / s.-à-manger (sur la poutre)", None),
       ("L11", 181, -10, "extérieur, perron avant", None)]
for code, x, y, ou, sym in LUM:
    el(code, "autre", "Luminaire plafonnier — " + ou, "(symbole cercle-croix)", x, y, None, None, None,
       note="symbole " + (sym or "cercle-croix") + " ; position ESTIMÉE")

# ---------------------------------------------------------------- STRUCTURE
S = []
def st(code, typ, txt, val, sens, geo, note, src="LU"):
    S.append({"id": "str-RDC-" + code, "type": typ,
              "dimension": {"texte_original": txt, "valeur": val, "source": src, "photo": "P3"},
              "sens": sens, "geometrie": geo, "note": note})
st("S01", "solives", "SOLIVES 2\"x7\" @ 16\" c/c", "2x7 @ 16 c/c", "y",
   {"zone": [[175, 204], [275, 374.5]], "espacement": 16},
   "écrit dans la chambre d'utilité, trait à deux butées orienté en y (avant-arrière) → solives parallèles à y ; probablement solives de plafond (non précisé)")
st("S02", "solives", "SOLIVES 2\"x7\" @ 16\" c/c", "2x7 @ 16 c/c", "y",
   {"zone": [[222, 5.5], [450.5, 157]], "espacement": 16},
   "écrit dans le salon, trait à deux butées orienté en y ; probablement solives de plafond")
st("P01", "poutre", "POUTRE 6\"x10\" FLUSH", "6x10", "x",
   {"x1": 316, "y1": 212, "x2": 450.5, "y2": 213},
   "poutre affleurante (« FLUSH ») traversant la cuisine de la cloison d'escalier au mur droit ; position y NON cotée (ESTIMÉ ≈ 17'-8\" du nu ext. avant) ; dans l'alignement de la cloison avant de la ch. d'utilité (y=204) à ~8 po près", src="LU")
LT = [("L01", "LINTEAU 2-2\"x8\"", "2-2x8", "ouv-RDC-001", 98, h), ("L02", "LINTEAU 2-2\"x10\"", "2-2x10", "ouv-RDC-002", 377, h),
      ("L03", "LINTEAU 2-2\"x8\"", "2-2x8", "ouv-RDC-003", 98, 374.5), ("L04", "LIN. 2-2\"x6\"", "2-2x6", "ouv-RDC-004", 197, 374.5),
      ("L05", "LINTEAU 2-2\"x8\"", "2-2x8", "ouv-RDC-005", 375, 374.5), ("L06", "LIN. 2-2\"x6\"", "2-2x6", "ouv-RDC-006", h, 191),
      ("L07", "LIN. 2-2\"x6\"", "2-2x6", "ouv-RDC-007", 450.5, 180)]
for code, txt, val, oid, x, y in LT:
    ob = next(o for o in O if o["id"] == oid)
    w = ob["largeur"]["valeur"]
    if y in (h, 374.5):
        g = {"x1": x - w / 2, "y1": y, "x2": x + w / 2, "y2": y}; s = "x"
    else:
        g = {"x1": x, "y1": y - w / 2, "x2": x, "y2": y + w / 2}; s = "y"
    st(code, "linteau", txt, val, s, g, "linteau de " + oid + " (2 pièces de 2\" ; longueur = baie, appuis non indiqués)")

# ---------------------------------------------------------------- NOTES
N = [
    ("01", "• REZ-DE-CHAUSSÉE •", "titre de la feuille : plan du rez-de-chaussée", "P6"),
    ("02", "ÉCHELLE : 1/4\" = 1'-0\"", "échelle 1:48 ; le dessin n'est pas fiable pour la mesure (les cotes priment), quoique l'homographie montre une bonne concordance (±3 po)", "P6"),
    ("03", "NOTE : BARRE & TABLETTE DANS TOUS LES G.R.", "tringle et tablette dans toutes les garde-robes", "P3"),
    ("04", "BÉTON REN. AVEC BARRE ½\"Ø @ 10\" c/c", "perron en béton renforcé (armé) de barres de ½ po de diamètre espacées de 10 po centre à centre", "P3"),
    ("05", "SOLIVES 2\"x7\" @ 16\" c/c (×2 : ch. d'utilité et salon)", "solives de 2x7 po à 16 po c/c, orientées avant-arrière (y) ; plafond probablement", "P3"),
    ("06", "POUTRE 6\"x10\" FLUSH", "poutre de 6x10 po affleurante (dans l'épaisseur du plafond) au-dessus de la cuisine/s.-à-manger", "P3"),
    ("07", "RAMPE", "main courante de l'escalier du sous-sol, côté gauche (ch. d'utilité)", "P3"),
    ("08", "2.R. 14 C.M.", "escalier de 14 contremarches vers le sous-sol ; préfixe « 2.R. » (ou « E.R. ») non interprété", "P3"),
    ("09", "ARMOIRES BAS / HAUT", "armoires basses et hautes de cuisine", "P3"),
    ("10", "POÊLE 220 ; SEC. 220", "prises 220 V pour la cuisinière et la sécheuse", "P3"),
    ("11", "SW ; 3W ; $ ; symboles ⊖ (cercle barré)", "symboles électriques : SW/$ = interrupteur, 3W = interrupteur 3 voies (haut de l'escalier, hall), cercles barrés le long des murs = prises de courant ; lignes tiretées = commande des luminaires ; non inventoriés un à un", "P3"),
    ("12", "PASSAGE", "nom du couloir entre le hall et la cuisine", "P3"),
    ("13", "TAB. À MÉD.", "armoire/tablette à médicaments dans la S. de bain (lecture incertaine)", "P3"),
    ("14", "ARMOIRES (entrée arrière)", "armoires de rangement dans l'entrée arrière", "P3"),
]
NOTES = [{"id": "note-RDC-" + a, "texte_original": b, "interpretation": c, "photo": d} for a, b, c, d in N]

# ---------------------------------------------------------------- OBSERVATIONS
OBS = [
    "Chaîne arrière rang 3 (cote-RDC-016/017/018) : 18'-3\" + 9'-0\" + 10'-9\" = 38'-0\" ; si le dernier chiffre est lu 5 (10'-5\"), la chaîne ne fait que 37'-8\" (−4\"). Le glyphe est identique au 9 de « 9'-0\" » de la même chaîne → lu 9, à confirmer.",
    "Chaîne arrière rang 2 (cotes 019-023) : 8'-2\"+8'-3\"+8'-0\"+6'-10\"+6'-9\" = 38'-0\" ; avec 6'-5\" = 37'-8\". Même ambiguïté S/9 que ci-dessus ; les deux chaînes arrière se corroborent si on lit 9.",
    "Entrée arrière : 8'-2\"+8'-3\"+8'-0\"+2'-9\" = 27'-2\" alors que 18'-3\"+9'-0\" = 27'-3\" pour le nu ext. droit de l'entrée → écart de 1\".",
    "Fenêtre de l'entrée arrière : « 3'-6\" » ou « 3'-0\" » (2e chiffre traversé par un trait de cote) ; dessin ≈ 39 po.",
    "Profondeur du volume de l'entrée arrière, profondeur/longueur des marches arrière et du perron avant : aucune cote écrite → ESTIMÉ seulement (entrée ≈ 5'-7\" hors-tout, marches arr. ≈ 6'-4\" x 4'-5\", perron ≈ 5'-7\" x 4'-5\").",
    "ARCHE hall/salon : texte lu « 4'-0\" » (glyphe 4 net sur P3, P4, P6) mais l'ouverture dessinée mesure ≈ 74 po (≈ 6'-2\"), aussi grande que l'« ARCHE 6'-0\" » salon/cuisine (≈ 73 po).",
    "Porte de la chambre d'utilité étiquetée « 2'-6\"x6'-8\" » (alt. 2'-4\") dans une baie de 2'-5\" d'axe en axe (cote-RDC-031) : une porte de 30 po (ou 28 po) ne peut pas y tenir avec ses montants.",
    "Cotes intérieures : elles ne sont pas des dimensions nettes de pièce — chaque chaîne intérieure ferme exactement sur le hors-tout (38'-0\" ou 31'-8\"), donc elles vont du nu ext. des murs extérieurs à des repères de cloisons (axe ou nu : à déterminer en Phase 2). Les 4 « 13'-1\" » (2 chambres, salon ×2) et les 12'-2\" / 9'-0\"+3'-2\" sont cohérents entre eux.",
    "Toutes les chaînes ferment : gauche 15'-9\"+15'-11\" ; droite 16'-8\"+15'-0\" ; avant 8'-2\"+8'-5\"+14'-10\"+6'-7\" ; int. x 9'-0\"+3'-2\"+2'-5\"+8'-4\"+3'-5\"+11'-8\" ; int. x avant 12'-2\"+2'-5\"+3'-11\"+19'-6\" ; int. y 13'-1\"+5'-6\"+13'-1\", 14'-8\"+3'-11\"+13'-1\", 18'-7\"+13'-1\".",
    "Petite cote « 9\" » (guillemets à gauche, peut-être « 6\" » tête-bêche) sur la cloison chambre arrière / S. de bain : seule épaisseur de mur écrite ; le dessin montre ≈ 5 po. Épaisseurs des murs ext. (≈ 11 po) et des cloisons (≈ 6 po) : ESTIMÉES seulement.",
    "Escalier : « 14 C.M. » écrit mais ~10 girons dessinés entre le palier et le BALAIS ; préfixe « 2.R. » (ou « E.R. ») non compris.",
    "La porte de la chambre arrière et celle de la ch. d'utilité sont dessinées ~11 po en avant de la cloison chambre arr./S. de bain (y≈212 vs 223) : baie en retrait, sans mur plein.",
    "Le « VEST. » (vestiaire) n'a pas de porte dessinée ; ouvert sur l'entrée avant.",
    "Rez-de-chaussée : aucune hauteur de plafond écrite ; aucune mention de mur porteur ; la poutre 6x10 FLUSH de la cuisine n'est pas cotée en position.",
    "Le symbole cercle-croix dans la S. de bain est dessiné dans le contour de la toilette : toilette ou luminaire ? Aucune autre toilette n'est dessinée.",
    "Les étiquettes de portes (ex. 2'-6\"x6'-8\") sont portées dans ouvertures[].texte_original et non dans cotes[].",
]

niveau = {
    "id": "RDC", "nom": "Rez-de-chaussée", "feuille": "A-101",
    "photos_sources": ["P3", "P4", "P6"],
    "hauteur_plafond": D(None, "ILLISIBLE", photo=None, note="aucune hauteur de plafond écrite sur la feuille"),
    "calage_estime": {
        "methode": "homographie P3 (pixels prep/redresse/P3.jpg) → pouces, calée sur les 4 coins ext. du rectangle principal",
        "points_px": {"arriere_gauche": [489, 216], "arriere_droit": [2065, 280], "avant_gauche": [427, 1632], "avant_droit": [2093, 1630]},
        "points_po": {"arriere_gauche": [0, 380], "arriere_droit": [456, 380], "avant_gauche": [0, 0], "avant_droit": [456, 0]},
        "controle": "cloisons à x=108/146/175/275/316 et y=157/204/223 retrouvées à ±4 po ; centres de fenêtres à ±3 po"},
    "murs": M, "ouvertures": O, "pieces": P, "elements": EL, "structure": S,
    "cotes": C, "notes": NOTES, "observations": OBS,
}
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(niveau, f, ensure_ascii=False, indent=2)
print(len(M), len(O), len(P), len(EL), len(S), len(C), len(NOTES), len(OBS))
