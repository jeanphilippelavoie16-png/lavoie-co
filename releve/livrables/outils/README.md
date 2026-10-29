# Générateur de plans — relevé de l'existant

`generer_plans.py` transforme `donnees/maison.json` (schéma figé : `travail/SCHEMA.md`, §4 et §6) en plans
professionnels. **Toute modification se fait dans `maison.json`, jamais dans les plans** : on régénère ensuite
tout en une commande.

## Prérequis

- Python 3.9 ou plus récent
- Bibliothèques :

```bash
pip install ezdxf cairosvg pypdf shapely
```

(`Pillow` est facultatif. S'il est installé avec la police Liberation Sans, les largeurs de texte sont mesurées
exactement ; sinon le script utilise l'approximation 0,6 × hauteur × nombre de caractères.)

## Tout régénérer (une commande)

```bash
cd livrables/outils
python3 generer_plans.py
```

Par défaut, le script lit `../donnees/maison.json` et écrit dans `..` (le dossier `livrables/`). Options :

```bash
python3 generer_plans.py --json exemple_factice.json --sortie /tmp/essai
```

| Sortie | Contenu |
|---|---|
| `svg/A-100_sous-sol.svg`, `svg/A-101_rdc.svg` | une feuille tabloïd 17 × 11 po par niveau, à l'échelle, calques Inkscape |
| `pdf/plans_existants.pdf` | toutes les feuilles, une page de 1224 × 792 pt par feuille, à imprimer à 100 % |
| `png/<feuille>.png` | aperçus à 150 ppp |
| `dxf/<feuille>.dxf` | AutoCAD R2010, unités en pouces (`$INSUNITS = 1`), repère maison (y vers l'arrière) |
| `donnees/tableau_pieces.csv` | tableau des pièces pour Excel (UTF-8 avec BOM, « ; », virgule décimale) |
| `donnees/verifications.txt` | rapport des contrôles (un résumé s'affiche aussi à l'écran) |

La sortie est **déterministe** : deux exécutions sur le même `maison.json` donnent des fichiers identiques octet
pour octet. La date et la révision du cartouche viennent de `projet.date` et `projet.revision`. Pour publier une
nouvelle version, augmentez `projet.revision` (R0 → R1) et mettez `projet.date` à jour.

`exemple_factice.json` contient des données **factices** (2 niveaux) qui servent à tester le générateur. Ce ne
sont pas les données de la maison.

## Modifier maison.json : exemples

Toutes les coordonnées sont en **pouces** dans le repère de la maison. L'origine (0, 0) est le coin extérieur
avant-gauche de la fondation, vu de la rue ; x suit la façade vers la droite et y va vers l'arrière.
Pour convertir : 12'-6" = 12 × 12 + 6 = 150.

**Déplacer un mur.** Un mur est le segment de son **axe**, avec l'épaisseur répartie à moitié de chaque côté.
Pour déplacer la cloison `mur-RDC-005` de 2 po vers la droite, ajoutez 2 à `x1` et à `x2` :

```json
{"id": "mur-RDC-005", "type": "int", "x1": 202, "y1": 6, "x2": 202, "y2": 374, ...}
```

Pensez aussi à corriger les polygones des pièces voisines (au nu intérieur des murs) et les `lignes_cote` qui
s'y rattachent. Sinon, `verifications.txt` signalera un trou ou un chevauchement dans le bilan de surface.
Les extrémités qui aboutissent à un autre mur sont prolongées automatiquement : les coins sont propres.

**Changer une cote.** Les cotes affichées sont **calculées** à partir de `p1` → `p2` (projection sur `direction`).
Pour qu'une cote vaille 12'-6", déplacez `p2` :

```json
{"id": "lc-SS-005", "p1": [100, 0], "p2": [250, 0], "direction": "x", "facade": "avant", "rang": 1,
 "source": "LU", "valeur_attendue": 150, "repere": null}
```

`valeur_attendue` est la valeur lue sur le plan. Si elle diffère de la longueur dessinée de plus de 0,5 po,
le rapport donne un avertissement. Règles de placement des cotes :

- `facade` (`avant`, `arriere`, `gauche`, `droite`) : la cote est placée hors du bâtiment.
- `rang` : 1 = ouvertures (le plus près du mur), 2 = segments de mur ou cloisons, 3 = hors-tout. L'espacement
  entre les rangs est constant.
- `facade` = `int` : cote intérieure. `decalage` (en pouces réels) déplace la ligne de cote
  perpendiculairement à `p1`-`p2` : valeur positive = vers +y (cote en x) ou vers +x (cote en y).

Si `lignes_cote` est **absent** d'un niveau, les 3 chaînes de chaque façade sont générées automatiquement à
partir des murs extérieurs et de fondation (source DÉDUIT). Une liste vide `[]` signifie : aucune cote.

**Ajouter une porte.** Ajoutez une entrée dans `ouvertures` du niveau :

```json
{"id": "ouv-RDC-017", "type": "porte", "operation": "battante", "mur_id": "mur-RDC-008",
 "position": {"valeur": 60, "source": "ESTIMÉ", "photo": "P3"},
 "largeur": {"valeur": 30, "source": "ESTIMÉ", "photo": "P3"},
 "hauteur": {"valeur": 80, "source": "PRÉSUMÉ", "photo": null},
 "sens": {"charniere": "debut", "ouvre_vers": "gauche"}}
```

- `position` est la distance mesurée le long du mur, de (x1, y1) jusqu'au **centre** de l'ouverture.
- `charniere` : `debut` = jambage du côté (x1, y1) ; `fin` = jambage du côté (x2, y2).
- `ouvre_vers` : côté où le vantail pousse, à gauche ou à droite **en regardant de (x1, y1) vers (x2, y2)**.
- `operation` : `battante`, `double`, `coulissante`, `pliante`, `fixe` ou `aucune`.
- `type` : `porte`, `fenetre`, `porte-patio`, `arche` ou `porte-garage`.

Une porte battante sans `sens` est une **erreur** (elle est alors dessinée comme une simple baie). Les portes
doubles et pliantes exigent au moins `ouvre_vers`.

**Régler une source.** Chaque dimension porte sa source :

```json
"epaisseur": {"valeur": 4.5, "source": "PRÉSUMÉ", "photo": null, "note": "cloison usuelle"}
```

| Source | Effet sur le plan |
|---|---|
| `LU` | aucun effet |
| `DÉDUIT` | aucun effet |
| `ESTIMÉ` | préfixe « ≈ » sur la cote ou la dimension |
| `PRÉSUMÉ` | repère ⚠n de l'écart référencé (`epaisseur.ref` pour un mur, `repere` pour une cote) |
| `ILLISIBLE` | « ? » après la cote |

Pour lier une cote à un écart du registre, mettez `"repere": "ecart-007"`. Pour lier un mur d'épaisseur
présumée, mettez `"ref": "ecart-006"` dans son objet `epaisseur`. Pour placer un repère sur le plan, ajoutez
`"position": [x, y]` à l'écart, dans le repère du niveau `ecart.niveau`. Un écart `global` positionné apparaît
sur chaque feuille dont la géométrie passe à moins de 24 po de cette position.

### Autres conventions (extensions tolérées)

- **Éléments fixes.**
  - `position` = **centre** de l'élément.
  - `longueur` = côté parallèle au mur d'appui ; `largeur` = profondeur.
  - `rotation_deg` = 0 : le dos de l'appareil est vers −y (côté rue) ; 90 : dos vers +x ; 180 : vers +y ;
    270 : vers −x.
  - Si les dimensions manquent, le symbole prend une taille usuelle (signalée dans le rapport).
- **Escaliers** (`type` : `escalier`).
  - `longueur` = course, mesurée dans la direction `escalier.direction` (`+x`, `-x`, `+y`, `-y`) ;
    `largeur` = largeur de l'escalier.
  - La flèche pointe dans cette direction, avec le texte `MONTE` ou `DESCEND`.
  - Le plan trace nb_contremarches − 1 lignes de marches. Si ce nombre est inconnu, les marches sont espacées
    de 10 po et le plan affiche « ≈ GIRON 10" ».
- **Structure.**
  - `poutre`, `axe`, `linteau` : segment `x1, y1, x2, y2`.
  - `colonne` et `semelle` : `x, y, largeur, profondeur`.
  - `solives` : zone `x1, y1, x2, y2`, plus `espacement` en pouces, et `sens` = `x` ou `y`.
- **Pièces.**
  - `dimensions: {"x": dim, "y": dim}` est facultatif. Sans lui, l'étiquette utilise la boîte englobante du
    polygone (source DÉDUIT).
  - `polygone` : contour au nu intérieur des murs, en sens antihoraire.
- **Notes.** `niveau.notes` sont affichées traduites dans le cartouche.
- **Feuille.**
  - `niveau.feuille` (par exemple A-100) et `niveau.photos_sources` alimentent le cartouche.
  - `niveau.slug` (facultatif) impose le nom de fichier.

## Calques (identiques en SVG et en DXF)

| Calque | Contenu |
|---|---|
| `00-Cartouche` | cadre, cartouche, légende, repères de la feuille, notes, échelle graphique, flèche du nord |
| `10-Murs` | remplissage de chaque mur, moins les baies (gris foncé : ext./fondation ; gris pâle : intérieur), puis contours unis |
| `20-Ouvertures` | portes (vantail et arc), coulissantes, pliantes, arches (tiretés), fenêtres (trait triple) |
| `30-Escaliers-Elements` | escaliers (marches, flèche, MONTE ou DESCEND, nombre de CM) et éléments fixes |
| `40-Structure` | poutres (tireté long), axes (trait mixte), colonnes (carré avec X), solives (double flèche), semelles (tireté) |
| `50-Cotes` | chaînes de cotes : traits obliques, lignes d'attache, texte en pi-po (métrique) |
| `60-Etiquettes` | noms, dimensions et superficie des pièces ; mention « FAÇADE AVANT (RUE) » |
| `70-Incertitudes` | repères ⚠n orange |
| `90-RENO-Propose` | vide, réservé aux interventions proposées |

Dans le SVG, chaque calque est un groupe Inkscape (`inkscape:groupmode="layer"`). Chaque entité porte l'`id` de
`maison.json` : `mur-SS-001`, `piece-RDC-CUI`, `lc-SS-004`, etc. Les repères portent `rep-<id>`, et ceux des
écarts portent l'id de l'écart.

Dans le DXF, l'id de chaque entité se trouve dans les XDATA (application `RELEVE`, code 1000). Une unité SVG ou
DXF vaut 1 po réel. Dans le SVG, y est inversé par calcul (aucune transformation miroir) : les textes restent
lisibles.

## Signification des symboles

- **≈** devant une cote ou une dimension : valeur **estimée**, mesurée sur l'image du plan d'origine et non
  écrite sur celui-ci. À confirmer sur place.
- **⚠n** (triangle orange suivi d'un numéro) : incertitude à consulter dans le **registre des écarts** de
  `RAPPORT.md`.
  - n est **toujours** le numéro d'un écart de `ecarts[]` : `ecart-007` → ⚠7. Aucun numéro inventé.
  - Chaque écart n'apparaît **qu'une fois par feuille**. Il est placé, par ordre de priorité, à sa
    `position`, sinon près de la première cote qui le référence, sinon près du premier mur qui le référence.
    Exemple : toutes les cloisons dont `epaisseur.ref` vaut `ecart-006` partagent un seul ⚠6. La ligne
    correspondante du cartouche précise « Toutes les cloisons sans cote d'épaisseur : 4½" présumé ».
  - Une cote présumée ou en conflit, ou un mur d'épaisseur présumée, sans écart référencé ne reçoit aucun
    repère. Il est signalé en [AVERT] dans `verifications.txt`.
  - La liste complète figure dans `verifications.txt` (section « Repères d'incertitude ») et, pour chaque
    feuille, dans son cartouche (descriptions abrégées).
- L'orange est réservé aux incertitudes. Tout le reste est en noir et gris.

## Échelle et mise en page

Le générateur choisit automatiquement la plus grande échelle parmi 1/4" = 1'-0", 3/16" = 1'-0" et
1/8" = 1'-0". Le plan, ses 3 chaînes de cotes et ses étiquettes doivent tenir dans la zone de dessin (feuille
moins les marges et le cartouche).

Les textes sont placés sans chevauchement : le script détecte les collisions par boîtes englobantes, mesurées
avec les métriques de Liberation Sans (identiques à celles d'Arial). Un texte ne doit toucher ni un autre texte
ni un trait : mur, ouverture, élément, structure, cote, ligne de rappel ou repère. Il ne doit pas non plus
sortir de la zone de dessin. Ordre de priorité :

1. **Cotes de façade.**
   - Les rangs présents sont empilés à 9 mm d'intervalle, ce qui laisse une bande de texte au-dessus ET
     au-dessous de chaque ligne.
   - Les cotes les plus contraintes, celles dont le texte est plus large que le segment, sont placées en
     premier. Ordre d'essai : centré au-dessus, au-dessous, décalé le long du segment, sur deux lignes
     (pi-po sur métrique), au-delà d'une extrémité, puis plus loin avec une ligne de rappel.
2. **Repères ancrés** (positions d'écarts, murs, cotes de façade).
3. **Étiquettes de pièces dans leur propre pièce.**
   - Variantes essayées : complète, nom + superficie, nom seul sur une ou deux lignes, nom tourné de 90°
     pour une pièce étroite.
   - Les couloirs des cotes intérieures sont d'abord laissés libres.
4. **Cotes intérieures, par chaînes colinéaires.**
   - Le `decalage` est un souhait : la chaîne entière peut être déplacée parallèlement, et le script retient
     la position sans collision qui garde les textes au plus près de leur ligne.
   - Si la chaîne entière n'a pas de place, ses cotes sont placées une à une. En dernier recours, le texte va
     à proximité avec une ligne de rappel.
5. **Libellés d'éléments**, à l'intérieur du symbole ou autour.
6. **Libellés de structure.**
   - Un libellé répété (par exemple COL. 8x8 ×6) n'est écrit qu'une fois, suivi de « (typ.) ».
   - La flèche des solives est placée avec son libellé.
7. **Étiquettes des petites pièces qui ne tiennent pas dans leur polygone.**
   - Nom seul, placé dans la zone libre la plus proche : de préférence hors des autres pièces, une pièce
     voisine étant tolérée.
   - Une ligne de rappel, terminée par un point, relie le nom à la pièce.
   - Les dimensions et la superficie de ces pièces sont alors omises sur le plan ; la légende le signale.
     Elles restent dans `tableau_pieces.csv`.

`verifications.txt` (section 8) doit indiquer « aucun chevauchement ». Sinon, il liste chaque cas restant.

## Contrôles (verifications.txt)

- **Identifiants** : ids dupliqués.
- **Murs** : géométrie incomplète, épaisseur manquante.
- **Ouvertures** : mur inexistant, ouverture hors du mur, porte sans sens, ouvertures qui se chevauchent.
- **Pièces** : polygone fermé et valide, sens antihoraire, chevauchement entre pièces, superficie déclarée
  différente de celle du polygone.
- **Bilan de surface** (par niveau) : empreinte brute comparée à Σ pièces + murs, et liste des trous de plus de
  1 pi² avec leur position.
- **Chaînes de cotes** : somme de chaque chaîne comparée au hors-tout de la même façade (± 0,5 po), continuité
  des chaînes, valeur attendue comparée à la valeur dessinée.
- **Textes** : chevauchements restants, texte/texte et texte/trait.
