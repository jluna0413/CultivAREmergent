import 'package:flutter/material.dart';
import 'app_colors.dart';
import 'app_text_styles.dart';

final ColorScheme lightColorScheme = ColorScheme.fromSeed(
  seedColor: AppColorsLight.primary,
  brightness: Brightness.light,
  primary: AppColorsLight.primary,
  onPrimary: AppColorsLight.onPrimary,
  secondary: AppColorsLight.secondary,
  onSecondary: AppColorsLight.onSecondary,
  surface: AppColorsLight.surface,
  onSurface: AppColorsLight.onSurface,
  error: AppColors.danger,
  onError: AppColorsLight.onPrimary,
);

final ColorScheme darkColorScheme = ColorScheme.fromSeed(
  seedColor: AppColorsDark.primary,
  brightness: Brightness.dark,
  primary: AppColorsDark.primary,
  onPrimary: AppColorsDark.onPrimary,
  secondary: AppColorsDark.secondary,
  onSecondary: AppColorsDark.onSecondary,
  surface: AppColorsDark.surface,
  onSurface: AppColorsDark.onSurface,
  error: AppColors.danger,
  onError: AppColorsDark.onPrimary,
);

/// Centralized ThemeData for CultivAR Flutter app.
/// Exports `lightTheme` and `darkTheme` for app initialization.
final ThemeData lightTheme = ThemeData(
  useMaterial3: true,
  colorScheme: lightColorScheme,
  scaffoldBackgroundColor: lightColorScheme.surface,
  appBarTheme: AppBarTheme(
    backgroundColor: Colors.transparent,
    surfaceTintColor: Colors.transparent,
    elevation: 0,
    centerTitle: true,
    foregroundColor: lightColorScheme.onSurface,
    titleTextStyle: AppTextStyles.lightTextTheme.titleLarge?.copyWith(
      fontWeight: FontWeight.w700,
    ),
  ),
  cardTheme: CardThemeData(
    color: lightColorScheme.surface,
    surfaceTintColor: Colors.transparent,
    elevation: 0,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(16),
      side: const BorderSide(color: AppColorsLight.border),
    ),
    margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 12),
  ),
  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      backgroundColor: lightColorScheme.primary,
      foregroundColor: lightColorScheme.onPrimary,
      padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 20),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      textStyle: const TextStyle(fontWeight: FontWeight.w600, fontSize: 16),
      elevation: 6,
      shadowColor: AppColorsLight.shadow,
    ),
  ),
  outlinedButtonTheme: OutlinedButtonThemeData(
    style: OutlinedButton.styleFrom(
      foregroundColor: lightColorScheme.primary,
      side: BorderSide(color: lightColorScheme.primary, width: 1.5),
      padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 18),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
    ),
  ),
  inputDecorationTheme: InputDecorationTheme(
    filled: true,
    fillColor: lightColorScheme.surface,
    contentPadding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
    border: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: const BorderSide(color: AppColorsLight.border, width: 1.5),
    ),
    focusedBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: BorderSide(color: lightColorScheme.primary, width: 2.0),
    ),
    errorBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: const BorderSide(color: AppColors.danger, width: 2.0),
    ),
    labelStyle: TextStyle(
      color: lightColorScheme.onSurface.withValues(alpha: 0.9),
    ),
    hintStyle: TextStyle(
      color: lightColorScheme.onSurface.withValues(alpha: 0.6),
    ),
  ),
  textTheme: AppTextStyles.lightTextTheme,
  iconTheme: IconThemeData(size: 20, color: lightColorScheme.onSurface),
  floatingActionButtonTheme: FloatingActionButtonThemeData(
    backgroundColor: lightColorScheme.primary,
    foregroundColor: lightColorScheme.onPrimary,
  ),
  visualDensity: VisualDensity.adaptivePlatformDensity,
);

/// AppTheme class providing centralized access to theme colors and properties
/// Used across the application for consistent theming
class AppTheme {
  // Colors - Primary
  static const Color primaryColor = Color(0xFF4CAF50);
  static const Color onPrimary = Color(0xFFFFFFFF);

  // Colors - Surface and Background
  static const Color surfaceColor = Color(0xFFFAFAFA);
  static const Color backgroundColor = Color(0xFFFFFFFF);

  // Colors - Borders
  static const Color borderColor = Color(0xFFE0E0E0);
  static const Color borderSecondary = Color(0xFFBDBDBD);

  // Colors - Text
  static const Color textPrimary = Color(0xFF212121);
  static const Color textSecondary = Color(0xFF757575);

  // Colors - Status
  static const Color success = Color(0xFF4CAF50);
  static const Color error = Color(0xFFF44336);
  static const Color warning = Color(0xFFFF9800);
  static const Color info = Color(0xFF2196F3);

  // Colors - Shadows
  static const Color shadow = Color(0x1A000000);

  // Getters for theme-dependent colors
  static Color getPrimaryColor(BuildContext context) {
    return Theme.of(context).colorScheme.primary;
  }

  static Color getSurfaceColor(BuildContext context) {
    return Theme.of(context).colorScheme.surface;
  }

  static Color getBackgroundColor(BuildContext context) {
    return Theme.of(context).colorScheme.surface;
  }

