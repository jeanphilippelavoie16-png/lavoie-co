# MAISON-18 — Fenêtres agrandies vers le bas et congélateur (agent « fenetres »)

## Demande (client, 2026-11-02)
- « Les fenêtres en bas sont plus grosses aussi (par le bas), sauf salle de bain et salle de lavage. La fenêtre du salon en
  haut est aussi plus grande vers le bas. »
- « On a un gros congélateur debout (genre gros comme un frigidaire) qu'il faudrait lui trouver une place en bas. »

Le client n'a donné aucune mesure. **Hypothèses à mesurer** :
- sous-sol : allège de **40 po** au lieu de 56 po, tête inchangée (86 po) ;
- salon du rez-de-chaussée : allège de **20 po** au lieu d'environ 34 po, tête (82 po) et linteau inchangés ;
- congélateur : **≈ 20 pi³, 32 po de large × 30 po de profond × 70 po de haut**.

## Ce qui change et pourquoi

### 1. Moteur 3D : allège et tête par fenêtre (`renovation/outils/generer_3d.py`, `visite3d_gabarit.html`)
Avant, le moteur utilisait une seule allège et une seule tête par étage (`SCENE["allege_fenetre"]` et `SCENE["tete_fenetre"]`).
On ajoute un réglage par fenêtre, à activer au besoin :

```python
SCENE["fenetres"] = {"ouv-SS-002": {"allege": 40},                       # tête : celle de l'étage
                     "ouv-RDC-002": {"allege": 20, "tete": 82, "sections": 3}}
```

- **Où le réglage s'applique** : le trou dans le mur, la vitre, le cadre noir, les meneaux, la tablette, les jambages et
  la tête. La lumière du jour suit la vitre : une fenêtre plus grande éclaire plus. Le réglage vaut aussi dans la
  maquette des deux étages, où chaque étage lit le sien, et dans les maquettes `ETAGE=SS` et `ETAGE=RDC`.
- **Clés facultatives** :
  - `"sections"` : le nombre de châssis, avec des meneaux également répartis (2 par défaut, soit le meneau central
    d'avant) ;
  - `"traverses"` : une liste de z pour des traverses horizontales, par exemple un panneau fixe en bas ;
  - `"margelle"`.
- **Terrain vu par la fenêtre** : si l'allège tombe sous le terrain (`sol_exterieur` + 2 po), le moteur pose une
  **margelle** devant la fenêtre :
  - fond de gravier à l'allège − 8 po ;
  - trois parois de béton jusqu'au terrain + 4 po ;
  - saillie de 36 po depuis la face extérieure du mur, et 6 po de débord de chaque côté.

  Le terrain est alors troué au ras de la maison et des margelles (`terrain_trou`). Avant, le trou était le grand
  rectangle de la maison : il laissait un vide de 50 à 60 po devant les façades avant et arrière. Pour régler la margelle :
  `"margelle": {"saillie", "debord", "fond", "dessus", "mat", "mat_fond"}`. `False` la retire.
- **Contrôles** : un id qui n'est pas une fenêtre de l'étage, une allège au-dessus de la tête, une clé inconnue ou des
  sections non entières arrêtent la génération avec un message clair.
- **Rien ne change pour un projet sans `"fenetres"`** : la scène générée est identique octet pour octet pour SS-17,
  RDC-01 et MAISON-18 avant réglage (copies de travail, voir Vérifications).

### 2. Sous-sol : 5 fenêtres descendues (`zone_global.py`, `SCENE["fenetres"]`)
| Fenêtre | Pièce | Largeur | Allège | Vitrage | Margelle (béton) |
|---|---|---|---|---|---|
| ouv-SS-002 | séjour, façade avant | 75 po | 56 → **40** po | 30 → 46 po de haut (+53 %) | x 337–427, 36 po de saillie |
| ouv-SS-004 | séjour, mur de droite (store, toile) | 36 po | 56 → **40** | idem | y 49½–100½ |
| ouv-SS-009, ouv-SS-010 | chambre 1, mur arrière (évacuation) | 40 po chacune | 56 → **40** | idem | deux margelles, x 84½–139½ et 148½–203½ |
| ouv-SS-003 | chambre 2, mur de droite (évacuation) | 80 po | 56 → **40** | idem | y 260½–355½ |
| ouv-SS-006 (salle de bain), ouv-SS-007 (salle de lavage) | — | 36 po | **56, inchangée** (demande du client) | — | — |

- **Pourquoi 40 po** : le vitrage grandit de moitié, et l'allège reste au-dessus des meubles bas (banc à jouets du séjour
  à 16 po, bancs et bureaux à 30 po ou moins). Pour une fenêtre d'évacuation, environ 1 m d'allège se franchit sans
  marche ; à 56 po (1,42 m), il en fallait une.
