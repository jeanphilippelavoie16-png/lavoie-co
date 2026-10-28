# -*- coding: utf-8 -*-
"""Phase 2a — réconciliation des cotes : lecture 1 (extraction/) × lecture 2 (lectures/).

Sorties :
  arbitrage/accords.json      cotes appariées en accord (id unifié cote-<NIV>-NNN)
  arbitrage/desaccords.json   désaccords (d-<NIV>-NN) + orphelines (o-<NIV>-NN), NON tranchés
  arbitrage/vignettes/<id>_<Pn>.png   vignettes ×4 contrastées (désaccords + orphelines significatives)
  arbitrage/appariement_log.json      trace : homographies, paires, items exclus (non dimensionnels)

Méthode :
  * Repère commun par feuille : SS → P1, RDC → P3, P2 → P2, P5 → P5 (pixels prep/redresse).
  * Recalage entre photos d'une même feuille (P1↔P7, P3↔P4↔P6) : homographie SIFT + RANSAC
    sur les images redressées, contrôlée sur les cotes appariées sans ambiguïté (résidus en log).
  * Étiquettes d'ouvertures RDC (portes LxH) et membrures RDC sans px chez la lecture 1 :
    px ESTIMÉ en projetant centre_xy / géométrie (pouces) dans P3 par l'homographie de calage
    de l'extracteur (4 coins ext.) → fenêtre d'appariement élargie, texte compatible exigé.
  * Appariement glouton par coût = distance px + pénalité (0 même valeur, 30 via alternative,
    80 valeurs différentes ; « différentes » admis seulement à < 45 px).
  * accord = même valeur, aucune alternative qui change la valeur, aucune lecture marquée « ? ».
"""
import json, math, os, re, copy
import cv2
import numpy as np

BASE = '/home/user/lavoie-co/releve/travail'
ARB = os.path.join(BASE, 'arbitrage')
VIG = os.path.join(ARB, 'vignettes')
os.makedirs(VIG, exist_ok=True)

def load(p):
    with open(os.path.join(BASE, p), encoding='utf-8') as f:
        return json.load(f)

E = {k: load(f'extraction/{k}.json') for k in ('SS', 'RDC', 'COMP')}
L = {k: load(f'lectures/{k}.json') for k in ('SS', 'RDC', 'COMP')}

# ----------------------------------------------------------------------------- images / recalage
IMG = {}
def img(p):
    if p not in IMG:
        IMG[p] = cv2.imread(os.path.join(BASE, 'prep/redresse', p + '.jpg'), cv2.IMREAD_GRAYSCALE)
    return IMG[p]

def sift_h(a, b):
    A, B = img(a), img(b)
    s = cv2.SIFT_create(8000)
    ka, da = s.detectAndCompute(A, None)
    kb, db = s.detectAndCompute(B, None)
    m = cv2.BFMatcher().knnMatch(da, db, k=2)
    g = [x for x, y in m if x.distance < 0.75 * y.distance]
    pa = np.float32([ka[x.queryIdx].pt for x in g]); pb = np.float32([kb[x.trainIdx].pt for x in g])
    H, mask = cv2.findHomography(pa, pb, cv2.RANSAC, 4.0)
    inl = mask.ravel() == 1
    r = cv2.perspectiveTransform(pa[inl][None], H)[0] - pb[inl]
    return H, {"appariements": len(g), "inliers": int(inl.sum()),
               "residu_median_px": round(float(np.median(np.linalg.norm(r, axis=1))), 2)}

HOMO = {}   # (a,b) -> H (a vers b)
LOG = {"homographies": {}, "controle_homographies": [], "paires": {}, "exclus": {}, "orphelines_mineures": {}}
for a, b in [('P1', 'P7'), ('P3', 'P4'), ('P3', 'P6'), ('P6', 'P4')]:
    H, info = sift_h(a, b)
    HOMO[(a, b)] = H; HOMO[(b, a)] = np.linalg.inv(H)
    LOG["homographies"][f"{a}->{b}"] = dict(info, H=np.round(H, 6).tolist())
HOMO[('P4', 'P6')] = np.linalg.inv(HOMO[('P6', 'P4')]); HOMO[('P6', 'P3')] = np.linalg.inv(HOMO[('P3', 'P6')])

def tr(pt, a, b):
    if pt is None: return None
    if a == b: return [float(pt[0]), float(pt[1])]
    H = HOMO[(a, b)]
    q = cv2.perspectiveTransform(np.float32([[pt]]), H)[0][0]
    return [float(q[0]), float(q[1])]

def local_scale(a, b, pt):
    """facteur d'échelle local a→b autour de pt"""
    if a == b: return 1.0
    p0 = tr(pt, a, b); p1 = tr([pt[0] + 50, pt[1]], a, b); p2 = tr([pt[0], pt[1] + 50], a, b)
    return math.sqrt(abs((p1[0] - p0[0]) * (p2[1] - p0[1]) - (p1[1] - p0[1]) * (p2[0] - p0[0]))) / 50

# homographie de calage RDC de l'extracteur : pouces -> px P3
cal = E['RDC']['calage_estime']
_src = np.float32([cal['points_po'][k] for k in ('arriere_gauche', 'arriere_droit', 'avant_gauche', 'avant_droit')])
_dst = np.float32([cal['points_px'][k] for k in ('arriere_gauche', 'arriere_droit', 'avant_gauche', 'avant_droit')])
H_PO_P3 = cv2.getPerspectiveTransform(_src, _dst)
def po2p3(x, y):
    q = cv2.perspectiveTransform(np.float32([[[x, y]]]), H_PO_P3)[0][0]
    return [round(float(q[0]), 1), round(float(q[1]), 1)]

