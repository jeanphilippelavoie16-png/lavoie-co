"""SS-17 — zone « global » : le reste du sous-sol (vestiaire et entrée de côté, hall, salle de lavage, salle de bain,
séjour hors dessous de l'escalier, trajets de nuit). Spec : scratchpad/ss17_conception/final_global/final_global.json.

Huit changements pour deux garçons de 4 et 6 ans, l'hiver à Baie-Comeau :
1. vestiaire : casiers d'hiver des garçons (séchoirs à bottes et mitaines, crochets à 36 et 44 po, tablette à 46 po,
   portes hautes vert forêt alignées sur les armoires existantes, GARDÉES), poste de recharge, colonne C03 adoucie ;
2. seuil à neige : tapis-grille encastré devant la porte de côté, bacs d'égouttement sous le banc (sol chauffant : note) ;
3. insonorisation (plafond, cloisons, portes pleines : notes) ; nuage de lattes de chêne au plafond du séjour ;
4. trajet de nuit : veilleuses à détection à 10–13 po, DEL sous la vanité, interrupteur à 42 po, colonne C02 adoucie ;
5. séjour : banc-rangement à jouets de 143 po sous la toile (dessus à 16 po : la barre de lestage, toile basse, est à
   ≈ 25 po), barre de son dessus, boîte de plancher au bout du divan sous un guéridon, store sans cordon ;
6. VRC (salle de lavage) et ses grilles d'évacuation, déshumidificateur à drain (le plancher chauffant : note) ;
7. salle de bain à hauteur d'enfant : marchepied sous la vanité, crochets à serviette à 38 po (mélangeur
   thermostatique au chauffe-eau, amortisseurs et verrou de la porte coulissante : notes) ;
8. salle de lavage : un panier de linge propre par garçon, trieur à 2 sacs, capsules en hauteur.
MAISON-18 (client, 2026-11-02) : « les fenêtres en bas sont plus grosses aussi (par le bas), sauf salle de bain et salle de
lavage » et « un gros congélateur debout ... lui trouver une place en bas » :
9. fenêtres du séjour, de la chambre 1 et de la chambre 2 descendues par le bas (allège 40 po, HYPOTHÈSE à mesurer ; tête
   inchangée) avec margelles (SCENE["fenetres"] du moteur) ; bain et lavage inchangés ; puis (2026-11-02, « les fenêtres
   dans la vidéo sont de bonnes dimensions ») séjour et chambre 2 aux dimensions de la vidéo DAG (fenetres_video.py) ;
10. congélateur vertical (≈ 20 pi³, 32 × 30 × 70 po) dans une niche de 33 po au bout du comptoir de pliage (le trieur part,
   le bac recule de 7 po, paniers des garçons de 12 po), prise simple dédiée au-dessus ; le déshumidificateur, qui était
   à 5 po devant le chauffe-eau, passe sous la fenêtre à côté de la laveuse (36 po libres devant le panneau et le chauffe-eau).
Écart assumé avec la spec : casiers de 18 po de profond (y 209¾–227¾) au lieu de 20, au nu du banc et des armoires
vertes existantes — leur dessus à 88 po ne bute plus sur la retombée de la poutre arrière (y 199–209, dessous ≈ 86 po).
Ne touche pas au mur du bain, à la galerie de photos du séjour, aux chambres, au gym ni au dessous de l'escalier.
MAISON-18 (2026-11-02, DESIGN_ss_poutre.md) : le mur hall / chambre 1 passe sous la poutre arrière et cache la colonne C02
(son habillage de chêne disparaît, C03 garde le sien) ; veilleuses, DEL de la vanité, interrupteur, marchepied et grille
d'évacuation suivent la nouvelle salle de bain et le hall de 40½ po.
Pouces, repère de la maison.
"""

# ----------------------------------------------------------------------------------------------------------- plan
NOUVEAUX = [  # id, type, nom, libellé, x, y, rotation, (longueur, largeur)
    ("elem-SS-Q-CASIERS", "armoires", "Casiers d'hiver des garçons (2 baies de 17⅞ po, séchoirs à bottes et mitaines, "
     "portes hautes vert forêt)", None, 300, 218.75, 180, (38, 18)),
    ("elem-SS-Q-GRILLE", "trappe", "Tapis-grille encastré au niveau du béton (48 × 36 po), devant la porte de côté",
     "GRILLE", 422, 180, 0, (48, 36)),
    ("elem-SS-Q-BANCJOUETS", "armoires", "Banc-rangement à jouets de chêne 143 × 16 po sous la toile (dessus à 16 po), "
     "6 tiroirs, niche ventilée, barre de son dessus", None, 438, 83.5, 90, (143, 16)),
    ("elem-SS-Q-BOITEPL", "autre", "Boîte de plancher (2 prises + 2 USB-C) au bout du divan, sous le guéridon", "",
     309, 138, 0, (6, 6)),
    ("elem-SS-Q-DESHUM", "autre", "Déshumidificateur à drain permanent (hygrostat), sous la fenêtre à côté de la laveuse "
     "(dégagement de 36 po devant le chauffe-eau)", "DÉSH.", 18, 56, 90, (20, 14)),
    ("elem-SS-Q-CONG", "refrigerateur", "Congélateur vertical ≈ 20 pi³ (≈ 32 × 30 × 70 po, blanc), niche de 33 po au bout du "
     "comptoir de pliage, porte à droite ; prise simple dédiée au-dessus (circuit séparé)", "CONG.", 92.6, 103, 90, (32, 30)),
    ("elem-SS-Q-VRC", "trappe", "Échangeur d'air récupérateur de chaleur (VRC), suspendu au mur avant à 74–94 po",
     "VRC", 85, 19, 0, (30, 18)),
]

