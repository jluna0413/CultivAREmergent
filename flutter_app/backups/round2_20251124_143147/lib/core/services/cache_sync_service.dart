/// Cache & Synchronization Service
/// Handles offline caching, data synchronization, and background sync operations
library;
// (removed stray library directive)

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';
import 'dart:io';
import 'dart:async';

import 'api_client.dart';
import '../logging.dart';

/// Cache configuration
class CacheConfig {
  static const String _cachePrefix = 'cultivar_cache_';
  static const String _syncStatusKey = 'sync_status';

  static const Duration _defaultTtl = Duration(
    hours: 1,
  ); // Default TTL for cached data
  static const Duration _maxSyncAge = Duration(
    hours: 24,
  ); // Maximum age before forcing sync

  // Cache keys
  static const String _plantsCacheKey = '${_cachePrefix}plants';
  static const String _cultivarsCacheKey = '${_cachePrefix}cultivars';
  static const String _sensorsCacheKey = '${_cachePrefix}sensors';
  static const String _cartCacheKey = '${_cachePrefix}cart';
  static const String _productsCacheKey = '${_cachePrefix}products';
  static const String _ordersCacheKey = '${_cachePrefix}orders';
  static const String _settingsCacheKey = '${_cachePrefix}settings';
  static const String _lastSyncKey = '${_cachePrefix}last_sync';
}

/// Cache entry model
class CacheEntry<T> {
  CacheEntry({
    required this.key,
    required this.data,
    required this.timestamp,
    this.ttl = const Duration(hours: 1),
  });

  factory CacheEntry.fromJson(Map<String, dynamic> json) => CacheEntry(
    key: json['key'] as String,
    data: _decodeData<T>(json['data']),
    timestamp: DateTime.parse(json['timestamp'] as String),
    ttl: Duration(milliseconds: json['ttl'] as int),
  );
  final String key;
  final T data;
  final DateTime timestamp;
  final Duration ttl;

  bool get isExpired => DateTime.now().difference(timestamp) > ttl;

  Map<String, dynamic> toJson() => {
    'key': key,
    'data': _encodeData(data),
    'timestamp': timestamp.toIso8601String(),
    'ttl': ttl.inMilliseconds,
  };

  static dynamic _encodeData(dynamic data) {
    return data;
  }

  static T _decodeData<T>(dynamic data) {
    return data as T;
  }
}

/// Sync operation status
class SyncStatus {
  SyncStatus({
    required this.endpoint,
    required this.lastSync,
    required this.isOnline,
    required this.pendingOperations,
  });

  factory SyncStatus.fromJson(Map<String, dynamic> json) => SyncStatus(
    endpoint: json['endpoint'],
    lastSync: DateTime.parse(json['lastSync']),
    isOnline: json['isOnline'] ?? true,
    pendingOperations: json['pendingOperations'] ?? 0,
  );
  final String endpoint;
  final DateTime lastSync;
  final bool isOnline;
  final int pendingOperations;

  Map<String, dynamic> toJson() => {
    'endpoint': endpoint,
    'lastSync': lastSync.toIso8601String(),
    'isOnline': isOnline,
    'pendingOperations': pendingOperations,
  };
}

/// Cache & Sync Service
class CacheSyncService {
  CacheSyncService(this._apiClient);
  final ApiClient _apiClient;
  late SharedPreferences _prefs;
  bool _isInitialized = false;
  Timer? _backgroundSyncTimer;

  // In-memory cache for better performance
  final Map<String, CacheEntry> _memoryCache = {};
  final Map<String, SyncStatus> _syncStatuses = {};

  /// Initialize cache and synchronization services
  Future<void> initialize() async {
    if (_isInitialized) return;

    try {
      _prefs = await SharedPreferences.getInstance();
      _isInitialized = true;

      // Load sync statuses from storage
      await _loadSyncStatuses();

      // Start background sync timer
      _startBackgroundSyncTimer();

      AppLogger.log('Cache & Sync service initialized successfully');
    } catch (e) {
      AppLogger.error('Failed to initialize Cache & Sync service', e);
      rethrow;
    }
  }

