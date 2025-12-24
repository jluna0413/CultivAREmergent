/// Flutter models for sensor management matching OpenAPI schemas
library;
// (removed stray library directive)

// Enums for better type safety
enum SensorStatus { online, offline, calibrating, error, maintenance }

enum SensorHealth { good, warning, alert, lowBattery, offline }

class Sensor {
  const Sensor({
    required this.id,
    required this.name,
    required this.description,
    required this.type,
    required this.model,
    required this.location,
    required this.zone,
    required this.status,
    required this.apiEndpoint,
    required this.apiKey,
    required this.unit,
    required this.minThreshold,
    required this.maxThreshold,
    required this.isActive,
    required this.lastReading,
    required this.value,
    required this.health,
    required this.firmware,
    required this.createdAt,
    required this.updatedAt,
    this.readings,
    this.recentReadings,
    this.source,
    this.device,
  });

  factory Sensor.fromJson(Map<String, dynamic> json) {
    String statusStr = (json['status'] as String?) ?? 'offline';
    SensorStatus status;
    switch (statusStr.toLowerCase()) {
      case 'online':
        status = SensorStatus.online;
        break;
      case 'offline':
        status = SensorStatus.offline;
        break;
      case 'calibrating':
        status = SensorStatus.calibrating;
        break;
      case 'error':
        status = SensorStatus.error;
        break;
      case 'maintenance':
        status = SensorStatus.maintenance;
        break;
      default:
        status = SensorStatus.offline;
    }

    String healthStr = (json['health'] as String?) ?? 'good';
    SensorHealth health;
    switch (healthStr.toLowerCase()) {
      case 'good':
        health = SensorHealth.good;
        break;
      case 'warning':
        health = SensorHealth.warning;
        break;
      case 'alert':
        health = SensorHealth.alert;
        break;
      case 'lowbattery':
      case 'low_battery':
        health = SensorHealth.lowBattery;
        break;
      case 'offline':
        health = SensorHealth.offline;
        break;
      default:
        health = SensorHealth.good;
    }

    return Sensor(
      id: (json['id'] as int?) ?? 0,
      name: (json['name'] as String?) ?? '',
      description: json['description'] as String?,
      type: (json['type'] as String?) ?? '',
      model: (json['model'] as String?) ?? '',
      location: json['location'] as String?,
      zone: json['zone'] as String?,
      status: status,
      apiEndpoint: json['api_endpoint'] as String?,
      apiKey: json['api_key'] as String?,
      unit: json['unit'] as String?,
      minThreshold:
          ((json['min_threshold'] as num?) ?? json['min_value'] as num?)
              ?.toDouble(),
      maxThreshold:
          ((json['max_threshold'] as num?) ?? json['max_value'] as num?)
              ?.toDouble(),
      isActive: (json['is_active'] as bool?) ?? true,
      lastReading: json['last_reading'] != null
          ? DateTime.parse(json['last_reading'] as String)
          : null,
      value: ((json['value'] as num?) ?? json['last_value'] as num?)
          ?.toDouble(),
      health: health,
      firmware: (json['firmware'] as String?) ?? '1.0.0',
      createdAt: DateTime.parse(
        (json['created_at'] as String?) ?? DateTime.now().toIso8601String(),
      ),
      updatedAt: DateTime.parse(
        (json['updated_at'] as String?) ?? DateTime.now().toIso8601String(),
      ),
      readings: json['readings'] != null && json['readings'] is List
          ? (json['readings'] as List)
                .map<SensorReading>(
                  (reading) =>
                      SensorReading.fromJson(reading as Map<String, dynamic>),
                )
                .toList()
          : null,
      recentReadings:
          json['recent_readings'] != null && json['recent_readings'] is List
          ? (json['recent_readings'] as List)
                .map<SensorReading>(
                  (reading) =>
                      SensorReading.fromJson(reading as Map<String, dynamic>),
                )
                .toList()
          : null,
      source: json['source'] as String?,
      device: json['device_id'] as String?,
    );
  }
  final int id;
  final String name;
  final String? description;
  final String type;
  final String model;
  final String? location;
  final String? zone;
  final SensorStatus status;
  final String? apiEndpoint;
  final String? apiKey;
  final String? unit;
  final double? minThreshold;
  final double? maxThreshold;
  final bool isActive;
  final DateTime? lastReading;
  final double? value; // Current sensor value
  final SensorHealth health;
  final String firmware;
  final DateTime createdAt;
  final DateTime updatedAt;
  final List<SensorReading>? readings;
  final List<SensorReading>? recentReadings;
  final String? source;
  final String? device;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'type': type,
      'model': model,
      'location': location,
      'zone': zone,
      'status': _statusToString(status),
      'api_endpoint': apiEndpoint,
      'api_key': apiKey,
      'unit': unit,
      'min_threshold': minThreshold,
      'max_threshold': maxThreshold,
      'is_active': isActive,
      'last_reading': lastReading?.toIso8601String(),
      'value': value,
      'health': _healthToString(health),
      'firmware': firmware,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
      'readings': readings?.map((reading) => reading.toJson()).toList(),
      'recent_readings': recentReadings
          ?.map((reading) => reading.toJson())
          .toList(),
      'source': source,
      'device_id': device,
    };
  }

  String _statusToString(SensorStatus status) {
    switch (status) {
      case SensorStatus.online:
        return 'online';
      case SensorStatus.offline:
        return 'offline';
      case SensorStatus.calibrating:
        return 'calibrating';
      case SensorStatus.error:
        return 'error';
      case SensorStatus.maintenance:
        return 'maintenance';
    }
  }

  String _healthToString(SensorHealth health) {
    switch (health) {
      case SensorHealth.good:
        return 'good';
      case SensorHealth.warning:
        return 'warning';
      case SensorHealth.alert:
        return 'alert';
      case SensorHealth.lowBattery:
        return 'low_battery';
      case SensorHealth.offline:
        return 'offline';
    }
  }

  Sensor copyWith({
    int? id,
    String? name,
    String? description,
    String? type,
    String? model,
    String? location,
    String? zone,
    SensorStatus? status,
    String? apiEndpoint,
    String? apiKey,
    String? unit,
    double? minThreshold,
    double? maxThreshold,
    bool? isActive,
    DateTime? lastReading,
    double? value,
    SensorHealth? health,
    String? firmware,
    DateTime? createdAt,
    DateTime? updatedAt,
    List<SensorReading>? readings,
    List<SensorReading>? recentReadings,
    String? source,
    String? device,
  }) {
    return Sensor(
      id: id ?? this.id,
      name: name ?? this.name,
      description: description ?? this.description,
      type: type ?? this.type,
      model: model ?? this.model,
      location: location ?? this.location,
      zone: zone ?? this.zone,
      status: status ?? this.status,
      apiEndpoint: apiEndpoint ?? this.apiEndpoint,
      apiKey: apiKey ?? this.apiKey,
      unit: unit ?? this.unit,
      minThreshold: minThreshold ?? this.minThreshold,
      maxThreshold: maxThreshold ?? this.maxThreshold,
      isActive: isActive ?? this.isActive,
      lastReading: lastReading ?? this.lastReading,
      value: value ?? this.value,
      health: health ?? this.health,
      firmware: firmware ?? this.firmware,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      readings: readings ?? this.readings,
      recentReadings: recentReadings ?? this.recentReadings,
      source: source ?? this.source,
      device: device ?? this.device,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is Sensor &&
        other.id == id &&
        other.name == name &&
        other.description == description &&
        other.type == type &&
        other.model == model &&
        other.location == location &&
        other.zone == zone &&
        other.status == status &&
        other.apiEndpoint == apiEndpoint &&
        other.apiKey == apiKey &&
        other.unit == unit &&
        other.minThreshold == minThreshold &&
        other.maxThreshold == maxThreshold &&
        other.isActive == isActive &&
        other.lastReading == lastReading &&
        other.value == value &&
        other.health == health &&
        other.firmware == firmware &&
        other.createdAt == createdAt &&
        other.updatedAt == updatedAt &&
        other.source == source &&
        other.device == device;
  }

  @override
  int get hashCode {
    return Object.hashAll([
      id,
      name,
      description,
      type,
      model,
      location,
      zone,
      status,
      apiEndpoint,
      apiKey,
      unit,
      minThreshold,
      maxThreshold,
      isActive,
      lastReading,
      value,
      health,
      firmware,
      createdAt,
      updatedAt,
      source,
      device,
    ]);
  }

  @override
  String toString() {
    return 'Sensor{id: $id, name: $name, type: $type, model: $model, status: $status, value: $value}';
  }
}

