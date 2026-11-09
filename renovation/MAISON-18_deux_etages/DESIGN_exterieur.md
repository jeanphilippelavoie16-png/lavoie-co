## Extérieur — la maison vue de dehors et la cour arrière (plan et vidéo DAG)

**Demande du client** : « Je veux aussi que tu fasses l'extérieur. » Puis, le 2 novembre 2026, avec 12 captures nettes de la
vidéo DAG : il veut que **l'extérieur ressemble à la vidéo** (section « Captures de la vidéo DAG », plus bas).

On n'a pas redessiné la cour : on a **mis en 3D le projet de Design Action Gestion (DAG)**, et on a ajouté autour la
maison vue de dehors, le devant du terrain et les côtés. Les données sont dans `exterieur.py` (dictionnaire `EXTERIEUR`,
contrat dans son docstring) ; **la visite les dessine et on y marche** : on fait le tour de la maison, on va dans la cour,
on entre et on sort par les portes (voir « Dans la visite », plus bas).

### Sources

| Source | Ce qu'on en a tiré |
|---|---|
| **Plan d'aménagement de la cour arrière, DAG, 17-12-2025**, éch. 3/16" = 1'-0" (`plan_cour-1.png`, 150 ppp) | Position et dimensions du palier, de l'escalier, du patio, du deck, du cabanon (agrandi en garage) et de la piscine de 21 pi (cotes) ; couleurs des garde-corps ; lignes de lot arrière et côtés (le plan est dessiné sur le certificat de localisation) |
| **Vidéo DAG « C-1329 Aménagement extérieur »** : 12 captures nettes (2026-11-02) | L'allure de tout le reste : forme du toit, pignons, fondation, niveaux du terrain, allée, muret et marches de pierre, escalier ouvert, piscine, cabanon, mobilier, arbres (détail dans la section du 2026-11-02) |
| `donnees/maison.json` (relevé R0, plan d'implantation 1957 P7, croquis 2016 P1) | Murs extérieurs, fenêtres et portes (lus à chaque génération : si un autre module change une ouverture, la façade suit), cheminée, perron avant, entrée arrière, lignes de lot du devant, fermes 5/12 |

**Calage du plan DAG.** Le dessin est tourné de 180° par rapport à nos plans. On a mesuré l'image au pixel près, à l'échelle de
la largeur de la maison (38'-0" = 1067 px, donc 2,34 px par pouce) : x = 456 - (x_px - 625) / 2,34 ; y = 380 + (y_px - 171) / 2,34.
Ça recoupe tout ce qu'on peut vérifier, à moins de 1 po près : l'entrée arrière tombe à x 219-327 (relevé : 219-327) ; le
palier fait 129 × 60 po (« ±10'-9" × 4'-11" ») ; le cabanon est à 3'-0" des deux lignes de lot. Les lignes de lot du plan DAG
concordent avec le plan d'implantation de 1957 à 4 po près.

### Ce qui est modélisé

Repère de la maison, en pouces ; z est compté depuis le plancher du sous-sol. Le rez-de-chaussée est à 105, la cour à 48.

**La cour**

| Élément | Où (x, y) | Hauteur, matériau |
|---|---|---|
| Palier ±10'-9" × 4'-11" | 327-456 × 380-440, contre le mur arrière, devant la porte de l'entrée arrière | dessus à 97½ (une marche sous le seuil) ; composite beige clair, lames selon x à joints sombres |
| Escalier 5'-9½" (plan) | 386-456 × 440-494, descend vers la cour | **ouvert** : 6 girons de composite, 3 limons blancs crantés, pas de contremarches ; 7 contremarches de 7,07 po |
| Patio ±19' × 10' | 159-386 × 440-560 | au niveau du palier ; le coin x 314-386 × 494-560 porte le BBQ |
| Deck ±13' × 11'-9" | 159-314 × 560 jusqu'à la piscine (y 601 à gauche, 705 à droite) | même niveau |
| Piscine hors-terre **21'** (plan ; choix du client le 2026-11-02) | centre (188,4 ; 724,1), rayon hors tout 126 po (moindres carrés sur les 3 cotes du plan, décalée de 2 po vers la ligne oblique : section du 2026-11-02 « Piscine de 21 pi… ») | paroi grise lisse de 52 po, margelle gris pâle, eau turquoise, écumoire ; anneau de gravier gris pâle de 12 po ; assise nivelée à 48 |
| Garde-corps d'aluminium noir | couleurs du plan | **vert** : barreaux 36 po ; **rouge** : barreaux 48 po (deux côtés du deck, jusqu'à la piscine) ; **bleu** : **verre pur** 48 po sur pinces (3 panneaux) entre le patio et le deck, **portillon noir à barreaux** de 36 po à ferme-porte (x 274-310) |
| Jupe des terrasses | sous le palier, le patio et le deck, et sur la face x = 386 (vue à travers l'escalier ouvert) | déclin horizontal blanc |
| Gravier sous l'escalier | 386-445 × 440-526, bordure blanche au sud | gravier gris pâle |
| **Murets de soutènement** | le long de l'allée (445-457 × 380-548) et une aile le long de x (500-572 × 510-522) | blocs de béton gris pâle, de l'allée (≈ 3) à la cour (48), couronnement de 2 po |
| **Marches de pierre** | 6 grosses dalles, x ≈ 459-503, y 452 à 548 | pierre naturelle gris pâle, contremarches de 7½ po, du bout de l'allée jusqu'à la cour |
| Pas japonais | 2 dalles de 36 × 24 po du portillon en haut des marches de pierre jusqu'à la porte du garage | dalles blanc gris au ras du gazon |
| **Garage 13' × 17'** (le cabanon du plan, agrandi à la demande du client) | murs 355-511 × 621-825 ; toit 343-523 × 609-837 ; à 3'-0" des lignes de lot (arrière et x = 560) au débord du toit | dalle de béton au ras du gazon (48,5) ; planches verticales blanches ; toit 7/12, rives, gouttières et retours blancs ; **porte de garage noire de 8' × 7'** à 8 carreaux, centrée sur le mur avant, tournée vers la maison, dessinée **ouverte** ; dedans : contreplaqué, plafond à 7'-10" |
| Appareils de la piscine | thermopompe et filtre au sable sur une dalle de 3' × 6' à l'emplacement du plan (entre la piscine et le coin arrière gauche) | blanc gris ; à 41 po (1,04 m) de la paroi et à 3'-4" de la ligne arrière |
| Mobilier du patio | salon dans le coin x 177-272 × 441-540 ; BBQ contre le garde-corps de l'escalier | sectionnel en L en résine tressée anthracite à coussins blanc cassé, table à dessus de verre, 2 fauteuils, 2 poufs ; gros BBQ au gaz ; 2 palmiers en pots blancs |
| Corde à linge | du mur arrière (x 172, z 168-173) à un poteau près de la ligne oblique (-32 ; 770) | deux fils blancs ; le fil passe à 4 pi de la paroi de la piscine |
| **Clôture d'intimité de 6 pi** | à 2¼ po en dedans des lignes arrière, x = 560 et oblique ; fermetures vers la maison (section du 2026-11-02 « Piscine de 21 pi… ») | planches sur planches teintes brun, poteaux 4 × 4 aux 8 pi au plus, panneaux en escalier ; **deux portillons de 42 po** à quincaillerie noir mat, dessinés ouverts |

**La maison vue de dehors**

- **Brique rouge** sur le rez-de-chaussée, de 97 po jusqu'aux soffites (202). **Fondation** en crépi **blanc lisse**, de 97 po
  jusqu'au terrain (elle se voit sur 37 à 97 po selon le niveau). Les deux parements sont percés aux ouvertures de **notre
  proposition** (`maison.json` : largeur, centre, allège et hauteur de chaque fenêtre).
- **Fenêtres noires** : cadre, vitre, meneaux aux mêmes places qu'à l'intérieur (sections de `fenetres_video.py`, meneaux
  inégaux du bureau et du salon compris), allège de béton au RDC. Cadres noirs autour des portes.
- **Toit à deux versants 5/12** (fermes 5/12 du croquis de 2016) en bardeau gris anthracite : faîte selon x (y 190, z 294), débord
  de 16 po, **pignons blancs en déclin vertical** aux deux bouts. **Pignon avant** transversal 5/12 au-dessus de la partie droite
  de la façade (x 154 à 472, sommet ≈ 276), avec retours de corniche en boîte à ses pieds. **Appentis 3/12** sur l'entrée
  arrière, qui prolonge le pan arrière plus bas. Fascias, soffites, rives et gouttières blancs ; évent noir près du faîte.
  *Le moteur n'a que des formes verticales : les versants sont faits de rangs de 2 po (gradins de 4,8 po) ; les bouts des rangs
  sont blancs (pignons et rives).*
- **Cheminée** de brique sur le mur gauche (x -20 à 0, y 132 à 154, d'après le relevé ; la vidéo la met au même endroit), du sol
  jusqu'à 318 po (2 pi au-dessus du faîte), chapeau de béton.
- **Perron avant** en béton (relevé) sur l'excroissance du sous-sol, dessus à 98, recalé sur le plateau du devant : 5 contremarches
  de 7,9 po vers la rue, garde-corps noirs. Appliques murales près des deux portes.

**Le terrain (relief)**

- **Lignes de lot** : arrière et côtés relevés au plan DAG. Devant, on a prolongé avec le plan de 1957 : marge avant de 40 pi
  (rue à y = -480), ligne droite perpendiculaire à la rue, façade du lot de 57,23 pi, ligne gauche oblique.
- **Relief** (`EXTERIEUR["relief"]`, grille de 83 × 110 lignes, pas de 12 po près de la maison et de l'allée, 24 po ailleurs) :
  - **allée d'asphalte au niveau du sous-sol** collée à la fondation sur tout le côté droit (x 456-552) : -15 à la rue, -8 au coin
    avant, -2 devant la porte de côté (seuil à 0), +3 au coin arrière ; elle continue derrière la maison en couloir de 4 pi
    (x 457-505) jusqu'au pied des marches de pierre ;
  - **devant** : plateau à 59 devant la partie gauche (perron), **talus de gazon en S** de x 282 (59) à x 350 (16,5), **palier bas**
    à 16,5-17 devant la grande fenêtre et la fenêtre du sous-sol, puis une chute presque verticale jusqu'à l'allée (x 444 à 456) ;
    plateau et palier descendent doucement vers la rue (34 et 4 à la ligne avant) ;
  - **côté gauche** : 58 au coin avant, 52 devant les deux fenêtres du sous-sol (allège 56, sans margelle dans notre
    proposition : 4 po de dégagement), 56 au coin arrière ;
  - **cour** à 48 (pied de l'escalier, piscine, garage), qui monte doucement vers la ligne gauche (56 à x ≤ 0) ; l'assise de la
    piscine et son anneau de gravier sont nivelés à 48 (raccord de 3 pi) ;
  - à l'est du bout de l'allée, un gazon bas (3 à 5) avec des arbustes, retenu au sud par l'aile du muret.
- **Revêtements** drapés : allée d'asphalte, gravier sous l'escalier et autour de la piscine, pas japonais.
- **Trous** : l'emprise de la maison (corps, entrée arrière, perron, cheminée). Les **margelles** des fenêtres du sous-sol sont
  faites par le moteur d'après le relief : il n'en reste qu'à l'arrière (terrain à 48) ; devant et le long de l'allée, le terrain
  est sous l'allège (palier bas à 17, allée à 0) ; au côté gauche, le terrain est tenu à 52, sous l'allège de 56.
- **Arbres** : une lisière de grands feuillus au-delà de la ligne arrière, le long de la ligne gauche et au-delà de l'allée,
  quatre bouleaux derrière le garage, deux pins près du coin arrière droit, un petit arbre ornemental à l'avant gauche ; haie
  ou arbustes du voisin de l'autre côté de l'allée.

**Arrêts de visite dehors** : façade avant (comme la capture 01), façade avant de biais, l'allée, l'allée devant la porte de
côté, le bout de l'allée, les marches de pierre et le portillon, vue d'ensemble de la cour (du coin du fond), le patio, le deck
et la piscine, le garage agrandi et les pas japonais, dans le garage, la piscine vue de la cour, le portillon du côté gauche de
la maison. Leur z est lu dans le relief.

### Hypothèses (à confirmer)

1. **Niveaux du terrain** : lus sur la vidéo (capture 03 calée : seuil de la porte de côté à 0, bas de la brique à 97, ce qui
   concorde avec notre relevé à 0,2 po près). Tout ce qui n'est pas visible est **à valider sur place** : pente de l'allée entre
   le coin avant et la rue, niveau de la rue, forme du talus vers la rue, bord du palier bas sur l'allée (talus raide ou
   bordure ?), niveau du fond de la cour près de la ligne gauche.
2. **Porte de côté du sous-sol de plain-pied** sur l'allée (vidéo 03) : l'ancienne descente extérieure (6 marches, murets,
   garde-corps) est supprimée. Seuil à 0, asphalte à -2 : il faut sans doute un caniveau devant la porte, **à valider avec un
   professionnel** (drainage).
3. **Le « patio » est une terrasse surélevée** au niveau du palier (la vidéo le confirme).
4. **Hauteurs** : palier, patio et deck à 97½ (49½ po du sol de la cour). L'escalier fait 7 contremarches de 7,07 po et des girons
   de 9 po mesurés au plan. **Un giron de 9 po est court** : le code demande au moins 235 mm (9¼ po), et 10 po est plus
   confortable. Il faudrait alors une volée plus longue (environ 60 po) : à faire vérifier par DAG.
5. **Toit** : la forme vient de la vidéo (détail et incertitudes dans la section du 2026-11-02). Le bout gauche du toit ne se voit
   dans aucune capture.
6. **Fenêtres** : allège et hauteur lues dans `maison.json` pour chaque fenêtre (depuis le 2026-11-02, les 10 fenêtres visibles
   dans la vidéo en ont pris les dimensions, à la demande du client : `DESIGN_fenetres_video.md`) ; celles qui n'en ont pas
   gardent les valeurs de l'étage (sous-sol 56-86, RDC 34-82 au-dessus du plancher).
7. **Perron avant** : on ne connaît ni le nombre de marches ni leur direction. Elles sont dessinées droit vers la rue, avec un
   pied sur le plateau (≈ 59). Il n'y a plus de trottoir jusqu'à l'allée : il traverserait le talus. Accès à pied depuis l'allée
   (marches dans le talus ou allée vers la rue) : **à décider avec le client**.

### Code et réglementation (à valider avec la Ville et un professionnel)

- **Piscine** : le règlement québécois sur la sécurité des piscines résidentielles demande une enceinte de 1,2 m. Une porte
  d'enceinte doit avoir un **dispositif de sécurité passif** qui la referme et la verrouille toute seule (c'est la note du plan
  DAG). Les appareils doivent être à **plus de 1 m** de la paroi ou de l'enceinte : la vidéo les met à environ 0,7 m ; on les a
  placés à 1,04 m (41 po), à l'emplacement du plan. Il faut aussi éviter tout ce qui permet de grimper : jupe, garde-corps,
  appareils (détail et sources : section du 2026-11-02 « Piscine de 21 pi… »).
- **Garde-corps** : 36 po (900 mm) si la chute fait moins de 1,8 m, 42 po (1070 mm) au-delà. Ouvertures de moins de 100 mm.
  Il faut une main courante dans l'escalier. **Avec l'allée au niveau du sous-sol, le palier et l'escalier surplombent le bout
  de l'allée d'environ 95 po (2,4 m)** : le garde-corps côté allée (36 po au plan) devrait faire 42 po, à faire vérifier par DAG.
- **Murets de soutènement** d'environ 45 po : au-delà d'environ 1 m, un mur de soutènement peut demander un calcul d'ingénieur
  et un drain ; à valider.
- **Garage** à 3'-0" des lignes de lot, mesuré au débord du toit, comme au plan : la Ville demande 90 cm (3 pi). Écart avec la
  piscine, superficie, hauteur : section du 2026-11-02 « Piscine de 21 pi… ». Il faut un **permis** pour la piscine, le deck,
  le garage, la clôture et les murets.
- **Empattements** sous le palier, le patio et le deck : sous la ligne de gel ou sur pieux vissés (note de DAG : « selon la
  capacité portante du sol »).

### Coût (ordre de grandeur, à faire chiffrer)

C'est le projet de DAG : leur soumission fait foi. Ordres de grandeur pour se repérer (Côte-Nord, 2026, posé) :

- terrasses composites (palier, patio, deck, environ 330 pi²) avec escalier ouvert et jupe : 28 000 à 48 000 $ ;
- garde-corps d'aluminium (environ 55 pi l. à barreaux) et verre pur sur pinces avec portillon : 9 000 à 16 000 $ ;
- piscine hors-terre de 21 pi avec filtre, pompe, thermopompe, nivellement et gravier : 9 000 à 16 000 $ ;
- garage 13' × 17' avec dalle et porte de garage : 13 000 à 24 000 $ ;
- clôture de bois de 6 pi (environ 131 pi l.) et deux portillons : 5 000 à 11 000 $ (sources : section du 2026-11-02) ;
- murets de blocs (environ 25 pi l. sur 4 pi), marches de pierre, gravier et dalles : 8 000 à 16 000 $ ;
- allée d'asphalte jusqu'au fond (environ 1 100 pi²) : 5 000 à 9 000 $.

### Photos à demander au client (pour remplacer les hypothèses)

1. Les **quatre façades**, de loin et bien en face, surtout le **côté gauche** (bout du toit : pignon ou croupe ?).
2. Le **toit** : pignon avant, appentis de l'entrée arrière (hauteur du soffite), couleur du bardeau, gouttières.
3. Le **côté de l'allée** : pente de l'allée jusqu'à la rue, niveau devant la porte de côté, bord du palier bas, drain.
4. L'**arrière** tel qu'il est aujourd'hui : niveau du sol au pied du mur, arbres existants, clôture, corde à linge.
5. Le **perron avant** : nombre de marches, direction, garde-corps, accès depuis l'allée.
6. Le **certificat de localisation** (le plan DAG est dessiné dessus) : repérer les bornes avant de poser la clôture.

### Dans la visite

`python3 renovation/outils/generer_3d.py renovation/MAISON-18_deux_etages` : la visite dessine le terrain en relief, les
revêtements, la cour et la maison vue de dehors (brique, fondation, fenêtres en verre sombre, toit), sous le soleil du jour.

- **Marcher dehors** : on monte et on descend seul les marches (8 po au plus) et les pentes du terrain ; terrasses,
  garde-corps, murets, piscine, murs du garage, clôture, mobilier, murs de la maison et lignes de lot bloquent. On entre et on sort par la
  **porte avant** (perron), la **porte arrière** (palier du deck) et la **porte de côté du sous-sol** (de plain-pied sur
  l'allée) quand elles sont ouvertes.
- **Arrêts** : section « Extérieur » de la liste. Le petit plan montre le lot quand on est dehors.
- **Maquette** : vue « Extérieur » (la maison avec son toit au milieu de son lot).
- **Aperçu du relief** : `EXT_APERCU=1` ajoute des colonnes de 24 po qui montrent le relief et les revêtements (pour un moteur
  qui ne dessine pas le relief). Sans cette variable, les données restent propres.

Corrections faites aux données pour la marche (novembre 2026) : obstacles ajoutés (cheminée, garde-corps du perron et du côté
gauche du deck, bacs à plantes, tronc de l'arbre du devant) ; les prismes de gazon sont remplacés par le terrain du moteur.

### 2026-11-02 — Captures de la vidéo DAG

Le client a envoyé 12 captures nettes de la vidéo DAG (façade avant de face et de biais, coin avant droit avec l'allée, dessous
du deck, escalier et cabanon, deck et piscine, salon du patio, façade arrière, vue aérienne, vue du dessus). Deux analyses ont
comparé chaque capture au modèle (caméra de la capture 03 calée par moindres carrés ; capture 12 redressée sur le plan du deck) ;
on a vérifié chaque point sur les captures avant de le reprendre. Planche capture / rendu (12 vues, moteur figé de HEAD, relief
dessiné par le moteur) : `/tmp/claude-0/-home-user-lavoie-co/a2f554a7-a4f7-5946-bdd4-2eb9d5a22192/scratchpad/m18/ext_donnees/planche_comparaison.jpg`
(dossier de travail, hors dépôt). Données : 1 219 objets (environ 1 000 avant),
relief de 83 × 110 lignes ; avec `EXT_APERCU=1`, 3 298 colonnes d'aperçu en plus.

**Ce qui a changé, et pourquoi**

| Zone | Avant | Maintenant | Pourquoi (captures) |
|---|---|---|---|
| Toit | croupe 5/12 partout, petite croupe sur l'entrée arrière | **deux versants 5/12**, faîte selon x sur toute la longueur, **pignons blancs** aux deux bouts ; **pignon avant** transversal au-dessus de la partie droite de la façade ; **appentis 3/12** sur l'entrée arrière | 03 et 07 : grand pignon blanc sur tout le côté droit ; 10 et 11 : faîte presque aussi long que la maison ; 01, 02 : pignon blanc au-dessus du salon ; 11 : pan arrière prolongé plus bas au-dessus de l'entrée arrière, côtés en rives droites |
| Pignons | — | déclin vertical blanc à couvre-joints, rives et fascias blancs, retours de corniche en boîte | 01, 02, 03 |
| Appentis | — | pente 3/12 au lieu de 5/12, soffite à 189 | à 5/12, le fascia tomberait à ≈ 181, sous la tête de la fenêtre ouv-RDC-008 (185) et de la porte arrière (≈ 188 avec son cadre) ; la brique des murs de l'entrée arrière s'arrête sous ce soffite |
| Cheminée | jusqu'à 290 (sous le faîte), conduit | jusqu'à 318 (2 pi au-dessus du faîte), chapeau de béton | 01, 02 ; règle des 2 pi |
| Évent | ventilateur gris | évent noir à chapeau près du faîte, pan arrière, x ≈ 232 | 07, 09, 10 |
| Fondation | crépi beige texturé, 49 po visibles partout | **crépi blanc lisse**, jusqu'au relief : ≈ 38 à 45 po à gauche, ≈ 80 devant la partie droite, toute la hauteur le long de l'allée | 01, 02, 03, 11 |
| Terrain | plat à 48 | **relief** (voir « Le terrain ») : allée au niveau du sous-sol, talus en S, palier bas, cour à 48 | 01, 02, 03 (calée), 04, 12 |
| Porte de côté | descente extérieure de 6 marches, murets, garde-corps, trou dans le gazon | **de plain-pied** sur l'allée ; descente supprimée | 03 |
| Allée | boîte d'asphalte de la rue à y = 40, à 6 po de la fondation | asphalte drapé, collé à la fondation, jusqu'au fond (couloir de 4 pi derrière la maison) | 02, 03, 04, 12 |
| Muret | bordure de béton de 20 po au milieu du gazon | **murets de soutènement** en blocs gris pâle (≈ 45 po côté allée) le long de l'allée et en aile | 03, 04, 07, 12 |
| Marches de pierre | — (bande de roche à plat) | **6 grosses dalles** de pierre de l'allée à la cour | 02 à 05, 11, 12 |
| Escalier du deck | massif blanc fermé | **escalier ouvert** : girons beiges, limons blancs crantés, gravier dessous | 04 à 07 |
| Platelage | érable (lattes de bois franc) | composite beige clair uni à joints sombres, lames selon x | 08 à 12 |
| Verre et portillon | verre entre poteaux, main courante ; portillon vitré | **verre pur sur pinces**, sans poteaux ; **portillon noir à barreaux** | 08, 10, 11 |
| Piscine | 21 pi (cote du plan), 24 montants foncés, anneau de terrazzo | **15 pi** (186 po hors tout), paroi lisse, margelle gris pâle, eau turquoise, écumoire, anneau de gravier ; le deck s'arrête sur elle (y 675 à droite, 627 à gauche). *Remplacée le même jour par la piscine de 21 pi (choix du client).* | 12 redressée (recoupée sur 4 cotes du plan), 11, 07 |
| Appareils de piscine | dalle de 3' × 6', thermopompe foncée | thermopompe et filtre blanc gris sur le gazon, grille sur le dessus | 12 |
| Cabanon | portes doubles de grange, imposte, X ; lanterne ; dalle de 4 po ; toit 6/12 | **une porte de garage** de 8' × 7', 8 carreaux, écharpes en Λ ; pas de lanterne ; au ras du gazon ; toit 7/12, gouttières, retours | 03 à 07 |
| Pas japonais | 1,5 po hors sol | au ras du gazon (revêtements) | 05, 06 |
| Mobilier | table de 6 pi et 4 chaises, petit BBQ, 2 bacs | **salon modulaire** tressé anthracite à coussins blancs (sectionnel en L, table de verre, 2 fauteuils, 2 poufs), **gros BBQ**, 2 **palmiers** en pots blancs | 08 à 12 |
| Corde à linge | — | du mur arrière à un poteau au fond | 08 à 12 (la double ligne blanche n'est pas la ligne de lot) |
| Végétation | haie de cèdres de 6 pi, 6 épinettes, 3 bouleaux | **pas de haie** ; lisière de grands feuillus, bouleaux derrière le cabanon, 2 pins près de l'allée, arbre ornemental devant, clôture de bois au fond (*depuis : clôture de 6 pi sur les trois lignes*) | 01 à 12 |
| Arrêts de visite | z = 48 partout | z lu dans le relief ; ajout de « L'allée devant la porte de côté », « Façade avant de biais » et « Le bout de l'allée et les marches de pierre » ; « Façade avant » placé comme la capture 01 | — |
| Couleurs | — | asphalte, composite, blocs, pierre, gravier et dalles un peu plus foncés que les teintes lues sur la vidéo | au soleil, le moteur éclaircit beaucoup les surfaces horizontales : l'asphalte au soleil sort beige clair quelle que soit sa teinte (reflet du soleil sur les peintures), il n'est foncé qu'à l'ombre ; à signaler à l'agent du moteur |

**Ce qui reste à valider sur place**

- **Forme réelle du toit** : le bout gauche (pignon supposé, aucune capture ne le montre), la pente et la hauteur du pignon avant
  (263 à 282 selon la capture ; on a 276), la hauteur du soffite de l'appentis de l'entrée arrière et sa pente (3/12 supposé).
- **Niveaux** : rue et pente de l'allée devant la maison (-15 à la rue, extrapolé), drainage devant la porte de côté (seuil à 0,
  asphalte à -2), forme du talus vers la rue, bord du palier bas sur l'allée (chute de 25 po : talus raide ou bordure ?), niveau
  de la cour près de la ligne gauche (≈ 56 estimé ± 8 po), niveau le long du mur gauche (52 devant les fenêtres du sous-sol :
  s'il est plus haut, il faut des margelles).
- **Murets** : longueur réelle du muret le long de l'allée (depuis le coin de la maison ou seulement au pied de l'escalier),
  hauteur (≈ 45 po), aile le long de x, matériau (bloc architectural ou béton coulé) ; nombre et taille des dalles de pierre.
- **Garde-corps du palier côté allée** : 42 po plutôt que 36 (chute d'environ 95 po).
- ~~**Piscine** : 15 pi (vidéo) ou 21 pi (cote du plan) ?~~ **Réglé** : 21 pi (le client, 2026-11-02).
- **Garage et pas japonais** : la vidéo montrait le cabanon environ 2 pi plus près de la maison que le plan ; on garde le plan
  (coté sur le certificat de localisation), garage agrandi de 5 pi vers la maison et de 3 pi vers la piscine.
- Arbres et corde à linge : existants, chez le voisin ou ajoutés par DAG ? Les arbres de la vidéo sont génériques. La clôture est
  réglée (6 pi sur les trois lignes, le client, 2026-11-02) ; reste à savoir si celle du fond, dans la vidéo, existe et à qui elle est.

**Écarts voulus avec la vidéo (on ne les copie pas)**

- **Fenêtres et portes** : elles suivent **notre proposition** (`maison.json`), lue à chaque génération ; ces données ne les
  copient pas de la vidéo. Le même jour, le client a demandé que les 10 fenêtres visibles prennent les dimensions de la vidéo :
  c'est fait dans `fenetres_video.py` (largeur, allège, tête à 80 po du plancher, sections), et l'extérieur suit. Il reste des
  écarts voulus : le **soffite reste à 202** (plafond du RDC à 201 ; dans la vidéo, le mur est plus bas et les têtes touchent le
  soffite, brique jusqu'à ≈ 194), les fenêtres que la vidéo ne montre pas gardent leurs valeurs (mur gauche, chambre 1 du
  sous-sol, dont la 2e fenêtre que la vidéo a omise et que le client confirme), et les **portes** restent celles de la
  maquette (la vidéo a une porte avant noire vitrée pleine hauteur et une porte de côté noire à demi vitrée).
- **Perron avant** : on garde celui du **relevé** (la vidéo n'en montre pas), recalé sur le plateau (5 contremarches).
- **Brique** : la vidéo a une brique rouge orangé plus vive ; la teinte est réglée dans le catalogue du moteur (pas dans ces
  données). À signaler si le client la trouve trop sombre.
- **Garage et pas japonais** : position du plan (voir plus haut), garage agrandi de 5 pi vers la maison et de 3 pi vers la piscine.

### 2026-11-02 — Piscine de 21 pi, clôture et garage agrandi (réponses du client)

**Demandes du client** (mot pour mot) : « piscine 21 pieds, pi oui met cloture tu avais le plan cadastre » ; « Je veux que tu
grossisse aussi le garage de 5 pieds par en avant et de 3 pieds côté piscine. » Le « garage », c'est le cabanon à porte de
garage du plan DAG ; « en avant », c'est vers la maison (sa porte y fait face) ; « côté piscine », c'est vers x bas.

**Ce qui change, et pourquoi**

| Élément | Avant | Maintenant | Pourquoi |
|---|---|---|---|
| Piscine | 15 pi (vidéo), centre (219 ; 699) | **21 pi** hors tout (rayon 126 po), centre (188,4 ; 724,1), paroi de 52 po | choix du client ; position par les cotes du plan (plus bas) |
| Deck | 159-314 × 560-675 | 159-314 × 560 jusqu'à la piscine (11'-9" au plan) : il s'arrête sur elle à y 601 à gauche et 705 à droite ; garde-corps de 48 po de chaque côté jusqu'à la piscine | plan DAG (le deck a été dessiné pour la 21 pi) |
| Anneau de gravier | rayon 103 | rayon 138 (12 po autour de la paroi) | plan |
| Terrain sous la piscine | pente vers la ligne gauche (jusqu'à 52 sous la paroi) | assise et gravier **nivelés à 48**, raccord de 3 pi | une piscine se pose de niveau ; la paroi garde 1,28 m partout (il faut 1,2 m sans enceinte) |
| Appareils | sur le gazon, côté x bas | dalle de 3' × 6' à l'emplacement du plan, à 41 po (1,04 m) de la paroi et 3'-4" de la ligne arrière ; écumoire de leur côté | plan ; règlement (plus de 1 m) |
| Corde à linge | poteau à (0 ; 855) | poteau à (-32 ; 770) | avec la 21 pi, le fil passait à 6 po de la paroi et au-dessus des appareils ; il passe maintenant à 4 pi de la paroi |
| Garage | 10' × 12' (391-511 × 681-825), bloc plein, porte fermée | **13' × 17'** (355-511 × 621-825), murs minces, porte ouverte, dalle où l'on marche | demande du client ; l'aménagement intérieur viendra après |
| Pas japonais | 3 dalles vers l'ancien cabanon | 2 dalles du portillon (haut des marches de pierre) à la porte du garage, sans y entrer | le garage avance de 5 pi : il ne reste que 5'-10" entre les marches et la porte |
| Clôture | un pan de 6 pi sur la ligne arrière, « à valider » | **clôture de 6 pi** sur les trois lignes et fermetures vers la maison, deux portillons | demande du client |
| Escalier du deck, côté allée | ouvert sous la main courante | jupe blanche du muret jusque sous les girons, comme sous le palier | sinon un enfant passe sous la main courante, descend le muret et sort de la cour |

**Position de la piscine.** Le plan donne trois cotes : 6'-2 5/8" du mur du cabanon (l'ancien, x = 391) à la piscine, 9'-10 3/8"
de la piscine à la ligne oblique, 3'-4 1/4" de la piscine à la ligne arrière. Résolues par moindres carrés avec un rayon hors
tout de 126 po : centre (190,4 ; 724,1), les trois cotes tombent à 0,04 po près (le centre lu au pixel sur le plan est à
(190,7 ; 724,8)). Avec le garage agrandi de 3 pi vers la piscine (mur à x = 355), la paroi serait à 38,6 po (0,98 m) du mur.
**On a décalé la piscine de 2 po vers la ligne oblique** : 40,6 po (1,03 m) entre le mur du garage et la paroi, 9'-8 3/8"
jusqu'à la ligne oblique, 3'-4 3/8" jusqu'à la ligne arrière. Le deck s'arrête toujours sur elle (son coin droit touche la paroi
à 0,4 po près ; au-delà de 3 po de décalage, il faudrait redessiner le deck). Le débord du toit du garage est à 28,6 po
(0,73 m) de la paroi, à 8 pi de haut.

**Le garage 13' × 17'.** Murs 355-511 × 621-825 (156 × 204 po, 221 pi², 20,5 m²), toit 343-523 × 609-837 (débord de 12 po),
toujours à 3'-0" des lignes de lot côté arrière et côté x = 560 (mesuré au débord, comme au plan). Même style que le cabanon
de la vidéo : planches verticales blanches à couvre-joints, toit 7/12 à pignon vers la maison, faîte à 12'-4" du sol
(3,76 m), gouttières et retours blancs, **porte de garage noire de 8' × 7' à 8 carreaux, centrée sur le nouveau mur avant**
(x 385-481). Pour l'agent qui aménagera l'intérieur, la porte est dessinée **ouverte** (panneau relevé à l'horizontale sous le
plafond, de y 627 à 711, sur ses rails noirs, arbre des ressorts au-dessus de l'ouverture) ; la dalle de béton (48,5, au ras du
gazon) est un plancher où l'on marche ; les murs sont minces (5 po : parement blanc dehors, contreplaqué dedans) ; plafond de
contreplaqué à 7'-10" ; un plafonnier. Intérieur fini : 146 × 194 po (12'-2" × 16'-2"). Constantes en tête d'`exterieur.py` :
`CAB`, `CAB_TOIT`, `CAB_EP`, `CAB_INT`, `CAB_Z_DALLE`, `CAB_H_MURS`, `CAB_Z_PLAFOND`, `CAB_PORTE`, `CAB_Z_PANNEAU`. Arrêts « Le
garage agrandi et les pas japonais » et « Dans le garage (vers la porte ouverte) ». À garder pour l'aménagement : rien de fixe
qui permette de grimper sur le mur côté piscine, dehors (pas de bac, de corde de bois ni d'échelle accrochée), et pas de fenêtre
de ce côté sans vérifier la bande de 1 m (règlement, plus bas).

**La souffleuse.** Le garage est au niveau de la cour (48) ; l'allée est 45 po plus bas, au bout de 6 marches de pierre de
7½ po (girons de 15½ po, pente de 48 %). Une souffleuse (90 à 150 kg) ne descend pas ces marches : **le trajet garage → allée ne
marche pas tel quel.** Deux solutions, non construites :
1. **La plus simple (recommandée)** : ranger la souffleuse au niveau de l'allée, dans un petit abri ou un coffre de 4' × 6' sur
   le gazon bas à l'est du bout de l'allée (x ≈ 505-552, y ≈ 400-500, à 3-5 po), là où elle sert. Une remise préfabriquée de
   15 m² et moins ne demande pas de permis à Baie-Comeau et ne compte pas dans la superficie des bâtiments accessoires (mais la
   Ville en permet 2 par terrain : garage + abri). Environ 1 500 à 3 500 $ (estimation).
2. **Une rampe** : 45 po à monter ; une souffleuse automotrice monte au plus environ 1:5 dans la neige, donc au moins 19 pi de
   rampe (≈ 225 po), le long de la ligne x = 560 du bout de l'allée (y ≈ 400) jusqu'à la cour (y ≈ 625), en refaisant l'aile du
   muret, avec un mur de soutènement côté allée et un garde-corps ; elle arriverait sur le côté du garage. Lourd (environ
   8 000 à 15 000 $, estimation) et elle prend le coin de la cour : on ne la recommande pas.

**La clôture.** Clôture d'intimité en bois de 6 pi comme celle du fond de la vidéo (capture 08) : planches sur planches teintes
brun (fermée des deux côtés), chapeau, poteaux 4 × 4 aux 8 pi au plus (23 poteaux). Elle est **posée à 2¼ po en dedans des
lignes de lot** (axe à 4 po, face extérieure des poteaux à 2¼ po). Elle **suit le relief en escalier** : chaque panneau est
horizontal, son bas est à 1½ po du point bas sous lui (jamais plus de 4 po de vide), le dessus est à 6 pi de ce point bas
(la cour descend de 56 à 48 le long de la ligne arrière). Tracé (axe, pouces) :

| Tronçon | De → à | Longueur |
|---|---|---|
| Côté gauche, le long de la ligne oblique | (-72 ; 372) → coin arrière gauche (-39,7 ; 898,8) | 44'-0" (6 baies) |
| Arrière | (-39,7 ; 898,8) → coin arrière droit (556 ; 867,2) | 49'-8" (7 baies) |
| Côté droit, le long de la ligne x = 560 | (556 ; 867,2) → (556 ; 553) | 26'-2" (4 baies) |
| Fermeture devant le garage, côté allée | y = 553, de x = 556 à 501 | 4'-7" |
| **Portillon de l'allée** | y = 553, ouverture x 456½ à 499½, en haut des marches de pierre | 42 po |
| Sur le muret de l'allée | x = 454,75 (dans l'axe du garde-corps de l'escalier du deck), de y = 553 à 497 | 4'-8" |
| Fermeture à gauche de la maison | y = 372 (8 po devant le coin arrière), de la ligne oblique (x = -72) à x = -48,5 | 2'-0" |
| **Portillon du côté gauche** | y = 372, ouverture x -46¾ à -4¼, poteau des pentures contre la brique (x = -2,5) | 42 po |

Environ **131 pi linéaires** de clôture, plus les deux portillons. À droite, la cour est fermée par le palier et l'escalier du
deck (garde-corps, jupe), la clôture posée sur le muret de l'allée, le portillon et la clôture qui rejoint la ligne x = 560 : le
gazon bas et l'aile du muret restent dehors. **Rien de haut dans la cour avant** : la clôture s'arrête derrière la maison des
deux côtés. Elle ne traverse ni muret, ni marches, ni garage, ni tronc, ni le poteau de la corde à linge ; elle est posée
**sur** le couronnement du muret de l'allée sur 4'-8" (poteaux sur bases d'acier noires fixées au muret, à faire valider par
l'entrepreneur). La haie et les arbustes du voisin, de l'autre côté de l'allée, sont gardés.

**Les portillons** (42 po, mêmes planches, deux traverses et une écharpe côté cour) : pentures en T, loquet à gravité à 54 po
(hors de portée des petits de 4 et 6 ans) et poignée, **noir mat**. Dessinés ouverts : celui de l'allée s'ouvre vers la cour et
se rabat à plat contre la clôture (180°, pentures sur le poteau de droite) ; celui de gauche s'ouvre de 90° vers la cour,
pentures du côté de la maison. Des pentures à ressort (fermeture automatique) sont un bon ajout avec deux jeunes garçons.
Arrêts « Le bout de l'allée, les marches de pierre et le portillon » et « Le portillon du côté gauche de la maison ».

**Règlements (à confirmer au permis)**

- **Clôture, Ville de Baie-Comeau** (règlement de zonage 2003-644 ; page résidentielle de la Ville) : **2 m (6'-6") au plus en
  cour latérale et arrière**, 1 m en cour avant, 1,2 m en cour riveraine ; permis requis (30,40 $). Notre clôture : 6 pi
  (1,83 m), rien en cour avant. Matériaux interdits : assemblages de tuyaux, de panneaux de bois, de fibre de verre, de déclin de
  vinyle ou de matériaux non ornementaux, broche carrelée, barbelé, mailles de chaîne non enduites. Nos planches sur planches ne
  sont pas des « panneaux de bois » au sens de la Ville (contreplaqué), mais c'est à confirmer au permis.
  Source : [Ville de Baie-Comeau — Clôture et haies, réglementation résidentielle](https://www.ville.baie-comeau.qc.ca/services/reglementation/permis-et-urbanisme/besoin-dinformation/cloture-et-haies-vegetales/reglementation-residentielle-cloture-et-haies-vegetales/).
- **Garage ou remise, Ville de Baie-Comeau** : au plus **60 m² (645 pi²)** pour l'ensemble des garages et remises (50 m² s'il y
  a déjà un garage attenant ou un abri d'auto), et au plus 15 % du terrain ; 2 bâtiments au plus par terrain ; 90 cm des lignes
  de lot ; 2 m de la maison ; hauteur de 4,25 m au plus, sans dépasser la maison. Distance d'une piscine : **1 m pour une
  remise** (36 m² au plus, rangement, pas d'automobile), **1,5 m pour un garage isolé** (stationnement de véhicules). Notre
  garage : 20,5 m², faîte à 3,76 m, 3'-0" des lignes, 20 pi de la maison ; 1,03 m de la piscine. Sources :
  [Garage isolé](https://www.ville.baie-comeau.qc.ca/services/reglementation/permis-et-urbanisme/besoin-dinformation/garage-isole/reglementation-residentielle-garage-isole/),
  [Remise](https://www.ville.baie-comeau.qc.ca/services/reglementation/permis-et-urbanisme/besoin-dinformation/remise/reglementation-residentielle-remise/).
- **Piscine, Règlement sur la sécurité des piscines résidentielles** (Québec ; la Ville l'applique, permis de 50,65 $) : une
  hors-terre dont la paroi fait **au moins 1,2 m** n'a pas besoin d'enceinte si l'on y accède depuis une terrasse rattachée à la
  maison dont la partie qui ouvre sur la piscine est protégée par une enceinte (ici : verre pur et portillon à fermeture et
  verrouillage automatiques). Les appareils doivent être à **plus de 1 m** de la paroi. Une **bande de dégagement de 1 m**
  autour de la paroi ne doit contenir aucune structure ni équipement fixe qui permette de grimper (mur de soutènement, module de
  jeux…) ni fenêtre (sauf exceptions). Ici : paroi à 1,28 m, appareils à 1,04 m, mur du garage à 1,03 m, poteau de la corde à
  2,5 m. La clôture de la cour n'est pas l'enceinte de la piscine. Sources : [Ville de Baie-Comeau — Piscine résidentielle](https://www.ville.baie-comeau.qc.ca/services/reglementation/permis-et-urbanisme/besoin-dinformation/piscine-hors-terre-residentielle/),
  [document-synthèse du MAMH, juin 2025](https://www.ville.baie-comeau.qc.ca/wp-content/uploads/2025/06/Document-synthese-a-lintention-des-citoyens_Juin-2025.pdf).

**Coûts (fourchettes, Côte-Nord 2026, posé, taxes en sus ; à faire chiffrer)**

| Poste | Fourchette | D'où ça vient |
|---|---|---|
| Piscine hors-terre de 21 pi, filtre, pompe, thermopompe, nivellement, gravier | 9 000 à 16 000 $ | piscine de 12 à 27 pi : 4 000 à 12 000 $, installation ≈ 1 200 $ ([Noovo Moi](https://www.noovomoi.ca/style-et-maison/maison/article.voici-le-guide-complet-sur-les-couts-l-installation-et-l-entreti.1.12866778.html)) ; thermopompe et dalle en plus |
| Garage 13' × 17' (221 pi²) avec dalle, porte de garage 8' × 7', contreplaqué dedans | 13 000 à 24 000 $ | structure de bois 35 à 65 $/pi² ([Soumission Rénovation, garage détaché 2026](https://soumissionrenovation.ca/fr/blogue/prix-dun-garage-detache-au-quebec-en-2026-couts-options-et-budget-a-prevoir)), plus dalle (3 000 à 5 000 $) et porte (1 500 à 3 000 $) ; environ 3 000 à 8 000 $ de plus que le cabanon de 10' × 12' |
| Clôture de bois de 6 pi, 131 pi l., deux portillons noir mat | 5 000 à 11 000 $ | bois 20 à 70 $/pi l. selon la qualité ([Soumission Rénovation, prix des clôtures](https://soumissionrenovation.ca/fr/blogue/prix-differents-types-clotures)) ; 35 à 70 $/pi l. pour de l'intimité de 6 pi, plus 600 à 1 500 $ de portillons |
| Abri pour la souffleuse au bout de l'allée (option 1) | 1 500 à 3 500 $ | estimation (remise préfabriquée de 4' × 6' et son assise) |
| Permis (piscine, garage, clôture) | ≈ 130 $ | tarifs de la Ville (50,65 + 50,65 + 30,40 $) |

**Rendus** (visite générée le 2026-11-02, dossier de travail, hors dépôt :
`/tmp/claude-0/-home-user-lavoie-co/a2f554a7-a4f7-5946-bdd4-2eb9d5a22192/scratchpad/m18/ext21/a/`) : `vue_deck_piscine.png` (du
patio, par le portillon du deck), `vue_ensemble_cour.png` (vue surélevée de 12 pi depuis le côté gauche de la cour),
`vue_garage.png` (porte ouverte, depuis le pied de l'escalier du deck), `vue_portillon_gauche.png` (depuis la cour),
`vue_portillon_allee.png` (depuis le bout de l'allée).

**Points à valider (décisions du client)**

1. **Garage ou remise ?** Rangement seulement (souffleuse, vélos, tondeuse, pas d'auto) : la Ville le traite comme une remise et
   1 m de la piscine suffit (on a 1,03 m). Si elle le classe « garage isolé », il faut 1,5 m : on peut (a) n'agrandir que de
   1'-3" côté piscine au lieu de 3 pi (garage 11'-3" × 17'), (b) décaler la piscine de 19 po de plus vers la ligne oblique et
   faire redessiner le deck par DAG, ou (c) demander une dérogation mineure. À demander au Service de l'urbanisme avec le permis.
2. **Débord du toit côté piscine** à 0,73 m de la paroi, à 8 pi de haut : on ne peut pas y grimper depuis la piscine, mais
   l'inspecteur peut le compter dans la bande de 1 m ; on peut le réduire à 6 po de ce côté.
3. **Souffleuse** : abri au bout de l'allée (recommandé) ou rampe (lourde).
4. **Bornes du lot** à repérer avant la clôture (certificat de localisation) ; savoir si la clôture du fond de la vidéo existe et
   si elle est au voisin (alors on la garde, et la nôtre s'arrête aux coins).
5. **Clôture sur le muret de l'allée** : fixation des poteaux au couronnement (ou poteaux derrière le muret), à voir avec
   l'entrepreneur.
6. **Nivellement** sous la piscine : déblai d'environ 4 po au coin gauche de l'anneau de gravier.
7. Électricité vers le garage et les appareils de la piscine (conduit enterré) : électricien.

**Aménagement intérieur du garage (2026-11-02)** : atelier, vélos, mur de bacs et place de la souffleuse, dans `garage.py`
(chargé par `exterieur.py`) ; programme, plan coté, coûts et points à valider dans **DESIGN_garage.md**.