- **Terrain** : le terrain est à environ 48 po au-dessus du plancher du sous-sol (56 − 8). Une allège de 40 po tombe
  donc 8 po sous le terrain, d'où une margelle devant chacune. Fond de gravier à 32 po, parois jusqu'à 52 po, soit
  4 po au-dessus du terrain. Les 36 po de saillie dépassent les 760 mm (30 po) de dégagement demandés devant une fenêtre
  d'évacuation qui donne sur une margelle (à confirmer).
- **Données** : l'allège (40 po, PRÉSUMÉE) et une note sont reportées sur chaque ouverture dans `maison.json`. Sur P-129,
  la note 1 devient : « Fenêtres agrandies par le bas (allège ≈ 40 po, sauf bain et lavage) ; congélateur au lavage. »
  Le cartouche ne tient que 5 notes : l'ancienne note 1 (« Esquisse par-dessus SS-16… ») était la moins utile au client.

### 3. Rez-de-chaussée : la fenêtre du salon (`base_rdc01_scene.py`, une seule ligne)
- ouv-RDC-002, façade avant, 108 po de large, 3 sections (x 323–431) :
  - allège environ 34 → **20 po** ;
  - tête (82 po) et linteau 2-2×10 inchangés ;
  - vitrage de 48 → 62 po de haut (+29 %) ;
  - deux meneaux (`"sections": 3`), comme la fenêtre réelle à 3 sections.
- Le store cellulaire remonté reste en haut de l'embrasure.
- Le terrain est à environ 57 po sous le plancher du RDC : pas de margelle.
- `modifs.py` reporte l'allège (20 po, PRÉSUMÉE) dans `maison.json`. La note 1 de P-130 se termine par « fenêtre du
  salon descendue (allège ≈ 20 po) ».

### 4. Meubles devant les fenêtres plus basses (contrôle géométrique)
Recherche : tout objet à moins de 32 po d'une fenêtre visée et qui monte plus haut que la nouvelle allège.
- **Séjour (ma zone)** :
  - **store** de la fenêtre de droite : il était remonté aux 2/3 (de 74 à 84 po) ; il est maintenant à mi-hauteur de
    la fenêtre agrandie (63 à 84 po) ;
  - la **toile motorisée** descend devant cette fenêtre, comme avant ;
  - le banc à jouets (16 po), la barre de son et les blocs de bois restent sous l'allège ;
  - rien devant la fenêtre avant.
- **Chambre 1 et chambre 2 (zones des autres agents, non touchées)** — contrôle refait sur les nouvelles chambres :
  - rien ne dépasse 40 po devant ouv-SS-009, ouv-SS-010 et ouv-SS-003, à part une tringle au plafond (chambre 1) ;
  - la nouvelle chambre 1 n'a plus de banquette sous ses fenêtres. Avec l'allège à 40 po (≈ 1 m), on sort encore sans
    marche (à confirmer) ; à 56 po, ça n'aurait pas été le cas. **L'allège basse est donc nécessaire à cette chambre** ;
  - chambre 2 : seuls des meubles bas (≤ 25 po) sont au bout de la fenêtre ;
  - **pour leurs nouvelles versions** : rien de plus haut qu'environ 38 po à moins de 30 po de ces fenêtres (pas
    d'étagère, de tête de lit haute ni de garde-robe devant) ;
  - un bureau sous une fenêtre d'évacuation est déconseillé : il gêne la sortie.
