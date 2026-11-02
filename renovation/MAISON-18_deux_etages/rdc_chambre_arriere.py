"""MAISON-18 — RDC : CHAMBRE DES PARENTS (chambre arrière CH1) « Lit king, rangement optimisé ».

Demande du client : « Réaménage la chambre arrière, lit king mais rangement optimisé. »

Parti pris (voir DESIGN_chambre_arriere.md) :
- LIT KING (matelas 76 × 80) tête au mur gauche (mur extérieur aveugle, x = 10) : c'est la seule orientation qui donne
  24 po et plus des deux côtés ET au pied sans toucher la porte, son arc ni la fenêtre. Plateforme noir mat 84 × 82 po à
  quatre grands tiroirs (deux par côté), socle en retrait (le lit « flotte »). Dégagements : 31 po de chaque côté,
  38¼ po au pied (jusqu'à la façade de la garde-robe).
- MUR DE TÊTE INTÉGRÉ : fourrure de 9 po devant le mur extérieur (l'isolant n'est pas touché), revêtue de vrai bois de
  grange (remplace le papier peint imitation planches) ; deux niches noir mat éclairées (DEL) au-dessus de deux chevets
  suspendus à tiroir, une niche-tablette horizontale éclairée au-dessus de la tête de lit rembourrée à canaux, deux
  liseuses murales noires articulées, prises USB-C dans chaque niche.
- GARDE-ROBE REPENSÉE : les G.R. 1 et 2 sont réunies (cloison mur-RDC-023 et montant central enlevés) en une garde-robe
  de 72 po, ouverture de 66 po à deux portes COULISSANTES (plus d'arcs dans la chambre) : panneau-miroir pleine hauteur
  à cadre noir mat devant, panneau noir mat à rainures derrière. Dedans : double penderie, tour de 4 tiroirs et
  tablettes, penderie longue et souliers, tablette haute à paniers, DEL à l'ouverture.
- Le VÉLO DE ROUTE sur base descend au gym du sous-sol (place prévue par SS-17). La commode blanche est retirée
  (tiroirs du lit, des chevets et de la garde-robe). Pas de banc au pied : il ramènerait le passage devant la
  garde-robe à 24 po (sous les 30–36 demandés).

appliquer_modifs_rdc(maison, ctx) : plan P-130 (cloison, portes, pièces, éléments, note).
appliquer_scene_rdc(S, h) : maquette (retire le mobilier RDC-01 de la chambre, ajoute le nouveau, 2 arrêts de visite).
Pouces, repère de la maison (x le long de la façade, y vers l'arrière, z vers le haut).
"""
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

SRC = "proposition MAISON-18, chambre des parents (esquisse)"

# ------------------------------------------------------------------------------------------- repères de la pièce
XG, XD, YS, YA = 10.0, 143.75, 226.0, 370.0      # nus : mur gauche (ext.), cloison des G.R., cloison S. de bain, mur arrière
XT = 19.0                                         # face du mur de tête (fourrure de 9 po)
YC = 298.0                                        # axe du lit (milieu de la chambre en y)
PX0, PX1, PY0, PY1 = 21.5, 105.5, 257.0, 339.0    # plateforme king 84 × 82 (matelas 76 × 80 : x 23–103, y 260–336)
GX0, GX1, GY0, GY1 = 148.25, 172.75, 298.25, 370.0  # garde-robe réunie (nu intérieur)
OY0, OY1 = 302.0, 368.0                           # baie coulissante dans mur-RDC-021 (66 po)
NICHES = [(230.0, 250.0, 32.0, 64.0), (346.0, 366.0, 32.0, 64.0)]   # niches latérales (y0, y1, z0, z1), 6 po de creux
TABLETTE = (256.0, 340.0, 54.0, 64.0)                               # niche-tablette au-dessus de la tête de lit

# emprise de la chambre (pour retirer le mobilier RDC-01) : chambre, retrait de la porte, fenêtre (store dans l'embrasure)
ZONE = [(9.0, 221.0, 146.5, 373.0)]


# ===================================================================================================== plan (P-130)
def _dim(v, src="PRÉSUMÉ", note=None):
    d = {"valeur": v, "source": src, "photo": None}
    if note:
        d["note"] = note
    return d


