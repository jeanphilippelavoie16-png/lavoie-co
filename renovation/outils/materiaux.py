#!/usr/bin/env python3
"""Bibliothèque de matériaux de la maquette 3D (voir catalogue_materiaux.py).

    python3 renovation/outils/materiaux.py telecharger          # cartes ambientCG manquantes (CC0)
    python3 renovation/outils/materiaux.py telecharger --forcer quartz
    python3 renovation/outils/materiaux.py ajouter <clé> <image.jpg> --taille 0.6 [--rugosite 0.3]
    python3 renovation/outils/materiaux.py liste

« ajouter » sert aux fichiers d'un fournisseur (photo de dalle Silestone, décor Egger, carreau de céramiste) :
l'image devient la couleur, le relief est déduit de sa luminance ; on l'ajoute ensuite à CATALOGUE avec
"source": "fournisseur" et la taille réelle de l'image en mètres.
"""
import argparse, io, json, os, sys, urllib.request, zipfile

ICI = os.path.dirname(os.path.abspath(__file__))
DOSSIER = os.path.join(ICI, "materiaux")
sys.path.insert(0, ICI)
from catalogue_materiaux import CATALOGUE  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0 (lavoie-co, maquette 3D)"}
TAILLE_COULEUR, TAILLE_CARTES = 1024, 512


def _get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()


def _sauver(im, chemin, taille, gris=False):
    from PIL import Image
    im = im.convert("L" if gris else "RGB").resize((taille, taille), Image.LANCZOS)
    im.save(chemin, quality=82, optimize=True)


def telecharger(cle, forcer=False):
    from PIL import Image
    e = CATALOGUE[cle]
    d = os.path.join(DOSSIER, cle)
    if e["source"] not in ("ambientcg", "polyhaven") or (os.path.isfile(os.path.join(d, "relief.jpg")) and not forcer):
        return False
    if e["source"] == "ambientcg":
        z = zipfile.ZipFile(io.BytesIO(_get(f"https://ambientcg.com/get?file={e['id']}_1K-JPG.zip")))
        noms = {n.rsplit("_", 1)[-1].lower(): n for n in z.namelist()}
        ouvre = lambda k: Image.open(io.BytesIO(z.read(noms[k])))
        url, fichier = f"https://ambientcg.com/view?id={e['id']}", f"{e['id']}_1K-JPG.zip"
    else:                                        # Poly Haven : une image par carte
        base = f"https://dl.polyhaven.org/file/ph-assets/Textures/jpg/1k/{e['id']}/{e['id']}"
        cartes = {"color.jpg": "_diff_1k.jpg", "normalgl.jpg": "_nor_gl_1k.jpg", "roughness.jpg": "_rough_1k.jpg"}
        noms = dict.fromkeys(cartes)
        ouvre = lambda k: Image.open(io.BytesIO(_get(base + cartes[k])))
        url, fichier = f"https://polyhaven.com/a/{e['id']}", e["id"] + "_*_1k.jpg"
    os.makedirs(d, exist_ok=True)
    if not e.get("relief_seul"):
        im = ouvre("color.jpg").convert("RGB")
        aj = e.get("ajustement") or {}            # pour rapprocher la photo du produit voulu (chêne pâle, quartz blanc)
        from PIL import ImageEnhance
        if "saturation" in aj:
            im = ImageEnhance.Color(im).enhance(aj["saturation"])
        if "luminosite" in aj:
            im = ImageEnhance.Brightness(im).enhance(aj["luminosite"])
        _sauver(im, os.path.join(d, "couleur.jpg"), TAILLE_COULEUR)
    _sauver(ouvre("normalgl.jpg"), os.path.join(d, "relief.jpg"), TAILLE_CARTES)
    if "roughness.jpg" in noms:
        _sauver(ouvre("roughness.jpg"), os.path.join(d, "rugosite.jpg"), TAILLE_CARTES, gris=True)
    json.dump({"source": {"ambientcg": "ambientCG", "polyhaven": "Poly Haven"}[e["source"]], "id": e["id"],
               "licence": "CC0 1.0 (domaine public)", "url": url, "fichier": fichier, "ajustement": e.get("ajustement")},
              open(os.path.join(d, "source.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return True


def ajouter(cle, image, taille, rugosite):
    """Image de fournisseur → couleur + relief déduit (Sobel sur la luminance) + rugosité constante."""
    import numpy as np
    from PIL import Image, ImageFilter
    d = os.path.join(DOSSIER, cle)
    os.makedirs(d, exist_ok=True)
    im = Image.open(image).convert("RGB")
    c = min(im.size)
    im = im.crop(((im.width - c) // 2, (im.height - c) // 2, (im.width + c) // 2, (im.height + c) // 2))
    _sauver(im, os.path.join(d, "couleur.jpg"), TAILLE_COULEUR)
    h = np.asarray(im.convert("L").resize((TAILLE_CARTES, TAILLE_CARTES)).filter(ImageFilter.GaussianBlur(1)), float) / 255
    gx = np.roll(h, -1, 1) - np.roll(h, 1, 1)
    gy = np.roll(h, -1, 0) - np.roll(h, 1, 0)
    n = np.dstack([-gx * 2, gy * 2, np.ones_like(h)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    Image.fromarray(((n * 0.5 + 0.5) * 255).astype("uint8")).save(os.path.join(d, "relief.jpg"), quality=85)
    Image.new("L", (8, 8), int(rugosite * 255)).save(os.path.join(d, "rugosite.jpg"))
    json.dump({"source": "fournisseur", "fichier_original": os.path.basename(image), "taille_m": taille},
              open(os.path.join(d, "source.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{cle} : ajouté dans {d}. Ajoute-le à CATALOGUE : "
          f'"{cle}": {{"source": "fournisseur", "taille_m": {taille}, "usage": "..."}}')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    t = sp.add_parser("telecharger"); t.add_argument("cles", nargs="*"); t.add_argument("--forcer", action="store_true")
    a = sp.add_parser("ajouter"); a.add_argument("cle"); a.add_argument("image")
    a.add_argument("--taille", type=float, required=True, help="largeur réelle de l'image, en mètres")
    a.add_argument("--rugosite", type=float, default=0.4)
    sp.add_parser("liste")
    o = ap.parse_args()
    if o.cmd == "telecharger":
        for k in o.cles or sorted(CATALOGUE):
            print(k, "téléchargé" if telecharger(k, o.forcer) else "déjà là")
    elif o.cmd == "ajouter":
        ajouter(o.cle, o.image, o.taille, o.rugosite)
    else:
        for k, e in sorted(CATALOGUE.items()):
            ok = os.path.isfile(os.path.join(DOSSIER, k, "relief.jpg"))
            print(f"{k:14} {e['source']:10} {e.get('id', ''):13} {e['taille_m']:>5} m  {'ok' if ok else 'manquant'}  {e['usage']}")


if __name__ == "__main__":
    main()
