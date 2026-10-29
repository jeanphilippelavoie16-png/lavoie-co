"""Catalogue des modèles 3D (GLB) de la maquette : provenance, licence, attribution.

Les fichiers optimisés (meshopt + textures WebP) sont dans modeles/. Dans scene_3d.py, un meuble s'écrit
{"forme": "modele", "cle": <clé>, "x", "y", "z", "rot" (degrés, sens antihoraire vu de dessus), "L" (longueur en po)
ou "H" (hauteur en po)} : le modèle est mis à l'échelle et posé au sol, centré sur (x, y).
"""

CATALOGUE = {}
