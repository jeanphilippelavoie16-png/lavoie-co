# MAISON-18 — Les deux étages réunis

Un seul projet pour toute la maison : le sous-sol de SS-17 (allégé) et le rez-de-chaussée réaménagé à partir du relevé photo RDC-01. Feuilles **P-129** (sous-sol) et **P-130** (rez-de-chaussée). La maquette `3d/visite.html` empile les deux étages : on monte et on descend par l'escalier (en marchant, ou avec le bouton « ▲ Monter / ▼ Descendre »), les arrêts de visite couvrent les deux étages, le mini-plan suit l'étage, et le mode maquette montre le sous-sol, le rez-de-chaussée ou les deux. Toutes les portes s'ouvrent et se ferment en les touchant.

## Demandes du client (2026-11-01)
- « Réaménage la chambre arrière, lit king mais rangement optimisé. »
- « Fusionne les plans pour qu'on puisse monter d'en bas à en haut. » — « Ajoute les marches en haut pour monter et descendre. »
- « Corrige les bugs en haut. »
- « Enlève les garde-robes en rouge en haut pour que ça fasse une grosse entrée, et entoure l'entrée de murs de verre côté cuisine et salon pour que ça soit comme isolé. Fais du rangement dans l'entrée en haut aussi. Fais de quoi de chic et fonctionnel. »
- « Dans les chambres en bas il y a comme trop de meubles, exagère pas. »
- « Arrange-toi que je puisse interagir avec les portes (ouvrir, fermer). »
- « La chambre avant devient un bureau de travail et de gaming (2 stations assis), idéalement face à la fenêtre qui a une vue vers le fleuve. »

Le reste du sous-sol est celui de SS-17 (voir `../SS-17_rangement_enfants_gym/DESIGN.md`) : bain et douche en travertin, béton poli, toile motorisée qui joue une émission, projecteur au plafond, galerie de photos, banc-cabane sous l'escalier, gym refait, casiers d'hiver.

Tout est une esquisse à valider avec la Ville de Baie-Comeau et un professionnel (structure de l'ouverture de l'escalier et de l'ancienne cloison hall/salon, coupe-feu entre logements, fenêtres d'évacuation, garde-corps).

## Rez-de-chaussée — grande entrée vitrée et escalier

### Entrée vitrée du rez-de-chaussée (module `rdc_entree.py`)

#### Demande du client
Annotations rouge et jaune sur la feuille P-128 de SS-17 (2026-11-01) :
« Enlève les garde-robes en rouge en haut pour que ça fasse une grosse entrée, et entoure l'entrée de murs de verre côté
cuisine et salon pour que ça soit comme isolé. Fais du rangement dans l'entrée en haut aussi. Fais de quoi de chic et
fonctionnel. » — « Ajoute les marches en haut pour monter et descendre. »

