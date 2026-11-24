# RDC-01 — État actuel du rez-de-chaussée (relevé photo du 2026-11-01)

Ce dossier n'est **pas une proposition** : c'est le rez-de-chaussée tel qu'il est aujourd'hui, modélisé à partir des
15 photos du propriétaire (`renovation/prive/rdc_actuel/01.jpg` à `15.jpg`, gardées hors du dépôt) et du plan de base
R0 (A-101). Il sert de point de départ aux futures propositions RDC-02 et suivantes.

- Plan : `png/R-101_rdc.png` (feuille R-101) ; le sous-sol (R-100) est la base, inchangée.
- Maquette : `3d/visite.html` (16 arrêts, du hall d'entrée à l'entrée arrière).
- Générer : `python3 renovation/outils/construire_projet.py renovation/RDC-01_etat_actuel` puis
  `python3 renovation/outils/generer_3d.py renovation/RDC-01_etat_actuel`.

## Ce qui a été modélisé, et d'après quelles photos
| Pièce | Photos | Modélisé |
|---|---|---|
| Cuisine | 01, 02, 03, 08 | Mur de brique rouge à joints pâles (mur arrière à partir du poteau, mur de droite) ; armoires du bas noir mat ; comptoirs de bois de grange ; évier double noir et robinet noir sous la fenêtre (cadrage noir, store noir) ; lave-vaisselle inox ; cuisinière inox 30 po, hotte cheminée inox, deux tablettes flottantes de bois ; colonne d'armoires noires pleine hauteur avec frigo inox encastré ; frigo à portes françaises devant la fenêtre du mur de droite ; îlot noir 40 × 84 po à dessus de bois de grange, 3 tabourets de cuir noir côté salle à manger ; poubelles inox ; tuile d'ardoise noire 24 po ; encastrés |
| Salon | 02, 03, 04 | Poutre et poteaux de bois brut teint ; plafond crépi ; grande fenêtre de façade à cadrage de pin, store gris ; sectionnel gris pâle en L à inclinables (dos au mur du hall, retour face à la fenêtre) ; grand tableau coloré **générique** ; télé murale et meuble flottant gris-bois sur le mur de droite ; thermopompe murale ; plante |
| Hall et entrée | 04, 05, 09 | Murs vert sauge ; mur de cadres **génériques** (aucune photo de famille reproduite) ; banc blanc ; vieille porte blanche décorative avec crochets ; ouverture vers le salon encadrée de bois brut (poutre et poteaux) ; ardoise à l'entrée avant |
| Dégagement (corridor) | 05, 06, 09 | Portes de pin teint à panneaux horizontaux, gros cadrages de pin ; trappe du grenier au plafond ; portes de garde-robes et de la lingerie fermées |
| Coin bureau | 05, 06 | Bureau flottant dans le renfoncement à côté du poteau, écran large, petit écran au mur, chaise noire |
| Salle à manger | 06, 07, 08 | Grande table de bois de récupération foncé, 8 chaises noires, luminaire linéaire noir suspendu ; buffet de bois sous un grand tableau **générique** ; tableau noir (ardoise) encadré de pin au mur arrière ; poteau de bois brut contre le mur arrière ; baie vers l'entrée arrière à chambranle noir ; bande d'ardoise devant la baie (prolongement de la cuisine) |
| Chambre arrière | 10, 11, 12 | Papier peint imitation planches grises au mur de tête de lit ; lit queen ; table de chevet blanche ; cadres de paysages brumeux **génériques** ; suspension cage noire ; commode blanche ; vélo de route sur base d'entraînement devant la fenêtre, tapis noir ; store et cantonnière marine |
| Salle de bain | 13, 14, 15 | Laveuse et sécheuse frontales blanches empilées (à gauche en entrant), muret tuilé ; douche vitrée coulissante à cadre noir, tuile blanche, niche ; toilette sous la fenêtre (cadrage de pin) ; vanité noire à deux vasques blanches, robinets noirs hauts ; deux miroirs ronds à cadre noir (un DEL) ; tablettes de fil noir ; plancher de porcelaine grise |
| Chambre avant | — | **Non photographiée** : lit queen, deux tables de chevet et une commode blanche, présumés |
| Entrée arrière | 01, 07, 08 | Ardoise au sol ; l'escalier qui descend et sa main courante (visibles sur les photos) ne sont pas modélisés |

