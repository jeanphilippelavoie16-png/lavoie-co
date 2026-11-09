"""CH-01 — La chambre des garçons, toute seule : état actuel (photos du 2026-11-09) et coin jeu proposé. Feuille P-131.

Demandes du client (2026-11-09) :
« Je veux que tu modélises la chambre en haut du coin avant comme elle est présentement. Je veux seulement garder le lit
superposé et le meuble blanc et que tu me proposes un coin jeu pour les gars pour jouer Lego, bac de jeu et place pour mettre
les livres. »
« Le bureau assis debout reste pas, c'est un test pour refaire la chambre bientôt et l'optimiser. Fais la chambre tout seul
dans son monde à elle pas dans l'autre plan. »

Donc un projet À PART : il ne dépend PAS de MAISON-18 (aucun bureau assis-debout) et part de la maison telle qu'elle est
aujourd'hui : copie de la base R0 (releve/livrables/donnees/maison.json) + relevé photo RDC-01 (base_rdc01_modifs.py, copie
telle quelle de renovation/RDC-01_etat_actuel/modifs.py). On ne garde que le rez-de-chaussée, et du rez-de-chaussée que la
chambre avant (piece-RDC-CH2) et sa garde-robe (piece-RDC-GRA) : les murs qui les bordent sont coupés à leur contour (leur
épaisseur reste), le reste de la maison (autres pièces, sous-sol, extérieur) est retiré. Repères : geometrie.py.

Le générateur de plans (releve/livrables/outils/generer_plans.py) n'est pas modifié : une maison à un seul niveau, des murs
courts et ses options habituelles (projet.affichage, niveau.feuille / nom / slug) suffisent ; l'échelle est la plus grande
qui tienne dans la feuille (1/4" = 1'-0").
"""
import copy
import importlib.util
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import geometrie as G  # noqa: E402

PHOTOS = "photos 01 à 12 du client (2026-11-09)"
SOURCE = "relevé photo CH-01 (" + PHOTOS + ")"

# murs gardés : id → nouvelles extrémités (axe) ; le reste du mur est hors de la pièce
MURS = {
    "mur-RDC-001": (5.0, 5.0, 143.25, 5.0),      # façade : prolongé par le plan jusqu'au nu droit de la cloison (148,25)
    "mur-RDC-004": (5.0, 5.0, 5.0, 139.25),      # mur gauche (mur vert) : jusqu'au nu arrière de la cloison de la SdB
    "mur-RDC-R01": (5.0, 142.0, 108.0, 142.0),   # cloison salle de bain / chambre (RDC-01)
    "mur-RDC-011": (108.0, 142.0, 108.0, 157.0),  # côté gauche du renfoncement de la porte
    "mur-RDC-012": (108.0, 157.0, 146.0, 157.0),  # mur de la porte de la chambre
    "mur-RDC-013": (146.0, 5.0, 146.0, 157.0),   # cloison chambre / garde-robe
    "mur-RDC-016": (146.0, 54.0, 175.0, 54.0),   # garde-robe : bout avant
    "mur-RDC-015": (146.0, 134.0, 175.0, 134.0),  # garde-robe : bout arrière
    "mur-RDC-014": (175.0, 54.0, 175.0, 134.0),  # garde-robe : fond
}
OUVERTURES = ("ouv-RDC-001", "ouv-RDC-014", "ouv-RDC-021")
PIECES = ("piece-RDC-CH2", "piece-RDC-GRA")


def _charger(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(ICI, fichier))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def dim(v, note=None, src="ESTIMÉ", photo=None):
    d = {"valeur": v, "source": src, "photo": photo}
    if note:
        d["note"] = note
    return d


def _element(eid, typ, nom, lib, x, y, rot, L, W, etat, src, note):
    e = {"id": eid, "type": typ, "nom": nom, "nom_original": None, "etat": etat,
         "position": {"x": round(x, 2), "y": round(y, 2), "rotation_deg": rot, "source": src},
         "dimensions": {"longueur": dim(L, None, src), "largeur": dim(W, None, src)}, "note": note}
    if lib is not None:
        e["libelle"] = lib
    return e


def _centre(b):
    return (b[0] + b[2]) / 2, (b[1] + b[3]) / 2


