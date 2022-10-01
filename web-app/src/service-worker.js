/* eslint-disable */
// This is the code piece that GenerateSW mode can't provide for us.
// This code listens for the user's confirmation to update the app.
console.log('Start Service worker')
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});

workbox.routing.registerRoute(
    new RegExp("http://fonts.(?:googleapis|gstatis).com/(.*)"),
    new workbox.strategies.CacheFirst({
        cacheName: "googleapis",
        plugins: [
            new workbox.expiration.Plugin({
                maxEntries: 30
            })
        ],
        method: "GET",
        cacheableResponse: { status: [0, 200] }
    })
);
workbox.core.setCacheNameDetails({ prefix: "demo" });
workbox.core.clientsClaim(); // Vue CLI 4 and Workbox v4, else
// workbox.clientsClaim(); // Vue CLI 3 and Workbox v3.

// The precaching code provided by Workbox.
self.__precacheManifest = [].concat(self.__precacheManifest || []);
// workbox.precaching.suppressWarnings(); // Only used with Vue CLI 3 and Workbox v3.
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});