# MAISON-18 — Fenêtres aux dimensions de la vidéo DAG (2026-11-02)

## Demande
Le client a envoyé 12 captures de la vidéo de son architecte paysagiste (DAG), puis a dit : « les fenêtres dans la vidéo
sont de bonnes dimensions ». Les fenêtres de la maquette prennent donc les dimensions de la vidéo : largeur, allège
(bas de la fenêtre au-dessus du plancher de son étage), tête (haut de la fenêtre) et nombre de sections.
Les fenêtres qu'on ne voit pas dans la vidéo gardent leurs valeurs. Les portes ne changent pas.

Tout est dans `fenetres_video.py` (tableau `FENETRES`), appelé par :
- `modifs.py` pour les plans P-129 et P-130 et `maison.json` (`appliquer_plans`) ;
- `zone_global.py` pour la 3D du sous-sol et `base_rdc01_scene.py` pour la 3D du rez-de-chaussée (`reglages_3d`, `meneaux_3d`).

## Avant / après
Pouces. Centre = x pour les murs avant et arrière, y pour le mur de droite. Allège et tête sont comptées depuis le
plancher de l'étage. **Gras** = valeur changée.

| Fenêtre | Pièce | Largeur | Centre | Allège | Tête | Sections |
|---|---|---|---|---|---|---|
| ouv-RDC-001 | Bureau (façade) | 75 → 75 | 98 | 34 → **37½** | 82 → **80** | 2 égales → **2 inégales, 1/3 + 2/3** (petite côté x 0) |
| ouv-RDC-002 | Salon (façade) | 108 → 108 | 377 | 20 (hyp.) → **12** | 82 → **80** | 3 → **2 inégales, 3/4 + 1/4** (petite côté allée) |
| ouv-RDC-003 | Chambre des parents (arrière) | 75 → 75 | 98 | 34 → **23½** | 82 → **80** | 2 → **3** |
| ouv-RDC-004 | Salle à manger (arrière) | 36 → 36 | 197 | 34 → **37½** | 82 → **80** | 2 → 2 |
| ouv-RDC-005 | Cuisine, évier (arrière) | 75 → 75 | 375 | 34 → **37½** | 82 → **80** | 2 → **3** |
| ouv-RDC-007 | Cuisine (mur de droite) | 36 → 36 | y 180 | 34 → **24** | 82 → **80** | 2 → 2 |
| ouv-RDC-008 | Entrée arrière (face arrière) | 42 → **36** | 293 | 34 → **38** | 82 → **80** | 2 → 2 |
| ouv-SS-002 | Séjour (façade) | 75 → **72** | 382 → **395** | 40 (hyp.) → **44** | 86 → **80** | 2 → **3** |
| ouv-SS-003 | Chambre 2 (mur de droite) | 80 → **84** | y 308 | 40 (hyp.) → **44** | 86 → **80** | 2 → **3** |
| ouv-SS-004 | Séjour (mur de droite) | 36 → 36 | y 75 | 40 (hyp.) → **44** | 86 → **80** | 2 → 2 |

Hauteurs qui en découlent : salon 68 po ; chambre des parents 56½ ; cuisine (mur de droite) 56 ; bureau, salle à manger
et cuisine (évier) 42½ ; entrée arrière 42 ; sous-sol 36.

Gardées telles quelles, car on ne les voit pas dans la vidéo :
- ouv-RDC-006 (salle de bain du RDC, mur gauche) : 36 po, allège 34, tête 82 ;
- ouv-SS-006 et ouv-SS-007 (salle de bain et salle de lavage du SS, mur gauche) : allège 56, tête 86 ;
- ouv-SS-009 et ouv-SS-010 (chambre 1, mur arrière) : 40 po, allège 40, tête 86. Elles sont cachées par le deck dans
  la vidéo. Sur la capture 11, la vidéo ne dessine aucune fenêtre à l'endroit de ouv-SS-010. C'est pourtant une fenêtre
  d'évacuation exigée : on la garde, et c'est au client de décider.

## Méthode
Deux relevés indépendants des captures ont été faits, puis comparés :
- **A** : homographies (DLT 1D et 4 points), bords lus au demi-pixel, correction du lacet (capture 01) et de la parallaxe
  (capture 10) ;
