"""MAISON-18 — maquette des deux étages.

- Sous-sol : ss_scene.py (copie de SS-17 : base_ss16_scene.py + zone_*.py).
- Rez-de-chaussée : base_rdc01_scene.py (copie du relevé RDC-01, corrigée) + modules rdc_*.py qui peuvent définir
  appliquer_scene_rdc(S, h) (S = SCENE du RDC à modifier en place, h = module base_rdc01_scene : helpers B, A, MOD...).
- ETAGE=SS ou ETAGE=RDC (variable d'environnement) : n'exporte que cet étage (scène à un seul niveau, pour les essais).
- Sinon SCENE = {"titre", "etages": [scène SS, scène RDC], "depart", "exterieur"} : la visionneuse empile les étages (contrat
  « etages ») et dessine l'extérieur (exterieur.py).
"""
import importlib.util
import os

ICI = os.path.dirname(os.path.abspath(__file__))
RDC_ZONES = ["rdc_corrections", "rdc_entree", "rdc_chambre_arriere", "rdc_bureau", "rdc_cuisine", "rdc_cafe_sdb", "rdc_robot"]
# modules qui touchent les deux étages à la fois (ex. chute à linge du RDC au SS) : appliquer_scene_deux(SCENE), SCENE à deux étages
DEUX_ETAGES = ["chute_linge"]
TITRE = "MAISON-18 — Les deux étages"


def _charger(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(ICI, fichier))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def scene_ss():
    S = _charger("m18_ss_scene", "ss_scene.py").SCENE
    S["titre"] = TITRE + " — sous-sol"
    return S


def scene_rdc():
    h = _charger("m18_rdc01_scene", "base_rdc01_scene.py")
    S = h.SCENE
    S["titre"] = TITRE + " — rez-de-chaussée"
    for z in RDC_ZONES:
        if os.path.isfile(os.path.join(ICI, z + ".py")):
            mz = _charger("m18_scene_" + z, z + ".py")
            if hasattr(mz, "appliquer_scene_rdc"):
                mz.appliquer_scene_rdc(S, h)
    return S


_E = os.environ.get("ETAGE")
if _E == "SS":
    SCENE = scene_ss()
elif _E == "RDC":
    SCENE = scene_rdc()
else:
    _ss = scene_ss()
    SCENE = {"titre": TITRE, "etages": [_ss, scene_rdc()], "depart": dict(_ss["depart"], etage="SS")}
    for _z in DEUX_ETAGES:
        if os.path.isfile(os.path.join(ICI, _z + ".py")):
            _mz = _charger("m18_scene_" + _z, _z + ".py")
            if hasattr(_mz, "appliquer_scene_deux"):
                _mz.appliquer_scene_deux(SCENE)

# --- Extérieur : exterieur.py fournit EXTERIEUR (terrain, enveloppe de la maison, cour arrière du plan DAG ; contrat dans son
# docstring), objets en z ABSOLU dans le repère du plancher du sous-sol. Maquette à deux étages : SCENE["exterieur"], que le
# moteur dessine (on marche dehors, on entre par les portes, vue « Extérieur » de la maquette). Avec ETAGE=SS ou RDC (un seul
# étage, repère de son plancher), pas d'extérieur.
if os.path.isfile(os.path.join(ICI, "exterieur.py")) and "etages" in SCENE:
    SCENE["exterieur"] = _charger("m18_exterieur", "exterieur.py").EXTERIEUR
    # balcon avant (photos du client, 2026-11-02) : balcon_avant.py complète ou remplace des éléments de l'extérieur
    if os.path.isfile(os.path.join(ICI, "balcon_avant.py")):
        _charger("m18_balcon_avant", "balcon_avant.py").appliquer_exterieur(SCENE["exterieur"])

# modules qui s'appliquent à la maquette complète, extérieur compris (fleuve et traversier, visiteur) :
# appliquer_scene_finale(SCENE), SCENE à deux étages avec SCENE["exterieur"]
# le visiteur (visiteur.py) est retiré à la demande du client (2026-11-08 : « enlève la personne qui cogne à la porte ») ;
# le module reste dans le dossier : remettre "visiteur" dans la liste pour le ramener
FINALE = ["fleuve"]
if "etages" in SCENE:
    for _z in FINALE:
        if os.path.isfile(os.path.join(ICI, _z + ".py")):
            _mz = _charger("m18_scene_" + _z, _z + ".py")
            if hasattr(_mz, "appliquer_scene_finale"):
                _mz.appliquer_scene_finale(SCENE)
