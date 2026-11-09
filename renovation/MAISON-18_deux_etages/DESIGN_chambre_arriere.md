## Chambre des parents (chambre arrière du RDC) — « lit king, rangement optimisé »

Module : `rdc_chambre_arriere.py` (`appliquer_modifs_rdc` pour le plan P-130, `appliquer_scene_rdc` pour la maquette).

### Demande
« Réaménage la chambre arrière, lit king mais rangement optimisé. » C'est la chambre des parents : un lit king
(matelas 76 × 80 po) avec 24 po de dégagement des deux côtés et 30 à 36 po au pied, du rangement « chic et
fonctionnel » sans surcharger la pièce. Aujourd'hui : lit queen tête au mur de la salle de bain, commode blanche, mur
en papier peint imitation planches, vélo de route sur base d'entraînement devant la fenêtre, deux petites garde-robes
(G.R. 1 et 2) à portes battantes qui ouvrent dans la chambre.

### Contraintes relevées (maison.json)
| Élément | Position | Conséquence |
|---|---|---|
| Chambre (nu intérieur) | x 10 à 143¾, y 226 à 370 (12'-0" × 11'-1¾", ≈ 136 pi²), plus le retrait de la porte (x 110 à 144, y 214 à 226) | 134 po de large au total : un king (82 po avec la plateforme) + 2 × 24 po = 130 po, ça entre dans un seul sens sans toucher la porte |
| Fenêtre `ouv-RDC-003` | mur arrière (y = 370), 75 po de large, axe x = 98 (x 60½ à 135½), allège ≈ 34, tête ≈ 82 | ne pas la bloquer ; rien de plus haut que l'allège devant |
| Porte `ouv-RDC-016` | 30 po, dans le retrait (y = 212, x 112 à 142), ouvre dans la chambre, pentures côté x = 142 | son arc couvre x 112 à 142, y 212 à 242 : rien dedans |
| Portes des G.R. `ouv-RDC-019`, `ouv-RDC-020` | 2 × 28 po battantes sur `mur-RDC-021` (x = 146), arcs jusqu'à x ≈ 118 | elles mangeraient le dégagement au pied d'un king : on les remplace |
| Mur gauche `mur-RDC-004` | mur extérieur aveugle (x = 10) | le seul long mur plein, sans porte ni fenêtre : c'est le mur de tête |

### Pourquoi la tête au mur gauche (orientations comparées)
- **Tête au mur de la salle de bain (comme aujourd'hui)** : un king centré laisse 29 po de chaque côté, mais le côté
  droit tombe dans le retrait de la porte et dans son arc (x 112 à 142). Refusé.
- **Tête sous la fenêtre (mur arrière)** : bloque la fenêtre, pas de mur de tête intégré possible, pied du lit à 65 po
  de la salle de bain mais rien ne s'y range. Refusé.
- **Tête au mur gauche (retenu)** : plateforme 84 × 82 po de x 21½ à 105½, y 257 à 339. **31 po de chaque côté,
  38¼ po au pied** (jusqu'à la façade de la garde-robe), l'arc de la porte reste libre, la fenêtre est sur le côté du lit
  (31 po de passage devant).

### Ce qui change
**Plan P-130**
- Pièce renommée « Chambre des parents ». Éléments neufs : `LIT KING` (plateforme), mur de tête intégré (bande de 9 po
  le long du mur gauche), deux chevets suspendus, tour de tiroirs dans la garde-robe.
- **G.R. 1 et 2 réunies** : la cloison `mur-RDC-023` et les deux portes battantes `ouv-RDC-019` / `ouv-RDC-020` sont
  retirées (gardées dans `murs_retires` / `ouvertures_retirees`) ; nouvelle baie `ouv-RDC-CH1-GR` de 66 po (y 302 à
  368) à **deux portes coulissantes** de 34 po dans `mur-RDC-021` ; nouvelle pièce `piece-RDC-GRP` « G.R. » de
  24½ × 71¾ po (12,2 pi²). Plus aucun arc de porte dans la chambre, sauf celui de la porte d'entrée de la pièce.
- Note courte ajoutée au cartouche (`note-RDC-CH1-01`).

**Maquette 3D** (le mobilier RDC-01 de la chambre est retiré : lit queen, chevet, cadres, suspension cage, commode,
vélo et son tapis, store marine, papier peint, panier)
| Élément | Description |
|---|---|
| Mur de tête intégré | fourrure de 9 po devant le mur extérieur (l'isolant n'est pas touché), du plancher au plafond, en **vrai bois de grange** (le client aime le bois : on passe du papier peint imitation au vrai, comme les comptoirs de la cuisine) |
| Niches éclairées | 2 niches latérales noir mat de 20 × 32 po, 6 po de creux, DEL sous le dessus, **2 prises USB-C** au fond ; une niche-tablette horizontale de 84 × 10 po au-dessus de la tête de lit (livres, cadres), aussi éclairée |
| Tête de lit | rembourrée à 7 canaux verticaux (tissu gris pâle), 86 po de large, de 12 à 50 po de haut |
| Liseuses | 2 liseuses murales noires articulées, bras vers l'oreiller, interrupteur à portée de main |
| Chevets suspendus | noir mat, 22 × 16 po, un tiroir chacun, dessus à 25 po (à la hauteur du matelas) ; plancher libre dessous |
| Lit king | plateforme noir mat 84 × 82 po, dessus à 12½ po, socle en retrait de 3 po (le lit « flotte »), **4 grands tiroirs** (≈ 32 × 20 × 8 po, 2 par côté, prises de doigt sans quincaillerie) ; matelas 76 × 80, couette blanche, jeté sauge, coussins caramel |
| Garde-robe réunie | **double penderie** (26 po, tringles noires à 41 et 81 po) ; **tour de 4 tiroirs** (22 po) et 3 tablettes à chandails ; **penderie longue** (24 po, tringle à 68 po) et tablette à souliers ; tablette haute continue à 84 po avec 4 paniers ; DEL à l'ouverture ; intérieur en placage de bois pâle |
| Portes coulissantes | rail encastré ; vantail avant = **miroir pleine hauteur à cadre noir mat** (remplace le miroir de la commode) ; vantail arrière = noir mat à fines rainures, tirette noire |
| Fenêtre | un grand rideau de lin pleine hauteur sur rail noir au plafond (la fenêtre paraît plus grande), qui se range côté lit : le coin entre la fenêtre et la garde-robe reste libre ; store opaque dans l'embrasure |
| Sol et murs | érable existant ; tapis de laine ≈ 8 × 8½ pi sous les deux tiers du lit (hors de l'arc de la porte) ; murs « Lin chaud » (greige, #E2D9CB, à choisir sur échantillon) |
| Éclairage | 4 encastrés plats 2700 K autour du lit (aucun au-dessus des oreillers), 1 dans la garde-robe, DEL des niches, liseuses |
| Cloison du pied | une seule œuvre encadrée (générique) ; le reste respire |

Arrêts de visite : « Chambre des parents » (depuis la porte, vers le mur de tête) et « Chambre des parents,
garde-robe » (depuis le côté fenêtre, vers la garde-robe), à la place des deux arrêts « Chambre arrière ».

### Rangement : avant / après
| | Avant | Après |
|---|---|---|
| Penderie | 2 G.R. à une tringle (≈ 67 po de tringle) | 76 po de tringle (2 × 26 po en double + 24 po en long) |
| Tiroirs | commode blanche (3 tiroirs) | 4 grands tiroirs sous le lit + 4 dans la garde-robe + 2 chevets |
| Tablettes | tablettes hautes des G.R. | tablette haute continue (4 paniers) + 3 tablettes à chandails + 3 niches |
| Plancher libre | commode, vélo, panier au sol | rien au sol à part le lit : la pièce respire |

### Le vélo
Le vélo de route sur base d'entraînement **descend au gym du sous-sol** : SS-17 y prévoit déjà l'emplacement d'un vélo
sur base, à côté du tapis roulant (`elem-SS-P-GYM-VELO`). Si un deuxième vélo est déjà là, les deux bases se placent
côte à côte ou le second va sur un support mural ; à coordonner avec la zone gym (non modifiée ici).

### Ce qui n'est pas fait, et pourquoi
- **Pas de banc au pied du lit** : un banc de 14 po ramènerait le passage devant la garde-robe de 38 à 24 po (sous les
  30 à 36 po demandés), et les tiroirs de la garde-robe doivent pouvoir s'ouvrir. Si le client y tient : un pouf
  rond qui se range sous la fenêtre, ou l'option « coffre à vérins » ci-dessous avec un lit plus court de 4 po.
- Pas de commode : ses tiroirs passent dans le lit, les chevets et la garde-robe.

### Options
| Choix | A — économique | B — recommandée (dessinée) |
|---|---|---|
| Garde-robe | on garde les 2 G.R. et la cloison ; portes battantes remplacées par 2 portes pliantes (saillie ≈ 14 po, 24 po libres au pied quand elles sont ouvertes) ; aménagement en kit | G.R. 1 et 2 réunies, baie de 66 po, 2 coulissantes (miroir + noir mat), aménagement complet |
| Mur de tête | panneau de bois de grange de 8 pi de large derrière le lit, 2 tablettes flottantes, 2 liseuses, prises USB-C en applique | fourrure pleine largeur et pleine hauteur, niches noir mat éclairées, chevets suspendus intégrés |
| Lit | plateforme du commerce à tiroirs | plateforme sur mesure à 4 tiroirs ; variante : **coffre à vérins** (tout le dessous en coffre, pour le saisonnier ; plus de rangement, moins pratique au quotidien) |
| Portes de la G.R. | — | variante : 2 panneaux de bois de grange sur rail apparent noir (look grange), mais alors un second grand pan de bois face au mur de tête |

### Coût (ordre de grandeur, à confirmer par 2 ou 3 soumissions à Baie-Comeau)
Estimation de l'équipe d'après les prix de détail et les taux usuels au Québec (2025-2026), installation comprise.
| Poste | Fourchette |
|---|---|
| Mur de tête intégré (fourrure, gypse, bois de grange ≈ 100 pi², 3 niches, DEL, 2 liseuses, 2 prises USB-C, électricien, chevets suspendus) | 4 500 – 9 000 $ |
| Plateforme king à 4 tiroirs (commerce → sur mesure) | 1 000 – 5 500 $ |
| Matelas king et literie king | 1 600 – 4 500 $ |
| Garde-robe : cloison et montant enlevés, linteau, gypse, peinture | 1 200 – 2 800 $ |
| Garde-robe : aménagement intérieur (penderies, 4 tiroirs, tablettes, DEL) | 1 500 – 4 000 $ |
| 2 portes coulissantes 34 × 80 (miroir et noir mat), rail encastré | 1 200 – 2 800 $ |
| Peinture de la chambre, 4 encastrés et gradateur | 1 200 – 2 400 $ |
| Rideau de lin, rail, store opaque, tapis | 1 000 – 2 500 $ |
| **Total option B** | **≈ 13 000 – 33 000 $** |
| Option A (pliantes, panneau de tête, plateforme du commerce) | ≈ 5 000 – 10 000 $ |

### Points à vérifier sur place
1. `mur-RDC-021` (chambre / garde-robes) : **porteur inconnu**. La baie de 66 po (au lieu de deux baies de 28 po et
   d'un montant) demande un linteau si le mur porte ; vérifier le sens des solives au-dessus.
2. Mur gauche (extérieur) : prises, thermostat ou plinthe électrique à déplacer dans la fourrure ; garder l'isolant et
   le pare-vapeur intacts derrière les niches (les niches sont dans la fourrure de 9 po, pas dans le mur extérieur).
3. Plinthe chauffante sous la fenêtre : garder ≈ 6 po entre la plinthe et le rideau (ou rideau qui s'arrête
   au-dessus).
4. Fenêtre `ouv-RDC-003` dessinée « fixe » au plan de base : une chambre doit avoir une **fenêtre qui ouvre et permet
   l'évacuation** (ouverture libre ≥ 0,35 m², aucune dimension < 380 mm) — à vérifier.
5. Avertisseur de fumée (et de CO) dans la chambre ou le corridor, relié aux autres.
6. Livraison : un matelas king (souple) passe la porte de 30 po ; pas de sommier rigide de 76 po (la plateforme le
   remplace) ; plateforme livrée en pièces.
7. Hauteur de plafond PRÉSUMÉE à 96 po : la tablette haute de la garde-robe est à 84 po.
8. Profondeur de la garde-robe (24½ po au nu) : juste suffisante pour une penderie ; mesurer avant de commander.

**À valider avec la Ville et un professionnel** (linteau, électricité, fenêtre d'évacuation, avertisseurs).

### Limites de la maquette
- Le miroir de la porte coulissante reflète l'intérieur de la garde-robe (il paraît brun) : la visionneuse prend
  l'image d'un miroir du côté du centre de la maison (x = 228), donc derrière ce miroir-ci. Signalé au moteur.
- Œuvre encadrée, livres et vêtements : génériques.
