// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'marketplace_breeder.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

MarketplaceBreeder _$MarketplaceBreederFromJson(Map<String, dynamic> json) {
  return _MarketplaceBreeder.fromJson(json);
}

/// @nodoc
mixin _$MarketplaceBreeder {
  int get id => throw _privateConstructorUsedError;
  @JsonKey(name: 'user_id')
  int get userId => throw _privateConstructorUsedError;
  @JsonKey(name: 'current_tier')
  String get currentTier => throw _privateConstructorUsedError;
  @JsonKey(name: 'month_sales')
  int get monthSales => throw _privateConstructorUsedError;
  @JsonKey(name: 'active_commission_rate')
  double get activeCommissionRate => throw _privateConstructorUsedError;
  @JsonKey(name: 'total_revenue')
  double get totalRevenue => throw _privateConstructorUsedError;
  @JsonKey(name: 'is_verified')
  bool get isVerified => throw _privateConstructorUsedError;
  @JsonKey(name: 'store_name')
  String? get storeName => throw _privateConstructorUsedError;

  /// Serializes this MarketplaceBreeder to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of MarketplaceBreeder
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $MarketplaceBreederCopyWith<MarketplaceBreeder> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $MarketplaceBreederCopyWith<$Res> {
  factory $MarketplaceBreederCopyWith(
    MarketplaceBreeder value,
    $Res Function(MarketplaceBreeder) then,
  ) = _$MarketplaceBreederCopyWithImpl<$Res, MarketplaceBreeder>;
  @useResult
  $Res call({
    int id,
    @JsonKey(name: 'user_id') int userId,
    @JsonKey(name: 'current_tier') String currentTier,
    @JsonKey(name: 'month_sales') int monthSales,
    @JsonKey(name: 'active_commission_rate') double activeCommissionRate,
    @JsonKey(name: 'total_revenue') double totalRevenue,
    @JsonKey(name: 'is_verified') bool isVerified,
    @JsonKey(name: 'store_name') String? storeName,
  });
}

/// @nodoc
class _$MarketplaceBreederCopyWithImpl<$Res, $Val extends MarketplaceBreeder>
    implements $MarketplaceBreederCopyWith<$Res> {
  _$MarketplaceBreederCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of MarketplaceBreeder
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? currentTier = null,
    Object? monthSales = null,
    Object? activeCommissionRate = null,
    Object? totalRevenue = null,
    Object? isVerified = null,
    Object? storeName = freezed,
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
            currentTier: null == currentTier
                ? _value.currentTier
                : currentTier // ignore: cast_nullable_to_non_nullable
                      as String,
            monthSales: null == monthSales
                ? _value.monthSales
                : monthSales // ignore: cast_nullable_to_non_nullable
                      as int,
            activeCommissionRate: null == activeCommissionRate
                ? _value.activeCommissionRate
                : activeCommissionRate // ignore: cast_nullable_to_non_nullable
                      as double,
            totalRevenue: null == totalRevenue
                ? _value.totalRevenue
                : totalRevenue // ignore: cast_nullable_to_non_nullable
                      as double,
            isVerified: null == isVerified
                ? _value.isVerified
                : isVerified // ignore: cast_nullable_to_non_nullable
                      as bool,
            storeName: freezed == storeName
                ? _value.storeName
                : storeName // ignore: cast_nullable_to_non_nullable
                      as String?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$MarketplaceBreederImplCopyWith<$Res>
    implements $MarketplaceBreederCopyWith<$Res> {
  factory _$$MarketplaceBreederImplCopyWith(
    _$MarketplaceBreederImpl value,
    $Res Function(_$MarketplaceBreederImpl) then,
  ) = __$$MarketplaceBreederImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    int id,
    @JsonKey(name: 'user_id') int userId,
    @JsonKey(name: 'current_tier') String currentTier,
    @JsonKey(name: 'month_sales') int monthSales,
    @JsonKey(name: 'active_commission_rate') double activeCommissionRate,
    @JsonKey(name: 'total_revenue') double totalRevenue,
    @JsonKey(name: 'is_verified') bool isVerified,
    @JsonKey(name: 'store_name') String? storeName,
  });
}

