"""MAISON-18 — RDC : la CHAMBRE AVANT devient le BUREAU (travail et gaming, deux postes côte à côte face à la fenêtre).

Demande du client (1) : « La chambre avant devient un bureau de travail et de gaming (2 stations assis), idéalement face à
la fenêtre qui a une vue vers le fleuve. »
Demande du client (2, 2026-11-02) : « pimp-moi le bureau de travail d'ordinateur avec des meubles ajustables, genre monter
descendre, pi rends-le plus beau aussi. » Et, pour toute la visite : « je veux que ça interagisse quand on y touche ».

Fenêtre « vers le fleuve » : la pièce n'a qu'UNE fenêtre, ouv-RDC-001 sur la façade avant (y = 5 ; 75 po, baie x 60,5 →
135,5 ; allège 37,5 po et tête 80 po d'après la vidéo DAG). Le mur de gauche (x = 5) n'a pas de fenêtre dans cette pièce
(ouv-RDC-006 est celle de la salle de bain). La façade regarde vers le sud-sud-est : c'est le côté du fleuve (HYPOTHÈSE).

Parti (2026-11-02) : DEUX BUREAUX ASSIS-DEBOUT électriques de 55 × 30 po, un par poste, face à la fenêtre (axes x = 57 et
114,5 ; 2½ po entre les plateaux ; dos à 3½ po du mur, devant la tablette de la fenêtre qui avance de 1¼ po).
Plateau de CHÊNE BLANC MASSIF HUILÉ de 1 po, coins arrondis, arêtes adoucies (le même chêne que les lattes et la crédence :
un seul bois dans la pièce ; le bois de grange reste la signature de la cuisine). Piètement noir mat à deux colonnes
télescopiques : pied en T et tube extérieur FIXES, tube intérieur, châssis et traverse qui MONTENT avec le plateau.
Manette (afficheur de hauteur, mémoires, verrou enfant) sous le bord avant droit. Assis : dessus à 29 po ; debout : 45 po
(course de 16 po). Montent aussi avec le plateau : écrans sur bras à pince (27 po droit devant, bas ; 24 po vertical sur le
côté extérieur), barre lumineuse d'écran et DEL de rétroéclairage, tour suspendue dans ses sangles, goulotte à câbles avec
parasurtenseur, brin mobile de la chaîne de câbles (chaîne à deux brins qui coulissent : le brin fixe part du plancher, vers
la prise double de chaque bureau). Tapis anti-fatigue glissé à moitié sous chaque bureau (on le tire du pied pour se lever).
Le reste de la pièce : mur de lattes de chêne sur feutre noir (gauche), mur arrière ardoise avec la crédence flottante et un
panneau acoustique imprimé (« le fleuve au crépuscule »), deux tablettes flottantes de chêne au mur de droite (DEL dessous),
grande sansevière dans le coin avant gauche, chaises ergonomiques anthracite, coin détente (fauteuil de cuir cognac, table
d'appoint, liseuse), toile solaire enroulée dans la fenêtre, tapis à poils ras.

Maquette : une COMMANDE INTERACTIVE par bureau (SCENE["commandes"] : « bureau_gauche », « bureau_droit », départ « bas » =
assis) ; toucher le bureau (plateau, écran, tour...) le monte ou le descend. Les objets mobiles portent "anim": "suivre" et
sont décrits à l'état « bas ». Le moteur translate un objet « suivre » de (pivot_z − z1)·(1 − f), z1 = haut de l'objet :
avec un pivot très haut (PIVOT) et fraction_min = 1 − COURSE / (PIVOT − dessus du plateau), tous les objets montent de
16 po (± 0,1 po), sans déformation, quel que soit leur haut.

On reste DANS la pièce : rien ici ne touche aux murs ni aux ouvertures. Pouces, repère de la maison.
"""
import math

PIECE = "piece-RDC-CH2"
NOM = "Bureau"

# --------------------------------------------------------------------------------------- repères de la pièce
XG, XD = 10.0, 143.75          # nu du mur gauche (extérieur, x = 5) ; nu de la cloison de droite (x = 146)
YF, YA = 10.0, 139.75          # nu de la façade (y = 5) ; nu de la cloison de la salle de bain (mur-RDC-R01, y = 142)
NICHE = (110.25, 139.75, 143.75, 154.75)     # renfoncement de la porte du dégagement (ouv-RDC-014, x 112 → 142)
FEN = (60.5, 135.5)            # baie de la fenêtre de façade ouv-RDC-001
ZONE = [(9.5, 9.5, 144.0, 140.4), (110.0, 139.5, 144.0, 155.0)]   # emprise : mobilier présumé de RDC-01 retiré
LAT = 11.1                     # face des lattes de chêne du mur gauche

# --------------------------------------------------------------------------------------- bureaux assis-debout
LB, PB = 55.0, 30.0                          # plateau : largeur et profondeur
YB0, YB1 = 13.5, 43.5                        # dos du plateau (3½ po du mur) et devant
YL = (YB0 + YB1) / 2                         # axe des colonnes (milieu de la profondeur)
ZP1 = 29.0                                   # dessus du plateau, ASSIS (état « bas » des données)
ZP0 = ZP1 - 1.0                              # dessous (chêne massif de 1 po)
COURSE = 16.0                                # debout : dessus à 45 po
BUREAUX = (  # id de la commande, x0, x1, côté extérieur (−1 : vers x = 10, +1 : vers x = 146), nom
    # « gauche » et « droit » : vus de la rue, comme le mur de gauche du projet ; de la porte du bureau, c'est l'inverse,
    # d'où des noms par repère visible (le mur de lattes, les tablettes)
    ("bureau_gauche", 29.5, 84.5, -1, "Bureau côté lattes"),
    ("bureau_droit", 87.0, 142.0, +1, "Bureau côté tablettes"))
