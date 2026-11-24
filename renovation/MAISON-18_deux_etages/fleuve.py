"""MAISON-18 — le fleuve Saint-Laurent au loin, la basse-ville qui descend jusqu'à la rive et le traversier F.-A.-Gauthier
qui passe pour vrai (demande du client : « je veux aussi que tu ajoutes le F.-A.-Gauthier sur le fleuve au loin » ; « fais le
traversier qui avance pour vrai »).

Module de la liste FINALE de scene_3d.py : appliquer_scene_finale(SCENE) reçoit la maquette à deux étages AVEC
SCENE["exterieur"] (exterieur.py) et y ajoute, en pouces, z ABSOLU (plancher du sous-sol = 0, RDC = 105) :
- SCENE["exterieur"]["lointain"] : le relief du lot n'est plus prolongé vers la rue (côté -y « ouvert ») ; au-delà, la terre
  du lointain (la rue, les maisons d'en face, la basse-ville, la rive de roche) et le fleuve jusqu'à l'horizon ;
- SCENE["exterieur"]["animes"] : le traversier (objet animé « lointain ») qui fait la navette au large ;
- un arrêt de visite « Le fleuve et le traversier » sur le perron avant, regard vers le fleuve ;
- deux lignes dans la palette de l'extérieur.
Contrat du moteur : generer_3d.exterieur_lointain() et exterieur_animes(), renovation/README.md (section « Le lointain »).
Sources, échelle, vitesse et simplifications : DESIGN_fleuve.md.
"""
import math
import random

M = 39.37                      # pouces par mètre

# ------------------------------------------------------------------------------------------------- site (à valider sur place)
Z_EAU = -45.0 * M              # surface du fleuve : 45 m sous le plancher du sous-sol (la maison est sur le haut de la pente)
Y_RIVE = -450.0 * M            # la rive : 450 m devant la façade (« quelques centaines de mètres »)
Y_BORD_LOT = -620.0            # bord avant du relief du lot (exterieur.py) : la terre du lointain part de là
Z_RUE = -14.0                  # trottoirs ; chaussée de -16 (bords) à -13 (couronne) ; l'entrée de l'allée arrive à -15
RUE = (-730.0, -1080.0)        # chaussée (9 m) entre deux trottoirs de 30 et 50 po
Y_FACE = -1650.0               # façades des maisons d'en face (elles regardent la rue, vers +y), en bas d'un talus
Z_HAUT_BERGE = -1665.0         # haut du talus de roche (42,3 m sous le sous-sol)
Y_HAUT_BERGE = -16900.0        # haut du talus de roche de la rive
X_LOIN = 314960.0              # la terre du lointain va à 8 km de chaque côté

# ------------------------------------------------------------------------------------------------- traversier F.-A.-Gauthier
# Fincantieri 2014 (STQ) : 133,2 m hors tout, 22,4 m de large, tirant d'eau 5,55 m, 8 ponts (1-2 machines, 3-5 véhicules,
# 6 passagers, 7 promenade, 8 passerelle), 20 nœuds au plus, embarquement avant et arrière. Silhouette et couleurs : photos
# (coque bleue jusqu'au pont des véhicules, superstructure blanche, passerelle à l'avant sur toute la largeur, cheminée à
# l'arrière, embarcations orange, « F.-A.-GAUTHIER » en lettres blanches sur la coque, vers l'arrière). Voir DESIGN_fleuve.md.
NOEUD = 0.514444               # m/s
VITESSE_REELLE = 15 * NOEUD    # vitesse de croisière demandée : 15 nœuds (7,7 m/s)
ACCELERE = 3                   # ×3 pour qu'on le voie avancer en quelques secondes (≈ 45 nœuds à l'écran)
Y_ALLER, Y_RETOUR, X_BOUT = -2000.0 * M, -2700.0 * M, 3000.0 * M      # passe à 2 km, revient à 2,7 km, demi-tour à 3 km de côté
DEPART = 78                    # s : au chargement, il est déjà en vue (à 1,2 km à droite du regard vers le fleuve)

BLEU_COQUE, BLANC, VITRAGE, MARINE = "#1f4896", "#eef1f2", "#25313b", "#1c2a52"
ORANGE, GRIS_RAMPE, GRIS_TUYAU = "#e5672a", "#3d4248", "#3a3c40"


def _m(v):
    return round(v * M, 1)


def _poly_m(pts):
    return [[_m(x), _m(y)] for x, y in pts]


