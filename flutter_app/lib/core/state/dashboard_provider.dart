import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'dart:async';

// AGENT_SIGNATURE: (Agent Type: IDE, Name: Kilo-Code, Action: Fix)

/// Dashboard data model
class DashboardStats {
  const DashboardStats({
    this.totalPlants = 0,
    this.activePlants = 0,
    this.completedHarvests = 0,
    this.pendingTasks = 0,
    this.avgGrowthRate = 0.0,
    this.lastUpdate = '',
  });

  factory DashboardStats.fromJson(Map<String, dynamic> json) {
    return DashboardStats(
      totalPlants: json['totalPlants'] as int? ?? 0,
      activePlants: json['activePlants'] as int? ?? 0,
      completedHarvests: json['completedHarvests'] as int? ?? 0,
      pendingTasks: json['pendingTasks'] as int? ?? 0,
      avgGrowthRate: (json['avgGrowthRate'] as num?)?.toDouble() ?? 0.0,
      lastUpdate:
          json['lastUpdate'] as String? ?? DateTime.now().toIso8601String(),
    );
  }
  final int totalPlants;
  final int activePlants;
  final int completedHarvests;
  final int pendingTasks;
  final double avgGrowthRate;
  final String lastUpdate;

  Map<String, dynamic> toJson() {
    return {
      'totalPlants': totalPlants,
      'activePlants': activePlants,
      'completedHarvests': completedHarvests,
      'pendingTasks': pendingTasks,
      'avgGrowthRate': avgGrowthRate,
      'lastUpdate': lastUpdate,
    };
  }
}

/// Dashboard provider
final dashboardProvider = FutureProvider<DashboardStats>((ref) async {
  // TODO: Replace with actual API call
  await Future.delayed(const Duration(seconds: 1));

  return DashboardStats(
    totalPlants: 47,
    activePlants: 32,
    completedHarvests: 15,
    pendingTasks: 8,
    avgGrowthRate: 78.5,
    lastUpdate: DateTime.now().toIso8601String(),
  );
});

final dashboardNotifierProvider = dashboardProvider;
final dashboardStatsProvider = dashboardProvider;
