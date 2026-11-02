# MAISON-18 — Corrections de la maquette du rez-de-chaussée (agent « corrections »)

## Demande
« Corrige les bugs en haut. » La maquette du rez-de-chaussée (copie du relevé photo RDC-01 :
`base_rdc01_modifs.py`, `base_rdc01_scene.py`) a été comparée aux 15 photos du propriétaire
(`renovation/prive/rdc_actuel/`), arrêt par arrêt, et en vue maquette (étage seul, `ETAGE=RDC`).
Zones traitées : cuisine, salle à manger, salon, dégagement, salle de bain, entrée arrière et problèmes communs
(portes, frigo, arrêts). L'entrée, le hall, l'escalier, la chambre arrière et la chambre avant sont réaménagés par
d'autres modules (`rdc_entree.py`, `rdc_chambre_arriere.py`, `rdc_bureau.py`) : leur mobilier n'a pas été retouché.

## Ce qui change et pourquoi
| Bogue | Correction | Fichier |
|---|---|---|
| 2e frigo (portes françaises) : le modèle `frigo_30` (30 × 24 × 69 po) agrandi par `L=36` l'était dans les trois sens → ≈ 83 po de haut, 29 po de creux | Frigo construit en blocs à la vraie taille 36 × 29 × 70 po (caisse inox, deux portes françaises, tiroir congélateur, poignées en barre, socle), devant la fenêtre comme sur les photos 01 à 03 ; la fenêtre reste visible au-dessus (≈ 12 po) | `base_rdc01_scene.py` (`frigo_36`) |
| Portes blanches des garde-robes de la chambre arrière rendues en pin (une seule essence de porte par maquette) | L'ouverture porte maintenant `"finition": "blanc"` dans maison.json (ouv-RDC-019, ouv-RDC-020) ; la scène habille le battant (calculé par les fonctions du moteur, ouvert ou fermé) d'une pellicule blanche de 0,08 po. Tout module peut s'en servir : `o["finition"] = "<matériau>"` | `base_rdc01_modifs.py`, `base_rdc01_scene.py` (`portes_finies`) |
| Entrée arrière sans ses marches qui descendent ni sa main courante | Volée qui descend vers la gauche le long du mur du fond (6 contremarches de 7½ po, girons de 10½ po, ardoise et contremarches noires), palier au niveau du RDC devant la porte extérieure (nez à x = 284 pour que le battant de la porte ne balaie pas la volée), nez de palier en inox, main courante de bois brut à 34 po sur consoles noires (photos 01, 07, 08). Ajoutée aussi au plan (« DESCEND », élément `elem-RDC-R-ESCARR`, existant). Le tapis est déplacé devant la porte extérieure (il entrait de 1 po dans le mur) | `base_rdc01_modifs.py`, `base_rdc01_scene.py` |
| Papier hygiénique dans l'ouverture de la fenêtre de la toilette (z = 49, fenêtre de 34 à 82 po) | Descendu à 27 po, sous l'allège, comme sur la photo 14 | `base_rdc01_scene.py` |
| Hauteur de plafond 96 po présumée | Gardée (aucune cote ni photo ne permet de la mesurer) ; toujours marquée PRÉSUMÉE — voir « Points à vérifier » | — |

## Limites du moteur (décrites à l'agent moteur, non corrigées ici)
1. **Plancher non perçable** : la visionneuse pose un sous-plancher de béton (`PlaneGeometry`, z ≈ 0) sous tout l'étage et
   un plancher par pièce, sans trou : rien sous z = 0 n'est visible. La volée de l'entrée arrière est modélisée sous le
   plancher et déclarée dans `SCENE["tremies_plancher"] = [[229, 398, 284, 430]]` (clé nouvelle, ignorée tant que le
   moteur ne perce pas le sous-plancher ET le plancher de la pièce à ces rectangles). Aujourd'hui on voit la main
   courante qui plonge sous le plancher et le nez de palier ; les marches apparaîtront quand le plancher sera percé.
2. **Une seule finition de battant** : `generer_3d.main` donne `mat: "porte"` à tous les battants (puis `mats_finitions`).
   Proposition : `mat = o.get("finition") or "porte"` (sans repasser par `mats_finitions`) ; la pellicule de
   `portes_finies` deviendra alors inutile (inoffensive : elle enveloppe le battant de 0,08 po).
3. **Modèles mis à l'échelle uniformément** (`L` ou `H`) : impossible d'avoir un frigo de 36 po de large ET de 70 po de
   haut avec `frigo_30`. Une échelle par axe (`Lx`, `Ly`, `H`) éviterait de construire en blocs.

## Options
- Frigo : A (fait) blocs à la vraie taille ; B `MOD("frigo_30", ..., H=70)` : bon modèle détaillé mais 30 po de large
  (6 po de moins que le vrai).
- Volée de l'entrée arrière : A (fait) droite le long du mur du fond, palier tournant en bas (hors de vue) ;
  B si le relevé montre une volée plus longue ou un autre sens, ajuster `EAR_*` en tête de la section.

## Coût
Aucun : corrections de maquette seulement, rien ne change dans la maison.

## Points à vérifier
- **Entrée arrière** : compter les marches, mesurer la largeur de la volée, le giron et la hauteur ; vérifier où elle
  arrive (le caveau à légumes du sous-sol est sous l'entrée arrière, et SS-17 y place un walk-in : **si la volée descend
  dans le caveau, le walk-in du sous-sol est à revoir**). Le côté ouvert de la volée n'a pas de garde visible sur les
  photos : une garde est normalement exigée quand la dénivellation dépasse 600 mm.
- Sens d'ouverture de la porte extérieure arrière (pentures côté mur du fond selon le plan de base).
- Hauteur de plafond (96 po présumés) et allège/tête des fenêtres (34 / 82 po estimées).
- Largeur réelle du 2e frigo (36 po présumés, à côté d'une fenêtre de 36 po).

À valider avec la Ville et un professionnel (garde et escalier de l'entrée arrière, tout changement à l'escalier ou aux
logements).
