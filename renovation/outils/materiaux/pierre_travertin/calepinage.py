#!/usr/bin/env python3
"""Cartes du matériau « pierre_travertin » : travertin beige-gris pâle adouci (mat), en dalles verticales de 24 × 48 po
à joints fins, composées à partir d'ambientCG Travertine009 (CC0, échantillon de 120 × 120 cm, cartes 1K).

Une répétition de la texture couvre 96 × 96 po (2,4384 m) : 4 dalles de large × 2 de haut, chacune taillée à sa vraie
grandeur dans l'échantillon (veines verticales, comme une dalle coupée dans le sens du lit), une dalle sur deux tournée
de 180° pour varier. Joints de 1/16 po à peine plus foncés, rainure légère dans le relief. Les joints verticaux tombent
à x ≡ 23½ po (mod 24) dans le repère de la maison (axe du bain de SS-16 et bords de sa niche), les joints horizontaux
au plancher et à 48 po.

    python3 renovation/outils/materiaux/pierre_travertin/calepinage.py      (télécharge l'échantillon si besoin)
"""
import io, json, os, sys, urllib.request, zipfile
import numpy as np
from PIL import Image, ImageEnhance

ICI = os.path.dirname(os.path.abspath(__file__))
ID, ECH_M = "Travertine009", 1.20                # échantillon ambientCG : 120 × 120 cm
REP_PO, PX = 96, 2048                            # répétition 96 po ; couleur 2048 px (≈ 21 px/po), relief 1024 px
DALLE = (24, 48)                                 # largeur × hauteur (po), pose verticale
DECALAGE_X = 23.5                                # joints verticaux à x ≡ 23½ po (mod 24)
SATURATION, LUMINOSITE = 0.45, 0.97              # beige-gris pâle (l'échantillon est plus jaune)


def source():
    z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(urllib.request.Request(
        f"https://ambientcg.com/get?file={ID}_1K-JPG.zip", headers={"User-Agent": "Mozilla/5.0 (lavoie-co, maquette 3D)"}),
        timeout=120).read()))
    lis = lambda k: Image.open(io.BytesIO(z.read(next(n for n in z.namelist() if n.endswith(k)))))
    return lis("_Color.jpg").convert("RGB"), lis("_NormalGL.jpg").convert("RGB")


def composer(src, n, taille, normale=False):
    """Une répétition de taille px : dalles taillées dans src (tournée de 90° : veines verticales), à l'échelle réelle."""
    a = np.asarray(src.rotate(90, expand=True), float)
    if normale:                                  # rotation de 90° (antihoraire) du vecteur (nx, ny) → (-ny, nx)
        nx, ny = a[..., 0] / 127.5 - 1, a[..., 1] / 127.5 - 1
        a = a.copy(); a[..., 0], a[..., 1] = (-ny + 1) * 127.5, (nx + 1) * 127.5
    s_px = a.shape[0] / (ECH_M / 0.0254)        # px de l'échantillon par pouce
    o_px = taille / REP_PO                       # px de la sortie par pouce
    out = np.zeros((taille, taille, 3))
    rng = np.random.default_rng(9)
    for j in range(REP_PO // DALLE[1]):
        for i in range(REP_PO // DALLE[0]):
            w, h = round(DALLE[0] * s_px), round(DALLE[1] * s_px)
            x0, y0 = rng.integers(0, a.shape[1]), rng.integers(0, a.shape[0])
            ys, xs = (np.arange(h) + y0) % a.shape[0], (np.arange(w) + x0) % a.shape[1]
            d = a[np.ix_(ys, xs)]
            if (i + j) % 2:                      # dalle tournée de 180°
                d = d[::-1, ::-1].copy()
                if normale:
                    d[..., 0], d[..., 1] = 255 - d[..., 0], 255 - d[..., 1]
            W, H = round(DALLE[0] * o_px), round(DALLE[1] * o_px)
            d = np.asarray(Image.fromarray(d.clip(0, 255).astype("uint8")).resize((W, H), Image.LANCZOS), float)
            out[j * H:(j + 1) * H, i * W:(i + 1) * W] = d
    # joints : bords gauche/droit (verticaux) et haut/bas (horizontaux) de chaque dalle, 1/16 po
    e = max(1, round(o_px / 16))
    jx = [round(k * DALLE[0] * o_px) for k in range(REP_PO // DALLE[0])]
    jy = [round(k * DALLE[1] * o_px) for k in range(REP_PO // DALLE[1])]
    for x in jx:
        for k, f in ((-e, 0.4), (0, 0.4)):       # deux demi-joints de part et d'autre du bord
            sl = np.s_[:, (x + k) % taille: (x + k) % taille + e]
            out[sl] = (out[sl] * 0.86 + 0.14 * 140) if not normale else _rainure(out[sl], (1 if k else -1), 0)
    for y in jy:
        for k in (-e, 0):
            sl = np.s_[(y + k) % taille: (y + k) % taille + e, :]
            out[sl] = (out[sl] * 0.86 + 0.14 * 140) if not normale else _rainure(out[sl], 0, (-1 if k else 1))
    # décalage : joint vertical à x ≡ DECALAGE_X (mod 24) dans le repère de la maison (u = x / 96 po)
    out = np.roll(out, round(DECALAGE_X * o_px), axis=1)
    return Image.fromarray(out.clip(0, 255).astype("uint8"))


def _rainure(p, sx, sy):
    """Petite pente de chaque côté du joint (normales OpenGL : G = +y vers le haut de l'image)."""
    p = p.copy()
    p[..., 0], p[..., 1], p[..., 2] = 127.5 + sx * 70, 127.5 + sy * 70, 230
    return p


def main():
    coul, nor = source()
    coul = ImageEnhance.Brightness(ImageEnhance.Color(coul).enhance(SATURATION)).enhance(LUMINOSITE)
    composer(coul, 0, PX).save(os.path.join(ICI, "couleur.jpg"), quality=86, optimize=True)
    composer(nor, 0, PX // 2, normale=True).save(os.path.join(ICI, "relief.jpg"), quality=88, optimize=True)
    json.dump({"source": "ambientCG", "id": ID, "licence": "CC0 1.0 (domaine public)", "url": f"https://ambientcg.com/view?id={ID}",
               "fichier": f"{ID}_1K-JPG.zip", "echantillon_m": ECH_M,
               "calepinage": "dalles verticales 24 × 48 po, joints 1/16 po ; répétition 96 × 96 po (2,4384 m) ; calepinage.py",
               "ajustement": {"saturation": SATURATION, "luminosite": LUMINOSITE}},
              open(os.path.join(ICI, "source.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("pierre_travertin : cartes écrites dans", ICI)


if __name__ == "__main__":
    sys.exit(main())
