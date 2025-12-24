import 'package:freezed_annotation/freezed_annotation.dart';

part 'dashboard_stats_model.freezed.dart';

/// Plant count statistics
@freezed
abstract class CountStats with _$CountStats {
  const factory CountStats({
    @JsonKey(name: 'total') required int total,
    required int active,
    required int harvested,
    required int seedlings,
    required int vegetative,
    required int flowering,
  }) = _CountStats;

  factory CountStats.fromJson(Map<String, dynamic> json) {
    return CountStats(
      total: json['total'] as int,
      active: json['active'] as int,
      harvested: json['harvested'] as int,
      seedlings: json['seedlings'] as int,
      vegetative: json['vegetative'] as int,
      flowering: json['flowering'] as int,
    );
  }
}

/// Cultivar statistics
@freezed
abstract class CultivarStats with _$CultivarStats {
  const factory CultivarStats({
    @JsonKey(name: 'total_cultivars') required int totalCultivars,
    @JsonKey(name: 'user_cultivars') required int userCultivars,
  }) = _CultivarStats;

  factory CultivarStats.fromJson(Map<String, dynamic> json) {
    return CultivarStats(
      totalCultivars: json['total_cultivars'] as int,
      userCultivars: json['user_cultivars'] as int,
    );
  }
}

/// Environmental data statistics
@freezed
abstract class EnvironmentalStats with _$EnvironmentalStats {
  const factory EnvironmentalStats({
    @JsonKey(name: 'avg_temperature') required double avgTemperature,
    @JsonKey(name: 'avg_humidity') required double avgHumidity,
    @JsonKey(name: 'avg_ph') double? avgPh,
    @JsonKey(name: 'avg_ec') double? avgEc,
  }) = _EnvironmentalStats;

  factory EnvironmentalStats.fromJson(Map<String, dynamic> json) {
    return EnvironmentalStats(
      avgTemperature: (json['avg_temperature'] as num).toDouble(),
      avgHumidity: (json['avg_humidity'] as num).toDouble(),
      avgPh: json['avg_ph'] != null ? (json['avg_ph'] as num).toDouble() : null,
      avgEc: json['avg_ec'] != null ? (json['avg_ec'] as num).toDouble() : null,
    );
  }
}

/// Sensor statistics
@freezed
abstract class SensorStats with _$SensorStats {
  const factory SensorStats({
    @JsonKey(name: 'total_sensors') required int totalSensors,
    @JsonKey(name: 'active_sensors') required int activeSensors,
    @JsonKey(name: 'last_reading_time') DateTime? lastReadingTime,
  }) = _SensorStats;

  factory SensorStats.fromJson(Map<String, dynamic> json) {
    return SensorStats(
      totalSensors: json['total_sensors'] as int,
      activeSensors: json['active_sensors'] as int,
      lastReadingTime: json['last_reading_time'] != null
          ? DateTime.parse(json['last_reading_time'] as String)
          : null,
    );
  }
}

/// Data slice for chart visualization
@freezed
abstract class DataSlice with _$DataSlice {
  const factory DataSlice({
    required DateTime timestamp,
    required double value,
    String? label,
  }) = _DataSlice;

  factory DataSlice.fromJson(Map<String, dynamic> json) {
    return DataSlice(
      timestamp: DateTime.parse(json['timestamp'] as String),
      value: (json['value'] as num).toDouble(),
      label: json['label'] as String?,
    );
  }
}

/// Environmental data slice for charts
@freezed
abstract class EnvironmentalSlice with _$EnvironmentalSlice {
  const factory EnvironmentalSlice({
    @JsonKey(name: 'temperature_data')
    @Default([])
    List<DataSlice> temperatureData,
    @JsonKey(name: 'humidity_data') @Default([]) List<DataSlice> humidityData,
    @JsonKey(name: 'ph_data') @Default([]) List<DataSlice> phData,
    @JsonKey(name: 'ec_data') @Default([]) List<DataSlice> ecData,
  }) = _EnvironmentalSlice;

