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

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'manufacturer': manufacturer,
      'brand_type': brandType,
      'component_count': componentCount,
      'description': description,
    };
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