- **Salon du RDC** :
  - le repose-pieds du sectionnel (15½ po) et la plante en pot sont devant la fenêtre, sous l'allège de 20 po :
    acceptable ;
  - le bras du sectionnel (24 po) s'arrête à x = 316, juste à côté de l'ouverture ;
  - le meuble télé est sur le mur de droite. Rien d'absurde.

### 5. Congélateur : au bout du comptoir de pliage, dans la salle de lavage (`zone_global.py`)
**Où** : une niche de 33 po (x 77½–109¾, y 86½–119½), dos au mur du gym, au bout du comptoir de pliage en L, juste à
gauche quand on entre par la porte du lavage.

**Pourquoi là** :
- la salle de lavage est la pièce utilitaire : dalle de béton, panneau électrique à côté pour une prise dédiée ;
- on ne l'entend pas des chambres ;
- c'est le chemin naturel depuis l'escalier : hall, gym, porte du lavage ;
- le comptoir de pliage sert de surface de dépôt pour l'épicerie, juste à côté.

**Les autres places essayées** :
- **Mur de gauche, entre la laveuse et le panneau** : entre le cadre de la fenêtre (y 67½) et le dégagement du panneau
  (y 94), il reste 26 po. Le congélateur cacherait la fenêtre ou empiéterait sur le dégagement.
- **Contre le mur du fond, devant le chauffe-eau** : c'est le dégagement de 36 po du chauffe-eau, et la porte du lavage
  balaie jusqu'à x = 82.
- **Retour du comptoir sur le mur avant (sous le VRC)** : il bloquerait le panneau d'accès du VRC et le coin du comptoir.
- **Vestiaire, hall, gym, dessous de l'escalier, walk-in** : un passage, une entrée chic, un gym déjà plein, le
  banc-cabane des garçons, une chambre. Hors de question.
- **Excroissance sous le perron** : aucun accès.

**L'appareil** :
- congélateur vertical blanc, comme la laveuse et la sécheuse ; caisse de 32 × 28¼ po, porte de 2 po, 70 po de haut ;
- 2 po d'air derrière, ½ po de chaque côté ;
- porte à droite, avec les pentures du côté de la porte du lavage : elle s'ouvre en s'éloignant du comptoir où l'on pose
  les sacs ;
- poignée verticale inox du côté du comptoir, petit afficheur de température.

**Dégagements vérifiés** (script de plan, voir Vérifications) :
- **porte du lavage** (y 120–150, pentures à y = 150) : son quart de cercle de 30 po passe à 1,2 po du coin du
  congélateur. Ajouter une butée de porte ;
- **panneau électrique** : zone de 30 po de large × 1 m devant (x 10–49½, y 94–124) libre. Seule la porte du congélateur
  y entre de 4 po quand elle est grande ouverte, temporairement ;
- **chauffe-eau** : 36 po libres devant (x 45–81, y 127–149). Le déshumidificateur, qui était à 5 po devant, est
  déplacé (voir plus bas) ;
- **passage** : 63 po de plancher libre entre le panneau et la porte du congélateur. La porte du congélateur
  (32 po) balaie x 45½–77½ quand on l'ouvre ;
- **séchoir suspendu** (z ≥ 80) : 10 po au-dessus du congélateur.

**Prise** : prise simple **dédiée**, sur son propre circuit et étiquetée au panneau, au mur à 74–78 po au-dessus du
congélateur. On voit la fiche, et on peut y brancher une alarme de température.

**Ce que ça coûte au lavage** :
- **le comptoir de pliage raccourci** : il fait maintenant y 35–86½ (51½ po + le retour de 40 po sur le mur avant) ;
- **le trieur à 2 sacs disparaît**, avec les deux tablettes et leurs paniers au-dessus ;
- **le bac recule de 7 po** (y 64–82) : il reste 4½ po de comptoir entre le bac et le congélateur ;
- **les paniers de linge propre des garçons** passent de 15 à 11½ po de large (un par garçon, toujours à leur couleur).

