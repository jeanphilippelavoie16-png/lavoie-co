"""CH-01, version 2 — la murale « Camp de base » du mur de gauche (l'ancien mur vert) et la palette du thème.

Thème : expédition nordique, version graphique et moderne (aplats, formes simples, lignes nettes ; bois et noir mat en
rappel). Pas de personnages ni de héros sous licence. Le jour du côté de la fenêtre (soleil), la nuit du côté des lits
(lune et étoiles) ; les deux enseignes de bois des gars flottent dans le ciel.

    python3 renovation/CH-01_chambre_garcons/murale.py      → murale/murale_camp.png (image de la maquette)
                                                              et murale/murale_camp_fiche.png (fiche pour le peintre)

scene_3d.py l'appelle (ecrire()) à chaque génération : l'image suit toujours la palette et geometrie.py.
Couleurs : teintes d'écran « à valider sur échantillon » (voir DESIGN.md, aucune référence de nuancier n'est certaine).
Repère : celui de la maison (pouces) ; la murale couvre le mur x = 10 de y = 10 (façade) à y = 139,75 (mur des lits), du
dessus de la plinthe (z = 4) au plafond (z = 96). Vue de la chambre, la façade est à gauche, les lits à droite.
"""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import geometrie as G  # noqa: E402

# nom : (hex à l'écran, alias du mobilier, où ça va) — à valider sur échantillon
PALETTE = {
    "Blanc nuage": ("#F3EFE7", "blanc-nuage", "3 murs et garde-robe (plafond : blanc pur mat)"),
    "Ciel du matin": ("#CDE5F1", "ciel-matin", "ciel de jour de la murale (côté fenêtre)"),
    "Bleu nuit doux": ("#7B8CC2", "bleu-nuit", "ciel de nuit de la murale (au-dessus des lits)"),
    "Bleu fjord": ("#77A6C8", "bleu-fjord", "grandes montagnes, portes des armoires hautes"),
    "Sauge": ("#A9C2A0", "sauge", "montagnes du milieu, bac des dinos, bacs de G.-R."),
    "Sapin doux": ("#5F8A6C", "sapin", "petits sapins de la murale"),
    "Terracotta": ("#DC9572", "terracotta", "collines, bac des autos, coussin, bordure du tapis"),
    "Moutarde": ("#E2A93F", "moutarde", "soleil, lune, tente, bac des Lego (comme les draps)"),
    "Neige": ("#FBF8F1", "neige", "neige des sommets, étoiles"),
    "Sable": ("#E8D9BD", "sable", "grand tapis, boîtes de la tablette haute"),
    "Noir mat": ("#1E1F20", "noir-mat", "quincaillerie, consoles, suspension (existante)"),
}
HEX = {k: v[0] for k, v in PALETTE.items()}

Y0, Y1, Z0, Z1 = G.MURALE
S = 12                      # px par pouce de l'image de la maquette
SUR = 3                     # suréchantillonnage (bords nets)

# formes (y, z) en pouces
MONT_FOND = [(Y0, Z0), (Y0, 37), (26, 57), (43, 36), (92, 70), (Y1, 35), (Y1, Z0)]           # bleu fjord
NEIGE = [[(20.2, 50.0), (26, 57), (32.0, 50.2), (29.4, 51.6), (27.0, 49.4), (24.2, 51.8)],      # sommets enneigés
         [(83.2, 56.2), (92, 70), (101.4, 58.9), (97.4, 60.6), (94.4, 57.8), (91.2, 61.0), (87.8, 57.4)]]
