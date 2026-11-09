## Chute à linge — de la salle de bain du haut à la salle de lavage — `chute_linge.py`

### Demande (client, 2026-11-02)
> « dans la salle de bain en haut où on a enlevé la laveuse sécheuse, c'est-tu possible de faire une drop pour envoyer du
> linge dans la salle de lavage? pi j'aimerais que ça soit possible de l'essayer sur notre outil. »

### Réponse courte
**Oui, c'est possible, et c'est dessiné.** L'option B de l'étude (`DESIGN_cafe_sdb.md`, « Étude de la chute à linge ») devient
le parti pris. Elle dépend de **3 choses à vérifier sur place** avant de commander quoi que ce soit (voir « Conditions »),
parce que la salle de lavage n'est sous la salle de bain que sur une bande de 8¾ po. Dans la visite 3D, on l'essaie avec le
bouton **« Envoyer du linge »** (aux deux étages) ou en touchant la trappe, puis **« Voir arriver au lavage »**.

### Le trajet du linge (de haut en bas)
1. **Trappe** (salle de bain, RDC) : dans le module de gauche de la colonne d'apothicaire, une trappe basculante **noir mat**
   avec **« LINGE » en lettres de laiton**. On la tire, elle bascule de 35° (charnière en bas), on dépose le linge, on la
   lâche : elle se **referme toute seule** (ressort et amortisseur).
2. **Gaine** : tôle d'acier galvanisé, **12 × 14 po à l'intérieur**, au fond du module de gauche, **encoffrée** dans la colonne
   (on ne la voit pas), de la trappe jusqu'au plancher.
3. **Plancher** : la gaine passe **entre deux solives** (2 × 10 parallèles à y, 20 po c/c) et se **décale de 5¼ po vers
   l'avant** (sous la cloison du fond de la salle de bain) pour sortir **devant la poutre maîtresse** 8 × 10 (y 153 → 161).
