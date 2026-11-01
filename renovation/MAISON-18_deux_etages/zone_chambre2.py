"""SS-17 — zone CHAMBRE 2 (le grand, 6 ans) et son WALK-IN (ancien caveau) : « La bibliothèque secrète ».

Spec : conception SS-17, final_chambre2.json (plan, élévations A-D, walk-in). Tout le mur arrière (y = 370) devient un
meuble de tête intégré : porte-bibliothèque secrète (x 245-277) qui pivote vers le walk-in, tour gauche, deux chevets-
niches éclairés, alcôve de lattes de chêne pour le lit queen sur plateforme à tiroirs, pont d'armoires hautes jusqu'au
banc-cabane sous la fenêtre ; tour à trésors dans le coin NE, garage à jouets sous des rebords à livres (mur du
vestiaire), mur d'activité avec bureau à rabat sur rail (mur mitoyen x = 240, côté chambre 2 seulement : x ≥ 242¼).
Walk-in : isolé (fini 83 × 47½, plafond supposé à 84), penderie double sur crémaillères, banc à souliers, tour de
tiroirs, miroir au dos de la porte-bibliothèque, panneau rayonnant au plafond.

Pièce réelle : x 242¼-446, y 232¼-370 ; walk-in brut x 229-317, y 380-430. Pouces, repère de la maison.
Écart volontaire avec la spec : le mur d'activité commence à y = 265 (au lieu de 264) pour ne pas toucher le battant
ouvert de la porte de la chambre (ouv-SS-P06, bout du battant à y = 264¼ dans la maquette).
"""
import random

# --------------------------------------------------------------------------------------------- emprises de la zone
CH2 = (242.0, 232.0, 447.0, 371.0)          # chambre 2 (x0, y0, x1, y1)
WI = (228.0, 379.0, 318.0, 431.0)           # walk-in (ancien caveau)

BLANC = "laque-blanc-chaud"                  # alias de peinture ajouté dans appliquer_scene (armoires hautes)
COUL_LIVRES = ["laque-marine", "art-argile", "draps", "carbone", "osier", "art-sable", "tissu", "cuir", "blanc",
               "laque-marine", "art-argile", "osier"]
COUL_VET = ["laque-marine", "draps", "art-argile", "tissu", "osier", "carbone", "art-sable", "cuir", "blanc"]


# ============================================================================================ PLAN (modifs.py)
def appliquer_modifs(L, base):
    """Plan : la commode SS-16 de la chambre 2 disparaît ; nouveaux meubles intégrés (rectangles du plan)."""
    L["EQUIPEMENTS"][:] = [e for e in L["EQUIPEMENTS"] if e[0] != "elem-SS-P-COMMODE2"]
    L["EQUIPEMENTS"] += [
        ("elem-SS-P-CH2-LIT", "autre", "Lit-plateforme queen intégré : socle de chêne à tiroirs, 2 bacs-wagons au pied, "
         "matelas 60 × 80 (dessus à 22 po), tête dans l'alcôve de lattes", "LIT QUEEN", 355, 325, 0, (66, 84)),
        ("elem-SS-P-CH2-PB", "autre", "Porte-bibliothèque secrète (pivots, livre-levier, miroir au dos) devant la baie du "
         "walk-in ; imposte-bibliothèque fixe au-dessus", "", 260.125, 366, 0, (35.75, 8)),
        ("elem-SS-P-CH2-TG", "armoires", "Tour gauche du mur de tête (bacs, niches éclairées, armoire haute), ancrée",
         None, 290, 364, 0, (24, 12)),
        ("elem-SS-P-CH2-NG", "comptoir", "Chevet-niche gauche intégré (tiroir, niche éclairée, USB-C)", None, 312, 364, 0, (20, 12)),
        ("elem-SS-P-CH2-LATTES", "autre", "Panneau de tête en lattes de chêne sur feutre (alcôve du lit), 2 liseuses DEL",
         "", 355, 368.5, 0, (66, 3)),
        ("elem-SS-P-CH2-ND", "comptoir", "Chevet-niche droit intégré (tiroir, niche éclairée, USB-C)", None, 403, 364, 0, (30, 12)),
        ("elem-SS-P-CH2-PONT", "trappe", "Pont d'armoires hautes (z 66-96) au-dessus des niches, du lit et du bout du banc ; "
         "DEL dessous", "", 374, 364, 0, (144, 12)),
        ("elem-SS-P-CH2-BANC", "comptoir", "Banc-cabane sous la fenêtre (assise 18, 3 tiroirs, trappe d'accès au drain, "
         "coussin = lit d'appoint) ; rail-rideau au plafond", "", 432, 316, 0, (28, 108)),
        ("elem-SS-P-CH2-TOUR", "armoires", "Tour d'angle à trésors (bacs à jouets, vitrine LEGO, armoire haute), ancrée",
         None, 432, 247.125, 0, (28, 29.75)),
        ("elem-SS-P-CH2-GARAGE", "comptoir", "Garage à jouets : banc bas de 16 po, 4 bacs-wagons ; rebords à livres et "
         "rail de galerie au-dessus", "", 351, 240.25, 0, (134, 16)),
        ("elem-SS-P-CH2-ACTIV", "comptoir", "Mur d'activité (12 po) : crochets, cases basses, bureau à rabat sur rail, "
         "panneau perforé, armoires hautes", "", 248.25, 296.5, 0, (12, 63)),
        ("elem-SS-P-WI-PENDERIE", "autre", "Walk-in : penderie double sur crémaillères (tringles z 34 et 70, tablette et "
         "bacs z 74)", "", 273, 416.5, 0, (83, 22)),
        ("elem-SS-P-WI-BANC", "comptoir", "Walk-in : banc à souliers et crochets", None, 238.5, 392.75, 0, (14, 25.5)),
        ("elem-SS-P-WI-TOUR", "armoires", "Walk-in : tour de tiroirs, panier à linge et valet (ancrée)", None, 305.5, 392.75, 0, (18, 25.5)),
    ]


