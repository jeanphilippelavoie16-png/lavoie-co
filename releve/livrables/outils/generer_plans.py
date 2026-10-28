#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generer_plans.py — Générateur des plans du relevé de l'existant.

Transforme maison.json (schéma figé, voir travail/SCHEMA.md §4 et §6) en :
  svg/<feuille>_<slug>.svg      une feuille tabloïd 17×11 po par niveau (calques Inkscape)
  pdf/plans_existants.pdf       toutes les feuilles, à l'échelle exacte
  png/<feuille>_<slug>.png      aperçus 150 ppp
  dxf/<feuille>_<slug>.dxf      géométrie en pouces réels (repère maison), R2010
  donnees/tableau_pieces.csv    tableau des pièces (Excel Québec)
  donnees/verifications.txt     rapport des contrôles

Usage :  python3 generer_plans.py [--json ../donnees/maison.json] [--sortie ..]

Sortie déterministe : aucune date système, aucun aléatoire.
"""
import argparse
import csv
import glob
import hashlib
import io
import json
import math
import os
import re
import sys
import unicodedata

from shapely import STRtree, affinity
from shapely.geometry import (LineString, MultiLineString, MultiPolygon, Point,
                              Polygon, GeometryCollection, box as sbox)
from shapely.ops import nearest_points, polylabel, unary_union

# ---------------------------------------------------------------------------
# Constantes de mise en page
# ---------------------------------------------------------------------------
CALQUES = ["00-Cartouche", "10-Murs", "20-Ouvertures", "30-Escaliers-Elements",
           "40-Structure", "50-Cotes", "60-Etiquettes", "70-Incertitudes",
           "90-RENO-Propose"]
ORANGE = "#E8730C"
POLICE = "Arial, Helvetica, sans-serif"
CAP = 0.716            # hauteur des capitales / taille de police (Arial)
FEUILLE_L, FEUILLE_H = 17.0, 11.0      # po imprimés (tabloïd paysage)
MARGE = 0.25                           # cadre de feuille
CART_L = 3.2                           # largeur du cartouche (po imprimés)
ZONE = (MARGE + 0.1, MARGE + 0.1, FEUILLE_L - MARGE - CART_L - 0.1, FEUILLE_H - MARGE - 0.1)
# (dénominateur, libellé, graduations de l'échelle graphique en pi)
ECHELLES = [(48, '1/4" = 1\'-0"', (0, 2, 4, 8)),
            (64, '3/16" = 1\'-0"', (0, 4, 8, 12)),
            (96, '1/8" = 1\'-0"', (0, 4, 8, 16))]
# Cotation (mm imprimés)
C_D1 = 8.0       # face du bâtiment → 1re chaîne
C_ESP = 7.0      # espacement entre chaînes
C_GAP = 0.8      # ligne de cote → bas du texte
C_DEP = 1.5      # dépassement des lignes d'attache au-delà de la ligne de cote
C_ECART = 1.5    # écart objet → début de ligne d'attache
C_TICK = 2.6     # longueur du trait oblique
H_COTE = 2.5     # hauteur des capitales (mm) : cotes, notes, libellés
H_NOM = 4.0      # noms de pièces
H_FACADE = 3.5
TRI = 4.0        # côté du triangle de repère ⚠ (mm)

ORDRE_SRC = ["LU", "DÉDUIT", "ESTIMÉ", "PRÉSUMÉ", "ILLISIBLE"]
T_DEFAUT = {"ext": 6.0, "fondation": 10.0, "int": 4.5}

# Styles : remplissage, trait, épaisseur (mm), tirets (mm), épaisseur DXF (1/100 mm), type de ligne DXF
STYLES = {
    "fond": ("#FFFFFF", None, 0, None),
    "masque": ("#FFFFFF", None, 0, None),
    "mur-lourd": ("#4D4D4D", None, 0, None),
    "mur-leger": ("#C8C8C8", None, 0, None),
    "mur-lourd-c": (None, "#000000", 0.70, None),
    "mur-leger-c": (None, "#000000", 0.50, None),
    "ouv": (None, "#000000", 0.25, None),
    "ouv-fin": (None, "#000000", 0.18, None),
    "ouv-tir": (None, "#000000", 0.25, (1.5, 1.0)),
    "elem": (None, "#000000", 0.25, None),
    "elem-fin": (None, "#000000", 0.18, None),
    "elem-tir": (None, "#000000", 0.25, (1.5, 1.0)),
    "elem-plein": ("#000000", None, 0, None),
    "elem-blanc": ("#FFFFFF", "#000000", 0.25, None),
    "str": (None, "#000000", 0.35, None),
    "str-fin": (None, "#000000", 0.25, None),
    "str-poutre": (None, "#000000", 0.35, (6.0, 1.5)),
    "str-axe": (None, "#000000", 0.35, (8.0, 1.5, 1.0, 1.5)),
    "str-tir": (None, "#000000", 0.25, (2.5, 1.2)),
    "str-plein": ("#000000", None, 0, None),
    "cote": (None, "#000000", 0.18, None),
    "cote-tick": (None, "#000000", 0.35, None),
    "rappel": (None, "#000000", 0.18, None),
    "inc": (ORANGE, None, 0, None),
    "inc-c": (None, ORANGE, 0.25, None),
    "inc-blanc": ("#FFFFFF", None, 0, None),
    "cart-cadre": (None, "#000000", 0.70, None),
    "cart-l": (None, "#000000", 0.35, None),
    "cart-f": (None, "#000000", 0.18, None),
    "cart-noir": ("#000000", None, 0, None),
    "cart-blanc": ("#FFFFFF", "#000000", 0.18, None),
    "cart-lourd": ("#4D4D4D", "#000000", 0.35, None),
    "cart-leger": ("#C8C8C8", "#000000", 0.25, None),
    "invisible": (None, None, 0, None),
}
DXF_LT = {"str-poutre": ("DASHED", 7.5), "str-axe": ("DASHDOT", 12.0), "str-tir": ("HIDDEN", 3.7),
          "ouv-tir": ("HIDDEN", 2.5), "elem-tir": ("HIDDEN", 2.5)}


# ---------------------------------------------------------------------------
# Outils généraux
# ---------------------------------------------------------------------------
def sans_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def norm_src(s):
    if not s:
        return None
    s0 = sans_accents(str(s)).strip().upper()
    for v in ORDRE_SRC:
        if sans_accents(v) == s0:
            return v
    return None


def num(v):
    """Nombre, ou objet dimension → valeur numérique ; sinon None."""
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, dict):
        return num(v.get("valeur"))
    return None


def src(v):
    return norm_src(v.get("source")) if isinstance(v, dict) else None


def pire_source(liste):
    rangs = [ORDRE_SRC.index(s) for s in liste if s in ORDRE_SRC]
    return ORDRE_SRC[max(rangs)] if rangs else ""


FRAC = {0: "", 1: "¼", 2: "½", 3: "¾"}


def pipo(v):
    """Pouces → texte pi-po arrondi au 1/4 po (12'-6½")."""
    q = int(round(abs(v) * 4 + 1e-9))
    pi, r = divmod(q, 48)
    po, f = divmod(r, 4)
    s = f"{pi}'-{po}{FRAC[f]}\"" if pi else f"{po}{FRAC[f]}\""
    return ("-" + s) if (v < 0 and q) else s


def metres(v):
    return f"{abs(v) * 0.0254:.2f}".replace(".", ",") + " m"


def fr(v, d=2):
    return f"{v:.{d}f}".replace(".", ",")


def f3(v):
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "", "-") else s


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def slugify(s):
    s = sans_accents(str(s)).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "niveau"


def rot2(p, ang):
    a = math.radians(ang)
    c, s = math.cos(a), math.sin(a)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def polys_de(g):
    if g is None or g.is_empty:
        return []
    if isinstance(g, Polygon):
        return [g]
    if isinstance(g, (MultiPolygon, GeometryCollection)):
        out = []
        for x in g.geoms:
            out += polys_de(x)
        return out
    return []


def lignes_de(g):
    if g is None or g.is_empty:
        return []
    if isinstance(g, LineString):
        return [list(g.coords)]
    if isinstance(g, (MultiLineString, GeometryCollection)):
        out = []
        for x in g.geoms:
            out += lignes_de(x)
        return out
    if isinstance(g, Polygon):
        return [list(g.exterior.coords)] + [list(i.coords) for i in g.interiors]
    if isinstance(g, MultiPolygon):
        out = []
        for x in g.geoms:
            out += lignes_de(x)
        return out
    return []


# ---------------------------------------------------------------------------
# Métrique du texte (Liberation Sans = métriques d'Arial)
# ---------------------------------------------------------------------------
class Metrique:
    def __init__(self):
        self.f = {}
        try:
            from PIL import ImageFont
            for gras, nom in ((False, "LiberationSans-Regular.ttf"), (True, "LiberationSans-Bold.ttf")):
                cand = sorted(glob.glob("/usr/share/fonts/**/" + nom, recursive=True))
                if cand:
                    self.f[gras] = ImageFont.truetype(cand[0], 1000)
        except Exception:
            self.f = {}

    def l(self, txt, taille, gras=False):
        f = self.f.get(gras)
        if f is not None:
            return f.getlength(txt) / 1000.0 * taille
        return 0.6 * taille * len(txt)


MET = Metrique()


def haut_txt(s):
    return 0.93 if any(c in "ÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ" for c in s) else 0.76


def boite(x, y, larg, f, ancre="middle", rot=0.0, pad=0.0, s=""):
    """Boîte englobante d'un texte (ligne de base en (x, y))."""
    x0 = {"start": 0.0, "middle": -larg / 2, "end": -larg}[ancre]
    top = haut_txt(s) * f
    b = Polygon([(x0 - pad, -0.21 * f - pad), (x0 + larg + pad, -0.21 * f - pad),
                 (x0 + larg + pad, top + pad), (x0 - pad, top + pad)])
    if rot:
        b = affinity.rotate(b, rot, origin=(0, 0))
    return affinity.translate(b, x, y)


def couper(txt, f, lmax, gras=False):
    mots, lignes, cur = str(txt).split(), [], ""
    for m in mots:
        essai = (cur + " " + m).strip()
        if cur and MET.l(essai, f, gras) > lmax:
            lignes.append(cur)
            cur = m
        else:
            cur = essai
    if cur:
        lignes.append(cur)
    return lignes or [""]


# ---------------------------------------------------------------------------
# Rapport de vérifications
# ---------------------------------------------------------------------------
SECTIONS = ["Identifiants", "Murs", "Ouvertures", "Pièces", "Bilan de surface",
            "Chaînes de cotes", "Repères d'incertitude", "Textes (chevauchements)", "Mise en page"]


class Verif:
    def __init__(self):
        self.items = {s: [] for s in SECTIONS}

    def add(self, sect, statut, msg):
        self.items[sect].append((statut, msg))

    def compte(self, sect):
        c = {"ERREUR": 0, "AVERT": 0}
        for st, _ in self.items[sect]:
            if st in c:
                c[st] += 1
        return c


# ---------------------------------------------------------------------------
# Dessin : primitives en coordonnées maison (pouces réels, y vers le haut)
# ---------------------------------------------------------------------------
class Dessin:
    def __init__(self):
        self.groupes = {c: [] for c in CALQUES}

    def g(self, calque, gid=None):
        lst = []
        self.groupes[calque].append((gid, lst))
        return lst


def P_pl(pts, st, ferme=False):
    return {"k": "pl", "pts": [tuple(p) for p in pts], "st": st, "ferme": ferme}


def P_poly(rings, st):
    return {"k": "poly", "rings": [[tuple(p) for p in r] for r in rings], "st": st}


def P_arc(c, r, a0, da, st):
    return {"k": "arc", "c": tuple(c), "r": r, "a0": a0, "da": da, "st": st}


def P_cercle(c, r, st):
    return {"k": "cercle", "c": tuple(c), "r": r, "st": st}


def P_txt(x, y, s, f, ancre="middle", rot=0.0, gras=False, coul="#000000"):
    return {"k": "txt", "x": x, "y": y, "s": s, "f": f, "ancre": ancre, "rot": rot, "gras": gras, "coul": coul}


def poly_prims(g, st):
    return [P_poly([list(p.exterior.coords)[:-1]] + [list(i.coords)[:-1] for i in p.interiors], st)
            for p in polys_de(g)]


def geom_prim(p):
    """Géométrie shapely (traits) d'une primitive, pour la détection des chevauchements."""
    k = p["k"]
    if k == "pl":
        pts = p["pts"] + ([p["pts"][0]] if p["ferme"] else [])
        return LineString(pts) if len(pts) >= 2 else None
    if k == "poly":
        rings = p["rings"]
        if not rings or len(rings[0]) < 3:
            return None
        return Polygon(rings[0], rings[1:])
    if k == "arc":
        n = 16
        pts = [(p["c"][0] + p["r"] * math.cos(math.radians(p["a0"] + p["da"] * i / n)),
                p["c"][1] + p["r"] * math.sin(math.radians(p["a0"] + p["da"] * i / n))) for i in range(n + 1)]
        return LineString(pts)
    if k == "cercle":
        return Point(p["c"]).buffer(p["r"], 8).exterior
    return None


def transformer(p, f, drot):
    q = dict(p)
    k = p["k"]
    if k == "pl":
        q["pts"] = [f(a) for a in p["pts"]]
    elif k == "poly":
        q["rings"] = [[f(a) for a in r] for r in p["rings"]]
    elif k in ("arc", "cercle"):
        q["c"] = f(p["c"])
        if k == "arc":
            q["a0"] = p["a0"] + drot
    elif k == "txt":
        q["x"], q["y"] = f((p["x"], p["y"]))
        q["rot"] = p["rot"] + drot
    return q


# ---------------------------------------------------------------------------
# Placement des textes sans chevauchement
# ---------------------------------------------------------------------------
class Placeur:
    def __init__(self):
        self.L, self.Lo = [], []      # traits
        self.Z, self.Zo = [], []      # zones (aires d'éléments, pour les étiquettes de pièces)
        self.T, self.To, self.Td = [], [], []
        self._t = {"L": None, "Z": None, "T": None}

    def ligne(self, g, own):
        if g is not None and not g.is_empty:
            self.L.append(g)
            self.Lo.append(own)
            self._t["L"] = None

    def prims(self, prims, own):
        for p in prims:
            if p["k"] != "txt":
                g = geom_prim(p)
                if p["k"] == "poly" and g is not None and STYLES[p["st"]][0] in ("#FFFFFF",):
                    continue
                self.ligne(g, own)

    def zone(self, g, own):
        if g is not None and not g.is_empty:
            self.Z.append(g)
            self.Zo.append(own)
            self._t["Z"] = None

    def texte(self, g, own, desc):
        self.T.append(g)
        self.To.append(own)
        self.Td.append(desc)
        self._t["T"] = None

    def _arbre(self, k):
        if self._t[k] is None:
            lst = {"L": self.L, "Z": self.Z, "T": self.T}[k]
            self._t[k] = STRtree(lst) if lst else False
        return self._t[k]

    def conflits(self, g, ignore=(), zones=False):
        n = 0
        for k, owners in (("L", self.Lo), ("T", self.To)) + ((("Z", self.Zo),) if zones else ()):
            t = self._arbre(k)
            if not t:
                continue
            for i in t.query(g, predicate="intersects"):
                if owners[int(i)] in ignore:
                    continue
                n += 1
        return n


