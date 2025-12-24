// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'plant_model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

Plant _$PlantFromJson(Map<String, dynamic> json) {
  return _Plant.fromJson(json);
}

/// @nodoc
mixin _$Plant {
  int get id => throw _privateConstructorUsedError;
  @JsonKey(name: 'user_id')
  int get userId => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  @JsonKey(name: 'status_id')
  int get statusId => throw _privateConstructorUsedError;
  @JsonKey(name: 'cultivar_id')
  int? get cultivarId => throw _privateConstructorUsedError;
  @JsonKey(name: 'zone_id')
  int? get zoneId => throw _privateConstructorUsedError;
  @JsonKey(name: 'current_day')
  int get currentDay => throw _privateConstructorUsedError;
  @JsonKey(name: 'current_week')
  int get currentWeek => throw _privateConstructorUsedError;
  @JsonKey(name: 'current_height')
  String? get currentHeight => throw _privateConstructorUsedError;
  @JsonKey(name: 'height_date')
  DateTime? get heightDate => throw _privateConstructorUsedError;
  @JsonKey(name: 'last_water_date')
  DateTime? get lastWaterDate => throw _privateConstructorUsedError;
  @JsonKey(name: 'last_feed_date')
  DateTime? get lastFeedDate => throw _privateConstructorUsedError;
  @JsonKey(name: 'is_clone')
  bool get isClone => throw _privateConstructorUsedError;
  @JsonKey(name: 'start_dt')
  DateTime? get startDt => throw _privateConstructorUsedError;
  @JsonKey(name: 'harvest_weight')
  double? get harvestWeight => throw _privateConstructorUsedError;
  @JsonKey(name: 'harvest_date')
  DateTime? get harvestDate => throw _privateConstructorUsedError;
  @JsonKey(name: 'cycle_time')
  int? get cycleTime => throw _privateConstructorUsedError;
  @JsonKey(name: 'strain_url')
  String? get strainUrl => throw _privateConstructorUsedError;
  @JsonKey(name: 'est_harvest_date')
  DateTime? get estHarvestDate => throw _privateConstructorUsedError;
  bool get autoflower => throw _privateConstructorUsedError;
  @JsonKey(name: 'parent_id')
  int? get parentId => throw _privateConstructorUsedError;
  @JsonKey(name: 'image_url')
  String? get imageUrl => throw _privateConstructorUsedError;
  @JsonKey(name: 'created_at')
  DateTime? get createdAt => throw _privateConstructorUsedError;
  @JsonKey(name: 'updated_at')
  DateTime? get updatedAt => throw _privateConstructorUsedError; // Computed fields from backend
  @JsonKey(name: 'status_name')
  String? get statusName => throw _privateConstructorUsedError;
  @JsonKey(name: 'strain_name')
  String? get strainName => throw _privateConstructorUsedError;
  @JsonKey(name: 'cultivar_name')
  String? get cultivarName => throw _privateConstructorUsedError;
  @JsonKey(name: 'breeder_name')
  String? get breederName => throw _privateConstructorUsedError;
  @JsonKey(name: 'zone_name')
  String? get zoneName => throw _privateConstructorUsedError;
  @JsonKey(name: 'parent_name')
  String? get parentName => throw _privateConstructorUsedError;
  @JsonKey(name: 'age_days')
  int? get ageDays => throw _privateConstructorUsedError;

  /// Serializes this Plant to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of Plant
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $PlantCopyWith<Plant> get copyWith => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PlantCopyWith<$Res> {
  factory $PlantCopyWith(Plant value, $Res Function(Plant) then) =
      _$PlantCopyWithImpl<$Res, Plant>;
  @useResult
  $Res call({
    int id,
    @JsonKey(name: 'user_id') int userId,
    String name,
    String? description,
    @JsonKey(name: 'status_id') int statusId,
    @JsonKey(name: 'cultivar_id') int? cultivarId,
    @JsonKey(name: 'zone_id') int? zoneId,
    @JsonKey(name: 'current_day') int currentDay,
    @JsonKey(name: 'current_week') int currentWeek,
    @JsonKey(name: 'current_height') String? currentHeight,
    @JsonKey(name: 'height_date') DateTime? heightDate,
    @JsonKey(name: 'last_water_date') DateTime? lastWaterDate,
    @JsonKey(name: 'last_feed_date') DateTime? lastFeedDate,
    @JsonKey(name: 'is_clone') bool isClone,
    @JsonKey(name: 'start_dt') DateTime? startDt,
    @JsonKey(name: 'harvest_weight') double? harvestWeight,
    @JsonKey(name: 'harvest_date') DateTime? harvestDate,
    @JsonKey(name: 'cycle_time') int? cycleTime,
    @JsonKey(name: 'strain_url') String? strainUrl,
    @JsonKey(name: 'est_harvest_date') DateTime? estHarvestDate,
    bool autoflower,
    @JsonKey(name: 'parent_id') int? parentId,
    @JsonKey(name: 'image_url') String? imageUrl,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(name: 'updated_at') DateTime? updatedAt,
    @JsonKey(name: 'status_name') String? statusName,
    @JsonKey(name: 'strain_name') String? strainName,
    @JsonKey(name: 'cultivar_name') String? cultivarName,
    @JsonKey(name: 'breeder_name') String? breederName,
    @JsonKey(name: 'zone_name') String? zoneName,
    @JsonKey(name: 'parent_name') String? parentName,
    @JsonKey(name: 'age_days') int? ageDays,
  });
}

/// @nodoc
class _$PlantCopyWithImpl<$Res, $Val extends Plant>
    implements $PlantCopyWith<$Res> {
  _$PlantCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of Plant
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? name = null,
    Object? description = freezed,
    Object? statusId = null,
    Object? cultivarId = freezed,
    Object? zoneId = freezed,
    Object? currentDay = null,
    Object? currentWeek = null,
    Object? currentHeight = freezed,
    Object? heightDate = freezed,
    Object? lastWaterDate = freezed,
    Object? lastFeedDate = freezed,
    Object? isClone = null,
    Object? startDt = freezed,
    Object? harvestWeight = freezed,
    Object? harvestDate = freezed,
    Object? cycleTime = freezed,
    Object? strainUrl = freezed,
    Object? estHarvestDate = freezed,
    Object? autoflower = null,
    Object? parentId = freezed,
    Object? imageUrl = freezed,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
    Object? statusName = freezed,
    Object? strainName = freezed,
    Object? cultivarName = freezed,
    Object? breederName = freezed,
    Object? zoneName = freezed,
    Object? parentName = freezed,
    Object? ageDays = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as int,
            userId: null == userId
                ? _value.userId
                : userId // ignore: cast_nullable_to_non_nullable
                      as int,
            name: null == name
                ? _value.name
                : name // ignore: cast_nullable_to_non_nullable
                      as String,
            description: freezed == description
                ? _value.description
                : description // ignore: cast_nullable_to_non_nullable
                      as String?,
            statusId: null == statusId
                ? _value.statusId
                : statusId // ignore: cast_nullable_to_non_nullable
                      as int,
            cultivarId: freezed == cultivarId
                ? _value.cultivarId
                : cultivarId // ignore: cast_nullable_to_non_nullable
                      as int?,
            zoneId: freezed == zoneId
                ? _value.zoneId
                : zoneId // ignore: cast_nullable_to_non_nullable
                      as int?,
            currentDay: null == currentDay
                ? _value.currentDay
                : currentDay // ignore: cast_nullable_to_non_nullable
                      as int,
            currentWeek: null == currentWeek
                ? _value.currentWeek
                : currentWeek // ignore: cast_nullable_to_non_nullable
                      as int,
            currentHeight: freezed == currentHeight
                ? _value.currentHeight
                : currentHeight // ignore: cast_nullable_to_non_nullable
                      as String?,
            heightDate: freezed == heightDate
                ? _value.heightDate
                : heightDate // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            lastWaterDate: freezed == lastWaterDate
                ? _value.lastWaterDate
                : lastWaterDate // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            lastFeedDate: freezed == lastFeedDate
                ? _value.lastFeedDate
                : lastFeedDate // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            isClone: null == isClone
                ? _value.isClone
                : isClone // ignore: cast_nullable_to_non_nullable
                      as bool,
            startDt: freezed == startDt
                ? _value.startDt
                : startDt // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            harvestWeight: freezed == harvestWeight
                ? _value.harvestWeight
                : harvestWeight // ignore: cast_nullable_to_non_nullable
                      as double?,
            harvestDate: freezed == harvestDate
                ? _value.harvestDate
                : harvestDate // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            cycleTime: freezed == cycleTime
                ? _value.cycleTime
                : cycleTime // ignore: cast_nullable_to_non_nullable
                      as int?,
            strainUrl: freezed == strainUrl
                ? _value.strainUrl
                : strainUrl // ignore: cast_nullable_to_non_nullable
                      as String?,
            estHarvestDate: freezed == estHarvestDate
                ? _value.estHarvestDate
                : estHarvestDate // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            autoflower: null == autoflower
                ? _value.autoflower
                : autoflower // ignore: cast_nullable_to_non_nullable
                      as bool,
            parentId: freezed == parentId
                ? _value.parentId
                : parentId // ignore: cast_nullable_to_non_nullable
                      as int?,
            imageUrl: freezed == imageUrl
                ? _value.imageUrl
                : imageUrl // ignore: cast_nullable_to_non_nullable
                      as String?,
            createdAt: freezed == createdAt
                ? _value.createdAt
                : createdAt // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            updatedAt: freezed == updatedAt
                ? _value.updatedAt
                : updatedAt // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            statusName: freezed == statusName
                ? _value.statusName
                : statusName // ignore: cast_nullable_to_non_nullable
                      as String?,
            strainName: freezed == strainName
                ? _value.strainName
                : strainName // ignore: cast_nullable_to_non_nullable
                      as String?,
            cultivarName: freezed == cultivarName
                ? _value.cultivarName
                : cultivarName // ignore: cast_nullable_to_non_nullable
                      as String?,
            breederName: freezed == breederName
                ? _value.breederName
                : breederName // ignore: cast_nullable_to_non_nullable
                      as String?,
            zoneName: freezed == zoneName
                ? _value.zoneName
                : zoneName // ignore: cast_nullable_to_non_nullable
                      as String?,
            parentName: freezed == parentName
                ? _value.parentName
                : parentName // ignore: cast_nullable_to_non_nullable
                      as String?,
            ageDays: freezed == ageDays
                ? _value.ageDays
                : ageDays // ignore: cast_nullable_to_non_nullable
                      as int?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$PlantImplCopyWith<$Res> implements $PlantCopyWith<$Res> {
  factory _$$PlantImplCopyWith(
    _$PlantImpl value,
    $Res Function(_$PlantImpl) then,
  ) = __$$PlantImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    int id,
    @JsonKey(name: 'user_id') int userId,
    String name,
    String? description,
    @JsonKey(name: 'status_id') int statusId,
    @JsonKey(name: 'cultivar_id') int? cultivarId,
    @JsonKey(name: 'zone_id') int? zoneId,
    @JsonKey(name: 'current_day') int currentDay,
    @JsonKey(name: 'current_week') int currentWeek,
    @JsonKey(name: 'current_height') String? currentHeight,
    @JsonKey(name: 'height_date') DateTime? heightDate,
    @JsonKey(name: 'last_water_date') DateTime? lastWaterDate,
    @JsonKey(name: 'last_feed_date') DateTime? lastFeedDate,
    @JsonKey(name: 'is_clone') bool isClone,
    @JsonKey(name: 'start_dt') DateTime? startDt,
    @JsonKey(name: 'harvest_weight') double? harvestWeight,
    @JsonKey(name: 'harvest_date') DateTime? harvestDate,
    @JsonKey(name: 'cycle_time') int? cycleTime,
    @JsonKey(name: 'strain_url') String? strainUrl,
    @JsonKey(name: 'est_harvest_date') DateTime? estHarvestDate,
    bool autoflower,
    @JsonKey(name: 'parent_id') int? parentId,
    @JsonKey(name: 'image_url') String? imageUrl,
    @JsonKey(name: 'created_at') DateTime? createdAt,
    @JsonKey(name: 'updated_at') DateTime? updatedAt,
    @JsonKey(name: 'status_name') String? statusName,
    @JsonKey(name: 'strain_name') String? strainName,
    @JsonKey(name: 'cultivar_name') String? cultivarName,
    @JsonKey(name: 'breeder_name') String? breederName,
    @JsonKey(name: 'zone_name') String? zoneName,
    @JsonKey(name: 'parent_name') String? parentName,
    @JsonKey(name: 'age_days') int? ageDays,
  });
}

