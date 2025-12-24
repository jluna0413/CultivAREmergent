// Centralized runtime configuration loaded from .env files

import 'package:flutter/foundation.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class AppConstants {
  AppConstants._();

  static const String appName = 'Cultivar';

  // Storage Keys
  static const String accessTokenKey = 'access_token';
  static const String refreshTokenKey = 'refresh_token';

  // Default values
  static const String _defaultWsBaseUrl = 'ws://127.0.0.1:7100/ws';
  static const int _defaultTimeoutMs = 30000;

  // Environment driven configuration
  static String get apiBaseUrl {
    if (kIsWeb) {
      return dotenv.env['API_BASE_URL'] ?? 'http://127.0.0.1:4205';
    }
    if (defaultTargetPlatform == TargetPlatform.android) {
      return dotenv.env['API_BASE_URL'] ?? 'http://10.0.2.2:4205';
    }
    return dotenv.env['API_BASE_URL'] ?? 'http://127.0.0.1:4205';
  }

  static String get wsBaseUrl => _normalizeUrl(
    dotenv.env['WS_BASE_URL'],
    fallback: _defaultWsBaseUrl,
    stripTrailingSlash: false,
  );

  static const int apiTimeoutMs = _defaultTimeoutMs;

  static bool get enableLogging =>
      _boolFromEnv('ENABLE_LOGGING', fallback: true);

  static bool get logNetworkTraffic =>
      _boolFromEnv('LOG_NETWORK_TRAFFIC', fallback: enableLogging);

  static bool get offlineModeEnabled =>
      _boolFromEnv('ENABLE_OFFLINE_MODE', fallback: false);

  // API endpoints (relative to apiBaseUrl)
  static const String authLogin = '/auth/login';
  static const String authRefresh = '/auth/refresh';
  static const String authMe = '/auth/me';
  static const String authLogout = '/auth/logout';
  static const String plantsEndpoint = '/plants';
  static const String dashboardStatsEndpoint = '/dashboard/stats';
  static const String sensorsEndpoint = '/sensors';
  static const String newsletterSubscribeEndpoint = '/newsletter/subscribe';

  // Pagination
  static const int defaultPageSize = 20;

  // Validation
  static const int passwordMinLength = 8;

  // Helper methods
  static bool _boolFromEnv(String key, {required bool fallback}) {
    final raw = dotenv.env[key];
    if (raw == null) return fallback;
    final normalized = raw.trim().toLowerCase();
    if (normalized.isEmpty) return fallback;
    return normalized == 'true' || normalized == '1' || normalized == 'yes';
  }

  static String _normalizeUrl(
    String? value, {
    required String fallback,
    bool stripTrailingSlash = true,
  }) {
    final resolved = (value ?? '').trim().isEmpty ? fallback : value!.trim();
    if (!stripTrailingSlash) {
      return resolved;
    }
    return resolved.endsWith('/')
        ? resolved.substring(0, resolved.length - 1)
        : resolved;
  }
}
