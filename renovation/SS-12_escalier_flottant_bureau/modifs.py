"""SS-12 — Escalier flottant, séjour épuré, bureau commun entre les chambres (copie de SS-11, revue avec le skill
designer-interieur).

Demandes du propriétaire (2026-10-30) :
- le séjour du bas « tourné de bord », sans petit frigo ni coin lecture : un sofa et une télé, on garde l'espace ;
- un escalier « qui tient tout seul », en métal ou en béton, à travers lequel on voit le gym : limon central en acier
  noir, marches de chêne épaisses sans contremarches ; le mur plein côté séjour devient une garde vitrée pleine hauteur ;
- entre les deux chambres, là où est le caveau : rétrécir un peu la chambre de gauche et faire une zone commune pour
  travailler (bureau, ordinateur, petite bibliothèque) qui communique avec les deux chambres.
Le rez-de-chaussée est celui de SS-11. Pouces, repère de la maison.
"""
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import polygonize, unary_union
from shapely.geometry.polygon import orient

T = 4.5
DATE = "2026-10-29"
SOURCE = "proposition SS-12 (esquisse)"
# Hauteur du sous-sol donnée par le propriétaire le 2026-10-29 (« 8 pi en bas ») : plancher au plafond actuel.
HAUTEUR_SS = {"valeur": 96, "source": "MESURÉ", "photo": None,
              "note": "8 pi, plancher du sous-sol au plafond, donné par le propriétaire (2026-10-29) ; sous les poutres : moins"}


def dim(v, note=None, src="PRÉSUMÉ"):
    d = {"valeur": v, "source": src, "photo": None}
    if note:
        d["note"] = note
    return d


MURS = [  # id, x1, y1, x2, y2, rôle (« VERRE » = cloison vitrée, « LATTES » = claustra de bois)
    ("mur-SS-P01", 10, 157, 146, 157, "salle de lavage / salle de bain (axe de la poutre avant)"),
    ("mur-SS-P10", 146, 157, 228, 157, "VERRE : salle d'entraînement / hall (axe de la poutre avant)"),
    ("mur-SS-P09", 228, 10, 228, 157, "VERRE : salle d'entraînement / escalier"),
    ("mur-SS-P08", 112, 10, 112, 157, "salle de lavage / salle d'entraînement"),
    ("mur-SS-P18", 272.25, 10, 272.25, 150, "VERRE : garde vitrée pleine hauteur de l'escalier / séjour"),
    ("mur-SS-P04", 142, 157, 142, 250, "salle de bain / hall"),
    ("mur-SS-P05", 10, 250, 198.75, 250, "salle de bain / chambre 1"),
    ("mur-SS-P06", 198.75, 250, 198.75, 370, "chambre 1 / bureau commun (à l'est de la fenêtre de la chambre)"),
    ("mur-SS-P07", 300, 230, 300, 370, "bureau commun / chambre 2"),
    ("mur-SS-P11", 300, 230, 446, 230, "vestiaire / chambre 2"),
    ("mur-SS-P12", 38.25, 280, 38.25, 370, "garde-robe / chambre 1"),
    ("mur-SS-P13", 10, 280, 38.25, 280, "garde-robe / chambre 1"),
    ("mur-SS-P14", 384, 258.25, 446, 258.25, "garde-robe / chambre 2"),
    ("mur-SS-P15", 384, 230, 384, 258.25, "garde-robe / chambre 2"),
]

PORTES = [  # id, mur, centre, largeur, ouvre_vers, rôle, opération, matériau, charnière (None = début du mur)
    ("ouv-SS-P01", "mur-SS-P10", 168.0, 32, "droite", "porte vitrée de la salle d'entraînement", "battante", "verre", "fin"),
    ("ouv-SS-P02", "mur-SS-P08", 135.0, 30, "gauche", "porte de la salle de lavage", "battante", None, "fin"),
    ("ouv-SS-P03", "mur-SS-P04", 220.0, 30, "gauche", "porte coulissante dans le mur de la salle de bain", "coulissante", None, None),
    ("ouv-SS-P05", "mur-SS-P06", 268.0, 30, "gauche", "porte de la chambre 1 (depuis le bureau commun)", "battante", None, "fin"),
    ("ouv-SS-P06", "mur-SS-P07", 252.0, 32, "droite", "porte de la chambre 2", "battante", None, None),
    ("ouv-SS-P07", "mur-SS-P12", 325.0, 60, "droite", "portes coulissantes de la garde-robe (chambre 1)", "coulissante", None, None),
    ("ouv-SS-P08", "mur-SS-P14", 415.0, 48, "gauche", "portes coulissantes de la garde-robe (chambre 2)", "coulissante", None, None),
]

