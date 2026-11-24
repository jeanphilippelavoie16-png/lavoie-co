## Entrée vitrée du rez-de-chaussée (module `rdc_entree.py`)

### Demande du client
Annotations rouge et jaune sur la feuille P-128 de SS-17 (2026-11-01) :
« Enlève les garde-robes en rouge en haut pour que ça fasse une grosse entrée, et entoure l'entrée de murs de verre côté
cuisine et salon pour que ça soit comme isolé. Fais du rangement dans l'entrée en haut aussi. Fais de quoi de chic et
fonctionnel. » — « Ajoute les marches en haut pour monter et descendre. »

Lecture du croquis (vérifiée sur l'image et sur maison.json) : le trait rouge suit la cloison x = 175 de y ≈ 53 à 192,
c'est-à-dire toute la colonne de rangement entre la chambre avant et le hall (VEST., G.R. de la chambre avant, LIN.) ;
le trait jaune ferme l'entrée par un mur de verre horizontal vers y ≈ 172 (de x ≈ 162 à 305), qui tourne et descend
jusqu'au mur avant le long de l'escalier, côté salon (x ≈ 262 à 290).

### Parti pris
Un vestibule de 124,7 pi² (12'-2" × 10'-3", trémie comprise), fermé par du verre clair plancher-plafond à cadres noirs
minces. À gauche, tout le mur du bureau devient un meuble d'entrée pleine hauteur (noir mat et chêne) ; à droite, le
haut de l'escalier derrière un garde-corps de verre ; au fond, la porte vitrée dans l'axe de la porte d'entrée : en
entrant, la vue traverse jusqu'à la salle à manger et la brique de la cuisine. L'hiver, l'entrée fait sas : la neige et
le froid restent entre la porte d'entrée et la porte vitrée.

### Ce qui change sur le plan P-130
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

### Rangement : chic et fonctionnel (mur du bureau, x = 148¼, de l'avant vers l'arrière, 144 po de long)
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

### Dégagements vérifiés (plan et maquette)
- Devant la porte d'entrée : x 182 → 216, y 10 → 52 libres (42 po), le tapis-grattoir est à fleur.
- Haut de l'escalier : palier x 192 → 234, y 14 → 50 libre (42 po devant la marche du haut, sortie vers l'ouest).
- Porte d'entrée ouverte : le vantail se range à x ≈ 182, à 16 po du banc ; elle ne balaie jamais la volée.

### Escalier : échappée, largeur, garde (à valider)
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

### Accès aux autres pièces
- **Bureau (ex-chambre avant)** : sa porte (`ouv-RDC-014`, x ≈ 127 sur y = 157, côté dégagement) **n'est pas déplacée**.
  Il perd son garde-robe (le G.R. de la colonne ouvrait dans la chambre ; `ouv-RDC-021` est refermée) : l'agent bureau
  peut prévoir du rangement dans le bureau. Option non retenue : une porte directe entrée → bureau dans `mur-RDC-013`
  (le mur porte maintenant le vestiaire).
- Salle de bain, chambre arrière : inchangées, par le dégagement. La lingerie (21 po) disparaît : linge dans l'armoire 2.

### Maquette 3D (`appliquer_scene_rdc`)
- Arrêts « Entrée vitrée » (départ de la visite du RDC), « Entrée vitrée — banc et vestiaire », « Entrée vitrée vue du
  dégagement » ; « Entrée avant » et « Hall (mur de cadres) » retirés ; « Salon vers le hall » renommé ; palette « Entrée
  vitrée » ; crépi du salon arrêté au verre ; lumières du hall remplacées.
- **À deux étages** (sans ETAGE) : le moteur troue le plancher du RDC à la trémie du sous-sol et pose le garde-corps ;
  l'escalier DESCEND du RDC n'est pas redessiné. Vérifié dans les données produites (trou, garde-corps, aucune marche).
- **À un seul étage** (ETAGE=RDC) : ce module dessine le même garde-corps et une trémie sombre avec les nez des marches.
  **À corriger côté moteur** : à un étage, `generer_3d.py` dessine encore `elem-RDC-P-ESC` comme un escalier qui
  MONTE (il ne saute les escaliers DESCEND que dans la maquette à deux étages). La trémie est aussi déclarée dans
  `SCENE["tremies_plancher"]` (clé demandée au moteur par l'agent corrections).

### Coût (ordre de grandeur, estimation à confirmer par 2 ou 3 soumissions ; escalier exclu, déjà au budget du sous-sol)
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

### Points à vérifier sur place
- Sens et grosseur des solives au-dessus de la trémie (chevêtres, appuis) ; hauteur réelle du plafond du sous-sol et
  épaisseur du plancher (105 po présumés) ; poutre `str-RDC-R01` décorative ou porteuse.
- Rien dans la colonne de garde-robes (conduits, plomberie, fils) ; position exacte des poteaux C04 et C05 (montants du verre).
- Prises et câblage : console (USB-C), DEL, suspension, applique ; interrupteurs à 3 voies en haut et en bas de l'escalier ;
  avertisseur de fumée au haut de l'escalier.
- Verre : trempé feuilleté là où il sert de garde (côté salon, garde-corps) ; buée l'hiver (ventilation de l'entrée).
- Séparation coupe-feu : si le sous-sol devenait un logement distinct, ni le verre ni la trémie ouverte ne conviennent.

Structure, échappée, garde-corps, verre et coupe-feu : **à valider avec la Ville et un professionnel**.
