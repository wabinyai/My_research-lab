const CACHE_NAME = 'air-quality-cache-v1';
const urlsToCache = [
    '/',
    '/heatmap-data?lat_north=90&lat_south=-90&lon_east=180&lon_west=-180',
    'https://api.mapbox.com/mapbox-gl-js/v3.5.1/mapbox-gl.js',
    'https://api.mapbox.com/mapbox-gl-js/v3.5.1/mapbox-gl.css'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                if (response) {
                    return response;
                }
                return fetch(event.request).then(
                    (response) => {
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }
                        const responseToCache = response.clone();
                        caches.open(CACHE_NAME)
                            .then((cache) => {
                                cache.put(event.request, responseToCache);
                            });
                        return response;
                    }
                );
            })
    );
});
