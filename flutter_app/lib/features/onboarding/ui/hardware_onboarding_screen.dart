// lib/features/onboarding/ui/hardware_onboarding_screen.dart

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_animate/flutter_animate.dart';

import '../domain/onboarding_state.dart';
import '../providers/onboarding_provider.dart';

/// Hardware Integration Screen - Step 4 of Onboarding
/// Allows users to link hardware manufacturer accounts
class HardwareOnboardingScreen extends ConsumerStatefulWidget {
  const HardwareOnboardingScreen({super.key});

  @override
  ConsumerState<HardwareOnboardingScreen> createState() =>
      _HardwareOnboardingScreenState();
}

class _HardwareOnboardingScreenState
    extends ConsumerState<HardwareOnboardingScreen> {
  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final onboardingState = ref.watch(onboardingProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Hardware Setup'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.pop(),
        ),
      ),
      body: SafeArea(
        child: onboardingState.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (e, _) => Center(child: Text('Error: $e')),
          data: (state) => SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Text(
                  'Choose Manufacturer',
                  style: theme.textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  'Connect your smart devices for automated monitoring',
                  style: theme.textTheme.bodyMedium?.copyWith(
                    color: colorScheme.onSurfaceVariant,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 32),

                // Manufacturer grid
                _buildManufacturerGrid(state, theme, colorScheme),

                const SizedBox(height: 32),

                // Finish button
                FilledButton(
                  onPressed: state.isSubmitting
                      ? null
                      : () => _finishSetup(state),
                  style: FilledButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: state.isSubmitting
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Text('Finish Setup'),
                ),

                const SizedBox(height: 16),

                // Skip button
                TextButton(
                  onPressed: () => _skipHardware(),
                  child: const Text('Skip for now'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildManufacturerGrid(
    OnboardingState state,
    ThemeData theme,
    ColorScheme colorScheme,
  ) {
    return GridView.count(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisCount: 2,
      mainAxisSpacing: 16,
      crossAxisSpacing: 16,
      childAspectRatio: 1.2,
      children: HardwareManufacturer.values.map((manufacturer) {
        final isLinked = state.integrations.any(
          (i) => i.manufacturer == manufacturer && i.isLinked,
        );

        return _buildManufacturerCard(
          theme,
          colorScheme,
          manufacturer: manufacturer,
          isLinked: isLinked,
        );
      }).toList(),
    ).animate().fadeIn(duration: 300.ms);
  }

  Widget _buildManufacturerCard(
    ThemeData theme,
    ColorScheme colorScheme, {
    required HardwareManufacturer manufacturer,
    required bool isLinked,
  }) {
    final logoPath = _getManufacturerLogoPath(manufacturer);

    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: () => _handleManufacturerTap(manufacturer, isLinked),
        borderRadius: BorderRadius.circular(16),
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 200),
          decoration: BoxDecoration(
            image: logoPath != null
                ? DecorationImage(
                    image: AssetImage(logoPath),
                    fit: BoxFit.cover,
                    opacity: isLinked ? 0.3 : 0.15,
                    colorFilter: ColorFilter.mode(
                      isLinked
                          ? colorScheme.primaryContainer
                          : colorScheme.surfaceContainerHighest,
                      BlendMode.multiply,
                    ),
                  )
                : null,
            color: logoPath == null
                ? (isLinked
                      ? colorScheme.primaryContainer
                      : colorScheme.surfaceContainerHighest)
                : null,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(
              color: isLinked ? colorScheme.primary : colorScheme.outline,
              width: isLinked ? 2 : 1,
            ),
          ),
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (logoPath == null)
                Icon(
                  _getManufacturerIcon(manufacturer),
                  size: 40,
                  color: isLinked
                      ? colorScheme.primary
                      : colorScheme.onSurfaceVariant,
                ),
              if (logoPath == null) const SizedBox(height: 8),
              Text(
                manufacturer.displayName,
                style: theme.textTheme.titleSmall?.copyWith(
                  color: isLinked
                      ? colorScheme.onPrimaryContainer
                      : colorScheme.onSurface,
                  fontWeight: FontWeight.bold,
                  shadows: logoPath != null
                      ? [
                          Shadow(
                            color: Colors.black.withOpacity(0.5),
                            blurRadius: 4,
                          ),
                        ]
                      : null,
                ),
                textAlign: TextAlign.center,
              ),
              if (manufacturer == HardwareManufacturer.acInfinity && !isLinked)
                Padding(
                  padding: const EdgeInsets.only(top: 8),
                  child: FilledButton.tonal(
                    onPressed: () => _showLoginDialog(manufacturer),
                    style: FilledButton.styleFrom(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 4,
                      ),
                      minimumSize: Size.zero,
                      tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                    ),
                    child: const Text('Log In'),
                  ),
                ),
              if (isLinked)
                Padding(
                  padding: const EdgeInsets.only(top: 8),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(
                        Icons.check_circle,
                        size: 16,
                        color: colorScheme.primary,
                      ),
                      const SizedBox(width: 4),
                      Text(
                        'Connected',
                        style: theme.textTheme.bodySmall?.copyWith(
                          color: colorScheme.primary,
                        ),
                      ),
                    ],
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildManufacturerImage(
    HardwareManufacturer manufacturer,
    bool isLinked,
    ColorScheme colorScheme,
  ) {
    String? logoPath;

    switch (manufacturer) {
      case HardwareManufacturer.acInfinity:
        logoPath = 'assets/images/manufacturers/ac_infinity_logo.jpg';
        break;
      case HardwareManufacturer.vivosun:
        logoPath = 'assets/images/manufacturers/vivosun_logo.png';
        break;
      case HardwareManufacturer.spiderFarmer:
        logoPath = 'assets/images/manufacturers/spider_farmer_logo.png';
        break;
      default:
        logoPath = null;
    }

    if (logoPath != null) {
      return Container(
        width: 60,
        height: 60,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(8),
          color: Colors.white,
        ),
        padding: const EdgeInsets.all(8),
        child: Image.asset(logoPath, fit: BoxFit.contain),
      );
    }

    // Fallback to icon for manufacturers without logos
    return Icon(
      _getManufacturerIcon(manufacturer),
      size: 40,
      color: isLinked ? colorScheme.primary : colorScheme.onSurfaceVariant,
    );
  }

  String? _getManufacturerLogoPath(HardwareManufacturer manufacturer) {
    switch (manufacturer) {
      case HardwareManufacturer.acInfinity:
        return 'assets/images/manufacturers/ac_infinity_logo.jpg';
      case HardwareManufacturer.vivosun:
        return 'assets/images/manufacturers/vivosun_logo.png';
      case HardwareManufacturer.spiderFarmer:
        return 'assets/images/manufacturers/spider_farmer_logo.png';
      default:
        return null;
    }
  }

  IconData _getManufacturerIcon(HardwareManufacturer manufacturer) {
    switch (manufacturer) {
      case HardwareManufacturer.acInfinity:
        return Icons.air;
      case HardwareManufacturer.ecowitt:
        return Icons.eco;
      case HardwareManufacturer.vivosun:
        return Icons.wb_sunny_outlined;
      case HardwareManufacturer.spiderFarmer:
        return Icons.bug_report_outlined;
      case HardwareManufacturer.marsHydro:
        return Icons.water_drop_outlined;
      case HardwareManufacturer.other:
        return Icons.help_outline;
    }
  }

  void _handleManufacturerTap(
    HardwareManufacturer manufacturer,
    bool isLinked,
  ) {
    if (isLinked) {
      // Disconnect
      ref
          .read(onboardingProvider.notifier)
          .removeHardwareIntegration(manufacturer);
    } else if (manufacturer == HardwareManufacturer.acInfinity) {
      // Show login dialog for AC Infinity
      _showLoginDialog(manufacturer);
    } else {
      // For other manufacturers, just add as "interested" but not linked
      ref
          .read(onboardingProvider.notifier)
          .addHardwareIntegration(
            HardwareIntegration(manufacturer: manufacturer, isLinked: false),
          );
    }
  }

  void _showLoginDialog(HardwareManufacturer manufacturer) {
    final emailController = TextEditingController();
    final passwordController = TextEditingController();

    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text('Connect ${manufacturer.displayName}'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: emailController,
                decoration: const InputDecoration(
                  labelText: 'Email',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.emailAddress,
              ),
              const SizedBox(height: 16),
              TextField(
                controller: passwordController,
                decoration: const InputDecoration(
                  labelText: 'Password',
                  border: OutlineInputBorder(),
                ),
                obscureText: true,
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancel'),
            ),
            FilledButton(
              onPressed: () async {
                final nav = Navigator.of(context);
                final messenger = ScaffoldMessenger.of(context);
                nav.pop();

                await ref
                    .read(onboardingProvider.notifier)
                    .mockAcInfinityLogin(
                      emailController.text,
                      passwordController.text,
                    );

                if (mounted) {
                  messenger.showSnackBar(
                    const SnackBar(
                      content: Text('Successfully connected to AC Infinity!'),
                      behavior: SnackBarBehavior.floating,
                    ),
                  );
                }
              },
              child: const Text('Connect'),
            ),
          ],
        );
      },
    );
  }

  void _finishSetup(OnboardingState state) async {
    // TODO: Get actual user ID from auth provider
    const mockUserId = '00000000-0000-0000-0000-000000000001';

    final success = await ref
        .read(onboardingProvider.notifier)
        .completeOnboarding(mockUserId);

    if (success && mounted) {
      context.go('/dashboard');
    }
  }

  void _skipHardware() {
    context.go('/dashboard');
  }
}
