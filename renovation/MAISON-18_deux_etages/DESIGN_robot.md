# Aspirateur robot au rez-de-chaussée (module `rdc_robot.py`)

## Demande du client (2026-11-02)
« Je veux qu'il y ait une balayeuse robot automatique qui se promène en haut dans la maison qui est en train de faire du ménage. »

## Ce qu'on voit dans la visite 3D
- Un aspirateur robot rond de 13,8 po (35 cm) × 3,6 po (9,2 cm) : jupe grise, dessus noir mat, tourelle laser, pare-chocs
  avant noir, brosse latérale qui tourne, voyant vert qui clignote.
- Il sort de son **garage, sous le garde-manger**, nettoie en allers-retours parallèles, rentre au garage, s'arrête 20 s
  et recommence. Un tour dure **≈ 5,6 min** (≈ 272 pi à 30 cm/s, virages sur place).
- Nouvel arrêt de visite **« Aspirateur robot »**, juste après « Cuisine — rangement » : on est au coin de la cuisine
  et du salon, on regarde vers la salle à manger et le garde-manger. Le robot passe dans ce champ environ 40 % du temps.
- Bouton **« Arrêter le robot » / « Repartir le robot »** au rez-de-chaussée. Toucher le robot fait la même chose.
- Au chargement de la page, le robot a 6 s d'avance : il sort de son garage.

## La base : un garage dans le socle du garde-manger
Le garde-manger encastré (`rdc_cuisine.py`, dans l'ancien coin ordi) est neuf. On en profite pour ajouter le garage
pendant sa fabrication :
- **Ouverture de 17 po × 4½ po** au centre du coup de pied (le socle passe de 4 à 4½ po). La base est collée au fond,
  contre le mur. Le robot se range au complet sous le caisson et ne dépasse pas.
- **Discret** : on ne voit qu'une fente noire dans le socle noir. On ne voit pas la base de l'entrée ni du salon.
- **Logique** : le garage est au centre des zones à nettoyer, à côté de la cuisine (les miettes). Il est dans le
  renfoncement entre le poteau et le mur des G.R. : pas dans un passage, ni devant une porte (la porte de la G.R. 3
  est plus loin, à y ≈ 260–288).
- **Prise** : une prise 15 A dans le caisson du bas du garde-manger, sur la cloison du fond (x = 146). Le fil de la
  base passe par un passe-fil dans le fond du socle. Il n'y a pas de fil au sol.
- **À valider avec le modèle choisi.** Les fabricants demandent souvent de la place libre de chaque côté de la base.
  Dans le garage, il reste 1,6 po de chaque côté. Il faut essayer le robot avec la base dans l'ouverture avant de
  poser le socle.
  **Option B** si le modèle refuse la niche : la base est posée au sol devant le socle, dans le même renfoncement.
  Elle dépasse alors d'environ 4 po et le robot reste visible quand il est rangé.

## Le trajet (calculé, pas dessiné à la main)
Le trajet est calculé sur les vraies emprises de la scène RDC de la maquette, avec une grille au ½ po. Voici ce qui
compte comme obstacle :
- les murs, les poteaux, le garde-corps de verre et la trémie de l'escalier ;
- les portes, dans leur état de départ ;
- tout ce qui descend sous 4 po : pieds de chaises et de tabourets, sofa (socle à 3 po), îlot, poubelles, pot de
  la plante.

Le centre du robot reste toujours à au moins 7,9 po de ces obstacles (rayon de 6,9 po + 1 po de jeu). Un tour se fait
comme suit :
1. Il sort du garage vers la salle à manger.
2. **Zone 1, le passage** dégagement → cuisine → salon : 3 allers-retours sur toute la largeur de la maison, entre les
   deux poteaux et l'îlot.
3. **Zone 2, le salon** : 10 allers-retours de l'avant vers l'arrière. Il contourne le sofa en L et le pot de la plante.
4. **Zone 3, l'allée entre la table et l'îlot** : 6 allers-retours, en longeant les chaises et les tabourets.
5. Il rentre au garage, s'arrête 20 s, puis recommence.

Réglages : écart de 12½ po entre deux passes (le robot fait 13,8 po, donc un peu de chevauchement), 11,8 po/s
(30 cm/s, vitesse de nettoyage courante), virages de 120°/s. Points, longueur et durée : `TRAJET` dans `rdc_robot.py`.

Volontairement hors du tour de démonstration :
- sous la table, entre les pattes de chaises ;
- l'entrée, à cause de la trémie de l'escalier ;
- les chambres, le bureau et la salle de bain.

Un vrai robot les fait : on choisit les pièces dans l'application.

Limite de la maquette : le robot suit son trajet et n'évite rien. Si on déplace un meuble de ces zones, il faut refaire
le trajet. À la génération, `_verifier()` avertit si un segment frôle un meuble.

## Modèle type (aucune marque imposée)
- **Navigation laser** (LiDAR, la tourelle sur le dessus) : il fait la carte de l'étage, on y met des zones interdites
  et on choisit les pièces et les horaires dans l'application. Par exemple, le faire passer quand la famille est
  partie.
- **Hauteur totale de 3,8 po (9,7 cm) au plus**, tourelle comprise, pour entrer sous le socle de 4½ po. Diamètre
  d'environ 35 cm.
- **Brosse principale en caoutchouc** (moins de cheveux enroulés), une brosse latérale, franchissement de seuils d'environ
  2 cm.
- **Sans station auto-vidante.** Ces stations font 40 à 45 cm de haut et n'entrent pas dans le socle. On vide le bac à la
  main tous les un ou deux passages. Une station auto-vidante demanderait une niche dans le bas du garde-manger, ce qui
  coûte plus cher (« exagère pas »).
- **Vadrouille facultative** : pas nécessaire pour l'usage décrit.

## Coûts (fourchette, taxes en sus)
| Poste | Fourchette | Base |
|---|---|---|
| Robot laser d'entrée de gamme, sans station | ≈ 400 à 650 $ CA | prix américains de ≈ 300 à 330 $ US (Best Buy É.-U. : Roborock Q7 Max à 299,99 $ US ; Roborock Q10 S5+ affiché à 329,99 $ US). Conversion et prix canadiens à vérifier en magasin |
| Garage dans le socle (ouverture, socle de 4½ po, passe-fil) | ≈ 150 à 400 $ | **estimation** : à faire chiffrer par l'ébéniste avec le garde-manger |
| Prise 15 A dans le garde-manger | ≈ 150 à 300 $ | **estimation** : à faire chiffrer par l'électricien |
| **Total** | **≈ 700 à 1 350 $** | |

Pour situer le marché : Protégez-Vous a testé 29 aspirateurs robots vendus au Québec, jusqu'à 1 995 $ (prix relevés en
août 2025). Le haut de cette fourchette correspond aux robots avec station auto-vidante et vadrouille, que l'on ne retient
pas ici.

