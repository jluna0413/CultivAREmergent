/// Theme Provider - Manages application theme and visual styling
/// Handles light/dark mode, custom themes, and visual preferences
library;
// (removed stray library directive)

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:state_notifier/state_notifier.dart';
import 'package:shared_preferences/shared_preferences.dart';

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
  factory ColorPalette.fromJson(Map<String, dynamic> json) {
    return ColorPalette(
      primary: Color(json['primary'] as int),
      secondary: Color(json['secondary'] as int),
      accent: Color(json['accent'] as int),
      background: Color(json['background'] as int),
      surface: Color(json['surface'] as int),
      error: Color(json['error'] as int),
      warning: Color(json['warning'] as int),
      success: Color(json['success'] as int),
      info: Color(json['info'] as int),
      onPrimary: json['on_primary'] != null
          ? Color(json['on_primary'] as int)
          : null,
      onSecondary: json['on_secondary'] != null
          ? Color(json['on_secondary'] as int)
          : null,
      onSurface: json['on_surface'] != null
          ? Color(json['on_surface'] as int)
          : null,
      onBackground: json['on_background'] != null
          ? Color(json['on_background'] as int)
          : null,
      onError: json['on_error'] != null ? Color(json['on_error'] as int) : null,
    );
  }
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

  Map<String, dynamic> toJson() {
    return {
      'primary': primary.toARGB32(),
      'secondary': secondary.toARGB32(),
      'accent': accent.toARGB32(),
      'background': background.toARGB32(),
      'surface': surface.toARGB32(),
      'error': error.toARGB32(),
      'warning': warning.toARGB32(),
      'success': success.toARGB32(),
      'info': info.toARGB32(),
      'on_primary': onPrimary?.toARGB32(),
      'on_secondary': onSecondary?.toARGB32(),
      'on_surface': onSurface?.toARGB32(),
      'on_background': onBackground?.toARGB32(),
      'on_error': onError?.toARGB32(),
    };
  }
}

/// Theme configuration
class ThemeConfig {
  factory ThemeConfig.fromJson(Map<String, dynamic> json) {
    return ThemeConfig(
      mode: ThemeMode.values.firstWhere(
        (e) => e.name == json['mode'],
        orElse: () => ThemeMode.system,
      ),
      colorScheme: ColorSchemeType.values.firstWhere(
        (e) => e.name == json['colorScheme'],
        orElse: () => ColorSchemeType.defaultScheme,
      ),
      fontFamily: json['fontFamily'] as String? ?? 'Roboto',
      borderRadius: (json['borderRadius'] as num).toDouble(),
      elevation: (json['elevation'] as num).toDouble(),
      animationDuration: Duration(
        milliseconds: json['animationDuration'] as int? ?? 200,
      ),
    );
  }
  const ThemeConfig({
    required this.mode,
    required this.colorScheme,
    required this.fontFamily,
    required this.borderRadius,
    required this.elevation,
    required this.animationDuration,
  });

  final ThemeMode mode;
  final ColorSchemeType colorScheme;
  final String fontFamily;
  final double borderRadius;
  final double elevation;
  final Duration animationDuration;

  ThemeConfig copyWith({
    ThemeMode? mode,
    ColorSchemeType? colorScheme,
    String? fontFamily,
    double? borderRadius,
    double? elevation,
    Duration? animationDuration,
  }) {
    return ThemeConfig(
      mode: mode ?? this.mode,
      colorScheme: colorScheme ?? this.colorScheme,
      fontFamily: fontFamily ?? this.fontFamily,
      borderRadius: borderRadius ?? this.borderRadius,
      elevation: elevation ?? this.elevation,
      animationDuration: animationDuration ?? this.animationDuration,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'mode': mode.name,
      'colorScheme': colorScheme.name,
      'fontFamily': fontFamily,
      'borderRadius': borderRadius,
      'elevation': elevation,
      'animationDuration': animationDuration.inMilliseconds,
    };
  }
}

/// Theme state
class ThemeState {
  const ThemeState({
    required this.mode,
    required this.colorScheme,
    this.customColors,
    this.isLoading = false,
    this.error,
  });

  final ThemeMode mode;
  final ColorSchemeType colorScheme;
  final ColorPalette? customColors;
  final bool isLoading;
  final String? error;

  bool get isDarkMode => mode == ThemeMode.dark;
  bool get isSystemMode => mode == ThemeMode.system;
  bool get hasError => error != null;

