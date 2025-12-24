import 'package:flutter/foundation.dart';
import '../api/api_client.dart';
import '../api/api_exceptions.dart' as api_ex;
import '../../../features/plants/domain/plant_model.dart';

/// API service for plant-related operations
class PlantsApiService {
  const PlantsApiService(this._apiClient);
  final ApiClient _apiClient;

  /// Get paginated list of plants
  Future<PaginatedPlantsResponse> getPlants({PlantsParams? params}) async {
    try {
      final responseData = await _apiClient.get<Map<String, dynamic>>(
        '/plants',
        queryParameters: params?.toQueryParameters(),
      );
      return PaginatedPlantsResponse.fromJson(responseData);
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to fetch plants: ${e.message}');
      rethrow;
    }
  }

  /// Get a single plant by ID
  Future<Plant> getPlant(int id) async {
    try {
      final responseData = await _apiClient.get<Map<String, dynamic>>(
        '/plants/$id',
      );
      return Plant.fromJson(responseData);
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to fetch plant $id: ${e.message}');
      rethrow;
    }
  }

  /// Create a new plant
  Future<Plant> createPlant(PlantCreate request) async {
    try {
      final responseData = await _apiClient.post<Map<String, dynamic>>(
        '/plants',
        data: request.toJson(),
      );
      return Plant.fromJson(responseData);
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to create plant: ${e.message}');
      rethrow;
    }
  }

  /// Update an existing plant
  Future<Plant> updatePlant(int id, PlantUpdate request) async {
    try {
      final responseData = await _apiClient.put<Map<String, dynamic>>(
        '/plants/$id',
        data: request.toJson(),
      );
      return Plant.fromJson(responseData);
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to update plant $id: ${e.message}');
      rethrow;
    }
  }

  /// Delete a plant
  Future<void> deletePlant(int id) async {
    try {
      await _apiClient.delete<Map<String, dynamic>>('/plants/$id');
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to delete plant $id: ${e.message}');
      rethrow;
    }
  }
}
