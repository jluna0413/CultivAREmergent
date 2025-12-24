/// Flutter models for cart and e-commerce functionality
library;
// (removed stray library directive)

class CartItem {
  const CartItem({
    required this.id,
    required this.productId,
    required this.productName,
    required this.price,
    required this.quantity,
    this.imageUrl,
    this.description,
    this.productData,
    required this.createdAt,
    required this.updatedAt,
  });

  factory CartItem.fromJson(Map<String, dynamic> json) {
    return CartItem(
      id: (json['id'] as int?) ?? 0,
      productId: (json['product_id'] as int?) ?? 0,
      productName: (json['product_name'] as String?) ?? '',
      price: ((json['price'] as num?) ?? 0.0).toDouble(),
      quantity: (json['quantity'] as int?) ?? 1,
      imageUrl: json['image_url'] as String?,
      description: json['description'] as String?,
      productData: json['product_data'] as Map<String, dynamic>?,
      createdAt: DateTime.parse(
        (json['created_at'] as String?) ?? DateTime.now().toIso8601String(),
      ),
      updatedAt: DateTime.parse(
        (json['updated_at'] as String?) ?? DateTime.now().toIso8601String(),
      ),
    );
  }
  final int id;
  final int productId;
  final String productName;
  final double price;
  final int quantity;
  final String? imageUrl;
  final String? description;
  final Map<String, dynamic>? productData;
  final DateTime createdAt;
  final DateTime updatedAt;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'product_id': productId,
      'product_name': productName,
      'price': price,
      'quantity': quantity,
      'image_url': imageUrl,
      'description': description,
      'product_data': productData,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }

  double get totalPrice => price * quantity;

  CartItem copyWith({
    int? id,
    int? productId,
    String? productName,
    double? price,
    int? quantity,
    String? imageUrl,
    String? description,
    Map<String, dynamic>? productData,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return CartItem(
      id: id ?? this.id,
      productId: productId ?? this.productId,
      productName: productName ?? this.productName,
      price: price ?? this.price,
      quantity: quantity ?? this.quantity,
      imageUrl: imageUrl ?? this.imageUrl,
      description: description ?? this.description,
      productData: productData ?? this.productData,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  CartItem incrementQuantity() {
    return copyWith(quantity: quantity + 1);
  }

  CartItem decrementQuantity() {
    if (quantity <= 1) return this;
    return copyWith(quantity: quantity - 1);
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is CartItem &&
        other.id == id &&
        other.productId == productId &&
        other.productName == productName &&
        other.price == price &&
        other.quantity == quantity &&
        other.imageUrl == imageUrl &&
        other.description == description &&
        other.productData == productData;
  }

  @override
  int get hashCode {
    return Object.hash(
      id,
      productId,
      productName,
      price,
      quantity,
      imageUrl,
      description,
      productData,
    );
  }

  @override
  String toString() {
    return 'CartItem{id: $id, productId: $productId, productName: $productName, price: $price, quantity: $quantity}';
  }
}

class Cart {
  const Cart({
    required this.id,
    required this.userId,
    required this.items,
    required this.subtotal,
    required this.tax,
    required this.shipping,
    required this.total,
    required this.status,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Cart.fromJson(Map<String, dynamic> json) {
    final items = (json['items'] as List? ?? [])
        .map((item) => CartItem.fromJson(item as Map<String, dynamic>))
        .toList();

    return Cart(
      id: (json['id'] as int?) ?? 0,
      userId: (json['user_id'] as int?) ?? 0,
      items: items,
      subtotal: ((json['subtotal'] as num?) ?? 0.0).toDouble(),
      tax: ((json['tax'] as num?) ?? 0.0).toDouble(),
      shipping: ((json['shipping'] as num?) ?? 0.0).toDouble(),
      total: ((json['total'] as num?) ?? 0.0).toDouble(),
      status: (json['status'] as String?) ?? 'active',
      createdAt: DateTime.parse(
        (json['created_at'] as String?) ?? DateTime.now().toIso8601String(),
      ),
      updatedAt: DateTime.parse(
        (json['updated_at'] as String?) ?? DateTime.now().toIso8601String(),
      ),
    );
  }
  final int id;
  final int userId;
  final List<CartItem> items;
  final double subtotal;
  final double tax;
  final double shipping;
  final double total;
  final String status;
  final DateTime createdAt;
  final DateTime updatedAt;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'items': items.map((item) => item.toJson()).toList(),
      'subtotal': subtotal,
      'tax': tax,
      'shipping': shipping,
      'total': total,
      'status': status,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }

  int get itemCount => items.fold(0, (sum, item) => sum + item.quantity);

  bool get isEmpty => items.isEmpty;

  Cart copyWith({
    int? id,
    int? userId,
    List<CartItem>? items,
    double? subtotal,
    double? tax,
    double? shipping,
    double? total,
    String? status,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return Cart(
      id: id ?? this.id,
      userId: userId ?? this.userId,
      items: items ?? this.items,
      subtotal: subtotal ?? this.subtotal,
      tax: tax ?? this.tax,
      shipping: shipping ?? this.shipping,
      total: total ?? this.total,
      status: status ?? this.status,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is Cart &&
        other.id == id &&
        other.userId == userId &&
        _listsEqual(other.items, items) &&
        other.subtotal == subtotal &&
        other.tax == tax &&
        other.shipping == shipping &&
        other.total == total &&
        other.status == status;
  }

  bool _listsEqual(List<CartItem> a, List<CartItem> b) {
    if (a.length != b.length) return false;
    for (int i = 0; i < a.length; i++) {
      if (a[i] != b[i]) return false;
    }
    return true;
  }

  @override
  int get hashCode {
    return Object.hash(
      id,
      userId,
      items,
      subtotal,
      tax,
      shipping,
      total,
      status,
    );
  }

  @override
  String toString() {
    return 'Cart{id: $id, userId: $userId, itemCount: $itemCount, total: $total, status: $status}';
  }
}