class SensorCreate {
  const SensorCreate({
    required this.name,
    this.description,
    required this.type,
    required this.model,
    this.location,
    this.zone,
    this.apiEndpoint,
    this.apiKey,
    this.unit,
    this.minValue,
    this.maxValue,
  });

  factory SensorCreate.fromJson(Map<String, dynamic> json) {
    return SensorCreate(
      name: (json['name'] as String?) ?? '',
      description: json['description'] as String?,
      type: (json['type'] as String?) ?? '',
      model: (json['model'] as String?) ?? '',
      location: json['location'] as String?,
      zone: json['zone'] as String?,
      apiEndpoint: json['api_endpoint'] as String?,
      apiKey: json['api_key'] as String?,
      unit: json['unit'] as String?,
      minValue: (json['min_value'] as num?)?.toDouble(),
      maxValue: (json['max_value'] as num?)?.toDouble(),
    );
  }
  final String name;
  final String? description;
  final String type;
  final String model;
  final String? location;
  final String? zone;
  final String? apiEndpoint;
  final String? apiKey;
  final String? unit;
  final double? minValue;
  final double? maxValue;

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'description': description,
      'type': type,
      'model': model,
      'location': location,
      'zone': zone,
      'api_endpoint': apiEndpoint,
      'api_key': apiKey,
      'unit': unit,
      'min_value': minValue,
      'max_value': maxValue,
    };
  }
}

