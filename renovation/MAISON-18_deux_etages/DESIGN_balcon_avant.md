# MAISON-18 — Balcon avant (existant) dans la visite

Demande du client (2026-11-02), mot pour mot : « Voici mon balcon avant, intègre-le à la visite. » Puis, à nos questions : il est
devant la façade (la porte d'entrée sort dessus) ; « 24 [pi] jusqu'à la rue et il termine juste un peu à côté de la porte (à
droite de la porte d'entrée quand tu regardes d'en avant) » ; le coin des enfants est devant, vers la rue ; « Il est comme
surélevé. Le filet noir sur le balcon c'est un filet katamaran pour lire. »

Correction du client sur la première version (2026-11-02), mot pour mot :
- sur son croquis : « ça ressemble plus à ça, le setup » (un grand rectangle « balcon », le « Filet » dans un coin du balcon, le
  « jeu » en dehors du rectangle, avec un coin coupé en biais) ;
- « Les marches sont à 6 pieds du mur de la maison » ;
- « Yé où ton four à pizza ?? » (nouvelles photos 17 à 20 : cuisine d'extérieur sous la pergola) ;
- photo 16 (hiver, de l'allée) : l'escalier part d'un petit palier près de la porte, parallèle à la façade ; jardinière de cèdre
  et boîte aux lettres entre l'escalier et le mur ; la fondation réelle est foncée, mais on garde le crépi blanc de la
  proposition DAG (confirmé par le client).

Correction du client sur la 2e version (2026-11-02), en rouge sur notre croquis du dessus, et mot pour mot : « le filet est plus
cette grosseur-là et les poutres en bois vont presque jusqu'à la maison, le patio doit avoir 20 de large finalement et les
poutres en bois font 16 à partir de gauche et arrêtent à 4 pieds de la maison, avec celui du milieu dans le milieu ». Lu ainsi
(même orientation que son croquis, la rue à gauche) :
- **balcon de 20'-0"** de la façade jusqu'au bord avant (et non 24'-0") ; la largeur le long de la façade ne change pas ;
- **pergola : poutres de 16'-0"** à partir du bord avant (« à partir de gauche »), qui **arrêtent à 4'-0" de la maison** ;
  trois rangées de poteaux : au bord avant, **au milieu** (« celui du milieu dans le milieu ») et à 4 pi de la maison ;
- **filet de la grosseur du rectangle rouge** : mesuré sur l'annotation avec la cote « 60 » du croquis (= 60 po), environ
  **9'-5" vers la maison sur 10'-0" le long de la façade**, toujours au coin avant côté allée.

Précision du client sur la 3e version (2026-11-02), mot pour mot : « pi le meuble avec le four à pizza fait toute la longueur des
poutres (20') », puis il se corrige : « je voulais dire quelle faisais 16 pied le meuble pas 20 pieds ». Lu ainsi (4e version) :
- **le meuble de cuisine fait 16'-0"**, toute la longueur des poutres de la pergola : du bord avant du balcon (y -240) jusqu'à la
  rangée de poteaux à 4 pi de la maison (y -48) ; les 20 pi, c'est la profondeur du balcon, pas le meuble ;
- la pergola (16 pi, à 4 pi de la maison), le toit de polycarbonate et le salon ne changent pas.

C'est un balcon qui **existe** : on le reproduit tel quel, on n'en fait pas un nouveau design. Sources : 20 photos du client
(`renovation/prive/balcon_avant/`, privées, jamais copiées dans le dépôt) et son croquis. Code : `balcon_avant.py` (appelé par
`scene_3d.py`) et l'avant de `exterieur.py` (relief creusé à l'escalier, asphalte élargi).

## Lecture du croquis du client

Le croquis est tourné d'un quart de tour par rapport à nos plans : **la maison est le côté droit du rectangle, la rue le côté
gauche ; le haut du croquis est le côté du voisin (écran d'intimité), le bas le côté de l'allée (escalier)**. C'est la seule
lecture qui colle aux photos 03, 06, 10 et 12 (de la terrasse vers le fleuve : filet devant à gauche contre le garde-corps
au-dessus de l'allée ; maisonnette « 86 » droit devant, au-delà du garde-corps avant ; pergola et écran à droite, du côté du
voisin). Donc :
- le balcon est **tout le rectangle** : de la façade jusqu'à 20 pi vers la rue (client, 3e version), sur toute sa largeur ;
- le filet est dans le coin avant côté allée, contre le garde-corps avant et le garde-corps de droite (le banc de planche entre
  les deux) ;
- le coin des enfants est **devant** le balcon, le long de la moitié côté voisin du bord avant, plus bas (paillis), fermé de
  clôtures ; son coin avant côté allée est coupé en biais, qui revient vers le bord avant du balcon à peu près vis-à-vis du filet.

Le croquis n'est pas à l'échelle : les tailles viennent des photos (tableau plus bas), sauf celles que le client a données. Sur
son premier croquis le filet paraissait plus grand que sur les photos ; on avait gardé la taille des photos (84 × 60 po). Le
client a confirmé en rouge que le filet est bien plus gros : ≈ 9'-5" × 10'-0" (3e version).

## Ce qu'on a compris des photos

- Le balcon couvre l'avant de la maison, de l'écran d'intimité du voisin de gauche (au-delà du coin de la maison) jusqu'à un peu
  à droite de la porte, sur 20 pi de profond (client). Il est sur poteaux et poutres teints foncés, à la hauteur du seuil : « surélevé »
  de 4 à 5 pi au-dessus du terrain, de 9 pi au-dessus de l'allée.
- Côté voisin, contre l'écran : la pergola de bois teint (poteaux 6 × 6, poutres, étriers et plaques en T noirs). Son poteau avant
  est au bord avant du balcon, là où commence le garde-corps au-dessus du coin des enfants (photos 03, 04, 06, 07, 10, 12) ; ses
  poutres de 16 pi vont presque jusqu'à la maison (client).
- **Cuisine d'extérieur** (photos 17 à 20), le long de l'écran sous la pergola : comptoir de béton gris lissé (microciment) aux
  bouts en cascade, façades à lattes horizontales de bois teint foncé, frigo à boissons à porte vitrée noire, bacs à condiments
  d'inox encastrés dans le dessus, four à pizza (dôme crème sur socle noir) au bout côté rue ; puis, côté maison, un comptoir plus
  bas avec le BBQ encastré (3 brûleurs, inox et noir) et la plaque de cuisson noire (4 boutons : 4 brûleurs), sa tablette
  dépassant le comptoir. Le bout du comptoir haut côté rue est au poteau avant de l'écran et le garde-corps avant bute dessus
  (photos 18, 19) ; le BBQ est collé au comptoir haut et la plaque au bout du comptoir bas (photos 18, 20) ; la tablette de la
  plaque arrive au poteau du fond (photo 20).
  Au-dessus : toit de tôle ondulée translucide (polycarbonate) sur chevrons, guirlandes d'ampoules qui pendent des poutres.
  Mobilier de détente (photo 17) : sofa 3 places gris pâle à cadre d'aluminium noir, table basse à dessus de bois, 2 fauteuils à
  cadre noir et coussins gris, 2 poufs blancs. Cette installation **remplace** le BBQ sur roues et la banquette en L des photos
  plus anciennes. Écran : planches horizontales teintes à jours, montants et lisse haute d'acier noir, jusque sous les poutres.
- Côté allée, devant : le filet catamaran tendu dans une ouverture du plancher, encadré de bandes teintes foncées, une planche
  (banc) le long du garde-corps droit, trois coussins noirs au bout côté voisin (photos 03 à 05, 10, 12).
- Le plancher : planches de pin naturel de 5½ po en panneaux de sens alternés, séparés par des bandes teintes foncées (rives,
  alignement des poteaux de la pergola, rangée du milieu, cadre du filet et bande vers la porte).
- Garde-corps : poteaux et main courante de bois naturel, barreaux noirs ; un panneau de verre teinté dans le garde-corps droit
  (photos 04, 10, 12).
- Devant le bord avant, entre le poteau avant de la pergola et la boîte d'écran au bout du garde-corps du filet : une
  plateforme une marche plus bas ; de là, trois marches (vers le voisin) et une glissade bleue (le long du biais) mènent au
  coin des enfants (photos 01, 02, 06, 07, 08). Le coin des enfants : paillis de cèdre, carré de sable au coin coupé dans le coin
  du balcon et du voisin, mur d'escalade sur la clôture du voisin, maisonnette « 86 » (affiche « Bureau », cadres noirs, toit en
  appentis) dos à la clôture côté rue ; clôtures à planches horizontales sur poteaux d'acier noir ; la rue juste derrière.
- L'escalier avant neuf (photos 13 à 16) **part du côté droit du balcon**, près de la porte, et descend vers l'allée,
  parallèle à la façade : 15 contremarches de bois neuf, contremarches fermées, main courante et barreaux noirs du côté de la
  rue seulement, lampes solaires sur les poteaux ; il arrive sur l'asphalte (dalle au pied). **Entre l'escalier et le mur**,
  devant la fenêtre du sous-sol : une jardinière de cèdre à planches horizontales en gradins qui suivent l'escalier, posée sur
  l'asphalte, la boîte aux lettres noire sur un court poteau sur son dernier gradin (photo 16).

## Relevé (pouces ; repère de exterieur.py : x vers la droite vu de la rue, y vers l'arrière, z depuis le sous-sol)

| Élément | Retenu | Source |
|---|---|---|
| Profondeur du balcon | **20'-0"** sur toute la largeur (y 0 à -240) | **client** (3e version ; 24'-0" avant) |
| Bout droit | x 232 (21 po à droite du cadre de la porte, x 177-211) | client (« un peu à droite de la porte ») ; photo 15 |
| Bout gauche (écran du voisin) | x -90 : 7'-6" à gauche du coin de la maison, de 8 po (près de la maison) à 2 pi (devant) en deçà de la ligne de lot | estimé (photos 04, 15) |
| Largeur totale | 26'-10" | déduit |
| Dessus du plancher | 103½ (1½ po sous le seuil 105) | estimé (photo 15b) |
| Pergola : longueur | **poutres de 16'-0"** du bord avant (y -240) jusqu'à **4'-0" de la maison** (y -48) ; **3 rangées de poteaux : au bord avant (y -237¼), au milieu (y -144), à 4 pi de la maison (y -50¾)**, soit 8'-0" + 8'-0" | **client** (3e version) |
| Pergola : largeur | 11'-10" : poteaux x 49 et dans l'écran (x -87) ; dessous des poutres à 7'-4" | estimé (photos 03, 07, 12, 18) |
| Toit de polycarbonate | de l'écran à x -26 (≈ 5'-4"), sur 4 chevrons, toute la longueur de la pergola (16 pi) | estimé (photos 17 à 20) |
| Cuisine d'extérieur | **meuble de 16'-0"** le long de l'écran, du bord avant (y -240) jusqu'aux poteaux à 4 pi de la maison (y -48) ; 28 po de profond (x -84 à -56, dessus jusqu'à -55), devant les poteaux de l'écran (x -90 à -84½) | **client** (16'-0", 4e version) |
| Cuisine : répartition | comptoir haut **10'-0"** à 36 po (y -240 à -120) : four à pizza (dôme de 26 po, centre à 2'-2" du bout côté rue), frigo à porte vitrée de 23 po (y -182 à -159), 8 bacs (6 au fond, 2 devant) au bout côté maison ; comptoir bas **6'-0"** à 26 po (y -120 à -48) : BBQ 28 po contre le comptoir haut, plaque 39 po (4 brûleurs) au bout, sa tablette de 15 po dépasse le bout de 1'-1" (jusqu'à y -35) | estimé (photos 17 à 20 : frigo, BBQ et plaque comme étalons) |
| Mobilier | entre la cuisine et le passage, sous la pergola : sofa 78 × 31 le long du garde-corps avant (y -236), table 44 × 24, fauteuils 28 × 29, poufs 18 × 19 ; mêmes places qu'avant ; devant les comptoirs : 2'-10½" jusqu'à la table, 1'-9" jusqu'au fauteuil côté cuisine, 1'-7" jusqu'au sofa (au bout du four, comme sur la photo 17) | estimé (photo 17) |
| Écran d'intimité | 7'-2" au-dessus du balcon (jusque sous les poutres), planches de 5½ po, jours de 1 po, sur les 20 pi | photos 19, 20 |
| Filet catamaran | **≈ 9'-5" vers la maison × 10'-0" le long de la façade** : ouverture 113 × 120 po (x 93½-213½, y -230 à -117), à 10 po du bord avant ; flèche ≈ 4 po | **client** (rectangle rouge, mesuré avec sa cote « 60 ») ; position : son croquis |
| Banc du filet | planche 2 × 12 le long du garde-corps droit, jusqu'au haut de l'escalier (y -121) | photos 04, 05 |
| Passage entre la pergola et le filet | 2'-11½" (des poteaux de la pergola au cadre du filet) ; ouverture du garde-corps avant vers la plateforme : 5'-0" (x 52 à 112) | déduit |
| Garde-corps | 36 po, barreaux ¾ po à 4 po c/c, main courante 2 × 6 à plat | photos ; hauteur réglementaire supposée |
| Verre teinté | garde-corps droit, juste devant l'escalier (y -168 à -120) | photos d'été 10 et 12 ; pas vu sur les photos d'automne |
| Coin des enfants | devant le balcon, il suit le nouveau bord avant : 16'-10" le long du bord avant (x -90 à 112), 10'-0" de profond (y -240 à -360) ; clôture côté rue 6'-4" ; biais de (-14, -360) à (112, -276), puis retour de 3 pi le long de la plateforme ; dans le lot : 10'-0" de la ligne avant du lot, clôture du voisin à x -90 (ligne de lot à x -114 / -121) | croquis du client (disposition) ; profondeur estimée sur les photos 06, 08 (carré de sable 4'-6", 2 pi de paillis, maisonnette 3'-4") |
| Paillis | 66 (37½ po sous le balcon, 2 à 2½ pi au-dessus du terrain) | estimé (3 marches, photo 02) |
| Clôtures du coin des enfants | dessus à 144 (6'-6" au-dessus du paillis), jusqu'au terrain | estimé (photos 01, 06, 07) |
| Plateforme basse | 4'-11" × 3'-0" (x 52-111, y -276 à -240), à 96 (une marche de 7½) | estimé (photos 01, 07) |
| Marches vers le coin des enfants | 3 marches de 7½ po, girons de 10 po, 2'-10" de large, vers le voisin | photos 01, 02 |
| Glissade | 4'-4" de long, du bord avant de la plateforme au paillis, le long du biais | photos 01, 02, 06 |
| Maisonnette « 86 » | 5'-0" × 3'-4", 5'-10" devant, 5'-0" derrière, dos à la clôture côté rue | estimé (photos 02, 07, 08) |
| Carré de sable | 4'-3" × 4'-6", coin coupé, bordure 2 × 8 | estimé (photos 06, 08) |
| Escalier avant | 4'-0" de large, **côté maison à 6'-0" du mur (y -120 à -72)**, 15 contremarches de 7,53 po, 14 girons de 11 po, 12'-10" à l'horizontale | **client** (6 pi) ; marches comptées et largeur sur les photos 13 à 16 |
| Pied de l'escalier | dalle de béton sur l'asphalte à ≈ -7 (x 386-412) | photos 13, 14, 16 |
| Jardinière de cèdre | entre l'escalier et le mur (y -68 à -1), x 234 à 444, 4 gradins (dessus à 84, 64, 46, 34 ; le dernier 10 po sous l'allège de la fenêtre du sous-sol) | estimé (photo 16) |
| Boîte aux lettres | noire, sur un court poteau, sur le dernier gradin de la jardinière | photo 16 |

## Ce qui a changé dans la maquette (4e version : meuble de cuisine de 16 pi)

- **`balcon_avant.py`** seulement (rien d'autre ne bouge : balcon, pergola, toit de polycarbonate, filet, salon, coin des enfants,
  escalier) :
  - **meuble de 16'-0"** : `CU_Y0`, `CU_Y1` (y -240 à -48, du bord avant aux poteaux à 4 pi de la maison) ; le meuble passe devant
    les poteaux de l'écran (son dos à x -84, les poteaux jusqu'à -84½) ; comptoir haut `CU_HAUT` de 10'-0" et comptoir bas
    `CU_BAS` de 6'-0" ; modules en constantes, partagés par la maquette, les obstacles et le croquis : `CU_FOUR`, `CU_FRIGO`,
    `CU_BACS`, `CU_BBQ`, `CU_PLAQUE`, `CU_TABLETTE` ;
  - **comptoir haut** : four à pizza au bout côté rue (à la même place qu'avant, y -214), façades à lattes en trois panneaux (grand
    panneau sous le four, bande étroite contre le frigo, panneau côté maison, photo 19), frigo un peu passé le milieu, bacs au bout
    côté maison ; les pelles et les bacs à fleurs de l'écran gardent leur place par rapport au four ;
  - **comptoir bas** : BBQ 3 brûleurs (28 po) collé au comptoir haut, plaque 4 brûleurs (39 po) collée au bout, sa tablette dépasse
    le bout du meuble (photo 20) ;
  - **garde-corps avant** (au-dessus du coin des enfants) : il part maintenant du bout en cascade du comptoir haut (x -55) au lieu
    de l'écran, poteau intermédiaire au milieu ; son obstacle est raccourci de même ;
  - **obstacles** : cuisine (y -240 à -48) et tablette (y -48 à -35) ; le toit de polycarbonate (y -241 à -47) couvre toujours
    toute la cuisine ;
  - **arrêt « Cuisine d'extérieur (four à pizza) »** déplacé côté maison (x 30, y -14, cap 222) : on voit tout le meuble, le four
    au fond.
