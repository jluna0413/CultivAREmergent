import 'package:flutter/foundation.dart';
import '../api/api_client.dart';
import '../api/api_exceptions.dart' as api_ex;

/// API service for AC Infinity device operations
class ACInfinityApiService {
  const ACInfinityApiService(this._apiClient);
  final ApiClient _apiClient;

  /// Get all AC Infinity devices
  Future<List<Map<String, dynamic>>> getDevices() async {
    try {
      final responseData = await _apiClient.get<Map<String, dynamic>>(
        '/api/v2/devices/acinfinity/list',
      );

      // Extract devices list from response
      final devices = responseData['devices'] as List?;
      if (devices == null) return [];

      return devices.cast<Map<String, dynamic>>();
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to fetch AC Infinity devices: ${e.message}');
      rethrow;
    }
  }

  /// Get a single AC Infinity device by ID
  Future<Map<String, dynamic>> getDevice(int id) async {
    try {
      final responseData = await _apiClient.get<Map<String, dynamic>>(
        '/api/v2/devices/acinfinity/$id',
      );
      return responseData;
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to fetch AC Infinity device $id: ${e.message}');
      rethrow;
    }
  }

  /// Create/register a new AC Infinity device
  Future<Map<String, dynamic>> createDevice(Map<String, dynamic> data) async {
    try {
      final responseData = await _apiClient.post<Map<String, dynamic>>(
        '/api/v2/devices/acinfinity/',
        data: data,
      );
      return responseData;
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to create AC Infinity device: ${e.message}');
      rethrow;
    }
  }

  /// Update device heartbeat
  Future<Map<String, dynamic>> updateHeartbeat(int deviceId) async {
    try {
      final responseData = await _apiClient.post<Map<String, dynamic>>(
        '/api/v2/devices/acinfinity/$deviceId/heartbeat',
        data: {},
      );
      return responseData;
    } on api_ex.ApiException catch (e) {
      debugPrint(
        'Failed to update heartbeat for device $deviceId: ${e.message}',
      );
      rethrow;
    }
  }
}
