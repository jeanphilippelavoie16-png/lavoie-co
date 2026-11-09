# CH-01 — La chambre des garçons : état actuel et coin jeu proposé

Projet **à part** : la chambre avant du rez-de-chaussée (les deux garçons, 4 et 6 ans) toute seule, avec sa garde-robe,
dans la maison telle qu'elle est aujourd'hui. Il ne dépend pas de MAISON-18 (pas de bureau assis-debout) et ne touche à
aucun autre projet. Il sert de test pour refaire bientôt la vraie chambre et l'optimiser.

- Plan : `png/P-131_chambre-garcons.png` (feuille P-131, 1/4" = 1'-0", la plus grande échelle du générateur).
- Maquette : `3d/visite.html` (6 arrêts, départ à la porte).
- Générer : `python3 renovation/outils/construire_projet.py renovation/CH-01_chambre_garcons` puis
  `python3 renovation/outils/generer_3d.py renovation/CH-01_chambre_garcons`.
- Plan final (à lancer avec le vrai lien, après publication) :
  `python3 renovation/outils/plan_final.py renovation/CH-01_chambre_garcons --lien <lien de la visite>`.

## Les demandes du client (2026-11-09), mot pour mot
> « Je veux que tu modélises la chambre en haut du coin avant comme elle est présentement. Je veux seulement garder le lit
> superposé et le meuble blanc et que tu me proposes un coin jeu pour les gars pour jouer Lego, bac de jeu et place pour
> mettre les livres. »

> « Le bureau assis debout reste pas, c'est un test pour refaire la chambre bientôt et l'optimiser. Fais la chambre tout seul
> dans son monde à elle pas dans l'autre plan. »

## Comment le projet est construit
- `modifs.py` : copie de la base R0 + relevé photo RDC-01 (`base_rdc01_modifs.py`, copie telle quelle de
  `RDC-01_etat_actuel/modifs.py`), puis on ne garde **qu'un niveau** et, de ce niveau, la chambre (`piece-RDC-CH2`) et sa
  garde-robe (`piece-RDC-GRA`). Les murs qui les bordent sont coupés à leur contour (leur épaisseur reste) ; le reste de la
  maison (autres pièces, sous-sol, extérieur) n'existe pas dans ce projet.
- `geometrie.py` : tous les repères et dimensions (une seule source pour le plan et la maquette).
- `scene_3d.py` : matériaux, peinture, mobilier, lumières, arrêts de visite.
- Le générateur de plans n'est pas modifié. Le moteur 3D a reçu trois clés **facultatives et génériques** (petits carreaux
  de fenêtre, texte peint ou gravé, emprise d'une seule pièce), documentées dans `renovation/README.md` et dans les
  docstrings de `generer_3d.py` ; MAISON-18 se génère à l'identique.

