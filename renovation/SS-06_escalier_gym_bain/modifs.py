"""SS-06 — Nouvel escalier, sous-sol repensé, bain sur pied, nouveau gym (copie de SS-05, revue avec le skill
designer-interieur).

Demandes du propriétaire (2026-10-29) :
- déplacer l'escalier, en haut et en bas, dans la bande dessinée en rouge sur A-101 : le long des garde-robes du
  rez-de-chaussée, de la fenêtre arrière (≈ x 15'-0" à 18'-2") jusqu'à ≈ 18'-9" du devant ; refaire le sous-sol au complet ;
- un bain sur pied moderne (pas encastré) avec un beau robinet noir ;
- gym : enlever le banc et les poids ; un tapis roulant, son vélo de route sur une base d'entraînement, des petits poids
  au sol.

Escalier : 14 contremarches (même hauteur d'étage qu'en 1957), x 15'-2" à 18'-2", du pied à y ≈ 19'-2" jusqu'au mur
arrière ; trois marches tournantes en haut (entrée par la droite au rez-de-chaussée, la volée ne peut pas commencer
contre le mur arrière). Au sous-sol, on arrive face à l'avant dans un hall central qui dessert tout.

Sous-sol :
- Hall central (ancienne alcôve de la vanité et corridor) : pied de l'escalier, porte vitrée du gym, salle de bain,
  chambre 1, passage du caveau, coin bar.
- Salle de bain (~80 pi²) : bain autoportant sous la fenêtre, robinet sur pied noir, douche de 60 × 36, toilette
  contre la cloison de la chambre 1, double vanité de 60 po ; porte coulissante dans le mur.
- Chambre 1 réduite à l'est par l'escalier ; dessous de l'escalier fermé (rangement possible).
- Chambre 2 agrandie vers l'ouest (l'ancien escalier n'y est plus), porte depuis le passage du caveau.
- Coin bar le long du mur de la chambre 2, entre la colonne et le frigo.
Coordonnées en pouces, repère de la maison. Murs à l'axe.
"""
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import polygonize, unary_union
from shapely.geometry.polygon import orient

T = 4.5
DATE = "2026-10-29"
SOURCE = "proposition SS-06 (esquisse)"


def dim(v, note=None, src="PRÉSUMÉ"):
    d = {"valeur": v, "source": src, "photo": None}
    if note:
        d["note"] = note
    return d


MURS = [  # id, x1, y1, x2, y2, rôle (« VERRE » = cloison vitrée, « LATTES » = claustra de bois)
    ("mur-SS-P01", 10, 157, 146, 157, "salle de lavage / salle de bain (axe de la poutre avant)"),
    ("mur-SS-P10", 146, 157, 228, 157, "VERRE : salle d'entraînement / hall (axe de la poutre avant)"),
    ("mur-SS-P09", 228, 10, 228, 157, "VERRE : salle d'entraînement / séjour"),
    ("mur-SS-P08", 112, 10, 112, 157, "salle de lavage / salle d'entraînement"),
    ("mur-SS-P04", 142, 157, 142, 250, "salle de bain / hall"),
    ("mur-SS-P05", 10, 250, 179.75, 250, "salle de bain / chambre 1"),
    ("mur-SS-P17", 179.75, 230, 179.75, 370, "chambre 1 / escalier"),
    ("mur-SS-P16", 219.5, 230, 219.5, 370, "LATTES : garde de l'escalier / passage du caveau"),
    ("mur-SS-P07", 278.25, 230, 278.25, 370, "passage du caveau / chambre 2"),
    ("mur-SS-P11", 278.25, 230, 446, 230, "coin bar / chambre 2"),
    ("mur-SS-P12", 38.25, 280, 38.25, 370, "garde-robe / chambre 1"),
    ("mur-SS-P13", 10, 280, 38.25, 280, "garde-robe / chambre 1"),
    ("mur-SS-P14", 384, 258.25, 446, 258.25, "garde-robe / chambre 2"),
    ("mur-SS-P15", 384, 230, 384, 258.25, "garde-robe / chambre 2"),
]

