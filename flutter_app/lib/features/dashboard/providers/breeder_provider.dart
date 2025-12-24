import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:cultivar_app/core/api/api_client.dart';
import 'package:cultivar_app/core/providers/api_client_provider.dart';
import '../models/marketplace_breeder.dart';

final breederProfileProvider = FutureProvider<MarketplaceBreeder>((ref) async {
  final api = ref.watch(apiClientProvider);
  final response = await api.get('/api/v2/marketplace/breeders/me');
  return MarketplaceBreeder.fromJson(response.data);
});