# ---------------------------------------------------------------------------
# Modèle : murs et ouvertures
# ---------------------------------------------------------------------------
class Mur:
    def __init__(self, d):
        self.d = d
        self.id = str(d.get("id"))
        self.type = str(d.get("type") or "int").lower()
        if self.type not in T_DEFAUT:
            self.type = "int"
        self.p1 = (float(d["x1"]), float(d["y1"]))
        self.p2 = (float(d["x2"]), float(d["y2"]))
        dx, dy = self.p2[0] - self.p1[0], self.p2[1] - self.p1[1]
        self.L = math.hypot(dx, dy)
        self.u = (dx / self.L, dy / self.L)
        self.n = (-self.u[1], self.u[0])          # gauche en regardant de p1 vers p2
        t = num(d.get("epaisseur"))
        self.t_src = src(d.get("epaisseur"))
        self.t_defaut = False
        if t is None or t <= 0:
            t = T_DEFAUT[self.type]
            self.t_defaut = True
            self.t_src = "PRÉSUMÉ"
        self.t = t
        self.e0 = self.e1 = 0.0
        self.ouvs = []
        self.lourd = self.type in ("ext", "fondation")

    def pt(self, s, o=0.0):
        return (self.p1[0] + self.u[0] * s + self.n[0] * o, self.p1[1] + self.u[1] * s + self.n[1] * o)

    def rect(self, s0, s1, o0, o1):
        return Polygon([self.pt(s0, o0), self.pt(s1, o0), self.pt(s1, o1), self.pt(s0, o1)])

    def emprise(self):
        return self.rect(-self.e0, self.L + self.e1, -self.t / 2, self.t / 2)

    def axe(self):
        return LineString([self.p1, self.p2])


def prolongements(murs):
    """Prolonge les extrémités qui aboutissent à un autre mur jusqu'à sa face opposée (coins propres)."""
    for A in murs:
        for fin in (0, 1):
            E = A.p1 if fin == 0 else A.p2
            uo = (-A.u[0], -A.u[1]) if fin == 0 else A.u
            best = 0.0
            for B in murs:
                if B is A:
                    continue
                cr = uo[0] * B.u[1] - uo[1] * B.u[0]
                if abs(cr) < 0.2:
                    continue
                w = (E[0] - B.p1[0], E[1] - B.p1[1])
                s = -(w[0] * B.u[1] - w[1] * B.u[0]) / cr
                demi = B.t / 2 / abs(cr)
                if abs(s) > demi + 1.0:
                    continue
                P = (E[0] + s * uo[0], E[1] + s * uo[1])
                tb = (P[0] - B.p1[0]) * B.u[0] + (P[1] - B.p1[1]) * B.u[1]
                if tb < -B.t - 1 or tb > B.L + B.t + 1:
                    continue
                best = max(best, s + demi)
            best = min(best, 2 * max(m.t for m in murs))
            if fin == 0:
                A.e0 = best
            else:
                A.e1 = best


class Ouv:
    def __init__(self, d, mur):
        self.d = d
        self.id = str(d.get("id"))
        self.type = str(d.get("type") or "porte").lower()
        op = d.get("operation")
        if not op:
            op = {"porte": "battante", "porte-patio": "coulissante", "fenetre": "coulissante",
                  "arche": "aucune", "porte-garage": "aucune"}.get(self.type, "battante")
        self.op = str(op).lower()
        self.mur = mur
        self.pos = num(d.get("position"))
        self.w = num(d.get("largeur"))
        sens = d.get("sens") if isinstance(d.get("sens"), dict) else {}
        self.charniere = sens.get("charniere") if sens.get("charniere") in ("debut", "fin") else None
        self.ouvre = sens.get("ouvre_vers") if sens.get("ouvre_vers") in ("gauche", "droite") else None
        self.valide = self.pos is not None and self.w is not None and self.w > 0
        if self.valide:
            self.a = self.pos - self.w / 2
            self.b = self.pos + self.w / 2

    def est_porte(self):
        return self.type in ("porte", "porte-patio", "porte-garage")

    def besoin_sens(self):
        if self.type == "fenetre" or self.type == "arche":
            return None
        if self.op == "battante":
            return ("charniere", "ouvre_vers")
        if self.op in ("double", "pliante"):
            return ("ouvre_vers",)
        return None


# ---------------------------------------------------------------------------
# Symboles d'ouvertures
# ---------------------------------------------------------------------------
def dessin_ouverture(o, mm):
    m = o.mur
    hw = m.t / 2
    a, b, c, w = o.a, o.b, o.pos, o.w
    P = m.pt
    pr = []
    typ, op = o.type, o.op

    def battant(h_s, f_s, sg, larg):
        H = P(h_s, sg * hw)
        F = P(f_s, sg * hw)
        nv = (m.n[0] * sg, m.n[1] * sg)
        O = (H[0] + nv[0] * larg, H[1] + nv[1] * larg)
        a_f = math.degrees(math.atan2(F[1] - H[1], F[0] - H[0]))
        a_o = math.degrees(math.atan2(nv[1], nv[0]))
        da = (a_o - a_f + 180) % 360 - 180
        return [P_pl([H, O], "ouv"), P_arc(H, larg, a_f, da, "ouv-fin")]

    if typ == "fenetre" or (op == "fixe" and typ != "arche"):
        pr.append(P_pl([P(a, -hw), P(b, -hw)], "ouv"))
        pr.append(P_pl([P(a, hw), P(b, hw)], "ouv"))
        pr.append(P_pl([P(a, 0), P(b, 0)], "ouv-fin"))
        pr.append(P_pl([P(a, -hw), P(a, hw)], "ouv"))
        pr.append(P_pl([P(b, -hw), P(b, hw)], "ouv"))
    elif typ == "arche" or op == "aucune" and typ != "porte-garage":
        pr.append(P_pl([P(a, -hw), P(b, -hw)], "ouv-tir"))
        pr.append(P_pl([P(a, hw), P(b, hw)], "ouv-tir"))
    elif op == "coulissante":
        ep = max(0.75, min(1.75, m.t / 4))
        o1 = m.t / 6
        pr.append(P_pl([P(a, o1 - ep / 2), P(c + 2, o1 - ep / 2), P(c + 2, o1 + ep / 2), P(a, o1 + ep / 2)], "ouv", True))
        pr.append(P_pl([P(c - 2, -o1 - ep / 2), P(b, -o1 - ep / 2), P(b, -o1 + ep / 2), P(c - 2, -o1 + ep / 2)], "ouv", True))
        pr.append(P_pl([P(a, -hw), P(a, hw)], "ouv-fin"))
        pr.append(P_pl([P(b, -hw), P(b, hw)], "ouv-fin"))
    elif typ == "porte-garage":
        pr.append(P_pl([P(a, -1), P(b, -1), P(b, 1), P(a, 1)], "ouv", True))
    elif op == "pliante" and o.ouvre:
        sg = 1 if o.ouvre == "gauche" else -1
        if w >= 36:
            pr.append(P_pl([P(a, sg * hw), P(a + w / 4, sg * (hw + w / 5)), P(c, sg * hw)], "ouv"))
            pr.append(P_pl([P(b, sg * hw), P(b - w / 4, sg * (hw + w / 5)), P(c, sg * hw)], "ouv"))
        else:
            h_s, f_s = (a, b) if o.charniere != "fin" else (b, a)
            pr.append(P_pl([P(h_s, sg * hw), P((a + b) / 2, sg * (hw + w / 3.5)), P(f_s, sg * hw)], "ouv"))
    elif op == "double" and o.ouvre:
        sg = 1 if o.ouvre == "gauche" else -1
        pr += battant(a, c, sg, w / 2)
        pr += battant(b, c, sg, w / 2)
    elif op == "battante" and o.charniere and o.ouvre:
        sg = 1 if o.ouvre == "gauche" else -1
        h_s, f_s = (a, b) if o.charniere == "debut" else (b, a)
        pr += battant(h_s, f_s, sg, w)
    else:
        # sens manquant ou opération inconnue : baie seule (signalée dans les vérifications)
        pr.append(P_pl([P(a, -hw), P(b, -hw)], "ouv-tir"))
        pr.append(P_pl([P(a, hw), P(b, hw)], "ouv-tir"))
    return pr


# ---------------------------------------------------------------------------
# Symboles d'éléments fixes (repère local : longueur sur x, largeur sur y, dos vers −y)
# ---------------------------------------------------------------------------
DIM_DEFAUT = {"toilette": (20, 28), "lavabo": (20, 18), "baignoire": (60, 30), "evier": (30, 21),
              "cuisiniere": (30, 26), "refrigerateur": (30, 30), "laveuse": (27, 27), "secheuse": (27, 27),
              "chauffe-eau": (22, 22), "fournaise": (24, 30), "reservoir-huile": (60, 27), "cheminee": (24, 24),
              "foyer": (48, 24), "comptoir": (48, 25), "armoires": (36, 24), "panneau-electrique": (16, 4),
              "bac-lavage": (24, 20), "robinet-exterieur": (4, 4), "drain": (6, 6), "event": (8, 8),
              "trappe": (22, 30), "perron": (60, 48), "marches-ext": (48, 33), "escalier": (120, 36),
              "autre": (24, 24)}
# libellés proposés (du plus long au plus court) ; [] = symbole sans libellé
LIBELLES = {"toilette": [], "lavabo": [], "baignoire": [], "evier": [], "cuisiniere": [], "comptoir": [],
            "armoires": [], "laveuse": ["L"], "secheuse": ["S"], "refrigerateur": ["RÉF."],
            "chauffe-eau": ["C.E."], "panneau-electrique": ["PANNEAU ÉLECT.", "P.É."], "bac-lavage": ["BAC"],
            "robinet-exterieur": ["R.E."], "drain": ["DRAIN", "D"], "event": ["ÉVENT"], "trappe": ["TRAPPE"],
            "fournaise": ["FOURNAISE", "FOURN."], "reservoir-huile": ["RÉSERVOIR À L'HUILE", "RÉS. HUILE"],
            "cheminee": ["CHEMINÉE"], "foyer": ["FOYER"]}
SANS_INTERIEUR = {"cheminee", "armoires", "marches-ext", "panneau-electrique", "trappe"}


def ellipse(cx, cy, rx, ry, n=36):
    return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]


def rect_arrondi(x0, y0, x1, y1, r):
    r = max(0.01, min(r, (x1 - x0) / 2 - 0.01, (y1 - y0) / 2 - 0.01))
    g = sbox(x0 + r, y0 + r, x1 - r, y1 - r).buffer(r, quad_segs=4)
    return list(g.exterior.coords)[:-1]


def hachures(poly, pas, ang=45.0):
    minx, miny, maxx, maxy = poly.bounds
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    R = math.hypot(maxx - minx, maxy - miny)
    d = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
    nrm = (-d[1], d[0])
    out = []
    k = -int(R / pas) - 1
    while k * pas <= R:
        o = k * pas
        p0 = (cx + nrm[0] * o - d[0] * R, cy + nrm[1] * o - d[1] * R)
        p1 = (cx + nrm[0] * o + d[0] * R, cy + nrm[1] * o + d[1] * R)
        inter = poly.intersection(LineString([p0, p1]))
        out += lignes_de(inter)
        k += 1
    return out


def symbole(typ, L, W, mm):
    """Primitives locales et contour (Polygon) d'un élément fixe."""
    x0, x1, y0, y1 = -L / 2, L / 2, -W / 2, W / 2
    R = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    contour = Polygon(R)
    pr = []
    if typ == "toilette":
        td = min(9.0, 0.32 * W)
        pr.append(P_pl([(x0, y0), (x1, y0), (x1, y0 + td), (x0, y0 + td)], "elem", True))
        cy = (y0 + td + y1) / 2
        el = ellipse(0, cy, 0.4 * L, (y1 - y0 - td) / 2)
        pr.append(P_pl(el, "elem", True))
        contour = unary_union([sbox(x0, y0, x1, y0 + td), Polygon(el)])
    elif typ == "lavabo":
        pr.append(P_pl(R, "elem", True))
        pr.append(P_pl(ellipse(0, 0.08 * W, 0.36 * L, 0.32 * W), "elem-fin", True))
    elif typ == "baignoire":
        pr.append(P_pl(R, "elem", True))
        pr.append(P_pl(rect_arrondi(x0 + 3, y0 + 3, x1 - 3, y1 - 2.5, 5), "elem-fin", True))
        pr.append(P_cercle((x0 + 7, (y0 + y1) / 2 + 0.25), 1.0, "elem-fin"))
    elif typ in ("evier", "bac-lavage"):
        pr.append(P_pl(R, "elem", True))
        if typ == "evier" and L >= 30:
            bw = (L - 7) / 2
            pr.append(P_pl(rect_arrondi(x0 + 2.5, y0 + 2.5, x0 + 2.5 + bw, y1 - 2.5, 2), "elem-fin", True))
            pr.append(P_pl(rect_arrondi(x1 - 2.5 - bw, y0 + 2.5, x1 - 2.5, y1 - 2.5, 2), "elem-fin", True))
        else:
            pr.append(P_pl(rect_arrondi(x0 + 2.5, y0 + 2.5, x1 - 2.5, y1 - 2.5, 2), "elem-fin", True))
    elif typ == "cuisiniere":
        pr.append(P_pl(R, "elem", True))
        r = min(L, W) * 0.15
        for sx in (-1, 1):
            for sy in (-1, 1):
                pr.append(P_cercle((sx * L / 4, sy * W / 4.5 + 1), r * (1.0 if sx < 0 else 0.8), "elem-fin"))
    elif typ == "refrigerateur":
        pr.append(P_pl(R, "elem", True))
        pr.append(P_pl([(x0, y1 - 2), (x1, y1 - 2)], "elem-fin"))
    elif typ == "laveuse":
        pr.append(P_pl(R, "elem", True))
        pr.append(P_cercle((0, 1), 0.36 * min(L, W), "elem-fin"))
    elif typ == "secheuse":
        pr.append(P_pl(R, "elem", True))
        pr.append(P_pl([(x0, y0 + 4), (x1, y0 + 4)], "elem-fin"))
    elif typ == "chauffe-eau":
        r = min(L, W) / 2
        pr.append(P_cercle((0, 0), r, "elem"))
        contour = Point(0, 0).buffer(r, 16)
    elif typ == "reservoir-huile":
        pts = rect_arrondi(x0, y0, x1, y1, W / 2)
        pr.append(P_pl(pts, "elem", True))
        contour = Polygon(pts)
    elif typ == "cheminee":
        pr.append(P_pl(R, "elem", True))
        for ln in hachures(contour, mm(1.4)):
            pr.append(P_pl(ln, "elem-fin"))
    elif typ == "foyer":
        pr.append(P_pl(R, "elem", True))
        pr.append(P_pl([(x0 + L * 0.2, y0), (x0 + L * 0.3, y0 + W * 0.6), (x1 - L * 0.3, y0 + W * 0.6), (x1 - L * 0.2, y0)], "elem-fin"))
    elif typ == "armoires":
        pr.append(P_pl(R, "elem", True))
        pr.append(P_pl([(x0, y0), (x1, y1)], "elem-fin"))
        pr.append(P_pl([(x0, y1), (x1, y0)], "elem-fin"))
    elif typ == "panneau-electrique":
        pr.append(P_poly([R], "elem-plein"))
    elif typ == "robinet-exterieur":
        r = max(L, W) / 2
        pr.append(P_cercle((0, 0), r, "elem"))
        contour = Point(0, 0).buffer(r, 12)
    elif typ == "drain":
        r = max(L, W) / 2
        pr.append(P_cercle((0, 0), r, "elem"))
        pr.append(P_pl([(-r * 0.7, -r * 0.7), (r * 0.7, r * 0.7)], "elem-fin"))
        pr.append(P_pl([(-r * 0.7, r * 0.7), (r * 0.7, -r * 0.7)], "elem-fin"))
        contour = Point(0, 0).buffer(r, 12)
    elif typ == "event":
        pr.append(P_pl(R, "elem", True))
        pr.append(P_pl([(x0, y0), (x1, y1)], "elem-fin"))
        pr.append(P_pl([(x0, y1), (x1, y0)], "elem-fin"))
    elif typ == "trappe":
        pr.append(P_pl(R, "elem-tir", True))
    elif typ == "marches-ext":
        pr.append(P_pl(R, "elem", True))
    else:   # fournaise, comptoir, perron, autre…
        pr.append(P_pl(R, "elem", True))
        if typ == "fournaise":
            pr.append(P_pl([(x0 + 2, y0 + 2), (x1 - 2, y0 + 2), (x1 - 2, y1 - 2), (x0 + 2, y1 - 2)], "elem-fin", True))
    return pr, contour


