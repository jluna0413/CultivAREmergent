// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'plant.dart';

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
  String get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  PlantStage get stage => throw _privateConstructorUsedError;
  PlantStatus get status => throw _privateConstructorUsedError;
  PlantHealth get health => throw _privateConstructorUsedError;
  DateTime get plantedDate => throw _privateConstructorUsedError;
  DateTime? get harvestDate => throw _privateConstructorUsedError;
  String? get strain => throw _privateConstructorUsedError;
  String? get notes => throw _privateConstructorUsedError;
  Map<String, dynamic>? get metrics => throw _privateConstructorUsedError;

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
    String id,
    String name,
    PlantStage stage,
    PlantStatus status,
    PlantHealth health,
    DateTime plantedDate,
    DateTime? harvestDate,
    String? strain,
    String? notes,
    Map<String, dynamic>? metrics,
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
    Object? name = null,
    Object? stage = null,
    Object? status = null,
    Object? health = null,
    Object? plantedDate = null,
    Object? harvestDate = freezed,
    Object? strain = freezed,
    Object? notes = freezed,
    Object? metrics = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as String,
            name: null == name
                ? _value.name
                : name // ignore: cast_nullable_to_non_nullable
                      as String,
            stage: null == stage
                ? _value.stage
                : stage // ignore: cast_nullable_to_non_nullable
                      as PlantStage,
            status: null == status
                ? _value.status
                : status // ignore: cast_nullable_to_non_nullable
                      as PlantStatus,
            health: null == health
                ? _value.health
                : health // ignore: cast_nullable_to_non_nullable
                      as PlantHealth,
            plantedDate: null == plantedDate
                ? _value.plantedDate
                : plantedDate // ignore: cast_nullable_to_non_nullable
                      as DateTime,
            harvestDate: freezed == harvestDate
                ? _value.harvestDate
                : harvestDate // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            strain: freezed == strain
                ? _value.strain
                : strain // ignore: cast_nullable_to_non_nullable
                      as String?,
            notes: freezed == notes
                ? _value.notes
                : notes // ignore: cast_nullable_to_non_nullable
                      as String?,
            metrics: freezed == metrics
                ? _value.metrics
                : metrics // ignore: cast_nullable_to_non_nullable
                      as Map<String, dynamic>?,
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
    String id,
    String name,
    PlantStage stage,
    PlantStatus status,
    PlantHealth health,
    DateTime plantedDate,
    DateTime? harvestDate,
    String? strain,
    String? notes,
    Map<String, dynamic>? metrics,
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
    Object? name = null,
    Object? stage = null,
    Object? status = null,
    Object? health = null,
    Object? plantedDate = null,
    Object? harvestDate = freezed,
    Object? strain = freezed,
    Object? notes = freezed,
    Object? metrics = freezed,
  }) {
    return _then(
      _$PlantImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as String,
        name: null == name
            ? _value.name
            : name // ignore: cast_nullable_to_non_nullable
                  as String,
        stage: null == stage
            ? _value.stage
            : stage // ignore: cast_nullable_to_non_nullable
                  as PlantStage,
        status: null == status
            ? _value.status
            : status // ignore: cast_nullable_to_non_nullable
                  as PlantStatus,
        health: null == health
            ? _value.health
            : health // ignore: cast_nullable_to_non_nullable
                  as PlantHealth,
        plantedDate: null == plantedDate
            ? _value.plantedDate
            : plantedDate // ignore: cast_nullable_to_non_nullable
                  as DateTime,
        harvestDate: freezed == harvestDate
            ? _value.harvestDate
            : harvestDate // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        strain: freezed == strain
            ? _value.strain
            : strain // ignore: cast_nullable_to_non_nullable
                  as String?,
        notes: freezed == notes
            ? _value.notes
            : notes // ignore: cast_nullable_to_non_nullable
                  as String?,
        metrics: freezed == metrics
            ? _value._metrics
            : metrics // ignore: cast_nullable_to_non_nullable
                  as Map<String, dynamic>?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$PlantImpl implements _Plant {
  const _$PlantImpl({
    required this.id,
    required this.name,
    required this.stage,
    required this.status,
    required this.health,
    required this.plantedDate,
    this.harvestDate,
    this.strain,
    this.notes,
    final Map<String, dynamic>? metrics,
  }) : _metrics = metrics;

  factory _$PlantImpl.fromJson(Map<String, dynamic> json) =>
      _$$PlantImplFromJson(json);

  @override
  final String id;
  @override
  final String name;
  @override
  final PlantStage stage;
  @override
  final PlantStatus status;
  @override
  final PlantHealth health;
  @override
  final DateTime plantedDate;
  @override
  final DateTime? harvestDate;
  @override
  final String? strain;
  @override
  final String? notes;
  final Map<String, dynamic>? _metrics;
  @override
  Map<String, dynamic>? get metrics {
    final value = _metrics;
    if (value == null) return null;
    if (_metrics is EqualUnmodifiableMapView) return _metrics;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(value);
  }

  @override
  String toString() {
    return 'Plant(id: $id, name: $name, stage: $stage, status: $status, health: $health, plantedDate: $plantedDate, harvestDate: $harvestDate, strain: $strain, notes: $notes, metrics: $metrics)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PlantImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.stage, stage) || other.stage == stage) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.health, health) || other.health == health) &&
            (identical(other.plantedDate, plantedDate) ||
                other.plantedDate == plantedDate) &&
            (identical(other.harvestDate, harvestDate) ||
                other.harvestDate == harvestDate) &&
            (identical(other.strain, strain) || other.strain == strain) &&
            (identical(other.notes, notes) || other.notes == notes) &&
            const DeepCollectionEquality().equals(other._metrics, _metrics));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    name,
    stage,
    status,
    health,
    plantedDate,
    harvestDate,
    strain,
    notes,
    const DeepCollectionEquality().hash(_metrics),
  );

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
    required final String id,
    required final String name,
    required final PlantStage stage,
    required final PlantStatus status,
    required final PlantHealth health,
    required final DateTime plantedDate,
    final DateTime? harvestDate,
    final String? strain,
    final String? notes,
    final Map<String, dynamic>? metrics,
  }) = _$PlantImpl;

  factory _Plant.fromJson(Map<String, dynamic> json) = _$PlantImpl.fromJson;

  @override
  String get id;
  @override
  String get name;
  @override
  PlantStage get stage;
  @override
  PlantStatus get status;
  @override
  PlantHealth get health;
  @override
  DateTime get plantedDate;
  @override
  DateTime? get harvestDate;
  @override
  String? get strain;
  @override
  String? get notes;
  @override
  Map<String, dynamic>? get metrics;

  /// Create a copy of Plant
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$PlantImplCopyWith<_$PlantImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