def _B(x0, x1, y0, y1, z0, z1, c, **k):            # boîte, mètres → pouces (repère local du navire)
    return dict({"forme": "boite", "x0": _m(x0), "x1": _m(x1), "y0": _m(y0), "y1": _m(y1), "z0": _m(z0), "z1": _m(z1), "couleur": c}, **k)


def _Pm(pts, z0, z1, c):                             # prisme vertical, mètres → pouces
    return {"forme": "boite", "pts": _poly_m(pts), "z0": _m(z0), "z1": _m(z1), "couleur": c}


def _sym(demi):
    """Contour fermé symétrique à partir des demi-largeurs [(x, y >= 0)] de l'arrière vers l'avant (pointe : y = 0)."""
    bas = [(x, -y) for x, y in demi]
    haut = [(x, y) for x, y in reversed(demi[:-1] if demi[-1][1] == 0 else demi)]
    return bas + haut


def _coupe(demi, x0=None, x1=None):
    """Demi-contour gardé entre x0 et x1 (points interpolés aux coupes)."""
    out = []
    for (xa, ya), (xb, yb) in zip(demi, demi[1:]):
        out.append((xa, ya))
        for xc in sorted(c for c in (x0, x1) if c is not None and xa < c < xb):
            out.append((xc, round(ya + (yb - ya) * (xc - xa) / (xb - xa), 3)))
    out.append(demi[-1])
    lo = -1e9 if x0 is None else x0
    hi = 1e9 if x1 is None else x1
    return [p for p in out if lo - 1e-9 <= p[0] <= hi + 1e-9]


# demi-largeurs de la coque (m) de l'arrière (tableau, x = -66,6) à l'étrave (x = +66,6) : étrave ronde brise-glace
COQUE = [(-66.6, 10.0), (-65.8, 10.9), (-62.0, 11.2), (30.0, 11.2), (40.0, 10.8), (48.0, 9.6), (54.0, 7.9), (59.0, 5.8),
         (62.8, 3.6), (65.4, 1.6), (66.6, 0.0)]
PONT6 = [(-50.0, 10.7), (40.0, 10.7), (44.0, 9.5), (46.5, 7.0), (47.5, 3.0), (47.8, 0.0)]
PONT7 = [(-42.0, 10.5), (41.0, 10.5), (44.0, 8.5), (45.5, 5.0), (46.0, 0.0)]


