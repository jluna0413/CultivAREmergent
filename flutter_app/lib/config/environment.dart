/// Environment configuration for CultivAREmergant
/// Handles different build variants and environment-specific settings
library;

enum BuildEnvironment { development, staging, production }

class EnvironmentConfig {
  static const String appName = 'CultivAREmergant';
  static const String appVersion = '1.0.0';
  static const String appBuildNumber = '1';

  // Environment-specific configurations
  static final Map<BuildEnvironment, EnvironmentData> _configs = {
    BuildEnvironment.development: const EnvironmentData(
      environment: BuildEnvironment.development,
      apiBaseUrl: 'https://dev-api.cultivaremergant.app',
      wsUrl: 'wss://dev-ws.cultivaremergant.app',
      analyticsEnabled: false,
      crashReportingEnabled: false,
      debugModeEnabled: true,
      networkTimeout: 30,
      enableLogging: true,
      logLevel: 'debug',
      baseImageUrl: 'https://dev-images.cultivaremergant.app',
      cdnUrl: 'https://dev-cdn.cultivaremergant.app',
      firebaseProjectId: 'cultivaremergant-dev',
      enableRemoteConfig: true,
      featureFlags: {
        'advanced_sensors': true,
        'ai_insights': false,
        'social_features': false,
        'premium_features': false,
      },
    ),
    BuildEnvironment.staging: const EnvironmentData(
      environment: BuildEnvironment.staging,
      apiBaseUrl: 'https://staging-api.cultivaremergant.app',
      wsUrl: 'wss://staging-ws.cultivaremergant.app',
      analyticsEnabled: true,
      crashReportingEnabled: true,
      debugModeEnabled: false,
      networkTimeout: 20,
      enableLogging: true,
      logLevel: 'info',
      baseImageUrl: 'https://staging-images.cultivaremergant.app',
      cdnUrl: 'https://staging-cdn.cultivaremergant.app',
      firebaseProjectId: 'cultivaremergant-staging',
      enableRemoteConfig: true,
      featureFlags: {
        'advanced_sensors': true,
        'ai_insights': true,
        'social_features': true,
        'premium_features': false,
      },
    ),
    BuildEnvironment.production: const EnvironmentData(
      environment: BuildEnvironment.production,
      apiBaseUrl: 'https://api.cultivaremergant.app',
      wsUrl: 'wss://ws.cultivaremergant.app',
      analyticsEnabled: true,
      crashReportingEnabled: true,
      debugModeEnabled: false,
      networkTimeout: 15,
      enableLogging: true,
      logLevel: 'error',
      baseImageUrl: 'https://images.cultivaremergant.app',
      cdnUrl: 'https://cdn.cultivaremergant.app',
      firebaseProjectId: 'cultivaremergant-prod',
      enableRemoteConfig: true,
      featureFlags: {
        'advanced_sensors': true,
        'ai_insights': true,
        'social_features': true,
        'premium_features': true,
      },
    ),
  };

  /// Get environment configuration based on build mode
  static EnvironmentData get current {
    // Determine environment from build mode
    BuildEnvironment environment;

    // Check for custom environment override
    const customEnv = String.fromEnvironment('ENVIRONMENT');
    if (customEnv.isNotEmpty) {
      environment = BuildEnvironment.values.firstWhere(
        (e) => e.toString() == customEnv,
        orElse: () => BuildEnvironment.development,
      );
    } else {
      // Use build mode
      const buildMode = String.fromEnvironment('BUILD_MODE');
      if (buildMode.contains('prod')) {
        environment = BuildEnvironment.production;
      } else if (buildMode.contains('staging')) {
        environment = BuildEnvironment.staging;
      } else {
        environment = BuildEnvironment.development;
      }
    }

    return _configs[environment]!;
  }

  /// Check if current environment is production
  static bool get isProduction =>
      current.environment == BuildEnvironment.production;

  /// Check if current environment is development
  static bool get isDevelopment =>
      current.environment == BuildEnvironment.development;

  /// Check if current environment is staging
  static bool get isStaging => current.environment == BuildEnvironment.staging;

  /// Get environment name
  static String get environmentName => current.environment.name;

