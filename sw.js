/* ================================================================
   LAVOIE & CO — Service Worker v4.8.1
   ----------------------------------------------------------------
   Stratégie :
   - Navigation / HTML : réseau d'abord (les mises à jour arrivent
     toujours), cache en secours (l'app ouvre quand même au chalet).
   - Autres fichiers (manifest, icônes) : cache d'abord, mise à jour
     en arrière-plan (stale-while-revalidate).
   - Polices Google (fonts.googleapis.com / fonts.gstatic.com) :
     cache d'abord — le texte garde sa vraie coupe hors ligne.
   - API Apps Script (script.google.com) : JAMAIS touchée par le SW —
     c'est le moteur de sync de l'app qui gère le hors-ligne.
   - skipWaiting + clients.claim : la nouvelle version prend le
     contrôle tout de suite ; l'app se recharge via controllerchange.
   Pour forcer une mise à jour chez tout le monde : change CACHE_NAME.
   ================================================================ */

var CACHE_NAME = 'lco-cache-v4.8.1';
// Les critiques doivent TOUS réussir, sinon l'installation échoue et
// l'ancienne version — avec son cache complet — reste en service.
// Avant v4.8.1 le précache était tolérant pour tout : une mise à jour
// attrapée sur un réseau qui flanche s'installait avec un cache troué,
// détruisait le vieux cache à l'activation, puis rechargeait la page…
// qui n'existait plus nulle part. C'est le bug qui a cassé le hors-ligne.
var PRECACHE_CRITIQUE = ['./', './index.html'];
var PRECACHE_TOLERANT = ['./manifest.json', './icon-180.png'];
var FONT_HOSTS = ['fonts.googleapis.com', 'fonts.gstatic.com'];

self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function (cache) {
      var critiques = Promise.all(PRECACHE_CRITIQUE.map(function (url) {
        // no-cache : on veut la version fraîche de GitHub Pages, pas
        // celle que le cache HTTP du navigateur croit encore bonne.
        return fetch(url, { cache: 'no-cache' }).then(function (res) {
          if (!res || !res.ok) throw new Error('précache ' + url + ' : HTTP ' + (res ? res.status : '?'));
          return cache.put(url, res);
        });
      }));
      var tolerants = Promise.all(PRECACHE_TOLERANT.map(function (url) {
        return cache.add(url).catch(function () {});
      }));
      return Promise.all([critiques, tolerants]);
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

  if (req.method !== 'GET') return;
  var url = new URL(req.url);

  // Hors domaine : seules les polices sont servies depuis le cache.
  // Tout le reste — surtout les appels API vers script.google.com —
  // passe direct au réseau.
  if (url.origin !== self.location.origin) {
    if (FONT_HOSTS.indexOf(url.hostname) >= 0) {
      event.respondWith(
        caches.match(req).then(function (hit) {
          return hit || fetch(req).then(function (res) {
            if (res && res.ok) {
              var copy = res.clone();
              caches.open(CACHE_NAME).then(function (c) { c.put(req, copy).catch(function () {}); });
            }
            return res;
          });
        })
      );
    }
    return;
  }

  var isNav = req.mode === 'navigate' ||
    (req.headers.get('accept') || '').indexOf('text/html') >= 0;

  if (isNav) {
    // Réseau d'abord : garantit qu'une nouvelle version publiée sur
    // GitHub Pages est servie dès qu'il y a du réseau. La copie fraîche
    // est rangée sous les deux clés ('./' et './index.html') : l'app
    // s'ouvre parfois par l'une, parfois par l'autre (PWA vs onglet).
    event.respondWith(
      fetch(req).then(function (res) {
        var c1 = res.clone(), c2 = res.clone();
        caches.open(CACHE_NAME).then(function (c) {
          c.put('./index.html', c1).catch(function () {});
          c.put('./', c2).catch(function () {});
        });
        return res;
      }).catch(function () {
        return caches.match(req).then(function (hit) {
          return hit || caches.match('./index.html');
        }).then(function (hit) {
          return hit || caches.match('./');
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
      }).catch(function () { return hit || Response.error(); });
      return hit || refresh;
    })
  );
});
