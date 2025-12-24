// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'strain_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$CultivarImpl _$$CultivarImplFromJson(Map<String, dynamic> json) =>
    _$CultivarImpl(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      description: json['description'] as String?,
      genetics: json['genetics'] as String?,
      breederId: (json['breederId'] as num?)?.toInt(),
      breederName: json['breederName'] as String?,
      indica: (json['indica'] as num?)?.toInt(),
      sativa: (json['sativa'] as num?)?.toInt(),
      ruderalis: (json['ruderalis'] as num?)?.toInt(),
      floweringType: json['floweringType'] as String?,
      floweringDays: (json['floweringDays'] as num?)?.toInt(),
      yieldIndoor: (json['yieldIndoor'] as num?)?.toInt(),
      yieldOutdoor: (json['yieldOutdoor'] as num?)?.toInt(),
      difficulty: json['difficulty'] as String?,
      imageUrl: json['imageUrl'] as String?,
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
      'description': instance.description,
      'genetics': instance.genetics,
      'breederId': instance.breederId,
      'breederName': instance.breederName,
      'indica': instance.indica,
      'sativa': instance.sativa,
      'ruderalis': instance.ruderalis,
      'floweringType': instance.floweringType,
      'floweringDays': instance.floweringDays,
      'yieldIndoor': instance.yieldIndoor,
      'yieldOutdoor': instance.yieldOutdoor,
      'difficulty': instance.difficulty,
      'imageUrl': instance.imageUrl,
      'createdAt': instance.createdAt?.toIso8601String(),
      'updatedAt': instance.updatedAt?.toIso8601String(),
    };

_$CultivarCreateImpl _$$CultivarCreateImplFromJson(Map<String, dynamic> json) =>
    _$CultivarCreateImpl(
      name: json['name'] as String,
      description: json['description'] as String?,
      genetics: json['genetics'] as String?,
      breederId: (json['breederId'] as num?)?.toInt(),
      indica: (json['indica'] as num?)?.toInt(),
      sativa: (json['sativa'] as num?)?.toInt(),
      ruderalis: (json['ruderalis'] as num?)?.toInt(),
      floweringType: json['floweringType'] as String?,
      floweringDays: (json['floweringDays'] as num?)?.toInt(),
      yieldIndoor: (json['yieldIndoor'] as num?)?.toInt(),
      yieldOutdoor: (json['yieldOutdoor'] as num?)?.toInt(),
      difficulty: json['difficulty'] as String?,
      imageUrl: json['imageUrl'] as String?,
    );

Map<String, dynamic> _$$CultivarCreateImplToJson(
  _$CultivarCreateImpl instance,
) => <String, dynamic>{
  'name': instance.name,
  'description': instance.description,
  'genetics': instance.genetics,
  'breederId': instance.breederId,
  'indica': instance.indica,
  'sativa': instance.sativa,
  'ruderalis': instance.ruderalis,
  'floweringType': instance.floweringType,
  'floweringDays': instance.floweringDays,
  'yieldIndoor': instance.yieldIndoor,
  'yieldOutdoor': instance.yieldOutdoor,
  'difficulty': instance.difficulty,
  'imageUrl': instance.imageUrl,
};

_$CultivarUpdateImpl _$$CultivarUpdateImplFromJson(Map<String, dynamic> json) =>
    _$CultivarUpdateImpl(
      name: json['name'] as String?,
      description: json['description'] as String?,
      genetics: json['genetics'] as String?,
      breederId: (json['breederId'] as num?)?.toInt(),
      indica: (json['indica'] as num?)?.toInt(),
      sativa: (json['sativa'] as num?)?.toInt(),
      ruderalis: (json['ruderalis'] as num?)?.toInt(),
      floweringType: json['floweringType'] as String?,
      floweringDays: (json['floweringDays'] as num?)?.toInt(),
      yieldIndoor: (json['yieldIndoor'] as num?)?.toInt(),
      yieldOutdoor: (json['yieldOutdoor'] as num?)?.toInt(),
      difficulty: json['difficulty'] as String?,
      imageUrl: json['imageUrl'] as String?,
    );