# ---------------------------------------------------------------------------
# Chaînes de cotes automatiques (si niveau.lignes_cote est absent)
# ---------------------------------------------------------------------------
def chaines_auto(niv_id, murs):
    ext = [m for m in murs if m.lourd]
    if not ext:
        return []
    U = unary_union([m.emprise() for m in ext])
    F = unary_union([Polygon(p.exterior) for p in polys_de(U)])
    minx, miny, maxx, maxy = F.bounds
    res = []
    n = 0
    for facade, axe, sg in (("avant", 0, -1), ("arriere", 0, 1), ("gauche", 1, -1), ("droite", 1, 1)):
        lo, hi = (minx, maxx) if axe == 0 else (miny, maxy)

        def face(c):
            c = min(max(c, lo + 0.05), hi - 0.05)
            ln = LineString([(c, miny - 10), (c, maxy + 10)]) if axe == 0 else LineString([(minx - 10, c), (maxx + 10, c)])
            b = F.intersection(ln).bounds
            if not b or any(math.isnan(v) for v in b):
                return None
            v0, v1 = (b[1], b[3]) if axe == 0 else (b[0], b[2])
            return v0 if sg < 0 else v1

        # sommets du profil de la façade
        som = {lo, hi}
        for p in polys_de(F):
            for x, y in p.exterior.coords:
                c = x if axe == 0 else y
                if lo + 0.5 < c < hi - 0.5:
                    f1, f2 = face(c - 0.1), face(c + 0.1)
                    if f1 is not None and f2 is not None and abs(f1 - f2) > 0.5:
                        som.add(c)
        # murs de façade
        fac = []
        for m in ext:
            parall = abs(m.u[1]) < 0.01 if axe == 0 else abs(m.u[0]) < 0.01
            if not parall:
                continue
            mid = m.pt(m.L / 2)
            cm, nm = (mid[0], mid[1]) if axe == 0 else (mid[1], mid[0])
            fc = face(cm)
            if fc is not None and abs(nm + sg * m.t / 2 - fc) <= 1.0:
                fac.append(m)
        cloisons, ouvs = set(), set()
        for m in murs:
            if m in fac or (m.lourd and m.emprise().intersection(F.exterior).length > 0.5 * m.L):
                continue
            perp = abs(m.u[0]) < 0.01 if axe == 0 else abs(m.u[1]) < 0.01
            if perp:
                for E in (m.p1, m.p2):
                    if any(f.emprise().distance(Point(E)) <= 1.0 for f in fac):
                        cloisons.add(E[0] if axe == 0 else E[1])
        for f in fac:
            for o in f.ouvs:
                if o.valide:
                    c = f.pt(o.pos)
                    ouvs.add(c[0] if axe == 0 else c[1])

        def uniq(vals):
            out = []
            for v in sorted(vals):
                if lo - 0.01 <= v <= hi + 0.01 and (not out or v - out[-1] > 0.25):
                    out.append(v)
            return out

        def pt(c):
            fc = face(c)
            return [round(c, 4), round(fc, 4)] if axe == 0 else [round(fc, 4), round(c, 4)]

        chaines = {3: [lo, hi], 2: uniq(som | cloisons), 1: uniq(som | ouvs) if ouvs else None}
        if len(chaines[2]) <= 2:
            chaines[2] = None
        for rang in (1, 2, 3):
            ch = chaines[rang]
            if not ch:
                continue
            for c1, c2 in zip(ch[:-1], ch[1:]):
                n += 1
                res.append({"id": f"lc-{niv_id}-A{n:03d}", "p1": pt(c1), "p2": pt(c2),
                            "direction": "x" if axe == 0 else "y", "facade": facade, "rang": rang,
                            "source": "DÉDUIT", "statut": "confirmee", "ref": None,
                            "valeur_attendue": None, "repere": None, "auto": True})
    return res


# ---------------------------------------------------------------------------
# Construction d'une feuille
# ---------------------------------------------------------------------------
FACADES = {"avant": (1, -1), "arriere": (1, 1), "gauche": (0, -1), "droite": (0, 1)}  # (axe normal, signe)


class Feuille:
    pass


def charger_niveau(niv, verif):
    nid = str(niv.get("id") or "?")
    murs, par_id = [], {}
    for d in niv.get("murs") or []:
        try:
            m = Mur(d)
            if m.L < 0.01:
                raise ValueError("longueur nulle")
        except Exception as e:
            verif.add("Murs", "ERREUR", f"[{nid}] {d.get('id')} : géométrie invalide ({e}) — ignoré")
            continue
        murs.append(m)
        par_id[m.id] = m
        if m.t_defaut:
            verif.add("Murs", "AVERT", f"[{nid}] {m.id} : épaisseur absente → {pipo(m.t)} présumé (repère ⚠)")
    prolongements(murs)
    ouvs = []
    for d in niv.get("ouvertures") or []:
        oid = d.get("id")
        m = par_id.get(d.get("mur_id"))
        if m is None:
            verif.add("Ouvertures", "ERREUR", f"[{nid}] {oid} : mur_id « {d.get('mur_id')} » inexistant")
            continue
        o = Ouv(d, m)
        if not o.valide:
            verif.add("Ouvertures", "ERREUR", f"[{nid}] {oid} : position ou largeur manquante — non dessinée")
            continue
        if o.a < -0.01 or o.b > m.L + 0.01:
            verif.add("Ouvertures", "ERREUR",
                      f"[{nid}] {oid} : hors du mur {m.id} (de {f3(o.a)} à {f3(o.b)} po ; mur de {f3(m.L)} po)")
        bs = o.besoin_sens()
        if bs:
            manque = [k for k in bs if (o.charniere if k == "charniere" else o.ouvre) is None]
            if manque:
                verif.add("Ouvertures", "ERREUR",
                          f"[{nid}] {oid} : porte {o.op} sans sens ({', '.join(manque)}) — dessinée comme baie")
        m.ouvs.append(o)
        ouvs.append(o)
    # chevauchement d'ouvertures sur un même mur
    for m in murs:
        lst = sorted(m.ouvs, key=lambda o: o.a)
        for o1, o2 in zip(lst[:-1], lst[1:]):
            if o2.a < o1.b - 0.01:
                verif.add("Ouvertures", "AVERT", f"[{nid}] {o1.id} et {o2.id} se chevauchent sur {m.id}")
    return murs, ouvs


def charger_pieces(niv, verif):
    nid = str(niv.get("id") or "?")
    pieces = []
    for d in niv.get("pieces") or []:
        pid = d.get("id")
        pts = d.get("polygone") or []
        try:
            pts = [(float(p[0]), float(p[1])) for p in pts]
        except Exception:
            verif.add("Pièces", "ERREUR", f"[{nid}] {pid} : polygone illisible")
            continue
        if len(pts) >= 2 and math.hypot(pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1]) < 1e-6:
            pts = pts[:-1]
        if len(pts) < 3:
            verif.add("Pièces", "ERREUR", f"[{nid}] {pid} : polygone non fermé (moins de 3 sommets)")
            continue
        poly = Polygon(pts)
        if not poly.is_valid:
            from shapely.validation import explain_validity
            verif.add("Pièces", "ERREUR", f"[{nid}] {pid} : polygone invalide ({explain_validity(poly)})")
            poly = poly.buffer(0)
            if poly.is_empty:
                continue
        elif not Polygon(pts).exterior.is_ccw:
            verif.add("Pièces", "AVERT", f"[{nid}] {pid} : polygone en sens horaire (antihoraire attendu)")
        pieces.append((d, poly))
    for i in range(len(pieces)):
        for j in range(i + 1, len(pieces)):
            a = pieces[i][1].intersection(pieces[j][1]).area
            if a > 1.0:
                verif.add("Pièces", "ERREUR", f"[{nid}] {pieces[i][0].get('id')} et {pieces[j][0].get('id')} "
                                              f"se chevauchent ({fr(a / 144, 2)} pi²)")
    return pieces


