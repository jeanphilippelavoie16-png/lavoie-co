/* Service Worker — Lavoie & Co (Étape 2 : interface offline + auto-mise à jour)
   - "Réseau d'abord" pour l'app : quand tu es en ligne, l'app la plus récente est servie
     et mise en cache ; hors ligne, on sert la dernière version en cache.
   - Les DONNÉES (recettes, listes…) sont gérées séparément par localStorage dans l'app.
   IMPORTANT : à chaque mise à jour de l'app, incrémente CACHE_VERSION (v2 → v3 …). */
var CACHE_VERSION = 'lavoie-co-v3';
var CORE_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './icon-180.png'
];

// Installation : met en cache les fichiers de base et s'active tout de suite
self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE_VERSION).then(function (cache) {
      return cache.addAll(CORE_ASSETS);
    }).then(function () { return self.skipWaiting(); })
  );
});

// Activation : supprime les vieux caches (donc l'ancienne version disparaît)
self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        if (k !== CACHE_VERSION) return caches.delete(k);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (e) {
  var url = e.request.url;

  // Les appels à l'API Apps Script ont besoin du réseau → on ne les touche pas.
  if (url.indexOf('/exec') >= 0 || url.indexOf('script.google.com') >= 0 || url.indexOf('googleusercontent') >= 0) {
    return;
  }

  // Pour l'interface : RÉSEAU D'ABORD, cache en secours.
  // → en ligne, tu as toujours la dernière version ; hors ligne, tu as la dernière version connue.
  e.respondWith(
    fetch(e.request).then(function (resp) {
      if (resp && resp.status === 200 && (resp.type === 'basic' || resp.type === 'cors')) {
        var copy = resp.clone();
        caches.open(CACHE_VERSION).then(function (cache) { cache.put(e.request, copy); });
      }
      return resp;
    }).catch(function () {
      // hors ligne → on sert depuis le cache
      return caches.match(e.request).then(function (cached) {
        return cached || caches.match('./index.html');
      });
    })
  );
});
