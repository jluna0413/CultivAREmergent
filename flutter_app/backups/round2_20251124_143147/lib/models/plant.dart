/// Plant management models for CultivAR mobile app
// (removed stray library directive)

/// Request model for creating a new plant (imported from core models)
library;

class CreatePlantRequest {
  const CreatePlantRequest({
    required this.name,
    this.cultivarName,
    this.strain,
    this.plantedDate,
    this.location,
    this.notes,
    this.seedBank,
    this.breeder,
  });

  factory CreatePlantRequest.fromJson(Map<String, dynamic> json) {
    return CreatePlantRequest(
      name: json['name'] as String,
      cultivarName: json['cultivar_name'] as String?,
      strain: json['strain'] as String?,
      plantedDate: json['planted_date'] != null
          ? DateTime.parse(json['planted_date'] as String)
          : null,
      location: json['location'] as String?,
      notes: json['notes'] as String?,
      seedBank: json['seed_bank'] as String?,
      breeder: json['breeder'] as String?,
    );
  }
  final String name;
  final String? cultivarName;
  final String? strain;
  final DateTime? plantedDate;
  final String? location;
  final String? notes;
  final String? seedBank;
  final String? breeder;

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'cultivar_name': cultivarName,
      'strain': strain,
      'planted_date': plantedDate?.toIso8601String(),
      'location': location,
      'notes': notes,
      'seed_bank': seedBank,
      'breeder': breeder,
    };
  }
}

/// Plant model representing a plant in the grow operation
class Plant {
  const Plant({
    required this.id,
    required this.name,
    required this.cultivarName,
    required this.strain,
    required this.plantedDate,
    required this.createdAt,
    required this.updatedAt,
    required this.location,
    required this.notes,
    required this.seedBank,
    required this.breeder,
    required this.status,
  });

  factory Plant.fromJson(Map<String, dynamic> json) {
    return Plant(
      id: json['id'] as int,
      name: json['name'] as String,
      cultivarName: json['cultivar_name'] as String?,
      strain: json['strain'] as String?,
      plantedDate: DateTime.parse(json['planted_date'] as String),
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
      location: json['location'] as String?,
      notes: json['notes'] as String?,
      seedBank: json['seed_bank'] as String?,
      breeder: json['breeder'] as String?,
      status: json['status'] as String,
    );
  }
  final int id;
  final String name;
  final String? cultivarName;
  final String? strain; // Deprecated: Use cultivarName instead
  final DateTime plantedDate;
  final DateTime createdAt;
  final DateTime updatedAt;
  final String? location;
  final String? notes;
  final String? seedBank;
  final String? breeder;
  final String status;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'cultivar_name': cultivarName,
      'strain': strain,
      'planted_date': plantedDate.toIso8601String(),
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
      'location': location,
      'notes': notes,
      'seed_bank': seedBank,
      'breeder': breeder,
      'status': status,
    };
  }

  /// Calculate age of plant in days
  int get ageInDays {
    return DateTime.now().difference(plantedDate).inDays;
  }

  /// Get the cultivar display name (prefers cultivarName, falls back to strain for compatibility)
  String get cultivarDisplay {
    return cultivarName ?? strain ?? 'Unknown';
  }

  /// Get readable status
  String get statusDisplay {
    switch (status.toLowerCase()) {
      case 'seedling':
        return '🌱 Seedling';
      case 'vegetative':
        return '🌿 Growing';
      case 'flowering':
        return '🌸 Flowering';
      case 'harvested':
        return '✂️ Harvested';
      case 'dried':
        return '🪣 Dried';
      case 'cured':
        return '🏺 Cured';
      default:
        return status;
    }
  }

  @override
  String toString() {
    return 'Plant{id: $id, name: $name, cultivarName: $cultivarName, status: $status}';
  }
}

/// Note: Cultivar and DashboardStats classes are now imported from core/models
/// to avoid conflicts. Use these imports:
/// import '../core/models/dashboard_stats.dart';
/// import '../core/models/create_plant_request.dart';