/// @nodoc
class __$$PlantImplCopyWithImpl<$Res>
    extends _$PlantCopyWithImpl<$Res, _$PlantImpl>
    implements _$$PlantImplCopyWith<$Res> {
  __$$PlantImplCopyWithImpl(
    _$PlantImpl _value,
    $Res Function(_$PlantImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of Plant
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? name = null,
    Object? description = freezed,
    Object? statusId = null,
    Object? cultivarId = freezed,
    Object? zoneId = freezed,
    Object? currentDay = null,
    Object? currentWeek = null,
    Object? currentHeight = freezed,
    Object? heightDate = freezed,
    Object? lastWaterDate = freezed,
    Object? lastFeedDate = freezed,
    Object? isClone = null,
    Object? startDt = freezed,
    Object? harvestWeight = freezed,
    Object? harvestDate = freezed,
    Object? cycleTime = freezed,
    Object? strainUrl = freezed,
    Object? estHarvestDate = freezed,
    Object? autoflower = null,
    Object? parentId = freezed,
    Object? imageUrl = freezed,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
    Object? statusName = freezed,
    Object? strainName = freezed,
    Object? cultivarName = freezed,
    Object? breederName = freezed,
    Object? zoneName = freezed,
    Object? parentName = freezed,
    Object? ageDays = freezed,
  }) {
    return _then(
      _$PlantImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as int,
        userId: null == userId
            ? _value.userId
            : userId // ignore: cast_nullable_to_non_nullable
                  as int,
        name: null == name
            ? _value.name
            : name // ignore: cast_nullable_to_non_nullable
                  as String,
        description: freezed == description
            ? _value.description
            : description // ignore: cast_nullable_to_non_nullable
                  as String?,
        statusId: null == statusId
            ? _value.statusId
            : statusId // ignore: cast_nullable_to_non_nullable
                  as int,
        cultivarId: freezed == cultivarId
            ? _value.cultivarId
            : cultivarId // ignore: cast_nullable_to_non_nullable
                  as int?,
        zoneId: freezed == zoneId
            ? _value.zoneId
            : zoneId // ignore: cast_nullable_to_non_nullable
                  as int?,
        currentDay: null == currentDay
            ? _value.currentDay
            : currentDay // ignore: cast_nullable_to_non_nullable
                  as int,
        currentWeek: null == currentWeek
            ? _value.currentWeek
            : currentWeek // ignore: cast_nullable_to_non_nullable
                  as int,
        currentHeight: freezed == currentHeight
            ? _value.currentHeight
            : currentHeight // ignore: cast_nullable_to_non_nullable
                  as String?,
        heightDate: freezed == heightDate
            ? _value.heightDate
            : heightDate // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        lastWaterDate: freezed == lastWaterDate
            ? _value.lastWaterDate
            : lastWaterDate // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        lastFeedDate: freezed == lastFeedDate
            ? _value.lastFeedDate
            : lastFeedDate // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        isClone: null == isClone
            ? _value.isClone
            : isClone // ignore: cast_nullable_to_non_nullable
                  as bool,
        startDt: freezed == startDt
            ? _value.startDt
            : startDt // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        harvestWeight: freezed == harvestWeight
            ? _value.harvestWeight
            : harvestWeight // ignore: cast_nullable_to_non_nullable
                  as double?,
        harvestDate: freezed == harvestDate
            ? _value.harvestDate
            : harvestDate // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        cycleTime: freezed == cycleTime
            ? _value.cycleTime
            : cycleTime // ignore: cast_nullable_to_non_nullable
                  as int?,
        strainUrl: freezed == strainUrl
            ? _value.strainUrl
            : strainUrl // ignore: cast_nullable_to_non_nullable
                  as String?,
        estHarvestDate: freezed == estHarvestDate
            ? _value.estHarvestDate
            : estHarvestDate // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        autoflower: null == autoflower
            ? _value.autoflower
            : autoflower // ignore: cast_nullable_to_non_nullable
                  as bool,
        parentId: freezed == parentId
            ? _value.parentId
            : parentId // ignore: cast_nullable_to_non_nullable
                  as int?,
        imageUrl: freezed == imageUrl
            ? _value.imageUrl
            : imageUrl // ignore: cast_nullable_to_non_nullable
                  as String?,
        createdAt: freezed == createdAt
            ? _value.createdAt
            : createdAt // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        updatedAt: freezed == updatedAt
            ? _value.updatedAt
            : updatedAt // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        statusName: freezed == statusName
            ? _value.statusName
            : statusName // ignore: cast_nullable_to_non_nullable
                  as String?,
        strainName: freezed == strainName
            ? _value.strainName
            : strainName // ignore: cast_nullable_to_non_nullable
                  as String?,
        cultivarName: freezed == cultivarName
            ? _value.cultivarName
            : cultivarName // ignore: cast_nullable_to_non_nullable
                  as String?,
        breederName: freezed == breederName
            ? _value.breederName
            : breederName // ignore: cast_nullable_to_non_nullable
                  as String?,
        zoneName: freezed == zoneName
            ? _value.zoneName
            : zoneName // ignore: cast_nullable_to_non_nullable
                  as String?,
        parentName: freezed == parentName
            ? _value.parentName
            : parentName // ignore: cast_nullable_to_non_nullable
                  as String?,
        ageDays: freezed == ageDays
            ? _value.ageDays
            : ageDays // ignore: cast_nullable_to_non_nullable
                  as int?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$PlantImpl implements _Plant {
  const _$PlantImpl({
    required this.id,
    @JsonKey(name: 'user_id') required this.userId,
    required this.name,
    this.description,
    @JsonKey(name: 'status_id') required this.statusId,
    @JsonKey(name: 'cultivar_id') this.cultivarId,
    @JsonKey(name: 'zone_id') this.zoneId,
    @JsonKey(name: 'current_day') this.currentDay = 0,
    @JsonKey(name: 'current_week') this.currentWeek = 0,
    @JsonKey(name: 'current_height') this.currentHeight,
    @JsonKey(name: 'height_date') this.heightDate,
    @JsonKey(name: 'last_water_date') this.lastWaterDate,
    @JsonKey(name: 'last_feed_date') this.lastFeedDate,
    @JsonKey(name: 'is_clone') this.isClone = false,
    @JsonKey(name: 'start_dt') this.startDt,
    @JsonKey(name: 'harvest_weight') this.harvestWeight,
    @JsonKey(name: 'harvest_date') this.harvestDate,
    @JsonKey(name: 'cycle_time') this.cycleTime,
    @JsonKey(name: 'strain_url') this.strainUrl,
    @JsonKey(name: 'est_harvest_date') this.estHarvestDate,
    this.autoflower = false,
    @JsonKey(name: 'parent_id') this.parentId,
    @JsonKey(name: 'image_url') this.imageUrl,
    @JsonKey(name: 'created_at') this.createdAt,
    @JsonKey(name: 'updated_at') this.updatedAt,
    @JsonKey(name: 'status_name') this.statusName,
    @JsonKey(name: 'strain_name') this.strainName,
    @JsonKey(name: 'cultivar_name') this.cultivarName,
    @JsonKey(name: 'breeder_name') this.breederName,
    @JsonKey(name: 'zone_name') this.zoneName,
    @JsonKey(name: 'parent_name') this.parentName,
    @JsonKey(name: 'age_days') this.ageDays,
  });

  factory _$PlantImpl.fromJson(Map<String, dynamic> json) =>
      _$$PlantImplFromJson(json);

  @override
  final int id;
  @override
  @JsonKey(name: 'user_id')
  final int userId;
  @override
  final String name;
  @override
  final String? description;
  @override
  @JsonKey(name: 'status_id')
  final int statusId;
  @override
  @JsonKey(name: 'cultivar_id')
  final int? cultivarId;
  @override
  @JsonKey(name: 'zone_id')
  final int? zoneId;
  @override
  @JsonKey(name: 'current_day')
  final int currentDay;
  @override
  @JsonKey(name: 'current_week')
  final int currentWeek;
  @override
  @JsonKey(name: 'current_height')
  final String? currentHeight;
  @override
  @JsonKey(name: 'height_date')
  final DateTime? heightDate;
  @override
  @JsonKey(name: 'last_water_date')
  final DateTime? lastWaterDate;
  @override
  @JsonKey(name: 'last_feed_date')
  final DateTime? lastFeedDate;
  @override
  @JsonKey(name: 'is_clone')
  final bool isClone;
  @override
  @JsonKey(name: 'start_dt')
  final DateTime? startDt;
  @override
  @JsonKey(name: 'harvest_weight')
  final double? harvestWeight;
  @override
  @JsonKey(name: 'harvest_date')
  final DateTime? harvestDate;
  @override
  @JsonKey(name: 'cycle_time')
  final int? cycleTime;
  @override
  @JsonKey(name: 'strain_url')
  final String? strainUrl;
  @override
  @JsonKey(name: 'est_harvest_date')
  final DateTime? estHarvestDate;
  @override
  @JsonKey()
  final bool autoflower;
  @override
  @JsonKey(name: 'parent_id')
  final int? parentId;
  @override
  @JsonKey(name: 'image_url')
  final String? imageUrl;
  @override
  @JsonKey(name: 'created_at')
  final DateTime? createdAt;
  @override
  @JsonKey(name: 'updated_at')
  final DateTime? updatedAt;
  // Computed fields from backend
  @override
  @JsonKey(name: 'status_name')
  final String? statusName;
  @override
  @JsonKey(name: 'strain_name')
  final String? strainName;
  @override
  @JsonKey(name: 'cultivar_name')
  final String? cultivarName;
  @override
  @JsonKey(name: 'breeder_name')
  final String? breederName;
  @override
  @JsonKey(name: 'zone_name')
  final String? zoneName;
  @override
  @JsonKey(name: 'parent_name')
  final String? parentName;
  @override
  @JsonKey(name: 'age_days')
  final int? ageDays;

  @override
  String toString() {
    return 'Plant(id: $id, userId: $userId, name: $name, description: $description, statusId: $statusId, cultivarId: $cultivarId, zoneId: $zoneId, currentDay: $currentDay, currentWeek: $currentWeek, currentHeight: $currentHeight, heightDate: $heightDate, lastWaterDate: $lastWaterDate, lastFeedDate: $lastFeedDate, isClone: $isClone, startDt: $startDt, harvestWeight: $harvestWeight, harvestDate: $harvestDate, cycleTime: $cycleTime, strainUrl: $strainUrl, estHarvestDate: $estHarvestDate, autoflower: $autoflower, parentId: $parentId, imageUrl: $imageUrl, createdAt: $createdAt, updatedAt: $updatedAt, statusName: $statusName, strainName: $strainName, cultivarName: $cultivarName, breederName: $breederName, zoneName: $zoneName, parentName: $parentName, ageDays: $ageDays)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PlantImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.statusId, statusId) ||
                other.statusId == statusId) &&
            (identical(other.cultivarId, cultivarId) ||
                other.cultivarId == cultivarId) &&
            (identical(other.zoneId, zoneId) || other.zoneId == zoneId) &&
            (identical(other.currentDay, currentDay) ||
                other.currentDay == currentDay) &&
            (identical(other.currentWeek, currentWeek) ||
                other.currentWeek == currentWeek) &&
            (identical(other.currentHeight, currentHeight) ||
                other.currentHeight == currentHeight) &&
            (identical(other.heightDate, heightDate) ||
                other.heightDate == heightDate) &&
            (identical(other.lastWaterDate, lastWaterDate) ||
                other.lastWaterDate == lastWaterDate) &&
            (identical(other.lastFeedDate, lastFeedDate) ||
                other.lastFeedDate == lastFeedDate) &&
            (identical(other.isClone, isClone) || other.isClone == isClone) &&
            (identical(other.startDt, startDt) || other.startDt == startDt) &&
            (identical(other.harvestWeight, harvestWeight) ||
                other.harvestWeight == harvestWeight) &&
            (identical(other.harvestDate, harvestDate) ||
                other.harvestDate == harvestDate) &&
            (identical(other.cycleTime, cycleTime) ||
                other.cycleTime == cycleTime) &&
            (identical(other.strainUrl, strainUrl) ||
                other.strainUrl == strainUrl) &&
            (identical(other.estHarvestDate, estHarvestDate) ||
                other.estHarvestDate == estHarvestDate) &&
            (identical(other.autoflower, autoflower) ||
                other.autoflower == autoflower) &&
            (identical(other.parentId, parentId) ||
                other.parentId == parentId) &&
            (identical(other.imageUrl, imageUrl) ||
                other.imageUrl == imageUrl) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt) &&
            (identical(other.updatedAt, updatedAt) ||
                other.updatedAt == updatedAt) &&
            (identical(other.statusName, statusName) ||
                other.statusName == statusName) &&
            (identical(other.strainName, strainName) ||
                other.strainName == strainName) &&
            (identical(other.cultivarName, cultivarName) ||
                other.cultivarName == cultivarName) &&
            (identical(other.breederName, breederName) ||
                other.breederName == breederName) &&
            (identical(other.zoneName, zoneName) ||
                other.zoneName == zoneName) &&
            (identical(other.parentName, parentName) ||
                other.parentName == parentName) &&
            (identical(other.ageDays, ageDays) || other.ageDays == ageDays));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hashAll([
    runtimeType,
    id,
    userId,
    name,
    description,
    statusId,
    cultivarId,
    zoneId,
    currentDay,
    currentWeek,
    currentHeight,
    heightDate,
    lastWaterDate,
    lastFeedDate,
    isClone,
    startDt,
    harvestWeight,
    harvestDate,
    cycleTime,
    strainUrl,
    estHarvestDate,
    autoflower,
    parentId,
    imageUrl,
    createdAt,
    updatedAt,
    statusName,
    strainName,
    cultivarName,
    breederName,
    zoneName,
    parentName,
    ageDays,
  ]);

  /// Create a copy of Plant
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$PlantImplCopyWith<_$PlantImpl> get copyWith =>
      __$$PlantImplCopyWithImpl<_$PlantImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PlantImplToJson(this);
  }
}

