/* Money Tracker – service worker (tryb offline)
 * Strategia: najpierw sieć, a gdy jej nie ma – ostatnia zapisana kopia.
 * Dzięki temu nowa wersja strony pojawia się od razu, gdy jest internet,
 * a bez internetu aplikacja dalej działa.
 * Przy każdej wersji aplikacji podbij CACHE, żeby stare kopie zostały usunięte.
 */
const CACHE = 'mt-v0.23.7';
const PRECACHE = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png', './icons/icon.svg'];
const NET_TIMEOUT = 4000; // ms – przy słabym zasięgu nie czekamy w nieskończoność

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k.startsWith('mt-') && k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

/* klucz bez parametrów (?123…), żeby content.json?czas nie tworzył nowych kopii przy każdym wejściu */
const keyOf = url => { const u = new URL(url); return u.origin === self.location.origin ? u.origin + u.pathname : url; };

function withTimeout(p, ms) {
  return new Promise((res, rej) => { const t = setTimeout(() => rej(new Error('timeout')), ms); p.then(v => { clearTimeout(t); res(v); }, err => { clearTimeout(t); rej(err); }); });
}

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (!/^https?:$/.test(url.protocol)) return;
  const same = url.origin === self.location.origin;
  /* z zewnętrznych adresów zapisujemy tylko kursy NBP i czcionki/biblioteki – reszta idzie normalnie */
  if (!same && !/(^|\.)nbp\.pl$|fonts\.(googleapis|gstatic)\.com$|cdnjs\.cloudflare\.com$|cdn\.jsdelivr\.net$/.test(url.hostname)) return;

  e.respondWith((async () => {
    const cache = await caches.open(CACHE);
    const key = keyOf(req.url);
    try {
      const fresh = await withTimeout(fetch(req), NET_TIMEOUT);
      if (fresh && (fresh.ok || fresh.type === 'opaque')) cache.put(key, fresh.clone()).catch(() => {});
      return fresh;
    } catch (err) {
      const hit = await cache.match(key) || (req.mode === 'navigate' ? await cache.match(keyOf(new URL('./', self.location).href)) : null);
      if (hit) return hit;
      if (req.mode === 'navigate') return new Response('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><body style="font-family:system-ui;background:#0a0c0f;color:#f0f4f8;display:grid;place-items:center;height:100vh;margin:0;text-align:center"><div><h1>📡 Brak połączenia</h1><p>Ta strona nie była jeszcze zapisana do użytku offline.<br>No connection – this page has not been saved for offline use yet.</p></div></body>', { headers: { 'Content-Type': 'text/html; charset=utf-8' } });
      throw err;
    }
  })());
});
