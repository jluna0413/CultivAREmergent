// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'plant_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$PlantImpl _$$PlantImplFromJson(Map<String, dynamic> json) => _$PlantImpl(
  id: (json['id'] as num).toInt(),
  userId: (json['user_id'] as num).toInt(),
  name: json['name'] as String,
  description: json['description'] as String?,
  statusId: (json['status_id'] as num).toInt(),
  cultivarId: (json['cultivar_id'] as num?)?.toInt(),
  zoneId: (json['zone_id'] as num?)?.toInt(),
  currentDay: (json['current_day'] as num?)?.toInt() ?? 0,
  currentWeek: (json['current_week'] as num?)?.toInt() ?? 0,
  currentHeight: json['current_height'] as String?,
  heightDate: json['height_date'] == null
      ? null
      : DateTime.parse(json['height_date'] as String),
  lastWaterDate: json['last_water_date'] == null
      ? null
      : DateTime.parse(json['last_water_date'] as String),
  lastFeedDate: json['last_feed_date'] == null
      ? null
      : DateTime.parse(json['last_feed_date'] as String),
  isClone: json['is_clone'] as bool? ?? false,
  startDt: json['start_dt'] == null
      ? null
      : DateTime.parse(json['start_dt'] as String),
  harvestWeight: (json['harvest_weight'] as num?)?.toDouble(),
  harvestDate: json['harvest_date'] == null
      ? null
      : DateTime.parse(json['harvest_date'] as String),
  cycleTime: (json['cycle_time'] as num?)?.toInt(),
  strainUrl: json['strain_url'] as String?,
  estHarvestDate: json['est_harvest_date'] == null
      ? null
      : DateTime.parse(json['est_harvest_date'] as String),
  autoflower: json['autoflower'] as bool? ?? false,
  parentId: (json['parent_id'] as num?)?.toInt(),
  imageUrl: json['image_url'] as String?,
  createdAt: json['created_at'] == null
      ? null
      : DateTime.parse(json['created_at'] as String),
  updatedAt: json['updated_at'] == null
      ? null
      : DateTime.parse(json['updated_at'] as String),
  statusName: json['status_name'] as String?,
  strainName: json['strain_name'] as String?,
  cultivarName: json['cultivar_name'] as String?,
  breederName: json['breeder_name'] as String?,
  zoneName: json['zone_name'] as String?,
  parentName: json['parent_name'] as String?,
  ageDays: (json['age_days'] as num?)?.toInt(),
);

Map<String, dynamic> _$$PlantImplToJson(_$PlantImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'name': instance.name,
      'description': instance.description,
      'status_id': instance.statusId,
      'cultivar_id': instance.cultivarId,
      'zone_id': instance.zoneId,
      'current_day': instance.currentDay,
      'current_week': instance.currentWeek,
      'current_height': instance.currentHeight,
      'height_date': instance.heightDate?.toIso8601String(),
      'last_water_date': instance.lastWaterDate?.toIso8601String(),
      'last_feed_date': instance.lastFeedDate?.toIso8601String(),
      'is_clone': instance.isClone,
      'start_dt': instance.startDt?.toIso8601String(),
      'harvest_weight': instance.harvestWeight,
      'harvest_date': instance.harvestDate?.toIso8601String(),
      'cycle_time': instance.cycleTime,
      'strain_url': instance.strainUrl,
      'est_harvest_date': instance.estHarvestDate?.toIso8601String(),
      'autoflower': instance.autoflower,
      'parent_id': instance.parentId,
      'image_url': instance.imageUrl,
      'created_at': instance.createdAt?.toIso8601String(),
      'updated_at': instance.updatedAt?.toIso8601String(),
      'status_name': instance.statusName,
      'strain_name': instance.strainName,
      'cultivar_name': instance.cultivarName,
      'breeder_name': instance.breederName,
      'zone_name': instance.zoneName,
      'parent_name': instance.parentName,
      'age_days': instance.ageDays,
    };