NOTES = [  # le cartouche est déjà plein : notes courtes (elles restent dans maison.json)
    "Plafond insonorisé (laine de roche, barres résilientes, 2 gypses ⅝ X) ; portes des chambres pleines.",
    "VRC (lavage) et déshumidificateur à drain ; sol chauffant : vestiaire, bain, aire de jeu (chape).",
    "Veilleuses à détection à 10–13 po ; eau chaude limitée (mélangeur) : à valider avec le plombier.",
]


# --- MAISON-18 : fenêtres descendues par le bas et niche du congélateur
ALLEGE_SS = 40          # HYPOTHÈSE : le client n'a pas donné de mesure (« plus grosses par le bas ») ; tête inchangée (86 po)
FENETRES_BASSES = ["ouv-SS-002", "ouv-SS-004",       # séjour : façade avant, mur de droite (store, toile)
                   "ouv-SS-009", "ouv-SS-010",       # chambre 1 : les deux fenêtres d'évacuation (mur arrière)
                   "ouv-SS-003"]                     # chambre 2 : mur de droite
# gardées à 56 po : ouv-SS-006 (salle de bain) et ouv-SS-007 (salle de lavage, au-dessus de la laveuse)
YN0, YN1 = 86.5, 119.5  # niche du congélateur le long du mur du gym (x 77½–109¾) : 33 po ; la porte du lavage (y 120–150)
                        # balaie un quart de cercle de 30 po autour de (112, 150) : le coin du congélateur passe à 1 po


def appliquer_modifs(L, base):
    eq = L["EQUIPEMENTS"]
    for i, e in enumerate(eq):
        if e[0] == "elem-SS-P-BANC":   # banc gardé ; les cases à souliers deviennent des bacs d'égouttement
            eq[i] = (e[0], e[1], "Vestiaire ouvert (gardé) : banc, bacs d'égouttement, crochets, tablette, poste de recharge") + tuple(e[3:])
        elif e[0] == "elem-SS-P-PLIAGE":   # comptoir de pliage raccourci (y 35 → 86½) : niche du congélateur au bout
            eq[i] = (e[0], e[1], "Comptoir de pliage en L avec rangement dessous (mur du gym), raccourci : niche du congélateur au bout",
                     e[3], e[4], (35 + YN0) / 2, e[6], (YN0 - 35, e[7][1]))
        elif e[0] == "elem-SS-P-BAC":      # bac reculé de 7 po (4½ po de comptoir entre le bac et le congélateur)
            eq[i] = e[:5] + (e[5] - 7,) + e[6:]
    ids = {n[0] for n in NOUVEAUX}
    eq[:] = [e for e in eq if e[0] not in ids] + NOUVEAUX


def apres_modifs(maison, base):
    ss = next(n for n in maison["niveaux"] if n["id"] == "SS")
    # fenêtres descendues : l'allège (hypothèse) et la note sont reportées dans maison.json (le plan ne dessine pas l'allège)
    for o in ss["ouvertures"]:
        if o["id"] in FENETRES_BASSES:
            o["allege"] = {"valeur": ALLEGE_SS, "source": "PRÉSUMÉ", "photo": None,
                           "note": "MAISON-18 (client, 2026-11-02 : « plus grosses par le bas ») : allège abaissée de 56 à 40 po "
                                   "(HYPOTHÈSE, tête inchangée ≈ 86 po) ; margelle devant ; à mesurer et à valider"}
            o["note"] = (o.get("note") or "") + (" — MAISON-18 : agrandie vers le bas (allège ≈ 40 po, tête inchangée), "
                                                 "margelle ; appui, allège de béton et margelle à valider avec un professionnel.")
    ss.setdefault("notes", [])
    ss["notes"] = [n for n in ss["notes"] if not str(n.get("id", "")).startswith("note-SS-Q")]
    ss["notes"] += [{"id": f"note-SS-Q{i + 1:02d}", "texte_original": None, "photo": None, "interpretation": t}
                    for i, t in enumerate(NOTES)]


# ----------------------------------------------------------------------------------------------------------- 3D
def _boite(o):
    if o.get("forme") in ("boite", "arrondi"):
        return o["x0"], o["y0"], o["x1"], o["y1"], o["z0"], o["z1"]
    return None


def _est(o, mat, x0, y0, x1, y1, z0, z1, tol=0.05):
    b = _boite(o)
    return b is not None and o.get("mat") == mat and all(abs(a - c) < tol for a, c in zip(b, (x0, y0, x1, y1, z0, z1)))