def apres_modifs(maison, base):
    """La porte du caveau (ouverture de la base ouv-SS-008) devient la porte-bibliothèque : même baie, même sens.
    « fermee » : dans la maquette 3D, le battant uni n'est plus dessiné ouvert (il traverserait la bibliothèque) ; il
    reste fermé dans la baie, caché derrière la porte-bibliothèque, et porte le miroir côté walk-in."""
    ss = next(n for n in maison["niveaux"] if n["id"] == "SS")
    for o in ss["ouvertures"]:
        if o["id"] == "ouv-SS-008":
            o["fermee"] = True
            o["interieure"] = True
            o["sens"] = dict(o.get("sens") or {}, charniere="fin", ouvre_vers="gauche",
                             note="porte-bibliothèque secrète pivotante (pentures/pivots côté ouest, ouvre vers la chambre), "
                                  "miroir au dos ; s'ouvre en poussant depuis le walk-in, aucun verrou — proposition SS-17 (esquisse)")
            o["note"] = ((o.get("note") or "") + " SS-17 : la porte devient une porte-bibliothèque pivotante (32 × 82, "
                         "8 po hors tout) posée devant la baie, côté chambre 2.")
    for p in ss["pieces"]:
        if p["id"] == "piece-SS-LEG":
            p["description"] = ("Ancien caveau à légumes isolé (2 po rigide + gypse, fini 83 × 47½, plafond supposé à 84 : À "
                                "MESURER) : walk-in de la chambre 2 — penderie double sur crémaillères (tringles z 34 et 70), "
                                "banc à souliers, tour de tiroirs, miroir au dos de la porte-bibliothèque, panneau rayonnant "
                                "au plafond — proposition SS-17 (esquisse)")


# ============================================================================================ 3D (scene_3d.py)
def _centre(o):
    f = o.get("forme", "boite")
    if f in ("boite", "arrondi") and "x0" in o:
        return (o["x0"] + o["x1"]) / 2, (o["y0"] + o["y1"]) / 2
    if f == "cylindre" and o.get("axe") == "x":
        return (o["x0"] + o["x1"]) / 2, o["y"]
    if f == "cylindre" and o.get("axe") == "y":
        return o["x"], (o["y0"] + o["y1"]) / 2
    if f == "tube":
        return sum(p[0] for p in o["pts"]) / len(o["pts"]), sum(p[1] for p in o["pts"]) / len(o["pts"])
    if "x" in o and "y" in o:
        return o["x"], o["y"]
    return None


def _dans(c, r):
    return c is not None and r[0] < c[0] < r[2] and r[1] < c[1] < r[3]


def _ma_zone(o):
    if o.get("forme", "boite") == "boite" and o.get("z1", 1) <= 0.06:
        return False                              # traits de scie du béton poli : gardés (dalle)
    c = _centre(o)
    return _dans(c, CH2) or _dans(c, WI)


def livres(h, x0, x1, ya, z, hmin, hmax, seed, dmin=5.0, dmax=7.0):
    """Livres debout le long de x, dos vers -y (dos à y ≈ ya), posés à z."""
    rng = random.Random(seed)
    out, x = [], x0
    while True:
        w = rng.uniform(0.55, 1.5)
        if x + w > x1:
            break
        hh, d, dy = rng.uniform(hmin, hmax), rng.uniform(dmin, dmax), rng.uniform(0, 0.35)
        out.append(h.B(x, ya + dy, x + w, ya + dy + d, z, z + hh, rng.choice(COUL_LIVRES)))
        x += w + (rng.uniform(1.2, 2.6) if rng.random() < 0.08 else 0.06)
    return out


def couvertures(h, x0, x1, ymur, z, seed):
    """Livres présentés de face (couverture vers +y) sur un rebord à lèvre, appuyés au mur y = ymur."""
    rng = random.Random(seed)
    out, x = [], x0 + rng.uniform(1, 4)
    while True:
        w, hh = rng.uniform(7, 10), rng.uniform(7.5, 11)
        if x + w > x1:
            break
        c1, c2 = rng.sample(["laque-marine", "art-argile", "osier", "art-sable", "draps", "carbone", "blanc"], 2)
        out += [h.B(x, ymur + 0.4, x + w, ymur + 0.9, z, z + hh, c1),
                h.B(x + 1, ymur + 0.9, x + w - 1, ymur + 1.0, z + 2.5, z + hh - 2, c2)]           # illustration
        x += w + rng.uniform(2.5, 6)
    return out


def chevet(h, x0, x1, seed):
    """Chevet-niche intégré (12 po de profondeur, y 358-370, z 0-66) : base ouverte, tiroir, niche éclairée avec USB-C,
    tablette à 44, niche haute ; tout en chêne."""
    B, A, C, SPH = h.B, h.A, h.C, h.SPH
    xc = (x0 + x1) / 2
    out = [B(x0, 358, x0 + 0.75, 370, 0, 66, "placage"), B(x1 - 0.75, 358, x1, 370, 0, 66, "placage"),
           B(x0 + 0.75, 369.25, x1 - 0.75, 370, 0, 66, "placage"),
           B(x0 + 0.75, 360, x1 - 0.75, 369.25, 0, 2.25, "carbone"),                       # socle en retrait
           B(x0 + 0.75, 358, x1 - 0.75, 369.25, 2.25, 3, "placage"),                       # base ouverte z 3-13
           B(x0 + 0.75, 358.5, x1 - 0.75, 369.25, 13.25, 22, "placage"),                   # caisson du tiroir
           A(x0 + 0.9, 357.7, x1 - 0.9, 358.6, 13.6, 21.9, "placage", r=0.3, b=0.2),       # façade du tiroir
           A(xc - 3, 357.35, xc + 3, 357.75, 19.2, 20.2, "carbone", r=0.4, b=0.1),         # poignée découpée
           B(x0 + 0.75, 358, x1 - 0.75, 369.25, 22, 22.75, "placage"),                     # fond de la niche
           B(x0 + 0.75, 358, x1 - 0.75, 369.25, 43.75, 44.5, "placage"),                   # tablette z 44
           B(x0 + 1, 358.4, x1 - 1, 358.9, 43.3, 43.75, "spot"),                           # DEL de la niche
           B(x0 + 0.75, 358, x1 - 0.75, 370, 65.25, 66, "placage"),                        # dessus (sous le pont)
           B(xc - 1.6, 369.05, xc + 1.6, 369.25, 26.5, 29.5, "blanc"),                      # prise USB-C + interrupteur
           B(xc - 0.7, 368.95, xc - 0.1, 369.05, 27.6, 28.4, "carbone"), B(xc + 0.2, 368.95, xc + 0.9, 369.05, 27.4, 28.6, "carbone")]
    # veilleuse (boule lumineuse), livre posé, pantoufles, quelques livres dans la niche haute
    out += [C(x0 + 4.5, 363.5, 2.2, 22.75, 23.5, "carbone"), SPH(x0 + 4.5, 363.5, 25.6, 2.4, "abat-jour"),
            B(x1 - 9.5, 360.5, x1 - 2.5, 367.5, 22.75, 23.6, "laque-marine"), B(x1 - 9, 361, x1 - 3, 367, 23.6, 24.3, "art-sable"),
            A(x0 + 2, 359.5, x0 + 5.6, 367, 3, 5.4, "tissu", r=1.6, b=0.9), A(x0 + 6, 359.5, x0 + 9.6, 367, 3, 5.4, "tissu", r=1.6, b=0.9)]
    out += livres(h, x0 + 1.5, x1 - 4, 361.5, 44.5, 7, 10.5, seed, 5, 7)
    return out


