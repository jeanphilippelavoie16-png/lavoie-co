"""RDC-01 — État actuel du rez-de-chaussée, d'après les 15 photos du propriétaire du 2026-11-01
(renovation/prive/rdc_actuel/, hors du dépôt).

Ce n'est PAS une proposition : c'est un relevé photo de ce qui existe aujourd'hui. La base R0 (A-101) est reprise telle
quelle, sauf là où les photos la contredisent ; chaque écart porte "source_position": "PHOTO" (ou une dimension
ESTIMÉ avec la photo citée) et est listé dans DESIGN.md, à vérifier sur place au ruban.
Les équipements vus sur les photos (cuisine, salle de bain) sont ajoutés au plan comme éléments existants.
Le sous-sol (R-100) est inchangé. Pouces, repère de la maison.
"""
from shapely.geometry import Polygon, box
from shapely.geometry.polygon import orient

SOURCE = "relevé photo RDC-01 (photos du 2026-11-01)"


def dim(v, note=None, src="ESTIMÉ", photo=None):
    d = {"valeur": v, "source": src, "photo": photo}
    if note:
        d["note"] = note
    return d


# Équipements vus sur les photos : id, type, nom, libellé, x, y, rotation (dos vers −y à 0°), (longueur, largeur), photos
# rotation : 0 = dos au mur avant (y bas), 180 = dos au mur arrière, 90 = dos au mur de droite (x = 446), 270 = dos à gauche
EQUIPEMENTS = [
    # cuisine — mur arrière (évier sous la fenêtre) et mur de droite (cuisinière, colonne d'armoires, frigo encastré)
    ("elem-RDC-R-CPT1", "comptoir", "Comptoir en bois de grange sur armoires noires (mur arrière)", None, 382, 357.5, 180, (128, 25), "01, 08"),
    ("elem-RDC-R-EVIER", "evier", "Évier double noir, robinet noir", None, 375, 358, 180, (33, 20), "01, 08"),
    ("elem-RDC-R-LV", "autre", "Lave-vaisselle inox", "L.V.", 348, 357.5, 180, (24, 24), "01, 08"),
    ("elem-RDC-R-CPT2", "comptoir", "Comptoir (mur de droite, entre le coin et la cuisinière)", None, 433.5, 340.5, 90, (9, 25), "02, 08"),
    ("elem-RDC-R-CUIS", "cuisiniere", "Cuisinière inox 30 po, hotte cheminée inox", None, 433.5, 321, 90, (30, 25), "01, 02, 08"),
    ("elem-RDC-R-CPT3", "comptoir", "Comptoir (après la cuisinière)", None, 433.5, 298, 90, (16, 25), "02"),
    ("elem-RDC-R-COL", "armoires", "Colonne d'armoires pleine hauteur noir mat", None, 433.5, 248, 90, (84, 25), "01, 02"),
    ("elem-RDC-R-FRIGO1", "refrigerateur", "Frigo inox encastré dans la colonne", None, 432, 258, 90, (36, 28), "01, 02"),
    ("elem-RDC-R-FRIGO2", "refrigerateur", "Frigo inox à portes françaises (devant la fenêtre)", None, 431, 180, 90, (36, 30), "01, 02, 03"),
    ("elem-RDC-R-ILOT", "comptoir", "Îlot noir, dessus en bois de grange (3 tabourets côté salle à manger)", "ÎLOT", 362, 258, 90, (84, 40), "01, 02, 03, 08"),
    # salle de bain — laveuse et sécheuse empilées, douche vitrée, toilette sous la fenêtre, vanité double
    ("elem-RDC-R-LAV", "laveuse", "Laveuse et sécheuse frontales empilées", None, 90.5, 158.25, 0, (27, 28), "13, 14, 15"),
    ("elem-RDC-R-DOU", "autre", "Douche vitrée coulissante (cadre noir), tuile blanche, niche", "DOUCHE", 42, 161.25, 0, (60, 34), "13, 14, 15"),
    ("elem-RDC-R-WC", "toilette", "Toilette (sous la fenêtre)", None, 24, 190, 270, (16, 28), "13, 14, 15"),
    ("elem-RDC-R-VAN", "comptoir", "Vanité noire, deux vasques blanches à poser, robinets noirs hauts", None, 73, 210, 180, (62, 20), "13, 14"),
    ("elem-RDC-R-LAVABO1", "lavabo", "Vasque à poser", None, 58, 210, 180, (16, 16), "14"),
    ("elem-RDC-R-LAVABO2", "lavabo", "Vasque à poser", None, 88, 210, 180, (16, 16), "14"),
]


