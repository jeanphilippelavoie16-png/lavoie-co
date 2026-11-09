"""MAISON-18 — balcon avant EXISTANT (photos du client, 2026-11-02), intégré à la visite extérieure.

Le client : « Voici mon balcon avant, intègre-le à la visite. » ; il est devant la façade (la porte d'entrée sort dessus), « 24 pi
jusqu'à la rue » et « il termine juste un peu à côté de la porte (à droite de la porte d'entrée quand tu regardes d'en avant) » ;
« Il est comme surélevé. Le filet noir sur le balcon c'est un filet katamaran pour lire. » Puis, sur son croquis (« ça ressemble
plus à ça, le setup ») : le balcon est un grand rectangle, le filet est dans un coin du balcon, le coin des enfants (« jeu ») est
EN DEHORS du rectangle, devant, avec un coin coupé en biais ; « Les marches sont à 6 pieds du mur de la maison » ; et « Yé où ton
four à pizza ?? » (photos 17 à 20 : cuisine d'extérieur sous la pergola). On reproduit l'existant (pas un nouveau design).
Puis, en rouge sur le croquis du dessus (3e version) : « le filet est plus cette grosseur-là et les poutres en bois vont presque
jusqu'à la maison, le patio doit avoir 20 de large finalement et les poutres en bois font 16 à partir de gauche et arrêtent à
4 pieds de la maison, avec celui du milieu dans le milieu » : balcon de 20 pi de la façade au bord avant ; poutres de la pergola
de 16 pi, du bord avant jusqu'à 4 pi de la maison, poteaux du milieu au centre ; filet ≈ 9'-5" × 10'-0" (rectangle rouge).
Puis (4e version) : « pi le meuble avec le four à pizza fait toute la longueur des poutres (20') », corrigé aussitôt : « je voulais
dire quelle faisais 16 pied le meuble pas 20 pieds » : meuble de cuisine de 16'-0", du bord avant aux poteaux à 4 pi de la maison.
Relevé estimé sur 20 photos (DESIGN_balcon_avant.md) : à valider, sauf les mesures du client.

appliquer_exterieur(EXT) (appelé par scene_3d.py après la création de SCENE["exterieur"]) :
- retire le perron de béton du relevé (objets de exterieur.perron_avant(), planchers « Perron avant » et « Marches du perron »,
  garde-corps du perron, trou du perron plein) : le balcon le remplace. L'excroissance de fondation du sous-sol (chambre froide
  sous l'ancien perron) reste, coiffée de sa dalle, sous le balcon ;
- ajoute le balcon (objets, planchers, obstacles), la pergola et sa cuisine d'extérieur, le coin des enfants, l'escalier avant
  (relief creusé dans exterieur.py : ESC_AV, AIRE_AV) et la jardinière, deux petites lampes sous la pergola, les couleurs
  (peintures et légende « Extérieur ») et cinq arrêts de visite.

Repère de exterieur.py (pouces) : x le long de la façade (0 à 456, vers la droite vu de la rue), y vers l'arrière (façade 0, rue
-480), z absolu depuis le plancher du sous-sol (RDC 105).

Plan retenu (vu de dessus, la rue en bas ; le croquis du client est tourné d'un quart de tour : maison à droite, rue à gauche) :
- balcon : TOUT le rectangle, x -90 à 232 (26'-10"), y -240 à 0 (20'-0", client), à 103,5 (1½ po sous le seuil) ;
- pergola contre l'écran du voisin (x -90 à 52) : poutres de 16'-0" du bord avant (y -240) jusqu'à 4'-0" de la maison (y -48),
  trois rangées de poteaux (bord avant, milieu y -144, à 4 pi de la maison) (client) ; toit de polycarbonate ondulé sur chevrons
  au-dessus de la cuisine, guirlandes d'ampoules ; cuisine d'extérieur le long de l'écran, meuble de 16'-0" sur toute la
  longueur des poutres (client) : comptoir haut de 10'-0" avec four à pizza, frigo à boissons et bacs à condiments ; comptoir
  bas de 6'-0" avec BBQ encastré et plaque de cuisson (sa tablette dépasse le bout) ; sofa, table basse,
  2 fauteuils, 2 poufs entre la cuisine et le passage ;
- filet catamaran ≈ 9'-5" × 10'-0" (113 po vers la maison sur 120 le long de la façade, rectangle rouge du client) au coin avant
  côté allée, banc de planche le long du garde-corps droit, 3 coussins ;
- coin des enfants DEVANT le balcon (y -240 à -360), le long de la moitié côté voisin (x -90 à 112), coin avant côté allée
  coupé en biais ; plateforme basse (une marche) x 52 à 112, trois marches et une glissade jusqu'au paillis (66) ;
  maisonnette « 86 », carré de sable, mur d'escalade sur la clôture du voisin ;
- escalier avant de bois neuf : du côté droit du balcon, à 6'-0" du mur (y -120 à -72), 15 contremarches de 7,55 po et 14
  girons de 11 po vers l'allée, jusqu'à l'asphalte ; main courante côté rue, lampes solaires ; entre l'escalier et le mur, la
  jardinière de cèdre en gradins et la boîte aux lettres noire posée dessus.
"""
import importlib.util
import json
import math
import os

