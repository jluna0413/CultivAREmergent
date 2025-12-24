/// AI Dashboard Provider - Real API integration with AsyncValue pattern
library;

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../features/ai/data/ai_dashboard_api_client.dart';
import '../../features/ai/domain/ai_dashboard_stats.dart';
import 'api_client_provider.dart';

/// AI Dashboard API client provider
final aiDashboardApiClientProvider = Provider<AIDashboardApiClient>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  return AIDashboardApiClient(apiClient);
});

/// AI Dashboard stats provider using AsyncValue pattern
final aiDashboardStatsProvider = FutureProvider<AIDashboardStats>((ref) async {
  final apiClient = ref.watch(aiDashboardApiClientProvider);

  try {
    final response = await apiClient.getAIDashboardStats();
    return AIDashboardStats.fromJson(response);
  } catch (e) {
    // Re-throw to let AsyncValue handle error state
    rethrow;
  }
});

/// Convenience providers for AI dashboard stats
final aiTotalQueriesProvider = Provider<int>((ref) {
  final asyncStats = ref.watch(aiDashboardStatsProvider);
  return asyncStats.maybeWhen(
    data: (stats) => stats.usage.totalQueries,
    orElse: () => 0,
  );
});

final aiTodayQueriesProvider = Provider<int>((ref) {
  final asyncStats = ref.watch(aiDashboardStatsProvider);
  return asyncStats.maybeWhen(
    data: (stats) => stats.usage.today,
    orElse: () => 0,
  );
});

final aiTopFeatureProvider = Provider<String>((ref) {
  final asyncStats = ref.watch(aiDashboardStatsProvider);
  return asyncStats.maybeWhen(
    data: (stats) => stats.usage.mostUsedFeature,
    orElse: () => 'None',
  );
});

final aiRecentActivitiesProvider = Provider<List<AIActivity>>((ref) {
  final asyncStats = ref.watch(aiDashboardStatsProvider);
  return asyncStats.maybeWhen(
    data: (stats) => stats.recentActivities,
    orElse: () => [],
  );
});

/// Loading state provider
final aiDashboardLoadingProvider = Provider<bool>((ref) {
  final asyncStats = ref.watch(aiDashboardStatsProvider);
  return asyncStats.isLoading;
});

/// Error state provider
final aiDashboardErrorProvider = Provider<String?>((ref) {
  final asyncStats = ref.watch(aiDashboardStatsProvider);
  return asyncStats.maybeWhen(
    error: (error, _) => error.toString(),
    orElse: () => null,
  );
});

/// Feature usage providers
final aiChatAdvisorCountProvider = Provider<int>((ref) {
  final asyncStats = ref.watch(aiDashboardStatsProvider);
  return asyncStats.maybeWhen(
    data: (stats) => stats.features.chatAdvisor,
    orElse: () => 0,
  );
});

final aiYieldPredictionCountProvider = Provider<int>((ref) {
  final asyncStats = ref.watch(aiDashboardStatsProvider);
  return asyncStats.maybeWhen(
    data: (stats) => stats.features.yieldPrediction,
    orElse: () => 0,
  );
});

final aiPlantHealthCountProvider = Provider<int>((ref) {
  final asyncStats = ref.watch(aiDashboardStatsProvider);
  return asyncStats.maybeWhen(
    data: (stats) => stats.features.plantHealth,
    orElse: () => 0,
  );
});

final aiEnvironmentalInsightsCountProvider = Provider<int>((ref) {
  final asyncStats = ref.watch(aiDashboardStatsProvider);
  return asyncStats.maybeWhen(
    data: (stats) => stats.features.environmentalInsights,
    orElse: () => 0,
  );
});

final aiGrowGuidanceCountProvider = Provider<int>((ref) {
  final asyncStats = ref.watch(aiDashboardStatsProvider);
  return asyncStats.maybeWhen(
    data: (stats) => stats.features.growGuidance,
    orElse: () => 0,
  );
});
