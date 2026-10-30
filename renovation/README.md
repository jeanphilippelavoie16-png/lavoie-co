# Projets de rénovation — 86, avenue Laurier

## Règle
- **Plans de base** : `releve/livrables/` (relevé de l'existant R0, figé au commit `59ac401`). On ne les modifie **jamais**
  pour un projet.
- **Chaque projet** est un dossier ici, `renovation/<code>_<nom>/`, construit à partir d'une **copie** de la base.
  Pour une nouvelle version, on copie le dossier du projet (ex. `SS-01` → `SS-02`) et on modifie la copie.

## Contenu d'un projet
- `modifs.py` : les changements par rapport à la base (murs projetés, portes, pièces, équipements).
- `donnees/maison.json`, `svg/`, `pdf/`, `png/`, `dxf/`, `donnees/tableau_pieces.csv` : générés.

## Régénérer
    python3 renovation/outils/construire_projet.py renovation/SS-01_amenagement_sous-sol

## Projets
| Code | Projet | État |
|---|---|---|
| SS-01 | Aménagement du sous-sol : 2 chambres, grande salle de bain, salon / salle de jeu, salle d'entraînement, salle d'utilité | esquisse |
| SS-02 | Copie de SS-01 : aire ouverte, salle d'entraînement vitrée, direction de design, maquette 3D visitable (`3d/visite.html`) | esquisse |
| SS-03 | Copie de SS-02 : grande salle de bain à double vanité, cuisine en ligne, caveau en rangement, buanderie (skill designer-interieur) | esquisse |
| SS-04 | Copie de SS-03 : escalier vers le rez-de-chaussée (emplacement de 1957), coin bar avec lavabo et frigo (plus de salle à manger), vraie salle de lavage, peinture et textures | esquisse |
| SS-05 | Copie de SS-04 : salle de bain revue (toilette contre le mur, bain en coin, douche de 6 pi), matériaux réels dans la maquette | esquisse |
| SS-06 | Copie de SS-05 : nouvel escalier (emplacement dessiné sur A-101, en haut et en bas), sous-sol repensé autour d'un hall central, bain sur pied, gym (tapis roulant, vélo de route sur base, poids au sol) ; feuilles P-105 et P-106 | esquisse |
| SS-07 | Copie de SS-06 : vestiaire à la place du coin bar, coin frigo dans le séjour, escalier à 3 marches tournantes en haut, tapis roulant dans le sens du vélo ; feuilles P-107 et P-108 | esquisse |
| SS-08 | Copie de SS-07 : escalier en L, palier dans le coin arrière (étude de 3 implantations dans DESIGN.md) ; feuilles P-109 et P-110 | esquisse |
| SS-09 | Copie de SS-08 : escalier déplacé à l'est de la fenêtre de la chambre 1 (étude 2), chambre 1 agrandie ; feuilles P-111 et P-112 | esquisse |

## Études
- `etudes/escalier/` : six emplacements possibles pour l'escalier, en haut et en bas (étude 3).

## Maquette 3D
    python3 renovation/outils/generer_3d.py renovation/<projet>
Lit `donnees/maison.json` et `scene_3d.py` (matériaux, peinture, mobilier, éclairage, arrêts de visite) du projet.
La visite est pensée pour une tablette à l'horizontale : toucher le plancher ou le petit plan pour y marcher (chemin
automatique par les portes), glisser pour regarder, ◀ ▶ pour la visite guidée, liste des pièces à gauche, maquette sans
plafond (un doigt tourne, deux doigts zooment). Les escaliers projetés (`etat: nouveau`) sont modélisés avec leur trémie ;
`peinture` / `accents` dans `scene_3d.py` colorent les murs pièce par pièce. Les visites déjà publiées de SS-02 et SS-03
gardent l'ancienne visionneuse tant qu'on ne les régénère pas.

## Matériaux
`renovation/outils/materiaux/` : bibliothèque de matériaux réels (ambientCG, Poly Haven, CC0, ou fichiers de
fournisseurs), décrite dans `renovation/outils/catalogue_materiaux.py` ; voir `renovation/outils/materiaux/README.md`.

## Modèles 3D
`renovation/outils/modeles/` : 31 modèles réels optimisés (Amazon Berkeley Objects, Sketchfab, Poly Haven ; CC BY 4.0 ou CC0),
décrits dans `renovation/outils/catalogue_modeles.py` (sens, licence, attribution) ; recherche et sources dans
`renovation/outils/modeles/SOURCES.md`. Les crédits sont affichés dans la visite (panneau Matériaux).

## Skill de design
`.claude/skills/designer-interieur/SKILL.md` : méthode, dégagements, code à vérifier, direction de design, livrables.
