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

OPTS = {
 "A": dict(titre="A — Droit + 3 marches tournantes en haut\n(SS-07)", ),
 "B": dict(titre="B — En L, palier dans le coin\n(recommandé)"),
 "C": dict(titre="C — En L, 3 marches tournantes dans le coin\n(le plus compact)"),
}
fig, axs = plt.subplots(2, 3, figsize=(15, 10.6))
for col, k in enumerate("ABC"):
    for row, nid in enumerate(("RDC", "SS")):
        ax = axs[row][col]; niv = NIV[nid]
        ax.set_xlim(Z[0], Z[2]); ax.set_ylim(Z[1], Z[3]); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
        sauf = ("mur-SS-P16", "mur-SS-P17", "mur-RDC-P01")
        murs(ax, niv, sauf)
        if nid == "SS":
            ax.text(250, 382, "caveau", ha="center", fontsize=7, color="#555")
            zone(ax, 222, 230, 276, 248, "passage")
            ax.text(150, 300, "chambre 1", fontsize=7, color="#555", ha="center"); ax.text(300, 300, "chambre 2", fontsize=7, color="#555", ha="center")
        else:
            ax.text(285, 300, "salle à manger\n(appartement)", fontsize=7, color="#555", ha="center")
            ax.text(295, 385, "entrée arr.", fontsize=6.5, color="#555", ha="center")
        haut = nid == "RDC"
        if k == "A":
            volee(ax, 182, 230, 218, 330, 10, "+y"); tournantes(ax, 182, 330, 218, 366, 218, 330)
            pts = [(200, 236), (200, 345), (225, 350)] if not haut else [(225, 350), (200, 345), (200, 236)]
            fleche(ax, pts)
            foot, prise = 230, "36 × 136 po"
        elif k == "B":
            volee(ax, 182, 254, 218, 334, 8, "+y"); palier(ax, 182, 334, 218, 370); volee(ax, 218, 334, 258, 370, 4, "+x")
            pts = [(200, 258), (200, 352), (254, 352)] if not haut else [(254, 352), (200, 352), (200, 258)]
            fleche(ax, pts)
        else:
            volee(ax, 182, 260, 218, 330, 7, "+y"); tournantes(ax, 182, 330, 218, 366, 218, 330); volee(ax, 218, 330, 248, 366, 3, "+x")
            pts = [(200, 264), (200, 348), (244, 348)] if not haut else [(244, 348), (200, 348), (200, 264)]
            fleche(ax, pts)
        ax.set_title(("REZ-DE-CHAUSSÉE — " if haut else "SOUS-SOL — ") + ("descend" if haut else "monte"), fontsize=9)
    axs[0][col].text(0.5, 1.13, OPTS[k]["titre"], transform=axs[0][col].transAxes, ha="center", va="bottom", fontsize=11, fontweight="bold")
INFOS = {
 "A": "Pied à 19'-2\" du devant · 36 × 136 po au sous-sol\nEntrée en haut par le côté, au fond\nMarches tournantes en haut (moins sûr)\nRien sous la porte du caveau",
 "B": "Pied à 21'-2\" du devant (+2 pi de hall)\nPalier 36 × 36 dans le coin, sous la fenêtre\nEn haut : on arrive près de l'entrée arrière\nSous la volée du haut : 6'-6\" à 7'-1\" libres → caveau OK (de justesse)",
 "C": "Pied à 21'-8\" du devant (+2½ pi de hall)\nAucun palier : 3 marches tournantes dans le coin\nVolée du haut plus courte (30 po)\nLe plus compact, mais tournant à mi-hauteur",
}
for col, k in enumerate("ABC"):
    axs[1][col].text(0.5, -0.04, INFOS[k], transform=axs[1][col].transAxes, ha="center", va="top", fontsize=8.6)
fig.suptitle("Escalier en coin — étude d'implantation (86, avenue Laurier) · 14 contremarches de ≈ 7½ po, girons de 10 po, 36 po de large",
             fontsize=12, y=0.995)
fig.tight_layout(rect=(0, 0.06, 1, 0.95))
fig.savefig("etude_escalier_en_coin.png", dpi=130)
print("ok")
