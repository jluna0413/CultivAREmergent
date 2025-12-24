// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'ai_dashboard_stats.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

/// @nodoc
mixin _$AIActivity {
  DateTime get timestamp => throw _privateConstructorUsedError;
  @JsonKey(name: 'activity_type')
  String get activityType => throw _privateConstructorUsedError;
  String get description => throw _privateConstructorUsedError;
  String? get feature => throw _privateConstructorUsedError;
  String? get result => throw _privateConstructorUsedError;

  /// Create a copy of AIActivity
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $AIActivityCopyWith<AIActivity> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AIActivityCopyWith<$Res> {
  factory $AIActivityCopyWith(
    AIActivity value,
    $Res Function(AIActivity) then,
  ) = _$AIActivityCopyWithImpl<$Res, AIActivity>;
  @useResult
  $Res call({
    DateTime timestamp,
    @JsonKey(name: 'activity_type') String activityType,
    String description,
    String? feature,
    String? result,
  });
}

/// @nodoc
class _$AIActivityCopyWithImpl<$Res, $Val extends AIActivity>
    implements $AIActivityCopyWith<$Res> {
  _$AIActivityCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of AIActivity
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? timestamp = null,
    Object? activityType = null,
    Object? description = null,
    Object? feature = freezed,
    Object? result = freezed,
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
            feature: freezed == feature
                ? _value.feature
                : feature // ignore: cast_nullable_to_non_nullable
                      as String?,
            result: freezed == result
                ? _value.result
                : result // ignore: cast_nullable_to_non_nullable
                      as String?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$AIActivityImplCopyWith<$Res>
    implements $AIActivityCopyWith<$Res> {
  factory _$$AIActivityImplCopyWith(
    _$AIActivityImpl value,
    $Res Function(_$AIActivityImpl) then,
  ) = __$$AIActivityImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    DateTime timestamp,
    @JsonKey(name: 'activity_type') String activityType,
    String description,
    String? feature,
    String? result,
  });
}

/// @nodoc
class __$$AIActivityImplCopyWithImpl<$Res>
    extends _$AIActivityCopyWithImpl<$Res, _$AIActivityImpl>
    implements _$$AIActivityImplCopyWith<$Res> {
  __$$AIActivityImplCopyWithImpl(
    _$AIActivityImpl _value,
    $Res Function(_$AIActivityImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of AIActivity
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? timestamp = null,
    Object? activityType = null,
    Object? description = null,
    Object? feature = freezed,
    Object? result = freezed,
  }) {
    return _then(
      _$AIActivityImpl(
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
        feature: freezed == feature
            ? _value.feature
            : feature // ignore: cast_nullable_to_non_nullable
                  as String?,
        result: freezed == result
            ? _value.result
            : result // ignore: cast_nullable_to_non_nullable
                  as String?,
      ),
    );
  }
}

/// @nodoc

class _$AIActivityImpl implements _AIActivity {
  const _$AIActivityImpl({
    required this.timestamp,
    @JsonKey(name: 'activity_type') required this.activityType,
    required this.description,
    this.feature,
    this.result,
  });

  @override
  final DateTime timestamp;
  @override
  @JsonKey(name: 'activity_type')
  final String activityType;
  @override
  final String description;
  @override
  final String? feature;
  @override
  final String? result;

  @override
  String toString() {
    return 'AIActivity(timestamp: $timestamp, activityType: $activityType, description: $description, feature: $feature, result: $result)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AIActivityImpl &&
            (identical(other.timestamp, timestamp) ||
                other.timestamp == timestamp) &&
            (identical(other.activityType, activityType) ||
                other.activityType == activityType) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.feature, feature) || other.feature == feature) &&
            (identical(other.result, result) || other.result == result));
  }

  @override
  int get hashCode => Object.hash(
    runtimeType,
    timestamp,
    activityType,
    description,
    feature,
    result,
  );

  /// Create a copy of AIActivity
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$AIActivityImplCopyWith<_$AIActivityImpl> get copyWith =>
      __$$AIActivityImplCopyWithImpl<_$AIActivityImpl>(this, _$identity);
}

