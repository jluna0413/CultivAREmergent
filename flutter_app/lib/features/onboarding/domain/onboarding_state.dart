// lib/features/onboarding/domain/onboarding_state.dart

import 'package:freezed_annotation/freezed_annotation.dart';

part 'onboarding_state.freezed.dart';
part 'onboarding_state.g.dart';

/// Onboarding step enum
enum OnboardingStep { welcome, genetics, environment, hardware, complete }

/// Genetic type (Seed or Clone)
enum GeneticType { seed, clone }

/// Environment type
enum EnvironmentType { tent, greenhouse, outdoors }

/// Hardware manufacturer
enum HardwareManufacturer {
  acInfinity('AC Infinity', 'ac_infinity'),
  ecowitt('Ecowitt', 'ecowitt'),
  vivosun('Vivosun', 'vivosun'),
  spiderFarmer('Spider-Farmer', 'spider_farmer'),
  marsHydro('Mars-Hydro', 'mars_hydro'),
  other('Other', 'other');

  final String displayName;
  final String apiValue;
  const HardwareManufacturer(this.displayName, this.apiValue);
}

/// Genetic item collected during onboarding
@freezed
class GeneticItem with _$GeneticItem {
  const factory GeneticItem({
    required String id,
    required String strainName,
    required String breederName,
    required GeneticType type,
    String? packagingImageUrl,
  }) = _GeneticItem;

  factory GeneticItem.fromJson(Map<String, dynamic> json) =>
      _$GeneticItemFromJson(json);
}

/// Pot position for environment config (serializable version)
@freezed
class PotPositionData with _$PotPositionData {
  const factory PotPositionData({
    required String id,
    required String potSizeLabel,
    @Default('fabric') String potType,
    required double xPosition,
    required double yPosition,
  }) = _PotPositionData;

  factory PotPositionData.fromJson(Map<String, dynamic> json) =>
      _$PotPositionDataFromJson(json);
}

/// Environment configuration
@freezed
class EnvironmentConfig with _$EnvironmentConfig {
  const factory EnvironmentConfig({
    required String name,
    required EnvironmentType environmentType,
    double? tentWidthInches,
    double? tentDepthInches,
    String? tentSizeLabel,
    @Default([]) List<PotPositionData> pots,
  }) = _EnvironmentConfig;

  factory EnvironmentConfig.fromJson(Map<String, dynamic> json) =>
      _$EnvironmentConfigFromJson(json);
}

/// Hardware integration
@freezed
class HardwareIntegration with _$HardwareIntegration {
  const factory HardwareIntegration({
    required HardwareManufacturer manufacturer,
    @Default(false) bool isLinked,
    String? linkedAccountId,
  }) = _HardwareIntegration;

  factory HardwareIntegration.fromJson(Map<String, dynamic> json) =>
      _$HardwareIntegrationFromJson(json);
}

/// Main onboarding state
@freezed
class OnboardingState with _$OnboardingState {
  const factory OnboardingState({
    @Default(OnboardingStep.welcome) OnboardingStep currentStep,
    @Default([]) List<GeneticItem> genetics,
    EnvironmentConfig? environmentConfig,
    @Default([]) List<HardwareIntegration> integrations,
    @Default(false) bool isCompleted,
    @Default(false) bool isSubmitting,
    String? error,
    // Environment setup state
    EnvironmentType? selectedEnvironmentType,
    String? selectedTentSize,
    String? selectedPotSize,
  }) = _OnboardingState;

  factory OnboardingState.fromJson(Map<String, dynamic> json) =>
      _$OnboardingStateFromJson(json);
}
