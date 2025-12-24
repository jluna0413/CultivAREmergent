import 'dart:convert';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Product categories enum
enum ProductCategory {
  seeds,
  clones,
  nutrients,
  equipment,
  tools,
  accessories,
  books,
  unknown,
}

/// Cart item model
class CartItem {
  factory CartItem.fromJson(Map<String, dynamic> json) {
    return CartItem(
      id: json['id'] as String,
      productId: json['productId'] as String,
      productName: json['productName'] as String,
      price: (json['price'] as num).toDouble(),
      quantity: json['quantity'] as int,
      variantId: json['variantId'] as String?,
      variant: json['variant'] as String?,
      category: json['category'] as String?,
      categoryType: json['categoryType'] != null
          ? ProductCategory.values.firstWhere(
              (e) => e.name == json['categoryType'],
              orElse: () => ProductCategory.unknown,
            )
          : null,
      imageUrl: json['imageUrl'] as String?,
      description: json['description'] as String?,
      maxQuantity: json['maxQuantity'] as int?,
      inStock: json['inStock'] as bool?,
    );
  }
  const CartItem({
    required this.id,
    required this.productId,
    required this.productName,
    required this.price,
    required this.quantity,
    this.variantId,
    this.variant,
    this.category,
    this.categoryType,
    this.imageUrl,
    this.description,
    this.maxQuantity,
    this.inStock,
  });

  final String id;
  final String productId;
  final String productName;
  final double price;
  final int quantity;
  final String? variantId;
  final String? variant;
  final String? category;
  final ProductCategory? categoryType;
  final String? imageUrl;
  final String? description;
  final int? maxQuantity;
  final bool? inStock;

  CartItem copyWith({
    String? id,
    String? productId,
    String? productName,
    double? price,
    int? quantity,
    String? variantId,
    String? variant,
    String? category,
    ProductCategory? categoryType,
    String? imageUrl,
    String? description,
    int? maxQuantity,
    bool? inStock,
  }) {
    return CartItem(
      id: id ?? this.id,
      productId: productId ?? this.productId,
      productName: productName ?? this.productName,
      price: price ?? this.price,
      quantity: quantity ?? this.quantity,
      variantId: variantId ?? this.variantId,
      variant: variant ?? this.variant,
      category: category ?? this.category,
      categoryType: categoryType ?? this.categoryType,
      imageUrl: imageUrl ?? this.imageUrl,
      description: description ?? this.description,
      maxQuantity: maxQuantity ?? this.maxQuantity,
      inStock: inStock ?? this.inStock,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'productId': productId,
      'productName': productName,
      'price': price,
      'quantity': quantity,
      'variantId': variantId,
      'variant': variant,
      'category': category,
      'categoryType': categoryType?.name,
      'imageUrl': imageUrl,
      'description': description,
      'maxQuantity': maxQuantity,
      'inStock': inStock,
    };
  }
}

/// Checkout information
class CheckoutInfo {
  factory CheckoutInfo.fromJson(Map<String, dynamic> json) {
    return CheckoutInfo(
      subtotal: (json['subtotal'] as num).toDouble(),
      tax: (json['tax'] as num).toDouble(),
      shipping: (json['shipping'] as num).toDouble(),
      discount: (json['discount'] as num).toDouble(),
      total: (json['total'] as num).toDouble(),
    );
  }
  const CheckoutInfo({
    required this.subtotal,
    required this.tax,
    required this.shipping,
    required this.discount,
    required this.total,
  });

  final double subtotal;
  final double tax;
  final double shipping;
  final double discount;
  final double total;

  CheckoutInfo copyWith({
    double? subtotal,
    double? tax,
    double? shipping,
    double? discount,
    double? total,
  }) {
    return CheckoutInfo(
      subtotal: subtotal ?? this.subtotal,
      tax: tax ?? this.tax,
      shipping: shipping ?? this.shipping,
      discount: discount ?? this.discount,
      total: total ?? this.total,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'subtotal': subtotal,
      'tax': tax,
      'shipping': shipping,
      'discount': discount,
      'total': total,
    };
  }
}

/// Cart provider state - Alias for backward compatibility
typedef CartProviderState = CartState;

/// Cart provider state
class CartState {
  const CartState({
    this.items = const [],
    this.isLoading = false,
    this.hasError = false,
    this.error,
    this.promoCode,
    this.discountPercentage,
    this.checkoutInfo,
  });

  final List<CartItem> items;
  final bool isLoading;
  final bool hasError;
  final String? error;
  final String? promoCode;
  final double? discountPercentage;
  final CheckoutInfo? checkoutInfo;

  CartState copyWith({
    List<CartItem>? items,
    bool? isLoading,
    bool? hasError,
    String? error,
    String? promoCode,
    double? discountPercentage,
    CheckoutInfo? checkoutInfo,
  }) {
    return CartState(
      items: items ?? this.items,
      isLoading: isLoading ?? this.isLoading,
      hasError: hasError ?? this.hasError,
      error: error,
      promoCode: promoCode ?? this.promoCode,
      discountPercentage: discountPercentage ?? this.discountPercentage,
      checkoutInfo: checkoutInfo ?? this.checkoutInfo,
    );
  }

