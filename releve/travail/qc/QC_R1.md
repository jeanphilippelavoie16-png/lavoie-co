# QC R1 — Contrôle qualité indépendant (Phase 4) — 86, av. Laurier, Baie-Comeau

Contrôleur : agent QC indépendant (lecture seule). Date : 2026-10-29.

## 0. Base contrôlée et périmètre

- **Base figée** : le commit `af231be` (« Relevé R0 : plans générés… »), extrait en lecture seule dans le scratchpad.
  `maison.json` sha256 `0b488ad4aabc…` (c'est la même empreinte que dans `verifications.txt`). Pendant le contrôle (vers 01:04 UTC),
  le dossier `livrables/` a été **modifié par une autre session** (retrait des cloisons axe B/C, cage d'escalier, balais :
  `mur-RDC-026/027/028` supprimés, `mur-RDC-019` raccourci). Toutes les corrections ci-dessous visent des identifiants qui
  existent toujours, sauf mention contraire.
- **Exclusions demandées par le coordonnateur** (constat du propriétaire, changements appliqués après le QC) : je ne signale aucun défaut
  sur les cloisons de la cage d'escalier ou du placard à balais, ni sur les cloisons axe C (y≈204) et axe B (y≈157). Rien non plus sur
  la zone escalier / balais / passage / cuisine ni sur le mobilier, les électroménagers, les comptoirs ou la baignoire.
  Cela touche `ouv-RDC-017`, `-023`, `-024` et `-025`, `elem-RDC-*` du mobilier et l'étiquette « ESCALIER ».
- **Choix assumés, non signalés** : état 1957 ; écarts avec le croquis 2016 portés au registre ; aucune mesure sur place ;
  hauteurs inconnues ; murs porteurs « inconnu » ; petites pièces non cotées sur le plan.
- **Numérotation des photos** : toujours celle des livrables (photo 1 = croquis 2016 … photo 7 = implantation).
  Correspondance des fichiers de travail : photo 2 = `P1.jpg`, photo 3 = `P7.jpg`, photo 4 = `P3.jpg`, photo 5 = `P4.jpg`,
  photo 6 = `P6.jpg`, photo 1 = `P2.jpg`, photo 7 = `P5.jpg`. Dans les paires de preuve, l'image de gauche est l'original
  (`prep/redresse/`) et celle de droite le SVG rendu par cairosvg (5100 px de large).
- Outils : `travail/qc/scripts/crop.py` (paires original / rendu) et `planche.py` (planches de cotes) ; preuves dans `travail/qc/preuves/`.

## 1. Tableau des critères

| # | Critère | Verdict | Preuve |
|---|---|---|---|
| 1 | Topologie SVG ↔ photos (pièces, enchaînements, portes, fenêtres, escaliers, éléments fixes) | **NON** | Pièces, fenêtres (SS 6 + 2 portes ; RDC 8 fenêtres), escaliers MONTE (SS, +y) / DESCEND (RDC, −y), cheminée, caveau, perron : conformes (`z_ss_*.jpg`, `z_rdc_*.jpg`). **4 portes RDC ont la charnière du mauvais côté** : C2–C5. **Étiquettes des G.R. décalées** : C7. |
| a | Cotes : même valeur ou registre (échantillon ≥ 30) | **OK** | 90 cotes contrôlées sur les photos (36 SS, photo 2 ; 54 RDC, photos 4 et 6), sur les 4 façades et l'intérieur : `planche_cotes_SS_1/2.jpg`, `planche_cotes_RDC_1/2/3.jpg`. Toutes identiques à `cotes[]` et aux plans. Les glyphes ambigus sont au registre (SS-006 ⚠20, SS-017 ⚠4, RDC-018 ⚠2, RDC-048 ⚠3) ou tranchés par bouclage, documenté dans `contrainte_de_bouclage` (SS-004 10'-9", SS-014 7'-0", RDC-023 6'-9"). Aucune cote de l'original absente de `cotes[]` (portes 2'-4"/2'-6"/2'-8"/1'-9"/2'-10" : 4/5/4/1/2, toutes présentes). |
| b | Chaînes = hors-tout à ½ po | **OK** | Recalcul indépendant sur `lignes_cote` : chaque façade et chaque rang 1-2-3 donne 456 / 380 sans trou ni chevauchement. Seul écart : `lc-RDC-056` dessinée 2'-10" pour 2'-9" attendue, consignée ⚠19. |
| c | Σ pièces + Σ murs = brute (shapely) | **OK** | Union des murs en tampon à extrémités carrées, à partir de `maison.json`. SS : 1138,06 + 134,28 = 1272,33 = emprise 1272,33 pi², aucun trou. RDC : 1062,16 + 186,21 = 1248,36 pour une emprise de 1248,33 pi² ; recouvrement pièces/murs 0,03 pi², aucun trou. Superficies du JSON = aires des polygones (±0,05). |
| d | Pièces nommées, cotées (CSV), superficie | **OK** | Les 22 pièces sont au CSV avec dimensions et superficie. Remarque mineure C13 : la chambre arrière (136,5 pi²) n'a ni dimensions ni superficie sur le plan. |
| e | Niveaux superposables | **OK** | Murs ext. identiques (0–456 × 0–380). Caveau et entrée arrière superposés (219–327 × 380–440). Perron : SS 162–234, RDC 164–231. Cheminée : y = 142,8 (SS) et 142 (RDC). Escalier à 5 po près (⚠22), plomberie (⚠25) et colonnes (⚠10–12, ⚠24) consignés. |
| f | Chaque porte a un sens ; chaque fenêtre dessinée | **NON** | Fenêtres : 14/14 dessinées. Portes : `ouv-SS-005` et `ouv-SS-008` n'ont **aucun sens** (operation « aucune ») et ne figurent pas au registre (C6). 4 sens RDC sont faux (C2–C5). |
| g | Textes lisibles, sans chevauchement ; tailles imprimées | **NON (mineur)** | Tailles : cotes 8,798 u = **3,49 mm** (≥ 2,5) ; noms de pièces 14,076 u = **5,59 mm** et 12,317 u = 4,89 mm (≥ 4). Aucun chevauchement texte/texte (test Liberation Sans). En revanche, « 2'-6" (0,76 m) » (SS, `lc-SS-016`) déborde sa cote de 30 po et coupe la ligne de rappel y = 0 (C16, `C_texte_2-6_SS.jpg`). Les textes 18'-7" / 13'-1" de `lc-RDC-050/051` sont décollés de leur ligne (C8). |
| h | SVG : XML, 9 calques, viewBox, 17×11 in, pas de ressource externe | **OK** | lxml : les 2 SVG s'analysent ; 9 calques dans l'ordre exact ; `width="17in" height="11in" viewBox="0 0 1088 704"` (1 u = 1 po réel à 3/16" = 1'-0") ; aucun `href` externe ni `<image>` ; calque 90 vide. |
| i | DXF, PDF, échelle graphique | **OK** | `ezdxf.readfile` + `audit()` : 0 erreur, 0 correction ; `$INSUNITS = 1` (pouces) ; 11 calques (les 9 + 0 + Defpoints). PDF : 2 pages de 1224 × 792 pt. Échelle graphique : barre 876,16 → 1020,16 = **144 u = 12 pi × 12**, segments de 48 u = 4 pi (2 feuilles). Mineur : les PNG n'ont pas de métadonnée dpi (C18). |
| j | Régénération identique (2 exécutions dans une copie) | **NON** | SVG, PDF, PNG, CSV, verifications et RAPPORT ont le même sha256 à chaque exécution et égal au livré. **DXF non déterministe** : sur 6 exécutions, 2 variantes alternent (SS `3a509c6c…` / `055e2c2c…`, RDC `8d77fa8b…` / `01b9a342…`). Seule l'ordre des objets LAYOUT / ACDBPLACEHOLDER change ; il dépend de `PYTHONHASHSEED` (deux graines fixes 1 et 2 donnent toujours `055e…`). Preuve : `preuves/j_hash_dxf.txt` (C1). |
| k | Normes de dessin | **OK (mineur)** | Le cartouche contient projet, niveau, n° de feuille, échelle 3/16" = 1'-0", date 2026-10-29, R0, photos sources (A-100 : P2, P3 ; A-101 : P4, P5, P6) et la mention « RELEVÉ DE L'EXISTANT — PRÉLIMINAIRE, À VALIDER SUR PLACE ». Aucune cote ESTIMÉE affichée, donc pas de « ≈ » requis. ⚠n : 26 repères, tous liés à un `ecart` existant. Orange #E8730C seulement dans 70-Incertitudes et la légende ; sinon noir et gris. Textes en `<text>` Arial, Helvetica, sans-serif. Mineur : « 9.8° » s'écrit avec un point (C19). |
| l | RAPPORT.md complet ; numéros de photos cohérents | **NON** | Le rapport contient les photos, la convention, les hypothèses, le registre et les mesures triées par impact avec le lieu et la raison. Mais la numérotation interne fuit (C11) : `ecart-005` « aucune épaisseur écrite sur P3 », `cote-RDC-222` « P4/P4/P6 », `ecart-027` « (P2/P3) », identifiants `cote-P5-0xx` pour la photo 7, renvois `cote-P2-0xx`. Les raisons « Pourquoi » sont tronquées avec des parenthèses non fermées (C12). |
| 3 | Cohérence interne de maison.json | **NON** | Les identifiants JSON, SVG et DXF (XDATA « RELEVE ») correspondent à 100 % : SS 105 et RDC 152 ids, aucun manquant. Mais les champs `mesure` des cotes RDC-030 à -046 renvoient à des **murs erronés** (renumérotation, C9). Il y a aussi des **références orphelines ou fausses** (C10) et 29 valeurs ESTIMÉ sans photo (C17). |

Bilan : **8 critères OK, 6 NON** (critère de topologie compris).

## 2. Liste numérotée des corrections

Gravité : **bloquante** = critère d'acceptation explicite en échec, à corriger avant diffusion ; **importante** = information fausse
ou trompeuse sur une feuille ou dans les données ; **mineure** = présentation ou traçabilité.

### C1 — Bloquante — DXF non reproductible (critère j)
- **Où** : `outils/generer_plans.py`, `dxf_feuille()` (l. 2731–2834) ; les 2 DXF.
- **Faux** : deux exécutions de `generer_plans.py --sortie <copie>` donnent des DXF différents. Section OBJECTS : l'ordre LAYOUT / ACDBPLACEHOLDER
  varie selon la graine de hachage de Python. SVG, PDF, PNG et CSV sont identiques.
- **Preuve** : `preuves/j_hash_dxf.txt` (6 exécutions, 2 variantes ; `diff` lignes 1326–1344). Avec `PYTHONHASHSEED=1` ou `=2`, toujours `055e2c2c…`.
- **Correction (générateur)** : au début de `main()`, si `os.environ.get("PYTHONHASHSEED") != "0"`, relancer le script avec
  `os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "PYTHONHASHSEED": "0"})`. On peut aussi trier la
  collection d'objets avant `saveas`. Ajouter à `verifications.txt` un contrôle qui génère deux fois le DXF en mémoire et compare les sha256.

### C2 — Importante — Porte d'entrée avant : charnière du mauvais côté
- **Où** : A-101, `ouv-RDC-010` (mur-RDC-001, centre x = 199, y = 5).
- **Faux** : `sens.charniere = "debut"`, donc charnière à x ≈ 182, côté vestibule. Sur l'original, le vantail est dessiné le long de la
  cloison du salon : charnière à x ≈ 216. La note de l'ouverture (« pentures côté salon ») et `cote-RDC-063`
  (« pentures côté droit (côté salon, x≈216) ») le disent aussi, mais la donnée les contredit.
- **Preuve** : `C_porte_avant_ouv-RDC-010.jpg` (photo 5) ; `photo5_zoom_porte_avant_ouv-RDC-010.jpg` ; `photo4_zoom_porte_avant_vest.jpg`.
- **Correction (maison.json)** : `ouv-RDC-010.sens.charniere` : `"debut"` → `"fin"` (`ouvre_vers` reste `"gauche"`, vers l'intérieur).

### C3 — Importante — Porte de la lingerie : charnière inversée
- **Où** : A-101, `ouv-RDC-022` (mur-RDC-012, centre x = 160,5, y = 157).
- **Faux** : charnière à droite (x ≈ 171) ; sur l'original, le vantail ouvert est dessiné verticalement sur le **jambage gauche** (x ≈ 148),
  avec un arc vers le jambage droit. Photos 4 et 5 concordantes.
- **Preuve** : `C_porte_lin_ouv-RDC-022.jpg`, `photo5_zoom_porte_LIN_ouv-RDC-022.jpg`, `photo4_zoom_portes_ch-avant_LIN_GR.jpg` (en haut au centre).
- **Correction (maison.json)** : `ouv-RDC-022.sens.charniere` : `"fin"` → `"debut"` (`ouvre_vers "gauche"` = +y, inchangé). Corriger aussi
  `cote-RDC-059.emplacement` : « pentures côté droit (x≈175) » → « pentures côté gauche (x≈148) ».

### C4 — Importante — Porte du G.R. arrière de la chambre arrière : charnière inversée
- **Où** : A-101, `ouv-RDC-019` (mur-RDC-021 x = 146, centre y = 354).
- **Faux** : `charniere = "fin"`, donc charnière à y ≈ 368, contre le mur arrière. Sur l'original, les deux portes des G.R. pivotent sur le
  **montant central commun** : la porte du haut a sa charnière en bas (y ≈ 340). C'est aussi ce que dit `cote-RDC-053` (« pentures
  sur le montant central (côté avant, y≈345) »). `ouv-RDC-020` est juste.
- **Preuve** : `C_porte_GR_arriere_ouv-RDC-019.jpg` (photo 5), `photo5_zoom_portes_GR_ouv-RDC-019-020.jpg`, `photo4_zoom_GR_chambre_arriere.jpg`.
- **Correction (maison.json)** : `ouv-RDC-019.sens.charniere` : `"fin"` → `"debut"` (`ouvre_vers "gauche"` = −x, vers la chambre, inchangé).

### C5 — Importante — Porte de l'entrée arrière vers le palier : charnière inversée
- **Où** : A-101, `ouv-RDC-026` (mur-RDC-003, centre x = 295, y = 375). Porte du mur extérieur, hors cloisons retirées.
- **Faux** : charnière à x ≈ 311 (« fin »). Sur l'original, le vantail est dessiné le long du **côté gauche**, cloison de la chambre
  d'utilité (x ≈ 279), avec un arc vers le jambage droit. C'est aussi ce que dit `cote-RDC-051` (« pentures côté gauche »).
- **Preuve** : `z_rdc_porte_arr_ouv-RDC-026.jpg` (photo 5).
- **Correction (maison.json)** : `ouv-RDC-026.sens.charniere` : `"fin"` → `"debut"` (`ouvre_vers "droite"` = −y, vers le palier, inchangé).

### C6 — Importante — Deux portes du sous-sol sans sens d'ouverture, non consignées (critère f)
- **Où** : A-100, `ouv-SS-005` (« PORTE 2'-8" », mur droit, y = 75) et `ouv-SS-008` (« PORTE 2'-6" », caveau, x = 261).
- **Faux** : `operation "aucune"`, pas de `sens`, aucun écart ni repère ⚠. L'original ne dessine qu'un rectangle barré d'un X, sans arc.
  Les tiretés près de la porte 2'-8" sont des circuits électriques et non un battant : `z_ss_droite_bas.jpg`.
- **Preuve** : `z_ss_droite_bas.jpg`, `z_ss_arriere.jpg` (photo 2).
- **Correction (maison.json)** : créer un écart (impact faible) « Sens d'ouverture non dessiné (rectangle barré d'un X) pour ouv-SS-005 et ouv-SS-008 ».
  Lui donner `position` [451, 75] (un repère par porte, ou un repère commun), une `a_valider_sur_place` « constater battant, charnière et côté
  d'ouverture », un `ref` dans chaque ouverture et une mesure dans RAPPORT §7. N'inventer aucun sens.

### C7 — Importante — Étiquettes des G.R. de la chambre arrière : « G.R. 1 » posée dans G.R. 2
- **Où** : A-101, 60-Etiquettes. Le texte « G.R. 1 » est en SVG (367,5 ; 219,3), soit maison (149,3 ; 319,2), **dans `piece-RDC-GR2`** (y 298–335).
  « G.R. 2 » est hors du bâtiment (maison y ≈ 387) avec un renvoi vers (156,5 ; 332), donc lui aussi dans GR2. La boîte du haut, `piece-RDC-GR1`
  (y 340–370), n'a aucune étiquette.
- **Preuve** : `A-101_zoom_etiquettes_GR.jpg`, `C_portes_GR_ouv-RDC-019_GR1_label.jpg`.
- **Correction (générateur)** : placer l'étiquette d'une petite pièce soit dans son propre polygone, soit hors du polygone avec un renvoi qui
  **se termine dans ce polygone**. Ajouter à `verifications.txt` le contrôle « point d'ancrage ou bout de renvoi ∈ polygone de la pièce ».
  À défaut, intervertir les noms affichés de GR1 et GR2 pour que l'étiquette posée corresponde à la boîte.

### C8 — Importante — Cotes intérieures 18'-7" / 13'-1" (côté cuisine/salon) décollées de leur ligne
- **Où** : A-101, `lc-RDC-050` (ref cote-RDC-045, 18'-7") et `lc-RDC-051` (ref cote-RDC-046, 13'-1"), avec p1/p2 à x = 355.
- **Faux** : le générateur dessine la ligne à x ≈ 454,5, **dans l'épaisseur du mur ext. droit** (446–456). Les textes ont `text-anchor`
  start / end et tombent **hors des extrémités** : 18'-7" au-dessus de la façade arrière (SVG y 155), 13'-1" sous la façade avant (SVG y 542),
  près des chaînes avant. Les rappels traversent la cuisine et le salon à y = 157.
- **Preuve** : `C_cotes_lc-RDC-050-051_hors_ligne.jpg` ; le SVG `<g id="lc-RDC-051">` (ligne x = 672,698, texte y = 541,755, anchor end).
- **Correction** : (a) dans le générateur, pour `facade = "int"`, garder la ligne à p1/p2 + `decalage` et centrer le texte sur le segment.
  Si le texte ne tient pas, le placer à côté avec un renvoi, jamais au-delà des extrémités ni dans un mur. (b) Si le déplacement est
  voulu, mettre dans maison.json `lc-RDC-050/051.decalage` à une valeur explicite qui garde la ligne dans la pièce (par ex. 0 à x = 355).

### C9 — Importante — `mesure` des cotes RDC : renvois vers des murs erronés (renumérotation)
- **Où** : `maison.json`, RDC `cotes[]`, champ `mesure`. La géométrie et les valeurs sont justes ; seuls les ids cités sont faux.
- **Faux et correction** (mur cité → mur réel) :
  - `cote-RDC-030` : « mur-RDC-013/014 » → `mur-RDC-021` (x = 146, côté arrière) ;
  - `cote-RDC-031` : « mur-RDC-013 → mur-RDC-015 » → `mur-RDC-021 → mur-RDC-022` (x = 146 → 175) ;
  - `cote-RDC-032` : « mur-RDC-015 → mur-RDC-021 » → `mur-RDC-022 → mur-RDC-027` (x = 175 → 275) ;
  - `cote-RDC-033` : « mur-RDC-021 → mur-RDC-022 » → `mur-RDC-027 → mur-RDC-028` ;
  - `cote-RDC-034` : « mur-RDC-022 » → `mur-RDC-028` ;
  - `cote-RDC-038` : « mur-RDC-026 » → `mur-RDC-013` ;
  - `cote-RDC-039` : « mur-RDC-026 → mur-RDC-027 » → `mur-RDC-013 → mur-RDC-014` ;
  - `cote-RDC-040` : « mur-RDC-027 → mur-RDC-025 » → `mur-RDC-014 → mur-RDC-018` ;
  - `cote-RDC-041` : « mur-RDC-025 » → `mur-RDC-018` ;
  - `cote-RDC-042` : « mur-RDC-020 » → `mur-RDC-026` (axe C) ;
  - `cote-RDC-043` : « mur-RDC-020 → mur-RDC-024 » → `mur-RDC-026 → mur-RDC-019` ;
  - `cote-RDC-044/045/046` : « mur-RDC-024 » → `mur-RDC-019` (axe B).

  Si la cloison axe B/C est retirée dans la version propriétaire, citer l'axe (`str-RDC-AXB` / `str-RDC-AXC`) plutôt qu'un mur supprimé.
  Le même décalage d'ids existe dans les notes des murs : `mur-RDC-019` cite « cote-RDC-044, -046 » (correct), mais vérifier toutes les
  `note` avec un script qui compare la géométrie de chaque mur cité.

### C10 — Importante — Références orphelines ou fausses dans maison.json
- `elem-SS-ESC.escalier.nb_contremarches.ref = "cote-SS-056"` : c'est l'échelle → `"cote-SS-055"` (14 C.M.).
- `elem-RDC-ESC1.escalier.nb_contremarches.ref = "cote-RDC-079"` : cet id n'existe pas → `"cote-RDC-077"`.
- `elem-SS-CHEM.note` et `cote-SS-013.mesure` citent `mur-SS-011`, qui n'existe pas : remplacer par `elem-SS-CHEM` (face avant du massif).
- `elem-SS-FOUR.note` et `elements_electriques_non_reportes` citent `elem-SS-TUYAU`, `elem-SS-VIROLE`, `elem-SS-LUMn`,
  etc. Ces ids sont absents : soit les écrire sans préfixe d'id, soit créer des objets.
- Les renvois `cote-P2-001…026` (anciens ids du croquis 2016) dans les `note` de `cote-RDC-201…226`, et les `contrainte_de_bouclage` de
  `cote-SS-046` (cote-P2-011/012), `cote-RDC-038` (cote-P2-003/004) et `cote-RDC-218` (cote-P2-008) → `cote-RDC-2nn` (même numéro + 200).
- **Preuve** : script de contrôle des ids (section 3 ci-dessous).

### C11 — Importante — Numérotation interne des photos visible dans les livrables (critère l)
- `ecart-005.description` (et RAPPORT ⚠5) : « aucune épaisseur écrite sur **P3** » → « sur les photos 4, 5 et 6 ».
- `cote-RDC-222.mesure` : « les lire sur P4/**P4**/P6 » → « P4/P5/P6 ».
- `cote-RDC-218`, `-220`, `-222` (`lecture_3.justification`, `cotes[94]`, `[95]`, `[97]`) : « sur **P3** » → « sur P4 ».
  `cotes[99]` : « pas sur **P2** » → « pas sur P1 ».
- `ecart-027.hypothese_retenue` : « Plans de 1957 (**P2/P3**) retenus pour la géométrie » → « (P2 à P6) ».
- Ids de l'implantation `cote-P5-001…012` (photo 7) : renommer `cote-IMP-001…012` et mettre à jour `ecart-001`, la mesure 16 du RAPPORT et
  les vignettes citées.
- Les noms de vignettes dans les écarts (`d-RDC-03_P4.png` = photo 5, `d-RDC-11_P3.png` = photo 4…) prêtent à confusion : ajouter « (fichier de travail,
  numérotation interne) » ou la photo livrable entre parenthèses.

### C12 — Mineure — RAPPORT §7 : raisons tronquées, parenthèses non fermées
- **Où** : `outils/generer_rapport.py`. Mesures 4, 5, 10, 11, 18, 26 (ex. « …(str-SS-P02 y = 10" + 12'-3" (⚠13, RDC) » ; « …(aucune coupe ni élévation (⚠8, global) »).
- **Correction (générateur)** : couper à la fin d'une phrase (« . ») ou équilibrer les parenthèses, ou citer la description complète. Fusionner
  les mesures 7 et 14, qui portent toutes deux sur l'arche hall/salon.

### C13 — Mineure — Chambre arrière sans dimensions ni superficie sur le plan
- **Où** : A-101, `piece-RDC-CH1` (136,5 pi², 11'-1¾" × 12'-11¾" au CSV). Ce n'est pas une « petite pièce » : afficher les 2 lignes comme pour la chambre avant.
  La boîte englobante inclut l'alcôve de la porte : préciser les dimensions principales 11'-1¾" × 12'-0" (144 po) ou garder l'ESTIMÉ avec « ≈ ».

### C14 — Mineure — « TRAPPE » au sous-sol désigne la porte de ramonage
- **Où** : A-100, `elem-SS-RAMO` (étiquette « TRAPPE » à x ≈ 10, y ≈ 146). L'original dit « PORTE DE RAMONAGE » (photo 2, `z_ss_gauche.jpg`).
  « TRAPPE » sert aussi pour la trappe d'entretoit du RDC. Afficher « P. DE RAMONAGE ».

### C15 — Mineure — Rampe de l'escalier du sous-sol non représentée
- **Où** : A-100, `elem-SS-ESC`. La « RAMPE », avec sa flèche vers le côté gauche de la volée, est écrite sur la photo 2 (`z_ss_escalier.jpg`).
  L'ajouter (trait le long de x ≈ 275, ESTIMÉ) ou la noter dans l'élément.

### C16 — Mineure — Texte de cote plus long que son segment (SS)
- **Où** : A-100, `lc-SS-016` (2'-6" = 30 po, chaîne gauche rang 1, y 0–30). Le texte « 2'-6" (0,76 m) » mesure environ 52 u et coupe la ligne de
  rappel y = 0 (`C_texte_2-6_SS.jpg`). Le contrôle « Textes (chevauchements) » n'a rien vu.
- **Correction (générateur)** : si la longueur du texte dépasse le segment, le sortir avec un renvoi ou passer le métrique sur une 2e ligne.
  Étendre la vérification texte/trait aux lignes de rappel.

### C17 — Mineure — Valeurs ESTIMÉ sans photo
- **Où** : 29 objets `superficie` et `dimensions` des pièces RDC (CH1, GR1, GR2, GRU, DEG, HALL, ENT, VES, GRA, LIN, PAS, BAL, ESC) : `source "ESTIMÉ"`, `photo null`.
  Mettre `"photo": "P4"`, la photo d'où viennent les positions estimées des cloisons.

### C18 — Mineure — PNG sans résolution déclarée
- `png/*.png` font 2550 × 1650 px sans métadonnée dpi, alors que le RAPPORT annonce 150 ppp. Sauvegarder avec `dpi=(150, 150)`.

### C19 — Mineure — Format du nord
- Cartouche des 2 feuilles : « 9.8° » → « 9,8° », pour suivre la virgule décimale utilisée partout ailleurs.

### C20 — Mineure — Nom « VIDE » non écrit sur l'original
- `piece-SS-PERRON` (« Vide ») : l'original ne nomme pas l'excroissance sous le perron et ne dit pas qu'elle est vide. Renommer
  « Excroissance sous perron », garder `nom_original "(aucun nom au plan)"` et ajouter une note « contenu (vide/remblai) inconnu ».

## 3. Contrôles automatiques indépendants (résumé)

- Ids : 488 ids, aucun doublon. JSON ⊂ SVG et JSON ⊂ DXF pour les murs, ouvertures, pièces, éléments, structure et lignes de cote.
- Sources : toutes les valeurs `LU` ont une photo. `DÉDUIT` a toujours une note ou un ref. Aucune valeur `ILLISIBLE` n'est chiffrée.
  Exception : les 29 ESTIMÉ sans photo de C17.
- Sens des portes recalculés à partir de (mur, position, largeur, charnière) et comparés aux notes des cotes : 4 contradictions
  (`ouv-RDC-010`, `-019`, `-022` par rapport aux photos ; `-026`). `ouv-RDC-023` est contradictoire aussi, mais hors périmètre (balais).
- Scripts : `travail/qc/scripts/crop.py`, `travail/qc/scripts/planche.py`. Les calculs shapely, ezdxf et pypdf ont été lancés en ligne de commande
  sur l'instantané `af231be`.

## 4. Totaux

- Critères : **8 OK / 6 NON** (topologie, f, g, j, l, cohérence 3).
- Corrections : **1 bloquante** (C1), **10 importantes** (C2 à C11), **9 mineures** (C12 à C20).
