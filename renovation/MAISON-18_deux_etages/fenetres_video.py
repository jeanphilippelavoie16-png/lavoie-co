"""MAISON-18 — fenêtres aux dimensions de la vidéo de l'architecte paysagiste (DAG).

Client (2026-11-02) : « les fenêtres dans la vidéo sont de bonnes dimensions ». Les fenêtres VISIBLES dans la vidéo prennent
sa largeur, son allège, sa tête et son nombre de sections ; celles qu'on n'y voit pas gardent leurs valeurs. Tableau avant /
après, méthode, écarts entre les relevés et points à mesurer : DESIGN_fenetres_video.md.

Deux relevés indépendants des 12 captures (A : homographies et bords au demi-pixel ; B : profils de luminance et de R−G,
rangs de brique), réconciliés ; recoupe propre sur les captures 01 (façade avant) et 03 (mur de droite) là où ils divergeaient.

Règles :
- largeur et centre : on garde ceux du plan (cotes LU) quand la vidéo s'en écarte de moins que l'incertitude de mesure
  (≈ 2 po sur 01 et 10, ≈ 3 po sur 03) ; sinon la vidéo fait foi. Un centre ne bouge que si l'écart est flagrant et
  confirmé par les deux relevés : ouv-SS-002 seulement (+13 po vers l'allée, bord droit aligné sur ouv-RDC-002) ;
- tête : dans la vidéo, toutes les fenêtres montent au soffite, à la tête des portes (79–80 po du plancher de l'étage, au
  RDC comme au SS) ; on la met à 80 po, la tête des portes de la maquette (le moteur les dessine à 80 po). Allège mesurée
  depuis le plancher de l'étage (bas de la porte avant pour le RDC, plancher du SS = RDC − 105 po) ;
- sections : comptées sur les vitres. Le moteur ne fait que des meneaux également répartis (SCENE["fenetres"]["sections"]) :
  les deux fenêtres de façade à sections inégales (ouv-RDC-001 : 1/3 + 2/3 ; ouv-RDC-002 : 3/4 + 1/4) reçoivent
  "sections": 1 et leur meneau est ajouté au mobilier par meneaux_3d(), identique à celui du moteur.

Utilisé par :
- modifs.py (plans P-129 / P-130, maison.json) : appliquer_plans(maison) — largeur, centre, allège, hauteur, notes des
  ouvertures et chaînes de cotes des façades ;
- zone_global.py (3D du sous-sol) et base_rdc01_scene.py (3D du rez-de-chaussée) : reglages_3d(niveau), meneaux_3d(niveau, B).
Pouces ; x le long de la façade (nu ext. 0 → 456), y vers l'arrière (0 → 380) ; z depuis le plancher de l'étage.
"""
import math
import sys

DATE = "2026-11-02"
TETE = 80            # tête de toutes les fenêtres de la vidéo (au soffite, alignée sur les portes : 80 po dans la maquette)
SOURCE = "vidéo DAG"

