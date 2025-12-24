import 'package:json_annotation/json_annotation.dart';

/// Sensor data model for IoT sensor readings
class SensorData {
  /// Creates SensorData with required and optional fields
  const SensorData({
    this.id,
    required this.deviceId,
    required this.sensorType,
    required this.value,
    required this.unit,
    required this.timestamp,
    this.metadata,
    this.status,
  });

  /// Creates SensorData from JSON
  factory SensorData.fromJson(Map<String, dynamic> json) {
    return SensorData(
      id: json['id'] as String?,
      deviceId: json['device_id'] as String,
      sensorType: json['sensor_type'] as String,
      value: (json['value'] as num).toDouble(),
      unit: json['unit'] as String,
      timestamp: DateTime.parse(json['timestamp'] as String),
      metadata: json['metadata'] as Map<String, dynamic>?,
      status: json['status'] as String?,
    );
  }

  /// Unique sensor reading identifier
  @JsonKey(name: 'id')
  final String? id;

  /// Sensor device identifier
  @JsonKey(name: 'device_id')
  final String deviceId;

  /// Sensor type (temperature, humidity, etc.)
  @JsonKey(name: 'sensor_type')
  final String sensorType;

  /// Sensor reading value
  @JsonKey(name: 'value')
  final double value;

  /// Sensor unit of measurement
  @JsonKey(name: 'unit')
  final String unit;

  /// Timestamp of the reading
  @JsonKey(name: 'timestamp')
  final DateTime timestamp;

  /// Additional sensor metadata
  @JsonKey(name: 'metadata')
  final Map<String, dynamic>? metadata;

  /// Sensor status (online, offline, error)
  @JsonKey(name: 'status')
  final String? status;

  /// Converts SensorData to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'device_id': deviceId,
      'sensor_type': sensorType,
      'value': value,
      'unit': unit,
      'timestamp': timestamp.toIso8601String(),
      'metadata': metadata,
      'status': status,
    };
  }

  /// Creates a copy with optional field overrides
  SensorData copyWith({
    String? id,
    String? deviceId,
    String? sensorType,
    double? value,
    String? unit,
    DateTime? timestamp,
    Map<String, dynamic>? metadata,
    String? status,
  }) {
    return SensorData(
      id: id ?? this.id,
      deviceId: deviceId ?? this.deviceId,
      sensorType: sensorType ?? this.sensorType,
      value: value ?? this.value,
      unit: unit ?? this.unit,
      timestamp: timestamp ?? this.timestamp,
      metadata: metadata ?? this.metadata,
      status: status ?? this.status,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is SensorData &&
        other.id == id &&
        other.deviceId == deviceId &&
        other.sensorType == sensorType &&
        other.value == value &&
        other.unit == unit &&
        other.timestamp == timestamp &&
        other.metadata == metadata &&
        other.status == status;
  }

  @override
  int get hashCode {
    return Object.hash(
      id,
      deviceId,
      sensorType,
      value,
      unit,
      timestamp,
      metadata,
      status,
    );
  }

  @override
  String toString() {
    return 'SensorData(id: $id, deviceId: $deviceId, sensorType: $sensorType, value: $value $unit, timestamp: $timestamp)';
  }

  /// Check if sensor is online
  bool get isOnline => status == 'online' || status == null;

  /// Check if sensor is offline
  bool get isOffline => status == 'offline';

  /// Check if sensor has error
  bool get hasError => status == 'error';

  /// Formatted value with unit
  String get formattedValue => '$value $unit';

  /// Get age of reading
  Duration get age => DateTime.now().difference(timestamp);

  /// Check if reading is recent (within 1 hour)
  bool get isRecent => age < const Duration(hours: 1);

  /// Check if reading is stale (older than 1 day)
  bool get isStale => age > const Duration(days: 1);
}
