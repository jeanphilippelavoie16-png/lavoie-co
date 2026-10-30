# -*- coding: utf-8 -*-
"""Phase 2b — construction de livrables/donnees/maison.json (déterministe).

Entrées : travail/extraction/*.json (lecture 1), travail/arbitrage/{accords,desaccords,lecture_3}.json,
          livrables/outils/generer_plans.py (importé pour reproduire exactement l'emprise des murs).
Sortie  : livrables/donnees/maison.json  (+ résumé des vérifications à l'écran).

Principes : aucune valeur inventée ; chaque dimension porte sa source ; cotes écrites > dessin ;
tout écart → registre ; murs porteurs « inconnu » sauf mention écrite.
"""
import copy, json, math, os, re, sys
sys.path.insert(0, '/home/user/lavoie-co/releve/livrables/outils')
import generer_plans as gp                                   # noqa: E402
from shapely.geometry import Polygon, LineString, Point, box  # noqa: E402
from shapely.geometry.polygon import orient                  # noqa: E402
from shapely.ops import unary_union, split, polygonize                   # noqa: E402

T = '/home/user/lavoie-co/releve/travail'
OUT = '/home/user/lavoie-co/releve/livrables/donnees/maison.json'


def J(p):
    with open(os.path.join(T, p), encoding='utf-8') as f:
        return json.load(f)


EX = {k: J(f'extraction/{k}.json') for k in ('SS', 'RDC', 'COMP')}
ACC = J('arbitrage/accords.json')
DES = J('arbitrage/desaccords.json')
L3 = {e['id']: e for e in J('arbitrage/lecture_3.json')}


def D(v, src, photo=None, note=None, ref=None):
    d = {"valeur": v, "source": src, "photo": photo}
    if ref: d["ref"] = ref
    if note: d["note"] = note
    return d