- **B** : profils de luminance et de R−G (la brique contre les cadres noirs), agrandissements, rangs de brique pour les
  rapports de profondeur.

Repères : l'échelle horizontale vient de la largeur de la maison (456 po) ; la porte avant mesure 34 × 79 po dans la
vidéo, ce qui confirme cette échelle. Le plancher du RDC est pris au bas de la porte avant. Le plancher du SS est à 105 po
plus bas : la porte de côté du SS retombe bien sur ce plancher. Les mesures se font sur la 01 (avant, presque de face),
la 10 (arrière, de face) et la 03 (mur de droite, de biais), puis on recoupe avec les captures 02, 07, 09 et 11.

Règles de décision :
1. **Tête à 80 po partout.** Dans la vidéo, toutes les fenêtres montent jusqu'au soffite, à la hauteur de la tête des
   portes (79 à 80 po). La maquette dessine toutes les portes à 80 po : on met donc la tête des fenêtres à 80 po, et
   l'alignement fenêtres / portes de la vidéo est gardé. La vidéo a un mur très bas (79 po du plancher au soffite, contre
   96 po dans la maquette). La hauteur de la brique ne peut donc pas servir d'échelle.
2. **Largeur et centre du plan gardés** quand la vidéo s'en écarte de moins que l'incertitude de mesure : environ 2 po sur
   les captures 01 et 10, 3 à 4 po sur la 03. Ce sont des cotes lues (LU) sur le plan : elles sont plus fiables qu'une
   lecture de pixels. Au-delà de l'incertitude, la vidéo fait foi.
3. **Centre déplacé seulement si l'écart est flagrant et confirmé par les deux relevés.** Un seul cas : ouv-SS-002.
4. **Sections comptées sur les vitres.** Le moteur ne fait que des meneaux également répartis. Les deux fenêtres de façade
   à sections inégales reçoivent donc `"sections": 1`, et leur meneau est ajouté au mobilier, identique à celui du moteur
   (1½ × 2½ po, noir, dans le plan de la vitre).

## Écarts entre les relevés et comment ils ont été tranchés
| Fenêtre | A | B | Décision |
|---|---|---|---|
| ouv-SS-003, largeur | 80 (84,4 brut, ramené de 1 px) | 85 (± 5) | **84**. Recoupe sur la 03 : cadre noir sur crépi, homographie du mur, bords à mi-niveau : 83,5 ± 1,5 po selon la position du coin arrière. La même mesure redonne 35,7 po pour ouv-SS-004 et 35,2 po pour la porte de côté (36 au plan) : il n'y a pas de biais d'un pixel, et la correction de A ne tient pas. |
| ouv-RDC-007, largeur | 36 (38,6 brut) | 40 (39,7–41,8) | **36 (plan gardé)**. Écart de 4 po, à la limite. Recoupe sur la 03 en R−G : 31 à 35 po (brique peu contrastée, une seule capture de biais). Rien ne justifie de l'élargir. |
| ouv-SS-002, largeur et centre | 73, centre 394 | 71 (69,4 sur la 02), centre 395 | **72, centre 395**. Recoupe sur la 01 : 72,1 po, x 358,2 à 430,3. On aligne le bord droit à 431, sur celui de ouv-RDC-002, comme dans la vidéo. |
| ouv-RDC-004, largeur | 36 | 34 | 36 (plan gardé ; B dit lui-même que l'entrée arrière le cache d'environ 2 px). |
| Allèges | — | — | Écarts de ½ à 1½ po, dans l'incertitude (± 1½ po) : on prend la moyenne, arrondie au ½ po. |
| Têtes | 79 | 79 à 80 | 80 (règle 1). |

Les deux relevés s'accordent sur toutes les sections. Écart flagrant de position confirmé par les deux : ouv-SS-002
seulement, à **+13 po vers l'allée** (plan : axe à 6'-2" du nu droit, x 344½ à 419½ ; vidéo : x 359 à 431). Les autres
centres sont à 3 po ou moins du plan, et ne bougent pas (ouv-RDC-005 : 378 dans la vidéo, 375 au plan).

