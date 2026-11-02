"""MAISON-18 — chute à linge de la salle de bain du haut jusqu'à la salle de lavage du sous-sol (client, 2026-11-02).

Demande du client, mot pour mot : « dans la salle de bain en haut où on a enlevé la laveuse sécheuse, c'est-tu possible de
faire une drop pour envoyer du linge dans la salle de lavage? pi j'aimerais que ça soit possible de l'essayer sur notre
outil. »

Parti pris (l'option B de DESIGN_cafe_sdb.md devient le choix dessiné ; conditions à valider : DESIGN_chute_linge.md) :
- RDC : trappe basculante noir mat « LINGE » dans le module de gauche de la colonne d'apothicaire (rdc_cafe_sdb.py, qui
  dessine la colonne et la trappe fermée) ; bouche de 12 × 12 po, seuil à 40 po, loquet enfant, fermeture automatique.
  Gaine de tôle galvanisée de 12 × 14 po (intérieur) au fond du module, ENCOFFRÉE dans la colonne jusqu'au plancher.
- Plancher : la gaine descend entre deux solives (2 × 10 parallèles à y) et se décale de 5¼ po vers l'avant (y) sous la
  cloison du fond de la salle de bain (mur-RDC-R01, y = 142, ESTIMÉE) pour sortir au plafond du lavage devant la poutre
  maîtresse (str-SS-P02, y 153 → 161) : sortie x 77,6 → 89,6, y 139 → 153.
- Sous-sol : rien d'encoffré ; la sortie au plafond porte une collerette et un COUDE-DÉFLECTEUR d'inox brossé Ø 14 po,
  APPARENT, qui passe au-dessus de l'arc de la porte du lavage (dessous à 83 po au droit de la porte, qui fait 80 po) et
  renvoie le linge 27 po vers la gauche, dans un chariot à linge roulant (cadre d'acier noir, sac de toile écrue, 20 × 14 ×
  33 po) entre le chauffe-eau et l'arc de la porte, hors du dégagement du panneau électrique.
- Plans : symbole « CHUTE » aux deux niveaux (gaine au RDC, sortie et déflecteur en pointillé au SS : au-dessus), note de
  la proposition sur P-129 (celles de P-130 sont fixées dans modifs.py) ; le chariot, meuble roulant, n'est pas au plan.
- 3D (maquette à deux étages) : SCENE["sequences"] — trappe, ballot de linge froissé, chute, glissade dans le déflecteur,
  arrivée dans le chariot ; boutons « Envoyer du linge » (deux étages) et « Voir arriver au lavage » ; arrêts « Chute à
  linge » (RDC) et « Chute à linge — arrivée au lavage » (SS). Avec ETAGE=RDC ou SS, pas de séquence (la trappe reste fixe).
Ne touche à aucun autre module du sous-sol : rien du lavage n'est déplacé (le chariot loge dans un coin libre).
Pouces, repère de la maison (x le long de la façade, y vers l'arrière) ; z depuis le plancher de chaque étage, sauf dans
la séquence (z absolu : plancher du sous-sol = 0).
"""
import importlib.util
import os

ICI = os.path.dirname(os.path.abspath(__file__))
SOURCE = "proposition MAISON-18 (esquisse) — chute à linge (client, 2026-11-02)"


