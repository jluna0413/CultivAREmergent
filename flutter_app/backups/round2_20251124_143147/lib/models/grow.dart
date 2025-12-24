/// Grow operation models for CultivAR mobile app
/// Defines structure for grow-related data types
library;
// (removed stray library directive)

class Grow {
  const Grow({
    required this.id,
    required this.name,
    this.description,
    this.cultivarId,
    this.strain,
    this.startedAt,
    this.completedAt,
    this.status = GrowStatus.planning,
    this.environment,
    this.targetTemp,
    this.targetHumidity,
    this.targetPh,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Grow.fromJson(Map<String, dynamic> json) {
    return Grow(
      id: json['id'] as String,
      name: json['name'] as String,
      description: json['description'] as String?,
      cultivarId: json['cultivar_id'] as String?,
      strain: json['strain'] as String?,
      startedAt: json['started_at'] != null
          ? DateTime.parse(json['started_at'] as String)
          : null,
      completedAt: json['completed_at'] != null
          ? DateTime.parse(json['completed_at'] as String)
          : null,
      status: GrowStatus.values.firstWhere(
        (s) => s.toString().split('.').last == json['status'],
        orElse: () => GrowStatus.planning,
      ),
      environment: json['environment'] as String?,
      targetTemp: (json['target_temp'] as num?)?.toDouble(),
      targetHumidity: (json['target_humidity'] as num?)?.toDouble(),
      targetPh: (json['target_ph'] as num?)?.toDouble(),
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }
  final String id;
  final String name;
  final String? description;
  final String? cultivarId;
  final String? strain;
  final DateTime? startedAt;
  final DateTime? completedAt;
  final GrowStatus status;
  final String? environment;
  final double? targetTemp;
  final double? targetHumidity;
  final double? targetPh;
  final DateTime createdAt;
  final DateTime updatedAt;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'cultivar_id': cultivarId,
      'strain': strain,
      'started_at': startedAt?.toIso8601String(),
      'completed_at': completedAt?.toIso8601String(),
      'status': status.toString().split('.').last,
      'environment': environment,
      'target_temp': targetTemp,
      'target_humidity': targetHumidity,
      'target_ph': targetPh,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }

  Grow copyWith({
    String? id,
    String? name,
    String? description,
    String? cultivarId,
    String? strain,
    DateTime? startedAt,
    DateTime? completedAt,
    GrowStatus? status,
    String? environment,
    double? targetTemp,
    double? targetHumidity,
    double? targetPh,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return Grow(
      id: id ?? this.id,
      name: name ?? this.name,
      description: description ?? this.description,
      cultivarId: cultivarId ?? this.cultivarId,
      strain: strain ?? this.strain,
      startedAt: startedAt ?? this.startedAt,
      completedAt: completedAt ?? this.completedAt,
      status: status ?? this.status,
      environment: environment ?? this.environment,
      targetTemp: targetTemp ?? this.targetTemp,
      targetHumidity: targetHumidity ?? this.targetHumidity,
      targetPh: targetPh ?? this.targetPh,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  // Calculate current phase based on status and timing
  String get currentPhase {
    switch (status) {
      case GrowStatus.planning:
        return 'Planning Phase';
      case GrowStatus.active:
        return 'Active Growth';
      case GrowStatus.harvesting:
        return 'Harvesting Phase';
      case GrowStatus.completed:
        return 'Completed';
      case GrowStatus.cancelled:
        return 'Cancelled';
    }
  }

  // Calculate days since start
  int get daysSinceStart {
    if (startedAt == null) return 0;
    return DateTime.now().difference(startedAt!).inDays;
  }
}

enum GrowStatus {
  planning('Planning'),
  active('Active'),
  harvesting('Harvesting'),
  completed('Completed'),
  cancelled('Cancelled');

  const GrowStatus(this.displayName);
  final String displayName;
}
