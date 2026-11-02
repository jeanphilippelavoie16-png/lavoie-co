"""MAISON-18 — RDC, zone « coin café et salle de bain » (client, 2026-11-02).

Demande du client : « En haut dans la pièce qui sert à sortir dehors sur le balcon de piscine, je veux un coin café, avec la
machine à café et tout. » — « Enlève les laveuse-sécheuse en haut et fais de l'espace de rangement, mais quelque chose
d'original. »

Ce module (appelé par modifs.py et scene_3d.py, après rdc_cuisine) :
1. ENTRÉE ARRIÈRE (piece-RDC-EAR, nu intérieur x 229..317, y 380..430, 88 × 50 po) → « Coin café ».
   - La descente de l'entrée arrière (elem-RDC-R-ESCARR, ESTIMÉE sur les photos 01, 07, 08) est refermée par un plancher à
     niveau : avec elle, la pièce n'est qu'un palier et une cage d'escalier (aucun mur libre avec 36 po devant). Le sous-sol
     garde l'escalier principal (neuf, à l'entrée avant) et sa porte de côté ; dessous, l'ancien caveau est déjà le walk-in de
     la chambre 2 (SS-17). Option B (volée gardée) : voir DESIGN_cafe_sdb.md.
   - Coin café de 50 po sur le mur de gauche (x = 229), le seul mur plein : caissons noir mat de 24 po (petit frigo 24 po à
     porte vitrée noire pour le lait, 3 tiroirs : grains et capsules, tasses, filtres), comptoir de bois de grange à 36¼ po,
     dosseret et mur de brique rouge (la brique de la cuisine), 2 tablettes flottantes de bois de grange à DEL (tasses, bocaux),
     2 prises doubles (circuit de 20 A pour la machine). Machine espresso inox, moulin, pichet à lait.
   - Passages : 62 po libres entre le nez du comptoir (x = 254¾) et le mur du palier (x = 317), 42 po quand quelqu'un se
     fait un café ; la baie de la salle à manger (x 279..311) et l'arc de la porte extérieure (x 283..317, y 392..426)
     restent vides.
   - Pas d'évier : l'évier de la cuisine est à ≈ 3,5 m et les trois murs de la pièce sont extérieurs (gel) ; voir DESIGN.
2. SALLE DE BAIN : laveuse et sécheuse empilées (elem-RDC-R-LAV) enlevées → « colonne d'apothicaire » dans leur niche
   (x 76,2..105,75, y 144,25..168,25, 29½ × 24 po, pleine hauteur) : 2 paniers à linge basculants (pâle / foncé) en bas,
   6 tiroirs d'apothicaire en bois de grange (porte-étiquettes noirs : un tiroir par membre de la famille), niche éclairée
   où les serviettes roulées sont cordées comme du bois de chauffage, armoire du haut (réserves) ; noir mat comme la vanité.
   La chute à linge vers la salle de lavage du sous-sol a été étudiée (option B, conditionnelle) : voir DESIGN_cafe_sdb.md.
3. PORTE DE LA SALLE DE LAVAGE (sous-sol, « pas capable d'ouvrir ») : corrigée dans zone_gym.py (le miroir de sa face gym
   était un décor fixe devant la porte ; il est maintenant lié à la porte). Rien à faire ici ; voir DESIGN_cafe_sdb.md.
Pouces, repère de la maison (x le long de la façade, y vers l'arrière, z depuis le plancher du RDC).
"""
import copy

SOURCE = "proposition MAISON-18 (esquisse) — coin café et salle de bain (client, 2026-11-02)"

