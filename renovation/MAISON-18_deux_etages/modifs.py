"""MAISON-18 — Les deux étages réunis : sous-sol (SS-17 allégé) + rez-de-chaussée réaménagé (grande entrée vitrée avec
l'escalier, chambre arrière avec lit king, bureau-gaming dans la chambre avant), une seule maquette où l'on monte et descend.

- Sous-sol : ss_modifs.py (copie de SS-17 : base_ss16_modifs.py + zone_*.py).
- Rez-de-chaussée : base_rdc01_modifs.py (copie du relevé photo RDC-01) + modules rdc_*.py qui peuvent définir
  appliquer_modifs_rdc(maison, ctx) : modifie EN PLACE le niveau RDC de maison (murs, ouvertures, éléments, pièces, notes).
  ctx = {"rdc": niveau RDC, "ss": niveau SS, "rdc_ss17": niveau RDC tel que la lignée SS-17 le dessinait (escalier)}.
Feuilles P-129 (sous-sol) et P-130 (rez-de-chaussée). Pouces, repère de la maison.
"""
import copy
import importlib.util
import os

ICI = os.path.dirname(os.path.abspath(__file__))
RDC_ZONES = ["rdc_corrections", "rdc_entree", "rdc_chambre_arriere", "rdc_bureau", "rdc_cuisine", "rdc_cafe_sdb"]


def _charger(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(ICI, fichier))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _niv(maison, nid):
    return next(n for n in maison["niveaux"] if n["id"] == nid)


def appliquer(maison):
    base = copy.deepcopy(maison)
    m_ss = _charger("m18_ss_modifs", "ss_modifs.py").appliquer(copy.deepcopy(base))      # SS-17 (sous-sol + son RDC)
    m_rdc = _charger("m18_rdc01_modifs", "base_rdc01_modifs.py").appliquer(copy.deepcopy(base))   # relevé photo du RDC
    maison = m_ss
    rdc_ss17 = _niv(m_ss, "RDC")
    i = next(k for k, n in enumerate(maison["niveaux"]) if n["id"] == "RDC")
    maison["niveaux"][i] = copy.deepcopy(_niv(m_rdc, "RDC"))
    rdc = maison["niveaux"][i]
    # l'escalier qui arrive à l'entrée avant (dessiné par la lignée SS) est reporté sur le relevé du RDC
    deja = {e["id"] for e in rdc["elements"]}
    rdc["elements"] += [copy.deepcopy(e) for e in rdc_ss17["elements"] if e["type"] == "escalier" and e["id"] not in deja]
    ctx = {"rdc": rdc, "ss": _niv(maison, "SS"), "rdc_ss17": rdc_ss17}
    for z in RDC_ZONES:
        if os.path.isfile(os.path.join(ICI, z + ".py")):
            mz = _charger("m18_" + z, z + ".py")
            if hasattr(mz, "appliquer_modifs_rdc"):
                mz.appliquer_modifs_rdc(maison, ctx)
    p = maison["projet"]
    p.update({"proposition": "MAISON-18", "revision": "A", "date": "2026-11-01", "titre_notes": "NOTES DE LA PROPOSITION",
              "mention": "PROPOSITION MAISON-18 — LES DEUX ÉTAGES : GRANDE ENTRÉE VITRÉE, CHAMBRE KING, BUREAU-GAMING — ESQUISSE À VALIDER",
              "nom_pdf": "MAISON-18_deux_etages.pdf"})
    _niv(maison, "SS")["feuille"], _niv(maison, "SS")["nom"] = "P-129", "Sous-sol proposé"
    rdc["feuille"], rdc["nom"] = "P-130", "Rez-de-chaussée proposé"
    # notes de la feuille P-130 (le cartouche en tient 6) : le détail est dans DESIGN.md
    notes = [
        "Esquisse sur le relevé photo RDC-01 (le reste est l'existant ; cotes à mesurer) ; fenêtre du salon descendue (allège ≈ 20 po).",
        "Grande entrée ouverte : garde-robes du hall enlevées ; escalier entouré d'un garde-corps de verre.",
        "Escalier vers le sous-sol : trémie ≈ 3 × 10 pi ; échappée ≈ 1,96 m à vérifier ; garde-corps de 42 po conseillé.",
        "Chambre des parents : lit king, mur de tête en bois de grange, garde-robes réunies à portes coulissantes.",
        "Bureau-gaming (ancienne chambre avant) : 2 postes face à la fenêtre avant.",
        "Poutre et appuis de l'ancienne cloison hall/salon, coupe-feu entre logements : à valider avec la Ville et un professionnel.",
    ]
    rdc["notes"] = [{"id": f"note-RDC-P{i + 1:02d}", "texte_original": None, "photo": None, "interpretation": t} for i, t in enumerate(notes)]
    # fenêtres agrandies vers le bas et congélateur (client, 2026-11-02) : allège de la fenêtre du salon dans les données (le plan
    # ne dessine pas l'allège ; la 3D la prend dans base_rdc01_scene.py, SCENE["fenetres"]) ; note 1 de P-129
    for o in rdc["ouvertures"]:
        if o["id"] == "ouv-RDC-002":
            o["allege"] = {"valeur": 20, "source": "PRÉSUMÉ", "photo": None,
                           "note": "MAISON-18 (client, 2026-11-02 : « plus grande vers le bas ») : allège abaissée d'environ 34 à 20 po "
                                   "(HYPOTHÈSE), tête et linteau 2-2×10 inchangés ; à mesurer et à valider"}
    ss = _niv(maison, "SS")
    if ss.get("notes"):
        ss["notes"][0]["interpretation"] = "Fenêtres agrandies par le bas (allège ≈ 40 po, sauf bain et lavage) ; congélateur au lavage."
    return maison