# Par fenêtre visible dans la vidéo :
#   plan   : état AVANT (largeur, centre, allège, tête, sections) — centre = x pour un mur parallèle à x, y sinon ;
#   video  : valeurs retenues ; largeur / centre None = ceux du plan gardés (écart sous l'incertitude) ;
#   meneaux: fractions de la largeur, depuis le bout de plus petite coordonnée (sections inégales, voir meneaux_3d) ;
#   axe / coord : mur parallèle à « x » (coord = y de son axe) ou à « y » (coord = x de son axe) ; facade : chaînes de cotes ;
#   A, B : relevés bruts (largeur, allège, tête, sections, centre) ; images : captures ; note : décision.
FENETRES = {
    # ------------------------------------------------------------------------------------------- rez-de-chaussée
    "ouv-RDC-001": dict(
        niveau="RDC", piece="Bureau", mur="mur-RDC-001", axe="x", coord=5.0, facade="avant",
        plan=dict(largeur=75, centre=98, allege=34, tete=82, sections=2),
        video=dict(largeur=None, centre=None, allege=37.5, tete=TETE, sections=2), meneaux=[1 / 3],
        A=(76, 37, 79, 2, 97.5), B=(77, 38, 79, 2, 98), images="01 (mesure), 02, 03", confiance="haute",
        note="2 sections inégales : petite (≈ 25 po) côté x 0, à gauche vu de la rue ; largeur 76–77 dans la vidéo = 6'-3\" "
             "du plan à l'incertitude près (gardée)"),
    "ouv-RDC-002": dict(
        niveau="RDC", piece="Salon", mur="mur-RDC-001", axe="x", coord=5.0, facade="avant",
        plan=dict(largeur=108, centre=377, allege=20, tete=82, sections=3),
        video=dict(largeur=None, centre=None, allege=12, tete=TETE, sections=2), meneaux=[3 / 4],
        A=(109, 11.5, 79, 2, 375.7), B=(108, 12, 79, 2, 377), images="01 (mesure), 02, 03", confiance="haute",
        note="2 sections et non 3 : grand fixe (≈ 81 po) côté porte, petite section (≈ 27 po) côté allée ; allège ≈ 12 po "
             "(l'hypothèse de 20 po tombe)"),
    "ouv-RDC-003": dict(
        niveau="RDC", piece="Chambre des parents", mur="mur-RDC-003", axe="x", coord=375.0, facade="arriere",
        plan=dict(largeur=75, centre=98, allege=34, tete=82, sections=2),
        video=dict(largeur=None, centre=None, allege=23.5, tete=TETE, sections=3),
        A=(76, 23, 79, 3, 99), B=(75, 24, 80, 3, 98), images="10 (mesure), 11, 09", confiance="haute",
        note="nettement plus haute que la cuisine (≈ 56 po) ; 3 sections égales"),
    "ouv-RDC-004": dict(
        niveau="RDC", piece="Salle à manger", mur="mur-RDC-003", axe="x", coord=375.0, facade="arriere",
        plan=dict(largeur=36, centre=197, allege=34, tete=82, sections=2),
        video=dict(largeur=None, centre=None, allege=37.5, tete=TETE, sections=2),
        A=(36, 37, 79, 2, 198), B=(34, 38, 80, 2, 197), images="10 (mesure), 11", confiance="moyenne",
        note="en partie cachée par l'entrée arrière sur la 10 ; même bas que la cuisine"),
    "ouv-RDC-005": dict(
        niveau="RDC", piece="Cuisine", mur="mur-RDC-003", axe="x", coord=375.0, facade="arriere",
        plan=dict(largeur=75, centre=375, allege=34, tete=82, sections=2),
        video=dict(largeur=None, centre=None, allege=37.5, tete=TETE, sections=3),
        A=(75, 37, 79, 3, 378), B=(75, 38, 80, 3, 378), images="10 (mesure), 11, 07", confiance="moyenne",
        note="3 sections égales (le tiers côté entrée arrière est caché sur la 10, vu sur la 11) ; centre 378 dans la vidéo, "
             "375 au plan : gardé (3 po)"),
    "ouv-RDC-007": dict(
        niveau="RDC", piece="Cuisine", mur="mur-RDC-002", axe="y", coord=451.0, facade="droite",
        plan=dict(largeur=36, centre=180, allege=34, tete=82, sections=2),
        video=dict(largeur=None, centre=None, allege=24, tete=TETE, sections=2),
        A=(36, 23.5, 79, 2, 178), B=(40, 24, 80, 2, 177), images="03 (seule, de biais)", confiance="moyenne",
        note="haute et étroite, juste au-dessus de la porte de côté du SS ; largeur 36 (A) / 40 (B) : recoupe sur la 03 "
             "(R−G) ≈ 31–35 po, on garde 36 (plan)"),
    "ouv-RDC-008": dict(
        niveau="RDC", piece="Entrée arrière", mur="mur-RDC-006", axe="x", coord=435.0, facade="arriere",
        plan=dict(largeur=42, centre=293, allege=34, tete=82, sections=2),
        video=dict(largeur=36, centre=None, allege=38, tete=TETE, sections=2),
        A=(36, 37.5, 79, 2, 294), B=(36, 39, 80, 2, 293), images="10 (mesure), 11, 09", confiance="moyenne",
        note="PLUS ÉTROITE que le plan (3'-6\" = 42) : 36 po dans les deux relevés"),
    # ------------------------------------------------------------------------------------------------- sous-sol
    "ouv-SS-002": dict(
        niveau="SS", piece="Séjour", mur="mur-SS-001", axe="x", coord=5.0, facade="avant",
        plan=dict(largeur=75, centre=382, allege=40, tete=86, sections=2),
        video=dict(largeur=72, centre=395, allege=44, tete=TETE, sections=3),
        A=(73, 44, 80, 3, 394), B=(71, 44, 80, 3, 395), images="01 (mesure), 02", confiance="haute",
        note="DÉPLACÉE de +13 po vers l'allée (x 359–431, bord droit aligné sur celui de ouv-RDC-002 comme dans la vidéo ; "
             "plan : axe à 6'-2\" du nu droit, x 344½–419½) ; 3 sections égales ; recoupe sur la 01 : 72,1 po, x 358,2–430,3"),
    "ouv-SS-003": dict(
        niveau="SS", piece="Chambre 2", mur="mur-SS-002", axe="y", coord=451.0, facade="droite",
        plan=dict(largeur=80, centre=308, allege=40, tete=86, sections=2),
        video=dict(largeur=84, centre=None, allege=44, tete=TETE, sections=3),
        A=(80, 44, 80, 3, 310), B=(85, 43, 80, 3, 310), images="03 (seule, de biais)", confiance="moyenne",
        note="fenêtre d'évacuation ; 84 po : A brut 84,4 (ramené à 80 par une correction d'un pixel), B 85, recoupe sur la 03 "
             "(cadre noir sur crépi, homographie du mur) 83,5 ± 1,5 alors que la même mesure redonne 36 po pour ouv-SS-004 et "
             "la porte : la correction de A ne tient pas"),
    "ouv-SS-004": dict(
        niveau="SS", piece="Séjour", mur="mur-SS-002", axe="y", coord=451.0, facade="droite",
        plan=dict(largeur=36, centre=75, allege=40, tete=86, sections=2),
        video=dict(largeur=None, centre=None, allege=44, tete=TETE, sections=2),
        A=(36, 44, 80, 2, 73.5), B=(37, 44, 80, 2, 73), images="03 (seule, de biais)", confiance="moyenne",
        note="largeur et centre du plan confirmés (recoupe 35,7 po, centre 73)"),
}