  // Computed properties
  bool get isEmpty => items.isEmpty;
  int get itemCount => items.fold(0, (sum, item) => sum + item.quantity);
  double get subtotal =>
      items.fold(0.0, (sum, item) => sum + (item.price * item.quantity));
}

/// Cart notifier using AsyncNotifier pattern
class CartNotifier extends AsyncNotifier<CartState> {
  static const String cartKey = 'shopping_cart';
  static const String promoKey = 'cart_promo_code';

  @override
  Future<CartState> build() async {
    return await _loadCart();
  }

  Future<CartState> _loadCart() async {
    try {
      final prefs = await SharedPreferences.getInstance();

      final cartJson = prefs.getString(cartKey);
      final promoCode = prefs.getString(promoKey);

      List<CartItem> items = [];
      double? discountPercentage;

      if (cartJson != null) {
        items = _deserializeCart(cartJson);
      }

      if (promoCode != null) {
        discountPercentage = _validatePromoCode(promoCode);
      }

      return CartState(
        items: items,
        promoCode: promoCode,
        discountPercentage: discountPercentage,
        hasError: false,
      );
    } catch (e) {
      return const CartState(hasError: true, error: 'Failed to load cart');
    }
  }

  Future<void> _saveCart(List<CartItem> items) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(cartKey, _serializeCart(items));
      if (state.value?.promoCode != null) {
        await prefs.setString(promoKey, state.value!.promoCode!);
      }
    } catch (e) {
      // Silent fail for storage issues
    }
  }

  String _serializeCart(List<CartItem> items) {
    final json = items.map((item) => item.toJson()).toList();
    return jsonEncode(json);
  }

  List<CartItem> _deserializeCart(String cartJson) {
    try {
      final List<dynamic> jsonList = jsonDecode(cartJson) as List;
      return jsonList
          .map((json) => CartItem.fromJson(json as Map<String, dynamic>))
          .toList();
    } catch (e) {
      return [];
    }
  }

  double? _validatePromoCode(String code) {
    switch (code.toUpperCase()) {
      case 'WELCOME10':
        return 10.0;
      case 'SAVE15':
        return 15.0;
      case 'SPRING20':
        return 20.0;
      default:
        return null;
    }
  }

  Future<void> addItem(CartItem item) async {
    state = const AsyncValue.loading();
    try {
      final currentState = state.value!;
      final existingItems = List<CartItem>.from(currentState.items);
      final existingIndex = existingItems.indexWhere(
        (existingItem) =>
            existingItem.productId == item.productId &&
            existingItem.variantId == item.variantId,
      );

      if (existingIndex >= 0) {
        existingItems[existingIndex] = existingItems[existingIndex].copyWith(
          quantity: existingItems[existingIndex].quantity + item.quantity,
        );
      } else {
        existingItems.add(item);
      }

      final newState = currentState.copyWith(
        items: existingItems,
        hasError: false,
        error: null,
      );

      state = AsyncValue.data(newState);
      await _saveCart(existingItems);
    } catch (e) {
      state = AsyncValue.error(
        'Failed to add item to cart: $e',
        StackTrace.current,
      );
    }
  }

  Future<void> updateQuantity(
    String productId,
    String? variantId,
    int quantity,
  ) async {
    state = const AsyncValue.loading();
    try {
      if (quantity <= 0) {
        await removeItem(productId, variantId);
        return;
      }

      final currentState = state.value!;
      final newItems = currentState.items.map((item) {
        if (item.productId == productId && item.variantId == variantId) {
          return item.copyWith(quantity: quantity);
        }
        return item;
      }).toList();

      final newState = currentState.copyWith(
        items: newItems,
        hasError: false,
        error: null,
      );

      state = AsyncValue.data(newState);
      await _saveCart(newItems);
    } catch (e) {
      state = AsyncValue.error(
        'Failed to update quantity: $e',
        StackTrace.current,
      );
    }
  }

  Future<void> removeItem(String productId, [String? variantId]) async {
    state = const AsyncValue.loading();
    try {
      final currentState = state.value!;
      final newItems = currentState.items.where((item) {
        return !(item.productId == productId && item.variantId == variantId);
      }).toList();

      final newState = currentState.copyWith(
        items: newItems,
        hasError: false,
        error: null,
      );

      state = AsyncValue.data(newState);
      await _saveCart(newItems);
    } catch (e) {
      state = AsyncValue.error('Failed to remove item: $e', StackTrace.current);
    }
  }

  Future<void> clearCart() async {
    state = const AsyncValue.loading();
    try {
      final newState = const CartState(items: [], hasError: false, error: null);

      state = AsyncValue.data(newState);
      await _saveCart([]);
    } catch (e) {
      state = AsyncValue.error('Failed to clear cart: $e', StackTrace.current);
    }
  }

  Future<void> applyPromoCode(String code) async {
    state = const AsyncValue.loading();
    try {
      final discountPercentage = _validatePromoCode(code);

      if (discountPercentage == null) {
        final currentState = state.value!;
        state = AsyncValue.data(
          currentState.copyWith(hasError: true, error: 'Invalid promo code'),
        );
        return;
      }

      final currentState = state.value!;
      final newState = currentState.copyWith(
        promoCode: code,
        discountPercentage: discountPercentage,
        hasError: false,
        error: null,
      );

      state = AsyncValue.data(newState);
      await _saveCart(currentState.items);
    } catch (e) {
      state = AsyncValue.error(
        'Failed to apply promo code: $e',
        StackTrace.current,
      );
    }
  }

  Future<void> removePromoCode() async {
    state = const AsyncValue.loading();
    try {
      final currentState = state.value!;
      final newState = currentState.copyWith(
        promoCode: null,
        discountPercentage: null,
        hasError: false,
        error: null,
      );

      state = AsyncValue.data(newState);
      await _saveCart(currentState.items);
    } catch (e) {
      state = AsyncValue.error(
        'Failed to remove promo code: $e',
        StackTrace.current,
      );
    }
  }

  void clearError() {
    if (state.value?.error != null) {
      final currentState = state.value!;
      state = AsyncValue.data(
        currentState.copyWith(error: null, hasError: false),
      );
    }
  }

  CartItem? getItem(String productId, String? variantId) {
    try {
      return state.value?.items.firstWhere(
        (item) => item.productId == productId && item.variantId == variantId,
      );
    } catch (e) {
      return null;
    }
  }

  bool isInCart(String productId, String? variantId) {
    return getItem(productId, variantId) != null;
  }

  int getQuantityForItem(String productId, String? variantId) {
    final item = getItem(productId, variantId);
    return item?.quantity ?? 0;
  }

  Future<void> refresh() async {
    await _loadCart();
  }

  /// Update item quantity (alias for updateQuantity)
  Future<void> updateItemQuantity(String id, int quantity) async {
    return updateQuantity(id, null, quantity);
  }
}

