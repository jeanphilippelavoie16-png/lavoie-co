"""MAISON-18 — RDC, zone « entrée » : la grande entrée ouverte avec le haut de l'escalier (2026-11-02 : plus de murs de
verre, seulement un garde-corps de verre tout autour de l'escalier).

Demandes du client (annotations rouge et jaune sur la feuille P-128 de SS-17, 2026-11-01) :
« Enlève les garde-robes en rouge en haut pour que ça fasse une grosse entrée, et entoure l'entrée de murs de verre côté
cuisine et salon pour que ça soit comme isolé. Fais du rangement dans l'entrée en haut aussi. Fais de quoi de chic et
fonctionnel. » — « Ajoute les marches en haut pour monter et descendre. »

Ce module (appelé par modifs.py et scene_3d.py, après rdc_corrections) :
- enlève la colonne de garde-robes du hall (G.R. de la chambre avant, VEST., LIN.) et ses cloisons, la ligne de porte
  entrée / hall et la cloison hall / salon (et la poutre décorative qui la coiffait) ;
- ferme le vestibule par des murs de verre plancher-plafond à cadres noirs minces : sous la poutre de bois brut de
  l'axe B (y = 157, entre les poteaux C04 et C05, puis jusqu'au coin) côté logement, et le long de l'escalier côté
  salon (x = 272,25, là où SS-17 mettait le mur de la cage) ; une porte vitrée battante de 36 po vers le dégagement ;
- garde la trémie et l'escalier de SS-17 (élément elem-RDC-P-ESC reporté du sous-sol, même x, y, L, W, tournant),
  trémie [234, 14, 270, 134,7] = celle que generer_3d.py calcule pour l'escalier du sous-sol (échappée ≈ 1,96 m au bord) ;
  à deux étages, le moteur troue le plancher et pose le garde-corps de verre ; à un seul étage (ETAGE=RDC), ce module
  dessine le même garde-corps et une trémie sombre ; main courante noire côté salon dans les deux cas ;
- rangement le long du mur du bureau : banc à bottes (cases et bacs d'égouttement, crochets enfants et adultes,
  tablette à bacs), armoire-vestiaire pleine hauteur noir mat, niche-console de chêne (clés, recharge, miroir), DEL.
Pouces, repère de la maison (x le long de la façade, y vers l'arrière, z vers le haut).
"""
import json
import math
import os

from shapely.geometry import Polygon, box
from shapely.geometry.polygon import orient

SOURCE = "proposition MAISON-18 (esquisse) — entrée vitrée"

# ------------------------------------------------------------------------------------------------ repères
XB = 148.25                  # face du mur du bureau (mur-RDC-013, axe x = 146, 4½ po)
XV = 272.25                  # axe du mur de verre côté salon (face intérieure 271,25)
YV = 157                     # axe du mur de verre côté logement, sous la poutre de l'axe B
T_VERRE = 2.0
# ouverture du plancher du RDC (x0, y0, x1, y1) : la trémie que generer_3d.py calcule pour elem-SS-P-ESC (échappée de
# 77 po au-dessus des nez avec le plafond du sous-sol à 96 po) ; c'est elle qui troue le plancher dans la maquette à 2 étages
TREMIE = [234, 14, 270, 134.67]
PORTE_V = (186.75, 222.75)               # porte vitrée battante de 36 po (contre l'habillage du poteau C05)
GARDE_H = 36                             # garde-corps (900 mm min. dans un logement) : celui du moteur ; 42 po en option
# rangement le long du mur du bureau (de l'avant vers l'arrière)
BANC = (10, 64)                          # banc à bottes, 18 po de profond
ARM1 = (64, 100)                         # armoire-vestiaire (2 portes)
NICHE = (100, 124)                       # niche-console ouverte (clés, recharge, miroir)
ARM2 = (124, 154)                        # armoire-vestiaire (2 portes)
P_ARM = 24                               # profondeur des armoires
ZONE = (146.0, 5.0, 273.5, 157.0)        # emprise de la zone (meubles RDC-01 retirés)
# garde-corps autour de la trémie, aux places où le moteur les pose dans la maquette à deux étages (garde_corps_tremies :
# 1¼ po hors du bord, ouvert au haut de la volée y 12 → 52, rien le long du mur avant ni du mur de verre)
GC = [((TREMIE[0] - 1.25, 52.0), (TREMIE[0] - 1.25, TREMIE[3])), ((TREMIE[0], TREMIE[3] + 1.25), (TREMIE[2], TREMIE[3] + 1.25)),
      ((TREMIE[2] + 1.25, 10.0), (TREMIE[2] + 1.25, TREMIE[3] + 1.25))]          # côté salon (plus de mur de verre, 2026-11-02)