# ------------------------------------------------------------------------------------------------ repères
# entrée arrière (nu intérieur) ; mur de gauche x = 224 (10 po) → face 229 ; mur du palier x = 322 → face 317
EAR = (229.0, 380.0, 317.0, 430.0)
XG = 229.0                         # face du mur de gauche (mur-RDC-005)
BRIQUE = 0.55                      # placage de brique mince (comme la cuisine)
XB = XG + BRIQUE                   # face de la brique
P_CAISSON = 24.0                   # profondeur des caissons
XF = XB + P_CAISSON                # face des portes et des tiroirs (253,55)
XC = XF + 1.25                     # nez du comptoir (254,8)
Y_CAFE = (380.0, 430.0)            # le coin café occupe tout le mur de gauche (50 po)
FRIGO = (380.75, 404.75)           # petit frigo 24 po (lait), porte vitrée noire, pentures côté mur avant
TIROIRS = (405.25, 429.45)         # 3 tiroirs (grains et capsules en haut)
Z_CPT = (34.5, 36.25)              # comptoir de bois de grange (dessus à 36¼ po)
Z_TAB = (58.0, 72.0)               # tablettes flottantes (22 po au-dessus du comptoir, puis 14 po)
P_TAB = 11.0                       # profondeur des tablettes
MACHINE = (412.0, 424.0)           # machine espresso (largeur sur y)
MOULIN = (400.5, 407.0)
ARC_PORTE_EAR = (283.0, 392.0, 317.0, 426.0)   # porte extérieure ouv-RDC-027 : pivot (317, 425,5), vantail de 33 po
BAIE_EAR = (279.0, 311.0)          # baie salle à manger / entrée arrière (ouv-RDC-026), sans porte
TREMIE_EAR = [229, 398, 284, 430]  # trou de plancher que base_rdc01_scene demandait pour la volée (retiré : plancher à niveau)

# salle de bain : niche de la laveuse-sécheuse entre le muret de la douche (face x = 76,2) et la cloison du dégagement
# (mur-RDC-011, axe x = 108, face 105,75) ; fond : cloison salle de bain / bureau (mur-RDC-R01, axe y = 142, face 144,25)
NICHE = (76.2, 144.25, 105.75, 172.0)
NICHE_3D = (76.2, 144.25, 105.75, 173.5)          # + hublots et boutons des appareils (jusqu'à y = 172,9)
COL = (76.2, 144.25, 105.75, 168.25)           # colonne d'apothicaire, 29,55 × 24 po
YF = COL[3] - 0.75                             # dos des façades (167,5) ; façades de ¾ po
Z_PANIERS = (4.0, 30.0)
Z_APOTH = (30.0, 62.0)                         # 3 rangées de tiroirs
Z_NICHE = (62.0, 84.0)                         # niche ouverte éclairée (serviettes roulées)
Z_HAUT = (84.0, 96.0)

RETIRES = {"elem-RDC-R-LAV": "laveuse et sécheuse enlevées (client, 2026-11-02) : colonne d'apothicaire à leur place ; "
                             "entrées d'eau, renvoi et prise de la sécheuse condamnés dans le mur, sortie de la sécheuse "
                             "bouchée (à faire par un plombier et un électricien)",
           "elem-RDC-R-ESCARR": "descente de l'entrée arrière refermée par un plancher à niveau pour le coin café "
                                "(option A, à valider : voir DESIGN_cafe_sdb.md)"}


def dim(v, note=None, src="PRÉSUMÉ"):
    d = {"valeur": v, "source": src, "photo": None}
    if note:
        d["note"] = note
    return d


def _element(eid, typ, nom, lib, x, y, rot, L, W, note=None):
    e = {"id": eid, "type": typ, "nom": nom, "nom_original": None, "etat": "nouveau",
         "position": {"x": round(x, 3), "y": round(y, 3), "rotation_deg": rot, "source": "PRÉSUMÉ"},
         "dimensions": {"longueur": dim(round(L, 2)), "largeur": dim(round(W, 2))}, "note": note or SOURCE}
    if lib is not None:
        e["libelle"] = lib
    return e


