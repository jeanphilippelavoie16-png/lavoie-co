/* Service Worker — Lavoie & Co (Étape 1 : cache de l'interface)
   Permet à l'app de S'OUVRIR hors ligne. La mise en cache des DONNÉES
   (recettes, listes…) viendra à l'Étape 2.
   Quand tu modifies l'app, change CACHE_VERSION pour forcer la mise à jour. */
var CACHE_VERSION = 'lavoie-co-v1';
var CORE_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './icon-180.png'
];

// Installation : on met en cache les fichiers de base
self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE_VERSION).then(function (cache) {
      return cache.addAll(CORE_ASSETS);
    }).then(function () { return self.skipWaiting(); })
  );
});

// Activation : on supprime les vieux caches
self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        if (k !== CACHE_VERSION) return caches.delete(k);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

// Interception des requêtes
self.addEventListener('fetch', function (e) {
  var url = e.request.url;

  // Les appels à l'API Apps Script (/exec) NE SONT PAS mis en cache :
  // ils ont besoin du réseau. Si offline, ils échoueront (géré à l'Étape 3).
  if (url.indexOf('/exec') >= 0 || url.indexOf('script.google.com') >= 0 || url.indexOf('googleusercontent') >= 0) {
    return; // laisse passer normalement (réseau)
  }

  // Pour l'interface : "cache d'abord, réseau ensuite"
  // → l'app s'ouvre instantanément et même sans réseau.
  e.respondWith(
    caches.match(e.request).then(function (cached) {
      if (cached) return cached;
      return fetch(e.request).then(function (resp) {
        // on met en cache les nouveaux fichiers de l'app au passage
        if (resp && resp.status === 200 && resp.type === 'basic') {
          var copy = resp.clone();
          caches.open(CACHE_VERSION).then(function (cache) { cache.put(e.request, copy); });
        }
        return resp;
      }).catch(function () {
        // hors ligne et pas en cache → on tente au moins de servir l'app
        return caches.match('./index.html');
      });
    })
  );
});
