"""MAISON-18 — maquette des deux étages.

- Sous-sol : ss_scene.py (copie de SS-17 : base_ss16_scene.py + zone_*.py).
- Rez-de-chaussée : base_rdc01_scene.py (copie du relevé RDC-01, corrigée) + modules rdc_*.py qui peuvent définir
  appliquer_scene_rdc(S, h) (S = SCENE du RDC à modifier en place, h = module base_rdc01_scene : helpers B, A, MOD...).
- ETAGE=SS ou ETAGE=RDC (variable d'environnement) : n'exporte que cet étage (scène à un seul niveau, pour les essais).
- Sinon SCENE = {"titre", "etages": [scène SS, scène RDC], "depart"} : la visionneuse empile les étages (contrat « etages »).
"""
import importlib.util
import os

ICI = os.path.dirname(os.path.abspath(__file__))
RDC_ZONES = ["rdc_corrections", "rdc_entree", "rdc_chambre_arriere", "rdc_bureau"]
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

# --- Extérieur (opt-in) : exterieur.py fournit EXTERIEUR (terrain, enveloppe de la maison, cour arrière du plan DAG ; contrat
# dans son docstring), objets en z ABSOLU dans le repère du plancher du sous-sol.
# - EXT_APERCU=1 : aperçu dans le moteur actuel, qui ne marche pas encore dehors : les objets d'EXTERIEUR sont ajoutés au
#   mobilier de l'étage SS (z inchangé) et ses couleurs (alias « ext-… ») aux peintures du sous-sol (aussi avec ETAGE=SS).
# - Sinon (maquette à deux étages) : SCENE["exterieur"] = EXTERIEUR, que le moteur ignore tant qu'il ne le gère pas.
if os.path.isfile(os.path.join(ICI, "exterieur.py")):
    _ext = _charger("m18_exterieur", "exterieur.py").EXTERIEUR
    if os.environ.get("EXT_APERCU") == "1":
        _S = SCENE["etages"][0] if "etages" in SCENE else SCENE
        if _S.get("niveau", "SS") == "SS":
            _S["mobilier"] = list(_S.get("mobilier", [])) + [dict(o) for o in _ext["objets"]]
            _S["peintures"] = dict(_S.get("peintures") or {}, **_ext["peintures"])
    elif "etages" in SCENE:
        SCENE["exterieur"] = _ext