from shapely.geometry import Polygon as _Poly

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
YAV = -240.0                    # devant du balcon (20 pi de la façade, client) sur toute la largeur
XP, XF = 52.0, 112.0            # face des poteaux intérieurs de la pergola = bord gauche de la plateforme ; boîte d'écran (bord droit)
Z_PLAT = ZB - 7.5               # plateforme basse (une marche)
Z_PAILLIS = Z_PLAT - 4 * 7.5    # paillis du coin des enfants : trois marches et une contremarche sous la plateforme (66)
# filet catamaran (rectangle rouge du client, ≈ 9'-5" vers la maison sur 10'-0" le long de la façade) : au coin avant côté
# allée, à 10 po du bord avant (rive et cadre), contre le banc du garde-corps droit ; il finit vis-à-vis du haut de l'escalier
FILET = (93.5, YAV + 10.0, 213.5, YAV + 123.0)
# coin des enfants, devant le balcon (10'-0" de profond à partir du bord avant) : clôture du voisin x -90, clôture côté rue
# y -360 (x -90 à -14), biais de (-14, -360) à (112, -276), petit retour le long de la plateforme de (112, -276) au balcon
YR, XC, YJ = YAV - 120.0, -14.0, YAV - 36.0
COIN = [(XG, YAV), (XG, YR), (XC, YR), (XF, YJ), (XF, YAV)]
X0E, YAE, X1E, YBE = X.ESC_AV                 # escalier avant (exterieur.py)
ZA_ESC = X.z_allee((YAE + YBE) / 2)           # asphalte au pied
R_ESC = (ZB - ZA_ESC) / X.ESC_AV_N            # hauteur de contremarche (7,55)
G_ESC = (X1E - X0E) / (X.ESC_AV_N - 1)        # giron (11)
Z_DALLE = ZA_ESC + 2.0                        # dalle de béton au pied de l'escalier
H_GC = 36.0                                   # garde-corps
# pergola : poteaux 6 × 6 (rangée intérieure x 49,25 ; rangée dans l'écran x -87,25) ; poutres de 16'-0" du bord avant (y -240)
# jusqu'à 4'-0" de la maison (y -48), client ; trois rangées de poteaux : au bord avant, au milieu (y -144), à 4 pi de la maison
PERGOLA_X = (XP - 2.75, XG + 2.75)
PERGOLA_Y0, PERGOLA_Y1 = YAV, -48.0
PERGOLA_Y = (PERGOLA_Y0 + 2.75, (PERGOLA_Y0 + PERGOLA_Y1) / 2, PERGOLA_Y1 - 2.75)
ZH = ZB + 88                                  # dessous des poutres (7'-4" sur le balcon), poutres 5½ × 7½
# cuisine d'extérieur le long de l'écran, sous la pergola : le meuble fait 16'-0", toute la longueur des poutres (client,
# 4e version), du bord avant (y -240 : son bout en cascade est contre le poteau avant, le garde-corps avant bute dessus, photos
# 18, 19) jusqu'à la rangée de poteaux à 4 pi de la maison (y -48). Les poteaux de la rangée de l'écran (x -90 à -84,5) sont
# derrière son dos (x -84) : il passe devant eux. Profondeur x -84 à -56 (dessus jusqu'à -55). (y0, y1, dessus)
CU_X0, CU_X1 = -84.0, -56.0
CU_Y0, CU_Y1 = YAV, PERGOLA_Y1                          # 16'-0" (client)
CU_HAUT = (CU_Y0, CU_Y0 + 120.0, ZB + 36)               # comptoir haut 10'-0" : four à pizza, frigo, bacs (photos 17 à 19)
CU_BAS = (CU_HAUT[1], CU_Y1, ZB + 26)                   # comptoir bas 6'-0" : BBQ et plaque, collés (photos 18, 20)
# modules, de la rue vers la maison (photos 17 à 20 ; frigo, BBQ et plaque comme étalons)
CU_FOUR = (-70.0, CU_Y0 + 26.0, 13.0)                   # four à pizza (dôme de 26 po) : centre x, y et rayon
CU_FRIGO = (CU_Y0 + 58.0, CU_Y0 + 81.0)                 # frigo à boissons à porte vitrée (23 po), un peu passé le milieu
CU_BACS = CU_Y0 + 75.0                                  # 6 bacs à condiments au fond (et 2 devant) jusqu'au bout côté maison
CU_BBQ = (CU_BAS[0] + 1.5, CU_BAS[0] + 29.5)            # BBQ encastré 3 brûleurs (28 po), contre le comptoir haut
CU_PLAQUE = (CU_BBQ[1] + 1.5, CU_BAS[1] - 2.0)          # plaque de cuisson 4 brûleurs (39 po), au bout du meuble
CU_TABLETTE = (CU_PLAQUE[1], CU_PLAQUE[1] + 15.0)       # sa tablette dépasse le bout du meuble, à côté du poteau (photo 20)
# salon entre la cuisine et le passage (mêmes dégagements qu'avant, par rapport au bord avant) : sofa dos au garde-corps avant,
# table basse, 2 fauteuils face au sofa, 2 poufs ; (x0, x1, y0, y1)
SOFA = (-36.0, 42.0, YAV + 4.0, YAV + 35.0)
TABLE = (-20.0, 24.0, YAV + 47.0, YAV + 71.0)
FAUTEUILS = [(-34.0, -6.0, YAV + 88.0, YAV + 117.0), (6.0, 34.0, YAV + 88.0, YAV + 117.0)]
POUFS = [(27.0, 44.5, YAV + 42.0, YAV + 61.0), (27.0, 44.5, YAV + 64.0, YAV + 83.0)]

PEINTURES = {
    "Pin naturel du balcon": ["#AD967F", "planches du balcon avant (pin naturel grisonné)", "bal-planche"],
    "Cadres teints foncés": ["#3A332D", "bandes qui encadrent le filet et divisent le plancher ; rives, solives, poutres et poteaux sous le balcon", "bal-cadre"],
    "Bois teint (pergola)": ["#6E4C33", "poteaux, poutres et chevrons de la pergola", "bal-teint"],
    "Bois naturel (mains courantes)": ["#B8895E", "mains courantes, poteaux de garde-corps, banc du filet, plateforme et marches", "bal-main"],
    "Écran à planches horizontales": ["#966843", "écrans d'intimité et clôtures du coin des enfants", "bal-ecran"],
    "Bois neuf (escalier avant)": ["#CBA36F", "escalier avant neuf : girons, contremarches, limons, main courante", "bal-neuf"],
    "Filet catamaran noir": ["#121212", "filet tendu dans l'ouverture du plancher", "bal-filet"],
    "Coussins noirs (filet)": ["#1E1E20", "coussins du filet catamaran", "bal-coussin-noir"],
    "Coussins gris foncé": ["#5A5E63", "dossiers des fauteuils", "bal-coussin"],
    "Coussins gris pâle": ["#C9CBCA", "sofa et assises des fauteuils (cadres d'aluminium noir)", "bal-coussin-pale"],
    "Poufs blancs": ["#EFEEEA", "poufs (cadres blancs, dessus rembourré)", "bal-pouf"],
    "Bois de la table basse": ["#A97C50", "dessus de la table basse, accoudoirs de bois", "bal-teck"],
    "Microciment gris": ["#A7A8A4", "comptoirs de la cuisine d'extérieur (béton gris lissé)", "bal-microciment"],
    "Lattes teintes foncées": ["#3D2B21", "façades à lattes horizontales de la cuisine d'extérieur", "bal-lattes"],
    "Crème (four à pizza)": ["#E4DAC3", "dôme du four à pizza", "bal-creme"],
    "Cèdre de la jardinière": ["#A6643D", "jardinière en gradins le long de l'escalier avant (planches horizontales)", "bal-cedre"],
    "Terre de la jardinière": ["#4B3B2E", "terre de la jardinière", "bal-terre"],
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
    ["Pergola de bois teint", "poteaux 6 × 6, poutres, chevrons ; toit de polycarbonate ondulé translucide au-dessus de la cuisine ; guirlandes d'ampoules", "#6E4C33"],
    ["Cuisine d'extérieur", "meuble de 16 pi (toute la longueur de la pergola) : comptoirs de microciment gris, façades à lattes de bois teint foncé, frigo à porte vitrée noire, four à pizza crème, BBQ et plaque de cuisson", "#A7A8A4"],
    ["Mobilier de détente", "sofa 3 places et 2 fauteuils (aluminium noir, coussins gris), table basse à dessus de bois, 2 poufs blancs", "#C9CBCA"],
    ["Garde-corps du balcon", "main courante et poteaux de bois naturel, barreaux noirs ; un panneau de verre teinté à droite", "#B8895E"],
    ["Écrans d'intimité", "planches horizontales teintes à jours sur montants d'acier noir (voisin de gauche, coin des enfants)", "#966843"],
    ["Filet catamaran", "maille noire tendue dans le plancher, coussins noirs", "#121212"],
    ["Escalier avant neuf", "15 contremarches de bois neuf, main courante côté rue, lampes solaires", "#CBA36F"],
    ["Jardinière de cèdre", "en gradins entre l'escalier avant et le mur, boîte aux lettres noire dessus", "#A6643D"],
    ["Coin des enfants", "paillis de cèdre, carré de sable, glissade bleue, maisonnette « 86 », mur d'escalade", "#6B3B23"],
]


def zt(x, y):
    return X._zg(x, y)


def zmin(pts, n=4):
    """Terrain le plus bas le long d'un contour (points et intermédiaires)."""
    out = []
    for (xa, ya), (xb, yb) in zip(pts, pts[1:] + pts[:1]):
        out += [zt(xa + (xb - xa) * k / n, ya + (yb - ya) * k / n) for k in range(n)]
    return min(out)


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


def ecran(a, b, z0, z1, montants, cote=1, mat="bal-ecran", jeu=0.75):
    """Écran d'intimité le long de x ou de y : planches horizontales de 5½ po (jours de « jeu » po) sur montants d'acier noir
    1½ po (positions depuis le bout de plus petite coordonnée, du côté « cote » : +1 vers +x ou +y)."""
    (xa, ya), (xb, yb) = a, b
    enx = abs(xb - xa) > abs(yb - ya)
    out, z = [], z0
    while z < z1 - 0.5:
        zz = min(z + 5.5, z1)
        out.append(B(xa, ya - 0.6, xb, ya + 0.6, z, zz, mat) if enx else B(xa - 0.6, ya, xa + 0.6, yb, z, zz, mat))
        z = zz + jeu
    for s in montants:
        if enx:
            x = min(xa, xb) + s
            out.append(B(x - 0.75, ya + cote * 0.6, x + 0.75, ya + cote * 2.1, z0, z1, "metal"))
        else:
            y = min(ya, yb) + s
            out.append(B(xa + cote * 0.6, y - 0.75, xa + cote * 2.1, y + 0.75, z0, z1, "metal"))
    return out