def geom_structure(s):
    g = s.get("geometrie") or {}
    typ = str(s.get("type") or "").lower()

    def n_(k):
        return num(g.get(k))

    x1, y1, x2, y2 = n_("x1"), n_("y1"), n_("x2"), n_("y2")
    x, y = n_("x"), n_("y")
    if typ == "colonne":
        if x is None or y is None:
            return None
        w = n_("largeur") or 4.0
        p = n_("profondeur") or w
        return sbox(x - w / 2, y - p / 2, x + w / 2, y + p / 2)
    if isinstance(g.get("polygone"), list) and len(g["polygone"]) >= 3:
        try:
            return Polygon([(float(a), float(b)) for a, b in g["polygone"]])
        except Exception:
            return None
    if typ == "semelle":
        if x is not None and y is not None:
            w = n_("largeur") or 24.0
            p = n_("profondeur") or w
            return sbox(x - w / 2, y - p / 2, x + w / 2, y + p / 2)
        if None not in (x1, y1, x2, y2):
            if abs(x2 - x1) > 1 and abs(y2 - y1) > 1 and n_("largeur") is None:
                return sbox(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
            return LineString([(x1, y1), (x2, y2)]).buffer((n_("largeur") or 20.0) / 2, cap_style="flat")
        return None
    if typ == "solives":
        if None in (x1, y1, x2, y2):
            return None
        return sbox(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
    if None in (x1, y1, x2, y2):
        return None
    return LineString([(x1, y1), (x2, y2)])


def texte_dim_structure(s):
    d = s.get("dimension") or {}
    v = d.get("valeur") if isinstance(d, dict) else None
    if v is None or v == "":
        v = d.get("texte_original") if isinstance(d, dict) else None
    if v is None:
        return ""
    t = str(v)
    if isinstance(d, dict) and norm_src(d.get("source")) == "ESTIMÉ":
        t = "≈" + t
    return t


def construire(niv, idx, projet, ctx, verif):
    """Construit la feuille d'un niveau : retourne un objet Feuille (dessin + données)."""
    F = Feuille()
    nid = str(niv.get("id") or f"N{idx}")
    F.nid = nid
    F.nom = str(niv.get("nom") or nid)
    F.feuille = str(niv.get("feuille") or f"A-{100 + idx}")
    F.slug = str(niv.get("slug") or {"SS": "sous-sol", "RDC": "rdc"}.get(nid, slugify(F.nom)))
    murs, ouvs = charger_niveau(niv, verif)
    pieces = charger_pieces(niv, verif)
    F.murs, F.ouvs, F.pieces = murs, ouvs, pieces

    # --- polygones de murs (rectangle − baies)
    for m in murs:
        emp = m.emprise()
        trous = [m.rect(o.a, o.b, -m.t / 2 - 0.05, m.t / 2 + 0.05) for o in m.ouvs if o.valide]
        m.poly = emp.difference(unary_union(trous)) if trous else emp
    lourd = unary_union([m.poly for m in murs if m.lourd]) if any(m.lourd for m in murs) else Polygon()
    leger_u = unary_union([m.poly for m in murs if not m.lourd]) if any(not m.lourd for m in murs) else Polygon()
    leger = leger_u.difference(lourd) if not lourd.is_empty else leger_u

    # --- éléments (géométrie)
    elems = []
    for e in niv.get("elements") or []:
        pos = e.get("position") or {}
        x, y = num(pos.get("x")), num(pos.get("y"))
        typ = str(e.get("type") or "autre").lower()
        if x is None or y is None:
            verif.add("Mise en page", "AVERT", f"[{nid}] {e.get('id')} : élément sans position — non dessiné")
            continue
        dims = e.get("dimensions") or {}
        L, W = num(dims.get("longueur")), num(dims.get("largeur"))
        dL, dW = DIM_DEFAUT.get(typ, DIM_DEFAUT["autre"])
        if L is None or L <= 0 or W is None or W <= 0:
            verif.add("Mise en page", "INFO", f"[{nid}] {e.get('id')} : dimensions absentes → symbole par défaut "
                                              f"{pipo(dL)} × {pipo(dW)}")
            L = L if (L and L > 0) else dL
            W = W if (W and W > 0) else dW
        elems.append({"d": e, "id": str(e.get("id")), "typ": typ, "x": x, "y": y,
                      "rot": num(pos.get("rotation_deg")) or 0.0, "L": L, "W": W})
    # --- structure (géométrie)
    strs = []
    for s in niv.get("structure") or []:
        g = geom_structure(s)
        if g is None or g.is_empty:
            verif.add("Mise en page", "AVERT", f"[{nid}] {s.get('id')} : géométrie de structure incomplète — non dessinée")
            continue
        strs.append((s, g))

    # --- lignes de cote
    lcs = niv.get("lignes_cote")
    if lcs is None:
        lcs = chaines_auto(nid, murs)
        verif.add("Chaînes de cotes", "INFO", f"[{nid}] lignes_cote absent → {len(lcs)} cotes générées "
                                              f"automatiquement (source DÉDUIT)")
    lcs = [l for l in lcs if isinstance(l, dict)]

    # --- emprise géométrique (po réels)
    geoms = [m.emprise() for m in murs] + [p for _, p in pieces] + [g for _, g in strs]
    for el in elems:
        geoms.append(rect_element(el))
    for ec in ctx["ecarts"]:
        if str(ec.get("niveau")) == nid and isinstance(ec.get("position"), list) and len(ec["position"]) >= 2:
            geoms.append(Point(float(ec["position"][0]), float(ec["position"][1])).buffer(1))
    if not geoms:
        geoms = [sbox(0, 0, 120, 120)]
    G = unary_union(geoms).bounds   # minx, miny, maxx, maxy

    # --- choix de l'échelle
    rmax = {f: 0 for f in FACADES}
    for l in lcs:
        f = l.get("facade")
        if f in rmax:
            rmax[f] = max(rmax[f], int(num(l.get("rang")) or 1))
    f_c = H_COTE / CAP          # taille de police des cotes (mm)

    def ext_mm(f):
        r = rmax[f]
        if not r:
            base = 0.0
        else:
            base = C_D1 + (r - 1) * C_ESP
        if f in ("arriere", "gauche"):
            return base + (C_GAP + f_c * 1.0 + 2.0 if r else 0)
        if f == "avant":
            return base + (C_DEP if r else 3.0) + 3.0 + (H_FACADE / CAP) * 1.0
        return base + (C_DEP if r else 0)

    ext = {f: ext_mm(f) for f in FACADES}
    zw, zh = ZONE[2] - ZONE[0], ZONE[3] - ZONE[1]
    choix = None
    for k, lib, grad in ECHELLES:
        w = (G[2] - G[0]) / k + (ext["gauche"] + ext["droite"]) / 25.4
        h = (G[3] - G[1]) / k + (ext["avant"] + ext["arriere"]) / 25.4
        if w <= zw and h <= zh:
            choix = (k, lib, grad)
            break
    if choix is None:
        choix = ECHELLES[-1]
        verif.add("Mise en page", "AVERT", f"[{nid}] le plan dépasse la zone de dessin même au 1/8\" = 1'-0\"")
    k, lib, grad = choix
    F.k, F.echelle, F.grad = k, lib, grad
    verif.add("Mise en page", "INFO", f"[{nid}] feuille {F.feuille} : échelle {lib}")

    def mm(v):
        return v / 25.4 * k

    F.mm = mm
    # origine : centrer (plan + annotations) dans la zone de dessin
    ext_r = {f: mm(v) for f, v in ext.items()}
    zcx, zcy = (ZONE[0] + ZONE[2]) / 2 * k, (ZONE[1] + ZONE[3]) / 2 * k
    F.X0 = zcx - ((G[0] - ext_r["gauche"]) + (G[2] + ext_r["droite"])) / 2
    F.Y0 = zcy + ((G[3] + ext_r["arriere"]) + (G[1] - ext_r["avant"])) / 2

    D = Dessin()
    PL = Placeur()
    F.dessin, F.placeur = D, PL
    fc = mm(f_c)                 # police cotes / libellés (po réels)
    fn = mm(H_NOM / CAP)         # police noms de pièces

    # =============================== 10-Murs ===============================
    for m in sorted(murs, key=lambda m: m.lourd):
        g = D.g("10-Murs", m.id)
        g += poly_prims(m.poly, "mur-lourd" if m.lourd else "mur-leger")
        PL.ligne(m.poly, m.id)
    if not leger.is_empty:
        lg = leger.boundary
        if not lourd.is_empty:
            lg = lg.difference(lourd.buffer(0.02))
        D.g("10-Murs", "contour-murs-legers").extend(P_pl(c, "mur-leger-c") for c in lignes_de(lg))
    if not lourd.is_empty:
        D.g("10-Murs", "contour-murs-lourds").extend(P_pl(c, "mur-lourd-c") for c in lignes_de(lourd.boundary))

    # =============================== 20-Ouvertures ===============================
    for o in ouvs:
        pr = dessin_ouverture(o, mm)
        D.g("20-Ouvertures", o.id).extend(pr)
        PL.prims(pr, o.id)

    # =============================== 30-Escaliers-Elements ===============================
    grp_elem = {}
    lib_elems = []
    for el in elems:
        g = D.g("30-Escaliers-Elements", el["id"])
        grp_elem[el["id"]] = g
        if el["typ"] == "escalier" or (el["typ"] == "marches-ext" and isinstance(el["d"].get("escalier"), dict)):
            dessiner_escalier(el, g, PL, mm, fc, verif, nid)
            continue
        pr, cont = symbole(el["typ"], el["L"], el["W"], mm)

        def tf(p, el=el):
            q = rot2(p, el["rot"])
            return (q[0] + el["x"], q[1] + el["y"])

        prs = [transformer(p, tf, el["rot"]) for p in pr]
        cont = affinity.translate(affinity.rotate(cont, el["rot"], origin=(0, 0)), el["x"], el["y"])
        g += prs
        PL.prims(prs, el["id"])
        PL.zone(cont, el["id"])
        libs = LIBELLES.get(el["typ"])
        if libs is None:
            nom = str(el["d"].get("nom") or el["typ"]).upper()
            libs = [nom]
        if libs:
            lib_elems.append((el, cont, libs, g))

    # =============================== 40-Structure ===============================
    lib_str = []
    elem_zones = [rect_element(el) for el in elems]
    for s, geo in strs:
        sid = str(s.get("id"))
        typ = str(s.get("type") or "").lower()
        g = D.g("40-Structure", sid)
        dt = texte_dim_structure(s)
        if typ in ("poutre", "axe", "linteau") and isinstance(geo, LineString):
            st = {"poutre": "str-poutre", "axe": "str-axe", "linteau": "str-tir"}[typ]
            pr = [P_pl(list(geo.coords), st)]
            g += pr
            PL.prims(pr, sid)
            if typ == "poutre":
                lib = ("POUTRE " + dt).strip()
            elif typ == "axe":
                lib = "AXE PORTEUR D'ORIGINE"
            else:
                lib = ("LINTEAU " + dt).strip()
            lib_str.append(("ligne", sid, geo, lib, g))
        elif typ == "colonne":
            c = list(geo.exterior.coords)[:-1]
            pr = [P_pl(c, "str", True), P_pl([c[0], c[2]], "str-fin"), P_pl([c[1], c[3]], "str-fin")]
            g += pr
            PL.prims(pr, sid)
            PL.zone(geo, sid)
            if dt:
                lib_str.append(("autour", sid, geo, "COL. " + dt, g))
        elif typ == "semelle":
            for p in polys_de(geo):
                pr = [P_pl(list(p.exterior.coords)[:-1], "str-tir", True)]
                g += pr
                PL.prims(pr, sid)
        elif typ == "solives":
            fl = fleche_solives(s, geo, murs, elem_zones, mm)
            if fl is None:
                continue
            pr, seg = fl
            g += pr
            PL.prims(pr, sid)
            esp = None
            gg = s.get("geometrie") or {}
            for cand in (gg.get("espacement"), s.get("espacement"), (s.get("dimension") or {}).get("espacement")):
                if num(cand) is not None:
                    esp = num(cand)
                    break
            lib = ("SOLIVES " + dt).strip()
            if esp:
                lib += f" @ {f3(esp)}\" c/c"
            lib_str.append(("ligne", sid, seg, lib, g))
        else:
            for p in polys_de(geo) or []:
                pr = [P_pl(list(p.exterior.coords)[:-1], "str-tir", True)]
                g += pr
                PL.prims(pr, sid)
            if isinstance(geo, LineString):
                pr = [P_pl(list(geo.coords), "str-tir")]
                g += pr
                PL.prims(pr, sid)

    # =============================== 50-Cotes (traits) ===============================
    Gb = G
    cotes = preparer_cotes(lcs, Gb, mm, verif, nid)
    emp_m = unary_union([m.emprise() for m in murs]) if murs else Polygon()
    masque = unary_union([z.buffer(mm(0.8), join_style=2) for z in elem_zones if not z.within(emp_m.envelope)]) \
        if elem_zones else None
    dessiner_traits_cotes(cotes, D, PL, mm, masque)

    # =============================== Libellé de façade (fixe) ===============================
    y_bas = min([c["ligne"] for c in cotes if c["facade"] == "avant"] + [G[1]])
    tf_ = mm(H_FACADE / CAP)
    yb = y_bas - mm(C_DEP + 3.0) - 0.8 * tf_ if any(c["facade"] == "avant" for c in cotes) else G[1] - mm(6) - 0.8 * tf_
    murs_b = unary_union([m.emprise() for m in murs]).bounds if murs else G
    xf = (murs_b[0] + murs_b[2]) / 2
    txt = "FAÇADE AVANT (RUE)"
    gfa = D.g("60-Etiquettes", "facade-avant")
    gfa.append(P_txt(xf, yb, txt, tf_, "middle", 0, True))
    PL.texte(boite(xf, yb, MET.l(txt, tf_, True), tf_, "middle", 0, 0, txt), "facade-avant", "libellé de façade")

    # =============================== Textes des cotes ===============================
    reperes_cotes = placer_textes_cotes(cotes, D, PL, mm, fc, ctx, nid, verif)

    # =============================== Libellés d'éléments ===============================
    for el, cont, libs, g in lib_elems:
        placer_libelle_element(el, cont, libs, g, PL, mm, fc)

    # =============================== Libellés de structure ===============================
    for kind, sid, geo, lib, g in lib_str:
        if kind == "ligne":
            placer_long_ligne(geo, lib, sid, g, PL, mm, fc)
        else:
            placer_autour(geo, [(lib, fc, False)], sid, g, PL, mm, interieur=False)

    # =============================== Étiquettes de pièces ===============================
    for d, poly in pieces:
        placer_etiquette_piece(d, poly, D, PL, mm, fn, fc)

    # =============================== 70-Incertitudes ===============================
    F.reperes = []
    for ec in ctx["ecarts"]:
        if str(ec.get("niveau")) != nid:
            continue
        pos = ec.get("position")
        n = ctx["num_ecart"].get(str(ec.get("id")))
        F.reperes.append((n, str(ec.get("id")), str(ec.get("description") or "")))
        if isinstance(pos, list) and len(pos) >= 2 and num(pos[0]) is not None and num(pos[1]) is not None:
            P0 = Point(float(pos[0]), float(pos[1]))
            g = D.g("70-Incertitudes", str(ec.get("id")))
            g.append(P_cercle((P0.x, P0.y), mm(0.6), "inc"))
            placer_marqueur(n, P0.buffer(mm(0.6)), str(ec.get("id")), g, PL, mm, point=(P0.x, P0.y))
    np_ = ctx["num_presume"].get(nid)
    for m in murs:
        if m.t_src == "PRÉSUMÉ" and np_ is not None:
            mid = m.pt(m.L / 2)
            g = D.g("70-Incertitudes", "rep-" + m.id)
            placer_marqueur(np_, Point(mid).buffer(m.t / 2 + mm(0.3)), "rep-" + m.id, g, PL, mm, point=mid)
    if np_ is not None and any(m.t_src == "PRÉSUMÉ" for m in murs):
        F.reperes.append((np_, "", "Épaisseur de mur présumée (non cotée)"))
    for n, lid, desc in reperes_cotes:
        if not any(r[0] == n for r in F.reperes):
            F.reperes.append((n, lid, desc))
    F.reperes.sort(key=lambda r: r[0])

    # =============================== 00-Cartouche ===============================
    cartouche(F, niv, projet, ctx)

    # =============================== chevauchements restants ===============================
    verifier_textes(F, verif)
    F.cotes = cotes
    F.lcs = lcs
    return F


# ---------------------------------------------------------------------------
# Escaliers
# ---------------------------------------------------------------------------
def rect_element(el):
    """Rectangle (Polygon) occupé par un élément, en coordonnées maison."""
    es = el["d"].get("escalier") if isinstance(el["d"].get("escalier"), dict) else {}
    dv = {"+x": (1, 0), "-x": (-1, 0), "+y": (0, 1), "-y": (0, -1)}.get(str(es.get("direction")))
    L, W = el["L"], el["W"]
    if el["typ"] == "escalier" and dv is not None:
        rot = 0.0 if abs(dv[0]) > 0.5 else 90.0
    elif el["typ"] == "marches-ext" and dv is not None:
        rot = 0.0
    else:
        rot = el["rot"]
    r = affinity.rotate(sbox(-L / 2, -W / 2, L / 2, W / 2), rot, origin=(0, 0))
    return affinity.translate(r, el["x"], el["y"])


def dessiner_escalier(el, g, PL, mm, fc, verif, nid):
    e = el["d"]
    es = e.get("escalier") if isinstance(e.get("escalier"), dict) else {}
    dv = {"+x": (1, 0), "-x": (-1, 0), "+y": (0, 1), "-y": (0, -1)}.get(str(es.get("direction")))
    if dv is None:
        dv = rot2((0, 1), el["rot"])
    pv = (-dv[1], dv[0])
    if el["typ"] == "marches-ext":
        run, wid = el["W"], el["L"]
        if abs(dv[0]) > 0.5:
            run, wid = el["L"], el["W"]
    else:
        run, wid = el["L"], el["W"]
    c = (el["x"], el["y"])

    def P(s, t):
        return (c[0] + dv[0] * s + pv[0] * t, c[1] + dv[1] * s + pv[1] * t)

    R = [P(-run / 2, -wid / 2), P(run / 2, -wid / 2), P(run / 2, wid / 2), P(-run / 2, wid / 2)]
    pr = [P_pl(R, "elem", True)]
    n = num(es.get("nb_contremarches"))
    n = int(round(n)) if n and n >= 2 else None
    if n:
        pas = run / n
        nb = n - 1
    else:
        pas = 10.0
        nb = int(run / pas - 1e-6)
    for i in range(1, nb + 1):
        s = -run / 2 + i * pas
        pr.append(P_pl([P(s, -wid / 2), P(s, wid / 2)], "elem-fin"))
    texte_fl = str(es.get("fleche") or "").upper()
    if el["typ"] == "escalier" or texte_fl:
        S = P(-run / 2 + min(mm(2), run * 0.1), 0)
        E = P(run / 2 - min(mm(1), run * 0.05), 0)
        pr.append(P_pl([S, E], "elem"))
        pr.append(P_cercle(S, mm(0.7), "elem"))
        ah, aw = mm(2.4), mm(0.9)
        B = (E[0] - dv[0] * ah, E[1] - dv[1] * ah)
        pr.append(P_poly([[E, (B[0] + pv[0] * aw, B[1] + pv[1] * aw), (B[0] - pv[0] * aw, B[1] - pv[1] * aw)]], "elem-plein"))
    g += pr
    PL.prims(pr, el["id"])
    PL.zone(Polygon(R), el["id"])
    if el["typ"] != "escalier":
        return
    rot = 0.0 if abs(dv[0]) > 0.5 else 90.0
    up = rot2((0, 1), rot)
    textes = []
    if texte_fl in ("MONTE", "DESCEND"):
        textes.append(texte_fl)
    elif texte_fl:
        textes.append(texte_fl)
    textes.append(f"{n} CM" if n else "≈ GIRON 10\"")
    for i, t in enumerate(textes[:2]):
        larg = MET.l(t, fc, False)
        off = (mm(0.9) + 0.21 * fc) if i == 0 else -(mm(0.9) + 0.76 * fc)
        x, y = c[0] + up[0] * off, c[1] + up[1] * off
        b = boite(x, y, larg, fc, "middle", rot, 0, t)
        mb = boite(x, y, larg, fc, "middle", rot, mm(0.4), t)
        g.append(P_poly([list(mb.exterior.coords)[:-1]], "masque"))
        g.append(P_txt(x, y, t, fc, "middle", rot))
        PL.texte(b, el["id"], f"escalier {el['id']} « {t} »")


def fleche_solives(s, zone, murs, elem_zones, mm):
    sens = str(s.get("sens") or "").lower()
    if sens not in ("x", "y"):
        sens = "y"
    minx, miny, maxx, maxy = zone.bounds
    obst = unary_union([m.emprise().buffer(mm(3)) for m in murs] + [z.buffer(mm(2)) for z in elem_zones]) \
        if (murs or elem_zones) else Polygon()
    best = None
    for i in range(15):
        fr_ = [0.5, 0.42, 0.58, 0.35, 0.65, 0.28, 0.72, 0.2, 0.8, 0.14, 0.86, 0.46, 0.54, 0.38, 0.62][i]
        if sens == "x":
            yy = miny + (maxy - miny) * fr_
            ln = LineString([(minx, yy), (maxx, yy)])
        else:
            xx = minx + (maxx - minx) * fr_
            ln = LineString([(xx, miny), (xx, maxy)])
        rest = ln.difference(obst) if not obst.is_empty else ln
        for part in lignes_de(rest):
            L = LineString(part)
            if best is None or L.length > best.length + 1e-6:
                best = L
    if best is None or best.length < mm(10):
        return None
    c = best.interpolate(0.5, normalized=True)
    half = min(best.length * 0.35, mm(30))
    if sens == "x":
        A, B = (c.x - half, c.y), (c.x + half, c.y)
    else:
        A, B = (c.x, c.y - half), (c.x, c.y + half)
    dv = ((B[0] - A[0]) / (2 * half), (B[1] - A[1]) / (2 * half))
    pv = (-dv[1], dv[0])
    ah, aw = mm(2.4), mm(0.9)
    pr = [P_pl([A, B], "str-fin")]
    for T, sg in ((B, 1), (A, -1)):
        Bb = (T[0] - sg * dv[0] * ah, T[1] - sg * dv[1] * ah)
        pr.append(P_poly([[T, (Bb[0] + pv[0] * aw, Bb[1] + pv[1] * aw), (Bb[0] - pv[0] * aw, Bb[1] - pv[1] * aw)]], "str-plein"))
    return pr, LineString([A, B])


# ---------------------------------------------------------------------------
# Cotes
# ---------------------------------------------------------------------------
def preparer_cotes(lcs, G, mm, verif, nid):
    cotes = []
    for l in lcs:
        lid = str(l.get("id"))
        try:
            p1 = (float(l["p1"][0]), float(l["p1"][1]))
            p2 = (float(l["p2"][0]), float(l["p2"][1]))
        except Exception:
            verif.add("Chaînes de cotes", "ERREUR", f"[{nid}] {lid} : p1/p2 illisibles — ignorée")
            continue
        d = str(l.get("direction") or ("x" if abs(p2[0] - p1[0]) >= abs(p2[1] - p1[1]) else "y")).lower()
        ax = 0 if d == "x" else 1
        facade = str(l.get("facade") or "int").lower()
        rang = int(num(l.get("rang")) or 1)
        longueur = abs(p2[ax] - p1[ax])
        if longueur < 0.01:
            verif.add("Chaînes de cotes", "AVERT", f"[{nid}] {lid} : longueur nulle — ignorée")
            continue
        c1, c2 = sorted((p1[ax], p2[ax]))
        if facade in FACADES:
            nax, sg = FACADES[facade]
            if nax == ax:
                verif.add("Chaînes de cotes", "ERREUR", f"[{nid}] {lid} : direction {d} incompatible avec la façade {facade}")
                continue
            face = (G[1] if sg < 0 else G[3]) if nax == 1 else (G[0] if sg < 0 else G[2])
            ligne = face + sg * mm(C_D1 + (max(1, min(rang, 3)) - 1) * C_ESP)
        else:
            facade = "int"
            dec = num(l.get("decalage")) or 0.0
            ligne = p1[1 - ax] + dec
            sg = 1 if dec >= 0 else -1
        cotes.append({"l": l, "id": lid, "p1": p1, "p2": p2, "ax": ax, "facade": facade, "rang": rang,
                      "c1": c1, "c2": c2, "ligne": ligne, "sg": sg, "longueur": longueur,
                      "source": norm_src(l.get("source")) or "", "statut": str(l.get("statut") or "")})
    return cotes


def pt_cote(c, along, normal):
    return (along, normal) if c["ax"] == 0 else (normal, along)


def dessiner_traits_cotes(cotes, D, PL, mm, masque=None):
    # lignes d'attache des façades, fusionnées par (façade, abscisse)
    attache = {}
    for c in cotes:
        c["grp"] = D.g("50-Cotes", c["id"])
        if c["facade"] == "int":
            continue
        for p in (c["p1"], c["p2"]):
            a = p[c["ax"]]
            n = p[1 - c["ax"]]
            key = (c["facade"], round(a, 2))
            s = c["sg"]
            rec = attache.get(key)
            if rec is None:
                attache[key] = {"own": c, "a": a, "start": n, "end": c["ligne"], "sg": s}
            else:
                if s * n < s * rec["start"]:
                    rec["start"] = n
                if s * c["ligne"] > s * rec["end"]:
                    rec["end"] = c["ligne"]
    for key in attache:
        r = attache[key]
        c = r["own"]
        s = r["sg"]
        n0 = r["start"] + s * mm(C_ECART)
        n1 = r["end"] + s * mm(C_DEP)
        if s * (n1 - n0) <= 0:
            continue
        ln = LineString([pt_cote(c, r["a"], n0), pt_cote(c, r["a"], n1)])
        if masque is not None and not masque.is_empty:
            ln = ln.difference(masque)
        for part in lignes_de(ln):
            pr = P_pl(part, "cote")
            c["grp"].append(pr)
            PL.prims([pr], c["id"])
    ticks = set()
    tk = mm(C_TICK) / 2 / math.sqrt(2)
    for c in cotes:
        A = pt_cote(c, c["c1"], c["ligne"])
        B = pt_cote(c, c["c2"], c["ligne"])
        pr = [P_pl([A, B], "cote")]
        if c["facade"] == "int":
            for p in (c["p1"], c["p2"]):
                n = p[1 - c["ax"]]
                if abs(n - c["ligne"]) > mm(C_ECART) * 1.5:
                    s = 1 if c["ligne"] > n else -1
                    pr.append(P_pl([pt_cote(c, p[c["ax"]], n + s * mm(C_ECART)),
                                    pt_cote(c, p[c["ax"]], c["ligne"] + s * mm(C_DEP))], "cote"))
        for T in (A, B):
            key = (c["facade"], c["rang"] if c["facade"] != "int" else c["id"], round(T[0], 2), round(T[1], 2))
            if key in ticks:
                continue
            ticks.add(key)
            pr.append(P_pl([(T[0] - tk, T[1] - tk), (T[0] + tk, T[1] + tk)], "cote-tick"))
        c["grp"].extend(pr)
        PL.prims(pr, c["id"])


def placer_textes_cotes(cotes, D, PL, mm, fc, ctx, nid, verif):
    reperes = []
    gap = mm(C_GAP)
    for c in cotes:
        prefix = "≈ " if c["source"] == "ESTIMÉ" else ""
        suffix = " ?" if c["source"] == "ILLISIBLE" or c["statut"] == "illisible" else ""
        c["texte"] = f"{prefix}{pipo(c['longueur'])} ({metres(c['longueur'])}){suffix}"
        c["rot"] = 0.0 if c["ax"] == 0 else 90.0
        c["up"] = (0.0, 1.0) if c["ax"] == 0 else (-1.0, 0.0)
        c["along"] = (1.0, 0.0) if c["ax"] == 0 else (0.0, 1.0)

    def cand(c, i):
        w = MET.l(c["texte"], fc)
        mid = (c["c1"] + c["c2"]) / 2
        lvl0 = gap + 0.21 * fc
        lvl1 = lvl0 + fc * 1.0 + mm(0.4)
        opts = [(mid, lvl0, "middle")]
        span = c["c2"] - c["c1"]
        if w + mm(2) < span:
            for fr_ in (0.35, 0.65, 0.25, 0.75):
                a = c["c1"] + span * fr_
                a = min(max(a, c["c1"] + w / 2 + mm(1)), c["c2"] - w / 2 - mm(1))
                opts.append((a, lvl0, "middle"))
        opts += [(c["c2"] + mm(1.5), lvl0, "start"), (c["c1"] - mm(1.5), lvl0, "end")]
        if not (c["facade"] in ("avant", "droite") and c["rang"] < 3):
            opts += [(mid, lvl1, "middle"), (c["c2"] + mm(1.5), lvl1, "start"), (c["c1"] - mm(1.5), lvl1, "end")]
        if i >= len(opts):
            return None
        a, off, anc = opts[i]
        base = pt_cote(c, a, c["ligne"])
        x, y = base[0] + c["up"][0] * off, base[1] + c["up"][1] * off
        return x, y, anc, boite(x, y, w, fc, anc, c["rot"], mm(0.25), c["texte"]), off > lvl0 + 1e-9, a

    places = {}
    for phase in (0, 1):
        for c in cotes:
            if c["id"] in places:
                continue
            idxs = [0] if phase == 0 else range(1, 12)
            for i in idxs:
                r = cand(c, i)
                if r is None:
                    break
                if PL.conflits(r[3], ignore=(c["id"],)) == 0:
                    places[c["id"]] = r
                    PL.texte(boite(r[0], r[1], MET.l(c["texte"], fc), fc, r[2], c["rot"], 0, c["texte"]),
                             c["id"], f"cote {c['id']}")
                    break
    for c in cotes:
        if c["id"] not in places:
            r = cand(c, 0)
            places[c["id"]] = r
            PL.texte(boite(r[0], r[1], MET.l(c["texte"], fc), fc, r[2], c["rot"], 0, c["texte"]), c["id"], f"cote {c['id']}")
        x, y, anc, b, haut, a_txt = places[c["id"]]
        c["grp"].append(P_txt(x, y, c["texte"], fc, anc, c["rot"]))
        if haut:
            base = pt_cote(c, a_txt if anc == "middle" else (c["c2"] if anc == "start" else c["c1"]), c["ligne"])
            tip = (x - c["up"][0] * 0.21 * fc, y - c["up"][1] * 0.21 * fc)
            if anc != "middle":
                tip = base[0] + c["up"][0] * (gap + fc * 1.2), base[1] + c["up"][1] * (gap + fc * 1.2)
            ld = P_pl([base, tip], "rappel")
            c["grp"].append(ld)
            PL.prims([ld], c["id"])
        c["boite"] = boite(x, y, MET.l(c["texte"], fc), fc, anc, c["rot"], 0, c["texte"])
        # repère ⚠
        l = c["l"]
        n, desc = None, None
        rep = l.get("repere")
        if rep:
            n = ctx["num_ecart"].get(str(rep))
            if n is None:
                verif.add("Repères d'incertitude", "AVERT", f"[{nid}] {c['id']} : repère « {rep} » sans écart correspondant")
                n = ctx["num_propre"].get(c["id"])
            desc = next((str(e.get("description") or "") for e in ctx["ecarts"] if str(e.get("id")) == str(rep)), "")
        elif c["source"] == "PRÉSUMÉ" or c["statut"] == "conflit":
            n = ctx["num_propre"].get(c["id"])
            desc = ("Cote présumée" if c["source"] == "PRÉSUMÉ" else "Cote en conflit") + f" ({c['id']})"
        if n is not None:
            g = D.g("70-Incertitudes", "rep-" + c["id"])
            placer_marqueur(n, c["boite"], "rep-" + c["id"], g, PL, mm, ignore=(c["id"],))
            reperes.append((n, str(rep or c["id"]), desc))
        # écart valeur attendue
        va = num(l.get("valeur_attendue"))
        if va is not None and abs(va - c["longueur"]) > 0.5:
            verif.add("Chaînes de cotes", "AVERT",
                      f"[{nid}] {c['id']} : longueur dessinée {pipo(c['longueur'])} ({f3(c['longueur'])} po) ≠ "
                      f"valeur attendue {pipo(va)} ({f3(va)} po), écart {f3(c['longueur'] - va)} po")
    return reperes


# ---------------------------------------------------------------------------
# Marqueurs ⚠n et libellés
# ---------------------------------------------------------------------------
def marqueur_prims(n, cx, cy, mm):
    s = mm(TRI)
    h = s * math.sqrt(3) / 2
    tri = [(cx - s / 2, cy - h / 3), (cx + s / 2, cy - h / 3), (cx, cy + 2 * h / 3)]
    bw = s * 0.07
    pr = [P_poly([tri], "inc"),
          P_poly([[(cx - bw, cy - h * 0.02), (cx + bw, cy - h * 0.02), (cx + bw * 0.8, cy + h * 0.42), (cx - bw * 0.8, cy + h * 0.42)]], "inc-blanc"),
          P_poly([[(cx - bw, cy - h * 0.2), (cx + bw, cy - h * 0.2), (cx + bw, cy - h * 0.1), (cx - bw, cy - h * 0.1)]], "inc-blanc")]
    f = mm(H_COTE / CAP)
    t = str(n)
    xt = cx + s / 2 + mm(0.4)
    yt = cy - h / 3
    pr.append(P_txt(xt, yt, t, f, "start", 0, True, ORANGE))
    tb = boite(xt, yt, MET.l(t, f, True), f, "start", 0, 0, t)
    return pr, Polygon(tri), tb


def placer_marqueur(n, ancre, own, g, PL, mm, point=None, ignore=()):
    s = mm(TRI)
    f = mm(H_COTE / CAP)
    larg = s + mm(0.4) + MET.l(str(n), f, True)
    haut = max(s * 0.87, f)
    minx, miny, maxx, maxy = ancre.bounds
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    best = None
    for d in (mm(0.8), mm(2.5), mm(5), mm(9), mm(14)):
        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)):
            x = cx + dx * ((maxx - minx) / 2 + d + larg / 2) - (s / 2 + mm(0.4) + MET.l(str(n), f, True) - s / 2) / 2 * 0
            y = cy + dy * ((maxy - miny) / 2 + d + haut / 2)
            tx = x - larg / 2 + s / 2           # centre du triangle
            pr, tri, tb = marqueur_prims(n, tx, y, mm)
            zone = unary_union([tri, tb]).envelope.buffer(mm(0.3), join_style=2)
            nconf = PL.conflits(zone, ignore=tuple(ignore) + (own,))
            if nconf == 0:
                best = (pr, tri, tb, d)
                break
            if best is None:
                best = (pr, tri, tb, d, nconf)
        if best is not None and len(best) == 4:
            break
    pr, tri, tb = best[0], best[1], best[2]
    if best[3] > mm(1.0) or point is not None:
        a, b = nearest_points(tri, Point(point) if point else ancre)
        if a.distance(b) > mm(0.5):
            ld = P_pl([(a.x, a.y), (b.x, b.y)], "inc-c")
            g.append(ld)
            PL.prims([ld], own)
    g += pr
    PL.ligne(tri, own)
    PL.texte(tb, own, f"repère ⚠{n} ({own})")