abstract class _AIActivity implements AIActivity {
  const factory _AIActivity({
    required final DateTime timestamp,
    @JsonKey(name: 'activity_type') required final String activityType,
    required final String description,
    final String? feature,
    final String? result,
  }) = _$AIActivityImpl;

  @override
  DateTime get timestamp;
  @override
  @JsonKey(name: 'activity_type')
  String get activityType;
  @override
  String get description;
  @override
  String? get feature;
  @override
  String? get result;

  /// Create a copy of AIActivity
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$AIActivityImplCopyWith<_$AIActivityImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
mixin _$AIUsageStats {
  @JsonKey(name: 'total_queries')
  int get totalQueries => throw _privateConstructorUsedError;
  @JsonKey(name: 'this_month')
  int get thisMonth => throw _privateConstructorUsedError;
  @JsonKey(name: 'this_week')
  int get thisWeek => throw _privateConstructorUsedError;
  @JsonKey(name: 'today')
  int get today => throw _privateConstructorUsedError;
  @JsonKey(name: 'most_used_feature')
  String get mostUsedFeature => throw _privateConstructorUsedError;
  @JsonKey(name: 'avg_response_time')
  double get avgResponseTime => throw _privateConstructorUsedError;

  /// Create a copy of AIUsageStats
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $AIUsageStatsCopyWith<AIUsageStats> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AIUsageStatsCopyWith<$Res> {
  factory $AIUsageStatsCopyWith(
    AIUsageStats value,
    $Res Function(AIUsageStats) then,
  ) = _$AIUsageStatsCopyWithImpl<$Res, AIUsageStats>;
  @useResult
  $Res call({
    @JsonKey(name: 'total_queries') int totalQueries,
    @JsonKey(name: 'this_month') int thisMonth,
    @JsonKey(name: 'this_week') int thisWeek,
    @JsonKey(name: 'today') int today,
    @JsonKey(name: 'most_used_feature') String mostUsedFeature,
    @JsonKey(name: 'avg_response_time') double avgResponseTime,
  });
}

/// @nodoc
class _$AIUsageStatsCopyWithImpl<$Res, $Val extends AIUsageStats>
    implements $AIUsageStatsCopyWith<$Res> {
  _$AIUsageStatsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of AIUsageStats
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? totalQueries = null,
    Object? thisMonth = null,
    Object? thisWeek = null,
    Object? today = null,
    Object? mostUsedFeature = null,
    Object? avgResponseTime = null,
  }) {
    return _then(
      _value.copyWith(
            totalQueries: null == totalQueries
                ? _value.totalQueries
                : totalQueries // ignore: cast_nullable_to_non_nullable
                      as int,
            thisMonth: null == thisMonth
                ? _value.thisMonth
                : thisMonth // ignore: cast_nullable_to_non_nullable
                      as int,
            thisWeek: null == thisWeek
                ? _value.thisWeek
                : thisWeek // ignore: cast_nullable_to_non_nullable
                      as int,
            today: null == today
                ? _value.today
                : today // ignore: cast_nullable_to_non_nullable
                      as int,
            mostUsedFeature: null == mostUsedFeature
                ? _value.mostUsedFeature
                : mostUsedFeature // ignore: cast_nullable_to_non_nullable
                      as String,
            avgResponseTime: null == avgResponseTime
                ? _value.avgResponseTime
                : avgResponseTime // ignore: cast_nullable_to_non_nullable
                      as double,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$AIUsageStatsImplCopyWith<$Res>
    implements $AIUsageStatsCopyWith<$Res> {
  factory _$$AIUsageStatsImplCopyWith(
    _$AIUsageStatsImpl value,
    $Res Function(_$AIUsageStatsImpl) then,
  ) = __$$AIUsageStatsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    @JsonKey(name: 'total_queries') int totalQueries,
    @JsonKey(name: 'this_month') int thisMonth,
    @JsonKey(name: 'this_week') int thisWeek,
    @JsonKey(name: 'today') int today,
    @JsonKey(name: 'most_used_feature') String mostUsedFeature,
    @JsonKey(name: 'avg_response_time') double avgResponseTime,
  });
}

/// @nodoc
class __$$AIUsageStatsImplCopyWithImpl<$Res>
    extends _$AIUsageStatsCopyWithImpl<$Res, _$AIUsageStatsImpl>
    implements _$$AIUsageStatsImplCopyWith<$Res> {
  __$$AIUsageStatsImplCopyWithImpl(
    _$AIUsageStatsImpl _value,
    $Res Function(_$AIUsageStatsImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of AIUsageStats
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? totalQueries = null,
    Object? thisMonth = null,
    Object? thisWeek = null,
    Object? today = null,
    Object? mostUsedFeature = null,
    Object? avgResponseTime = null,
  }) {
    return _then(
      _$AIUsageStatsImpl(
        totalQueries: null == totalQueries
            ? _value.totalQueries
            : totalQueries // ignore: cast_nullable_to_non_nullable
                  as int,
        thisMonth: null == thisMonth
            ? _value.thisMonth
            : thisMonth // ignore: cast_nullable_to_non_nullable
                  as int,
        thisWeek: null == thisWeek
            ? _value.thisWeek
            : thisWeek // ignore: cast_nullable_to_non_nullable
                  as int,
        today: null == today
            ? _value.today
            : today // ignore: cast_nullable_to_non_nullable
                  as int,
        mostUsedFeature: null == mostUsedFeature
            ? _value.mostUsedFeature
            : mostUsedFeature // ignore: cast_nullable_to_non_nullable
                  as String,
        avgResponseTime: null == avgResponseTime
            ? _value.avgResponseTime
            : avgResponseTime // ignore: cast_nullable_to_non_nullable
                  as double,
      ),
    );
  }
}

/// @nodoc

class _$AIUsageStatsImpl implements _AIUsageStats {
  const _$AIUsageStatsImpl({
    @JsonKey(name: 'total_queries') required this.totalQueries,
    @JsonKey(name: 'this_month') required this.thisMonth,
    @JsonKey(name: 'this_week') required this.thisWeek,
    @JsonKey(name: 'today') required this.today,
    @JsonKey(name: 'most_used_feature') required this.mostUsedFeature,
    @JsonKey(name: 'avg_response_time') required this.avgResponseTime,
  });

  @override
  @JsonKey(name: 'total_queries')
  final int totalQueries;
  @override
  @JsonKey(name: 'this_month')
  final int thisMonth;
  @override
  @JsonKey(name: 'this_week')
  final int thisWeek;
  @override
  @JsonKey(name: 'today')
  final int today;
  @override
  @JsonKey(name: 'most_used_feature')
  final String mostUsedFeature;
  @override
  @JsonKey(name: 'avg_response_time')
  final double avgResponseTime;

  @override
  String toString() {
    return 'AIUsageStats(totalQueries: $totalQueries, thisMonth: $thisMonth, thisWeek: $thisWeek, today: $today, mostUsedFeature: $mostUsedFeature, avgResponseTime: $avgResponseTime)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AIUsageStatsImpl &&
            (identical(other.totalQueries, totalQueries) ||
                other.totalQueries == totalQueries) &&
            (identical(other.thisMonth, thisMonth) ||
                other.thisMonth == thisMonth) &&
            (identical(other.thisWeek, thisWeek) ||
                other.thisWeek == thisWeek) &&
            (identical(other.today, today) || other.today == today) &&
            (identical(other.mostUsedFeature, mostUsedFeature) ||
                other.mostUsedFeature == mostUsedFeature) &&
            (identical(other.avgResponseTime, avgResponseTime) ||
                other.avgResponseTime == avgResponseTime));
  }

  @override
  int get hashCode => Object.hash(
    runtimeType,
    totalQueries,
    thisMonth,
    thisWeek,
    today,
    mostUsedFeature,
    avgResponseTime,
  );

  /// Create a copy of AIUsageStats
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$AIUsageStatsImplCopyWith<_$AIUsageStatsImpl> get copyWith =>
      __$$AIUsageStatsImplCopyWithImpl<_$AIUsageStatsImpl>(this, _$identity);
}

abstract class _AIUsageStats implements AIUsageStats {
  const factory _AIUsageStats({
    @JsonKey(name: 'total_queries') required final int totalQueries,
    @JsonKey(name: 'this_month') required final int thisMonth,
    @JsonKey(name: 'this_week') required final int thisWeek,
    @JsonKey(name: 'today') required final int today,
    @JsonKey(name: 'most_used_feature') required final String mostUsedFeature,
    @JsonKey(name: 'avg_response_time') required final double avgResponseTime,
  }) = _$AIUsageStatsImpl;

