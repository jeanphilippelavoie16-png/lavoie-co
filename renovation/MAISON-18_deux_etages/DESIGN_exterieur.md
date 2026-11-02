## Extérieur — la maison vue de dehors et la cour arrière (plan DAG)

**Demande du client** : « Je veux aussi que tu fasses l'extérieur. »

On n'a pas redessiné la cour : on a **mis en 3D le projet de Design Action Gestion (DAG)**, tel quel, et on a ajouté autour la
maison vue de dehors, le devant du terrain et les côtés. Pour l'instant, ce sont **des données seulement**
(`exterieur.py`, dictionnaire `EXTERIEUR`). La visite ne marche pas encore dehors : le moteur l'ajoutera en suivant le contrat
décrit dans le docstring de `exterieur.py`. On peut déjà voir le résultat dans la maquette actuelle avec un aperçu (voir plus bas).

### Sources

| Source | Ce qu'on en a tiré |
|---|---|
| **Plan d'aménagement de la cour arrière, DAG, 17-12-2025**, éch. 3/16" = 1'-0" (`plan_cour-1.png`, 150 ppp) | Tout ce qui est dans la cour : position, dimensions, couleurs des garde-corps, lignes de lot arrière et côtés |
| Vidéo DAG « C-1329 Aménagement extérieur » (vignettes) | L'allure : cabanon blanc en planches verticales, toit à deux versants, portes doubles noires de grange avec impostes vitrées ; pas japonais en dalles blanches ; deck à garde-corps d'aluminium noir sur une jupe blanche en déclin ; piscine hors-terre grise ; maison en brique rouge, toit en croupe gris foncé, fascias blancs, fenêtres noires, cheminée, fondation blanche apparente, allée sur le côté ; patio beige avec table, BBQ et bacs à plantes |
| `donnees/maison.json` (relevé R0, plan d'implantation 1957 P7, croquis 2016 P1) | Murs extérieurs, fenêtres et portes (lus à chaque génération : si un autre module change une ouverture, la façade suit), cheminée, perron avant, entrée arrière, lignes de lot du devant, fermes 5/12 |

**Calage du plan DAG.** Le dessin est tourné de 180° par rapport à nos plans. On a mesuré l'image au pixel près, à l'échelle de
la largeur de la maison (38'-0" = 1067 px, donc 2,34 px par pouce) : x = 456 - (x_px - 625) / 2,34 ; y = 380 + (y_px - 171) / 2,34.
Ça recoupe tout ce qu'on peut vérifier, à moins de 1 po près : l'entrée arrière tombe à x 219-327 (relevé : 219-327) ; le
palier fait 129 × 60 po (« ±10'-9" × 4'-11" ») ; la piscine est à 6'-2⅝" du cabanon, à 9'-10⅜" de la ligne de lot oblique et à
3'-4¼" de la ligne arrière ; le cabanon est à 3'-0" des deux lignes de lot. Les lignes de lot du plan DAG concordent avec le plan
d'implantation de 1957 à 4 po près (profondeur du côté droit 1351 po contre 1347 ; largeur arrière 604 contre 603 ; ligne
gauche 1386 contre 1382).

### Ce qui est modélisé

Repère de la maison, en pouces ; z est compté depuis le plancher du sous-sol. Le rez-de-chaussée est à 105 et le terrain à 48.

**La cour, d'après le plan DAG**

| Élément | Où (x, y) | Hauteur, matériau |
|---|---|---|
| Palier ±10'-9" × 4'-11" | 327-456 × 380-440, contre le mur arrière, devant la porte de l'entrée arrière | dessus à 97½ (une marche sous le seuil, 49½ po du sol) ; platelage beige |
| Escalier 5'-9½" | 386-456 × 440-494, descend vers la cour | 7 contremarches de 7,07 po, 6 girons de 9 po (mesurés au plan) ; contremarches blanches |
| Patio ±19' × 10' | 159-386 × 440-560 | au niveau du palier (le plan ne montre ni marche ni garde-corps entre les deux) |
| Deck ±13' × 11'-9" | 159-314 × 560-701, entaillé par la piscine | au même niveau, 2½ po sous la margelle |
| Piscine hors-terre de 21' | centre (190,6 ; 724,3) | paroi grise de 52 po, 24 montants, margelle, toile bleue, eau |
| Anneau de gravier | rayon de 126 à 140 po autour de la piscine | |
| Garde-corps d'aluminium noir | couleurs du plan | **vert** : barreaux 36 po (palier et escalier côté allée, patio côté escalier, devant le mur, bout gauche, bas du patio) ; **rouge** : barreaux 48 po (deux côtés du deck) ; **bleu** : verre pur 48 po entre le patio et le deck, avec un **portillon de 36 po à ferme-porte** (« la porte menant au deck sera munie d'un dispositif de fermeture automatique ») |
| Jupe des terrasses | sous le palier, le patio et le deck | déclin horizontal blanc (vidéo) |
| Bande de roche de 4'-0" | 457-505 × 380-560, plus le pied de l'escalier (386-445 × 494-560) | pierre décorative |
| Muret de soutènement | 445-457 × 494-560 | béton, 18 po hors sol |
| Pas japonais (interblocs) | 3 dalles de 36 × 24 po entre le pied de l'escalier et le cabanon, inclinées comme au plan | dalles blanches |
| Cabanon 10' × 12' | murs 391-511 × 681-825 ; toit 379-523 × 669-837 (débord de 12 po) | dalle de béton ; planches verticales blanches à couvre-joints ; toit 6/12 à deux versants, faîte selon y ; pignon et **portes doubles noires de grange (2 × 32 × 76 po), impostes à 4 carreaux, écharpes en X** tournés vers la maison, au bout des pas japonais (comme dans la vidéo) ; lanterne |
| Appareils de la piscine | dalle de 3' × 6' inclinée, à 3'-4" de la piscine et de la ligne arrière | thermopompe, filtre au sable, pompe |
| Mobilier du patio (sobre) | | table de 6 pi en bois sur aluminium noir, 4 chaises ; BBQ au gaz contre le garde-corps de l'escalier ; 2 bacs blancs plantés |

**La maison vue de dehors**

- **Brique rouge** sur les murs du rez-de-chaussée, de 97 po jusqu'aux soffites. **Fondation apparente** crépie blanche, du sol
  à 97 po. Les deux parements sont percés aux vraies ouvertures du relevé.
- **Fenêtres noires** : cadre, vitre, meneaux sur les grandes baies, allège de béton au RDC. Cadres noirs autour des portes
  (avant, entrée arrière, porte de côté du sous-sol).
- **Toit en croupe 5/12** (fermes 5/12 du croquis de 2016) en bardeau gris foncé, débord de 16 po, fascias et soffites blancs,
  faîte à 294 po. Petite croupe sur l'entrée arrière, ventilateur de toit.
  *Le moteur n'a que des formes verticales : le toit est fait de rangs de 2 po (gradins de 4,8 po). De près, ça se lit comme
  des rangs de bardeaux.*
- **Cheminée** de brique sur le mur gauche (x -20 à 0, y 132 à 154, d'après le relevé), du sol jusqu'à 290 po.
  Couronnement de béton et conduit.
- **Perron avant** en béton sur l'excroissance du sous-sol (dessus à 98, une marche sous le seuil), 6 marches vers la rue,
  garde-corps noirs, trottoir jusqu'à l'allée. Appliques murales près des deux portes.

**Le terrain**

- **Lignes de lot** : arrière et côtés relevés au plan DAG. Devant, on a prolongé avec le plan de 1957 : marge avant de 40 pi
  (rue à y = -480), ligne droite perpendiculaire à la rue, façade du lot de 57,23 pi, ligne gauche oblique.
- **Gazon** sur tout le lot.
- **Allée** d'asphalte le long du côté droit (x 462-556, de la rue jusqu'à y = 60). Elle est *supposée* : la vidéo montre une
  allée de ce côté, et le plan de 1957 écrit « ALLÉE » près de la ligne droite.
- **Haie de cèdres** de 6 pi le long de la ligne oblique, dans la cour arrière.
- **Épinettes et bouleaux** au-delà de la ligne arrière (la vidéo montre un boisé). Un arbre sur le devant.

**Arrêts de visite dehors (pour le moteur)** : vue d'ensemble de la cour, le patio, le deck et la piscine, le cabanon et les
pas japonais, la piscine vue de la cour, la façade avant, l'allée.

### Hypothèses (à confirmer)

1. **Terrain plat à 48 po**, comme le gazon actuel du moteur (8 po sous l'allège des fenêtres du sous-sol). La vidéo montre
   pourtant une **pente** : le gazon du devant descend vers l'allée, la fondation blanche est de plus en plus haute vers
   l'arrière du côté de l'allée, et le **muret de soutènement** et la bande de roche du plan DAG laissent croire que l'allée
   est plus basse que la cour. Le moteur ne fait qu'un plan de gazon et cache tout ce qui est sous 48 po : la pente n'est donc
   pas reproduite. Le muret est dessiné comme une bordure de 18 po.
2. **Porte de côté du sous-sol** (côté allée, y ≈ 180) : son seuil est au niveau du plancher du sous-sol, 48 po sous le terrain
   supposé. On a dessiné une **descente extérieure en béton** (6 marches de 9 po, palier, murets, garde-corps), mais c'est une
   hypothèse : si l'allée descend jusqu'à cette porte, il n'y a pas de descente. Elle est sous le gazon : `EXTERIEUR["trous"]`
   dit au moteur où couper le terrain.
3. **Le « patio » est une terrasse surélevée** au niveau du palier, pas un pavé au sol. Les garde-corps de 36 po du plan
   (en vert) n'ont de sens que s'il y a une chute, et le palier y donne directement sur 5'-0" sans marche. Platelage beige
   (teinte de la vidéo ; composite ou bois à choisir). Si DAG voulait un pavé au sol, il faut une volée de plus entre le palier
   et le patio : à demander à DAG.
4. **Hauteurs** : palier, patio et deck à 97½ (49½ po du sol). La piscine a une paroi de 52 po : c'est courant, mais le modèle
   n'est pas choisi. L'escalier fait 7 contremarches de 7,07 po et des girons de 9 po mesurés au plan. **Un giron de 9 po est
   court** : le code demande au moins 235 mm (9¼ po), et 10 po est plus confortable. Il faudrait alors une volée plus longue
   (environ 60 po) : à faire vérifier par DAG.
5. **Toit** : en croupe partout, 5/12, débord de 16 po. Sur la vignette de la vidéo prise de face, le salon semble avoir un
   **pignon** au-dessus de la grande fenêtre avant : à confirmer. La hauteur de la cheminée est estimée.
6. **Fenêtres** : allège et tête lues dans les scènes d'étage (sous-sol 56-86, RDC 34-82 au-dessus du plancher), sauf les fenêtres agrandies vers le bas : leur allège propre est lue dans `maison.json` (sous-sol à 40, salon à 20). Les 5 fenêtres du sous-sol plus basses que le terrain ont une margelle (dessinée par le moteur) ; le gazon d'`EXTERIEUR` y est troué. Fenêtres noires d'après la vidéo.
7. **Perron avant** : on ne connaît ni le nombre de marches ni leur direction. Elles sont dessinées droit vers la rue.

### Code et réglementation (à valider avec la Ville et un professionnel)

- **Piscine** : le règlement québécois sur la sécurité des piscines résidentielles demande une enceinte de 1,2 m. Une porte
  d'enceinte doit avoir un **dispositif de sécurité passif** qui la referme et la verrouille toute seule (c'est la note du plan
  DAG). Les appareils doivent être à **au moins 1 m** de la paroi ou de l'enceinte : le plan les met à 3'-4", soit environ
  1,02 m, juste à la limite. Il faut aussi éviter tout ce qui permet de grimper : jupe, garde-corps, appareils.
- **Garde-corps** : 36 po (900 mm) si la chute fait moins de 1,8 m, 42 po (1070 mm) au-delà. Ouvertures de moins de 100 mm.
  Il faut une main courante dans l'escalier.
- **Cabanon** à 3'-0" des lignes de lot, mesuré au débord du toit, comme au plan : marges du règlement de zonage de
  Baie-Comeau à vérifier. Il faut un **permis** pour la piscine, le deck et le cabanon.
- **Empattements** sous le palier, le patio et le deck : sous la ligne de gel ou sur pieux vissés (note de DAG : « selon la
  capacité portante du sol »).

### Coût (ordre de grandeur, à faire chiffrer)

C'est le projet de DAG : leur soumission fait foi. Ordres de grandeur pour se repérer (Côte-Nord, 2026, posé) :

- terrasses composites (palier, patio, deck, environ 350 pi²) avec escalier et jupe : 30 000 à 50 000 $ ;
- garde-corps d'aluminium (environ 55 pi l. à barreaux et 13 pi l. de verre avec portillon) : 9 000 à 16 000 $ ;
- piscine hors-terre de 21 pi avec filtre, pompe et thermopompe : 9 000 à 16 000 $ ;
- cabanon 10' × 12' sur dalle : 9 000 à 15 000 $ ;
- roche, muret, dalles et gravier : 3 000 à 7 000 $.

### Photos à demander au client (pour remplacer les hypothèses)

1. Les **quatre façades**, de loin et bien en face : brique, fondation apparente, fenêtres, portes, cheminée.
2. Le **toit** : croupe ou pignon au-dessus du salon, couleur du bardeau, débord, gouttières.
3. Le **côté de l'allée** : pente de l'allée, **accès à la porte de côté** du sous-sol (descente ? allée au niveau ?), hauteur
   de fondation apparente aux deux coins.
4. L'**arrière** tel qu'il est aujourd'hui : porte de l'entrée arrière, ce qu'il y a dessous, niveau du sol au pied du mur,
   arbres existants.
5. Le **perron avant** : nombre de marches, direction, garde-corps.
6. Le **certificat de localisation** : lignes de lot exactes.

### Voir l'aperçu

```
EXT_APERCU=1 python3 renovation/outils/generer_3d.py renovation/MAISON-18_deux_etages
```

Les objets de l'extérieur sont alors posés dans le mobilier du sous-sol, à leur hauteur réelle. En maquette, on voit la maison
avec son toit, au milieu de son lot. En visite, on peut se poser dehors avec `poserJoueur(x, y, cap, z)`, z = sol sous les
pieds. Sur une terrasse, donner z ≈ 92 : sinon le visiteur est ramené au plancher du RDC et l'étage du sous-sol, qui porte
l'extérieur, disparaît.

Sans cette variable, rien ne change pour l'instant : `SCENE["exterieur"] = EXTERIEUR` (maquette à deux étages), et le moteur
l'ignore.

**Pour l'agent moteur** (constaté dans l'aperçu) :

- Le plafond de chaque étage (plan à hauteur H) dépasse de la maison de 60 po devant, 80 po derrière et 10 po sur les côtés.
  Dehors, ça fait des auvents blancs, à 96 po (sous-sol) et à 201 po (RDC). Il faut le couper à l'emprise quand l'extérieur
  est actif.
- Le gazon du moteur est troué au rectangle des bornes du sous-sol, qui va jusqu'à y = -47 à cause du perron. Le gazon
  d'`EXTERIEUR` bouche ce trou dans l'aperçu.
- En visite, seul l'étage courant est dessiné. Dehors, il faudra dessiner les deux étages et `EXTERIEUR`.
- `EXTERIEUR["planchers"]`, `["obstacles"]`, `["trous"]`, `["lumieres"]` et `["visites"]` (avec z) sont prêts pour marcher
  dehors.
