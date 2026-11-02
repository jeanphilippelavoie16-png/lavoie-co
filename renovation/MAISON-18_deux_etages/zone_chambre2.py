"""MAISON-18 — zone CHAMBRE 2 (le grand, 6 ans) et son WALK-IN (ancien caveau) : « Le mur de chêne ».

Demande du client (2026-11-02) : « Les chambres des enfants en bas, j'aime pas super ça, faut les refaire. » Après le
rangement « wow » (SS-17), le lit queen, puis « exagère pas » et une version allégée qui ne lui plaît pas non plus : une
vraie direction de design. Une chambre de grand garçon chic, calme et chaleureuse, qui tiendra jusqu'à l'adolescence.
Peu de pièces, belles, des surfaces planes ; chêne, noir mat, travertin, béton poli, blanc chaud ; UNE seule couleur
d'accent : le marine (Hale Navy, déjà celui des armoires du lavage), à trois endroits seulement.

- MUR DE CHÊNE pleine largeur et pleine hauteur (mur arrière, x 242¼-446) : planches de chêne blanc de 16½ po, joints
  creux noirs de ¼ po, ligne horizontale à 82 po (hauteur de la porte), socle noir en retrait. La PORTE DÉROBÉE du
  walk-in est une planche double de ce mur (x 244½-277½) qui pivote vers la chambre (pivots invisibles côté ouest,
  loquet poussoir, aucun verrou) : elle remplace la porte-bibliothèque (des dizaines de petits livres sur un mur qu'on
  veut calme) ; le secret reste. Dans la 3D, on clique sur le mur et il s'ouvre.
- LIT QUEEN sur plateforme de chêne à 4 tiroirs (2 par côté, vers le pied, hors des chevets), socle noir en retrait,
  centré sur le mur ; TÊTE REMBOURRÉE marine de 66 × 30 po alignée sur deux joints ; 2 LISEUSES murales noires à bras
  pivotant ; 2 CHEVETS en blocs de travertin adouci.
- BUREAU à hauteur réglable (plateau de chêne 54 × 24, piètement électrique noir, de 22 à 30 po : de 6 à 16 ans) au
  nord de la fenêtre, une tablette de chêne au-dessus, une lampe d'architecte noire, une chaise pivotante.
- COIN LECTURE au sud de la fenêtre : fauteuil bas marine, liseuse sur pied noire ; le chevet de travertin sert de table.
- GRAND TAPIS de laine 8 × 10 pi (avoine) sous les deux tiers du lit ; LANTERNE de papier washi Ø 28 po au-dessus du lit.
- WALK-IN peint marine (le rangement principal) : penderie à deux hauteurs (tringles noires à 40 et 78 po) sur 54½ po,
  colonne de chêne à 4 tiroirs et 3 tablettes éclairées, banc à souliers, crochets, miroir au dos de la porte dérobée,
  DEL linéaire au plafond, panneau rayonnant.
Fenêtre d'évacuation (mur est, y 268-348) : rien de plus haut que 31 po devant (son allège sera abaissée à ≈ 40 po par
un autre module) ; 54 po de large et 44 po de profond libres devant. Lit : 28 po et plus de chaque côté, 48 po au pied.

Pièce réelle : x 242¼-446, y 232¼-370 ; walk-in brut x 229-317, y 380-430 (fini 83 × 47½, plafond supposé à 84).
Battants libres : porte de la chambre (ouv-SS-P06, x 246-278, y 232¼-264¼) et porte dérobée (x 244½-278, y 334-367½).
"""
import math
import random

# --------------------------------------------------------------------------------------------- emprises de la zone
CH2 = (242.0, 232.0, 447.0, 371.0)          # chambre 2 (x0, y0, x1, y1)
WI = (228.0, 379.0, 318.0, 431.0)           # walk-in (ancien caveau)

