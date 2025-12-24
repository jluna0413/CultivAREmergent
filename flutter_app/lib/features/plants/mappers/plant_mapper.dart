import '../domain/plant_model.dart';
import '../models/plant_ui_model.dart';

// Simple Data Transfer Object for API communication
class PlantDto {
  const PlantDto({
    required this.id,
    required this.name,
    required this.status,
    this.strainName,
    this.startDt,
    this.imageUrl,
  });

  factory PlantDto.fromJson(Map<String, dynamic> json) {
    return PlantDto(
      id: json['id'] as int,
      name: json['name'] as String,
      status: json['status'] as String,
      strainName: json['strain_name'] as String?,
      startDt: json['start_dt'] != null
          ? DateTime.parse(json['start_dt'] as String)
          : null,
      imageUrl: json['image_url'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'status': status,
      'strain_name': strainName,
      'start_dt': startDt?.toIso8601String(),
      'image_url': imageUrl,
    };
  }

  final int id;
  final String name;
  final String status;
  final String? strainName;
  final DateTime? startDt;
  final String? imageUrl;
}

// Mapper functions between domain, DTO, and UI models
int _statusStringToId(String? status) {
  final s = status?.toLowerCase() ?? '';
  switch (s) {
    case 'seed':
    case 'seedling':
      return 1;
    case 'vegetative':
    case 'veg':
      return 2;
    case 'flowering':
    case 'flower':
      return 3;
    case 'harvested':
    case 'harvest':
      return 4;
    case 'active':
      return 5;
    default:
      return 0; // Unknown/unspecified
  }
}

Plant plantFromDto(PlantDto dto) {
  final statusId = _statusStringToId(dto.status);
  return Plant(
    id: dto.id,
    userId: 0, // API dto may not include userId; default to 0 for mapping
    name: dto.name,
    description: null,
    statusId: statusId,
    cultivarId: null,
    zoneId: null,
    currentDay: 0,
    currentWeek: 0,
    currentHeight: null,
    heightDate: null,
    lastWaterDate: null,
    lastFeedDate: null,
    isClone: false,
    startDt: dto.startDt,
    harvestWeight: null,
    harvestDate: null,
    cycleTime: null,
    strainUrl: null,
    estHarvestDate: null,
    autoflower: false,
    parentId: null,
    imageUrl: dto.imageUrl,
    createdAt: DateTime.now(),
    updatedAt: DateTime.now(),
    statusName: dto.status,
    strainName: dto.strainName,
    cultivarName: null,
    breederName: null,
    zoneName: null,
    parentName: null,
    ageDays: null,
  );
}

PlantDto plantToDto(Plant domain) {
  final map = {
    1: 'seedling',
    2: 'vegetative',
    3: 'flowering',
    4: 'harvested',
    5: 'active',
  };
  final statusStr = map[domain.statusId] ?? domain.statusName ?? 'unknown';

  return PlantDto(
    id: domain.id,
    name: domain.name,
    status: statusStr,
    strainName: domain.strainName,
    startDt: domain.startDt,
    imageUrl: domain.imageUrl,
  );
}

// UI model conversion
PlantUiModel plantToUi(Plant domain) {
  return PlantUiModel.fromJson({
    'id': domain.id,
    'name': domain.name,
    'description': domain.description,
    'status': domain.statusName ?? 'unknown',
    'strain_name': domain.strainName,
    'is_clone': domain.isClone,
    'start_dt': domain.startDt?.toIso8601String(),
    'image_url': domain.imageUrl,
  });
}

Plant plantFromUi(PlantUiModel ui) {
  final statusId = _statusStringToId(ui.status.name);
  return Plant(
    id: ui.id ?? 0,
    userId: 0,
    name: ui.name ?? 'Unknown',
    description: ui.description,
    statusId: statusId,
    cultivarId: null,
    zoneId: null,
    currentDay: ui.ageInDays,
    currentWeek: (ui.ageInDays / 7).floor(),
    currentHeight: null,
    heightDate: null,
    lastWaterDate: null,
    lastFeedDate: null,
    isClone: ui.isClone,
    startDt: ui.startDt,
    harvestWeight: null,
    harvestDate: null,
    cycleTime: null,
    strainUrl: null,
    estHarvestDate: null,
    autoflower: false,
    parentId: null,
    imageUrl: ui.imageUrl,
    createdAt: DateTime.now(),
    updatedAt: DateTime.now(),
    statusName: ui.status.name,
    strainName: ui.strainName,
    cultivarName: null,
    breederName: null,
    zoneName: null,
    parentName: null,
    ageDays: ui.ageInDays,
  );
}

// Helper extensions
extension DomainPlantMapper on Plant {
  PlantDto toDto() => plantToDto(this);
  PlantUiModel toUi() => plantToUi(this);
}

extension UiPlantMapper on PlantUiModel {
  Plant toDomain() => plantFromUi(this);
}

extension DtoPlantMapper on PlantDto {
  Plant toDomain() => plantFromDto(this);
}
