"""Étude 3 : où mettre l'escalier, en haut ET en bas — options sur toute la maison."""
import json, math, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Poly, FancyArrowPatch, Rectangle, Circle, Wedge
from shapely.geometry import LineString, Polygon
SORTIE = sys.argv[1] if len(sys.argv) > 1 else "."   # python3 etude_escalier_3.py . ../../../releve/livrables/donnees/maison.json
M = json.load(open(sys.argv[2] if len(sys.argv) > 2 else "/home/user/lavoie-co/releve/livrables/donnees/maison.json"))
NIV = {n["id"]: n for n in M["niveaux"]}
Z = (-8, -56, 464, 444)
BRUN, BOIS, ROUGE = "#7a5a2a", "#f3e3c9", "#b0302a"

def fond(ax, nid):
    niv = NIV[nid]
    for m in niv["murs"]:
        if nid == "SS" and m["type"] not in ("fondation", "ext"):
            continue                                           # sous-sol : seulement la fondation (on refera les cloisons)
        t = (m.get("epaisseur") or {}).get("valeur") or 4.5
        g = LineString([(m["x1"], m["y1"]), (m["x2"], m["y2"])]).buffer(t / 2, cap_style=3)
        ax.add_patch(Poly(list(g.exterior.coords), closed=True, fc="#3a3a3a" if m["type"] in ("ext", "fondation") else "#a8a8a8",
                          ec="#222", lw=0.4))
    for o in niv["ouvertures"]:
        m = next(mm for mm in niv["murs"] if mm["id"] == o["mur_id"])
        if nid == "SS" and m["type"] not in ("fondation", "ext"):
            continue
        L = math.hypot(m["x2"] - m["x1"], m["y2"] - m["y1"]); ux, uy = (m["x2"] - m["x1"]) / L, (m["y2"] - m["y1"]) / L
        c, w = o["position"]["valeur"], o["largeur"]["valeur"]
        a = (m["x1"] + ux * (c - w / 2), m["y1"] + uy * (c - w / 2)); b = (m["x1"] + ux * (c + w / 2), m["y1"] + uy * (c + w / 2))
        t = (m.get("epaisseur") or {}).get("valeur") or 4.5
        g = LineString([a, b]).buffer(t / 2 + 0.3, cap_style=2)
        ax.add_patch(Poly(list(g.exterior.coords), closed=True, fc="#bfe0f0" if o["type"] == "fenetre" else "white", ec="#555", lw=0.4))
    for s in niv["structure"]:
        g = s.get("geometrie") or {}
        if s["type"] == "colonne":
            ax.add_patch(Rectangle((g["x"] - 5, g["y"] - 5), 10, 10, fc="#b98e5e", ec="#5a3d14", lw=0.5))
        elif s["type"] == "poutre" and "x1" in g:
            ax.plot([g["x1"], g["x2"]], [g["y1"], g["y2"]], color="#5a3d14", lw=0.8, ls=(0, (6, 3)))
    if nid == "RDC":
        for p in niv["pieces"]:
            P = Polygon(p["polygone"]); c = P.representative_point()
            if P.area / 144 > 12:
                ax.text(c.x, c.y, p["nom"].replace("Salle à manger", "S. à manger").replace("Dégagement", "Dégag."), fontsize=5.2,
                        ha="center", va="center", color="#666")
    else:
        for x, y, t in ((60, 80, "lavage"), (170, 80, "gym"), (340, 80, "séjour"), (273, 410, "caveau"), (60, 300, "ch. 1"), (380, 300, "ch. 2")):
            ax.text(x, y, t, fontsize=5.2, ha="center", va="center", color="#999")
        ax.text(462, 175, "porte", fontsize=4.5, color="#555", rotation=90, va="center")

def volee(ax, x0, y0, x1, y1, n, axe):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=BOIS, ec=BRUN, lw=0.8))
    for i in range(1, n):
        if axe == "y":
            y = y0 + (y1 - y0) * i / n; ax.plot([x0, x1], [y, y], color=BRUN, lw=0.4)
        else:
            x = x0 + (x1 - x0) * i / n; ax.plot([x, x], [y0, y1], color=BRUN, lw=0.4)

def tournantes(ax, x0, y0, x1, y1, px, py, nb=3):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=BOIS, ec=BRUN, lw=0.8))
    xf, yf = (x0 if abs(px - x1) < .1 else x1), (y0 if abs(py - y1) < .1 else y1)
    hx, vy = math.copysign(1, xf - px), math.copysign(1, yf - py)
    for j in range(1, nb):
        f = math.radians(90 * j / nb); dx, dy = math.cos(f) * hx, math.sin(f) * vy
        t = min(abs((xf - px) / dx), abs((yf - py) / dy)); ax.plot([px, px + dx * t], [py, py + dy * t], color=BRUN, lw=0.4)

