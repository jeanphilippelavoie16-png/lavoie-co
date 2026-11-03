import json, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Poly, FancyArrowPatch, Rectangle
from shapely.geometry import LineString, box
M = json.load(open("../SS-07_vestiaire_coin_frigo/donnees/maison.json"))
NIV = {n["id"]: n for n in M["niveaux"]}
Z = (120, 196, 330, 392)

def murs(ax, niv, sauf=()):
    for m in niv["murs"]:
        if m["id"] in sauf or m.get("materiau") == "lattes":
            continue
        t = (m.get("epaisseur") or {}).get("valeur") or 4.5
        g = LineString([(m["x1"], m["y1"]), (m["x2"], m["y2"])]).buffer(t / 2, cap_style=3).intersection(box(*Z))
        if g.is_empty:
            continue
        for p in (g.geoms if hasattr(g, "geoms") else [g]):
            if p.geom_type != "Polygon":
                continue
            c = "#3a3a3a" if m["type"] in ("ext", "fondation") else ("#9a9a9a" if m.get("etat") != "nouveau" else "#ffffff")
            ax.add_patch(Poly(list(p.exterior.coords), closed=True, fc=c, ec="#222", lw=0.6))
    for o in niv["ouvertures"]:
        m = next(mm for mm in niv["murs"] if mm["id"] == o["mur_id"])
        L = math.hypot(m["x2"] - m["x1"], m["y2"] - m["y1"]); ux, uy = (m["x2"] - m["x1"]) / L, (m["y2"] - m["y1"]) / L
        c, w = o["position"]["valeur"], o["largeur"]["valeur"]
        a = (m["x1"] + ux * (c - w / 2), m["y1"] + uy * (c - w / 2)); b = (m["x1"] + ux * (c + w / 2), m["y1"] + uy * (c + w / 2))
        if not (Z[0] < (a[0] + b[0]) / 2 < Z[2] and Z[1] < (a[1] + b[1]) / 2 < Z[3]):
            continue
        t = (m.get("epaisseur") or {}).get("valeur") or 4.5
        g = LineString([a, b]).buffer(t / 2 + 0.3, cap_style=2)
        ax.add_patch(Poly(list(g.exterior.coords), closed=True, fc="#dfeef5" if o["type"] == "fenetre" else "white", ec="#555", lw=0.5))

def volee(ax, x0, y0, x1, y1, n, sens, coul="#f3e3c9"):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=coul, ec="#7a5a2a", lw=1))
    for i in range(1, n):
        if sens in "+y-y":
            y = y0 + (y1 - y0) * i / n; ax.plot([x0, x1], [y, y], color="#7a5a2a", lw=0.6)
        else:
            x = x0 + (x1 - x0) * i / n; ax.plot([x, x], [y0, y1], color="#7a5a2a", lw=0.6)

def fleche(ax, pts, txt=None):
    xs, ys = zip(*pts)
    ax.plot(xs[:-1] + (xs[-1],), ys, color="#b0302a", lw=1.4)
    ax.add_patch(FancyArrowPatch(pts[-2], pts[-1], arrowstyle="-|>", mutation_scale=12, color="#b0302a", lw=1.4))

def palier(ax, x0, y0, x1, y1, txt="palier"):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="#e6d2ad", ec="#7a5a2a", lw=1))
    ax.text((x0 + x1) / 2, (y0 + y1) / 2, txt, ha="center", va="center", fontsize=6.5, color="#5a3d14")

def tournantes(ax, x0, y0, x1, y1, px, py, nb=3):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="#f3e3c9", ec="#7a5a2a", lw=1))
    xf, yf = (x0 if abs(px - x1) < .1 else x1), (y0 if abs(py - y1) < .1 else y1)
    hx, vy = math.copysign(1, xf - px), math.copysign(1, yf - py)
    for j in range(1, nb):
        f = math.radians(90 * j / nb); dx, dy = math.cos(f) * hx, math.sin(f) * vy
        t = min(abs((xf - px) / dx), abs((yf - py) / dy)); ax.plot([px, px + dx * t], [py, py + dy * t], color="#7a5a2a", lw=0.6)

def zone(ax, x0, y0, x1, y1, txt, c="#cfe6c9"):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=c, ec="none", alpha=.6))
    ax.text((x0 + x1) / 2, (y0 + y1) / 2, txt, ha="center", va="center", fontsize=6, color="#2d5a27")

