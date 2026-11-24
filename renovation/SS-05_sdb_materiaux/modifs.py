"""SS-05 — Salle de bain revue, matériaux réels (copie de SS-04, revue avec le skill designer-interieur).

Demandes du propriétaire (2026-10-29) : la toilette contre le mur, sans tenir compte du drain existant ; le bain placé
comme il faut ; de plus beaux matériaux dans la maquette.

Ce qui change par rapport à SS-04 (tout le reste est identique) :
- Bain de 60 × 30 en coin, contre le mur de fondation et la cloison de la salle de lavage, sous la fenêtre (le mur
  partagé avec la salle de lavage porte la plomberie).
- Douche walk-in de 72 × 36 à côté du bain, derrière un muret carrelé surmonté de verre ; panneau vitré fixe à l'avant.
- Toilette au plancher, dos contre la cloison de la chambre 1, dans le coin ; 15 po et plus de chaque côté de l'axe,
  36 po libres devant. Le drain existant est ignoré : drain de toilette à refaire (tranchée dans la dalle).
- Armoire à serviettes en chêne contre la même cloison.
Coordonnées en pouces, repère de la maison. Murs à l'axe.
"""
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import polygonize, unary_union
from shapely.geometry.polygon import orient

T = 4.5
DATE = "2026-10-29"
SOURCE = "proposition SS-05 (esquisse)"


def dim(v, note=None, src="PRÉSUMÉ"):
    d = {"valeur": v, "source": src, "photo": None}
    if note:
        d["note"] = note
    return d


MURS = [  # id, x1, y1, x2, y2, rôle (« VERRE » = cloison vitrée, « LATTES » = claustra de bois)
    ("mur-SS-P01", 10, 157, 146, 157, "salle de lavage / salle de bain (axe de la poutre avant)"),
    ("mur-SS-P10", 146, 157, 228, 157, "VERRE : salle d'entraînement / corridor (axe de la poutre avant)"),
    ("mur-SS-P09", 228, 10, 228, 157, "VERRE : salle d'entraînement / séjour"),
    ("mur-SS-P08", 112, 10, 112, 157, "salle de lavage / salle d'entraînement"),
    ("mur-SS-P04", 146, 157, 146, 204, "salle de bain / corridor"),
    ("mur-SS-P02", 146, 204, 228, 204, "alcôve de la vanité / corridor (axe de la poutre arrière)"),
    ("mur-SS-P05", 10, 250, 228, 250, "salle de bain / chambre 1"),
    ("mur-SS-P06", 228, 204, 228, 370, "salle de bain et chambre 1 / passage"),
    ("mur-SS-P11", 316.25, 230, 446, 230, "coin bar / chambre 2"),
    ("mur-SS-P07", 316.25, 230, 316.25, 370, "escalier et passage / chambre 2"),
    ("mur-SS-P12", 38.25, 280, 38.25, 370, "garde-robe / chambre 1"),
    ("mur-SS-P13", 10, 280, 38.25, 280, "garde-robe / chambre 1"),
    ("mur-SS-P14", 384, 258.25, 446, 258.25, "garde-robe / chambre 2"),
    ("mur-SS-P15", 384, 230, 384, 258.25, "garde-robe / chambre 2"),
    ("mur-SS-P16", 277, 207.25, 277, 329, "LATTES : garde de l'escalier / passage"),
]

