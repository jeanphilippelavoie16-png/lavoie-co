"""MAISON-18 — aménagement intérieur du garage 13' × 17' (demande du client du 2026-11-02 : « Je veux que tu l'aménages aussi.
Coin atelier, rack à vélo suspendu, super rangement de bacs, place pour la souffleuse, quelque chose de nice. »).

Module chargé par exterieur.py (importlib, comme les autres modules du projet) : amenagement(...) reçoit la coque du garage
(constantes CAB… d'exterieur.py) et rend les données à fusionner dans EXTERIEUR. Pouces, z ABSOLU (repère du plancher du
sous-sol), mêmes formes et mêmes conventions que le contrat d'exterieur.py.

Intérieur fini : x 360 → 506 (146 po, 12'-2"), y 626 (mur de la porte) → 820 (mur du fond) (194 po, 16'-2"), dalle à 48,5,
plafond à 142,5 (7'-10"). Porte de garage de 8' (x 385 → 481) dessinée ouverte : panneau sous le plafond de y 627 à 711, rails
jusqu'à y 717 ; rien ne monte au plafond dans cette bande.

Programme (plan coté dans DESIGN_garage.md) :
- devant, derrière la porte : la souffleuse (2 phases, 28 × 50 × 44 po) sur un tapis de caoutchouc ; elle sort tout droit ;
- mur de gauche (côté piscine), devant : rail noir avec les pelles, le poussoir et le grattoir à toit ; extincteur et prise ;
- mur de gauche, au fond : établi de 8 pi (dessus en bloc de boucher de chêne, deux caissons à tiroirs noirs, étau, tabouret),
  panneau perforé noir mat avec les outils, tablette et DEL sous la tablette, barre de prises ;
- mur du fond : le mur de bacs (pièce maîtresse) : rack sur mesure noir mat, 6 colonnes × 5 rangées = 30 bacs identiques de
  68 L glissés par le rebord comme des tiroirs, couvercles noirs, étiquettes (rangée du haut : bacs saisonniers, étiquettes
  kraft), dessus en chêne ;
- mur de droite, au fond : vélos des gars à LEUR hauteur (support au sol, roue avant dans la fente), deux trottinettes, casques
  sur des crochets à 38 po ; au-dessus, les deux vélos des adultes sur palans à poulies, à l'envers, près du plafond (guidons
  de 24 po décalés, rien ne dépasse au-dessus de l'allée) ;
- mur de droite, devant : rail des outils de jardin ; armoire noire ventilée et verrouillée des produits de piscine, en haut à
  58 po du sol, sur le bout de mur à droite de la porte (loin de la souffleuse et de l'essence) ;
- plafond : 4 luminaires DEL de 4 pi (lumières de la visite).
Allée centrale de 71 po (5'-11") entre l'établi et les vélos ; 50 po libres de la porte à l'établi à droite de la souffleuse.
"""
import math

# matériaux propres au garage : [couleur, description, alias] (fusionnés dans EXTERIEUR["peintures"])
PEINTURES = {
    "Noir mat (garage)": ["#1F2022", "rack à bacs, panneau perforé, rails et crochets du garage", "ext-noir-mat"],
    "Bac gris givré": ["#C2C7C9", "bacs de rangement identiques de 68 L (corps)", "ext-bac"],
    "Étiquette kraft": ["#C49A62", "étiquettes des bacs saisonniers (rangée du haut)", "ext-etiquette-kraft"],
    "Rouge souffleuse": ["#A8231C", "souffleuse 2 phases, extincteur", "ext-souffleuse"],
    "Bleu marine vélo": ["#2E4E73", "vélo, casque et trottinette du plus vieux", "ext-velo-bleu"],
    "Gris vélo": ["#6E7276", "vélo d'un adulte", "ext-velo-gris"],
}

PALETTE = [
    ["Garage — mur de bacs", "rack sur mesure noir mat, 30 bacs identiques de 68 L gris givré, couvercles noirs, étiquettes ; dessus en chêne", "#C2C7C9"],
    ["Garage — établi de 8 pi", "bloc de boucher de chêne, caissons à tiroirs noirs, panneau perforé noir mat, DEL sous la tablette", "#1F2022"],
    ["Garage — vélos", "palans à poulies pour les 2 vélos des adultes ; support au sol et crochets bas pour les gars", "#2E4E73"],
    ["Garage — souffleuse", "place derrière la porte, tapis de caoutchouc noir 40 × 70 po", "#A8231C"],
]


