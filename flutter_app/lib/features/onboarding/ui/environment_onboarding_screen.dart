// lib/features/onboarding/ui/environment_onboarding_screen.dart

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_animate/flutter_animate.dart';

import '../domain/onboarding_state.dart';
import '../logic/pot_placement_logic.dart';
import '../providers/onboarding_provider.dart';
import 'widgets/tent_visualizer.dart';

/// Environment Setup Screen - Step 3 of Onboarding
/// Allows users to configure their grow environment with tent visualizer
class EnvironmentOnboardingScreen extends ConsumerStatefulWidget {
  const EnvironmentOnboardingScreen({super.key});

  @override
  ConsumerState<EnvironmentOnboardingScreen> createState() =>
      _EnvironmentOnboardingScreenState();
}

class _EnvironmentOnboardingScreenState
    extends ConsumerState<EnvironmentOnboardingScreen> {
  int _currentPhase = 0; // 0: Type, 1: Size, 2: Pot Layout
  String? _selectedPotId;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final onboardingState = ref.watch(onboardingProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Environment Setup'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () {
            if (_currentPhase > 0) {
              setState(() => _currentPhase--);
            } else {
              context.pop();
            }
          },
        ),
      ),
      body: SafeArea(
        child: onboardingState.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (e, _) => Center(child: Text('Error: $e')),
          data: (state) => Padding(
            padding: const EdgeInsets.all(24),
            child: AnimatedSwitcher(
              duration: const Duration(milliseconds: 300),
              child: _buildPhaseContent(state, theme, colorScheme),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildPhaseContent(
    OnboardingState state,
    ThemeData theme,
    ColorScheme colorScheme,
  ) {
    switch (_currentPhase) {
      case 0:
        return _buildTypeSelector(state, theme, colorScheme);
      case 1:
        return _buildSizeSelector(state, theme, colorScheme);
      case 2:
        return _buildPotLayout(state, theme, colorScheme);
      default:
        return _buildTypeSelector(state, theme, colorScheme);
    }
  }

  Widget _buildTypeSelector(
    OnboardingState state,
    ThemeData theme,
    ColorScheme colorScheme,
  ) {
    return Column(
      key: const ValueKey('phase0'),
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text(
          'Select Environment Type',
          style: theme.textTheme.headlineSmall?.copyWith(
            fontWeight: FontWeight.bold,
          ),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 32),
        Expanded(
          child: Row(
            children: [
              _buildEnvironmentTypeCard(
                theme,
                colorScheme,
                type: EnvironmentType.tent,
                icon: Icons.home_outlined,
                label: 'Tent',
                isSelected:
                    state.selectedEnvironmentType == EnvironmentType.tent,
              ),
              const SizedBox(width: 16),
              _buildEnvironmentTypeCard(
                theme,
                colorScheme,
                type: EnvironmentType.greenhouse,
                icon: Icons.house_outlined,
                label: 'Greenhouse',
                isSelected:
                    state.selectedEnvironmentType == EnvironmentType.greenhouse,
              ),
              const SizedBox(width: 16),
              _buildEnvironmentTypeCard(
                theme,
                colorScheme,
                type: EnvironmentType.outdoors,
                icon: Icons.wb_sunny_outlined,
                label: 'Outdoors',
                isSelected:
                    state.selectedEnvironmentType == EnvironmentType.outdoors,
              ),
            ],
          ),
        ),
        const SizedBox(height: 24),
        _buildNextButton(
          enabled: state.selectedEnvironmentType != null,
          onPressed: () {
            if (state.selectedEnvironmentType == EnvironmentType.tent) {
              setState(() => _currentPhase = 1);
            } else {
              // Skip to hardware for non-tent environments
              ref
                  .read(onboardingProvider.notifier)
                  .finalizeEnvironmentConfig(
                    'My ${state.selectedEnvironmentType?.name ?? 'Grow'}',
                  );
              context.go('/onboarding/hardware');
            }
          },
        ),
      ],
    ).animate().fadeIn(duration: 300.ms);
  }

  Widget _buildEnvironmentTypeCard(
    ThemeData theme,
    ColorScheme colorScheme, {
    required EnvironmentType type,
    required IconData icon,
    required String label,
    required bool isSelected,
  }) {
    return Expanded(
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: () {
            ref.read(onboardingProvider.notifier).setEnvironmentType(type);
          },
          borderRadius: BorderRadius.circular(16),
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 200),
            decoration: BoxDecoration(
              color: isSelected
                  ? colorScheme.primaryContainer
                  : colorScheme.surfaceContainerHighest,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(
                color: isSelected ? colorScheme.primary : colorScheme.outline,
                width: isSelected ? 2 : 1,
              ),
            ),
            padding: const EdgeInsets.all(20),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  icon,
                  size: 48,
                  color: isSelected
                      ? colorScheme.primary
                      : colorScheme.onSurfaceVariant,
                ),
                const SizedBox(height: 12),
                Text(
                  label,
                  style: theme.textTheme.titleMedium?.copyWith(
                    color: isSelected
                        ? colorScheme.primary
                        : colorScheme.onSurface,
                    fontWeight: isSelected
                        ? FontWeight.bold
                        : FontWeight.normal,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildSizeSelector(
    OnboardingState state,
    ThemeData theme,
    ColorScheme colorScheme,
  ) {
    return Column(
      key: const ValueKey('phase1'),
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text(
          'Select Tent Size',
          style: theme.textTheme.headlineSmall?.copyWith(
            fontWeight: FontWeight.bold,
          ),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 32),
        Expanded(
          child: GridView.count(
            crossAxisCount: 3,
            mainAxisSpacing: 16,
            crossAxisSpacing: 16,
            childAspectRatio: 1.5,
            children: TentDimensions.allSizes.map((tent) {
              final isSelected = state.selectedTentSize == tent.label;
              return Material(
                color: Colors.transparent,
                child: InkWell(
                  onTap: () {
                    ref
                        .read(onboardingProvider.notifier)
                        .setTentSize(tent.label);
                  },
                  borderRadius: BorderRadius.circular(12),
                  child: AnimatedContainer(
                    duration: const Duration(milliseconds: 200),
                    decoration: BoxDecoration(
                      color: isSelected
                          ? colorScheme.primary
                          : colorScheme.surfaceContainerHighest,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(
                        color: isSelected
                            ? colorScheme.primary
                            : colorScheme.outline,
                        width: isSelected ? 2 : 1,
                      ),
                    ),
                    alignment: Alignment.center,
                    child: Text(
                      tent.label,
                      style: theme.textTheme.titleLarge?.copyWith(
                        color: isSelected
                            ? colorScheme.onPrimary
                            : colorScheme.onSurface,
                        fontWeight: isSelected
                            ? FontWeight.bold
                            : FontWeight.normal,
                      ),
                    ),
                  ),
                ),
              );
            }).toList(),
          ),
        ),
        const SizedBox(height: 24),
        _buildNextButton(
          enabled: state.selectedTentSize != null,
          onPressed: () {
            // Default to 5 Gal if not set
            if (state.selectedPotSize == null) {
              ref.read(onboardingProvider.notifier).setPotSize('5 Gal');
            }
            setState(() => _currentPhase = 2);
          },
        ),
      ],
    ).animate().fadeIn(duration: 300.ms);
  }

  Widget _buildPotLayout(
    OnboardingState state,
    ThemeData theme,
    ColorScheme colorScheme,
  ) {
    final potPositions = ref.watch(potPositionsProvider);
    final tentSize = state.selectedTentSize ?? '4x4';
    final potSize = state.selectedPotSize ?? '5 Gal';
    final tent = TentDimensions.fromLabel(tentSize);

    return Column(
      key: const ValueKey('phase2'),
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text(
          'Configure Pot Layout',
          style: theme.textTheme.headlineSmall?.copyWith(
            fontWeight: FontWeight.bold,
          ),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 8),
        Text(
          '${potPositions.length} pots in $tentSize tent',
          style: theme.textTheme.bodyMedium?.copyWith(
            color: colorScheme.onSurfaceVariant,
          ),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 24),
        Expanded(
          child: TentVisualizer(
            tentDimensions: tent,
            potPositions: potPositions,
            potSizeLabel: potSize,
            selectedPotId: _selectedPotId,
            onPotTap: (potId) {
              setState(() {
                _selectedPotId = _selectedPotId == potId ? null : potId;
              });
            },
          ),
        ),
        const SizedBox(height: 16),
        PotSizeSelector(
          selectedSize: potSize,
          onSizeChanged: (size) {
            ref.read(onboardingProvider.notifier).setPotSize(size);
          },
        ),
        if (_selectedPotId != null) ...[
          const SizedBox(height: 16),
          _buildPotTypeSelector(theme, colorScheme),
        ],
        const SizedBox(height: 24),
        FilledButton(
          onPressed: () {
            ref
                .read(onboardingProvider.notifier)
                .finalizeEnvironmentConfig('My $tentSize Tent');
            ref.read(onboardingProvider.notifier).nextStep();
            context.go('/onboarding/hardware');
          },
          style: FilledButton.styleFrom(
            padding: const EdgeInsets.symmetric(vertical: 16),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
          child: const Text('Done'),
        ),
      ],
    ).animate().fadeIn(duration: 300.ms);
  }

  Widget _buildPotTypeSelector(ThemeData theme, ColorScheme colorScheme) {
    return Card(
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(color: colorScheme.outline),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Change Pot Type for $_selectedPotId',
              style: theme.textTheme.titleSmall,
            ),
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: PotType.values.map((type) {
                return ActionChip(
                  label: Text(type.displayName),
                  onPressed: () {
                    ref
                        .read(onboardingProvider.notifier)
                        .updatePotType(_selectedPotId!, type.name);
                    setState(() => _selectedPotId = null);
                  },
                );
              }).toList(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildNextButton({
    required bool enabled,
    required VoidCallback onPressed,
  }) {
    return FilledButton(
      onPressed: enabled ? onPressed : null,
      style: FilledButton.styleFrom(
        padding: const EdgeInsets.symmetric(vertical: 16),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),
      child: const Text('Next'),
    );
  }
}