  @override
  @JsonKey(name: 'total_queries')
  int get totalQueries;
  @override
  @JsonKey(name: 'this_month')
  int get thisMonth;
  @override
  @JsonKey(name: 'this_week')
  int get thisWeek;
  @override
  @JsonKey(name: 'today')
  int get today;
  @override
  @JsonKey(name: 'most_used_feature')
  String get mostUsedFeature;
  @override
  @JsonKey(name: 'avg_response_time')
  double get avgResponseTime;

  /// Create a copy of AIUsageStats
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$AIUsageStatsImplCopyWith<_$AIUsageStatsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
mixin _$AIFeatureStats {
  @JsonKey(name: 'chat_advisor')
  int get chatAdvisor => throw _privateConstructorUsedError;
  @JsonKey(name: 'yield_prediction')
  int get yieldPrediction => throw _privateConstructorUsedError;
  @JsonKey(name: 'plant_health')
  int get plantHealth => throw _privateConstructorUsedError;
  @JsonKey(name: 'environmental_insights')
  int get environmentalInsights => throw _privateConstructorUsedError;
  @JsonKey(name: 'grow_guidance')
  int get growGuidance => throw _privateConstructorUsedError;

  /// Create a copy of AIFeatureStats
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $AIFeatureStatsCopyWith<AIFeatureStats> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AIFeatureStatsCopyWith<$Res> {
  factory $AIFeatureStatsCopyWith(
    AIFeatureStats value,
    $Res Function(AIFeatureStats) then,
  ) = _$AIFeatureStatsCopyWithImpl<$Res, AIFeatureStats>;
  @useResult
  $Res call({
    @JsonKey(name: 'chat_advisor') int chatAdvisor,
    @JsonKey(name: 'yield_prediction') int yieldPrediction,
    @JsonKey(name: 'plant_health') int plantHealth,
    @JsonKey(name: 'environmental_insights') int environmentalInsights,
    @JsonKey(name: 'grow_guidance') int growGuidance,
  });
}

/// @nodoc
class _$AIFeatureStatsCopyWithImpl<$Res, $Val extends AIFeatureStats>
    implements $AIFeatureStatsCopyWith<$Res> {
  _$AIFeatureStatsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of AIFeatureStats
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? chatAdvisor = null,
    Object? yieldPrediction = null,
    Object? plantHealth = null,
    Object? environmentalInsights = null,
    Object? growGuidance = null,
  }) {
    return _then(
      _value.copyWith(
            chatAdvisor: null == chatAdvisor
                ? _value.chatAdvisor
                : chatAdvisor // ignore: cast_nullable_to_non_nullable
                      as int,
            yieldPrediction: null == yieldPrediction
                ? _value.yieldPrediction
                : yieldPrediction // ignore: cast_nullable_to_non_nullable
                      as int,
            plantHealth: null == plantHealth
                ? _value.plantHealth
                : plantHealth // ignore: cast_nullable_to_non_nullable
                      as int,
            environmentalInsights: null == environmentalInsights
                ? _value.environmentalInsights
                : environmentalInsights // ignore: cast_nullable_to_non_nullable
                      as int,
            growGuidance: null == growGuidance
                ? _value.growGuidance
                : growGuidance // ignore: cast_nullable_to_non_nullable
                      as int,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$AIFeatureStatsImplCopyWith<$Res>
    implements $AIFeatureStatsCopyWith<$Res> {
  factory _$$AIFeatureStatsImplCopyWith(
    _$AIFeatureStatsImpl value,
    $Res Function(_$AIFeatureStatsImpl) then,
  ) = __$$AIFeatureStatsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    @JsonKey(name: 'chat_advisor') int chatAdvisor,
    @JsonKey(name: 'yield_prediction') int yieldPrediction,
    @JsonKey(name: 'plant_health') int plantHealth,
    @JsonKey(name: 'environmental_insights') int environmentalInsights,
    @JsonKey(name: 'grow_guidance') int growGuidance,
  });
}

/// @nodoc
class __$$AIFeatureStatsImplCopyWithImpl<$Res>
    extends _$AIFeatureStatsCopyWithImpl<$Res, _$AIFeatureStatsImpl>
    implements _$$AIFeatureStatsImplCopyWith<$Res> {
  __$$AIFeatureStatsImplCopyWithImpl(
    _$AIFeatureStatsImpl _value,
    $Res Function(_$AIFeatureStatsImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of AIFeatureStats
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? chatAdvisor = null,
    Object? yieldPrediction = null,
    Object? plantHealth = null,
    Object? environmentalInsights = null,
    Object? growGuidance = null,
  }) {
    return _then(
      _$AIFeatureStatsImpl(
        chatAdvisor: null == chatAdvisor
            ? _value.chatAdvisor
            : chatAdvisor // ignore: cast_nullable_to_non_nullable
                  as int,
        yieldPrediction: null == yieldPrediction
            ? _value.yieldPrediction
            : yieldPrediction // ignore: cast_nullable_to_non_nullable
                  as int,
        plantHealth: null == plantHealth
            ? _value.plantHealth
            : plantHealth // ignore: cast_nullable_to_non_nullable
                  as int,
        environmentalInsights: null == environmentalInsights
            ? _value.environmentalInsights
            : environmentalInsights // ignore: cast_nullable_to_non_nullable
                  as int,
        growGuidance: null == growGuidance
            ? _value.growGuidance
            : growGuidance // ignore: cast_nullable_to_non_nullable
                  as int,
      ),
    );
  }
}

/// @nodoc

class _$AIFeatureStatsImpl implements _AIFeatureStats {
  const _$AIFeatureStatsImpl({
    @JsonKey(name: 'chat_advisor') required this.chatAdvisor,
    @JsonKey(name: 'yield_prediction') required this.yieldPrediction,
    @JsonKey(name: 'plant_health') required this.plantHealth,
    @JsonKey(name: 'environmental_insights')
    required this.environmentalInsights,
    @JsonKey(name: 'grow_guidance') required this.growGuidance,
  });

  @override
  @JsonKey(name: 'chat_advisor')
  final int chatAdvisor;
  @override
  @JsonKey(name: 'yield_prediction')
  final int yieldPrediction;
  @override
  @JsonKey(name: 'plant_health')
  final int plantHealth;
  @override
  @JsonKey(name: 'environmental_insights')
  final int environmentalInsights;
  @override
  @JsonKey(name: 'grow_guidance')
  final int growGuidance;

  @override
  String toString() {
    return 'AIFeatureStats(chatAdvisor: $chatAdvisor, yieldPrediction: $yieldPrediction, plantHealth: $plantHealth, environmentalInsights: $environmentalInsights, growGuidance: $growGuidance)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AIFeatureStatsImpl &&
            (identical(other.chatAdvisor, chatAdvisor) ||
                other.chatAdvisor == chatAdvisor) &&
            (identical(other.yieldPrediction, yieldPrediction) ||
                other.yieldPrediction == yieldPrediction) &&
            (identical(other.plantHealth, plantHealth) ||
                other.plantHealth == plantHealth) &&
            (identical(other.environmentalInsights, environmentalInsights) ||
                other.environmentalInsights == environmentalInsights) &&
            (identical(other.growGuidance, growGuidance) ||
                other.growGuidance == growGuidance));
  }

  @override
  int get hashCode => Object.hash(
    runtimeType,
    chatAdvisor,
    yieldPrediction,
    plantHealth,
    environmentalInsights,
    growGuidance,
  );

  /// Create a copy of AIFeatureStats
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$AIFeatureStatsImplCopyWith<_$AIFeatureStatsImpl> get copyWith =>
      __$$AIFeatureStatsImplCopyWithImpl<_$AIFeatureStatsImpl>(
        this,
        _$identity,
      );
}

abstract class _AIFeatureStats implements AIFeatureStats {
  const factory _AIFeatureStats({
    @JsonKey(name: 'chat_advisor') required final int chatAdvisor,
    @JsonKey(name: 'yield_prediction') required final int yieldPrediction,
    @JsonKey(name: 'plant_health') required final int plantHealth,
    @JsonKey(name: 'environmental_insights')
    required final int environmentalInsights,
    @JsonKey(name: 'grow_guidance') required final int growGuidance,
  }) = _$AIFeatureStatsImpl;

