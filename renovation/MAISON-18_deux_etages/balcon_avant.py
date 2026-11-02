"""MAISON-18 — balcon avant EXISTANT (photos du client, 2026-11-02), intégré à la visite extérieure.

Le client : « Voici mon balcon avant, intègre-le à la visite. » ; il est devant la façade (la porte d'entrée sort dessus), « 24 pi
jusqu'à la rue » et « il termine juste un peu à côté de la porte (à droite de la porte d'entrée quand tu regardes d'en avant) » ;
le coin des enfants est devant, vers la rue ; « Il est comme surélevé. Le filet noir sur le balcon c'est un filet katamaran pour
lire. » On le reproduit tel quel (pas un nouveau design). Relevé estimé sur 15 photos (DESIGN_balcon_avant.md) : à valider.

appliquer_exterieur(EXT) (appelé par scene_3d.py après la création de SCENE["exterieur"]) :
- retire le perron de béton du relevé (objets de exterieur.perron_avant(), planchers « Perron avant » et « Marches du perron »,
  garde-corps du perron, trou du perron plein) : le balcon le remplace. L'excroissance de fondation du sous-sol (chambre froide
  sous l'ancien perron) reste, coiffée de sa dalle, sous le balcon ;
- ajoute le balcon (objets, planchers, obstacles), l'escalier avant (relief creusé dans exterieur.py : ESC_AV, AIRE_AV), le coin
  des enfants, les couleurs (peintures et légende « Extérieur ») et quatre arrêts de visite.

Repère de exterieur.py (pouces) : x le long de la façade (0 à 456, vers la droite vu de la rue), y vers l'arrière (façade 0, rue
-480), z absolu depuis le plancher du sous-sol (RDC 105).

Plan retenu (vu de dessus, la rue en bas) :
- grand plancher x -90 à 232 (26'-10"), y -180 à 0 (15'), à 103,5 (1½ po sous le seuil) ; partie avant droite (filet) x 112 à 232,
  y -288 à -180 : le balcon fait 24 pi de profond à droite ;
- pergola sur le côté gauche (écran d'intimité du voisin) : poteaux x 49, y -177 / -104 / -31 et poteaux dans l'écran ; BBQ et
  banquette en L dessous ;
- filet catamaran (83 × 54 po) dans le plancher, au coin avant droit, banc de planche le long du garde-corps droit, 3 coussins ;
- plateforme basse (une marche plus bas) x 52 à 112 devant le grand plancher ; trois marches et une glissade vers le coin des
  enfants (x -90 à 52, y -288 à -180, paillis à 66) : maisonnette « 86 », carré de sable, mur d'escalade sur la clôture ;
- escalier avant de bois neuf : du côté droit du balcon (y -144 à -96), 15 contremarches de 7,55 po et 14 girons de 11 po vers
  l'allée, jusqu'à l'asphalte ; main courante côté rue, lampes solaires ; boîte aux lettres noire sur poteau.
"""
import importlib.util
import json
import math
import os

ICI = os.path.dirname(os.path.abspath(__file__))


