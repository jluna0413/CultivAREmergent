// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'plant.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$PlantImpl _$$PlantImplFromJson(Map<String, dynamic> json) => _$PlantImpl(
  id: json['id'] as String,
  name: json['name'] as String,
  stage: $enumDecode(_$PlantStageEnumMap, json['stage']),
  status: $enumDecode(_$PlantStatusEnumMap, json['status']),
  health: $enumDecode(_$PlantHealthEnumMap, json['health']),
  plantedDate: DateTime.parse(json['plantedDate'] as String),
  harvestDate: json['harvestDate'] == null
      ? null
      : DateTime.parse(json['harvestDate'] as String),
  strain: json['strain'] as String?,
  notes: json['notes'] as String?,
  metrics: json['metrics'] as Map<String, dynamic>?,
);

Map<String, dynamic> _$$PlantImplToJson(_$PlantImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'stage': _$PlantStageEnumMap[instance.stage]!,
      'status': _$PlantStatusEnumMap[instance.status]!,
      'health': _$PlantHealthEnumMap[instance.health]!,
      'plantedDate': instance.plantedDate.toIso8601String(),
      'harvestDate': instance.harvestDate?.toIso8601String(),
      'strain': instance.strain,
      'notes': instance.notes,
      'metrics': instance.metrics,
    };

const _$PlantStageEnumMap = {
  PlantStage.seedling: 'seedling',
  PlantStage.vegetative: 'vegetative',
  PlantStage.flowering: 'flowering',
  PlantStage.harvest: 'harvest',
  PlantStage.dried: 'dried',
  PlantStage.cured: 'cured',
};

const _$PlantStatusEnumMap = {
  PlantStatus.active: 'active',
  PlantStatus.inactive: 'inactive',
  PlantStatus.harvested: 'harvested',
  PlantStatus.destroyed: 'destroyed',
};

const _$PlantHealthEnumMap = {
  PlantHealth.healthy: 'healthy',
  PlantHealth.stressed: 'stressed',
  PlantHealth.diseased: 'diseased',
  PlantHealth.dead: 'dead',
};
