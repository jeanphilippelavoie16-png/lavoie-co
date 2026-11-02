"""MAISON-18 — zone CHAMBRE 2 (le grand, 6 ans) et son WALK-IN (ancien caveau) : « La bibliothèque secrète », allégée.

Demande du client (2026-11-01) : « Dans les chambres en bas il y a comme trop de meubles, exagère pas. » Le rangement
principal de la chambre 2 est le WALK-IN (vêtements, souliers, tiroirs) : la chambre elle-même garde peu de pièces et
beaucoup de plancher.
- PORTE-BIBLIOTHÈQUE SECRÈTE (x 245-277) qui pivote vers le walk-in, imposte-bibliothèque au-dessus : gardée telle quelle
  (le « wow » du client) ; elle est seule dans son coin, au bout de l'axe de la porte d'entrée.
- LIT QUEEN SUR PLATEFORME à 4 tiroirs (2 par côté), tête contre le mur arrière, devant un panneau de lattes de chêne sur
  feutre noir (106 po, 60 po de haut) qui porte 2 chevets flottants à tiroir et 2 liseuses DEL.
- BANC DE FENÊTRE sous la fenêtre est (24 po de profond, assise 18, 3 tiroirs ; celui du centre s'enlève : trappe
  d'accès au drain) ; c'est aussi la marche d'évacuation.
- PUPITRE À RABAT mural (36 po, rabat à 23 po) sur le mur du vestiaire, hors des battants de porte, et un tabouret.
- COIN JEU AU SOL : tapis rond de 64 po entre la porte, le pupitre et le lit, gardé hors du balayage des deux portes.
Retirés de la version SS-17 : tour gauche et pont d'armoires hautes du mur de tête, chevets-niches, tour d'angle à
trésors (vitrine LEGO), garage à jouets avec rebords à livres et galerie, mur d'activité (crochets, cases, panneau
perforé, armoires hautes), bacs-wagons du pied du lit, rail-rideau (déjà retiré) et la plupart des bibelots.
Walk-in : isolé (fini 83 × 47½, plafond supposé à 84), penderie double sur crémaillères, banc à souliers, tour de
tiroirs, miroir au dos de la porte-bibliothèque, panneau rayonnant au plafond (inchangé).

Pièce réelle : x 242¼-446, y 232¼-370 ; walk-in brut x 229-317, y 380-430. Pouces, repère de la maison.
Battants à garder libres : porte de la chambre (ouv-SS-P06, pentures à l'ouest : x 245-277, y 232¼-264¼) et
porte-bibliothèque (pivots à l'ouest : x 245-277, y 338-370) — rien au sol, pas même le tapis.
"""
import random

# --------------------------------------------------------------------------------------------- emprises de la zone
CH2 = (242.0, 232.0, 447.0, 371.0)          # chambre 2 (x0, y0, x1, y1)
WI = (228.0, 379.0, 318.0, 431.0)           # walk-in (ancien caveau)

COUL_LIVRES = ["laque-marine", "art-argile", "draps", "carbone", "osier", "art-sable", "tissu", "cuir", "blanc",
               "laque-marine", "art-argile", "osier"]
COUL_VET = ["laque-marine", "draps", "art-argile", "tissu", "osier", "carbone", "art-sable", "cuir", "blanc"]


