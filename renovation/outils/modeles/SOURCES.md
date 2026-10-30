# Sources de modèles 3D libres : bilan (29 oct. 2026)

Projet : visite 3D du sous-sol (three.js r149). Style « moderne chaleureux ». Tous les codes HTTP ci-dessous ont été testés depuis ce conteneur avec curl et un User-Agent de navigateur.

## Classement pour notre usage

| # | Source | Licence (vérifiée sur la page de la source) | Accès depuis le conteneur | Formats | Qualité | Points forts |
|---|---|---|---|---|---|---|
| 1 | **Amazon Berkeley Objects (ABO)** amazon-berkeley-objects.s3.amazonaws.com | **CC BY 4.0** (pas NC). Crédit : « Amazon.com » | 200. GLB direct sur S3, sans jeton : `3dmodels/original/<x>/<id>.glb`. Métadonnées : `3dmodels/metadata/3dmodels.csv.gz` et `archives/abo-listings.tar` (83 Mo) | GLB | Produits réels modélisés par des artistes, PBR, **échelle réelle en mètres**. Fichiers bruts lourds (17 à 87 Mo) : il faut ajouter `--simplify-ratio` | 7 953 modèles : 1 184 chaises, 859 canapés, 817 tapis, 584 tables, 345 lampes, 340 tabourets de bar, 288 poufs, 195 luminaires, 182 jardinières, 109 miroirs, 50 vases. Fitness : haltères hexagonaux et en néoprène, support d'haltères, tapis de yoga, banc plat. **Pas de tapis roulant ni de vélo** |
| 2 | **BlenderKit / Blendkit**, offre gratuite (blenderkit.com) | Deux licences : **CC0** (2 563 modèles gratuits en CC0) et **Royalty Free** (usage commercial permis, sans crédit, mais interdit de revendre ou de redistribuer le modèle comme asset) | 200. Recherche : `api/v1/search/?query=…+asset_type:model+is_free:true+license:cc_zero`. **Téléchargement GLB sans jeton** : `api/v1/downloads/<uuid>/?scene_uuid=<uuid4>` renvoie une URL signée | GLB (`gltf`), blend | Élevée : PBR, faite par des artistes, échelle correcte | Mobilier moderne (canapés, fauteuils, tabourets de bar, luminaires suspendus, lampes, tapis, plantes, téléviseurs) et un peu de fitness (haltères, disques, « exercise equipment »). La recherche est floue : « treadmill » renvoie un convoyeur à rouleaux, il faut toujours regarder l'aperçu |
| 3 | **Poly Haven** (polyhaven.com) | **CC0** | 200. API `api.polyhaven.com/assets?t=models`, fichiers sur dl.polyhaven.org (200). Script d'aide : `ph_modele.py` | glTF, FBX, blend, USD | Photoréaliste, PBR 1k à 8k, échelle correcte | 521 modèles : 85 meubles, 34 assises, 29 luminaires, plantes en pot, vases en laiton et céramique, cadres, coussins (`throw_pillows_01`), canapés (`sofa_02` et `sofa_03`), tables d'appoint et basses modernes, `mid_century_lounge_chair`, `bar_chair_round_01`. **Aucun article de fitness** |
| 4 | **Sketchfab par le miroir Objaverse** (huggingface.co/datasets/allenai/objaverse) | Dataset : ODC-By. **Chaque objet garde sa licence Sketchfab** : on ne prend que CC BY ou CC0, après vérification en direct sur `api.sketchfab.com/v3/models/<uid>` | 200, non verrouillé. GLB sur `resolve/main/glbs/…`. Index : `object-paths.json.gz` (800 000 objets) | GLB (converti par Sketchfab, instantané 2022) | Variable, souvent bonne. **Échelle souvent fausse** (mm, ou ×1,8) à corriger | Le meilleur pour le **fitness** : tapis roulants (14 des 24 meilleurs résultats CC BY sont dans le miroir), haltères, kettlebells, vélos de route (B'Twin Triban, etc.), plantes en pot, canapés |
| 5 | Sketchfab direct (sketchfab.com) | CC BY / CC0 / CC BY-SA à garder. NC, ND et « Standard » à rejeter. Le filtre de l'API est `licenses=by` ou `licenses=cc0` | Recherche API : 200 sans jeton. **Téléchargement : 401** (il faut un jeton d'API d'un compte gratuit). Site : 202 (contrôle anti-robot) | glTF, GLB, source | Variable | Le plus grand catalogue CC BY. Si le client fournit un jeton, ce serait la source n° 1 pour le fitness |
| 6 | Khronos glTF-Sample-Assets | Licence propre à chaque modèle. CC0 : SheenChair (Wayfair), GlassVaseFlowers, DiffuseTransmissionTeacup. CC BY 4.0 : GlamVelvetSofa, ChairDamaskPurplegold, AnisotropyBarnLamp, IridescenceLamp, StainedGlassLamp (Wayfair) ; SheenWoodLeatherSofa et CommercialRefrigerator (DGG) | raw.githubusercontent.com : 200. github.com et codeload : **403 (dépôt non autorisé pour cette session)** | GLB, glTF | Qualité vitrine, mais peu de modèles | Quelques pièces de décor haut de gamme. Limites de r149 : pas d'anisotropie ni de *diffuse transmission*. Sheen et transmission sont pris en charge. Le canapé en cuir est de style classique, il ne colle pas à la direction design |
| 7 | Google Scanned Objects (Gazebo Fuel, `fuel.gazebosim.org/1.0/GoogleResearch/models`) | **CC BY 4.0** (Google Research) | API 200 (1 033 modèles). Zip 200 | OBJ, MTL et PNG (conversion avec obj2gltf) | Photoscan propre | Uniquement de petits objets de décor : paniers, tasses, pots, chaussures, jouets. Pas de mobilier |
| 8 | ambientCG (ambientcg.com) | **CC0** | 200. API v3 `api/v3/assets?type=3d-model` (34 modèles) | OBJ, USDC, PBR JPG | Photoscan | Seulement de la nourriture (pommes, citrons, pain) : utile comme décor du bar |
| 9 | Smithsonian 3D (3d-api.si.edu) | CC0 **seulement** pour les objets en Open Access, à vérifier objet par objet | API de fichiers : 200, GLB Draco téléchargeable. 3d.si.edu : 403 (Cloudflare). api.si.edu : 429 avec DEMO_KEY, donc pas de vérification automatique des droits | GLB (Draco) | Numérisations de musée | Vases anciens, plantes : marginal |
| 10 | Kenney (kenney.nl) | CC0 | 200. Le zip se télécharge par un bouton JavaScript | GLB, FBX, OBJ | Low-poly en aplats de couleur | Furniture Kit (140 modèles) : **rejeté**, trop dessin animé |
| 11 | Quaternius (quaternius.com) | Anciens packs en CC0. **Nouvelle licence QAL v1.0 (28 août 2026)** pour les sorties récentes : usage libre, mais redistribution de l'asset interdite | 200. Fichiers sur Google Drive | FBX, OBJ, blend | Low-poly stylisé | Ultimate House Interior (123 modèles, CC0) : **rejeté**, style non réaliste |
| 12 | Poly Pizza | CC0 ou CC BY selon le modèle | Site : 403 (Cloudflare). API : 401 (clé requise) | GLB | Low-poly | Ignoré |
| 13 | OpenGameArt | Mélange CC0, CC BY, GPL | 200 | variés | Qualité jeu vidéo | Marginal |

## Sources rejetées ou inaccessibles

- **BIMobject** : 403 (Cloudflare) et connexion requise. Les conditions varient selon le fabricant ; c'est de la CAO lourde sans textures PBR.
- **3D Warehouse** : site 200, mais l'API répond 400 sans authentification. Il faut une connexion Trimble, et la *General Model License* est restrictive.
- **Connexion obligatoire ou blocage anti-robot** : CGTrader (202, anti-robot), TurboSquid (403), Free3D (403), Fab/Megascans (403), 3dsky (connexion), Pixabay 3D (403).
- **Pas de textures** : Printables et Thingiverse (403, fichiers STL).
- **Conditions de GrabCAD** : usage « non-commercial, internal » seulement.
- **Licences NC ou recherche** : ShapeNet, 3D-FUTURE, HSSD, PartNet, et les dérivés OmniObject3D sur Hugging Face (CC BY-NC).
- **Hors sujet** : NASA 3D (espace ; github.com/nasa en 403).
- **Connexion requise ou licence propriétaire** : Chocofur, BlendSwap.
- **Textures seulement** : cgbookcase, cc0textures.

## Recommandation par besoin

- **Mobilier « moderne chaleureux »** (canapé en tissu gris, fauteuil en cuir cognac, tabourets de bar, tapis, luminaires, plantes) :
  1. ABO (réel, à l'échelle, CC BY)
  2. BlenderKit CC0
  3. Poly Haven CC0
  4. BlenderKit Royalty Free, en dernier recours
- **Petits poids au sol** (haltères, kettlebells, tapis de yoga) : ABO (haltères hexagonaux, haltères néoprène, tapis de yoga), puis Objaverse/Sketchfab CC BY (kettlebells).
- **Tapis roulant** : Objaverse/Sketchfab CC BY. Deux candidats sont testés et de bonne qualité :
  - `faed3a2a…` « Treadmill Machine », par sousinho. Il est à réduire à environ 0,55× (il mesure 3,48 m).
  - `327b6f6c…` « Tunturi T85 », par dima051983. Il est en mm, donc à mettre à ×0,001.
- **Vélo de route sur base d'entraînement** : Objaverse/Sketchfab CC BY. Il y a plusieurs vélos de route, dont un B'Twin Triban 100 (environ 283 000 faces, à simplifier). La base d'entraînement est probablement à modéliser ou à combiner avec un autre modèle.
- **Décor du bar** : Poly Haven (laiton, vases, bouteilles), ambientCG (citrons, pommes), Khronos GlassVaseFlowers (CC0).

## Outils écrits

- `_outils/bk_glb.py search "<q>" [cc_zero|royalty_free]` puis `get <assetBaseId> <dossier>` : produit un GLB et un json (licence, auteur, page).
- `_outils/objv_glb.py search "<q>" [by|cc0]` puis `get <uid> <dossier>` : produit un GLB tiré du miroir Hugging Face et un json qui contient la **licence revérifiée en direct** et la chaîne d'attribution CC BY. Le script refuse toute autre licence.
- Les aperçus testés sont dans `_sondes/apercu_echantillons.png`, `_sondes/apercu_abo.png` et `_sondes/apercu_bk_khr.png`.
- Pour ABO, en production, ajouter `--simplify-ratio 0.1 --simplify-error 0.001` à `optimize`. Avec ce réglage, le canapé passe de 87 Mo à 692 Ko, le tabouret de 52 Mo à 66 Ko et l'haltère de 18 Mo à 51 Ko.

## Chaînes d'attribution type

- **ABO** : « 3D model: Amazon Berkeley Objects, © Amazon.com, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), modified (optimised) ».
- **Sketchfab** : « "<titre>" by <auteur> (https://sketchfab.com/<user>), CC BY 4.0, https://sketchfab.com/3d-models/<uid> — modified ». Le script objv_glb.py la produit automatiquement.
- **GSO** : « Google Scanned Objects, Google Research, CC BY 4.0 ».
- **Khronos et Wayfair** : « © 2021 Wayfair, LLC, CC BY 4.0 ».

## Modèles retenus (dans ce dossier)

| Clé | Usage | Licence | Attribution |
|---|---|---|---|
| `velo_route_base` | vélo de route monté sur une base d'entraînement à transmission directe (composé : vélo Sketchfab + base modélisée) | CC BY 4.0 | "Road Bike" by Tanya Andreeva (https://sketchfab.com/tanity), CC BY 4.0, https://sketchfab.com/3d-models/cb03b0657fbc4693b59194124ba713db — modified (optimised, rescaled, rear wheel removed) — https://sketchfab.com/3d-models/cb03b0657fbc4693b59194124ba713db |
| `tapis_roulant` | tapis roulant de maison | CC BY 4.0 | "Treadmill Machine" by Sousinho (https://sketchfab.com/sousinho), CC BY 4.0, https://sketchfab.com/3d-models/faed3a2a275b4fd68089e1d8bdfb7f89 — modified (optimised, rescaled) — https://sketchfab.com/3d-models/faed3a2a275b4fd68089e1d8bdfb7f89 |
| `haltere_a` | haltère hexagonal | CC BY 4.0 | 3D model: Amazon Berkeley Objects (ABO), © Amazon.com, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), modified (optimised) — https://amazon-berkeley-objects.s3.amazonaws.com/index.html |
| `haltere_b` | haltère hexagonal | CC BY 4.0 | 3D model: Amazon Berkeley Objects (ABO), © Amazon.com, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), modified (optimised) — https://amazon-berkeley-objects.s3.amazonaws.com/index.html |
| `haltere_c` | haltère hexagonal | CC BY 4.0 | 3D model: Amazon Berkeley Objects (ABO), © Amazon.com, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), modified (optimised) — https://amazon-berkeley-objects.s3.amazonaws.com/index.html |
| `kettlebell` | kettlebell noir à bande laiton (recoloré) | CC BY 4.0 | "kettlebell" by anesbe89 (https://sketchfab.com/anesbe89), CC BY 4.0, https://sketchfab.com/3d-models/2e09cbcbde964a658d51838e2f9866bb — modified (optimised, rescaled, recoloured) — https://sketchfab.com/3d-models/2e09cbcbde964a658d51838e2f9866bb |
| `tapis_exercice` | tapis d'exercice gris | CC BY 4.0 | 3D model: Amazon Berkeley Objects (ABO), © Amazon.com, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), modified (optimised) — https://amazon-berkeley-objects.s3.amazonaws.com/index.html |
| `canape` | sofa 81 po, tissu gris chiné, pieds noirs | CC BY 4.0 | 3D model: Amazon Berkeley Objects (ABO), © Amazon.com, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), modified (optimised) — https://amazon-berkeley-objects.s3.amazonaws.com/index.html (produit B07124WQLW) |
| `fauteuil_cuir` | fauteuil en cuir cognac, accoudoirs en acier noir | CC BY 4.0 | 3D model: Amazon Berkeley Objects (ABO), © Amazon.com, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), modified (optimised) — https://amazon-berkeley-objects.s3.amazonaws.com/index.html (produit B071J7Q9WN) |
| `table_basse` | table basse chêne, pieds en épingle | CC BY 4.0 | 3D model: Amazon Berkeley Objects (ABO), © Amazon.com, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), modified (optimised) — https://amazon-berkeley-objects.s3.amazonaws.com/index.html (produit B072ZMVR53) |
| `table_appoint` | table d'appoint ronde noire | CC BY 4.0 | 3D model: Amazon Berkeley Objects (ABO), © Amazon.com, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), modified (optimised) — https://amazon-berkeley-objects.s3.amazonaws.com/index.html (produit B07B7J5XSQ) |
| `lampe_pied` | liseuse noir et laiton | CC BY 4.0 | 3D model: Amazon Berkeley Objects (ABO), © Amazon.com, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), modified (optimised) — https://amazon-berkeley-objects.s3.amazonaws.com/index.html (produit B07374K536) |
| `tele` | télé OLED 65 po | CC BY 4.0 | "LG C9 OLED TV | Game Ready Model" by 4DS Artwork (https://sketchfab.com/4DS_Arts), CC BY 4.0, https://sketchfab.com/3d-models/a0f8cb83918e41649bc106a728397e2c — modified (optimised) — https://sketchfab.com/3d-models/a0f8cb83918e41649bc106a728397e2c |
| `plante_sansevieria` | sansevière en pot noir | CC BY 4.0 | "Sansevieria" by Lassi Kaukonen (https://sketchfab.com/thesidekick), CC BY 4.0, https://sketchfab.com/3d-models/2118ba211bac47d1a56c2ef5b4a645f3 — modified (optimised) — https://sketchfab.com/3d-models/2118ba211bac47d1a56c2ef5b4a645f3 |
| `vase` | vase en céramique blanche | CC0 1.0 | Aucune attribution requise (CC0). — https://polyhaven.com/a/ceramic_vase_01 |
| `cadre_monstera_1` | cadre (feuille de monstera) | CC BY 4.0 | 3D model: Amazon Berkeley Objects (ABO), © Amazon.com, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), modified (optimised) — https://amazon-berkeley-objects.s3.amazonaws.com/index.html (produit B075YLKDPG) |
| `cadre_monstera_2` | cadre (feuille de monstera) | CC BY 4.0 | 3D model: Amazon Berkeley Objects (ABO), © Amazon.com, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), modified (optimised) — https://amazon-berkeley-objects.s3.amazonaws.com/index.html |
| `lit_queen` | lit queen en acacia pâle, duvet blanc (composé) | CC BY 4.0 | 3D models: Amazon Berkeley Objects, © Amazon.com, CC BY 4.0, modified ; "Bed" by Eduard (https://sketchfab.com/buresin.eduard), CC BY 4.0, https://sketchfab.com/3d-models/94478363372f4ab592b338778b01549d — modified (duvet réutilisé) — https://www.amazon.com/dp/B07HSF3Y12 ; https://sketchfab.com/3d-models/94478363372f4ab592b338778b01549d |
| `table_chevet` | table de chevet bois pâle, tiroirs blancs | CC BY 4.0 | 3D model: Amazon Berkeley Objects (ABO), © Amazon.com, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), modified (optimised) — https://www.amazon.com/dp/B07QD6TXWS |
| `lampe_chevet` | lampe de chevet bois blond | CC BY 4.0 | 3D model: Amazon Berkeley Objects (ABO), © Amazon.com, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), modified (optimised) — https://www.amazon.com/dp/B0825DHHVM |
| `bain_autoportant` | bain autoportant ovale | CC BY 4.0 | "Angelo Freestanding Bath" by tissinouk (https://sketchfab.com/tissinouk), CC BY 4.0, https://sketchfab.com/3d-models/dcd691724f6b4d29a6d16def24d14e6e — modified — https://sketchfab.com/3d-models/dcd691724f6b4d29a6d16def24d14e6e |
| `toilette_suspendue` | toilette suspendue | CC BY 4.0 | "Wall Mounted Toilet" by greekisback (https://sketchfab.com/greekisback), CC BY 4.0, https://sketchfab.com/3d-models/e0772bfeea264736a657f3cb8ce94de2 — modified — https://sketchfab.com/3d-models/e0772bfeea264736a657f3cb8ce94de2 |
| `plaque_chasse` | plaque de chasse noire | CC BY 4.0 | "Wall Mounted Toilet" by greekisback (https://sketchfab.com/greekisback), CC BY 4.0, https://sketchfab.com/3d-models/e0772bfeea264736a657f3cb8ce94de2 — modified — https://sketchfab.com/3d-models/e0772bfeea264736a657f3cb8ce94de2 |
| `vasque_carree` | vasque à poser carrée | CC BY 4.0 | "Washbasin" by businessyuen (https://sketchfab.com/businessyuen), CC BY 4.0, https://sketchfab.com/3d-models/9ae7b722a6834c729896e441fa88a1fa — modified — https://sketchfab.com/3d-models/9ae7b722a6834c729896e441fa88a1fa |
| `robinet_vasque_noir` | mitigeur haut noir mat | CC BY 4.0 | "Faucet Volle (water mixer)" by Nick Kotik (https://sketchfab.com/Nathanson), CC BY 4.0, https://sketchfab.com/3d-models/61ee6efa02b64aceaa70f1bc233d9ee2 — modified — https://sketchfab.com/3d-models/61ee6efa02b64aceaa70f1bc233d9ee2 |
| `colonne_douche_noire` | colonne de douche noire, pomme pluie | CC BY 4.0 | "12 Le Vivi Milan Shower System" by audriusm (https://sketchfab.com/13213213213), CC BY 4.0, https://sketchfab.com/3d-models/776a3b4bb4f04594b8fae2f5af691cb1 — modified — https://sketchfab.com/3d-models/776a3b4bb4f04594b8fae2f5af691cb1 |
| `serviettes_pliees` | serviettes blanches pliées | CC BY 4.0 | "White Towel" by Anežka Hájková (https://sketchfab.com/anezka), CC BY 4.0, https://sketchfab.com/3d-models/35b76b90614d49a3aa92eeeb6afec60f — modified — https://sketchfab.com/3d-models/35b76b90614d49a3aa92eeeb6afec60f |
| `distributeurs_marbre` | distributeurs de savon en marbre | CC BY 4.0 | "2 Soap Bottles" by ebomb2 (https://sketchfab.com/ebomb2), CC BY 4.0, https://sketchfab.com/3d-models/181397bb7c42478c85267cd4c92ef540 — modified — https://sketchfab.com/3d-models/181397bb7c42478c85267cd4c92ef540 |
| `laveuse_secheuse` | laveuse et sécheuse frontales côte à côte | CC BY 4.0 | "Washer Dryer SBS" by maimo (https://sketchfab.com/maimo), CC BY 4.0, https://sketchfab.com/3d-models/79e4cdde40034be5be40eb4d9c9c92a2 — modified — https://sketchfab.com/3d-models/79e4cdde40034be5be40eb4d9c9c92a2 |
| `frigo_30` | frigo inox 30 po à portes françaises | CC BY 4.0 | "French Door Refrigerator - Stainless" by Smokahontas (https://sketchfab.com/Smokahontas), CC BY 4.0, https://sketchfab.com/3d-models/ebe62ed6dd9b446a9c9b7d7d6a8086e7 — modified — https://sketchfab.com/3d-models/ebe62ed6dd9b446a9c9b7d7d6a8086e7 |
| `chauffe_eau` | chauffe-eau électrique 60 gal | création du projet | Modèle procédural créé pour le projet (aucune restriction) — /tmp/claude-0/-home-user-lavoie-co/a2f554a7-a4f7-5946-bdd4-2eb9d5a22192/scratchpad/outils3d/construire_chauffe_eau_sdb.js |
