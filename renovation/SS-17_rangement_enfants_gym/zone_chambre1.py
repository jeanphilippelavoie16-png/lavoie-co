"""SS-17 — zone CHAMBRE 1 (l'enfant de 4 ans) : « Le socle de chêne ».

Un seul socle de chêne fait le tour de la chambre : LIT-PLATEFORME QUEEN « cabane » dans le coin ouest-arrière (tête au
mur ouest, long côté au mur arrière, dessus du matelas à 22 po, 3 bacs-wagons roulants dessous, dosseret à niches
éclairées, tête en lattes de chêne, canopée de rangement au-dessus et rideau-cabane), puis BANQUETTE sous les deux
fenêtres (6 tiroirs-images ; c'est aussi la marche d'évacuation), 2 bibliothèques et une valance, puis GARE À JOUETS le
long du mur de la chambre 2 (bacs à hauteur d'enfant, mur à crémaillères qui grandit). L'ancienne garde-robe de SS-16
(cloisons P12 et P13, portes coulissantes P07) est remplacée par une GARDE-ROBE INTÉGRÉE de 134 po sur le mur de la salle
de bain (penderie évolutive, tour de tiroirs-images, niche-cachette, tiroirs de plinthe) ; le recoin d'entrée devient la
STATION DU MATIN. Règle des 4 pieds : ce qui est à l'enfant est sous 48 po ; ce qui est aux parents est au-dessus.

Spec : scratchpad/ss17_conception/final_chambre1/final_chambre1.json (+ plan et élévations). Pouces, repère de la maison.
Faces des murs : ouest (fondation) x = 10 ; arrière (fondation) y = 370 ; P05 (salle de bain) y = 252,25 ;
P07 (chambre 2) x = 237,75 ; P06 (hall) y = 232,25 ; P04 (salle de bain / recoin) x = 144,25.
Rien ne dépasse x = 237,75 (la chambre 2 met ses meubles dos à dos de l'autre côté de P07).
"""

# --------------------------------------------------------------------------------------------- repères de la pièce
XW, YB, YS, XE = 10.0, 370.0, 252.25, 237.75        # nu : mur ouest, mur arrière, mur P05, mur P07
YR, XR = 232.25, 144.25                              # recoin d'entrée : face de P06, face de P04
AIR = 0.5                                            # vide d'air derrière les caissons contre la fondation
YBA = YB - AIR                                       # dos des caissons du mur arrière

# emprise de la zone (pour retirer le mobilier de SS-16) : chambre + ancienne garde-robe, et le recoin d'entrée
ZONE = [(9.5, 250.5, 240.0, 371.0), (142.0, 230.5, 240.0, 252.6)]

# ------------------------------------------------------------------------------------------------- plan (P-127)
RETIRER_MURS = {"mur-SS-P12", "mur-SS-P13"}          # cloisons de l'ancienne garde-robe
RETIRER_PORTES = {"ouv-SS-P07"}                      # ses portes coulissantes
RETIRER_PIECES = {"piece-SS-GR1"}                    # fusionnée à la chambre 1
RETIRER_EQUIP = {"elem-SS-P-COMMODE1"}               # commode du mur est (remplacée par la gare à jouets)

EQUIPEMENTS = [  # id, type, nom, libellé, x, y, rotation, (longueur, largeur) — repère local : dos vers −y
    ("elem-SS-P-C1-LIT", "autre", "Lit-plateforme queen « cabane » (matelas 60 × 80 à 22 po), 3 bacs roulants dessous, "
     "dosseret à niches éclairées", "LIT QUEEN", 52.0, 336.0, 0, (82, 68)),
    ("elem-SS-P-C1-CANOPEE", "trappe", "Canopée de rangement au-dessus du lit (dessous à 72 po), portes à loquet", "",
     51.25, 362.75, 180, (81.5, 13.5)),
    ("elem-SS-P-C1-BANC", "autre", "Banquette des fenêtres (assise 16–18 po), 6 tiroirs-images ; marche d'évacuation",
     "BANQUETTE", 165.375, 360.75, 180, (144.75, 17.5)),
    ("elem-SS-P-C1-BIB1", "armoires", "Bibliothèque entre les fenêtres (livres face avant), ancrée", "", 144.0, 363.75, 180, (24, 11.5)),
    ("elem-SS-P-C1-BIB2", "armoires", "Bibliothèque au coin des fenêtres, ancrée", "", 208.0, 363.75, 180, (24, 11.5)),
    ("elem-SS-P-C1-GARE", "comptoir", "Gare à jouets : 3 modules bas de bacs (dessus à 24 po), crémaillères au mur",
     "BACS", 228.75, 310.0, 90, (84, 18)),
    ("elem-SS-P-C1-GR", "armoires", "Garde-robe intégrée 134 po (penderie évolutive, tour de tiroirs, niche-cachette, "
     "tiroirs de plinthe)", "G.-R.", 77.125, 264.25, 0, (134.25, 24)),
    ("elem-SS-P-C1-VEST", "autre", "Station du matin : banc à cases, crochets, miroir incassable, tablette", "",
     170.125, 239.25, 0, (51.75, 14)),
]


