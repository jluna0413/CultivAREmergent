import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../../core/providers/api_client_provider.dart';
import '../models/marketplace_listing.dart';

part 'marketplace_provider.g.dart';

@riverpod
class MarketplaceListings extends _$MarketplaceListings {
  @override
  Future<List<MarketplaceListing>> build() async {
    final apiClient = ref.watch(apiClientProvider);
    try {
      return await apiClient.getMarketplaceListings();
    } catch (e) {
      // Fallback for dev/demo if API fails or is empty
      // Or rethrow if we want to show error state
      print('Marketplace API Error: $e');
      return [];
    }
  }
}
