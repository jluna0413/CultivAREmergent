import 'package:flutter/material.dart';

import 'app_colors.dart';

class AppTextStyles {
  AppTextStyles._();

  static const String _fontFamily = 'Inter';

  // Static getters for common text styles
  static TextStyle get headlineSmall => _headlineSmall;
  static TextStyle get titleLarge => _titleLarge;
  static TextStyle get titleMedium => _titleMedium;
  static TextStyle get bodyLarge => _bodyLarge;
  static TextStyle get bodyMedium => _bodyMedium;
  static TextStyle get bodySmall => _bodySmall;
  static TextStyle get labelLarge => _labelLarge;
  static TextStyle get labelSmall => _labelSmall;

  static const TextStyle fixedH1 = TextStyle(
    fontFamily: _fontFamily,
    fontSize: 52,
    fontWeight: FontWeight.w700,
    height: 1.1,
    letterSpacing: -0.5,
  );

  static const TextStyle _headlineSmall = TextStyle(
    fontFamily: _fontFamily,
    fontSize: 24,
    fontWeight: FontWeight.w600,
    height: 1.2,
    letterSpacing: -0.2,
  );

  static const TextStyle _titleLarge = TextStyle(
    fontFamily: _fontFamily,
    fontSize: 20,
    fontWeight: FontWeight.w600,
    height: 1.3,
    letterSpacing: -0.1,
  );

  static const TextStyle _titleMedium = TextStyle(
    fontFamily: _fontFamily,
    fontSize: 18,
    fontWeight: FontWeight.w500,
    height: 1.3,
  );

  static const TextStyle _bodyLarge = TextStyle(
    fontFamily: _fontFamily,
    fontSize: 16,
    fontWeight: FontWeight.w500,
    height: 1.5,
  );

  static const TextStyle _bodyMedium = TextStyle(
    fontFamily: _fontFamily,
    fontSize: 14,
    height: 1.5,
  );

  static const TextStyle _bodySmall = TextStyle(
    fontFamily: _fontFamily,
    fontSize: 12,
    height: 1.4,
  );

  static const TextStyle _labelLarge = TextStyle(
    fontFamily: _fontFamily,
    fontSize: 14,
    fontWeight: FontWeight.w600,
    letterSpacing: 0.1,
  );

  static const TextStyle _labelSmall = TextStyle(
    fontFamily: _fontFamily,
    fontSize: 11,
    fontWeight: FontWeight.w600,
    letterSpacing: 0.25,
  );

  static TextTheme build({
    required Color primaryColor,
    required Color secondaryColor,
    required Color tertiaryColor,
  }) {
    return TextTheme(
      displayLarge: fixedH1.copyWith(color: primaryColor),
      headlineSmall: _headlineSmall.copyWith(color: primaryColor),
      titleLarge: _titleLarge.copyWith(color: primaryColor),
      titleMedium: _titleMedium.copyWith(color: primaryColor),
      bodyLarge: _bodyLarge.copyWith(color: primaryColor),
      bodyMedium: _bodyMedium.copyWith(color: secondaryColor),
      bodySmall: _bodySmall.copyWith(color: tertiaryColor),
      labelLarge: _labelLarge.copyWith(color: primaryColor),
      labelSmall: _labelSmall.copyWith(color: secondaryColor),
    );
  }

  static final TextTheme lightTextTheme = build(
    primaryColor: AppColors.textPrimaryLight,
    secondaryColor: AppColors.textSecondaryLight,
    tertiaryColor: AppColors.textTertiaryLight,
  );

  static final TextTheme darkTextTheme = build(
    primaryColor: AppColors.textPrimaryDark,
    secondaryColor: AppColors.textSecondaryDark,
    tertiaryColor: AppColors.textTertiaryDark,
  );
}
