/// Flutter models for dashboard statistics and data.
library;
// (removed stray library directive)

class CountStats {
  const CountStats({
    required this.total,
    required this.active,
    required this.harvested,
    required this.seedlings,
    required this.vegetative,
    required this.flowering,
  });

  factory CountStats.fromJson(Map<String, dynamic> json) {
    return CountStats(
      total: (json['total'] as int?) ?? 0,
      active: (json['active'] as int?) ?? 0,
      harvested: (json['harvested'] as int?) ?? 0,
      seedlings: (json['seedlings'] as int?) ?? 0,
      vegetative: (json['vegetative'] as int?) ?? 0,
      flowering: (json['flowering'] as int?) ?? 0,
    );
  }
  final int total;
  final int active;
  final int harvested;
  final int seedlings;
  final int vegetative;
  final int flowering;

  Map<String, dynamic> toJson() {
    return {
      'total': total,
      'active': active,
      'harvested': harvested,
      'seedlings': seedlings,
      'vegetative': vegetative,
      'flowering': flowering,
    };
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is CountStats &&
        other.total == total &&
        other.active == active &&
        other.harvested == harvested &&
        other.seedlings == seedlings &&
        other.vegetative == vegetative &&
        other.flowering == flowering;
  }

  @override
  int get hashCode {
    return Object.hash(
      total,
      active,
      harvested,
      seedlings,
      vegetative,
      flowering,
    );
  }

  @override
  String toString() {
    return 'CountStats{total: $total, active: $active, harvested: $harvested, seedlings: $seedlings, vegetative: $vegetative, flowering: $flowering}';
  }
}

class CultivarStats {
  const CultivarStats({
    required this.totalCultivars,
    required this.userCultivars,
  });

  factory CultivarStats.fromJson(Map<String, dynamic> json) {
    return CultivarStats(
      totalCultivars: (json['total_cultivars'] as int?) ?? 0,
      userCultivars: (json['user_cultivars'] as int?) ?? 0,
    );
  }
  final int totalCultivars;
  final int userCultivars;

  Map<String, dynamic> toJson() {
    return {'total_cultivars': totalCultivars, 'user_cultivars': userCultivars};
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is CultivarStats &&
        other.totalCultivars == totalCultivars &&
        other.userCultivars == userCultivars;
  }

  @override
  int get hashCode {
    return Object.hash(totalCultivars, userCultivars);
  }

  @override
  String toString() {
    return 'CultivarStats{totalCultivars: $totalCultivars, userCultivars: $userCultivars}';
  }
}

class EnvironmentalStats {
  const EnvironmentalStats({
    required this.avgTemperature,
    required this.avgHumidity,
    this.avgPh,
    this.avgEc,
  });

  factory EnvironmentalStats.fromJson(Map<String, dynamic> json) {
    return EnvironmentalStats(
      avgTemperature: ((json['avg_temperature'] as num?) ?? 0.0).toDouble(),
      avgHumidity: ((json['avg_humidity'] as num?) ?? 0.0).toDouble(),
      avgPh: (json['avg_ph'] as num?)?.toDouble(),
      avgEc: (json['avg_ec'] as num?)?.toDouble(),
    );
  }
  final double avgTemperature;
  final double avgHumidity;
  final double? avgPh;
  final double? avgEc;

  Map<String, dynamic> toJson() {
    return {
      'avg_temperature': avgTemperature,
      'avg_humidity': avgHumidity,
      'avg_ph': avgPh,
      'avg_ec': avgEc,
    };
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is EnvironmentalStats &&
        other.avgTemperature == avgTemperature &&
        other.avgHumidity == avgHumidity &&
        other.avgPh == avgPh &&
        other.avgEc == avgEc;
  }

  @override
  int get hashCode {
    return Object.hash(avgTemperature, avgHumidity, avgPh, avgEc);
  }

  @override
  String toString() {
    return 'EnvironmentalStats{avgTemperature: $avgTemperature, avgHumidity: $avgHumidity, avgPh: $avgPh, avgEc: $avgEc}';
  }
}