/// Cart provider declaration using AsyncNotifierProvider
final cartProvider = AsyncNotifierProvider<CartNotifier, CartState>(
  CartNotifier.new,
);

/// Alias for backward compatibility
final cartNotifierProvider = cartProvider;

/// Computed properties as providers
final cartSubtotalProvider = Provider<double>((ref) {
  final cartState = ref.watch(cartProvider);
  return cartState.when(
    data: (data) => data.subtotal,
    loading: () => 0.0,
    error: (_, __) => 0.0,
  );
});

final cartTotalProvider = Provider<double>((ref) {
  final cartState = ref.watch(cartProvider);
  return cartState.when(
    data: (data) {
      final subtotal = data.subtotal;
      final discount = data.discountPercentage != null
          ? subtotal * data.discountPercentage! / 100
          : 0.0;
      final tax = subtotal * 0.08; // 8% tax rate
      return subtotal - discount + tax;
    },
    loading: () => 0.0,
    error: (_, __) => 0.0,
  );
});

final cartDiscountProvider = Provider<double>((ref) {
  final cartState = ref.watch(cartProvider);
  return cartState.when(
    data: (data) => data.discountPercentage != null
        ? data.subtotal * data.discountPercentage! / 100
        : 0.0,
    loading: () => 0.0,
    error: (_, __) => 0.0,
  );
});

final cartTaxProvider = Provider<double>((ref) {
  final cartState = ref.watch(cartProvider);
  return cartState.when(
    data: (data) => data.subtotal * 0.08, // 8% tax rate
    loading: () => 0.0,
    error: (_, __) => 0.0,
  );
});

final cartTotalItemsProvider = Provider<int>((ref) {
  final cartState = ref.watch(cartProvider);
  return cartState.when(
    data: (data) => data.itemCount,
    loading: () => 0,
    error: (_, __) => 0,
  );
});

final cartIsEmptyProvider = Provider<bool>((ref) {
  final cartState = ref.watch(cartProvider);
  return cartState.when(
    data: (data) => data.isEmpty,
    loading: () => true,
    error: (_, __) => true,
  );
});

final cartLoadingProvider = Provider<bool>((ref) {
  final cartState = ref.watch(cartProvider);
  return cartState.isLoading;
});

final cartErrorProvider = Provider<String?>((ref) {
  final cartState = ref.watch(cartProvider);
  return cartState.when(
    data: (data) => data.error,
    loading: () => null,
    error: (error, _) => error.toString(),
  );
});

final cartPromoCodeProvider = Provider<String?>((ref) {
  final cartState = ref.watch(cartProvider);
  return cartState.when(
    data: (data) => data.promoCode,
    loading: () => null,
    error: (_, __) => null,
  );
});

final cartDiscountPercentageProvider = Provider<double?>((ref) {
  final cartState = ref.watch(cartProvider);
  return cartState.when(
    data: (data) => data.discountPercentage,
    loading: () => null,
    error: (_, __) => null,
  );
});
