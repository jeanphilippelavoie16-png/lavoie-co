## Rez-de-chaussée — cuisine et salle à manger — `rdc_cuisine.py`

### Demande (2026-11-02)
> « En haut les chaises sont buggées, mets-les sous la table de cuisine. Je veux qu'on enlève le coin ordi aussi dans la
> cuisine et que tu transformes ça en beau rangement ou quelque chose d'efficace. La céramique va tout droit de la porte
> arrière, genre c'est un gros rectangle où tu as commencé à la dessiner dans la cuisine. »

Le coin café de l'entrée arrière, les laveuse-sécheuse du RDC et la porte de la salle de lavage sont traités à part
(`rdc_cafe_sdb.py`).

### Pourquoi les chaises étaient « buggées »
La fonction `chaise()` de RDC-01 (`base_rdc01_scene.py`) dessinait une **boîte** : une assise plate de 2 po et un dossier
en planche verticale de 15 × 18 po, posés à 3 po de la table (le dossier à 2 po du mur du côté gauche). Surtout, la chaise
(190, 324) **entrait de 13 po dans le buffet** (x 177,6 → 194). Les tabourets de l'îlot avaient le même dossier en
planche. Sur les photos 06 et 07, ce sont des **chaises coques** en similicuir noir à pattes de métal noir évasées.

### Ce qui change (et pourquoi)
| Élément | Proposition | Pourquoi |
|---|---|---|
| Chaises (8) | **Chaises coques** redessinées : assise 18½ × 18 po à 18¼ po du sol, dossier enveloppant incliné (≈ 6°) jusqu'à 32 po, quatre pattes noires évasées. **Rangées sous la table** : 3 par côté (axes y = 274, 295, 316), assise glissée de 17½ po sous le plateau, haut du dossier à **3½ po** du bord ; une à chaque bout, haut du dossier à 5 po du bord (assise glissée de 16 po). | Comme les vraies chaises. Contrôle dans le code (`_verifier_chaises`) : aucune chaise ne touche un pied de table (6 po et plus), la ceinture, une autre chaise (1 po et plus) ou le buffet ; rien de plus haut que 29 po ne passe sous le plateau. |
| Table | **Avancée de 8 po vers la cuisine** avec son luminaire linéaire (plateau x 210 → 256 au lieu de 202 → 248, même y). | Avec la table de RDC-01, il restait **8 po** entre le bord de la table et le buffet et 24¾ po jusqu'au mur : impossible de tirer une chaise, et la porte de la G.R. 3 frappait les chaises. Maintenant : 16 po jusqu'au buffet, 32¾ po jusqu'au mur, la porte de la G.R. 3 s'ouvre à 90° sans toucher les chaises rangées, et il reste **75 po** entre les dossiers côté cuisine et les tabourets de l'îlot. Rien à construire ; le boîtier du luminaire se déplace de 8 po. |
| Porte de la G.R. 3 | Pentures du **côté arrière** (y ≈ 288), elle s'ouvre vers la salle à manger. | Correction du relevé d'après la photo 06 : la poignée est du côté du renfoncement et les pentures sont visibles côté salle à manger. |
| Tabourets de l'îlot (3) | Même coque, hauteur comptoir (assise à 26 po, dossier court jusqu'à 36 po, repose-pieds sur trois côtés). **Glissés sous le porte-à-faux de 12 po** : l'avant de l'assise est à 1½ po du caisson, le dossier reste hors du dessus. | Assortis aux chaises, comme sur les photos 01 et 08 ; le passage entre la table et l'îlot s'élargit. |
| Coin ordi | **Enlevé** (bureau flottant, deux écrans, chaise de bureau). | Demande du client. |
| Garde-manger | **Garde-manger encastré pleine hauteur** dans le renfoncement : 42¼ po de large (du poteau à la cloison de la G.R. 3) × 29 po de profond, **face au nu du mur des G.R.** (x = 177¼, il ne dépasse pas), du plancher au plafond. Caisson et portes **noir mat** (comme la colonne d'armoires de la cuisine), portes en retrait de ¾ po dans un **cadre de bois de grange** de 1½ po (joue pleine hauteur côté dégagement, montant contre le mur, couronne de 3 po). Deux grandes portes (4 → 78 po) sur **5 tiroirs coulissants intérieurs à rebord** (environ 18 × 26 po chacun, pleine extension) ; deux portes hautes (78 → 93 po) avec une tablette pour ce qui sert peu. Longues poignées noires de 24 po, socle noir en retrait. | Le rangement qui manque le plus dans une cuisine sans garde-manger, à 3 pas de l'îlot. Environ 30 pi² de tablettes coulissantes : épicerie, collations des garçons à leur hauteur (tiroirs du bas), petits électros. Les tiroirs à rebord (pas des tablettes fixes) évitent le fond perdu de 29 po. La joue de bois de grange est ce qu'on voit en arrivant de l'entrée : elle reprend les comptoirs. |
| Thermostat | Déplacé du fond du renfoncement au mur des G.R., entre le cadre du garde-manger et le cadrage de la porte de la G.R. 3 (y ≈ 254, à 59 po). | Le garde-manger le couvrirait (électricien). |
| Tuile d'ardoise (« céramique ») | **Un seul rectangle** : du mur arrière (porte arrière) **tout droit** jusqu'à la poutre de l'axe B, x 264 → 446, y 157 → 370 (**15'-2" × 17'-9"**, environ **269 pi²**), plus l'épaisseur de la baie vers l'entrée arrière. Avant : ardoise seulement dans la pièce « Cuisine » (x ≥ 316) et une bande estimée devant la baie. **La pièce « Cuisine » devient ce rectangle** (elle prend la bande x 264 → 316 à la salle à manger et au dégagement). | Photos 01, 07 et 08 : le joint érable / ardoise part du poteau de bois brut contre le mur arrière (côté gauche de la baie) et file droit vers l'avant, à droite des chaises ; photo 02 : côté salon, l'ardoise s'arrête sous la poutre. Le joint de gauche tombe sur une ligne de carreaux (carreaux entiers le long de la salle à manger). |
| Plancher ailleurs | **Érable naturel** (plancher réel, photos 05 et 06) : salle à manger, renfoncement, dégagement. | |
| Seuils | **Réducteurs d'érable de 2¼ po** (comme sur la photo 07) le long du joint de la salle à manger (x ≈ 263, du poteau à la poutre) et du joint du salon (sous la poutre, x 272 → 446). Les anciens seuils d'inox de la maquette sont enlevés. | Barres de seuil propres, de la couleur du plancher. |