def appliquer(maison):
    p = maison["projet"]
    p.update({"proposition": "RDC-01", "revision": "A", "date": "2026-11-01", "titre_notes": "NOTES DU RELEVÉ PHOTO",
              "mention": "RDC-01 — ÉTAT ACTUEL DU REZ-DE-CHAUSSÉE (PHOTOS DU 2026-11-01)",
              "nom_pdf": "RDC-01_etat_actuel.pdf",
              "base": "copie de releve/livrables/donnees/maison.json (plans de base R0, commit 59ac401)"})
    p["affichage"] = dict(p.get("affichage") or {}, noms_pieces=True, dimensions_pieces=True)
    ss = next(n for n in maison["niveaux"] if n["id"] == "SS")
    rdc = next(n for n in maison["niveaux"] if n["id"] == "RDC")
    maison["ecarts"] = []
    ss["feuille"], ss["nom"] = "R-100", "Sous-sol (inchangé)"
    rdc["feuille"], rdc["nom"] = "R-101", "Rez-de-chaussée actuel"
    rdc["photos_sources"] = ["photos 01 à 15 du 2026-11-01"]
    murs = {m["id"]: m for m in rdc["murs"]}

    # 1) salle de bain plus profonde que la base : laveuse-sécheuse (≈ 28 po), douche (≈ 34 po), passage (≈ 22 po) et
    #    vanité (≈ 20 po) ne tiennent pas dans 61 po. On recule la cloison salle de bain / chambre avant de 15 po
    #    (y 157 → 142) sur la largeur de la salle de bain ; la porte est déplacée à côté de la laveuse (photo 13).
    m12, m11 = murs["mur-RDC-012"], murs["mur-RDC-011"]
    dx = 108 - m12["x1"]
    m12["x1"] = 108
    m11["y1"] = 142
    m11["source_position"] = "PHOTO"
    m11["note"] = (m11.get("note") or "") + " — prolongée jusqu'à y = 142 (salle de bain plus profonde, photos 13 à 15) : À MESURER."
    for o in rdc["ouvertures"]:
        if o["mur_id"] == "mur-RDC-012":
            o["position"] = dict(o["position"], valeur=round(o["position"]["valeur"] - dx, 2))
        if o["id"] == "ouv-RDC-015":       # porte de la salle de bain : centre y 178 → 188 (à côté de la laveuse)
            o["position"] = dim(188 - 142, "centre à y ≈ 188 : la laveuse-sécheuse est juste à gauche en entrant (photo 13) — À MESURER",
                                "ESTIMÉ", "rdc_actuel/13")
            o["source_position"] = "PHOTO"
    # portes fermées sur les photos (garde-robes, lingerie) : dessinées fermées dans la maquette 3D
    for o in rdc["ouvertures"]:
        if o["id"] in ("ouv-RDC-018", "ouv-RDC-020", "ouv-RDC-021", "ouv-RDC-022"):
            o["fermee"] = True
    rdc["murs"].append({"id": "mur-RDC-R01", "type": "int", "porteur": "inconnu", "indices_porteur": [],
                        "epaisseur": dict(m12["epaisseur"]), "x1": 5, "y1": 142, "x2": 108, "y2": 142,
                        "source_position": "PHOTO",
                        "note": "Cloison salle de bain / chambre avant, reportée 15 po plus à l'avant que la base (y 157 → 142) : "
                                "la salle de bain des photos 13 à 15 est plus profonde que 61 po — À MESURER (" + SOURCE + ")."})
    for x in rdc["pieces"]:
        P = Polygon(x["polygone"])
        if x["id"] == "piece-RDC-SDB":
            P = P.union(box(10, 144.25, 105.75, 159.5))
        elif x["id"] == "piece-RDC-CH2":
            P = P.difference(box(0, 139.75, 110.25, 160))
        else:
            continue
        P = orient(P.simplify(0.01), 1.0)
        x["polygone"] = [[round(a, 2), round(b, 2)] for a, b in list(P.exterior.coords)[:-1]]
        x["superficie"] = dim(round(P.area / 144, 1), "aire recalculée avec la cloison reportée (photos) — " + SOURCE, "DÉDUIT")
        x0, y0, x1, y1 = P.bounds
        x["dimensions"] = {"x": dim(round(x1 - x0, 2), None, "DÉDUIT"), "y": dim(round(y1 - y0, 2), None, "DÉDUIT")}

    # 2) poutre de bois brut apparente : seulement du hall au mur de droite (rien de visible dans la salle de bain ni
    #    la chambre avant) ; une seconde poutre coiffe l'ouverture hall / salon (photos 03, 04, 05)
    for s in rdc["structure"]:
        if s["id"] == "str-RDC-P02":
            s["geometrie"] = dict(s["geometrie"], x1=175)
            s["source_position"] = "PHOTO"
            s["note"] = (s.get("note") or "") + (" — partie apparente (bois brut teint) du hall au mur de droite, photos 01 à 05 ; "
                                                 "côté chambres : cachée dans le plafond ou les cloisons (" + SOURCE + ").")
    rdc["structure"].append({"id": "str-RDC-R01", "type": "poutre", "libelle": None,
                             "dimension": dim(None, "section non relevée ; bois brut teint apparent", "ILLISIBLE", "rdc_actuel/04"),
                             "sens": "y", "geometrie": {"x1": 222, "y1": 94.6, "x2": 222, "y2": 157},
                             "source_position": "PHOTO",
                             "note": "Poutre apparente au-dessus de l'ouverture hall / salon, du bout de la cloison au poteau de l'axe B "
                                     "(photos 03, 04, 05) ; décorative ou porteuse : à vérifier (" + SOURCE + ")."})

    # 3) équipements existants vus sur les photos (cuisine, salle de bain)
    for eid, typ, nom, lib, x, y, rot, (L, W), ph in EQUIPEMENTS:
        e = {"id": eid, "type": typ, "nom": nom, "nom_original": None, "etat": "existant",
             "position": {"x": x, "y": y, "rotation_deg": rot, "source": "ESTIMÉ"},
             "dimensions": {"longueur": dim(L, None, "ESTIMÉ", "rdc_actuel/" + ph), "largeur": dim(W, None, "ESTIMÉ", "rdc_actuel/" + ph)},
             "photo": "rdc_actuel/" + ph, "note": f"vu sur les photos {ph} ; position et dimensions estimées — {SOURCE}"}
        if lib is not None:
            e["libelle"] = lib
        rdc["elements"].append(e)
    rdc["elements"].sort(key=lambda e: e["id"])

    rdc["notes"] = [{"id": f"note-RDC-R{i + 1:02d}", "texte_original": None, "photo": None, "interpretation": t} for i, t in enumerate((
        "Relevé photo de l'état actuel (15 photos du 2026-11-01) : ce n'est pas une proposition.",
        "Salle de bain : cloison côté chambre avant reportée de 15 po (photos) ; à mesurer.",
        "Porte de la salle de bain déplacée de 10 po vers l'arrière (laveuse-sécheuse à côté) ; à mesurer.",
        "Poutres et poteaux de bois brut teint apparents : axe B (hall → mur de droite) et ouverture du hall.",
        "Cuisine : brique, armoires noires, îlot, frigo encastré et frigo à portes françaises (photos 01 à 03, 08).",
        "Chambre avant : non photographiée ; mobilier de la maquette présumé."))]
    ss["notes"] = [{"id": "note-SS-R01", "texte_original": None, "photo": None,
                    "interpretation": "Sous-sol inchangé (base R0) ; ce relevé porte sur le rez-de-chaussée (R-101)."}]
    return maison
