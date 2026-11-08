# MAISON-18 — Le visiteur qui cogne à la porte (« JULIEEEEE ! »)

> **Retiré de la visite le 2026-11-08**, à la demande du client : « Enlève la personne qui cogne à la porte ». Le module
> `visiteur.py` reste dans le dossier ; pour le ramener, remettre `"visiteur"` dans `FINALE` (`scene_3d.py`).

Demande du client (2026-11-02), mot pour mot : « je veux aussi que tu ajoutes un personnage qui cogne à la porte pi qui crie
"JULIEEEEE" » ; « un vieux monsieur » ; [photo] « faut qu'il ressemble à lui » ; « il faut qu'il ait une bedaine aussi, pi il
cogne, il crie et il rentre dans la maison. Il recrie Julie et lâche un gros pet ».

Données : `visiteur.py` (appelé par `scene_3d.py`, liste `FINALE`). Moteur : clé générique `SCENE["scenarios"]`
(`generer_3d.scenarios()`, `visite3d_gabarit.html`, contrat dans `renovation/README.md`, section « Scénario »).

## Le personnage
Stylisé, en formes 3D seulement (aucune image de la photo dans la page ; la photo reste dans `prive/`). On reprend ses traits :

| Trait (photo) | Dans la maquette |
|---|---|
| Cheveux courts foncés, poivre et sel, un peu en bataille | calotte brun très foncé, tempes et nuque gris, sept mèches qui rebiquent sur le dessus et une mèche sur le front |
| Lunettes rectangulaires, monture foncée bleu-gris | verres de 2,3 × 1,4 po, barre du haut plus épaisse, pont et branches jusqu'aux oreilles (#3B4A5E) |
| Visage rond, joues rouges | tête ronde, double menton, joues rouges en relief, nez un peu plus rose |
| Grand sourire | bouche ouverte, dents du haut visibles |
| Polo bleu roi à rayures horizontales bleu pâle, col ouvert | polo #1F57D6, rayures #5FAEF2 tout autour du thorax et de la bedaine, manches courtes rayées, col ouvert en V, patte à deux boutons |
| Bonne bedaine | bedaine ronde qui avance de 5½ po devant le thorax et cache la ceinture |
| Pantalon et souliers sobres | pantalon gris anthracite, souliers de cuir brun |

Taille : 5'-8" (68 po au sommet du crâne, mèches comprises ≈ 72). Sympathique : sourire, joues rouges, démarche un peu
balancée (rebond de 0,8 po), rien de méchant.

## Ce qui joue (≈ 45 s du trottoir au trottoir)
1. Il monte du trottoir jusqu'au pied des marches, puis monte les marches du perron (chemin et sol lus dans la visite :
   avec le futur grand balcon, il prendra ses marches à lui).
2. Devant la porte d'entrée (ouv-RDC-010), il se tourne vers elle et **cogne trois coups** (main gauche, la tête tournée
   vers la rue ; sons de coups synthétisés) — bulle « TOC ! TOC ! TOC ! ».
3. Il **crie « JULIEEEEE ! »** (bulle rouge, bras ouverts, menton levé ; voix de l'appareil : « Juliiiiiie ! »).
4. **La porte s'ouvre**, il **entre** et marche jusque dans l'entrée (entre le banc à bottes et le garde-corps de
   l'escalier), se tourne vers la maison et **recrie « JULIEEEEE ! »**.
5. Il lève un peu la jambe et **lâche un gros pet** : son synthétisé (grave qui tremble, crachotements, « prrt » final et
   petit « pfff »), bulle verte « PRRRT ! », petit nuage vert pâle qui se dissipe derrière lui, le corps qui vibre.
6. Il attend, l'air content (tête tournée, mains sur la bedaine), **ressort**, **la porte se referme**, et il redescend
   vers le trottoir où il disparaît.

## Quand
- **Tout seul** (dès qu'on a touché la page une première fois) quand on s'approche de l'entrée, dedans ou dehors : à moins de 13 pi (156 po) de la porte, au niveau du
  rez-de-chaussée ou du perron et du terrain devant (pas depuis le sous-sol). Il part alors du trottoir (on le voit monter si
  l'on est dehors ; dedans, on entend cogner une dizaine de secondes plus tard). **Au plus une fois aux 2 minutes** (délai
  compté depuis la fin, ou l'arrêt, du passage précédent).
- **Bouton « Quelqu'un cogne »** (au-dessus de la visite guidée, au rez-de-chaussée et dehors) : il part du pied des marches
  et cogne 3 s plus tard ; si l'on est loin, on est d'abord amené devant la porte.
- **Arrêt « Le visiteur à la porte »** (section Extérieur, 2e arrêt) : sur le gazon à gauche du perron, de profil, d'où on
  le voit cogner ; il arrive à l'arrivée.

## Comment l'arrêter
- **« Arrêter le visiteur »** (le même bouton pendant qu'il joue) : il disparaît, sons et voix coupés, la porte revient
  comme elle était.
- **« Son du visiteur »** : coupe (✕) ou remet (♪) ses sons et sa voix ; la bulle reste.

## Son
- Coups et pet : **Web Audio** seulement (synthèse : aucun fichier, aucun réseau). Volume 0,5 (raisonnable).
- Voix : **speechSynthesis** du navigateur, voix fr-CA si l'appareil en a une (d'homme si possible), sinon française, sinon
  celle par défaut ; grave (hauteur 0,45) et lente (débit 0,72). Aucune voix sur l'appareil : la bulle seule.
- **Rien ne joue avant un premier geste** sur la page (toucher, clic, touche) : règle des navigateurs. Avant ce geste, on
  voit les bulles sans entendre.

## Limites
- **La voix change d'un appareil à l'autre** (iPad : voix d'Apple ; Android : Google ; ordinateur : Windows ou macOS) ; une
  voix fr-CA n'existe pas partout, et « Juliiiiiie » peut être prononcé un peu autrement selon la voix.
- La voix du navigateur ne passe pas par le bouton de volume de la page (le bouton « Son du visiteur » la coupe quand même).
- Le personnage n'a pas d'ombre portée (seulement une ombre ronde au sol), traverse les meubles s'ils sont sur son chemin et
  ne bloque pas le visiteur ; il ne se touche pas (les boutons le commandent).
- Dans l'onglet en arrière-plan, la visite s'arrête (le navigateur ne dessine plus) : il reprend là où il était.
- Si on referme la porte pendant qu'il entre, il passe quand même.
