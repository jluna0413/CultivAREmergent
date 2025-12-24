// GENERATED: Freezed-compatible model for Plant domain
// Run: flutter pub run build_runner build --delete-conflicting-outputs
import 'package:freezed_annotation/freezed_annotation.dart';

part 'plant_model.freezed.dart';
part 'plant_model.g.dart';

@freezed
class Plant with _$Plant {
  const factory Plant({
    required int id,
    required String name,
    String? description,
    int? statusId,
    String? statusName,
    String? strain,
    DateTime? startDate,
    DateTime? harvestDate,
    bool? isClone,
    bool? autoflower,
    String? imageUrl,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) = _Plant;

  factory Plant.fromJson(Map<String, dynamic> json) => _$PlantFromJson(json);
}

@freezed
class PlantCreate with _$PlantCreate {
  const factory PlantCreate({
    required String name,
    String? description,
    int? statusId,
    String? strain,
    DateTime? startDate,
    bool? isClone,
    bool? autoflower,
    String? imageUrl,
  }) = _PlantCreate;

  factory PlantCreate.fromJson(Map<String, dynamic> json) => _$PlantCreateFromJson(json);
}

@freezed
class PlantUpdate with _$PlantUpdate {
  const factory PlantUpdate({
    String? name,
    String? description,
    int? statusId,
    String? strain,
    DateTime? startDate,
    DateTime? harvestDate,
    bool? isClone,
    bool? autoflower,
    String? imageUrl,
  }) = _PlantUpdate;

  factory PlantUpdate.fromJson(Map<String, dynamic> json) => _$PlantUpdateFromJson(json);
}
