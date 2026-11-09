#!/usr/bin/env python3
"""Plan final d'un projet : les feuilles du PDF du projet sur UNE page, l'une au-dessus de l'autre (l'étage le plus haut en
haut), avec un bandeau de titre et, en bas, le lien de la visite 3D (lien cliquable et code QR).

Usage :
    python3 renovation/outils/plan_final.py <dossier du projet> --lien https://claude.ai/artifact/...

Lit pdf/<nom_pdf> (produit par construire_projet.py) et donnees/maison.json ; écrit pdf/<proposition>_plan_final.pdf et
un aperçu png/<proposition>_plan_final.png. À relancer après chaque construire_projet.py.

Les feuilles gardent leur taille (17 × 11 po, à l'échelle) : la page assemblée fait 17 po de large et un peu moins de 25 po
de haut. Imprimée sur une seule feuille, elle est réduite : l'échelle graphique de chaque feuille reste juste, pas l'échelle
écrite. Pour l'échelle exacte, imprimer le PDF du projet (une feuille 11 × 17 par niveau).
Le code QR demande le module qrcode (pip install qrcode) ; sans lui, la page n'a que le lien.
"""
import argparse, io, json, os, re, subprocess, sys
from xml.sax.saxutils import escape

import cairosvg
from pypdf import PageObject, PdfReader, PdfWriter, Transformation
from pypdf.annotations import Link

PT = 72.0                   # points par pouce
TETE = 0.9 * PT             # bandeau de titre
PIED = 1.9 * PT             # bandeau du lien
POLICE = "Arial, Helvetica, sans-serif"       # celle des feuilles (Liberation Sans ici)


def svg_bandeau(largeur, hauteur, corps):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{largeur}pt" height="{hauteur}pt" '
            f'viewBox="0 0 {largeur} {hauteur}">{corps}</svg>')


def page_svg(svg):
    return PdfReader(io.BytesIO(cairosvg.svg2pdf(bytestring=svg.encode("utf-8")))).pages[0]


