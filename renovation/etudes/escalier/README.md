# Étude — où mettre l'escalier (en haut et en bas)

Demande du propriétaire (2026-10-29) : l'escalier ne peut pas être devant la fenêtre de la chambre 1 au sous-sol ;
« on peut regarder pour le mettre ailleurs en haut ? Donne-moi plein d'options. »

`etude_escalier_3.py` dessine six implantations sur les deux étages, à partir des plans de base (lus, jamais modifiés) :
`python3 etude_escalier_3.py . ../../../releve/livrables/donnees/maison.json` → `etude_escalier_3a.png`, `etude_escalier_3b.png`.

Hypothèses communes : 14 contremarches d'environ 7½ po (8 pi au sous-sol + ~9 po de plancher), girons de 10 po, 36 po
de large. Au sous-sol, seules la fondation, les fenêtres, les portes, les poutres et les colonnes sont fixes : les
cloisons seront redessinées autour de l'option choisie.

| # | Emplacement | En haut | En bas | Coût relatif |
|---|---|---|---|---|
| 1 | Emplacement de 1957 | bande de 3 pi entre salle à manger et cuisine ; entrée au fond | pied face au hall central ; chambre 2 réduite | faible (trémie d'origine) |
| 2 | Entrée avant (escalier commun) | on descend directement de l'entrée ; le salon perd une bande de 3 pi ; cloison de l'entrée ouverte ; 3 tournantes en haut | pied dans le hall entre les poutres ; mur télé du séjour à déplacer | moyen |
| 3 | Au centre, entre les deux poutres | dans le dégagement + coin avant de la cuisine | pied face à la porte d'entrée du bas ; lien hall–vestiaire coupé | moyen |
| 4 | Entrée arrière et caveau | aucune pièce touchée ; on descend depuis l'entrée arrière | le caveau devient la cage d'escalier | élevé (fondation) |
| 5 | Colimaçon Ø 5 pi | coin de la salle à manger | passage du caveau | moyen ; code à vérifier |
| 6 | Côté cuisine, à l'est de la colonne de droite | bande de 3 pi dans la cuisine | chambre 2 étroite (≈ 6'-6") | moyen |

Aucune n'est devant une fenêtre du sous-sol. À valider dans tous les cas : sens des solives, linteaux de la trémie,
coupe-feu entre les deux logements (Ville de Baie-Comeau et un professionnel).