POSTES = tuple((b[1] + b[2]) / 2 for b in BUREAUX)    # axes des postes : 57 et 114,5
RETRAIT = 5.5                                # axe des colonnes à 5½ po des bouts du plateau
ZT0 = 22.5                                   # haut du tube extérieur (fixe)
ZTR = ZP0 - 1.2                              # haut du tube intérieur, sous le bras du châssis
YCH = 61.0                                   # centre des chaises (bord avant de l'assise à 7 po du bureau)
ZE0, ZE1 = 32.0, 46.3                        # écran 27 po, assis : bas et haut (sous la hauteur des yeux)
YE = 21.5                                    # dos des écrans principaux
YM = 16.0                                    # mât des bras d'écran (pince sur le bord arrière)
CREDENCE = (60.0, 108.0, 121.75)             # crédence flottante : x0, x1, devant (dos au mur arrière)
TABLETTES = (46.0, 76.0, 8.0, (50.0, 64.0))  # tablettes du mur de droite : y0, y1, profondeur, dessus des deux tablettes
PIVOT = 10000.0                              # voir le docstring : translation uniforme des objets « suivre »
FRACTION_MIN = 1 - COURSE / (PIVOT - ZP1)


# =============================================================================================== plan (P-130)
def _dim(v, note=None):
    d = {"valeur": v, "source": "PROPOSÉ", "photo": None}
    if note:
        d["note"] = note
    return d


def _nom_bureau(cote):
    return (f"Bureau assis-debout électrique 55 × 30 po, poste {cote} : plateau de chêne blanc massif huilé, piètement "
            "noir mat à 2 colonnes télescopiques, dessus de 29 po (assis) à 45 po (debout) ; écrans sur bras, tour "
            "suspendue, goulotte et chaîne de câbles qui montent avec le plateau ; une prise double derrière")


LIB_BUREAU = "ASSIS- DEBOUT"     # « ASSIS-DEBOUT » coupé après le trait d'union : 2 lignes, lu DANS le symbole du bureau
ELEMENTS = [  # id, type, nom, libellé, x, y, rotation (dos vers −y à 0°), (longueur, largeur)
    ("elem-RDC-P-BUR-BUR1", "comptoir", _nom_bureau("1 (gauche)"), LIB_BUREAU, POSTES[0], YL, 0, (LB, PB)),
    ("elem-RDC-P-BUR-BUR2", "comptoir", _nom_bureau("2 (droite)"), LIB_BUREAU, POSTES[1], YL, 0, (LB, PB)),
    ("elem-RDC-P-BUR-CH1", "autre", "Chaise ergonomique, poste 1 (gauche)", "", POSTES[0], YCH, 180, (26, 26)),
    ("elem-RDC-P-BUR-CH2", "autre", "Chaise ergonomique, poste 2 (droite)", "", POSTES[1], YCH, 180, (26, 26)),
    ("elem-RDC-P-BUR-CRED", "armoires", "Crédence flottante de chêne 48 × 18 po (consoles, manettes, casques, jeux), DEL dessous ; "
     "panneau acoustique imprimé au-dessus", "", (CREDENCE[0] + CREDENCE[1]) / 2, (CREDENCE[2] + YA) / 2, 180,
     (CREDENCE[1] - CREDENCE[0], YA - CREDENCE[2])),
    ("elem-RDC-P-BUR-FAUT", "autre", "Fauteuil de détente en cuir cognac (coin détente), table d'appoint et liseuse", "",
     28.5, 118.5, 195, (26, 31)),
    ("elem-RDC-P-BUR-LATTES", "autre", "Mur de lattes de chêne acoustiques sur feutre noir (plancher au plafond)", "",
     XG + 0.6, (YF + YA) / 2, 90, (YA - YF, 1.2)),
    ("elem-RDC-P-BUR-TABL", "autre", "Deux tablettes flottantes de chêne 30 × 8 po au mur de droite (dessus à 50 et 64 po), "
     "ruban DEL sous la tablette du bas", "", XD - TABLETTES[2] / 2, (TABLETTES[0] + TABLETTES[1]) / 2, 90,
     (TABLETTES[1] - TABLETTES[0], TABLETTES[2])),
]


def _element(eid, typ, nom, lib, x, y, rot, LW):
    e = {"id": eid, "type": typ, "nom": nom, "nom_original": None, "etat": "nouveau",
         "position": {"x": round(x, 2), "y": round(y, 2), "rotation_deg": rot, "source": "PROPOSÉ"},
         "dimensions": {"longueur": _dim(LW[0]), "largeur": _dim(LW[1])},
         "note": "bureau-gaming de MAISON-18 (rdc_bureau.py) ; mobilier proposé, chambre avant non photographiée : à mesurer"}
    e["libelle"] = lib
    return e


def appliquer_modifs_rdc(maison, ctx):
    rdc = ctx["rdc"]
    for p in rdc["pieces"]:
        if p["id"] == PIECE:
            p["nom"] = NOM
            p["description"] = ("Bureau de travail et de gaming (ancienne chambre avant) : deux bureaux assis-debout "
                                "électriques face à la fenêtre de façade (vue vers le fleuve), coin détente.")
            xs = [q[0] for q in p["polygone"]]
            ys = [q[1] for q in p["polygone"]]
            if abs(min(xs) - XG) > 0.5 or abs(max(xs) - XD) > 0.5 or abs(min(ys) - YF) > 0.5:
                print(f"  [rdc_bureau] ATTENTION : la pièce {PIECE} a changé ({min(xs)}..{max(xs)} × {min(ys)}..{max(ys)}) ; "
                      "revoir les bureaux (prévus de x = 29,5 à 142)")
    rdc["elements"] = [e for e in rdc["elements"] if not e["id"].startswith("elem-RDC-P-BUR-")]
    rdc["elements"] += [_element(*t) for t in ELEMENTS]
    rdc["elements"].sort(key=lambda e: e["id"])
    rdc.setdefault("notes", []).append(
        {"id": "note-RDC-B01", "texte_original": None, "photo": None,
         "interpretation": "Bureau (ancienne chambre avant) : 2 bureaux assis-debout (29 → 45 po) face à la fenêtre de "
                           "façade, plateaux de chêne massif ; lattes acoustiques, crédence, tablettes, coin détente."})


