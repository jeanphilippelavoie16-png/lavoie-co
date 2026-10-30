# Schéma figé — maison.json (R0)

Ce document est la référence commune de TOUS les agents. Ne pas le modifier.

## 1. Inventaire des photos (Phase 0)

| Photo | Contenu | Usage |
|---|---|---|
| P1 | Feuille « FONDATIONS & SOUS-SOL », éch. 1/4" = 1'-0" — gros plan, meilleure résolution | source principale sous-sol |
| P7 | Même feuille, vue entière (bas de feuille et cartouche visibles) | source secondaire sous-sol |
| P3 | Feuille « REZ-DE-CHAUSSÉE », éch. 1/4" = 1'-0" — gros plan, meilleure résolution (haut de la feuille un peu coupé) | source principale RDC |
| P4 | Même feuille RDC, vue entière | source secondaire RDC |
| P6 | Même feuille RDC, vue entière, autre prise (redressée en perspective) | source secondaire RDC |
| P5 | « Plan montrant l'emplacement de la maison projetée sur le lot 1-487 », Ville de Baie-Comeau, av. Laurier, éch. 1" = 20', daté 6 nov. 1957, flèche du nord | implantation, orientation |
| P2 | « Croquis no 1 — Résidence du 86, Laurier à Baie-Comeau — Plan d'origine et plan actuel du RDC », Claude Mazerolle, ing., 19 septembre 2016 (impression couleur superposée au plan d'origine ; quadrillage 1–7 / A–D ; axes porteurs d'origine ; colonnes retirées ; fissures ; ferme de toit 5/12) | indices état 2016, structure |

Aucune photo des lieux réels. Aucune feuille d'étage, d'élévation ou de coupe.

Fichiers (dossier `/home/user/lavoie-co/releve/travail/`) :
- `photos/Pn.jpg` : originaux (NE PAS modifier).
- `prep/redresse/Pn.jpg` : image tournée pour que le texte du plan se lise à l'endroit, contraste amélioré (P4, P6 aussi redressées en perspective).
- `prep/tuiles/Pn_rRcC.jpg` : tuiles zoomées ×2 (chevauchement 25 %). `prep/index_tuiles.json` donne pour chaque tuile sa boîte `[x0, y0, w, h]` en pixels de `prep/redresse/Pn.jpg`. Pixel dans la tuile (tx, ty) → pixel dans l'image redressée : (x0 + tx/2, y0 + ty/2).

## 2. Orientation et repère (IMPORTANT)

Les feuilles d'origine sont dessinées **rue en bas**. Dans toutes les images `prep/redresse/` (sauf P5, déjà à l'endroit, et P2 qui a son propre quadrillage) :
- le **bas de l'image = façade avant (côté rue, av. Laurier)**, côté de 38'-0" (perron de béton avec marches, vestibule, salon) ;
- le **haut de l'image = arrière** (entrée arrière / armoires, caveau à légumes au sous-sol) ;
- la **gauche de l'image = mur latéral gauche vu de la rue** (cheminée, chambres) ;
- la **droite de l'image = mur latéral droit** (salon, cuisine).

Repère de la maison (pouces) :
- **Origine (0,0)** = coin extérieur avant-gauche de la fondation (rectangle principal, sans les excroissances), vu de la rue. Même origine pour tous les niveaux.
- **x** suit la façade, de gauche à droite (vers la droite de l'image).
- **y** va vers l'arrière (vers le haut de l'image).
- Rectangle principal attendu : 38'-0" (x) × 31'-8" (y) — à confirmer par les cotes.
- Les éléments devant la façade (perron, excroissance de fondation sous le perron) ont y < 0.

Quadrillage du croquis 2016 (P2), une fois P2 tourné texte à l'endroit : lignes 1→7 le long de la façade (x), lignes A→D en profondeur (y), A côté rue.

## 3. Conventions générales

- Unité interne : **pouces** (décimales permises). 12'-6" = 150.
- **Objet dimension** : `{"valeur": <pouces ou null>, "source": "LU|DÉDUIT|ESTIMÉ|PRÉSUMÉ|ILLISIBLE", "photo": "P3", "ref": "cote-RDC-012" (optionnel), "note": "..." (optionnel)}`
  - LU = écrit sur le plan ; DÉDUIT = calculé à partir d'autres cotes (dire lesquelles dans `note`) ; ESTIMÉ = mesuré dans l'image ; PRÉSUMÉ = standard de construction faute d'info ; ILLISIBLE.
