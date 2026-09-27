# Redéployer le backend Apps Script : `Code.gs` v5.3.0

Le frontend v5.3.0 marche avec l'ancien serveur, mais **la moitié des
bugs de sync vit dans le serveur**. Tant que la v5.3.0 n'est pas
déployée, ces bugs restent :

- **Les dîners redeviennent des soupers après chaque synchro.** L'onglet
  `Soupers` a deux colonnes « Repas » (D et E), créées par deux migrations
  lancées en même temps. Le serveur écrit dans D et relit E, qui est vide.
  Le dîner cache alors le souper du même jour, et l'épicerie peut ajouter
  ses ingrédients en double.
- **Un repas ajouté pendant une synchro peut rester invisible** jusqu'à la
  modification suivante. `getAllData` lisait la révision au milieu de la
  lecture et mettait en cache un instantané incomplet, étiqueté « à jour ».
- **Quantités doublées** quand le réseau coupe après l'écriture mais avant
  la réponse : l'op était rejouée.
- **Écritures simultanées écrasées** : un `tryLock` raté était ignoré.

## Étapes (2 minutes)

1. Ouvrir le projet Apps Script **« App »** (script.google.com).
2. Dans `Code.gs`, tout sélectionner et coller le nouveau fichier `Code.gs`
   v5.3.0, envoyé à part : il n'est pas dans ce dépôt public, car
   `serveur/` est ignoré par git. Enregistrer.
3. **Déployer → Gérer les déploiements → ✏️ Modifier → Version :
   « Nouvelle version » → Déployer.** Ne pas créer un *nouveau*
   déploiement : l'URL `/exec` changerait et la PWA serait coupée.

Au premier appel, le serveur répare l'onglet `Soupers` tout seul, une
seule fois et sous verrou. Il fusionne les deux colonnes « Repas » puis
supprime la colonne vide. Le dîner du 5 septembre redevient un dîner.

## Vérifier

- Sur ordinateur, passe la souris sur la pastille « Synchronisé » :
  l'infobulle doit dire `serveur 5.3.0`. Si elle dit
  `serveur ancien (à redéployer)`, c'est l'étape 3 qui manque.
- Sur téléphone, ajoute un dîner et attends « Synchronisé ». Il doit
  rester dans la ligne **Dîner**.

Une fois déployé et vérifié, **supprimer ce fichier**.
