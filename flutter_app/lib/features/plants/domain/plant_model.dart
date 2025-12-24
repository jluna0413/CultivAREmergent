// ignore_for_file: invalid_annotation_target
import 'package:freezed_annotation/freezed_annotation.dart';

part 'plant_model.freezed.dart';
part 'plant_model.g.dart';

/// Complete Plant model matching backend schema
@freezed
abstract class Plant with _$Plant {
  const factory Plant({
    required int id,
    @JsonKey(name: 'user_id') required int userId,
    required String name,
    String? description,
    @JsonKey(name: 'status_id') required int statusId,
    @JsonKey(name: 'cultivar_id') int? cultivarId,
    @JsonKey(name: 'zone_id') int? zoneId,
    @JsonKey(name: 'current_day') @Default(0) int currentDay,
    @JsonKey(name: 'current_week') @Default(0) int currentWeek,
    @JsonKey(name: 'current_height') String? currentHeight,
    @JsonKey(name: 'height_date') DateTime? heightDate,
    @JsonKey(name: 'last_water_date') DateTime? lastWaterDate,
    @JsonKey(name: 'last_feed_date') DateTime? lastFeedDate,
    @JsonKey(name: 'is_clone') @Default(false) bool isClone,
    @JsonKey(name: 'start_dt') DateTime? startDt,
    @JsonKey(name: 'harvest_weight') double? harvestWeight,
    @JsonKey(name: 'harvest_date') DateTime? harvestDate,
    @JsonKey(name: 'cycle_time') int? cycleTime,
    @JsonKey(name: 'strain_url') String? strainUrl,
    @JsonKey(name: 'est_harvest_date') DateTime? estHarvestDate,
    @Default(false) bool autoflower,
    @JsonKey(name: 'parent_id') int? parentId,
    @JsonKey(name: 'image_url') String? imageUrl,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(name: 'updated_at') DateTime? updatedAt,
    // Computed fields from backend
    @JsonKey(name: 'status_name') String? statusName,
    @JsonKey(name: 'strain_name') String? strainName,
    @JsonKey(name: 'cultivar_name') String? cultivarName,
    @JsonKey(name: 'breeder_name') String? breederName,
    @JsonKey(name: 'zone_name') String? zoneName,
    @JsonKey(name: 'parent_name') String? parentName,
    @JsonKey(name: 'age_days') int? ageDays,
  }) = _Plant;

  factory Plant.fromJson(Map<String, dynamic> json) => _$PlantFromJson(json);
}

/// Model for creating a new plant
@freezed
abstract class PlantCreate with _$PlantCreate {
  const factory PlantCreate({
    required String name,
    String? description,
    @JsonKey(name: 'status_id') @Default(1) int statusId,
    @JsonKey(name: 'cultivar_id') int? cultivarId,
    @JsonKey(name: 'zone_id') int? zoneId,
    @JsonKey(name: 'is_clone') @Default(false) bool isClone,
    @Default(false) bool autoflower,
    @JsonKey(name: 'parent_id') int? parentId,
    @JsonKey(name: 'image_url') String? imageUrl,
  }) = _PlantCreate;

  factory PlantCreate.fromJson(Map<String, dynamic> json) =>
      _$PlantCreateFromJson(json);
}

/// Model for updating an existing plant
@freezed
abstract class PlantUpdate with _$PlantUpdate {
  const factory PlantUpdate({
    String? name,
    String? description,
    @JsonKey(name: 'status_id') int? statusId,
    @JsonKey(name: 'cultivar_id') int? cultivarId,
    @JsonKey(name: 'zone_id') int? zoneId,
    @JsonKey(name: 'current_height') String? currentHeight,
    @JsonKey(name: 'last_water_date') DateTime? lastWaterDate,
    @JsonKey(name: 'last_feed_date') DateTime? lastFeedDate,
    @JsonKey(name: 'is_clone') bool? isClone,
    @JsonKey(name: 'start_dt') DateTime? startDt,
    @JsonKey(name: 'harvest_weight') double? harvestWeight,
    @JsonKey(name: 'harvest_date') DateTime? harvestDate,
    @JsonKey(name: 'est_harvest_date') DateTime? estHarvestDate,
    bool? autoflower,
    @JsonKey(name: 'parent_id') int? parentId,
    @JsonKey(name: 'image_url') String? imageUrl,
  }) = _PlantUpdate;

  factory PlantUpdate.fromJson(Map<String, dynamic> json) =>
      _$PlantUpdateFromJson(json);
}

/// Paginated response for plant lists
@freezed
abstract class PaginatedPlantsResponse with _$PaginatedPlantsResponse {
  const factory PaginatedPlantsResponse({
    @Default([]) List<Plant> items,
    @Default(0) int total,
    @Default(1) int page,
    @JsonKey(name: 'page_size') @Default(20) int limit,
    @Default(0) int pages,
    @JsonKey(name: 'has_next') @Default(false) bool hasNext,
    @JsonKey(name: 'has_prev') @Default(false) bool hasPrev,
  }) = _PaginatedPlantsResponse;

  factory PaginatedPlantsResponse.fromJson(Map<String, dynamic> json) =>
      _$PaginatedPlantsResponseFromJson(json);
}

/// Parameters for fetching plants list
class PlantsParams {
  const PlantsParams({
    this.page = 1,
    this.limit = 20,
    this.status,
    this.search,
    this.cultivarId,
    this.zoneId,
    this.sortBy,
    this.sortOrder,
  });

  final int page;
  final int limit;
  final String? status;
  final String? search;
  final int? cultivarId;
  final int? zoneId;
  final String? sortBy;
  final String? sortOrder;

  PlantsParams copyWith({
    int? page,
    int? limit,
    String? status,
    String? search,
    int? cultivarId,
    int? zoneId,
    String? sortBy,
    String? sortOrder,
  }) {
    return PlantsParams(
      page: page ?? this.page,
      limit: limit ?? this.limit,
      status: status ?? this.status,
      search: search ?? this.search,
      cultivarId: cultivarId ?? this.cultivarId,
      zoneId: zoneId ?? this.zoneId,
      sortBy: sortBy ?? this.sortBy,
      sortOrder: sortOrder ?? this.sortOrder,
    );
  }

  Map<String, String> toQueryParameters() {
    final params = <String, String>{
      'page': page.toString(),
      'limit': limit.toString(),
    };
    if (status != null) params['status'] = status!;
    if (search != null) params['search'] = search!;
    if (cultivarId != null) params['cultivar_id'] = cultivarId.toString();
    if (zoneId != null) params['zone_id'] = zoneId.toString();
    if (sortBy != null) params['sort_by'] = sortBy!;
    if (sortOrder != null) params['sort_order'] = sortOrder!;
    return params;
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is PlantsParams &&
        other.page == page &&
        other.limit == limit &&
        other.status == status &&
        other.search == search &&
        other.cultivarId == cultivarId &&
        other.zoneId == zoneId &&
        other.sortBy == sortBy &&
        other.sortOrder == sortOrder;
  }

  @override
  int get hashCode {
    return Object.hash(
      page,
      limit,
      status,
      search,
      cultivarId,
      zoneId,
      sortBy,
      sortOrder,
    );
  }
}
