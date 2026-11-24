"""SS-17 — zone « escalier » : le banc-cabane cinéma sous l'escalier flottant.

Spec : ss17_conception/final_escalier/final_escalier.json (+ plan et élévation « banc-cabane cinéma »).
Demande : « En dessous des marches, je pense à quelque chose… je veux pas que ça bloque toute la vue. »
On n'occupe que la bande basse du dessous de l'escalier (x 229¾ → 270¼, entre le verre du gym à x = 228 et la rampe à
x = 271) : un banc de chêne bas et ajouré qui flotte sur un socle d'acier noir en retrait (ruban DEL dessous), 6 cases
traversantes (1 à livres + 5 à 2 bacs de feutre = 10 bacs), assise et traversin en cuir cognac, présentoir à livres de
face, plateau-télécommandes avec USB-C, sabot technique et chasse au pied de l'escalier ; sous les marches tournantes,
un coin-cabane au sol (matelas de laine, 2 rebords à livres au mur avant, garde-pieds devant le verre) éclairé par une
« lune » de 12 po vissée sous la marche T1. RIEN DE PLEIN AU-DESSUS DE 26 PO (sauf la lune, collée sous T1) : la vue du
séjour vers le gym reste ouverte.

L'escalier et la rampe (base SS-16) ne sont pas touchés ; rien n'est fixé au verre du gym (autre lot).
Pouces, repère de la maison (x le long de la façade, y vers l'arrière, z vers le haut).
"""

# ------------------------------------------------------------------------------------------------ repères de la zone
X0, X1 = 229.75, 270.25            # banc : ¾ po du verre (faces 227-229) ; ¾ po de la rampe (barreaux 270⅝-271⅜)
YB0, YB1 = 52.5, 128.25            # banc (75¾ po), après le poteau du pivot (234, 50 ; y 48½-51½)
# montants de ¾ po ; cases : L (livres), 1-3 « jouets », 4-5 « cinéma »
MONTANTS = [(52.5, 53.25), (62.5, 63.25), (75.5, 76.25), (88.5, 89.25), (101.5, 102.25), (114.5, 115.25), (127.5, 128.25)]
CASES = [(a[1], b[0]) for a, b in zip(MONTANTS, MONTANTS[1:])]        # L, 1, 2, 3, 4, 5
ZI0, ZI1 = 4.75, 14.25             # intérieur des cases (9½ po)
LUNE = (262.4, 42.4, 6.0)          # centre et rayon : inscrite dans la marche tournante T1 (dessous à 80½ po)
ZONE = (228.5, 10.0, 270.5, 149.5)  # emprise du dessous de l'escalier (sans la rampe x ≥ 270⅝ ni le verre)

# --------------------------------------------------------------------------------------------------------- plan
EQUIPEMENTS = [  # id, type, nom, libellé, x, y, rotation, (longueur en x, largeur en y)
    ("elem-SS-P-BANCCAB", "autre",
     "Banc-cabane cinéma sous l'escalier : chêne ajouré sur socle d'acier en retrait (DEL), 6 cases (livres + 10 bacs de feutre), "
     "assise cuir cognac à 18½ po, présentoir à livres, plateau-télécommandes USB-C ; rien de plein au-dessus de 26 po",
     "", 250.0, 90.375, 0, (40.5, 75.75)),
    ("elem-SS-P-SABOT", "comptoir", "Sabot technique (24 V, USB, détecteur de veilleuse) et chasse du pied de l'escalier (chêne, ≤ 11 po)",
     "", 250.0, 138.375, 0, (40.5, 20.25)),
    ("elem-SS-P-CABANE", "autre", "Coin-cabane : matelas de laine 32 × 32 × 4 po sous les marches tournantes, coussins",
     "", 253.0, 31.0, 0, (32, 32)),
    ("elem-SS-P-LUNE", "trappe", "« Lune » lumineuse Ø 12 po vissée sous la marche tournante T1 (DEL 24 V gradable)",
     "", LUNE[0], LUNE[1], 0, (12, 12)),
    ("elem-SS-P-REBLIV", "comptoir", "Deux rebords à livres bas de chêne (z 5-8 et 20-23) sur le mur avant", "", 253.0, 11.875, 0, (30, 3.75)),
]