class SensorStats {
  const SensorStats({
    required this.totalSensors,
    required this.activeSensors,
    this.lastReadingTime,
  });

  factory SensorStats.fromJson(Map<String, dynamic> json) {
    DateTime? lastReading;
    if (json['last_reading_time'] != null) {
      lastReading = DateTime.parse(json['last_reading_time'] as String);
    }
    return SensorStats(
      totalSensors: (json['total_sensors'] as int?) ?? 0,
      activeSensors: (json['active_sensors'] as int?) ?? 0,
      lastReadingTime: lastReading,
    );
  }
  final int totalSensors;
  final int activeSensors;
  final DateTime? lastReadingTime;

  Map<String, dynamic> toJson() {
    return {
      'total_sensors': totalSensors,
      'active_sensors': activeSensors,
      'last_reading_time': lastReadingTime?.toIso8601String(),
    };
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is SensorStats &&
        other.totalSensors == totalSensors &&
        other.activeSensors == activeSensors &&
        other.lastReadingTime == lastReadingTime;
  }

  @override
  int get hashCode {
    return Object.hash(totalSensors, activeSensors, lastReadingTime);
  }

  @override
  String toString() {
    return 'SensorStats{totalSensors: $totalSensors, activeSensors: $activeSensors, lastReadingTime: $lastReadingTime}';
  }
}

class DataSlice {
  const DataSlice({required this.timestamp, required this.value, this.label});

  factory DataSlice.fromJson(Map<String, dynamic> json) {
    return DataSlice(
      timestamp: DateTime.parse(
        (json['timestamp'] as String?) ?? DateTime.now().toIso8601String(),
      ),
      value: ((json['value'] as num?) ?? 0.0).toDouble(),
      label: json['label'] as String?,
    );
  }
  final DateTime timestamp;
  final double value;
  final String? label;

  Map<String, dynamic> toJson() {
    return {
      'timestamp': timestamp.toIso8601String(),
      'value': value,
      'label': label,
    };
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is DataSlice &&
        other.timestamp == timestamp &&
        other.value == value &&
        other.label == label;
  }

  @override
  int get hashCode {
    return Object.hash(timestamp, value, label);
  }

  @override
  String toString() {
    return 'DataSlice{timestamp: $timestamp, value: $value, label: $label}';
  }
}

class EnvironmentalSlice {
  const EnvironmentalSlice({
    this.temperatureData = const [],
    this.humidityData = const [],
    this.phData = const [],
    this.ecData = const [],
  });

  factory EnvironmentalSlice.fromJson(Map<String, dynamic> json) {
    List<DataSlice> parseDataSliceList(dynamic data) {
      if (data is List) {
        return data
            .map((item) => DataSlice.fromJson(item as Map<String, dynamic>))
            .toList();
      }
      return [];
    }

    return EnvironmentalSlice(
      temperatureData: parseDataSliceList(json['temperature_data']),
      humidityData: parseDataSliceList(json['humidity_data']),
      phData: parseDataSliceList(json['ph_data']),
      ecData: parseDataSliceList(json['ec_data']),
    );
  }
  final List<DataSlice> temperatureData;
  final List<DataSlice> humidityData;
  final List<DataSlice> phData;
  final List<DataSlice> ecData;

  Map<String, dynamic> toJson() {
    return {
      'temperature_data': temperatureData.map((e) => e.toJson()).toList(),
      'humidity_data': humidityData.map((e) => e.toJson()).toList(),
      'ph_data': phData.map((e) => e.toJson()).toList(),
      'ec_data': ecData.map((e) => e.toJson()).toList(),
    };
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is EnvironmentalSlice &&
        other.temperatureData == temperatureData &&
        other.humidityData == humidityData &&
        other.phData == phData &&
        other.ecData == ecData;
  }

  @override
  int get hashCode {
    return Object.hash(temperatureData, humidityData, phData, ecData);
  }

