"""MAISON-18 — zone CHAMBRE 1 (le petit de 4 ans) : « La niche bleue ».

Demande du client (2026-11-02) : « Les chambres des enfants en bas, j'aime pas super ça, faut les refaire. » Après le
rangement « wow » (SS-17), le lit queen « pour que ça dure », puis « trop de meubles, exagère pas » et une version
allégée toute en chêne qui ne lui plaît pas non plus, on change de direction : une chambre d'enfant CHIC, CALME ET
CHALEUREUSE, qui grandira avec lui. Peu de pièces, des surfaces planes et propres :
- UN MUR DE RANGEMENT INTÉGRÉ pleine hauteur sur le mur ouest (fondation, sans fenêtre) : façades affleurantes peintes
  « bleu brume » (la seule couleur d'accent), ouverture par pression, aucune quincaillerie ; deux colonnes de 27 po
  (penderie évolutive ; jouets et livres en rotation) et un pont au-dessus du lit (les parents) ;
- LA NICHE DU LIT QUEEN creusée dans ce mur, doublée de chêne blanc (cadre de chant de ¾ po) : tête de lit rembourrée
  à canaux verticaux en lin, tablette de chêne, deux liseuses murales noir mat, DEL douce sous le pont ; le lit est un
  socle de chêne à 4 tiroirs sans poignée (2 par côté) ;
- LE BUREAU DU RECOIN : plateau de chêne de 52½ po glissé dans le recoin à gauche de la porte, sur crémaillères noires
  (22 po aujourd'hui, 29 po plus tard), un tiroir, une petite chaise de chêne et une lampe noire ;
- LE COIN LECTURE à la fenêtre est : un fauteuil de cuir cognac et une liseuse sur pied (un parent y lit avec lui) ;
- un grand tapis de laine 8 × 10 pi, une grande lanterne de papier au centre de la pièce (dans l'axe de la niche),
  des rideaux de lin plafond-plancher repliés entre les deux fenêtres. Murs et plafond blanc chaud ; béton poli.
Retirés de la version allégée : banquette des fenêtres, garde-robe de 134 po du mur de la salle de bain, rebord à
livres, pouf, jouets au sol ; le mur argile (accent) disparaît.

L'ancienne garde-robe de SS-16 (cloisons P12 et P13, portes coulissantes P07) reste fusionnée à la chambre ; la commode
SS-16 reste retirée. Pouces, repère de la maison. Faces des murs : ouest (fondation) x = 10 ; arrière (fondation)
y = 370 ; P05 (salle de bain) y = 252,25 ; P07 (chambre 2) x = 237,75 ; P06 (hall) y = 232,25 ; P04 (salle de bain /
recoin) x = 144,25. Fenêtres (mur arrière) : x 92-132 et 156-196, allège abaissée vers 40 po par un autre module :
rien de plus haut que le lit devant elles. Porte (P05) : x 201-231 sur P06, battant vers la chambre. Rien ne dépasse
x = 237,75.
"""
import math

# --------------------------------------------------------------------------------------------- repères de la pièce
XW, YB, YS, XE = 10.0, 370.0, 252.25, 237.75        # nu : mur ouest, mur arrière, mur P05, mur P07
YR, XR = 232.25, 144.25                              # recoin d'entrée : face de P06, face de P04
AIR = 0.5                                            # vide d'air derrière les caissons contre la fondation
XB = XW + AIR                                        # dos des caissons du mur de rangement
FX = XB + 24.0                                       # plan des façades (34,5)
FD = FX - 0.75                                       # dos des portes
COL = 27.0                                           # largeur d'une colonne
NY0, NY1 = YS + COL, YB - COL                        # baie de la niche (279,25 → 343,0 : 63¾ po)
LT = 0.75                                            # doublure de chêne de la niche
NC0, NC1 = NY0 + LT, NY1 - LT                        # niche finie (280,0 → 342,25 : 62¼ po)
YC = (NY0 + NY1) / 2                                 # axe de la niche et de la pièce (311,125)
ZP, ZN, ZH = 3.5, 74.0, 96.0                         # socle en retrait, dessous du pont, plafond
BX1 = 95.25                                          # pied du lit (socle)
LX, LY = 136.0, YC                                   # lanterne : centre de la pièce hors mur de rangement, axe de la niche
PEINT = "laque-bleu-brume"                           # alias de la peinture « Bleu brume » (mobilier peint)