## Plans (P-129, P-130)
- `maison.json` : largeur (ESTIMÉ), position (ESTIMÉ, ouv-SS-002), allège et hauteur (ESTIMÉ), note datée sur chaque
  ouverture. L'hypothèse « salon à 20 po » (modifs.py) et l'allège de 40 po de zone_global sont remplacées pour les
  fenêtres de la vidéo ; la chambre 1 garde 40 po.
- Chaînes de cotes : façade avant du SS (≈ 29'-11" / ≈ 6'-0" / ≈ 2'-1" et ≈ 13'-5" / ≈ 5'-1") et mur de droite du SS
  (≈ 5'-10" / ≈ 7'-0" / ≈ 2'-6"), marquées ≈ (ESTIMÉ). Les sommes retombent sur les hors-tout.
- Notes : P-130 note 1 (« fenêtres selon la vidéo DAG, salon : allège ≈ 12 po ») et P-129 note 1.

## 3D : ce qui suit les fenêtres
- Sous-sol : `S["fenetres"]` (zone_global.py) prend les réglages de la vidéo pour ouv-SS-002, ouv-SS-003 et ouv-SS-004.
  Le store à enrouleur de ouv-SS-004 suit maintenant l'allège et la tête : il est à moitié remonté de 62 à 78½ po, et son
  tube est à 79 po.
- Rez-de-chaussée : `"fenetres"` (base_rdc01_scene.py) vient de `fenetres_video.reglages_3d("RDC")`, et les deux meneaux
  inégaux viennent de `meneaux_3d`. Les cadrages noirs, la brique d'embrasure et le store de la cuisine (évier et mur de
  droite) suivent l'allège et la tête, comme le store du salon. La toile solaire du bureau (rdc_bureau.py) et le store
  et son rail dans la chambre des parents (rdc_chambre_arriere.py) descendent de 2 po, sous la nouvelle tête. Sans ce
  changement, ils seraient restés dans le mur, au-dessus de la tête.

## Conflits à l'intérieur
Vérifiés objet par objet : tout le mobilier et les revêtements, de l'embrasure jusqu'à 30 po devant chaque fenêtre.
- **Cuisine, évier (ouv-RDC-005)** : l'allège remonte à 37½ po. La tablette de chêne de la fenêtre passe donc juste
  au-dessus du comptoir (36¼ po), et le pied du robinet l'aurait traversée. **Corrigé** : le robinet est avancé de 1 po
  (y 368,2 → 367,2, base_rdc01_scene.py).
- **Cuisine, mur de droite (ouv-RDC-007)** : allège à 24 po. Rien devant : le 2e frigo est déjà parti. La brique et le
  cadrage noir suivent la fenêtre.
- **Salon (ouv-RDC-002)** : allège à 12 po. Le sectionnel s'arrête à x 316 et la fenêtre commence à x 323. Le repose-pieds
  (dessus à 15½ po) est à 10 po du mur ; la sansevieria dans son panier est à 9 po du mur, devant la petite section.
  Aucun ne touche la fenêtre.
- **Chambre des parents (ouv-RDC-003)** : allège à 23½ po. Le lit king s'arrête à 31 po du mur, et le rideau est rangé
  côté lit. Pas de conflit.
- **Bureau (ouv-RDC-001)**, **salle à manger (ouv-RDC-004)**, **entrée arrière (ouv-RDC-008)** : ces fenêtres sont plus
  hautes ou plus étroites qu'avant. Le plan de travail (29½ po) reste sous l'allège de 37½ po.
- **Séjour (ouv-SS-002, déplacée vers x 359–431)** : le mur avant est libre. La galerie de photos (x 279½ à 336) n'est pas
  touchée, mais elle n'est plus centrée entre la trémie et la fenêtre (marges de 8½ et 23 po). À recentrer si le client
  le souhaite. La sansevieria sur le banc à jouets (coin x ≈ 432) frôle le bout droit de la fenêtre, plus haut que
  l'allège ; c'est du décor, pas un conflit.
- **Chambre 2 (ouv-SS-003, y 266 → 350)** : le bureau s'arrête à y 256¾. Le fauteuil du coin lecture (31 po de haut) est
  sous l'allège de 44 po, et la liseuse est à y 361. L'aire libre devant la fenêtre d'évacuation est gardée.

