# Projets de rénovation — 86, avenue Laurier

## Règle
- **Plans de base** : `releve/livrables/` (relevé de l'existant R0, figé au commit `59ac401`). On ne les modifie **jamais**
  pour un projet.
- **Chaque projet** est un dossier ici, `renovation/<code>_<nom>/`, construit à partir d'une **copie** de la base.
  Pour une nouvelle version, on copie le dossier du projet (ex. `SS-01` → `SS-02`) et on modifie la copie.

## Contenu d'un projet
- `modifs.py` : les changements par rapport à la base (murs projetés, portes, pièces, équipements).
- `donnees/maison.json`, `svg/`, `pdf/`, `png/`, `dxf/`, `donnees/tableau_pieces.csv` : générés.

## Régénérer
    python3 renovation/outils/construire_projet.py renovation/SS-01_amenagement_sous-sol

## Projets
| Code | Projet | État |
|---|---|---|
| SS-01 | Aménagement du sous-sol : 2 chambres, grande salle de bain, salon / salle de jeu, salle d'entraînement, salle d'utilité | esquisse |
| SS-02 | Copie de SS-01 : aire ouverte, salle d'entraînement vitrée, direction de design, maquette 3D visitable (`3d/visite.html`) | esquisse |
| SS-03 | Copie de SS-02 : grande salle de bain à double vanité, cuisine en ligne, caveau en rangement, buanderie (skill designer-interieur) | esquisse |
| SS-04 | Copie de SS-03 : escalier vers le rez-de-chaussée (emplacement de 1957), coin bar avec lavabo et frigo (plus de salle à manger), vraie salle de lavage, peinture et textures | esquisse |
| SS-05 | Copie de SS-04 : salle de bain revue (toilette contre le mur, bain en coin, douche de 6 pi), matériaux réels dans la maquette | esquisse |
| SS-06 | Copie de SS-05 : nouvel escalier (emplacement dessiné sur A-101, en haut et en bas), sous-sol repensé autour d'un hall central, bain sur pied, gym (tapis roulant, vélo de route sur base, poids au sol) ; feuilles P-105 et P-106 | esquisse |
| SS-07 | Copie de SS-06 : vestiaire à la place du coin bar, coin frigo dans le séjour, escalier à 3 marches tournantes en haut, tapis roulant dans le sens du vélo ; feuilles P-107 et P-108 | esquisse |
| SS-08 | Copie de SS-07 : escalier en L, palier dans le coin arrière (étude de 3 implantations dans DESIGN.md) ; feuilles P-109 et P-110 | esquisse |
| SS-09 | Copie de SS-08 : escalier déplacé à l'est de la fenêtre de la chambre 1 (étude 2), chambre 1 agrandie ; feuilles P-111 et P-112 | esquisse |
| SS-10 | Copie de SS-09 : **escalier à l'entrée avant (option 2, choisie)**, vestibule commun en haut, sous-sol refait (chambre 1 pleine largeur, mur télé sur la cage), vrais modèles 3D ; feuilles P-113 et P-114 | esquisse |
| SS-11 | Copie de SS-10 : petit frigo sous comptoir (coin café) au sous-sol, salle de bain du haut agrandie de 1½ pi vers la chambre avant ; feuilles P-115 et P-116 | esquisse |
| SS-12 | Copie de SS-11 : escalier flottant (limon acier, marches de chêne, garde vitrée), séjour épuré (sofa + télé), bureau commun entre les chambres ; feuilles P-117 et P-118 | esquisse |
| SS-13 | Copie de SS-12 : salle de bain refaite (porte depuis le hall, vanité simple, douche de 7 pi, bain sur pied), salle de lavage revue (laveuse à chargement par le dessus, bac dégagé, comptoir de pliage), coin lecture et travail ouvert ; feuilles P-119 et P-120 | esquisse |
| SS-14 | Copie de SS-13 : coin lecture avec pouf et petite bibliothèque basse, bac de la salle de lavage encastré dans le comptoir de pliage en L ; feuilles P-121 et P-122 | esquisse |
| SS-15 | Copie de SS-14 : plus de coin commun, les deux chambres agrandies, le caveau devient le walk-in de la chambre 2 ; rampe de métal côté séjour (verre gardé côté gym), rangement sous l'escalier, divan en L avec projecteur et toile ; feuilles P-123 et P-124 | esquisse |
| SS-16 | Copie de SS-15 : salle de bain refaite autour du bain (bain sculptural centré dans une alcôve de travertin chaud, niche éclairée, suspension), douche simple 36 × 48, béton poli dans tout le sous-sol ; dessous de l'escalier dégagé (plus de rangement), projecteur au plafond, toile motorisée de 120 po centrée qu'on monte et descend dans la visite, walk-in du caveau isolé (évents fermés), galerie de 6 photos de famille au séjour, robinetterie corrigée ; feuilles P-125 et P-126 | esquisse |
| SS-17 | Par-dessus SS-16 (un module par zone) : chambres des garçons de 4 et 6 ans avec lits queen et rangement intégré (« Le socle de chêne », « La bibliothèque secrète » avec porte pivotante vers le walk-in), banc-cabane cinéma sous l'escalier, gym refait (cardio contre le mur, mur-miroir, banc-coffre), casiers d'hiver au vestiaire, banc à jouets sous la toile, trajet de nuit ; feuilles P-127 et P-128 | esquisse |
| MAISON-18 | Les deux étages réunis en une maquette où l'on monte et descend : sous-sol de SS-17 allégé (chambres moins meublées) ; rez-de-chaussée réaménagé sur le relevé RDC-01 : grande entrée vitrée avec l'escalier et du rangement, chambre des parents avec lit king, bureau-gaming à 2 postes face à la fenêtre avant, bugs corrigés ; portes interactives ; extérieur (maison vue de dehors, cour arrière du plan DAG) où l'on marche et entre par les portes ; feuilles P-129 et P-130 | esquisse |

## Études
- `etudes/escalier/` : six emplacements possibles pour l'escalier, en haut et en bas (étude 3).

## Maquette 3D
    python3 renovation/outils/generer_3d.py renovation/<projet>
Lit `donnees/maison.json` et `scene_3d.py` (matériaux, peinture, mobilier, éclairage, arrêts de visite) du projet.
La visite est pensée pour une tablette à l'horizontale : toucher le plancher ou le petit plan pour y marcher (chemin
automatique par les portes), glisser pour regarder, ◀ ▶ pour la visite guidée, liste des pièces à gauche, maquette sans
plafond (un doigt tourne, deux doigts zooment) ; toucher un objet animé ou mobile le fait bouger (voir « Toucher les objets »). Les escaliers projetés (`etat: nouveau`) sont modélisés avec leur trémie ;
`peinture` / `accents` dans `scene_3d.py` colorent les murs pièce par pièce. Les visites déjà publiées de SS-02 et SS-03
gardent l'ancienne visionneuse tant qu'on ne les régénère pas.

