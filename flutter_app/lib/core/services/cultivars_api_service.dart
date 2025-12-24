/// Cultivars API Service
/// Provides a clean interface for cultivars CRUD operations
/// Handles API communication and error handling
library;
// (removed stray library directive)

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/cultivar_models.dart';
import 'package:cultivar_app/core/api/api_client.dart';
import '../api/api_exceptions.dart' as api_ex;
import '../logging.dart';

class CultivarsApiService {
  static final CultivarsApiService _instance = CultivarsApiService._internal();
  factory CultivarsApiService() => _instance;
  CultivarsApiService._internal();

  final ApiClient _apiClient = ApiClient();

  static Future<List<Cultivar>> getCultivars() async {
    return _instance.getAllCultivars();
  }

  static Future<CultivarStats> getCultivarStats() async {
    // Mock implementation or fetch from dashboard stats
    // For now, returning mock data to unblock
    await Future.delayed(const Duration(milliseconds: 200));
    return const CultivarStats(
      totalCultivars: 5,
      autoflower: 2,
      photoperiod: 3,
      mostUsedCultivar: 'OG Kush',
      mostUsedCount: 12,
    );
  }

  /// Get all cultivars from the API
  Future<List<Cultivar>> getAllCultivars() async {
    try {
      AppLogger.log('Fetching all cultivars from API');
      return await _apiClient.getCultivars();
    } on api_ex.ApiException catch (e) {
      AppLogger.error('Failed to fetch cultivars', e);
      throw api_ex.ApiException(
        message: 'Failed to fetch cultivars: ${e.message}',
        statusCode: e.statusCode,
        details: e.details,
      );
    }
  }

  /// Get a specific cultivar by ID
  Future<Cultivar> getCultivarById(int id) async {
    try {
      AppLogger.log('Fetching cultivar with ID: $id');
      return await _apiClient.getCultivar(id);
    } on api_ex.ApiException catch (e) {
      AppLogger.error('Failed to fetch cultivar $id', e);
      throw api_ex.ApiException(
        message: 'Failed to fetch cultivar $id: ${e.message}',
        statusCode: e.statusCode,
        details: e.details,
      );
    }
  }

  /// Create a new cultivar
  Future<Cultivar> createCultivar(Map<String, dynamic> cultivarData) async {
    try {
      AppLogger.log('Creating new cultivar: ${cultivarData['name']}');
      return await _apiClient.createCultivar(cultivarData);
    } on api_ex.ApiException catch (e) {
      AppLogger.error('Failed to create cultivar', e);
      throw api_ex.ApiException(
        message: 'Failed to create cultivar: ${e.message}',
        statusCode: e.statusCode,
        details: e.details,
      );
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
    } on api_ex.ApiException catch (e) {
      AppLogger.error('Failed to update cultivar $id', e);
      throw api_ex.ApiException(
        message: 'Failed to update cultivar $id: ${e.message}',
        statusCode: e.statusCode,
        details: e.details,
      );
    }
  }

  /// Delete a cultivar
  Future<void> deleteCultivar(int id) async {
    try {
      AppLogger.log('Deleting cultivar with ID: $id');
      await _apiClient.deleteCultivar(id);
    } on api_ex.ApiException catch (e) {
      AppLogger.error('Failed to delete cultivar $id', e);
      throw api_ex.ApiException(
        message: 'Failed to delete cultivar $id: ${e.message}',
        statusCode: e.statusCode,
        details: e.details,
      );
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
