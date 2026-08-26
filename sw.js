/* ================================================================
   LAVOIE & CO — Service Worker v4.3.1
   ----------------------------------------------------------------
   Stratégie :
   - Navigation / HTML : réseau d'abord (les mises à jour arrivent
     toujours), cache en secours (l'app ouvre quand même au chalet).
   - Autres fichiers (manifest, icônes) : cache d'abord, mise à jour
     en arrière-plan (stale-while-revalidate).
   - API Apps Script (script.google.com) : JAMAIS touchée par le SW —
     c'est le moteur de sync de l'app qui gère le hors-ligne.
   - skipWaiting + clients.claim : la nouvelle version prend le
     contrôle tout de suite ; l'app se recharge via controllerchange.
   Pour forcer une mise à jour chez tout le monde : change CACHE_NAME.
   ================================================================ */

var CACHE_NAME = 'lco-cache-v4.3.1';
var PRECACHE = ['./', './index.html', './manifest.json', './icon-180.png'];

self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function (cache) {
      // Précache tolérant : un fichier manquant (ex. icône) ne bloque pas l'installation.
      return Promise.all(PRECACHE.map(function (url) {
        return cache.add(url).catch(function () {});
      }));
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        if (k !== CACHE_NAME) return caches.delete(k);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (event) {
  var req = event.request;

  // On ne gère que les GET du même domaine (GitHub Pages).
  // Tout le reste — surtout les appels API vers script.google.com — passe direct au réseau.
  if (req.method !== 'GET') return;
  var url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  var isNav = req.mode === 'navigate' ||
    (req.headers.get('accept') || '').indexOf('text/html') >= 0;

  if (isNav) {
    // Réseau d'abord : garantit qu'une nouvelle version publiée sur
    // GitHub Pages est servie dès qu'il y a du réseau.
    event.respondWith(
      fetch(req).then(function (res) {
        var copy = res.clone();
        caches.open(CACHE_NAME).then(function (c) { c.put('./index.html', copy).catch(function () {}); });
        return res;
      }).catch(function () {
        return caches.match(req).then(function (hit) {
          return hit || caches.match('./index.html');
        });
      })
    );
    return;
  }

  // Assets : cache d'abord, rafraîchissement silencieux en arrière-plan.
  event.respondWith(
    caches.match(req).then(function (hit) {
      var refresh = fetch(req).then(function (res) {
        if (res && res.ok) {
          var copy = res.clone();
          caches.open(CACHE_NAME).then(function (c) { c.put(req, copy).catch(function () {}); });
        }
        return res;
      }).catch(function () { return hit; });
      return hit || refresh;
    })
  );
});
