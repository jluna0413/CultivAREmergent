import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/providers/api_client_provider.dart';
import '../data/dashboard_api_client.dart';
import '../domain/dashboard_stats_model.dart';

// Imports for Plants
import '../../plants/data/plants_api_client.dart';
import '../../plants/domain/plant_model.dart';

final dashboardApiClientProvider = Provider<DashboardApiClient>((ref) {
  return DashboardApiClient(ref.read(apiClientProvider));
});

final dashboardStatsProvider = FutureProvider<DashboardStats>((ref) {
  return ref.watch(dashboardApiClientProvider).getDashboardStats();
});

final recentActivitiesProvider = FutureProvider<List<RecentActivity>>((ref) {
  return ref.watch(dashboardApiClientProvider).getRecentActivities();
});

final autoRefreshDashboardProvider = StreamProvider.autoDispose((ref) {
  return Stream.periodic(const Duration(minutes: 1), (_) {
    ref.invalidate(dashboardStatsProvider);
  });
});

// Derived providers for environmental stats
final avgTemperatureProvider = Provider<double?>((ref) {
  return ref.watch(dashboardStatsProvider).value?.environment.avgTemperature;
});

final avgHumidityProvider = Provider<double?>((ref) {
  return ref.watch(dashboardStatsProvider).value?.environment.avgHumidity;
});

final avgPhProvider = Provider<double?>((ref) {
  return ref.watch(dashboardStatsProvider).value?.environment.avgPh;
});

final avgEcProvider = Provider<double?>((ref) {
  return ref.watch(dashboardStatsProvider).value?.environment.avgEc;
});

// Derived providers for sensor stats
final totalSensorsProvider = Provider<int?>((ref) {
  return ref.watch(dashboardStatsProvider).value?.sensors.totalSensors;
});

final activeSensorsProvider = Provider<int?>((ref) {
  return ref.watch(dashboardStatsProvider).value?.sensors.activeSensors;
});

final lastReadingTimeProvider = Provider<DateTime?>((ref) {
  return ref.watch(dashboardStatsProvider).value?.sensors.lastReadingTime;
});

// Plants API Client Provider
final plantsApiClientProvider = Provider<PlantsApiClient>((ref) {
  return PlantsApiClient(ref.read(apiClientProvider));
});

// Recent Plants Provider

// Recent Plants Provider
final recentPlantsProvider = FutureProvider<List<Plant>>((ref) async {
  final response = await ref.watch(plantsApiClientProvider).getPlants(limit: 5);
  return response.items;
});
