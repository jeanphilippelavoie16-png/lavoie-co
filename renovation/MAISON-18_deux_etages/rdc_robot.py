"""MAISON-18 — RDC : l'aspirateur robot qui fait le ménage en haut (demande du client, 2026-11-02).

« Je veux qu'il y ait une balayeuse robot automatique qui se promène en haut dans la maison qui est en train de faire du
ménage. »

Ce module (chargé en dernier par scene_3d.py et modifs.py) :
- creuse un GARAGE dans le socle du garde-manger encastré (rdc_cuisine.py) : ouverture de 17 po au centre du coup de pied,
  socle porté de 4 à 4½ po ; la base de recharge est au fond, contre le mur (prise dans le caisson du bas du garde-manger) ;
- ajoute le robot (SCENE["animes"] du RDC, contrat dans generer_3d.animes) : rond, 13,8 po × 3,6 po, dessus noir mat,
  tourelle laser, pare-chocs avant, brosse latérale qui tourne, voyant vert qui clignote ;
- son trajet en boucle : sort du garage, nettoie en allers-retours parallèles le passage dégagement-cuisine-salon, le salon,
  le fond de la cuisine et l'allée entre la table et l'îlot, puis rentre au garage (pause) et recommence.
  Le trajet a été CALCULÉ (scratchpad, planificateur à part) sur les emprises réelles de la scène RDC générée : murs,
  poteaux, garde-corps de la trémie, portes dans leur état de départ, pieds de chaises et de tabourets, sofa, îlot, poubelles,
  plantes ; centre du robot à au moins 7,9 po de tout obstacle (rayon 6,9 + 1 po de jeu). Le moteur ne fait aucun
  évitement : si le mobilier de ces zones change, refaire le trajet (_verifier() avertit d'un segment qui frôle un meuble) ;
- un arrêt de visite « Aspirateur robot » d'où on le voit passer ; on TOUCHE le robot pour l'arrêter ou le faire repartir
  (petit bip ; zone de toucher élargie ; repère « Touche le robot » sur tablette en arrivant à l'arrêt) — plus de bouton.
Plan P-130 : le garde-manger (elem-RDC-K-GM) mentionne le garage du robot (appliquer_modifs_rdc).
Détail et coûts : DESIGN_robot.md. Pouces, repère du plancher du RDC (x le long de la façade, y vers l'arrière).
"""
import math

SOURCE = "proposition MAISON-18 (esquisse) — aspirateur robot"

# --------------------------------------------------------------------------- garde-manger (rdc_cuisine.py) et garage
GM_X0, GM_YC = 148.25, 229.375          # fond du garde-manger (nu du mur, x = 148¼) ; axe du garde-manger en y
SOCLE_FACE = 173.5                      # face du coup de pied (3 po en retrait des portes, x = 176½)
SOCLE_Z = 4.5                           # socle porté de 4 à 4½ po : robot de 3,6 po + jeu
GARAGE_L = 17.0                         # largeur de l'ouverture du garage (robot de 13,8 po)
GARAGE = (GM_X0, GM_YC - GARAGE_L / 2, SOCLE_FACE, GM_YC + GARAGE_L / 2)
DOCK_X1 = 151.25                        # face de la base de recharge (contre le fond du garde-manger)

# --------------------------------------------------------------------------- robot
R_ROBOT, H_ROBOT = 6.9, 3.6             # 13,8 po de diamètre (35 cm) × 3,6 po (9,2 cm)
VITESSE = 11.8                          # po/s (30 cm/s, vitesse de nettoyage d'un robot courant)
ROTATION = 120                          # °/s, virages sur place
PAUSE_BASE = 20                         # s au garage avant de repartir (la recharge réelle dure plus longtemps)
DEPART = 6                              # s déjà écoulées au chargement : il sort du garage

