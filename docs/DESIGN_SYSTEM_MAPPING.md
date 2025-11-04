# Design System Mapping

## Overview

This document provides a comprehensive mapping between the legacy CSS design system and Flutter theme constants. The legacy system uses CSS custom properties (variables) extensively, with 840+ lines of design tokens covering colors, typography, spacing, shadows, and animations.

## CSS to Flutter Token Mapping

### Color System

#### Primary Color Palette
```css
/* Legacy CSS Custom Properties (from app/web/static/css/styles.css lines 13-45) */
--primary-50: #f0f9ff;
--primary-100: #e0f2fe;
--primary-200: #bae6fd;
--primary-300: #7dd3fc;
--primary-400: #38bdf8;
--primary-500: #0ea5e9;
--primary-600: #0284c7;
--primary-700: #0369a1;
--primary-800: #075985;
--primary-900: #0c4a6e;
```

```dart
// Flutter Theme Extension (ColorScheme extensions)
class AppColors extends ThemeExtension<AppColors> {
  static const primary50 = Color(0xFFF0F9FF);
  static const primary100 = Color(0xFFE0F2FE);
  static const primary200 = Color(0xFFBAE6FD);
  static const primary300 = Color(0xFF7DD3FC);
  static const primary400 = Color(0xFF38BDF8);
  static const primary500 = Color(0xFF0EA5E9);
  static const primary600 = Color(0xFF0284C7);
  static const primary700 = Color(0xFF0369A1);
  static const primary800 = Color(0xFF075985);
  static const primary900 = Color(0xFF0C4A6E);
  
  // Default primary color
  static const primary = primary600;
}
```

#### Surface Colors
```css
/* Legacy CSS (lines 46-60) */
--surface-primary: #ffffff;
--surface-secondary: #f8fafc;
--surface-tertiary: #f1f5f9;
--surface-glass-light: rgba(255, 255, 255, 0.1);
--surface-glass-dark: rgba(255, 255, 255, 0.05);
```

```dart
// Flutter Theme Surface Colors
class AppColors extends ThemeExtension<AppColors> {
  static const surfacePrimary = Color(0xFFFFFFFF);
  static const surfaceSecondary = Color(0xFFF8FAFC);
  static const surfaceTertiary = Color(0xFFF1F5F9);
  static const surfaceGlassLight = Color(0x1AFFFFFF);
  static const surfaceGlassDark = Color(0x0DFFFFFF);
}
```

#### Text Colors
```css
/* Legacy CSS (lines 61-75) */
--text-primary: #1e293b;
--text-secondary: #64748b;
--text-tertiary: #94a3b8;
--text-inverse: #ffffff;
```

```dart
// Flutter Text Colors
class AppColors extends ThemeExtension<AppColors> {
  static const textPrimary = Color(0xFF1E293B);
  static const textSecondary = Color(0xFF64748B);
  static const textTertiary = Color(0xFF94A3B8);
  static const textInverse = Color(0xFFFFFFFF);
}
```

#### Status Colors
```css
/* Legacy CSS (lines 76-95) */
--status-success: #10b981;
--status-warning: #f59e0b;
--status-error: #ef4444;
--status-info: #3b82f6;
--status-seedling: #22c55e;
--status-vegetative: #06b6d4;
--status-flowering: #8b5cf6;
--status-harvested: #f59e0b;
--status-dead: #ef4444;
```

```dart
// Flutter Status Colors
class AppColors extends ThemeExtension<AppColors> {
  static const statusSuccess = Color(0xFF10B981);
  static const statusWarning = Color(0xFFF59E0B);
  static const statusError = Color(0xFFEF4444);
  static const statusInfo = Color(0xFF3B82F6);
  
  // Plant status specific colors
  static const statusSeedling = Color(0xFF22C55E);
  static const statusVegetative = Color(0xFF06B6D4);
  static const statusFlowering = Color(0xFF8B5CF6);
  static const statusHarvested = Color(0xFFF59E0B);
  static const statusDead = Color(0xFFEF4444);
}
```