  @override
  String toString() {
    return 'EnvironmentalSlice{temperatureData: ${temperatureData.length}, humidityData: ${humidityData.length}, phData: ${phData.length}, ecData: ${ecData.length}}';
  }
}

class GrowthPhaseSlice {
  const GrowthPhaseSlice({
    required this.phase,
    required this.count,
    required this.percentage,
  });

  factory GrowthPhaseSlice.fromJson(Map<String, dynamic> json) {
    return GrowthPhaseSlice(
      phase: (json['phase'] as String?) ?? '',
      count: (json['count'] as int?) ?? 0,
      percentage: ((json['percentage'] as num?) ?? 0.0).toDouble(),
    );
  }
  final String phase;
  final int count;
  final double percentage;

  Map<String, dynamic> toJson() {
    return {'phase': phase, 'count': count, 'percentage': percentage};
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is GrowthPhaseSlice &&
        other.phase == phase &&
        other.count == count &&
        other.percentage == percentage;
  }

  @override
  int get hashCode {
    return Object.hash(phase, count, percentage);
  }

  @override
  String toString() {
    return 'GrowthPhaseSlice{phase: $phase, count: $count, percentage: $percentage}';
  }
}

class RecentReading {
  const RecentReading({
    required this.timestamp,
    required this.sensorType,
    required this.value,
    required this.unit,
    this.location,
  });

  factory RecentReading.fromJson(Map<String, dynamic> json) {
    return RecentReading(
      timestamp: DateTime.parse(
        (json['timestamp'] as String?) ?? DateTime.now().toIso8601String(),
      ),
      sensorType: (json['sensor_type'] as String?) ?? '',
      value: ((json['value'] as num?) ?? 0.0).toDouble(),
      unit: (json['unit'] as String?) ?? '',
      location: (json['location'] as String?),
    );
  }
  final DateTime timestamp;
  final String sensorType;
  final double value;
  final String unit;
  final String? location;

  Map<String, dynamic> toJson() {
    return {
      'timestamp': timestamp.toIso8601String(),
      'sensor_type': sensorType,
      'value': value,
      'unit': unit,
      'location': location,
    };
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is RecentReading &&
        other.timestamp == timestamp &&
        other.sensorType == sensorType &&
        other.value == value &&
        other.unit == unit &&
        other.location == location;
  }

  @override
  int get hashCode {
    return Object.hash(timestamp, sensorType, value, unit, location);
  }

  @override
  String toString() {
    return 'RecentReading{timestamp: $timestamp, sensorType: $sensorType, value: $value, unit: $unit, location: $location}';
  }
}

class RecentActivity {
  const RecentActivity({
    required this.timestamp,
    required this.activityType,
    required this.description,
    this.plantId,
    required this.severity,
  });

  factory RecentActivity.fromJson(Map<String, dynamic> json) {
    return RecentActivity(
      timestamp: DateTime.parse(
        (json['timestamp'] as String?) ?? DateTime.now().toIso8601String(),
      ),
      activityType: (json['activity_type'] as String?) ?? '',
      description: (json['description'] as String?) ?? '',
      plantId: (json['plant_id'] as int?),
      severity: (json['severity'] as String?) ?? 'info',
    );
  }
  final DateTime timestamp;
  final String activityType;
  final String description;
  final int? plantId;
  final String severity;

  Map<String, dynamic> toJson() {
    return {
      'timestamp': timestamp.toIso8601String(),
      'activity_type': activityType,
      'description': description,
      'plant_id': plantId,
      'severity': severity,
    };
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is RecentActivity &&
        other.timestamp == timestamp &&
        other.activityType == activityType &&
        other.description == description &&
        other.plantId == plantId &&
        other.severity == severity;
  }

  @override
  int get hashCode {
    return Object.hash(timestamp, activityType, description, plantId, severity);
  }

  @override
  String toString() {
    return 'RecentActivity{timestamp: $timestamp, activityType: $activityType, description: $description, plantId: $plantId, severity: $severity}';
  }
}

