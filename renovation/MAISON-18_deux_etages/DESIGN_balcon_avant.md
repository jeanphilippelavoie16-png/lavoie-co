# MAISON-18 — Balcon avant (existant) dans la visite

Demande du client (2026-11-02), mot pour mot : « Voici mon balcon avant, intègre-le à la visite. » Puis, à nos questions : il est
devant la façade (la porte d'entrée sort dessus) ; « 24 [pi] jusqu'à la rue et il termine juste un peu à côté de la porte (à
droite de la porte d'entrée quand tu regardes d'en avant) » ; le coin des enfants est devant, vers la rue ; « Il est comme
surélevé. Le filet noir sur le balcon c'est un filet katamaran pour lire. »

C'est un balcon qui **existe** : on le reproduit tel quel, on n'en fait pas un nouveau design. Sources : 15 photos du client
(`renovation/prive/balcon_avant/`, privées, jamais copiées dans le dépôt) : 10 photos d'été du balcon et du coin des enfants,
3 photos d'automne de l'escalier avant neuf et de la façade. Code : `balcon_avant.py` (appelé par `scene_3d.py`) et l'avant de
`exterieur.py` (relief creusé à l'escalier).

## Ce qu'on a compris des photos

- Le balcon couvre l'avant de la maison, de l'écran d'intimité du voisin de gauche (au-delà du coin de la maison) jusqu'à un peu
  à droite de la porte. Il est sur poteaux et poutres teints foncés, à la hauteur du seuil : « surélevé » de 4 à 5 pi au-dessus
  du terrain, de 9 pi au-dessus de l'allée.
- Côté gauche, contre l'écran du voisin : la pergola de bois teint (poteaux 6 × 6 et poutres, étriers et plaques en T noirs),
  dessous le BBQ et la banquette en L à coussins gris foncé.
- Côté droit, devant : le filet catamaran tendu dans une ouverture du plancher, encadré de bandes teintes foncées, une planche
  (banc) le long du garde-corps droit, trois coussins noirs au bout (photos 03 à 05).
- Le plancher : planches de pin naturel de 5½ po en panneaux de sens alternés, séparés par des bandes teintes foncées (autour
  du filet, sous l'alignement des poteaux de la pergola, de part et d'autre de la porte).
- Garde-corps : poteaux et main courante de bois naturel, barreaux noirs ; un panneau de verre teinté dans le garde-corps droit
  (photos 04, 10, 12).
- Devant à gauche, plus bas : une plateforme (une marche), trois marches et une glissade bleue mènent au coin des enfants,
  fermé par des clôtures à planches horizontales sur poteaux d'acier noir : paillis de cèdre, carré de sable au coin coupé, mur
  d'escalade sur la clôture gauche, maisonnette « 86 » (affiche « Bureau », cadres noirs, toit en appentis) dans le coin avant.
- L'escalier avant neuf (photos 13 à 15) **part du côté droit du balcon** et descend vers l'allée, parallèle à la façade : une
  quinzaine de marches de bois neuf, contremarches fermées, main courante et barreaux noirs du côté de la rue seulement, lampes
  solaires sur les poteaux ; il arrive sur l'asphalte (dalle de béton au pied). Boîte aux lettres noire sur poteau à droite du
  pied. L'ancien escalier de béton est dessous.

## Relevé estimé (pouces ; repère de exterieur.py : x vers la droite vu de la rue, y vers l'arrière, z depuis le sous-sol)

| Élément | Retenu | Comment |
|---|---|---|
| Profondeur du balcon | 24'-0" (y 0 à -288) | **client** |
| Bout droit | x 232 (21 po à droite du cadre de la porte, x 177-211) | client (« un peu à droite de la porte ») ; photo 15 |
| Bout gauche (écran du voisin) | x -90 : 7'-6" à gauche du coin de la maison, ≈ 8 po en deçà de la ligne de lot | supposé (photos 04, 15 : le balcon dépasse le coin de la maison jusqu'à l'écran) |
| Largeur totale | 26'-10" | déduit |
| Dessus du plancher | 103½ (1½ po sous le seuil 105) | photo 15b (le plancher arrive au seuil) ; supposé |
| Grand plancher | 26'-10" × 15'-0" (y 0 à -180) | supposé : bord du coin des enfants à 15 pi (photos 06, 07) |
| Partie avant droite (filet) | 10'-0" × 9'-0" (x 112 à 232, y -180 à -288) | supposé, photos 04, 05, 10 |
| Ouverture du filet | 83 × 54 po (x 130-213, y -278 à -224), flèche ≈ 4 po | compté : ≈ 15 planches le long, 3 coussins au bout ; supposé |
| Banc du filet | planche 2 × 12 le long du garde-corps droit | photos 04, 05 |
| Pergola | 11'-4" × 12'-3" : poteaux x 49 (y -177, -104, -31) et dans l'écran (x -87), poutres 5½ × 7½ à 7'-4" | photos 03-05, 09-12 (3 poteaux en ligne, poutres vers l'écran) ; dimensions supposées |
| Écran d'intimité | 6 pi au-dessus du balcon, planches de 5½ po, jours de ¾ po, montants d'acier noir | photos 04, 09 |
| BBQ | contre l'écran, y -160 à -110 | photos d'été (sur les photos d'automne il est près de la porte) |
| Banquette en L | 7'-6" le long de l'écran + 8'-0" le long de la maison, assise à 15 po | photos 04, 09 ; supposé |
| Garde-corps | 36 po, barreaux ¾ po à 4 po c/c, main courante 2 × 6 à plat | photos ; hauteur réglementaire supposée |
| Verre teinté | garde-corps droit, y -192 à -144 (juste devant l'escalier) | photos d'été 10 et 12 ; **pas vu sur les photos d'automne** |
| Plateforme basse | 5'-0" × 9'-0" (x 52-112), à 96 (une marche de 7½) | photos 01, 02, 07 ; supposé |
| Marches vers le coin des enfants | 3 marches de 7½ po, girons de 10 po, 6'-10" de large | photo 02 (3 marches) |
| Coin des enfants | 11'-10" × 9'-0" (x -90 à 52, y -288 à -180), paillis à 66 (37½ po sous le balcon) | photos 01, 02, 06-08 ; supposé |
| Clôtures du coin des enfants | 6'-6" au-dessus du paillis (dessus à 144), jusqu'au terrain | photos 01, 06 ; supposé |
| Maisonnette « 86 » | 5'-0" × 3'-4", 5'-4" devant, 4'-6" derrière (appentis vers la rue) | photos 02, 07, 08 ; supposé |
| Carré de sable | 4'-3" × 4'-6", coin coupé, bordure 2 × 8 | photos 06, 08 ; supposé |
| Glissade | 4'-4" de long, de la plateforme (96) au paillis | photos 01, 02 |
| Escalier avant | 4'-0" de large (y -144 à -96, à 8 pi de la façade), 15 contremarches de 7,55 po, 14 girons de 11 po, 12'-10" à l'horizontale | photos 13-15 : marches comptées, largeur mesurée sur une contremarche ; position estimée entre la photo 15 (≈ 6 à 10 pi) et les photos 13-14 (≈ 10 à 14 pi) |
| Pied de l'escalier | dalle de béton sur l'asphalte à ≈ -10 (x 386-412) | photos 13, 14 |

## Ce qui a changé dans la maquette

- **Nouveau `balcon_avant.py`** (`appliquer_exterieur(EXT)`, appelé par `scene_3d.py` après la création de l'extérieur) :
  - retire le perron de béton du relevé : ses objets (dalle, 4 marches, garde-corps noirs), les planchers « Perron avant » et
    « Marches du perron », les obstacles « Garde-corps du perron » et le trou du perron plein. L'excroissance de fondation du
    sous-sol (chambre froide sous l'ancien perron) reste, coiffée de sa dalle, cachée sous le balcon ;
  - ajoute le balcon (planches, bandes, rives, solives, poutres et poteaux teints foncés), les garde-corps, l'écran, la
    pergola, le BBQ, la banquette, le filet, la plateforme, les marches, le coin des enfants et l'escalier avant ;
  - planchers où l'on marche : balcon (103½), filet (100½), plateforme (96), 3 marches, paillis (66), 14 girons de l'escalier,
    dalle du pied ; on sort par la porte d'entrée directement sur le balcon (1½ po plus bas), on descend l'escalier jusqu'à
    l'asphalte, on va au coin des enfants par la plateforme et les marches (toutes les marches font 8 po ou moins) ;
  - obstacles : garde-corps, écran, clôtures, poteaux de la pergola, BBQ, banquette, maisonnette, carré de sable, glissade,
    main courante de l'escalier, boîte aux lettres ;
  - le petit arbre ornemental de `exterieur.py` (x -60, y -250) tombait dans le coin des enfants : il est remplacé par le
    feuillu des photos, entre la clôture du coin des enfants et la rue (x -45, y -360), ses branches au-dessus du coin ;
  - couleurs : 18 peintures « bal-… » et 8 lignes dans la légende « Extérieur » ;
  - arrêts de visite (section Extérieur) : « Balcon avant — vue sur le fleuve », « Filet catamaran », « Coin des enfants »,
    « Escalier avant (de la rue) ».
- **Filet catamaran** : on peut marcher et s'étendre dessus. C'est un plancher à 3 po sous le balcon (la flèche moyenne), qu'on
  descend seul ; la maille est dessinée en cordes noires aux 2½ po avec une flèche de 4 po : on voit le sol à travers. C'est ce
  qui est le plus crédible dans le moteur (un filet catamaran se marche ; le moteur n'a pas de surface molle).
- **`exterieur.py`, avant seulement** : le relief de la vidéo DAG est **creusé** (jamais remonté) par `_creux_avant` : sous
  l'escalier, le terrain reste à 7 à 11 po sous les girons (talus raide comme sur les photos) ; l'asphalte de l'allée s'élargit
  devant la partie droite de la façade (x 380 à 456, de la rue jusqu'à 6'-8" de la façade) pour que l'escalier arrive sur
  l'asphalte ; talus de 32° autour. Nouvelles constantes `Z_BALCON`, `ESC_AV`, `ESC_AV_N`, `AIRE_AV`, `CREUX_PENTE`,
  `LIGNES_AVANT` ; `_sol_avant` devient le minimum de l'ancien relief (`_sol_avant_dag`, inchangé) et du creux ; 5 lignes de
  grille de plus devant (`_relief`) ; revêtement « Asphalte devant l'escalier avant ». Le palier bas de la vidéo DAG reste près
  de la maison (la fenêtre du sous-sol n'a pas de margelle). Rien n'est touché derrière la maison.
- **Fondation** : sur les photos elle est peinte foncée ; on garde la proposition DAG (crépi blanc). Les fenêtres et la porte
  restent celles de notre proposition.

## Questions pour le client (mesures à prendre)

1. **Escalier avant** : du mur de la maison (sous la porte) jusqu'au poteau de l'escalier le plus proche de la maison, et la
   largeur entre les deux poteaux du haut de l'escalier. (On a mis 8'-0" et 4'-0".) Le panneau de verre teinté est-il encore
   dans le garde-corps (on l'a mis juste devant l'escalier, comme sur les photos d'été) ?
2. **Largeur du balcon** : de l'écran du voisin (gauche) jusqu'au bout droit du balcon, et du bout droit au cadre de la porte.
   (On a mis 26'-10" et 21 po.)
3. **Coin des enfants** : du mur de la maison jusqu'au garde-corps qui le borde (on a mis 15'-0"), et sa largeur de l'écran du
   voisin jusqu'à la plateforme (on a mis 11'-10").
4. **Filet catamaran** : longueur et largeur de l'ouverture (on a mis 83 × 54 po).
5. **Hauteurs** : combien de marches à l'escalier avant (on en a compté 15 contremarches), et la marche entre le plancher du
   balcon et le seuil de la porte (on a mis 1½ po).