# Trajet calculé (planificateur : scratchpad m18/anim/robot/planifier.py) : point 0 = au garage, sur la base.
TRAJET = [[158.6, 229.4], [190, 229.4], [185.5, 205.5], [184, 204], [413.2, 204], [415.5, 199.5], [437.8, 192],
          [180, 192], [180, 180], [437.8, 180], [437.5, 162], [437.5, 18.5], [432.5, 34.5], [426.5, 40.5],
          [425, 40.5], [425, 162], [412.5, 162], [412.5, 41], [410.5, 41.5], [402.5, 33.5], [400.5, 18.5],
          [400.5, 162], [388, 162], [388, 18.5], [375.5, 18.5], [375.5, 88.2], [363, 88.2], [363, 18.5], [351, 18.5],
          [351, 88.2], [338.5, 88.2], [338.5, 18.5], [326, 18.5], [326, 88.2], [378.5, 88.5], [382.5, 93.5],
          [382.5, 137.5], [322, 205], [322, 339.8], [315.5, 339.5], [311.5, 343.5], [311, 352], [311, 205],
          [300.5, 205], [300.5, 352], [289.5, 352], [289.5, 205], [279, 205], [279, 352], [268, 352], [268, 205],
          [190, 229.4]]

ARRET = {"nom": "Aspirateur robot", "x": 350, "y": 165, "cap": 145, "tangage": -22}


def _robot():
    """Objets du robot, repère LOCAL : origine au centre du dessous, +x = l'avant, +y = sa gauche."""
    r, out = R_ROBOT, []
    out += [{"forme": "cylindre", "x": 0, "y": 0, "z0": 0.3, "z1": 0.45, "r": r - 0.6, "mat": "pneu"},       # dessous
            {"forme": "cylindre", "x": 0, "y": 0, "z0": 0.45, "z1": 2.95, "r": r - 0.2, "mat": "gris"},              # jupe grise
            {"forme": "cylindre", "x": 0, "y": 0, "z0": 2.95, "z1": 3.08, "r": r - 0.3, "mat": "pneu"},       # dessus noir mat
            # tourelle laser (télémètre) : socle noir, fenêtre sombre, chapeau noir
            {"forme": "cylindre", "x": -1.3, "y": 0, "z0": 3.08, "z1": 3.22, "r": 1.75, "mat": "pneu"},
            {"forme": "cylindre", "x": -1.3, "y": 0, "z0": 3.22, "z1": 3.42, "r": 1.6, "mat": "carbone"},
            {"forme": "cylindre", "x": -1.3, "y": 0, "z0": 3.42, "z1": 3.6, "r": 1.7, "mat": "pneu"},
            # bouton à voyant (vert : en marche) devant la tourelle
            {"forme": "cylindre", "x": 2.3, "y": 0, "z0": 3.08, "z1": 3.14, "r": 0.55, "mat": "carbone"},
            {"forme": "cylindre", "x": 2.3, "y": 0, "z0": 3.14, "z1": 3.17, "r": 0.3, "mat": "spot", "clignote": 2.4,
             "couleur": "#3fd18b"}]
    # pare-chocs avant : bande noire en arc (± 75°) autour de la jupe
    a = [math.radians(-75 + 150 * i / 14) for i in range(15)]
    ext = [[round(r * math.cos(t), 3), round(r * math.sin(t), 3)] for t in a]
    inn = [[round((r - 0.3) * math.cos(t), 3), round((r - 0.3) * math.sin(t), 3)] for t in reversed(a)]
    out.append({"forme": "boite", "pts": ext + inn, "z0": 0.7, "z1": 2.7, "mat": "carbone"})
    # brosse latérale (avant droit) : moyeu et 3 brins qui balaient vers le centre (antihoraire vu de dessus)
    hx, hy = 4.7, -4.5
    out.append({"forme": "cylindre", "x": hx, "y": hy, "z0": 0.18, "z1": 0.5, "r": 0.65, "mat": "carbone", "tourne": 540})
    for d in (15, 135, 255):
        t = math.radians(d)
        out.append({"forme": "tube", "pts": [[hx, hy, 0.32], [round(hx + 3.2 * math.cos(t), 3), round(hy + 3.2 * math.sin(t), 3), 0.12]],
                    "r": 0.14, "mat": "gris", "tourne": 540, "centre": [hx, hy]})
    return out


