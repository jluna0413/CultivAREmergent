// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'strain.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

Strain _$StrainFromJson(Map<String, dynamic> json) {
  return _Strain.fromJson(json);
}

/// @nodoc
mixin _$Strain {
  String get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String get breederName => throw _privateConstructorUsedError;
  VerificationBadge get badge => throw _privateConstructorUsedError;
  String get imageUrl => throw _privateConstructorUsedError;
  double get thcPercentage => throw _privateConstructorUsedError;
  double get cbdPercentage => throw _privateConstructorUsedError;
  int get flowerTimeWeeks => throw _privateConstructorUsedError;
  bool get isIndica => throw _privateConstructorUsedError;
  bool get isSativa => throw _privateConstructorUsedError;
  double get price => throw _privateConstructorUsedError; // G-NFT Price
  int get availableStock => throw _privateConstructorUsedError;
  String? get parent1Name => throw _privateConstructorUsedError;
  String? get parent2Name => throw _privateConstructorUsedError;

  /// Serializes this Strain to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of Strain
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $StrainCopyWith<Strain> get copyWith => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $StrainCopyWith<$Res> {
  factory $StrainCopyWith(Strain value, $Res Function(Strain) then) =
      _$StrainCopyWithImpl<$Res, Strain>;
  @useResult
  $Res call({
    String id,
    String name,
    String breederName,
    VerificationBadge badge,
    String imageUrl,
    double thcPercentage,
    double cbdPercentage,
    int flowerTimeWeeks,
    bool isIndica,
    bool isSativa,
    double price,
    int availableStock,
    String? parent1Name,
    String? parent2Name,
  });
}

/// @nodoc
class _$StrainCopyWithImpl<$Res, $Val extends Strain>
    implements $StrainCopyWith<$Res> {
  _$StrainCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of Strain
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? breederName = null,
    Object? badge = null,
    Object? imageUrl = null,
    Object? thcPercentage = null,
    Object? cbdPercentage = null,
    Object? flowerTimeWeeks = null,
    Object? isIndica = null,
    Object? isSativa = null,
    Object? price = null,
    Object? availableStock = null,
    Object? parent1Name = freezed,
    Object? parent2Name = freezed,
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
            breederName: null == breederName
                ? _value.breederName
                : breederName // ignore: cast_nullable_to_non_nullable
                      as String,
            badge: null == badge
                ? _value.badge
                : badge // ignore: cast_nullable_to_non_nullable
                      as VerificationBadge,
            imageUrl: null == imageUrl
                ? _value.imageUrl
                : imageUrl // ignore: cast_nullable_to_non_nullable
                      as String,
            thcPercentage: null == thcPercentage
                ? _value.thcPercentage
                : thcPercentage // ignore: cast_nullable_to_non_nullable
                      as double,
            cbdPercentage: null == cbdPercentage
                ? _value.cbdPercentage
                : cbdPercentage // ignore: cast_nullable_to_non_nullable
                      as double,
            flowerTimeWeeks: null == flowerTimeWeeks
                ? _value.flowerTimeWeeks
                : flowerTimeWeeks // ignore: cast_nullable_to_non_nullable
                      as int,
            isIndica: null == isIndica
                ? _value.isIndica
                : isIndica // ignore: cast_nullable_to_non_nullable
                      as bool,
            isSativa: null == isSativa
                ? _value.isSativa
                : isSativa // ignore: cast_nullable_to_non_nullable
                      as bool,
            price: null == price
                ? _value.price
                : price // ignore: cast_nullable_to_non_nullable
                      as double,
            availableStock: null == availableStock
                ? _value.availableStock
                : availableStock // ignore: cast_nullable_to_non_nullable
                      as int,
            parent1Name: freezed == parent1Name
                ? _value.parent1Name
                : parent1Name // ignore: cast_nullable_to_non_nullable
                      as String?,
            parent2Name: freezed == parent2Name
                ? _value.parent2Name
                : parent2Name // ignore: cast_nullable_to_non_nullable
                      as String?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$StrainImplCopyWith<$Res> implements $StrainCopyWith<$Res> {
  factory _$$StrainImplCopyWith(
    _$StrainImpl value,
    $Res Function(_$StrainImpl) then,
  ) = __$$StrainImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String id,
    String name,
    String breederName,
    VerificationBadge badge,
    String imageUrl,
    double thcPercentage,
    double cbdPercentage,
    int flowerTimeWeeks,
    bool isIndica,
    bool isSativa,
    double price,
    int availableStock,
    String? parent1Name,
    String? parent2Name,
  });
}

