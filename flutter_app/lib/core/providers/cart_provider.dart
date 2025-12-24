import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'cart_provider.g.dart';

/// Cart item data model
class CartItem {
  factory CartItem.fromJson(Map<String, dynamic> json) {
    return CartItem(
      id: json['id'] as String,
      productId: json['product_id'] as String,
      productName: json['product_name'] as String,
      category: ProductCategory.values.firstWhere(
        (e) => e.name == json['category'],
        orElse: () => ProductCategory.general,
      ),
      price: (json['price'] as num).toDouble(),
      quantity: json['quantity'] as int,
      variant: json['variant'] as String?,
      imageUrl: json['image_url'] as String?,
      description: json['description'] as String?,
      inStock: json['in_stock'] as bool?,
      maxQuantity: json['max_quantity'] as int?,
    );
  }
  const CartItem({
    required this.id,
    required this.productId,
    required this.productName,
    required this.category,
    required this.price,
    required this.quantity,
    this.variant,
    this.imageUrl,
    this.description,
    this.inStock,
    this.maxQuantity,
  });

  final String id;
  final String productId;
  final String productName;
  final ProductCategory category;
  final double price;
  final int quantity;
  final String? variant;
  final String? imageUrl;
  final String? description;
  final bool? inStock;
  final int? maxQuantity;

  CartItem copyWith({
    String? id,
    String? productId,
    String? productName,
    ProductCategory? category,
    double? price,
    int? quantity,
    String? variant,
    String? imageUrl,
    String? description,
    bool? inStock,
    int? maxQuantity,
  }) {
    return CartItem(
      id: id ?? this.id,
      productId: productId ?? this.productId,
      productName: productName ?? this.productName,
      category: category ?? this.category,
      price: price ?? this.price,
      quantity: quantity ?? this.quantity,
      variant: variant ?? this.variant,
      imageUrl: imageUrl ?? this.imageUrl,
      description: description ?? this.description,
      inStock: inStock ?? this.inStock,
      maxQuantity: maxQuantity ?? this.maxQuantity,
    );
  }

  /// Calculate subtotal for this item
  double get subtotal => price * quantity;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'product_id': productId,
      'product_name': productName,
      'category': category.name,
      'price': price,
      'quantity': quantity,
      'variant': variant,
      'image_url': imageUrl,
      'description': description,
      'in_stock': inStock,
      'max_quantity': maxQuantity,
    };
  }
}

/// Product category enum
enum ProductCategory {
  seeds,
  clones,
  nutrients,
  equipment,
  tools,
  accessories,
  books,
  general,
}

/// Checkout information
class CheckoutInfo {
  const CheckoutInfo({
    required this.subtotal,
    required this.tax,
    required this.shipping,
    required this.discount,
    required this.total,
    this.shippingAddress,
    this.paymentMethod,
    this.notes,
  });

  final double subtotal;
  final double tax;
  final double shipping;
  final double discount;
  final double total;
  final ShippingAddress? shippingAddress;
  final PaymentMethod? paymentMethod;
  final String? notes;

  CheckoutInfo copyWith({
    double? subtotal,
    double? tax,
    double? shipping,
    double? discount,
    double? total,
    ShippingAddress? shippingAddress,
    PaymentMethod? paymentMethod,
    String? notes,
  }) {
    return CheckoutInfo(
      subtotal: subtotal ?? this.subtotal,
      tax: tax ?? this.tax,
      shipping: shipping ?? this.shipping,
      discount: discount ?? this.discount,
      total: total ?? this.total,
      shippingAddress: shippingAddress ?? this.shippingAddress,
      paymentMethod: paymentMethod ?? this.paymentMethod,
      notes: notes ?? this.notes,
    );
  }
}

/// Shipping address model
class ShippingAddress {
  const ShippingAddress({
    required this.street,
    required this.city,
    required this.state,
    required this.zipCode,
    required this.country,
    this.name,
    this.phone,
    this.company,
  });

  final String street;
  final String city;
  final String state;
  final String zipCode;
  final String country;
  final String? name;
  final String? phone;
  final String? company;

  String get fullAddress {
    return '$street, $city, $state $zipCode, $country';
  }
}

/// Payment method model
class PaymentMethod {
  const PaymentMethod({
    required this.type,
    this.lastFour,
    this.brand,
    this.expiryMonth,
    this.expiryYear,
  });

  final PaymentType type;
  final String? lastFour;
  final String? brand;
  final int? expiryMonth;
  final int? expiryYear;

  String get displayName {
    switch (type) {
      case PaymentType.creditCard:
        return '$brand **** **** **** $lastFour';
      case PaymentType.debitCard:
        return 'Debit Card **** $lastFour';
      case PaymentType.paypal:
        return 'PayPal';
      case PaymentType.bankTransfer:
        return 'Bank Transfer';
      case PaymentType.cash:
        return 'Cash';
    }
  }
}

/// Payment type enum
enum PaymentType { creditCard, debitCard, paypal, bankTransfer, cash }

/// Cart provider state
class CartProviderState {
  const CartProviderState({
    required this.items,
    this.checkoutInfo,
    this.isLoading,
    this.error,
    this.promoCode,
  });

  final List<CartItem> items;
  final CheckoutInfo? checkoutInfo;
  final bool? isLoading;
  final String? error;
  final String? promoCode;

  bool get hasError => error != null;
  bool get isEmpty => items.isEmpty;
  int get itemCount => items.length;
  double get subtotal => items.fold(0.0, (sum, item) => sum + item.subtotal);

  CartProviderState copyWith({
    List<CartItem>? items,
    CheckoutInfo? checkoutInfo,
    bool? isLoading,
    String? error,
    String? promoCode,
  }) {
    return CartProviderState(
      items: items ?? this.items,
      checkoutInfo: checkoutInfo ?? this.checkoutInfo,
      isLoading: isLoading ?? this.isLoading,
      error: error ?? this.error,
      promoCode: promoCode ?? this.promoCode,
    );
  }
}

/// Simple cart provider for now
@riverpod
class CartNotifier extends _$CartNotifier {
  @override
  CartProviderState build() {
    return const CartProviderState(items: []);
  }
}