Lecture du croquis (vérifiée sur l'image et sur maison.json) : le trait rouge suit la cloison x = 175 de y ≈ 53 à 192,
c'est-à-dire toute la colonne de rangement entre la chambre avant et le hall (VEST., G.R. de la chambre avant, LIN.) ;
le trait jaune ferme l'entrée par un mur de verre horizontal vers y ≈ 172 (de x ≈ 162 à 305), qui tourne et descend
jusqu'au mur avant le long de l'escalier, côté salon (x ≈ 262 à 290).

#### Parti pris
Un vestibule de 124,7 pi² (12'-2" × 10'-3", trémie comprise), fermé par du verre clair plancher-plafond à cadres noirs
minces. À gauche, tout le mur du bureau devient un meuble d'entrée pleine hauteur (noir mat et chêne) ; à droite, le
haut de l'escalier derrière un garde-corps de verre ; au fond, la porte vitrée dans l'axe de la porte d'entrée : en
entrant, la vue traverse jusqu'à la salle à manger et la brique de la cuisine. L'hiver, l'entrée fait sas : la neige et
le froid restent entre la porte d'entrée et la porte vitrée.

#### Ce qui change sur le plan P-130
- **Enlevé** : les cloisons de la colonne de rangement `mur-RDC-014`, `-015`, `-016` (VEST., G.R., LIN.), la ligne de
  porte entrée / hall `mur-RDC-017` (et son ouverture `ouv-RDC-011`), la cloison hall / salon `mur-RDC-018` ; les portes
  `ouv-RDC-021` (G.R. qui ouvrait dans la chambre avant) et `ouv-RDC-022` (lingerie) ; `mur-RDC-012` est raccourci à
  x = 146 (la partie bureau / dégagement reste). La poutre apparente `str-RDC-R01`, qui coiffait le bout de la cloison
  hall / salon, n'a plus d'appui : retirée (décorative selon RDC-01 ; si elle se révèle porteuse, ingénieur).
  Tout est versé dans `murs_retires`, `ouvertures_retirees`, `structure_retiree`.
- **Murs de verre** (`materiau: verre`, 2 po) : `mur-RDC-E01` (x 146 → 224, y = 157) et `mur-RDC-E02` (x 232 → 272¼)
  côté logement, **sous la poutre de bois brut de l'axe B**, les poteaux C04 et C05 servant de montants ;
  `mur-RDC-E03` (x = 272¼, de y 157 au mur avant) côté salon, là où SS-17 mettait le mur de la cage : il sert aussi de
  garde du côté droit de la volée (verre trempé feuilleté obligatoire).
  - Écart avec le croquis : le verre est ≈ 15 po plus près de l'avant que le trait jaune (y = 157 au lieu de ≈ 172).
    Raison : il tombe exactement sous la poutre et entre les poteaux existants (aucune structure à toucher, pas de
    verre suspendu à un plafond plat à côté d'une poutre, poteau C05 pas planté seul au milieu de l'entrée).
    **Option B** : verre à y ≈ 172 comme le croquis (+ 13 pi² d'entrée, poteau C05 dans l'entrée, habillé de bois brut).
- **Porte vitrée** `ouv-RDC-E01` : battante, 36 po, x 186¾ → 222¾ (contre l'habillage du poteau C05), pentures côté
  poteau, ouvre vers le dégagement (on la pousse en entrant), ferme-porte doux, coupe-froid.
- **Pas de porte vers le salon** : le côté salon longe la volée sur toute sa longueur ; une porte y ouvrirait sur la
  trémie. Le salon est à deux pas de la porte vitrée par le dégagement, qui reste ouvert sur le salon et la cuisine.
- **Porte d'entrée** `ouv-RDC-010` : pentures à gauche (comme SS-17) : elle s'ouvre contre le banc et laisse le haut de
  l'escalier libre ; dessinée fermée dans la maquette (on l'ouvre en la touchant).
- **Escalier** : l'élément `elem-RDC-P-ESC` reporté du sous-sol (14 contremarches, 3 marches tournantes en haut, sortie
  vers l'ouest dans l'entrée, flèche DESCEND) n'est pas déplacé. Ajouts : `escalier.tremie` et `rdc["tremies"]` =
  [234, 14, 270, 134,7], soit la trémie que `generer_3d.py` calcule pour l'escalier du sous-sol.
- **Pièces** : une seule « Entrée » (`piece-RDC-ENT`, 124,7 pi²) remplace Entrée, Hall, Vest., G.R. et Lin. ; le Salon
  passe de 227,3 à 176,3 pi² (il commence au verre, x = 273¼) ; le Dégagement est recoupé au verre.
- **Éléments** : `elem-RDC-E-BANC` (libellé BANC), `-ARM1` et `-ARM2` (armoires, X), `-CONS` (niche-console),
  `-GC1` et `-GC2` (garde-corps, sans libellé) ; ils sont aux places exactes où le moteur pose son garde-corps.
- **Note du cartouche** : `note-RDC-E01` ajoutée (une ligne). Le cartouche n'en tient que 6 : à arbitrer à la fusion.

#### Rangement : chic et fonctionnel (mur du bureau, x = 148¼, de l'avant vers l'arrière, 144 po de long)
| Module | Où | Contenu |
|---|---|---|
| Banc à bottes, 54 × 18 po | y 10 → 64, contre la porte | Assise de chêne à 19 po avec coussin de cuir ; dessous, 3 cases à bottes avec bacs d'égouttement de caoutchouc (une case libre pour sécher) ; dossier de lattes de chêne ; crochets noirs **à 40 po pour les garçons** (5) et à 64 po pour les adultes (4) ; tablette de chêne à 72 po avec **4 bacs, un par membre de la famille** (tuques, mitaines, cache-cous) ; ruban DEL sous la tablette ; caisson fermé en haut (saison morte) |
| Armoire-vestiaire 1, 36 × 24 po | y 64 → 100 | Pleine hauteur, 2 portes noir mat, tirettes longues de chêne ; tringle double (manteaux d'hiver des parents), tablette |
| Niche-console, 24 × 24 po | y 100 → 124 | Niche ouverte doublée de chêne (37 à 76 po) : tablette-console pour les clés (plateau de cuir), **tiroir de recharge** (prises USB-C, téléphones et montres), miroir au fond, DEL ; armoires noires dessus et dessous (souliers, sacs) |
| Armoire-vestiaire 2, 30 × 24 po | y 124 → 154 | Pleine hauteur, 2 portes : manteaux des garçons (tringle basse réglable), sacs d'école, aspirateur, et le linge de la lingerie enlevée |

Passage libre entre les armoires et le garde-corps : 60 po (42 po porte d'armoire ouverte). Rien ne descend sous 80 po
au-dessus du passage (suspension globe : bas à 80 po).

Matériaux (style du client au RDC) : ardoise noire 24 po au sol, comme la cuisine, avec **tapis-grattoir encastré** à
fleur devant la porte ; caissons et portes **noir mat** (comme les armoires de cuisine), chêne pour le banc, les lattes,
la niche et les tirettes ; verre clair à cadres d'aluminium noir mat ; poutre et poteaux de bois brut gardés ; murs vert
sauge (existant). Éclairage : suspension globe opale au centre, 4 encastrés (2 au-dessus de l'escalier), applique noire
entre la porte et l'escalier, DEL sous la tablette du banc et dans la niche, veilleuse DEL au pied du garde-corps (sur
détecteur de mouvement : les garçons la nuit). Mobilier RDC-01 retiré de la zone : mur de cadres, banc blanc, vieille
porte, crochets, tapis ; le **sectionnel du client** (il passait sous la volée) est replacé 52 po plus loin, dos au mur
de verre, face à la télé.

#### Dégagements vérifiés (plan et maquette)
- Devant la porte d'entrée : x 182 → 216, y 10 → 52 libres (42 po), le tapis-grattoir est à fleur.
- Haut de l'escalier : palier x 192 → 234, y 14 → 50 libre (42 po devant la marche du haut, sortie vers l'ouest).
- Porte d'entrée ouverte : le vantail se range à x ≈ 182, à 16 po du banc ; elle ne balaie jamais la volée.

#### Escalier : échappée, largeur, garde (à valider)
- Largeur : 36 po (914 mm), au-dessus des 860 mm demandés dans un logement.
- Échappée : plafond du sous-sol à 96 po (8 pi, propriétaire), hauteur d'étage présumée 105 po (14 × 7½ po). Au bord de
  la trémie (y = 134,7), la ligne des nez est à 19 po : **77 po, soit 1,96 m, juste au-dessus du 1,95 m d'un logement**.
  Option : allonger la trémie de 6 po vers l'arrière (y ≈ 141) → environ 82 po (2,08 m) ; il reste 15 po jusqu'au verre.
- Garde-corps : 36 po (900 mm, minimum dans un logement), verre clair, poteaux d'acier noir, main courante de chêne
  (c'est celui que le moteur pose dans la maquette à deux étages). **Recommandé : 42 po (1 070 mm)** pour des garçons de
  4 et 6 ans, verre feuilleté sans traverse grimpable.
- Main courante : ronde, noire, côté salon, continue du palier jusqu'au sous-sol (34 à 38 po au-dessus des nez), le long
  du mur avant au droit des marches tournantes puis du verre, où elle rejoint celle du sous-sol.
- Marches tournantes en haut (3 × 30°) : admises dans un logement, giron et hauteur à valider avec l'escalier du sous-sol.

#### Accès aux autres pièces
- **Bureau (ex-chambre avant)** : sa porte (`ouv-RDC-014`, x ≈ 127 sur y = 157, côté dégagement) **n'est pas déplacée**.
  Il perd son garde-robe (le G.R. de la colonne ouvrait dans la chambre ; `ouv-RDC-021` est refermée) : l'agent bureau
  peut prévoir du rangement dans le bureau. Option non retenue : une porte directe entrée → bureau dans `mur-RDC-013`
  (le mur porte maintenant le vestiaire).
- Salle de bain, chambre arrière : inchangées, par le dégagement. La lingerie (21 po) disparaît : linge dans l'armoire 2.

#### Maquette 3D (`appliquer_scene_rdc`)
- Arrêts « Entrée vitrée » (départ de la visite du RDC), « Entrée vitrée — banc et vestiaire », « Entrée vitrée vue du
  dégagement » ; « Entrée avant » et « Hall (mur de cadres) » retirés ; « Salon vers le hall » renommé ; palette « Entrée
  vitrée » ; crépi du salon arrêté au verre ; lumières du hall remplacées.
- **À deux étages** (sans ETAGE) : le moteur troue le plancher du RDC à la trémie du sous-sol et pose le garde-corps ;
  l'escalier DESCEND du RDC n'est pas redessiné. Vérifié dans les données produites (trou, garde-corps, aucune marche).
- **À un seul étage** (ETAGE=RDC) : ce module dessine le même garde-corps et une trémie sombre avec les nez des marches.
  **À corriger côté moteur** : à un étage, `generer_3d.py` dessine encore `elem-RDC-P-ESC` comme un escalier qui
  MONTE (il ne saute les escaliers DESCEND que dans la maquette à deux étages). La trémie est aussi déclarée dans
  `SCENE["tremies_plancher"]` (clé demandée au moteur par l'agent corrections).

#### Coût (ordre de grandeur, estimation à confirmer par 2 ou 3 soumissions ; escalier exclu, déjà au budget du sous-sol)
| Poste | Fourchette |
|---|---|
| Démolition (garde-robes, lingerie, cloisons), reprise du gypse, du plancher et du plafond | 2 500 – 5 000 $ |
| Trémie : ouverture, chevêtres et solives doublées, plans d'ingénieur | 4 000 – 8 500 $ |
| Murs de verre plancher-plafond (≈ 17 m², cadres noirs) et porte vitrée | 12 000 – 22 000 $ |
| Garde-corps de verre (≈ 3 m) et main courante | 3 000 – 6 000 $ |
| Menuiserie sur mesure (banc, 2 armoires, niche-console, 12 pi pleine hauteur) | 9 000 – 16 000 $ |
| Ardoise (≈ 125 pi²) et tapis-grattoir encastré | 2 500 – 4 500 $ |
| Électricité (suspension, applique, encastrés, DEL, USB-C, interrupteurs à 3 voies) | 1 500 – 3 000 $ |
| **Total** | **≈ 35 000 – 65 000 $** |
Options : plancher chauffant électrique sous l'ardoise (+ 1 000 à 2 000 $) ; garde-corps de 42 po (+ 10 %).

#### Points à vérifier sur place
- Sens et grosseur des solives au-dessus de la trémie (chevêtres, appuis) ; hauteur réelle du plafond du sous-sol et
  épaisseur du plancher (105 po présumés) ; poutre `str-RDC-R01` décorative ou porteuse.
- Rien dans la colonne de garde-robes (conduits, plomberie, fils) ; position exacte des poteaux C04 et C05 (montants du verre).
- Prises et câblage : console (USB-C), DEL, suspension, applique ; interrupteurs à 3 voies en haut et en bas de l'escalier ;
  avertisseur de fumée au haut de l'escalier.
- Verre : trempé feuilleté là où il sert de garde (côté salon, garde-corps) ; buée l'hiver (ventilation de l'entrée).
- Séparation coupe-feu : si le sous-sol devenait un logement distinct, ni le verre ni la trémie ouverte ne conviennent.

Structure, échappée, garde-corps, verre et coupe-feu : **à valider avec la Ville et un professionnel**.

## Rez-de-chaussée — chambre des parents (lit king)

### Chambre des parents (chambre arrière du RDC) — « lit king, rangement optimisé »

Module : `rdc_chambre_arriere.py` (`appliquer_modifs_rdc` pour le plan P-130, `appliquer_scene_rdc` pour la maquette).

#### Demande
« Réaménage la chambre arrière, lit king mais rangement optimisé. » C'est la chambre des parents : un lit king
(matelas 76 × 80 po) avec 24 po de dégagement des deux côtés et 30 à 36 po au pied, du rangement « chic et
fonctionnel » sans surcharger la pièce. Aujourd'hui : lit queen tête au mur de la salle de bain, commode blanche, mur
en papier peint imitation planches, vélo de route sur base d'entraînement devant la fenêtre, deux petites garde-robes
(G.R. 1 et 2) à portes battantes qui ouvrent dans la chambre.

#### Contraintes relevées (maison.json)
| Élément | Position | Conséquence |
|---|---|---|
| Chambre (nu intérieur) | x 10 à 143¾, y 226 à 370 (12'-0" × 11'-1¾", ≈ 136 pi²), plus le retrait de la porte (x 110 à 144, y 214 à 226) | 134 po de large au total : un king (82 po avec la plateforme) + 2 × 24 po = 130 po, ça entre dans un seul sens sans toucher la porte |
| Fenêtre `ouv-RDC-003` | mur arrière (y = 370), 75 po de large, axe x = 98 (x 60½ à 135½), allège ≈ 34, tête ≈ 82 | ne pas la bloquer ; rien de plus haut que l'allège devant |
| Porte `ouv-RDC-016` | 30 po, dans le retrait (y = 212, x 112 à 142), ouvre dans la chambre, pentures côté x = 142 | son arc couvre x 112 à 142, y 212 à 242 : rien dedans |
| Portes des G.R. `ouv-RDC-019`, `ouv-RDC-020` | 2 × 28 po battantes sur `mur-RDC-021` (x = 146), arcs jusqu'à x ≈ 118 | elles mangeraient le dégagement au pied d'un king : on les remplace |
| Mur gauche `mur-RDC-004` | mur extérieur aveugle (x = 10) | le seul long mur plein, sans porte ni fenêtre : c'est le mur de tête |

#### Pourquoi la tête au mur gauche (orientations comparées)
- **Tête au mur de la salle de bain (comme aujourd'hui)** : un king centré laisse 29 po de chaque côté, mais le côté
  droit tombe dans le retrait de la porte et dans son arc (x 112 à 142). Refusé.
- **Tête sous la fenêtre (mur arrière)** : bloque la fenêtre, pas de mur de tête intégré possible, pied du lit à 65 po
  de la salle de bain mais rien ne s'y range. Refusé.
- **Tête au mur gauche (retenu)** : plateforme 84 × 82 po de x 21½ à 105½, y 257 à 339. **31 po de chaque côté,
  38¼ po au pied** (jusqu'à la façade de la garde-robe), l'arc de la porte reste libre, la fenêtre est sur le côté du lit
  (31 po de passage devant).

#### Ce qui change
**Plan P-130**
- Pièce renommée « Chambre des parents ». Éléments neufs : `LIT KING` (plateforme), mur de tête intégré (bande de 9 po
  le long du mur gauche), deux chevets suspendus, tour de tiroirs dans la garde-robe.
- **G.R. 1 et 2 réunies** : la cloison `mur-RDC-023` et les deux portes battantes `ouv-RDC-019` / `ouv-RDC-020` sont
  retirées (gardées dans `murs_retires` / `ouvertures_retirees`) ; nouvelle baie `ouv-RDC-CH1-GR` de 66 po (y 302 à
  368) à **deux portes coulissantes** de 34 po dans `mur-RDC-021` ; nouvelle pièce `piece-RDC-GRP` « G.R. » de
  24½ × 71¾ po (12,2 pi²). Plus aucun arc de porte dans la chambre, sauf celui de la porte d'entrée de la pièce.
- Note courte ajoutée au cartouche (`note-RDC-CH1-01`).

**Maquette 3D** (le mobilier RDC-01 de la chambre est retiré : lit queen, chevet, cadres, suspension cage, commode,
vélo et son tapis, store marine, papier peint, panier)
| Élément | Description |
|---|---|
| Mur de tête intégré | fourrure de 9 po devant le mur extérieur (l'isolant n'est pas touché), du plancher au plafond, en **vrai bois de grange** (le client aime le bois : on passe du papier peint imitation au vrai, comme les comptoirs de la cuisine) |
| Niches éclairées | 2 niches latérales noir mat de 20 × 32 po, 6 po de creux, DEL sous le dessus, **2 prises USB-C** au fond ; une niche-tablette horizontale de 84 × 10 po au-dessus de la tête de lit (livres, cadres), aussi éclairée |
| Tête de lit | rembourrée à 7 canaux verticaux (tissu gris pâle), 86 po de large, de 12 à 50 po de haut |
| Liseuses | 2 liseuses murales noires articulées, bras vers l'oreiller, interrupteur à portée de main |
| Chevets suspendus | noir mat, 22 × 16 po, un tiroir chacun, dessus à 25 po (à la hauteur du matelas) ; plancher libre dessous |
| Lit king | plateforme noir mat 84 × 82 po, dessus à 12½ po, socle en retrait de 3 po (le lit « flotte »), **4 grands tiroirs** (≈ 32 × 20 × 8 po, 2 par côté, prises de doigt sans quincaillerie) ; matelas 76 × 80, couette blanche, jeté sauge, coussins caramel |
| Garde-robe réunie | **double penderie** (26 po, tringles noires à 41 et 81 po) ; **tour de 4 tiroirs** (22 po) et 3 tablettes à chandails ; **penderie longue** (24 po, tringle à 68 po) et tablette à souliers ; tablette haute continue à 84 po avec 4 paniers ; DEL à l'ouverture ; intérieur en placage de bois pâle |
| Portes coulissantes | rail encastré ; vantail avant = **miroir pleine hauteur à cadre noir mat** (remplace le miroir de la commode) ; vantail arrière = noir mat à fines rainures, tirette noire |
| Fenêtre | un grand rideau de lin pleine hauteur sur rail noir au plafond (la fenêtre paraît plus grande), qui se range côté lit : le coin entre la fenêtre et la garde-robe reste libre ; store opaque dans l'embrasure |
| Sol et murs | érable existant ; tapis de laine ≈ 8 × 8½ pi sous les deux tiers du lit (hors de l'arc de la porte) ; murs « Lin chaud » (greige, #E2D9CB, à choisir sur échantillon) |
| Éclairage | 4 encastrés plats 2700 K autour du lit (aucun au-dessus des oreillers), 1 dans la garde-robe, DEL des niches, liseuses |
| Cloison du pied | une seule œuvre encadrée (générique) ; le reste respire |

Arrêts de visite : « Chambre des parents » (depuis la porte, vers le mur de tête) et « Chambre des parents,
garde-robe » (depuis le côté fenêtre, vers la garde-robe), à la place des deux arrêts « Chambre arrière ».

#### Rangement : avant / après
| | Avant | Après |
|---|---|---|
| Penderie | 2 G.R. à une tringle (≈ 67 po de tringle) | 76 po de tringle (2 × 26 po en double + 24 po en long) |
| Tiroirs | commode blanche (3 tiroirs) | 4 grands tiroirs sous le lit + 4 dans la garde-robe + 2 chevets |
| Tablettes | tablettes hautes des G.R. | tablette haute continue (4 paniers) + 3 tablettes à chandails + 3 niches |
| Plancher libre | commode, vélo, panier au sol | rien au sol à part le lit : la pièce respire |

#### Le vélo
Le vélo de route sur base d'entraînement **descend au gym du sous-sol** : SS-17 y prévoit déjà l'emplacement d'un vélo
sur base, à côté du tapis roulant (`elem-SS-P-GYM-VELO`). Si un deuxième vélo est déjà là, les deux bases se placent
côte à côte ou le second va sur un support mural ; à coordonner avec la zone gym (non modifiée ici).

#### Ce qui n'est pas fait, et pourquoi
- **Pas de banc au pied du lit** : un banc de 14 po ramènerait le passage devant la garde-robe de 38 à 24 po (sous les
  30 à 36 po demandés), et les tiroirs de la garde-robe doivent pouvoir s'ouvrir. Si le client y tient : un pouf
  rond qui se range sous la fenêtre, ou l'option « coffre à vérins » ci-dessous avec un lit plus court de 4 po.
- Pas de commode : ses tiroirs passent dans le lit, les chevets et la garde-robe.

#### Options
| Choix | A — économique | B — recommandée (dessinée) |
|---|---|---|
| Garde-robe | on garde les 2 G.R. et la cloison ; portes battantes remplacées par 2 portes pliantes (saillie ≈ 14 po, 24 po libres au pied quand elles sont ouvertes) ; aménagement en kit | G.R. 1 et 2 réunies, baie de 66 po, 2 coulissantes (miroir + noir mat), aménagement complet |
| Mur de tête | panneau de bois de grange de 8 pi de large derrière le lit, 2 tablettes flottantes, 2 liseuses, prises USB-C en applique | fourrure pleine largeur et pleine hauteur, niches noir mat éclairées, chevets suspendus intégrés |
| Lit | plateforme du commerce à tiroirs | plateforme sur mesure à 4 tiroirs ; variante : **coffre à vérins** (tout le dessous en coffre, pour le saisonnier ; plus de rangement, moins pratique au quotidien) |
| Portes de la G.R. | — | variante : 2 panneaux de bois de grange sur rail apparent noir (look grange), mais alors un second grand pan de bois face au mur de tête |

#### Coût (ordre de grandeur, à confirmer par 2 ou 3 soumissions à Baie-Comeau)
Estimation de l'équipe d'après les prix de détail et les taux usuels au Québec (2025-2026), installation comprise.
| Poste | Fourchette |
|---|---|
| Mur de tête intégré (fourrure, gypse, bois de grange ≈ 100 pi², 3 niches, DEL, 2 liseuses, 2 prises USB-C, électricien, chevets suspendus) | 4 500 – 9 000 $ |
| Plateforme king à 4 tiroirs (commerce → sur mesure) | 1 000 – 5 500 $ |
| Matelas king et literie king | 1 600 – 4 500 $ |
| Garde-robe : cloison et montant enlevés, linteau, gypse, peinture | 1 200 – 2 800 $ |
| Garde-robe : aménagement intérieur (penderies, 4 tiroirs, tablettes, DEL) | 1 500 – 4 000 $ |
| 2 portes coulissantes 34 × 80 (miroir et noir mat), rail encastré | 1 200 – 2 800 $ |
| Peinture de la chambre, 4 encastrés et gradateur | 1 200 – 2 400 $ |
| Rideau de lin, rail, store opaque, tapis | 1 000 – 2 500 $ |
| **Total option B** | **≈ 13 000 – 33 000 $** |
| Option A (pliantes, panneau de tête, plateforme du commerce) | ≈ 5 000 – 10 000 $ |

#### Points à vérifier sur place
1. `mur-RDC-021` (chambre / garde-robes) : **porteur inconnu**. La baie de 66 po (au lieu de deux baies de 28 po et
   d'un montant) demande un linteau si le mur porte ; vérifier le sens des solives au-dessus.
2. Mur gauche (extérieur) : prises, thermostat ou plinthe électrique à déplacer dans la fourrure ; garder l'isolant et
   le pare-vapeur intacts derrière les niches (les niches sont dans la fourrure de 9 po, pas dans le mur extérieur).
3. Plinthe chauffante sous la fenêtre : garder ≈ 6 po entre la plinthe et le rideau (ou rideau qui s'arrête
   au-dessus).
4. Fenêtre `ouv-RDC-003` dessinée « fixe » au plan de base : une chambre doit avoir une **fenêtre qui ouvre et permet
   l'évacuation** (ouverture libre ≥ 0,35 m², aucune dimension < 380 mm) — à vérifier.
5. Avertisseur de fumée (et de CO) dans la chambre ou le corridor, relié aux autres.
6. Livraison : un matelas king (souple) passe la porte de 30 po ; pas de sommier rigide de 76 po (la plateforme le
   remplace) ; plateforme livrée en pièces.
7. Hauteur de plafond PRÉSUMÉE à 96 po : la tablette haute de la garde-robe est à 84 po.
8. Profondeur de la garde-robe (24½ po au nu) : juste suffisante pour une penderie ; mesurer avant de commander.

**À valider avec la Ville et un professionnel** (linteau, électricité, fenêtre d'évacuation, avertisseurs).

#### Limites de la maquette
- Le miroir de la porte coulissante reflète l'intérieur de la garde-robe (il paraît brun) : la visionneuse prend
  l'image d'un miroir du côté du centre de la maison (x = 228), donc derrière ce miroir-ci. Signalé au moteur.
- Œuvre encadrée, livres et vêtements : génériques.

## Rez-de-chaussée — bureau et gaming

### Bureau de travail et de gaming (ancienne chambre avant) — `rdc_bureau.py`

#### Demande
> « La chambre avant devient un bureau de travail et de gaming (2 stations assis), idéalement face à la fenêtre qui a
> une vue vers le fleuve. »

#### Hypothèse : la fenêtre « vers le fleuve »
- La pièce n'a **qu'une fenêtre** : `ouv-RDC-001`, sur la façade avant (y = 5). Elle fait 75 po (6'-3"), baie de x = 60,5 à
  x = 135,5, allège présumée à 34 po, tête à 82 po (relevé RDC-01). Le mur de gauche (x = 5) n'a pas de fenêtre dans
  cette pièce : `ouv-RDC-006` est celle de la salle de bain, et la cheminée est dehors, au coin arrière.
- D'après la flèche du nord (9,8° en sens horaire depuis l'arrière, valeur ESTIMÉE), la façade regarde à environ 170°,
  donc **plein sud, un peu vers l'est**. Baie-Comeau est sur la rive nord : le fleuve est au sud. On suppose donc que c'est
  cette fenêtre qui donne vers le fleuve. **À confirmer avec le client.**

#### Ce qui change (et pourquoi)
| Élément | Proposition | Pourquoi |
|---|---|---|
| Pièce | Renommée **« Bureau »** (124 pi², 11'-1¾" × 12'-0¾" plus le renfoncement de la porte). Murs, porte, fenêtre et garde-robe **inchangés**. | Rien de structurel. La pièce peut redevenir une chambre (revente). |
| Plan de travail | **Un seul plan continu en chêne** de mur à mur : 132 × 30 po, dessus à 29,5 po, posé contre la façade, sous la fenêtre. Il repose sur un tasseau au mur, deux pattes en U d'acier noir mat aux bouts et un caisson central. | Les deux postes regardent la fenêtre. Une seule ligne de bois est plus calme que deux bureaux. Le chêne fait le lien avec l'érable, le bois de grange et le noir mat du RDC. |
| Postes | Deux postes de **54 po d'axe en axe** (x = 60 et x = 114), donc 28 po libres entre les chaises. **Chaises ergonomiques** (haut dossier, appui-tête, appui lombaire, accoudoirs 4D qui passent sous le plan) en tissu anthracite sur piètement noir. | Deux bureaux de 60 po ne tiennent pas devant la fenêtre : il n'y a que 134 po de mur à mur, et la fenêtre est décalée vers la droite. 54 po par poste, c'est le confort d'un poste de jeu (clavier et souris larges). |
| Écrans | Par poste : **un écran principal de 27 po droit devant, monté BAS** (bas à 31,5 po, haut à 45,8 po, sous la hauteur des yeux assis, 46 à 48 po), plus **un écran de 24 po vertical** sur le côté extérieur, pivoté de 28°. Bras articulés à pince sur le bord arrière. | La vue reste dégagée au-dessus des écrans, à la hauteur des yeux, là où se trouve l'horizon du fleuve. Le **centre de la fenêtre reste libre** (x 72 → 102, environ 30 po). Les écrans verticaux sont aux bouts : celui de gauche est devant le mur plein. Les écrans ne cachent que le bas de la vitre (34 → 46 po), et les bras permettent de les écarter. |
| Ordinateurs et câbles | Tours **suspendues sous le plan** aux deux bouts (sangles d'acier, panneau vitré côté chaise), **caisson à 3 tiroirs** au centre (tirettes de laiton), **goulotte à câbles** sous le bord arrière, passe-câbles dans le plan. | Le plancher reste dégagé (balayeuse, roulettes) et les jambes sont libres. On ne voit aucun fil depuis la porte. |
| Dégagement | **36 po libres derrière les chaises** (y 72 → 108), puis encore 14 po jusqu'à la crédence. | Comme demandé ; on se lève et on passe derrière sans déranger l'autre. |
| Acoustique | **Mur gauche : lattes de chêne sur feutre noir**, du plancher au plafond (environ 10'-10" × 7'-10", 5 à 6 panneaux de 24 po). **Deux panneaux de feutre sable** de 20 × 36 po au mur arrière. **Tapis à poils ras** d'environ 6' × 9' sous les chaises. | Les voix au micro et le clavier résonnent dans une petite pièce aux surfaces dures. Le mur de lattes est aussi le mur d'accent chaleureux de la pièce. |
| Rangement | **Crédence flottante de chêne** de 48 × 18 × 18 po au mur arrière (dessous à 9 po) : deux portes à poussoir (consoles, manettes, câbles) et une niche ouverte (jeux debout, panier des manettes). Dessus : deux supports à casque et un socle de recharge des manettes. | Rangement bas qui laisse respirer la pièce. Tout ce qui sert au jeu est à un pas derrière les chaises. |
| Détente | **Fauteuil de cuir cognac** dans le coin arrière gauche, tourné vers les écrans, avec une petite table d'appoint et une liseuse. Il est hors du dégagement. | Pour lire, attendre son tour, ou pour que les garçons regardent jouer. |
| Éclairage | **2 encastrés plats** de 2700 à 3000 K à gradateur, derrière les chaises (hors de l'axe des écrans). **Ruban DEL blanc chaud** sous le plan (lueur sur le mur et le plancher) et sous la crédence. Liseuse au coin détente. Le plafonnier de la chambre est retiré. | Un éclairage doux et indirect pour jouer le soir sans reflets dans les écrans. Rubans RGBW possibles : blanc chaud par défaut, couleur pour le jeu. |
| Couleurs | **Mur arrière peint ardoise** (le fond vu par la caméra), les autres murs restent blanc cassé, plancher d'érable conservé. | Le fond sombre fait ressortir le feutre sable et le chêne. Il rappelle l'ardoise de la cuisine. |
| Fenêtre | **Toile solaire** (3 à 5 % d'ouverture) enroulée en haut de la baie. | Face à une fenêtre plein sud, le contre-jour et le soleil bas d'hiver éblouissent. La toile filtre sans cacher la vue. |

Plan P-130 : plan de travail « 2 POSTES », deux chaises, crédence (symbole d'armoire), fauteuil et mur de lattes
(éléments `elem-RDC-P-BUR-*`), note « Bureau (ancienne chambre avant) ». Maquette : le lit, les tables de chevet, la commode
et le plafonnier présumés de RDC-01 sont retirés de la pièce. Il y a deux arrêts de visite : **« Bureau et gaming »** (depuis
la porte) et **« Bureau et gaming, coin détente »**. Les deux écrans principaux montrent l'émission animée ; les écrans
verticaux montrent une interface sombre stylisée.

#### Options
- **A (proposée)** : plan continu de chêne face à la fenêtre ; par poste, un écran de 27 po bas et un écran de 24 po
  vertical à l'extérieur.
- **B, 3 écrans par poste** : on ajoute un 27 po du côté intérieur de chaque poste, ou on remplace le 27 po par un
  ultralarge courbe de 34 po. Ça coûte la vue au centre de la fenêtre, qui serait cachée de 34 à 46 po.
- **C, l'ergonomie d'abord** : on tourne les postes à 90° de la fenêtre (le long du mur de gauche, la fenêtre sur le côté).
  C'est la règle de l'ergonomie de bureau : pas de contre-jour ni de reflets. En contrepartie, la vue n'est plus devant soi.
- **Plan noir mat** (stratifié mat anti-traces ou chêne teint noir) au lieu du chêne : plus « gaming », moins chaleureux,
  et la poussière y paraît davantage.
- **Bureaux assis-debout** (2 × 60 po) : en position debout, les écrans montent à environ 48 à 60 po et cachent toute la
  fenêtre. Ça va mal avec la demande « face à la vue ».

#### Ordre de grandeur des coûts (estimation de l'agent, non soumissionnée)
Ce sont des fourchettes de prix de détail courants au Québec (détaillants de mobilier et de quincaillerie, fabricants de
chaises et de panneaux acoustiques), qui n'ont pas été vérifiées en magasin. **À confirmer par des soumissions.**

| Poste | Fourchette |
|---|---|
| Plan de chêne lamellé 132 × 30 po (finition huile ou vernis), pattes d'acier sur mesure, caisson à tiroirs, goulotte | 1 500 – 3 500 $ |
| 2 chaises ergonomiques ou de jeu de qualité | 800 – 3 600 $ |
| Bras d'écran (2 doubles), supports de tour, passe-câbles | 250 – 600 $ |
| Mur de lattes acoustiques (5 à 6 panneaux de 24 × 94,5 po) et 2 panneaux de feutre | 1 000 – 2 000 $ |
| Crédence flottante de chêne (semi-sur-mesure ou sur mesure) | 600 – 1 800 $ |
| Fauteuil de cuir, table d'appoint, liseuse, tapis à poils ras 6' × 9' | 1 000 – 2 500 $ |
| Éclairage : 2 encastrés plats, rubans DEL et alimentation, gradateurs | 300 – 800 $ (+ électricien) |
| Électricité : circuit dédié de 20 A, prises au-dessus de la goulotte, 2 prises réseau Cat 6 | 600 – 1 500 $ |
| Toile solaire motorisée de 75 po | 400 – 900 $ |
| Peinture du mur ardoise (fait soi-même) | 80 – 200 $ |
| **Total sans écrans ni ordinateurs** | **≈ 6 500 – 17 000 $** |
| Écrans neufs, si achetés (2 × 27 po à 1440p et 144 Hz, 2 × 24 po) | 1 100 – 2 000 $ |

#### Points à vérifier sur place
1. **La pièce n'a pas été photographiée** : mesurer la largeur (133¾ po présumés), la profondeur, la fenêtre (largeur,
   **allège** et type d'ouvrant), les prises, les plinthes chauffantes, le plafonnier et le détecteur de fumée.
2. **Allège de la fenêtre** : le plan (dessus à 29,5 po) passe sous l'allège présumée de 34 po. Si l'allège est sous 31 po,
   il faut baisser le plan ou le décoller du mur. Si la fenêtre ouvre à manivelle, vérifier qu'on la rejoint par-dessus
   30 po de plan.
3. **Plinthe chauffante sous la fenêtre ?** Le plan ne doit jamais la couvrir (dégagements du fabricant). Il faudra alors
   la déplacer ou la remplacer par un convecteur mural ailleurs dans la pièce.
4. **Électricité** : deux PC de jeu et quatre écrans demandent environ 1 000 à 1 500 W en pointe. On recommande un circuit
   dédié, des prises à hauteur de la goulotte, des parasurtenseurs et un câble réseau jusqu'aux postes.
5. **Mur de gauche = mur extérieur** : visser les lattes dans les montants avec des vis courtes, sans percer le pare-vapeur
   inutilement.
6. **Porte de la garde-robe** (`ouv-RDC-021`) : en s'ouvrant, elle passe dans le dégagement derrière la chaise de droite.
   Elle reste utilisable quand la chaise est rentrée. Le module de l'entrée peut modifier cette garde-robe : rien ici
   n'en dépend, et le bureau reste à l'intérieur de la pièce.
7. **Contre-jour** : de jour, une fenêtre derrière les écrans fatigue les yeux. La toile solaire, les écrans bas et la
   luminosité automatique compensent ; sinon, voir l'option C.
8. **Revente** : on perd une chambre au RDC sur papier. La garde-robe est conservée et tout est amovible, sauf la peinture.

Les travaux d'électricité (circuit dédié, déplacement d'une plinthe chauffante) demandent un maître électricien et,
selon le cas, un permis. **À valider avec la Ville et un professionnel.**

## Rez-de-chaussée — bugs corrigés


### Demande
« Corrige les bugs en haut. » La maquette du rez-de-chaussée (copie du relevé photo RDC-01 :
`base_rdc01_modifs.py`, `base_rdc01_scene.py`) a été comparée aux 15 photos du propriétaire
(`renovation/prive/rdc_actuel/`), aux 16 arrêts de visite et en vue maquette (étage seul, `ETAGE=RDC`), avec en plus un
contrôle géométrique (objets qui entrent dans un mur, faces confondues, arrêts dans un meuble, lumières cachées).
Zones traitées : cuisine, salle à manger, salon, dégagement, salle de bain, entrée arrière et problèmes communs
(portes, frigo, arrêts). L'entrée, le hall, l'escalier, la chambre arrière et la chambre avant sont réaménagés par
d'autres modules (`rdc_entree.py`, `rdc_chambre_arriere.py`, `rdc_bureau.py`) : leur mobilier n'a pas été retouché.

### Ce qui change et pourquoi
| Bogue | Correction | Fichier |
|---|---|---|
| 2e frigo (portes françaises) : `MOD("frigo_30", ..., L=36)` agrandissait le modèle (30 × 24 × 69 po) dans les trois sens → ≈ 83 po de haut, 29 po de creux | Frigo construit en blocs à la vraie taille 36 × 29 × 70 po (caisse inox, deux portes françaises, tiroir congélateur, poignées en barre, grille du socle), devant la fenêtre comme sur les photos 01 à 03 ; la fenêtre reste visible au-dessus | `base_rdc01_scene.py` (`frigo_36`) |
| Portes blanches des garde-robes de la chambre arrière rendues en pin (une seule essence de porte par maquette) | L'ouverture porte `"finition": "blanc"` dans maison.json (ouv-RDC-019, ouv-RDC-020, photo 10). La scène habille le battant fermé calculé par le moteur (`battant()`) d'une pellicule blanche de 0,08 po liée à la porte (`"porte": id`) : elle pivote avec elle quand on l'ouvre. Tout module peut s'en servir : `o["finition"] = "<matériau>"` | `base_rdc01_modifs.py`, `base_rdc01_scene.py` (`portes_finies`) |
| Entrée arrière sans ses marches qui descendent ni sa main courante | Volée qui descend vers la gauche le long du mur du fond (6 contremarches de 7½ po, girons de 10½ po, ardoise et contremarches noires), palier au niveau du RDC devant la porte extérieure (nez à x = 284 pour que le battant de la porte ne balaie pas la volée), nez de palier en inox, main courante de bois brut à 34 po sur consoles noires (photos 01, 07, 08). Ajoutée au plan P-130 (« DESCEND », élément existant `elem-RDC-R-ESCARR`). Tapis déplacé devant la porte extérieure (il entrait de 1 po dans le mur) | `base_rdc01_modifs.py`, `base_rdc01_scene.py` (`EAR_*`) |
| Baie salle à manger / entrée arrière : doublage de pin dans l'épaisseur, alors que tout le cadrage est noir sur les photos 01, 07, 08 | Doublage noir mat par-dessus celui du moteur | `base_rdc01_scene.py` |
| Arrêt « Salle à manger » collé au bout de la table, face à la fenêtre et au tableau noir | Déplacé en diagonale depuis le coin cuisine (305, 212, cap 145) : table, chaises, buffet, fenêtre, tableau noir, porte de garde-robe et coin bureau dans le même cadre | `base_rdc01_scene.py` (`visites`) |
| Arrêt « Hall (mur de cadres) » placé dans le dossier du sectionnel | Reculé derrière le sectionnel (300, 146) | idem |
| Arrêt « Salon » presque identique à « Cuisine vers le salon » (même point, même cap), qui regardait surtout un mur blanc et la fenêtre | Nouveau point de vue dans le salon (300, 80, cap 25) : télé, thermopompe, 2e frigo et cuisine par l'ouverture de la poutre | idem |
| Deux encastrés de la cuisine cachés au-dessus de la colonne d'armoires pleine hauteur (0,2 po sous le plafond), un troisième qui éclairait le dessus de la hotte | Déplacés devant la colonne (x = 406) et devant la hotte (x = 414) | `base_rdc01_scene.py` (`lumieres`) |
| Papier hygiénique dans l'ouverture de la fenêtre de la toilette (z = 49, fenêtre de 34 à 82 po) | Descendu à 27 po, sous l'allège (photo 14) | `base_rdc01_scene.py` |
| Hauteur de plafond 96 po présumée | Gardée (aucune cote ni photo ne permet de la mesurer), toujours marquée PRÉSUMÉE | — |

Vérifié sans changement : sens des robinets (cuisine et vanité : bec vers l'usager), de la cuisinière, du
lave-vaisselle, de la laveuse-sécheuse, de la toilette et de la colonne de douche ; objets posés sur les tablettes,
le buffet et la table ; aucun objet de ces zones n'entre dans un mur (le comptoir de cuisine entre de 4 po dans le mur
arrière, caché, et sert d'appui dans l'embrasure de la fenêtre de l'évier) ; pas de faces confondues visibles.

### Limites du moteur (signalées à l'agent moteur, non corrigées ici)
1. **Plancher non perçable à un seul étage** : le plancher n'est troué qu'aux trémies de l'étage du dessous (« trous »,
   maquette à plusieurs étages). La volée de l'entrée arrière est modélisée sous le plancher (z < 0) et déclarée dans
   `SCENE["tremies_plancher"] = [[229, 398, 284, 430]]` (clé nouvelle) : il faudrait l'ajouter aux « trous » de l'étage
   (plancher de la pièce ET sous-plancher de béton), aussi en `ETAGE=RDC`. D'ici là on voit le palier, son nez d'inox et
   la main courante qui descend sous le plancher, comme sur les photos ; les marches apparaîtront avec le trou.
2. **Une seule finition de battant** : tous les battants intérieurs reçoivent `mat: "porte"` (puis `mats_finitions`).
   Proposition : `o.get("finition") or "porte"` dans `battant()`, sans repasser par `mats_finitions` ; la pellicule de
   `portes_finies` deviendra inutile (inoffensive).
3. **Béquilles blanches** : elles sont en `"metal"`, que `mats_finitions` du RDC change en blanc (pour les cadres de
   fenêtre) ; les photos montrent des boutons noirs. Une clé de matériau propre aux poignées réglerait ça.
4. **Lampes (`lumieres` avec `z`)** : `PointLight` sans ombre et sans portée : elles éclairent les faces des pièces
   voisines à travers les murs (suspensions des chambres, appoints du salon). Une portée (`distance`) de ~250 po ou
   une ombre pour la plus proche limiterait la fuite.
5. **Modèles mis à l'échelle uniformément** (`L` ou `H`) : impossible d'avoir `frigo_30` à 36 po de large ET 70 po de haut.
6. **Escalier sous-sol → RDC** : dans la scène RDC seule, il est dessiné comme un escalier qui MONTE dans le salon
   (trémie au plafond, à travers le sectionnel) ; le module de l'entrée et la maquette à deux étages s'en occupent. Le
   plafond de crépi du salon (revêtement z 95,6 à 96) recouvrirait une trémie de plafond à cet endroit.

### Options
- Frigo : A (fait) blocs à la vraie taille ; B `MOD("frigo_30", ..., H=70)` : modèle détaillé mais 30 po de large.
- Volée de l'entrée arrière : A (fait) droite le long du mur du fond, palier tournant en bas (hors de vue) ;
  B si le relevé montre une autre forme, ajuster `EAR_*` en tête de la section et l'élément du plan.

### Coût
Aucun : corrections de maquette et de plan seulement, rien ne change dans la maison.

### Points à vérifier
- **Entrée arrière** : compter les marches, mesurer largeur, giron et hauteur ; vérifier où la volée arrive. Le caveau à
  légumes du sous-sol est sous l'entrée arrière et SS-17 y place un walk-in : **si la volée descend dans le caveau, le
  walk-in du sous-sol est à revoir**. Le côté ouvert de la volée n'a pas de garde visible sur les photos : une garde
  est normalement exigée quand la dénivellation dépasse 600 mm.
- Sens d'ouverture de la porte extérieure arrière (pentures côté mur du fond selon le plan de base).
- Hauteur de plafond (96 po présumés) ; allège et tête des fenêtres (34 et 82 po estimées).
- Largeur réelle du 2e frigo (36 po présumés, devant une fenêtre de 36 po).

À valider avec la Ville et un professionnel (garde et escalier de l'entrée arrière, tout changement à l'escalier ou aux
logements).

## Sous-sol — chambres des garçons allégées

### Sous-sol — chambres des garçons allégées (zone_chambre1.py, zone_chambre2.py)

#### Demande

> « Dans les chambres en bas il y a comme trop de meubles, exagère pas. »

Le client veut garder quatre choses :
- le lit queen sur plateforme à tiroirs ;
- un rangement principal bien pensé par chambre ;
- la porte-bibliothèque secrète vers le walk-in de la chambre 2 (son « wow ») ;
- un coin pour jouer au sol.

Le reste est retiré ou simplifié. Le rideau au plafond était déjà retiré à sa demande.

**Parti pris** : quelques pièces de chêne, belles et utiles, et du plancher libre au centre de chaque chambre. Aucune cloison,
porte ou fenêtre ne change par rapport à SS-17. Seuls le mobilier intégré, le plan, la 3D, les arrêts de visite et la
palette des deux modules sont touchés.

#### Chambre 1 — le petit de 4 ans : « le socle de chêne », allégé

**On garde (3 pièces)**

- **Lit-plateforme queen en coin**
  - Tête au mur ouest, long côté au mur arrière, dessus du matelas à 22 po.
  - Trois bacs-wagons roulants sous le lit : les jouets de la semaine, qu'on roule jusqu'au tapis.
  - Tête en lattes de chêne et une seule liseuse.
  - Au lieu des niches éclairées, une simple tablette-dosseret le long du mur, pour la veilleuse et les livres du soir.
  - On garde la DEL de plinthe : c'est le chemin de nuit.
- **Banquette des fenêtres**
  - Du pied du lit au mur de la chambre 2.
  - Quatre grands tiroirs de 36 po au lieu de six, deux coussins.
  - Elle sert aussi de marche d'évacuation.
  - Le mur argile derrière reste l'accent de la pièce.
- **Garde-robe intégrée de 134 po (le rangement principal)**
  - Façade calme : portes pleines de chêne et gorges noires.
  - Penderie évolutive.
  - Quatre tiroirs à sa hauteur.
  - Un module de « rotation des jouets » : ce qui ne sert pas cette semaine dort là, et ce qui sert tient dans les bacs du lit.
  - Le haut est aux parents.

**Coin jeu au sol, au centre**
- Tapis de laine 5 × 8 pi entre le lit, la garde-robe et la banquette.
- Un pouf.
- Un seul rebord de chêne de 48 po au mur est, à 26 po, pour 4 livres de face.

**Retirés**
- La canopée au-dessus du lit, ses loquets et ses DEL.
- Les niches éclairées et la prise cachée du dosseret.
- Les deux bibliothèques de part et d'autre de la banquette, la valance et les stores cachés : les stores sans cordon vont dans l'embrasure.
- La gare à jouets (12 bacs, comptoir de jeu) et le mur à crémaillères (panneau perforé, chevilles, câble à dessins).
- La station du matin du recoin. Le recoin redevient une entrée libre, où la porte s'ouvre.
- La niche-cachette de la garde-robe (coussin, veilleuse, tringle à billes), les tiroirs de plinthe et les étiquettes-images.
- La moitié des jouets : il reste un camion de bois et trois blocs.

**Plan P-129**

Éléments retirés :
- `elem-SS-P-C1-CANOPEE`, `-BIB1`, `-BIB2`, `-GARE`, `-VEST`.

Éléments gardés, avec un nouveau libellé :
- `elem-SS-P-C1-LIT`, `-BANC` (4 tiroirs), `-GR` (portes pleines).

Les retraits de SS-17 sont maintenus : cloisons P12 et P13, portes P07, pièce GR1, commode SS-16.

**Visite 3D** : 5 arrêts.
1. vue d'entrée ;
2. lit sur plateforme à bacs ;
3. banquette des fenêtres ;
4. coin jeu au sol ;
5. garde-robe intégrée.

#### Chambre 2 — le grand de 6 ans : « la bibliothèque secrète », allégée

Le **rangement principal de la chambre 2, c'est le walk-in** (ancien caveau, inchangé) :
- penderie double qui grandit sur crémaillères noires ;
- banc à souliers ;
- tour de tiroirs ;
- miroir au dos de la porte.

La chambre elle-même n'a donc plus besoin de mur de rangement.

**On garde**

- **Porte-bibliothèque secrète et son imposte**
  - Telles quelles, livre-levier rouge compris.
  - Elles sont maintenant seules dans le coin nord-ouest, au bout de l'axe de la porte d'entrée : c'est la première chose qu'on voit en entrant.
- **Lit queen sur plateforme**
  - Quatre tiroirs, deux par côté.
  - Tête au mur arrière, au même endroit.
- **Tête de lit simplifiée**
  - Un seul panneau de lattes de chêne sur feutre noir, de 106 × 60 po, coiffé d'un chapeau de chêne.
  - Deux chevets flottants à tiroir, de 16 × 12 po, avec le dessus à 24 po.
  - Deux liseuses DEL encastrées dans les lattes.
- **Banc de fenêtre sous la fenêtre est**
  - Ramené à 24 po de profondeur (au lieu de 28) : il reste 34 po de passage entre le lit et le banc.
  - Trois tiroirs. Celui du centre s'enlève : c'est la trappe d'accès au drain (432½, 314¼).
  - Deux dossiers, un coussin d'accent, une liseuse.
  - Il sert aussi de marche d'évacuation.
- **Pupitre à rabat**
  - C'est ce qui reste du mur d'activité.
  - Une boîte de chêne de 36 × 9 × 20 po, fixée au mur du vestiaire (x 282-318).
  - Le rabat s'ouvre à 23¾ po (hauteur d'un enfant de 6 ans), sur deux compas amortis, avec une DEL dessous.
  - Fermé, c'est une simple boîte au mur. Un tabouret rond l'accompagne.
  - Il est déplacé hors du mur mitoyen : le mur d'activité de SS-17 bloquait, une fois ouvert, le chemin entre la porte et la porte-bibliothèque.
- **Coin jeu au sol**
  - Tapis rond de laine de 64 po, bordé d'osier, entre la porte, le pupitre et le lit.
  - Il est placé **hors du balayage des deux portes** : rien ne doit gêner la porte-bibliothèque qui pivote vers la chambre.
  - Un petit train de bois.

**Retirés**
- La tour gauche du mur de tête et le pont d'armoires hautes blanches : l'alias de peinture « Blanc chaud mat » est retiré, il ne sert plus.
- Les deux chevets-niches pleine hauteur.
- La tour d'angle à trésors : vitrine LEGO, globe, coffre, bocal.
- Le garage à jouets, ses rebords à livres et le rail de galerie.
- Le mur d'activité : crochets, cases, panneau perforé, armoires hautes.
- Les bacs-wagons du pied du lit et les LEGO éparpillés.
- Les coussins en trop sur le banc.

**Plan P-129**

Éléments retirés :
- `elem-SS-P-CH2-TG`, `-PONT`, `-TOUR`, `-GARAGE`, `-ACTIV`.

Éléments nouveaux :
- `elem-SS-P-CH2-PUPITRE`.

Éléments redimensionnés :
- `-LATTES` (106 po) ;
- `-NG` et `-ND` (chevets flottants 16 × 12) ;
- `-BANC` (24 × 108).

Éléments gardés : `-LIT`, `-PB` et les trois éléments du walk-in.

Description de la pièce `piece-SS-CH2` ajoutée.

**Visite 3D** : 5 arrêts.
1. vue d'entrée (la bibliothèque au bout) ;
2. lit queen et tête de lattes ;
3. banc de fenêtre ;
4. coin jeu et pupitre ;
5. walk-in (inchangé).

#### Options pour le client

| Sujet | A (proposé) | B |
|---|---|---|
| Garde-robe ch. 1 | Tout sur mesure en placage de chêne | Caissons de série et façades de chêne sur mesure (≈ −30 %) |
| Niche-cachette ch. 1 | Retirée (portes pleines) | Remise dans le module C de la garde-robe (+ 600 à 1 000 $) si le petit y tient |
| Banquette ch. 1 | 4 grands tiroirs | Caissons ouverts et 4 paniers d'osier (≈ −800 $, encore plus léger à l'œil) |
| Recoin ch. 1 | Libre | 3 crochets de chêne au mur (≈ 60 $) |
| Pupitre ch. 2 | Maintenant (fermé, c'est une boîte au mur) | Plus tard, vers 7-8 ans (les ancrages sont prévus dès maintenant) |
| Rangement des parents ch. 2 | Tablette et bacs du walk-in (74 po) | Une armoire haute au-dessus du pupitre, plus tard |
| Porte du walk-in | Porte-bibliothèque secrète | Porte pleine de chêne avec miroir et bibliothèque fixe à côté (≈ −2 000 $) |

#### Coût (ordre de grandeur, estimation du designer : ébénisterie résidentielle au Québec 2025-2026, non sourcée ; à confirmer par 2 ou 3 soumissions d'ébénistes de la Côte-Nord)

**Chambre 1**

| Poste | Fourchette |
|---|---|
| Lit-plateforme + 3 bacs-wagons + tablette-dosseret + tête en lattes | 4 000 – 6 000 $ |
| Banquette de 12 pi, 4 tiroirs, coussins | 3 500 – 5 500 $ |
| Garde-robe intégrée de 134 po à portes pleines (3 modules) | 6 500 – 9 500 $ |
| Rebord à livres | 150 – 300 $ |
| Électricité (DEL de plinthe, liseuse, prises TR) | 700 – 1 200 $ |
| Crédit : garde-robe SS-16 non construite | − 1 500 à − 2 500 $ |
| **Total** | **≈ 13 000 – 20 000 $** (au lieu de 25 000 – 37 000 $ en SS-17) |

**Chambre 2 et walk-in**

| Poste | Fourchette |
|---|---|
| Lit-plateforme à 4 tiroirs | 2 000 – 3 500 $ |
| Panneau de lattes de 106 po + 2 chevets flottants | 1 800 – 3 000 $ |
| Porte-bibliothèque secrète (pivots, loquet, miroir, imposte) | 2 500 – 4 000 $ |
| Banc de fenêtre (3 tiroirs, trappe du drain, coussins) | 1 800 – 3 000 $ |
| Pupitre à rabat mural | 500 – 1 000 $ |
| Walk-in aménagé (inchangé) | 3 500 – 6 000 $ |
| Électricité (3 liseuses, USB, DEL du pupitre, panneau rayonnant, détecteur) | 1 500 – 2 800 $ |
| **Total** | **≈ 13 500 – 23 500 $** (au lieu de 24 000 – 42 000 $ en SS-17) |

Ces totaux excluent les matelas (800 à 1 500 $ chacun), les tapis (5 × 8 pi : 400 à 1 200 $ ; rond de 64 po : 250 à
700 $), le pouf et le tabouret. L'économie des deux chambres réunies est d'environ 20 000 à 35 000 $.

#### Points à vérifier — à valider avec la Ville et un professionnel

- **Fenêtres d'évacuation**
  - Concernées : ouv-SS-009 et ouv-SS-010 (chambre 1), ouv-SS-003 (chambre 2).
  - Elles doivent **ouvrir** : ouverture libre d'au moins 0,35 m², aucune dimension sous 380 mm, puits dégagé.
  - Allège (56 po) et tête (86 po) PRÉSUMÉES : à mesurer.
  - La banquette (16 po) et le banc (18 po) servent de marche ; rien d'autre devant le vitrage.
  - Limiteur d'ouverture qui se déverrouille sans outil.
- **Porte-bibliothèque**
  - Prévoir des pivots à usage intensif, dimensionnés pour le poids chargé.
  - Aucun verrou : elle s'ouvre en poussant depuis le walk-in.
  - Son balayage (x 245-277, y 338-370) reste libre : ni tapis, ni jouet, ni meuble.
  - Il faut vérifier la hauteur de la baie et le linteau.
- **Tapis sur béton poli** : sous-tapis antidérapant. Le tapis rond de la chambre 2 reste hors des deux battants.
- **Drain (432½, 314¼)** sous le banc de la chambre 2 : bouchonner ou garder accessible (le tiroir du centre s'enlève) ; vérifier le siphon et les odeurs.
- **Ancrages**
  - Garde-robe et banquette : vissées dans les montants ou les fourrures, avec attaches anti-basculement. Laisser ½ po d'air contre la fondation.
  - Chevets flottants : tasseau français dans du blocage.
  - Pupitre : vissé dans les montants du mur du vestiaire, avec blocage, sans toucher les armoires vert forêt de l'autre côté.
- **Électricité**
  - Prises inviolables (TR).
  - Liseuses DEL à basse tension.
  - Détecteurs de fumée et de CO reliés.
- **Arêtes** : coins arrondis à hauteur de tête et tiroirs à fermeture douce.
- **Caveau (walk-in)** : hauteur libre, isolation et humidité (moins de 50 % HR) avant d'y ranger les vêtements, comme en SS-17.

## Maquette des deux étages (moteur)

- Étages empilés (rez-de-chaussée à 105 po), escalier praticable, plancher et plafond troués à la trémie avec garde-corps de verre.
- Portes battantes et coulissantes interactives (toucher pour ouvrir ou fermer ; une porte fermée bloque la marche et s'ouvre toute seule sur un trajet).
- Les marches de l'entrée arrière ne sont pas dessinées : elles plongeraient dans le walk-in du sous-sol sous le perron ; le niveau réel de l'entrée arrière est à mesurer.

## Mise à jour (2026-11-02) : entrée ouverte
À la demande du client (« Enlève la vitre en haut, garde la vitre seulement tout le tour des marches, comme garde-corps en vitre,
mais le reste de l'entrée ouvert »), les trois murs de verre et la porte vitrée de l'entrée sont retirés. L'entrée est ouverte sur
le salon et le dégagement ; l'ouverture de l'escalier est entourée d'un garde-corps de verre clair (poteaux d'acier noir, main
courante de chêne) sur ses trois côtés libres — côté entrée, au bout et côté salon — et reste ouverte à l'arrivée en haut de la
volée. Le rangement de l'entrée (banc à bottes, armoires-vestiaires, niche-console) ne change pas. Les mentions de murs de verre
dans la section « grande entrée vitrée » ci-dessus ne s'appliquent plus.


## Mise à jour (2026-11-02) : un seul frigo en haut
Le 2e frigo (portes françaises, devant la fenêtre du mur de droite de la cuisine) est retiré à la demande du client : la
fenêtre est dégagée ; le frigo encastré dans la colonne d'armoires reste.

## Mise à jour (2026-11-02) : fenêtres aux dimensions de la vidéo DAG — toutes les fenêtres visibles dans la vidéo (« de bonnes dimensions », dit le client) en prennent la largeur, l'allège, la tête (80 po, à la tête des portes) et les sections ; ouv-SS-002 déplacée de +13 po vers l'allée, ouv-SS-003 à 84 po, ouv-RDC-008 à 36 po, salon à 12 po : fenetres_video.py, détail dans DESIGN_fenetres_video.md.

## Mise à jour (2026-11-02) : portes bloquées (salle de lavage, garde-robe des parents)
- **Salle de lavage** (sous-sol, `ouv-SS-P02`, 30 × 80 po, pentures côté hall, ouvre vers le lavage) : le miroir de sa face gym était un décor fixe posé devant la porte ; le toucher tombait sur lui (la porte ne s'ouvrait pas du gym) et, ouverte, il bouchait la baie. Il est collé au vantail et pivote avec lui (`zone_gym.py`) ; essayé dans la visite : on ouvre et on ferme des deux côtés, on passe à pied et par le trajet automatique, l'arc de 30 po libre (le coin du congélateur est à ≈ 1½ po hors de l'arc). **Garde-robe des parents** (RDC, `ouv-RDC-CH1-GR`, baie de 66 po) : même défaut ; le moteur dessine maintenant ses deux vantaux de 34 po (`"vantaux": 2`) : le miroir glisse de 32 po devant le panneau noir fixe, et les deux répondent au toucher. Les 12 autres portes des deux étages s'ouvrent, se ferment et se traversent.
- À valider sur place : la porte du lavage ouvre bien vers le lavage (pentures côté hall) et le congélateur (32 po de large, au bout du comptoir de pliage) laisse son arc libre : mesurer avant l'achat ; rail double encastré de la garde-robe (linteau de `mur-RDC-021`, porteur inconnu : avec un professionnel).