def _elem(eid, typ, nom, lib, x, y, rot, L, W, note=None):
    e = {"id": eid, "type": typ, "nom": nom, "nom_original": None, "etat": "nouveau",
         "position": {"x": x, "y": y, "rotation_deg": rot, "source": "PRÉSUMÉ"},
         "dimensions": {"longueur": _dim(L), "largeur": _dim(W)}, "note": note or SRC, "libelle": lib}
    return e


ELEMENTS = [  # rotation : 270 = dos au mur gauche (x = 10), 90 = dos au mur de droite ; (longueur, largeur) en repère local
    _elem("elem-RDC-CH1-LIT", "autre", "Lit king sur plateforme noir mat 84 × 82 po (matelas 76 × 80), 4 tiroirs (2 par côté), "
          "socle en retrait ; 31 po de chaque côté, 38 po au pied", "LIT KING", (PX0 + PX1) / 2, YC, 270, PY1 - PY0, PX1 - PX0),
    _elem("elem-RDC-CH1-TETE", "autre", "Mur de tête intégré : fourrure de 9 po revêtue de bois de grange, 2 niches noir mat "
          "éclairées (USB-C), niche-tablette éclairée, tête rembourrée, 2 liseuses murales", "", (XG + XT) / 2, (YS + YA) / 2,
          270, YA - YS, XT - XG),
    _elem("elem-RDC-CH1-CHEV1", "autre", "Chevet suspendu noir mat à tiroir (dessus à 25 po)", "", 27.0, 240.0, 270, 22, 16),
    _elem("elem-RDC-CH1-CHEV2", "autre", "Chevet suspendu noir mat à tiroir (dessus à 25 po)", "", 27.0, 356.0, 270, 22, 16),
    _elem("elem-RDC-CH1-GRTIR", "armoires", "Garde-robe : tour de 4 tiroirs et tablettes (entre la double penderie et la "
          "penderie longue)", "", 160.875, 335.25, 90, 22, 22.75),
]

RETIRER_MURS = {"mur-RDC-023"}                       # cloison entre les G.R. 1 et 2
RETIRER_OUV = {"ouv-RDC-019", "ouv-RDC-020"}         # leurs deux portes battantes de 28 po (arcs dans la chambre)
RETIRER_PIECES = {"piece-RDC-GR1", "piece-RDC-GR2"}


def _niv(maison, nid):
    return next(n for n in maison["niveaux"] if n["id"] == nid)


