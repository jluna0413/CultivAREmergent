/// Sensors Provider - Manages sensor data and operations
/// Handles sensor CRUD operations, real-time data, and monitoring
library;

import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Sensor data model
class Sensor {
  factory Sensor.fromJson(Map<String, dynamic> json) {
    return Sensor(
      id: json['id'] as String,
      name: json['name'] as String,
      type: SensorType.values.firstWhere(
        (e) => e.name == json['type'],
        orElse: () => SensorType.temperature,
      ),
      value: (json['value'] as num).toDouble(),
      unit: json['unit'] as String,
      status: SensorStatus.values.firstWhere(
        (e) => e.name == json['status'],
        orElse: () => SensorStatus.online,
      ),
      location: json['location'] as String?,
      minThreshold: (json['min_threshold'] as num?)?.toDouble(),
      maxThreshold: (json['max_threshold'] as num?)?.toDouble(),
      lastReading: json['last_reading'] != null
          ? DateTime.parse(json['last_reading'] as String)
          : null,
      batteryLevel: json['battery_level'] as int?,
      signalStrength: json['signal_strength'] as int?,
      firmware: json['firmware'] as String?,
      metadata: json['metadata'] as Map<String, dynamic>?,
    );
  }
  const Sensor({
    required this.id,
    required this.name,
    required this.type,
    required this.value,
    required this.unit,
    required this.status,
    this.location,
    this.minThreshold,
    this.maxThreshold,
    this.lastReading,
    this.batteryLevel,
    this.signalStrength,
    this.firmware,
    this.metadata,
  });

  final String id;
  final String name;
  final SensorType type;
  final double value;
  final String unit;
  final SensorStatus status;
  final String? location;
  final double? minThreshold;
  final double? maxThreshold;
  final DateTime? lastReading;
  final int? batteryLevel;
  final int? signalStrength;
  final String? firmware;
  final Map<String, dynamic>? metadata;

  Sensor copyWith({
    String? id,
    String? name,
    SensorType? type,
    double? value,
    String? unit,
    SensorStatus? status,
    String? location,
    double? minThreshold,
    double? maxThreshold,
    DateTime? lastReading,
    int? batteryLevel,
    int? signalStrength,
    String? firmware,
    Map<String, dynamic>? metadata,
  }) {
    return Sensor(
      id: id ?? this.id,
      name: name ?? this.name,
      type: type ?? this.type,
      value: value ?? this.value,
      unit: unit ?? this.unit,
      status: status ?? this.status,
      location: location ?? this.location,
      minThreshold: minThreshold ?? this.minThreshold,
      maxThreshold: maxThreshold ?? this.maxThreshold,
      lastReading: lastReading ?? this.lastReading,
      batteryLevel: batteryLevel ?? this.batteryLevel,
      signalStrength: signalStrength ?? this.signalStrength,
      firmware: firmware ?? this.firmware,
      metadata: metadata ?? this.metadata,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'type': type.name,
      'value': value,
      'unit': unit,
      'status': status.name,
      'location': location,
      'min_threshold': minThreshold,
      'max_threshold': maxThreshold,
      'last_reading': lastReading?.toIso8601String(),
      'battery_level': batteryLevel,
      'signal_strength': signalStrength,
      'firmware': firmware,
      'metadata': metadata,
    };
  }

  /// Check if sensor value is within threshold range
  bool get isWithinThreshold {
    if (minThreshold == null && maxThreshold == null) return true;
    if (minThreshold != null && value < minThreshold!) return false;
    if (maxThreshold != null && value > maxThreshold!) return false;
    return true;
  }

  /// Get sensor health status based on value and thresholds
  SensorHealth get health {
    if (status != SensorStatus.online) {
      return SensorHealth.offline;
    }
    if (batteryLevel != null && batteryLevel! < 20) {
      return SensorHealth.lowBattery;
    }
    if (signalStrength != null && signalStrength! < 30) {
      return SensorHealth.poorSignal;
    }
    if (!isWithinThreshold) {
      return SensorHealth.alert;
    }
    return SensorHealth.normal;
  }
}

/// Sensor type enum
enum SensorType {
  temperature,
  humidity,
  ph,
  ec,
  light,
  co2,
  pressure,
  waterTemp,
}

/// Sensor status enum
enum SensorStatus { online, offline, error, calibrating }

/// Sensor health enum
enum SensorHealth { normal, offline, lowBattery, poorSignal, alert }

/// Sensors filter options
class SensorFilter {
  const SensorFilter({this.types, this.statuses, this.locations, this.health});

  final List<SensorType>? types;
  final List<SensorStatus>? statuses;
  final List<String>? locations;
  final List<SensorHealth>? health;
}