**Déshumidificateur** : il était à 5 po devant le chauffe-eau. Il passe contre le mur de gauche, sous la fenêtre du
lavage, à côté de la laveuse (x 11–25, y 46–66, 24 po de haut, sous l'allège de 56 po). Son boyau va à l'évacuation de
la laveuse.

**Plan P-129** : élément `elem-SS-Q-CONG` « CONG. » (type réfrigérateur, face vers la pièce). Le comptoir de pliage et le
bac sont raccourcis et déplacés, le DÉSH. est déplacé.

**3D** : blocs propres (caisse, porte, grille du bas, penture, poignée inox, afficheur), prise et cordon. Nouvel arrêt de
visite « Congélateur (salle de lavage) » (30, 104, cap 2), placé après « Paniers de linge des garçons » (`ss_scene.py`,
ordre du parcours). La ligne « Salle de lavage » de la palette le mentionne, et une ligne « Fenêtres (MAISON-18) » est
ajoutée.

## Options
- **Allège du sous-sol** :
  - 36 po : plus de vitrage, mais la margelle est plus creuse et plus chère ;
  - 44 po : moins de sciage, encore 8 po de gagnés.

  On garde 40 po, qui ne dépasse pas les meubles bas. Changer la valeur se fait en une ligne : `ALLEGE_SS` dans
  `zone_global.py`.
- **Margelles** :
  - béton coulé ou préfabriqué (dessiné) : chic, au style du béton du sous-sol ;
  - acier galvanisé ondulé : moins cher ;
  - ou terrain abaissé en pente douce devant la fenêtre avant du séjour (plus de lumière, pas de puits), si le
    terrain le permet.
- **Salon du RDC** :
  - 20 po (proposé), ou 24 po pour garder un dossier de meuble bas devant ;
  - une traverse à environ 34 po avec un panneau fixe en bas est possible : `"traverses": [34]` dans `SCENE["fenetres"]`.
- **Congélateur** :
  - inox plutôt que blanc, si le client préfère ;
  - un modèle de 33-34 po demande de raccourcir le comptoir de 1 à 2 po de plus (le bac garde alors 2½-3½ po de
    comptoir) ;
  - près de la porte de côté (épicerie) : pas de place sans sacrifier le vestiaire ou le gym. Le lavage reste le
    meilleur compromis.

## Coût (ordres de grandeur 2026, à faire chiffrer)
| Poste | Estimation |
|---|---|
| Sous-sol, par fenêtre : sciage de la fondation sous l'appui (16 po), nouvelle fenêtre ouvrante, imperméabilisation | 3 500 à 7 000 $ |
| Sous-sol, par fenêtre : margelle (excavation, drain relié au drain français, gravier, couvercle) | 1 500 à 3 500 $ |
| **Sous-sol, 5 fenêtres** | **≈ 25 000 à 50 000 $** |
| Salon du RDC : fenêtre de 108 po à 3 sections, ossature de l'allège, parement extérieur et finition intérieure à refaire sous la fenêtre | 6 000 à 12 000 $ |
| Congélateur vertical ≈ 20 pi³ | 1 200 à 2 000 $ |
| Circuit et prise dédiés | 300 à 600 $ |
| Comptoir raccourci, bac déplacé (plomberie) | 600 à 1 500 $ |

## Points à vérifier — à valider avec la Ville et un professionnel
- **Structure du sous-sol** :
  - la tête ne bouge pas : le linteau existant reste, mais vérifier son état ;
  - sous l'appui, la fondation est sciée sur 16 po de haut : vérifier qu'elle est en béton coulé, et non en blocs ;
  - armatures et appui à refaire par un ingénieur.
- **Structure du RDC** : nouvelle lisse d'appui et montants nains sous la fenêtre du salon. Le linteau 2-2×10 reste si la
  largeur ne change pas.
- **Margelles** :
  - drain au fond relié au drain français ;
  - pente du terrain qui éloigne l'eau ;
  - la neige de Baie-Comeau : prévoir un couvercle de polycarbonate ;
  - avec des garçons de 4 et 6 ans, couvercle anti-chute, qui doit s'ouvrir de l'intérieur pour les fenêtres
    d'évacuation des chambres.
- **Fenêtres d'évacuation des chambres (ouv-SS-003, ouv-SS-009, ouv-SS-010) : c'est un gain** :
  - allège d'environ 1 m (40 po) au lieu d'environ 1,42 m ;
  - ouverture libre plus grande ;
  - margelle avec au moins 760 mm devant, à confirmer ;
  - elles doivent ouvrir : battant ou coulissant, au moins 0,35 m² libres, aucune dimension sous 380 mm.
- **Sécurité des enfants au RDC** : une allège de 20 po (≈ 510 mm) est à la portée d'un enfant de 4 ans.
  - sections ouvrantes avec limiteur d'ouverture d'environ 100 mm, ou sections du bas fixes ;
  - verre trempé conseillé pour un vitrage aussi bas ;
  - vérifier les exigences de garde du Code.
- **Confort** : plus de vitrage, c'est plus de perte de chaleur et de condensation.
  - fenêtres à haut rendement (triple vitrage au sous-sol) ;
  - plinthe chauffante ou sortie d'air sous les fenêtres agrandies.
- **Intimité** : au séjour, la fenêtre avant donne sur la rue au niveau du sol. Un store ou un film givré en bas, au besoin.
- **Congélateur** :
  - une prise à moins de 1,5 m du bac demande probablement une protection DDFT (Code de construction du Québec,
    ch. V – Électricité) : à valider avec l'électricien ;
  - si un DDFT est exigé, une **alarme de température** Wi-Fi est conseillée : un déclenchement passe inaperçu ;
  - laisser 2 po d'air derrière (fiche du fabricant) ;
  - butée de la porte du lavage ;
  - mesurer le modèle choisi : niche de 33 po, 30 po de profond dans le passage.
- **Mesures** : allèges et têtes réelles, hauteur du terrain devant chaque fenêtre, épaisseur de la fondation, modèle du
  congélateur. Toutes les cotes de ce document sont des hypothèses.

## Fichiers modifiés
- `renovation/outils/generer_3d.py` :
  - `reglages_fenetres`, `allege_tete`, `margelles`, `terrain_trou` ;
  - `boites_mur` et `finitions` prennent `fen` ;
  - `construire` et `fusionner` transmettent `terrain_trou`.
- `renovation/outils/visite3d_gabarit.html` : le terrain est troué par `S.terrain_trou` s'il existe, sinon par le
  rectangle d'avant.
- `zone_global.py` (MAISON-18) :
  - fenêtres (`ALLEGE_SS`, `FENETRES_BASSES`) ;
  - niche, comptoir et bac (`YN0`, `YN1`, `appliquer_modifs`, `_retirer_ss16`, `_lavage`) ;
  - `_congelateur` ;
  - déshumidificateur et store ;
  - arrêt de visite et palette.
- `base_rdc01_scene.py` : `SCENE["fenetres"]` de la fenêtre du salon (une ligne).
- `modifs.py` : allège de ouv-RDC-002 dans les données, note 1 de P-129, fin de la note 1 de P-130.
- `ss_scene.py` : l'arrêt « Congélateur (salle de lavage) » dans l'ordre du parcours.

## Vérifications
- **Plans** : `construire_projet.py` sans erreur sur une copie de travail. Les avertissements sont les mêmes qu'avant :
  repères, épaisseurs présumées, cartouche du RDC.
- **Moteur inchangé sans réglage** : scène JSON identique avant et après le changement de moteur pour SS-17, RDC-01 et
  MAISON-18 (copies de travail ; même md5).
- **Maquettes** :
  - `ETAGE=SS` : margelles et terrain troué ;
  - `ETAGE=RDC` : fenêtre du salon à 20 po, pas de margelle ;
  - deux étages (sans ETAGE) : page de 12,6 Mo, sous le budget de 14 Mo.
- **Script de plan (matplotlib)** : congélateur, porte du lavage, dégagements du panneau et du chauffe-eau, margelles et
  trou du terrain.
- **Rendus (2 appels, script CSP, aucune erreur de page)** :
  - fenêtres agrandies : séjour avant et côté, chambre 1, chambre 2 ;
  - congélateur : de face et en diagonale avec le bac ;
  - salle de lavage : déshumidificateur sous la fenêtre ;
  - salon du RDC ;
  - margelle avant vue de l'extérieur ;
  - maquette des deux étages.

  Planche : `scratchpad/m18/fenetres/planche_fenetres_congelateur.jpg`.