YF, YB = 367.5, 369.3                       # face du mur de chêne ; devant du fond noir (cache plinthe et chambranles)
XP0, XP1 = 244.5, 277.5                     # porte dérobée (planche double) devant la baie x 246-276
PAS, JOINT, ZL = 16.5, 0.25, 82.0           # largeur des planches, joint creux, ligne horizontale (tête de la porte)
LIT = (311.5, 281.0, 375.5, 365.0)          # plateforme 64 × 84, centrée sur le mur (x 343,5)
NAVY = "laque-marine"                       # alias de la peinture « Marine » (Hale Navy) : la seule couleur d'accent
COUL_LIVRES = ["draps", "tapis", "carbone", "osier", "blanc", "tissu", "draps", "carbone", NAVY, "tapis"]
COUL_VET = ["draps", "tissu", "carbone", "tapis", "blanc", "osier", NAVY, "draps", "tissu"]

# ============================================================================================ PLAN (modifs.py)
ELEMENTS = [  # id, type, nom, libellé, x, y, rotation, (longueur, largeur)
    ("elem-SS-P-CH2-MUR", "autre", "Mur de tête pleine largeur : planches de chêne blanc de 16½ po à joints creux noirs, "
     "plancher au plafond ; la porte dérobée du walk-in en fait partie (à l'ouest)", "", 361.75, 368.75, 0, (168.5, 2.5)),
    ("elem-SS-P-CH2-LIT", "autre", "Lit-plateforme queen de chêne à 4 tiroirs (matelas 60 × 80, dessus à 22½ po), tête "
     "rembourrée marine 66 × 30 po, 2 liseuses murales noires", "LIT QUEEN", 343.5, 323.0, 0, (64, 84)),
    ("elem-SS-P-CH2-NG", "autre", "Chevet : bloc de travertin adouci 18 × 15 po, dessus à 21 po", "", 298.0, 359.5, 0, (18, 15)),
    ("elem-SS-P-CH2-ND", "autre", "Chevet : bloc de travertin adouci 18 × 15 po, dessus à 21 po", "", 389.0, 359.5, 0, (18, 15)),
    ("elem-SS-P-CH2-BUREAU", "autre", "Bureau à hauteur réglable 54 × 24 po (plateau de chêne, piètement électrique noir, "
     "22 à 30 po), tablette de chêne au-dessus", "BUREAU", 418.0, 244.75, 0, (54, 24)),
    ("elem-SS-P-CH2-FAUTEUIL", "autre", "Coin lecture : fauteuil bas marine 30 × 30 po et liseuse sur pied noire", "",
     419.0, 351.0, 0, (30, 30)),
    ("elem-SS-P-WI-PENDERIE", "autre", "Walk-in : penderie à deux hauteurs (tringles noires à 40 et 78 po), DEL linéaire "
     "au plafond", "", 258.75, 416.5, 0, (54.5, 22)),
    ("elem-SS-P-WI-TOUR", "armoires", "Walk-in : colonne de chêne, 4 tiroirs (dessus-valet à 36¾ po) et 3 tablettes "
     "éclairées", None, 300.75, 416.5, 0, (27.5, 22)),
    ("elem-SS-P-WI-BANC", "comptoir", "Walk-in : banc à souliers (assise à 16 po) et crochets noirs", None, 307.5, 393.0, 0, (14, 24)),
]


def appliquer_modifs(L, base):
    """Plan : la commode SS-16 de la chambre 2 disparaît ; mobilier de la proposition (rectangles du plan)."""
    ids = {e[0] for e in ELEMENTS}
    L["EQUIPEMENTS"][:] = [e for e in L["EQUIPEMENTS"] if e[0] != "elem-SS-P-COMMODE2" and e[0] not in ids] + ELEMENTS


