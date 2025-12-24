import 'package:freezed_annotation/freezed_annotation.dart';

part 'dashboard_stats_model.freezed.dart';
part 'dashboard_stats_model.g.dart';

/// Plant count statistics
@freezed
abstract class CountStats with _$CountStats {
  @JsonSerializable(explicitToJson: true)
  const factory CountStats({
    required int total,
    required int active,
    required int harvested,
    required int seedlings,
    required int vegetative,
    required int flowering,
  }) = _CountStats;

  factory CountStats.fromJson(Map<String, dynamic> json) =>
      _$CountStatsFromJson(json);
}

/// Cultivar statistics
@freezed
abstract class CultivarStats with _$CultivarStats {
  @JsonSerializable(explicitToJson: true)
  const factory CultivarStats({
    @JsonKey(name: 'total_cultivars') required int totalCultivars,
    @JsonKey(name: 'user_cultivars') required int userCultivars,
  }) = _CultivarStats;

  factory CultivarStats.fromJson(Map<String, dynamic> json) =>
      _$CultivarStatsFromJson(json);
}

/// Environmental data statistics
@freezed
abstract class EnvironmentalStats with _$EnvironmentalStats {
  @JsonSerializable(explicitToJson: true)
  const factory EnvironmentalStats({
    @JsonKey(name: 'avg_temperature') required double avgTemperature,
    @JsonKey(name: 'avg_humidity') required double avgHumidity,
    @JsonKey(name: 'avg_ph') double? avgPh,
    @JsonKey(name: 'avg_ec') double? avgEc,
  }) = _EnvironmentalStats;

  factory EnvironmentalStats.fromJson(Map<String, dynamic> json) =>
      _$EnvironmentalStatsFromJson(json);
}

/// Sensor statistics
@freezed
abstract class SensorStats with _$SensorStats {
  @JsonSerializable(explicitToJson: true)
  const factory SensorStats({
    @JsonKey(name: 'total_sensors') required int totalSensors,
    @JsonKey(name: 'active_sensors') required int activeSensors,
    @JsonKey(name: 'last_reading_time') DateTime? lastReadingTime,
  }) = _SensorStats;

  factory SensorStats.fromJson(Map<String, dynamic> json) =>
      _$SensorStatsFromJson(json);
}

/// Data slice for chart visualization
@freezed
abstract class DataSlice with _$DataSlice {
  @JsonSerializable(explicitToJson: true)
  const factory DataSlice({
    required DateTime timestamp,
    required double value,
    String? label,
  }) = _DataSlice;

  factory DataSlice.fromJson(Map<String, dynamic> json) =>
      _$DataSliceFromJson(json);
}

/// Environmental data slice for charts
@freezed
abstract class EnvironmentalSlice with _$EnvironmentalSlice {
  @JsonSerializable(explicitToJson: true)
  const factory EnvironmentalSlice({
    @JsonKey(name: 'temperature_data')
    @Default([])
    List<DataSlice> temperatureData,
    @JsonKey(name: 'humidity_data') @Default([]) List<DataSlice> humidityData,
    @JsonKey(name: 'ph_data') @Default([]) List<DataSlice> phData,
    @JsonKey(name: 'ec_data') @Default([]) List<DataSlice> ecData,
  }) = _EnvironmentalSlice;

  factory EnvironmentalSlice.fromJson(Map<String, dynamic> json) =>
      _$EnvironmentalSliceFromJson(json);
}

/// Growth phase distribution data
@freezed
abstract class GrowthPhaseSlice with _$GrowthPhaseSlice {
  @JsonSerializable(explicitToJson: true)
  const factory GrowthPhaseSlice({
    required String phase,
    required int count,
    required double percentage,
  }) = _GrowthPhaseSlice;

  factory GrowthPhaseSlice.fromJson(Map<String, dynamic> json) =>
      _$GrowthPhaseSliceFromJson(json);
}

/// Recent sensor readings
@freezed
abstract class RecentReading with _$RecentReading {
  @JsonSerializable(explicitToJson: true)
  const factory RecentReading({
    required DateTime timestamp,
    @JsonKey(name: 'sensor_type') required String sensorType,
    required double value,
    required String unit,
    String? location,
  }) = _RecentReading;

  factory RecentReading.fromJson(Map<String, dynamic> json) =>
      _$RecentReadingFromJson(json);
}

/// Recent dashboard activities
@freezed
abstract class RecentActivity with _$RecentActivity {
  @JsonSerializable(explicitToJson: true)
  const factory RecentActivity({
    required DateTime timestamp,
    @JsonKey(name: 'activity_type') required String activityType,
    required String description,
    @JsonKey(name: 'plant_id') int? plantId,
    required String severity,
  }) = _RecentActivity;

  factory RecentActivity.fromJson(Map<String, dynamic> json) =>
      _$RecentActivityFromJson(json);
}

/// Complete dashboard statistics response
@freezed
abstract class DashboardStats with _$DashboardStats {
  @JsonSerializable(explicitToJson: true)
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

  factory DashboardStats.fromJson(Map<String, dynamic> json) =>
      _$DashboardStatsFromJson(json);
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

  factory Activity.fromJson(Map<String, dynamic> json) =>
      _$ActivityFromJson(json);
}

@freezed
abstract class Task with _$Task {
  const factory Task({
    required int id,
    required String title,
    @JsonKey(name: 'due_date') required DateTime dueDate,
  }) = _Task;

  factory Task.fromJson(Map<String, dynamic> json) => _$TaskFromJson(json);
}