def appliquer_modifs_rdc(maison, ctx):
    rdc = ctx.get("rdc") or _niv(maison, "RDC")
    # 1) G.R. 1 et 2 réunies : la cloison et les deux portes battantes partent (gardées dans les « retirés »)
    for cle, cle_ret, ids in (("murs", "murs_retires", RETIRER_MURS), ("ouvertures", "ouvertures_retirees", RETIRER_OUV)):
        partis = [x for x in rdc.get(cle, []) if x.get("id") in ids]
        rdc[cle] = [x for x in rdc.get(cle, []) if x.get("id") not in ids]
        deja = {x.get("id") for x in rdc.get(cle_ret) or []}
        rdc.setdefault(cle_ret, [])
        rdc[cle_ret] += [dict(x, note=(x.get("note") or "") + " — retiré : G.R. 1 et 2 réunies (" + SRC + ").")
                         for x in partis if x.get("id") not in deja]
    murs = {m["id"]: m for m in rdc["murs"]}
    m21 = murs.get("mur-RDC-021")
    if m21 and not any(o.get("id") == "ouv-RDC-CH1-GR" for o in rdc["ouvertures"]):
        y0 = min(m21["y1"], m21["y2"])
        rdc["ouvertures"].append({
            "id": "ouv-RDC-CH1-GR", "type": "porte", "operation": "coulissante", "mur_id": "mur-RDC-021", "etat": "nouveau",
            "position": _dim(round((OY0 + OY1) / 2 - y0, 2), "PRÉSUMÉ", "baie de 66 po, y 302 à 368 (retours de 4 et 2 po)"),
            "largeur": _dim(OY1 - OY0), "hauteur": _dim(80), "allege": {"valeur": None, "source": "ILLISIBLE", "photo": None},
            "note": "Garde-robe des parents : 2 portes coulissantes de 34 po (miroir pleine hauteur à cadre noir mat devant, "
                    "panneau noir mat à rainures derrière), rail encastré. Remplace les 2 portes battantes de 28 po ; "
                    "mur-RDC-021 porteur INCONNU : linteau à valider avec un professionnel (" + SRC + ")."})
    # 2) pièces : la chambre devient « Chambre des parents » ; G.R. 1 + G.R. 2 → une seule garde-robe
    pieces = [p for p in rdc["pieces"] if p["id"] not in RETIRER_PIECES]
    if not any(p["id"] == "piece-RDC-GRP" for p in pieces):
        P = orient(Polygon([(GX0, GY0), (GX1, GY0), (GX1, GY1), (GX0, GY1)]), 1.0)
        pieces.append({"id": "piece-RDC-GRP", "nom": "G.R.", "nom_original": None, "etat": "nouveau",
                       "description": "Garde-robe des parents (G.R. 1 et 2 réunies) : double penderie, tour de tiroirs, "
                                      "penderie longue, tablette haute ; portes coulissantes — " + SRC,
                       "polygone": [[round(a, 2), round(b, 2)] for a, b in list(P.exterior.coords)[:-1]],
                       "superficie": _dim(round(P.area / 144, 1), "DÉDUIT", "aire du polygone au nu intérieur"),
                       "hauteur_plafond": {"valeur": None, "source": "ILLISIBLE", "photo": None, "note": "non écrite"},
                       "dimensions": {"x": _dim(round(GX1 - GX0, 2), "DÉDUIT"), "y": _dim(round(GY1 - GY0, 2), "DÉDUIT")}})
    for p in pieces:
        if p["id"] == "piece-RDC-CH1":
            p["nom"] = "Chambre des parents"
            p["description"] = ("Chambre des parents (ancienne chambre arrière) : lit king tête au mur gauche, mur de tête "
                                "intégré à niches éclairées, garde-robe réunie à portes coulissantes — " + SRC)
    rdc["pieces"] = pieces
    # 3) éléments : mobilier intégré de la chambre et de la garde-robe
    ids = {e["id"] for e in ELEMENTS}
    rdc["elements"] = [e for e in rdc["elements"] if e["id"] not in ids] + [dict(e) for e in ELEMENTS]
    rdc["elements"].sort(key=lambda e: e["id"])
    # 4) note de la proposition (courte : le cartouche est petit)
    rdc.setdefault("notes", [])
    if not any(n.get("id") == "note-RDC-CH1-01" for n in rdc["notes"]):
        rdc["notes"].append({"id": "note-RDC-CH1-01", "texte_original": None, "photo": None,
                             "interpretation": "Chambre des parents : lit king tête au mur gauche (31 po de chaque côté, 38 au "
                                               "pied), mur de tête intégré ; G.R. 1 et 2 réunies, portes coulissantes ; "
                                               "le vélo descend au gym."})


# ====================================================================================================== maquette 3D
def _bornes(o):
    """Emprise en plan (x0, y0, x1, y1) d'un objet de S["mobilier"] ou S["revetements"], ou None."""
    f = o.get("forme")
    if "x0" in o and "y0" in o:
        return o["x0"], o["y0"], o["x1"], o["y1"]
    if f == "cylindre":
        r = max(o.get("r", 0), o.get("r2", 0))
        if o.get("axe") == "y" and "y0" in o:
            return o["x"] - r, o["y0"], o["x"] + r, o["y1"]
        if o.get("axe") == "x" and "x0" in o:
            return o["x0"], o["y"] - r, o["x1"], o["y"] + r
        return o["x"] - r, o["y"] - r, o["x"] + r, o["y"] + r
    if f == "tube" or "pts" in o:
        xs, ys = [p[0] for p in o["pts"]], [p[1] for p in o["pts"]]
        return min(xs), min(ys), max(xs), max(ys)
    if "x" in o and "y" in o:
        r = o.get("R", o.get("r", 0)) or 0
        return o["x"] - r, o["y"] - r, o["x"] + r, o["y"] + r
    return None


def _dans_zone(o):
    b = _bornes(o)
    if b is None:
        return False
    return any(zx0 <= b[0] and b[2] <= zx1 and zy0 <= b[1] and b[3] <= zy1 for zx0, zy0, zx1, zy1 in ZONE)


