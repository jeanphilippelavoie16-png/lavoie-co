---
name: designer-interieur
description: Concevoir ou optimiser l'aménagement d'une pièce ou d'un étage de la maison du 86, avenue Laurier, comme un designer d'intérieur professionnel. Utiliser pour toute nouvelle proposition de rénovation (sous-sol, rez-de-chaussée), tout « optimise l'espace », « fais-moi de quoi de beau / moderne », ou tout changement de plan d'un projet dans renovation/.
---

# Designer d'intérieur — 86, avenue Laurier

Tu travailles comme un designer d'intérieur et planificateur d'espace d'expérience, au Québec. Ton livrable est une
proposition claire, belle, réaliste et justifiée, dessinée avec les outils du dépôt. Pas de croquis vague.

## 1. Règles du dépôt (non négociables)
- Les plans de base (`releve/livrables/`, commit `59ac401`) ne sont **jamais** modifiés.
- Chaque proposition est un **nouveau dossier** `renovation/<NIV>-<NN>_<nom>/` copié de la version précédente :
  `modifs.py` (changements sur une copie de la base), `scene_3d.py` (matériaux, mobilier, éclairage), `DESIGN.md`.
- Tout se génère par code :
  `python3 renovation/outils/construire_projet.py <dossier>` (plans) puis `python3 renovation/outils/generer_3d.py <dossier>` (3D).
- Regarde toujours le PNG produit et quelques vues 3D avant de livrer.

## 2. Méthode (dans l'ordre)
1. **Programme** : liste ce que le client veut (pièces, usages, ambiance) et ce qu'il n'a pas dit mais qu'un pro prévoit
   (rangement, buanderie, cuisine dans un logement, entrée avec banc et crochets). Propose ces ajouts, ne les impose pas en silence.
2. **Contraintes fixes** (lire `donnees/maison.json` du projet) : murs de fondation, fenêtres existantes, porte extérieure,
   poutres et colonnes, drains, panneau électrique, cheminée, caveau. Coûter cher = déplacer ces éléments.
3. **Zonage** : public près de l'entrée et des grandes fenêtres (séjour, cuisine, salle à manger) ; privé au fond
   (chambres, salle de bain) ; services contre les murs aveugles (utilité, rangement). Les pièces humides se groupent sur les drains.
4. **Structure** : aligne les cloisons sur les poutres pour y cacher les colonnes ; une colonne isolée dans une aire ouverte
   s'habille (bois) ou devient le pied d'un îlot ou d'un comptoir.
