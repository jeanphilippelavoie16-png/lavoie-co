## Rez-de-chaussée — coin café, rangement de la salle de bain, porte de la salle de lavage — `rdc_cafe_sdb.py`

### Demande (client, 2026-11-02)
> « En haut dans la pièce qui sert à sortir dehors sur le balcon de piscine, je veux un coin café, avec la machine à café
> et tout. » — « Enlève les laveuse-sécheuse en haut et fais de l'espace de rangement, mais quelque chose d'original. »
> — « Présentement on n'est pas capable d'accéder à la salle de lavage, c'est buggé, la porte pas capable d'ouvrir. »

Les chaises, le coin ordi et la tuile d'ardoise de la cuisine sont traités par `rdc_cuisine.py` (DESIGN_cuisine.md).

---

### 1. Coin café dans l'entrée arrière

#### La pièce (relevé)
- **Entrée arrière** (`piece-RDC-EAR`), au nu intérieur x 229 → 317, y 380 → 430 : **88 × 50 po (7'-4" × 4'-2"), ≈ 30½ pi²**.
  La profondeur n'est pas cotée au plan de 1957 (PRÉSUMÉE à 5'-0" hors tout).
- **Baie** vers la salle à manger, sans porte (`ouv-RDC-026`) : x 279 → 311 (32 po), au mur avant de la pièce.
- **Porte du palier de la piscine** (`ouv-RDC-027`), mur de droite : y 392 → 426 (34 po), pentures côté mur du fond,
  s'ouvre vers l'intérieur. **Son arc occupe x 283 → 317, y 392 → 426** ; ouverte, elle se range contre le mur du fond.
- **Fenêtre** du mur du fond (`ouv-RDC-008`) : x 272 → 314, derrière la porte quand elle est ouverte.
- **Une descente** (photos 01, 07 et 08 : main courante qui descend le long du mur du fond) : modélisée en RDC-01 comme
  une volée de 6 contremarches, x 229 → 284 le long du mur du fond (`elem-RDC-R-ESCARR`, tout ESTIMÉ). Le plan de 1957
  n'en montre pas (« ARMOIRES » dans cette pièce) ; dessous, l'ancien caveau est devenu en SS-17 le walk-in de la chambre 2.

#### Le problème
Avec la volée, la pièce n'est qu'un palier et une cage d'escalier : il ne reste qu'une bande de 18 po entre la baie et le
vide de l'escalier, et le palier est pris par l'arc de la porte. **Aucun mur n'a 36 po libres devant lui.** Un coin café
n'y entre pas sans refermer la descente.

#### Parti pris (option A, dessinée)
**On referme la descente par un plancher à niveau** (solives sur lambourdes, contreplaqué, ardoise comme le reste) et on
fait du **mur de gauche (x = 229, 50 po, le seul mur plein)** un coin café encastré, d'un mur à l'autre :
- le sous-sol garde l'escalier principal (neuf, à l'entrée avant) et sa porte de côté ; le walk-in de la chambre 2 (SS-17),
  qui est dessous, n'a plus d'escalier qui arrive dedans (le conflit signalé par l'agent corrections disparaît) ;
- un vide non protégé de moins (aucune garde n'était visible du côté ouvert de la volée, avec des garçons de 4 et 6 ans).

| Élément | Dimensions | Détail |
|---|---|---|
| Mur de brique | 50 × 96 po (≈ 33 pi²) | Brique mince rouge à joints pâles, **la même que la cuisine** : on la voit en entrant par la baie |
| Caissons | 50 po de long, **24 po** de profond, socle en retrait de 2½ po | **Noir mat** comme les armoires de la cuisine |
| Petit frigo (lait) | **24 × 24 × 34 po**, ≈ 5 pi³ | Encastrable, ventilation par l'avant, **porte vitrée teintée** à cadre inox, poignée verticale ; à gauche (côté baie), pentures côté mur avant : ouverte, la porte longe le mur avant et ne touche pas la baie |
| 3 tiroirs | 24 po de large | Haut (8½ po) : **grains et capsules**, séparateurs ; milieu : tasses de réserve, filtres, détartrant ; bas : sacs de grains, sirops. Tirettes noires |
| Comptoir | 50 × 25¼ po, dessus à **36¼ po**, 1¾ po | **Bois de grange**, comme les comptoirs et l'îlot |
| Tablettes | 2 tablettes flottantes de 11 × 49 po, à **58 po** (22 po au-dessus du comptoir) et **72 po** | Bois de grange ; **ruban DEL 2700 K** sous chacune, sur gradateur (tasses, verres à latte, bocaux de grains, une plante) |
| Prises | 2 prises doubles à 44 po (8 po au-dessus du comptoir) | L'une sur un **circuit dédié de 20 A** (machine espresso 1 200 à 1 600 W), l'autre pour le moulin ; le frigo sur sa propre prise sous le comptoir |
| Appareils (maquette) | Machine espresso ≈ 12 × 15 × 16 po, moulin à trémie, pichet à lait, tasses | La machine du client (photos 01 et 08, sur le comptoir de la cuisine) peut y déménager |

**Passages** (vérifiés au plan et à la marche de la visite) : 62 po libres entre le nez du comptoir (x = 254¾) et le mur
du palier ; quand quelqu'un se fait un café (≈ 20 po devant le comptoir), il reste **42 po** jusqu'au mur de droite.
Le trajet baie → porte du palier (x 279 → 317, 38 po) et l'arc de la porte restent vides ; le frigo ouvert s'arrête à
x ≈ 278, avant la baie. Depuis la salle à manger, le coin café ne se voit pas (il est derrière le jambage gauche de la
baie) : on voit toujours la fenêtre et la porte de la piscine ; on le découvre en entrant.

**Pas d'évier.** L'évier de la cuisine est à ≈ 3,5 m (de l'autre côté de la salle à manger, mur arrière de la cuisine) et
les trois murs de l'entrée arrière sont extérieurs : une entrée d'eau et un renvoi (pente, évent) y gèleraient à
Baie-Comeau et coûteraient de 2 500 à 5 000 $. On garde une machine à réservoir (rempli à l'évier de la cuisine, trois pas).

#### Option B : garder la descente
Si la descente sert (elle mène au sous-sol ou au caveau), on ne peut pas mettre de coin café dans l'entrée arrière avec
les dégagements demandés. Le coin café irait alors dans la salle à manger, contre le mur arrière à gauche de la baie
(buffet de 18 po de profond, comptoir et tablettes pareils), ce qui demande de reculer la table (à coordonner avec
`rdc_cuisine.py`). Non dessinée.

#### Plan P-130 et maquette
- Pièce `piece-RDC-EAR` renommée **« Coin café »** (même polygone) ; éléments `elem-RDC-C-CAFE` (comptoir) et
  `elem-RDC-C-FRIGO` (« FR. ») ; la volée `elem-RDC-R-ESCARR` passe dans `elements_retires` (note : option A).
- 3D : mur de brique, caissons, frigo, comptoir, tablettes à DEL, prises, machine, moulin, tasses, bocaux, plante ;
  lampe DEL sous les tablettes ; le trou de plancher demandé pour la volée (`tremies_plancher` [229, 398, 284, 430]) est retiré.
- Arrêt de visite **« Coin café »** (307, 406, cap 186), après « Entrée arrière » ; ligne « Coin café » dans la palette.

---

### 2. Salle de bain : laveuse-sécheuse enlevées, « colonne d'apothicaire »

#### Étude de la chute à linge (demandée en premier)
On a superposé les deux plans :
- la niche de la laveuse-sécheuse (RDC) : x 76¼ → 105¾, y 144¼ → 172 ; la salle de lavage (SS) : x 10 → 109¾, y 10 → 154¾ ;
- **elles ne se recouvrent que sur une bande de 8¾ po** (y 144¼ → 153), juste devant la **poutre maîtresse 8 × 10**
  (`str-SS-P02`, axe y = 157, y 153 → 161) sur laquelle repose la cloison lavage / salle de bain du sous-sol ;
- la cloison du fond de la salle de bain (`mur-RDC-R01`, y = 142) est elle-même **ESTIMÉE** d'après les photos ; au plan
  de 1957 elle est sur l'axe de la poutre (y = 157) : dans ce cas, **aucun recouvrement**.
- les solives (2 × 10 à 20 po c/c) sont parallèles à y : une gaine peut se décaler en y dans l'épaisseur du plancher
  (≈ 4 po), pas en x ;
- elle arriverait au plafond du lavage vers x 78 → 92, y 141 → 153 : **en plein dans l'arc de la porte de la salle de
  lavage** (vantail de 29 po qui s'ouvre vers le lavage, arc x 80 → 110, y 120 → 150). Un panier dessous bloquerait la porte ;
  il faudrait un déflecteur jusqu'à un panier entre le chauffe-eau et l'arc (x 50 → 78), hors du dégagement du panneau.

**Conclusion : la salle de lavage est « presque » dessous, mais pas assez pour la dessiner sans mesurer.** On propose
d'abord un rangement original sans structure (ci-dessous) et la chute en **option B, conditionnelle**.

#### Parti pris : la colonne d'apothicaire (dessinée)
Un meuble pleine hauteur encastré dans la niche, entre le muret de la douche et la cloison du dégagement : **29½ po de large
× 24 po de profond × 96 po** (x 76,2 → 105,75, y 144,25 → 168,25). Caisson **noir mat** comme la vanité ; façades de
**bois de grange** comme les comptoirs de la cuisine.

| Hauteur | Module | Détail |
|---|---|---|
| 4 → 30 po | **2 paniers à linge basculants** (14½ po chacun) | Linge pâle / linge foncé, sacs de toile amovibles qu'on descend au lavage ; façades noires, tirettes noires |
| 30 → 62 po | **6 tiroirs d'apothicaire** (2 × 3, ≈ 14½ × 10½ po, 22 po de profond) | Bois de grange, poignées-coquilles et **porte-étiquettes noirs : un tiroir par membre de la famille** (comme les bacs de l'entrée), plus pharmacie et réserves |
| 62 → 84 po | **Niche ouverte éclairée** (28 × 21 × 23 po) | Fond de bois de grange, ruban DEL en haut ; **9 serviettes roulées cordées comme du bois de chauffage** (4-3-2) |
| 84 → 96 po | Armoire du haut, 2 portes noires à ouverture par poussée | Papier, savons, réserves |

- **Dégagements** : le devant de la colonne recule de 4 po par rapport à la laveuse (y 168¼ au lieu de 172) : le passage
  entre la colonne et la vanité passe de 28 à **32 po** ; la porte de la salle de bain s'ouvre vers le dégagement (rien ne
  change) ; la douche, la toilette et la vanité ne bougent pas.
- **À faire derrière** : entrées d'eau et renvoi de la laveuse condamnés dans le mur, sortie de la sécheuse bouchée,
  circuit 240 V de la sécheuse retiré (ou converti, voir options).

#### Options
- **B — chute à linge** (si les mesures le permettent) : gaine d'acier galvanisé de 12 × 14 po derrière le panier de gauche,
  bouche **à 36 po ou plus** avec trappe à fermeture automatique et **loquet de sécurité pour enfants** (ouverture de 12 po
  au plus : les garçons ont 4 et 6 ans), arrivée au plafond du lavage avec déflecteur vers un panier roulant entre le
  chauffe-eau et l'arc de la porte. Conditions : cloison du fond bien à y ≈ 142, baie de solives libre entre x ≈ 76 et 106,
  aucun conduit dedans. Si le sous-sol devenait un logement séparé, la chute devrait être enlevée ou coupe-feu. + 1 500 à 3 500 $.
- **C — porte-serviettes chauffant** noir mat sur le muret, branché sur le circuit de la sécheuse converti : + 400 à 900 $.

#### Plan P-130 et maquette
- `elem-RDC-R-LAV` passe dans `elements_retires` ; nouvel élément `elem-RDC-S-APOTH` (armoires, X).
- 3D : laveuse, sécheuse, hublots et boutons enlevés ; colonne dessinée module par module ; lampe DEL de la niche.
- Arrêt de visite **« Salle de bain — rangement »** (103, 196, cap 252), après « Vanité ».

---

### 3. Porte de la salle de lavage (sous-sol) : le bogue, et la correction
**Cause** : SS-17 (`zone_gym.py`) revêt de miroir la face gym de la porte `ouv-SS-P02` pour qu'elle se fonde dans le
mur-miroir. Mais le miroir et sa plaque noire étaient un **décor fixe** posé devant la porte, à fleur du mur (x 112,9 → 114,2),
sans lien avec elle : le toucher tombait sur le miroir, pas sur la porte (**elle ne s'ouvrait pas**), et quand la porte
s'ouvrait toute seule sur un trajet, le miroir restait dans la baie (on passait à travers).

**Correction** (dans `zone_gym.py`, seulement les lignes de cette porte) : le miroir est collé sur la face gym du vantail que
dessine le moteur (fermé : x 109,75 → 111,55) et **lié à la porte** (`"porte": "ouv-SS-P02"`, le mécanisme des portes
finies et de la porte-bibliothèque) ; il pivote avec elle vers le lavage. La poignée côté gym suit aussi ; côté lavage, c'est
la béquille noire du moteur. Le pivot ne change pas (x 109,75 ; y 149,5), la porte s'ouvre toujours vers le lavage (pas de
porte qui balaie la zone d'entraînement). Le miroir est maintenant en retrait de 2½ po dans son cadre noir (comme une vraie
porte dans son chambranle) au lieu d'être à fleur.
Vérifié sans rendu : 2 objets liés à la porte, plus aucun décor fixe dans la baie, trajet gym → lavage OK.

---

### Coût (ordre de grandeur ; estimation du designer, prix courants au Québec 2025-2026, non soumissionnée : à confirmer par 2 ou 3 soumissions à Baie-Comeau)
| Poste | Fourchette |
|---|---|
| Fermer la descente : solives, contreplaqué, ardoise (≈ 12 pi²), main courante enlevée, gypse dessous | 1 500 – 3 500 $ |
| Ébénisterie du coin café (caissons noir mat, 3 tiroirs, comptoir et 2 tablettes de bois de grange) | 2 500 – 4 500 $ |
| Brique mince posée (≈ 33 pi²) | 800 – 1 500 $ |
| Électricité du coin café (circuit 20 A, 3 prises, DEL et gradateur) | 800 – 1 600 $ |
| Petit frigo encastrable 24 po à porte vitrée | 900 – 1 800 $ |
| **Coin café** (machine et moulin non compris) | **≈ 6 500 – 12 900 $** |
| Laveuse-sécheuse : condamner l'eau, le renvoi, la sortie et la prise ; réparer le gypse | 400 – 900 $ |
| Colonne d'apothicaire sur mesure (30 × 24 × 96 po) | 3 500 – 6 500 $ |
| DEL de la niche et interrupteur | 250 – 500 $ |
| **Salle de bain** | **≈ 4 200 – 7 900 $** |

### Points à valider sur place
1. **La descente de l'entrée arrière** : où elle mène (sous-sol, caveau, dehors ?), nombre de marches, largeur ; si on la
   referme, ce qu'il y a dessous. **Décision du client : option A (refermer, coin café) ou B (garder).**
2. Mesurer l'entrée arrière (88 × 50 po présumés) et la niche de la laveuse (29½ × 27¾ po estimés).
3. L'entrée arrière est-elle chauffée l'hiver ? (frigo : 10 °C minimum). Plinthe électrique sous la fenêtre du fond
   (bande sombre sur la photo 01, à confirmer) : la garder, rien devant.
4. Murs extérieurs derrière la brique et les prises : isolant, pare-vapeur, boîtes étanches.
5. Salle de bain : où sont les entrées d'eau, le renvoi et la sortie de la sécheuse ; ventilateur de la salle de bain.
6. Pour la chute (option B) : position réelle de la cloison du fond (y ≈ 142 ou 157), sens et position des solives, poutre.
7. Le panneau électrique a-t-il la capacité d'un circuit de 20 A de plus.

À valider avec la Ville et un professionnel (plancher qui ferme la descente, électricité, chute à linge, coupe-feu si le
sous-sol devenait un logement).

### Note proposée pour le cartouche de P-130 (les notes sont fixées dans `modifs.py`)
« Entrée arrière : descente refermée (à valider), coin café ; salle de bain : colonne de rangement au lieu de la laveuse-sécheuse. »

### Ce qui reste imparfait
- La volée de l'entrée arrière n'a jamais été mesurée : l'option A est dessinée sur une estimation.
- Dans la visite, on traverse les meubles (le moteur n'en fait pas des obstacles, partout dans la maison).
- La machine espresso et le moulin sont faits de blocs (aucun modèle CC0 / CC BY de machine au catalogue).
- À l'arrêt « Coin café », le bas des caissons (frigo, tiroirs) sort du cadre : la pièce n'a que 62 po de recul ;
  on le voit en baissant le regard.