def appliquer_modifs(L, base):
    L["MURS"][:] = [m for m in L["MURS"] if m[0] not in RETIRER_MURS]
    L["PORTES"][:] = [p for p in L["PORTES"] if p[0] not in RETIRER_PORTES]
    L["PIECES"][:] = [p for p in L["PIECES"] if p[0] not in RETIRER_PIECES]
    L["EQUIPEMENTS"][:] = [e for e in L["EQUIPEMENTS"] if e[0] not in RETIRER_EQUIP]
    L["EQUIPEMENTS"] += EQUIPEMENTS


def apres_modifs(maison, base):
    ss = next(n for n in maison["niveaux"] if n["id"] == "SS")
    for p in ss["pieces"]:
        if p["id"] == "piece-SS-CH1":
            p["description"] = ("Chambre 1 (enfant de 4 ans) : lit queen-plateforme en coin, banquette sous les fenêtres, gare à "
                                "jouets, garde-robe intégrée sur le mur de la salle de bain (l'ancienne garde-robe est fusionnée) — "
                                "proposition SS-17 (esquisse)")
    for o in ss["ouvertures"]:
        if o["id"] in ("ouv-SS-009", "ouv-SS-010"):
            o["note"] = ((o.get("note") or "") + " SS-17 : fenêtre d'évacuation de la chambre 1 — doit OUVRIR (≥ 0,35 m², "
                         "aucune dimension < 380 mm) ; la banquette fixe sous la fenêtre sert de marche ; allège et tête à "
                         "mesurer ; à valider avec la Ville et un professionnel.").strip()


# --------------------------------------------------------------------------------------------------- maquette 3D
def _bornes(o):
    """Emprise en plan (x0, y0, x1, y1) d'un objet de S["mobilier"], ou None."""
    f = o.get("forme")
    if "x0" in o and "y0" in o:
        return o["x0"], o["y0"], o["x1"], o["y1"]
    if f == "cylindre":
        r = o.get("r", 0)
        if o.get("axe") == "y":
            return o["x"] - r, o["y0"], o["x"] + r, o["y1"]
        if o.get("axe") == "x":
            return o["x0"], o["y"] - r, o["x1"], o["y"] + r
        return o["x"] - r, o["y"] - r, o["x"] + r, o["y"] + r
    if f == "tube":
        xs, ys = [p[0] for p in o["pts"]], [p[1] for p in o["pts"]]
        return min(xs), min(ys), max(xs), max(ys)
    if "x" in o and "y" in o:
        return o["x"], o["y"], o["x"], o["y"]
    return None


def _dans_zone(o):
    b = _bornes(o)
    if b is None:
        return False
    return any(zx0 <= b[0] and b[2] <= zx1 and zy0 <= b[1] and b[3] <= zy1 for zx0, zy0, zx1, zy1 in ZONE)