  /// Load sync statuses from shared preferences
  Future<void> _loadSyncStatuses() async {
    try {
      final syncStatusJson = _prefs.getString(CacheConfig._syncStatusKey);
      if (syncStatusJson != null) {
        final Map<String, dynamic> statuses = jsonDecode(syncStatusJson);
        for (final entry in statuses.entries) {
          _syncStatuses[entry.key] = SyncStatus.fromJson(entry.value);
        }
      }
    } catch (e) {
      AppLogger.error('Failed to load sync statuses', e);
    }
  }

  /// Save sync statuses to shared preferences
  Future<void> _saveSyncStatuses() async {
    try {
      final Map<String, dynamic> statuses = {};
      for (final entry in _syncStatuses.entries) {
        statuses[entry.key] = entry.value.toJson();
      }
      await _prefs.setString(CacheConfig._syncStatusKey, jsonEncode(statuses));
    } catch (e) {
      AppLogger.error('Failed to save sync statuses', e);
    }
  }

  // Cache Operations

  /// Cache API response
  Future<void> cacheResponse<T>(String key, T data, {Duration? ttl}) async {
    if (!_isInitialized) await initialize();

    try {
      final entry = CacheEntry<T>(
        key: key,
        data: data,
        timestamp: DateTime.now(),
        ttl: ttl ?? CacheConfig._defaultTtl,
      );

      // Store in memory cache
      _memoryCache[key] = entry;

      // Store in persistent cache (optional, for persistence across app restarts)
      await _prefs.setString(key, jsonEncode(entry.toJson()));

      AppLogger.log('Cached response for key: $key');
    } catch (e) {
      AppLogger.error('Failed to cache response for key: $key', e);
    }
  }

  /// Get cached response
  Future<T?> getCachedResponse<T>(String key) async {
    if (!_isInitialized) await initialize();

    try {
      // Check memory cache first (faster)
      final memoryEntry = _memoryCache[key];
      if (memoryEntry != null && !memoryEntry.isExpired) {
        AppLogger.log('Retrieved response from memory cache for key: $key');
        return memoryEntry.data as T;
      }

      // Check persistent cache
      final jsonData = _prefs.getString(key);
      if (jsonData == null) return null;

      final entry = CacheEntry.fromJson(jsonDecode(jsonData)) as CacheEntry<T>;

      if (entry.isExpired) {
        await _prefs.remove(key);
        _memoryCache.remove(key);
        AppLogger.log('Expired cache removed for key: $key');
        return null;
      }

      // Update memory cache
      _memoryCache[key] = entry;

      AppLogger.log('Retrieved cached response for key: $key');
      return entry.data;
    } catch (e) {
      AppLogger.error('Failed to get cached response for key: $key', e);
      return null;
    }
  }

  /// Clear expired cache entries
  Future<void> clearExpiredCache() async {
    if (!_isInitialized) await initialize();

    try {
      final keysToDelete = <String>[];

      // Check memory cache
      for (final entry in _memoryCache.entries) {
        if (entry.value.isExpired) {
          keysToDelete.add(entry.key);
        }
      }

      // Check persistent cache
      final keys = _prefs.getKeys();
      for (final key in keys) {
        if (key.startsWith(CacheConfig._cachePrefix)) {
          final jsonData = _prefs.getString(key);
          if (jsonData != null) {
            try {
              final entry = CacheEntry.fromJson(jsonDecode(jsonData));
              if (entry.isExpired) {
                keysToDelete.add(key);
              }
            } catch (e) {
              // Invalid JSON, remove it
              keysToDelete.add(key);
            }
          }
        }
      }

      // Remove expired entries
      for (final key in keysToDelete) {
        await _prefs.remove(key);
        _memoryCache.remove(key);
      }

      AppLogger.log('Cleared ${keysToDelete.length} expired cache entries');
    } catch (e) {
      AppLogger.error('Failed to clear expired cache', e);
    }
  }