class SensorUpdate {
  const SensorUpdate({
    this.name,
    this.description,
    this.type,
    this.model,
    this.location,
    this.zone,
    this.status,
    this.apiEndpoint,
    this.apiKey,
    this.unit,
    this.minValue,
    this.maxValue,
    this.isActive,
  });

  factory SensorUpdate.fromJson(Map<String, dynamic> json) {
    return SensorUpdate(
      name: json['name'] as String?,
      description: json['description'] as String?,
      type: json['type'] as String?,
      model: json['model'] as String?,
      location: json['location'] as String?,
      zone: json['zone'] as String?,
      status: json['status'] as String?,
      apiEndpoint: json['api_endpoint'] as String?,
      apiKey: json['api_key'] as String?,
      unit: json['unit'] as String?,
      minValue: (json['min_value'] as num?)?.toDouble(),
      maxValue: (json['max_value'] as num?)?.toDouble(),
      isActive: json['is_active'] as bool?,
    );
  }
  final String? name;
  final String? description;
  final String? type;
  final String? model;
  final String? location;
  final String? zone;
  final String? status;
  final String? apiEndpoint;
  final String? apiKey;
  final String? unit;
  final double? minValue;
  final double? maxValue;
  final bool? isActive;

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'description': description,
      'type': type,
      'model': model,
      'location': location,
      'zone': zone,
      'status': status,
      'api_endpoint': apiEndpoint,
      'api_key': apiKey,
      'unit': unit,
      'min_value': minValue,
      'max_value': maxValue,
      'is_active': isActive,
    };
  }
}

class SensorReading {
  const SensorReading({
    required this.id,
    required this.sensorId,
    required this.value,
    required this.unit,
    required this.timestamp,
    required this.source,
    this.metadata,
  });

