// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'onboarding_state.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

GeneticItem _$GeneticItemFromJson(Map<String, dynamic> json) {
  return _GeneticItem.fromJson(json);
}

/// @nodoc
mixin _$GeneticItem {
  String get id => throw _privateConstructorUsedError;
  String get strainName => throw _privateConstructorUsedError;
  String get breederName => throw _privateConstructorUsedError;
  GeneticType get type => throw _privateConstructorUsedError;
  String? get packagingImageUrl => throw _privateConstructorUsedError;

  /// Serializes this GeneticItem to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of GeneticItem
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $GeneticItemCopyWith<GeneticItem> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $GeneticItemCopyWith<$Res> {
  factory $GeneticItemCopyWith(
    GeneticItem value,
    $Res Function(GeneticItem) then,
  ) = _$GeneticItemCopyWithImpl<$Res, GeneticItem>;
  @useResult
  $Res call({
    String id,
    String strainName,
    String breederName,
    GeneticType type,
    String? packagingImageUrl,
  });
}

/// @nodoc
class _$GeneticItemCopyWithImpl<$Res, $Val extends GeneticItem>
    implements $GeneticItemCopyWith<$Res> {
  _$GeneticItemCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of GeneticItem
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? strainName = null,
    Object? breederName = null,
    Object? type = null,
    Object? packagingImageUrl = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as String,
            strainName: null == strainName
                ? _value.strainName
                : strainName // ignore: cast_nullable_to_non_nullable
                      as String,
            breederName: null == breederName
                ? _value.breederName
                : breederName // ignore: cast_nullable_to_non_nullable
                      as String,
            type: null == type
                ? _value.type
                : type // ignore: cast_nullable_to_non_nullable
                      as GeneticType,
            packagingImageUrl: freezed == packagingImageUrl
                ? _value.packagingImageUrl
                : packagingImageUrl // ignore: cast_nullable_to_non_nullable
                      as String?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$GeneticItemImplCopyWith<$Res>
    implements $GeneticItemCopyWith<$Res> {
  factory _$$GeneticItemImplCopyWith(
    _$GeneticItemImpl value,
    $Res Function(_$GeneticItemImpl) then,
  ) = __$$GeneticItemImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String id,
    String strainName,
    String breederName,
    GeneticType type,
    String? packagingImageUrl,
  });
}

/// @nodoc
class __$$GeneticItemImplCopyWithImpl<$Res>
    extends _$GeneticItemCopyWithImpl<$Res, _$GeneticItemImpl>
    implements _$$GeneticItemImplCopyWith<$Res> {
  __$$GeneticItemImplCopyWithImpl(
    _$GeneticItemImpl _value,
    $Res Function(_$GeneticItemImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of GeneticItem
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? strainName = null,
    Object? breederName = null,
    Object? type = null,
    Object? packagingImageUrl = freezed,
  }) {
    return _then(
      _$GeneticItemImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as String,
        strainName: null == strainName
            ? _value.strainName
            : strainName // ignore: cast_nullable_to_non_nullable
                  as String,
        breederName: null == breederName
            ? _value.breederName
            : breederName // ignore: cast_nullable_to_non_nullable
                  as String,
        type: null == type
            ? _value.type
            : type // ignore: cast_nullable_to_non_nullable
                  as GeneticType,
        packagingImageUrl: freezed == packagingImageUrl
            ? _value.packagingImageUrl
            : packagingImageUrl // ignore: cast_nullable_to_non_nullable
                  as String?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$GeneticItemImpl implements _GeneticItem {
  const _$GeneticItemImpl({
    required this.id,
    required this.strainName,
    required this.breederName,
    required this.type,
    this.packagingImageUrl,
  });

  factory _$GeneticItemImpl.fromJson(Map<String, dynamic> json) =>
      _$$GeneticItemImplFromJson(json);

  @override
  final String id;
  @override
  final String strainName;
  @override
  final String breederName;
  @override
  final GeneticType type;
  @override
  final String? packagingImageUrl;

  @override
  String toString() {
    return 'GeneticItem(id: $id, strainName: $strainName, breederName: $breederName, type: $type, packagingImageUrl: $packagingImageUrl)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$GeneticItemImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.strainName, strainName) ||
                other.strainName == strainName) &&
            (identical(other.breederName, breederName) ||
                other.breederName == breederName) &&
            (identical(other.type, type) || other.type == type) &&
            (identical(other.packagingImageUrl, packagingImageUrl) ||
                other.packagingImageUrl == packagingImageUrl));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    strainName,
    breederName,
    type,
    packagingImageUrl,
  );

  /// Create a copy of GeneticItem
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$GeneticItemImplCopyWith<_$GeneticItemImpl> get copyWith =>
      __$$GeneticItemImplCopyWithImpl<_$GeneticItemImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$GeneticItemImplToJson(this);
  }
}