  /// Clear all cache
  Future<void> clearAllCache() async {
    if (!_isInitialized) await initialize();

    try {
      final keys = _prefs.getKeys();
      for (final key in keys) {
        if (key.startsWith(CacheConfig._cachePrefix)) {
          await _prefs.remove(key);
        }
      }

      _memoryCache.clear();
      AppLogger.log('All cache cleared');
    } catch (e) {
      AppLogger.error('Failed to clear all cache', e);
    }
  }

  // API Caching Methods

  /// Get plants with cache
  Future<List<dynamic>> getPlantsWithCache() async {
    const cacheKey = CacheConfig._plantsCacheKey;
    final cached = await getCachedResponse<List<dynamic>>(cacheKey);

    if (cached != null) {
      AppLogger.log('Retrieved plants from cache');
      return cached;
    }

    try {
      final plants = await _apiClient.getPlants();
      await cacheResponse(cacheKey, plants);
      await _updateSyncStatus('plants');
      return plants;
    } catch (e) {
      AppLogger.error('Failed to fetch plants with cache', e);
      return cached ?? [];
    }
  }

  /// Get cultivars with cache
  Future<List<dynamic>> getCultivarsWithCache() async {
    const cacheKey = CacheConfig._cultivarsCacheKey;
    final cached = await getCachedResponse<List<dynamic>>(cacheKey);

    if (cached != null) {
      AppLogger.log('Retrieved cultivars from cache');
      return cached;
    }

    try {
      final cultivars = await _apiClient.getCultivars();
      await cacheResponse(cacheKey, cultivars);
      await _updateSyncStatus('cultivars');
      return cultivars;
    } catch (e) {
      AppLogger.error('Failed to fetch cultivars with cache', e);
      return cached ?? [];
    }
  }

  /// Get sensors with cache
  Future<List<dynamic>> getSensorsWithCache() async {
    const cacheKey = CacheConfig._sensorsCacheKey;
    final cached = await getCachedResponse<List<dynamic>>(cacheKey);

    if (cached != null) {
      AppLogger.log('Retrieved sensors from cache');
      return cached;
    }

    try {
      final sensors = await _apiClient.getSensors();
      await cacheResponse(cacheKey, sensors);
      await _updateSyncStatus('sensors');
      return sensors;
    } catch (e) {
      AppLogger.error('Failed to fetch sensors with cache', e);
      return cached ?? [];
    }
  }

  /// Get cart with cache
  Future<List<dynamic>> getCartWithCache() async {
    const cacheKey = CacheConfig._cartCacheKey;
    final cached = await getCachedResponse<List<dynamic>>(cacheKey);

    if (cached != null) {
      AppLogger.log('Retrieved cart from cache');
      return cached;
    }

    try {
      final cart = await _apiClient.getCartItems();
      await cacheResponse(cacheKey, cart);
      await _updateSyncStatus('cart');
      return cart;
    } catch (e) {
      AppLogger.error('Failed to fetch cart with cache', e);
      return cached ?? [];
    }
  }

  /// Get products with cache
  Future<List<dynamic>> getProductsWithCache({
    int page = 1,
    int pageSize = 20,
  }) async {
    final cacheKey = '${CacheConfig._productsCacheKey}_$page';
    final cached = await getCachedResponse<List<dynamic>>(cacheKey);

    if (cached != null) {
      AppLogger.log('Retrieved products from cache');
      return cached;
    }

    try {
      final products = await _apiClient.getProductsPaginated(
        page: page,
        pageSize: pageSize,
      );
      await cacheResponse(cacheKey, products, ttl: const Duration(minutes: 30));
      await _updateSyncStatus('products');
      return products;
    } catch (e) {
      AppLogger.error('Failed to fetch products with cache', e);
      return cached ?? [];
    }
  }

