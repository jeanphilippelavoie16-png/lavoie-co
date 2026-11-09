"""SS-03 — Grande salle de bain à double vanité, cuisine, caveau en rangement (copie de SS-02, revue avec le skill
designer-interieur).

Demandes du propriétaire (2026-10-29) : une grande salle de bain avec double lavabo ; le caveau devient un rangement ;
la porte vitrée de la salle d'entraînement ; un coin cuisine (logement indépendant) ; « de quoi de nice, comme un pro ».

Ce qui change par rapport à SS-02 :
- Salle de bain en L de ~115 pi² : la garde-robe walk-in de la chambre 1 devient une alcôve à double vanité (72 po),
  fermée par une porte coulissante (l'arc d'une porte battante frapperait la vanité). Bain sous la fenêtre sur le drain
  existant, toilette murale devant un muret technique sur le drain existant, douche walk-in 60 × 36 vitrée.
- Cuisine en ligne de 10 pi au fond de l'aire ouverte : le mur de la chambre 2 recule de 26 po (axe à 19'-2") pour lui
  faire place ; évier à ~8 pi du drain existant (raccord à prévoir).
- Chambre 1 et chambre 2 : garde-robes à portes coulissantes.
- Caveau : rangement fermé (étagères), accessible par le passage.
- Salle d'entraînement : deux cloisons vitrées, porte vitrée à cadre noir.
- Salle d'utilité : panneau, chauffe-eau, laveuse et sécheuse.
Coordonnées en pouces, repère de la maison. Murs à l'axe.
"""
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import polygonize, unary_union
from shapely.geometry.polygon import orient

T = 4.5
DATE = "2026-10-29"
SOURCE = "proposition SS-03 (esquisse)"


def dim(v, note=None, src="PRÉSUMÉ"):
    d = {"valeur": v, "source": src, "photo": None}
    if note:
        d["note"] = note
    return d


MURS = [  # id, x1, y1, x2, y2, rôle (« VERRE » = cloison vitrée)
    ("mur-SS-P01", 10, 157, 146, 157, "utilité / salle de bain (axe de la poutre avant)"),
    ("mur-SS-P10", 146, 157, 228, 157, "VERRE : salle d'entraînement / corridor (axe de la poutre avant)"),
    ("mur-SS-P09", 228, 10, 228, 157, "VERRE : salle d'entraînement / séjour"),
    ("mur-SS-P08", 100, 10, 100, 157, "utilité / salle d'entraînement"),
    ("mur-SS-P04", 146, 157, 146, 204, "salle de bain / corridor"),
    ("mur-SS-P02", 146, 204, 228, 204, "alcôve de la vanité / corridor (axe de la poutre arrière)"),
    ("mur-SS-P05", 10, 250, 228, 250, "salle de bain / chambre 1"),
    ("mur-SS-P06", 228, 204, 228, 370, "salle de bain et chambre 1 / cuisine et passage"),
    ("mur-SS-P11", 300, 230, 446, 230, "cuisine / chambre 2"),
    ("mur-SS-P07", 300, 230, 300, 370, "passage / chambre 2"),
    ("mur-SS-P12", 38.25, 280, 38.25, 370, "garde-robe / chambre 1"),
    ("mur-SS-P13", 10, 280, 38.25, 280, "garde-robe / chambre 1"),
    ("mur-SS-P14", 384, 258.25, 446, 258.25, "garde-robe / chambre 2"),
    ("mur-SS-P15", 384, 230, 384, 258.25, "garde-robe / chambre 2"),
]

