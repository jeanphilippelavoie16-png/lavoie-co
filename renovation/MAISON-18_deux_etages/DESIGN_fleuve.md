# MAISON-18 — Le fleuve Saint-Laurent et le traversier F.-A.-Gauthier

Demande du client, mot pour mot : « je veux aussi que tu ajoutes le F.-A.-Gauthier sur le fleuve au loin » ; « fais le
traversier qui avance pour vrai ».

Données : `fleuve.py` (module de la liste `FINALE` de `scene_3d.py`). Moteur : « Le lointain et les objets animés de
l'extérieur » dans `renovation/README.md`. Arrêt de visite : **Le fleuve et le traversier** (section Extérieur, sur le haut du terrain
avant, à gauche du perron, regard vers le fleuve ; pas sur le perron même : le visiteur qui cogne s'y déclenche).

## Ce qu'on voit
Du terrain avant (du perron, du bord de la rue, et par les fenêtres avant), au-delà de la rue : les maisons d'en face, plus basses que la rue
(le terrain descend), la basse-ville qui descend jusqu'à un talus de roche, puis le fleuve bleu foncé jusqu'à l'horizon,
avec un léger reflet du ciel qui pâlit vers le large. L'autre rive (environ 50 km) est hors de vue. Le traversier passe au
large, de droite à gauche, avec sa vague d'étrave et son sillage, fait demi-tour hors du champ et revient plus loin.

## Le site (hypothèses, à valider sur place)
| | Valeur retenue | Pourquoi |
|---|---|---|
| Surface du fleuve | 45 m sous le plancher du sous-sol | la ville descend vers le fleuve ; le haut des pentes de Baie-Comeau est à 30-60 m |
| Rive | 450 m devant la façade, droite, parallèle à la rue | « quelques centaines de mètres » |
| Rue | devant le lot (chaussée de 9 m, trottoirs), au niveau du bas de l'allée (-15 po) | relevé du lot : l'allée arrive à -15 |
| Maisons d'en face | en bas d'un talus, façades à 42 m de la nôtre, plancher 5 m plus bas que la rue | on voit le fleuve « par-dessus les toits d'en face » |
| Basse-ville | pente concave (plus raide en haut) jusqu'à un talus de roche de 3 m ; rues parallèles au fleuve tous les 50 m | on voit tout jusqu'à la rive |

Le fleuve est droit devant (vers -y). Si l'orientation réelle diffère, il suffit de faire pivoter la rive et le trajet.

## Le traversier F.-A.-Gauthier (Société des traversiers du Québec)
Sources :
- STQ, fiche du navire (traversiers.com, « MV F.-A.-Gauthier ») : 133,3 m, 22,4 m de large, tirant d'eau 5,55 m, 20 nœuds,
  800 passagers, 180 véhicules, embarquement avant et arrière, GNL et diesel-électrique (4 Wärtsilä 12V34DF), Fincantieri
  Castellammare di Stabia, 2014 ;
- Fincantieri (communiqués 2013-2014) et Deltamarin (fiche de référence) : 133,2 m hors tout, 22,4 m, 5,6 m, 15 901 tjb,
  classe glace 1A, étrave et poupe brise-glace ;
- Wikipédia (fr) : 120 m entre perpendiculaires, creux 8 m, 8 ponts (1-2 machines, 3-5 véhicules, 6 passagers, 7
  promenade, 8 passerelle), 17 à 20 nœuds ;