def elements():
    """Éléments du plan : l'existant gardé (ESTIMÉ sur les photos) et le coin jeu (PROPOSÉ)."""
    ex = "existant, " + SOURCE + " : position et dimensions estimées, à mesurer"
    pr = "coin jeu proposé (CH-01) : voir DESIGN.md"
    L = G.LITS
    out = [
        _element("elem-CH-LITS", "autre", "Lits superposés existants, simple sur simple (≈ 81 × 43 × 63 po), panneaux blancs, "
                 "montants de bois naturel ; tête au mur vert", "LITS SUPERPOSÉS", *_centre(L), 180, L[2] - L[0], L[3] - L[1],
                 "existant", "ESTIMÉ", ex),
        _element("elem-CH-ECH", "autre", "Échelle de bois inclinée des lits superposés", "", (G.ECHELLE[0] + G.ECHELLE[1]) / 2,
                 (G.ECHELLE[2] + L[1]) / 2, 0, G.ECHELLE[1] - G.ECHELLE[0], L[1] - G.ECHELLE[2], "existant", "ESTIMÉ", ex),
        _element("elem-CH-COMM", "autre", "Commode blanche basse existante (≈ 48 × 16 × 27 po), 3 rangs de tiroirs", "COMMODE",
                 *_centre(G.COMMODE), 90, G.COMMODE[3] - G.COMMODE[1], G.COMMODE[2] - G.COMMODE[0], "existant", "ESTIMÉ",
                 ex + " ; à ancrer au mur (anti-basculement)"),
        _element("elem-CH-PC1", "autre", "Plinthe chauffante électrique sous la fenêtre (≈ 96 po)", "PLINTHES CHAUFFANTES",
                 *_centre(G.PC_AVANT), 0, G.PC_AVANT[2] - G.PC_AVANT[0], G.PC_AVANT[3] - G.PC_AVANT[1], "existant", "ESTIMÉ", ex),
        _element("elem-CH-PC2", "autre", "Plinthe chauffante électrique au mur vert (≈ 72 po)", "",
                 *_centre(G.PC_GAUCHE), 270, G.PC_GAUCHE[3] - G.PC_GAUCHE[1], G.PC_GAUCHE[2] - G.PC_GAUCHE[0], "existant",
                 "ESTIMÉ", ex),
        # --- coin jeu (proposé)
        _element("elem-CH-P-TABLE", "comptoir", "Table à Lego en chêne 30 × 24 po, dessus à 20 po, rebord de ¾ po et deux bacs "
                 "de tri encastrés ; à environ 1 pi des plinthes chauffantes (à valider)", "TABLE LEGO", *_centre(G.TABLE), 0,
                 G.TABLE[2] - G.TABLE[0], G.TABLE[3] - G.TABLE[1], "nouveau", "PROPOSÉ", pr),
        _element("elem-CH-P-TAB1", "autre", "Tabouret d'enfant en chêne (assise à 12 po)", "", *G.TABOURETS[0], 0, 12, 12,
                 "nouveau", "PROPOSÉ", pr),
        _element("elem-CH-P-TAB2", "autre", "Tabouret d'enfant en chêne (assise à 12 po)", "", *G.TABOURETS[1], 0, 12, 12,
                 "nouveau", "PROPOSÉ", pr),
        _element("elem-CH-P-LIVRES", "trappe", "Deux rebords à livres de face en chêne (48 × 4 po) au-dessus de la commode, "
                 "à 34 et 45½ po", "LIVRES DE FACE (AU MUR)", G.REBORDS[0] + (G.REBORDS[1] - G.REBORDS[0]) / 2,
                 sum(G.REBORDS_Y) / 2, 90, G.REBORDS_Y[1] - G.REBORDS_Y[0], G.REBORDS[1] - G.REBORDS[0], "nouveau", "PROPOSÉ", pr),
        _element("elem-CH-P-TOUR", "autre", "Tour de 3 bacs étiquetés en chêne (17½ × 15 × 39 po), ancrée au mur", "BACS",
                 *_centre(G.TOUR), 180, G.TOUR[2] - G.TOUR[0], G.TOUR[3] - G.TOUR[1], "nouveau", "PROPOSÉ", pr),
        _element("elem-CH-P-GR1", "autre", "Garde-robe : étagère de 6 bacs étiquetés, 6 tiroirs à Lego triés et tablette des "
                 "constructions (28 × 16 po)", "BACS ET LEGO", *_centre(G.GR_ETAGERE), 90,
                 G.GR_ETAGERE[3] - G.GR_ETAGERE[1], G.GR_ETAGERE[2] - G.GR_ETAGERE[0], "nouveau", "PROPOSÉ", pr),
    ]
    return out