def _retirer_ss16(M):
    """Retire de la scène UNIQUEMENT les objets SS-16 de la zone remplacés par SS-17 (signatures exactes)."""
    YT = 83.5

    def a_retirer(o):
        if "commande" in o:                                  # toile motorisée : jamais
            return False
        if o.get("forme") == "modele":
            return ((o["cle"] == "plante_sansevieria" and abs(o["x"] - 432) < 0.1 and abs(o["y"] - 21) < 0.1)   # plante du séjour
                    or (o["cle"] == "panier_osier" and abs(o["x"] - 106) < 0.1 and abs(o["y"] - 170) < 0.1))    # sous la vanité
        # séjour : meuble bas suspendu de 72 po et barre de son (remplacés par le banc à jouets)
        if (_est(o, "placage", 430, YT - 36, 446, YT + 36, 3, 15) or _est(o, "carbone", 430.6, YT - 35.5, 430.8, YT + 35.5, 4, 14)
                or _est(o, "carbone", 431.5, YT - 18, 437, YT + 18, 15, 18.2)):
            return True
        # vestiaire : souliers posés dans les cases du banc (les cases deviennent des bacs d'égouttement)
        b = _boite(o)
        if b and o.get("forme") == "arrondi" and abs(b[1] - 212) < 0.05 and abs(b[3] - 224) < 0.05 and abs(b[4] - 3) < 0.05 \
                and abs(b[5] - 7) < 0.05 and 336 < b[0] < 395:
            return True
        # salle de lavage : caisson plein sous le comptoir de pliage et ses traits (refait : paniers des garçons)
        if _est(o, "laque-marine", 85.75, 35, 109.75, 110, 4, 34.5) or any(_est(o, "carbone", 85.2, 37, 85.75, 109, z, z + 0.4) for z in (14, 24)):
            return True
        # MAISON-18 : comptoir de pliage raccourci pour la niche du congélateur (dessus, socle, bac et robinet reculés de 7 po,
        # poignée du trieur, tablettes et paniers au-dessus du trieur)
        if (_est(o, "placage", 84.75, 35, 109.75, 111, 34.5, 36) or _est(o, "metal", 85.75, 37, 109.75, 108, 0, 4)
                or _est(o, "inox", 89, 71, 107, 89, 35.7, 36.1) or _est(o, "inox", 90, 72, 106, 88, 26, 35.7)
                or any(_est(o, "placage", 97.75, 92, 109.75, 110, z, z + 1.5) for z in (54, 68))):
            return True
        if o.get("forme") == "tube" and o["pts"] in ([[108.5, 80, 36], [108.5, 80, 50], [105.5, 80, 52.5], [101, 80, 50]],
                                                    [[85.3, 95, 30], [85.3, 103, 30]]):
            return True
        if o.get("forme") == "cylindre" and "axe" not in o and ((o["mat"] == "metal" and (o["x"], o["y"], o["z0"]) == (108.4, 85, 36))
                                                               or (o["mat"] == "osier" and o["x"] == 103 and o["y"] in (98, 105) and o["z0"] == 55.5)):
            return True
        return False

    M[:] = [o for o in M if not a_retirer(o)]


