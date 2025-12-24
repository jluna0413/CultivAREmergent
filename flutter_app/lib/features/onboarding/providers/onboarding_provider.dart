// lib/features/onboarding/providers/onboarding_provider.dart

import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../domain/onboarding_state.dart';
import '../logic/pot_placement_logic.dart';

/// Main onboarding notifier for state management
class OnboardingNotifier extends AsyncNotifier<OnboardingState> {
  @override
  Future<OnboardingState> build() async {
    return const OnboardingState();
  }

  // ==================== NAVIGATION ====================

  /// Move to next step
  void nextStep() {
    final current = state.value;
    if (current == null) return;

    final steps = OnboardingStep.values;
    final currentIndex = steps.indexOf(current.currentStep);
    if (currentIndex < steps.length - 1) {
      state = AsyncValue.data(
        current.copyWith(currentStep: steps[currentIndex + 1]),
      );
    }
  }

  /// Move to previous step
  void previousStep() {
    final current = state.value;
    if (current == null) return;

    final steps = OnboardingStep.values;
    final currentIndex = steps.indexOf(current.currentStep);
    if (currentIndex > 0) {
      state = AsyncValue.data(
        current.copyWith(currentStep: steps[currentIndex - 1]),
      );
    }
  }

  /// Skip to specific step
  void goToStep(OnboardingStep step) {
    final current = state.value;
    if (current == null) return;

    state = AsyncValue.data(current.copyWith(currentStep: step));
  }

  // ==================== GENETICS ====================

  /// Add a genetic item to the collection
  void addGenetic(GeneticItem item) {
    final current = state.value;
    if (current == null) return;

    state = AsyncValue.data(
      current.copyWith(genetics: [...current.genetics, item]),
    );
  }

  /// Remove a genetic item from the collection
  void removeGenetic(String itemId) {
    final current = state.value;
    if (current == null) return;

    state = AsyncValue.data(
      current.copyWith(
        genetics: current.genetics.where((g) => g.id != itemId).toList(),
      ),
    );
  }

  /// Clear all genetics
  void clearGenetics() {
    final current = state.value;
    if (current == null) return;

    state = AsyncValue.data(current.copyWith(genetics: []));
  }

  // ==================== ENVIRONMENT ====================

  /// Set the environment type (Tent, Greenhouse, Outdoors)
  void setEnvironmentType(EnvironmentType type) {
    final current = state.value;
    if (current == null) return;

    state = AsyncValue.data(
      current.copyWith(
        selectedEnvironmentType: type,
        // Reset tent-specific settings when switching types
        selectedTentSize: type == EnvironmentType.tent
            ? current.selectedTentSize
            : null,
      ),
    );
  }

  /// Set the tent size
  void setTentSize(String sizeLabel) {
    final current = state.value;
    if (current == null) return;

    state = AsyncValue.data(current.copyWith(selectedTentSize: sizeLabel));
  }

  /// Set the pot size
  void setPotSize(String potSizeLabel) {
    final current = state.value;
    if (current == null) return;

    state = AsyncValue.data(current.copyWith(selectedPotSize: potSizeLabel));
  }

  /// Update a specific pot's type
  void updatePotType(String potId, String newPotType) {
    final current = state.value;
    if (current == null || current.environmentConfig == null) return;

    final updatedPots = current.environmentConfig!.pots.map((pot) {
      if (pot.id == potId) {
        return pot.copyWith(potType: newPotType);
      }
      return pot;
    }).toList();

    state = AsyncValue.data(
      current.copyWith(
        environmentConfig: current.environmentConfig!.copyWith(
          pots: updatedPots,
        ),
      ),
    );
  }