GC_NOM = "Garde-corps de verre clair, poteaux d'acier noir, main courante de chêne (36 po ; 42 po en option)"

MURS_RETIRES = ["mur-RDC-014", "mur-RDC-015", "mur-RDC-016", "mur-RDC-017", "mur-RDC-018"]
OUV_RETIREES = ["ouv-RDC-011", "ouv-RDC-021", "ouv-RDC-022"]
PIECES_RETIREES = ["piece-RDC-HALL", "piece-RDC-VES", "piece-RDC-GRA", "piece-RDC-LIN"]


def dim(v, note=None, src="PRÉSUMÉ"):
    d = {"valeur": v, "source": src, "photo": None}
    if note:
        d["note"] = note
    return d


def _mur_verre(mid, x1, y1, x2, y2, role):
    return {"id": mid, "type": "int", "etat": "nouveau", "porteur": "non", "indices_porteur": [],
            "epaisseur": dim(T_VERRE, "mur de verre trempé feuilleté plancher-plafond, cadre d'aluminium noir mat de 1¾ po"),
            "x1": x1, "y1": y1, "x2": x2, "y2": y2, "materiau": "verre", "source_position": "PRÉSUMÉ",
            "note": f"Mur de verre projeté — {role} ({SOURCE})."}


def _element(eid, typ, nom, lib, x, y, rot, L, W, note=None):
    e = {"id": eid, "type": typ, "nom": nom, "nom_original": None, "etat": "nouveau",
         "position": {"x": x, "y": y, "rotation_deg": rot, "source": "PRÉSUMÉ"},
         "dimensions": {"longueur": dim(L), "largeur": dim(W)}, "note": note or SOURCE}
    if lib is not None:
        e["libelle"] = lib
    return e


def _piece(pieces, pid, nom, P, desc):
    P = orient(P.simplify(0.01), 1.0)
    x0, y0, x1, y1 = P.bounds
    d = {"id": pid, "nom": nom, "nom_original": None, "etat": "nouveau", "description": desc,
         "polygone": [[round(a, 2), round(b, 2)] for a, b in list(P.exterior.coords)[:-1]],
         "superficie": dim(round(P.area / 144, 1), "aire du polygone au nu des murs", "DÉDUIT"),
         "dimensions": {"x": dim(round(x1 - x0, 2), None, "DÉDUIT"), "y": dim(round(y1 - y0, 2), None, "DÉDUIT")}}
    vieux = next((p for p in pieces if p["id"] == pid), None)
    if vieux:
        for k in ("hauteur_plafond",):
            if k in vieux:
                d[k] = vieux[k]
        pieces[pieces.index(vieux)] = d
    else:
        pieces.append(d)
    return d


