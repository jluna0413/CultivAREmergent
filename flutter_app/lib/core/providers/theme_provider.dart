/// Theme Provider - Manages application theme and visual styling
/// Handles light/dark mode, custom themes, and visual preferences
library;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Theme mode enum
enum ThemeMode { light, dark, system }

/// Color scheme types
enum ColorSchemeType {
  defaultScheme,
  nature,
  ocean,
  sunset,
  forest,
  purple,
  custom,
}

/// Custom color palette
class ColorPalette {
  const ColorPalette({
    required this.primary,
    required this.secondary,
    required this.accent,
    required this.background,
    required this.surface,
    required this.error,
    required this.warning,
    required this.success,
    required this.info,
    this.onPrimary,
    this.onSecondary,
    this.onSurface,
    this.onBackground,
    this.onError,
  });

  final Color primary;
  final Color secondary;
  final Color accent;
  final Color background;
  final Color surface;
  final Color error;
  final Color warning;
  final Color success;
  final Color info;
  final Color? onPrimary;
  final Color? onSecondary;
  final Color? onSurface;
  final Color? onBackground;
  final Color? onError;
}

/// Theme configuration
class ThemeConfig {
  const ThemeConfig({
    required this.mode,
    required this.colorScheme,
    required this.fontFamily,
    required this.borderRadius,
    required this.elevation,
    required this.animationDuration,
    required this.customColors,
  });

  final ThemeMode mode;
  final ColorSchemeType colorScheme;
  final String fontFamily;
  final double borderRadius;
  final double elevation;
  final Duration animationDuration;
  final ColorPalette? customColors;

  ThemeConfig copyWith({
    ThemeMode? mode,
    ColorSchemeType? colorScheme,
    String? fontFamily,
    double? borderRadius,
    double? elevation,
    Duration? animationDuration,
    ColorPalette? customColors,
  }) {
    return ThemeConfig(
      mode: mode ?? this.mode,
      colorScheme: colorScheme ?? this.colorScheme,
      fontFamily: fontFamily ?? this.fontFamily,
      borderRadius: borderRadius ?? this.borderRadius,
      elevation: elevation ?? this.elevation,
      animationDuration: animationDuration ?? this.animationDuration,
      customColors: customColors ?? this.customColors,
    );
  }
}

/// Theme provider state
class ThemeProviderState {
  const ThemeProviderState({
    required this.config,
    this.isLoading,
    this.error,
    this.lastUpdated,
  });

  final ThemeConfig config;
  final bool? isLoading;
  final String? error;
  final DateTime? lastUpdated;

  bool get hasError => error != null;
  bool get isDark => _isDarkMode(config.mode);
  Brightness get brightness => isDark ? Brightness.dark : Brightness.light;

  static bool _isDarkMode(ThemeMode mode) {
    switch (mode) {
      case ThemeMode.light:
        return false;
      case ThemeMode.dark:
        return true;
      case ThemeMode.system:
        return WidgetsBinding.instance.platformDispatcher.platformBrightness ==
            Brightness.dark;
    }
  }

  ThemeProviderState copyWith({
    ThemeConfig? config,
    bool? isLoading,
    String? error,
    DateTime? lastUpdated,
  }) {
    return ThemeProviderState(
      config: config ?? this.config,
      isLoading: isLoading ?? this.isLoading,
      error: error ?? this.error,
      lastUpdated: lastUpdated ?? this.lastUpdated,
    );
  }
}

/// Theme notifier class
class ThemeNotifier {
  ThemeNotifier();

  void setThemeMode(ThemeMode mode) {
    // Simplified method
  }

  void setColorScheme(ColorSchemeType colorScheme) {
    // Simplified method
  }

  void toggleThemeMode() {
    // Simplified method
  }
}

// Default theme configuration
const ThemeConfig defaultThemeConfig = ThemeConfig(
  mode: ThemeMode.system,
  colorScheme: ColorSchemeType.defaultScheme,
  fontFamily: 'Roboto',
  borderRadius: 8.0,
  elevation: 2.0,
  animationDuration: Duration(milliseconds: 200),
  customColors: null,
);

const ThemeProviderState defaultThemeState = ThemeProviderState(
  config: defaultThemeConfig,
);

// Simplified provider using Provider pattern (same as auth_provider.dart)
final themeProvider = Provider<ThemeProviderState>((ref) {
  return defaultThemeState;
});