  @override
  @JsonKey(name: 'chat_advisor')
  int get chatAdvisor;
  @override
  @JsonKey(name: 'yield_prediction')
  int get yieldPrediction;
  @override
  @JsonKey(name: 'plant_health')
  int get plantHealth;
  @override
  @JsonKey(name: 'environmental_insights')
  int get environmentalInsights;
  @override
  @JsonKey(name: 'grow_guidance')
  int get growGuidance;

  /// Create a copy of AIFeatureStats
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$AIFeatureStatsImplCopyWith<_$AIFeatureStatsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
mixin _$AIDashboardStats {
  AIUsageStats get usage => throw _privateConstructorUsedError;
  AIFeatureStats get features => throw _privateConstructorUsedError;
  @JsonKey(name: 'recent_activities')
  List<AIActivity> get recentActivities => throw _privateConstructorUsedError;
  @JsonKey(name: 'generated_at')
  DateTime get generatedAt => throw _privateConstructorUsedError;
  @JsonKey(name: 'user_id')
  int get userId => throw _privateConstructorUsedError;

  /// Create a copy of AIDashboardStats
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $AIDashboardStatsCopyWith<AIDashboardStats> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AIDashboardStatsCopyWith<$Res> {
  factory $AIDashboardStatsCopyWith(
    AIDashboardStats value,
    $Res Function(AIDashboardStats) then,
  ) = _$AIDashboardStatsCopyWithImpl<$Res, AIDashboardStats>;
  @useResult
  $Res call({
    AIUsageStats usage,
    AIFeatureStats features,
    @JsonKey(name: 'recent_activities') List<AIActivity> recentActivities,
    @JsonKey(name: 'generated_at') DateTime generatedAt,
    @JsonKey(name: 'user_id') int userId,
  });

  $AIUsageStatsCopyWith<$Res> get usage;
  $AIFeatureStatsCopyWith<$Res> get features;
}

/// @nodoc
class _$AIDashboardStatsCopyWithImpl<$Res, $Val extends AIDashboardStats>
    implements $AIDashboardStatsCopyWith<$Res> {
  _$AIDashboardStatsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of AIDashboardStats
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? usage = null,
    Object? features = null,
    Object? recentActivities = null,
    Object? generatedAt = null,
    Object? userId = null,
  }) {
    return _then(
      _value.copyWith(
            usage: null == usage
                ? _value.usage
                : usage // ignore: cast_nullable_to_non_nullable
                      as AIUsageStats,
            features: null == features
                ? _value.features
                : features // ignore: cast_nullable_to_non_nullable
                      as AIFeatureStats,
            recentActivities: null == recentActivities
                ? _value.recentActivities
                : recentActivities // ignore: cast_nullable_to_non_nullable
                      as List<AIActivity>,
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

  /// Create a copy of AIDashboardStats
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $AIUsageStatsCopyWith<$Res> get usage {
    return $AIUsageStatsCopyWith<$Res>(_value.usage, (value) {
      return _then(_value.copyWith(usage: value) as $Val);
    });
  }

  /// Create a copy of AIDashboardStats
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $AIFeatureStatsCopyWith<$Res> get features {
    return $AIFeatureStatsCopyWith<$Res>(_value.features, (value) {
      return _then(_value.copyWith(features: value) as $Val);
    });
  }
}

/// @nodoc
abstract class _$$AIDashboardStatsImplCopyWith<$Res>
    implements $AIDashboardStatsCopyWith<$Res> {
  factory _$$AIDashboardStatsImplCopyWith(
    _$AIDashboardStatsImpl value,
    $Res Function(_$AIDashboardStatsImpl) then,
  ) = __$$AIDashboardStatsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    AIUsageStats usage,
    AIFeatureStats features,
    @JsonKey(name: 'recent_activities') List<AIActivity> recentActivities,
    @JsonKey(name: 'generated_at') DateTime generatedAt,
    @JsonKey(name: 'user_id') int userId,
  });

  @override
  $AIUsageStatsCopyWith<$Res> get usage;
  @override
  $AIFeatureStatsCopyWith<$Res> get features;
}

/// @nodoc
class __$$AIDashboardStatsImplCopyWithImpl<$Res>
    extends _$AIDashboardStatsCopyWithImpl<$Res, _$AIDashboardStatsImpl>
    implements _$$AIDashboardStatsImplCopyWith<$Res> {
  __$$AIDashboardStatsImplCopyWithImpl(
    _$AIDashboardStatsImpl _value,
    $Res Function(_$AIDashboardStatsImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of AIDashboardStats
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? usage = null,
    Object? features = null,
    Object? recentActivities = null,
    Object? generatedAt = null,
    Object? userId = null,
  }) {
    return _then(
      _$AIDashboardStatsImpl(
        usage: null == usage
            ? _value.usage
            : usage // ignore: cast_nullable_to_non_nullable
                  as AIUsageStats,
        features: null == features
            ? _value.features
            : features // ignore: cast_nullable_to_non_nullable
                  as AIFeatureStats,
        recentActivities: null == recentActivities
            ? _value._recentActivities
            : recentActivities // ignore: cast_nullable_to_non_nullable
                  as List<AIActivity>,
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

class _$AIDashboardStatsImpl implements _AIDashboardStats {
  const _$AIDashboardStatsImpl({
    required this.usage,
    required this.features,
    @JsonKey(name: 'recent_activities')
    final List<AIActivity> recentActivities = const [],
    @JsonKey(name: 'generated_at') required this.generatedAt,
    @JsonKey(name: 'user_id') required this.userId,
  }) : _recentActivities = recentActivities;

  @override
  final AIUsageStats usage;
  @override
  final AIFeatureStats features;
  final List<AIActivity> _recentActivities;
  @override
  @JsonKey(name: 'recent_activities')
  List<AIActivity> get recentActivities {
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
    return 'AIDashboardStats(usage: $usage, features: $features, recentActivities: $recentActivities, generatedAt: $generatedAt, userId: $userId)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AIDashboardStatsImpl &&
            (identical(other.usage, usage) || other.usage == usage) &&
            (identical(other.features, features) ||
                other.features == features) &&
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
    usage,
    features,
    const DeepCollectionEquality().hash(_recentActivities),
    generatedAt,
    userId,
  );

  /// Create a copy of AIDashboardStats
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$AIDashboardStatsImplCopyWith<_$AIDashboardStatsImpl> get copyWith =>
      __$$AIDashboardStatsImplCopyWithImpl<_$AIDashboardStatsImpl>(
        this,
        _$identity,
      );
}

abstract class _AIDashboardStats implements AIDashboardStats {
  const factory _AIDashboardStats({
    required final AIUsageStats usage,
    required final AIFeatureStats features,
    @JsonKey(name: 'recent_activities') final List<AIActivity> recentActivities,
    @JsonKey(name: 'generated_at') required final DateTime generatedAt,
    @JsonKey(name: 'user_id') required final int userId,
  }) = _$AIDashboardStatsImpl;

  @override
  AIUsageStats get usage;
  @override
  AIFeatureStats get features;
  @override
  @JsonKey(name: 'recent_activities')
  List<AIActivity> get recentActivities;
  @override
  @JsonKey(name: 'generated_at')
  DateTime get generatedAt;
  @override
  @JsonKey(name: 'user_id')
  int get userId;

  /// Create a copy of AIDashboardStats
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$AIDashboardStatsImplCopyWith<_$AIDashboardStatsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