PORTES = [  # id, mur, centre, largeur, ouvre_vers, rôle, opération, matériau, charnière (None = début du mur)
    ("ouv-SS-P01", "mur-SS-P10", 168.0, 32, "droite", "porte vitrée de la salle d'entraînement", "battante", "verre", "fin"),
    ("ouv-SS-P02", "mur-SS-P08", 135.0, 30, "gauche", "porte de la salle de lavage", "battante", None, "fin"),
    ("ouv-SS-P03", "mur-SS-P04", 220.0, 30, "gauche", "porte coulissante dans le mur de la salle de bain", "coulissante", None, None),
    ("ouv-SS-P05", "mur-SS-P05", 161.0, 30, "gauche", "porte de la chambre 1", "battante", None, "fin"),
    ("ouv-SS-P06", "mur-SS-P07", 252.0, 32, "droite", "porte de la chambre 2", "battante", None, None),
    ("ouv-SS-P07", "mur-SS-P12", 325.0, 60, "droite", "portes coulissantes de la garde-robe (chambre 1)", "coulissante", None, None),
    ("ouv-SS-P08", "mur-SS-P14", 415.0, 48, "gauche", "portes coulissantes de la garde-robe (chambre 2)", "coulissante", None, None),
]

PIECES = [  # id, nom, point dans la pièce
    ("piece-SS-LAVAGE", "Salle de lavage", (50, 80)),
    ("piece-SS-GYM", "Salle d'entraînement", (170, 80)),
    ("piece-SS-SALON", "Séjour", (340, 80)),
    ("piece-SS-BAR", "Coin bar", (390, 190)),
    ("piece-SS-HALL", "Hall", (195, 190)),
    ("piece-SS-SDB", "Salle de bain", (60, 215)),
    ("piece-SS-CH1", "Chambre 1", (100, 320)),
    ("piece-SS-GR1", "G.-R.", (24, 320)),
    ("piece-SS-ESC", "Escalier", (200, 300)),
    ("piece-SS-PASS", "Passage", (248, 300)),
    ("piece-SS-CH2", "Chambre 2", (360, 320)),
    ("piece-SS-GR2", "G.-R.", (415, 244)),
]
COUPES = [  # limites sans mur (prolongées jusqu'aux murs ; l'excédent est coupé par la région)
    ((226, 157), (452, 157)),   # séjour / coin bar
    ((228, 155), (228, 232)),   # hall / coin bar
    ((179, 230), (280, 230)),   # hall / escalier et passage du caveau
]

