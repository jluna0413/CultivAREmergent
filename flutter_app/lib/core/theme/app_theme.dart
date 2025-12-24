// AGENT_SIGNATURE: (Agent Type: IDE, Name: Kilo-Code, Action: Refactor-Theme)
import 'package:flutter/material.dart';
import 'dart:ui' as ui;
import 'app_colors.dart';
import 'app_text_styles.dart';

/// Centralized ThemeData for CultivAR Flutter app.
/// "Apple-Style" Minimalist Aesthetic:
/// - Generous whitespace/padding
/// - Subtle shadows (no hard elevation)
/// - Typography-first hierarchy
/// - Refined border radii (Apple uses super-ellipses, we use standard rounded)
final ThemeData lightTheme = ThemeData(
  useMaterial3: true,
  brightness: Brightness.light,
  colorScheme: ColorScheme.fromSeed(
    seedColor: AppColorsLight.primary,
    brightness: Brightness.light,
    surface: Colors.white, // Pure white for Apple feel
    onSurface: const Color(0xFF1D1D1F), // Apple's "Graphite" for text
    outline: const Color(0xFFD2D2D7), // Apple's light gray border
  ),
  scaffoldBackgroundColor: const Color(
    0xFFF5F5F7,
  ), // Apple's off-white background
  appBarTheme: const AppBarTheme(
    backgroundColor: Colors.transparent,
    surfaceTintColor: Colors.transparent,
    elevation: 0,
    centerTitle: true,
    foregroundColor: Color(0xFF1D1D1F),
    titleTextStyle: TextStyle(
      // SF Pro Display approximate
      fontFamily: 'Roboto',
      fontWeight: FontWeight.w600,
      fontSize: 17,
      color: Color(0xFF1D1D1F),
      letterSpacing: -0.4,
    ),
  ),
  cardTheme: CardThemeData(
    color: Colors.white,
    surfaceTintColor: Colors.transparent,
    elevation: 0, // We use custom shadows instead of elevation
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(18), // Slightly more rounded
      side: BorderSide.none, // Clean look
    ),
    margin: const EdgeInsets.symmetric(vertical: 10, horizontal: 16),
  ),
  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      backgroundColor: const Color(0xFF0071E3), // Apple Blue
      foregroundColor: Colors.white,
      padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 24),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(99),
      ), // Capsule
      textStyle: const TextStyle(fontWeight: FontWeight.w500, fontSize: 15),
      elevation: 0,
      shadowColor: Colors.transparent,
    ),
  ),
  inputDecorationTheme: InputDecorationTheme(
    filled: true,
    fillColor: Colors.white,
    contentPadding: const EdgeInsets.symmetric(vertical: 16, horizontal: 16),
    border: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: const BorderSide(color: Color(0xFFD2D2D7), width: 1.0),
    ),
    enabledBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: const BorderSide(color: Color(0xFFD2D2D7), width: 1.0),
    ),
    focusedBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: const BorderSide(color: Color(0xFF0071E3), width: 2.0),
    ),
    hintStyle: const TextStyle(color: Color(0xFF86868B)),
  ),
  iconTheme: const IconThemeData(size: 22, color: Color(0xFF1D1D1F)),
);

final ThemeData darkTheme = ThemeData(
  useMaterial3: true,
  brightness: Brightness.dark,
  colorScheme: ColorScheme.fromSeed(
    seedColor: AppColorsDark.primary,
    brightness: Brightness.dark,
    surface: const Color(0xFF1C1C1E), // Apple Dark Surface
    onSurface: const Color(0xFFF5F5F7),
    outline: const Color(0xFF38383A),
  ),
  scaffoldBackgroundColor: const Color(0xFF000000), // Pure Black for OLED
  appBarTheme: const AppBarTheme(
    backgroundColor: Colors.transparent,
    surfaceTintColor: Colors.transparent,
    elevation: 0,
    centerTitle: true,
    foregroundColor: Colors.white,
    titleTextStyle: TextStyle(
      fontFamily: 'Roboto',
      fontWeight: FontWeight.w600,
      fontSize: 17,
      color: Colors.white,
      letterSpacing: -0.4,
    ),
  ),
  cardTheme: CardThemeData(
    color: const Color(0xFF1C1C1E),
    surfaceTintColor: Colors.transparent,
    elevation: 0,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(18),
      side: BorderSide.none,
    ),
    margin: const EdgeInsets.symmetric(vertical: 10, horizontal: 16),
  ),
  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      backgroundColor: const Color(0xFF0071E3),
      foregroundColor: Colors.white,
      padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 24),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(99)),
      textStyle: const TextStyle(fontWeight: FontWeight.w500, fontSize: 15),
      elevation: 0,
      shadowColor: Colors.transparent,
    ),
  ),
  inputDecorationTheme: InputDecorationTheme(
    filled: true,
    fillColor: const Color(0xFF1C1C1E),
    contentPadding: const EdgeInsets.symmetric(vertical: 16, horizontal: 16),
    border: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: const BorderSide(color: Color(0xFF38383A), width: 1.0),
    ),
    enabledBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: const BorderSide(color: Color(0xFF38383A), width: 1.0),
    ),
    focusedBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: const BorderSide(color: Color(0xFF0071E3), width: 2.0),
    ),
    hintStyle: const TextStyle(color: Color(0xFF86868B)),
  ),
  iconTheme: const IconThemeData(size: 22, color: Colors.white),
);