abstract class _GeneticItem implements GeneticItem {
  const factory _GeneticItem({
    required final String id,
    required final String strainName,
    required final String breederName,
    required final GeneticType type,
    final String? packagingImageUrl,
  }) = _$GeneticItemImpl;

  factory _GeneticItem.fromJson(Map<String, dynamic> json) =
      _$GeneticItemImpl.fromJson;

  @override
  String get id;
  @override
  String get strainName;
  @override
  String get breederName;
  @override
  GeneticType get type;
  @override
  String? get packagingImageUrl;

  /// Create a copy of GeneticItem
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$GeneticItemImplCopyWith<_$GeneticItemImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

PotPositionData _$PotPositionDataFromJson(Map<String, dynamic> json) {
  return _PotPositionData.fromJson(json);
}

/// @nodoc
mixin _$PotPositionData {
  String get id => throw _privateConstructorUsedError;
  String get potSizeLabel => throw _privateConstructorUsedError;
  String get potType => throw _privateConstructorUsedError;
  double get xPosition => throw _privateConstructorUsedError;
  double get yPosition => throw _privateConstructorUsedError;

  /// Serializes this PotPositionData to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of PotPositionData
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $PotPositionDataCopyWith<PotPositionData> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PotPositionDataCopyWith<$Res> {
  factory $PotPositionDataCopyWith(
    PotPositionData value,
    $Res Function(PotPositionData) then,
  ) = _$PotPositionDataCopyWithImpl<$Res, PotPositionData>;
  @useResult
  $Res call({
    String id,
    String potSizeLabel,
    String potType,
    double xPosition,
    double yPosition,
  });
}

/// @nodoc
class _$PotPositionDataCopyWithImpl<$Res, $Val extends PotPositionData>
    implements $PotPositionDataCopyWith<$Res> {
  _$PotPositionDataCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of PotPositionData
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? potSizeLabel = null,
    Object? potType = null,
    Object? xPosition = null,
    Object? yPosition = null,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as String,
            potSizeLabel: null == potSizeLabel
                ? _value.potSizeLabel
                : potSizeLabel // ignore: cast_nullable_to_non_nullable
                      as String,
            potType: null == potType
                ? _value.potType
                : potType // ignore: cast_nullable_to_non_nullable
                      as String,
            xPosition: null == xPosition
                ? _value.xPosition
                : xPosition // ignore: cast_nullable_to_non_nullable
                      as double,
            yPosition: null == yPosition
                ? _value.yPosition
                : yPosition // ignore: cast_nullable_to_non_nullable
                      as double,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$PotPositionDataImplCopyWith<$Res>
    implements $PotPositionDataCopyWith<$Res> {
  factory _$$PotPositionDataImplCopyWith(
    _$PotPositionDataImpl value,
    $Res Function(_$PotPositionDataImpl) then,
  ) = __$$PotPositionDataImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String id,
    String potSizeLabel,
    String potType,
    double xPosition,
    double yPosition,
  });
}

/// @nodoc
class __$$PotPositionDataImplCopyWithImpl<$Res>
    extends _$PotPositionDataCopyWithImpl<$Res, _$PotPositionDataImpl>
    implements _$$PotPositionDataImplCopyWith<$Res> {
  __$$PotPositionDataImplCopyWithImpl(
    _$PotPositionDataImpl _value,
    $Res Function(_$PotPositionDataImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of PotPositionData
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? potSizeLabel = null,
    Object? potType = null,
    Object? xPosition = null,
    Object? yPosition = null,
  }) {
    return _then(
      _$PotPositionDataImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as String,
        potSizeLabel: null == potSizeLabel
            ? _value.potSizeLabel
            : potSizeLabel // ignore: cast_nullable_to_non_nullable
                  as String,
        potType: null == potType
            ? _value.potType
            : potType // ignore: cast_nullable_to_non_nullable
                  as String,
        xPosition: null == xPosition
            ? _value.xPosition
            : xPosition // ignore: cast_nullable_to_non_nullable
                  as double,
        yPosition: null == yPosition
            ? _value.yPosition
            : yPosition // ignore: cast_nullable_to_non_nullable
                  as double,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$PotPositionDataImpl implements _PotPositionData {
  const _$PotPositionDataImpl({
    required this.id,
    required this.potSizeLabel,
    this.potType = 'fabric',
    required this.xPosition,
    required this.yPosition,
  });

  factory _$PotPositionDataImpl.fromJson(Map<String, dynamic> json) =>
      _$$PotPositionDataImplFromJson(json);

  @override
  final String id;
  @override
  final String potSizeLabel;
  @override
  @JsonKey()
  final String potType;
  @override
  final double xPosition;
  @override
  final double yPosition;

  @override
  String toString() {
    return 'PotPositionData(id: $id, potSizeLabel: $potSizeLabel, potType: $potType, xPosition: $xPosition, yPosition: $yPosition)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PotPositionDataImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.potSizeLabel, potSizeLabel) ||
                other.potSizeLabel == potSizeLabel) &&
            (identical(other.potType, potType) || other.potType == potType) &&
            (identical(other.xPosition, xPosition) ||
                other.xPosition == xPosition) &&
            (identical(other.yPosition, yPosition) ||
                other.yPosition == yPosition));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode =>
      Object.hash(runtimeType, id, potSizeLabel, potType, xPosition, yPosition);

  /// Create a copy of PotPositionData
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$PotPositionDataImplCopyWith<_$PotPositionDataImpl> get copyWith =>
      __$$PotPositionDataImplCopyWithImpl<_$PotPositionDataImpl>(
        this,
        _$identity,
      );

  @override
  Map<String, dynamic> toJson() {
    return _$$PotPositionDataImplToJson(this);
  }
}

abstract class _PotPositionData implements PotPositionData {
  const factory _PotPositionData({
    required final String id,
    required final String potSizeLabel,
    final String potType,
    required final double xPosition,
    required final double yPosition,
  }) = _$PotPositionDataImpl;

  factory _PotPositionData.fromJson(Map<String, dynamic> json) =
      _$PotPositionDataImpl.fromJson;

  @override
  String get id;
  @override
  String get potSizeLabel;
  @override
  String get potType;
  @override
  double get xPosition;
  @override
  double get yPosition;

  /// Create a copy of PotPositionData
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$PotPositionDataImplCopyWith<_$PotPositionDataImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

EnvironmentConfig _$EnvironmentConfigFromJson(Map<String, dynamic> json) {
  return _EnvironmentConfig.fromJson(json);
}

/// @nodoc
mixin _$EnvironmentConfig {
  String get name => throw _privateConstructorUsedError;
  EnvironmentType get environmentType => throw _privateConstructorUsedError;
  double? get tentWidthInches => throw _privateConstructorUsedError;
  double? get tentDepthInches => throw _privateConstructorUsedError;
  String? get tentSizeLabel => throw _privateConstructorUsedError;
  List<PotPositionData> get pots => throw _privateConstructorUsedError;

  /// Serializes this EnvironmentConfig to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of EnvironmentConfig
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $EnvironmentConfigCopyWith<EnvironmentConfig> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $EnvironmentConfigCopyWith<$Res> {
  factory $EnvironmentConfigCopyWith(
    EnvironmentConfig value,
    $Res Function(EnvironmentConfig) then,
  ) = _$EnvironmentConfigCopyWithImpl<$Res, EnvironmentConfig>;
  @useResult
  $Res call({
    String name,
    EnvironmentType environmentType,
    double? tentWidthInches,
    double? tentDepthInches,
    String? tentSizeLabel,
    List<PotPositionData> pots,
  });
}

/// @nodoc
class _$EnvironmentConfigCopyWithImpl<$Res, $Val extends EnvironmentConfig>
    implements $EnvironmentConfigCopyWith<$Res> {
  _$EnvironmentConfigCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of EnvironmentConfig
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? name = null,
    Object? environmentType = null,
    Object? tentWidthInches = freezed,
    Object? tentDepthInches = freezed,
    Object? tentSizeLabel = freezed,
    Object? pots = null,
  }) {
    return _then(
      _value.copyWith(
            name: null == name
                ? _value.name
                : name // ignore: cast_nullable_to_non_nullable
                      as String,
            environmentType: null == environmentType
                ? _value.environmentType
                : environmentType // ignore: cast_nullable_to_non_nullable
                      as EnvironmentType,
            tentWidthInches: freezed == tentWidthInches
                ? _value.tentWidthInches
                : tentWidthInches // ignore: cast_nullable_to_non_nullable
                      as double?,
            tentDepthInches: freezed == tentDepthInches
                ? _value.tentDepthInches
                : tentDepthInches // ignore: cast_nullable_to_non_nullable
                      as double?,
            tentSizeLabel: freezed == tentSizeLabel
                ? _value.tentSizeLabel
                : tentSizeLabel // ignore: cast_nullable_to_non_nullable
                      as String?,
            pots: null == pots
                ? _value.pots
                : pots // ignore: cast_nullable_to_non_nullable
                      as List<PotPositionData>,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$EnvironmentConfigImplCopyWith<$Res>
    implements $EnvironmentConfigCopyWith<$Res> {
  factory _$$EnvironmentConfigImplCopyWith(
    _$EnvironmentConfigImpl value,
    $Res Function(_$EnvironmentConfigImpl) then,
  ) = __$$EnvironmentConfigImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String name,
    EnvironmentType environmentType,
    double? tentWidthInches,
    double? tentDepthInches,
    String? tentSizeLabel,
    List<PotPositionData> pots,
  });
}

/// @nodoc
class __$$EnvironmentConfigImplCopyWithImpl<$Res>
    extends _$EnvironmentConfigCopyWithImpl<$Res, _$EnvironmentConfigImpl>
    implements _$$EnvironmentConfigImplCopyWith<$Res> {
  __$$EnvironmentConfigImplCopyWithImpl(
    _$EnvironmentConfigImpl _value,
    $Res Function(_$EnvironmentConfigImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of EnvironmentConfig
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? name = null,
    Object? environmentType = null,
    Object? tentWidthInches = freezed,
    Object? tentDepthInches = freezed,
    Object? tentSizeLabel = freezed,
    Object? pots = null,
  }) {
    return _then(
      _$EnvironmentConfigImpl(
        name: null == name
            ? _value.name
            : name // ignore: cast_nullable_to_non_nullable
                  as String,
        environmentType: null == environmentType
            ? _value.environmentType
            : environmentType // ignore: cast_nullable_to_non_nullable
                  as EnvironmentType,
        tentWidthInches: freezed == tentWidthInches
            ? _value.tentWidthInches
            : tentWidthInches // ignore: cast_nullable_to_non_nullable
                  as double?,
        tentDepthInches: freezed == tentDepthInches
            ? _value.tentDepthInches
            : tentDepthInches // ignore: cast_nullable_to_non_nullable
                  as double?,
        tentSizeLabel: freezed == tentSizeLabel
            ? _value.tentSizeLabel
            : tentSizeLabel // ignore: cast_nullable_to_non_nullable
                  as String?,
        pots: null == pots
            ? _value._pots
            : pots // ignore: cast_nullable_to_non_nullable
                  as List<PotPositionData>,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$EnvironmentConfigImpl implements _EnvironmentConfig {
  const _$EnvironmentConfigImpl({
    required this.name,
    required this.environmentType,
    this.tentWidthInches,
    this.tentDepthInches,
    this.tentSizeLabel,
    final List<PotPositionData> pots = const [],
  }) : _pots = pots;

  factory _$EnvironmentConfigImpl.fromJson(Map<String, dynamic> json) =>
      _$$EnvironmentConfigImplFromJson(json);

  @override
  final String name;
  @override
  final EnvironmentType environmentType;
  @override
  final double? tentWidthInches;
  @override
  final double? tentDepthInches;
  @override
  final String? tentSizeLabel;
  final List<PotPositionData> _pots;
  @override
  @JsonKey()
  List<PotPositionData> get pots {
    if (_pots is EqualUnmodifiableListView) return _pots;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_pots);
  }

  @override
  String toString() {
    return 'EnvironmentConfig(name: $name, environmentType: $environmentType, tentWidthInches: $tentWidthInches, tentDepthInches: $tentDepthInches, tentSizeLabel: $tentSizeLabel, pots: $pots)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$EnvironmentConfigImpl &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.environmentType, environmentType) ||
                other.environmentType == environmentType) &&
            (identical(other.tentWidthInches, tentWidthInches) ||
                other.tentWidthInches == tentWidthInches) &&
            (identical(other.tentDepthInches, tentDepthInches) ||
                other.tentDepthInches == tentDepthInches) &&
            (identical(other.tentSizeLabel, tentSizeLabel) ||
                other.tentSizeLabel == tentSizeLabel) &&
            const DeepCollectionEquality().equals(other._pots, _pots));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    name,
    environmentType,
    tentWidthInches,
    tentDepthInches,
    tentSizeLabel,
    const DeepCollectionEquality().hash(_pots),
  );

  /// Create a copy of EnvironmentConfig
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$EnvironmentConfigImplCopyWith<_$EnvironmentConfigImpl> get copyWith =>
      __$$EnvironmentConfigImplCopyWithImpl<_$EnvironmentConfigImpl>(
        this,
        _$identity,
      );

  @override
  Map<String, dynamic> toJson() {
    return _$$EnvironmentConfigImplToJson(this);
  }
}

abstract class _EnvironmentConfig implements EnvironmentConfig {
  const factory _EnvironmentConfig({
    required final String name,
    required final EnvironmentType environmentType,
    final double? tentWidthInches,
    final double? tentDepthInches,
    final String? tentSizeLabel,
    final List<PotPositionData> pots,
  }) = _$EnvironmentConfigImpl;

  factory _EnvironmentConfig.fromJson(Map<String, dynamic> json) =
      _$EnvironmentConfigImpl.fromJson;

  @override
  String get name;
  @override
  EnvironmentType get environmentType;
  @override
  double? get tentWidthInches;
  @override
  double? get tentDepthInches;
  @override
  String? get tentSizeLabel;
  @override
  List<PotPositionData> get pots;

  /// Create a copy of EnvironmentConfig
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$EnvironmentConfigImplCopyWith<_$EnvironmentConfigImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

HardwareIntegration _$HardwareIntegrationFromJson(Map<String, dynamic> json) {
  return _HardwareIntegration.fromJson(json);
}

/// @nodoc
mixin _$HardwareIntegration {
  HardwareManufacturer get manufacturer => throw _privateConstructorUsedError;
  bool get isLinked => throw _privateConstructorUsedError;
  String? get linkedAccountId => throw _privateConstructorUsedError;

  /// Serializes this HardwareIntegration to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of HardwareIntegration
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $HardwareIntegrationCopyWith<HardwareIntegration> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $HardwareIntegrationCopyWith<$Res> {
  factory $HardwareIntegrationCopyWith(
    HardwareIntegration value,
    $Res Function(HardwareIntegration) then,
  ) = _$HardwareIntegrationCopyWithImpl<$Res, HardwareIntegration>;
  @useResult
  $Res call({
    HardwareManufacturer manufacturer,
    bool isLinked,
    String? linkedAccountId,
  });
}

/// @nodoc
class _$HardwareIntegrationCopyWithImpl<$Res, $Val extends HardwareIntegration>
    implements $HardwareIntegrationCopyWith<$Res> {
  _$HardwareIntegrationCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of HardwareIntegration
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? manufacturer = null,
    Object? isLinked = null,
    Object? linkedAccountId = freezed,
  }) {
    return _then(
      _value.copyWith(
            manufacturer: null == manufacturer
                ? _value.manufacturer
                : manufacturer // ignore: cast_nullable_to_non_nullable
                      as HardwareManufacturer,
            isLinked: null == isLinked
                ? _value.isLinked
                : isLinked // ignore: cast_nullable_to_non_nullable
                      as bool,
            linkedAccountId: freezed == linkedAccountId
                ? _value.linkedAccountId
                : linkedAccountId // ignore: cast_nullable_to_non_nullable
                      as String?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$HardwareIntegrationImplCopyWith<$Res>
    implements $HardwareIntegrationCopyWith<$Res> {
  factory _$$HardwareIntegrationImplCopyWith(
    _$HardwareIntegrationImpl value,
    $Res Function(_$HardwareIntegrationImpl) then,
  ) = __$$HardwareIntegrationImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    HardwareManufacturer manufacturer,
    bool isLinked,
    String? linkedAccountId,
  });
}

/// @nodoc
class __$$HardwareIntegrationImplCopyWithImpl<$Res>
    extends _$HardwareIntegrationCopyWithImpl<$Res, _$HardwareIntegrationImpl>
    implements _$$HardwareIntegrationImplCopyWith<$Res> {
  __$$HardwareIntegrationImplCopyWithImpl(
    _$HardwareIntegrationImpl _value,
    $Res Function(_$HardwareIntegrationImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of HardwareIntegration
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? manufacturer = null,
    Object? isLinked = null,
    Object? linkedAccountId = freezed,
  }) {
    return _then(
      _$HardwareIntegrationImpl(
        manufacturer: null == manufacturer
            ? _value.manufacturer
            : manufacturer // ignore: cast_nullable_to_non_nullable
                  as HardwareManufacturer,
        isLinked: null == isLinked
            ? _value.isLinked
            : isLinked // ignore: cast_nullable_to_non_nullable
                  as bool,
        linkedAccountId: freezed == linkedAccountId
            ? _value.linkedAccountId
            : linkedAccountId // ignore: cast_nullable_to_non_nullable
                  as String?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$HardwareIntegrationImpl implements _HardwareIntegration {
  const _$HardwareIntegrationImpl({
    required this.manufacturer,
    this.isLinked = false,
    this.linkedAccountId,
  });

  factory _$HardwareIntegrationImpl.fromJson(Map<String, dynamic> json) =>
      _$$HardwareIntegrationImplFromJson(json);

  @override
  final HardwareManufacturer manufacturer;
  @override
  @JsonKey()
  final bool isLinked;
  @override
  final String? linkedAccountId;

  @override
  String toString() {
    return 'HardwareIntegration(manufacturer: $manufacturer, isLinked: $isLinked, linkedAccountId: $linkedAccountId)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$HardwareIntegrationImpl &&
            (identical(other.manufacturer, manufacturer) ||
                other.manufacturer == manufacturer) &&
            (identical(other.isLinked, isLinked) ||
                other.isLinked == isLinked) &&
            (identical(other.linkedAccountId, linkedAccountId) ||
                other.linkedAccountId == linkedAccountId));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode =>
      Object.hash(runtimeType, manufacturer, isLinked, linkedAccountId);

  /// Create a copy of HardwareIntegration
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$HardwareIntegrationImplCopyWith<_$HardwareIntegrationImpl> get copyWith =>
      __$$HardwareIntegrationImplCopyWithImpl<_$HardwareIntegrationImpl>(
        this,
        _$identity,
      );

  @override
  Map<String, dynamic> toJson() {
    return _$$HardwareIntegrationImplToJson(this);
  }
}

abstract class _HardwareIntegration implements HardwareIntegration {
  const factory _HardwareIntegration({
    required final HardwareManufacturer manufacturer,
    final bool isLinked,
    final String? linkedAccountId,
  }) = _$HardwareIntegrationImpl;

  factory _HardwareIntegration.fromJson(Map<String, dynamic> json) =
      _$HardwareIntegrationImpl.fromJson;

  @override
  HardwareManufacturer get manufacturer;
  @override
  bool get isLinked;
  @override
  String? get linkedAccountId;

  /// Create a copy of HardwareIntegration
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$HardwareIntegrationImplCopyWith<_$HardwareIntegrationImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

OnboardingState _$OnboardingStateFromJson(Map<String, dynamic> json) {
  return _OnboardingState.fromJson(json);
}

/// @nodoc
mixin _$OnboardingState {
  OnboardingStep get currentStep => throw _privateConstructorUsedError;
  List<GeneticItem> get genetics => throw _privateConstructorUsedError;
  EnvironmentConfig? get environmentConfig =>
      throw _privateConstructorUsedError;
  List<HardwareIntegration> get integrations =>
      throw _privateConstructorUsedError;
  bool get isCompleted => throw _privateConstructorUsedError;
  bool get isSubmitting => throw _privateConstructorUsedError;
  String? get error =>
      throw _privateConstructorUsedError; // Environment setup state
  EnvironmentType? get selectedEnvironmentType =>
      throw _privateConstructorUsedError;
  String? get selectedTentSize => throw _privateConstructorUsedError;
  String? get selectedPotSize => throw _privateConstructorUsedError;

  /// Serializes this OnboardingState to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of OnboardingState
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $OnboardingStateCopyWith<OnboardingState> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $OnboardingStateCopyWith<$Res> {
  factory $OnboardingStateCopyWith(
    OnboardingState value,
    $Res Function(OnboardingState) then,
  ) = _$OnboardingStateCopyWithImpl<$Res, OnboardingState>;
  @useResult
  $Res call({
    OnboardingStep currentStep,
    List<GeneticItem> genetics,
    EnvironmentConfig? environmentConfig,
    List<HardwareIntegration> integrations,
    bool isCompleted,
    bool isSubmitting,
    String? error,
    EnvironmentType? selectedEnvironmentType,
    String? selectedTentSize,
    String? selectedPotSize,
  });

  $EnvironmentConfigCopyWith<$Res>? get environmentConfig;
}

/// @nodoc
class _$OnboardingStateCopyWithImpl<$Res, $Val extends OnboardingState>
    implements $OnboardingStateCopyWith<$Res> {
  _$OnboardingStateCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of OnboardingState
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? currentStep = null,
    Object? genetics = null,
    Object? environmentConfig = freezed,
    Object? integrations = null,
    Object? isCompleted = null,
    Object? isSubmitting = null,
    Object? error = freezed,
    Object? selectedEnvironmentType = freezed,
    Object? selectedTentSize = freezed,
    Object? selectedPotSize = freezed,
  }) {
    return _then(
      _value.copyWith(
            currentStep: null == currentStep
                ? _value.currentStep
                : currentStep // ignore: cast_nullable_to_non_nullable
                      as OnboardingStep,
            genetics: null == genetics
                ? _value.genetics
                : genetics // ignore: cast_nullable_to_non_nullable
                      as List<GeneticItem>,
            environmentConfig: freezed == environmentConfig
                ? _value.environmentConfig
                : environmentConfig // ignore: cast_nullable_to_non_nullable
                      as EnvironmentConfig?,
            integrations: null == integrations
                ? _value.integrations
                : integrations // ignore: cast_nullable_to_non_nullable
                      as List<HardwareIntegration>,
            isCompleted: null == isCompleted
                ? _value.isCompleted
                : isCompleted // ignore: cast_nullable_to_non_nullable
                      as bool,
            isSubmitting: null == isSubmitting
                ? _value.isSubmitting
                : isSubmitting // ignore: cast_nullable_to_non_nullable
                      as bool,
            error: freezed == error
                ? _value.error
                : error // ignore: cast_nullable_to_non_nullable
                      as String?,
            selectedEnvironmentType: freezed == selectedEnvironmentType
                ? _value.selectedEnvironmentType
                : selectedEnvironmentType // ignore: cast_nullable_to_non_nullable
                      as EnvironmentType?,
            selectedTentSize: freezed == selectedTentSize
                ? _value.selectedTentSize
                : selectedTentSize // ignore: cast_nullable_to_non_nullable
                      as String?,
            selectedPotSize: freezed == selectedPotSize
                ? _value.selectedPotSize
                : selectedPotSize // ignore: cast_nullable_to_non_nullable
                      as String?,
          )
          as $Val,
    );
  }

  /// Create a copy of OnboardingState
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $EnvironmentConfigCopyWith<$Res>? get environmentConfig {
    if (_value.environmentConfig == null) {
      return null;
    }

    return $EnvironmentConfigCopyWith<$Res>(_value.environmentConfig!, (value) {
      return _then(_value.copyWith(environmentConfig: value) as $Val);
    });
  }
}

/// @nodoc
abstract class _$$OnboardingStateImplCopyWith<$Res>
    implements $OnboardingStateCopyWith<$Res> {
  factory _$$OnboardingStateImplCopyWith(
    _$OnboardingStateImpl value,
    $Res Function(_$OnboardingStateImpl) then,
  ) = __$$OnboardingStateImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    OnboardingStep currentStep,
    List<GeneticItem> genetics,
    EnvironmentConfig? environmentConfig,
    List<HardwareIntegration> integrations,
    bool isCompleted,
    bool isSubmitting,
    String? error,
    EnvironmentType? selectedEnvironmentType,
    String? selectedTentSize,
    String? selectedPotSize,
  });

  @override
  $EnvironmentConfigCopyWith<$Res>? get environmentConfig;
}

/// @nodoc
class __$$OnboardingStateImplCopyWithImpl<$Res>
    extends _$OnboardingStateCopyWithImpl<$Res, _$OnboardingStateImpl>
    implements _$$OnboardingStateImplCopyWith<$Res> {
  __$$OnboardingStateImplCopyWithImpl(
    _$OnboardingStateImpl _value,
    $Res Function(_$OnboardingStateImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of OnboardingState
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? currentStep = null,
    Object? genetics = null,
    Object? environmentConfig = freezed,
    Object? integrations = null,
    Object? isCompleted = null,
    Object? isSubmitting = null,
    Object? error = freezed,
    Object? selectedEnvironmentType = freezed,
    Object? selectedTentSize = freezed,
    Object? selectedPotSize = freezed,
  }) {
    return _then(
      _$OnboardingStateImpl(
        currentStep: null == currentStep
            ? _value.currentStep
            : currentStep // ignore: cast_nullable_to_non_nullable
                  as OnboardingStep,
        genetics: null == genetics
            ? _value._genetics
            : genetics // ignore: cast_nullable_to_non_nullable
                  as List<GeneticItem>,
        environmentConfig: freezed == environmentConfig
            ? _value.environmentConfig
            : environmentConfig // ignore: cast_nullable_to_non_nullable
                  as EnvironmentConfig?,
        integrations: null == integrations
            ? _value._integrations
            : integrations // ignore: cast_nullable_to_non_nullable
                  as List<HardwareIntegration>,
        isCompleted: null == isCompleted
            ? _value.isCompleted
            : isCompleted // ignore: cast_nullable_to_non_nullable
                  as bool,
        isSubmitting: null == isSubmitting
            ? _value.isSubmitting
            : isSubmitting // ignore: cast_nullable_to_non_nullable
                  as bool,
        error: freezed == error
            ? _value.error
            : error // ignore: cast_nullable_to_non_nullable
                  as String?,
        selectedEnvironmentType: freezed == selectedEnvironmentType
            ? _value.selectedEnvironmentType
            : selectedEnvironmentType // ignore: cast_nullable_to_non_nullable
                  as EnvironmentType?,
        selectedTentSize: freezed == selectedTentSize
            ? _value.selectedTentSize
            : selectedTentSize // ignore: cast_nullable_to_non_nullable
                  as String?,
        selectedPotSize: freezed == selectedPotSize
            ? _value.selectedPotSize
            : selectedPotSize // ignore: cast_nullable_to_non_nullable
                  as String?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$OnboardingStateImpl implements _OnboardingState {
  const _$OnboardingStateImpl({
    this.currentStep = OnboardingStep.welcome,
    final List<GeneticItem> genetics = const [],
    this.environmentConfig,
    final List<HardwareIntegration> integrations = const [],
    this.isCompleted = false,
    this.isSubmitting = false,
    this.error,
    this.selectedEnvironmentType,
    this.selectedTentSize,
    this.selectedPotSize,
  }) : _genetics = genetics,
       _integrations = integrations;

  factory _$OnboardingStateImpl.fromJson(Map<String, dynamic> json) =>
      _$$OnboardingStateImplFromJson(json);

  @override
  @JsonKey()
  final OnboardingStep currentStep;
  final List<GeneticItem> _genetics;
  @override
  @JsonKey()
  List<GeneticItem> get genetics {
    if (_genetics is EqualUnmodifiableListView) return _genetics;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_genetics);
  }

  @override
  final EnvironmentConfig? environmentConfig;
  final List<HardwareIntegration> _integrations;
  @override
  @JsonKey()
  List<HardwareIntegration> get integrations {
    if (_integrations is EqualUnmodifiableListView) return _integrations;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_integrations);
  }

  @override
  @JsonKey()
  final bool isCompleted;
  @override
  @JsonKey()
  final bool isSubmitting;
  @override
  final String? error;
  // Environment setup state
  @override
  final EnvironmentType? selectedEnvironmentType;
  @override
  final String? selectedTentSize;
  @override
  final String? selectedPotSize;

  @override
  String toString() {
    return 'OnboardingState(currentStep: $currentStep, genetics: $genetics, environmentConfig: $environmentConfig, integrations: $integrations, isCompleted: $isCompleted, isSubmitting: $isSubmitting, error: $error, selectedEnvironmentType: $selectedEnvironmentType, selectedTentSize: $selectedTentSize, selectedPotSize: $selectedPotSize)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$OnboardingStateImpl &&
            (identical(other.currentStep, currentStep) ||
                other.currentStep == currentStep) &&
            const DeepCollectionEquality().equals(other._genetics, _genetics) &&
            (identical(other.environmentConfig, environmentConfig) ||
                other.environmentConfig == environmentConfig) &&
            const DeepCollectionEquality().equals(
              other._integrations,
              _integrations,
            ) &&
            (identical(other.isCompleted, isCompleted) ||
                other.isCompleted == isCompleted) &&
            (identical(other.isSubmitting, isSubmitting) ||
                other.isSubmitting == isSubmitting) &&
            (identical(other.error, error) || other.error == error) &&
            (identical(
                  other.selectedEnvironmentType,
                  selectedEnvironmentType,
                ) ||
                other.selectedEnvironmentType == selectedEnvironmentType) &&
            (identical(other.selectedTentSize, selectedTentSize) ||
                other.selectedTentSize == selectedTentSize) &&
            (identical(other.selectedPotSize, selectedPotSize) ||
                other.selectedPotSize == selectedPotSize));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    currentStep,
    const DeepCollectionEquality().hash(_genetics),
    environmentConfig,
    const DeepCollectionEquality().hash(_integrations),
    isCompleted,
    isSubmitting,
    error,
    selectedEnvironmentType,
    selectedTentSize,
    selectedPotSize,
  );

  /// Create a copy of OnboardingState
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$OnboardingStateImplCopyWith<_$OnboardingStateImpl> get copyWith =>
      __$$OnboardingStateImplCopyWithImpl<_$OnboardingStateImpl>(
        this,
        _$identity,
      );

  @override
  Map<String, dynamic> toJson() {
    return _$$OnboardingStateImplToJson(this);
  }
}

abstract class _OnboardingState implements OnboardingState {
  const factory _OnboardingState({
    final OnboardingStep currentStep,
    final List<GeneticItem> genetics,
    final EnvironmentConfig? environmentConfig,
    final List<HardwareIntegration> integrations,
    final bool isCompleted,
    final bool isSubmitting,
    final String? error,
    final EnvironmentType? selectedEnvironmentType,
    final String? selectedTentSize,
    final String? selectedPotSize,
  }) = _$OnboardingStateImpl;

  factory _OnboardingState.fromJson(Map<String, dynamic> json) =
      _$OnboardingStateImpl.fromJson;

  @override
  OnboardingStep get currentStep;
  @override
  List<GeneticItem> get genetics;
  @override
  EnvironmentConfig? get environmentConfig;
  @override
  List<HardwareIntegration> get integrations;
  @override
  bool get isCompleted;
  @override
  bool get isSubmitting;
  @override
  String? get error; // Environment setup state
  @override
  EnvironmentType? get selectedEnvironmentType;
  @override
  String? get selectedTentSize;
  @override
  String? get selectedPotSize;

  /// Create a copy of OnboardingState
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$OnboardingStateImplCopyWith<_$OnboardingStateImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