def apres_modifs(maison, base):
    """La porte du caveau (ouv-SS-008) devient la porte dérobée du mur de chêne : même baie, même sens (vers la chambre).
    « fermee » : dans la 3D, le battant est dessiné fermé et les planches de chêne de la porte pivotent avec lui."""
    ss = next(n for n in maison["niveaux"] if n["id"] == "SS")
    for o in ss["ouvertures"]:
        if o["id"] == "ouv-SS-008":
            o["fermee"] = True
            o["interieure"] = True
            o["sens"] = dict(o.get("sens") or {}, charniere="fin", ouvre_vers="gauche",
                             note="porte dérobée affleurante dans le mur de chêne (pivots invisibles côté ouest, loquet "
                                  "poussoir), ouvre vers la chambre ; s'ouvre en poussant depuis le walk-in, aucun verrou ; "
                                  "miroir au dos — proposition MAISON-18 (esquisse)")
            o["note"] = ((o.get("note") or "") + " MAISON-18 : la porte devient une porte dérobée de chêne (33 × 81 po) "
                         "intégrée au mur de tête, côté chambre 2.")
    for p in ss["pieces"]:
        if p["id"] == "piece-SS-CH2":
            p["description"] = ("Chambre 2 (garçon de 6 ans, jusqu'à l'adolescence) « le mur de chêne » : mur de tête "
                                "pleine largeur en chêne avec la porte dérobée du walk-in, lit queen sur plateforme à "
                                "tiroirs, tête rembourrée marine, bureau réglable, coin lecture à la fenêtre, grand tapis, "
                                "lanterne de papier — proposition MAISON-18 (esquisse)")
        if p["id"] == "piece-SS-LEG":
            p["description"] = ("Ancien caveau à légumes isolé (2 po rigide + gypse, fini 83 × 47½, plafond supposé à 84 : "
                                "À MESURER) : walk-in de la chambre 2, peint marine — penderie à deux hauteurs (tringles "
                                "à 40 et 78 po), colonne de chêne à tiroirs et tablettes éclairées, banc à souliers, "
                                "miroir au dos de la porte dérobée, DEL linéaire, panneau rayonnant — proposition "
                                "MAISON-18 (esquisse)")


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


def _livres(B, x0, x1, yd, z, seed):
    """Livres debout le long de x, dos vers +y (dos à y ≈ yd), posés à z."""
    rng = random.Random(seed)
    out, x = [], x0
    while True:
        w = rng.uniform(0.7, 1.6)
        if x + w > x1:
            break
        hh, d = rng.uniform(7.5, 10.5), rng.uniform(5.5, 7.5)
        out.append(B(x, yd - d, x + w, yd - rng.uniform(0, 0.3), z, z + hh, rng.choice(COUL_LIVRES)))
        x += w + 0.06
    return out


def _mur_de_chene(B):
    """Mur de tête : planches de chêne de 16½ po sur fond noir (joints creux), ligne à 82 po, socle noir en retrait.
    Retourne (fixe, porte) : les morceaux de la porte dérobée pivotent avec le battant ouv-SS-008."""
    bords = [242.25, XP0, 261.0, XP1] + [XP1 + PAS * k for k in range(1, 11)] + [446.0]
    fixe = [B(XP1, YB, 446.0, 370.0, 0, 96, "carbone"), B(242.25, YB, XP0, 370.0, 0, 96, "carbone"),
            B(XP0, YB, XP1, 370.0, ZL - 0.2, 96, "carbone")]
    porte = [B(XP0, YB, XP1, YB + 0.1, 0.9, ZL - 0.1, "carbone")]
    for a, b in zip(bords, bords[1:]):
        x0 = a + (JOINT / 2 if a > 242.3 else 0)
        x1 = b - (JOINT / 2 if b < 445.9 else 0)
        bas = B(x0, YF, x1, YB, 1.0, ZL - JOINT / 2, "placage")
        (porte if XP0 <= a and b <= XP1 else fixe).append(bas)
        fixe.append(B(x0, YF, x1, YB, ZL + JOINT / 2, 96, "placage"))
    return fixe, porte


