// Minimal service worker stub to satisfy registration during development.
// This worker does not implement caching and is intentionally simple.

'use strict';

self.addEventListener('install', event => {
  // Activate immediately
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', event => {
  // Default to network; keep this worker minimal and non-intrusive.
  event.respondWith(fetch(event.request));
});
const CACHE_NAME = 'cultivar-v1.0.0';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/css/bootstrap.min.css',
  '/static/css/all.min.css',
  '/static/js/main.js',
  '/static/js/jquery.min.js',
  '/static/js/bootstrap.bundle.min.js',
  '/static/js/chart.min.js',
  '/static/images/favicon-32x32.png',
  '/static/images/logo.png'
];

// Install event
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch event
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Return cached version or fetch from network
        return response || fetch(event.request);
      }
    )
  );
});

// Activate event
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});