"""Esquisse préliminaire : piscine de béton hors terre, spa intégré, fenêtre dans la paroi (croquis du client, 2026-11-24).
Pouces. x le long de la piscine, y vers l'arrière (le spa est devant, y négatif), z depuis le sol. Sort esquisse.png."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

E = 10                       # épaisseur des parois
PL, PW, PH = 260, 140, 54    # piscine hors tout (21'-8" × 11'-8"), 4'-6" de haut
SW, SD, SH = 132, 96, PH     # spa : 11'-0" de large depuis le bout gauche, 8'-0" de saillie, même hauteur que la piscine ; ouvert sur la piscine
FX0, FX1, FZ0, FZ1 = 150, 246, 14, 44      # fenêtre : 8'-0" × 2'-6"
BET, EAU, VIT, SPA = "#c9c7c2", "#4fb3d9", "#9fe3f5", "#3aa0c8"
pp = lambda v: f"{int(v // 12)}'-{int(v % 12)}\""

fig = plt.figure(figsize=(17, 11), facecolor="white")
fig.suptitle("Piscine de béton hors terre, spa intégré et fenêtre — esquisse préliminaire", fontsize=20, fontweight="bold", x=0.03, ha="left")
fig.text(0.03, 0.935, "86, avenue Laurier · 2026-11-24 · dimensions proposées, à valider par un ingénieur en structure et un pisciniste", fontsize=11, color="#444")

# ---- plan
a = fig.add_axes([0.03, 0.42, 0.42, 0.48]); a.set_aspect("equal"); a.axis("off"); a.set_title("VUE DU HAUT", loc="left", fontweight="bold")
a.add_patch(Rectangle((0, 0), PL, PW, fc=BET, ec="k", lw=1.5)); a.add_patch(Rectangle((E, E), PL - 2 * E, PW - 2 * E, fc=EAU, ec="k"))
a.add_patch(Rectangle((0, -SD), SW, SD, fc=BET, ec="k", lw=1.5)); a.add_patch(Rectangle((E, -SD + E), SW - 2 * E, SD, fc=SPA, ec="none"))
a.add_patch(Rectangle((E, -SD + E), SW - 2 * E, 18, fc="#7cc3dd", ec="k", ls="--")); a.add_patch(Rectangle((E, -SD + E), 18, SD - E, fc="#7cc3dd", ec="k", ls="--"))
a.add_patch(Rectangle((SW - E - 18, -SD + E), 18, SD - E, fc="#7cc3dd", ec="k", ls="--"))
a.plot([E, SW - E], [E, E], color="k", ls=":", lw=1.2); a.text(SW / 2, E + 9, "ouvert (seuil sous l'eau)", ha="center", fontsize=8)
a.add_patch(Rectangle((FX0, 0), FX1 - FX0, E, fc=VIT, ec="#0077aa", lw=2))
a.add_patch(Rectangle((PL - E - 60, E), 60, 48, fc="#7cc3dd", ec="k", ls="--"))
a.text(PL / 2 + 20, PW / 2 + 10, f"PISCINE\nintérieur {pp(PL - 2 * E)} × {pp(PW - 2 * E)}\neau 4'-0\"", ha="center", va="center", fontsize=12, fontweight="bold")
a.text(SW / 2, -SD / 2 + 14, f"SPA\n{pp(SW - 2 * E)} × {pp(SD - E)}", ha="center", va="center", fontsize=11, fontweight="bold")
a.text(SW / 2, -SD + E + 9, "banc en U", ha="center", va="center", fontsize=8)
a.text((FX0 + FX1) / 2, -14, f"FENÊTRE {pp(FX1 - FX0)}", ha="center", color="#0077aa", fontweight="bold")
a.text(PL - E - 30, E + 24, "marches\net banc", ha="center", va="center", fontsize=8)
def cote(ax, x0, y0, x1, y1, t, d=0, rot=0):
    ax.annotate("", (x0, y0), (x1, y1), arrowprops=dict(arrowstyle="<->", lw=1))
    ax.text((x0 + x1) / 2 + (d if rot else 0), (y0 + y1) / 2 + (0 if rot else d), t, ha="center", va="center", rotation=rot, fontsize=10, bbox=dict(fc="white", ec="none", pad=1))
cote(a, 0, PW + 16, PL, PW + 16, pp(PL)); cote(a, PL + 16, 0, PL + 16, PW, pp(PW), rot=90)
cote(a, 0, -SD - 12, SW, -SD - 12, pp(SW)); cote(a, -16, -SD, -16, 0, pp(SD), rot=90)
a.set_xlim(-40, PL + 40); a.set_ylim(-SD - 30, PW + 35)

# ---- élévation avant
b = fig.add_axes([0.03, 0.06, 0.42, 0.30]); b.set_aspect("equal"); b.axis("off"); b.set_title("VUE DE FACE (côté du spa)", loc="left", fontweight="bold")
b.add_patch(Rectangle((-30, -6), PL + 60, 6, fc="#7da35a", ec="none")); b.add_patch(Rectangle((0, 0), PL, PH, fc=BET, ec="k", lw=1.5))
b.add_patch(Rectangle((FX0, FZ0), FX1 - FX0, FZ1 - FZ0, fc=VIT, ec="#0077aa", lw=2)); b.add_patch(Rectangle((0, 0), SW, SH, fc="#bdbbb6", ec="k", lw=1.5))
b.plot([0, PL], [PH - 6] * 2, color="#0077aa", ls=":"); b.text(PL + 30, PH - 6, "eau", va="center", fontsize=8, color="#0077aa")
b.text(SW / 2, SH / 2, "SPA", ha="center", va="center", fontweight="bold"); b.text((FX0 + FX1) / 2, (FZ0 + FZ1) / 2, f"acrylique\n{pp(FX1 - FX0)} × {pp(FZ1 - FZ0)}", ha="center", va="center", fontsize=9)
cote(b, PL + 14, 0, PL + 14, PH, pp(PH), rot=90); cote(b, 0, -14, SW, -14, pp(SW))
b.set_xlim(-40, PL + 40); b.set_ylim(-24, PH + 12)

# ---- 3D (projection cavalière dessinée à la main : fond vers le haut à droite ; du fond vers l'avant)
from matplotlib.patches import Polygon
c = fig.add_axes([0.47, 0.33, 0.52, 0.57]); c.set_aspect("equal"); c.axis("off"); c.set_title("3D", loc="left", fontweight="bold")
P = lambda x, y, z: (x + 0.5 * y, z + 0.32 * y)
def face(pts, col, **k):
    c.add_patch(Polygon([P(*p) for p in pts], closed=True, fc=col, ec=k.pop("ec", "k"), lw=k.pop("lw", 1), **k))
def cuve(x0, y0, x1, y1, h, col, eau, prof=6, ouvert=False):
    face([(x1, y0, 0), (x1, y1, 0), (x1, y1, h), (x1, y0, h)], "#a9a7a2")                      # côté droit
    face([(x0, y0, 0), (x1, y0, 0), (x1, y0, h), (x0, y0, h)], col)                           # devant
    face([(x0, y0, h), (x1, y0, h), (x1, y1, h), (x0, y1, h)], "#e2e0da")                     # margelle
    a0, b0, a1, b1 = x0 + E, y0 + E, x1 - E, y1 - E
    face([(a0, b0, h), (a1, b0, h), (a1, b1, h), (a0, b1, h)], "#8f8d88")                     # intérieur (ombre)
    if not ouvert: face([(a0, b1, h), (a1, b1, h), (a1, b1, h - prof), (a0, b1, h - prof)], "#b5b3ae")       # paroi du fond, au-dessus de l'eau
    face([(a0, b0, h), (a0, b1, h), (a0, b1, h - prof), (a0, b0, h - prof)], "#a09e99")       # paroi de gauche
    face([(a0, b0, h - prof), (a1, b0, h - prof), (a1, b1, h - prof), (a0, b1, h - prof)], eau)
c.add_patch(Polygon([P(-70, -150, 0), (P(PL + 110, -150, 0)), P(PL + 110, PW + 60, 0), P(-70, PW + 60, 0)], fc="#b7d39b", ec="none"))
cuve(0, 0, PL, PW, PH, BET, EAU)
face([(FX0, 0, FZ0), (FX1, 0, FZ0), (FX1, 0, FZ1), (FX0, 0, FZ1)], VIT, ec="#0077aa", lw=2.5)
cuve(0, -SD, SW, 2 * E, SH, "#bdbbb6", SPA, ouvert=True)
face([(E + 4, 0, PH - 6), (SW - E, 0, PH - 6), (SW - E, 3 * E, PH - 6), (E + 4, 3 * E, PH - 6)], EAU, ec="none")   # passage ouvert
c.text(*P(PL / 2, PW / 2, PH - 6), "piscine", ha="center", va="center", fontsize=13, fontweight="bold")
c.text(*P(SW / 2, -SD / 2 + E, SH - 6), "spa", ha="center", va="center", fontsize=12, fontweight="bold")
c.text(*P((FX0 + FX1) / 2, 0, (FZ0 + FZ1) / 2), "fenêtre", ha="center", va="center", color="#005f88", fontsize=11)
c.set_xlim(-160, PL + 170); c.set_ylim(-80, PH + 90)

fig.text(0.47, 0.27, "PROPOSITION", fontweight="bold", fontsize=12)
fig.text(0.47, 0.035, "\n".join([
 f"• Piscine : {pp(PL)} × {pp(PW)} hors tout, parois de béton armé de {E} po, {pp(PH)} hors sol, eau de 4'-0\" ; marches et banc dans un coin.",
 f"• Spa : {pp(SW)} × {pp(SD)}, au bout gauche du long côté, MÊME hauteur que la piscine ({pp(PH)}), banc en U avec jets,",
 "   OUVERT sur la piscine (seuil sous l'eau, même plan d'eau) : on passe du spa à la piscine en nageant.",
 f"• Fenêtre : panneau d'acrylique de {pp(FX1 - FX0)} × {pp(FZ1 - FZ0)} dans le long côté, à côté du spa, visible de la cour.",
 "• Fini : béton lisse apparent ou crépi blanc dehors ; margelle de béton de 10 po ; intérieur en enduit ou en tuile.",
 "À VALIDER : structure, gel et hivernage (ingénieur) · épaisseur de l'acrylique (fabricant) · eau commune : le spa est à la",
 "température de la piscine (pas un spa chaud à part) · accès et enceinte selon le règlement sur les piscines · permis de la Ville."]),
 fontsize=9.5, va="bottom", linespacing=1.5)
fig.savefig("esquisse.png", dpi=110)