  ThemeState copyWith({
    ThemeMode? mode,
    ColorSchemeType? colorScheme,
    ColorPalette? customColors,
    bool? isLoading,
    String? error,
  }) {
    return ThemeState(
      mode: mode ?? this.mode,
      colorScheme: colorScheme ?? this.colorScheme,
      customColors: customColors ?? this.customColors,
      isLoading: isLoading ?? this.isLoading,
      error: error ?? this.error,
    );
  }
}

/// Theme notifier
class ThemeNotifier extends StateNotifier<ThemeState> {
  ThemeNotifier()
    : super(
        const ThemeState(
          mode: ThemeMode.system,
          colorScheme: ColorSchemeType.defaultScheme,
        ),
      ) {
    _loadThemePreferences();
  }

  static const String _themeModeKey = 'theme_mode';
  static const String _colorSchemeKey = 'color_scheme';
  static const String _customColorsKey = 'custom_colors';
  static const String _fontFamilyKey = 'font_family';
  static const String _borderRadiusKey = 'border_radius';
  static const String _elevationKey = 'elevation';
  static const String _animationDurationKey = 'animation_duration';

  Future<void> _loadThemePreferences() async {
    try {
      state = state.copyWith(isLoading: true);

      final prefs = await SharedPreferences.getInstance();

      final modeString = prefs.getString(_themeModeKey);
      final schemeString = prefs.getString(_colorSchemeKey);
      final customColorsJson = prefs.getString(_customColorsKey);

      ThemeMode mode = ThemeMode.system;
      ColorSchemeType colorScheme = ColorSchemeType.defaultScheme;
      ColorPalette? customColors;

      if (modeString != null) {
        mode = ThemeMode.values.firstWhere(
          (e) => e.name == modeString,
          orElse: () => ThemeMode.system,
        );
      }

      if (schemeString != null) {
        colorScheme = ColorSchemeType.values.firstWhere(
          (e) => e.name == schemeString,
          orElse: () => ColorSchemeType.defaultScheme,
        );
      }

      if (customColorsJson != null) {
        // Parse custom colors from JSON
        try {
          final jsonMap = Map<String, dynamic>.from({
            'primary': int.parse(customColorsJson.split(',')[0]),
            'secondary': int.parse(customColorsJson.split(',')[1]),
            'accent': int.parse(customColorsJson.split(',')[2]),
            'background': int.parse(customColorsJson.split(',')[3]),
            'surface': int.parse(customColorsJson.split(',')[4]),
            'error': int.parse(customColorsJson.split(',')[5]),
            'warning': int.parse(customColorsJson.split(',')[6]),
            'success': int.parse(customColorsJson.split(',')[7]),
            'info': int.parse(customColorsJson.split(',')[8]),
          });
          customColors = ColorPalette.fromJson(jsonMap);
        } catch (e) {
          // Fall back to default if parsing fails
        }
      }

      state = ThemeState(
        mode: mode,
        colorScheme: colorScheme,
        customColors: customColors,
        isLoading: false,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: 'Failed to load theme preferences: $e',
      );
    }
  }

