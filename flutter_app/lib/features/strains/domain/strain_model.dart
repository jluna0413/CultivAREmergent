// lib/features/strains/domain/strain_model.dart

import 'package:freezed_annotation/freezed_annotation.dart';

part 'strain_model.freezed.dart';
part 'strain_model.g.dart';

@freezed
abstract class Cultivar with _$Cultivar {
  const factory Cultivar({
    required int id,
    required String name,
    String? description,
    String? genetics,
    int? breederId,
    String? breederName,
    int? indica,
    int? sativa,
    int? ruderalis,
    String? floweringType,
    int? floweringDays,
    int? yieldIndoor,
    int? yieldOutdoor,
    String? difficulty,
    String? imageUrl,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) = _Cultivar;

  factory Cultivar.fromJson(Map<String, dynamic> json) =>
      _$CultivarFromJson(json);
}

@freezed
abstract class CultivarCreate with _$CultivarCreate {
  const factory CultivarCreate({
    required String name,
    String? description,
    String? genetics,
    int? breederId,
    int? indica,
    int? sativa,
    int? ruderalis,
    String? floweringType,
    int? floweringDays,
    int? yieldIndoor,
    int? yieldOutdoor,
    String? difficulty,
    String? imageUrl,
  }) = _CultivarCreate;

  factory CultivarCreate.fromJson(Map<String, dynamic> json) =>
      _$CultivarCreateFromJson(json);
}

@freezed
abstract class CultivarUpdate with _$CultivarUpdate {
  const factory CultivarUpdate({
    String? name,
    String? description,
    String? genetics,
    int? breederId,
    int? indica,
    int? sativa,
    int? ruderalis,
    String? floweringType,
    int? floweringDays,
    int? yieldIndoor,
    int? yieldOutdoor,
    String? difficulty,
    String? imageUrl,
  }) = _CultivarUpdate;

  factory CultivarUpdate.fromJson(Map<String, dynamic> json) =>
      _$CultivarUpdateFromJson(json);
}

@freezed
abstract class Breeder with _$Breeder {
  const factory Breeder({
    required int id,
    required String name,
    String? description,
    String? website,
    String? imageUrl,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) = _Breeder;

  factory Breeder.fromJson(Map<String, dynamic> json) =>
      _$BreederFromJson(json);
}

@freezed
abstract class StrainsParams with _$StrainsParams {
  const factory StrainsParams({
    @Default(1) int page,
    @Default(20) int limit,
    String? search,
    String? breeder,
    String? difficulty,
    String? floweringType,
    int? minIndica,
    int? maxIndica,
    int? minFloweringDays,
    int? maxFloweringDays,
  }) = _StrainsParams;

  factory StrainsParams.fromJson(Map<String, dynamic> json) =>
      _$StrainsParamsFromJson(json);

  const StrainsParams._();

  Map<String, dynamic> toQueryParams() {
    final params = <String, dynamic>{};
    if (page != 1) params['page'] = page.toString();
    if (limit != 20) params['limit'] = limit.toString();
    if (search != null && search!.isNotEmpty) params['search'] = search;
    if (breeder != null && breeder!.isNotEmpty) params['breeder'] = breeder;
    if (difficulty != null && difficulty!.isNotEmpty) {
      params['difficulty'] = difficulty;
    }
    if (floweringType != null && floweringType!.isNotEmpty) {
      params['flowering_type'] = floweringType;
    }
    if (minIndica != null) params['min_indica'] = minIndica.toString();
    if (maxIndica != null) params['max_indica'] = maxIndica.toString();
    if (minFloweringDays != null) {
      params['min_flowering_days'] = minFloweringDays.toString();
    }
    if (maxFloweringDays != null) {
      params['max_flowering_days'] = maxFloweringDays.toString();
    }
    return params;
  }

  StrainsParams copyWithNextPage() => copyWith(page: page + 1);

  StrainsParams copyWithPrevPage() => copyWith(page: page > 1 ? page - 1 : 1);
}

@freezed
abstract class PaginatedStrainsResponse with _$PaginatedStrainsResponse {
  const factory PaginatedStrainsResponse({
    required List<Cultivar> data,
    required int total,
    required int page,
    required int limit,
    required int totalPages,
    required bool hasNext,
    required bool hasPrev,
  }) = _PaginatedStrainsResponse;

  factory PaginatedStrainsResponse.fromJson(Map<String, dynamic> json) =>
      _$PaginatedStrainsResponseFromJson(json);

  const PaginatedStrainsResponse._();

  bool get isEmpty => data.isEmpty;
  bool get isNotEmpty => data.isNotEmpty;
}

@freezed
abstract class CultivarStats with _$CultivarStats {
  const factory CultivarStats({
    required int totalCultivars,
    required int totalBreeders,
    required Map<String, int> byDifficulty,
    required Map<String, int> byFloweringType,
    required List<String> popularBreeders,
  }) = _CultivarStats;

  factory CultivarStats.fromJson(Map<String, dynamic> json) =>
      _$CultivarStatsFromJson(json);
}

// Extension methods for computed properties
extension CultivarExtensions on Cultivar {
  String get geneticsDisplay {
    if (genetics != null && genetics!.isNotEmpty) {
      return genetics!;
    }
    if (indica != null && sativa != null && ruderalis != null) {
      return '$indica/$sativa/$ruderalis';
    }
    return 'Unknown';
  }

  String get breederNameDisplay => breederName ?? 'Unknown Breeder';

  bool get hasParents => genetics != null && genetics!.contains('x');
}

extension BreederExtensions on Breeder {
  bool get hasWebsite => website != null && website!.isNotEmpty;
}
