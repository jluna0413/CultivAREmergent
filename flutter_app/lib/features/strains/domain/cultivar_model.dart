import 'package:freezed_annotation/freezed_annotation.dart';

part 'cultivar_model.freezed.dart';
part 'cultivar_model.g.dart';

@freezed
abstract class Cultivar with _$Cultivar {
  const factory Cultivar({
    required int id,
    required String name,
    int? breederId,
    @Default(0) int indica,
    @Default(0) int sativa,
    @Default(false) bool autoflower,
    String? description,
    @Default(0) int seedCount,
    int? cycleTime,
    String? url,
    String? parent1,
    String? parent2,
    Map<String, dynamic>? lineageJson,
    String? seedfinderId,
    double? thcContent,
    double? cbdContent,
    String? floweringType,
    Breeder? breeder,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) = _Cultivar;

  factory Cultivar.fromJson(Map<String, dynamic> json) =>
      _$CultivarFromJson(json);

  const Cultivar._();

  String get geneticsDisplay {
    if (indica == 0 && sativa == 0) return 'Unknown';
    return '$indica% Indica / $sativa% Sativa';
  }

  String get breederName => breeder?.name ?? 'Unknown Breeder';

  bool get hasParents => parent1 != null || parent2 != null;
}

@freezed
abstract class Breeder with _$Breeder {
  const factory Breeder({
    required int id,
    required String name,
    String? country,
    String? website,
    String? seedfinderId,
    String? description,
    List<Cultivar>? cultivars,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) = _Breeder;

  factory Breeder.fromJson(Map<String, dynamic> json) =>
      _$BreederFromJson(json);
}

@freezed
abstract class CultivarCreate with _$CultivarCreate {
  const factory CultivarCreate({
    required String name,
    int? breederId,
    @Default(0) int indica,
    @Default(0) int sativa,
    @Default(false) bool autoflower,
    String? description,
    @Default(0) int seedCount,
    int? cycleTime,
    String? url,
    String? parent1,
    String? parent2,
    Map<String, dynamic>? lineageJson,
    String? seedfinderId,
    double? thcContent,
    double? cbdContent,
    String? floweringType,
  }) = _CultivarCreate;

  factory CultivarCreate.fromJson(Map<String, dynamic> json) =>
      _$CultivarCreateFromJson(json);
}

@freezed
abstract class CultivarUpdate with _$CultivarUpdate {
  const factory CultivarUpdate({
    String? name,
    int? breederId,
    int? indica,
    int? sativa,
    bool? autoflower,
    String? description,
    int? seedCount,
    int? cycleTime,
    String? url,
    String? parent1,
    String? parent2,
    Map<String, dynamic>? lineageJson,
    String? seedfinderId,
    double? thcContent,
    double? cbdContent,
    String? floweringType,
  }) = _CultivarUpdate;

  factory CultivarUpdate.fromJson(Map<String, dynamic> json) =>
      _$CultivarUpdateFromJson(json);
}

@freezed
abstract class StrainsParams with _$StrainsParams {
  const factory StrainsParams({
    @Default(1) int page,
    @Default(20) int limit,
    String? search,
    int? breederId,
    bool? autoflower,
    String? sortBy,
    @Default('asc') String sortOrder,
  }) = _StrainsParams;

  factory StrainsParams.fromJson(Map<String, dynamic> json) =>
      _$StrainsParamsFromJson(json);

  const StrainsParams._();

  Map<String, dynamic> toQueryParams() {
    final params = <String, dynamic>{};

    if (page != 1) params['page'] = page.toString();
    if (limit != 20) params['limit'] = limit.toString();
    if (search != null && search!.isNotEmpty) params['search'] = search;
    if (breederId != null) params['breeder_id'] = breederId.toString();
    if (autoflower != null) params['autoflower'] = autoflower.toString();
    if (sortBy != null) params['sort_by'] = sortBy;
    if (sortOrder != 'asc') params['sort_order'] = sortOrder;

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
    required int pages,
    @Default(false) bool hasNext,
    @Default(false) bool hasPrev,
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
    required int indicaCount,
    required int sativaCount,
    required int hybridCount,
    required int autoflowerCount,
    double? averageCycleTime,
  }) = _CultivarStats;

  factory CultivarStats.fromJson(Map<String, dynamic> json) =>
      _$CultivarStatsFromJson(json);
}