# emprise de la zone (pour retirer le mobilier de SS-16) : chambre + ancienne garde-robe, et le recoin d'entrée
ZONE = [(9.5, 250.5, 240.0, 371.0), (142.0, 230.5, 240.0, 252.6)]

# ------------------------------------------------------------------------------------------------- plan (P-129)
RETIRER_MURS = {"mur-SS-P12", "mur-SS-P13"}          # cloisons de l'ancienne garde-robe
RETIRER_PORTES = {"ouv-SS-P07"}                      # ses portes coulissantes
RETIRER_PIECES = {"piece-SS-GR1"}                    # fusionnée à la chambre 1
RETIRER_EQUIP = {"elem-SS-P-COMMODE1"}               # commode SS-16 du mur est

EQUIPEMENTS = [  # id, type, nom, libellé, x, y, rotation, (longueur sur x, largeur sur y)
    ("elem-SS-P-C1-RGS", "armoires", "Mur de rangement intégré, colonne sud (27 × 24 po, pleine hauteur) : penderie "
     "évolutive (2 tringles à sa hauteur, puis une à 66 po) et tiroirs intérieurs ; façades peintes affleurantes, "
     "ouverture par pression", "", (XB + FX) / 2, (YS + NY0) / 2, 0, (24, COL)),
    ("elem-SS-P-C1-RGN", "armoires", "Mur de rangement intégré, colonne nord (27 × 24 po, pleine hauteur) : tablettes "
     "réglables, bacs de jouets en rotation et livres à sa hauteur ; façades peintes affleurantes, ouverture par pression",
     "", (XB + FX) / 2, (NY1 + YB) / 2, 0, (24, COL)),
    ("elem-SS-P-C1-LIT", "autre", "Lit queen dans la niche du mur de rangement (matelas 60 × 80, dessus à 22 po) : socle "
     "de chêne à 4 tiroirs sans poignée, tête rembourrée en lin et tablette, 2 liseuses ; pont de rangement au-dessus "
     "(74 → 96 po, les parents)", "LIT QUEEN", (XB + BX1) / 2, YC, 0, (BX1 - XB, NY1 - NY0)),
    ("elem-SS-P-C1-BUREAU", "comptoir", "Bureau du recoin : plateau de chêne de 52½ × 20 po sur crémaillères noires "
     "(22 po aujourd'hui, jusqu'à 29 po), un tiroir ; chaise d'enfant de chêne", "BUREAU", (XR + 0.25 + 197.0) / 2,
     (YR + YS) / 2, 0, (197.0 - XR - 0.25, YS - YR)),
    ("elem-SS-P-C1-LECTURE", "autre", "Coin lecture : fauteuil de cuir cognac et liseuse sur pied, à côté de la fenêtre "
     "est (pas devant)", "", 216.8, 347.0, 335, (26, 31.5)),
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
            p["description"] = ("Chambre 1 (enfant de 4 ans), « la niche bleue » : mur de rangement intégré pleine hauteur "
                                "sur le mur ouest (façades peintes affleurantes, sans quincaillerie) avec la niche du lit "
                                "queen doublée de chêne, bureau dans le recoin d'entrée, coin lecture à la fenêtre est, "
                                "grand tapis et lanterne centrale — proposition MAISON-18 (esquisse)")
    for o in ss["ouvertures"]:
        if o["id"] in ("ouv-SS-009", "ouv-SS-010"):
            o["note"] = ((o.get("note") or "") + " Fenêtre d'évacuation de la chambre 1 — doit OUVRIR (≥ 0,35 m², "
                         "aucune dimension < 380 mm) ; plancher libre devant (aucun meuble), rideaux repliés entre les "
                         "deux fenêtres ; allège abaissée (≈ 40 po) et puits à vérifier ; à valider avec la Ville et un "
                         "professionnel.").strip()


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


def _mur_rangement(h):
    """Mur de rangement pleine hauteur (façades peintes affleurantes, joints d'ombre) et niche doublée de chêne."""
    A, B = h.A, h.B
    M = []
    g = 0.12                                                                                    # demi-joint d'ombre
    for y0, y1 in ((YS, NY0), (NY1, YB)):                                                       # 2 colonnes de 27 po
        M += [B(XB, y0 + 0.05, FX - 3, y1 - 0.05, 0, ZP, "carbone"),                            # socle noir en retrait
              B(XB, y0 + 0.05, FD - 0.3, y1 - 0.05, ZP, ZH, PEINT),                             # caisson
              B(FD - 0.3, y0 + 0.05, FD, y1 - 0.05, ZP, ZH, "carbone"),                          # fond des joints
              B(FD, y0 + g, FX, y1 - g, ZP + g, ZN - g, PEINT, r=0.12),                          # porte basse (70 po)
              B(FD, y0 + g, FX, y1 - g, ZN + g, ZH - 0.2, PEINT, r=0.12)]                         # porte haute
    # pont au-dessus du lit : 2 portes relevables, même bande que les portes hautes des colonnes
    M += [B(XB, NY0, FD - 0.3, NY1, ZN, ZH, PEINT), B(FD - 0.3, NY0, FD, NY1, ZN, ZH, "carbone")]
    M += [B(FD, a + g, FX, b - g, ZN + g, ZH - 0.2, PEINT, r=0.12) for a, b in ((NY0, YC), (YC, NY1))]
    # doublure de chêne de la niche : dos, joues et plafond (leurs chants de ¾ po cadrent la baie)
    M += [B(XB, NC0, XB + LT, NC1, 0, ZN - LT, "placage"),
          B(XB, NY0, FX, NC0, ZP, ZN, "placage"), B(XB, NC1, FX, NY1, ZP, ZN, "placage"),
          B(XB, NY0, FX, NY1, ZN - LT, ZN, "placage")]
    M += [B(31.4, NC0 + 0.6, 32.4, NC1 - 0.6, ZN - LT - 0.25, ZN - LT, "spot")]                 # DEL douce sous le pont
    return M


def _lit(h):
    """Lit queen dans la niche : socle de chêne à 4 tiroirs, tête rembourrée à canaux, tablette, 2 liseuses, literie."""
    A, B, C, CX, SPH, T = h.A, h.B, h.C, h.CX, h.SPH, h.T
    M = []
    X0 = XB + LT                                                                                # 11,25 : dos de la niche
    M += [B(14.0, NC0 + 2.5, BX1 - 2.5, NC1 - 2.5, 0, ZP, "carbone"),                           # socle en retrait
          B(X0, NC0, BX1, NC1, ZP, 12, "placage", r=0.25)]                                      # caisse (dessus à 12)
    # 4 tiroirs sans poignée (gorge au chant du haut), 2 par côté, hors de la niche
    xs = [FX + 1.5, (FX + 1.5 + BX1 - 1.0) / 2, BX1 - 1.0]
    for yf, s in ((NC0, -1), (NC1, 1)):
        for a, b in zip(xs, xs[1:]):
            xc = (a + b) / 2
            M += [B(a + 0.2, min(yf, yf + 0.6 * s), b - 0.2, max(yf, yf + 0.6 * s), ZP + 0.4, 11.6, "placage", r=0.2),
                  B(xc - 5, min(yf + 0.55 * s, yf + 0.65 * s), xc + 5, max(yf + 0.55 * s, yf + 0.65 * s), 10.3, 11.0, "carbone")]
    # tête de lit : 6 canaux verticaux rembourrés (lin), tablette de chêne de 4½ po au-dessus
    w = (NC1 - NC0 - 0.2) / 6
    M += [A(X0, NC0 + 0.1 + k * w + 0.08, 14.5, NC0 + 0.1 + (k + 1) * w - 0.08, 12.3, 45.7, "tissu", r=1.4, b=1.1)
          for k in range(6)]
    M += [A(X0, NC0, 15.75, NC1, 45.8, 47.0, "placage", r=0.3, b=0.2)]
    M += [B(11.8, 287.5, 15.4, 295.5, 47.0, 47.8, "laque-marine"), B(12.0, 288.2, 15.2, 294.8, 47.8, 48.4, "draps")]  # 2 livres
    # 2 liseuses murales noir mat (bras articulé, tête conique), tournées vers les oreillers
    for y, s in ((NC0 + 7.0, 1), (NC1 - 7.0, -1)):
        yt = y + 3 * s
        M += [CX(X0, X0 + 1.0, y, 57, 1.9, "metal", pans=24),
              h.T([(X0 + 1.0, y, 57), (18.5, y, 57), (21, yt, 55.2)], 0.28, "metal"),
              C(21, yt, 1.7, 51.6, 55.2, "metal", r2=1.05, pans=24), C(21, yt, 1.3, 51.5, 51.65, "spot", pans=24)]
    # literie : matelas, couette repliée, jeté bleu brume au pied, 2 oreillers, un coussin de lin, l'ourson
    M += [A(14.75, NC0 + 1.1, 94.75, NC1 - 1.1, 12, 22, "draps", r=3, b=2.5),
          A(32, NC0 + 0.6, 95.2, NC1 - 0.6, 20.6, 23.4, "draps", r=2.5, b=1.8),
          A(32, NC0 + 0.5, 40, NC1 - 0.5, 23.2, 24.6, "draps", r=2, b=1.2),
          A(74, NC0 + 0.2, 95.6, NC1 - 0.2, 23.3, 24.5, PEINT, r=1.5, b=0.8),
          A(95.3, NC0 + 3, 96.3, NC1 - 3, 14.5, 24.3, PEINT, r=0.5, b=0.3),
          A(15.5, 284.5, 31, 309.5, 21.5, 27.5, "draps", r=4, b=3), A(15.5, 312.75, 31, 337.75, 21.5, 27.5, "draps", r=4, b=3),
          A(29, 299, 34, 323.25, 22.5, 30, "tissu", r=3, b=2)]
    M += [SPH(38, 331, 26.0, 3.6, "osier"), SPH(38, 331, 31.2, 2.6, "osier"),
          SPH(38, 329.4, 33.4, 0.95, "osier"), SPH(38, 332.6, 33.4, 0.95, "osier")]
    return M


def _bureau(h):
    """Bureau du recoin : plateau de chêne sur crémaillères noires, un tiroir, chaise d'enfant, lampe noire."""
    A, B, C, T = h.A, h.B, h.C, h.T
    M = [A(XR + 0.25, YR + 0.25, 197.0, YS, 20.5, 22.0, "placage", r=0.4, b=0.25)]
    for xs in (151.0, 190.5):
        M += [B(xs - 0.5, YR, xs + 0.5, YR + 0.45, 8, 34, "metal"),                              # crémaillère
              B(xs - 0.35, YR + 0.45, xs + 0.35, 248.5, 19.6, 20.5, "metal")]                     # console
    M += [A(158, 234, 184, 251.7, 17.8, 20.4, "placage", r=0.3, b=0.2),
          B(166, 251.65, 176, 251.78, 19.0, 19.6, "carbone")]                                     # tiroir, gorge
    M += [B(158, 236, 171, 245, 22.0, 22.35, "draps"), C(150.5, 237.5, 1.4, 22, 25.8, "placage", pans=20)]  # cahier, pot
    M += [C(190, 237.5, 2.6, 22.0, 22.7, "metal", pans=24),                                      # lampe noir mat
          T([(190, 237.5, 22.7), (190, 238.5, 36.5)], 0.3, "metal"),
          T([(190, 238.5, 36.5), (183.5, 241.5, 36.2)], 0.3, "metal"),
          C(183.5, 241.5, 2.3, 32.6, 35.9, "metal", r2=1.3, pans=24), C(183.5, 241.5, 1.9, 32.5, 32.65, "spot", pans=24)]
    # chaise d'enfant de chêne (assise à 12 po), tournée vers le bureau
    M += [A(162, 254.5, 176, 266.5, 11.0, 12.0, "placage", r=1, b=0.4)]
    M += [C(x, 255.6, 0.55, 0, 11, "placage", pans=12) for x in (163.1, 174.9)]
    M += [C(x, 265.4, 0.55, 0, 23.5, "placage", pans=12) for x in (163.1, 174.9)]
    M += [A(162.4, 264.9, 175.6, 266.1, 17.5, 23.5, "placage", r=0.5, b=0.3)]
    return M


def _ambiance(h):
    """Tapis, lanterne de papier, coin lecture, rideaux de lin."""
    A, B, C, MOD, SPH, TOR = h.A, h.B, h.C, h.MOD, h.SPH, h.TOR
    M = [A(60.0, YC - 48, 180.0, YC + 48, 0, 0.5, "tapis", r=1.5, b=0.2)]                       # tapis de laine 8 × 10 pi
    # grande lanterne de papier (30 po × 16½ po, nervures), semi-plafonnier : dessous à 77 po
    R, ec, zc = 15.0, 0.55, 85.25
    hz = R * ec
    M += [SPH(LX, LY, zc, R, "abat-jour", ecrase=ec)]
    M += [TOR(LX, LY, zc + dz, R * math.sqrt(1 - (dz / hz) ** 2) + 0.06, 0.13, "draps", axe="z")
          for dz in (-6.0, -3.0, 0.0, 3.0, 6.0)]
    M += [TOR(LX, LY, zc - hz + 0.4, 3.6, 0.18, "metal", axe="z"), TOR(LX, LY, zc + hz - 0.3, 2.8, 0.18, "metal", axe="z"),
          C(LX, LY, 0.18, zc + hz - 0.3, ZH - 0.6, "metal", pans=8), C(LX, LY, 2.4, ZH - 0.6, ZH, "metal", pans=24)]
    # coin lecture : fauteuil de cuir cognac tourné vers la pièce, liseuse sur pied à sa gauche
    M += [MOD("fauteuil_cuir", 216.8, 347.0, face="-y", rot=-25), MOD("lampe_pied", 232.0, 327.0, face="+y")]
    # rideaux de lin plafond-plancher sur rail noir, repliés entre les deux fenêtres (rien devant le vitrage)
    M += [B(89.0, 365.6, 199.0, 366.9, 94.8, 96.0, "metal")]
    for xa in (134.2, 145.2):
        M += [C(xa + 2.2 * k, 366.25 + (0.55 if k % 2 else -0.55), 1.3, 0.6, 94.8, "draps", pans=12) for k in range(5)]
    return M


VISITES = [
    {"nom": "Chambre 1 — la niche bleue", "x": 226, "y": 311, "cap": 180},
    {"nom": "Chambre 1 — coin lecture et bureau", "x": 100, "y": 360, "cap": 334},
    {"nom": "Chambre 1 — la niche de près", "x": 150, "y": 259, "cap": 160},
]


def appliquer_scene(S, h):
    S["mobilier"][:] = [o for o in S["mobilier"] if not _dans_zone(o)] + _mur_rangement(h) + _lit(h) + _bureau(h) + _ambiance(h)
    # peinture : la seule couleur d'accent est sur le mur de rangement (le mur argile de SS-16 disparaît)
    S["peintures"]["Bleu brume"] = ["#7F94A8", "mur de rangement et jeté de la chambre 1 (bleu-gris poudré, doux ; ≈ Farrow & "
                                    "Ball Selvedge n° 306, à valider sur échantillon), laque mate lavable", PEINT]
    S["accents"][:] = [a for a in S.get("accents", []) if a.get("piece") != "piece-SS-CH1"]
    if not any(a.get("peinture") == "Argile" for a in S["accents"]) and "Argile" not in S.get("peinture", {}).values():
        S["peintures"].pop("Argile", None)
    # éclairage : la lanterne, une lueur dans la niche, un encastré au-dessus du bureau, un près du coin lecture
    S["lumieres"][:] = [l for l in S["lumieres"] if not (10 < l["x"] < 240 and 232 < l["y"] < 370)]
    S["lumieres"] += [{"x": LX, "y": LY, "z": 93, "i": 8}, {"x": 22, "y": YC, "z": 80, "i": 2.5},
                      {"x": 171, "y": 244, "i": 6}, {"x": 200, "y": 300, "i": 6}]
    v = S["visites"]
    i = next((k for k, s in enumerate(v) if s.get("nom") == "Chambre 1"), len(v))
    v[i:i + 1 if i < len(v) else i] = VISITES
    S["palette"].append(["Chambre 1 (4 ans)",
                         "« la niche bleue » : mur de rangement pleine hauteur peint bleu brume (laque mate, façades "
                         "affleurantes, ouverture par pression) ; niche du lit queen doublée de chêne blanc, tête rembourrée "
                         "en lin à canaux, deux liseuses noir mat ; socle de chêne à 4 tiroirs ; bureau de chêne sur "
                         "crémaillères noires dans le recoin ; fauteuil de cuir cognac ; tapis de laine crème 8 × 10 ; "
                         "lanterne de papier ; rideaux de lin ; murs blanc chaud, béton poli", "#7F94A8"])
