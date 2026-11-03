#!/usr/bin/env python3
"""Phase 0 — prétraitement des photos de plans.

Pour chaque photo : redressement de perspective (si la feuille entière est visible),
rotation pour lire le texte à l'endroit (rue en bas de la feuille), amélioration du
contraste (CLAHE), puis découpe en tuiles zoomées ×2 qui se chevauchent.

Usage : python3 pretraitement.py <dossier_photos_Pn.jpg> <dossier_sortie>
"""
import sys, os, json
import cv2
import numpy as np

# Pn : (rotation pour texte à l'endroit, redresser la feuille ?, grille tuiles (cols, rangées))
PHOTOS = {
    "P1": dict(rot=cv2.ROTATE_90_COUNTERCLOCKWISE, redresser=False, grille=(5, 4)),
    "P2": dict(rot=cv2.ROTATE_90_COUNTERCLOCKWISE, redresser=False, grille=(3, 3)),
    "P3": dict(rot=cv2.ROTATE_90_COUNTERCLOCKWISE, redresser=False, grille=(5, 4)),
    "P4": dict(rot=cv2.ROTATE_90_COUNTERCLOCKWISE, redresser=True, grille=(3, 3)),
    "P5": dict(rot=None, redresser=False, grille=(2, 2)),
    "P6": dict(rot=cv2.ROTATE_90_COUNTERCLOCKWISE, redresser=True, grille=(3, 3)),
    "P7": dict(rot=cv2.ROTATE_90_COUNTERCLOCKWISE, redresser=False, grille=(5, 4)),
}


def ordonner(pts):
    pts = pts.reshape(4, 2).astype(np.float32)
    s, d = pts.sum(1), np.diff(pts, axis=1).ravel()
    return np.array([pts[s.argmin()], pts[d.argmin()], pts[s.argmax()], pts[d.argmax()]], np.float32)


def redresser(img):
    """Trouve le quadrilatère de la feuille (papier clair sur fond foncé) et le redresse."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    masque = ((hsv[..., 2] > 150) & (hsv[..., 1] < 90)).astype(np.uint8) * 255
    masque = cv2.morphologyEx(masque, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    cnts, _ = cv2.findContours(masque, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # le pli de la feuille peut la couper en deux : on réunit les grands morceaux
    gros = [c for c in cnts if cv2.contourArea(c) > 0.05 * img.shape[0] * img.shape[1]]
    if not gros:
        return img, None
    hull = cv2.convexHull(np.vstack(gros))
    if cv2.contourArea(hull) < 0.4 * img.shape[0] * img.shape[1]:
        return img, None
    approx = None
    for eps in np.linspace(0.01, 0.08, 15):
        a = cv2.approxPolyDP(hull, eps * cv2.arcLength(hull, True), True)
        if len(a) == 4:
            approx = a
            break
    if approx is None:
        return img, None
    q = ordonner(approx)
    w = int(max(np.linalg.norm(q[1] - q[0]), np.linalg.norm(q[2] - q[3])))
    h = int(max(np.linalg.norm(q[3] - q[0]), np.linalg.norm(q[2] - q[1])))
    M = cv2.getPerspectiveTransform(q, np.array([[0, 0], [w, 0], [w, h], [0, h]], np.float32))
    return cv2.warpPerspective(img, M, (w, h), flags=cv2.INTER_CUBIC), q.tolist()


def contraste(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8)).apply(lab[..., 0])
    out = cv2.cvtColor(cv2.merge([l, lab[..., 1], lab[..., 2]]), cv2.COLOR_LAB2BGR)
    flou = cv2.GaussianBlur(out, (0, 0), 2)
    return cv2.addWeighted(out, 1.6, flou, -0.6, 0)


def tuiles(img, cols, rangees, recouvrement=0.25):
    H, W = img.shape[:2]
    tw = int(W / (cols - (cols - 1) * recouvrement))
    th = int(H / (rangees - (rangees - 1) * recouvrement))
    for r in range(rangees):
        for c in range(cols):
            x0 = min(int(c * tw * (1 - recouvrement)), W - tw)
            y0 = min(int(r * th * (1 - recouvrement)), H - th)
            yield r, c, (x0, y0, tw, th), img[y0:y0 + th, x0:x0 + tw]


def main(src, dst):
    os.makedirs(f"{dst}/redresse", exist_ok=True)
    os.makedirs(f"{dst}/tuiles", exist_ok=True)
    index = {}
    for p, cfg in PHOTOS.items():
        img = cv2.imread(f"{src}/{p}.jpg")
        quad = None
        if cfg["redresser"]:
            img, quad = redresser(img)
        if cfg["rot"] is not None:
            img = cv2.rotate(img, cfg["rot"])
        img = contraste(img)
        cv2.imwrite(f"{dst}/redresse/{p}.jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 92])
        index[p] = {"redresse": f"redresse/{p}.jpg", "taille": img.shape[1::-1], "quad_source": quad, "tuiles": []}
        cols, rangees = cfg["grille"]
        for r, c, box, t in tuiles(img, cols, rangees):
            t = cv2.resize(t, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            nom = f"tuiles/{p}_r{r}c{c}.jpg"
            cv2.imwrite(f"{dst}/{nom}", t, [cv2.IMWRITE_JPEG_QUALITY, 90])
            index[p]["tuiles"].append({"fichier": nom, "rangee": r, "colonne": c, "boite_xywh_dans_redresse": box})
    with open(f"{dst}/index_tuiles.json", "w") as f:
        json.dump(index, f, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