# =============================================================================================== maquette 3D
def _centre(o):
    f = o.get("forme", "boite")
    if "pts" in o and f in ("boite", "tube"):
        pts = o["pts"]
        return sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
    if f in ("boite", "arrondi"):
        return (o["x0"] + o["x1"]) / 2, (o["y0"] + o["y1"]) / 2
    if f == "cylindre" and o.get("axe") == "y":
        return o["x"], (o["y0"] + o["y1"]) / 2
    if f == "cylindre" and o.get("axe") == "x":
        return (o["x0"] + o["x1"]) / 2, o["y"]
    return o.get("x", -1e9), o.get("y", -1e9)


def _dans_zone(x, y):
    return any(a <= x <= c and b <= y <= d for a, b, c, d in ZONE)


def _lier(objs, cid):
    """Objets qui montent avec le plateau du bureau cid (translation « suivre », décrits en position assise)."""
    for o in objs:
        o["commande"] = cid
        o["anim"] = "suivre"
    return objs


def _dalle(h, p0, u, larg, ep, z0, z1, mat, cote=1):
    """Plaque mince inclinée en plan : bord p0, direction u (unitaire), largeur larg, épaisseur ep vers l'arrière
    (normale −n, n = u tourné de 90° du côté « cote ») ; prisme de z0 à z1."""
    n = (-u[1] * cote, u[0] * cote)
    a = p0
    b = (p0[0] + u[0] * larg, p0[1] + u[1] * larg)
    c = (b[0] - n[0] * ep, b[1] - n[1] * ep)
    d = (a[0] - n[0] * ep, a[1] - n[1] * ep)
    pts = [a, b, c, d]
    # sens antihoraire pour l'extrusion
    s = sum(pts[i][0] * pts[(i + 1) % 4][1] - pts[(i + 1) % 4][0] * pts[i][1] for i in range(4))
    if s < 0:
        pts.reverse()
    return {"forme": "boite", "pts": [[round(x, 3), round(y, 3)] for x, y in pts], "z0": z0, "z1": z1, "mat": mat}


def _ecran27(h, xc):
    """Écran 27 po (24,4 × 14,3 po) droit devant, BAS, émission animée ; bras sur un mât à pince fixé au bord arrière du
    plateau ; barre lumineuse sur le dessus ; DEL de rétroéclairage au dos (lueur douce sur le mur, moins de fatigue)."""
    A, B, C, T, CX = h.A, h.B, h.C, h.T, h.CX
    return [A(xc - 12.2, YE, xc + 12.2, YE + 1.0, ZE0, ZE1, "carbone", r=0.25, b=0.15),
            {"forme": "ecran", "x": xc, "y": YE + 1.06, "z0": ZE0 + 0.5, "z1": ZE1 - 0.5, "larg": 23.6, "face": "+y"},
            B(xc - 2.2, YE - 0.6, xc + 2.2, YE, 37.0, 41.5, "metal"),                          # plaque VESA
            C(xc, YM, 0.75, ZP1, 47.5, "metal"), C(xc, YM, 1.9, ZP1, ZP1 + 0.45, "metal"),     # mât et semelle
            B(xc - 1.6, YB0 - 0.6, xc + 1.6, YB0, ZP0 - 1.6, ZP1 + 0.45, "metal"),            # pince : dos
            B(xc - 1.6, YB0 - 0.6, xc + 1.6, YM + 2.3, ZP0 - 1.6, ZP0 - 1.0, "metal"),        # pince : mâchoire
            T([(xc, YM, 41.0), (xc, 18.8, 40.4), (xc, YE - 0.6, 39.6)], 0.55, "metal", bouts=True),
            CX(xc - 9.0, xc + 9.0, YE + 0.75, ZE1 + 0.75, 0.5, "carbone"),                     # barre lumineuse
            B(xc - 1.0, YE - 0.2, xc + 1.0, YE + 1.3, ZE1 - 0.5, ZE1 + 0.4, "carbone"),
            B(xc - 11.4, YE - 0.15, xc + 11.4, YE, ZE1 - 1.1, ZE1 - 0.7, "abat-jour"),         # DEL au dos
            B(xc - 11.4, YE - 0.15, xc - 11.0, YE, ZE0 + 0.7, ZE1 - 0.7, "abat-jour"),
            B(xc + 11.0, YE - 0.15, xc + 11.4, YE, ZE0 + 0.7, ZE1 - 0.7, "abat-jour")]