# =============================================================================================== plan (maison.json)
def appliquer_modifs_rdc(maison, ctx):
    rdc = ctx["rdc"]
    # 1) éléments retirés : laveuse-sécheuse de la salle de bain, descente de l'entrée arrière
    partis = [e for e in rdc["elements"] if e["id"] in RETIRES]
    rdc["elements"] = [e for e in rdc["elements"] if e["id"] not in RETIRES]
    deja = {e["id"] for e in rdc.get("elements_retires", [])}
    for e in partis:
        if e["id"] in deja:
            continue
        e = copy.deepcopy(e)
        e["note"] = (e.get("note") or "") + " — RETIRÉ, MAISON-18 : " + RETIRES[e["id"]] + "."
        rdc.setdefault("elements_retires", []).append(e)

    # 2) éléments nouveaux
    yc = (Y_CAFE[0] + Y_CAFE[1]) / 2
    els = [
        _element("elem-RDC-C-CAFE", "comptoir",
                 "Coin café : comptoir de bois de grange (dessus à 36¼ po) sur caissons noir mat de 24 po, 3 tiroirs (grains et "
                 "capsules, tasses, filtres), machine espresso, moulin ; dosseret et mur de brique rouge ; 2 tablettes "
                 "flottantes de bois de grange à DEL (58 et 72 po) ; 2 prises doubles (circuit de 20 A)",
                 None, XG + (XC - XG) / 2, yc, 270, Y_CAFE[1] - Y_CAFE[0], XC - XG),
        _element("elem-RDC-C-FRIGO", "refrigerateur",
                 "Petit frigo de 24 po sous le comptoir (lait), porte vitrée noire, ventilation par l'avant, pentures côté mur avant",
                 "FR.", XB + P_CAISSON / 2, (FRIGO[0] + FRIGO[1]) / 2, 270, FRIGO[1] - FRIGO[0], P_CAISSON),
        _element("elem-RDC-S-APOTH", "armoires",
                 "Colonne d'apothicaire pleine hauteur (29½ × 24 po) à la place de la laveuse-sécheuse : 2 paniers à linge "
                 "basculants (pâle / foncé), 6 tiroirs de bois de grange à porte-étiquettes noirs (un par membre de la famille), "
                 "niche éclairée de serviettes roulées, armoire du haut ; caisson noir mat comme la vanité",
                 None, (COL[0] + COL[2]) / 2, (COL[1] + COL[3]) / 2, 0, COL[2] - COL[0], COL[3] - COL[1]),
    ]
    ids = {e["id"] for e in els}
    rdc["elements"] = [e for e in rdc["elements"] if e["id"] not in ids] + els
    rdc["elements"].sort(key=lambda e: e["id"])

    # 3) pièces : l'entrée arrière devient « Coin café » (même polygone), la salle de bain garde le sien
    for p in rdc["pieces"]:
        if p["id"] == "piece-RDC-EAR":
            p["nom"] = "Coin café"
            p["description"] = ("Entrée arrière vers le palier de la piscine, avec coin café sur le mur de gauche ; descente refermée "
                                "par un plancher à niveau (option A) — " + SOURCE)
        elif p["id"] == "piece-RDC-SDB":
            p["description"] = ((p.get("description") or "Salle de bain") + " ; laveuse-sécheuse remplacées par une colonne "
                                "d'apothicaire pleine hauteur — " + SOURCE)


# =============================================================================================== 3D (SCENE du RDC)
def _bornes(o):
    """Emprise en plan (x0, y0, x1, y1) d'un objet de la scène, ou None."""
    if "x0" in o and "y0" in o and "x1" in o and "y1" in o:
        return o["x0"], o["y0"], o["x1"], o["y1"]
    if o.get("forme") == "tube" and o.get("pts"):
        xs, ys = [p[0] for p in o["pts"]], [p[1] for p in o["pts"]]
        return min(xs), min(ys), max(xs), max(ys)
    if o.get("forme") == "cylindre":
        r = max(o.get("r", 0), o.get("r2", 0))
        if o.get("axe") == "y":
            return o["x"] - r, o["y0"], o["x"] + r, o["y1"]
        if o.get("axe") == "x":
            return o["x0"], o["y"] - r, o["x1"], o["y"] + r
        return o["x"] - r, o["y"] - r, o["x"] + r, o["y"] + r
    if "x" in o and "y" in o:
        r = o.get("R", o.get("r", 0)) if o.get("forme") in ("tore", "sphere") else 0
        return o["x"] - r, o["y"] - r, o["x"] + r, o["y"] + r
    return None


def _dedans(o, zone, marge=0.6):
    """Objet entièrement compris dans zone (x0, y0, x1, y1) à la marge près."""
    b = _bornes(o)
    if b is None:
        return False
    return b[0] >= zone[0] - marge and b[1] >= zone[1] - marge and b[2] <= zone[2] + marge and b[3] <= zone[3] + marge


