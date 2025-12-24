/// Settings Provider - Manages application settings and preferences
/// Handles user preferences, app configuration, and data management
library;

import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Notification settings
class NotificationSettings {
  const NotificationSettings({
    required this.enabled,
    required this.plantAlerts,
    required this.harvestReminders,
    required this.sensorAlerts,
    required this.weeklyReports,
    required this.marketingEmails,
  });

  final bool enabled;
  final bool plantAlerts;
  final bool harvestReminders;
  final bool sensorAlerts;
  final bool weeklyReports;
  final bool marketingEmails;

  NotificationSettings copyWith({
    bool? enabled,
    bool? plantAlerts,
    bool? harvestReminders,
    bool? sensorAlerts,
    bool? weeklyReports,
    bool? marketingEmails,
  }) {
    return NotificationSettings(
      enabled: enabled ?? this.enabled,
      plantAlerts: plantAlerts ?? this.plantAlerts,
      harvestReminders: harvestReminders ?? this.harvestReminders,
      sensorAlerts: sensorAlerts ?? this.sensorAlerts,
      weeklyReports: weeklyReports ?? this.weeklyReports,
      marketingEmails: marketingEmails ?? this.marketingEmails,
    );
  }
}

/// Display settings
class DisplaySettings {
  const DisplaySettings({
    required this.theme,
    required this.language,
    required this.temperatureUnit,
    required this.timeFormat,
    required this.dateFormat,
    required this.compactMode,
    required this.autoRefresh,
  });

  final String theme; // 'light', 'dark', 'system'
  final String language; // ISO 639-1 language code
  final String temperatureUnit; // 'celsius', 'fahrenheit'
  final String timeFormat; // '12h', '24h'
  final String dateFormat; // 'MM/dd/yyyy', 'dd/MM/yyyy', etc.
  final bool compactMode;
  final bool autoRefresh;

  DisplaySettings copyWith({
    String? theme,
    String? language,
    String? temperatureUnit,
    String? timeFormat,
    String? dateFormat,
    bool? compactMode,
    bool? autoRefresh,
  }) {
    return DisplaySettings(
      theme: theme ?? this.theme,
      language: language ?? this.language,
      temperatureUnit: temperatureUnit ?? this.temperatureUnit,
      timeFormat: timeFormat ?? this.timeFormat,
      dateFormat: dateFormat ?? this.dateFormat,
      compactMode: compactMode ?? this.compactMode,
      autoRefresh: autoRefresh ?? this.autoRefresh,
    );
  }
}

/// Privacy settings
class PrivacySettings {
  const PrivacySettings({
    required this.analyticsEnabled,
    required this.crashReporting,
    required this.dataSharing,
    required this.locationServices,
    required this.biometricAuth,
    required this.autoBackup,
  });

  final bool analyticsEnabled;
  final bool crashReporting;
  final bool dataSharing;
  final bool locationServices;
  final bool biometricAuth;
  final bool autoBackup;

  PrivacySettings copyWith({
    bool? analyticsEnabled,
    bool? crashReporting,
    bool? dataSharing,
    bool? locationServices,
    bool? biometricAuth,
    bool? autoBackup,
  }) {
    return PrivacySettings(
      analyticsEnabled: analyticsEnabled ?? this.analyticsEnabled,
      crashReporting: crashReporting ?? this.crashReporting,
      dataSharing: dataSharing ?? this.dataSharing,
      locationServices: locationServices ?? this.locationServices,
      biometricAuth: biometricAuth ?? this.biometricAuth,
      autoBackup: autoBackup ?? this.autoBackup,
    );
  }
}

/// App settings
class AppSettings {
  const AppSettings({
    required this.version,
    required this.buildNumber,
    required this.firstLaunch,
    required this.tutorialCompleted,
    required this.notifications,
    required this.display,
    required this.privacy,
  });

  final String version;
  final String buildNumber;
  final bool firstLaunch;
  final bool tutorialCompleted;
  final NotificationSettings notifications;
  final DisplaySettings display;
  final PrivacySettings privacy;