Plan P-130 : garde-manger ajouté (élément `elem-RDC-K-GM`, symbole d'armoire « G.-M. ») ; le coin ordi n'était pas
dessiné au plan ; sens de la porte de la G.R. 3 corrigé. Les pièces suivent les planchers (il n'y a pas de mur entre
elles) : **Cuisine 15'-2" × 17'-9", 269 pi²** (avant 192 pi²), **Salle à manger 9'-7¾" × 13'-10", 109 pi²** (avant 169),
**Dégagement 51 pi²** (avant 68). L'aire ouverte est la même ; seule la limite tracée change. Dans la maquette, le sol est
posé par pièce : le rectangle d'ardoise est donc le sol de la cuisine (visible aussi en mode maquette, qui ne dessine pas
les revêtements).
Maquette : arrêt « Coin bureau » remplacé par **« Cuisine — rangement »** (262, 220, cap 186 : le garde-manger, la joue de
bois de grange, la porte de la G.R. 3 et le bout de la table) ; « Salle à manger » (305, 212, cap 145) montre la table et
les 8 chaises rangées ; « Cuisine » (262, 232, cap 32) montre les tabourets glissés sous l'îlot.

### Options
- **A (proposée)** : garde-manger à portes noir mat et cadre de bois de grange, 5 tiroirs intérieurs.
- **B, vaisselier** : même caisson, mais une niche ouverte au milieu (36 → 54 po) à fond de brique et tablette de bois de
  grange éclairée (DEL), tiroirs dessous, portes dessus. Plus décoratif, environ 25 % de rangement en moins.
- **C, économique** : colonnes de garde-manger de grande surface (caissons de 24 po de profond et tiroirs intérieurs), avec
  panneaux de finition noir mat et joue de bois de grange posés sur place ; il reste 5 po de creux devant ou derrière.
- Table : si le client préfère la garder où elle est, la porte de la G.R. 3 ne s'ouvre qu'à 54° environ avant de toucher
  la première chaise du côté gauche (on tire la chaise pour ouvrir).

### Ordre de grandeur des coûts (estimation de l'agent, non soumissionnée)
Fourchettes de prix courants au Québec, non vérifiées. **À confirmer par des soumissions.**

| Poste | Fourchette |
|---|---|
| Garde-manger sur mesure 42 × 29 × 96 po, portes noir mat, 5 tiroirs intérieurs, cadre et joue de bois de grange | 3 500 – 7 000 $ |
| Option C (caissons de grande surface + panneaux et bois de grange) | 1 500 – 3 000 $ |
| Déplacer le thermostat (électricien) | 150 – 400 $ |
| Déplacer le boîtier du luminaire de 8 po (électricien, plâtre et peinture) | 150 – 400 $ |
| Réducteurs d'érable (2) | 80 – 200 $ |

### Points à valider sur place
1. **Limites de l'ardoise** : distance du mur de droite au joint de gauche (≈ 15'-2", au ras gauche du poteau contre le
   mur arrière) et du mur arrière au joint du salon (≈ 17'-9", sous la poutre). Vérifier que l'ardoise couvre bien aussi
   le passage devant la salle à manger jusqu'à la poutre (x 264 → 316, y 157 → 204 : déduit des photos 01 et 08, à valider).
2. **Renfoncement** : largeur du poteau à la cloison (≈ 42¼ po), profondeur (≈ 29 po), aplomb des murs ; prises,
   fils du thermostat et du bureau, bouche de chauffage ou de ventilation éventuelle.
3. Hauteur de plafond (96 po présumés) pour le garde-manger pleine hauteur.
4. **Table et chaises** : hauteur du dessous de la ceinture de la table (25 po présumés) et hauteur de l'assise des chaises
   (elles doivent glisser dessous) ; position réelle de la table et du boîtier du luminaire.
5. Sens réel de la porte de la G.R. 3 (pentures côté arrière d'après la photo 06).

### Ce qui reste imparfait (maquette)
- Le dossier des chaises et des tabourets est fait de tranches verticales décalées (8 et 6) : de très près, on devine les
  marches de l'inclinaison ; les ailes de la coque sont verticales.
- La texture d'ardoise est calée sur le repère de la maison : carreaux entiers au joint de la salle à manger, mais une rangée
  coupée de 11 po sous la poutre et de 10 po au mur arrière (calepinage réel inconnu).
- L'intérieur du garde-manger (tiroirs) n'est pas modélisé : portes fermées.
