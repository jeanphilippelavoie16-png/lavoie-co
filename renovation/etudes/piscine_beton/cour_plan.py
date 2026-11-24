"""Implantation préliminaire de la piscine de béton (20' × 20', spa ouvert, patio et bar) dans la cour arrière du 86, avenue
Laurier. Repère de la maison (pouces) : x le long de la façade, y vers l'arrière (mur arrière à y = 380). Lignes de lot et
bâtiments : renovation/MAISON-18_deux_etages/exterieur.py (plan DAG sur le certificat de localisation). Sort cour_plan.png.
Règles (Ville de Baie-Comeau, fiche « Réglementation | Piscine hors terre », lue le 2026-11-24) : piscine à 1 m au moins du
bâtiment principal, des lignes de lot et d'un bâtiment accessoire ; appareils à 1 m au moins de la piscine et des lignes ;
enceinte de 1,2 m avec porte à fermeture et verrouillage automatiques ; remise à 90 cm des lignes et 2 m de la maison."""
import math
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

M1 = 39.37                                    # 1 m en pouces
X0, YF = 55, 486                              # coin avant gauche de l'ensemble (devant du spa et du patio, vers la maison)
SW, SD, PL, PW = 132, 96, 260, 260
YP = YF + SD                                  # mur avant de la piscine (celui de la fenêtre)
PISC = (X0, YP, X0 + PL, YP + PW); SPA = (X0, YF, X0 + SW, YP); PATIO = (X0 + SW, YF, X0 + PL, YP)
GAR = (356, 621, 512, 825); GAR_TOIT = (344, 609, 524, 837)
APP = (-27, 398, 9, 440)                      # dalle des appareils (filtre, thermopompe) 3' × 3'-6"
LG = lambda y: -75.5 + (32.1 / 523.3) * (y - 380)            # ligne de lot gauche (oblique)
RA, RB = (560.0, 871.0), (-43.0, 903.0)                        # ligne arrière
def d_arr(x, y):
    (ax, ay), (bx, by) = RA, RB; L = math.hypot(bx - ax, by - ay); return abs((bx - ax) * (ay - y) - (ax - x) * (by - ay)) / L
def d_gau(x, y):
    k = 32.1 / 523.3; return (x - LG(y)) / math.sqrt(1 + k * k)
