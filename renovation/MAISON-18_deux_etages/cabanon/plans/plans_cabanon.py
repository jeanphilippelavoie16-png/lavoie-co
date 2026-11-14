#!/usr/bin/env python3
"""Plans de construction (menuiserie) du cabanon 13' x 17' — 86, avenue Laurier, Baie-Comeau.

Source : renovation/MAISON-18_deux_etages/cabanon/FICHE_cabanon.md (depot lavoie-co, branche
claude/releve-existant-plans-rmyk2l). Toutes les cotes des feuilles sont calculees ici, en pouces.

    python plans_cabanon.py      -> svg/A1..A6.svg + plans.html
    node rendre.js               -> png/A1..A6.png + PLANS_cabanon.pdf
"""
import math, os, textwrap

ICI = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ donnees
FINI_L, FINI_P = 156.0, 204.0        # hors tout fini (fiche) : 13'-0" x 17'-0"
PAREMENT = 2.0                       # OSB 7/16 + fourrure 3/4 + planche 3/4
OSS_L, OSS_P = FINI_L - 2 * PAREMENT, FINI_P - 2 * PAREMENT      # ossature 152 x 200
EP = 3.5                             # 2 x 4
CTP = 0.5                            # contreplaque interieur
BORD = 6.0                           # bordure de beton
H_MUR = 96.0                         # dalle -> dessus des sablieres
COL = H_MUR - BORD - 4.5             # colombage : 85 1/2
PORTE_L, PORTE_H = 96.0, 84.0
OB_L = PORTE_L + 3.0                 # ouverture brute : 99
LINT_H = 7.25                        # 2 x 8
OB_H = H_MUR - 3.0 - LINT_H          # 85 3/4
OB_X0 = (OSS_L - OB_L) / 2           # 26 1/2
OB_X1 = OB_X0 + OB_L
PENTE = 7.0 / 12.0
ANG = math.atan(PENTE)
COS = math.cos(ANG)
CHEV = 5.5                           # 2 x 6
CHEV_PL = CHEV / COS                 # hauteur d'aplomb du chevron : 6,37
ASSISE = 3.5
ENT_PL = ASSISE * PENTE              # entaille d'aplomb : 2,04
HAP = CHEV_PL - ENT_PL               # 4,33 au-dessus de la sabliere, au nu de l'ossature
CX = OSS_L / 2                       # axe du faite : 76
DEB_FINI = 12.0                      # debord fini (du parement au fascia)
BOUT = CX + PAREMENT + DEB_FINI - 0.75 - 1.5     # bout du chevron depuis l'axe : 87 3/4
FAIT = 0.75                          # demi-epaisseur de la faitiere
REV_TOIT = 0.625 / COS               # 5/8 de pontage, d'aplomb


def zt(x):
    """Dessus du chevron (pouces au-dessus de la dalle) a x de l'axe du faite."""
    return H_MUR + HAP + (CX - abs(x)) * PENTE


def zb(x):
    return zt(x) - CHEV_PL


L_CHEV = (BOUT - FAIT) / COS                     # 100,72
L_TALON = (CX - FAIT) / COS                      # 87,12 du faite a l'aplomb du mur
L_QUEUE = (BOUT - CX) / COS                      # 13,60
Z_FAITE = zt(0) + REV_TOIT + 0.25                # dessus du bardeau au faite

AXES = [16.0 * i for i in range(1, 13)]          # axes des colombages et chevrons des murs de cote
BOUL_COTE = [8, 56, 104, 152, 188]
BOUL_FOND = [10, 52, 100, 138]
BOUL_AVANT = [10, 19.5, OSS_L - 19.5, OSS_L - 10]

FR = {0: "", 1: "⅛", 2: "¼", 3: "⅜", 4: "½", 5: "⅝", 6: "¾", 7: "⅞"}


def po(v):
    """Pouces arrondis au 1/8."""
    n = round(v * 8)
    e, f = divmod(n, 8)
    return (str(e) if e or not f else "") + FR[f] + '"'


def pp(v):
    """Pieds-pouces arrondis au 1/8."""
    n = round(v * 8)
    pi, r = divmod(n, 96)
    e, f = divmod(r, 8)
    return f"{pi}'-{e}{FR[f]}\""


def cote(v):
    return pp(v) if v >= 24 else po(v)


# ------------------------------------------------------------------ dessin
class Vue:
    def __init__(s, ox, oy, k):
        s.ox, s.oy, s.k = ox, oy, k

    def X(s, x):
        return s.ox + x * s.k

    def Y(s, y):
        return s.oy - y * s.k


class Feuille:
    W, H = 1632, 1056

    def __init__(s, no, titre):
        s.no, s.titre, s.o = no, titre, []

    def R(s, v, x0, y0, x1, y1, c):
        a, b = sorted((v.X(x0), v.X(x1)))
        d, e = sorted((v.Y(y0), v.Y(y1)))
        s.o.append(f'<rect class="{c}" x="{a:.1f}" y="{d:.1f}" width="{b - a:.1f}" height="{e - d:.1f}"/>')

    def P(s, v, pts, c):
        p = " ".join(f"{v.X(x):.1f},{v.Y(y):.1f}" for x, y in pts)
        s.o.append(f'<polygon class="{c}" points="{p}"/>')

    def L(s, v, x0, y0, x1, y1, c="tr"):
        s.o.append(f'<line class="{c}" x1="{v.X(x0):.1f}" y1="{v.Y(y0):.1f}" x2="{v.X(x1):.1f}" y2="{v.Y(y1):.1f}"/>')

    def C(s, v, x, y, r, c):
        s.o.append(f'<circle class="{c}" cx="{v.X(x):.1f}" cy="{v.Y(y):.1f}" r="{r}"/>')

    def T(s, px, py, txt, c="t", a="middle", rot=None):
        r = f' transform="rotate({rot} {px:.1f} {py:.1f})"' if rot is not None else ""
        txt = txt.replace("&", "&amp;").replace("<", "&lt;")
        s.o.append(f'<text class="{c}" x="{px:.1f}" y="{py:.1f}" text-anchor="{a}"{r}>{txt}</text>')

    def TV(s, v, x, y, txt, c="t", a="middle", dx=0, dy=0, rot=None):
        s.T(v.X(x) + dx, v.Y(y) + dy, txt, c, a, rot)

    def fleche(s, v, x, y, px, py, txt, c="t"):
        """Renvoi : texte ancre a (px, py) en pixels, trait jusqu'au point (x, y) de la vue.
        Le texte part vers la droite si le point est a sa gauche, vers la gauche sinon."""
        a = "start" if v.X(x) <= px else "end"
        s.o.append(f'<line class="rv" x1="{px:.1f}" y1="{py - 4:.1f}" x2="{v.X(x):.1f}" y2="{v.Y(y):.1f}"/>')
        s.o.append(f'<circle class="pt" cx="{v.X(x):.1f}" cy="{v.Y(y):.1f}" r="2.2"/>')
        s.T(px + (4 if a == "start" else -4), py, txt, c, a)

    def dh(s, v, x0, x1, y, off, txt=None, c="dt"):
        """Cote horizontale ; off en pixels (positif = vers le bas)."""
        a, b, y0 = v.X(x0), v.X(x1), v.Y(y)
        py = y0 + off
        g = 4 if off > 0 else -4
        for x in (a, b):
            s.o.append(f'<line class="dim" x1="{x:.1f}" y1="{y0 + g:.1f}" x2="{x:.1f}" y2="{py + g:.1f}"/>')
            s.o.append(f'<line class="tick" x1="{x - 4:.1f}" y1="{py + 4:.1f}" x2="{x + 4:.1f}" y2="{py - 4:.1f}"/>')
        s.o.append(f'<line class="dim" x1="{a:.1f}" y1="{py:.1f}" x2="{b:.1f}" y2="{py:.1f}"/>')
        s.T((a + b) / 2, py - 5, txt if txt is not None else cote(abs(x1 - x0)), c)

    def dv(s, v, y0, y1, x, off, txt=None, c="dt"):
        """Cote verticale ; off en pixels (positif = vers la droite)."""
        a, b, x0 = v.Y(y0), v.Y(y1), v.X(x)
        px = x0 + off
        g = 4 if off > 0 else -4
        for y in (a, b):
            s.o.append(f'<line class="dim" x1="{x0 + g:.1f}" y1="{y:.1f}" x2="{px + g:.1f}" y2="{y:.1f}"/>')
            s.o.append(f'<line class="tick" x1="{px - 4:.1f}" y1="{y + 4:.1f}" x2="{px + 4:.1f}" y2="{y - 4:.1f}"/>')
        s.o.append(f'<line class="dim" x1="{px:.1f}" y1="{a:.1f}" x2="{px:.1f}" y2="{b:.1f}"/>')
        s.T(px - 5, (a + b) / 2, txt if txt is not None else cote(abs(y1 - y0)), c, rot=-90)

    def titre_vue(s, px, py, txt, sous=None):
        s.T(px, py, txt, "h", "start")
        if sous:
            s.T(px, py + 18, sous, "s", "start")

    def notes(s, px, py, titre, lignes, larg=60, lh=18.5):
        s.T(px, py, titre, "h2", "start")
        y = py + 22
        for l in lignes:
            morceaux = textwrap.wrap(l, larg) or [""]
            for i, m in enumerate(morceaux):
                s.T(px + (0 if i == 0 else 14), y, m, "n", "start")
                y += lh
            y += 3
        return y

    def table(s, px, py, cols, rangs, larg, lh=21):
        x = px
        s.o.append(f'<rect class="th" x="{px}" y="{py}" width="{sum(larg)}" height="{lh}"/>')
        for c, w in zip(cols, larg):
            s.T(x + 6, py + 15, c, "tb", "start")
            x += w
        y = py + lh
        for r in rangs:
            x = px
            if len(r) == 1:
                s.o.append(f'<rect class="tg" x="{px}" y="{y}" width="{sum(larg)}" height="{lh}"/>')
                s.T(px + 6, y + 15, r[0], "tb", "start")
            else:
                for c, w in zip(r, larg):
                    s.T(x + 6, y + 15, c, "n", "start")
                    x += w
            s.o.append(f'<line class="tl" x1="{px}" y1="{y + lh}" x2="{px + sum(larg)}" y2="{y + lh}"/>')
            y += lh
        return y

    def svg(s):
        W, H = s.W, s.H
        cart = [
            f'<rect class="cadre" x="24" y="24" width="{W - 48}" height="{H - 48}"/>',
            f'<line class="cadre" x1="24" y1="{H - 78}" x2="{W - 24}" y2="{H - 78}"/>',
            f'<text class="ct" x="40" y="{H - 44}">CABANON 13\' × 17\' — 86, avenue Laurier, Baie-Comeau</text>',
            f'<text class="cs" x="640" y="{H - 44}">{s.titre}</text>',
            f'<text class="cn" x="{W - 40}" y="{H - 52}" text-anchor="end">A{s.no} / 6</text>',
            f'<text class="cp" x="{W - 40}" y="{H - 34}" text-anchor="end">2026-11-14 · plans de menuiserie · projet, pas un relevé · cotes en pieds et pouces</text>',
        ]
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
                f'<style>{CSS}</style>\n<rect width="{W}" height="{H}" fill="#fff"/>\n'
                + "\n".join(cart) + "\n" + "\n".join(s.o) + "\n</svg>\n")