def _ecran_vertical(h, xc, sens):
    """Écran 24 po vertical (12,6 × 21,4 po) sur le côté extérieur du poste (sens −1 : à gauche, +1 : à droite), pivoté
    de 28° vers l'usager ; interface sombre stylisée. Bras secondaire depuis le même mât."""
    T = h.T
    a = math.radians(28)
    u = (sens * math.cos(a), math.sin(a))
    p0 = (xc + sens * 12.9, YE + 0.6)
    cote = sens                                   # n = u tourné vers l'usager (face de l'écran)
    z0, z1 = ZE0, ZE0 + 21.4
    out = [_dalle(h, p0, u, 12.6, 0.8, z0, z1, "carbone", cote)]
    q0 = (p0[0] + u[0] * 0.45, p0[1] + u[1] * 0.45)
    n = (-u[1] * cote, u[0] * cote)
    q0 = (q0[0] + n[0] * 0.06, q0[1] + n[1] * 0.06)
    out.append(_dalle(h, q0, u, 11.7, 0.05, z0 + 0.5, z1 - 0.5, "ecran", cote))

    def ligne(d0, larg, za, zb, mat):
        p = (p0[0] + u[0] * d0 + n[0] * 0.11, p0[1] + u[1] * d0 + n[1] * 0.11)
        return _dalle(h, p, u, larg, 0.04, za, zb, mat, cote)
    out.append(ligne(1.0, 10.6, z1 - 2.6, z1 - 1.3, "jete"))
    for k, (d0, larg, mat) in enumerate(((1.0, 8.5, "gris"), (2.2, 7.8, "blanc"), (1.0, 9.2, "gris"),
                                         (2.2, 6.6, "blanc"), (1.0, 8.0, "gris"), (2.2, 5.4, "blanc"))):
        za = z1 - 4.6 - k * 2.4
        out.append(ligne(d0, larg, za, za + 0.5, mat))
    out.append(ligne(1.0, 10.6, z0 + 1.4, z0 + 2.3, "gris"))
    m = (p0[0] + u[0] * 6.3 - n[0] * 0.8, p0[1] + u[1] * 6.3 - n[1] * 0.8)
    out.append(T([(xc, YM, 42.5), ((xc + m[0]) / 2, YM + 1.8, 43.0), (m[0] - n[0] * 1.2, m[1] - n[1] * 1.2, 42.5)],
                 0.5, "metal", bouts=True))
    return out


def _poste(h, xc, sens):
    """Ce qui est posé sur le plateau d'un poste : écrans, sous-main de feutre, clavier, souris ; un carnet de cuir à
    gauche, une tasse à droite."""
    A, B, C, CX, TOR = h.A, h.B, h.C, h.CX, h.TOR
    out = _ecran27(h, xc) + _ecran_vertical(h, xc, sens)
    out += [A(xc - 16, 29.5, xc + 16, 41.5, ZP1, ZP1 + 0.15, "anthracite", r=1, b=0.05),
            A(xc - 8.5, 32.0, xc + 5.5, 36.8, ZP1 + 0.15, ZP1 + 1.0, "carbone", r=0.4, b=0.2),
            B(xc - 8.0, 32.4, xc + 5.0, 36.4, ZP1 + 1.0, ZP1 + 1.05, "gris"),
            A(xc + 9.5, 32.5, xc + 12.0, 36.6, ZP1 + 0.15, ZP1 + 1.4, "carbone", r=1.2, b=0.45)]
    if sens < 0:
        out += [A(xc - 23.5, 31.0, xc - 17.5, 39.0, ZP1, ZP1 + 0.55, "cuir", r=0.35, b=0.12),
                CX(xc - 23.0, xc - 18.0, 39.8, ZP1 + 0.25, 0.22, "laiton")]
    else:
        out += [C(xc + 20.0, 34.0, 1.6, ZP1, ZP1 + 3.8, "blanc"),
                TOR(xc + 21.6, 34.0, ZP1 + 2.0, 0.95, 0.25, "blanc")]
    return out


def _ordinateur(h, x0, vitre):
    """Tour (8,5 × 18 × 18,5 po) suspendue sous le plateau dans deux sangles d'acier noir, sous la traverse ; panneau vitré
    côté chaise, liseré DEL en façade."""
    A, B = h.A, h.B
    x1 = x0 + 8.5
    y0, y1 = 15.0, 33.0
    z1 = ZP0 - 2.2
    z0 = z1 - 18.5
    out = [A(x0, y0, x1, y1, z0, z1, "carbone", r=0.5, b=0.3)]
    xv = x1 if vitre > 0 else x0
    out += [B(min(xv, xv + vitre * 0.15), y0 + 1.0, max(xv, xv + vitre * 0.15), y1 - 1.0, z0 + 1.0, z1 - 1.0, "ecran"),
            B((x0 + x1) / 2 - 0.3, y1, (x0 + x1) / 2 + 0.3, y1 + 0.2, z0 + 2.5, z1 - 1.5, "abat-jour"),
            B((x0 + x1) / 2 - 0.6, y1, (x0 + x1) / 2 + 0.6, y1 + 0.2, z1 - 1.0, z1 - 0.4, "spot")]
    for y in (y0 + 2.0, y1 - 2.5):                 # sangles (hors de la traverse, y 27,5 → 29,5)
        out += [B(x0 - 0.4, y, x0, y + 1.2, z0 - 0.4, ZP0, "metal"), B(x1, y, x1 + 0.4, y + 1.2, z0 - 0.4, ZP0, "metal"),
                B(x0 - 0.4, y, x1 + 0.4, y + 1.2, z0 - 0.4, z0, "metal")]
    return out