FEUILLES = {
    'SS':  {'ref': 'P1', 'photos': ['P1', 'P7']},
    'RDC': {'ref': 'P3', 'photos': ['P3', 'P4', 'P6']},
    'P2':  {'ref': 'P2', 'photos': ['P2']},
    'P5':  {'ref': 'P5', 'photos': ['P5']},
}

# ----------------------------------------------------------------------------- parsing
def norm_txt(s):
    return (s or '').replace('’', "'").replace('”', '"').replace('“', '"').replace('″', '"').replace('′', "'")

def parse_dim(s):
    """texte -> pouces (float) ou None. Gère 38'-0", 10-9", 16 8", 13-1, 6'-10', 31' 8", 38', 10", 7.79', 57.23, 112,28'."""
    if s is None: return None
    t = norm_txt(s).upper().strip()
    t = re.sub(r'^(PORTE|ARCHE|@)\s*', '', t)
    t = re.sub(r'\s*(C/C|\?)\s*$', '', t).strip()
    t = t.replace('½', '.5').replace('¼', '.25')
    m = re.match(r"^(\d+)\s*'?\s*[- ]\s*(\d+(?:\.\d+)?)\s*[\"']?$", t)
    if m: return int(m.group(1)) * 12 + float(m.group(2))
    m = re.match(r"^(\d+[.,]\d+)\s*'?$", t)
    if m: return round(float(m.group(1).replace(',', '.')) * 12, 2)
    m = re.match(r"^(\d+)\s*'$", t)
    if m: return int(m.group(1)) * 12.0
    m = re.match(r'^(\d+(?:\.\d+)?)\s*"?$', t)
    if m: return float(m.group(1))
    m = re.match(r'^(\d+[.,]?\d*)\s*M$', t)
    if m: return round(float(m.group(1).replace(',', '.')) * 39.3701, 1)
    return None

def parse_lxh(s):
    t = norm_txt(s)
    m = re.search(r"(\d+'?\s*-\s*\d+\"?)\s*[xX×]\s*(\d+'?\s*-\s*\d+\"?)", t)
    if not m: return None
    a, b = parse_dim(m.group(1)), parse_dim(m.group(2))
    return (a, b) if a and b else None

MEMB_TYPES = [('LINTEAU', 'LINTEAU'), ('LIN.', 'LINTEAU'), ('POUTRE', 'POUTRE'), ('SOLIVES', 'SOLIVES'),
              ('COL.', 'COLONNE'), ('BARRE', 'BARRE')]
def memb_key(s):
    t = norm_txt(s)
    typ = None
    for k, v in MEMB_TYPES:
        if k in t.upper(): typ = v; break
    u = re.sub(r'["\']', '', t)
    u = re.sub(r'(?<=\d)\s*[xX×]\s*(?=\d)', 'x', u)
    toks = re.findall(r'[\d½¼]+(?:-[\d½¼]+)*(?:x[\d½¼]+(?:-[\d½¼]+)*)*|@', u)
    return f"{typ}:{''.join(toks)}" if typ else None

def kind_of(text):
    t = norm_txt(text).upper()
    if 'ECHELLE' in t or 'ÉCHELLE' in t: return 'echelle'
    if 'C.M.' in t: return 'compte'
    if re.search(r'\d\s*/\s*12', t) and "'" not in t: return 'pente'
    if memb_key(text): return 'membrure'
    if parse_lxh(text): return 'lxh'
    return 'dim'

def cmp_value(kind, text, valeur=None, hauteur=None, unite=None):
    """valeur comparable selon le genre"""
    if kind == 'echelle': return re.sub(r'[^0-9/=\'"]', '', norm_txt(text).split(':')[-1])
    if kind == 'compte':
        m = re.search(r'(\d+)\s*C\.M', norm_txt(text).upper()); return int(m.group(1)) if m else None
    if kind == 'pente':
        m = re.search(r'(\d+)\s*/\s*(\d+)', text); return f"{m.group(1)}/{m.group(2)}" if m else None
    if kind == 'membrure': return memb_key(text)
    if kind == 'lxh':
        if valeur is not None and hauteur is not None: return (float(valeur), float(hauteur))
        return parse_lxh(text)
    # dim
    if valeur is not None and isinstance(valeur, (int, float)):
        v = float(valeur)
        if unite in ('pi', 'pi décimaux'): v = round(v * 12, 2)
        elif unite == 'm': v = round(v * 39.3701, 1)
        return v
    return parse_dim(text)

def fmt(v):
    if v is None: return None
    if isinstance(v, tuple): return [fmt(v[0]), fmt(v[1])]
    if isinstance(v, (int, float)):
        return int(v) if float(v).is_integer() else round(v, 2)
    return v

# ----------------------------------------------------------------------------- items lecture 1
def item(**k):
    base = dict(src=None, id=None, texte=None, kind=None, val=None, alts=[], photo=None, px=None,
                px_estime=False, emplacement=None, mesure=None, note=None, incertain=False, orient=None,
                refs=[], conf=None, n=None)
    base.update(k); return base