abstract class _Plant implements Plant {
  const factory _Plant({
    required final int id,
    @JsonKey(name: 'user_id') required final int userId,
    required final String name,
    final String? description,
    @JsonKey(name: 'status_id') required final int statusId,
    @JsonKey(name: 'cultivar_id') final int? cultivarId,
    @JsonKey(name: 'zone_id') final int? zoneId,
    @JsonKey(name: 'current_day') final int currentDay,
    @JsonKey(name: 'current_week') final int currentWeek,
    @JsonKey(name: 'current_height') final String? currentHeight,
    @JsonKey(name: 'height_date') final DateTime? heightDate,
    @JsonKey(name: 'last_water_date') final DateTime? lastWaterDate,
    @JsonKey(name: 'last_feed_date') final DateTime? lastFeedDate,
    @JsonKey(name: 'is_clone') final bool isClone,
    @JsonKey(name: 'start_dt') final DateTime? startDt,
    @JsonKey(name: 'harvest_weight') final double? harvestWeight,
    @JsonKey(name: 'harvest_date') final DateTime? harvestDate,
    @JsonKey(name: 'cycle_time') final int? cycleTime,
    @JsonKey(name: 'strain_url') final String? strainUrl,
    @JsonKey(name: 'est_harvest_date') final DateTime? estHarvestDate,
    final bool autoflower,
    @JsonKey(name: 'parent_id') final int? parentId,
    @JsonKey(name: 'image_url') final String? imageUrl,
    @JsonKey(name: 'created_at') final DateTime? createdAt,
    @JsonKey(name: 'updated_at') final DateTime? updatedAt,
    @JsonKey(name: 'status_name') final String? statusName,
    @JsonKey(name: 'strain_name') final String? strainName,
    @JsonKey(name: 'cultivar_name') final String? cultivarName,
    @JsonKey(name: 'breeder_name') final String? breederName,
    @JsonKey(name: 'zone_name') final String? zoneName,
    @JsonKey(name: 'parent_name') final String? parentName,
    @JsonKey(name: 'age_days') final int? ageDays,
  }) = _$PlantImpl;

