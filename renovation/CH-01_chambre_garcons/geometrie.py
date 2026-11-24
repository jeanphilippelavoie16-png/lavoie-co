"""CH-01 — repères de la chambre des garçons (chambre avant du rez-de-chaussée), partagés par modifs.py (plan P-131) et
scene_3d.py (maquette) : une seule source pour les positions et les dimensions.

Pouces ; x le long de la façade (croissant vers la droite vu de la rue), y vers l'arrière (façade 0), z depuis le plancher
du rez-de-chaussée. Origine : coin extérieur avant gauche de la fondation (comme releve/livrables/donnees/maison.json).
Sources : PLAN = base R0 et relevé RDC-01 ; DAG = vidéo de l'architecte paysagiste (MAISON-18/fenetres_video.py) ;
PHOTO = photos du client du 2026-11-09 (renovation/prive/chambre_avant/, hors du dépôt), dimensions ESTIMÉES sur les
photos (grand-angle, précision de l'ordre de 2 à 4 po) ; PROPOSÉ = rangement, coin jeu et thème (version 2).
"""

# --------------------------------------------------------------------------- enveloppe (PLAN)
XG, XD = 10.0, 143.75          # nu du mur gauche (extérieur, axe x = 5) ; nu de la cloison de droite (axe x = 146)
YF, YA = 10.0, 139.75          # nu de la façade (axe y = 5) ; nu de la cloison de la salle de bain (mur-RDC-R01, axe y = 142)
NICHE = (110.25, 139.75, 143.75, 154.75)    # renfoncement de la porte (x0, y0, x1, y1) ; porte au fond, y = 157
GR = (148.25, 56.25, 172.75, 131.75)        # garde-robe : 24½ × 75½ po au nu intérieur (ESTIMÉ, plan R0)
PLAFOND = 96                   # PRÉSUMÉ (8 pi), comme RDC-01 et MAISON-18 : à mesurer

# --------------------------------------------------------------------------- fenêtre de façade ouv-RDC-001
FEN = (60.5, 135.5)            # baie (PLAN, largeur 6'-3" LU)
ALLEGE, TETE = 37.5, 80.0      # DAG (MAISON-18), cohérent avec les photos à quelques pouces près
SECTIONS = 3                   # PHOTO 10 : trois châssis égaux ; manivelle sur celui de droite vu de l'intérieur (x bas)
CARREAUX = {"hauteur": 9.5, "rangs": 2, "colonnes": 3}    # PHOTO 02, 10 : bande de petits carreaux en haut de chaque châssis
CHAMBRANLE = 4.5               # PHOTO : chambranle plat de pin teint, coins d'onglet (≈ 4 à 5 po)

# --------------------------------------------------------------------------- portes (PLAN)
PORTE_CH = (112.0, 142.0)      # porte de la chambre (ouv-RDC-014), x ; charnière côté x = 142, ouvre dans la chambre
PORTE_GR = (78.0, 108.0)       # porte de la garde-robe (ouv-RDC-021), y ; charnière côté y = 78 (PHOTO 05, 06 : poignée côté arrière)

# --------------------------------------------------------------------------- existant gardé (PHOTO, ESTIMÉ)
LITS = (11.0, 96.5, 91.5, 139.5)            # lits superposés simple sur simple ≈ 80½ × 43 po, tête au mur vert (x = 10)
LITS_H = 63.0                                # haut des garde-corps du lit du haut ≈ 63 po
ECHELLE = (61.5, 76.5, 74.5)                 # échelle inclinée : x0, x1, y du pied (le haut s'accroche au lit à y = 96,5)
COMMODE = (127.75, 18.0, 143.75, 66.0)       # commode blanche basse ≈ 48 × 16 po, devant vers −x
COMMODE_H = 27.0                             # ≈ 27 po (3 rangs de tiroirs sur pattes grises)

