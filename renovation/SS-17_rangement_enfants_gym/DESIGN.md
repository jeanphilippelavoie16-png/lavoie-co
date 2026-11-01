# SS-17 — Rangement des chambres d'enfants, banc-cabane sous l'escalier, gym refait, sous-sol optimisé

Construit par-dessus SS-16 (bain sur travertin, béton poli, toile interactive, galerie de photos de famille, caveau isolé), qui reste intact. Feuilles **P-127** (sous-sol) et **P-128** (rez-de-chaussée, inchangé). Chaque zone est un module (`zone_*.py`) ajouté à une copie figée de SS-16 (`base_ss16_scene.py`, `base_ss16_modifs.py`).

## Demandes du client (2026-11-01)
- « Du rangement spécial dans les chambres des enfants, du rangement que tu disais : wow, c'est bien pensé ça. » Les enfants ont 4 et 6 ans.
- « Je veux un lit queen en chambre d'enfant minimum, pour que ça dure. »
- « En dessous des marches, je pense à quelque chose ; je veux pas que ça bloque toute la vue. »
- « Le gym aussi, retravailler comment les choses sont placées, l'optimiser ; puis tout optimiser. »

## Sommaire
| Zone | Idée | Ordre de grandeur |
|---|---|---|
| Chambre 1 (4 ans) | « Le socle de chêne » : lit queen-cabane, banquette des fenêtres à tiroirs-images, gare à jouets, garde-robe intégrée de 11 pi | 15 000 à 37 000 $ |
| Chambre 2 (6 ans) + walk-in | « La bibliothèque secrète » : mur de tête intégré, porte-bibliothèque pivotante vers le walk-in, lit queen sur tiroirs, banc-cabane, mur d'activité | 24 000 à 42 000 $ |
| Dessous de l'escalier | « Le banc-cabane cinéma » : banc bas et ajouré (≤ 26 po), 10 bacs, coin-cabane et sa lune | 6 350 à 10 100 $ |
| Gym | Cardio contre le mur avant, zone au sol 6 × 6 pi, mur-miroir de 12 pi, banc-coffre à poids verrouillé | 7 200 à 14 000 $ (porte coulissante comprise) |
| Reste du sous-sol | Casiers d'hiver, seuil à neige, insonorisation, trajet de nuit, banc à jouets sous la toile, VRC, salle de bain à hauteur d'enfant | 16 000 à 30 000 $ |

Coûts : estimations à confirmer par des soumissions. Tout est une esquisse à valider avec la Ville de Baie-Comeau et un professionnel.

## Chambre 1 — le petit de 4 ans

### Chambre 1 (l'enfant de 4 ans) — « Le socle de chêne »

**L'idée.** Un seul socle de chêne fait le tour de la chambre. Il commence par un **lit queen-cabane** dans le coin
ouest-arrière, devient une **banquette** sous les deux fenêtres (6 tiroirs-images ; c'est aussi la marche pour sortir par
la fenêtre), puis une **gare à jouets** le long du mur de la chambre 2. **Règle des 4 pieds** : tout ce qui est à l'enfant
est sous 48 po et s'ouvre sans danger ; ce qui est aux parents est au-dessus, derrière des loquets. On ne refait rien à
l'adolescence : on monte une tringle, on enlève un module, on pose un bureau sur les mêmes crémaillères.

#### Ce qui change par rapport à SS-16, et pourquoi

| SS-16 | SS-17 | Pourquoi |
|---|---|---|
| Lit queen tête au mur arrière, entre les deux fenêtres | Lit-plateforme queen dans le coin : tête au mur ouest, long côté au mur arrière | Les deux fenêtres restent libres : la banquette sous elles sert de marche d'évacuation, au lieu de passer par-dessus le lit |
| Garde-robe de 28 × 90 po (cloisons P12 et P13, portes coulissantes P07) le long du mur ouest | Garde-robe intégrée de 134¼ × 24 po sur le mur de la salle de bain (P05) | Plus de rangement sur un mur aveugle ; le mur ouest reçoit le lit ; la garde-robe sert aussi de tampon acoustique avec la salle de bain |
| Commode de 60 po sur le mur est, bureau et chaise près de l'ancienne garde-robe | Gare à jouets basse (bacs) et mur à crémaillères sur le mur est ; le bureau viendra « plus tard » | À 4 ans, il faut des bacs à sa hauteur et un comptoir de jeu debout, pas un bureau |
| Recoin d'entrée vide | Station du matin (banc à pantoufles, crochets, miroir, routine en pictogrammes) | Habillage autonome dès la porte |

Superficie : environ **199 pi²** avec l'ancienne garde-robe et le recoin (179,7 + 15,8 pi², plus les cloisons enlevées).
Le centre reste un grand coin jeu au sol, d'environ 127 × 76 po, avec un tapis lavable de 5 × 8 pi.

#### Ce qui est construit (pouces, repère de la maison)

- **C1-LIT, lit-plateforme queen « cabane »** : x 11–93, y 302–364. Dessus du caisson à 12 po, matelas 60 × 80 × 10 po, **dessus du matelas à 22 po**
  (aucun couchage en hauteur). Le socle est en retrait de 3 po, avec une DEL de plinthe à détecteur (2200 K) qui éclaire le chemin jusqu'à la porte.
  Dessous : **3 bacs-wagons** de 23 × 56 po sur roulettes, sans rail (rien ne pince), avec une poignée découpée et une étiquette-image.
  Côté accessible (sud) : **25¾ po** jusqu'aux façades de la garde-robe.
