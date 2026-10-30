# QC R2 — Contrôle qualité indépendant (dernière boucle) — 86, av. Laurier, Baie-Comeau

Contrôleur : agent QC indépendant (lecture seule). Date : 2026-10-29.

## 0. Base contrôlée et périmètre

- **Base** : `HEAD = df6e90f` (« corrections du générateur QC R1… et régénération »), précédé de `8d7debb` (données QC R1), `8dae3f0` et `3c77bd0` (constat du propriétaire).
  Le dossier de travail `livrables/` est identique octet pour octet à HEAD (comparaison sha256 de tous les fichiers). Instantané en lecture seule dans le scratchpad.
  `maison.json` sha256 `40fabadefa41…`. Les cotes (160), leurs valeurs et leurs statuts sont **inchangés depuis R0** : l'échantillon de 90 cotes de R1 reste valable.
- **Changements volontaires depuis R1, non signalés comme défauts** : au RDC, cloisons de la cage d'escalier, du balais et des axes B/C retirées (`murs_retires` : mur-RDC-019 d'origine, -026 à -029) ;
  portes ou arches -013, -017, -023, -024 et -025 retirées ; trumeau `mur-RDC-019` (x 439,5–451) ; mobilier et électroménagers retirés (`elements_retires`) ;
  `ouv-RDC-015` qui ouvre vers le dégagement. Ces zones sont **contrôlées** ici quant à la cohérence géométrique, aux étiquettes, aux cotes et au ⚠30.