def appliquer_scene(S, h):
    B, A, C, CY, CX, T, SPH, TOR, MOD = h.B, h.A, h.C, h.CY, h.CX, h.T, h.SPH, h.TOR, h.MOD
    S["mobilier"][:] = [o for o in S["mobilier"] if not _ma_zone(o)]
    M = []

    # ------------------------------------------------------------------ mur de chêne et porte dérobée
    fixe, porte = _mur_de_chene(B)
    # dos de la porte (côté walk-in, devant le battant uni du plan) : miroir pleine hauteur, cadre noir mince
    porte += [B(249.0, 371.85, 270.0, 372.1, 8, 76, "inox"), B(248.6, 371.8, 249.0, 372.2, 7.6, 76.4, "metal"),
              B(270.0, 371.8, 270.4, 372.2, 7.6, 76.4, "metal"), B(248.6, 371.8, 270.4, 372.2, 7.6, 8, "metal"),
              B(248.6, 371.8, 270.4, 372.2, 76, 76.4, "metal")]
    for o in porte:
        o["porte"] = "ouv-SS-008"
    M += fixe + porte

    # ------------------------------------------------------------------ lit-plateforme queen, tête rembourrée, liseuses
    x0, y0, x1, y1 = LIT
    M += [B(x0 + 4, y0 + 4, x1 - 4, y1 - 4, 0, 3.5, "metal"),                                            # socle noir en retrait
          A(x0, y0, x1, y1, 3.5, 13, "placage", r=0.8, b=0.35)]
    for xs, d in ((x0, -1), (x1, 1)):                                    # 2 tiroirs par côté (y 286-316, 317-347)
        for ya, yb in ((286.0, 316.0), (317.0, 347.0)):
            M += [B(min(xs, xs + d * 0.12), ya - 0.12, max(xs, xs + d * 0.12), ya + 0.12, 4.2, 12.6, "carbone"),
                  B(min(xs, xs + d * 0.12), yb - 0.12, max(xs, xs + d * 0.12), yb + 0.12, 4.2, 12.6, "carbone"),
                  B(min(xs, xs + d * 0.12), ya + 0.4, max(xs, xs + d * 0.12), yb - 0.4, 11.6, 12.2, "carbone")]  # gorge
    M += [A(313.5, 283.0, 373.5, 363.0, 13, 22.5, "draps", r=2.5, b=2.0),                               # matelas
          A(312.9, 282.4, 374.1, 342.0, 21.2, 24.0, "draps", r=2.2, b=1.2),                             # couette blanche
          B(312.7, 283.0, 313.3, 341.5, 15.0, 22.5, "draps"), B(373.7, 283.0, 374.3, 341.5, 15.0, 22.5, "draps"),
          B(313.2, 282.2, 373.8, 282.8, 15.0, 22.5, "draps"),
          A(313.0, 336.0, 374.0, 344.0, 23.0, 25.2, "draps", r=2.0, b=1.0),                             # repli
          A(317.0, 346.0, 341.5, 362.0, 22.0, 28.5, "draps", r=4, b=3), A(345.5, 346.0, 370.0, 362.0, 22.0, 28.5, "draps", r=4, b=3),
          A(312.4, 283.5, 374.6, 302.0, 23.6, 25.0, "tapis", r=1.5, b=0.6),                             # jeté de laine avoine
          B(312.0, 284.0, 312.7, 301.5, 16.0, 24.4, "tapis"), B(374.3, 284.0, 375.0, 301.5, 16.0, 24.4, "tapis")]
    M += [A(310.5, 365.0, 376.5, YF, 16, 46, NAVY, r=1.2, b=1.0)]                                         # tête rembourrée
    for xl, s in ((298.0, 1), (389.0, -1)):                                                               # liseuses murales
        xt, yt = xl + s * 5.5, YF - 11.5
        M += [CY(xl, YF - 0.6, YF, 46, 2.4, "metal", pans=32),
              T([(xl, YF - 0.6, 46), (xl, YF - 7, 46.2), (xt, yt, 46.0)], 0.3, "metal"),
              C(xt, yt, 2.3, 41.5, 45.6, "metal", r2=1.3, pans=32), C(xt, yt, 1.9, 41.4, 41.5, "spot", pans=32)]
    # chevets : blocs de travertin adouci (18 × 15, dessus à 21)
    for xa in (289.0, 380.0):
        M += [A(xa, 352.0, xa + 18, 367.0, 0, 21, "pierre_travertin", r=1.0, b=0.6)]
    M += [B(292.0, 356.0, 301.0, 363.0, 21, 21.9, "draps"), B(292.5, 356.4, 300.5, 362.6, 21.9, 22.6, "carbone"),  # 2 livres
          C(392.0, 358.5, 1.6, 21, 24.6, "blanc", pans=24)]                                                      # une tasse

    # ------------------------------------------------------------------ grand tapis (8 × 10 pi) et lanterne de papier
    M += [A(283.5, 251.5, 403.5, 347.5, 0, 0.6, "tapis", r=1.5, b=0.25)]
    LX, LY, LZ, LR, LE = 343.5, 312.0, 83.0, 14.0, 0.68              # au-dessus du milieu du lit, dessous à 73½ po
    M += [SPH(LX, LY, LZ, LR, "abat-jour", ecrase=LE)]
    for dz in (-6.6, -3.4, 0.0, 3.4, 6.6):                                                               # nervures de bambou
        M += [TOR(LX, LY, LZ + dz, LR * math.sqrt(max(0.0, 1 - (dz / (LR * LE)) ** 2)) + 0.08, 0.09, "osier", axe="z")]
    zt = LZ + LR * LE
    M += [C(LX, LY, 1.8, zt - 0.4, zt + 0.3, "metal"), C(LX, LY, 0.15, zt, 95.6, "metal"), C(LX, LY, 2.6, 95.6, 96, "metal")]

    # ------------------------------------------------------------------ bureau réglable, tablette, lampe, chaise
    DX0, DX1, DY0, DY1, DZ = 391.0, 445.0, 232.75, 256.75, 27.25
    M += [A(DX0, DY0, DX1, DY1, DZ - 1.25, DZ, "placage", r=0.5, b=0.3),
          B(DX0 + 3, DY0 + 9, DX1 - 3, DY0 + 12, DZ - 3, DZ - 1.25, "metal"),                          # cadre
          B(DX1 - 9, DY1 - 0.5, DX1 - 5, DY1 + 0.1, DZ - 2.1, DZ - 1.25, "metal")]                      # commande
    for xc in (DX0 + 4.5, DX1 - 4.5):                                                                  # 2 colonnes
        M += [B(xc - 1.8, DY0 + 8.5, xc + 1.8, DY0 + 12.5, 1.2, 14, "metal"),
              B(xc - 1.4, DY0 + 8.9, xc + 1.4, DY0 + 12.1, 14, DZ - 1.25, "metal"),
              B(xc - 1.3, DY0 + 1.0, xc + 1.3, DY1 - 1.0, 0.3, 1.2, "metal")]
    M += [A(DX0, 232.25, DX1, 242.25, 50, 51.5, "placage", r=0.3, b=0.2)]                               # tablette flottante
    M += _livres(B, 393.0, 418.0, 241.8, 51.5, 7) + [B(418.6, 236.0, 419.2, 242.0, 51.5, 57.5, "metal"),
                                                    B(418.6, 236.0, 423.0, 242.0, 51.5, 51.7, "metal")]  # serre-livres
    lx, ly = 438.0, 236.5                                                                              # lampe d'architecte
    M += [C(lx, ly, 2.6, DZ, DZ + 0.8, "metal", pans=32),
          T([(lx, ly, DZ + 0.8), (lx - 1, ly + 3, DZ + 15), (lx - 9, ly + 9, DZ + 19)], 0.28, "metal"),
          C(lx - 10, ly + 10, 2.4, DZ + 14.6, DZ + 18.6, "metal", r2=1.3, pans=32),
          C(lx - 10, ly + 10, 2.0, DZ + 14.5, DZ + 14.6, "spot", pans=32)]
    M += [B(404.0, 243.0, 417.0, 252.0, DZ, DZ + 0.3, "blanc"), B(410.4, 243.0, 410.6, 252.0, DZ + 0.3, DZ + 0.35, "carbone"),
          C(399.0, 238.5, 1.5, DZ, DZ + 4, "placage", pans=24)]                                        # cahier, pot à crayons
    M += [C(399.0 + dx, 238.5 + dy, 0.18, DZ + 3, DZ + 7.5, "carbone", pans=8) for dx, dy in ((-0.5, 0.3), (0.4, -0.3), (0.2, 0.6))]
    M += [MOD("chaise_bureau", 418.0, 268.5, face="-y")]

    # ------------------------------------------------------------------ coin lecture : fauteuil bas marine, liseuse sur pied
    FX0, FY0, FX1, FY1 = 404.0, 336.0, 434.0, 366.0
    M += [B(FX0 + 3, FY0 + 3, FX1 - 3, FY1 - 3, 0, 3, "metal"),
          A(FX0, FY0, FX1, FY1, 3, 14, NAVY, r=3.5, b=2.0),
          A(FX0, FY1 - 8, FX1, FY1, 14, 31, NAVY, r=3.5, b=2.5),                                       # dossier
          A(FX0, FY0 + 0.5, FX0 + 5.5, FY1 - 6, 14, 24, NAVY, r=2.5, b=2.0),                           # accoudoirs
          A(FX1 - 5.5, FY0 + 0.5, FX1, FY1 - 6, 14, 24, NAVY, r=2.5, b=2.0),
          A(FX0 + 5.5, FY0 + 1, FX1 - 5.5, FY1 - 7.5, 14, 18.5, NAVY, r=3.0, b=2.2),                   # coussins
          A(FX0 + 6, FY1 - 13, FX1 - 6, FY1 - 7.5, 17, 30, NAVY, r=2.5, b=2.0),
          A(FX1 - 6.2, FY0 + 6, FX1 + 0.4, FY0 + 18, 22.6, 25.0, "tapis", r=1.2, b=0.8),               # jeté sur l'accoudoir
          B(FX1 + 0.05, FY0 + 6.3, FX1 + 0.6, FY0 + 17.7, 12, 24, "tapis")]
    bx, by = 440.5, 361.0
    M += [C(bx, by, 4.5, 0, 0.9, "metal", pans=40), C(bx, by, 0.45, 0.9, 58, "metal"),
          T([(bx, by, 58), (bx - 3, by - 1.5, 61), (bx - 13, by - 6, 60)], 0.3, "metal"),
          C(bx - 14, by - 6.5, 3.2, 54, 59, "metal", r2=1.6, pans=32), C(bx - 14, by - 6.5, 2.8, 53.9, 54, "spot", pans=32)]
    M += [C(432.5, 314.3, 2.2, 0, 0.08, "inox", pans=32)]                       # couvercle affleurant du drain (432½, 314¼)

    # ------------------------------------------------------------------ WALK-IN (ancien caveau) : fini 83 × 47½, plafond 84
    M += [B(229, 380, 231.5, 430, 0, 84, NAVY), B(314.5, 380, 317, 430, 0, 84, NAVY),
          B(231.5, 427.5, 314.5, 430, 0, 84, NAVY), B(229, 380, 317, 430, 84, 96, "plafond")]
    # penderie à deux hauteurs (x 231½-286) : tringles noires à 40 (lui) et 78 po (la grandeur suivante, puis l'ado)
    PX1 = 286.0
    for z in (40.0, 78.0):
        M += [CX(231.5, PX1, 416.5, z, 0.6, "metal"), B(231.5, 415.6, 232.4, 417.4, z - 1.2, z + 1.2, "metal")]
    rng = random.Random(5)

    def vetement(x, ep, zb, zt, larg, mat):
        """Vêtement sur cintre de chêne (crochet noir sur la tringle, 2 po au-dessus de zt)."""
        xc, ya, yb = x + ep / 2, 416.5 - larg / 2, 416.5 + larg / 2
        return [A(x, ya, x + ep, yb, zb, zt - 0.6, mat, r=0.3, b=0.25),
                A(x, ya + 1.2, x + ep, yb - 1.2, zt - 0.6, zt, mat, r=0.3, b=0.25),
                B(xc - 0.2, ya + 0.8, xc + 0.2, yb - 0.8, zt, zt + 0.5, "placage"),
                T([(xc, 416.5, zt + 0.5), (xc, 416.5, zt + 1.3), (xc, 417.1, zt + 2.0)], 0.1, "metal")]
    x, k = 234.0, 0
    while x < 281:                                                                                     # ses vêtements (bas)
        ep = rng.uniform(0.9, 1.6)
        M += vetement(x, ep, rng.uniform(19, 23), 38.0, rng.uniform(12, 14), COUL_VET[k % len(COUL_VET)])
        x += ep + rng.uniform(1.4, 2.6)
        k += 1
    x = 236.0
    while x < 272:                                                                                     # grandeur suivante (haut)
        ep = rng.uniform(1.0, 1.8)
        M += vetement(x, ep, rng.uniform(46, 52), 76.0, rng.uniform(14, 16), COUL_VET[(k * 2) % len(COUL_VET)])
        x += ep + rng.uniform(4.5, 7)
        k += 1
    # colonne de chêne (x 287-314½) : 4 tiroirs, dessus-valet à 36¾, tablettes éclairées à 50, 64 et 78
    TX0, TX1, TY0 = 286.0, 314.5, 405.5
    M += [B(TX0, TY0, TX0 + 1, 427.5, 0, 84, "placage"),                                                # flanc (porte les tringles)
          B(TX0 + 1, TY0 + 0.6, TX1, 427.5, 0, 1, "carbone"), B(TX0 + 1, TY0 + 0.5, TX1, 427.5, 1, 36, "placage"),
          A(TX0, TY0 - 0.5, TX1, 427.5, 36, 36.75, "placage", r=0.3, b=0.2)]
    for za, zb in ((1.2, 10.2), (10.5, 19.0), (19.3, 27.6), (27.9, 35.8)):
        M += [A(TX0 + 1.15, TY0 - 0.25, TX1 - 0.15, TY0 + 0.5, za, zb, "placage", r=0.2, b=0.15),
              B(TX0 + 9.5, TY0 - 0.33, TX1 - 8.5, TY0 - 0.2, zb - 1.0, zb - 0.5, "metal")]               # gorge noire
    for z in (50.0, 64.0, 78.0):
        M += [B(TX0 + 1, TY0, TX1, 427.5, z, z + 0.75, "placage"), B(TX0 + 1.5, TY0 + 0.3, TX1 - 0.5, TY0 + 0.9, z - 0.15, z, "spot")]
    M += [B(290.0, 409.0, 300.0, 416.0, 36.75, 37.25, "metal")]                                         # vide-poche
    M += [A(288.5, 408.0, 299.5, 420.0, 50.75, 53.8, "tissu", r=0.8, b=0.5), A(288.8, 408.3, 299.2, 419.7, 53.8, 56.8, "draps", r=0.8, b=0.5),
          A(301.5, 408.0, 312.5, 420.0, 50.75, 53.5, "carbone", r=0.8, b=0.5), A(301.8, 408.3, 312.2, 419.7, 53.5, 56.2, "tapis", r=0.8, b=0.5),
          A(288.5, 408.0, 299.5, 420.0, 64.75, 67.6, "tapis", r=0.8, b=0.5), A(301.5, 408.0, 312.5, 420.0, 64.75, 67.4, "draps", r=0.8, b=0.5),
          A(288.5, 408.0, 312.5, 426.0, 78.75, 83.4, "osier", r=1.0, b=0.5)]                           # bac des parents
    # banc à souliers (x 300½-314½, y 381-405, assise à 16) et 2 paires
    M += [B(300.5, 381.0, 301.25, 405.0, 0, 15.25, "placage"), B(301.25, 381.0, 314.5, 381.75, 0, 15.25, "placage"),
          B(301.25, 404.25, 314.5, 405.0, 0, 15.25, "placage"), B(301.25, 381.75, 314.5, 404.25, 6.0, 6.75, "placage"),
          A(300.5, 381.0, 314.5, 405.0, 15.25, 16.25, "placage", r=0.4, b=0.2)]
    M += [A(302.5, 383.5, 313.0, 387.5, 6.75, 10.0, "carbone", r=1.6, b=0.9), A(302.5, 388.3, 313.0, 392.3, 6.75, 10.0, "carbone", r=1.6, b=0.9),
          A(302.5, 394.5, 313.0, 398.5, 0.2, 3.6, "blanc", r=1.6, b=0.9), A(302.5, 399.3, 313.0, 403.3, 0.2, 3.6, "blanc", r=1.6, b=0.9)]
    # 3 crochets noirs sur le mur ouest (z 48) et le sac d'école
    for y in (385.0, 392.5, 400.0):
        M += [CX(231.5, 233.3, y, 48, 0.35, "metal"), SPH(233.5, y, 48, 0.8, "metal")]
    M += [A(231.7, 380.8, 237.0, 390.5, 31, 47, "tissu", r=2.2, b=1.6)]
    # DEL linéaire devant la penderie, panneau rayonnant au plafond
    M += [B(232.0, 403.6, 314.0, 404.4, 83.6, 84, "spot"), B(248.0, 383.0, 282.0, 399.0, 83.3, 84, "blanc")]

    S["mobilier"] += M

    # ------------------------------------------------------------------ peinture, lumières, visites, palette
    pt = S.setdefault("peinture", {})
    pt["piece-SS-CH2"] = "Blanc chaud"
    pt["piece-SS-LEG"] = "Marine"
    pt.pop("piece-SS-GR2", None)                  # ancienne garde-robe de la chambre 2 (fusionnée)
    utilisees = set(pt.values()) | {a.get("peinture") for a in S.get("accents", [])}
    if "Sauge" not in utilisees:                  # la sauge n'est plus nulle part
        S.get("peintures", {}).pop("Sauge", None)
    S["lumieres"][:] = [l for l in S["lumieres"] if not (_dans((l["x"], l["y"]), CH2) or _dans((l["x"], l["y"]), WI))]
    S["lumieres"] += [{"x": 300, "y": 352}, {"x": 388, "y": 352}, {"x": 296, "y": 264}, {"x": 420, "y": 300},
                      {"x": LX, "y": LY, "z": 91, "i": 5}, {"x": 268, "y": 404, "z": 86, "i": 4}]
    vis = S["visites"]
    i = next((k for k, v in enumerate(vis) if v.get("nom") == "Chambre 2"), len(vis))
    vis[:] = [v for v in vis if v.get("nom") not in ("Chambre 2", "Walk-in (caveau isolé)")]
    vis[i:i] = [{"nom": "Chambre 2 — vue d'entrée (mur de chêne, lit, coin lecture)", "x": 262, "y": 244, "cap": 50},
                {"nom": "Chambre 2 — bureau réglable et fenêtre", "x": 290, "y": 262, "cap": 16},
                {"nom": "Walk-in — penderie à deux hauteurs et colonne de tiroirs", "x": 250, "y": 378, "cap": 60}]
    pal = S.setdefault("palette", [])
    pal[:] = [p for p in pal if not p[0].startswith(("Chambre 2", "Walk-in"))]
    for p in pal:
        if p[0] == "Chambres" and "chambre 2" in p[1]:
            p[1] = p[1].split("; chambre 2")[0].rstrip(" ;")
    pal += [["Chambre 2 « le mur de chêne »", "murs blanc chaud ; mur de tête pleine largeur en planches de chêne blanc de "
             "16½ po à joints creux noirs, porte dérobée du walk-in intégrée ; lit queen sur plateforme de chêne à 4 tiroirs "
             "(socle noir en retrait), tête rembourrée marine, 2 liseuses murales noir mat, chevets en blocs de travertin "
             "adouci ; bureau réglable (chêne, piètement noir) et sa tablette ; fauteuil bas marine et liseuse sur pied "
             "noire à la fenêtre ; tapis de laine avoine 8 × 10 pi ; lanterne de papier washi Ø 28 po", "#C9A574"],
            ["Walk-in de la chambre 2", "peint marine (l'accent de la chambre, avec la tête de lit et le fauteuil) ; penderie "
             "à deux hauteurs (tringles noires à 40 et 78 po), colonne de chêne à 4 tiroirs et 3 tablettes éclairées, banc "
             "à souliers, crochets noirs, miroir au dos de la porte dérobée, DEL linéaire, panneau rayonnant", "#2E3B4E"]]
