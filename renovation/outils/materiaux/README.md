# Bibliothèque de matériaux de la maquette 3D

Chaque dossier `<clé>/` contient les cartes d'un matériau, à la taille donnée dans `../catalogue_materiaux.py` :
- `couleur.jpg` : la couleur (photo à plat, sans ombre) ;
- `relief.jpg` : carte de normales (OpenGL) — joints de carreaux, fibres du bois, grain du tissu ;
- `rugosite.jpg` : lustré (noir) ou mat (blanc) ;
- `source.json` : provenance et licence.

`generer_3d.py` intègre au fichier de visite seulement les matériaux employés par la scène.

## Commandes
    python3 renovation/outils/materiaux.py liste
    python3 renovation/outils/materiaux.py telecharger            # tout ce qui manque
    python3 renovation/outils/materiaux.py ajouter quartz-calacatta photo_dalle.jpg --taille 1.6 --rugosite 0.1

## D'où viennent les matériaux
Recherche faite le 2026-10-29.
- **Format** : aucun fournisseur ne livre ses matériaux en SVG (le SVG est un dessin vectoriel, utile pour un motif
  de calepinage, pas pour une matière). Le standard est le **jeu de cartes « PBR »** (couleur, relief, rugosité en
  JPG/PNG), parfois en MaterialX, glTF ou Substance (.sbsar). C'est ce que la visionneuse lit maintenant.
- **ambientCG** (https://ambientcg.com) : plus de 2 000 matériaux, licence CC0 (domaine public), API publique sans clé ;
  le script télécharge directement les cartes 1K. Source principale ici.
- **Poly Haven** (https://polyhaven.com) : matériaux CC0 de grande qualité ; même script (`"source": "polyhaven"`).
- **Fabricants** :
  - Egger offre des fichiers BIM gratuits et les décors pour les logiciels de planification dans l'espace myEGGER (compte requis).
  - Cosentino (Silestone, Dekton) offre des photos haute résolution des couleurs dans sa zone de téléchargement. Ce sont des photos, pas des cartes PBR : on les ajoute avec `ajouter`.
  - Syncronia héberge gratuitement des textures de produits de fabricants (couleur, relief, réflexion), dont Silestone et Dekton. Le site refuse les téléchargements automatiques depuis l'environnement de travail ; un fichier téléchargé à la main s'ajoute avec `ajouter`.
  - Les textures de céramistes (Marazzi, Porcelanosa, Mutina) se trouvent surtout sur des marchés tiers (CGTrader, SketchUp Texture Club), souvent payants ou à usage limité : vérifier la licence.
- **Peinture** : les couleurs sont des codes hexadécimaux dans `scene_3d.py` (`peintures`), avec la référence du nuancier.

Pour un produit précis choisi en magasin (comptoir, carreau, plancher), le plus fiable est la photo à plat du
fabricant (ou un échantillon photographié de face, en lumière douce) ajoutée avec `ajouter`, avec sa vraie largeur.
