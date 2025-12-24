// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'cultivar_model.dart';

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
  int? get breederId => throw _privateConstructorUsedError;
  int get indica => throw _privateConstructorUsedError;
  int get sativa => throw _privateConstructorUsedError;
  bool get autoflower => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  int get seedCount => throw _privateConstructorUsedError;
  int? get cycleTime => throw _privateConstructorUsedError;
  String? get url => throw _privateConstructorUsedError;
  String? get parent1 => throw _privateConstructorUsedError;
  String? get parent2 => throw _privateConstructorUsedError;
  Map<String, dynamic>? get lineageJson => throw _privateConstructorUsedError;
  String? get seedfinderId => throw _privateConstructorUsedError;
  double? get thcContent => throw _privateConstructorUsedError;
  double? get cbdContent => throw _privateConstructorUsedError;
  String? get floweringType => throw _privateConstructorUsedError;
  Breeder? get breeder => throw _privateConstructorUsedError;
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
    int? breederId,
    int indica,
    int sativa,
    bool autoflower,
    String? description,
    int seedCount,
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
  });

  $BreederCopyWith<$Res>? get breeder;
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
    Object? breederId = freezed,
    Object? indica = null,
    Object? sativa = null,
    Object? autoflower = null,
    Object? description = freezed,
    Object? seedCount = null,
    Object? cycleTime = freezed,
    Object? url = freezed,
    Object? parent1 = freezed,
    Object? parent2 = freezed,
    Object? lineageJson = freezed,
    Object? seedfinderId = freezed,
    Object? thcContent = freezed,
    Object? cbdContent = freezed,
    Object? floweringType = freezed,
    Object? breeder = freezed,
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
            breederId: freezed == breederId
                ? _value.breederId
                : breederId // ignore: cast_nullable_to_non_nullable
                      as int?,
            indica: null == indica
                ? _value.indica
                : indica // ignore: cast_nullable_to_non_nullable
                      as int,
            sativa: null == sativa
                ? _value.sativa
                : sativa // ignore: cast_nullable_to_non_nullable
                      as int,
            autoflower: null == autoflower
                ? _value.autoflower
                : autoflower // ignore: cast_nullable_to_non_nullable
                      as bool,
            description: freezed == description
                ? _value.description
                : description // ignore: cast_nullable_to_non_nullable
                      as String?,
            seedCount: null == seedCount
                ? _value.seedCount
                : seedCount // ignore: cast_nullable_to_non_nullable
                      as int,
            cycleTime: freezed == cycleTime
                ? _value.cycleTime
                : cycleTime // ignore: cast_nullable_to_non_nullable
                      as int?,
            url: freezed == url
                ? _value.url
                : url // ignore: cast_nullable_to_non_nullable
                      as String?,
            parent1: freezed == parent1
                ? _value.parent1
                : parent1 // ignore: cast_nullable_to_non_nullable
                      as String?,
            parent2: freezed == parent2
                ? _value.parent2
                : parent2 // ignore: cast_nullable_to_non_nullable
                      as String?,
            lineageJson: freezed == lineageJson
                ? _value.lineageJson
                : lineageJson // ignore: cast_nullable_to_non_nullable
                      as Map<String, dynamic>?,
            seedfinderId: freezed == seedfinderId
                ? _value.seedfinderId
                : seedfinderId // ignore: cast_nullable_to_non_nullable
                      as String?,
            thcContent: freezed == thcContent
                ? _value.thcContent
                : thcContent // ignore: cast_nullable_to_non_nullable
                      as double?,
            cbdContent: freezed == cbdContent
                ? _value.cbdContent
                : cbdContent // ignore: cast_nullable_to_non_nullable
                      as double?,
            floweringType: freezed == floweringType
                ? _value.floweringType
                : floweringType // ignore: cast_nullable_to_non_nullable
                      as String?,
            breeder: freezed == breeder
                ? _value.breeder
                : breeder // ignore: cast_nullable_to_non_nullable
                      as Breeder?,
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

  /// Create a copy of Cultivar
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $BreederCopyWith<$Res>? get breeder {
    if (_value.breeder == null) {
      return null;
    }

    return $BreederCopyWith<$Res>(_value.breeder!, (value) {
      return _then(_value.copyWith(breeder: value) as $Val);
    });
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
    int? breederId,
    int indica,
    int sativa,
    bool autoflower,
    String? description,
    int seedCount,
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
  });

  @override
  $BreederCopyWith<$Res>? get breeder;
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
    Object? breederId = freezed,
    Object? indica = null,
    Object? sativa = null,
    Object? autoflower = null,
    Object? description = freezed,
    Object? seedCount = null,
    Object? cycleTime = freezed,
    Object? url = freezed,
    Object? parent1 = freezed,
    Object? parent2 = freezed,
    Object? lineageJson = freezed,
    Object? seedfinderId = freezed,
    Object? thcContent = freezed,
    Object? cbdContent = freezed,
    Object? floweringType = freezed,
    Object? breeder = freezed,
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
        breederId: freezed == breederId
            ? _value.breederId
            : breederId // ignore: cast_nullable_to_non_nullable
                  as int?,
        indica: null == indica
            ? _value.indica
            : indica // ignore: cast_nullable_to_non_nullable
                  as int,
        sativa: null == sativa
            ? _value.sativa
            : sativa // ignore: cast_nullable_to_non_nullable
                  as int,
        autoflower: null == autoflower
            ? _value.autoflower
            : autoflower // ignore: cast_nullable_to_non_nullable
                  as bool,
        description: freezed == description
            ? _value.description
            : description // ignore: cast_nullable_to_non_nullable
                  as String?,
        seedCount: null == seedCount
            ? _value.seedCount
            : seedCount // ignore: cast_nullable_to_non_nullable
                  as int,
        cycleTime: freezed == cycleTime
            ? _value.cycleTime
            : cycleTime // ignore: cast_nullable_to_non_nullable
                  as int?,
        url: freezed == url
            ? _value.url
            : url // ignore: cast_nullable_to_non_nullable
                  as String?,
        parent1: freezed == parent1
            ? _value.parent1
            : parent1 // ignore: cast_nullable_to_non_nullable
                  as String?,
        parent2: freezed == parent2
            ? _value.parent2
            : parent2 // ignore: cast_nullable_to_non_nullable
                  as String?,
        lineageJson: freezed == lineageJson
            ? _value._lineageJson
            : lineageJson // ignore: cast_nullable_to_non_nullable
                  as Map<String, dynamic>?,
        seedfinderId: freezed == seedfinderId
            ? _value.seedfinderId
            : seedfinderId // ignore: cast_nullable_to_non_nullable
                  as String?,
        thcContent: freezed == thcContent
            ? _value.thcContent
            : thcContent // ignore: cast_nullable_to_non_nullable
                  as double?,
        cbdContent: freezed == cbdContent
            ? _value.cbdContent
            : cbdContent // ignore: cast_nullable_to_non_nullable
                  as double?,
        floweringType: freezed == floweringType
            ? _value.floweringType
            : floweringType // ignore: cast_nullable_to_non_nullable
                  as String?,
        breeder: freezed == breeder
            ? _value.breeder
            : breeder // ignore: cast_nullable_to_non_nullable
                  as Breeder?,
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
class _$CultivarImpl extends _Cultivar {
  const _$CultivarImpl({
    required this.id,
    required this.name,
    this.breederId,
    this.indica = 0,
    this.sativa = 0,
    this.autoflower = false,
    this.description,
    this.seedCount = 0,
    this.cycleTime,
    this.url,
    this.parent1,
    this.parent2,
    final Map<String, dynamic>? lineageJson,
    this.seedfinderId,
    this.thcContent,
    this.cbdContent,
    this.floweringType,
    this.breeder,
    this.createdAt,
    this.updatedAt,
  }) : _lineageJson = lineageJson,
       super._();

