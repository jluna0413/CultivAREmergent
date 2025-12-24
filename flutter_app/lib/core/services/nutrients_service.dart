import 'package:flutter/foundation.dart';
import '../../core/api/api_client.dart';
import '../../core/api/api_exceptions.dart' as api_ex;

/// Nutrient brand model
class NutrientBrand {
  final int id;
  final String name;
  final String? manufacturer;
  final String brandType;
  final int componentCount;
  final String? description;

  NutrientBrand({
    required this.id,
    required this.name,
    this.manufacturer,
    required this.brandType,
    required this.componentCount,
    this.description,
  });

  factory NutrientBrand.fromJson(Map<String, dynamic> json) {
    return NutrientBrand(
      id: json['id'] as int,
      name: json['name'] as String,
      manufacturer: json['manufacturer'] as String?,
      brandType: json['brand_type'] as String,
      componentCount: json['component_count'] as int,
      description: json['description'] as String?,
    );
  }
}

/// Nutrient component model
class NutrientComponent {
  final int id;
  final int brandId;
  final String name;
  final String? npkRatio;
  final String? description;

  NutrientComponent({
    required this.id,
    required this.brandId,
    required this.name,
    this.npkRatio,
    this.description,
  });

  factory NutrientComponent.fromJson(Map<String, dynamic> json) {
    return NutrientComponent(
      id: json['id'] as int,
      brandId: json['brand_id'] as int,
      name: json['name'] as String,
      npkRatio: json['npk_ratio'] as String?,
      description: json['description'] as String?,
    );
  }
}

/// Nutrient mix calculation result
class NutrientMix {
  final Map<String, double> components;
  final double totalVolumeLiters;
  final (double, double) ppmTarget;
  final (double, double) ecTarget;
  final (double, double) phTarget;
  final List<String> mixingInstructions;
  final bool requiresCalmag;
  final double? calmagMl;
  final bool inventorySufficient;
  final List<String> insufficientItems;
  final double? estimatedCost;

  NutrientMix({
    required this.components,
    required this.totalVolumeLiters,
    required this.ppmTarget,
    required this.ecTarget,
    required this.phTarget,
    required this.mixingInstructions,
    required this.requiresCalmag,
    this.calmagMl,
    required this.inventorySufficient,
    this.insufficientItems = const [],
    this.estimatedCost,
  });

  factory NutrientMix.fromJson(Map<String, dynamic> json) {
    final ppmList = json['ppm_target'] as List;
    final ecList = json['ec_target'] as List;
    final phList = json['ph_target'] as List;

    return NutrientMix(
      components: Map<String, double>.from(
        (json['components'] as Map).map(
          (k, v) => MapEntry(k.toString(), (v as num).toDouble()),
        ),
      ),
      totalVolumeLiters: (json['total_volume_liters'] as num).toDouble(),
      ppmTarget: (
        (ppmList[0] as num).toDouble(),
        (ppmList[1] as num).toDouble(),
      ),
      ecTarget: ((ecList[0] as num).toDouble(), (ecList[1] as num).toDouble()),
      phTarget: ((phList[0] as num).toDouble(), (phList[1] as num).toDouble()),
      mixingInstructions: List<String>.from(
        json['mixing_instructions'] as List,
      ),
      requiresCalmag: json['requires_calmag'] as bool,
      calmagMl: json['calmag_ml'] != null
          ? (json['calmag_ml'] as num).toDouble()
          : null,
      inventorySufficient: json['inventory_sufficient'] as bool,
      insufficientItems: List<String>.from(
        json['insufficient_items'] as List? ?? [],
      ),
      estimatedCost: json['estimated_cost'] != null
          ? (json['estimated_cost'] as num).toDouble()
          : null,
    );
  }
}

/// Inventory item model
class InventoryItem {
  final int id;
  final int componentId;
  final String componentName;
  final double quantityMl;
  final double? originalQuantityMl;
  final bool isLowStock;
  final double? percentageRemaining;
  final String? purchaseDate;
  final String? expiryDate;

  InventoryItem({
    required this.id,
    required this.componentId,
    required this.componentName,
    required this.quantityMl,
    this.originalQuantityMl,
    required this.isLowStock,
    this.percentageRemaining,
    this.purchaseDate,
    this.expiryDate,
  });

