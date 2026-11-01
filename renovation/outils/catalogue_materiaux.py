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
    # --- rez-de-chaussée actuel (RDC-01, relevé photo du 2026-11-01)
    "brique_rouge": {"source": "polyhaven", "id": "red_brick_03", "taille_m": 0.87, "ajustement": {"luminosite": 1.12}, "usage": "placage de brique rouge à joints pâles (cuisine du RDC)"},
    "ardoise_noire": {"source": "ambientcg", "id": "Tiles138", "taille_m": 7.32, "ajustement": {"luminosite": 0.55, "saturation": 0.6}, "usage": "tuile d'ardoise noire 24 × 24 po (cuisine, entrée du RDC)"},
    "erable": {"source": "ambientcg", "id": "WoodFloor047", "taille_m": 1.5, "ajustement": {"luminosite": 1.0, "saturation": 0.72}, "usage": "plancher d'érable naturel clair, lames étroites (RDC)"},
    "bois_grange": {"source": "polyhaven", "id": "weathered_brown_planks", "taille_m": 1.2, "ajustement": {"luminosite": 0.72, "saturation": 1.15}, "usage": "bois de grange multicolore (comptoirs et îlot du RDC)"},
    "bois_brut": {"source": "ambientcg", "id": "Wood060", "taille_m": 0.8, "usage": "bois brut teint brun-roux (poutres et poteaux du RDC)"},
    "pin_teint": {"source": "polyhaven", "id": "coated_pine_02", "taille_m": 0.9, "ajustement": {"luminosite": 0.8, "saturation": 0.85}, "rugosite": 0.55, "usage": "pin noueux teint (portes, cadrages et plinthes du RDC)"},
    "papier_planches": {"source": "polyhaven", "id": "wood_planks_grey", "taille_m": 1.4, "ajustement": {"luminosite": 1.7, "saturation": 0.5}, "usage": "papier peint imitation planches grises (chambre du RDC)"},
    "crepi": {"source": "polyhaven", "id": "white_stucco_02", "taille_m": 0.8, "usage": "plafond texturé (crépi) du salon du RDC"},
    "bois_recupere": {"source": "polyhaven", "id": "wood_cabinet_worn_long", "taille_m": 1.0, "usage": "bois de récupération foncé (table de la salle à manger du RDC)"},
    "inox": {"source": "ambientcg", "id": "Metal009", "taille_m": 0.6, "metal": 1.0, "usage": "frigo, éviers, électros"},
    "laiton": {"source": "ambientcg", "id": "Metal048A", "taille_m": 0.4, "metal": 1.0, "usage": "robinet du bar, poignées"},
    "beton_poli": {"source": "ambientcg", "id": "Concrete016", "taille_m": 2.4, "ajustement": {"luminosite": 1.24, "saturation": 0.1},
                   "rugosite": 0.34, "vernis": 0.45, "vernis_rugosite": 0.22,
                   "usage": "béton poli gris pâle, léger marbrage (dalle meulée et densifiée ou chape polie) — tout le sous-sol de SS-16"},
    "platre": {"source": "ambientcg", "id": "Plaster001", "taille_m": 1.5, "relief_seul": True,
               "usage": "relief des murs peints (la couleur vient de la peinture)"},
}
