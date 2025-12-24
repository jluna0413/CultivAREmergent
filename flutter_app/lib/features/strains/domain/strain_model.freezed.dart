// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'strain_model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

Cultivar _$CultivarFromJson(Map<String, dynamic> json) {
  return _Cultivar.fromJson(json);
}

/// @nodoc
mixin _$Cultivar {
  int get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  String? get genetics => throw _privateConstructorUsedError;
  int? get breederId => throw _privateConstructorUsedError;
  String? get breederName => throw _privateConstructorUsedError;
  int? get indica => throw _privateConstructorUsedError;
  int? get sativa => throw _privateConstructorUsedError;
  int? get ruderalis => throw _privateConstructorUsedError;
  String? get floweringType => throw _privateConstructorUsedError;
  int? get floweringDays => throw _privateConstructorUsedError;
  int? get yieldIndoor => throw _privateConstructorUsedError;
  int? get yieldOutdoor => throw _privateConstructorUsedError;
  String? get difficulty => throw _privateConstructorUsedError;
  String? get imageUrl => throw _privateConstructorUsedError;
  DateTime? get createdAt => throw _privateConstructorUsedError;
  DateTime? get updatedAt => throw _privateConstructorUsedError;

  /// Serializes this Cultivar to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of Cultivar
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $CultivarCopyWith<Cultivar> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $CultivarCopyWith<$Res> {
  factory $CultivarCopyWith(Cultivar value, $Res Function(Cultivar) then) =
      _$CultivarCopyWithImpl<$Res, Cultivar>;
  @useResult
  $Res call({
    int id,
    String name,
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
  });
}

/// @nodoc
class _$CultivarCopyWithImpl<$Res, $Val extends Cultivar>
    implements $CultivarCopyWith<$Res> {
  _$CultivarCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of Cultivar
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? description = freezed,
    Object? genetics = freezed,
    Object? breederId = freezed,
    Object? breederName = freezed,
    Object? indica = freezed,
    Object? sativa = freezed,
    Object? ruderalis = freezed,
    Object? floweringType = freezed,
    Object? floweringDays = freezed,
    Object? yieldIndoor = freezed,
    Object? yieldOutdoor = freezed,
    Object? difficulty = freezed,
    Object? imageUrl = freezed,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as int,
            name: null == name
                ? _value.name
                : name // ignore: cast_nullable_to_non_nullable
                      as String,
            description: freezed == description
                ? _value.description
                : description // ignore: cast_nullable_to_non_nullable
                      as String?,
            genetics: freezed == genetics
                ? _value.genetics
                : genetics // ignore: cast_nullable_to_non_nullable
                      as String?,
            breederId: freezed == breederId
                ? _value.breederId
                : breederId // ignore: cast_nullable_to_non_nullable
                      as int?,
            breederName: freezed == breederName
                ? _value.breederName
                : breederName // ignore: cast_nullable_to_non_nullable
                      as String?,
            indica: freezed == indica
                ? _value.indica
                : indica // ignore: cast_nullable_to_non_nullable
                      as int?,
            sativa: freezed == sativa
                ? _value.sativa
                : sativa // ignore: cast_nullable_to_non_nullable
                      as int?,
            ruderalis: freezed == ruderalis
                ? _value.ruderalis
                : ruderalis // ignore: cast_nullable_to_non_nullable
                      as int?,
            floweringType: freezed == floweringType
                ? _value.floweringType
                : floweringType // ignore: cast_nullable_to_non_nullable
                      as String?,
            floweringDays: freezed == floweringDays
                ? _value.floweringDays
                : floweringDays // ignore: cast_nullable_to_non_nullable
                      as int?,
            yieldIndoor: freezed == yieldIndoor
                ? _value.yieldIndoor
                : yieldIndoor // ignore: cast_nullable_to_non_nullable
                      as int?,
            yieldOutdoor: freezed == yieldOutdoor
                ? _value.yieldOutdoor
                : yieldOutdoor // ignore: cast_nullable_to_non_nullable
                      as int?,
            difficulty: freezed == difficulty
                ? _value.difficulty
                : difficulty // ignore: cast_nullable_to_non_nullable
                      as String?,
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
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$CultivarImplCopyWith<$Res>
    implements $CultivarCopyWith<$Res> {
  factory _$$CultivarImplCopyWith(
    _$CultivarImpl value,
    $Res Function(_$CultivarImpl) then,
  ) = __$$CultivarImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    int id,
    String name,
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
  });
}

/// @nodoc
class __$$CultivarImplCopyWithImpl<$Res>
    extends _$CultivarCopyWithImpl<$Res, _$CultivarImpl>
    implements _$$CultivarImplCopyWith<$Res> {
  __$$CultivarImplCopyWithImpl(
    _$CultivarImpl _value,
    $Res Function(_$CultivarImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of Cultivar
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? description = freezed,
    Object? genetics = freezed,
    Object? breederId = freezed,
    Object? breederName = freezed,
    Object? indica = freezed,
    Object? sativa = freezed,
    Object? ruderalis = freezed,
    Object? floweringType = freezed,
    Object? floweringDays = freezed,
    Object? yieldIndoor = freezed,
    Object? yieldOutdoor = freezed,
    Object? difficulty = freezed,
    Object? imageUrl = freezed,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(
      _$CultivarImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as int,
        name: null == name
            ? _value.name
            : name // ignore: cast_nullable_to_non_nullable
                  as String,
        description: freezed == description
            ? _value.description
            : description // ignore: cast_nullable_to_non_nullable
                  as String?,
        genetics: freezed == genetics
            ? _value.genetics
            : genetics // ignore: cast_nullable_to_non_nullable
                  as String?,
        breederId: freezed == breederId
            ? _value.breederId
            : breederId // ignore: cast_nullable_to_non_nullable
                  as int?,
        breederName: freezed == breederName
            ? _value.breederName
            : breederName // ignore: cast_nullable_to_non_nullable
                  as String?,
        indica: freezed == indica
            ? _value.indica
            : indica // ignore: cast_nullable_to_non_nullable
                  as int?,
        sativa: freezed == sativa
            ? _value.sativa
            : sativa // ignore: cast_nullable_to_non_nullable
                  as int?,
        ruderalis: freezed == ruderalis
            ? _value.ruderalis
            : ruderalis // ignore: cast_nullable_to_non_nullable
                  as int?,
        floweringType: freezed == floweringType
            ? _value.floweringType
            : floweringType // ignore: cast_nullable_to_non_nullable
                  as String?,
        floweringDays: freezed == floweringDays
            ? _value.floweringDays
            : floweringDays // ignore: cast_nullable_to_non_nullable
                  as int?,
        yieldIndoor: freezed == yieldIndoor
            ? _value.yieldIndoor
            : yieldIndoor // ignore: cast_nullable_to_non_nullable
                  as int?,
        yieldOutdoor: freezed == yieldOutdoor
            ? _value.yieldOutdoor
            : yieldOutdoor // ignore: cast_nullable_to_non_nullable
                  as int?,
        difficulty: freezed == difficulty
            ? _value.difficulty
            : difficulty // ignore: cast_nullable_to_non_nullable
                  as String?,
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
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$CultivarImpl implements _Cultivar {
  const _$CultivarImpl({
    required this.id,
    required this.name,
    this.description,
    this.genetics,
    this.breederId,
    this.breederName,
    this.indica,
    this.sativa,
    this.ruderalis,
    this.floweringType,
    this.floweringDays,
    this.yieldIndoor,
    this.yieldOutdoor,
    this.difficulty,
    this.imageUrl,
    this.createdAt,
    this.updatedAt,
  });

  factory _$CultivarImpl.fromJson(Map<String, dynamic> json) =>
      _$$CultivarImplFromJson(json);

  @override
  final int id;
  @override
  final String name;
  @override
  final String? description;
  @override
  final String? genetics;
  @override
  final int? breederId;
  @override
  final String? breederName;
  @override
  final int? indica;
  @override
  final int? sativa;
  @override
  final int? ruderalis;
  @override
  final String? floweringType;
  @override
  final int? floweringDays;
  @override
  final int? yieldIndoor;
  @override
  final int? yieldOutdoor;
  @override
  final String? difficulty;
  @override
  final String? imageUrl;
  @override
  final DateTime? createdAt;
  @override
  final DateTime? updatedAt;

  @override
  String toString() {
    return 'Cultivar(id: $id, name: $name, description: $description, genetics: $genetics, breederId: $breederId, breederName: $breederName, indica: $indica, sativa: $sativa, ruderalis: $ruderalis, floweringType: $floweringType, floweringDays: $floweringDays, yieldIndoor: $yieldIndoor, yieldOutdoor: $yieldOutdoor, difficulty: $difficulty, imageUrl: $imageUrl, createdAt: $createdAt, updatedAt: $updatedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$CultivarImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.genetics, genetics) ||
                other.genetics == genetics) &&
            (identical(other.breederId, breederId) ||
                other.breederId == breederId) &&
            (identical(other.breederName, breederName) ||
                other.breederName == breederName) &&
            (identical(other.indica, indica) || other.indica == indica) &&
            (identical(other.sativa, sativa) || other.sativa == sativa) &&
            (identical(other.ruderalis, ruderalis) ||
                other.ruderalis == ruderalis) &&
            (identical(other.floweringType, floweringType) ||
                other.floweringType == floweringType) &&
            (identical(other.floweringDays, floweringDays) ||
                other.floweringDays == floweringDays) &&
            (identical(other.yieldIndoor, yieldIndoor) ||
                other.yieldIndoor == yieldIndoor) &&
            (identical(other.yieldOutdoor, yieldOutdoor) ||
                other.yieldOutdoor == yieldOutdoor) &&
            (identical(other.difficulty, difficulty) ||
                other.difficulty == difficulty) &&
            (identical(other.imageUrl, imageUrl) ||
                other.imageUrl == imageUrl) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt) &&
            (identical(other.updatedAt, updatedAt) ||
                other.updatedAt == updatedAt));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    name,
    description,
    genetics,
    breederId,
    breederName,
    indica,
    sativa,
    ruderalis,
    floweringType,
    floweringDays,
    yieldIndoor,
    yieldOutdoor,
    difficulty,
    imageUrl,
    createdAt,
    updatedAt,
  );

  /// Create a copy of Cultivar
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$CultivarImplCopyWith<_$CultivarImpl> get copyWith =>
      __$$CultivarImplCopyWithImpl<_$CultivarImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$CultivarImplToJson(this);
  }
}