  factory _$CultivarImpl.fromJson(Map<String, dynamic> json) =>
      _$$CultivarImplFromJson(json);

  @override
  final int id;
  @override
  final String name;
  @override
  final int? breederId;
  @override
  @JsonKey()
  final int indica;
  @override
  @JsonKey()
  final int sativa;
  @override
  @JsonKey()
  final bool autoflower;
  @override
  final String? description;
  @override
  @JsonKey()
  final int seedCount;
  @override
  final int? cycleTime;
  @override
  final String? url;
  @override
  final String? parent1;
  @override
  final String? parent2;
  final Map<String, dynamic>? _lineageJson;
  @override
  Map<String, dynamic>? get lineageJson {
    final value = _lineageJson;
    if (value == null) return null;
    if (_lineageJson is EqualUnmodifiableMapView) return _lineageJson;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(value);
  }

  @override
  final String? seedfinderId;
  @override
  final double? thcContent;
  @override
  final double? cbdContent;
  @override
  final String? floweringType;
  @override
  final Breeder? breeder;
  @override
  final DateTime? createdAt;
  @override
  final DateTime? updatedAt;

  @override
  String toString() {
    return 'Cultivar(id: $id, name: $name, breederId: $breederId, indica: $indica, sativa: $sativa, autoflower: $autoflower, description: $description, seedCount: $seedCount, cycleTime: $cycleTime, url: $url, parent1: $parent1, parent2: $parent2, lineageJson: $lineageJson, seedfinderId: $seedfinderId, thcContent: $thcContent, cbdContent: $cbdContent, floweringType: $floweringType, breeder: $breeder, createdAt: $createdAt, updatedAt: $updatedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$CultivarImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.breederId, breederId) ||
                other.breederId == breederId) &&
            (identical(other.indica, indica) || other.indica == indica) &&
            (identical(other.sativa, sativa) || other.sativa == sativa) &&
            (identical(other.autoflower, autoflower) ||
                other.autoflower == autoflower) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.seedCount, seedCount) ||
                other.seedCount == seedCount) &&
            (identical(other.cycleTime, cycleTime) ||
                other.cycleTime == cycleTime) &&
            (identical(other.url, url) || other.url == url) &&
            (identical(other.parent1, parent1) || other.parent1 == parent1) &&
            (identical(other.parent2, parent2) || other.parent2 == parent2) &&
            const DeepCollectionEquality().equals(
              other._lineageJson,
              _lineageJson,
            ) &&
            (identical(other.seedfinderId, seedfinderId) ||
                other.seedfinderId == seedfinderId) &&
            (identical(other.thcContent, thcContent) ||
                other.thcContent == thcContent) &&
            (identical(other.cbdContent, cbdContent) ||
                other.cbdContent == cbdContent) &&
            (identical(other.floweringType, floweringType) ||
                other.floweringType == floweringType) &&
            (identical(other.breeder, breeder) || other.breeder == breeder) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt) &&
            (identical(other.updatedAt, updatedAt) ||
                other.updatedAt == updatedAt));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hashAll([
    runtimeType,
    id,
    name,
    breederId,
    indica,
    sativa,
    autoflower,
    description,
    seedCount,
    cycleTime,
    url,
    parent1,
    parent2,
    const DeepCollectionEquality().hash(_lineageJson),
    seedfinderId,
    thcContent,
    cbdContent,
    floweringType,
    breeder,
    createdAt,
    updatedAt,
  ]);

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

abstract class _Cultivar extends Cultivar {
  const factory _Cultivar({
    required final int id,
    required final String name,
    final int? breederId,
    final int indica,
    final int sativa,
    final bool autoflower,
    final String? description,
    final int seedCount,
    final int? cycleTime,
    final String? url,
    final String? parent1,
    final String? parent2,
    final Map<String, dynamic>? lineageJson,
    final String? seedfinderId,
    final double? thcContent,
    final double? cbdContent,
    final String? floweringType,
    final Breeder? breeder,
    final DateTime? createdAt,
    final DateTime? updatedAt,
  }) = _$CultivarImpl;
  const _Cultivar._() : super._();

  factory _Cultivar.fromJson(Map<String, dynamic> json) =
      _$CultivarImpl.fromJson;

