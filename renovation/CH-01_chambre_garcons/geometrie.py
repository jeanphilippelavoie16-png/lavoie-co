"""CH-01 — repères de la chambre des garçons (chambre avant du rez-de-chaussée), partagés par modifs.py (plan P-131) et
scene_3d.py (maquette) : une seule source pour les positions et les dimensions.

Pouces ; x le long de la façade (croissant vers la droite vu de la rue), y vers l'arrière (façade 0), z depuis le plancher
du rez-de-chaussée. Origine : coin extérieur avant gauche de la fondation (comme releve/livrables/donnees/maison.json).
Sources : PLAN = base R0 et relevé RDC-01 ; DAG = vidéo de l'architecte paysagiste (MAISON-18/fenetres_video.py) ;
PHOTO = photos du client du 2026-11-09 (renovation/prive/chambre_avant/, hors du dépôt), dimensions ESTIMÉES sur les
photos (grand-angle, précision de l'ordre de 2 à 4 po) ; PROPOSÉ = coin jeu.
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

# --------------------------------------------------------------------------- coin jeu (PROPOSÉ)
TABLE = (26.0, 27.5, 56.0, 51.5)             # table à Lego 30 × 24 po, dessus à 20 po ; ≈ 1 pi des plinthes chauffantes
TABLE_Z = 20.0
TABOURETS = ((34.0, 59.0), (48.0, 59.0))     # deux tabourets de 12 po (assise 11 po de diamètre)
REBORDS = (139.75, 143.75, (34.0, 45.5))     # rebords à livres de face au-dessus de la commode : x0, x1, z des rebords
REBORDS_Y = (19.0, 65.0)
TOUR = (92.0, 124.5, 109.5, 139.5)           # tour de 3 bacs près de la porte, au pied des lits (17½ × 15 × 39 po)
TOUR_H = 39.0
TAPIS = (100.0, 58.0, 28.0)                  # tapis rond : centre x, y et rayon (56 po)

# garde-robe aménagée
GR_ETAGERE = (156.75, 79.0, 172.75, 107.0)   # bacs et tiroirs à Lego, face à la porte
GR_PENDERIE = (56.25, 79.0)                  # aile gauche (y) : tringles à 42 et 78 po
GR_AILE_D = (107.0, 131.75)                  # aile droite (y) : tablettes de bacs saisonniers
GR_TABLETTE_Z = 83.0