def lignes_cote():
    def lc(i, p1, p2, d, fac, rang, src="DÉDUIT", ref=None, va=None):
        return {"id": f"lc-CH-{i:03d}", "p1": list(p1), "p2": list(p2), "direction": d, "facade": fac, "rang": rang,
                "source": src, "statut": "confirmee", "ref": ref, "valeur_attendue": va, "repere": None}
    return [
        # façade avant : intérieur de la chambre et fenêtre (6'-3" LU)
        lc(1, (G.XG, 0), (G.FEN[0], 0), "x", "avant", 1),
        lc(2, (G.FEN[0], 0), (G.FEN[1], 0), "x", "avant", 1, "LU", "cote-RDC-014", 75.0),
        lc(3, (G.FEN[1], 0), (G.XD, 0), "x", "avant", 1),
        lc(4, (G.XG, 0), (G.XD, 0), "x", "avant", 3),
        # mur gauche : profondeur intérieure de la chambre
        lc(5, (0, G.YF), (0, G.YA), "y", "gauche", 3),
        # mur arrière : mur des lits et renfoncement de la porte
        lc(6, (G.XG, 160), (G.NICHE[0], 160), "x", "arriere", 1),
        lc(7, (G.NICHE[0], 160), (G.NICHE[2], 160), "x", "arriere", 1),
        lc(8, (G.XG, 160), (G.NICHE[2], 160), "x", "arriere", 3),
        # garde-robe : longueur intérieure (ESTIMÉ au plan R0) et porte
        lc(9, (180, G.GR[1]), (180, G.PORTE_GR[0]), "y", "droite", 1, "ESTIMÉ"),
        lc(10, (180, G.PORTE_GR[0]), (180, G.PORTE_GR[1]), "y", "droite", 1, "LU", "cote-RDC-061", 30.0),
        lc(11, (180, G.PORTE_GR[1]), (180, G.GR[3]), "y", "droite", 1, "ESTIMÉ"),
        lc(12, (180, G.GR[1]), (180, G.GR[3]), "y", "droite", 3, "ESTIMÉ"),
    ]


NOTES = (
    "Relevé photo du 2026-11-09 (12 photos) sur le relevé RDC-01 : la chambre seule ; tout est ESTIMÉ, à mesurer au ruban.",
    "Gardés : lits superposés et commode blanche, à leur place. Enlevés : fauteuil, petite table et chaises, présentoir, "
    "tablettes de jeux, toise, jouets.",
    "Coin jeu proposé : table à Lego de chêne sous les enseignes, livres de face au-dessus de la commode, tour de bacs à la porte.",
    "Garde-robe aménagée : bacs étiquetés, tiroirs à Lego triés et penderie à la hauteur des gars.",
    "Plinthes chauffantes : dégagement à valider avec le fabricant et un électricien ; meubles bas ancrés au mur.",
    "Fenêtre : 3 châssis, petits carreaux en haut, allège ≈ 37½ po, tête ≈ 80 po (vidéo DAG) ; plafond 96 po présumé.",
)