abstract class _Cultivar implements Cultivar {
  const factory _Cultivar({
    required final int id,
    required final String name,
    final String? description,
    final String? genetics,
    final int? breederId,
    final String? breederName,
    final int? indica,
    final int? sativa,
    final int? ruderalis,
    final String? floweringType,
    final int? floweringDays,
    final int? yieldIndoor,
    final int? yieldOutdoor,
    final String? difficulty,
    final String? imageUrl,
    final DateTime? createdAt,
    final DateTime? updatedAt,
  }) = _$CultivarImpl;

  factory _Cultivar.fromJson(Map<String, dynamic> json) =
      _$CultivarImpl.fromJson;

  @override
  int get id;
  @override
  String get name;
  @override
  String? get description;
  @override
  String? get genetics;
  @override
  int? get breederId;
  @override
  String? get breederName;
  @override
  int? get indica;
  @override
  int? get sativa;
  @override
  int? get ruderalis;
  @override
  String? get floweringType;
  @override
  int? get floweringDays;
  @override
  int? get yieldIndoor;
  @override
  int? get yieldOutdoor;
  @override
  String? get difficulty;
  @override
  String? get imageUrl;
  @override
  DateTime? get createdAt;
  @override
  DateTime? get updatedAt;

  /// Create a copy of Cultivar
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$CultivarImplCopyWith<_$CultivarImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

CultivarCreate _$CultivarCreateFromJson(Map<String, dynamic> json) {
  return _CultivarCreate.fromJson(json);
}

/// @nodoc
mixin _$CultivarCreate {
  String get name => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  String? get genetics => throw _privateConstructorUsedError;
  int? get breederId => throw _privateConstructorUsedError;
  int? get indica => throw _privateConstructorUsedError;
  int? get sativa => throw _privateConstructorUsedError;
  int? get ruderalis => throw _privateConstructorUsedError;
  String? get floweringType => throw _privateConstructorUsedError;
  int? get floweringDays => throw _privateConstructorUsedError;
  int? get yieldIndoor => throw _privateConstructorUsedError;
  int? get yieldOutdoor => throw _privateConstructorUsedError;
  String? get difficulty => throw _privateConstructorUsedError;
  String? get imageUrl => throw _privateConstructorUsedError;

  /// Serializes this CultivarCreate to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of CultivarCreate
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $CultivarCreateCopyWith<CultivarCreate> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $CultivarCreateCopyWith<$Res> {
  factory $CultivarCreateCopyWith(
    CultivarCreate value,
    $Res Function(CultivarCreate) then,
  ) = _$CultivarCreateCopyWithImpl<$Res, CultivarCreate>;
  @useResult
  $Res call({
    String name,
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
  });
}

/// @nodoc
class _$CultivarCreateCopyWithImpl<$Res, $Val extends CultivarCreate>
    implements $CultivarCreateCopyWith<$Res> {
  _$CultivarCreateCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of CultivarCreate
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? name = null,
    Object? description = freezed,
    Object? genetics = freezed,
    Object? breederId = freezed,
    Object? indica = freezed,
    Object? sativa = freezed,
    Object? ruderalis = freezed,
    Object? floweringType = freezed,
    Object? floweringDays = freezed,
    Object? yieldIndoor = freezed,
    Object? yieldOutdoor = freezed,
    Object? difficulty = freezed,
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
            genetics: freezed == genetics
                ? _value.genetics
                : genetics // ignore: cast_nullable_to_non_nullable
                      as String?,
            breederId: freezed == breederId
                ? _value.breederId
                : breederId // ignore: cast_nullable_to_non_nullable
                      as int?,
            indica: freezed == indica
                ? _value.indica
                : indica // ignore: cast_nullable_to_non_nullable
                      as int?,
            sativa: freezed == sativa
                ? _value.sativa
                : sativa // ignore: cast_nullable_to_non_nullable
                      as int?,
            ruderalis: freezed == ruderalis
                ? _value.ruderalis
                : ruderalis // ignore: cast_nullable_to_non_nullable
                      as int?,
            floweringType: freezed == floweringType
                ? _value.floweringType
                : floweringType // ignore: cast_nullable_to_non_nullable
                      as String?,
            floweringDays: freezed == floweringDays
                ? _value.floweringDays
                : floweringDays // ignore: cast_nullable_to_non_nullable
                      as int?,
            yieldIndoor: freezed == yieldIndoor
                ? _value.yieldIndoor
                : yieldIndoor // ignore: cast_nullable_to_non_nullable
                      as int?,
            yieldOutdoor: freezed == yieldOutdoor
                ? _value.yieldOutdoor
                : yieldOutdoor // ignore: cast_nullable_to_non_nullable
                      as int?,
            difficulty: freezed == difficulty
                ? _value.difficulty
                : difficulty // ignore: cast_nullable_to_non_nullable
                      as String?,
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
abstract class _$$CultivarCreateImplCopyWith<$Res>
    implements $CultivarCreateCopyWith<$Res> {
  factory _$$CultivarCreateImplCopyWith(
    _$CultivarCreateImpl value,
    $Res Function(_$CultivarCreateImpl) then,
  ) = __$$CultivarCreateImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String name,
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
  });
}

/// @nodoc
class __$$CultivarCreateImplCopyWithImpl<$Res>
    extends _$CultivarCreateCopyWithImpl<$Res, _$CultivarCreateImpl>
    implements _$$CultivarCreateImplCopyWith<$Res> {
  __$$CultivarCreateImplCopyWithImpl(
    _$CultivarCreateImpl _value,
    $Res Function(_$CultivarCreateImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of CultivarCreate
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? name = null,
    Object? description = freezed,
    Object? genetics = freezed,
    Object? breederId = freezed,
    Object? indica = freezed,
    Object? sativa = freezed,
    Object? ruderalis = freezed,
    Object? floweringType = freezed,
    Object? floweringDays = freezed,
    Object? yieldIndoor = freezed,
    Object? yieldOutdoor = freezed,
    Object? difficulty = freezed,
    Object? imageUrl = freezed,
  }) {
    return _then(
      _$CultivarCreateImpl(
        name: null == name
            ? _value.name
            : name // ignore: cast_nullable_to_non_nullable
                  as String,
        description: freezed == description
            ? _value.description
            : description // ignore: cast_nullable_to_non_nullable
                  as String?,
        genetics: freezed == genetics
            ? _value.genetics
            : genetics // ignore: cast_nullable_to_non_nullable
                  as String?,
        breederId: freezed == breederId
            ? _value.breederId
            : breederId // ignore: cast_nullable_to_non_nullable
                  as int?,
        indica: freezed == indica
            ? _value.indica
            : indica // ignore: cast_nullable_to_non_nullable
                  as int?,
        sativa: freezed == sativa
            ? _value.sativa
            : sativa // ignore: cast_nullable_to_non_nullable
                  as int?,
        ruderalis: freezed == ruderalis
            ? _value.ruderalis
            : ruderalis // ignore: cast_nullable_to_non_nullable
                  as int?,
        floweringType: freezed == floweringType
            ? _value.floweringType
            : floweringType // ignore: cast_nullable_to_non_nullable
                  as String?,
        floweringDays: freezed == floweringDays
            ? _value.floweringDays
            : floweringDays // ignore: cast_nullable_to_non_nullable
                  as int?,
        yieldIndoor: freezed == yieldIndoor
            ? _value.yieldIndoor
            : yieldIndoor // ignore: cast_nullable_to_non_nullable
                  as int?,
        yieldOutdoor: freezed == yieldOutdoor
            ? _value.yieldOutdoor
            : yieldOutdoor // ignore: cast_nullable_to_non_nullable
                  as int?,
        difficulty: freezed == difficulty
            ? _value.difficulty
            : difficulty // ignore: cast_nullable_to_non_nullable
                  as String?,
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
class _$CultivarCreateImpl implements _CultivarCreate {
  const _$CultivarCreateImpl({
    required this.name,
    this.description,
    this.genetics,
    this.breederId,
    this.indica,
    this.sativa,
    this.ruderalis,
    this.floweringType,
    this.floweringDays,
    this.yieldIndoor,
    this.yieldOutdoor,
    this.difficulty,
    this.imageUrl,
  });

  factory _$CultivarCreateImpl.fromJson(Map<String, dynamic> json) =>
      _$$CultivarCreateImplFromJson(json);

  @override
  final String name;
  @override
  final String? description;
  @override
  final String? genetics;
  @override
  final int? breederId;
  @override
  final int? indica;
  @override
  final int? sativa;
  @override
  final int? ruderalis;
  @override
  final String? floweringType;
  @override
  final int? floweringDays;
  @override
  final int? yieldIndoor;
  @override
  final int? yieldOutdoor;
  @override
  final String? difficulty;
  @override
  final String? imageUrl;

  @override
  String toString() {
    return 'CultivarCreate(name: $name, description: $description, genetics: $genetics, breederId: $breederId, indica: $indica, sativa: $sativa, ruderalis: $ruderalis, floweringType: $floweringType, floweringDays: $floweringDays, yieldIndoor: $yieldIndoor, yieldOutdoor: $yieldOutdoor, difficulty: $difficulty, imageUrl: $imageUrl)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$CultivarCreateImpl &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.genetics, genetics) ||
                other.genetics == genetics) &&
            (identical(other.breederId, breederId) ||
                other.breederId == breederId) &&
            (identical(other.indica, indica) || other.indica == indica) &&
            (identical(other.sativa, sativa) || other.sativa == sativa) &&
            (identical(other.ruderalis, ruderalis) ||
                other.ruderalis == ruderalis) &&
            (identical(other.floweringType, floweringType) ||
                other.floweringType == floweringType) &&
            (identical(other.floweringDays, floweringDays) ||
                other.floweringDays == floweringDays) &&
            (identical(other.yieldIndoor, yieldIndoor) ||
                other.yieldIndoor == yieldIndoor) &&
            (identical(other.yieldOutdoor, yieldOutdoor) ||
                other.yieldOutdoor == yieldOutdoor) &&
            (identical(other.difficulty, difficulty) ||
                other.difficulty == difficulty) &&
            (identical(other.imageUrl, imageUrl) ||
                other.imageUrl == imageUrl));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    name,
    description,
    genetics,
    breederId,
    indica,
    sativa,
    ruderalis,
    floweringType,
    floweringDays,
    yieldIndoor,
    yieldOutdoor,
    difficulty,
    imageUrl,
  );

  /// Create a copy of CultivarCreate
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$CultivarCreateImplCopyWith<_$CultivarCreateImpl> get copyWith =>
      __$$CultivarCreateImplCopyWithImpl<_$CultivarCreateImpl>(
        this,
        _$identity,
      );

  @override
  Map<String, dynamic> toJson() {
    return _$$CultivarCreateImplToJson(this);
  }
}

abstract class _CultivarCreate implements CultivarCreate {
  const factory _CultivarCreate({
    required final String name,
    final String? description,
    final String? genetics,
    final int? breederId,
    final int? indica,
    final int? sativa,
    final int? ruderalis,
    final String? floweringType,
    final int? floweringDays,
    final int? yieldIndoor,
    final int? yieldOutdoor,
    final String? difficulty,
    final String? imageUrl,
  }) = _$CultivarCreateImpl;

  factory _CultivarCreate.fromJson(Map<String, dynamic> json) =
      _$CultivarCreateImpl.fromJson;

  @override
  String get name;
  @override
  String? get description;
  @override
  String? get genetics;
  @override
  int? get breederId;
  @override
  int? get indica;
  @override
  int? get sativa;
  @override
  int? get ruderalis;
  @override
  String? get floweringType;
  @override
  int? get floweringDays;
  @override
  int? get yieldIndoor;
  @override
  int? get yieldOutdoor;
  @override
  String? get difficulty;
  @override
  String? get imageUrl;

  /// Create a copy of CultivarCreate
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$CultivarCreateImplCopyWith<_$CultivarCreateImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

CultivarUpdate _$CultivarUpdateFromJson(Map<String, dynamic> json) {
  return _CultivarUpdate.fromJson(json);
}

/// @nodoc
mixin _$CultivarUpdate {
  String? get name => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  String? get genetics => throw _privateConstructorUsedError;
  int? get breederId => throw _privateConstructorUsedError;
  int? get indica => throw _privateConstructorUsedError;
  int? get sativa => throw _privateConstructorUsedError;
  int? get ruderalis => throw _privateConstructorUsedError;
  String? get floweringType => throw _privateConstructorUsedError;
  int? get floweringDays => throw _privateConstructorUsedError;
  int? get yieldIndoor => throw _privateConstructorUsedError;
  int? get yieldOutdoor => throw _privateConstructorUsedError;
  String? get difficulty => throw _privateConstructorUsedError;
  String? get imageUrl => throw _privateConstructorUsedError;

  /// Serializes this CultivarUpdate to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of CultivarUpdate
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $CultivarUpdateCopyWith<CultivarUpdate> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $CultivarUpdateCopyWith<$Res> {
  factory $CultivarUpdateCopyWith(
    CultivarUpdate value,
    $Res Function(CultivarUpdate) then,
  ) = _$CultivarUpdateCopyWithImpl<$Res, CultivarUpdate>;
  @useResult
  $Res call({
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
  });
}

/// @nodoc
class _$CultivarUpdateCopyWithImpl<$Res, $Val extends CultivarUpdate>
    implements $CultivarUpdateCopyWith<$Res> {
  _$CultivarUpdateCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of CultivarUpdate
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? name = freezed,
    Object? description = freezed,
    Object? genetics = freezed,
    Object? breederId = freezed,
    Object? indica = freezed,
    Object? sativa = freezed,
    Object? ruderalis = freezed,
    Object? floweringType = freezed,
    Object? floweringDays = freezed,
    Object? yieldIndoor = freezed,
    Object? yieldOutdoor = freezed,
    Object? difficulty = freezed,
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
            genetics: freezed == genetics
                ? _value.genetics
                : genetics // ignore: cast_nullable_to_non_nullable
                      as String?,
            breederId: freezed == breederId
                ? _value.breederId
                : breederId // ignore: cast_nullable_to_non_nullable
                      as int?,
            indica: freezed == indica
                ? _value.indica
                : indica // ignore: cast_nullable_to_non_nullable
                      as int?,
            sativa: freezed == sativa
                ? _value.sativa
                : sativa // ignore: cast_nullable_to_non_nullable
                      as int?,
            ruderalis: freezed == ruderalis
                ? _value.ruderalis
                : ruderalis // ignore: cast_nullable_to_non_nullable
                      as int?,
            floweringType: freezed == floweringType
                ? _value.floweringType
                : floweringType // ignore: cast_nullable_to_non_nullable
                      as String?,
            floweringDays: freezed == floweringDays
                ? _value.floweringDays
                : floweringDays // ignore: cast_nullable_to_non_nullable
                      as int?,
            yieldIndoor: freezed == yieldIndoor
                ? _value.yieldIndoor
                : yieldIndoor // ignore: cast_nullable_to_non_nullable
                      as int?,
            yieldOutdoor: freezed == yieldOutdoor
                ? _value.yieldOutdoor
                : yieldOutdoor // ignore: cast_nullable_to_non_nullable
                      as int?,
            difficulty: freezed == difficulty
                ? _value.difficulty
                : difficulty // ignore: cast_nullable_to_non_nullable
                      as String?,
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
abstract class _$$CultivarUpdateImplCopyWith<$Res>
    implements $CultivarUpdateCopyWith<$Res> {
  factory _$$CultivarUpdateImplCopyWith(
    _$CultivarUpdateImpl value,
    $Res Function(_$CultivarUpdateImpl) then,
  ) = __$$CultivarUpdateImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
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
  });
}

/// @nodoc
class __$$CultivarUpdateImplCopyWithImpl<$Res>
    extends _$CultivarUpdateCopyWithImpl<$Res, _$CultivarUpdateImpl>
    implements _$$CultivarUpdateImplCopyWith<$Res> {
  __$$CultivarUpdateImplCopyWithImpl(
    _$CultivarUpdateImpl _value,
    $Res Function(_$CultivarUpdateImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of CultivarUpdate
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? name = freezed,
    Object? description = freezed,
    Object? genetics = freezed,
    Object? breederId = freezed,
    Object? indica = freezed,
    Object? sativa = freezed,
    Object? ruderalis = freezed,
    Object? floweringType = freezed,
    Object? floweringDays = freezed,
    Object? yieldIndoor = freezed,
    Object? yieldOutdoor = freezed,
    Object? difficulty = freezed,
    Object? imageUrl = freezed,
  }) {
    return _then(
      _$CultivarUpdateImpl(
        name: freezed == name
            ? _value.name
            : name // ignore: cast_nullable_to_non_nullable
                  as String?,
        description: freezed == description
            ? _value.description
            : description // ignore: cast_nullable_to_non_nullable
                  as String?,
        genetics: freezed == genetics
            ? _value.genetics
            : genetics // ignore: cast_nullable_to_non_nullable
                  as String?,
        breederId: freezed == breederId
            ? _value.breederId
            : breederId // ignore: cast_nullable_to_non_nullable
                  as int?,
        indica: freezed == indica
            ? _value.indica
            : indica // ignore: cast_nullable_to_non_nullable
                  as int?,
        sativa: freezed == sativa
            ? _value.sativa
            : sativa // ignore: cast_nullable_to_non_nullable
                  as int?,
        ruderalis: freezed == ruderalis
            ? _value.ruderalis
            : ruderalis // ignore: cast_nullable_to_non_nullable
                  as int?,
        floweringType: freezed == floweringType
            ? _value.floweringType
            : floweringType // ignore: cast_nullable_to_non_nullable
                  as String?,
        floweringDays: freezed == floweringDays
            ? _value.floweringDays
            : floweringDays // ignore: cast_nullable_to_non_nullable
                  as int?,
        yieldIndoor: freezed == yieldIndoor
            ? _value.yieldIndoor
            : yieldIndoor // ignore: cast_nullable_to_non_nullable
                  as int?,
        yieldOutdoor: freezed == yieldOutdoor
            ? _value.yieldOutdoor
            : yieldOutdoor // ignore: cast_nullable_to_non_nullable
                  as int?,
        difficulty: freezed == difficulty
            ? _value.difficulty
            : difficulty // ignore: cast_nullable_to_non_nullable
                  as String?,
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
class _$CultivarUpdateImpl implements _CultivarUpdate {
  const _$CultivarUpdateImpl({
    this.name,
    this.description,
    this.genetics,
    this.breederId,
    this.indica,
    this.sativa,
    this.ruderalis,
    this.floweringType,
    this.floweringDays,
    this.yieldIndoor,
    this.yieldOutdoor,
    this.difficulty,
    this.imageUrl,
  });

  factory _$CultivarUpdateImpl.fromJson(Map<String, dynamic> json) =>
      _$$CultivarUpdateImplFromJson(json);

  @override
  final String? name;
  @override
  final String? description;
  @override
  final String? genetics;
  @override
  final int? breederId;
  @override
  final int? indica;
  @override
  final int? sativa;
  @override
  final int? ruderalis;
  @override
  final String? floweringType;
  @override
  final int? floweringDays;
  @override
  final int? yieldIndoor;
  @override
  final int? yieldOutdoor;
  @override
  final String? difficulty;
  @override
  final String? imageUrl;

  @override
  String toString() {
    return 'CultivarUpdate(name: $name, description: $description, genetics: $genetics, breederId: $breederId, indica: $indica, sativa: $sativa, ruderalis: $ruderalis, floweringType: $floweringType, floweringDays: $floweringDays, yieldIndoor: $yieldIndoor, yieldOutdoor: $yieldOutdoor, difficulty: $difficulty, imageUrl: $imageUrl)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$CultivarUpdateImpl &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.genetics, genetics) ||
                other.genetics == genetics) &&
            (identical(other.breederId, breederId) ||
                other.breederId == breederId) &&
            (identical(other.indica, indica) || other.indica == indica) &&
            (identical(other.sativa, sativa) || other.sativa == sativa) &&
            (identical(other.ruderalis, ruderalis) ||
                other.ruderalis == ruderalis) &&
            (identical(other.floweringType, floweringType) ||
                other.floweringType == floweringType) &&
            (identical(other.floweringDays, floweringDays) ||
                other.floweringDays == floweringDays) &&
            (identical(other.yieldIndoor, yieldIndoor) ||
                other.yieldIndoor == yieldIndoor) &&
            (identical(other.yieldOutdoor, yieldOutdoor) ||
                other.yieldOutdoor == yieldOutdoor) &&
            (identical(other.difficulty, difficulty) ||
                other.difficulty == difficulty) &&
            (identical(other.imageUrl, imageUrl) ||
                other.imageUrl == imageUrl));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    name,
    description,
    genetics,
    breederId,
    indica,
    sativa,
    ruderalis,
    floweringType,
    floweringDays,
    yieldIndoor,
    yieldOutdoor,
    difficulty,
    imageUrl,
  );

  /// Create a copy of CultivarUpdate
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$CultivarUpdateImplCopyWith<_$CultivarUpdateImpl> get copyWith =>
      __$$CultivarUpdateImplCopyWithImpl<_$CultivarUpdateImpl>(
        this,
        _$identity,
      );

  @override
  Map<String, dynamic> toJson() {
    return _$$CultivarUpdateImplToJson(this);
  }
}

abstract class _CultivarUpdate implements CultivarUpdate {
  const factory _CultivarUpdate({
    final String? name,
    final String? description,
    final String? genetics,
    final int? breederId,
    final int? indica,
    final int? sativa,
    final int? ruderalis,
    final String? floweringType,
    final int? floweringDays,
    final int? yieldIndoor,
    final int? yieldOutdoor,
    final String? difficulty,
    final String? imageUrl,
  }) = _$CultivarUpdateImpl;

  factory _CultivarUpdate.fromJson(Map<String, dynamic> json) =
      _$CultivarUpdateImpl.fromJson;

  @override
  String? get name;
  @override
  String? get description;
  @override
  String? get genetics;
  @override
  int? get breederId;
  @override
  int? get indica;
  @override
  int? get sativa;
  @override
  int? get ruderalis;
  @override
  String? get floweringType;
  @override
  int? get floweringDays;
  @override
  int? get yieldIndoor;
  @override
  int? get yieldOutdoor;
  @override
  String? get difficulty;
  @override
  String? get imageUrl;

  /// Create a copy of CultivarUpdate
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$CultivarUpdateImplCopyWith<_$CultivarUpdateImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

Breeder _$BreederFromJson(Map<String, dynamic> json) {
  return _Breeder.fromJson(json);
}

/// @nodoc
mixin _$Breeder {
  int get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  String? get website => throw _privateConstructorUsedError;
  String? get imageUrl => throw _privateConstructorUsedError;
  DateTime? get createdAt => throw _privateConstructorUsedError;
  DateTime? get updatedAt => throw _privateConstructorUsedError;

  /// Serializes this Breeder to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of Breeder
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $BreederCopyWith<Breeder> get copyWith => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $BreederCopyWith<$Res> {
  factory $BreederCopyWith(Breeder value, $Res Function(Breeder) then) =
      _$BreederCopyWithImpl<$Res, Breeder>;
  @useResult
  $Res call({
    int id,
    String name,
    String? description,
    String? website,
    String? imageUrl,
    DateTime? createdAt,
    DateTime? updatedAt,
  });
}

/// @nodoc
class _$BreederCopyWithImpl<$Res, $Val extends Breeder>
    implements $BreederCopyWith<$Res> {
  _$BreederCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of Breeder
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? description = freezed,
    Object? website = freezed,
    Object? imageUrl = freezed,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as int,
            name: null == name
                ? _value.name
                : name // ignore: cast_nullable_to_non_nullable
                      as String,
            description: freezed == description
                ? _value.description
                : description // ignore: cast_nullable_to_non_nullable
                      as String?,
            website: freezed == website
                ? _value.website
                : website // ignore: cast_nullable_to_non_nullable
                      as String?,
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
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$BreederImplCopyWith<$Res> implements $BreederCopyWith<$Res> {
  factory _$$BreederImplCopyWith(
    _$BreederImpl value,
    $Res Function(_$BreederImpl) then,
  ) = __$$BreederImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    int id,
    String name,
    String? description,
    String? website,
    String? imageUrl,
    DateTime? createdAt,
    DateTime? updatedAt,
  });
}

/// @nodoc
class __$$BreederImplCopyWithImpl<$Res>
    extends _$BreederCopyWithImpl<$Res, _$BreederImpl>
    implements _$$BreederImplCopyWith<$Res> {
  __$$BreederImplCopyWithImpl(
    _$BreederImpl _value,
    $Res Function(_$BreederImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of Breeder
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? description = freezed,
    Object? website = freezed,
    Object? imageUrl = freezed,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(
      _$BreederImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as int,
        name: null == name
            ? _value.name
            : name // ignore: cast_nullable_to_non_nullable
                  as String,
        description: freezed == description
            ? _value.description
            : description // ignore: cast_nullable_to_non_nullable
                  as String?,
        website: freezed == website
            ? _value.website
            : website // ignore: cast_nullable_to_non_nullable
                  as String?,
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
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$BreederImpl implements _Breeder {
  const _$BreederImpl({
    required this.id,
    required this.name,
    this.description,
    this.website,
    this.imageUrl,
    this.createdAt,
    this.updatedAt,
  });

  factory _$BreederImpl.fromJson(Map<String, dynamic> json) =>
      _$$BreederImplFromJson(json);

  @override
  final int id;
  @override
  final String name;
  @override
  final String? description;
  @override
  final String? website;
  @override
  final String? imageUrl;
  @override
  final DateTime? createdAt;
  @override
  final DateTime? updatedAt;

  @override
  String toString() {
    return 'Breeder(id: $id, name: $name, description: $description, website: $website, imageUrl: $imageUrl, createdAt: $createdAt, updatedAt: $updatedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$BreederImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.website, website) || other.website == website) &&
            (identical(other.imageUrl, imageUrl) ||
                other.imageUrl == imageUrl) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt) &&
            (identical(other.updatedAt, updatedAt) ||
                other.updatedAt == updatedAt));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    name,
    description,
    website,
    imageUrl,
    createdAt,
    updatedAt,
  );

  /// Create a copy of Breeder
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$BreederImplCopyWith<_$BreederImpl> get copyWith =>
      __$$BreederImplCopyWithImpl<_$BreederImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$BreederImplToJson(this);
  }
}

abstract class _Breeder implements Breeder {
  const factory _Breeder({
    required final int id,
    required final String name,
    final String? description,
    final String? website,
    final String? imageUrl,
    final DateTime? createdAt,
    final DateTime? updatedAt,
  }) = _$BreederImpl;

  factory _Breeder.fromJson(Map<String, dynamic> json) = _$BreederImpl.fromJson;

  @override
  int get id;
  @override
  String get name;
  @override
  String? get description;
  @override
  String? get website;
  @override
  String? get imageUrl;
  @override
  DateTime? get createdAt;
  @override
  DateTime? get updatedAt;

  /// Create a copy of Breeder
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$BreederImplCopyWith<_$BreederImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

StrainsParams _$StrainsParamsFromJson(Map<String, dynamic> json) {
  return _StrainsParams.fromJson(json);
}

/// @nodoc
mixin _$StrainsParams {
  int get page => throw _privateConstructorUsedError;
  int get limit => throw _privateConstructorUsedError;
  String? get search => throw _privateConstructorUsedError;
  String? get breeder => throw _privateConstructorUsedError;
  String? get difficulty => throw _privateConstructorUsedError;
  String? get floweringType => throw _privateConstructorUsedError;
  int? get minIndica => throw _privateConstructorUsedError;
  int? get maxIndica => throw _privateConstructorUsedError;
  int? get minFloweringDays => throw _privateConstructorUsedError;
  int? get maxFloweringDays => throw _privateConstructorUsedError;

  /// Serializes this StrainsParams to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of StrainsParams
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $StrainsParamsCopyWith<StrainsParams> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $StrainsParamsCopyWith<$Res> {
  factory $StrainsParamsCopyWith(
    StrainsParams value,
    $Res Function(StrainsParams) then,
  ) = _$StrainsParamsCopyWithImpl<$Res, StrainsParams>;
  @useResult
  $Res call({
    int page,
    int limit,
    String? search,
    String? breeder,
    String? difficulty,
    String? floweringType,
    int? minIndica,
    int? maxIndica,
    int? minFloweringDays,
    int? maxFloweringDays,
  });
}

/// @nodoc
class _$StrainsParamsCopyWithImpl<$Res, $Val extends StrainsParams>
    implements $StrainsParamsCopyWith<$Res> {
  _$StrainsParamsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of StrainsParams
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? page = null,
    Object? limit = null,
    Object? search = freezed,
    Object? breeder = freezed,
    Object? difficulty = freezed,
    Object? floweringType = freezed,
    Object? minIndica = freezed,
    Object? maxIndica = freezed,
    Object? minFloweringDays = freezed,
    Object? maxFloweringDays = freezed,
  }) {
    return _then(
      _value.copyWith(
            page: null == page
                ? _value.page
                : page // ignore: cast_nullable_to_non_nullable
                      as int,
            limit: null == limit
                ? _value.limit
                : limit // ignore: cast_nullable_to_non_nullable
                      as int,
            search: freezed == search
                ? _value.search
                : search // ignore: cast_nullable_to_non_nullable
                      as String?,
            breeder: freezed == breeder
                ? _value.breeder
                : breeder // ignore: cast_nullable_to_non_nullable
                      as String?,
            difficulty: freezed == difficulty
                ? _value.difficulty
                : difficulty // ignore: cast_nullable_to_non_nullable
                      as String?,
            floweringType: freezed == floweringType
                ? _value.floweringType
                : floweringType // ignore: cast_nullable_to_non_nullable
                      as String?,
            minIndica: freezed == minIndica
                ? _value.minIndica
                : minIndica // ignore: cast_nullable_to_non_nullable
                      as int?,
            maxIndica: freezed == maxIndica
                ? _value.maxIndica
                : maxIndica // ignore: cast_nullable_to_non_nullable
                      as int?,
            minFloweringDays: freezed == minFloweringDays
                ? _value.minFloweringDays
                : minFloweringDays // ignore: cast_nullable_to_non_nullable
                      as int?,
            maxFloweringDays: freezed == maxFloweringDays
                ? _value.maxFloweringDays
                : maxFloweringDays // ignore: cast_nullable_to_non_nullable
                      as int?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$StrainsParamsImplCopyWith<$Res>
    implements $StrainsParamsCopyWith<$Res> {
  factory _$$StrainsParamsImplCopyWith(
    _$StrainsParamsImpl value,
    $Res Function(_$StrainsParamsImpl) then,
  ) = __$$StrainsParamsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    int page,
    int limit,
    String? search,
    String? breeder,
    String? difficulty,
    String? floweringType,
    int? minIndica,
    int? maxIndica,
    int? minFloweringDays,
    int? maxFloweringDays,
  });
}

/// @nodoc
class __$$StrainsParamsImplCopyWithImpl<$Res>
    extends _$StrainsParamsCopyWithImpl<$Res, _$StrainsParamsImpl>
    implements _$$StrainsParamsImplCopyWith<$Res> {
  __$$StrainsParamsImplCopyWithImpl(
    _$StrainsParamsImpl _value,
    $Res Function(_$StrainsParamsImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of StrainsParams
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? page = null,
    Object? limit = null,
    Object? search = freezed,
    Object? breeder = freezed,
    Object? difficulty = freezed,
    Object? floweringType = freezed,
    Object? minIndica = freezed,
    Object? maxIndica = freezed,
    Object? minFloweringDays = freezed,
    Object? maxFloweringDays = freezed,
  }) {
    return _then(
      _$StrainsParamsImpl(
        page: null == page
            ? _value.page
            : page // ignore: cast_nullable_to_non_nullable
                  as int,
        limit: null == limit
            ? _value.limit
            : limit // ignore: cast_nullable_to_non_nullable
                  as int,
        search: freezed == search
            ? _value.search
            : search // ignore: cast_nullable_to_non_nullable
                  as String?,
        breeder: freezed == breeder
            ? _value.breeder
            : breeder // ignore: cast_nullable_to_non_nullable
                  as String?,
        difficulty: freezed == difficulty
            ? _value.difficulty
            : difficulty // ignore: cast_nullable_to_non_nullable
                  as String?,
        floweringType: freezed == floweringType
            ? _value.floweringType
            : floweringType // ignore: cast_nullable_to_non_nullable
                  as String?,
        minIndica: freezed == minIndica
            ? _value.minIndica
            : minIndica // ignore: cast_nullable_to_non_nullable
                  as int?,
        maxIndica: freezed == maxIndica
            ? _value.maxIndica
            : maxIndica // ignore: cast_nullable_to_non_nullable
                  as int?,
        minFloweringDays: freezed == minFloweringDays
            ? _value.minFloweringDays
            : minFloweringDays // ignore: cast_nullable_to_non_nullable
                  as int?,
        maxFloweringDays: freezed == maxFloweringDays
            ? _value.maxFloweringDays
            : maxFloweringDays // ignore: cast_nullable_to_non_nullable
                  as int?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$StrainsParamsImpl extends _StrainsParams {
  const _$StrainsParamsImpl({
    this.page = 1,
    this.limit = 20,
    this.search,
    this.breeder,
    this.difficulty,
    this.floweringType,
    this.minIndica,
    this.maxIndica,
    this.minFloweringDays,
    this.maxFloweringDays,
  }) : super._();

  factory _$StrainsParamsImpl.fromJson(Map<String, dynamic> json) =>
      _$$StrainsParamsImplFromJson(json);

  @override
  @JsonKey()
  final int page;
  @override
  @JsonKey()
  final int limit;
  @override
  final String? search;
  @override
  final String? breeder;
  @override
  final String? difficulty;
  @override
  final String? floweringType;
  @override
  final int? minIndica;
  @override
  final int? maxIndica;
  @override
  final int? minFloweringDays;
  @override
  final int? maxFloweringDays;

  @override
  String toString() {
    return 'StrainsParams(page: $page, limit: $limit, search: $search, breeder: $breeder, difficulty: $difficulty, floweringType: $floweringType, minIndica: $minIndica, maxIndica: $maxIndica, minFloweringDays: $minFloweringDays, maxFloweringDays: $maxFloweringDays)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$StrainsParamsImpl &&
            (identical(other.page, page) || other.page == page) &&
            (identical(other.limit, limit) || other.limit == limit) &&
            (identical(other.search, search) || other.search == search) &&
            (identical(other.breeder, breeder) || other.breeder == breeder) &&
            (identical(other.difficulty, difficulty) ||
                other.difficulty == difficulty) &&
            (identical(other.floweringType, floweringType) ||
                other.floweringType == floweringType) &&
            (identical(other.minIndica, minIndica) ||
                other.minIndica == minIndica) &&
            (identical(other.maxIndica, maxIndica) ||
                other.maxIndica == maxIndica) &&
            (identical(other.minFloweringDays, minFloweringDays) ||
                other.minFloweringDays == minFloweringDays) &&
            (identical(other.maxFloweringDays, maxFloweringDays) ||
                other.maxFloweringDays == maxFloweringDays));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    page,
    limit,
    search,
    breeder,
    difficulty,
    floweringType,
    minIndica,
    maxIndica,
    minFloweringDays,
    maxFloweringDays,
  );

  /// Create a copy of StrainsParams
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$StrainsParamsImplCopyWith<_$StrainsParamsImpl> get copyWith =>
      __$$StrainsParamsImplCopyWithImpl<_$StrainsParamsImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$StrainsParamsImplToJson(this);
  }
}

abstract class _StrainsParams extends StrainsParams {
  const factory _StrainsParams({
    final int page,
    final int limit,
    final String? search,
    final String? breeder,
    final String? difficulty,
    final String? floweringType,
    final int? minIndica,
    final int? maxIndica,
    final int? minFloweringDays,
    final int? maxFloweringDays,
  }) = _$StrainsParamsImpl;
  const _StrainsParams._() : super._();

  factory _StrainsParams.fromJson(Map<String, dynamic> json) =
      _$StrainsParamsImpl.fromJson;

  @override
  int get page;
  @override
  int get limit;
  @override
  String? get search;
  @override
  String? get breeder;
  @override
  String? get difficulty;
  @override
  String? get floweringType;
  @override
  int? get minIndica;
  @override
  int? get maxIndica;
  @override
  int? get minFloweringDays;
  @override
  int? get maxFloweringDays;

  /// Create a copy of StrainsParams
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$StrainsParamsImplCopyWith<_$StrainsParamsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

PaginatedStrainsResponse _$PaginatedStrainsResponseFromJson(
  Map<String, dynamic> json,
) {
  return _PaginatedStrainsResponse.fromJson(json);
}

/// @nodoc
mixin _$PaginatedStrainsResponse {
  List<Cultivar> get data => throw _privateConstructorUsedError;
  int get total => throw _privateConstructorUsedError;
  int get page => throw _privateConstructorUsedError;
  int get limit => throw _privateConstructorUsedError;
  int get totalPages => throw _privateConstructorUsedError;
  bool get hasNext => throw _privateConstructorUsedError;
  bool get hasPrev => throw _privateConstructorUsedError;

  /// Serializes this PaginatedStrainsResponse to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of PaginatedStrainsResponse
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $PaginatedStrainsResponseCopyWith<PaginatedStrainsResponse> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PaginatedStrainsResponseCopyWith<$Res> {
  factory $PaginatedStrainsResponseCopyWith(
    PaginatedStrainsResponse value,
    $Res Function(PaginatedStrainsResponse) then,
  ) = _$PaginatedStrainsResponseCopyWithImpl<$Res, PaginatedStrainsResponse>;
  @useResult
  $Res call({
    List<Cultivar> data,
    int total,
    int page,
    int limit,
    int totalPages,
    bool hasNext,
    bool hasPrev,
  });
}

/// @nodoc
class _$PaginatedStrainsResponseCopyWithImpl<
  $Res,
  $Val extends PaginatedStrainsResponse
>
    implements $PaginatedStrainsResponseCopyWith<$Res> {
  _$PaginatedStrainsResponseCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of PaginatedStrainsResponse
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? data = null,
    Object? total = null,
    Object? page = null,
    Object? limit = null,
    Object? totalPages = null,
    Object? hasNext = null,
    Object? hasPrev = null,
  }) {
    return _then(
      _value.copyWith(
            data: null == data
                ? _value.data
                : data // ignore: cast_nullable_to_non_nullable
                      as List<Cultivar>,
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
            totalPages: null == totalPages
                ? _value.totalPages
                : totalPages // ignore: cast_nullable_to_non_nullable
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
abstract class _$$PaginatedStrainsResponseImplCopyWith<$Res>
    implements $PaginatedStrainsResponseCopyWith<$Res> {
  factory _$$PaginatedStrainsResponseImplCopyWith(
    _$PaginatedStrainsResponseImpl value,
    $Res Function(_$PaginatedStrainsResponseImpl) then,
  ) = __$$PaginatedStrainsResponseImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    List<Cultivar> data,
    int total,
    int page,
    int limit,
    int totalPages,
    bool hasNext,
    bool hasPrev,
  });
}

/// @nodoc
class __$$PaginatedStrainsResponseImplCopyWithImpl<$Res>
    extends
        _$PaginatedStrainsResponseCopyWithImpl<
          $Res,
          _$PaginatedStrainsResponseImpl
        >
    implements _$$PaginatedStrainsResponseImplCopyWith<$Res> {
  __$$PaginatedStrainsResponseImplCopyWithImpl(
    _$PaginatedStrainsResponseImpl _value,
    $Res Function(_$PaginatedStrainsResponseImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of PaginatedStrainsResponse
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? data = null,
    Object? total = null,
    Object? page = null,
    Object? limit = null,
    Object? totalPages = null,
    Object? hasNext = null,
    Object? hasPrev = null,
  }) {
    return _then(
      _$PaginatedStrainsResponseImpl(
        data: null == data
            ? _value._data
            : data // ignore: cast_nullable_to_non_nullable
                  as List<Cultivar>,
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
        totalPages: null == totalPages
            ? _value.totalPages
            : totalPages // ignore: cast_nullable_to_non_nullable
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
class _$PaginatedStrainsResponseImpl extends _PaginatedStrainsResponse {
  const _$PaginatedStrainsResponseImpl({
    required final List<Cultivar> data,
    required this.total,
    required this.page,
    required this.limit,
    required this.totalPages,
    required this.hasNext,
    required this.hasPrev,
  }) : _data = data,
       super._();

  factory _$PaginatedStrainsResponseImpl.fromJson(Map<String, dynamic> json) =>
      _$$PaginatedStrainsResponseImplFromJson(json);

  final List<Cultivar> _data;
  @override
  List<Cultivar> get data {
    if (_data is EqualUnmodifiableListView) return _data;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_data);
  }

  @override
  final int total;
  @override
  final int page;
  @override
  final int limit;
  @override
  final int totalPages;
  @override
  final bool hasNext;
  @override
  final bool hasPrev;

  @override
  String toString() {
    return 'PaginatedStrainsResponse(data: $data, total: $total, page: $page, limit: $limit, totalPages: $totalPages, hasNext: $hasNext, hasPrev: $hasPrev)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PaginatedStrainsResponseImpl &&
            const DeepCollectionEquality().equals(other._data, _data) &&
            (identical(other.total, total) || other.total == total) &&
            (identical(other.page, page) || other.page == page) &&
            (identical(other.limit, limit) || other.limit == limit) &&
            (identical(other.totalPages, totalPages) ||
                other.totalPages == totalPages) &&
            (identical(other.hasNext, hasNext) || other.hasNext == hasNext) &&
            (identical(other.hasPrev, hasPrev) || other.hasPrev == hasPrev));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    const DeepCollectionEquality().hash(_data),
    total,
    page,
    limit,
    totalPages,
    hasNext,
    hasPrev,
  );

  /// Create a copy of PaginatedStrainsResponse
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$PaginatedStrainsResponseImplCopyWith<_$PaginatedStrainsResponseImpl>
  get copyWith =>
      __$$PaginatedStrainsResponseImplCopyWithImpl<
        _$PaginatedStrainsResponseImpl
      >(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PaginatedStrainsResponseImplToJson(this);
  }
}

abstract class _PaginatedStrainsResponse extends PaginatedStrainsResponse {
  const factory _PaginatedStrainsResponse({
    required final List<Cultivar> data,
    required final int total,
    required final int page,
    required final int limit,
    required final int totalPages,
    required final bool hasNext,
    required final bool hasPrev,
  }) = _$PaginatedStrainsResponseImpl;
  const _PaginatedStrainsResponse._() : super._();

  factory _PaginatedStrainsResponse.fromJson(Map<String, dynamic> json) =
      _$PaginatedStrainsResponseImpl.fromJson;

  @override
  List<Cultivar> get data;
  @override
  int get total;
  @override
  int get page;
  @override
  int get limit;
  @override
  int get totalPages;
  @override
  bool get hasNext;
  @override
  bool get hasPrev;

  /// Create a copy of PaginatedStrainsResponse
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$PaginatedStrainsResponseImplCopyWith<_$PaginatedStrainsResponseImpl>
  get copyWith => throw _privateConstructorUsedError;
}

CultivarStats _$CultivarStatsFromJson(Map<String, dynamic> json) {
  return _CultivarStats.fromJson(json);
}

/// @nodoc
mixin _$CultivarStats {
  int get totalCultivars => throw _privateConstructorUsedError;
  int get totalBreeders => throw _privateConstructorUsedError;
  Map<String, int> get byDifficulty => throw _privateConstructorUsedError;
  Map<String, int> get byFloweringType => throw _privateConstructorUsedError;
  List<String> get popularBreeders => throw _privateConstructorUsedError;

  /// Serializes this CultivarStats to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of CultivarStats
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $CultivarStatsCopyWith<CultivarStats> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $CultivarStatsCopyWith<$Res> {
  factory $CultivarStatsCopyWith(
    CultivarStats value,
    $Res Function(CultivarStats) then,
  ) = _$CultivarStatsCopyWithImpl<$Res, CultivarStats>;
  @useResult
  $Res call({
    int totalCultivars,
    int totalBreeders,
    Map<String, int> byDifficulty,
    Map<String, int> byFloweringType,
    List<String> popularBreeders,
  });
}

/// @nodoc
class _$CultivarStatsCopyWithImpl<$Res, $Val extends CultivarStats>
    implements $CultivarStatsCopyWith<$Res> {
  _$CultivarStatsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of CultivarStats
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? totalCultivars = null,
    Object? totalBreeders = null,
    Object? byDifficulty = null,
    Object? byFloweringType = null,
    Object? popularBreeders = null,
  }) {
    return _then(
      _value.copyWith(
            totalCultivars: null == totalCultivars
                ? _value.totalCultivars
                : totalCultivars // ignore: cast_nullable_to_non_nullable
                      as int,
            totalBreeders: null == totalBreeders
                ? _value.totalBreeders
                : totalBreeders // ignore: cast_nullable_to_non_nullable
                      as int,
            byDifficulty: null == byDifficulty
                ? _value.byDifficulty
                : byDifficulty // ignore: cast_nullable_to_non_nullable
                      as Map<String, int>,
            byFloweringType: null == byFloweringType
                ? _value.byFloweringType
                : byFloweringType // ignore: cast_nullable_to_non_nullable
                      as Map<String, int>,
            popularBreeders: null == popularBreeders
                ? _value.popularBreeders
                : popularBreeders // ignore: cast_nullable_to_non_nullable
                      as List<String>,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$CultivarStatsImplCopyWith<$Res>
    implements $CultivarStatsCopyWith<$Res> {
  factory _$$CultivarStatsImplCopyWith(
    _$CultivarStatsImpl value,
    $Res Function(_$CultivarStatsImpl) then,
  ) = __$$CultivarStatsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    int totalCultivars,
    int totalBreeders,
    Map<String, int> byDifficulty,
    Map<String, int> byFloweringType,
    List<String> popularBreeders,
  });
}

/// @nodoc
class __$$CultivarStatsImplCopyWithImpl<$Res>
    extends _$CultivarStatsCopyWithImpl<$Res, _$CultivarStatsImpl>
    implements _$$CultivarStatsImplCopyWith<$Res> {
  __$$CultivarStatsImplCopyWithImpl(
    _$CultivarStatsImpl _value,
    $Res Function(_$CultivarStatsImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of CultivarStats
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? totalCultivars = null,
    Object? totalBreeders = null,
    Object? byDifficulty = null,
    Object? byFloweringType = null,
    Object? popularBreeders = null,
  }) {
    return _then(
      _$CultivarStatsImpl(
        totalCultivars: null == totalCultivars
            ? _value.totalCultivars
            : totalCultivars // ignore: cast_nullable_to_non_nullable
                  as int,
        totalBreeders: null == totalBreeders
            ? _value.totalBreeders
            : totalBreeders // ignore: cast_nullable_to_non_nullable
                  as int,
        byDifficulty: null == byDifficulty
            ? _value._byDifficulty
            : byDifficulty // ignore: cast_nullable_to_non_nullable
                  as Map<String, int>,
        byFloweringType: null == byFloweringType
            ? _value._byFloweringType
            : byFloweringType // ignore: cast_nullable_to_non_nullable
                  as Map<String, int>,
        popularBreeders: null == popularBreeders
            ? _value._popularBreeders
            : popularBreeders // ignore: cast_nullable_to_non_nullable
                  as List<String>,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$CultivarStatsImpl implements _CultivarStats {
  const _$CultivarStatsImpl({
    required this.totalCultivars,
    required this.totalBreeders,
    required final Map<String, int> byDifficulty,
    required final Map<String, int> byFloweringType,
    required final List<String> popularBreeders,
  }) : _byDifficulty = byDifficulty,
       _byFloweringType = byFloweringType,
       _popularBreeders = popularBreeders;

  factory _$CultivarStatsImpl.fromJson(Map<String, dynamic> json) =>
      _$$CultivarStatsImplFromJson(json);

  @override
  final int totalCultivars;
  @override
  final int totalBreeders;
  final Map<String, int> _byDifficulty;
  @override
  Map<String, int> get byDifficulty {
    if (_byDifficulty is EqualUnmodifiableMapView) return _byDifficulty;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_byDifficulty);
  }

  final Map<String, int> _byFloweringType;
  @override
  Map<String, int> get byFloweringType {
    if (_byFloweringType is EqualUnmodifiableMapView) return _byFloweringType;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(_byFloweringType);
  }

  final List<String> _popularBreeders;
  @override
  List<String> get popularBreeders {
    if (_popularBreeders is EqualUnmodifiableListView) return _popularBreeders;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_popularBreeders);
  }

  @override
  String toString() {
    return 'CultivarStats(totalCultivars: $totalCultivars, totalBreeders: $totalBreeders, byDifficulty: $byDifficulty, byFloweringType: $byFloweringType, popularBreeders: $popularBreeders)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$CultivarStatsImpl &&
            (identical(other.totalCultivars, totalCultivars) ||
                other.totalCultivars == totalCultivars) &&
            (identical(other.totalBreeders, totalBreeders) ||
                other.totalBreeders == totalBreeders) &&
            const DeepCollectionEquality().equals(
              other._byDifficulty,
              _byDifficulty,
            ) &&
            const DeepCollectionEquality().equals(
              other._byFloweringType,
              _byFloweringType,
            ) &&
            const DeepCollectionEquality().equals(
              other._popularBreeders,
              _popularBreeders,
            ));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    totalCultivars,
    totalBreeders,
    const DeepCollectionEquality().hash(_byDifficulty),
    const DeepCollectionEquality().hash(_byFloweringType),
    const DeepCollectionEquality().hash(_popularBreeders),
  );

  /// Create a copy of CultivarStats
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$CultivarStatsImplCopyWith<_$CultivarStatsImpl> get copyWith =>
      __$$CultivarStatsImplCopyWithImpl<_$CultivarStatsImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$CultivarStatsImplToJson(this);
  }
}

abstract class _CultivarStats implements CultivarStats {
  const factory _CultivarStats({
    required final int totalCultivars,
    required final int totalBreeders,
    required final Map<String, int> byDifficulty,
    required final Map<String, int> byFloweringType,
    required final List<String> popularBreeders,
  }) = _$CultivarStatsImpl;

  factory _CultivarStats.fromJson(Map<String, dynamic> json) =
      _$CultivarStatsImpl.fromJson;

  @override
  int get totalCultivars;
  @override
  int get totalBreeders;
  @override
  Map<String, int> get byDifficulty;
  @override
  Map<String, int> get byFloweringType;
  @override
  List<String> get popularBreeders;

  /// Create a copy of CultivarStats
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$CultivarStatsImplCopyWith<_$CultivarStatsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
