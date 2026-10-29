#!/usr/bin/env python3
"""Génère ../RAPPORT.md à partir de ../donnees/maison.json et ../donnees/verifications.txt.

Usage : python3 generer_rapport.py [--json ../donnees/maison.json] [--sortie ..]
Appelé automatiquement à la fin de generer_plans.py. Déterministe.
"""
import argparse, json, os, re

IMPACTS = ["critique", "moyen", "faible"]
ORDRE_SOURCE = ["LU", "DÉDUIT", "ESTIMÉ", "PRÉSUMÉ", "ILLISIBLE"]


def pp(v):
    """pouces → 12'-6\" (au ¼ po)."""
    if v is None:
        return "—"
    s = "-" if v < 0 else ""
    v = round(abs(v) * 4) / 4
    p, i = int(v // 12), v - 12 * int(v // 12)
    ent, frac = int(i), i - int(i)
    fr = {0: "", 0.25: "¼", 0.5: "½", 0.75: "¾"}[round(frac, 2)]
    return f"{s}{p}'-{ent}{fr}\""


def nf(x, d=1):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


def premiere_phrase(t, maxi=260):
    """Première phrase complète (parenthèses et guillemets équilibrés) ; texte entier si aucune coupure propre."""
    for m in re.finditer(r"(?<=[.;:])\s", t):
        bout = t[:m.start()].rstrip(" ;:")
        if len(bout) >= 40 and bout.count("(") == bout.count(")") and bout.count("«") == bout.count("»"):
            return bout if len(bout) <= maxi or True else bout
    return t


def cell(t):
    return str(t if t is not None else "").replace("|", "\\|").replace("\n", " ")


def main():
    ap = argparse.ArgumentParser()
    ici = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--json", default=os.path.join(ici, "..", "donnees", "maison.json"))
    ap.add_argument("--sortie", default=os.path.join(ici, ".."))
    a = ap.parse_args()
    M = json.load(open(a.json, encoding="utf-8"))
    P = M["projet"]
    ver_path = os.path.join(a.sortie, "donnees", "verifications.txt")
    ver = open(ver_path, encoding="utf-8").read() if os.path.exists(ver_path) else ""
    brute = dict(re.findall(r"\[(\w+)\] brute \(empreinte\) ([\d  ,]+) pi²", ver))

    L = []
    w = L.append
    w(f"# Relevé de l'existant — {P['nom']}")
    w("")
    w(f"**RELEVÉ DE L'EXISTANT — PRÉLIMINAIRE, À VALIDER SUR PLACE** · Révision {P.get('revision', 'R0')} · {P.get('date', '')}")
    w("")
    w("Ce relevé reproduit, en plans propres et modifiables, les plans d'origine dessinés à la main. "
      "Il ne contient aucune proposition de rénovation. Aucune mesure n'a été prise sur place : "
      "toutes les dimensions viennent des documents photographiés, avec leur source.")
    w("")

    # ------------------------------------------------------------------ livrables
    w("## 1. Livrables")
    w("")
    w("| Dossier | Contenu |")
    w("|---|---|")
    feuilles = ", ".join(f"{n['feuille']} {n['nom']}" for n in M["niveaux"])
    w(f"| `svg/` | Une feuille par niveau ({feuilles}), calques Inkscape, 1 unité = 1 po réel, tabloïd 17 × 11 po à l'échelle |")
    w("| `pdf/plans_existants.pdf` | Toutes les feuilles, à l'échelle (vérifier avec l'échelle graphique du cartouche) |")
    w("| `png/` | Aperçus 150 ppp |")
    w("| `dxf/` | Un fichier par niveau, unités en pouces, mêmes calques et identifiants (XDATA « RELEVE ») |")
    w("| `donnees/maison.json` | Source de vérité unique (géométrie, cotes, sources, registre des écarts) |")
    w("| `donnees/tableau_pieces.csv` | Tableau des pièces (Excel : séparateur « ; », décimales à virgule) |")
    w("| `donnees/verifications.txt` | Rapport des contrôles automatiques |")
    w("| `outils/` | `generer_plans.py` (tout régénérer en une commande), `README.md`, `pretraitement.py` |")
    w("")

    # ------------------------------------------------------------------ photos
    w("## 2. Photos utilisées")
    w("")
    w("Numérotation dans l'ordre d'envoi. Aucune photo des lieux réels n'a été fournie.")
    w("")
    corr = P.get("correspondance_photos_internes", {})
    w("| Photo | Document | Fichier de travail |")
    w("|---|---|---|")
    for ph in P.get("photos", []):
        w(f"| {ph['id']} | {cell(ph.get('description'))} | `travail/photos/{corr.get(ph['id'], ph['id'])}.jpg` |")
    w("")
    w("Les fichiers du dossier `travail/` (photos, tuiles, vignettes d'arbitrage, extractions) gardent la numérotation "
      "interne de la colonne de droite ; tous les livrables utilisent la numérotation de gauche.")
    w("")

    # ------------------------------------------------------------------ convention
    w("## 3. Repère et convention de cotation")
    w("")
    w(f"- **Origine :** {P.get('origine', '')}. Unité interne : pouce ; affichage en pieds-pouces, métrique entre parenthèses.")
    nord = P.get("nord") or {}
    if nord.get("angle_deg") is not None:
        w(f"- **Nord :** {nord['angle_deg']}° dans le sens horaire depuis l'axe façade → arrière ({nord.get('source', '')}, "
          f"photo {nord.get('photo', '')}{' ; ' + nord['note'] if nord.get('note') else ''}). La façade avant regarde donc à peu près vers le sud.")
    w(f"- **Convention de cotation de l'original :** {P.get('convention_cotation', '')}")
    w("- **Sources des dimensions :** LU (écrit sur le plan) · DÉDUIT (calculé à partir d'autres cotes) · "
      "ESTIMÉ (mesuré dans l'image, précédé de « ≈ » sur les plans) · PRÉSUMÉ (standard de construction faute d'info) · ILLISIBLE. "
      "Un repère orange ⚠n renvoie à l'écart n du registre (section 6).")
    w("")

    # ------------------------------------------------------------------ hypothèses
    w("## 4. Hypothèses retenues")
    w("")
    w("- **État représenté : les plans d'origine (1957).** Le croquis d'ingénieur de 2016 (photo 1) montre moins de cloisons "
      "et des colonnes retirées ; il n'est pas un relevé complet (la salle de bain n'y figure même pas). Les cloisons de 1957 "
      "sont donc conservées et chaque différence est consignée comme écart critique, à valider en visite.")
    w("- **Aucune mesure sur place (ancres vides)** : le relevé n'est calé sur aucune mesure du bâtiment réel.")
    w("- **Les cotes écrites priment sur le dessin** : la géométrie est construite à partir des chaînes de cotes ; "
      "les proportions du dessin servent seulement à combler les trous (ESTIMÉ).")
    w("- **Lecture des cotes** : deux lectures indépendantes de chaque cote, puis une 3e lecture à l'aveugle pour chaque désaccord ; "
      "une cote non tranchée garde le statut « conflit » et figure au registre.")
    w("- **Murs porteurs** : aucun plan n'écrit « porteur » pour l'état actuel ; tous les murs sont « inconnu », "
      "avec les indices notés dans `maison.json` (poutres dessous, axes porteurs d'origine du croquis 2016).")
    w("- **Épaisseurs** non cotées : valeurs PRÉSUMÉES (voir écarts) ; hauteurs de plafond : inconnues, laissées vides.")
    w("")

    # ------------------------------------------------------------------ superficies
    w("## 5. Superficies")
    w("")
    w("| Niveau | Feuille | Superficie brute (empreinte) | Σ superficies nettes des pièces | Nb de pièces |")
    w("|---|---|---|---|---|")
    for n in M["niveaux"]:
        sp = sum((p.get("superficie") or {}).get("valeur") or 0 for p in n["pieces"])
        b = brute.get(n["id"])
        bt = f"{b.strip()} pi² ({nf(float(b.replace(' ', '').replace(' ', '').replace(',', '.')) * 0.09290304)} m²)" if b else "—"
        w(f"| {n['nom']} | {n['feuille']} | {bt} | {nf(sp)} pi² ({nf(sp * 0.09290304)} m²) | {len(n['pieces'])} |")
    w("")
    w("Superficie brute = empreinte extérieure des murs du niveau, excroissances comprises (caveau, entrée arrière, etc.). "
      "Contrôle : Σ pièces + Σ murs = superficie brute (voir `donnees/verifications.txt`). Détail par pièce : `donnees/tableau_pieces.csv`.")
    w("")

    # ------------------------------------------------------------------ registre
    E = M.get("ecarts", [])
    cnt = {i: sum(e["impact"] == i for e in E) for i in IMPACTS}
    w("## 6. Registre des écarts")
    w("")
    w(f"{len(E)} écarts : **{cnt['critique']} critiques**, {cnt['moyen']} moyens, {cnt['faible']} faibles.")
    w("")
    w("| # | Niveau | Impact | Description | Hypothèse retenue |")
    w("|---|---|---|---|---|")
    for e in E:
        num = int(e["id"].split("-")[1])
        w(f"| ⚠{num} | {e['niveau']} | {e['impact']} | {cell(e['description'])} | {cell(e['hypothese_retenue'])} |")
    w("")

    # cotes en conflit / illisibles
    w("### Cotes en conflit ou illisibles")
    w("")
    w("| Cote | Niveau | Texte | Lecture 1 | Lecture 2 | Statut |")
    w("|---|---|---|---|---|---|")
    k = 0
    for n in M["niveaux"]:
        for c in n.get("cotes", []):
            if c.get("statut") in ("conflit", "illisible"):
                k += 1
                w(f"| {c['id']} | {n['id']} | {cell(c.get('texte_original'))} | {cell(c.get('lecture_1'))} | {cell(c.get('lecture_2'))} | {c['statut']} |")
    if not k:
        w("| — | | | | | |")
    w("")

    # ------------------------------------------------------------------ mesures
    w("## 7. Mesures à prendre sur place (par priorité)")
    w("")
    w("Aucune zone de rénovation n'a été désignée : le tri suit l'impact des écarts (critiques d'abord). "
      "Chaque ligne dit où mesurer et pourquoi.")
    w("")
    i = 0
    for imp in IMPACTS:
        lot = [e for e in E if e["impact"] == imp and e.get("a_valider_sur_place")]
        if not lot:
            continue
        w(f"### Impact {imp}")
        w("")
        for e in lot:
            if e.get("statut") == "sans objet":
                continue
            # une même mesure à faire (même texte) n'est listée qu'une fois, avec tous ses repères
            meme = [x for x in E if x.get("a_valider_sur_place") == e["a_valider_sur_place"] and x.get("statut") != "sans objet"]
            if meme[0] is not e:
                continue
            i += 1
            nums = ", ".join(f"⚠{int(x['id'].split('-')[1])}" for x in meme)
            w(f"{i}. **{cell(e['a_valider_sur_place'])}** — Pourquoi : {cell(premiere_phrase(e['description']))} ({nums}, {e['niveau']})")
        w("")

    w("## 8. Modifier et régénérer")
    w("")
    w("Toute correction se fait dans `donnees/maison.json`, puis : `cd outils && python3 generer_plans.py` "
      "(régénère SVG, PDF, PNG, DXF, CSV, vérifications et ce rapport). Voir `outils/README.md`. "
      "Le calque `90-RENO-Propose` des SVG est vide et prêt pour les propositions de rénovation.")
    w("")

    out = os.path.join(a.sortie, "RAPPORT.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print("RAPPORT.md écrit :", out)


if __name__ == "__main__":
    main()
