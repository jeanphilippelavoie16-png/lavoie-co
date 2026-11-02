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
| **Plan d'aménagement de la cour arrière, DAG, 17-12-2025**, éch. 3/16" = 1'-0" (`plan_cour-1.png`, 150 ppp) | Position et dimensions du palier, de l'escalier, du patio, du deck, du cabanon et des pas japonais ; couleurs des garde-corps ; lignes de lot arrière et côtés |
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
| Deck | 159-314 × 560-675, il s'arrête sur la piscine | même niveau |
| Piscine hors-terre **15'** (vidéo ; le plan dit 21') | centre (219 ; 699) ; son bord est aligné sur le côté x = 314 du deck | paroi grise lisse de 52 po, margelle gris pâle, eau turquoise, écumoire ; anneau de gravier gris pâle |
| Garde-corps d'aluminium noir | couleurs du plan | **vert** : barreaux 36 po ; **rouge** : barreaux 48 po (deux côtés du deck, jusqu'à la piscine) ; **bleu** : **verre pur** 48 po sur pinces (3 panneaux) entre le patio et le deck, **portillon noir à barreaux** de 36 po à ferme-porte (x 274-310) |
| Jupe des terrasses | sous le palier, le patio et le deck, et sur la face x = 386 (vue à travers l'escalier ouvert) | déclin horizontal blanc |
| Gravier sous l'escalier | 386-445 × 440-526, bordure blanche au sud | gravier gris pâle |
| **Murets de soutènement** | le long de l'allée (445-457 × 380-548) et une aile le long de x (500-572 × 510-522) | blocs de béton gris pâle, de l'allée (≈ 3) à la cour (48), couronnement de 2 po |
| **Marches de pierre** | 6 grosses dalles, x ≈ 459-503, y 452 à 548 | pierre naturelle gris pâle, contremarches de 7½ po, du bout de l'allée jusqu'à la cour |
| Pas japonais | 3 dalles de 36 × 24 po entre le pied de l'escalier et le cabanon (plan) | dalles blanc gris au ras du gazon |
| Cabanon 10' × 12' | murs 391-511 × 681-825 ; toit 379-523 × 669-837 (plan) | au ras du gazon ; planches verticales blanches ; toit 7/12, rives, gouttières et retours blancs ; **une porte de garage noire de 8' × 7'** à 8 carreaux et écharpes en Λ, tournée vers la maison |
| Appareils de la piscine | thermopompe et filtre au sable sur le gazon, côté x bas de la piscine | blanc gris ; à plus de 1 m de la paroi |
| Mobilier du patio | salon dans le coin x 177-272 × 441-540 ; BBQ contre le garde-corps de l'escalier | sectionnel en L en résine tressée anthracite à coussins blanc cassé, table à dessus de verre, 2 fauteuils, 2 poufs ; gros BBQ au gaz ; 2 palmiers en pots blancs |
| Corde à linge | du mur arrière (x 172, z 168-173) à un poteau au fond (0 ; 855) | deux fils blancs |
| Clôture de bois | sur la ligne arrière | planches de 6 pi, poteaux tous les 8 pi |

**La maison vue de dehors**

- **Brique rouge** sur le rez-de-chaussée, de 97 po jusqu'aux soffites (202). **Fondation** en crépi **blanc lisse**, de 97 po
  jusqu'au terrain (elle se voit sur 37 à 97 po selon le niveau). Les deux parements sont percés aux ouvertures de **notre
  proposition** (`maison.json`).
- **Fenêtres noires** : cadre, vitre, meneaux sur les grandes baies, allège de béton au RDC. Cadres noirs autour des portes.
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
- **Relief** (`EXTERIEUR["relief"]`, grille de 85 × 113 lignes, pas de 12 po près de la maison et de l'allée, 24 po ailleurs) :
  - **allée d'asphalte au niveau du sous-sol** collée à la fondation sur tout le côté droit (x 456-552) : -15 à la rue, -8 au coin
    avant, -2 devant la porte de côté (seuil à 0), +3 au coin arrière ; elle continue derrière la maison en couloir de 4 pi
    (x 457-505) jusqu'au pied des marches de pierre ;
  - **devant** : plateau à 59 devant la partie gauche (perron), **talus de gazon en S** de x 282 (59) à x 350 (16,5), **palier bas**
    à 16,5-17 devant la grande fenêtre et la fenêtre du sous-sol, puis une chute presque verticale jusqu'à l'allée (x 444 à 456) ;
    plateau et palier descendent doucement vers la rue (34 et 4 à la ligne avant) ;
  - **côté gauche** : 58 à l'avant, 56 au coin arrière ;
  - **cour** à 48 (pied de l'escalier, piscine, cabanon), qui monte doucement vers la ligne gauche (56 à x ≤ 0) ;
  - à l'est du bout de l'allée, un gazon bas (3 à 5) avec des arbustes, retenu au sud par l'aile du muret.
- **Revêtements** drapés : allée d'asphalte, gravier sous l'escalier et autour de la piscine, pas japonais.
- **Trous** : l'emprise de la maison (corps, entrée arrière, perron, cheminée). Les **margelles** des fenêtres du sous-sol sont
  faites par le moteur d'après le relief : il n'en reste qu'au côté gauche et à l'arrière (terrain à 48-58) ; devant et le long de
  l'allée, le terrain est sous l'allège (palier bas à 17, allée à 0).
- **Arbres** : une lisière de grands feuillus au-delà de la ligne arrière, le long de la ligne gauche et au-delà de l'allée,
  quatre bouleaux derrière le cabanon, deux pins près du coin arrière droit, un petit arbre ornemental à l'avant gauche ; haie
  ou arbustes du voisin de l'autre côté de l'allée.

**Arrêts de visite dehors** : façade avant (comme la capture 01), façade avant de biais, l'allée, l'allée devant la porte de
côté, le bout de l'allée et les marches de pierre, vue d'ensemble de la cour, le patio, le deck et la piscine, le cabanon et
les pas japonais, la piscine vue de la cour. Leur z est lu dans le relief.

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
6. **Fenêtres** : allège et tête lues dans les scènes d'étage (sous-sol 56-86, RDC 34-82 au-dessus du plancher), sauf les
   fenêtres agrandies vers le bas : leur allège propre est lue dans `maison.json` (sous-sol à 40, salon à 20).
7. **Perron avant** : on ne connaît ni le nombre de marches ni leur direction. Elles sont dessinées droit vers la rue, avec un
   pied sur le plateau (≈ 59). Il n'y a plus de trottoir jusqu'à l'allée : il traverserait le talus. Accès à pied depuis l'allée
   (marches dans le talus ou allée vers la rue) : **à décider avec le client**.

### Code et réglementation (à valider avec la Ville et un professionnel)

- **Piscine** : le règlement québécois sur la sécurité des piscines résidentielles demande une enceinte de 1,2 m. Une porte
  d'enceinte doit avoir un **dispositif de sécurité passif** qui la referme et la verrouille toute seule (c'est la note du plan
  DAG). Les appareils doivent être à **au moins 1 m** de la paroi ou de l'enceinte : la vidéo les met à environ 0,7 m ; on les a
  placés à 1,1 m. Il faut aussi éviter tout ce qui permet de grimper : jupe, garde-corps, appareils.
- **Garde-corps** : 36 po (900 mm) si la chute fait moins de 1,8 m, 42 po (1070 mm) au-delà. Ouvertures de moins de 100 mm.
  Il faut une main courante dans l'escalier. **Avec l'allée au niveau du sous-sol, le palier et l'escalier surplombent le bout
  de l'allée d'environ 95 po (2,4 m)** : le garde-corps côté allée (36 po au plan) devrait faire 42 po, à faire vérifier par DAG.
- **Murets de soutènement** d'environ 45 po : au-delà d'environ 1 m, un mur de soutènement peut demander un calcul d'ingénieur
  et un drain ; à valider.
- **Cabanon** à 3'-0" des lignes de lot, mesuré au débord du toit, comme au plan : marges du règlement de zonage de
  Baie-Comeau à vérifier. Il faut un **permis** pour la piscine, le deck, le cabanon et les murets.
- **Empattements** sous le palier, le patio et le deck : sous la ligne de gel ou sur pieux vissés (note de DAG : « selon la
  capacité portante du sol »).

### Coût (ordre de grandeur, à faire chiffrer)

C'est le projet de DAG : leur soumission fait foi. Ordres de grandeur pour se repérer (Côte-Nord, 2026, posé) :

- terrasses composites (palier, patio, deck, environ 330 pi²) avec escalier ouvert et jupe : 28 000 à 48 000 $ ;
- garde-corps d'aluminium (environ 55 pi l. à barreaux) et verre pur sur pinces avec portillon : 9 000 à 16 000 $ ;
- piscine hors-terre de 15 pi avec filtre, pompe et thermopompe : 7 000 à 12 000 $ ;
- cabanon 10' × 12' avec porte de garage : 10 000 à 16 000 $ ;
- murets de blocs (environ 25 pi l. sur 4 pi), marches de pierre, gravier et dalles : 8 000 à 16 000 $ ;
- allée d'asphalte jusqu'au fond (environ 1 100 pi²) : 5 000 à 9 000 $.

### Photos à demander au client (pour remplacer les hypothèses)

1. Les **quatre façades**, de loin et bien en face, surtout le **côté gauche** (bout du toit : pignon ou croupe ?).
2. Le **toit** : pignon avant, appentis de l'entrée arrière (hauteur du soffite), couleur du bardeau, gouttières.
3. Le **côté de l'allée** : pente de l'allée jusqu'à la rue, niveau devant la porte de côté, bord du palier bas, drain.
4. L'**arrière** tel qu'il est aujourd'hui : niveau du sol au pied du mur, arbres existants, clôture, corde à linge.
5. Le **perron avant** : nombre de marches, direction, garde-corps, accès depuis l'allée.
6. Le **certificat de localisation** : lignes de lot exactes, position du cabanon.

### Dans la visite

`python3 renovation/outils/generer_3d.py renovation/MAISON-18_deux_etages` : la visite dessine le terrain en relief, les
revêtements, la cour et la maison vue de dehors (brique, fondation, fenêtres en verre sombre, toit), sous le soleil du jour.

- **Marcher dehors** : on monte et on descend seul les marches (8 po au plus) et les pentes du terrain ; terrasses,
  garde-corps, murets, piscine, cabanon, mobilier, murs de la maison et lignes de lot bloquent. On entre et on sort par la
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
on a vérifié chaque point sur les captures avant de le reprendre. Planche capture / rendu :
`planche_comparaison.jpg` (dossier de travail de l'extérieur).

**Ce qui a changé, et pourquoi**

| Zone | Avant | Maintenant | Pourquoi (captures) |
|---|---|---|---|
| Toit | croupe 5/12 partout, petite croupe sur l'entrée arrière | **deux versants 5/12**, faîte selon x sur toute la longueur, **pignons blancs** aux deux bouts ; **pignon avant** transversal au-dessus de la partie droite de la façade ; **appentis 3/12** sur l'entrée arrière | 03 et 07 : grand pignon blanc sur tout le côté droit ; 10 et 11 : faîte presque aussi long que la maison ; 01, 02 : pignon blanc au-dessus du salon ; 11 : pan arrière prolongé plus bas au-dessus de l'entrée arrière, côtés en rives droites |
| Pignons | — | déclin vertical blanc à couvre-joints, rives et fascias blancs, retours de corniche en boîte | 01, 02, 03 |
| Appentis | — | pente 3/12 au lieu de 5/12, soffite à 189 | à 5/12, le fascia tomberait sous la tête de notre fenêtre ouv-RDC-008 (187) ; la brique des murs de l'entrée arrière s'arrête sous ce soffite |
| Cheminée | jusqu'à 290 (sous le faîte), conduit | jusqu'à 318 (2 pi au-dessus du faîte), chapeau de béton | 01, 02 ; règle des 2 pi |
| Évent | ventilateur gris | évent noir à chapeau près du faîte, pan arrière, x ≈ 232 | 07, 09, 10 |
| Fondation | crépi beige texturé, 49 po visibles partout | **crépi blanc lisse**, jusqu'au relief : ≈ 38 po à gauche, ≈ 80 devant la partie droite, toute la hauteur le long de l'allée | 01, 02, 03, 11 |
| Terrain | plat à 48 | **relief** (voir « Le terrain ») : allée au niveau du sous-sol, talus en S, palier bas, cour à 48 | 01, 02, 03 (calée), 04, 12 |
| Porte de côté | descente extérieure de 6 marches, murets, garde-corps, trou dans le gazon | **de plain-pied** sur l'allée ; descente supprimée | 03 |
| Allée | boîte d'asphalte de la rue à y = 40, à 6 po de la fondation | asphalte drapé, collé à la fondation, jusqu'au fond (couloir de 4 pi derrière la maison) | 02, 03, 04, 12 |
| Muret | bordure de béton de 20 po au milieu du gazon | **murets de soutènement** en blocs gris pâle (≈ 45 po côté allée) le long de l'allée et en aile | 03, 04, 07, 12 |
| Marches de pierre | — (bande de roche à plat) | **6 grosses dalles** de pierre de l'allée à la cour | 02 à 05, 11, 12 |
| Escalier du deck | massif blanc fermé | **escalier ouvert** : girons beiges, limons blancs crantés, gravier dessous | 04 à 07 |
| Platelage | érable (lattes de bois franc) | composite beige clair uni à joints sombres, lames selon x | 08 à 12 |
| Verre et portillon | verre entre poteaux, main courante ; portillon vitré | **verre pur sur pinces**, sans poteaux ; **portillon noir à barreaux** | 08, 10, 11 |
| Piscine | 21 pi (cote du plan), 24 montants foncés, anneau de terrazzo | **15 pi** (186 po hors tout), paroi lisse, margelle gris pâle, eau turquoise, écumoire, anneau de gravier ; le deck s'arrête sur elle (y 675 à droite, 627 à gauche) | 12 redressée (recoupée sur 4 cotes du plan), 11, 07 |
| Appareils de piscine | dalle de 3' × 6', thermopompe foncée | thermopompe et filtre blanc gris sur le gazon, grille sur le dessus | 12 |
| Cabanon | portes doubles de grange, imposte, X ; lanterne ; dalle de 4 po ; toit 6/12 | **une porte de garage** de 8' × 7', 8 carreaux, écharpes en Λ ; pas de lanterne ; au ras du gazon ; toit 7/12, gouttières, retours | 03 à 07 |
| Pas japonais | 1,5 po hors sol | au ras du gazon (revêtements) | 05, 06 |
| Mobilier | table de 6 pi et 4 chaises, petit BBQ, 2 bacs | **salon modulaire** tressé anthracite à coussins blancs (sectionnel en L, table de verre, 2 fauteuils, 2 poufs), **gros BBQ**, 2 **palmiers** en pots blancs | 08 à 12 |
| Corde à linge | — | du mur arrière à un poteau au fond | 08 à 12 (la double ligne blanche n'est pas la ligne de lot) |
| Végétation | haie de cèdres de 6 pi, 6 épinettes, 3 bouleaux | **pas de haie** ; lisière de grands feuillus, bouleaux derrière le cabanon, 2 pins près de l'allée, arbre ornemental devant, clôture de bois au fond | 01 à 12 |
| Arrêts de visite | z = 48 partout | z lu dans le relief ; ajout de « L'allée devant la porte de côté », « Façade avant de biais » et « Le bout de l'allée et les marches de pierre » ; « Façade avant » placé comme la capture 01 | — |

**Ce qui reste à valider sur place**

- **Forme réelle du toit** : le bout gauche (pignon supposé, aucune capture ne le montre), la pente et la hauteur du pignon avant
  (263 à 282 selon la capture ; on a 276), la hauteur du soffite de l'appentis de l'entrée arrière et sa pente (3/12 supposé).
- **Niveaux** : rue et pente de l'allée devant la maison (-15 à la rue, extrapolé), drainage devant la porte de côté (seuil à 0,
  asphalte à -2), forme du talus vers la rue, bord du palier bas sur l'allée (chute de 25 po : talus raide ou bordure ?), niveau
  de la cour près de la ligne gauche (≈ 56 estimé ± 8 po).
- **Murets** : longueur réelle du muret le long de l'allée (depuis le coin de la maison ou seulement au pied de l'escalier),
  hauteur (≈ 45 po), aile le long de x, matériau (bloc architectural ou béton coulé) ; nombre et taille des dalles de pierre.
- **Garde-corps du palier côté allée** : 42 po plutôt que 36 (chute d'environ 95 po).
- **Piscine** : 15 pi (vidéo) ou 21 pi (cote du plan) ? Tout en dépend : bout du deck, appareils, dégagements. **Le client ou DAG
  doit trancher.**
- **Cabanon et pas japonais** : la vidéo les montre environ 2 pi plus près de la maison que le plan ; on a gardé le plan (coté)
  tant que le certificat de localisation n'est pas là.
- Arbres, clôture du fond, corde à linge : existants, chez le voisin ou ajoutés par DAG ? Les arbres de la vidéo sont génériques.

**Écarts voulus avec la vidéo (on ne les copie pas)**

- **Fenêtres et portes** : on garde **notre proposition** (`maison.json`) : fenêtres du sous-sol et du salon agrandies vers le
  bas (allèges à 40 et 20), têtes à 86 et 187, soffite à 202 (plafond du RDC à 201). La vidéo a des têtes collées au soffite,
  une fenêtre avant du sous-sol d'environ 36 po, de plus petites fenêtres de côté au sous-sol, une porte avant noire vitrée
  pleine hauteur, une porte de côté noire à demi vitrée, et un avant-toit environ 8 po plus bas (brique jusqu'à ≈ 194).
- **Perron avant** : on garde celui du **relevé** (la vidéo n'en montre pas), recalé sur le plateau (5 contremarches).
- **Brique** : la vidéo a une brique rouge orangé plus vive ; la teinte est réglée dans le catalogue du moteur (pas dans ces
  données). À signaler si le client la trouve trop sombre.
- **Cabanon et pas japonais** : position du plan (voir plus haut).
