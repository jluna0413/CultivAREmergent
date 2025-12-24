import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:flutter/material.dart';

part 'plant.freezed.dart';
part 'plant.g.dart';

/// Plant model representing a cannabis plant in the cultivation system
@freezed
abstract class Plant with _$Plant {
  const factory Plant({
    required String id,
    required String name,
    required PlantStage stage,
    required PlantStatus status,
    required PlantHealth health,
    required DateTime plantedDate,
    DateTime? harvestDate,
    String? strain,
    String? notes,
    Map<String, dynamic>? metrics,
  }) = _Plant;

  factory Plant.fromJson(Map<String, dynamic> json) => _$PlantFromJson(json);
}

/// Plant stage enumeration
enum PlantStage { seedling, vegetative, flowering, harvest, dried, cured }

/// Plant status enumeration
enum PlantStatus { active, inactive, harvested, destroyed }

/// Plant health enumeration
enum PlantHealth { healthy, stressed, diseased, dead }

/// Extension methods for PlantStage
extension PlantStageExtension on PlantStage {
  String get displayName {
    switch (this) {
      case PlantStage.seedling:
        return 'Seedling';
      case PlantStage.vegetative:
        return 'Vegetative';
      case PlantStage.flowering:
        return 'Flowering';
      case PlantStage.harvest:
        return 'Harvest';
      case PlantStage.dried:
        return 'Dried';
      case PlantStage.cured:
        return 'Cured';
    }
  }

  int get daysToNext {
    switch (this) {
      case PlantStage.seedling:
        return 14;
      case PlantStage.vegetative:
        return 60;
      case PlantStage.flowering:
        return 63;
      case PlantStage.harvest:
        return 7;
      case PlantStage.dried:
        return 7;
      case PlantStage.cured:
        return 0;
    }
  }
}

/// Extension methods for PlantStatus
extension PlantStatusExtension on PlantStatus {
  String get displayName {
    switch (this) {
      case PlantStatus.active:
        return 'Active';
      case PlantStatus.inactive:
        return 'Inactive';
      case PlantStatus.harvested:
        return 'Harvested';
      case PlantStatus.destroyed:
        return 'Destroyed';
    }
  }

  Color get statusColor {
    switch (this) {
      case PlantStatus.active:
        return Colors.green;
      case PlantStatus.inactive:
        return Colors.orange;
      case PlantStatus.harvested:
        return Colors.blue;
      case PlantStatus.destroyed:
        return Colors.red;
    }
  }
}

/// Extension methods for PlantHealth
extension PlantHealthExtension on PlantHealth {
  String get displayName {
    switch (this) {
      case PlantHealth.healthy:
        return 'Healthy';
      case PlantHealth.stressed:
        return 'Stressed';
      case PlantHealth.diseased:
        return 'Diseased';
      case PlantHealth.dead:
        return 'Dead';
    }
  }

  Color get healthColor {
    switch (this) {
      case PlantHealth.healthy:
        return Colors.green;
      case PlantHealth.stressed:
        return Colors.orange;
      case PlantHealth.diseased:
        return Colors.red;
      case PlantHealth.dead:
        return Colors.grey;
    }
  }
}
