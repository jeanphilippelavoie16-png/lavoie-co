# CH-01 — La chambre des garçons : rangement, coin jeu et thème (version 2)

Projet **à part** : la chambre avant du rez-de-chaussée (les deux garçons, 4 et 6 ans) toute seule, avec sa garde-robe,
dans la maison telle qu'elle est aujourd'hui. Il ne dépend pas de MAISON-18 (pas de bureau assis-debout) et ne touche à
aucun autre projet. Il sert de test pour refaire bientôt la vraie chambre et l'optimiser.

- Plan : `png/P-131_chambre-garcons.png` (feuille P-131, révision B, 1/4" = 1'-0").
- Maquette : `3d/visite.html` (7 arrêts, départ à la porte ; les bacs sous le lit sortent quand on les touche).
- Murale : `murale/murale_camp_fiche.png` (fiche pour le peintre : murale, enseignes, plinthe, lit, palette) ;
  `murale/murale_camp.png` (l'image peinte sur le mur dans la maquette). Les deux sont dessinées par `murale.py`.
- Générer : `python3 renovation/outils/construire_projet.py renovation/CH-01_chambre_garcons` puis
  `python3 renovation/outils/generer_3d.py renovation/CH-01_chambre_garcons` (la murale se redessine toute seule).
- Plan final (à relancer avec le vrai lien, après publication ; celui du dossier est encore celui de la version 1) :
  `python3 renovation/outils/plan_final.py renovation/CH-01_chambre_garcons --lien <lien de la visite>`.

## Version 2 (révision B, 2026-11-09)

### La réponse du client, mot pour mot
> « Non mais je veux pas nécessairement de table, là tu m'as donné de quoi de prémâché. Je veux de l'espace de rangement et
> un coin jeu. Je veux aussi changer les couleurs et mettre un thème plus genre enfant [4 et 6] ans. »

> « enfant mais genre moderne, pas genre Avengers... mais que ça reste enfant, cool mais moderne »

Lecture : la version 1 décidait trop de choses à sa place (un meuble pour une seule activité). Il veut **beaucoup de
rangement** (c'est la priorité), un **coin jeu ouvert** au plancher, **plus de vert forêt** (trop sombre, aussi sur
téléphone) et un **thème d'enfant moderne**, graphique, sans héros ni personnages sous licence, qui vieillit bien jusqu'à
10-12 ans. Il a demandé expressément des **bacs roulants sous le lit**.

### Ce qui change, et pourquoi
| Version 1 | Version 2 | Pourquoi |
|---|---|---|
| Table à Lego de chêne et 2 tabourets sous les enseignes | **Enlevés** : le coin de la fenêtre redevient du plancher libre | « pas nécessairement de table » ; on joue au sol |
| Tapis rond de 56 po | **Grand tapis plat 4½ × 7 pi** (54 × 84 po), champ sable uni, bordure terracotta, 2 coussins de sol | un vrai coin jeu ouvert : Lego, autos et figurines au plancher |
| Tour de 3 bacs à la porte | **Tour aux albums** au même coin (≈ 60 à 70 albums debout + bac à toutous) | il a « beaucoup d'albums » ; les bacs de jouets vont sous le lit |
| Rien sous les lits | **3 bacs roulants bas** (Lego, autos, dinos) qui sortent vers le tapis | demandé expressément ; ≈ 100 L à leur portée |
| Mur au-dessus de la commode : 2 rebords à livres | Rebords gardés (livres de face, z 33 et 44½) + **armoires fermées au-dessus** (parents) + **tablette haute** de chêne et 6 boîtes | le volume du haut des murs, hors de portée des petits |
| — | **3 patères** à leur hauteur entre la garde-robe et la porte | pyjamas, tuques, sac d'école |
| Mur vert forêt grisé, panache d'orignal | **Murale « Camp de base »** au même mur ; enseignes gardées, **panache retiré** | nouveau thème, plus clair, gai et moderne |
| Garde-robe aménagée | **Gardée** (bacs étiquetés, tiroirs à Lego triés, penderie basse) ; le bac « 🦸 » devient « 🎭 COSTUMES », couleurs du nouveau thème | c'était bon ; pas de héros |

Gardés tels quels : les lits superposés, la commode blanche (à leur place réelle), la fenêtre et ses petits carreaux, les
chambranles et portes de pin teint, les plinthes chauffantes, le plancher d'érable, la suspension cage noire.

### Le thème : « Camp de base » (expédition nordique, version graphique)
Une murale de montagnes en **aplats** sur tout le mur de gauche (l'ancien mur vert), formes simples et lignes nettes :
le **jour du côté de la fenêtre** (grand soleil moutarde, ciel du matin) et la **nuit du côté des lits** (quart de ciel bleu
nuit avec lune et étoiles, au-dessus des lits superposés : on s'endort « sous les étoiles »). Devant : montagnes bleu fjord
enneigées, montagnes sauge, collines terracotta, trois petits sapins et une tente moutarde (le « camp de base »). Les deux
**enseignes de bois** à leurs noms sont gardées et remontées dans le ciel de la murale : le bois va avec l'idée du camp et
elles rendent la chambre à eux. Le reste de la pièce reste calme (murs blanc nuage), et le **bois naturel** (comme les lits)
et le **noir mat** (quincaillerie, suspension) font le rappel. Aucun personnage, rien de « bébé » : à 10-12 ans, une murale
de montagnes reste cool ; on change seulement les jouets dans les bacs.

Le **panache d'orignal** n'est pas gardé dans la chambre : c'est un trophée « chalet de chasse » qui ne va pas avec un thème
graphique et moderne, et ses pointes sont au-dessus de la zone de jeu et de l'échelle. À replacer ailleurs (au choix du
client : entrée, sous-sol, garage).

#### Palette (teintes d'écran, **à valider sur échantillon** : aucune référence de nuancier n'est certaine)
| Couleur | Hex (écran) | Où |
|---|---|---|
| Blanc nuage | #F3EFE7 | 3 murs (façade, mur des lits, mur de droite) et garde-robe |
| Blanc pur mat | #F5F5F1 | plafond (comme les panneaux des lits) |
| Ciel du matin | #CDE5F1 | ciel de jour de la murale (fond du mur de gauche) |
| Bleu nuit doux | #7B8CC2 | ciel de nuit de la murale (quart de disque au-dessus des lits) |
| Bleu fjord | #77A6C8 | grandes montagnes de la murale ; portes des armoires hautes ; un coussin |
| Sauge | #A9C2A0 | montagnes du milieu ; bac des dinos ; bacs de la garde-robe |
| Sapin doux | #5F8A6C | les trois sapins (petites surfaces seulement) |
| Terracotta | #DC9572 | collines ; bac des autos ; bac à toutous ; bordure du tapis ; étiquettes des boîtes |
| Moutarde | #E2A93F | soleil, lune, tente ; bac des Lego ; un coussin (rappel des draps-housses moutarde) |
| Neige | #FBF8F1 | neige des sommets, étoiles |
| Sable | #E8D9BD | grand tapis ; boîtes de lin de la tablette haute |
| Noir mat | #1E1F20 | boutons, porte de la tente, suspension et caissons de stores (existants) |
| Chêne naturel | (bois) | rebords à livres, tablette haute, tour aux albums, patères, caisses des bacs (comme les lits) |

Les couleurs ont été choisies **claires à moyennes** : sur téléphone (profil Léger, toute la pièce y est plus sombre), la
murale reste lisible et gaie ; seul le ciel de nuit, au-dessus des lits, sort bleu marine. La teinte de la peinture réelle
se choisit sur des échantillons posés au mur, à la lumière de la chambre. Plafond : on peut ajouter quelques étoiles
phosphorescentes au-dessus des lits (facultatif, non modélisé).

#### Deux autres thèmes possibles (non modélisés)
1. **« Arches et formes »** (graphique abstrait, esprit Bauhaus pour enfants) : grandes arches et cercles en aplats
   terracotta, moutarde, bleu ciel et crème sur le mur de gauche, une arche par lit au mur du fond comme « tête de lit »
   peinte, une bande de peinture-tableau noire à leur hauteur pour dessiner. Le plus intemporel (rien de figuratif) ;
   les enseignes vont aussi bien sur une arche. Un peu moins « histoire » pour un enfant de 4 ans.
2. **« Mission cosmos »** (espace, sans fusées ni héros de licence) : planètes en aplats et orbites au trait sur le mur de
   gauche, bande bleu nuit doux en haut des murs, étoiles phosphorescentes au plafond, accents moutarde et corail. Très
   aimé à 4-8 ans ; plus sombre (bleu nuit) donc à garder en bande étroite dans une petite pièce, et les enseignes de bois
   y vont moins bien.

### Le rangement (compté)
| Rangement | Où | Dimensions | Contenu | Qui |
|---|---|---|---|---|
| **3 bacs roulants bas** (caisse de bouleau, façade de couleur à prise ronde, étiquette pictogramme + mot, 4 roulettes) | sous le lit du bas, entre la patte de tête, l'échelle et la patte du pied ; ils sortent de 22 po vers le tapis | 19 × 30, 19 × 30 et 11 × 30 po, **6¼ po de haut roulettes comprises** | Lego en vrac, autos et pistes, dinos et figurines : **≈ 40 + 40 + 22 = ≈ 100 L** | les gars |
| **Livres de face** : 2 rebords de chêne à lèvre | au-dessus de la commode, z 33 et 44½ | 48 × 4 po | **≈ 8 à 10 albums de face** (les « livres de la semaine ») | les gars |
| Commode blanche (gardée) | mur de droite | 6 tiroirs | vêtements | les gars |
| **Armoires murales fermées** (caisson blanc, 2 portes bleu fjord, loquets de sécurité) | au-dessus des livres, z 57 → 84 | 48 × 12 × 27 po | **≈ 215 L** : jouets en rotation, grandeur suivante, souvenirs | parents |
| **Tablette haute** de chêne flottante + **6 boîtes de lin** à couvercle | de la fenêtre à la porte, au-dessus des armoires et de la porte de la garde-robe, dessous à 85½ po | 100 × 11 po ; boîtes ≈ 14 × 10 × 7½ po | **≈ 6 × 15 = ≈ 90 L** | parents |
| **Tour aux albums** de chêne | coin de la porte, contre le mur des lits | 17½ × 12¾ × 42 po | bac à toutous (≈ 28 L) + 2 rangs d'albums debout (**≈ 60 à 70 albums**) ; veilleuse dessus | les gars |
| **3 patères** sur une latte de chêne | mur de droite, entre la garde-robe et la porte, à 44 po | 9 po | pyjamas, tuques, sac | les gars |
| Garde-robe aménagée (gardée) | garde-robe | 24½ × 75½ po | 6 bacs de feutre étiquetés (≈ 6 × 30 L), 6 tiroirs à Lego triés, tablette des constructions, penderie basse à 42 po et haute à 78 po, bacs saisonniers, tablette haute | les deux |

**À leur portée** : ≈ 130 L de bacs (sous le lit et à toutous) + ≈ 180 L de bacs de garde-robe + ≈ 70 à 80 albums +
6 tiroirs à Lego + penderie basse + patères. **Pour les parents** : ≈ 215 L d'armoires + ≈ 90 L de boîtes en hauteur + la
tablette haute de la garde-robe. Tout est simple et souple : des bacs et des tablettes, aucun meuble fait pour une seule
activité.

**Les bacs sous le lit, mesurés sur les photos 07, 08, 11 et 12** : la traverse avant du lit du bas a son dessous à peu près à
la hauteur du dessus de la plinthe chauffante voisine (photo 07, au pied du lit côté mur), soit **≈ 7½ à 8 po du plancher
(ESTIMÉ)** ; aucune patte ni barre au milieu sur le devant (photo 07). Les bacs font donc 6¼ po de haut roulettes comprises
(≈ 1¾ po de jeu) et passent entre la patte de tête (x ≈ 13), l'échelle (x 61½ → 76½, dont le pied est à 22 po devant le
lit) et la patte du pied (x ≈ 89). **À mesurer au ruban avant d'acheter** : s'il y a moins de 7¼ po libres, on prend des
bacs de 5 po. Dans la maquette, on touche un bac (ou l'endroit où il sort) : il sort ; on le touche encore : il rentre.

### Le coin jeu ouvert
Le centre de la pièce et le coin de la fenêtre restent **libres** : un grand tapis plat 4½ × 7 pi (laine tissée ou coton
lavable, champ uni pour bâtir), deux coussins de sol ronds (18 po) pour s'asseoir, et rien d'autre. Le rangement est
**tout autour, à portée de main** : les bacs du lit sortent jusqu'au bord du tapis, les livres de face et la commode sont à
un pas, la tour aux albums et le bac à toutous à la porte, la garde-robe à côté. On joue aux Lego et aux autos au plancher ;
on ramasse en poussant le bac sous le lit.

Dégagements (en pouces, ESTIMÉS) : tapis à ≈ 6 po de la plinthe chauffante de la fenêtre et ≈ 10½ po de celle du mur de
gauche ; le bac de gauche, sorti, arrive à ≈ 7½ po de la plinthe du mur de gauche (on le rentre après le jeu) ; pied de
l'échelle à côté des bacs sortis, jamais dessus ; tiroirs de la commode et porte de la garde-robe libres ; ≈ 31 po de passage
entre la tour aux albums et la porte de la chambre ouverte ; fenêtre et arc des portes dégagés. **Aucun de ces chiffres
n'est une norme** : les dégagements devant les plinthes chauffantes sont à faire valider (fabricant de la plinthe,
électricien).

### Points à vérifier
1. **Dessous du lit du bas** : hauteur libre sous la traverse avant (≈ 7½ à 8 po estimé) et absence de barre au milieu.
2. **Plinthes chauffantes** : dégagements du tapis, des coussins et des bacs sortis **à faire valider** avec le fabricant et
   un électricien ; ne pas laisser un bac sorti devant la plinthe du mur de gauche.
3. **Ancrage et sécurité** : commode **ancrée** (elle est sous les armoires : un enfant pourrait y grimper), armoires
   vissées dans les montants avec **loquets de sécurité**, tablette haute sur supports cachés dans les montants (boîtes
   légères seulement), tour aux albums ancrée.
4. **Plafond** (96 po présumé) et dessus du chambranle de la garde-robe (84½ po estimé) : la tablette haute (dessous à
   85½ po) laisse ≈ 9 po pour les boîtes ; à mesurer.
5. **Murale** : état du mur (gypse), apprêt ; derrière la plinthe chauffante du mur de gauche, on peint autour (ou on la
   fait décrocher par un électricien) ; tracer la murale au crayon d'après la fiche, ruban à peinture pour les arêtes.
6. **Couleurs** : échantillons au mur avant d'acheter (le ciel, le bleu fjord et le bleu nuit surtout).
7. Prise de courant près de la tour aux albums (veilleuse) : à repérer.
8. Le panache d'orignal : où le replacer.

### Ordre de grandeur des coûts (version 2)
**Estimation** de l'agent, sans soumission ni prix vérifié en magasin (fourchettes 2026, taxes en sus, à confirmer) :

| Poste | Du commerce, posé soi-même | Sur mesure, posé |
|---|---|---|
| 3 bacs roulants bas | 120 – 300 $ | 450 – 900 $ |
| Armoires murales 48 × 12 × 27 (2 portes peintes, loquets) | 250 – 550 $ | 900 – 1 600 $ |
| 2 rebords à livres de chêne | 80 – 200 $ | 150 – 350 $ |
| Tablette haute de chêne 100 po (supports cachés) + 6 boîtes | 180 – 400 $ | 450 – 900 $ |
| Tour aux albums + bac | 150 – 350 $ | 400 – 800 $ |
| Patères | 30 – 80 $ | 30 – 80 $ |
| Tapis 4½ × 7 pi + 2 coussins de sol | 260 – 760 $ | 260 – 760 $ |
| Murale (apprêt, 6 à 8 couleurs en petits formats, ruban) | 150 – 300 $ | 600 – 1 500 $ (peintre ou muraliste) |
| Peinture des 3 autres murs et du plafond | 120 – 250 $ | 500 – 900 $ |
| Garde-robe aménagée (comme en version 1) | 500 – 1 100 $ | 1 500 – 2 800 $ |
| Ancrages, loquets, étiquettes | 40 – 80 $ | 40 – 80 $ |
| **Total** | **≈ 1 900 – 4 400 $** | **≈ 5 300 – 10 700 $** |

### Maquette 3D (version 2)
Arrêts, dans l'ordre : **Depuis la porte** ; **Le coin jeu (le tapis)** (le bac des Lego sort) ; **Les bacs sous le lit
(touche un bac)** (les trois sortent) ; **Le mur de rangement** (ils rentrent) ; **La murale et les lits** ; **La garde-robe
aménagée** (touche la porte) ; **De la fenêtre vers la porte**. Les portes s'ouvrent au toucher, les bacs sortent et rentrent
au toucher.

Moteur : une clé facultative et générique de plus pour les bacs, `"course": [dx, dy, dz]` sur une commande et
`"anim": "glisser"` sur ses objets (translation au lieu de monter ou descendre), documentée dans `renovation/README.md` et
dans le docstring de `generer_3d.commandes()`. Une commande sans `course` est rendue comme avant : MAISON-18 donne la même
scène, octet par octet (seul le code du gabarit change). La murale est une image plane (forme `image` déjà existante),
dessinée par `murale.py` ; aucune photo n'est dans la page.

### Ce qui reste imparfait (version 2)
- Toutes les dimensions de l'existant restent estimées sur des photos grand-angle ; le dessous du lit surtout.
- Les couleurs à l'écran ne sont pas celles d'un nuancier ; sur téléphone (profil Léger), toute la pièce est plus sombre.
- La murale est une image : de très près, ses arêtes sont un peu moins nettes qu'une vraie peinture au ruban.
- Les emojis des étiquettes (🧱, 🚗, 🦕, 🧸) dépendent de l'appareil ; sans police emoji, seul le mot s'affiche.
- La tablette haute et les patères ne sont pas dessinées au plan (trop petites ou au-dessus des armoires : voir les notes).
- Le plan final (`png/CH-01_plan_final.png`) est encore celui de la version 1 : à relancer avec le lien publié.

---

## Version 1 (révision A, 2026-11-09) — remplacée par la version 2
Ce qui suit décrit la première proposition (table à Lego, tour de bacs, tapis rond). Le relevé de l'existant (photos,
estimations, enveloppe) reste valable ; le coin jeu, ses coûts et ses arrêts sont remplacés par la section précédente.