class DashboardStats {
  const DashboardStats({
    required this.counts,
    required this.cultivars,
    required this.environment,
    required this.sensors,
    required this.dataSlices,
    this.growthPhases = const [],
    this.recentReadings = const [],
    this.recentActivities = const [],
    required this.generatedAt,
    required this.userId,
  });

  factory DashboardStats.fromJson(Map<String, dynamic> json) {
    List<GrowthPhaseSlice> parseGrowthPhaseList(dynamic data) {
      if (data is List) {
        return data
            .map(
              (item) => GrowthPhaseSlice.fromJson(item as Map<String, dynamic>),
            )
            .toList();
      }
      return [];
    }

    List<RecentReading> parseRecentReadingList(dynamic data) {
      if (data is List) {
        return data
            .map((item) => RecentReading.fromJson(item as Map<String, dynamic>))
            .toList();
      }
      return [];
    }

    List<RecentActivity> parseRecentActivityList(dynamic data) {
      if (data is List) {
        return data
            .map(
              (item) => RecentActivity.fromJson(item as Map<String, dynamic>),
            )
            .toList();
      }
      return [];
    }

    return DashboardStats(
      counts: CountStats.fromJson(
        json['counts'] as Map<String, dynamic>? ?? {},
      ),
      cultivars: CultivarStats.fromJson(
        json['cultivars'] as Map<String, dynamic>? ?? {},
      ),
      environment: EnvironmentalStats.fromJson(
        json['environment'] as Map<String, dynamic>? ?? {},
      ),
      sensors: SensorStats.fromJson(
        json['sensors'] as Map<String, dynamic>? ?? {},
      ),
      dataSlices: EnvironmentalSlice.fromJson(
        json['data_slices'] as Map<String, dynamic>? ?? {},
      ),
      growthPhases: parseGrowthPhaseList(json['growth_phases']),
      recentReadings: parseRecentReadingList(json['recent_readings']),
      recentActivities: parseRecentActivityList(json['recent_activities']),
      generatedAt: DateTime.parse(
        (json['generated_at'] as String?) ?? DateTime.now().toIso8601String(),
      ),
      userId: (json['user_id'] as int?) ?? 0,
    );
  }
  final CountStats counts;
  final CultivarStats cultivars;
  final EnvironmentalStats environment;
  final SensorStats sensors;
  final EnvironmentalSlice dataSlices;
  final List<GrowthPhaseSlice> growthPhases;
  final List<RecentReading> recentReadings;
  final List<RecentActivity> recentActivities;
  final DateTime generatedAt;
  final int userId;

  Map<String, dynamic> toJson() {
    return {
      'counts': counts.toJson(),
      'cultivars': cultivars.toJson(),
      'environment': environment.toJson(),
      'sensors': sensors.toJson(),
      'data_slices': dataSlices.toJson(),
      'growth_phases': growthPhases.map((e) => e.toJson()).toList(),
      'recent_readings': recentReadings.map((e) => e.toJson()).toList(),
      'recent_activities': recentActivities.map((e) => e.toJson()).toList(),
      'generated_at': generatedAt.toIso8601String(),
      'user_id': userId,
    };
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is DashboardStats &&
        other.counts == counts &&
        other.cultivars == cultivars &&
        other.environment == environment &&
        other.sensors == sensors &&
        other.dataSlices == dataSlices &&
        other.growthPhases == growthPhases &&
        other.recentReadings == recentReadings &&
        other.recentActivities == recentActivities &&
        other.generatedAt == generatedAt &&
        other.userId == userId;
  }

  @override
  int get hashCode {
    return Object.hash(
      counts,
      cultivars,
      environment,
      sensors,
      dataSlices,
      growthPhases,
      recentReadings,
      recentActivities,
      generatedAt,
      userId,
    );
  }

  @override
  String toString() {
    return 'DashboardStats{userId: $userId, counts: $counts, cultivars: $cultivars, environment: $environment, sensors: $sensors}';
  }
}
