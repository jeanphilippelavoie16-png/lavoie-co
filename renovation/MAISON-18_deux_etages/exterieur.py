"""MAISON-18 — l'extérieur : terrain en relief, enveloppe de la maison et cour arrière (plan DAG du 17-12-2025, vidéo DAG).

Données (le moteur les lit : generer_3d.preparer_exterieur ; on y marche dans la visite). Pouces, repère de la maison : x le
long de la façade (0 à 456 au nu extérieur ; vu de la rue, x augmente vers la droite), y vers l'arrière (façade 0, mur arrière
380), z vers le haut DEPUIS LE PLANCHER DU SOUS-SOL (le RDC est à 105).

Sources
- Plan « PLAN D'AMÉNAGEMENT — COUR ARRIÈRE », Design Action Gestion (DAG), 17-12-2025, 3/16" = 1'-0" (PNG 2550 × 1650 px à 150 ppp :
  2,34 px par pouce, mesuré sur la largeur de la maison, 38'-0" = 1067 px). Le dessin est tourné de 180° par
  rapport aux plans du dépôt : x_maison = 456 - (x_px - 625) / 2,34 ; y_maison = 380 + (y_px - 171) / 2,34 (171 = nu du mur
  arrière, 625 = coin arrière droit, x = 456). Contrôles : l'entrée arrière tombe à x 219-327 (relevé : 219-327), le palier fait
  129 × 60 (« ±10'-9" × 4'-11" »), le cabanon est à 3'-0" des lignes de lot, les lignes de lot recoupent le plan
  d'implantation de 1957 (P7) à 4 po près.
- Vidéo DAG « C-1329 Aménagement extérieur » : 12 captures nettes (2026-11-02, dag_01 à dag_12). On en suit l'allure : toit à deux
  versants avec pignons blancs en déclin vertical et pignon avant, fondation blanche lisse, terrain en pente (allée au niveau
  du sous-sol, talus en S devant), muret de blocs et marches de pierre, escalier ouvert, porte de garage du cabanon, salon de
  patio, feuillus. Écarts voulus : fenêtres et portes de NOTRE proposition, perron du relevé (DESIGN_exterieur.md).
- Réponses du client du 2026-11-02 : piscine de 21 pi à la position du plan (la vidéo en montrait une de 15 pi), clôture de bois
  de 6 pi sur les lignes de lot avec deux portillons, cabanon agrandi en garage de 13' × 17' (5 pi vers la maison, 3 pi vers la
  piscine).
- Demande du client du 2026-11-02 (aménager le garage : atelier, vélos suspendus, rangement de bacs, souffleuse) : garage.py,
  chargé ici (GARAGE_AMENAGE) ; programme et coûts dans DESIGN_garage.md.
- donnees/maison.json (murs extérieurs, ouvertures, cheminée, perron, entrée arrière), lu à l'import : les fenêtres et portes
  suivent les changements des autres modules (repli : les valeurs du relevé si le fichier manque).

CONTRAT (lu par le moteur) — EXTERIEUR = {
  "sol": 48,                 z de repli du terrain (terrain plat si "relief" manque) et niveau typique de la cour ;
  "relief": {"xs": [x croissants], "ys": [y croissants], "z": [[z(xs[i], ys[j]) pour i] pour j]}
                             terrain en relief : grille non uniforme (pas d'au plus 24 po, 12 près de la maison et de l'allée),
                             z ABSOLU ; chaque case en deux triangles (diagonale (xs[i], ys[j]) -> (xs[i+1], ys[j+1])) ; une case
                             dont le centre tombe dans un des "trous" n'est pas dessinée. Les arêtes de la maison et des trous
                             tombent sur des lignes de la grille. Elle couvre le lot et déborde (alentours dessinés, pas marchés) ;
  "revetements": [{"nom", "pts", "mat"}]  surfaces drapées sur le relief (asphalte, gravier, dalles) ; on y marche comme sur
                             le terrain ;
  "terrain": [[x, y], ...],  lignes de lot (polygone, sens horaire vu de dessus) : limites où l'on marche, lot du mini-plan ;
  "objets": [...],           objets (formes du moteur : boite, arrondi, cylindre, tube, sphere, tore ; "pts" = prisme vertical)
                             en z ABSOLU, posés sur le relief ; matériaux du catalogue ou alias de EXTERIEUR["peintures"] ;
  "planchers": [{"nom", "pts", "z"}],   surfaces où l'on marche au-dessus du terrain (palier, marches, patio, deck, pierres…),
                             z fixe = dessus ; une marche = un plancher ; jamais sous le relief ;
  "obstacles": [{"nom", "pts"}],        emprises où l'on ne passe pas (piscine, murs du garage, clôture, murets, garde-corps, mobilier…) ;
                             les murs de la maison bloquent d'office (sauf aux portes extérieures ouvertes), une marche de
                             plus de 8 po aussi ;
  "trous": [[[x, y], ...]],  où le terrain n'est pas dessiné : emprise de la maison (corps, entrée arrière, perron plein,
                             cheminée). Les margelles des fenêtres du sous-sol sont calculées par le moteur à partir du relief ;
  "visites": [{"nom", "x", "y", "cap", "z"}],  arrêts dehors (z = dessus du sol ou du plancher sous les pieds ; facultatif :
                                                sans lui, le plus haut plancher sous le point, sinon le terrain) ;
  "lumieres": [{"x", "y", "z", "i"}],   appliques (même format que les lumières d'étage, z absolu) ;
  "peintures": {nom: [couleur, description, alias]}  couleurs des alias employés par les objets ("ext-blanc"…) ;
  "palette": [[nom, description, couleur]]           (facultatif) matériaux de l'extérieur, section « Extérieur » de la liste }.

Aperçu : avec la variable d'environnement EXT_APERCU=1, des colonnes prismatiques (cases d'environ 24 po, dessus au relief,
couleur du gazon ou du revêtement) sont ajoutées aux objets pour voir le relief avec un moteur qui ne le dessine pas. Sans
EXT_APERCU, les données restent propres (le moteur dessine lui-même le relief et les revêtements).
"""
import json
import math
import os

ICI = os.path.dirname(os.path.abspath(__file__))

SOL = 48.0                 # niveau typique de la cour (et valeur plate de repli) : 8 po sous l'allège des fenêtres du sous-sol
Z_RDC = 105.0              # plancher du RDC (hauteur d'étage du sous-sol)
Z_TERRASSE = 97.5          # palier, patio et deck : une marche de 7½ po sous le seuil de la porte arrière (49½ po du sol)
Z_PERRON = 98.0            # dessus du perron avant (une marche sous le seuil)
SOFFITE = 202.0            # dessous des soffites (plafond du RDC à 201)
PENTE = 5 / 12             # toit à deux versants : fermes 5/12 (croquis P1 2016), pente confirmée par la vidéo (0,44)
DEBORD = 16                # débord de toit (soffite)

# GARAGE (le « cabanon » du plan DAG, agrandi le 2026-11-02 : 5 pi vers la maison, 3 pi vers la piscine) — constantes reprises
# par garage.py, qui aménage l'intérieur (établi, mur de bacs, vélos, souffleuse ; demande du client du 2026-11-02). Murs minces (obstacles), dalle où l'on marche (planchers), porte de garage OUVERTE.
CAB = (355, 621, 511, 825)       # murs, nu extérieur : 13' × 17' (156 × 204 po) ; avant (porte) du côté y0, vers la maison
CAB_TOIT = (343, 609, 523, 837)  # débord de toit de 12 po ; à 3'-0" des lignes de lot côté arrière et côté x = 560 (plan)
CAB_EP = 5.0                     # épaisseur des murs : planches verticales blanches 3/4 po + ossature 2 × 4 + contreplaqué 1/2 po
CAB_INT = (CAB[0] + CAB_EP, CAB[1] + CAB_EP, CAB[2] - CAB_EP, CAB[3] - CAB_EP)   # intérieur fini : 146 × 194 po (≈ 12'-2" × 16'-2")
CAB_Z_DALLE = 48.5               # dessus de la dalle de béton (gazon à 48 tout autour : au ras, comme dans la vidéo)
CAB_H_MURS = 96.0                # murs de 8 pi (dessus de la dalle au dessus des sablières)
CAB_Z_PLAFOND = CAB_Z_DALLE + CAB_H_MURS - 2     # dessous du plafond de contreplaqué (142,5 ; 7'-10" de haut)
CAB_PORTE = (385.0, 481.0, 84.0)                 # porte de garage 8' × 7' : x0, x1 (centrée sur le mur avant, y = 621), hauteur
CAB_Z_PANNEAU = CAB_Z_DALLE + CAB_PORTE[2] + 2   # dessous du panneau relevé sous le plafond (porte ouverte), de y 627 à 711

PEINTURES = {   # nom : [couleur à l'écran, description, alias employé par les objets]
    "Blanc extérieur": ["#F4F4F2", "fascias, soffites, rives, pignons en déclin vertical, jupe, limons, garage", "ext-blanc"],
    "Crépi blanc": ["#EEEDE8", "fondation apparente (crépi lisse)", "ext-crepi"],
    "Bardeau gris anthracite": ["#3F4245", "toit de la maison (bardeau d'asphalte)", "ext-bardeau"],
    "Bardeau du garage": ["#4E5154", "toit du garage", "ext-bardeau-cab"],
    "Asphalte": ["#1D1E20", "allée au niveau du sous-sol", "ext-asphalte"],
    "Gravier gris pâle": ["#9A9A96", "sous l'escalier du deck, autour de la piscine", "ext-gravier"],
    "Composite beige clair": ["#A88D69", "platelage et girons (palier, patio, deck, escalier)", "ext-composite"],
    "Joint de platelage": ["#6E604E", "joints entre les lames", "ext-joint"],
    "Bloc de béton gris pâle": ["#8E908C", "murets de soutènement", "ext-bloc"],
    "Couronnement de muret": ["#C3C4C0", "chaperon des murets", "ext-chaperon"],
    "Joint de bloc": ["#7E807C", "joints horizontaux des murets", "ext-joint-bloc"],
    "Pierre naturelle gris pâle": ["#A2A19B", "marches de pierre de l'allée à la cour", "ext-pierre"],
    "Toile de piscine": ["#5FA9CC", "fond de la piscine (eau turquoise)", "ext-toile"],
    "Gris piscine": ["#8C9090", "paroi de la piscine hors-terre", "ext-piscine"],
    "Margelle de piscine": ["#C9CBCA", "margelle de la piscine", "ext-margelle"],
    "Gris foncé": ["#5C5F63", "écumoire, vanne", "ext-gris"],
    "Blanc gris (appareils)": ["#D9DBD8", "thermopompe et filtre de la piscine", "ext-appareil"],
    "Gris BBQ": ["#3A3D3D", "caisson du BBQ", "ext-bbq"],
    "Résine tressée anthracite": ["#3A3B3C", "salon de patio modulaire", "ext-osier"],
    "Coussins blanc cassé": ["#D8D6D0", "coussins du salon de patio", "ext-coussin"],
    "Carreaux de porte": ["#C9CFD2", "carreaux de la porte de garage", "ext-carreau"],
    "Dalle blanche": ["#C8CBC8", "pas japonais (dalles blanc gris), dalle des appareils de la piscine", "ext-dalle"],
    "Bois de clôture": ["#8A6A48", "clôture d'intimité de 6 pi et portillons (planches sur planches teintes)", "ext-cloture"],
    "Contreplaqué": ["#C7A676", "intérieur des murs et plafond du garage", "ext-contreplaque"],
    "Feuillage": ["#4F6B3E", "feuillus", "ext-feuillage"],
    "Feuillage clair": ["#6A8748", "feuillus au soleil, arbre ornemental", "ext-feuillage-clair"],
    "Épinette": ["#3E5A3F", "pins, haie du voisin, arbustes", "ext-sapin"],
    "Écorce de bouleau": ["#E9E6DE", "troncs de bouleaux", "ext-bouleau"],
    "Gazon": ["#6E8A4E", "pelouse (aperçu du relief)", "ext-gazon"],
}


