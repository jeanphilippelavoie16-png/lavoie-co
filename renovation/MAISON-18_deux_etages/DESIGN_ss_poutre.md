## Sous-sol — la poutre du hall rentre dans le mur ; chambre 1 et salle de bain agrandies

Modules : `base_ss16_modifs.py` (murs, portes, pièces, éléments du plan), `base_ss16_scene.py` (salle de bain, hall,
lingerie, lumières, arrêts), `zone_chambre1.py` (bureau, vestibule), `zone_global.py` (veilleuses, marchepied, grille
d'évacuation), `ss_scene.py` (ordre des arrêts), `ss_modifs.py` (note de la feuille P-129).

### Demande du client (2026-11-02)

> « Dans le sous-sol, côté chambre du fond, y'a une poutre devant la porte qui a comme pas rapport. Donne l'espace à la
> chambre, tant qu'à avoir juste une poutre dans le milieu de nulle part. Et j'aimerais que la salle de bain soit un peu
> plus grosse : prendre un peu d'espace dans la chambre et l'aménager en fonction qu'on ajoute de l'espace grâce à
> l'espace de la poutre. »

### Ce qu'on a vérifié

Sur le plan P-129 et dans la 3D d'avant :
- **La poutre.** C'est la poutre arrière `str-SS-P01`, une poutre de 8 × 10 po à y = 204. Sa retombée occupe y 199 → 209
  et son dessous est à ≈ 86 po.
- **Ce qui la rendait gênante.** Elle traversait le hall à 26 po devant la porte de la chambre 1. Elle laissait la colonne
  `C02` (x = 228) seule entre le hall et le vestiaire. La colonne `C01` (x = 146) dépassait du mur de la salle de bain.
- **Le hall.** Il faisait 40,5 pi², dont une bande de 26 po derrière la poutre qui ne servait qu'à la porte de la chambre.

### Programme

1. Mettre la cloison hall / chambre sous la poutre, pour que la retombée et les colonnes disparaissent dans le mur.
2. Donner à la chambre 1 la bande du hall derrière la poutre.
3. Garder un vrai hall qui dessert :
   - la salle de bain (elle n'est jamais accessible par une chambre) ;
   - la chambre 1 ;
   - le gym ;
   - la chambre 2 et le vestiaire, comme avant.
4. Agrandir la salle de bain avec une partie de la chambre. La chambre doit garder au moins ses 199,2 pi², son lit queen
   avec ses dégagements, son rangement et ses deux fenêtres d'évacuation.
5. Réaménager la salle de bain dans le même esprit : bain vedette, travertin, chêne, noir mat, béton poli. Ni céramique
   ni tuile verte.

### Parti pris

**1. Le mur de la poutre**
- `mur-SS-P06` passe à y = 204 et fait **11 po d'épais**. C'est une ossature de 2x4 de chaque côté de la poutre et des
  colonnes, avec du gypse sur les deux faces.
- La retombée et les colonnes `C01` et `C02` disparaissent dedans : dans le hall, le plafond est plat et on ne voit
  plus de colonne.
- On utilise l'épaisseur du mur :
  - **la porte de la chambre 1** a une embrasure de chêne de 11 po ;
  - **une lingerie encastrée** donne sur le hall, entre `C01` et la porte : 34 po de large, 7½ po de profond, deux portes
    de chêne affleurantes qui s'ouvrent par pression, sous la retombée (3½ → 82 po). On y range les serviettes roulées,
    le papier et les savons, juste à côté de la salle de bain.

**2. Le hall**
- Il fait **40½ po de large** (y 158 → 198½), entre 36 po minimum et 42 po confortable.
- Il dessert quatre accès :
  - au bout ouest, la salle de bain ;
  - au fond, la chambre 1 ;
  - en face, le gym par sa porte coulissante vitrée (inchangée) ;
  - à l'est, le vestiaire et la chambre 2, ouverts comme avant.
- Il reste deux veilleuses ambre au pied du mur, une à chaque bout.

**3. La chambre 1**
- Elle reprend la bande du hall. L'ancien recoin du bureau devient un petit **vestibule d'entrée** de 49½ × 42¾ po.
- La porte est pentée côté ouest et s'ouvre contre le mur de la douche.
- Dans le vestibule, sur le mur de la chambre 2 : trois patères de chêne à 44 po (sac, robe de chambre) et une veilleuse.
- Le **bureau** passe sur le mur de la salle de bain, à l'est du pied du lit. C'est le même plateau de chêne de
  52½ × 20 po sur crémaillères noires, sans pattes : le tapis passe dessous.
- Ce qui ne bouge pas :
  - le mur de rangement bleu brume, avec la penderie et les tablettes ;
  - la niche du lit queen ;
  - les dégagements de 27¾ po de chaque côté du lit et de plus de 8 pi au pied ;
  - le coin lecture ;
  - les deux fenêtres d'évacuation, avec le plancher libre devant.

**4. La salle de bain**
- Elle prend le coin de l'ancien recoin, derrière le mur de la poutre :
  - `mur-SS-P04` est raccourci (y 157 → 204) ;
  - `mur-SS-P05` est prolongé jusqu'à x = 186 ;
  - un nouveau mur, `mur-SS-P15`, sépare la douche de l'entrée de la chambre.
- **Douche à l'italienne de 38 × 69 po**, au lieu de 36 × 48 po :
  - elle est logée dans l'épaisseur gagnée, derrière le mur de la poutre ;
  - on y entre sous la retombée par une ouverture libre de 24 po (pierre à pierre), entre le muret et le coin du mur, sans porte ni marche ;
  - la pomme pluie noire est au fond, à plus de 18 po de l'entrée ;
  - le mitigeur et la douchette sont sur le muret, juste à l'entrée : on ouvre l'eau sans se mouiller ;
  - un banc de travertin est au fond (assise à 17½ po), pratique pour laver le petit ;
  - une tablette éclairée au-dessus est hors de portée des enfants ;
  - un drain linéaire court le long du mur de la chambre ;
  - c'est du travertin plancher au plafond, la même pierre que le bain.
- **Le bain reste la vedette.** Le muret `mur-SS-P14` passe de x = 48¼ à x = 112¼, ce qui élargit l'alcôve :
  - elle va de 88½ à 98½ po de pierre à pierre ;
  - la pierre couvre trois côtés : le mur de fondation, le fond et le muret ;
  - elle est toujours encadrée par la retombée de la poutre ;
  - le bain sculptural est centré, avec 16¼ po de chaque côté et la niche éclairée dans son axe ;
  - on garde le robinet sur pied noir mat, la suspension globe et le plateau de chêne ;
  - on ajoute un porte-serviette noir sur la pierre, à portée de main.
- **Vanité double de 60 po** au lieu de 36 po, sur le mur du lavage :
  - chêne suspendu, quartz, deux vasques, deux mitigeurs noirs ;
  - deux miroirs ronds et trois appliques ;
  - le marchepied des garçons est rangé dessous, et la DEL de nuit court sous la vanité.
- **La toilette suspendue** passe près de la fenêtre :
  - 17½ po de son axe au mur et à la vanité ;
  - 22 po libres devant.
- **La porte devient battante pleine** au lieu de coulissante. Le mur `P04` est maintenant trop court pour un rail.
  - Elle est pentée côté avant et s'ouvre contre le mur du lavage, où sont les crochets des garçons.
  - Son arc ne touche ni la vanité ni la toilette.
  - L'interrupteur, à 42 po, est sur le coin du mur de la poutre, côté poignée.
- **Ventilation.** La grille d'évacuation (VRC ou ventilateur à hygrostat) passe au plafond de la douche.

### Avant / après (superficies au nu des cloisons, tableau_pieces.csv)

| Pièce | Avant | Après | Écart |
|---|---|---|---|
| Chambre 1 | 199,2 pi² (18,5 m²) | **200,9 pi² (18,7 m²)** | + 1,7 pi² |
| Salle de bain | 78,2 pi² (7,3 m²) | **89,9 pi² (8,4 m²)** | + 11,7 pi² (+ 15 %) |
| Hall | 40,5 pi² (3,8 m²), 69¾ po de profond | **23,5 pi² (2,2 m²)**, 40½ po de large | − 17,0 pi² |
| Vestiaire | 109,2 pi² | 106,3 pi² | − 2,9 pi² (coin derrière l'ancienne colonne C02) |

Ce qu'on fait des 17 pi² enlevés au hall et des 3 pi² enlevés au vestiaire :
- la salle de bain prend 11,7 pi² ;
- la chambre gagne 1,7 pi² ;
- le reste (≈ 6 pi²) va dans le mur épais qui avale la poutre et les colonnes.

Ce que chaque pièce y gagne :

| Élément | Avant | Après |
|---|---|---|
| Douche | 36 × 48 po | **38 × 69 po** (+ 50 %) |
| Vanité | 36 po, 1 vasque | **60 po, 2 vasques** |
| Alcôve du bain | 88½ po | **98½ po** |
| Rangement | — | lingerie encastrée de 34 po |
| Chambre | — | un vestibule ; aucune colonne ni retombée devant la porte |

### Ce qui change dans les fichiers

- **Plan P-129.**
  - Murs `P04`, `P05`, `P06` (11 po), `P07` (prolongé jusqu'au mur de la poutre), `P14` (déplacé) et `P15` (nouveau).
  - La porte `ouv-SS-P03` devient battante ; la porte `ouv-SS-P05` passe dans le mur épais.
  - La coupe hall / vestiaire s'arrête au mur.
  - Éléments refaits : bain, douche avec son banc, toilette, vanité double avec deux lavabos, lingerie, bureau de la
    chambre 1.
  - La note 2 de la feuille est mise à jour.
- **3D.**
  - Salle de bain refaite.
  - Embrasure de chêne de la porte de la chambre, lingerie du hall.
  - L'habillage de chêne de `C02` est retiré, puisqu'elle est dans le mur.
  - Veilleuses, marchepied, interrupteur et grille déplacés ; bureau et vestibule de la chambre.
  - Arrêts nouveaux ou déplacés :
    - « Hall — le mur de la poutre » ;
    - « Douche à l'italienne (derrière la poutre) » ;
    - « Chambre 1 — l'entrée sous la poutre » ;
    - « Salle de bain (entrée) », « Le bain (alcôve de pierre) », « Vanité », « Chambre 1 — la niche de près ».
- **Les drains existants** (`elem-SS-DR-BAIN` et `elem-SS-DR-WC`, x 28 et 55 à y = 203) restent dessinés où ils sont
  aujourd'hui.

### Coûts (ordre de grandeur, Québec 2026, à confirmer par soumissions)

| Poste | Fourchette | Source |
|---|---|---|
| Douche à l'italienne complète (référence) | 5 000 à 9 000 $ en standard, 6 500 à 9 500 $ en milieu de gamme, 11 000 $ et plus en luxe | [Soumission Rénovation, *Prix d'une rénovation de douche italienne au Québec*, modifié le 12 mai 2026](https://soumissionrenovation.ca/fr/blogue/quel-est-le-prix-dune-renovation-de-douche-italienne-au-quebec) |
| Drain linéaire / membrane d'étanchéité | 500 à 1 000 $ (sans pose) / 600 à 1 200 $ | même source |
| Plombier | 70 à 130 $ l'heure | même source ; [*Déplacer la plomberie d'une vanité*, modifié le 28 avril 2026](https://soumissionrenovation.ca/fr/blogue/deplacer-la-plomberie-dune-vanite-au-quebec-prix-et-couts-en-2026) |
| Pierre naturelle au mur / comptoir de granite | ≈ 10 $/pi² (matériau) / 40 à 150 $ le pied linéaire | [*Coût d'une rénovation de salle de bain*, modifié le 3 mars 2026](https://soumissionrenovation.ca/cout-dune-renovation-de-salle-de-bain) |
| **Écart, douche 38 × 69 au lieu de 36 × 48** (≈ 35 pi² de pierre et de membrane de plus, drain plus long, banc) | + 2 000 à 4 500 $ | estimation du designer d'après les lignes ci-dessus |
| **Drains dans la dalle** : trait de scie, tranchée, ABS, recoulage et repolissage, sur ≈ 12 pi de plus qu'en SS-16 | + 1 500 à 3 500 $ | estimation du designer ; la source dit seulement que briser une dalle coûte « nettement » plus cher, et conseille 10 à 15 % d'imprévus |
| **Vanité double de 60 po** sur mesure en chêne et quartz, 2e vasque et robinet, au lieu de 36 po | + 1 500 à 3 000 $ | estimation du designer |
| **Mur épais sous la poutre** (au lieu d'une cloison 2x4) et embrasure de chêne | + 800 à 1 800 $ | estimation du designer |
| **Lingerie encastrée**, 2 portes de chêne affleurantes | 600 à 1 500 $ | estimation du designer |
| Porte battante pleine au lieu de coulissante à rail apparent | ≈ 0 $ (− 200 à + 200 $) | estimation du designer |
| **Total de l'écart par rapport à la version précédente** | **≈ + 6 400 à 14 300 $** | les murs sont tous neufs dans les deux versions : rien à démolir |

### Points à valider (avec la Ville de Baie-Comeau et un professionnel)

- **La poutre.**
  - Mesurer sa hauteur réelle et la cote de son dessous. Le plan suppose ≈ 86 po (7'-2") sous une poutre de 8 × 10.
  - Les portes de 80 po passent dessous avec 6 po pour le linteau.
  - Le mur ne porte rien : il enveloppe la poutre sans la toucher. Le dessus de l'ossature est fixé de côté, pas
    sous la poutre.
- **Les colonnes.**
  - `C02` est « douteuse » : selon le croquis de 2016, elle aurait été retirée. Confirmer sur place.
  - `C01` et `C02` restent en place dans le mur et ne doivent pas être coupées. On ne déplace aucun appui.
  - Fermer une colonne de bois dans une cloison est courant ; la résistance au feu se fait avec le gypse.
- **Les drains.** Toilette, bain et douche sont tous déplacés par rapport aux drains d'origine (x 28 et 55 à y = 203) :
  - la toilette, d'environ 3 pi ;
  - le bain, d'environ 3½ pi ;
  - la douche, sur une nouvelle branche d'environ 12 pi sous la dalle, avec un drain linéaire.
  - Un plombier doit confirmer la pente, le diamètre et l'évent avant de couper la dalle. C'était déjà le cas en SS-16.
- **La ventilation.** La douche est fermée sur trois côtés et sans fenêtre :
  - il faut une évacuation au plafond de la douche, sur le VRC ou un ventilateur à hygrostat d'au moins 50 pi³/min,
    évacué dehors ;
  - un encastré étanche ;
  - une membrane continue sous la pierre, un drain linéaire et une pente de ¼ po/pi.
- **La hauteur sous la poutre.** Elle est de ≈ 86 po à l'entrée de la douche, au-dessus du bain et dans l'embrasure de la
  porte de la chambre. Au-dessus de ≈ 1,95 m, c'est correct, mais il faut la mesurer.
- **Les fenêtres d'évacuation de la chambre 1.** Inchangées ; leur ouverture reste à vérifier (voir DESIGN_ss_chambres.md).

### Décisions demandées au client

1. **Douche sans porte**, entrée libre de 24 po. On peut ajouter une porte vitrée pivotante d'environ 600 à 1 200 $.
2. **Porte de salle de bain battante** au lieu de coulissante. Le mur est maintenant trop court pour un rail.
3. **La lingerie dans le hall**, ou rien à cet endroit (le mur reste lisse).
4. **Le bureau du petit sur le mur de la salle de bain**, ou un bureau libre ailleurs dans la chambre.
5. **Vanité double de 60 po** (deux vasques), ou une vanité de 48 po avec une tour de rangement.