- Coordonnées (x1, y1, polygone, …) : simples nombres en pouces, dans le repère ci-dessus.
- Identifiants stables, ASCII, majuscules pour les codes : `mur-SS-001`, `ouv-RDC-012`, `piece-RDC-CUI`, `elem-SS-FOUR`, `str-SS-P01`, `cote-RDC-034`, `note-SS-03`, `ecart-007`.
- Niveaux : `SS` (sous-sol), `RDC` (rez-de-chaussée).
- Traduction : tout texte anglais → français québécois, original conservé (`nom_original`, `texte_original`).

## 4. Structure de maison.json

```json
{
  "projet": {
    "nom": "Résidence — 86, avenue Laurier, Baie-Comeau",
    "unites": "pouces (affichage pi-po, métrique entre parenthèses)",
    "origine": "coin extérieur avant-gauche de la fondation, vu de la rue ; x le long de la façade, y vers l'arrière",
    "convention_cotation": "<texte : hors-tout / à l'axe / au nu des murs, déterminé en Phase 2>",
    "ancres": [],
    "nord": {"angle_deg": <angle horaire de +y vers le nord, ou null>, "source": "...", "photo": "P5"},
    "photos": [{"id": "P1", "description": "..."}]
  },
  "niveaux": [
    {
      "id": "SS", "nom": "Sous-sol",
      "hauteur_plafond": {"valeur": null, "source": "ILLISIBLE", "photo": null},
      "murs": [{
        "id": "mur-SS-001",
        "type": "ext|int|fondation",
        "porteur": "oui|non|inconnu",
        "indices_porteur": ["poutre 8x10 dessous (P1)", "..."],
        "epaisseur": {"valeur": 10, "source": "LU", "photo": "P1"},
        "x1": 0, "y1": 5, "x2": 456, "y2": 5,
        "note": "optionnel"
      }],
      "ouvertures": [{
        "id": "ouv-SS-001",
        "type": "porte|fenetre|porte-patio|arche|porte-garage",
        "operation": "battante|double|coulissante|pliante|fixe|aucune",
        "mur_id": "mur-SS-001",
        "position": {"valeur": 60, "source": "...", "photo": "P1"},
        "largeur": {"valeur": 32, "source": "LU", "photo": "P1"},
        "hauteur": {"valeur": 80, "source": "LU", "photo": "P1"},
        "allege": {"valeur": null, "source": "ILLISIBLE", "photo": null},
        "sens": {"charniere": "debut|fin", "ouvre_vers": "gauche|droite"},
        "texte_original": "2'-8\"x6'-8\"",
        "note": "linteau 2-2x8 …"
      }],
      "pieces": [{
        "id": "piece-RDC-CUI", "nom": "Cuisine / salle à manger", "nom_original": "CUISINE S.-À-MANGER",
        "polygone": [[x, y], ...],
        "superficie": {"valeur": <pi²>, "source": "DÉDUIT", "photo": null},
        "hauteur_plafond": {"valeur": null, "source": "ILLISIBLE", "photo": null}
      }],
      "elements": [{
        "id": "elem-SS-FOUR", "type": "fournaise|chauffe-eau|evier|toilette|baignoire|lavabo|cuisiniere|refrigerateur|laveuse|secheuse|comptoir|armoires|cheminee|reservoir-huile|panneau-electrique|foyer|bac-lavage|robinet-exterieur|drain|escalier|perron|marches-ext|event|trappe|autre",
        "nom": "Fournaise", "nom_original": "FOURNAISE",
        "position": {"x": 0, "y": 0, "rotation_deg": 0},
        "dimensions": {"longueur": {...dim...}, "largeur": {...dim...}},
        "texte_original": "...",
        "escalier": {"nb_contremarches": {...dim...}, "fleche": "MONTE|DESCEND", "direction": "+x|-x|+y|-y", "texte_original": "14 C.M."}
      }],
      "structure": [{
        "id": "str-SS-P01", "type": "poutre|colonne|solives|semelle|linteau",
        "dimension": {"texte_original": "8\"x10\"", "valeur": "8x10", "source": "LU", "photo": "P1"},
        "sens": "x|y|null",
        "geometrie": {"x1": 0, "y1": 0, "x2": 0, "y2": 0} ,
        "note": "colonne : geometrie = {x, y, largeur, profondeur} ; solives : zone + espacement"
      }],
      "cotes": [{
        "id": "cote-SS-001",
        "texte_original": "12'-3\"",
        "valeur": 147,
        "lecture_1": "12'-3\"", "lecture_2": "12'-3\"",
        "statut": "confirmee|conflit|illisible",
        "photo": "P1",
        "emplacement": "chaîne extérieure côté gauche, 2e ligne depuis le mur, segment entre …",
        "px": [x, y],
        "mesure": "ce que la cote mesure (de quoi à quoi), réf. aux ids si possible"
      }],
      "notes": [{"id": "note-SS-01", "texte_original": "...", "interpretation": "...", "photo": "P1"}]
    }
  ],
  "ecarts": [{
    "id": "ecart-001", "niveau": "SS|RDC|global",
    "description": "...", "impact": "critique|moyen|faible",
    "hypothese_retenue": "...", "a_valider_sur_place": "où et quoi mesurer",
    "photo": "P1", "statut": "ouvert"
  }]
}
```

