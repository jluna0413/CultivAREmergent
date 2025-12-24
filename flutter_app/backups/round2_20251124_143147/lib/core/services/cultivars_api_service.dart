/// Cultivars API Service
/// Provides a clean interface for cultivars CRUD operations
/// Handles API communication and error handling
library;
// (removed stray library directive)

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/cultivar_models.dart';
import 'api_client.dart';
import '../logging.dart';

class CultivarsApiService {
  final ApiClient _apiClient = ApiClient();

  /// Get all cultivars from the API
  Future<List<Cultivar>> getAllCultivars() async {
    try {
      AppLogger.log('Fetching all cultivars from API');
      return await _apiClient.getCultivars();
    } on ApiException catch (e) {
      AppLogger.error('Failed to fetch cultivars', e);
      throw ApiException('Failed to fetch cultivars: ${e.message}');
    }
  }

  /// Get a specific cultivar by ID
  Future<Cultivar> getCultivarById(int id) async {
    try {
      AppLogger.log('Fetching cultivar with ID: $id');
      return await _apiClient.getCultivar(id);
    } on ApiException catch (e) {
      AppLogger.error('Failed to fetch cultivar $id', e);
      throw ApiException('Failed to fetch cultivar $id: ${e.message}');
    }
  }

  /// Create a new cultivar
  Future<Cultivar> createCultivar(Map<String, dynamic> cultivarData) async {
    try {
      AppLogger.log('Creating new cultivar: ${cultivarData['name']}');
      return await _apiClient.createCultivar(cultivarData);
    } on ApiException catch (e) {
      AppLogger.error('Failed to create cultivar', e);
      throw ApiException('Failed to create cultivar: ${e.message}');
    }
  }

  /// Update an existing cultivar
  Future<Cultivar> updateCultivar(
    int id,
    Map<String, dynamic> cultivarData,
  ) async {
    try {
      AppLogger.log('Updating cultivar with ID: $id');
      return await _apiClient.updateCultivar(id, cultivarData);
    } on ApiException catch (e) {
      AppLogger.error('Failed to update cultivar $id', e);
      throw ApiException('Failed to update cultivar $id: ${e.message}');
    }
  }

  /// Delete a cultivar
  Future<void> deleteCultivar(int id) async {
    try {
      AppLogger.log('Deleting cultivar with ID: $id');
      await _apiClient.deleteCultivar(id);
    } on ApiException catch (e) {
      AppLogger.error('Failed to delete cultivar $id', e);
      throw ApiException('Failed to delete cultivar $id: ${e.message}');
    }
  }

  /// Convert provider cultivar data to API format
  Map<String, dynamic> providerCultivarToApiFormat(dynamic providerCultivar) {
    if (providerCultivar is Map<String, dynamic>) {
      return {
        'name': providerCultivar['name'] as String?,
        'description': providerCultivar['description'] as String?,
        'genetics': providerCultivar['genetics'] as String? ?? '',
        'thc_content': providerCultivar['thcContent'] as double? ?? 0.0,
        'cbd_content': providerCultivar['cbdContent'] as double? ?? 0.0,
        'effects': providerCultivar['effects'] as String?,
        'flavor': providerCultivar['flavor'] as String?,
        'breeder_id': providerCultivar['breederId'] as int?,
      };
    }

    // Handle object-based cultivar data
    return {
      'name': providerCultivar.name,
      'description': providerCultivar.description,
      'genetics': providerCultivar.genetics,
      'thc_content': providerCultivar.thcContent,
      'cbd_content': providerCultivar.cbdContent,
      'effects': providerCultivar.effects,
      'flavor': providerCultivar.flavor,
      'breeder_id': providerCultivar.breederId,
    };
  }

  /// Convert API cultivar to provider-compatible format
  Map<String, dynamic> apiCultivarToProviderFormat(Cultivar apiCultivar) {
    return {
      'id': apiCultivar.id.toString(),
      'name': apiCultivar.name,
      'description': apiCultivar.description,
      'genetics': apiCultivar.genetics,
      'thcContent': apiCultivar.thcContent,
      'cbdContent': apiCultivar.cbdContent,
      'effects': apiCultivar.effects,
      'flavor': apiCultivar.flavor,
      'breederId': apiCultivar.breederId,
    };
  }
}

/// Provider for CultivarsApiService
final cultivarsApiServiceProvider = Provider<CultivarsApiService>((ref) {
  return CultivarsApiService();
});