def _coin_cafe(h):
    B, A, C, T, CX, MOD = h.B, h.A, h.C, h.T, h.CX, h.MOD
    NOIR = getattr(h, "NOIR", "noir-mat")
    out = []
    y0, y1 = Y_CAFE
    # socle en retrait, filler côté mur avant, caisson des tiroirs, séparation frigo / tiroirs
    out += [B(XB, y0 + 1, XF - 2.5, y1 - 0.5, 0, 4, "carbone"),
            B(XB, y0, XF, FRIGO[0], 0, Z_CPT[0], NOIR),
            B(XB, FRIGO[1], XF, TIROIRS[0], 4, Z_CPT[0], NOIR),
            A(XB, TIROIRS[0], XF, TIROIRS[1], 4, Z_CPT[0], NOIR, r=0.3, b=0.3),
            B(XB, TIROIRS[1], XF - 0.5, y1, 4, Z_CPT[0], NOIR)]
    ya, yb = TIROIRS
    out += [B(XF - 0.1, ya + 0.3, XF + 0.15, yb - 0.3, z - 0.12, z + 0.12, "carbone") for z in (15.5, 26.0)]   # joints
    for zp in (13.2, 23.7, 32.1):                                                                            # tirettes noires
        out += [T([(XF + 0.95, ya + 7.8, zp), (XF + 0.95, yb - 7.8, zp)], 0.28, "metal", bouts=True),
                B(XF, ya + 7.6, XF + 0.95, ya + 8.2, zp - 0.25, zp + 0.25, "metal"),
                B(XF, yb - 8.2, XF + 0.95, yb - 7.6, zp - 0.25, zp + 0.25, "metal")]
    # petit frigo 24 po (lait) : caisse noire, porte vitrée teintée à cadre inox, grille, poignée verticale côté tiroirs
    fa, fb = FRIGO
    out += [A(XB + 0.05, fa + 0.1, XF - 1.15, fb - 0.1, 0.6, 34.2, "carbone", r=0.5, b=0.3),
            A(XF - 1.15, fa + 0.2, XF + 0.15, fb - 0.2, 3.9, 34.1, "inox", r=0.4, b=0.2),
            B(XF + 0.15, fa + 1.4, XF + 0.35, fb - 1.4, 5.1, 32.9, "ecran"),
            B(XF - 0.95, fa + 0.8, XF - 0.05, fb - 0.8, 0.8, 3.7, "metal"),
            T([(XF + 1.45, fb - 2.2, 9.0), (XF + 1.45, fb - 2.2, 30.0)], 0.35, "inox", bouts=True),
            B(XF + 0.15, fb - 2.5, XF + 1.45, fb - 1.9, 9.2, 10.0, "inox"), B(XF + 0.15, fb - 2.5, XF + 1.45, fb - 1.9, 29.0, 29.8, "inox")]
    # comptoir de bois de grange
    out += [A(XB, y0 + 0.15, XC, y1 - 0.15, Z_CPT[0], Z_CPT[1], "bois_grange", r=0.4, b=0.3)]
    zc = Z_CPT[1]
    # prises doubles (plaques noires) sur la brique, à 8 po au-dessus du comptoir
    for yp in (393.0, 409.0):
        out += [B(XB, yp - 1.4, XB + 0.35, yp + 1.4, zc + 6.0, zc + 10.5, "carbone"),
                B(XB + 0.35, yp - 0.55, XB + 0.45, yp + 0.55, zc + 6.8, zc + 7.8, "metal"),
                B(XB + 0.35, yp - 0.55, XB + 0.45, yp + 0.55, zc + 8.7, zc + 9.7, "metal")]
    # machine espresso inox (devant vers +x) : caisse, pieds, groupe, porte-filtre, bac d'égouttement, buse vapeur, manomètre
    ma, mb = MACHINE
    ym = (ma + mb) / 2
    xm0, xm1 = XB + 3.4, XB + 18.4
    out += [B(xm0 + 1, ma + 1, xm1 - 1, mb - 1, zc, zc + 0.8, "carbone"),
            A(xm0, ma, xm1, mb, zc + 0.8, zc + 16.0, "inox", r=0.8, b=0.4),
            B(xm0 + 1, ma + 0.6, xm1 - 1.5, mb - 0.6, zc + 16.0, zc + 16.3, "carbone"),            # chauffe-tasses
            C(xm1 + 0.9, ym, 1.7, zc + 8.4, zc + 11.4, "inox", pans=24),                            # groupe
            C(xm1 + 1.2, ym, 1.55, zc + 6.9, zc + 8.4, "inox", pans=24),                            # porte-filtre
            T([(xm1 + 2.4, ym, zc + 7.6), (xm1 + 7.0, ym, zc + 7.0)], 0.5, "carbone", bouts=True),
            B(xm1, ma + 1.0, xm1 + 3.6, mb - 1.0, zc + 0.8, zc + 2.0, "inox"),                     # bac d'égouttement
            B(xm1 + 0.2, ma + 1.4, xm1 + 3.4, mb - 1.4, zc + 2.0, zc + 2.1, "carbone"),
            T([(xm1 + 0.3, mb - 1.2, zc + 11.5), (xm1 + 2.2, mb - 0.8, zc + 10.5), (xm1 + 2.6, mb - 0.8, zc + 4.5)], 0.22, "inox"),
            CX(xm1 - 0.1, xm1 + 0.3, ym, zc + 13.3, 1.5, "inox"), CX(xm1, xm1 + 0.4, ym, zc + 13.3, 1.2, "blanc"),
            B(xm1, ma + 1.5, xm1 + 0.3, ma + 2.6, zc + 13.0, zc + 14.0, "carbone")]                # interrupteur
    out += [C(xm0 + 4.0, ym - 2.2, 1.2, zc + 16.3, zc + 18.3, "blanc", pans=20),                     # tasses à espresso
            C(xm0 + 4.0, ym + 2.2, 1.2, zc + 16.3, zc + 18.3, "blanc", pans=20)]
    # moulin à grains noir : socle, bec, trémie de verre avec grains, couvercle
    ga, gb = MOULIN
    yg = (ga + gb) / 2
    out += [A(XB + 6.5, ga, XB + 14.5, gb, zc, zc + 10.5, "carbone", r=1.2, b=0.5),
            B(XB + 14.5, yg - 1.0, XB + 15.6, yg + 1.0, zc + 5.0, zc + 7.0, "carbone"),
            C(XB + 10.5, yg, 1.7, zc + 10.5, zc + 16.5, "verre-clair", r2=2.9, pans=24),
            C(XB + 10.5, yg, 1.5, zc + 10.7, zc + 14.0, "bois_brut", r2=2.3, pans=24),
            C(XB + 10.5, yg, 3.0, zc + 16.5, zc + 17.1, "carbone", pans=24)]
    # pichet à lait inox, bocal de grains
    out += [C(XB + 19.5, 396.5, 1.5, zc, zc + 4.2, "inox", r2=1.75, pans=20),
            C(XB + 4.5, 386.5, 2.0, zc, zc + 6.0, "verre-clair", pans=24), C(XB + 4.5, 386.5, 1.85, zc + 0.15, zc + 4.2, "bois_brut", pans=24),
            C(XB + 4.5, 386.5, 2.1, zc + 6.0, zc + 6.7, "bois_grange", pans=24)]
    # tablettes flottantes de bois de grange, ruban DEL dessous
    for z in Z_TAB:
        out += [A(XB, y0 + 0.6, XB + P_TAB, y1 - 0.6, z, z + 1.75, "bois_grange", r=0.3, b=0.25),
                B(XB + P_TAB - 2.0, y0 + 1.5, XB + P_TAB - 1.2, y1 - 1.5, z - 0.15, z, "spot")]
    z1, z2 = Z_TAB[0] + 1.75, Z_TAB[1] + 1.75
    for k, yt in enumerate((385.0, 390.5, 396.0, 401.5)):                       # tasses (blanches et noires)
        out += [C(XB + 4.5, yt, 1.65, z1, z1 + 3.8, "blanc" if k % 2 == 0 else "carbone", pans=24),
                T([(XB + 4.5, yt + 1.6, z1 + 3.0), (XB + 4.5, yt + 2.7, z1 + 2.0), (XB + 4.5, yt + 1.6, z1 + 1.0)], 0.22,
                  "blanc" if k % 2 == 0 else "carbone")]
    for yt in (409.0, 412.0):                                                   # tasses à espresso empilées
        out += [C(XB + 4.0, yt, 1.25, z1 + 2.2 * i, z1 + 2.2 * i + 2.1, "blanc", pans=20) for i in range(2)]
    out += [C(XB + 4.5, 419.0, 2.3, z1, z1 + 5.5, "verre-clair", pans=24)]      # verre à latte
    for yt in (385.5, 391.5):                                                   # bocaux de grains (tablette du haut)
        out += [C(XB + 4.5, yt, 2.0, z2, z2 + 6.5, "verre-clair", pans=24), C(XB + 4.5, yt, 1.85, z2 + 0.15, z2 + 4.6, "bois_brut", pans=24),
                C(XB + 4.5, yt, 2.1, z2 + 6.5, z2 + 7.2, "bois_grange", pans=24)]
    out += [MOD("plante_syngonium", XB + 5.0, 422.0, z=z2, H=11)]
    return out