PORTES = [  # id, mur, centre, largeur, ouvre_vers, rôle, opération, matériau
    ("ouv-SS-P01", "mur-SS-P10", 190.0, 32, "droite", "porte vitrée de la salle d'entraînement", "battante", "verre"),
    ("ouv-SS-P02", "mur-SS-P08", 125.0, 30, "gauche", "porte de la salle d'utilité", "battante", None),
    ("ouv-SS-P03", "mur-SS-P02", 187.0, 30, "gauche", "porte coulissante de la salle de bain", "coulissante", None),
    ("ouv-SS-P05", "mur-SS-P06", 300.0, 32, "gauche", "porte de la chambre 1", "battante", None),
    ("ouv-SS-P06", "mur-SS-P07", 300.0, 32, "droite", "porte de la chambre 2", "battante", None),
    ("ouv-SS-P07", "mur-SS-P12", 325.0, 60, "droite", "portes coulissantes de la garde-robe (chambre 1)", "coulissante", None),
    ("ouv-SS-P08", "mur-SS-P14", 415.0, 48, "gauche", "portes coulissantes de la garde-robe (chambre 2)", "coulissante", None),
]

PIECES = [  # id, nom, point dans la pièce
    ("piece-SS-UTIL", "Utilité et buanderie", (50, 80)),
    ("piece-SS-GYM", "Salle d'entraînement", (165, 80)),
    ("piece-SS-SALON", "Séjour / salle à manger", (340, 80)),
    ("piece-SS-CUIS", "Cuisine", (380, 190)),
    ("piece-SS-CORR", "Corridor", (190, 180)),
    ("piece-SS-SDB", "Salle de bain", (80, 200)),
    ("piece-SS-CH1", "Chambre 1", (130, 320)),
    ("piece-SS-GR1", "G.-R.", (24, 320)),
    ("piece-SS-PASS", "Passage", (264, 300)),
    ("piece-SS-CH2", "Chambre 2", (360, 320)),
    ("piece-SS-GR2", "G.-R.", (415, 244)),
]
COUPES = [  # limites sans mur
    ((228, 157), (452, 157)),   # séjour / cuisine
    ((228, 157), (228, 204)),   # corridor / cuisine
    ((228, 230), (300, 230)),   # cuisine / passage
]

EQUIPEMENTS = [  # id, type, nom, libellé, x, y, rotation, (longueur, largeur)
    ("elem-SS-P-CE", "chauffe-eau", "Chauffe-eau", None, 34, 138, 0, (22, 22)),
    ("elem-SS-P-LAV", "laveuse", "Laveuse", None, 28, 24, 0, (27, 27)),
    ("elem-SS-P-SEC", "secheuse", "Sécheuse", None, 58, 24, 0, (27, 27)),
    ("elem-SS-P-BAIN", "baignoire", "Baignoire", None, 25.5, 190, 90, (60, 30)),
    ("elem-SS-P-WC", "toilette", "Toilette murale", None, 60, 212, 180, (22, 15)),
    ("elem-SS-P-DOUCHE", "autre", "Douche", "DOUCHE", 114, 177, 0, (60, 36)),
    ("elem-SS-P-VAN", "comptoir", "Double vanité", None, 187, 236.75, 180, (72, 22)),
    ("elem-SS-P-LAVABO1", "lavabo", "Lavabo", None, 169, 237, 180, (18, 14)),
    ("elem-SS-P-LAVABO2", "lavabo", "Lavabo", None, 205, 237, 180, (18, 14)),
    ("elem-SS-P-COMPT", "comptoir", "Comptoir de cuisine", None, 372, 218, 180, (84, 25)),
    ("elem-SS-P-EVIER", "evier", "Évier", None, 392, 218.5, 180, (30, 20)),
    ("elem-SS-P-CUIS", "cuisiniere", "Cuisinière", None, 348, 217.5, 180, (30, 25)),
    ("elem-SS-P-REF", "refrigerateur", "Réfrigérateur", None, 429.5, 215, 180, (30, 30)),
]


def _mur(mid, x1, y1, x2, y2, role):
    verre = role.startswith("VERRE")
    m = {"id": mid, "type": "int", "etat": "nouveau", "porteur": "non", "indices_porteur": [],
         "epaisseur": dim(2.0 if verre else T, "cloison vitrée, cadre d'aluminium noir" if verre else "cloison projetée 2x4 + gypse"),
         "x1": x1, "y1": y1, "x2": x2, "y2": y2,
         "source_position": "PRÉSUMÉ", "note": f"Cloison projetée — {role} ({SOURCE})."}
    if verre:
        m["materiau"] = "verre"
    return m