## Ce qui vient des photos, ce qui est estimé
Les 12 photos (`renovation/prive/chambre_avant/`, gardées hors du dépôt ; aucune n'est reproduite dans la page) ont été
regardées une à une (recadrées au besoin). Photo 11 : depuis le corridor ; 12 : depuis l'intérieur près de la porte ;
10 : la fenêtre de face ; 01 à 03 et 09 : le coin avant gauche ; 04 et 05 : la commode et la garde-robe ; 06 à 08 : les lits
et le mur vert.

| Élément | Source | Retenu |
|---|---|---|
| Murs, fenêtre (largeur 6'-3", position), portes (2'-6") | plan R0 (LU) et RDC-01 | intérieur 11'-1¾" × 10'-9¾" (≈ 124 pi² avec le renfoncement de la porte) |
| Profondeur de la chambre | RDC-01 (cloison de la salle de bain reportée d'après ses photos) | 129¾ po : **à mesurer** |
| Fenêtre : 3 châssis égaux, cadre blanc, manivelle sur celui de droite vu de l'intérieur | photos 02, 10, 12 | modélisée |
| Bande de petits carreaux (2 rangs × 3 colonnes) en haut de chaque châssis | photos 02, 10 | ≈ 9½ po de haut (ESTIMÉ) |
| Allège ≈ 37½ po, tête ≈ 80 po | vidéo DAG (MAISON-18) | gardées ; la photo 12 laisse voir plus de mur au-dessus des stores que ne le donne un plafond de 96 po : **plafond et tête à mesurer** |
| Chambranle plat de pin teint, coins d'onglet ; deux caissons noirs de stores | photos 02, 10, 12 | chambranle ≈ 4½ po (4 à 5 sur les photos) |
| Portes de pin teint à panneaux horizontaux, bouton rond et pentures noirs | photos 04, 05, 11, 12 | porte de la chambre : charnière côté mur de droite (photo 11) ; garde-robe : charnière côté fenêtre, bouton côté porte (photos 05, 06) |
| Plinthes chauffantes blanches (≈ 3 × 7½ po) | photos 01 à 03, 08, 09, 12 | sous la fenêtre ≈ 96 po (x 26 → 122) ; au mur vert ≈ 72 po (y 22 → 94). **Bouts cachés par les meubles : longueurs estimées** |
| Mur d'accent vert forêt grisé (mur gauche, extérieur) ; murs blanc chaud ; plancher d'érable ; plafond blanc | photos | vert ≈ #465E52, à comparer au nuancier |
| Suspension cage de fil noir à chapeau de bois, au centre | photos 06 à 10 | modélisée |
| Enseignes « Pierre-Alexis » (planches foncées, lettres pâles) et « Louis-Charles » (planches pâles, lettres foncées), panache d'orignal | photos 03, 07 à 09 | ≈ 38 × 13 po et 40 × 13 po ; panache ≈ 40 po ; noms en texture de canevas (écriture liée de l'appareil) |
| Lits superposés simple sur simple, panneaux blancs, montants de bois naturel, échelle inclinée | photos 05 à 09, 12 | ≈ 80½ × 43 × 63 po (ESTIMÉ), le long du mur arrière, tête au mur vert |
| Commode blanche basse (2 colonnes × 3 tiroirs à poignées encastrées, pattes grises) | photos 04, 05, 10 à 12 | ≈ 48 × 16 × 27 po (ESTIMÉ), mur de droite entre la fenêtre et la garde-robe |
| Plafond | présumé | 96 po (8 pi), comme RDC-01 : **à mesurer** |

Non modélisés : les petits animaux dessinés sur les murs blancs (autocollants), le thermostat et les prises (non visibles).

## Ce qu'on garde, ce qu'on enlève
- **Gardés** (à leur place réelle) : les lits superposés et la commode blanche. Le coin jeu ne gagne pas assez à les
  déplacer : les lits ne peuvent aller ailleurs sans bloquer une plinthe chauffante, la fenêtre ou la porte, et la commode
  est déjà au seul endroit libre du mur de droite.
- **Gardés aussi** (c'est la pièce) : fenêtre, portes, plinthes chauffantes, mur vert et son décor, suspension.
- **Enlevés** : fauteuil inclinable, petite table et chaises, présentoir à livres blanc, tablettes flottantes de jeux et
  cadres, toise, jouets et livres au sol (l'aspirateur robot et le tiroir de plastique au pied des lits aussi).

## Le coin jeu proposé : « l'atelier des bâtisseurs »
La pièce n'a presque pas de mur libre : plinthes chauffantes sous la fenêtre et au mur vert, lits au mur arrière, commode,
garde-robe et porte au mur de droite. Le parti : **trois petits postes au bon endroit plutôt qu'un gros meuble**, le
plancher du centre gardé libre pour jouer, et la garde-robe qui devient le vrai rangement des jeux.

| Poste | Où | Dimensions | Pourquoi |
|---|---|---|---|
| **Table à Lego** en chêne, rebord de ¾ po tout autour (les pièces ne roulent pas en bas), plaque de construction, deux bacs de tri ; piètement noir mat ; **deux tabourets** de chêne (assise à 12 po, coussins sauge et terracotta) | coin avant gauche, sous les enseignes, à côté de la fenêtre (x 26 → 56, y 27½ → 51½) | 30 × 24 po, dessus à 20 po (bonne hauteur à 4 et 6 ans) | la lumière du jour, l'ancien coin de jeu des gars ; ≈ 12½ po de la plinthe du mur vert et ≈ 14 po de celle de la fenêtre (hypothèse de travail, à valider) ; piètement ouvert, rien ne s'appuie sur une plinthe |
| **Livres de face** : deux rebords de chêne à lèvre de 1½ po | au mur de droite, au-dessus de la commode, à 34 et 45½ po du plancher | 48 × 4 po chacun, ≈ 8 à 10 albums de face | les couvertures à la hauteur des gars ; le dessus de la commode sert de comptoir pour poser le livre choisi. Les autres albums dorment dans la garde-robe : **rotation** chaque semaine (les livres de face changent, les gars les redécouvrent) |
| **Tour de 3 bacs** étiquetés (pictogramme + mot : toutous, autos, dinos), veilleuse dessus | au pied des lits, à côté de la porte (x 92 → 109½) | 17½ × 15 × 39 po, ancrée au mur | on ramasse en entrant ; elle laisse ≈ 30 po de passage avec la porte de la chambre ouverte |
| **Tapis rond** de laine sable bordé de sauge | centre (à l'écart du pied de l'échelle) | 56 po | le plancher de jeu (Lego, autos) ; le centre reste libre |
| **Garde-robe aménagée** (voir plus bas) | garde-robe | 24½ × 75½ po | le vrai rangement : bacs de jeu étiquetés, Lego triés par couleur, constructions exposées, vêtements à leur hauteur |

### La garde-robe aménagée
- **Face à la porte** : étagère de chêne de 28 po (16 po de profond) avec **6 bacs de feutre étiquetés** à 2, 14 et 26 po
  (trains, casse-têtes, animaux, bricolage, costumes, jeux) ; dessus, **6 tiroirs à Lego triés par couleur** (pastille de
  couleur sur chaque tiroir : rouge, bleu, jaune, vert, orange, noir) ; au-dessus, une **tablette des constructions** à 56 po
  (les modèles finis s'exposent, hors de portée du petit frère).
- **Aile de gauche** : penderie double, tringle basse à **42 po** (leurs vêtements, qu'ils prennent seuls) et tringle haute à
  78 po (vestes, grandeur suivante) ; pantoufles au sol.
- **Aile de droite** : deux tablettes (30 et 52 po) de bacs saisonniers, gros bac « hiver » au sol (tuques, mitaines).
- Tablette haute à 83 po sur toute la longueur (rangement des parents), **ruban DEL** sous la tablette.
- La porte de pin est gardée (charnière côté fenêtre) : ouverte, elle ne gêne ni la commode ni les rebords à livres.

### Circulation et dégagements (en pouces, ESTIMÉS)
- Porte de la chambre → lits et échelle : ≈ 31 po entre les tabourets et les lits ; ≈ 30 po entre la tour de bacs et la porte
  ouverte.
- Pied de l'échelle (y ≈ 74½) : rien devant ni sur le côté (le tapis commence à côté, il ne passe pas sous l'échelle).
- Tiroirs de la commode : ils sortent sur le tapis, rien devant ; arc de la porte de la garde-robe libre.
- Fenêtre : rien devant plus haut que l'allège ; plinthes chauffantes : aucun meuble devant, aucun rangement fermé dessus.

## Options
- **A — proposée (sans travaux)** : ce qui est dessiné. Meubles du commerce ou faits sur mesure, garde-robe aménagée avec un
  système modulaire.
- **B — si on refait la chambre au complet** : agrandir l'ouverture de la garde-robe à environ 60 po (cloison présumée non
  porteuse, à vérifier ; linteau, gypse, chambranles, deux portes de pin pliantes ou coulissantes) et y mettre **la commode**
  sous une penderie haute. Le mur de droite se libère sur environ 4 pi : on y met un vrai meuble bas de bacs avec la table à
  Lego dessus, et les livres de face juste au-dessus. Plus de rangement accessible, mais des travaux (voir coûts).
- Variante à considérer dans les deux cas : une porte de garde-robe pliante au lieu de la porte battante (plus d'arc dans la
  chambre), en pin teint pour garder le style.

## Points à vérifier sur place
1. **Plinthes chauffantes** : longueur et bouts réels ; dégagement à garder devant et au-dessus (table, tabourets, tapis,
   rideaux) **à faire valider avec le fabricant de la plinthe et un électricien** ; aucun chiffre de ce document n'est
   une norme. Le pied des lits arrive près du bout de la plinthe du mur vert (situation existante) : à faire regarder aussi.
2. **Ancrage** : commode, tour de bacs et étagère de la garde-robe vissées au mur (courroie ou équerre anti-basculement,
   dans un montant).
3. **Mesures au ruban** : largeur et profondeur de la chambre ; profondeur du renfoncement de la porte ; hauteur du plafond ;
   allège et tête de la fenêtre ; position et largeur de la porte de la garde-robe ; dimensions intérieures de la
   garde-robe ; lits superposés (longueur, largeur, hauteur des garde-corps, pied de l'échelle) ; commode.
4. Prises de courant et interrupteur (veilleuses, ruban DEL de la garde-robe : une prise ou un transformateur à prévoir).
5. Couleur du mur vert : comparer au nuancier avant de retoucher.
6. Option B : cloison de la garde-robe porteuse ou non, et ce qui passe dedans (fils), **à valider avec un professionnel**.

## Ordre de grandeur des coûts (option A)
Estimation, sans source de prix vérifiée (fourchettes 2026, taxes en sus, à confirmer en magasin ou en soumission) :

| Poste | Du commerce, posé soi-même | Sur mesure, posé |
|---|---|---|
| Table à Lego de chêne et 2 tabourets | 250 – 500 $ | 600 – 1 100 $ |
| 2 rebords à livres de chêne (48 po) | 80 – 200 $ | 150 – 350 $ |
| Tour de 3 bacs et ses bacs | 150 – 300 $ | 300 – 600 $ |
| Garde-robe : étagère, 6 bacs, 6 tiroirs, tablettes, 2 tringles, DEL | 500 – 1 100 $ | 1 500 – 2 800 $ |
| Tapis rond de laine 56 po | 150 – 400 $ | — |
| Ancrages, étiquettes, petites fournitures | 30 – 60 $ | — |
| **Total** | **≈ 1 200 – 2 600 $** | **≈ 2 700 – 5 300 $** |

Option B en plus : ≈ 2 000 – 4 500 $ (ouverture élargie, linteau, gypse, peinture, chambranles, portes de pin), estimation.

## Maquette 3D
Arrêts, dans l'ordre : **Depuis la porte** (comme la photo 11) ; **Le coin des bâtisseurs (Lego)** ; **Les livres de face** ;
**Les lits et le mur vert** ; **La garde-robe aménagée** (touche la porte pour l'ouvrir) ; **De la fenêtre vers la porte**
(comme la photo 06). Les deux portes s'ouvrent et se ferment au toucher. Dehors, par la fenêtre : ciel et terrain simples
(l'extérieur de MAISON-18 n'est pas recopié) ; par la porte de la chambre, un bout de corridor neutre (décor).

Ajouts au moteur pour ce projet (facultatifs, génériques, documentés dans `renovation/README.md`) :
- `SCENE["fenetres"][id]["carreaux"]` : la bande de petits carreaux de la fenêtre ;
- forme `"texte"` du mobilier : les noms des enseignes et les étiquettes des bacs ;
- `SCENE["bornes"]` : l'emprise d'une seule pièce (la garde-robe dépasse le mur de façade coupé).

## Ce qui reste imparfait
- Toutes les dimensions de l'existant sont estimées sur des photos grand-angle (précision de quelques pouces) ; les
  proportions des photos 08 et 12 ne s'accordent pas parfaitement avec un plafond de 96 po (à mesurer).
- Les noms des enseignes prennent l'écriture liée de l'appareil (Snell Roundhand sur iPad et iPhone) : la lettre ne sera
  pas exactement celle des planches gravées.
- Les panneaux du lit sont à coins carrés (les vrais ont des coins arrondis) ; le panache est stylisé.
- La porte de la garde-robe part fermée, comme sur les photos : il faut la toucher pour voir l'aménagement.
- Le plan ne montre pas le tapis ni les tringles de la garde-robe ; les rebords à livres sont en tirets (au mur, au-dessus
  de la commode).