# ------------------------------------------------------------------------------------------------- formes du moteur
def B(x0, y0, x1, y1, z0, z1, mat):
    return {"forme": "boite", "x0": round(min(x0, x1), 2), "y0": round(min(y0, y1), 2), "x1": round(max(x0, x1), 2),
            "y1": round(max(y0, y1), 2), "z0": round(min(z0, z1), 2), "z1": round(max(z0, z1), 2), "mat": mat}


def C(x, y, r, z0, z1, mat, **k):
    return dict({"forme": "cylindre", "x": round(x, 2), "y": round(y, 2), "r": r, "z0": round(z0, 2), "z1": round(z1, 2), "mat": mat}, **k)


def CX(x0, x1, y, z, r, mat, pans=16):        # cylindre couché selon x
    return {"forme": "cylindre", "axe": "x", "x0": round(x0, 2), "x1": round(x1, 2), "y": round(y, 2), "z": round(z, 2), "r": r, "mat": mat, "pans": pans}


def CY(y0, y1, x, z, r, mat, pans=16):        # cylindre couché selon y
    return {"forme": "cylindre", "axe": "y", "y0": round(y0, 2), "y1": round(y1, 2), "x": round(x, 2), "z": round(z, 2), "r": r, "mat": mat, "pans": pans}


def T(pts, r, mat, **k):
    return dict({"forme": "tube", "pts": [[round(v, 2) for v in p] for p in pts], "r": r, "mat": mat}, **k)


def SPH(x, y, z, r, mat, **k):
    return dict({"forme": "sphere", "x": round(x, 2), "y": round(y, 2), "z": round(z, 2), "r": r, "mat": mat}, **k)


def TOR(x, y, z, R, r, mat, **k):
    return dict({"forme": "tore", "x": round(x, 2), "y": round(y, 2), "z": round(z, 2), "R": R, "r": r, "mat": mat}, **k)


def rect(x0, y0, x1, y1):
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]


NOIR, BOIS = "ext-noir-mat", "chene"


# ------------------------------------------------------------------------------------------------- vélo (formes simples)
def velo(o, axe, sens, R, WB, hs, hb, bw, cadre, z0=None, renverse_a=None, rt=0.7, sl=10.0):
    """Vélo en tubes : o = (x, y) du moyeu arrière, axe "x" ou "y" (direction du vélo), sens ±1 (vers l'avant), R rayon hors
    tout de la roue, WB empattement, hs hauteur de la selle, hb du guidon, bw largeur du guidon. Debout sur z0, ou à l'envers
    (renverse_a = z du dessus des pneus, palan au plafond)."""
    ox, oy = o

    def p(u, v, w):
        z = (z0 + w) if renverse_a is None else (renverse_a - w)
        return (ox + sens * u, oy + v, z) if axe == "x" else (ox + v, oy + sens * u, z)
    roue = {} if axe == "x" else {"axe": "x"}
    out = []
    for u in (0, WB):                                                   # roues : pneu, jante, moyeu
        c = p(u, 0, R)
        out += [TOR(*c, R - 0.9, 0.9, "pneu", **roue), TOR(*c, R - 2.1, 0.35, "inox", **roue)]
        out.append(CY(c[1] - 1.6, c[1] + 1.6, c[0], c[2], 0.7, "inox", 10) if axe == "x" else CX(c[0] - 1.6, c[0] + 1.6, c[1], c[2], 0.7, "inox", 10))
    bbu, bbw = 0.41 * WB, 0.78 * R + 1
    st = (bbu - 0.3 * (hs - 7 - bbw), hs - 7)                          # haut du tube de selle
    sa = (bbu - 0.3 * (hs - bbw), hs - 1)                               # selle
    hb_ = (WB - 3.5, R + 5.5)                                           # bas du tube de direction
    ht = (WB - 5.5, hb - 6)                                             # haut du tube de direction
    tub = lambda a, b, r=rt, m=cadre: T([p(a[0], 0, a[1]), p(b[0], 0, b[1])], r, m, pans=8)
    out += [tub((0, R), (bbu, bbw)), tub((0, R), st), tub((bbu, bbw), st), tub(st, ht), tub((bbu, bbw), hb_), tub(hb_, ht, rt * 1.2)]
    for v in (-1.4, 1.4):                                               # fourche et haubans doublés
        out.append(T([p(hb_[0], v * 0.6, hb_[1]), p(WB, v, R)], rt * 0.8, cadre, pans=8))
    out.append(tub(st, sa, rt * 0.7, "inox"))                           # tige de selle
    s0, s1 = p(sa[0] - sl / 2, -sl * 0.26, sa[1]), p(sa[0] + sl / 2, sl * 0.26, sa[1] + 2)
    out.append(B(s0[0], s0[1], s1[0], s1[1], s0[2], s1[2], "pneu"))     # selle
    st_ = (WB - 4.5, hb)                                                # potence et guidon
    out.append(tub(ht, st_, rt * 0.8, "metal"))
    g0, g1 = p(st_[0], -bw / 2, st_[1]), p(st_[0], bw / 2, st_[1])
    out.append(T([g0, g1], 0.5, "metal", pans=8))
    for v in (-bw / 2, bw / 2 - 4):                                     # poignées
        a, b = p(st_[0], v, st_[1]), p(st_[0], v + 4, st_[1])
        out.append(T([a, b], 0.75, "pneu", pans=8))
    c = p(bbu, 1.5, bbw)                                                # plateau et manivelles
    out.append(TOR(*c, 0.28 * R, 0.3, "metal", **roue))
    out += [T([p(bbu, 1.8, bbw), p(bbu + 0.45 * R, 2.6, bbw - 0.3 * R)], 0.45, "metal", pans=6),
            T([p(bbu, -1.8, bbw), p(bbu - 0.45 * R, -2.6, bbw + 0.3 * R)], 0.45, "metal", pans=6)]
    return out