### Les demandes du client (2026-11-09), mot pour mot
> « Je veux que tu modélises la chambre en haut du coin avant comme elle est présentement. Je veux seulement garder le lit
> superposé et le meuble blanc et que tu me proposes un coin jeu pour les gars pour jouer Lego, bac de jeu et place pour
> mettre les livres. »

> « Le bureau assis debout reste pas, c'est un test pour refaire la chambre bientôt et l'optimiser. Fais la chambre tout seul
> dans son monde à elle pas dans l'autre plan. »

### Comment le projet est construit
- `modifs.py` : copie de la base R0 + relevé photo RDC-01 (`base_rdc01_modifs.py`, copie telle quelle de
  `RDC-01_etat_actuel/modifs.py`), puis on ne garde **qu'un niveau** et, de ce niveau, la chambre (`piece-RDC-CH2`) et sa
  garde-robe (`piece-RDC-GRA`). Les murs qui les bordent sont coupés à leur contour (leur épaisseur reste) ; le reste de la
  maison (autres pièces, sous-sol, extérieur) n'existe pas dans ce projet.
- `geometrie.py` : tous les repères et dimensions (une seule source pour le plan et la maquette).
- `scene_3d.py` : matériaux, peinture, mobilier, lumières, arrêts de visite.
- Le générateur de plans n'est pas modifié. Le moteur 3D a reçu trois clés **facultatives et génériques** (petits carreaux
  de fenêtre, texte peint ou gravé, emprise d'une seule pièce), documentées dans `renovation/README.md` et dans les
  docstrings de `generer_3d.py` ; MAISON-18 se génère à l'identique.