4. **Sous-sol** : sortie au plafond de la salle de lavage (12 × 14 po, x 77,6 → 89,6, y 139 → 153), avec une collerette
   d'inox et un **coude-déflecteur d'inox brossé Ø 14 po, apparent** (pas d'encoffrement : il est au-dessus d'une porte et
   d'un coin de service). Il descend en pente de 32 à 40° vers la gauche, **passe au-dessus de l'arc de la porte du lavage**
   (son dessous est à **≈ 83 po** au droit de la porte, qui fait 80 po) et finit par un **bec vertical à 69 po** au-dessus
   du chariot, 27 po plus loin.
5. **Chariot à linge** : cadre d'acier noir sur 4 roulettes, **sac de toile écrue** amovible. Le linge tombe dedans ; on
   roule le chariot jusqu'à la laveuse (≈ 10 pi).

### Dimensions
| Élément | Dimensions | Détail |
|---|---|---|
| Trappe | façade 14½ × 19 po, de **33 à 52⅓ po** du plancher | Noir mat comme la colonne ; lettres « LINGE » de laiton (1,9 po) ; poignée-coquille noire en haut ; **loquet de sécurité pour enfants à double action** (pousser puis glisser) en haut à droite, à ≈ 51 po ; trémie à joues derrière la façade |
| Bouche (ouverture dans le caisson) | **12 × 12 po**, seuil à **40 po** | Exigé : 36 po ou plus ; ouverture de 12 po au plus |
| Gaine | 12 × 14 po intérieur, ≈ 40 po de haut + plancher | Tôle galvanisée calibre 26 ; joints à recouvrement dans le sens de la descente, rivets à tête lisse (rien qui accroche) |
| Décalage dans le plancher | 5¼ po vers l'avant, dans une baie de solives | Aucune solive coupée, pas de chevêtre si la baie est libre |
| Sortie au plafond du lavage | 12 × 14 po | Collerette d'inox (16 × 16 po) ; plafond de 2 gypses ⅝ X refait autour |
| Coude-déflecteur | Ø 14 po, 27 po de déport, pente 32 à 40° | Inox brossé, 2 suspentes noires ; dessous à ≈ 83 po au-dessus de l'arc de la porte ; bec vertical à 69 po, fond noir |
| Chariot | **20 × 14 × 33 po**, sac de 19 po de creux (≈ 3 pi³, une brassée) | Acier noir, roulettes, sac de toile écrue amovible et lavable, suspendu au cadre |
| Durée (dans la visite) | trappe ouverte en 0,6 s, ballot au chariot ≈ 1,8 s après le clic, trappe refermée à ≈ 1,9 s | |

### La colonne d'apothicaire, réorganisée autour de la trappe (`rdc_cafe_sdb.py`)
Même meuble (29½ × 24 × 96 po, caisson noir mat, façades de bois de grange), même esprit, un peu moins de modules :

| Hauteur | Gauche | Droite |
|---|---|---|
| 0 → 4 po | socle en retrait | socle en retrait |
| 4 → 33 po | **porte basse à loquet enfant** (noir mat) : produits ménagers sur une tablette de 8 po devant la gaine ; accès à la gaine pour la nettoyer | **panier basculant** (noir mat) : délicats et ce qui ne va pas dans la chute |
| 33 → 52⅓ po | **trappe de la chute « LINGE »** | **2 tiroirs de bois de grange : un par garçon** (à leur hauteur) |
| 52⅓ → 62 po | **tiroir de bois de grange** (un parent) | **tiroir de bois de grange** (l'autre parent) |
| 62 → 84 po | **niche éclairée** : 9 serviettes roulées cordées comme du bois de chauffage (inchangée) | |
| 84 → 96 po | armoire du haut : **pharmacie, hors de portée des enfants**, et réserves | |

Un tiroir par membre de la famille (porte-étiquettes noirs), comme avant ; on passe de 2 paniers et 6 tiroirs à 1 panier,
4 tiroirs, la trappe et une porte basse. La trappe noire au milieu de la colonne, avec ses lettres de laiton, devient le
détail qu'on remarque.

### Sous-sol : où va le chariot, ce qui ne bouge pas
- Chariot **x 47 → 67, y 140 → 154**, contre le mur du fond (la poutre), **entre le chauffe-eau et l'arc de la porte** :
  2 po du devant du chauffe-eau, **12¾ po du bout de la porte grande ouverte** (la porte ne le touche pas).
- **Panneau électrique** : son dégagement de 1 m (x 10 → 49, y ≈ 94 → 124) reste vide.
- **Chauffe-eau** : rien de fixe devant ; on tire le chariot de côté pour l'entretien.
- **Passage** porte → laveuse : 23 po entre le coin du chariot et le coin du congélateur, sur un pas (comme avant, la pièce
  est serrée à cet endroit).
- **Rien du lavage n'est déplacé** et aucun module du sous-sol n'est modifié : le chariot loge dans un coin libre, le
  déflecteur est au plafond.

### Conditions à valider sur place (avant de commander)
On ouvre une trappe de 12 × 12 po dans le gypse du plafond du lavage, sous la colonne, et on regarde :
1. **La cloison du fond de la salle de bain** (`mur-RDC-R01`) est-elle bien à y ≈ 142 (photos) ? Au plan de 1957 elle est sur
   la poutre (y ≈ 157) : **dans ce cas, la salle de lavage n'est plus dessous et la chute n'est pas faisable ici.**
2. **Les solives** : bien parallèles à y, une baie libre d'au moins 13 po entre x ≈ 76 et 92, **sans conduit** dedans
   (renvoi et entrées d'eau de l'ancienne laveuse, fils, conduit de chauffage ou de la sécheuse).
3. **La poutre maîtresse** : sa face avant à y ≈ 153 ou moins, pour que la sortie tombe devant elle.
4. Hauteurs au lavage : plafond à ≈ 96 po et porte de 80 po (jeu de ≈ 3 po sous le déflecteur).

### Code et sécurité (à valider avec la Ville de Baie-Comeau et un professionnel)
- **Une seule famille, un seul logement** : la partie 9 du Code de construction du Québec (chapitre I, CNB 2015 modifié Québec)
  n'exige pas de séparation coupe-feu entre le rez-de-chaussée et le sous-sol d'un même logement, et ne prévoit rien de
  propre aux chutes à linge d'une maison (celles des grands bâtiments relèvent de la partie 3, sous-section 3.6.3). À
  confirmer au permis de rénovation.
- **Si le sous-sol devenait un logement distinct** (logement accessoire, bigénération, location) : le plancher devient une
  séparation coupe-feu et une ouverture non protégée n'y est pas permise. La chute serait **condamnée** (gaine obturée,
  2 gypses X refaits au plafond et dans la colonne : le plus simple) ou refaite avec une gaine coupe-feu et un dispositif
  d'obturation homologué à fermeture automatique à chaque bout (coûteux).
- **Fumée** : la gaine relie les deux étages ; la trappe se referme seule. Avertisseurs de fumée reliés aux deux étages
  (déjà prévus) ; en ajouter un près de la salle de lavage s'il n'y en a pas.
- **Enfants (4 et 6 ans)** : seuil à 40 po, ouverture de 12 po au plus (on ne passe pas la tête et les épaules), trémie à
  joues (on ne voit pas le vide), loquet à double action en haut, fermeture automatique. Ne pas ranger de marchepied devant
  la colonne. Règle de la maison : **on n'envoie que du linge mou** (pas de souliers, de jouets, de ciseaux) et personne ne
  joue sous le bec au sous-sol.
- **Hygiène** : pas de serviettes mouillées dans la chute (moisissure) ; la porte basse donne accès au bas de la gaine pour
  la nettoyer.
- **Bruit** : la gaine laisse passer un peu le bruit du lavage ; joint d'étanchéité sur le pourtour de la trappe.

### Coût (ordre de grandeur ; estimation du designer, prix courants au Québec 2025-2026, même base que `DESIGN_cafe_sdb.md`, non soumissionnée : à confirmer par 2 ou 3 soumissions d'un ferblantier et d'un menuisier à Baie-Comeau)
| Poste | Fourchette |
|---|---|
| Gaine de tôle galvanisée sur mesure, décalage, collerette (ferblantier) | 500 – 1 000 $ |
| Coude-déflecteur d'inox brossé Ø 14 po sur mesure, suspentes | 400 – 900 $ |
| Trappe basculante : quincaillerie à fermeture amortie, loquet enfant, joint, lettres de laiton | 250 – 600 $ |
| Ouverture du plancher entre solives, gypse du plafond (2 couches X), peinture | 400 – 900 $ |
| Module de gauche de la colonne adapté (si la colonne est fabriquée avec) | 0 – 400 $ |
| Chariot à linge roulant (acier noir, sac de toile) | 80 – 250 $ |
| **Chute à linge** | **≈ 1 600 – 4 000 $** |

L'étude donnait « + 1 500 à 3 500 $ » ; l'écart vient du déflecteur d'inox apparent et du chariot.

### Dans l'outil (visite 3D)
- **« Envoyer du linge »** : au RDC, on est amené devant la colonne si on est loin, la trappe bascule, un ballot de linge
  froissé (drap, jeté vert sauge, chandail gris dont une manche dépasse) y est posé, part, culbute dans la gaine, sort au
  plafond du lavage, glisse dans le déflecteur et tombe dans le chariot ; la trappe se referme. On peut aussi **toucher la
  trappe**. Les ballots s'empilent (3 au plus) ; au 4e envoi, le chariot est vidé.
- **« Voir arriver au lavage »** (après l'envoi) : amène au sous-sol, vue sur la sortie, le déflecteur et le chariot, et
  rejoue l'arrivée. Au sous-sol, le bouton « Envoyer du linge » est là aussi.
- Arrêts de visite : **« Chute à linge »** (RDC, devant la colonne, après « Salle de bain — rangement ») et **« Chute à
  linge — arrivée au lavage »** (sous-sol, après « Congélateur (salle de lavage) »).
- Palette : lignes « Salle de bain » et « Salle de lavage » complétées.

### Plans
- **P-130** : symbole de la gaine (boîte à croix) **« CHUTE »** dans la colonne (`elem-RDC-S-CHUTE`).
- **P-129** : sortie et déflecteur **en pointillé** (au plafond) **« CHUTE »** (`elem-SS-S-CHUTE`) ; note 2 de la proposition :
  « Chute à linge (salle de bain du haut → plafond du lavage) : déflecteur inox, chariot ; cloison, solives et coupe-feu à
  valider. » Le chariot, meuble roulant, n'est pas dessiné (comme les autres paniers).
- **Note proposée pour le cartouche de P-130** (les 6 notes sont fixées dans `modifs.py`, pas dans ce module) :
  « Salle de bain : colonne d'apothicaire avec chute à linge vers la salle de lavage (trappe à 40 po, loquet enfant ; à valider). »

### Ce qui reste imparfait
- Tout repose sur la cloison du fond estimée (y ≈ 142) et sur des solives qu'on n'a pas vues.
- Dans la 3D, la gaine et le décalage dans le plancher ne se voient pas (ils sont cachés, comme en vrai) ; le ballot n'a pas
  d'ombre ; la trémie à joues derrière la trappe n'est pas modélisée (on voit une bouche noire).
- Le chariot n'est pas un obstacle dans la visite (on le traverse, comme les autres meubles).
- Le ballot est un peu petit (≈ 9½ po) pour tenir dans le sac sans en traverser les parois ; dans les captures, un léger
  halo sombre l'entoure quand il tombe (vu en rendu logiciel, cause non cherchée).
- Avec `ETAGE=RDC` ou `ETAGE=SS` (exports d'un seul étage), il n'y a pas de séquence : la trappe reste fermée et le
  déflecteur et le chariot n'existent pas au sous-sol.
