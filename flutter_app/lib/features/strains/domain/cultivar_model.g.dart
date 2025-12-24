// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'cultivar_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$CultivarImpl _$$CultivarImplFromJson(Map<String, dynamic> json) =>
    _$CultivarImpl(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      breederId: (json['breederId'] as num?)?.toInt(),
      indica: (json['indica'] as num?)?.toInt() ?? 0,
      sativa: (json['sativa'] as num?)?.toInt() ?? 0,
      autoflower: json['autoflower'] as bool? ?? false,
      description: json['description'] as String?,
      seedCount: (json['seedCount'] as num?)?.toInt() ?? 0,
      cycleTime: (json['cycleTime'] as num?)?.toInt(),
      url: json['url'] as String?,
      parent1: json['parent1'] as String?,
      parent2: json['parent2'] as String?,
      lineageJson: json['lineageJson'] as Map<String, dynamic>?,
      seedfinderId: json['seedfinderId'] as String?,
      thcContent: (json['thcContent'] as num?)?.toDouble(),
      cbdContent: (json['cbdContent'] as num?)?.toDouble(),
      floweringType: json['floweringType'] as String?,
      breeder: json['breeder'] == null
          ? null
          : Breeder.fromJson(json['breeder'] as Map<String, dynamic>),
      createdAt: json['createdAt'] == null
          ? null
          : DateTime.parse(json['createdAt'] as String),
      updatedAt: json['updatedAt'] == null
          ? null
          : DateTime.parse(json['updatedAt'] as String),
    );

Map<String, dynamic> _$$CultivarImplToJson(_$CultivarImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'breederId': instance.breederId,
      'indica': instance.indica,
      'sativa': instance.sativa,
      'autoflower': instance.autoflower,
      'description': instance.description,
      'seedCount': instance.seedCount,
      'cycleTime': instance.cycleTime,
      'url': instance.url,
      'parent1': instance.parent1,
      'parent2': instance.parent2,
      'lineageJson': instance.lineageJson,
      'seedfinderId': instance.seedfinderId,
      'thcContent': instance.thcContent,
      'cbdContent': instance.cbdContent,
      'floweringType': instance.floweringType,
      'breeder': instance.breeder,
      'createdAt': instance.createdAt?.toIso8601String(),
      'updatedAt': instance.updatedAt?.toIso8601String(),
    };

_$BreederImpl _$$BreederImplFromJson(Map<String, dynamic> json) =>
    _$BreederImpl(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      country: json['country'] as String?,
      website: json['website'] as String?,
      seedfinderId: json['seedfinderId'] as String?,
      description: json['description'] as String?,
      cultivars: (json['cultivars'] as List<dynamic>?)
          ?.map((e) => Cultivar.fromJson(e as Map<String, dynamic>))
          .toList(),
      createdAt: json['createdAt'] == null
          ? null
          : DateTime.parse(json['createdAt'] as String),
      updatedAt: json['updatedAt'] == null
          ? null
          : DateTime.parse(json['updatedAt'] as String),
    );

Map<String, dynamic> _$$BreederImplToJson(_$BreederImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'country': instance.country,
      'website': instance.website,
      'seedfinderId': instance.seedfinderId,
      'description': instance.description,
      'cultivars': instance.cultivars,
      'createdAt': instance.createdAt?.toIso8601String(),
      'updatedAt': instance.updatedAt?.toIso8601String(),
    };

_$CultivarCreateImpl _$$CultivarCreateImplFromJson(Map<String, dynamic> json) =>
    _$CultivarCreateImpl(
      name: json['name'] as String,
      breederId: (json['breederId'] as num?)?.toInt(),
      indica: (json['indica'] as num?)?.toInt() ?? 0,
      sativa: (json['sativa'] as num?)?.toInt() ?? 0,
      autoflower: json['autoflower'] as bool? ?? false,
      description: json['description'] as String?,
      seedCount: (json['seedCount'] as num?)?.toInt() ?? 0,
      cycleTime: (json['cycleTime'] as num?)?.toInt(),
      url: json['url'] as String?,
      parent1: json['parent1'] as String?,
      parent2: json['parent2'] as String?,
      lineageJson: json['lineageJson'] as Map<String, dynamic>?,
      seedfinderId: json['seedfinderId'] as String?,
      thcContent: (json['thcContent'] as num?)?.toDouble(),
      cbdContent: (json['cbdContent'] as num?)?.toDouble(),
      floweringType: json['floweringType'] as String?,
    );

Map<String, dynamic> _$$CultivarCreateImplToJson(
  _$CultivarCreateImpl instance,
) => <String, dynamic>{
  'name': instance.name,
  'breederId': instance.breederId,
  'indica': instance.indica,
  'sativa': instance.sativa,
  'autoflower': instance.autoflower,
  'description': instance.description,
  'seedCount': instance.seedCount,
  'cycleTime': instance.cycleTime,
  'url': instance.url,
  'parent1': instance.parent1,
  'parent2': instance.parent2,
  'lineageJson': instance.lineageJson,
  'seedfinderId': instance.seedfinderId,
  'thcContent': instance.thcContent,
  'cbdContent': instance.cbdContent,
  'floweringType': instance.floweringType,
};