# fenêtres qu'on ne voit pas dans la vidéo : valeurs actuelles gardées
NON_VISIBLES = {
    "ouv-RDC-006": "salle de bain, mur gauche (x 0) : jamais montré dans la vidéo",
    "ouv-SS-006": "salle de bain, mur gauche : jamais montré",
    "ouv-SS-007": "salle de lavage, mur gauche : jamais montré",
    "ouv-SS-009": "chambre 1, mur arrière : cachée par le deck, son garde-corps et le sofa (10, 11)",
    "ouv-SS-010": "chambre 1, mur arrière : la vidéo n'y dessine AUCUNE fenêtre (11), mais le client confirme qu'elle existe (2026-11-02) : gardée",
}


def retenu(oid):
    """Valeurs retenues d'une fenêtre de la vidéo : {largeur, centre, allege, tete, sections}."""
    f = FENETRES[oid]
    return {k: (f["video"][k] if f["video"].get(k) is not None else f["plan"][k])
            for k in ("largeur", "centre", "allege", "tete", "sections")}


def reglages_3d(niveau):
    """SCENE["fenetres"] du moteur pour un étage : {id: {"allege", "tete", "sections", "note"}}. Sections inégales :
    "sections": 1 (aucun meneau du moteur) et meneaux_3d() pose le meneau au bon endroit."""
    out = {}
    for oid, f in FENETRES.items():
        if f["niveau"] != niveau:
            continue
        r = retenu(oid)
        out[oid] = {"allege": r["allege"], "tete": r["tete"], "sections": 1 if f.get("meneaux") else r["sections"],
                    "note": f"{SOURCE} ({DATE})" + (" ; meneau inégal posé par fenetres_video.meneaux_3d" if f.get("meneaux") else "")}
    return out


