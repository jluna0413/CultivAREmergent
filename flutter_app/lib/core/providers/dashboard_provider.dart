/// Dashboard Provider - Real API integration with AsyncValue pattern
library;

import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../features/dashboard/data/dashboard_api_client.dart';
import '../../features/dashboard/domain/dashboard_stats_model.dart';
import '../../features/plants/domain/plant_model.dart';
// import '../../core/models/plant_models.dart' as core_plant; // Unused
import 'api_client_provider.dart';

/// Dashboard API client provider
final dashboardApiClientProvider = Provider<DashboardApiClient>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  return DashboardApiClient(apiClient);
});

/// Dashboard stats provider using AsyncValue pattern
final dashboardStatsProvider = FutureProvider<DashboardStats>((ref) async {
  final apiClient = ref.watch(dashboardApiClientProvider);

  try {
    final stats = await apiClient.getDashboardStats();
    return stats;
  } catch (e) {
    // Re-throw to let AsyncValue handle error state
    rethrow;
  }
});

/// Convenience providers for dashboard stats
final totalPlantsProvider = Provider<int>((ref) {
  final asyncStats = ref.watch(dashboardStatsProvider);
  return asyncStats.maybeWhen(
    data: (stats) => stats.counts.total,
    orElse: () => 0,
  );
});

final activePlantsProvider = Provider<int>((ref) {
  final asyncStats = ref.watch(dashboardStatsProvider);
  return asyncStats.maybeWhen(
    data: (stats) => stats.counts.active,
    orElse: () => 0,
  );
});

final strainsProvider = Provider<int>((ref) {
  final asyncStats = ref.watch(dashboardStatsProvider);
  return asyncStats.maybeWhen(
    data: (stats) => stats.cultivars.userCultivars,
    orElse: () => 0,
  );
});

final harvestedPlantsProvider = Provider<int>((ref) {
  final asyncStats = ref.watch(dashboardStatsProvider);
  return asyncStats.maybeWhen(
    data: (stats) => stats.counts.harvested,
    orElse: () => 0,
  );
});

// Recent plants provider
final recentPlantsProvider = FutureProvider<List<Plant>>((ref) async {
  final apiClient = ref.watch(apiClientProvider);
  final plants = await apiClient
      .getPlants(); // Returns List<core_plant.PlantModel>

  if (plants.isEmpty) return [];

  // Convert core_plant.PlantModel to features/plants/domain/Plant
  return plants
      .map(
        (p) => Plant(
          id: p.id,
          userId: p.userId,
          name: p.name,
          statusId: p.statusId,
          cultivarId: p.cultivarId,
          imageUrl:
              null, // PlantModel in core doesn't seem to have imageUrl exposed or it's named differently?
          // Checking core plant model: it DOES NOT have imageUrl.

          // We need to provide required fields
          strainName:
              'Unknown Strain', // Core model doesn't have strain name directly
          statusName: 'Growing', // Placeholder
          startDt: p.startDate,
        ),
      )
      .take(5)
      .toList();
});

/// Recent activities provider
final recentActivitiesProvider = Provider<List<RecentActivity>>((ref) {
  final asyncStats = ref.watch(dashboardStatsProvider);
  return asyncStats.maybeWhen(
    data: (stats) => stats.recentActivities,
    orElse: () => [],
  );
});

/// Loading state provider
final dashboardLoadingProvider = Provider<bool>((ref) {
  final asyncStats = ref.watch(dashboardStatsProvider);
  return asyncStats.isLoading;
});

/// Error state provider
final dashboardErrorProvider = Provider<String?>((ref) {
  final asyncStats = ref.watch(dashboardStatsProvider);
  return asyncStats.maybeWhen(
    error: (error, _) => error.toString(),
    orElse: () => null,
  );
});