Rendu (bouton **Haute / Normale** en haut ; Haute par défaut, une tablette lente passe seule en Normale) : image rendue
dans une cible multi-échantillonnée puis finie par passes (occlusion ambiante, halo des sources claires, vignette) ;
encastrés 3000 K et lumière du jour bleutée par les fenêtres, attribués aux sources les plus proches du visiteur (nombre
de lumières fixe, avec fondu) ; ombres douces des encastrés les plus proches ; vernis (clearcoat) des planchers, comptoirs
et céramiques et duvet (sheen) des tissus ; ciel et terrain vus par les fenêtres (`sol_exterieur` dans `scene_3d.py`,
en pouces ; par défaut 8 po sous l'allège au sous-sol, -30 ailleurs). Un matériau du catalogue peut donner son fini :
`vernis`, `vernis_rugosite`, `duvet`. Normale coupe les ombres, l'occlusion, le halo et les finis.

Commandes interactives (facultatif : toile motorisée, stores, porte de garage...) : `SCENE["commandes"]` =
`[{"id": "toile", "nom", "libelle_bas", "libelle_haut", "pivot_z", "fraction_min": 0.03, "depart": "haut", "duree": 3.0}]`
(`pivot_z` = z du haut de la partie mobile, c.-à-d. le bas du boîtier). Les objets du mobilier liés portent
`"commande": "toile"` et `"anim": "etirer"` (défaut : se déroule depuis `pivot_z`) ou `"suivre"` (barre de lestage, plateau
de bureau qui suit le bas sans se déformer) ; ils sont décrits à l'état « bas ». Un arrêt de visite peut porter
`"commandes": {"toile": "bas"}`. Dans la visite : **on touche l'objet** (visite et maquette) pour le monter ou le descendre ;
la zone de toucher couvre toute sa course (bas et haut, 6 po de plus vers le boîtier) : une toile enroulée se retrouve en
touchant son boîtier ou l'endroit où elle descend. Facultatif : `"invite"` (étiquette du repère sur tablette ; défaut
« Touche pour descendre la toile », d'après `libelle_bas` / `libelle_haut`, qui servent aussi au survol et à l'aide).
Sans `commandes`, rien ne change. Pour les tests : `commander(id, "bas" | "haut" | "basculer", immediat)`.

### Toucher les objets (aucun bouton d'action)
Depuis la demande du client du 2026-11-02 (« enlève ces boutons-là, je veux que ça interagisse quand on y touche »), la visite
n'a **plus de barre de boutons d'action** : restent le menu du haut, la visite guidée, le bouton d'étage (▲ Monter / ▼
Descendre) et le petit plan. Tout se fait en touchant (tap, clic) l'objet dans la vue, en visite comme en maquette :

