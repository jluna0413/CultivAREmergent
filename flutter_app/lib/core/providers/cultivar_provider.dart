import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/cultivar_models.dart';

/// Cultivar type enum - matching UI expectations
enum CultivarType { indica, sativa, hybrid, ruderalis }

/// Grow difficulty enum - matching UI expectations
enum GrowDifficulty { easy, medium, hard }

/// Cultivar filter for search and filtering
class CultivarFilter {
  const CultivarFilter({
    this.types,
    this.difficulties,
    this.breederId,
    this.searchQuery,
    this.autoflower,
    this.minThc,
    this.maxThc,
  });
  final List<CultivarType>? types;
  final List<GrowDifficulty>? difficulties;
  final String? breederId;
  final String? searchQuery;
  final bool? autoflower;
  final double? minThc;
  final double? maxThc;

  CultivarFilter copyWith({
    List<CultivarType>? types,
    List<GrowDifficulty>? difficulties,
    String? breederId,
    String? searchQuery,
    bool? autoflower,
    double? minThc,
    double? maxThc,
  }) {
    return CultivarFilter(
      types: types ?? this.types,
      difficulties: difficulties ?? this.difficulties,
      breederId: breederId ?? this.breederId,
      searchQuery: searchQuery ?? this.searchQuery,
      autoflower: autoflower ?? this.autoflower,
      minThc: minThc ?? this.minThc,
      maxThc: maxThc ?? this.maxThc,
    );
  }

  bool matches(Cultivar cultivar) {
    // Apply type filter
    if (types != null && types!.isNotEmpty) {
      // Convert CultivarType to string comparison
      final typeStr = _guessTypeFromGenetics(cultivar.genetics);
      if (!types!.any((type) => _typeMatches(type, typeStr))) {
        return false;
      }
    }

    // Apply difficulty filter (simplified matching)
    if (difficulties != null && difficulties!.isNotEmpty) {
      // Mock difficulty based on THC content
      final difficulty = _guessDifficultyFromThc(cultivar.thcContent);
      if (!difficulties!.contains(difficulty)) {
        return false;
      }
    }

    // Apply breeder filter
    if (breederId != null && breederId!.isNotEmpty) {
      if (cultivar.breederId.toString() != breederId) {
        return false;
      }
    }

    // Apply search query
    if (searchQuery != null && searchQuery!.isNotEmpty) {
      final query = searchQuery!.toLowerCase();
      if (!cultivar.name.toLowerCase().contains(query) &&
          !(cultivar.description?.toLowerCase().contains(query) ?? false) &&
          !cultivar.genetics.toLowerCase().contains(query)) {
        return false;
      }
    }

    // Apply autoflower filter (simplified)
    if (autoflower != null) {
      final isAutoflower = _isAutoflower(cultivar.genetics);
      if (isAutoflower != autoflower) {
        return false;
      }
    }

    // Apply THC range filters
    if (minThc != null && cultivar.thcContent < minThc!) {
      return false;
    }
    if (maxThc != null && cultivar.thcContent > maxThc!) {
      return false;
    }

    return true;
  }

  bool _typeMatches(CultivarType type, String geneticsType) {
    switch (type) {
      case CultivarType.indica:
        return geneticsType.contains('indica') ||
            geneticsType.contains('i-dominant');
      case CultivarType.sativa:
        return geneticsType.contains('sativa') ||
            geneticsType.contains('s-dominant');
      case CultivarType.hybrid:
        return geneticsType.contains('hybrid') ||
            geneticsType.contains('balanced');
      case CultivarType.ruderalis:
        return geneticsType.contains('ruderalis') ||
            geneticsType.contains('auto');
    }
  }

  String _guessTypeFromGenetics(String genetics) {
    final g = genetics.toLowerCase();
    if (g.contains('indica') || g.contains('i-dominant')) return 'indica';
    if (g.contains('sativa') || g.contains('s-dominant')) return 'sativa';
    if (g.contains('hybrid') || g.contains('balanced')) return 'hybrid';
    return 'hybrid'; // default
  }