PORTES = [  # id, mur, centre, largeur, ouvre_vers, rôle, opération, matériau, charnière (None = début du mur)
    ("ouv-SS-P01", "mur-SS-P10", 168.0, 32, "droite", "porte vitrée de la salle d'entraînement", "battante", "verre", "fin"),
    ("ouv-SS-P02", "mur-SS-P08", 135.0, 30, "gauche", "porte de la salle de lavage", "battante", None, "fin"),
    ("ouv-SS-P03", "mur-SS-P02", 187.0, 30, "gauche", "porte coulissante de la salle de bain", "coulissante", None, None),
    ("ouv-SS-P05", "mur-SS-P06", 300.0, 32, "gauche", "porte de la chambre 1", "battante", None, None),
    ("ouv-SS-P06", "mur-SS-P11", 338.0, 32, "gauche", "porte de la chambre 2", "battante", None, None),
    ("ouv-SS-P07", "mur-SS-P12", 325.0, 60, "droite", "portes coulissantes de la garde-robe (chambre 1)", "coulissante", None, None),
    ("ouv-SS-P08", "mur-SS-P14", 415.0, 48, "gauche", "portes coulissantes de la garde-robe (chambre 2)", "coulissante", None, None),
]

PIECES = [  # id, nom, point dans la pièce
    ("piece-SS-LAVAGE", "Salle de lavage", (50, 80)),
    ("piece-SS-GYM", "Salle d'entraînement", (170, 80)),
    ("piece-SS-SALON", "Séjour", (340, 80)),
    ("piece-SS-BAR", "Coin bar", (390, 190)),
    ("piece-SS-CORR", "Corridor", (190, 180)),
    ("piece-SS-SDB", "Salle de bain", (80, 200)),
    ("piece-SS-CH1", "Chambre 1", (130, 320)),
    ("piece-SS-GR1", "G.-R.", (24, 320)),
    ("piece-SS-PASS", "Passage", (252, 300)),
    ("piece-SS-ESC", "Escalier", (296, 280)),
    ("piece-SS-CH2", "Chambre 2", (380, 320)),
    ("piece-SS-GR2", "G.-R.", (415, 244)),
]
COUPES = [  # limites sans mur (prolongées jusqu'aux murs ; l'excédent est coupé par la région)
    ((226, 157), (452, 157)),   # séjour / coin bar
    ((228, 155), (228, 206)),   # corridor / coin bar
    ((226, 230), (279, 230)),   # coin bar / passage
    ((275, 207.25), (318, 207.25)),   # pied de l'escalier
    ((314, 205), (314, 232)),   # côté droit des premières marches
    ((275, 329), (318, 329)),   # palier du haut (le dessous devient une niche du passage)
]

# Escalier : emplacement, nombre de contremarches et course de 1957 (elem-SS-ESC, P2) — reconstruit au même endroit.
ESCALIER = {"id": "elem-SS-P-ESC", "x": 296.0, "y": 268.1, "L": 121.7, "W": 37}