  /// Finalize environment configuration
  void finalizeEnvironmentConfig(String name) {
    final current = state.value;
    if (current == null) return;

    final envType = current.selectedEnvironmentType ?? EnvironmentType.tent;

    // Calculate pot positions if tent
    List<PotPositionData> pots = [];
    double? tentWidth;
    double? tentDepth;

    if (envType == EnvironmentType.tent && current.selectedTentSize != null) {
      final tent = TentDimensions.fromLabel(current.selectedTentSize!);
      final pot = PotDimensions.fromLabel(current.selectedPotSize ?? '5 Gal');

      tentWidth = tent.widthInches;
      tentDepth = tent.depthInches;

      final positions = calculatePotLayout(tent: tent, pot: pot);
      pots = positions
          .map(
            (p) => PotPositionData(
              id: p.id,
              potSizeLabel: pot.label,
              potType: p.potType,
              xPosition: p.x,
              yPosition: p.y,
            ),
          )
          .toList();
    }

    final config = EnvironmentConfig(
      name: name,
      environmentType: envType,
      tentWidthInches: tentWidth,
      tentDepthInches: tentDepth,
      tentSizeLabel: current.selectedTentSize,
      pots: pots,
    );

    state = AsyncValue.data(current.copyWith(environmentConfig: config));
  }

  // ==================== HARDWARE ====================

  /// Add a hardware integration
  void addHardwareIntegration(HardwareIntegration integration) {
    final current = state.value;
    if (current == null) return;

    // Remove existing integration for same manufacturer
    final filtered = current.integrations
        .where((i) => i.manufacturer != integration.manufacturer)
        .toList();

    state = AsyncValue.data(
      current.copyWith(integrations: [...filtered, integration]),
    );
  }

  /// Remove a hardware integration
  void removeHardwareIntegration(HardwareManufacturer manufacturer) {
    final current = state.value;
    if (current == null) return;

    state = AsyncValue.data(
      current.copyWith(
        integrations: current.integrations
            .where((i) => i.manufacturer != manufacturer)
            .toList(),
      ),
    );
  }

  /// Mock AC Infinity login
  Future<bool> mockAcInfinityLogin(String email, String password) async {
    // Simulate API call
    await Future.delayed(const Duration(seconds: 1));

    // Mock success for any credentials
    addHardwareIntegration(
      const HardwareIntegration(
        manufacturer: HardwareManufacturer.acInfinity,
        isLinked: true,
        linkedAccountId: 'mock_account_123',
      ),
    );

    return true;
  }

  // ==================== SUBMISSION ====================

  /// Complete onboarding - POST to backend
  Future<bool> completeOnboarding(String userId) async {
    final current = state.value;
    if (current == null) return false;

    state = AsyncValue.data(current.copyWith(isSubmitting: true, error: null));

    try {
      // TODO: Replace with actual API call
      // final payload = {
      //   'user_id': userId,
      //   'genetics': current.genetics.map((g) => g.toJson()).toList(),
      //   'environments': current.environmentConfig != null
      //       ? [current.environmentConfig!.toJson()]
      //       : [],
      //   'integrations': current.integrations.map((i) => i.toJson()).toList(),
      // };

      // Simulate API call
      await Future.delayed(const Duration(seconds: 2));

      state = AsyncValue.data(
        current.copyWith(
          isSubmitting: false,
          isCompleted: true,
          currentStep: OnboardingStep.complete,
        ),
      );
      return true;
    } catch (e) {
      state = AsyncValue.data(
        current.copyWith(
          isSubmitting: false,
          error: 'Failed to complete onboarding: $e',
        ),
      );
      return false;
    }
  }

  /// Reset onboarding state
  void reset() {
    state = const AsyncValue.data(OnboardingState());
  }
}

/// Main onboarding provider
final onboardingProvider =
    AsyncNotifierProvider<OnboardingNotifier, OnboardingState>(
      OnboardingNotifier.new,
    );

/// Computed provider for pot positions based on current selections
final potPositionsProvider = Provider<List<PotPosition>>((ref) {
  final onboardingState = ref.watch(onboardingProvider);

  return onboardingState.when(
    data: (state) {
      if (state.selectedTentSize == null || state.selectedPotSize == null) {
        return [];
      }

      final tent = TentDimensions.fromLabel(state.selectedTentSize!);
      final pot = PotDimensions.fromLabel(state.selectedPotSize!);

      return calculatePotLayout(tent: tent, pot: pot);
    },
    loading: () => [],
    error: (_, __) => [],
  );
});

/// Provider to check if user has premium features
final isPremiumProvider = Provider<bool>((ref) {
  // TODO: Connect to actual user provider
  return false; // Default to non-premium for now
});