  Future<void> setThemeMode(ThemeMode mode) async {
    try {
      state = state.copyWith(mode: mode, isLoading: true, error: null);

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(_themeModeKey, mode.name);

      state = state.copyWith(mode: mode, isLoading: false);
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: 'Failed to save theme mode: $e',
      );
    }
  }

  Future<void> setColorScheme(ColorSchemeType colorScheme) async {
    try {
      state = state.copyWith(
        colorScheme: colorScheme,
        customColors: null,
        isLoading: true,
        error: null,
      );

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(_colorSchemeKey, colorScheme.name);
      await prefs.remove(
        _customColorsKey,
      ); // Clear custom colors when switching schemes

      state = state.copyWith(colorScheme: colorScheme, isLoading: false);
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: 'Failed to save color scheme: $e',
      );
    }
  }

  Future<void> setCustomColors(ColorPalette colors) async {
    try {
      state = state.copyWith(
        customColors: colors,
        isLoading: true,
        error: null,
      );

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(_customColorsKey, _serializeColors(colors));

      state = state.copyWith(customColors: colors, isLoading: false);
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: 'Failed to save custom colors: $e',
      );
    }
  }

  Future<void> toggleThemeMode() async {
    if (state.mode == ThemeMode.light) {
      await setThemeMode(ThemeMode.dark);
    } else if (state.mode == ThemeMode.dark) {
      await setThemeMode(ThemeMode.system);
    } else {
      await setThemeMode(ThemeMode.light);
    }
  }

  void clearError() {
    if (state.hasError) {
      state = state.copyWith(error: null);
    }
  }

  String _serializeColors(ColorPalette colors) {
    return '${colors.primary.toARGB32()},${colors.secondary.toARGB32()},${colors.accent.toARGB32()},${colors.background.toARGB32()},${colors.surface.toARGB32()},${colors.error.toARGB32()},${colors.warning.toARGB32()},${colors.success.toARGB32()},${colors.info.toARGB32()}';
  }

  ColorScheme getColorScheme(BuildContext context) {
    switch (state.colorScheme) {
      case ColorSchemeType.nature:
        return _getNatureScheme(context);
      case ColorSchemeType.ocean:
        return _getOceanScheme(context);
      case ColorSchemeType.sunset:
        return _getSunsetScheme(context);
      case ColorSchemeType.forest:
        return _getForestScheme(context);
      case ColorSchemeType.purple:
        return _getPurpleScheme(context);
      case ColorSchemeType.custom:
        return _getCustomScheme(context);
      default:
        return Theme.of(context).colorScheme;
    }
  }

  ColorScheme _getNatureScheme(BuildContext context) {
    return ColorScheme.fromSeed(
      seedColor: Colors.green,
      brightness: Theme.of(context).brightness,
    );
  }

  ColorScheme _getOceanScheme(BuildContext context) {
    return ColorScheme.fromSeed(
      seedColor: Colors.blue,
      brightness: Theme.of(context).brightness,
    );
  }

  ColorScheme _getSunsetScheme(BuildContext context) {
    return ColorScheme.fromSeed(
      seedColor: Colors.orange,
      brightness: Theme.of(context).brightness,
    );
  }

  ColorScheme _getForestScheme(BuildContext context) {
    return ColorScheme.fromSeed(
      seedColor: Colors.green[700]!,
      brightness: Theme.of(context).brightness,
    );
  }

  ColorScheme _getPurpleScheme(BuildContext context) {
    return ColorScheme.fromSeed(
      seedColor: Colors.purple,
      brightness: Theme.of(context).brightness,
    );
  }

  ColorScheme _getCustomScheme(BuildContext context) {
    if (state.customColors != null) {
      final colors = state.customColors!;
      return ColorScheme(
        primary: colors.primary,
        secondary: colors.secondary,
        surface: colors.surface,
        error: colors.error,
        onPrimary:
            colors.onPrimary ??
            (Theme.of(context).brightness == Brightness.light
                ? Colors.white
                : Colors.black),
        onSecondary:
            colors.onSecondary ??
            (Theme.of(context).brightness == Brightness.light
                ? Colors.white
                : Colors.black),
        onSurface:
            colors.onSurface ??
            (Theme.of(context).brightness == Brightness.light
                ? Colors.black
                : Colors.white),
        onError:
            colors.onError ??
            (Theme.of(context).brightness == Brightness.light
                ? Colors.white
                : Colors.black),
        brightness: Theme.of(context).brightness,
      );
    }
    return Theme.of(context).colorScheme;
  }
}

/// Providers
final themeProvider = StateNotifierProvider<ThemeNotifier, ThemeState>((ref) {
  return ThemeNotifier();
});

final themeModeProvider = Provider<ThemeMode>((ref) {
  final themeState = ref.watch(themeProvider);
  return themeState.mode;
});

final isDarkModeProvider = Provider<bool>((ref) {
  final themeState = ref.watch(themeProvider);
  return themeState.isDarkMode;
});

final colorSchemeProvider = Provider<ColorSchemeType>((ref) {
  final themeState = ref.watch(themeProvider);
  return themeState.colorScheme;
});

final themeLoadingProvider = Provider<bool>((ref) {
  final themeState = ref.watch(themeProvider);
  return themeState.isLoading;
});

final themeErrorProvider = Provider<String?>((ref) {
  final themeState = ref.watch(themeProvider);
  return themeState.error;
});

final customColorsProvider = Provider<ColorPalette?>((ref) {
  final themeState = ref.watch(themeProvider);
  return themeState.customColors;
});
