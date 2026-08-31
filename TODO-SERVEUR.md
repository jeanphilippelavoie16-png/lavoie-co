# À ajouter au backend Apps Script : `lireLienWeb`

Le frontend v4.9.0 (« Importer d'Internet ») appelle d'abord `lireLienWeb(url)`
pour n'importe quel lien non-Instagram, et retombe sur `lireLienIG` puis sur le
texte collé/captures tant que cette fonction n'existe pas. **L'app fonctionne
donc déjà**, mais la lecture automatique des sites de recettes n'arrivera
qu'avec ce morceau, à coller dans le projet Apps Script (`serveur/`, clasp) et
à redéployer.

Contrat, identique à `lireLienIG` : rend `{ texte: "..." }` si la page a livré
une recette lisible, `{ besoinTexte: true }` sinon. Jamais d'exception vers le
client pour un site récalcitrant.

```javascript
// Lit n'importe quelle page web et en tire le texte de la recette.
// 1. JSON-LD schema.org/Recipe — le standard des sites de recettes
//    (Ricardo, Marmiton, AllRecipes...) : nom, ingredients, etapes propres.
// 2. Sinon : texte visible de la page, borne, et l'IA de
//    structurerRecetteTexte fait le tri.
function lireLienWeb(url) {
  url = String(url || '').trim();
  if (!/^https?:\/\//i.test(url)) return { besoinTexte: true };
  var res;
  try {
    res = UrlFetchApp.fetch(url, {
      muteHttpExceptions: true,
      followRedirects: true,
      // Sans User-Agent de navigateur, beaucoup de sites servent un 403.
      headers: { 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' }
    });
  } catch (e) { return { besoinTexte: true }; }
  if (res.getResponseCode() >= 400) return { besoinTexte: true };
  var html = res.getContentText();
  var texte = extraireRecetteJsonLd_(html) || htmlVersTexte_(html);
  if (!texte || texte.length < 80) return { besoinTexte: true };
  return { texte: texte.slice(0, 12000) };
}

// Cherche un bloc <script type="application/ld+json"> portant un
// schema.org/Recipe (parfois enfoui dans @graph ou dans un tableau).
function extraireRecetteJsonLd_(html) {
  var re = /<script[^>]*type\s*=\s*["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi;
  var m;
  while ((m = re.exec(html)) !== null) {
    var obj;
    try { obj = JSON.parse(m[1].trim()); } catch (e) { continue; }
    var pile = Array.isArray(obj) ? obj.slice() : [obj];
    while (pile.length) {
      var n = pile.shift();
      if (!n || typeof n !== 'object') continue;
      if (Array.isArray(n['@graph'])) pile = pile.concat(n['@graph']);
      var type = n['@type'];
      var estRecette = type === 'Recipe' || (Array.isArray(type) && type.indexOf('Recipe') >= 0);
      if (!estRecette) continue;
      var lignes = [];
      if (n.name) lignes.push('Recette : ' + n.name);
      if (n.recipeYield) lignes.push('Portions : ' + [].concat(n.recipeYield)[0]);
      var ings = n.recipeIngredient || n.ingredients;
      if (ings && ings.length) {
        lignes.push('', 'Ingrédients :');
        [].concat(ings).forEach(function (i) { lignes.push('- ' + nettoyer_(String(i))); });
      }
      var etapes = aplatirInstructions_(n.recipeInstructions);
      if (etapes.length) {
        lignes.push('', 'Étapes :');
        etapes.forEach(function (s, i) { lignes.push((i + 1) + '. ' + s); });
      }
      if (lignes.length > 2) return lignes.join('\n');
    }
  }
  return '';
}

// recipeInstructions : chaine, tableau de chaines, HowToStep, ou
// HowToSection imbriquant des HowToStep — on aplatit tout.
function aplatirInstructions_(ins) {
  var sortie = [];
  [].concat(ins || []).forEach(function (s) {
    if (!s) return;
    if (typeof s === 'string') { sortie.push(nettoyer_(s)); return; }
    if (Array.isArray(s.itemListElement)) {
      sortie = sortie.concat(aplatirInstructions_(s.itemListElement));
      return;
    }
    if (s.text) sortie.push(nettoyer_(s.text));
    else if (s.name) sortie.push(nettoyer_(s.name));
  });
  return sortie.filter(Boolean);
}

// Le texte visible d'une page, sans scripts ni balises ni entités.
function htmlVersTexte_(html) {
  var t = html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<(br|\/p|\/div|\/li|\/h[1-6]|\/tr)[^>]*>/gi, '\n')
    .replace(/<[^>]+>/g, ' ');
  return nettoyer_(t);
}

function nettoyer_(t) {
  return String(t)
    .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#0?39;/g, "'")
    .replace(/&#(\d+);/g, function (_, c) { return String.fromCharCode(+c); })
    .replace(/[ \t]+/g, ' ')
    .replace(/\s*\n\s*/g, '\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}
```

Et dans le routeur des fonctions exposées (là où `lireLienIG` est déclaré),
ajouter `lireLienWeb` à la liste des fonctions permises.

Une fois collé, déployé et vérifié (le frontend n'a pas besoin de changer :
il essaie déjà `lireLienWeb` en premier), **supprimer ce fichier**.