  GrowDifficulty _guessDifficultyFromThc(double thc) {
    if (thc < 10) return GrowDifficulty.easy;
    if (thc < 20) return GrowDifficulty.medium;
    return GrowDifficulty.hard;
  }

  bool _isAutoflower(String genetics) {
    return genetics.toLowerCase().contains('auto') ||
        genetics.toLowerCase().contains('ruderalis');
  }
}

/// Extended Cultivar class matching UI expectations
class ExtendedCultivar {
  const ExtendedCultivar({
    required this.base,
    this.type,
    this.difficulty,
    this.autoflower = false,
    this.cycleTime,
    this.seedCount,
    this.plantCount,
    this.shortDescription,
    required this.thcLevel,
    required this.cbdLevel,
    this.effects,
    this.imageUrl,
  });

  factory ExtendedCultivar.fromBase(Cultivar cultivar) {
    final genetics = cultivar.genetics.toLowerCase();
    final type = _detectType(genetics);
    final difficulty = _detectDifficulty(cultivar.thcContent);
    final autoflower =
        genetics.contains('auto') || genetics.contains('ruderalis');
    final cycleTime = autoflower ? 75 : 90; // Mock cycle times
    final seedCount = 1; // Mock
    final plantCount = 0; // Mock
    final shortDescription = cultivar.description;
    final thcLevel = cultivar.thcContent;
    final cbdLevel = cultivar.cbdContent;
    final effects = cultivar.effects;
    final imageUrl = cultivar.images
        ?.firstWhere(
          (img) => img.isPrimary,
          orElse: () =>
              cultivar.images?.first ??
              CultivarImage(
                id: 0,
                url: 'https://via.placeholder.com/300x200?text=No+Image',
                caption: 'No image available',
                isPrimary: false,
                createdAt: DateTime.now(),
              ),
        )
        .url;

    return ExtendedCultivar(
      base: cultivar,
      type: type,
      difficulty: difficulty,
      autoflower: autoflower,
      cycleTime: cycleTime,
      seedCount: seedCount,
      plantCount: plantCount,
      shortDescription: shortDescription,
      thcLevel: thcLevel,
      cbdLevel: cbdLevel,
      effects: effects,
      imageUrl: imageUrl,
    );
  }
  final Cultivar base;
  final CultivarType? type;
  final GrowDifficulty? difficulty;
  final bool autoflower;
  final int? cycleTime;
  final int? seedCount;
  final int? plantCount;
  final String? shortDescription;
  final double thcLevel;
  final double cbdLevel;
  final String? effects;
  final String? imageUrl;

  static CultivarType? _detectType(String genetics) {
    if (genetics.contains('indica') && genetics.contains('sativa')) {
      if (genetics.contains('indica-dominant') ||
          genetics.contains('i-dominant')) {
        return CultivarType.indica;
      }
      if (genetics.contains('sativa-dominant') ||
          genetics.contains('s-dominant')) {
        return CultivarType.sativa;
      }
      return CultivarType.hybrid;
    }
    if (genetics.contains('indica')) return CultivarType.indica;
    if (genetics.contains('sativa')) return CultivarType.sativa;
    if (genetics.contains('ruderalis')) return CultivarType.ruderalis;
    return CultivarType.hybrid;
  }

  static GrowDifficulty _detectDifficulty(double thc) {
    if (thc < 10) return GrowDifficulty.easy;
    if (thc < 20) return GrowDifficulty.medium;
    return GrowDifficulty.hard;
  }

  // Forward base properties
  int get id => base.id;
  String get name => base.name;
  String get description => base.description ?? '';
  String get genetics => base.genetics;
  String? get breederName => base.breeder?.name;
  int get breederId => base.breederId;
  DateTime get createdAt => base.createdAt;
  DateTime get updatedAt => base.updatedAt;
  bool get isActive => base.isActive;
}