  factory EnvironmentalSlice.fromJson(Map<String, dynamic> json) {
    return EnvironmentalSlice(
      temperatureData:
          (json['temperature_data'] as List<dynamic>?)
              ?.map((e) => DataSlice.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      humidityData:
          (json['humidity_data'] as List<dynamic>?)
              ?.map((e) => DataSlice.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      phData:
          (json['ph_data'] as List<dynamic>?)
              ?.map((e) => DataSlice.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      ecData:
          (json['ec_data'] as List<dynamic>?)
              ?.map((e) => DataSlice.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
    );
  }
}

/// Growth phase distribution data
@freezed
abstract class GrowthPhaseSlice with _$GrowthPhaseSlice {
  const factory GrowthPhaseSlice({
    required String name,
    required int count,
    required double percentage,
  }) = _GrowthPhaseSlice;

  factory GrowthPhaseSlice.fromJson(Map<String, dynamic> json) {
    return GrowthPhaseSlice(
      name: json['name'] as String,
      count: json['count'] as int,
      percentage: (json['percentage'] as num).toDouble(),
    );
  }
}

/// Recent sensor readings
@freezed
abstract class RecentReading with _$RecentReading {
  const factory RecentReading({
    required DateTime timestamp,
    @JsonKey(name: 'sensor_type') required String sensorType,
    required double value,
    required String unit,
    String? location,
  }) = _RecentReading;

  factory RecentReading.fromJson(Map<String, dynamic> json) {
    return RecentReading(
      timestamp: DateTime.parse(json['timestamp'] as String),
      sensorType: json['sensor_type'] as String,
      value: (json['value'] as num).toDouble(),
      unit: json['unit'] as String,
      location: json['location'] as String?,
    );
  }
}

/// Recent dashboard activities
@freezed
abstract class RecentActivity with _$RecentActivity {
  const factory RecentActivity({
    required DateTime timestamp,
    @JsonKey(name: 'activity_type') required String activityType,
    required String description,
    @JsonKey(name: 'plant_id') int? plantId,
    required String severity,
  }) = _RecentActivity;

  factory RecentActivity.fromJson(Map<String, dynamic> json) {
    return RecentActivity(
      timestamp: DateTime.parse(json['timestamp'] as String),
      activityType: json['activity_type'] as String,
      description: json['description'] as String,
      plantId: json['plant_id'] as int?,
      severity: json['severity'] as String,
    );
  }
}

/// Complete dashboard statistics response
@freezed
abstract class DashboardStats with _$DashboardStats {
  const factory DashboardStats({
    required CountStats counts,
    required CultivarStats cultivars,
    required EnvironmentalStats environment,
    required SensorStats sensors,
    @JsonKey(name: 'data_slices') required EnvironmentalSlice dataSlices,
    @JsonKey(name: 'growth_phases')
    @Default([])
    List<GrowthPhaseSlice> growthPhases,
    @JsonKey(name: 'recent_readings')
    @Default([])
    List<RecentReading> recentReadings,
    @JsonKey(name: 'recent_activities')
    @Default([])
    List<RecentActivity> recentActivities,
    @JsonKey(name: 'generated_at') required DateTime generatedAt,
    @JsonKey(name: 'user_id') required int userId,
  }) = _DashboardStats;

  factory DashboardStats.fromJson(Map<String, dynamic> json) {
    return DashboardStats(
      counts: CountStats.fromJson(json['counts'] as Map<String, dynamic>),
      cultivars: CultivarStats.fromJson(
        json['cultivars'] as Map<String, dynamic>,
      ),
      environment: EnvironmentalStats.fromJson(
        json['environment'] as Map<String, dynamic>,
      ),
      sensors: SensorStats.fromJson(json['sensors'] as Map<String, dynamic>),
      dataSlices: EnvironmentalSlice.fromJson(
        json['data_slices'] as Map<String, dynamic>,
      ),
      growthPhases:
          (json['growth_phases'] as List<dynamic>?)
              ?.map((e) => GrowthPhaseSlice.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      recentReadings:
          (json['recent_readings'] as List<dynamic>?)
              ?.map((e) => RecentReading.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      recentActivities:
          (json['recent_activities'] as List<dynamic>?)
              ?.map((e) => RecentActivity.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      generatedAt: DateTime.parse(json['generated_at'] as String),
      userId: json['user_id'] as int,
    );
  }
}

// Backwards compatibility getters for legacy code expecting old property names
extension DashboardStatsLegacyGetters on DashboardStats {
  int get totalPlants => counts.total;
  int get activePlants => counts.active;
  int get totalStrains => cultivars.totalCultivars;
  int get harvested => counts.harvested;
}

/// Legacy models for backward compatibility
@freezed
abstract class Activity with _$Activity {
  const factory Activity({
    required int id,
    required String description,
    @JsonKey(name: 'created_at') required DateTime createdAt,
  }) = _Activity;

  factory Activity.fromJson(Map<String, dynamic> json) {
    return Activity(
      id: json['id'] as int,
      description: json['description'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }
}

@freezed
abstract class Task with _$Task {
  const factory Task({
    required int id,
    required String title,
    @JsonKey(name: 'due_date') required DateTime dueDate,
  }) = _Task;

  factory Task.fromJson(Map<String, dynamic> json) {
    return Task(
      id: json['id'] as int,
      title: json['title'] as String,
      dueDate: DateTime.parse(json['due_date'] as String),
    );
  }
}
