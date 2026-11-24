"""MAISON-18 — RDC, zone CUISINE et SALLE À MANGER.

Demande du client (2026-11-02) :
« En haut les chaises sont buggées, mets-les sous la table de cuisine. Je veux qu'on enlève le coin ordi aussi dans la
cuisine et que tu transformes ça en beau rangement ou quelque chose d'efficace. La céramique va tout droit de la porte
arrière, genre c'est un gros rectangle où tu as commencé à la dessiner dans la cuisine. »
(Le coin café de l'entrée arrière, les laveuse-sécheuse et la porte de la salle de lavage sont traités par rdc_cafe_sdb.py.)

Ce module (appelé par modifs.py et scene_3d.py, après rdc_bureau) :
1. CHAISES : les 8 chaises de RDC-01 (fonction chaise() de base_rdc01_scene.py) étaient des « boîtes » (assise plate de
   2 po, dossier en planche verticale) et la chaise (190, 324) entrait de 13 po dans le buffet. Elles sont remplacées par
   des chaises coques (comme sur les photos 06 et 07 : coque de similicuir noir, dossier enveloppant incliné, quatre
   pattes de métal noir évasées) RANGÉES SOUS LA TABLE : 3 par côté, haut du dossier à 3½ po du bord du plateau, assise
   glissée de 17½ po dessous ; une à chaque bout, haut du dossier à 5 po du bord. Aucune ne touche un pied de table, la
   ceinture, une autre chaise ni le buffet (contrôle _verifier_chaises). La table et son luminaire avancent de 8 po vers
   la cuisine (32¾ po jusqu'au mur au lieu de 24¾, 16 po jusqu'au buffet au lieu de 8) : la porte de la G.R. 3, dont les
   pentures sont corrigées d'après la photo 06 (côté arrière), s'ouvre à 90° sans toucher les chaises rangées.
   Les 3 tabourets de l'îlot prennent la même coque (hauteur comptoir) et sont glissés sous le porte-à-faux de 12 po.
2. COIN ORDI (renfoncement x 148¼ → 177¼, y 204 → 250¾, photos 05 et 06) : bureau flottant, écrans et chaise enlevés.
   À la place, un GARDE-MANGER ENCASTRÉ pleine hauteur, au nu du mur des garde-robes (29 po de profond, 42¼ po de large) :
   caisson et portes noir mat (comme la colonne d'armoires de la cuisine), deux grandes portes sur 5 tiroirs coulissants
   intérieurs à rebord (26 po), deux portes hautes (rangement d'appoint), cadre et joue de bois de grange (comme les
   comptoirs), longues poignées noires. Le thermostat qui était au fond du renfoncement passe sur le mur, à côté.
3. TUILE D'ARDOISE (« céramique » du client) : un seul rectangle, de la baie de l'entrée arrière tout droit jusqu'à la
   poutre de l'axe B : x 264 → 446, y 157 → 370 (photos 01, 02, 07, 08 : le joint part du poteau de bois brut contre le
   mur arrière et file vers l'avant ; côté salon, la tuile s'arrête sous la poutre). Ce rectangle EST la pièce « Cuisine »
   (agrandie de x = 316 à x = 264 aux dépens de la salle à manger et du dégagement) : la maquette pose le sol par pièce,
   et le mode maquette ne dessine pas les revêtements. Le reste de la salle à manger et du dégagement est en érable
   (plancher réel, photos 05 et 06). Réducteurs d'érable de 2¼ po le long des deux joints érable / ardoise ; l'ardoise
   continue dans l'épaisseur de la baie vers l'entrée arrière (ardoise aussi). Anciens seuils d'inox enlevés.
4. Plan P-130 : garde-manger ajouté (elem-RDC-K-GM) ; le coin ordi n'était pas au plan ; pièces Cuisine, Salle à manger
   et Dégagement redessinées. Arrêt de visite « Coin bureau » remplacé par « Cuisine — rangement ».
Pouces, repère de la maison (x le long de la façade, y vers l'arrière, z depuis le plancher du RDC).
"""
import math

from shapely.geometry import Polygon, box
from shapely.geometry.polygon import orient

SRC = "proposition MAISON-18, cuisine et salle à manger (esquisse)"