- **C1-DOSSERET** : caisson de 6 po le long du mur arrière avec 3 niches éclairées (DEL tactile à portée de l'enfant), une prise TR + USB-C cachée
  sous un couvercle, et une tablette à 34 po. Le jour, il fait du lit un « divan ».
- **C1-TETE** : lattes de chêne de 1½ po sur le mur ouest (z 12–46) ; 2 liseuses murales à bras court, avec les cordons dans le mur.
- **C1-CANOPEE** : armoires hautes de 81½ × 14 × 24 po au-dessus du lit, avec 3 portes à loquet positif (pas de « pousser-ouvrir » au-dessus d'un lit).
  Le dessous est à **72 po**, ce qui laisse 50 po libres au-dessus du matelas. Un ruban DEL chaud dessous sert de veilleuse de la cabane.
- **C1-RIDEAU** : rail en L encastré au plafond (y = 300, puis x = 94) et rideau de lin couleur sable, sans cordon ni boucle.
  Ouvert, le pan du long côté se range contre le mur ouest et celui du pied contre la banquette : le coin du pied reste libre.
- **C1-BANC, banquette des fenêtres** : x 93–237¾, y 352–370, dessus à 16 po, plus un coussin de 2 po. **6 tiroirs-images** à fermeture douce,
  façades en laque argile. Elle sert de **marche fixe** sous les fenêtres d'évacuation ; rien de fixe sur l'assise devant les fenêtres.
- **C1-BIB1 et C1-BIB2** : 2 bibliothèques de 24 × 12 po ancrées, posées sur la banquette.
  - **BIB1**, entre les fenêtres : rebords « livres face avant » à 22, 32 et 42 po.
  - **BIB2**, au coin : 2 bacs d'osier en bas.
  - Les deux : tablettes réglables au-dessus de 48 po (pour les parents).
- **C1-VALANCE** : bandeau de chêne de 10 po (z 86–96) qui cache 2 stores occultants **sans cordon**. La fenêtre s'ouvre en entier.
- **C1-GARE, gare à jouets** : x 219¾–237¾, y 268–352. 3 modules de 28 × 18 × 24 po, avec 12 bacs en laque argile et étiquettes-images.
  Les modules sont posés sur un socle vissé et ancrés au mur. Le dessus de chêne arrondi, à 24 po, est un comptoir de jeu debout.
  - **C1-MUR** : 4 crémaillères noires de 30 à 84 po, un panneau perforé de chêne de 72 × 36 po et un câble à dessins avec pinces.
  - **C1-BUREAU (plus tard, pas dessiné en 3D)** : plateau de 48 × 24 po à 29 po sur les crémaillères, à la place du module central.
    Il peut aussi servir de table à bricolage à 21–22 po dès 5 ans.
- **Garde-robe intégrée (mur P05)** : x 10–144¼, y 252¼–276¼, du plancher au plafond. Poignées encastrées : rien ne dépasse dans le passage.
  - **C1-GR-A, penderie** (2 portes de 21 po) : tringle d'enfant à 36 po et tringle haute à 72 po. À l'adolescence : une tringle à 66 po et une tablette à 70 po.
  - **C1-GR-B, tour de tiroirs-images** : 4 tiroirs de 4 à 40 po, avec une butée qui ne laisse ouvrir qu'un tiroir à la fois, et 2 portes à loquet au-dessus.
  - **C1-GR-C, niche-cachette** : 46 × 22 × 40 po, avec un coussin, un petit rideau sur tringle à ressort et une veilleuse à pile.
  - **C1-PLINTHE** : 3 tiroirs plats dans le coup-de-pied.
- **C1-VESTIAIRE, station du matin** (recoin, x 144¼–196, y 232¼–246¼) :
  - banc de 12 po à 3 cases à pantoufles ;
  - crochets champignons à 36 po (enfant) et à 60 po (plus tard) ;
  - miroir incassable de 24 à 48 po ;
  - tableau magnétique « routine du matin » ;
  - tablette à 66 po avec paniers.

  La station s'arrête 5 po avant l'arc de la porte.
- **C1-TAPIS** : tapis de laine lavable de 5 × 8 pi sur une thibaude antidérapante (x 108–204, y 286–346).

#### Plan (P-127) et maquette 3D

- **Plan** :
  - enlevés : les murs mur-SS-P12 et mur-SS-P13, les portes ouv-SS-P07, la pièce piece-SS-GR1 (fusionnée à la chambre 1) et la commode elem-SS-P-COMMODE1 ;
  - ajoutés : le lit (« LIT QUEEN »), la canopée (pointillé), la banquette, les 2 bibliothèques, la gare (« BACS »), la garde-robe (« G.-R. ») et la station du matin ;
  - une note sur ouv-SS-009 et ouv-SS-010 : ce sont les fenêtres d'évacuation, elles doivent ouvrir.
- **3D** :
  - retiré tout le mobilier de SS-16 dans la chambre : lit, chevets, lampes, tapis, porte de garde-robe, bureau, chaise, écran, commode et ses objets, miroir rond ;
  - ajouté tout ce qui précède ;
  - 3 encastrés : coin jeu, passage lit et garde-robe, recoin ;
  - 6 arrêts de visite, « Chambre 1 — … » : le socle de chêne, le lit-cabane, la banquette des fenêtres, la gare à jouets,
    la garde-robe et la cachette, la station du matin.
- **Matériaux** :
  - placage de chêne ;
  - laque argile (alias art-argile, la même teinte que le mur arrière) sur tout ce que l'enfant ouvre ;
  - rideau et coussins sable et tissu ;
  - pas de vert.
- Tout reste à l'ouest de x = 237¾ (nu de P07). La chambre 2 met ses meubles dos à dos de l'autre côté.

#### Écarts avec la spec (corrections d'incohérences)

1. **Banquette** : les 6 tiroirs occupent x 93–219¾ (21⅛ po chacun) et le coin x 219¾–237¾ reste fixe. Un 6ᵉ tiroir à cet endroit heurterait la gare à jouets en s'ouvrant.
2. **Niches du dosseret** : 16 × 9 po (z 23½–32½) au lieu de 16 × 12. Elles restent ainsi au-dessus du matelas (22 po) et sous la tablette (34 po).
3. **Gare** : **12 bacs** (4 par module, en 2 × 2), comme sur l'élévation E3. Le texte de la spec disait 6.
4. **Canopée** : elle s'arrête à x = 92, où commence la fenêtre ouv-SS-010. Elle fait donc 81½ po au lieu de 83.
5. **Bibliothèques** : à 24 po de large, elles touchent les tablettes de fenêtre (1½ po de chaque côté).
   À la pose, il faut couper les tablettes de fenêtre, ou réduire les bibliothèques à 21 po.

#### Options pour le client

- **A, économique (15 000 – 22 000 $)** : caissons standards (type PAX ou BESTÅ) avec façades de chêne sur mesure.
  Lit-plateforme fabriqué en atelier et banquette en caissons de cuisine de 15 po.
- **B, proposé (25 000 – 37 000 $)** : tout sur mesure en placage de chêne.
- Façades de l'enfant : laque argile (proposé), sauge, ou chêne naturel partout.
- Rideau-cabane : oui (proposé) ou non (canopée seule).
- Niche-cachette dès maintenant (proposé) ou tour de tiroirs tout de suite.
- Table à bricolage basse (21 po) sur les crémaillères dès 5 ans, ou bureau à 29 po seulement plus tard.
- Stores sans cordon : à ressort (proposé) ou motorisés à pile.

#### Coût (ordre de grandeur, ébénisterie résidentielle au Québec 2025-2026, à confirmer par soumissions)

| Poste | Fourchette |
|---|---|
| Lit-plateforme + 3 bacs-wagons + dosseret-niches + tête en lattes | 5 000 – 7 500 $ |
| Canopée + rail et rideau | 2 300 – 3 500 $ |
| Banquette (6 tiroirs) + 2 bibliothèques + valance + 2 stores sans cordon | 6 500 – 9 500 $ |
| Garde-robe intégrée 134 po (3 modules + plinthe) | 7 000 – 10 500 $ |
| Gare à jouets + crémaillères + panneau perforé | 1 800 – 2 800 $ |
| Station du matin | 1 000 – 1 600 $ |
| Électricité (DEL des niches et de la plinthe, liseuses, prises TR et USB-C) | 1 400 – 2 200 $ |
| Crédit : garde-robe SS-16 non construite (2 cloisons, portes coulissantes) | − 1 500 à − 2 500 $ |
| **Total sur mesure (matelas exclu)** | **25 000 – 37 000 $** |
| Plus tard : bureau sur crémaillères ; tringle relevée et tour de tiroirs dans la niche | 400 – 900 $ ; 300 – 600 $ |

#### Frontières communes

- **mur-SS-P05 (salle de bain)** : la garde-robe s'y ancre sur toute la longueur. De l'autre côté se trouvent le mur d'accent fourré et la niche du bain
  (x ≈ 71–119, z 33½–48½) : vis de 2 po au plus dans les montants, aucun percement traversant. Il faut isoler la cloison (laine de roche).
- **mur-SS-P07 (chambre 2)** : la gare, les crémaillères et le coin de la banquette sont ancrés côté chambre 1. La cloison est à isoler acoustiquement.
  Aucune ouverture ne change. À coordonner avec la chambre 2, qui met des meubles dos à dos de l'autre côté.
- **mur-SS-P04 et mur-SS-P06** : la station du matin est ancrée côté recoin. La porte coulissante de la salle de bain (ouv-SS-P03) n'est pas touchée,
  pas plus que la porte de la chambre (ouv-SS-P05 : 30 po, pentures côté est, ouvre vers la chambre).
  Ouverte contre le mur est, la porte reste à 6 po de la gare.

#### Points à vérifier — à valider avec la Ville et un professionnel

- **Fenêtres ouv-SS-009 et ouv-SS-010** : elles sont notées « fixe » au relevé, mais une fenêtre d'évacuation doit **ouvrir**.
  - Ouverture libre d'au moins 0,35 m², aucune dimension sous 380 mm, puits extérieur dégagé.
  - L'allège (56 po) et la tête (86 po) sont PRÉSUMÉES : à mesurer.
  - La banquette fixe qui sert de marche est à faire accepter par la Ville.
  - Il faut un limiteur d'ouverture qui se déverrouille sans outil (enfant de 4 ans et banquette).
- **Murs de fondation** (x = 10, y = 370) : l'épaisseur réelle des fourrures et de l'isolant est inconnue.
  Laisser ½ po d'air derrière les caissons, aucun dos en contact avec le béton, et des pieds réglables sur le béton poli.
- **Ancrages** : la canopée, les bibliothèques, la garde-robe et la gare sont vissées dans les montants ou les fourrures (attaches anti-basculement).
  Sur P05, il ne faut pas percer la niche du bain.
- **Électricité** : toutes les prises sont TR (inviolables). Les prises derrière le lit et la garde-robe sont déplacées dans les niches ou au-dessus du comptoir de jeu.
  Il faut un détecteur de fumée et de CO relié, dans la chambre ou le hall.
- **Arêtes et quincaillerie** :
  - rayon de 1 po aux coins à hauteur de tête : lit, banquette, gare, vestiaire ;
  - crochets à bout rond ;
  - fermeture douce et butées sur tous les tiroirs ;
  - un seul tiroir ouvert à la fois dans la tour.
- **Hauteurs** : plafond de 96 po, aucune poutre dans la chambre (la poutre arrière est à y = 204). Il reste 50 po libres au-dessus du matelas, sous la canopée.

## Chambre 2 et walk-in — le grand de 6 ans

### Chambre 2 (le grand, 6 ans) et son walk-in — « La bibliothèque secrète »

Pièce réelle : 203¾ × 137¾ po (x 242¼-446, y 232¼-370), ≈ 195 pi², plafond 96 po (aucune poutre au-dessus).
Une seule fenêtre (ouv-SS-003, mur est, y 268-348) ; les deux portes sont dans le coin ouest (chambre ouv-SS-P06 et
walk-in ouv-SS-008). Murs sauge (SS-16), béton poli au sol, chêne blanc (placage), armoires hautes blanc chaud mat,
quincaillerie et crémaillères noir mat. Module : `zone_chambre2.py` ; plan P-127, maquette 3D (arrêts « Chambre 2 — … »
et « Walk-in — … »).

#### Ce qui change et pourquoi

| Élément | Où (po) | Ce que ça donne |
|---|---|---|
| **Mur de tête intégré** (mur arrière y = 370) | x 245-446, 12 po de profondeur | Tout le mur devient un seul meuble : porte-bibliothèque, tour gauche (bacs en bas, 2 niches éclairées, armoire haute), 2 chevets-niches (base ouverte pour les pantoufles, tiroir au niveau du matelas, niche avec DEL, USB-C et interrupteur de veilleuse à sa portée), **alcôve de lattes de chêne** sur feutre acoustique noir avec 2 liseuses encastrées à 39 po, et un **pont d'armoires hautes** (z 66-96) jusqu'au bout du banc ; DEL linéaire 2700 K dessous = lumière de lecture indirecte. 44 po libres entre le matelas et le dessous du pont. |
| **Lit queen sur plateforme-tiroirs** | socle 66 × 84 (x 322-388, y 283-367), dessus du matelas à 22 | Lit bas (jamais en hauteur), centré sur le mur de tête : 30 po côté banc, 67¾ po côté jeu, 34¾ po au pied. Dessous ≈ 25 pi³ : 2 tiroirs de chaque côté, 2 bacs-wagons sur roulettes au pied (LEGO, peluches ; dans la maquette, celui de droite est sorti), réserve centrale avec trappe (saisons, accès adulte). Socle noir en retrait de 3 po, coins arrondis, fixé au mur. |
| **Porte-bibliothèque secrète** | baie existante du caveau, x 245-277 (panneau 32 × 82, 8 po hors tout) | Il tire sur le **livre rouge**, la bibliothèque pivote et il entre dans SON walk-in ; miroir pleine hauteur au dos. Même baie et même sens que la porte SS-16 (pivots côté ouest, ouvre vers la chambre). 5 rebords minces à lèvre, rien sous 8 po (pas d'échelle), s'ouvre en poussant depuis le walk-in (aucun verrou), ferme-porte amorti, butée à 90°, protège-doigts. Imposte-bibliothèque fixe au-dessus (cache le linteau). |
| **Banc-cabane sous la fenêtre** | x 418-446, y 262-370, assise à 18 | 3 grands tiroirs (celui du milieu a un fond amovible = trappe d'accès au drain existant 432½, 314¼), coussin attaché de 27 × 75 = lit d'appoint pour un ami, coussins de dos, 2 liseuses murales avec USB, rail-rideau au plafond (x = 416) : on tire le rideau de lin et c'est une cabane ; plus tard, coin lecture/jeux vidéo. Dessus fixe = marche vers la fenêtre d'évacuation. |
| **Tour à trésors** (coin NE) | x 418-446, y 232¼-262, 0-96 | 3 cases à bacs à jouets à sa hauteur (z 3-45), vitrine ouverte éclairée pour les LEGO (z 45-66), armoire haute pour les jeux de société (adulte). Ancrée. |
| **Garage à jouets** (mur du vestiaire) | x 284-418, y 232¼-248¼, banc à 16 | 4 bacs-wagons 30 × 14 × 12 sur roulettes feutrées, poignées découpées, étiquettes-photos ; au-dessus, 2 rebords à livres présentés de face (z 26 et 40) et un rail de galerie magnétique pour ses dessins (z 54-62). Remplace la commode SS-16. |
| **Mur d'activité** (mur mitoyen x = 240, côté ch. 2) | x 242¼-254¼, y 265-328 | Colonne de crochets (souliers, sac d'école à z 40, 2e rangée à z 56 pour plus tard), cases basses à bacs de bricolage, **bureau à rabat sur rail** (caisson à casiers ; rabat 40 × 20 ouvert à z 22, compas amortis), panneau perforé de chêne, armoires hautes avec DEL dessous ; tabouret rond qui glisse sous le pupitre. Remplace le bureau SS-16 sous la fenêtre. |
| **Aire de jeu** | x 258-316, y 254-350 | Tapis de laine 5' × 8' dans la « rue » de 67¾ po entre le lit et le mur d'activité (48 po avec le rabat ouvert). |
| **Walk-in** (ancien caveau) | brut x 229-317, y 380-430 ; fini 83 × 47½ | Isolant rigide 2 po + gypse (SS-16) ; plafond fini supposé à 84 (dalle du perron, **à mesurer**). Penderie double sur crémaillères noires (tringle basse à 34 = SES vêtements, haute à 70 = la grandeur suivante, tablette à 74 + 6 bacs étiquetés, DEL dessous), banc à souliers (assise 17) et crochets ronds, tour de tiroirs (panier à linge coulissant, 3 tiroirs, dessus à 36 pour plier, valet escamotable, tablettes 52/66/80), miroir au dos de la porte, panneau rayonnant au plafond + plafonnier DEL à détecteur de mouvement (remplace la plinthe SS-16 qui tombait sous la tour). |

**Évolution sans démolir** : le caisson du bureau remonte sur son rail (plan à 29 po, bureau d'ado) ; les tringles du
walk-in passent à 40/78 vers 9-10 ans puis à une penderie longue 66 + double 40/80 à l'adolescence (crémaillères :
5 minutes) ; le garage reçoit disques et équipement de sport ; le banc-cabane devient coin lecture ; le lit queen reste.

**Dispositions écartées** : tête sur le mur ouest (le lit tombe entre les deux arcs de porte, 6-8 po de dégagement) ;
tête sur le mur du vestiaire (mur bruyant, le pied frappe la porte du walk-in) ; lit sous la fenêtre (évacuation).

**Retraits SS-16** (plan et 3D) : lit queen et 2 chevets/lampes, tapis, commode elem-SS-P-COMMODE2, bureau et chaise
sous la fenêtre, cadres monstera, plante ; dans le walk-in, tringle unique, tablettes de côté et plinthe électrique ;
le battant uni de ouv-SS-008 (remplacé par la porte-bibliothèque).

#### Frontières (autres zones)
- Mur mitoyen x = 240 (mur-SS-P07, chambre 1) : le mur d'activité (12 po) y est fixé de y 265 à 328 ; **blocage 2x6 et
  laine de roche acoustique dans la cloison** ; éviter un meuble lourd dos à dos au même endroit côté chambre 1 (ou
  partager le blocage). Aucune cloison déplacée.
- Mur du vestiaire y = 230 (mur-SS-P11) : garage à jouets fixé côté chambre ; rien ne change côté vestiaire.
- Porte de la chambre ouv-SS-P06 : inchangée (32 po, pentures x = 246) ; son battant ouvert se range le long du mur
  ouest, devant rien. Porte du walk-in ouv-SS-008 : même baie, même sens ; marquée « fermée » dans les données pour que
  la maquette 3D dessine la porte-bibliothèque (le battant uni reste caché dans la baie, miroir côté walk-in).

#### Écarts avec la spec de conception
- Mur d'activité décalé de 1 po (y 265-328 au lieu de 264-328) : le battant ouvert de la porte de la chambre arrive à
  y = 264¼ dans la maquette.
- Rail-rideau : dessiné droit le long de x = 416 (y 262-358), arrêté sous le pont d'armoires ; le retour du « L » le
  long de la tour NE est inutile (la tour est pleine hauteur).
- Porte-bibliothèque : 5 rebords minces à lèvre, livres de petit format de dos et un livre de face par rebord (sécurité
  « rien de grimpable » de la spec) plutôt que des tablettes profondes.
- Miroir : dans la maquette, posé sur le battant caché dans la baie (y ≈ 376) plutôt qu'au dos même de la
  bibliothèque (y = 370), et rendu en inox satiné (la visite 3D calcule le reflet d'un miroir du côté de la chambre,
  pas du walk-in) ; en réalité c'est un miroir de sécurité (verre laminé ou acrylique) vissé au dos de la
  porte-bibliothèque.
- Tabouret rond du pupitre et jouets (camion, train de bois, ballon, LEGO dans le bac-wagon sorti) : accessoires de
  mise en scène seulement.

#### Coût (estimation du designer, non sourcée — 2 ou 3 soumissions d'ébénistes de la Côte-Nord)
| Poste | Fourchette |
|---|---|
| Lit-plateforme intégré (tiroirs, bacs-wagons, réserve) | 2 500 - 4 500 $ |
| Mur de tête (tour, 2 chevets-niches, lattes, pont, DEL) | 5 500 - 9 500 $ |
| Porte-bibliothèque secrète (pivots, loquet, miroir, imposte) | 2 500 - 4 000 $ |
| Banc-cabane (3 tiroirs, coussins, rail-rideau) | 2 000 - 3 500 $ |
| Tour NE + garage à jouets + rebords/galerie | 3 000 - 5 000 $ |
| Mur d'activité (rail, rabat, panneau perforé, armoires) | 2 500 - 4 500 $ |
| Walk-in aménagé (crémaillères, tiroirs, banc, miroir, bacs) | 3 500 - 6 000 $ |
| Électricité (liseuses, USB, DEL, détecteur, panneau rayonnant) | 2 000 - 3 500 $ |
| **Total** | **≈ 24 000 à 42 000 $** (hors matelas 800-1 500 $ et hors isolation du caveau déjà prévue à SS-16) |

Option économique : caissons de série (armoires de cuisine ou système de penderie) avec façades de chêne sur mesure,
environ −30 à −40 %.

#### Options pour le client
- **A (retenue)** porte-bibliothèque secrète ; **B** (≈ −2 000 $) porte pleine de chêne avec miroir, la bibliothèque
  devient fixe à côté.
- Sous le lit : tiroirs et bacs-wagons (retenu, sûr à 6 ans) ou, à l'adolescence, plateforme à vérins avec verrou.
- Bacs-wagons du pied remplaçables par un lit gigogne simple (soirées pyjama) si le banc-cabane ne suffit pas.
- Façades basses : chêne naturel partout (retenu) ou laque sauge un ton plus foncé que les murs.
- Mur d'activité : panneau perforé de chêne (retenu) ou tableau magnétique/craie pleine largeur.

#### Points à vérifier — à valider avec la Ville de Baie-Comeau et un professionnel
- **Fenêtre d'évacuation ouv-SS-003** : largeur réelle (80 lu / ≈ 72 au dessin), allège (56 PRÉSUMÉE), type d'ouvrant ;
  ouverture libre ≥ 0,35 m², aucune dimension < 380 mm ; le banc fixe à 18 po sert de marche, rien d'autre devant le
  vitrage. **À valider avec la Ville et un professionnel.**
- **Caveau** : hauteur libre sous la dalle du perron et niveau du plancher (marche ?) — dessiné pour 84 po finis ; si
  moins, on baisse la tringle haute et la tablette. Humidité < 50 % HR pendant un mois après l'isolation AVANT d'y
  ranger les vêtements (déshumidificateur les premiers mois).
- **Baie de la porte du caveau** : hauteur (dessinée 80) et état du linteau ; poids de la porte-bibliothèque (pivots
  à usage intensif dimensionnés en conséquence, quincaillerie certifiée).
- **Drain existant** (432½, 314¼) sous le banc : bouchonner ou garder accessible (trappe prévue) ; siphon et odeur.
- **Électricité** (électricien maître) : prises inviolables (TR), circuits des DEL et USB, panneau rayonnant du walk-in
  (dégagements du fabricant, thermostat), détecteur de fumée de la chambre.
- **Ancrage** : attaches anti-basculement dans le béton pour la tour gauche, la tour NE et la tour du walk-in ; meubles
  du mur de tête fixés à travers la fourrure isolée ; blocage dans la cloison mitoyenne x = 240.
- **Conduits ou tuyaux** sous les solives au-dessus du mur arrière : le pont monte à 96 po (plafond mesuré).
- **Sécurité enfant** : fermeture douce partout (tiroirs, portes, rabat amorti), coins arrondis R 1 po, rideaux et
  stores sans cordon en boucle, aucun meuble grimpable sous la fenêtre autre que le banc, porte-bibliothèque sans
  verrou et toujours ouvrable de l'intérieur du walk-in.

## Dessous de l'escalier

### Le dessous de l'escalier : le banc-cabane cinéma

> « En dessous des marches, je pense à quelque chose… je veux pas que ça bloque toute la vue. »

Dans SS-15, les trois caissons fermés avaient été refusés ; dans SS-16, le dessous était resté vide. SS-17 y met
**quelque chose d'utile pour des enfants de 4 et 6 ans sans fermer la vue** : on n'occupe que la bande basse.
**Rien de plein au-dessus de 26 po** (seule exception : la « lune », collée sous une marche à 80 po). Vu du séjour, le banc
reste caché derrière le dossier du divan (31 po) et l'escalier flotte toujours devant le verre du gym.

```
 verre du gym (x = 228)                                rampe à barreaux (x = 271) → séjour, divan en L
   │ ¾ po
   │ ┌ garde-pieds   ┌──────── coin-cabane 42½ po ────────┐┌──────── banc 75¾ po ────────┐┌ sabot + chasse ┐
   │ │ (0-12)        │ matelas de laine 32 × 32 × 4       ││ L │ 1 │ 2 │ 3 │ 4 │ 5        ││ 24 V, USB,     │
   │ │               │ 2 coussins, lune Ø 12 au-dessus    ││ livres + 10 bacs de feutre   ││ détecteur      │
 mur avant (y = 10) : 2 rebords à livres     poteau du pivot (234, 50)        pied de l'escalier (y = 150)
```

#### Ce qui change dans la zone (P-127 et maquette 3D)
| Élément | Description | Pourquoi |
|---|---|---|
| **Banc de chêne bas, ajouré** (x 229¾-270¼, y 52½-128¼, dessus à 16 po) | Contreplaqué de chêne blanc ¾ po, chants massifs, arêtes arrondies (r ½ po), huile-cire mate. **6 cases traversantes** ouvertes côté séjour (arrêt bas côté verre) : 1 case à livres de 9¼ po + 5 cases de 12¼ po | Rangement à la hauteur des enfants ; aucune porte, aucun couvercle, aucune quincaillerie : rien qui pince |
| **Socle d'acier noir en retrait** (3 po) + **ruban DEL 2700 K** collé sous les deux débords du caisson (côté séjour et côté verre), devant le socle | Le banc « flotte » comme les marches ; la nuit, veilleuse à 10 % sur détecteur (un enfant qui sort de la chambre 2 voit la première marche) ; 5 % ou éteint en mode cinéma | Même langage que l'escalier flottant ; sécurité la nuit |
| **10 bacs de feutre de laine** (30 × 42 × 23 cm), poignée cuir cognac, **étiquettes d'ardoise** à la craie | 2 bacs par case : bac « enfant » devant (côté séjour), bac « parents / rotation des jouets » derrière. Cases 1-3 : jouets ; cases 4-5 : **cinéma** (jeux de société, manettes, 2 jetés à 3 pas du divan) | ≈ 290 L de rangement ; l'ardoise rappelle celle du rez-de-chaussée |
| **Assise cuir cognac** (38¾ × 32½ × 2½ po, dessus à 18½ po), **dossier bas de chêne** (dessus à 26 po) et **traversin** Ø 7 po | Housse zippée cuir pleine fleur (s'essuie : jus, crayons) ; le dossier garde le dos des enfants loin du verre (¾ po de jeu, rien n'y est fixé) | Coin lecture ; 32 à 54 po libres au-dessus de l'assise sous les marches 7 à 10 |
| **Présentoir à livres de face** (dessus à 24 po) | Bac de chêne en gradins, 3 rangs de livres couverture vers le séjour | Les enfants choisissent par la couverture |
| **Plateau-télécommandes** + **USB-C** (basse tension) | Plateau creux doublé de feutre (télécommandes, manettes) ; ferme la fente de 4½ po sous la marche 3 (il reste 2 po) | Fonction cinéma ; aucune fente de 3½ à 9 po (piège à tête) |
| **Sabot technique** (≤ 11 po) et **chasse** de 3½ po sous la marche 1 | Panneau avant vissé : bloc 24 V gradable, module USB, détecteur (lentille vers la porte de la chambre 2) ; le 120 V reste dans le sabot fermé. La chasse s'arrête à y = 148½, avant le pied du limon | Plus de jouets ni de petites mains coincés sous les premières marches |
| **Coin-cabane** sous les marches tournantes | Matelas de laine feutrée crème 32 × 32 × 4 po (housse lavable), 2 coussins (cuir cognac, laine crème), **garde-pieds** de chêne de 12 po ¾ po devant le verre, **2 rebords à livres** bas sur le mur avant (z 5-8 et 20-23) | 76½ po libres au-dessus du matelas : un adulte s'y assoit, un enfant s'y tient debout |
| **La lune** : disque opalin Ø 12 po, 1 po d'épaisseur, sous la marche tournante T1 (z 79½-80½) | DEL 2700 K gradable 5-100 % ; fil 24 V par l'intérieur du poteau du pivot puis une rainure refermée par une latte de chêne ; **bouton-poussoir de laiton** à hauteur d'enfant sur le flanc du banc, côté cabane | L'« effet wow » : les enfants allument leur lune eux-mêmes |

Plan P-127 : banc, sabot et chasse, matelas-cabane, rebords à livres et lune (pointillé, au plafond) dessinés sans
libellé sous l'escalier (la note 4 les nomme). Rien ne change aux murs, aux portes ni à l'escalier.

#### Pourquoi celle-là (options comparées)
| Option | Vue libre (élévation) | Au-dessus de 26 po | Rangement | Pour les enfants | Cinéma | Coût | Verdict |
|---|---|---|---|---|---|---|---|
| **A. Banc-cabane** | ≈ 67 % | 100 % libre | ≈ 290 L + livres | excellent | faible | 6 000 – 9 500 $ | **retenu comme base** |
| B. Tiroirs dans les marches 1-3 | ≈ 95 % | 100 % libre | ≈ 150 L | faible (obstacle au pied de l'escalier) | faible | 3 500 – 5 500 $ (marches refaites en caissons : on perd l'escalier flottant) | rejeté |
| C. Console basse ajourée « cinéma » | ≈ 80 % | 100 % libre | ≈ 250 L | moyen | bon | 3 000 – 5 000 $ | **fusionné dans A** (cases 4-5, plateau, USB-C) |
| D. Jardin intérieur éclairé | ≈ 60-70 % | partiel | 0 | risqué à 4 ans (terre, gravier, eau sur le béton poli) | lampe | 1 500 – 3 000 $ + entretien | rejeté ; une plante sous la lune pour l'adolescence |

Par rapport au premier concept (escalier_1) : coussin **cuir cognac** au lieu du vert forêt (le client a rejeté le vert),
**lune** au lieu d'un spot, plateau qui ferme la fente sous la marche 3, chasse raccourcie avant le pied du limon,
garde-pieds devant le verre, veilleuse sur détecteur, USB-C.

#### Frontières avec les autres lots
- **Verre du gym** (x = 228, autre agent) : rien n'y est fixé ni collé ; banc, dossier et garde-pieds à ¾ po, ancrés à la dalle.
- **Escalier** (fabricant) : la lune est vissée sous T1 (vis ≤ 1¼ po dans 2 po de chêne) ; fil 24 V dans le poteau d'acier du
  pivot (perçage en atelier, avant la peinture). Aucun élément ne touche le limon (1 po de jeu ; 2 po sous les marches 1-3).
- **Séjour** : rien ne dépasse x = 270¼ ; le passage rampe ↔ dossier du divan reste à **30⅝ po**.
- **Dalle / béton poli** : 4 ancrages du socle + 2 du garde-pieds ; conduit électrique noyé dans la chape (option B) ou
  rainure sciée (option A) jusqu'au sabot, **avant le polissage**.

#### Évolution (10-14 ans)
Le coin-cabane devient un coin pouf / jeux vidéo, ou reçoit une grande plante sous la lune ; les bacs « jouets » deviennent
jeux de société et manettes ; rien à démolir.

#### Coût (ordre de grandeur, $ CA 2026 avant taxes, Baie-Comeau)
| Poste | Min | Max |
|---|---:|---:|
| Banc de chêne ajouré (6 cases, socle d'acier, plateau-télécommandes) — ébéniste | 2 600 | 3 800 |
| Sabot technique + chasse | 450 | 700 |
| Présentoir, 2 rebords à livres, garde-pieds | 500 | 850 |
| Coussin, dossier rembourré et traversin cuir cognac sur mesure | 1 100 | 1 700 |
| 10 bacs de feutre + étiquettes d'ardoise | 300 | 500 |
| Matelas-cabane 32 × 32 × 4 laine + 2 coussins | 250 | 450 |
| Lune DEL, ruban 2700 K, bloc 24 V gradable, détecteur, bouton, module USB-C | 450 | 800 |
| Électricien (conduit avant polissage, raccords, passage dans le poteau avec le fabricant) | 700 | 1 300 |
| **Total** | **6 350** | **10 100** |

Version sobre (tissu performance au lieu du cuir, sans lune ni USB) : ≈ 4 800 – 7 500 $.

#### Options pour le client
1. Assise : **cuir cognac** (dessiné) ou tissu performance lavable (caramel, gris chaud).
2. La lune : disque lunaire (dessiné), simple rond opalin, ou 20 « étoiles » DEL à fibre optique sous T2 et T3.
3. Cases : 3 « jouets » + 2 « cinéma » (dessiné) ou 4 + 1 ; un tiroir à roulettes plein (Lego) à la place de 2 bacs.
4. Rideau de cabane : toile de lin sur tringle sous T1, attachée ouverte (on la ferme pour jouer).
5. Le verre du gym, côté cabane, comme tableau à dessin (crayons pour vitres).
6. Ruban DEL sous chaque nez de marche (lot escalier) : chemin lumineux de nuit vers les parents.

#### Points à vérifier (ne pas tenir pour conforme sans vérification)
- **Contremarches ouvertes** de l'escalier flottant (≈ 5½ po entre les marches) : la règle courante pour les enfants est
  qu'une sphère de 4 po (100 mm) ne passe pas. Faire valider par le concepteur de l'escalier ; au besoin, une tige d'acier
  noir au milieu de chaque contremarche (lot escalier).
- **Verre du gym** : confirmer verre de sécurité (trempé ou feuilleté, marquage visible) — des enfants jouent à ¾ po.
- Arêtes inférieures des marches 4 à 10 au-dessus du banc et coins du poteau du pivot : **adoucir (r ¼ po)** — un enfant
  debout sur le banc s'y cogne.
- Électricité : conduit avant le polissage ; circuit et protections (DDFT / AFCI, prises inviolables) selon l'électricien ;
  120 V seulement dans le sabot vissé ; tout le reste en 24 V.
- **Relevé réel de l'escalier** avant fabrication (contremarche de 7½ po déduite de 105 po / 14 ; position du limon et du
  pivot) ; perçage du poteau du pivot : accord du fabricant.
- Mousses certifiées (CertiPUR ou équivalent), housses lavables.
- Ancrages dans la dalle : avec l'option A (dalle existante polie), les trous restent visibles si on déplace le banc.

#### Maquette 3D
Nouveaux arrêts : **« Banc-cabane cinéma (sous l'escalier) »** (depuis le passage rampe ↔ divan) et **« Coin-cabane et
sa lune »** (petite lumière sous la marche T1). Matériaux du catalogue : `placage` (chêne), `cuir` (cognac), `tissu`
(feutre des bacs), `tapis` (matelas de laine), `draps` (coussin crème), `ardoise_noire` (étiquettes), `laiton` (bouton) ;
`metal` (acier noir) et `spot` (DEL, lune) de la visionneuse. Aucun nouveau modèle 3D.

À valider avec la Ville de Baie-Comeau et un professionnel.

## Gym

### Le gym (salle d'entraînement, P-127)

**Idée :** tout le mur du lavage devient un **miroir de 12 pi, porte comprise** : la porte du lavage disparaît dans le
miroir, la pièce de 9'-4" paraît deux fois plus large et reflète l'escalier flottant. Devant ce miroir, un **vrai
plancher libre de 6 × 6 pi**. Le **tapis roulant et le vélo sont regroupés côte à côte contre le mur avant**, face à
une télé commune.

Pièce : 112¾ × 146 po au nu (9'-4¾" × 12'-2", 114 pi²), plafond 96 po (86 po sous la retombée de la poutre avant,
bande y 152–156), aucune fenêtre. Verre sur le hall (y = 157) et sur l'escalier (x = 228). La salle de lavage n'a pas
d'autre accès : on traverse le gym de la porte vitrée à la porte du lavage ; ce trajet occupe le fond ouest du gym.
Sur le plan, la pièce s'appelle maintenant **« Gym »** (le nom long ne tenait plus entre les appareils dessinés).

#### Ce qui change par rapport à SS-16

| SS-16 | SS-17 | Pourquoi |
|---|---|---|
| Tapis roulant le long du mur avant, face au verre de l'escalier : 34 po derrière, console à 4 po du verre | **Tapis roulant contre le mur avant, face au mur** (console à 2 po du mur) : 20 po libres de chaque côté, **69 po derrière**, vers le coin est où personne ne passe | L'arrière de la bande ne donne plus sur le trajet du lavage, où passent les enfants |
| Vélo en travers de la pièce, au milieu | **Vélo à côté du tapis, roue avant vers le mur avant**, avec une allée de 22 po entre les deux pour monter | Libère tout l'arrière de la pièce |
| Haltères et kettlebells au sol, sur un tapis | **Poids sous clé** dans les tiroirs d'un **banc-coffre bas** (16 × 60 × 18 po) contre le verre de l'escalier | Enfants de 4 et 6 ans : rien de lourd ou d'écrasant à leur portée ; le banc reste bas, la vue vers le séjour reste |
| Miroir sur le mur avant | **Mur-miroir sur le mur du lavage** (105 × 74 po, 4 panneaux, pellicule de sécurité) + **miroir sur la face gym de la porte du lavage** (cadre noir) : 12 pi continus | Fait face au plancher libre (yoga, poids, étirements) ; le cycliste voit sa position de profil |
| — | **Zone au sol 72 × 72 po** en dalles de caoutchouc 24 × 24 de 10 mm | Poids libres, yoga, jeu au sol avec les enfants ; c'est aussi le passage vers le lavage, donc rien n'y reste à demeure |
| — | **Tablette haute de chêne** pleine largeur à 78 po (serviettes, bouteilles, haut-parleur, trousse de premiers soins, ventilateur oscillant), DEL dessous | Rangement au-dessus des têtes, hors de portée des enfants |
| — | **Télé de 40 po sur bras articulé** entre les deux appareils (pivote vers le tapis ou le vélo), câbles dans le mur | Un seul écran pour les deux appareils |
| — | **Colonne de crochets d'acier noir** (62, 68 et 74 po) au coin est du mur avant : élastiques, corde à sauter, sangle, 2 tapis de yoga ; **clé du tapis roulant à 66 po** | Corde et élastiques (risque d'étranglement) hors de portée ; tapis inutilisable sans sa clé |
| Porte vitrée battante (arc de 32 po dans la pièce) | **Porte vitrée coulissante**, rail apparent noir et vantail **côté hall**, rangée vers l'est (x 184–216) ; amortisseurs aux deux bouts, loquet haut à 60 po | Aucun arc dans la zone au sol ni dans l'aire de sécurité du tapis |
| 2 encastrés | **6 encastrés plats 3000 K gradables** + **DEL linéaire au plafond qui lave le miroir** ; **extracteur** silencieux au plafond | Lumière égale et sans éblouissement (yoga) ; humidité et odeurs |

Murs anthracite gardés, béton poli, caoutchouc noir, chêne, cuir cognac sur le coussin du banc, acier noir.

#### Dégagements

| Élément | Obtenu | Cible | Statut |
|---|---|---|---|
| Tapis roulant, côtés | 20 po (ouest) / 20 po (est, jusqu'au verre) | 20 po | OK |
| Tapis roulant, derrière | **69 po** | 79 po (2 m, ASTM F2115) | **Court de 10 po** : à accepter, ou options C ou D |
| Plafond au-dessus du plateau | 88 po | taille du coureur + ~6 po | OK jusqu'à ~6'-6" |
| Allée de montée du vélo | 22 po | 20 po | OK (partagée avec le côté ouest du tapis) |
| Zone au sol | 72 × 72 po | 72 × 72 po | OK ; sa bande est (15 po) est la fin de l'aire de sécurité du tapis : on ne s'y met pas quand quelqu'un court |
| Passage vers le lavage | 38 po de large | 36 po | OK si la zone au sol est rangée |
| Porte du lavage | ouvre côté lavage | aucun arc dans le gym | OK |
| Banc-coffre / aire de sécurité | 3 à 4 po hors de l'aire | hors de l'aire | OK ; tiroirs (14 po) ouverts seulement tapis arrêté |

#### Options pour le client
- **A — Porte du gym :** coulissante vitrée côté hall (recommandée, 1 200–2 500 $) ou garder la battante actuelle (0 $ ;
  on la garde fermée quand quelqu'un court ; son arc tombe dans la zone au sol).
- **B — Poids :** tiroirs à clé du banc-coffre (recommandé avec des enfants de 4 et 6 ans) ou support mural vertical
  ouvert au coin est du mur avant (plus pratique, moins sûr).
- **C — Tapis roulant :** garder l'appareil actuel (69 po derrière) ou passer à un modèle compact ou pliable de 66 po ou
  moins (79 po derrière ; la zone au sol perd son petit coin).
- **D — À explorer :** ouvrir le mur de fondation vers l'excroissance sous le perron (x 168–228) pour y loger la console
  du tapis (plus de 79 po derrière) : sciage du béton, linteau, ingénieur, isolation et étanchéité de la dalle du perron ;
  environ 10 000–20 000 $ ; hauteur et état de l'excroissance inconnus.
- **E — Écran :** télé 40 po sur bras (recommandée) ou tablette seulement ; bonus sans frais : du fond de la zone au sol,
  on voit la toile de 120 po du séjour à travers le verre, au-dessus des marches.
- **F — Miroir :** verre avec pellicule de sécurité (recommandé, net) ou acrylique (incassable, reflet un peu ondulé).

#### Ordre de grandeur (CAD, installé, 2026 — à confirmer par soumissions)

| Poste | Coût |
|---|---|
| Miroir mural 105 × 74 avec pellicule de sécurité | 900–1 600 $ |
| Miroir sur la porte du lavage + 3e penture | 250–500 $ |
| Banc-coffre de chêne sur mesure (tiroirs à clé, glissières 100 lb à fermeture douce, coussin) | 1 500–3 000 $ (500–900 $ en modulaire du commerce) |
| Tablette haute de chêne 112 po, supports cachés, DEL | 350–700 $ |
| Colonne de crochets d'acier noir | 100–250 $ |
| Bras articulé de télé (télé 40 po neuve : + 350–600 $) | 100–250 $ |
| Dalles de caoutchouc 10 mm (≈ 36 pi²) et tapis sous les appareils | 300–600 $ |
| Électricité : circuit 20 A dédié au tapis, 3 prises, interrupteurs, 6 encastrés, DEL linéaire | 1 800–3 200 $ |
| Extracteur silencieux 80–110 pcm, conduit, minuterie | 700–1 300 $ |
| Ventilateur oscillant | 60–150 $ |
| **Total** | **≈ 6 000–11 500 $** ; porte coulissante vitrée en plus : 1 200–2 500 $ |

#### Frontières avec les autres zones
- **Mur du lavage (mur-SS-P08, x = 112)** : miroir sur la face gym seulement, et sur la face gym de la porte ouv-SS-P02
  (dessinée **fermée** dans la 3D pour montrer l'effet ; elle ouvre toujours côté lavage). Rien ne change côté lavage.
  Si la porte du lavage est déplacée, le miroir se redécoupe.
- **Verre du hall (mur-SS-P10) et porte ouv-SS-P01** : la porte devient **coulissante** (plan et 3D) ; vantail et rail
  côté hall entre x 151 et 218 : rien à placer contre ce verre côté hall entre x 184 et 218.
- **Verre de l'escalier (mur-SS-P09, x = 228)** : seulement le banc-coffre de 20½ po de haut côté gym ; rien de haut
  contre ce verre. La vue du gym vers le séjour passe sous le haut de l'escalier et au-dessus des marches du bas.
- **Mur de fondation avant** : ancrages de la tablette, du bras de télé et des crochets ; prises ; sortie possible de
  l'extracteur à l'ouest du perron. **Plafond du gym** : extracteur, 6 encastrés, DEL linéaire.

#### Points à vérifier
- Mesurer le tapis roulant (longueur, largeur, hauteur, pliable ?) et ses exigences électriques (120 V 15/20 A dédié ou
  240 V ; certains fabricants déconseillent le disjoncteur DDFT) ; mesurer le vélo et sa base. La maquette utilise un
  tapis générique de 75 × 41 po.
- Aire de sécurité de 69 po au lieu de 79 : à accepter par le client, sinon option C ou D.
- Verre des cloisons y = 157 et x = 228 et de la porte : **verre de sécurité trempé ou feuilleté obligatoire** ;
  feuilleté recommandé derrière le tapis.
- Le trajet vers le lavage traverse le gym : c'est le seul accès (porte P02 ; le lavage ne touche pas le hall).
- Hauteur : 96 po (propriétaire) ; vérifier conduits ou tuyaux sous le plafond du gym et la retombée de la poutre avant
  (y 152–162, 86 po) où s'accroche le rail de la porte coulissante.
- Sortie de l'extracteur à l'ouest du perron, pas sous sa dalle ; air de compensation (jeu sous la porte vitrée).
- Caoutchouc sur béton poli : certains caoutchoucs tachent ou jaunissent le béton ; faire un essai ou prendre un endos
  non tachant.
- Porte-miroir : poids, 3 pentures, perçage de la poignée ; ancrages au béton du mur avant (tablette, bras de télé,
  crochets).
- Sécurité des enfants : loquet haut à 60 po sur la porte du gym ; clé du tapis toujours retirée et accrochée à 66 po ;
  tiroirs du banc verrouillés ; option : prise du tapis commandée par un interrupteur à 60 po près de la porte (à valider
  avec l'électricien).
- **Code et sécurité : à valider avec la Ville de Baie-Comeau et un professionnel** (électricien, entrepreneur,
  ingénieur pour l'option D). Rien ici n'affirme la conformité.

#### Maquette 3D
Arrêts de visite : **« Gym — mur-miroir et zone au sol »** (du coin est, vers le miroir) et **« Gym — cardio »** (de
la porte, vers le mur avant) ; « Gym (porte vitrée) » montre la porte coulissante rangée côté hall. Le tapis roulant et
le vélo sont les modèles du catalogue (tapis_roulant, velo_route_base) ; les poids ne sont plus montrés (rangés dans les
tiroirs du banc).

## Le reste du sous-sol

### Le reste du sous-sol : vestiaire d'hiver, trajets de nuit, séjour, salle de bain et lavage (zone « global »)

Les deux garçons ont **4 et 6 ans** (novembre 2026) ; l'hiver à Baie-Comeau, ils entrent par la **porte de côté** avec
bottes, habits de neige et mitaines mouillées. Le vestiaire, le hall et le séjour de SS-16 étaient pensés pour des
adultes : crochets à 58 po, tablette à 66 po, armoire fermée, rien pour les jouets. Huit changements, classés par impact
sur le quotidien et par coût. Les **armoires vert forêt du vestiaire sont gardées telles quelles**, le **mur du bain** et
la **galerie de photos du séjour** ne sont pas touchés (refaits dans SS-16), ni les chambres, le gym ou le dessous de
l'escalier. Feuille **P-127** ; maquette 3D (arrêts « Casiers d'hiver des garçons », « Seuil à neige », « Trajet de
nuit vers la salle de bain », « Banc à jouets sous la toile », « Paniers de linge des garçons »).

| # | Pièce | Ce qui change | Pourquoi | Ordre de grandeur* |
|---|---|---|---|---|
| 1 | Vestiaire | **Casiers d'hiver des garçons** (un chacun) dans le pan de mur perdu entre la porte de la chambre 2 et la colonne C03 : séchoir à bottes et mitaines à air tiède, crochets à 36 et 44 po, tablette à 46 po, portes hautes vert forêt ; **poste de recharge** sous les armoires vertes ; colonne C03 habillée de chêne à coins arrondis | Chaque garçon s'habille et range seul, à sa hauteur ; mitaines et bottes sèches et tièdes le lendemain matin | 2 000 à 3 500 $ |
| 2 | Vestiaire (porte de côté) | **Tapis-grille encastré** affleurant (48 × 36 po) devant la porte ; **sol chauffant** devant le banc et les casiers ; **bacs d'égouttement** sous le banc à la place des cases à souliers | Neige, calcium et gravier restent dans le premier mètre ; le béton poli ne devient pas une patinoire et ne se raye pas | 1 500 à 3 000 $ |
| 3 | Tout le sous-sol | **Insonorisation** : plafond (laine de roche, barres résilientes, 2 gypses ⅝ po type X), laine dans les cloisons des chambres et de la salle de bain, portes de chambres à âme pleine avec joints ; **nuage de lattes de chêne** au plafond du séjour | Les garçons dorment à 19 h 30 à 6 pi du cinéma ; béton, gypse et verre font résonner le séjour | 5 000 à 9 000 $ |
| 4 | Hall, vestiaire, salle de bain | **Veilleuses à détection** à 10–13 po du sol (ambre 2200 K, mode nuit), DEL sous la vanité, interrupteur à détection à 42 po, colonne C02 adoucie | Le garçon de 4 ans trouve la salle de bain seul, sans plafonnier qui le réveille, sans heurter la colonne | 500 à 1 000 $ |
| 5 | Séjour | **Banc-rangement à jouets** de chêne pleine largeur sous la toile (143 × 16 po, dessus à 16 po), 6 tiroirs, niche ventilée, barre de son dessus ; **boîte de plancher** au bout du divan ; **store sans cordon** | Les jouets se rangent en 2 minutes là où l'on joue ; plus de rallonge dans le passage | 2 500 à 4 500 $ |
| 6 | Lavage, salle de bain, vestiaire, séjour | **VRC** (échangeur d'air) avec évacuations à la salle de bain, au lavage et au vestiaire ; **déshumidificateur à drain** ; sol chauffant devant le bain et dans l'aire de jeu | Bottes, habits qui sèchent, bain, lessive : l'humidité est le premier risque de moisissure au sous-sol | 4 000 à 7 500 $ |
| 7 | Salle de bain, lavage | **Marchepied** sous la vanité, **crochets à serviette à 38 po**, porte coulissante amortie avec verrou à déverrouillage d'urgence, **mélangeur thermostatique** au chauffe-eau | Autonomie (dents, mains, bain) et sécurité (brûlures, doigts pincés, enfant enfermé) | 400 à 900 $ |
| 8 | Salle de lavage | **Un panier de linge propre par garçon** dans le bas du comptoir de pliage, trieur à 2 sacs, loquet sous le bac, capsules de détergent en hauteur | Une vraie tâche de 4–6 ans ; les capsules sont un danger connu pour les petits | 300 à 700 $ |

\* Estimations du designer (prix Québec 2026, non sourcées), à confirmer par soumissions. Total ≈ 16 000 à 30 000 $.

#### 1. Les casiers d'hiver des garçons (vestiaire)
- **Où** : x 281–319, adossés à la cloison vestiaire / chambre 2 (y = 230), entre le cadre de la porte de la chambre 2
  (x 246–278) et la colonne C03 : un pan de mur de 38 po qui ne servait à rien.
- **Caisson** de chêne (placage, comme le banc) de **38 × 18 × 88 po**, deux baies de 17⅞ po, socle noir de 2½ po en
  retrait, coins avant adoucis ; **ancré au mur** (2 équerres anti-basculement). Baie A (6 ans) à gauche, plaquette et
  serviette **vert forêt** ; baie B (4 ans) à droite, **marine** : le plus jeune reconnaît sa couleur avant de lire.
- **Dans chaque baie**, du bas vers le haut : bac d'égouttement de caoutchouc noir (amovible, se vide à l'évier du
  lavage) ; **séchoir à bottes et mitaines** du commerce (≤ 16 po de large, 4 tiges, air tiède ≈ 40 °C, ≤ 100 W) sur une
  prise dédiée au fond du casier à 30 po ; 2 crochets de laiton à **36 po** (habit de neige, manteau) et 1 à **44 po**
  (sac d'école) ; tablette à **46 po** avec un panier d'osier (tuques, cache-cous, mitaines de rechange) — le garçon de
  4 ans (≈ 40 po) l'atteint ; 2e tablette à 62 po (casques de vélo et de ski).
- **Haut (70–88 po)** : portes **vert forêt** (≈ BM Tarrytown Green HC-134) à charnières à fermeture douce,
  quincaillerie noire, alignées sur les armoires vertes du banc : la ligne verte continue sur tout le mur (habits d'été,
  vêtements « pour l'an prochain »).
- **Minuterie de 2 h des séchoirs** (un bouton, commande des parents) à 48–53 po et **thermostat du sol chauffant** à
  55–60 po, sur la face avant de la colonne C03, dont le nouvel **habillage de chêne à coins arrondis** (R ¾ po) cache
  les fils. Les séchoirs ne restent jamais allumés la nuit.
- **Poste de recharge** (prises 120 V + USB-C, bandeau noir encastré) sous les armoires vertes du banc, au-dessus de la
  tablette à 66 po : cellulaires et tablettes se rechargent ici le soir, pas dans les chambres, hors de portée.
- **Écart avec la spec** : les casiers ont **18 po de profond** (y 209¾–227¾) au lieu de 20, au nu du banc et des
  armoires vertes existantes. Avec 20 po, leur dessus à 88 po aurait buté sur la retombée de la poutre arrière
  (y 199–209, dessous ≈ 86 po). Un séchoir de 15 po de profond y entre sans peine.

#### 2. Le seuil à neige (porte de côté)
- **Tapis-grille encastré** de 48 × 36 po (x 398–446, y 162–198) : cadre et profilés d'aluminium noir, inserts brosse
  et caoutchouc, bac de récupération dessous qui se soulève pour vider l'eau et le gravier. **Affleurant** : aucun bord
  où trébucher, la porte (qui ouvre vers l'intérieur) passe par-dessus.
- **Plancher chauffant électrique** (≈ 32 pi², x 280–398, y 160–199) : câble dans la chape, thermostat avec sonde réglé
  ≈ 27 °C, programmé de novembre à avril. Les flaques sèchent en 1–2 h ; rien de fixe dessus (pas sous les casiers).
- **Bacs d'égouttement** de caoutchouc noir dans les 3 cases du banc existant (bottes des adultes), à la place des
  cases à souliers. Le banc, ses crochets à 58 po, ses armoires vertes et l'armoire à manteaux restent tels quels.
- **Options** : la grille et le sol chauffant supposent la **chape de l'option B** (voir « Le plancher ») ; avec
  l'option A (dalle polie), grille dans une saignée sciée de la dalle et pas de sol chauffant.

#### 3. L'insonorisation (non dessinée en 3D ; notes du plan)
- **Plafond** sous le rez-de-chaussée : laine de roche 3 po entre les solives, barres résilientes, **2 gypses ⅝ po
  type X**, joints scellés au mastic acoustique. Le plafond descend d'environ **1¾ po** (96 → ≈ 94¼ po ; sous les
  poutres habillées, ≈ 84½ po). Encastrés minces DEL ou boîtiers coupe-feu. C'est maintenant ou jamais, avant le gypse.
- **Cloisons** hall et vestiaire / chambres (y = 230) et hall / salle de bain (x = 142) : laine de roche 3½ po ; prises
  décalées d'un côté à l'autre (jamais dos à dos).
- **Portes des chambres** (x 201–231 et 246–278) à **âme pleine**, coupe-son périphérique et seuil automatique,
  fermeture douce — à coordonner avec les chambres.
- **Nuage acoustique** au plafond du séjour (dessiné en 3D) : 3 panneaux de **lattes de chêne sur feutre noir**
  (24 × 94 po chacun, x 302–374, y 37–131), au-dessus du divan, entre le projecteur et la toile, hors du faisceau ;
  encastrés minces entre les panneaux. Il garde le fil du chêne et calme l'écho du béton.

#### 4. Le trajet de nuit (chambres → salle de bain)
- **3 veilleuses encastrées** à **10–13 po du sol**, à détection de mouvement, ambre 2200 K à ≈ 10 %, mode nuit
  22 h–7 h : **V1** entre les portes des deux chambres (éclaire le sol devant les portes et le pied de C02), **V2** sur
  la cloison de la salle de bain côté hall après la colonne C01, **V3** dans le hall côté chambre 1.
- **Colonne C02** (sur le trajet, entre le vestiaire et le hall) : même habillage de chêne à coins arrondis que C03.
- **Salle de bain** : ruban DEL 2200–2700 K **sous la vanité suspendue**, à détection (lumière rasante au sol et sur la
  toilette, sans éblouir) ; **interrupteur à détection à 42 po** (les garçons l'atteignent), côté vanité de la porte
  coulissante, qui allume à 50 % la nuit.
- **Tapis du hall** (sur le trajet, sur du béton poli) : à **endos de caoutchouc antidérapant**.

#### 5. Le banc à jouets sous la toile (séjour)
- Le meuble bas suspendu de 72 po de SS-16 devient un **banc-rangement de chêne pleine largeur** :
  **143 × 16 po, dessus à 16 po** (x 430–446, y 12–155), socle noir en retrait de 3 po avec **DEL ambre** (veilleuse de
  cinéma : les petits voient où ils marchent pendant le film), coins avant arrondis, **ancré au mur**.
- **6 grands tiroirs** de ≈ 20½ po (3 de chaque côté), 11 po utiles, coulisses à extension complète et **fermeture
  douce**, **poignées découpées** (rien qui accroche), **étiquettes en images** (blocs, autos, déguisements,
  casse-têtes…) pour le garçon de 4 ans.
- **Niche centrale ventilée** (porte abattante perforée) sur l'axe de la toile : boîte de diffusion et câble HDMI (fibre)
  qui descend du plafond dans le mur. **Barre de son** posée sur le banc.
- **La toile n'est pas gênée** : en position basse, sa barre de lestage est à ≈ 25 po, au-dessus de la barre de son
  (19¼ po) et du banc (16 po) ; rien ne frotte. Garder la toile remontée quand on ne s'en sert pas et mettre sa
  commande murale hors de portée (≈ 54 po) : un garçon debout sur le banc atteint la barre de lestage.
- La sansevière du coin passe sur le bout avant du banc. Quand la toile est remontée, le mur reste un seul trait de
  chêne calme ; le banc sert d'assise aux enfants (coussin).
- **Boîte de plancher** (2 prises + 2 USB-C, couvercle affleurant de laiton noirci) au bout de l'accoudoir du divan,
  sous un **guéridon avec lampe** : lampe et recharge sans rallonge qui traverse le passage (chape de l'option B ; sinon
  prise murale). Le guéridon reste hors de la bande de passage derrière le divan (x 272–302).
- **Store à enrouleur sans cordon** (occultant) dans l'embrasure de la fenêtre du mur de la toile : aucune boucle.

#### 6. L'air sec et le sol tiède
- **VRC** (échangeur d'air récupérateur de chaleur) suspendu au mur avant de la salle de lavage, à 74–94 po au-dessus du
  retour du comptoir (service par le dessous). **Évacuations** au plafond : salle de bain (hors de la retombée de la
  poutre), salle de lavage (près du séchoir suspendu) et **vestiaire, devant les casiers** (l'air humide des séchoirs et
  des habits de neige). Il amène de l'air frais aux chambres et au séjour. Deux sorties extérieures dans la solive de
  rive : emplacement à valider ; conduits posés avant le gypse.
- **Déshumidificateur** (30–50 pintes, hygrostat) à **drain permanent** (boyau vers le bac de lavage ou un drain de
  plancher), dans la salle de lavage près du chauffe-eau, hors du dégagement du panneau électrique ; on n'a jamais à le
  vider ; l'été, sous 50 % d'humidité.
- **Plancher chauffant électrique** (non dessiné) devant le bain, la toilette et la vanité (pieds nus), et dans l'aire
  de jeu du séjour entre la table basse et le banc (sous le tapis de laine) : le béton est à ≈ 15–18 °C l'hiver.

#### 7. La salle de bain à hauteur d'enfant (le mur du bain n'est pas touché)
- **Boîte-marchepied** de chêne massif (24 × 12 × 8 po, dessus antidérapant, poignées découpées) qui se range dans le
  vide sous la vanité suspendue (dessous à 12 po) : à 4 ans, on ne rejoint pas une vasque à ≈ 34 po.
- **Crochets à serviette** : 2 à **38 po** (un par garçon, serviette à sa couleur) et 1 à 64 po, sur le mur de la salle
  de lavage entre la vanité et la porte.
- **Porte coulissante** : amortisseurs de fermeture douce aux deux bouts du rail (doigts) et verrou à déverrouillage
  d'urgence de l'extérieur (un parent ouvre si un garçon s'enferme).
- **Mélangeur thermostatique** à la sortie du chauffe-eau : eau chaude limitée aux appareils (≈ 49 °C) pour le bain, la
  douche et la vanité d'un coup. Exigence et réglage à valider avec le plombier.

#### 8. Le linge des garçons (salle de lavage)
- Le bas du comptoir de pliage (le long du gym) est refait : **2 paniers de toile coulissants** de 16 po (un par
  garçon, plaquette vert forêt / marine), à la hauteur des garçons, entre le retour du comptoir et le bac encastré. Le
  parent plie et dépose ; chaque garçon vient chercher son panier et le rapporte vide.
- **Trieur à 2 sacs** (pâles / foncés) au bout du comptoir ; les 3 paniers d'osier du retour restent (serviettes,
  draps). **Loquet magnétique** invisible sur les portes sous le bac (produits ménagers) ; **capsules de détergent** dans
  un pot fermé sur la tablette du haut (66 po).
- La salle de lavage ne s'atteint qu'en traversant le gym : la bande du gym le long du lavage (y ≈ 120–157) doit rester
  **libre (≥ 36 po), sans poids au sol**, pour passer avec un panier (frontière avec le gym).

#### Plan et maquette
- **P-127** : casiers des garçons (armoires), grille encastrée (pointillé, « GRILLE »), banc à jouets (armoires),
  boîte de plancher, déshumidificateur (« DÉSH. ») et VRC suspendu (pointillé, « VRC »). Notes **note-SS-Q01 à Q03**
  ajoutées à `ss["notes"]` (insonorisation, VRC, plancher chauffant, veilleuses, eau chaude limitée) : le cartouche est
  déjà plein avec les 6 notes de SS-16 ; elles sont dans `donnees/maison.json` et paraîtront si les notes sont
  regroupées à l'intégration.
- **3D** : tout ce qui se voit est dessiné (casiers, séchoirs, bottes, habits, grille, bacs, veilleuses, habillages des
  colonnes, minuterie, poste de recharge, banc à jouets, store, guéridon et boîte de plancher, nuage de lattes, VRC,
  grilles d'évacuation, déshumidificateur, mélangeur, marchepied, crochets et serviettes, paniers de linge). L'encastré
  du séjour qui tombait au-dessus du nuage devient une lumière intégrée au nuage. L'insonorisation, le sol chauffant,
  les portes pleines et le limiteur d'eau chaude ne se voient pas : notes seulement.

#### Frontières avec les autres zones
- Cloison y = 230 (vestiaire / chambre 2) : les casiers s'y adossent (x 281–319) et les prises des séchoirs y sont ; si
  la porte de la chambre 2 (x 246–278) se déplace vers l'est, les casiers se décalent d'autant.
- Cloisons y = 230 et portes des 2 chambres : laine acoustique, portes à âme pleine, veilleuses V1 et V3 côté hall et
  vestiaire — à coordonner avec les chambres.
- Plafond insonorisé et conduits du VRC : tout le sous-sol, y compris chambres, gym et dessous de l'escalier ;
  diffuseurs d'air frais des chambres à placer par leurs auteurs.
- Gym : passage libre ≥ 36 po vers la salle de lavage. Séjour : galerie de photos, dessous de l'escalier et bande
  derrière le divan (x 272–302) non touchés.

#### À vérifier sur place et à valider
- **Porte de côté** : est-ce bien la porte de tous les jours des garçons l'hiver ? Côté des pentures présumé (y = 162).
  Sinon, le seuil à neige se déplace au pied de l'escalier.
- **Armoire à manteaux verte** (gardée) : son dessus à 88 po touche la retombée de la poutre arrière (dessous ≈ 86 po)
  sur ses 4 premiers po — à vérifier (sinon abaisser son dessus à 85 po).
- **Plafond insonorisé** : il descend d'≈ 1¾ po ; vérifier le boîtier de la toile au-dessus du cadrage de la fenêtre
  (≈ 2 po en SS-16) et la hauteur libre sous les poutres avec la chape de l'option B (≈ 82½ po).
- **Option A ou B du plancher** : la grille encastrée, le sol chauffant et la boîte de plancher supposent la chape (B).
- **Électricité** : capacité du panneau (séchoirs, 3 zones de sol chauffant, VRC, déshumidificateur) ; prises
  inviolables (à obturateurs) partout ; DDFT près de l'eau (bacs, salle de bain, lavage, casiers) — électricien.
- **VRC** : sorties extérieures, débits, exigence de ventilation mécanique ; **séparation coupe-feu et acoustique**
  entre le sous-sol et le rez-de-chaussée (deux logements ?).
- **Eau chaude** : température maximale aux appareils et type de mélangeur — plombier.
- Tous ces points de code et de sécurité : **à valider avec la Ville de Baie-Comeau et un professionnel** ; aucune
  conformité n'est affirmée ici.