def l1_alts(c, kind):
    out = []
    for a in c.get('alternatives') or []:
        if isinstance(a, dict):
            txt = a.get('texte'); v = a.get('valeur'); raison = a.get('raison')
        else:
            txt = a; v = None; raison = None
        if kind == 'lxh':
            v2 = parse_lxh(txt) if txt else None
            if v2 is None and v is not None: v2 = None
            v = v2
        elif kind == 'membrure':
            v = memb_key(txt) if txt else None
        else:
            if v is None:
                pdim = parse_dim(re.sub(r'\s*\(.*\)$', '', txt or ''))
                v = pdim
            v = float(v) if isinstance(v, (int, float)) else v
        out.append({'texte': txt, 'valeur': v, 'raison': raison})
    return out

def build_l1(niv):
    items = []
    if niv in ('SS', 'RDC'):
        d = E[niv]; ref = FEUILLES[niv]['ref']
        cotes = d['cotes']
        for c in cotes:
            k = kind_of(c['texte_original'])
            it = item(src='cote', id=c['id'], texte=c['texte_original'], kind=k,
                      val=cmp_value(k, c['texte_original'], c.get('valeur')),
                      photo=c['photo'], px=c.get('px'), emplacement=c.get('emplacement'), mesure=c.get('mesure'),
                      note=c.get('note'), refs=[c['id']])
            it['alts'] = l1_alts(c, k)
            items.append(it)
        # ouvertures sans ref (étiquettes LxH) — RDC
        for o in d['ouvertures']:
            if (o.get('largeur') or {}).get('ref'): continue
            t = o.get('texte_original') or ''
            if not parse_lxh(t): continue
            px = po2p3(*o['centre_xy']) if niv == 'RDC' and o.get('centre_xy') else None
            alts = []
            n = (o['largeur'] or {}).get('note') or ''
            m = re.search(r"alt\.\s*(\d+'-\d+\")", n)
            if m:
                h = o['hauteur']['valeur']
                alts.append({'texte': f"{m.group(1)}x{t.split('x')[1]}", 'valeur': (parse_dim(m.group(1)), float(h)),
                             'raison': n})
            items.append(item(src='ouverture', id=None, texte=t, kind='lxh',
                              val=(float(o['largeur']['valeur']), float(o['hauteur']['valeur'])),
                              alts=alts, photo=ref, px=px, px_estime=True,
                              emplacement=o.get('note'), mesure=f"largeur x hauteur de {o['id']} ({o['type']})",
                              refs=[o['id']]))
        # membrures (structure)
        notes_px = {}
        for nt in d.get('notes', []):
            if nt.get('px'): notes_px[nt['texte_original']] = nt['px']
        seen = {}
        for s in d['structure']:
            dim = s.get('dimension') or {}
            t = dim.get('texte_original') or ''
            if not memb_key(t): continue
            key = memb_key(t)
            # colonnes : une seule étiquette pour toutes
            if s['type'] == 'colonne':
                if key in seen: seen[key]['refs'].append(s['id']); continue
            px = None; est = False
            if niv == 'SS':
                for nt, p in notes_px.items():
                    if t.split(' ')[0] in nt and memb_key(nt) and memb_key(nt).split(':')[1].startswith(key.split(':')[1]):
                        if not any(i['px'] == p for i in items if i['src'] == 'structure'):
                            px = p; break
            else:
                g = s.get('geometrie') or {}
                if 'x1' in g:
                    px = po2p3((g['x1'] + g['x2']) / 2, (g['y1'] + g['y2']) / 2); est = True
                elif 'zone' in g:
                    (x0, y0), (x1, y1) = g['zone']; px = po2p3((x0 + x1) / 2, (y0 + y1) / 2); est = True
            it = item(src='structure', texte=t, kind='membrure', val=key, photo=ref, px=px, px_estime=est,
                      emplacement=s.get('note'), mesure=f"membrure {s['id']} ({s['type']})", refs=[s['id']])
            # fusion avec une cote lecture 1 qui porte la même info (ex. « @ 20" c/c »)
            merged = False
            for c in items:
                if c['src'] == 'cote' and c['texte'] and c['texte'].strip() and c['texte'] in t and c['px'] and px \
                        and math.dist(c['px'], px) < 80:
                    c.update(kind='membrure', val=key, texte=t, mesure=c['mesure'] + f" — étiquette {s['id']}")
                    c['refs'].append(s['id'])
                    c['alts'] = [{'texte': t.replace(c['texte'].strip(), a['texte']), 'valeur': memb_key(t.replace(c['texte'].strip(), a['texte'])),
                                  'raison': a['raison']} for a in c['alts']]
                    merged = True
            if merged: continue
            seen[key] = it; items.append(it)
        # notes dimensionnelles (escalier C.M., échelle, armature)
        for nt in d.get('notes', []):
            t = nt['texte_original']
            if not re.search(r'C\.M\.|ECHELLE|ÉCHELLE|BARRE', t): continue
            k = kind_of(t)
            items.append(item(src='note', id=None, texte=t, kind=k, val=cmp_value(k, t),
                              photo=nt.get('photo') or ref, px=nt.get('px'), emplacement=nt.get('interpretation'),
                              mesure=nt.get('interpretation') or 'note', refs=[nt['id']]))
    else:  # P2 / P5 (COMP)
        d = E['COMP'][niv]
        for c in d['cotes']:
            t = c['texte_original']
            k = kind_of(t)
            v = c.get('valeur')
            incertain = '?' in t or c.get('statut') == 'illisible'
            if k == 'dim' and v is None: v = parse_dim(t)
            it = item(src='cote', id=c['id'], texte=t, kind=k, val=cmp_value(k, t, v), photo=c['photo'], px=c.get('px'),
                      emplacement=c.get('emplacement'), mesure=c.get('mesure'), note=c.get('note'),
                      incertain=incertain, refs=[c['id']])
            it['alts'] = l1_alts(c, k)
            items.append(it)
        for a in d.get('annotations', []):
            t = a['texte_original']
            if re.search(r'\d+[,.]\d+\s*m\b', t):
                m = re.search(r'(\d+[,.]\d+)\s*m\b', t)
                items.append(item(src='annotation', texte=t, kind='dim', val=round(float(m.group(1).replace(',', '.')) * 39.3701, 1),
                                  photo=a.get('photo', niv), px=a.get('px'), emplacement=a.get('position'),
                                  mesure=a.get('interpretation'), refs=[f"{niv}.annotations"]))
    return items

