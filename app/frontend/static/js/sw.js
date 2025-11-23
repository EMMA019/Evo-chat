const CACHE_NAME = 'evo-persona-v1';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/js/script.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

// 【修正】Network First 戦略に変更
// まずネットワーク（サーバー）に最新を取りに行き、失敗したら（オフラインなど）キャッシュを使う
self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // 正常に取得できたら、次回のためにキャッシュも更新しておく
        if (!response || response.status !== 200 || response.type !== 'basic') {
          return response;
        }
        
        const responseToCache = response.clone();
        caches.open(CACHE_NAME)
          .then(cache => {
            cache.put(event.request, responseToCache);
          });
          
        return response;
      })
      .catch(() => {
        // オフラインなどで取得できなかった場合はキャッシュを返す
        return caches.match(event.request);
      })
  );
});