PIECES = [  # id, nom, point dans la pièce
    ("piece-SS-LAVAGE", "Salle de lavage", (50, 80)),
    ("piece-SS-GYM", "Salle d'entraînement", (170, 80)),
    ("piece-SS-ESC", "Escalier", (252, 100)),
    ("piece-SS-SALON", "Séjour", (360, 80)),
    ("piece-SS-VEST", "Vestiaire", (390, 190)),
    ("piece-SS-HALL", "Hall", (195, 190)),
    ("piece-SS-SDB", "Salle de bain", (60, 215)),
    ("piece-SS-CH1", "Chambre 1", (100, 320)),
    ("piece-SS-GR1", "G.-R.", (24, 320)),
    ("piece-SS-BUREAU", "Bureau commun", (250, 300)),
    ("piece-SS-CH2", "Chambre 2", (380, 320)),
    ("piece-SS-GR2", "G.-R.", (415, 244)),
]
COUPES = [  # limites sans mur (prolongées jusqu'aux murs ; l'excédent est coupé par la région)
    ((272.25, 148), (272.25, 157), (452, 157)),   # séjour / vestiaire (depuis le bout du mur télé)
    ((226, 150), (274, 150)),   # pied de l'escalier
    ((228, 148), (228, 231)),   # hall / vestiaire
    ((196, 230), (302, 230)),   # hall et vestiaire / bureau commun
    ((198.75, 228), (198.75, 252)),   # recoin du hall (porte de la salle de bain) / bureau commun
]

# Escalier : option 2 (entrée avant) ; volée droite qui monte vers l'avant, 3 marches tournantes en haut, sortie à l'ouest
ESCALIER = {"x": 252.0, "y": 82.0, "L": 136.0, "W": 36.0,
            "tournant": {"nb": 3, "carre": [234, 14, 270, 50], "pivot": [234, 50]}, "style": "flottant"}

EQUIPEMENTS = [  # id, type, nom, libellé, x, y, rotation, (longueur, largeur)
    ("elem-SS-P-CE", "chauffe-eau", "Chauffe-eau", None, 34, 138, 0, (22, 22)),
    ("elem-SS-P-PLIAGE", "comptoir", "Comptoir de pliage (au-dessus de la laveuse et de la sécheuse)", None, 59.9, 23, 0, (99.75, 26)),
    ("elem-SS-P-LAV", "laveuse", "Laveuse frontale", None, 25.5, 23.5, 0, (27, 27)),
    ("elem-SS-P-SEC", "secheuse", "Sécheuse frontale", None, 54.5, 23.5, 0, (27, 27)),
    ("elem-SS-P-BAC", "bac-lavage", "Bac de lavage", None, 86, 22, 0, (24, 20)),
    ("elem-SS-P-ARM", "armoires", "Colonne de rangement (balai, produits, paniers)", None, 97.75, 78, 90, (68, 24)),
    ("elem-SS-P-BAIN", "baignoire", "Bain autoportant (sur pied)", None, 32, 199, 90, (66, 32)),
    ("elem-SS-P-DOUCHE", "autre", "Douche", "DOUCHE", 109.9, 177.1, 0, (59.75, 35.75)),
    ("elem-SS-P-WC", "toilette", "Toilette", None, 63, 233.75, 180, (20, 28)),
    ("elem-SS-P-VAN", "comptoir", "Double vanité de 60 po", None, 109, 236.9, 180, (60, 21.75)),
    ("elem-SS-P-LAVABO1", "lavabo", "Lavabo", None, 94, 237, 180, (18, 14)),
    ("elem-SS-P-LAVABO2", "lavabo", "Lavabo", None, 124, 237, 180, (18, 14)),
    ("elem-SS-P-BANC", "armoires", "Vestiaire ouvert : banc, cases à souliers, crochets, tablette", None, 368, 218.75, 180, (68, 18)),
    ("elem-SS-P-MANT", "armoires", "Armoire à manteaux", None, 424, 215.75, 180, (40, 24)),
    ("elem-SS-P-POSTES", "comptoir", "Bureau à deux postes (ordinateurs)", None, 284.75, 310, 90, (80, 26)),
    ("elem-SS-P-BIBLIO", "armoires", "Petite bibliothèque", None, 207.5, 328, 90, (76, 12)),
]