CSS = """
text{font-family:'Segoe UI',Arial,Helvetica,sans-serif;fill:#1c1c1c}
.t{font-size:13px}.s{font-size:12.5px;fill:#555}.n{font-size:13.5px}
.h{font-size:17px;font-weight:700}.h2{font-size:15px;font-weight:700}
.dt{font-size:13px;fill:#a3201a;font-weight:600}.dg{font-size:12px;fill:#a3201a}
.tb{font-size:13px;font-weight:700}.g{font-size:12.5px;fill:#666;font-style:italic}
.ct{font-size:20px;font-weight:700}.cs{font-size:18px;font-weight:600}.cn{font-size:20px;font-weight:700}.cp{font-size:12.5px;fill:#444}
.cadre{fill:none;stroke:#1c1c1c;stroke-width:1.6}
.dim{stroke:#a3201a;stroke-width:.9;fill:none}.tick{stroke:#a3201a;stroke-width:1.5}
.tr{stroke:#222;stroke-width:1.1;fill:none}.fin{stroke:#222;stroke-width:.6;fill:none}
.gros{stroke:#111;stroke-width:2;fill:none}
.pt{fill:#222}.rv{stroke:#555;stroke-width:.8}
.ti{stroke:#222;stroke-width:1;stroke-dasharray:7 4;fill:none}
.axe{stroke:#444;stroke-width:.9;stroke-dasharray:14 4 3 4;fill:none}
.sol{stroke:#3c6e2f;stroke-width:1.6;fill:none}
.bois{fill:#efdcae;stroke:#5a4520;stroke-width:.9}
.bois2{fill:#d6b676;stroke:#5a4520;stroke-width:.9}
.trt{fill:#b7cc9c;stroke:#3f5a2a;stroke-width:.9}
.osb{fill:#e3bf7c;stroke:#6b5020;stroke-width:.6}
.ctp{fill:#f6e9c9;stroke:#6b5020;stroke-width:.6}
.bet{fill:#cfd0d2;stroke:#444;stroke-width:1}
.gra{fill:#ebe5d6;stroke:#9b927c;stroke-width:.6;stroke-dasharray:3 3}
.mur{fill:#555;stroke:#222;stroke-width:1}
.par{fill:#fff;stroke:#222;stroke-width:1.1}
.cj{stroke:#888;stroke-width:.7}
.toit{fill:#4e5154;stroke:#222;stroke-width:1}
.porte{fill:#1d1d1f;stroke:#000;stroke-width:1}
.vit{fill:#b9cdd8;stroke:#000;stroke-width:.6}
.vide{fill:#fff;stroke:#222;stroke-width:1}
.boul{fill:#fff;stroke:#a3201a;stroke-width:1.8}
.fer{stroke:#1a4f8a;stroke-width:1.6;fill:none}.ferp{fill:#1a4f8a}
.th{fill:#e7e7e7;stroke:#888;stroke-width:.6}.tg{fill:#f3efe3;stroke:none}.tl{stroke:#bbb;stroke-width:.6}
"""


# ------------------------------------------------------------------ positions des colombages
def col_cote():
    """Colombages d'un mur de cote : (y0, y1) le long du mur."""
    return [(0, 1.5), (3.5, 5)] + [(a - 0.75, a + 0.75) for a in AXES] + [(OSS_P - 5, OSS_P - 3.5), (OSS_P - 1.5, OSS_P)]


def col_fond():
    return [(3.5, 5)] + [(16.0 * i - 0.75, 16.0 * i + 0.75) for i in range(1, 10)] + [(OSS_L - 5, OSS_L - 3.5)]


def col_avant():
    g = [(3.5, 5), (15.25, 16.75), (OB_X0 - 4.5, OB_X0 - 3)]
    d = [(OSS_L - b, OSS_L - a) for a, b in g]
    return g + d


def pignon():
    """Colombages de pignon : (axe x, longueur au long point)."""
    out = []
    for i in range(1, 10):
        x = 16.0 * i
        d = min(x, OSS_L - x) + 0.75
        lg = d * PENTE - ENT_PL
        if lg > 5:
            out.append((x, lg))
    return out


def dessin_pignon(f, v):
    """Pignon au-dessus d'un mur de 152 : chevrons de rive, faitiere, colombages."""
    for sg in (-1, 1):
        f.P(v, [(CX + sg * FAIT, zt(FAIT)), (CX + sg * BOUT, zt(BOUT)), (CX + sg * BOUT, zb(BOUT)),
                (CX + sg * CX, zb(CX)), (CX + sg * CX, H_MUR), (CX + sg * (CX - ASSISE), H_MUR),
                (CX + sg * FAIT, zb(FAIT))], "bois2")
    f.R(v, CX - FAIT, zt(FAIT) - 7.25, CX + FAIT, zt(FAIT), "bois")
    for x, lg in pignon():
        f.P(v, [(x - 0.75, H_MUR), (x + 0.75, H_MUR), (x + 0.75, zb(x + 0.75 - CX)), (x - 0.75, zb(x - 0.75 - CX))], "bois")


def pente_symbole(f, v, x, z):
    """Triangle 7/12 pose dans le ciel, au-dessus du versant de droite."""
    f.P(v, [(x, z + 14), (x, z), (x + 24, z)], "tr")
    f.TV(v, x + 12, z, "12", "tb", dy=15)
    f.TV(v, x, z + 7, "7", "tb", dx=-10, dy=5)