def _vestiaire(h):
    B, A, C, T = h.B, h.A, h.C, h.T
    out = []
    # --- casiers des garçons : caisson de chêne 38 × 18 po (x 281–319), 2 baies de 17⅞ po ; ancrés au mur
    X0, X1, Y0, Y1 = 281, 319, 209.75, 227.75
    out += [B(X0 + 0.5, Y0 + 1.5, X1 - 0.5, Y1, 0, 2.5, "metal")]                                     # socle noir en retrait
    out += [A(x, Y0, x + 0.75, Y1, 2.5, 70, "placage", r=0.4, b=0.25) for x in (X0, 299.625, X1 - 0.75)]   # montants
    out += [B(X0, Y1 - 0.5, X1, Y1, 2.5, 70, "placage"),                                               # fond de chêne
            B(X0 + 0.75, Y0, X1 - 0.75, Y1, 2.5, 3.25, "placage")]                                     # fond du bas
    out += [A(xa, Y0, xb, Y1 - 0.5, z, z + 0.75, "placage", r=0.3, b=0.2)
            for xa, xb in ((X0 + 0.75, 299.625), (300.375, X1 - 0.75)) for z in (46, 62)]               # tablettes 46 et 62
    # haut : rangement de saison, portes vert forêt pareilles aux armoires du banc (70–88 po), quincaillerie noire
    out += [A(X0, Y0, X1, Y1, 69.25, 88, "laque-vert", r=0.3, b=0.3),
            B(299.8, Y0 - 0.15, 300.2, Y0, 70, 87.5, "carbone"),
            B(296.6, Y0 - 0.5, 297.2, Y0, 71, 76, "metal"), B(302.8, Y0 - 0.5, 303.4, Y0, 71, 76, "metal")]
    baies = [(290.69, "laque-vert", "laque-vert", "cuir", "carbone"),        # baie A : 6 ans (vert)
             (309.31, "laque-marine", "laque-marine", "tissu", "pneu")]      # baie B : 4 ans (marine)
    for xc, plaque, habit, sac, botte in baies:
        out += [B(xc - 3.5, Y1 - 0.75, xc + 3.5, Y1 - 0.5, 56.5, 60.5, "placage"),                   # plaquette au prénom
                B(xc - 3.5, Y1 - 0.85, xc + 3.5, Y1 - 0.75, 56.5, 57.5, plaque)]                        # (à sa couleur)
        out += [A(xc - 8.3, Y0 + 0.6, xc + 8.3, Y1 - 1, 3.25, 4.75, "caoutchouc-noir", r=1, b=0.4)]       # bac d'égouttement
        # séchoir à bottes et mitaines (air tiède, minuterie) : socle noir, 2 tiges à bottes, 2 tiges à mitaines
        out += [A(xc - 7, 212, xc + 7, 219.5, 4.75, 8.5, "carbone", r=1.2, b=0.6),
                B(xc - 2, 211.9, xc + 2, 212, 6, 7.2, "spot")]
        for dx in (-3.4, 3.4):
            out += [C(xc + dx, 215, 0.55, 8.5, 21, "carbone")]
            out += [A(xc + dx - 1.6, 213.2, xc + dx + 1.6, 216.8, 12, 20.6, botte, r=1, b=0.6),       # botte retournée
                    A(xc + dx - 1.6, 213.2, xc + dx + 1.6, 220.4, 20.6, 23.4, botte, r=1.2, b=0.8)]   # pied de la botte
        for dx in (-6.2, 6.2):
            out += [T([(xc + dx * 0.8, 217.5, 8.5), (xc + dx, 217.5, 25)], 0.45, "carbone", bouts=True),
                    A(xc + dx - 1.4, 216.4, xc + dx + 1.4, 218.6, 23, 28, habit, r=1, b=0.6)]          # mitaine
        # crochets de laiton à 36 po (habit de neige, manteau) et à 44 po (sac d'école)
        out += [T([(x, Y1 - 0.5, z), (x, Y1 - 2.8, z + 1)], 0.35, "laiton", bouts=True)
                for x, z in ((xc - 4.6, 36), (xc + 4.6, 36), (xc, 44))]
        out += [A(xc - 8.1, 222.8, xc - 1.2, 226.9, 15, 35.6, habit, r=1.5, b=1.2),                   # habit de neige
                A(xc - 3, 219.8, xc + 3.6, 222.6, 31, 43, sac, r=1.2, b=0.8),                         # sac d'école
                T([(xc, 224.5, 44.6), (xc + 0.3, 222, 43)], 0.2, "pneu")]
        out += [A(xc - 7.6, 212, xc + 7.6, 224, 46.75, 54.75, "osier", r=0.8, b=0.4),                  # panier : tuques, mitaines
                h.SPH(xc, 218.5, 62.75 + 3.0, 3.6, "carbone" if xc < 300 else "blanc", ecrase=0.85)]   # casque de vélo / ski
    # --- colonne C03 : habillage de chêne à coins arrondis (trajet de nuit, hauteur de tête des enfants) ; C02 est
    #     maintenant cachée dans le mur de la poutre (MAISON-18)
    out += [A(x - 5.5, 198.5, x + 5.5, 209.5, 0, 85.9, "placage", r=0.75, b=0.5) for x in (324,)]
    # minuterie 2 h des séchoirs et thermostat du sol chauffant, face avant de C03 (commandes des parents)
    out += [B(322, 198.2, 326, 198.5, 48, 53, "carbone"), B(323.3, 198.1, 324.7, 198.2, 51, 52, "spot"),
            B(322, 198.2, 326, 198.5, 55, 60, "blanc"), B(322.6, 198.1, 325.4, 198.2, 57, 59, "ecran")]
    # --- banc existant gardé : bacs d'égouttement dans les 3 cases (bottes des adultes)
    for xa, xb in ((335.2, 356.2), (357.8, 378.7), (380.3, 400.8)):
        out += [A(xa, 211.5, xb, 226.5, 3, 4.5, "caoutchouc-noir", r=1, b=0.4)]
    for x0, mat in ((338.5, "cuir"), (383.5, "carbone")):
        for dx in (0, 6):
            out += [A(x0 + dx, 213, x0 + dx + 4.4, 224, 4.5, 8.5, mat, r=1.5, b=1),                    # bottes d'adulte
                    A(x0 + dx, 219.5, x0 + dx + 4.4, 224.5, 8.5, 14.5, mat, r=1.2, b=0.8)]
    # poste de recharge 120 V + USB-C sous les armoires vertes : bandeau noir ; tablettes et cellulaires des garçons
    out += [B(336, 210, 400, 212, 68.6, 69.95, "carbone"), B(345, 214, 352.5, 224, 67.5, 67.85, "ecran"),
            B(355, 214, 362.5, 224, 67.5, 67.85, "ecran"), B(366, 216, 369.2, 222.5, 67.5, 67.85, "ecran")]
    # --- seuil à neige : tapis-grille encastré affleurant (cadre et profilés d'aluminium noir, inserts brosse)
    out += [B(398, 162, 446, 198, 0, 0.05, "caoutchouc-noir")]
    out += [B(398, 162, 446, 162.75, 0, 0.1, "metal"), B(398, 197.25, 446, 198, 0, 0.1, "metal"),
            B(398, 162, 398.75, 198, 0, 0.1, "metal")]
    x = 400.25
    while x < 445.5:
        out.append(B(x - 0.25, 162.75, x + 0.25, 197.25, 0, 0.09, "metal"))
        x += 1.5
    # grille d'évacuation du VRC au plafond, devant les casiers
    out += [B(295, 186, 303, 194, 95.7, 96, "metal"), B(296, 187, 302, 193, 95.6, 95.7, "pneu")]
    return out


