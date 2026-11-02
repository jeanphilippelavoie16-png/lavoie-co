"""MAISON-18 — le visiteur qui cogne à la porte d'entrée et crie « JULIEEEEE ! » (gag de famille, demande du client du 2026-11-02).

Demande du client, mot pour mot : « je veux aussi que tu ajoutes un personnage qui cogne à la porte pi qui crie "JULIEEEEE" » ;
« un vieux monsieur » ; [photo] « faut qu'il ressemble à lui » ; « il faut qu'il ait une bedaine aussi, pi il cogne, il crie et
il rentre dans la maison. Il recrie Julie et lâche un gros pet ».

Personnage STYLISÉ en formes 3D (aucune image de la photo dans la page) qui en reprend les traits : cheveux courts foncés poivre
et sel un peu en bataille, lunettes rectangulaires à monture bleu-gris foncé, visage rond aux joues rouges, grand sourire, polo
bleu roi à rayures horizontales bleu pâle au col ouvert, bonne bedaine, pantalon gris foncé et souliers bruns. 5'-8" (68 po).

Le moteur joue le scénario (contrat : renovation/README.md, section « Scénario » ; generer_3d.scenarios()) : il monte du
trottoir au perron (chemin et sol lus dans la visite : perron, marches ou futur balcon), cogne trois coups, crie, la porte
s'ouvre, il entre dans l'entrée, recrie, lâche un gros pet (son synthétisé, bulle « PRRRT ! », petit nuage), attend, ressort
et la porte se referme. Il vient tout seul quand on s'approche de l'entrée (dedans ou dehors, 13 pi ; au plus une fois aux
2 minutes), avec le bouton « Quelqu'un cogne » ou à l'arrêt « Le visiteur à la porte » (section Extérieur).

Appelé par scene_3d.py (liste FINALE) : appliquer_scene_finale(SCENE), SCENE à deux étages avec SCENE["exterieur"].
Pouces, repère de la maison (x le long de la façade, y vers l'arrière, z depuis le plancher du sous-sol ; RDC = 105).
Repère du personnage : origine au sol entre ses pieds, +x devant lui, +y à sa gauche, z vers le haut.
"""
import math

PORTE = "ouv-RDC-010"            # porte d'entrée (centre x ≈ 199, façade y = 0 ; vantail à y 8,2-10, ouvre vers l'intérieur)
Z_RDC = 105.0

# ------------------------------------------------------------------------------------------------- couleurs (d'après la photo)
COULEURS = {
    "v-peau": {"couleur": "#E3A58C", "rugosite": .62},          # teint rosé, hâlé
    "v-nez": {"couleur": "#DE927C", "rugosite": .6},
    "v-joues": {"couleur": "#D86A5E", "rugosite": .65},         # joues rouges
    "v-bouche": {"couleur": "#5E1F1F", "rugosite": .5},
    "v-dents": {"couleur": "#F1EDE2", "rugosite": .3},
    "v-yeux": {"couleur": "#27323C", "rugosite": .2},
    "v-cheveux": {"couleur": "#211C1A", "rugosite": .92},                     # foncés
    "v-cheveux-gris": {"couleur": "#625E59", "rugosite": .92},                # poivre et sel (tempes, nuque)
    "v-sourcils": {"couleur": "#3A3431", "rugosite": .9},
    "v-lunettes": {"couleur": "#3B4A5E", "rugosite": .35, "metal": .2},      # monture rectangulaire bleu-gris foncé
    "v-polo": {"couleur": "#1F57D6", "rugosite": .78, "duvet": .45},         # polo bleu roi
    "v-rayure": {"couleur": "#5FAEF2", "rugosite": .78, "duvet": .45},       # rayures bleu pâle
    "v-bouton": {"couleur": "#D9DDE3", "rugosite": .3},
    "v-pantalon": {"couleur": "#46474D", "rugosite": .85, "duvet": .3},      # gris anthracite
    "v-ceinture": {"couleur": "#2C2420", "rugosite": .5},
    "v-souliers": {"couleur": "#3B2B22", "rugosite": .45},                   # cuir brun foncé
}


# ------------------------------------------------------------------------------------------------- formes (repère du personnage)
def CY(x, y, z0, z1, r, mat, r2=None, **k):
    o = {"forme": "cylindre", "x": x, "y": y, "z0": z0, "z1": z1, "r": r, "mat": mat}
    if r2 is not None:
        o["r2"] = r2
    o.update(k)
    return o