# ------------------------------------------------------------------------------------------------- aménagement
def amenagement(cab, ep, z_dalle, z_plafond, porte, z_panneau):
    """{"objets", "obstacles", "lumieres", "visites", "peintures", "palette"} du garage aménagé (z absolu)."""
    X0, Y0, X1, Y1 = cab[0] + ep, cab[1] + ep, cab[2] - ep, cab[3] - ep        # intérieur fini : 360, 626, 506, 820
    Z, ZC = z_dalle, z_plafond
    PA, PB = porte[0], porte[1]
    o, obs = [], []

    # -- souffleuse 2 phases (28 × 50 × 44 po) derrière la porte, la vis vers la porte : elle sort tout droit
    SX0, SY0 = 397.0, 636.0
    sx1, xm = SX0 + 28, SX0 + 14
    zt = Z + 0.4
    o.append(B(391, 630, 431, 702, Z, zt, "caoutchouc-noir"))                                  # tapis 40 × 70 po (rebord)
    o += [B(391, 630, 431, 631, zt, zt + 0.5, "caoutchouc-noir"), B(391, 701, 431, 702, zt, zt + 0.5, "caoutchouc-noir"),
          B(391, 630, 392, 702, zt, zt + 0.5, "caoutchouc-noir"), B(430, 630, 431, 702, zt, zt + 0.5, "caoutchouc-noir")]
    R = "ext-souffleuse"
    o += [B(SX0, SY0, sx1, SY0 + 4, zt, zt + 1.5, "metal"),                                    # lame racleuse
          B(SX0, SY0 + 15, sx1, SY0 + 18, zt + 1, zt + 21.5, R),                                # carter de la vis, ouvert devant
          B(SX0, SY0 + 1, sx1, SY0 + 18, zt + 19.5, zt + 21.5, R), CX(SX0, sx1, SY0 + 17, zt + 19.5, 2, R, 12),
          B(SX0, SY0 + 1, SX0 + 1.2, SY0 + 18, zt + 1, zt + 21.5, R), B(sx1 - 1.2, SY0 + 1, sx1, SY0 + 18, zt + 1, zt + 21.5, R),
          CX(SX0 + 1.2, sx1 - 1.2, SY0 + 8.5, zt + 10, 8, "metal", 16),                         # vis
          CX(xm - 2, xm + 2, SY0 + 8.5, zt + 10, 8.6, "gris", 16),                              # turbine (au centre)
          C(xm + 6, SY0 + 14, 3.6, zt + 18, zt + 33, R, pans=16),                               # goulotte et déflecteur
          B(xm + 3, SY0 + 8.5, xm + 9, SY0 + 14, zt + 31, zt + 35, R),
          B(SX0 + 5, SY0 + 19, sx1 - 5, SY0 + 37, zt + 9, zt + 24, R),                          # moteur
          B(SX0 + 7, SY0 + 21, sx1 - 7, SY0 + 35, zt + 24, zt + 29, "metal"),
          C(SX0 + 9, SY0 + 33, 2.2, zt + 29, zt + 31, "metal", pans=12)]                        # bouchon d'essence
    for x in (SX0 + 2, sx1 - 2):                                                                # roues de 15 po
        o.append(CX(x - 2, x + 2, SY0 + 34, zt + 7.5, 7.5, "pneu", 20))
    for x in (SX0 + 3, sx1 - 3):                                                                # mancherons
        o.append(T([(x, SY0 + 33, zt + 18), (x, SY0 + 44, zt + 34), (x, SY0 + 53, zt + 43)], 0.6, "metal", pans=8))
    o += [T([(SX0 + 3, SY0 + 53, zt + 43), (sx1 - 3, SY0 + 53, zt + 43)], 0.75, "pneu", pans=8),
          B(xm - 7, SY0 + 41, xm + 7, SY0 + 45, zt + 32, zt + 36, "metal")]                     # tableau de commande
    obs.append({"nom": "Garage, souffleuse", "pts": rect(SX0 - 1, SY0 - 1, sx1 + 1, SY0 + 55)})

    # -- pelles, poussoir et grattoir à toit sur un rail noir (mur de gauche, devant) ; extincteur et prise sur le bout de mur
    o.append(B(X0, 630, X0 + 1, 690, Z + 57, Z + 60, NOIR))
    for y in (640, 664, 681):
        o.append(B(X0 + 1, y - 1, X0 + 3.5, y + 1, Z + 56.5, Z + 58, NOIR))                    # crochets
    o += [T([(X0 + 3, 640, Z + 3), (X0 + 3, 640, Z + 79)], 0.7, "inox", pans=8),                # grattoir à toit (perche)
          B(X0 + 1.5, 629, X0 + 6, 651, Z + 79, Z + 83, "inox"),
          T([(X0 + 3.5, 664, Z + 19), (X0 + 3.5, 664, Z + 57)], 0.65, "bois_brut", pans=8),     # poussoir de 24 po
          B(X0 + 1.5, 652, X0 + 3.5, 676, Z + 4, Z + 19, "metal"), B(X0 + 2.5, 663, X0 + 4.5, 665, Z + 57, Z + 62, "metal"),
          T([(X0 + 6, 681, Z + 19), (X0 + 6, 681, Z + 57)], 0.65, "bois_brut", pans=8),         # pelle de 18 po
          B(X0 + 4, 672, X0 + 6.5, 690, Z + 5, Z + 19.5, "metal"), B(X0 + 5, 680, X0 + 7, 682, Z + 57, Z + 62, "metal")]
    obs.append({"nom": "Garage, pelles et grattoir", "pts": rect(X0, Y0, X0 + 8, 691)})
    o += [C(377, Y0 + 3, 2.6, Z + 24, Z + 40, "ext-souffleuse", pans=16), C(377, Y0 + 3, 1.2, Z + 40, Z + 43, "metal", pans=10),
          B(375, Y0, 379, Y0 + 0.6, Z + 30, Z + 36, NOIR),                                     # extincteur ABC
          B(367, Y0, 370, Y0 + 0.4, Z + 44, Z + 48.5, "blanc")]                                 # prise (démarreur électrique)

    # -- établi de 8 pi (x 360-385, y 692-788) : bloc de boucher de chêne, 2 caissons à tiroirs noirs, panneau perforé noir
    EY0, EY1, EX1, ZE = 692.0, 788.0, 385.0, Z + 36
    o.append(B(X0, EY0, EX1, EY1, ZE - 1.5, ZE, BOIS))
    for (a, b) in ((EY0 + 2, EY0 + 30), (EY1 - 30, EY1 - 2)):
        o.append(B(X0 + 1, a, EX1 - 2, b, Z + 3, ZE - 1.5, "metal"))
        o.append(B(X0 + 2, a + 1, EX1 - 3, b - 1, Z, Z + 3, NOIR))                              # socle en retrait
        for zz in (Z + 11, Z + 18, Z + 24, Z + 29.5):                                           # joints des 5 tiroirs
            o.append(B(EX1 - 2.05, a, EX1 - 1.9, b, zz - 0.25, zz + 0.25, "gris"))
        for zz in (Z + 9, Z + 16, Z + 22, Z + 27.5, Z + 33):                                    # poignées
            o.append(B(EX1 - 2, a + 6, EX1 - 1.3, b - 6, zz - 0.35, zz + 0.35, "inox"))
    o += [B(X0 + 1, EY0 + 30, EX1 - 3, EY1 - 30, Z + 5, Z + 6, NOIR),                           # tablette basse (au milieu)
          B(X0, EY0 + 30, X0 + 1, EY1 - 30, Z, ZE - 1.5, NOIR)]
    o += [B(X0 + 0.75, EY0, X0 + 1.5, EY1, Z + 40, Z + 72, NOIR),                               # panneau perforé 8' × 32"
          B(X0 + 0.75, EY0, X0 + 2, EY1, Z + 72, Z + 73.5, BOIS), B(X0 + 0.75, EY0, X0 + 2, EY1, Z + 38.5, Z + 40, BOIS),
          B(X0 + 0.75, EY0, X0 + 2, EY0 + 1.5, Z + 38.5, Z + 73.5, BOIS), B(X0 + 0.75, EY1 - 1.5, X0 + 2, EY1, Z + 38.5, Z + 73.5, BOIS)]
    o += [B(X0, EY0, X0 + 11, EY1, Z + 76, Z + 77.5, BOIS)]                                      # tablette de chêne
    for y in (EY0 + 6, (EY0 + EY1) / 2, EY1 - 6):
        o += [B(X0, y - 0.6, X0 + 9, y + 0.6, Z + 75, Z + 76, NOIR), B(X0, y - 0.6, X0 + 1, y + 0.6, Z + 68, Z + 76, NOIR)]
    o += [B(X0 + 8, EY0 + 2, X0 + 9.5, EY1 - 2, Z + 75.4, Z + 76, "spot")]                      # DEL sous la tablette
    for i in range(4):                                                                           # 4 bacs à quincaillerie
        y = EY0 + 5 + i * 22.5
        o += [B(X0 + 1, y, X0 + 10, y + 14, Z + 77.5, Z + 84, "ext-bac"), B(X0 + 0.8, y - 0.2, X0 + 10.3, y + 14.2, Z + 84, Z + 85, "metal"),
              B(X0 + 10, y + 4, X0 + 10.1, y + 10, Z + 79.5, Z + 82, "blanc")]
    o.append(B(X0 + 1.5, EY0 + 20, X0 + 3, EY1 - 20, ZE + 1, ZE + 3.5, NOIR))                   # barre de prises (2 × 4 prises)
    for i in range(8):
        y = EY0 + 24 + i * 6.6
        o.append(B(X0 + 3, y, X0 + 3.1, y + 1.6, ZE + 1.6, ZE + 2.9, "blanc"))
    # outils au panneau : niveau, serre-joints, marteau, clés, ruban, tournevis, scie, perceuse
    P_ = X0 + 1.5
    o += [B(P_, EY0 + 6, P_ + 1.2, EY0 + 30, Z + 65, Z + 67.5, "inox"),
          B(P_, EY0 + 6, P_ + 1.3, EY0 + 8, Z + 65, Z + 67.5, "metal"), B(P_, EY0 + 28, P_ + 1.3, EY0 + 30, Z + 65, Z + 67.5, "metal")]
    for y in (EY0 + 8, EY0 + 14):
        o += [B(P_, y, P_ + 0.8, y + 0.8, Z + 44, Z + 61, "inox"), B(P_, y - 0.5, P_ + 2.5, y + 4, Z + 59, Z + 61.5, "metal"),
              B(P_, y - 0.5, P_ + 2.5, y + 4, Z + 47, Z + 49.5, "metal")]
    o += [T([(P_ + 1, EY0 + 24, Z + 46), (P_ + 1, EY0 + 24, Z + 58)], 0.6, "bois_brut", pans=8),
          B(P_, EY0 + 21, P_ + 2, EY0 + 27.5, Z + 58, Z + 59.8, "metal")]
    for i, L in enumerate((6, 7, 8, 9, 10)):
        y = EY0 + 33 + i * 2.2
        o.append(B(P_, y, P_ + 0.4, y + 0.9, Z + 60 - L, Z + 60, "inox"))
    o.append(B(P_, EY0 + 45, P_ + 2.6, EY0 + 48.5, Z + 63, Z + 66.5, "metal"))
    for i in range(6):
        y = EY0 + 52 + i * 2
        o += [T([(P_ + 1, y, Z + 55), (P_ + 1, y, Z + 59.5)], 0.55, "metal", pans=8), T([(P_ + 1, y, Z + 49), (P_ + 1, y, Z + 55)], 0.15, "inox", pans=6)]
    o += [B(P_, EY0 + 66, P_ + 0.3, EY0 + 82, Z + 46, Z + 53, "inox"), B(P_, EY0 + 82, P_ + 1.2, EY0 + 87, Z + 45.5, Z + 53.5, "bois_brut")]
    o += [B(P_, EY1 - 26, P_ + 3, EY1 - 18, Z + 62, Z + 66, NOIR), B(P_, EY1 - 24, P_ + 3, EY1 - 21, Z + 56, Z + 62, NOIR),
          B(P_ + 0.5, EY1 - 25, P_ + 2.5, EY1 - 20, Z + 54.5, Z + 56, "gris")]                  # perceuse sans fil sur son crochet
    # étau, au bout de l'établi côté porte
    o += [B(EX1 - 7, EY0 + 4, EX1 + 1, EY0 + 12, ZE, ZE + 2, "metal"), B(EX1 - 5, EY0 + 5, EX1 + 1, EY0 + 11, ZE + 2, ZE + 6, "metal"),
          B(EX1 + 1, EY0 + 4.5, EX1 + 4, EY0 + 11.5, ZE + 0.5, ZE + 7, "metal"),
          T([(EX1 + 4, EY0 + 8, ZE + 3.5), (EX1 + 7.5, EY0 + 8, ZE + 3.5)], 0.4, "inox", pans=8),
          T([(EX1 + 7.5, EY0 + 4.5, ZE + 3.5), (EX1 + 7.5, EY0 + 11.5, ZE + 3.5)], 0.3, "inox", pans=8)]
    # tabouret d'atelier (assise de chêne, pattes noires), devant la baie ouverte
    tx, ty = 397.0, 740.0
    o += [C(tx, ty, 7, Z + 25, Z + 26.5, BOIS, pans=24), C(tx, ty, 5.5, Z + 23.5, Z + 25, "metal", pans=20),
          TOR(tx, ty, Z + 9, 7, 0.35, "metal", axe="z")]
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        o.append(T([(tx + 4.5 * math.cos(a), ty + 4.5 * math.sin(a), Z + 24), (tx + 8.5 * math.cos(a), ty + 8.5 * math.sin(a), Z)], 0.45, "metal", pans=8))
    obs += [{"nom": "Garage, établi", "pts": rect(X0, EY0, EX1 + 1, EY1)},
            {"nom": "Garage, étau", "pts": rect(EX1, EY0 + 4, EX1 + 8, EY0 + 12)},
            {"nom": "Garage, tabouret", "pts": rect(tx - 8, ty - 8, tx + 8, ty + 8)}]

    # -- mur de bacs (fond) : rack sur mesure noir mat, 6 colonnes × 5 rangées de bacs de 68 L (20 × 28 × 15 po) glissés par le
    #    rebord ; couvercles noirs, étiquettes blanches (rangée du haut : saisonniers, étiquettes kraft) ; dessus en chêne
    RY0, RY1, RX0 = Y1 - 30, Y1, 362.5
    BAIE, MONT = 21.75, 1.5
    for i in range(7):
        x = RX0 + i * (BAIE + MONT)
        o += [B(x, RY0, x + MONT, RY1, Z, Z + 86, NOIR), B(x - 0.2, RY0 - 0.2, x + MONT + 0.2, RY0 + 0.6, Z, Z + 86, NOIR)]
    rx1 = RX0 + 6 * (BAIE + MONT) + MONT
    o += [B(RX0 - 0.5, RY0 - 0.75, rx1 + 0.5, RY1, Z + 86, Z + 87.5, BOIS), B(RX0, RY0, rx1, RY0 + 2, Z, Z + 1.5, NOIR)]
    for j in range(5):
        zb = Z + 2.5 + j * 16.5
        for i in range(6):
            xa = RX0 + MONT + i * (BAIE + MONT)
            xc = xa + BAIE / 2
            o += [B(xa + 0.9, RY0 + 1.2, xa + BAIE - 0.9, RY1 - 1, zb, zb + 13.5, "ext-bac"),         # corps
                  B(xa + 0.1, RY0 + 0.7, xa + BAIE - 0.1, RY1 - 0.5, zb + 13.5, zb + 14.8, "metal"),  # couvercle (repose sur les tasseaux)
                  B(xc - 4.2, RY0 + 1.05, xc + 4.2, RY0 + 1.2, zb + 6.3, zb + 11.2, "metal"),           # porte-étiquette noir
                  B(xc - 3.5, RY0 + 0.95, xc + 3.5, RY0 + 1.05, zb + 7, zb + 10.5, "ext-etiquette-kraft" if j == 4 else "blanc")]
            o.append(B(xa - 0.1, RY0 + 0.6, xa + 0.6, RY1 - 1, zb + 12.6, zb + 13.4, NOIR))           # tasseaux (rails)
            o.append(B(xa + BAIE - 0.6, RY0 + 0.6, xa + BAIE + 0.1, RY1 - 1, zb + 12.6, zb + 13.4, NOIR))
    obs.append({"nom": "Garage, mur de bacs", "pts": rect(X0, RY0 - 1, X1, Y1)})

    # -- vélos : les gars à leur hauteur (support au sol contre le mur de droite), les adultes au plafond sur palans
    o.append(B(X1 - 18, 721, X1, 763, Z, Z + 0.4, NOIR))                                           # support au sol
    for (yc, R_, WB, hs, hb, bw, coul, casque) in ((731.0, 8.3, 28.0, 21.0, 26.0, 18.0, "ext-velo-bleu", "ext-velo-bleu"),
                                                   (753.0, 7.2, 25.0, 18.5, 23.0, 16.0, "rouge-velo", "ext-souffleuse")):
        xr = X1 - 2.5 - R_ - WB                                                                   # moyeu arrière (roue avant au mur)
        o += velo((xr, yc), "x", 1, R_, WB, hs, hb, bw, coul, z0=Z + 0.4, rt=0.6, sl=7.0)
        o += [B(X1 - 9, yc - 2.2, X1 - 1, yc - 1.6, Z + 1, Z + 11, NOIR), B(X1 - 9, yc + 1.6, X1 - 1, yc + 2.2, Z + 1, Z + 11, NOIR)]
        o += [B(X1 - 1.5, yc - 0.6, X1, yc + 0.6, Z + 41, Z + 43, NOIR),                         # crochet et casque à 38 po
              SPH(X1 - 5.5, yc, Z + 37, 5, casque, ecrase=0.78), B(X1 - 9.5, yc - 3.5, X1 - 8.5, yc + 3.5, Z + 33.5, Z + 35, "metal")]
    for (yc, coul, hT) in ((771.0, "ext-velo-bleu", 30.0), (782.0, "rouge-velo", 26.0)):          # trottinettes
        o += [B(X1 - 26, yc - 2.5, X1 - 6, yc + 2.5, Z + 2.5, Z + 3.7, coul), CY(yc - 1, yc + 1, X1 - 24, Z + 2.2, 2.2, "pneu", 14),
              CY(yc - 1, yc + 1, X1 - 5, Z + 2.2, 2.2, "pneu", 14),
              T([(X1 - 6, yc, Z + 3.5), (X1 - 4, yc, Z + hT)], 0.55, "inox", pans=8),
              T([(X1 - 4, yc - 6, Z + hT), (X1 - 4, yc + 6, Z + hT)], 0.5, "metal", pans=8)]
    o.append(B(X1 - 0.4, 716, X1, 719, Z + 44, Z + 48.5, "blanc"))                               # prise (recharge)
    obs.append({"nom": "Garage, vélos et trottinettes des gars (vélos des adultes au-dessus)", "pts": rect(X1 - 50, 719, X1, RY0 - 1)})
    ZT = ZC - 2.5                                                                                # dessus des pneus (à l'envers)
    for (xv, sens, y_arr, coul) in ((493.5, 1, 733.6, "carbone"), (470.0, -1, 774.6, "ext-velo-gris")):     # guidons de 24 po
        o += velo((xv, y_arr), "y", sens, 13.6, 41.0, 38.0, 39.5, 24.0, coul, renverse_a=ZT, rt=0.75)
        for u in (0.41 * 41 - 0.3 * (38 - 0.78 * 13.6 - 1), 41 - 4.5):                          # câbles des palans : selle, guidon
            yy = y_arr + sens * u
            zh = ZT - (38 if u < 20 else 39.5) - 1
            o += [B(xv - 2, yy - 2, xv + 2, yy + 2, ZC - 1.5, ZC, NOIR), C(xv + 2.6, yy, 1.4, ZC - 4, ZC - 1.5, "metal", pans=12),
                  T([(xv + 2.6, yy, ZC - 3), (xv + 2.6, yy, zh)], 0.15, "metal", pans=4),
                  T([(xv + 2.6, yy - 1.5, zh - 1), (xv + 2.6, yy + 1.5, zh - 1)], 0.35, "metal", pans=6)]

    # -- outils de jardin sur un rail noir (mur de droite, devant)
    o.append(B(X1 - 1, 642, X1, 716, Z + 63, Z + 66, NOIR))
    xr = X1 - 3
    o += [T([(xr, 653, Z + 6), (xr, 653, Z + 66)], 0.6, "bois_brut", pans=8), B(xr - 1, 651, xr + 1, 655, Z + 63, Z + 67, NOIR)]
    for j in range(9):                                                                           # râteau à feuilles (éventail)
        o.append(T([(xr, 653, Z + 66), (xr, 653 + (j - 4) * 2.6, Z + 84)], 0.18, "metal", pans=4))
    o.append(T([(xr, 645, Z + 78), (xr, 661, Z + 78)], 0.25, "metal", pans=4))
    o += [T([(xr, 677, Z + 6), (xr, 677, Z + 66)], 0.6, "bois_brut", pans=8),                      # balai-poussoir de 24 po
          B(xr - 1.5, 665, xr + 1.5, 689, Z + 66, Z + 69, "bois_brut"), B(xr - 1.2, 665.3, xr + 1.2, 688.7, Z + 69, Z + 72.5, "metal")]
    o += [T([(xr, 697, Z + 6), (xr, 697, Z + 68)], 0.6, "bois_brut", pans=8),                      # râteau
          B(xr - 1, 690, xr + 1, 704, Z + 68, Z + 69.5, "metal")]
    for j in range(8):
        o.append(B(xr - 0.25, 690.5 + j * 1.85, xr + 0.25, 691.1 + j * 1.85, Z + 69.5, Z + 72.5, "metal"))
    o += [T([(xr, 710, Z + 9), (xr, 710, Z + 66)], 0.6, "bois_brut", pans=8),                      # bêche
          B(xr - 0.6, 705.5, xr + 0.6, 714.5, Z + 66, Z + 78, "metal"), TOR(xr, 710, Z + 7, 2.4, 0.45, "metal", axe="x")]
    obs.append({"nom": "Garage, outils de jardin", "pts": rect(X1 - 7, 642, X1, 717)})

    # -- armoire noire ventilée et verrouillée des produits de piscine : bout de mur à droite de la porte, de 58 à 88 po
    ax0, ax1, zb = PB + 4, X1 - 0.5, Z + 58
    o += [B(ax0, Y0, ax1, Y0 + 12, zb, zb + 30, "metal"),
          B(ax0 + 0.5, Y0 + 12, ax1 - 0.5, Y0 + 12.15, zb + 0.5, zb + 29.5, NOIR)]
    for zz in (zb + 3, zb + 4.5, zb + 6, zb + 24, zb + 25.5, zb + 27):                         # persiennes (haut et bas)
        o.append(B(ax0 + 3, Y0 + 12.1, ax1 - 3, Y0 + 12.4, zz, zz + 0.6, "gris"))
    o += [B(ax1 - 4, Y0 + 12.1, ax1 - 3, Y0 + 12.8, zb + 12, zb + 18, "inox"),                   # poignée et cadenas
          B(ax1 - 4.6, Y0 + 12.4, ax1 - 2.4, Y0 + 13.4, zb + 10, zb + 11.8, "laiton"),
          B(ax0 + 3, Y0 + 12.1, ax0 + 11, Y0 + 12.3, zb + 14, zb + 17, "blanc")]                  # étiquette

    # -- éclairage DEL : 4 luminaires de 4 pi (4000 K) hors de la bande de la porte ouverte
    LUM = ((405.0, 728.0, 776.0), (437.0, 728.0, 776.0), (494.0, 642.0, 690.0), (372.0, 642.0, 690.0))
    for (x, a, b) in LUM:
        o += [B(x - 2.2, a, x + 2.2, b, ZC - 1.8, ZC, "blanc"), B(x - 1.7, a + 0.6, x + 1.7, b - 0.6, ZC - 2.1, ZC - 1.8, "spot")]
    lumieres = [{"x": x, "y": (a + b) / 2, "z": ZC + 2, "i": 1.1} for (x, a, b) in LUM]

    visites = [{"nom": "Garage — atelier et rangement", "x": 452, "y": 660, "cap": 112, "z": Z}]
    return {"objets": o, "obstacles": obs, "lumieres": lumieres, "visites": visites, "peintures": PEINTURES, "palette": PALETTE}