# ------------------------------------------------------------------ A1 vue d'ensemble
def a1():
    f = Feuille(1, "Vue d'ensemble et bases du calcul")
    v = Vue(130, 800, 2.5)                      # repere de l'ossature ; y = 0 a l'avant
    f.titre_vue(48, 64, "Plan", "avant (porte) en bas ; le toit en tireté")
    f.R(v, -14, -14, OSS_L + 14, OSS_P + 14, "ti")
    f.R(v, -2, -2, OSS_L + 2, OSS_P + 2, "mur")
    f.R(v, 4, 4, OSS_L - 4, OSS_P - 4, "vide")
    f.R(v, CX - 48, -2.4, CX + 48, 4.4, "vide")
    f.L(v, CX - 48, 2, CX + 48, 2, "ti")
    f.L(v, CX, -20, CX, OSS_P + 20, "axe")
    f.TV(v, CX, 160, "faîte", "g", dx=-8, rot=-90)
    f.TV(v, CX, 122, "intérieur fini", "t")
    f.TV(v, CX, 113, "12'-0\" × 16'-0\"", "tb")
    f.TV(v, CX, 16, "porte de garage 8'-0\" × 7'-0\"", "t")
    f.TV(v, 13, OSS_P / 2, "côté piscine", "g", rot=-90)
    f.TV(v, OSS_L - 9, OSS_P / 2, "côté ligne de lot", "g", rot=-90)
    f.dh(v, -2, OSS_L + 2, -14, 62, "13'-0\" hors tout fini")
    f.dh(v, CX - 48, CX + 48, -14, 34, "8'-0\"")
    f.dh(v, -2, CX - 48, -14, 34, "2'-6\"")
    f.dh(v, CX + 48, OSS_L + 2, -14, 34, "2'-6\"")
    f.dh(v, -14, OSS_L + 14, OSS_P + 14, -22, "15'-0\" toit, fascia à fascia")
    f.dv(v, -2, OSS_P + 2, OSS_L + 14, 34, "17'-0\" hors tout fini")
    f.dv(v, -14, OSS_P + 14, OSS_L + 14, 62, "19'-0\" toit")
    f.dv(v, 0, OSS_P, -14, -24, "16'-8\" ossature")
    f.dh(v, 0, OSS_L, 60, 0, "12'-8\" ossature")
    f.T(v.X(CX), v.Y(-14) + 86, "COUR — vers la maison", "g")
    f.T(v.X(CX), v.Y(OSS_P + 14) - 46, "ligne de lot arrière", "g")

    e = Vue(850, 470, 2.2)                      # elevation avant, x depuis l'axe
    f.titre_vue(640, 64, "Élévation avant", "le pignon et la porte, vers la maison")
    f.L(e, -100, -0.5, 100, -0.5, "sol")
    f.R(e, -76, -0.5, 76, 6, "bet")
    f.P(e, [(-78, 5), (78, 5), (78, zb(78)), (0, zb(0) + 1), (-78, zb(78))], "par")
    for x in range(-72, 73, 12):
        f.L(e, x, 87.5 if -52 < x < 52 else 5, x, zb(x), "cj")
    f.R(e, -51, 0, 51, 87, "par")
    f.R(e, -48, 0, 48, 84, "porte")
    for z in (21, 42, 63):
        f.L(e, -48, z, 48, z, "cj")
    for i in range(8):
        f.R(e, -45 + i * 11.4, 67, -45 + i * 11.4 + 9.6, 80, "vit")
    f.P(e, [(-90, zt(90) + 1), (0, zt(0) + 1.2), (90, zt(90) + 1), (90, zt(90) - 6), (0, zt(0) - 6), (-90, zt(90) - 6)], "par")
    f.P(e, [(-90.5, zt(90) + 1), (0, zt(0) + 1.4), (90.5, zt(90) + 1), (90.5, zt(90) + 2.2), (0, zt(0) + 2.6), (-90.5, zt(90) + 2.2)], "toit")
    f.dh(e, -78, 78, -0.5, 30, "13'-0\"")
    f.dh(e, -90, 90, -0.5, 56, "15'-0\"")
    f.dv(e, 0, 84, -90, -18, "7'-0\"")
    pente_symbole(f, e, 52, 128)

    c = Vue(1100, 470, 2.0)                     # elevation de cote
    f.titre_vue(1072, 64, "Élévation de côté", "mur de 17 pi")
    f.L(c, -20, -0.5, 222, -0.5, "sol")
    f.R(c, 0, -0.5, 200, 6, "bet")
    f.R(c, -2, 5, 202, 87.1, "par")
    for y in range(4, 201, 12):
        f.L(c, y, 5, y, 87.1, "cj")
    f.R(c, -14, zt(90) - 6, 214, zt(90) + 1, "par")
    f.R(c, -14.5, zt(90) + 1, 214.5, Z_FAITE, "toit")
    f.dh(c, -2, 202, -0.5, 30, "17'-0\"")
    f.dh(c, -14, 214, -0.5, 56, "19'-0\"")
    f.dv(c, 0, H_MUR, 214, 30, "8'-0\" mur")
    f.dv(c, -0.5, Z_FAITE, 214, 58, pp(Z_FAITE + 0.5) + " faîte")
    f.TV(c, 100, 118, "bardeau d'asphalte, pente 7/12", "t")
    f.o[-1] = f.o[-1].replace('class="t"', 'class="t" style="fill:#fff"')
    f.o.append(f'<rect fill="#fff" x="{c.X(100) - 150:.0f}" y="{c.Y(50) - 15:.0f}" width="300" height="42"/>')
    f.TV(c, 100, 50, "planches verticales, couvre-joints aux 12\"", "t")
    f.TV(c, 100, 50, "bordure de béton de 6\" au pied des murs", "s", dy=18)

    x0, y0 = 640, 592
    y = f.notes(x0, y0, "Bases du calcul", [
        "Neige de Baie-Comeau : 4,3 kPa au sol + 0,4 kPa de pluie. Sur le toit : 0,55 × 4,3 + 0,4 = 2,8 kPa ; "
        "toutes les pièces sont lues dans la colonne 3,0 kPa des tableaux de portées.",
        "Bois : épinette-pin-sapin n° 2 ou mieux, sec. Traité sous pression partout où il touche le béton.",
        f"Chevrons 2 × 6 aux 16\" : portée permise 10'-1\", portée ici {pp(CX - ASSISE - FAIT)}.",
        f"Solives de plafond 2 × 6 aux 16\" : permis 14'-7\", ici {pp(OSS_L - 2 * EP)}.",
        f"Linteau de la porte, 2 − 2 × 8 dans le mur pignon (il ne porte que le débord du toit) : permis 12'-0\", ici {pp(OB_L)}.",
        "Colombages 2 × 4 aux 16\", un chevron et une solive au-dessus de chacun.",
    ], 66)
    f.notes(x0, y + 8, "Reste à valider", [
        "La dalle : épaisseurs et armature typiques, non calculées. Le sol, le drainage et le gel se jugent sur place.",
        "Le permis, et la distance de 1 m à la piscine (remise, pas garage).",
    ], 66)
    f.notes(1130, y0, "Écarts avec la fiche", [
        "1. Le hors tout fini reste à 13'-0\" × 17'-0\" : c'est lui qui tient les marges de la piscine et des lignes "
        "de lot. L'ossature est donc à 12'-8\" × 16'-8\", et l'intérieur fini à 12'-0\" × 16'-0\" (fiche : 12'-2\" × 16'-2\").",
        "2. Mur de 6\" et non 5\" : OSB et fourrures sous les planches. Sans OSB le mur n'est pas contreventé ; "
        "sans fourrure la planche verticale n'a rien où se clouer.",
        "3. Bordure de béton de 6\" sous les murs : le bois ne trempe ni dans le gazon ni dans la neige. "
        "La dalle reste au ras du gazon et le mur garde 8'-0\".",
        "4. Dalle au nu de l'ossature, sans le débord de 2\" : un rebord de béton ramasse l'eau et l'envoie sous la lisse.",
        f"5. Plafond fini à 7'-11½\" (fiche : 7'-10\"). Faîte à {pp(Z_FAITE + 0.5)} du sol (fiche : 12'-4\" ; la Ville permet 13'-11\").",
        "6. Rack de bacs de 141\" : il entre dans 144\", avec 1½\" de jeu de chaque côté.",
    ], 62)
    return f