def SP(x, y, z, r, mat, e=None):
    o = {"forme": "sphere", "x": x, "y": y, "z": z, "r": r, "mat": mat}
    if e:
        o["echelle"] = list(e)
    return o


def TU(a, b, r, mat):
    return {"forme": "tube", "pts": [list(a), list(b)], "r": r, "mat": mat, "bouts": True}


def ANNEAU(x, y, z, R, r, mat, e=None):             # anneau horizontal (rayure, ourlet, col)
    o = {"forme": "tore", "x": x, "y": y, "z": z, "R": R, "r": r, "mat": mat, "axe": "z"}
    if e:
        o["echelle"] = list(e)
    return o


def BX(x0, x1, y0, y1, z0, z1, mat, r=None):
    o = {"forme": "boite", "x0": x0, "x1": x1, "y0": y0, "y1": y1, "z0": z0, "z1": z1, "mat": mat}
    if r:
        o["r"] = r
    return o


# ------------------------------------------------------------------------------------------------- le corps
TORSE = dict(x=0.3, z0=37.0, z1=55.0, r=8.0, r2=7.4, ex=0.70)        # polo : cylindre elliptique (16 po de large)
BEDAINE = dict(x=3.0, z=43.5, r=8.4, e=(1.0, 0.97, 0.95))             # la bedaine : 5½ po devant le thorax


def rayon_torse(z):
    return TORSE["r"] + (TORSE["r2"] - TORSE["r"]) * (z - TORSE["z0"]) / (TORSE["z1"] - TORSE["z0"])


def haut_du_corps():
    """Polo bleu roi à rayures bleu pâle (thorax + bedaine), col ouvert, patte à deux boutons, cou."""
    t, b = TORSE, BEDAINE
    out = [CY(t["x"], 0, t["z0"], t["z1"], t["r"], "v-polo", r2=t["r2"], echelle=[t["ex"], 1, 1]),
           SP(0.3, 0, 54.2, 8.6, "v-polo", (0.6, 1.08, 0.42)),                     # épaules
           SP(b["x"], 0, b["z"], b["r"], "v-polo", b["e"])]                          # bedaine
    rz = b["r"] * b["e"][2]
    for k in range(7):                                                               # rayures horizontales
        z = 38.6 + 2.35 * k
        out.append(ANNEAU(t["x"], 0, z, rayon_torse(z) + 0.04, 0.24, "v-rayure", (t["ex"], 1, 1)))
        if abs(z - b["z"]) < rz - 0.6:
            rho = b["r"] * math.sqrt(1 - ((z - b["z"]) / rz) ** 2)
            out.append(ANNEAU(b["x"], 0, z, rho + 0.04, 0.24, "v-rayure", (b["e"][0], b["e"][1], 1)))
    out += [CY(0.8, 0, 54.0, 59.5, 2.9, "v-peau"),                                    # cou
            SP(4.5, 0, 55.4, 1.4, "v-peau", (0.5, 1.0, 1.45)),                        # le V du col ouvert
            ANNEAU(0.8, 0, 56.7, 3.35, 0.75, "v-polo", (1.0, 1.05, 1)),               # col
            TU((2.4, 2.9, 57.3), (5.0, 1.3, 54.7), 0.85, "v-polo"),                   # pointes du col, ouvertes
            TU((2.4, -2.9, 57.3), (5.0, -1.3, 54.7), 0.85, "v-polo"),
            BX(5.15, 5.6, -0.55, 0.55, 51.6, 54.6, "v-polo"),                         # patte de boutonnage
            SP(5.62, 0, 52.4, 0.3, "v-bouton"), SP(5.62, 0, 53.9, 0.3, "v-bouton")]
    return out


