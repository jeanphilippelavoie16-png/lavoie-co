# Fiche du cabanon (garage de cour) — 86, avenue Laurier, Baie-Comeau

Tout ce qu'on sait du cabanon, pour l'agent qui en fera les plans. Dans le dépôt on l'appelle « garage » : c'est le cabanon du
plan de DAG, agrandi à la demande du client le 2026-11-02 (« 5 pieds par en avant et 3 pieds côté piscine »).
**Ce n'est pas encore construit : ce sont les dimensions du projet, pas un relevé.**

## Dimensions

| Élément | Dimension |
|---|---|
| Murs, hors tout | **13'-0" × 17'-0"** (156 × 204 po) ; 221 pi² (20,5 m²) |
| Largeur (mur de la porte et mur du fond) | 13'-0" |
| Profondeur (murs de côté) | 17'-0" |
| Intérieur fini | 12'-2" × 16'-2" (146 × 194 po) |
| Épaisseur des murs | 5 po : planches verticales ¾ po + ossature 2 × 4 + contreplaqué ½ po dedans |
| Hauteur des murs | 8'-0" (dalle au-dessus des sablières) |
| Plafond (contreplaqué) | 7'-10" au-dessus de la dalle |
| Toit | deux versants, pente **7/12**, faîte dans le sens de la profondeur, pignon vers la maison |
| Débord du toit | 12 po sur les quatre côtés : toit de **15'-0" × 19'-0"** (180 × 228 po) |
| Faîte | 12'-4" au-dessus du sol (3,76 m) |
| Porte de garage | **8'-0" de large × 7'-0" de haut**, centrée sur le mur avant (30 po de mur de chaque côté), tournée vers la maison |
| Dalle | béton, au ras du gazon (½ po au-dessus), débord de 2 po autour des murs |
| Fenêtres, porte de service | aucune (pas de fenêtre côté piscine sans vérifier la bande de 1 m) |

## Implantation sur le terrain

- Dans la cour arrière, coin arrière droit vu de la rue (côté de l'allée).
- **3'-0" des lignes de lot** arrière et de côté, mesuré au débord du toit (la Ville demande 90 cm).
- Environ **20'-1"** du mur arrière de la maison au mur avant du cabanon.
- **40,6 po (1,03 m)** entre le mur côté piscine et la paroi de la piscine de 21 pi ; le débord du toit est à 28,6 po de la paroi.
- Sol de la cour au niveau du cabanon ; l'allée est 45 po plus bas (6 marches de pierre) : une souffleuse ne descend pas tel quel.
- Deux dalles de pas japonais du portillon (haut des marches) jusqu'à la porte.
- Repère du dépôt (pouces ; x le long de la façade, y vers l'arrière, mur arrière de la maison à y = 380) :
  murs x 355 → 511, y 621 → 825 ; toit x 343 → 523, y 609 → 837 ; porte x 385 → 481 sur y = 621 ; dalle à z 48,5.

## Allure (vidéo DAG « C-1329 », captures 03 à 07)

- Planches verticales **blanches** à couvre-joints (aux 12 po), rives, soffites, gouttières et retours de corniche blancs.
- Bardeau d'asphalte gris foncé (#4E5154).
- Porte de garage **noire** à 4 sections, 8 carreaux dans la section du haut, chambranle blanc de 3 po.
- Dedans : murs et plafond de contreplaqué, dalle de béton.

## Aménagement intérieur prévu (DESIGN_garage.md, garage.py)

Souffleuse derrière la porte à gauche ; établi de 8 pi au mur de gauche (côté piscine) ; mur de 30 bacs de 68 L au fond
(141 × 30 po, 87½ po de haut) ; vélos des garçons au sol et vélos des adultes au plafond à droite ; outils de jardin et armoire
des produits de piscine à droite de la porte ; 4 luminaires DEL de 4 pi. Allée centrale de 5'-11".

## Règles de la Ville et points à valider

- Garages et remises : 60 m² au plus en tout, 15 % du terrain, 2 bâtiments au plus, 90 cm des lignes, 2 m de la maison,
  hauteur de 4,25 m au plus. Ici : 20,5 m², faîte à 3,76 m.
- Distance d'une piscine : **1 m pour une remise** (rangement, pas d'auto), 1,5 m pour un garage isolé. À 1,03 m, il doit rester
  une remise aux yeux de la Ville : à dire au Service de l'urbanisme. **Permis requis.**
- Rien de fixe qui permette de grimper sur le mur côté piscine, dehors.
- Électricité : aucune pour l'instant ; conduit enterré depuis la maison à prévoir (maître électricien).
- Fondation, charpente du toit, charges de neige : non étudiées ; à valider avec un professionnel.
- Coût repère : 13 000 à 24 000 $ pour le bâtiment avec dalle et porte ; aménagement 3 000 à 6 500 $ ; électricité 2 500 à 6 000 $ (estimations).

## Images (ce dossier)

- `vue_exterieur_porte.jpg` : le cabanon vu de la cour, porte ouverte (coque vide, avant l'aménagement).
- `planche_amenagement.jpg` et `plan_amenagement.png` : plan coté de l'intérieur et 4 vues.
- `vue_interieur_depuis_porte.jpg`, `vue_atelier.jpg`, `vue_mur_bacs.jpg`, `vue_velos.jpg`.
- Visite 3D complète (on y entre) : https://claude.ai/artifact/BcvbdKVk2VjTxMswm2JYLC, arrêts « Garage vu de la cour » et « Garage — atelier et rangement ».

## Plans de construction (dossier `plans/`, 2026-11-14)

Plans de menuiserie en 6 feuilles 11 × 17 : `plans/PLANS_cabanon.pdf`, une image par feuille dans `plans/png/` (A1 vue d'ensemble,
A2 dalle, A3 et A4 ossature des murs, A5 toit, A6 gabarit du chevron, corniche, listes). Toutes les cotes sont calculées par
`plans/plans_cabanon.py` (`python plans_cabanon.py`, puis `node rendre.js` pour les PNG et le PDF).

- Charpente dimensionnée pour la neige de Baie-Comeau (4,3 kPa au sol + 0,4 kPa de pluie, 2,8 kPa sur le toit, pièces lues à
  3,0 kPa) : colombages 2 × 4 aux 16 po, chevrons et solives de plafond 2 × 6 aux 16 po, linteau de la porte 2 − 2 × 8.
- **Écarts avec cette fiche, à valider par le client** (détail sur la feuille A1) : hors tout fini gardé à 13' × 17', donc ossature
  12'-8" × 16'-8" et intérieur fini 12'-0" × 16'-0" ; mur de 6 po (OSB et fourrures sous les planches) ; bordure de béton de 6 po
  sous les murs ; dalle au nu de l'ossature, sans le débord de 2 po ; plafond fini à 7'-11½", faîte à 12'-2⅛".
- Toujours à valider : la dalle (typique, non calculée), le dégagement de 11½ po au-dessus de la porte, le permis.

## Sources dans le dépôt

- `../exterieur.py` : constantes `CAB…` en tête et fonction `garage()` (géométrie exacte).
- `../garage.py` : aménagement intérieur.
- `../DESIGN_exterieur.md` (section du 2026-11-02) et `../DESIGN_garage.md` : décisions, règlements et sources.
- Plan DAG du 17-12-2025 et vidéo DAG : `renovation/prive/` (hors dépôt).