# ------------------------------------------------------------------ A2 dalle
def a2():
    f = Feuille(2, "Dalle, bordure et ancrages")
    v = Vue(150, 880, 3.6)
    f.titre_vue(48, 64, "Plan de la dalle", "dalle au nu de l'ossature : 12'-8\" × 16'-8\"")
    f.R(v, 0, 0, OSS_L, OSS_P, "bet")
    f.R(v, 12, 12, OSS_L - 12, OSS_P - 12, "ti")
    for (a, b, c_, d) in ((0, 0, EP, OSS_P), (OSS_L - EP, 0, OSS_L, OSS_P), (0, OSS_P - EP, OSS_L, OSS_P),
                          (0, 0, OB_X0, EP), (OB_X1, 0, OSS_L, EP)):
        f.R(v, a, b, c_, d, "mur")
    for y in BOUL_COTE:
        f.C(v, EP / 2, y, 4, "boul")
        f.C(v, OSS_L - EP / 2, y, 4, "boul")
    for x in BOUL_FOND:
        f.C(v, x, OSS_P - EP / 2, 4, "boul")
    for x in BOUL_AVANT:
        f.C(v, x, EP / 2, 4, "boul")
    f.dh(v, 0, OSS_L, 0, 64, "12'-8\"")
    f.dh(v, OB_X0, OB_X1, 0, 36, pp(OB_L) + " ouverture brute")
    f.dh(v, 0, OB_X0, 0, 36)
    f.dh(v, OB_X1, OSS_L, 0, 36)
    f.dv(v, 0, OSS_P, 0, -64, "16'-8\"")
    ch = [0] + BOUL_COTE + [OSS_P]
    for a, b in zip(ch, ch[1:]):
        f.dv(v, a, b, 0, -32)
    ch = [0] + BOUL_FOND + [OSS_L]
    for a, b in zip(ch, ch[1:]):
        f.dh(v, a, b, OSS_P, -26)
    f.TV(v, CX, 108, "dalle 4\" min., pente ⅛\" au pied vers la porte", "t")
    f.TV(v, CX, 96, "treillis d'acier ou 10M aux 18\" dans les deux sens", "t")
    f.TV(v, CX, 24, "bord épaissi 12\" × 12\" sous les quatre côtés (tireté)", "s")
    f.TV(v, CX, 6, "seuil : dalle seule, pas de bordure", "s", dy=14)
    f.fleche(v, OSS_L - EP / 2, 188, v.X(OSS_L) + 30, v.Y(194), "boulon ½\" × 8\"")
    f.fleche(v, OSS_L - 1, 172, v.X(OSS_L) + 30, v.Y(176), "bordure 3½\" × 6\"")
    f.T(v.X(OSS_L) + 34, v.Y(176) + 16, "(en gris foncé)", "s", "start")
    f.T(v.X(CX), v.Y(0) + 90, "AVANT — la cour", "g")

    c = Vue(1120, 560, 10.0)    # x = 0 au nu exterieur de l'ossature, positif vers l'interieur ; z = 0 dessus de dalle
    f.titre_vue(830, 64, "Coupe du bord de la dalle", "typique des trois murs ; à la porte, la bordure s'arrête")
    f.P(c, [(-13, -17), (24, -17), (24, -4), (20, -4), (12, -12), (0, -12), (0, -10), (-13, -10)], "gra")
    f.P(c, [(0, -12), (12, -12), (20, -4), (24, -4), (24, 0), (EP, 0), (EP, BORD), (0, BORD)], "bet")
    f.L(c, -13, -0.5, 0, -0.5, "sol")
    f.R(c, 0, BORD, EP, BORD + 1.5, "trt")
    f.R(c, 0, BORD + 1.5, EP, BORD + 16, "bois")
    f.R(c, -0.44, BORD - 1, 0, BORD + 16, "osb")
    f.R(c, -1.19, BORD + 0.5, -0.44, BORD + 2, "bois2")
    f.R(c, -1.19, BORD + 12, -0.44, BORD + 13.5, "bois2")
    f.R(c, -1.94, BORD - 1.5, -1.19, BORD + 16, "par")
    f.R(c, EP, 0.5, EP + CTP, BORD + 16, "ctp")
    f.L(c, EP / 2, BORD + 2.3, EP / 2, -3, "fer")
    f.L(c, EP / 2, -3, EP / 2 + 2, -3, "fer")
    for (x, z) in ((3, -9), (9, -9), (EP / 2 + 0.9, 3.2)):
        f.C(c, x, z, 3.2, "ferp")
    f.L(c, 13, -2, 24, -2, "fer")
    f.dv(c, 0, BORD, EP + CTP, 34, "6\"")
    f.dv(c, -4, 0, 22, 0, "4\"")
    f.dv(c, -12, 0, 0, -140, "12\"")
    f.dh(c, 0, 12, -17, 26, "12\"")
    f.dh(c, 0, EP, BORD + 16, -18, "3½\"")
    xr = c.X(17)
    f.fleche(c, EP + CTP / 2, BORD + 14, xr, c.Y(BORD + 15), "contreplaqué ½\", arrêté ½\" au-dessus de la dalle")
    f.fleche(c, EP / 2, BORD + 10, xr, c.Y(BORD + 11.5), "colombage 2 × 4")
    f.fleche(c, EP / 2, BORD + 0.75, xr, c.Y(BORD + 8), "lisse 2 × 4 traitée, sur mousse de lisse")
    f.fleche(c, EP / 2, BORD - 1.2, xr, c.Y(BORD + 4.5), "boulon ½\" × 8\", crochet dans le bord épaissi")
    f.fleche(c, EP / 2 + 0.9, 3.2, xr, c.Y(BORD + 1), "1 − 10M continu dans la bordure")
    xb = c.X(26.5)
    f.fleche(c, 23, -2, xb, c.Y(-1.2), "treillis ou 10M")
    f.fleche(c, 9, -9, xb, c.Y(-7.5), "2 − 15M continus")
    f.fleche(c, 21, -14.5, xb, c.Y(-13.5), "pierre 0-¾\" compactée")
    xg = c.X(-13)
    f.fleche(c, -1.56, BORD + 9, xg, c.Y(BORD + 10), "planche ¾\" + couvre-joint")
    f.fleche(c, -0.8, BORD + 12.7, xg, c.Y(BORD + 14), "fourrure 1 × 3 horizontale")
    f.fleche(c, -0.22, BORD - 0.5, xg, c.Y(BORD - 1), "l'OSB descend 1\" sur le béton")
    f.fleche(c, -7, -0.5, xg, c.Y(-4.5), "gazon ½\" sous la dalle")

    f.notes(830, 806, "Notes", [
        "Béton de 32 MPa à air entraîné (plancher de garage). Sortir la terre noire jusqu'au sol ferme, remonter en pierre "
        "0-¾\" compactée par couches de 6\". Le fond doit se drainer : une dalle flottante qui gèle dans l'eau se soulève.",
        "Bordure coulée avec la dalle, coffrée au nu extérieur. Elle s'arrête de chaque côté de l'ouverture de 8'-3\".",
        "18 boulons ½\" × 8\" : 5 par mur de côté, 4 au fond, 2 par bout du mur avant. Ils tombent entre les colombages.",
        "Vérifier les diagonales avant de couler : 20'-11¼\" d'un coin à l'autre.",
    ], 108)
    return f