MONT_MILIEU = [(Y0, Z0), (Y0, 27), (19, 35), (35, 21), (60, 46), (79, 25), (115, 50), (Y1, 31), (Y1, Z0)]   # sauge
COLLINES = [(31, 4, 25, 15), (88, 4, 30, 12), (130, 4, 20, 17)]                                  # terracotta : y, z, ry, rz
SAPINS = [(66.0, 15.0, 3.2, 12.0), (71.5, 13.5, 2.6, 10.0), (114.0, 19.5, 3.0, 11.0)]          # y, z du pied, demi-largeur, hauteur
TENTE = (44.0, 16.0, 6.5, 9.0)                                                                  # y centre, z sol, demi-largeur, hauteur
SOLEIL = (30.0, 76.0, 8.0)
NUIT = (Y1, Z1, 50.0)                                                                           # ciel de nuit : quart de disque dans le coin des lits (y, z, rayon)
LUNE = (124.0, 84.0, 5.5)
ETOILES = [(100.5, 88.5, 1.6), (108.0, 76.5, 1.2), (115.5, 91.0, 1.0), (133.5, 89.0, 1.5), (130.5, 73.5, 1.1),
           (104.0, 69.5, 0.9), (119.5, 72.0, 0.8), (136.0, 80.0, 0.7), (97.0, 79.0, 0.8)]


def _rgb(h, a=255):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (a,)


def dessiner(s=S, sur=SUR, avec_cadre=False):
    """Image RGBA (opaque) de la murale : s px par pouce."""
    from PIL import Image, ImageDraw
    k = s * sur
    W, H = round((Y1 - Y0) * k), round((Z1 - Z0) * k)
    im = Image.new("RGBA", (W, H), _rgb(HEX["Ciel du matin"]))
    d = ImageDraw.Draw(im)
    P = lambda y, z: ((y - Y0) * k, (Z1 - z) * k)
    poly = lambda pts, c: d.polygon([P(*q) for q in pts], fill=_rgb(c))
    y, z, r = NUIT                                                                            # ciel de nuit (arc)
    d.ellipse([P(y - r, z + r), P(y + r, z - r)], fill=_rgb(HEX["Bleu nuit doux"]))
    y, z, r = SOLEIL
    d.ellipse([P(y - r, z + r), P(y + r, z - r)], fill=_rgb(HEX["Moutarde"]))
    y, z, r = LUNE                                                                            # croissant
    d.ellipse([P(y - r, z + r), P(y + r, z - r)], fill=_rgb(HEX["Moutarde"]))
    d.ellipse([P(y - r + 2.6, z + r + 0.8), P(y + r + 2.6, z - r + 0.8)], fill=_rgb(HEX["Bleu nuit doux"]))
    for y, z, r in ETOILES:                                                                   # étoiles à 4 branches
        poly([(y - r, z), (y - r * 0.22, z + r * 0.22), (y, z + r), (y + r * 0.22, z + r * 0.22), (y + r, z),
              (y + r * 0.22, z - r * 0.22), (y, z - r), (y - r * 0.22, z - r * 0.22)], HEX["Neige"])
    poly(MONT_FOND, HEX["Bleu fjord"])
    for n in NEIGE:
        poly(n, HEX["Neige"])
    poly(MONT_MILIEU, HEX["Sauge"])
    for y, z, ry, rz in COLLINES:
        d.ellipse([P(y - ry, z + rz), P(y + ry, z - rz)], fill=_rgb(HEX["Terracotta"]))
    for y, z, w, h in SAPINS:                                                                 # sapins : 3 étages et un tronc
        d.rectangle([P(y - 0.45, z + 1.6), P(y + 0.45, z)], fill=_rgb(HEX["Noir mat"]))
        for j in range(3):
            zb = z + 1.4 + j * h * 0.27
            ww = w * (1 - 0.22 * j)
            poly([(y - ww, zb), (y, zb + h * 0.42), (y + ww, zb)], HEX["Sapin doux"])
    y, z, w, h = TENTE                                                                        # tente moutarde, porte noire
    poly([(y - w, z), (y, z + h), (y + w, z)], HEX["Moutarde"])
    poly([(y - w * 0.32, z), (y, z + h * 0.48), (y + w * 0.32, z)], HEX["Noir mat"])
    d.line([P(y, z + h), P(y, z + h + 2.4)], fill=_rgb(HEX["Noir mat"]), width=max(1, round(0.3 * k)))
    poly([(y, z + h + 2.4), (y + 2.2, z + h + 1.8), (y, z + h + 1.2)], HEX["Terracotta"])    # fanion
    im = im.resize((round((Y1 - Y0) * s), round((Z1 - Z0) * s)), Image.LANCZOS)
    if avec_cadre:
        im = _fiche(im, s)
    return im