# =============================================================================================== plan (maison.json)
def appliquer_modifs_rdc(maison, ctx):
    rdc = ctx["rdc"]
    # 1) garde-robes du hall (G.R. de la chambre avant, VEST., LIN.), ligne de porte entrée / hall, cloison hall / salon
    partis = [m for m in rdc["murs"] if m["id"] in MURS_RETIRES]
    rdc["murs"] = [m for m in rdc["murs"] if m["id"] not in MURS_RETIRES]
    ouv_parties = [o for o in rdc["ouvertures"] if o["id"] in OUV_RETIREES or o["mur_id"] in MURS_RETIRES]
    rdc["ouvertures"] = [o for o in rdc["ouvertures"] if o not in ouv_parties]
    # cloison dégagement / LIN. : ne garde que la partie bureau (x 108 → 146), la lingerie disparaît
    for m in rdc["murs"]:
        if m["id"] == "mur-RDC-012" and max(m["x1"], m["x2"]) > 146:
            if m["x2"] >= m["x1"]:
                m["x2"] = 146
            else:
                m["x1"] = 146
            m["note"] = (m.get("note") or "") + " — raccourcie à x = 146 : la lingerie (LIN.) est enlevée (" + SOURCE + ")."
            L = abs(m["x2"] - m["x1"])
            for o in [o for o in rdc["ouvertures"] if o["mur_id"] == m["id"]]:
                if o["position"]["valeur"] + o["largeur"]["valeur"] / 2 > L + 0.01:
                    rdc["ouvertures"].remove(o)
                    ouv_parties.append(o)
    for m in partis:
        m["note"] = (m.get("note") or "") + " — ENLEVÉE : grande entrée vitrée (" + SOURCE + ")."
    rdc.setdefault("murs_retires", []).extend(partis)
    rdc.setdefault("ouvertures_retirees", []).extend(ouv_parties)
    # poutre apparente qui coiffait le bout de la cloison hall / salon : sans la cloison, elle n'a plus d'appui
    parties = [s for s in rdc["structure"] if s["id"] == "str-RDC-R01"]
    for s in parties:
        s["note"] = (s.get("note") or "") + (" — ENLEVÉE avec la cloison hall / salon ; si elle se révèle porteuse à "
                                             "l'ouverture du plafond, la reprendre (ingénieur) — " + SOURCE + ".")
    rdc["structure"] = [s for s in rdc["structure"] if s["id"] != "str-RDC-R01"]
    rdc.setdefault("structure_retiree", []).extend(parties)

    # 2) (2026-11-02) le client ne veut plus de murs de verre : l'entrée reste ouverte sur le salon et le dégagement ;
    #    seul l'escalier est entouré d'un garde-corps de verre (3 côtés, ouvert à l'arrivée en haut de la volée)
    rdc["murs"] = [m for m in rdc["murs"] if m["id"] not in ("mur-RDC-E01", "mur-RDC-E02", "mur-RDC-E03")]
    rdc["ouvertures"] = [o for o in rdc["ouvertures"] if o["id"] != "ouv-RDC-E01"]
    # porte d'entrée : pentures à gauche (comme SS-17) : elle s'ouvre contre le banc, le haut de l'escalier reste dégagé
    for o in rdc["ouvertures"]:
        if o["id"] == "ouv-RDC-010":
            o["fermee"] = True                    # dessinée fermée dans la maquette (on l'ouvre en la touchant)
            o["sens"] = dict(o.get("sens") or {}, charniere="debut", ouvre_vers="gauche",
                             note="pentures à gauche : la porte s'ouvre contre le banc ; 42 po libres devant la porte et "
                                  "au haut de l'escalier — " + SOURCE)

    # 3) escalier : même volée que le sous-sol (elem-SS-P-ESC) ; au RDC on voit le haut (DESCEND) et la trémie
    esc = next((e for e in rdc["elements"] if e["id"] == "elem-RDC-P-ESC"), None)
    if esc is None:
        src = next((e for e in ctx["rdc_ss17"]["elements"] if e["type"] == "escalier"), None)
        if src is not None:
            import copy
            esc = copy.deepcopy(src)
            rdc["elements"].append(esc)
    if esc is not None:
        es = esc.setdefault("escalier", {})
        es["fleche"], es["direction"] = "DESCEND", "+y"
        es["tremie"] = list(TREMIE)
        esc["note"] = (esc.get("note") or "") + (
            " — RDC (entrée vitrée) : trémie d'environ 36 × 121 po (x 234 → 270, y 14 → 134,7) ; échappée ≈ 77 po "
            "(1,96 m) au bord de la trémie avec le plafond du sous-sol à 8 pi ; largeur 36 po ; garde-corps de verre "
            "(36 po min., 42 po en option) sur les trois côtés libres de la trémie (entrée, bout, salon), ouvert à "
            "l'arrivée ; main courante continue côté salon — à valider (" + SOURCE + ").")
    rdc["tremies"] = [t for t in rdc.get("tremies", []) if t.get("id") != "tremie-RDC-ESC"] + [
        {"id": "tremie-RDC-ESC", "rect": list(TREMIE), "element": "elem-RDC-P-ESC",
         "note": "ouverture du plancher du RDC au-dessus de l'escalier du sous-sol (chevêtres et solives doublées : ingénieur)"}]

    # 4) éléments de la zone : rangement, garde-corps
    els = [
        _element("elem-RDC-E-BANC", "autre", "Banc à bottes de chêne : 3 cases à bottes avec bacs d'égouttement, coussin, "
                 "dossier de lattes de chêne, crochets enfants (40 po) et adultes (64 po), tablette à 4 bacs, caisson haut",
                 "BANC", XB + 9, (BANC[0] + BANC[1]) / 2, 270, BANC[1] - BANC[0], 18),
        _element("elem-RDC-E-ARM1", "armoires", "Armoire-vestiaire pleine hauteur, portes noir mat, tringle et tablettes",
                 None, XB + P_ARM / 2, (ARM1[0] + ARM1[1]) / 2, 270, ARM1[1] - ARM1[0], P_ARM),
        _element("elem-RDC-E-CONS", "comptoir", "Niche-console ouverte de chêne : tiroir de recharge (USB-C), plateau à clés, "
                 "miroir, DEL ; armoires noires dessus et dessous", "", XB + P_ARM / 2, (NICHE[0] + NICHE[1]) / 2, 270,
                 NICHE[1] - NICHE[0], P_ARM),
        _element("elem-RDC-E-ARM2", "armoires", "Armoire-vestiaire pleine hauteur, portes noir mat (manteaux des garçons, "
                 "sacs, aspirateur)", None, XB + P_ARM / 2, (ARM2[0] + ARM2[1]) / 2, 270, ARM2[1] - ARM2[0], P_ARM),
        _element("elem-RDC-E-GC1", "autre", GC_NOM + " (côté entrée)", "", GC[0][0][0], (GC[0][0][1] + GC[0][1][1]) / 2, 90,
                 GC[0][1][1] - GC[0][0][1], 1.5),
        _element("elem-RDC-E-GC2", "autre", GC_NOM + " (bout de la trémie)", "", (GC[1][0][0] + GC[1][1][0]) / 2, GC[1][0][1], 0,
                 GC[1][1][0] - GC[1][0][0], 1.5),
        _element("elem-RDC-E-GC3", "autre", GC_NOM + " (côté salon)", "", GC[2][0][0], (GC[2][0][1] + GC[2][1][1]) / 2, 90,
                 GC[2][1][1] - GC[2][0][1], 1.5),
    ]
    ids = {e["id"] for e in els}
    rdc["elements"] = [e for e in rdc["elements"] if e["id"] not in ids] + els
    rdc["elements"].sort(key=lambda e: e["id"])

    # 5) pièces : une seule « Entrée » (hall, entrée, vestibule, garde-robes, lingerie réunis), zone ouverte sur le salon
    #    et le dégagement (limites sans mur, le long de la poutre de l'axe B et du garde-corps côté salon)
    pieces = rdc["pieces"]
    rdc["pieces"] = pieces = [p for p in pieces if p["id"] not in PIECES_RETIREES]
    ent = box(XB, 10, XV, YV)       # trémie comprise (le moteur la troue à 2 étages)
    _piece(pieces, "piece-RDC-ENT", "Entrée", ent,
           "Grande entrée ouverte (trémie de l'escalier comprise) : porte d'entrée, haut de l'escalier du sous-sol entouré d'un "
           "garde-corps de verre, banc à bottes, armoires-vestiaires et niche-console ; ouverte sur le salon et le dégagement — " + SOURCE)
    for p in pieces:
        P = Polygon(p["polygone"])
        if p["id"] == "piece-RDC-SAL":
            P = P.difference(box(0, 0, XV, YV))
        elif p["id"] == "piece-RDC-DEG":
            P = P.union(box(146, YV, 177.25, 159.25)).difference(box(146, 140, XV, YV))
        else:
            continue
        if P.geom_type != "Polygon":
            P = max(P.geoms, key=lambda g: g.area)
        _piece(pieces, p["id"], p["nom"], P, p.get("description") or p["nom"])

    # 6) note du cartouche (une seule ; le détail est dans DESIGN_entree.md)
    rdc["notes"] = [n for n in rdc.get("notes", []) if n.get("id") != "note-RDC-E01"] + [
        {"id": "note-RDC-E01", "texte_original": None, "photo": None,
         "interpretation": "Grande entrée ouverte : garde-robes enlevées, trémie entourée d'un garde-corps de verre ; "
                           "structure, échappée et coupe-feu à valider avec la Ville et un professionnel."}]