# ----------------------------------------------------------------------------- items lecture 2
NON_DIM = re.compile(r"^(3W|E 14|#220|3)$|CROQUIS|RÉSIDENCE|SEPTEMBRE|NOV\.|AV\. PARENT|RETIRÉE|MARQUE PÂLE|^…SUR LE LOT|^1-48",
                     re.I)

def build_l2(niv):
    src = L['COMP'] if niv in ('P2', 'P5') else L[niv]
    items, excl = [], []
    for c in src['cotes']:
        if niv in ('P2', 'P5') and c['photo'] != niv: continue
        t = c['texte_original']
        has_dim = bool(re.search(r"\d\s*['\"]|\d+[.,]\d+|C\.M\.|\d\s*/\s*12|\d\s*-\s*\d", t))
        if NON_DIM.search(t.strip()) or (c['categorie'] in ('autre', 'annotation', 'lot') and not has_dim):
            excl.append({'n': c['n'], 'texte': t, 'categorie': c['categorie'], 'raison': 'non dimensionnel'})
            continue
        k = kind_of(t)
        if c.get('dimension_nominale') and k != 'membrure': k = 'membrure'
        if k == 'dim' and c['categorie'] == 'annotation' and c.get('unite') == 'ratio (pente)': k = 'pente'
        val = cmp_value(k, t, c.get('valeur'), c.get('hauteur'), c.get('unite'))
        alts = []
        for a in c.get('alternatives') or []:
            if isinstance(a, dict):
                at = a.get('texte')
                if k == 'lxh':
                    av = (float(a['valeur']), float(a.get('hauteur') or val[1])) if a.get('valeur') is not None else parse_lxh(at)
                elif k == 'membrure':
                    av = memb_key(at) or memb_key(t.split(' ')[0] + ' ' + at)
                else:
                    av = cmp_value(k, at, a.get('valeur'), unite=c.get('unite'))
            else:
                at = a
                if k == 'membrure':
                    av = memb_key(at) or memb_key(t.split(' ')[0] + ' ' + at)
                elif k == 'pente':
                    av = cmp_value(k, at)
                else:
                    av = parse_dim(at)
                    if av is not None and c.get('unite') in ('pi', 'pi décimaux') and not re.search(r"['\"]", at):
                        av = round(av * 12, 2)
            alts.append({'texte': at, 'valeur': av, 'raison': None})
        orient = c.get('orientation') or ''
        items.append(item(src='l2', n=c['n'], texte=t, kind=k, val=val, alts=alts, photo=c['photo'], px=c.get('px'),
                          emplacement=c.get('emplacement'), mesure=c.get('mesure'), note=c.get('note'),
                          incertain='?' in t, orient='verticale' if orient.startswith('verticale (texte lu') or orient == 'verticale' else 'horizontale',
                          conf=c.get('confiance'), lap=c.get('lecture_autre_photo')))
    return items, excl

# ----------------------------------------------------------------------------- appariement
def to_ref(it, niv):
    ref = FEUILLES[niv]['ref']
    if it['px'] is None: return None
    return tr(it['px'], it['photo'], ref)

def same(a, b):
    if a is None or b is None: return False
    if isinstance(a, tuple) and isinstance(b, tuple):
        return abs(a[0] - b[0]) < 0.6 and abs(a[1] - b[1]) < 0.6
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) < 0.6
    return a == b

def compat(i1, i2):
    if i1['kind'] != i2['kind']: return None
    if same(i1['val'], i2['val']): return 'meme'
    if any(same(i1['val'], a['valeur']) for a in i2['alts']) or any(same(i2['val'], a['valeur']) for a in i1['alts']):
        return 'alt'
    return 'diff'