def _mur(mid, x1, y1, x2, y2, role):
    verre = role.startswith("VERRE")
    lattes = role.startswith("LATTES")
    m = {"id": mid, "type": "int", "etat": "nouveau", "porteur": "non", "indices_porteur": [],
         "epaisseur": dim(2.0 if verre or lattes else T, "cloison vitrée, cadre d'aluminium noir" if verre else
                          "claustra de lattes de chêne 1x2 espacées, plancher au plafond" if lattes else "cloison projetée 2x4 + gypse"),
         "x1": x1, "y1": y1, "x2": x2, "y2": y2,
         "source_position": "PRÉSUMÉ", "note": f"Cloison projetée — {role} ({SOURCE})."}
    if verre:
        m["materiau"] = "verre"
    if lattes:
        m["materiau"] = "lattes"
    return m


def _porte(oid, mur, centre, larg, vers, role, op, mat, charn):
    horiz = mur["y1"] == mur["y2"]
    a = mur["x1"] if horiz else mur["y1"]
    b = mur["x2"] if horiz else mur["y2"]
    o = {"id": oid, "type": "porte", "operation": op, "mur_id": mur["id"], "etat": "nouveau",
         "position": dim(round(abs(centre - a), 2)), "largeur": dim(larg), "hauteur": dim(80),
         "allege": {"valeur": None, "source": "ILLISIBLE", "photo": None},
         "sens": {"charniere": charn or ("debut" if b > a else "fin"), "ouvre_vers": vers}, "note": f"{role} ({SOURCE})"}
    if mat:
        o["materiau"] = mat
    return o