# ------------------------------------------------------------------------------------------------ repères
# table de bois de récupération de RDC-01 (plateau x 202 → 248, y 248 → 342) avancée de 8 po vers la cuisine avec son
# luminaire : 32¾ po (au lieu de 24¾) entre le bord de la table et le mur des G.R., et la porte de la G.R. 3 s'ouvre à 90°
# sans toucher les chaises rangées ; il reste 75 po jusqu'aux dossiers des tabourets de l'îlot.
DX_TABLE = 8.0
ZONE_TABLE = (200.0, 246.0, 250.0, 344.0)            # emprise de la table et du luminaire de RDC-01 (avant le décalage)
TABLE = (202.0 + DX_TABLE, 248.0, 248.0 + DX_TABLE, 342.0)   # plateau (dessus à 31 po, dessous à 29 po)
CEINTURE = (206.0 + DX_TABLE, 253.0, 244.0 + DX_TABLE, 337.0, 25.0)   # ... et sa ceinture (dessous à 25 po)
PIEDS = [(x + DX_TABLE, y, x + DX_TABLE + 4, y + 4) for x in (206.0, 240.0) for y in (253.0, 333.0)]
BUFFET = (177.6, 312.0, 194.0, 364.0)
# porte de la G.R. 3 (ouv-RDC-018, 28 po, mur-RDC-022 à x = 175) : pentures du côté arrière (photo 06 : poignée du côté
# du renfoncement, pentures visibles côté salle à manger), elle s'ouvre vers la salle à manger
PORTE_GR3 = ("ouv-RDC-018", (177.25, 288.0), 28.0)
# chaises rangées : (x, y, face) ; face = vers où regarde la personne assise (le dossier est du côté opposé)
RECUL = 3.5                                          # dossier (haut, face extérieure) à 3½ po du bord du plateau (côtés)
DOS = 11.91                                          # du centre de la chaise au haut du dossier (face extérieure)
CH_COTES = (274.0, 295.0, 316.0)                     # axes des 3 chaises de chaque côté
CH_BOUT_AV, CH_BOUT_AR = 255.0, 335.0                # axes des chaises des bouts (avant, arrière)
# îlot (RDC-01) : dessus x 340 → 384 (porte-à-faux de 12 po côté salle à manger), caisson à x = 352
ILOT_BORD, ILOT_CAISSON = 340.0, 352.0
TAB_Y = (232.0, 258.0, 284.0)
TAB_X = 342.0                                        # avant de l'assise à 1½ po du caisson, sous le porte-à-faux
# garde-manger dans le renfoncement : du poteau C01 (y 200 → 208) au mur des G.R. (mur-RDC-025, nu à y = 250¾)
GM_X0, GM_X1 = 148.25, 177.25                        # dos au mur (mur-RDC-021, nu) ; face au nu du mur des G.R. (x = 177¼)
GM_Y0, GM_Y1 = 208.25, 250.5
GM_CADRE = 1.5                                       # cadre de bois de grange (joue côté dégagement, montant au mur, couronne)
GM_RETRAIT = 0.75                                    # portes en retrait du cadre
GM_Z_HAUT = 78.0                                     # joint portes basses / portes hautes
PLAFOND = 96.0
# tuile d'ardoise : un seul rectangle (le joint de gauche tombe sur une ligne de la texture de 24 po : carreaux entiers)
TUILE = (264.0, 157.0, 446.0, 370.0)
BAIE_EAR = (279.55, 310.45)                          # embrasure de la baie vers l'entrée arrière (dans le doublage noir)
# emprises de ce qu'on enlève de RDC-01
ZONE_ORDI = (147.5, 204.5, 178.0, 250.6)
ANCIENNES_CHAISES = [(190, 266), (190, 295), (190, 324), (260, 266), (260, 295), (260, 324), (225, 236), (225, 354)]
ANCIENS_TABOURETS = [(328, 232), (328, 258), (328, 284)]


# =============================================================================================== plan (P-130)
def _dim(v, note=None, src="PROPOSÉ"):
    d = {"valeur": v, "source": src, "photo": None}
    if note:
        d["note"] = note
    return d


def _repiece(p, P, note):
    """Nouveau polygone d'une pièce existante (aire et dimensions recalculées)."""
    P = orient(P.simplify(0.01), 1.0)
    x0, y0, x1, y1 = P.bounds
    p["polygone"] = [[round(a, 2), round(b, 2)] for a, b in list(P.exterior.coords)[:-1]]
    p["superficie"] = _dim(round(P.area / 144, 1), note, "DÉDUIT")
    p["dimensions"] = {"x": _dim(round(x1 - x0, 2), None, "DÉDUIT"), "y": _dim(round(y1 - y0, 2), None, "DÉDUIT")}


