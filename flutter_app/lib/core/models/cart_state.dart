import 'package:json_annotation/json_annotation.dart';

/// Cart items model
class CartItem {
  const CartItem({
    required this.id,
    required this.name,
    required this.price,
    required this.quantity,
    this.imageUrl,
  });

  factory CartItem.fromJson(Map<String, dynamic> json) {
    return CartItem(
      id: json['id'] as String,
      name: json['name'] as String,
      price: (json['price'] as num).toDouble(),
      quantity: json['quantity'] as int,
      imageUrl: json['image_url'] as String?,
    );
  }
  final String id;
  final String name;
  final double price;
  final int quantity;
  final String? imageUrl;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'price': price,
      'quantity': quantity,
      'image_url': imageUrl,
    };
  }

  CartItem copyWith({
    String? id,
    String? name,
    double? price,
    int? quantity,
    String? imageUrl,
  }) {
    return CartItem(
      id: id ?? this.id,
      name: name ?? this.name,
      price: price ?? this.price,
      quantity: quantity ?? this.quantity,
      imageUrl: imageUrl ?? this.imageUrl,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is CartItem &&
        other.id == id &&
        other.name == name &&
        other.price == price &&
        other.quantity == quantity &&
        other.imageUrl == imageUrl;
  }

  @override
  int get hashCode {
    return Object.hash(id, name, price, quantity, imageUrl);
  }

  @override
  String toString() {
    return 'CartItem(id: $id, name: $name, price: $price, quantity: $quantity, imageUrl: $imageUrl)';
  }
}

/// Cart provider state model for managing cart data
class CartProviderState {
  /// Creates CartProviderState with default values
  const CartProviderState({
    this.items = const [],
    this.itemCount = 0,
    this.total = 0.0,
    this.isLoading = true,
    this.error,
  });

  /// Creates CartProviderState from JSON
  factory CartProviderState.fromJson(Map<String, dynamic> json) {
    return CartProviderState(
      items:
          (json['items'] as List<dynamic>?)
              ?.map((item) => CartItem.fromJson(item as Map<String, dynamic>))
              .toList() ??
          const [],
      itemCount: json['item_count'] as int? ?? 0,
      total: (json['total'] as num?)?.toDouble() ?? 0.0,
      isLoading: json['is_loading'] as bool? ?? true,
      error: json['error'] as String?,
    );
  }

  /// List of cart items
  @JsonKey(name: 'items')
  final List<CartItem> items;

  /// Total number of items in cart
  @JsonKey(name: 'item_count')
  final int itemCount;

  /// Total cart value
  @JsonKey(name: 'total')
  final double total;

  /// Loading state flag
  @JsonKey(name: 'is_loading')
  final bool isLoading;

  /// Error message if any
  @JsonKey(name: 'error')
  final String? error;

  /// Converts CartProviderState to JSON
  Map<String, dynamic> toJson() {
    return {
      'items': items.map((item) => item.toJson()).toList(),
      'item_count': itemCount,
      'total': total,
      'is_loading': isLoading,
      'error': error,
    };
  }

  /// Creates a copy with optional field overrides
  CartProviderState copyWith({
    List<CartItem>? items,
    int? itemCount,
    double? total,
    bool? isLoading,
    String? error,
  }) {
    return CartProviderState(
      items: items ?? this.items,
      itemCount: itemCount ?? this.itemCount,
      total: total ?? this.total,
      isLoading: isLoading ?? this.isLoading,
      error: error ?? this.error,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is CartProviderState &&
        other.items == items &&
        other.itemCount == itemCount &&
        other.total == total &&
        other.isLoading == isLoading &&
        other.error == error;
  }

  @override
  int get hashCode {
    return Object.hash(items, itemCount, total, isLoading, error);
  }

  @override
  String toString() {
    return 'CartProviderState(items: ${items.length}, itemCount: $itemCount, total: $total, isLoading: $isLoading, error: $error)';
  }
}