def _garage(S):
    """Coup de pied du garde-manger : ouverture de 17 po au centre, socle à 4½ po ; base de recharge au fond.
    Retourne False (et ne touche à rien) si le garde-manger de rdc_cuisine.py n'est pas trouvé."""
    M = S["mobilier"]
    socle = [o for o in M if o.get("forme", "boite") == "boite" and o.get("mat") == "carbone" and "x0" in o
             and abs(o["x0"] - GM_X0) < 0.3 and abs(o["x1"] - SOCLE_FACE) < 0.3 and o.get("z0") == 0 and abs(o["z1"] - 4.0) < 0.05
             and o["y0"] < GARAGE[1] and o["y1"] > GARAGE[3]]
    caisson = [o for o in M if o.get("forme") == "arrondi" and o.get("mat") == "noir-mat" and "x0" in o and abs(o["x0"] - GM_X0) < 0.3
               and abs(o["z0"] - 4.0) < 0.05 and o["y0"] < GARAGE[1] and o["y1"] > GARAGE[3] and o["x1"] > SOCLE_FACE]
    if len(socle) != 1 or len(caisson) != 1:
        print("  [rdc_robot] ATTENTION : socle du garde-manger introuvable ; garage non creusé")
        return False
    s, c = socle[0], caisson[0]
    c["z0"] = SOCLE_Z
    i = M.index(s)
    M[i:i + 1] = [dict(s, y1=GARAGE[1], z1=SOCLE_Z), dict(s, y0=GARAGE[3], z1=SOCLE_Z),
                  # fond du garage : bande de socle derrière la base
                  dict(s, x1=GM_X0 + 0.75, y0=GARAGE[1], y1=GARAGE[3], z1=SOCLE_Z)]
    yc = GM_YC
    M += [  # fond du garage noir (on voit une fente sombre dans le socle, pas le plancher)
        {"forme": "boite", "x0": GM_X0 + 0.75, "x1": SOCLE_FACE, "y0": GARAGE[1], "y1": GARAGE[3], "z0": 0, "z1": 0.15, "mat": "pneu"},
        # base de recharge : tour noire contre le fond, plaque à contacts, petit voyant blanc
        {"forme": "arrondi", "x0": GM_X0 + 0.75, "x1": DOCK_X1, "y0": yc - 4.2, "y1": yc + 4.2, "z0": 0, "z1": 3.9,
         "mat": "noir-mat", "r": 0.6, "b": 0.3},
        {"forme": "arrondi", "x0": DOCK_X1, "x1": DOCK_X1 + 4.5, "y0": yc - 3.6, "y1": yc + 3.6, "z0": 0, "z1": 0.28,
         "mat": "carbone", "r": 1.2, "b": 0.1},
        {"forme": "boite", "x0": DOCK_X1 + 1.6, "x1": DOCK_X1 + 2.4, "y0": yc - 2.2, "y1": yc - 1.4, "z0": 0.28, "z1": 0.34, "mat": "inox"},
        {"forme": "boite", "x0": DOCK_X1 + 1.6, "x1": DOCK_X1 + 2.4, "y0": yc + 1.4, "y1": yc + 2.2, "z0": 0.28, "z1": 0.34, "mat": "inox"},
        {"forme": "boite", "x0": DOCK_X1, "x1": DOCK_X1 + 0.08, "y0": yc - 0.25, "y1": yc + 0.25, "z0": 3.1, "z1": 3.4, "mat": "spot"},
    ]
    return True


