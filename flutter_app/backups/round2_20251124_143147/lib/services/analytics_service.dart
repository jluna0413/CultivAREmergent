/// Analytics service for CultivAREmergant
/// Integrates with Firebase Analytics and provides custom tracking
library;

import 'package:firebase_analytics/firebase_analytics.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import '../config/environment.dart';

class AnalyticsService {
  static FirebaseAnalytics get _analytics => FirebaseAnalytics.instance;
  static FirebaseCrashlytics get _crashlytics => FirebaseCrashlytics.instance;

  /// Initialize analytics service based on environment
  static Future<void> initialize() async {
    if (!EnvironmentConfig.analyticsEnabled) {
      return;
    }

    try {
      // Set user properties
      await _setUserProperties();

      // Set custom event parameters
      await _setDefaultParameters();

      // Initialize crash reporting
      await _initializeCrashReporting();

      if (EnvironmentConfig.isDevelopment) {
        await _analytics.setAnalyticsCollectionEnabled(false);
      }
    } catch (e) {
      // Log error without analytics to avoid infinite loops
      print('Analytics initialization failed: $e');
    }
  }

  /// Track custom events
  static Future<void> trackEvent(
    String eventName, {
    Map<String, dynamic>? parameters,
    bool critical = false,
  }) async {
    if (!EnvironmentConfig.analyticsEnabled) {
      return;
    }

    try {
      await _analytics.logEvent(
        name: eventName,
        parameters: _sanitizeParameters(parameters),
      );

      // Track critical events in Crashlytics as well
      if (critical) {
        await _crashlytics.log('Critical Event: $eventName');
      }
    } catch (e) {
      // Fallback logging
      print('Analytics tracking failed: $e');
    }
  }

  /// Track screen views
  static Future<void> trackScreenView(
    String screenName, {
    String? className,
  }) async {
    if (!EnvironmentConfig.analyticsEnabled) {
      return;
    }

    try {
      await _analytics.logScreenView(
        screenName: screenName,
        screenClass: className ?? screenName,
      );
    } catch (e) {
      print('Screen view tracking failed: $e');
    }
  }

  /// Track user authentication events
  static Future<void> trackAuthentication({
    required String method,
    required bool success,
    String? userId,
    String? errorMessage,
  }) async {
    await trackEvent(
      'user_authentication',
      parameters: {
        'method': method,
        'success': success,
        'user_id': userId,
        'error_message': errorMessage,
      },
    );

    if (!success && errorMessage != null) {
      await _crashlytics.log('Authentication failed: $errorMessage');
    }
  }

  /// Track cultivation events
  static Future<void> trackCultivationEvent({
    required String action,
    required String plantType,
    String? plantId,
    Map<String, dynamic>? additionalData,
  }) async {
    await trackEvent(
      'cultivation_action',
      parameters: {
        'action': action,
        'plant_type': plantType,
        'plant_id': plantId,
        ...?additionalData,
      },
    );
  }

  /// Track sensor data events
  static Future<void> trackSensorEvent({
    required String sensorType,
    required double value,
    required String unit,
    String? deviceId,
    bool abnormal = false,
  }) async {
    await trackEvent(
      'sensor_reading',
      parameters: {
        'sensor_type': sensorType,
        'value': value,
        'unit': unit,
        'device_id': deviceId,
        'abnormal_reading': abnormal,
      },
    );

    // Track abnormal readings as critical events
    if (abnormal) {
      await _crashlytics.log(
        'Abnormal sensor reading: $sensorType = $value $unit',
      );
    }
  }

  /// Track app performance metrics
  static Future<void> trackPerformance({
    required String operation,
    required int durationMs,
    bool success = true,
    String? errorMessage,
  }) async {
    await trackEvent(
      'app_performance',
      parameters: {
        'operation': operation,
        'duration_ms': durationMs,
        'success': success,
        'error_message': errorMessage,
      },
    );
  }

  /// Track feature usage
  static Future<void> trackFeatureUsage({
    required String feature,
    required String action,
    Map<String, dynamic>? metadata,
  }) async {
    await trackEvent(
      'feature_usage',
      parameters: {'feature': feature, 'action': action, ...?metadata},
    );
  }

  /// Track error events
  static Future<void> trackError({
    required String errorType,
    required String errorMessage,
    String? stackTrace,
    String? context,
  }) async {
    await trackEvent(
      'app_error',
      parameters: {
        'error_type': errorType,
        'error_message': errorMessage,
        'context': context,
      },
      critical: true,
    );

    // Also log to Crashlytics
    await _crashlytics.recordError(
      errorType,
      stackTrace ?? StackTrace.current,
      reason: errorMessage,
      context: context,
    );
  }

