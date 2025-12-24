// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'dashboard_stats_model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

/// @nodoc
mixin _$CountStats {
  @JsonKey(name: 'total')
  int get total => throw _privateConstructorUsedError;
  int get active => throw _privateConstructorUsedError;
  int get harvested => throw _privateConstructorUsedError;
  int get seedlings => throw _privateConstructorUsedError;
  int get vegetative => throw _privateConstructorUsedError;
  int get flowering => throw _privateConstructorUsedError;

  /// Create a copy of CountStats
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $CountStatsCopyWith<CountStats> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $CountStatsCopyWith<$Res> {
  factory $CountStatsCopyWith(
    CountStats value,
    $Res Function(CountStats) then,
  ) = _$CountStatsCopyWithImpl<$Res, CountStats>;
  @useResult
  $Res call({
    @JsonKey(name: 'total') int total,
    int active,
    int harvested,
    int seedlings,
    int vegetative,
    int flowering,
  });
}

/// @nodoc
class _$CountStatsCopyWithImpl<$Res, $Val extends CountStats>
    implements $CountStatsCopyWith<$Res> {
  _$CountStatsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of CountStats
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? total = null,
    Object? active = null,
    Object? harvested = null,
    Object? seedlings = null,
    Object? vegetative = null,
    Object? flowering = null,
  }) {
    return _then(
      _value.copyWith(
            total: null == total
                ? _value.total
                : total // ignore: cast_nullable_to_non_nullable
                      as int,
            active: null == active
                ? _value.active
                : active // ignore: cast_nullable_to_non_nullable
                      as int,
            harvested: null == harvested
                ? _value.harvested
                : harvested // ignore: cast_nullable_to_non_nullable
                      as int,
            seedlings: null == seedlings
                ? _value.seedlings
                : seedlings // ignore: cast_nullable_to_non_nullable
                      as int,
            vegetative: null == vegetative
                ? _value.vegetative
                : vegetative // ignore: cast_nullable_to_non_nullable
                      as int,
            flowering: null == flowering
                ? _value.flowering
                : flowering // ignore: cast_nullable_to_non_nullable
                      as int,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$CountStatsImplCopyWith<$Res>
    implements $CountStatsCopyWith<$Res> {
  factory _$$CountStatsImplCopyWith(
    _$CountStatsImpl value,
    $Res Function(_$CountStatsImpl) then,
  ) = __$$CountStatsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    @JsonKey(name: 'total') int total,
    int active,
    int harvested,
    int seedlings,
    int vegetative,
    int flowering,
  });
}

/// @nodoc
class __$$CountStatsImplCopyWithImpl<$Res>
    extends _$CountStatsCopyWithImpl<$Res, _$CountStatsImpl>
    implements _$$CountStatsImplCopyWith<$Res> {
  __$$CountStatsImplCopyWithImpl(
    _$CountStatsImpl _value,
    $Res Function(_$CountStatsImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of CountStats
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? total = null,
    Object? active = null,
    Object? harvested = null,
    Object? seedlings = null,
    Object? vegetative = null,
    Object? flowering = null,
  }) {
    return _then(
      _$CountStatsImpl(
        total: null == total
            ? _value.total
            : total // ignore: cast_nullable_to_non_nullable
                  as int,
        active: null == active
            ? _value.active
            : active // ignore: cast_nullable_to_non_nullable
                  as int,
        harvested: null == harvested
            ? _value.harvested
            : harvested // ignore: cast_nullable_to_non_nullable
                  as int,
        seedlings: null == seedlings
            ? _value.seedlings
            : seedlings // ignore: cast_nullable_to_non_nullable
                  as int,
        vegetative: null == vegetative
            ? _value.vegetative
            : vegetative // ignore: cast_nullable_to_non_nullable
                  as int,
        flowering: null == flowering
            ? _value.flowering
            : flowering // ignore: cast_nullable_to_non_nullable
                  as int,
      ),
    );
  }
}

/// @nodoc

class _$CountStatsImpl implements _CountStats {
  const _$CountStatsImpl({
    @JsonKey(name: 'total') required this.total,
    required this.active,
    required this.harvested,
    required this.seedlings,
    required this.vegetative,
    required this.flowering,
  });

  @override
  @JsonKey(name: 'total')
  final int total;
  @override
  final int active;
  @override
  final int harvested;
  @override
  final int seedlings;
  @override
  final int vegetative;
  @override
  final int flowering;

  @override
  String toString() {
    return 'CountStats(total: $total, active: $active, harvested: $harvested, seedlings: $seedlings, vegetative: $vegetative, flowering: $flowering)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$CountStatsImpl &&
            (identical(other.total, total) || other.total == total) &&
            (identical(other.active, active) || other.active == active) &&
            (identical(other.harvested, harvested) ||
                other.harvested == harvested) &&
            (identical(other.seedlings, seedlings) ||
                other.seedlings == seedlings) &&
            (identical(other.vegetative, vegetative) ||
                other.vegetative == vegetative) &&
            (identical(other.flowering, flowering) ||
                other.flowering == flowering));
  }

  @override
  int get hashCode => Object.hash(
    runtimeType,
    total,
    active,
    harvested,
    seedlings,
    vegetative,
    flowering,
  );

  /// Create a copy of CountStats
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$CountStatsImplCopyWith<_$CountStatsImpl> get copyWith =>
      __$$CountStatsImplCopyWithImpl<_$CountStatsImpl>(this, _$identity);
}

abstract class _CountStats implements CountStats {
  const factory _CountStats({
    @JsonKey(name: 'total') required final int total,
    required final int active,
    required final int harvested,
    required final int seedlings,
    required final int vegetative,
    required final int flowering,
  }) = _$CountStatsImpl;

  @override
  @JsonKey(name: 'total')
  int get total;
  @override
  int get active;
  @override
  int get harvested;
  @override
  int get seedlings;
  @override
  int get vegetative;
  @override
  int get flowering;