def traversier():
    """Le F.-A.-Gauthier en formes simples, à l'échelle réelle. Repère local : origine au milieu, À LA FLOTTAISON (rien sous
    l'eau : le fleuve ne cache rien), +x = l'étrave (sens de marche), +y = bâbord."""
    o = []
    # coque : bleue de la flottaison à 7 m (9,6 m à l'avant, où le bleu remonte), blanche jusqu'au pont 6 (13,6 m)
    o.append(_Pm(_sym(COQUE), 0.0, 7.0, BLEU_COQUE))
    o.append(_Pm(_sym(_coupe(COQUE, x0=36.0)), 7.0, 9.6, BLEU_COQUE))
    o.append(_Pm(_sym(_coupe(COQUE, x1=36.0)), 7.0, 13.6, BLANC))
    o.append(_Pm(_sym(_coupe(COQUE, x0=36.0)), 9.6, 13.6, BLANC))
    # hublots des ponts des véhicules (bande sombre), rampe arrière relevée sur le tableau
    for s in (1, -1):
        o.append(_B(-58.0, 30.0, s * 11.2, s * 11.5, 10.3, 11.1, VITRAGE))
    o.append(_B(-66.95, -66.6, -5.5, 5.5, 2.0, 8.4, GRIS_RAMPE))
    # superstructure : pont 6 (passagers) et pont 7 (promenade), bandes de fenêtres ; passerelle (pont 8) à l'avant, sur
    # toute la largeur avec ses ailes ; toit, mât, radar qui tourne
    o.append(_Pm(_sym(PONT6), 13.6, 16.4, BLANC))
    o.append(_Pm(_sym(PONT7), 16.4, 19.2, BLANC))
    for s in (1, -1):
        o.append(_B(-46.0, 42.0, s * 10.7, s * 11.0, 14.3, 15.6, VITRAGE))
        o.append(_B(-38.0, 40.0, s * 10.5, s * 10.8, 17.0, 18.5, VITRAGE))
    o.append(_B(31.0, 41.5, -11.2, 11.2, 19.2, 22.0, BLANC))
    o.append(_B(41.5, 41.8, -10.8, 10.8, 20.1, 21.4, VITRAGE))
    for s in (1, -1):
        o.append(_B(32.0, 41.0, s * 11.2, s * 11.5, 20.1, 21.4, VITRAGE))
    o.append(_B(30.6, 41.9, -11.4, 11.4, 22.0, 22.35, BLANC))
    o.append({"forme": "cylindre", "x": _m(36.0), "y": 0.0, "r": _m(0.3), "z0": _m(22.35), "z1": _m(30.5), "couleur": BLANC, "pans": 8})
    o.append(_B(35.8, 36.2, -2.2, 2.2, 27.6, 27.9, BLANC))
    o.append(_B(35.0, 37.0, -0.12, 0.12, 28.5, 28.8, GRIS_TUYAU, tourne=150, centre=[_m(36.0), 0.0]))
    # cheminée à l'arrière : caisson blanc, chapeau bleu marine, quatre tuyaux d'échappement (quatre moteurs bicarburant)
    o.append(_B(-50.0, -42.0, -2.4, 2.4, 16.4, 25.8, BLANC))
    o.append(_B(-50.2, -41.8, -2.6, 2.6, 25.8, 26.8, MARINE))
    for x in (-47.5, -44.5):
        for y in (-0.9, 0.9):
            o.append({"forme": "cylindre", "x": _m(x), "y": _m(y), "r": _m(0.5), "z0": _m(26.8), "z1": _m(27.8), "couleur": GRIS_TUYAU, "pans": 8})
    # embarcations de sauvetage (orange) au pont 7, deux de chaque bord
    for s in (1, -1):
        for x0, x1 in ((6.0, 13.0), (-20.0, -13.0)):
            o.append(_B(x0, x1, min(s * 10.6, s * 12.0), max(s * 10.6, s * 12.0), 17.2, 18.8, ORANGE))
    # nom sur la coque, vers l'arrière, des deux bords (lettres blanches de 1,4 m)
    o.append({"forme": "texte", "texte": "F.-A.-GAUTHIER", "x": _m(-44.0), "y": _m(11.55), "z0": _m(3.4), "z1": _m(4.8), "larg": _m(15.0),
              "face": "+y", "couleur": "#ffffff"})
    o.append({"forme": "texte", "texte": "F.-A.-GAUTHIER", "x": _m(-44.0), "y": _m(-11.55), "z0": _m(3.4), "z1": _m(4.8), "larg": _m(15.0),
              "face": "-y", "couleur": "#ffffff"})
    # vague d'étrave et sillage (à fleur d'eau, 10 cm) : on voit qu'il avance même sur une image fixe
    for s in (1, -1):
        o.append(_Pm([(40.0, s * 11.0), (55.0, s * 9.4), (66.7, s * 0.4), (67.9, s * 1.8), (56.0, s * 11.6), (40.0, s * 12.7)], 0.0, 0.1, "#e6edf0"))
    for (xa, xb, ra, rb, c) in ((-66.6, -170.0, 9.0, 14.0, "#cfdce3"), (-170.0, -300.0, 14.0, 22.0, "#8fa8b7"), (-300.0, -460.0, 22.0, 30.0, "#5d7b91")):
        o.append(_Pm([(xa, -ra), (xa, ra), (xb, rb), (xb, -rb)], 0.0, 0.1, c))
    return o


def anime_traversier():
    v = VITESSE_REELLE * ACCELERE * M                # po/s
    return {"id": "traversier", "nom": "Le traversier F.-A.-Gauthier", "lointain": True, "cadence": 10, "ombre": False, "toucher": False,
            "objets": traversier(), "z": round(Z_EAU, 1),
            "trajet": [[-X_BOUT, Y_ALLER], [X_BOUT, Y_ALLER], [X_BOUT, Y_RETOUR], [-X_BOUT, Y_RETOUR]],
            "vitesse": round(v, 1), "rotation": 2.0, "depart": DEPART,
            "note": f"15 nœuds réels × {ACCELERE} ; aller à 2 km, retour à 2,7 km, demi-tours à 3 km de côté (hors du champ)"}


