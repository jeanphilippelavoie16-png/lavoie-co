"""SS-17 — maquette 3D : la scène de SS-16 (base_ss16_scene.py, copie figée de
../SS-16_bain_vedette_beton_poli/scene_3d.py) + les modules de zone.

Chaque zone_*.py peut définir appliquer_scene(S, h) : S est le dictionnaire SCENE (à modifier en place : retirer des
éléments de S["mobilier"] dans SA zone seulement, en ajouter, ajuster S["visites"], S["lumieres"], S["palette"]...),
h est le module de base (helpers B, A, C, CY, CX, T, SPH, TOR, MOD, lit, commode...).
"""
import importlib.util
import os

ICI = os.path.dirname(os.path.abspath(__file__))
ZONES = ["zone_chambre1", "zone_chambre2", "zone_escalier", "zone_gym", "zone_global"]


def _charger(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(ICI, fichier))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


h = _charger("ss17_base_scene", "base_ss16_scene.py")
SCENE = h.SCENE
SCENE["titre"] = "SS-17 — Rangement des enfants, escalier, gym"
for _z in ZONES:
    if os.path.isfile(os.path.join(ICI, _z + ".py")):
        _m = _charger("ss17_scene_" + _z, _z + ".py")
        if hasattr(_m, "appliquer_scene"):
            _m.appliquer_scene(SCENE, h)