def _porte(oid, mur, centre, larg, vers, role, op, mat):
    horiz = mur["y1"] == mur["y2"]
    a = mur["x1"] if horiz else mur["y1"]
    b = mur["x2"] if horiz else mur["y2"]
    o = {"id": oid, "type": "porte", "operation": op, "mur_id": mur["id"], "etat": "nouveau",
         "position": dim(round(abs(centre - a), 2)), "largeur": dim(larg), "hauteur": dim(80),
         "allege": {"valeur": None, "source": "ILLISIBLE", "photo": None},
         "sens": {"charniere": "debut" if b > a else "fin", "ouvre_vers": vers}, "note": f"{role} ({SOURCE})"}
    if mat:
        o["materiau"] = mat
    return o


def appliquer(maison):
    p = maison["projet"]
    p.update({"proposition": "SS-03", "revision": "A", "date": DATE, "titre_notes": "NOTES DE LA PROPOSITION",
              "mention": "PROPOSITION SS-03 — GRANDE SALLE DE BAIN, CUISINE, CAVEAU EN RANGEMENT — ESQUISSE À VALIDER",
              "nom_pdf": "SS-03_grande_sdb_cuisine.pdf",
              "base": "copie de releve/livrables/donnees/maison.json (plans de base R0, commit 59ac401)"})
    p["affichage"] = dict(p.get("affichage") or {}, noms_pieces=True, dimensions_pieces=True)
    ss = next(n for n in maison["niveaux"] if n["id"] == "SS")
    maison["niveaux"] = [ss]
    maison["ecarts"] = []
    ss["feuille"] = "P-102"
    ss["nom"] = "Sous-sol proposé"

    murs = [_mur(*m) for m in MURS]
    ss["murs"] += murs
    par_id = {m["id"]: m for m in ss["murs"]}
    ss["ouvertures"] += [_porte(oid, par_id[mid], c, w, v, r, op, mt) for oid, mid, c, w, v, r, op, mt in PORTES]

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
        morceaux += list(polygonize(unary_union([r.exterior] + [i.exterior for i in r.interiors] + coupe))) if coupe else [r]
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
    ss["pieces"] = pieces + autres

    for eid, typ, nom, lib, x, y, rot, (L, W) in EQUIPEMENTS:
        e = {"id": eid, "type": typ, "nom": nom, "nom_original": None, "etat": "nouveau",
             "position": {"x": x, "y": y, "rotation_deg": rot, "source": "PRÉSUMÉ"},
             "dimensions": {"longueur": dim(L), "largeur": dim(W)}, "note": SOURCE}
        if lib:
            e["libelle"] = lib
        ss["elements"].append(e)
    ss["elements"].sort(key=lambda e: e["id"])
    notes = [
        "Esquisse : cloisons, portes, cuisine et appareils sanitaires projetés ; le reste est l'existant (plans de base R0).",
        "Salle de bain sur les drains existants (bain sous la fenêtre, toilette murale) ; vanité double dans l'alcôve, porte coulissante.",
        "Évier de cuisine à environ 8 pi du drain existant : raccord sous dalle à prévoir.",
        "Caveau : rangement fermé ; prévoir isolation et déshumidification avant d'y ranger des objets sensibles.",
        "Fenêtres des chambres à vérifier pour l'évacuation ; hauteur sous poutres et séparation coupe-feu à valider.",
    ]
    ss["notes"] = [{"id": f"note-SS-P{i + 1:02d}", "texte_original": None, "photo": None, "interpretation": t} for i, t in enumerate(notes)]
    ss["lignes_cote"] = [l for l in ss["lignes_cote"] if l.get("facade") != "int"]
    return maison