/// AppShadows for that "Premium/Depth" feel without Heavy Material Elevation.
class AppShadows {
  // Soft, diffused shadow for cards (Apple style - Validated against apple.com)
  static final List<BoxShadow> card = [
    BoxShadow(
      color: Colors.black.withOpacity(0.04),
      blurRadius: 32, // Further diffused for "Apple" feel
      offset: const Offset(0, 8), // Slightly lower elevation
    ),
    BoxShadow(
      color: Colors.black.withOpacity(0.02),
      blurRadius: 8,
      offset: const Offset(0, 4),
    ),
  ];

  // Slightly stronger for floating elements
  static final List<BoxShadow> floating = [
    BoxShadow(
      color: Colors.black.withOpacity(0.12),
      blurRadius: 24,
      offset: const Offset(0, 8),
    ),
  ];

  // --- LEGACY COMPATIBILITY (Mapped to new style) ---
  static const List<BoxShadow> small = [
    BoxShadow(color: Color(0x0A000000), blurRadius: 4, offset: ui.Offset(0, 2)),
  ];
  static const List<BoxShadow> medium = [
    BoxShadow(
      color: Color(0x0F000000),
      blurRadius: 12,
      offset: ui.Offset(0, 6),
    ),
  ];
  static const List<BoxShadow> large = [
    BoxShadow(
      color: Color(0x1F000000),
      blurRadius: 24,
      offset: ui.Offset(0, 12),
    ),
  ];

  static final BoxShadow shadowSm = small[0];
  static final BoxShadow shadowMd = medium[0];
  static final BoxShadow shadowLg = large[0];
}

/// AppTheme class providing centralized access to theme colors and properties
/// Used across the application for consistent theming
class AppTheme {
  // --- LEGACY COMPATIBILITY (Mapped to new style) ---
  // Colors - Primary (Apple Green for continuity)
  static const Color primaryColor = Color(0xFF34C759);
  static const Color onPrimary = Colors.white;

  // Colors - Surface and Background
  static const Color surfaceColor = Colors.white;
  static const Color backgroundColor = Color(0xFFF5F5F7);

  // Colors - Borders
  static const Color borderColor = Color(0xFFD2D2D7);
  static const Color borderSecondary = Color(0xFFE5E5EA);

  // Colors - Text
  static const Color textPrimary = Color(0xFF1D1D1F);
  static const Color textSecondary = Color(0xFF86868B);

  // Colors - Status
  static const Color success = Color(0xFF34C759);
  static const Color error = Color(0xFFFF3B30);
  static const Color warning = Color(0xFFFF9500);
  static const Color info = Color(0xFF007AFF);

  // Colors - Shadows
  static const Color shadow = Color(0x0A000000);

  // Getters for theme-dependent colors
  static Color getPrimaryColor(BuildContext context) {
    return Theme.of(context).colorScheme.primary;
  }

  static Color getSurfaceColor(BuildContext context) {
    return Theme.of(context).colorScheme.surface;
  }

  static Color getBackgroundColor(BuildContext context) {
    return Theme.of(context).scaffoldBackgroundColor;
  }

  static Color getTextSecondary(BuildContext context) {
    return Theme.of(context).colorScheme.onSurface.withOpacity(0.6);
  }

  static Color getBorderColor(BuildContext context) {
    return Theme.of(context).colorScheme.outline;
  }

  // Light theme defaults for compilation
  static Color get lightPrimaryColor => const Color(0xFF34C759);
  static Color get lightSurfaceColor => Colors.white;
  static Color get lightBackgroundColor => const Color(0xFFF5F5F7);
  static Color get lightTextSecondary => const Color(0xFF86868B);
  static Color get lightBorderColor => const Color(0xFFD2D2D7);
  static Color get lightBorderSecondary => const Color(0xFFE5E5EA);

  // Dark theme defaults for compilation
  static Color get darkPrimaryColor => const Color(0xFF30D158);
  static Color get darkSurfaceColor => const Color(0xFF1C1C1E);
  static Color get darkBackgroundColor => Colors.black;
  static Color get darkTextSecondary => const Color(0xFFacaeb0);
  static Color get darkBorderColor => const Color(0xFF38383A);
  static Color get darkBorderSecondary => const Color(0xFF48484A);
}