  @override
  int get id;
  @override
  String get name;
  @override
  int? get breederId;
  @override
  int get indica;
  @override
  int get sativa;
  @override
  bool get autoflower;
  @override
  String? get description;
  @override
  int get seedCount;
  @override
  int? get cycleTime;
  @override
  String? get url;
  @override
  String? get parent1;
  @override
  String? get parent2;
  @override
  Map<String, dynamic>? get lineageJson;
  @override
  String? get seedfinderId;
  @override
  double? get thcContent;
  @override
  double? get cbdContent;
  @override
  String? get floweringType;
  @override
  Breeder? get breeder;
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

Breeder _$BreederFromJson(Map<String, dynamic> json) {
  return _Breeder.fromJson(json);
}

/// @nodoc
mixin _$Breeder {
  int get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String? get country => throw _privateConstructorUsedError;
  String? get website => throw _privateConstructorUsedError;
  String? get seedfinderId => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  List<Cultivar>? get cultivars => throw _privateConstructorUsedError;
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
    String? country,
    String? website,
    String? seedfinderId,
    String? description,
    List<Cultivar>? cultivars,
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
    Object? country = freezed,
    Object? website = freezed,
    Object? seedfinderId = freezed,
    Object? description = freezed,
    Object? cultivars = freezed,
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
            country: freezed == country
                ? _value.country
                : country // ignore: cast_nullable_to_non_nullable
                      as String?,
            website: freezed == website
                ? _value.website
                : website // ignore: cast_nullable_to_non_nullable
                      as String?,
            seedfinderId: freezed == seedfinderId
                ? _value.seedfinderId
                : seedfinderId // ignore: cast_nullable_to_non_nullable
                      as String?,
            description: freezed == description
                ? _value.description
                : description // ignore: cast_nullable_to_non_nullable
                      as String?,
            cultivars: freezed == cultivars
                ? _value.cultivars
                : cultivars // ignore: cast_nullable_to_non_nullable
                      as List<Cultivar>?,
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
    String? country,
    String? website,
    String? seedfinderId,
    String? description,
    List<Cultivar>? cultivars,
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
    Object? country = freezed,
    Object? website = freezed,
    Object? seedfinderId = freezed,
    Object? description = freezed,
    Object? cultivars = freezed,
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
        country: freezed == country
            ? _value.country
            : country // ignore: cast_nullable_to_non_nullable
                  as String?,
        website: freezed == website
            ? _value.website
            : website // ignore: cast_nullable_to_non_nullable
                  as String?,
        seedfinderId: freezed == seedfinderId
            ? _value.seedfinderId
            : seedfinderId // ignore: cast_nullable_to_non_nullable
                  as String?,
        description: freezed == description
            ? _value.description
            : description // ignore: cast_nullable_to_non_nullable
                  as String?,
        cultivars: freezed == cultivars
            ? _value._cultivars
            : cultivars // ignore: cast_nullable_to_non_nullable
                  as List<Cultivar>?,
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
    this.country,
    this.website,
    this.seedfinderId,
    this.description,
    final List<Cultivar>? cultivars,
    this.createdAt,
    this.updatedAt,
  }) : _cultivars = cultivars;

  factory _$BreederImpl.fromJson(Map<String, dynamic> json) =>
      _$$BreederImplFromJson(json);

  @override
  final int id;
  @override
  final String name;
  @override
  final String? country;
  @override
  final String? website;
  @override
  final String? seedfinderId;
  @override
  final String? description;
  final List<Cultivar>? _cultivars;
  @override
  List<Cultivar>? get cultivars {
    final value = _cultivars;
    if (value == null) return null;
    if (_cultivars is EqualUnmodifiableListView) return _cultivars;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(value);
  }

  @override
  final DateTime? createdAt;
  @override
  final DateTime? updatedAt;

  @override
  String toString() {
    return 'Breeder(id: $id, name: $name, country: $country, website: $website, seedfinderId: $seedfinderId, description: $description, cultivars: $cultivars, createdAt: $createdAt, updatedAt: $updatedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$BreederImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.country, country) || other.country == country) &&
            (identical(other.website, website) || other.website == website) &&
            (identical(other.seedfinderId, seedfinderId) ||
                other.seedfinderId == seedfinderId) &&
            (identical(other.description, description) ||
                other.description == description) &&
            const DeepCollectionEquality().equals(
              other._cultivars,
              _cultivars,
            ) &&
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
    country,
    website,
    seedfinderId,
    description,
    const DeepCollectionEquality().hash(_cultivars),
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
    final String? country,
    final String? website,
    final String? seedfinderId,
    final String? description,
    final List<Cultivar>? cultivars,
    final DateTime? createdAt,
    final DateTime? updatedAt,
  }) = _$BreederImpl;

  factory _Breeder.fromJson(Map<String, dynamic> json) = _$BreederImpl.fromJson;

  @override
  int get id;
  @override
  String get name;
  @override
  String? get country;
  @override
  String? get website;
  @override
  String? get seedfinderId;
  @override
  String? get description;
  @override
  List<Cultivar>? get cultivars;
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

CultivarCreate _$CultivarCreateFromJson(Map<String, dynamic> json) {
  return _CultivarCreate.fromJson(json);
}