def bloc_lignes(lignes, cx, cy):
    """lignes = [(texte, police, gras)] → prims, boîte, liste de boîtes, centrées en (cx, cy)."""
    hs = [f * (1.18 if i else 1.0) for i, (t, f, g) in enumerate(lignes)]
    H = sum(hs) - 0.21 * lignes[-1][1] * 0
    top = cy + H / 2
    prims, boites = [], []
    y = top
    for (t, f, gr), h in zip(lignes, hs):
        y -= h
        yb = y + 0.24 * f
        prims.append(P_txt(cx, yb, t, f, "middle", 0, gr))
        boites.append(boite(cx, yb, MET.l(t, f, gr), f, "middle", 0, 0, t))
    return prims, unary_union(boites).envelope, boites


def placer_autour(geom, lignes, own, g, PL, mm, interieur=True, zones=False, extra_ignore=()):
    W = max(MET.l(t, f, gr) for t, f, gr in lignes)
    H = sum(f * (1.18 if i else 1.0) for i, (t, f, gr) in enumerate(lignes))
    minx, miny, maxx, maxy = geom.bounds
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    cands = []
    if interieur:
        cands.append((cx, cy, 0.0))
    for d in (mm(1.2), mm(4), mm(8), mm(13)):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)):
            cands.append((cx + dx * ((maxx - minx) / 2 + d + W / 2), cy + dy * ((maxy - miny) / 2 + d + H / 2), d))
    choix = None
    for x, y, d in cands:
        pr, env, bx = bloc_lignes(lignes, x, y)
        zone = env.buffer(mm(0.3), join_style=2)
        if d == 0.0 and not zone.within(geom):
            continue
        if PL.conflits(zone, ignore=(own,) + tuple(extra_ignore), zones=zones) == 0:
            choix = (pr, env, bx, d)
            break
    if choix is None:
        x, y, d = cands[1] if len(cands) > 1 else cands[0]
        pr, env, bx = bloc_lignes(lignes, x, y)
        choix = (pr, env, bx, d)
    pr, env, bx, d = choix
    if d > mm(1.5):
        a, b = nearest_points(env, geom)
        ld = P_pl([(a.x, a.y), (b.x, b.y)], "rappel")
        g.append(ld)
        PL.prims([ld], own)
    g += pr
    for i, b in enumerate(bx):
        PL.texte(b, own, f"libellé {own} « {lignes[i][0]} »")
    return True


def placer_libelle_element(el, cont, libs, g, PL, mm, fc):
    interieur_ok = el["typ"] not in SANS_INTERIEUR
    # 1) à l'intérieur du symbole
    if interieur_ok:
        for t in libs:
            pr, env, bx = bloc_lignes([(t, fc, False)], cont.centroid.x, cont.centroid.y)
            zone = env.buffer(mm(0.3), join_style=2)
            if zone.within(cont.buffer(-mm(0.2))) and PL.conflits(zone, ignore=(el["id"],)) == 0:
                g += pr
                PL.texte(bx[0], el["id"], f"libellé {el['id']} « {t} »")
                return
    # 2) autour
    for t in libs:
        lignes = [(t, fc, False)]
        W = MET.l(t, fc)
        minx, miny, maxx, maxy = cont.bounds
        cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
        for d in (mm(1.2), mm(4), mm(8)):
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)):
                x = cx + dx * ((maxx - minx) / 2 + d + W / 2)
                y = cy + dy * ((maxy - miny) / 2 + d + fc / 2)
                pr, env, bx = bloc_lignes(lignes, x, y)
                zone = env.buffer(mm(0.3), join_style=2)
                if PL.conflits(zone, ignore=(el["id"],), zones=True) == 0:
                    if d > mm(1.5):
                        a, b = nearest_points(env, cont)
                        ld = P_pl([(a.x, a.y), (b.x, b.y)], "rappel")
                        g.append(ld)
                        PL.prims([ld], el["id"])
                    g += pr
                    PL.texte(bx[0], el["id"], f"libellé {el['id']} « {t} »")
                    return
    placer_autour(cont, [(libs[-1], fc, False)], el["id"], g, PL, mm, interieur=False)


