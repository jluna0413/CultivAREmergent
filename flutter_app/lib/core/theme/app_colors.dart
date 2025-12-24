import 'package:flutter/material.dart';

/// AppColors centralizes color tokens derived from the web design system
/// (app/web/static/css/styles.css). Use AppColorsLight / AppColorsDark for
/// theme-specific overrides.
class AppColors {
  // Primary green palette (50 - 900)
  static const Color primary50 = Color(0xFFF0FBF4);
  static const Color primary100 = Color(0xFFDFF7E8);
  static const Color primary200 = Color(0xFFBEF0D0);
  static const Color primary300 = Color(0xFF9FDDAD);
  static const Color primary400 = Color(0xFF74C784);
  static const Color primary500 = Color(0xFF4FB85F); // primary
  static const Color primary600 = Color(0xFF42A554);
  static const Color primary700 = Color(0xFF338B43);
  static const Color primary800 = Color(0xFF256831);
  static const Color primary900 = Color(0xFF14451F);

  // Accent / secondary palette (light green / lime)
  static const Color accent50 = Color(0xFFF8FFF4);
  static const Color accent100 = Color(0xFFEFFFDF);
  static const Color accent200 = Color(0xFFDFFFBF);
  static const Color accent300 = Color(0xFFCEFA8F);
  static const Color accent400 = Color(0xFFB8F64F);
  static const Color accent500 = Color(0xFFA0E12A); // accent
  static const Color accent600 = Color(0xFF8CCD24);
  static const Color accent700 = Color(0xFF69A91A);
  static const Color accent800 = Color(0xFF4A7A12);
  static const Color accent900 = Color(0xFF2B4C09);

  // Surface/background palettes
  static const Color surfaceLight = Color(0xFFFFFFFF);
  static const Color surfaceLighter = Color(0xFFF7F9FA);
  static const Color backgroundLight = Color(0xFFF3F6F7);

  static const Color surfaceDark = Color(0xFF0F1720);
  static const Color backgroundDark = Color(0xFF071020);

  // Text colors
  static const Color textPrimaryLight = Color(0xFF0B1B14);
  static const Color textSecondaryLight = Color(0xFF42524A);
  static const Color textTertiaryLight = Color(0xFF6B7A73);

  static const Color textPrimaryDark = Color(0xFFEFF6F1);
  static const Color textSecondaryDark = Color(0xFFBFD3C6);
  static const Color textTertiaryDark = Color(0xFF8FA79A);

  // Borders & outlines
  static const Color borderLight = Color(0xFFE6ECE6);
  static const Color borderDark = Color(0xFF16302A);

  // Status colors
  static const Color success = Color(0xFF22C55E);
  static const Color info = Color(0xFF3B82F6);
  static const Color warning = Color(0xFFF59E0B);
  static const Color danger = Color(0xFFEF4444);

  // Admin-specific colors matching Flask admin design
  static const Color adminPrimary = Color(0xFF4E73DF); // Primary admin blue
  static const Color adminSecondary = Color(0xFF6C757D);
  static const Color adminSuccess = Color(0xFF1CC88A);
  static const Color adminInfo = Color(0xFF36B9CC);
  static const Color adminWarning = Color(0xFFF6C23E);
  static const Color adminDanger = Color(0xFFE74A3B);
  static const Color adminLight = Color(0xFFF8F9FC);
  static const Color adminDark = Color(0xFF5A5C69);
  static const Color adminSidebar = Color(0xFF121212);
  static const Color adminCard = Color(0xFF2A2A2A);
  static const Color adminSurface = Color(0xFF1E1E1E);

  // Glass-specific tokens
  static const Color glassLight = Color.fromRGBO(255, 255, 255, 0.72);
  static const Color glassDark = Color.fromRGBO(6, 10, 12, 0.36);
  static const Color glassBorderLight = Color.fromRGBO(255, 255, 255, 0.18);
  static const Color glassBorderDark = Color.fromRGBO(255, 255, 255, 0.06);

  // Shadow colors (subtle)
  static const Color shadowLight = Color.fromRGBO(16, 24, 32, 0.06);
  static const Color shadowDark = Color.fromRGBO(0, 0, 0, 0.5);
}

/// Light theme overrides
class AppColorsLight extends AppColors {
  static const Color primary = AppColors.primary500;
  static const Color onPrimary = AppColors.surfaceLight;

  static const Color secondary = AppColors.accent500;
  static const Color onSecondary = AppColors.surfaceLight;

  static const Color surface = AppColors.surfaceLight;
  static const Color background = AppColors.backgroundLight;
  static const Color onSurface = AppColors.textPrimaryLight;
  static const Color onBackground = AppColors.textPrimaryLight;
  static const Color border = AppColors.borderLight;
  static const Color glass = AppColors.glassLight;
  static const Color glassBorder = AppColors.glassBorderLight;
  static const Color shadow = AppColors.shadowLight;
}

/// Dark theme overrides
class AppColorsDark extends AppColors {
  static const Color primary = AppColors.primary300;
  static const Color onPrimary = AppColors.surfaceDark;

  static const Color secondary = AppColors.accent300;
  static const Color onSecondary = AppColors.surfaceDark;

  static const Color surface = AppColors.surfaceDark;
  static const Color background = AppColors.backgroundDark;
  static const Color onSurface = AppColors.textPrimaryDark;
  static const Color onBackground = AppColors.textPrimaryDark;
  static const Color border = AppColors.borderDark;
  static const Color glass = AppColors.glassDark;
  static const Color glassBorder = AppColors.glassBorderDark;
  static const Color shadow = AppColors.shadowDark;
}