/// @nodoc
mixin _$CultivarCreate {
  String get name => throw _privateConstructorUsedError;
  int? get breederId => throw _privateConstructorUsedError;
  int get indica => throw _privateConstructorUsedError;
  int get sativa => throw _privateConstructorUsedError;
  bool get autoflower => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  int get seedCount => throw _privateConstructorUsedError;
  int? get cycleTime => throw _privateConstructorUsedError;
  String? get url => throw _privateConstructorUsedError;
  String? get parent1 => throw _privateConstructorUsedError;
  String? get parent2 => throw _privateConstructorUsedError;
  Map<String, dynamic>? get lineageJson => throw _privateConstructorUsedError;
  String? get seedfinderId => throw _privateConstructorUsedError;
  double? get thcContent => throw _privateConstructorUsedError;
  double? get cbdContent => throw _privateConstructorUsedError;
  String? get floweringType => throw _privateConstructorUsedError;

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
    int? breederId,
    int indica,
    int sativa,
    bool autoflower,
    String? description,
    int seedCount,
    int? cycleTime,
    String? url,
    String? parent1,
    String? parent2,
    Map<String, dynamic>? lineageJson,
    String? seedfinderId,
    double? thcContent,
    double? cbdContent,
    String? floweringType,
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
    Object? breederId = freezed,
    Object? indica = null,
    Object? sativa = null,
    Object? autoflower = null,
    Object? description = freezed,
    Object? seedCount = null,
    Object? cycleTime = freezed,
    Object? url = freezed,
    Object? parent1 = freezed,
    Object? parent2 = freezed,
    Object? lineageJson = freezed,
    Object? seedfinderId = freezed,
    Object? thcContent = freezed,
    Object? cbdContent = freezed,
    Object? floweringType = freezed,
  }) {
    return _then(
      _value.copyWith(
            name: null == name
                ? _value.name
                : name // ignore: cast_nullable_to_non_nullable
                      as String,
            breederId: freezed == breederId
                ? _value.breederId
                : breederId // ignore: cast_nullable_to_non_nullable
                      as int?,
            indica: null == indica
                ? _value.indica
                : indica // ignore: cast_nullable_to_non_nullable
                      as int,
            sativa: null == sativa
                ? _value.sativa
                : sativa // ignore: cast_nullable_to_non_nullable
                      as int,
            autoflower: null == autoflower
                ? _value.autoflower
                : autoflower // ignore: cast_nullable_to_non_nullable
                      as bool,
            description: freezed == description
                ? _value.description
                : description // ignore: cast_nullable_to_non_nullable
                      as String?,
            seedCount: null == seedCount
                ? _value.seedCount
                : seedCount // ignore: cast_nullable_to_non_nullable
                      as int,
            cycleTime: freezed == cycleTime
                ? _value.cycleTime
                : cycleTime // ignore: cast_nullable_to_non_nullable
                      as int?,
            url: freezed == url
                ? _value.url
                : url // ignore: cast_nullable_to_non_nullable
                      as String?,
            parent1: freezed == parent1
                ? _value.parent1
                : parent1 // ignore: cast_nullable_to_non_nullable
                      as String?,
            parent2: freezed == parent2
                ? _value.parent2
                : parent2 // ignore: cast_nullable_to_non_nullable
                      as String?,
            lineageJson: freezed == lineageJson
                ? _value.lineageJson
                : lineageJson // ignore: cast_nullable_to_non_nullable
                      as Map<String, dynamic>?,
            seedfinderId: freezed == seedfinderId
                ? _value.seedfinderId
                : seedfinderId // ignore: cast_nullable_to_non_nullable
                      as String?,
            thcContent: freezed == thcContent
                ? _value.thcContent
                : thcContent // ignore: cast_nullable_to_non_nullable
                      as double?,
            cbdContent: freezed == cbdContent
                ? _value.cbdContent
                : cbdContent // ignore: cast_nullable_to_non_nullable
                      as double?,
            floweringType: freezed == floweringType
                ? _value.floweringType
                : floweringType // ignore: cast_nullable_to_non_nullable
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
    int? breederId,
    int indica,
    int sativa,
    bool autoflower,
    String? description,
    int seedCount,
    int? cycleTime,
    String? url,
    String? parent1,
    String? parent2,
    Map<String, dynamic>? lineageJson,
    String? seedfinderId,
    double? thcContent,
    double? cbdContent,
    String? floweringType,
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
    Object? breederId = freezed,
    Object? indica = null,
    Object? sativa = null,
    Object? autoflower = null,
    Object? description = freezed,
    Object? seedCount = null,
    Object? cycleTime = freezed,
    Object? url = freezed,
    Object? parent1 = freezed,
    Object? parent2 = freezed,
    Object? lineageJson = freezed,
    Object? seedfinderId = freezed,
    Object? thcContent = freezed,
    Object? cbdContent = freezed,
    Object? floweringType = freezed,
  }) {
    return _then(
      _$CultivarCreateImpl(
        name: null == name
            ? _value.name
            : name // ignore: cast_nullable_to_non_nullable
                  as String,
        breederId: freezed == breederId
            ? _value.breederId
            : breederId // ignore: cast_nullable_to_non_nullable
                  as int?,
        indica: null == indica
            ? _value.indica
            : indica // ignore: cast_nullable_to_non_nullable
                  as int,
        sativa: null == sativa
            ? _value.sativa
            : sativa // ignore: cast_nullable_to_non_nullable
                  as int,
        autoflower: null == autoflower
            ? _value.autoflower
            : autoflower // ignore: cast_nullable_to_non_nullable
                  as bool,
        description: freezed == description
            ? _value.description
            : description // ignore: cast_nullable_to_non_nullable
                  as String?,
        seedCount: null == seedCount
            ? _value.seedCount
            : seedCount // ignore: cast_nullable_to_non_nullable
                  as int,
        cycleTime: freezed == cycleTime
            ? _value.cycleTime
            : cycleTime // ignore: cast_nullable_to_non_nullable
                  as int?,
        url: freezed == url
            ? _value.url
            : url // ignore: cast_nullable_to_non_nullable
                  as String?,
        parent1: freezed == parent1
            ? _value.parent1
            : parent1 // ignore: cast_nullable_to_non_nullable
                  as String?,
        parent2: freezed == parent2
            ? _value.parent2
            : parent2 // ignore: cast_nullable_to_non_nullable
                  as String?,
        lineageJson: freezed == lineageJson
            ? _value._lineageJson
            : lineageJson // ignore: cast_nullable_to_non_nullable
                  as Map<String, dynamic>?,
        seedfinderId: freezed == seedfinderId
            ? _value.seedfinderId
            : seedfinderId // ignore: cast_nullable_to_non_nullable
                  as String?,
        thcContent: freezed == thcContent
            ? _value.thcContent
            : thcContent // ignore: cast_nullable_to_non_nullable
                  as double?,
        cbdContent: freezed == cbdContent
            ? _value.cbdContent
            : cbdContent // ignore: cast_nullable_to_non_nullable
                  as double?,
        floweringType: freezed == floweringType
            ? _value.floweringType
            : floweringType // ignore: cast_nullable_to_non_nullable
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
    this.breederId,
    this.indica = 0,
    this.sativa = 0,
    this.autoflower = false,
    this.description,
    this.seedCount = 0,
    this.cycleTime,
    this.url,
    this.parent1,
    this.parent2,
    final Map<String, dynamic>? lineageJson,
    this.seedfinderId,
    this.thcContent,
    this.cbdContent,
    this.floweringType,
  }) : _lineageJson = lineageJson;

  factory _$CultivarCreateImpl.fromJson(Map<String, dynamic> json) =>
      _$$CultivarCreateImplFromJson(json);

  @override
  final String name;
  @override
  final int? breederId;
  @override
  @JsonKey()
  final int indica;
  @override
  @JsonKey()
  final int sativa;
  @override
  @JsonKey()
  final bool autoflower;
  @override
  final String? description;
  @override
  @JsonKey()
  final int seedCount;
  @override
  final int? cycleTime;
  @override
  final String? url;
  @override
  final String? parent1;
  @override
  final String? parent2;
  final Map<String, dynamic>? _lineageJson;
  @override
  Map<String, dynamic>? get lineageJson {
    final value = _lineageJson;
    if (value == null) return null;
    if (_lineageJson is EqualUnmodifiableMapView) return _lineageJson;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(value);
  }

  @override
  final String? seedfinderId;
  @override
  final double? thcContent;
  @override
  final double? cbdContent;
  @override
  final String? floweringType;

  @override
  String toString() {
    return 'CultivarCreate(name: $name, breederId: $breederId, indica: $indica, sativa: $sativa, autoflower: $autoflower, description: $description, seedCount: $seedCount, cycleTime: $cycleTime, url: $url, parent1: $parent1, parent2: $parent2, lineageJson: $lineageJson, seedfinderId: $seedfinderId, thcContent: $thcContent, cbdContent: $cbdContent, floweringType: $floweringType)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$CultivarCreateImpl &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.breederId, breederId) ||
                other.breederId == breederId) &&
            (identical(other.indica, indica) || other.indica == indica) &&
            (identical(other.sativa, sativa) || other.sativa == sativa) &&
            (identical(other.autoflower, autoflower) ||
                other.autoflower == autoflower) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.seedCount, seedCount) ||
                other.seedCount == seedCount) &&
            (identical(other.cycleTime, cycleTime) ||
                other.cycleTime == cycleTime) &&
            (identical(other.url, url) || other.url == url) &&
            (identical(other.parent1, parent1) || other.parent1 == parent1) &&
            (identical(other.parent2, parent2) || other.parent2 == parent2) &&
            const DeepCollectionEquality().equals(
              other._lineageJson,
              _lineageJson,
            ) &&
            (identical(other.seedfinderId, seedfinderId) ||
                other.seedfinderId == seedfinderId) &&
            (identical(other.thcContent, thcContent) ||
                other.thcContent == thcContent) &&
            (identical(other.cbdContent, cbdContent) ||
                other.cbdContent == cbdContent) &&
            (identical(other.floweringType, floweringType) ||
                other.floweringType == floweringType));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    name,
    breederId,
    indica,
    sativa,
    autoflower,
    description,
    seedCount,
    cycleTime,
    url,
    parent1,
    parent2,
    const DeepCollectionEquality().hash(_lineageJson),
    seedfinderId,
    thcContent,
    cbdContent,
    floweringType,
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
    final int? breederId,
    final int indica,
    final int sativa,
    final bool autoflower,
    final String? description,
    final int seedCount,
    final int? cycleTime,
    final String? url,
    final String? parent1,
    final String? parent2,
    final Map<String, dynamic>? lineageJson,
    final String? seedfinderId,
    final double? thcContent,
    final double? cbdContent,
    final String? floweringType,
  }) = _$CultivarCreateImpl;

  factory _CultivarCreate.fromJson(Map<String, dynamic> json) =
      _$CultivarCreateImpl.fromJson;

  @override
  String get name;
  @override
  int? get breederId;
  @override
  int get indica;
  @override
  int get sativa;
  @override
  bool get autoflower;
  @override
  String? get description;
  @override
  int get seedCount;
  @override
  int? get cycleTime;
  @override
  String? get url;
  @override
  String? get parent1;
  @override
  String? get parent2;
  @override
  Map<String, dynamic>? get lineageJson;
  @override
  String? get seedfinderId;
  @override
  double? get thcContent;
  @override
  double? get cbdContent;
  @override
  String? get floweringType;

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
  int? get breederId => throw _privateConstructorUsedError;
  int? get indica => throw _privateConstructorUsedError;
  int? get sativa => throw _privateConstructorUsedError;
  bool? get autoflower => throw _privateConstructorUsedError;
  String? get description => throw _privateConstructorUsedError;
  int? get seedCount => throw _privateConstructorUsedError;
  int? get cycleTime => throw _privateConstructorUsedError;
  String? get url => throw _privateConstructorUsedError;
  String? get parent1 => throw _privateConstructorUsedError;
  String? get parent2 => throw _privateConstructorUsedError;
  Map<String, dynamic>? get lineageJson => throw _privateConstructorUsedError;
  String? get seedfinderId => throw _privateConstructorUsedError;
  double? get thcContent => throw _privateConstructorUsedError;
  double? get cbdContent => throw _privateConstructorUsedError;
  String? get floweringType => throw _privateConstructorUsedError;

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
    Object? breederId = freezed,
    Object? indica = freezed,
    Object? sativa = freezed,
    Object? autoflower = freezed,
    Object? description = freezed,
    Object? seedCount = freezed,
    Object? cycleTime = freezed,
    Object? url = freezed,
    Object? parent1 = freezed,
    Object? parent2 = freezed,
    Object? lineageJson = freezed,
    Object? seedfinderId = freezed,
    Object? thcContent = freezed,
    Object? cbdContent = freezed,
    Object? floweringType = freezed,
  }) {
    return _then(
      _value.copyWith(
            name: freezed == name
                ? _value.name
                : name // ignore: cast_nullable_to_non_nullable
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
            autoflower: freezed == autoflower
                ? _value.autoflower
                : autoflower // ignore: cast_nullable_to_non_nullable
                      as bool?,
            description: freezed == description
                ? _value.description
                : description // ignore: cast_nullable_to_non_nullable
                      as String?,
            seedCount: freezed == seedCount
                ? _value.seedCount
                : seedCount // ignore: cast_nullable_to_non_nullable
                      as int?,
            cycleTime: freezed == cycleTime
                ? _value.cycleTime
                : cycleTime // ignore: cast_nullable_to_non_nullable
                      as int?,
            url: freezed == url
                ? _value.url
                : url // ignore: cast_nullable_to_non_nullable
                      as String?,
            parent1: freezed == parent1
                ? _value.parent1
                : parent1 // ignore: cast_nullable_to_non_nullable
                      as String?,
            parent2: freezed == parent2
                ? _value.parent2
                : parent2 // ignore: cast_nullable_to_non_nullable
                      as String?,
            lineageJson: freezed == lineageJson
                ? _value.lineageJson
                : lineageJson // ignore: cast_nullable_to_non_nullable
                      as Map<String, dynamic>?,
            seedfinderId: freezed == seedfinderId
                ? _value.seedfinderId
                : seedfinderId // ignore: cast_nullable_to_non_nullable
                      as String?,
            thcContent: freezed == thcContent
                ? _value.thcContent
                : thcContent // ignore: cast_nullable_to_non_nullable
                      as double?,
            cbdContent: freezed == cbdContent
                ? _value.cbdContent
                : cbdContent // ignore: cast_nullable_to_non_nullable
                      as double?,
            floweringType: freezed == floweringType
                ? _value.floweringType
                : floweringType // ignore: cast_nullable_to_non_nullable
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
    Object? breederId = freezed,
    Object? indica = freezed,
    Object? sativa = freezed,
    Object? autoflower = freezed,
    Object? description = freezed,
    Object? seedCount = freezed,
    Object? cycleTime = freezed,
    Object? url = freezed,
    Object? parent1 = freezed,
    Object? parent2 = freezed,
    Object? lineageJson = freezed,
    Object? seedfinderId = freezed,
    Object? thcContent = freezed,
    Object? cbdContent = freezed,
    Object? floweringType = freezed,
  }) {
    return _then(
      _$CultivarUpdateImpl(
        name: freezed == name
            ? _value.name
            : name // ignore: cast_nullable_to_non_nullable
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
        autoflower: freezed == autoflower
            ? _value.autoflower
            : autoflower // ignore: cast_nullable_to_non_nullable
                  as bool?,
        description: freezed == description
            ? _value.description
            : description // ignore: cast_nullable_to_non_nullable
                  as String?,
        seedCount: freezed == seedCount
            ? _value.seedCount
            : seedCount // ignore: cast_nullable_to_non_nullable
                  as int?,
        cycleTime: freezed == cycleTime
            ? _value.cycleTime
            : cycleTime // ignore: cast_nullable_to_non_nullable
                  as int?,
        url: freezed == url
            ? _value.url
            : url // ignore: cast_nullable_to_non_nullable
                  as String?,
        parent1: freezed == parent1
            ? _value.parent1
            : parent1 // ignore: cast_nullable_to_non_nullable
                  as String?,
        parent2: freezed == parent2
            ? _value.parent2
            : parent2 // ignore: cast_nullable_to_non_nullable
                  as String?,
        lineageJson: freezed == lineageJson
            ? _value._lineageJson
            : lineageJson // ignore: cast_nullable_to_non_nullable
                  as Map<String, dynamic>?,
        seedfinderId: freezed == seedfinderId
            ? _value.seedfinderId
            : seedfinderId // ignore: cast_nullable_to_non_nullable
                  as String?,
        thcContent: freezed == thcContent
            ? _value.thcContent
            : thcContent // ignore: cast_nullable_to_non_nullable
                  as double?,
        cbdContent: freezed == cbdContent
            ? _value.cbdContent
            : cbdContent // ignore: cast_nullable_to_non_nullable
                  as double?,
        floweringType: freezed == floweringType
            ? _value.floweringType
            : floweringType // ignore: cast_nullable_to_non_nullable
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
    this.breederId,
    this.indica,
    this.sativa,
    this.autoflower,
    this.description,
    this.seedCount,
    this.cycleTime,
    this.url,
    this.parent1,
    this.parent2,
    final Map<String, dynamic>? lineageJson,
    this.seedfinderId,
    this.thcContent,
    this.cbdContent,
    this.floweringType,
  }) : _lineageJson = lineageJson;

  factory _$CultivarUpdateImpl.fromJson(Map<String, dynamic> json) =>
      _$$CultivarUpdateImplFromJson(json);

  @override
  final String? name;
  @override
  final int? breederId;
  @override
  final int? indica;
  @override
  final int? sativa;
  @override
  final bool? autoflower;
  @override
  final String? description;
  @override
  final int? seedCount;
  @override
  final int? cycleTime;
  @override
  final String? url;
  @override
  final String? parent1;
  @override
  final String? parent2;
  final Map<String, dynamic>? _lineageJson;
  @override
  Map<String, dynamic>? get lineageJson {
    final value = _lineageJson;
    if (value == null) return null;
    if (_lineageJson is EqualUnmodifiableMapView) return _lineageJson;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableMapView(value);
  }

  @override
  final String? seedfinderId;
  @override
  final double? thcContent;
  @override
  final double? cbdContent;
  @override
  final String? floweringType;

  @override
  String toString() {
    return 'CultivarUpdate(name: $name, breederId: $breederId, indica: $indica, sativa: $sativa, autoflower: $autoflower, description: $description, seedCount: $seedCount, cycleTime: $cycleTime, url: $url, parent1: $parent1, parent2: $parent2, lineageJson: $lineageJson, seedfinderId: $seedfinderId, thcContent: $thcContent, cbdContent: $cbdContent, floweringType: $floweringType)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$CultivarUpdateImpl &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.breederId, breederId) ||
                other.breederId == breederId) &&
            (identical(other.indica, indica) || other.indica == indica) &&
            (identical(other.sativa, sativa) || other.sativa == sativa) &&
            (identical(other.autoflower, autoflower) ||
                other.autoflower == autoflower) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.seedCount, seedCount) ||
                other.seedCount == seedCount) &&
            (identical(other.cycleTime, cycleTime) ||
                other.cycleTime == cycleTime) &&
            (identical(other.url, url) || other.url == url) &&
            (identical(other.parent1, parent1) || other.parent1 == parent1) &&
            (identical(other.parent2, parent2) || other.parent2 == parent2) &&
            const DeepCollectionEquality().equals(
              other._lineageJson,
              _lineageJson,
            ) &&
            (identical(other.seedfinderId, seedfinderId) ||
                other.seedfinderId == seedfinderId) &&
            (identical(other.thcContent, thcContent) ||
                other.thcContent == thcContent) &&
            (identical(other.cbdContent, cbdContent) ||
                other.cbdContent == cbdContent) &&
            (identical(other.floweringType, floweringType) ||
                other.floweringType == floweringType));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    name,
    breederId,
    indica,
    sativa,
    autoflower,
    description,
    seedCount,
    cycleTime,
    url,
    parent1,
    parent2,
    const DeepCollectionEquality().hash(_lineageJson),
    seedfinderId,
    thcContent,
    cbdContent,
    floweringType,
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
    final int? breederId,
    final int? indica,
    final int? sativa,
    final bool? autoflower,
    final String? description,
    final int? seedCount,
    final int? cycleTime,
    final String? url,
    final String? parent1,
    final String? parent2,
    final Map<String, dynamic>? lineageJson,
    final String? seedfinderId,
    final double? thcContent,
    final double? cbdContent,
    final String? floweringType,
  }) = _$CultivarUpdateImpl;

  factory _CultivarUpdate.fromJson(Map<String, dynamic> json) =
      _$CultivarUpdateImpl.fromJson;

  @override
  String? get name;
  @override
  int? get breederId;
  @override
  int? get indica;
  @override
  int? get sativa;
  @override
  bool? get autoflower;
  @override
  String? get description;
  @override
  int? get seedCount;
  @override
  int? get cycleTime;
  @override
  String? get url;
  @override
  String? get parent1;
  @override
  String? get parent2;
  @override
  Map<String, dynamic>? get lineageJson;
  @override
  String? get seedfinderId;
  @override
  double? get thcContent;
  @override
  double? get cbdContent;
  @override
  String? get floweringType;

  /// Create a copy of CultivarUpdate
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$CultivarUpdateImplCopyWith<_$CultivarUpdateImpl> get copyWith =>
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
  int? get breederId => throw _privateConstructorUsedError;
  bool? get autoflower => throw _privateConstructorUsedError;
  String? get sortBy => throw _privateConstructorUsedError;
  String get sortOrder => throw _privateConstructorUsedError;

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
    int? breederId,
    bool? autoflower,
    String? sortBy,
    String sortOrder,
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
    Object? breederId = freezed,
    Object? autoflower = freezed,
    Object? sortBy = freezed,
    Object? sortOrder = null,
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
            breederId: freezed == breederId
                ? _value.breederId
                : breederId // ignore: cast_nullable_to_non_nullable
                      as int?,
            autoflower: freezed == autoflower
                ? _value.autoflower
                : autoflower // ignore: cast_nullable_to_non_nullable
                      as bool?,
            sortBy: freezed == sortBy
                ? _value.sortBy
                : sortBy // ignore: cast_nullable_to_non_nullable
                      as String?,
            sortOrder: null == sortOrder
                ? _value.sortOrder
                : sortOrder // ignore: cast_nullable_to_non_nullable
                      as String,
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
    int? breederId,
    bool? autoflower,
    String? sortBy,
    String sortOrder,
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
    Object? breederId = freezed,
    Object? autoflower = freezed,
    Object? sortBy = freezed,
    Object? sortOrder = null,
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
        breederId: freezed == breederId
            ? _value.breederId
            : breederId // ignore: cast_nullable_to_non_nullable
                  as int?,
        autoflower: freezed == autoflower
            ? _value.autoflower
            : autoflower // ignore: cast_nullable_to_non_nullable
                  as bool?,
        sortBy: freezed == sortBy
            ? _value.sortBy
            : sortBy // ignore: cast_nullable_to_non_nullable
                  as String?,
        sortOrder: null == sortOrder
            ? _value.sortOrder
            : sortOrder // ignore: cast_nullable_to_non_nullable
                  as String,
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
    this.breederId,
    this.autoflower,
    this.sortBy,
    this.sortOrder = 'asc',
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
  final int? breederId;
  @override
  final bool? autoflower;
  @override
  final String? sortBy;
  @override
  @JsonKey()
  final String sortOrder;

  @override
  String toString() {
    return 'StrainsParams(page: $page, limit: $limit, search: $search, breederId: $breederId, autoflower: $autoflower, sortBy: $sortBy, sortOrder: $sortOrder)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$StrainsParamsImpl &&
            (identical(other.page, page) || other.page == page) &&
            (identical(other.limit, limit) || other.limit == limit) &&
            (identical(other.search, search) || other.search == search) &&
            (identical(other.breederId, breederId) ||
                other.breederId == breederId) &&
            (identical(other.autoflower, autoflower) ||
                other.autoflower == autoflower) &&
            (identical(other.sortBy, sortBy) || other.sortBy == sortBy) &&
            (identical(other.sortOrder, sortOrder) ||
                other.sortOrder == sortOrder));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    page,
    limit,
    search,
    breederId,
    autoflower,
    sortBy,
    sortOrder,
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
    final int? breederId,
    final bool? autoflower,
    final String? sortBy,
    final String sortOrder,
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
  int? get breederId;
  @override
  bool? get autoflower;
  @override
  String? get sortBy;
  @override
  String get sortOrder;

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
  int get pages => throw _privateConstructorUsedError;
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
    int pages,
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
    Object? pages = null,
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
    int pages,
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
    Object? pages = null,
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
class _$PaginatedStrainsResponseImpl extends _PaginatedStrainsResponse {
  const _$PaginatedStrainsResponseImpl({
    required final List<Cultivar> data,
    required this.total,
    required this.page,
    required this.limit,
    required this.pages,
    this.hasNext = false,
    this.hasPrev = false,
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
  final int pages;
  @override
  @JsonKey()
  final bool hasNext;
  @override
  @JsonKey()
  final bool hasPrev;

  @override
  String toString() {
    return 'PaginatedStrainsResponse(data: $data, total: $total, page: $page, limit: $limit, pages: $pages, hasNext: $hasNext, hasPrev: $hasPrev)';
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
            (identical(other.pages, pages) || other.pages == pages) &&
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
    pages,
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
    required final int pages,
    final bool hasNext,
    final bool hasPrev,
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
  int get pages;
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
  int get indicaCount => throw _privateConstructorUsedError;
  int get sativaCount => throw _privateConstructorUsedError;
  int get hybridCount => throw _privateConstructorUsedError;
  int get autoflowerCount => throw _privateConstructorUsedError;
  double? get averageCycleTime => throw _privateConstructorUsedError;

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
    int indicaCount,
    int sativaCount,
    int hybridCount,
    int autoflowerCount,
    double? averageCycleTime,
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
    Object? indicaCount = null,
    Object? sativaCount = null,
    Object? hybridCount = null,
    Object? autoflowerCount = null,
    Object? averageCycleTime = freezed,
  }) {
    return _then(
      _value.copyWith(
            totalCultivars: null == totalCultivars
                ? _value.totalCultivars
                : totalCultivars // ignore: cast_nullable_to_non_nullable
                      as int,
            indicaCount: null == indicaCount
                ? _value.indicaCount
                : indicaCount // ignore: cast_nullable_to_non_nullable
                      as int,
            sativaCount: null == sativaCount
                ? _value.sativaCount
                : sativaCount // ignore: cast_nullable_to_non_nullable
                      as int,
            hybridCount: null == hybridCount
                ? _value.hybridCount
                : hybridCount // ignore: cast_nullable_to_non_nullable
                      as int,
            autoflowerCount: null == autoflowerCount
                ? _value.autoflowerCount
                : autoflowerCount // ignore: cast_nullable_to_non_nullable
                      as int,
            averageCycleTime: freezed == averageCycleTime
                ? _value.averageCycleTime
                : averageCycleTime // ignore: cast_nullable_to_non_nullable
                      as double?,
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
    int indicaCount,
    int sativaCount,
    int hybridCount,
    int autoflowerCount,
    double? averageCycleTime,
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
    Object? indicaCount = null,
    Object? sativaCount = null,
    Object? hybridCount = null,
    Object? autoflowerCount = null,
    Object? averageCycleTime = freezed,
  }) {
    return _then(
      _$CultivarStatsImpl(
        totalCultivars: null == totalCultivars
            ? _value.totalCultivars
            : totalCultivars // ignore: cast_nullable_to_non_nullable
                  as int,
        indicaCount: null == indicaCount
            ? _value.indicaCount
            : indicaCount // ignore: cast_nullable_to_non_nullable
                  as int,
        sativaCount: null == sativaCount
            ? _value.sativaCount
            : sativaCount // ignore: cast_nullable_to_non_nullable
                  as int,
        hybridCount: null == hybridCount
            ? _value.hybridCount
            : hybridCount // ignore: cast_nullable_to_non_nullable
                  as int,
        autoflowerCount: null == autoflowerCount
            ? _value.autoflowerCount
            : autoflowerCount // ignore: cast_nullable_to_non_nullable
                  as int,
        averageCycleTime: freezed == averageCycleTime
            ? _value.averageCycleTime
            : averageCycleTime // ignore: cast_nullable_to_non_nullable
                  as double?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$CultivarStatsImpl implements _CultivarStats {
  const _$CultivarStatsImpl({
    required this.totalCultivars,
    required this.indicaCount,
    required this.sativaCount,
    required this.hybridCount,
    required this.autoflowerCount,
    this.averageCycleTime,
  });

  factory _$CultivarStatsImpl.fromJson(Map<String, dynamic> json) =>
      _$$CultivarStatsImplFromJson(json);

  @override
  final int totalCultivars;
  @override
  final int indicaCount;
  @override
  final int sativaCount;
  @override
  final int hybridCount;
  @override
  final int autoflowerCount;
  @override
  final double? averageCycleTime;

  @override
  String toString() {
    return 'CultivarStats(totalCultivars: $totalCultivars, indicaCount: $indicaCount, sativaCount: $sativaCount, hybridCount: $hybridCount, autoflowerCount: $autoflowerCount, averageCycleTime: $averageCycleTime)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$CultivarStatsImpl &&
            (identical(other.totalCultivars, totalCultivars) ||
                other.totalCultivars == totalCultivars) &&
            (identical(other.indicaCount, indicaCount) ||
                other.indicaCount == indicaCount) &&
            (identical(other.sativaCount, sativaCount) ||
                other.sativaCount == sativaCount) &&
            (identical(other.hybridCount, hybridCount) ||
                other.hybridCount == hybridCount) &&
            (identical(other.autoflowerCount, autoflowerCount) ||
                other.autoflowerCount == autoflowerCount) &&
            (identical(other.averageCycleTime, averageCycleTime) ||
                other.averageCycleTime == averageCycleTime));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    totalCultivars,
    indicaCount,
    sativaCount,
    hybridCount,
    autoflowerCount,
    averageCycleTime,
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
    required final int indicaCount,
    required final int sativaCount,
    required final int hybridCount,
    required final int autoflowerCount,
    final double? averageCycleTime,
  }) = _$CultivarStatsImpl;

  factory _CultivarStats.fromJson(Map<String, dynamic> json) =
      _$CultivarStatsImpl.fromJson;

  @override
  int get totalCultivars;
  @override
  int get indicaCount;
  @override
  int get sativaCount;
  @override
  int get hybridCount;
  @override
  int get autoflowerCount;
  @override
  double? get averageCycleTime;

  /// Create a copy of CultivarStats
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$CultivarStatsImplCopyWith<_$CultivarStatsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