def placer_long_ligne(geo, lib, own, g, PL, mm, fc):
    coords = list(geo.coords)
    A, B = coords[0], coords[-1]
    ang = math.degrees(math.atan2(B[1] - A[1], B[0] - A[0]))
    if ang > 90.0001 or ang <= -90:
        ang = (ang + 180) % 360
        if ang > 180:
            ang -= 360
    up = rot2((0, 1), ang)
    w = MET.l(lib, fc)
    L = geo.length
    choix = None
    for frac in (0.5, 0.35, 0.65, 0.22, 0.78, 0.12, 0.88, 0.42, 0.58, 0.3, 0.7):
        p = geo.interpolate(frac, normalized=True)
        for off in (mm(0.9) + 0.21 * fc, -(mm(0.9) + 0.76 * fc), mm(2.5) + 0.21 * fc, -(mm(2.5) + 0.76 * fc),
                    mm(4.5) + 0.21 * fc, -(mm(4.5) + 0.76 * fc)):
            x, y = p.x + up[0] * off, p.y + up[1] * off
            b = boite(x, y, w, fc, "middle", ang, mm(0.3), lib)
            if PL.conflits(b, ignore=(own,), zones=True) == 0:
                choix = (x, y)
                break
        if choix:
            break
    if choix is None:
        p = geo.interpolate(0.5, normalized=True)
        choix = (p.x + up[0] * (mm(0.9) + 0.21 * fc), p.y + up[1] * (mm(0.9) + 0.21 * fc))
    g.append(P_txt(choix[0], choix[1], lib, fc, "middle", ang))
    PL.texte(boite(choix[0], choix[1], w, fc, "middle", ang, 0, lib), own, f"libellé {own} « {lib} »")


def lignes_nom(nom, fn, lmax):
    if MET.l(nom, fn, True) <= lmax:
        return [nom]
    mots = nom.split()
    best = None
    for i in range(1, len(mots)):
        l1, l2 = " ".join(mots[:i]), " ".join(mots[i:])
        w = max(MET.l(l1, fn, True), MET.l(l2, fn, True))
        if best is None or w < best[0]:
            best = (w, [l1, l2])
    return best[1] if best else [nom]


def placer_etiquette_piece(d, poly, D, PL, mm, fn, fc):
    pid = str(d.get("id"))
    g = D.g("60-Etiquettes", pid)
    g.append(P_poly([list(poly.exterior.coords)[:-1]], "invisible"))
    nom = str(d.get("nom") or d.get("nom_original") or pid).upper()
    dims = d.get("dimensions") if isinstance(d.get("dimensions"), dict) else {}
    minx, miny, maxx, maxy = poly.bounds
    vx, vy = num(dims.get("x")), num(dims.get("y"))
    sx, sy = src(dims.get("x")), src(dims.get("y"))
    if vx is None:
        vx, sx = maxx - minx, "DÉDUIT"
    if vy is None:
        vy, sy = maxy - miny, "DÉDUIT"
    tx = ("≈" if sx == "ESTIMÉ" else "") + pipo(vx)
    ty = ("≈" if sy == "ESTIMÉ" else "") + pipo(vy)
    sup = d.get("superficie") if isinstance(d.get("superficie"), dict) else {}
    a = num(sup)
    if a is None:
        a = poly.area / 144
    ta = ("≈" if src(sup) == "ESTIMÉ" else "") + f"{fr(a, 1)} pi² ({fr(a * 0.09290304, 1)} m²)"
    lmax = (maxx - minx) * 0.92
    noms = lignes_nom(nom, fn, lmax)
    jeux = [noms]
    if len(noms) == 1 and len(nom.split()) > 1:
        jeux.append(lignes_nom(nom, fn, 0))          # nom coupé en deux lignes
    variantes = []
    for sous in ([(f"{tx} × {ty}", fc, False), (ta, fc, False)], [(ta, fc, False)], []):
        for nn in jeux:
            variantes.append([(t, fn, True) for t in nn] + sous)
    try:
        pole = polylabel(poly, tolerance=1.0)
    except Exception:
        pole = poly.representative_point()
    interieur = poly.buffer(-mm(0.6), join_style=2)
    choix = None
    for lignes in variantes:
        W = max(MET.l(t, f, gr) for t, f, gr in lignes)
        H = sum(f * (1.18 if i else 1.0) for i, (t, f, gr) in enumerate(lignes))
        if W > (maxx - minx) or H > (maxy - miny):
            continue
        step = max(mm(1.5), min(W, H) / 4)
        pts = [(pole.x, pole.y)]
        nx = int((maxx - minx) / step) + 1
        ny = int((maxy - miny) / step) + 1
        grille = []
        for i in range(nx + 1):
            for j in range(ny + 1):
                x, y = minx + i * step, miny + j * step
                grille.append(((x - pole.x) ** 2 + (y - pole.y) ** 2, round(x, 4), round(y, 4)))
        grille.sort()
        pts += [(x, y) for _, x, y in grille[:900]]
        env0 = bloc_lignes(lignes, 0.0, 0.0)[1].buffer(mm(0.4), join_style=2)
        for x, y in pts:
            zone = affinity.translate(env0, x, y)
            if not zone.within(interieur):
                continue
            if PL.conflits(zone, ignore=(pid,), zones=True) == 0:
                choix = (lignes, x, y)
                break
        if choix:
            break
    leader = None
    if choix is None:
        # hors de la pièce, avec ligne de rappel vers le pôle
        for lignes in ([(t, fn, True) for t in noms] + [(ta, fc, False)], [(t, fn, True) for t in noms]):
            W = max(MET.l(t, f, gr) for t, f, gr in lignes)
            H = sum(f * (1.18 if i else 1.0) for i, (t, f, gr) in enumerate(lignes))
            env0 = bloc_lignes(lignes, 0.0, 0.0)[1]
            for d in (mm(4), mm(7), mm(11), mm(16), mm(22), mm(30)):
                for ang in range(0, 360, 30):
                    x = pole.x + math.cos(math.radians(ang)) * (d + W / 2)
                    y = pole.y + math.sin(math.radians(ang)) * (d + H / 2)
                    env = affinity.translate(env0, x, y)
                    a_, b_ = nearest_points(env, Point(pole.x, pole.y))
                    ld = LineString([(a_.x, a_.y), (pole.x, pole.y)])
                    if PL.conflits(env.buffer(mm(0.4), join_style=2), ignore=(pid,), zones=True) == 0 and \
                            not any(PL.T[i].intersects(ld) for i in range(len(PL.T))):
                        choix, leader = (lignes, x, y), ld
                        break
                if choix:
                    break
            if choix:
                break
    if choix is None:
        choix = (variantes[-1], pole.x, pole.y)
    lignes, x, y = choix
    pr, env, bx = bloc_lignes(lignes, x, y)
    if leader is not None:
        lp = [P_pl(list(leader.coords), "rappel"), P_cercle(leader.coords[-1], mm(0.5), "elem-plein")]
        g += lp
        PL.prims(lp, pid)
    g += pr
    for i, b in enumerate(bx):
        PL.texte(b, pid, f"étiquette {pid} « {lignes[i][0]} »")


def verifier_textes(F, verif):
    PL = F.placeur
    n = 0
    vus = set()
    T = PL.T
    tree = STRtree(T) if T else None
    for i, g in enumerate(T):
        for j in tree.query(g, predicate="intersects"):
            j = int(j)
            if j <= i or PL.To[i] == PL.To[j] and PL.To[i] == "cartouche" and False:
                continue
            inter = g.intersection(T[j]).area
            if inter > 1e-4 and (i, j) not in vus:
                vus.add((i, j))
                c = g.centroid
                verif.add("Textes (chevauchements)", "AVERT",
                          f"[{F.nid}] texte/texte : {PL.Td[i]} × {PL.Td[j]} (x≈{f3(c.x)}, y≈{f3(c.y)} po)")
                n += 1
    lt = STRtree(PL.L) if PL.L else None
    if lt is not None:
        for i, g in enumerate(T):
            for j in lt.query(g, predicate="intersects"):
                j = int(j)
                if PL.Lo[j] == PL.To[i]:
                    continue
                c = g.centroid
                verif.add("Textes (chevauchements)", "AVERT",
                          f"[{F.nid}] texte/trait : {PL.Td[i]} × trait de {PL.Lo[j]} (x≈{f3(c.x)}, y≈{f3(c.y)} po)")
                n += 1
    F.nb_chev = n
    if n == 0:
        verif.add("Textes (chevauchements)", "OK", f"[{F.nid}] aucun chevauchement texte/texte ni texte/trait "
                                                   f"({len(T)} textes vérifiés)")


# ---------------------------------------------------------------------------
# Cartouche
# ---------------------------------------------------------------------------
def cartouche(F, niv, projet, ctx):
    k, mm, X0, Y0 = F.k, F.mm, F.X0, F.Y0
    D, PL = F.dessin, F.placeur
    g = D.g("00-Cartouche", "cartouche")

    def S(sx, sy):              # po imprimés depuis le haut-gauche → coordonnées maison
        return (sx * k - X0, Y0 - sy * k)

    def ligne(pts, st="cart-f"):
        g.append(P_pl([S(*p) for p in pts], st))

    def rect(x0, y0, x1, y1, st):
        g.append(P_poly([[S(x0, y0), S(x1, y0), S(x1, y1), S(x0, y1)]], st))

    def rcadre(x0, y0, x1, y1, st):
        g.append(P_pl([S(x0, y0), S(x1, y0), S(x1, y1), S(x0, y1)], st, True))

    def texte(sx, sy, t, hcap, gras=False, ancre="start", coul="#000000"):
        f = mm(hcap / CAP)
        x, y = S(sx, sy)
        g.append(P_txt(x, y, t, f, ancre, 0, gras, coul))
        PL.texte(boite(x, y, MET.l(t, f, gras), f, ancre, 0, 0, t), "cartouche", f"cartouche « {t[:30]} »")
        return hcap / 25.4

    def lw(t, hcap, gras=False):     # largeur en po imprimés
        return MET.l(t, hcap / CAP, gras) / 25.4

    def wrap(t, hcap, larg, gras=False):
        return couper(t, hcap / CAP * 25.4 / 25.4, larg * 25.4, gras) if t else []

    # fond blanc et cadre de feuille
    g.append(P_poly([[S(0, 0), S(FEUILLE_L, 0), S(FEUILLE_L, FEUILLE_H), S(0, FEUILLE_H)]], "fond"))
    rcadre(MARGE, MARGE, FEUILLE_L - MARGE, FEUILLE_H - MARGE, "cart-cadre")
    x0, x1 = FEUILLE_L - MARGE - CART_L, FEUILLE_L - MARGE
    y0, y1 = MARGE, FEUILLE_H - MARGE
    ligne([(x0, y0), (x0, y1)], "cart-cadre")
    p = 0.09
    L = x1 - x0 - 2 * p
    cap_s, cap_m = 2.5, 3.0
    pas_s = 2.5 / 25.4 * 1.55
    y = y0 + p

    def cap(t, yy):
        texte(x0 + p, yy + 2.5 / 25.4, t, 2.5, True)
        return yy + 2.5 / 25.4 * 1.7

    # --- Projet
    y = cap("PROJET", y)
    for t in couper(projet.get("nom") or "", 3.2 / CAP, L * 25.4, True):
        y += 3.2 / 25.4
        texte(x0 + p, y, t, 3.2, True)
        y += 3.2 / 25.4 * 0.55
    y += 0.06
    # --- Avertissement
    msg = "RELEVÉ DE L'EXISTANT — PRÉLIMINAIRE, À VALIDER SUR PLACE"
    lignes = couper(msg, 3.0 / CAP, (L - 0.12) * 25.4, True)
    hbox = len(lignes) * 3.0 / 25.4 * 1.6 + 0.1
    rcadre(x0 + p, y, x1 - p, y + hbox, "cart-l")
    yy = y + 0.06
    for t in lignes:
        yy += 3.0 / 25.4
        texte((x0 + x1) / 2, yy, t, 3.0, True, "middle")
        yy += 3.0 / 25.4 * 0.6
    y += hbox + 0.08
    ligne([(x0, y), (x1, y)], "cart-l")
    y += 0.07

    # --- bloc du bas (de bas en haut)
    yb = y1
    # Niveau | Feuille
    hrow = 0.72
    xs = x1 - 1.15
    ligne([(x0, yb - hrow), (x1, yb - hrow)], "cart-l")
    ligne([(xs, yb - hrow), (xs, yb)], "cart-l")
    texte(x0 + p, yb - hrow + 0.05 + 2.5 / 25.4, "NIVEAU", 2.5, True)
    hn = 4.0
    while hn > 3.0 and lw(F.nom.upper(), hn, True) > xs - x0 - 2 * p:
        hn -= 0.25
    nl = couper(F.nom.upper(), hn / CAP, (xs - x0 - 2 * p) * 25.4, True)
    yy = yb - hrow + 0.05 + 2.5 / 25.4 * 2.1
    for t in nl[:2]:
        yy += hn / 25.4
        texte(x0 + p, yy, t, hn, True)
        yy += hn / 25.4 * 0.45
    texte(xs + p, yb - hrow + 0.05 + 2.5 / 25.4, "FEUILLE", 2.5, True)
    texte((xs + x1) / 2, yb - 0.12, F.feuille, 7.0, True, "middle")
    yb -= hrow
    # Échelle | Date | Révision
    hrow = 0.48
    ligne([(x0, yb - hrow), (x1, yb - hrow)], "cart-l")
    xa, xb_ = x0 + 1.25, x0 + 2.3
    ligne([(xa, yb - hrow), (xa, yb)], "cart-l")
    ligne([(xb_, yb - hrow), (xb_, yb)], "cart-l")
    for xx, cap_t, val in ((x0, "ÉCHELLE", F.echelle), (xa, "DATE", str(projet.get("date") or "—")),
                           (xb_, "RÉVISION", str(projet.get("revision") or "—"))):
        texte(xx + p, yb - hrow + 0.05 + 2.5 / 25.4, cap_t, 2.5, True)
        texte(xx + p, yb - 0.1, val, 3.0)
    yb -= hrow
    # Photos sources
    hrow = 0.42
    ligne([(x0, yb - hrow), (x1, yb - hrow)], "cart-l")
    texte(x0 + p, yb - hrow + 0.05 + 2.5 / 25.4, "PHOTOS SOURCES", 2.5, True)
    ph = niv.get("photos_sources") or []
    texte(x0 + p, yb - 0.1, ", ".join(str(x) for x in ph) if ph else "—", 3.0)
    yb -= hrow
    # Échelle graphique
    hrow = 0.62
    ligne([(x0, yb - hrow), (x1, yb - hrow)], "cart-l")
    texte(x0 + p, yb - hrow + 0.05 + 2.5 / 25.4, "ÉCHELLE GRAPHIQUE (pi)", 2.5, True)
    gx0 = x0 + p + 0.05
    gy = yb - 0.27
    hb = 1.6 / 25.4
    grad = F.grad
    for i in range(len(grad) - 1):
        a, b = grad[i] * 12 / k, grad[i + 1] * 12 / k
        rect(gx0 + a, gy, gx0 + b, gy + hb, "cart-noir" if i % 2 == 0 else "cart-blanc")
    rcadre(gx0, gy, gx0 + grad[-1] * 12 / k, gy + hb, "cart-f")
    for v in grad:
        t = str(v) + (" pi" if v == grad[-1] else "")
        texte(gx0 + v * 12 / k, gy + hb + 0.03 + 2.5 / 25.4, t, 2.5, False, "start" if v == grad[-1] and False else "middle")
    yb -= hrow
    # Nord
    nord = projet.get("nord") if isinstance(projet.get("nord"), dict) else {}
    ang = num(nord.get("angle_deg"))
    if ang is not None:
        hrow = 0.95
        ligne([(x0, yb - hrow), (x1, yb - hrow)], "cart-l")
        r = 0.3
        cx, cy = x0 + p + r + 0.05, yb - hrow / 2 + 0.06
        C = S(cx, cy)
        R = r * k
        g.append(P_cercle(C, R, "cart-f"))
        pts = [(0, R * 0.92), (-R * 0.32, -R * 0.62), (0, -R * 0.3), (R * 0.32, -R * 0.62)]
        pts = [rot2(q, -ang) for q in pts]
        pts = [(C[0] + a, C[1] + b) for a, b in pts]
        g.append(P_poly([[pts[0], pts[1], pts[2]]], "cart-noir"))
        g.append(P_poly([[pts[0], pts[2], pts[3]]], "cart-blanc"))
        tip = rot2((0, R * 1.0 + mm(1.2)), -ang)
        fN = mm(3.0 / CAP)
        xN, yN = C[0] + tip[0] * 1.0, C[1] + tip[1] * 1.0
        # « N » placé au-delà de la pointe, hors du cercle
        dirn = rot2((0, 1), -ang)
        xN, yN = C[0] + dirn[0] * (R + mm(2.2)), C[1] + dirn[1] * (R + mm(2.2)) - 0.35 * fN
        g.append(P_txt(xN, yN, "N", fN, "middle", 0, True))
        PL.texte(boite(xN, yN, MET.l("N", fN, True), fN, "middle", 0, 0, "N"), "cartouche", "cartouche « N »")
        tx = cx + r + 0.28
        yy = yb - hrow + 0.08
        yy += 2.5 / 25.4
        texte(tx, yy, "NORD", 2.5, True)
        stxt = f"{f3(ang)}° (sens horaire depuis +y). Source : {nord.get('source') or '—'}"
        if nord.get("photo"):
            stxt += f" ({nord.get('photo')})"
        for t in couper(stxt, 2.5 / CAP, (x1 - p - tx) * 25.4)[:5]:
            yy += 2.5 / 25.4 * 1.5
            texte(tx, yy, t, 2.5)
        yb -= hrow

    # --- Zone centrale : légende, repères, notes
    ymax = yb - 0.06
    ycur = y

    def peut(h):
        return ycur + h <= ymax

    # Légende
    ycur = cap("LÉGENDE", ycur)
    sw, sh = 0.42, 0.11
    lx = x0 + p + sw + 0.1
    items = [("lourd", "Mur extérieur / fondation"), ("leger", "Mur intérieur (cloison)"),
             ("poutre", "Poutre (au-dessus)"), ("axe", "Axe porteur d'origine"),
             ("col", "Colonne"), ("sol", "Solives (sens)"),
             ("approx", "Valeur estimée (mesurée sur l'image)"),
             ("rep", "Voir registre des écarts dans RAPPORT.md"),
             ("cote", "Cotes en pi-po (métrique en m)")]
    for kind, t in items:
        if not peut(0.2):
            break
        yc = ycur + 0.07
        sx0, sx1 = x0 + p, x0 + p + sw
        if kind == "lourd":
            rect(sx0, yc - sh / 2, sx1, yc + sh / 2, "cart-lourd")
        elif kind == "leger":
            rect(sx0, yc - sh / 2 * 0.75, sx1, yc + sh / 2 * 0.75, "cart-leger")
        elif kind in ("poutre", "axe"):
            g.append(P_pl([S(sx0, yc), S(sx1, yc)], "str-poutre" if kind == "poutre" else "str-axe"))
        elif kind == "col":
            a, b = S((sx0 + sx1) / 2 - 0.05, yc - 0.05), S((sx0 + sx1) / 2 + 0.05, yc + 0.05)
            g.append(P_pl([a, (b[0], a[1]), b, (a[0], b[1])], "str", True))
            g.append(P_pl([a, b], "str-fin"))
            g.append(P_pl([(b[0], a[1]), (a[0], b[1])], "str-fin"))
        elif kind == "sol":
            A, B = S(sx0, yc), S(sx1, yc)
            g.append(P_pl([A, B], "str-fin"))
            ah, aw = mm(2.0), mm(0.8)
            g.append(P_poly([[B, (B[0] - ah, B[1] + aw), (B[0] - ah, B[1] - aw)]], "str-plein"))
            g.append(P_poly([[A, (A[0] + ah, A[1] + aw), (A[0] + ah, A[1] - aw)]], "str-plein"))
        elif kind == "approx":
            texte((sx0 + sx1) / 2, yc + 0.045, "≈", 3.0, True, "middle")
        elif kind == "rep":
            C = S((sx0 + sx1) / 2 - 0.04, yc + 0.01)
            pr, tri, tb = marqueur_prims("n", C[0], C[1], mm)
            g.extend(pr[:3])
            ftxt = pr[3]
            g.append(ftxt)
            PL.texte(tb, "cartouche", "cartouche « ⚠n »")
        elif kind == "cote":
            A, B = S(sx0, yc + 0.03), S(sx1, yc + 0.03)
            g.append(P_pl([A, B], "cote"))
            tk = mm(C_TICK) / 2 / math.sqrt(2)
            for T in (A, B):
                g.append(P_pl([(T[0] - tk, T[1] - tk), (T[0] + tk, T[1] + tk)], "cote-tick"))
        lg = couper(t, 2.5 / CAP, (x1 - p - lx) * 25.4)
        for i_, t_ in enumerate(lg):
            texte(lx, yc + 0.045 + i_ * pas_s, t_, 2.5)
        ycur += 0.19 + (len(lg) - 1) * pas_s
    ycur += 0.04
    ligne([(x0, ycur), (x1, ycur)], "cart-l")
    ycur += 0.06

    # Repères de la feuille
    if F.reperes:
        ycur = cap("REPÈRES ⚠ SUR CETTE FEUILLE".replace("⚠ ", ""), ycur)
        tronque = False
        for n, rid, desc in F.reperes:
            lignes = couper(f"{desc}" + (f" [{rid}]" if rid and rid not in desc else ""), 2.5 / CAP, (L - 0.42) * 25.4)
            h = len(lignes) * pas_s + 0.05
            if not peut(h + 0.05):
                tronque = True
                break
            C = S(x0 + p + 0.09, ycur + 0.06)
            pr, tri, tb = marqueur_prims(n, C[0], C[1], mm)
            g.extend(pr)
            PL.texte(tb, "cartouche", f"cartouche « ⚠{n} »")
            yy = ycur
            for t in lignes:
                yy += 2.5 / 25.4
                texte(x0 + p + 0.42, yy, t, 2.5)
                yy += pas_s - 2.5 / 25.4
            ycur += h
        if tronque and peut(0.12):
            ycur += 2.5 / 25.4
            texte(x0 + p, ycur, "… liste complète : donnees/verifications.txt", 2.5)
            ycur += 0.06
        ycur += 0.03
        ligne([(x0, ycur), (x1, ycur)], "cart-l")
        ycur += 0.06
    # Notes
    notes = [n_ for n_ in (niv.get("notes") or []) if isinstance(n_, dict)]
    if notes and peut(0.3):
        ycur = cap("NOTES DU PLAN D'ORIGINE (traduites)", ycur)
        for i, n_ in enumerate(notes, 1):
            t = str(n_.get("interpretation") or n_.get("texte_original") or "")
            if n_.get("texte_original") and n_.get("interpretation"):
                t += f" [« {n_.get('texte_original')} »]"
            lignes = couper(f"{i}. {t}", 2.5 / CAP, L * 25.4)
            h = len(lignes) * pas_s
            if not peut(h):
                if peut(0.12):
                    ycur += 2.5 / 25.4
                    texte(x0 + p, ycur, "… autres notes : voir maison.json", 2.5)
                break
            for t2 in lignes:
                ycur += 2.5 / 25.4
                texte(x0 + p, ycur, t2, 2.5)
                ycur += pas_s - 2.5 / 25.4
            ycur += 0.03


