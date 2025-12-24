import 'package:flutter/foundation.dart';
import '../api/api_client.dart';
import '../api/api_exceptions.dart' as api_ex;

/// API service for sensor-related operations
class SensorsApiService {
  const SensorsApiService(this._apiClient);
  final ApiClient _apiClient;

  /// Get all sensors
  Future<List<Map<String, dynamic>>> getSensors() async {
    try {
      final responseData = await _apiClient.get<List<Map<String, dynamic>>>(
        '/sensors',
      );
      return responseData;
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to fetch sensors: ${e.message}');
      rethrow;
    }
  }

  /// Get a single sensor by ID
  Future<Map<String, dynamic>> getSensor(int id) async {
    try {
      final responseData = await _apiClient.get<Map<String, dynamic>>(
        '/sensors/$id',
      );
      return responseData;
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to fetch sensor $id: ${e.message}');
      rethrow;
    }
  }

  /// Create a new sensor
  Future<Map<String, dynamic>> createSensor(Map<String, dynamic> data) async {
    try {
      final responseData = await _apiClient.post<Map<String, dynamic>>(
        '/sensors',
        data: data,
      );
      return responseData;
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to create sensor: ${e.message}');
      rethrow;
    }
  }

  /// Update an existing sensor
  Future<Map<String, dynamic>> updateSensor(
    int id,
    Map<String, dynamic> data,
  ) async {
    try {
      final responseData = await _apiClient.put<Map<String, dynamic>>(
        '/sensors/$id',
        data: data,
      );
      return responseData;
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to update sensor $id: ${e.message}');
      rethrow;
    }
  }

  /// Delete a sensor
  Future<void> deleteSensor(int id) async {
    try {
      await _apiClient.delete<Map<String, dynamic>>('/sensors/$id');
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to delete sensor $id: ${e.message}');
      rethrow;
    }
  }

  /// Get sensor readings for a specific sensor
  Future<List<Map<String, dynamic>>> getSensorReadings(int sensorId) async {
    try {
      final responseData = await _apiClient.get<List<Map<String, dynamic>>>(
        '/sensors/$sensorId/readings',
      );
      return responseData;
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to fetch readings for sensor $sensorId: ${e.message}');
      rethrow;
    }
  }

  /// Record a new sensor reading
  Future<Map<String, dynamic>> recordReading(
    int sensorId,
    Map<String, dynamic> data,
  ) async {
    try {
      final responseData = await _apiClient.post<Map<String, dynamic>>(
        '/sensors/$sensorId/readings',
        data: data,
      );
      return responseData;
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to record reading for sensor $sensorId: ${e.message}');
      rethrow;
    }
  }
}