def _nuit(h):
    """Veilleuses encastrées à 10–13 po (DEL ambre, détection de mouvement), interrupteur et DEL de la salle de bain."""
    B = h.B
    # MAISON-18 : V1 et V2 au pied du mur de la poutre, côté hall (bout est et bout ouest) ; V3 dans l'entrée de la
    # chambre 1 (mur de la chambre 2) ; interrupteur sur le coin du mur de la poutre, côté poignée de la porte
    out = [B(224.5, 198.25, 227.5, 198.5, 10, 13, "metal"), B(225, 198.15, 227, 198.25, 10.6, 11.6, "spot"),     # V1
           B(147, 198.25, 150, 198.5, 10, 13, "metal"), B(147.5, 198.15, 149.5, 198.25, 10.6, 11.6, "spot"),     # V2
           B(237.5, 236, 237.75, 239, 10, 13, "metal"), B(237.4, 236.5, 237.5, 238.5, 10.6, 11.6, "spot")]       # V3
    out += [B(46, 179.4, 104, 180.4, 11.55, 11.95, "spot"),                                                   # DEL sous la vanité
            B(138.55, 201, 138.95, 204, 40, 44, "metal")]                                                      # interrupteur à 42 po
    return out


def _salle_de_bain(h):
    A, B, T = h.A, h.B, h.T
    # boîte-marchepied de chêne rangée sous la vanité suspendue (dessous à 12 po), sous la vasque de droite, dessus antidérapant
    out = [A(78, 166, 102, 178, 0, 7.75, "placage", r=0.6, b=0.4), B(78.6, 166.6, 101.4, 177.4, 7.75, 8, "caoutchouc-noir"),
           B(77.9, 170, 78, 174, 4.5, 6, "carbone"), B(102, 170, 102.1, 174, 4.5, 6, "carbone")]
    # crochets à serviette : 2 à 38 po (un par garçon, serviette à sa couleur), 1 à 64 po
    for x, z in ((128.5, 38), (135.5, 38), (132, 64)):
        out.append(T([(x, 159.25, z), (x, 161.6, z + 0.8)], 0.35, "laiton", bouts=True))
    out += [A(125.3, 159.6, 131.7, 161.2, 18, 38.3, "laque-vert", r=0.6, b=0.5),
            A(132.3, 159.6, 138.7, 161.2, 18, 38.3, "laque-marine", r=0.6, b=0.5)]
    # évacuation du VRC (ou ventilateur à hygrostat) au plafond de la douche (MAISON-18), hors de la retombée de la poutre
    out += [B(124, 224, 132, 232, 95.7, 96, "metal"), B(125, 225, 131, 231, 95.6, 95.7, "pneu")]
    return out


