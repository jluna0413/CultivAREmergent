// lib/features/onboarding/ui/genetics_onboarding_screen.dart

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_animate/flutter_animate.dart';

import '../domain/onboarding_state.dart';
import '../providers/onboarding_provider.dart';

/// Genetics Collection Screen - Step 2 of Onboarding
/// Allows users to add strains via manual entry or OCR scan (premium)
class GeneticsOnboardingScreen extends ConsumerStatefulWidget {
  const GeneticsOnboardingScreen({super.key});

  @override
  ConsumerState<GeneticsOnboardingScreen> createState() =>
      _GeneticsOnboardingScreenState();
}

class _GeneticsOnboardingScreenState
    extends ConsumerState<GeneticsOnboardingScreen> {
  final _formKey = GlobalKey<FormState>();
  final _strainNameController = TextEditingController();
  final _breederNameController = TextEditingController();
  GeneticType _selectedType = GeneticType.seed;
  bool _isManualEntry = true;

  @override
  void dispose() {
    _strainNameController.dispose();
    _breederNameController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final onboardingState = ref.watch(onboardingProvider);
    final isPremium = ref.watch(isPremiumProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Genetics Collection'),
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
                // Hero section
                _buildHeroSection(theme, colorScheme),
                const SizedBox(height: 32),

                // Entry mode toggle
                _buildModeToggle(theme, colorScheme, isPremium),
                const SizedBox(height: 24),

                // Main content card
                Card(
                  elevation: 0,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                    side: BorderSide(color: colorScheme.outlineVariant),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(20),
                    child: _isManualEntry
                        ? _buildManualEntryForm(theme, colorScheme)
                        : _buildOcrScanner(theme, colorScheme, isPremium),
                  ),
                ).animate().fadeIn(duration: 300.ms).slideY(begin: 0.1, end: 0),

                const SizedBox(height: 32),

                // Added genetics list or empty state
                if (state.genetics.isEmpty)
                  _buildEmptyState(theme, colorScheme)
                else ...[
                  _buildCollectionHeader(
                    theme,
                    colorScheme,
                    state.genetics.length,
                  ),
                  const SizedBox(height: 12),
                  ...state.genetics.map(
                    (genetic) => _buildGeneticCard(theme, colorScheme, genetic),
                  ),
                ],

                const SizedBox(height: 40),

                // Continue or skip buttons
                _buildActionButtons(
                  theme,
                  colorScheme,
                  state.genetics.isNotEmpty,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildHeroSection(ThemeData theme, ColorScheme colorScheme) {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.all(24),
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: [
                colorScheme.primaryContainer,
                colorScheme.secondaryContainer,
              ],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
            borderRadius: BorderRadius.circular(20),
          ),
          child: Column(
            children: [
              Icon(
                Icons.eco,
                size: 56,
                color: colorScheme.onPrimaryContainer,
              ).animate().scale(duration: 400.ms, delay: 100.ms),
              const SizedBox(height: 16),
              Text(
                'Build Your Genetics Library',
                style: theme.textTheme.headlineSmall?.copyWith(
                  fontWeight: FontWeight.bold,
                  color: colorScheme.onPrimaryContainer,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 8),
              Text(
                'Add strains to track lineage, optimize grows, and maintain your collection',
                style: theme.textTheme.bodyMedium?.copyWith(
                  color: colorScheme.onPrimaryContainer.withOpacity(0.8),
                ),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ).animate().fadeIn(duration: 400.ms).slideY(begin: -0.1, end: 0),
      ],
    );
  }

  Widget _buildEmptyState(ThemeData theme, ColorScheme colorScheme) {
    return Container(
      padding: const EdgeInsets.all(32),
      decoration: BoxDecoration(
        color: colorScheme.surfaceContainerLow,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: colorScheme.outlineVariant,
          style: BorderStyle.solid,
          width: 2,
        ),
      ),
      child: Column(
        children: [
          Icon(
            Icons.add_circle_outline,
            size: 64,
            color: colorScheme.onSurfaceVariant.withOpacity(0.5),
          ),
          const SizedBox(height: 16),
          Text(
            'Your collection is empty',
            style: theme.textTheme.titleMedium?.copyWith(
              color: colorScheme.onSurfaceVariant,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            'Add your first strain using the form above',
            style: theme.textTheme.bodyMedium?.copyWith(
              color: colorScheme.onSurfaceVariant.withOpacity(0.7),
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    ).animate().fadeIn(duration: 300.ms);
  }

  Widget _buildCollectionHeader(
    ThemeData theme,
    ColorScheme colorScheme,
    int count,
  ) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(
          'Your Collection',
          style: theme.textTheme.titleLarge?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
          decoration: BoxDecoration(
            color: colorScheme.primaryContainer,
            borderRadius: BorderRadius.circular(20),
          ),
          child: Text(
            '$count ${count == 1 ? 'Strain' : 'Strains'}',
            style: theme.textTheme.labelMedium?.copyWith(
              color: colorScheme.onPrimaryContainer,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ],
    ).animate().fadeIn(duration: 200.ms);
  }

  Widget _buildModeToggle(
    ThemeData theme,
    ColorScheme colorScheme,
    bool isPremium,
  ) {
    return Row(
      children: [
        Expanded(
          child: _buildToggleButton(
            theme,
            colorScheme,
            label: 'Manual Entry',
            isSelected: _isManualEntry,
            onTap: () => setState(() => _isManualEntry = true),
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: _buildToggleButton(
            theme,
            colorScheme,
            label: 'AI Scan (Premium)',
            isSelected: !_isManualEntry,
            isDisabled: !isPremium,
            icon: isPremium ? null : Icons.lock_outline,
            onTap: isPremium
                ? () => setState(() => _isManualEntry = false)
                : null,
          ),
        ),
      ],
    );
  }

  Widget _buildToggleButton(
    ThemeData theme,
    ColorScheme colorScheme, {
    required String label,
    required bool isSelected,
    bool isDisabled = false,
    IconData? icon,
    VoidCallback? onTap,
  }) {
    return Material(
      color: isSelected
          ? colorScheme.primary
          : colorScheme.surfaceContainerHighest,
      borderRadius: BorderRadius.circular(12),
      child: InkWell(
        onTap: isDisabled ? null : onTap,
        borderRadius: BorderRadius.circular(12),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 16),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (icon != null) ...[
                Icon(
                  icon,
                  size: 18,
                  color: isSelected
                      ? colorScheme.onPrimary
                      : colorScheme.onSurfaceVariant,
                ),
                const SizedBox(width: 6),
              ],
              Text(
                label,
                style: theme.textTheme.bodyMedium?.copyWith(
                  color: isSelected
                      ? colorScheme.onPrimary
                      : colorScheme.onSurfaceVariant,
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildManualEntryForm(ThemeData theme, ColorScheme colorScheme) {
    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          TextFormField(
            controller: _strainNameController,
            decoration: InputDecoration(
              labelText: 'Strain Name',
              hintText: 'e.g., Blue Dream',
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
            validator: (value) =>
                value?.isEmpty ?? true ? 'Please enter a strain name' : null,
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: _breederNameController,
            decoration: InputDecoration(
              labelText: 'Breeder Name',
              hintText: 'e.g., Humboldt Seed Co',
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
            validator: (value) =>
                value?.isEmpty ?? true ? 'Please enter a breeder name' : null,
          ),
          const SizedBox(height: 16),
          DropdownButtonFormField<GeneticType>(
            initialValue: _selectedType,
            decoration: InputDecoration(
              labelText: 'Type (Seed/Clone)',
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
            items: GeneticType.values.map((type) {
              return DropdownMenuItem(
                value: type,
                child: Text(
                  type.name[0].toUpperCase() + type.name.substring(1),
                ),
              );
            }).toList(),
            onChanged: (value) {
              if (value != null) {
                setState(() => _selectedType = value);
              }
            },
          ),
          const SizedBox(height: 24),
          FilledButton(
            onPressed: _addGenetic,
            style: FilledButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
            child: const Text('Add to Collection'),
          ),
        ],
      ),
    );
  }

  Widget _buildOcrScanner(
    ThemeData theme,
    ColorScheme colorScheme,
    bool isPremium,
  ) {
    return Column(
      children: [
        Container(
          height: 200,
          decoration: BoxDecoration(
            color: colorScheme.surfaceContainerLow,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: colorScheme.outline),
          ),
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  Icons.camera_alt_outlined,
                  size: 48,
                  color: colorScheme.onSurfaceVariant,
                ),
                const SizedBox(height: 12),
                Text(
                  'Scan seed packaging',
                  style: theme.textTheme.bodyLarge?.copyWith(
                    color: colorScheme.onSurfaceVariant,
                  ),
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 16),
        FilledButton.icon(
          onPressed: _openCamera,
          icon: const Icon(Icons.qr_code_scanner),
          label: const Text('Open Scanner'),
          style: FilledButton.styleFrom(
            padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 24),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildGeneticCard(
    ThemeData theme,
    ColorScheme colorScheme,
    GeneticItem genetic,
  ) {
    return Card(
      elevation: 0,
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(color: colorScheme.outlineVariant, width: 1.5),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            // Icon
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: colorScheme.primaryContainer,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(
                genetic.type == GeneticType.seed
                    ? Icons.grain
                    : Icons.content_cut,
                color: colorScheme.onPrimaryContainer,
                size: 24,
              ),
            ),
            const SizedBox(width: 16),
            // Content
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    genetic.strainName,
                    style: theme.textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Row(
                    children: [
                      Icon(
                        Icons.business_outlined,
                        size: 14,
                        color: colorScheme.onSurfaceVariant,
                      ),
                      const SizedBox(width: 4),
                      Text(
                        genetic.breederName,
                        style: theme.textTheme.bodySmall?.copyWith(
                          color: colorScheme.onSurfaceVariant,
                        ),
                      ),
                      const SizedBox(width: 8),
                      // Type chip
                      Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 8,
                          vertical: 2,
                        ),
                        decoration: BoxDecoration(
                          color: genetic.type == GeneticType.seed
                              ? colorScheme.tertiaryContainer
                              : colorScheme.secondaryContainer,
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          genetic.type.name[0].toUpperCase() +
                              genetic.type.name.substring(1),
                          style: theme.textTheme.labelSmall?.copyWith(
                            color: genetic.type == GeneticType.seed
                                ? colorScheme.onTertiaryContainer
                                : colorScheme.onSecondaryContainer,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            // Delete button
            IconButton(
              icon: const Icon(Icons.delete_outline),
              color: colorScheme.error,
              onPressed: () {
                ref.read(onboardingProvider.notifier).removeGenetic(genetic.id);
              },
              tooltip: 'Remove',
            ),
          ],
        ),
      ),
    ).animate().fadeIn(duration: 200.ms).slideX(begin: -0.05, end: 0);
  }

  Widget _buildActionButtons(
    ThemeData theme,
    ColorScheme colorScheme,
    bool hasGenetics,
  ) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        if (hasGenetics) ...[
          Text(
            'Ready to continue?',
            style: theme.textTheme.titleMedium,
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(
                child: OutlinedButton(
                  onPressed: () {
                    // Reset form to add more
                    _strainNameController.clear();
                    _breederNameController.clear();
                    setState(() => _selectedType = GeneticType.seed);
                  },
                  style: OutlinedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: const Text('Add More'),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                flex: 2,
                child: FilledButton(
                  onPressed: () {
                    ref.read(onboardingProvider.notifier).nextStep();
                    context.go('/onboarding/environment');
                  },
                  style: FilledButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: const Text('Continue to Environment'),
                ),
              ),
            ],
          ),
        ] else ...[
          FilledButton.tonalIcon(
            onPressed: () {
              ref.read(onboardingProvider.notifier).nextStep();
              context.go('/onboarding/environment');
            },
            icon: const Icon(Icons.skip_next),
            label: const Text('Skip for Now'),
            style: FilledButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 24),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
          ),
          const SizedBox(height: 8),
          Text(
            'You can always add genetics later',
            style: theme.textTheme.bodySmall?.copyWith(
              color: colorScheme.onSurfaceVariant,
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ],
    );
  }

  Widget _buildContinueSection(ThemeData theme, ColorScheme colorScheme) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text(
          'Ready to start your first grow?',
          style: theme.textTheme.titleMedium,
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 16),
        Row(
          children: [
            Expanded(
              child: OutlinedButton(
                onPressed: () {
                  // Reset form to add more
                  _strainNameController.clear();
                  _breederNameController.clear();
                  setState(() => _selectedType = GeneticType.seed);
                },
                style: OutlinedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: const Text('Add More'),
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: FilledButton(
                onPressed: () {
                  ref.read(onboardingProvider.notifier).nextStep();
                  context.go('/onboarding/environment');
                },
                style: FilledButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: const Text('Yes, Continue'),
              ),
            ),
          ],
        ),
      ],
    );
  }

  void _addGenetic() {
    if (_formKey.currentState?.validate() ?? false) {
      final genetic = GeneticItem(
        id: DateTime.now().millisecondsSinceEpoch.toString(),
        strainName: _strainNameController.text.trim(),
        breederName: _breederNameController.text.trim(),
        type: _selectedType,
      );

      ref.read(onboardingProvider.notifier).addGenetic(genetic);

      _strainNameController.clear();
      _breederNameController.clear();
      setState(() => _selectedType = GeneticType.seed);

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('${genetic.strainName} added to collection'),
          behavior: SnackBarBehavior.floating,
        ),
      );
    }
  }

  void _openCamera() {
    // Mock OCR - would open camera and scan in real implementation
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('OCR Scanner - Coming Soon'),
        behavior: SnackBarBehavior.floating,
      ),
    );
  }
}
