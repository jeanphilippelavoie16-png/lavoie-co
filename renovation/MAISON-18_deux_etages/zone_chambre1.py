"""MAISON-18 — zone CHAMBRE 1 (l'enfant de 4 ans) : « Le socle de chêne », version allégée.

Demande du client (2026-11-01) : « Dans les chambres en bas il y a comme trop de meubles, exagère pas. » On garde trois
pièces de chêne, belles et utiles, et on rend le plancher :
- LIT-PLATEFORME QUEEN dans le coin ouest-arrière (tête au mur ouest, long côté au mur arrière, dessus du matelas à 22 po),
  3 bacs-wagons roulants dessous (les jouets du jour), tête en lattes de chêne, simple tablette-dosseret le long du mur ;
- BANQUETTE sous les deux fenêtres, du pied du lit au mur de la chambre 2 (4 grands tiroirs ; c'est aussi la marche
  d'évacuation) ;
- GARDE-ROBE INTÉGRÉE de 134 po sur le mur de la salle de bain = LE rangement principal : portes pleines de chêne, penderie
  évolutive, 4 tiroirs à sa hauteur, module de rotation des jouets (ce qui ne sert pas cette semaine dort là).
- COIN JEU AU SOL : tapis 5 × 8 pi au centre, un pouf, un seul rebord à livres (couvertures de face) au mur est.
Retirés de la version SS-17 : canopée au-dessus du lit, rideau-cabane (déjà retiré), niches éclairées du dosseret, deux
bibliothèques et valance autour de la banquette, gare à jouets et mur à crémaillères (panneau perforé, câble à dessins),
station du matin du recoin, niche-cachette de la garde-robe, tiroirs de plinthe, la moitié des jouets.

L'ancienne garde-robe de SS-16 (cloisons P12 et P13, portes coulissantes P07) reste fusionnée à la chambre.
Pouces, repère de la maison. Faces des murs : ouest (fondation) x = 10 ; arrière (fondation) y = 370 ; P05 (salle de bain)
y = 252,25 ; P07 (chambre 2) x = 237,75 ; P06 (hall) y = 232,25 ; P04 (salle de bain / recoin) x = 144,25.
Fenêtres (mur arrière) : x 92-132 et 156-196. Porte (P05) : x 201-231 sur P06, battant vers la chambre.
Rien ne dépasse x = 237,75.
"""

# --------------------------------------------------------------------------------------------- repères de la pièce
XW, YB, YS, XE = 10.0, 370.0, 252.25, 237.75        # nu : mur ouest, mur arrière, mur P05, mur P07
YR, XR = 232.25, 144.25                              # recoin d'entrée : face de P06, face de P04
AIR = 0.5                                            # vide d'air derrière les caissons contre la fondation
YBA = YB - AIR                                       # dos des caissons du mur arrière

# emprise de la zone (pour retirer le mobilier de SS-16) : chambre + ancienne garde-robe, et le recoin d'entrée
ZONE = [(9.5, 250.5, 240.0, 371.0), (142.0, 230.5, 240.0, 252.6)]

# ------------------------------------------------------------------------------------------------- plan (P-129)
RETIRER_MURS = {"mur-SS-P12", "mur-SS-P13"}          # cloisons de l'ancienne garde-robe
RETIRER_PORTES = {"ouv-SS-P07"}                      # ses portes coulissantes
RETIRER_PIECES = {"piece-SS-GR1"}                    # fusionnée à la chambre 1
RETIRER_EQUIP = {"elem-SS-P-COMMODE1"}               # commode du mur est (le mur est reste libre : coin jeu)