## Évacuation (chambres du sous-sol), à valider avec la Ville
- **ouv-SS-003 (chambre 2) : LIMITE.** Baie de 84 × 36 po en 3 sections égales d'environ 28 po. Un seul battant ouvrant
  laisse une ouverture libre d'environ 19 à 21 × 27 à 29 po, selon le cadre, soit **0,33 à 0,39 m²**. Le minimum est
  0,35 m², sans aucune dimension sous 380 mm (aucune n'y est). Avant, la baie faisait 80 × 46 po en 2 sections, soit
  environ 0,7 m² libres. Pour garder une marge, il faudrait un battant central plus large (≥ 30 po), un coulissant ou
  deux battants. La margelle de 36 po (914 mm) donne plus que les 760 mm de dégagement exigés.
- ouv-SS-009 et ouv-SS-010 (chambre 1) : inchangées par la vidéo. Rappel : à 40 po de large, une fenêtre en 2 battants
  égaux laisse environ 13 po (≈ 330 mm) de large, sous 380 mm. Il y faut un seul ouvrant (ou un coulissant).

## Limites connues (autres modules)
- `exterieur.py` (autre agent) dessine les fenêtres vues de dehors à partir de `maison.json`. Il y lit la largeur, la
  position et l'allège, qui suivent donc la vidéo. Mais il fixe lui-même la tête (82 po au RDC, 86 po au SS) et le nombre
  de meneaux (selon la largeur). Pour suivre la vidéo, il devrait lire la `hauteur` de `maison.json` (ou
  `fenetres_video.retenu(id)`) et les sections de `fenetres_video.FENETRES`. D'ici là, vues de dehors, les fenêtres du SS
  montrent une bande de mur de 80 à 86 po derrière la vitre, et les meneaux ne correspondent pas.
- Margelles : les allèges du SS (44 po) sont sous le terrain de la maquette (48 po). Le moteur pose donc des margelles,
  alors que dans la vidéo le terrain est plus bas : la pelouse est à environ z 16 devant, et l'allée est au niveau du
  plancher du SS sur le côté. C'est au terrain d'exterieur.py de suivre la vidéo.
- `rdc_cuisine.py` (en cours, autre agent) : la fenêtre de l'évier est à 37½ → 80 po (3 sections), celle du mur de droite
  à 24 → 80 po. La tablette de la fenêtre de l'évier est à 36¾–37½ po, au ras du comptoir de 36¼ po.

## Vérifications
(voir la fin du fichier)

## À valider sur place
Mesurer les vraies fenêtres (baie brute et cadre) : la vidéo est une maquette d'architecte paysagiste, et les mesures
qu'on en tire sont à ± 1½ po en hauteur, ± 2 po en largeur sur les captures de face, ± 3 à 4 po sur la 03.
1. **ouv-SS-002** : sa vraie position (axe à 6'-2" du nu droit au plan, ou bord aligné sur la fenêtre du salon comme dans
   la vidéo ?) et sa largeur (6'-3" au plan, ≈ 6'-0" dans la vidéo).
2. **ouv-SS-003** : largeur (6'-8" au plan, ≈ 7'-0" dans la vidéo), type d'ouvrant et ouverture libre (évacuation).
3. **ouv-RDC-008** : largeur (3'-6" au plan, 3'-0" dans la vidéo).
4. **Têtes** : la vidéo met toutes les fenêtres au soffite, à la tête des portes. Il faut mesurer la vraie tête (82 po
   estimé sur les photos) et les linteaux. Une tête à 80 po au lieu de 82 po change la hauteur des fenêtres de 2 po.
5. **Allèges abaissées** : salon (12 po, linteau 2-2×10 inchangé), chambre des parents (23½ po), cuisine, mur de droite
   (24 po). Il faut vérifier l'appui, la brique sous l'appui et les plinthes chauffantes. Au salon, l'allège tombe à
   12 po (305 mm), sous 450 mm. Si la chute dehors dépasse environ 1,8 m, le code peut exiger une protection : partie
   basse fixe, ouverture limitée ou garde-corps. Il peut aussi exiger un verre de sécurité. À valider avec la Ville.
6. **Sections inégales** de la façade (bureau 1/3 + 2/3, salon 3/4 + 1/4) : vérifier lesquelles ouvrent.
7. ouv-SS-010 : le client veut-il vraiment l'enlever, comme dans la vidéo ? C'est une fenêtre d'évacuation de la chambre 1.