def apparier(niv, l1, l2):
    for it in l1 + l2: it['pref'] = to_ref(it, niv)
    cand = []
    for a, i1 in enumerate(l1):
        for b, i2 in enumerate(l2):
            c = compat(i1, i2)
            if c is None: continue
            if i1['pref'] is not None and i2['pref'] is not None:
                d = math.dist(i1['pref'], i2['pref'])
                gate = 170 if (i1['px_estime'] or i2['px_estime']) else 90
                if c == 'diff' and (d > 45 or i1['px_estime']): continue
                if d > gate: continue
            else:
                if c == 'diff': continue
                d = 120  # appariement texte seul (px absent) : accepté si unique, plus tard
            cost = d + {'meme': 0, 'alt': 30, 'diff': 80}[c]
            cand.append((cost, a, b, c, d))
    cand.sort()
    u1, u2, pairs = set(), set(), []
    for cost, a, b, c, d in cand:
        if a in u1 or b in u2: continue
        if l1[a]['pref'] is None or l2[b]['pref'] is None:
            # texte seul : exiger l'unicité du texte compatible parmi les restants
            others = [bb for (_, aa, bb, cc, _) in cand if aa == a and bb not in u2]
            if len(set(others)) > 1: continue
        u1.add(a); u2.add(b); pairs.append((a, b, c, round(d, 1)))
    o1 = [i for i in range(len(l1)) if i not in u1]
    o2 = [i for i in range(len(l2)) if i not in u2]
    return pairs, o1, o2

# ----------------------------------------------------------------------------- chaînes (contrainte de bouclage)
def F(p, i=0): return p * 12 + i
CHAINES = {
    'SS': [
        ("chaîne arrière rang 2 (= hors-tout 38'-0\")", ['cote-SS-002', 'cote-SS-003', 'cote-SS-004'], 456, 0),
        ("chaîne avant rang 3 (= 38'-0\")", ['cote-SS-027', 'cote-SS-028', 'cote-SS-029', 'cote-SS-030'], 456, 0),
        ("chaîne gauche rang 2 (= 31'-8\")", ['cote-SS-012', 'cote-SS-013', 'cote-SS-014', 'cote-SS-015'], 380, 0),
        ("chaîne droite rang 2 (= 31'-8\")", ['cote-SS-021', 'cote-SS-022', 'cote-SS-023', 'cote-SS-024'], 380, 0),
        ("chaîne intérieure x murs+colonnes (= 38'-0\")", ['cote-SS-037', 'cote-SS-038', 'cote-SS-039', 'cote-SS-040', 'cote-SS-041',
                                                     'cote-SS-042', 'cote-SS-043', 'cote-SS-044', 'cote-SS-045'], 456, 0),
        ("chaîne intérieure y (= 31'-8\", + 10\" mur arrière non écrit sur cette chaîne, cf. P2 cote-P2-011)",
         ['cote-SS-046', 'cote-SS-047', 'cote-SS-048', 'cote-SS-034'], 380, 10),
    ],
    'RDC': [
        ("chaîne avant rang 2 (= 38'-0\")", ['cote-RDC-010', 'cote-RDC-011', 'cote-RDC-012', 'cote-RDC-013'], 456, 0),
        ("chaîne arrière rang 3 (P4/P6, = 38'-0\")", ['cote-RDC-016', 'cote-RDC-017', 'cote-RDC-018'], 456, 0),
        ("chaîne arrière rang 2 axes (= 38'-0\")", ['cote-RDC-019', 'cote-RDC-020', 'cote-RDC-021', 'cote-RDC-022', 'cote-RDC-023'], 456, 0),
        ("entrée arrière : 8'-2\"+8'-3\"+8'-0\"+[2'-9\"] comparé à 18'-3\"+9'-0\" (nu ext. droit du volume, 327 po)",
         ['cote-RDC-019', 'cote-RDC-020', 'cote-RDC-021', 'cote-RDC-027'], 327, 0),
        ("chaîne gauche rang 2 (= 31'-8\")", ['cote-RDC-002', 'cote-RDC-003'], 380, 0),
        ("chaîne droite rang 2 (= 31'-8\")", ['cote-RDC-006', 'cote-RDC-007'], 380, 0),
        ("chaîne intérieure x (y≈18', = 38'-0\")", ['cote-RDC-029', 'cote-RDC-030', 'cote-RDC-031', 'cote-RDC-032', 'cote-RDC-033', 'cote-RDC-034'], 456, 0),
        ("chaîne intérieure x avant (y≈7', = 38'-0\")", ['cote-RDC-038', 'cote-RDC-039', 'cote-RDC-040', 'cote-RDC-041'], 456, 0),
        ("chaîne intérieure y gauche (= 31'-8\")", ['cote-RDC-035', 'cote-RDC-036', 'cote-RDC-037'], 380, 0),
        ("chaîne intérieure y milieu (= 31'-8\")", ['cote-RDC-042', 'cote-RDC-043', 'cote-RDC-044'], 380, 0),
        ("chaîne intérieure y droite (= 31'-8\")", ['cote-RDC-045', 'cote-RDC-046'], 380, 0),
    ],
    'P2': [
        ("P2 chaîne du bas lignes 1→7 (= 38')", ['cote-P2-003', 'cote-P2-004', 'cote-P2-005', 'cote-P2-006', 'cote-P2-007',
                                               'cote-P2-008', 'cote-P2-009', 'cote-P2-010'], 456, 0),
        ("P2 chaîne de droite D→A (= 31'-8\" ; hors-tout lu à gauche cote-P2-002)", ['cote-P2-011', 'cote-P2-012', 'cote-P2-013',
                                                                                   'cote-P2-014', 'cote-P2-015'], 380, 0),
    ],
    'P5': [],
}
# corroborations / contraintes factuelles hors chaîne (citées des lectures ou d'autres feuilles ; non tranchées)
EXTRA = {
    'cote-SS-004': "même chaîne arrière sur la feuille RDC (cote-RDC-016/017/018 : 18'-3\" + 9'-0\" + 10'-?\")",
    'cote-SS-005': "aucune chaîne fermée ; lecture 2 : à l'échelle ≈ 13'-1\" jusqu'au trait de rappel du meneau",
    'cote-SS-006': "aucune chaîne fermée ; lecture 1 : longueur dessinée ≈ 73 po, semblable à la fenêtre avant cotée 6'-3\"",
    'cote-SS-010': "aucune chaîne ; point de départ de la cote non dessiné (lecture 1)",
    'cote-SS-016': "aucune chaîne ; lecture 2 : mesure ≈ 3'-1\"",
    'cote-SS-017': "aucune chaîne ; lecture 1 : longueur dessinée ≈ 37 po",
    'cote-SS-025': "aucune chaîne ; lecture 1 : longueur dessinée ≈ 72 po ; lecture 2 : ≈ 6'-1\"",
    'cote-SS-036': "aucune chaîne",
    'cote-SS-046': "P2 (2016) cote-P2-012 « 13' 10\" » pour le même segment (nu int. mur arrière → axe C)",
    'cote-SS-051': "aucune chaîne ; note de structure",
    'cote-RDC-014': "aucune chaîne ; lecture 1 : largeur dessinée ≈ 76 po",
    'cote-RDC-015': "aucune chaîne ; lecture 1 : largeur dessinée ≈ 106 po",
    'cote-RDC-018': "même chaîne au sous-sol (cote-SS-002/003/004 : 18'-3\" + 9'-0\" + 10'-9\")",
    'cote-RDC-026': "aucune chaîne ; lecture 1 : largeur dessinée ≈ 39 po",
    'cote-RDC-038': "P2 (2016) : ligne 2 = 10\" + 11' 4\" = 146 po (cote-P2-003 + cote-P2-004)",
    'cote-RDC-047': "aucune chaîne ; lecture 1 : épaisseur dessinée ≈ 5 po",
    'cote-RDC-048': "aucune chaîne ; lecture 1 : ouverture dessinée ≈ 74 po (≈ l'ARCHE 6'-0\" salon/cuisine ≈ 73 po)",
    'ouv-RDC-017': "baie de 2'-5\" (cote-RDC-031, 29 po) entre cloisons de la colonne des G.R. (lecture 1) ; autres portes intérieures étiquetées 6'-8\" de hauteur",
    'ouv-RDC-022': "aucune chaîne",
    'ouv-RDC-011': "baie entre cloisons x=175 et x=222 (largeur du hall 3'-11\", cote-RDC-040) selon lecture 1",
    'str-RDC-L05': "aucune chaîne ; les autres fenêtres 6'-3\" (ouv-RDC-001, ouv-RDC-003) portent « LINTEAU 2-2\"x8\" »",
    'cote-P2-002': "hors-tout aussi lu 31'-8\" sur SS, RDC et P5",
    'cote-P2-017': "cote pâle du plan d'origine ; segment correspondant sur P3 : cote-RDC-032 « 8'-4\" »",
    'cote-P2-018': "cote pâle du plan d'origine ; P3 cote-RDC-033 « 3'-5\" » et P2 cote-P2-008 « 3' 5\" »",
    'cote-P2-019': "cote pâle du plan d'origine ; P3 cote-RDC-034 « 11'-8\" »",
    'cote-P2-021': "note pâle du plan d'origine ; P3 : « POUTRE 6\"x10\" FLUSH » (str-RDC-P01)",
    'cote-P5-002': "hors-tout aussi lu 31'-8\" sur SS, RDC et P2",
    'cote-P5-003': "7.79' + 38'-0\" + 9' = 54,79 pi ; lecture 1 : largeur du lot mesurée dans l'image à 40 pi de la rue ≈ 54,3 pi (ESTIMÉ)",
    'cote-P5-008': "aucune chaîne",
    'cote-P5-010': "aucune chaîne",
    'cote-P5-011': "aucune chaîne",
}