def qr_svg(lien, x, y, cote):
    """Code QR en carrés SVG (x, y : coin haut-gauche, cote : côté en points), ou '' sans le module qrcode."""
    try:
        import qrcode
    except ImportError:
        return ""
    q = qrcode.QRCode(border=0, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(lien)
    q.make(fit=True)
    m = q.get_matrix()
    n = len(m)
    t = cote / n
    carres = []
    for j, rang in enumerate(m):
        i = 0
        while i < n:                                 # une bande par suite de modules noirs (fichier plus léger)
            if rang[i]:
                k = i
                while k < n and rang[k]:
                    k += 1
                carres.append(f"M{x + i * t:.2f} {y + j * t:.2f}h{(k - i) * t:.2f}v{t:.2f}h{-(k - i) * t:.2f}z")
                i = k
            else:
                i += 1
    return f'<path d="{"".join(carres)}" fill="#000"/>'


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("dossier")
    ap.add_argument("--lien", required=True, help="adresse de la visite 3D publiée")
    a = ap.parse_args()
    dossier = os.path.abspath(a.dossier)
    maison = json.load(open(os.path.join(dossier, "donnees", "maison.json"), encoding="utf-8"))
    projet = maison.get("projet") or {}
    nom_pdf = projet.get("nom_pdf") or (os.path.basename(dossier) + ".pdf")
    source = PdfReader(os.path.join(dossier, "pdf", nom_pdf))

    # une page du PDF par niveau, dans l'ordre des niveaux (du plus bas au plus haut) ; on la reconnaît à son numéro de feuille
    niveaux = [n for n in maison.get("niveaux") or [] if isinstance(n, dict)]
    pages = list(source.pages)
    feuilles = []
    for k, niv in enumerate(niveaux):
        code = str(niv.get("feuille") or "")
        p = next((pg for pg in pages if code and code in (pg.extract_text() or "")), pages[k] if k < len(pages) else None)
        if p is not None:
            feuilles.append((niv, p))
    feuilles.reverse()                               # l'étage le plus haut en haut de la page
    if not feuilles:
        sys.exit("Aucune feuille dans " + nom_pdf)

    L = max(float(p.mediabox.width) for _, p in feuilles)
    H = TETE + sum(float(p.mediabox.height) for _, p in feuilles) + PIED

    adresse = escape(str(projet.get("nom") or ""))
    prop = str(projet.get("proposition") or os.path.basename(dossier))
    rev, date = escape(str(projet.get("revision") or "")), escape(str(projet.get("date") or ""))
    place = lambda i: "" if len(feuilles) == 1 else ("en haut" if i == 0 else ("en bas" if i == len(feuilles) - 1 else "au milieu")) + " : "
    ordre = " · ".join(f'{place(i)}'
                       f'{escape(str(n.get("nom") or ""))} ({escape(str(n.get("feuille") or ""))})'
                       for i, (n, _) in enumerate(feuilles))
    tete = svg_bandeau(L, TETE,
        f'<rect x="0" y="0" width="{L}" height="{TETE}" fill="#fff"/>'
        f'<text x="36" y="30" font-family="{POLICE}" font-size="20" font-weight="bold">{adresse} — plan final {escape(prop)}</text>'
        f'<text x="36" y="52" font-family="{POLICE}" font-size="12.5" fill="#333">Révision {rev}, {date} · {ordre}</text>'
        f'<line x1="36" y1="{TETE - 2}" x2="{L - 36}" y2="{TETE - 2}" stroke="#000" stroke-width="1"/>')

    cote = 1.45 * PT
    xq, yq = 36, (PIED - cote) / 2
    qr = qr_svg(a.lien, xq, yq, cote)
    xt = xq + cote + 22 if qr else 36
    lignes = [("Visite 3D", 17, "bold", "#000"),
              (escape(a.lien), 15, "normal", "#0645ad"),
              ("Touchez le lien" + (" ou balayez le code avec le téléphone" if qr else "") + " pour faire la visite.",
               11.5, "normal", "#333"),
              ("Lien privé : il s'ouvre avec le compte du propriétaire ; pour le donner à quelqu'un, le partager d'abord "
               "(menu Partager de la page).", 11.5, "normal", "#333"),
              ("Feuilles à l'échelle de leur cartouche sur 11 × 17 : imprimer " + escape(nom_pdf) +
               ". Sur cette page assemblée, se fier à l'échelle graphique de chaque feuille.", 11.5, "normal", "#333")]
    y, corps = yq + 14, ""
    rect_lien = None
    for i, (t, f, g, c) in enumerate(lignes):
        corps += (f'<text x="{xt}" y="{y:.1f}" font-family="{POLICE}" font-size="{f}" font-weight="{g}" fill="{c}"'
                  f'{" text-decoration=\"underline\"" if i == 1 else ""}>{t}</text>')
        if i == 1:
            rect_lien = (xt - 2, y - f, xt + 0.53 * f * len(a.lien) + 2, y + 4)     # zone cliquable (coordonnées du bandeau)
        y += f + 9
    pied = svg_bandeau(L, PIED, f'<rect x="0" y="0" width="{L}" height="{PIED}" fill="#fff"/>'
                                f'<line x1="36" y1="1" x2="{L - 36}" y2="1" stroke="#000" stroke-width="1"/>' + qr + corps)

    page = PageObject.create_blank_page(width=L, height=H)
    page.merge_transformed_page(page_svg(tete), Transformation().translate(0, H - TETE))
    yb = H - TETE
    for _, p in feuilles:
        h = float(p.mediabox.height)
        yb -= h
        page.merge_transformed_page(p, Transformation().translate(-float(p.mediabox.left), yb - float(p.mediabox.bottom)))
    page.merge_transformed_page(page_svg(pied), Transformation().translate(0, 0))

    w = PdfWriter()
    w.add_page(page)
    # liens : l'adresse et le code QR (le bandeau du pied est en bas de la page : y du PDF = PIED - y du bandeau)
    zones = [rect_lien] + ([(xq, yq, xq + cote, yq + cote)] if qr else [])
    for x0, y0, x1, y1 in zones:
        w.add_annotation(page_number=0, annotation=Link(rect=(x0, PIED - y1, x1, PIED - y0), url=a.lien))
    w.add_metadata({"/Title": f"Plan final {prop} — {projet.get('nom') or ''}", "/Subject": f"Révision {projet.get('revision') or ''}, "
                    f"{projet.get('date') or ''}", "/Creator": "plan_final.py", "/Producer": "plan_final.py"})
    dt = re.sub(r"\D", "", str(projet.get("date") or ""))[:8]
    if dt:
        w.add_metadata({"/CreationDate": f"D:{dt}000000", "/ModDate": f"D:{dt}000000"})
    sortie = os.path.join(dossier, "pdf", f"{prop}_plan_final.pdf")
    with open(sortie, "wb") as fh:
        w.write(fh)
    apercu = os.path.join(dossier, "png", f"{prop}_plan_final")
    try:
        subprocess.run(["pdftoppm", "-png", "-r", "90", "-singlefile", sortie, apercu], check=True)
        print("aperçu :", os.path.relpath(apercu + ".png"))
    except (OSError, subprocess.CalledProcessError):
        print("aperçu non produit (pdftoppm absent)")
    print("plan final :", os.path.relpath(sortie), f"({L / PT:.0f} × {H / PT:.1f} po ;", ordre.replace("&amp;", "&") + ")")


if __name__ == "__main__":
    main()
