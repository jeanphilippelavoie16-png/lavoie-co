"""SS-01 — Esquisse d'aménagement du sous-sol (appartement indépendant).

Programme demandé par le propriétaire (2026-10-29) : deux chambres, une grande salle de bain, un salon / salle de jeu,
une salle d'entraînement, une salle d'utilité avec le panneau électrique et le chauffe-eau.

Partis pris :
- un corridor entre les deux poutres du sous-sol (axes à 13'-1" et 17'-0" du nu ext. avant) : ses murs passent sur les
  six colonnes 8"x8", qui disparaissent dans les cloisons, et il part de la porte extérieure du mur droit ;
- la salle de bain sur les drains existants (bain et toilette, côté gauche) ;
- la salle d'utilité contre le mur gauche, autour du panneau électrique existant ;
- chaque chambre sur une fenêtre existante (arrière gauche, mur droit arrière) ;
- l'accès au caveau conservé par un passage entre les chambres.
Coordonnées en pouces, repère de la maison (origine au coin ext. avant-gauche, y vers l'arrière). Murs à l'axe.
"""
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import polygonize, unary_union
from shapely.geometry.polygon import orient

T = 4.5           # cloison projetée 2x4 + gypse
DATE = "2026-10-29"
SOURCE = "proposition SS-01 (esquisse)"


def dim(v, note=None, src="PRÉSUMÉ"):
    d = {"valeur": v, "source": src, "photo": None}
    if note:
        d["note"] = note
    return d


MURS = [  # id, x1, y1, x2, y2, rôle
    ("mur-SS-P01", 10, 157, 360, 157, "corridor / utilité, salle d'entraînement, salon (axe de la poutre avant)"),
    ("mur-SS-P02", 146, 204, 228, 204, "corridor / rangement (axe de la poutre arrière)"),
    ("mur-SS-P03", 300, 204, 446, 204, "corridor / chambre 2 (axe de la poutre arrière)"),
    ("mur-SS-P04", 146, 157, 146, 250, "salle de bain / corridor et rangement"),
    ("mur-SS-P05", 10, 250, 228, 250, "salle de bain et rangement / chambre 1"),
    ("mur-SS-P06", 228, 204, 228, 370, "chambre 1 et rangement / passage du caveau"),
    ("mur-SS-P07", 300, 204, 300, 370, "passage du caveau / chambre 2"),
    ("mur-SS-P08", 100, 10, 100, 157, "salle d'utilité / salle d'entraînement"),
    ("mur-SS-P09", 228, 10, 228, 157, "salle d'entraînement / salon"),
]

PORTES = [  # id, mur, centre (coordonnée le long du mur), largeur, ouvre_vers, rôle
    ("ouv-SS-P01", "mur-SS-P01", 200.0, 32, "droite", "porte de la salle d'entraînement"),
    ("ouv-SS-P02", "mur-SS-P08", 125.0, 30, "gauche", "porte de la salle d'utilité (depuis la salle d'entraînement)"),
    ("ouv-SS-P03", "mur-SS-P04", 180.5, 30, "gauche", "porte de la salle de bain"),
    ("ouv-SS-P04", "mur-SS-P05", 190.0, 28, "gauche", "porte du rangement (walk-in de la chambre 1)"),
    ("ouv-SS-P05", "mur-SS-P06", 300.0, 32, "gauche", "porte de la chambre 1"),
    ("ouv-SS-P06", "mur-SS-P07", 300.0, 32, "droite", "porte de la chambre 2"),
]

PIECES = [  # id, nom, point dans la pièce
    ("piece-SS-UTIL", "Salle d'utilité", (50, 80)),
    ("piece-SS-GYM", "Salle d'entraînement", (165, 80)),
    ("piece-SS-SALON", "Salon / salle de jeu", (340, 80)),
    ("piece-SS-SDB", "Salle de bain", (80, 200)),
    ("piece-SS-CORR", "Corridor", (380, 180)),
    ("piece-SS-RANG", "G.-R.", (190, 227)),
    ("piece-SS-CH1", "Chambre 1", (120, 310)),
    ("piece-SS-PASS", "Passage (caveau)", (264, 300)),
    ("piece-SS-CH2", "Chambre 2", (370, 300)),
]
COUPES = [  # limites sans mur entre espaces ouverts
    ((360, 157), (452, 157)),   # salon / corridor : grande ouverture près de l'entrée
    ((228, 204), (300, 204)),   # corridor / passage du caveau
]

