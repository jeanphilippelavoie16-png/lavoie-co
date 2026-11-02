"""SS-17 — Rangement des chambres d'enfants (lits queen), banc-cabane sous l'escalier, gym refait, sous-sol optimisé.

Construit par-dessus SS-16 : base_ss16_modifs.py est une copie figée de ../SS-16_bain_vedette_beton_poli/modifs.py.
Chaque zone a son module (zone_chambre1.py, zone_chambre2.py, zone_escalier.py, zone_gym.py, zone_global.py) ;
ils peuvent définir :
- appliquer_modifs(L, base) : AVANT la construction, modifie EN PLACE les listes de SS-16
  (L["MURS"], L["PORTES"], L["PIECES"], L["COUPES"], L["EQUIPEMENTS"], L["ESCALIER"]) ;
- apres_modifs(maison, base) : APRÈS la construction (éléments de la base, notes, ouvertures existantes...).
Pouces, repère de la maison.
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


def zones():
    return [_charger("ss17_" + z, z + ".py") for z in ZONES if os.path.isfile(os.path.join(ICI, z + ".py"))]


def appliquer(maison):
    base = _charger("ss17_base_modifs", "base_ss16_modifs.py")
    base.SOURCE = "proposition SS-17 (esquisse)"
    L = {k: getattr(base, k) for k in ("MURS", "PORTES", "PIECES", "COUPES", "EQUIPEMENTS", "ESCALIER")}
    zs = zones()
    for z in zs:
        if hasattr(z, "appliquer_modifs"):
            z.appliquer_modifs(L, base)
    maison = base.appliquer(maison)
    p = maison["projet"]
    p.update({"proposition": "SS-17", "revision": "A", "date": "2026-11-01",
              "mention": "PROPOSITION SS-17 — RANGEMENT DES CHAMBRES D'ENFANTS, ESCALIER, GYM, SOUS-SOL OPTIMISÉ — ESQUISSE À VALIDER",
              "nom_pdf": "SS-17_rangement_enfants_gym.pdf"})
    ss = next(n for n in maison["niveaux"] if n["id"] == "SS")
    rdc = next(n for n in maison["niveaux"] if n["id"] == "RDC")
    ss["feuille"], rdc["feuille"] = "P-127", "P-128"
    for z in zs:
        if hasattr(z, "apres_modifs"):
            z.apres_modifs(maison, base)
    # notes de la feuille P-127 (le cartouche en tient 6) : le détail de chaque zone est dans DESIGN.md
    notes = [
        "Esquisse par-dessus SS-16 (le reste est l'existant, base R0) ; béton poli d'un seul tenant.",
        "Chambres d'enfants : lits queen 60 × 80 et rangement intégré de chêne ; fenêtres d'évacuation ouvrantes à vérifier.",
        "Walk-in (ancien caveau) : isolé, évents fermés, chauffé ; porte dérobée dans le mur de chêne de la chambre 2.",
        "Escalier : banc-cabane bas (≤ 26 po) dessous ; vides entre les marches (5½ po) à valider avec des enfants.",
        "Gym : cardio contre le mur avant, mur-miroir sur le mur du lavage, porte vitrée coulissante.",
        "Insonorisation, VRC et déshumidificateur ; hauteur 8 pi (propriétaire) ; à valider avec la Ville et un professionnel.",
    ]
    ss["notes"] = [{"id": f"note-SS-P{i + 1:02d}", "texte_original": None, "photo": None, "interpretation": t} for i, t in enumerate(notes)]
    return maison