def appliquer_modifs_rdc(maison, ctx):
    rdc = ctx["rdc"]
    # 0) la pièce « Cuisine » devient le rectangle d'ardoise (le sol de la maquette suit les pièces) : elle prend la bande
    #    x 264 → 316 à la salle à manger et au dégagement, de la poutre (y = 157) au mur arrière
    bande = box(TUILE[0], TUILE[1], 316.0, TUILE[3])
    note = "aire recalculée : la cuisine suit la tuile d'ardoise (x 264 → 446, photos 01, 02, 07, 08) — " + SRC
    for p in rdc["pieces"]:
        P = Polygon(p["polygone"])
        if p["id"] == "piece-RDC-CUI":
            Q = P.union(bande)
            if abs(Q.area - box(*TUILE).area) > 1.0:
                print(f"  [rdc_cuisine] ATTENTION : la cuisine n'est pas le rectangle d'ardoise ({Q.bounds})")
            _repiece(p, Q, note)
            p["description"] = ("Cuisine : tout le rectangle de tuile d'ardoise noire, de la baie de l'entrée arrière à la "
                                "poutre ; îlot et 3 tabourets — " + SRC)
        elif p["id"] in ("piece-RDC-UTI", "piece-RDC-DEG") and P.intersects(bande) and P.intersection(bande).area > 1:
            Q = P.difference(bande)
            if Q.geom_type != "Polygon":
                Q = max(Q.geoms, key=lambda g: g.area)
            _repiece(p, Q, note)
    e = {"id": "elem-RDC-K-GM", "type": "armoires",
         "nom": "Garde-manger encastré pleine hauteur (remplace le coin ordi) : caisson et portes noir mat, 5 tiroirs "
                "coulissants intérieurs, 2 portes hautes, cadre et joue de bois de grange — 42¼ × 29 po, face au nu du mur des G.R.",
         "nom_original": None, "etat": "nouveau", "libelle": "G.-M.",
         "position": {"x": round((GM_X0 + GM_X1) / 2, 2), "y": round((GM_Y0 + GM_Y1) / 2, 2), "rotation_deg": 270,
                      "source": "PROPOSÉ"},
         "dimensions": {"longueur": _dim(round(GM_Y1 - GM_Y0, 2), "du poteau (y ≈ 208) au mur des G.R. (y = 250¾) : à mesurer"),
                        "largeur": _dim(round(GM_X1 - GM_X0, 2), "profondeur du renfoncement (photos 05, 06) : à mesurer")},
         "note": "Coin ordi de RDC-01 (bureau flottant, écrans, chaise) enlevé ; thermostat à déplacer sur le mur voisin "
                 "(électricien) — " + SRC}
    rdc["elements"] = [x for x in rdc["elements"] if x["id"] != e["id"]] + [e]
    rdc["elements"].sort(key=lambda x: x["id"])
    # porte de la G.R. 3 : pentures du côté arrière, comme sur la photo 06 (poignée du côté du renfoncement, pentures
    # visibles côté salle à manger : elle s'ouvre vers la salle à manger)
    for o in rdc["ouvertures"]:
        if o["id"] == PORTE_GR3[0]:
            o["sens"] = dict(o.get("sens") or {}, charniere="fin", ouvre_vers="droite",
                             note="pentures côté arrière (y ≈ 288), poignée côté renfoncement : d'après la photo 06 — " + SRC)


# =============================================================================================== maquette 3D
def _centre(o):
    f = o.get("forme", "boite")
    if "pts" in o and f in ("boite", "tube"):
        pts = o["pts"]
        return sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
    if f in ("boite", "arrondi"):
        return (o["x0"] + o["x1"]) / 2, (o["y0"] + o["y1"]) / 2
    if f == "cylindre" and o.get("axe") == "y":
        return o["x"], (o["y0"] + o["y1"]) / 2
    if f == "cylindre" and o.get("axe") == "x":
        return (o["x0"] + o["x1"]) / 2, o["y"]
    return o.get("x", -1e9), o.get("y", -1e9)


def _dans(x, y, r):
    return r[0] <= x <= r[2] and r[1] <= y <= r[3]