/// Cultivars provider state
class CultivarsProviderState {
  const CultivarsProviderState({
    this.cultivars = const [],
    this.filteredCultivars = const [],
    this.isLoading = false,
    this.hasError = false,
    this.error,
    this.filter,
  });
  final List<ExtendedCultivar> cultivars;
  final List<ExtendedCultivar> filteredCultivars;
  final bool isLoading;
  final bool hasError;
  final String? error;
  final CultivarFilter? filter;

  CultivarsProviderState copyWith({
    List<ExtendedCultivar>? cultivars,
    List<ExtendedCultivar>? filteredCultivars,
    bool? isLoading,
    bool? hasError,
    String? error,
    CultivarFilter? filter,
  }) {
    return CultivarsProviderState(
      cultivars: cultivars ?? this.cultivars,
      filteredCultivars: filteredCultivars ?? this.filteredCultivars,
      isLoading: isLoading ?? this.isLoading,
      hasError: hasError ?? this.hasError,
      error: error ?? this.error,
      filter: filter ?? this.filter,
    );
  }

  // Computed properties
  int get totalCount => cultivars.length;
  int get filteredCount => filteredCultivars.length;
  List<ExtendedCultivar> get sativaCultivars =>
      cultivars.where((c) => c.type == CultivarType.sativa).toList();
  List<ExtendedCultivar> get indicaCultivars =>
      cultivars.where((c) => c.type == CultivarType.indica).toList();
  List<ExtendedCultivar> get hybridCultivars =>
      cultivars.where((c) => c.type == CultivarType.hybrid).toList();
  List<ExtendedCultivar> get autoflowerCultivars =>
      cultivars.where((c) => c.autoflower).toList();
}

/// Cultivars notifier using AsyncNotifier pattern
class CultivarsNotifier extends AsyncNotifier<CultivarsProviderState> {
  @override
  Future<CultivarsProviderState> build() async {
    return await _loadCultivars();
  }

  Future<CultivarsProviderState> _loadCultivars() async {
    try {
      // Mock cultivars for now - can be enhanced with real API calls
      final mockCultivars = _getMockCultivars();
      final extendedCultivars = mockCultivars
          .map((cultivar) => ExtendedCultivar.fromBase(cultivar))
          .toList();

      return CultivarsProviderState(
        cultivars: extendedCultivars,
        filteredCultivars: extendedCultivars,
        isLoading: false,
        hasError: false,
      );
    } catch (e) {
      return CultivarsProviderState(
        isLoading: false,
        hasError: true,
        error: 'Failed to load cultivars: $e',
      );
    }
  }

  Future<void> loadCultivars() async {
    state = const AsyncValue.loading();
    try {
      final newState = await _loadCultivars();
      state = AsyncValue.data(newState);
    } catch (e, stackTrace) {
      state = AsyncValue.error(e, stackTrace);
    }
  }

  void setFilter(CultivarFilter filter) {
    final currentState = state.value;
    if (currentState == null) return;

    final filteredCultivars = currentState.cultivars
        .where((cultivar) => filter.matches(cultivar.base))
        .toList();

    state = AsyncValue.data(
      currentState.copyWith(
        filter: filter,
        filteredCultivars: filteredCultivars,
      ),
    );
  }

  void clearFilter() {
    final currentState = state.value;
    if (currentState == null) return;

    state = AsyncValue.data(
      currentState.copyWith(
        filter: null,
        filteredCultivars: currentState.cultivars,
      ),
    );
  }

  Future<void> refresh() async {
    await loadCultivars();
  }