/// @nodoc
class __$$StrainImplCopyWithImpl<$Res>
    extends _$StrainCopyWithImpl<$Res, _$StrainImpl>
    implements _$$StrainImplCopyWith<$Res> {
  __$$StrainImplCopyWithImpl(
    _$StrainImpl _value,
    $Res Function(_$StrainImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of Strain
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? breederName = null,
    Object? badge = null,
    Object? imageUrl = null,
    Object? thcPercentage = null,
    Object? cbdPercentage = null,
    Object? flowerTimeWeeks = null,
    Object? isIndica = null,
    Object? isSativa = null,
    Object? price = null,
    Object? availableStock = null,
    Object? parent1Name = freezed,
    Object? parent2Name = freezed,
  }) {
    return _then(
      _$StrainImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as String,
        name: null == name
            ? _value.name
            : name // ignore: cast_nullable_to_non_nullable
                  as String,
        breederName: null == breederName
            ? _value.breederName
            : breederName // ignore: cast_nullable_to_non_nullable
                  as String,
        badge: null == badge
            ? _value.badge
            : badge // ignore: cast_nullable_to_non_nullable
                  as VerificationBadge,
        imageUrl: null == imageUrl
            ? _value.imageUrl
            : imageUrl // ignore: cast_nullable_to_non_nullable
                  as String,
        thcPercentage: null == thcPercentage
            ? _value.thcPercentage
            : thcPercentage // ignore: cast_nullable_to_non_nullable
                  as double,
        cbdPercentage: null == cbdPercentage
            ? _value.cbdPercentage
            : cbdPercentage // ignore: cast_nullable_to_non_nullable
                  as double,
        flowerTimeWeeks: null == flowerTimeWeeks
            ? _value.flowerTimeWeeks
            : flowerTimeWeeks // ignore: cast_nullable_to_non_nullable
                  as int,
        isIndica: null == isIndica
            ? _value.isIndica
            : isIndica // ignore: cast_nullable_to_non_nullable
                  as bool,
        isSativa: null == isSativa
            ? _value.isSativa
            : isSativa // ignore: cast_nullable_to_non_nullable
                  as bool,
        price: null == price
            ? _value.price
            : price // ignore: cast_nullable_to_non_nullable
                  as double,
        availableStock: null == availableStock
            ? _value.availableStock
            : availableStock // ignore: cast_nullable_to_non_nullable
                  as int,
        parent1Name: freezed == parent1Name
            ? _value.parent1Name
            : parent1Name // ignore: cast_nullable_to_non_nullable
                  as String?,
        parent2Name: freezed == parent2Name
            ? _value.parent2Name
            : parent2Name // ignore: cast_nullable_to_non_nullable
                  as String?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$StrainImpl implements _Strain {
  const _$StrainImpl({
    required this.id,
    required this.name,
    required this.breederName,
    this.badge = VerificationBadge.none,
    required this.imageUrl,
    required this.thcPercentage,
    required this.cbdPercentage,
    required this.flowerTimeWeeks,
    this.isIndica = false,
    this.isSativa = false,
    this.price = 0.0,
    this.availableStock = 0,
    this.parent1Name,
    this.parent2Name,
  });

  factory _$StrainImpl.fromJson(Map<String, dynamic> json) =>
      _$$StrainImplFromJson(json);

  @override
  final String id;
  @override
  final String name;
  @override
  final String breederName;
  @override
  @JsonKey()
  final VerificationBadge badge;
  @override
  final String imageUrl;
  @override
  final double thcPercentage;
  @override
  final double cbdPercentage;
  @override
  final int flowerTimeWeeks;
  @override
  @JsonKey()
  final bool isIndica;
  @override
  @JsonKey()
  final bool isSativa;
  @override
  @JsonKey()
  final double price;
  // G-NFT Price
  @override
  @JsonKey()
  final int availableStock;
  @override
  final String? parent1Name;
  @override
  final String? parent2Name;

  @override
  String toString() {
    return 'Strain(id: $id, name: $name, breederName: $breederName, badge: $badge, imageUrl: $imageUrl, thcPercentage: $thcPercentage, cbdPercentage: $cbdPercentage, flowerTimeWeeks: $flowerTimeWeeks, isIndica: $isIndica, isSativa: $isSativa, price: $price, availableStock: $availableStock, parent1Name: $parent1Name, parent2Name: $parent2Name)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$StrainImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.breederName, breederName) ||
                other.breederName == breederName) &&
            (identical(other.badge, badge) || other.badge == badge) &&
            (identical(other.imageUrl, imageUrl) ||
                other.imageUrl == imageUrl) &&
            (identical(other.thcPercentage, thcPercentage) ||
                other.thcPercentage == thcPercentage) &&
            (identical(other.cbdPercentage, cbdPercentage) ||
                other.cbdPercentage == cbdPercentage) &&
            (identical(other.flowerTimeWeeks, flowerTimeWeeks) ||
                other.flowerTimeWeeks == flowerTimeWeeks) &&
            (identical(other.isIndica, isIndica) ||
                other.isIndica == isIndica) &&
            (identical(other.isSativa, isSativa) ||
                other.isSativa == isSativa) &&
            (identical(other.price, price) || other.price == price) &&
            (identical(other.availableStock, availableStock) ||
                other.availableStock == availableStock) &&
            (identical(other.parent1Name, parent1Name) ||
                other.parent1Name == parent1Name) &&
            (identical(other.parent2Name, parent2Name) ||
                other.parent2Name == parent2Name));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    name,
    breederName,
    badge,
    imageUrl,
    thcPercentage,
    cbdPercentage,
    flowerTimeWeeks,
    isIndica,
    isSativa,
    price,
    availableStock,
    parent1Name,
    parent2Name,
  );

  /// Create a copy of Strain
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$StrainImplCopyWith<_$StrainImpl> get copyWith =>
      __$$StrainImplCopyWithImpl<_$StrainImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$StrainImplToJson(this);
  }
}

abstract class _Strain implements Strain {
  const factory _Strain({
    required final String id,
    required final String name,
    required final String breederName,
    final VerificationBadge badge,
    required final String imageUrl,
    required final double thcPercentage,
    required final double cbdPercentage,
    required final int flowerTimeWeeks,
    final bool isIndica,
    final bool isSativa,
    final double price,
    final int availableStock,
    final String? parent1Name,
    final String? parent2Name,
  }) = _$StrainImpl;

  factory _Strain.fromJson(Map<String, dynamic> json) = _$StrainImpl.fromJson;

  @override
  String get id;
  @override
  String get name;
  @override
  String get breederName;
  @override
  VerificationBadge get badge;
  @override
  String get imageUrl;
  @override
  double get thcPercentage;
  @override
  double get cbdPercentage;
  @override
  int get flowerTimeWeeks;
  @override
  bool get isIndica;
  @override
  bool get isSativa;
  @override
  double get price; // G-NFT Price
  @override
  int get availableStock;
  @override
  String? get parent1Name;
  @override
  String? get parent2Name;

  /// Create a copy of Strain
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$StrainImplCopyWith<_$StrainImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