# ---------------------------------------------------------------------------
# Sortie SVG
# ---------------------------------------------------------------------------
def css(k):
    def mm(v):
        return v / 25.4 * k
    out = []
    for nom, (fill, stroke, sw, dash) in STYLES.items():
        r = [f"fill:{fill or 'none'}"]
        if stroke:
            r += [f"stroke:{stroke}", f"stroke-width:{f3(mm(sw))}", "stroke-linecap:butt", "stroke-linejoin:miter"]
            if dash:
                r.append("stroke-dasharray:" + ",".join(f3(mm(d)) for d in dash))
        else:
            r.append("stroke:none")
        out.append(f".{nom}{{{';'.join(r)}}}")
    return "\n".join(out)


def svg_feuille(F, projet):
    k, X0, Y0 = F.k, F.X0, F.Y0

    def X(x):
        return f3(X0 + x)

    def Y(y):
        return f3(Y0 - y)

    def pts(lst):
        return " ".join(f"{X(a)},{Y(b)}" for a, b in lst)

    o = ['<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
         '<svg xmlns="http://www.w3.org/2000/svg" '
         'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
         'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" '
         f'width="17in" height="11in" viewBox="0 0 {f3(FEUILLE_L * k)} {f3(FEUILLE_H * k)}" version="1.1">',
         f"<title>{esc(F.feuille)} — {esc(F.nom)} — {esc(projet.get('nom') or '')}</title>",
         f"<desc>Relevé de l'existant — préliminaire. Échelle {esc(F.echelle)} ; 1 unité = 1 po réel. "
         f"Révision {esc(projet.get('revision') or '')}, {esc(projet.get('date') or '')}.</desc>",
         '<sodipodi:namedview id="namedview" pagecolor="#ffffff" bordercolor="#666666" '
         'inkscape:document-units="in" showgrid="false"/>',
         "<defs><style type=\"text/css\">", css(k), "</style></defs>"]
    for cal in CALQUES:
        o.append(f'<g inkscape:groupmode="layer" inkscape:label="{cal}" id="{cal}">')
        for gid, prims in F.dessin.groupes[cal]:
            if not prims:
                continue
            if gid:
                o.append(f'<g id="{esc(gid)}">')
            for p in prims:
                k_ = p["k"]
                if k_ == "pl":
                    tag = "polygon" if p["ferme"] else "polyline"
                    o.append(f'<{tag} class="{p["st"]}" points="{pts(p["pts"])}"/>')
                elif k_ == "poly":
                    d = " ".join("M " + " L ".join(f"{X(a)} {Y(b)}" for a, b in r) + " Z" for r in p["rings"] if len(r) >= 3)
                    o.append(f'<path class="{p["st"]}" fill-rule="evenodd" d="{d}"/>')
                elif k_ == "arc":
                    c, r, a0, da = p["c"], p["r"], p["a0"], p["da"]
                    s = (c[0] + r * math.cos(math.radians(a0)), c[1] + r * math.sin(math.radians(a0)))
                    e = (c[0] + r * math.cos(math.radians(a0 + da)), c[1] + r * math.sin(math.radians(a0 + da)))
                    big = 1 if abs(da) > 180 else 0
                    sweep = 0 if da > 0 else 1
                    o.append(f'<path class="{p["st"]}" d="M {X(s[0])} {Y(s[1])} A {f3(r)} {f3(r)} 0 {big} {sweep} '
                             f'{X(e[0])} {Y(e[1])}"/>')
                elif k_ == "cercle":
                    o.append(f'<circle class="{p["st"]}" cx="{X(p["c"][0])}" cy="{Y(p["c"][1])}" r="{f3(p["r"])}"/>')
                elif k_ == "txt":
                    x, y = X(p["x"]), Y(p["y"])
                    tr = f' transform="rotate({f3(-p["rot"])} {x} {y})"' if abs(p["rot"]) > 1e-9 else ""
                    gr = ' font-weight="bold"' if p["gras"] else ""
                    o.append(f'<text x="{x}" y="{y}" font-family="{POLICE}" font-size="{f3(p["f"])}"{gr} '
                             f'text-anchor="{p["ancre"]}" fill="{p["coul"]}"{tr}>{esc(p["s"])}</text>')
            if gid:
                o.append("</g>")
        o.append("</g>")
    o.append("</svg>")
    return "\n".join(o) + "\n"


# ---------------------------------------------------------------------------
# Sortie DXF
# ---------------------------------------------------------------------------
LW_OK = [0, 5, 9, 13, 15, 18, 20, 25, 30, 35, 40, 50, 53, 60, 70, 80, 90, 100, 106, 120, 140, 158, 200, 211]


def dxf_feuille(F, chemin):
    import ezdxf
    from ezdxf.enums import TextEntityAlignment
    from ezdxf import const
    ezdxf.options.write_fixed_meta_data_for_testing = True
    k = F.k
    doc = ezdxf.new("R2010", setup=True)
    doc.header["$INSUNITS"] = 1
    doc.header["$MEASUREMENT"] = 0
    doc.header["$LUNITS"] = 4
    doc.header["$LTSCALE"] = 1.0
    doc.appids.add("RELEVE")
    for cal in CALQUES:
        lay = doc.layers.add(cal, color=7)
        if cal == "70-Incertitudes":
            lay.color = 30
            lay.rgb = (0xE8, 0x73, 0x0C)
    if "RELEVE" not in doc.styles:
        doc.styles.add("RELEVE", font="arial.ttf")
        doc.styles.add("RELEVE_GRAS", font="arialbd.ttf")
    lts = set(lt.dxf.name for lt in doc.linetypes)
    msp = doc.modelspace()

    def rgb(hexa):
        return tuple(int(hexa[i:i + 2], 16) for i in (1, 3, 5))

    def attrs(cal, st, trait=True):
        fill, stroke, sw, dash = STYLES[st]
        a = {"layer": cal}
        coul = stroke if trait else fill
        if coul and coul.upper() == ORANGE:
            a["color"] = 30
            a["true_color"] = ezdxf.colors.rgb2int(rgb(ORANGE))
        elif coul and coul not in ("#000000",):
            a["true_color"] = ezdxf.colors.rgb2int(rgb(coul))
        else:
            a["color"] = 7
        if trait and sw:
            v = int(round(sw * 100))
            a["lineweight"] = min(LW_OK, key=lambda z: abs(z - v))
        if trait and st in DXF_LT and DXF_LT[st][0] in lts:
            nom, lng = DXF_LT[st]
            base = {"DASHED": 0.75, "DASHDOT": 1.0, "HIDDEN": 0.375}[nom]
            a["linetype"] = nom
            a["ltscale"] = (lng / 25.4 * k) / base
        return a

    def xd(e, gid):
        if gid:
            e.set_xdata("RELEVE", [(1000, gid)])

    for cal in CALQUES:
        for gid, prims in F.dessin.groupes[cal]:
            for p in prims:
                st = p.get("st")
                k_ = p["k"]
                if k_ == "pl":
                    if STYLES[st][1] is None:
                        continue
                    e = msp.add_lwpolyline(p["pts"], close=p["ferme"], dxfattribs=attrs(cal, st))
                    xd(e, gid)
                elif k_ == "poly":
                    fill, stroke = STYLES[st][0], STYLES[st][1]
                    if fill and fill.upper() != "#FFFFFF":
                        a = attrs(cal, st, trait=False)
                        h = msp.add_hatch(dxfattribs={"layer": cal})
                        h.set_solid_fill(color=a.get("color", 7), rgb=rgb(fill))
                        for i, r in enumerate(p["rings"]):
                            if len(r) >= 3:
                                h.paths.add_polyline_path(r, is_closed=True,
                                                          flags=const.BOUNDARY_PATH_EXTERNAL if i == 0 else const.BOUNDARY_PATH_DEFAULT)
                        xd(h, gid)
                    if stroke:
                        for r in p["rings"]:
                            e = msp.add_lwpolyline(r, close=True, dxfattribs=attrs(cal, st))
                            xd(e, gid)
                elif k_ == "arc":
                    a0, da = p["a0"], p["da"]
                    s_, e_ = (a0, a0 + da) if da > 0 else (a0 + da, a0)
                    e = msp.add_arc(p["c"], p["r"], s_ % 360, e_ % 360, dxfattribs=attrs(cal, st))
                    xd(e, gid)
                elif k_ == "cercle":
                    fill, stroke = STYLES[st][0], STYLES[st][1]
                    if stroke:
                        e = msp.add_circle(p["c"], p["r"], dxfattribs=attrs(cal, st))
                        xd(e, gid)
                    elif fill and fill.upper() != "#FFFFFF":
                        h = msp.add_hatch(dxfattribs={"layer": cal})
                        h.set_solid_fill(color=30 if fill.upper() == ORANGE else 7, rgb=rgb(fill))
                        h.paths.add_polyline_path(ellipse(p["c"][0], p["c"][1], p["r"], p["r"], 16), is_closed=True)
                        xd(h, gid)
                elif k_ == "txt":
                    a = {"layer": cal, "style": "RELEVE_GRAS" if p["gras"] else "RELEVE"}
                    if p["coul"].upper() == ORANGE:
                        a["color"] = 30
                        a["true_color"] = ezdxf.colors.rgb2int(rgb(ORANGE))
                    else:
                        a["color"] = 7
                    e = msp.add_text(p["s"], height=p["f"] * CAP, rotation=p["rot"], dxfattribs=a)
                    al = {"start": TextEntityAlignment.LEFT, "middle": TextEntityAlignment.CENTER,
                          "end": TextEntityAlignment.RIGHT}[p["ancre"]]
                    e.set_placement((p["x"], p["y"]), align=al)
                    xd(e, gid)
    doc.saveas(chemin)


