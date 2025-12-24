// (removed stray library directive)

class Zone {
  const Zone({
    required this.id,
    required this.name,
    this.description,
    this.temperature,
    this.humidity,
    this.ph,
    this.ec,
    this.lighting,
    this.area,
    this.environmentType,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Zone.fromJson(Map<String, dynamic> json) {
    return Zone(
      id: json['id'] as String,
      name: json['name'] as String,
      description: json['description'] as String?,
      temperature: (json['temperature'] as num?)?.toDouble(),
      humidity: (json['humidity'] as num?)?.toDouble(),
      ph: (json['ph'] as num?)?.toDouble(),
      ec: (json['ec'] as num?)?.toDouble(),
      lighting: json['lighting'] as String?,
      area: (json['area'] as num?)?.toDouble(),
      environmentType: json['environment_type'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }
  final String id;
  final String name;
  final String? description;
  final double? temperature;
  final double? humidity;
  final double? ph;
  final double? ec;
  final String? lighting;
  final double? area;
  final String? environmentType;
  final DateTime createdAt;
  final DateTime updatedAt;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'temperature': temperature,
      'humidity': humidity,
      'ph': ph,
      'ec': ec,
      'lighting': lighting,
      'area': area,
      'environment_type': environmentType,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }

  Zone copyWith({
    String? id,
    String? name,
    String? description,
    double? temperature,
    double? humidity,
    double? ph,
    double? ec,
    String? lighting,
    double? area,
    String? environmentType,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return Zone(
      id: id ?? this.id,
      name: name ?? this.name,
      description: description ?? this.description,
      temperature: temperature ?? this.temperature,
      humidity: humidity ?? this.humidity,
      ph: ph ?? this.ph,
      ec: ec ?? this.ec,
      lighting: lighting ?? this.lighting,
      area: area ?? this.area,
      environmentType: environmentType ?? this.environmentType,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  // Get environment status based on current readings
  EnvironmentStatus get status {
    if (temperature == null || humidity == null) {
      return EnvironmentStatus.unknown;
    }

    // Simple status calculation based on optimal ranges
    final temp = temperature!;
    final hum = humidity!;

    if ((temp >= 20 && temp <= 28) && (hum >= 50 && hum <= 70)) {
      return EnvironmentStatus.optimal;
    } else if ((temp >= 18 && temp <= 32) && (hum >= 40 && hum <= 80)) {
      return EnvironmentStatus.good;
    } else {
      return EnvironmentStatus.needsAttention;
    }
  }

  // Format temperature display
  String get temperatureDisplay {
    if (temperature == null) return 'N/A';
    return '${temperature!.toStringAsFixed(1)}°C';
  }

  // Format humidity display
  String get humidityDisplay {
    if (humidity == null) return 'N/A';
    return '${humidity!.toStringAsFixed(0)}%';
  }
}

enum EnvironmentStatus {
  unknown('Unknown'),
  optimal('Optimal'),
  good('Good'),
  needsAttention('Needs Attention');

  const EnvironmentStatus(this.displayName);
  final String displayName;
}