  factory InventoryItem.fromJson(Map<String, dynamic> json) {
    return InventoryItem(
      id: json['id'] as int,
      componentId: json['component_id'] as int,
      componentName: json['component_name'] as String,
      quantityMl: (json['quantity_ml'] as num).toDouble(),
      originalQuantityMl: json['original_quantity_ml'] != null
          ? (json['original_quantity_ml'] as num).toDouble()
          : null,
      isLowStock: json['is_low_stock'] as bool,
      percentageRemaining: json['percentage_remaining'] != null
          ? (json['percentage_remaining'] as num).toDouble()
          : null,
      purchaseDate: json['purchase_date'] as String?,
      expiryDate: json['expiry_date'] as String?,
    );
  }
}

/// API service for nutrient operations
class NutrientsApiService {
  const NutrientsApiService(this._apiClient);
  final ApiClient _apiClient;

  /// Get all nutrient brands
  Future<List<NutrientBrand>> getBrands() async {
    try {
      final responseData = await _apiClient.get<List<dynamic>>(
        '/api/v2/nutrients/brands',
      );
      return responseData
          .map((json) => NutrientBrand.fromJson(json as Map<String, dynamic>))
          .toList();
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to fetch nutrient brands: ${e.message}');
      rethrow;
    }
  }

  /// Get components for a specific brand
  Future<List<NutrientComponent>> getComponents(int brandId) async {
    try {
      final responseData = await _apiClient.get<List<dynamic>>(
        '/api/v2/nutrients/brands/$brandId/components',
      );
      return responseData
          .map(
            (json) => NutrientComponent.fromJson(json as Map<String, dynamic>),
          )
          .toList();
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to fetch components for brand $brandId: ${e.message}');
      rethrow;
    }
  }

  /// Calculate nutrient mix
  Future<NutrientMix> calculateMix({
    required int brandId,
    required String growthStage,
    required String medium,
    required double tankSizeLiters,
    String feedingStrength = 'medium',
    double? customStrength,
    String waterType = 'tap',
  }) async {
    try {
      final requestData = {
        'brand_id': brandId,
        'growth_stage': growthStage,
        'medium': medium,
        'tank_size_liters': tankSizeLiters,
        'feeding_strength': feedingStrength,
        if (customStrength != null) 'custom_strength': customStrength,
        'water_type': waterType,
      };

      final responseData = await _apiClient.post<Map<String, dynamic>>(
        '/api/v2/nutrients/calculate',
        data: requestData,
      );

      return NutrientMix.fromJson(responseData);
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to calculate nutrient mix: ${e.message}');
      rethrow;
    }
  }

  /// Get user's nutrient inventory
  Future<List<InventoryItem>> getInventory({bool lowStockOnly = false}) async {
    try {
      final queryParams = lowStockOnly ? '?low_stock_only=true' : '';
      final responseData = await _apiClient.get<List<dynamic>>(
        '/api/v2/nutrients/inventory$queryParams',
      );
      return responseData
          .map((json) => InventoryItem.fromJson(json as Map<String, dynamic>))
          .toList();
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to fetch inventory: ${e.message}');
      rethrow;
    }
  }

  /// Add item to inventory
  Future<void> addInventory({
    required int componentId,
    required double quantityMl,
    double? originalQuantityMl,
    String? purchaseDate,
    String? expiryDate,
    double? cost,
    double lowStockThreshold = 100.0,
  }) async {
    try {
      final requestData = {
        'component_id': componentId,
        'quantity_ml': quantityMl,
        if (originalQuantityMl != null)
          'original_quantity_ml': originalQuantityMl,
        if (purchaseDate != null) 'purchase_date': purchaseDate,
        if (expiryDate != null) 'expiry_date': expiryDate,
        if (cost != null) 'cost': cost,
        'low_stock_threshold': lowStockThreshold,
      };

      await _apiClient.post<Map<String, dynamic>>(
        '/api/v2/nutrients/inventory',
        data: requestData,
      );
    } on api_ex.ApiException catch (e) {
      debugPrint('Failed to add inventory item: ${e.message}');
      rethrow;
    }
  }
}