/// @nodoc
class __$$MarketplaceBreederImplCopyWithImpl<$Res>
    extends _$MarketplaceBreederCopyWithImpl<$Res, _$MarketplaceBreederImpl>
    implements _$$MarketplaceBreederImplCopyWith<$Res> {
  __$$MarketplaceBreederImplCopyWithImpl(
    _$MarketplaceBreederImpl _value,
    $Res Function(_$MarketplaceBreederImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of MarketplaceBreeder
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? userId = null,
    Object? currentTier = null,
    Object? monthSales = null,
    Object? activeCommissionRate = null,
    Object? totalRevenue = null,
    Object? isVerified = null,
    Object? storeName = freezed,
  }) {
    return _then(
      _$MarketplaceBreederImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as int,
        userId: null == userId
            ? _value.userId
            : userId // ignore: cast_nullable_to_non_nullable
                  as int,
        currentTier: null == currentTier
            ? _value.currentTier
            : currentTier // ignore: cast_nullable_to_non_nullable
                  as String,
        monthSales: null == monthSales
            ? _value.monthSales
            : monthSales // ignore: cast_nullable_to_non_nullable
                  as int,
        activeCommissionRate: null == activeCommissionRate
            ? _value.activeCommissionRate
            : activeCommissionRate // ignore: cast_nullable_to_non_nullable
                  as double,
        totalRevenue: null == totalRevenue
            ? _value.totalRevenue
            : totalRevenue // ignore: cast_nullable_to_non_nullable
                  as double,
        isVerified: null == isVerified
            ? _value.isVerified
            : isVerified // ignore: cast_nullable_to_non_nullable
                  as bool,
        storeName: freezed == storeName
            ? _value.storeName
            : storeName // ignore: cast_nullable_to_non_nullable
                  as String?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$MarketplaceBreederImpl implements _MarketplaceBreeder {
  const _$MarketplaceBreederImpl({
    required this.id,
    @JsonKey(name: 'user_id') required this.userId,
    @JsonKey(name: 'current_tier') this.currentTier = 'Starter',
    @JsonKey(name: 'month_sales') this.monthSales = 0,
    @JsonKey(name: 'active_commission_rate') this.activeCommissionRate = 0.25,
    @JsonKey(name: 'total_revenue') this.totalRevenue = 0.0,
    @JsonKey(name: 'is_verified') this.isVerified = false,
    @JsonKey(name: 'store_name') this.storeName,
  });

  factory _$MarketplaceBreederImpl.fromJson(Map<String, dynamic> json) =>
      _$$MarketplaceBreederImplFromJson(json);

  @override
  final int id;
  @override
  @JsonKey(name: 'user_id')
  final int userId;
  @override
  @JsonKey(name: 'current_tier')
  final String currentTier;
  @override
  @JsonKey(name: 'month_sales')
  final int monthSales;
  @override
  @JsonKey(name: 'active_commission_rate')
  final double activeCommissionRate;
  @override
  @JsonKey(name: 'total_revenue')
  final double totalRevenue;
  @override
  @JsonKey(name: 'is_verified')
  final bool isVerified;
  @override
  @JsonKey(name: 'store_name')
  final String? storeName;

  @override
  String toString() {
    return 'MarketplaceBreeder(id: $id, userId: $userId, currentTier: $currentTier, monthSales: $monthSales, activeCommissionRate: $activeCommissionRate, totalRevenue: $totalRevenue, isVerified: $isVerified, storeName: $storeName)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$MarketplaceBreederImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.userId, userId) || other.userId == userId) &&
            (identical(other.currentTier, currentTier) ||
                other.currentTier == currentTier) &&
            (identical(other.monthSales, monthSales) ||
                other.monthSales == monthSales) &&
            (identical(other.activeCommissionRate, activeCommissionRate) ||
                other.activeCommissionRate == activeCommissionRate) &&
            (identical(other.totalRevenue, totalRevenue) ||
                other.totalRevenue == totalRevenue) &&
            (identical(other.isVerified, isVerified) ||
                other.isVerified == isVerified) &&
            (identical(other.storeName, storeName) ||
                other.storeName == storeName));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    userId,
    currentTier,
    monthSales,
    activeCommissionRate,
    totalRevenue,
    isVerified,
    storeName,
  );

  /// Create a copy of MarketplaceBreeder
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$MarketplaceBreederImplCopyWith<_$MarketplaceBreederImpl> get copyWith =>
      __$$MarketplaceBreederImplCopyWithImpl<_$MarketplaceBreederImpl>(
        this,
        _$identity,
      );

  @override
  Map<String, dynamic> toJson() {
    return _$$MarketplaceBreederImplToJson(this);
  }
}

abstract class _MarketplaceBreeder implements MarketplaceBreeder {
  const factory _MarketplaceBreeder({
    required final int id,
    @JsonKey(name: 'user_id') required final int userId,
    @JsonKey(name: 'current_tier') final String currentTier,
    @JsonKey(name: 'month_sales') final int monthSales,
    @JsonKey(name: 'active_commission_rate') final double activeCommissionRate,
    @JsonKey(name: 'total_revenue') final double totalRevenue,
    @JsonKey(name: 'is_verified') final bool isVerified,
    @JsonKey(name: 'store_name') final String? storeName,
  }) = _$MarketplaceBreederImpl;

  factory _MarketplaceBreeder.fromJson(Map<String, dynamic> json) =
      _$MarketplaceBreederImpl.fromJson;

  @override
  int get id;
  @override
  @JsonKey(name: 'user_id')
  int get userId;
  @override
  @JsonKey(name: 'current_tier')
  String get currentTier;
  @override
  @JsonKey(name: 'month_sales')
  int get monthSales;
  @override
  @JsonKey(name: 'active_commission_rate')
  double get activeCommissionRate;
  @override
  @JsonKey(name: 'total_revenue')
  double get totalRevenue;
  @override
  @JsonKey(name: 'is_verified')
  bool get isVerified;
  @override
  @JsonKey(name: 'store_name')
  String? get storeName;

  /// Create a copy of MarketplaceBreeder
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$MarketplaceBreederImplCopyWith<_$MarketplaceBreederImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