  // Synchronization Operations

  /// Update sync status for an endpoint
  Future<void> _updateSyncStatus(String endpoint) async {
    if (!_isInitialized) await initialize();

    try {
      final isOnline = await _checkNetworkConnectivity();
      final existing =
          _syncStatuses[endpoint] ??
          SyncStatus(
            endpoint: endpoint,
            lastSync: DateTime.fromMillisecondsSinceEpoch(0),
            isOnline: isOnline,
            pendingOperations: 0,
          );

      _syncStatuses[endpoint] = SyncStatus(
        endpoint: endpoint,
        lastSync: DateTime.now(),
        isOnline: isOnline,
        pendingOperations: existing.pendingOperations,
      );

      await _saveSyncStatuses();
    } catch (e) {
      AppLogger.error('Failed to update sync status', e);
    }
  }

  /// Check network connectivity
  Future<bool> _checkNetworkConnectivity() async {
    try {
      final result = await InternetAddress.lookup('google.com');
      return result.isNotEmpty && result[0].rawAddress.isNotEmpty;
    } catch (e) {
      return false;
    }
  }

  /// Get sync status for an endpoint
  Future<SyncStatus?> getSyncStatus(String endpoint) async {
    if (!_isInitialized) await initialize();

    final status = _syncStatuses[endpoint];
    if (status == null) return null;

    // Update online status
    final isOnline = await _checkNetworkConnectivity();
    if (status.isOnline != isOnline) {
      _syncStatuses[endpoint] = SyncStatus(
        endpoint: status.endpoint,
        lastSync: status.lastSync,
        isOnline: isOnline,
        pendingOperations: status.pendingOperations,
      );
      await _saveSyncStatuses();
    }

    return _syncStatuses[endpoint];
  }

  /// Check if sync is needed based on last sync time
  Future<bool> isSyncNeeded(String endpoint) async {
    final status = await getSyncStatus(endpoint);
    if (status == null) return true;

    final age = DateTime.now().difference(status.lastSync);
    return age > CacheConfig._maxSyncAge;
  }

  // Background Synchronization

  /// Start background sync timer
  void _startBackgroundSyncTimer() {
    _backgroundSyncTimer = Timer.periodic(
      const Duration(minutes: 15),
      (timer) => _performBackgroundSync(),
    );
  }

  /// Stop background sync timer
  void _stopBackgroundSyncTimer() {
    _backgroundSyncTimer?.cancel();
    _backgroundSyncTimer = null;
  }

  /// Perform background synchronization
  Future<void> _performBackgroundSync() async {
    AppLogger.log('Starting background synchronization');

    try {
      final isOnline = await _checkNetworkConnectivity();
      if (!isOnline) {
        AppLogger.log('No network connection, skipping background sync');
        return;
      }

      await clearExpiredCache();

      // Sync critical data if needed
      final syncTasks = [
        _syncPlantsData(),
        _syncCultivarsData(),
        _syncCartData(),
        _syncProductsData(),
      ];

      await Future.wait(syncTasks);

      AppLogger.log('Background synchronization completed');
    } catch (e) {
      AppLogger.error('Background synchronization failed', e);
    }
  }

  /// Sync plants data
  Future<void> _syncPlantsData() async {
    try {
      if (await isSyncNeeded('plants')) {
        final plants = await _apiClient.getPlants();
        await cacheResponse(CacheConfig._plantsCacheKey, plants);
        AppLogger.log('Plants data synchronized');
      }
    } catch (e) {
      AppLogger.error('Failed to sync plants data', e);
    }
  }

  /// Sync cultivars data
  Future<void> _syncCultivarsData() async {
    try {
      if (await isSyncNeeded('cultivars')) {
        final cultivars = await _apiClient.getCultivars();
        await cacheResponse(CacheConfig._cultivarsCacheKey, cultivars);
        AppLogger.log('Cultivars data synchronized');
      }
    } catch (e) {
      AppLogger.error('Failed to sync cultivars data', e);
    }
  }

