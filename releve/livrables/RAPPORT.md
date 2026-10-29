# Relevé de l'existant — Résidence — 86, avenue Laurier, Baie-Comeau

**RELEVÉ DE L'EXISTANT — PRÉLIMINAIRE, À VALIDER SUR PLACE** · Révision R0 · 2026-10-29

Ce relevé reproduit, en plans propres et modifiables, les plans d'origine dessinés à la main (1957), corrigés par le constat du propriétaire (cloisons disparues, porte de la salle de bain). Il ne contient aucune proposition de rénovation. Aucune mesure n'a été prise sur place : toutes les dimensions viennent des documents photographiés, avec leur source.

## 1. Livrables

| Dossier | Contenu |
|---|---|
| `svg/` | Une feuille par niveau (A-100 Sous-sol, A-101 Rez-de-chaussée), calques Inkscape, 1 unité = 1 po réel, tabloïd 17 × 11 po à l'échelle |
| `pdf/plans_existants.pdf` | Toutes les feuilles, à l'échelle (vérifier avec l'échelle graphique du cartouche) |
| `png/` | Aperçus 150 ppp |
| `dxf/` | Un fichier par niveau, unités en pouces, mêmes calques et identifiants (XDATA « RELEVE ») |
| `donnees/maison.json` | Source de vérité unique (géométrie, cotes, sources, registre des écarts) |
| `donnees/tableau_pieces.csv` | Tableau des pièces (Excel : séparateur « ; », décimales à virgule) |
| `donnees/verifications.txt` | Rapport des contrôles automatiques |
| `outils/` | `generer_plans.py` (tout régénérer en une commande), `README.md`, `pretraitement.py` |

## 2. Photos utilisées

Numérotation dans l'ordre d'envoi. Aucune photo des lieux réels n'a été fournie.

| Photo | Document | Fichier de travail |
|---|---|---|
| P1 | Croquis no 1 — « Plan d'origine et plan actuel du RDC », Claude Mazerolle, ing., 19 septembre 2016 (quadrillage 1–7 / A–D, axes porteurs d'origine, colonnes retirées, fissures, ferme 5/12) | `travail/photos/P2.jpg` |
| P2 | Feuille « FONDATIONS & SOUS-SOL », éch. 1/4" = 1'-0" — gros plan (source principale sous-sol) | `travail/photos/P1.jpg` |
| P3 | Feuille « FONDATIONS & SOUS-SOL », vue entière avec cartouche (source secondaire) | `travail/photos/P7.jpg` |
| P4 | Feuille « REZ-DE-CHAUSSÉE », éch. 1/4" = 1'-0" — gros plan (source principale RDC ; haut un peu coupé) | `travail/photos/P3.jpg` |
| P5 | Feuille RDC, vue entière (source secondaire) | `travail/photos/P4.jpg` |
| P6 | Feuille RDC, vue entière, autre prise redressée en perspective (source secondaire) | `travail/photos/P6.jpg` |
| P7 | Plan d'implantation de la maison projetée sur le lot 1-487, Ville de Baie-Comeau, éch. 1" = 20', 6 nov. 1957, flèche du nord | `travail/photos/P5.jpg` |