# plinthes chauffantes électriques blanches (PHOTO 01 à 03, 08, 09, 12 : longueurs et bouts ESTIMÉS)
PC_AVANT = (26.0, 10.5, 122.0, 13.5)         # sous la fenêtre (96 po)
PC_GAUCHE = (10.5, 22.0, 13.5, 94.0)         # mur vert (72 po), jusqu'au pied des lits
PC_Z = (0.6, 8.1)

# --------------------------------------------------------------------------- version 2 (2026-11-09, révision B) : PROPOSÉ
# Réponse du client : pas de table, du RANGEMENT d'abord, un coin jeu ouvert au plancher, un thème d'enfant moderne.
# coin jeu ouvert : grand tapis plat (4½ × 7 pi), à ≈ 6 po de la plinthe de la fenêtre et ≈ 10½ po de celle du mur de gauche
TAPIS = (24.0, 19.5, 108.0, 73.5)
COUSSINS = ((40.0, 37.0, 9.0), (58.0, 31.0, 9.0))    # deux coussins de sol ronds (18 po) : x, y, rayon

# bacs roulants sous le lit du bas (PHOTO 07, 08, 11, 12 : dessous de la traverse du lit du bas ≈ 7½ à 8 po du plancher,
# ESTIMÉ à partir de la plinthe chauffante voisine ; à mesurer) ; ils sortent vers le tapis (−y)
BACS_Y = (97.0, 127.0)            # face avant (rangé, sous la traverse) → arrière : 30 po de profond
BACS_X = ((21.0, 40.0), (41.5, 60.5), (77.5, 88.5))    # entre la patte de tête, l'échelle (x 61,4 → 76,6) et la patte du pied
BACS_H = 6.25                     # roulettes comprises : ≈ 1¾ po sous la traverse (z 8)
BACS_COURSE = 22.0                # sortis : face avant à y ≈ 75 (le pied de l'échelle est à 74,5, à côté)

# mur de droite autour de la commode : livres de face à leur hauteur, armoires fermées au-dessus (parents)
REBORDS = (139.75, 143.75, (33.0, 44.5))     # deux rebords à livres de face au-dessus de la commode : x0, x1, z des rebords
REBORDS_Y = (19.0, 65.0)
ARMOIRES = (131.75, 18.0, 143.75, 66.0)      # armoires murales 12 po de profond, 2 portes de 24 po, au-dessus de la commode
ARMOIRES_Z = (57.0, 84.0)
TABLETTE_HAUTE = (132.75, 16.0, 143.75, 116.0)   # tablette haute de chêne (11 po) au-dessus des armoires et de la porte de la G.-R.
TABLETTE_HAUTE_Z = 85.5                          # dessous (dessus à 87) : 9 po libres sous le plafond présumé (boîtes de 7½ po)
PATERES = (114.5, 123.5, 44.0)                   # 3 patères sur une latte de chêne, entre la G.-R. et la porte de la chambre

# coin de la porte : la tour aux albums (albums debout, bac à toutous en bas)
ALBUMS = (92.5, 127.0, 110.0, 139.75)
ALBUMS_H = 42.0

# murale du mur de gauche (ancien mur vert) : image plane peinte, du dessus de la plinthe au plafond
MURALE = (10.0, 139.75, 4.0, 96.0)           # y0, y1, z0, z1
ENSEIGNES_DY, ENSEIGNES_DZ = -16.0, 17.0     # enseignes remontées dans le ciel de la murale (décalage depuis leur place actuelle)

# garde-robe aménagée (gardée de la version 1)
GR_ETAGERE = (156.75, 79.0, 172.75, 107.0)   # bacs et tiroirs à Lego, face à la porte
GR_PENDERIE = (56.25, 79.0)                  # aile gauche (y) : tringles à 42 et 78 po
GR_AILE_D = (107.0, 131.75)                  # aile droite (y) : tablettes de bacs saisonniers
GR_TABLETTE_Z = 83.0