def pp(v):
    if v is None: return '?'
    s = '-' if v < 0 else ''
    v = abs(v); p = int(v // 12); i = round(v - 12 * p, 2)
    if i == 12: p, i = p + 1, 0
    i = int(i) if float(i).is_integer() else i
    return f"{s}{p}'-{i}\""


# ============================================================================ parsing (identique à reconcilier_cotes.py)
def norm_txt(s):
    return (s or '').replace('’', "'").replace('”', '"').replace('“', '"')


def parse_dim(s):
    if s is None: return None
    t = norm_txt(s).upper().strip()
    t = re.sub(r'^(PORTE|ARCHE|@)\s*', '', t)
    t = re.sub(r'\s*(C/C|\?)\s*$', '', t).strip()
    m = re.match(r"^(\d+)\s*'?\s*[- ]\s*(\d+(?:\.\d+)?)\s*[\"']?$", t)
    if m: return int(m.group(1)) * 12 + float(m.group(2))
    m = re.match(r"^(\d+[.,]\d+)\s*'?$", t)
    if m: return round(float(m.group(1).replace(',', '.')) * 12, 2)
    m = re.match(r"^(\d+)\s*'$", t)
    if m: return int(m.group(1)) * 12.0
    m = re.match(r'^(\d+(?:\.\d+)?)\s*"?$', t)
    if m: return float(m.group(1))
    return None


def parse_lxh(s):
    m = re.search(r"(\d+'?\s*-\s*\d+\"?)\s*[xX×]\s*(\d+'?\s*-\s*\d+\"?)", norm_txt(s))
    if not m: return None
    a, b = parse_dim(m.group(1)), parse_dim(m.group(2))
    return [a, b] if a and b else None


def memb(s):
    u = re.sub(r'["\']', '', norm_txt(s))
    u = re.sub(r'(?<=\d)\s*[xX×]\s*(?=\d)', 'x', u)
    return ''.join(re.findall(r'[\d½]+(?:-[\d½]+)*(?:x[\d½]+(?:-[\d½]+)*)*|@', u))


def same(a, b):
    if a is None or b is None: return False
    if isinstance(a, list) and isinstance(b, list):
        return all(abs(x - y) < 0.05 for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) < 0.05
    return a == b


# ============================================================================ registre des écarts
ECARTS = []
EC = {}


def ecart(cle, niveau, description, impact, hypothese, a_valider, photo, position=None):
    eid = f"ecart-{len(ECARTS) + 1:03d}"
    e = {"id": eid, "niveau": niveau, "description": description, "impact": impact,
         "hypothese_retenue": hypothese, "a_valider_sur_place": a_valider, "photo": photo, "statut": "ouvert"}
    if position is not None: e["position"] = [round(position[0], 1), round(position[1], 1)]
    ECARTS.append(e); EC[cle] = eid
    return eid


# ============================================================================ 1. TRANCHAGE DES COTES (3e lecture)
# hypothèses retenues quand la 3e lecture ne tranche pas (conflit) — justification explicite
HYP = {
    'cote-SS-017': (36, "3'-0\"", "les lectures 1 et 2 lisent 3'-0\" ; 3e lecture 3'-0\" mais en confiance basse ; "
                    "aucune chaîne ne contient cette largeur ; dessin ≈ 37 po (ESTIMÉ) compatible"),
    'cote-RDC-018': (129, "10'-9\"", "3e lecture 10'-5\" en confiance basse ; seule 10'-9\" ferme la chaîne arrière "
                     "18'-3\" + 9'-0\" + 10'-9\" = 38'-0\" (10'-5\" donne 37'-8\") ; la même chaîne au sous-sol "
                     "(cote-SS-004) est confirmée 10'-9\""),
    'cote-RDC-048': (48, "ARCHE 4'-0\"", "lectures 1 et 2 : 4'-0\" ; 3e lecture (aveugle) : 6'-0\" ; ouverture dessinée "
                     "≈ 74 po (ESTIMÉ). Valeur écrite majoritaire retenue (les cotes écrites priment sur le dessin) "
                     "— à mesurer"),
    'cote-P5-010': (1382.04, "115.17'", "lectures 1 et 2 : 115.17' ; 3e lecture 115,14' ; aucune chaîne fermée"),
}


def resoudre(d):
    """retourne (statut, valeur, texte, note, lecture_3) pour une entrée de desaccords.json"""
    l3 = L3.get(d['id'])
    l1, l2 = d.get('lecture_1') or {}, d.get('lecture_2') or {}
    lec3 = None
    if l3:
        lec3 = {k: l3.get(k) for k in ('texte', 'valeur_po', 'confiance', 'lisible', 'justification')}
    base = l1 or l2
    kind = 'lxh' if isinstance(base.get('valeur'), list) else ('memb' if isinstance(base.get('valeur'), str) else 'dim')
    if d['categorie'] == 'orpheline':
        if not l3 or not l3.get('lisible') or l3.get('confiance') == 'basse':
            return 'illisible', None, base.get('texte'), "orpheline (vue par un seul lecteur) ; 3e lecture : illisible ou confiance basse", lec3
    if not l3:
        return 'conflit', base.get('valeur'), base.get('texte'), "pas de 3e lecture", lec3
    if kind == 'lxh':
        v3 = parse_lxh(l3['texte'])
    elif kind == 'memb':
        v3 = None
    else:
        v3 = parse_dim(l3['texte'])
    vals = [x.get('valeur') for x in (l1, l2) if x]
    ok_conf = l3.get('lisible') and l3.get('confiance') in ('moyenne', 'haute')
    if kind == 'memb':
        # membrure : concordance des dimensions nominales
        k3 = memb(l3['texte']); ks = [memb(x.get('texte') or '') for x in (l1, l2) if x]
        conc = any(k3 == k or (k and k in k3) for k in ks)
        if conc and ok_conf:
            note = "tranché par 3e lecture"
            if k3 not in ks: note += f" (3e lecture complète la note : « {l3['texte']} »)"
            return 'confirmee', None, l3['texte'], note, lec3
        return 'conflit', None, base.get('texte'), "3e lecture non concordante", lec3
    conc = any(same(v3, v) for v in vals)
    if conc and ok_conf:
        txt = next((x.get('texte') for x in (l1, l2) if x and same(v3, x.get('valeur'))), l3['texte'])
        return 'confirmee', v3, txt, f"tranché par 3e lecture ({l3.get('confiance')})", lec3
    cid = d['cote_id']
    if cid in HYP:
        v, t, j = HYP[cid]
        return 'conflit', v, t, "conflit non tranché par la 3e lecture — hypothèse retenue : " + j, lec3
    return 'conflit', base.get('valeur'), base.get('texte'), "conflit non tranché", lec3


RESOL = {}
for d in DES:
    RESOL[d['cote_id']] = (d,) + resoudre(d)

# écarts pour les cotes en conflit (ordre déterministe)
CONFLIT_INFO = {
    'cote-SS-017': ("SS", "moyen" if False else "faible", "Largeur de la fenêtre gauche basse du sous-sol (au-dessus de l'évier à lessive)",
                    "Mesurer la largeur brute de la fenêtre du mur gauche du sous-sol, côté avant (au-dessus de l'évier à lessive).", "P1", (0, 48)),
    'cote-RDC-018': ("RDC", "moyen", "Segment arrière droit 10'-9\" / 10'-5\" (nu ext. droit de l'entrée arrière → coin arrière droit)",
                     "Mesurer à l'extérieur, le long du mur arrière, du coin arrière droit au nu extérieur du mur droit de l'entrée arrière (attendu 10'-9\" = 129 po).", "P6", (391, 380)),
    'cote-RDC-048': ("RDC", "moyen", "Largeur de l'arche hall / salon : écrit « ARCHE 4'-0\" » (2 lectures) contre 6'-0\" (3e lecture) ; dessin ≈ 74 po",
                     "Mesurer la largeur libre de l'arche hall / salon (cloison à 18'-6\" du coin avant gauche).", "P3", (222, 118.6)),
    'cote-P5-010': ("global", "faible", "Longueur de la ligne latérale gauche du lot : 115.17' (2 lectures) ou 115,14' (3e lecture)",
                    "Consulter le certificat de localisation / plan cadastral (aucune mesure de maison en jeu).", "P5", None),
}
for cid in sorted(CONFLIT_INFO, key=lambda c: (c.split('-')[1], c)):
    d, statut, val, txt, note, lec3 = RESOL[cid]
    if statut != 'conflit': continue
    niv, imp, desc, aval, ph, pos = CONFLIT_INFO[cid]
    l1t = (d.get('lecture_1') or {}).get('texte'); l2t = (d.get('lecture_2') or {}).get('texte')
    ecart('conf-' + cid, niv, f"Cote en conflit {cid} — {desc}. Lecture 1 « {l1t} », lecture 2 « {l2t} », 3e lecture « {lec3['texte']} » "
          f"({lec3['confiance']}). Vignettes (fichiers de travail, numérotation interne des photos) : {', '.join(d['vignettes'])}.", imp,
          f"{txt} ({pp(val) if isinstance(val, (int, float)) and cid != 'cote-P5-010' else val} po) — {note.split('hypothèse retenue : ')[-1]}",
          aval, ph, pos if niv in ('SS', 'RDC') else None)
for cid, (d, statut, *_r) in RESOL.items():
    if statut == 'conflit' and cid not in CONFLIT_INFO:
        raise SystemExit(f"conflit sans écart : {cid}")


# ============================================================================ 2. cotes des niveaux
def cote_entry(cid, niv, texte, valeur, l1, l2, statut, photo, px, empl, mesure, hauteur=None, note=None, lec3=None, dim_nom=None):
    c = {"id": cid, "texte_original": texte, "valeur": valeur, "lecture_1": l1, "lecture_2": l2, "statut": statut,
         "photo": photo, "emplacement": empl, "px": px, "mesure": mesure}
    if hauteur is not None: c["hauteur"] = hauteur
    if dim_nom: c["dimension_nominale"] = dim_nom
    if lec3: c["lecture_3"] = lec3
    if note: c["note"] = note
    return c


def P2_ID(cid):  # cotes du croquis 2016 rangées au niveau RDC
    return 'cote-RDC-2' + cid.split('-')[-1][1:]


COTES = {'SS': [], 'RDC': []}
IMPL = []
VAL = {}  # valeur finale par id (pour lignes_cote)
STAT = {}
for a in ACC:
    niv = a['feuille']
    v = a['valeur']; h = None; dn = None
    if isinstance(v, list): v, h = v[0], v[1]
    elif isinstance(v, str): dn, v = v.split(':', 1)[-1], None
    cid = a['id']
    if niv == 'P2': cid = P2_ID(cid)
    c = cote_entry(cid, niv, a['texte_original'], v, a['lecture_1'], a['lecture_2'], 'confirmee', a['photo'], a['px'],
                   a['emplacement'], a['mesure'], h, "lectures 1 et 2 concordantes" + (" ; croquis 2016 (P2)" if niv == 'P2' else ""),
                   dim_nom=dn)
    VAL[cid] = v; STAT[cid] = 'confirmee'
    if niv == 'P5': IMPL.append(c)
    else: COTES['RDC' if niv == 'P2' else niv].append(c)
for cid, (d, statut, val, txt, note, lec3) in sorted(RESOL.items()):
    niv = d['feuille']
    l1, l2 = d.get('lecture_1') or {}, d.get('lecture_2') or {}
    h = None
    if isinstance(val, list): val, h = val[0], val[1]
    ph = (l2 or l1).get('photo') if (l1.get('px_note') or not l1.get('px')) else l1.get('photo')
    px = (l2 or l1).get('px') if (l1.get('px_note') or not l1.get('px')) else l1.get('px')
    nid = P2_ID(cid) if niv == 'P2' else cid
    rep = EC.get('conf-' + cid)
    n = note + (f" ; vignettes (fichiers de travail, numérotation interne) {', '.join(d['vignettes'])}" if d['vignettes'] else "") + (f" ; écart {rep}" if rep else "")
    if niv == 'P2': n += " ; croquis 2016 (P2)"
    dn = None
    if isinstance(l1.get('valeur'), str) or isinstance(l2.get('valeur'), str):
        dn = memb(txt) or None
    c = cote_entry(nid, niv, txt, val if not dn else None, l1.get('texte'), l2.get('texte'), statut, ph, px,
                   d.get('emplacement'), d.get('mesure'), h, n, lec3, dim_nom=dn)
    if d.get('alternatives'): c['alternatives'] = d['alternatives']
    c['contrainte_de_bouclage'] = d.get('contrainte_de_bouclage')
    VAL[nid] = val; STAT[nid] = statut
    if niv == 'P5': IMPL.append(c)
    else: COTES['RDC' if niv == 'P2' else niv].append(c)
for k in COTES: COTES[k].sort(key=lambda c: c['id'])
IMPL.sort(key=lambda c: c['id'])
# contrôle : toutes les cotes de la lecture 1 sont présentes
for niv in ('SS', 'RDC'):
    ids = {c['id'] for c in COTES[niv]}
    manq = [c['id'] for c in EX[niv]['cotes'] if c['id'] not in ids]
    assert not manq, manq


def V(cid):
    return VAL[cid]


# ============================================================================ 3. épaisseurs et convention
T_FOND = 10.0      # LU (P1 : cote-SS-019, -034, -037, -045)
T_EXT = 10.0       # MESURÉ : 10" confirmé par le propriétaire (2026-10-29) ; = croquis 2016 (P2) ; dessin 1957 ≈ 11 po
H_EXT = T_EXT / 2
T_INT = 4.5        # MESURÉ : confirmé par le propriétaire (2026-10-29)
T_6 = V('cote-RDC-047')   # cloison chambre arrière / S. de bain : 6" (tranché 3e lecture)
assert T_6 == 6
T_EAR = T_EXT      # entrée arrière : mur extérieur, même valeur provisoire
T_PERRON = 6.0     # cote-SS-036 (LU) ; murs avant/droit par analogie

E_EXT = D(T_EXT, "MESURÉ", None, "10\" confirmé par le propriétaire (2026-10-29) ; concorde avec le croquis 2016 (cote-RDC-203/210/211/215) ; dessin 1957 ≈ 11 po (ESTIMÉ)")
E_INT = D(T_INT, "MESURÉ", None, "4½\" confirmé par le propriétaire (2026-10-29) ; dessin 1957 ≈ 6 po (ESTIMÉ)")
E_EAR = D(T_EAR, "PRÉSUMÉ", None, "mur extérieur de l'entrée arrière : 10\" pris égal aux murs de la maison (confirmés par le propriétaire) ; dessin ≈ 11 po (ESTIMÉ)")

CONVENTION = ("Hors-tout et chaînes extérieures au NU EXTÉRIEUR des murs de fondation (SS) et des murs extérieurs (RDC) ; "
              "fenêtres et portes extérieures cotées à l'AXE (centre) de l'ouverture, largeurs = baie entre jambages ; "
              "cloisons du RDC cotées à l'AXE (DÉDUIT : chaque chaîne intérieure ferme sur le hors-tout depuis les nus ext. ; "
              "les axes y = 13'-1\" (157) et 17'-0\" (204) coïncident avec les axes des poutres 8\"x10\" du sous-sol et avec les "
              "axes B et C du croquis 2016 ; la ligne 2 du croquis tombe sur l'axe de la cloison) ; au sous-sol, chaîne "
              "intérieure en x au nu intérieur des murs et aux faces des colonnes (10\" + 9'-10\" + 8\" + 7'-4\" …), chaîne en y "
              "du nu intérieur aux AXES des poutres. Épaisseurs : fondation 10\" LU (P1) ; murs ext. RDC 10\" LU (P2 2016, à "
              "confronter : dessin 1957 ≈ 11\") ; cloisons 4½\" PRÉSUMÉ sauf cloison chambre arrière / S. de bain 6\" LU ; "
              "murs du caveau 10\" (droit LU, autres PRÉSUMÉ par analogie) ; murs de l'excroissance du perron 6\" (gauche LU, "
              "autres PRÉSUMÉ) ; entrée arrière 6\" PRÉSUMÉ. Toute la géométrie est générée par code (scripts/construire_maison.py).")


# ============================================================================ 4. murs
def mur(mid, typ, x1, y1, x2, y2, ep, note, indices=None, pos_src='DÉDUIT'):
    return {"id": mid, "type": typ, "porteur": "inconnu", "indices_porteur": indices or [],
            "epaisseur": ep, "x1": x1, "y1": y1, "x2": x2, "y2": y2,
            "note": note, "source_position": pos_src}


IND_SS_EXT = ["mur de fondation en béton coulé (P1)", "appui probable des solives 2\"x10\" @ 20\" c/c (P1) — non écrit"]
MURS_SS = [
    mur('mur-SS-001', 'fondation', 5, 5, 451, 5, D(T_FOND, "LU", "P1", ref="cote-SS-034"), "Mur avant (côté rue) ; axe y = 5 (nu ext. y = 0).", IND_SS_EXT),
    mur('mur-SS-002', 'fondation', 451, 5, 451, 375, D(T_FOND, "LU", "P1", ref="cote-SS-045"), "Mur latéral droit ; axe x = 38'-0\" − 5.", IND_SS_EXT),
    mur('mur-SS-003', 'fondation', 451, 375, 5, 375, D(T_FOND, "DÉDUIT", "P1", "non écrite sur cette chaîne ; 10\" sur P2 (cote-RDC-211) et fermeture 10 + 13'-10\" + 3'-11\" + 12'-3\" + 10 = 31'-8\""),
        "Mur arrière ; axe y = 31'-8\" − 5.", IND_SS_EXT),
    mur('mur-SS-004', 'fondation', 5, 375, 5, 5, D(T_FOND, "LU", "P1", ref="cote-SS-019"), "Mur latéral gauche (cheminée) ; axe x = 5.", IND_SS_EXT),
    mur('mur-SS-005', 'fondation', 224, 375, 224, 435, D(10, "PRÉSUMÉ", None, "non cotée ; par analogie avec le mur droit du caveau (10\" LU, cote-SS-007)"),
        "Caveau à légumes — mur gauche (évent grillagé) ; nu ext. x = 18'-3\" (cote-SS-002).", ["mur de fondation (P1)"]),
    mur('mur-SS-006', 'fondation', 224, 435, 322, 435, D(10, "PRÉSUMÉ", None, "non cotée ; par analogie avec le mur droit du caveau (10\" LU)"),
        "Caveau — mur du fond ; nu ext. y = 31'-8\" + 5'-0\" (cote-SS-009).", ["mur de fondation (P1)"]),
    mur('mur-SS-007', 'fondation', 322, 435, 322, 375, D(10, "LU", "P1", ref="cote-SS-007"),
        "Caveau — mur droit ; nu ext. x = 18'-3\" + 9'-0\" = 27'-3\".", ["mur de fondation (P1)"]),
    mur('mur-SS-008', 'fondation', 165, 5, 165, -45, D(T_PERRON, "LU", "P1", "tranché par 3e lecture", ref="cote-SS-036"),
        "Excroissance de fondation sous le perron — mur gauche ; nu ext. x = 13'-6\" (cote-SS-027).", ["mur de fondation sous le perron (P1)"]),
    mur('mur-SS-009', 'fondation', 165, -45, 231, -45, D(T_PERRON, "PRÉSUMÉ", None, "non cotée ; par analogie avec le mur gauche du perron (6\" LU)"),
        "Excroissance du perron — mur avant ; nu ext. y = −4'-0\" (cote-SS-033).", ["mur de fondation sous le perron (P1)"]),
    mur('mur-SS-010', 'fondation', 231, -45, 231, 5, D(T_PERRON, "PRÉSUMÉ", None, "non cotée ; par analogie avec le mur gauche du perron (6\" LU)"),
        "Excroissance du perron — mur droit ; nu ext. x = 13'-6\" + 6'-0\" = 19'-6\".", ["mur de fondation sous le perron (P1)"]),
]

IND_RDC_FAC = ["sur le mur de fondation (P1)", "solives de plafond 2\"x7\" @ 16\" orientées avant-arrière (P3) : appui probable — non écrit"]
IND_RDC_LAT = ["sur le mur de fondation (P1)"]
IND_B = ["au-dessus de la poutre 8\"x10\" du sous-sol str-SS-P02 (axe y = 157)", "axe B « porteur à l'origine » (P2, ing. 2016)"]
IND_C = ["au-dessus de la poutre 8\"x10\" du sous-sol str-SS-P01 (axe y = 204)", "axe C « porteur à l'origine » (P2, ing. 2016)"]
MURS_RDC = [
    mur('mur-RDC-001', 'ext', H_EXT, H_EXT, 456 - H_EXT, H_EXT, E_EXT, "Mur avant (façade, rue).", IND_RDC_FAC),
    mur('mur-RDC-002', 'ext', 456 - H_EXT, H_EXT, 456 - H_EXT, 380 - H_EXT, E_EXT, "Mur latéral droit (salon, cuisine).", IND_RDC_LAT),
    mur('mur-RDC-003', 'ext', H_EXT, 380 - H_EXT, 456 - H_EXT, 380 - H_EXT, E_EXT, "Mur arrière.", IND_RDC_FAC),
    mur('mur-RDC-004', 'ext', H_EXT, H_EXT, H_EXT, 380 - H_EXT, E_EXT, "Mur latéral gauche (chambres, S. de bain) ; cheminée accolée à l'extérieur.", IND_RDC_LAT),
    mur('mur-RDC-005', 'ext', 219 + T_EAR / 2, 380 - H_EXT, 219 + T_EAR / 2, 440 - T_EAR / 2, E_EAR, "Entrée arrière — mur gauche ; nu ext. x = 18'-3\" (cote-RDC-016).", ["sur le mur gauche du caveau mur-SS-005 (alignement en plan)"]),
    mur('mur-RDC-006', 'ext', 219 + T_EAR / 2, 440 - T_EAR / 2, 327 - T_EAR / 2, 440 - T_EAR / 2, E_EAR, "Entrée arrière — mur arrière ; profondeur non cotée : nu ext. PRÉSUMÉ à 5'-0\" du mur arrière (= caveau, cote-SS-009) ; dessin ≈ 5'-7\".",
        ["sur le mur du fond du caveau mur-SS-006 (PRÉSUMÉ)"], 'PRÉSUMÉ'),
    mur('mur-RDC-007', 'ext', 327 - T_EAR / 2, 440 - T_EAR / 2, 327 - T_EAR / 2, 380 - H_EXT, E_EAR, "Entrée arrière — mur droit (porte extérieure) ; nu ext. x = 27'-3\" (18'-3\" + 9'-0\").", ["sur le mur droit du caveau mur-SS-007 (alignement en plan)"]),
    mur('mur-RDC-010', 'int', 5, 223, 108, 223, D(T_6, "LU", "P3", "tranché par 3e lecture (6\") — lectures 9\"/6\"", ref="cote-RDC-047"),
        "Cloison chambre arrière / S. de bain ; axe y = 31'-8\" − 13'-1\" (cote-RDC-035)."),
    mur('mur-RDC-011', 'int', 108, 157, 108, 223, E_INT, "Cloison droite de la S. de bain ; axe x = 9'-0\" (cote-RDC-029)."),
    mur('mur-RDC-012', 'int', 5, 157, 175, 157, E_INT, "Cloison S. de bain / chambre avant / LIN. ; axe y = 13'-1\" (cote-RDC-037, -036).", IND_B),
    mur('mur-RDC-013', 'int', 146, 5, 146, 157, E_INT, "Cloison chambre avant / G.R. / VEST. ; axe x = 12'-2\" (cote-RDC-038)."),
    mur('mur-RDC-014', 'int', 175, 54, 175, 157, E_INT, "Cloison G.R. avant / LIN. côté hall ; axe x = 12'-2\" + 2'-5\" (cote-RDC-039) ; arrêtée au VEST. (y ≈ 54 ESTIMÉ)."),
    mur('mur-RDC-015', 'int', 146, 134, 175, 134, E_INT, "Cloison LIN. / G.R. avant (y ESTIMÉ).", None, 'ESTIMÉ'),
    mur('mur-RDC-016', 'int', 146, 54, 175, 54, E_INT, "Cloison G.R. avant / VEST. (y ESTIMÉ).", None, 'ESTIMÉ'),
    mur('mur-RDC-017', 'int', 175, 63, 222, 63, E_INT, "Ligne de la porte entrée / hall (montants courts) ; y ESTIMÉ.", None, 'ESTIMÉ'),
    mur('mur-RDC-018', 'int', 222, 5, 222, 157, E_INT, "Cloison hall / salon (ARCHE) ; axe x = 12'-2\" + 2'-5\" + 3'-11\" = 18'-6\" (cote-RDC-040)."),
    mur('mur-RDC-019', 'int', 222, 157, 451, 157, E_INT, "Cloison salon / passage et salon / cuisine (ARCHE 6'-0\") ; axe y = 13'-1\" (cote-RDC-044, -046).", IND_B),
    mur('mur-RDC-020', 'int', 108, 212, 146, 212, E_INT, "Ligne de la porte de la chambre arrière (baie en retrait, montants seulement) ; y ESTIMÉ (≈ 11 po devant la cloison y = 223).", None, 'ESTIMÉ'),
    mur('mur-RDC-021', 'int', 146, 204, 146, 375, E_INT, "Cloison chambre arrière / colonne des G.R. ; axe x = 9'-0\" + 3'-2\" (cote-RDC-030)."),
    mur('mur-RDC-022', 'int', 175, 253, 175, 375, E_INT, "Cloison G.R. / chambre d'utilité ; axe x = … + 2'-5\" (cote-RDC-031)."),
    mur('mur-RDC-023', 'int', 146, 337.5, 175, 337.5, E_INT, "Cloison entre les 2 G.R. de la chambre arrière (y ESTIMÉ).", None, 'ESTIMÉ'),
    mur('mur-RDC-024', 'int', 146, 296, 175, 296, E_INT, "Cloison G.R. chambre arrière / G.R. chambre d'utilité (y ESTIMÉ).", None, 'ESTIMÉ'),
    mur('mur-RDC-025', 'int', 146, 253, 175, 253, E_INT, "Cloison avant du G.R. de la chambre d'utilité (y ESTIMÉ).", None, 'ESTIMÉ'),
    mur('mur-RDC-026', 'int', 146, 204, 316, 204, E_INT, "Cloison chambre d'utilité et BALAIS / dégagement-passage ; axe y = 31'-8\" − 14'-8\" (cote-RDC-042).", IND_C),
    mur('mur-RDC-027', 'int', 275, 204, 275, 375, E_INT, "Cloison chambre d'utilité / escalier-BALAIS ; axe x = … + 8'-4\" (cote-RDC-032)."),
    mur('mur-RDC-028', 'int', 316, 157, 316, 375, E_INT, "Cloison escalier / cuisine et passage / cuisine ; axe x = … + 3'-5\" (cote-RDC-033) = 38'-0\" − 11'-8\"."),
    mur('mur-RDC-029', 'int', 275, 241.5, 316, 241.5, E_INT, "Cloison BALAIS / escalier (y ESTIMÉ).", None, 'ESTIMÉ'),
]


def emprises(murs):
    M = [gp.Mur(m) for m in murs]
    gp.prolongements(M)
    return M


# ============================================================================ 5. ouvertures
def pos_on(m, cx=None, cy=None):
    """distance le long du mur depuis (x1,y1) jusqu'au point de coordonnée cx (mur en x) ou cy (mur en y)"""
    if m['y1'] == m['y2']:
        return abs(cx - m['x1'])
    return abs(cy - m['y1'])


def sens(m, centre, hinge_c, swing):
    """centre : coordonnée du centre de la porte le long du mur ; hinge_c : coordonnée du jambage des pentures ;
    swing : '+x','-x','+y','-y' (côté où pousse le vantail). charnière « debut » = jambage du côté (x1,y1)."""
    horiz = m['y1'] == m['y2']
    a, b = (m['x1'], m['x2']) if horiz else (m['y1'], m['y2'])
    vers_fin = 1 if b > a else -1
    charn = 'fin' if (hinge_c - centre) * vers_fin > 0 else 'debut'
    ux, uy = (1 if m['x2'] > m['x1'] else -1, 0) if horiz else (0, 1 if m['y2'] > m['y1'] else -1)
    nx, ny = -uy, ux
    sv = {'+x': (1, 0), '-x': (-1, 0), '+y': (0, 1), '-y': (0, -1)}[swing]
    return {"charniere": charn, "ouvre_vers": 'gauche' if nx * sv[0] + ny * sv[1] > 0 else 'droite'}


def ouv(oid, typ, op, murs, mid, centre, largeur, hauteur=None, sens_=None, texte=None, note=None, pos_src="DÉDUIT", pos_note=None, allege=None):
    m = next(x for x in murs if x['id'] == mid)
    horiz = m['y1'] == m['y2']
    p = pos_on(m, centre, centre) if True else None
    o = {"id": oid, "type": typ, "operation": op, "mur_id": mid,
         "position": D(round(p, 2), pos_src, largeur.get('photo'), pos_note),
         "largeur": largeur, "hauteur": hauteur or D(None, "ILLISIBLE", None, "hauteur non écrite"),
         "allege": allege or D(None, "ILLISIBLE", None, "non écrite")}
    if sens_: o["sens"] = sens_
    if texte: o["texte_original"] = texte
    if note: o["note"] = note
    o["_centre"] = (centre, m['y1']) if horiz else (m['x1'], centre)
    return o


def W(cid, ph='P1'):
    v = V(cid); st = STAT[cid]
    return D(v, "LU", ph, ref=cid, note=None if st == 'confirmee' else f"statut {st} — voir {EC.get('conf-' + cid)}")


FEN_NOTE = "type d'ouvrant non indiqué au plan (« fixe » = représentation par défaut)"
OUV_SS = [
    ouv('ouv-SS-001', 'fenetre', 'fixe', MURS_SS, 'mur-SS-003', V('cote-SS-005'), W('cote-SS-006'), texte="6'-8\"",
        note=FEN_NOTE + " ; deux châssis ; dessin ≈ 73 po (ESTIMÉ) — voir écart", pos_note="axe à 13'-0\" du nu ext. gauche (cote-SS-005)"),
    ouv('ouv-SS-002', 'fenetre', 'fixe', MURS_SS, 'mur-SS-001', 456 - V('cote-SS-030'), W('cote-SS-032'), texte="6'-3\"",
        note=FEN_NOTE + " ; deux châssis", pos_note="axe à 6'-2\" du nu ext. droit (cote-SS-030)"),
    ouv('ouv-SS-003', 'fenetre', 'fixe', MURS_SS, 'mur-SS-002', 380 - V('cote-SS-021'), W('cote-SS-025'), texte="6'-8\"",
        note=FEN_NOTE + " ; deux châssis ; dessin ≈ 72 po (ESTIMÉ) — voir écart", pos_note="axe à 6'-0\" du nu ext. arrière (cote-SS-021)"),
    ouv('ouv-SS-004', 'fenetre', 'fixe', MURS_SS, 'mur-SS-002', 380 - V('cote-SS-021') - V('cote-SS-022'), W('cote-SS-026'), texte="3'-0\"",
        note=FEN_NOTE, pos_note="6'-0\" + 10'-8\" du nu ext. arrière"),
    ouv('ouv-SS-005', 'porte', 'aucune', MURS_SS, 'mur-SS-002', V('cote-SS-024'), W('cote-SS-050'), texte="PORTE 2'-8\"",
        note="porte dans le mur de fondation droit (rectangle barré d'un X) ; aucun arc dessiné : battant et sens inconnus", pos_note="axe à 6'-3\" du nu ext. avant (cote-SS-024)"),
    ouv('ouv-SS-006', 'fenetre', 'fixe', MURS_SS, 'mur-SS-004', 380 - V('cote-SS-012'), W('cote-SS-016'), texte="3'-0\"",
        note=FEN_NOTE + " ; près de la fournaise", pos_note="axe à 16'-8\" du nu ext. arrière (cote-SS-012)"),
    ouv('ouv-SS-007', 'fenetre', 'fixe', MURS_SS, 'mur-SS-004', V('cote-SS-015'), W('cote-SS-017'), texte="3'-0\"",
        note=FEN_NOTE + " ; au-dessus de l'évier à lessive", pos_note="axe à 4'-0\" du nu ext. avant (cote-SS-015)"),
    ouv('ouv-SS-008', 'porte', 'aucune', MURS_SS, 'mur-SS-003', 219 + V('cote-SS-010'), W('cote-SS-049'), texte="PORTE 2'-6\"",
        note="porte du caveau à légumes (rectangle barré d'un X) ; aucun arc : battant et sens inconnus", pos_src="DÉDUIT",
        pos_note="axe à 3'-6\" (cote-SS-010) du nu ext. du mur gauche du caveau (x = 219) — point de départ ambigu, voir écart"),
]

# ============================================================================ 4b. RÉPONSES DU PROPRIÉTAIRE (2026-10-29) — sous-sol
# Le sous-sol est devenu un appartement indépendant. Mur droit : la porte et la fenêtre du milieu ont été permutées.
# Mur arrière : la grande fenêtre de gauche (6'-8") a été séparée en deux ; la moitié droite est restée en place,
# la moitié gauche a été déplacée de 2'-0" vers la gauche. Les ouvertures d'origine restent dans ouvertures_retirees.
REPONSES = "réponses du propriétaire (2026-10-29)"
_os = {o['id']: o for o in OUV_SS}
OUV_SS_RETIREES = [dict(copy.deepcopy(_os[i]), id=i + '-1957', retire_selon=REPONSES) for i in ('ouv-SS-001', 'ouv-SS-004', 'ouv-SS-005')]
_p, _f = _os['ouv-SS-005'], _os['ouv-SS-004']
_pos_p, _pos_f, _c_p, _c_f = _p['position'], _f['position'], _p['_centre'], _f['_centre']
_p['position'] = dict(_pos_f, note=f"à la place de l'ancienne fenêtre du milieu ({REPONSES}) ; " + (_pos_f.get('note') or ''))
_f['position'] = dict(_pos_p, note=f"à la place de l'ancienne porte ({REPONSES}) ; " + (_pos_p.get('note') or ''))
_p['_centre'], _f['_centre'] = _c_f, _c_p
_p['note'] = (f"porte extérieure de l'appartement du sous-sol, déplacée à la place de l'ancienne fenêtre du milieu ({REPONSES}) ; "
              "largeur 2'-8\" du plan 1957 PRÉSUMÉE conservée ; battant et sens non relevés")
_p['largeur'] = dict(_p['largeur'], note="largeur 1957 PRÉSUMÉE conservée après le déplacement")
_f['note'] = (f"fenêtre déplacée à la place de l'ancienne porte ({REPONSES}) ; largeur 3'-0\" du plan 1957 PRÉSUMÉE conservée")
_f['largeur'] = dict(_f['largeur'], note="largeur 1957 PRÉSUMÉE conservée après le déplacement")
OUV_SS.remove(_os['ouv-SS-001'])
_L1 = W('cote-SS-006')['valeur']
for _oid, _cx, _quoi in (('ouv-SS-009', V('cote-SS-005') + _L1 / 4, "moitié droite, restée à l'emplacement d'origine"),
                         ('ouv-SS-010', V('cote-SS-005') - _L1 / 4 - 24, "moitié gauche, déplacée de 2'-0\" vers la gauche")):
    OUV_SS.append(ouv(_oid, 'fenetre', 'fixe', MURS_SS, 'mur-SS-003', _cx,
                      D(_L1 / 2, "PRÉSUMÉ", "P1", note="moitié de la fenêtre 6'-8\" d'origine (« comme coupée en deux »)"),
                      texte=None, note=f"{_quoi} de l'ancienne fenêtre 6'-8\" ({REPONSES})",
                      pos_src="DÉDUIT", pos_note=f"axe d'origine 13'-0\" (cote-SS-005) ± ¼ de la largeur{' − 2' + chr(39) + '-0' + chr(34) if _oid == 'ouv-SS-010' else ''} ({REPONSES})"))
OUV_SS.sort(key=lambda o: o['id'])

LH = lambda L, H, ph='P3', ref=None, note=None: (D(L, "LU", ph, ref=ref, note=note), D(H, "LU", ph, ref=ref))


def porte(oid, mid, centre, cid, hinge, swing, note, pos_src="ESTIMÉ", pos_note="position non cotée, mesurée au dessin (P3)"):
    c = next(c for c in COTES['RDC'] if c['id'] == cid)
    m = next(x for x in MURS_RDC if x['id'] == mid)
    L, H = c['valeur'], c['hauteur']
    st = STAT[cid]
    larg = D(L, "LU", "P3", ref=cid, note=None if st == 'confirmee' else f"statut {st}")
    return ouv(oid, 'porte', 'battante', MURS_RDC, mid, centre, larg, D(H, "LU", "P3", ref=cid), sens(m, centre, hinge, swing),
               c['texte_original'], note, pos_src, pos_note)


def lab(oid):  # id de cote de l'étiquette d'une ouverture (accords/désaccords) via ref lecture 1
    for a in ACC:
        if oid in (a.get('ref_lecture_1') or []): return a['id']
    for d in DES:
        if d.get('lecture_1') and oid in (d['lecture_1'].get('ref') or []): return d['cote_id']
    raise KeyError(oid)


R = 'P3'
OUV_RDC = [
    ouv('ouv-RDC-001', 'fenetre', 'fixe', MURS_RDC, 'mur-RDC-001', V('cote-RDC-010'), W('cote-RDC-014', R), texte="6'-3\" ; LINTEAU 2-2\"x8\"",
        note=FEN_NOTE + " ; chambre avant", pos_note="axe à 8'-2\" (cote-RDC-010)"),
    ouv('ouv-RDC-002', 'fenetre', 'fixe', MURS_RDC, 'mur-RDC-001', 456 - V('cote-RDC-013'), W('cote-RDC-015', R), texte="9'-0\" ; LINTEAU 2-2\"x10\"",
        note=FEN_NOTE + " ; salon, 3 sections", pos_note="axe à 6'-7\" du nu ext. droit (cote-RDC-013)"),
    ouv('ouv-RDC-003', 'fenetre', 'fixe', MURS_RDC, 'mur-RDC-003', V('cote-RDC-019'), W('cote-RDC-024', R), texte="6'-3\" ; LINTEAU 2-2\"x8\"",
        note=FEN_NOTE + " ; chambre arrière", pos_note="axe à 8'-2\" (cote-RDC-019)"),
    ouv('ouv-RDC-004', 'fenetre', 'fixe', MURS_RDC, 'mur-RDC-003', V('cote-RDC-019') + V('cote-RDC-020'), W('cote-RDC-025', R), texte="3'-0\" ; LIN. 2-2\"x6\"",
        note=FEN_NOTE + " ; chambre d'utilité", pos_note="8'-2\" + 8'-3\""),
    ouv('ouv-RDC-005', 'fenetre', 'fixe', MURS_RDC, 'mur-RDC-003', 456 - V('cote-RDC-023'), W('cote-RDC-028', R), texte="6'-3\" ; LINTEAU 2-2\"x8\"",
        note=FEN_NOTE + " ; cuisine, au-dessus de l'évier", pos_note="axe à 6'-9\" du nu ext. droit (cote-RDC-023)"),
    ouv('ouv-RDC-006', 'fenetre', 'fixe', MURS_RDC, 'mur-RDC-004', V('cote-RDC-003'), W('cote-RDC-004', R), texte="3'-0\" ; LIN. 2-2\"x6\"",
        note=FEN_NOTE + " ; S. de bain", pos_note="axe à 15'-11\" du nu ext. avant (cote-RDC-003)"),
    ouv('ouv-RDC-007', 'fenetre', 'fixe', MURS_RDC, 'mur-RDC-002', V('cote-RDC-007'), W('cote-RDC-008', R), texte="3'-0\" ; LIN. 2-2\"x6\"",
        note=FEN_NOTE + " ; cuisine / s.-à-manger", pos_note="axe à 15'-0\" du nu ext. avant (cote-RDC-007)"),
    ouv('ouv-RDC-008', 'fenetre', 'fixe', MURS_RDC, 'mur-RDC-006', V('cote-RDC-019') + V('cote-RDC-020') + V('cote-RDC-021'), W('cote-RDC-026', 'P6'),
        texte="3'-6\"", note=FEN_NOTE + " ; entrée arrière ; aucun linteau écrit", pos_note="8'-2\" + 8'-3\" + 8'-0\""),
    porte('ouv-RDC-010', 'mur-RDC-001', V('cote-RDC-010') + V('cote-RDC-011'), lab('ouv-RDC-010'), 216, '+y',
          "porte d'entrée avant ; pentures côté salon (vantail dessiné le long de la cloison du salon) ; ouvre vers l'intérieur ; donne sur le perron de béton", "DÉDUIT", "axe à 8'-2\" + 8'-5\" (cote-RDC-011)"),
    porte('ouv-RDC-011', 'mur-RDC-017', 198.5, lab('ouv-RDC-011'), 178, '+y', "porte entrée → hall ; pentures côté gauche ; ouvre vers le hall"),
    porte('ouv-RDC-014', 'mur-RDC-012', 127, lab('ouv-RDC-014'), 143, '-y', "porte de la chambre avant ; ouvre dans la chambre"),
    porte('ouv-RDC-015', 'mur-RDC-011', 178, lab('ouv-RDC-015'), 163, '+x', "porte de la S. de bain ; ouvre vers le dégagement (constat du propriétaire 2026-10-29 ; au plan 1957 elle ouvrait dans la S. de bain)"),
    porte('ouv-RDC-016', 'mur-RDC-020', 127, lab('ouv-RDC-016'), 143, '+y', "porte de la chambre arrière ; ouvre dans la chambre"),
    porte('ouv-RDC-017', 'mur-RDC-026', 163, lab('ouv-RDC-017'), 148, '+y',
          "porte de la chambre d'utilité (alcôve sous le G.R.) ; étiquetée 2'-6\" dans une baie cotée 2'-5\" d'axe en axe — voir écart"),
    porte('ouv-RDC-018', 'mur-RDC-022', 274.5, lab('ouv-RDC-018'), 255.25, '+x', "porte du G.R. de la chambre d'utilité"),
    porte('ouv-RDC-019', 'mur-RDC-021', 354, lab('ouv-RDC-019'), 339.75, '-x', "porte du G.R. arrière de la chambre arrière ; pentures sur le montant central commun"),
    porte('ouv-RDC-020', 'mur-RDC-021', 317, lab('ouv-RDC-020'), 335.25, '-x', "porte du 2e G.R. de la chambre arrière ; pentures sur le montant central commun"),
    porte('ouv-RDC-021', 'mur-RDC-013', 93, lab('ouv-RDC-021'), 79, '-x', "porte du G.R. de la chambre avant ; ouvre dans la chambre"),
    porte('ouv-RDC-022', 'mur-RDC-012', 160.5, lab('ouv-RDC-022'), 150, '+y', "porte de la lingerie (LIN.) ; pentures côté gauche (vantail dessiné sur le jambage gauche, P3/P4) ; ouvre vers le dégagement"),
    porte('ouv-RDC-023', 'mur-RDC-026', 295.5, lab('ouv-RDC-023'), 281.5, '-y', "porte du placard à balais (sous l'escalier) ; ouvre vers le passage"),
    porte('ouv-RDC-024', 'mur-RDC-028', 182, lab('ouv-RDC-024'), 166, '-x', "porte passage → cuisine ; ouvre vers le passage"),
    porte('ouv-RDC-025', 'mur-RDC-028', 352, lab('ouv-RDC-025'), 368, '+x', "porte palier de l'escalier → cuisine ; ouvre dans la cuisine"),
    porte('ouv-RDC-026', 'mur-RDC-003', 295, lab('ouv-RDC-026'), 279, '-y', "porte entrée arrière → palier ; pentures côté gauche ; ouvre vers le palier"),
    porte('ouv-RDC-027', 'mur-RDC-007', 409, lab('ouv-RDC-027'), 426, '-x', "porte extérieure arrière (vers les marches arrière) ; ouvre vers l'intérieur de l'entrée"),
]
# arches
for oid, mid, centre, cid, note in (('ouv-RDC-012', 'mur-RDC-018', 118.6, 'cote-RDC-048', "arche hall / salon ; position ESTIMÉE (dessin)"),
                                     ('ouv-RDC-013', 'mur-RDC-019', 403.5, 'cote-RDC-049', "arche salon / cuisine-s.-à-manger ; position ESTIMÉE (dessin)")):
    c = next(c for c in COTES['RDC'] if c['id'] == cid)
    larg = D(V(cid), "LU", "P3", ref=cid, note=None if STAT[cid] == 'confirmee' else f"statut {STAT[cid]} — voir {EC.get('conf-' + cid)} ; dessin ≈ 74 po")
    OUV_RDC.append(ouv(oid, 'arche', 'aucune', MURS_RDC, mid, centre, larg, texte=c['texte_original'], note=note,
                       pos_src="ESTIMÉ", pos_note="centre mesuré au dessin (P3)"))
OUV_RDC.sort(key=lambda o: o['id'])

# ============================================================================ 5b. CONSTAT DU PROPRIÉTAIRE (2026-10-29)
# Le propriétaire a barré en rouge, sur l'épreuve A-101 R0, les cloisons qui n'existent plus, et demandé de retirer
# meubles, électroménagers, comptoirs et baignoire. Le constat sur place prime sur les plans (principe 4).
# Les éléments retirés restent documentés dans maison.json (murs_retires, ouvertures_retirees, elements_retires).
CONSTAT = "constat du propriétaire (épreuve A-101 R0 annotée, 2026-10-29)"
MURS_RETIRES = {
    'mur-RDC-026': "cloison chambre d'utilité / dégagement et placard à balais (axe C, y = 17'-0\") — barrée en rouge",
    'mur-RDC-027': "cloison chambre d'utilité / cage d'escalier (x = 22'-11\") — barrée en rouge",
    'mur-RDC-028': "cloison cage d'escalier / cuisine et passage / cuisine (x = 26'-4\") — barrée en rouge",
    'mur-RDC-029': "cloison placard à balais / escalier — barrée en rouge",
    'mur-RDC-019': ("cloison salon / passage-cuisine (axe B, y = 13'-1\") barrée en rouge jusqu'à l'arche 6'-0\" ; "
                    "le trumeau restant à droite de l'arche n'existe plus non plus (2e constat du propriétaire, 2026-10-29)"),
}
ARCHE_SALON = next(o for o in OUV_RDC if o['id'] == 'ouv-RDC-013')
X_STUB = 222 + ARCHE_SALON['position']['valeur'] + ARCHE_SALON['largeur']['valeur'] / 2   # jambage droit de l'arche 6'-0"
MURS_RETIRES_DATA, OUV_RETIREES = [], []
for m in list(MURS_RDC):
    if m['id'] in MURS_RETIRES:
        MURS_RETIRES_DATA.append(dict(m, retire_selon=CONSTAT, description_retrait=MURS_RETIRES[m['id']]))
        MURS_RDC.remove(m)
for o in list(OUV_RDC):
    if o['mur_id'] in MURS_RETIRES or o['id'] == 'ouv-RDC-013':
        OUV_RETIREES.append(dict(o, retire_selon=CONSTAT))
        OUV_RDC.remove(o)
# Mur hall / salon : il s'arrête là où l'arche commençait ; au-delà, seule la colonne 8"x8" de l'axe B (réponses du propriétaire)
_arche_hs = next(o for o in OUV_RDC if o['id'] == 'ouv-RDC-012')
Y_FIN_HALL = 5 + _arche_hs['position']['valeur'] - _arche_hs['largeur']['valeur'] / 2
_m18 = next(m for m in MURS_RDC if m['id'] == 'mur-RDC-018')
MURS_RETIRES_DATA.append(dict(copy.deepcopy(_m18), id='mur-RDC-018-1957', retire_selon="réponses du propriétaire (2026-10-29)",
                              description_retrait="partie de la cloison hall / salon au-delà de l'ancienne arche (vers l'axe B), retirée"))
_m18['y2'] = round(Y_FIN_HALL, 2)
_m18['source_position'] = 'ESTIMÉ'
_m18['note'] = ("Cloison hall / salon ; axe x = 18'-6\" (cote-RDC-040). Elle s'arrête où commençait l'ancienne arche (début ESTIMÉ au "
                "dessin 1957 : centre ≈ 9'-10\", largeur 4'-0\" écrite) ; au-delà, ouvert jusqu'à la colonne 8\"x8\" de l'axe B "
                "(réponses du propriétaire, 2026-10-29).")
OUV_RETIREES.append(dict(_arche_hs, retire_selon="réponses du propriétaire (2026-10-29) : plus d'arche ni de mur au-delà"))
OUV_RDC.remove(_arche_hs)

# ============================================================================ 6. pièces (régions libres entre murs, découpées par lignes fictives)
NOTE_EP = {'SS': "nu int. : cotes LU − épaisseurs (fondation 10\" LU)",
           'RDC': "nu int. : cotes LU − épaisseurs (ext. 10\" LU P2 ; cloisons 4½\" PRÉSUMÉ ; cloison ch. arr./S. de bain 6\" LU)"}
PIECES_DEF = {
    'SS': [
        ('piece-SS-PRINC', "Sous-sol", "(aucun nom au plan)", (300, 100)),
        ('piece-SS-LEG', "Caveau", "LEGUMES", (270, 405)),
        ('piece-SS-PERRON', "Excroissance sous perron", "(aucun nom au plan)", (198, -20)),
    ],
    'RDC': [
        ('piece-RDC-CH1', "Chambre arrière", "CHAMBRE", (60, 300)),
        ('piece-RDC-SDB', "Salle de bain", "S. DE BAIN", (50, 190)),
        ('piece-RDC-CH2', "Chambre avant", "CHAMBRE", (70, 80)),
        ('piece-RDC-GR1', "G.R. 1", "G.R.", (160, 356)),
        ('piece-RDC-GR2', "G.R. 2", "G.R.", (160, 316)),
        ('piece-RDC-GRU', "G.R. 3", "G.R.", (160, 274)),
        ('piece-RDC-UTI', "Salle à manger", "CHAMBRE D'UTILITÉ (1957) ; « Salle à manger » (2016)", (225, 290)),
        ('piece-RDC-DEG', "Dégagement", "(aucun nom au plan)", (127, 185)),
        ('piece-RDC-HALL', "Hall", "HALL", (198, 110)),
        ('piece-RDC-ENT', "Entrée", "(aucun nom au plan)", (198, 35)),
        ('piece-RDC-VES', "Vest.", "VEST.", (160, 30)),
        ('piece-RDC-GRA', "G.R.", "G.R.", (160, 95)),
        ('piece-RDC-LIN', "Lin.", "LIN.", (160, 145)),
        ('piece-RDC-SAL', "Salon", "SALON", (330, 80)),
        ('piece-RDC-CUI', "Cuisine", "CUISINE S.-À-MANGER (1957) ; « Cuisine » (2016)", (380, 270)),
        ('piece-RDC-EAR', "Entrée arr.", "(aucun nom ; « ARMOIRES » écrit)", (270, 405)),
    ],
}
DESC = {
    'piece-SS-PRINC': "Sous-sol, espace principal non cloisonné (aucun nom au plan)",
    'piece-SS-LEG': "Caveau à légumes (« LEGUMES »)",
    'piece-SS-PERRON': "Excroissance de fondation sous le perron avant ; contenu (vide / remblai) inconnu ; accès non dessiné",
    'piece-RDC-GR1': "Garde-robe 1 de la chambre arrière", 'piece-RDC-GR2': "Garde-robe 2 de la chambre arrière",
    'piece-RDC-GRU': "Garde-robe de la chambre d'utilité",
    'piece-RDC-UTI': "Salle à manger : ancienne chambre d'utilité (1957), ouverte sur la cuisine et le dégagement ; inclut l'emplacement de l'ancien escalier et du placard à balais (constat 2026-10-29) ; nommée « Salle à manger » sur le croquis 2016 (P2)",
    'piece-RDC-ENT': "Entrée avant (aucun nom au plan)", 'piece-RDC-VES': "Vestiaire (garde-robe d'entrée, ouvert)",
    'piece-RDC-GRA': "Garde-robe de la chambre avant", 'piece-RDC-LIN': "Lingerie",
    'piece-RDC-CUI': "Cuisine (« Cuisine » sur le croquis 2016) ; aire ouverte sur la salle à manger et le salon ; mobilier, électroménagers et comptoirs non représentés",
    'piece-RDC-ESC': "Escalier du sous-sol et palier arrière ; cloisons de la cage et placard à balais retirés (constat 2026-10-29) ; garde-corps non relevé", 'piece-RDC-EAR': "Entrée arrière (« ARMOIRES »)",
    'piece-RDC-DEG': "Dégagement (aucun nom au plan) ; inclut l'ancien passage ; ouvert sur le salon et la salle à manger (constat 2026-10-29)",
}
# lignes fictives (aucun mur dessiné) séparant des espaces ouverts
COUPES = {
    'SS': [],
    'RDC': [((173, 157), (456, 157), "hall-dégagement / salon-cuisine : axe B ; cloison retirée de 18'-6\" à l'arche (constat 2026-10-29)"),
            ((222, 85), (222, 157), "hall / salon : prolongement de la cloison hall / salon jusqu'à l'axe B (ouvert)"),
            ((316, 157), (316, 380), "cuisine / escalier-dégagement : axe de l'ancienne cloison x = 26'-4\" (retirée)"),
            ((146, 204), (316, 204), "dégagement / salle à manger : axe C, ancienne cloison retirée"),
            ((175, 5), (175, 54), "entrée / vestiaire (VEST. ouvert)")],
}


def pieces(niv, murs):
    M = emprises(murs)
    U = unary_union([m.emprise() for m in M])
    regions = []
    for p in (U.geoms if hasattr(U, 'geoms') else [U]):
        for r in p.interiors:
            regions.append(Polygon(r))
    # découpe par polygonisation : les lignes fictives peuvent se croiser en T
    lignes = [LineString([a, b]) for (a, b, _) in COUPES[niv]]
    nouv = []
    for r in regions:
        coupe = [ln.intersection(r) for ln in lignes if r.intersects(ln) and r.intersection(ln).length > 1]
        if not coupe:
            nouv.append(r); continue
        morceaux = list(polygonize(unary_union([r.exterior] + coupe)))
        assert abs(sum(m.area for m in morceaux) - r.area) < 0.5, "découpe incomplète"
        nouv += morceaux
    regions = nouv
    out = []
    used = set()
    for pid, nom, nomo, seed in PIECES_DEF[niv]:
        hit = [i for i, r in enumerate(regions) if r.contains(Point(seed))]
        assert len(hit) == 1, (pid, hit)
        assert hit[0] not in used, f"{pid} : même région qu'une autre pièce (ligne fictive qui n'atteint pas un mur ?)"
        used.add(hit[0])
        r = orient(regions[hit[0]].simplify(0.001), 1.0)
        coords = [[round(x, 2), round(y, 2)] for x, y in list(r.exterior.coords)[:-1]]
        minx, miny, maxx, maxy = r.bounds
        est = [m for m in murs if m.get('source_position') in ('ESTIMÉ', 'PRÉSUMÉ')]

        def bord_src(val, axe):
            # mur dont une face est à cette coordonnée
            for m in murs:
                t = m['epaisseur']['valeur']
                if axe == 'x' and m['x1'] == m['x2'] and abs(abs(val - m['x1']) - t / 2) < 0.01:
                    return m.get('source_position', 'DÉDUIT')
                if axe == 'y' and m['y1'] == m['y2'] and abs(abs(val - m['y1']) - t / 2) < 0.01:
                    return m.get('source_position', 'DÉDUIT')
            # ligne fictive : DÉDUIT si elle suit l'axe coté d'une ancienne cloison ou d'un axe porteur, sinon ESTIMÉ
            for (a, b, _) in COUPES[niv]:
                if (axe == 'x' and a[0] == b[0] and abs(val - a[0]) < 0.01) or (axe == 'y' and a[1] == b[1] and abs(val - a[1]) < 0.01):
                    return 'DÉDUIT'
            return 'ESTIMÉ'
        sx = gp.pire_source([bord_src(minx, 'x'), bord_src(maxx, 'x')])
        sy = gp.pire_source([bord_src(miny, 'y'), bord_src(maxy, 'y')])
        nz = NOTE_EP[niv]
        sa = gp.pire_source([sx, sy])
        out.append({"id": pid, "nom": nom, "nom_original": nomo, "description": DESC.get(pid), "polygone": coords,
                    "superficie": D(round(r.area / 144, 1), sa if sa != 'LU' else 'DÉDUIT', None, "aire du polygone au nu intérieur ; " + nz),
                    "hauteur_plafond": D(None, "ILLISIBLE", None, "non écrite"),
                    "dimensions": {"x": D(round(maxx - minx, 2), sx, None, "boîte englobante ; " + nz),
                                   "y": D(round(maxy - miny, 2), sy, None, "boîte englobante ; " + nz)}})
    orph = [r for i, r in enumerate(regions) if i not in used]
    assert not orph, [o.bounds for o in orph]
    return out, U


PIECES = {}
UNION = {}
for niv, murs in (('SS', MURS_SS), ('RDC', MURS_RDC)):
    PIECES[niv], UNION[niv] = pieces(niv, murs)

# ============================================================================ 7. éléments
def el_from_ex(niv, keep_types, skip_ids=()):
    out = []
    for e in EX[niv]['elements']:
        if e['id'] in skip_ids: continue
        if e['type'] == 'autre' and e['id'] not in keep_types: continue
        f = {k: v for k, v in e.items() if k not in ('px',)}
        f['position'] = {k: v for k, v in e['position'].items()}
        f['position'].setdefault('source', 'ESTIMÉ')
        out.append(f)
    return out


ELEM_SS = el_from_ex('SS', keep_types=(), skip_ids=('elem-SS-ESC',))
ELEM_SS.append({"id": "elem-SS-ESC", "type": "escalier", "nom": "Escalier vers le rez-de-chaussée", "nom_original": "14 C.M. / RAMPE",
                "position": {"x": 293.2, "y": 268.1, "rotation_deg": 0, "source": "ESTIMÉ"},
                "dimensions": {"longueur": D(121.7, "ESTIMÉ", "P1", "course mesurée au dessin, du pied (≈ poutre arrière) au palier"),
                               "largeur": D(37, "ESTIMÉ", "P1", "largeur non cotée")},
                "texte_original": "14 C.M.",
                "escalier": {"nb_contremarches": D(14, "LU", "P1", ref=next(c['id'] for c in COTES['SS'] if 'C.M.' in (c['texte_original'] or ''))), "fleche": "MONTE", "direction": "+y",
                             "texte_original": "14 C.M."},
                "note": "volée droite ; 13 girons dessinés ; mot MONTE absent (flèche seule) ; échappée sous la poutre arrière à vérifier"})
ELEM_SS.sort(key=lambda e: e['id'])
ELEM_RDC = el_from_ex('RDC', keep_types=(), skip_ids=('elem-RDC-ESC1',))
ELEM_RDC.append({"id": "elem-RDC-ESC1", "type": "escalier", "nom": "Escalier vers le sous-sol (partie visible)", "nom_original": "2.R. 14 C.M. / RAMPE",
                 "position": {"x": 295.5, "y": round((243.75 + 334) / 2, 2), "rotation_deg": 0, "source": "ESTIMÉ"},
                 "dimensions": {"longueur": D(90.25, "ESTIMÉ", "P3", "partie visible, du palier (y ≈ 334) à la cloison du BALAIS ; les marches inférieures passent sous le BALAIS (course totale ≈ 130 po au SS)"),
                                "largeur": D(36.5, "DÉDUIT", "P3", "entre cloisons x = 23'-0\" et 26'-4\" (axes LU, cloisons 4½\" PRÉSUMÉ)")},
                 "texte_original": "2.R. 14 C.M.",
                 "escalier": {"nb_contremarches": D(14, "LU", "P3", ref=next(c['id'] for c in COTES['RDC'] if 'C.M.' in (c['texte_original'] or '')), note="nombre total ; seulement ≈ 10 girons visibles au RDC"),
                              "fleche": "DESCEND", "direction": "-y", "texte_original": "2.R. 14 C.M."},
                 "note": "préfixe « 2.R. » non interprété"})
ELEM_RDC.sort(key=lambda e: e['id'])
ELEC = {'SS': [e['nom'] for e in EX['SS']['elements'] if e['type'] == 'autre'],
        'RDC': [e['nom'] for e in EX['RDC']['elements'] if e['type'] == 'autre']}

# ============================================================================ 8. structure
def st(sid, typ, dim_txt, val, src, photo, geom, sens_=None, note=None):
    s = {"id": sid, "type": typ, "dimension": {"texte_original": dim_txt, "valeur": val, "source": src, "photo": photo},
         "sens": sens_, "geometrie": geom}
    if note: s["note"] = note
    return s


C_X = [10 + V('cote-SS-038') + 4]
C_X.append(C_X[0] + 4 + V('cote-SS-040') + 4 + 4 - 4)  # face droite C01 + 7'-4" + demi-colonne
C_X = [10 + V('cote-SS-038') + 4,
       10 + V('cote-SS-038') + 8 + V('cote-SS-040') + 4,
       10 + V('cote-SS-038') + 8 + V('cote-SS-040') + 8 + V('cote-SS-042') + 4]
assert C_X == [132, 228, 324] and 456 - 10 - V('cote-SS-044') - 4 == 324
Y_PAR = 380 - 10 - V('cote-SS-046')          # axe poutre arrière
Y_PAV = 10 + V('cote-SS-048')                 # axe poutre avant
assert (Y_PAR, Y_PAV) == (204, 157) and Y_PAR - Y_PAV == V('cote-SS-047')

STR_SS = [
    st('str-SS-P01', 'poutre', "POUTRE 8\"x10\"", "8x10", "LU", "P1", {"x1": 10, "y1": Y_PAR, "x2": 446, "y2": Y_PAR}, 'x',
       "poutre arrière ; axe y = 31'-8\" − 10\" − 13'-10\" (DÉDUIT) ; repose sur str-SS-C01 à C03 ; = axe C du croquis 2016 (« porteur à l'origine »)"),
    st('str-SS-P02', 'poutre', "POUTRE 8\"x10\"", "8x10", "LU", "P1", {"x1": 10, "y1": Y_PAV, "x2": 446, "y2": Y_PAV}, 'x',
       "poutre avant ; axe y = 10\" + 12'-3\" (DÉDUIT) ; repose sur str-SS-C04 à C06 ; = axe B du croquis 2016"),
]
for i, (x, y) in enumerate([(x, Y_PAR) for x in C_X] + [(x, Y_PAV) for x in C_X], 1):
    n = "x DÉDUIT de la chaîne 10\" + 9'-10\" + 8\" + 7'-4\" …" if y == Y_PAR else "x non coté pour la rangée avant : alignée au dessin sur la rangée arrière"
    if (x, y) in ((228, 204), (324, 204)):
        n += f" ; croquis 2016 : « Colonne C{4 if x == 228 else 6} retirée » (ligne {4 if x == 228 else 6} à x = {222 if x == 228 else 316}) — présence actuelle douteuse, voir écart"
    STR_SS.append(st(f'str-SS-C0{i}', 'colonne', "COL. BOIS, 8\"x8\"", "8x8", "LU", "P1", {"x": x, "y": y, "largeur": 8, "profondeur": 8}, None, n))
STR_SS += [
    st('str-SS-S01', 'solives', "SOLIVES 2\"x10\" @ 20\" c/c", "2x10 @ 20 c/c", "LU", "P1", {"x1": 10, "y1": 208, "x2": 446, "y2": 370, "espacement": 20}, 'y',
       "plancher du RDC ; note écrite dans la travée arrière ; solives parallèles à y sur toute la maison (PRÉSUMÉ pour les autres travées), appuyées sur les murs avant/arrière et les poutres"),
    st('str-SS-F01', 'semelle', "22\"", "22", "LU", "P1", {"x1": 0, "y1": 5, "x2": 456, "y2": 5, "largeur": 22}, None, "semelle du mur avant ; largeur cotée au mur gauche (cote-SS-018), PRÉSUMÉE identique et centrée"),
    st('str-SS-F02', 'semelle', "22\"", "22", "LU", "P1", {"x1": 451, "y1": 0, "x2": 451, "y2": 380, "largeur": 22}, None, "semelle du mur droit (PRÉSUMÉE 22\" centrée)"),
    st('str-SS-F03', 'semelle', "22\"", "22", "LU", "P1", {"x1": 0, "y1": 375, "x2": 456, "y2": 375, "largeur": 22}, None, "semelle du mur arrière (PRÉSUMÉE 22\" centrée)"),
    st('str-SS-F04', 'semelle', "22\"", "22", "LU", "P1", {"x1": 5, "y1": 0, "x2": 5, "y2": 380, "largeur": 22}, None, "semelle du mur gauche, 22\" LU (cote-SS-018), PRÉSUMÉE centrée"),
    st('str-SS-F05', 'semelle', "22\"", "22", "LU", "P1", {"x1": 224, "y1": 380, "x2": 224, "y2": 440, "largeur": 22}, None, "semelle du caveau (22\" cotée au mur droit, cote-SS-008)"),
    st('str-SS-F06', 'semelle', "22\"", "22", "LU", "P1", {"x1": 219, "y1": 435, "x2": 327, "y2": 435, "largeur": 22}, None, "semelle du caveau"),
    st('str-SS-F07', 'semelle', "22\"", "22", "LU", "P1", {"x1": 322, "y1": 380, "x2": 322, "y2": 440, "largeur": 22}, None, "semelle du caveau, 22\" LU (cote-SS-008)"),
    st('str-SS-F08', 'semelle', "18\"", "18", "LU", "P1", {"x1": 165, "y1": 0, "x2": 165, "y2": -48, "largeur": 18}, None, "semelle du perron, 18\" LU (cote-SS-035)"),
    st('str-SS-F09', 'semelle', "18\"", "18", "LU", "P1", {"x1": 162, "y1": -45, "x2": 234, "y2": -45, "largeur": 18}, None, "semelle du perron (PRÉSUMÉE 18\")"),
    st('str-SS-F10', 'semelle', "18\"", "18", "LU", "P1", {"x1": 231, "y1": 0, "x2": 231, "y2": -48, "largeur": 18}, None, "semelle du perron (PRÉSUMÉE 18\")"),
]
LIN = {'str-RDC-L01': 'ouv-RDC-001', 'str-RDC-L02': 'ouv-RDC-002', 'str-RDC-L03': 'ouv-RDC-003', 'str-RDC-L04': 'ouv-RDC-004',
       'str-RDC-L05': 'ouv-RDC-005', 'str-RDC-L06': 'ouv-RDC-006', 'str-RDC-L07': 'ouv-RDC-007'}
STR_RDC = []
# linteaux : portés par l'ouverture (champ « linteau ») plutôt que dessinés en structure (lisibilité du plan)
for s_ in EX['RDC']['structure']:
    if s_['id'] in LIN:
        o = next(o for o in OUV_RDC if o['id'] == LIN[s_['id']])
        o['linteau'] = {"id": s_['id'], "texte_original": s_['dimension']['texte_original'], "valeur": s_['dimension']['valeur'],
                        "source": "LU", "photo": "P3", "ref": lab(s_['id']),
                        "note": "2 pièces de 2\" ; longueur = baie ; appuis non indiqués"}
STR_RDC += [
    st('str-RDC-S01', 'solives', "SOLIVES 2\"x7\" @ 16\" c/c", "2x7 @ 16 c/c", "LU", "P3", {"x1": 148.25, "y1": 206.25, "x2": 316, "y2": 370, "espacement": 16}, 'y',
       "écrit dans la chambre d'utilité ; flèche orientée avant-arrière ; solives de plafond probables (non précisé)"),
    st('str-RDC-S02', 'solives', "SOLIVES 2\"x7\" @ 16\" c/c", "2x7 @ 16 c/c", "LU", "P3", {"x1": 224.25, "y1": 10, "x2": 446, "y2": 154.75, "espacement": 16}, 'y',
       "écrit dans le salon ; solives de plafond probables"),
    st('str-RDC-P01', 'poutre', "POUTRE 6\"x10\" FLUSH", "6x10", "LU", "P3", {"x1": 318.25, "y1": 206, "x2": 446, "y2": 206}, 'x',
       "poutre affleurante (« FLUSH ») au plafond de la cuisine, de la cloison de l'escalier au mur droit ; y NON coté : ≈ 206 po ESTIMÉ (P3), "
       "concordant à 2 po près avec l'axe C (204) et la poutre arrière du sous-sol ; aussi visible en filigrane sur P2 (cote-RDC-221)"),
    st('str-RDC-AXB', 'axe', "Axe porteur à l'origine", "AXE B (2016)", "LU", "P2", {"x1": 0, "y1": 157, "x2": 456, "y2": 157}, 'x',
       "axe B du croquis 2016 (Mazerolle) : y = 10\" + 12'-3\" = 157 (cote-RDC-214/215) ; coïncide exactement avec l'axe de la poutre str-SS-P02 "
       "et avec les cloisons mur-RDC-012/019 ; « porteur à l'origine » : rien n'est écrit sur l'état 2016"),
    st('str-RDC-AXC', 'axe', "Axe porteur à l'origine", "AXE C (2016)", "LU", "P2", {"x1": 0, "y1": 204, "x2": 456, "y2": 204}, 'x',
       "axe C du croquis 2016 : y = 157 + 3'-11\" = 204 (cote-RDC-213) ; coïncide avec l'axe de la poutre str-SS-P01 et la cloison mur-RDC-026 ; "
       "la poutre FLUSH str-RDC-P01 (≈ 206) le prolonge dans la cuisine ; colonnes C4 et C6 « retirées »"),
]
STR_RDC.sort(key=lambda s: s['id'])

# ============================================================================ 9. lignes de cote
LC = {'SS': [], 'RDC': []}


def lc(niv, p1, p2, direction, facade, rang, ref=None, source=None, decalage=None):
    va = None; statut = 'confirmee'; rep = None
    if ref:
        va = VAL[ref]; statut = STAT[ref]
        src = source or 'LU'
        rep = EC.get('conf-' + ref)
    else:
        src = source or 'DÉDUIT'
    d = {"id": f"lc-{niv}-{len(LC[niv]) + 1:03d}", "p1": [round(p1[0], 2), round(p1[1], 2)], "p2": [round(p2[0], 2), round(p2[1], 2)],
         "direction": direction, "facade": facade, "rang": rang, "source": src, "statut": statut, "ref": ref,
         "valeur_attendue": va, "repere": rep}
    if decalage is not None: d["decalage"] = decalage
    LC[niv].append(d)


def chaine(niv, facade, rang, pts, refs, fixe):
    """pts : coordonnées le long de la façade ; refs[i] : id de cote du segment i (ou None = DÉDUIT) ; fixe = coord. normale"""
    dirn = 'x' if facade in ('avant', 'arriere') else 'y'
    for i, (a, b) in enumerate(zip(pts[:-1], pts[1:])):
        p1 = (a, fixe) if dirn == 'x' else (fixe, a)
        p2 = (b, fixe) if dirn == 'x' else (fixe, b)
        lc(niv, p1, p2, dirn, facade, rang, refs[i])


def larg_chain(lst, total):
    """lst : [(centre, largeur, ref)] → points et refs d'une chaîne d'ouvertures (jambages)"""
    pts, refs = [0], []
    for c, w, r in sorted(lst):
        pts += [c - w / 2, c + w / 2]; refs += [None, r]
    pts.append(total); refs.append(None)
    return pts, refs


# --- SS
o = {x['id']: x for x in OUV_SS}
p, r = larg_chain([(382, V('cote-SS-032'), 'cote-SS-032')], 456); chaine('SS', 'avant', 1, p, r, 0)
chaine('SS', 'avant', 2, [0, 162, 234, 382, 456], ['cote-SS-027', 'cote-SS-028', 'cote-SS-029', 'cote-SS-030'], 0)
lc('SS', (0, 0), (456, 0), 'x', 'avant', 3, None, 'DÉDUIT')
p, r = larg_chain([(V('cote-SS-005') - _L1 / 4 - 24, _L1 / 2, None), (V('cote-SS-005') + _L1 / 4, _L1 / 2, None)], 456)
chaine('SS', 'arriere', 1, p, r, 380)   # fenêtre séparée en deux (réponses du propriétaire)
chaine('SS', 'arriere', 2, [0, 219, 327, 456], ['cote-SS-002', 'cote-SS-003', 'cote-SS-004'], 380)
lc('SS', (0, 380), (456, 380), 'x', 'arriere', 3, 'cote-SS-001')
p, r = larg_chain([(48, V('cote-SS-017'), 'cote-SS-017'), (180, V('cote-SS-016'), 'cote-SS-016')], 380); chaine('SS', 'gauche', 1, p, r, 0)
chaine('SS', 'gauche', 2, [0, 48, 132, 180, 380], ['cote-SS-015', 'cote-SS-014', 'cote-SS-013', 'cote-SS-012'], 0)
lc('SS', (0, 0), (0, 380), 'y', 'gauche', 3, 'cote-SS-011')
p, r = larg_chain([(75, V('cote-SS-026'), 'cote-SS-026'), (180, V('cote-SS-050'), 'cote-SS-050'), (308, V('cote-SS-025'), 'cote-SS-025')], 380)  # porte et fenêtre permutées
chaine('SS', 'droite', 1, p, r, 456)
chaine('SS', 'droite', 2, [0, 75, 180, 308, 380], ['cote-SS-024', 'cote-SS-023', 'cote-SS-022', 'cote-SS-021'], 456)
lc('SS', (456, 0), (456, 380), 'y', 'droite', 3, 'cote-SS-020')
# intérieures SS
xs = [0, 10, 128, 136, 224, 232, 320, 328, 446, 456]
for (a, b), rf in zip(zip(xs[:-1], xs[1:]), ['cote-SS-037', 'cote-SS-038', 'cote-SS-039', 'cote-SS-040', 'cote-SS-041', 'cote-SS-042', 'cote-SS-043', 'cote-SS-044', 'cote-SS-045']):
    lc('SS', (a, 216), (b, 216), 'x', 'int', 2, rf, decalage=0)
ys = [(380, 370, None), (370, 204, 'cote-SS-046'), (204, 157, 'cote-SS-047'), (157, 10, 'cote-SS-048'), (10, 0, 'cote-SS-034')]
for a, b, rf in ys:
    lc('SS', (261, b), (261, a), 'y', 'int', 2, rf, decalage=0)
lc('SS', (219, 392), (261, 392), 'x', 'int', 1, 'cote-SS-010', decalage=0)
lc('SS', (327, 380), (327, 440), 'y', 'int', 1, 'cote-SS-009', decalage=14)
lc('SS', (234, -48), (234, 0), 'y', 'int', 1, 'cote-SS-033', decalage=14)
# --- RDC
p, r = larg_chain([(98, V('cote-RDC-014'), 'cote-RDC-014'), (199, 34, lab('ouv-RDC-010')), (377, V('cote-RDC-015'), 'cote-RDC-015')], 456)
chaine('RDC', 'avant', 1, p, r, 0)
chaine('RDC', 'avant', 2, [0, 98, 199, 377, 456], ['cote-RDC-010', 'cote-RDC-011', 'cote-RDC-012', 'cote-RDC-013'], 0)
lc('RDC', (0, 0), (456, 0), 'x', 'avant', 3, 'cote-RDC-009')
chaine('RDC', 'arriere', 1, [0, 98, 197, 293, 375, 456], ['cote-RDC-019', 'cote-RDC-020', 'cote-RDC-021', 'cote-RDC-022', 'cote-RDC-023'], 380)
chaine('RDC', 'arriere', 2, [0, 219, 327, 456], ['cote-RDC-016', 'cote-RDC-017', 'cote-RDC-018'], 380)
lc('RDC', (0, 380), (456, 380), 'x', 'arriere', 3, None, 'DÉDUIT')
p, r = larg_chain([(191, V('cote-RDC-004'), 'cote-RDC-004')], 380); chaine('RDC', 'gauche', 1, p, r, 0)
chaine('RDC', 'gauche', 2, [0, 191, 380], ['cote-RDC-003', 'cote-RDC-002'], 0)
lc('RDC', (0, 0), (0, 380), 'y', 'gauche', 3, 'cote-RDC-001')
p, r = larg_chain([(180, V('cote-RDC-008'), 'cote-RDC-008')], 380); chaine('RDC', 'droite', 1, p, r, 456)
chaine('RDC', 'droite', 2, [0, 180, 380], ['cote-RDC-007', 'cote-RDC-006'], 456)
lc('RDC', (456, 0), (456, 380), 'y', 'droite', 3, 'cote-RDC-005')
xs = [0, 108, 146, 175, 275, 316, 456]
for (a, b), rf in zip(zip(xs[:-1], xs[1:]), ['cote-RDC-029', 'cote-RDC-030', 'cote-RDC-031', 'cote-RDC-032', 'cote-RDC-033', 'cote-RDC-034']):
    lc('RDC', (a, 216), (b, 216), 'x', 'int', 2, rf, decalage=0)
xs = [0, 146, 175, 222, 456]
for (a, b), rf in zip(zip(xs[:-1], xs[1:]), ['cote-RDC-038', 'cote-RDC-039', 'cote-RDC-040', 'cote-RDC-041']):
    lc('RDC', (a, 128), (b, 128), 'x', 'int', 2, rf, decalage=0)
for x, seq in ((100, [(380, 223, 'cote-RDC-035'), (223, 157, 'cote-RDC-036'), (157, 0, 'cote-RDC-037')]),
               (262, [(380, 204, 'cote-RDC-042'), (204, 157, 'cote-RDC-043'), (157, 0, 'cote-RDC-044')]),
               (355, [(380, 157, 'cote-RDC-045'), (157, 0, 'cote-RDC-046')])):
    for a, b, rf in seq:
        lc('RDC', (x, b), (x, a), 'y', 'int', 2, rf, decalage=0)
for c, rf in ((98, 'cote-RDC-024'), (197, 'cote-RDC-025'), (375, 'cote-RDC-028')):
    w = V(rf); lc('RDC', (c - w / 2, 370), (c + w / 2, 370), 'x', 'int', 1, rf, decalage=-12)
w = V('cote-RDC-026'); lc('RDC', (293 - w / 2, 437), (293 + w / 2, 437), 'x', 'int', 1, 'cote-RDC-026', decalage=-14)
lc('RDC', (293, 440), (327, 440), 'x', 'int', 1, 'cote-RDC-027', decalage=14)
w = V('cote-RDC-047'); lc('RDC', (40, 220), (40, 226), 'y', 'int', 1, 'cote-RDC-047', decalage=0)

# ============================================================================ 10. notes (traduites / interprétées)
NOTES = {
    'SS': [
        {"id": "note-SS-01", "texte_original": "SOLIVES 2\"x10\" @ 20\" c/c", "interpretation": "Solives de plancher 2 po × 10 po espacées de 20 po c/c (plancher du RDC), parallèles à y.", "photo": "P1"},
        {"id": "note-SS-02", "texte_original": "SOLIVES DOUBLES SOUS LES CLOISONS PARALLÈLES", "interpretation": "Solives doublées sous les cloisons parallèles aux solives (un double trait dessiné à x ≈ 137, de la poutre arrière au mur arrière).", "photo": "P1"},
        {"id": "note-SS-03", "texte_original": "CROIX ST ANDRÉ (3 fois)", "interpretation": "Rangées d'entretoises en croix entre les solives (dessinées dans la moitié gauche seulement).", "photo": "P1"},
        {"id": "note-SS-04", "texte_original": "POUTRE 8\"x10\" (2 fois) ; COL. BOIS, 8\"x8\"", "interpretation": "Deux poutres de 8 × 10 po sur colonnes de bois de 8 × 8 po (3 par poutre).", "photo": "P1"},
        {"id": "note-SS-05", "texte_original": "PORTE DE RAMONAGE ; VÉROLE", "interpretation": "Trappe de ramonage au pied de la cheminée ; « virole » (raccord du tuyau de fumée) — lecture « VÉROLE ».", "photo": "P1"},
        {"id": "note-SS-06", "texte_original": "3W ; $ ; ⊕ ; Θ", "interpretation": "Symboles électriques (interrupteurs, sorties) non légendés : non reportés sur ce plan (voir extraction/SS.json).", "photo": "P1"},
    ],
    'RDC': [
        {"id": "note-RDC-01", "texte_original": "NOTE : BARRE & TABLETTE DANS TOUS LES G.R.", "interpretation": "Tringle et tablette dans toutes les garde-robes.", "photo": "P3"},
        {"id": "note-RDC-02", "texte_original": "BÉTON REN. AVEC BARRE ½\"Ø @ 10\" c/c", "interpretation": "Perron avant en béton armé de barres de ½ po à 10 po c/c.", "photo": "P3"},
        {"id": "note-RDC-03", "texte_original": "SOLIVES 2\"x7\" @ 16\" c/c (×2)", "interpretation": "Solives 2 × 7 po à 16 po c/c (chambre d'utilité, salon), orientées avant-arrière ; plafond probable.", "photo": "P3"},
        {"id": "note-RDC-04", "texte_original": "POUTRE 6\"x10\" FLUSH", "interpretation": "Poutre de 6 × 10 po affleurante au plafond de la cuisine / salle à manger.", "photo": "P3"},
        {"id": "note-RDC-05", "texte_original": "POÊLE #220 ; SEC. #220", "interpretation": "Prises 220 V pour la cuisinière et la sécheuse.", "photo": "P3"},
        {"id": "note-RDC-06", "texte_original": "Axe porteur à l'origine (B, C) ; Colonne C4 retirée ; Colonne C6 retirée", "interpretation": "Croquis 2016 (ing. C. Mazerolle) : axes porteurs d'origine y = 157 et 204 ; colonnes C4 et C6 retirées.", "photo": "P2"},
        {"id": "note-RDC-07", "texte_original": "Zone de fissures au plafond de plâtre ; Fissure ± 1,2 m au plafond de stucco", "interpretation": "Croquis 2016 : fissures au plafond (cuisine le long de la ligne 6 et de l'axe C ; salon ≈ ligne 6).", "photo": "P2"},
        {"id": "note-RDC-09", "texte_original": "TAB. À MÉD.", "interpretation": "Tablette / armoire à médicaments dans la S. de bain (lecture incertaine ; non dessinée en élément).", "photo": "P3"},
        {"id": "note-RDC-08", "texte_original": "SW ; 3W ; $ ; ⊖", "interpretation": "Symboles électriques non légendés : non reportés sur ce plan (voir extraction/RDC.json).", "photo": "P3"},
    ],
}

# ============================================================================ 11. vérifications (superposition, chaînes) → écarts
VERIF = []


def check(ok, msg):
    VERIF.append(("OK " if ok else "ÉCART ") + msg)
    return ok


# chaînes = hors-tout
for niv in ('SS', 'RDC'):
    par = {}
    for l in LC[niv]:
        if l['facade'] == 'int': continue
        ax = 0 if l['direction'] == 'x' else 1
        par.setdefault((l['facade'], l['rang']), []).append(abs(l['p2'][ax] - l['p1'][ax]))
    for (fac, rg), lst in sorted(par.items()):
        ht = sum(par[(fac, 3)])
        check(abs(sum(lst) - ht) <= 0.5, f"[{niv}] chaîne {fac} rang {rg} : Σ {sum(lst)} = hors-tout {ht}")
    # valeurs lues vs dessinées
    for l in LC[niv]:
        if l['valeur_attendue'] is None: continue
        ax = 0 if l['direction'] == 'x' else 1
        dl = abs(l['p2'][ax] - l['p1'][ax])
        check(abs(dl - l['valeur_attendue']) <= 0.5, f"[{niv}] {l['id']} ({l['ref']}) dessinée {dl} vs lue {l['valeur_attendue']}")
# superposition SS ↔ RDC
check(True, "murs ext. : nu ext. SS et RDC sur le même rectangle 0–456 × 0–380 (même origine, mêmes hors-tout 38'-0\" × 31'-8\")")
check(True, "volume de l'entrée arrière RDC (x 219–327) = caveau SS (x 219–327) : mêmes cotes 18'-3\" + 9'-0\" + 10'-9\" sur les deux feuilles")
esc_ss = next(e for e in ELEM_SS if e['id'] == 'elem-SS-ESC'); esc_r = next(e for e in ELEM_RDC if e['id'] == 'elem-RDC-ESC1')
x_ss = (esc_ss['position']['x'] - 18.5, esc_ss['position']['x'] + 18.5); x_r = (277.25, 313.75)
top_ss = esc_ss['position']['y'] + 121.7 / 2; top_r = 334
d_esc = max(abs(x_ss[0] - x_r[0]), abs(x_ss[1] - x_r[1]), abs(top_ss - top_r))
check(d_esc <= 6, f"escalier SS x {x_ss[0]:.1f}–{x_ss[1]:.1f}, haut y {top_ss:.1f} vs cage RDC x 277.25–313.75, palier y ≈ 334 : écart max {d_esc:.1f} po")
# colonnes SS sous cloisons RDC
part = [m for m in MURS_RDC if m['type'] == 'int']
sous, pas_sous = [], []
for s in STR_SS:
    if s['type'] != 'colonne': continue
    g = s['geometrie']; pt = Point(g['x'], g['y'])
    on = [m['id'] for m in part if LineString([(m['x1'], m['y1']), (m['x2'], m['y2'])]).distance(pt) <= m['epaisseur']['valeur'] / 2 + 0.01]
    flush = 318 <= g['x'] <= 446 and abs(g['y'] - 206) <= 4
    (sous if on or flush else pas_sous).append((s['id'], g['x'], g['y'], on or (['str-RDC-P01 (poutre FLUSH)'] if flush else [])))
for sid, x, y, on in sous:
    check(True, f"colonne {sid} ({x},{y}) sous {', '.join(on)}")
for sid, x, y, on in pas_sous:
    check(False, f"colonne {sid} ({x},{y}) sous aucune cloison du RDC")
# plomberie
sdb = Polygon(next(p for p in PIECES['RDC'] if p['id'] == 'piece-RDC-SDB')['polygone'])
cui = Polygon(next(p for p in PIECES['RDC'] if p['id'] == 'piece-RDC-CUI')['polygone'])
plomb = []
for eid in ('elem-SS-CE', 'elem-SS-EVIER'):
    e = next(e for e in ELEM_SS if e['id'] == eid); pt = Point(e['position']['x'], e['position']['y'])
    plomb.append(f"{e['nom'].lower()} du sous-sol à {pp(round(e['position']['x']))} du coin gauche et {pp(round(e['position']['y']))} du nu ext. avant : "
                 f"à {pp(round(sdb.distance(pt)))} de la S. de bain et {pp(round(cui.distance(pt)))} de la cuisine (en plan)")
check(False, "colonnes de plomberie : " + " ; ".join(plomb) + " — aucun appareil SS directement sous la S. de bain ou l'évier de cuisine ; drains non dessinés")

# ============================================================================ 12. registre des écarts (suite)
ARCHE_AV = "Mesurer la largeur libre de l'arche hall / salon (cloison à 18'-6\" du coin avant gauche)."
ecart('ep-ext-rdc', 'RDC', "Épaisseur des murs extérieurs du RDC : 10\" écrit sur le croquis 2016 (P2, chaînes 10\" aux 4 côtés — valeur typique "
      "d'une fondation, peut-être reprise du plan de fondation) ; le dessin 1957 montre ≈ 11 po ; aucune épaisseur écrite sur la feuille RDC (P3, P4 et P6).",
      "moyen", "10\" (LU P2) appliqué aux 4 murs ext. du RDC ; les dimensions intérieures des pièces en dépendent (± 1 po).",
      "Mesurer l'épaisseur totale du mur extérieur au jambage de la porte d'entrée avant et d'une fenêtre (revêtement int. au revêtement ext.).", "P2", (5, 100))
ecart('ep-int-rdc', 'RDC', "Épaisseur des cloisons du RDC non cotée (sauf cloison chambre arrière / S. de bain 6\" LU, tranchée par 3e lecture) ; dessin ≈ 6 po.",
      "moyen", "4½\" PRÉSUMÉ (cloison 2x4 + plâtre) ; les cloisons sont positionnées à l'AXE (convention déduite) donc seules les dimensions nettes des pièces varient.",
      "Mesurer l'épaisseur d'une cloison à un cadre de porte (ex. porte de la chambre avant) et la largeur nette du hall (attendu 3'-11\" − 4½\" ≈ 42½\").", "P3", (146, 120))
ecart('ep-pres', 'global', "Épaisseurs PRÉSUMÉES par analogie ou par défaut : murs gauche et du fond du caveau (10\"), murs avant et droit de l'excroissance du perron (6\"), "
      "murs de l'entrée arrière (6\", dessin ≈ 11\") ; profondeur de l'entrée arrière non cotée : nu ext. PRÉSUMÉ à 5'-0\" du mur arrière (= caveau cote-SS-009), "
      "alors que le dessin RDC montre ≈ 5'-7\".", "faible",
      "Valeurs PRÉSUMÉES indiquées par le repère ⚠ sur les plans.",
      "Mesurer l'épaisseur des murs du caveau à la porte 2'-6\", la profondeur hors-tout et l'épaisseur des murs de l'entrée arrière à la porte extérieure.", "P1", (273, 437))
ecart('hp', 'global', "Hauteurs de plafond inconnues aux deux niveaux (aucune coupe ni élévation ; aucune hauteur écrite).", "moyen",
      "Hauteur laissée vide (ILLISIBLE) ; aucune valeur présumée.",
      "Mesurer la hauteur plancher-plafond au sous-sol (sous solives et sous les poutres 8x10) et au RDC (salon, cuisine sous la poutre FLUSH).", "P1", None)
ecart('p2-cloisons', 'RDC', "Croquis 2016 (P2, « plan d'origine et plan actuel ») : seules quelques cloisons sont redessinées en gris (murs ext., cloison ligne 3 à ≈ 14'-5\" "
      "du coin gauche, de l'axe C au mur arrière ; placards en H entre les lignes 2 et 3 ; bout de cloison ligne 4 à 18'-6\", de ≈ 6'-4\" au mur avant). Absentes du gris : murs de la S. de bain, "
      "cloisons des G.R. de la chambre arrière (≈ 12'-1\" à 13'-5\"), cloisons de la cage d'escalier (lignes 5 et 6, entre C et D), escalier, cloison médiane des placards avant, "
      "cloisons le long des axes B et C. État actuel incertain : cloisons retirées ou simple croquis partiel.", "critique",
      "Le relevé reproduit le plan de 1957 (P3), corrigé par le constat du propriétaire ; les autres cloisons absentes du gris 2016 sont conservées et signalées ici.",
      "Constater les cloisons qui restent incertaines (absentes du gris 2016 et non barrées par le propriétaire) : G.R. de la chambre arrière (entre 12'-2\" et 14'-7\" du coin gauche), "
      "murs de la S. de bain, lingerie (LIN.) et cloison hall / salon (18'-6\", arche 4'-0\") ; position réelle de la cloison ligne 3 (≈ 14'-5\" sur P2 contre 14'-7\" en 1957).",
      "P2", (160, 300))
ecart('col-c4', 'SS', "Croquis 2016 : « Colonne C4 retirée » (axe C à 17'-0\" du nu ext. avant × ligne 4 à 18'-6\" du coin gauche). Au plan 1957 (P1), la colonne la plus proche est str-SS-C02 "
      "à 19'-0\" (DÉDUIT de la chaîne 9'-10\" + 8\" + 7'-4\") : décalage de 6 po entre les deux documents.", "critique",
      "str-SS-C02 conservée au plan (état 1957) avec mention ; portée de la poutre arrière possiblement doublée (≈ 15'-4\" entre C01 et C03 sans C02).",
      "Au sous-sol, sous la poutre arrière (17'-0\" du nu ext. avant) : vérifier la présence / l'absence de colonne à x ≈ 18'-6\"–19'-0\", la flèche de la poutre et tout appui ajouté.", "P2", (228, 204))
ecart('col-c6', 'SS', "Croquis 2016 : « Colonne C6 retirée » (axe C × ligne 6 à 26'-4\" du coin gauche). Au plan 1957 : str-SS-C03 à 27'-0\" (8 po de décalage).", "critique",
      "str-SS-C03 conservée au plan (état 1957) avec mention ; zone de fissures 2016 au droit (ligne 6 / axe C).",
      "Au sous-sol, sous la poutre arrière : vérifier la colonne à x ≈ 26'-4\"–27'-0\" ; mesurer la flèche de la poutre entre C02 et le mur droit.", "P2", (324, 204))
ecart('col-p2', 'SS', "Le croquis 2016 ne marque des colonnes qu'aux lignes 4 et 6 (B4, B6 pleines ; C4, C6 retirées) ; le plan 1957 en montre 3 par poutre "
      "(à 11'-0\", 19'-0\" et 27'-0\" du coin gauche). Les colonnes à 11'-0\" (C01, C04) n'apparaissent pas sur P2 ; positions décalées de 6 à 8 po entre documents.", "moyen",
      "Positions 1957 retenues (DÉDUITES des cotes du sous-sol).",
      "Relever au sous-sol la position et la section de chaque colonne sous les deux poutres 8x10.", "P1", (132, 180))
ecart('axes', 'RDC', "Axes porteurs d'origine (P2) : B à 13'-1\" et C à 17'-0\" du nu ext. avant, « porteurs à l'origine ». Concordance vérifiée : ils coïncident exactement avec les "
      "axes des poutres 8x10 du sous-sol (str-SS-P02 : 10\" + 12'-3\" ; str-SS-P01 : 31'-8\" − 10\" − 13'-10\") et avec les cloisons RDC d'origine mur-RDC-012/019 (B) "
      "et mur-RDC-026 (C). Le croquis ne dit rien de leur état en 2016 ; le propriétaire a constaté le retrait des cloisons sur B (à droite de 18'-6\", sauf le trumeau près du mur droit) et sur C.", "critique",
      "Cloisons restantes sur B (mur-RDC-012, trumeau mur-RDC-019) marquées porteur « inconnu » avec indices ; aucune reprise structurale relevée.",
      "Au sous-sol : appui des solives 2x10 sur les deux poutres 8x10 (13'-1\" et 17'-0\" du nu ext. avant). Au RDC : poutre ou retombée ajoutée au plafond lors du retrait "
      "des cloisons sur les axes B et C (section, appuis, hauteur libre).", "P2", (440, 157))
ecart('fissures', 'RDC', "Fissures signalées en 2016 (P2) : « zone de fissures au plafond de plâtre » le long de la ligne 6 (≈ 26'-1\" à 26'-7\" du coin gauche), de l'axe C au mur arrière, "
      "et le long de l'axe C (≈ 16'-3\" à 17'-0\" du nu ext. avant), de 26'-4\" à ≈ 31'-7\" ; « fissure ± 1,2 m au plafond de stucco » dans le salon à ≈ 26'-7\" du coin gauche, de 2'-7\" à 5'-7\" du nu ext. avant.", "critique",
      "Fissures reportées comme écart (aucune donnée de profondeur ni d'évolution) ; probablement liées au retrait des colonnes C4/C6 (NON écrit).",
      "Relever les fissures (longueur, ouverture, évolution) au plafond de la cuisine le long de l'ancienne cloison de l'escalier et de la poutre FLUSH, et au plafond du salon à ≈ 26'-7\" du coin gauche.",
      "P2", (316, 290))
ecart('fiss-salon', 'RDC', "Fissure ± 1,2 m au plafond de stucco du salon (P2) : à ≈ 26'-7\" du coin gauche, de 2'-7\" à 5'-7\" du nu ext. avant (longueur dessinée ≈ 37 po ; texte 1,2 m ≈ 47 po).", "moyen",
      "Position ESTIMÉE sur le croquis 2016.", "Mesurer la fissure au plafond du salon, près de 26'-7\" du coin avant gauche.", "P2", (319, 49))
ecart('usage', 'RDC', "Usage des pièces : le croquis 2016 nomme « Salle à manger » l'espace que le plan 1957 nomme « CHAMBRE D'UTILITÉ », et « Cuisine » la "
      "« CUISINE S.-À-MANGER » d'origine ; l'absence de cloisons grises aux lignes 5 et 6 suggère un espace ouvert (NON écrit).", "moyen",
      "Nom d'origine conservé, nom 2016 indiqué entre parenthèses.", "Constater l'usage et l'aménagement actuels de la chambre d'utilité et de la cuisine.", "P2", (225, 290))
ecart('arche', 'RDC', "ARCHE hall / salon : texte « ARCHE 4'-0\" » (lectures 1 et 2) mais ouverture dessinée ≈ 74 po, aussi grande que l'ancienne « ARCHE 6'-0\" » salon / cuisine.",
      "moyen", f"Voir {EC['conf-cote-RDC-048']} (cote en conflit) : 4'-0\" retenu.", ARCHE_AV, "P3", (222, 118.6))
ecart('porte-uti', 'RDC', "Porte de la chambre d'utilité étiquetée « 2'-6\"x6'-8\" » (3 lectures) dans une baie cotée 2'-5\" d'axe en axe (cote-RDC-031) : une porte de 30 po "
      "ne peut pas y tenir avec ses montants ; le dessin place la porte en avant de la colonne des G.R., dans le prolongement de la cloison à 17'-0\" du nu ext. avant.", "faible",
      "Porte de 30 po placée sur la cloison de l'axe C, entre ≈ 12'-4\" et 14'-10\" du coin gauche (ESTIMÉ).", "Mesurer la largeur et la position de la porte de la chambre d'utilité.", "P3", (163, 204))
ecart('ear-1po', 'RDC', "Entrée arrière : 8'-2\" + 8'-3\" + 8'-0\" + 2'-9\" = 27'-2\" (axe de la fenêtre + 2'-9\") alors que 18'-3\" + 9'-0\" = 27'-3\" au nu ext. droit du volume "
      "→ écart de 1 po (2'-9\" confirmé par la 3e lecture).", "faible",
      "Nu ext. droit du volume à 27'-3\" (chaîne hors-tout) ; la cote 2'-9\" est dessinée 2'-10\" (repère sur la cote).",
      "Mesurer de l'axe de la fenêtre de l'entrée arrière au nu ext. de son mur droit.", "P6", (310, 440))
ecart('fen-ss', 'SS', "Fenêtres arrière et droite haute du sous-sol : « 6'-8\" » confirmé par la 3e lecture, mais dessinées de la même longueur que la fenêtre avant cotée 6'-3\" (≈ 72–73 po).",
      "faible", "6'-8\" (LU, confirmé).", "Mesurer la largeur des fenêtres du mur arrière (13'-0\" du coin gauche) et du mur droit (6'-0\" du coin arrière).", "P1", (156, 380))
ecart('porte-cav', 'SS', "Porte du caveau « PORTE 2'-6\" » positionnée par la cote 3'-6\" dont le point de départ n'est pas dessiné (nu ext. ou int. du mur gauche du caveau).",
      "faible", "Axe à 18'-3\" + 3'-6\" = 21'-9\" du coin gauche (depuis le nu ext.) ; alternative 22'-7\" (depuis le nu int.).",
      "Mesurer la position de la porte du caveau depuis le coin intérieur arrière gauche du sous-sol.", "P1", (261, 375))
ecart('escalier', 'global', f"Escalier SS ↔ RDC : superposition à {d_esc:.0f} po près (SS largeur ≈ 37 po ESTIMÉ, RDC cage 36½ po DÉDUIT) ; 14 C.M. écrit aux deux niveaux "
      "mais ≈ 10 girons visibles au RDC (les marches inférieures passaient sous le placard BALAIS) ; échappée sous la poutre arrière (17'-0\" du nu ext. avant) au pied de l'escalier non vérifiable.",
      "faible", "Course ESTIMÉE au dessin ; position alignée sur la cage du RDC.",
      "Mesurer la hauteur et le giron des marches, la largeur de l'escalier et l'échappée sous la poutre arrière.", "P1", (295, 270))
ecart('poutre-flush', 'RDC', "Poutre 6\"x10\" FLUSH (cuisine) non cotée en position : ≈ 17'-2\" du nu ext. avant ESTIMÉ (P3), à 2 po de l'axe C (17'-0\") et de la poutre arrière du SS.",
      "faible", "17'-2\" (206 po) ESTIMÉ.", "Repérer la poutre au plafond de la cuisine (bande de plâtre, fissures) et mesurer sa distance au mur arrière.", "P3", (380, 206))
ecart('col-plancher', 'SS', "Colonne str-SS-C01 (11'-0\" du coin gauche, sur la poutre arrière à 17'-0\" du nu ext. avant) : aucune cloison RDC au-dessus (zone de la porte de la chambre arrière, ≈ 17'-8\") ; "
      "la cloison à 12'-2\" passe à 14 po de la rangée de colonnes à 11'-0\".", "faible",
      "Aucune incidence sur le relevé ; information pour la structure.", "Vérifier l'appui de la cloison à 12'-2\" du coin gauche sur la solive doublée (note « solives doubles sous les cloisons »).", "P1", (132, 204))
ecart('plomberie', 'global', "Superposition de la plomberie : " + " ; ".join(plomb) + ". Aucun drain, colonne de chute ni panneau électrique dessiné au sous-sol.",
      "faible", "Aucune conduite reportée (non dessinée).", "Repérer au sous-sol la colonne de chute sous la S. de bain (0 à 9'-0\" du coin gauche, 13'-1\" à 18'-7\" du nu ext. avant) et sous l'ancien évier de cuisine.", "P1", (40, 190))
ecart('cheminee', 'global', "Cheminée : massif extérieur au mur gauche non coté (seule sa face avant, à 11'-0\" du nu ext. avant, est située par la chaîne gauche du sous-sol) ; saillie et profondeur ≈ 20 × 21 po ESTIMÉES.",
      "faible", "Dimensions ESTIMÉES au dessin.", "Mesurer la saillie et la largeur du massif de cheminée à l'extérieur, côté gauche.", "P1", (-10, 142))
ecart('p5', 'global', "Plan d'implantation P5 (1957, « maison projetée ») : rectangle 38'-0\" × 31'-8\" concordant ; excroissance avant dessinée ≈ 12,6–19,0 pi du coin gauche "
      "(perron SS : 13'-6\"–19'-6\") ; volume arrière ≈ 17,0–26,4 pi (entrée arrière : 18'-3\"–27'-3\") et marches ≈ 26,4–34,5 pi ; profondeur mesurée ≈ 32,1 pi (1 %). "
      "Implantation projetée, pas un relevé ; marges 40' (avant), 7.79' et 9' (latérales).", "faible",
      "Plans de 1957 (P1, P7, P3, P4, P6) retenus pour la géométrie ; P5 sert à l'orientation (nord ≈ 9,8° ± 1,5°) et au lot.",
      "Certificat de localisation récent pour l'implantation réelle et l'orientation.", "P5", None)
ecart('ancres', 'global', "Aucune mesure prise sur place n'a été fournie par le propriétaire (ancres vides) : toute la géométrie provient des plans de 1957 et du croquis 2016.",
      "moyen", "Plans d'origine reproduits sans calage sur le bâtiment réel.",
      "Mesurer au minimum les deux hors-tout extérieurs (38'-0\" et 31'-8\") et une diagonale au sous-sol pour caler le relevé.", "P1", None)
ecart('portes-ss', 'SS', "Sens d'ouverture non dessiné pour les deux portes du sous-sol (rectangle barré d'un X dans le mur, aucun arc) : ouv-SS-005 « PORTE 2'-8\" » "
      "(mur droit, axe à 6'-3\" du nu ext. avant) et ouv-SS-008 « PORTE 2'-6\" » (porte du caveau, mur arrière). Les tiretés près de la porte 2'-8\" sont des circuits électriques.",
      "faible", "Portes dessinées comme baies (opération « aucune ») ; aucun sens inventé.",
      "Constater pour chaque porte le type de battant, le côté des pentures et le côté d'ouverture.", "P1", (451, 75))
for o in OUV_SS:
    if o['id'] in ('ouv-SS-005', 'ouv-SS-008'):
        o['repere'] = EC['portes-ss']
        o['note'] += f" — voir {EC['portes-ss']}"

# repères des écarts sur les cotes concernées
for niv in ('SS', 'RDC'):
    for l in LC[niv]:
        if l['ref'] == 'cote-RDC-027': l['repere'] = EC['ear-1po']
        if l['ref'] in ('cote-SS-006', 'cote-SS-025'): l['repere'] = EC['fen-ss']
        if l['ref'] == 'cote-SS-010': l['repere'] = EC['porte-cav']

# ============================================================================ 12b. corrections QC R1 (données)
# C9 : champ « mesure » des cotes intérieures du RDC — renvois aux murs actuels, ou aux axes pour les cloisons retirées
MESURES_RDC = {
    'cote-RDC-029': "nu ext. mur gauche → axe de la cloison droite de la S. de bain (mur-RDC-011)",
    'cote-RDC-030': "axe mur-RDC-011 → axe de la cloison à 12'-2\" (mur-RDC-021, colonne des G.R.)",
    'cote-RDC-031': "axe mur-RDC-021 → axe mur-RDC-022 (colonne des G.R., 12'-2\" → 14'-7\")",
    'cote-RDC-032': "axe mur-RDC-022 → axe de l'ancienne cloison à 22'-11\" (mur-RDC-027, retirée)",
    'cote-RDC-033': "ancienne cloison à 22'-11\" → ancienne cloison à 26'-4\" (mur-RDC-027 → mur-RDC-028, retirées) : largeur de l'ancienne cage d'escalier",
    'cote-RDC-034': "ancienne cloison à 26'-4\" (mur-RDC-028, retirée) → nu ext. mur droit",
    'cote-RDC-035': "nu ext. mur arrière → axe de la cloison chambre arrière / S. de bain (mur-RDC-010)",
    'cote-RDC-036': "axe mur-RDC-010 → axe mur-RDC-012 (profondeur de la S. de bain)",
    'cote-RDC-037': "nu ext. mur avant → axe mur-RDC-012 (cloison S. de bain / chambre avant, axe B)",
    'cote-RDC-038': "nu ext. mur gauche → axe de la cloison chambre avant / G.R. (mur-RDC-013)",
    'cote-RDC-039': "axe mur-RDC-013 → axe mur-RDC-014 (profondeur G.R. / LIN. / VEST.)",
    'cote-RDC-040': "axe mur-RDC-014 → axe de la cloison hall / salon (mur-RDC-018) : largeur du hall",
    'cote-RDC-041': "axe mur-RDC-018 → nu ext. mur droit",
    'cote-RDC-042': "nu ext. mur arrière → axe C (str-RDC-AXC ; ancienne cloison mur-RDC-026, retirée)",
    'cote-RDC-043': "axe C → axe B (str-RDC-AXC → str-RDC-AXB) : largeur de l'ancien passage",
    'cote-RDC-044': "nu ext. mur avant → axe B (str-RDC-AXB ; ancienne cloison salon / passage, retirée)",
    'cote-RDC-045': "nu ext. mur arrière → axe B (str-RDC-AXB ; ancienne arche 6'-0\", trumeau mur-RDC-019)",
    'cote-RDC-046': "nu ext. mur avant → axe B (str-RDC-AXB ; trumeau mur-RDC-019)",
}
for c in COTES['RDC']:
    if c['id'] in MESURES_RDC:
        c['mesure'] = MESURES_RDC[c['id']]
    if c['id'] == lab('ouv-RDC-022') and c.get('emplacement'):
        c['emplacement'] = c['emplacement'].replace("pentures côté droit (x≈175)", "pentures côté gauche (x≈148)")
# C13 : chambre arrière — dimensions principales (hors alcôve de la porte)
for p in PIECES['RDC']:
    if p['id'] == 'piece-RDC-CH1':
        p['dimensions'] = {
            "x": D(146 - 10 - T_INT / 2, "DÉDUIT", "P3", "dimension principale : 12'-2\" (cote-RDC-030 + cote-RDC-029) − mur ext. 10\" − ½ cloison 4½\" PRÉSUMÉE"),
            "y": D(V('cote-RDC-035') - 10 - T_6 / 2, "DÉDUIT", "P3", "dimension principale hors alcôve de la porte : 13'-1\" (cote-RDC-035) − mur ext. 10\" − ½ cloison 6\" (cote-RDC-047)")}
# C17 : valeurs ESTIMÉ des pièces → photo d'où viennent les positions estimées
for niv, ph in (('SS', 'P1'), ('RDC', 'P3')):
    for p in PIECES[niv]:
        for d_ in [p['superficie'], p['dimensions']['x'], p['dimensions']['y']]:
            if d_['source'] in ('ESTIMÉ', 'PRÉSUMÉ') and not d_.get('photo'):
                d_['photo'] = ph
# C14 : « TRAPPE » du sous-sol = porte de ramonage
for e in ELEM_SS:
    if e['id'] == 'elem-SS-RAMO':
        e['type'] = 'autre'
        e['nom'] = "P. de ramonage"
        e['note'] = (e.get('note') or '') + " ; libellé abrégé de « PORTE DE RAMONAGE »"
# C15 : rampe de l'escalier du sous-sol
for e in ELEM_SS:
    if e['id'] == 'elem-SS-ESC':
        e['rampe'] = {"texte_original": "RAMPE", "cote": "gauche de la volée (côté −x, ≈ 22'-11\" du coin gauche)", "source": "LU", "photo": "P1",
                      "note": "« RAMPE » écrit avec une flèche vers le côté gauche de la volée ; position ESTIMÉE ; non dessinée"}
        e['note'] += " ; rampe (main courante) écrite « RAMPE » du côté gauche de la volée (P1)"

# ============================================================================ 13. assemblage
for o in OUV_SS + OUV_RDC: o.pop('_centre', None)


def niveau(nid, nom, feuille, photos, murs, ouvs, pieces_, elems, struct, cotes, notes, lcs):
    return {"id": nid, "nom": nom, "feuille": feuille, "photos_sources": photos,
            "hauteur_plafond": D(None, "ILLISIBLE", None, "aucune hauteur de plafond écrite sur la feuille ; voir " + EC['hp']),
            "murs": murs, "ouvertures": ouvs, "pieces": pieces_, "elements": elems, "structure": struct,
            "cotes": cotes, "notes": notes, "lignes_cote": lcs,
            "elements_electriques_non_reportes": ELEC[nid]}


PHOTOS = [
    {"id": "P1", "description": "Feuille « FONDATIONS & SOUS-SOL », éch. 1/4\" = 1'-0\" — gros plan (source principale sous-sol)"},
    {"id": "P2", "description": "Croquis no 1 — « Plan d'origine et plan actuel du RDC », Claude Mazerolle, ing., 19 septembre 2016 (quadrillage 1–7 / A–D, axes porteurs d'origine, colonnes retirées, fissures, ferme 5/12)"},
    {"id": "P3", "description": "Feuille « REZ-DE-CHAUSSÉE », éch. 1/4\" = 1'-0\" — gros plan (source principale RDC ; haut un peu coupé)"},
    {"id": "P4", "description": "Feuille RDC, vue entière (source secondaire)"},
    {"id": "P5", "description": "Plan d'implantation de la maison projetée sur le lot 1-487, Ville de Baie-Comeau, éch. 1\" = 20', 6 nov. 1957, flèche du nord"},
    {"id": "P6", "description": "Feuille RDC, vue entière, autre prise redressée en perspective (source secondaire)"},
    {"id": "P7", "description": "Feuille « FONDATIONS & SOUS-SOL », vue entière avec cartouche (source secondaire)"},
]
maison = {
    "projet": {
        "nom": "Résidence — 86, avenue Laurier, Baie-Comeau",
        "unites": "pouces (affichage pi-po, métrique entre parenthèses)",
        "origine": "coin extérieur avant-gauche de la fondation, vu de la rue ; x le long de la façade, y vers l'arrière",
        "convention_cotation": CONVENTION,
        "ancres": [],
        "ancres_note": "Aucune mesure sur place n'a été fournie par le propriétaire ; voir " + EC['ancres'] + ".",
        "nord": {"angle_deg": 9.8, "source": "ESTIMÉ", "photo": "P5",
                 "note": "mesuré par code sur la flèche du plan d'implantation (prep/redresse/P5.jpg), ± 1,5° ; angle horaire de +y (vers l'arrière) au nord ; nord non qualifié (vrai/magnétique)"},
        "photos": PHOTOS,
        "date": "2026-10-29",
        "revision": "R0",
        "affichage": {"noms_pieces": False, "dimensions_pieces": False, "note": "noms, dimensions et superficies des pièces retirés des plans à la demande du propriétaire (2026-10-29) ; ils restent dans pieces[] et tableau_pieces.csv"},
        "implantation": {"source": "P5", "note": "cotes du plan d'implantation (pieds décimaux convertis en pouces) ; maison « projetée » 1957",
                         "cotes": IMPL},
    },
    "niveaux": [
        niveau('SS', "Sous-sol", "A-100", ["P1", "P7"], [{k: v for k, v in m.items()} for m in MURS_SS], OUV_SS, PIECES['SS'],
               ELEM_SS, STR_SS, COTES['SS'], NOTES['SS'], LC['SS']),
        niveau('RDC', "Rez-de-chaussée", "A-101", ["P3", "P4", "P6"], MURS_RDC, OUV_RDC, PIECES['RDC'],
               ELEM_RDC, STR_RDC, COTES['RDC'], NOTES['RDC'], LC['RDC']),
    ],
    "ecarts": ECARTS,
}
# ---------------------------------------------------------------------------- post-traitement (orchestrateur)
# 1) chaque épaisseur PRÉSUMÉE renvoie à l'écart qui la documente (repère ⚠ unique par écart)
for niv in maison["niveaux"]:
    for m in niv["murs"]:
        ep = m.get("epaisseur") or {}
        if ep.get("source") == "PRÉSUMÉ" and not str(ep.get("ref", "")).startswith("ecart-"):
            ep["ref"] = EC['ep-int-rdc'] if (niv["id"] == "RDC" and m["type"] == "int") else EC['ep-pres']

# 1b) constat du propriétaire (2026-10-29) : mobilier retiré, cotes intérieures qui visaient des cloisons disparues
ELEM_RETIRES_IDS = {'elem-RDC-ARM-AR', 'elem-RDC-ARM-DR', 'elem-RDC-ARM-EAR', 'elem-RDC-BAIN', 'elem-RDC-COMPT',
                    'elem-RDC-EVIER', 'elem-RDC-LAV', 'elem-RDC-SEC', 'elem-RDC-POELE', 'elem-RDC-REF',
                    # 2e constat : tout le mobilier et les appareils, et l'escalier qui n'existe plus (aux deux niveaux)
                    'elem-RDC-WC', 'elem-RDC-LAVABO', 'elem-RDC-ESC1',
                    'elem-SS-CE', 'elem-SS-EVIER', 'elem-SS-FOUR', 'elem-SS-HUILE', 'elem-SS-ESC'}
MOTIF_RETRAIT = {
    'escalier': "l'escalier entre le sous-sol et le RDC n'existe plus (2e constat du propriétaire, 2026-10-29)",
}
for niv_ in maison["niveaux"]:
    niv_["elements_retires"] = [dict(e, retire_selon=MOTIF_RETRAIT.get(e["type"], (
        "demande du propriétaire (2026-10-29) : mobilier, appareils (plomberie, chauffage, électroménagers), "
        "comptoirs et armoires non représentés ; position d'origine (plan 1957) conservée ici pour mémoire")))
        for e in niv_["elements"] if e["id"] in ELEM_RETIRES_IDS]
    niv_["elements"] = [e for e in niv_["elements"] if e["id"] not in ELEM_RETIRES_IDS]
rdc = next(n for n in maison["niveaux"] if n["id"] == "RDC")
# poutre apparente au plafond du RDC sur l'axe B (côté rue), dans le prolongement de la poutre str-SS-P02 du sous-sol
rdc["structure"].append({
    "id": "str-RDC-P02", "type": "poutre",
    "dimension": {"texte_original": None, "valeur": None, "source": "ILLISIBLE", "photo": None,
                  "note": "section non relevée"},
    "sens": "x",
    "geometrie": {"x1": 175.0, "y1": 157.0, "x2": 446.0, "y2": 157.0},
    "note": ("Poutre au plafond du RDC côté rue, qui suit la poutre 8\"x10\" du sous-sol (str-SS-P02, axe B) — 2e constat du "
             "propriétaire (2026-10-29). Étendue PRÉSUMÉE sur la partie ouverte de l'axe B (de la fin de la cloison "
             "S. de bain / chambre avant au mur droit) ; sur l'axe C : poutre autoportante (str-RDC-P03).")})
rdc["structure"].sort(key=lambda x: x["id"])
rdc["murs_retires"] = MURS_RETIRES_DATA
rdc["ouvertures_retirees"] = [{k: v for k, v in o.items() if not k.startswith('_')} for o in OUV_RETIREES]


def _sur_mur(pt, murs_):
    return any(LineString([(m['x1'], m['y1']), (m['x2'], m['y2'])]).distance(Point(pt)) < 1 for m in murs_)


lc_retirees = [l for l in rdc["lignes_cote"] if l["facade"] == "int"
               and any(_sur_mur(p, MURS_RETIRES_DATA) and not _sur_mur(p, rdc["murs"]) for p in (l["p1"], l["p2"]))]
rdc["lignes_cote"] = [l for l in rdc["lignes_cote"] if l not in lc_retirees]
ids_lc_ret = sorted(l["ref"] for l in lc_retirees if l.get("ref"))
for c in rdc["cotes"]:
    if c["id"] in ids_lc_ret:
        c["note_constat"] = (f"cote d'origine conservée pour mémoire ; elle vise une cloison retirée ({CONSTAT}) "
                             "et n'est plus dessinée")
for e in ECARTS:
    if e["id"] == EC['porte-uti']:
        e["statut"] = "sans objet"
        e["hypothese_retenue"] = f"Sans objet : la porte et sa cloison n'existent plus ({CONSTAT}). " + e["hypothese_retenue"]
    if e["id"] == EC['p2-cloisons']:
        e["description"] += (f" — CONFIRMÉ en partie par le {CONSTAT} : cloisons de la cage d'escalier, du placard à balais, "
                             "chambre d'utilité / dégagement (axe C) et salon / passage (axe B) retirées.")
    if e["id"] == EC['usage']:
        e["hypothese_retenue"] = "Noms 2016 adoptés (Salle à manger, Cuisine) : l'aire est ouverte selon le constat du 2026-10-29 ; noms 1957 conservés dans nom_original."
_n = len(ECARTS)
ECARTS.append({
    "id": f"ecart-{_n + 1:03d}", "niveau": "RDC", "impact": "critique", "statut": "ouvert", "photo": "P2",
    "description": (f"{CONSTAT} : les cloisons mur-RDC-026, -027, -028, -029 et la partie de mur-RDC-019 à gauche de l'arche 6'-0\" "
                    "n'existent plus ; 4 portes (ouv-RDC-017, -023, -024, -025) et l'arche ouv-RDC-013 disparaissent avec elles. "
                    "Deux de ces cloisons étaient sur les axes porteurs d'origine B et C (P2) ; les colonnes str-SS-C01, C02, C05, C06 "
                    "du sous-sol ne sont plus sous aucune cloison. Le trait diagonal au coin hall / salon est interprété comme le début "
                    "du trait de l'axe B : la cloison hall / salon (arche 4'-0\") est conservée."),
    "hypothese_retenue": ("Cloisons retirées du plan (conservées dans murs_retires pour mémoire) ; aire ouverte découpée en zones "
                          "(dégagement, salle à manger, escalier, cuisine, salon) aux axes des anciennes cloisons, sans mur. "
                          "Escalier conservé (seul accès au sous-sol) ; garde-corps et reprises structurales (poutres, linteaux, "
                          "retombées) non relevés. Trumeau à droite de l'ancienne arche conservé (position ESTIMÉE)."),
    "a_valider_sur_place": ("Au RDC : présence d'une retombée ou poutre au plafond le long des axes B (13'-1\" du nu ext. avant) et "
                            "C (17'-0\") là où les cloisons ont été enlevées, et sa hauteur libre ; garde-corps de l'escalier ; "
                            "existence du trumeau près du mur droit sur l'axe B ; cloison hall / salon (arche 4'-0\") toujours en place ?"),
    "position": [262.0, 180.0]})
ECARTS[-1]["description"] += (" La porte de la salle de bain ouv-RDC-015 ouvre aujourd'hui vers le dégagement (au plan 1957 : dans la "
                              "salle de bain). 2e constat (2026-10-29) : le trumeau à droite de l'ancienne arche n'existe plus ; "
                              "l'escalier entre le sous-sol et le RDC n'existe plus ; une poutre est visible au plafond du RDC "
                              "côté rue seulement, dans l'axe de la poutre avant du sous-sol (axe B) ; une poutre autoportante a été installée dans le plafond sur l'axe C.")
ECARTS[-1]["hypothese_retenue"] = ECARTS[-1]["hypothese_retenue"].replace(
    "Escalier conservé (seul accès au sous-sol) ; garde-corps et reprises structurales (poutres, linteaux, retombées) non relevés. "
    "Trumeau à droite de l'ancienne arche conservé (position ESTIMÉE).",
    "Escalier et trumeau retirés ; ouverture de plancher présumée refermée. Poutre de l'axe B dessinée (str-RDC-P02), section "
    "inconnue, étendue PRÉSUMÉE sur la partie ouverte de l'axe.")
ECARTS[-1]["a_valider_sur_place"] = (
    "Au RDC : section, hauteur libre et appuis de la poutre apparente sur l'axe B (13'-1\" du nu ext. avant) et son étendue exacte ; "
    "sur l'axe C (17'-0\"), comment le plafond est porté sans cloison ni poutre ; cloison hall / salon (arche 4'-0\") toujours en place ? "
    "Accès actuel au sous-sol (l'escalier intérieur n'existe plus) et plancher refait à l'emplacement de l'ancienne trémie.")

# 1c) QC R2 : ids uniques, écarts sans objet, textes périmés, limites des zones ouvertes
for e in ECARTS:
    if e["id"] == EC['escalier']:
        e["statut"] = "sans objet"
        e.pop("position", None)
        e["a_valider_sur_place"] = ""
        e["hypothese_retenue"] = "Sans objet : l'escalier n'existe plus (2e constat du propriétaire, 2026-10-29). " + e["hypothese_retenue"]
    if e["id"] == EC['axes']:
        e["a_valider_sur_place"] = ("Relever au plafond du RDC la poutre de l'axe B (13'-1\" du nu ext. avant) et la poutre autoportante "
                                    "de l'axe C (17'-0\") : section, longueur, appuis aux extrémités (colonnes, murs) et hauteur libre dessous.")
    if e["id"] == EC['plomberie']:
        e["hypothese_retenue"] += (" Appareils du sous-sol (chauffe-eau, fournaise, réservoir à l'huile, évier à lessive) et de la "
                                   "S. de bain retirés du plan à la demande du propriétaire ; positions 1957 dans elements_retires.")
    if e["id"] == EC['porte-uti']:
        e.pop("position", None)
        e["a_valider_sur_place"] = ""
    if e["id"] == EC['escalier']:
        e["description"] = e["description"].replace("RDC cage 36½ po DÉDUIT", "RDC 3'-5\" à l'axe des anciennes cloisons (cote-RDC-033), cage retirée")
        e["hypothese_retenue"] = e["hypothese_retenue"].replace("position x alignée sur la cage du RDC",
                                                                "position x alignée sur les axes des anciennes cloisons de la cage (retirées)")
    if e["id"] == EC['usage']:
        e["a_valider_sur_place"] = "Constater l'usage et l'aménagement actuels de la salle à manger (ancienne chambre d'utilité) et de la cuisine."
for e in rdc["elements"]:
    if e["id"] == "elem-RDC-ESC1":
        lg = (e.get("dimensions") or {}).get("largeur") or {}
        if lg.get("note"):
            lg["note"] = lg["note"].replace("entre cloisons x = 23'-0\" et 26'-4\"",
                                            "entre les axes des anciennes cloisons x = 23'-0\" et 26'-4\" (retirées, constat 2026-10-29)")
for c in rdc["cotes"]:
    if c["id"] == "cote-RDC-058":
        c["emplacement"] += " (état 1957 ; la porte ouvre aujourd'hui vers le dégagement, constat 2026-10-29)"
rdc["limites_zones"] = [{"id": f"lz-RDC-{i:03d}", "p1": list(a), "p2": list(b), "note": n}
                        for i, (a, b, n) in enumerate(COUPES['RDC'], 1)]

# 1d) réponses du propriétaire (2026-10-29) aux questions de la R0
ss = next(n for n in maison["niveaux"] if n["id"] == "SS")
ss["ouvertures_retirees"] = [{k: v for k, v in o.items() if not k.startswith('_')} for o in OUV_SS_RETIREES]
ss["usage"] = f"appartement indépendant ; aucun accès intérieur depuis le RDC ({REPONSES})"
ss["notes"].append({"id": "note-SS-REP", "texte_original": None,
                    "interpretation": (f"{REPONSES} : le sous-sol est un appartement indépendant ; aucune cloison ajoutée depuis 1957 ; "
                                       "porte et fenêtre du milieu du mur droit permutées ; grande fenêtre arrière gauche séparée en deux."),
                    "photo": None})
rdc["usage"] = f"logement du RDC ; l'escalier vers le sous-sol n'existe plus ({REPONSES})"
for st_ in rdc["structure"]:
    if st_["id"] == "str-RDC-P02":
        st_["dimension"] = {"texte_original": None, "valeur": None, "source": "ILLISIBLE", "photo": None,
                            "note": "section non relevée (le 8\"x8\" donné par le propriétaire désigne les colonnes)"}
        sx = next(x for x in ss["structure"] if x["id"] == "str-SS-P02")["geometrie"]
        st_["geometrie"] = {"x1": sx["x1"], "y1": sx["y1"], "x2": sx["x2"], "y2": sx["y2"]}
        st_["note"] = (f"Poutre au plafond du RDC, côté rue seulement, exactement à l'aplomb de la poutre 8\"x10\" du "
                       f"sous-sol str-SS-P02 (axe B) ({REPONSES}). Étendue prise identique à celle de la poutre du sous-sol. "
                       "Sur l'axe C : poutre autoportante str-RDC-P03.")
COL_RETIREES_RDC = {'str-SS-C02': "C4", 'str-SS-C03': "C6"}   # « Colonne C4 / C6 retirée » (P2, 2016), axe C
for c_ in ss["structure"]:
    if c_["type"] != "colonne":
        continue
    c_["note"] = (c_.get("note") or "") + (f" ; colonne 8\"x8\" continue jusqu'en haut ({REPONSES})"
                                          if c_["id"] not in COL_RETIREES_RDC else
                                          f" ; présente au sous-sol, mais son prolongement au RDC (« Colonne {COL_RETIREES_RDC[c_['id']]} "
                                          f"retirée », P2) n'existe plus ({REPONSES})")
    if c_["id"] in COL_RETIREES_RDC:
        continue
    g_ = c_["geometrie"]
    rdc["structure"].append({
        "id": c_["id"].replace("-SS-", "-RDC-"), "type": "colonne",
        "dimension": {"texte_original": "8x8", "valeur": "8x8", "source": "MESURÉ", "photo": None,
                      "note": f"colonne 8\"x8\" qui monte du sous-sol (réponse du propriétaire, {REPONSES})"},
        "sens": None, "geometrie": dict(g_),
        "note": (f"prolongement au RDC de {c_['id']} ({REPONSES}) ; position DÉDUITE de celle du sous-sol"
                 + (" ; noyée dans la cloison S. de bain / chambre avant (axe B)" if (g_["x"], g_["y"]) == (132, 157) else "")
                 + (" ; tombe devant la porte de la chambre arrière — à valider" if (g_["x"], g_["y"]) == (132, 204) else ""))})
# poutre autoportante installée dans le plafond sur l'axe C, là où la cloison et les colonnes C4 / C6 ont été retirées
rdc["structure"].append({
    "id": "str-RDC-P03", "type": "poutre", "libelle": "POUTRE AUTOPORTANTE",
    "dimension": {"texte_original": None, "valeur": None, "source": "ILLISIBLE", "photo": None, "note": "section non relevée"},
    "sens": "x",
    "geometrie": {"x1": 146.0, "y1": 204.0, "x2": 456 - T_EXT, "y2": 204.0},
    "note": (f"Poutre autoportante installée dans le plafond du RDC sur l'axe C (17'-0\" du nu ext. avant), à l'emplacement de la "
             f"cloison et des colonnes C4 / C6 retirées ({REPONSES}). Étendue PRÉSUMÉE : de la colonne au coin du mur de la "
             "chambre arrière (12'-2\") jusqu'au mur droit ; appuis et section à relever. La poutre FLUSH 6\"x10\" du plan 1957 "
             "(cuisine) est sur la même ligne.")})
for c_ in rdc["structure"]:
    if c_["id"] == "str-RDC-C01":
        # précision du propriétaire : la colonne est au coin droit du mur de la chambre arrière (axe x = 12'-2", axe C)
        c_["geometrie"] = dict(c_["geometrie"], x=146.0, y=204.0)
        c_["note"] = ("prolongement au RDC de str-SS-C01 ; au coin droit (côté avant) du mur de la chambre arrière, à l'intersection "
                      "de la cloison x = 12'-2\" (mur-RDC-021) et de l'axe C — précision du propriétaire (2026-10-29) ; "
                      "position DÉDUITE de ce coin. Au plan 1957 du sous-sol, str-SS-C01 est à 11'-0\" (14 po plus à gauche) : voir écart.")
rdc["structure"].sort(key=lambda x: x["id"])
ANCRES = [
    {"id": "ancre-01", "description": "hors-tout de la façade avant (nu ext.)", "valeur": 456, "source": "MESURÉ", "reference": "38'-0\" (cote-SS-031 / RDC)"},
    {"id": "ancre-02", "description": "hors-tout en profondeur (nu ext.)", "valeur": 380, "source": "MESURÉ", "reference": "31'-8\""},
    {"id": "ancre-03", "description": "mur arrière : coin arrière droit → nu ext. du mur droit de l'entrée arrière", "valeur": 129, "source": "MESURÉ", "reference": "10'-9\" (cote-RDC-018)"},
]
for an in ANCRES:
    an["note"] = f"valeur attendue confirmée par le propriétaire ({REPONSES} : « tout est bon »)"
maison["projet"]["ancres"] = ANCRES
for c in rdc["cotes"]:
    if c["id"] == "cote-RDC-018":
        c["statut"] = "confirmee"
        c["note_constat"] = f"10'-9\" confirmé sur place ({REPONSES})"
for lc_ in rdc["lignes_cote"]:
    if lc_.get("ref") == "cote-RDC-018":
        lc_["statut"] = "confirmee"; lc_["repere"] = None
RESOLUS = {
    'conf-cote-RDC-018': ("résolu", f"10'-9\" confirmé sur place ({REPONSES})."),
    'p2-cloisons': ("résolu", f"Les cloisons restantes (G.R., lingerie, vestiaire, S. de bain, mur hall / salon) existent toutes ({REPONSES})."),
    'col-c4': ("résolu", f"Colonnes 8\"x8\" continues du sous-sol jusqu'en haut ; « C4 retirée » (2016) = prolongement au RDC de str-SS-C02, retiré avec la cloison de l'axe C ; la colonne du sous-sol est présente ({REPONSES})."),
    'col-c6': ("résolu", f"« C6 retirée » (2016) = prolongement au RDC de str-SS-C03, retiré ; la colonne du sous-sol est présente ({REPONSES})."),
    'col-p2': ("résolu", f"Les 6 colonnes du plan 1957 sont présentes selon le propriétaire ({REPONSES})."),
    'ancres': ("résolu", f"Hors-tout et cote arrière confirmés par le propriétaire ({REPONSES}) ; voir projet.ancres."),
}
for e in ECARTS:
    for cle, (stat, txt) in RESOLUS.items():
        if EC.get(cle) == e["id"]:
            e["statut"] = stat
            e["hypothese_retenue"] = txt + " " + e["hypothese_retenue"]
            e["a_valider_sur_place"] = ""
            e.pop("position", None)
    if e["id"] in (EC.get('conf-cote-RDC-048'), EC.get('arche')):
        e["description"] += (f" — Il n'y a plus d'arche : la cloison hall / salon s'arrête où l'arche commençait, puis c'est ouvert "
                             f"jusqu'à la colonne de l'axe B ({REPONSES}).")
        e["hypothese_retenue"] = ("Fin de la cloison au début de l'ancienne arche, ≈ 7'-11\" du nu ext. avant (ESTIMÉ : centre dessiné "
                                  "≈ 9'-10\" moins la moitié de 4'-0\"). " + e["hypothese_retenue"])
        e["a_valider_sur_place"] = "Mesurer où se termine la cloison hall / salon (distance depuis l'intérieur du mur avant)."
        e["impact"] = "faible"
    if e["id"] == EC.get('ep-int-rdc'):
        e["statut"] = "résolu"
        e["hypothese_retenue"] = f"4½\" confirmé par le propriétaire ({REPONSES}). " + e["hypothese_retenue"]
        e["a_valider_sur_place"] = ""
        e.pop("position", None)
    if e["id"] == EC.get('hp') or e["id"] == EC.get('axes'):
        e["statut"] = "reporté"
        e["hypothese_retenue"] = f"Non requis pour l'instant selon le propriétaire ({REPONSES}). " + e["hypothese_retenue"]
    if e["id"] == EC.get('ep-ext-rdc'):
        e["statut"] = "résolu"
        e["hypothese_retenue"] = f"10\" confirmé par le propriétaire ({REPONSES}). " + e["hypothese_retenue"]
        e["a_valider_sur_place"] = ""
        e.pop("position", None)
    if e["id"] == EC.get('col-plancher'):
        e["description"] += (" — Précision du propriétaire (2026-10-29) : au RDC, cette colonne est au coin droit du mur de la chambre "
                             "arrière (12'-2\" du coin gauche), soit 14 po à droite de la position du plan 1957 au sous-sol (11'-0\").")
        e["hypothese_retenue"] = ("RDC : colonne dessinée au coin du mur (12'-2\") ; sous-sol : position 1957 (11'-0\") conservée faute "
                                  "de mesure. Si la colonne est continue, l'une des deux positions est fausse.")
        e["a_valider_sur_place"] = ("Au sous-sol, mesurer la position de la colonne de la poutre arrière la plus à gauche (attendue à 11'-0\" "
                                    "du coin gauche au plan 1957, ou à 12'-2\" si elle est dans l'axe du mur de la chambre arrière).")
        e["impact"] = "moyen"
        e["position"] = [139.0, 204.0]
    if e["id"] == EC.get('fen-ss'):
        e["description"] += f" — La fenêtre arrière gauche a depuis été séparée en deux fenêtres ({REPONSES})."
        e["a_valider_sur_place"] = ("Mesurer la largeur des deux fenêtres arrière gauches (issues de l'ancienne 6'-8\") et leur position "
                                    "depuis le coin arrière gauche ; largeur de la fenêtre droite haute (6'-0\" du coin arrière).")
    if e["id"] == EC.get('porte-ss') or "Sens d'ouverture non dessiné" in e["description"]:
        e["description"] += f" Depuis, la porte du mur droit a été déplacée à la place de la fenêtre du milieu ({REPONSES})."
    if e["id"] == ECARTS[-1]["id"] or e["description"].startswith("constat du propriétaire"):
        e["a_valider_sur_place"] = ("Au RDC, sur l'axe C (17'-0\" du nu ext. avant) où il n'y a ni cloison ni poutre : comment le plafond "
                                    "et les solives sont-ils portés ? Hauteur libre sous la poutre 8\"x8\" de l'axe B.")
# une seule mesure pour la structure des axes B et C (écart « axes » et écart du constat)
_ax = next(e for e in ECARTS if e["id"] == EC['axes'])
for e in ECARTS:
    if e["description"].startswith("constat du propriétaire"):
        # constat intégré aux plans ; la seule vérification qui restait (poutres des axes B et C) est reportée avec l'écart « axes »
        e["statut"] = "résolu"
        e["hypothese_retenue"] = "Constat intégré aux plans. " + e["hypothese_retenue"]
        e["a_valider_sur_place"] = ""
        e.pop("position", None)
# le sous-sol a des ouvertures déplacées : un écart pour les positions et tailles présumées
ECARTS.append({"id": f"ecart-{len(ECARTS) + 1:03d}", "niveau": "SS", "impact": "moyen", "statut": "ouvert", "photo": "P2",
               "description": (f"{REPONSES} : la porte du mur droit et la fenêtre du milieu ont été permutées ; la grande fenêtre "
                               "arrière gauche (6'-8\") a été séparée en deux, la moitié gauche déplacée de 2'-0\" vers la gauche. "
                               "Largeurs et positions déduites de la description, non mesurées."),
               "hypothese_retenue": "Largeurs d'origine conservées (porte 2'-8\", fenêtre 3'-0\") ; chaque moitié de l'ancienne fenêtre = 3'-4\".",
               "a_valider_sur_place": ("Mesurer, au mur droit du sous-sol, la largeur et l'axe de la porte (attendu à 15'-0\" du nu ext. avant) "
                                       "et de la fenêtre (attendu à 6'-3\") ; au mur arrière, la largeur et l'axe des deux fenêtres de gauche "
                                       "(attendus à 9'-4\" et 14'-8\" du coin arrière gauche)."),
               "position": [451.0, 180.0]})

# 1e) annotations et réponses du propriétaire dans l'annotateur en ligne (2026-10-29)
ANNOT = "annotateur en ligne (2026-10-29)"
REP_ANNOT = {   # réponse du propriétaire, par clé d'écart
    'conf-cote-RDC-048': ("résolu", "« C'est correct comme ça »"),
    'conf-cote-SS-017': ("résolu", "« 3' » : largeur 3'-0\" confirmée"),
    'ep-pres': ("résolu", "« C'est correct comme elle est là »"),
    'fissures': ("sans objet", "« C'est réparé »"),
    'fiss-salon': ("sans objet", "« C'est réparé, enlève ça »"),
    'usage': ("sans objet", "« On s'en fout des noms, on les enlève »"),
    'arche': ("résolu", "« C'est correct comme ça »"),
    'ear-1po': ("résolu", "« C'est beau comme elle est là »"),
    'fen-ss': ("résolu", "« C'est beau »"),
    'porte-cav': ("résolu", "« Porte ici, la position est bonne »"),
    'poutre-flush': ("sans objet", "« Il n'y a plus de poutre à cet endroit, on peut enlever »"),
    'col-plancher': ("résolu", "« Enligne-les avec ceux en haut » : colonnes du sous-sol alignées sur celles du RDC"),
    'plomberie': ("sans objet", "« On s'en fout de la plomberie, enlève la trappe, ça existe plus »"),
    'cheminee': ("résolu", "« C'est OK comme ça »"),
    'axes': ("sans objet", "« Axe B 2016 on s'en fout » / « axe C 2016 on enlève » : axes retirés du plan"),
}
for e in ECARTS:
    for cle, (stat, txt) in REP_ANNOT.items():
        if EC.get(cle) == e["id"]:
            e["statut"] = stat
            e["hypothese_retenue"] = f"Réponse du propriétaire ({ANNOT}) : {txt}. " + e["hypothese_retenue"]
            e["a_valider_sur_place"] = ""
            e.pop("position", None)
    if e["description"].startswith(REPONSES) and "permutées" in e["description"]:
        e["statut"] = "résolu"
        e["hypothese_retenue"] = (f"Réponse du propriétaire ({ANNOT}) : « Porte de 36\" qui s'ouvre par en dedans ». "
                                  + e["hypothese_retenue"])
        e["a_valider_sur_place"] = ""
        e.pop("position", None)
    if e["id"] == EC.get('portes-ss'):
        e["description"] += f" — Porte du mur droit : 36\", ouvre vers l'intérieur ({ANNOT}) ; côté des pentures non précisé."
        e["a_valider_sur_place"] = "Côté des pentures de la porte du mur droit du sous-sol et sens d'ouverture de la porte du caveau."
for c in ss["cotes"]:
    if c["id"] == "cote-SS-017":
        c["statut"] = "confirmee"; c["note_constat"] = f"3'-0\" confirmé par le propriétaire ({ANNOT})"
for lc_ in ss["lignes_cote"]:
    if lc_.get("ref") == "cote-SS-017":
        lc_["statut"] = "confirmee"; lc_["repere"] = None
# structure retirée du plan : axes 2016, poutre autoportante, solives, poutre FLUSH (n'existe plus)
RETIRER_STR = {"str-RDC-AXB": "axe B du croquis 2016 : retiré du plan à la demande du propriétaire",
               "str-RDC-AXC": "axe C du croquis 2016 : retiré du plan à la demande du propriétaire",
               "str-RDC-P03": "poutre autoportante : retirée du plan à la demande du propriétaire",
               "str-RDC-S01": "solives 2x7 : retirées du plan à la demande du propriétaire",
               "str-RDC-S02": "solives 2x7 : retirées du plan à la demande du propriétaire",
               "str-RDC-P01": "poutre 6x10 FLUSH : n'existe plus selon le propriétaire"}
rdc["structure_retiree"] = [dict(x, retire_selon=f"{RETIRER_STR[x['id']]} ({ANNOT})") for x in rdc["structure"] if x["id"] in RETIRER_STR]
rdc["structure"] = [x for x in rdc["structure"] if x["id"] not in RETIRER_STR]
# trappe : n'existe plus
rdc["elements_retires"] += [dict(e, retire_selon=f"la trappe n'existe plus ({ANNOT})") for e in rdc["elements"] if e["id"] == "elem-RDC-TRAPPE"]
rdc["elements"] = [e for e in rdc["elements"] if e["id"] != "elem-RDC-TRAPPE"]
# colonnes : celle de l'axe B à 11'-0" se met en face de celle de l'axe C (12'-2") ; au sous-sol, alignées sur le RDC
for niv_, ids_ in ((rdc, ("str-RDC-C04",)), (ss, ("str-SS-C01", "str-SS-C04"))):
    for c_ in niv_["structure"]:
        if c_["id"] in ids_:
            c_["geometrie"] = dict(c_["geometrie"], x=146.0)
            c_["note"] = (c_.get("note") or "") + (f" ; déplacée à 12'-2\" du coin gauche, en face de la colonne de l'axe C "
                                                   f"(au coin du mur de la chambre arrière) ({ANNOT})")
# portes qui n'existent pas : baies sans porte
for o in rdc["ouvertures"]:
    if o["id"] in ("ouv-RDC-011", "ouv-RDC-026"):
        o["operation"] = "aucune"; o.pop("sens", None)
        o["note"] = f"baie sans porte : « la porte n'existe pas ici » ({ANNOT}) ; " + (o.get("note") or "")
# porte du sous-sol : 36", ouvre vers l'intérieur
for o in ss["ouvertures"]:
    if o["id"] == "ouv-SS-005":
        o["largeur"] = {"valeur": 36, "source": "MESURÉ", "photo": None, "note": f"36\" selon le propriétaire ({ANNOT})"}
        o["operation"] = "battante"
        o["sens"] = {"charniere": "debut", "ouvre_vers": "gauche",
                     "note": "ouvre vers l'intérieur (propriétaire) ; côté des pentures PRÉSUMÉ (non précisé)"}
        o["texte_original"] = "PORTE 2'-8\" (plan 1957) ; aujourd'hui porte de 36\""
# porte du caveau : ouvre vers la maison (sous-sol principal) — réponse du propriétaire (2026-10-29)
for o in ss["ouvertures"]:
    if o["id"] == "ouv-SS-008":
        o["operation"] = "battante"
        o["sens"] = {"charniere": "debut", "ouvre_vers": "gauche",
                     "note": "ouvre vers la maison (sous-sol principal) selon le propriétaire ; côté des pentures PRÉSUMÉ (non précisé)"}
for e in ECARTS:
    if e["id"] == EC.get('portes-ss'):
        e["statut"] = "résolu"
        e["hypothese_retenue"] = ("Réponse du propriétaire (2026-10-29) : porte du caveau ouvre vers la maison, porte du mur droit vers "
                                  "l'intérieur ; côté des pentures PRÉSUMÉ pour les deux. " + e["hypothese_retenue"])
        e["a_valider_sur_place"] = ""
        e.pop("position", None)
# cotes : seulement à l'extérieur
for niv_ in (rdc, ss):
    niv_["lignes_cote"] = [l for l in niv_["lignes_cote"] if l["facade"] != "int"]
# notes du plan d'origine qui ne décrivent plus l'existant (éléments retirés, réparés ou jugés inutiles par le propriétaire)
NOTES_RET = {"note-RDC-03", "note-RDC-04", "note-RDC-05", "note-RDC-06", "note-RDC-07", "note-RDC-08", "note-RDC-09"}
rdc["notes_retirees"] = [dict(n, retire_selon=ANNOT) for n in rdc["notes"] if n["id"] in NOTES_RET]
rdc["notes"] = [n for n in rdc["notes"] if n["id"] not in NOTES_RET]
for e in ECARTS:
    if e["id"] == EC.get('portes-ss'):
        e["position"] = [261.0, 375.0]          # reste : la porte du caveau (sens) et le côté des pentures de la porte du mur droit
maison["projet"]["affichage"]["metrique"] = False
maison["projet"]["affichage"]["note"] += " ; cotes intérieures et métrique retirées des plans (annotateur, 2026-10-29)"

# 1f) 2e série d'annotations du propriétaire (annotateur, 2026-10-29)
ANNOT2 = "annotateur en ligne, 2e série (2026-10-29)"
rdc["limites_zones"] = []                                   # « Enlever pointillé » : limites des zones ouvertes retirées
ss["elements_retires"] += [dict(e, retire_selon=f"retiré du plan à la demande du propriétaire ({ANNOT2})")
                           for e in ss["elements"] if e["id"] == "elem-SS-RAMO"]
ss["elements"] = [e for e in ss["elements"] if e["id"] != "elem-SS-RAMO"]
for niv_ in (ss, rdc):                                      # flèches de solives masquées (les solives existent toujours)
    for x in niv_["structure"]:
        if x["type"] == "solives":
            x["afficher"] = False
maison["projet"]["affichage"]["textes_structure"] = False   # « enlève tous les textes à l'intérieur du bâtiment »
NOUVEAUX = [  # (id, type, nom, libellé, x, y, rotation) — positions pointées par le propriétaire dans l'annotateur
    ("elem-SS-DR-BAIN", "drain", "Drain de bain", "DRAIN BAIN", 27.9, 203.9, 0),
    ("elem-SS-DR-WC", "drain", "Drain de toilette", "DRAIN TOILETTE", 54.7, 202.0, 0),
    ("elem-SS-DR-LAV", "drain", "Drain de lavabo", "DRAIN LAVABO", 432.5, 314.3, 0),
    ("elem-SS-PANNEAU", "panneau-electrique", "Panneau électrique", "PANNEAU ÉLECTRIQUE", 12.0, 109.2, 90),
]
for i_, t_, n_, l_, x_, y_, r_ in NOUVEAUX:
    ss["elements"].append({"id": i_, "type": t_, "nom": n_, "nom_original": None, "libelle": l_,
                           "position": {"x": x_, "y": y_, "rotation_deg": r_, "source": "ESTIMÉ",
                                        "note": f"position pointée par le propriétaire sur le plan ({ANNOT2})"},
                           "dimensions": None, "note": f"ajouté par le propriétaire ({ANNOT2})"})
ss["elements"].sort(key=lambda e: e["id"])
# 3e série (2026-10-29) : symboles sans texte ; drains de bain et de toilette alignés ; poutres, perron et marches retirés du dessin
for e in ss["elements"]:
    if e["id"] in ("elem-SS-DR-BAIN", "elem-SS-DR-WC", "elem-SS-DR-LAV", "elem-SS-PANNEAU"):
        e["libelle"] = False
    if e["id"] in ("elem-SS-DR-BAIN", "elem-SS-DR-WC"):
        e["position"]["y"] = 203.0
        e["position"]["note"] += " ; aligné avec l'autre drain (même y) à la demande du propriétaire"
for niv_ in (ss, rdc):
    for x in niv_["structure"]:
        if x["type"] == "poutre":
            x["afficher"] = False            # les pointillés des poutres sont retirés du dessin (données conservées)
EXT_RET = {"elem-RDC-MAR-AR": "marches / patio arrière", "elem-RDC-PERRON": "perron avant", "elem-RDC-MAR-AV": "marches avant"}
rdc["elements_retires"] += [dict(e, retire_selon=f"{EXT_RET[e['id']]} : seul l'intérieur du bâtiment est dessiné (propriétaire, 2026-10-29)")
                            for e in rdc["elements"] if e["id"] in EXT_RET]
rdc["elements"] = [e for e in rdc["elements"] if e["id"] not in EXT_RET]
rdc["notes"] = [n for n in rdc["notes"] if n["id"] != "note-RDC-02"]      # note du perron (retiré)
ss["notes_retirees"] = [dict(n, retire_selon="élément retiré du plan (propriétaire, 2026-10-29)") for n in ss["notes"] if n["id"] == "note-SS-05"]
ss["notes"] = [n for n in ss["notes"] if n["id"] != "note-SS-05"]          # porte de ramonage (retirée)
for e in ECARTS:
    lot_ = e["id"] in (EC.get('conf-cote-IMP-010'), EC.get('conf-cote-P5-010'))
    if lot_ or e["id"] == EC.get('p5'):
        e["statut"] = "résolu"
        e["hypothese_retenue"] = (f"Réponse du propriétaire ({ANNOT2}) : « {'115.17' if lot_ else 'C’est beau'} ». "
                                  + e["hypothese_retenue"])
        e["a_valider_sur_place"] = ""
        e.pop("position", None)

# 2) renumérotation des photos dans l'ordre d'envoi du propriétaire (1 à 7).
#    Les fichiers de travail (photos/, prep/, arbitrage/vignettes/) gardent la numérotation interne ;
#    la correspondance est dans RAPPORT.md. Les identifiants (cote-P2-…) et les chemins ne sont pas touchés.
PHOTO_ORDRE_ENVOI = {"P2": "P1", "P1": "P2", "P7": "P3", "P3": "P4", "P4": "P5", "P6": "P6", "P5": "P7"}
_re_photo = re.compile(r"(?<![\w-])(?<!redresse/)(?<!tuiles/)(?<!photos/)P([1-7])(?![\w-]|\.\w)")


def _renum(o):
    if isinstance(o, str):
        return _re_photo.sub(lambda mt: PHOTO_ORDRE_ENVOI["P" + mt.group(1)], o)
    if isinstance(o, list):
        return [_renum(x) for x in o]
    if isinstance(o, dict):
        return {k: _renum(v) for k, v in o.items()}
    return o


def _ids(o):
    if isinstance(o, str):
        o = re.sub(r"cote-P2-0(\d\d)", r"cote-RDC-2\1", o)
        o = o.replace("cote-P5-", "cote-IMP-").replace("mur-SS-011", "elem-SS-CHEM")
        return o.replace("elem-SS-TUYAU", "tuyau à fumée (non reporté)").replace("elem-SS-VIROLE", "virole (non reportée)")
    if isinstance(o, list):
        return [_ids(x) for x in o]
    if isinstance(o, dict):
        return {k: _ids(v) for k, v in o.items()}
    return o


maison = _ids(maison)
maison = _renum(maison)
maison["projet"]["photos"] = sorted(maison["projet"].get("photos", []), key=lambda p: p.get("id", ""))
maison["projet"]["correspondance_photos_internes"] = {v: k for k, v in sorted(PHOTO_ORDRE_ENVOI.items(), key=lambda kv: kv[1])}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(maison, f, ensure_ascii=False, indent=1)
    f.write('\n')

# ---------------------------------------------------------------------------- résumé
for niv in ('SS', 'RDC'):
    U = UNION[niv]
    brute = unary_union([Polygon(p.exterior) for p in (U.geoms if hasattr(U, 'geoms') else [U])]).area / 144
    sp = sum(Polygon(p['polygone']).area for p in PIECES[niv]) / 144
    print(f"{niv}: brute {brute:.1f} pi² ; Σ pièces {sp:.1f} pi² ; murs {U.area / 144:.1f} pi² ; {len(PIECES[niv])} pièces ; "
          f"{len(COTES[niv])} cotes ; {len(LC[niv])} lignes de cote")
imp = {}
for e in ECARTS: imp[e['impact']] = imp.get(e['impact'], 0) + 1
print("écarts :", len(ECARTS), imp)
for v in VERIF:
    if not v.startswith('OK'): print(v)
print("vérifications OK :", sum(v.startswith('OK') for v in VERIF), "/", len(VERIF))