_$PlantCreateImpl _$$PlantCreateImplFromJson(Map<String, dynamic> json) =>
    _$PlantCreateImpl(
      name: json['name'] as String,
      description: json['description'] as String?,
      statusId: (json['status_id'] as num?)?.toInt() ?? 1,
      cultivarId: (json['cultivar_id'] as num?)?.toInt(),
      zoneId: (json['zone_id'] as num?)?.toInt(),
      isClone: json['is_clone'] as bool? ?? false,
      autoflower: json['autoflower'] as bool? ?? false,
      parentId: (json['parent_id'] as num?)?.toInt(),
      imageUrl: json['image_url'] as String?,
    );

Map<String, dynamic> _$$PlantCreateImplToJson(_$PlantCreateImpl instance) =>
    <String, dynamic>{
      'name': instance.name,
      'description': instance.description,
      'status_id': instance.statusId,
      'cultivar_id': instance.cultivarId,
      'zone_id': instance.zoneId,
      'is_clone': instance.isClone,
      'autoflower': instance.autoflower,
      'parent_id': instance.parentId,
      'image_url': instance.imageUrl,
    };

_$PlantUpdateImpl _$$PlantUpdateImplFromJson(Map<String, dynamic> json) =>
    _$PlantUpdateImpl(
      name: json['name'] as String?,
      description: json['description'] as String?,
      statusId: (json['status_id'] as num?)?.toInt(),
      cultivarId: (json['cultivar_id'] as num?)?.toInt(),
      zoneId: (json['zone_id'] as num?)?.toInt(),
      currentHeight: json['current_height'] as String?,
      lastWaterDate: json['last_water_date'] == null
          ? null
          : DateTime.parse(json['last_water_date'] as String),
      lastFeedDate: json['last_feed_date'] == null
          ? null
          : DateTime.parse(json['last_feed_date'] as String),
      isClone: json['is_clone'] as bool?,
      startDt: json['start_dt'] == null
          ? null
          : DateTime.parse(json['start_dt'] as String),
      harvestWeight: (json['harvest_weight'] as num?)?.toDouble(),
      harvestDate: json['harvest_date'] == null
          ? null
          : DateTime.parse(json['harvest_date'] as String),
      estHarvestDate: json['est_harvest_date'] == null
          ? null
          : DateTime.parse(json['est_harvest_date'] as String),
      autoflower: json['autoflower'] as bool?,
      parentId: (json['parent_id'] as num?)?.toInt(),
      imageUrl: json['image_url'] as String?,
    );

Map<String, dynamic> _$$PlantUpdateImplToJson(_$PlantUpdateImpl instance) =>
    <String, dynamic>{
      'name': instance.name,
      'description': instance.description,
      'status_id': instance.statusId,
      'cultivar_id': instance.cultivarId,
      'zone_id': instance.zoneId,
      'current_height': instance.currentHeight,
      'last_water_date': instance.lastWaterDate?.toIso8601String(),
      'last_feed_date': instance.lastFeedDate?.toIso8601String(),
      'is_clone': instance.isClone,
      'start_dt': instance.startDt?.toIso8601String(),
      'harvest_weight': instance.harvestWeight,
      'harvest_date': instance.harvestDate?.toIso8601String(),
      'est_harvest_date': instance.estHarvestDate?.toIso8601String(),
      'autoflower': instance.autoflower,
      'parent_id': instance.parentId,
      'image_url': instance.imageUrl,
    };

_$PaginatedPlantsResponseImpl _$$PaginatedPlantsResponseImplFromJson(
  Map<String, dynamic> json,
) => _$PaginatedPlantsResponseImpl(
  items:
      (json['items'] as List<dynamic>?)
          ?.map((e) => Plant.fromJson(e as Map<String, dynamic>))
          .toList() ??
      const [],
  total: (json['total'] as num?)?.toInt() ?? 0,
  page: (json['page'] as num?)?.toInt() ?? 1,
  limit: (json['page_size'] as num?)?.toInt() ?? 20,
  pages: (json['pages'] as num?)?.toInt() ?? 0,
  hasNext: json['has_next'] as bool? ?? false,
  hasPrev: json['has_prev'] as bool? ?? false,
);

Map<String, dynamic> _$$PaginatedPlantsResponseImplToJson(
  _$PaginatedPlantsResponseImpl instance,
) => <String, dynamic>{
  'items': instance.items,
  'total': instance.total,
  'page': instance.page,
  'page_size': instance.limit,
  'pages': instance.pages,
  'has_next': instance.hasNext,
  'has_prev': instance.hasPrev,
};