def _bureau(h, x0, x1, sens):
    """Un bureau assis-debout, décrit ASSIS. Retourne (fixe, mobile) : pieds en T, patins, tubes extérieurs et brin fixe de
    la chaîne de câbles restent au sol ; tout le reste monte avec le plateau."""
    A, B, C, CX = h.A, h.B, h.C, h.CX
    xc = (x0 + x1) / 2
    xl0, xl1 = x0 + RETRAIT, x1 - RETRAIT
    fixe, mob = [], []
    for xl in (xl0, xl1):
        fixe += [A(xl - 1.3, YB0 + 1.5, xl + 1.3, YB1 - 1.5, 0.45, 1.75, "metal", r=0.6, b=0.35),    # pied en T
                 C(xl, YB0 + 2.4, 0.6, 0, 0.45, "carbone"), C(xl, YB1 - 2.4, 0.6, 0, 0.45, "carbone"),  # patins
                 A(xl - 1.25, YL - 1.85, xl + 1.25, YL + 1.85, 1.75, ZT0, "metal", r=0.3, b=0.12),      # tube extérieur
                 A(xl - 1.4, YL - 2.0, xl + 1.4, YL + 2.0, ZT0 - 0.6, ZT0, "carbone", r=0.4, b=0.15)]   # bague
        # tube intérieur : assez long pour rester engagé de 2 po dans le tube extérieur en position debout
        mob += [A(xl - 0.95, YL - 1.5, xl + 0.95, YL + 1.5, ZT0 - 2.0 - COURSE, ZTR, "metal", r=0.25, b=0.1),
                B(xl - 1.15, YB0 + 2.0, xl + 1.15, YB1 - 2.0, ZTR, ZP0, "metal")]                   # bras du châssis
    mob += [B(xl0 + 1.15, YL - 1.0, xl1 - 1.15, YL + 1.0, ZP0 - 1.8, ZP0, "metal"),                # traverse (moteurs)
            A(x0, YB0, x1, YB1, ZP0, ZP1, "placage", r=2.0, b=0.35)]                                # plateau de chêne
    # manette sous le bord avant droit : afficheur de hauteur, flèches, mémoires
    xk = x1 - 9.0
    mob += [A(xk - 3.0, YB1 - 3.2, xk + 3.0, YB1 - 0.4, ZP0 - 1.0, ZP0, "carbone", r=0.6, b=0.25),
            B(xk - 2.2, YB1 - 0.46, xk - 0.3, YB1 - 0.38, ZP0 - 0.75, ZP0 - 0.3, "abat-jour"),
            B(xk + 0.4, YB1 - 0.5, xk + 1.2, YB1 - 0.36, ZP0 - 0.8, ZP0 - 0.25, "gris"),
            B(xk + 1.5, YB1 - 0.5, xk + 2.3, YB1 - 0.36, ZP0 - 0.8, ZP0 - 0.25, "gris")]
    # tour suspendue côté extérieur, goulotte à câbles entre la tour et l'autre colonne
    if sens < 0:
        xpc = xl0 + 2.5
        xa, xb = xpc + 10.5, xl1 - 3.0
    else:
        xpc = xl1 - 2.5 - 8.5
        xa, xb = xl0 + 3.0, xpc - 2.0
    mob += _ordinateur(h, xpc, -sens)
    zg = ZP0 - 5.0
    mob += [B(xa, 14.3, xb, 19.3, zg, zg + 0.25, "metal"),
            B(xa, 19.0, xb, 19.3, zg, zg + 2.6, "metal"), B(xa, 14.3, xb, 14.6, zg, zg + 2.6, "metal"),
            B(xa, 14.3, xa + 0.35, 19.3, zg, ZP0, "metal"), B(xb - 0.35, 14.3, xb, 19.3, zg, ZP0, "metal"),
            A(xa + 3.0, 15.0, xa + 17.0, 17.4, zg + 0.25, zg + 1.6, "blanc", r=0.4, b=0.2),          # parasurtenseur
            CX(xa + 0.5, xb - 0.5, 18.1, zg + 0.85, 0.55, "carbone")]                                # faisceau de câbles
    # chaîne de câbles à deux brins : le brin fixe part du plancher, le brin mobile monte avec la goulotte
    xcc = xa + 2.0 if sens < 0 else xb - 2.0
    fixe += [A(xcc - 0.75, 15.0, xcc + 0.75, 16.3, 0.0, zg, "carbone", r=0.35, b=0.2)]
    fixe += [B(xcc - 0.9, 14.9, xcc + 0.9, 16.4, 1.5 + 2.4 * k, 1.8 + 2.4 * k, "gris") for k in range(9)]
    mob += [A(xcc - 0.75, 16.4, xcc + 0.75, 17.7, 0.4, zg, "carbone", r=0.35, b=0.2)]
    mob += [B(xcc - 0.9, 16.3, xcc + 0.9, 17.8, 2.7 + 4.8 * k, 3.0 + 4.8 * k, "gris") for k in range(4)]
    # au pied : les câbles filent au mur jusqu'à la prise double du bureau (sous l'allège)
    fixe += [B(xcc - 0.6, YF + 0.5, xcc + 0.6, 15.0, 0.0, 0.6, "carbone"),
             B(xcc - 0.35, YF + 0.5, xcc + 0.35, YF + 1.0, 0.6, 12.4, "carbone"),
             B(xcc - 1.5, YF, xcc + 1.5, YF + 0.25, 11.0, 15.6, "blanc"),
             B(xcc - 0.8, YF + 0.25, xcc + 0.8, YF + 1.3, 11.8, 13.6, "carbone")]
    return fixe, mob