  /// Sync cart data
  Future<void> _syncCartData() async {
    try {
      final cart = await _apiClient.getCartItems();
      await cacheResponse(CacheConfig._cartCacheKey, cart);
      AppLogger.log('Cart data synchronized');
    } catch (e) {
      AppLogger.error('Failed to sync cart data', e);
    }
  }

  /// Sync products data
  Future<void> _syncProductsData() async {
    try {
      final products = await _apiClient.getProducts();
      await cacheResponse(CacheConfig._productsCacheKey, products);
      AppLogger.log('Products data synchronized');
    } catch (e) {
      AppLogger.error('Failed to sync products data', e);
    }
  }

  // Utility Methods

  /// Get cache statistics
  Future<Map<String, dynamic>> getCacheStatistics() async {
    if (!_isInitialized) await initialize();

    try {
      final memoryCacheCount = _memoryCache.length;
      final persistentCacheCount = _prefs
          .getKeys()
          .where((key) => key.startsWith(CacheConfig._cachePrefix))
          .length;

      final onlineEndpoints = _syncStatuses.values
          .where((status) => status.isOnline)
          .length;

      final totalPendingOps = _syncStatuses.values.fold(
        0,
        (sum, status) => sum + status.pendingOperations,
      );

      return {
        'memory_cache_entries': memoryCacheCount,
        'persistent_cache_entries': persistentCacheCount,
        'online_endpoints': onlineEndpoints,
        'total_sync_endpoints': _syncStatuses.length,
        'pending_operations': totalPendingOps,
        'is_online': await _checkNetworkConnectivity(),
      };
    } catch (e) {
      AppLogger.error('Failed to get cache statistics', e);
      return {};
    }
  }

  /// Force refresh all data
  Future<void> forceRefreshAll() async {
    AppLogger.log('Forcing refresh of all cached data');

    try {
      await clearExpiredCache();
      await _performBackgroundSync();

      // Update all sync statuses
      for (final endpoint in [
        'plants',
        'cultivars',
        'sensors',
        'cart',
        'products',
      ]) {
        await _updateSyncStatus(endpoint);
      }

      AppLogger.log('All data refreshed successfully');
    } catch (e) {
      AppLogger.error('Failed to force refresh all data', e);
    }
  }

  /// Get offline status
  Future<bool> isOffline() async {
    return !(await _checkNetworkConnectivity());
  }

  /// Get cached data when offline
  Future<List<dynamic>> getOfflineData(String type) async {
    switch (type) {
      case 'plants':
        return await getCachedResponse<List<dynamic>>(
              CacheConfig._plantsCacheKey,
            ) ??
            [];
      case 'cultivars':
        return await getCachedResponse<List<dynamic>>(
              CacheConfig._cultivarsCacheKey,
            ) ??
            [];
      case 'sensors':
        return await getCachedResponse<List<dynamic>>(
              CacheConfig._sensorsCacheKey,
            ) ??
            [];
      case 'cart':
        return await getCachedResponse<List<dynamic>>(
              CacheConfig._cartCacheKey,
            ) ??
            [];
      case 'products':
        return await getCachedResponse<List<dynamic>>(
              CacheConfig._productsCacheKey,
            ) ??
            [];
      default:
        return [];
    }
  }

  /// Dispose resources
  Future<void> dispose() async {
    try {
      _stopBackgroundSyncTimer();
      await _saveSyncStatuses();
      _isInitialized = false;
      AppLogger.log('Cache & Sync service disposed');
    } catch (e) {
      AppLogger.error('Failed to dispose Cache & Sync service', e);
    }
  }
}

/// Provider for CacheSyncService
final cacheSyncServiceProvider = Provider<CacheSyncService>((ref) {
  final apiClient = ApiClient();
  return CacheSyncService(apiClient);
});
