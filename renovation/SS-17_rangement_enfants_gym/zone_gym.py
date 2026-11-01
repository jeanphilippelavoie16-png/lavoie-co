"""SS-17 — zone « gym » : salle d'entraînement (x 112–228, y 10–157 ; verre sur y = 157 et x = 228).

Plan retenu (spec : final_gym.json) : tapis roulant et vélo côte à côte contre le mur avant, face au mur ; tout l'arrière
devient un plancher libre de 72 × 72 po en dalles de caoutchouc, qui sert aussi de passage de 38 po vers la salle de
lavage ; le mur du lavage (x = 112) devient un mur-miroir de 12 pi, porte du lavage comprise (miroir sur sa face gym,
dessinée fermée dans la 3D) ; télé de 40 po sur bras entre les appareils ; tablette haute de chêne et colonne de crochets
au mur avant (tout ce qui est dangereux pour des enfants de 4 et 6 ans est au-dessus de 56 po) ; banc-coffre bas à
tiroirs verrouillés (poids) contre le verre de l'escalier (rien de haut contre ce verre) ; extracteur, 6 encastrés
3000 K et DEL linéaire qui lave le miroir ; porte vitrée ouv-SS-P01 coulissante, rail et vantail côté hall.
Pouces, repère de la maison.
"""

# nus intérieurs de la pièce
XM, XG, YA, YH = 114.25, 227.0, 10.0, 156.0          # mur du lavage (face gym), verre de l'escalier, mur avant, verre du hall
SS16_LUMIERES_GYM = {(170, 50), (160, 120)}
SS16_VISITES_GYM = {"Vélo et tapis roulant"}


# ---------------------------------------------------------------------------------------------------- plan (2D)
def appliquer_modifs(L, base):
    # porte du gym : battante → coulissante vitrée, rail apparent noir et vantail côté hall (se range vers l'est)
    L["PORTES"][:] = [("ouv-SS-P01", "mur-SS-P10", 168.0, 32, "droite",
                       "porte vitrée coulissante de la salle d'entraînement (rail apparent noir côté hall, se range vers l'est)",
                       "coulissante", "verre", None) if p[0] == "ouv-SS-P01" else p for p in L["PORTES"]]
    # nom court : avec les appareils dessinés, « Salle d'entraînement » ne tient plus dans la pièce sur le plan
    L["PIECES"][:] = [("piece-SS-GYM", "Gym", p[2]) if p[0] == "piece-SS-GYM" else p for p in L["PIECES"]]
    ids = {"elem-SS-P-GYM-TAPIS", "elem-SS-P-GYM-VELO", "elem-SS-P-GYM-BANC", "elem-SS-P-GYM-SOL", "elem-SS-P-GYM-MIROIR"}
    L["EQUIPEMENTS"][:] = [e for e in L["EQUIPEMENTS"] if e[0] not in ids]
    L["EQUIPEMENTS"] += [
        ("elem-SS-P-GYM-TAPIS", "autre", "Tapis roulant (existant), console vers le mur avant ; 20 po de chaque côté, 69 po derrière",
         "TAPIS", 189, 49.5, 90, (75, 36)),
        ("elem-SS-P-GYM-VELO", "autre", "Vélo de route sur base d'entraînement (existant), roue avant vers le mur avant",
         "VÉLO", 134, 47, 90, (70, 30)),
        ("elem-SS-P-GYM-BANC", "armoires", "Banc-coffre bas 16 × 60 × 18 po contre le verre de l'escalier : tiroirs verrouillés (poids), case ouverte",
         "", 218, 121.75, 90, (59.5, 16)),
        ("elem-SS-P-GYM-SOL", "trappe", "Zone au sol 6 × 6 pi en dalles de caoutchouc 10 mm (aussi le passage vers la salle de lavage)",
         "", 150.25, 120, 0, (72, 72)),
        ("elem-SS-P-GYM-MIROIR", "autre", "Mur-miroir 105 × 74 po sur la face gym du mur du lavage ; la porte du lavage est revêtue de miroir côté gym",
         "", 114.75, 64.5, 90, (105, 1.0)),
    ]