def appliquer_scene(S, h):
    B, A, C, CY, CX, T, SPH, TOR = h.B, h.A, h.C, h.CY, h.CX, h.T, h.SPH, h.TOR
    S["mobilier"][:] = [o for o in S["mobilier"] if not _ma_zone(o)]
    pe = S.setdefault("peintures", {})
    global BLANC
    deja = next((v for k, v in pe.items() if k == "Blanc chaud mat" and len(v) > 2), None)
    if deja:
        BLANC = deja[2]
    else:
        pe["Blanc chaud mat"] = ["#EEEAE2", "armoires hautes de la chambre 2 (pont, tours, mur d'activité), laque mate "
                                 "(≈ Benjamin Moore White Dove OC-17)", BLANC]
    M = []

    # ------------------------------------------------------------------ porte-bibliothèque secrète (PB) et imposte
    # Panneau 32 × 82, 8 po hors tout (x 245-277, y 362-370), pivots côté ouest ; 5 rebords à lèvre (rien sous 8 po),
    # livre-levier rouge ; joints d'ombre de 0,2 po tout autour (seul indice que c'est une porte).
    M += [B(242.25, 362, 244.8, 370, 0, 82, "placage"), B(277.2, 362, 278, 370, 0, 82, "placage"),        # fourrures fixes
          B(244.8, 361.95, 245.0, 370, 0, 82, "carbone"), B(277.0, 361.95, 277.2, 370, 0, 82, "carbone"),  # joints d'ombre
          B(244.8, 361.95, 277.2, 370, 81.75, 82, "carbone")]
    M += [A(245, 362, 246.5, 370, 0.25, 81.75, "placage", r=0.2, b=0.15), A(275.5, 362, 277, 370, 0.25, 81.75, "placage", r=0.2, b=0.15),
          B(246.5, 362, 275.5, 370, 79.5, 81.75, "placage"),                                            # traverse du haut
          A(246.5, 362.2, 275.5, 370, 0.25, 8, "placage", r=0.2, b=0.15),                               # socle plein
          B(246.5, 366, 275.5, 370, 8, 79.5, "placage")]                                                # âme (caisson-torsion)
    for k, z in enumerate((8, 22, 36, 50, 64)):
        M += [B(246.5, 362.5, 275.5, 366, z, z + 0.75, "placage"), B(246.5, 362.25, 275.5, 362.75, z + 0.75, z + 1.75, "placage")]
        if k == 3:                                                                                       # livre-levier
            M += livres(h, 247, 258.4, 362.8, z + 0.75, 7.5, 10.5, 40 + k, 2.9, 3.15)
            M += [B(258.7, 362.55, 260.5, 366, z + 0.75, z + 11.2, "rouge-velo"),
                  B(258.7, 362.5, 260.5, 362.6, z + 9, z + 9.6, "laiton")]
            M += livres(h, 260.9, 274.8, 362.8, z + 0.75, 7.5, 10.5, 50 + k, 2.9, 3.15)
        else:
            xf = 249 + (k * 7) % 14                                                                     # un livre de face
            M += livres(h, 247, xf - 0.4, 362.8, z + 0.75, 7, 11, 40 + k, 2.9, 3.15)
            M += [B(xf, 365.3, xf + 8, 365.9, z + 0.75, z + 10.5, ["art-argile", "laque-marine", "osier", "art-sable", "draps"][k]),
                  B(xf + 1, 365.2, xf + 7, 365.3, z + 3, z + 8.5, ["draps", "art-sable", "laque-marine", "carbone", "art-argile"][k])]
            M += livres(h, xf + 8.4, 274.8, 362.8, z + 0.75, 7, 11, 50 + k, 2.9, 3.15)
    # imposte-bibliothèque fixe (cache le linteau) : deux rebords de livres de collection
    M += [B(242.25, 366, 278, 370, 82, 96, "placage"), B(242.25, 362, 278, 366, 82, 83, "placage"),
          B(242.25, 362, 243, 366, 83, 96, "placage"), B(277.25, 362, 278, 366, 83, 96, "placage"),
          B(243, 362.3, 277.25, 366, 88.9, 89.6, "placage"), B(242.25, 362, 278, 366, 95.25, 96, "placage")]
    M += livres(h, 243.5, 276.5, 362.6, 83, 4.8, 5.8, 61, 3, 3.3) + livres(h, 243.5, 276.5, 362.6, 89.6, 4.6, 5.5, 62, 3, 3.3)

    # ------------------------------------------------------------------ tour gauche TG (x 278-302)
    M += [B(278, 358, 278.75, 370, 0, 96, "placage"), B(301.25, 358, 302, 370, 0, 96, "placage"),
          B(278.75, 360, 301.25, 370, 0, 3, "carbone"),
          A(278.85, 358, 301.15, 370, 3, 23.9, "placage", r=0.3, b=0.25),                              # porte du bas (bacs)
          A(286, 357.7, 294, 358.1, 21, 22.2, "carbone", r=0.4, b=0.1),
          B(278.75, 369.25, 301.25, 370, 24, 66, "placage"), B(278.75, 358, 301.25, 370, 23.9, 24.65, "placage"),
          B(278.75, 358.4, 301.25, 370, 44.6, 45.35, "placage"),
          B(279, 358.5, 301, 359, 44.1, 44.6, "spot"), B(279, 358.5, 301, 359, 65.5, 66, "spot"),
          A(278.75, 358, 301.25, 370, 66, 96, BLANC, r=0.25, b=0.25)]                                   # armoire haute (adulte)
    M += livres(h, 279.5, 293, 360.5, 24.65, 8, 11.5, 71, 6, 8.5)
    M += [B(294.5, 360.5, 300.5, 368.5, 24.65, 25.6, "art-argile"), B(295, 361, 300, 368, 25.6, 26.4, "laque-marine")]
    # trésors : globe, bocal de cailloux, coffre
    M += [C(285, 364, 2.4, 45.35, 46.2, "carbone"), C(285, 364, 0.3, 46.2, 49, "laiton"), SPH(285, 364, 53, 4.3, "laque-marine"),
          TOR(285, 364, 53, 4.9, 0.18, "laiton"),
          C(292.5, 364.5, 1.9, 45.35, 50.5, "verre-clair"), C(292.5, 364.5, 1.6, 45.6, 48.2, "art-sable"),
          A(295.5, 361, 300.5, 368, 45.35, 49.5, "cuir", r=0.6, b=0.4), B(295.4, 360.9, 300.6, 368.1, 47.5, 47.8, "laiton")]

    # ------------------------------------------------------------------ chevets-niches NG (302-322) et ND (388-418)
    M += chevet(h, 302, 322, 81) + chevet(h, 388, 418, 82)

    # ------------------------------------------------------------------ alcôve : lattes de chêne sur feutre noir, liseuses
    M += [B(322, 369.4, 388, 370, 0, 66, "pneu")]
    M += [B(322.5 + 2 * k, 367.9, 323.5 + 2 * k, 369.4, 0, 66, "placage") for k in range(33)]
    for xl in (333, 377):
        M += [CY(xl, 367.5, 367.9, 39, 1.6, "carbone", pans=32), CY(xl, 367.35, 367.5, 39, 1.1, "spot", pans=32)]

    # ------------------------------------------------------------------ lit-plateforme queen intégré (66 × 84, dessus 12)
    M += [B(325, 306, 385, 364, 0, 3, "carbone"),                                                       # socle en retrait
          A(322, 283, 388, 367, 3, 12, "placage", r=1, b=0.4)]
    for xs, xp in ((321.5, 321.2), (387.7, 388.4)):                                                     # 2 tiroirs par côté
        for ya, yb in ((306.5, 335.2), (336, 364.7)):
            yc = (ya + yb) / 2
            M += [A(xs, ya, xs + 0.8, yb, 3.8, 11.4, "placage", r=0.3, b=0.2),
                  A(xp, yc - 3, xp + 0.4, yc + 3, 9, 10.3, "carbone", r=0.4, b=0.1)]
    # bacs-wagons du pied (30 × 22 × 9 sur roulettes) : celui de gauche rangé, celui de droite sorti (LEGO)
    M += [A(324, 282.4, 354, 283.2, 1.2, 11.4, "placage", r=0.4, b=0.2), A(336, 282.1, 342, 282.5, 8.6, 10, "carbone", r=0.6, b=0.1),
          C(326.5, 284.5, 0.6, 0, 1.2, "carbone"), C(351.5, 284.5, 0.6, 0, 1.2, "carbone")]
    M += [A(356.5, 269.2, 385.5, 291, 1.2, 10.4, "placage", r=1, b=0.3, trou=0.6),
          A(356, 268.4, 386, 269.2, 1.2, 11.4, "placage", r=0.4, b=0.2), A(368, 268.1, 374, 268.5, 8.6, 10, "carbone", r=0.6, b=0.1)]
    M += [C(x, y, 0.6, 0, 1.2, "carbone") for x in (358.5, 383.5) for y in (271, 289)]
    rng = random.Random(7)
    for _ in range(14):
        x, y = rng.uniform(358, 382), rng.uniform(270.5, 281)
        w, d = rng.choice([(2.5, 1.25), (1.25, 2.5), (1.25, 1.25), (5, 1.25)])
        z = rng.uniform(5.5, 8)
        M.append(B(x, y, x + w, y + d, z, z + 1.2, rng.choice(["rouge-velo", "laque-marine", "blanc", "osier", "art-argile"])))
    # matelas, couette, oreillers, jeté, ourson
    M += [A(325, 285, 385, 365, 12, 22, "draps", r=3, b=2.5),
          A(324.4, 284.4, 385.6, 344, 20.8, 23.6, "tissu", r=2.5, b=1.2),                              # couette
          A(324.6, 338, 385.4, 346, 22.6, 24.4, "draps", r=2, b=1),                                     # rabat du drap
          A(324.2, 285.5, 385.8, 299, 23.4, 24.6, "laque-marine", r=1.5, b=0.6),                       # jeté au pied
          A(329, 345, 353, 362, 21, 27.5, "draps", r=4, b=3), A(357, 345, 381, 362, 21, 27.5, "draps", r=4, b=3),
          SPH(372, 342, 27.6, 3.4, "osier", ecrase=0.9), SPH(372, 343, 32.4, 2.5, "osier"),
          SPH(370.4, 343, 34.4, 0.9, "osier"), SPH(373.6, 343, 34.4, 0.9, "osier"), SPH(372, 340.7, 32, 0.8, "art-sable")]

    # ------------------------------------------------------------------ pont d'armoires hautes (x 302-446, z 66-96)
    M += [A(302 + 24 * k + 0.08, 358, 302 + 24 * (k + 1) - 0.08, 370, 66, 96, BLANC, r=0.25, b=0.25) for k in range(6)]
    M += [B(303, 358.4, 445, 359.1, 65.6, 66, "spot")]                                                  # DEL de lecture

    # ------------------------------------------------------------------ banc-cabane sous la fenêtre (x 418-446, y 262-370)
    M += [B(420, 264, 446, 368, 0, 3, "carbone"), A(418, 262, 446, 370, 3, 14, "placage", r=1, b=0.4)]
    for ya, yb in ((262.6, 297.6), (298.4, 333.6), (334.4, 369.4)):
        yc = (ya + yb) / 2
        M += [A(417.4, ya, 418.2, yb, 3.6, 13.4, "placage", r=0.3, b=0.2), A(417.05, yc - 3.5, 417.5, yc + 3.5, 10.6, 11.8, "carbone", r=0.4, b=0.1)]
    M += [A(418.6, 262.6, 446, 369.4, 14, 18, "tissu", r=2, b=1.5)]                                    # coussin attaché
    for k, (ya, yb) in enumerate(((263.5, 289.5), (290.5, 316), (317, 342.5), (343.5, 369.2))):
        M.append(A(439.6, ya, 445.9, yb, 18, 33, ["tapis", "osier", "tapis", "osier"][k], r=2.6, b=2))  # coussins de dos
    M += [A(433, 350, 439.5, 364, 18, 29, "laque-marine", r=3, b=2.5), A(433.5, 268, 439.5, 280, 18, 28, "art-argile", r=3, b=2.5)]
    for yl in (265.5, 366.5):                                                                           # liseuses murales + USB
        M += [B(445.2, yl - 1.4, 446, yl + 1.4, 40.5, 46.5, "metal"), CX(441.6, 445.2, yl, 44.5, 0.3, "metal"),
              C(441.2, yl, 1.7, 41.8, 44.8, "metal", pans=24), C(441.2, yl, 1.3, 41.6, 41.8, "spot", pans=24),
              B(445.6, yl - 0.6, 445.9, yl + 0.6, 41, 42.2, "blanc")]
    # (rail-rideau au plafond retiré à la demande du client, 2026-11-01)

    # ------------------------------------------------------------------ tour d'angle à trésors NE (x 418-446, y 232¼-262)
    M += [B(418, 232.25, 446, 233, 0, 66, "placage"), B(418, 261.25, 446, 262, 0, 66, "placage"),
          B(418, 233, 446, 261.25, 0, 0.1, "placage"), B(420, 233, 445.25, 261.25, 0, 2.25, "carbone"),
          B(445.25, 233, 446, 261.25, 2.25, 66, "placage")]
    M += [B(418, 233, 445.25, 261.25, z, z + 0.75, "placage") for z in (2.25, 16.5, 30.75, 44.25, 65.25)]
    M += [B(419.5, 233, 445.25, 261.25, 55, 55.6, "placage")]
    for k, (zb, mat, photo) in enumerate(((3, "art-argile", "laque-marine"), (17.25, "laque-marine", "osier"), (31.5, "osier", "art-argile"))):
        M += [A(419.4, 234.3, 443.8, 259.9, zb + 0.2, zb + 11.6, mat, r=1.5, b=0.6),
              B(419.1, 243.2, 419.4, 249.6, zb + 5.6, zb + 9.8, "blanc"), B(419.0, 244.0, 419.1, 248.8, zb + 6.3, zb + 9.1, photo)]
    M += [B(418.5, 233.3, 419.1, 260.9, 64.75, 65.25, "spot"), B(418.5, 233.3, 419.1, 260.9, 54.5, 55, "spot")]
    # vitrine LEGO : une maison, une auto, une petite tour
    M += [B(424, 236, 436, 246, 45, 48.5, "rouge-velo"), B(424.5, 236.5, 435.5, 245.5, 48.5, 50.5, "blanc"),
          B(425, 237, 435, 245, 50.5, 52.5, "laque-marine"), B(427, 234.4, 430, 236, 45, 48, "osier"),
          B(424, 250, 432, 254, 45, 46.5, "blanc"), B(425, 250.5, 429, 253.5, 46.5, 48.2, "laque-marine"),
          B(424.6, 249.6, 425.8, 250, 45, 46.4, "carbone"),
          B(430.2, 249.6, 431.4, 250, 45, 46.4, "carbone"),
          B(436, 251, 440, 255, 45, 53, "art-sable"), B(436.4, 251.4, 439.6, 254.6, 53, 54.6, "rouge-velo")]
    M += livres(h, 421, 438, 238, 55.6, 6.5, 8.5, 91, 5, 6)
    M += [A(418, 232.25, 446, 262, 66, 96, BLANC, r=0.25, b=0.25)]                                    # armoire haute

    # ------------------------------------------------------------------ garage à jouets (x 284-418, y 232¼-248¼, banc à 16)
    M += [B(284, 232.25, 418, 233, 0, 14.5, "placage")]
    M += [B(x, 232.25, x + 0.75, 248.25, 0, 14.5, "placage") for x in (284, 317.3, 350.6, 383.9, 417.25)]
    M += [B(284, 233, 418, 248.25, 0, 0.6, "placage"), A(284, 232.25, 418, 248.25, 14.5, 16, "placage", r=1, b=0.5)]
    for k, xc in enumerate((301, 334.3, 367.6, 400.9)):
        mat = ["laque-marine", "art-argile", "osier", "art-sable"][k]
        M += [A(xc - 15, 233.6, xc + 15, 247.6, 1.4, 13.2, "placage", r=1.2, b=0.4),
              A(xc - 3.2, 247.45, xc + 3.2, 247.8, 9.6, 11.4, "carbone", r=0.6, b=0.1),             # poignée découpée
              B(xc - 3, 247.6, xc + 3, 247.75, 4, 8, "blanc"), B(xc - 2.4, 247.75, xc + 2.4, 247.85, 4.6, 7.4, mat)]  # photo
        M += [C(xc + dx, 246, 0.55, 0, 1.4, "pneu") for dx in (-12.5, 12.5)]
    # camion de bois sur le banc
    M += [A(296, 238, 307, 244, 17.6, 21.5, "art-argile", r=0.6, b=0.4), A(307.2, 238.4, 311.5, 243.6, 17.6, 23.4, "laque-marine", r=0.6, b=0.4),
          B(307.6, 238.3, 311.2, 238.4, 20.5, 22.6, "verre-clair")]
    M += [CY(x, y0, y0 + 0.9, 17.2, 1.2, "carbone", pans=20) for x in (298.5, 309) for y0 in (237.2, 243.9)]
    # rebords à livres (z 26 et 40, 3 po, lèvre) et rail de galerie magnétique (dessins)
    for z, s in ((26, 11), (40, 12)):
        M += [B(284, 232.25, 418, 235.25, z, z + 0.75, "placage"), B(284, 234.75, 418, 235.25, z + 0.75, z + 1.9, "placage")]
        M += couvertures(h, 285, 417, 232.25, z + 0.75, s)
    M += [B(284, 232.25, 418, 232.6, 58.5, 62, "metal")]
    rng = random.Random(5)
    x = 288
    for k in range(9):
        w, hh = (11, 8.5) if k % 3 else (8.5, 11)
        if x + w > 416:
            break
        z1 = 61 - rng.uniform(0, 1.2)
        fond = "blanc" if k % 2 else "draps"
        M += [B(x, 232.6, x + w, 232.75, z1 - hh, z1, fond), CY(x + w / 2, 232.75, 233.2, z1 - 0.8, 0.5, "carbone", pans=16)]
        c1, c2 = rng.sample(["art-argile", "laque-marine", "osier", "art-sable", "rouge-velo"], 2)
        if k % 3 == 0:          # soleil et maison
            M += [CY(x + w - 2.4, 232.75, 232.85, z1 - 2.6, 1.4, "osier", pans=20),
                  B(x + 1.5, 232.75, x + 5, 232.85, z1 - hh + 1, z1 - hh + 4, c1), B(x + 1.2, 232.75, x + 5.3, 232.85, z1 - hh + 4, z1 - hh + 5.2, c2)]
        elif k % 3 == 1:        # bonhomme et gribouillis
            M += [CY(x + 3.5, 232.75, 232.85, z1 - 2.8, 1.1, c1, pans=16), B(x + 3.2, 232.75, x + 3.8, 232.85, z1 - 7, z1 - 3.8, c1),
                  B(x + 6, 232.75, x + 9.5, 232.85, z1 - 5, z1 - 4.4, c2), B(x + 6.5, 232.75, x + 9, 232.85, z1 - 6.5, z1 - 5.9, c2)]
        else:                   # fusée
            M += [B(x + 3, 232.75, x + 5.5, 232.85, z1 - 9, z1 - 3, c1), B(x + 2.2, 232.75, x + 6.3, 232.85, z1 - 9.5, z1 - 8.5, c2)]
        x += w + rng.uniform(3, 6)

    # ------------------------------------------------------------------ mur d'activité (x 242¼-254¼, y 265-328) — mitoyen
    # colonne crochets (y 265-280)
    M += [B(242.25, 265, 254.25, 265.75, 0, 72, "placage"), B(242.25, 279.25, 254.25, 280, 0, 72, "placage"),
          B(242.25, 265.75, 243, 279.25, 0, 72, "placage"), B(243, 267, 254.25, 279.25, 0, 2.25, "carbone"),
          B(243, 265.75, 254.25, 279.25, 2.25, 3, "placage"), B(243, 265.75, 254.25, 279.25, 13.25, 14, "placage")]
    M += [A(244.2, 266.4, 252.6, 269.6, 3, 6.2, "laque-marine", r=1.4, b=0.8), A(244.2, 270, 252.6, 273.2, 3, 6.2, "laque-marine", r=1.4, b=0.8),
          A(245, 274, 251.5, 276.4, 3, 11.5, "art-argile", r=1.1, b=0.7), A(245, 276.6, 251.5, 279, 3, 11.5, "art-argile", r=1.1, b=0.7)]
    for z in (40, 56):
        for y in (269, 276):
            M += [CX(243, 246, y, z, 0.45, "placage"), SPH(246.3, y, z, 1.05, "placage")]
    M += [A(243.4, 265.9, 249.6, 273, 24.5, 39.2, "laque-marine", r=2.2, b=1.8),                    # sac d'école
          A(249.4, 266.6, 250.6, 272.3, 26, 33, "laque-marine", r=1, b=0.5), T([(246.3, 269, 40.3), (244.5, 269, 38.6)], 0.35, "carbone"),
          A(243.2, 273.6, 246.6, 278.8, 29, 40.4, "tapis", r=1.5, b=1.2)]                           # pyjama
    # cases basses (y 280-328, z 0-18) et bacs de bricolage
    M += [B(242.25, 280, 254.25, 280.75, 0, 18, "placage"), B(242.25, 327.25, 254.25, 328, 0, 18, "placage"),
          B(242.25, 303.6, 254.25, 304.4, 0, 18, "placage"), B(242.25, 280.75, 243, 327.25, 0, 18, "placage"),
          B(243, 282, 254.25, 326, 0, 2.25, "carbone"), B(243, 280.75, 254.25, 327.25, 2.25, 3, "placage"),
          A(242.25, 280, 254.25, 328, 17.25, 18, "placage", r=0.3, b=0.2),
          A(244, 281.7, 253.8, 302.7, 3, 14, "art-argile", r=1.5, b=0.6), A(244, 305.3, 253.8, 326.3, 3, 14, "laque-marine", r=1.5, b=0.6)]
    # caisson à casiers sur rail (z 22-46) et rabat ouvert (pupitre 40 × 20 à z 22) avec compas amortis
    M += [B(242.25, 280, 254.25, 280.75, 22, 46, "placage"), B(242.25, 327.25, 254.25, 328, 22, 46, "placage"),
          B(242.25, 280.75, 254.25, 327.25, 45.25, 46, "placage"), B(242.25, 280.75, 254.25, 327.25, 22, 22.75, "placage"),
          B(242.25, 280.75, 243, 327.25, 22.75, 45.25, "placage"),
          B(243, 296.1, 253.6, 296.85, 22.75, 45.25, "placage"), B(243, 311.9, 253.6, 312.65, 22.75, 45.25, "placage"),
          B(243, 280.75, 253.6, 327.25, 33.6, 34.35, "placage"),
          B(242.25, 280, 243.25, 328, 18, 22, "carbone"),                                               # rail (tasseau français)
          A(254.25, 284, 274.25, 324, 22, 22.75, "placage", r=1.5, b=0.3)]
    M += [T([(253.9, y, 33.5), (266, y, 22.9)], 0.16, "metal") for y in (284.7, 323.3)]
    M += [B(244, 282, 252.5, 295, 22.75, 24.6, "blanc"), B(244, 282.5, 252, 294.5, 24.6, 25.4, "osier"),
          C(247.5, 304, 1.8, 22.75, 27, "art-argile"), C(250.5, 304, 1.6, 22.75, 26.5, "laque-marine")]
    M += [C(247.5 + dx, 304 + dy, 0.2, 27, 30.5, c) for dx, dy, c in ((-0.6, 0.3, "osier"), (0.5, -0.4, "rouge-velo"), (0.1, 0.6, "laque-marine"))]
    M += [B(244, 313.5, 252.5, 326, 34.35, 36, "draps"), B(244, 313.5, 252.5, 326, 36, 36.6, "art-sable")]
    # sur le pupitre : un dessin en cours et des crayons
    M += [B(259, 297, 270, 305.5, 22.75, 22.85, "blanc"), B(262, 299, 266, 300, 22.85, 22.9, "art-argile"),
          B(261, 302, 268, 302.6, 22.85, 22.9, "laque-marine"), CY(259.4, 308, 312.5, 23.05, 0.2, "art-argile", pans=8),
          CY(260.2, 308.5, 313, 23.05, 0.2, "laque-marine", pans=8), CY(261, 308, 312.5, 23.05, 0.2, "osier", pans=8)]
    # panneau perforé de chêne (y 280-328, z 46-72) : trous, tablette à pots, bobines, règle
    M += [B(242.25, 280, 243.25, 328, 46, 72, "placage")]
    M += [B(243.25, 281.5 + 3 * i - 0.22, 243.3, 281.5 + 3 * i + 0.22, 47.5 + 3 * j - 0.22, 47.5 + 3 * j + 0.22, "carbone")
          for i in range(16) for j in range(9)]
    M += [B(243.25, 300, 247.6, 318, 57.6, 58.3, "placage")]
    for y, c in ((303.5, "art-argile"), (309, "laque-marine"), (314.5, "osier")):
        M += [C(245.4, y, 1.6, 58.3, 62.4, c, pans=24)]
        M += [C(245.4 + dx, y + dy, 0.18, 62, 65.6, cc, pans=8) for dx, dy, cc in ((-0.5, 0.4, "rouge-velo"), (0.4, -0.3, "osier"), (0.2, 0.6, "laque-marine"))]
    M += [CX(243.25, 247, 287, 64, 0.22, "metal"), CX(244.6, 246.8, 287, 64, 1.5, "art-argile", pans=20),
          CX(243.25, 247, 292.5, 64, 0.22, "metal"), CX(244.6, 246.8, 292.5, 64, 1.5, "laque-marine", pans=20),
          B(243.3, 321, 243.6, 322.6, 50, 66, "osier")]
    # armoires hautes (z 72-96, 3 portes, adulte) et DEL dessous
    M += [A(242.25, 265 + 21 * k + 0.08, 254.25, 265 + 21 * (k + 1) - 0.08, 72, 96, BLANC, r=0.25, b=0.25) for k in range(3)]
    M += [B(252.8, 266, 253.6, 327, 71.5, 72, "spot")]
    # tabouret rond (glisse sous le pupitre)
    M += [C(277, 304, 6.5, 11.8, 13, "placage", pans=40)]
    M += [T([(277 + 4.6 * a, 304 + 4.6 * b, 11.8), (277 + 6.3 * a, 304 + 6.3 * b, 0)], 0.5, "placage")
          for a, b in ((1, 0), (-0.5, 0.866), (-0.5, -0.866))]

    # ------------------------------------------------------------------ tapis de jeu 5' × 8' et jouets
    M += [A(258, 254, 316, 350, 0, 0.5, "tapis", r=2, b=0.2)]
    M += [B(262, 258, 312, 259, 0.5, 0.56, "osier"), B(262, 345, 312, 346, 0.5, 0.56, "osier"),
          B(262, 258, 263, 346, 0.5, 0.56, "osier"), B(311, 258, 312, 346, 0.5, 0.56, "osier")]
    M += [TOR(296, 318, 0.8, 13, 0.45, "placage", axe="z"), TOR(296, 318, 0.8, 11.2, 0.45, "placage", axe="z")]
    M += [A(307.6, 313, 310.4, 318.5, 0.5, 3.6, "art-argile", r=0.4, b=0.3), A(307.6, 319.3, 310.4, 324.3, 0.5, 3, "laque-marine", r=0.4, b=0.3),
          C(309, 315, 0.5, 3.6, 5, "carbone")]
    M += [B(283, 289, 286, 292, 0.5, 3.5, "placage"), B(283.4, 289.4, 286.4, 292.4, 3.5, 6.5, "art-argile"),
          B(283, 289, 286, 292, 6.5, 9.5, "laque-marine"), B(287.5, 290, 293.5, 293, 0.5, 3.5, "osier")]
    M += [SPH(300, 272, 4, 4, "rouge-velo")]

    # ------------------------------------------------------------------ WALK-IN (ancien caveau) : fini 83 × 47½, plafond 84
    M += [B(229, 380, 231.5, 430, 0, 84, "art-sauge"), B(314.5, 380, 317, 430, 0, 84, "art-sauge"),
          B(231.5, 427.5, 314.5, 430, 0, 84, "art-sauge"), B(229, 380, 317, 430, 84, 96, "plafond")]
    # miroir pleine hauteur au dos de la porte (vu du walk-in), cadre noir mince. Rendu « inox » (satiné) : la visite 3D
    # capture le reflet d'un miroir placé au nord de y = 190 du côté sud (la chambre) ; ici il regarde le walk-in.
    M += [B(247, 375.95, 275, 376.3, 8, 76, "inox"), B(246.6, 375.9, 247, 376.4, 7.6, 76.4, "metal"),
          B(275, 375.9, 275.4, 376.4, 7.6, 76.4, "metal"), B(246.6, 375.9, 275.4, 376.4, 7.6, 8, "metal"),
          B(246.6, 375.9, 275.4, 376.4, 76, 76.4, "metal")]
    # penderie double sur crémaillères noires (x 233, 260, 287, 313), tringles z 34 (lui) et z 70 (plus tard)
    for x in (233, 260, 287, 313):
        M += [B(x - 0.5, 426.9, x + 0.5, 427.5, 2, 82, "metal")]
        M += [B(x - 0.3, 416, x + 0.3, 426.9, z - 0.5, z + 1, "metal") for z in (34, 70)]
        M += [B(x - 0.3, 411, x + 0.3, 426.9, 72.6, 74, "metal")]
    M += [CX(231.5, 314.5, 416.5, 34, 0.55, "metal"), CX(231.5, 314.5, 416.5, 70, 0.55, "metal"),
          A(231.5, 410, 314.5, 427.5, 74, 75, "placage", r=0.3, b=0.3), B(232, 410.3, 314, 410.9, 73.6, 74, "spot")]
    for k in range(6):
        x0 = 232.5 + 13.75 * k
        M += [A(x0, 413, x0 + 12.5, 427, 75, 82.5, ["osier", "tapis", "art-sable", "osier", "tapis", "art-sable"][k], r=1, b=0.5),
              B(x0 + 4, 412.8, x0 + 8.5, 413, 78, 80.5, "blanc"), B(x0 + 4.6, 412.7, x0 + 7.9, 412.8, 78.5, 80, COUL_VET[k])]
    rng = random.Random(3)

    def vetement(x, ep, zb, zt, larg, mat):
        """Vêtement d'enfant sur cintre de bois (crochet noir sur la tringle à zt + 1.6)."""
        xc, y0, y1 = x + ep / 2, 416.5 - larg / 2, 416.5 + larg / 2
        return [A(x, y0, x + ep, y1, zb, zt - 0.6, mat, r=0.3, b=0.25),
                A(x, y0 + 1.2, x + ep, y1 - 1.2, zt - 0.6, zt, mat, r=0.3, b=0.25),          # épaules
                B(xc - 0.2, y0 + 0.8, xc + 0.2, y1 - 0.8, zt, zt + 0.5, "placage"),             # cintre
                T([(xc, 416.5, zt + 0.5), (xc, 416.5, zt + 1.3), (xc, 417.1, zt + 2.0)], 0.1, "metal")]
    x, k = 233.5, 0
    while x < 294:                                                                                      # SES vêtements (bas)
        ep = rng.uniform(0.9, 1.6)
        M += vetement(x, ep, rng.uniform(16, 22), 32, rng.uniform(12, 14), COUL_VET[k % len(COUL_VET)])
        x += ep + rng.uniform(0.5, 1.4)
        k += 1
    x = 236
    while x < 286:                                                                                      # grandeur suivante (haut)
        ep = rng.uniform(1.0, 1.8)
        M += vetement(x, ep, rng.uniform(44, 52), 68, rng.uniform(14, 16), COUL_VET[(k * 3) % len(COUL_VET)])
        x += ep + rng.uniform(2, 4.5)
        k += 1
    # banc à souliers (x 231½-245½, y 380-405½, assise 17) et crochets ronds sur le mur x = 231½
    M += [B(231.5, 380, 245.5, 380.75, 0, 15, "placage"), B(231.5, 404.75, 245.5, 405.5, 0, 15, "placage"),
          B(231.5, 392.4, 245.5, 393.1, 0, 15, "placage"), B(231.5, 380.75, 232.25, 404.75, 0, 15, "placage"),
          B(232.25, 380.75, 245.5, 404.75, 0, 1, "placage"), B(232.25, 380.75, 245.5, 404.75, 7, 7.75, "placage"),
          A(231.5, 380, 245.5, 405.5, 14.25, 15.25, "placage", r=0.4, b=0.25), A(232, 380.5, 245.3, 405, 15.25, 17, "tissu", r=1.2, b=0.8)]
    for ya, z, c in ((381.5, 1, "laque-marine"), (394, 1, "art-argile"), (381.5, 7.75, "carbone"), (394, 7.75, "tissu")):
        M += [A(233.5, ya, 244.5, ya + 4.6, z, z + 3.6, c, r=1.6, b=0.9), A(233.5, ya + 5.2, 244.5, ya + 9.8, z, z + 3.6, c, r=1.6, b=0.9)]
    for z in (32, 54):
        for y in (385, 392.75, 400.5):
            M += [CX(231.5, 233.2, y, z, 0.4, "placage"), SPH(233.4, y, z, 0.95, "placage")]
    M += [SPH(234.2, 400.5, 30, 2.8, "laque-marine", ecrase=0.8), SPH(234.2, 400.5, 32.2, 0.8, "draps"),
          A(231.7, 381.6, 235.6, 388.6, 37, 54.5, "art-argile", r=2, b=1.5)]                         # tuque, imperméable
    # tour de tiroirs (x 296½-314½, y 380-405½) : panier à linge, 3 tiroirs, dessus à 36, valet, tablettes 52/66/80
    M += [B(296.5, 380, 314.5, 380.75, 0, 84, "placage"), B(296.5, 404.75, 314.5, 405.5, 0, 84, "placage"),
          B(313.75, 380.75, 314.5, 404.75, 0, 84, "placage"), B(298.5, 380.75, 313.75, 404.75, 0, 1, "carbone"),
          B(297, 380.75, 313.75, 404.75, 1, 35.25, "placage"), A(296.5, 380, 314.5, 405.5, 35.25, 36, "placage", r=0.3, b=0.2)]
    for z0, z1 in ((1.2, 13.2), (13.6, 20.6), (21, 28), (28.4, 35.1)):
        zc = (z0 + z1) / 2 + (2.5 if z1 < 14 else 0)
        M += [A(296.3, 380.9, 297.1, 404.6, z0, z1, "placage", r=0.3, b=0.2),
              A(295.9, 389.7, 296.4, 395.8, zc - 0.5, zc + 0.5, "carbone", r=0.4, b=0.1)]
    M += [B(297, 380.75, 313.75, 404.75, z, z + 0.75, "placage") for z in (52, 66, 80)] + [B(297, 380.75, 313.75, 404.75, 83.25, 84, "placage")]
    M += [CX(295.6, 297, 392.75, 47, 0.35, "metal"), SPH(295.6, 392.75, 47, 0.6, "metal")]           # valet escamotable (rentré)
    for z, mats in ((52.75, ("laque-marine", "art-sable", "draps")), (66.75, ("tissu", "art-argile", "osier")), (80.75, ("cuir",))):
        y = 382
        for m in mats:
            hh = 2.2 if z > 80 else 2.6
            M += [A(299, y, 312.5, y + 6.8, z, z + hh, m, r=0.8, b=0.5), A(299.3, y + 0.2, 312.2, y + 6.6, z + hh, z + 2 * hh, m, r=0.8, b=0.5)]
            y += 7.4
    M += [B(297.5, 382, 312, 393, 36, 36.6, "tapis"), A(298, 395, 305, 402, 36, 38.5, "laque-marine", r=1, b=0.6)]
    # panneau rayonnant au plafond, plafonnier DEL à détecteur, détecteur de mouvement
    M += [B(256, 383, 288, 403, 83.2, 84, "blanc"), B(256.6, 383.6, 287.4, 402.4, 83.1, 83.2, "gris"),
          C(272, 408.6, 3.4, 83.3, 84, "spot", pans=32), C(272, 408.6, 3.8, 83.6, 84, "metal", pans=32),
          B(239.8, 380, 241.8, 380.6, 46, 49, "blanc")]

    S["mobilier"] += M

    # ------------------------------------------------------------------ lumières, visites, palette
    S["lumieres"][:] = [l for l in S["lumieres"] if not (_dans((l["x"], l["y"]), CH2) or _dans((l["x"], l["y"]), WI))]
    S["lumieres"] += [{"x": 300, "y": 300}, {"x": 362, "y": 300}, {"x": 400, "y": 262}, {"x": 432, "y": 316, "i": 6},
                      {"x": 272, "y": 398, "z": 90, "i": 4}]
    vis = S["visites"]
    i = next((k for k, v in enumerate(vis) if v.get("nom") == "Chambre 2"), len(vis))
    vis[:] = [v for v in vis if v.get("nom") not in ("Chambre 2", "Walk-in (caveau isolé)")]
    vis[i:i] = [{"nom": "Chambre 2 — la bibliothèque secrète", "x": 268, "y": 250, "cap": 62},
                {"nom": "Chambre 2 — lit queen et mur de tête", "x": 355, "y": 258, "cap": 90},
                {"nom": "Chambre 2 — banc-cabane et tour à trésors", "x": 300, "y": 300, "cap": 5},
                {"nom": "Chambre 2 — mur d'activité (bureau à rabat)", "x": 330, "y": 268, "cap": 160},
                {"nom": "Walk-in — penderie qui grandit", "x": 261, "y": 378, "cap": 90}]
    for p in S.get("palette", []):
        if p[0] == "Chambres" and "chambre 2" in p[1]:
            p[1] = p[1].split("; chambre 2")[0].rstrip(" ;")
    S.setdefault("palette", []).append(
        ["Chambre 2 « bibliothèque secrète »", "murs sauge ; mur de tête intégré en chêne blanc (porte-bibliothèque pivotante "
         "vers le walk-in, tours, niches éclairées, alcôve de lattes, lit queen sur plateforme à tiroirs), armoires hautes "
         "blanc chaud mat, quincaillerie noir mat ; banc-cabane sous la fenêtre, garage à jouets, mur d'activité ; walk-in "
         "sur crémaillères noires", "#C9A97A"])