EQUIPEMENTS = [  # id, type, nom, libellé, x, y, rotation, (longueur, largeur) — repère local : dos vers −y
    ("elem-SS-P-C1-LIT", "autre", "Lit-plateforme queen (matelas 60 × 80 à 22 po), 3 bacs-wagons roulants dessous, tête en "
     "lattes de chêne, tablette-dosseret", "LIT QUEEN", 52.0, 336.0, 0, (82, 68)),
    ("elem-SS-P-C1-BANC", "autre", "Banquette des fenêtres (assise 16 po), 4 grands tiroirs ; marche d'évacuation",
     "BANQUETTE", 165.375, 360.75, 180, (144.75, 17.5)),
    ("elem-SS-P-C1-GR", "armoires", "Garde-robe intégrée 134 po à portes pleines de chêne (penderie évolutive, 4 tiroirs, "
     "rotation des jouets ; le haut aux parents)", "G.-R.", 77.125, 264.25, 0, (134.25, 24)),
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
            p["description"] = ("Chambre 1 (enfant de 4 ans), allégée : lit queen sur plateforme à bacs en coin, banquette sous "
                                "les fenêtres, garde-robe intégrée sur le mur de la salle de bain (l'ancienne garde-robe est "
                                "fusionnée), coin jeu au sol au centre — proposition MAISON-18 (esquisse)")
    for o in ss["ouvertures"]:
        if o["id"] in ("ouv-SS-009", "ouv-SS-010"):
            o["note"] = ((o.get("note") or "") + " Fenêtre d'évacuation de la chambre 1 — doit OUVRIR (≥ 0,35 m², "
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
    A, B, C, CX, CY, SPH = h.A, h.B, h.C, h.CX, h.CY, h.SPH
    M = []

    # ================================================================ C1-LIT : lit-plateforme queen, 3 bacs-wagons
    LX0, LX1, LY0, LY1 = 11.0, 93.0, 302.0, 364.0
    M += [A(LX0, LY0, LX1, LY1, 10.5, 12, "placage", r=1, b=0.5)]                              # plateau (dessus à 12)
    M += [A(LX0, LY0, 14.5, LY1, 1.5, 10.5, "placage", r=0.5, b=0.3),                           # flanc ouest
          A(89.5, LY0, LX1, LY1, 3, 10.5, "placage", r=1, b=0.5),                               # flanc est (pied du lit)
          B(90.0, LY0 + 3, LX1 - 0.5, LY1, 0, 3, "carbone")]                                    # socle en retrait de 3 po
    M += [A(x, LY0, x + 3, LY1, 1.5, 10.5, "placage", r=0.4, b=0.3) for x in (37.5, 63.5)]      # cloisons des « garages »
    M += [B(14.5, 303.2, 89.5, 304.0, 0, 10.5, "carbone"),                                      # fond d'ombre des bacs
          B(15.0, 302.8, 89.0, 303.1, 0.3, 0.6, "spot")]                                         # DEL de plinthe (chemin de nuit)
    for wx0 in (14.5, 40.5, 66.5):                                                              # 3 bacs-wagons de 23 po
        xc = wx0 + 11.5
        M += [A(wx0 + 0.2, LY0, wx0 + 22.8, 303.25, 1.6, 10.2, "placage", r=0.8, b=0.4),
              A(xc - 4, 301.88, xc + 4, 302.02, 7.2, 8.8, "carbone", r=0.7, b=0.1)]             # poignée découpée
    # matelas, couette, jeté, 2 oreillers, un coussin d'accent, l'ourson
    M += [A(12, 303, 92, 363, 12, 22, "draps", r=3, b=2.5),
          A(34, 302.6, 92.4, 363.4, 20.6, 23.2, "draps", r=2.5, b=1.8),
          A(70, 302.3, 92.7, 363.7, 22.8, 24.2, "tissu", r=2, b=1.0),
          A(14, 306, 31, 331.5, 21.5, 27.5, "draps", r=4, b=3), A(14, 334.5, 31, 360, 21.5, 27.5, "draps", r=4, b=3),
          A(30, 336, 34, 358, 22, 30, "art-argile", r=3, b=2)]
    M += [SPH(44, 350, 25.8, 3.4, "art-sable"), SPH(44, 350, 30.6, 2.5, "art-sable"),
          SPH(42.6, 350, 32.8, 0.9, "art-sable"), SPH(45.4, 350, 32.8, 0.9, "art-sable")]

    # ================================================================ C1-DOSSERET : panneau plein + tablette à 31½ po
    M += [B(LX0, LY1, LX1, YBA, 12, 30, "placage"),
          A(LX0, 363.4, LX1, YBA, 30, 31.5, "placage", r=0.8, b=0.4)]
    M += [C(22, 366.5, 1.6, 31.5, 32, "carbone"), SPH(22, 366.5, 34, 2.2, "abat-jour")]          # veilleuse
    M += [B(78 + 1.3 * k, 365.4, 79.1 + 1.3 * k, 368.6, 31.5, 31.5 + 7.5 - (k % 2), ["laque-marine", "art-sable", "blanc"][k])
          for k in range(3)]                                                                    # 3 livres du soir

    # ================================================================ C1-TETE : tête de lit en lattes (mur ouest), 1 liseuse
    M += [B(XW, LY0, XW + 0.3, LY1, 12, 46, "carbone")]
    y = LY0
    while y + 1.5 <= LY1 + 0.01:
        M.append(A(XW, y, XW + 1, y + 1.5, 12, 46, "placage", r=0.3, b=0.2))
        y += 2.0
    yl = 333.0
    M += [CX(XW, XW + 0.8, yl, 51, 1.8, "metal", pans=24),
          h.T([(XW + 0.8, yl, 51), (15.5, yl, 51), (17, yl, 50)], 0.3, "metal"),
          C(17, yl, 1.9, 46.6, 50.2, "metal", r2=1.0), C(17, yl, 1.6, 46.5, 46.65, "abat-jour")]

    # (canopée, rideau-cabane et niches éclairées : retirés — client, 2026-11-01)

    # ================================================================ C1-BANC : banquette des fenêtres, 4 grands tiroirs
    BX0, BX1, BY0 = 93.0, XE, 352.0
    M += [B(BX0 + 0.5, BY0 + 3, BX1, YBA, 0, 3, "carbone"),                                      # socle en retrait
          A(BX0, BY0, BX1, YBA, 3, 15, "placage", r=0.5, b=0.3),
          A(BX0 - 0.25, BY0 - 0.5, BX1, YBA, 15, 16, "placage", r=1, b=0.5)]                     # dessus arrondi à 16 po
    TX = [BX0 + k * (BX1 - 0.25 - BX0) / 4 for k in range(5)]                                  # 4 tiroirs de 36 po
    for a, b in zip(TX, TX[1:]):
        xc = (a + b) / 2
        M += [A(a + 0.2, BY0 - 0.7, b - 0.2, BY0 + 0.05, 3.6, 14.6, "placage", r=0.8, b=0.3),
              A(xc - 4, BY0 - 0.8, xc + 4, BY0 - 0.66, 12.0, 13.2, "carbone", r=0.5, b=0.1)]  # poignée découpée
    M += [A(BX0 + 0.6, BY0 - 0.2, 165.0, YBA - 0.2, 16, 18.5, "tissu", r=1.5, b=1.2),           # 2 coussins amovibles
          A(165.6, BY0 - 0.2, BX1 - 0.3, YBA - 0.2, 16, 18.5, "tissu", r=1.5, b=1.2)]
    M += [A(95, 364, 109, 368.6, 18.5, 31, "art-argile", r=3, b=2), A(222, 364.2, 236, 368.8, 18.5, 30, "laque-marine", r=3, b=2)]

    # (bibliothèques, valance, gare à jouets, mur à crémaillères et station du matin : retirés — client, 2026-11-01)

    # ================================================================ GARDE-ROBE intégrée (mur P05) : 134¼ × 24 po
    GY0, GY1 = YS, YS + 24.0                                                                    # face à y = 276,25
    GF = GY1 - 0.75                                                                             # plan des façades
    M += [B(XW, GY0, XR, GY1 - 3, 0, 4, "carbone")]                                             # coup-de-pied en retrait
    M += [B(XW, GY0, XR, GF - 0.2, 4, 96, "placage"), B(XW, GF - 0.2, XR, GF, 4, 96, "carbone")]  # caissons, fond d'ombre

    def porte(x0, x1, z0, z1, poignee):
        out = [A(x0 + 0.1, GF, x1 - 0.1, GY1, z0 + 0.1, z1 - 0.1, "placage", r=0.3, b=0.2)]
        xp = x1 - 1.6 if poignee == "d" else x0 + 0.6
        zp = min(max(z0 + 2, 40), z1 - 14)
        out.append(B(xp + 0.2, GY1 - 0.02, xp + 0.8, GY1 + 0.06, zp, zp + 9, "carbone"))         # poignée encastrée (gorge)
        return out

    # A : penderie évolutive (tringle à 36 po aujourd'hui, à 66 po plus tard), 2 portes de 21 po pleine hauteur
    M += porte(XW, 31.0, 4, 96, "d") + porte(31.0, 52.0, 4, 96, "g")
    # B : 4 tiroirs à sa hauteur (4 → 40 po), 2 portes au-dessus (les parents)
    for k in range(4):
        z0 = 4 + 9 * k
        M += [A(52.2, GF, 93.8, GY1, z0 + 0.15, z0 + 8.85, "placage", r=0.6, b=0.3),
              A(69, GY1 - 0.02, 77, GY1 + 0.12, z0 + 6.6, z0 + 7.8, "carbone", r=0.5, b=0.1)]
    M += porte(52.0, 73.0, 40, 96, "d") + porte(73.0, 94.0, 40, 96, "g")
    # C : rotation des jouets (tablettes et bacs derrière 2 portes pleine hauteur)
    M += porte(94.0, 119.125, 4, 96, "d") + porte(119.125, XR, 4, 96, "g")

    # ================================================================ C1-JEU : coin jeu au sol (tapis 5 × 8 pi)
    M += [A(117, 284, 213, 344, 0, 0.5, "tapis", r=2, b=0.2)]
    M += [C(202, 331, 9, 0.5, 9.5, "tissu", pans=36, r2=8.4)]                                    # pouf
    M += [A(130, 306, 142, 312, 2.0, 6.4, "art-argile", r=1, b=0.5), A(138, 306.4, 142.2, 311.6, 6.4, 9.6, "placage", r=0.8, b=0.4),
          CY(132.5, 305.4, 312.6, 1.9, 1.4, "carbone", pans=16), CY(139.5, 305.4, 312.6, 1.9, 1.4, "carbone", pans=16)]  # camion de bois
    M += [A(152 + (k % 2) * 0.5, 322, 156 + (k % 2) * 0.5, 326, 0.5 + 4 * k, 4.5 + 4 * k,
            ["placage", "laque-marine", "art-sable"][k], r=0.4, b=0.2) for k in range(3)]   # 3 blocs
    # un seul rebord à livres (couvertures de face) au mur est, à sa hauteur (dessus à 26 po)
    RX0 = XE - 4.5
    M += [B(RX0, 290, XE, 338, 25.25, 26, "placage"), A(RX0, 290, RX0 + 0.75, 338, 25.25, 28, "placage", r=0.3, b=0.15)]
    for k, (ya, c1, c2) in enumerate(((292.5, "laque-marine", "art-sable"), (304.5, "art-argile", "blanc"),
                                      (316.5, "osier", "laque-marine"), (327.0, "blanc", "art-argile"))):
        hh = 9.5 - (k % 2) * 1.5
        M += [B(XE - 1.6, ya, XE - 1.1, ya + 9, 26, 26 + hh, c1),
              B(XE - 1.7, ya + 1, XE - 1.6, ya + 8, 28, 24 + hh, c2)]                                 # illustration
    return M


VISITES = [
    {"nom": "Chambre 1 — vue d'entrée", "x": 230, "y": 274, "cap": 158},
    {"nom": "Chambre 1 — lit sur plateforme à bacs", "x": 150, "y": 300, "cap": 168},
    {"nom": "Chambre 1 — banquette des fenêtres", "x": 166, "y": 288, "cap": 92},
    {"nom": "Chambre 1 — coin jeu au sol", "x": 100, "y": 300, "cap": 12},
    {"nom": "Chambre 1 — garde-robe intégrée", "x": 214, "y": 342, "cap": 210},
]


def appliquer_scene(S, h):
    S["mobilier"][:] = [o for o in S["mobilier"] if not _dans_zone(o)] + _mobilier(h)
    # éclairage encastré : un au-dessus du coin jeu, un entre le lit et la garde-robe, un dans le recoin d'entrée
    S["lumieres"][:] = [l for l in S["lumieres"] if not (10 < l["x"] < 240 and 250 < l["y"] < 370)]
    S["lumieres"] += [{"x": 166, "y": 318}, {"x": 56, "y": 289, "i": 7}, {"x": 190, "y": 244, "i": 6}]
    v = S["visites"]
    i = next((k for k, s in enumerate(v) if s.get("nom") == "Chambre 1"), len(v))
    v[i:i + 1 if i < len(v) else i] = VISITES
    S["palette"].append(["Chambre 1 (4 ans)",
                         "« le socle de chêne », allégé : trois pièces de chêne et du plancher libre — lit-plateforme queen en "
                         "coin (matelas à 22 po, 3 bacs-wagons roulants, tête en lattes, tablette-dosseret), banquette des "
                         "fenêtres à 4 grands tiroirs (marche d'évacuation) devant le mur argile, garde-robe intégrée de 134 po "
                         "à portes pleines (penderie évolutive, tiroirs, rotation des jouets) ; au centre, coin jeu au sol "
                         "(tapis de laine 5 × 8, pouf, un rebord à livres)", "#C39A82"])