  /// API endpoints
  static String get apiBaseUrl => current.apiBaseUrl;
  static String get wsUrl => current.wsUrl;
  static String get baseImageUrl => current.baseImageUrl;
  static String get cdnUrl => current.cdnUrl;

  /// Feature flags
  static Map<String, bool> get featureFlags => current.featureFlags;
  static bool get featureAdvancedSensors =>
      current.featureFlags['advanced_sensors'] ?? false;
  static bool get featureAiInsights =>
      current.featureFlags['ai_insights'] ?? false;
  static bool get featureSocialFeatures =>
      current.featureFlags['social_features'] ?? false;
  static bool get featurePremiumFeatures =>
      current.featureFlags['premium_features'] ?? false;

  /// Analytics and monitoring
  static bool get analyticsEnabled => current.analyticsEnabled;
  static bool get crashReportingEnabled => current.crashReportingEnabled;
  static String get firebaseProjectId => current.firebaseProjectId;

  /// Development flags
  static bool get debugModeEnabled => current.debugModeEnabled;
  static bool get enableLogging => current.enableLogging;
  static String get logLevel => current.logLevel;

  /// Configuration
  static int get networkTimeout => current.networkTimeout;
  static bool get enableRemoteConfig => current.enableRemoteConfig;
}

class EnvironmentData {
  const EnvironmentData({
    required this.environment,
    required this.apiBaseUrl,
    required this.wsUrl,
    required this.analyticsEnabled,
    required this.crashReportingEnabled,
    required this.debugModeEnabled,
    required this.networkTimeout,
    required this.enableLogging,
    required this.logLevel,
    required this.baseImageUrl,
    required this.cdnUrl,
    required this.firebaseProjectId,
    required this.enableRemoteConfig,
    required this.featureFlags,
  });

  final BuildEnvironment environment;
  final String apiBaseUrl;
  final String wsUrl;
  final bool analyticsEnabled;
  final bool crashReportingEnabled;
  final bool debugModeEnabled;
  final int networkTimeout;
  final bool enableLogging;
  final String logLevel;
  final String baseImageUrl;
  final String cdnUrl;
  final String firebaseProjectId;
  final bool enableRemoteConfig;
  final Map<String, bool> featureFlags;

  /// Convert to JSON for serialization
  Map<String, dynamic> toJson() {
    return {
      'environment': environment.name,
      'apiBaseUrl': apiBaseUrl,
      'wsUrl': wsUrl,
      'analyticsEnabled': analyticsEnabled,
      'crashReportingEnabled': crashReportingEnabled,
      'debugModeEnabled': debugModeEnabled,
      'networkTimeout': networkTimeout,
      'enableLogging': enableLogging,
      'logLevel': logLevel,
      'baseImageUrl': baseImageUrl,
      'cdnUrl': cdnUrl,
      'firebaseProjectId': firebaseProjectId,
      'enableRemoteConfig': enableRemoteConfig,
      'featureFlags': featureFlags,
    };
  }

  @override
  String toString() {
    return 'EnvironmentData(environment: ${environment.name}, debugMode: $debugModeEnabled, analytics: $analyticsEnabled)';
  }
}

// Build mode constants for compile-time environment detection
class BuildModes {
  static const bool isProduction = bool.fromEnvironment('PRODUCTION_MODE');
  static const bool isStaging = bool.fromEnvironment('STAGING_MODE');
  static const bool isDevelopment = !isProduction && !isStaging;

  // API endpoints based on build mode
  static String get apiBaseUrl {
    if (isProduction) return 'https://api.cultivaremergant.app';
    if (isStaging) return 'https://staging-api.cultivaremergant.app';
    return 'https://dev-api.cultivaremergant.app';
  }

  // Feature flags based on build mode
  static Map<String, bool> get featureFlags {
    if (isProduction) {
      return {
        'advanced_sensors': true,
        'ai_insights': true,
        'social_features': true,
        'premium_features': true,
      };
    }

    if (isStaging) {
      return {
        'advanced_sensors': true,
        'ai_insights': true,
        'social_features': true,
        'premium_features': false,
      };
    }

    return {
      'advanced_sensors': true,
      'ai_insights': false,
      'social_features': false,
      'premium_features': false,
    };
  }
}
