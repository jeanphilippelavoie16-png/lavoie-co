# MAISON-18 — Corrections de la maquette du rez-de-chaussée (agent « corrections »)

## Demande
« Corrige les bugs en haut. » La maquette du rez-de-chaussée (copie du relevé photo RDC-01 :
`base_rdc01_modifs.py`, `base_rdc01_scene.py`) a été comparée aux 15 photos du propriétaire
(`renovation/prive/rdc_actuel/`), aux 16 arrêts de visite et en vue maquette (étage seul, `ETAGE=RDC`), avec en plus un
contrôle géométrique (objets qui entrent dans un mur, faces confondues, arrêts dans un meuble, lumières cachées).
Zones traitées : cuisine, salle à manger, salon, dégagement, salle de bain, entrée arrière et problèmes communs
(portes, frigo, arrêts). L'entrée, le hall, l'escalier, la chambre arrière et la chambre avant sont réaménagés par
d'autres modules (`rdc_entree.py`, `rdc_chambre_arriere.py`, `rdc_bureau.py`) : leur mobilier n'a pas été retouché.

## Ce qui change et pourquoi
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

## Limites du moteur (signalées à l'agent moteur, non corrigées ici)
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

## Options
- Frigo : A (fait) blocs à la vraie taille ; B `MOD("frigo_30", ..., H=70)` : modèle détaillé mais 30 po de large.
- Volée de l'entrée arrière : A (fait) droite le long du mur du fond, palier tournant en bas (hors de vue) ;
  B si le relevé montre une autre forme, ajuster `EAR_*` en tête de la section et l'élément du plan.

## Coût
Aucun : corrections de maquette et de plan seulement, rien ne change dans la maison.

## Points à vérifier
- **Entrée arrière** : compter les marches, mesurer largeur, giron et hauteur ; vérifier où la volée arrive. Le caveau à
  légumes du sous-sol est sous l'entrée arrière et SS-17 y place un walk-in : **si la volée descend dans le caveau, le
  walk-in du sous-sol est à revoir**. Le côté ouvert de la volée n'a pas de garde visible sur les photos : une garde
  est normalement exigée quand la dénivellation dépasse 600 mm.
- Sens d'ouverture de la porte extérieure arrière (pentures côté mur du fond selon le plan de base).
- Hauteur de plafond (96 po présumés) ; allège et tête des fenêtres (34 et 82 po estimées).
- Largeur réelle du 2e frigo (36 po présumés, devant une fenêtre de 36 po).

À valider avec la Ville et un professionnel (garde et escalier de l'entrée arrière, tout changement à l'escalier ou aux
logements).