def palier(ax, x0, y0, x1, y1):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="#e6d2ad", ec=BRUN, lw=0.8))

def colimacon(ax, cx, cy, r=30, n=13):
    ax.add_patch(Circle((cx, cy), r, fc=BOIS, ec=BRUN, lw=0.8)); ax.add_patch(Circle((cx, cy), 3, fc=BRUN))
    for i in range(n):
        a = 2 * math.pi * i / 15; ax.plot([cx, cx + r * math.cos(a)], [cy, cy + r * math.sin(a)], color=BRUN, lw=0.4)

def fleche(ax, pts):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=ROUGE, lw=1.1)
    ax.add_patch(FancyArrowPatch(pts[-2], pts[-1], arrowstyle="-|>", mutation_scale=8, color=ROUGE, lw=1.1))

def note(ax, x, y, t, c=ROUGE):
    ax.text(x, y, t, fontsize=5.4, color=c, ha="center", va="center", bbox=dict(fc="white", ec=c, lw=0.4, pad=1.2))

def ouvrir(ax, x0, y0, x1, y1):            # cloison existante à enlever / ouvrir (rez-de-chaussée)
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="none", ec=ROUGE, lw=0.8, ls="--"))

# ------------------------------------------------------------------ options (coordonnées en pouces, repère de la maison)
OPTIONS = []
def opt(code, titre, dessin_rdc, dessin_ss, pour, contre, note_cout):
    OPTIONS.append(dict(code=code, titre=titre, rdc=dessin_rdc, ss=dessin_ss, pour=pour, contre=contre, cout=note_cout))

def o1(ax, haut):
    volee(ax, 277, 205, 314, 335, 13, "y"); palier(ax, 277, 335, 314, 370) if haut else None
    fleche(ax, [(295.5, 352), (295.5, 212)] if haut else [(295.5, 212), (295.5, 330)])
    if haut: note(ax, 240, 352, "on entre\nau fond")
    else: note(ax, 295, 180, "pied face\nau hall")
opt("1", "1 — À l'emplacement de 1957",
    lambda ax: o1(ax, True), lambda ax: o1(ax, False),
    "trémie d'origine (solives déjà coupées une fois) ; pied au centre du sous-sol ; volée droite, pas de tournantes",
    "en haut : bande de 3 pi entre la salle à manger et la cuisine ; en bas : chambre 2 réduite (comme SS-04)",
    "faible")

def o2(ax, haut):
    volee(ax, 234, 50, 270, 150, 10, "y"); tournantes(ax, 234, 14, 270, 50, 234, 50)
    fleche(ax, [(225, 32), (252, 34), (252, 143)] if haut else [(252, 143), (252, 34), (225, 32)])
    if haut:
        ouvrir(ax, 219, 8, 234, 95); note(ax, 300, 105, "cloison de l'entrée\nouverte")
    else:
        note(ax, 252, 185, "pied dans le hall\n(entre les poutres)")
opt("2", "2 — À l'entrée avant (escalier commun)",
    lambda ax: o2(ax, True), lambda ax: o2(ax, False),
    "en haut : on descend directement de l'entrée avant (entrée commune aux deux logements) ; en bas : arrivée au hall central ; rien devant une fenêtre",
    "le salon du haut perd une bande de 3 pi le long de l'entrée ; 3 tournantes en haut ; mur télé du séjour du bas à déplacer",
    "moyen")

def o3(ax, haut):
    volee(ax, 240, 162.5, 370, 198.5, 13, "x"); palier(ax, 204, 162.5, 240, 198.5) if haut else None
    fleche(ax, [(222, 180), (365, 180)] if haut else [(365, 180), (245, 180)])
    if haut: note(ax, 365, 230, "coin de la cuisine\npris (≈ 4½ × 3 pi)")
    else: note(ax, 400, 225, "pied face à la\nporte d'entrée du bas")
opt("3", "3 — Au centre, entre les deux poutres",
    lambda ax: o3(ax, True), lambda ax: o3(ax, False),
    "les deux poutres forment les côtés de la trémie (structure simple) ; escalier ouvert au centre, très « design » ; en bas on arrive à la porte d'entrée",
    "en haut : coupe le dégagement et le coin avant de la cuisine ; en bas : coupe le lien hall–vestiaire (on passe à chaque bout)",
    "moyen")

