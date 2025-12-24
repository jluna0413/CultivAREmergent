// (removed stray library directive)

import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class ThemeToggleButton extends StatelessWidget {
  const ThemeToggleButton({
    super.key,
    required this.currentThemeMode,
    this.onChanged,
    this.size = 48,
    this.showLabels = false,
    this.compact = false,
  });

  final ThemeMode currentThemeMode;
  final void Function(ThemeMode)? onChanged;
  final double size;
  final bool showLabels;
  final bool compact;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Container(
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor.withAlpha(0x80),
        borderRadius: BorderRadius.circular(size / 2),
        border: Border.all(
          color: AppTheme.borderColor.withAlpha(0x33),
          width: 1,
        ),
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: () {
            final newMode = currentThemeMode == ThemeMode.light
                ? ThemeMode.dark
                : ThemeMode.light;
            onChanged?.call(newMode);
          },
          borderRadius: BorderRadius.circular(size / 2),
          child: Padding(
            padding: EdgeInsets.all(compact ? 4 : 8),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                // Light Theme Icon
                AnimatedContainer(
                  duration: const Duration(milliseconds: 200),
                  padding: const EdgeInsets.all(6),
                  decoration: BoxDecoration(
                    color: !isDark ? AppTheme.primaryColor : Colors.transparent,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Icon(
                    Icons.light_mode,
                    color: !isDark
                        ? AppTheme.onPrimary
                        : AppTheme.textSecondary,
                    size: compact ? 16 : 20,
                  ),
                ),

                const SizedBox(width: 4),

                // Dark Theme Icon
                AnimatedContainer(
                  duration: const Duration(milliseconds: 200),
                  padding: const EdgeInsets.all(6),
                  decoration: BoxDecoration(
                    color: isDark ? AppTheme.primaryColor : Colors.transparent,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Icon(
                    Icons.dark_mode,
                    color: isDark ? AppTheme.onPrimary : AppTheme.textSecondary,
                    size: compact ? 16 : 20,
                  ),
                ),

                // Labels (if enabled)
                if (showLabels) ...[
                  const SizedBox(width: 12),
                  Text(
                    isDark ? 'Dark' : 'Light',
                    style: theme.textTheme.bodyMedium?.copyWith(
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}

/// Compact theme toggle button for smaller spaces
class ThemeToggleButtonCompact extends StatelessWidget {
  const ThemeToggleButtonCompact({
    super.key,
    required this.currentThemeMode,
    this.onChanged,
  });

  final ThemeMode currentThemeMode;
  final void Function(ThemeMode)? onChanged;

  @override
  Widget build(BuildContext context) {
    return ThemeToggleButton(
      currentThemeMode: currentThemeMode,
      onChanged: onChanged,
      size: 36,
      compact: true,
    );
  }
}

/// Full theme toggle button with labels for larger components
class ThemeToggleButtonWithLabels extends StatelessWidget {
  const ThemeToggleButtonWithLabels({
    super.key,
    required this.currentThemeMode,
    this.onChanged,
  });

  final ThemeMode currentThemeMode;
  final void Function(ThemeMode)? onChanged;

  @override
  Widget build(BuildContext context) {
    return ThemeToggleButton(
      currentThemeMode: currentThemeMode,
      onChanged: onChanged,
      size: 56,
      showLabels: true,
      compact: false,
    );
  }
}

/// Theme toggle switch for material design switches
class ThemeToggleSwitch extends StatelessWidget {
  const ThemeToggleSwitch({
    super.key,
    required this.currentThemeMode,
    this.onChanged,
  });

  final ThemeMode currentThemeMode;
  final void Function(ThemeMode)? onChanged;

  @override
  Widget build(BuildContext context) {
    final isDark = currentThemeMode == ThemeMode.dark;

    return Switch(
      value: isDark,
      onChanged: (value) {
        onChanged?.call(value ? ThemeMode.dark : ThemeMode.light);
      },
      activeThumbColor: AppTheme.primaryColor,
      activeTrackColor: AppTheme.primaryColor.withAlpha(0x4D),
      inactiveThumbColor: AppTheme.textSecondary,
      inactiveTrackColor: AppTheme.textSecondary.withAlpha(0x4D),
    );
  }
}

/// Theme toggle segmented control for desktop/web
class ThemeToggleSegmented extends StatelessWidget {
  const ThemeToggleSegmented({
    super.key,
    required this.currentThemeMode,
    this.onChanged,
  });

  final ThemeMode currentThemeMode;
  final void Function(ThemeMode)? onChanged;

  @override
  Widget build(BuildContext context) {
    return SegmentedButton<ThemeMode>(
      segments: const [
        ButtonSegment(
          value: ThemeMode.light,
          icon: Icon(Icons.light_mode),
          label: Text('Light'),
        ),
        ButtonSegment(
          value: ThemeMode.dark,
          icon: Icon(Icons.dark_mode),
          label: Text('Dark'),
        ),
        ButtonSegment(
          value: ThemeMode.system,
          icon: Icon(Icons.brightness_auto),
          label: Text('Auto'),
        ),
      ],
      selected: {currentThemeMode},
      onSelectionChanged: (Set<ThemeMode> newSelection) {
        onChanged?.call(newSelection.first);
      },
      style: SegmentedButton.styleFrom(
        backgroundColor: AppTheme.surfaceColor.withAlpha(0x80),
        selectedBackgroundColor: AppTheme.primaryColor,
        selectedForegroundColor: AppTheme.onPrimary,
        foregroundColor: AppTheme.textSecondary,
        side: BorderSide(color: AppTheme.borderColor.withAlpha(0x33), width: 1),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      ),
    );
  }
}

/// Circular theme toggle button for floating action buttons
class ThemeToggleFloating extends StatelessWidget {
  const ThemeToggleFloating({
    super.key,
    required this.currentThemeMode,
    this.onChanged,
    this.size = 56,
  });

  final ThemeMode currentThemeMode;
  final void Function(ThemeMode)? onChanged;
  final double size;

  @override
  Widget build(BuildContext context) {
    final isDark = currentThemeMode == ThemeMode.dark;

    return FloatingActionButton(
      onPressed: () {
        final newMode = isDark ? ThemeMode.light : ThemeMode.dark;
        onChanged?.call(newMode);
      },
      backgroundColor: AppTheme.primaryColor,
      foregroundColor: AppTheme.onPrimary,
      mini: size < 48,
      child: AnimatedSwitcher(
        duration: const Duration(milliseconds: 200),
        child: Icon(
          key: ValueKey(isDark),
          isDark ? Icons.light_mode : Icons.dark_mode,
          size: size < 48 ? 20 : 24,
        ),
      ),
    );
  }
}

/// Theme toggle bar for settings pages
class ThemeToggleBar extends StatelessWidget {
  const ThemeToggleBar({
    super.key,
    required this.currentThemeMode,
    this.onChanged,
    this.title,
  });

  final ThemeMode currentThemeMode;
  final void Function(ThemeMode)? onChanged;
  final String? title;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Container(
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor.withAlpha(0xCC),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: AppTheme.borderColor.withAlpha(0x33),
          width: 1,
        ),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            if (title != null) ...[
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title!,
                      style: theme.textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'Choose your preferred theme',
                      style: theme.textTheme.bodySmall?.copyWith(
                        color: AppTheme.textSecondary,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 16),
            ],

            // Theme Options
            Container(
              decoration: BoxDecoration(
                color: AppTheme.backgroundColor.withAlpha(0x80),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(
                  color: AppTheme.borderColor.withAlpha(0x33),
                  width: 1,
                ),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  // Light Option
                  _buildThemeOption(
                    ThemeMode.light,
                    Icons.light_mode,
                    'Light',
                    currentThemeMode,
                    onChanged,
                    context,
                  ),

                  // Dark Option
                  _buildThemeOption(
                    ThemeMode.dark,
                    Icons.dark_mode,
                    'Dark',
                    currentThemeMode,
                    onChanged,
                    context,
                  ),

                  // System Option
                  _buildThemeOption(
                    ThemeMode.system,
                    Icons.brightness_auto,
                    'Auto',
                    currentThemeMode,
                    onChanged,
                    context,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildThemeOption(
    ThemeMode mode,
    IconData icon,
    String label,
    ThemeMode currentMode,
    void Function(ThemeMode)? onChanged,
    BuildContext context,
  ) {
    final isSelected = currentMode == mode;

    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: () => onChanged?.call(mode),
        borderRadius: BorderRadius.circular(8),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
          decoration: BoxDecoration(
            color: isSelected ? AppTheme.primaryColor : Colors.transparent,
            borderRadius: BorderRadius.circular(8),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                icon,
                color: isSelected ? AppTheme.onPrimary : AppTheme.textSecondary,
                size: 20,
              ),
              const SizedBox(height: 4),
              Text(
                label,
                style: TextStyle(
                  color: isSelected
                      ? AppTheme.onPrimary
                      : AppTheme.textSecondary,
                  fontSize: 12,
                  fontWeight: isSelected ? FontWeight.w600 : FontWeight.w400,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