### Typography System

#### Font Families
```css
/* Legacy CSS (lines 96-110) */
--font-family-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--font-family-heading: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

```dart
// Flutter Typography
class AppTextStyles {
  static const String primaryFontFamily = 'Inter';
  
  static const TextTheme textTheme = TextTheme(
    displayLarge: TextStyle(
      fontFamily: primaryFontFamily,
      fontSize: 57,
      fontWeight: FontWeight.w400,
      letterSpacing: -0.25,
    ),
    // ... other text styles
  );
}
```

#### Font Weights
```css
/* Legacy CSS (lines 111-125) */
--font-weight-light: 300;
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

```dart
// Flutter Font Weights
class AppFontWeights {
  static const FontWeight light = FontWeight.w300;
  static const FontWeight normal = FontWeight.w400;
  static const FontWeight medium = FontWeight.w500;
  static const FontWeight semibold = FontWeight.w600;
  static const FontWeight bold = FontWeight.w700;
}
```

#### Font Sizes (Responsive Scale)
```css
/* Legacy CSS (lines 126-150) using clamp() for responsive scaling */
--font-size-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
--font-size-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
--font-size-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
--font-size-lg: clamp(1.125rem, 1rem + 0.625vw, 1.25rem);
--font-size-xl: clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem);
--font-size-2xl: clamp(1.5rem, 1.3rem + 1vw, 2rem);
```

```dart
// Flutter Responsive Font Sizes
class AppFontSizes {
  static double xs(double screenWidth) => 
      screenWidth < 768 ? 12.0 : 14.0;
  static double sm(double screenWidth) => 
      screenWidth < 768 ? 14.0 : 16.0;
  static double base(double screenWidth) => 
      screenWidth < 768 ? 16.0 : 18.0;
  static double lg(double screenWidth) => 
      screenWidth < 768 ? 18.0 : 20.0;
  static double xl(double screenWidth) => 
      screenWidth < 768 ? 20.0 : 24.0;
  static double _2xl(double screenWidth) => 
      screenWidth < 768 ? 24.0 : 32.0;
}
```

### Spacing System

#### Gap System
```css
/* Legacy CSS (lines 151-170) */
--gap-xs: 0.25rem;   /* 4px */
--gap-sm: 0.5rem;    /* 8px */
--gap-md: 1rem;      /* 16px */
--gap-lg: 1.5rem;    /* 24px */
--gap-xl: 2rem;      /* 32px */
--gap-2xl: 3rem;     /* 48px */
```

```dart
// Flutter Spacing
class AppSpacing {
  static const double xs = 4.0;
  static const double sm = 8.0;
  static const double md = 16.0;
  static const double lg = 24.0;
  static const double xl = 32.0;
  static const double _2xl = 48.0;
}
```

#### Padding & Margin
```css
/* Legacy CSS (lines 171-190) */
--padding-xs: 0.25rem;
--padding-sm: 0.5rem;
--padding-md: 1rem;
--padding-lg: 1.5rem;
--padding-xl: 2rem;
```

```dart
// Flutter Padding/Margin
class AppPadding {
  static const EdgeInsets xs = EdgeInsets.all(4.0);
  static const EdgeInsets sm = EdgeInsets.all(8.0);
  static const EdgeInsets md = EdgeInsets.all(16.0);
  static const EdgeInsets lg = EdgeInsets.all(24.0);
  static const EdgeInsets xl = EdgeInsets.all(32.0);
}
```

### Shadow System

#### Elevation Levels
```css
/* Legacy CSS (lines 191-220) */
--shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
--shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);
```