def _chaise(h, xc, yc):
    """Chaise ergonomique (travail et jeu) qui regarde vers −y : piètement 5 branches à roulettes, assise à bord tombant et
    dossier de tissu anthracite en deux coussins (sans appui-tête : le dossier s'arrête à 44 po et laisse voir les bureaux
    et la fenêtre depuis la porte), appui lombaire, accoudoirs 4D réglables."""
    A, B, C, T = h.A, h.B, h.C, h.T
    out = []
    for k in range(5):
        a = math.radians(90 + 72 * k)
        px, py = xc + 12 * math.cos(a), yc + 12 * math.sin(a)
        out += [T([(xc, yc, 3.6), (px, py, 2.6)], 0.75, "carbone"), {"forme": "sphere", "x": px, "y": py, "z": 1.3, "r": 1.3, "mat": "carbone"}]
    out += [C(xc, yc, 2.0, 2.4, 4.4, "carbone"), C(xc, yc, 1.0, 4.4, 16.5, "metal"), C(xc, yc, 1.5, 4.4, 10, "carbone"),
            B(xc - 5, yc - 4, xc + 5, yc + 6, 16.2, 18.2, "carbone")]
    out += [A(xc - 10.25, yc - 10.5, xc + 10.25, yc + 9.0, 18.0, 21.4, "anthracite", r=3, b=1.2),            # assise
            B(xc - 1.2, yc + 8.0, xc + 1.2, yc + 13.0, 16.5, 19.0, "carbone"),
            B(xc - 1.2, yc + 12.0, xc + 1.2, yc + 13.6, 18.0, 30.0, "carbone"),                              # dosseret
            A(xc - 9.5, yc + 9.6, xc + 9.5, yc + 12.4, 22.5, 35.0, "anthracite", r=2.5, b=1.0),
            A(xc - 9.0, yc + 10.6, xc + 9.0, yc + 13.4, 34.5, 44.0, "anthracite", r=2.5, b=1.0),
            A(xc - 7.5, yc + 9.2, xc + 7.5, yc + 10.0, 25.0, 31.0, "carbone", r=1.5, b=0.3)]                # appui lombaire
    for s in (-1, 1):
        xa = xc + s * 11.2
        out += [B(xa - 0.7, yc - 1.0, xa + 0.7, yc + 2.0, 19.0, 26.0, "carbone"),
                B(xa - 0.5, yc + 1.0, xa + 0.5, yc + 6.0, 19.0, 20.0, "carbone"),
                A(xa - 1.6, yc - 6.0, xa + 1.6, yc + 4.0, 26.0, 27.4, "carbone", r=1.2, b=0.4)]
    return out


def _credence(h):
    """Crédence flottante de chêne (48 × 18 × 18 po, dessous à 9 po) : deux portes à poussoir (consoles, manettes,
    casques) et une niche ouverte (jeux, panier) ; ruban DEL sous le meuble. Dessus : 2 supports à casque, socle de
    recharge des manettes, sansevière."""
    A, B, C, TOR, CX = h.A, h.B, h.C, h.TOR, h.CX
    x0, x1, y0 = CREDENCE
    y1, z0, z1 = YA - 0.15, 9.0, 27.0
    xn = x1 - 16.0                                       # début de la niche ouverte
    out = [A(x0, y0, xn, y1, z0, z1, "placage", r=0.3, b=0.2)]
    out += [B(xn, y0, x1, y1, z0, z0 + 1.5, "placage"), B(xn, y0, x1, y1, z1 - 1.5, z1, "placage"),
            B(x1 - 1.0, y0, x1, y1, z0, z1, "placage"), B(xn, y1 - 1.0, x1, y1, z0, z1, "carbone"),
            B(xn, y0 + 0.5, x1 - 1.0, y1 - 1.0, 18.3, 19.1, "placage")]
    out += [B((x0 + xn) / 2 - 0.1, y0 - 0.1, (x0 + xn) / 2 + 0.1, y0, z0 + 0.4, z1 - 0.4, "carbone"),
            B(xn - 0.1, y0 - 0.1, xn + 0.1, y0, z0 + 0.4, z1 - 0.4, "carbone")]
    tons = ("carbone", "blanc", "rouge-velo", "jete", "carbone", "gris", "blanc", "osier", "carbone", "rouge-velo",
            "gris", "blanc", "jete", "carbone", "cuir", "blanc")
    for k, t in enumerate(tons):
        xa = xn + 0.6 + k * 0.62
        out.append(B(xa, y0 + 4.5, xa + 0.56, y0 + 11.5, z0 + 1.5, z0 + 1.5 + 6.7, t))
    out.append(A(xn + 1.0, y0 + 2.0, x1 - 2.0, y1 - 2.0, 19.1, 24.6, "osier", r=1.0, b=0.4, trou=0.6))
    out += [B(x0 + 2.0, y1 - 6.0, x1 - 2.0, y1 - 0.2, z0 - 1.2, z0, "noir-mat"),                  # rail d'appui au mur
            B(x0 + 2.0, y1 - 6.5, x1 - 2.0, y1 - 5.9, z0 - 0.9, z0 - 0.5, "abat-jour")]           # DEL sous la crédence
    for xs in (x0 + 7.0, x0 + 15.0):
        ys = (y0 + y1) / 2 + 1.0
        out += [C(xs, ys, 2.2, z1, z1 + 0.5, "metal"), C(xs, ys, 0.35, z1 + 0.5, z1 + 10.0, "metal"),
                B(xs - 1.6, ys - 0.5, xs + 1.6, ys + 0.5, z1 + 9.6, z1 + 10.2, "metal"),
                TOR(xs, ys, z1 + 7.0, 3.7, 0.55, "carbone", arc=math.pi),
                CX(xs - 4.5, xs - 3.0, ys, z1 + 6.0, 1.9, "carbone"), CX(xs + 3.0, xs + 4.5, ys, z1 + 6.0, 1.9, "carbone")]
    xd = x0 + 26.0
    out += [A(xd, y0 + 4.0, xd + 11.0, y0 + 9.0, z1, z1 + 1.0, "carbone", r=1.0, b=0.3),
            A(xd + 0.6, y0 + 4.6, xd + 5.0, y0 + 8.4, z1 + 1.0, z1 + 2.6, "blanc", r=1.5, b=0.6),
            A(xd + 6.0, y0 + 4.6, xd + 10.4, y0 + 8.4, z1 + 1.0, z1 + 2.6, "carbone", r=1.5, b=0.6)]
    out += [h.MOD("plante_sansevieria", x1 - 6.5, (y0 + y1) / 2, z=z1, H=20)]
    return out


