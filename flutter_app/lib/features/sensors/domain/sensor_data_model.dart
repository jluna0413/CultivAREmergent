import 'package:freezed_annotation/freezed_annotation.dart';

part 'sensor_data_model.freezed.dart';
part 'sensor_data_model.g.dart';

@freezed
abstract class SensorData with _$SensorData {
  const factory SensorData({
    required String id,
    required double value,
    required DateTime timestamp,
  }) = _SensorData;

  factory SensorData.fromJson(Map<String, dynamic> json) =>
      _$SensorDataFromJson(json);
}
