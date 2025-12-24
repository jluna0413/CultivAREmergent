/// Sensors API Service
/// Provides a clean interface for sensors CRUD operations
/// Handles API communication and error handling
library;

import '../../core/providers/riverpod_exports.dart';

import '../models/sensor_models.dart';
import 'api_client.dart';
import '../logging.dart';

class SensorsApiService {
  final ApiClient _apiClient = ApiClient();

  /// Get all sensors from the API
  Future<List<Sensor>> getAllSensors() async {
    try {
      AppLogger.log('Fetching all sensors from API');
      return await _apiClient.getAllSensors(); // Fixed method name
    } on ApiException catch (e) {
      AppLogger.error('Failed to fetch sensors', e);
      throw ApiException('Failed to fetch sensors: ${e.message}');
    }
  }

  /// Get a specific sensor by ID
  Future<Sensor> getSensorById(int id) async {
    try {
      AppLogger.log('Fetching sensor with ID: $id');
      return await _apiClient.getSensorById(id); // Fixed method name
    } on ApiException catch (e) {
      AppLogger.error('Failed to fetch sensor $id', e);
      throw ApiException('Failed to fetch sensor $id: ${e.message}');
    }
  }

  /// Create a new sensor
  Future<Sensor> createSensor(Map<String, dynamic> sensorData) async {
    try {
      AppLogger.log('Creating new sensor: ${sensorData['name']}');
      return await _apiClient.createSensor(sensorData);
    } on ApiException catch (e) {
      AppLogger.error('Failed to create sensor', e);
      throw ApiException('Failed to create sensor: ${e.message}');
    }
  }

  /// Update an existing sensor
  Future<Sensor> updateSensor(int id, Map<String, dynamic> sensorData) async {
    try {
      AppLogger.log('Updating sensor with ID: $id');
      return await _apiClient.updateSensor(id, sensorData);
    } on ApiException catch (e) {
      AppLogger.error('Failed to update sensor $id', e);
      throw ApiException('Failed to update sensor $id: ${e.message}');
    }
  }

  /// Delete a sensor
  Future<void> deleteSensor(int id) async {
    try {
      AppLogger.log('Deleting sensor with ID: $id');
      await _apiClient.deleteSensor(id);
    } on ApiException catch (e) {
      AppLogger.error('Failed to delete sensor $id', e);
      throw ApiException('Failed to delete sensor $id: ${e.message}');
    }
  }

  /// Get sensor data history for a specific sensor
  Future<List<SensorReading>> getSensorHistory(
    int sensorId, {
    DateTime? startDate,
    DateTime? endDate,
  }) async {
    try {
      AppLogger.log('Fetching sensor history for sensor: $sensorId');
      // This would typically be a separate endpoint in the API
      // For now, we'll implement a placeholder
      return []; // TODO: Implement actual sensor history endpoint
    } on ApiException catch (e) {
      AppLogger.error('Failed to fetch sensor history', e);
      throw ApiException('Failed to fetch sensor history: ${e.message}');
    }
  }

  /// Real-time sensor data subscription (WebSocket/SSE simulation)
  Stream<SensorReading> subscribeToSensorData(int sensorId) {
    AppLogger.log('Starting real-time data subscription for sensor: $sensorId');

    // This would typically connect to WebSocket or Server-Sent Events
    // For now, we'll implement a placeholder stream
    return const Stream.empty(); // TODO: Implement actual real-time connection
  }

  /// Convert provider sensor data to API format
  Map<String, dynamic> providerSensorToApiFormat(dynamic providerSensor) {
    if (providerSensor is Map<String, dynamic>) {
      return {
        'name': providerSensor['name'] as String?,
        'type': providerSensor['type'] as String?,
        'location': providerSensor['location'] as String?,
        'min_value': providerSensor['minThreshold'] as double?,
        'max_value': providerSensor['maxThreshold'] as double?,
        'unit': providerSensor['unit'] as String?,
        'is_active': providerSensor['isActive'] as bool? ?? true,
      };
    }

    // Handle object-based sensor data
    return {
      'name': providerSensor.name,
      'type': providerSensor.type,
      'location': providerSensor.location,
      'min_value': providerSensor.minValue,
      'max_value': providerSensor.maxValue,
      'unit': providerSensor.unit,
      'is_active': providerSensor.isActive,
    };
  }

  /// Convert API sensor to provider-compatible format
  Map<String, dynamic> apiSensorToProviderFormat(Sensor apiSensor) {
    return {
      'id': apiSensor.id.toString(),
      'name': apiSensor.name,
      'type': apiSensor.type,
      'location': apiSensor.location,
      'minThreshold': apiSensor.minThreshold,
      'maxThreshold': apiSensor.maxThreshold,
      'unit': apiSensor.unit,
      'isActive': apiSensor.isActive,
      'lastReading': apiSensor.lastReading,
      'status': apiSensor.status.name,
    };
  }

  /// Map sensor status to provider format
  String _mapSensorStatusToProvider(SensorStatus sensorStatus) {
    switch (sensorStatus) {
      case SensorStatus.online:
        return 'online';
      case SensorStatus.offline:
        return 'offline';
      case SensorStatus.error:
        return 'error';
      case SensorStatus.maintenance:
        return 'maintenance';
      case SensorStatus.calibrating:
        return 'calibrating';
    }
  }

  /// Get sensor alert thresholds
  Future<Map<String, double>> getSensorThresholds(int sensorId) async {
    try {
      AppLogger.log('Fetching sensor thresholds for sensor: $sensorId');
      // This would typically be a separate endpoint
      // For now, return default thresholds
      return {
        'min': 0.0,
        'max': 100.0,
      }; // TODO: Implement actual thresholds endpoint
    } on ApiException catch (e) {
      AppLogger.error('Failed to fetch sensor thresholds', e);
      throw ApiException('Failed to fetch sensor thresholds: ${e.message}');
    }
  }

  /// Set sensor alert thresholds
  Future<void> setSensorThresholds(
    int sensorId,
    Map<String, double> thresholds,
  ) async {
    try {
      AppLogger.log('Setting sensor thresholds for sensor: $sensorId');
      // This would typically be a separate endpoint
      // For now, this is a placeholder
      return; // TODO: Implement actual thresholds endpoint
    } on ApiException catch (e) {
      AppLogger.error('Failed to set sensor thresholds', e);
      throw ApiException('Failed to set sensor thresholds: ${e.message}');
    }
  }
}

/// Provider for SensorsApiService
final sensorsApiServiceProvider = Provider<SensorsApiService>((ref) {
  return SensorsApiService();
});