/// Mock data generator - generates sample sensors
List<Sensor> _generateMockSensors() {
  return [
    Sensor(
      id: '1',
      name: 'Temperature Sensor 1',
      type: SensorType.temperature,
      value: 22.5,
      unit: '°C',
      status: SensorStatus.online,
      location: 'Grow Tent A',
      minThreshold: 18.0,
      maxThreshold: 30.0,
      lastReading: DateTime.now().subtract(const Duration(minutes: 5)),
      batteryLevel: 85,
      signalStrength: 90,
      firmware: 'v1.2.3',
    ),
    Sensor(
      id: '2',
      name: 'Humidity Sensor 1',
      type: SensorType.humidity,
      value: 65.0,
      unit: '%',
      status: SensorStatus.online,
      location: 'Grow Tent A',
      minThreshold: 40.0,
      maxThreshold: 70.0,
      lastReading: DateTime.now().subtract(const Duration(minutes: 3)),
      batteryLevel: 78,
      signalStrength: 85,
      firmware: 'v1.2.1',
    ),
    Sensor(
      id: '3',
      name: 'pH Sensor 1',
      type: SensorType.ph,
      value: 6.2,
      unit: 'pH',
      status: SensorStatus.online,
      location: 'Hydroponic System',
      minThreshold: 5.5,
      maxThreshold: 6.8,
      lastReading: DateTime.now().subtract(const Duration(minutes: 10)),
      batteryLevel: 45,
      signalStrength: 75,
      firmware: 'v2.0.1',
    ),
    Sensor(
      id: '4',
      name: 'EC Sensor 1',
      type: SensorType.ec,
      value: 1200.0,
      unit: 'ppm',
      status: SensorStatus.calibrating,
      location: 'Hydroponic System',
      minThreshold: 800.0,
      maxThreshold: 1600.0,
      lastReading: DateTime.now().subtract(const Duration(minutes: 15)),
      batteryLevel: 32,
      signalStrength: 60,
      firmware: 'v1.5.0',
    ),
    Sensor(
      id: '5',
      name: 'Light Sensor 1',
      type: SensorType.light,
      value: 450.0,
      unit: 'PPFD',
      status: SensorStatus.online,
      location: 'Grow Tent A',
      minThreshold: 300.0,
      maxThreshold: 600.0,
      lastReading: DateTime.now().subtract(const Duration(minutes: 2)),
      batteryLevel: 92,
      signalStrength: 95,
      firmware: 'v1.1.8',
    ),
  ];
}

/// Filters a list of sensors based on filter criteria
List<Sensor> _filterSensors(List<Sensor> sensors, SensorFilter? filter) {
  if (filter == null) return sensors;

  return sensors.where((sensor) {
    // Filter by type
    if (filter.types != null && !filter.types!.contains(sensor.type)) {
      return false;
    }

    // Filter by status
    if (filter.statuses != null && !filter.statuses!.contains(sensor.status)) {
      return false;
    }

    // Filter by location
    if (filter.locations != null &&
        sensor.location != null &&
        !filter.locations!.contains(sensor.location)) {
      return false;
    }

    // Filter by health
    if (filter.health != null && !filter.health!.contains(sensor.health)) {
      return false;
    }

    return true;
  }).toList();
}

/// Main provider for sensors state using simple Provider pattern
final sensorsProvider = Provider<List<Sensor>>((ref) {
  return _generateMockSensors();
});

/// Convenience providers
final allSensorsProvider = Provider<List<Sensor>>((ref) {
  final sensors = ref.watch(sensorsProvider);
  return sensors;
});

final filteredSensorsProvider = Provider<List<Sensor>>((ref) {
  final sensors = ref.watch(sensorsProvider);
  final filter = ref.watch(sensorsFilterProvider);
  return _filterSensors(sensors, filter);
});

final sensorsLoadingProvider = Provider<bool>((ref) {
  return false; // Static data, no loading state
});

final sensorsErrorProvider = Provider<String?>((ref) {
  return null; // Static data, no error state
});

final sensorsFilterProvider = Provider<SensorFilter?>((ref) {
  return null; // No default filter
});

final sensorsCountProvider = Provider<int>((ref) {
  final sensors = ref.watch(sensorsProvider);
  return sensors.length;
});

final filteredSensorsCountProvider = Provider<int>((ref) {
  final filteredSensors = ref.watch(filteredSensorsProvider);
  return filteredSensors.length;
});

final sensorsByTypeProvider = Provider<Map<SensorType, List<Sensor>>>((ref) {
  final sensors = ref.watch(sensorsProvider);
  final Map<SensorType, List<Sensor>> sensorsByType = {};

  for (final sensor in sensors) {
    if (!sensorsByType.containsKey(sensor.type)) {
      sensorsByType[sensor.type] = [];
    }
    sensorsByType[sensor.type]!.add(sensor);
  }

  return sensorsByType;
});

final sensorsByLocationProvider = Provider<Map<String, List<Sensor>>>((ref) {
  final sensors = ref.watch(sensorsProvider);
  final Map<String, List<Sensor>> sensorsByLocation = {};

  for (final sensor in sensors) {
    final location = sensor.location ?? 'Unknown';
    if (!sensorsByLocation.containsKey(location)) {
      sensorsByLocation[location] = [];
    }
    sensorsByLocation[location]!.add(sensor);
  }

  return sensorsByLocation;
});

final sensorsByHealthProvider = Provider<Map<SensorHealth, List<Sensor>>>((
  ref,
) {
  final sensors = ref.watch(sensorsProvider);
  final Map<SensorHealth, List<Sensor>> sensorsByHealth = {};

  for (final sensor in sensors) {
    if (!sensorsByHealth.containsKey(sensor.health)) {
      sensorsByHealth[sensor.health] = [];
    }
    sensorsByHealth[sensor.health]!.add(sensor);
  }

  return sensorsByHealth;
});

final sensorsRealTimeEnabledProvider = Provider<bool>((ref) {
  return true; // Default real-time enabled
});