def _charger_garage():
    """garage.py (même dossier) : l'aménagement intérieur du garage, fusionné dans EXTERIEUR (objets, obstacles, lumières, arrêts,
    peintures, palette)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("m18_garage", os.path.join(ICI, "garage.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.amenagement(CAB, CAB_EP, CAB_Z_DALLE, CAB_Z_PLAFOND, CAB_PORTE, CAB_Z_PANNEAU)


GARAGE_AMENAGE = _charger_garage()
PEINTURES.update(GARAGE_AMENAGE["peintures"])


# ------------------------------------------------------------------------------------------------- formes du moteur
def B(x0, y0, x1, y1, z0, z1, mat):
    return {"forme": "boite", "x0": round(min(x0, x1), 2), "y0": round(min(y0, y1), 2), "x1": round(max(x0, x1), 2),
            "y1": round(max(y0, y1), 2), "z0": round(z0, 2), "z1": round(z1, 2), "mat": mat}


def P(pts, z0, z1, mat):                     # prisme vertical (polygone en plan)
    return {"forme": "boite", "pts": [[round(x, 2), round(y, 2)] for x, y in pts], "z0": round(z0, 2), "z1": round(z1, 2), "mat": mat}


def C(x, y, r, z0, z1, mat, **k):
    return dict({"forme": "cylindre", "x": x, "y": y, "r": r, "z0": round(z0, 2), "z1": round(z1, 2), "mat": mat}, **k)


def T(pts, r, mat, **k):
    return dict({"forme": "tube", "pts": [[round(v, 2) for v in p] for p in pts], "r": r, "mat": mat}, **k)


def SPH(x, y, z, r, mat, **k):
    return dict({"forme": "sphere", "x": round(x, 2), "y": round(y, 2), "z": round(z, 2), "r": r, "mat": mat}, **k)


def TOR(x, y, z, R, r, mat, **k):
    return dict({"forme": "tore", "x": x, "y": y, "z": z, "R": R, "r": r, "mat": mat}, **k)


def ARR(x0, y0, x1, y1, z0, z1, mat, r=2, b=0.6):     # boîte aux arêtes arrondies (coussins, bases tressées)
    return {"forme": "arrondi", "x0": x0, "y0": y0, "x1": x1, "y1": y1, "z0": round(z0, 2), "z1": round(z1, 2), "mat": mat, "r": r, "b": b}


def rect(x0, y0, x1, y1):
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]


def cercle(cx, cy, r, n=48):
    return [[round(cx + r * math.cos(2 * math.pi * i / n), 2), round(cy + r * math.sin(2 * math.pi * i / n), 2)] for i in range(n)]


# ------------------------------------------------------------------------------------------------- relevé (maison.json)
MURS_REPLI = {   # niveau : [(id, type, x1, y1, x2, y2, épaisseur)] — relevé R0 (si donnees/maison.json manque)
    "SS": [("mur-SS-001", "fondation", 5, 5, 451, 5, 10), ("mur-SS-002", "fondation", 451, 5, 451, 375, 10),
           ("mur-SS-003", "fondation", 451, 375, 5, 375, 10), ("mur-SS-004", "fondation", 5, 375, 5, 5, 10),
           ("mur-SS-005", "fondation", 224, 375, 224, 435, 10), ("mur-SS-006", "fondation", 224, 435, 322, 435, 10),
           ("mur-SS-007", "fondation", 322, 435, 322, 375, 10), ("mur-SS-008", "fondation", 165, 5, 165, -45, 6),
           ("mur-SS-009", "fondation", 165, -45, 231, -45, 6), ("mur-SS-010", "fondation", 231, -45, 231, 5, 6)],
    "RDC": [("mur-RDC-001", "ext", 5, 5, 451, 5, 10), ("mur-RDC-002", "ext", 451, 5, 451, 375, 10),
            ("mur-RDC-003", "ext", 5, 375, 451, 375, 10), ("mur-RDC-004", "ext", 5, 5, 5, 375, 10),
            ("mur-RDC-005", "ext", 224, 375, 224, 435, 10), ("mur-RDC-006", "ext", 224, 435, 322, 435, 10),
            ("mur-RDC-007", "ext", 322, 435, 322, 375, 10)],
}
OUV_REPLI = {    # niveau : [(mur, type, position depuis le 1er point, largeur)]
    "SS": [("mur-SS-001", "fenetre", 377, 75), ("mur-SS-002", "fenetre", 303, 80), ("mur-SS-002", "fenetre", 70, 36),
           ("mur-SS-002", "porte", 175, 36), ("mur-SS-004", "fenetre", 195, 36), ("mur-SS-004", "fenetre", 327, 36),
           ("mur-SS-003", "porte", 190, 30), ("mur-SS-003", "fenetre", 275, 40), ("mur-SS-003", "fenetre", 339, 40)],
    "RDC": [("mur-RDC-001", "fenetre", 93, 75), ("mur-RDC-001", "fenetre", 372, 108), ("mur-RDC-003", "fenetre", 93, 75),
            ("mur-RDC-003", "fenetre", 192, 36), ("mur-RDC-003", "fenetre", 370, 75), ("mur-RDC-004", "fenetre", 186, 36),
            ("mur-RDC-002", "fenetre", 175, 36), ("mur-RDC-006", "fenetre", 69, 42), ("mur-RDC-001", "porte", 194, 34),
            ("mur-RDC-003", "porte", 290, 32), ("mur-RDC-007", "porte", 26, 34)],
}


def releve():
    """{niveau: (murs extérieurs, ouvertures)} depuis donnees/maison.json (construit avant la maquette), sinon le repli.
    Ouverture : (mur, type, position, largeur, allège, hauteur, id) ; allège et hauteur None = valeurs de l'étage."""
    f = os.path.join(ICI, "donnees", "maison.json")
    out = {}
    try:
        M = json.load(open(f, encoding="utf-8"))
        for n in M["niveaux"]:
            if n["id"] not in ("SS", "RDC"):
                continue
            murs = [(m["id"], m["type"], m["x1"], m["y1"], m["x2"], m["y2"], (m.get("epaisseur") or {}).get("valeur") or 10)
                    for m in n["murs"] if m["type"] in ("fondation", "ext") and m.get("materiau") not in ("verre", "lattes")]
            ids = {m[0] for m in murs}
            val = lambda o, k: (o.get(k) or {}).get("valeur") if isinstance(o.get(k), dict) else None
            ouvs = [(o["mur_id"], o["type"], val(o, "position"), val(o, "largeur"), val(o, "allege"),
                     val(o, "hauteur") if o["type"] == "fenetre" else None, o.get("id"))
                    for o in n["ouvertures"] if o["mur_id"] in ids]
            out[n["id"]] = (murs, [o for o in ouvs if o[2] is not None and o[3] is not None])
    except (OSError, ValueError, KeyError):
        pass
    for nid in ("SS", "RDC"):
        out.setdefault(nid, (MURS_REPLI[nid], [o + (None, None, None) for o in OUV_REPLI[nid]]))
    return out