def _protege(o):                      # battants et habillages de portes : jamais retirés
    return bool(o.get("role") or o.get("ouverture") or o.get("porte"))


def _decaler(o, dx):
    """Copie de l'objet déplacée de dx en x (boîtes, prismes, tubes, cylindres, modèles, sphères)."""
    o = dict(o)
    if "pts" in o:
        o["pts"] = [[p[0] + dx] + list(p[1:]) for p in o["pts"]]
    elif "x0" in o and "x1" in o:
        o["x0"], o["x1"] = o["x0"] + dx, o["x1"] + dx
    elif "x" in o:
        o["x"] = o["x"] + dx
    return o


def _table_et_luminaire(o):
    """Objet de RDC-01 qui appartient à la table (bois de récupération) ou à son luminaire linéaire et à la plante."""
    if _protege(o):
        return False
    cx, cy = _centre(o)
    if not _dans(cx, cy, ZONE_TABLE):
        return False
    if o.get("mat") == "bois_recupere" or o.get("forme") == "modele":
        return True
    return o.get("mat") in ("carbone", "spot", "metal") and _bornes(o)[1][1] > 60


FACES = {"+x": (1.0, 0.0), "-x": (-1.0, 0.0), "+y": (0.0, 1.0), "-y": (0.0, -1.0)}


def _repere(x, y, face):
    """(u, v) local → (X, Y) maison ; u vers l'avant de la personne assise, v sur le côté."""
    fx, fy = FACES[face]
    return lambda u, v: (x + u * fx - v * fy, y + u * fy + v * fx)


def _rect(rp, u0, u1, v0, v1):
    (ax, ay), (bx, by) = rp(u0, v0), rp(u1, v1)
    return min(ax, bx), min(ay, by), max(ax, bx), max(ay, by)


def _ccw(pts):
    s = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
    return pts if s > 0 else pts[::-1]


def _coque(h, rp, uc, R, t, demi, z0, z1, tranches, recul, mat):
    """Dossier enveloppant d'une chaise coque : bande courbe en plan (arc de rayon intérieur R centré en u = uc), épaisseur
    t, de z0 à z1 en « tranches » décalées vers l'arrière (inclinaison de recul po au total) ; bord du haut arrondi."""
    a = math.asin(min(0.99, demi / R))
    n = 9
    angs = [math.pi - a + 2 * a * k / (n - 1) for k in range(n)]
    out = []
    dz = (z1 - z0) / tranches
    for k in range(tranches):
        d = -recul * (k + 0.5) / tranches
        inte = [rp(uc + d + R * math.cos(q), R * math.sin(q)) for q in angs]
        exte = [rp(uc + d + (R + t) * math.cos(q), (R + t) * math.sin(q)) for q in reversed(angs)]
        pts = _ccw([[round(x, 3), round(y, 3)] for x, y in inte + exte])
        out.append({"forme": "boite", "pts": pts, "z0": round(z0 + k * dz, 3), "z1": round(z0 + (k + 1) * dz + 0.02, 3), "mat": mat})
    d = -recul * (tranches - 0.5) / tranches
    bord = [rp(uc + d + (R + t / 2) * math.cos(q), (R + t / 2) * math.sin(q)) for q in angs]
    out.append(h.T([(x, y, z1) for x, y in bord], t / 2, mat, bouts=True))
    return out


def chaise_coque(h, x, y, face):
    """Chaise de salle à manger coque (photos 06, 07) : coque de similicuir noir (assise 18½ × 18 po à 18¼ po du sol,
    dossier enveloppant incliné jusqu'à 32 po), quatre pattes de métal noir évasées, platine sous l'assise.
    Emprise au sol : u de −11,9 (dossier, haut) à +9 (avant de l'assise), v ± 9,4."""
    A, B, T = h.A, h.B, h.T
    rp = _repere(x, y, face)
    out = [A(*_rect(rp, -9.6, 9.0, -9.0, 9.0), 16.8, 18.4, h.CUIR, r=3.5, b=0.6)]               # assise
    out += _coque(h, rp, 7.1, 17.0, 0.75, 9.0, 17.2, 31.8, 8, 1.4, h.CUIR)                       # dossier
    out.append(B(*_rect(rp, -6.2, 5.8, -5.6, 5.6), 16.3, 16.8, "carbone"))                      # platine
    for us, ub in ((8.4, 5.4), (-8.8, -5.8)):                                                    # pattes évasées
        for vs in (-1, 1):
            out.append(T([(*rp(us, vs * 8.5), 0), (*rp(ub, vs * 5.4), 16.4)], 0.42, "metal"))
    return out