# Escalier : nouvel emplacement (croquis du propriétaire sur A-101, 2026-10-29) ; 14 contremarches comme en 1957 (P2)
ESCALIER = {"id": "elem-SS-P-ESC", "x": 200.0, "y": 298.0, "L": 136.0, "W": 36.0}

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
    ("elem-SS-P-BARC", "comptoir", "Comptoir du coin bar", None, 373, 218, 180, (82, 24)),
    ("elem-SS-P-EVBAR", "evier", "Lavabo de bar", None, 362, 218.5, 180, (16, 15)),
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
    p.update({"proposition": "SS-06", "revision": "A", "date": DATE, "titre_notes": "NOTES DE LA PROPOSITION",
              "mention": "PROPOSITION SS-06 — NOUVEL ESCALIER, SOUS-SOL REPENSÉ — ESQUISSE À VALIDER",
              "nom_pdf": "SS-06_escalier_gym_bain.pdf",
              "base": "copie de releve/livrables/donnees/maison.json (plans de base R0, commit 59ac401)"})
    p["affichage"] = dict(p.get("affichage") or {}, noms_pieces=True, dimensions_pieces=True)
    ss = next(n for n in maison["niveaux"] if n["id"] == "SS")
    rdc = next(n for n in maison["niveaux"] if n["id"] == "RDC")
    maison["ecarts"] = []
    ss["feuille"], ss["nom"] = "P-105", "Sous-sol proposé"
    rdc["feuille"], rdc["nom"] = "P-106", "RDC proposé"

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
    note_esc = ("Nouvel emplacement dessiné par le propriétaire sur A-101 (2026-10-29). 14 contremarches comme l'escalier "
                "de 1957 (P2) ; 13 girons dont 3 tournants en haut (entrée par la droite au rez-de-chaussée). Hauteur "
                "plancher-plancher non mesurée : giron, hauteur de marche, échappée et trémie à valider — " + SOURCE)
    for niv, fl, dr in ((ss, "MONTE", "+y"), (rdc, "DESCEND", "-y")):
        niv["elements"].append({
            "id": ESCALIER["id"].replace("-SS-", "-" + niv["id"] + "-"), "type": "escalier",
            "nom": "Escalier entre le sous-sol et le rez-de-chaussée (projeté)", "nom_original": None, "etat": "nouveau",
            "position": {"x": ESCALIER["x"], "y": ESCALIER["y"], "rotation_deg": 0, "source": "PRÉSUMÉ"},
            "dimensions": {"longueur": dim(ESCALIER["L"], "course : 10 girons droits + 3 tournants"), "largeur": dim(ESCALIER["W"])},
            "escalier": {"nb_contremarches": dict(vieux["escalier"]["nb_contremarches"]), "fleche": fl, "direction": dr},
            "note": note_esc})
        niv["elements"].sort(key=lambda e: e["id"])
    # rez-de-chaussée : garde le long de l'escalier côté salle à manger ; la porte de garde-robe qui donnait sur la bande
    # de l'escalier est enlevée (à refaire côté chambre)
    for x in rdc["pieces"]:
        x["etiquette"] = False          # comme A-101 : pas de noms de pièces au rez-de-chaussée (appartement existant)
    garde = _mur("mur-RDC-P01", 219.5, 230, 219.5, 330, "LATTES : garde de l'escalier / salle à manger")
    rdc["murs"].append(garde)
    rdc["ouvertures"] = [o for o in rdc["ouvertures"] if o["id"] != "ouv-RDC-018"]
    rdc["notes"] = [{"id": f"note-RDC-P{i + 1:02d}", "texte_original": None, "photo": None, "interpretation": t} for i, t in enumerate((
        "Escalier projeté (même emplacement qu'au sous-sol) : trémie d'environ 3 × 9 pi à ouvrir dans le plancher.",
        "Entrée par la droite, au fond (trois marches tournantes) ; garde en lattes de chêne côté salle à manger.",
        "Porte de garde-robe qui donnait sur l'escalier enlevée : à refaire du côté de la chambre.",
        "Fenêtre arrière au-dessus du haut de l'escalier ; séparation coupe-feu entre logements à valider."))]
    ss["elements"].sort(key=lambda e: e["id"])
    notes = [
        "Esquisse : cloisons, portes, escalier, bar et appareils projetés ; le reste est l'existant (base R0).",
        "Escalier de 14 c.m. au nouvel emplacement (voir P-106) : trémie à ouvrir, giron et échappée à valider.",
        "Fenêtre arrière de la chambre 1 coupée par l'escalier : la réduire ou la condamner (à décider).",
        "Salle de bain : bain autoportant et toilette déplacés, drains existants ignorés (tranchée).",
        "Coin bar : lavabo de bar à ~6 pi du drain de la chambre 2 (raccord à prévoir).",
        "Évacuation des chambres, hauteur sous poutres, coupe-feu à valider.",
    ]
    ss["notes"] = [{"id": f"note-SS-P{i + 1:02d}", "texte_original": None, "photo": None, "interpretation": t} for i, t in enumerate(notes)]
    ss["lignes_cote"] = [l for l in ss["lignes_cote"] if l.get("facade") != "int"]
    return maison