# ------------------------------------------------------------------------------------------------- terre du lointain
def _lisse(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def _lin(pts, v):
    if v <= pts[0][0]:
        return pts[0][1]
    for (a, za), (b, zb) in zip(pts, pts[1:]):
        if v <= b:
            return za + (zb - za) * (v - a) / (b - a)
    return pts[-1][1]


# profil de la descente (y croissant), z absolu : rue, terrains d'en face qui descendent, basse-ville (pente concave : on
# voit tout jusqu'à la rive), talus de roche, rive au niveau de l'eau
PROFIL = [(-2400.0, -290.0), (-2000.0, -255.0), (-1650.0, -205.0), (-1300.0, -95.0), (-1132.0, Z_RUE), (-1080.0, Z_RUE)]


def z_profil(y, x=0.0):
    if y >= -1080.0:
        if y >= -730.0:
            return Z_RUE
        u = (y - RUE[1]) / (RUE[0] - RUE[1])           # 0 au bord sud de la chaussée, 1 au bord nord
        return -16.0 + 3.0 * math.sin(math.pi * u)      # couronne
    if y >= -2400.0:
        return _lin(sorted(PROFIL), y)
    if y >= Y_HAUT_BERGE:
        u = (-2400.0 - y) / (-2400.0 - Y_HAUT_BERGE)
        ond = 60.0 * math.sin(x / 12000.0) * math.sin(math.pi * u) + 35.0 * math.sin(x / 4100.0 + 1.3) * math.sin(math.pi * u)
        return -290.0 + (Z_HAUT_BERGE + 290.0) * (1 - (1 - u) ** 1.3) + ond
    u = (Y_HAUT_BERGE - y) / (Y_HAUT_BERGE - Y_RIVE)
    return Z_HAUT_BERGE + (Z_EAU - Z_HAUT_BERGE) * _lisse(u) if y > Y_RIVE else Z_EAU


def _xs(lot_xs):
    pas = [120, 240, 400, 600, 900, 1300, 1800, 2500, 3500, 5000, 7000, 10000, 14000, 20000, 28000, 40000, 60000, 90000,
           130000, 180000, 240000, X_LOIN]
    g = [lot_xs[0] - p for p in pas if lot_xs[0] - p >= -X_LOIN]
    d = [lot_xs[-1] + p for p in pas if lot_xs[-1] + p <= X_LOIN]
    return sorted(set([round(v, 2) for v in g + list(lot_xs) + d]))


def _ys():
    ys = [Y_RIVE, -17600.0, -17450.0, -17250.0, -17080.0, Y_HAUT_BERGE]
    y = Y_HAUT_BERGE
    while y < -2400.0 - 1e-6:
        y = min(-2400.0, y + 560.0)
        ys.append(y)
    ys += [-2100.0, -1900.0, -1700.0, -1525.0, -1350.0, -1250.0, -1132.0, -1130.0, -1082.0, -1080.0, -995.0, -905.0, -815.0,
           -730.0, -728.0, -700.0, -660.0, Y_BORD_LOT]
    return sorted(set(round(v, 2) for v in ys))


GAZON, GAZON_FONCE, BOISE, BOISE_FONCE, TOITS = "#6c8a4a", "#5f7c43", "#405a35", "#36502f", "#77736d"
TROTTOIR, ASPHALTE, ROCHE, ROCHE_PALE, GREVE = "#a5a5a0", "#4a4b4e", "#7c766b", "#8f887a", "#a39a84"


def _couleur_sommet(x, y, rnd):
    if y > -700.0:
        return GAZON
    if y >= -728.0 or -1130.0 <= y <= -1082.0:
        return TROTTOIR
    if -1080.0 <= y <= -730.0:
        return ASPHALTE
    if y > -2400.0:
        return GAZON if rnd.random() < 0.7 else GAZON_FONCE
    if y <= Y_RIVE + 1:
        return GREVE
    if y <= Y_HAUT_BERGE + 1:
        return ROCHE if rnd.random() < 0.6 else ROCHE_PALE
    centre = abs(x - 228.0) < 40000.0                   # la basse-ville : maisons et rues ; plus loin, la forêt
    r = rnd.random()
    if centre:
        return BOISE if r < 0.40 else GAZON if r < 0.70 else TOITS if r < 0.88 else BOISE_FONCE
    return BOISE_FONCE if r < 0.55 else BOISE if r < 0.85 else GAZON_FONCE


def terre(relief_lot):
    """Grille de la terre du lointain (z absolu, couleurs par sommet), du bord avant du relief du lot jusqu'à la rive. Le
    premier rang reprend exactement le bord du lot (mêmes x, mêmes z ; au-delà, le z du coin, comme le prolongement du
    moteur) : pas de marche entre le lot et le lointain."""
    lx, ly, lz = relief_lot["xs"], relief_lot["ys"], relief_lot["z"]
    j0 = min(range(len(ly)), key=lambda j: ly[j])
    bord = list(zip(lx, lz[j0]))
    xs, ys = _xs(lx), _ys()
    rnd = random.Random(86)
    Z, C = [], []
    for y in ys:
        rz, rc = [], []
        for x in xs:
            ze = _lin(bord, x)
            if y >= Y_BORD_LOT - 1e-6:
                z = ze
            elif y >= -700.0:                            # talus jusqu'au trottoir
                t = _lisse((Y_BORD_LOT - y) / (Y_BORD_LOT + 700.0))
                z = ze + (Z_RUE - ze) * t
            else:
                z = z_profil(y, x)
            rz.append(round(z, 1))
            rc.append(_couleur_sommet(x, y, rnd))
        Z.append(rz)
        C.append(rc)
    return {"xs": xs, "ys": ys, "z": Z, "couleurs": C}


# ------------------------------------------------------------------------------------------------- maisons et arbres
REVET = ["#e9e6dc", "#d9d4c4", "#c7cdd0", "#b9c4cc", "#e6dcc0", "#cfc4b0", "#a9b2a5", "#f1efe8", "#8f9aa3", "#c9b9a0"]
TOITURE = ["#3f4245", "#2f3133", "#4d4a46", "#5a4a40", "#3c4650", "#55585b"]


def _maison(x, yf, larg, prof, rnd, face=1, etages=1):
    """Bungalow (ou cottage) : façade sur la ligne yf, profondeur vers -y (face=1 : elle regarde +y, la rue au nord) ou vers
    +y (face=-1). Plancher au niveau du terrain devant la façade ; sur la pente, la fondation descend jusqu'au plus bas."""
    y0, y1 = (yf - prof, yf) if face == 1 else (yf, yf + prof)
    zs = z_profil(yf, x)
    zb = min(z_profil(y0, x), z_profil(y1, x), z_profil(yf, x - larg / 2), z_profil(yf, x + larg / 2), zs) - 12.0
    zt = zs + 18.0 + 112.0 * etages
    X0, X1 = round(x - larg / 2, 1), round(x + larg / 2, 1)
    out = [{"forme": "boite", "x0": X0, "x1": X1, "y0": round(y0, 1), "y1": round(y1, 1), "z0": round(zb, 1), "z1": round(zs + 18.0, 1),
            "couleur": "#b8b6ae"},
           {"forme": "boite", "x0": X0, "x1": X1, "y0": round(y0, 1), "y1": round(y1, 1), "z0": round(zs + 18.0, 1), "z1": round(zt, 1),
            "couleur": rnd.choice(REVET)},
           {"forme": "toit", "x0": round(X0 - 12, 1), "x1": round(X1 + 12, 1), "y0": round(y0 - 12, 1), "y1": round(y1 + 12, 1),
            "z0": round(zt, 1), "z1": round(zt + (prof / 2 + 12) * 5 / 12, 1), "faitage": "x", "couleur": rnd.choice(TOITURE)}]
    return out, zs


def _fenetres(x, yf, larg, zs, face=1):
    """Deux ou trois fenêtres sombres sur la façade (à 6 po du mur : lisibles de loin sans scintiller)."""
    out = []
    n = 3 if larg > 440 else 2
    for k in range(n):
        cx = x - larg / 2 + larg * (k + 0.5) / n
        yy = yf + 6 if face == 1 else yf - 6
        out.append({"forme": "boite", "x0": round(cx - 34, 1), "x1": round(cx + 34, 1), "y0": round(min(yf, yy), 1), "y1": round(max(yf, yy), 1),
                    "z0": round(zs + 54, 1), "z1": round(zs + 102, 1), "couleur": "#2b333a"})
    return out


def _arbre(x, y, rnd, gros=1.0):
    z = z_profil(y, x)
    if rnd.random() < 0.6:                          # épinette : cône sombre
        h = (300 + rnd.random() * 380) * gros
        return [{"forme": "cylindre", "x": round(x, 1), "y": round(y, 1), "r": round(h * 0.2, 1), "r2": 0, "z0": round(z, 1),
                 "z1": round(z + h, 1), "pans": 7, "couleur": rnd.choice(["#2f4a33", "#36503a", "#3b5a3c"])}]
    r = (110 + rnd.random() * 130) * gros            # feuillu (bouleau, érable) : boule
    return [{"forme": "sphere", "x": round(x, 1), "y": round(y, 1), "z": round(z + r * 1.25, 1), "r": round(r, 1), "ecrase": 0.85,
             "couleur": rnd.choice(["#4f6b3e", "#5b7744", "#6a8748", "#47613a"])}]


def objets_lointains():
    rnd = random.Random(1957)
    out = []
    # maisons d'en face : lots de 60 pi le long de la rue, façades vers nous ; plus basses que la rue (le terrain descend)
    for k in range(-9, 10):
        x = 228.0 + k * 720.0 + rnd.uniform(-60, 60)
        larg, prof = rnd.uniform(400, 520), rnd.uniform(300, 360)
        m, zs = _maison(x, Y_FACE, larg, prof, rnd)
        out += m + _fenetres(x, Y_FACE, larg, zs)
        if rnd.random() < 0.7:
            out += _arbre(x + rnd.choice([-1, 1]) * (larg / 2 + 80), Y_FACE + 60 + rnd.uniform(0, 80), rnd, 0.8)
    # basse-ville : rues parallèles au fleuve, maisons des deux côtés, arbres ; plus clairsemée en s'éloignant
    for yr in (-3400.0, -5400.0, -7400.0, -9400.0, -11400.0, -13400.0, -15200.0):
        for face, dy in ((1, -330.0), (-1, 330.0)):
            x = -36000.0 + rnd.uniform(0, 400)
            while x < 36000.0:
                larg = rnd.uniform(380, 540)
                if rnd.random() < 0.72 - abs(x) / 36000.0 * 0.35:
                    prof = rnd.uniform(300, 380)
                    m, zs = _maison(x, yr + dy, larg, prof, rnd, face, etages=2 if rnd.random() < 0.18 else 1)
                    out += m
                x += larg + rnd.uniform(220, 420)
        for _ in range(70):
            out += _arbre(rnd.uniform(-38000, 38000), yr + rnd.uniform(-900, 900), rnd)
    # boisés sur le haut du talus de la rive et des deux côtés de la basse-ville
    for _ in range(160):
        out += _arbre(rnd.uniform(-60000, 60000), rnd.uniform(Y_HAUT_BERGE + 60, Y_HAUT_BERGE + 1500), rnd, 1.1)
    for _ in range(140):
        s = rnd.choice([-1, 1])
        out += _arbre(228 + s * rnd.uniform(38000, 90000), rnd.uniform(-15500, -2600), rnd, 1.2)
    return out


def eau():
    L = 5900000.0                                    # 150 km : l'horizon (l'autre rive, à environ 50 km, est hors de vue)
    return {"nom": "Fleuve Saint-Laurent", "z": round(Z_EAU, 1), "pts": [[-L, Y_RIVE + 40], [L, Y_RIVE + 40], [L, -L], [-L, -L]],
            "couleur": "#143350", "couleur_loin": "#21476b", "reflet": 0.18}


# ------------------------------------------------------------------------------------------------- application
def _entiers(o):
    """Coordonnées au pouce près (au loin, c'est bien assez) : la page reste légère."""
    return {k: (round(v) if isinstance(v, float) else [[round(a) for a in p] for p in v] if k == "pts" else v) for k, v in o.items()}


ARRET = (100.0, -200.0)        # arrêt « Le fleuve et le traversier » (sur le filet du balcon avant)


def appliquer_scene_finale(S):
    X = S.get("exterieur")
    if not X or not X.get("relief"):
        return
    X["lointain"] = {"ouvert": ["-y"], "eau": eau(), "terre": terre(X["relief"]), "objets": [_entiers(o) for o in objets_lointains()],
                     "brume": 2400000, "couleur_brume": "#d9e3ea"}
    X.setdefault("animes", []).append(anime_traversier())
    # à gauche du perron (hors de la zone où le visiteur arrive), regard vers le fleuve ; sans « z » : les pieds sur le sol réel
    # (le moteur prend le plus haut plancher qui couvre le point : le filet du balcon avant, construit depuis par-dessus le terrain)
    X.setdefault("visites", []).append({"nom": "Le fleuve et le traversier", "x": ARRET[0], "y": ARRET[1], "cap": 270, "tangage": -4})
    X.setdefault("palette", []).extend([
        ["Fleuve Saint-Laurent", "au loin, 45 m plus bas que le sous-sol ; la rive à 450 m, l'autre rive hors de vue", "#143350"],
        ["Traversier F.-A.-Gauthier (STQ)", "133 m ; coque bleue, superstructure blanche ; passe à 2 et 2,7 km, à 3 × sa vitesse réelle", BLEU_COQUE]])