def apres_modifs(maison, base):
    """Porte du lavage ouv-SS-P02 : revêtue de miroir côté gym ; dessinée FERMÉE dans la 3D pour qu'elle se fonde dans le
    mur-miroir (elle ouvre toujours côté lavage)."""
    ss = next(n for n in maison["niveaux"] if n["id"] == "SS")
    for o in ss["ouvertures"]:
        if o["id"] == "ouv-SS-P02":
            o["fermee"] = True
            o["note"] = (o.get("note") or "") + " Face gym revêtue de miroir (mur-miroir du gym, SS-17) ; porte pleine, 3 pentures ; ouvre côté lavage."


# ---------------------------------------------------------------------------------------------------- 3D
def _emprise(o):
    if "x0" in o and "y0" in o:
        return o["x0"], o["y0"], o["x1"], o["y1"]
    if "pts" in o:
        xs, ys = [p[0] for p in o["pts"]], [p[1] for p in o["pts"]]
        return min(xs), min(ys), max(xs), max(ys)
    if "x0" in o:                                   # cylindre d'axe x
        return o["x0"], o["y"], o["x1"], o["y"]
    if "y0" in o:                                   # cylindre d'axe y
        return o["x"], o["y0"], o["x"], o["y1"]
    if "x" in o and "y" in o:
        return o["x"], o["y"], o["x"], o["y"]
    return None


def _ss16_du_gym(o):
    """Objet de SS-16 dans la salle d'entraînement (on garde le trait de scie du béton, x = 120)."""
    e = _emprise(o)
    if e is None:
        return False
    x0, y0, x1, y1 = e
    if not (112 <= x0 and x1 <= 228 and 10 <= y0 and y1 <= 157):
        return False
    if o.get("forme") == "boite" and o.get("z1", 1) <= 0.06:
        return False                                # trait de scie du béton poli
    return True