def o4(ax, haut):
    volee(ax, 265, 394, 315, 430, 5, "x"); tournantes(ax, 229, 394, 265, 430, 265, 394); volee(ax, 229, 344, 265, 394, 5, "y")
    fleche(ax, [(310, 412), (247, 412), (247, 350)] if haut else [(247, 350), (247, 412), (310, 412)])
    if haut: note(ax, 330, 330, "aucune pièce\ndu haut touchée")
    else: note(ax, 330, 330, "caveau = cage\nd'escalier")
opt("4", "4 — Par l'entrée arrière et le caveau",
    lambda ax: o4(ax, True), lambda ax: o4(ax, False),
    "aucune pièce habitable perdue en haut ni en bas ; on descend depuis l'entrée arrière ; le caveau devient la cage d'escalier",
    "gros travaux : ouverture dans la fondation arrière, plancher de l'entrée arrière à refaire, hauteur à vérifier ; on perd le rangement du caveau",
    "élevé")

def o5(ax, haut):
    colimacon(ax, 250, 288)
    note(ax, 250, 240, "colimaçon Ø 5 pi")
    if not haut: note(ax, 330, 355, "passage libre\nvers le caveau", c="#2d5a27")
opt("5", "5 — Colimaçon (5 pi) au fond de la salle à manger",
    lambda ax: o5(ax, True), lambda ax: o5(ax, False),
    "très peu de place (≈ 25 pi² par étage) ; original et « fun » ; en bas il tombe dans le passage du caveau",
    "moins pratique (meubles, sécurité des enfants) ; souvent refusé comme escalier principal par le code : à vérifier avec la Ville",
    "moyen")

def o6(ax, haut):
    volee(ax, 330, 209.5, 366, 334.5, 13, "y"); palier(ax, 330, 334.5, 366, 370) if haut else None
    fleche(ax, [(348, 352), (348, 216)] if haut else [(348, 216), (348, 330)])
    if haut: note(ax, 380, 290, "côté cuisine")
    else: note(ax, 395, 245, "chambre 2\nà revoir")
opt("6", "6 — Côté cuisine, juste à l'est de la colonne de droite",
    lambda ax: o6(ax, True), lambda ax: o6(ax, False),
    "dans l'axe des colonnes (x 27'-0\") : pied entre les deux poutres, devant le vestiaire ; volée droite avec palier en haut",
    "en haut : bande de 3 pi prise dans la cuisine ; en bas : la chambre 2 devient plus étroite (≈ 6'-6\")",
    "moyen")

def figure(liste, nom):
    fig, axs = plt.subplots(2, len(liste), figsize=(5.4 * len(liste), 11.2))
    for col, o in enumerate(liste):
        for row, nid in enumerate(("RDC", "SS")):
            ax = axs[row][col]; ax.set_xlim(Z[0], Z[2]); ax.set_ylim(Z[1], Z[3]); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values(): s.set_visible(False)
            fond(ax, nid)
            (o["rdc"] if nid == "RDC" else o["ss"])(ax)
            ax.set_title("REZ-DE-CHAUSSÉE (descend)" if nid == "RDC" else "SOUS-SOL (monte)", fontsize=8.5, color="#444")
        axs[0][col].text(0.5, 1.09, o["titre"], transform=axs[0][col].transAxes, ha="center", fontsize=11, fontweight="bold")
        import textwrap
        txt = "\n".join(textwrap.fill(t, 62) for t in ("Pour : " + o["pour"], "Contre : " + o["contre"], "Coût relatif : " + o["cout"]))
        axs[1][col].text(0.02, -0.03, txt.replace("$", ""), transform=axs[1][col].transAxes, ha="left", va="top", fontsize=7.6, linespacing=1.35)
    for ax in axs.flat:
        ax.text(228, -48, "façade avant (rue)", fontsize=5.5, ha="center", color="#777")
    fig.suptitle("Escalier — étude 3 : ailleurs en haut et en bas · 14 contremarches ≈ 7½ po, girons 10 po, 36 po de large",
                 fontsize=12.5, y=0.995)
    fig.tight_layout(rect=(0, 0.13, 1, 0.965))
    fig.savefig(f"{SORTIE}/{nom}", dpi=120)

figure(OPTIONS[:3], "etude_escalier_3a.png")
figure(OPTIONS[3:], "etude_escalier_3b.png")
print("ok")