def _decoupe(y0, y1, z0, z1, trous):
    """Rectangles (ya, yb, za, zb) qui couvrent [y0, y1] × [z0, z1] moins les trous (y0, y1, z0, z1) ; tranches fusionnées."""
    ys = sorted({y0, y1} | {v for t in trous for v in (t[0], t[1]) if y0 < v < y1})
    tranches = []
    for ya, yb in zip(ys, ys[1:]):
        zs = [(t[2], t[3]) for t in trous if t[0] <= ya and yb <= t[1]]
        libres, z = [], z0
        for za, zb in sorted(zs):
            if za > z:
                libres.append((z, za))
            z = max(z, zb)
        if z < z1:
            libres.append((z, z1))
        if tranches and tranches[-1][2] == libres and abs(tranches[-1][1] - ya) < 1e-9:
            tranches[-1][1] = yb
        else:
            tranches.append([ya, yb, libres])
    return [(ya, yb, za, zb) for ya, yb, libres in tranches for za, zb in libres]


def _mobilier(h, fen=None):
    A, B, C, CX, CY, T = h.A, h.B, h.C, h.CX, h.CY, h.T
    NOIR = "noir-mat"
    M = []

    # ------------------------------------------------------------ mur de tête intégré (bois de grange, niches éclairées)
    trous = NICHES + [TABLETTE]
    M += [B(13.0, ya, XT, yb, za, zb, "bois_grange") for ya, yb, za, zb in _decoupe(YS, YA, 0.0, 96.0, trous)]
    M += [B(10.0, YS, 13.0, YA, 0.0, 96.0, "gypse")]                                  # fourrure (dos, caché)
    for y0, y1, z0, z1 in trous:
        p = 13.0 if (y0, y1, z0, z1) != TABLETTE else 14.0                              # tablette : 5 po de creux
        M += [B(p, y0, p + 0.5, y1, z0, z1, NOIR),                                       # fond
              B(p, y0, XT, y0 + 0.5, z0, z1, NOIR), B(p, y1 - 0.5, XT, y1, z0, z1, NOIR),  # joues
              B(p, y0, XT, y1, z0, z0 + 0.5, NOIR), B(p, y0, XT, y1, z1 - 0.5, z1, NOIR),  # fond et dessus
              B(XT - 1.6, y0 + 1, XT - 0.6, y1 - 1, z1 - 0.95, z1 - 0.5, "spot")]         # DEL sous le dessus
    for y0, y1, z0, z1 in NICHES:                                                       # prises USB-C (fond de niche)
        yp = y0 + 3.5 if y0 < YC else y1 - 6.25
        M += [B(13.5, yp, 13.75, yp + 2.75, z0 + 1.5, z0 + 6, "blanc"),
              B(13.75, yp + 0.8, 13.85, yp + 1.2, z0 + 3.0, z0 + 3.8, "carbone"), B(13.75, yp + 1.55, 13.85, yp + 1.95, z0 + 3.0, z0 + 3.8, "carbone")]
    # objets dans les niches : livres, petit vase, photo encadrée (génériques)
    M += [B(14.5, 233, 18, 233.9, 32.5, 41.5, "carbone"), B(14.5, 234, 18, 235.1, 32.5, 40.5, "draps"),
          B(14.5, 235.2, 18, 236.0, 32.5, 42.0, "jete"), C(16.0, 244.0, 1.8, 32.5, 41.0, "blanc", r2=1.2),
          B(14.5, 350, 15.3, 360, 32.5, 42.5, "metal"), B(15.3, 351.2, 15.5, 358.8, 33.7, 41.3, "jete"),
          C(16.2, 363.0, 1.5, 32.5, 37.0, "osier")]
    M += [B(14.6, 276, 15.4, 286, 54.5, 62.5, "metal"), B(15.4, 277, 15.6, 285, 55.5, 61.5, "draps"),
          B(14.6, 310, 15.4, 318, 54.5, 61.0, "laiton"), B(15.4, 311, 15.6, 317, 55.5, 60.0, "carbone"),
          C(16.5, 296.0, 1.6, 54.5, 60.5, "blanc", r2=1.0), B(14.6, 325, 18.0, 331, 54.5, 56.0, "carbone")]
    # tête de lit rembourrée à canaux verticaux (tissu), sur panneau noir
    M += [B(XT, 255.0, XT + 0.6, 341.0, 12.0, 50.0, NOIR)]
    w = (341.0 - 255.0) / 7
    M += [A(XT + 0.5, 255.0 + i * w + 0.2, XT + 3.0, 255.0 + (i + 1) * w - 0.2, 12.0, 50.0, "tissu", r=1.0, b=0.8) for i in range(7)]
    # chevets suspendus noir mat à tiroir (dessus à 25 po), sous les niches
    for y0, y1 in ((229.0, 251.0), (345.0, 367.0)):
        M += [A(XT, y0, 35.0, y1, 17.0, 25.0, NOIR, r=0.4, b=0.3),
              B(34.85, y0 + 0.6, 35.05, y1 - 0.6, 22.9, 23.1, "carbone"),               # joint du tiroir
              B(34.8, y0 + 5, 35.0, y1 - 5, 23.6, 24.2, "carbone")]                     # prise de doigt
    M += [A(22, 232, 31, 244, 25, 26.4, "blanc", r=0.3, b=0.2), A(22.5, 232.5, 30.5, 243, 26.4, 27.5, "carbone", r=0.3, b=0.2),
          C(28.0, 360.0, 1.6, 25.0, 30.5, "verre-clair"), A(22, 348, 30, 356, 25, 26.2, "jete", r=0.3, b=0.2)]
    # liseuses murales articulées noires (bras vers l'oreiller), sur le bois entre niche et tête de lit
    for yb, sg in ((252.75, 1), (343.25, -1)):
        ys = yb + sg * 4.0
        M += [CX(XT, XT + 0.9, yb, 52.0, 1.5, "metal"),
              T([(XT + 0.9, yb, 52.0), (XT + 6.5, yb, 52.5), (XT + 9.5, ys, 51.0)], 0.22, "metal"),
              C(XT + 9.5, ys, 1.9, 47.6, 50.8, "metal", r2=1.0), C(XT + 9.5, ys, 1.6, 47.45, 47.65, "spot")]

    # ------------------------------------------------------------ lit king sur plateforme noir mat à 4 tiroirs
    M += [B(PX0 + 3, PY0 + 3, PX1 - 3, PY1 - 3, 0.0, 3.0, "carbone"),                  # socle en retrait (lit « flottant »)
          A(PX0, PY0, PX1, PY1, 3.0, 12.5, NOIR, r=0.6, b=0.4)]
    for yf, s in ((PY0, -1), (PY1, 1)):                                                # façades des tiroirs (2 par côté)
        ya, yb = (yf - 0.15, yf + 0.05) if s < 0 else (yf - 0.05, yf + 0.15)
        for x0, x1 in ((37.5, 70.25), (71.0, 103.75)):
            M += [B(x0 - 0.12, ya, x0 + 0.12, yb, 3.6, 12.0, "carbone"),                   # joint
                  B(x0 + 7, ya, x1 - 7, yb, 10.9, 11.7, "carbone")]                      # prise de doigt
        M += [B(103.63, ya, 103.87, yb, 3.6, 12.0, "carbone")]
    M += [A(23.0, 260.0, 103.0, 336.0, 12.5, 23.0, "draps", r=3, b=2.5),               # matelas
          A(46.0, 259.4, 103.8, 336.6, 21.8, 24.6, "draps", r=2.5, b=1.6),             # couette
          A(44.0, 259.3, 49.0, 336.7, 22.6, 25.6, "draps", r=2.0, b=1.4),              # rabat de la couette
          A(86.0, 258.8, 104.4, 337.2, 24.4, 25.6, "jete", r=2.0, b=0.5),              # jeté au pied
          A(103.6, 262.0, 105.2, 334.0, 15.0, 25.6, "jete", r=0.6, b=0.3),
          A(23.5, 261.5, 40.0, 296.5, 21.5, 28.5, "draps", r=4, b=3),                  # oreillers king
          A(23.5, 299.5, 40.0, 334.5, 21.5, 28.5, "draps", r=4, b=3),
          A(38.5, 270.0, 44.0, 292.0, 22.5, 33.0, "osier", r=2.5, b=2),               # coussins d'accent
          A(38.5, 304.0, 44.0, 326.0, 22.5, 33.0, "osier", r=2.5, b=2),
          A(42.5, 288.0, 47.5, 308.0, 22.5, 30.0, "jete", r=2.4, b=2)]
    # tapis de laine 8 × 8½ pi sous les deux tiers du lit (hors de l'arc de la porte)
    M += [A(44.0, 246.0, 140.0, 350.0, 0.0, 0.45, "tapis", r=1, b=0.2)]

    # ------------------------------------------------------------ garde-robe réunie (intérieur)
    M += [B(GX0, GY0, GX1, GY1, 84.0, 85.0, "placage")]                                # tablette haute continue
    M += [A(150.5 + 0.0, y, 167.5, y + 13.0, 85.0, 93.0, "osier", r=1, b=0.5) for y in (300.5, 316.0, 331.5, 347.0)]
    M += [B(GX0 + 0.3, 300.0, GX0 + 1.1, 368.0, 83.3, 83.9, "spot")]                    # DEL de l'ouverture
    # section A : double penderie (tringles noires à 41 et 81 po)
    LINGE = ["carbone", "draps", "jete", "tissu", "blanc", "osier", "carbone", "cuir", "tissu", "draps"]
    for zr in (41.0, 81.0):
        M += [CY(160.5, GY0, 324.25, zr, 0.55, "metal")]
        M += [B(152.0, 300.0 + k * 2.4, 169.0, 300.75 + k * 2.4, zr - 32.0, zr - 1.2, LINGE[(k + int(zr)) % len(LINGE)]) for k in range(9)]
    # section B : tour de 4 tiroirs (placage, poignées noires) et tablettes à chandails
    M += [A(149.6, 324.25, 172.6, 346.25, 0.0, 40.0, "placage", r=0.3, b=0.2),
          B(149.4, 324.6, 149.6, 345.9, 0.0, 3.5, "carbone")]
    for z in (12.5, 21.5, 30.5):
        M += [B(149.45, 324.6, 149.6, 345.9, z - 0.12, z + 0.12, "carbone")]
    M += [B(149.0, 332.75, 149.4, 337.75, z, z + 0.6, "metal") for z in (9.5, 18.5, 27.5, 36.5)]
    M += [B(149.6, 324.25, 172.6, 325.0, 40.0, 84.0, "placage"), B(149.6, 345.5, 172.6, 346.25, 40.0, 84.0, "placage")]
    for z in (52.0, 64.0, 76.0):
        M += [B(149.6, 325.0, 172.6, 345.5, z, z + 0.75, "placage"),
              A(152.0, 326.5, 166.0, 344.0, z + 0.75, z + 5.5, LINGE[int(z) % len(LINGE)], r=1, b=0.6)]
    M += [A(152.0, 326.5, 166.0, 344.0, 40.0, 44.5, "tissu", r=1, b=0.6)]
    # section C : penderie longue (tringle à 68 po) et souliers
    M += [CY(160.5, 346.25, GY1, 68.0, 0.55, "metal")]
    M += [B(152.0, 348.0 + k * 2.9, 169.0, 348.8 + k * 2.9, 22.0, 66.8, LINGE[(k + 3) % len(LINGE)]) for k in range(6)]
    M += [B(149.6, 346.25, 172.6, GY1, 6.0, 6.75, "placage")]
    M += [A(151.0, y, 161.0, y + 3.4, 6.75, 10.5, m, r=1.2, b=0.6) for y, m in ((348.5, "carbone"), (353.0, "cuir"), (357.5, "blanc"), (362.0, "carbone"))]
    # portes coulissantes (rail encastré) : miroir devant (au repos à droite), panneau noir glissé derrière lui
    M += [B(144.0, OY0, 148.0, OY1, 79.4, 80.0, "metal")]                              # rail
    M += [B(144.0, 334.0, 145.3, OY1, 0.5, 79.3, NOIR),                                # vantail avant : cadre noir mat
          B(143.8, 335.5, 144.0, OY1 - 1.5, 2.0, 77.8, "miroir"),                      # miroir pleine hauteur
          B(146.4, 334.0, 147.7, OY1, 0.5, 79.3, NOIR)]                                # vantail arrière (glissé derrière)
    M += [B(147.7, 334.6, 147.9, 335.0, 4, 76, "carbone")]
    M += [B(146.3, y, 146.4, y + 0.2, 1.0, 79.0, "carbone") for y in range(336, 367, 3)]   # rainures (face chambre)
    M += [B(143.55, 365.0, 143.8, 366.2, 30.0, 50.0, "metal")]                         # tirette noire

    # ------------------------------------------------------------ fenêtre : rideau de lin pleine hauteur, store opaque
    # un seul grand panneau qui se range côté lit (x < 61) : le coin entre la fenêtre et la garde-robe reste libre
    M += [B(45.0, 365.4, 138.0, 366.2, 93.6, 94.6, "metal")]                           # rail au plafond
    for x0, x1 in ((45.5, 61.5),):
        n = max(2, int((x1 - x0) / 2.3))
        pas = (x1 - x0) / n
        M += [A(x0 + k * pas, 362.4 + (0.9 if k % 2 else 0), x0 + (k + 1) * pas + 0.4, 364.6 + (0.9 if k % 2 else 0),
                0.8, 93.6, "draps", r=1.0, b=0.4) for k in range(n)]
    # (2026-11-02) le store suit la tête de la fenêtre : 80 po dans la vidéo DAG (fen = SCENE["fenetres"]), 82 avant
    te = ((fen or {}).get("ouv-RDC-003") or {}).get("tete", 82)
    M += [B(61.0, 371.0, 135.0, 371.6, te - 12.0, te, "tissu"), B(60.5, 370.6, 135.5, 372.0, te - 1.0, te, "metal")]

    # ------------------------------------------------------------ cloison du pied (x = 143,75) : une seule œuvre encadrée
    M += h.cadre_mur_x(XD, 256.0, 290.0, 40.0, 74.0, "jete", sens=-1, cadre="metal")
    M += [B(142.3, 266.0, 142.45, 282.0, 46.0, 68.0, "osier")]                         # aplat ocre (générique)
    return M