  /// Set user properties
  static Future<void> setUserProperties(Map<String, String> properties) async {
    if (!EnvironmentConfig.analyticsEnabled) {
      return;
    }

    try {
      for (final entry in properties.entries) {
        await _analytics.setUserProperty(name: entry.key, value: entry.value);
      }
    } catch (e) {
      print('Setting user properties failed: $e');
    }
  }

  /// Track user engagement
  static Future<void> trackUserEngagement({
    required String engagementType,
    required int durationSeconds,
    String? contentId,
    String? contentType,
  }) async {
    await trackEvent(
      'user_engagement',
      parameters: {
        'engagement_type': engagementType,
        'duration_seconds': durationSeconds,
        'content_id': contentId,
        'content_type': contentType,
      },
    );
  }

  /// Track conversion events
  static Future<void> trackConversion({
    required String conversionType,
    required double value,
    String? currency,
    String? itemId,
  }) async {
    await trackEvent(
      'conversion',
      parameters: {
        'conversion_type': conversionType,
        'value': value,
        'currency': currency,
        'item_id': itemId,
      },
    );
  }

  /// Private methods
  static Future<void> _setUserProperties() async {
    await _analytics.setUserId(
      // Don't set user ID in development for privacy
      EnvironmentConfig.isProduction ? null : null,
    );

    await _analytics.setUserProperty(
      name: 'app_version',
      value: EnvironmentConfig.appVersion,
    );

    await _analytics.setUserProperty(
      name: 'build_type',
      value: EnvironmentConfig.environmentName,
    );

    await _analytics.setUserProperty(
      name: 'platform',
      value: 'android', // Could be made dynamic
    );
  }

  static Future<void> _setDefaultParameters() async {
    // Set global parameters that should be included with all events
    // This is handled automatically by Firebase Analytics
  }

  static Future<void> _initializeCrashReporting() async {
    if (!EnvironmentConfig.crashReportingEnabled) {
      return;
    }

    // Enable crash collection in non-production environments for testing
    if (EnvironmentConfig.isDevelopment) {
      await _crashlytics.setCrashlyticsCollectionEnabled(true);
    }

    // Set custom keys for crash reporting
    await _crashlytics.setCustomKey(
      'app_version',
      EnvironmentConfig.appVersion,
    );
    await _crashlytics.setCustomKey(
      'environment',
      EnvironmentConfig.environmentName,
    );
    await _crashlytics.setCustomKey('platform', 'android');
  }

  static Map<String, dynamic> _sanitizeParameters(
    Map<String, dynamic>? parameters,
  ) {
    if (parameters == null) {
      return {};
    }

    final sanitized = <String, dynamic>{};

    for (final entry in parameters.entries) {
      // Ensure parameter names are valid
      final key = entry.key.replaceAll(RegExp(r'[^a-zA-Z0-9_]'), '_');

      // Ensure parameter values are not too large
      final value = entry.value;
      if (value is String && value.length > 100) {
        sanitized[key] = '${value.substring(0, 97)}...';
      } else {
        sanitized[key] = value;
      }
    }

    return sanitized;
  }

  /// Test analytics setup (development only)
  static Future<void> testAnalyticsSetup() async {
    if (!EnvironmentConfig.isDevelopment) {
      return;
    }

    await trackEvent(
      'analytics_test',
      parameters: {
        'test_timestamp': DateTime.now().millisecondsSinceEpoch,
        'environment': EnvironmentConfig.environmentName,
      },
    );

    await trackScreenView('TestScreen', className: 'AnalyticsService');
  }
}

/// Analytics event names - maintain consistency across the app
class AnalyticsEvents {
  // Authentication
  static const String userLogin = 'user_login';
  static const String userLogout = 'user_logout';
  static const String userRegistration = 'user_registration';

  // Navigation
  static const String screenView = 'screen_view';

  // Cultivation
  static const String plantCreated = 'plant_created';
  static const String plantUpdated = 'plant_updated';
  static const String plantDeleted = 'plant_deleted';
  static const String harvestRecorded = 'harvest_recorded';

  // Sensors
  static const String sensorConnected = 'sensor_connected';
  static const String sensorDisconnected = 'sensor_disconnected';
  static const String sensorDataReceived = 'sensor_data_received';

  // Commerce
  static const String productViewed = 'product_viewed';
  static const String addToCart = 'add_to_cart';
  static const String purchaseCompleted = 'purchase_completed';

  // Errors
  static const String apiError = 'api_error';
  static const String appCrash = 'app_crash';

  // Performance
  static const String appStart = 'app_start';
  static const String apiCall = 'api_call';
}