def meneaux_3d(niveau, B):
    """Meneaux des fenêtres à sections inégales, comme ceux du moteur (generer_3d.finitions : 1½ po de large, 2½ po de
    profond, centrés sur l'axe du mur, de l'allège à la tête, matériau « metal »). B : constructeur de boîte de la scène."""
    out = []
    for oid, f in FENETRES.items():
        if f["niveau"] != niveau or not f.get("meneaux"):
            continue
        r = retenu(oid)
        a = r["centre"] - r["largeur"] / 2
        for k in f["meneaux"]:
            s = round(a + r["largeur"] * k, 3)
            c = f["coord"]
            if f["axe"] == "x":
                out.append(B(s - 0.75, c - 1.25, s + 0.75, c + 1.25, r["allege"], r["tete"], "metal"))
            else:
                out.append(B(c - 1.25, s - 0.75, c + 1.25, s + 0.75, r["allege"], r["tete"], "metal"))
    return out


def _pipo(v):
    """Pouces → texte pieds-pouces (au ½ po)."""
    v = round(v * 2) / 2
    p, q = divmod(v, 12)
    q = (f"{int(q)}" if q == int(q) else f"{int(q)}½") if q else "0"
    return f"{int(p)}'-{q}\""


def _avert(msg):
    print("fenetres_video : " + msg, file=sys.stderr)