from matplotlib.patches import Rectangle as R_
OPTS = {"D1": "D1 — Droit, 3 marches tournantes en haut\n(recommandé)", "D2": "D2 — Tournantes en haut et en bas\n(arrivée dans le passage du caveau)"}
fig, axs = plt.subplots(2, 2, figsize=(11, 10.6))
for col, k in enumerate(("D1", "D2")):
    for row, nid in enumerate(("RDC", "SS")):
        ax = axs[row][col]; niv = NIV[nid]
        ax.set_xlim(Z[0], Z[2]); ax.set_ylim(Z[1], Z[3]); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
        murs(ax, niv, ("mur-SS-P16", "mur-SS-P17", "mur-RDC-P01", "mur-SS-P05"))
        haut = nid == "RDC"
        if not haut:
            ax.add_patch(R_((156, 352), 40, 18, fc="none", ec="#c0392b", hatch="////", lw=1))
            ax.text(176, 345, "fenêtre de la chambre 1\n(on n'y touche pas)", ha="center", va="top", fontsize=6.5, color="#c0392b")
            ax.add_patch(R_((196.5, 250), 4.5, 120, fc="white", ec="#222", lw=.8))       # nouveau mur de la chambre 1
            ax.add_patch(R_((10, 247.75), 191, 4.5, fc="white", ec="#222", lw=.8))
            ax.text(150, 300, "chambre 1\n(+1½ pi)", fontsize=7, color="#555", ha="center")
            ax.text(300, 300, "chambre 2", fontsize=7, color="#555", ha="center"); ax.text(250, 382, "caveau", ha="center", fontsize=7, color="#555")
            ax.add_patch(R_((223, 199), 10, 10, fc="#b98e5e", ec="#5a3d14", lw=.8)); ax.text(236, 200, "colonne", fontsize=6, color="#5a3d14")
            zone(ax, 238.5, 236, 276, 300, "passage\n37½ po")
        else:
            ax.text(285, 300, "salle à manger\n(appartement)", fontsize=7, color="#555", ha="center")
            zone(ax, 177.5, 262, 199, 330, "2 pi\nlibres", c="#f6e7c1")
        if k == "D1":
            volee(ax, 201, 230, 236, 330, 10, "+y"); tournantes(ax, 201, 330, 236, 366, 236, 330)
            pts = [(218.5, 236), (218.5, 345), (242, 350)]
        else:
            tournantes(ax, 201, 230, 236, 266, 236, 266); volee(ax, 201, 266, 236, 334, 7, "+y"); tournantes(ax, 201, 334, 236, 370, 236, 334)
            pts = [(242, 248), (218.5, 252), (218.5, 350), (242, 354)]
        fleche(ax, pts if not haut else pts[::-1])
        ax.set_title(("REZ-DE-CHAUSSÉE — descend" if haut else "SOUS-SOL — monte"), fontsize=9)
    axs[0][col].text(0.5, 1.12, OPTS[k], transform=axs[0][col].transAxes, ha="center", va="bottom", fontsize=11, fontweight="bold")
INFOS = {"D1": "Bande de 35 po entre la fenêtre de la chambre et la porte du caveau\nPied face au hall, à 19'-2\" du devant\nLa colonne est à 21 po devant le pied, à droite\nChambre 1 plus large de 1½ pi, fenêtre entière",
         "D2": "Même bande ; 3 tournantes en bas, sortie vers le passage\nRien devant le pied (la colonne n'est plus dans le chemin)\nDeux séries de marches tournantes : moins confortable\nOn arrive dans le passage du caveau"}
for col, k in enumerate(("D1", "D2")):
    axs[1][col].text(0.5, -0.04, INFOS[k], transform=axs[1][col].transAxes, ha="center", va="top", fontsize=8.6)
fig.suptitle("Escalier — étude 2 : à l'est de la fenêtre de la chambre 1 · 14 contremarches de ≈ 7½ po, girons de 10 po, 35 po de large",
             fontsize=12, y=0.995)
fig.tight_layout(rect=(0, 0.06, 1, 0.95))
fig.savefig("etude_escalier_2.png", dpi=130)
print("ok")