- Les paires de preuve de R2 sont dans `travail/qc/preuves_r2/` (à gauche l'original `prep/redresse/`, à droite le rendu cairosvg du SVG R2).
  Numérotation des photos des livrables : photo 4 = `P3.jpg`, photo 5 = `P4.jpg`, photo 2 = `P1.jpg`.
  NB : les recadrages RDC de R1 étaient décalés de 5 po en x (constante de repère) ; c'est corrigé dans `scripts/crop.py`. Aucune conclusion de R1 n'en dépendait : les sens de porte avaient été vérifiés aussi dans le JSON et le SVG.

## 1. Suivi des corrections R1

| # | Gravité R1 | État R2 | Preuve |
|---|---|---|---|
| C1 DXF non reproductible | bloquante | **Corrigée** | 3 régénérations dans des copies avec `PYTHONHASHSEED=1`, `=12345` et aléatoire, puis 3 de plus avec une graine aléatoire : les 16 fichiers ont le même sha256, égal à celui des fichiers livrés. Section « Reproductibilité » ajoutée à `verifications.txt`. Voir `preuves_r2/j_sha256_R2.txt`. |
| C2 `ouv-RDC-010` charnière | importante | **Corrigée** | `sens.charniere = "fin"`. Le rendu montre le vantail le long de la cloison du salon, comme sur la photo 5 (`R2_C2_porte_avant_ouv-RDC-010.jpg`). |
| C3 `ouv-RDC-022` (LIN.) | importante | **Corrigée** | `"debut"`, vantail sur le jambage gauche (`R2_C3_porte_LIN_ouv-RDC-022.jpg`). `cote-RDC-059` : « pentures côté gauche (x≈148) ». |
| C4 `ouv-RDC-019` (G.R. arrière) | importante | **Corrigée** | `"debut"` : les deux portes pivotent sur le montant central (`R2_C4_portes_GR_ouv-RDC-019-020.jpg`). |
| C5 `ouv-RDC-026` | importante | **Corrigée** | `"debut"`, vantail côté gauche (x ≈ 279) (`R2_C5_porte_arr_ouv-RDC-026.jpg`). |
| C6 portes SS sans sens | importante | **Corrigée** | `ecart-029` (faible) créé, ⚠29 sur A-100 au mur droit, mesure 28 du RAPPORT §7, renvoi dans les notes de `ouv-SS-005` et `ouv-SS-008`. Remarque : un seul repère, pour la porte 2'-8" ; la porte du caveau n'en a pas (accepté, l'écart couvre les deux). |
| C7 étiquettes G.R. | importante | **Partielle, avec régression** | « G.R. 1 » est maintenant juste (renvoi vers GR1). En revanche, **6 étiquettes sont posées dans une autre pièce**, dont 3 nouvelles : voir R2-1. |
| C8 `lc-RDC-050/051` décollées | importante | **Corrigée (sans objet)** | Les deux lignes ont disparu avec la cloison de l'axe B ; les cotes 18'-7" et 13'-1" restent dans `cotes[]`. Aucune autre cote intérieure n'a son texte hors segment sans renvoi. |
| C9 `mesure` vers des murs erronés | importante | **Corrigée** | cote-RDC-029 à -047 renvoient aux bons murs. Les cloisons retirées sont citées comme « retirée » et existent dans `murs_retires`. |
| C10 références orphelines | importante | **Corrigée** | Plus aucun id orphelin. `elem-SS-ESC` → `cote-SS-055`, `elem-RDC-ESC1` → `cote-RDC-077`, `cote-SS-013` → `elem-SS-CHEM`. Aucune occurrence de `cote-P2-`, `mur-SS-011` ni `elem-SS-TUYAU`. |
| C11 fuites de numérotation | importante | **Corrigée** | `ecart-005` : « feuille RDC (P4, P5 et P6) » ; `cote-RDC-222` : « P4/P5/P6 » ; `ecart-027` : « (P2, P3, P4, P5, P6) » ; ids `cote-IMP-001…012` ; vignettes signalées « (fichiers de travail, numérotation interne) ». Aucun motif interne restant. |
| C12 « Pourquoi » tronqués | mineure | **Corrigée** | Contrôle automatique : aucune parenthèse ni guillemet déséquilibré dans les 28 mesures. Les doublons sur l'arche sont fusionnés (mesure 8 : ⚠3, ⚠17). |
| C13 chambre arrière sans cotes | mineure | **Corrigée** | Étiquette « 11'-1¾" × 12'-0" / ≈136,5 pi² (12,7 m²) », avec « ≈ » car la superficie est ESTIMÉE. |
| C14 « TRAPPE » / ramonage | mineure | **Corrigée** | A-100 : « P. DE RAMONAGE ». |
| C15 rampe de l'escalier SS | mineure | **Non corrigée** | Rien n'est dessiné ni décrit hors de `nom_original` (`R2_C15_SS_escalier_rampe.jpg`) : voir R2-6. |
| C16 texte 2'-6" débordant | mineure | **Corrigée** | `lc-SS-016` : texte sorti sous le segment, avec renvoi ; il ne coupe plus la ligne de rappel (`R2_C16_lc-SS-016.jpg`). |
| C17 ESTIMÉ sans photo | mineure | **Corrigée** | 0 valeur LU ou ESTIMÉ sans photo. |
| C18 dpi des PNG | mineure | **Corrigée** | Les deux PNG font 2550 × 1650 px à 150 dpi. |
| C19 « 9.8° » | mineure | **Corrigée** | « 9,8° » sur les 2 cartouches. |
| C20 « VIDE » | mineure | **Partielle, avec régression** | Le nom devient « Excroissance sous perron », sans la note « contenu inconnu ». L'étiquette est maintenant **en bas de la feuille**, à environ 7 pi de la pièce, et son renvoi traverse les 3 chaînes avant ; elle touche presque « FAÇADE AVANT (RUE) » (`R2_C20_excroissance_label.jpg`) : voir R2-7. |

Bilan : **17 corrigées** (C1–C6, C8–C14, C16–C19), **2 partielles** (C7, C20), **1 non corrigée** (C15).

## 2. Critères d'acceptation, version R2

| # | Critère | Verdict | Preuve |
|---|---|---|---|
| 1 | Topologie (pièces, portes, fenêtres, escaliers, éléments) | **NON** | Portes conformes aux photos 4 et 5 (C2–C5). `ouv-RDC-015` ouvre vers le dégagement : charnière (110,25 ; 163) au nu du mur, vantail vers +x, sans conflit avec les portes -014, -016 et -022. Fenêtres : 14/14. Escaliers : MONTE +y (SS), DESCEND −y (RDC). Aires ouvertes sans mur et colonnes SS signalées par ⚠30. **Mais 6 étiquettes de pièce sont posées dans une autre pièce** (R2-1, `preuves_r2/etiquettes_R2.txt`). |
| a | Cotes : même valeur ou registre | **OK** | Cotes identiques à R0 (160, mêmes valeurs et statuts), dont l'échantillon de 90 vérifié en R1. Les cotes des cloisons retirées (8'-4", 3'-5", 11'-8", 14'-8", 3'-11", 18'-7", 13'-1") ne sont plus dessinées ; elles restent dans `cotes[]`, avec les `mesure` mises à jour et le renvoi ⚠30. |
| b | Chaînes = hors-tout | **OK** | Les 24 chaînes de façade (2 niveaux × 4 façades × 3 rangs) ferment à 456 ou 380, sans trou. Seul écart : `lc-RDC-056` (+1 po), consigné ⚠19. |
| c | Σ pièces + Σ murs = brute (shapely) | **OK** | SS : 1138,06 + 134,28 = 1272,33 = emprise. RDC : 1087,04 pi² de pièces, aucun chevauchement entre pièces, aucun trou. Les 0,24 pi² de recouvrement pièces/murs que donne le calcul en extrémités carrées sont un artefact des bouts libres des cloisons tronquées (0 en extrémités plates) ; le bilan du générateur donne 1087,0 + 161,3 = 1248,3. Superficies = aires des polygones. |
| d | Pièces nommées, cotées, superficie | **OK** | 20 pièces au CSV (SS 3, RDC 17), comme dans le RAPPORT §5. Les étiquettes du plan donnent les dimensions et superficies des pièces principales. Voir R2-1 pour le placement. |
| e | Niveaux superposables | **OK** | Murs ext., caveau / entrée arrière, perron, cheminée inchangés. Les colonnes C02, C05 et C06 ne sont plus sous une cloison : consigné ⚠30 (et ⚠10–12, ⚠24). |
| f | Sens de chaque porte ; fenêtres | **OK** | Toutes les portes RDC ont un `sens`. Les 2 portes SS sans sens sont consignées (`ecart-029`, ⚠29). |
| g | Textes lisibles, sans chevauchement, tailles | **OK** | Cotes 8,798 u = 3,49 mm ; noms 14,076 u = 5,59 mm. Test Liberation Sans : 0 chevauchement texte/texte ; test raster : 0 texte sur un trait (329 textes). |
| h | SVG : XML, 9 calques, viewBox, 17×11 in, rien d'externe | **OK** | Les 2 SVG s'analysent avec lxml ; calques exacts ; `0 0 1088 704` ; aucun href externe ni `<image>` ; calque 90 vide. |
| i | DXF, PDF, échelle graphique | **OK** | DXF R2010 : `audit()` 0 erreur et 0 correction, `$INSUNITS=1`, calques exacts. Ids JSON = SVG = DXF (aucun manquant) et aucun id retiré dans les dessins. PDF : 2 pages de 1224 × 792 pt. Échelle graphique : 144 u = 12 pi × 12 sur les 2 feuilles. |
| j | Régénération identique | **OK** | Voir C1 : 6 régénérations avec 4 graines différentes, tous les sha256 identiques et égaux aux fichiers livrés. |
| k | Normes de dessin | **OK** | Cartouche complet. « ≈ » sur la seule valeur ESTIMÉE affichée (136,5 pi²). Repères ⚠ SS {4, 7, 10, 11, 12, 20, 21, 22, 24, 25, 26, 29} et RDC {2, 3, 5, 6, 7, 9, 13–19, 22, 23, 25, 26, 30}, tous dans le registre. Orange seulement en 70 et en légende ; police Arial, Helvetica, sans-serif. Mineur : ⚠18 est encore dessiné alors que `ecart-018` est « sans objet » (R2-4). |
| l | RAPPORT complet ; photos 1–7 cohérentes | **NON** | Numérotation cohérente partout (aucun motif interne). Le §7 compte 28 mesures triées, avec lieu et raison, et inclut ⚠29 et ⚠30. **Mais le §4 contredit les plans** : « État représenté : les plans d'origine (1957) … Les cloisons de 1957 sont donc conservées » (R2-2). |
| 3 | Cohérence interne de maison.json | **NON (mineur)** | Plus aucune référence orpheline et toutes les sources sont présentes. Mais **l'id `mur-RDC-019` est en double** : trumeau dans `murs`, cloison d'origine dans `murs_retires`. `verifications.txt` annonce « 435 identifiants, aucun doublon » parce qu'il ignore les listes `*_retires` (R2-3). Il reste quelques textes périmés (R2-5). |

Bilan : **11 OK / 3 NON** (topologie des étiquettes, l, cohérence).

## 3. Reproductibilité (demande 3)

Copies de `livrables/` dans le scratchpad, puis `python3 outils/generer_plans.py --sortie <copie>` avec `PYTHONHASHSEED=1`, `=12345` et non défini (aléatoire).
Les 16 fichiers ont le même sha256 entre eux et avec les fichiers livrés : SVG `ec158f5e…` et `7e19b580…`, DXF `0225685b…` et `abdd3c9a…`, PDF `4eff1a02…`, PNG, CSV, verifications et RAPPORT.
Trois autres exécutions aléatoires donnent la même empreinte cumulée DXF + SVG + PDF `d78788de490487ce`. Détail : `preuves_r2/j_sha256_R2.txt`.

## 4. Corrections résiduelles

### R2-1 — Importante — Étiquettes de pièces posées dans une autre pièce (C7 partiel ; 3 régressions)
- **Où** : A-101, calque 60-Etiquettes. Coordonnées SVG ; les renvois se terminent bien dans la bonne pièce, mais le texte est lu dans la pièce voisine.

  | Étiquette (pièce) | Texte posé à (SVG) | Pièce où l'on lit le texte | R0 → R2 |
  |---|---|---|---|
  | HALL (`piece-RDC-HALL`) | (420,8 ; 490,0), soit maison y ≈ 48 | **ENTRÉE**, à 100 % | nouveau (en R0, HALL était dans sa pièce) |
  | ENTRÉE (`piece-RDC-ENT`) | (480,5 ; 523,8) | **SALON**, à 100 % | déjà en R0 |
  | LIN. (`piece-RDC-LIN`) | (416,1 ; 422,8) | **HALL**, à 100 % | déjà en R0 (alors dans le dégagement) |
  | VEST. (`piece-RDC-VES`) | (368,3 ; 454,6) | CHAMBRE AVANT 47 % et G.R. 42 %, dans la baie de `ouv-RDC-021` | nouveau |
  | G.R. 2 (`piece-RDC-GR2`) | (397,7 ; 272,1) | **boîte G.R. 3** 46 % et SALLE À MANGER 43 % | nouveau (même défaut qu'en R1, décalé d'une boîte) |
  | G.R. 3 (`piece-RDC-GRU`) | (424,2 ; 292,5) | **SALLE À MANGER**, à 100 % | déjà en R0 (alors dans la chambre arrière) |

  ESCALIER (renvoi d'environ 90 u qui traverse le mur arrière et la chaîne 3'-0") et G.R. 1 (renvoi qui croise la chaîne arrière) sont hors de toute pièce : c'est acceptable, mais le renvoi est long.
- **Preuve** : `preuves_r2/etiquettes_R2.txt` (part du texte dans sa pièce ou dans une autre), `R2_zone_hall_vest_lin_gr.jpg`, `R2_zone_ouverte_RDC.jpg`. Le contrôle « 17 étiquettes… dans sa pièce ou reliée par un renvoi » de `verifications.txt` passe, car il ne teste que le bout du renvoi.
- **Correction (générateur)** :
  - (a) Essayer d'abord de poser le nom **dans sa pièce**, horizontal puis vertical, à 14,076 u puis 12,317 u (4,9 mm ≥ 4 mm).
    Ces tailles tiennent toutes dans leur pièce : HALL vertical (91,75 po), ENTRÉE vertical (50,75 po) et VEST. vertical à 12,3 u (41,75 po).
  - (b) Sinon, placer le texte dans une zone qui n'appartient à **aucune pièce nommée**, hors du bâtiment ou dans le dégagement à la rigueur, avec un renvoi court.
  - (c) Ajouter à `verifications.txt` le contrôle « boîte du texte ∩ autre pièce < 20 % de la boîte », en ERREUR.

### R2-2 — Importante — RAPPORT §4 en contradiction avec l'état dessiné
- **Où** : `RAPPORT.md` §4, 1re puce, générée par `outils/generer_rapport.py`. Elle dit : « État représenté : les plans d'origine (1957). … Les cloisons de 1957 sont donc conservées et chaque différence est consignée ».
  Or A-101 applique maintenant le constat du propriétaire : cloisons retirées, aires ouvertes, porte de la S. de bain inversée (⚠30).
- **Correction** : écrire « État représenté : plans d'origine (1957) corrigés par le constat du propriétaire du 2026-10-29 (⚠30 : cloisons de la cage d'escalier, du balais et des axes B et C retirées, mobilier retiré, porte de la S. de bain inversée). Les autres cloisons absentes du croquis 2016 sont conservées (⚠9). » Ajuster de même l'introduction (« reproduit… les plans d'origine »).

### R2-3 — Mineure — Id `mur-RDC-019` en double
- **Où** : `maison.json`, `niveaux[RDC].murs` (trumeau x 439,5–451) et `murs_retires` (cloison d'origine x 222–451).
- **Correction** : renommer la copie retirée `mur-RDC-019-1957` (ou donner un nouvel id au trumeau, par ex. `mur-RDC-030`) et mettre à jour `cote-RDC-045`, `cote-RDC-046`, `ecart-013` et `ecart-030`.
  Étendre le contrôle d'unicité de `verifications.txt` à `murs_retires`, `ouvertures_retirees` et `elements_retires`.

### R2-4 — Mineure — Repère ⚠18 dessiné pour un écart « sans objet »
- **Où** : A-101, ⚠18 sur l'axe C vers x ≈ 160 (`R2_marqueur_18_sans_objet.jpg`). `ecart-018.statut = "sans objet"` : la porte -017 et sa cloison n'existent plus.
- **Correction** : ne pas dessiner les repères des écarts dont le statut n'est pas « ouvert », ou retirer `ecart-018.position`. Vider aussi `a_valider_sur_place` (« Mesurer la largeur et la position de la porte de la chambre d'utilité »). Facultatif : ajouter un second repère ⚠29 sur la porte du caveau (x = 261, y = 375).

### R2-5 — Mineure — Textes périmés après le constat
- `ecart-022` : « RDC cage 36½ po DÉDUIT » et « position alignée sur la cage du RDC » → « largeur 3'-5" à l'axe des anciennes cloisons (cote-RDC-033), cage retirée (⚠30) ».
- `elem-RDC-ESC1.dimensions.largeur.note` : « entre cloisons x = 23'-0" et 26'-4" » → « entre les axes des anciennes cloisons (retirées) ».
- `cote-RDC-058.emplacement` : « ouvre dans la S. de bain (-x) » → ajouter « (plan 1957 ; ouvre aujourd'hui vers le dégagement, constat 2026-10-29) ».
- RAPPORT §7, mesure 14 : « chambre d'utilité » → « salle à manger (ancienne chambre d'utilité) ».

### R2-6 — Mineure — Rampe de l'escalier du sous-sol absente (C15 non corrigée)
- **Où** : A-100, `elem-SS-ESC`. « RAMPE » est écrit sur la photo 2, avec une flèche vers le côté gauche de la volée (x ≈ 275).
- **Correction** : ajouter dans `elem-SS-ESC.note` la mention « rampe côté gauche (x ≈ 275, ESTIMÉ, photo 2) » ou un trait ESTIMÉ. Au RDC, le garde-corps est déjà à constater (⚠30).

### R2-7 — Mineure — Étiquette « EXCROISSANCE SOUS PERRON » mal placée (C20 partiel)
- **Où** : A-100. Texte au centre (267,8 ; 675,4) SVG, au bas de la feuille, à environ 10 u de « FAÇADE AVANT (RUE) ». Son renvoi (378,1 ; 664,7) → (391,2 ; 580,0) traverse les rangs 1 à 3 de la chaîne avant.
- **Correction** : placer l'étiquette à gauche de l'excroissance, entre le mur avant et la chaîne de rang 1 (vers x = 100, y = −25 dans le repère maison), avec un renvoi court, ou sur 2 lignes « EXCROISSANCE / SOUS PERRON ». Ajouter la note « contenu (vide ou remblai) inconnu » à `piece-SS-PERRON`.

### R2-8 — Mineure — Limites des zones ouvertes non dessinées
- **Où** : A-101. Les dimensions de la salle à manger (10'-6¾", jusqu'à x = 275), de la cuisine (10'-10", depuis x = 316) et de la zone escalier (3'-5") s'appuient sur des **limites invisibles**, les axes des cloisons retirées. Seuls les axes B et C sont tracés.
- **Correction** : tracer les limites de zones en tireté fin gris (calque 60) aux x = 275 et 316, ou ajouter à la légende « limites des zones ouvertes = axes des cloisons retirées (⚠30) ».

### R2-9 — Mineure — Textes de cotes déplacés loin de leur segment
- **Où** : `lc-SS-043` (7'-4", texte 36 po après la fin du segment ; le renvoi traverse l'escalier et la colonne C03, `R2_lc-SS-043_renvoi_escalier.jpg`) ; `lc-RDC-045` (5'-6" de la S. de bain, texte 37 po plus haut, lu dans la chambre arrière) ; `lc-RDC-035` (3'-2", 36 po) ; `lc-SS-031` (6'-8", 38 po, déjà en R0).
- **Correction (générateur)** : limiter le déplacement d'un texte de cote à environ 1,5 fois sa longueur, en le collant à l'extrémité du segment côté libre ; interdire qu'un renvoi croise un élément de 30-Escaliers-Elements ou une colonne.

## 5. Totaux

- Suivi R1 : **17 corrigées, 2 partielles (C7, C20), 1 non corrigée (C15)**.
- Critères R2 : **11 OK / 3 NON** (topologie des étiquettes, l, cohérence).
- Corrections résiduelles : **0 bloquante, 2 importantes** (R2-1, R2-2), **7 mineures** (R2-3 à R2-9).