Règles de géométrie :
- Mur = segment sur son **axe** (ligne médiane) ; `epaisseur` de part et d'autre (moitié chaque côté).
- `position` d'une ouverture = distance le long du mur, de (x1,y1) jusqu'au **centre** de l'ouverture.
- `sens` d'une porte : `charniere` = jambage côté début (x1,y1) ou côté fin (x2,y2) du mur ; `ouvre_vers` = côté vers lequel le vantail pousse, **gauche ou droite en regardant de (x1,y1) vers (x2,y2)**.
- `polygone` d'une pièce = contour au **nu intérieur** des murs (surface nette), sens antihoraire.
- Superficies en pi² (le générateur affichera aussi m²).

## 5. Principes non négociables (rappel)

1. Aucune valeur inventée. 2. Chaque dimension porte sa source et sa photo. 3. Les cotes écrites priment sur le dessin (dessin pas à l'échelle ; proportions = ESTIMÉ seulement). 4. Aucune mesure sur place fournie (ancres vides). 5. Aucune incohérence corrigée en silence → registre des écarts. 6. Murs porteurs : jamais déduits ; « oui » seulement si un plan l'écrit ; sinon « inconnu » + indices. 7. Toute géométrie et tout fichier sont générés par code Python. 8. Confusions manuscrites à surveiller : 1/7, 3/8, 5/6, 0/6, ¼/½, pieds (') vs pouces (").

## 6. Extensions d'affichage (utilisées par le générateur)

- `projet.date` : "AAAA-MM-JJ" (date du relevé, fixe → régénération identique) ; `projet.revision` : "R0".
- `niveau.feuille` : "A-100" (SS), "A-101" (RDC).
- `niveau.photos_sources` : ["P1", "P7"].
- `piece.dimensions` (optionnel) : `{"x": <dim>, "y": <dim>}` — dimensions intérieures affichées sur l'étiquette (sinon boîte englobante du polygone, source DÉDUIT).
- `niveau.lignes_cote[]` : cotes à dessiner, écrites par le code de réconciliation :
  `{"id": "lc-RDC-001", "p1": [x, y], "p2": [x, y], "direction": "x|y", "facade": "avant|arriere|gauche|droite|int", "rang": 1|2|3, "decalage": <pouces réels, pour facade=int : distance perpendiculaire signée du segment p1-p2 à la ligne de cote>, "source": "LU|DÉDUIT|ESTIMÉ|PRÉSUMÉ", "statut": "confirmee|conflit|illisible", "ref": "cote-RDC-012", "valeur_attendue": <pouces lus sur le plan ou null>, "repere": "ecart-007" ou null}`
  Le texte affiché = longueur calculée p1→p2 (projetée sur `direction`), formatée pi-po + métrique.
  Rang 1 = ouvertures (le plus près du mur), 2 = segments de mur / cloisons, 3 = hors-tout.
- `ecart.position` (optionnel) : `[x, y]` dans le repère du niveau `ecart.niveau` → le générateur y place le repère ⚠n orange.
- `structure` de type « axe » permis (axe porteur d'origine signalé par l'ingénieur, P2).
