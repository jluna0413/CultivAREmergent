import '../data/cultivars_api_client.dart';
import '../domain/cultivar_model.dart' as cultivar_model;
import '../domain/strain_model.dart' as strain_model;
import 'package:flutter_riverpod/flutter_riverpod.dart';

// API Client Provider - Add this import
import '../../../core/api/api_client.dart';

// API Client Provider
final apiClientProvider = Provider<ApiClient>((ref) {
  return ApiClient();
});

// API Client Provider
final cultivarsApiClientProvider = Provider<CultivarsApiClient>((ref) {
  return CultivarsApiClient(ref.read(apiClientProvider));
});

// Strains Parameters Provider (for filtering/search)
final strainsParamsProvider =
    NotifierProvider<StrainsParamsNotifier, cultivar_model.StrainsParams>(() {
      return StrainsParamsNotifier();
    });

class StrainsParamsNotifier extends Notifier<cultivar_model.StrainsParams> {
  @override
  cultivar_model.StrainsParams build() {
    return const cultivar_model.StrainsParams();
  }

  void updateSearch(String? search) {
    state = state.copyWith(search: search);
  }

  void updateBreederId(int? breederId) {
    state = state.copyWith(breederId: breederId);
  }

  void updateAutoflower(bool? autoflower) {
    state = state.copyWith(autoflower: autoflower);
  }

  void updateSortBy(String? sortBy) {
    state = state.copyWith(sortBy: sortBy);
  }

  void updateSortOrder(String sortOrder) {
    state = state.copyWith(sortOrder: sortOrder);
  }

  void resetFilters() {
    state = const cultivar_model.StrainsParams();
  }

  void nextPage() {
    state = state.copyWithNextPage();
  }

  void prevPage() {
    state = state.copyWithPrevPage();
  }
}

// Paginated Strains List Provider
final paginatedStrainsProvider =
    FutureProvider.family<
      strain_model.PaginatedStrainsResponse,
      cultivar_model.StrainsParams
    >((ref, params) async {
      final apiClient = ref.read(cultivarsApiClientProvider);
      return apiClient.getCultivars(
        page: params.page,
        limit: params.limit,
        search: params.search,
        breederId: params.breederId,
        autoflower: params.autoflower,
        sortBy: params.sortBy,
        sortOrder: params.sortOrder,
      );
    });

// All Strains Provider (for dropdowns/searches)
final allStrainsProvider = FutureProvider<List<strain_model.Cultivar>>((
  ref,
) async {
  final apiClient = ref.read(cultivarsApiClientProvider);
  final response = await apiClient.getCultivars(limit: 1000); // Get all strains
  return response.data;
});

// Single Strain Provider
final strainProvider = FutureProvider.family<strain_model.Cultivar, int>((
  ref,
  strainId,
) async {
  final apiClient = ref.read(cultivarsApiClientProvider);
  return apiClient.getCultivar(strainId);
});

// Strain Stats Provider
final strainStatsProvider = FutureProvider<strain_model.CultivarStats>((
  ref,
) async {
  final apiClient = ref.read(cultivarsApiClientProvider);
  return apiClient.getCultivarStats();
});

// Filtered Strains Provider
final filteredStrainsProvider = FutureProvider<List<strain_model.Cultivar>>((
  ref,
) async {
  final params = ref.watch(strainsParamsProvider);
  final apiClient = ref.read(cultivarsApiClientProvider);

  if (params.search != null ||
      params.breederId != null ||
      params.autoflower != null) {
    return apiClient.filterCultivars(
      breederId: params.breederId,
      autoflower: params.autoflower,
      search: params.search,
    );
  } else {
    final response = await apiClient.getCultivars(limit: 100);
    return response.data;
  }
});

// Search Strains Provider
final searchStrainsProvider =
    FutureProvider.family<List<strain_model.Cultivar>, String>((
      ref,
      query,
    ) async {
      if (query.isEmpty) return [];
      final apiClient = ref.read(cultivarsApiClientProvider);
      return apiClient.searchCultivars(query);
    });

// Strain Mutations (Create/Update/Delete)
final createStrainMutationProvider =
    FutureProvider.family<strain_model.Cultivar, strain_model.CultivarCreate>((
      ref,
      data,
    ) async {
      final apiClient = ref.read(cultivarsApiClientProvider);
      final newStrain = await apiClient.createCultivar(data);

      // Invalidate related providers
      ref.invalidate(paginatedStrainsProvider);
      ref.invalidate(allStrainsProvider);
      ref.invalidate(filteredStrainsProvider);
      ref.invalidate(strainStatsProvider);

      return newStrain;
    });

final updateStrainMutationProvider =
    FutureProvider.family<
      strain_model.Cultivar,
      ({int id, strain_model.CultivarUpdate data})
    >((ref, params) async {
      final apiClient = ref.read(cultivarsApiClientProvider);
      final updatedStrain = await apiClient.updateCultivar(
        params.id,
        params.data,
      );

      // Invalidate related providers
      ref.invalidate(paginatedStrainsProvider);
      ref.invalidate(strainProvider(params.id));
      ref.invalidate(allStrainsProvider);
      ref.invalidate(filteredStrainsProvider);
      ref.invalidate(strainStatsProvider);

      return updatedStrain;
    });

final deleteStrainMutationProvider = FutureProvider.family<void, int>((
  ref,
  strainId,
) async {
  final apiClient = ref.read(cultivarsApiClientProvider);
  await apiClient.deleteCultivar(strainId);

  // Invalidate related providers
  ref.invalidate(paginatedStrainsProvider);
  ref.invalidate(strainProvider(strainId));
  ref.invalidate(allStrainsProvider);
  ref.invalidate(filteredStrainsProvider);
  ref.invalidate(strainStatsProvider);
});

// Strain Form State Provider
final strainFormStateProvider =
    NotifierProvider<StrainFormNotifier, StrainFormState>(() {
      return StrainFormNotifier();
    });

class StrainFormState {
  const StrainFormState({
    this.isLoading = false,
    this.error,
    this.editingStrain,
  });

  final bool isLoading;
  final String? error;
  final strain_model.Cultivar? editingStrain;

  StrainFormState copyWith({
    bool? isLoading,
    String? error,
    strain_model.Cultivar? editingStrain,
  }) {
    return StrainFormState(
      isLoading: isLoading ?? this.isLoading,
      error: error ?? this.error,
      editingStrain: editingStrain ?? this.editingStrain,
    );
  }
}

class StrainFormNotifier extends Notifier<StrainFormState> {
  @override
  StrainFormState build() {
    return const StrainFormState();
  }

  void setLoading(bool loading) {
    state = state.copyWith(isLoading: loading, error: null);
  }

  void setError(String error) {
    state = state.copyWith(isLoading: false, error: error);
  }

  void clearError() {
    state = state.copyWith(error: null);
  }

  void setEditingStrain(strain_model.Cultivar? strain) {
    state = state.copyWith(editingStrain: strain);
  }

  void reset() {
    state = const StrainFormState();
  }
}
