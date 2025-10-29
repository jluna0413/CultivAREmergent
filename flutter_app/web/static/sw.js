// Minimal service worker stub to be included in Flutter web builds at /static/sw.js
// This is a minimal, non-intrusive placeholder for development and local testing.

'use strict';

self.addEventListener('install', event => {
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', event => {
  // Default to network for all requests. Keep stub behavior explicit and simple.
  event.respondWith(fetch(event.request));
});