def appliquer_modifs(L, base):
    ids = {e[0] for e in EQUIPEMENTS}
    L["EQUIPEMENTS"][:] = [e for e in L["EQUIPEMENTS"] if e[0] not in ids] + EQUIPEMENTS


def apres_modifs(maison, base):
    ss = next(n for n in maison["niveaux"] if n["id"] == "SS")
    for n in ss.get("notes", []):
        t = n.get("interpretation") or ""
        if "dessous de l'escalier dégagé" in t:
            n["interpretation"] = t.replace("dessous de l'escalier dégagé", "banc-cabane bas sous l'escalier (≤ 26 po)")
    for p in ss.get("pieces", []):
        if p["id"] == "piece-SS-ESC":
            p["description"] = ("Escalier flottant ; dessous : banc-cabane cinéma bas et ajouré (rien de plein au-dessus de 26 po), "
                                "coin-cabane sous les marches tournantes — proposition SS-17 (esquisse)")


# --------------------------------------------------------------------------------------------------------- 3D
def _dans_zone(o):
    """Objet SS-16 posé entièrement sous l'escalier (boîtes : emprise ; formes centrées : position)."""
    x0, y0, x1, y1 = ZONE
    if "x0" in o and "y0" in o:
        return x0 <= o["x0"] and o["x1"] <= x1 and y0 <= o["y0"] and o["y1"] <= y1
    if "x" in o and "y" in o and "pts" not in o:
        return x0 <= o["x"] <= x1 and y0 <= o["y"] <= y1
    return False


