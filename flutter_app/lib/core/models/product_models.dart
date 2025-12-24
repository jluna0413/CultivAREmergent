/// Product and E-commerce models
/// Consolidates product-related data models for the application
library;

/// Product category enum
enum ProductCategory { seed, equipment, nutrient, accessory }

/// Extended product category with display information
class ProductCategoryInfo {
  const ProductCategoryInfo({
    required this.category,
    required this.displayName,
    required this.icon,
    this.description,
  });

  final ProductCategory category;
  final String displayName;
  final String icon;
  final String? description;

  static const Map<ProductCategory, ProductCategoryInfo> categories = {
    ProductCategory.seed: ProductCategoryInfo(
      category: ProductCategory.seed,
      displayName: 'Seeds',
      icon: '🌱',
      description: 'Cannabis seeds for cultivation',
    ),
    ProductCategory.equipment: ProductCategoryInfo(
      category: ProductCategory.equipment,
      displayName: 'Equipment',
      icon: '⚡',
      description: 'Growing equipment and tools',
    ),
    ProductCategory.nutrient: ProductCategoryInfo(
      category: ProductCategory.nutrient,
      displayName: 'Nutrients',
      icon: '🧪',
      description: 'Nutrients and supplements',
    ),
    ProductCategory.accessory: ProductCategoryInfo(
      category: ProductCategory.accessory,
      displayName: 'Accessories',
      icon: '🔧',
      description: 'Growing accessories and supplies',
    ),
  };
}

/// Extended Product model for e-commerce
class Product {
  const Product({
    required this.id,
    required this.name,
    required this.description,
    required this.price,
    required this.category,
    this.imageUrl,
    this.inStock = true,
    this.maxQuantity = 0,
    this.stock = 0,
    this.metadata,
    this.createdAt,
    this.updatedAt,
  });

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: (json['id'] as int?) ?? 0,
      name: (json['name'] as String?) ?? '',
      description: (json['description'] as String?) ?? '',
      price: ((json['price'] as num?) ?? 0.0).toDouble(),
      category: _parseProductCategory(json['category']),
      imageUrl: json['image_url'] as String?,
      inStock: (json['in_stock'] as bool?) ?? true,
      maxQuantity: (json['max_quantity'] as int?) ?? 0,
      stock: (json['stock'] as int?) ?? 0,
      metadata: json['metadata'] as Map<String, dynamic>?,
      createdAt: json['created_at'] != null
          ? DateTime.parse(json['created_at'] as String)
          : null,
      updatedAt: json['updated_at'] != null
          ? DateTime.parse(json['updated_at'] as String)
          : null,
    );
  }

  final int id;
  final String name;
  final String description;
  final double price;
  final ProductCategory category;
  final String? imageUrl;
  final bool inStock;
  final int maxQuantity;
  final int stock;
  final Map<String, dynamic>? metadata;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'price': price,
      'category': _productCategoryToString(category),
      'image_url': imageUrl,
      'in_stock': inStock,
      'max_quantity': maxQuantity,
      'stock': stock,
      'metadata': metadata,
      'created_at': createdAt?.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
    };
  }
}

/// Cart item extension with variant support
class CartItem {
  const CartItem({
    required this.id,
    required this.productId,
    required this.productName,
    required this.price,
    required this.quantity,
    this.variant,
    this.imageUrl,
    this.description,
    this.inStock = true,
    this.maxQuantity = 10,
    this.stock = 0,
    this.productData,
    this.createdAt,
    this.updatedAt,
  });

  factory CartItem.fromJson(Map<String, dynamic> json) {
    return CartItem(
      id: (json['id'] as int?) ?? 0,
      productId: (json['product_id'] as int?) ?? 0,
      productName: (json['product_name'] as String?) ?? '',
      price: ((json['price'] as num?) ?? 0.0).toDouble(),
      quantity: (json['quantity'] as int?) ?? 1,
      variant: json['variant'] as String?,
      imageUrl: json['image_url'] as String?,
      description: json['description'] as String?,
      inStock: (json['in_stock'] as bool?) ?? true,
      maxQuantity: (json['max_quantity'] as int?) ?? 10,
      stock: (json['stock'] as int?) ?? 0,
      productData: json['product_data'] as Map<String, dynamic>?,
      createdAt: json['created_at'] != null
          ? DateTime.parse(json['created_at'] as String)
          : null,
      updatedAt: json['updated_at'] != null
          ? DateTime.parse(json['updated_at'] as String)
          : null,
    );
  }

  final int id;
  final int productId;
  final String productName;
  final double price;
  final int quantity;
  final String? variant;
  final String? imageUrl;
  final String? description;
  final bool inStock;
  final int maxQuantity;
  final int stock;
  final Map<String, dynamic>? productData;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'product_id': productId,
      'product_name': productName,
      'price': price,
      'quantity': quantity,
      'variant': variant,
      'image_url': imageUrl,
      'description': description,
      'in_stock': inStock,
      'max_quantity': maxQuantity,
      'stock': stock,
      'product_data': productData,
      'created_at': createdAt?.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
    };
  }

  /// Total price for this cart item
  double get totalPrice => price * quantity;

  /// Check if can add more quantity
  bool get canAddMore => quantity < maxQuantity;

  /// Check if in stock
  bool get hasStock => inStock && stock > 0;
}

/// Checkout information
class CheckoutInfo {
  const CheckoutInfo({
    required this.customerName,
    required this.customerEmail,
    required this.shippingAddress,
    required this.billingAddress,
    this.notes,
    this.useExistingShipping = false,
  });

  factory CheckoutInfo.fromJson(Map<String, dynamic> json) {
    return CheckoutInfo(
      customerName: (json['customer_name'] as String?) ?? '',
      customerEmail: (json['customer_email'] as String?) ?? '',
      shippingAddress: (json['shipping_address'] as String?) ?? '',
      billingAddress: (json['billing_address'] as String?) ?? '',
      notes: json['notes'] as String?,
      useExistingShipping: (json['use_existing_shipping'] as bool?) ?? false,
    );
  }

  final String customerName;
  final String customerEmail;
  final String shippingAddress;
  final String billingAddress;
  final String? notes;
  final bool useExistingShipping;

  Map<String, dynamic> toJson() {
    return {
      'customer_name': customerName,
      'customer_email': customerEmail,
      'shipping_address': shippingAddress,
      'billing_address': billingAddress,
      'notes': notes,
      'use_existing_shipping': useExistingShipping,
    };
  }
}

/// Helper functions
ProductCategory _parseProductCategory(dynamic category) {
  if (category is ProductCategory) return category;
  if (category is String) {
    switch (category.toLowerCase()) {
      case 'seed':
        return ProductCategory.seed;
      case 'equipment':
        return ProductCategory.equipment;
      case 'nutrient':
        return ProductCategory.nutrient;
      case 'accessory':
        return ProductCategory.accessory;
    }
  }
  return ProductCategory.seed; // default
}

String _productCategoryToString(ProductCategory category) {
  switch (category) {
    case ProductCategory.seed:
      return 'seed';
    case ProductCategory.equipment:
      return 'equipment';
    case ProductCategory.nutrient:
      return 'nutrient';
    case ProductCategory.accessory:
      return 'accessory';
  }
}