# ------------------------------------------------------------------ A3 plan d'ossature + mur avant
def a3():
    f = Feuille(3, "Ossature des murs : plan et mur avant")
    v = Vue(150, 880, 3.6)
    f.titre_vue(48, 64, "Plan des colombages", "vu de dessus, à la lisse ; axes aux 16\" mesurés depuis l'avant et depuis la gauche")
    f.R(v, 0, 0, EP, OSS_P, "trt")
    f.R(v, OSS_L - EP, 0, OSS_L, OSS_P, "trt")
    f.R(v, EP, OSS_P - EP, OSS_L - EP, OSS_P, "trt")
    f.R(v, EP, 0, OB_X0, EP, "trt")
    f.R(v, OB_X1, 0, OSS_L - EP, EP, "trt")
    for a, b in col_cote():
        f.R(v, 0, a, EP, b, "bois2")
        f.R(v, OSS_L - EP, a, OSS_L, b, "bois2")
    for a, b in col_fond():
        f.R(v, a, OSS_P - EP, b, OSS_P, "bois2")
    for a, b in col_avant():
        f.R(v, a, 0, b, EP, "bois2")
    for a in (OB_X0 - 3, OB_X0 - 1.5, OB_X1, OB_X1 + 1.5):
        f.R(v, a, 0, a + 1.5, EP, "bois")
    f.L(v, OB_X0, EP / 2, OB_X1, EP / 2, "ti")
    f.dh(v, 0, OSS_L, 0, 66, "12'-8\" hors ossature")
    f.dh(v, OB_X0, OB_X1, 0, 38, pp(OB_L) + " ouverture brute")
    f.dh(v, 0, OB_X0, 0, 38)
    f.dh(v, OB_X1, OSS_L, 0, 38)
    f.dv(v, 0, OSS_P, 0, -66, "16'-8\" hors ossature")
    for a, b in zip([0] + AXES[:3], AXES[:4]):
        f.dv(v, a, b, 0, -34)
    f.TV(v, 0, 108, "… aux 16\" jusqu'au fond", "dg", dx=-30, rot=-90)
    for a in (0, 16, 32):
        f.dh(v, a, a + 16, OSS_P, -28)
    f.TV(v, 84, OSS_P, "… aux 16\"", "dg", dy=-33)
    f.dh(v, EP, OSS_L - EP, 150, 0, pp(OSS_L - 2 * EP) + " entre les murs de côté")
    f.TV(v, CX, 112, "Les murs de côté filent d'un bout à l'autre (16'-8\").", "t")
    f.TV(v, CX, 112, "Les murs avant et arrière se montent entre les deux (12'-1\").", "t", dy=17)
    f.TV(v, CX, 186, "à chaque coin : 2 colombages, le 2ᵉ sert de fond de clouage", "s")
    f.TV(v, CX, 14, "de chaque côté de la porte : 1 colombage plein + 2 jambages", "s")
    f.T(v.X(CX), v.Y(0) + 92, "AVANT — la cour", "g")

    e = Vue(945, 730, 4.0)                       # mur avant vu de dehors
    f.titre_vue(830, 64, "Mur avant, vu de la cour", "ossature seule ; le pignon et les chevrons de rive par-dessus")
    f.L(e, -14, 0, OSS_L + 14, 0, "tr")
    f.R(e, 0, 0, OB_X0, BORD, "bet")
    f.R(e, OB_X1, 0, OSS_L, BORD, "bet")
    f.R(e, 0, BORD, OB_X0, BORD + 1.5, "trt")
    f.R(e, OB_X1, BORD, OSS_L, BORD + 1.5, "trt")
    for a, b in [(0, 1.5), (2, 3.5)] + col_avant() + [(OSS_L - 3.5, OSS_L - 2), (OSS_L - 1.5, OSS_L)]:
        f.R(e, a, BORD + 1.5, b, H_MUR - 3, "bois")
    for a in (OB_X0 - 3, OB_X0 - 1.5, OB_X1, OB_X1 + 1.5):
        f.R(e, a, BORD + 1.5, a + 1.5, OB_H, "bois2")
    f.R(e, OB_X0 - 3, OB_H, OB_X1 + 3, H_MUR - 3, "bois2")
    f.R(e, 0, H_MUR - 3, OSS_L, H_MUR - 1.5, "bois")
    f.R(e, 0, H_MUR - 1.5, OSS_L, H_MUR, "bois")
    f.R(e, OB_X0, 0, OB_X0 + 1.5, OB_H - 1.5, "ti")
    f.R(e, OB_X1 - 1.5, 0, OB_X1, OB_H - 1.5, "ti")
    f.R(e, OB_X0, OB_H - 1.5, OB_X1, OB_H, "ti")
    dessin_pignon(f, e)
    for x, lg in pignon():
        f.TV(e, x, H_MUR + 2.5, po(lg), "dg", dx=20, dy=-2)
    f.dh(e, 0, OSS_L, 0, 62, "12'-8\"")
    f.dh(e, OB_X0, OB_X1, 0, 34, pp(OB_L) + " ouverture brute")
    f.dh(e, 0, OB_X0, 0, 34)
    f.dh(e, OB_X1, OSS_L, 0, 34)
    f.dv(e, 0, OB_H, OB_X0 + 13, 0, pp(OB_H) + " brut")
    f.dv(e, BORD + 1.5, OB_H, OB_X1 - 9, 0, pp(OB_H - BORD - 1.5) + " jambage")
    f.dv(e, 0, BORD, 0, -62, "6\"")
    f.dv(e, BORD + 1.5, H_MUR - 3, 0, -62, pp(COL) + " colombage")
    f.dv(e, 0, H_MUR, 0, -90, "8'-0\"")
    f.dv(e, H_MUR, zt(0), 0, -90, cote(zt(0) - H_MUR))
    f.TV(e, CX, OB_H + LINT_H / 2, "linteau 2 − 2 × 8 de 8'-9\"", "tb", dy=5)
    f.TV(e, CX, 48, "ouverture finie 8'-0\" × 7'-0\"", "tb")
    f.TV(e, CX, 48, "après la doublure 2 × 6 (en tireté)", "s", dy=18)
    f.fleche(e, CX + 22, zt(22) - 3, e.X(CX + 34), e.Y(zt(16)), "chevron de rive 2 × 6")
    f.fleche(e, CX, zt(FAIT) - 4, e.X(CX - 12), e.Y(zt(0) + 2), "faîtière 2 × 8")
    f.notes(830, 826, "Notes", [
        "La dalle passe sous la porte ; la bordure et la lisse s'arrêtent à l'ouverture brute.",
        "Linteau : deux 2 × 8 de 8'-9\" avec un contreplaqué ½\" entre les deux, collé sous la sablière, porté par deux jambages de chaque côté.",
        "Doublure 2 × 6, traitée aux jambages : elle ramène l'ouverture à 8'-0\" × 7'-0\".",
        "Colombages de pignon aux 16\", coupés à 30¼° en tête ; longueurs en rouge, au long point.",
    ], 108, 18)
    return f