def ecran_biais(a, b, z0, z1, pas=48.0, mat="bal-ecran", jeu=0.75):
    """Écran d'intimité sur un tracé oblique (planches en prismes minces), montants d'acier noir du côté gauche de a -> b."""
    (xa, ya), (xb, yb) = a, b
    L = math.hypot(xb - xa, yb - ya)
    ux, uy = (xb - xa) / L, (yb - ya) / L
    nx, ny = -uy, ux                                       # à gauche du tracé (dedans du coin des enfants)
    q = lambda s, d: (xa + ux * s + nx * d, ya + uy * s + ny * d)
    out, z = [], z0
    while z < z1 - 0.5:
        zz = min(z + 5.5, z1)
        out.append(P([q(0, -0.6), q(L, -0.6), q(L, 0.6), q(0, 0.6)], z, zz, mat))
        z = zz + jeu
    n = max(1, round(L / pas))
    for k in range(n + 1):
        s = min(max(L * k / n, 1.0), L - 1.0)
        out.append(P([q(s - 0.75, 0.6), q(s + 0.75, 0.6), q(s + 0.75, 2.1), q(s - 0.75, 2.1)], z0, z1, "metal"))
    return out


def chapeau(a, b, z, mat="bal-main"):
    """Chapeau de 2 × 6 à plat sur une clôture (tracé quelconque)."""
    (xa, ya), (xb, yb) = a, b
    L = math.hypot(xb - xa, yb - ya)
    nx, ny = -(yb - ya) / L * 2.75, (xb - xa) / L * 2.75
    return P([(xa - nx, ya - ny), (xb - nx, yb - ny), (xb + nx, yb + ny), (xa + nx, ya + ny)], z, z + 1.5, mat)


# ------------------------------------------------------------------------------------------------- plancher, structure
def plancher():
    """Planches de pin naturel en panneaux de sens alternés, bandes teintes foncées (rives, alignement des poteaux de la
    pergola, rangée du milieu, cadre du filet et bande vers la porte), fond sombre dans les joints ; rives, solives, poutres et
    poteaux teints foncés dessous."""
    o = []
    z1 = ZB
    fx0, fy0, fx1, fy1 = FILET
    cad = lambda x0, y0, x1, y1: B(x0, y0, x1, y1, z1 - 1, z1, "bal-cadre")
    ym0, ym1 = PERGOLA_Y[1] - 2.75, PERGOLA_Y[1] + 2.75
    # fond des joints (pas sous le filet)
    for r in [(XG, YAV, fx0, 0), (fx0, fy1, XD, 0), (fx0, YAV, XD, fy0), (fx1, fy0, XD, fy1)]:
        o.append(B(*r, z1 - 1.6, z1 - 1, "bal-cadre"))
    # bandes teintes foncées : rives (devant, droite, gauche, derrière), poteaux de la pergola, rangée du milieu, filet
    for r in [(XG, YAV, XD, YAV + 5.5), (XD - 5.5, YAV + 5.5, XD, 0), (XG, YAV + 5.5, XG + 5.5, 0), (XG + 5.5, -5.5, XD - 5.5, 0),
              (XP - 5.5, YAV + 5.5, XP, -5.5), (XG + 5.5, ym0, XP - 5.5, ym1), (XP, ym0, fx0 - 5.5, ym1),
              (fx0 - 5.5, YAV + 5.5, fx0, -5.5), (fx0, fy0 - 4.5, fx1, fy0), (fx0, fy1, XD - 5.5, fy1 + 5.5)]:
        o.append(cad(*r))
    # panneaux de planches (sens alternés)
    o += planches(XG + 5.5, YAV + 5.5, XP - 5.5, ym0, "y", z1)            # sous la pergola, devant
    o += planches(XG + 5.5, ym1, XP - 5.5, -5.5, "x", z1)                 # sous la pergola et vers la maison
    o += planches(XP, YAV + 5.5, fx0 - 5.5, ym0, "x", z1)                 # passage vers la plateforme
    o += planches(XP, ym1, fx0 - 5.5, -5.5, "y", z1)
    o += planches(fx0, fy1 + 5.5, XD - 5.5, -5.5, "y", z1)                # devant la porte et le long du garde-corps droit
    o += planches(fx1, fy0, XD - 5.5, fy1, "y", z1)                       # sous le banc
    # rives (2 × 10 doubles), solives 2 × 8 à 16 po, poutres triples 2 × 10, poteaux 6 × 6 et étriers noirs
    zr0, zs0 = z1 - 1 - 9.25, z1 - 1 - 7.25
    for r in [(XD - 3, YAV, XD, 0), (XG, YAV, XD, YAV + 3), (XG, YAV, XG + 3, 0), (XG, -3, XD, 0)]:
        o.append(B(*r, zr0, z1 - 1, "bal-cadre"))
    x = XG + 16
    while x < XD - 4:
        if fx0 - 3 < x < fx1 + 3:                   # solives coupées par l'ouverture du filet (chevêtres)
            o += [B(x - 0.75, YAV + 3, x + 0.75, fy0 - 3, zs0, z1 - 1, "bal-cadre"), B(x - 0.75, fy1 + 3, x + 0.75, -3, zs0, z1 - 1, "bal-cadre")]
        else:
            o.append(B(x - 0.75, YAV + 3, x + 0.75, -3, zs0, z1 - 1, "bal-cadre"))
        x += 16
    o += [B(fx0 - 3, fy0 - 3, fx1 + 3, fy0, zs0, z1 - 1, "bal-cadre"), B(fx0 - 3, fy1, fx1 + 3, fy1 + 3, zs0, z1 - 1, "bal-cadre"),
          B(fx0 - 3, fy0, fx0, fy1, zs0, z1 - 1, "bal-cadre"), B(fx1, fy0, fx1 + 3, fy1, zs0, z1 - 1, "bal-cadre")]
    zp1 = zs0
    zp0 = zp1 - 9.25
    poteaux = []
    xs = (XG + 2.75, -20.0, XP - 2.75, XF, 172.0, XD - 2.75)
    for yb in (YAV + 5.75, -156.0, -78.0):                  # trois poutres (≈ 6'-6" c/c)
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
    # devant, côté voisin : du bout en cascade de la cuisine (au bord avant, contre le poteau avant de l'écran) au poteau avant
    # de la pergola, au-dessus du coin des enfants (photos 18, 19 : le garde-corps bute sur le bout du comptoir haut)
    xg0 = CU_X1 + 1
    o += garde_corps((xg0, YAV + 1.75), (XP - 5.5, YAV + 1.75), ZB, montants=((XP - 5.5 - xg0) / 2,))
    # devant, partie du filet : de la boîte d'écran au coin droit
    o += garde_corps((XF, YAV + 1.75), (XD, YAV + 1.75), ZB, montants=(60,))
    # côté droit : du coin avant à l'escalier (verre teinté juste devant l'escalier), puis de l'escalier au mur (côté porte)
    o += garde_corps((XD - 1.75, YAV), (XD - 1.75, YAE), ZB, montants=(YAE - YAV - 48,), verre=(YAE - YAV - 48, YAE - YAV))
    o += garde_corps((XD - 1.75, YBE), (XD - 1.75, 0), ZB, montants=(36,))
    # derrière, à gauche de la maison (du coin de l'écran au coin de la maison)
    o += garde_corps((XG + 1.5, -1.75), (0, -1.75), ZB, montants=())
    return o


