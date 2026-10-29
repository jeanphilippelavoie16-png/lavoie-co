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