- **Salon** : à la même place (photo 17). On n'a pas pu mettre 3'-0" devant les comptoirs partout : entre le dessus des comptoirs
  et les poteaux de la pergola, il reste 8'-5" ; le sofa (6'-6") avec 3'-0" devant le comptoir en demanderait 9'-6" et
  boucherait le passage vers la plateforme. Il y a 2'-10½" jusqu'à la table, mais 1'-9" jusqu'au fauteuil côté cuisine et 1'-7"
  jusqu'au sofa (au bout du four), comme avant.

## Ce qui a changé dans la maquette (3e version : 20 pi, pergola de 16 pi, gros filet)

(Historique pour la cuisine : sa longueur et sa position sont remplacées par la 4e version.)

- **`balcon_avant.py`** seulement (`exterieur.py` n'a pas changé : l'escalier reste à 6 pi du mur, y -120 à -72) :
  - **balcon de 20'-0"** : bord avant à y -240 (`YAV`) ; planches, bandes, rives, solives, 3 poutres (y -234, -156, -78) et
    18 poteaux refaits sur la nouvelle profondeur ; garde-corps droit de 10'-0" jusqu'à l'escalier, verre teinté sur ses 4 derniers
    pieds (toujours juste devant l'escalier) ; écran du voisin sur les 20 pi ;
  - **pergola** : poutres de 16'-0" du bord avant jusqu'à 4'-0" de la maison (y -240 à -48) ; poteaux au bord avant, **au
    milieu (y -144)** et à 4 pi de la maison (2 travées de 8'-0") ; largeur inchangée (11'-10") ; toit de polycarbonate
    au-dessus de la cuisine sur les 16 pi ; guirlandes sur les 3 poutres, le long de la rangée intérieure et en X dans la
    travée avant ; les 2 vraies lampes au milieu de chaque travée ;
  - **cuisine d'extérieur** déplacée sous la nouvelle pergola, le long de l'écran, à 9 po du bord avant comme avant (four à
    pizza côté rue ; BBQ et plaque côté maison ; la tablette arrête à 1 pi des poteaux du fond) ; **salon** (sofa, table,
    fauteuils, poufs) entre la cuisine et le passage, mêmes dégagements qu'avant par rapport au garde-corps avant ;
  - **filet ≈ 9'-5" × 10'-0"** (113 × 120 po) au coin avant côté allée, contre le garde-corps avant (10 po : rive et cadre) et le
    banc du garde-corps droit ; 3 coussins au milieu du bout côté voisin ; le banc arrête au haut de l'escalier ;
  - passages gardés : vers l'escalier, le filet et son cadre finissent vis-à-vis du côté rue du haut de l'escalier (y -117 et
    -111½ ; l'escalier y -120 à -72) : on y va de la porte par les 9'-3" de planches entre le filet et le mur ; vers la
    plateforme du coin des enfants, un passage de 2'-11½" entre les poteaux de la pergola et le cadre du filet, puis
    l'ouverture de 5'-0" du garde-corps avant (le bout du filet côté voisin arrive au-dessus de la plateforme) ;
  - **coin des enfants** : suit le nouveau bord avant (y -240 à -360), même forme (coin coupé en biais), même profondeur
    (10'-0") et même contenu (plateforme, 3 marches, glissade, carré de sable, mur d'escalade, maisonnette « 86 ») ; il reste dans
    le lot (10'-0" de la ligne avant, 2 à 2½ pi de la ligne du voisin) ; le terrain y est de 38 à 49, sous le paillis (66) ;
  - planchers, obstacles (sofa, table, fauteuils, poufs : mêmes constantes que le dessin) et **arrêts de visite** :
    « Balcon avant — vue sur le fleuve » (en sortant de la porte), « Filet catamaran » (derrière le filet), « Cuisine
    d'extérieur (four à pizza) » (sous la pergola, côté maison), « Coin des enfants » (sur la plateforme), « Escalier avant
    (de la rue) » (inchangé).

## Ce qui a changé dans la maquette (2e version)

(Historique : les profondeurs de 24 pi et le filet de 84 × 60 po ci-dessous sont remplacés par la 3e version.)

- **`balcon_avant.py`** (`appliquer_exterieur(EXT)`, appelé par `scene_3d.py` après la création de l'extérieur) :
  - balcon sur tout le rectangle (24 pi de profond partout) : planches, bandes, rives, solives, 3 poutres et 18 poteaux ;
  - pergola déplacée jusqu'au bord avant (poteau avant au garde-corps du coin des enfants), toit de polycarbonate ondulé
    translucide sur chevrons au-dessus de la cuisine, guirlandes d'ampoules (6 fils, petites ampoules chaudes ; deux vraies lampes
    seulement, `lumieres` : le moteur n'a qu'un bassin de 4 lampes) ;
  - **nouveau** : cuisine d'extérieur (comptoirs, four à pizza, frigo, bacs, BBQ encastré, plaque de cuisson, pelles et bacs à
    fleurs sur l'écran) et mobilier de détente ; le BBQ sur roues et la banquette en L sont retirés ;
  - écran du voisin sur toute la profondeur, 7'-2", jours de 1 po, lisse haute d'acier noir ;
  - filet 84 × 60 au coin avant côté allée ; garde-corps avant en deux parties (au-dessus du coin des enfants ; devant le filet),
    ouverture vers la plateforme entre les deux ;
  - coin des enfants **devant** le balcon, contour en biais (clôture oblique dessinée en prismes), plateforme, marches,
    glissade parallèle au biais, carré de sable, mur d'escalade, maisonnette ;
  - escalier à 6'-0" du mur ; jardinière de cèdre en gradins et boîte aux lettres posée dessus (l'ancien poteau de boîte aux
    lettres dans le gazon est retiré) ;
  - le feuillu des photos est replacé entre la clôture côté rue du coin des enfants et la rue (x 30, y -446) ;
  - planchers : balcon (103½, en 4 morceaux autour du filet), filet (100½), plateforme (96), 3 marches, paillis (66), 14 girons
    de l'escalier, dalle du pied ; obstacles : garde-corps, écran, 4 clôtures du coin des enfants, poteaux de la pergola,
    cuisine, sofa, table, fauteuils, poufs, maisonnette, carré de sable, glissade, main courante, jardinière ;
  - couleurs : 26 peintures « bal-… » (nouvelles : microciment, lattes, crème du four, coussins gris pâle, poufs, bois de table,
    cèdre et terre de la jardinière) et 11 lignes dans la légende « Extérieur » ;
  - arrêts de visite : « Balcon avant — vue sur le fleuve », « Filet catamaran », « Cuisine d'extérieur (four à pizza) »
    (nouveau), « Coin des enfants » (sur la plateforme), « Escalier avant (de la rue) » (de l'allée, comme la photo 16).
- Déplacements : on sort par la porte directement sur le balcon (1½ po plus bas) ; on longe le garde-corps droit jusqu'à
  l'escalier et l'asphalte ; on va au coin des enfants par le passage entre la pergola et le filet, la plateforme (7½ po), les
  3 marches et le paillis (7½ po chacune). Toutes les marches font 8 po ou moins.
- **Filet catamaran** : on peut marcher et s'étendre dessus (plancher 3 po sous le balcon, la flèche moyenne) ; la maille est
  dessinée en cordes noires aux 2½ po avec une flèche de 4 po : on voit le sol à travers.
- **`exterieur.py`, avant seulement** : `ESC_AV` passe à y -120 à -72 (6'-0" du mur) ; `AIRE_AV` (asphalte élargi) monte
  jusqu'au mur (y -2) : la jardinière est posée sur l'asphalte et l'asphalte longe son bout côté allée (photo 16). Le relief est
  toujours **creusé** (jamais remonté) par `_creux_avant`, qui suit ces deux constantes. Rien n'est touché derrière la maison.
- **Fondation** : sur les photos elle est peinte foncée ; on garde la proposition DAG (crépi blanc), confirmé par le client.

## Questions pour le client (mesures à prendre)

1. **Coin des enfants** : sa profondeur, du bord avant du balcon jusqu'à la clôture côté rue (on a mis 10'-0"), la longueur de
   la clôture côté rue (6'-4") et le point où le biais rejoint le balcon (on l'a fait arriver à la boîte d'écran, au bout du
   garde-corps du filet, par un petit retour de 3 pi le long de la plateforme). Le biais touche-t-il directement le balcon ?
2. **Pergola** : la longueur (16 pi) et les poteaux du milieu sont à toi ; reste la largeur de l'écran à la rangée intérieure
   (on a mis 11'-7" entre les poteaux, 11'-10" hors tout) et jusqu'où va le toit de polycarbonate vers l'allée (≈ 5'-4" à
   partir de l'écran).
3. **Filet catamaran** : on l'a mesuré sur ton rectangle rouge (≈ 9'-5" vers la maison × 10'-0" le long de la façade). Ça le
   fait finir vis-à-vis du haut de l'escalier et laisse 2'-11½" de passage entre la pergola et le filet vers la plateforme :
   est-ce bien ça ? Les mesures exactes de l'ouverture ?
4. **Cuisine d'extérieur** : le meuble fait 16'-0" (toi), du bord avant aux poteaux à 4 pi de la maison. Reste la répartition :
   le comptoir haut et le comptoir bas (on a mis 10'-0" et 6'-0") et leur hauteur (36 et 26 po) ; sur les photos 17 et 18, le
   comptoir haut semble finir vis-à-vis du poteau du milieu : est-ce le cas ? Les 16 pi, est-ce le béton seul (on l'a fait
   ainsi) ou avec la tablette de la plaque (on la fait dépasser de 1'-1" au bout) ?
5. **Escalier avant** : la largeur entre les deux poteaux du haut (on a mis 4'-0") ; le panneau de verre teinté est-il encore
   dans le garde-corps (on l'a mis juste devant l'escalier) ?
6. **Largeur du balcon** : de l'écran du voisin jusqu'au bout droit du balcon (on a mis 26'-10").
7. **Jardinière** : jusqu'où elle va vers l'allée (on l'a arrêtée à 1 pi du coin de la maison) et la hauteur de ses gradins.
