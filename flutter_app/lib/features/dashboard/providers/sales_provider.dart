import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:cultivar_app/core/api/api_client.dart';
import 'package:cultivar_app/core/providers/api_client_provider.dart';

final salesHistoryProvider =
    FutureProvider.family<List<Map<String, dynamic>>, int>((ref, days) async {
      final api = ref.watch(apiClientProvider);
      final response = await api.get(
        '/api/v2/sales/analytics/history',
        queryParameters: {'days': days},
      );

      return (response.data as List)
          .map((e) => e as Map<String, dynamic>)
          .toList();
    });