def appliquer(maison):
    p = maison["projet"]
    p.update({"proposition": "SS-12", "revision": "A", "date": DATE, "titre_notes": "NOTES DE LA PROPOSITION",
              "mention": "PROPOSITION SS-12 — ESCALIER FLOTTANT, BUREAU COMMUN — ESQUISSE À VALIDER",
              "nom_pdf": "SS-12_escalier_flottant_bureau.pdf",
              "base": "copie de releve/livrables/donnees/maison.json (plans de base R0, commit 59ac401)"})
    p["affichage"] = dict(p.get("affichage") or {}, noms_pieces=True, dimensions_pieces=True)
    ss = next(n for n in maison["niveaux"] if n["id"] == "SS")
    rdc = next(n for n in maison["niveaux"] if n["id"] == "RDC")
    maison["ecarts"] = []
    ss["feuille"], ss["nom"] = "P-117", "Sous-sol proposé"
    rdc["feuille"], rdc["nom"] = "P-118", "RDC proposé"

    murs = [_mur(*m) for m in MURS]
    ss["murs"] += murs
    par_id = {m["id"]: m for m in ss["murs"]}
    ss["ouvertures"] += [_porte(oid, par_id[mid], c, w, v, r, op, mt, ch) for oid, mid, c, w, v, r, op, mt, ch in PORTES]

    princ = next(x for x in ss["pieces"] if x["id"] == "piece-SS-PRINC")
    autres = [x for x in ss["pieces"] if x["id"] != "piece-SS-PRINC"]
    for x in autres:
        if x["id"] == "piece-SS-LEG":
            x["nom"] = "Rangement (caveau)"
            x["description"] = "Ancien caveau à légumes transformé en rangement fermé (étagères) — " + SOURCE
    zone = Polygon(princ["polygone"])
    emprises = unary_union([LineString([(m["x1"], m["y1"]), (m["x2"], m["y2"])]).buffer(m["epaisseur"]["valeur"] / 2, cap_style=3)
                            for m in murs])
    libre = zone.difference(emprises)
    morceaux = []
    for r in (libre.geoms if hasattr(libre, "geoms") else [libre]):
        coupe = [LineString(c).intersection(r) for c in COUPES if LineString(c).intersects(r)]
        morceaux += list(polygonize(unary_union([r.exterior] + list(r.interiors) + coupe))) if coupe else [r]
    pieces = []
    for pid, nom, seed in PIECES:
        hit = [m for m in morceaux if m.contains(Point(seed))]
        assert len(hit) == 1, (pid, len(hit))
        poly = orient(hit[0].simplify(0.01), 1.0)
        minx, miny, maxx, maxy = poly.bounds
        pieces.append({"id": pid, "nom": nom, "nom_original": None, "etat": "nouveau", "description": f"{nom} — {SOURCE}",
                       "polygone": [[round(x, 2), round(y, 2)] for x, y in list(poly.exterior.coords)[:-1]],
                       "superficie": dim(round(poly.area / 144, 1), "aire du polygone au nu des cloisons projetées", "DÉDUIT"),
                       "hauteur_plafond": dict(HAUTEUR_SS),
                       "dimensions": {"x": dim(round(maxx - minx, 2), None, "DÉDUIT"), "y": dim(round(maxy - miny, 2), None, "DÉDUIT")}})
    for x in pieces:
        if x["id"] == "piece-SS-ESC":
            x["etiquette"] = False
    ss["pieces"] = pieces + autres

    for eid, typ, nom, lib, x, y, rot, (L, W) in EQUIPEMENTS:
        e = {"id": eid, "type": typ, "nom": nom, "nom_original": None, "etat": "nouveau",
             "position": {"x": x, "y": y, "rotation_deg": rot, "source": "PRÉSUMÉ"},
             "dimensions": {"longueur": dim(L), "largeur": dim(W)}, "note": SOURCE}
        if lib:
            e["libelle"] = lib
        ss["elements"].append(e)
    vieux = next(e for e in ss.get("elements_retires", []) if e["id"] == "elem-SS-ESC")
    note_esc = ("Escalier à l'entrée avant (option 2 de l'étude 3, choisie par le propriétaire le 2026-10-30) : 14 "
                "contremarches, 3 tournantes en haut, sortie à l'ouest dans le vestibule d'entrée. Hauteur d'étage ≈ 105 po "
                "(8 pi au sous-sol, propriétaire) ; giron, échappée et trémie à valider — " + SOURCE)
    for niv, fl, dr in ((ss, "MONTE", "-y"), (rdc, "DESCEND", "+y")):
        niv["elements"].append({
            "id": f"elem-{niv['id']}-P-ESC", "type": "escalier",
            "nom": "Escalier entre le sous-sol et le rez-de-chaussée (projeté)", "nom_original": None, "etat": "nouveau",
            "position": {"x": ESCALIER["x"], "y": ESCALIER["y"], "rotation_deg": 0, "source": "PRÉSUMÉ"},
            "dimensions": {"longueur": dim(ESCALIER["L"], "10 girons droits de 10 po + 3 tournants"), "largeur": dim(ESCALIER["W"])},
            "escalier": {"nb_contremarches": dim(14, "même nombre que l'escalier de 1957 (P2)", "DÉDUIT"), "fleche": fl,
                         "direction": dr, "tournant": dict(ESCALIER["tournant"]), "style": ESCALIER["style"]},
            "note": note_esc})
        niv["elements"].sort(key=lambda e: e["id"])
    # rez-de-chaussée : garde le long de l'escalier côté salle à manger ; la porte de garde-robe qui donnait sur la bande
    # de l'escalier est enlevée (à refaire côté chambre)
    for x in rdc["pieces"]:
        x["etiquette"] = False          # comme A-101 : pas de noms de pièces au rez-de-chaussée (appartement existant)
    # rez-de-chaussée : cage fermée (côté salon, côté hall, bout), vestibule d'entrée commun, porte d'entrée inversée
    rdc["murs"] = [m for m in rdc["murs"] if m["id"] != "mur-RDC-018"]
    rdc["ouvertures"] = [o for o in rdc["ouvertures"] if o["mur_id"] != "mur-RDC-018"]
    rdc["murs"] += [_mur("mur-RDC-P01", 272.25, 10, 272.25, 152.25, "cage d'escalier / salon"),
                    _mur("mur-RDC-P02", 231.75, 50, 231.75, 152.25, "cage d'escalier / hall"),
                    _mur("mur-RDC-P03", 231.75, 152.25, 272.25, 152.25, "bout de la cage d'escalier"),
                    _mur("mur-RDC-P04", 222, 63, 231.75, 63, "vestibule d'entrée / hall (prolongement)")]
    for o in rdc["ouvertures"]:
        if o["id"] == "ouv-RDC-010":
            o["sens"] = dict(o.get("sens") or {}, charniere="debut",
                             note="sens inversé (pentures à gauche) pour dégager le haut de l'escalier — " + SOURCE)
    # salle de bain du haut : le mur côté chambre avant descend de 18 po (y 157 → 139) sur la largeur de la salle de bain
    murs = {m["id"]: m for m in rdc["murs"]}
    m12, m11 = murs["mur-RDC-012"], murs["mur-RDC-011"]
    dx = 108 - m12["x1"]
    m12["x1"] = 108                                       # le reste du mur (dégagement / chambre avant) reste en place
    m11["y1"] = 139                                       # la cloison salle de bain / dégagement descend aussi
    for o in rdc["ouvertures"]:
        if o["mur_id"] == "mur-RDC-012":
            o["position"] = dict(o["position"], valeur=round(o["position"]["valeur"] - dx, 2))
        if o["mur_id"] == "mur-RDC-011":
            o["position"] = dict(o["position"], valeur=round(o["position"]["valeur"] + 18, 2))
    rdc["murs"].append(_mur("mur-RDC-P05", 5, 139, 108, 139, "salle de bain / chambre avant (déplacé de 18 po vers l'avant)"))
    rdc["murs"][-1]["epaisseur"] = dict(m12["epaisseur"])
    from shapely.geometry import box
    for p in rdc["pieces"]:
        P = Polygon(p["polygone"])
        if p["id"] == "piece-RDC-SDB":
            P = P.union(box(10, 141.25, 105.75, 159.5))
        elif p["id"] == "piece-RDC-CH2":
            P = P.difference(box(0, 136.75, 110.25, 160))
        else:
            continue
        P = orient(P.simplify(0.01), 1.0)
        p["polygone"] = [[round(x, 2), round(y, 2)] for x, y in list(P.exterior.coords)[:-1]]
        p["superficie"] = dim(round(P.area / 144, 1), "aire recalculée après le déplacement du mur — " + SOURCE, "DÉDUIT")
        p["etat"] = "modifie"
        x0, y0, x1, y1 = P.bounds
        p["dimensions"] = {"x": dim(round(x1 - x0, 2), None, "DÉDUIT"), "y": dim(round(y1 - y0, 2), None, "DÉDUIT")}
    rdc["notes"] = [{"id": f"note-RDC-P{i + 1:02d}", "texte_original": None, "photo": None, "interpretation": t} for i, t in enumerate((
        "Escalier à l'entrée avant (option 2) : trémie d'environ 3 × 10 pi à ouvrir dans le plancher.",
        "Vestibule d'entrée commun : on descend au sous-sol ou on entre au logement du haut.",
        "Cloison entre l'entrée et le salon enlevée ; cage fermée côté salon et côté hall.",
        "Porte d'entrée : pentures à gauche (sens inversé) ; coupe-feu entre logements à valider.",
        "Salle de bain agrandie de 1½ pi vers la chambre avant (mur déplacé) ; plomberie à vérifier."))]
    for o in ss["ouvertures"]:
        if o["id"] == "ouv-SS-008":
            o["sens"] = dict(o.get("sens") or {}, charniere="fin",
                             note="pentures du côté ouest (le battant se range le long de la bibliothèque) — " + SOURCE)
    ss["elements"].sort(key=lambda e: e["id"])
    notes = [
        "Esquisse : cloisons, portes, escalier, bar et appareils projetés ; le reste est l'existant (base R0).",
        "Escalier de 14 c.m. à l'entrée avant (voir P-118) : trémie, giron et échappée à valider.",
        "Escalier flottant (limon central acier, marches de chêne) ; garde vitrée côté séjour.",
        "Salle de bain : bain autoportant et toilette déplacés, drains existants ignorés (tranchée).",
        "Bureau commun entre les chambres : 2 postes, bibliothèque ; accès au caveau.",
        "Hauteur du sous-sol : 8 pi (propriétaire) ; hauteur sous poutres et coupe-feu à valider.",
    ]
    ss["notes"] = [{"id": f"note-SS-P{i + 1:02d}", "texte_original": None, "photo": None, "interpretation": t} for i, t in enumerate(notes)]
    ss["lignes_cote"] = [l for l in ss["lignes_cote"] if l.get("facade") != "int"]
    return maison