def ecrans():
    o = []
    # écran du voisin de gauche, sur le balcon (7'-2", jusque sous les poutres de la pergola), sur toute la profondeur ; jours
    # de 1 po, montants et lisse haute d'acier noir (photos 19, 20)
    o += ecran((XG + 0.6, YAV), (XG + 0.6, -4), ZB, ZB + 86, montants=(3, 50, 100, 150, 200, -4 - YAV - 3), cote=1, jeu=1.0)
    o.append(B(XG - 0.2, YAV, XG + 2.1, -4, ZB + 86, ZB + 87.5, "metal"))
    # clôtures du coin des enfants (dessus à 144, 6'-6" au-dessus du paillis ; jusqu'au terrain) : voisin (mur d'escalade),
    # rue, biais, petit retour le long de la plateforme ; chapeaux de 2 × 6
    zb = zmin(COIN) - 3
    o += ecran((XG + 0.6, YR), (XG + 0.6, YAV), zb, 144, montants=(2, 40, 80, 118), cote=1)
    o += ecran((XG, YR + 0.6), (XC, YR + 0.6), zb, 144, montants=(2, 38, 74), cote=1)
    o += ecran_biais((XC, YR), (XF, YJ), zb, 144)
    o += ecran((XF - 0.6, YJ), (XF - 0.6, YAV - 2.75), zb, 144, montants=(2, 33), cote=-1)
    o += [chapeau((XG, YR), (XG, YAV), 144), chapeau((XG, YR), (XC, YR), 144), chapeau((XC, YR), (XF, YJ), 144),
          chapeau((XF, YJ), (XF, YAV - 2.75), 144)]
    # boîte d'écran (poteau habillé) au bout du garde-corps du filet, au coin de la plateforme
    o += [B(XF - 2.75, YAV - 2.75, XF + 2.75, YAV + 2.75, zt(XF, YAV) - 2, 145, "bal-ecran"),
          B(XF - 3.5, YAV - 3.5, XF + 3.5, YAV + 3.5, 145, 146.5, "bal-main")]
    return o


