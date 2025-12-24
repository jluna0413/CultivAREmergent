import 'dart:developer' as developer;
import 'package:flutter/foundation.dart';

/// Analytics service for tracking user interactions, errors, and performance
/// Currently implements basic logging with stub provider support for Firebase
class AnalyticsService {
  AnalyticsService._internal();
  static AnalyticsService? _instance;
  static AnalyticsService get instance =>
      _instance ??= AnalyticsService._internal();

  // Analytics configuration
  static bool _enabled = false;
  static bool get enabled => _enabled;

  /// Initialize analytics service
  /// Currently enables basic logging - can be extended for Firebase/other providers
  static void initialize({bool enableFirebase = false}) {
    _enabled = true;
    if (kDebugMode) {
      developer.log('Analytics service initialized', name: 'Analytics');
    }

    // Firebase initialization can be added here if enableFirebase is true
    if (enableFirebase) {
      // Initialize Firebase Analytics
      // Firebase.initializeApp();
      // FirebaseAnalytics analytics = FirebaseAnalytics.instance;
    }
  }

  /// Track screen view
  static void trackScreenView(String screenName) {
    if (!_enabled) return;

    final eventData = {
      'screen_name': screenName,
      'timestamp': DateTime.now().toIso8601String(),
    };

    _logEvent('screen_view', eventData);
  }

  /// Track custom event
  static void trackEvent(String eventName, [Map<String, dynamic>? parameters]) {
    if (!_enabled) return;

    final eventData = {
      'event_name': eventName,
      'timestamp': DateTime.now().toIso8601String(),
      if (parameters != null) ...parameters,
    };

    _logEvent(eventName, eventData);
  }

  /// Track user action
  static void trackUserAction(
    String action,
    String screen, [
    Map<String, dynamic>? details,
  ]) {
    if (!_enabled) return;

    final eventData = {
      'action': action,
      'screen': screen,
      'timestamp': DateTime.now().toIso8601String(),
      if (details != null) ...details,
    };

    _logEvent('user_action', eventData);
  }

  /// Track error with context
  static void trackError(
    String error,
    StackTrace? stackTrace, {
    String? context,
    Map<String, dynamic>? additionalData,
  }) {
    if (!_enabled) return;

    final errorData = {
      'error': error,
      'context': context ?? 'Unknown',
      'timestamp': DateTime.now().toIso8601String(),
      'stack_trace': stackTrace?.toString(),
      if (additionalData != null) ...additionalData,
    };

    _logEvent('error', errorData);
  }

  /// Track performance metric
  static void trackPerformance(
    String metricName,
    Duration duration, [
    Map<String, dynamic>? details,
  ]) {
    if (!_enabled) return;

    final performanceData = {
      'metric_name': metricName,
      'duration_ms': duration.inMilliseconds,
      'timestamp': DateTime.now().toIso8601String(),
      if (details != null) ...details,
    };

    _logEvent('performance', performanceData);
  }

  /// Track API call performance
  static void trackApiCall(
    String endpoint,
    String method,
    Duration duration, {
    int? statusCode,
    bool? success,
    String? error,
  }) {
    if (!_enabled) return;

    final apiData = {
      'endpoint': endpoint,
      'method': method,
      'duration_ms': duration.inMilliseconds,
      'timestamp': DateTime.now().toIso8601String(),
      'status_code': statusCode,
      'success': success,
      'error': error,
    };

    _logEvent('api_call', apiData);
  }

  /// Track user engagement
  static void trackUserEngagement(String action, [Map<String, dynamic>? data]) {
    if (!_enabled) return;

    final engagementData = {
      'action': action,
      'timestamp': DateTime.now().toIso8601String(),
      if (data != null) ...data,
    };

    _logEvent('user_engagement', engagementData);
  }

  /// Set user properties
  static void setUserProperties(Map<String, String> properties) {
    if (!_enabled) return;

    final userData = {
      'properties': properties,
      'timestamp': DateTime.now().toIso8601String(),
    };

    _logEvent('user_properties', userData);
  }

  /// Internal logging method
  static void _logEvent(String eventName, Map<String, dynamic> data) {
    if (kDebugMode) {
      developer.log(
        'Analytics Event: $eventName',
        name: 'Analytics',
        error: data.toString(),
      );
    }

    // Firebase Analytics integration would go here
    // Example:
    // FirebaseAnalytics.instance.logEvent(
    //   name: eventName,
    //   parameters: data,
    // );
  }

  /// Flush analytics data (for when app is closing or data needs to be sent)
  static Future<void> flush() async {
    if (!_enabled) return;

    if (kDebugMode) {
      developer.log('Flushing analytics data', name: 'Analytics');
    }

    // Implementation for flushing cached analytics data
    // This would be relevant when using remote analytics services
  }

  /// Reset analytics data (useful for testing or user privacy)
  static void reset() {
    if (!_enabled) return;

    if (kDebugMode) {
      developer.log('Resetting analytics data', name: 'Analytics');
    }

    // Implementation for resetting analytics data
  }
}

/// Extension for convenient analytics tracking in widgets
extension AnalyticsExtension on String {
  void trackScreenView() => AnalyticsService.trackScreenView(this);

  void trackUserAction(String action, [Map<String, dynamic>? details]) =>
      AnalyticsService.trackUserAction(action, this, details);
}