def _lavage(h):
    A, B, C, T = h.A, h.B, h.C, h.T
    out = []
    # bas du comptoir de pliage refait : 2 paniers coulissants de linge propre (un par garçon) dans une niche ouverte,
    # portes sous le bac (loquet magnétique), trieur à 2 sacs au bout
    # MAISON-18 : le comptoir s'arrête à y = 86½ (niche du congélateur au bout) ; le trieur part, le bac recule de 7 po,
    # les paniers des garçons passent à 11½ po de large
    out += [A(85.75, 35, 109.75, 37.5, 4, 34.5, "laque-marine", r=0.3, b=0.3),
            A(85.75, 37.5, 109.75, 63, 21.75, 34.5, "laque-marine", r=0.3, b=0.3),
            B(109, 37.5, 109.75, 63, 4, 21.75, "laque-marine"), B(86.5, 50, 109.75, 50.5, 4, 21.75, "laque-marine"),
            A(85.75, 63, 109.75, YN0, 4, 34.5, "laque-marine", r=0.3, b=0.3)]
    out += [B(85.6, 74.6, 85.75, 74.9, 4.5, 34, "carbone"),                        # 2 portes sous le bac
            B(85.6, 63, 85.75, 63.3, 4.5, 34, "carbone"),
            B(85.6, 37.5, 85.75, 63, 21.75, 22.05, "carbone")]
    out += [B(85.75, 37, 109.75, YN0 - 1, 0, 4, "metal"), A(84.75, 35, 109.75, YN0, 34.5, 36, "placage", r=0.3, b=0.3),   # socle, dessus
            A(89, 64, 107, 82, 35.7, 36.1, "inox", r=2.5, b=0.1), B(90, 65, 106, 81, 26, 35.7, "inox"),                  # bac encastré
            T([(108.5, 73, 36), (108.5, 73, 50), (105.5, 73, 52.5), (101, 73, 50)], 0.45, "metal"),                        # robinet
            C(108.4, 78, 0.6, 36, 39, "metal")]
    for (ya, yb), plaque, linge in (((38, 49.5), "laque-vert", "draps"), ((51, 62.5), "laque-marine", "tissu")):
        out += [A(86.6, ya, 108.6, yb, 4.3, 17, "tapis", r=0.8, b=0.5),                                  # panier de toile
                A(88, ya + 1.5, 107, yb - 1.5, 17, 19.2, linge, r=1, b=0.8),                             # linge plié
                B(86.35, (ya + yb) / 2 - 3, 86.6, (ya + yb) / 2 + 3, 12.5, 15.5, plaque),                # plaquette
                B(86.4, (ya + yb) / 2 - 2.5, 86.6, (ya + yb) / 2 + 2.5, 15.9, 16.6, "carbone")]          # poignée découpée
    # capsules de détergent sur la tablette du haut (66 po), hors de portée
    out += [C(37.5, 16, 2.4, 67.5, 72, "blanc"), C(37.5, 16, 2.5, 72, 73, "laque-marine")]
    # déshumidificateur à drain permanent (boyau vers le tuyau d'évacuation de la laveuse), sous la fenêtre à côté de la
    # laveuse : hors du dégagement du panneau électrique et des 36 po devant le chauffe-eau (MAISON-18)
    out += [A(11, 46, 25, 66, 0, 24, "blanc", r=1.5, b=0.6), B(12.5, 48, 23.5, 64, 24, 24.12, "gris"),
            B(25, 50, 25.15, 62, 4, 18, "gris"), B(19, 62.2, 23, 64.2, 24.12, 24.2, "ecran"),
            T([(11.6, 49, 2.5), (10.7, 46, 2), (10.7, 30, 2)], 0.35, "gris")]
    # VRC suspendu au mur avant au-dessus du retour du comptoir ; 4 conduits vers le plafond
    out += [A(70.5, 10.5, 99.5, 27.5, 74, 92, "blanc", r=1, b=0.5), B(78, 27.5, 92, 27.6, 80, 86, "gris"),
            B(83, 27.6, 87, 27.7, 88, 89.5, "ecran")]
    out += [C(x, 19, 2.8, 92, 96, "inox") for x in (75, 81.5, 88.5, 95)]
    out += [B(55, 100, 63, 108, 95.7, 96, "metal"), B(56, 101, 62, 107, 95.6, 95.7, "pneu")]   # évacuation du VRC
    out += _congelateur(h)
    # mélangeur thermostatique à la sortie du chauffe-eau (eau chaude limitée aux appareils)
    out += [C(31, 138, 0.5, 66, 96, "laiton"), C(37, 138, 0.5, 66, 96, "laiton"),
            B(30, 136.6, 38, 139.4, 70, 73.4, "laiton"), h.CY(34, 135.5, 136.6, 71.7, 1.1, "metal")]
    return out


def _congelateur(h):
    """Congélateur vertical ≈ 20 pi³ (32 × 30 × 70 po, blanc comme la laveuse et la sécheuse) dans la niche au bout du comptoir
    de pliage, dos au mur du gym (2 po d'air), face vers la pièce (-x), porte à droite (pentures côté porte du lavage, elle
    s'ouvre en s'éloignant du comptoir où l'on pose l'épicerie) ; prise simple dédiée au-dessus, au mur."""
    A, B, C, T = h.A, h.B, h.C, h.T
    X0, X1, Y0, Y1 = 79.5, 107.75, YN0 + 0.5, YN1 - 0.5          # caisse (x 79½–107¾, y 87–119)
    out = [B(X0 + 1, Y0 + 1, X1 - 0.5, Y1 - 1, 0, 0.6, "carbone"),                     # socle en retrait, pattes
           A(X0, Y0, X1, Y1, 0.6, 70, "blanc", r=1.2, b=0.5),                          # caisse
           A(X0 - 2, Y0, X0 + 0.1, Y1, 4.4, 69.6, "blanc", r=0.8, b=0.5),              # porte (2 po)
           B(X0 - 1.3, Y0 + 1.5, X0, Y1 - 1.5, 0.8, 4, "carbone"),                     # grille du bas
           B(X0 - 2.2, Y1 - 1.6, X0, Y1, 69.6, 70.2, "gris"),                          # penture du haut
           B(X0 - 2.1, 96, X0 - 2, 104, 62, 65, "ecran"), B(X0 - 2.15, 99.3, X0 - 2.1, 100.7, 63, 64, "spot")]   # afficheur
    xp, yp = X0 - 3.6, Y0 + 3.2                                                        # poignée verticale inox, côté comptoir
    out += [C(xp, yp, 0.55, 30, 56, "inox"),
            T([(X0 - 2, yp, 31.5), (xp, yp, 31.5)], 0.4, "inox", bouts=True), T([(X0 - 2, yp, 54.5), (xp, yp, 54.5)], 0.4, "inox", bouts=True)]
    # prise simple dédiée (circuit séparé) au mur au-dessus du congélateur, fiche et cordon qui descend derrière
    out += [B(109.45, 101.5, 109.75, 104.25, 74, 78.5, "blanc"), B(109.38, 102.4, 109.45, 103.35, 75.3, 77.2, "gris"),
            B(108.6, 102.3, 109.38, 103.45, 75.6, 76.9, "pneu"),
            T([(108.9, 102.9, 75.6), (108.9, 102.9, 70.6), (108.3, 102.9, 69.8)], 0.17, "pneu")]
    return out