# ------------------------------------------------------------------------------------------------- pergola
def guirlande(a, b, z, fleche=5.0, pas=12.0):
    """Guirlande d'ampoules (style Edison) entre deux points d'accroche à la hauteur z : fil noir en chaînette, douilles noires,
    ampoules chaudes aux « pas » po."""
    (xa, ya), (xb, yb) = a, b
    L = math.hypot(xb - xa, yb - ya)
    zf = lambda t: z - fleche * 4 * t * (1 - t)
    o = [T([(xa + (xb - xa) * k / 8, ya + (yb - ya) * k / 8, zf(k / 8)) for k in range(9)], 0.15, "metal", pans=4)]
    n = max(1, int(L // pas))
    for k in range(1, n + 1):
        t = (k - 0.5) / n
        x, y, zz = xa + (xb - xa) * t, ya + (yb - ya) * t, zf(t)
        o += [C(round(x, 2), round(y, 2), 0.45, zz - 2.2, zz, "metal", pans=8),
              SPH(x, y, zz - 3.6, 1.05, "abat-jour", ecrase=1.35)]
    return o


def pergola():
    o = []
    zh = ZH
    y0, y1 = PERGOLA_Y0, PERGOLA_Y1                       # poutres de 16'-0" (client)
    for xc in PERGOLA_X:
        for yc in PERGOLA_Y:
            o += [B(xc - 2.75, yc - 2.75, xc + 2.75, yc + 2.75, ZB, zh, "bal-teint"),
                  B(xc - 3.2, yc - 3.2, xc + 3.2, yc + 3.2, ZB, ZB + 5, "metal")]               # étrier noir
            o += [B(xc + 2.75, yc - 4, xc + 3.05, yc + 4, zh - 10, zh + 6, "metal"),               # plaques en T noires
                  B(xc - 3.05, yc - 4, xc - 2.75, yc + 4, zh - 10, zh + 6, "metal")]
        o.append(B(xc - 2.75, y0, xc + 2.75, y1, zh, zh + 7.5, "bal-teint"))                 # poutres le long de y
    for yc in PERGOLA_Y:
        o.append(B(XG - 3, yc - 2.75, XP + 4, yc + 2.75, zh, zh + 7.5, "bal-teint"))        # poutres le long de x
        o.append(B(XP - 7, yc - 3.05, XP + 1, yc + 3.05, zh + 1, zh + 6.5, "metal"))         # plaque en T sur le dessus
    # toit de polycarbonate ondulé translucide sur chevrons, au-dessus de la cuisine (de l'écran à x -26)
    for xr in (-84.0, -66.0, -48.0, -30.0):
        o.append(B(xr - 0.75, y0, xr + 0.75, y1, zh + 7.5, zh + 11, "bal-teint"))
    o.append(B(XG - 2, y0 - 1, -26, y1 + 1, zh + 11, zh + 11.3, "verre-clair"))
    y = y0
    while y < y1:
        o.append(B(XG - 2, y + 1.1, -26, y + 1.7, zh + 11.3, zh + 11.9, "verre-clair"))      # ondes du polycarbonate
        y += 2.7 * 2
    # guirlandes d'ampoules sous les poutres et en travers de la travée avant
    zg = zh - 0.5
    xi, xe = XP - 6, XG + 6
    for yc in PERGOLA_Y:
        o += guirlande((xi, yc), (xe, yc), zg)
    o += guirlande((XP - 9, PERGOLA_Y[0] + 4), (XP - 9, PERGOLA_Y[-1] - 4), zg, fleche=7)
    o += guirlande((xi, PERGOLA_Y[0] + 4), (xe, PERGOLA_Y[1] - 4), zg, fleche=8)
    o += guirlande((xe, PERGOLA_Y[0] + 4), (xi, PERGOLA_Y[1] - 4), zg, fleche=8)
    return o


LUMIERES = [{"x": -18.0, "y": -190.0, "z": round(ZH - 6, 1), "i": 2.5},          # guirlandes : deux lampes réelles seulement
            {"x": -18.0, "y": -98.0, "z": round(ZH - 6, 1), "i": 2.5}]


# ------------------------------------------------------------------------------------------------- cuisine d'extérieur
def lattes(xf, ya, yb, z0, z1):
    """Façade à lattes horizontales de bois teint foncé (lattes de 1½ po, jours de ½ po, fond noir) dans le plan x = xf."""
    o = [B(xf - 1.6, ya, xf - 0.8, yb, z0, z1, "metal")]
    z = z0 + 0.25
    while z < z1 - 0.5:
        o.append(B(xf - 0.8, ya, xf, yb, z, min(z + 1.5, z1), "bal-lattes"))
        z += 2.0
    return o


def cuisine():
    """Cuisine d'extérieur bâtie le long de l'écran (photos 17 à 20) : comptoir haut de microciment (bouts en cascade), façades
    à lattes, frigo à boissons à porte vitrée noire, bacs à condiments d'inox, four à pizza (dôme crème, socle noir) ; comptoir
    plus bas avec le BBQ encastré (3 brûleurs) et la plaque de cuisson noire à tablette latérale ; bacs à fleurs noirs sur
    l'écran."""
    o = []
    xa, xb = CU_X0, CU_X1
    # comptoir haut (10'-0", du bord avant)
    ya, yb, zc = CU_HAUT
    o += [B(xa, ya, xb + 1, yb, zc - 2.5, zc, "bal-microciment"),                         # dessus
          B(xa, ya, xb + 1, ya + 3, ZB, zc - 2.5, "bal-microciment"),                      # bout en cascade (côté rue)
          B(xa, yb - 3, xb + 1, yb, ZB, zc - 2.5, "bal-microciment"),                      # bout côté maison
          B(xa, ya + 3, xb - 2, yb - 3, ZB, ZB + 1, "metal"),                              # socle en retrait
          B(xa, ya + 3, xa + 1, yb - 3, ZB, zc - 2.5, "bal-microciment")]                  # dos
    yfr0, yfr1 = CU_FRIGO                                                                # frigo à boissons (23 po)
    # façades à lattes : grand panneau sous le four, bande étroite contre le frigo, panneau côté maison (photo 19)
    o += lattes(xb, ya + 3, yfr0 - 9.0, ZB + 1, zc - 2.5) + lattes(xb, yfr0 - 8.6, yfr0, ZB + 1, zc - 2.5)
    o += lattes(xb, yfr1, yb - 3, ZB + 1, zc - 2.5)
    o += [B(xb - 1.2, yfr0, xb - 0.2, yfr1, ZB + 1.5, zc - 3, "ecran"),                   # porte vitrée noire
          B(xb - 1.6, yfr0 - 0.4, xb - 1.0, yfr1 + 0.4, ZB + 1, zc - 2.5, "metal"),
          B(xb - 0.2, yfr1 - 1.8, xb + 0.4, yfr1 - 1.0, ZB + 18, ZB + 30, "inox")]          # poignée
    # bacs à condiments encastrés (inox) : 6 au fond, 2 devant, au bout côté maison
    for k in range(6):
        y = CU_BACS + k * 6.8
        o += [B(-79, y, -73, y + 6, zc - 0.05, zc + 0.15, "inox"), B(-78.2, y + 0.8, -73.8, y + 5.2, zc + 0.15, zc + 0.2, "metal")]
    for k in range(2):
        y = CU_BACS + 26.0 + k * 6.8
        o += [B(-70, y, -64, y + 6, zc - 0.05, zc + 0.15, "inox"), B(-69.2, y + 0.8, -64.8, y + 5.2, zc + 0.15, zc + 0.2, "metal")]
    # four à pizza (dôme crème sur socle noir, style « dôme », sans logo), bouche vers l'avant (+x)
    cx, cy, _ = CU_FOUR
    o += [C(cx, cy, 12.5, zc, zc + 4, "metal", pans=24),                                  # socle noir
          C(cx, cy, 13.0, zc + 4, zc + 5, "metal", pans=24),
          SPH(cx, cy, zc + 5, 13.0, "bal-creme", ecrase=0.85),                             # dôme
          B(cx + 9.5, cy - 7.5, cx + 13.4, cy + 7.5, zc + 5, zc + 11.5, "metal"),          # bouche (cadre noir)
          B(cx + 10.5, cy - 6, cx + 13.6, cy + 6, zc + 6, zc + 10.5, "ecran"),
          C(cx - 3, cy, 2.6, zc + 15, zc + 22, "metal", pans=16),                          # cheminée
          C(cx - 3, cy, 3.2, zc + 22, zc + 23, "metal", pans=16),
          B(cx + 12.5, cy - 3.5, cx + 13.8, cy + 3.5, zc + 1, zc + 3.5, "metal")]          # commande
    # pelles à pizza accrochées à l'écran, bacs à fleurs noirs sur l'écran (photo 17)
    o += [B(XG + 2.3, cy, XG + 2.8, cy + 10, ZB + 44, ZB + 56, "inox"), B(XG + 2.3, cy + 4, XG + 2.8, cy + 6, ZB + 56, ZB + 72, "gris"),
          B(XG + 2.3, cy + 13, XG + 2.8, cy + 22, ZB + 46, ZB + 57, "inox"), B(XG + 2.3, cy + 16.5, XG + 2.8, cy + 18.5, ZB + 57, ZB + 73, "gris")]
    for (ya_, z_) in ((cy + 26, ZB + 66), (cy + 38, ZB + 54), (cy + 26, ZB + 42)):
        o += [B(XG + 2.3, ya_, XG + 8.5, ya_ + 14, z_, z_ + 5.5, "metal"), B(XG + 3, ya_ + 1, XG + 7.8, ya_ + 13, z_ + 5.5, z_ + 8, "plante")]
    # comptoir bas (6'-0", jusqu'aux poteaux à 4 pi de la maison)
    ya, yb, zc = CU_BAS
    o += [B(xa, ya, xb + 1, yb, zc - 2.5, zc, "bal-microciment"),
          B(xa, yb - 3, xb + 1, yb, ZB, zc - 2.5, "bal-microciment"),
          B(xa, ya, xb - 2, yb - 3, ZB, ZB + 1, "metal")]
    o += lattes(xb, ya + 0.5, yb - 3, ZB + 1, zc - 2.5)
    # BBQ encastré 3 brûleurs (inox et noir)
    q0, q1 = CU_BBQ
    o += [B(-82, q0, -61, q1, zc, zc + 9, "metal"),                                       # cuve
          B(-61, q0, -59.6, q1, zc + 0.5, zc + 8.5, "inox"),                               # panneau de commande
          ARR(-82, q0 - 0.5, -60, q1 + 0.5, zc + 9, zc + 18.5, "metal", r=3.5, b=1.5),      # couvercle noir
          B(-60.5, q0 + 2, -59.2, q1 - 2, zc + 13, zc + 14.2, "inox")]                    # poignée
    for k in range(3):
        y = (q0 + q1) / 2 + (k - 1) * 8.0
        o.append(C(-59.0, y, 1.1, zc + 3, zc + 5.4, "metal", pans=10))
    # plaque de cuisson noire 4 brûleurs (style « griddle », sans logo) à tablette latérale qui dépasse le bout du meuble
    g0, g1 = CU_PLAQUE
    t1 = CU_TABLETTE[1]
    o += [B(-82, g0, -60, g1, zc, zc + 7, "metal"),
          B(-81, g0 + 0.5, -61, g1 - 0.5, zc + 7, zc + 7.6, "carbone"),                     # plaque
          ARR(-82.5, g0 - 0.3, -60.5, g1 + 0.3, zc + 7.6, zc + 13, "metal", r=2.5, b=1.2),   # couvercle
          B(-82, g1, -61, t1, zc + 6, zc + 7, "metal"),                                    # tablette latérale
          B(-81.5, t1 - 2, -61.5, t1, zc + 2, zc + 6, "metal")]
    for k in range(4):
        y = (g0 + g1) / 2 + (k - 1.5) * 9.0
        o.append(C(-59.4, y, 1.0, zc + 2.5, zc + 4.5, "metal", pans=10))
    return o


# ------------------------------------------------------------------------------------------------- mobilier de détente
def mobilier():
    """Sofa 3 places (cadre d'aluminium noir, coussins gris pâle), table basse à dessus de bois, 2 fauteuils (cadre noir,
    coussins gris), 2 poufs blancs (photo 17)."""
    o = []
    # sofa le long du garde-corps avant, dos à la rue
    x0, x1, y0, y1 = SOFA
    o += [B(x0, y0, x0 + 2.5, y1, ZB, ZB + 24, "metal"), B(x1 - 2.5, y0, x1, y1, ZB, ZB + 24, "metal"),     # accoudoirs
          B(x0 + 2.5, y0, x1 - 2.5, y0 + 2.5, ZB + 7, ZB + 30, "metal"),                                  # dossier
          B(x0 + 2.5, y0 + 2.5, x1 - 2.5, y1, ZB + 7, ZB + 10, "metal")]                                  # assise
    for (xa, ya) in ((x0, y0), (x1 - 2.5, y0), (x0, y1 - 2.5), (x1 - 2.5, y1 - 2.5)):
        o.append(B(xa, ya, xa + 2.5, ya + 2.5, ZB, ZB + 7, "metal"))
    w = (x1 - x0 - 5) / 3
    for k in range(3):
        a = x0 + 2.5 + k * w
        o += [ARR(a + 0.3, y0 + 9, a + w - 0.3, y1, ZB + 10, ZB + 16, "bal-coussin-pale", r=2.2, b=1.2),
              ARR(a + 0.3, y0 + 2.5, a + w - 0.3, y0 + 9, ZB + 11, ZB + 30, "bal-coussin-pale", r=2.5, b=1.2)]
    # table basse : dessus de bois, cadre noir en luge aux bouts
    tx0, tx1, ty0, ty1 = TABLE
    o += [B(tx0, ty0, tx1, ty1, ZB + 14.5, ZB + 16, "bal-teck"), B(tx0 - 0.5, ty0 - 0.5, tx1 + 0.5, ty1 + 0.5, ZB + 13.5, ZB + 14.5, "metal")]
    for xx in (tx0 + 1, tx1 - 2.5):
        o += [B(xx, ty0, xx + 1.5, ty1, ZB, ZB + 1.5, "metal"), B(xx, ty0, xx + 1.5, ty0 + 1.5, ZB, ZB + 13.5, "metal"),
              B(xx, ty1 - 1.5, xx + 1.5, ty1, ZB, ZB + 13.5, "metal")]
    # deux fauteuils face au sofa (cadre noir, assise gris pâle, dossier gris, accoudoirs de bois)
    for (a, b, c0, c1) in FAUTEUILS:
        o += [B(a, c0, a + 2.5, c1, ZB, ZB + 23, "metal"), B(b - 2.5, c0, b, c1, ZB, ZB + 23, "metal"),
              B(a, c0 + 6, a + 2.5, c1, ZB + 23, ZB + 24, "bal-teck"), B(b - 2.5, c0 + 6, b, c1, ZB + 23, ZB + 24, "bal-teck"),
              B(a + 2.5, c1 - 2.5, b - 2.5, c1, ZB + 7, ZB + 29, "metal"),
              B(a + 2.5, c0, b - 2.5, c1 - 2.5, ZB + 7, ZB + 10, "metal"),
              ARR(a + 2.8, c0 + 0.3, b - 2.8, c1 - 8, ZB + 10, ZB + 16, "bal-coussin-pale", r=2.2, b=1.2),
              ARR(a + 2.8, c1 - 8.5, b - 2.8, c1 - 2.5, ZB + 11, ZB + 29, "bal-coussin", r=2.5, b=1.2)]
    # deux poufs blancs (cadre blanc, bordure de bois, dessus rembourré)
    for (qa, qb, pa, pb) in POUFS:
        o += [B(qa, pa, qb, pb, ZB, ZB + 13, "bal-pouf"), B(qa - 0.5, pa - 0.5, qb + 0.5, pb + 0.5, ZB + 12, ZB + 13.5, "bal-teck"),
              ARR(qa + 0.3, pa + 0.3, qb - 0.3, pb - 0.3, ZB + 13.5, ZB + 17, "bal-pouf", r=2, b=1)]
    return o


# ------------------------------------------------------------------------------------------------- filet catamaran
def filet():
    """Maille noire tendue (cordes aux 2½ po), flèche de 4 po au milieu, bordure de corde, banc de planche le long du
    garde-corps droit, trois coussins noirs au bout côté voisin (tête)."""
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
    for k in range(3):
        ya = (y0 + y1) / 2 - 29.25 + k * 19.5
        o.append(ARR(x0 + 1.5, ya, x0 + 17, ya + 18.5, zb - 1.6, zb + 4.2, "bal-coussin-noir", r=3, b=1.6))
    # banc : planche 2 × 12 le long du garde-corps droit, jusqu'au haut de l'escalier
    o.append(B(x1 + 0.5, y0 - 5, XD - 5.5, min(y1 + 5, YAE - 1), ZB, ZB + 1.75, "bal-main"))
    return o


# ------------------------------------------------------------------------------------------------- plateforme et coin des enfants
def _dedans(pts, d):
    """Contour décalé de d po vers l'intérieur (angles vifs)."""
    g = _Poly(pts).buffer(-d, join_style=2)
    return [(round(x, 2), round(y, 2)) for x, y in list(g.exterior.coords)[:-1]]


GLISSADE_HAUT = (88.0, YJ - 1.0)                 # haut de la glissade, au bord avant de la plateforme
_L = math.hypot(XC - XF, YR - YJ)
GLISSADE_DIR = ((XC - XF) / _L, (YR - YJ) / _L)  # parallèle au biais
GLISSADE_L, GLISSADE_W = 52.0, 16.0


def _glissade_pts(marge=0.0):
    (sx, sy), (ux, uy) = GLISSADE_HAUT, GLISSADE_DIR
    nx, ny = -uy, ux
    w = GLISSADE_W / 2 + marge
    a, b = -marge, GLISSADE_L + marge
    return [(sx + ux * a + nx * w, sy + uy * a + ny * w), (sx + ux * b + nx * w, sy + uy * b + ny * w),
            (sx + ux * b - nx * w, sy + uy * b - ny * w), (sx + ux * a - nx * w, sy + uy * a - ny * w)]


SABLE = [(XG + 1.2, YAV - 1.5), (-36.0, YAV - 1.5), (-36.0, YAV - 43.5), (-48.0, YAV - 55.5), (XG + 1.2, YAV - 55.5)]
MAISONNETTE = (XG + 1.2, XG + 61.2, YR + 1.2, YR + 41.2)       # x0, x1, y0 (dos, côté rue), y1 (devant, vers le balcon)


def coin_enfants():
    o = []
    # plateforme basse (devant le balcon, entre le poteau avant de la pergola et la boîte d'écran), trois marches vers le voisin
    o += planches(XP, YJ, XF - 1.2, YAV, "y", Z_PLAT, mat="bal-main")
    o.append(B(XP, YJ, XF - 1.2, YAV, Z_PAILLIS - 4, Z_PLAT - 1, "bal-cadre"))
    for i in range(1, 4):
        o += planches(XP - 10 * i, YJ, XP - 10 * (i - 1), YAV - 1.5, "x", Z_PLAT - 7.5 * i, mat="bal-main", e=1.5)
        o.append(B(XP - 10 * i, YJ, XP - 10 * (i - 1), YAV - 1.5, Z_PAILLIS - 4, Z_PLAT - 7.5 * i - 1.5, "bal-main"))
    # paillis (massif sous le paillis caché par les clôtures) ; jupe teinte sous le bord du balcon
    zb = zmin(COIN) - 2
    o.append(P(_dedans(COIN, 1.2), zb, Z_PAILLIS, "bal-paillis"))
    o.append(B(XG + 1.2, YAV - 0.6, XP, YAV, Z_PAILLIS, ZB - 10.25, "bal-cadre"))
    # carré de sable (bordure 2 × 8 naturelle, coin coupé), dans le coin du mur d'escalade et du balcon
    pts = SABLE
    for (a, b) in zip(pts, pts[1:] + pts[:1]):
        (xa, ya), (xb, yb) = a, b
        L = math.hypot(xb - xa, yb - ya)
        nx, ny = (yb - ya) / L * 1.5, -(xb - xa) / L * 1.5          # vers l'intérieur (contour en sens horaire)
        o.append(P([(xa, ya), (xb, yb), (xb + nx, yb + ny), (xa + nx, ya + ny)], Z_PAILLIS - 2, Z_PAILLIS + 7, "bal-main"))
    o.append(P(_dedans(SABLE, 1.5), Z_PAILLIS - 2, Z_PAILLIS + 3, "bal-sable"))
    o += [B(-60, YAV - 22, -54, YAV - 16, Z_PAILLIS + 3, Z_PAILLIS + 6, "bal-prise-j"),
          B(-72, YAV - 34, -66, YAV - 30, Z_PAILLIS + 3, Z_PAILLIS + 5.5, "bal-prise-o")]
    # mur d'escalade : prises sur la face intérieure de la clôture du voisin, au-dessus du carré de sable
    cols = ["bal-prise-v", "bal-prise-j", "bal-prise-r", "bal-prise-b", "bal-prise-o"]
    k = 0
    for i, z in enumerate(range(80, 140, 11)):
        for j, y in enumerate((YAV - 48, YAV - 32, YAV - 16)):
            yy = y + (5 if (i + j) % 2 else -3)
            o.append(SPH(XG + 2.4, yy, z + (2 if j % 2 else 0), 1.9, cols[k % 5], ecrase=0.75))
            k += 1
    # glissade bleue : du bord avant de la plateforme vers le fond, le long du biais
    (sx, sy), (ux, uy) = GLISSADE_HAUT, GLISSADE_DIR
    nx, ny = -uy, ux
    n = 20
    zz = lambda t: Z_PAILLIS + 2 + (Z_PLAT - Z_PAILLIS - 2) * (1 - t) ** 2
    w = GLISSADE_W / 2
    for kk in range(n):
        t0, t1 = kk / n, (kk + 1) / n
        a, b = GLISSADE_L * t0, GLISSADE_L * t1 + 0.4
        q = [(sx + ux * a + nx * w, sy + uy * a + ny * w), (sx + ux * b + nx * w, sy + uy * b + ny * w),
             (sx + ux * b - nx * w, sy + uy * b - ny * w), (sx + ux * a - nx * w, sy + uy * a - ny * w)]
        zm = zz((t0 + t1) / 2)
        o.append(P(q, zm - 1, zm, "bal-glissade"))
    for sgn in (1, -1):
        o.append(T([(sx + ux * GLISSADE_L * t + sgn * nx * (w + 0.6), sy + uy * GLISSADE_L * t + sgn * ny * (w + 0.6), zz(t) + 3)
                    for t in (0, 0.2, 0.45, 0.7, 1.0)], 1.2, "bal-glissade", pans=8, bouts=True))
    ex, ey = sx + ux * GLISSADE_L, sy + uy * GLISSADE_L
    o.append(P([(ex + nx * (w + 1), ey + ny * (w + 1)), (ex + ux * 3 + nx * (w + 1), ey + uy * 3 + ny * (w + 1)),
                (ex + ux * 3 - nx * (w + 1), ey + uy * 3 - ny * (w + 1)), (ex - nx * (w + 1), ey - ny * (w + 1))],
               Z_PAILLIS - 1, Z_PAILLIS + 2.5, "bal-glissade"))
    # maisonnette « 86 » (5 pi × 3'-4"), dos à la clôture côté rue, devant vers le balcon (+y), toit en appentis plus bas vers la rue
    mx0, mx1, my0, my1 = MAISONNETTE
    zf, zr = Z_PAILLIS + 70, Z_PAILLIS + 60
    o += [B(mx0, my0, mx1, my0 + 1.5, Z_PAILLIS, zr, "bal-maisonnette"), B(mx0, my0, mx0 + 1.5, my1, Z_PAILLIS, zr, "bal-maisonnette"),
          B(mx1 - 1.5, my0, mx1, my1, Z_PAILLIS, zr, "bal-maisonnette")]
    for q in range(4):                                     # pignons en gradins sous l'appentis
        ya_ = my0 + (my1 - my0) * q / 4
        zq = zr + (zf - zr) * (q + 1) / 4
        o += [B(mx0, ya_, mx0 + 1.5, my1, zr, zq, "bal-maisonnette"), B(mx1 - 1.5, ya_, mx1, my1, zr, zq, "bal-maisonnette")]
    # façade : fenêtres ouvertes (cadres noirs), porte, affiche « Bureau », numéro « 86 »
    fy0, fy1 = my1 - 1.5, my1
    ouv = [(mx0 + 4, mx0 + 18, Z_PAILLIS + 24, Z_PAILLIS + 50), (mx0 + 23, mx0 + 37, Z_PAILLIS, Z_PAILLIS + 54),
           (mx0 + 42, mx0 + 56, Z_PAILLIS + 24, Z_PAILLIS + 50)]
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
    o += [B(a + 0.5, fy0 + 3, b - 0.5, fy0 + 4, Z_PAILLIS, Z_PAILLIS + 53, "bal-maisonnette"),          # porte entrouverte
          B(a + 4, fy0 + 2.6, b - 4, fy0 + 3, Z_PAILLIS + 32, Z_PAILLIS + 40, "metal"),                   # sa petite fenêtre
          B(a + 1, fy1, b - 1, fy1 + 0.5, Z_PAILLIS + 55.5, Z_PAILLIS + 58.5, "blanc"),                   # affiche « Bureau »
          B(a + 3.5, fy1, a + 6, fy1 + 0.5, Z_PAILLIS + 61, Z_PAILLIS + 66, "metal"),                    # « 86 »
          B(a + 7.5, fy1, a + 10, fy1 + 0.5, Z_PAILLIS + 61, Z_PAILLIS + 66, "metal")]
    o.append(B(mx1 - 0.2, my0 + 12, mx1 + 0.3, my0 + 29, Z_PAILLIS + 26, Z_PAILLIS + 44, "metal"))     # fenêtre de côté
    for q in range(5):                                     # toit de planches en appentis (débord de 6 po devant)
        ya_ = my1 + 6 - (my1 + 6 - my0 + 2) * (q + 1) / 5
        yb_ = my1 + 6 - (my1 + 6 - my0 + 2) * q / 5
        zq = zf + 1.5 - (zf - zr) * q / 5
        o.append(B(mx0 - 2, ya_, mx1 + 3, yb_, zq - 1.2, zq, "bal-maisonnette"))
    return o


# ------------------------------------------------------------------------------------------------- escalier avant et jardinière
# jardinière de cèdre en gradins entre l'escalier et le mur (photo 16) : (x0, x1, dessus) ; le dernier gradin, devant la fenêtre
# du sous-sol (x 354 à 426, allège 44), reste 10 po sous l'allège
JARDINIERE_Y = (YBE + 4.0, -1.0)
JARDINIERE = [(X0E + 2, 267.0, 84.0), (267.0, 300.0, 64.0), (300.0, 352.0, 46.0), (352.0, 444.0, 34.0)]
BOITE_LETTRES = (428.0, -40.0)


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
    o.append(B(X1E, YAE - 6, X1E + 26, YBE, ZA_ESC - 2, Z_DALLE, "beton"))
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
    o += jardiniere()
    return o


def jardiniere():
    """Jardinière de cèdre à planches horizontales, en gradins qui suivent l'escalier, entre l'escalier et le mur (devant la
    fenêtre du sous-sol), posée sur l'asphalte ; boîte aux lettres noire sur un court poteau, sur le dernier gradin (photo 16)."""
    o = []
    y0, y1 = JARDINIERE_Y
    for (x0, x1, zh) in JARDINIERE:
        zb = zmin([(x0, y0), (x1, y0), (x1, y1), (x0, y1)]) - 2
        o.append(B(x0, y0, x1, y1, zb, zh - 1.5, "bal-cedre"))
        o.append(B(x0, y0, x1, y1, zh - 1.5, zh, "bal-cedre"))                             # chapeau
        o.append(B(x0 + 1.5, y0 + 1.5, x1 - 1.5, y1 - 1.5, zh - 2.5, zh + 0.1, "bal-terre"))
        z = zh - 1.5 - 5.5
        while z > zb + 1:                                                                 # joints des planches (devant, bout)
            o += [B(x0 - 0.1, y0 - 0.15, x1 + 0.1, y0 + 0.2, z - 0.35, z, "bal-cadre"),
                  B(x1 - 0.2, y0 - 0.15, x1 + 0.15, y1, z - 0.35, z, "bal-cadre")]
            z -= 5.75
    bx, by = BOITE_LETTRES
    zh = JARDINIERE[-1][2]
    o += [B(bx - 1.75, by - 1.75, bx + 1.75, by + 1.75, zh, zh + 7, "bal-cedre"),
          ARR(bx - 9, by - 4.5, bx + 9, by + 4.5, zh + 7, zh + 15, "metal", r=1, b=0.5)]
    return o


# ------------------------------------------------------------------------------------------------- données du contrat
def planchers_balcon():
    fx0, fy0, fx1, fy1 = FILET
    pl = [{"nom": "Balcon avant", "pts": rect(XG, YAV, fx0, 0), "z": ZB},
          {"nom": "Balcon avant (derrière le filet)", "pts": rect(fx0, fy1, XD, 0), "z": ZB},
          {"nom": "Balcon avant (devant le filet)", "pts": rect(fx0, YAV, XD, fy0), "z": ZB},
          {"nom": "Balcon avant (banc du filet)", "pts": rect(fx1, fy0, XD, fy1), "z": ZB},
          {"nom": "Filet catamaran (on peut s'y étendre)", "pts": rect(*FILET), "z": round(ZB - 3, 2)},
          {"nom": "Plateforme basse", "pts": rect(XP, YJ, XF - 1.2, YAV), "z": Z_PLAT}]
    pl += [{"nom": f"Marches du coin des enfants, marche {i}", "pts": rect(XP - 10 * i, YJ, XP - 10 * (i - 1), YAV - 1.5),
            "z": Z_PLAT - 7.5 * i} for i in range(1, 4)]
    pl.append({"nom": "Paillis du coin des enfants", "pts": [list(p) for p in _dedans(COIN, 1.2)], "z": Z_PAILLIS})
    pl += [{"nom": f"Escalier avant, marche {i}", "pts": rect(X0E + G_ESC * (i - 1), YAE, X0E + G_ESC * i, YBE),
            "z": round(ZB - R_ESC * i, 2)} for i in range(1, X.ESC_AV_N)]
    pl.append({"nom": "Dalle au pied de l'escalier avant", "pts": rect(X1E, YAE - 6, X1E + 26, YBE), "z": round(Z_DALLE, 2)})
    return pl


def _bande(a, b, e):
    """Emprise d'un tracé (a -> b) de demi-largeur e."""
    (xa, ya), (xb, yb) = a, b
    L = math.hypot(xb - xa, yb - ya)
    nx, ny = -(yb - ya) / L * e, (xb - xa) / L * e
    return [[round(xa - nx, 2), round(ya - ny, 2)], [round(xb - nx, 2), round(yb - ny, 2)], [round(xb + nx, 2), round(yb + ny, 2)],
            [round(xa + nx, 2), round(ya + ny, 2)]]


def obstacles_balcon(poteaux):
    mx0, mx1, my0, my1 = MAISONNETTE
    y0j, y1j = JARDINIERE_Y
    ob = [{"nom": "Garde-corps avant du balcon (au-dessus du coin des enfants)", "pts": rect(CU_X1 + 1, YAV, XP - 5.5, YAV + 3.5)},
          {"nom": "Garde-corps avant du balcon (filet)", "pts": rect(XF - 3.5, YAV, XD, YAV + 3.5)},
          {"nom": "Garde-corps droit du balcon (devant l'escalier, verre teinté)", "pts": rect(XD - 3.5, YAV, XD, YAE)},
          {"nom": "Garde-corps droit du balcon (côté porte)", "pts": rect(XD - 3.5, YBE, XD, 0)},
          {"nom": "Garde-corps à gauche de la maison", "pts": rect(XG, -3.5, 0, 0)},
          {"nom": "Écran d'intimité (voisin de gauche)", "pts": rect(XG, YAV, XG + 2.2, 0)},
          {"nom": "Clôture du coin des enfants (voisin, mur d'escalade)", "pts": rect(XG - 0.5, YR, XG + 2.2, YAV)},
          {"nom": "Clôture du coin des enfants (côté rue)", "pts": rect(XG, YR - 0.5, XC, YR + 2.2)},
          {"nom": "Clôture du coin des enfants (biais)", "pts": _bande((XC, YR), (XF, YJ), 2.2)},
          {"nom": "Clôture de la plateforme", "pts": rect(XF - 2.2, YJ, XF + 0.6, YAV)},
          {"nom": "Cuisine d'extérieur (meuble de 16 pi : four à pizza, frigo, BBQ, plaque de cuisson)", "pts": rect(CU_X0 - 1, CU_Y0, CU_X1 + 1.5, CU_Y1)},
          {"nom": "Tablette de la plaque de cuisson", "pts": rect(-82, CU_Y1, -61, CU_TABLETTE[1])},
          {"nom": "Sofa", "pts": rect(SOFA[0], SOFA[2], SOFA[1], SOFA[3])},
          {"nom": "Table basse", "pts": rect(TABLE[0] - 0.5, TABLE[2] - 0.5, TABLE[1] + 0.5, TABLE[3] + 0.5)},
          {"nom": "Maisonnette « 86 »", "pts": rect(mx0 - 1, my0 - 1, mx1 + 1, my1 + 1)},
          {"nom": "Carré de sable", "pts": [list(p) for p in SABLE]},
          {"nom": "Glissade", "pts": [[round(x, 2), round(y, 2)] for x, y in _glissade_pts(1.0)]},
          {"nom": "Main courante de l'escalier avant", "pts": rect(X0E - 3.5, YAE - 3.5, X1E + 4, YAE)},
          {"nom": "Jardinière de cèdre et boîte aux lettres", "pts": rect(JARDINIERE[0][0], y0j, JARDINIERE[-1][1], y1j)}]
    ob += [{"nom": "Fauteuil", "pts": rect(f[0], f[2], f[1], f[3])} for f in FAUTEUILS]
    ob += [{"nom": "Pouf", "pts": rect(q[0] - 0.5, q[2] - 0.5, q[1] + 0.5, q[3] + 0.5)} for q in POUFS]
    for xc in PERGOLA_X:
        for yc in PERGOLA_Y:
            ob.append({"nom": "Poteau de la pergola", "pts": rect(xc - 3.2, yc - 3.2, xc + 3.2, yc + 3.2)})
    return ob


VISITES = [
    {"nom": "Balcon avant — vue sur le fleuve", "x": 192, "y": -22, "cap": 258, "z": ZB},         # en sortant de la porte
    {"nom": "Filet catamaran", "x": 168, "y": -84, "cap": 250, "z": ZB},                          # derrière le filet
    {"nom": "Cuisine d'extérieur (four à pizza)", "x": 30, "y": -14, "cap": 222, "z": ZB},        # côté maison : tout le meuble de 16 pi
    {"nom": "Coin des enfants", "x": 95, "y": YAV - 12, "cap": 210, "z": Z_PLAT},                 # sur la plateforme
    {"nom": "Escalier avant (de la rue)", "x": 486, "y": -236, "cap": 140, "z": None},
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


ARBRE_AVANT = (30.0, -446.0, 380.0)     # feuillu entre le coin des enfants et la rue (ses branches passent au-dessus, photos 01, 02, 06)


def _deplacer_arbre(EXT):
    """Le petit arbre ornemental de exterieur.py (x -60, y -250) tombe dans le coin des enfants : il est retiré et remplacé
    par le feuillu des photos, entre la clôture côté rue du coin des enfants et la rue."""
    EXT["objets"] = [o for o in EXT["objets"] if not (o.get("x") == -60 and o.get("y") == -250 and o.get("forme") in ("cylindre", "sphere"))]
    EXT["obstacles"] = [o for o in EXT["obstacles"] if o["nom"] != "Arbre ornemental (tronc)"]
    x, y, H = ARBRE_AVANT
    z = zt(x, y)
    EXT["objets"] += [C(x, y, 8, z, z + 0.45 * H, "bois_brut", pans=10),
                      SPH(x, y, z + 0.58 * H, 0.28 * H, "ext-feuillage-clair", ecrase=0.8),
                      SPH(x + 0.07 * H, y + 0.08 * H, z + 0.8 * H, 0.21 * H, "ext-feuillage", ecrase=0.85)]
    EXT["obstacles"].append({"nom": "Arbre devant le coin des enfants (tronc)", "pts": X.cercle(x, y, 10, 12)})


def appliquer_exterieur(EXT):
    _retirer_perron(EXT)
    _deplacer_arbre(EXT)
    struct, poteaux = plancher()
    EXT["objets"] += (struct + garde_corps_balcon() + ecrans() + pergola() + cuisine() + mobilier() + filet() + coin_enfants()
                      + escalier())
    EXT["planchers"] += planchers_balcon()
    EXT["obstacles"] += obstacles_balcon(poteaux)
    EXT["lumieres"] = list(EXT.get("lumieres") or []) + LUMIERES
    for v in VISITES:
        v = dict(v)
        if v["z"] is None:
            v["z"] = round(zt(v["x"], v["y"]), 1)
        EXT["visites"].append(v)
    EXT["peintures"] = dict(EXT.get("peintures") or {}, **PEINTURES)
    EXT["palette"] = list(EXT.get("palette") or []) + PALETTE
    return EXT
