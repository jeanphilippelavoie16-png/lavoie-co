#!/usr/bin/env python3
"""Construit un projet de rénovation à partir d'une COPIE des plans de base.

Les plans de base (relevé de l'existant) sont dans releve/livrables/ et ne sont jamais modifiés.
Chaque projet est un dossier renovation/<code>_<nom>/ qui contient modifs.py :

    def appliquer(maison):      # reçoit une copie de releve/livrables/donnees/maison.json
        ...                     # ajoute / retire murs, portes, pièces, éléments
        return maison

Usage : python3 renovation/outils/construire_projet.py renovation/SS-01_amenagement_sous-sol
Produit dans le dossier du projet : donnees/maison.json, svg/, pdf/, png/, dxf/, donnees/tableau_pieces.csv.
"""
import copy, importlib.util, json, os, subprocess, sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, "..", ".."))
BASE = os.path.join(RACINE, "releve", "livrables", "donnees", "maison.json")
GENERATEUR = os.path.join(RACINE, "releve", "livrables", "outils", "generer_plans.py")


def main(dossier):
    dossier = os.path.abspath(dossier)
    if os.path.commonpath([dossier, os.path.join(RACINE, "releve")]) == os.path.join(RACINE, "releve"):
        sys.exit("Refusé : un projet ne s'écrit jamais dans releve/ (plans de base).")
    spec = importlib.util.spec_from_file_location("modifs", os.path.join(dossier, "modifs.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    base = json.load(open(BASE, encoding="utf-8"))
    maison = mod.appliquer(copy.deepcopy(base))
    os.makedirs(os.path.join(dossier, "donnees"), exist_ok=True)
    sortie_json = os.path.join(dossier, "donnees", "maison.json")
    with open(sortie_json, "w", encoding="utf-8") as f:
        json.dump(maison, f, ensure_ascii=False, indent=1)
        f.write("\n")
    subprocess.run([sys.executable, GENERATEUR, "--json", sortie_json, "--sortie", dossier], check=True)


if __name__ == "__main__":
    main(sys.argv[1])