# =============================================================================================== 3D (SCENE du RDC)
def _bornes(o):
    """Emprise en plan (x0, y0, x1, y1) d'un objet de la scène, ou None."""
    if "x0" in o and "y0" in o and "x1" in o and "y1" in o:
        return o["x0"], o["y0"], o["x1"], o["y1"]
    if o.get("forme") == "tube" and o.get("pts"):
        xs, ys = [p[0] for p in o["pts"]], [p[1] for p in o["pts"]]
        return min(xs), min(ys), max(xs), max(ys)
    if o.get("forme") == "cylindre":
        r = o.get("r", 0)
        if o.get("axe") == "y":
            return o["x"] - r, o["y0"], o["x"] + r, o["y1"]
        if o.get("axe") == "x":
            return o["x0"], o["y"] - r, o["x1"], o["y"] + r
        return o["x"] - r, o["y"] - r, o["x"] + r, o["y"] + r
    if "x" in o and "y" in o:
        r = o.get("R", o.get("r", 0)) if o.get("forme") in ("tore", "sphere") else 0
        return o["x"] - r, o["y"] - r, o["x"] + r, o["y"] + r
    return None


def _dans_zone(o):
    b = _bornes(o)
    if b is None:
        return False
    x0, y0, x1, y1 = ZONE
    return b[0] < x1 - 0.01 and b[2] > x0 + 0.01 and b[1] < y1 - 0.01 and b[3] > y0 + 0.01