Sources :
- [Slickdeals — Roborock Q7 Max à 299,99 $ US chez Best Buy (É.-U.)](https://slickdeals.net/f/17478843-roborock-q7-max-4200pa-robot-vacuum-mop-cleaner-white-or-black-300-free-shipping)
- [Smart Home Compared — Roborock Q10 S5+ affiché à 329,99 $ US](https://smarthomecompared.com/robot-vacuums/eufy-l60-with-self-empty-station-vs-roborock-q10-s5-plus)
- [Protégez-Vous — Comment nous avons testé les aspirateurs robots](https://www.protegez-vous.ca/electromenagers/aspirateurs-robots/comment-nous-avons-teste-les-aspirateurs-robots)
  (page bloquée à la lecture automatique : résumé du moteur de recherche)

## À prévoir
- **Prise** 15 A dans le caisson du bas du garde-manger, à commander à l'électricien en même temps que le déplacement
  du thermostat (déjà prévu au garde-manger).
- **Seuils bas.** Les réducteurs d'érable entre le chêne et l'ardoise font environ 0,3 po (8 mm) : le robot passe sans
  problème. Les seuils des portes doivent rester sous ¾ po (environ 2 cm), qui est la limite courante de ces robots.
  La porte arrière et le coin café ne sont pas sur le trajet.
- **Tapis.** Il n'y a aucun tapis sur le trajet dans la maquette. Si on en ajoute un au salon, choisir un poil ras de
  ¾ po au plus, sans franges. Les tapis de bain et les tapis épais : zone interdite dans l'application.
- **Escalier.** En plus des capteurs anti-chute du robot, mettre une zone interdite dans l'application au haut de la
  volée : le garde-corps de verre est ouvert à l'arrivée de l'escalier.
- **Ardoise noire de la cuisine.** Sur certains robots, les capteurs anti-chute prennent un sol très foncé pour un vide
  et le robot refuse d'y aller. Vérifier les avis du modèle sur les sols noirs avant l'achat.
- **Les garçons de 4 et 6 ans.** Ramasser les Lego et les petits jouets avant le passage (le robot les avale ou s'y
  bloque). Les horaires d'école sont le meilleur moment pour le faire passer.
- **Fils au sol** (télé, chargeurs) : les relever ou mettre une zone interdite.
- **Wi-Fi** au rez-de-chaussée pour l'application.

## Plan P-130
Le garde-manger (`elem-RDC-K-GM`) mentionne le garage du robot et sa prise. Rien d'autre ne change au plan.
