// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'sensor_data_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$SensorDataImpl _$$SensorDataImplFromJson(Map<String, dynamic> json) =>
    _$SensorDataImpl(
      id: json['id'] as String,
      value: (json['value'] as num).toDouble(),
      timestamp: DateTime.parse(json['timestamp'] as String),
    );

Map<String, dynamic> _$$SensorDataImplToJson(_$SensorDataImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'value': instance.value,
      'timestamp': instance.timestamp.toIso8601String(),
    };