  factory _Plant.fromJson(Map<String, dynamic> json) = _$PlantImpl.fromJson;

  @override
  int get id;
  @override
  @JsonKey(name: 'user_id')
  int get userId;
  @override
  String get name;
  @override
  String? get description;
  @override
  @JsonKey(name: 'status_id')
  int get statusId;
  @override
  @JsonKey(name: 'cultivar_id')
  int? get cultivarId;
  @override
  @JsonKey(name: 'zone_id')
  int? get zoneId;
  @override
  @JsonKey(name: 'current_day')
  int get currentDay;
  @override
  @JsonKey(name: 'current_week')
  int get currentWeek;
  @override
  @JsonKey(name: 'current_height')
  String? get currentHeight;
  @override
  @JsonKey(name: 'height_date')
  DateTime? get heightDate;
  @override
  @JsonKey(name: 'last_water_date')
  DateTime? get lastWaterDate;
  @override
  @JsonKey(name: 'last_feed_date')
  DateTime? get lastFeedDate;
  @override
  @JsonKey(name: 'is_clone')
  bool get isClone;
  @override
  @JsonKey(name: 'start_dt')
  DateTime? get startDt;
  @override
  @JsonKey(name: 'harvest_weight')
  double? get harvestWeight;
  @override
  @JsonKey(name: 'harvest_date')
  DateTime? get harvestDate;
  @override
  @JsonKey(name: 'cycle_time')
  int? get cycleTime;
  @override
  @JsonKey(name: 'strain_url')
  String? get strainUrl;
  @override
  @JsonKey(name: 'est_harvest_date')
  DateTime? get estHarvestDate;
  @override
  bool get autoflower;
  @override
  @JsonKey(name: 'parent_id')
  int? get parentId;
  @override
  @JsonKey(name: 'image_url')
  String? get imageUrl;
  @override
  @JsonKey(name: 'created_at')
  DateTime? get createdAt;
  @override
  @JsonKey(name: 'updated_at')
  DateTime? get updatedAt; // Computed fields from backend
  @override
  @JsonKey(name: 'status_name')
  String? get statusName;
  @override
  @JsonKey(name: 'strain_name')
  String? get strainName;
  @override
  @JsonKey(name: 'cultivar_name')
  String? get cultivarName;
  @override
  @JsonKey(name: 'breeder_name')
  String? get breederName;
  @override
  @JsonKey(name: 'zone_name')
  String? get zoneName;
  @override
  @JsonKey(name: 'parent_name')
  String? get parentName;
  @override
  @JsonKey(name: 'age_days')
  int? get ageDays;