def _banc(h):
    B, A, T = h.B, h.A, h.T
    y0, y1 = BANC
    out = []
    # socle noir en retrait, 3 cases à bottes (fond de chêne, bacs d'égouttement de caoutchouc noir), assise de chêne
    out += [B(XB, y0, XB + 15.5, y1, 0, 3, "carbone"), A(XB, y0, XB + 18, y1, 3, 4, "placage", r=0.3, b=0.2)]
    cases = [(y0 + 0.75 + k * (y1 - y0 - 1.5) / 3, y0 + 0.75 + (k + 1) * (y1 - y0 - 1.5) / 3) for k in range(3)]
    for a, b in cases:
        out += [A(XB + 0.5, a + 0.6, XB + 17.5, b - 0.6, 4, 4.8, "caoutchouc-noir", r=1, b=0.3)]
    out += [B(XB, y, XB + 18, y + 0.75, 4, 15.5, "placage") for y in (y0, y0 + (y1 - y0) / 3 - 0.375, y0 + 2 * (y1 - y0) / 3 - 0.375, y1 - 0.75)]
    out += [A(XB, y0, XB + 18, y1, 15.5, 17, "placage", r=0.4, b=0.3), A(XB + 0.5, y0 + 0.5, XB + 17.5, y1 - 0.5, 17, 19.25, "cuir", r=1.2, b=0.8)]
    # bottes d'hiver : deux paires d'adultes, deux paires d'enfants (une case vide pour sécher)
    for (a, b), paires in zip(cases, ((("carbone", 13), ("cuir", 13)), (("rouge-velo", 9), ("jete", 9)), ())):
        for k, (mat, hz) in enumerate(paires):
            yy = a + 2 + k * (b - a - 4) / 2
            out += [A(XB + 3, yy, XB + 14, yy + 3.6, 4.8, 4.8 + hz * 0.45, mat, r=1.4, b=0.6),
                    A(XB + 3, yy + 4.2, XB + 14, yy + 7.8, 4.8, 4.8 + hz * 0.45, mat, r=1.4, b=0.6)]
    # dossier de lattes de chêne (rainures sombres), crochets noirs : enfants à 40 po, adultes à 64 po
    out += [B(XB, y0, XB + 0.9, y1, 19.25, 84, "placage")]
    out += [B(XB + 0.9, y - 0.12, XB + 1.05, y + 0.12, 19.25, 72, "carbone") for y in [y0 + 3 * k for k in range(1, int((y1 - y0) / 3))]]
    for z, ys in ((40, [y0 + 8 + 9.5 * k for k in range(5)]), (64, [y0 + 11 + 11 * k for k in range(4)])):
        for y in ys:
            out += [T([(XB + 0.9, y, z), (XB + 3.2, y, z), (XB + 3.6, y, z + 1.6)], 0.32, "metal", bouts=True),
                    B(XB + 0.9, y - 0.9, XB + 1.3, y + 0.9, z - 1.2, z + 1.2, "metal")]
    # manteaux accrochés : deux petits (garçons), un d'adulte ; tuques et mitaines dans les bacs
    for yc, zb, zh, mat, w in ((y0 + 8, 23, 40.5, "osier", 4.5), (y0 + 27, 22, 40.5, "jete", 4.5), (y0 + 44, 31, 64.5, "tissu", 6.5)):
        out += [A(XB + 1.2, yc - w, XB + 5.4, yc + w, zb, zh - 3.5, mat, r=1.2, b=0.8),
                A(XB + 1.2, yc - w + 1.5, XB + 4.6, yc + w - 1.5, zh - 4, zh, mat, r=1.2, b=0.8)]
    # tablette de chêne à 72 po (14 po), 4 bacs (un par membre de la famille), ruban DEL dessous, caisson haut noir
    out += [A(XB, y0, XB + 14, y1, 72, 73.5, "placage", r=0.3, b=0.2), B(XB + 12.8, y0 + 1, XB + 13.3, y1 - 1, 71.75, 72, "spot")]
    lb = (y1 - y0 - 2.5) / 4
    for k, mat in enumerate(("osier", "tissu", "osier", "tissu")):
        a = y0 + 1 + k * (lb + 0.17)
        out += [A(XB + 1, a, XB + 13, a + lb, 73.5, 81.5, mat, r=1, b=0.5, trou=0.5)]
    out += [A(XB, y0, XB + P_ARM, y1, 84, 95.9, "noir-mat", r=0.2, b=0.2), B(XB + P_ARM, y0 + (y1 - y0) / 2 - 0.12, XB + P_ARM + 0.15, y0 + (y1 - y0) / 2 + 0.12, 84.5, 95.5, "carbone")]
    # joue pleine hauteur entre le banc et l'armoire (noir mat)
    out += [A(XB, y1 - 0.75, XB + P_ARM, y1, 0, 84, "noir-mat", r=0.2, b=0.15)]
    return out