EQUIPEMENTS = [  # id, type, nom, libellé, x, y, rotation, (longueur, largeur)
    ("elem-SS-P-CE", "chauffe-eau", "Chauffe-eau", None, 34, 138, 0, (22, 22)),
    ("elem-SS-P-PLIAGE", "comptoir", "Comptoir de pliage (au-dessus de la laveuse et de la sécheuse)", None, 59.9, 23, 0, (99.75, 26)),
    ("elem-SS-P-LAV", "laveuse", "Laveuse frontale", None, 25.5, 23.5, 0, (27, 27)),
    ("elem-SS-P-SEC", "secheuse", "Sécheuse frontale", None, 54.5, 23.5, 0, (27, 27)),
    ("elem-SS-P-BAC", "bac-lavage", "Bac de lavage", None, 86, 22, 0, (24, 20)),
    ("elem-SS-P-ARM", "armoires", "Colonne de rangement (balai, produits, paniers)", None, 97.75, 78, 90, (68, 24)),
    ("elem-SS-P-BAIN", "baignoire", "Baignoire", None, 40.25, 174.25, 0, (60, 30)),
    ("elem-SS-P-DOUCHE", "autre", "Douche", "DOUCHE", 107.9, 177.25, 0, (71.75, 36)),
    ("elem-SS-P-WC", "toilette", "Toilette", None, 40, 233.75, 180, (20, 28)),
    ("elem-SS-P-SERV", "armoires", "Armoire à serviettes", None, 119, 240.75, 180, (30, 14)),
    ("elem-SS-P-VAN", "comptoir", "Double vanité", None, 187, 236.75, 180, (72, 22)),
    ("elem-SS-P-LAVABO1", "lavabo", "Lavabo", None, 169, 237, 180, (18, 14)),
    ("elem-SS-P-LAVABO2", "lavabo", "Lavabo", None, 205, 237, 180, (18, 14)),
    ("elem-SS-P-BARC", "comptoir", "Comptoir du coin bar", None, 386, 218, 180, (56, 24)),
    ("elem-SS-P-EVBAR", "evier", "Lavabo de bar", None, 378, 218.5, 180, (16, 15)),
    ("elem-SS-P-REF", "refrigerateur", "Réfrigérateur", None, 429.5, 215, 180, (30, 30)),
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
    p.update({"proposition": "SS-05", "revision": "A", "date": DATE, "titre_notes": "NOTES DE LA PROPOSITION",
              "mention": "PROPOSITION SS-05 — SALLE DE BAIN REVUE, MATÉRIAUX — ESQUISSE À VALIDER",
              "nom_pdf": "SS-05_sdb_materiaux.pdf",
              "base": "copie de releve/livrables/donnees/maison.json (plans de base R0, commit 59ac401)"})
    p["affichage"] = dict(p.get("affichage") or {}, noms_pieces=True, dimensions_pieces=True)
    ss = next(n for n in maison["niveaux"] if n["id"] == "SS")
    maison["niveaux"] = [ss]
    maison["ecarts"] = []
    ss["feuille"] = "P-104"
    ss["nom"] = "Sous-sol proposé"

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
                       "hauteur_plafond": {"valeur": None, "source": "ILLISIBLE", "photo": None},
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
    esc = {"id": ESCALIER["id"], "type": "escalier", "nom": "Escalier vers le rez-de-chaussée (reconstruit)", "nom_original": None,
           "etat": "nouveau", "position": {"x": ESCALIER["x"], "y": ESCALIER["y"], "rotation_deg": 0, "source": "ESTIMÉ"},
           "dimensions": {"longueur": dict(vieux["dimensions"]["longueur"]), "largeur": dict(vieux["dimensions"]["largeur"])},
           "escalier": {"nb_contremarches": dict(vieux["escalier"]["nb_contremarches"]), "fleche": "MONTE", "direction": "+y"},
           "note": "Volée droite reconstruite à l'emplacement de 1957 (elem-SS-ESC de la base, P2), décalée de 2,8 po vers "
                   "l'est pour s'aligner sur la cloison de la chambre 2 ; giron, hauteur de marche, échappée et trémie à "
                   "valider (hauteur plancher-plancher non mesurée) — " + SOURCE}
    assert abs(esc["dimensions"]["longueur"]["valeur"] - ESCALIER["L"]) < 0.01 and esc["dimensions"]["largeur"]["valeur"] == ESCALIER["W"]
    ss["elements"].append(esc)
    ss["elements"].sort(key=lambda e: e["id"])
    notes = [
        "Esquisse : cloisons, portes, escalier, bar et appareils projetés ; le reste est l'existant (base R0).",
        "Escalier de 14 c.m. à l'emplacement de 1957 : trémie à rouvrir au rez-de-chaussée ; giron et échappée à valider.",
        "Salle de bain : toilette et bain déplacés, drains existants ignorés (tranchée dans la dalle).",
        "Coin bar : lavabo de bar à ~9 pi du drain de la chambre 2 (raccord à prévoir).",
        "Salle de lavage : panneau et chauffe-eau en place, 36 po libres devant le panneau.",
        "Évacuation des chambres, hauteur sous poutres, coupe-feu à valider.",
    ]
    ss["notes"] = [{"id": f"note-SS-P{i + 1:02d}", "texte_original": None, "photo": None, "interpretation": t} for i, t in enumerate(notes)]
    ss["lignes_cote"] = [l for l in ss["lignes_cote"] if l.get("facade") != "int"]
    return maison