  /// Create a copy of Plant
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$PlantImplCopyWith<_$PlantImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

PlantCreate _$PlantCreateFromJson(Map<String, dynamic> json) {
  return _PlantCreate.fromJson(json);
}

/// @nodoc
mixin _$PlantCreate {
  String get name => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  @JsonKey(name: 'status_id')
  int get statusId => throw _privateConstructorUsedError;
  @JsonKey(name: 'cultivar_id')
  int? get cultivarId => throw _privateConstructorUsedError;
  @JsonKey(name: 'zone_id')
  int? get zoneId => throw _privateConstructorUsedError;
  @JsonKey(name: 'is_clone')
  bool get isClone => throw _privateConstructorUsedError;
  bool get autoflower => throw _privateConstructorUsedError;
  @JsonKey(name: 'parent_id')
  int? get parentId => throw _privateConstructorUsedError;
  @JsonKey(name: 'image_url')
  String? get imageUrl => throw _privateConstructorUsedError;

  /// Serializes this PlantCreate to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of PlantCreate
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $PlantCreateCopyWith<PlantCreate> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PlantCreateCopyWith<$Res> {
  factory $PlantCreateCopyWith(
    PlantCreate value,
    $Res Function(PlantCreate) then,
  ) = _$PlantCreateCopyWithImpl<$Res, PlantCreate>;
  @useResult
  $Res call({
    String name,
    String? description,
    @JsonKey(name: 'status_id') int statusId,
    @JsonKey(name: 'cultivar_id') int? cultivarId,
    @JsonKey(name: 'zone_id') int? zoneId,
    @JsonKey(name: 'is_clone') bool isClone,
    bool autoflower,
    @JsonKey(name: 'parent_id') int? parentId,
    @JsonKey(name: 'image_url') String? imageUrl,
  });
}

/// @nodoc
class _$PlantCreateCopyWithImpl<$Res, $Val extends PlantCreate>
    implements $PlantCreateCopyWith<$Res> {
  _$PlantCreateCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of PlantCreate
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? name = null,
    Object? description = freezed,
    Object? statusId = null,
    Object? cultivarId = freezed,
    Object? zoneId = freezed,
    Object? isClone = null,
    Object? autoflower = null,
    Object? parentId = freezed,
    Object? imageUrl = freezed,
  }) {
    return _then(
      _value.copyWith(
            name: null == name
                ? _value.name
                : name // ignore: cast_nullable_to_non_nullable
                      as String,
            description: freezed == description
                ? _value.description
                : description // ignore: cast_nullable_to_non_nullable
                      as String?,
            statusId: null == statusId
                ? _value.statusId
                : statusId // ignore: cast_nullable_to_non_nullable
                      as int,
            cultivarId: freezed == cultivarId
                ? _value.cultivarId
                : cultivarId // ignore: cast_nullable_to_non_nullable
                      as int?,
            zoneId: freezed == zoneId
                ? _value.zoneId
                : zoneId // ignore: cast_nullable_to_non_nullable
                      as int?,
            isClone: null == isClone
                ? _value.isClone
                : isClone // ignore: cast_nullable_to_non_nullable
                      as bool,
            autoflower: null == autoflower
                ? _value.autoflower
                : autoflower // ignore: cast_nullable_to_non_nullable
                      as bool,
            parentId: freezed == parentId
                ? _value.parentId
                : parentId // ignore: cast_nullable_to_non_nullable
                      as int?,
            imageUrl: freezed == imageUrl
                ? _value.imageUrl
                : imageUrl // ignore: cast_nullable_to_non_nullable
                      as String?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$PlantCreateImplCopyWith<$Res>
    implements $PlantCreateCopyWith<$Res> {
  factory _$$PlantCreateImplCopyWith(
    _$PlantCreateImpl value,
    $Res Function(_$PlantCreateImpl) then,
  ) = __$$PlantCreateImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String name,
    String? description,
    @JsonKey(name: 'status_id') int statusId,
    @JsonKey(name: 'cultivar_id') int? cultivarId,
    @JsonKey(name: 'zone_id') int? zoneId,
    @JsonKey(name: 'is_clone') bool isClone,
    bool autoflower,
    @JsonKey(name: 'parent_id') int? parentId,
    @JsonKey(name: 'image_url') String? imageUrl,
  });
}

/// @nodoc
class __$$PlantCreateImplCopyWithImpl<$Res>
    extends _$PlantCreateCopyWithImpl<$Res, _$PlantCreateImpl>
    implements _$$PlantCreateImplCopyWith<$Res> {
  __$$PlantCreateImplCopyWithImpl(
    _$PlantCreateImpl _value,
    $Res Function(_$PlantCreateImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of PlantCreate
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? name = null,
    Object? description = freezed,
    Object? statusId = null,
    Object? cultivarId = freezed,
    Object? zoneId = freezed,
    Object? isClone = null,
    Object? autoflower = null,
    Object? parentId = freezed,
    Object? imageUrl = freezed,
  }) {
    return _then(
      _$PlantCreateImpl(
        name: null == name
            ? _value.name
            : name // ignore: cast_nullable_to_non_nullable
                  as String,
        description: freezed == description
            ? _value.description
            : description // ignore: cast_nullable_to_non_nullable
                  as String?,
        statusId: null == statusId
            ? _value.statusId
            : statusId // ignore: cast_nullable_to_non_nullable
                  as int,
        cultivarId: freezed == cultivarId
            ? _value.cultivarId
            : cultivarId // ignore: cast_nullable_to_non_nullable
                  as int?,
        zoneId: freezed == zoneId
            ? _value.zoneId
            : zoneId // ignore: cast_nullable_to_non_nullable
                  as int?,
        isClone: null == isClone
            ? _value.isClone
            : isClone // ignore: cast_nullable_to_non_nullable
                  as bool,
        autoflower: null == autoflower
            ? _value.autoflower
            : autoflower // ignore: cast_nullable_to_non_nullable
                  as bool,
        parentId: freezed == parentId
            ? _value.parentId
            : parentId // ignore: cast_nullable_to_non_nullable
                  as int?,
        imageUrl: freezed == imageUrl
            ? _value.imageUrl
            : imageUrl // ignore: cast_nullable_to_non_nullable
                  as String?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$PlantCreateImpl implements _PlantCreate {
  const _$PlantCreateImpl({
    required this.name,
    this.description,
    @JsonKey(name: 'status_id') this.statusId = 1,
    @JsonKey(name: 'cultivar_id') this.cultivarId,
    @JsonKey(name: 'zone_id') this.zoneId,
    @JsonKey(name: 'is_clone') this.isClone = false,
    this.autoflower = false,
    @JsonKey(name: 'parent_id') this.parentId,
    @JsonKey(name: 'image_url') this.imageUrl,
  });

  factory _$PlantCreateImpl.fromJson(Map<String, dynamic> json) =>
      _$$PlantCreateImplFromJson(json);

  @override
  final String name;
  @override
  final String? description;
  @override
  @JsonKey(name: 'status_id')
  final int statusId;
  @override
  @JsonKey(name: 'cultivar_id')
  final int? cultivarId;
  @override
  @JsonKey(name: 'zone_id')
  final int? zoneId;
  @override
  @JsonKey(name: 'is_clone')
  final bool isClone;
  @override
  @JsonKey()
  final bool autoflower;
  @override
  @JsonKey(name: 'parent_id')
  final int? parentId;
  @override
  @JsonKey(name: 'image_url')
  final String? imageUrl;

  @override
  String toString() {
    return 'PlantCreate(name: $name, description: $description, statusId: $statusId, cultivarId: $cultivarId, zoneId: $zoneId, isClone: $isClone, autoflower: $autoflower, parentId: $parentId, imageUrl: $imageUrl)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PlantCreateImpl &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.statusId, statusId) ||
                other.statusId == statusId) &&
            (identical(other.cultivarId, cultivarId) ||
                other.cultivarId == cultivarId) &&
            (identical(other.zoneId, zoneId) || other.zoneId == zoneId) &&
            (identical(other.isClone, isClone) || other.isClone == isClone) &&
            (identical(other.autoflower, autoflower) ||
                other.autoflower == autoflower) &&
            (identical(other.parentId, parentId) ||
                other.parentId == parentId) &&
            (identical(other.imageUrl, imageUrl) ||
                other.imageUrl == imageUrl));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    name,
    description,
    statusId,
    cultivarId,
    zoneId,
    isClone,
    autoflower,
    parentId,
    imageUrl,
  );

  /// Create a copy of PlantCreate
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$PlantCreateImplCopyWith<_$PlantCreateImpl> get copyWith =>
      __$$PlantCreateImplCopyWithImpl<_$PlantCreateImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PlantCreateImplToJson(this);
  }
}

abstract class _PlantCreate implements PlantCreate {
  const factory _PlantCreate({
    required final String name,
    final String? description,
    @JsonKey(name: 'status_id') final int statusId,
    @JsonKey(name: 'cultivar_id') final int? cultivarId,
    @JsonKey(name: 'zone_id') final int? zoneId,
    @JsonKey(name: 'is_clone') final bool isClone,
    final bool autoflower,
    @JsonKey(name: 'parent_id') final int? parentId,
    @JsonKey(name: 'image_url') final String? imageUrl,
  }) = _$PlantCreateImpl;

  factory _PlantCreate.fromJson(Map<String, dynamic> json) =
      _$PlantCreateImpl.fromJson;

  @override
  String get name;
  @override
  String? get description;
  @override
  @JsonKey(name: 'status_id')
  int get statusId;
  @override
  @JsonKey(name: 'cultivar_id')
  int? get cultivarId;
  @override
  @JsonKey(name: 'zone_id')
  int? get zoneId;
  @override
  @JsonKey(name: 'is_clone')
  bool get isClone;
  @override
  bool get autoflower;
  @override
  @JsonKey(name: 'parent_id')
  int? get parentId;
  @override
  @JsonKey(name: 'image_url')
  String? get imageUrl;

  /// Create a copy of PlantCreate
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$PlantCreateImplCopyWith<_$PlantCreateImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

PlantUpdate _$PlantUpdateFromJson(Map<String, dynamic> json) {
  return _PlantUpdate.fromJson(json);
}

/// @nodoc
mixin _$PlantUpdate {
  String? get name => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  @JsonKey(name: 'status_id')
  int? get statusId => throw _privateConstructorUsedError;
  @JsonKey(name: 'cultivar_id')
  int? get cultivarId => throw _privateConstructorUsedError;
  @JsonKey(name: 'zone_id')
  int? get zoneId => throw _privateConstructorUsedError;
  @JsonKey(name: 'current_height')
  String? get currentHeight => throw _privateConstructorUsedError;
  @JsonKey(name: 'last_water_date')
  DateTime? get lastWaterDate => throw _privateConstructorUsedError;
  @JsonKey(name: 'last_feed_date')
  DateTime? get lastFeedDate => throw _privateConstructorUsedError;
  @JsonKey(name: 'is_clone')
  bool? get isClone => throw _privateConstructorUsedError;
  @JsonKey(name: 'start_dt')
  DateTime? get startDt => throw _privateConstructorUsedError;
  @JsonKey(name: 'harvest_weight')
  double? get harvestWeight => throw _privateConstructorUsedError;
  @JsonKey(name: 'harvest_date')
  DateTime? get harvestDate => throw _privateConstructorUsedError;
  @JsonKey(name: 'est_harvest_date')
  DateTime? get estHarvestDate => throw _privateConstructorUsedError;
  bool? get autoflower => throw _privateConstructorUsedError;
  @JsonKey(name: 'parent_id')
  int? get parentId => throw _privateConstructorUsedError;
  @JsonKey(name: 'image_url')
  String? get imageUrl => throw _privateConstructorUsedError;

  /// Serializes this PlantUpdate to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of PlantUpdate
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $PlantUpdateCopyWith<PlantUpdate> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PlantUpdateCopyWith<$Res> {
  factory $PlantUpdateCopyWith(
    PlantUpdate value,
    $Res Function(PlantUpdate) then,
  ) = _$PlantUpdateCopyWithImpl<$Res, PlantUpdate>;
  @useResult
  $Res call({
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
  });
}

/// @nodoc
class _$PlantUpdateCopyWithImpl<$Res, $Val extends PlantUpdate>
    implements $PlantUpdateCopyWith<$Res> {
  _$PlantUpdateCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of PlantUpdate
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? name = freezed,
    Object? description = freezed,
    Object? statusId = freezed,
    Object? cultivarId = freezed,
    Object? zoneId = freezed,
    Object? currentHeight = freezed,
    Object? lastWaterDate = freezed,
    Object? lastFeedDate = freezed,
    Object? isClone = freezed,
    Object? startDt = freezed,
    Object? harvestWeight = freezed,
    Object? harvestDate = freezed,
    Object? estHarvestDate = freezed,
    Object? autoflower = freezed,
    Object? parentId = freezed,
    Object? imageUrl = freezed,
  }) {
    return _then(
      _value.copyWith(
            name: freezed == name
                ? _value.name
                : name // ignore: cast_nullable_to_non_nullable
                      as String?,
            description: freezed == description
                ? _value.description
                : description // ignore: cast_nullable_to_non_nullable
                      as String?,
            statusId: freezed == statusId
                ? _value.statusId
                : statusId // ignore: cast_nullable_to_non_nullable
                      as int?,
            cultivarId: freezed == cultivarId
                ? _value.cultivarId
                : cultivarId // ignore: cast_nullable_to_non_nullable
                      as int?,
            zoneId: freezed == zoneId
                ? _value.zoneId
                : zoneId // ignore: cast_nullable_to_non_nullable
                      as int?,
            currentHeight: freezed == currentHeight
                ? _value.currentHeight
                : currentHeight // ignore: cast_nullable_to_non_nullable
                      as String?,
            lastWaterDate: freezed == lastWaterDate
                ? _value.lastWaterDate
                : lastWaterDate // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            lastFeedDate: freezed == lastFeedDate
                ? _value.lastFeedDate
                : lastFeedDate // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            isClone: freezed == isClone
                ? _value.isClone
                : isClone // ignore: cast_nullable_to_non_nullable
                      as bool?,
            startDt: freezed == startDt
                ? _value.startDt
                : startDt // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            harvestWeight: freezed == harvestWeight
                ? _value.harvestWeight
                : harvestWeight // ignore: cast_nullable_to_non_nullable
                      as double?,
            harvestDate: freezed == harvestDate
                ? _value.harvestDate
                : harvestDate // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            estHarvestDate: freezed == estHarvestDate
                ? _value.estHarvestDate
                : estHarvestDate // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            autoflower: freezed == autoflower
                ? _value.autoflower
                : autoflower // ignore: cast_nullable_to_non_nullable
                      as bool?,
            parentId: freezed == parentId
                ? _value.parentId
                : parentId // ignore: cast_nullable_to_non_nullable
                      as int?,
            imageUrl: freezed == imageUrl
                ? _value.imageUrl
                : imageUrl // ignore: cast_nullable_to_non_nullable
                      as String?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$PlantUpdateImplCopyWith<$Res>
    implements $PlantUpdateCopyWith<$Res> {
  factory _$$PlantUpdateImplCopyWith(
    _$PlantUpdateImpl value,
    $Res Function(_$PlantUpdateImpl) then,
  ) = __$$PlantUpdateImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
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
  });
}

/// @nodoc
class __$$PlantUpdateImplCopyWithImpl<$Res>
    extends _$PlantUpdateCopyWithImpl<$Res, _$PlantUpdateImpl>
    implements _$$PlantUpdateImplCopyWith<$Res> {
  __$$PlantUpdateImplCopyWithImpl(
    _$PlantUpdateImpl _value,
    $Res Function(_$PlantUpdateImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of PlantUpdate
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? name = freezed,
    Object? description = freezed,
    Object? statusId = freezed,
    Object? cultivarId = freezed,
    Object? zoneId = freezed,
    Object? currentHeight = freezed,
    Object? lastWaterDate = freezed,
    Object? lastFeedDate = freezed,
    Object? isClone = freezed,
    Object? startDt = freezed,
    Object? harvestWeight = freezed,
    Object? harvestDate = freezed,
    Object? estHarvestDate = freezed,
    Object? autoflower = freezed,
    Object? parentId = freezed,
    Object? imageUrl = freezed,
  }) {
    return _then(
      _$PlantUpdateImpl(
        name: freezed == name
            ? _value.name
            : name // ignore: cast_nullable_to_non_nullable
                  as String?,
        description: freezed == description
            ? _value.description
            : description // ignore: cast_nullable_to_non_nullable
                  as String?,
        statusId: freezed == statusId
            ? _value.statusId
            : statusId // ignore: cast_nullable_to_non_nullable
                  as int?,
        cultivarId: freezed == cultivarId
            ? _value.cultivarId
            : cultivarId // ignore: cast_nullable_to_non_nullable
                  as int?,
        zoneId: freezed == zoneId
            ? _value.zoneId
            : zoneId // ignore: cast_nullable_to_non_nullable
                  as int?,
        currentHeight: freezed == currentHeight
            ? _value.currentHeight
            : currentHeight // ignore: cast_nullable_to_non_nullable
                  as String?,
        lastWaterDate: freezed == lastWaterDate
            ? _value.lastWaterDate
            : lastWaterDate // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        lastFeedDate: freezed == lastFeedDate
            ? _value.lastFeedDate
            : lastFeedDate // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        isClone: freezed == isClone
            ? _value.isClone
            : isClone // ignore: cast_nullable_to_non_nullable
                  as bool?,
        startDt: freezed == startDt
            ? _value.startDt
            : startDt // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        harvestWeight: freezed == harvestWeight
            ? _value.harvestWeight
            : harvestWeight // ignore: cast_nullable_to_non_nullable
                  as double?,
        harvestDate: freezed == harvestDate
            ? _value.harvestDate
            : harvestDate // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        estHarvestDate: freezed == estHarvestDate
            ? _value.estHarvestDate
            : estHarvestDate // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        autoflower: freezed == autoflower
            ? _value.autoflower
            : autoflower // ignore: cast_nullable_to_non_nullable
                  as bool?,
        parentId: freezed == parentId
            ? _value.parentId
            : parentId // ignore: cast_nullable_to_non_nullable
                  as int?,
        imageUrl: freezed == imageUrl
            ? _value.imageUrl
            : imageUrl // ignore: cast_nullable_to_non_nullable
                  as String?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$PlantUpdateImpl implements _PlantUpdate {
  const _$PlantUpdateImpl({
    this.name,
    this.description,
    @JsonKey(name: 'status_id') this.statusId,
    @JsonKey(name: 'cultivar_id') this.cultivarId,
    @JsonKey(name: 'zone_id') this.zoneId,
    @JsonKey(name: 'current_height') this.currentHeight,
    @JsonKey(name: 'last_water_date') this.lastWaterDate,
    @JsonKey(name: 'last_feed_date') this.lastFeedDate,
    @JsonKey(name: 'is_clone') this.isClone,
    @JsonKey(name: 'start_dt') this.startDt,
    @JsonKey(name: 'harvest_weight') this.harvestWeight,
    @JsonKey(name: 'harvest_date') this.harvestDate,
    @JsonKey(name: 'est_harvest_date') this.estHarvestDate,
    this.autoflower,
    @JsonKey(name: 'parent_id') this.parentId,
    @JsonKey(name: 'image_url') this.imageUrl,
  });

  factory _$PlantUpdateImpl.fromJson(Map<String, dynamic> json) =>
      _$$PlantUpdateImplFromJson(json);

  @override
  final String? name;
  @override
  final String? description;
  @override
  @JsonKey(name: 'status_id')
  final int? statusId;
  @override
  @JsonKey(name: 'cultivar_id')
  final int? cultivarId;
  @override
  @JsonKey(name: 'zone_id')
  final int? zoneId;
  @override
  @JsonKey(name: 'current_height')
  final String? currentHeight;
  @override
  @JsonKey(name: 'last_water_date')
  final DateTime? lastWaterDate;
  @override
  @JsonKey(name: 'last_feed_date')
  final DateTime? lastFeedDate;
  @override
  @JsonKey(name: 'is_clone')
  final bool? isClone;
  @override
  @JsonKey(name: 'start_dt')
  final DateTime? startDt;
  @override
  @JsonKey(name: 'harvest_weight')
  final double? harvestWeight;
  @override
  @JsonKey(name: 'harvest_date')
  final DateTime? harvestDate;
  @override
  @JsonKey(name: 'est_harvest_date')
  final DateTime? estHarvestDate;
  @override
  final bool? autoflower;
  @override
  @JsonKey(name: 'parent_id')
  final int? parentId;
  @override
  @JsonKey(name: 'image_url')
  final String? imageUrl;

  @override
  String toString() {
    return 'PlantUpdate(name: $name, description: $description, statusId: $statusId, cultivarId: $cultivarId, zoneId: $zoneId, currentHeight: $currentHeight, lastWaterDate: $lastWaterDate, lastFeedDate: $lastFeedDate, isClone: $isClone, startDt: $startDt, harvestWeight: $harvestWeight, harvestDate: $harvestDate, estHarvestDate: $estHarvestDate, autoflower: $autoflower, parentId: $parentId, imageUrl: $imageUrl)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PlantUpdateImpl &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.statusId, statusId) ||
                other.statusId == statusId) &&
            (identical(other.cultivarId, cultivarId) ||
                other.cultivarId == cultivarId) &&
            (identical(other.zoneId, zoneId) || other.zoneId == zoneId) &&
            (identical(other.currentHeight, currentHeight) ||
                other.currentHeight == currentHeight) &&
            (identical(other.lastWaterDate, lastWaterDate) ||
                other.lastWaterDate == lastWaterDate) &&
            (identical(other.lastFeedDate, lastFeedDate) ||
                other.lastFeedDate == lastFeedDate) &&
            (identical(other.isClone, isClone) || other.isClone == isClone) &&
            (identical(other.startDt, startDt) || other.startDt == startDt) &&
            (identical(other.harvestWeight, harvestWeight) ||
                other.harvestWeight == harvestWeight) &&
            (identical(other.harvestDate, harvestDate) ||
                other.harvestDate == harvestDate) &&
            (identical(other.estHarvestDate, estHarvestDate) ||
                other.estHarvestDate == estHarvestDate) &&
            (identical(other.autoflower, autoflower) ||
                other.autoflower == autoflower) &&
            (identical(other.parentId, parentId) ||
                other.parentId == parentId) &&
            (identical(other.imageUrl, imageUrl) ||
                other.imageUrl == imageUrl));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    name,
    description,
    statusId,
    cultivarId,
    zoneId,
    currentHeight,
    lastWaterDate,
    lastFeedDate,
    isClone,
    startDt,
    harvestWeight,
    harvestDate,
    estHarvestDate,
    autoflower,
    parentId,
    imageUrl,
  );

  /// Create a copy of PlantUpdate
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$PlantUpdateImplCopyWith<_$PlantUpdateImpl> get copyWith =>
      __$$PlantUpdateImplCopyWithImpl<_$PlantUpdateImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PlantUpdateImplToJson(this);
  }
}

abstract class _PlantUpdate implements PlantUpdate {
  const factory _PlantUpdate({
    final String? name,
    final String? description,
    @JsonKey(name: 'status_id') final int? statusId,
    @JsonKey(name: 'cultivar_id') final int? cultivarId,
    @JsonKey(name: 'zone_id') final int? zoneId,
    @JsonKey(name: 'current_height') final String? currentHeight,
    @JsonKey(name: 'last_water_date') final DateTime? lastWaterDate,
    @JsonKey(name: 'last_feed_date') final DateTime? lastFeedDate,
    @JsonKey(name: 'is_clone') final bool? isClone,
    @JsonKey(name: 'start_dt') final DateTime? startDt,
    @JsonKey(name: 'harvest_weight') final double? harvestWeight,
    @JsonKey(name: 'harvest_date') final DateTime? harvestDate,
    @JsonKey(name: 'est_harvest_date') final DateTime? estHarvestDate,
    final bool? autoflower,
    @JsonKey(name: 'parent_id') final int? parentId,
    @JsonKey(name: 'image_url') final String? imageUrl,
  }) = _$PlantUpdateImpl;

  factory _PlantUpdate.fromJson(Map<String, dynamic> json) =
      _$PlantUpdateImpl.fromJson;

  @override
  String? get name;
  @override
  String? get description;
  @override
  @JsonKey(name: 'status_id')
  int? get statusId;
  @override
  @JsonKey(name: 'cultivar_id')
  int? get cultivarId;
  @override
  @JsonKey(name: 'zone_id')
  int? get zoneId;
  @override
  @JsonKey(name: 'current_height')
  String? get currentHeight;
  @override
  @JsonKey(name: 'last_water_date')
  DateTime? get lastWaterDate;
  @override
  @JsonKey(name: 'last_feed_date')
  DateTime? get lastFeedDate;
  @override
  @JsonKey(name: 'is_clone')
  bool? get isClone;
  @override
  @JsonKey(name: 'start_dt')
  DateTime? get startDt;
  @override
  @JsonKey(name: 'harvest_weight')
  double? get harvestWeight;
  @override
  @JsonKey(name: 'harvest_date')
  DateTime? get harvestDate;
  @override
  @JsonKey(name: 'est_harvest_date')
  DateTime? get estHarvestDate;
  @override
  bool? get autoflower;
  @override
  @JsonKey(name: 'parent_id')
  int? get parentId;
  @override
  @JsonKey(name: 'image_url')
  String? get imageUrl;

  /// Create a copy of PlantUpdate
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$PlantUpdateImplCopyWith<_$PlantUpdateImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

PaginatedPlantsResponse _$PaginatedPlantsResponseFromJson(
  Map<String, dynamic> json,
) {
  return _PaginatedPlantsResponse.fromJson(json);
}

/// @nodoc
mixin _$PaginatedPlantsResponse {
  List<Plant> get items => throw _privateConstructorUsedError;
  int get total => throw _privateConstructorUsedError;
  int get page => throw _privateConstructorUsedError;
  @JsonKey(name: 'page_size')
  int get limit => throw _privateConstructorUsedError;
  int get pages => throw _privateConstructorUsedError;
  @JsonKey(name: 'has_next')
  bool get hasNext => throw _privateConstructorUsedError;
  @JsonKey(name: 'has_prev')
  bool get hasPrev => throw _privateConstructorUsedError;

  /// Serializes this PaginatedPlantsResponse to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of PaginatedPlantsResponse
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $PaginatedPlantsResponseCopyWith<PaginatedPlantsResponse> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PaginatedPlantsResponseCopyWith<$Res> {
  factory $PaginatedPlantsResponseCopyWith(
    PaginatedPlantsResponse value,
    $Res Function(PaginatedPlantsResponse) then,
  ) = _$PaginatedPlantsResponseCopyWithImpl<$Res, PaginatedPlantsResponse>;
  @useResult
  $Res call({
    List<Plant> items,
    int total,
    int page,
    @JsonKey(name: 'page_size') int limit,
    int pages,
    @JsonKey(name: 'has_next') bool hasNext,
    @JsonKey(name: 'has_prev') bool hasPrev,
  });
}

/// @nodoc
class _$PaginatedPlantsResponseCopyWithImpl<
  $Res,
  $Val extends PaginatedPlantsResponse
>
    implements $PaginatedPlantsResponseCopyWith<$Res> {
  _$PaginatedPlantsResponseCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of PaginatedPlantsResponse
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? items = null,
    Object? total = null,
    Object? page = null,
    Object? limit = null,
    Object? pages = null,
    Object? hasNext = null,
    Object? hasPrev = null,
  }) {
    return _then(
      _value.copyWith(
            items: null == items
                ? _value.items
                : items // ignore: cast_nullable_to_non_nullable
                      as List<Plant>,
            total: null == total
                ? _value.total
                : total // ignore: cast_nullable_to_non_nullable
                      as int,
            page: null == page
                ? _value.page
                : page // ignore: cast_nullable_to_non_nullable
                      as int,
            limit: null == limit
                ? _value.limit
                : limit // ignore: cast_nullable_to_non_nullable
                      as int,
            pages: null == pages
                ? _value.pages
                : pages // ignore: cast_nullable_to_non_nullable
                      as int,
            hasNext: null == hasNext
                ? _value.hasNext
                : hasNext // ignore: cast_nullable_to_non_nullable
                      as bool,
            hasPrev: null == hasPrev
                ? _value.hasPrev
                : hasPrev // ignore: cast_nullable_to_non_nullable
                      as bool,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$PaginatedPlantsResponseImplCopyWith<$Res>
    implements $PaginatedPlantsResponseCopyWith<$Res> {
  factory _$$PaginatedPlantsResponseImplCopyWith(
    _$PaginatedPlantsResponseImpl value,
    $Res Function(_$PaginatedPlantsResponseImpl) then,
  ) = __$$PaginatedPlantsResponseImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    List<Plant> items,
    int total,
    int page,
    @JsonKey(name: 'page_size') int limit,
    int pages,
    @JsonKey(name: 'has_next') bool hasNext,
    @JsonKey(name: 'has_prev') bool hasPrev,
  });
}

/// @nodoc
class __$$PaginatedPlantsResponseImplCopyWithImpl<$Res>
    extends
        _$PaginatedPlantsResponseCopyWithImpl<
          $Res,
          _$PaginatedPlantsResponseImpl
        >
    implements _$$PaginatedPlantsResponseImplCopyWith<$Res> {
  __$$PaginatedPlantsResponseImplCopyWithImpl(
    _$PaginatedPlantsResponseImpl _value,
    $Res Function(_$PaginatedPlantsResponseImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of PaginatedPlantsResponse
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? items = null,
    Object? total = null,
    Object? page = null,
    Object? limit = null,
    Object? pages = null,
    Object? hasNext = null,
    Object? hasPrev = null,
  }) {
    return _then(
      _$PaginatedPlantsResponseImpl(
        items: null == items
            ? _value._items
            : items // ignore: cast_nullable_to_non_nullable
                  as List<Plant>,
        total: null == total
            ? _value.total
            : total // ignore: cast_nullable_to_non_nullable
                  as int,
        page: null == page
            ? _value.page
            : page // ignore: cast_nullable_to_non_nullable
                  as int,
        limit: null == limit
            ? _value.limit
            : limit // ignore: cast_nullable_to_non_nullable
                  as int,
        pages: null == pages
            ? _value.pages
            : pages // ignore: cast_nullable_to_non_nullable
                  as int,
        hasNext: null == hasNext
            ? _value.hasNext
            : hasNext // ignore: cast_nullable_to_non_nullable
                  as bool,
        hasPrev: null == hasPrev
            ? _value.hasPrev
            : hasPrev // ignore: cast_nullable_to_non_nullable
                  as bool,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$PaginatedPlantsResponseImpl implements _PaginatedPlantsResponse {
  const _$PaginatedPlantsResponseImpl({
    final List<Plant> items = const [],
    this.total = 0,
    this.page = 1,
    @JsonKey(name: 'page_size') this.limit = 20,
    this.pages = 0,
    @JsonKey(name: 'has_next') this.hasNext = false,
    @JsonKey(name: 'has_prev') this.hasPrev = false,
  }) : _items = items;

  factory _$PaginatedPlantsResponseImpl.fromJson(Map<String, dynamic> json) =>
      _$$PaginatedPlantsResponseImplFromJson(json);

  final List<Plant> _items;
  @override
  @JsonKey()
  List<Plant> get items {
    if (_items is EqualUnmodifiableListView) return _items;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_items);
  }

  @override
  @JsonKey()
  final int total;
  @override
  @JsonKey()
  final int page;
  @override
  @JsonKey(name: 'page_size')
  final int limit;
  @override
  @JsonKey()
  final int pages;
  @override
  @JsonKey(name: 'has_next')
  final bool hasNext;
  @override
  @JsonKey(name: 'has_prev')
  final bool hasPrev;

  @override
  String toString() {
    return 'PaginatedPlantsResponse(items: $items, total: $total, page: $page, limit: $limit, pages: $pages, hasNext: $hasNext, hasPrev: $hasPrev)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PaginatedPlantsResponseImpl &&
            const DeepCollectionEquality().equals(other._items, _items) &&
            (identical(other.total, total) || other.total == total) &&
            (identical(other.page, page) || other.page == page) &&
            (identical(other.limit, limit) || other.limit == limit) &&
            (identical(other.pages, pages) || other.pages == pages) &&
            (identical(other.hasNext, hasNext) || other.hasNext == hasNext) &&
            (identical(other.hasPrev, hasPrev) || other.hasPrev == hasPrev));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    const DeepCollectionEquality().hash(_items),
    total,
    page,
    limit,
    pages,
    hasNext,
    hasPrev,
  );

  /// Create a copy of PaginatedPlantsResponse
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$PaginatedPlantsResponseImplCopyWith<_$PaginatedPlantsResponseImpl>
  get copyWith =>
      __$$PaginatedPlantsResponseImplCopyWithImpl<
        _$PaginatedPlantsResponseImpl
      >(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PaginatedPlantsResponseImplToJson(this);
  }
}

abstract class _PaginatedPlantsResponse implements PaginatedPlantsResponse {
  const factory _PaginatedPlantsResponse({
    final List<Plant> items,
    final int total,
    final int page,
    @JsonKey(name: 'page_size') final int limit,
    final int pages,
    @JsonKey(name: 'has_next') final bool hasNext,
    @JsonKey(name: 'has_prev') final bool hasPrev,
  }) = _$PaginatedPlantsResponseImpl;

  factory _PaginatedPlantsResponse.fromJson(Map<String, dynamic> json) =
      _$PaginatedPlantsResponseImpl.fromJson;

  @override
  List<Plant> get items;
  @override
  int get total;
  @override
  int get page;
  @override
  @JsonKey(name: 'page_size')
  int get limit;
  @override
  int get pages;
  @override
  @JsonKey(name: 'has_next')
  bool get hasNext;
  @override
  @JsonKey(name: 'has_prev')
  bool get hasPrev;

  /// Create a copy of PaginatedPlantsResponse
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$PaginatedPlantsResponseImplCopyWith<_$PaginatedPlantsResponseImpl>
  get copyWith => throw _privateConstructorUsedError;
}