  // Mock data for development
  List<Cultivar> _getMockCultivars() {
    return [
      Cultivar(
        id: 1,
        name: 'Purple Haze',
        description:
            'A legendary sativa-dominant hybrid with purple buds and earthy flavors.',
        genetics: 'sativa-dominant hybrid',
        thcContent: 18.0,
        cbdContent: 2.0,
        effects: 'Energetic, Creative, Uplifting',
        flavor: 'Earthy, Sweet, Grape',
        breederId: 1,
        isActive: true,
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
        breeder: Breeder(
          id: 1,
          name: 'Sensi Seeds',
          description: 'Legendary cannabis breeder since 1985',
          website: 'https://sensiseeds.com',
          isActive: true,
          createdAt: DateTime.now(),
          updatedAt: DateTime.now(),
        ),
      ),
      Cultivar(
        id: 2,
        name: 'OG Kush',
        description:
            'Classic indica hybrid known for its potent effects and pine aroma.',
        genetics: 'indica-dominant hybrid',
        thcContent: 20.0,
        cbdContent: 1.5,
        effects: 'Relaxing, Sleepy, Euphoric',
        flavor: 'Pine, Lemon, Earthy',
        breederId: 2,
        isActive: true,
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      ),
      Cultivar(
        id: 3,
        name: 'Blue Dream',
        description: 'Balanced hybrid with berry flavors and balanced effects.',
        genetics: 'sativa-dominant hybrid',
        thcContent: 17.0,
        cbdContent: 2.5,
        effects: 'Relaxing, Creative, Happy',
        flavor: 'Berry, Sweet, Herbal',
        breederId: 3,
        isActive: true,
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      ),
      Cultivar(
        id: 4,
        name: 'Northern Lights',
        description:
            'Pure indica strain known for its powerful relaxing effects.',
        genetics: 'pure indica',
        thcContent: 16.0,
        cbdContent: 1.0,
        effects: 'Sleepy, Relaxing, Euphoric',
        flavor: 'Sweet, Pine, Earthy',
        breederId: 1,
        isActive: true,
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      ),
      Cultivar(
        id: 5,
        name: 'Jack Herer',
        description:
            'Award-winning sativa named after cannabis activist Jack Herer.',
        genetics: 'sativa-dominant hybrid',
        thcContent: 19.0,
        cbdContent: 1.0,
        effects: 'Energetic, Focused, Creative',
        flavor: 'Pine, Spice, Herbal',
        breederId: 4,
        isActive: true,
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      ),
    ];
  }
}

/// Main cultivars provider using AsyncNotifierProvider
final cultivarsProvider =
    AsyncNotifierProvider<CultivarsNotifier, CultivarsProviderState>(
      CultivarsNotifier.new,
    );

/// Aliases for backward compatibility
final cultivarsNotifierProvider = cultivarsProvider;

/// Filtered cultivars provider
final filteredCultivarsProvider = Provider<List<ExtendedCultivar>>((ref) {
  final cultivarsState = ref.watch(cultivarsProvider);
  return cultivarsState.when(
    data: (state) => state.filteredCultivars,
    loading: () => <ExtendedCultivar>[],
    error: (_, __) => <ExtendedCultivar>[],
  );
});

/// Cultivars loading provider
final cultivarsLoadingProvider = Provider<bool>((ref) {
  final cultivarsState = ref.watch(cultivarsProvider);
  return cultivarsState.isLoading;
});

/// Cultivars error provider
final cultivarsErrorProvider = Provider<String?>((ref) {
  final cultivarsState = ref.watch(cultivarsProvider);
  return cultivarsState.when(
    data: (state) => state.error,
    loading: () => null,
    error: (error, _) => error.toString(),
  );
});

/// Cultivars count provider
final cultivarsCountProvider = Provider<int>((ref) {
  final cultivarsState = ref.watch(cultivarsProvider);
  return cultivarsState.when(
    data: (state) => state.filteredCount,
    loading: () => 0,
    error: (_, __) => 0,
  );
});

/// Total cultivars count provider
final totalCultivarsCountProvider = Provider<int>((ref) {
  final cultivarsState = ref.watch(cultivarsProvider);
  return cultivarsState.when(
    data: (state) => state.totalCount,
    loading: () => 0,
    error: (_, __) => 0,
  );
});