def tabouret_coque(h, x, y, face):
    """Tabouret de comptoir coque, assorti aux chaises (photos 01, 08) : assise à 26 po, dossier court enveloppant,
    quatre pattes noires et repose-pieds sur trois côtés à 9½ po."""
    A, B, T = h.A, h.B, h.T
    rp = _repere(x, y, face)
    out = [A(*_rect(rp, -9.0, 8.4, -8.6, 8.6), 24.4, 26.0, h.CUIR, r=3.5, b=0.6)]
    out += _coque(h, rp, 6.5, 16.0, 0.7, 8.6, 24.8, 36.0, 6, 1.0, h.CUIR)
    out.append(B(*_rect(rp, -5.6, 5.2, -5.2, 5.2), 23.9, 24.4, "carbone"))
    pieds = {}
    for us, ub in ((7.6, 5.0), (-8.0, -5.4)):
        for vs in (-1, 1):
            out.append(T([(*rp(us, vs * 7.8), 0), (*rp(ub, vs * 5.0), 24.0)], 0.4, "metal"))
            f = 9.5 / 24.0                                                                       # point des pattes à 9½ po
            pieds[(us, vs)] = (us + (ub - us) * f, vs * (7.8 + (5.0 - 7.8) * f))
    for a, b in (((7.6, -1), (7.6, 1)), ((7.6, -1), (-8.0, -1)), ((7.6, 1), (-8.0, 1))):         # repose-pieds
        (ua, va), (ub, vb) = pieds[a], pieds[b]
        out.append(T([(*rp(ua, va), 9.5), (*rp(ub, vb), 9.5)], 0.32, "metal"))
    return out


def _bornes(o):
    """Rectangle en plan (x0, y0, x1, y1) et hauteurs (z0, z1) d'un objet de la scène."""
    f = o.get("forme", "boite")
    if f == "tube":
        r = o["r"]
        xs, ys, zs = [p[0] for p in o["pts"]], [p[1] for p in o["pts"]], [p[2] for p in o["pts"]]
        return (min(xs) - r, min(ys) - r, max(xs) + r, max(ys) + r), (min(zs) - r, max(zs) + r)
    if "pts" in o:
        xs, ys = [p[0] for p in o["pts"]], [p[1] for p in o["pts"]]
        return (min(xs), min(ys), max(xs), max(ys)), (o["z0"], o["z1"])
    return (o["x0"], o["y0"], o["x1"], o["y1"]), (o["z0"], o["z1"])


def _union(rs):
    return min(r[0] for r in rs), min(r[1] for r in rs), max(r[2] for r in rs), max(r[3] for r in rs)


def chaises_rangees():
    """(x, y, face) des 8 chaises glissées sous la table."""
    tx0, ty0, tx1, ty1 = TABLE
    xg = tx0 - RECUL + DOS                 # côté gauche (regarde +x) : haut du dossier à RECUL po du bord
    xd = tx1 + RECUL - DOS                 # côté droit (regarde −x)
    xm = (tx0 + tx1) / 2
    out = [(xg, y, "+x") for y in CH_COTES] + [(xd, y, "-x") for y in CH_COTES]
    out += [(xm, CH_BOUT_AV, "+y"), (xm, CH_BOUT_AR, "-y")]
    return out


def _chevauche(a, b, jeu=0.0):
    return a[0] < b[2] - jeu and b[0] < a[2] - jeu and a[1] < b[3] - jeu and b[1] < a[3] - jeu