# ============================================================================================ PLAN (modifs.py)
def appliquer_modifs(L, base):
    """Plan : la commode SS-16 de la chambre 2 disparaît ; meubles intégrés (rectangles du plan)."""
    L["EQUIPEMENTS"][:] = [e for e in L["EQUIPEMENTS"] if e[0] != "elem-SS-P-COMMODE2"]
    L["EQUIPEMENTS"] += [
        ("elem-SS-P-CH2-LIT", "autre", "Lit-plateforme queen : socle de chêne à 4 tiroirs, matelas 60 × 80 (dessus à 22 po)",
         "LIT QUEEN", 355, 325, 0, (66, 84)),
        ("elem-SS-P-CH2-PB", "autre", "Porte-bibliothèque secrète (pivots, livre-levier, miroir au dos) devant la baie du "
         "walk-in ; imposte-bibliothèque fixe au-dessus", "", 260.125, 366, 0, (35.75, 8)),
        ("elem-SS-P-CH2-LATTES", "autre", "Tête de lit : panneau de lattes de chêne sur feutre (106 × 60 po), 2 liseuses DEL",
         "", 355, 368.75, 0, (106, 2.5)),
        ("elem-SS-P-CH2-NG", "comptoir", "Chevet flottant gauche à tiroir (dessus à 24 po)", "", 312, 362, 0, (16, 12)),
        ("elem-SS-P-CH2-ND", "comptoir", "Chevet flottant droit à tiroir (dessus à 24 po)", "", 398, 362, 0, (16, 12)),
        ("elem-SS-P-CH2-BANC", "comptoir", "Banc de fenêtre (assise 18 po, 3 tiroirs ; celui du centre s'enlève : trappe "
         "d'accès au drain) ; marche d'évacuation", "", 434, 316, 0, (24, 108)),
        ("elem-SS-P-CH2-PUPITRE", "armoires", "Pupitre à rabat mural (36 po, rabat à 23 po, 9 po fermé) et tabouret",
         "", 300, 236.75, 0, (36, 9)),
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
        if p["id"] == "piece-SS-CH2":
            p["description"] = ("Chambre 2 (enfant de 6 ans), allégée : porte-bibliothèque secrète vers le walk-in, lit queen sur "
                                "plateforme à tiroirs devant un panneau de lattes, banc de fenêtre, pupitre à rabat, coin jeu "
                                "au sol — proposition MAISON-18 (esquisse)")
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


def appliquer_scene(S, h):
    B, A, C, CY, CX, T, SPH = h.B, h.A, h.C, h.CY, h.CX, h.T, h.SPH
    S["mobilier"][:] = [o for o in S["mobilier"] if not _ma_zone(o)]
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

    # ------------------------------------------------------------------ tête de lit : lattes de chêne sur feutre noir
    # Panneau de 106 po (x 302-408) × 60 po, lattes de 1 po aux 2 po, chapeau de chêne ; 2 liseuses DEL encastrées.
    TX0, TX1, TZ = 302.0, 408.0, 60.0
    M += [B(TX0, 369.4, TX1, 370, 0, TZ, "pneu")]
    M += [B(TX0 + 0.5 + 2 * k, 367.9, TX0 + 1.5 + 2 * k, 369.4, 0, TZ, "placage") for k in range(53)]
    M += [A(TX0, 367.3, TX1, 370, TZ, TZ + 1.25, "placage", r=0.4, b=0.3)]
    for xl in (333, 377):
        M += [CY(xl, 367.5, 367.9, 39, 1.6, "carbone", pans=32), CY(xl, 367.35, 367.5, 39, 1.1, "spot", pans=32)]
    # 2 chevets flottants (16 × 12, z 16-24) accrochés au panneau, un tiroir chacun
    for x0, x1 in ((304.0, 320.0), (390.0, 406.0)):
        xc = (x0 + x1) / 2
        M += [A(x0, 356, x1, 367.9, 16, 24, "placage", r=0.5, b=0.3),
              B(x0 + 0.6, 355.9, x1 - 0.6, 356.0, 16.6, 16.75, "carbone"),                              # joint du tiroir
              A(xc - 3, 355.8, xc + 3, 356.05, 21.6, 22.6, "carbone", r=0.4, b=0.1)]                    # poignée découpée
    M += [C(308.5, 362, 2.0, 24, 24.6, "carbone"), SPH(308.5, 362, 26.6, 2.2, "abat-jour"),             # veilleuse
          B(395, 359, 402.5, 365.5, 24, 24.8, "laque-marine"), B(395.4, 359.4, 402, 365, 24.8, 25.4, "art-sable")]  # 2 livres

    # ------------------------------------------------------------------ lit-plateforme queen (66 × 84, dessus 12), 4 tiroirs
    M += [B(325, 286, 385, 364, 0, 3, "carbone"),                                                       # socle en retrait
          A(322, 283, 388, 367, 3, 12, "placage", r=1, b=0.4)]
    for xs, xp in ((321.5, 321.2), (387.7, 388.4)):                                                     # 2 tiroirs par côté
        for ya, yb in ((306.5, 335.2), (336, 364.7)):
            yc = (ya + yb) / 2
            M += [A(xs, ya, xs + 0.8, yb, 3.8, 11.4, "placage", r=0.3, b=0.2),
                  A(xp, yc - 3, xp + 0.4, yc + 3, 9, 10.3, "carbone", r=0.4, b=0.1)]
    # matelas, couette, rabat, jeté, 2 oreillers, l'ourson
    M += [A(325, 285, 385, 365, 12, 22, "draps", r=3, b=2.5),
          A(324.4, 284.4, 385.6, 344, 20.8, 23.6, "tissu", r=2.5, b=1.2),                              # couette
          A(324.6, 338, 385.4, 346, 22.6, 24.4, "draps", r=2, b=1),                                     # rabat du drap
          A(324.2, 285.5, 385.8, 299, 23.4, 24.6, "laque-marine", r=1.5, b=0.6),                       # jeté au pied
          A(329, 345, 353, 362, 21, 27.5, "draps", r=4, b=3), A(357, 345, 381, 362, 21, 27.5, "draps", r=4, b=3),
          SPH(372, 342, 27.6, 3.4, "osier", ecrase=0.9), SPH(372, 343, 32.4, 2.5, "osier"),
          SPH(370.4, 343, 34.4, 0.9, "osier"), SPH(373.6, 343, 34.4, 0.9, "osier"), SPH(372, 340.7, 32, 0.8, "art-sable")]

    # ------------------------------------------------------------------ banc de fenêtre (x 422-446, y 262-370), 3 tiroirs
    M += [B(424, 264, 446, 368, 0, 3, "carbone"), A(422, 262, 446, 370, 3, 14, "placage", r=1, b=0.4)]
    for ya, yb in ((262.6, 297.6), (298.4, 333.6), (334.4, 369.4)):                                     # le tiroir du centre
        yc = (ya + yb) / 2                                                                              # s'enlève (drain)
        M += [A(421.4, ya, 422.2, yb, 3.6, 13.4, "placage", r=0.3, b=0.2),
              A(421.05, yc - 3.5, 421.5, yc + 3.5, 10.6, 11.8, "carbone", r=0.4, b=0.1)]
    M += [A(422.6, 262.6, 446, 369.4, 14, 18, "tissu", r=2, b=1.5)]                                    # coussin attaché
    M += [A(439.6, ya, 445.9, yb, 18, 32, "tapis", r=2.6, b=2) for ya, yb in ((263.5, 315.5), (316.5, 369.2))]  # dossiers
    M += [A(433, 350, 439.5, 364, 18, 29, "laque-marine", r=3, b=2.5)]                                  # un coussin d'accent
    yl = 366.5                                                                                          # une liseuse + USB
    M += [B(445.2, yl - 1.4, 446, yl + 1.4, 40.5, 46.5, "metal"), CX(441.6, 445.2, yl, 44.5, 0.3, "metal"),
          C(441.2, yl, 1.7, 41.8, 44.8, "metal", pans=24), C(441.2, yl, 1.3, 41.6, 41.8, "spot", pans=24),
          B(445.6, yl - 0.6, 445.9, yl + 0.6, 41, 42.2, "blanc")]
    # (rail-rideau au plafond retiré à la demande du client, 2026-11-01)

    # ------------------------------------------------------------------ pupitre à rabat (mur du vestiaire, x 282-318)
    # Caisson de chêne 36 × 9 × 20 po (z 23-43) ancré aux montants ; rabat ouvert = surface de 34 × 19 à 23¾ po,
    # 2 compas amortis ; 2 cases dedans (papier, crayons), DEL sous le dessus. Fermé : une boîte de chêne au mur.
    PX0, PX1, PY0, PY1 = 282.0, 318.0, 232.25, 241.25
    M += [B(PX0, PY0, PX0 + 0.75, PY1, 23, 43, "placage"), B(PX1 - 0.75, PY0, PX1, PY1, 23, 43, "placage"),
          A(PX0, PY0, PX1, PY1, 42.25, 43, "placage", r=0.3, b=0.2), B(PX0, PY0, PX1, PY1, 23, 23.75, "placage"),
          B(PX0 + 0.75, PY0, PX1 - 0.75, PY0 + 0.75, 23.75, 42.25, "placage"),
          B(299.6, PY0 + 0.75, 300.4, PY1 - 0.5, 23.75, 42.25, "placage"),
          B(300.4, PY0 + 0.75, PX1 - 0.75, PY1 - 0.5, 33, 33.75, "placage"),
          B(PX0 + 1, PY1 - 1.2, PX1 - 1, PY1 - 0.7, 41.75, 42.25, "spot"),
          A(PX0 + 1, PY1, PX1 - 1, PY1 + 19, 23, 23.75, "placage", r=1, b=0.3)]                          # rabat ouvert
    M += [T([(x, PY1 - 1, 33), (x, PY1 + 10, 23.9)], 0.16, "metal") for x in (PX0 + 1.2, PX1 - 1.2)]
    M += [B(284, 234, 298, 240.5, 23.75, 25.6, "blanc"), B(284.3, 234.2, 297.7, 240.3, 25.6, 26.0, "art-sable"),
          C(306, 237, 1.8, 33.75, 38, "art-argile", pans=24)]
    M += [C(306 + dx, 237 + dy, 0.18, 37, 41, cc, pans=8) for dx, dy, cc in ((-0.5, 0.4, "rouge-velo"), (0.4, -0.3, "osier"),
                                                                          (0.2, 0.6, "laque-marine"))]
    M += [B(294, 248, 305, 256.5, 23.75, 23.85, "blanc"), B(297, 250, 301, 251, 23.85, 23.9, "art-argile"),   # un dessin
          B(296, 253, 303, 253.6, 23.85, 23.9, "laque-marine"), CY(307, 249, 253.5, 24.0, 0.2, "art-argile", pans=8)]
    # tabouret rond (12 po)
    M += [C(300, 270, 6.5, 11.8, 13, "placage", pans=40)]
    M += [T([(300 + 4.6 * a, 270 + 4.6 * b, 11.8), (300 + 6.3 * a, 270 + 6.3 * b, 0)], 0.5, "placage")
          for a, b in ((1, 0), (-0.5, 0.866), (-0.5, -0.866))]

    # ------------------------------------------------------------------ coin jeu au sol : tapis rond (64 po) et un train de bois
    # Centre (287, 303), r 32 : hors du balayage de la porte (y ≤ 264¼) et de la porte-bibliothèque (y ≥ 338 à x ≤ 277).
    M += [C(287, 303, 32, 0, 0.45, "osier", pans=72), C(287, 303, 30.6, 0, 0.5, "tapis", pans=72)]
    M += [A(272, 304, 278, 308.5, 0.9, 4.6, "laque-marine", r=0.6, b=0.4), C(273.6, 306.25, 0.8, 4.6, 6.2, "carbone", pans=12),
          A(279, 304.2, 284.5, 308.3, 0.9, 3.4, "art-argile", r=0.6, b=0.4), A(285.5, 304.2, 291, 308.3, 0.9, 3.4, "placage", r=0.6, b=0.4)]
    M += [CY(x, 303.8, 308.7, 1.0, 0.75, "carbone", pans=12) for x in (273.5, 276.5, 280.5, 283, 287, 289.5)]

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
    S["lumieres"] += [{"x": 290, "y": 300}, {"x": 362, "y": 300}, {"x": 404, "y": 262}, {"x": 434, "y": 316, "i": 6},
                      {"x": 272, "y": 398, "z": 90, "i": 4}]
    vis = S["visites"]
    i = next((k for k, v in enumerate(vis) if v.get("nom") == "Chambre 2"), len(vis))
    vis[:] = [v for v in vis if v.get("nom") not in ("Chambre 2", "Walk-in (caveau isolé)")]
    vis[i:i] = [{"nom": "Chambre 2 — vue d'entrée (la bibliothèque au bout)", "x": 264, "y": 244, "cap": 76},
                {"nom": "Chambre 2 — lit queen et tête de lattes", "x": 355, "y": 256, "cap": 90},
                {"nom": "Chambre 2 — banc de fenêtre", "x": 334, "y": 262, "cap": 26},
                {"nom": "Chambre 2 — coin jeu et pupitre", "x": 262, "y": 346, "cap": 292},
                {"nom": "Walk-in — penderie qui grandit", "x": 261, "y": 378, "cap": 90}]
    for p in S.get("palette", []):
        if p[0] == "Chambres" and "chambre 2" in p[1]:
            p[1] = p[1].split("; chambre 2")[0].rstrip(" ;")
    S.setdefault("palette", []).append(
        ["Chambre 2 « bibliothèque secrète »", "allégée, murs sauge : porte-bibliothèque secrète en chêne blanc qui pivote "
         "vers le walk-in (le vrai rangement : penderie qui grandit sur crémaillères noires, souliers, tiroirs) ; lit queen sur "
         "plateforme à 4 tiroirs devant un panneau de lattes de chêne sur feutre noir avec 2 chevets flottants ; banc de "
         "fenêtre à 3 tiroirs ; pupitre à rabat ; tapis rond de laine pour jouer au sol ; quincaillerie noir mat", "#C9A97A"])