# ------------------------------------------------------------------ A4 murs de cote et du fond
def a4():
    f = Feuille(4, "Ossature des murs : côtés et fond")
    v = Vue(110, 540, 3.4)
    f.titre_vue(48, 64, "Mur de côté (deux pareils, en miroir)", "vu de dehors ; un chevron et une solive de plafond tombent sur chaque colombage")
    f.L(v, -10, 0, OSS_P + 10, 0, "tr")
    f.R(v, 0, 0, OSS_P, BORD, "bet")
    f.R(v, 0, BORD, OSS_P, BORD + 1.5, "trt")
    for a, b in col_cote():
        f.R(v, a, BORD + 1.5, b, H_MUR - 3, "bois")
    f.R(v, 0, H_MUR - 3, OSS_P, H_MUR - 1.5, "bois")
    f.R(v, 0, H_MUR - 1.5, OSS_P, H_MUR, "bois")
    f.L(v, 120, H_MUR - 3, 120, H_MUR - 1.5, "gros")
    f.L(v, 72, H_MUR - 1.5, 72, H_MUR, "gros")
    for a in [0.75] + AXES + [OSS_P - 0.75]:
        f.R(v, a - 0.75, H_MUR, a + 0.75, H_MUR + HAP, "bois2")
    for a in AXES:
        f.R(v, a + 0.75, H_MUR, a + 2.25, H_MUR + 5.5, "bois")
    f.R(v, 1.5, H_MUR, 3, H_MUR + 5.5, "bois")
    f.R(v, OSS_P - 3, H_MUR, OSS_P - 1.5, H_MUR + 5.5, "bois")
    for y in BOUL_COTE:
        f.C(v, y, BORD - 2.6, 3.2, "boul")
    f.dh(v, 0, OSS_P, 0, 60, "16'-8\" — l'avant à gauche, le fond à droite")
    ch = [0] + AXES + [OSS_P]
    for a, b in zip(ch, ch[1:]):
        f.dh(v, a, b, 0, 30, po(b - a))
    f.dv(v, 0, BORD, OSS_P, 28, "6\"")
    f.dv(v, BORD + 1.5, H_MUR - 3, OSS_P, 28, pp(COL))
    f.dv(v, 0, H_MUR, OSS_P, 56, "8'-0\"")
    f.fleche(v, 33.5, H_MUR + 4, v.X(38), v.Y(H_MUR + 26), "solive de plafond 2 × 6, clouée au flanc du chevron")
    f.fleche(v, 96, H_MUR + 3, v.X(102), v.Y(H_MUR + 15), "chevron 2 × 6, sur l'axe du colombage")

    e = Vue(985, 540, 3.0)
    f.titre_vue(940, 64, "Mur du fond, vu de dehors", "plein, sans ouverture ; même pignon qu'à l'avant")
    f.L(e, -10, 0, OSS_L + 10, 0, "tr")
    f.R(e, 0, 0, OSS_L, BORD, "bet")
    f.R(e, 0, BORD, OSS_L, BORD + 1.5, "trt")
    for a, b in [(0, 1.5), (2, 3.5)] + col_fond() + [(OSS_L - 3.5, OSS_L - 2), (OSS_L - 1.5, OSS_L)]:
        f.R(e, a, BORD + 1.5, b, H_MUR - 3, "bois")
    f.R(e, 0, H_MUR - 3, OSS_L, H_MUR - 1.5, "bois")
    f.R(e, 0, H_MUR - 1.5, OSS_L, H_MUR, "bois")
    dessin_pignon(f, e)
    f.dh(e, 0, OSS_L, 0, 30, "12'-8\"")
    f.dv(e, 0, H_MUR, OSS_L, 52, "8'-0\"")
    f.dv(e, H_MUR, zt(0), OSS_L, 52, cote(zt(0) - H_MUR))
    f.dv(e, 0, zt(0), OSS_L, 82, pp(zt(0)) + " dessus des chevrons")

    f.T(48, 660, "Pièces des murs", "h", "start")
    f.table(48, 674, ["Pièce", "Bois", "Longueur", "Qté"], [
        ["Colombages pleins", "2 × 4", pp(COL), "49"],
        ["Jambages de la porte", "2 × 4", pp(OB_H - BORD - 1.5), "4"],
        ["Lisses traitées, côtés", "2 × 4 traité", "16'-8\" (10' + 8')", "2"],
        ["Lisse traitée, fond", "2 × 4 traité", pp(OSS_L - 2 * EP), "1"],
        ["Lisses traitées, bouts du mur avant", "2 × 4 traité", po(OB_X0 - EP), "2"],
        ["Sablières, côtés (deux rangs)", "2 × 4", "16'-8\"", "4"],
        ["Sablières, avant et fond (deux rangs)", "2 × 4", "12'-1\" et 12'-8\"", "2 + 2"],
        ["Linteau", "2 × 8", "8'-9\"", "2"],
        ["Doublure de l'ouverture", "2 × 6", "2 de 7'-0\" traités, 1 de 8'-0\"", "3"],
        ["Colombages de pignon", "2 × 4", "voir A3", "16"],
    ], [290, 110, 250, 70])
    f.notes(830, 660, "Montage", [
        "Monter les deux murs de côté à plat sur la dalle, les lever, les étayer d'aplomb. Monter ensuite le fond et l'avant entre les deux.",
        "Lisse traitée boulonnée sur une mousse de lisse. Double sablière, joints décalés d'au moins 4' d'un rang à l'autre.",
        "Le rang du haut de la sablière croise les coins : il passe par-dessus le mur voisin et lie les quatre murs.",
        "Poser l'OSB avant le toit : c'est lui qui tient les murs d'équerre. Joints sur un colombage, clous aux 6\" en rive et aux 12\" ailleurs.",
        "Aux bouts du mur avant (2'-2½\" de chaque côté de la porte), clouer l'OSB aux 4\" : ce sont eux qui retiennent le pignon.",
    ], 104)
    return f


