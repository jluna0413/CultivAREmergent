import 'package:json_annotation/json_annotation.dart';

/// App settings model for managing user preferences
class AppSettings {
  /// Creates AppSettings with default values
  const AppSettings({
    this.language = 'en',
    this.notifications = true,
    this.darkMode = true,
    this.theme = 1,
  });

  /// Creates AppSettings from JSON
  factory AppSettings.fromJson(Map<String, dynamic> json) {
    return AppSettings(
      language: json['language'] as String? ?? 'en',
      notifications: json['notifications'] as bool? ?? true,
      darkMode: json['dark_mode'] as bool? ?? true,
      theme: json['theme'] as int? ?? 1,
    );
  }

  /// Language preference (default: 'en')
  @JsonKey(name: 'language')
  final String language;

  /// Notification preferences (default: true)
  @JsonKey(name: 'notifications')
  final bool notifications;

  /// Dark mode preference (default: true)
  @JsonKey(name: 'dark_mode')
  final bool darkMode;

  /// Theme selection (default: 1)
  @JsonKey(name: 'theme')
  final int theme;

  /// Converts AppSettings to JSON
  Map<String, dynamic> toJson() {
    return {
      'language': language,
      'notifications': notifications,
      'dark_mode': darkMode,
      'theme': theme,
    };
  }

  /// Creates a copy with optional field overrides
  AppSettings copyWith({
    String? language,
    bool? notifications,
    bool? darkMode,
    int? theme,
  }) {
    return AppSettings(
      language: language ?? this.language,
      notifications: notifications ?? this.notifications,
      darkMode: darkMode ?? this.darkMode,
      theme: theme ?? this.theme,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is AppSettings &&
        other.language == language &&
        other.notifications == notifications &&
        other.darkMode == darkMode &&
        other.theme == theme;
  }

  @override
  int get hashCode {
    return Object.hash(language, notifications, darkMode, theme);
  }

  @override
  String toString() {
    return 'AppSettings(language: $language, notifications: $notifications, darkMode: $darkMode, theme: $theme)';
  }
}