// Convenience providers
final themeModeProvider = Provider<ThemeMode>((ref) {
  final themeState = ref.watch(themeProvider);
  return themeState.config.mode;
});

final themeIsDarkProvider = Provider<bool>((ref) {
  final themeState = ref.watch(themeProvider);
  return themeState.isDark;
});

final themeBrightnessProvider = Provider<Brightness>((ref) {
  final themeState = ref.watch(themeProvider);
  return themeState.brightness;
});

final currentColorSchemeProvider = Provider<ColorScheme>((ref) {
  final themeState = ref.watch(themeProvider);
  final config = themeState.config;
  final isDark = themeState.isDark;

  switch (config.colorScheme) {
    case ColorSchemeType.defaultScheme:
      return isDark
          ? ThemeData.dark().colorScheme
          : ThemeData.light().colorScheme;
    case ColorSchemeType.nature:
      return isDark
          ? const ColorScheme.dark(
              primary: Color(0xFF4CAF50),
              secondary: Color(0xFF8BC34A),
              surface: Color(0xFF1B5E20),
            )
          : const ColorScheme.light(
              primary: Color(0xFF4CAF50),
              secondary: Color(0xFF8BC34A),
              surface: Color(0xFFFFFFFF),
            );
    case ColorSchemeType.ocean:
      return isDark
          ? const ColorScheme.dark(
              primary: Color(0xFF2196F3),
              secondary: Color(0xFF03DAC6),
              surface: Color(0xFF0D47A1),
            )
          : const ColorScheme.light(
              primary: Color(0xFF2196F3),
              secondary: Color(0xFF03DAC6),
              surface: Color(0xFFFFFFFF),
            );
    case ColorSchemeType.sunset:
      return isDark
          ? const ColorScheme.dark(
              primary: Color(0xFFFF9800),
              secondary: Color(0xFFFF5722),
              surface: Color(0xFFE65100),
            )
          : const ColorScheme.light(
              primary: Color(0xFFFF9800),
              secondary: Color(0xFFFF5722),
              surface: Color(0xFFFFFFFF),
            );
    case ColorSchemeType.forest:
      return isDark
          ? const ColorScheme.dark(
              primary: Color(0xFF388E3C),
              secondary: Color(0xFF689F38),
              surface: Color(0xFF2E7D32),
            )
          : const ColorScheme.light(
              primary: Color(0xFF388E3C),
              secondary: Color(0xFF689F38),
              surface: Color(0xFFFFFFFF),
            );
    case ColorSchemeType.purple:
      return isDark
          ? const ColorScheme.dark(
              primary: Color(0xFF9C27B0),
              secondary: Color(0xFF673AB7),
              surface: Color(0xFF4A148C),
            )
          : const ColorScheme.light(
              primary: Color(0xFF9C27B0),
              secondary: Color(0xFF673AB7),
              surface: Color(0xFFFFFFFF),
            );
    case ColorSchemeType.custom:
      // Return default custom color scheme
      return isDark
          ? const ColorScheme.dark(
              primary: Colors.blue,
              secondary: Colors.cyan,
              surface: Colors.black,
            )
          : const ColorScheme.light(
              primary: Colors.blue,
              secondary: Colors.cyan,
              surface: Colors.white,
            );
  }
});

final themeConfigProvider = Provider<ThemeConfig>((ref) {
  final themeState = ref.watch(themeProvider);
  return themeState.config;
});

final themeLoadingProvider = Provider<bool>((ref) {
  final themeState = ref.watch(themeProvider);
  return themeState.isLoading ?? false;
});

final themeErrorProvider = Provider<String?>((ref) {
  final themeState = ref.watch(themeProvider);
  return themeState.error;
});

final themeLastUpdatedProvider = Provider<DateTime?>((ref) {
  final themeState = ref.watch(themeProvider);
  return themeState.lastUpdated;
});

final isSystemThemeProvider = Provider<bool>((ref) {
  final themeState = ref.watch(themeProvider);
  return themeState.config.mode == ThemeMode.system;
});

final themeColorSchemeTypeProvider = Provider<ColorSchemeType>((ref) {
  final themeState = ref.watch(themeProvider);
  return themeState.config.colorScheme;
});

final customColorsProvider = Provider<ColorPalette?>((ref) {
  final themeState = ref.watch(themeProvider);
  return themeState.config.customColors;
});