def _sejour(h, fen=None):
    A, B, C, MOD = h.A, h.B, h.C, h.MOD
    out = []
    # --- banc-rangement à jouets de chêne pleine largeur sous la toile : 143 × 16 po, dessus à 16 po (la barre de lestage,
    #     toile basse, est à ≈ 25 po : rien ne frotte) ; socle noir en retrait de 3 po, 6 tiroirs à fermeture douce,
    #     niche centrale ventilée (boîte de diffusion), ancré au mur
    X0, Y0, Y1 = 430, 12, 155
    out += [B(433, 13, 446, 154, 0, 3, "metal"), A(X0, Y0, 446, Y1, 3, 16, "placage", r=1, b=0.4),
            B(432.7, 13.5, 433, 153.5, 1.4, 2.2, "spot")]                                               # DEL de socle
    gauche = [Y0 + k * (74.5 - Y0) / 3 for k in range(4)]
    droite = [92.5 + k * (Y1 - 92.5) / 3 for k in range(4)]
    for y in gauche[1:] + droite[:-1]:
        out.append(B(X0 - 0.15, y - 0.15, X0 + 0.05, y + 0.15, 3.4, 15.6, "carbone"))                  # joints des tiroirs
    pictos = ["laque-marine", "art-argile", "rouge-velo", "laque-vert", "art-sable", "carbone"]
    k = 0
    for ys in (gauche, droite):
        for a, b in zip(ys, ys[1:]):
            yc = (a + b) / 2
            out += [B(X0 - 0.15, yc - 3.5, X0 + 0.05, yc + 3.5, 13.4, 14.6, "carbone"),                 # poignée découpée
                    B(X0 - 0.12, yc - 2.4, X0 + 0.02, yc + 2.4, 7.2, 10.6, "blanc"),                    # étiquette en image
                    B(X0 - 0.18, yc - 1.2, X0 - 0.12, yc + 1.2, 7.9, 9.9, pictos[k])]
            k += 1
    out += [B(X0 - 0.15, 74.8, X0 + 0.05, 92.2, 3.6, 15.4, "placage")]                                  # porte abattante
    out += [B(X0 - 0.2, 76.5, X0 - 0.15, 90.5, z, z + 0.45, "carbone") for z in (5.5, 7.5, 9.5, 11.5)]   # fentes d'aération
    # barre de son sur le banc ; coussin d'assise des garçons ; plante déplacée sur le bout avant du banc
    out += [A(431.5, 65.5, 437, 101.5, 16, 19.2, "carbone", r=1, b=0.6), B(431.4, 66, 431.5, 101, 16.5, 18.7, "pneu"),
            A(431, 112, 445, 150, 16, 18.4, "tissu", r=1.5, b=1), MOD("plante_sansevieria", 438.5, 19, z=16)]
    # quelques blocs de bois sur le tapis de l'aire de jeu (sol chauffant dessous)
    out += [B(402, 38, 405, 41, 0.5, 3.5, "placage"), B(405.6, 38.4, 408.6, 41.4, 0.5, 3.5, "laque-marine"),
            B(403.8, 38.8, 406.8, 41.8, 3.5, 6.5, "art-argile"), B(398, 46, 404, 49, 0.5, 3.5, "placage")]
    # store à enrouleur sans cordon dans l'embrasure de la fenêtre (y 57–93), à moitié remonté ; il suit l'allège et la tête
    # de ouv-SS-004 (fen = SCENE["fenetres"] ; vidéo DAG, 2026-11-02 : 44 → 80 po ; avant 40 → 86 : mêmes boîtes qu'avant)
    r = (fen or {}).get("ouv-SS-004") or {}
    al, te = r.get("allege", ALLEGE_SS), r.get("tete", 86)
    zb = (al + te) / 2                                                                      # bas du store : mi-hauteur
    out += [h.CY(447.6, 57.5, 92.5, te - 0.9, 0.8, "carbone"), B(447.5, 57.6, 447.7, 92.4, zb, te - 1.6, "tissu"),
            B(447.3, 57.6, 447.9, 92.4, zb - 0.6, zb, "metal")]
    # --- boîte de plancher (2 prises + 2 USB-C) au bout de l'accoudoir, sous un guéridon avec lampe : pas de rallonge
    out += [B(306, 135, 312, 141, 0.5, 0.62, "laiton"), B(307, 136, 311, 140, 0.62, 0.66, "carbone")]
    gx, gy = 312, 140
    out += [C(gx, gy, 6, 0.5, 1, "metal", pans=40), C(gx, gy, 0.8, 1, 21, "metal"), C(gx, gy, 8, 21, 22, "placage", pans=48),
            C(gx, gy, 3, 22, 23, "metal"), C(gx, gy, 0.4, 23, 33, "laiton"), C(gx, gy, 6, 30, 37, "abat-jour", r2=4.5),
            h.T([(gx + 1, gy, 22), (gx + 1, gy, 1.2), (309, 138, 0.7)], 0.12, "pneu")]
    # --- nuage acoustique de lattes de chêne sur feutre noir au plafond (3 panneaux de 24 × 94 po), au-dessus du divan,
    #     entre le projecteur et la toile, hors du faisceau ; encastrés minces entre les panneaux
    out += [B(302, 37, 374, 131, 95.2, 96, "caoutchouc-noir")]
    x = 302.25
    while x < 373.5:
        out.append(B(x, 37, x + 0.75, 131, 94.5, 95.2, "placage"))
        x += 1.25
    out += [C(px, py, 1.6, 94.3, 94.45, "spot") for px in (326, 350) for py in (60, 108)]
    return out