### Ce qui vient des photos, ce qui est estimé
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

### Ce qu'on garde, ce qu'on enlève
- **Gardés** (à leur place réelle) : les lits superposés et la commode blanche. Le coin jeu ne gagne pas assez à les
  déplacer : les lits ne peuvent aller ailleurs sans bloquer une plinthe chauffante, la fenêtre ou la porte, et la commode
  est déjà au seul endroit libre du mur de droite.
- **Gardés aussi** (c'est la pièce) : fenêtre, portes, plinthes chauffantes, mur vert et son décor, suspension.
- **Enlevés** : fauteuil inclinable, petite table et chaises, présentoir à livres blanc, tablettes flottantes de jeux et
  cadres, toise, jouets et livres au sol (l'aspirateur robot et le tiroir de plastique au pied des lits aussi).

### Le coin jeu proposé : « l'atelier des bâtisseurs »
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

#### La garde-robe aménagée
- **Face à la porte** : étagère de chêne de 28 po (16 po de profond) avec **6 bacs de feutre étiquetés** à 2, 14 et 26 po
  (trains, casse-têtes, animaux, bricolage, costumes, jeux) ; dessus, **6 tiroirs à Lego triés par couleur** (pastille de
  couleur sur chaque tiroir : rouge, bleu, jaune, vert, orange, noir) ; au-dessus, une **tablette des constructions** à 56 po
  (les modèles finis s'exposent, hors de portée du petit frère).
- **Aile de gauche** : penderie double, tringle basse à **42 po** (leurs vêtements, qu'ils prennent seuls) et tringle haute à
  78 po (vestes, grandeur suivante) ; pantoufles au sol.
- **Aile de droite** : deux tablettes (30 et 52 po) de bacs saisonniers, gros bac « hiver » au sol (tuques, mitaines).
- Tablette haute à 83 po sur toute la longueur (rangement des parents), **ruban DEL** sous la tablette.
- La porte de pin est gardée (charnière côté fenêtre) : ouverte, elle ne gêne ni la commode ni les rebords à livres.

#### Circulation et dégagements (en pouces, ESTIMÉS)
- Porte de la chambre → lits et échelle : ≈ 31 po entre les tabourets et les lits ; ≈ 30 po entre la tour de bacs et la porte
  ouverte.
- Pied de l'échelle (y ≈ 74½) : rien devant ni sur le côté (le tapis commence à côté, il ne passe pas sous l'échelle).
- Tiroirs de la commode : ils sortent sur le tapis, rien devant ; arc de la porte de la garde-robe libre.
- Fenêtre : rien devant plus haut que l'allège ; plinthes chauffantes : aucun meuble devant, aucun rangement fermé dessus.

### Options
- **A — proposée (sans travaux)** : ce qui est dessiné. Meubles du commerce ou faits sur mesure, garde-robe aménagée avec un
  système modulaire.
- **B — si on refait la chambre au complet** : agrandir l'ouverture de la garde-robe à environ 60 po (cloison présumée non
  porteuse, à vérifier ; linteau, gypse, chambranles, deux portes de pin pliantes ou coulissantes) et y mettre **la commode**
  sous une penderie haute. Le mur de droite se libère sur environ 4 pi : on y met un vrai meuble bas de bacs avec la table à
  Lego dessus, et les livres de face juste au-dessus. Plus de rangement accessible, mais des travaux (voir coûts).
- Variante à considérer dans les deux cas : une porte de garde-robe pliante au lieu de la porte battante (plus d'arc dans la
  chambre), en pin teint pour garder le style.

### Points à vérifier sur place
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

### Ordre de grandeur des coûts (option A)
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

### Maquette 3D
Arrêts, dans l'ordre : **Depuis la porte** (comme la photo 11) ; **Le coin des bâtisseurs (Lego)** ; **Les livres de face** ;
**Les lits et le mur vert** ; **La garde-robe aménagée** (touche la porte pour l'ouvrir) ; **De la fenêtre vers la porte**
(comme la photo 06). Les deux portes s'ouvrent et se ferment au toucher. Dehors, par la fenêtre : ciel et terrain simples
(l'extérieur de MAISON-18 n'est pas recopié) ; par la porte de la chambre, un bout de corridor neutre (décor).

Ajouts au moteur pour ce projet (facultatifs, génériques, documentés dans `renovation/README.md`) :
- `SCENE["fenetres"][id]["carreaux"]` : la bande de petits carreaux de la fenêtre ;
- forme `"texte"` du mobilier : les noms des enseignes et les étiquettes des bacs ;
- `SCENE["bornes"]` : l'emprise d'une seule pièce (la garde-robe dépasse le mur de façade coupé).

### Ce qui reste imparfait
- Toutes les dimensions de l'existant sont estimées sur des photos grand-angle (précision de quelques pouces) ; les
  proportions des photos 08 et 12 ne s'accordent pas parfaitement avec un plafond de 96 po (à mesurer).
- Les noms des enseignes prennent l'écriture liée de l'appareil (Snell Roundhand sur iPad et iPhone) : la lettre ne sera
  pas exactement celle des planches gravées.
- Les panneaux du lit sont à coins carrés (les vrais ont des coins arrondis) ; le panache est stylisé.
- La porte de la garde-robe part fermée, comme sur les photos : il faut la toucher pour voir l'aménagement.
- Le plan ne montre pas le tapis ni les tringles de la garde-robe ; les rebords à livres sont en tirets (au mur, au-dessus
  de la commode).