m = lambda po: f"{po * 0.0254:.2f} m".replace(".", ",")
pp = lambda v: f"{int(round(v) // 12)}'-{int(round(v) % 12)}\""
CONTROLES = [
    ("Piscine – ligne de lot gauche", d_gau(PISC[0], PISC[3]), M1), ("Piscine – ligne de lot arrière", d_arr(PISC[2], PISC[3]), M1),
    ("Piscine – cabanon (mur)", GAR[0] - PISC[2], M1), ("Spa – maison (entrée arrière)", YF - 440, M1), ("Piscine – ligne de lot droite", 560 - PISC[2], M1),
    ("Appareils – piscine", math.hypot(SPA[0] - APP[2], SPA[1] - APP[3]), M1), ("Appareils – ligne de lot gauche", d_gau(APP[0], APP[1]), M1),
    ("Cabanon (toit) – ligne droite", 560 - GAR_TOIT[2], 35.43), ("Cabanon (toit) – ligne arrière", d_arr(GAR_TOIT[2], GAR_TOIT[3]), 35.43),
    ("Cabanon – maison", GAR[1] - 380, 78.74), ("Paroi de la piscine hors sol", 54, 47.24),
]
if __name__ == "__main__":
    fig = plt.figure(figsize=(17, 11), facecolor="white")
    fig.suptitle("Cour arrière — implantation de la piscine de béton (préliminaire)", fontsize=20, fontweight="bold", x=0.03, ha="left")
    fig.text(0.03, 0.935, "86, avenue Laurier · 2026-11-24 · lignes de lot du plan DAG (certificat de localisation) · à valider avec la Ville, un arpenteur et un ingénieur", fontsize=11, color="#444")
    a = fig.add_axes([0.02, 0.03, 0.62, 0.88]); a.set_aspect("equal"); a.axis("off")
    a.add_patch(Polygon([(LG(300), 300), (LG(903), 903), RA, (560, 300)], fc="#cfe3b8", ec="none"))
    a.add_patch(Rectangle((457, 300), 103, 222, fc="#8d8f92", ec="none")); a.text(508, 400, "ALLÉE\n(45 po plus bas)", ha="center", va="center", color="white", fontsize=9)
    a.add_patch(Rectangle((445, 380), 12, 168, fc="#b9b6ae", ec="k", lw=.6)); a.add_patch(Rectangle((457, 510), 44, 43, fc="#d9d4c7", ec="k", lw=.6)); a.text(479, 531, "marches", ha="center", va="center", fontsize=7)
    a.add_patch(Rectangle((0, 300), 456, 80, fc="#e9e6df", ec="k", lw=1.5)); a.text(228, 335, "MAISON", ha="center", va="center", fontsize=14, fontweight="bold")
    a.add_patch(Rectangle((219, 380), 108, 60, fc="#e9e6df", ec="k", lw=1.5)); a.text(273, 410, "entrée\narrière", ha="center", va="center", fontsize=8)
    a.add_patch(Rectangle((318, 442), 127, 164, fc="#b9b7b2", ec="k", lw=.6)); a.add_patch(Rectangle((445, 554), 111, 52, fc="#b9b7b2", ec="k", lw=.6))
    a.add_patch(Rectangle((327, 380), 45, 60, fc="#d6d3cc", ec="k")); a.add_patch(Rectangle((372, 380), 70, 60, fc="#d6d3cc", ec="k", hatch="|||")); a.text(385, 410, "marches (7)", ha="center", va="center", fontsize=8, bbox=dict(fc="white", ec="none", pad=1))
    a.add_patch(Rectangle((354, 446), 91, 164, fc="none", ec="k", ls=":", lw=1.2)); a.text(400, 615, "pergola", ha="center", fontsize=7)
    a.add_patch(Rectangle((420, 454), 23, 68, fc="#333", ec="k")); a.add_patch(Rectangle((407, 452), 13, 72, fc="#8a5a2e", ec="k")); a.text(431, 488, "BAR", rotation=90, color="white", ha="center", va="center", fontsize=8, fontweight="bold")
    for yy in (465, 488, 511): a.add_patch(plt.Circle((398, yy), 6, fc="#8a5a2e", ec="k"))
    a.add_patch(Rectangle((350, 572), 84, 32, fc="#e7e2d6", ec="k")); a.add_patch(Rectangle((350, 504), 32, 60, fc="#e7e2d6", ec="k")); a.add_patch(plt.Circle((404, 545), 16, fc="#ffb066", ec="k")); a.text(404, 545, "foyer", ha="center", va="center", fontsize=7)
    for yy in (536, 558): a.add_patch(plt.Circle((436, yy), 8, fc="#e7e2d6", ec="k"))
    a.text(336, 478, "TERRASSE\nLOUNGE", fontsize=7, fontweight="bold", ha="center")
    a.plot([LG(300), LG(903), RA[0], 560], [300, 903, RA[1], 300], color="#b02a2a", lw=1.6, ls="-."); a.text(300, 897, "ligne de lot arrière", color="#b02a2a", fontsize=9, ha="center")
    a.text(LG(650) - 8, 650, "ligne de lot", color="#b02a2a", fontsize=9, rotation=86, ha="right", va="center"); a.text(568, 700, "ligne de lot", color="#b02a2a", fontsize=9, rotation=90, va="center")
    a.plot([LG(372) + 4, LG(899) + 4, 556, 556, 501], [372, 899, 867, 553, 553], color="#7a5230", lw=2.5); a.text(120, 880, "clôture de 6 pi (existante au projet)", color="#7a5230", fontsize=8, ha="center")
    # cabanon
    a.add_patch(Rectangle(GAR_TOIT[:2], GAR_TOIT[2] - GAR_TOIT[0], GAR_TOIT[3] - GAR_TOIT[1], fc="none", ec="k", ls="--", lw=.8))
    a.add_patch(Rectangle(GAR[:2], GAR[2] - GAR[0], GAR[3] - GAR[1], fc="#f4f2ec", ec="k", lw=1.5)); a.text(434, 723, "CABANON\n13' × 17'\n(inchangé)", ha="center", va="center", fontsize=10, fontweight="bold")
    a.plot([386, 482], [621, 621], color="k", lw=4)
    # piscine, spa, patio
    BET, EAU, SPAC, BOIS = "#c9c7c2", "#4fb3d9", "#3aa0c8", "#c79a66"
    for (x0, y0, x1, y1), c in ((PISC, EAU), (SPA, SPAC)):
        a.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=BET, ec="k", lw=1.5))
    a.add_patch(Rectangle((PISC[0] + 10, PISC[1] + 10), PL - 20, PW - 20, fc=EAU, ec="k", lw=.6)); a.add_patch(Rectangle((SPA[0] + 10, SPA[1] + 10), SW - 20, SD, fc=SPAC, ec="none"))
    a.add_patch(Rectangle(PATIO[:2], PATIO[2] - PATIO[0], SD, fc=BOIS, ec="k", hatch="---"))
    a.add_patch(Rectangle((PATIO[0] - 2, YF + 8), 16, SD - 16, fc="#8a5a2e", ec="k")); a.plot([X0 + 150, X0 + 246], [YP + 5, YP + 5], color="#0077aa", lw=5)
    for xx in (X0 + 178, X0 + 216): a.add_patch(Rectangle((xx, YF + 14), 25, 55, fc="white", ec="k"))
    a.text(X0 + PL / 2, YP + PW / 2, "PISCINE\n20' × 20' d'eau\n4'-6\" hors sol", ha="center", va="center", fontsize=13, fontweight="bold"); a.text(X0 + SW / 2, YF + SD / 2 + 6, "SPA\nouvert", ha="center", va="center", fontsize=10, fontweight="bold")
    a.text(X0 + 196, YP + 16, "fenêtre", ha="center", fontsize=8, color="#004d6e"); a.text(X0 + PL - 30, YF + 4, "PATIO", fontsize=8, fontweight="bold", ha="center", va="bottom")
    # enceinte du patio : garde-corps de verre de 1,2 m et portillon
    a.plot([PATIO[0], PATIO[2], PATIO[2]], [YF, YF, YP], color="#00a0c8", lw=3); a.plot([PATIO[2], PATIO[2]], [YF + 20, YF + 56], color="#e2a93f", lw=5)
    a.annotate("garde-corps de verre 1,2 m\net portillon à fermeture auto", (PATIO[2], YF + 38), (PATIO[2] - 150, YF - 30), fontsize=8, arrowprops=dict(arrowstyle="->"), color="#005f88")
    a.add_patch(Rectangle((PATIO[2], YF + 14), 24, 48, fc="#d8b98f", ec="k", hatch="|||")); 
    a.add_patch(Rectangle(APP[:2], APP[2] - APP[0], APP[3] - APP[1], fc="#9aa0a6", ec="k")); a.annotate("appareils\n(filtre, thermopompe)", (APP[0] + 18, APP[3]), (APP[0] - 10, APP[3] + 40), fontsize=8, arrowprops=dict(arrowstyle="->"))
    def cote(x0, y0, x1, y1, t, dx=0, dy=0):
        a.annotate("", (x0, y0), (x1, y1), arrowprops=dict(arrowstyle="<->", lw=1.1, color="#b02a2a"))
        a.text((x0 + x1) / 2 + dx, (y0 + y1) / 2 + dy, t, ha="center", va="center", fontsize=8.5, color="#b02a2a", bbox=dict(fc="white", ec="none", pad=1))
    yb = PISC[3] - 30; cote(LG(yb), yb, PISC[0], yb, m(d_gau(PISC[0], yb))); cote(PISC[2] - 20, PISC[3], PISC[2] - 20, PISC[3] + d_arr(PISC[2] - 20, PISC[3]), m(d_arr(PISC[2], PISC[3])), dx=-32)
    cote(PISC[2], 700, GAR[0], 700, m(GAR[0] - PISC[2]), dy=14); cote(273, 440, 273, YF, m(YF - 440), dx=34); cote(120, 380, 120, YF, pp(YF - 380), dx=30)
    cote(GAR_TOIT[2], 650, 560, 650, m(560 - GAR_TOIT[2]), dy=14)
    a.set_xlim(-110, 600); a.set_ylim(290, 925)
    fig.text(0.66, 0.86, "CE QUI CHANGE", fontweight="bold", fontsize=12)
    fig.text(0.66, 0.845, "\n".join([
        "• La piscine ronde de 21 pi, le patio et le deck de DAG sont remplacés",
        "  par la piscine de béton de 20' × 20' avec son spa, son patio et son bar.",
        "• L'ensemble est tourné vers la maison : la fenêtre, le patio et le bar",
        "  font face à la porte arrière.",
        "• Plus de balcon à la porte arrière : des marches larges descendent le",
        "  long de la maison vers une terrasse lounge (bar, foyer, pergola).",
        "• Le cabanon de 13' × 17' ne bouge pas ; la clôture de 6 pi non plus.",
        "• Les appareils vont près du coin arrière gauche de la maison.",
        "• Le patio (14 po) et le bar rendent la piscine facile à grimper : un",
        "  garde-corps de verre de 1,2 m avec portillon ferme le patio."]), fontsize=10, va="top", linespacing=1.5)
    fig.text(0.66, 0.60, "CONTRÔLE DES RÈGLES (Ville de Baie-Comeau)", fontweight="bold", fontsize=12)
    y = 0.57
    for nom, v, mini in CONTROLES:
        ok = v >= mini - 0.01
        fig.text(0.66, y, ("✓ " if ok else "✗ ") + nom, fontsize=10, color="#1b6e2d" if ok else "#b02a2a"); fig.text(0.985, y, f"{m(v)}  (min. {m(mini)})", fontsize=10, ha="right", family="DejaVu Sans Mono"); y -= 0.027
    fig.text(0.66, y - 0.01, "\n".join([
        "Règles lues sur la fiche de la Ville : 1 m de la maison, des lignes et d'un",
        "bâtiment accessoire ; appareils à 1 m ; enceinte de 1,2 m. La fiche ne",
        "dit rien sur les spas, la superficie maximale ni les terrasses : à",
        "demander au Service de l'urbanisme avec la demande de permis.",
        "Les lignes de lot viennent du plan DAG : marges à faire piqueter.",
        "L'allée est 45 po plus bas que la cour (mur de soutènement existant)."]), fontsize=9, va="top", color="#444", linespacing=1.5)
    fig.savefig("cour_plan.png", dpi=110)
    for c in CONTROLES: print(("OK " if c[1] >= c[2] - .01 else "NON"), c[0], round(c[1], 1), ">=", round(c[2], 1))