def _tableau(h):
    """Panneau acoustique imprimé au-dessus de la crédence (44 × 30 po, cadre de chêne) : « le fleuve au crépuscule »,
    trois aplats (ciel sable, rive cognac, fleuve bleu ardoise), soleil et reflets ocre. Œuvre générique (aucune
    œuvre réelle reproduite) ; un vrai panneau imprimé sur feutre ou tissu tendu sur mousse, à choisir."""
    B, CY = h.B, h.CY
    xm = (CREDENCE[0] + CREDENCE[1]) / 2
    xa, xb, z0, z1 = xm - 22.0, xm + 22.0, 42.0, 72.0
    yc = YA - 1.6                                       # face de la toile
    out = [B(xa, yc - 0.25, xb, YA, z0, z0 + 0.9, "placage"), B(xa, yc - 0.25, xb, YA, z1 - 0.9, z1, "placage"),
           B(xa, yc - 0.25, xa + 0.9, YA, z0, z1, "placage"), B(xb - 0.9, yc - 0.25, xb, YA, z0, z1, "placage"),
           B(xa + 0.9, yc, xb - 0.9, YA, z0 + 0.9, z1 - 0.9, "feutre-sable")]
    yt = yc - 0.06
    zr = 53.5                                           # ligne de la rive sud
    out += [B(xa + 0.9, yt, xb - 0.9, yc, z0 + 0.9, zr, "bleu-fleuve"),
            B(xa + 0.9, yt, xb - 0.9, yc, zr, zr + 1.1, "cuir"),
            CY(xm + 8.0, yt - 0.04, yc, 61.0, 3.3, "ocre-soleil")]
    for k, (dl, za) in enumerate(((3.2, 51.0), (2.4, 48.9), (1.6, 46.9), (0.9, 45.0))):
        out.append(B(xm + 8.0 - dl, yt - 0.04, xm + 8.0 + dl, yc, za, za + 0.45 - 0.05 * k, "ocre-soleil"))
    return out


def _tablettes(h):
    """Deux tablettes flottantes de chêne (30 × 8 × 1½ po, supports cachés) au mur de droite, à côté du poste 2, hors de la
    circulation ; ruban DEL sous la tablette du bas. Quelques livres, un serre-livre de laiton, une plante retombante, un
    petit cadre."""
    A, B, C, MOD = h.A, h.B, h.C, h.MOD
    y0, y1, p, zs = TABLETTES
    x0 = XD - p
    out = [A(x0, y0, XD - 0.05, y1, z - 1.5, z, "placage", r=0.35, b=0.25) for z in zs]
    out.append(B(XD - 1.8, y0 + 1.0, XD - 1.1, y1 - 1.0, zs[0] - 1.65, zs[0] - 1.5, "abat-jour"))
    # tablette du bas : livres debout et serre-livre
    y, za = y0 + 2.0, zs[0]
    for ep, ht, mat in ((1.2, 9.0, "carbone"), (0.9, 8.2, "feutre-sable"), (1.5, 9.6, "ardoise-tableau"),
                        (1.0, 8.6, "blanc"), (0.8, 7.8, "cuir"), (1.3, 9.2, "jete"), (1.0, 8.4, "carbone")):
        out.append(B(XD - 7.0, y, XD - 1.2, y + ep, za, za + ht, mat))
        y += ep + 0.05
    out += [B(XD - 5.5, y + 0.1, XD - 2.5, y + 0.5, za, za + 5.0, "laiton"), B(XD - 5.5, y + 0.1, XD - 2.5, y + 3.0, za, za + 0.3, "laiton")]
    out.append(MOD("plante_syngonium", XD - 4.0, y1 - 6.0, z=za, H=10))
    # tablette du haut : petit cadre et pile de livres à plat
    zb = zs[1]
    out += [B(XD - 1.6, y0 + 4.0, XD - 0.9, y0 + 12.0, zb, zb + 10.0, "metal"),
            B(XD - 1.65, y0 + 4.8, XD - 1.6, y0 + 11.2, zb + 0.8, zb + 9.2, "feutre-sable"),
            B(XD - 7.0, y1 - 11.0, XD - 1.5, y1 - 3.0, zb, zb + 1.0, "carbone"),
            B(XD - 6.6, y1 - 10.6, XD - 1.8, y1 - 3.6, zb + 1.0, zb + 1.8, "blanc"),
            B(XD - 6.8, y1 - 10.8, XD - 1.6, y1 - 3.3, zb + 1.8, zb + 2.9, "cuir"),
            C(XD - 4.2, y1 - 7.0, 0.9, zb + 2.9, zb + 6.5, "laiton")]
    return out


def _lattes(h):
    """Mur gauche : panneaux de lattes de chêne (1,1 po, pas de 1,75 po) sur feutre noir, 94,5 po de haut."""
    B = h.B
    R = [B(XG, YF, XG + 0.35, YA, 0.75, 95.25, "feutre-noir")]
    M = []
    y = YF + 0.6
    while y + 1.1 <= YA - 0.3:
        M.append(B(XG + 0.35, y, LAT, y + 1.1, 0.75, 95.25, "placage"))
        y += 1.75
    return R, M


def _detente(h):
    MOD = h.MOD
    return [MOD("fauteuil_cuir", 29.0, 117.5, face="-y", rot=15),
            MOD("table_appoint", 50.5, 129.0, face="-y"),
            MOD("lampe_pied", 16.5, 133.0, face="-y", rot=35)]