def _fenetres_video():
    """fenetres_video.py (même dossier) : dimensions des fenêtres de la vidéo DAG (MAISON-18, 2026-11-02)."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location(
        "m18_fenetres_video", os.path.join(os.path.dirname(os.path.abspath(__file__)), "fenetres_video.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def appliquer_scene(S, h):
    M = S["mobilier"]
    _retirer_ss16(M)
    # fenêtres descendues par le bas (allège 40 po, tête de l'étage) ; le moteur pose les margelles (terrain à 48 po).
    # MAISON-18 (client, 2026-11-02 : « les fenêtres dans la vidéo sont de bonnes dimensions ») : celles qu'on voit dans la
    # vidéo DAG en prennent les dimensions (fenetres_video.py : séjour et chambre 2 à 44 → 80 po, 3 sections à la façade et
    # dans la chambre 2) ; la chambre 1 (cachée par le deck dans la vidéo) garde l'hypothèse de 40 po
    S["fenetres"] = dict(S.get("fenetres") or {}, **{oid: {"allege": ALLEGE_SS} for oid in FENETRES_BASSES})
    S["fenetres"].update(_fenetres_video().reglages_3d("SS"))
    M += _vestiaire(h) + _nuit(h) + _salle_de_bain(h) + _lavage(h) + _sejour(h, S["fenetres"])
    # l'encastré du séjour sous le nuage devient une lumière intégrée au nuage (la source passe sous les lattes)
    S["lumieres"][:] = [l for l in S["lumieres"] if not (l.get("x") == 330 and l.get("y") == 80 and not l.get("z"))]
    S["lumieres"] += [{"x": 338, "y": 84, "z": 101, "i": 6}]
    V = S["visites"]
    for v in V:
        if v["nom"] == "Vanité":
            v["nom"] = "Vanité (marchepied, crochets des garçons)"
    noms = {v["nom"] for v in V}
    for v in [{"nom": "Casiers d'hiver des garçons", "x": 262, "y": 176, "cap": 48},
              {"nom": "Seuil à neige (porte de côté)", "x": 352, "y": 176, "cap": 8},
              {"nom": "Trajet de nuit vers la salle de bain", "x": 238, "y": 188, "cap": 178},
              {"nom": "Banc à jouets sous la toile", "x": 384, "y": 146, "cap": 322, "commandes": {"toile": "haut"}},
              {"nom": "Paniers de linge des garçons", "x": 36, "y": 58, "cap": 5},
              {"nom": "Congélateur (salle de lavage)", "x": 30, "y": 104, "cap": 2}]:
        if v["nom"] not in noms:
            V.append(v)
    for ligne in S["palette"]:
        if ligne[0] == "Séjour":
            ligne[1] = ligne[1].replace("meuble bas de chêne", "banc à jouets de chêne de 143 po sous la toile, nuage de lattes "
                                        "de chêne au plafond")
        elif ligne[0] == "Salle de lavage":
            ligne[1] += ", congélateur vertical blanc dans une niche au bout du comptoir (prise dédiée)"
        elif ligne[0] == "Vestiaire":
            ligne[1] = ligne[1].replace("banc et cases en chêne", "banc de chêne et bacs d'égouttement")
    S["palette"].append(["Fenêtres (MAISON-18)", "séjour et chambre 2 aux dimensions de la vidéo DAG (allège ≈ 44 po, tête "
                         "≈ 80 po, 3 sections à la façade et dans la chambre 2), chambre 1 agrandie vers le bas (allège ≈ 40 "
                         "po) ; à mesurer ; cadres noirs, margelles de béton ; salle de bain et salle de lavage inchangées",
                         "#1E1E1E"])
    S["palette"].append(["Rangements des garçons (SS-17)", "casiers d'hiver de chêne avec séchoirs à bottes et portes hautes "
                         "vert forêt (comme les armoires gardées), grille à neige encastrée en aluminium noir, banc à jouets "
                         "de chêne, paniers de linge et serviettes à la couleur de chaque garçon (vert forêt, marine), "
                         "veilleuses ambre à 10–13 po", "#B08A5A"])