  /// Create a copy of CountStats
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$CountStatsImplCopyWith<_$CountStatsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
mixin _$CultivarStats {
  @JsonKey(name: 'total_cultivars')
  int get totalCultivars => throw _privateConstructorUsedError;
  @JsonKey(name: 'user_cultivars')
  int get userCultivars => throw _privateConstructorUsedError;

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
    @JsonKey(name: 'total_cultivars') int totalCultivars,
    @JsonKey(name: 'user_cultivars') int userCultivars,
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
  $Res call({Object? totalCultivars = null, Object? userCultivars = null}) {
    return _then(
      _value.copyWith(
            totalCultivars: null == totalCultivars
                ? _value.totalCultivars
                : totalCultivars // ignore: cast_nullable_to_non_nullable
                      as int,
            userCultivars: null == userCultivars
                ? _value.userCultivars
                : userCultivars // ignore: cast_nullable_to_non_nullable
                      as int,
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
    @JsonKey(name: 'total_cultivars') int totalCultivars,
    @JsonKey(name: 'user_cultivars') int userCultivars,
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
  $Res call({Object? totalCultivars = null, Object? userCultivars = null}) {
    return _then(
      _$CultivarStatsImpl(
        totalCultivars: null == totalCultivars
            ? _value.totalCultivars
            : totalCultivars // ignore: cast_nullable_to_non_nullable
                  as int,
        userCultivars: null == userCultivars
            ? _value.userCultivars
            : userCultivars // ignore: cast_nullable_to_non_nullable
                  as int,
      ),
    );
  }
}

/// @nodoc

class _$CultivarStatsImpl implements _CultivarStats {
  const _$CultivarStatsImpl({
    @JsonKey(name: 'total_cultivars') required this.totalCultivars,
    @JsonKey(name: 'user_cultivars') required this.userCultivars,
  });

  @override
  @JsonKey(name: 'total_cultivars')
  final int totalCultivars;
  @override
  @JsonKey(name: 'user_cultivars')
  final int userCultivars;

  @override
  String toString() {
    return 'CultivarStats(totalCultivars: $totalCultivars, userCultivars: $userCultivars)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$CultivarStatsImpl &&
            (identical(other.totalCultivars, totalCultivars) ||
                other.totalCultivars == totalCultivars) &&
            (identical(other.userCultivars, userCultivars) ||
                other.userCultivars == userCultivars));
  }

  @override
  int get hashCode => Object.hash(runtimeType, totalCultivars, userCultivars);

  /// Create a copy of CultivarStats
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$CultivarStatsImplCopyWith<_$CultivarStatsImpl> get copyWith =>
      __$$CultivarStatsImplCopyWithImpl<_$CultivarStatsImpl>(this, _$identity);
}

abstract class _CultivarStats implements CultivarStats {
  const factory _CultivarStats({
    @JsonKey(name: 'total_cultivars') required final int totalCultivars,
    @JsonKey(name: 'user_cultivars') required final int userCultivars,
  }) = _$CultivarStatsImpl;

  @override
  @JsonKey(name: 'total_cultivars')
  int get totalCultivars;
  @override
  @JsonKey(name: 'user_cultivars')
  int get userCultivars;

  /// Create a copy of CultivarStats
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$CultivarStatsImplCopyWith<_$CultivarStatsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
mixin _$EnvironmentalStats {
  @JsonKey(name: 'avg_temperature')
  double get avgTemperature => throw _privateConstructorUsedError;
  @JsonKey(name: 'avg_humidity')
  double get avgHumidity => throw _privateConstructorUsedError;
  @JsonKey(name: 'avg_ph')
  double? get avgPh => throw _privateConstructorUsedError;
  @JsonKey(name: 'avg_ec')
  double? get avgEc => throw _privateConstructorUsedError;

  /// Create a copy of EnvironmentalStats
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $EnvironmentalStatsCopyWith<EnvironmentalStats> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $EnvironmentalStatsCopyWith<$Res> {
  factory $EnvironmentalStatsCopyWith(
    EnvironmentalStats value,
    $Res Function(EnvironmentalStats) then,
  ) = _$EnvironmentalStatsCopyWithImpl<$Res, EnvironmentalStats>;
  @useResult
  $Res call({
    @JsonKey(name: 'avg_temperature') double avgTemperature,
    @JsonKey(name: 'avg_humidity') double avgHumidity,
    @JsonKey(name: 'avg_ph') double? avgPh,
    @JsonKey(name: 'avg_ec') double? avgEc,
  });
}

/// @nodoc
class _$EnvironmentalStatsCopyWithImpl<$Res, $Val extends EnvironmentalStats>
    implements $EnvironmentalStatsCopyWith<$Res> {
  _$EnvironmentalStatsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of EnvironmentalStats
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? avgTemperature = null,
    Object? avgHumidity = null,
    Object? avgPh = freezed,
    Object? avgEc = freezed,
  }) {
    return _then(
      _value.copyWith(
            avgTemperature: null == avgTemperature
                ? _value.avgTemperature
                : avgTemperature // ignore: cast_nullable_to_non_nullable
                      as double,
            avgHumidity: null == avgHumidity
                ? _value.avgHumidity
                : avgHumidity // ignore: cast_nullable_to_non_nullable
                      as double,
            avgPh: freezed == avgPh
                ? _value.avgPh
                : avgPh // ignore: cast_nullable_to_non_nullable
                      as double?,
            avgEc: freezed == avgEc
                ? _value.avgEc
                : avgEc // ignore: cast_nullable_to_non_nullable
                      as double?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$EnvironmentalStatsImplCopyWith<$Res>
    implements $EnvironmentalStatsCopyWith<$Res> {
  factory _$$EnvironmentalStatsImplCopyWith(
    _$EnvironmentalStatsImpl value,
    $Res Function(_$EnvironmentalStatsImpl) then,
  ) = __$$EnvironmentalStatsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    @JsonKey(name: 'avg_temperature') double avgTemperature,
    @JsonKey(name: 'avg_humidity') double avgHumidity,
    @JsonKey(name: 'avg_ph') double? avgPh,
    @JsonKey(name: 'avg_ec') double? avgEc,
  });
}

/// @nodoc
class __$$EnvironmentalStatsImplCopyWithImpl<$Res>
    extends _$EnvironmentalStatsCopyWithImpl<$Res, _$EnvironmentalStatsImpl>
    implements _$$EnvironmentalStatsImplCopyWith<$Res> {
  __$$EnvironmentalStatsImplCopyWithImpl(
    _$EnvironmentalStatsImpl _value,
    $Res Function(_$EnvironmentalStatsImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of EnvironmentalStats
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? avgTemperature = null,
    Object? avgHumidity = null,
    Object? avgPh = freezed,
    Object? avgEc = freezed,
  }) {
    return _then(
      _$EnvironmentalStatsImpl(
        avgTemperature: null == avgTemperature
            ? _value.avgTemperature
            : avgTemperature // ignore: cast_nullable_to_non_nullable
                  as double,
        avgHumidity: null == avgHumidity
            ? _value.avgHumidity
            : avgHumidity // ignore: cast_nullable_to_non_nullable
                  as double,
        avgPh: freezed == avgPh
            ? _value.avgPh
            : avgPh // ignore: cast_nullable_to_non_nullable
                  as double?,
        avgEc: freezed == avgEc
            ? _value.avgEc
            : avgEc // ignore: cast_nullable_to_non_nullable
                  as double?,
      ),
    );
  }
}

/// @nodoc

class _$EnvironmentalStatsImpl implements _EnvironmentalStats {
  const _$EnvironmentalStatsImpl({
    @JsonKey(name: 'avg_temperature') required this.avgTemperature,
    @JsonKey(name: 'avg_humidity') required this.avgHumidity,
    @JsonKey(name: 'avg_ph') this.avgPh,
    @JsonKey(name: 'avg_ec') this.avgEc,
  });

  @override
  @JsonKey(name: 'avg_temperature')
  final double avgTemperature;
  @override
  @JsonKey(name: 'avg_humidity')
  final double avgHumidity;
  @override
  @JsonKey(name: 'avg_ph')
  final double? avgPh;
  @override
  @JsonKey(name: 'avg_ec')
  final double? avgEc;

  @override
  String toString() {
    return 'EnvironmentalStats(avgTemperature: $avgTemperature, avgHumidity: $avgHumidity, avgPh: $avgPh, avgEc: $avgEc)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$EnvironmentalStatsImpl &&
            (identical(other.avgTemperature, avgTemperature) ||
                other.avgTemperature == avgTemperature) &&
            (identical(other.avgHumidity, avgHumidity) ||
                other.avgHumidity == avgHumidity) &&
            (identical(other.avgPh, avgPh) || other.avgPh == avgPh) &&
            (identical(other.avgEc, avgEc) || other.avgEc == avgEc));
  }

  @override
  int get hashCode =>
      Object.hash(runtimeType, avgTemperature, avgHumidity, avgPh, avgEc);

  /// Create a copy of EnvironmentalStats
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$EnvironmentalStatsImplCopyWith<_$EnvironmentalStatsImpl> get copyWith =>
      __$$EnvironmentalStatsImplCopyWithImpl<_$EnvironmentalStatsImpl>(
        this,
        _$identity,
      );
}

abstract class _EnvironmentalStats implements EnvironmentalStats {
  const factory _EnvironmentalStats({
    @JsonKey(name: 'avg_temperature') required final double avgTemperature,
    @JsonKey(name: 'avg_humidity') required final double avgHumidity,
    @JsonKey(name: 'avg_ph') final double? avgPh,
    @JsonKey(name: 'avg_ec') final double? avgEc,
  }) = _$EnvironmentalStatsImpl;

  @override
  @JsonKey(name: 'avg_temperature')
  double get avgTemperature;
  @override
  @JsonKey(name: 'avg_humidity')
  double get avgHumidity;
  @override
  @JsonKey(name: 'avg_ph')
  double? get avgPh;
  @override
  @JsonKey(name: 'avg_ec')
  double? get avgEc;

  /// Create a copy of EnvironmentalStats
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$EnvironmentalStatsImplCopyWith<_$EnvironmentalStatsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
mixin _$SensorStats {
  @JsonKey(name: 'total_sensors')
  int get totalSensors => throw _privateConstructorUsedError;
  @JsonKey(name: 'active_sensors')
  int get activeSensors => throw _privateConstructorUsedError;
  @JsonKey(name: 'last_reading_time')
  DateTime? get lastReadingTime => throw _privateConstructorUsedError;

  /// Create a copy of SensorStats
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $SensorStatsCopyWith<SensorStats> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $SensorStatsCopyWith<$Res> {
  factory $SensorStatsCopyWith(
    SensorStats value,
    $Res Function(SensorStats) then,
  ) = _$SensorStatsCopyWithImpl<$Res, SensorStats>;
  @useResult
  $Res call({
    @JsonKey(name: 'total_sensors') int totalSensors,
    @JsonKey(name: 'active_sensors') int activeSensors,
    @JsonKey(name: 'last_reading_time') DateTime? lastReadingTime,
  });
}

/// @nodoc
class _$SensorStatsCopyWithImpl<$Res, $Val extends SensorStats>
    implements $SensorStatsCopyWith<$Res> {
  _$SensorStatsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of SensorStats
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? totalSensors = null,
    Object? activeSensors = null,
    Object? lastReadingTime = freezed,
  }) {
    return _then(
      _value.copyWith(
            totalSensors: null == totalSensors
                ? _value.totalSensors
                : totalSensors // ignore: cast_nullable_to_non_nullable
                      as int,
            activeSensors: null == activeSensors
                ? _value.activeSensors
                : activeSensors // ignore: cast_nullable_to_non_nullable
                      as int,
            lastReadingTime: freezed == lastReadingTime
                ? _value.lastReadingTime
                : lastReadingTime // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$SensorStatsImplCopyWith<$Res>
    implements $SensorStatsCopyWith<$Res> {
  factory _$$SensorStatsImplCopyWith(
    _$SensorStatsImpl value,
    $Res Function(_$SensorStatsImpl) then,
  ) = __$$SensorStatsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    @JsonKey(name: 'total_sensors') int totalSensors,
    @JsonKey(name: 'active_sensors') int activeSensors,
    @JsonKey(name: 'last_reading_time') DateTime? lastReadingTime,
  });
}

/// @nodoc
class __$$SensorStatsImplCopyWithImpl<$Res>
    extends _$SensorStatsCopyWithImpl<$Res, _$SensorStatsImpl>
    implements _$$SensorStatsImplCopyWith<$Res> {
  __$$SensorStatsImplCopyWithImpl(
    _$SensorStatsImpl _value,
    $Res Function(_$SensorStatsImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of SensorStats
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? totalSensors = null,
    Object? activeSensors = null,
    Object? lastReadingTime = freezed,
  }) {
    return _then(
      _$SensorStatsImpl(
        totalSensors: null == totalSensors
            ? _value.totalSensors
            : totalSensors // ignore: cast_nullable_to_non_nullable
                  as int,
        activeSensors: null == activeSensors
            ? _value.activeSensors
            : activeSensors // ignore: cast_nullable_to_non_nullable
                  as int,
        lastReadingTime: freezed == lastReadingTime
            ? _value.lastReadingTime
            : lastReadingTime // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
      ),
    );
  }
}

/// @nodoc

class _$SensorStatsImpl implements _SensorStats {
  const _$SensorStatsImpl({
    @JsonKey(name: 'total_sensors') required this.totalSensors,
    @JsonKey(name: 'active_sensors') required this.activeSensors,
    @JsonKey(name: 'last_reading_time') this.lastReadingTime,
  });

  @override
  @JsonKey(name: 'total_sensors')
  final int totalSensors;
  @override
  @JsonKey(name: 'active_sensors')
  final int activeSensors;
  @override
  @JsonKey(name: 'last_reading_time')
  final DateTime? lastReadingTime;

  @override
  String toString() {
    return 'SensorStats(totalSensors: $totalSensors, activeSensors: $activeSensors, lastReadingTime: $lastReadingTime)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$SensorStatsImpl &&
            (identical(other.totalSensors, totalSensors) ||
                other.totalSensors == totalSensors) &&
            (identical(other.activeSensors, activeSensors) ||
                other.activeSensors == activeSensors) &&
            (identical(other.lastReadingTime, lastReadingTime) ||
                other.lastReadingTime == lastReadingTime));
  }

  @override
  int get hashCode =>
      Object.hash(runtimeType, totalSensors, activeSensors, lastReadingTime);

  /// Create a copy of SensorStats
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$SensorStatsImplCopyWith<_$SensorStatsImpl> get copyWith =>
      __$$SensorStatsImplCopyWithImpl<_$SensorStatsImpl>(this, _$identity);
}

abstract class _SensorStats implements SensorStats {
  const factory _SensorStats({
    @JsonKey(name: 'total_sensors') required final int totalSensors,
    @JsonKey(name: 'active_sensors') required final int activeSensors,
    @JsonKey(name: 'last_reading_time') final DateTime? lastReadingTime,
  }) = _$SensorStatsImpl;

  @override
  @JsonKey(name: 'total_sensors')
  int get totalSensors;
  @override
  @JsonKey(name: 'active_sensors')
  int get activeSensors;
  @override
  @JsonKey(name: 'last_reading_time')
  DateTime? get lastReadingTime;

  /// Create a copy of SensorStats
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$SensorStatsImplCopyWith<_$SensorStatsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
mixin _$DataSlice {
  DateTime get timestamp => throw _privateConstructorUsedError;
  double get value => throw _privateConstructorUsedError;
  String? get label => throw _privateConstructorUsedError;

  /// Create a copy of DataSlice
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $DataSliceCopyWith<DataSlice> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $DataSliceCopyWith<$Res> {
  factory $DataSliceCopyWith(DataSlice value, $Res Function(DataSlice) then) =
      _$DataSliceCopyWithImpl<$Res, DataSlice>;
  @useResult
  $Res call({DateTime timestamp, double value, String? label});
}

/// @nodoc
class _$DataSliceCopyWithImpl<$Res, $Val extends DataSlice>
    implements $DataSliceCopyWith<$Res> {
  _$DataSliceCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of DataSlice
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? timestamp = null,
    Object? value = null,
    Object? label = freezed,
  }) {
    return _then(
      _value.copyWith(
            timestamp: null == timestamp
                ? _value.timestamp
                : timestamp // ignore: cast_nullable_to_non_nullable
                      as DateTime,
            value: null == value
                ? _value.value
                : value // ignore: cast_nullable_to_non_nullable
                      as double,
            label: freezed == label
                ? _value.label
                : label // ignore: cast_nullable_to_non_nullable
                      as String?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$DataSliceImplCopyWith<$Res>
    implements $DataSliceCopyWith<$Res> {
  factory _$$DataSliceImplCopyWith(
    _$DataSliceImpl value,
    $Res Function(_$DataSliceImpl) then,
  ) = __$$DataSliceImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({DateTime timestamp, double value, String? label});
}

/// @nodoc
class __$$DataSliceImplCopyWithImpl<$Res>
    extends _$DataSliceCopyWithImpl<$Res, _$DataSliceImpl>
    implements _$$DataSliceImplCopyWith<$Res> {
  __$$DataSliceImplCopyWithImpl(
    _$DataSliceImpl _value,
    $Res Function(_$DataSliceImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of DataSlice
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? timestamp = null,
    Object? value = null,
    Object? label = freezed,
  }) {
    return _then(
      _$DataSliceImpl(
        timestamp: null == timestamp
            ? _value.timestamp
            : timestamp // ignore: cast_nullable_to_non_nullable
                  as DateTime,
        value: null == value
            ? _value.value
            : value // ignore: cast_nullable_to_non_nullable
                  as double,
        label: freezed == label
            ? _value.label
            : label // ignore: cast_nullable_to_non_nullable
                  as String?,
      ),
    );
  }
}

/// @nodoc

class _$DataSliceImpl implements _DataSlice {
  const _$DataSliceImpl({
    required this.timestamp,
    required this.value,
    this.label,
  });

  @override
  final DateTime timestamp;
  @override
  final double value;
  @override
  final String? label;

  @override
  String toString() {
    return 'DataSlice(timestamp: $timestamp, value: $value, label: $label)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$DataSliceImpl &&
            (identical(other.timestamp, timestamp) ||
                other.timestamp == timestamp) &&
            (identical(other.value, value) || other.value == value) &&
            (identical(other.label, label) || other.label == label));
  }

  @override
  int get hashCode => Object.hash(runtimeType, timestamp, value, label);

  /// Create a copy of DataSlice
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$DataSliceImplCopyWith<_$DataSliceImpl> get copyWith =>
      __$$DataSliceImplCopyWithImpl<_$DataSliceImpl>(this, _$identity);
}

abstract class _DataSlice implements DataSlice {
  const factory _DataSlice({
    required final DateTime timestamp,
    required final double value,
    final String? label,
  }) = _$DataSliceImpl;

  @override
  DateTime get timestamp;
  @override
  double get value;
  @override
  String? get label;

  /// Create a copy of DataSlice
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$DataSliceImplCopyWith<_$DataSliceImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
mixin _$EnvironmentalSlice {
  @JsonKey(name: 'temperature_data')
  List<DataSlice> get temperatureData => throw _privateConstructorUsedError;
  @JsonKey(name: 'humidity_data')
  List<DataSlice> get humidityData => throw _privateConstructorUsedError;
  @JsonKey(name: 'ph_data')
  List<DataSlice> get phData => throw _privateConstructorUsedError;
  @JsonKey(name: 'ec_data')
  List<DataSlice> get ecData => throw _privateConstructorUsedError;

  /// Create a copy of EnvironmentalSlice
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $EnvironmentalSliceCopyWith<EnvironmentalSlice> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $EnvironmentalSliceCopyWith<$Res> {
  factory $EnvironmentalSliceCopyWith(
    EnvironmentalSlice value,
    $Res Function(EnvironmentalSlice) then,
  ) = _$EnvironmentalSliceCopyWithImpl<$Res, EnvironmentalSlice>;
  @useResult
  $Res call({
    @JsonKey(name: 'temperature_data') List<DataSlice> temperatureData,
    @JsonKey(name: 'humidity_data') List<DataSlice> humidityData,
    @JsonKey(name: 'ph_data') List<DataSlice> phData,
    @JsonKey(name: 'ec_data') List<DataSlice> ecData,
  });
}

/// @nodoc
class _$EnvironmentalSliceCopyWithImpl<$Res, $Val extends EnvironmentalSlice>
    implements $EnvironmentalSliceCopyWith<$Res> {
  _$EnvironmentalSliceCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of EnvironmentalSlice
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? temperatureData = null,
    Object? humidityData = null,
    Object? phData = null,
    Object? ecData = null,
  }) {
    return _then(
      _value.copyWith(
            temperatureData: null == temperatureData
                ? _value.temperatureData
                : temperatureData // ignore: cast_nullable_to_non_nullable
                      as List<DataSlice>,
            humidityData: null == humidityData
                ? _value.humidityData
                : humidityData // ignore: cast_nullable_to_non_nullable
                      as List<DataSlice>,
            phData: null == phData
                ? _value.phData
                : phData // ignore: cast_nullable_to_non_nullable
                      as List<DataSlice>,
            ecData: null == ecData
                ? _value.ecData
                : ecData // ignore: cast_nullable_to_non_nullable
                      as List<DataSlice>,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$EnvironmentalSliceImplCopyWith<$Res>
    implements $EnvironmentalSliceCopyWith<$Res> {
  factory _$$EnvironmentalSliceImplCopyWith(
    _$EnvironmentalSliceImpl value,
    $Res Function(_$EnvironmentalSliceImpl) then,
  ) = __$$EnvironmentalSliceImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    @JsonKey(name: 'temperature_data') List<DataSlice> temperatureData,
    @JsonKey(name: 'humidity_data') List<DataSlice> humidityData,
    @JsonKey(name: 'ph_data') List<DataSlice> phData,
    @JsonKey(name: 'ec_data') List<DataSlice> ecData,
  });
}

/// @nodoc
class __$$EnvironmentalSliceImplCopyWithImpl<$Res>
    extends _$EnvironmentalSliceCopyWithImpl<$Res, _$EnvironmentalSliceImpl>
    implements _$$EnvironmentalSliceImplCopyWith<$Res> {
  __$$EnvironmentalSliceImplCopyWithImpl(
    _$EnvironmentalSliceImpl _value,
    $Res Function(_$EnvironmentalSliceImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of EnvironmentalSlice
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? temperatureData = null,
    Object? humidityData = null,
    Object? phData = null,
    Object? ecData = null,
  }) {
    return _then(
      _$EnvironmentalSliceImpl(
        temperatureData: null == temperatureData
            ? _value._temperatureData
            : temperatureData // ignore: cast_nullable_to_non_nullable
                  as List<DataSlice>,
        humidityData: null == humidityData
            ? _value._humidityData
            : humidityData // ignore: cast_nullable_to_non_nullable
                  as List<DataSlice>,
        phData: null == phData
            ? _value._phData
            : phData // ignore: cast_nullable_to_non_nullable
                  as List<DataSlice>,
        ecData: null == ecData
            ? _value._ecData
            : ecData // ignore: cast_nullable_to_non_nullable
                  as List<DataSlice>,
      ),
    );
  }
}

/// @nodoc

class _$EnvironmentalSliceImpl implements _EnvironmentalSlice {
  const _$EnvironmentalSliceImpl({
    @JsonKey(name: 'temperature_data')
    final List<DataSlice> temperatureData = const [],
    @JsonKey(name: 'humidity_data')
    final List<DataSlice> humidityData = const [],
    @JsonKey(name: 'ph_data') final List<DataSlice> phData = const [],
    @JsonKey(name: 'ec_data') final List<DataSlice> ecData = const [],
  }) : _temperatureData = temperatureData,
       _humidityData = humidityData,
       _phData = phData,
       _ecData = ecData;

  final List<DataSlice> _temperatureData;
  @override
  @JsonKey(name: 'temperature_data')
  List<DataSlice> get temperatureData {
    if (_temperatureData is EqualUnmodifiableListView) return _temperatureData;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_temperatureData);
  }

  final List<DataSlice> _humidityData;
  @override
  @JsonKey(name: 'humidity_data')
  List<DataSlice> get humidityData {
    if (_humidityData is EqualUnmodifiableListView) return _humidityData;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_humidityData);
  }

  final List<DataSlice> _phData;
  @override
  @JsonKey(name: 'ph_data')
  List<DataSlice> get phData {
    if (_phData is EqualUnmodifiableListView) return _phData;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_phData);
  }

  final List<DataSlice> _ecData;
  @override
  @JsonKey(name: 'ec_data')
  List<DataSlice> get ecData {
    if (_ecData is EqualUnmodifiableListView) return _ecData;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_ecData);
  }

  @override
  String toString() {
    return 'EnvironmentalSlice(temperatureData: $temperatureData, humidityData: $humidityData, phData: $phData, ecData: $ecData)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$EnvironmentalSliceImpl &&
            const DeepCollectionEquality().equals(
              other._temperatureData,
              _temperatureData,
            ) &&
            const DeepCollectionEquality().equals(
              other._humidityData,
              _humidityData,
            ) &&
            const DeepCollectionEquality().equals(other._phData, _phData) &&
            const DeepCollectionEquality().equals(other._ecData, _ecData));
  }

  @override
  int get hashCode => Object.hash(
    runtimeType,
    const DeepCollectionEquality().hash(_temperatureData),
    const DeepCollectionEquality().hash(_humidityData),
    const DeepCollectionEquality().hash(_phData),
    const DeepCollectionEquality().hash(_ecData),
  );

  /// Create a copy of EnvironmentalSlice
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$EnvironmentalSliceImplCopyWith<_$EnvironmentalSliceImpl> get copyWith =>
      __$$EnvironmentalSliceImplCopyWithImpl<_$EnvironmentalSliceImpl>(
        this,
        _$identity,
      );
}

abstract class _EnvironmentalSlice implements EnvironmentalSlice {
  const factory _EnvironmentalSlice({
    @JsonKey(name: 'temperature_data') final List<DataSlice> temperatureData,
    @JsonKey(name: 'humidity_data') final List<DataSlice> humidityData,
    @JsonKey(name: 'ph_data') final List<DataSlice> phData,
    @JsonKey(name: 'ec_data') final List<DataSlice> ecData,
  }) = _$EnvironmentalSliceImpl;

  @override
  @JsonKey(name: 'temperature_data')
  List<DataSlice> get temperatureData;
  @override
  @JsonKey(name: 'humidity_data')
  List<DataSlice> get humidityData;
  @override
  @JsonKey(name: 'ph_data')
  List<DataSlice> get phData;
  @override
  @JsonKey(name: 'ec_data')
  List<DataSlice> get ecData;

  /// Create a copy of EnvironmentalSlice
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$EnvironmentalSliceImplCopyWith<_$EnvironmentalSliceImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
mixin _$GrowthPhaseSlice {
  String get name => throw _privateConstructorUsedError;
  int get count => throw _privateConstructorUsedError;
  double get percentage => throw _privateConstructorUsedError;

  /// Create a copy of GrowthPhaseSlice
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $GrowthPhaseSliceCopyWith<GrowthPhaseSlice> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $GrowthPhaseSliceCopyWith<$Res> {
  factory $GrowthPhaseSliceCopyWith(
    GrowthPhaseSlice value,
    $Res Function(GrowthPhaseSlice) then,
  ) = _$GrowthPhaseSliceCopyWithImpl<$Res, GrowthPhaseSlice>;
  @useResult
  $Res call({String name, int count, double percentage});
}

/// @nodoc
class _$GrowthPhaseSliceCopyWithImpl<$Res, $Val extends GrowthPhaseSlice>
    implements $GrowthPhaseSliceCopyWith<$Res> {
  _$GrowthPhaseSliceCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of GrowthPhaseSlice
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? name = null,
    Object? count = null,
    Object? percentage = null,
  }) {
    return _then(
      _value.copyWith(
            name: null == name
                ? _value.name
                : name // ignore: cast_nullable_to_non_nullable
                      as String,
            count: null == count
                ? _value.count
                : count // ignore: cast_nullable_to_non_nullable
                      as int,
            percentage: null == percentage
                ? _value.percentage
                : percentage // ignore: cast_nullable_to_non_nullable
                      as double,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$GrowthPhaseSliceImplCopyWith<$Res>
    implements $GrowthPhaseSliceCopyWith<$Res> {
  factory _$$GrowthPhaseSliceImplCopyWith(
    _$GrowthPhaseSliceImpl value,
    $Res Function(_$GrowthPhaseSliceImpl) then,
  ) = __$$GrowthPhaseSliceImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({String name, int count, double percentage});
}

/// @nodoc
class __$$GrowthPhaseSliceImplCopyWithImpl<$Res>
    extends _$GrowthPhaseSliceCopyWithImpl<$Res, _$GrowthPhaseSliceImpl>
    implements _$$GrowthPhaseSliceImplCopyWith<$Res> {
  __$$GrowthPhaseSliceImplCopyWithImpl(
    _$GrowthPhaseSliceImpl _value,
    $Res Function(_$GrowthPhaseSliceImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of GrowthPhaseSlice
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? name = null,
    Object? count = null,
    Object? percentage = null,
  }) {
    return _then(
      _$GrowthPhaseSliceImpl(
        name: null == name
            ? _value.name
            : name // ignore: cast_nullable_to_non_nullable
                  as String,
        count: null == count
            ? _value.count
            : count // ignore: cast_nullable_to_non_nullable
                  as int,
        percentage: null == percentage
            ? _value.percentage
            : percentage // ignore: cast_nullable_to_non_nullable
                  as double,
      ),
    );
  }
}

/// @nodoc

class _$GrowthPhaseSliceImpl implements _GrowthPhaseSlice {
  const _$GrowthPhaseSliceImpl({
    required this.name,
    required this.count,
    required this.percentage,
  });

  @override
  final String name;
  @override
  final int count;
  @override
  final double percentage;

  @override
  String toString() {
    return 'GrowthPhaseSlice(name: $name, count: $count, percentage: $percentage)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$GrowthPhaseSliceImpl &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.count, count) || other.count == count) &&
            (identical(other.percentage, percentage) ||
                other.percentage == percentage));
  }

  @override
  int get hashCode => Object.hash(runtimeType, name, count, percentage);

  /// Create a copy of GrowthPhaseSlice
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$GrowthPhaseSliceImplCopyWith<_$GrowthPhaseSliceImpl> get copyWith =>
      __$$GrowthPhaseSliceImplCopyWithImpl<_$GrowthPhaseSliceImpl>(
        this,
        _$identity,
      );
}

abstract class _GrowthPhaseSlice implements GrowthPhaseSlice {
  const factory _GrowthPhaseSlice({
    required final String name,
    required final int count,
    required final double percentage,
  }) = _$GrowthPhaseSliceImpl;

  @override
  String get name;
  @override
  int get count;
  @override
  double get percentage;

  /// Create a copy of GrowthPhaseSlice
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$GrowthPhaseSliceImplCopyWith<_$GrowthPhaseSliceImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
mixin _$RecentReading {
  DateTime get timestamp => throw _privateConstructorUsedError;
  @JsonKey(name: 'sensor_type')
  String get sensorType => throw _privateConstructorUsedError;
  double get value => throw _privateConstructorUsedError;
  String get unit => throw _privateConstructorUsedError;
  String? get location => throw _privateConstructorUsedError;

  /// Create a copy of RecentReading
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $RecentReadingCopyWith<RecentReading> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $RecentReadingCopyWith<$Res> {
  factory $RecentReadingCopyWith(
    RecentReading value,
    $Res Function(RecentReading) then,
  ) = _$RecentReadingCopyWithImpl<$Res, RecentReading>;
  @useResult
  $Res call({
    DateTime timestamp,
    @JsonKey(name: 'sensor_type') String sensorType,
    double value,
    String unit,
    String? location,
  });
}

/// @nodoc
class _$RecentReadingCopyWithImpl<$Res, $Val extends RecentReading>
    implements $RecentReadingCopyWith<$Res> {
  _$RecentReadingCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of RecentReading
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? timestamp = null,
    Object? sensorType = null,
    Object? value = null,
    Object? unit = null,
    Object? location = freezed,
  }) {
    return _then(
      _value.copyWith(
            timestamp: null == timestamp
                ? _value.timestamp
                : timestamp // ignore: cast_nullable_to_non_nullable
                      as DateTime,
            sensorType: null == sensorType
                ? _value.sensorType
                : sensorType // ignore: cast_nullable_to_non_nullable
                      as String,
            value: null == value
                ? _value.value
                : value // ignore: cast_nullable_to_non_nullable
                      as double,
            unit: null == unit
                ? _value.unit
                : unit // ignore: cast_nullable_to_non_nullable
                      as String,
            location: freezed == location
                ? _value.location
                : location // ignore: cast_nullable_to_non_nullable
                      as String?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$RecentReadingImplCopyWith<$Res>
    implements $RecentReadingCopyWith<$Res> {
  factory _$$RecentReadingImplCopyWith(
    _$RecentReadingImpl value,
    $Res Function(_$RecentReadingImpl) then,
  ) = __$$RecentReadingImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    DateTime timestamp,
    @JsonKey(name: 'sensor_type') String sensorType,
    double value,
    String unit,
    String? location,
  });
}

/// @nodoc
class __$$RecentReadingImplCopyWithImpl<$Res>
    extends _$RecentReadingCopyWithImpl<$Res, _$RecentReadingImpl>
    implements _$$RecentReadingImplCopyWith<$Res> {
  __$$RecentReadingImplCopyWithImpl(
    _$RecentReadingImpl _value,
    $Res Function(_$RecentReadingImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of RecentReading
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? timestamp = null,
    Object? sensorType = null,
    Object? value = null,
    Object? unit = null,
    Object? location = freezed,
  }) {
    return _then(
      _$RecentReadingImpl(
        timestamp: null == timestamp
            ? _value.timestamp
            : timestamp // ignore: cast_nullable_to_non_nullable
                  as DateTime,
        sensorType: null == sensorType
            ? _value.sensorType
            : sensorType // ignore: cast_nullable_to_non_nullable
                  as String,
        value: null == value
            ? _value.value
            : value // ignore: cast_nullable_to_non_nullable
                  as double,
        unit: null == unit
            ? _value.unit
            : unit // ignore: cast_nullable_to_non_nullable
                  as String,
        location: freezed == location
            ? _value.location
            : location // ignore: cast_nullable_to_non_nullable
                  as String?,
      ),
    );
  }
}

/// @nodoc

class _$RecentReadingImpl implements _RecentReading {
  const _$RecentReadingImpl({
    required this.timestamp,
    @JsonKey(name: 'sensor_type') required this.sensorType,
    required this.value,
    required this.unit,
    this.location,
  });

  @override
  final DateTime timestamp;
  @override
  @JsonKey(name: 'sensor_type')
  final String sensorType;
  @override
  final double value;
  @override
  final String unit;
  @override
  final String? location;

  @override
  String toString() {
    return 'RecentReading(timestamp: $timestamp, sensorType: $sensorType, value: $value, unit: $unit, location: $location)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$RecentReadingImpl &&
            (identical(other.timestamp, timestamp) ||
                other.timestamp == timestamp) &&
            (identical(other.sensorType, sensorType) ||
                other.sensorType == sensorType) &&
            (identical(other.value, value) || other.value == value) &&
            (identical(other.unit, unit) || other.unit == unit) &&
            (identical(other.location, location) ||
                other.location == location));
  }

  @override
  int get hashCode =>
      Object.hash(runtimeType, timestamp, sensorType, value, unit, location);

  /// Create a copy of RecentReading
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$RecentReadingImplCopyWith<_$RecentReadingImpl> get copyWith =>
      __$$RecentReadingImplCopyWithImpl<_$RecentReadingImpl>(this, _$identity);
}

abstract class _RecentReading implements RecentReading {
  const factory _RecentReading({
    required final DateTime timestamp,
    @JsonKey(name: 'sensor_type') required final String sensorType,
    required final double value,
    required final String unit,
    final String? location,
  }) = _$RecentReadingImpl;

  @override
  DateTime get timestamp;
  @override
  @JsonKey(name: 'sensor_type')
  String get sensorType;
  @override
  double get value;
  @override
  String get unit;
  @override
  String? get location;

  /// Create a copy of RecentReading
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$RecentReadingImplCopyWith<_$RecentReadingImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
mixin _$RecentActivity {
  DateTime get timestamp => throw _privateConstructorUsedError;
  @JsonKey(name: 'activity_type')
  String get activityType => throw _privateConstructorUsedError;
  String get description => throw _privateConstructorUsedError;
  @JsonKey(name: 'plant_id')
  int? get plantId => throw _privateConstructorUsedError;
  String get severity => throw _privateConstructorUsedError;

  /// Create a copy of RecentActivity
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $RecentActivityCopyWith<RecentActivity> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $RecentActivityCopyWith<$Res> {
  factory $RecentActivityCopyWith(
    RecentActivity value,
    $Res Function(RecentActivity) then,
  ) = _$RecentActivityCopyWithImpl<$Res, RecentActivity>;
  @useResult
  $Res call({
    DateTime timestamp,
    @JsonKey(name: 'activity_type') String activityType,
    String description,
    @JsonKey(name: 'plant_id') int? plantId,
    String severity,
  });
}

/// @nodoc
class _$RecentActivityCopyWithImpl<$Res, $Val extends RecentActivity>
    implements $RecentActivityCopyWith<$Res> {
  _$RecentActivityCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of RecentActivity
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? timestamp = null,
    Object? activityType = null,
    Object? description = null,
    Object? plantId = freezed,
    Object? severity = null,
  }) {
    return _then(
      _value.copyWith(
            timestamp: null == timestamp
                ? _value.timestamp
                : timestamp // ignore: cast_nullable_to_non_nullable
                      as DateTime,
            activityType: null == activityType
                ? _value.activityType
                : activityType // ignore: cast_nullable_to_non_nullable
                      as String,
            description: null == description
                ? _value.description
                : description // ignore: cast_nullable_to_non_nullable
                      as String,
            plantId: freezed == plantId
                ? _value.plantId
                : plantId // ignore: cast_nullable_to_non_nullable
                      as int?,
            severity: null == severity
                ? _value.severity
                : severity // ignore: cast_nullable_to_non_nullable
                      as String,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$RecentActivityImplCopyWith<$Res>
    implements $RecentActivityCopyWith<$Res> {
  factory _$$RecentActivityImplCopyWith(
    _$RecentActivityImpl value,
    $Res Function(_$RecentActivityImpl) then,
  ) = __$$RecentActivityImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    DateTime timestamp,
    @JsonKey(name: 'activity_type') String activityType,
    String description,
    @JsonKey(name: 'plant_id') int? plantId,
    String severity,
  });
}

/// @nodoc
class __$$RecentActivityImplCopyWithImpl<$Res>
    extends _$RecentActivityCopyWithImpl<$Res, _$RecentActivityImpl>
    implements _$$RecentActivityImplCopyWith<$Res> {
  __$$RecentActivityImplCopyWithImpl(
    _$RecentActivityImpl _value,
    $Res Function(_$RecentActivityImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of RecentActivity
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? timestamp = null,
    Object? activityType = null,
    Object? description = null,
    Object? plantId = freezed,
    Object? severity = null,
  }) {
    return _then(
      _$RecentActivityImpl(
        timestamp: null == timestamp
            ? _value.timestamp
            : timestamp // ignore: cast_nullable_to_non_nullable
                  as DateTime,
        activityType: null == activityType
            ? _value.activityType
            : activityType // ignore: cast_nullable_to_non_nullable
                  as String,
        description: null == description
            ? _value.description
            : description // ignore: cast_nullable_to_non_nullable
                  as String,
        plantId: freezed == plantId
            ? _value.plantId
            : plantId // ignore: cast_nullable_to_non_nullable
                  as int?,
        severity: null == severity
            ? _value.severity
            : severity // ignore: cast_nullable_to_non_nullable
                  as String,
      ),
    );
  }
}

/// @nodoc

class _$RecentActivityImpl implements _RecentActivity {
  const _$RecentActivityImpl({
    required this.timestamp,
    @JsonKey(name: 'activity_type') required this.activityType,
    required this.description,
    @JsonKey(name: 'plant_id') this.plantId,
    required this.severity,
  });

  @override
  final DateTime timestamp;
  @override
  @JsonKey(name: 'activity_type')
  final String activityType;
  @override
  final String description;
  @override
  @JsonKey(name: 'plant_id')
  final int? plantId;
  @override
  final String severity;

  @override
  String toString() {
    return 'RecentActivity(timestamp: $timestamp, activityType: $activityType, description: $description, plantId: $plantId, severity: $severity)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$RecentActivityImpl &&
            (identical(other.timestamp, timestamp) ||
                other.timestamp == timestamp) &&
            (identical(other.activityType, activityType) ||
                other.activityType == activityType) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.plantId, plantId) || other.plantId == plantId) &&
            (identical(other.severity, severity) ||
                other.severity == severity));
  }

  @override
  int get hashCode => Object.hash(
    runtimeType,
    timestamp,
    activityType,
    description,
    plantId,
    severity,
  );

  /// Create a copy of RecentActivity
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$RecentActivityImplCopyWith<_$RecentActivityImpl> get copyWith =>
      __$$RecentActivityImplCopyWithImpl<_$RecentActivityImpl>(
        this,
        _$identity,
      );
}

abstract class _RecentActivity implements RecentActivity {
  const factory _RecentActivity({
    required final DateTime timestamp,
    @JsonKey(name: 'activity_type') required final String activityType,
    required final String description,
    @JsonKey(name: 'plant_id') final int? plantId,
    required final String severity,
  }) = _$RecentActivityImpl;

  @override
  DateTime get timestamp;
  @override
  @JsonKey(name: 'activity_type')
  String get activityType;
  @override
  String get description;
  @override
  @JsonKey(name: 'plant_id')
  int? get plantId;
  @override
  String get severity;

  /// Create a copy of RecentActivity
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$RecentActivityImplCopyWith<_$RecentActivityImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
mixin _$DashboardStats {
  CountStats get counts => throw _privateConstructorUsedError;
  CultivarStats get cultivars => throw _privateConstructorUsedError;
  EnvironmentalStats get environment => throw _privateConstructorUsedError;
  SensorStats get sensors => throw _privateConstructorUsedError;
  @JsonKey(name: 'data_slices')
  EnvironmentalSlice get dataSlices => throw _privateConstructorUsedError;
  @JsonKey(name: 'growth_phases')
  List<GrowthPhaseSlice> get growthPhases => throw _privateConstructorUsedError;
  @JsonKey(name: 'recent_readings')
  List<RecentReading> get recentReadings => throw _privateConstructorUsedError;
  @JsonKey(name: 'recent_activities')
  List<RecentActivity> get recentActivities =>
      throw _privateConstructorUsedError;
  @JsonKey(name: 'generated_at')
  DateTime get generatedAt => throw _privateConstructorUsedError;
  @JsonKey(name: 'user_id')
  int get userId => throw _privateConstructorUsedError;

  /// Create a copy of DashboardStats
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $DashboardStatsCopyWith<DashboardStats> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $DashboardStatsCopyWith<$Res> {
  factory $DashboardStatsCopyWith(
    DashboardStats value,
    $Res Function(DashboardStats) then,
  ) = _$DashboardStatsCopyWithImpl<$Res, DashboardStats>;
  @useResult
  $Res call({
    CountStats counts,
    CultivarStats cultivars,
    EnvironmentalStats environment,
    SensorStats sensors,
    @JsonKey(name: 'data_slices') EnvironmentalSlice dataSlices,
    @JsonKey(name: 'growth_phases') List<GrowthPhaseSlice> growthPhases,
    @JsonKey(name: 'recent_readings') List<RecentReading> recentReadings,
    @JsonKey(name: 'recent_activities') List<RecentActivity> recentActivities,
    @JsonKey(name: 'generated_at') DateTime generatedAt,
    @JsonKey(name: 'user_id') int userId,
  });

  $CountStatsCopyWith<$Res> get counts;
  $CultivarStatsCopyWith<$Res> get cultivars;
  $EnvironmentalStatsCopyWith<$Res> get environment;
  $SensorStatsCopyWith<$Res> get sensors;
  $EnvironmentalSliceCopyWith<$Res> get dataSlices;
}

/// @nodoc
class _$DashboardStatsCopyWithImpl<$Res, $Val extends DashboardStats>
    implements $DashboardStatsCopyWith<$Res> {
  _$DashboardStatsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of DashboardStats
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? counts = null,
    Object? cultivars = null,
    Object? environment = null,
    Object? sensors = null,
    Object? dataSlices = null,
    Object? growthPhases = null,
    Object? recentReadings = null,
    Object? recentActivities = null,
    Object? generatedAt = null,
    Object? userId = null,
  }) {
    return _then(
      _value.copyWith(
            counts: null == counts
                ? _value.counts
                : counts // ignore: cast_nullable_to_non_nullable
                      as CountStats,
            cultivars: null == cultivars
                ? _value.cultivars
                : cultivars // ignore: cast_nullable_to_non_nullable
                      as CultivarStats,
            environment: null == environment
                ? _value.environment
                : environment // ignore: cast_nullable_to_non_nullable
                      as EnvironmentalStats,
            sensors: null == sensors
                ? _value.sensors
                : sensors // ignore: cast_nullable_to_non_nullable
                      as SensorStats,
            dataSlices: null == dataSlices
                ? _value.dataSlices
                : dataSlices // ignore: cast_nullable_to_non_nullable
                      as EnvironmentalSlice,
            growthPhases: null == growthPhases
                ? _value.growthPhases
                : growthPhases // ignore: cast_nullable_to_non_nullable
                      as List<GrowthPhaseSlice>,
            recentReadings: null == recentReadings
                ? _value.recentReadings
                : recentReadings // ignore: cast_nullable_to_non_nullable
                      as List<RecentReading>,
            recentActivities: null == recentActivities
                ? _value.recentActivities
                : recentActivities // ignore: cast_nullable_to_non_nullable
                      as List<RecentActivity>,
            generatedAt: null == generatedAt
                ? _value.generatedAt
                : generatedAt // ignore: cast_nullable_to_non_nullable
                      as DateTime,
            userId: null == userId
                ? _value.userId
                : userId // ignore: cast_nullable_to_non_nullable
                      as int,
          )
          as $Val,
    );
  }

  /// Create a copy of DashboardStats
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $CountStatsCopyWith<$Res> get counts {
    return $CountStatsCopyWith<$Res>(_value.counts, (value) {
      return _then(_value.copyWith(counts: value) as $Val);
    });
  }

  /// Create a copy of DashboardStats
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $CultivarStatsCopyWith<$Res> get cultivars {
    return $CultivarStatsCopyWith<$Res>(_value.cultivars, (value) {
      return _then(_value.copyWith(cultivars: value) as $Val);
    });
  }

  /// Create a copy of DashboardStats
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $EnvironmentalStatsCopyWith<$Res> get environment {
    return $EnvironmentalStatsCopyWith<$Res>(_value.environment, (value) {
      return _then(_value.copyWith(environment: value) as $Val);
    });
  }

  /// Create a copy of DashboardStats
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $SensorStatsCopyWith<$Res> get sensors {
    return $SensorStatsCopyWith<$Res>(_value.sensors, (value) {
      return _then(_value.copyWith(sensors: value) as $Val);
    });
  }

  /// Create a copy of DashboardStats
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $EnvironmentalSliceCopyWith<$Res> get dataSlices {
    return $EnvironmentalSliceCopyWith<$Res>(_value.dataSlices, (value) {
      return _then(_value.copyWith(dataSlices: value) as $Val);
    });
  }
}

/// @nodoc
abstract class _$$DashboardStatsImplCopyWith<$Res>
    implements $DashboardStatsCopyWith<$Res> {
  factory _$$DashboardStatsImplCopyWith(
    _$DashboardStatsImpl value,
    $Res Function(_$DashboardStatsImpl) then,
  ) = __$$DashboardStatsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    CountStats counts,
    CultivarStats cultivars,
    EnvironmentalStats environment,
    SensorStats sensors,
    @JsonKey(name: 'data_slices') EnvironmentalSlice dataSlices,
    @JsonKey(name: 'growth_phases') List<GrowthPhaseSlice> growthPhases,
    @JsonKey(name: 'recent_readings') List<RecentReading> recentReadings,
    @JsonKey(name: 'recent_activities') List<RecentActivity> recentActivities,
    @JsonKey(name: 'generated_at') DateTime generatedAt,
    @JsonKey(name: 'user_id') int userId,
  });

  @override
  $CountStatsCopyWith<$Res> get counts;
  @override
  $CultivarStatsCopyWith<$Res> get cultivars;
  @override
  $EnvironmentalStatsCopyWith<$Res> get environment;
  @override
  $SensorStatsCopyWith<$Res> get sensors;
  @override
  $EnvironmentalSliceCopyWith<$Res> get dataSlices;
}

/// @nodoc
class __$$DashboardStatsImplCopyWithImpl<$Res>
    extends _$DashboardStatsCopyWithImpl<$Res, _$DashboardStatsImpl>
    implements _$$DashboardStatsImplCopyWith<$Res> {
  __$$DashboardStatsImplCopyWithImpl(
    _$DashboardStatsImpl _value,
    $Res Function(_$DashboardStatsImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of DashboardStats
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? counts = null,
    Object? cultivars = null,
    Object? environment = null,
    Object? sensors = null,
    Object? dataSlices = null,
    Object? growthPhases = null,
    Object? recentReadings = null,
    Object? recentActivities = null,
    Object? generatedAt = null,
    Object? userId = null,
  }) {
    return _then(
      _$DashboardStatsImpl(
        counts: null == counts
            ? _value.counts
            : counts // ignore: cast_nullable_to_non_nullable
                  as CountStats,
        cultivars: null == cultivars
            ? _value.cultivars
            : cultivars // ignore: cast_nullable_to_non_nullable
                  as CultivarStats,
        environment: null == environment
            ? _value.environment
            : environment // ignore: cast_nullable_to_non_nullable
                  as EnvironmentalStats,
        sensors: null == sensors
            ? _value.sensors
            : sensors // ignore: cast_nullable_to_non_nullable
                  as SensorStats,
        dataSlices: null == dataSlices
            ? _value.dataSlices
            : dataSlices // ignore: cast_nullable_to_non_nullable
                  as EnvironmentalSlice,
        growthPhases: null == growthPhases
            ? _value._growthPhases
            : growthPhases // ignore: cast_nullable_to_non_nullable
                  as List<GrowthPhaseSlice>,
        recentReadings: null == recentReadings
            ? _value._recentReadings
            : recentReadings // ignore: cast_nullable_to_non_nullable
                  as List<RecentReading>,
        recentActivities: null == recentActivities
            ? _value._recentActivities
            : recentActivities // ignore: cast_nullable_to_non_nullable
                  as List<RecentActivity>,
        generatedAt: null == generatedAt
            ? _value.generatedAt
            : generatedAt // ignore: cast_nullable_to_non_nullable
                  as DateTime,
        userId: null == userId
            ? _value.userId
            : userId // ignore: cast_nullable_to_non_nullable
                  as int,
      ),
    );
  }
}

/// @nodoc

class _$DashboardStatsImpl implements _DashboardStats {
  const _$DashboardStatsImpl({
    required this.counts,
    required this.cultivars,
    required this.environment,
    required this.sensors,
    @JsonKey(name: 'data_slices') required this.dataSlices,
    @JsonKey(name: 'growth_phases')
    final List<GrowthPhaseSlice> growthPhases = const [],
    @JsonKey(name: 'recent_readings')
    final List<RecentReading> recentReadings = const [],
    @JsonKey(name: 'recent_activities')
    final List<RecentActivity> recentActivities = const [],
    @JsonKey(name: 'generated_at') required this.generatedAt,
    @JsonKey(name: 'user_id') required this.userId,
  }) : _growthPhases = growthPhases,
       _recentReadings = recentReadings,
       _recentActivities = recentActivities;

  @override
  final CountStats counts;
  @override
  final CultivarStats cultivars;
  @override
  final EnvironmentalStats environment;
  @override
  final SensorStats sensors;
  @override
  @JsonKey(name: 'data_slices')
  final EnvironmentalSlice dataSlices;
  final List<GrowthPhaseSlice> _growthPhases;
  @override
  @JsonKey(name: 'growth_phases')
  List<GrowthPhaseSlice> get growthPhases {
    if (_growthPhases is EqualUnmodifiableListView) return _growthPhases;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_growthPhases);
  }

  final List<RecentReading> _recentReadings;
  @override
  @JsonKey(name: 'recent_readings')
  List<RecentReading> get recentReadings {
    if (_recentReadings is EqualUnmodifiableListView) return _recentReadings;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_recentReadings);
  }

  final List<RecentActivity> _recentActivities;
  @override
  @JsonKey(name: 'recent_activities')
  List<RecentActivity> get recentActivities {
    if (_recentActivities is EqualUnmodifiableListView)
      return _recentActivities;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_recentActivities);
  }

  @override
  @JsonKey(name: 'generated_at')
  final DateTime generatedAt;
  @override
  @JsonKey(name: 'user_id')
  final int userId;

  @override
  String toString() {
    return 'DashboardStats(counts: $counts, cultivars: $cultivars, environment: $environment, sensors: $sensors, dataSlices: $dataSlices, growthPhases: $growthPhases, recentReadings: $recentReadings, recentActivities: $recentActivities, generatedAt: $generatedAt, userId: $userId)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$DashboardStatsImpl &&
            (identical(other.counts, counts) || other.counts == counts) &&
            (identical(other.cultivars, cultivars) ||
                other.cultivars == cultivars) &&
            (identical(other.environment, environment) ||
                other.environment == environment) &&
            (identical(other.sensors, sensors) || other.sensors == sensors) &&
            (identical(other.dataSlices, dataSlices) ||
                other.dataSlices == dataSlices) &&
            const DeepCollectionEquality().equals(
              other._growthPhases,
              _growthPhases,
            ) &&
            const DeepCollectionEquality().equals(
              other._recentReadings,
              _recentReadings,
            ) &&
            const DeepCollectionEquality().equals(
              other._recentActivities,
              _recentActivities,
            ) &&
            (identical(other.generatedAt, generatedAt) ||
                other.generatedAt == generatedAt) &&
            (identical(other.userId, userId) || other.userId == userId));
  }

  @override
  int get hashCode => Object.hash(
    runtimeType,
    counts,
    cultivars,
    environment,
    sensors,
    dataSlices,
    const DeepCollectionEquality().hash(_growthPhases),
    const DeepCollectionEquality().hash(_recentReadings),
    const DeepCollectionEquality().hash(_recentActivities),
    generatedAt,
    userId,
  );

  /// Create a copy of DashboardStats
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$DashboardStatsImplCopyWith<_$DashboardStatsImpl> get copyWith =>
      __$$DashboardStatsImplCopyWithImpl<_$DashboardStatsImpl>(
        this,
        _$identity,
      );
}

abstract class _DashboardStats implements DashboardStats {
  const factory _DashboardStats({
    required final CountStats counts,
    required final CultivarStats cultivars,
    required final EnvironmentalStats environment,
    required final SensorStats sensors,
    @JsonKey(name: 'data_slices') required final EnvironmentalSlice dataSlices,
    @JsonKey(name: 'growth_phases') final List<GrowthPhaseSlice> growthPhases,
    @JsonKey(name: 'recent_readings') final List<RecentReading> recentReadings,
    @JsonKey(name: 'recent_activities')
    final List<RecentActivity> recentActivities,
    @JsonKey(name: 'generated_at') required final DateTime generatedAt,
    @JsonKey(name: 'user_id') required final int userId,
  }) = _$DashboardStatsImpl;

  @override
  CountStats get counts;
  @override
  CultivarStats get cultivars;
  @override
  EnvironmentalStats get environment;
  @override
  SensorStats get sensors;
  @override
  @JsonKey(name: 'data_slices')
  EnvironmentalSlice get dataSlices;
  @override
  @JsonKey(name: 'growth_phases')
  List<GrowthPhaseSlice> get growthPhases;
  @override
  @JsonKey(name: 'recent_readings')
  List<RecentReading> get recentReadings;
  @override
  @JsonKey(name: 'recent_activities')
  List<RecentActivity> get recentActivities;
  @override
  @JsonKey(name: 'generated_at')
  DateTime get generatedAt;
  @override
  @JsonKey(name: 'user_id')
  int get userId;

  /// Create a copy of DashboardStats
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$DashboardStatsImplCopyWith<_$DashboardStatsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
mixin _$Activity {
  int get id => throw _privateConstructorUsedError;
  String get description => throw _privateConstructorUsedError;
  @JsonKey(name: 'created_at')
  DateTime get createdAt => throw _privateConstructorUsedError;

  /// Create a copy of Activity
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $ActivityCopyWith<Activity> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ActivityCopyWith<$Res> {
  factory $ActivityCopyWith(Activity value, $Res Function(Activity) then) =
      _$ActivityCopyWithImpl<$Res, Activity>;
  @useResult
  $Res call({
    int id,
    String description,
    @JsonKey(name: 'created_at') DateTime createdAt,
  });
}

/// @nodoc
class _$ActivityCopyWithImpl<$Res, $Val extends Activity>
    implements $ActivityCopyWith<$Res> {
  _$ActivityCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of Activity
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? description = null,
    Object? createdAt = null,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as int,
            description: null == description
                ? _value.description
                : description // ignore: cast_nullable_to_non_nullable
                      as String,
            createdAt: null == createdAt
                ? _value.createdAt
                : createdAt // ignore: cast_nullable_to_non_nullable
                      as DateTime,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$ActivityImplCopyWith<$Res>
    implements $ActivityCopyWith<$Res> {
  factory _$$ActivityImplCopyWith(
    _$ActivityImpl value,
    $Res Function(_$ActivityImpl) then,
  ) = __$$ActivityImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    int id,
    String description,
    @JsonKey(name: 'created_at') DateTime createdAt,
  });
}

/// @nodoc
class __$$ActivityImplCopyWithImpl<$Res>
    extends _$ActivityCopyWithImpl<$Res, _$ActivityImpl>
    implements _$$ActivityImplCopyWith<$Res> {
  __$$ActivityImplCopyWithImpl(
    _$ActivityImpl _value,
    $Res Function(_$ActivityImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of Activity
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? description = null,
    Object? createdAt = null,
  }) {
    return _then(
      _$ActivityImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as int,
        description: null == description
            ? _value.description
            : description // ignore: cast_nullable_to_non_nullable
                  as String,
        createdAt: null == createdAt
            ? _value.createdAt
            : createdAt // ignore: cast_nullable_to_non_nullable
                  as DateTime,
      ),
    );
  }
}

/// @nodoc

class _$ActivityImpl implements _Activity {
  const _$ActivityImpl({
    required this.id,
    required this.description,
    @JsonKey(name: 'created_at') required this.createdAt,
  });

  @override
  final int id;
  @override
  final String description;
  @override
  @JsonKey(name: 'created_at')
  final DateTime createdAt;

  @override
  String toString() {
    return 'Activity(id: $id, description: $description, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ActivityImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @override
  int get hashCode => Object.hash(runtimeType, id, description, createdAt);

  /// Create a copy of Activity
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$ActivityImplCopyWith<_$ActivityImpl> get copyWith =>
      __$$ActivityImplCopyWithImpl<_$ActivityImpl>(this, _$identity);
}

abstract class _Activity implements Activity {
  const factory _Activity({
    required final int id,
    required final String description,
    @JsonKey(name: 'created_at') required final DateTime createdAt,
  }) = _$ActivityImpl;

  @override
  int get id;
  @override
  String get description;
  @override
  @JsonKey(name: 'created_at')
  DateTime get createdAt;

  /// Create a copy of Activity
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$ActivityImplCopyWith<_$ActivityImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
mixin _$Task {
  int get id => throw _privateConstructorUsedError;
  String get title => throw _privateConstructorUsedError;
  @JsonKey(name: 'due_date')
  DateTime get dueDate => throw _privateConstructorUsedError;

  /// Create a copy of Task
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $TaskCopyWith<Task> get copyWith => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $TaskCopyWith<$Res> {
  factory $TaskCopyWith(Task value, $Res Function(Task) then) =
      _$TaskCopyWithImpl<$Res, Task>;
  @useResult
  $Res call({
    int id,
    String title,
    @JsonKey(name: 'due_date') DateTime dueDate,
  });
}

/// @nodoc
class _$TaskCopyWithImpl<$Res, $Val extends Task>
    implements $TaskCopyWith<$Res> {
  _$TaskCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of Task
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({Object? id = null, Object? title = null, Object? dueDate = null}) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as int,
            title: null == title
                ? _value.title
                : title // ignore: cast_nullable_to_non_nullable
                      as String,
            dueDate: null == dueDate
                ? _value.dueDate
                : dueDate // ignore: cast_nullable_to_non_nullable
                      as DateTime,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$TaskImplCopyWith<$Res> implements $TaskCopyWith<$Res> {
  factory _$$TaskImplCopyWith(
    _$TaskImpl value,
    $Res Function(_$TaskImpl) then,
  ) = __$$TaskImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    int id,
    String title,
    @JsonKey(name: 'due_date') DateTime dueDate,
  });
}

/// @nodoc
class __$$TaskImplCopyWithImpl<$Res>
    extends _$TaskCopyWithImpl<$Res, _$TaskImpl>
    implements _$$TaskImplCopyWith<$Res> {
  __$$TaskImplCopyWithImpl(_$TaskImpl _value, $Res Function(_$TaskImpl) _then)
    : super(_value, _then);

  /// Create a copy of Task
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({Object? id = null, Object? title = null, Object? dueDate = null}) {
    return _then(
      _$TaskImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as int,
        title: null == title
            ? _value.title
            : title // ignore: cast_nullable_to_non_nullable
                  as String,
        dueDate: null == dueDate
            ? _value.dueDate
            : dueDate // ignore: cast_nullable_to_non_nullable
                  as DateTime,
      ),
    );
  }
}

/// @nodoc

class _$TaskImpl implements _Task {
  const _$TaskImpl({
    required this.id,
    required this.title,
    @JsonKey(name: 'due_date') required this.dueDate,
  });

  @override
  final int id;
  @override
  final String title;
  @override
  @JsonKey(name: 'due_date')
  final DateTime dueDate;

  @override
  String toString() {
    return 'Task(id: $id, title: $title, dueDate: $dueDate)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$TaskImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.title, title) || other.title == title) &&
            (identical(other.dueDate, dueDate) || other.dueDate == dueDate));
  }

  @override
  int get hashCode => Object.hash(runtimeType, id, title, dueDate);

  /// Create a copy of Task
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$TaskImplCopyWith<_$TaskImpl> get copyWith =>
      __$$TaskImplCopyWithImpl<_$TaskImpl>(this, _$identity);
}

abstract class _Task implements Task {
  const factory _Task({
    required final int id,
    required final String title,
    @JsonKey(name: 'due_date') required final DateTime dueDate,
  }) = _$TaskImpl;

  @override
  int get id;
  @override
  String get title;
  @override
  @JsonKey(name: 'due_date')
  DateTime get dueDate;

  /// Create a copy of Task
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$TaskImplCopyWith<_$TaskImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