  AppSettings copyWith({
    String? version,
    String? buildNumber,
    bool? firstLaunch,
    bool? tutorialCompleted,
    NotificationSettings? notifications,
    DisplaySettings? display,
    PrivacySettings? privacy,
  }) {
    return AppSettings(
      version: version ?? this.version,
      buildNumber: buildNumber ?? this.buildNumber,
      firstLaunch: firstLaunch ?? this.firstLaunch,
      tutorialCompleted: tutorialCompleted ?? this.tutorialCompleted,
      notifications: notifications ?? this.notifications,
      display: display ?? this.display,
      privacy: privacy ?? this.privacy,
    );
  }
}

// Settings state class
class SettingsProviderState {
  const SettingsProviderState({
    required this.settings,
    this.isLoading,
    this.error,
    this.lastUpdated,
  });

  final AppSettings settings;
  final bool? isLoading;
  final String? error;
  final DateTime? lastUpdated;

  bool get hasError => error != null;

  SettingsProviderState copyWith({
    AppSettings? settings,
    bool? isLoading,
    String? error,
    DateTime? lastUpdated,
  }) {
    return SettingsProviderState(
      settings: settings ?? this.settings,
      isLoading: isLoading ?? this.isLoading,
      error: error ?? this.error,
      lastUpdated: lastUpdated ?? this.lastUpdated,
    );
  }
}

// Default settings
const AppSettings defaultSettings = AppSettings(
  version: '1.0.0',
  buildNumber: '1',
  firstLaunch: true,
  tutorialCompleted: false,
  notifications: NotificationSettings(
    enabled: true,
    plantAlerts: true,
    harvestReminders: true,
    sensorAlerts: true,
    weeklyReports: false,
    marketingEmails: false,
  ),
  display: DisplaySettings(
    theme: 'system',
    language: 'en',
    temperatureUnit: 'celsius',
    timeFormat: '12h',
    dateFormat: 'MM/dd/yyyy',
    compactMode: false,
    autoRefresh: true,
  ),
  privacy: PrivacySettings(
    analyticsEnabled: true,
    crashReporting: true,
    dataSharing: false,
    locationServices: false,
    biometricAuth: false,
    autoBackup: true,
  ),
);

const SettingsProviderState defaultSettingsState = SettingsProviderState(
  settings: defaultSettings,
);

// Simplified provider using Provider pattern (same as auth_provider.dart)
final settingsProvider = Provider<SettingsProviderState>((ref) {
  return defaultSettingsState;
});

// Convenience providers using simplified pattern
final appSettingsProvider = Provider<AppSettings>((ref) {
  final settingsState = ref.watch(settingsProvider);
  return settingsState.settings;
});

final settingsLoadingProvider = Provider<bool>((ref) {
  final settingsState = ref.watch(settingsProvider);
  return settingsState.isLoading ?? false;
});

final settingsErrorProvider = Provider<String?>((ref) {
  final settingsState = ref.watch(settingsProvider);
  return settingsState.error;
});

final notificationSettingsProvider = Provider<NotificationSettings>((ref) {
  final settings = ref.watch(appSettingsProvider);
  return settings.notifications;
});

final displaySettingsProvider = Provider<DisplaySettings>((ref) {
  final settings = ref.watch(appSettingsProvider);
  return settings.display;
});

final privacySettingsProvider = Provider<PrivacySettings>((ref) {
  final settings = ref.watch(appSettingsProvider);
  return settings.privacy;
});

final isFirstLaunchProvider = Provider<bool>((ref) {
  final settings = ref.watch(appSettingsProvider);
  return settings.firstLaunch;
});

final tutorialCompletedProvider = Provider<bool>((ref) {
  final settings = ref.watch(appSettingsProvider);
  return settings.tutorialCompleted;
});

final currentThemeProvider = Provider<String>((ref) {
  final display = ref.watch(displaySettingsProvider);
  return display.theme;
});

final currentLanguageProvider = Provider<String>((ref) {
  final display = ref.watch(displaySettingsProvider);
  return display.language;
});

final temperatureUnitProvider = Provider<String>((ref) {
  final display = ref.watch(displaySettingsProvider);
  return display.temperatureUnit;
});

final notificationsEnabledProvider = Provider<bool>((ref) {
  final notifications = ref.watch(notificationSettingsProvider);
  return notifications.enabled;
});

final analyticsEnabledProvider = Provider<bool>((ref) {
  final privacy = ref.watch(privacySettingsProvider);
  return privacy.analyticsEnabled;
});