def _armoire(h, ya, yb, portes):
    """Armoire-vestiaire pleine hauteur noir mat, plinthe en retrait, portes avec joints et tirettes de chêne."""
    B, A = h.B, h.A
    xf = XB + P_ARM
    out = [B(XB, ya, xf - 3, yb, 0, 3.5, "carbone"), A(XB, ya, xf, yb, 3.5, 95.9, "noir-mat", r=0.2, b=0.2)]
    w = (yb - ya) / portes
    for k in range(1, portes):
        out.append(B(xf - 0.05, ya + k * w - 0.12, xf + 0.1, ya + k * w + 0.12, 4, 95.5, "carbone"))
    out.append(B(xf - 0.05, ya, xf + 0.1, yb, 83.9, 84.1, "carbone"))            # porte haute (rangement d'été)
    for k in range(portes):
        yp = ya + (k + 0.5) * w + (w / 2 - 2.2) * (1 if k % 2 == 0 else -1)
        out.append(A(xf, yp - 0.5, xf + 1.1, yp + 0.5, 30, 62, "placage", r=0.3, b=0.2))   # tirette longue de chêne
    return out


def _niche(h):
    B, A, C = h.B, h.A, h.C
    ya, yb = NICHE
    xf = XB + P_ARM
    out = [B(XB, ya, xf - 3, yb, 0, 3.5, "carbone"), A(XB, ya, xf, yb, 3.5, 30, "noir-mat", r=0.2, b=0.2),
           A(XB, ya, xf, yb, 30, 35.5, "noir-mat", r=0.2, b=0.2),                                   # tiroir de recharge
           A(xf, (ya + yb) / 2 - 3, xf + 0.9, (ya + yb) / 2 + 3, 32.2, 33.2, "placage", r=0.3, b=0.2),
           A(XB, ya - 0.5, xf + 1, yb + 0.5, 35.5, 37, "placage", r=0.3, b=0.25),                     # tablette de chêne
           B(XB, ya, xf, ya + 0.75, 37, 76, "placage"), B(XB, yb - 0.75, xf, yb, 37, 76, "placage"),
           B(XB, ya, XB + 0.75, yb, 37, 76, "placage"), B(XB, ya, xf, yb, 75.25, 76, "placage"),
           B(XB + 0.75, ya + 2, XB + 1.0, yb - 2, 41, 73, "miroir"),                                 # miroir au fond
           B(xf - 3, ya + 1, xf - 2.5, yb - 1, 74.9, 75.25, "spot"),                                 # ruban DEL
           A(XB, ya, xf, yb, 76, 95.9, "noir-mat", r=0.2, b=0.2)]
    # plateau à clés (cuir), téléphone sur le chargeur, petit vase
    out += [A(XB + 9, ya + 3, XB + 17, ya + 11, 37, 37.6, "cuir", r=1.5, b=0.3),
            A(XB + 10, ya + 14, XB + 13.2, ya + 20.5, 37, 37.4, "ecran", r=0.6, b=0.15),
            C(XB + 6, yb - 5, 2.2, 37, 45, "blanc", r2=1.6, pans=24)]
    return out


def _garde_corps(h):
    """Maquette d'un seul étage seulement : le garde-corps que le moteur pose autour de la trémie dans la maquette à deux
    étages (generer_3d.garde_corps : verre clair, poteaux d'acier noir au plus 48 po d'entraxe, main courante de chêne)."""
    B = h.B
    out = []
    for (xa, ya), (xb, yb) in GC:
        horiz = abs(ya - yb) < 0.01
        lo, hi = sorted([xa, xb] if horiz else [ya, yb])
        f = ya if horiz else xa
        r = (lambda u0, u1, v0, v1, z0, z1, mat: B(u0, f + v0, u1, f + v1, z0, z1, mat)) if horiz else \
            (lambda u0, u1, v0, v1, z0, z1, mat: B(f + v0, u0, f + v1, u1, z0, z1, mat))
        n = max(1, math.ceil((hi - lo) / 48))
        for k in range(n + 1):
            u = lo + (hi - lo) * k / n
            out.append(r(max(lo, u - 1), min(hi, u + 1), -1, 1, 0, GARDE_H - 1.5, "metal"))
        out += [r(lo, hi, -0.25, 0.25, 2, GARDE_H - 2, "verre-clair"), r(lo, hi, -0.6, 0.6, 1, 2, "metal"),
                r(lo, hi, -1.25, 1.25, GARDE_H - 1.5, GARDE_H, "placage")]
    return out