def _cafe():
    spec = importlib.util.spec_from_file_location("m18_chute_cafe_sdb", os.path.join(ICI, "rdc_cafe_sdb.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


CAFE = _cafe()
XC = CAFE.XC_CHUTE                       # axe de la chute en x (83,63)
GAINE_RDC = CAFE.GAINE                   # x0, x1, y0, y1 : gaine au fond du module de gauche de la colonne (RDC)
PLAFOND_SS = 96.0
YS = 146.0                               # axe de la sortie et du déflecteur en y
SORTIE = (XC - 6.0, XC + 6.0, YS - 7.0, YS + 7.0)        # sortie au plafond du lavage : 12 × 14 po, devant la poutre (y 153)
R_DEF = 7.0                                              # coude-déflecteur d'inox, Ø 14 po
X_BEC = 57.0                                             # axe du bec vertical du déflecteur, au-dessus du chariot
Z_BEC = 69.0                                             # bas du bec
# axe du coude-déflecteur (z du sous-sol) : vertical sous la sortie, pente de 32 à 40° vers -x, bec vertical
AXE_DEF = [(XC, YS, 97.5), (XC, YS, 94.0), (77.0, YS, 89.6), (66.0, YS, 82.4), (59.5, YS, 76.6), (X_BEC, YS, 72.5), (X_BEC, YS, Z_BEC)]
CHARIOT = (47.0, 140.0, 67.0, 154.0)                     # cadre du chariot à linge (x 47 → 67, y 140 → 154 : 20 × 14 po)
TOILE = "draps"                                          # sac de toile écrue
Z_SAC = 13.5                                             # dessus du fond du sac (sac de 19 po suspendu au cadre)
PORTE_LAVAGE = {"pivot": (109.75, 149.5), "rayon": 30.0, "haut": 80.0}   # ouv-SS-P02, s'ouvre vers le lavage


# ------------------------------------------------------------------------------------------------ plan (maison.json)
def _element(eid, typ, nom, lib, x, y, L, W, note=None):
    d = lambda v: {"valeur": round(v, 2), "source": "PRÉSUMÉ", "photo": None}
    return {"id": eid, "type": typ, "nom": nom, "nom_original": None, "etat": "nouveau", "libelle": lib,
            "position": {"x": round(x, 3), "y": round(y, 3), "rotation_deg": 0, "source": "PRÉSUMÉ"},
            "dimensions": {"longueur": d(L), "largeur": d(W)}, "note": note or SOURCE}


NOTE_SS = ("Chute à linge (salle de bain du haut → plafond du lavage) : déflecteur inox, chariot ; cloison, solives et "
           "coupe-feu à valider.")


def appliquer_modifs_rdc(maison, ctx):
    rdc, ss = ctx["rdc"], ctx["ss"]
    gx0, gx1, gy0, gy1 = GAINE_RDC
    e_rdc = _element("elem-RDC-S-CHUTE", "event",
                     "Chute à linge : gaine de tôle galvanisée de 12 × 14 po (intérieur) encoffrée dans la colonne d'apothicaire, "
                     "trappe basculante noir mat « LINGE » à fermeture automatique et loquet enfant (bouche de 12 × 12 po, seuil "
                     "à 40 po) ; descend entre deux solives jusqu'au plafond de la salle de lavage",
                     "CHUTE", (gx0 + gx1) / 2, (gy0 + gy1) / 2, gx1 - gx0 + 0.5, gy1 - gy0 + 0.5,
                     SOURCE + " — à valider : position de la cloison du fond (y ≈ 142), sens des solives, baie libre")
    xs = [p[0] for p in AXE_DEF]
    e_sortie = _element("elem-SS-S-CHUTE", "trappe",
                        "Arrivée de la chute à linge au plafond (12 × 14 po, devant la poutre maîtresse) et coude-déflecteur "
                        "d'inox Ø 14 po apparent, au-dessus de l'arc de la porte (dessous à 83 po), bec au-dessus du chariot "
                        "à linge roulant (20 × 14 × 33 po, entre le chauffe-eau et l'arc de la porte)",
                        "CHUTE", (min(xs) - R_DEF + max(xs) + R_DEF) / 2, YS, max(xs) - min(xs) + 2 * R_DEF, 2 * R_DEF)
    # le chariot à linge (meuble roulant) n'est pas dessiné au plan, comme les autres paniers ; il est dans la note et la 3D
    for niv, els in ((rdc, [e_rdc]), (ss, [e_sortie])):
        ids = {e["id"] for e in els}
        niv["elements"] = [e for e in niv["elements"] if e["id"] not in ids] + els
        niv["elements"].sort(key=lambda e: e["id"])
    for p in rdc["pieces"]:
        if p["id"] == "piece-RDC-SDB" and "chute à linge" not in (p.get("description") or ""):
            p["description"] = (p.get("description") or "Salle de bain") + " ; chute à linge vers la salle de lavage — " + SOURCE
    for p in ss["pieces"]:
        if p["id"] == "piece-SS-LAVAGE" and "chute à linge" not in (p.get("description") or ""):
            p["description"] = (p.get("description") or "Salle de lavage") + " ; arrivée de la chute à linge et chariot — " + SOURCE
    # note de la proposition sur P-129 : 2e note (la 1re est réécrite par modifs.py) ; celles de P-130 sont fixées par modifs.py
    notes = ss.setdefault("notes", [])
    notes[:] = [n for n in notes if n.get("id") != "note-SS-CHUTE"]
    notes.insert(min(1, len(notes)), {"id": "note-SS-CHUTE", "texte_original": None, "photo": None, "interpretation": NOTE_SS})


# ------------------------------------------------------------------------------------------------ 3D
def B(x0, y0, x1, y1, z0, z1, mat):
    return {"forme": "boite", "x0": x0, "y0": y0, "x1": x1, "y1": y1, "z0": z0, "z1": z1, "mat": mat}


def A(x0, y0, x1, y1, z0, z1, mat, r=3, b=0.5, trou=None):
    o = {"forme": "arrondi", "x0": x0, "y0": y0, "x1": x1, "y1": y1, "z0": z0, "z1": z1, "mat": mat, "r": r, "b": b}
    if trou:
        o["trou"] = trou
    return o


def C(x, y, r, z0, z1, mat, **k):
    return dict({"forme": "cylindre", "x": x, "y": y, "r": r, "z0": z0, "z1": z1, "mat": mat}, **k)


def T(pts, r, mat, **k):
    return dict({"forme": "tube", "pts": [list(p) for p in pts], "r": r, "mat": mat}, **k)


def _z_axe(x):
    """z de l'axe du déflecteur (polyligne AXE_DEF, partie en pente) à l'abscisse x."""
    pts = AXE_DEF[1:-1]
    for (xa, _, za), (xb, _, zb) in zip(pts, pts[1:]):
        if min(xa, xb) <= x <= max(xa, xb) and xa != xb:
            return za + (zb - za) * (x - xa) / (xb - xa)
    return None


def _sous_sol():
    """Objets fixes du sous-sol (z du sous-sol) : collerette, coude-déflecteur, suspentes, chariot à linge."""
    out = []
    sx0, sx1, sy0, sy1 = SORTIE
    # collerette d'inox au plafond (transition 12 × 14 → Ø 14) et coude-déflecteur d'inox brossé, apparent
    out += [B(sx0 - 2.0, sy0 - 1.0, sx1 + 2.0, sy1 + 1.0, PLAFOND_SS - 1.4, PLAFOND_SS, "inox"),
            T(AXE_DEF, R_DEF, "inox", pans=32)]
    # fond noir dans le bec (on voit un trou noir d'en dessous, pas le plafond à travers le tube)
    out += [C(X_BEC, YS, R_DEF - 0.4, Z_BEC + 0.5, Z_BEC + 0.7, "pneu", pans=32)]
    # bague du bec et suspentes (tiges filetées noires et colliers) au plafond
    out += [{"forme": "tore", "x": X_BEC, "y": YS, "z": Z_BEC + 0.3, "R": R_DEF, "r": 0.35, "mat": "inox", "axe": "z"}]
    for xs in (70.0, 61.0):
        zt = _z_axe(xs) + R_DEF / 0.83
        out += [T([(xs, YS, PLAFOND_SS), (xs, YS, zt + 0.4)], 0.22, "metal"),
                B(xs - 0.6, YS - R_DEF - 0.3, xs + 0.6, YS + R_DEF + 0.3, zt - 0.6, zt + 0.4, "metal")]
    # chariot à linge : cadre d'acier noir mat (montants, cadres haut et bas), 4 roulettes, sac de toile écrue creux
    x0, y0, x1, y1 = CHARIOT
    i = 0.45
    coins = [(x0 + i, y0 + i), (x1 - i, y0 + i), (x1 - i, y1 - i), (x0 + i, y1 - i)]
    for (xa, ya) in coins:
        out += [T([(xa, ya, 3.6), (xa, ya, 33.0)], 0.4, "metal"),
                C(xa, ya, 0.55, 2.6, 3.6, "metal"),                                        # chape de la roulette
                {"forme": "cylindre", "axe": "y", "x": xa, "y0": ya - 0.55, "y1": ya + 0.55, "z": 1.35, "r": 1.35,
                 "mat": "pneu", "pans": 20}]
    for z, r in ((4.0, 0.32), (33.0, 0.4)):                                                 # cadres bas et haut
        out += [T([(*coins[k], z), (*coins[(k + 1) % 4], z)], r, "metal") for k in range(4)]
    # sac de toile : 4 parois minces et un fond, ourlet replié par-dessus le cadre du haut
    a0, b0, a1, b1, e = x0 + 0.9, y0 + 0.9, x1 - 0.9, y1 - 0.9, 0.3
    zs0 = Z_SAC - 0.5
    out += [B(a0, b0, a1, b0 + e, zs0, 32.4, TOILE), B(a0, b1 - e, a1, b1, zs0, 32.4, TOILE),
            B(a0, b0 + e, a0 + e, b1 - e, zs0, 32.4, TOILE), B(a1 - e, b0 + e, a1, b1 - e, zs0, 32.4, TOILE),
            B(a0 + e, b0 + e, a1 - e, b1 - e, zs0, Z_SAC, TOILE)]
    h0, h1 = 30.9, 33.6
    out += [B(x0 - 0.15, y0 - 0.15, x1 + 0.15, y0 + 0.95, h0, h1, TOILE), B(x0 - 0.15, y1 - 0.95, x1 + 0.15, y1 + 0.15, h0, h1, TOILE),
            B(x0 - 0.15, y0 + 0.95, x0 + 0.95, y1 - 0.95, h0, h1, TOILE), B(x1 - 0.95, y0 + 0.95, x1 + 0.15, y1 - 0.95, h0, h1, TOILE)]
    return out


def _ballot():
    """Ballot de linge en tissu froissé (repère local : origine au centre du dessous), ≈ 9½ × 9½ × 8 po : il passe la bouche
    de 12 × 12 po et tient dans le sac du chariot (11½ po de large à l'intérieur) sans en traverser les parois."""
    return [{"forme": "sphere", "x": 0, "y": 0, "z": 3.3, "r": 4.6, "ecrase": 0.7, "mat": "draps"},
            {"forme": "sphere", "x": 1.6, "y": -1.2, "z": 5.6, "r": 3.0, "ecrase": 0.75, "mat": "jete"},
            {"forme": "sphere", "x": -2.0, "y": 1.3, "z": 5.2, "r": 2.8, "ecrase": 0.7, "mat": "tissu"},
            {"forme": "sphere", "x": 1.0, "y": 2.2, "z": 2.2, "r": 2.0, "ecrase": 0.7, "mat": "draps"},
            T([(-2.0, -2.6, 2.2), (-3.0, -3.6, 1.6)], 0.85, "tissu", bouts=True)]                             # manche qui dépasse


def _mat_rdc(SCENE, mat):
    """Nom du matériau d'un alias de peinture du RDC après la fusion des étages (le moteur renomme les alias homonymes de
    couleurs différentes en « alias@RDC » ; il ne le fait pas pour les séquences)."""
    couleurs = set()
    for E in SCENE["etages"]:
        for v in (E.get("peintures") or {}).values():
            if len(v) > 2 and v[2] == mat:
                couleurs.add(str(v[0]).lower())
    return f"{mat}@RDC" if len(couleurs) > 1 else mat


def appliquer_scene_deux(SCENE):
    ss, rdc = SCENE["etages"][0], SCENE["etages"][1]
    H = float(ss.get("hauteur_etage", 105))                        # plancher du RDC en z absolu
    # 1) la trappe fixe de la colonne (rdc_cafe_sdb.py) devient la trappe animée de la séquence
    trappe = CAFE.trappe_chute()
    avant = len(rdc["mobilier"])
    rdc["mobilier"] = [o for o in rdc["mobilier"] if o not in trappe]
    if avant - len(rdc["mobilier"]) != len(trappe):
        raise SystemExit("chute_linge.py : trappe de la colonne introuvable dans le mobilier du RDC (rdc_cafe_sdb.py a changé ?)")
    noir = _mat_rdc(SCENE, "noir-mat")

    def absolu(o):
        o = dict(o, mat=noir if o["mat"] == "noir-mat" else o["mat"])
        if "pts" in o:
            return dict(o, pts=[[p[0], p[1], round(p[2] + H, 3)] for p in o["pts"]])
        return dict(o, z0=round(o["z0"] + H, 3), z1=round(o["z1"] + H, 3))
    y_ch, z_ch = CAFE.COL[3], CAFE.Z_TRAPPE[0] + 0.25                # charnière : arête du bas, devant
    xa, xb = CAFE.X_GAUCHE
    # 2) sous-sol : collerette, déflecteur, chariot
    ss["mobilier"] += _sous_sol()
    # 3) chemin du ballot (origine = centre du dessous ; z absolu) : posé dans la trappe ouverte, bouche, pente du
    #    fond de la trémie, gaine, décalage dans le plancher, déflecteur (axe - 3,9 po), bec, fond du sac du chariot
    gy = (GAINE_RDC[2] + GAINE_RDC[3]) / 2
    zr = lambda z: round(H + z, 2)
    chemin = [[XC, 173.0, zr(44.0)], [XC, 166.0, zr(41.0)], [XC, gy, zr(31.0)], [XC, gy, zr(1.0)],
              [XC, YS, round(PLAFOND_SS - 1.0, 2)]]
    chemin += [[x, y, round(z - 3.9, 2)] for (x, y, z) in AXE_DEF[1:]]
    xc_sac = (CHARIOT[0] + CHARIOT[2]) / 2
    chemin += [[xc_sac - 0.3, (CHARIOT[1] + CHARIOT[3]) / 2, Z_SAC]]
    SCENE["sequences"] = [s for s in SCENE.get("sequences") or [] if s.get("id") != "chute"] + [{
        "id": "chute", "nom": "Chute à linge", "libelle": "Envoyer du linge", "libelle_voir": "Voir arriver au lavage",
        "note": "Trappe de la colonne d'apothicaire (salle de bain du haut) → chariot de la salle de lavage",
        "trappe": {"objets": [absolu(o) for o in trappe],
                   "charniere": [[xa, y_ch, zr(z_ch)], [xb, y_ch, zr(z_ch)]], "angle": -35, "duree": 0.6, "ferme_apres": 0.5},
        "ballot": {"objets": _ballot(), "chemin": chemin, "vitesse_depart": 30, "frottement": 0.3, "culbute": 110},
        "panier": {"pile": [[0, 0, 0], [1.6, -0.7, 5.0], [-1.4, 0.6, 10.0]]},
        "vue_depart": {"x": 87, "y": 197, "cap": 266, "etage": "RDC", "tangage": -24},
        "vue_arrivee": {"x": 54, "y": 64, "cap": 79, "etage": "SS", "tangage": -10},
        "attente_voir": 15}]
    # 4) arrêts de visite et palettes
    def inserer(E, arret, apres):
        vis = [v for v in E.get("visites", []) if v.get("nom") != arret["nom"]]
        noms = [v.get("nom") for v in vis]
        i = next((noms.index(a) + 1 for a in apres if a in noms), len(vis))
        vis.insert(i, arret)
        E["visites"] = vis
    inserer(rdc, {"nom": "Chute à linge", "x": 87, "y": 197, "cap": 266, "tangage": -24}, ["Salle de bain — rangement", "Vanité"])
    inserer(ss, {"nom": "Chute à linge — arrivée au lavage", "x": 54, "y": 64, "cap": 79, "tangage": -10},
            ["Congélateur (salle de lavage)", "Salle de lavage"])
    for E, piece, txt in ((rdc, "Salle de bain", "chute à linge : trappe basculante noir mat « LINGE » (lettres de laiton, loquet enfant) "
                                                 "dans la colonne d'apothicaire"),
                          (ss, "Salle de lavage", "chute à linge : coude-déflecteur d'inox brossé apparent sous la sortie au "
                                                  "plafond, chariot à linge roulant (acier noir, sac de toile écrue)")):
        for p in E.setdefault("palette", []):
            if p[0] == piece and "chute à linge" not in p[1]:
                p[1] += " ; " + txt