def _verifier(S, trajet, jeu=R_ROBOT + 0.9):
    """Avertit si le trajet passe à moins de `jeu` po d'un objet bas (sous 4 po) du mobilier : boîtes, cylindres (pieds,
    pots), tubes (pieds de chaises). Le garage et sa base sont exclus (le robot y entre par construction)."""
    formes = []
    for o in S["mobilier"]:
        f = o.get("forme", "boite")
        if f in ("boite", "arrondi") and "x0" in o and o.get("z0", 0) < 4 and o.get("z1", 0) > 0.8:
            if o["x0"] >= GM_X0 - 0.1 and o["x1"] <= SOCLE_FACE + 0.1 and GARAGE[1] - 12 <= o["y0"] and o["y1"] <= GARAGE[3] + 12:
                continue
            formes.append(("b", o["x0"], o["y0"], o["x1"], o["y1"]))
        elif f == "cylindre" and "z0" in o and o["z0"] < 4 and o["z1"] > 0.8:
            formes.append(("c", o["x"], o["y"], o["r"]))
        elif f == "tube" and o.get("pts"):
            P = o["pts"]
            formes += [("t", p[0], p[1], q[0], q[1], o.get("r", 0.5)) for p, q in zip(P, P[1:]) if min(p[2], q[2]) < 4]

    def dist(x, y, f):
        if f[0] == "b":
            return math.hypot(max(f[1] - x, 0, x - f[3]), max(f[2] - y, 0, y - f[4]))
        if f[0] == "c":
            return math.hypot(x - f[1], y - f[2]) - f[3]
        dx, dy = f[3] - f[1], f[4] - f[2]
        t = max(0, min(1, ((x - f[1]) * dx + (y - f[2]) * dy) / (dx * dx + dy * dy or 1)))
        return math.hypot(x - f[1] - t * dx, y - f[2] - t * dy) - f[5]
    n = len(trajet)
    for k in range(n):
        p, q = trajet[k], trajet[(k + 1) % n]
        m = max(2, int(math.hypot(q[0] - p[0], q[1] - p[1]) / 0.5))
        pts = [(p[0] + (q[0] - p[0]) * i / m, p[1] + (q[1] - p[1]) * i / m) for i in range(m + 1)]
        x0, x1 = min(p[0], q[0]) - jeu - 30, max(p[0], q[0]) + jeu + 30
        y0, y1 = min(p[1], q[1]) - jeu - 30, max(p[1], q[1]) + jeu + 30
        proches = [f for f in formes if (f[1] < x1 and f[3] > x0 and f[2] < y1 and f[4] > y0 if f[0] == "b"
                                         else x0 < f[1] < x1 and y0 < f[2] < y1)]
        for f in proches:
            d = min(dist(x, y, f) for x, y in pts)
            if d < jeu - 0.5:
                print(f"  [rdc_robot] ATTENTION : segment {k} → {(k + 1) % n} du trajet à {d:.1f} po d'un objet {f}")
                break


def appliquer_scene_rdc(S, h):
    if not _garage(S):
        return
    S.setdefault("animes", []).append({
        "id": "robot", "nom": "Aspirateur robot",
        "objets": _robot(), "trajet": [list(p) for p in TRAJET], "vitesse": VITESSE, "rotation": ROTATION,
        "pauses": [{"point": 0, "duree": PAUSE_BASE}], "depart": DEPART,
        "invite": "Touche le robot",                         # repère sur tablette (on le touche : pause / il repart)
        "note": "Aspirateur robot : sort du garage du garde-manger, allers-retours dans le passage, le salon et la cuisine — " + SOURCE})
    _verifier(S, TRAJET)
    v = S.setdefault("visites", [])
    v[:] = [a for a in v if a.get("nom") != ARRET["nom"]]
    i = next((k + 1 for k, a in enumerate(v) if a.get("nom") == "Cuisine — rangement"), len(v))
    v.insert(i, dict(ARRET))
    S.setdefault("palette", []).append(
        ["Aspirateur robot", "rond, 35 cm, dessus noir mat, tourelle laser ; garage dans le socle du garde-manger", "#1E1F20"])


def appliquer_modifs_rdc(maison, ctx):
    """Plan P-130 : le garde-manger mentionne le garage du robot et sa prise (rien d'autre ne change au plan)."""
    for e in ctx["rdc"]["elements"]:
        if e["id"] == "elem-RDC-K-GM" and "robot" not in e.get("nom", ""):
            e["nom"] = e.get("nom", "") + f" ; garage d'aspirateur robot dans le socle (ouverture {GARAGE_L:g} × 4½ po, base au fond)"
            e["note"] = (e.get("note") or "") + (" ; prise 15 A dans le caisson du bas du garde-manger (base de recharge "
                                                 "au fond du garage du socle) — " + SOURCE)