def appliquer_scene(S, h):
    B, A, C, CX, CY, T, TOR, MOD = h.B, h.A, h.C, h.CX, h.CY, h.T, h.TOR, h.MOD
    S["mobilier"][:] = [o for o in S["mobilier"] if not _ss16_du_gym(o)]
    M = []

    # --- cardio contre le mur avant, face au mur ------------------------------------------------------------------
    # tapis roulant : console à 2 po du mur avant, 20 po libres de chaque côté, 69 po derrière (vers le coin est)
    M += [A(169, 10.5, 209, 87.5, 0, 0.375, "caoutchouc-noir", r=2, b=0.15),
          MOD("tapis_roulant", 189, 49.5, face="-y", z=0.375)]
    # vélo de route sur base (le modèle porte son propre tapis, caché sous le nôtre ; la cale avant reste à 4 po du mur)
    M += [A(116.25, 10.5, 152, 84, 0, 0.25, "caoutchouc-noir", r=2, b=0.15),
          MOD("velo_route_base", 134, 47, face="-y")]

    # --- zone au sol 72 × 72 en dalles de caoutchouc 24 × 24 (10 mm), aussi le passage vers le lavage --------------
    M += [A(XM, 87.5, 186.25, YH, 0, 0.375, "caoutchouc", r=1, b=0.1),
          A(XM, 84, 169, 87.5, 0, 0.375, "caoutchouc", r=0.5, b=0.1)]
    M += [B(x - 0.08, 84.2, x + 0.08, YH - 0.2, 0.375, 0.39, "pneu") for x in (138.25, 162.25)]
    M += [B(XM + 0.2, y - 0.08, 186.05, y + 0.08, 0.375, 0.39, "pneu") for y in (108, 132)]

    # --- mur-miroir de 12 pi (mur du lavage, face gym) ---------------------------------------------------------------
    # miroir sans cadre 105 × 74 en 4 panneaux, pellicule de sécurité, profilé noir mince en bas
    M += [B(XM, 12, XM + 0.5, 117.25, 10, 84, "miroir"), B(XM, 12, XM + 0.75, 117.25, 9.5, 10, "metal")]
    M += [B(XM + 0.5, y - 0.06, XM + 0.53, y + 0.06, 10, 84, "carbone") for y in (38.3, 64.6, 90.9)]
    # porte du lavage (fermée dans la 3D) : miroir collé sur sa face gym, presque à fleur du mur-miroir ; cadre noir
    # (chambranle recouvert) ; poignée noire côté libre (pentures du côté du hall)
    M += [B(112.9, 120.55, 114.1, 149.45, 0.5, 80, "porte"), B(114.1, 120.9, 114.2, 149.1, 6, 78, "miroir")]
    M += [B(XM, 117.35, XM + 0.75, 120.15, 0, 82.65, "metal"), B(XM, 149.85, XM + 0.75, 152.65, 0, 82.65, "metal"),
          B(XM, 117.35, XM + 0.75, 152.65, 79.9, 82.65, "metal")]
    M += [T([(114.2, 124, 38), (116.4, 124, 38), (116.4, 129, 38)], 0.35, "metal", bouts=True),
          T([(111.1, 124, 38), (108.9, 124, 38), (108.9, 129, 38)], 0.35, "metal", bouts=True)]
    # DEL linéaire encastrée au plafond qui lave le miroir (3000 K)
    M += [B(115.5, 12, 117, 150, 95.7, 96, "spot")]

    # --- mur avant : tablette haute de chêne, télé sur bras, colonne de crochets --------------------------------------
    M += [A(XM + 0.75, YA, 226.5, 20, 78, 79.5, "placage", r=0.3, b=0.3), B(116, 17.5, 225.5, 18, 77.75, 78, "spot")]
    M += [CY(120 + 5.2 * k, 11, 19, 82.1, 2.6, "draps") for k in range(3)] + \
         [CY(122.6 + 5.2 * k, 12, 18, 86.6, 2.2, "art-sable") for k in range(2)]                     # serviettes roulées
    M += [C(141 + 3.6 * k, 15, 1.4, 79.5, 89, "inox") for k in range(3)] + \
         [C(141 + 3.6 * k, 15, 0.8, 89, 90.2, "carbone") for k in range(3)]                          # bouteilles
    M += [A(176, 12, 186, 18, 79.5, 85, "carbone", r=1.5, b=0.8), CY(181, 17.9, 18.1, 82.2, 1.8, "gris"),   # haut-parleur
          A(192, 12, 202, 19, 79.5, 85.5, "blanc", r=0.8, b=0.4), B(195.8, 18.95, 198.2, 19.05, 81.5, 83.5, "cuir")]  # premiers soins
    # ventilateur oscillant sur la tablette, vers le tapis et le vélo
    M += [C(218, 15, 3.2, 79.5, 80.3, "metal"), C(218, 15, 0.5, 80.3, 84, "metal"), A(216, 11, 220, 14.5, 81, 89, "carbone", r=1, b=0.5),
          CY(218, 13.5, 16.8, 85, 4.4, "carbone", pans=32), TOR(218, 16.9, 85, 4.4, 0.3, "gris"), CY(218, 16.6, 16.8, 85, 1.2, "gris")]
    # télé 40 po sur bras articulé (repliée) entre les deux appareils, câbles dans le mur
    M += [B(156, YA, 164, 10.6, 58, 70, "metal"), T([(160, 10.6, 64), (160, 12.8, 64)], 0.7, "metal"),
          B(142.5, 12.8, 177.5, 14, 54, 74, "carbone"), B(143, 14, 177, 14.1, 54.5, 73.5, "ecran")]
    # colonne de crochets d'acier noir (62, 68, 74 po) : élastiques, corde à sauter, sangle, 2 tapis de yoga ; clé du tapis à 66 po
    M += [B(210.5, YA, 211.5, 10.6, 56, 77, "metal"), B(222.5, YA, 223.5, 10.6, 56, 77, "metal")]
    M += [B(210.5, YA, 223.5, 10.6, z - 0.5, z + 0.5, "metal") for z in (62, 68, 74)]
    for x, z in ((213, 74), (220, 74), (213, 68), (217, 68), (220, 68), (216.5, 62), (220.5, 62)):
        M.append(T([(x, 10.6, z), (x, 12.6, z), (x, 13.2, z + 1.2)], 0.22, "metal", bouts=True))
    M += [C(213, 13.2, 2.6, 49, 73, "tissu"), C(220, 13.2, 2.6, 49, 73, "art-sable"),               # tapis de yoga roulés
          T([(213, 12.6, 73.8), (213, 13.2, 75.6)], 0.3, "carbone"), T([(220, 12.6, 73.8), (220, 13.2, 75.6)], 0.3, "carbone")]
    M += [TOR(217, 12.7, 64.6, 2.8, 0.28, "cuir"), TOR(217, 12.9, 64.2, 2.4, 0.28, "carbone"),       # élastiques
          TOR(220, 12.8, 64.4, 2.2, 0.35, "pneu")]                                                    # corde à sauter enroulée
    M += [B(216.2, 12.4, 216.8, 12.8, 58.6, 62, "carbone"), A(215.6, 12.2, 217.4, 13, 57.2, 58.6, "carbone", r=0.4, b=0.2)]  # sangle
    M += [T([(212.6, 10.6, 66), (212.6, 11.8, 66)], 0.25, "laiton", bouts=True), C(212.6, 12.2, 0.7, 64.2, 65.6, "laiton")]   # clé (aimant)

    # --- banc-coffre bas contre le verre de l'escalier (rien de haut contre ce verre) --------------------------------
    # 16 × 59½ × 18 po : socle d'acier noir en retrait, caisson de chêne à coins arrondis ; case ouverte (y 92–118)
    # et 2 grands tiroirs verrouillés (y 118–135, 135–151½) pour les haltères et les kettlebells ; dessus rembourré
    BX0, BX1, BY0, BY1 = 210, 226, 92, 151.5
    M += [B(BX0 + 1.5, BY0 + 1, BX1 - 0.5, BY1 - 1, 0, 3, "metal")]
    M += [A(BX0, 118, BX1, BY1, 3, 18, "placage", r=0.8, b=0.3),                                      # tiroirs
          A(BX0, BY0, BX1, BY0 + 1, 3, 18, "placage", r=0.4, b=0.2),                                  # côté de la case
          B(BX1 - 0.75, BY0 + 1, BX1, 118, 3, 18, "placage"),                                         # fond de la case
          B(BX0 + 0.3, BY0 + 1, BX1 - 0.75, 118, 3, 3.75, "placage"),                                 # plancher de la case
          B(BX0, BY0, BX1, BY1, 17.25, 18, "placage")]                                                # dessus
    M += [A(BX0 + 0.25, BY0 + 0.25, BX1 - 0.25, BY1 - 0.25, 18, 20.5, "cuir", r=1.5, b=0.9)]       # coussin
    M += [B(BX0 - 0.1, y - 0.12, BX0 + 0.05, y + 0.12, 3.5, 16.75, "carbone") for y in (118.2, 134.85)]
    for yc in (126.5, 143.25):                                                                        # poignées, serrures
        M += [B(BX0 - 0.7, yc - 4.5, BX0, yc + 4.5, 13.2, 13.8, "metal"), B(BX0 - 0.7, yc - 4.5, BX0 - 0.1, yc - 3.9, 13.2, 14.6, "metal"),
              B(BX0 - 0.7, yc + 3.9, BX0 - 0.1, yc + 4.5, 13.2, 14.6, "metal"), CX(BX0 - 0.3, BX0, yc, 15.7, 0.45, "inox")]
    M += [CY(216.5, BY0 + 2, BY0 + 16, 6.95, 3.2, "tissu", pans=24),                                 # rouleau de massage
          TOR(221, 113.5, 4.2, 3.3, 0.45, "cuir", axe="z"), TOR(221, 113.5, 5.1, 2.8, 0.45, "carbone", axe="z")]   # élastiques doux

    # --- plafond : extracteur, interrupteur sur la colonne C04 ----------------------------------------------------
    M += [B(190, 136, 198, 144, 95.6, 96, "blanc"), B(191, 137, 197, 143, 95.55, 95.6, "gris")]
    M += [B(144.6, 151.55, 147.4, 151.75, 45.5, 50.5, "blanc"), B(145.6, 151.45, 146.4, 151.55, 47, 49, "gris")]

    # --- porte vitrée COULISSANTE ouv-SS-P01 (dessinée ouverte, rangée vers l'est) : vantail et rail côté hall -------
    # vantail 34 × 81½ : verre trempé dans un cadre noir, poignée côté hall, loquet haut à 60 po ; rail sous la retombée
    # de la poutre (z 86), amortisseurs aux deux bouts
    PX0, PX1, PY0, PY1 = 183, 217, 158.6, 159.3
    M += [B(PX0 + 1.5, PY0 + 0.15, PX1 - 1.5, PY1 - 0.15, 2.25, 79.75, "porte-verre"),
          B(PX0, PY0, PX0 + 1.5, PY1, 0.75, 81.25, "metal"), B(PX1 - 1.5, PY0, PX1, PY1, 0.75, 81.25, "metal"),
          B(PX0, PY0, PX1, PY1, 0.75, 2.25, "metal"), B(PX0, PY0, PX1, PY1, 79.75, 81.25, "metal")]
    M += [T([(PX0 + 4, PY1, 34), (PX0 + 4, PY1 + 1.6, 35.5), (PX0 + 4, PY1 + 1.6, 50.5), (PX0 + 4, PY1, 52)], 0.4, "metal"),
          B(PX0 + 0.3, PY1, PX0 + 1.3, PY1 + 0.9, 59, 61.5, "metal")]
    M += [B(151.5, 158.2, 218, 160.4, 82.4, 85.97, "metal"), B(151.5, 158.2, 153, 160.6, 80.5, 82.4, "metal"),
          B(216.5, 158.2, 218, 160.6, 80.5, 82.4, "metal")]
    M += [C(x, (PY0 + PY1) / 2, 0.6, 81.25, 82.4, "metal") for x in (PX0 + 5, PX1 - 5)]
    S["mobilier"] += M

    # --- lumières : 6 encastrés 3000 K (gradables) ----------------------------------------------------------------
    S["lumieres"][:] = [l for l in S["lumieres"] if (l.get("x"), l.get("y")) not in SS16_LUMIERES_GYM or l.get("z")]
    S["lumieres"] += [{"x": 142, "y": 40}, {"x": 199, "y": 40}, {"x": 142, "y": 84}, {"x": 199, "y": 112},
                      {"x": 142, "y": 128}, {"x": 199, "y": 146}]

    # --- visite ---------------------------------------------------------------------------------------------------
    S["visites"][:] = [v for v in S["visites"] if v["nom"] not in SS16_VISITES_GYM]
    i = next((k + 1 for k, v in enumerate(S["visites"]) if v["nom"].startswith("Gym (porte")), len(S["visites"]))
    S["visites"][i:i] = [{"nom": "Gym — mur-miroir et zone au sol", "x": 200, "y": 150, "cap": 200},
                         {"nom": "Gym — cardio", "x": 150, "y": 150, "cap": 285}]

    # --- palette --------------------------------------------------------------------------------------------------
    S["palette"][:] = [p for p in S["palette"] if p[0] != "Gym"]
    S["palette"].append(["Gym", "murs anthracite, mur-miroir de 12 pi (porte du lavage comprise), dalles de caoutchouc 24 × 24 "
                         "pour la zone au sol de 6 × 6 pi, tapis noirs sous les appareils ; tablette et banc-coffre de chêne, "
                         "dessus de cuir, acier noir ; porte vitrée coulissante sur rail noir", "#2A2A2A"])