def appliquer_scene_rdc(S, h):
    A, B = h.A, h.B
    # 1) retirer le mobilier présumé de RDC-01 (lit, chevets, commode) et sa lumière
    garder = lambda o: o.get("role") or o.get("ouverture") or not _dans_zone(*_centre(o))   # battants de portes : jamais
    S["mobilier"] = [o for o in S["mobilier"] if garder(o)]
    S["revetements"] = [o for o in S["revetements"] if garder(o)]
    S["lumieres"] = [l for l in S["lumieres"] if not _dans_zone(l["x"], l["y"])]
    # 2) couleurs : feutres, tissu, bleu du tableau (alias pour le mobilier), mur arrière ardoise
    S.setdefault("peintures", {}).update({
        "Anthracite": ["#2F3134", "tissu des chaises, sous-mains et tapis anti-fatigue (bureau du RDC)", "anthracite"],
        "Feutre sable": ["#B9A88B", "panneau acoustique imprimé du bureau (fond) — à choisir sur échantillon", "feutre-sable"],
        "Feutre noir": ["#1C1D1F", "feutre sous les lattes de chêne du bureau", "feutre-noir"],
        "Bleu fleuve": ["#3D5361", "fleuve du panneau imprimé du bureau (impression, pas une peinture)", "bleu-fleuve"],
        "Ocre soleil": ["#C98A3D", "soleil et reflets du panneau imprimé du bureau (impression)", "ocre-soleil"],
    })
    if "Ardoise" not in S["peintures"]:
        S["peintures"]["Ardoise"] = ["#2C302F", "mur arrière du bureau", "ardoise-tableau"]
    S.setdefault("accents", []).append({"piece": PIECE, "mur": "mur-RDC-R01", "peinture": "Ardoise"})
    # 3) mobilier : deux bureaux assis-debout (parties mobiles liées à leur commande), chaises, crédence, tableau,
    #    tablettes, coin détente, lattes
    M = []
    for (cid, x0, x1, sens, nom), xc in zip(BUREAUX, POSTES):
        fixe, mob = _bureau(h, x0, x1, sens)
        M += fixe + _lier(mob + _poste(h, xc, sens), cid)
    M += _chaise(h, POSTES[0], YCH) + _chaise(h, POSTES[1], YCH)
    M += _credence(h) + _tableau(h) + _tablettes(h) + _detente(h)
    R, lat = _lattes(h)
    M += lat
    # tapis à poils ras sous les chaises (roulettes) ; tapis anti-fatigue glissés à moitié sous les bureaux
    M += [A(33.0, 30.0, 140.0, 104.0, 0, 0.35, "tapis", r=1.5, b=0.12)]
    M += [A(xc - 15.0, 31.0, xc + 15.0, 50.0, 0.35, 1.1, "anthracite", r=2.5, b=0.35) for xc in POSTES]
    # toile solaire enroulée en haut de la fenêtre ; elle suit la tête de la fenêtre (80 po dans la vidéo DAG)
    dz = 82 - ((S.get("fenetres") or {}).get("ouv-RDC-001") or {}).get("tete", S.get("tete_fenetre", 82))
    M += [B(FEN[0] + 0.5, 6.3, FEN[1] - 0.5, 8.2, 77.6 - dz, 81.8 - dz, "gris"),
          B(FEN[0] + 1.0, 7.0, FEN[1] - 1.0, 7.3, 75.5 - dz, 77.6 - dz, "gris")]
    # grande sansevière dans le coin avant gauche, entre les lattes et le bureau de gauche
    M += [h.MOD("plante_sansevieria", 20.0, 24.0, z=0, H=36)]
    S["mobilier"] += M
    S["revetements"] += R
    # 4) éclairage : 2 encastrés à gradateur derrière les chaises, lueur douce derrière les écrans (DEL de
    #    rétroéclairage : les lumières de la maquette sont fixes, on les met à 50 po, entre l'écran assis et l'écran debout,
    #    à 10 po du mur pour ne pas y faire de point chaud), DEL sous les tablettes, liseuse du coin détente
    S["lumieres"] += [{"x": POSTES[0], "y": 94}, {"x": POSTES[1], "y": 94},
                      {"x": POSTES[0], "y": 20, "z": 50, "i": 0.6}, {"x": POSTES[1], "y": 20, "z": 50, "i": 0.6},
                      {"x": XD - 3, "y": 61, "z": 46, "i": 0.8}, {"x": 22, "y": 126, "z": 66, "i": 2.5}]
    # 5) commandes interactives : un bureau par commande, départ assis ; toucher le bureau le monte ou le descend
    S.setdefault("commandes", [])
    S["commandes"] = [c for c in S["commandes"] if c.get("id") not in [b[0] for b in BUREAUX]]
    for cid, x0, x1, sens, nom in BUREAUX:
        S["commandes"].append({"id": cid, "nom": nom + " (assis-debout)", "libelle_haut": "Monter le bureau",
                               "libelle_bas": "Descendre le bureau", "pivot_z": PIVOT,
                               "fraction_min": round(FRACTION_MIN, 10), "depart": "bas", "duree": 4.5})
    # 6) arrêts de visite (à la place de « Chambre avant (présumée) ») : le 2e montre les bureaux qui montent
    tous = {b[0]: "bas" for b in BUREAUX}
    arrets = [{"nom": "Bureau et gaming", "x": 128, "y": 134, "cap": 246, "commandes": dict(tous)},
              {"nom": "Bureau, postes debout", "x": 128, "y": 134, "cap": 246, "commandes": {k: "haut" for k in tous}},
              {"nom": "Bureau et gaming, coin détente", "x": 96, "y": 66, "cap": 120}]
    v = S.get("visites", [])
    i = next((k for k, a in enumerate(v) if "Chambre avant" in a.get("nom", "")), len(v))
    S["visites"] = v[:i] + arrets + [a for a in v[i:] if "Chambre avant" not in a.get("nom", "")]
    S.setdefault("palette", []).append(
        ["Bureau", "deux bureaux assis-debout (plateaux de chêne blanc massif huilé, piètement noir mat), lattes de chêne "
                   "acoustiques, mur ardoise, feutre sable, chaises anthracite, DEL blanc chaud 2700 K", "#B9A88B"])