def _main_courante(h):
    """Main courante ronde noire (Ø 1½ po) côté salon, continue du palier jusqu'au sous-sol : 36 po au-dessus des nez,
    le long du mur avant (marches tournantes) puis du mur de verre (pinces sur les montants) ; sous le plancher, elle va
    rejoindre celle du sous-sol. Veilleuse DEL sous le garde-corps, côté trémie."""
    B, T = h.B, h.T
    x0, y0, x1, y1 = TREMIE
    xr, yr = x1 - 1.25, 12.25
    zl = lambda y: 0.75 * (150 - y) - 61.5                   # 36 po au-dessus de la ligne des nez (volée droite)
    pts = [(229.0, yr, 36.0), (244.0, yr, 28.5), (258.0, yr, 21.5), (xr, yr + 1.5, 19.0), (xr, 29.0, 15.5), (xr, 50.0, 13.5),
           (xr, 68.0, zl(68.0)), (271.0, 80.3, zl(80.3))]
    out = [T(pts, 0.75, "metal", bouts=True)]
    out += [B(236.5, 10, 237.5, yr, 31.0, 32.0, "metal"), B(253.5, 10, 254.5, yr, 23.6, 24.6, "metal"),
            B(xr, 39.5, TREMIE[2] + 0.6, 40.5, 13.8, 14.8, "metal")]               # console vers le garde-corps côté salon
    out += [B(x0, 53, x0 + 0.15, y1, 0.4, 0.8, "spot"), B(x0 + 0.5, y1 - 0.15, x1 - 0.5, y1, 0.4, 0.8, "spot")]
    return out


def _tremie_seule(h):
    """Maquette d'un seul étage (ETAGE=RDC) : le plancher du dessous n'existe pas ; l'ouverture est rendue sombre, avec
    les nez des marches qui descendent tracés en chêne (la vraie volée est celle du sous-sol, dans la maquette à deux étages)."""
    B = h.B
    x0, y0, x1, y1 = TREMIE
    out = [B(x0, y0, x1, y1, 0.0, 0.004, "carbone")]
    out += [B(234, y - 0.5, 270, y + 0.5, 0.004, 0.05, "placage") for y in range(60, 135, 10)]
    for k in (1, 2):                                            # rayons des marches tournantes (pivot 234, 50)
        a = math.radians(30 * k)
        dx, dy = math.cos(a), -math.sin(a)
        t = min(36 / dx if dx > 1e-6 else 1e9, 36 / -dy if dy < -1e-6 else 1e9)
        L = t
        n = 12
        for i in range(n):
            px, py = 234 + dx * L * (i + 0.5) / n, 50 + dy * L * (i + 0.5) / n
            out.append(B(px - 1.6, py - 1.6, px + 1.6, py + 1.6, 0.004, 0.05, "placage"))
    out += [B(234, 49.5, 270, 50.5, 0.004, 0.05, "placage")]
    return out


