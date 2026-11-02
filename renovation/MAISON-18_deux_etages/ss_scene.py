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

# --- intégration : la ligne « Chambres » de SS-16 est remplacée par les lignes des deux chambres ; arrêts dans l'ordre du parcours
SCENE["palette"] = [p for p in SCENE["palette"] if p[0] != "Chambres"]
_ORDRE = ["Entrée", "Vestiaire", "Casiers d'hiver des garçons", "Seuil à neige (porte de côté)", "Escalier", "Escalier vu du séjour",
          "Banc-cabane cinéma (sous l'escalier)", "Coin-cabane et sa lune", "Séjour", "Galerie de famille", "Coin cinéma (toile)",
          "Banc à jouets sous la toile", "Gym (porte vitrée)", "Gym — mur-miroir et zone au sol", "Gym — cardio", "Salle de lavage",
          "Paniers de linge des garçons", "Congélateur (salle de lavage)", "Hall — le mur de la poutre", "Trajet de nuit vers la salle de bain",
          "Salle de bain (entrée)", "Le bain (alcôve de pierre)", "Douche à l'italienne (derrière la poutre)",
          "Vanité (marchepied, crochets des garçons)"]
_rang = {n: i for i, n in enumerate(_ORDRE)}
SCENE["visites"] = sorted(SCENE["visites"], key=lambda v: _rang.get(v["nom"], len(_ORDRE)))   # tri stable : chambres et walk-in à la fin, dans leur ordre

# --- couleurs d'accent utilisées par de petits objets (livres, pictogrammes, coussins) des autres zones : les chambres
# refaites ont retiré les peintures qui les définissaient ; on les redéfinit ici pour qu'ils ne s'affichent pas en blanc
for _nom, _v in (("Accent argile", ["#C39A82", "petits objets : livres, pictogrammes, coussins", "art-argile"]),
                 ("Accent sable", ["#D8C3A0", "petits objets : livres, pictogrammes, coussins", "art-sable"]),
                 ("Accent sauge", ["#A6AF9A", "petits objets : livres, pictogrammes", "art-sauge"])):
    if not any(len(v) > 2 and v[2] == _v[2] for v in SCENE.get("peintures", {}).values()):
        SCENE.setdefault("peintures", {})[_nom] = _v