def _banc(h):
    B, A, CY = h.B, h.A, h.CY
    out = []
    # socle d'acier noir mat en retrait de 3 po (ombre au sol), pattes réglables, 4 équerres cachées dans la dalle
    out += [A(232.75, 55.5, 267.25, 125.25, 0, 3.5, "metal", r=0.4, b=0.2)]
    # ruban DEL 2700 K sous le débord du caisson, devant le socle (lueur au sol côté séjour, veilleuse sur détecteur)
    out += [B(267.45, 56, 267.85, 125, 3.15, 3.5, "spot"), B(232.15, 56, 232.55, 125, 3.15, 3.5, "spot")]
    # caisson ajouré de chêne blanc : fond, dessus, montants de ¾ po, arrêt bas côté verre (cases ouvertes côté séjour)
    out += [A(X0, YB0, X1, YB1, 3.5, ZI0, "placage", r=0.5, b=0.25), A(X0, YB0, X1, YB1, ZI1, 16, "placage", r=0.5, b=0.4)]
    out += [B(X0, a, X1, b, ZI0, ZI1, "placage") for a, b in MONTANTS]
    out += [B(X0, YB0 + 0.75, X0 + 0.75, YB1 - 0.75, ZI0, 7.5, "placage")]
    # case L : livres debout, dos vers le séjour (devant) et réserve (derrière)
    livres = ["laque-marine", "art-argile", "cuir", "draps", "art-sable", "rouge-velo", "carbone", "blanc", "art-argile", "laque-marine"]
    ya, yb = CASES[0]
    y = ya + 0.3
    k = 0
    while y < yb - 0.9:
        ep = 0.55 + (k * 3 % 4) * 0.15
        hz = 7.6 + (k * 5 % 4) * 0.45
        out.append(A(259.5, y, 269.4, y + ep, ZI0, ZI0 + hz, livres[k % len(livres)], r=0.15, b=0.1))
        if k % 2 == 0:
            out.append(A(232, y, 241.5, y + ep, ZI0, ZI0 + hz - 0.6, livres[(k + 3) % len(livres)], r=0.15, b=0.1))
        y += ep + 0.12
        k += 1
    # 10 bacs de feutre de laine (2 par case) : bac « enfant » devant, bac « parents / rotation » derrière ;
    # poignée de cuir cognac et étiquette d'ardoise sur la face côté séjour
    for a, b in CASES[1:]:
        yc = (a + b) / 2
        out += [A(252.75, a + 0.2, 269.5, b - 0.2, ZI0, 13.85, "tissu", r=1, b=0.6),
                A(231.0, a + 0.2, 248.0, b - 0.2, ZI0, 13.85, "tissu", r=1, b=0.6),
                A(269.45, yc - 2.0, 269.85, yc + 2.0, 11.0, 12.1, "cuir", r=0.2, b=0.1),
                B(269.45, yc - 2.4, 269.6, yc + 2.4, 7.3, 9.6, "ardoise_noire")]
    # assise : coussin cuir cognac 38¾ × 32½ × 2½ (dessus à 18½), dossier bas de chêne (dessus à 26 = point plein le plus
    # haut), traversin Ø 7 po appuyé au dossier
    out += [A(231.25, 53.5, 270.0, 86.0, 16, 18.5, "cuir", r=1.5, b=1.0),
            A(X0, YB0, 231.25, 86.0, 16, 26, "placage", r=0.4, b=0.3),
            CY(234.75, 54.5, 84.5, 22.0, 3.5, "cuir", pans=32)]
    # présentoir à livres de face (bac de chêne en gradins, 3 rangs, couvertures vers le séjour ; dessus à 24)
    py0, py1 = 88.0, 110.0
    out += [A(257, py0, 270, py1, 16, 16.75, "placage", r=0.4, b=0.2),
            A(257, py0, 265.5, py1, 16.75, 18.5, "placage", r=0.4, b=0.2),
            A(257, py0, 261.0, py1, 18.5, 20.5, "placage", r=0.4, b=0.2),
            A(257, py0, 258.0, py1, 20.5, 24.0, "placage", r=0.3, b=0.2),
            A(269.25, py0, 270, py1, 16.75, 17.9, "placage", r=0.3, b=0.15),
            A(257, py0, 270, py0 + 0.6, 16.75, 18.0, "placage", r=0.2, b=0.1), A(257, py1 - 0.6, 270, py1, 16.75, 18.0, "placage", r=0.2, b=0.1)]
    rangs = [(268.4, 16.75, 22.3, [(89.0, 98.4, "art-argile"), (99.6, 109.0, "laque-marine")]),
             (264.7, 18.5, 23.4, [(88.9, 97.0, "art-sable"), (98.0, 108.8, "rouge-velo")]),
             (260.5, 20.5, 24.0, [(89.5, 99.0, "draps"), (100.0, 109.0, "cuir")])]
    for xr, z0, z1, ls in rangs:
        out += [A(xr, a, xr + 0.55, b, z0, z1, m, r=0.15, b=0.1) for a, b, m in ls]
    # plateau-télécommandes : plateau creux de chêne doublé de feutre, télécommandes, manette, module USB-C
    # (ferme la fente de 4½ po sous la marche 3 : il reste 2 po sous le giron, 1 po sous le limon)
    out += [A(X0, 120.5, X1, YB1, 16, 16.75, "placage", r=0.5, b=0.2),
            A(X0, 120.5, X1, YB1, 16.75, 18.5, "placage", r=0.5, b=0.2, trou=0.75),
            B(X0 + 0.75, 121.25, X1 - 0.75, YB1 - 0.75, 16.75, 16.95, "tissu"),
            A(236.0, 122.4, 242.5, 124.1, 16.95, 17.75, "carbone", r=0.5, b=0.3),
            A(244.0, 123.6, 250.5, 125.3, 16.95, 17.75, "carbone", r=0.5, b=0.3),
            A(255.0, 122.3, 260.5, 125.9, 16.95, 18.15, "carbone", r=1.2, b=0.5),
            B(262.0, 127.15, 266.0, 127.5, 17.0, 18.1, "metal"),
            B(262.8, 127.1, 263.8, 127.15, 17.4, 17.7, "ecran"), B(264.2, 127.1, 265.2, 127.15, 17.4, 17.7, "ecran")]
    # sabot technique (panneau avant vissé ; bloc 24 V, module USB, détecteur dont la lentille regarde la porte de la
    # chambre 2) et chasse de 3½ po sous la marche 1, arrêtée avant le pied du limon (y 149-150)
    out += [A(X0, YB1, X1, 139.0, 0, 11.0, "placage", r=0.5, b=0.3),
            CY(262.0, 139.0, 139.45, 8.5, 0.85, "blanc", pans=24),
            A(X0, 139.0, X1, 148.5, 0, 3.5, "placage", r=0.4, b=0.3)]
    # bouton-poussoir de laiton (24 V) sur le flanc du banc, côté cabane : allume et gradue la lune
    out += [CY(267.75, 51.95, 52.5, 11.25, 0.7, "laiton", pans=24)]
    return out