```dart
// Flutter Shadow System
class AppShadows {
  static final List<BoxShadow> xs = [
    BoxShadow(
      color: Colors.black.withOpacity(0.05),
      blurRadius: 2,
      offset: const Offset(0, 1),
      spreadRadius: 0,
    ),
  ];
  
  static final List<BoxShadow> sm = [
    BoxShadow(
      color: Colors.black.withOpacity(0.1),
      blurRadius: 3,
      offset: const Offset(0, 1),
      spreadRadius: -1,
    ),
    BoxShadow(
      color: Colors.black.withOpacity(0.1),
      blurRadius: 2,
      offset: const Offset(0, 1),
      spreadRadius: -2,
    ),
  ];
  
  static final List<BoxShadow> md = [
    BoxShadow(
      color: Colors.black.withOpacity(0.1),
      blurRadius: 6,
      offset: const Offset(0, 4),
      spreadRadius: -1,
    ),
    BoxShadow(
      color: Colors.black.withOpacity(0.1),
      blurRadius: 4,
      offset: const Offset(0, 2),
      spreadRadius: -2,
    ),
  ];
  
  static final List<BoxShadow> lg = [
    BoxShadow(
      color: Colors.black.withOpacity(0.1),
      blurRadius: 15,
      offset: const Offset(0, 10),
      spreadRadius: -3,
    ),
    BoxShadow(
      color: Colors.black.withOpacity(0.1),
      blurRadius: 6,
      offset: const Offset(0, 4),
      spreadRadius: -4,
    ),
  ];
  
  static final List<BoxShadow> xl = [
    BoxShadow(
      color: Colors.black.withOpacity(0.1),
      blurRadius: 25,
      offset: const Offset(0, 20),
      spreadRadius: -5,
    ),
    BoxShadow(
      color: Colors.black.withOpacity(0.1),
      blurRadius: 10,
      offset: const Offset(0, 8),
      spreadRadius: -6,
    ),
  ];
  
  static final List<BoxShadow> _2xl = [
    BoxShadow(
      color: Colors.black.withOpacity(0.25),
      blurRadius: 50,
      offset: const Offset(0, 25),
      spreadRadius: -12,
    ),
  ];
}
```

### Border Radius System

#### Radius Values
```css
/* Legacy CSS (lines 221-235) */
--radius-none: 0;
--radius-sm: 0.125rem;   /* 2px */
--radius-md: 0.375rem;   /* 6px */
--radius-lg: 0.5rem;     /* 8px */
--radius-xl: 0.75rem;    /* 12px */
--radius-2xl: 1rem;      /* 16px */
--radius-full: 9999px;
```

```dart
// Flutter Border Radius
class AppRadius {
  static const double none = 0.0;
  static const double sm = 2.0;
  static const double md = 6.0;
  static const double lg = 8.0;
  static const double xl = 12.0;
  static const double _2xl = 16.0;
  static const double full = 9999.0;
}
```

### Glass Morphism Effects

#### Glass Card Styling
```css
/* Legacy CSS (lines 370-410) */
.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
}
```

```dart
// Flutter Glass Morphism
class AppDecorations {
  static BoxDecoration glassCardDecoration(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    
    return BoxDecoration(
      color: isDark 
          ? AppColors.surfaceGlassDark
          : AppColors.surfaceGlassLight,
      borderRadius: BorderRadius.circular(AppRadius.lg),
      border: Border.all(
        color: Colors.white.withOpacity(0.2),
        width: 1,
      ),
      boxShadow: AppShadows.lg,
    );
  }
}
```

### Animation System

#### Transition Durations
```css
/* Legacy CSS (lines 236-250) */
--duration-fast: 150ms;
--duration-normal: 300ms;
--duration-slow: 500ms;
--duration-slower: 700ms;
```

```dart
// Flutter Animation Durations
class AppDuration {
  static const Duration fast = Duration(milliseconds: 150);
  static const Duration normal = Duration(milliseconds: 300);
  static const Duration slow = Duration(milliseconds: 500);
  static const Duration slower = Duration(milliseconds
