import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../models/cart_item.dart';
import '../../marketplace/models/marketplace_listing.dart';
import '../../../core/providers/api_client_provider.dart';

part 'cart_provider.g.dart';

@riverpod
class Cart extends _$Cart {
  @override
  List<CartItem> build() {
    return [];
  }

  Future<void> syncFromBackend() async {
    final apiClient = ref.read(apiClientProvider);
    try {
      final jsonItems = await apiClient.getCart();
      state = jsonItems.map((json) {
        final listingJson = json['listing'];
        return CartItem(
          listing: MarketplaceListing.fromJson({
            'id': listingJson['id'].toString(),
            'strainName': listingJson['strain_name'] ?? 'Unknown',
            'breederName': listingJson['breeder_name'] ?? 'Unknown',
            'imageUrl':
                listingJson['image_url'] ?? 'https://via.placeholder.com/400',
            'price':
                (listingJson['pack_${json['pack_size']}_price'] ?? 0.0)
                    as double,
            'availablePacks':
                (listingJson['pack_${json['pack_size']}_available'] ?? 0)
                    as int,
          }),
          quantity: json['quantity'] as int,
        );
      }).toList();
    } catch (e) {
      print('Cart sync error: $e');
    }
  }

  Future<void> addItem(MarketplaceListing listing) async {
    final apiClient = ref.read(apiClientProvider);
    await apiClient.addToCart(int.parse(listing.id));
    await syncFromBackend();
  }

  Future<void> removeItem(String listingId) async {
    // For now, since we don't store cart_item_id in frontend model yet,
    // we'll just clear or find the first match. In real app, model should have ID.
    final apiClient = ref.read(apiClientProvider);
    // await apiClient.removeFromCart(id);
    // Simplified: clear for demo or re-sync
    await syncFromBackend();
  }

  void updateQuantity(String listingId, int quantity) {
    // Local update for responsiveness, then sync
    state = state.map((item) {
      if (item.listing.id == listingId) {
        return item.copyWith(quantity: quantity);
      }
      return item;
    }).toList();
    // TODO: Call API patch
  }

  Future<void> clear() async {
    final apiClient = ref.read(apiClientProvider);
    await apiClient.clearCart();
    state = [];
  }

  Future<void> checkout({
    String? shippingAddress,
    String paymentMethod = "card",
  }) async {
    final apiClient = ref.read(apiClientProvider);

    final items = state
        .map(
          (item) => {
            'listing_id': int.parse(item.listing.id),
            'pack_size': 5,
            'quantity': item.quantity,
          },
        )
        .toList();

    await apiClient.processCheckout(
      items: items,
      shippingAddress: shippingAddress,
      paymentMethod: paymentMethod,
    );

    state = [];
  }

  double get total {
    return state.fold(
      0,
      (sum, item) => sum + (item.listing.price * item.quantity),
    );
  }
}
