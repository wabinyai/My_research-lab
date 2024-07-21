const CACHE_NAME = 'air-quality-cache-v2'; // Updated cache name for versioning
const urlsToCache = [
    '/',
    '/heatmap-data?lat_north=90&lat_south=-90&lon_east=180&lon_west=-180',
    'https://api.mapbox.com/mapbox-gl-js/v3.5.1/mapbox-gl.js',
    'https://api.mapbox.com/mapbox-gl-js/v3.5.1/mapbox-gl.css'
];

// Install event: open cache and add all resources to cache
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                return cache.addAll(urlsToCache);
            })
            .catch((error) => {
                console.error('Failed to open cache or add resources:', error);
            })
    );
});

// Activate event: clean up old caches
self.addEventListener('activate', (event) => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (!cacheWhitelist.includes(cacheName)) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Fetch event: serve cached resources if available, otherwise fetch from network and cache the response
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                if (response) {
                    return response;
                }
                return fetch(event.request).then(
                    (networkResponse) => {
                        if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
                            return networkResponse;
                        }
                        const responseToCache = networkResponse.clone();
                        caches.open(CACHE_NAME)
                            .then((cache) => {
                                cache.put(event.request, responseToCache);
                            })
                            .catch((error) => {
                                console.error('Failed to cache response:', error);
                            });
                        return networkResponse;
                    }
                );
            }).catch((error) => {
                console.error('Failed to fetch resource:', error);
            })
    );
});