def _mobilier(h):
    A, B, C, CX, CY, T, SPH = h.A, h.B, h.C, h.CX, h.CY, h.T, h.SPH
    M = []
    LIVRES = ["art-argile", "laque-marine", "blanc", "art-sable", "carbone", "osier", "placage"]

    # ================================================================ C1-LIT : lit-plateforme queen « cabane »
    LX0, LX1, LY0, LY1 = 11.0, 93.0, 302.0, 364.0
    M += [A(LX0, LY0, LX1, LY1, 10.5, 12, "placage", r=1, b=0.5)]                              # plateau (dessus à 12)
    M += [A(LX0, LY0, 14.5, LY1, 1.5, 10.5, "placage", r=0.5, b=0.3),                           # flanc ouest
          A(89.5, LY0, LX1, LY1, 3, 10.5, "placage", r=1, b=0.5),                               # flanc est (pied du lit)
          B(90.0, LY0 + 3, LX1 - 0.5, LY1, 0, 3, "carbone")]                                    # socle en retrait de 3 po
    M += [A(x, LY0, x + 3, LY1, 1.5, 10.5, "placage", r=0.4, b=0.3) for x in (37.5, 63.5)]      # cloisons des « garages »
    M += [B(14.5, 303.2, 89.5, 304.0, 0, 10.5, "carbone"),                                      # fond d'ombre des wagons
          B(15.0, 302.8, 89.0, 303.1, 0.3, 0.6, "spot")]                                         # DEL de plinthe (chemin de nuit)
    for wx0 in (14.5, 40.5, 66.5):                                                              # 3 bacs-wagons de 23 po
        xc = wx0 + 11.5
        M += [A(wx0 + 0.2, LY0, wx0 + 22.8, 303.25, 1.6, 10.2, "placage", r=0.8, b=0.4),
              A(xc - 4, 301.88, xc + 4, 302.02, 7.2, 8.8, "carbone", r=0.7, b=0.1),             # poignée découpée
              B(xc - 3.5, 301.85, xc + 3.5, 302.0, 3.0, 5.6, "blanc"),                          # étiquette-image
              CY(wx0 + 2.5, 303.3, 310, 1.0, 0.8, "carbone"), CY(wx0 + 20.5, 303.3, 310, 1.0, 0.8, "carbone")]  # roulettes
    # matelas, couette, coussins, jeté au pied, toutou
    M += [A(12, 303, 92, 363, 12, 22, "draps", r=3, b=2.5),
          A(34, 302.6, 92.4, 363.4, 20.6, 23.2, "draps", r=2.5, b=1.8),
          A(70, 302.3, 92.7, 363.7, 22.8, 24.2, "tissu", r=2, b=1.0),
          A(14, 306, 31, 331.5, 21.5, 27.5, "draps", r=4, b=3), A(14, 334.5, 31, 360, 21.5, 27.5, "draps", r=4, b=3),
          A(30, 336, 34, 358, 22, 30, "art-argile", r=3, b=2)]                                  # coussin d'accent
    M += [SPH(44, 350, 25.8, 3.4, "art-sable"), SPH(44, 350, 30.6, 2.5, "art-sable"),
          SPH(42.6, 350, 32.8, 0.9, "art-sable"), SPH(45.4, 350, 32.8, 0.9, "art-sable")]       # ourson

    # ================================================================ C1-DOSSERET : niches éclairées, tablette à 34 po
    NICHES = [(16.67, 32.67), (44.0, 60.0), (71.33, 87.33)]                                     # 16 po de large
    NZ0, NZ1 = 23.5, 32.5                                                                       # au-dessus du matelas
    M += [B(LX0, LY1, LX1, YBA, 12, NZ0, "placage"),
          A(LX0, 363.4, LX1, YBA, NZ1, 34.5, "placage", r=0.8, b=0.4)]                          # tablette du dessus
    bords = [LX0] + [v for n in NICHES for v in n] + [LX1]
    M += [B(a, LY1, b, YBA, NZ0, NZ1, "placage") for a, b in zip(bords[::2], bords[1::2])]
    for nx0, nx1 in NICHES:
        M += [B(nx0, 368.6, nx1, YBA, NZ0, NZ1, "art-argile"),                                  # fond argile
              B(nx0 + 0.5, LY1 + 0.3, nx1 - 0.5, 368.6, NZ1 - 0.3, NZ1, "spot")]                 # DEL 2200 K sous le dessus
    M += [B(19 + 1.4 * k, 366.0, 20.2 + 1.4 * k, 368.4, NZ0, NZ0 + 6.5 - (k % 3), LIVRES[k % 7]) for k in range(6)]
    M += [SPH(52, 366.4, NZ0 + 2.2, 2.2, "abat-jour")]                                          # veilleuse
    M += [CY(80, 365.2, 365.5, NZ0 + 2.2, 1.7, "blanc", pans=24), CY(80, 365.5, 366, NZ0 + 2.2, 1.5, "laque-marine")]  # prise cachée (couvercle)
    M += [B(66 + 1.2 * k, 365.5, 67 + 1.2 * k, 368.8, 34.5, 34.5 + 7 + (k % 2), LIVRES[(k + 2) % 7]) for k in range(5)]
    M += [C(84, 367, 1.4, 34.5, 38.5, "verre-clair")]                                           # verre d'eau

    # ================================================================ C1-TETE : tête de lit en lattes (mur ouest)
    M += [B(XW, LY0, XW + 0.3, LY1, 12, 46, "carbone")]
    y = LY0
    while y + 1.5 <= LY1 + 0.01:
        M.append(A(XW, y, XW + 1, y + 1.5, 12, 46, "placage", r=0.3, b=0.2))
        y += 2.0
    for yl in (318.0, 348.0):                                                                   # 2 liseuses à bras court
        M += [CX(XW, XW + 0.8, yl, 51, 1.8, "metal", pans=24),
              T([(XW + 0.8, yl, 51), (15.5, yl, 51), (17, yl, 50)], 0.3, "metal"),
              C(17, yl, 1.9, 46.6, 50.2, "metal", r2=1.0), C(17, yl, 1.6, 46.5, 46.65, "abat-jour")]

    # ================================================================ C1-CANOPEE : armoires hautes au-dessus du lit
    CX0, CX1, CY0 = XW + 0.5, 92.0, 356.0
    M += [A(CX0, CY0, CX1, YBA, 72, 95.9, "placage", r=0.5, b=0.3)]
    larg = (CX1 - CX0) / 3
    M += [B(CX0 + larg * k - 0.1, CY0 - 0.12, CX0 + larg * k + 0.1, CY0 + 0.05, 72.3, 95.6, "carbone") for k in (1, 2)]
    M += [B(CX0 + larg * (k + 0.5) - 2, CY0 - 0.4, CX0 + larg * (k + 0.5) + 2, CY0, 73.4, 74.2, "metal") for k in range(3)]  # loquets
    M += [B(CX0 + 1.5, CY0 + 1, CX1 - 1.5, CY0 + 2, 71.75, 72, "spot")]                         # DEL chaude = veilleuse

    # ================================================================ C1-RIDEAU : rail en L au plafond, rideau sable ouvert
    #   (le pan du long côté se range contre le mur ouest, celui du pied contre la banquette : le coin du pied reste libre)
    M += [B(XW, 299.6, 94.4, 300.4, 95.3, 96, "metal"), B(93.6, 299.6, 94.4, 352, 95.3, 96, "metal")]
    M += [C(11.4 + 1.7 * k, 300 + (0.45 if k % 2 else -0.45), 1.05, 1.5, 95.3, "art-sable", pans=12) for k in range(6)]
    M += [C(94 + (0.45 if k % 2 else -0.45), 350.4 - 1.7 * k, 1.05, 1.5, 95.3, "art-sable", pans=12) for k in range(5)]

    # ================================================================ C1-BANC : banquette-évacuation, 6 tiroirs-images
    BX0, BX1, BY0 = 93.0, XE, 352.0
    M += [B(BX0 + 0.5, BY0 + 3, BX1, YBA, 0, 3, "carbone"),                                      # socle en retrait
          B(BX0 + 1, BY0 + 2.9, 219.0, BY0 + 3.1, 0.4, 0.7, "spot"),                              # DEL de plinthe
          A(BX0, BY0, BX1, YBA, 3, 15, "placage", r=0.5, b=0.3),
          A(BX0 - 0.25, BY0 - 0.5, BX1, YBA, 15, 16, "placage", r=1, b=0.5)]                     # dessus arrondi à 16 po
    TX = [BX0 + k * (219.75 - BX0) / 6 for k in range(7)]                                       # 6 tiroirs de 21 po (le coin est fixe)
    for a, b in zip(TX, TX[1:]):
        xc = (a + b) / 2
        M += [A(a + 0.2, BY0 - 0.7, b - 0.2, BY0 + 0.05, 3.6, 14.6, "art-argile", r=0.8, b=0.3),
              B(xc - 3.5, BY0 - 0.86, xc + 3.5, BY0 - 0.68, 9.4, 12.6, "blanc"),
              A(xc - 4, BY0 - 0.8, xc + 4, BY0 - 0.66, 5.6, 6.8, "carbone", r=0.5, b=0.1)]
    for a, b in ((BX0 + 0.6, 131.6), (156.4, 195.6), (220.4, BX1 - 0.3)):                         # coussins amovibles
        M.append(A(a, BY0 - 0.2, b, YBA - 0.2, 16, 18.5, "tissu", r=1.5, b=1.2))
    M += [A(95, 364, 109, 368.6, 18.5, 31, "art-argile", r=3, b=2), A(222, 364.2, 236, 368.8, 18.5, 30, "laque-marine", r=3, b=2)]

    # ================================================================ C1-BIB1 / C1-BIB2 : bibliothèques sur la banquette
    def bibliotheque(x0, x1, bas_osier):
        out = [A(x0, 358, x0 + 0.75, YBA, 16, 86, "placage", r=0.3, b=0.2),
               A(x1 - 0.75, 358, x1, YBA, 16, 86, "placage", r=0.3, b=0.2),
               B(x0 + 0.75, YBA - 0.5, x1 - 0.75, YBA, 16, 86, "art-argile"),
               B(x0 + 0.75, 358, x1 - 0.75, YBA, 16, 16.75, "placage")]
        xa, xb = x0 + 0.75, x1 - 0.75
        if bas_osier:                                                                           # 2 bacs d'osier à hauteur d'enfant
            out += [B(xa, 358.5, xb, YBA - 0.5, 28, 28.75, "placage"), B(xa, 358.5, xb, YBA - 0.5, 40, 40.75, "placage")]
            out += [A(xa + 0.8, 359.2, xb - 0.8, 368.4, z, z + 10, "osier", r=1.5, b=0.8) for z in (16.75, 28.75)]
            rebords = []
        else:                                                                                   # 3 rebords « face avant »
            rebords = [22, 32, 42]
        for z in rebords:
            out += [B(xa, 364.5, xb, YBA - 0.5, z - 0.75, z, "placage"),
                    A(xa, 363.9, xb, 364.6, z - 0.75, z + 2.2, "placage", r=0.3, b=0.15)]
            out += [B(xa + 0.6, 366.6 - 0.4 * (k % 2), xa + 0.6 + 10, 367.3 - 0.4 * (k % 2), z, z + 8.6 - 0.8 * k, LIVRES[(int(z) // 10 + k) % 7])
                    for k in range(1)]
            out += [B(xa + 11.4, 366.4, xb - 0.6, 367.1, z, z + 8.2, LIVRES[(int(z) // 10 + 3) % 7])]
        for z in (54, 66, 78):                                                                  # tablettes réglables (parents)
            out.append(A(xa, 358.6, xb, YBA - 0.5, z - 0.75, z, "placage", r=0.2, b=0.15))
            n = 0
            xx = xa + 1.0
            while xx < xb - 6:
                ep = 0.8 + (n * 7 % 4) * 0.25
                out.append(B(xx, 360.5, xx + ep, 368, z, z + 7.5 + (n * 5 % 3), LIVRES[(n + int(z)) % 7]))
                xx += ep + 0.08
                n += 1
                if n == 7:
                    break
            out.append(C(xb - 3, 364, 2.0, z, z + 4.5, "blanc" if z != 66 else "osier", pans=20))
        return out

    M += bibliotheque(132.0, 156.0, False) + bibliotheque(196.0, 220.0, True)

    # ================================================================ C1-VALANCE : bandeau de chêne (stores sans cordon cachés)
    M += [A(92.0, 360.0, BX1, YBA, 86, 95.9, "placage", r=0.4, b=0.3)]

    # ================================================================ C1-GARE : gare à jouets (mur de la chambre 2)
    GX0, GX1 = 219.75, XE                                                                       # 18 po de profond, x < 237,75
    M += [B(GX0 + 3, 268.5, GX1, 351.5, 0, 2.5, "carbone")]                                      # socle vissé en retrait
    for y0 in (268.0, 296.0, 324.0):
        y1 = y0 + 28
        M += [A(GX0, y0 + 0.1, GX1, y0 + 0.85, 2.5, 22.75, "placage", r=0.3, b=0.2),
              A(GX0, y1 - 0.85, GX1, y1 - 0.1, 2.5, 22.75, "placage", r=0.3, b=0.2),
              B(GX0 + 1.2, y0 + 0.85, GX1, y1 - 0.85, 2.5, 22.75, "carbone"),                    # fond d'ombre
              B(GX0, y0 + 0.85, GX1, y1 - 0.85, 2.5, 3.25, "placage"),
              B(GX0, y0 + 0.85, GX1, y1 - 0.85, 12.6, 13.1, "placage"),
              B(GX0, y0 + 13.75, GX1, y0 + 14.25, 3.25, 22.75, "placage")]
        for yb0 in (y0 + 0.95, y0 + 14.35):                                                     # 4 bacs par module
            yb1 = yb0 + 12.7
            ym = (yb0 + yb1) / 2
            for zb0 in (3.35, 13.2):
                M += [A(GX0 - 0.5, yb0, GX0 + 0.3, yb1, zb0, zb0 + 9.2, "art-argile", r=0.7, b=0.3),
                      B(GX0 - 0.62, ym - 2.6, GX0 - 0.48, ym + 2.6, zb0 + 3.2, zb0 + 6.0, "blanc"),
                      A(GX0 - 0.6, ym - 2.4, GX0 - 0.46, ym + 2.4, zb0 + 7.0, zb0 + 8.2, "carbone", r=0.5, b=0.1)]
    M += [A(GX0 - 0.5, 267.5, GX1, 352.0, 22.75, 24, "placage", r=1, b=0.6)]                       # comptoir de jeu à 24 po
    # jeux sur le comptoir : tour de blocs, plaque de construction
    BLOCS = ["art-argile", "placage", "laque-marine", "blanc", "art-sable", "placage"]
    M += [A(224 + (k % 2) * 0.4, 280 + (k % 3) * 0.3, 227 + (k % 2) * 0.4, 283 + (k % 3) * 0.3, 24 + 3 * k, 27 + 3 * k,
            BLOCS[k], r=0.3, b=0.2) for k in range(5)]
    M += [B(224, 330, 234, 342, 24, 24.4, "laque-marine")] + \
         [A(226 + 3 * (k % 3), 332 + 3.5 * (k // 3), 228.5 + 3 * (k % 3), 334 + 3.5 * (k // 3), 24.4, 25.6, BLOCS[k], r=0.2, b=0.1)
          for k in range(6)]

    # ================================================================ C1-MUR : crémaillères, panneau perforé, fil à dessins
    M += [B(XE - 0.4, yc - 0.5, XE, yc + 0.5, 30, 84, "metal") for yc in (272, 296, 324, 348)]
    PX0 = XE - 1.4                                                                              # panneau sur consoles
    M += [A(PX0, 274, PX0 + 0.75, 346, 30, 66, "placage", r=0.4, b=0.2)]
    M += [B(PX0 - 0.03, yy - 0.18, PX0, yy + 0.18, zz - 0.18, zz + 0.18, "carbone")
          for yy in range(277, 345, 4) for zz in range(33, 65, 4)]                              # trous du panneau perforé
    M += [CX(PX0 - 2.2, PX0, yy, zz, 0.3, "placage", pans=12) for yy, zz in ((285, 57), (301, 45), (321, 57), (333, 41))]  # chevilles
    M += [A(PX0 - 4.5, 290, PX0, 312, 48.6, 49.3, "placage", r=0.3, b=0.15),                    # petite tablette
          C(PX0 - 2.2, 295, 1.3, 49.3, 53.3, "art-argile", pans=20), C(PX0 - 2.2, 300, 1.3, 49.3, 52.8, "laque-marine", pans=20)]
    M += [CY(XE - 0.8, 270, 350, 78, 0.12, "metal")]                                            # câble à dessins
    DESSINS = ["blanc", "art-sable", "blanc", "blanc", "art-sable", "blanc"]
    M += [B(XE - 0.95, 277 + 11.5 * k, XE - 0.85, 286 + 11.5 * k, 67.5 + (k % 2), 77.5, DESSINS[k]) for k in range(6)]
    M += [B(XE - 1.15, 280.5 + 11.5 * k, XE - 0.75, 282.5 + 11.5 * k, 76.8, 78.6, "placage") for k in range(6)]  # pinces

    # ================================================================ GARDE-ROBE intégrée (mur P05) : 134¼ × 24 po
    GY0, GY1 = YS, YS + 24.0                                                                    # face à y = 276,25
    GF = GY1 - 0.75                                                                             # plan des façades
    M += [B(XW, GY0, XR, GF, 0, 4, "placage")]                                                  # coup-de-pied
    M += [A(XW + 0.2 + 44.75 * k, GF, XW + 44.55 + 44.75 * k, GY1, 0.5, 3.6, "placage", r=0.4, b=0.2) for k in range(3)]  # tiroirs de plinthe
    M += [A(XW + 22.4 + 44.75 * k - 3, GY1 - 0.05, XW + 22.4 + 44.75 * k + 3, GY1 + 0.08, 2.4, 3.0, "carbone", r=0.3, b=0.1) for k in range(3)]
    M += [B(XW, GY0, 94.0, GF - 0.2, 4, 96, "placage"), B(XW, GF - 0.2, 94.0, GF, 4, 96, "carbone")]  # caissons A et B, fond d'ombre
    M += [B(94.0, GY0, XR, GF - 0.2, 46, 96, "placage"), B(94.0, GF - 0.2, XR, GF, 46, 96, "carbone")]  # dessus du module C

    def porte(x0, x1, z0, z1, poignee):
        out = [A(x0 + 0.1, GF, x1 - 0.1, GY1, z0 + 0.1, z1 - 0.1, "placage", r=0.3, b=0.2)]
        xp = x1 - 1.6 if poignee == "d" else x0 + 0.6
        zp = min(max(z0 + 2, 40), z1 - 14)
        out.append(B(xp + 0.2, GY1 - 0.02, xp + 0.8, GY1 + 0.06, zp, zp + 9, "carbone"))         # poignée encastrée (gorge)
        return out

    # C1-GR-A : penderie évolutive, 2 portes de 21 po
    M += porte(XW, 31.0, 4, 96, "d") + porte(31.0, 52.0, 4, 96, "g")
    # C1-GR-B : 4 tiroirs-images (4 → 40 po) + 2 portes à loquet au-dessus
    for k in range(4):
        z0 = 4 + 9 * k
        M += [A(52.2, GF, 93.8, GY1, z0 + 0.15, z0 + 8.85, "art-argile", r=0.6, b=0.3),
              B(69.5, GY1, 76.5, GY1 + 0.15, z0 + 4.2, z0 + 7.2, "blanc"),
              A(69, GY1 - 0.02, 77, GY1 + 0.12, z0 + 1.6, z0 + 2.8, "carbone", r=0.5, b=0.1)]
    M += porte(52.0, 73.0, 40, 96, "d") + porte(73.0, 94.0, 40, 96, "g")
    # C1-GR-C : niche-cachette (46 × 22 × 40 po) + 2 portes au-dessus
    NX0, NX1 = 96.1, 142.15
    M += [A(94.0, GY0, NX0, GY1, 4, 46, "placage", r=0.5, b=0.3), A(NX1, GY0, XR, GY1, 4, 46, "placage", r=0.5, b=0.3),
          A(94.0, GY0, XR, GY1, 44, 46.2, "placage", r=0.5, b=0.3),
          B(NX0, GY0, NX1, GY0 + 1, 4, 44, "art-argile"),                                        # fond argile
          A(NX0 + 0.5, GY0 + 1.2, NX1 - 0.5, GY1 - 0.6, 4, 7, "tissu", r=1.5, b=1.2),            # coussin de sol
          A(NX0 + 1.5, GY0 + 1.4, NX0 + 15, GY0 + 6.5, 7, 19, "art-sable", r=3, b=2),
          A(NX0 + 16, GY0 + 1.4, NX0 + 28, GY0 + 6, 7, 17, "art-argile", r=3, b=2),
          SPH(NX1 - 4, GY0 + 3, 38.5, 1.6, "abat-jour"),                                         # veilleuse à pile
          CX(NX0, NX1, GY1 - 1.5, 42.5, 0.3, "metal", pans=12)]                                  # tringle à ressort
    M += [C(NX0 + 0.9 + 1.5 * k, GY1 - 1.5 + (0.35 if k % 2 else -0.35), 0.8, 4.5, 42.4, "art-sable", pans=10) for k in range(4)]
    M += [C(NX1 - 0.9 - 1.5 * k, GY1 - 1.5 + (0.35 if k % 2 else -0.35), 0.8, 4.5, 42.4, "art-sable", pans=10) for k in range(3)]
    M += [B(NX0 + 18 + 1.3 * k, GY0 + 2, NX0 + 19 + 1.3 * k, GY0 + 9, 7, 7.0 + 7 + (k % 2), LIVRES[(k + 1) % 7]) for k in range(4)]
    M += porte(94.0, 119.125, 46, 96, "d") + porte(119.125, XR, 46, 96, "g")

    # ================================================================ C1-VESTIAIRE : station du matin (recoin d'entrée)
    VX0, VX1, VY1 = XR, 196.0, YR + 14.0
    M += [B(VX0, YR, VX1, VY1, 0, 1, "carbone"),
          B(VX0, YR, VX1, YR + 0.75, 1, 65, "placage"),                                          # panneau de chêne
          A(VX0, YR, VX1, VY1, 10.75, 12, "placage", r=1, b=0.5),                                # banc à 12 po
          A(VX0 + 0.5, YR + 0.75, VX1 - 0.5, VY1 - 0.5, 12, 13.4, "tissu", r=1.2, b=0.8)]
    M += [A(x, YR, x + 0.75, VY1, 1, 10.75, "placage", r=0.3, b=0.2) for x in (VX0, 161.5, 178.5, VX1 - 0.75)]
    M += [A(VX0 + 2 + 17.2 * k, YR + 4, VX0 + 7 + 17.2 * k, YR + 11, 1, 3.5, "art-sable" if k % 2 else "art-argile", r=1.5, b=0.8)
          for k in range(3)] + \
         [A(VX0 + 8 + 17.2 * k, YR + 4, VX0 + 13 + 17.2 * k, YR + 11, 1, 3.5, "art-sable" if k % 2 else "art-argile", r=1.5, b=0.8)
          for k in range(3)]                                                                     # pantoufles
    for xh, zh in [(149, 36), (157, 36), (165, 36), (173, 36), (152, 60), (165, 60), (178, 60)]:  # crochets champignons
        M += [CY(xh, YR + 0.75, YR + 2.6, zh, 0.3, "placage", pans=12), SPH(xh, YR + 2.9, zh, 0.75, "placage")]
    M += [A(154.5, YR + 1.2, 159.5, YR + 4.6, 21.5, 36.2, "art-argile", r=1.5, b=1.0),          # petit manteau
          A(162.0, YR + 1.2, 168.5, YR + 5.4, 25.5, 36.0, "laque-marine", r=2, b=1.5)]           # sac à dos
    M += [A(179, YR + 0.75, 195, YR + 1.4, 23.5, 48.5, "placage", r=1, b=0.3),
          B(180, YR + 1.4, 194, YR + 1.5, 24.5, 47.5, "miroir")]                                 # miroir incassable 24–48 po
    M += [B(147, YR + 0.75, 175, YR + 1.15, 42, 56, "carbone")]                                  # tableau « routine du matin »
    M += [A(149 + 5 * k, YR + 1.15, 152.6 + 5 * k, YR + 1.35, 50.5, 54, ["blanc", "art-argile", "art-sable", "blanc", "laque-marine"][k],
            r=0.4, b=0.05) for k in range(5)]
    M += [SPH(150.8 + 5 * k, YR + 1.4, 46.5, 0.6, "art-argile" if k < 3 else "blanc") for k in range(5)]
    M += [A(VX0, YR, VX1, YR + 10, 65, 66.5, "placage", r=0.5, b=0.3)]                           # tablette à 66 po
    M += [A(148 + 15.5 * k, YR + 1.2, 160 + 15.5 * k, YR + 9.2, 66.5, 73, "osier", r=1.2, b=0.6) for k in range(3)]

    # ================================================================ C1-TAPIS : coin jeu au sol (5 × 8 pi) et jouets
    M += [A(108, 286, 204, 346, 0, 0.5, "tapis", r=2, b=0.2)]
    M += [C(190, 334, 9, 0.5, 9.5, "tissu", pans=36, r2=8.4)]                                     # pouf
    M += [A(130, 306, 142, 312, 2.0, 6.4, "art-argile", r=1, b=0.5), A(138, 306.4, 142.2, 311.6, 6.4, 9.6, "placage", r=0.8, b=0.4),
          CY(132.5, 305.4, 312.6, 1.9, 1.4, "carbone", pans=16), CY(139.5, 305.4, 312.6, 1.9, 1.4, "carbone", pans=16)]  # camion de bois
    M += [A(150 + (k % 2) * 0.5, 322, 154 + (k % 2) * 0.5, 326, 0.5 + 4 * k, 4.5 + 4 * k, BLOCS[k], r=0.4, b=0.2) for k in range(4)]
    M += [A(157, 321, 161, 325, 0.5, 4.5, "art-sable", r=0.4, b=0.2), A(145, 329, 149, 333, 0.5, 4.5, "laque-marine", r=0.4, b=0.2)]
    return M


VISITES = [
    {"nom": "Chambre 1 — le socle de chêne", "x": 225, "y": 262, "cap": 160},
    {"nom": "Chambre 1 — lit-cabane", "x": 150, "y": 296, "cap": 162},
    {"nom": "Chambre 1 — banquette des fenêtres", "x": 166, "y": 290, "cap": 98},
    {"nom": "Chambre 1 — gare à jouets", "x": 150, "y": 306, "cap": 8},
    {"nom": "Chambre 1 — garde-robe et cachette", "x": 140, "y": 332, "cap": 238},
    {"nom": "Chambre 1 — station du matin", "x": 205, "y": 290, "cap": 236},
]


def appliquer_scene(S, h):
    S["mobilier"][:] = [o for o in S["mobilier"] if not _dans_zone(o)] + _mobilier(h)
    # éclairage encastré : un au-dessus du coin jeu, un entre le lit et la garde-robe, un dans le recoin d'entrée
    S["lumieres"][:] = [l for l in S["lumieres"] if not (10 < l["x"] < 240 and 250 < l["y"] < 370)]
    S["lumieres"] += [{"x": 166, "y": 318}, {"x": 56, "y": 289, "i": 7}, {"x": 172, "y": 244, "i": 6}]
    v = S["visites"]
    i = next((k for k, s in enumerate(v) if s.get("nom") == "Chambre 1"), len(v))
    v[i:i + 1 if i < len(v) else i] = VISITES
    S["palette"].append(["Chambre 1 (4 ans)",
                         "« le socle de chêne » : lit-plateforme queen en coin (matelas à 22 po, 3 bacs-wagons roulants, niches "
                         "éclairées, tête en lattes, canopée de rangement, rideau-cabane sable), banquette des fenêtres à 6 "
                         "tiroirs-images laque argile (marche d'évacuation), 2 bibliothèques, gare à jouets et mur à crémaillères, "
                         "garde-robe intégrée de 134 po avec niche-cachette, station du matin dans le recoin", "#C39A82"])