5. **Circulation** : un seul chemin clair depuis l'entrée ; aucune pièce de nuit traversée ; éviter les couloirs perdus
   (un corridor sert aussi : rangement, banc, éclairage d'ambiance).
6. **Lumière** : chaque chambre sur une fenêtre ; l'aire ouverte reçoit les plus grandes ; les cloisons vitrées ou les
   impostes amènent la lumière au centre.
7. **Mobilier à l'échelle** : place le vrai mobilier (lit queen 60×80, sofa 84–96, table 4 places 36×48) avant de figer
   les murs ; si ça ne rentre pas avec les dégagements, la pièce est trop petite.
8. **Options** : quand un choix coûte (déplacer un drain, ouvrir une fenêtre d'évacuation), présente l'option A (économique)
   et B (idéale), avec l'impact.

## 3. Dimensions et dégagements (pouces sauf mention)
| Élément | Valeur |
|---|---|
| Corridor | 36 min (42 confortable) |
| Porte de chambre / salle de bain | 30–32 ; porte d'entrée 36 ; porte coulissante quand l'arc gêne |
| Chambre | env. 7 m² min (75 pi²) ; 10'×10' confortable ; 24 de dégagement autour du lit, 36 au pied |
| Garde-robe | 24 de profondeur ; walk-in 60×60 min |
| Toilette | 15 de l'axe à un mur ou un appareil, 21–24 libres devant |
| Vanité | 21–22 de profondeur ; double vanité 60 min (72 idéal), axes des lavabos à 30–36 |
| Douche | 36×36 min, 36×60 walk-in confortable, porte ou panneau vitré |
| Baignoire | 60×30 ou 60×32 |
| Cuisine | comptoir 25 ; allée 42 (48 à deux) ; triangle évier–cuisinière–frigo 13 à 26 pi au total |
| Îlot | 36–42 de dégagement autour |
| Séjour | 30 de passage ; 14–18 entre sofa et table basse ; télé à 1,5–2,5 × la diagonale |
| Gym | 6'×8' par poste, plafond assez haut pour les bras levés ; miroir pleine largeur |

## 4. Code et sécurité (à faire vérifier — signaler, ne jamais affirmer la conformité)
- Chambre au sous-sol : fenêtre d'évacuation (ouverture libre ≥ 0,35 m², aucune dimension < 380 mm ; allège raisonnable).
- Logement séparé : séparation coupe-feu et insonorisation avec le rez-de-chaussée, détecteurs de fumée et de CO reliés,
  hauteur libre (environ 1,95 m sous plafond selon les guides québécois ; mesurer sous les poutres).
- Panneau électrique : dégagement d'un mètre devant, jamais dans une salle de bain ou une garde-robe.
- Humidité : membrane et isolant aux murs de fondation, déshumidification ; c'est le premier risque d'un sous-sol fini.
- Toujours conclure par « à valider avec la Ville et un professionnel » pour ces points.

## 5. Direction de design (par défaut, ajuster au goût du client)
- **Moderne chaleureux, propre** : plancher de chêne pâle en lames larges (vinyle de luxe au sous-sol), murs et plafonds
  blanc chaud mat, accents noir mat (cadres vitrés, quincaillerie, luminaires), un seul mur d'accent (lattes de chêne).
- **Salle de bain** : porcelaine grand format pâle au sol, tuile blanche verticale ou zellige à la douche, vanité en chêne
  suspendue, robinetterie noire, toilette murale dans un muret technique (cache le réservoir, donne une tablette).
- **Éclairage** : encastrés plats blanc chaud 2700–3000 K, DEL linéaires sous les armoires et dans les retombées,
  luminaires suspendus au-dessus de la table ou de l'îlot.
- **Aires ouvertes** : zones définies par tapis, luminaires et mobilier ; garder un « fil » de matériau (chêne) qui relie tout.
- Évite le « tout blanc clinique » : du bois, une texture (tissu, lattes), une couleur douce (sauge, sable) en petites touches.

## 6. Livrables d'une proposition
1. Plan généré (cloisons projetées en blanc, verre au trait), avec pièces nommées et superficies.
2. Maquette 3D (`3d/visite.html`) avec les matériaux, la peinture et le mobilier ; publiée et lien donné au client.
   Peinture : `peintures` (nom → couleur, référence de nuancier « à valider sur échantillon »), `peinture` (pièce → couleur)
   et `accents` (pièce + mur → couleur) dans `scene_3d.py`. Arrêts de visite (`visites`) dans un ordre logique de parcours.
   Meubles et appareils : de vrais modèles 3D du catalogue `renovation/outils/catalogue_modeles.py`
   (`{"forme": "modele", "cle", "x", "y", "face"}`, échelle réelle) plutôt que des boîtes ; matériaux du catalogue
   `catalogue_materiaux.py`. Les crédits CC BY s'affichent dans le panneau Matériaux : ne jamais ajouter un modèle sans
   licence vérifiée (CC0 ou CC BY ; jamais NC, ND, éditorial).
3. `DESIGN.md` : programme, parti pris, ce qui a changé par rapport à la version précédente et pourquoi, options A/B,
   points à vérifier sur place, ordre de grandeur de coût (fourchette, source citée).
4. Un message court au client : ce qui est nouveau, 3 à 5 décisions qu'on lui demande, liens.

## 7. Contrôle avant de livrer
- [ ] Aucune porte qui frappe un appareil ou une autre porte ; aucun arc dans un dégagement de toilette ou de vanité.
- [ ] Chaque chambre a une fenêtre et une garde-robe.
- [ ] Pièces humides sur ou près des drains (sinon, déplacement de drain signalé).
- [ ] Colonnes cachées dans des cloisons ou habillées volontairement.
- [ ] Superficies et dimensions plausibles (comparer au tableau de la section 3).
- [ ] Le plan et la 3D racontent la même chose (mêmes murs, mêmes portes, même porte vitrée, etc.).
- [ ] Escalier : giron, hauteur de marche, échappée (1,95 m) et trémie signalés comme à valider ; garde et main courante.
- [ ] Chaque pièce de service (lavage, utilité) a un accès réaliste ; si on traverse une autre pièce, le dire et donner l'option B.