EQUIPEMENTS = [  # id, type, nom, libellé, x, y, rotation, (longueur, largeur)
    ("elem-SS-P-CE", "chauffe-eau", "Chauffe-eau", None, 34, 136, 0, (22, 22)),
    ("elem-SS-P-BAIN", "baignoire", "Baignoire", None, 25.5, 220, 90, (60, 30)),
    ("elem-SS-P-WC", "toilette", "Toilette", None, 60, 212, 180, (28, 18)),
    ("elem-SS-P-VAN", "lavabo", "Vanité", None, 78, 171, 180, (44, 22)),
    ("elem-SS-P-DOUCHE", "autre", "Douche", "DOUCHE", 126, 230, 0, (36, 36)),
]


def _mur(mid, x1, y1, x2, y2, role):
    return {"id": mid, "type": "int", "etat": "nouveau", "porteur": "non", "indices_porteur": [],
            "epaisseur": dim(T, "cloison projetée 2x4 + gypse"), "x1": x1, "y1": y1, "x2": x2, "y2": y2,
            "source_position": "PRÉSUMÉ", "note": f"Cloison projetée — {role} ({SOURCE})."}


def _porte(oid, mur, centre, larg, vers, role):
    horiz = mur["y1"] == mur["y2"]
    a = mur["x1"] if horiz else mur["y1"]
    b = mur["x2"] if horiz else mur["y2"]
    pos = abs(centre - a)
    return {"id": oid, "type": "porte", "operation": "battante", "mur_id": mur["id"], "etat": "nouveau",
            "position": dim(round(pos, 2)), "largeur": dim(larg), "hauteur": dim(80),
            "allege": {"valeur": None, "source": "ILLISIBLE", "photo": None},
            "sens": {"charniere": "debut" if b > a else "fin", "ouvre_vers": vers}, "note": f"{role} ({SOURCE})"}


def appliquer(maison):
    p = maison["projet"]
    p["proposition"] = "SS-01"
    p["mention"] = "PROPOSITION SS-01 — ESQUISSE D'AMÉNAGEMENT DU SOUS-SOL, À VALIDER"
    p["revision"] = "A"
    p["titre_notes"] = "NOTES DE LA PROPOSITION"
    p["nom_pdf"] = "SS-01_amenagement_sous-sol.pdf"
    p["date"] = DATE
    p["affichage"] = dict(p.get("affichage") or {}, noms_pieces=True, dimensions_pieces=True)
    p["base"] = "copie de releve/livrables/donnees/maison.json (plans de base R0, étiquette plans-de-base-R0)"
    ss = next(n for n in maison["niveaux"] if n["id"] == "SS")
    maison["niveaux"] = [ss]
    maison["ecarts"] = []
    ss["feuille"] = "P-100"
    ss["nom"] = "Sous-sol proposé"

    murs = [_mur(*m) for m in MURS]
    ss["murs"] += murs
    par_id = {m["id"]: m for m in ss["murs"]}
    ss["ouvertures"] += [_porte(oid, par_id[mid], c, w, v, r) for oid, mid, c, w, v, r in PORTES]

    # pièces : intérieur du sous-sol découpé par les cloisons projetées et les limites sans mur
    princ = next(x for x in ss["pieces"] if x["id"] == "piece-SS-PRINC")
    autres = [x for x in ss["pieces"] if x["id"] != "piece-SS-PRINC"]
    zone = Polygon(princ["polygone"])
    emprises = unary_union([LineString([(m["x1"], m["y1"]), (m["x2"], m["y2"])]).buffer(T / 2, cap_style=3) for m in murs])
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
        pieces.append({"id": pid, "nom": nom, "nom_original": None, "etat": "nouveau",
                       "description": f"{nom} — {SOURCE}",
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
    for e in ss["elements"]:
        if e["id"] == "elem-SS-DR-LAV":
            e["note"] = (e.get("note") or "") + " ; dans la chambre 2 de la proposition SS-01 : à condamner ou à réutiliser"
    ss["elements"].sort(key=lambda e: e["id"])
    ss["notes"] = [{"id": "note-SS-P01", "texte_original": None, "photo": None,
                    "interpretation": "Esquisse : cloisons, portes et équipements de salle de bain projetés ; tout le reste est l'existant (plans de base R0)."},
                   {"id": "note-SS-P02", "texte_original": None, "photo": None,
                    "interpretation": "Les murs du corridor passent sur les deux poutres et les six colonnes 8\"x8\" existantes."},
                   {"id": "note-SS-P03", "texte_original": None, "photo": None,
                    "interpretation": "Fenêtres des chambres à vérifier pour l'évacuation (dimension et hauteur d'allège) ; hauteur sous poutres à mesurer."}]
    ss["lignes_cote"] = [l for l in ss["lignes_cote"] if l.get("facade") != "int"]
    return maison