  static Color getTextSecondary(BuildContext context) {
    return Theme.of(context).colorScheme.onSurface.withValues(alpha: 0.7);
  }

  static Color getBorderColor(BuildContext context) {
    return Theme.of(context).colorScheme.outline.withValues(alpha: 0.3);
  }

  // Light theme defaults for compilation
  static Color get lightPrimaryColor => const Color(0xFF4CAF50);
  static Color get lightSurfaceColor => const Color(0xFFFAFAFA);
  static Color get lightBackgroundColor => const Color(0xFFFFFFFF);
  static Color get lightTextSecondary => const Color(0xFF757575);
  static Color get lightBorderColor => const Color(0xFFE0E0E0);
  static Color get lightBorderSecondary => const Color(0xFFBDBDBD);

  // Dark theme defaults for compilation
  static Color get darkPrimaryColor => const Color(0xFF66BB6A);
  static Color get darkSurfaceColor => const Color(0xFF121212);
  static Color get darkBackgroundColor => const Color(0xFF1E1E1E);
  static Color get darkTextSecondary => const Color(0xFFB0B0B0);
  static Color get darkBorderColor => const Color(0xFF333333);
  static Color get darkBorderSecondary => const Color(0xFF424242);

  // Material Design shadows
  static const List<BoxShadow> shadows = [
    BoxShadow(color: Color(0x1A000000), blurRadius: 2, offset: Offset(0, 1)),
    BoxShadow(color: Color(0x0A000000), blurRadius: 1, offset: Offset(0, 1)),
  ];
}

/// AppShadows class for consistent shadow definitions
class AppShadows {
  // Individual shadow definitions (lists for spreading)
  static const List<BoxShadow> small = [
    BoxShadow(color: Color(0x1A000000), blurRadius: 2, offset: Offset(0, 1)),
  ];

  static const List<BoxShadow> medium = [
    BoxShadow(color: Color(0x26000000), blurRadius: 4, offset: Offset(0, 2)),
  ];

  static const List<BoxShadow> large = [
    BoxShadow(color: Color(0x33000000), blurRadius: 8, offset: Offset(0, 4)),
  ];

  // Individual shadow objects for direct use (non-const to avoid expression issues)
  static final BoxShadow shadowSm = BoxShadow(
    color: const Color(0x1A000000),
    blurRadius: 2,
    offset: const Offset(0, 1),
  );

  static final BoxShadow shadowMd = BoxShadow(
    color: const Color(0x26000000),
    blurRadius: 4,
    offset: const Offset(0, 2),
  );

  static final BoxShadow shadowLg = BoxShadow(
    color: const Color(0x33000000),
    blurRadius: 8,
    offset: const Offset(0, 4),
  );
}

final ThemeData darkTheme = ThemeData(
  useMaterial3: true,
  colorScheme: darkColorScheme,
  scaffoldBackgroundColor: darkColorScheme.surface,
  appBarTheme: AppBarTheme(
    backgroundColor: Colors.transparent,
    surfaceTintColor: Colors.transparent,
    elevation: 0,
    centerTitle: true,
    foregroundColor: darkColorScheme.onSurface,
    titleTextStyle: AppTextStyles.darkTextTheme.titleLarge?.copyWith(
      fontWeight: FontWeight.w700,
    ),
  ),
  cardTheme: CardThemeData(
    color: darkColorScheme.surface,
    surfaceTintColor: Colors.transparent,
    elevation: 0,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(16),
      side: const BorderSide(color: AppColorsDark.border),
    ),
    margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 12),
  ),
  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      backgroundColor: darkColorScheme.primary,
      foregroundColor: darkColorScheme.onPrimary,
      padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 20),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      textStyle: const TextStyle(fontWeight: FontWeight.w600, fontSize: 16),
      elevation: 6,
      shadowColor: AppColorsDark.shadow,
    ),
  ),
  outlinedButtonTheme: OutlinedButtonThemeData(
    style: OutlinedButton.styleFrom(
      foregroundColor: darkColorScheme.primary,
      side: BorderSide(color: darkColorScheme.primary, width: 1.5),
      padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 18),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
    ),
  ),
  inputDecorationTheme: InputDecorationTheme(
    filled: true,
    fillColor: darkColorScheme.surface,
    contentPadding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
    border: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: const BorderSide(color: AppColorsDark.border, width: 1.5),
    ),
    focusedBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: BorderSide(color: darkColorScheme.primary, width: 2.0),
    ),
    errorBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: const BorderSide(color: AppColors.danger, width: 2.0),
    ),
    labelStyle: TextStyle(
      color: darkColorScheme.onSurface.withValues(alpha: 0.9),
    ),
    hintStyle: TextStyle(
      color: darkColorScheme.onSurface.withValues(alpha: 0.6),
    ),
  ),
  textTheme: AppTextStyles.darkTextTheme,
  iconTheme: IconThemeData(size: 20, color: darkColorScheme.onSurface),
  floatingActionButtonTheme: FloatingActionButtonThemeData(
    backgroundColor: darkColorScheme.primary,
    foregroundColor: darkColorScheme.onPrimary,
  ),
  visualDensity: VisualDensity.adaptivePlatformDensity,
);