def _colonne_apothicaire(h):
    B, A, C, T, CY = h.B, h.A, h.C, h.T, h.CY
    NOIR = getattr(h, "NOIR", "noir-mat")
    x0, y0, x1, y1 = COL
    xm = (x0 + x1) / 2
    cols = [(x0 + 0.2, xm - 0.12), (xm + 0.12, x1 - 0.2)]
    out = [B(x0 + 0.1, y0 + 0.1, x1 - 0.1, y1 - 2.5, 0, Z_PANIERS[0], "carbone"),                  # socle en retrait
           B(x0 + 0.1, y0 + 0.05, x1 - 0.1, YF, Z_PANIERS[0], Z_APOTH[1], NOIR),                     # caisson bas
           B(x0 + 0.1, y0 + 0.05, x1 - 0.1, YF, Z_HAUT[0], Z_HAUT[1], NOIR)]                         # caisson haut
    # paniers à linge basculants (pâle / foncé) : façades noir mat, tirette noire
    for a, b in cols:
        out += [A(a, YF, b, y1, Z_PANIERS[0] + 0.3, Z_PANIERS[1] - 0.25, NOIR, r=0.15, b=0.1),
                T([(a + 3.4, y1 + 0.7, 27.0), (b - 3.4, y1 + 0.7, 27.0)], 0.28, "metal", bouts=True),
                B(a + 3.2, y1, a + 3.8, y1 + 0.7, 26.75, 27.25, "metal"), B(b - 3.8, y1, b - 3.2, y1 + 0.7, 26.75, 27.25, "metal")]
    # tiroirs d'apothicaire : 3 rangées × 2, façades de bois de grange, poignée-coquille et porte-étiquette noirs
    za, zb = Z_APOTH
    pas = (zb - za) / 3
    for i in range(3):
        r0, r1 = za + i * pas, za + (i + 1) * pas
        zcen = (r0 + r1) / 2
        for a, b in cols:
            xc = (a + b) / 2
            out += [A(a, YF, b, y1, r0 + 0.12, r1 - 0.12, "bois_grange", r=0.15, b=0.1),
                    B(xc - 2.0, y1, xc + 2.0, y1 + 0.75, zcen - 1.3, zcen - 0.4, "metal"),
                    B(xc - 2.0, y1, xc - 1.7, y1 + 0.75, zcen - 1.3, zcen + 0.1, "metal"),
                    B(xc + 1.7, y1, xc + 2.0, y1 + 0.75, zcen - 1.3, zcen + 0.1, "metal"),
                    B(xc - 1.4, y1, xc + 1.4, y1 + 0.15, zcen + 0.7, zcen + 2.4, "metal"),
                    B(xc - 1.15, y1 + 0.15, xc + 1.15, y1 + 0.2, zcen + 0.9, zcen + 2.2, "blanc")]
    # niche ouverte : fond de bois de grange, côtés et tablettes noirs, DEL en haut ; serviettes roulées cordées
    n0, n1 = Z_NICHE
    xi0, xi1 = x0 + 0.85, x1 - 0.85
    out += [B(x0 + 0.1, y0 + 0.05, x1 - 0.1, y0 + 0.75, n0, n1, "bois_grange"),
            B(x0 + 0.1, y0 + 0.75, xi0, y1, n0, n1, NOIR), B(xi1, y0 + 0.75, x1 - 0.1, y1, n0, n1, NOIR),
            B(xi0, y0 + 0.75, xi1, y1, n0, n0 + 0.75, NOIR), B(xi0, y0 + 0.75, xi1, y1, n1 - 0.75, n1, NOIR),
            B(xi0 + 1.0, y1 - 1.6, xi1 - 1.0, y1 - 0.9, n1 - 1.05, n1 - 0.75, "spot")]
    r = 3.1
    larg = xi1 - xi0
    xs0 = xi0 + (larg - 8 * r) / 2 + r
    rangs = [[xs0 + 2 * r * k for k in range(4)], [xs0 + r + 2 * r * k for k in range(3)], [xs0 + 2 * r + 2 * r * k for k in range(2)]]
    couleurs = [["draps"] * 4, ["jete", "draps", "jete"], ["draps", "draps"]]
    for j, (rang, coul) in enumerate(zip(rangs, couleurs)):
        zr = n0 + 0.75 + r + j * 2 * r * 0.866
        for xr, mat in zip(rang, coul):
            out += [CY(xr, y0 + 3.0, y1 - 2.2, zr, r, mat, pans=20), CY(xr, y1 - 2.2, y1 - 2.12, zr, r * 0.45, "gris", pans=16)]
    # armoire du haut (réserves) : 2 portes noir mat à ouverture par poussée
    for a, b in cols:
        out += [A(a, YF, b, y1, Z_HAUT[0] + 0.3, Z_HAUT[1] - 0.3, NOIR, r=0.15, b=0.1)]
    return out