def appliquer(maison):
    maison = _charger("ch01_base_rdc01", "base_rdc01_modifs.py").appliquer(maison)
    rdc = copy.deepcopy(next(n for n in maison["niveaux"] if n["id"] == "RDC"))
    maison["niveaux"] = [rdc]                       # un seul niveau : la chambre dans son monde à elle
    maison["ecarts"] = []
    p = maison["projet"]
    p.update({"proposition": "CH-01", "revision": "A", "date": "2026-11-09", "titre_notes": "NOTES",
              "mention": "CHAMBRE DES GARÇONS — ÉTAT ACTUEL ET COIN JEU PROPOSÉ",
              "nom_pdf": "CH-01_chambre_garcons.pdf",
              "base": "copie de releve/livrables/donnees/maison.json (plans de base R0, commit 59ac401) + relevé RDC-01"})
    p["affichage"] = dict(p.get("affichage") or {}, noms_pieces=True, dimensions_pieces=True, metrique=False,
                          textes_structure=False)
    p.pop("implantation", None)                     # plan d'implantation du lot : hors de la chambre

    rdc.update({"feuille": "P-131", "nom": "Rez-de-chaussée", "slug": "chambre-garcons",
                "photos_sources": ["photos 01 à 12 du 2026-11-09"],
                "usage": "chambre des deux garçons (4 et 6 ans) ; plan CH-01 : la pièce seule, état actuel et coin jeu proposé",
                "hauteur_plafond": dim(G.PLAFOND, "PRÉSUMÉ (8 pi), comme RDC-01 ; à mesurer", "PRÉSUMÉ")})
    for k in ("murs_retires", "ouvertures_retirees", "elements_retires", "structure_retiree", "notes_retirees", "limites_zones"):
        rdc[k] = []
    rdc["elements_electriques_non_reportes"] = [x for x in rdc.get("elements_electriques_non_reportes") or []
                                                if "chambre avant" in x]

    # murs coupés au contour de la chambre et de sa garde-robe
    murs = {m["id"]: m for m in rdc["murs"]}
    rdc["murs"] = []
    for mid, (x1, y1, x2, y2) in MURS.items():
        m = murs[mid]
        m.update({"x1": x1, "y1": y1, "x2": x2, "y2": y2})
        m["note"] = (m.get("note") or "") + " — CH-01 : coupé au contour de la chambre et de sa garde-robe (le reste du mur est hors du plan)."
        rdc["murs"].append(m)

    # ouvertures : fenêtre de façade, porte de la chambre, porte de la garde-robe (les autres sont hors du plan)
    ouvs = {o["id"]: o for o in rdc["ouvertures"]}
    rdc["ouvertures"] = [ouvs[i] for i in OUVERTURES]
    f = ouvs["ouv-RDC-001"]
    f["allege"] = dim(G.ALLEGE, "vidéo DAG (MAISON-18, fenetres_video.py), depuis le plancher ; à mesurer", "ESTIMÉ")
    f["hauteur"] = dim(G.TETE - G.ALLEGE, f"allège {G.ALLEGE} → tête {G.TETE} po (vidéo DAG) ; à mesurer", "ESTIMÉ")
    f["note"] = ("chambre avant : 3 châssis égaux en PVC blanc (manivelle sur celui de droite vu de l'intérieur), bande de "
                 "petits carreaux (2 rangs × 3 colonnes) en haut de chaque châssis, chambranle plat de pin teint à coins "
                 "d'onglet, deux caissons noirs de stores enrouleurs au-dessus (" + SOURCE + ")")
    for oid in ("ouv-RDC-014", "ouv-RDC-021"):
        ouvs[oid]["note"] = (ouvs[oid].get("note") or "") + (" ; porte de pin teint à panneaux horizontaux, bouton rond et "
                                                             "pentures noirs (" + SOURCE + ")")
    ouvs["ouv-RDC-014"]["source_position"] = "PHOTO"     # charnière côté x = 142 (photo 11), ouvre dans la chambre

    # pièces : la chambre et sa garde-robe
    pcs = {q["id"]: q for q in rdc["pieces"]}
    ch, gr = pcs["piece-RDC-CH2"], pcs["piece-RDC-GRA"]
    ch["nom"] = "Chambre des garçons"
    ch["description"] = "Chambre des deux garçons (4 et 6 ans) : lits superposés et commode gardés, coin jeu proposé."
    gr["description"] = "Garde-robe de la chambre des garçons, aménagée (bacs, tiroirs à Lego, penderie basse)."
    rdc["pieces"] = [ch, gr]

    rdc["structure"] = []        # colonne C04 et poutre de l'axe B : dans les cloisons, hors de la pièce (voir DESIGN.md)
    rdc["elements"] = elements()
    lcs = lignes_cote()
    rdc["lignes_cote"] = lcs
    refs = {q["ref"] for q in lcs if q.get("ref")}
    rdc["cotes"] = [c for c in rdc.get("cotes") or [] if c.get("id") in refs]
    rdc["notes"] = [{"id": f"note-CH-{i + 1:02d}", "texte_original": None, "photo": None, "interpretation": t}
                    for i, t in enumerate(NOTES)]
    return maison
