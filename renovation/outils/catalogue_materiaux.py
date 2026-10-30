"""Catalogue des matériaux de la maquette 3D.

Chaque entrée donne la provenance (ambientCG ou Poly Haven, licence CC0, ou un fichier de fournisseur ajouté avec
`materiaux.py ajouter`) et la taille réelle couverte par une répétition de la texture, pour que les
carreaux, les lames et les veines aient leur vraie grandeur. Les cartes sont dans materiaux/<clé>/ :
couleur.jpg (sRGB), relief.jpg (normales OpenGL), rugosite.jpg (gris : noir = lustré, blanc = mat).

Les clés remplacent les matériaux de même nom de la visionneuse (chene, placage, quartz, ...).
"""

CATALOGUE = {
    # clé : source, id, taille (m) d'une répétition, réglages de rendu, usage
    "chene": {"source": "ambientcg", "id": "WoodFloor051", "taille_m": 1.8, "ajustement": {"luminosite": 1.3, "saturation": 0.7},
              "usage": "plancher de chêne pâle, lames larges"},
    "placage": {"source": "polyhaven", "id": "oak_veneer_01", "taille_m": 0.9, "usage": "chêne des armoires, claustra, marches"},
    "quartz": {"source": "ambientcg", "id": "Marble019", "taille_m": 1.4, "ajustement": {"luminosite": 1.05, "saturation": 0.4}, "rugosite": 0.12, "usage": "comptoirs, vanité (quartz veiné)"},
    "porcelaine": {"source": "ambientcg", "id": "Tiles040", "taille_m": 4.88, "usage": "porcelaine 24 × 24 po au sol (8 carreaux par répétition)"},
    "tuile_blanche": {"source": "ambientcg", "id": "Tiles136A", "taille_m": 0.91, "ajustement": {"saturation": 0.4}, "rugosite": 0.15, "usage": "tuile blanche de douche"},
    "zellige-vert": {"source": "ambientcg", "id": "Tiles032", "taille_m": 1.0, "rugosite": 0.1, "usage": "zellige vert du coin bar"},
    "terrazzo": {"source": "ambientcg", "id": "Terrazzo011", "taille_m": 0.7, "usage": "terrazzo de la salle de lavage"},
    "tissu": {"source": "ambientcg", "id": "Fabric030", "taille_m": 0.5, "ajustement": {"luminosite": 1.7}, "usage": "sofa, tête de lit"},
    "draps": {"source": "ambientcg", "id": "Fabric019", "taille_m": 0.5, "usage": "literie"},
    "tapis": {"source": "ambientcg", "id": "Carpet016", "taille_m": 0.8, "usage": "tapis"},
    "cuir": {"source": "ambientcg", "id": "Leather023", "taille_m": 0.5, "usage": "fauteuils en cuir cognac"},
    "beton": {"source": "ambientcg", "id": "Concrete034", "taille_m": 2.0, "usage": "dalle du caveau"},
    "inox": {"source": "ambientcg", "id": "Metal009", "taille_m": 0.6, "metal": 1.0, "usage": "frigo, éviers, électros"},
    "laiton": {"source": "ambientcg", "id": "Metal048A", "taille_m": 0.4, "metal": 1.0, "usage": "robinet du bar, poignées"},
    "platre": {"source": "ambientcg", "id": "Plaster001", "taille_m": 1.5, "relief_seul": True,
               "usage": "relief des murs peints (la couleur vient de la peinture)"},
}