def _verifier_chaises(h):
    """Contrôle sur la géométrie dessinée : aucune chaise ne touche un pied de table, une autre chaise ou le buffet ;
    ce qui dépasse 29 po (dessous du plateau) reste hors du plateau, ce qui dépasse 25 po hors de la ceinture."""
    pbs, emp = [], []
    ch = chaises_rangees()
    for c in ch:
        objs = [_bornes(o) for o in chaise_coque(h, *c)]
        emp.append(_union([r for r, _ in objs]))
        for r, (z0, z1) in objs:
            if z1 > 29.0 and _chevauche(r, TABLE):
                pbs.append(f"chaise {c} : dossier sous le plateau {r}")
            if z1 > CEINTURE[4] and _chevauche(r, CEINTURE[:4]):
                pbs.append(f"chaise {c} : touche la ceinture {r}")
            for p in PIEDS:
                if _chevauche(r, p):
                    pbs.append(f"chaise {c} / pied {p}")
    for i in range(len(emp)):
        if _chevauche(emp[i], BUFFET):
            pbs.append(f"chaise {ch[i]} / buffet")
        for j in range(i + 1, len(emp)):
            if _chevauche(emp[i], emp[j]):
                pbs.append(f"chaise {ch[i]} / chaise {ch[j]}")
    _, (px, py), Lp = PORTE_GR3                             # balayage de la porte de la G.R. 3 (vantail de 28 po + 1 po)
    for c in ch:
        for o in chaise_coque(h, *c):
            pts = [p[:2] for p in o["pts"]] if "pts" in o else [(o["x0"], o["y0"]), (o["x1"], o["y1"]), (o["x0"], o["y1"]), (o["x1"], o["y0"])]
            if any(x > px and y < py + 2 and math.hypot(x - px, y - py) < Lp + 1.0 for x, y in pts):
                pbs.append(f"chaise {c} dans le balayage de la porte de la G.R. 3")
                break
    for y in TAB_Y:                                         # tabourets : sous le porte-à-faux, sans toucher le caisson
        objs = [_bornes(o) for o in tabouret_coque(h, TAB_X, y, "+x")]
        e = _union([r for r, _ in objs])
        if e[2] >= ILOT_CAISSON:
            pbs.append(f"tabouret {y} touche le caisson de l'îlot ({e[2]:.2f})")
        if any(z1 > 34.5 and r[2] > ILOT_BORD for r, (z0, z1) in objs):
            pbs.append(f"tabouret {y} : dossier sous le dessus de l'îlot")
    if pbs:
        print("  [rdc_cuisine] ATTENTION chaises :", "; ".join(pbs))
    return pbs, emp


def _garde_manger(h):
    A, B, T = h.A, h.B, h.T
    x0, x1, y0, y1, c = GM_X0, GM_X1, GM_Y0, GM_Y1, GM_CADRE
    xf = x1 - GM_RETRAIT                                   # face des portes
    zc = PLAFOND - 3.0                                     # dessous de la couronne
    out = []
    # cadre de bois de grange : joue côté dégagement (vue de l'entrée), montant contre le mur des G.R., couronne
    out += [A(x0, y0, x1, y0 + c, 0, PLAFOND - 0.1, "bois_grange", r=0.3, b=0.2),
            B(x0, y1 - c, x1, y1, 0, PLAFOND - 0.1, "bois_grange"),
            B(xf - 2, y0 + c, x1, y1 - c, zc, PLAFOND - 0.1, "bois_grange")]
    # caisson et portes noir mat, socle en retrait
    out += [A(x0, y0 + c, xf, y1 - c, 4.0, zc, h.NOIR, r=0.2, b=0.2),
            B(x0, y0 + c, xf - 3.0, y1 - c, 0, 4.0, "carbone")]
    ym = (y0 + y1) / 2
    out += [B(xf - 0.05, ym - 0.12, xf + 0.05, ym + 0.12, 4.5, zc - 0.3, "carbone"),            # joint central
            B(xf - 0.05, y0 + c, xf + 0.05, y1 - c, GM_Z_HAUT - 0.12, GM_Z_HAUT + 0.12, "carbone")]   # joint haut
    # longues poignées noires (barres de 24 po) des portes basses ; courtes aux portes hautes
    for yp in (ym - 1.6, ym + 1.6):
        out += [T([(xf + 1.1, yp, 34.0), (xf + 1.1, yp, 58.0)], 0.32, "metal", bouts=True),
                B(xf, yp - 0.3, xf + 1.1, yp + 0.3, 36.0, 36.8, "metal"), B(xf, yp - 0.3, xf + 1.1, yp + 0.3, 55.2, 56.0, "metal"),
                T([(xf + 1.1, yp, GM_Z_HAUT + 1.8), (xf + 1.1, yp, GM_Z_HAUT + 7.8)], 0.3, "metal", bouts=True)]
    # thermostat (était au fond du renfoncement, photo 06) : sur le mur des G.R., entre le cadre et la porte
    out += [A(177.25, 252.7, 178.15, 256.1, 57.0, 61.5, "blanc", r=0.4, b=0.2)]
    return out


