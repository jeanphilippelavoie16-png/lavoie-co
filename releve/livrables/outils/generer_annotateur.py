#!/usr/bin/env python3
"""Génère ../annotateur/annotateur.html : la page web où le propriétaire annote les plans
(notes épinglées, traits, « à enlever ») et répond aux repères ⚠ du registre des écarts.

Les annotations et réponses sont gardées dans la base de l'artefact (capability `db`) :
  annotations/<id>  {niveau, kind: note|trait|retirer, x, y | points, texte, statut, cree, reponse_claude?}
  reponses/<ecart>  {ecart, niveau, texte, maj, statut}
Coordonnées stockées en pouces, repère maison (origine coin avant-gauche, y vers l'arrière).

Usage : python3 generer_annotateur.py   (après generer_plans.py)
"""
import json, os, re

ICI = os.path.dirname(os.path.abspath(__file__))
RAC = os.path.normpath(os.path.join(ICI, ".."))
FEUILLES = [("SS", "A-100_sous-sol.svg"), ("RDC", "A-101_rdc.svg")]


def origine(svg, niv):
    """(X0, Y0) : position SVG du point maison (0, 0), lue sur le mur avant mur-<niv>-001."""
    i = svg.index(f'id="mur-{niv}-001"')
    bloc = svg[i:svg.index("</g>", i)]
    nums = [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", " ".join(re.findall(r'\sd="([^"]+)"', bloc)))]
    xs, ys = nums[0::2], nums[1::2]
    return min(xs), max(ys)


def main():
    M = json.load(open(os.path.join(RAC, "donnees", "maison.json"), encoding="utf-8"))
    feuilles = {}
    for niv, f in FEUILLES:
        svg = open(os.path.join(RAC, "svg", f), encoding="utf-8").read()
        svg = re.sub(r"^<\?xml[^>]*>\s*", "", svg)
        x0, y0 = origine(svg, niv)
        n = next(n for n in M["niveaux"] if n["id"] == niv)
        feuilles[niv] = {"svg": svg, "x0": x0, "y0": y0, "nom": n["nom"], "feuille": n["feuille"]}
    ecarts = [{"id": e["id"], "num": int(e["id"].split("-")[1]), "niveau": e["niveau"], "impact": e["impact"],
               "statut": e.get("statut", "ouvert"), "description": e["description"],
               "hypothese": e.get("hypothese_retenue", ""), "a_valider": e.get("a_valider_sur_place", "")}
              for e in M.get("ecarts", [])]
    donnees = json.dumps({"feuilles": feuilles, "ecarts": ecarts, "projet": M["projet"]["nom"],
                          "date": M["projet"].get("date", ""), "revision": M["projet"].get("revision", "")},
                         ensure_ascii=False).replace("</", "<\\/")
    gabarit = open(os.path.join(ICI, "annotateur_gabarit.html"), encoding="utf-8").read()
    os.makedirs(os.path.join(RAC, "annotateur"), exist_ok=True)
    sortie = os.path.join(RAC, "annotateur", "annotateur.html")
    with open(sortie, "w", encoding="utf-8") as fh:
        fh.write(gabarit.replace("/*__DONNEES__*/null", donnees))
    print("annotateur écrit :", sortie)


if __name__ == "__main__":
    main()