Les fichiers du dossier `travail/` (photos, tuiles, vignettes d'arbitrage, extractions) gardent la numérotation interne de la colonne de droite ; tous les livrables utilisent la numérotation de gauche.

## 3. Repère et convention de cotation

- **Origine :** coin extérieur avant-gauche de la fondation, vu de la rue ; x le long de la façade, y vers l'arrière. Unité interne : pouce ; affichage en pieds-pouces, métrique entre parenthèses.
- **Nord :** 9.8° dans le sens horaire depuis l'axe façade → arrière (ESTIMÉ, photo P7 ; mesuré par code sur la flèche du plan d'implantation (prep/redresse/P5.jpg), ± 1,5° ; angle horaire de +y (vers l'arrière) au nord ; nord non qualifié (vrai/magnétique)). La façade avant regarde donc à peu près vers le sud.
- **Convention de cotation de l'original :** Hors-tout et chaînes extérieures au NU EXTÉRIEUR des murs de fondation (SS) et des murs extérieurs (RDC) ; fenêtres et portes extérieures cotées à l'AXE (centre) de l'ouverture, largeurs = baie entre jambages ; cloisons du RDC cotées à l'AXE (DÉDUIT : chaque chaîne intérieure ferme sur le hors-tout depuis les nus ext. ; les axes y = 13'-1" (157) et 17'-0" (204) coïncident avec les axes des poutres 8"x10" du sous-sol et avec les axes B et C du croquis 2016 ; la ligne 2 du croquis tombe sur l'axe de la cloison) ; au sous-sol, chaîne intérieure en x au nu intérieur des murs et aux faces des colonnes (10" + 9'-10" + 8" + 7'-4" …), chaîne en y du nu intérieur aux AXES des poutres. Épaisseurs : fondation 10" LU (P2) ; murs ext. RDC 10" LU (P1 2016, à confronter : dessin 1957 ≈ 11") ; cloisons 4½" PRÉSUMÉ sauf cloison chambre arrière / S. de bain 6" LU ; murs du caveau 10" (droit LU, autres PRÉSUMÉ par analogie) ; murs de l'excroissance du perron 6" (gauche LU, autres PRÉSUMÉ) ; entrée arrière 6" PRÉSUMÉ. Toute la géométrie est générée par code (scripts/construire_maison.py).
- **Sources des dimensions :** LU (écrit sur le plan) · DÉDUIT (calculé à partir d'autres cotes) · ESTIMÉ (mesuré dans l'image, précédé de « ≈ » sur les plans) · PRÉSUMÉ (standard de construction faute d'info) · ILLISIBLE. Un repère orange ⚠n renvoie à l'écart n du registre (section 6).

## 4. Hypothèses retenues

- **État représenté : les plans d'origine (1957) corrigés par le constat du propriétaire du 2026-10-29** (⚠30) : au rez-de-chaussée, les cloisons de la cage d'escalier, du placard à balais et des axes porteurs d'origine B et C (chambre d'utilité / dégagement, salon / passage) n'existent plus ; la porte de la salle de bain ouvre vers le dégagement ; meubles, électroménagers, comptoirs et baignoire ne sont pas représentés (conservés pour mémoire dans `maison.json`). Les autres cloisons de 1957 absentes du croquis d'ingénieur de 2016 (photo 1, qui n'est pas un relevé complet) sont conservées et consignées comme écart à valider en visite.
- **Aucune mesure sur place (ancres vides)** : le relevé n'est calé sur aucune mesure du bâtiment réel.
- **Les cotes écrites priment sur le dessin** : la géométrie est construite à partir des chaînes de cotes ; les proportions du dessin servent seulement à combler les trous (ESTIMÉ).
- **Lecture des cotes** : deux lectures indépendantes de chaque cote, puis une 3e lecture à l'aveugle pour chaque désaccord ; une cote non tranchée garde le statut « conflit » et figure au registre.
- **Murs porteurs** : aucun plan n'écrit « porteur » pour l'état actuel ; tous les murs sont « inconnu », avec les indices notés dans `maison.json` (poutres dessous, axes porteurs d'origine du croquis 2016).
- **Épaisseurs** non cotées : valeurs PRÉSUMÉES (voir écarts) ; hauteurs de plafond : inconnues, laissées vides.

## 5. Superficies

| Niveau | Feuille | Superficie brute (empreinte) | Σ superficies nettes des pièces | Nb de pièces |
|---|---|---|---|---|
| Sous-sol | A-100 | 1272,3 pi² (118,2 m²) | 1 138,1 pi² (105,7 m²) | 3 |
| Rez-de-chaussée | A-101 | 1248,3 pi² (116,0 m²) | 1 087,0 pi² (101,0 m²) | 17 |

Superficie brute = empreinte extérieure des murs du niveau, excroissances comprises (caveau, entrée arrière, etc.). Contrôle : Σ pièces + Σ murs = superficie brute (voir `donnees/verifications.txt`). Détail par pièce : `donnees/tableau_pieces.csv`.

## 6. Registre des écarts

30 écarts : **6 critiques**, 10 moyens, 14 faibles.

| # | Niveau | Impact | Description | Hypothèse retenue |
|---|---|---|---|---|
| ⚠1 | global | faible | Cote en conflit cote-IMP-010 — Longueur de la ligne latérale gauche du lot : 115.17' (2 lectures) ou 115,14' (3e lecture). Lecture 1 « 115.17' », lecture 2 « 115.17' », 3e lecture « 115,14' » (moyenne). Vignettes (fichiers de travail, numérotation interne des photos) : arbitrage/vignettes/d-P5-04_P5.png. | 115.17' (1382.04 po) — lectures 1 et 2 : 115.17' ; 3e lecture 115,14' ; aucune chaîne fermée |
| ⚠2 | RDC | moyen | Cote en conflit cote-RDC-018 — Segment arrière droit 10'-9" / 10'-5" (nu ext. droit de l'entrée arrière → coin arrière droit). Lecture 1 « 10'-9" », lecture 2 « 10-9" », 3e lecture « 10'-5" » (basse). Vignettes (fichiers de travail, numérotation interne des photos) : arbitrage/vignettes/d-RDC-03_P4.png, arbitrage/vignettes/d-RDC-03_P6.png. | 10'-9" (10'-9" po) — 3e lecture 10'-5" en confiance basse ; seule 10'-9" ferme la chaîne arrière 18'-3" + 9'-0" + 10'-9" = 38'-0" (10'-5" donne 37'-8") ; la même chaîne au sous-sol (cote-SS-004) est confirmée 10'-9" |
| ⚠3 | RDC | moyen | Cote en conflit cote-RDC-048 — Largeur de l'arche hall / salon : écrit « ARCHE 4'-0" » (2 lectures) contre 6'-0" (3e lecture) ; dessin ≈ 74 po. Lecture 1 « ARCHE 4'-0" », lecture 2 « ARCHE 4'-0" », 3e lecture « ARCHE 6'-0" » (moyenne). Vignettes (fichiers de travail, numérotation interne des photos) : arbitrage/vignettes/d-RDC-11_P3.png, arbitrage/vignettes/d-RDC-11_P4.png, arbitrage/vignettes/d-RDC-11_P6.png. | ARCHE 4'-0" (4'-0" po) — lectures 1 et 2 : 4'-0" ; 3e lecture (aveugle) : 6'-0" ; ouverture dessinée ≈ 74 po (ESTIMÉ). Valeur écrite majoritaire retenue (les cotes écrites priment sur le dessin) — à mesurer |
| ⚠4 | SS | faible | Cote en conflit cote-SS-017 — Largeur de la fenêtre gauche basse du sous-sol (au-dessus de l'évier à lessive). Lecture 1 « 3'-0" », lecture 2 « 3'-0" », 3e lecture « 3'-0" » (basse). Vignettes (fichiers de travail, numérotation interne des photos) : arbitrage/vignettes/d-SS-07_P1.png, arbitrage/vignettes/d-SS-07_P7.png. | 3'-0" (3'-0" po) — les lectures 1 et 2 lisent 3'-0" ; 3e lecture 3'-0" mais en confiance basse ; aucune chaîne ne contient cette largeur ; dessin ≈ 37 po (ESTIMÉ) compatible |
| ⚠5 | RDC | moyen | Épaisseur des murs extérieurs du RDC : 10" écrit sur le croquis 2016 (P1, chaînes 10" aux 4 côtés — valeur typique d'une fondation, peut-être reprise du plan de fondation) ; le dessin 1957 montre ≈ 11 po ; aucune épaisseur écrite sur la feuille RDC (P4, P5 et P6). | 10" (LU P1) appliqué aux 4 murs ext. du RDC ; les dimensions intérieures des pièces en dépendent (± 1 po). |
| ⚠6 | RDC | moyen | Épaisseur des cloisons du RDC non cotée (sauf cloison chambre arrière / S. de bain 6" LU, tranchée par 3e lecture) ; dessin ≈ 6 po. | 4½" PRÉSUMÉ (cloison 2x4 + plâtre) ; les cloisons sont positionnées à l'AXE (convention déduite) donc seules les dimensions nettes des pièces varient. |
| ⚠7 | global | faible | Épaisseurs PRÉSUMÉES par analogie ou par défaut : murs gauche et du fond du caveau (10"), murs avant et droit de l'excroissance du perron (6"), murs de l'entrée arrière (6", dessin ≈ 11") ; profondeur de l'entrée arrière non cotée : nu ext. PRÉSUMÉ à 5'-0" du mur arrière (= caveau cote-SS-009), alors que le dessin RDC montre ≈ 5'-7". | Valeurs PRÉSUMÉES indiquées par le repère ⚠ sur les plans. |
| ⚠8 | global | moyen | Hauteurs de plafond inconnues aux deux niveaux (aucune coupe ni élévation ; aucune hauteur écrite). | Hauteur laissée vide (ILLISIBLE) ; aucune valeur présumée. |
| ⚠9 | RDC | critique | Croquis 2016 (P1, « plan d'origine et plan actuel ») : seules quelques cloisons sont redessinées en gris (murs ext., cloison ligne 3 à ≈ 14'-5" du coin gauche, de l'axe C au mur arrière ; placards en H entre les lignes 2 et 3 ; bout de cloison ligne 4 à 18'-6", de ≈ 6'-4" au mur avant). Absentes du gris : murs de la S. de bain, cloisons des G.R. de la chambre arrière (≈ 12'-1" à 13'-5"), cloisons de la cage d'escalier (lignes 5 et 6, entre C et D), escalier, cloison médiane des placards avant, cloisons le long des axes B et C. État actuel incertain : cloisons retirées ou simple croquis partiel. — CONFIRMÉ en partie par le constat du propriétaire (épreuve A-101 R0 annotée, 2026-10-29) : cloisons de la cage d'escalier, du placard à balais, chambre d'utilité / dégagement (axe C) et salon / passage (axe B) retirées. | Le relevé reproduit le plan de 1957 (P4), corrigé par le constat du propriétaire ; les autres cloisons absentes du gris 2016 sont conservées et signalées ici. |
| ⚠10 | SS | critique | Croquis 2016 : « Colonne C4 retirée » (axe C à 17'-0" du nu ext. avant × ligne 4 à 18'-6" du coin gauche). Au plan 1957 (P2), la colonne la plus proche est str-SS-C02 à 19'-0" (DÉDUIT de la chaîne 9'-10" + 8" + 7'-4") : décalage de 6 po entre les deux documents. | str-SS-C02 conservée au plan (état 1957) avec mention ; portée de la poutre arrière possiblement doublée (≈ 15'-4" entre C01 et C03 sans C02). |
| ⚠11 | SS | critique | Croquis 2016 : « Colonne C6 retirée » (axe C × ligne 6 à 26'-4" du coin gauche). Au plan 1957 : str-SS-C03 à 27'-0" (8 po de décalage). | str-SS-C03 conservée au plan (état 1957) avec mention ; zone de fissures 2016 au droit (ligne 6 / axe C). |
| ⚠12 | SS | moyen | Le croquis 2016 ne marque des colonnes qu'aux lignes 4 et 6 (B4, B6 pleines ; C4, C6 retirées) ; le plan 1957 en montre 3 par poutre (à 11'-0", 19'-0" et 27'-0" du coin gauche). Les colonnes à 11'-0" (C01, C04) n'apparaissent pas sur P1 ; positions décalées de 6 à 8 po entre documents. | Positions 1957 retenues (DÉDUITES des cotes du sous-sol). |
| ⚠13 | RDC | critique | Axes porteurs d'origine (P1) : B à 13'-1" et C à 17'-0" du nu ext. avant, « porteurs à l'origine ». Concordance vérifiée : ils coïncident exactement avec les axes des poutres 8x10 du sous-sol (str-SS-P02 : 10" + 12'-3" ; str-SS-P01 : 31'-8" − 10" − 13'-10") et avec les cloisons RDC d'origine mur-RDC-012/019 (B) et mur-RDC-026 (C). Le croquis ne dit rien de leur état en 2016 ; le propriétaire a constaté le retrait des cloisons sur B (à droite de 18'-6", sauf le trumeau près du mur droit) et sur C. | Cloisons restantes sur B (mur-RDC-012, trumeau mur-RDC-019) marquées porteur « inconnu » avec indices ; aucune reprise structurale relevée. |
| ⚠14 | RDC | critique | Fissures signalées en 2016 (P1) : « zone de fissures au plafond de plâtre » le long de la ligne 6 (≈ 26'-1" à 26'-7" du coin gauche), de l'axe C au mur arrière, et le long de l'axe C (≈ 16'-3" à 17'-0" du nu ext. avant), de 26'-4" à ≈ 31'-7" ; « fissure ± 1,2 m au plafond de stucco » dans le salon à ≈ 26'-7" du coin gauche, de 2'-7" à 5'-7" du nu ext. avant. | Fissures reportées comme écart (aucune donnée de profondeur ni d'évolution) ; probablement liées au retrait des colonnes C4/C6 (NON écrit). |
| ⚠15 | RDC | moyen | Fissure ± 1,2 m au plafond de stucco du salon (P1) : à ≈ 26'-7" du coin gauche, de 2'-7" à 5'-7" du nu ext. avant (longueur dessinée ≈ 37 po ; texte 1,2 m ≈ 47 po). | Position ESTIMÉE sur le croquis 2016. |
| ⚠16 | RDC | moyen | Usage des pièces : le croquis 2016 nomme « Salle à manger » l'espace que le plan 1957 nomme « CHAMBRE D'UTILITÉ », et « Cuisine » la « CUISINE S.-À-MANGER » d'origine ; l'absence de cloisons grises aux lignes 5 et 6 suggère un espace ouvert (NON écrit). | Noms 2016 adoptés (Salle à manger, Cuisine) : l'aire est ouverte selon le constat du 2026-10-29 ; noms 1957 conservés dans nom_original. |
| ⚠17 | RDC | moyen | ARCHE hall / salon : texte « ARCHE 4'-0" » (lectures 1 et 2) mais ouverture dessinée ≈ 74 po, aussi grande que l'ancienne « ARCHE 6'-0" » salon / cuisine. | Voir ecart-003 (cote en conflit) : 4'-0" retenu. |
| ⚠18 | RDC | faible | Porte de la chambre d'utilité étiquetée « 2'-6"x6'-8" » (3 lectures) dans une baie cotée 2'-5" d'axe en axe (cote-RDC-031) : une porte de 30 po ne peut pas y tenir avec ses montants ; le dessin place la porte en avant de la colonne des G.R., dans le prolongement de la cloison à 17'-0" du nu ext. avant. | Sans objet : la porte et sa cloison n'existent plus (constat du propriétaire (épreuve A-101 R0 annotée, 2026-10-29)). Porte de 30 po placée sur la cloison de l'axe C, entre ≈ 12'-4" et 14'-10" du coin gauche (ESTIMÉ). |
| ⚠19 | RDC | faible | Entrée arrière : 8'-2" + 8'-3" + 8'-0" + 2'-9" = 27'-2" (axe de la fenêtre + 2'-9") alors que 18'-3" + 9'-0" = 27'-3" au nu ext. droit du volume → écart de 1 po (2'-9" confirmé par la 3e lecture). | Nu ext. droit du volume à 27'-3" (chaîne hors-tout) ; la cote 2'-9" est dessinée 2'-10" (repère sur la cote). |
| ⚠20 | SS | faible | Fenêtres arrière et droite haute du sous-sol : « 6'-8" » confirmé par la 3e lecture, mais dessinées de la même longueur que la fenêtre avant cotée 6'-3" (≈ 72–73 po). | 6'-8" (LU, confirmé). |
| ⚠21 | SS | faible | Porte du caveau « PORTE 2'-6" » positionnée par la cote 3'-6" dont le point de départ n'est pas dessiné (nu ext. ou int. du mur gauche du caveau). | Axe à 18'-3" + 3'-6" = 21'-9" du coin gauche (depuis le nu ext.) ; alternative 22'-7" (depuis le nu int.). |
| ⚠22 | global | faible | Escalier SS ↔ RDC : superposition à 5 po près (SS largeur ≈ 37 po ESTIMÉ, RDC 3'-5" à l'axe des anciennes cloisons (cote-RDC-033), cage retirée) ; 14 C.M. écrit aux deux niveaux mais ≈ 10 girons visibles au RDC (les marches inférieures passaient sous le placard BALAIS) ; échappée sous la poutre arrière (17'-0" du nu ext. avant) au pied de l'escalier non vérifiable. | Course ESTIMÉE au dessin ; position alignée sur la cage du RDC. |
| ⚠23 | RDC | faible | Poutre 6"x10" FLUSH (cuisine) non cotée en position : ≈ 17'-2" du nu ext. avant ESTIMÉ (P4), à 2 po de l'axe C (17'-0") et de la poutre arrière du SS. | 17'-2" (206 po) ESTIMÉ. |
| ⚠24 | SS | faible | Colonne str-SS-C01 (11'-0" du coin gauche, sur la poutre arrière à 17'-0" du nu ext. avant) : aucune cloison RDC au-dessus (zone de la porte de la chambre arrière, ≈ 17'-8") ; la cloison à 12'-2" passe à 14 po de la rangée de colonnes à 11'-0". | Aucune incidence sur le relevé ; information pour la structure. |
| ⚠25 | global | faible | Superposition de la plomberie : chauffe-eau du sous-sol à 2'-2" du coin gauche et 9'-0" du nu ext. avant : à 4'-4" de la S. de bain et 24'-6" de la cuisine (en plan) ; évier à lessive du sous-sol à 1'-10" du coin gauche et 4'-3" du nu ext. avant : à 9'-0" de la S. de bain et 26'-0" de la cuisine (en plan). Aucun drain, colonne de chute ni panneau électrique dessiné au sous-sol. | Aucune conduite reportée (non dessinée). |
| ⚠26 | global | faible | Cheminée : massif extérieur au mur gauche non coté (seule sa face avant, à 11'-0" du nu ext. avant, est située par la chaîne gauche du sous-sol) ; saillie et profondeur ≈ 20 × 21 po ESTIMÉES. | Dimensions ESTIMÉES au dessin. |
| ⚠27 | global | faible | Plan d'implantation P7 (1957, « maison projetée ») : rectangle 38'-0" × 31'-8" concordant ; excroissance avant dessinée ≈ 12,6–19,0 pi du coin gauche (perron SS : 13'-6"–19'-6") ; volume arrière ≈ 17,0–26,4 pi (entrée arrière : 18'-3"–27'-3") et marches ≈ 26,4–34,5 pi ; profondeur mesurée ≈ 32,1 pi (1 %). Implantation projetée, pas un relevé ; marges 40' (avant), 7.79' et 9' (latérales). | Plans de 1957 (P2, P3, P4, P5, P6) retenus pour la géométrie ; P7 sert à l'orientation (nord ≈ 9,8° ± 1,5°) et au lot. |
| ⚠28 | global | moyen | Aucune mesure prise sur place n'a été fournie par le propriétaire (ancres vides) : toute la géométrie provient des plans de 1957 et du croquis 2016. | Plans d'origine reproduits sans calage sur le bâtiment réel. |
| ⚠29 | SS | faible | Sens d'ouverture non dessiné pour les deux portes du sous-sol (rectangle barré d'un X dans le mur, aucun arc) : ouv-SS-005 « PORTE 2'-8" » (mur droit, axe à 6'-3" du nu ext. avant) et ouv-SS-008 « PORTE 2'-6" » (porte du caveau, mur arrière). Les tiretés près de la porte 2'-8" sont des circuits électriques. | Portes dessinées comme baies (opération « aucune ») ; aucun sens inventé. |
| ⚠30 | RDC | critique | constat du propriétaire (épreuve A-101 R0 annotée, 2026-10-29) : les cloisons mur-RDC-026, -027, -028, -029 et la partie de mur-RDC-019 à gauche de l'arche 6'-0" n'existent plus ; 4 portes (ouv-RDC-017, -023, -024, -025) et l'arche ouv-RDC-013 disparaissent avec elles. Deux de ces cloisons étaient sur les axes porteurs d'origine B et C (P1) ; les colonnes str-SS-C01, C02, C05, C06 du sous-sol ne sont plus sous aucune cloison. Le trait diagonal au coin hall / salon est interprété comme le début du trait de l'axe B : la cloison hall / salon (arche 4'-0") est conservée. La porte de la salle de bain ouv-RDC-015 ouvre aujourd'hui vers le dégagement (au plan 1957 : dans la salle de bain). | Cloisons retirées du plan (conservées dans murs_retires pour mémoire) ; aire ouverte découpée en zones (dégagement, salle à manger, escalier, cuisine, salon) aux axes des anciennes cloisons, sans mur. Escalier conservé (seul accès au sous-sol) ; garde-corps et reprises structurales (poutres, linteaux, retombées) non relevés. Trumeau à droite de l'ancienne arche conservé (position ESTIMÉE). |

### Cotes en conflit ou illisibles

| Cote | Niveau | Texte | Lecture 1 | Lecture 2 | Statut |
|---|---|---|---|---|---|
| cote-SS-017 | SS | 3'-0" | 3'-0" | 3'-0" | conflit |
| cote-RDC-018 | RDC | 10'-9" | 10'-9" | 10-9" | conflit |
| cote-RDC-048 | RDC | ARCHE 4'-0" | ARCHE 4'-0" | ARCHE 4'-0" | conflit |
| cote-RDC-220 | RDC | 9'-0" ? | 9'-0" ? |  | illisible |
| cote-RDC-222 | RDC | (nombreuses cotes manuscrites pâles : linteaux, ouvertures, placards, « 2'-4" »…) | (nombreuses cotes manuscrites pâles : linteaux, ouvertures, placards, « 2'-4" »…) |  | illisible |
| cote-RDC-224 | RDC | ?'-5" |  | ?'-5" | illisible |
| cote-RDC-225 | RDC | ?'-5" |  | ?'-5" | illisible |
| cote-RDC-226 | RDC | 3'-?0" |  | 3'-?0" | illisible |

## 7. Mesures à prendre sur place (par priorité)

Aucune zone de rénovation n'a été désignée : le tri suit l'impact des écarts (critiques d'abord). Chaque ligne dit où mesurer et pourquoi.

### Impact critique

1. **Constater les cloisons qui restent incertaines (absentes du gris 2016 et non barrées par le propriétaire) : G.R. de la chambre arrière (entre 12'-2" et 14'-7" du coin gauche), murs de la S. de bain, lingerie (LIN.) et cloison hall / salon (18'-6", arche 4'-0") ; position réelle de la cloison ligne 3 (≈ 14'-5" sur P1 contre 14'-7" en 1957).** — Pourquoi : Croquis 2016 (P1, « plan d'origine et plan actuel ») (⚠9, RDC)
2. **Au sous-sol, sous la poutre arrière (17'-0" du nu ext. avant) : vérifier la présence / l'absence de colonne à x ≈ 18'-6"–19'-0", la flèche de la poutre et tout appui ajouté.** — Pourquoi : Croquis 2016 : « Colonne C4 retirée » (axe C à 17'-0" du nu ext. avant × ligne 4 à 18'-6" du coin gauche). (⚠10, SS)
3. **Au sous-sol, sous la poutre arrière : vérifier la colonne à x ≈ 26'-4"–27'-0" ; mesurer la flèche de la poutre entre C02 et le mur droit.** — Pourquoi : Croquis 2016 : « Colonne C6 retirée » (axe C × ligne 6 à 26'-4" du coin gauche). (⚠11, SS)
4. **Au sous-sol : appui des solives 2x10 sur les deux poutres 8x10 (13'-1" et 17'-0" du nu ext. avant). Au RDC : poutre ou retombée ajoutée au plafond lors du retrait des cloisons sur les axes B et C (section, appuis, hauteur libre).** — Pourquoi : Axes porteurs d'origine (P1) : B à 13'-1" et C à 17'-0" du nu ext. (⚠13, RDC)
5. **Relever les fissures (longueur, ouverture, évolution) au plafond de la cuisine le long de l'ancienne cloison de l'escalier et de la poutre FLUSH, et au plafond du salon à ≈ 26'-7" du coin gauche.** — Pourquoi : Fissures signalées en 2016 (P1) : « zone de fissures au plafond de plâtre » le long de la ligne 6 (≈ 26'-1" à 26'-7" du coin gauche), de l'axe C au mur arrière, et le long de l'axe C (≈ 16'-3" à 17'-0" du nu ext. avant), de 26'-4" à ≈ 31'-7" (⚠14, RDC)
6. **Au RDC : présence d'une retombée ou poutre au plafond le long des axes B (13'-1" du nu ext. avant) et C (17'-0") là où les cloisons ont été enlevées, et sa hauteur libre ; garde-corps de l'escalier ; existence du trumeau près du mur droit sur l'axe B ; cloison hall / salon (arche 4'-0") toujours en place ?** — Pourquoi : constat du propriétaire (épreuve A-101 R0 annotée, 2026-10-29) (⚠30, RDC)

### Impact moyen

7. **Mesurer à l'extérieur, le long du mur arrière, du coin arrière droit au nu extérieur du mur droit de l'entrée arrière (attendu 10'-9" = 129 po).** — Pourquoi : Cote en conflit cote-RDC-018 — Segment arrière droit 10'-9" / 10'-5" (nu ext. droit de l'entrée arrière → coin arrière droit). (⚠2, RDC)
8. **Mesurer la largeur libre de l'arche hall / salon (cloison à 18'-6" du coin avant gauche).** — Pourquoi : Cote en conflit cote-RDC-048 — Largeur de l'arche hall / salon (⚠3, ⚠17, RDC)
9. **Mesurer l'épaisseur totale du mur extérieur au jambage de la porte d'entrée avant et d'une fenêtre (revêtement int. au revêtement ext.).** — Pourquoi : Épaisseur des murs extérieurs du RDC : 10" écrit sur le croquis 2016 (P1, chaînes 10" aux 4 côtés — valeur typique d'une fondation, peut-être reprise du plan de fondation) (⚠5, RDC)
10. **Mesurer l'épaisseur d'une cloison à un cadre de porte (ex. porte de la chambre avant) et la largeur nette du hall (attendu 3'-11" − 4½" ≈ 42½").** — Pourquoi : Épaisseur des cloisons du RDC non cotée (sauf cloison chambre arrière / S. de bain 6" LU, tranchée par 3e lecture) (⚠6, RDC)
11. **Mesurer la hauteur plancher-plafond au sous-sol (sous solives et sous les poutres 8x10) et au RDC (salon, cuisine sous la poutre FLUSH).** — Pourquoi : Hauteurs de plafond inconnues aux deux niveaux (aucune coupe ni élévation ; aucune hauteur écrite). (⚠8, global)
12. **Relever au sous-sol la position et la section de chaque colonne sous les deux poutres 8x10.** — Pourquoi : Le croquis 2016 ne marque des colonnes qu'aux lignes 4 et 6 (B4, B6 pleines ; C4, C6 retirées) (⚠12, SS)
13. **Mesurer la fissure au plafond du salon, près de 26'-7" du coin avant gauche.** — Pourquoi : Fissure ± 1,2 m au plafond de stucco du salon (P1) (⚠15, RDC)
14. **Constater l'usage et l'aménagement actuels de la salle à manger (ancienne chambre d'utilité) et de la cuisine.** — Pourquoi : Usage des pièces : le croquis 2016 nomme « Salle à manger » l'espace que le plan 1957 nomme « CHAMBRE D'UTILITÉ », et « Cuisine » la « CUISINE S.-À-MANGER » d'origine (⚠16, RDC)
15. **Mesurer au minimum les deux hors-tout extérieurs (38'-0" et 31'-8") et une diagonale au sous-sol pour caler le relevé.** — Pourquoi : Aucune mesure prise sur place n'a été fournie par le propriétaire (ancres vides) (⚠28, global)

### Impact faible

16. **Consulter le certificat de localisation / plan cadastral (aucune mesure de maison en jeu).** — Pourquoi : Cote en conflit cote-IMP-010 — Longueur de la ligne latérale gauche du lot (⚠1, global)
17. **Mesurer la largeur brute de la fenêtre du mur gauche du sous-sol, côté avant (au-dessus de l'évier à lessive).** — Pourquoi : Cote en conflit cote-SS-017 — Largeur de la fenêtre gauche basse du sous-sol (au-dessus de l'évier à lessive). (⚠4, SS)
18. **Mesurer l'épaisseur des murs du caveau à la porte 2'-6", la profondeur hors-tout et l'épaisseur des murs de l'entrée arrière à la porte extérieure.** — Pourquoi : Épaisseurs PRÉSUMÉES par analogie ou par défaut (⚠7, global)
19. **Mesurer de l'axe de la fenêtre de l'entrée arrière au nu ext. de son mur droit.** — Pourquoi : Entrée arrière : 8'-2" + 8'-3" + 8'-0" + 2'-9" = 27'-2" (axe de la fenêtre + 2'-9") alors que 18'-3" + 9'-0" = 27'-3" au nu ext. (⚠19, RDC)
20. **Mesurer la largeur des fenêtres du mur arrière (13'-0" du coin gauche) et du mur droit (6'-0" du coin arrière).** — Pourquoi : Fenêtres arrière et droite haute du sous-sol (⚠20, SS)
21. **Mesurer la position de la porte du caveau depuis le coin intérieur arrière gauche du sous-sol.** — Pourquoi : Porte du caveau « PORTE 2'-6" » positionnée par la cote 3'-6" dont le point de départ n'est pas dessiné (nu ext. ou int. du mur gauche du caveau). (⚠21, SS)
22. **Mesurer la hauteur et le giron des marches, la largeur de l'escalier et l'échappée sous la poutre arrière.** — Pourquoi : Escalier SS ↔ RDC : superposition à 5 po près (SS largeur ≈ 37 po ESTIMÉ, RDC 3'-5" à l'axe des anciennes cloisons (cote-RDC-033), cage retirée) (⚠22, global)
23. **Repérer la poutre au plafond de la cuisine (bande de plâtre, fissures) et mesurer sa distance au mur arrière.** — Pourquoi : Poutre 6"x10" FLUSH (cuisine) non cotée en position (⚠23, RDC)
24. **Vérifier l'appui de la cloison à 12'-2" du coin gauche sur la solive doublée (note « solives doubles sous les cloisons »).** — Pourquoi : Colonne str-SS-C01 (11'-0" du coin gauche, sur la poutre arrière à 17'-0" du nu ext. avant) (⚠24, SS)
25. **Repérer au sous-sol la colonne de chute sous la S. de bain (0 à 9'-0" du coin gauche, 13'-1" à 18'-7" du nu ext. avant) et sous l'ancien évier de cuisine.** — Pourquoi : Superposition de la plomberie : chauffe-eau du sous-sol à 2'-2" du coin gauche et 9'-0" du nu ext. (⚠25, global)
26. **Mesurer la saillie et la largeur du massif de cheminée à l'extérieur, côté gauche.** — Pourquoi : Cheminée : massif extérieur au mur gauche non coté (seule sa face avant, à 11'-0" du nu ext. avant, est située par la chaîne gauche du sous-sol) (⚠26, global)
27. **Certificat de localisation récent pour l'implantation réelle et l'orientation.** — Pourquoi : Plan d'implantation P7 (1957, « maison projetée ») (⚠27, global)
28. **Constater pour chaque porte le type de battant, le côté des pentures et le côté d'ouverture.** — Pourquoi : Sens d'ouverture non dessiné pour les deux portes du sous-sol (rectangle barré d'un X dans le mur, aucun arc) (⚠29, SS)

## 8. Modifier et régénérer

Toute correction se fait dans `donnees/maison.json`, puis : `cd outils && python3 generer_plans.py` (régénère SVG, PDF, PNG, DXF, CSV, vérifications et ce rapport). Voir `outils/README.md`. Le calque `90-RENO-Propose` des SVG est vide et prêt pour les propositions de rénovation.