# ---------------------------------------------------------------------------
# Tableau des pièces, bilan de surface, chaînes
# ---------------------------------------------------------------------------
def lignes_csv(F, niv, verif):
    rows = []
    hp_niv = niv.get("hauteur_plafond")
    for d, poly in F.pieces:
        pid = str(d.get("id"))
        dims = d.get("dimensions") if isinstance(d.get("dimensions"), dict) else {}
        minx, miny, maxx, maxy = poly.bounds
        vx, vy = num(dims.get("x")), num(dims.get("y"))
        srcs = []
        if vx is None:
            vx = maxx - minx
            srcs.append("DÉDUIT")
        else:
            srcs.append(src(dims.get("x")) or "DÉDUIT")
        if vy is None:
            vy = maxy - miny
            srcs.append("DÉDUIT")
        else:
            srcs.append(src(dims.get("y")) or "DÉDUIT")
        sup = d.get("superficie") if isinstance(d.get("superficie"), dict) else {}
        a_poly = poly.area / 144
        a = num(sup)
        if a is None:
            a = a_poly
            srcs.append("DÉDUIT")
        else:
            srcs.append(src(sup) or "DÉDUIT")
            if abs(a - a_poly) > 1.0:
                verif.add("Pièces", "AVERT", f"[{F.nid}] {pid} : superficie déclarée {fr(a, 1)} pi² ≠ "
                                             f"polygone {fr(a_poly, 1)} pi²")
        hp = d.get("hauteur_plafond")
        h = num(hp)
        if h is None:
            h = num(hp_niv)
        per = poly.exterior.length
        np_, nf = 0, 0
        for o in F.ouvs:
            c = Point(o.mur.pt(o.pos))
            if poly.exterior.distance(c) <= o.mur.t / 2 + 1.0:
                if o.type == "fenetre":
                    nf += 1
                elif o.est_porte():
                    np_ += 1
        lg, la = max(vx, vy), min(vx, vy)
        rows.append([F.nid, pid, str(d.get("nom") or ""), pipo(lg), pipo(la), fr(a, 2), fr(a * 0.09290304, 2),
                     pipo(per), pipo(h) if h else "", fr(per * h / 144, 2) if h else "", str(np_), str(nf),
                     pire_source(srcs)])
    return rows


def bilan_surface(F, verif):
    murs = F.murs
    if not murs and not F.pieces:
        return
    emp_m = unary_union([m.emprise() for m in murs]) if murs else Polygon()
    pu = unary_union([p for _, p in F.pieces]) if F.pieces else Polygon()
    tout = unary_union([emp_m, pu])
    empreinte = unary_union([Polygon(p.exterior) for p in polys_de(tout)])
    brute = empreinte.area / 144
    sp = sum(p.area for _, p in F.pieces) / 144
    am = emp_m.area / 144
    chev = pu.intersection(emp_m).area / 144
    ecart = brute - (sp + am - chev)
    st = "OK" if abs(ecart) <= 1.0 and chev <= 1.0 else "AVERT"
    verif.add("Bilan de surface", st,
              f"[{F.nid}] brute (empreinte) {fr(brute, 1)} pi² ; Σ pièces {fr(sp, 1)} pi² + murs {fr(am, 1)} pi² "
              f"− chevauchement pièces/murs {fr(chev, 1)} pi² = {fr(sp + am - chev, 1)} pi² ; écart {fr(ecart, 1)} pi²")
    trous = empreinte.difference(emp_m).difference(pu) if not empreinte.is_empty else Polygon()
    lst = sorted([t for t in polys_de(trous) if t.area > 144], key=lambda t: (-t.area, t.bounds))
    for t in lst:
        c = t.representative_point()
        b = t.bounds
        verif.add("Bilan de surface", "AVERT",
                  f"[{F.nid}] trou (ni pièce ni mur) de {fr(t.area / 144, 1)} pi² vers x={f3(c.x)}, y={f3(c.y)} po "
                  f"(boîte {f3(b[0])},{f3(b[1])} → {f3(b[2])},{f3(b[3])})")
    if not lst:
        verif.add("Bilan de surface", "OK", f"[{F.nid}] aucun trou > 1 pi² entre pièces et murs")


def controle_chaines(F, verif):
    par = {}
    for c in F.cotes:
        if c["facade"] == "int":
            continue
        par.setdefault(c["facade"], {}).setdefault(c["rang"], []).append(c)
    for fac in ("avant", "arriere", "gauche", "droite"):
        if fac not in par:
            continue
        rangs = par[fac]
        ht = max((c["longueur"] for c in rangs.get(3, [])), default=None)
        for r in sorted(rangs):
            ch = sorted(rangs[r], key=lambda c: c["c1"])
            for a, b in zip(ch[:-1], ch[1:]):
                if abs(b["c1"] - a["c2"]) > 0.5:
                    verif.add("Chaînes de cotes", "AVERT", f"[{F.nid}] façade {fac}, rang {r} : discontinuité entre "
                                                           f"{a['id']} et {b['id']} ({f3(b['c1'] - a['c2'])} po)")
            if r == 3 or ht is None:
                continue
            s = sum(c["longueur"] for c in ch)
            if abs(s - ht) <= 0.5:
                verif.add("Chaînes de cotes", "OK", f"[{F.nid}] façade {fac}, rang {r} : Σ = {pipo(s)} = hors-tout {pipo(ht)}")
            else:
                verif.add("Chaînes de cotes", "AVERT", f"[{F.nid}] façade {fac}, rang {r} : Σ = {pipo(s)} ({f3(s)} po) "
                                                       f"≠ hors-tout {pipo(ht)} ({f3(ht)} po), écart {f3(s - ht)} po")
        if ht is None:
            verif.add("Chaînes de cotes", "INFO", f"[{F.nid}] façade {fac} : aucune cote hors-tout (rang 3)")


def controle_ids(data, verif):
    vus = {}
    def ajoute(i, ou):
        if i is None:
            return
        vus.setdefault(str(i), []).append(ou)
    for n in data.get("niveaux") or []:
        nid = n.get("id")
        ajoute(nid, "niveau")
        for cle in ("murs", "ouvertures", "pieces", "elements", "structure", "cotes", "notes", "lignes_cote"):
            for x in n.get(cle) or []:
                if isinstance(x, dict):
                    ajoute(x.get("id"), f"{nid}/{cle}")
    for e in data.get("ecarts") or []:
        ajoute(e.get("id"), "ecarts")
    dup = {k: v for k, v in vus.items() if len(v) > 1}
    for k in sorted(dup):
        verif.add("Identifiants", "ERREUR", f"id dupliqué « {k} » ({', '.join(dup[k])})")
    if not dup:
        verif.add("Identifiants", "OK", f"{len(vus)} identifiants, aucun doublon")


# ---------------------------------------------------------------------------
# Programme principal
# ---------------------------------------------------------------------------
def numeroter(data, verif):
    ecarts = [e for e in (data.get("ecarts") or []) if isinstance(e, dict)]
    num_ecart = {}
    for i, e in enumerate(ecarts, 1):
        m = re.search(r"(\d+)", str(e.get("id") or ""))
        num_ecart[str(e.get("id"))] = int(m.group(1)) if m else i
    nxt = max(num_ecart.values(), default=0) + 1
    num_presume, num_propre = {}, {}
    for n in data.get("niveaux") or []:
        nid = str(n.get("id"))
        if any(src(m.get("epaisseur")) == "PRÉSUMÉ" or num(m.get("epaisseur")) is None for m in n.get("murs") or []):
            num_presume[nid] = nxt
            nxt += 1
        lcs = n.get("lignes_cote") or []
        for l in lcs:
            if not isinstance(l, dict):
                continue
            if (norm_src(l.get("source")) == "PRÉSUMÉ" or str(l.get("statut")) == "conflit") or \
                    (l.get("repere") and str(l.get("repere")) not in num_ecart):
                if not l.get("repere") or str(l.get("repere")) not in num_ecart:
                    num_propre[str(l.get("id"))] = nxt
                    nxt += 1
    return {"ecarts": ecarts, "num_ecart": num_ecart, "num_presume": num_presume, "num_propre": num_propre}


def main(argv=None):
    ici = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="Génère les plans du relevé de l'existant à partir de maison.json.")
    ap.add_argument("--json", default=None, help="fichier maison.json (défaut : ../donnees/maison.json)")
    ap.add_argument("--sortie", default=None, help="dossier racine des livrables (défaut : ..)")
    args = ap.parse_args(argv)
    chemin_json = os.path.abspath(args.json) if args.json else os.path.normpath(os.path.join(ici, "..", "donnees", "maison.json"))
    sortie = os.path.abspath(args.sortie) if args.sortie else os.path.normpath(os.path.join(ici, ".."))
    if not os.path.isfile(chemin_json):
        print(f"ERREUR : fichier introuvable : {chemin_json}", file=sys.stderr)
        return 2
    brut = open(chemin_json, "rb").read()
    try:
        data = json.loads(brut.decode("utf-8-sig"))
    except Exception as e:
        print(f"ERREUR : JSON invalide ({e})", file=sys.stderr)
        return 2
    projet = data.get("projet") or {}
    verif = Verif()
    controle_ids(data, verif)
    ctx = numeroter(data, verif)

    for sous in ("svg", "pdf", "png", "dxf", "donnees"):
        os.makedirs(os.path.join(sortie, sous), exist_ok=True)

    feuilles = []
    lignes = []
    for i, niv in enumerate(data.get("niveaux") or []):
        if not isinstance(niv, dict):
            continue
        F = construire(niv, i, projet, ctx, verif)
        bilan_surface(F, verif)
        controle_chaines(F, verif)
        lignes += lignes_csv(F, niv, verif)
        feuilles.append((F, niv))

    # repères (registre)
    for n, nid in sorted((v, k) for k, v in ctx["num_presume"].items()):
        verif.add("Repères d'incertitude", "INFO", f"⚠{n} [{nid}] : épaisseurs de murs présumées")
    for lid, n in sorted(ctx["num_propre"].items(), key=lambda kv: kv[1]):
        verif.add("Repères d'incertitude", "INFO", f"⚠{n} : cote {lid} présumée ou en conflit (pas d'écart référencé)")
    for e in ctx["ecarts"]:
        n = ctx["num_ecart"][str(e.get("id"))]
        pos = " (positionné)" if isinstance(e.get("position"), list) else ""
        verif.add("Repères d'incertitude", "INFO", f"⚠{n} = {e.get('id')} [{e.get('niveau')}, impact {e.get('impact')}]{pos} : "
                                                   f"{e.get('description')}")

    # --- écritures
    import cairosvg
    from pypdf import PdfReader, PdfWriter
    produits = []
    pdf_pages = []
    for F, niv in feuilles:
        base = f"{F.feuille}_{F.slug}"
        svg = svg_feuille(F, projet)
        p_svg = os.path.join(sortie, "svg", base + ".svg")
        with open(p_svg, "w", encoding="utf-8", newline="\n") as f:
            f.write(svg)
        p_png = os.path.join(sortie, "png", base + ".png")
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=p_png, dpi=150)
        pdf_pages.append(cairosvg.svg2pdf(bytestring=svg.encode("utf-8")))
        p_dxf = os.path.join(sortie, "dxf", base + ".dxf")
        dxf_feuille(F, p_dxf)
        produits += [p_svg, p_png, p_dxf]
    p_pdf = os.path.join(sortie, "pdf", "plans_existants.pdf")
    w = PdfWriter()
    for b in pdf_pages:
        r = PdfReader(io.BytesIO(b))
        for pg in r.pages:
            w.add_page(pg)
    dt = re.sub(r"\D", "", str(projet.get("date") or ""))[:8] or "20000101"
    w.add_metadata({"/Title": f"Plans de l'existant — {projet.get('nom') or ''}",
                    "/Subject": f"Relevé de l'existant, révision {projet.get('revision') or ''}",
                    "/Producer": "generer_plans.py", "/Creator": "generer_plans.py",
                    "/CreationDate": f"D:{dt}000000", "/ModDate": f"D:{dt}000000"})
    buf = io.BytesIO()
    w.write(buf)
    with open(p_pdf, "wb") as f:
        f.write(buf.getvalue())
    produits.append(p_pdf)

    # CSV
    p_csv = os.path.join(sortie, "donnees", "tableau_pieces.csv")
    s = io.StringIO()
    cw = csv.writer(s, delimiter=";", lineterminator="\r\n")
    cw.writerow(["niveau", "piece_id", "piece", "longueur", "largeur", "superficie_pi2", "superficie_m2", "perimetre",
                 "hauteur_plafond", "surface_murale_brute_pi2", "nb_portes", "nb_fenetres", "fiabilite"])
    for r in lignes:
        cw.writerow(r)
    with open(p_csv, "wb") as f:
        f.write(s.getvalue().encode("utf-8-sig"))
    produits.append(p_csv)

    # Rapport
    p_ver = os.path.join(sortie, "donnees", "verifications.txt")
    rap = rapport(verif, projet, brut, feuilles)
    with open(p_ver, "w", encoding="utf-8", newline="\n") as f:
        f.write(rap)
    produits.append(p_ver)

    # Résumé écran
    print(f"Relevé : {projet.get('nom') or '(sans nom)'} — révision {projet.get('revision') or '?'} ({projet.get('date') or '?'})")
    for F, _ in feuilles:
        print(f"  {F.feuille} {F.nom} : échelle {F.echelle}, {len(F.murs)} murs, {len(F.ouvs)} ouvertures, "
              f"{len(F.pieces)} pièces, {len(F.cotes)} cotes")
    print("Contrôles :")
    for sct in SECTIONS:
        c = verif.compte(sct)
        etat = "ERREUR" if c["ERREUR"] else ("AVERT." if c["AVERT"] else "OK")
        print(f"  {sct:<28} {etat:<7} ({c['ERREUR']} erreur(s), {c['AVERT']} avertissement(s))")
    print("Fichiers :")
    for p in produits:
        print("  " + os.path.relpath(p, sortie))
    print(f"Détails : {os.path.relpath(p_ver, sortie)}")
    return 0


def rapport(verif, projet, brut, feuilles):
    o = []
    o.append("RAPPORT DE VÉRIFICATIONS — GÉNÉRATEUR DE PLANS")
    o.append("=" * 72)
    o.append(f"Projet   : {projet.get('nom') or ''}")
    o.append(f"Révision : {projet.get('revision') or ''}    Date : {projet.get('date') or ''}")
    o.append(f"Données  : maison.json, sha256 {hashlib.sha256(brut).hexdigest()}")
    o.append("Feuilles : " + " ; ".join(f"{F.feuille} {F.nom} ({F.echelle})" for F, _ in feuilles))
    o.append("")
    o.append("SOMMAIRE")
    for s in SECTIONS:
        c = verif.compte(s)
        etat = "ERREUR" if c["ERREUR"] else ("AVERT." if c["AVERT"] else "OK")
        o.append(f"  {s:<28} {etat:<7} {c['ERREUR']} erreur(s), {c['AVERT']} avertissement(s)")
    o.append("")
    for i, s in enumerate(SECTIONS, 1):
        o.append(f"{i}. {s.upper()}")
        o.append("-" * 72)
        if not verif.items[s]:
            o.append("  (rien à signaler)")
        for st, msg in verif.items[s]:
            o.append(f"  [{st}] {msg}")
        o.append("")
    o.append("Légende : [ERREUR] à corriger dans maison.json ; [AVERT] à examiner ; [INFO] information ; [OK] contrôle réussi.")
    return "\n".join(o) + "\n"


if __name__ == "__main__":
    sys.exit(main())