  factory SensorReading.fromJson(Map<String, dynamic> json) {
    return SensorReading(
      id: (json['id'] as int?) ?? 0,
      sensorId: (json['sensor_id'] as int?) ?? 0,
      value: ((json['value'] as num?) ?? 0).toDouble(),
      unit: (json['unit'] as String?) ?? '',
      timestamp: DateTime.parse(
        (json['timestamp'] as String?) ?? DateTime.now().toIso8601String(),
      ),
      source: json['source'] as String?,
      metadata: json['metadata'] is Map<String, dynamic>
          ? json['metadata'] as Map<String, dynamic>
          : null,
    );
  }
  final int id;
  final int sensorId;
  final double value;
  final String unit;
  final DateTime timestamp;
  final String? source;
  final Map<String, dynamic>? metadata;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'sensor_id': sensorId,
      'value': value,
      'unit': unit,
      'timestamp': timestamp.toIso8601String(),
      'source': source,
      'metadata': metadata,
    };
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is SensorReading &&
        other.id == id &&
        other.sensorId == sensorId &&
        other.value == value &&
        other.unit == unit &&
        other.timestamp == timestamp &&
        other.source == source &&
        other.metadata == metadata;
  }

  @override
  int get hashCode {
    return Object.hash(id, sensorId, value, unit, timestamp, source, metadata);
  }

  @override
  String toString() {
    return 'SensorReading{id: $id, sensorId: $sensorId, value: $value $unit, timestamp: $timestamp}';
  }
}

class SensorListResponse {
  const SensorListResponse({
    required this.items,
    required this.total,
    required this.page,
    required this.pageSize,
    required this.hasNext,
    required this.hasPrev,
  });

  factory SensorListResponse.fromJson(Map<String, dynamic> json) {
    List<Sensor> items = [];
    if (json['items'] != null && json['items'] is List) {
      items = (json['items'] as List)
          .map<Sensor>((item) => Sensor.fromJson(item as Map<String, dynamic>))
          .toList();
    }

    return SensorListResponse(
      items: items,
      total: (json['total'] as int?) ?? 0,
      page: (json['page'] as int?) ?? 1,
      pageSize: (json['page_size'] as int?) ?? 20,
      hasNext: (json['has_next'] as bool?) ?? false,
      hasPrev: (json['has_prev'] as bool?) ?? false,
    );
  }
  final List<Sensor> items;
  final int total;
  final int page;
  final int pageSize;
  final bool hasNext;
  final bool hasPrev;

  Map<String, dynamic> toJson() {
    return {
      'items': items.map((item) => item.toJson()).toList(),
      'total': total,
      'page': page,
      'page_size': pageSize,
      'has_next': hasNext,
      'has_prev': hasPrev,
    };
  }
}

class ReadingsListResponse {
  const ReadingsListResponse({
    required this.items,
    required this.total,
    required this.page,
    required this.pageSize,
    required this.hasNext,
    required this.hasPrev,
  });

  factory ReadingsListResponse.fromJson(Map<String, dynamic> json) {
    List<SensorReading> items = [];
    if (json['items'] != null && json['items'] is List) {
      items = (json['items'] as List)
          .map<SensorReading>(
            (item) => SensorReading.fromJson(item as Map<String, dynamic>),
          )
          .toList();
    }

    return ReadingsListResponse(
      items: items,
      total: (json['total'] as int?) ?? 0,
      page: (json['page'] as int?) ?? 1,
      pageSize: (json['page_size'] as int?) ?? 20,
      hasNext: (json['has_next'] as bool?) ?? false,
      hasPrev: (json['has_prev'] as bool?) ?? false,
    );
  }
  final List<SensorReading> items;
  final int total;
  final int page;
  final int pageSize;
  final bool hasNext;
  final bool hasPrev;

  Map<String, dynamic> toJson() {
    return {
      'items': items.map((item) => item.toJson()).toList(),
      'total': total,
      'page': page,
      'page_size': pageSize,
      'has_next': hasNext,
      'has_prev': hasPrev,
    };
  }
}
