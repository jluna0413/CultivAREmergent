import 'package:flutter/foundation.dart';
import '../api/api_client.dart';
import '../api/api_exceptions.dart' as api_ex;

/// API service for Emerald Plant Tracker integration operations
class EmeraldIntegrationService {
  const EmeraldIntegrationService(this._apiClient);
  final ApiClient _apiClient;

  /// Check Emerald integration status
  Future<Map<String, dynamic>> getStatus() async {
    try {
      final responseData = await _apiClient.get<Map<String, dynamic>>(
        '/api/v2/integrations/emerald/status',
      );
      return responseData;
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to fetch Emerald status: ${e.message}');
      rethrow;
    }
  }

  /// Get all plants from Emerald
  Future<List<Map<String, dynamic>>> getPlants() async {
    try {
      final responseData = await _apiClient.get<List<dynamic>>(
        '/api/v2/integrations/emerald/plants',
      );
      return responseData.cast<Map<String, dynamic>>();
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to fetch Emerald plants: ${e.message}');
      rethrow;
    }
  }

  /// Get specific plant from Emerald
  Future<Map<String, dynamic>> getPlant(int plantId) async {
    try {
      final responseData = await _apiClient.get<Map<String, dynamic>>(
        '/api/v2/integrations/emerald/plants/$plantId',
      );
      return responseData;
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to fetch Emerald plant $plantId: ${e.message}');
      rethrow;
    }
  }

  /// Get environment logs from Emerald
  Future<List<Map<String, dynamic>>> getEnvironmentLogs({int? tentId}) async {
    try {
      final queryParams = tentId != null ? '?tent_id=$tentId' : '';
      final responseData = await _apiClient.get<List<dynamic>>(
        '/api/v2/integrations/emerald/environment$queryParams',
      );
      return responseData.cast<Map<String, dynamic>>();
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to fetch Emerald environment logs: ${e.message}');
      rethrow;
    }
  }

  /// Get weekly environment averages from Emerald
  Future<Map<String, dynamic>> getWeeklyAverages() async {
    try {
      final responseData = await _apiClient.get<Map<String, dynamic>>(
        '/api/v2/integrations/emerald/environment/weekly',
      );
      return responseData;
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to fetch Emerald weekly averages: ${e.message}');
      rethrow;
    }
  }

  /// Get activity logs from Emerald
  Future<List<Map<String, dynamic>>> getActivityLogs({int? plantId}) async {
    try {
      final queryParams = plantId != null ? '?plant_id=$plantId' : '';
      final responseData = await _apiClient.get<List<dynamic>>(
        '/api/v2/integrations/emerald/logs$queryParams',
      );
      return responseData.cast<Map<String, dynamic>>();
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to fetch Emerald activity logs: ${e.message}');
      rethrow;
    }
  }

  /// Get plant statistics from Emerald
  Future<Map<String, dynamic>> getPlantStats(int plantId) async {
    try {
      final responseData = await _apiClient.get<Map<String, dynamic>>(
        '/api/v2/integrations/emerald/plants/$plantId/stats',
      );
      return responseData;
    } on api_ex.ApiException catch (e) {
      debugPrint(
        'Failed to fetch stats for Emerald plant $plantId: ${e.message}',
      );
      rethrow;
    }
  }

  /// Get tents from Emerald
  Future<List<Map<String, dynamic>>> getTents() async {
    try {
      final responseData = await _apiClient.get<List<dynamic>>(
        '/api/v2/integrations/emerald/tents',
      );
      return responseData.cast<Map<String, dynamic>>();
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to fetch Emerald tents: ${e.message}');
      rethrow;
    }
  }
}