| On touche | Ça fait |
|---|---|
| une commande (toile, bureau assis-debout...) | elle monte ou descend (un toucher pendant le mouvement l'inverse) |
| un objet animé (aspirateur robot) | il s'arrête ; encore : il repart (petit bip) |
| la trappe d'une séquence (« LINGE ») | la séquence part ; depuis l'étage de la trappe, l'invite passagère `libelle_voir` (« Voir arriver au lavage ») apparaît `attente_voir` s (défaut 10) puis s'efface seule ; on la touche pour aller voir l'arrivée |
| un objet du mobilier qui porte `"sequence": id` (le panier du bas) | la séquence part au complet, vue d'en bas |
| la porte d'un scénario (`"porte"`, fermée ; dedans ou dehors) | « Quelqu'un cogne » : il arrive et joue sa scène ; porte ouverte : elle se ferme ; pendant la scène, la porte est à lui |
| le personnage pendant qu'il joue | il s'efface (0,45 s), sons coupés, portes remises comme avant |
| une autre porte | elle s'ouvre ou se ferme |
| un objet du lointain (traversier) | rien : il avance tout seul |

Zones de toucher généreuses (invisibles, jamais dessinées) : robot (rayon + 4½ po, 7 po plus haut), trappe et panier (+ 2½ po),
personnage (cylindre de 15 po de rayon au moins), course entière d'une commande (+ 2 po). Un glisser n'est pas un toucher : le
doigt qui a bougé de plus de 10 px (5 à la souris) fait tourner la vue et ne déclenche rien ; un pincement non plus.
Repères, sans bouton : à la souris, la main et un léger halo ambré au survol (et le nom de l'action en info-bulle) ; sur écran
tactile, en arrivant à un arrêt de visite, chaque objet touchable visible (un toucher à cet endroit l'atteindrait vraiment) à
15 pi au plus de l'œil pulse 2 s (2 au plus) avec une petite étiquette qui s'efface seule (`"invite"` : « Touche le robot »,
« Touche la trappe », « Touche le panier », « Touche la porte »...) ; un toucher fait un court éclair de halo. Le panneau d'aide
« ? » liste ce qu'on peut toucher et porte l'interrupteur **« Sons de la visite »** (voix et sons du visiteur, bip du robot,
chute du ballot ; retenu sur l'appareil). Rien ne joue avant un premier geste sur la page.

Clés des anciens boutons : **gardées, sans effet** (acceptées par `generer_3d.py` pour ne rien casser) : `"bouton"` d'un objet
animé, `"libelle_arret"` et `"libelle_son"` d'un scénario. Toujours utiles : `libelle_bas` / `libelle_haut` (survol, aide,
repère par défaut), `libelle` d'une séquence ou d'un scénario (survol, aide), `libelle_voir` (texte de l'invite passagère),
`depart_bouton` (étape où il commence quand on touche sa porte). Pour les tests : `cibles()` (objets touchables et leur point
à l'écran, `vu` : un toucher là les atteint), `toucherObjet(x, y)`, `inviterToucher()`, `forcerInvites(true)`, `tenirHalo(cle, k)`.

### Objets animés en boucle (facultatif : aspirateur robot...)
`SCENE["animes"]` d'une scène d'**étage** (repère de son plancher ; MAISON-18 : `appliquer_scene_rdc(S, h)` fait
`S.setdefault("animes", []).append({...})`). Pouces, secondes, degrés.

| Clé | Sens |
|---|---|
| `id`, `nom` | texte ; `id` unique dans la maquette, `nom` = titre de l'aide et du survol |
| `objets` | comme le mobilier (`boite`, `cylindre`, `arrondi`, `tube`, `sphere`, `tore`, `modele`...), dans un repère **local** : origine au centre de l'objet, au sol (z = 0 = son dessous), **+x = l'avant** (le sens de marche), +y = sa gauche. Interdits : `commande`, `porte`, `fixe`, `anim` |
| … `"tourne": 540` | sous-objet qui tourne sur lui-même (°/s, positif = antihoraire vu de dessus) autour d'un axe vertical en `"centre": [x, y]` (local ; défaut : `x, y` de l'objet ou centre de sa boîte) ; arrêté pendant les pauses |
| … `"clignote": 2.0` | voyant : période en s ; `"couleur": "#3fd18b"` (couleur et émission ; sinon celle du matériau) ; matériau conseillé `"spot"` |
| `trajet` | `[[x, y], ...]` (repère du plancher), au moins 2 points, **boucle fermée** (ne pas répéter le point 0 à la fin) ; au chargement l'objet est au point 0, tourné vers le point 1 |
| `vitesse` | po/s en ligne droite (30 cm/s = 11,8) |
| `rotation` | °/s (défaut 90) : à chaque point, il **tourne sur place** vers le segment suivant (par le plus court) |
| `pauses` | `[{"point": i, "duree": s}]` : arrêt en arrivant au point i, avant de tourner (base de recharge) |
| `z`, `depart`, `ombre` | dessous au-dessus du plancher (défaut 0) ; s déjà écoulées au chargement (défaut 0) ; ombre de contact ronde (défaut `True`) |
| `toucher`, `invite` | on le touche pour l'arrêter ou le faire repartir (défaut `True` ; `False` : rien à toucher) ; étiquette du repère sur tablette (défaut « Touche : <nom> ») ; `bouton` (ancien) : accepté, sans effet |

Un tour = pour chaque segment : avancer (longueur / vitesse), pause éventuelle au point d'arrivée, tourner. Ces objets ne sont
jamais fusionnés, ne projettent pas d'ombre, ne bloquent pas le visiteur ; on les touche (zone élargie) pour les arrêter ou les faire repartir.
Rendu continu (30 images/s au plus ; 8 pour un voyant seul à l'arrêt) seulement si l'objet est visible : étage et mobilier
montrés, dans le champ de vision, aucun mur entre l'œil et lui, page visible.

    S.setdefault("animes", []).append({"id": "robot", "nom": "Aspirateur robot",
        "objets": [{"forme": "cylindre", "x": 0, "y": 0, "z0": 0.4, "z1": 3.3, "r": 6.9, "mat": "metal"},
                   {"forme": "cylindre", "x": -1.2, "y": 0, "z0": 3.3, "z1": 4.2, "r": 1.7, "mat": "gris"},
                   {"forme": "cylindre", "x": 3.2, "y": 0, "z0": 3.3, "z1": 3.42, "r": 0.45, "mat": "spot", "clignote": 2.0, "couleur": "#3fd18b"},
                   {"forme": "tube", "pts": [[4.6, 4.6, 0.35], [7.6, 5.7, 0.25]], "r": 0.13, "mat": "gris", "tourne": 540, "centre": [4.6, 4.6]}],
        "trajet": [[124, 185], [405, 172], [404, 330], [400, 196]], "vitesse": 12, "rotation": 90,
        "pauses": [{"point": 0, "duree": 8}], "invite": "Touche le robot"})

### Séquence sur deux étages (facultatif : chute à linge...)
`SCENE["sequences"]` de la scène **principale** (celle qui porte `"etages"` ; MAISON-18 : `appliquer_scene_deux(SCENE)` ;
un projet à un étage : sa SCENE). Pouces, x et y du repère de la maison, **z ABSOLU** (plancher du sous-sol = 0, RDC = 105).
Les objets fixes (bouche noire, panier, gaine) vont dans le mobilier de chaque étage : `SCENE["etages"][0]` (SS) et `[1]` (RDC),
z de leur plancher.

| Clé | Sens |
|---|---|
| `id`, `nom`, `libelle`, `libelle_voir`, `attente_voir` | `libelle` : nom de l'action (survol, aide ; défaut `nom`) ; `libelle_voir` : invite passagère montrée sur l'étage de la trappe après l'envoi, `attente_voir` s (défaut 10), puis effacée seule |
| `invite`, `invite_panier` | étiquettes des repères sur tablette (défaut « Touche la trappe », « Touche le panier ») |
| `trappe.objets` | mobilier en z absolu, décrit **fermé** ; le toucher déclenche la séquence |
| `trappe.charniere` | `[[x, y, z], [x, y, z]]` : axe de rotation (deux points distincts) |
| `trappe.angle` | degrés, règle de la main droite autour de l'axe point 1 → point 2 (voir plus bas) |
| `trappe.duree`, `trappe.ferme_apres` | s pour s'ouvrir (et se refermer), défaut 0,6 ; elle se referme `ferme_apres` s (défaut 0,3) après que le ballot a passé le point 1 du chemin |
| `ballot.objets` | mobilier en repère **local** : origine au centre du **dessous** du ballot |
| `ballot.chemin` | `[[x, y, z], ...]` (z absolu) suivi par l'origine du ballot : point 0 = où il apparaît (devant ou sur la trappe ouverte) ; point 1 = dans l'ouverture ; ... ; dernier = posé au fond du panier |
| `ballot.vitesse_depart`, `ballot.frottement`, `ballot.culbute` | po/s de la poussée (défaut 30 : jamais plus lent) ; frottement des pentes (0 à 1, défaut 0,3) ; degrés de roulade pendant la descente (défaut 0 ; il revient droit à l'arrivée) |
| `panier.pile` | `[[dx, dy, dz], ...]` : décalage du dernier point pour le 1er, 2e, 3e... ballot (défaut `[[0,0,0],[2,-1.5,5],[-1.5,1.5,10]]`) ; pile pleine : le lancer suivant vide le panier |
| `vue_depart` | facultatif, `{"x", "y", "cap", "etage", "tangage"}` (tangage en degrés, négatif = vers le bas) : (tests) `declencherSequence(id, "bouton")` y amène d'abord si l'on est à plus de 30 po ou tourné de plus de 30° ; touchée, la trappe part tout de suite |
| `vue_arrivee` | **obligatoire** si trappe et panier sont sur deux étages : point de vue qui voit la sortie au plafond **et** le panier ; l'invite « Voir arriver » y amène |

Déroulement : t = 0, la trappe s'ouvre et le ballot apparaît au point 0 ; à t = `duree`, il part à `vitesse_depart` et suit
le chemin : sur chaque segment, accélération g·(sin − frottement·cos) avec g = 386 po/s² (verticale = chute libre ; à plat ou
trop peu en pente pour glisser : vitesse gardée) ; il passe d'un étage à l'autre quand son origine descend sous le plancher ;
il se pose au dernier point + `pile[k]` (petit tassement) et y reste. « Voir arriver » : on vole jusqu'à `vue_arrivee` ; si
le ballot était déjà passé, il repart d'un peu avant sa sortie du plafond (on le voit arriver). Depuis le sous-sol, toucher
le panier déclenche et on voit le ballot sortir du plafond. Rendu continu seulement pendant la séquence.

Sens de `angle` (trappe à charnière en bas, sur une face verticale) : face qui regarde +y (on se tient du côté des y plus
grands), axe de x petit à x grand → `angle` **négatif** (le haut vient vers +y) ; face qui regarde −y : positif ; face qui
regarde +x, axe de y petit à y grand : positif ; face qui regarde −x : négatif. Elle s'ouvre du mauvais côté : changer le signe.

Le panier du bas se touche aussi : ses objets du mobilier (étage du panier) portent `"sequence": id` (groupe à part, jamais
fusionné ; la séquence joue au complet, on voit le ballot sortir du plafond). Sons : un « pouf » quand le ballot tombe.

Pour que ce soit crédible : une **bouche noire** fixe (mobilier, mat `"pneu"`, 0,2 po d'épaisseur juste derrière la trappe)
fait un trou noir quand la trappe s'ouvre, et le ballot y disparaît ; au plafond du sous-sol, une **plaque de sortie** noire
(z0 = plafond − 0,7, z1 = plafond − 0,1) : le plafond cache tout ce qui est au-dessus, le ballot apparaît en la traversant ;
**panier creux** (forme `"arrondi"` avec `"trou"` = épaisseur de paroi), sinon le ballot disparaît dans un volume plein.

    SCENE["sequences"] = [{"id": "chute", "nom": "Chute à linge", "libelle": "Envoyer du linge",
        "libelle_voir": "Voir arriver au lavage",
        "trappe": {"objets": [{"x0": 79, "x1": 93, "y0": 168.5, "y1": 169.25, "z0": 141, "z1": 153, "mat": "metal"}],
                   "charniere": [[79, 169.25, 141], [93, 169.25, 141]], "angle": -65, "duree": 0.6, "ferme_apres": 0.3},
        "ballot": {"objets": [{"forme": "sphere", "x": 0, "y": 0, "z": 3.9, "r": 5.6, "ecrase": 0.7, "mat": "draps"}],
                   "chemin": [[86, 178, 145.2], [86, 166, 141.5], [86, 156, 132], [86, 150, 108], [86, 146, 95], [86, 140, 1]],
                   "vitesse_depart": 30, "frottement": 0.3, "culbute": 120},
        "panier": {"pile": [[0, 0, 0], [1.5, -1, 6], [-1.5, 1.2, 12]]},
        "vue_depart": {"x": 93, "y": 198, "cap": 266, "etage": "RDC", "tangage": -14},
        "vue_arrivee": {"x": 40, "y": 76, "cap": 55, "etage": "SS", "tangage": -4},
        "attente_voir": 10, "invite": "Touche la trappe", "invite_panier": "Touche le panier"}]
    # au sous-sol, les objets du panier : {"forme": "arrondi", ..., "trou": 0.3, "mat": "draps", "sequence": "chute"}

Pour les tests (Playwright) : `figerAnimations(true)` (horloges arrêtées : une image par changement), `poserHorloge(id, s)`,
`basculerAnime(id[, pause])`, `declencherSequence(id[, "objet" | "bouton"])`, `voirArrivee(id)`, `fixerSequence(id, s)` (pose
la séquence à s secondes du déclenchement, la lance au besoin ; s ≥ fin : ballot posé), `etatSequence(id)` (temps, trappe,
pile, position du ballot, `sortiePlafond`). `generer_3d.py` vérifie le contrat (`animes()`, `sequences()`) et dit quoi corriger.

<!-- --- scénarios -->
### Scénario : un personnage qui joue une suite d'étapes (facultatif : visiteur qui cogne à la porte...)
`SCENE["scenarios"]` de la scène **principale** (MAISON-18 : `appliquer_scene_finale(SCENE)` d'un module de la liste
`FINALE`, après l'extérieur). Pouces, secondes, degrés ; x et y du repère de la maison, z **absolu**. Exemple complet :
`MAISON-18_deux_etages/visiteur.py`.

| Clé | Sens |
|---|---|
| `id`, `nom`, `libelle` | `libelle` : ce que fait le toucher de sa porte (« Quelqu'un cogne » ; survol, aide) ; `libelle_arret`, `libelle_son` (anciens boutons) : acceptés, sans effet |
| `porte`, `invite` | porte qu'on touche (fermée, dedans ou dehors) pour le faire venir (défaut : la première que ses étapes ouvrent) ; étiquette du repère sur tablette (défaut « Touche la porte ») |
| `personnage.objets` | objets fixes du corps (comme le mobilier), repère **du personnage** : origine au sol entre ses pieds, **+x devant lui**, +y à sa gauche, z vers le haut |
| `personnage.parties` | `[{"id", "pivot": [x, y, z], "parent", "objets", "balance", "phase", "frappe", "poses"}]` : parties articulées (jambes, haut du corps, tête, bras, avant-bras), objets décrits dans le repère du personnage, pivot = articulation ; `parent` déclaré avant (l'avant-bras suit le bras) ; `balance` : ° de balancement à la marche, `phase` : 0 ou 180 (jambe gauche 0, droite 180, bras à l'inverse) ; `frappe` : ° du coup (l'avant-bras qui cogne) |
| … `"poses": {"repos": [b, e, l], "cogner": ..., "dire": ..., "pet": ...}` | angles de la partie selon l'étape (fondu de 0,3 s) : `b` balancement (positif : le bas de la partie vers l'avant ; tête : elle lève le menton), `e` écart (positif : vers l'extérieur), `l` lacet (positif : vers sa gauche). Pose de l'étape : `pose` de l'étape, sinon `marche`/`repos`, `cogner`, `dire`, le nom du son |
| … `"echelle": [ex, ey, ez]` | sur une sphère, un cylindre, un tore ou une boîte : ellipsoïdes (tête, bedaine), torse elliptique |
| `personnage.couleurs` | `{"v-polo": "#1F57D6" ou {"couleur", "rugosite", "metal", "duvet"}}` : matériaux du personnage (sans relief), employés par `"mat"` |
| `personnage.hauteur`, `foulee`, `rebond`, `vitesse`, `rayon`, `ombre` | haut de la tête (la bulle va au-dessus), po par cycle de deux pas (46), rebond du corps (0,8), po/s (40), rayon (ombre ronde, champ de vision), ombre ronde au sol (`True`) |
| `depart` | `{"x", "y", "cap", "etage"}` : où il apparaît (`"EXT"` dehors) |
| `etapes` | une action par étape (voir plus bas) ; `depart_bouton` : indice de l'étape où la porte touchée et l'arrêt le font commencer (défaut 0) |
| `declencheur` | `{"x", "y", "z", "rayon", "hauteur", "attente", "auto"}` : il vient tout seul (après un premier geste sur la page) quand le visiteur est à moins de `rayon` po de (x, y) et à moins de `hauteur` po de z (dedans ou dehors), au plus une fois par `attente` s (défaut 120 : jamais moins de 2 min entre deux passages ; arrêté = attente aussi) |
| `vue` | `{"x", "y", "cap", "etage", "tangage", "z"}` : (tests) `lancerScenario(id, "bouton")` y amène d'abord si l'on est hors du rayon ; la porte touchée, on la voit déjà |
| `volume` | 0 à 1 (défaut 0,5) |

Étapes : `{"marcher": [[x, y], ...], "vitesse"}` (chemin trouvé sur la grille de la visite, autour des obstacles, par les
marches de 8 po au plus et par la porte extérieure la plus commode d'une zone à l'autre ; z lu au sol à l'exécution : perron,
marches, balcon, terrain, plancher ; il regarde où il va, jambes et bras balancent) ; `{"tourner": cap ou [x, y]}` ;
`{"cogner": n, "intervalle": 0.45}` (le bras qui a `frappe` cogne, un coup synthétisé par contact) ; `{"dire": "JULIEEEEE !",
"voix": "Juliiiiiie !", "duree"}` (bulle au-dessus de la tête ; voix du navigateur : fr-CA si l'appareil en a une, sinon
française, grave et lente ; aucune voix : la bulle seule) ; `{"son": "pet" | "coup", "duree", "vibre", "nuage"}` (Web Audio,
aucun fichier) ; `{"ouvrir": id}` / `{"fermer": id}` (porte de la maquette, `duree` d'attente, défaut 0,9) ; `{"attendre": s}`.
Toute étape : `"bulle"` (texte), `"bulle_style"` (`parole`, `cri`, `son`, `nuage`), `"pose"`, `"duree"`. Un arrêt de visite
peut porter `"scenario": id` (il le fait venir à l'arrivée).

Dans la visite : le personnage va dans le mobilier de l'étage où il marche (ou dans l'extérieur, éclairé par le ciel), jamais
fusionné, sans ombre portée ni collision ; pendant qu'il joue, une zone de toucher l'entoure : touché, il s'efface. Rendu
continu (30 images/s au plus) seulement pendant qu'il joue et qu'il est dans le champ de vision. La bulle suit sa tête (rabattue
au bord de l'écran s'il est hors champ). Rien ne sonne avant le premier geste de l'utilisateur sur la page (règle des
navigateurs) ; interrupteur « Sons de la visite » dans l'aide. Sans `scenarios`, rien ne change.
Pour les tests : `fixerScenario(id, s)` (horloge figée, personnage, bulle et portes à s secondes du plan), `etatScenario(id)`
(`debuts` des étapes, position, zone, bulle), `lancerScenario(id[, "porte" | "auto" | "arret" | "bouton"])`,
`arreterScenario(id[, fini, fondu])`.
`generer_3d.py` vérifie le contrat (`scenarios()`).
<!-- --- fin scénarios -->

Extérieur (facultatif, maquette à plusieurs étages) : `SCENE["exterieur"]` (terrain, cour, maison vue de dehors ; contrat
dans le docstring de `MAISON-18_deux_etages/exterieur.py`). La visite dessine le terrain jusqu'à l'horizon, la cour et
l'enveloppe de la maison sous le soleil du jour ; on marche dehors (marches de 8 po au plus montées seules, obstacles, murs,
lignes de lot) et on entre ou sort par les portes extérieures ouvertes (une porte dont un côté est hors de l'emprise de son
étage). Arrêts dehors dans la section « Extérieur » ; petit plan du lot dehors ; maquette : vue « Extérieur » (maison avec
son toit). Dedans, l'extérieur n'est dessiné qu'à travers les fenêtres et les portes ouvertes (et l'inverse dehors).
Facultatif : `"relief"` (terrain non plat : grille `xs`, `ys`, `z[j][i]` en z absolu ; chaque case en deux triangles par la
diagonale (xs[i], ys[j]) → (xs[i+1], ys[j+1]), sautée si son centre tombe dans un trou ; on ne marche pas sur une pente de
plus de 50 % ; les margelles lisent le sol devant chaque fenêtre) et `"revetements"` (`[{"nom", "pts", "mat"}]` drapés sur
le relief, découpés case par case ; on y marche comme sur le terrain). Sans relief, terrain plat à `"sol"`. Sortie
ailleurs que dans le projet (essais) : `python3 renovation/outils/generer_3d.py renovation/<projet> /chemin/visite.html`.

<!-- --- lointain -->
### Le lointain et les objets animés de l'extérieur (facultatif : fleuve, traversier...)
Dans `SCENE["exterieur"]` (MAISON-18 : `fleuve.py`, module de la liste `FINALE` de `scene_3d.py`, `appliquer_scene_finale(S)`).
Pouces, secondes, degrés, **z ABSOLU** (plancher du sous-sol = 0). Contrat : `generer_3d.exterieur_animes()`,
`exterieur_lointain()` et `_objets_lointains()`, qui disent quoi corriger.

**`"animes"`** : objets animés en boucle dehors, **même contrat que `SCENE["animes"]` d'un étage** (objets en repère local,
`trajet`, `vitesse`, `rotation`, `pauses`, `depart`, `ombre`, `toucher`, `invite`, sous-objets `tourne`, voyants `clignote`), mais `z` absolu
(dessous de l'objet) et `id` unique dans toute la maquette. Un objet `lointain` ne se touche pas (`toucher` vaut `False`). En plus :

| Clé | Sens |
|---|---|
| `lointain` | `True` : objet au loin (navire sur le fleuve...), au-delà du lot, à 10 km au plus. Dessiné dans le plan lointain (voir plus bas) ; ses `objets` sont des formes du lointain (`boite`, `cylindre`, `sphere`, `toit`, `texte`, une `couleur` chacune) ; pas d'ombre de contact |
| `cadence` | images par seconde au plus pendant qu'il roule et se voit (1 à 30, défaut 30 ; un navire à 2 km : 10 suffisent) |

Rendu continu seulement s'il se voit : dehors, dans le champ de vision ; dedans, par une fenêtre ou une porte ouverte de
l'étage (aucun mur entre l'œil et lui) ; rien quand la page est cachée. Un objet animé de l'extérieur qui n'est pas au loin se
touche comme le robot. Tests : `poserHorloge(id, s)`, `basculerAnime(id)`, `figerAnimations(true)`.

**`"lointain"`** : ce qu'on voit au-delà du lot jusqu'à l'horizon. Le lot est dessiné dans les 200 m de la caméra, sous une
brume de 40 à 180 m ; le lointain est dessiné **derrière tout le reste** (le terrain du lot, la maison et leurs objets passent
toujours devant), avec sa propre brume de distance, un éclairage simple (soleil du jour, ciel) et des couleurs par sommet :
un maillage pour l'eau, un pour la terre et tous les objets fixes. Dedans, on ne le voit que par les fenêtres.

| Clé | Sens |
|---|---|
| `ouvert` | côtés du relief du lot **non prolongés** jusqu'à l'horizon (défaut `["-y"]`, vers la rue) : au-delà du bord du relief, on voit le lointain. Il faut un `"relief"` |
| `eau` | `{"nom", "z", "pts", "couleur", "couleur_loin", "reflet"}` : surface (z absolu), polygone `[[x, y], ...]` (jusqu'à 150 km : l'horizon ; commencer à 50 m de la maison au moins), couleur proche et au loin, part du reflet du ciel (0 à 1, défaut 0,35 ; il grandit en rasant l'eau). L'eau ne cache jamais la terre ni les objets |
| `terre` | `{"xs", "ys", "z", "couleurs"}` : relief du lointain (grille comme `"relief"`, même diagonale, 10 km au plus), une couleur `"#rrggbb"` par sommet (facultatif). Son premier rang reprend le bord du relief du lot (pas de marche) ; elle s'arrête à la rive, **au niveau de l'eau, jamais dessous** |
| `objets` | formes du lointain, z absolu, `"couleur"` (ou `"mat"`) : `boite` (x0..z1, ou `pts` : prisme), `cylindre` (x, y, r, z0, z1 ; `r2` = rayon du haut, 0 = cône), `sphere` (x, y, z, r, `ecrase`), `toit` (deux versants sur x0..y1, de z0 à z1, `faitage` `"x"` ou `"y"`), `texte` (`texte`, x, y, z0, z1, `larg`, `face`) |
| `brume`, `couleur_brume` | distance (po) où la brume du lointain voile 63 % (défaut 1 200 000, environ 30 km) ; sa couleur |

Au loin, la profondeur est grossière : décoller de 6 po au moins ce qui est peint sur une surface (fenêtres, nom d'un navire),
12 po sur un navire à plus de 1 km.

    X = SCENE["exterieur"]
    X["lointain"] = {"ouvert": ["-y"], "brume": 2400000,
        "eau": {"nom": "Fleuve Saint-Laurent", "z": -1772, "pts": [[-5.9e6, -17677], [5.9e6, -17677], [5.9e6, -5.9e6], [-5.9e6, -5.9e6]],
                "couleur": "#143350", "couleur_loin": "#21476b", "reflet": 0.18},
        "terre": {"xs": [...], "ys": [...], "z": [[...]], "couleurs": [[...]]},
        "objets": [{"forme": "toit", "x0": -40, "x1": 460, "y0": -1662, "y1": -1338, "z0": -9, "z1": 64, "couleur": "#3f4245"}]}
    X.setdefault("animes", []).append({"id": "traversier", "nom": "Le traversier F.-A.-Gauthier", "lointain": True,
        "cadence": 10, "z": -1772, "vitesse": 911.5, "rotation": 2, "depart": 78,
        "trajet": [[-118110, -78740], [118110, -78740], [118110, -106299], [-118110, -106299]],
        "objets": [{"forme": "boite", "pts": [[-2622, -394], ...], "z0": 0, "z1": 276, "couleur": "#1f4896"},
                   {"forme": "texte", "texte": "F.-A.-GAUTHIER", "x": -1732, "y": 455, "z0": 134, "z1": 189, "larg": 591,
                    "face": "+y", "couleur": "#ffffff"}]})
<!-- --- fin lointain -->

## Matériaux
`renovation/outils/materiaux/` : bibliothèque de matériaux réels (ambientCG, Poly Haven, CC0, ou fichiers de
fournisseurs), décrite dans `renovation/outils/catalogue_materiaux.py` ; voir `renovation/outils/materiaux/README.md`.

## Modèles 3D
`renovation/outils/modeles/` : 31 modèles réels optimisés (Amazon Berkeley Objects, Sketchfab, Poly Haven ; CC BY 4.0 ou CC0),
décrits dans `renovation/outils/catalogue_modeles.py` (sens, licence, attribution) ; recherche et sources dans
`renovation/outils/modeles/SOURCES.md`. Les crédits sont affichés dans la visite (panneau Matériaux).

## Skill de design
`.claude/skills/designer-interieur/SKILL.md` : méthode, dégagements, code à vérifier, direction de design, livrables.