Map<String, dynamic> _$$CultivarUpdateImplToJson(
  _$CultivarUpdateImpl instance,
) => <String, dynamic>{
  'name': instance.name,
  'description': instance.description,
  'genetics': instance.genetics,
  'breederId': instance.breederId,
  'indica': instance.indica,
  'sativa': instance.sativa,
  'ruderalis': instance.ruderalis,
  'floweringType': instance.floweringType,
  'floweringDays': instance.floweringDays,
  'yieldIndoor': instance.yieldIndoor,
  'yieldOutdoor': instance.yieldOutdoor,
  'difficulty': instance.difficulty,
  'imageUrl': instance.imageUrl,
};

_$BreederImpl _$$BreederImplFromJson(Map<String, dynamic> json) =>
    _$BreederImpl(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      description: json['description'] as String?,
      website: json['website'] as String?,
      imageUrl: json['imageUrl'] as String?,
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
      'description': instance.description,
      'website': instance.website,
      'imageUrl': instance.imageUrl,
      'createdAt': instance.createdAt?.toIso8601String(),
      'updatedAt': instance.updatedAt?.toIso8601String(),
    };

_$StrainsParamsImpl _$$StrainsParamsImplFromJson(Map<String, dynamic> json) =>
    _$StrainsParamsImpl(
      page: (json['page'] as num?)?.toInt() ?? 1,
      limit: (json['limit'] as num?)?.toInt() ?? 20,
      search: json['search'] as String?,
      breeder: json['breeder'] as String?,
      difficulty: json['difficulty'] as String?,
      floweringType: json['floweringType'] as String?,
      minIndica: (json['minIndica'] as num?)?.toInt(),
      maxIndica: (json['maxIndica'] as num?)?.toInt(),
      minFloweringDays: (json['minFloweringDays'] as num?)?.toInt(),
      maxFloweringDays: (json['maxFloweringDays'] as num?)?.toInt(),
    );

Map<String, dynamic> _$$StrainsParamsImplToJson(_$StrainsParamsImpl instance) =>
    <String, dynamic>{
      'page': instance.page,
      'limit': instance.limit,
      'search': instance.search,
      'breeder': instance.breeder,
      'difficulty': instance.difficulty,
      'floweringType': instance.floweringType,
      'minIndica': instance.minIndica,
      'maxIndica': instance.maxIndica,
      'minFloweringDays': instance.minFloweringDays,
      'maxFloweringDays': instance.maxFloweringDays,
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
  totalPages: (json['totalPages'] as num).toInt(),
  hasNext: json['hasNext'] as bool,
  hasPrev: json['hasPrev'] as bool,
);

Map<String, dynamic> _$$PaginatedStrainsResponseImplToJson(
  _$PaginatedStrainsResponseImpl instance,
) => <String, dynamic>{
  'data': instance.data,
  'total': instance.total,
  'page': instance.page,
  'limit': instance.limit,
  'totalPages': instance.totalPages,
  'hasNext': instance.hasNext,
  'hasPrev': instance.hasPrev,
};

_$CultivarStatsImpl _$$CultivarStatsImplFromJson(Map<String, dynamic> json) =>
    _$CultivarStatsImpl(
      totalCultivars: (json['totalCultivars'] as num).toInt(),
      totalBreeders: (json['totalBreeders'] as num).toInt(),
      byDifficulty: Map<String, int>.from(json['byDifficulty'] as Map),
      byFloweringType: Map<String, int>.from(json['byFloweringType'] as Map),
      popularBreeders: (json['popularBreeders'] as List<dynamic>)
          .map((e) => e as String)
          .toList(),
    );

Map<String, dynamic> _$$CultivarStatsImplToJson(_$CultivarStatsImpl instance) =>
    <String, dynamic>{
      'totalCultivars': instance.totalCultivars,
      'totalBreeders': instance.totalBreeders,
      'byDifficulty': instance.byDifficulty,
      'byFloweringType': instance.byFloweringType,
      'popularBreeders': instance.popularBreeders,
    };