def tete():
    """Tête ronde, double menton, joues rouges, grand sourire, lunettes rectangulaires, cheveux courts en bataille."""
    out = [SP(1.1, 0, 64.0, 4.9, "v-peau", (0.95, 0.9, 1.08)),                      # crâne et visage rond
           SP(2.0, 0, 60.6, 3.6, "v-peau", (0.95, 1.12, 0.78)),                      # mâchoire et menton ronds
           SP(5.85, 0, 63.6, 0.95, "v-nez", (0.95, 0.85, 1.15)),                      # nez
           SP(5.05, 0, 61.35, 1.0, "v-bouche", (0.55, 2.1, 0.8)),                     # grand sourire (bouche ouverte)
           SP(5.3, 0, 61.85, 0.75, "v-dents", (0.5, 2.3, 0.4))]                       # dents du haut
    for s in (1, -1):
        out += [SP(0.6, 4.35 * s, 63.8, 1.25, "v-peau", (0.55, 0.4, 1.0)),          # oreilles
                SP(4.6, 2.35 * s, 62.4, 1.45, "v-joues", (0.55, 1.0, 0.85)),         # joues rouges
                SP(5.3, 1.6 * s, 64.6, 0.42, "v-yeux"),                               # yeux
                TU((5.45, 0.7 * s, 65.95), (5.2, 2.9 * s, 66.15), 0.32, "v-sourcils")]
        # lunettes : verres rectangulaires 2,3 × 1,4 po, barre du haut plus épaisse, branches jusqu'aux oreilles
        y0, y1, z0, z1, x = 0.55 * s, 2.85 * s, 63.85, 65.35, 5.95
        out += [TU((x, y0, z1), (x, y1, z1), 0.24, "v-lunettes"), TU((x, y0, z0), (x, y1, z0), 0.16, "v-lunettes"),
                TU((x, y0, z0), (x, y0, z1), 0.16, "v-lunettes"), TU((x, y1, z0), (x, y1, z1), 0.17, "v-lunettes"),
                TU((5.85, 2.95 * s, 65.1), (1.0, 4.5 * s, 64.6), 0.14, "v-lunettes")]
    out.append(TU((5.95, 0.55, 64.85), (5.95, -0.55, 64.85), 0.16, "v-lunettes"))       # pont
    # cheveux : calotte foncée (front dégagé), tempes et nuque poivre et sel, quelques mèches en bataille
    out += [SP(-0.2, 0, 66.9, 5.15, "v-cheveux", (0.97, 0.93, 0.72)),
            SP(3.7, 0.6, 68.1, 1.9, "v-cheveux", (0.6, 1.5, 0.55)),                   # mèche sur le front
            SP(0.9, 4.25, 65.4, 1.5, "v-cheveux-gris", (1.25, 0.36, 0.9)),            # tempes grises
            SP(0.9, -4.25, 65.4, 1.5, "v-cheveux-gris", (1.25, 0.36, 0.9)),
            SP(-3.2, 0, 64.6, 3.0, "v-cheveux-gris", (0.5, 1.3, 0.9))]                # nuque
    # mèches courtes qui rebiquent (surtout sur le devant, comme sur la photo) : à peine 1 po hors de la calotte
    for a, b in (((2.2, 0.2, 69.6), (3.5, -0.5, 70.9)), ((1.0, 1.4, 70.0), (1.8, 2.1, 71.1)), ((1.2, -1.5, 70.0), (2.0, -2.2, 71.0)),
                 ((-0.4, 0.2, 70.3), (0.3, 0.8, 71.4)), ((-1.8, -1.0, 70.0), (-2.5, -1.6, 70.9)), ((3.0, 1.9, 69.0), (4.0, 2.5, 69.9)),
                 ((-2.0, 1.5, 69.9), (-2.8, 2.1, 70.7)), ((0.4, -0.6, 70.3), (1.0, -1.2, 71.3)), ((3.3, -1.6, 69.0), (4.2, -2.2, 69.7))):
        out.append(TU(a, b, 0.72, "v-cheveux"))
    return out


def bras(s):
    """Bras (s = 1 : gauche, -1 : droit) : manche courte rayée, bras nu ; l'avant-bras et la main sont une autre partie."""
    y = 9.6 * s
    return [SP(0.3, 9.2 * s, 54.4, 3.1, "v-polo"),
            CY(0.3, y, 46.5, 55.2, 2.75, "v-polo", r2=3.05),
            ANNEAU(0.3, y, 47.3, 2.82, 0.22, "v-rayure"), ANNEAU(0.3, y, 49.9, 2.92, 0.22, "v-rayure"),
            ANNEAU(0.3, y, 52.5, 3.02, 0.22, "v-rayure"),
            CY(0.3, y, 43.6, 47.0, 2.15, "v-peau")]