def fmt_pp(v):
    if v is None: return '?'
    v = float(v); s = '-' if v < 0 else ''; v = abs(v)
    p = int(v // 12); i = v - 12 * p
    i = int(i) if float(i).is_integer() else round(i, 2)
    return f"{s}{p}'-{i}\""

def bouclage(niv, cid, candidats, valeurs_feuille):
    out = []
    for nom, ids, cible, cst in CHAINES.get(niv, []):
        if cid not in ids: continue
        autres = [valeurs_feuille.get(i) for i in ids if i != cid]
        if any(v is None or not isinstance(v, (int, float)) for v in autres):
            continue
        base = sum(autres) + cst
        parts = []
        for txt, v in candidats:
            if not isinstance(v, (int, float)): continue
            s = base + v
            parts.append(f"{txt} → somme {fmt(s)} po (écart {fmt(s - cible):+})")
        ferme = [txt for txt, v in candidats if isinstance(v, (int, float)) and abs(base + v - cible) < 0.6]
        out.append(f"{nom} : " + ' ; '.join(parts) + (f" ⇒ ferme avec {', '.join(dict.fromkeys(ferme))}" if ferme else " ⇒ aucune valeur ne ferme"))
    return out

# ----------------------------------------------------------------------------- vignettes
def vignette(vid, niv, pts_by_photo, orient, kind, label):
    """pts_by_photo : {photo: [px,...]} ; produit <vid>_<P>.png pour chaque photo où le point est dans l'image."""
    files = []
    ref = FEUILLES[niv]['ref']
    for ph in FEUILLES[niv]['photos']:
        pts = pts_by_photo.get(ph) or []
        if not pts: continue
        im = img(ph); Hh, Ww = im.shape
        cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
        if not (5 <= cx < Ww - 5 and 5 <= cy < Hh - 5): continue
        sc = local_scale(ref, ph, tr([cx, cy], ph, ref)) if ph != ref and (ref, ph) in HOMO else 1.0
        if kind in ('lxh', 'membrure', 'echelle'): hw, hh = 150, 50
        else: hw, hh = 95, 42
        if orient == 'verticale': hw, hh = hh + 5, hw
        hw *= sc; hh *= sc
        x0 = int(max(0, min(p[0] for p in pts) - hw)); x1 = int(min(Ww, max(p[0] for p in pts) + hw))
        y0 = int(max(0, min(p[1] for p in pts) - hh)); y1 = int(min(Hh, max(p[1] for p in pts) + hh))
        crop = im[y0:y1, x0:x1]
        if crop.size == 0: continue
        cl = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(4, 4)).apply(crop)
        cl = cv2.normalize(cl, None, 0, 255, cv2.NORM_MINMAX)
        big = cv2.resize(cl, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
        blur = cv2.GaussianBlur(big, (0, 0), 3)
        big = cv2.addWeighted(big, 1.5, blur, -0.5, 0)
        band = np.full((34, big.shape[1]), 255, np.uint8)
        cv2.putText(band, f"{vid}  {ph}  [{x0},{y0}]-[{x1},{y1}]  {label}"[:110], (6, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 0, 1, cv2.LINE_AA)
        out = np.vstack([band, big])
        fn = f"{vid}_{ph}.png"
        cv2.imwrite(os.path.join(VIG, fn), out)
        files.append({'fichier': f"arbitrage/vignettes/{fn}", 'photo': ph, 'boite_px': [x0, y0, x1, y1]})
    return files

def pts_photos(niv, items):
    """positions du texte dans chaque photo de la feuille (px réels prioritaires sur px estimés)"""
    ref = FEUILLES[niv]['ref']
    reels = [it for it in items if it and it['px'] is not None and not it['px_estime']]
    use = reels or [it for it in items if it and it['px'] is not None]
    out = {}
    for ph in FEUILLES[niv]['photos']:
        pts = []
        for it in use:
            if it['photo'] == ph: pts.append(list(it['px']))
            elif (it['photo'], ph) in HOMO: pts.append(tr(it['px'], it['photo'], ph))
        if pts: out[ph] = pts
    return out

# ----------------------------------------------------------------------------- principal
def lecture_dict(it, qui):
    if it is None: return None
    d = {'texte': it['texte'], 'valeur': fmt(it['val']), 'photo': it['photo'],
         'px': [round(p) for p in it['px']] if it['px'] else None}
    if it['px_estime']: d['px_note'] = "px ESTIMÉ (projection de la géométrie lecture 1 dans P3), pas la position du texte"
    if qui == 1: d['ref'] = it['refs']
    else:
        d['n'] = it['n']; d['confiance'] = it['conf']
        if it.get('lap'): d['lecture_autre_photo'] = it['lap']
    if it.get('note'): d['note'] = it['note']
    return d

accords, desaccords = [], []
stats = {}
for niv in ('SS', 'RDC', 'P2', 'P5'):
    l1 = build_l1(niv)
    l2, excl = build_l2(niv)
    LOG['exclus'][niv] = excl
    pairs, o1, o2 = apparier(niv, l1, l2)
    # ids unifiés
    if niv in ('SS', 'RDC'):
        nmax = max(int(c['id'].split('-')[-1]) for c in E[niv]['cotes'])
    else:
        nmax = max(int(c['id'].split('-')[-1]) for c in E['COMP'][niv]['cotes'])
    def new_id():
        global nmax
        nmax += 1
        return f"cote-{niv}-{nmax:03d}"
    groups = []
    for a, b, c, d in pairs: groups.append((l1[a], l2[b], c, d))
    for a in o1: groups.append((l1[a], None, None, None))
    for b in o2: groups.append((None, l2[b], None, None))
    groups.sort(key=lambda g: (int(g[0]['id'].split('-')[-1]) if g[0] and g[0]['id'] else 999,
                               g[1]['n'] if g[1] else 0))
    for g in groups:
        i1 = g[0]
        if i1 and not i1['id']: i1['id'] = new_id()
        if not i1 and g[1]: g[1]['uid'] = new_id()
    # valeurs de la feuille pour les chaînes (lecture 1 sinon lecture 2)
    vals = {}
    for i1, i2, c, d in groups:
        uid = i1['id'] if i1 else i2['uid']
        v = (i1 or i2)['val']
        vals[uid] = v
    nd = no = na = 0; nomin = 0
    LOG['paires'][niv] = []
    for i1, i2, c, d in groups:
        uid = i1['id'] if i1 else i2['uid']
        main = i1 or i2
        LOG['paires'][niv].append({'id': uid, 'l1': i1['refs'] if i1 else None, 'l2_n': i2['n'] if i2 else None,
                                   'texte_1': i1['texte'] if i1 else None, 'texte_2': i2['texte'] if i2 else None,
                                   'compat': c, 'distance_px_ref': d})
        alts = []
        for it, qui in ((i1, 'lecture_1'), (i2, 'lecture_2')):
            if not it: continue
            for a in it['alts']:
                if a['valeur'] is not None and not same(a['valeur'], it['val']):
                    alts.append({'texte': a['texte'], 'valeur': fmt(a['valeur']), 'propose_par': qui, 'raison': a['raison']})
        if i1 and i2:
            nature = []
            if not same(i1['val'], i2['val']): nature.append('valeurs_differentes')
            if alts: nature.append('alternative_signalee')
            if i1['incertain'] or i2['incertain']: nature.append('lecture_marquee_incertaine')
            if not nature:
                ph = i1['photo'] if not i1['px_estime'] else i2['photo']
                px = i1['px'] if not i1['px_estime'] else i2['px']
                accords.append({'id': uid, 'feuille': niv, 'texte_original': i1['texte'], 'valeur': fmt(i1['val']),
                                'lecture_1': i1['texte'], 'lecture_2': i2['texte'], 'photo': ph,
                                'px': [round(p) for p in px] if px else None,
                                'emplacement': i1['emplacement'], 'mesure': i1['mesure'],
                                'ref_lecture_1': i1['refs'], 'n_lecture_2': i2['n'],
                                'mesure_lecture_2': i2['mesure'], 'distance_px': d})
                na += 1
                continue
            nd += 1
            did = f"d-{niv}-{nd:02d}"; cat = 'desaccord'
        else:
            no += 1
            did = f"o-{niv}-{no:02d}"; cat = 'orpheline'; nature = ['vue_par_lecture_1_seulement' if i1 else 'vue_par_lecture_2_seulement']
        # contrainte de bouclage
        cands = []
        for it in (i1, i2):
            if it: cands.append((it['texte'], it['val']))
        for a in alts: cands.append((a['texte'], a['valeur']))
        cands = [(t, (v if not isinstance(v, list) else tuple(v))) for t, v in cands]
        cid = uid
        bl = bouclage(niv, cid, cands, vals)
        extra = [EXTRA[r] for r in ((i1['refs'] if i1 else []) + [uid]) if r in EXTRA]
        contrainte = ' | '.join(dict.fromkeys(bl + extra)) or "aucune chaîne fermée ne contient cette cote"
        significative = main['kind'] in ('dim', 'lxh', 'membrure', 'compte', 'pente') and main['px'] is not None
        vign = []
        if cat == 'desaccord' or significative:
            orient = (i2 or {}).get('orient') or ('verticale' if 'vertical' in (main['emplacement'] or '') else 'horizontale')
            if i2 is None and i1 is not None and not i1['px_estime'] and i1['photo'] in ('P2', 'P5'):
                orient = 'verticale' if 'verticale' in (i1['emplacement'] or '') else 'horizontale'
            vign = vignette(did, niv, pts_photos(niv, [i1, i2]), orient, main['kind'],
                            f"{(i1 or {}).get('texte') or ''} | {(i2 or {}).get('texte') or ''}")
        entry = {'id': did, 'categorie': cat, 'nature': nature, 'feuille': niv, 'cote_id': uid,
                 'vignettes': [v['fichier'] for v in vign], 'vignettes_boites': vign,
                 'emplacement': main['emplacement'] if i1 else i2['emplacement'],
                 'emplacement_lecture_2': i2['emplacement'] if (i1 and i2) else None,
                 'mesure': main['mesure'], 'mesure_lecture_2': i2['mesure'] if (i1 and i2) else None,
                 'lecture_1': lecture_dict(i1, 1), 'lecture_2': lecture_dict(i2, 2),
                 'alternatives': alts, 'contrainte_de_bouclage': contrainte,
                 'distance_px_entre_lectures': d}
        if cat == 'orpheline':
            entry['significative'] = significative
            if not significative:
                entry['raison_non_significative'] = 'pas de px (texte générique)' if main['px'] is None else 'non dimensionnel'
        desaccords.append(entry)
    stats[niv] = {'accords': na, 'desaccords': nd, 'orphelines': no,
                  'l1_items': len(l1), 'l2_items': len(l2), 'l2_exclus_non_dimensionnels': len(excl)}

# contrôle des homographies sur les paires appariées situées dans des photos différentes
for niv in ('SS', 'RDC'):
    pass

with open(os.path.join(ARB, 'accords.json'), 'w', encoding='utf-8') as f:
    json.dump(accords, f, ensure_ascii=False, indent=1)
with open(os.path.join(ARB, 'desaccords.json'), 'w', encoding='utf-8') as f:
    json.dump(desaccords, f, ensure_ascii=False, indent=1)
LOG['stats'] = stats
with open(os.path.join(ARB, 'appariement_log.json'), 'w', encoding='utf-8') as f:
    json.dump(LOG, f, ensure_ascii=False, indent=1)
print(json.dumps(stats, ensure_ascii=False, indent=1))
for d in desaccords:
    print(d['id'], d['cote_id'], d['nature'], '|', (d['lecture_1'] or {}).get('texte'), '|', (d['lecture_2'] or {}).get('texte'),
          '|', [a['texte'] for a in d['alternatives']], '|', len(d['vignettes']), 'vign', '|', d['distance_px_entre_lectures'])