def _sections():
    """{id de fenêtre: (nombre de sections, fractions des meneaux inégaux ou None)} : fenetres_video.py (fenêtres aux dimensions
    de la vidéo, décision du client), pour que les meneaux vus de dehors soient ceux de l'intérieur ; {} s'il manque."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("m18_fenetres_video_ext", os.path.join(ICI, "fenetres_video.py"))
        fv = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fv)
        return {oid: (fv.retenu(oid)["sections"], f.get("meneaux")) for oid, f in fv.FENETRES.items()}
    except Exception:                       # module absent ou changé : meneaux également répartis selon la largeur
        return {}


RELEVE = releve()
SECTIONS = _sections()

# emprises (nu extérieur) : corps de la maison, entrée arrière (caveau dessous), excroissance sous le perron
CORPS, ENTREE_ARR, PERRON = (0, 0, 456, 380), (219, 380, 327, 440), (162, -48, 234, 0)
PERRON_PLEIN = (161, -49, 235, 0)          # dalle du perron (emprise pleine : trou du terrain)
CHEMINEE = (-20.3, 132.0, 0.0, 153.6)      # massif de maçonnerie hors du mur gauche (elem-SS-CHEM / elem-RDC-CHEM)
TROUS = [rect(*CORPS), rect(*ENTREE_ARR), rect(*PERRON_PLEIN), rect(*CHEMINEE)]


def _dans(x, y, rects):
    return any(a <= x <= c and b <= y <= d for a, b, c, d in rects)


# ------------------------------------------------------------------------------------------------- cour arrière (plan DAG + vidéo)
PALIER = (327, 380, 456, 440)              # ±10'-9" × 4'-11", contre le mur arrière, à côté de l'entrée arrière
ESC = (386, 440, 456, 494)                 # escalier de 5'-9½" de large, 6 girons de 9 po, 7 contremarches de 7,07 po
PATIO = (159, 440, 386, 560)               # ±19' × 10'
DECK = (159, 560, 314, 712)                # ±13' × 11'-9" (plan) ; il s'arrête sur la piscine (y 601 à gauche, 705 à droite)
# piscine hors-terre de 21' DIA. (plan DAG ; réponse du client du 2026-11-02) : centre, rayon hors tout (margelle comprise).
# Moindres carrés sur les trois cotes du plan (6'-2 5/8" du mur de l'ANCIEN cabanon, x = 391 ; 9'-10 3/8" de la ligne oblique ;
# 3'-4 1/4" de la ligne arrière) : (190,4 ; 724,1), écarts de 0,04 po au plus. Décalée de 2 po vers la ligne oblique pour garder
# 1 m (40,6 po) entre la paroi et le mur du garage agrandi (x = 355) : 9'-8 3/8" de la ligne oblique, 3'-4 3/8" de la ligne arrière.
PISC = (188.4, 724.1, 126.0)
GRAVIER_R = 138.0                          # anneau de gravier de 12 po autour de la piscine (plan)
# dalle des appareils de la piscine (thermopompe, filtre) 3' × 6', orientée comme au plan (« emplacement approx. ») : coin le plus
# proche à 41 po de la paroi (plus de 1 m, règlement) et à 3'-4" de la ligne arrière
APPAREILS = [(31.8, 782.1), (-3.2, 793.3), (22.0, 859.5), (55.3, 848.8)]
MURET_Y = (445, 380, 457, 548)             # muret de soutènement le long de l'allée (cour 48 / allée ≈ 3)
MURET_X = (500, 510, 572, 522)             # aile du muret le long de x, de la dernière pierre jusqu'au-delà de la ligne de lot
GRAVIER_ESC = (386, 440, 445, 526)         # gravier sous l'escalier et devant, bordure blanche au sud


def _dalle(cx, cy, a, l=36.0, p=24.0):     # dalle l × p centrée en (cx, cy), tournée de a degrés
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    return [(round(cx + c * u - s * v, 1), round(cy + s * u + c * v, 1)) for u, v in ((-l / 2, -p / 2), (l / 2, -p / 2), (l / 2, p / 2), (-l / 2, p / 2))]


# pas japonais (dalles 36 × 24 po du plan) : du haut des marches de pierre (portillon) jusqu'à la porte du garage, sans y entrer
DALLES = [_dalle(471.0, 568.0, -8), _dalle(446.0, 602.0, -4)]
CORDE_POTEAU = (-32.0, 770.0)              # poteau de la corde à linge, près de la ligne oblique : le fil reste à 4 pi de la paroi
PIERRES_Y0, PIERRES_GIRON, PIERRES_H = 452.0, 15.5, 7.5      # marches de pierre : début, giron, hauteur (6 marches)
# lignes de lot : arrière et côtés mesurés sur le plan DAG ; devant prolongé avec le plan d'implantation de 1957 (marge avant
# de 40', ligne droite ⟂ à la rue, façade du lot 57,23')
TERRAIN = [[560, -480], [560, 871], [-43, 903], [-128, -480]]


def _ligne_gauche(y):                       # ligne de lot oblique (côté x bas) de la cour, mesurée sur le plan DAG
    return -75.5 + (32.1 / 523.3) * (y - 380)


# ------------------------------------------------------------------------------------------------- relief (profil de niveaux)
# Niveaux lus sur la vidéo DAG (capture 03 calée par moindres carrés : seuil de la porte de côté à 0, bas de la brique à 97) ;
# tout ce qui n'est pas visible est à valider sur place (pente de la rue, bord du palier bas, niveau du fond de la cour).
ALLEE_Z = [(-480, -15.0), (0, -8.0), (180, -2.0), (380, 3.0)]   # dessus de l'asphalte le long du côté droit (z selon y)
TALUS = (282.0, 350.0)                     # crête et pied du talus en S devant la façade (01, 03)
PLATEAU, PALIER_BAS = 59.0, 16.5           # près de la façade : plateau à gauche, palier bas devant la partie droite
PLATEAU_RUE, PALIER_RUE = 34.0, 4.0        # à la ligne avant du lot (y = -480) : à valider sur place
BORD = 444.0                               # bord du palier bas sur l'allée (chute presque verticale jusqu'à x = 456)
Z_COULOIR = 3.0                            # bout de l'allée derrière la maison (niveau du sous-sol)
# côté gauche (le long du mur x = 0) : 58 au coin avant (vidéo), 52 devant les deux fenêtres du sous-sol (allège 56, pas de
# margelle dans notre proposition : 4 po de dégagement), 56 au coin arrière (vidéo 11) ; à valider sur place
COTE_GAUCHE = [(0, 58.0), (24, 52.0), (210, 52.0), (380, 56.0)]


def _lisse(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def _lin(pts, v):
    if v <= pts[0][0]:
        return pts[0][1]
    for (a, za), (b, zb) in zip(pts, pts[1:]):
        if v <= b:
            return za + (zb - za) * (v - a) / (b - a)
    return pts[-1][1]


def z_allee(y):
    return _lin(ALLEE_Z, y)


def _cote_droit(x, za):                    # au-delà de l'asphalte (x > 552) : bande de gazon, puis le voisin
    return za + 2 * min(1.0, max(0.0, (x - 552) / 8)) + 3 * min(1.0, max(0.0, (x - 560) / 12))


# --- avant : escalier du balcon avant (photos du client, 2026-11-02 ; balcon_avant.py dessine le balcon et l'escalier). Le balcon
# remplace le perron ; son escalier part du côté droit du balcon (x 232) et descend vers l'allée, parallèle à la façade, en 15
# contremarches jusqu'à l'asphalte (photos 13 à 16). Le client : « Les marches sont à 6 pieds du mur de la maison » : le côté de
# l'escalier le plus proche de la façade est à 6'-0" (y -72). Entre l'escalier et le mur, devant la fenêtre du sous-sol : la
# jardinière de cèdre en gradins (photo 16), posée sur l'asphalte. Le relief de la vidéo DAG est creusé (jamais remonté) : talus
# raide qui suit l'escalier, puis asphalte élargi devant la partie droite de la façade, de la rue jusqu'au mur (sous la
# jardinière et le long de son bout côté allée, photo 16). Le reste de l'avant (plateau sous le balcon et le coin des enfants,
# talus en S) reste celui de la vidéo DAG.
Z_BALCON = 103.5                           # dessus du balcon avant : 1½ po sous le seuil de la porte avant (105)
ESC_AV = (232.0, -120.0, 386.0, -72.0)     # escalier avant : x du haut (rive du balcon), y côté rue, x du pied, y côté maison
ESC_AV_N = 15                              # contremarches (14 girons de 11 po), dernière marche sur une dalle au pied
AIRE_AV = (380.0, -480.0, 456.0, -2.0)     # asphalte élargi devant la partie droite de la façade (rejoint l'allée à x = 456)
CREUX_PENTE = 0.62                         # pente des talus autour du creux (≈ 32°, talus raide des photos)
LIGNES_AVANT = ([ESC_AV[0], AIRE_AV[0], ESC_AV[2]], [AIRE_AV[3], ESC_AV[1] - 8, ESC_AV[1], ESC_AV[3], ESC_AV[3] + 8])


def _fond_escalier(x):
    """Plafond du terrain sous l'escalier avant : 12 po sous la ligne des nez de marche, jamais sous l'asphalte."""
    x0, ya, x1, yb = ESC_AV
    za = z_allee((ya + yb) / 2)
    t = min(max((x - x0) / (x1 - x0), 0.0), 1.0)
    return max(za, Z_BALCON + (za - Z_BALCON) * t - 12)


def _creux_avant(x, y):
    """Plafond du terrain près de l'escalier avant et de l'asphalte élargi : fond (asphalte ou sous l'escalier) au point le plus
    proche de la bande de l'escalier ou de l'aire d'asphalte, plus CREUX_PENTE fois la distance (talus tout autour)."""
    x0, ya, x1, yb = ESC_AV
    zones = [((x0, ya - 8, AIRE_AV[0], yb + 8), lambda px, py: _fond_escalier(px)),
             ((AIRE_AV[0], AIRE_AV[1], AIRE_AV[2], AIRE_AV[3]), lambda px, py: z_allee(py))]
    out = None
    for (a, b, c, d), fond in zones:
        px, py = min(max(x, a), c), min(max(y, b), d)
        z = fond(px, py) + CREUX_PENTE * math.hypot(x - px, y - py)
        out = z if out is None else min(out, z)
    return out


def _sol_avant(x, y):                      # devant la façade (y < 0) : relief de la vidéo DAG, creusé à l'escalier avant
    return min(_sol_avant_dag(x, y), _creux_avant(x, y))


def _sol_avant_dag(x, y):                  # devant la façade (y < 0), vidéo DAG
    t = _lisse((-60 - y) / 420)            # 0 près de la façade, 1 à la rue
    za = z_allee(max(y, -480))
    haut = PLATEAU + (PLATEAU_RUE - PLATEAU) * t
    bas = PALIER_BAS + (PALIER_RUE - PALIER_BAS) * t
    if x <= 0:
        return haut - 1
    if x < 60:
        return haut - 1 + x / 60
    if x <= TALUS[0]:
        return haut
    if x < TALUS[1]:                        # talus en S (convexe en haut, concave en bas)
        return haut + (bas - haut) * _lisse((x - TALUS[0]) / (TALUS[1] - TALUS[0]))
    if x <= BORD:
        return bas + 0.5 * (x - TALUS[1]) / (BORD - TALUS[1])
    if x < 456:                             # bord du palier bas : chute jusqu'à l'allée (talus raide ou bordure, à valider)
        return bas + 0.5 + (za - bas - 0.5) * (x - BORD) / (456 - BORD)
    if x <= 552:
        return za
    return _cote_droit(x, za)


def _sol_cour(x, y):
    """Derrière la maison (y > 380). L'assise de la piscine et son anneau de gravier sont nivelés à SOL (une piscine hors-terre
    se pose de niveau ; la paroi garde ainsi au moins 1,2 m partout), raccord doux sur 3 pi vers le terrain naturel."""
    z = _sol_cour_naturel(x, y)
    d = math.hypot(x - PISC[0], y - PISC[1])
    if d < GRAVIER_R + 36:
        z = SOL + (z - SOL) * _lisse((d - GRAVIER_R) / 36)
    return z


def _sol_cour_naturel(x, y):
    if x < 445:                             # cour à 48, monte doucement vers la ligne gauche (≈ 56 au coin arrière gauche)
        return SOL + 8 * _lisse((120 - x) / 120)
    if x < 456:                             # dans le muret le long de l'allée (marche du relief dans son épaisseur)
        return SOL
    bas = Z_COULOIR + (2 * min(1.0, (x - 505) / 55) if x > 505 else 0) + (3 * min(1.0, (x - 560) / 12) if x > 560 else 0)
    if x <= 505:                            # couloir d'asphalte, puis rampe sous les marches de pierre, puis la cour
        if y <= PIERRES_Y0:
            return Z_COULOIR
        if y < PIERRES_Y0 + 6 * PIERRES_GIRON + 3:
            return max(Z_COULOIR, min(SOL - 2, 0.5 + PIERRES_H * (y - PIERRES_Y0 - 3) / PIERRES_GIRON))
        return SOL
    if x <= MURET_X[2]:                     # gazon bas au nord de l'aile du muret, cour au sud
        return bas if y <= MURET_X[1] else SOL if y >= MURET_X[3] else bas + (SOL - bas) * (y - MURET_X[1]) / (MURET_X[3] - MURET_X[1])
    return bas + (SOL - bas) * _lisse((y - 470) / 90)        # chez le voisin : talus (à valider)


def _sol(x, y):
    """Terrain analytique (z absolu). Dans l'emprise de la maison (cases non dessinées), on reprend le terrain juste dehors,
    devant le mur le plus proche : les sommets posés sur les murs ont ainsi le niveau du dehors."""
    if 0 < x < 456 and 0 <= y <= 380:
        mur = min((y, "avant"), (380 - y, "arriere"), (x, "gauche"), (456 - x, "droit"))[1]
        x, y = {"avant": (x, -1e-6), "arriere": (x, 380 + 1e-6), "gauche": (0.0, y), "droit": (456.0, y)}[mur]
    if y < 0:
        return _sol_avant(x, y)
    if y <= 380:
        if x >= 456:
            za = z_allee(y)
            return za if x <= 552 else _cote_droit(x, za)
        return _lin(COTE_GAUCHE, y)
    return _sol_cour(x, y)


def _margelles_prevues():
    """Rectangles des margelles que le moteur fera (fenêtre du sous-sol dont l'allège tombe sous le relief + 2 po) : leurs bords
    deviennent des lignes de la grille. Même règle que generer_3d.margelles (saillie 36, débord 6, parois 1,5)."""
    murs, ouvs = RELEVE["SS"]
    par_id = {m[0]: m for m in murs}
    out = []
    for (mid, typ, c, w, allege, _, _) in ouvs:
        if typ != "fenetre" or mid not in par_id:
            continue
        _, _, x1, y1, x2, y2, t = par_id[mid]
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        horiz = abs(ux) > 0.5
        nx, ny = (0, math.copysign(1, y1 - 190)) if horiz else (math.copysign(1, x1 - 228), 0)
        px, py = x1 + ux * c + nx * (t / 2 + 6), y1 + uy * c + ny * (t / 2 + 6)
        if (allege if allege is not None else 56) >= _sol(px, py) + 2:
            continue
        a, b = c - w / 2 - 7.5, c + w / 2 + 7.5
        pa = (x1 + ux * a + nx * (t / 2 - 0.5), y1 + uy * a + ny * (t / 2 - 0.5))
        pb = (x1 + ux * b + nx * (t / 2 + 37.5), y1 + uy * b + ny * (t / 2 + 37.5))
        out.append((min(pa[0], pb[0]), min(pa[1], pb[1]), max(pa[0], pb[0]), max(pa[1], pb[1])))
    return out


def _lignes(requises, a, b, fine, pas_fin=12.0, pas=24.0):
    """Lignes de grille de a à b : les lignes requises, puis chaque intervalle subdivisé (pas_fin dans la zone fine)."""
    L = sorted({round(v, 2) for v in requises if a < v < b} | {a, b})
    out = [L[0]]
    for u, v in zip(L, L[1:]):
        p = pas_fin if fine[0] <= (u + v) / 2 <= fine[1] else pas
        n = max(1, math.ceil((v - u) / p - 1e-9))
        out += [round(u + (v - u) * k / n, 2) for k in range(1, n + 1)]
    return out


def _relief():
    mg = _margelles_prevues()
    ex = [-20.3, 0, 219, 327, 161, 235, 456, 159, 314, 386, BORD, 445, 450, 457, 500, 505, 552, 560, MURET_X[2], 120, 60,
          -128, -43, 282, 290.5, 299, 307.5, 316, 324.5, 333, 341.5, 350]
    ey = [-49, 0, 132, 153.6, 380, 440, -60, -480, 180, PIERRES_Y0, MURET_X[1], MURET_X[3], 532, 560, 494, 526,
          PIERRES_Y0 + 6 * PIERRES_GIRON + 3, 871, 903]
    for (a, b, c, d) in mg:
        ex += [a, c]
        ey += [b, d]
    ex, ey = ex + LIGNES_AVANT[0], ey + LIGNES_AVANT[1]      # escalier du balcon avant, asphalte élargi
    xs = _lignes(ex, -260.0, 720.0, (-60, 580))
    ys = _lignes(ey, -620.0, 1160.0, (-120, 560))
    return {"xs": xs, "ys": ys, "z": [[round(_sol(x, y), 2) for x in xs] for y in ys]}, mg


RELIEF, MARGELLES_PREVUES = _relief()


def _zg(x, y):
    """z du relief en (x, y) : les mêmes triangles que le moteur (generer_3d.fonction_relief) ; bornes recopiées au-delà."""
    import bisect
    xs, ys, Z = RELIEF["xs"], RELIEF["ys"], RELIEF["z"]
    x, y = min(max(x, xs[0]), xs[-1]), min(max(y, ys[0]), ys[-1])
    i = min(max(bisect.bisect_right(xs, x) - 1, 0), len(xs) - 2)
    j = min(max(bisect.bisect_right(ys, y) - 1, 0), len(ys) - 2)
    u, v = (x - xs[i]) / (xs[i + 1] - xs[i]), (y - ys[j]) / (ys[j + 1] - ys[j])
    z00, z10, z01, z11 = Z[j][i], Z[j][i + 1], Z[j + 1][i], Z[j + 1][i + 1]
    return z00 + u * (z10 - z00) + v * (z11 - z10) if u >= v else z00 + v * (z01 - z00) + u * (z11 - z01)


def _zmin(pts, n=6):
    """Plus bas du relief sur un segment ou un polygone (échantillonné)."""
    zs = []
    for (xa, ya), (xb, yb) in zip(pts, pts[1:] + pts[:1]):
        zs += [_zg(xa + (xb - xa) * k / n, ya + (yb - ya) * k / n) for k in range(n + 1)]
    return min(zs)


# ------------------------------------------------------------------------------------------------- enveloppe de la maison
def enveloppe():
    """Brique rouge sur le RDC (jusqu'au soffite ; sous l'appentis sur l'entrée arrière), crépi blanc lisse sur la fondation
    apparente jusqu'au relief, fenêtres noires vues de dehors (notre proposition), cadres de portes, cheminée."""
    out = []
    niveaux = {"SS": dict(emprise=[CORPS, ENTREE_ARR, PERRON], z1=97.0, mat="ext-crepi", fen=(56, 86), porte=(0, 80)),
               "RDC": dict(emprise=[CORPS, ENTREE_ARR], z0=97.0, z1=SOFFITE + 0.5, mat="brique_rouge",
                           fen=(Z_RDC + 34, Z_RDC + 82), porte=(Z_RDC, Z_RDC + 80))}
    for nid, cfg in niveaux.items():
        murs, ouvs = RELEVE[nid]
        for (mid, typ, x1, y1, x2, y2, t) in murs:
            L = math.hypot(x2 - x1, y2 - y1)
            if L < 1:
                continue
            ux, uy = (x2 - x1) / L, (y2 - y1) / L
            nx, ny = -uy, ux
            # normale vers l'extérieur : le côté où le plus de points (le long du mur) tombent hors de l'emprise
            cote = sum((0 if _dans(x1 + ux * L * s + nx * (t / 2 + 1), y1 + uy * L * s + ny * (t / 2 + 1), cfg["emprise"]) else 1)
                       - (0 if _dans(x1 + ux * L * s - nx * (t / 2 + 1), y1 + uy * L * s - ny * (t / 2 + 1), cfg["emprise"]) else 1)
                       for s in (0.1, 0.3, 0.5, 0.7, 0.9))
            if cote < 0:
                nx, ny = -nx, -ny
            f = t / 2                                      # nu extérieur, depuis l'axe

            def pt(a, d):
                return x1 + ux * a + nx * d, y1 + uy * a + ny * d

            def bx(a0, a1, d0, d1, z0, z1, mat):
                (xa, ya), (xb, yb) = pt(a0, d0), pt(a1, d1)
                return B(xa, ya, xb, yb, z0, z1, mat)
            # brique des murs de l'entrée arrière : sous le soffite de l'appentis (189), au-dessus de la tête de ouv-RDC-008
            z1m = (ZS_APPENTIS - 0.8) if (nid == "RDC" and max(y1, y2) > 400) else cfg["z1"]
            # parties du nu extérieur qui donnent dehors (pas contre l'entrée arrière ni dans le perron)
            pas = 1.0
            libres, a, debut = [], -f - 0.5, None
            while a <= L + f + 0.5 + 1e-6:
                x, y = pt(a, f + 0.8)
                dehors = not _dans(x, y, cfg["emprise"])
                if dehors and debut is None:
                    debut = a
                if (not dehors or a + pas > L + f + 0.5) and debut is not None:
                    libres.append((debut, a if not dehors else L + f + 0.5))
                    debut = None
                a += pas
            trous = []
            for (mur, typ_o, c, w, allege, haut, oid) in ouvs:
                if mur != mid:
                    continue
                z0o, z1o = cfg["fen"] if typ_o == "fenetre" else cfg["porte"]
                if typ_o == "fenetre" and allege is not None:      # allège et tête propres à la fenêtre (maison.json)
                    z0o = allege + (Z_RDC if nid == "RDC" else 0)
                    if haut:
                        z1o = z0o + haut
                trous.append((c - w / 2, c + w / 2, z0o, z1o, typ_o, oid, ux + uy))
            trous.sort()
            for (a0, a1) in libres:
                # bas du crépi : 4 po sous le plus bas du relief devant ce morceau de mur (le terrain coupe le reste)
                z0 = cfg["z0"] if "z0" in cfg else round(min(_zg(*pt(a0 + (a1 - a0) * k / 8, f + 1.5)) for k in range(9)) - 4, 1)
                coupe = [tr for tr in trous if tr[1] > a0 and tr[0] < a1]
                pos = a0
                for (o0, o1, z0o, z1o, *_) in coupe:
                    if o0 > pos:
                        out.append(bx(pos, o0, f - 0.5, f + 0.5, z0, z1m, cfg["mat"]))
                    if z0o > z0:
                        out.append(bx(max(o0, a0), min(o1, a1), f - 0.5, f + 0.5, z0, z0o, cfg["mat"]))
                    if z1o < z1m:
                        out.append(bx(max(o0, a0), min(o1, a1), f - 0.5, f + 0.5, z1o, z1m, cfg["mat"]))
                    pos = max(pos, o1)
                if pos < a1:
                    out.append(bx(pos, a1, f - 0.5, f + 0.5, z0, z1m, cfg["mat"]))
                # fenêtres (cadre noir, vitre, allège) et cadres de portes, vus de dehors
                for (o0, o1, z0o, z1o, typ_o, oid, sens) in coupe:
                    if typ_o == "fenetre":
                        k = 2.5
                        out += [bx(o0, o0 + k, f - 3, f + 0.2, z0o, z1o, "metal"), bx(o1 - k, o1, f - 3, f + 0.2, z0o, z1o, "metal"),
                                bx(o0, o1, f - 3, f + 0.2, z1o - k, z1o, "metal"), bx(o0, o1, f - 3, f + 0.2, z0o, z0o + k, "metal"),
                                bx(o0 + k, o1 - k, f - 2, f - 1.6, z0o + k, z1o - k, "vitre"),
                                bx(o0 - 1.5, o1 + 1.5, f - 0.5, f + 2.0, z0o - 2.5, z0o, "beton" if nid == "RDC" else "metal")]
                        n_sec, inegaux = SECTIONS.get(oid, (3 if o1 - o0 > 90 else (2 if o1 - o0 > 50 else 1), None))
                        fr = inegaux or [(j + 1) / n_sec for j in range(n_sec - 1)]
                        for q in fr:                       # fractions depuis le bout de plus petite coordonnée
                            am = o0 + (o1 - o0) * (q if sens > 0 else 1 - q)
                            out.append(bx(am - 1, am + 1, f - 2.6, f - 0.5, z0o + k, z1o - k, "metal"))
                    else:
                        zb = max(z0o, z0)
                        if z1o <= zb:
                            continue
                        out += [bx(o0 - 3, o0, f + 0.4, f + 1.4, zb, z1o + 3, "metal"),
                                bx(o1, o1 + 3, f + 0.4, f + 1.4, zb, z1o + 3, "metal"),
                                bx(o0, o1, f + 0.4, f + 1.4, z1o, z1o + 3, "metal")]
    # cheminée de brique hors du mur gauche (position du relevé, que la vidéo confirme), du sol jusqu'à 2 pi au-dessus du faîte
    # (294 + 24 = 318), chapeau de béton gris de 3 po
    x0, y0, x1, y1 = CHEMINEE
    zb = _zmin([(x0, y0), (x1, y0), (x1, y1), (x0, y1)]) - 4
    out += [B(x0, y0, x1 - 0.2, y1, zb, 318, "brique_rouge"), B(x0 - 1, y0 - 1, x1 + 0.8, y1 + 1, 318, 321, "beton")]
    return out


# ------------------------------------------------------------------------------------------------- toit
ZS_APPENTIS = 190.0        # sous-face de l'appentis de l'entrée arrière : au-dessus de ouv-RDC-008 et du cadre de la porte arrière (≈ 188)


def toit():
    """Toit à deux versants 5/12, faîte selon x (y 190, z 294), pignons blancs en déclin vertical aux deux bouts (le gauche est
    supposé), pignon avant transversal 5/12 au-dessus de la partie droite de la façade (x 154 à 472, sommet ≈ 276), appentis
    3/12 sur l'entrée arrière, fascias, soffites, rives et retours blancs, gouttières, évent noir. Le moteur n'a que des formes
    verticales : versants en rangs de 2 po (gradins de 4,8 po) ; les bouts des rangs sont blancs (pignons et rives)."""
    out = []
    h = 2.0
    d = h / PENTE                                  # 4,8 po de recul par rang
    X0, Y0, X1, Y1 = CORPS[0] - DEBORD, CORPS[1] - DEBORD, CORPS[2] + DEBORD, CORPS[3] + DEBORD
    ze = SOFFITE + 6                               # bord des versants (dessus du fascia)
    BA, W = "ext-bardeau", "ext-blanc"
    EX0, EX1, EY1 = ENTREE_ARR[0] - DEBORD, ENTREE_ARR[2] + DEBORD, ENTREE_ARR[3] + DEBORD    # appentis : 203-343 × 380-456
    # toit principal : rangs qui ne rétrécissent qu'en y ; bouts blancs (pignons, rives)
    k = 0
    while (Y1 - Y0) - 2 * k * d > 0.5:
        ya, yb, za, zb = Y0 + k * d, Y1 - k * d, ze + k * h, ze + (k + 1) * h
        out += [B(X0, ya, X1, yb, za, zb, BA), B(X0 - 0.6, ya, X0, yb, za, zb, W), B(X1, ya, X1 + 0.6, yb, za, zb, W)]
        k += 1
    faite = ze + k * h                             # 294
    yc = (Y0 + Y1) / 2
    out.append(B(X0, yc - 5, X1, yc + 5, faite - 1, faite + 0.8, BA))                    # faîtière
    # pignon avant (transversal) : rangs qui ne rétrécissent qu'en x, de la rive jusqu'au versant avant (noue) ; bout blanc
    PX0, PX1 = 154.0, X1
    k = 0
    while (PX1 - PX0) - 2 * k * d > 0.5:
        xa, xb, za, zb = PX0 + k * d, PX1 - k * d, ze + k * h, ze + (k + 1) * h
        out += [B(xa, Y0, xb, Y0 + k * d + 1, za, zb, BA), B(xa, Y0 - 0.6, xb, Y0, za, zb, W)]
        k += 1
    sommet = ze + k * h
    xm = (PX0 + PX1) / 2
    out.append(B(xm - 5, Y0, xm + 5, Y0 + (k - 1) * d + 1, sommet - 1, sommet + 0.8, BA))
    # déclin vertical des pignons : couvre-joints de 1,5 po tous les 16 po, sous une bande de rive de 7 po
    y = Y0 + 8
    while y < Y1 - 4:
        zr = ze + min(y - Y0, Y1 - y) * PENTE - 7
        if zr > ze + 4:
            out += [B(X0 - 1.2, y - 0.75, X0 - 0.6, y + 0.75, SOFFITE + 8, zr, W), B(X1 + 0.6, y - 0.75, X1 + 1.2, y + 0.75, SOFFITE + 8, zr, W)]
        y += 16
    x = PX0 + 8
    while x < PX1 - 4:
        zr = ze + min(x - PX0, PX1 - x) * PENTE - 7
        if zr > ze + 4:
            out.append(B(x - 0.75, Y0 - 1.2, x + 0.75, Y0 - 0.6, SOFFITE + 8, zr, W))
        x += 16
    # fascias (8 po), soffites, gouttières, retours de corniche en boîte aux pieds du pignon avant
    out += [B(X0, Y0 - 1, X1, Y0, SOFFITE, ze + h, W),                                    # avant (sous le pignon aussi)
            B(X0 - 1, Y0, X0, Y1, SOFFITE, ze, W), B(X1, Y0, X1 + 1, Y1, SOFFITE, ze, W),  # bas des pignons
            B(X0, Y1, EX0, Y1 + 1, SOFFITE, ze + h, W), B(EX1, Y1, X1, Y1 + 1, SOFFITE, ze + h, W)]   # arrière
    out += [B(X0, Y0, X1, 0, SOFFITE, SOFFITE + 1, W), B(X0, 0, 0, 380, SOFFITE, SOFFITE + 1, W), B(456, 0, X1, 380, SOFFITE, SOFFITE + 1, W),
            B(X0, 380, EX0, Y1, SOFFITE, SOFFITE + 1, W), B(EX1, 380, X1, Y1, SOFFITE, SOFFITE + 1, W)]
    out += [B(X0, Y0 - 5, PX0 - 4, Y0 - 1, SOFFITE + 1, ze - 1, W),                      # gouttières (avant gauche, arrière)
            B(X0, Y1 + 1, EX0, Y1 + 5, SOFFITE + 1, ze - 1, W), B(EX1, Y1 + 1, X1, Y1 + 5, SOFFITE + 1, ze - 1, W),
            B(PX0 - 6, Y0 - 3, PX0 + 18, 0, SOFFITE - 10, ze, W), B(456, Y0 - 3, X1 + 8, 0, SOFFITE - 10, ze, W)]   # retours
    # appentis 3/12 sur l'entrée arrière : prolonge le pan arrière plus bas, côtés en rives blanches (pas de croupe)
    he, de = 2.0, 8.0                              # 3/12
    ze_e = ZS_APPENTIS + 7                         # bord (dessus du fascia) 197
    out += [B(EX0, 376, EX1, EY1, ZS_APPENTIS, ze_e, BA), B(EX0 - 0.6, 376, EX0, EY1, ZS_APPENTIS, ze_e, W),
            B(EX1, 376, EX1 + 0.6, EY1, ZS_APPENTIS, ze_e, W), B(EX0, EY1, EX1, EY1 + 1, ZS_APPENTIS, ze_e + he, W)]
    k = 1
    while EY1 - k * de > 378:
        yb, za, zb = EY1 - k * de, ze_e + (k - 1) * he, ze_e + k * he
        out += [B(EX0, 376, EX1, yb, za, zb, BA), B(EX0 - 0.6, 376, EX0, yb, za, zb, W), B(EX1, 376, EX1 + 0.6, yb, za, zb, W)]
        k += 1
    out += [B(EX0, 380, ENTREE_ARR[0], EY1, ZS_APPENTIS - 1, ZS_APPENTIS, W), B(ENTREE_ARR[2], 380, EX1, EY1, ZS_APPENTIS - 1, ZS_APPENTIS, W),
            B(ENTREE_ARR[0], 440, ENTREE_ARR[2], EY1, ZS_APPENTIS - 1, ZS_APPENTIS, W),
            B(EX0, EY1 + 1, EX1, EY1 + 5, ZS_APPENTIS + 1, ze_e - 1, W)]                  # gouttière
    # évent noir près du faîte, sur le pan arrière, vers le milieu (vidéo 07, 09, 10)
    out += [B(226, 196, 238, 208, 282, 300, "metal"), B(224.5, 194.5, 239.5, 209.5, 300, 302, "metal")]
    return out


# ------------------------------------------------------------------------------------------------- perron avant (relevé)
def perron_avant():
    """Perron de béton du relevé devant la porte avant (sur l'excroissance du sous-sol), recalé sur le plateau : 5 contremarches
    d'environ 7,8 po (98 → plateau ≈ 59), 4 girons de 11 po vers la rue, garde-corps noirs. La vidéo ne le montre pas."""
    zp = _zg(198, -92)
    n = 5
    r = (Z_PERRON - zp) / n
    out = [B(*PERRON_PLEIN, 92, Z_PERRON, "beton")]
    for i in range(1, n):
        out.append(B(162, -48 - 11 * i, 234, -48, zp - 4, Z_PERRON - r * i, "beton"))
    for x in (163.5, 232.5):
        out += garde_corps_pente((x, 0), (x, -48), Z_PERRON, Z_PERRON, 36, Z_PERRON)
        out += garde_corps_pente((x, -48), (x, -48 - 11 * (n - 1)), Z_PERRON - r, zp + r, 36, zp)
    return out


def _marches_perron():
    zp = _zg(198, -92)
    r = (Z_PERRON - zp) / 5
    return [(i, rect(162, -48 - 11 * i, 234, -48 - 11 * (i - 1)), round(Z_PERRON - r * i, 2)) for i in range(1, 5)]


# ------------------------------------------------------------------------------------------------- garde-corps d'aluminium
def garde_corps(a, b, z, h):
    """Garde-corps d'aluminium noir horizontal de a à b (segment parallèle à x ou à y), plancher à z, hauteur h :
    poteaux (≤ 60 po), main courante, lisse basse, barreaux tous les 4¾ po."""
    (xa, ya), (xb, yb) = a, b
    L = math.hypot(xb - xa, yb - ya)
    ux, uy = (xb - xa) / L, (yb - ya) / L
    q = lambda s: (xa + ux * s, ya + uy * s)
    out = []

    def bar(s0, s1, e, z0, z1, mat="metal"):
        (p, r), (pp, rr) = q(s0), q(s1)
        if abs(ux) > 0.5:
            return B(p, r - e / 2, pp, rr + e / 2, z0, z1, mat)
        return B(p - e / 2, r, pp + e / 2, rr, z0, z1, mat)
    n = max(1, math.ceil(L / 60))
    poteaux = [L * i / n for i in range(n + 1)]
    for s in poteaux:
        s = min(max(s, 1.25), L - 1.25)
        out.append(bar(s - 1.25, s + 1.25, 2.5, z, z + h))
    for s0, s1 in zip(poteaux, poteaux[1:]):
        out += [bar(s0, s1, 2.5, z + h - 1.75, z + h), bar(s0, s1, 1.5, z + 2.5, z + 4)]
        m = max(1, round((s1 - s0) / 4.75))
        for j in range(1, m):
            s = s0 + (s1 - s0) * j / m
            out.append(bar(s - 0.375, s + 0.375, 0.75, z + 4, z + h - 1.75))
    return out


def garde_corps_pente(a, b, za, zb, h, z_bas):
    """Garde-corps d'escalier (barreaux) de a (haut, plancher za) à b (bas, nez de marche zb) : poteaux (le bas posé à z_bas),
    main courante en pente."""
    (xa, ya), (xb, yb) = a, b
    L = math.hypot(xb - xa, yb - ya)
    out = [B(xa - 1.25, ya - 1.25, xa + 1.25, ya + 1.25, za, za + h + 2, "metal"),
           B(xb - 1.25, yb - 1.25, xb + 1.25, yb + 1.25, min(z_bas, zb), zb + h + 2, "metal"),
           T([(xa, ya, za + h), (xb, yb, zb + h)], 1.1, "metal", pans=8), T([(xa, ya, za + 3.5), (xb, yb, zb + 3.5)], 0.7, "metal", pans=8)]
    m = max(1, round(L / 4.75))
    for j in range(1, m):
        t = j / m
        x, y, zz = xa + (xb - xa) * t, ya + (yb - ya) * t, za + (zb - za) * t
        out.append(B(x - 0.375, y - 0.375, x + 0.375, y + 0.375, zz + 3.5, zz + h, "metal"))
    return out


def verre_pur(Z):
    """Séparation patio / deck (y = 560) : verre pur 48 po sans cadre (3 panneaux sur pinces noires), portillon d'aluminium noir à
    barreaux (x 274-310) à ferme-porte, accroché au poteau du coin du BBQ (x 312)."""
    out = []
    for (a, b) in ((161, 197), (199, 235), (237, 272)):
        out.append(B(a, 559.75, b, 560.25, Z + 3, Z + 48, "verre-clair"))
        for xc in (a + (b - a) / 5, b - (b - a) / 5):
            out.append(B(xc - 1.25, 558.9, xc + 1.25, 561.1, Z, Z + 6, "metal"))
    out += [B(271.75, 558.75, 274.25, 561.25, Z, Z + 50, "metal"), B(310.75, 558.75, 313.25, 561.25, Z, Z + 50, "metal"),
            B(275, 559.2, 310, 560.8, Z + 3, Z + 4.5, "metal"), B(275, 559.2, 310, 560.8, Z + 44, Z + 45.5, "metal"),
            B(275, 559.2, 276.5, 560.8, Z + 3, Z + 45.5, "metal"), B(308.5, 559.2, 310, 560.8, Z + 3, Z + 45.5, "metal"),
            B(303, 558.4, 307, 559.2, Z + 37, Z + 41, "metal")]                         # ferme-porte
    m = round((308.5 - 276.5) / 4.75)
    for j in range(1, m):
        x = 276.5 + (308.5 - 276.5) * j / m
        out.append(B(x - 0.375, 559.625, x + 0.375, 560.375, Z + 4.5, Z + 44, "metal"))
    return out


def jupe(x0, y0, x1, y1, z0, z1):
    """Jupe blanche en déclin horizontal (planches de 6 po, ombre de 0,4 po) sur une face mince (x0 = x1 ou y0 = y1 ± épaisseur)."""
    out, z, i = [], z0, 0
    while z < z1 - 0.1:
        e = 0.4 if i % 2 else 0.0
        zz = min(z + 6, z1)
        if x1 - x0 < y1 - y0:
            out.append(B(x0 - e / 2, y0, x1 + e / 2, y1, z, zz, "ext-blanc"))
        else:
            out.append(B(x0, y0 - e / 2, x1, y1 + e / 2, z, zz, "ext-blanc"))
        z, i = zz, i + 1
    return out


# ------------------------------------------------------------------------------------------------- cour arrière
def _bout_deck(x):
    """y où le deck s'arrête sur la piscine au droit de x (DECK[3] si le cercle n'atteint pas x)."""
    cx, cy, R = PISC
    dx = abs(x - cx)
    if dx >= R + 1:
        return DECK[3]
    return min(DECK[3], cy - math.sqrt((R + 1) ** 2 - dx ** 2))


def _deck_pts():
    from shapely.geometry import Point, Polygon
    g = Polygon(rect(*DECK)).difference(Point(PISC[0], PISC[1]).buffer(PISC[2] + 1, 24))
    if g.geom_type != "Polygon":
        g = max(g.geoms, key=lambda q: q.area)
    return [[round(x, 2), round(y, 2)] for x, y in list(g.exterior.coords)[:-1]]


def _pierre(cx, cy, a, b, k, n=12):
    """Dalle de pierre naturelle : contour arrondi presque rectangulaire (superellipse), un peu irrégulier."""
    pts = []
    for j in range(n):
        t = 2 * math.pi * j / n + 0.25 * k
        c, s = math.cos(t), math.sin(t)
        f = 1 + 0.06 * math.sin(3 * t + 1.7 * k) + 0.035 * math.cos(5 * t + k)
        pts.append((cx + a * f * math.copysign(abs(c) ** 0.55, c), cy + b * f * math.copysign(abs(s) ** 0.55, s)))
    return pts


def _pierres():
    """6 marches de grosses dalles de pierre, du bout de l'allée (≈ 3) à la cour (48), sens +y : (polygone, dessus)."""
    out = []
    for i in range(1, 7):
        y0 = PIERRES_Y0 + PIERRES_GIRON * (i - 1)
        cy = y0 + (PIERRES_GIRON + 3) / 2
        out.append((_pierre(481 + (1.5 if i % 2 else -1.5), cy, 22 + (i % 3 - 1), (PIERRES_GIRON + 3) / 2, i),
                    round(Z_COULOIR + PIERRES_H * i, 2)))
    return out


def _joints_platelage(Z, deck_pts):
    """Joints sombres entre les lames de composite (lames selon x, tous les 5¾ po), coupés par la piscine."""
    from shapely.geometry import LineString, Polygon
    from shapely.ops import unary_union
    U = unary_union([Polygon(rect(*PALIER)), Polygon(rect(*PATIO)), Polygon(deck_pts)])
    out, y = [], PALIER[1] + 5.75
    while y < DECK[3] - 1:
        g = U.intersection(LineString([(100, y), (500, y)]))
        for s in (g.geoms if hasattr(g, "geoms") else [g]):
            if s.geom_type == "LineString" and s.length > 2:
                (xa, _), (xb, _) = s.coords[0], s.coords[-1]
                out.append(B(min(xa, xb) + 0.3, y - 0.18, max(xa, xb) - 0.3, y + 0.18, Z - 0.3, Z + 0.08, "ext-joint"))
        y += 5.75
    return out


def cour():
    out, Z = [], Z_TERRASSE
    r_esc = (Z - SOL) / 7
    CO, W = "ext-composite", "ext-blanc"
    # palier, patio, deck : platelage composite beige clair, joints, jupe blanche en déclin
    deck_pts = _deck_pts()
    out += [B(*PALIER, Z - 1.5, Z, CO), B(*PATIO, Z - 1.5, Z, CO), P(deck_pts, Z - 1.5, Z, CO)]
    out += _joints_platelage(Z, deck_pts)
    out += jupe(455.5, 380, 456, 440, SOL + 2, Z - 1.5)                    # palier, côté allée (au-dessus du muret)
    out += jupe(159, 440, 159.5, 560, SOL, Z - 1.5) + jupe(159, 440, 219, 440.5, SOL, Z - 1.5)
    out += jupe(314, 559.5, 386, 560, SOL, Z - 1.5) + jupe(385.5, 440, 386, 560, SOL, Z - 1.5)   # coin du BBQ (vu sous l'escalier)
    yd, yg = _bout_deck(314), _bout_deck(159)
    out += jupe(313.5, 560, 314, yd, SOL, Z - 1.5) + jupe(159, 560, 159.5, yg, SOL, Z - 1.5)
    # escalier ouvert vers la cour : girons de composite (nez de 1 po), trois limons blancs crantés, pas de contremarches
    for i in range(1, 7):
        y = ESC[1] + 9 * (i - 1)
        zt = Z - r_esc * i
        out.append(B(ESC[0], y - 1, ESC[2], y + 9, zt - 1, zt, CO))
        for xl in (387.25, 420.75, 453.75):
            out.append(B(xl - 0.75, y, xl + 0.75, y + 9, zt - 11, zt - 1, W))
    # garde-corps (couleurs du plan DAG) : vert = barreaux 36 po, rouge = barreaux 48 po, bleu = verre pur 48 po
    out += garde_corps((454.75, 380), (454.75, 440), Z, 36)                                        # vert, palier
    out += garde_corps_pente((454.75, 440), (454.75, 494), Z - r_esc, SOL + r_esc, 36, SOL + 2)   # vert, escalier
    out += garde_corps((386, 440), (386, 560), Z, 36)                                              # vert, patio / escalier
    out += garde_corps((386, 558.75), (314, 558.75), Z, 36)                                        # vert
    out += garde_corps((219, 441.25), (159, 441.25), Z, 36)                                        # vert, devant le mur
    out += garde_corps((160.25, 440), (160.25, 560), Z, 36)                                        # vert
    out += verre_pur(Z)                                                                            # bleu + portillon
    out += garde_corps((312.75, 560), (312.75, yd - 1), Z, 48)                                    # rouge
    out += garde_corps((160.25, 560), (160.25, yg - 1), Z, 48)                                    # rouge
    # piscine hors-terre 21' : paroi grise lisse, margelle gris pâle, eau turquoise, écumoire du côté des appareils (gravier :
    # revêtement ; assise nivelée à SOL)
    cx, cy, R = PISC
    zp = _zmin(cercle(cx, cy, R, 16))
    ae = math.radians(150)                                  # écumoire : vers la dalle des appareils
    xe, ye = cx + (R - 1) * math.cos(ae), cy + (R - 1) * math.sin(ae)
    out += [C(cx, cy, R, zp - 1, 98.5, "ext-piscine", pans=72), C(cx, cy, R - 2.5, 98.5, 98.7, "ext-toile", pans=72),
            C(cx, cy, R - 2.5, 98.7, 99.2, "eau", pans=72), TOR(cx, cy, 100.5, R - 1, 2.6, "ext-margelle", axe="z"),
            B(xe - 4, ye - 4, xe + 4, ye + 4, 88, 98.5, "ext-gris")]
    out += appareils_piscine()
    # murets de soutènement en blocs gris pâle (cour 48 / allée ≈ 3), couronnement clair, joints sur la face côté allée
    for (x0, y0, x1, y1) in (MURET_Y, MURET_X):
        out += [B(x0, y0, x1, y1, Z_COULOIR - 4, SOL, "ext-bloc"), B(x0 - 0.75, y0 - 0.75, x1 + 0.75, y1 + 0.75, SOL, SOL + 2, "ext-chaperon")]
    for zj in (11, 19, 27, 35, 43):
        out += [B(MURET_Y[2], MURET_Y[1], MURET_Y[2] + 0.3, MURET_Y[3], zj, zj + 0.5, "ext-joint-bloc"),
                B(MURET_X[0], MURET_X[1] - 0.3, MURET_X[2], MURET_X[1], zj, zj + 0.5, "ext-joint-bloc")]
    # sous l'escalier ouvert, côté allée : jupe blanche du dessus du muret (50) au dessous de chaque giron, comme sous le palier
    # (sinon un enfant passe sous la main courante et sort de la cour par le muret)
    for i in range(1, 7):
        y = ESC[1] + 9 * (i - 1)
        out += jupe(455.5, y, 456, y + 9, SOL + 2, Z - r_esc * i - 1)
    # marches de pierre de l'allée à la cour, bordure blanche du gravier
    out += [P(p, Z_COULOIR - 3, z, "ext-pierre") for p, z in _pierres()]
    out.append(B(GRAVIER_ESC[0], GRAVIER_ESC[3], GRAVIER_ESC[2], GRAVIER_ESC[3] + 4, SOL - 1, SOL + 1, W))
    out += garage()
    out += mobilier_patio()
    return out


def appareils_piscine():
    """Thermopompe et filtre au sable sur une dalle de 3' × 6' (APPAREILS, position du plan), à plus de 1 m de la paroi."""
    (ax, ay), (bx, by), (qx, qy), (dx, dy) = APPAREILS
    ux, uy = (qx - bx) / math.dist((bx, by), (qx, qy)), (qy - by) / math.dist((bx, by), (qx, qy))   # grand axe
    vx, vy = uy, -ux                                                                                 # petit axe
    mx, my = sum(p[0] for p in APPAREILS) / 4, sum(p[1] for p in APPAREILS) / 4
    zb = _zmin(APPAREILS) - 2
    zd = max(_zg(x, y) for x, y in APPAREILS) + 1.5
    def carre(cx, cy, a, b):                     # rectangle a (grand axe) × b (petit axe) centré en (cx, cy)
        return [(cx + ux * i * a / 2 + vx * j * b / 2, cy + uy * i * a / 2 + vy * j * b / 2) for i, j in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    tx, ty = mx - ux * 17, my - uy * 17          # thermopompe 30 × 30 × 32, grille du ventilateur sur le dessus
    fx, fy = mx + ux * 18, my + uy * 18          # filtre au sable et pompe
    return [P(APPAREILS, zb, zd, "ext-dalle"), P(carre(tx, ty, 30, 30), zd, zd + 32, "ext-appareil"),
            C(round(tx, 2), round(ty, 2), 11, zd + 32, zd + 33, "metal", pans=24),
            C(round(fx, 2), round(fy, 2), 12, zd, zd + 29, "ext-appareil", pans=24), C(round(fx, 2), round(fy, 2), 4, zd + 29, zd + 35, "ext-gris", pans=12),
            P(carre(fx - vx * 15, fy - vy * 15, 12, 8), zd, zd + 9, "ext-gris")]


def garage():
    """Garage 13' × 17' (le cabanon du plan DAG agrandi, réponse du client du 2026-11-02) : même style que le cabanon de la vidéo,
    planches verticales blanches à couvre-joints, toit à deux versants 7/12 (faîte selon y, pignon vers la maison), débord 12 po,
    rives, gouttières et retours blancs ; porte de garage noire de 8' × 7' à 8 carreaux centrée sur le mur avant, dessinée OUVERTE
    (panneau relevé sous le plafond, sur ses rails). On y entre : murs minces (parement blanc dehors, contreplaqué dedans), plafond
    de contreplaqué, dalle de béton au ras du gazon. Constantes en tête du module (CAB, CAB_Z_DALLE, CAB_H_MURS, CAB_PORTE…).
    L'intérieur aménagé (souffleuse, établi, mur de bacs, vélos, luminaires DEL) vient de garage.py (GARAGE_AMENAGE)."""
    x0, y0, x1, y1 = CAB
    e, zs = CAB_EP, CAB_Z_DALLE
    zm = zs + CAB_H_MURS                             # haut des murs
    pa, pb, hp = CAB_PORTE
    zh = zs + hp                                     # tête de la porte
    W, CP = "ext-blanc", "ext-contreplaque"
    zsol = _zmin([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
    out = [B(x0 - 2, y0 - 2, x1 + 2, y1 + 2, min(zsol, zs - 0.5) - 4, zs, "beton")]          # dalle (débord de 2 po)
    # murs minces : parement blanc de 3/4 po dehors, âme en contreplaqué dedans (on ne voit pas de blanc à l'intérieur)
    k = 0.75
    out += [B(x0, y0, pa, y0 + k, zs, zm, W), B(pb, y0, x1, y0 + k, zs, zm, W), B(pa, y0, pb, y0 + k, zh, zm, W),   # avant
            B(x0, y1 - k, x1, y1, zs, zm, W), B(x0, y0, x0 + k, y1, zs, zm, W), B(x1 - k, y0, x1, y1, zs, zm, W)]
    out += [B(x0 + k, y0 + k, pa, y0 + e, zs, zm, CP), B(pb, y0 + k, x1 - k, y0 + e, zs, zm, CP), B(pa, y0 + k, pb, y0 + e, zh, zm, CP),
            B(x0 + k, y1 - e, x1 - k, y1 - k, zs, zm, CP), B(x0 + k, y0 + e, x0 + e, y1 - e, zs, zm, CP),
            B(x1 - e, y0 + e, x1 - k, y1 - e, zs, zm, CP)]
    out.append(B(x0 + e, y0 + e, x1 - e, y1 - e, zm - 2, zm - 1, CP))                          # plafond (dessous à CAB_Z_PLAFOND)
    out += [B(pa, y0, pa + 0.75, y0 + e, zs, zh, W), B(pb - 0.75, y0, pb, y0 + e, zs, zh, W),   # jambages et linteau de l'ouverture
            B(pa, y0, pb, y0 + e, zh - 0.75, zh, W)]
    for x in range(x0 + 6, x1, 12):                  # couvre-joints des planches verticales
        out.append(B(x - 0.75, y1, x + 0.75, y1 + 0.6, zs, zm, W))
        if not (pa - 3 < x < pb + 3):
            out.append(B(x - 0.75, y0 - 0.6, x + 0.75, y0, zs, zm, W))
    for y in range(y0 + 6, y1, 12):
        out += [B(x0 - 0.6, y - 0.75, x0, y + 0.75, zs, zm, W), B(x1, y - 0.75, x1 + 0.6, y + 0.75, zs, zm, W)]
    # toit 7/12 en rangs (gradins de 4,5 po), bouts blancs (pignons et rives)
    tx0, ty0, tx1, ty1 = CAB_TOIT
    h, d = 2.625, 4.5
    ze = zm - 1
    k = 0
    while (tx1 - tx0) - 2 * k * d > 0.5:
        xa, xb, za, zb = tx0 + k * d, tx1 - k * d, ze + k * h, ze + (k + 1) * h
        out += [B(xa, ty0, xb, ty1, za, zb, "ext-bardeau-cab"), B(xa, ty0 - 0.6, xb, ty0, za, zb, W), B(xa, ty1, xb, ty1 + 0.6, za, zb, W)]
        k += 1
    out += [B(tx0, ty0, x0, ty1, ze - 1.5, ze, W), B(x1, ty0, tx1, ty1, ze - 1.5, ze, W),                 # soffites
            B(tx0 - 1, ty0, tx0, ty1, ze - 6, ze + h, W), B(tx1, ty0, tx1 + 1, ty1, ze - 6, ze + h, W),   # fascias
            B(tx0 - 6, ty0, tx0 - 1, ty1, ze - 6, ze - 1, W), B(tx1 + 1, ty0, tx1 + 6, ty1, ze - 6, ze - 1, W),   # gouttières
            B(tx0, ty0, tx1, y0, ze - 8, ze, W), B(tx0, y1, tx1, ty1, ze - 8, ze, W)]                     # caissons sous les pignons
    for (xa, xb) in ((tx0 - 1, tx0 + 11), (tx1 - 11, tx1 + 1)):                                         # retours de corniche
        out += [B(xa, ty0 - 1, xb, ty0 + 7, ze - 10, ze, W), B(xa, ty1 - 7, xb, ty1 + 1, ze - 10, ze, W)]
    # chambranle blanc de la porte, dehors
    out += [B(pa - 3, y0 - 0.4, pa, y0, zs, zh + 3, W), B(pb, y0 - 0.4, pb + 3, y0, zs, zh + 3, W), B(pa - 3, y0 - 0.4, pb + 3, y0, zh, zh + 3, W)]
    # porte de garage OUVERTE : panneau noir relevé à l'horizontale sous le plafond (4 sections de 21 po, les 8 carreaux de la
    # section du haut au fond), rails noirs horizontaux et verticaux, arbre des ressorts au-dessus de l'ouverture
    zp, yp0 = CAB_Z_PANNEAU, y0 + e + 1
    xm = (pa + pb) / 2
    out.append(B(pa + 0.5, yp0, pb - 0.5, yp0 + hp, zp, zp + 1.5, "porte-ext"))
    for j in (1, 2, 3):
        out.append(B(pa + 0.5, yp0 + 21 * j - 0.4, pb - 0.5, yp0 + 21 * j + 0.4, zp - 0.3, zp, "metal"))
    for (a, b) in ((pa + 4, xm - 2), (xm + 2, pb - 4)):
        out.append(B(a, yp0 + 66, b, yp0 + 80, zp - 0.25, zp, "ext-carreau"))
        for j in range(1, 4):
            xx = a + (b - a) * j / 4
            out.append(B(xx - 0.6, yp0 + 66, xx + 0.6, yp0 + 80, zp - 0.5, zp, "metal"))
    for xr in (pa - 2.25, pb + 0.75):
        out += [B(xr, y0 + e, xr + 1.5, yp0 + hp + 6, zp - 0.5, zp + 3, "metal"),                     # rails horizontaux
                B(xr, y0 + e, xr + 1.5, y0 + e + 2, zs, zp + 3, "metal")]                              # rails verticaux
    out.append(T([(pa - 3, y0 + e + 2.5, zh + 7), (pb + 3, y0 + e + 2.5, zh + 7)], 1.0, "metal", pans=8))   # arbre des ressorts
    # aménagement intérieur (garage.py) : souffleuse, établi, mur de bacs, vélos, outils, luminaires DEL
    return out + GARAGE_AMENAGE["objets"]


def _palmier(x, y, z, g):
    """Palmier (kentia) dans un pot blanc lustré en boule : tiges, palmes arquées."""
    out = [C(x, y, 6, z, z + 2.5, "ext-blanc", pans=16), SPH(x, y, z + 10, 10, "ext-blanc", ecrase=0.85)]
    for j in range(3):
        a = g + 2.1 * j
        out.append(T([(x, y, z + 14), (x + 2.5 * math.cos(a), y + 2.5 * math.sin(a), z + 32 + 4 * j)], 0.8, "bois_brut", pans=6))
    for j in range(16):
        a = g + 2 * math.pi * j / 16
        z0 = z + 30 + 5 * (j % 3)
        L = 18 + 5 * (j % 2) + (6 if j % 4 == 0 else 0)
        dz = 30 if j % 4 == 0 else 22 - 3 * (j % 3)
        out.append(T([(x + 2 * math.cos(a), y + 2 * math.sin(a), z0), (x + 0.45 * L * math.cos(a), y + 0.45 * L * math.sin(a), z0 + dz),
                      (x + L * math.cos(a), y + L * math.sin(a), z0 + dz - 12)], 1.3, "plante", pans=5))
    return out


def mobilier_patio():
    """Salon de patio modulaire en résine tressée anthracite à coussins blanc cassé (sectionnel en L, table à dessus de verre,
    2 fauteuils, 2 poufs), gros BBQ au gaz contre le garde-corps de l'escalier, deux palmiers en pots blancs."""
    Z = Z_TERRASSE
    O, K = "ext-osier", "ext-coussin"
    out = [ARR(177, 441, 255, 470, Z, Z + 13, O), ARR(177, 441, 207, 522, Z, Z + 13, O),          # bases du sectionnel en L
           ARR(184, 447, 254, 469, Z + 13, Z + 17, K, 2, 1), ARR(184, 447, 206, 521, Z + 13, Z + 17, K, 2, 1),   # assises
           ARR(177, 441, 255, 447, Z + 13, Z + 28, O), ARR(177, 441, 183, 522, Z + 13, Z + 28, O),  # dossiers (cadre)
           ARR(183, 447, 254, 452, Z + 17, Z + 28, K, 2, 1), ARR(183, 447, 188, 521, Z + 17, Z + 28, K, 2, 1),   # coussins de dos
           ARR(250, 441, 255, 470, Z + 13, Z + 22, O), ARR(177, 517, 207, 522, Z + 13, Z + 22, O)]  # accoudoirs
    out += [B(x - 1.25, y - 1.25, x + 1.25, y + 1.25, Z, Z + 24, O) for x in (211, 251) for y in (476, 514)]   # table
    out += [B(209, 474, 253, 516, Z + 23, Z + 25, O), B(210, 475, 252, 515, Z + 25, Z + 25.4, "verre-clair")]
    for x in (212, 233):                                                                       # 2 fauteuils à dossier haut
        out += [ARR(x, 518, x + 20, 540, Z, Z + 14, O), ARR(x + 1, 519, x + 19, 535, Z + 14, Z + 18, K, 2, 1),
                ARR(x, 535, x + 20, 540, Z + 14, Z + 31, O)]
    for y in (478, 497):                                                                       # 2 poufs
        out += [ARR(255, y, 272, y + 17, Z, Z + 14, O), ARR(255.5, y + 0.5, 271.5, y + 16.5, Z + 14, Z + 17, K, 2, 1)]
    # BBQ au gaz (caisson gris foncé, dessus et couvercle inox, tablettes), dos au garde-corps x = 386, face vers -x
    out += [B(350, 476, 378, 546, Z + 2, Z + 35, "ext-bbq"), B(349, 474, 379, 548, Z + 35, Z + 36.5, "inox"),
            {"forme": "cylindre", "axe": "y", "x": 363, "y0": 480, "y1": 542, "z": Z + 38, "r": 10, "mat": "inox"},
            B(351, 464, 377, 474, Z + 33.5, Z + 35, "ext-bbq"), B(351, 548, 377, 558, Z + 33.5, Z + 35, "ext-bbq"),
            B(349.4, 480, 350, 542, Z + 6, Z + 30, "metal"),
            {"forme": "cylindre", "axe": "x", "x0": 351, "x1": 377, "y": 480, "z": Z + 3, "r": 3, "mat": "pneu"},
            {"forme": "cylindre", "axe": "x", "x0": 351, "x1": 377, "y": 542, "z": Z + 3, "r": 3, "mat": "pneu"}]
    out += _palmier(180, 532, Z, 0.3) + _palmier(425, 393, Z, 1.1)
    return out


# ------------------------------------------------------------------------------------------------- végétation, clôture, corde
ARBRES = [  # (x, y, hauteur, genre) : f = feuillu, b = bouleau, p = pin, o = arbre ornemental
    # lisière de feuillus au-delà de la ligne arrière
    (-200, 960, 560, "f"), (-110, 1050, 620, "f"), (-20, 970, 520, "f"), (70, 1070, 600, "f"), (160, 985, 540, "f"),
    (250, 1060, 640, "f"), (340, 975, 560, "f"), (430, 1090, 600, "f"), (530, 1010, 580, "f"), (620, 1080, 620, "f"),
    (690, 960, 540, "f"),
    # bouleaux derrière le garage (au-delà de la ligne arrière)
    (455, 930, 380, "b"), (510, 955, 420, "b"), (565, 920, 360, "b"), (405, 955, 400, "b"),
    # le long de la ligne gauche (cimes au-dessus de la pelouse)
    (-200, 80, 600, "f"), (-185, 240, 520, "f"), (-150, 400, 580, "f"), (-130, 560, 540, "f"),
    (-120, 710, 600, "f"), (-115, 840, 520, "f"),
    # au-delà de l'allée (côté droit) : feuillus et deux pins près du coin arrière droit
    (780, -330, 520, "f"), (720, 20, 600, "f"), (680, 210, 560, "f"), (640, 430, 560, "p"), (690, 560, 600, "p"),
    (680, 780, 580, "f"),
    # petit arbre ornemental à l'avant gauche
    (-60, -250, 170, "o"),
]


def terrain_et_vegetation():
    """Le gazon est le relief du moteur. Ici : arbres, haie du voisin le long de l'allée, arbustes, clôture de bois au fond,
    corde à linge."""
    out = []
    for i, (x, y, H, g) in enumerate(ARBRES):
        z = _zg(x, y)
        if g == "p":
            out += [C(x, y, 7, z, z + 90, "bois_brut", pans=10), C(x, y, H * 0.12, z + 60, z + H, "ext-sapin", r2=0, pans=12)]
        elif g == "o":
            out += [C(x, y, 4, z, z + 80, "bois_brut", pans=10), SPH(x, y, z + 115, 50, "ext-feuillage-clair", ecrase=0.85)]
        else:
            tronc = "ext-bouleau" if g == "b" else "bois_brut"
            m1, m2 = ("ext-feuillage", "ext-feuillage-clair") if i % 2 else ("ext-feuillage-clair", "ext-feuillage")
            dx, dy = (0.08 * H, -0.05 * H) if i % 3 else (-0.07 * H, 0.06 * H)
            out += [C(x, y, 4.5 if g == "b" else 8, z, z + 0.45 * H, tronc, pans=10),
                    SPH(x, y, z + 0.58 * H, 0.28 * H, m1, ecrase=0.8), SPH(x + dx, y + dy, z + 0.8 * H, 0.21 * H, m2, ecrase=0.85)]
    # arbustes bas de l'autre côté de l'allée (chez le voisin) et à l'est du bout de l'allée (gazon bas), à valider
    out += [SPH(x, y, _zg(x, y) + r * 0.5, r, "ext-sapin", ecrase=0.75) for (x, y, r) in
            ((592, 20, 20), (598, 140, 24), (590, 260, 20), (596, 360, 22), (550, 448, 17), (552, 486, 18))]
    out += cloture()
    # corde à linge : poulie sur le mur arrière, deux fils blancs, poteau près de la ligne oblique (CORDE_POTEAU, déplacé le
    # 2026-11-02 pour que le fil ne passe pas au-dessus de la piscine de 21 pi : il reste à 4 pi de la paroi)
    px, py = CORDE_POTEAU
    zc = _zg(px, py)
    L = math.hypot(px - 172, py - 381.5)
    nx, ny = (py - 381.5) / L, -(px - 172) / L                 # traverse perpendiculaire au fil
    out += [B(168, 380, 176, 382, 165, 177, "metal"), T([(172, 381.5, 168), (px, py, 168)], 0.25, "blanc", pans=4),
            T([(172, 381.5, 173), (px, py, 173)], 0.25, "blanc", pans=4), C(px, py, 2, zc, 180, "gris", pans=10),
            T([(px - 5 * nx, py - 5 * ny, 176), (px + 5 * nx, py + 5 * ny, 176)], 0.8, "metal", pans=6)]
    return out


# ------------------------------------------------------------------------------------------------- clôture et portillons
# Clôture d'intimité en bois de 6 pi (comme celle du fond dans la vidéo DAG 08) : planches sur planches teintes brun, chapeau,
# poteaux 4 × 4 aux 8 pi au plus, à CL_RETRAIT en dedans des lignes de lot ; panneaux en escalier qui suivent le relief (bas des
# planches à 1½ po du point bas de chaque panneau : jamais plus de 4 po de vide). Deux portillons de 42 po, quincaillerie noir mat,
# dessinés ouverts. Rien de haut dans la cour avant : à droite, la clôture s'arrête derrière la maison (portillon en haut des
# marches de pierre) ; à gauche, elle revient vers le mur de la maison à 8 po du coin arrière.
CL_RETRAIT = 4.0           # axe à 4 po en dedans des lignes de lot : face extérieure des poteaux (3½ po) à 2¼ po de la ligne
CL_H = 72.0                # 6 pi au-dessus du point bas de chaque panneau (dessus du chapeau)
CL_ENTRAXE = 96.0          # poteaux aux 8 pi au plus
CL_POT = 3.5               # poteaux 4 × 4
CL_Y_GAUCHE = 372.0        # fermeture côté gauche : de la ligne oblique au mur gauche de la maison, 8 po devant le coin arrière
CL_Y_DROITE = 553.0        # fermeture côté droit : de la ligne x = 560 au haut des marches de pierre (portillon), puis sur le muret
CL_X_MURET = 454.75        # axe de la clôture sur le muret le long de l'allée (dans l'axe du garde-corps de l'escalier du deck)


def _cl_axes():
    """Sommets de l'axe de la clôture : coin arrière gauche et coin arrière droit (intersections des lignes décalées)."""
    k = 32.1 / 523.3
    xg = lambda y: _ligne_gauche(y) + CL_RETRAIT * math.sqrt(1 + k * k)
    (ax, ay), (bx, by) = (560.0, 871.0), (-43.0, 903.0)        # ligne arrière
    L = math.hypot(bx - ax, by - ay)
    nx, ny = -(by - ay) / L, (bx - ax) / L                     # normale vers l'intérieur du lot (-y)
    a2 = (ax + CL_RETRAIT * nx, ay + CL_RETRAIT * ny)
    yr = lambda x: a2[1] + (x - a2[0]) * (by - ay) / (bx - ax)
    xd = 560.0 - CL_RETRAIT
    y = 900.0
    for _ in range(20):                                        # coin arrière gauche (point fixe, pentes faibles)
        y = yr(xg(y))
    return xg, (round(xg(y), 2), round(y, 2)), (xd, round(yr(xd), 2))


XG_CL, CL_COIN_G, CL_COIN_D = _cl_axes()
# tronçons (polylignes de l'axe) : poteaux aux sommets et aux 8 pi au plus
CL_TRONCONS = [
    ("Clôture côté gauche (ligne oblique)", [(round(XG_CL(CL_Y_GAUCHE), 2), CL_Y_GAUCHE), CL_COIN_G]),
    ("Clôture arrière", [CL_COIN_G, CL_COIN_D]),
    ("Clôture côté droit (ligne x = 560)", [CL_COIN_D, (CL_COIN_D[0], CL_Y_DROITE)]),
    ("Clôture devant le garage, côté allée", [(CL_COIN_D[0], CL_Y_DROITE), (501.25, CL_Y_DROITE)]),
    ("Clôture sur le muret de l'allée", [(CL_X_MURET, CL_Y_DROITE), (CL_X_MURET, 497.0)]),
    ("Clôture à gauche de la maison", [(round(XG_CL(CL_Y_GAUCHE), 2), CL_Y_GAUCHE), (-48.5, CL_Y_GAUCHE)]),
]
# portillons de 42 po : (nom, poteau des pentures, poteau du loquet, rotation à l'ouverture en degrés (+ = antihoraire vu de dessus))
PORTILLONS = [
    ("Portillon de l'allée (haut des marches de pierre)", (501.25, CL_Y_DROITE), (CL_X_MURET, CL_Y_DROITE), 180),
    ("Portillon du côté gauche de la maison", (-2.5, CL_Y_GAUCHE), (-48.5, CL_Y_GAUCHE), -90),
]


def _cl_sol(x, y):
    """Dessus de ce sur quoi la clôture est posée : le relief, ou le couronnement des murets (50)."""
    z = _zg(x, y)
    for (x0, y0, x1, y1) in (MURET_Y, MURET_X):
        if x0 - 0.75 <= x <= x1 + 0.75 and y0 - 0.75 <= y <= y1 + 0.75:
            z = max(z, SOL + 2)
    return z


def _bande(p, u, n, s0, s1, w0, w1):
    """Rectangle le long de la direction u (unitaire) depuis p : de s0 à s1 en long, de w0 à w1 selon la normale n."""
    return [(p[0] + u[0] * s + n[0] * w, p[1] + u[1] * s + n[1] * w) for s, w in ((s0, w0), (s1, w0), (s1, w1), (s0, w1))]


def _panneau(p, u, n, s0, s1, zmin, mat="ext-cloture"):
    """Panneau de planches sur planches de s0 à s1 le long de u : âme mince, planches de 5½ po alternées sur les deux faces
    (aux 9 po), chapeau ; bas à zmin + 1½, dessus du chapeau à zmin + CL_H."""
    zb, zt = zmin + 1.5, zmin + CL_H - 1.5
    out = [P(_bande(p, u, n, s0, s1, -0.3, 0.3), zb, zt, mat), P(_bande(p, u, n, s0 - 0.5, s1 + 0.5, -2.75, 2.75), zt, zt + 1.5, mat)]
    s = s0
    while s < s1 - 0.5:
        for (d, w0, w1) in ((0.0, 0.3, 1.05), (4.5, -1.05, -0.3)):
            a, b = s + d, min(s + d + 5.5, s1)
            if b - a > 0.5:
                out.append(P(_bande(p, u, n, a, b, w0, w1), zb, zt, mat))
        s += 9.0
    return out


def _cl_poteaux_baies():
    """[(p0, p1)] baies de chaque tronçon, et {poteau arrondi: (x, y)}."""
    baies, poteaux = [], {}
    for nom, pts in CL_TRONCONS:
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            L = math.hypot(xb - xa, yb - ya)
            m = max(1, math.ceil(L / CL_ENTRAXE - 1e-9))
            q = [(xa + (xb - xa) * i / m, ya + (yb - ya) * i / m) for i in range(m + 1)]
            for p0, p1 in zip(q, q[1:]):
                baies.append((nom, p0, p1))
            for x, y in q:
                poteaux[(round(x, 1), round(y, 1))] = (x, y)
    for _, h, l, _ in PORTILLONS:
        for x, y in (h, l):
            poteaux[(round(x, 1), round(y, 1))] = (x, y)
    return baies, poteaux


def _zmin_seg(p0, p1, n=8):
    return min(_cl_sol(p0[0] + (p1[0] - p0[0]) * k / n, p0[1] + (p1[1] - p0[1]) * k / n) for k in range(n + 1))


def cloture():
    out, hauts = [], {}
    baies, poteaux = _cl_poteaux_baies()
    for _, p0, p1 in baies:
        L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        u = ((p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L)
        n = (-u[1], u[0])
        zmin = _zmin_seg(p0, p1)
        out += _panneau(p0, u, n, CL_POT / 2, L - CL_POT / 2, zmin)
        for q in (p0, p1):
            k = (round(q[0], 1), round(q[1], 1))
            hauts[k] = max(hauts.get(k, -1e9), zmin + CL_H)
    # portillons : planches sur planches, deux traverses et une écharpe dedans, pentures en T, loquet et poignée noir mat
    for _, h, l, rot in PORTILLONS:
        L = math.hypot(l[0] - h[0], l[1] - h[1])
        u0 = ((l[0] - h[0]) / L, (l[1] - h[1]) / L)              # du poteau des pentures vers le loquet (fermé)
        a = math.radians(rot)
        u = (u0[0] * math.cos(a) - u0[1] * math.sin(a), u0[0] * math.sin(a) + u0[1] * math.cos(a))
        n = (-u[1], u[0])
        # pivot sur la face du poteau, battant décalé de son demi-épais pour se rabattre à côté (180°) ou s'ouvrir (90°)
        piv = (h[0] + u0[0] * CL_POT / 2, h[1] + u0[1] * CL_POT / 2)
        if rot == 180:
            piv = (h[0] - u0[0] * CL_POT / 2 + n[0] * 6.0, h[1] - u0[1] * CL_POT / 2 + n[1] * 6.0)
        else:
            piv = (h[0] + u0[0] * (CL_POT / 2 + 1.2), h[1] + u0[1] * (CL_POT / 2 + 1.2))
        s0, s1 = 0.5, 42.5
        zg = _zmin_seg(piv, (piv[0] + u[0] * s1, piv[1] + u[1] * s1))
        out += _panneau(piv, u, n, s0, s1, zg)
        zb = zg + 1.5
        out += [P(_bande(piv, u, n, s0 + 1, s1 - 1, 1.05, 2.55), zb + 6, zb + 9.5, "ext-cloture"),
                P(_bande(piv, u, n, s0 + 1, s1 - 1, 1.05, 2.55), zb + 56, zb + 59.5, "ext-cloture"),
                T([(piv[0] + u[0] * (s1 - 3) + n[0] * 1.8, piv[1] + u[1] * (s1 - 3) + n[1] * 1.8, zb + 10),
                   (piv[0] + u[0] * (s0 + 3) + n[0] * 1.8, piv[1] + u[1] * (s0 + 3) + n[1] * 1.8, zb + 55)], 1.3, "ext-cloture", pans=6)]
        for zz in (zb + 7, zb + 57):                              # pentures en T noires
            out += [P(_bande(piv, u, n, s0, s0 + 16, 2.55, 2.85), zz, zz + 1.5, "metal"),
                    C(round(piv[0], 2), round(piv[1], 2), 0.6, zz - 1, zz + 2.5, "metal", pans=8)]
        out += [P(_bande(piv, u, n, s1 - 5, s1 - 0.5, 1.05, 1.9), zb + 52, zb + 55, "metal"),   # loquet à gravité à 54 po (hors de portée des petits)
                P(_bande(piv, u, n, s1 - 4, s1 - 3.2, -1.9, -1.05), zb + 34, zb + 46, "metal")]   # poignée
    # poteaux 4 × 4 (chapeau), enfouis dans le sol
    for k, (x, y) in poteaux.items():
        zt = hauts.get(k, _cl_sol(x, y) + CL_H) + 2
        zb = min(_cl_sol(x + dx, y + dy) for dx in (-2, 2) for dy in (-2, 2)) - 4
        u = (1.0, 0.0)
        for _, p0, p1 in baies:
            if (round(p0[0], 1), round(p0[1], 1)) == k or (round(p1[0], 1), round(p1[1], 1)) == k:
                L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
                u = ((p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L)
                break
        n = (-u[1], u[0])
        out += [P(_bande((x, y), u, n, -CL_POT / 2, CL_POT / 2, -CL_POT / 2, CL_POT / 2), zb, zt, "ext-cloture"),
                P(_bande((x, y), u, n, -2.75, 2.75, -2.75, 2.75), zt, zt + 1, "ext-cloture")]
    return out


def _cl_obstacles():
    """Obstacles minces (4 po) le long de chaque baie, poteaux compris ; rien dans l'ouverture des portillons ; battants ouverts."""
    baies, _ = _cl_poteaux_baies()
    out = []
    for i, (nom, p0, p1) in enumerate(baies):
        L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        u = ((p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L)
        n = (-u[1], u[0])
        out.append({"nom": f"{nom} ({i + 1})", "pts": [[round(x, 2), round(y, 2)] for x, y in _bande(p0, u, n, -2, L + 2, -2, 2)]})
    for nom, h, l, rot in PORTILLONS:
        for q in (h, l):
            out.append({"nom": f"{nom}, poteau", "pts": rect(round(q[0] - 2, 2), round(q[1] - 2, 2), round(q[0] + 2, 2), round(q[1] + 2, 2))})
        L = math.hypot(l[0] - h[0], l[1] - h[1])
        u0 = ((l[0] - h[0]) / L, (l[1] - h[1]) / L)
        a = math.radians(rot)
        u = (u0[0] * math.cos(a) - u0[1] * math.sin(a), u0[0] * math.sin(a) + u0[1] * math.cos(a))
        n = (-u[1], u[0])
        piv = (h[0] - u0[0] * CL_POT / 2 + n[0] * 6.0, h[1] - u0[1] * CL_POT / 2 + n[1] * 6.0) if rot == 180 else \
              (h[0] + u0[0] * (CL_POT / 2 + 1.2), h[1] + u0[1] * (CL_POT / 2 + 1.2))
        out.append({"nom": f"{nom} (battant ouvert)", "pts": [[round(x, 2), round(y, 2)] for x, y in _bande(piv, u, n, 0, 43, -1.5, 3)]})
    return out


# ------------------------------------------------------------------------------------------------- revêtements, planchers, obstacles
def _revetements():
    out = [{"nom": "Allée d'asphalte", "mat": "ext-asphalte",
            "pts": [[456, -480], [552, -480], [552, 380], [505, 380], [505, PIERRES_Y0], [457, PIERRES_Y0], [457, 380], [456, 380]]},
           {"nom": "Asphalte devant l'escalier avant", "mat": "ext-asphalte", "pts": rect(*AIRE_AV)},
           {"nom": "Gravier sous l'escalier du deck", "mat": "ext-gravier", "pts": rect(*GRAVIER_ESC)},
           {"nom": "Gravier autour de la piscine", "mat": "ext-gravier", "pts": cercle(PISC[0], PISC[1], GRAVIER_R, 40)}]
    out += [{"nom": f"Pas japonais {i + 1}", "mat": "ext-dalle", "pts": [list(p) for p in d]} for i, d in enumerate(DALLES)]
    return out


def _planchers():
    Z = Z_TERRASSE
    r_esc = (Z - SOL) / 7
    out = [{"nom": "Palier de la porte arrière", "pts": rect(*PALIER), "z": Z},
           {"nom": "Patio", "pts": rect(*PATIO), "z": Z},
           {"nom": "Deck de la piscine", "pts": _deck_pts(), "z": Z}]
    out += [{"nom": f"Escalier de la cour, marche {i}", "pts": rect(ESC[0], ESC[1] + 9 * (i - 1), ESC[2], ESC[1] + 9 * i),
             "z": round(Z - r_esc * i, 2)} for i in range(1, 7)]
    out.append({"nom": "Garage (dalle de béton)", "pts": rect(CAB[0] - 2, CAB[1] - 2, CAB[2] + 2, CAB[3] + 2), "z": CAB_Z_DALLE})
    out.append({"nom": "Perron avant", "pts": rect(*PERRON), "z": Z_PERRON})
    out += [{"nom": f"Marches du perron, marche {i}", "pts": p, "z": z} for i, p, z in _marches_perron()]
    out += [{"nom": f"Marches de pierre, marche {i + 1}", "pts": [[round(x, 2), round(y, 2)] for x, y in p], "z": z}
            for i, (p, z) in enumerate(_pierres())]
    return out


def _obstacles():
    cx, cy, R = PISC
    yd, yg = _bout_deck(314), _bout_deck(159)
    cer = lambda x, y, r, n=12: cercle(x, y, r, n)
    return [{"nom": "Piscine", "pts": cer(cx, cy, R + 1, 32)},
            {"nom": "Muret le long de l'allée", "pts": rect(*MURET_Y)}, {"nom": "Muret (aile)", "pts": rect(*MURET_X)},
            {"nom": "Garde-corps du palier et de l'escalier", "pts": rect(453.5, 380, 456, 494)},
            {"nom": "Garde-corps patio / escalier", "pts": rect(385, 440, 387, 560)},
            {"nom": "Garde-corps du patio (bas)", "pts": rect(314, 557.5, 386, 560)},
            {"nom": "Garde-corps du patio (devant le mur)", "pts": rect(159, 440, 219, 442.5)},
            {"nom": "Garde-corps du patio (gauche)", "pts": rect(159, 440, 161.5, 560)},
            {"nom": "Verre patio / deck (le portillon, x 274-310, s'ouvre)", "pts": rect(159, 559, 274, 561)},
            {"nom": "Verre patio / deck, bout droit", "pts": rect(310, 559, 314, 561)},
            {"nom": "Garde-corps du deck (droite)", "pts": rect(311.5, 560, 314, round(yd, 1))},
            {"nom": "Garde-corps du deck (gauche)", "pts": rect(159, 560, 161.5, round(yg, 1))},
            {"nom": "Appareils de la piscine", "pts": [list(p) for p in APPAREILS]},
            {"nom": "Salon du patio", "pts": rect(175, 440, 272, 542)}, {"nom": "BBQ", "pts": rect(348, 462, 380, 558)},
            {"nom": "Cheminée", "pts": rect(*CHEMINEE)},
            {"nom": "Garde-corps du perron (gauche)", "pts": rect(162, -92, 165, 0)},
            {"nom": "Garde-corps du perron (droite)", "pts": rect(231, -92, 234, 0)},
            {"nom": "Palmier (patio)", "pts": cer(180, 532, 10)}, {"nom": "Palmier (palier)", "pts": cer(425, 393, 10)},
            {"nom": "Poteau de la corde à linge", "pts": cer(CORDE_POTEAU[0], CORDE_POTEAU[1], 3, 8)},
            {"nom": "Arbre ornemental (tronc)", "pts": cer(-60, -250, 6)}] + _obstacles_garage() + _cl_obstacles()


def _obstacles_garage():
    """Murs minces du garage (la porte de garage est ouverte : on entre)."""
    x0, y0, x1, y1 = CAB
    e = CAB_EP
    return [{"nom": "Garage, mur avant (gauche de la porte)", "pts": rect(x0, y0, CAB_PORTE[0], y0 + e)},
            {"nom": "Garage, mur avant (droite de la porte)", "pts": rect(CAB_PORTE[1], y0, x1, y0 + e)},
            {"nom": "Garage, mur arrière", "pts": rect(x0, y1 - e, x1, y1)},
            {"nom": "Garage, mur côté piscine", "pts": rect(x0, y0, x0 + e, y1)},
            {"nom": "Garage, mur côté x = 560", "pts": rect(x1 - e, y0, x1, y1)}] + GARAGE_AMENAGE["obstacles"]


def _visites():
    Z = Z_TERRASSE
    s = lambda x, y: round(_zg(x, y), 1)
    return [
        {"nom": "Façade avant", "x": 228, "y": -390, "cap": 90, "z": s(228, -390)},
        {"nom": "Façade avant de biais (côté allée)", "x": 500, "y": -300, "cap": 118, "z": s(500, -300)},
        {"nom": "L'allée et le côté", "x": 530, "y": -430, "cap": 100, "z": s(530, -430)},
        {"nom": "L'allée devant la porte de côté", "x": 530, "y": 110, "cap": 145, "z": s(530, 110)},
        {"nom": "Le bout de l'allée, les marches de pierre et le portillon", "x": 481, "y": 405, "cap": 90, "z": s(481, 405)},
        {"nom": "Cour arrière — vue d'ensemble (du coin du fond)", "x": 60, "y": 880, "cap": 312, "z": s(60, 880)},
        {"nom": "Le patio", "x": 372, "y": 452, "cap": 123, "z": Z},
        {"nom": "Le deck et la piscine", "x": 330, "y": 515, "cap": 120, "z": Z},
        {"nom": "Le garage agrandi et les pas japonais", "x": 420, "y": 508, "cap": 84, "z": s(420, 508)},
        {"nom": "Garage vu de la cour", "x": 433, "y": 548, "cap": 90, "z": s(433, 548)},
        *GARAGE_AMENAGE["visites"],
        {"nom": "Dans le garage (vers la porte ouverte)", "x": 440, "y": 766, "cap": 270, "z": CAB_Z_DALLE},
        {"nom": "La piscine vue de la cour", "x": 30, "y": 505, "cap": 55, "z": s(30, 505)},
        {"nom": "Le portillon du côté gauche de la maison", "x": -20, "y": 470, "cap": 268, "z": s(-20, 470)},
    ]


# ------------------------------------------------------------------------------------------------- aperçu du relief (EXT_APERCU=1)
def _apercu():
    """Colonnes prismatiques (cases d'environ 24 po, dessus au relief) en couleur du gazon ou du revêtement : seulement pour
    voir le relief avec un moteur qui ne le dessine pas. Les arêtes de la maison sont gardées (aucune colonne dans un trou)."""
    from shapely.geometry import Point, Polygon
    trous = [Polygon(t) for t in TROUS]
    revs = [(Polygon(r["pts"]), r["mat"]) for r in REVETEMENTS]
    bords_x = {0, 456, 219, 327, 161, 235, -20.3, BORD, 445, 457, 505, 552}
    bords_y = {0, 380, 440, -49, 132, 153.6, MURET_X[1], MURET_X[3]}

    def sous(lignes, bords):
        out = [lignes[0]]
        for v in lignes[1:]:
            if v - out[-1] >= 20 or v in bords or v == lignes[-1]:
                out.append(v)
        return out
    xs, ys = sous(RELIEF["xs"], bords_x), sous(RELIEF["ys"], bords_y)
    out = []
    for ya, yb in zip(ys, ys[1:]):
        for xa, xb in zip(xs, xs[1:]):
            c = Point((xa + xb) / 2, (ya + yb) / 2)
            if any(t.contains(c) for t in trous):
                continue
            mat = next((m for g, m in revs if g.contains(c)), "ext-gazon")
            out.append(B(xa, ya, xb, yb, -30, _zg(c.x, c.y), mat))
    return out


REVETEMENTS = _revetements()

EXTERIEUR = {
    "sol": SOL,
    "relief": RELIEF,
    "revetements": REVETEMENTS,
    "terrain": TERRAIN,
    "objets": enveloppe() + toit() + perron_avant() + cour() + terrain_et_vegetation(),
    "planchers": _planchers(),
    "obstacles": _obstacles(),
    "trous": TROUS,
    "visites": _visites(),
    "lumieres": [{"x": 328.5, "y": 432, "z": 178, "i": 2}, {"x": 240, "y": -1.5, "z": 170, "i": 2},
                 *GARAGE_AMENAGE["lumieres"]],   # 4 luminaires DEL du garage (garage.py)
    "peintures": PEINTURES,
    "palette": [["Brique rouge", "parement du rez-de-chaussée (existant)", "#8E3B2E"],
                ["Fondation crépie blanche", "fondation apparente, lisse (vidéo DAG)", "#EEEDE8"],
                ["Bardeau d'asphalte gris anthracite", "toit à deux versants 5/12 et pignon avant", "#3F4245"],
                ["Pignons en déclin vertical blanc", "pignons, rives, fascias, soffites", "#F4F4F2"],
                ["Platelage composite beige clair", "palier, patio, deck et girons (teinte de la vidéo DAG, à choisir)", "#CBB592"],
                ["Garde-corps d'aluminium noir", "barreaux 36 et 48 po, portillon à barreaux ; verre pur sur pinces entre le patio et le deck", "#1A1A1A"],
                ["Jupe en déclin blanc", "sous les terrasses ; limons blancs de l'escalier ouvert", "#F4F4F2"],
                ["Piscine hors-terre 21 pi", "paroi grise de 52 po, margelle gris pâle, eau turquoise ; anneau de gravier", "#8C9090"],
                ["Muret de blocs gris pâle", "soutènement entre la cour et l'allée, marches de pierre naturelle", "#A8AAA6"],
                ["Asphalte", "allée au niveau du sous-sol, jusqu'au bout derrière la maison", "#45474A"],
                ["Garage 13' × 17'", "planches verticales blanches, toit 7/12, porte de garage noire à carreaux ; dedans : contreplaqué", "#F4F4F2"],
                ["Clôture de bois 6 pi", "planches sur planches teintes brun, poteaux 4 × 4 ; 2 portillons de 42 po, quincaillerie noir mat", "#8A6A48"],
                ["Salon de patio", "résine tressée anthracite, coussins blanc cassé", "#3A3B3C"]] + GARAGE_AMENAGE["palette"],
}
# appliques des portes (les lumières ci-dessus y sont placées)
EXTERIEUR["objets"] += [B(327.5, 429, 333, 435, 172, 184, "metal"), B(328.5, 430, 332, 434, 174, 182, "abat-jour"),
                        B(237, -5.5, 243, -0.5, 164, 176, "metal"), B(238, -4.5, 242, -1.5, 166, 174, "abat-jour")]
if os.environ.get("EXT_APERCU") == "1":
    EXTERIEUR["objets"] += _apercu()