def avant_bras(s):
    y = 9.6 * s
    return [SP(0.3, y, 44.0, 2.1, "v-peau"), CY(0.3, y, 34.5, 44.0, 1.75, "v-peau", r2=2.1),
            SP(0.45, y, 32.6, 2.0, "v-peau", (0.85, 0.65, 1.2))]


def jambe(s):
    y = 4.0 * s
    return [CY(0.5, y, 3.0, 33.5, 2.5, "v-pantalon", r2=3.9),
            BX(-2.6, 6.8, y - 1.95, y + 1.95, 0.0, 3.4, "v-souliers", r=1.3)]


# poses : [balancement, écart, lacet] en degrés. Balancement positif = le bas de la partie vers l'avant (tête : vers l'arrière,
# elle lève le menton) ; écart positif = vers l'extérieur ; lacet positif = vers sa gauche.
PERSONNAGE = {
    "couleurs": COULEURS,
    "hauteur": 72, "foulee": 46, "rebond": 0.8, "vitesse": 40, "rayon": 11,
    "objets": [CY(0.5, 0, 29.0, 38.0, 7.0, "v-pantalon", r2=7.4, echelle=[0.62, 1, 1]),   # bassin (dans le prolongement des cuisses)
               CY(0.5, 0, 36.8, 38.2, 7.5, "v-ceinture", echelle=[0.66, 1, 1])],            # ceinture (sous la bedaine)
    "parties": [
        {"id": "jambe_g", "pivot": [0.5, 4.0, 33.0], "objets": jambe(1), "balance": 24, "phase": 0,
         "poses": {"pet": [-4, 3]}},
        {"id": "jambe_d", "pivot": [0.5, -4.0, 33.0], "objets": jambe(-1), "balance": 24, "phase": 180,
         "poses": {"pet": [-8, 22]}},                                                       # il lève la jambe pour forcer
        {"id": "haut", "pivot": [0.5, 0, 36.0], "objets": haut_du_corps(),
         "poses": {"dire": [-4], "pet": [7], "content": [-2]}},
        {"id": "tete", "parent": "haut", "pivot": [0.8, 0, 58.5], "objets": tete(),
         "poses": {"dire": [14], "pet": [9, 0, -8], "content": [6, 0, 22], "cogner": [-2, 0, 42]}},
        {"id": "bras_g", "parent": "haut", "pivot": [0.3, 9.4, 54.3], "objets": bras(1), "balance": 18, "phase": 180,
         "poses": {"repos": [0, 7], "cogner": [55, 4], "dire": [28, 32], "pet": [12, 16], "content": [14, -12]}},
        {"id": "avant_bras_g", "parent": "bras_g", "pivot": [0.3, 9.6, 44.0], "objets": avant_bras(1), "balance": 8, "phase": 180,
         "frappe": 16, "poses": {"repos": [8], "cogner": [55], "dire": [40], "pet": [25], "content": [72]}},
        {"id": "bras_d", "parent": "haut", "pivot": [0.3, -9.4, 54.3], "objets": bras(-1), "balance": 18, "phase": 0,
         "poses": {"repos": [0, 7], "dire": [28, 32], "pet": [12, 18], "content": [14, -12]}},
        {"id": "avant_bras_d", "parent": "bras_d", "pivot": [0.3, -9.6, 44.0], "objets": avant_bras(-1), "balance": 8, "phase": 0,
         "poses": {"repos": [8], "dire": [40], "pet": [25], "content": [72]}},
    ],
}

# ------------------------------------------------------------------------------------------------- le scénario
# Il frappe avec la main gauche (côté -x de la maison quand il regarde la porte, celui qu'on voit de l'arrêt) en tournant la
# tête vers la rue : poing à ~21 po devant lui, à ~52 po du perron ; debout à y = -13 (bedaine à 2 po du parement), dans
# l'axe de la porte, le poing touche le vantail (x ≈ 189, y = 8,2, dans l'embrasure).
COGNE = [199, -13]
CRI = [202, 88]                    # dans l'entrée, entre le banc à bottes et le garde-corps de l'escalier
TROTTOIR = [228, -462]
PIED_MARCHES = [200, -104]

