import 'package:freezed_annotation/freezed_annotation.dart';

part 'dashboard_stats_model.freezed.dart';
part 'dashboard_stats_model.g.dart';

@freezed
class DashboardStats with _$DashboardStats {
  const factory DashboardStats({
    required int totalPlants,
    required int activePlants,
    required int clones,
    required int harvested,
    required int totalStrains,
    List<Map<String, dynamic>>? recentActivities,
    List<Map<String, dynamic>>? upcomingTasks,
  }) = _DashboardStats;

  factory DashboardStats.fromJson(Map<String, dynamic> json) => _$DashboardStatsFromJson(json);
}