def appliquer_scene_rdc(S, h):
    B, A, C, T, MOD = h.B, h.A, h.C, h.T, h.MOD
    seul = os.environ.get("ETAGE") == "RDC"
    # meubles RDC-01 de la zone (hall, entrée, cadres, banc, vieille porte) et tout le sectionnel du salon, qui passait
    # sous la volée et le mur de verre
    sect = {json.dumps(o, sort_keys=True) for o in h.sectionnel()} if hasattr(h, "sectionnel") else set()
    S["mobilier"] = [o for o in S["mobilier"] if not _dans_zone(o) and json.dumps(o, sort_keys=True) not in sect]
    R = []
    for o in S.get("revetements", []):
        if o.get("mat") == "crepi" and "x0" in o and o["x0"] < XV + 1:          # crépi : salon seulement
            o = dict(o, x0=XV + T_VERRE / 2)
        if _dans_zone(o) and o.get("mat") != "crepi":
            continue
        R.append(o)
    S["revetements"] = R
    M = []
    # sectionnel du client replacé dans le salon, dos au garde-corps de l'escalier (même meuble, décalé de 52 po)
    if hasattr(h, "sectionnel"):
        for o in h.sectionnel():
            o = dict(o)
            if "x0" in o:
                o["x0"], o["x1"] = o["x0"] + 52, o["x1"] + 52
            M.append(o)
    # rangement le long du mur du bureau
    M += _banc(h) + _armoire(h, *ARM1, 2) + _niche(h) + _armoire(h, *ARM2, 2)
    # main courante ; garde-corps et trémie sombre dans la maquette d'un seul étage (à deux étages, le moteur troue le
    # plancher à la trémie de l'escalier du sous-sol et pose lui-même le garde-corps aux mêmes places)
    M += _main_courante(h)
    if seul:
        M += _garde_corps(h) + _tremie_seule(h)
    tp = S.setdefault("tremies_plancher", [])           # demande au moteur (trou du plancher dans une maquette d'un étage)
    if list(TREMIE) not in tp:
        tp.append(list(TREMIE))
    # tapis-grattoir encastré devant la porte (cadre d'acier noir), tapis de passage vers la porte vitrée
    M += [B(182, 10, 216, 40, 0, 0.12, "metal"), A(182.75, 10.5, 215.25, 39.25, 0.1, 0.3, "caoutchouc-noir", r=0.3, b=0.1),
          A(186, 62, 220, 140, 0, 0.4, "tissu", r=2, b=0.2)]
    # applique noire à côté de la porte (entre la porte et l'escalier), suspension globe au centre, encastrés
    M += [B(223.5, 10, 226.5, 11.2, 63, 77, "metal"), A(222.6, 11.2, 227.4, 15.6, 65, 75, "abat-jour", r=2.2, b=0.8)]
    M += [C(204, 96, 2.6, 95.2, 96, "metal", pans=32), T([(204, 96, 95.2), (204, 96, 92.5)], 0.12, "metal"),
          C(204, 96, 1.4, 90.8, 92.6, "metal", pans=24), {"forme": "sphere", "x": 204, "y": 96, "z": 85.0, "r": 6.5, "mat": "abat-jour"}]
    # grande plante derrière la trémie (vue du salon et du dégagement à travers le verre)
    M += [MOD("plante_sansevieria", 258, 146, H=38), C(258, 146, 6.5, 0, 10, "carbone", pans=32)]
    S["mobilier"] += M
    # lumières : celles du hall et de l'entrée RDC-01 sont remplacées
    S["lumieres"] = [l for l in S.get("lumieres", []) if not (ZONE[0] <= l["x"] <= ZONE[2] and ZONE[1] <= l["y"] <= ZONE[3])]
    S["lumieres"] += [{"x": 200, "y": 34}, {"x": 200, "y": 134}, {"x": 252, "y": 30}, {"x": 252, "y": 104},
                      {"x": 204, "y": 96, "z": 85, "i": 4}, {"x": 225, "y": 14, "z": 72, "i": 2}, {"x": 166, "y": 112, "z": 70, "i": 2}]
    # peinture et sol : ardoise noire dans toute l'entrée, murs vert sauge (existant), plafond blanc
    S.setdefault("sols", {})["piece-RDC-ENT"] = "ardoise_noire"
    pe = S.setdefault("peinture", {})
    pe.pop("piece-RDC-HALL", None)
    pe["piece-RDC-ENT"] = "Vert sauge"
    # visite : arrêts de l'entrée au début, l'arrêt du salon renommé
    vis = [v for v in S.get("visites", []) if v.get("nom") not in ("Entrée avant", "Hall (mur de cadres)")]
    for v in vis:
        if v.get("nom") == "Salon vers le hall":
            v["nom"] = "Salon vers l'entrée"
    S["visites"] = [{"nom": "Entrée", "x": 200, "y": 30, "cap": 92},
                    {"nom": "Entrée — banc et vestiaire", "x": 222, "y": 132, "cap": 222},
                    {"nom": "Entrée vue du dégagement", "x": 214, "y": 214, "cap": 262}] + vis
    S["depart"] = {"x": 200, "y": 30, "cap": 92}
    pal = [p for p in S.get("palette", []) if p[0] != "Hall"]
    pal.insert(min(3, len(pal)), ["Entrée", "grande entrée ouverte sur le salon et le dégagement, ardoise noire ; escalier entouré "
                                  "d'un garde-corps de verre clair (poteaux noirs, main courante de chêne) ; banc de chêne, armoires "
                                  "noir mat, niche-console de chêne et miroir", "#2B2F2E"])
    S["palette"] = pal