def _cabane(h):
    B, A, C = h.B, h.A, h.C
    out = []
    # matelas de laine feutrée 32 × 32 × 4 (housse lavable) et 2 coussins debout (cuir cognac, laine crème)
    out += [A(237, 15, 269, 47, 0, 4, "tapis", r=2, b=1.5),
            A(237.5, 18, 243.5, 30.5, 4, 16, "cuir", r=2.5, b=2.4), A(237.5, 31.5, 243.5, 44, 4, 16, "draps", r=2.5, b=2.4)]
    # garde-pieds bas de chêne sur 2 pattes ancrées à la dalle, ¾ po devant le verre du gym
    out += [A(X0, 14, 231.25, 47, 0.75, 12, "placage", r=0.4, b=0.25),
            B(229.9, 15.5, 231.1, 17.5, 0, 0.75, "metal"), B(229.9, 43.5, 231.1, 45.5, 0, 0.75, "metal")]
    # deux rebords à livres de chêne à lèvre, vissés dans la fourrure du mur avant (livres de face, ≤ 26 po)
    couv = [("art-argile", "laque-marine", "art-sable"), ("rouge-velo", "draps", "cuir")]
    for i, z in enumerate((5.0, 20.0)):
        out += [A(238, 10, 268, 13.75, z, z + 0.75, "placage", r=0.3, b=0.2), B(238, 13.0, 268, 13.75, z + 0.75, z + 3.0, "placage")]
        hs = (8.4, 7.4, 9.0) if i == 0 else (5.2, 4.6, 5.0)
        for (xa, xb), m, hz in zip(((240.0, 248.5), (249.5, 257.0), (258.5, 266.5)), couv[i], hs):
            out.append(A(xa, 12.2, xb, 12.8, z + 0.75, z + 0.75 + hz, m, r=0.15, b=0.1))
    # la lune : disque opalin Ø 12 po, 1 po d'épaisseur, vissé sous la marche tournante T1 (dessous à 80½)
    lx, ly, lr = LUNE
    out += [C(lx, ly, lr - 0.4, 80.25, 80.5, "laiton", pans=48), C(lx, ly, lr, 79.5, 80.25, "spot", pans=64)]
    return out


def appliquer_scene(S, h):
    # SS-16 : le dessous de l'escalier était vide ; on ne retire que ce qui serait posé dans l'emprise (rien en principe)
    S["mobilier"][:] = [o for o in S["mobilier"] if not _dans_zone(o)]
    S["mobilier"] += _banc(h) + _cabane(h)
    # la lune éclaire le coin-cabane (petite lumière ponctuelle sous T1)
    S["lumieres"].append({"x": LUNE[0], "y": LUNE[1], "z": 86, "i": 2.5})
    # visite : le banc vu du passage rampe ↔ divan ; le coin-cabane et sa lune
    # (depuis le séjour, entre la rampe et le divan : sous y ≈ 70, les barreaux commencent au-dessus des yeux)
    S["visites"] += [{"nom": "Banc-cabane cinéma (sous l'escalier)", "x": 304, "y": 34, "cap": 136},
                     {"nom": "Coin-cabane et sa lune", "x": 340, "y": 28, "cap": 178}]
    for p in S["palette"]:
        if p[0] == "Escalier flottant":
            p[1] = p[1].replace("dessous dégagé (béton poli continu)", "dessous : banc-cabane bas (voir ci-dessous), la vue reste ouverte au-dessus de 26 po")
    S["palette"].append(["Banc-cabane (escalier)",
                         "sous l'escalier : banc bas de chêne blanc ajouré sur socle d'acier noir en retrait (DEL 2700 K), 10 bacs de feutre "
                         "de laine à étiquettes d'ardoise, assise et traversin cuir cognac, présentoir à livres, plateau-télécommandes ; "
                         "coin-cabane au sol (matelas de laine crème) sous une « lune » lumineuse ; rien de plein au-dessus de 26 po",
                         "#9A5B32"])
