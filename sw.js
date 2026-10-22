// sw.js EasyCache
self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open('crosspix-v1').then((cache) => {
            return cache.addAll([
                './',
                './index.html',
                './data.json',
                './neighbors.json'
            ]);
        })
    );
});

self.addEventListener('fetch', (e) => {
    e.respondWith(
        caches.match(e.request).then((response) => {
            return response || fetch(e.request);
        })
    );
});