# ------------------------------------------------------------------ A5 toit
def a5():
    f = Feuille(5, "Charpente du toit : plan et coupe")
    v = Vue(150, 850, 3.1)                       # repere de l'ossature
    f.titre_vue(48, 64, "Plan des chevrons", "avant en bas ; murs en tireté ; 14 paires, plus une paire volante à chaque pignon")
    ys = [0.75] + AXES + [OSS_P - 0.75]
    x_g, x_d = CX - BOUT, CX + BOUT
    for y in ys:
        f.R(v, x_g, y - 0.75, CX - FAIT, y + 0.75, "bois")
        f.R(v, CX + FAIT, y - 0.75, x_d, y + 0.75, "bois")
    for y in (-12.5, OSS_P + 12.5):
        f.R(v, x_g, y - 0.75, CX - FAIT, y + 0.75, "bois2")
        f.R(v, CX + FAIT, y - 0.75, x_d, y + 0.75, "bois2")
    pas = 24 * COS
    for sg in (-1, 1):
        for i in range(1, int((BOUT - FAIT) // pas) + 1):
            x = CX + sg * (FAIT + i * pas)
            f.R(v, x - 0.75, -11.75, x + 0.75, 0, "bois")
            f.R(v, x - 0.75, OSS_P, x + 0.75, OSS_P + 11.75, "bois")
    f.R(v, CX - FAIT, -13.25, CX + FAIT, OSS_P + 13.25, "bois2")
    f.R(v, x_g - 1.5, -13.25, x_g, OSS_P + 13.25, "bois2")
    f.R(v, x_d, -13.25, x_d + 1.5, OSS_P + 13.25, "bois2")
    f.R(v, 0, 0, OSS_L, OSS_P, "ti")
    g, d = CX - 44, CX + 44
    f.TV(v, g, 184, "↑ chevron volant 2 × 6, sans entaille", "t", dy=4)
    f.TV(v, d, 184, "↑ blocs 2 × 6 de 10¼\" aux 24\"", "t", dy=4)
    f.TV(v, g, 136, "← sous-fascia 2 × 6", "t", dy=4)
    f.TV(v, d, 136, "sous-fascia 2 × 6 →", "t", dy=4)
    f.TV(v, g, 104, "chevron 2 × 6 de " + pp(L_CHEV), "tb", dy=4)
    f.TV(v, d, 104, "14 paires aux 16\"", "tb", dy=4)
    f.TV(v, g, 72, "faîtière 2 × 8 de 18'-10½\" →", "t", dy=4)
    f.TV(v, d, 72, "en 2 morceaux, joint sur une paire", "t", dy=4)
    f.TV(v, g, 40, "une solive de plafond 2 × 6", "t", dy=4)
    f.TV(v, d, 40, "au flanc de chaque paire", "t", dy=4)
    f.dh(v, x_g - 2.25, x_d + 2.25, -13.25, 58, "15'-0\" fascia à fascia")
    f.dh(v, 0, OSS_L, -13.25, 30, "12'-8\" ossature")
    f.dh(v, x_g - 2.25, 0, -13.25, 30, "14\"")
    f.dv(v, -14, OSS_P + 14, x_g - 1.5, -58, "19'-0\" fascia à fascia")
    f.dv(v, 0, OSS_P, x_g - 1.5, -30, "16'-8\" ossature")
    for a in (0, 16, 32):
        f.dv(v, a, a + 16, x_d + 1.5, 28, "16\"")
    f.dv(v, -14, 0, x_d + 1.5, 28, "14\"")

    c = Vue(1180, 700, 3.7)                      # coupe en travers, x depuis l'axe
    f.titre_vue(800, 64, "Coupe en travers", "une paire de chevrons, sa solive de plafond, les deux murs de côté")
    f.P(c, [(-98, -17), (98, -17), (98, -12), (64, -12), (56, -4), (-56, -4), (-64, -12), (-98, -12)], "gra")
    f.P(c, [(-76, -12), (-64, -12), (-56, -4), (56, -4), (64, -12), (76, -12), (76, BORD), (76 - EP, BORD), (76 - EP, 0),
            (-(76 - EP), 0), (-(76 - EP), BORD), (-76, BORD)], "bet")
    f.L(c, -98, -0.5, -76, -0.5, "sol")
    f.L(c, 76, -0.5, 98, -0.5, "sol")
    for sg in (-1, 1):
        a, b = sorted((sg * (CX - EP), sg * CX))
        f.R(c, a, BORD, b, BORD + 1.5, "trt")
        f.R(c, a, BORD + 1.5, b, H_MUR - 3, "bois")
        f.R(c, a, H_MUR - 3, b, H_MUR - 1.5, "bois2")
        f.R(c, a, H_MUR - 1.5, b, H_MUR, "bois2")
        p, q = sorted((sg * CX, sg * (CX + PAREMENT)))
        f.R(c, p, BORD - 1, q, zb(CX + PAREMENT) - 0.3, "par")
        p, q = sorted((sg * (CX - EP - CTP), sg * (CX - EP)))
        f.R(c, p, 0.5, q, H_MUR - 0.5, "ctp")
    f.R(c, -(CX - EP), H_MUR - 0.5, CX - EP, H_MUR, "ctp")
    xc = CX - (5.5 - HAP) / PENTE
    f.P(c, [(-CX, H_MUR), (CX, H_MUR), (CX, H_MUR + HAP), (xc, H_MUR + 5.5), (-xc, H_MUR + 5.5), (-CX, H_MUR + HAP)], "bois")
    for sg in (-1, 1):
        f.P(c, [(sg * FAIT, zt(FAIT)), (sg * BOUT, zt(BOUT)), (sg * BOUT, zb(BOUT)), (sg * CX, zb(CX)), (sg * CX, H_MUR),
                (sg * (CX - ASSISE), H_MUR), (sg * FAIT, zb(FAIT))], "bois2")
        f.P(c, [(0, zt(0) + REV_TOIT), (sg * 90, zt(90) + REV_TOIT), (sg * 90, zt(90)), (0, zt(0))], "osb")
        a, b = sorted((sg * BOUT, sg * (BOUT + 1.5)))
        f.R(c, a, zb(BOUT), b, zt(BOUT + 1.5), "bois")
        a, b = sorted((sg * (BOUT + 1.5), sg * 90))
        f.R(c, a, zb(BOUT) - 0.75, b, zt(90) + REV_TOIT, "par")
        a, b = sorted((sg * (CX + PAREMENT), sg * (BOUT + 1.5)))
        f.R(c, a, zb(BOUT) - 0.5, b, zb(BOUT), "par")
    f.R(c, -FAIT, zt(FAIT) - 7.25, FAIT, zt(FAIT), "bois")
    f.L(c, 0, -22, 0, zt(0) + 10, "axe")
    f.dh(c, -CX, CX, -17, 26, "12'-8\" hors ossature")
    f.dh(c, -(CX - EP - CTP), CX - EP - CTP, 14, 0, "12'-0\" fini")
    f.dh(c, CX + PAREMENT, 90, -17, 26, "12\"")
    f.dh(c, -90, -(CX + PAREMENT), -17, 26, "12\"")
    f.dh(c, -90, 90, -17, 54, "15'-0\" fascia à fascia")
    f.dv(c, 0, H_MUR, 90, 30, "8'-0\"")
    f.dv(c, H_MUR, zt(0), 90, 30, cote(zt(0) - H_MUR))
    f.dv(c, -0.5, Z_FAITE, 90, 60, pp(Z_FAITE + 0.5) + " du sol au faîte")
    f.dv(c, 0, H_MUR - 0.5, 10, 0, "7'-11½\" plafond fini")
    f.dv(c, 0, zb(BOUT) - 0.5, -90, -24, pp(zb(BOUT) - 0.5) + " sous le soffite")
    pente_symbole(f, c, 48, 128)
    f.fleche(c, -36, zt(36) - 3, c.X(-46), c.Y(zt(36) + 12), "chevron 2 × 6 aux 16\"")
    f.fleche(c, -20, zt(20) + 0.4, c.X(-28), c.Y(zt(20) + 13), "pontage ⅝\", membrane, bardeau")
    f.fleche(c, 0, zt(FAIT) - 4, c.X(9), c.Y(zt(0) + 5), "faîtière 2 × 8")
    f.fleche(c, -68, H_MUR + 3, c.X(-62), c.Y(82), "solive de plafond 2 × 6 aux 16\"")
    f.T(c.X(-62) + 4, c.Y(82) + 16, "12'-8\", 5 clous dans chaque chevron", "s", "start")
    f.fleche(c, -64, H_MUR - 0.25, c.X(-62), c.Y(64), "contreplaqué ½\" au plafond")
    f.fleche(c, CX - EP / 2, 80, c.X(66), c.Y(84), "colombage 2 × 4 aux 16\"")
    f.fleche(c, CX + 1, 68, c.X(66), c.Y(70), "OSB, fourrures, planches")
    f.fleche(c, CX - EP - CTP / 2, 54, c.X(66), c.Y(56), "contreplaqué ½\"")
    f.notes(800, 846, "Notes", [
        "Les solives de plafond retiennent le pied des chevrons, que la neige pousse vers dehors : n'en couper aucune. "
        "Les palans des vélos se vissent dedans.",
        "Soffites ventilés des deux côtés et une grille dans chaque pignon : l'entretoit doit respirer.",
        "Membrane autocollante sur 3 pi au bas de chaque versant, sous le bardeau.",
    ], 110)
    return f


# ------------------------------------------------------------------ A6 details et listes
def a6():
    f = Feuille(6, "Gabarit du chevron, corniche, mur et listes")
    k = 6.0
    z0 = 88.0
    v = Vue(96, 200 + (zt(FAIT) - H_MUR + 8) * k, k)     # x depuis l'axe ; z au-dessus de la dalle, moins 88
    f.titre_vue(48, 64, "Gabarit du chevron", "en couper un, l'essayer sur le mur, puis tracer les 31 autres dessus")

    def pt(x, z):
        return (x, z - z0)
    f.P(v, [pt(FAIT, zt(FAIT)), pt(BOUT, zt(BOUT)), pt(BOUT, zb(BOUT)), pt(CX, zb(CX)), pt(CX, H_MUR),
            pt(CX - ASSISE, H_MUR), pt(FAIT, zb(FAIT))], "bois")
    f.R(v, CX - ASSISE, H_MUR - 3 - z0, CX, H_MUR - z0, "bois2")
    f.L(v, CX - ASSISE, H_MUR - 1.5 - z0, CX, H_MUR - 1.5 - z0, "fin")
    f.L(v, CX, H_MUR - z0, CX, zt(CX) - z0, "ti")
    yy = zt(FAIT) - z0 + 3
    f.dh(v, FAIT, CX, yy, -20, po(L_TALON) + " sur le dessus, du faîte à l'aplomb du mur")
    f.dh(v, CX, BOUT, yy, -20, po(L_QUEUE))
    f.dh(v, FAIT, BOUT, yy, -48, f"longueur totale {pp(L_CHEV)}, dans un 2 × 6 de 10'")
    f.dh(v, FAIT, CX, zb(BOUT) - z0 - 5, 24, pp(CX - FAIT) + " à l'horizontale")
    f.dh(v, CX, BOUT, zb(BOUT) - z0 - 5, 24, po(BOUT - CX))
    f.fleche(v, FAIT, zt(FAIT) - z0 - 3, v.X(8), v.Y(zb(8) - z0 - 10), "coupe d'aplomb au faîte")
    f.T(120, 366, "Coupes d'aplomb à 30¼° :", "t", "start")
    f.T(120, 383, "7 sur 12 à l'équerre de charpente.", "t", "start")

    w = Vue(150 - (CX - 10) * 8, 580 + 86 * 8, 8.0)           # entaille grossie
    f.T(150, 412, "L'entaille, grossie", "tb", "start")
    f.P(w, [(CX - 10, zt(CX - 10)), (BOUT, zt(BOUT)), (BOUT, zb(BOUT)), (CX, zb(CX)), (CX, H_MUR),
            (CX - ASSISE, H_MUR), (CX - 10, zb(CX - 10))], "bois")
    f.R(w, CX - ASSISE, H_MUR - 3, CX, H_MUR - 1.5, "bois2")
    f.R(w, CX - ASSISE, H_MUR - 1.5, CX, H_MUR, "bois2")
    f.L(w, CX, H_MUR, CX, zt(CX), "ti")
    f.dh(w, CX - ASSISE, CX, H_MUR - 3, 20, "3½\"")
    f.T(w.X(CX - ASSISE) - 8, w.Y(H_MUR - 3) + 19, "à plat", "dg", "end")
    f.dv(w, zb(CX), H_MUR, CX, 112, po(ENT_PL))
    f.dv(w, H_MUR, zt(CX), CX, 112, po(HAP))
    f.T(w.X(CX) + 122, w.Y(H_MUR - 1) + 4, "d'aplomb", "dg", "start")
    f.T(w.X(CX) + 122, w.Y(H_MUR + 2.2) + 4, "de bois qui reste", "dg", "start")

    m = Vue(700, 300, 10.0)                       # composition du mur, coupe horizontale
    f.titre_vue(700, 64, "Composition du mur", "coupe à l'horizontale, dehors en haut")
    f.R(m, 0, 0.75, 30, 1.5, "par")
    for x in (2, 14, 26):
        f.R(m, x - 0.75, 1.5, x + 0.75, 2.25, "par")
    f.R(m, 0, 0, 30, 0.75, "bois2")
    f.R(m, 0, -0.44, 30, 0, "osb")
    for x in (1, 17):
        f.R(m, x - 0.75, -3.94, x + 0.75, -0.44, "bois")
    f.R(m, 0, -4.44, 30, -3.94, "ctp")
    f.dh(m, 1, 17, -4.44, 26, "16\"")
    f.dh(m, 2, 14, 2.25, -18, "12\"")
    f.dv(m, -4.44, 1.5, 30, 28, "6\"")
    for i, t in enumerate(["De dehors à dedans :", "couvre-joint 1 × 2 aux 12\"", "planche verticale ¾\"",
                           "fourrure 1 × 3 horizontale aux 24\"", "membrane pare-intempéries", "OSB 7/16\"",
                           "colombage 2 × 4 aux 16\"", "contreplaqué ½\""]):
        f.T(700, 410 + i * 18, t, "tb" if i == 0 else "n", "start")

    k = 7.5
    c = Vue(1215 - 62 * k, 480, k)                # corniche ; z au-dessus de la dalle, moins 80
    f.titre_vue(1160, 64, "Corniche", "bas de versant, sur un mur de côté")

    def q(x, z):
        return (x, z - 80)
    f.R(c, CX - EP, 0, CX, H_MUR - 3 - 80, "bois")
    f.R(c, CX - EP, H_MUR - 3 - 80, CX, H_MUR - 1.5 - 80, "bois2")
    f.R(c, CX - EP, H_MUR - 1.5 - 80, CX, H_MUR - 80, "bois2")
    f.R(c, CX, 0, CX + PAREMENT, zb(CX + PAREMENT) - 80.3, "par")
    f.R(c, CX - EP - CTP, 0, CX - EP, H_MUR - 80.5, "ctp")
    f.R(c, 62, H_MUR - 80.5, CX - EP, H_MUR - 80, "ctp")
    xc = CX - (5.5 - HAP) / PENTE
    f.P(c, [q(62, H_MUR), q(CX, H_MUR), q(CX, H_MUR + HAP), q(xc, H_MUR + 5.5), q(62, H_MUR + 5.5)], "bois")
    f.P(c, [q(62, zt(62)), q(BOUT, zt(BOUT)), q(BOUT, zb(BOUT)), q(CX, zb(CX)), q(CX, H_MUR), q(CX - ASSISE, H_MUR), q(62, zb(62))], "bois2")
    f.P(c, [q(62, zt(62) + REV_TOIT), q(90, zt(90) + REV_TOIT), q(90, zt(90)), q(62, zt(62))], "osb")
    f.R(c, BOUT, zb(BOUT) - 80, BOUT + 1.5, zt(BOUT + 1.5) - 80, "bois")
    f.R(c, BOUT + 1.5, zb(BOUT) - 80.75, 90, zt(90) + REV_TOIT - 80, "par")
    f.R(c, CX + PAREMENT, zb(BOUT) - 80.5, BOUT + 1.5, zb(BOUT) - 80, "par")
    f.R(c, CX + PAREMENT, zb(BOUT) - 80, CX + PAREMENT + 1.5, zb(BOUT) - 78.5, "bois")
    f.dh(c, CX + PAREMENT, 90, 0, 24, "12\" fini")
    f.dh(c, CX, BOUT, 0, 54, po(BOUT - CX))
    f.T(c.X((CX + BOUT) / 2), c.Y(0) + 70, "du mur au bout du chevron", "dg")
    xr = c.X(90) + 18
    f.fleche(c, BOUT + 0.75, zb(BOUT) - 77, xr, c.Y(zb(BOUT) - 75), "sous-fascia 2 × 6")
    f.fleche(c, 89.6, zb(BOUT) - 79, xr, c.Y(zb(BOUT) - 78.5), "fascia 1 × 8")
    f.fleche(c, 84, zb(BOUT) - 80.25, xr, c.Y(zb(BOUT) - 82), "soffite ventilé")
    xg = c.X(62) - 8
    f.fleche(c, 64, zt(64) - 83, xg, c.Y(zt(62) - 86), "chevron 2 × 6")
    f.fleche(c, 64, H_MUR - 77, xg, c.Y(H_MUR - 77.5), "solive, 5 clous de 3¼\"")
    f.fleche(c, CX - 1.75, H_MUR - 80, xg, c.Y(H_MUR - 85), "3 clous en biais + étrier")

    y0 = 652
    f.T(48, y0 - 14, "Liste de bois de charpente", "h", "start")
    f.table(48, y0, ["Bois", "Sert à", "Qté"], [
        ["2 × 4 × 8'", "colombages, jambages, pignons, blocs de coin", "64"],
        ["2 × 4 traité", "lisses : 2 de 10', 3 de 8', 1 de 14'", "6"],
        ["2 × 4", "sablières : 4 de 10', 4 de 8', 4 de 14'", "12"],
        ["2 × 6 × 10'", "32 chevrons, 4 sous-fascias, 2 pour les blocs", "38"],
        ["2 × 6 × 14'", "solives de plafond (12'-8\")", "14"],
        ["2 × 8 × 10'", "2 pour le linteau, 2 pour la faîtière", "4"],
        ["2 × 6", "doublure de la porte : 2 de 8' traités, 1 de 10'", "3"],
        ["OSB 7/16\" 4 × 8", "murs et pignons", "16"],
        ["Pontage ⅝\" 4 × 8", "toit, avec agrafes en H entre les chevrons", "12"],
        ["Contreplaqué ½\" 4 × 8", "murs (13) et plafond (6), plus le linteau", "20"],
        ["Fourrure 1 × 3", "horizontale aux 24\", pieds linéaires", "340"],
    ], [150, 340, 50])
    f.T(48, y0 + 21 * 12 + 22, "À recompter avant d'acheter. Planches, bardeau et finition ne sont pas dans la liste.", "s", "start")

    f.T(620, y0 - 14, "Clouage", "h", "start")
    f.table(620, y0, ["Assemblage", "Clous"], [
        ["Colombage sur lisse et sablière", "2 de 3¼\" en bout"],
        ["Sablière double", "3¼\" aux 16\", 4 à chaque joint"],
        ["Linteau (les deux 2 × 8)", "3¼\" aux 12\", en quinconce"],
        ["Chevron sur sablière", "3 de 3¼\" en biais + étrier"],
        ["Chevron sur solive de plafond", "5 de 3¼\" (calculé pour la poussée)"],
        ["Chevron sur faîtière", "3 de 3¼\""],
        ["Bloc d'échelle", "3 de 3¼\" à chaque bout"],
        ["OSB des murs", "2⅜\" aux 6\" en rive, 12\" ailleurs"],
        ["Pontage du toit", "2⅜\" aux 6\" en rive, 12\" ailleurs"],
    ], [240, 290])
    f.notes(1190, y0 - 14, "Porte de garage", [
        "Ouverture finie = grandeur de la porte : 8'-0\" × 7'-0\".",
        "Ressorts de torsion : 12\" au-dessus en standard, 14\" avec un ouvre-porte ; 5\" et 7\" au minimum, en quincaillerie basse.",
        "Ici 11½\" sous le plafond : le dire en commandant la porte.",
        "6\" au moins de chaque côté (on en a 24) et 9'-0\" de profondeur libre au plafond (on en a 16').",
        "Fond de clouage 2 × 6 au milieu du pignon, au-dessus du linteau, pour le ressort.",
    ], 54)
    return f


def main():
    os.makedirs(os.path.join(ICI, "svg"), exist_ok=True)
    feuilles = [a1(), a2(), a3(), a4(), a5(), a6()]
    for f in feuilles:
        with open(os.path.join(ICI, "svg", f"A{f.no}.svg"), "w", encoding="utf-8") as h:
            h.write(f.svg())
    corps = "\n".join(f'<div class="p">{f.svg()}</div>' for f in feuilles)
    with open(os.path.join(ICI, "plans.html"), "w", encoding="utf-8") as h:
        h.write('<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Plans du cabanon</title><style>'
                '@page{size:17in 11in;margin:0}html,body{margin:0}'
                '.p{width:17in;height:11in;page-break-after:always;overflow:hidden}.p svg{width:17in;height:11in;display:block}'
                '</style></head><body>' + corps + '</body></html>')
    print(f"ossature {OSS_L} x {OSS_P} ; colombage {COL} ; chevron {L_CHEV:.2f} ({L_TALON:.2f} + {L_QUEUE:.2f}) ; "
          f"HAP {HAP:.3f} ; entaille {ENT_PL:.3f} ; faite {Z_FAITE:.2f} ; diagonale {math.hypot(OSS_L, OSS_P):.2f}")


if __name__ == "__main__":
    main()