def appliquer_plans(maison):
    """Reporte les fenêtres de la vidéo dans maison.json (plans P-129 / P-130) : largeur et centre (s'ils changent), allège,
    hauteur, note de chaque ouverture, et les chaînes de cotes de façade qui passaient par ses bords ou son axe.
    Modifie maison EN PLACE et le retourne."""
    for niv in maison["niveaux"]:
        murs = {m["id"]: m for m in niv["murs"]}
        ouvs = {o["id"]: o for o in niv["ouvertures"]}
        for oid, f in FENETRES.items():
            if f["niveau"] != niv["id"]:
                continue
            o = ouvs.get(oid)
            if o is None or o.get("type") != "fenetre":
                _avert(f"{oid} introuvable au niveau {niv['id']} : rien appliqué")
                continue
            m = murs[o["mur_id"]]
            L = math.hypot(m["x2"] - m["x1"], m["y2"] - m["y1"])
            ux, uy = (m["x2"] - m["x1"]) / L, (m["y2"] - m["y1"]) / L
            p, r = f["plan"], retenu(oid)
            # garde-fou : l'état de départ doit être celui que la vidéo corrige (sinon quelqu'un l'a changé entre-temps)
            c0 = m["x1"] + ux * o["position"]["valeur"] if f["axe"] == "x" else m["y1"] + uy * o["position"]["valeur"]
            if abs(o["largeur"]["valeur"] - p["largeur"]) > 0.5 or abs(c0 - p["centre"]) > 0.5:
                _avert(f"{oid} : état de départ {o['largeur']['valeur']} po centré à {c0:.1f} ≠ attendu {p['largeur']} "
                       f"centré à {p['centre']} (modifié ailleurs ?) ; la vidéo est appliquée quand même")
            changes = []
            if f["video"].get("largeur") is not None:
                o["largeur"] = {"valeur": r["largeur"], "source": "ESTIMÉ", "photo": None,
                                "note": f"MAISON-18 ({DATE}) : {SOURCE}, captures {f['images']} ; avant {_pipo(p['largeur'])} "
                                        f"({o['largeur'].get('source')}) ; à mesurer sur place"}
                changes.append(f"largeur {p['largeur']} → {r['largeur']} po")
            if f["video"].get("centre") is not None:
                px, py = (r["centre"], f["coord"]) if f["axe"] == "x" else (f["coord"], r["centre"])
                pos = (px - m["x1"]) * ux + (py - m["y1"]) * uy
                o["position"] = {"valeur": round(pos, 3), "source": "ESTIMÉ", "photo": None,
                                 "note": f"MAISON-18 ({DATE}) : axe à {'x' if f['axe'] == 'x' else 'y'} = {r['centre']} "
                                         f"d'après la {SOURCE} (avant {p['centre']}, {(o['position'].get('note') or '').strip()}) ; "
                                         f"écart confirmé par les deux relevés ; à vérifier sur place"}
                changes.append(f"centre {p['centre']} → {r['centre']}")
            o["allege"] = {"valeur": r["allege"], "source": "ESTIMÉ", "photo": None,
                           "note": f"MAISON-18 ({DATE}) : {SOURCE} (captures {f['images']}), depuis le plancher de l'étage ; "
                                   f"avant {p['allege']} po ; à mesurer"}
            o["hauteur"] = {"valeur": r["tete"] - r["allege"], "source": "ESTIMÉ", "photo": None,
                            "note": f"MAISON-18 ({DATE}) : allège {r['allege']} → tête {r['tete']} po (au soffite dans la "
                                    f"vidéo, alignée sur la tête des portes)"}
            changes.append(f"allège {p['allege']} → {r['allege']} ; tête {p['tete']} → {r['tete']} ; "
                           f"sections {p['sections']} → {r['sections']}" + (" inégales" if f.get("meneaux") else ""))
            note = o.get("note") or ""
            k = note.find(" — MAISON-18 : agrandie vers le bas")      # hypothèse de zone_global (allège 40), remplacée
            if k >= 0:
                note = note[:k]
            o["note"] = (note + f" — MAISON-18 ({DATE}, client : « les fenêtres dans la vidéo sont de bonnes dimensions ») : "
                         + " ; ".join(changes) + f". {f['note']}. À mesurer sur place.").strip()
            # chaînes de cotes de la façade : bords et axe déplacés
            if f["video"].get("largeur") is None and f["video"].get("centre") is None:
                continue
            avant = {round(p["centre"] - p["largeur"] / 2, 3): r["centre"] - r["largeur"] / 2,
                     round(p["centre"] + p["largeur"] / 2, 3): r["centre"] + r["largeur"] / 2,
                     round(float(p["centre"]), 3): r["centre"]}
            ax = 0 if f["axe"] == "x" else 1
            for lc in niv.get("lignes_cote") or []:
                if lc.get("facade") != f["facade"]:
                    continue
                p1, p2 = list(lc["p1"]), list(lc["p2"])
                n1, n2 = avant.get(round(p1[ax], 3)), avant.get(round(p2[ax], 3))
                if n1 is None and n2 is None:
                    continue
                old = f"{p1[ax]}→{p2[ax]}" + (f", {lc.get('source')} {lc['ref']} = {lc.get('valeur_attendue')}" if lc.get("ref") else "")
                if n1 is not None:
                    p1[ax] = n1
                if n2 is not None:
                    p2[ax] = n2
                if abs(abs(p2[ax] - p1[ax]) - abs(float(lc["p2"][ax]) - float(lc["p1"][ax]))) < 0.01:
                    lc["p1"], lc["p2"] = p1, p2
                    continue
                lc.update({"p1": p1, "p2": p2, "source": "ESTIMÉ", "ref": None, "valeur_attendue": None,
                           "note": f"MAISON-18 ({DATE}) : {oid} selon la {SOURCE} (avant {old})"})
    return maison
