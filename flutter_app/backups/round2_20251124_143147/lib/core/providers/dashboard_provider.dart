/// Dashboard Provider - Simplified for immediate compilation
library;

import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Dashboard provider state
class DashboardProviderState {
  const DashboardProviderState({
    required this.totalPlants,
    required this.activePlants,
    required this.totalSensors,
    required this.onlineSensors,
    this.isLoading = false,
    this.error,
  });

  final int totalPlants;
  final int activePlants;
  final int totalSensors;
  final int onlineSensors;
  final bool isLoading;
  final String? error;

  bool get hasError => error != null;

  DashboardProviderState copyWith({
    int? totalPlants,
    int? activePlants,
    int? totalSensors,
    int? onlineSensors,
    bool? isLoading,
    String? error,
  }) {
    return DashboardProviderState(
      totalPlants: totalPlants ?? this.totalPlants,
      activePlants: activePlants ?? this.activePlants,
      totalSensors: totalSensors ?? this.totalSensors,
      onlineSensors: onlineSensors ?? this.onlineSensors,
      isLoading: isLoading ?? this.isLoading,
      error: error ?? this.error,
    );
  }
}

/// Simple provider for dashboard state
final dashboardProvider = Provider<DashboardProviderState>((ref) {
  return const DashboardProviderState(
    totalPlants: 24,
    activePlants: 18,
    totalSensors: 8,
    onlineSensors: 7,
  );
});

/// Convenience providers
final totalPlantsProvider = Provider<int>((ref) {
  final dashboardState = ref.watch(dashboardProvider);
  return dashboardState.totalPlants;
});

final activePlantsProvider = Provider<int>((ref) {
  final dashboardState = ref.watch(dashboardProvider);
  return dashboardState.activePlants;
});

final onlineSensorsProvider = Provider<int>((ref) {
  final dashboardState = ref.watch(dashboardProvider);
  return dashboardState.onlineSensors;
});

final totalSensorsProvider = Provider<int>((ref) {
  final dashboardState = ref.watch(dashboardProvider);
  return dashboardState.totalSensors;
});

final dashboardLoadingProvider = Provider<bool>((ref) {
  final dashboardState = ref.watch(dashboardProvider);
  return dashboardState.isLoading;
});

final dashboardErrorProvider = Provider<String?>((ref) {
  final dashboardState = ref.watch(dashboardProvider);
  return dashboardState.error;
});