_$CultivarUpdateImpl _$$CultivarUpdateImplFromJson(Map<String, dynamic> json) =>
    _$CultivarUpdateImpl(
      name: json['name'] as String?,
      breederId: (json['breederId'] as num?)?.toInt(),
      indica: (json['indica'] as num?)?.toInt(),
      sativa: (json['sativa'] as num?)?.toInt(),
      autoflower: json['autoflower'] as bool?,
      description: json['description'] as String?,
      seedCount: (json['seedCount'] as num?)?.toInt(),
      cycleTime: (json['cycleTime'] as num?)?.toInt(),
      url: json['url'] as String?,
      parent1: json['parent1'] as String?,
      parent2: json['parent2'] as String?,
      lineageJson: json['lineageJson'] as Map<String, dynamic>?,
      seedfinderId: json['seedfinderId'] as String?,
      thcContent: (json['thcContent'] as num?)?.toDouble(),
      cbdContent: (json['cbdContent'] as num?)?.toDouble(),
      floweringType: json['floweringType'] as String?,
    );

Map<String, dynamic> _$$CultivarUpdateImplToJson(
  _$CultivarUpdateImpl instance,
) => <String, dynamic>{
  'name': instance.name,
  'breederId': instance.breederId,
  'indica': instance.indica,
  'sativa': instance.sativa,
  'autoflower': instance.autoflower,
  'description': instance.description,
  'seedCount': instance.seedCount,
  'cycleTime': instance.cycleTime,
  'url': instance.url,
  'parent1': instance.parent1,
  'parent2': instance.parent2,
  'lineageJson': instance.lineageJson,
  'seedfinderId': instance.seedfinderId,
  'thcContent': instance.thcContent,
  'cbdContent': instance.cbdContent,
  'floweringType': instance.floweringType,
};

_$StrainsParamsImpl _$$StrainsParamsImplFromJson(Map<String, dynamic> json) =>
    _$StrainsParamsImpl(
      page: (json['page'] as num?)?.toInt() ?? 1,
      limit: (json['limit'] as num?)?.toInt() ?? 20,
      search: json['search'] as String?,
      breederId: (json['breederId'] as num?)?.toInt(),
      autoflower: json['autoflower'] as bool?,
      sortBy: json['sortBy'] as String?,
      sortOrder: json['sortOrder'] as String? ?? 'asc',
    );

Map<String, dynamic> _$$StrainsParamsImplToJson(_$StrainsParamsImpl instance) =>
    <String, dynamic>{
      'page': instance.page,
      'limit': instance.limit,
      'search': instance.search,
      'breederId': instance.breederId,
      'autoflower': instance.autoflower,
      'sortBy': instance.sortBy,
      'sortOrder': instance.sortOrder,
    };

_$PaginatedStrainsResponseImpl _$$PaginatedStrainsResponseImplFromJson(
  Map<String, dynamic> json,
) => _$PaginatedStrainsResponseImpl(
  data: (json['data'] as List<dynamic>)
      .map((e) => Cultivar.fromJson(e as Map<String, dynamic>))
      .toList(),
  total: (json['total'] as num).toInt(),
  page: (json['page'] as num).toInt(),
  limit: (json['limit'] as num).toInt(),
  pages: (json['pages'] as num).toInt(),
  hasNext: json['hasNext'] as bool? ?? false,
  hasPrev: json['hasPrev'] as bool? ?? false,
);

Map<String, dynamic> _$$PaginatedStrainsResponseImplToJson(
  _$PaginatedStrainsResponseImpl instance,
) => <String, dynamic>{
  'data': instance.data,
  'total': instance.total,
  'page': instance.page,
  'limit': instance.limit,
  'pages': instance.pages,
  'hasNext': instance.hasNext,
  'hasPrev': instance.hasPrev,
};

_$CultivarStatsImpl _$$CultivarStatsImplFromJson(Map<String, dynamic> json) =>
    _$CultivarStatsImpl(
      totalCultivars: (json['totalCultivars'] as num).toInt(),
      indicaCount: (json['indicaCount'] as num).toInt(),
      sativaCount: (json['sativaCount'] as num).toInt(),
      hybridCount: (json['hybridCount'] as num).toInt(),
      autoflowerCount: (json['autoflowerCount'] as num).toInt(),
      averageCycleTime: (json['averageCycleTime'] as num?)?.toDouble(),
    );

Map<String, dynamic> _$$CultivarStatsImplToJson(_$CultivarStatsImpl instance) =>
    <String, dynamic>{
      'totalCultivars': instance.totalCultivars,
      'indicaCount': instance.indicaCount,
      'sativaCount': instance.sativaCount,
      'hybridCount': instance.hybridCount,
      'autoflowerCount': instance.autoflowerCount,
      'averageCycleTime': instance.averageCycleTime,
    };