def _ext():
    spec = importlib.util.spec_from_file_location("m18_exterieur_pour_balcon", os.path.join(ICI, "exterieur.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


X = _ext()
B, P, C, T, SPH, ARR, rect = X.B, X.P, X.C, X.T, X.SPH, X.ARR, X.rect

# ------------------------------------------------------------------------------------------------- relevé estimé (pouces)
ZB = X.Z_BALCON                 # 103,5 : dessus des planches
XG, XD = -90.0, 232.0           # nu gauche (écran du voisin) et nu droit (rive, un peu à droite de la porte x 177-211)
YAV, YK = -288.0, -180.0        # devant du balcon (24 pi) ; bord avant du grand plancher côté coin des enfants
XP, XF = 52.0, 112.0            # alignement des poteaux de la pergola = bord gauche de la plateforme ; bord droit de la plateforme
Z_PLAT = ZB - 7.5               # plateforme basse (une marche)
Z_PAILLIS = Z_PLAT - 3 * 7.5    # paillis du coin des enfants (trois marches sous la plateforme) : 66
FILET = (130.0, -278.0, 213.0, -224.0)        # ouverture du filet catamaran
X0E, YAE, X1E, YBE = X.ESC_AV                 # escalier avant (exterieur.py)
ZA_ESC = X.z_allee((YAE + YBE) / 2)           # asphalte au pied
R_ESC = (ZB - ZA_ESC) / X.ESC_AV_N            # hauteur de contremarche (7,55)
G_ESC = (X1E - X0E) / (X.ESC_AV_N - 1)        # giron (11)
Z_DALLE = ZA_ESC + 2.0                        # dalle de béton au pied de l'escalier
H_GC = 36.0                                   # garde-corps

PEINTURES = {
    "Pin naturel du balcon": ["#AD967F", "planches du balcon avant (pin naturel grisonné)", "bal-planche"],
    "Cadres teints foncés": ["#3A332D", "bandes qui encadrent le filet et divisent le plancher ; rives, solives, poutres et poteaux sous le balcon", "bal-cadre"],
    "Bois teint (pergola)": ["#6E4C33", "poteaux et poutres de la pergola, base de la banquette", "bal-teint"],
    "Bois naturel (mains courantes)": ["#B8895E", "mains courantes, poteaux de garde-corps, banc du filet, plateforme et marches", "bal-main"],
    "Écran à planches horizontales": ["#966843", "écrans d'intimité et clôtures du coin des enfants", "bal-ecran"],
    "Bois neuf (escalier avant)": ["#CBA36F", "escalier avant neuf : girons, contremarches, limons, main courante", "bal-neuf"],
    "Filet catamaran noir": ["#121212", "filet tendu dans l'ouverture du plancher", "bal-filet"],
    "Coussins noirs (filet)": ["#1E1E20", "coussins du filet catamaran", "bal-coussin-noir"],
    "Coussins gris foncé": ["#454A50", "coussins de la banquette en L", "bal-coussin"],
    "Paillis de cèdre": ["#6B3B23", "sol du coin des enfants", "bal-paillis"],
    "Sable": ["#C4B89E", "carré de sable", "bal-sable"],
    "Glissade bleue": ["#2B7FD0", "glissade du coin des enfants", "bal-glissade"],
    "Maisonnette": ["#A5764D", "maisonnette « 86 » (planches horizontales)", "bal-maisonnette"],
    "Prise d'escalade verte": ["#3DBB4C", "mur d'escalade", "bal-prise-v"],
    "Prise d'escalade jaune": ["#F0CF1A", "mur d'escalade", "bal-prise-j"],
    "Prise d'escalade rose": ["#E5427E", "mur d'escalade", "bal-prise-r"],
    "Prise d'escalade bleue": ["#2F6CDB", "mur d'escalade", "bal-prise-b"],
    "Prise d'escalade orange": ["#F07A1E", "mur d'escalade", "bal-prise-o"],
}
PALETTE = [
    ["Balcon avant : pin naturel", "planches de 5½ po (pas de composite), sens alternés d'un panneau à l'autre", "#AD967F"],
    ["Cadres teints foncés", "bandes de 5½ po autour du filet et entre les panneaux ; structure sous le balcon", "#3A332D"],
    ["Pergola de bois teint", "poteaux 6 × 6 et poutres, quincaillerie noire", "#6E4C33"],
    ["Garde-corps du balcon", "main courante et poteaux de bois naturel, barreaux noirs ; un panneau de verre teinté à droite", "#B8895E"],
    ["Écrans d'intimité", "planches horizontales teintes sur montants d'acier noir (voisin de gauche, coin des enfants)", "#966843"],
    ["Filet catamaran", "maille noire tendue dans le plancher, coussins noirs", "#121212"],
    ["Escalier avant neuf", "15 contremarches de bois neuf, main courante côté rue, lampes solaires", "#CBA36F"],
    ["Coin des enfants", "paillis de cèdre, carré de sable, glissade bleue, maisonnette « 86 », mur d'escalade", "#6B3B23"],
]


def zt(x, y):
    return X._zg(x, y)


# ------------------------------------------------------------------------------------------------- aides
def planches(x0, y0, x1, y1, sens, z1, mat="bal-planche", e=1.0, larg=5.5, jeu=0.25):
    """Planches de larg po (jeu entre elles) remplissant le rectangle, posées selon x ("x") ou selon y ("y"), dessus à z1."""
    out = []
    a, b = (y0, y1) if sens == "x" else (x0, x1)
    s = a
    while s < b - 0.5:
        t = min(s + larg, b)
        out.append(B(x0, s, x1, t, z1 - e, z1, mat) if sens == "x" else B(s, y0, t, y1, z1 - e, z1, mat))
        s = t + jeu
    return out


def garde_corps(a, b, z, montants=(), verre=None, h=H_GC, mat="bal-main"):
    """Garde-corps de bois (le long de x ou de y) : poteaux 3½ po aux bouts et aux positions « montants » (distance depuis a),
    main courante 5½ × 1½, lisse 2 × 4 dessous, lisse basse, barreaux noirs ¾ po à 4 po c/c ; verre = (s0, s1) : panneau de verre
    teinté au lieu des barreaux entre ces distances."""
    (xa, ya), (xb, yb) = a, b
    L = math.hypot(xb - xa, yb - ya)
    ux, uy = (xb - xa) / L, (yb - ya) / L
    enx = abs(ux) > 0.5

    def bx(s0, s1, d0, d1, z0, z1, m):
        s0, s1 = min(s0, s1), max(s0, s1)
        if enx:
            return B(xa + ux * s0, ya + d0, xa + ux * s1, ya + d1, z0, z1, m)
        return B(xa + d0, ya + uy * s0, xa + d1, ya + uy * s1, z0, z1, m)
    out = []
    pos = sorted({0.0, L} | {float(s) for s in montants})
    for s in pos:
        s = min(max(s, 1.75), L - 1.75)
        out.append(bx(s - 1.75, s + 1.75, -1.75, 1.75, z, z + h - 1.5, mat))
    out += [bx(0, L, -2.75, 2.75, z + h - 1.5, z + h, mat),                 # main courante (2 × 6 à plat)
            bx(0, L, -0.75, 0.75, z + h - 5, z + h - 1.5, mat),             # lisse 2 × 4 de chant
            bx(0, L, -1.75, 1.75, z + 2, z + 3.5, mat)]                     # lisse basse
    for s0, s1 in zip(pos, pos[1:]):
        a0, a1 = s0 + 1.75, s1 - 1.75
        if verre and a0 >= verre[0] - 2 and a1 <= verre[1] + 2:
            out.append(bx(a0 + 0.5, a1 - 0.5, -0.35, 0.35, z + 4, z + h - 5.5, "vitre-ext"))
            out += [bx(a0 + 3, a0 + 5, -0.9, 0.9, zc, zc + 2, "metal") for zc in (z + 8, z + h - 10)]
            out += [bx(a1 - 5, a1 - 3, -0.9, 0.9, zc, zc + 2, "metal") for zc in (z + 8, z + h - 10)]
            continue
        n = max(1, round((a1 - a0) / 4))
        for j in range(1, n):
            s = a0 + (a1 - a0) * j / n
            out.append(bx(s - 0.375, s + 0.375, -0.375, 0.375, z + 3.5, z + h - 5, "metal"))
    return out


def ecran(a, b, z0, z1, montants, cote=1, mat="bal-ecran"):
    """Écran d'intimité : planches horizontales de 5½ po (jours de ¾ po) sur montants d'acier noir 1½ po (positions depuis a,
    du côté « cote » : +1 vers +x ou +y)."""
    (xa, ya), (xb, yb) = a, b
    enx = abs(xb - xa) > abs(yb - ya)
    out, z = [], z0
    while z < z1 - 0.5:
        zz = min(z + 5.5, z1)
        out.append(B(xa, ya - 0.6, xb, ya + 0.6, z, zz, mat) if enx else B(xa - 0.6, ya, xa + 0.6, yb, z, zz, mat))
        z = zz + 0.75
    for s in montants:
        if enx:
            x = min(xa, xb) + s
            out.append(B(x - 0.75, ya + cote * 0.6, x + 0.75, ya + cote * 2.1, z0, z1, "metal"))
        else:
            y = min(ya, yb) + s
            out.append(B(xa + cote * 0.6, y - 0.75, xa + cote * 2.1, y + 0.75, z0, z1, "metal"))
    return out


# ------------------------------------------------------------------------------------------------- plancher, structure
def plancher():
    """Planches de pin naturel en panneaux de sens alternés, bandes teintes foncées (rives, filet, alignement des poteaux de la
    pergola, x 127, y -104), fond sombre dans les joints ; rives, solives, poutres et poteaux teints foncés dessous."""
    o = []
    z1 = ZB
    cad = lambda x0, y0, x1, y1: B(x0, y0, x1, y1, z1 - 1, z1, "bal-cadre")
    # fond des joints (pas sous le filet)
    for r in [(XG, YK, XD, 0), (XF, YAV, XD, -278), (XF, -224, XD, YK), (XF, -278, 130, -224), (213, -278, XD, -224)]:
        o.append(B(*r, z1 - 1.6, z1 - 1, "bal-cadre"))
    # bandes teintes foncées
    for r in [(226.5, YAV, XD, 0), (XF, YAV, 226.5, -282.5), (XF, -282.5, 117.5, YK), (XG, YK, 117.5, YK + 5.5),
              (XG, YK + 5.5, XG + 5.5, 0), (XG + 5.5, -5.5, 226.5, 0), (XP - 5.5, YK + 5.5, XP, -5.5),
              (124.5, -218.5, 130, -5.5), (XP, -106.75, 124.5, -101.25),
              (117.5, -283.5, 130, -218.5), (130, -283.5, 213.5, -278), (117.5, -224, 226.5, -218.5)]:
        o.append(cad(*r))
    # panneaux de planches (sens alternés)
    o += planches(XG + 5.5, YK + 5.5, XP - 5.5, -5.5, "y", z1)          # sous la pergola
    o += planches(XP, -101.25, 124.5, -5.5, "x", z1)
    o += planches(XP, YK + 5.5, 124.5, -106.75, "y", z1)
    o += planches(117.5, YK, 124.5, -5.5, "y", z1)
    o += planches(130, -218.5, 226.5, -5.5, "y", z1)                     # devant la porte et le long du garde-corps droit
    o += planches(213.5, -278, 226.5, -224, "y", z1)                     # sous le banc
    # rives (2 × 10 doubles), solives 2 × 8 à 16 po, poutres triples 2 × 10, poteaux 6 × 6 et étriers noirs
    zr0, zs0 = z1 - 1 - 9.25, z1 - 1 - 7.25
    for r in [(XD - 3, YAV, XD, 0), (XF, YAV, XD, YAV + 3), (XF, YAV, XF + 3, YK), (XG, YK, XF, YK + 3), (XG, YK, XG + 3, 0),
              (XG, -3, 0, 0)]:
        o.append(B(*r, zr0, z1 - 1, "bal-cadre"))
    x = XG + 16
    fx0, fy0, fx1, fy1 = FILET
    while x < XD - 4:
        y0 = YAV + 3 if x > XF + 3 else YK + 3
        if fx0 - 3 < x < fx1 + 3:                   # solives coupées par l'ouverture du filet (chevêtres)
            o += [B(x - 0.75, y0, x + 0.75, fy0 - 3, zs0, z1 - 1, "bal-cadre"), B(x - 0.75, fy1 + 3, x + 0.75, -3, zs0, z1 - 1, "bal-cadre")]
        else:
            o.append(B(x - 0.75, y0, x + 0.75, -3, zs0, z1 - 1, "bal-cadre"))
        x += 16
    o += [B(fx0 - 3, fy0 - 3, fx1 + 3, fy0, zs0, z1 - 1, "bal-cadre"), B(fx0 - 3, fy1, fx1 + 3, fy1 + 3, zs0, z1 - 1, "bal-cadre"),
          B(fx0 - 3, fy0, fx0, fy1, zs0, z1 - 1, "bal-cadre"), B(fx1, fy0, fx1 + 3, fy1, zs0, z1 - 1, "bal-cadre")]
    zp1 = zs0
    zp0 = zp1 - 9.25
    poteaux = []
    for (yb, xs) in [(YK + 4.25, (XG + 2.75, -20, XP - 2.75, XF, 172, XD - 2.75)), (-92, (XG + 2.75, -20, XP - 2.75, XF, 172, XD - 2.75)),
                     (YAV + 5.75, (XF + 2.75, 172, XD - 2.75))]:
        o.append(B(min(xs) - 2.75, yb - 2.25, max(xs) + 2.75, yb + 2.25, zp0, zp1, "bal-cadre"))
        for xp in xs:
            zb = zt(xp, yb) - 2
            o += [B(xp - 2.75, yb - 2.75, xp + 2.75, yb + 2.75, zb, zp0, "bal-cadre"),
                  B(xp - 3.25, yb - 3.25, xp + 3.25, yb + 3.25, zp0 - 4, zp0 + 1, "metal")]
            poteaux.append((xp, yb))
    # dessus de l'excroissance de fondation (chambre froide sous l'ancien perron), sous le balcon
    x0, y0, x1, y1 = X.PERRON
    o.append(B(x0, y0, x1, y1, 89, zs0 - 0.2, "beton"))
    return o, poteaux


def garde_corps_balcon():
    o = []
    # devant (partie du filet), y -288
    o += garde_corps((XF, YAV + 1.75), (XD, YAV + 1.75), ZB, montants=(60,))
    # côté droit : devant l'escalier (verre teinté entre -192 et -144), puis côté porte
    o += garde_corps((XD - 1.75, YAV), (XD - 1.75, YAE), ZB, montants=(48, 96), verre=(96, 144))
    o += garde_corps((XD - 1.75, YBE), (XD - 1.75, 0), ZB, montants=(48,))
    # entre le grand plancher et le coin des enfants (de l'écran au poteau avant de la pergola)
    o += garde_corps((XG + 1.5, YK + 1.5), (XP - 5.5, YK + 1.5), ZB, montants=(68,))
    # derrière, à gauche de la maison (du coin de l'écran au coin de la maison)
    o += garde_corps((XG + 1.5, -1.75), (0, -1.75), ZB, montants=())
    return o


def ecrans():
    o = []
    # écran du voisin de gauche, sur le balcon (6 pi), jusqu'au coin arrière gauche
    o += ecran((XG + 0.6, YK), (XG + 0.6, -4), ZB, ZB + 72, montants=(4, 50, 100, 150), cote=1)
    # clôtures du coin des enfants (bas : sous le paillis, haut : 144) : côté gauche (mur d'escalade) et devant (rue)
    zb3 = min(zt(XG, YAV), zt(XG, YK)) - 3
    o += ecran((XG + 0.6, YAV), (XG + 0.6, YK), zb3, 144, montants=(2, 54, 104), cote=1)
    zb2 = min(zt(x, YAV) for x in (XG, 0, XF)) - 3
    o += ecran((XG, YAV + 0.6), (XF, YAV + 0.6), zb2, 144, montants=(4, 52, 100, 148, 196), cote=1)
    # coin de la plateforme (boîte d'écran entre la plateforme et la partie du filet)
    o += ecran((XF - 1.0, YAV + 1.2), (XF - 1.0, -246), Z_PLAT, Z_PLAT + 40, montants=(), cote=-1)
    o.append(B(XF - 3, YAV + 1.2, XF + 0.5, -246, Z_PLAT + 40, Z_PLAT + 41.5, "bal-main"))
    return o


# ------------------------------------------------------------------------------------------------- pergola, BBQ, banquette
PERGOLA_Y = (YK + 2.75, -104.0, -30.75)
PERGOLA_X = (XP - 2.75, XG + 2.75)


def pergola():
    o = []
    zh = ZB + 88                                   # dessous des poutres (7'-4" sur le balcon), poutres 5½ × 7½
    for xc in PERGOLA_X:
        for yc in PERGOLA_Y:
            o += [B(xc - 2.75, yc - 2.75, xc + 2.75, yc + 2.75, ZB, zh, "bal-teint"),
                  B(xc - 3.2, yc - 3.2, xc + 3.2, yc + 3.2, ZB, ZB + 5, "metal")]               # étrier noir
            o += [B(xc + 2.75, yc - 4, xc + 3.05, yc + 4, zh - 10, zh + 6, "metal"),               # plaques en T noires
                  B(xc - 3.05, yc - 4, xc - 2.75, yc + 4, zh - 10, zh + 6, "metal")]
        o.append(B(xc - 2.75, YK - 4, xc + 2.75, -22, zh, zh + 7.5, "bal-teint"))           # poutres le long de y
    for yc in PERGOLA_Y:
        o.append(B(XG - 3, yc - 2.75, XP + 4, yc + 2.75, zh, zh + 7.5, "bal-teint"))        # poutres le long de x
        o.append(B(XP - 7, yc - 3.05, XP + 1, yc + 3.05, zh + 1, zh + 6.5, "metal"))         # plaque en T sur le dessus
    return o


def bbq():
    x0, x1, y0, y1 = XG + 7, XG + 29, -148.0, -122.0
    o = [B(x0, y0, x1, y1, ZB + 4, ZB + 33, "ext-bbq"),
         ARR(x0, y0 - 1, x1, y1 + 1, ZB + 33, ZB + 47, "ext-bbq", r=4, b=1.5),
         B(x1 - 0.5, y0, x1 + 0.6, y1, ZB + 29, ZB + 36, "inox"),                       # panneau de commande
         B(x0 + 1, y0 - 12, x1 - 1, y0, ZB + 34, ZB + 35.5, "inox"), B(x0 + 1, y1, x1 - 1, y1 + 12, ZB + 34, ZB + 35.5, "inox"),
         T([(x1 + 1.5, y0 + 2, ZB + 44), (x1 + 1.5, y1 - 2, ZB + 44)], 0.5, "inox", pans=8)]
    for xx in (x0 + 2, x1 - 2):
        for yy in (y0 + 2, y1 - 2):
            o.append(C(xx, yy, 1.5, ZB, ZB + 4, "pneu", pans=10))
    for k in range(3):                                                                 # boutons
        o.append(B(x1 + 0.6, y0 + 5 + 7 * k, x1 + 2, y0 + 7 + 7 * k, ZB + 31.5, ZB + 33.5, "metal"))
    return o


def banquette():
    o = []
    s0, s1 = ZB + 15, ZB + 19.5
    bx0 = XG + 5.5
    o += [B(bx0, -100, bx0 + 26, -10, ZB, s0, "bal-teint"), B(bx0 + 26, -36, 34, -10, ZB, s0, "bal-teint"),
          B(bx0, -10, 34, -4, ZB, ZB + 30, "bal-teint"), B(34, -36, 46, -10, ZB, ZB + 22, "bal-teint")]
    # coussins d'assise et de dossier (gris foncé)
    for (ya, yb) in ((-100, -78.5), (-78, -57.5), (-57, -36.5)):
        o.append(ARR(bx0 + 6, ya, bx0 + 26, yb, s0, s1, "bal-coussin", r=2.5, b=1.2))
    o.append(ARR(bx0 + 6, -36, bx0 + 26, -10.5, s0, s1, "bal-coussin", r=2.5, b=1.2))
    xs = [bx0 + 26, -5.0, 14.5, 34.0]
    for xa, xb in zip(xs, xs[1:]):
        o.append(ARR(xa + 0.3, -36, xb - 0.3, -16, s0, s1, "bal-coussin", r=2.5, b=1.2))
    for (ya, yb) in ((-100, -68), (-67.5, -36)):
        o.append(ARR(bx0, ya, bx0 + 6, yb, s1, ZB + 33, "bal-coussin", r=2, b=1.2))
    for (xa, xb) in ((bx0, bx0 + 30), (bx0 + 30.5, 0.0), (0.5, 33.5)):
        o.append(ARR(xa, -16, xb, -10, s1, ZB + 33, "bal-coussin", r=2, b=1.2))
    return o


# ------------------------------------------------------------------------------------------------- filet catamaran
def filet():
    """Maille noire tendue (cordes aux 2½ po), flèche de 4 po au milieu, bordure de corde, banc de planche le long du
    garde-corps droit, trois coussins noirs au bout gauche (tête)."""
    x0, y0, x1, y1 = FILET
    zb, S = ZB - 1.2, 4.0
    sag = lambda u, v: zb - S * math.sin(math.pi * u) * math.sin(math.pi * v)
    o = [T([(x0, y0, zb), (x1, y0, zb), (x1, y1, zb), (x0, y1, zb), (x0, y0, zb)], 0.55, "bal-filet", pans=6)]
    ny = round((y1 - y0) / 2.5)
    for k in range(1, ny):
        v = k / ny
        y = y0 + (y1 - y0) * v
        o.append(T([(x0 + (x1 - x0) * j / 6, y, sag(j / 6, v)) for j in range(7)], 0.2, "bal-filet", pans=4))
    nx = round((x1 - x0) / 2.5)
    for k in range(1, nx):
        u = k / nx
        x = x0 + (x1 - x0) * u
        o.append(T([(x, y0 + (y1 - y0) * j / 6, sag(u, j / 6)) for j in range(7)], 0.2, "bal-filet", pans=4))
    # coussins noirs (têtes) sur le filet, au bout gauche
    for k in range(3):
        ya = y0 + 1 + k * 17.5
        o.append(ARR(x0 + 1.5, ya, x0 + 17, ya + 16.5, zb - 1.6, zb + 4.2, "bal-coussin-noir", r=3, b=1.6))
    # banc : planche 2 × 12 le long du garde-corps droit
    o.append(B(213.5, -283.5, 226.5, -218.5, ZB, ZB + 1.75, "bal-main"))
    return o


# ------------------------------------------------------------------------------------------------- plateforme et coin des enfants
def coin_enfants():
    o = []
    # plateforme basse, trois marches pleines
    o += planches(XP, YAV + 1.5, XF, YK, "y", Z_PLAT, mat="bal-main")
    o.append(B(XP, YAV + 1.5, XF, YK, Z_PAILLIS - 4, Z_PLAT - 1, "bal-cadre"))
    for i in range(1, 4):
        o += planches(XP - 10 * i, -262, XP - 10 * (i - 1), YK - 0.25, "x", Z_PLAT - 7.5 * i, mat="bal-main", e=1.5)
        o.append(B(XP - 10 * i, -262, XP - 10 * (i - 1), YK - 0.25, Z_PAILLIS - 4, Z_PLAT - 7.5 * i - 1.5, "bal-main"))
    # paillis (massif sous le paillis caché par les clôtures) ; jupe teinte sous le bord du grand plancher
    zb = min(zt(XG, YAV), zt(XP, YAV), zt(XG, YK), zt(XP, YK)) - 2
    o.append(B(XG + 1.2, YAV + 1.2, XP, YK - 0.25, zb, Z_PAILLIS, "bal-paillis"))
    o += [B(XG + 1.2, YK - 0.25, XP - 5.5, YK + 1.5, Z_PAILLIS, ZB - 10.25, "bal-cadre")]
    # carré de sable (bordure 2 × 8 naturelle, coin coupé), dans le coin du mur d'escalade et du garde-corps
    pts = [(XG + 1.2, YK - 1.5), (-36, YK - 1.5), (-36, -224), (-48, -236), (XG + 1.2, -236)]
    for (a, b) in zip(pts, pts[1:] + pts[:1]):
        (xa, ya), (xb, yb) = a, b
        L = math.hypot(xb - xa, yb - ya)
        nx, ny = (yb - ya) / L * 1.5, -(xb - xa) / L * 1.5          # vers l'intérieur (contour en sens horaire)
        o.append(P([(xa, ya), (xb, yb), (xb + nx, yb + ny), (xa + nx, ya + ny)], Z_PAILLIS - 2, Z_PAILLIS + 7, "bal-main"))
    inner = [(XG + 2.7, YK - 3), (-37.5, YK - 3), (-37.5, -223.4), (-48.6, -234.5), (XG + 2.7, -234.5)]
    o.append(P(inner, Z_PAILLIS - 2, Z_PAILLIS + 3, "bal-sable"))
    o += [B(-60, -205, -54, -199, Z_PAILLIS + 3, Z_PAILLIS + 6, "bal-prise-j"), B(-72, -215, -66, -211, Z_PAILLIS + 3, Z_PAILLIS + 5.5, "bal-prise-o")]
    # mur d'escalade : prises sur la face intérieure de la clôture gauche, au-dessus du carré de sable
    cols = ["bal-prise-v", "bal-prise-j", "bal-prise-r", "bal-prise-b", "bal-prise-o"]
    k = 0
    for i, z in enumerate(range(80, 140, 11)):
        for j, y in enumerate((-230, -214, -198)):
            yy = y + (5 if (i + j) % 2 else -3)
            o.append(SPH(XG + 2.4, yy, z + (2 if j % 2 else 0), 1.9, cols[k % 5], ecrase=0.75))
            k += 1
    # glissade bleue : de la plateforme vers le fond, le long de la clôture avant
    n = 24
    ya, yb = -283.0, -267.0
    zz = lambda t: Z_PAILLIS + 2 + (Z_PLAT - Z_PAILLIS - 2) * (1 - t) ** 2
    for k in range(n):
        t0, t1 = k / n, (k + 1) / n
        xa, xb = XP - 52 * t1, XP - 52 * t0
        o.append(B(xa, ya, xb, yb, zz((t0 + t1) / 2) - 1, zz((t0 + t1) / 2), "bal-glissade"))
    for yr in (ya - 0.6, yb + 0.6):
        o.append(T([(XP - 52 * t, yr, zz(t) + 3) for t in (0, 0.2, 0.45, 0.7, 1.0)], 1.2, "bal-glissade", pans=8, bouts=True))
    o.append(B(XP - 54, ya - 1, XP - 50, yb + 1, Z_PAILLIS - 1, Z_PAILLIS + 2.5, "bal-glissade"))
    # maisonnette « 86 » (5 pi × 3'-4"), devant vers le balcon (+y), toit en appentis plus bas vers la rue
    mx0, mx1, my0, my1 = XG + 1.2, XG + 61.2, YAV + 1.2, -246.5
    zf, zr = Z_PAILLIS + 64, Z_PAILLIS + 54
    o += [B(mx0, my0, mx1, my0 + 1.5, Z_PAILLIS, zr, "bal-maisonnette"), B(mx0, my0, mx0 + 1.5, my1, Z_PAILLIS, zr, "bal-maisonnette"),
          B(mx1 - 1.5, my0, mx1, my1, Z_PAILLIS, zr, "bal-maisonnette")]
    for q in range(4):                                     # pignons en gradins sous l'appentis
        ya_ = my0 + (my1 - my0) * q / 4
        zq = zr + (zf - zr) * (q + 1) / 4
        o += [B(mx0, ya_, mx0 + 1.5, my1, zr, zq, "bal-maisonnette"), B(mx1 - 1.5, ya_, mx1, my1, zr, zq, "bal-maisonnette")]
    # façade : fenêtres ouvertes (cadres noirs), porte, affiche « Bureau », numéro « 86 »
    fy0, fy1 = my1 - 1.5, my1
    ouv = [(mx0 + 4, mx0 + 18, Z_PAILLIS + 22, Z_PAILLIS + 46), (mx0 + 23, mx0 + 37, Z_PAILLIS, Z_PAILLIS + 50),
           (mx0 + 42, mx0 + 56, Z_PAILLIS + 22, Z_PAILLIS + 46)]
    pos = mx0
    for (a, b, z0, z1) in ouv:
        o.append(B(pos, fy0, a, fy1, Z_PAILLIS, zf, "bal-maisonnette"))
        if z0 > Z_PAILLIS:
            o.append(B(a, fy0, b, fy1, Z_PAILLIS, z0, "bal-maisonnette"))
        o.append(B(a, fy0, b, fy1, z1, zf, "bal-maisonnette"))
        o += [B(a - 1.2, fy1, a, fy1 + 0.4, z0, z1, "metal"), B(b, fy1, b + 1.2, fy1 + 0.4, z0, z1, "metal"),
              B(a - 1.2, fy1, b + 1.2, fy1 + 0.4, z1, z1 + 1.2, "metal")]
        if z0 > Z_PAILLIS:
            o.append(B(a - 1.2, fy1, b + 1.2, fy1 + 0.4, z0 - 1.2, z0, "metal"))
        pos = b
    o.append(B(pos, fy0, mx1, fy1, Z_PAILLIS, zf, "bal-maisonnette"))
    a, b = ouv[1][0], ouv[1][1]
    o += [B(a + 0.5, fy0 + 3, b - 0.5, fy0 + 4, Z_PAILLIS, Z_PAILLIS + 49, "bal-maisonnette"),          # porte entrouverte
          B(a + 4, fy0 + 2.6, b - 4, fy0 + 3, Z_PAILLIS + 30, Z_PAILLIS + 38, "metal"),                   # sa petite fenêtre
          B(a + 1, fy1, b - 1, fy1 + 0.5, Z_PAILLIS + 51.5, Z_PAILLIS + 54.5, "blanc"),                   # affiche « Bureau »
          B(a + 3.5, fy1, a + 6, fy1 + 0.5, Z_PAILLIS + 56.5, Z_PAILLIS + 61.5, "metal"),                # « 86 »
          B(a + 7.5, fy1, a + 10, fy1 + 0.5, Z_PAILLIS + 56.5, Z_PAILLIS + 61.5, "metal")]
    o.append(B(mx1 - 0.2, -275, mx1 + 0.3, -258, Z_PAILLIS + 24, Z_PAILLIS + 42, "metal"))              # fenêtre de côté
    for q in range(5):                                     # toit de planches en appentis (débord de 6 po devant)
        ya_ = my1 + 6 - (my1 + 6 - my0 + 2) * (q + 1) / 5
        yb_ = my1 + 6 - (my1 + 6 - my0 + 2) * q / 5
        zq = zf + 1.5 - (zf - zr) * q / 5
        o.append(B(mx0 - 2, ya_, mx1 + 3, yb_, zq - 1.2, zq, "bal-maisonnette"))
    return o


# ------------------------------------------------------------------------------------------------- escalier avant
def escalier():
    o = []
    n = X.ESC_AV_N
    for i in range(1, n):
        xa, xb = X0E + G_ESC * (i - 1), X0E + G_ESC * i
        z = ZB - R_ESC * i
        o += [B(xa, YAE, xa + 5.5, YBE, z - 1.5, z, "bal-neuf"), B(xa + 5.75, YAE, xb + 1, YBE, z - 1.5, z, "bal-neuf"),
              B(xb - 1, YAE + 0.5, xb, YBE - 0.5, z - R_ESC if i < n - 1 else Z_DALLE, z - 1.5, "bal-neuf")]      # contremarche
        for y0, y1 in ((YAE, YAE + 1.5), (YBE - 1.5, YBE), ((YAE + YBE) / 2 - 0.75, (YAE + YBE) / 2 + 0.75)):  # limons
            o.append(B(xa, y0, xb, y1, max(z - 1.5 - 10.5, Z_DALLE), z - 1.5, "bal-neuf"))
    # dalle de béton au pied
    o.append(B(X1E, YAE - 6, X1E + 26, YBE + 6, ZA_ESC - 2, Z_DALLE, "beton"))
    # main courante côté rue (poteaux en haut, au milieu, en bas ; étrier noir en bas), barreaux noirs
    yr = YAE - 1.75
    znez = lambda x: ZB - R_ESC * (x - X0E) / G_ESC
    xm, xbas = (X0E + X1E) / 2, X1E + 2
    o += [B(xm - 1.75, yr - 1.75, xm + 1.75, yr + 1.75, znez(xm) - 12, znez(xm) + H_GC + 1, "bal-neuf"),
          B(xbas - 1.75, yr - 1.75, xbas + 1.75, yr + 1.75, Z_DALLE, Z_DALLE + R_ESC + H_GC + 1, "bal-neuf"),
          B(xbas - 2.4, yr - 2.4, xbas + 2.4, yr + 2.4, Z_DALLE, Z_DALLE + 6, "metal"),
          B(X0E - 3.5, yr - 1.75, X0E, yr + 1.75, ZB + H_GC - 1.5, ZB + H_GC + 1, "bal-main")]
    za_, zb_ = ZB + H_GC, znez(xbas) + H_GC
    o += [T([(X0E - 1.75, yr, za_ + 0.5), (xbas, yr, zb_ + 0.5)], 1.9, "bal-neuf", pans=8),
          T([(X0E, yr, ZB + 4), (xbas - 1.75, yr, znez(xbas) + 4)], 0.9, "bal-neuf", pans=8)]
    L = xbas - X0E
    m = round(L / 4)
    for j in range(1, m):
        x = X0E + L * j / m
        if abs(x - xm) < 2.5:
            continue
        o.append(B(x - 0.375, yr - 0.375, x + 0.375, yr + 0.375, znez(x) + 4.8, znez(x) + H_GC - 1.5, "metal"))
    # lampes solaires sur les poteaux (face vers l'escalier)
    for (x, z) in ((X0E - 1.75, ZB + 30), (xm, znez(xm) + 28), (xbas, Z_DALLE + R_ESC + 28)):
        o += [B(x - 2, yr + 1.75, x + 2, yr + 3.2, z, z + 3.5, "metal"), B(x - 1.4, yr + 3.2, x + 1.4, yr + 3.4, z + 0.6, z + 2.6, "abat-jour")]
    # boîte aux lettres noire sur poteau, à droite du pied de l'escalier
    xb_, yb_ = 404.0, -72.0
    zb = zt(xb_, yb_)
    o += [B(xb_ - 1.75, yb_ - 1.75, xb_ + 1.75, yb_ + 1.75, zb - 6, zb + 42, "bal-neuf"),
          ARR(xb_ - 9, yb_ - 4, xb_ + 9, yb_ + 4, zb + 42, zb + 50, "metal", r=1, b=0.5)]
    return o


# ------------------------------------------------------------------------------------------------- données du contrat
def planchers_balcon():
    pl = [{"nom": "Balcon avant", "pts": rect(XG, YK, XD, 0), "z": ZB},
          {"nom": "Balcon avant (devant le filet, à gauche)", "pts": rect(XF, YAV, FILET[0], YK), "z": ZB},
          {"nom": "Balcon avant (devant le filet)", "pts": rect(FILET[0], YAV, XD, FILET[1]), "z": ZB},
          {"nom": "Balcon avant (derrière le filet)", "pts": rect(FILET[0], FILET[3], XD, YK), "z": ZB},
          {"nom": "Balcon avant (banc du filet)", "pts": rect(FILET[2], FILET[1], XD, FILET[3]), "z": ZB},
          {"nom": "Filet catamaran (on peut s'y étendre)", "pts": rect(*FILET), "z": round(ZB - 3, 2)},
          {"nom": "Plateforme basse", "pts": rect(XP, YAV + 1.2, XF, YK), "z": Z_PLAT}]
    pl += [{"nom": f"Marches du coin des enfants, marche {i}", "pts": rect(XP - 10 * i, -262, XP - 10 * (i - 1), YK - 0.25),
            "z": Z_PLAT - 7.5 * i} for i in range(1, 4)]
    pl.append({"nom": "Paillis du coin des enfants", "pts": rect(XG + 1.2, YAV + 1.2, XP, YK - 0.25), "z": Z_PAILLIS})
    pl += [{"nom": f"Escalier avant, marche {i}", "pts": rect(X0E + G_ESC * (i - 1), YAE, X0E + G_ESC * i, YBE),
            "z": round(ZB - R_ESC * i, 2)} for i in range(1, X.ESC_AV_N)]
    pl.append({"nom": "Dalle au pied de l'escalier avant", "pts": rect(X1E, YAE - 6, X1E + 26, YBE + 6), "z": round(Z_DALLE, 2)})
    return pl


def obstacles_balcon(poteaux):
    ob = [{"nom": "Garde-corps avant du balcon", "pts": rect(XF, YAV, XD, YAV + 3.5)},
          {"nom": "Garde-corps droit du balcon (devant l'escalier, verre teinté)", "pts": rect(XD - 3.5, YAV, XD, YAE)},
          {"nom": "Garde-corps droit du balcon (côté porte)", "pts": rect(XD - 3.5, YBE, XD, 0)},
          {"nom": "Garde-corps du coin des enfants", "pts": rect(XG, YK - 0.25, XP - 5.5, YK + 3.25)},
          {"nom": "Garde-corps à gauche de la maison", "pts": rect(XG, -3.5, 0, 0)},
          {"nom": "Écran d'intimité (voisin de gauche)", "pts": rect(XG, YK, XG + 2.2, 0)},
          {"nom": "Clôture du coin des enfants (mur d'escalade)", "pts": rect(XG, YAV, XG + 2.2, YK)},
          {"nom": "Clôture avant du coin des enfants", "pts": rect(XG, YAV, XF, YAV + 2.2)},
          {"nom": "Écran de la plateforme", "pts": rect(XF - 3, YAV, XF + 0.5, -246)},
          {"nom": "BBQ", "pts": rect(XG + 6, -160, XG + 31, -110)},
          {"nom": "Banquette en L", "pts": [[XG + 2, -100], [XG + 31.5, -100], [XG + 31.5, -36], [46, -36], [46, -3], [XG + 2, -3]]},
          {"nom": "Maisonnette « 86 »", "pts": rect(XG, YAV, XG + 62, -245)},
          {"nom": "Carré de sable", "pts": [[XG, YK - 0.25], [-34.5, YK - 0.25], [-34.5, -224.6], [-47.4, -237.5], [XG, -237.5]]},
          {"nom": "Glissade", "pts": rect(XP - 55, -284.2, XP, -265.8)},
          {"nom": "Main courante de l'escalier avant", "pts": rect(X0E - 3.5, YAE - 3.5, X1E + 4, YAE)},
          {"nom": "Boîte aux lettres", "pts": rect(400, -76, 408, -68)}]
    for xc in PERGOLA_X:
        for yc in PERGOLA_Y:
            ob.append({"nom": "Poteau de la pergola", "pts": rect(xc - 3.2, yc - 3.2, xc + 3.2, yc + 3.2)})
    return ob


VISITES = [
    {"nom": "Balcon avant — vue sur le fleuve", "x": 150, "y": -40, "cap": 288, "z": ZB},
    {"nom": "Filet catamaran", "x": 205, "y": -196, "cap": 228, "z": ZB},
    {"nom": "Coin des enfants", "x": 34, "y": -166, "cap": 218, "z": ZB},
    {"nom": "Escalier avant (de la rue)", "x": 446, "y": -112, "cap": 194, "z": None},
]


def _retirer_perron(EXT):
    """Retire le perron de béton du relevé (objets identiques à exterieur.perron_avant(), planchers, garde-corps, trou)."""
    cle = lambda o: json.dumps(o, sort_keys=True)
    perron = {cle(o) for o in X.perron_avant()}
    n0 = len(EXT["objets"])
    EXT["objets"] = [o for o in EXT["objets"] if cle(o) not in perron]
    if n0 - len(EXT["objets"]) < len(perron) - 2:
        raise SystemExit("balcon_avant.py : le perron de béton n'a pas été retrouvé dans les objets de l'extérieur")
    EXT["planchers"] = [p for p in EXT["planchers"] if not (p["nom"] == "Perron avant" or p["nom"].startswith("Marches du perron"))]
    EXT["obstacles"] = [o for o in EXT["obstacles"] if not o["nom"].startswith("Garde-corps du perron")]
    plein = rect(*X.PERRON_PLEIN)
    EXT["trous"] = [t for t in EXT["trous"] if t != plein]


ARBRE_AVANT = (-45.0, -360.0, 380.0)     # feuillu entre le coin des enfants et la rue (ses branches passent au-dessus, photos 01, 04, 06)


def _deplacer_arbre(EXT):
    """Le petit arbre ornemental de exterieur.py (x -60, y -250) tombe dans le coin des enfants : il est retiré et remplacé par
    le feuillu des photos, devant la clôture côté rue."""
    EXT["objets"] = [o for o in EXT["objets"] if not (o.get("x") == -60 and o.get("y") == -250 and o.get("forme") in ("cylindre", "sphere"))]
    EXT["obstacles"] = [o for o in EXT["obstacles"] if o["nom"] != "Arbre ornemental (tronc)"]
    x, y, H = ARBRE_AVANT
    z = zt(x, y)
    EXT["objets"] += [C(x, y, 8, z, z + 0.45 * H, "bois_brut", pans=10),
                      SPH(x, y, z + 0.58 * H, 0.28 * H, "ext-feuillage-clair", ecrase=0.8),
                      SPH(x + 0.07 * H, y - 0.05 * H, z + 0.8 * H, 0.21 * H, "ext-feuillage", ecrase=0.85)]
    EXT["obstacles"].append({"nom": "Arbre devant le coin des enfants (tronc)", "pts": X.cercle(x, y, 10, 12)})


def appliquer_exterieur(EXT):
    _retirer_perron(EXT)
    _deplacer_arbre(EXT)
    struct, poteaux = plancher()
    EXT["objets"] += (struct + garde_corps_balcon() + ecrans() + pergola() + bbq() + banquette() + filet() + coin_enfants()
                      + escalier())
    EXT["planchers"] += planchers_balcon()
    EXT["obstacles"] += obstacles_balcon(poteaux)
    for v in VISITES:
        v = dict(v)
        if v["z"] is None:
            v["z"] = round(zt(v["x"], v["y"]), 1)
        EXT["visites"].append(v)
    EXT["peintures"] = dict(EXT.get("peintures") or {}, **PEINTURES)
    EXT["palette"] = list(EXT.get("palette") or []) + PALETTE
    return EXT