Matériaux ajoutés au catalogue (CC0) : `brique_rouge` (Poly Haven red_brick_03), `ardoise_noire` (ambientCG Tiles138,
carreaux de 24 po), `erable` (ambientCG WoodFloor047, éclairci), `bois_grange` (Poly Haven weathered_brown_planks),
`bois_brut` (ambientCG Wood060), `pin_teint` (Poly Haven coated_pine_02), `papier_planches` (Poly Haven
wood_planks_grey), `crepi` (Poly Haven white_stucco_02), `bois_recupere` (Poly Haven wood_cabinet_worn_long).
Les couleurs de peinture (blanc cassé, vert sauge, noir mat) sont **estimées sur les photos**, sans référence de nuancier.

## Hypothèses
- **Hauteur de plafond : 96 po (8 pi), PRÉSUMÉE** — aucune hauteur sur la base ni sur les photos ; à mesurer.
- Fenêtres : allège 34 po, tête 82 po (estimées sur les photos, la même pour toutes).
- Dimensions du mobilier et des appareils : standards (cuisinière 30 po, frigo 36 po, laveuse 27 po, lit queen
  60 × 80 po) ; positions estimées sur des photos grand-angle (déformation aux bords) — précision de l'ordre de 6 po.
- Îlot : 40 × 84 po, dégagements d'environ 42 po vers le comptoir arrière et la colonne d'armoires.
- Table de la salle à manger : 46 × 94 po.

## Écarts avec le plan de base, à vérifier sur place
1. **Salle de bain plus profonde que la base (source PHOTO)** : laveuse-sécheuse (≈ 28 po), douche (≈ 34 po), passage
   (≈ 22 po) et vanité (≈ 20 po) ne tiennent pas dans les 61 po de la base. La cloison salle de bain / chambre avant
   (`mur-RDC-R01`) est reportée de 15 po vers l'avant (y 157 → 142) ; la chambre avant perd d'autant
   (124 pi² au lieu de 134). **Mesurer la profondeur de la salle de bain et de la chambre avant.**
2. **Porte de la salle de bain (source PHOTO)** : déplacée d'environ 10 po vers l'arrière (centre y ≈ 188) pour que la
   laveuse-sécheuse soit à côté de la porte comme sur la photo 13. À mesurer.
3. **Poutre de l'axe B (source PHOTO)** : apparente (bois brut teint) seulement du hall au mur de droite ; du côté des
   chambres, rien n'est visible (cachée dans le plafond ou les cloisons). À confirmer.
4. **Poutre au-dessus de l'ouverture hall / salon (source PHOTO, `str-RDC-R01`)** : visible sur les photos 03 à 05,
   absente de la base ; décorative ou porteuse, à vérifier. Le bout de la cloison du hall est habillé de bois brut.
5. **Poteau contre le mur arrière de la salle à manger** (photo 07), à côté de la baie de l'entrée arrière : absent de
   la base ; probablement l'ancien bout de la cloison de 1957 (`mur-RDC-027`). Modélisé comme habillage, pas comme structure.
6. Le placage de brique couvre aussi la partie du mur de droite derrière la colonne d'armoires (présumé).
7. Limite de l'ardoise dans la salle à manger (bande devant la baie de l'entrée arrière) : forme estimée sur la photo 07.

## Ce qui reste imparfait
- Entrée arrière : l'escalier qui descend et la main courante ne sont pas modélisés (la visionneuse ne sait pas
  dessiner un plancher plus bas).
- Les portes de garde-robe blanches de la chambre arrière sont rendues en pin comme les autres (une seule essence de
  porte par maquette).
- Chambre avant non photographiée : mobilier présumé.
- Les objets du quotidien (jouets, vêtements, paniers) ne sont pas représentés.
