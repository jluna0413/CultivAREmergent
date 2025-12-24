import 'package:freezed_annotation/freezed_annotation.dart';

part 'ai_dashboard_stats.freezed.dart';
// part 'ai_dashboard_stats.g.dart'; // Temporarily commented out

/// AI Activity item for recent activity list
@freezed
abstract class AIActivity with _$AIActivity {
  const factory AIActivity({
    required DateTime timestamp,
    @JsonKey(name: 'activity_type') required String activityType,
    required String description,
    String? feature,
    String? result,
  }) = _AIActivity;

  factory AIActivity.fromJson(Map<String, dynamic> json) {
    return AIActivity(
      timestamp: DateTime.parse(json['timestamp'] as String),
      activityType: json['activity_type'] as String,
      description: json['description'] as String,
      feature: json['feature'] as String?,
      result: json['result'] as String?,
    );
  }
}

/// AI Usage Statistics
@freezed
abstract class AIUsageStats with _$AIUsageStats {
  const factory AIUsageStats({
    @JsonKey(name: 'total_queries') required int totalQueries,
    @JsonKey(name: 'this_month') required int thisMonth,
    @JsonKey(name: 'this_week') required int thisWeek,
    @JsonKey(name: 'today') required int today,
    @JsonKey(name: 'most_used_feature') required String mostUsedFeature,
    @JsonKey(name: 'avg_response_time') required double avgResponseTime,
  }) = _AIUsageStats;

  factory AIUsageStats.fromJson(Map<String, dynamic> json) {
    return AIUsageStats(
      totalQueries: json['total_queries'] as int,
      thisMonth: json['this_month'] as int,
      thisWeek: json['this_week'] as int,
      today: json['today'] as int,
      mostUsedFeature: json['most_used_feature'] as String,
      avgResponseTime: (json['avg_response_time'] as num).toDouble(),
    );
  }
}

/// AI Feature Statistics
@freezed
abstract class AIFeatureStats with _$AIFeatureStats {
  const factory AIFeatureStats({
    @JsonKey(name: 'chat_advisor') required int chatAdvisor,
    @JsonKey(name: 'yield_prediction') required int yieldPrediction,
    @JsonKey(name: 'plant_health') required int plantHealth,
    @JsonKey(name: 'environmental_insights') required int environmentalInsights,
    @JsonKey(name: 'grow_guidance') required int growGuidance,
  }) = _AIFeatureStats;

  factory AIFeatureStats.fromJson(Map<String, dynamic> json) {
    return AIFeatureStats(
      chatAdvisor: json['chat_advisor'] as int,
      yieldPrediction: json['yield_prediction'] as int,
      plantHealth: json['plant_health'] as int,
      environmentalInsights: json['environmental_insights'] as int,
      growGuidance: json['grow_guidance'] as int,
    );
  }
}

/// Complete AI Dashboard Statistics Response
@freezed
abstract class AIDashboardStats with _$AIDashboardStats {
  const factory AIDashboardStats({
    required AIUsageStats usage,
    required AIFeatureStats features,
    @JsonKey(name: 'recent_activities')
    @Default([])
    List<AIActivity> recentActivities,
    @JsonKey(name: 'generated_at') required DateTime generatedAt,
    @JsonKey(name: 'user_id') required int userId,
  }) = _AIDashboardStats;

  factory AIDashboardStats.fromJson(Map<String, dynamic> json) {
    return AIDashboardStats(
      usage: AIUsageStats.fromJson(json['usage'] as Map<String, dynamic>),
      features: AIFeatureStats.fromJson(
        json['features'] as Map<String, dynamic>,
      ),
      recentActivities:
          (json['recent_activities'] as List<dynamic>?)
              ?.map((e) => AIActivity.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      generatedAt: DateTime.parse(json['generated_at'] as String),
      userId: json['user_id'] as int,
    );
  }
}

// Backwards compatibility getters
extension AIDashboardStatsLegacyGetters on AIDashboardStats {
  int get totalAIQueries => usage.totalQueries;
  int get todayAIQueries => usage.today;
  String get topFeature => usage.mostUsedFeature;
  List<AIActivity> get recentActivity => recentActivities;
}