SCENARIO = {
    "id": "visiteur", "nom": "Le visiteur", "libelle": "Quelqu'un cogne", "libelle_arret": "Arrêter le visiteur",
    "libelle_son": "Son du visiteur", "volume": 0.5,
    "personnage": PERSONNAGE,
    "depart": {"x": TROTTOIR[0], "y": TROTTOIR[1], "cap": 95, "etage": "EXT"},
    "depart_bouton": 1,            # le bouton et l'arrêt le font partir du pied des marches (il cogne 3 s plus tard)
    "declencheur": {"x": 199, "y": 0, "z": Z_RDC, "rayon": 156, "hauteur": 60, "attente": 120, "auto": True},
    "vue": {"x": 80, "y": -36, "cap": 10, "etage": "EXT", "tangage": 8},
    "etapes": [
        {"marcher": [PIED_MARCHES], "vitesse": 40},                                       # 0 : monte le terrain du trottoir
        {"marcher": [COGNE], "vitesse": 32},                                              # 1 : monte les marches (bouton : ici)
        {"tourner": 90},
        {"cogner": 3, "intervalle": 0.42, "bulle": "TOC ! TOC ! TOC !", "bulle_style": "son"},
        {"attendre": 0.6},
        {"dire": "JULIEEEEE !", "voix": "Juliiiiiie !", "duree": 2.8, "bulle_style": "cri"},
        {"attendre": 1.3},
        {"ouvrir": PORTE, "duree": 1.0},
        {"marcher": [[200, 40], CRI], "vitesse": 34},                                     # il entre
        {"tourner": 80},
        {"dire": "JULIEEEEE !", "voix": "Juliiiiiie !", "duree": 2.8, "bulle_style": "cri"},
        {"attendre": 0.7},
        {"son": "pet", "bulle": "PRRRT !", "bulle_style": "nuage", "duree": 2.3, "vibre": 0.35, "nuage": True},
        {"attendre": 2.2, "pose": "content"},
        {"marcher": [[199, 30], [196, -16]], "vitesse": 36},                              # il ressort
        {"fermer": PORTE, "duree": 0.2},
        {"marcher": [PIED_MARCHES, TROTTOIR], "vitesse": 40},                             # et s'en retourne
    ],
}


# ------------------------------------------------------------------------------------------------- sol de l'extérieur (arrêt)
def _dans(pts, x, y):
    c = False
    for i in range(len(pts)):
        (xa, ya), (xb, yb) = pts[i - 1], pts[i]
        if (ya > y) != (yb > y) and x < xa + (y - ya) * (xb - xa) / (yb - ya):
            c = not c
    return c


def sol_ext(X, x, y):
    """Dessus du sol dehors en (x, y) : le plus haut plancher qui le couvre, sinon le relief (mêmes triangles que le moteur)."""
    import bisect
    h = None
    for p in X.get("planchers") or []:
        if _dans(p["pts"], x, y) and (h is None or p["z"] > h):
            h = p["z"]
    R = X.get("relief")
    if R:
        xs, ys, Z = R["xs"], R["ys"], R["z"]
        i = min(max(bisect.bisect_right(xs, x) - 1, 0), len(xs) - 2)
        j = min(max(bisect.bisect_right(ys, y) - 1, 0), len(ys) - 2)
        u, v = (x - xs[i]) / (xs[i + 1] - xs[i]), (y - ys[j]) / (ys[j + 1] - ys[j])
        z00, z10, z01, z11 = Z[j][i], Z[j][i + 1], Z[j + 1][i], Z[j + 1][i + 1]
        t = z00 + u * (z10 - z00) + v * (z11 - z10) if u >= v else z00 + v * (z01 - z00) + u * (z11 - z01)
    else:
        t = X.get("sol", 48)
    return max(h, t) if h is not None and h <= t + 8.5 else (h if h is not None else t)


def appliquer_scene_finale(SCENE):
    SCENE.setdefault("scenarios", []).append(SCENARIO)
    X = SCENE.get("exterieur")
    if X is not None:
        v = SCENARIO["vue"]
        arret = {"nom": "Le visiteur à la porte", "x": v["x"], "y": v["y"], "cap": v["cap"], "tangage": v["tangage"],
                 "z": round(sol_ext(X, v["x"], v["y"]), 1), "scenario": "visiteur"}
        vis = X.setdefault("visites", [])
        vis.insert(min(1, len(vis)), arret)                  # deuxième arrêt de l'extérieur, après la façade avant