def _fiche(im, s):
    """Fiche pour le peintre : la murale, les enseignes en pointillé, la plinthe chauffante et le lit, la palette."""
    from PIL import Image, ImageDraw, ImageFont
    marge, bas = 40, 330
    F = Image.new("RGB", (im.width + 2 * marge, im.height + marge + bas), (255, 255, 255))
    F.paste(im.convert("RGB"), (marge, marge))
    d = ImageDraw.Draw(F)
    P = lambda y, z: (marge + (y - Y0) * s, marge + (Z1 - z) * s)
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
        fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except OSError:
        f = fb = ImageFont.load_default()

    def tirets(y0, z0, y1, z1, c=(40, 40, 40)):
        for (a, b) in (((y0, z0), (y1, z0)), ((y1, z0), (y1, z1)), ((y1, z1), (y0, z1)), ((y0, z1), (y0, z0))):
            n = 40
            for i in range(0, n, 2):
                p = [P(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n),
                     P(a[0] + (b[0] - a[0]) * (i + 1) / n, a[1] + (b[1] - a[1]) * (i + 1) / n)]
                d.line(p, fill=c, width=2)
    dy, dz = G.ENSEIGNES_DY, G.ENSEIGNES_DZ
    tirets(64.5 + dy, 56.4 + dz, 102.5 + dy, 69.9 + dz)
    d.text(P(66 + dy, 69.5 + dz), "enseigne Pierre-Alexis", fill=(30, 30, 30), font=f)
    tirets(56.0 + dy, 37.7 + dz, 95.5 + dy, 50.5 + dz)
    d.text(P(57.5 + dy, 50.1 + dz), "enseigne Louis-Charles", fill=(30, 30, 30), font=f)
    tirets(G.PC_GAUCHE[1], Z0, G.PC_GAUCHE[3], G.PC_Z[1], (200, 40, 40))
    d.text(P(G.PC_GAUCHE[1] + 1, G.PC_Z[1] + 3.5), "plinthe chauffante (on peint derrière avant de la remettre, au besoin)",
           fill=(200, 40, 40), font=f)
    tirets(G.LITS[1], Z0, G.LITS[3], 64.5, (40, 40, 160))
    d.text(P(G.LITS[1] + 2, 63.0), "lits superposés (le bas de la murale est caché)", fill=(40, 40, 160), font=f)
    y = im.height + marge + 18
    d.text((marge, y), "CH-01 — Murale « Camp de base », mur de gauche : 10'-9¾\" × 7'-8\" (plinthe → plafond)."
                       "", fill=(20, 20, 20), font=fb)
    d.text((marge, y + 22), "Couleurs d'écran : à valider sur échantillon (aucune référence de nuancier n'est certaine).", fill=(90, 90, 90), font=f)
    x, y = marge, y + 52
    for nom, (hx, _, usage) in PALETTE.items():
        d.rectangle([x, y, x + 34, y + 34], fill=_rgb(hx)[:3], outline=(120, 120, 120))
        d.text((x + 42, y + 1), f"{nom}  {hx}", fill=(20, 20, 20), font=fb)
        d.text((x + 42, y + 19), usage[:62], fill=(70, 70, 70), font=f)
        x += 520
        if x + 500 > F.width:
            x, y = marge, y + 46
    return F


def ecrire():
    """Écrit murale/murale_camp.png (maquette) et murale/murale_camp_fiche.png ; retourne le chemin relatif de la première."""
    dos = os.path.join(ICI, "murale")
    os.makedirs(dos, exist_ok=True)
    im = dessiner()
    im.save(os.path.join(dos, "murale_camp.png"), optimize=True)       # RGBA : gardée telle quelle par generer_3d.py
    dessiner(s=8, avec_cadre=True).save(os.path.join(dos, "murale_camp_fiche.png"), optimize=True)
    return "murale/murale_camp.png"


if __name__ == "__main__":
    print(ecrire())