def appliquer_scene_rdc(S, h):
    # 1) le mobilier RDC-01 de la chambre part (lit queen, chevet, cadres, suspension cage, commode, vélo, store marine,
    #    papier peint imitation planches, panier) ; la lampe de la suspension aussi
    S["mobilier"][:] = [o for o in S.get("mobilier", []) if not _dans_zone(o)]
    S["revetements"][:] = [o for o in S.get("revetements", []) if not _dans_zone(o)]
    S["lumieres"][:] = [l for l in S.get("lumieres", []) if not (ZONE[0][0] < l["x"] < ZONE[0][2] and ZONE[0][1] < l["y"] < ZONE[0][3])]
    # 2) mobilier proposé
    S["mobilier"] += _mobilier(h, S.get("fenetres"))
    # 3) éclairage : 4 encastrés autour du lit (pas au-dessus des oreillers), 1 dans la garde-robe, lueur du mur de tête
    S["lumieres"] += [{"x": 40, "y": 242, "i": 5}, {"x": 40, "y": 354, "i": 5}, {"x": 124, "y": 254, "i": 6},
                      {"x": 124, "y": 342, "i": 6}, {"x": 160.5, "y": 334, "i": 4}, {"x": 24, "y": YC, "z": 66, "i": 2}]
    # 4) peinture : murs lin chaud (le bois de grange et le noir mat ressortent sans « tout blanc »)
    S.setdefault("peintures", {})["Lin chaud"] = ["#E2D9CB", "chambre des parents : murs (greige chaud ; teinte à choisir sur échantillon)"]
    S.setdefault("peinture", {})["piece-RDC-CH1"] = "Lin chaud"
    # 5) arrêts de visite : remplacent ceux de la chambre arrière, au même endroit du parcours
    v = S.get("visites", [])
    i = next((k for k, x in enumerate(v) if x["nom"].startswith("Chambre arrière")), len(v))
    v[:] = [x for x in v if not x["nom"].startswith("Chambre arrière")]
    v[i:i] = [{"nom": "Chambre des parents", "x": 131, "y": 234, "cap": 152},
              {"nom": "Chambre des parents, garde-robe", "x": 52, "y": 356, "cap": 350}]
    # 6) palette
    pal = [p for p in S.get("palette", []) if not p[0].startswith("Chambre arrière")]
    pal.append(["Chambre des parents", "mur de tête intégré en bois de grange (niches noir mat éclairées, liseuses, USB-C), "
                "lit king sur plateforme noir mat à tiroirs, tête rembourrée, murs lin chaud, garde-robe à portes coulissantes "
                "(miroir) et double penderie", "#8A6E55"])
    S["palette"] = pal