def _sol(h):
    """Tuile d'ardoise : un rectangle de la baie de l'entrée arrière à la poutre de l'axe B ; seuils d'érable."""
    B, A = h.B, h.A
    x0, y0, x1, y1 = TUILE
    # le rectangle lui-même est le sol de la pièce « Cuisine » (agrandie à x = 264 dans appliquer_modifs_rdc, sols :
    # ardoise) : visible aussi en mode maquette, qui ne dessine pas les revêtements ; ici, l'ardoise dans l'épaisseur
    # de la baie vers l'entrée arrière (sinon seuil d'érable) et les réducteurs
    R = [B(BAIE_EAR[0], y1 - 0.1, BAIE_EAR[1], 380.1, 0, 0.12, "ardoise_noire")]
    # seuils (réducteurs) d'érable de 2¼ po : joint de gauche (salle à manger et dégagement) et joint du salon
    R += [A(x0 - 2.0, y0 + 0.2, x0 + 0.25, 364.4, 0, 0.32, "erable", r=0.3, b=0.12),
          A(272.25, y0 - 1.25, x1 - 0.2, y0 + 1.0, 0, 0.32, "erable", r=0.3, b=0.12)]
    return R


def appliquer_scene_rdc(S, h):
    # 1) retirer le coin ordi, les chaises et les tabourets de RDC-01, l'ancienne bande d'ardoise et ses seuils d'inox
    zch = [(x - 11.5, y - 11.5, x + 11.5, y + 11.5) for x, y in ANCIENNES_CHAISES]
    zta = [(x - 12, y - 12, x + 12, y + 12) for x, y in ANCIENS_TABOURETS]
    garde = []
    for o in S["mobilier"]:
        if not _protege(o):
            cx, cy = _centre(o)
            if _dans(cx, cy, ZONE_ORDI):
                continue
            if o.get("mat") in (h.CUIR, "metal") and any(_dans(cx, cy, z) for z in zch + zta):
                continue
        garde.append(o)
    S["mobilier"] = garde
    S["revetements"] = [o for o in S["revetements"]
                        if not (o.get("mat") in ("ardoise_noire", "inox") and _dans(*_centre(o), (260, 155, 318, 371)))]
    # table, luminaire et plante avancés de DX_TABLE vers la cuisine (le luminaire suit : boîtier à déplacer)
    n = 0
    for k, o in enumerate(S["mobilier"]):
        if _table_et_luminaire(o):
            S["mobilier"][k] = _decaler(o, DX_TABLE)
            n += 1
    if n < 14:
        print(f"  [rdc_cuisine] ATTENTION : {n} objets de la table et du luminaire trouvés (14 attendus)")
    for l in S.get("lumieres", []):
        if l.get("z") and _dans(l["x"], l["y"], ZONE_TABLE):
            l["x"] = l["x"] + DX_TABLE
    # 2) chaises coques rangées sous la table, tabourets assortis glissés sous l'îlot
    _verifier_chaises(h)
    M = []
    for c in chaises_rangees():
        M += chaise_coque(h, *c)
    for y in TAB_Y:
        M += tabouret_coque(h, TAB_X, y, "+x")
    # 3) garde-manger encastré
    M += _garde_manger(h)
    S["mobilier"] += M
    # 4) sol : un seul rectangle d'ardoise = la pièce Cuisine ; ardoise dans la baie, seuils d'érable
    S.setdefault("sols", {})["piece-RDC-CUI"] = "ardoise_noire"
    S["revetements"] += _sol(h)
    # 5) arrêts de visite : « Coin bureau » devient « Cuisine — rangement » (même place dans le parcours)
    arret = {"nom": "Cuisine — rangement", "x": 262, "y": 220, "cap": 186}
    v = S.get("visites", [])
    i = next((k for k, a in enumerate(v) if a.get("nom") == "Coin bureau"), None)
    if i is None:
        i = next((k + 1 for k, a in enumerate(v) if a.get("nom") == "Salle à manger"), len(v))
        v.insert(i, arret)
    else:
        v[i] = arret
    S["visites"] = v
    S.setdefault("palette", []).append(
        ["Garde-manger", "encastré dans l'ancien coin ordi : noir mat, cadre et joue de bois de grange, longues poignées noires",
         "#1E1F20"])