- photos (Radio-Canada 2020 au quai ; mise à l'eau à Castellammare, 2014) : silhouette et couleurs.

| Partie | Dans la maquette (à l'échelle réelle) |
|---|---|
| Coque | 133,2 m × 22,4 m ; étrave ronde brise-glace, tableau arrière ; **bleu roi** (`#1f4896`) de la flottaison à 7 m (9,6 m à l'avant, où le bleu remonte), **blanche** jusqu'au pont 6 (13,6 m), bande de hublots des ponts des véhicules |
| Superstructure | blanche : pont 6 (13,6 à 16,4 m) et pont 7 (16,4 à 19,2 m), avant arrondi, bandes de fenêtres sombres |
| Passerelle | pont 8 à l'avant, sur toute la largeur (ailes comprises), vitrée devant et sur les côtés, toit, mât blanc, radar qui tourne |
| Cheminée | à l'arrière : caisson blanc, chapeau bleu marine, quatre tuyaux (quatre moteurs) ; **sans logo** |
| Embarcations | quatre, orange, au pont 7 |
| Rampes | rampe arrière relevée contre le tableau (gris foncé) ; la porte d'étrave est fondue dans l'étrave (invisible de loin) |
| Nom | « F.-A.-GAUTHIER » en lettres blanches de 1,4 m sur la coque bleue, vers l'arrière, des deux bords |

Rien sous la flottaison n'est modélisé (le fleuve ne cache rien : il est dessiné sous tout le reste).

## Vitesse et trajet
- Vitesse réelle demandée : 15 nœuds (7,7 m/s). **Accélérée ×3** : 23,1 m/s à l'écran (≈ 45 nœuds), pour qu'on le voie
  avancer en quelques secondes. À 2 km, il se déplace d'environ 0,7° par seconde : une dizaine de pixels par seconde sur
  la tablette, 5 à 6° en 10 s (les trois images de la planche). À vitesse réelle, ce serait 3 fois moins.
- Trajet en boucle : aller à **2 km** de la façade (de droite à gauche vu du terrain avant), demi-tour à 3 km de côté (hors du champ),
  retour à **2,7 km**, demi-tour de l'autre côté. Un tour : environ 12 min 40 s ; vu de l'arrêt, il est dans le champ un peu plus
  de la moitié du temps. Au chargement, il est déjà en vue (à 1,2 km à droite du regard vers le fleuve).
- À 2 km, il paraît comme en vrai : environ 3,8° de long (une cinquantaine de pixels sur la tablette) et une dizaine de
  pixels de haut ; deux doigts zooment (champ de 35°) pour mieux le voir.

## Rendu (tablette)
Le lot est dessiné dans les 200 m de la caméra sous une brume de 40 à 180 m ; le fleuve va à l'horizon. Le moteur dessine
donc un **plan lointain** à part, derrière tout le reste, avec sa propre brume de distance (voir le README) : l'eau (un seul
maillage, un petit programme : couleur selon la distance, reflet du ciel plus fort en rasant l'eau, longues ondulations de
300 m qui ne scintillent pas), la terre, quelque 700 maisons et 800 arbres (un seul maillage, couleurs par sommet), le
traversier (deux maillages et son nom). Le traversier ne demande des images que s'il est dans le champ (dehors, ou par une
fenêtre de l'étage) : **10 images par seconde au plus**, aucune quand la page est cachée. Page : environ +0,5 Mo.

## Simplifié
- Formes simples et couleurs unies, sans logo de la STQ ; pas de détails de pont (bastingages, portes, antennes).
- Eau plane sans vagues ni écume ; pas de courbure de la Terre (l'horizon est à 0,04° sous l'horizontale au lieu de 0,2°).
- Rive droite ; basse-ville faite au hasard (graine fixe : toujours la même) : bungalows et cottages génériques, épinettes et
  feuillus ; les maisons d'en face ne sont pas relevées.
- Le vrai traversier traverse vers Matane (perpendiculaire à la rive) ; ici, il passe parallèlement pour traverser le champ,
  comme demandé.
- Même soleil que le reste de la visite : vers le fleuve, on regarde vers le soleil (le côté du navire qu'on voit est à
  contre-jour, comme sur une rive sud ensoleillée).
- La brume du lot (40 à 180 m) reste celle du moteur sur les côtés : en regardant le long de la rue, le terrain des voisins
  pâlit plus vite que la basse-ville.