def appliquer_scene_rdc(S, h):
    # laveuse et sécheuse (et tout objet de la niche) retirées ; le muret tuilé de la douche (x < 76,2) reste
    S["mobilier"] = [o for o in S["mobilier"] if not _dedans(o, NICHE_3D, marge=0.6)]
    # volée de l'entrée arrière refermée : plus de trou de plancher demandé à cet endroit
    if S.get("tremies_plancher"):
        S["tremies_plancher"] = [t for t in S["tremies_plancher"] if list(t) != TREMIE_EAR]
    # mur de gauche de l'entrée arrière en brique rouge (la brique de la cuisine), du plancher au plafond
    S.setdefault("revetements", []).append(h.B(XG, EAR[1], XB, EAR[3], 0, S.get("plafond", 96), "brique_rouge"))
    S["mobilier"] += _coin_cafe(h) + _colonne_apothicaire(h)
    # lumières : DEL sous les tablettes du coin café, DEL de la niche à serviettes
    S.setdefault("lumieres", []).extend([{"x": XB + 8, "y": 405, "z": Z_TAB[0] - 1, "i": 2},
                                         {"x": (COL[0] + COL[2]) / 2, "y": 160, "z": Z_NICHE[1] - 3, "i": 1.5}])
    # visite : « Coin café » après « Entrée arrière », « Salle de bain — rangement » après « Vanité »
    vis = [v for v in S.get("visites", []) if v.get("nom") not in ("Coin café", "Salle de bain — rangement")]
    cafe = {"nom": "Coin café", "x": 307, "y": 406, "cap": 186}
    sdb = {"nom": "Salle de bain — rangement", "x": 103, "y": 196, "cap": 252}
    noms = [v.get("nom") for v in vis]
    i = noms.index("Vanité") + 1 if "Vanité" in noms else len(vis)
    vis.insert(i, sdb)
    noms = [v.get("nom") for v in vis]
    i = noms.index("Entrée arrière") + 1 if "Entrée arrière" in noms else len(vis)
    vis.insert(i, cafe)
    S["visites"] = vis
    # palette
    pal = S.setdefault("palette", [])
    for p in pal:
        if p[0] == "Salle de bain" and "apothicaire" not in p[1]:
            p[1] += " ; colonne d'apothicaire (tiroirs de bois de grange, caisson noir mat) à la place de la laveuse-sécheuse"
    if not any(p[0] == "Coin café" for p in pal):
        pal.append(["Coin café", "entrée arrière : mur de brique rouge, caissons noir mat, comptoir et tablettes de bois de grange, "
                                 "DEL sous les tablettes, petit frigo à porte vitrée noire, machine espresso inox ; ardoise au sol",
                    "#8A4B2A"])
