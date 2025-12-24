/// Strains Provider - Manages strain data and operations
/// Handles strain CRUD operations, filtering, and search
library;

import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Strain data model
class Strain {
  const Strain({
    required this.id,
    required this.name,
    required this.type,
    required this.thcLevel,
    required this.cbdLevel,
    required this.difficulty,
    required this.floweringTime,
    this.genetics,
    this.description,
    this.effects,
    this.flavor,
    this.growDifficulty,
    this.yield,
    this.imageUrl,
  });

  final String id;
  final String name;
  final StrainType type;
  final double thcLevel;
  final double cbdLevel;
  final int difficulty;
  final int floweringTime;
  final String? genetics;
  final String? description;
  final List<String>? effects;
  final List<String>? flavor;
  final GrowDifficulty? growDifficulty;
  final double? yield;
  final String? imageUrl;

  Strain copyWith({
    String? id,
    String? name,
    StrainType? type,
    double? thcLevel,
    double? cbdLevel,
    int? difficulty,
    int? floweringTime,
    String? genetics,
    String? description,
    List<String>? effects,
    List<String>? flavor,
    GrowDifficulty? growDifficulty,
    double? yield,
    String? imageUrl,
  }) {
    return Strain(
      id: id ?? this.id,
      name: name ?? this.name,
      type: type ?? this.type,
      thcLevel: thcLevel ?? this.thcLevel,
      cbdLevel: cbdLevel ?? this.cbdLevel,
      difficulty: difficulty ?? this.difficulty,
      floweringTime: floweringTime ?? this.floweringTime,
      genetics: genetics ?? this.genetics,
      description: description ?? this.description,
      effects: effects ?? this.effects,
      flavor: flavor ?? this.flavor,
      growDifficulty: growDifficulty ?? this.growDifficulty,
      yield: yield ?? this.yield,
      imageUrl: imageUrl ?? this.imageUrl,
    );
  }
}

/// Strain type enum
enum StrainType { sativa, indica, hybrid }

/// Grow difficulty enum
enum GrowDifficulty { easy, medium, hard }

/// Strains filter options
class StrainFilter {
  const StrainFilter({
    this.types,
    this.difficulty,
    this.growDifficulty,
    this.searchQuery,
  });

  final List<StrainType>? types;
  final List<int>? difficulty;
  final List<GrowDifficulty>? growDifficulty;
  final String? searchQuery;
}

/// Strains provider state
class StrainsProviderState {
  const StrainsProviderState({
    required this.strains,
    this.filter,
    this.isLoading,
    this.error,
  });

  final List<Strain> strains;
  final StrainFilter? filter;
  final bool? isLoading;
  final String? error;

  bool get hasError => error != null;
  bool get isFiltered => filter != null;

  StrainsProviderState copyWith({
    List<Strain>? strains,
    StrainFilter? filter,
    bool? isLoading,
    String? error,
  }) {
    return StrainsProviderState(
      strains: strains ?? this.strains,
      filter: filter ?? this.filter,
      isLoading: isLoading ?? this.isLoading,
      error: error ?? this.error,
    );
  }

  List<Strain> get filteredStrains {
    if (filter == null) return strains;

    return strains.where((strain) {
      // Filter by type
      if (filter!.types != null && !filter!.types!.contains(strain.type)) {
        return false;
      }

      // Filter by difficulty
      if (filter!.difficulty != null &&
          !filter!.difficulty!.contains(strain.difficulty)) {
        return false;
      }

      // Filter by grow difficulty
      if (filter!.growDifficulty != null &&
          strain.growDifficulty != null &&
          !filter!.growDifficulty!.contains(strain.growDifficulty!)) {
        return false;
      }

      // Filter by search query
      if (filter!.searchQuery != null && filter!.searchQuery!.isNotEmpty) {
        final query = filter!.searchQuery!.toLowerCase();
        return strain.name.toLowerCase().contains(query) ||
            (strain.genetics?.toLowerCase().contains(query) ?? false) ||
            (strain.description?.toLowerCase().contains(query) ?? false);
      }

      return true;
    }).toList();
  }
}

/// Strains notifier class
class StrainsNotifier {
  StrainsNotifier();

  void updateStrains(List<Strain> newStrains) {
    // Simplified update method
  }

  void setFilter(StrainFilter? filter) {
    // Simplified filter method
  }

  void clearFilter() {
    // Simplified clear filter method
  }
}

// Mock data generator
List<Strain> get defaultStrains => [
  const Strain(
    id: '1',
    name: 'Purple Kush',
    type: StrainType.indica,
    thcLevel: 18.0,
    cbdLevel: 2.0,
    difficulty: 3,
    floweringTime: 60,
    genetics: 'Hindu Kush x Purple Afghani',
    description:
        'A potent indica strain with beautiful purple buds and relaxing effects.',
    effects: ['Relaxed', 'Happy', 'Sleepy'],
    flavor: ['Sweet', 'Grape', 'Earthy'],
    growDifficulty: GrowDifficulty.easy,
    yield: 450.0,
  ),
  const Strain(
    id: '2',
    name: 'White Widow',
    type: StrainType.hybrid,
    thcLevel: 20.0,
    cbdLevel: 1.5,
    difficulty: 4,
    floweringTime: 55,
    genetics: 'Brazilian Sativa x South Indian Indica',
    description: 'A legendary hybrid known for its white crystal resin.',
    effects: ['Euphoric', 'Energetic', 'Creative'],
    flavor: ['Earthy', 'Pine', 'Woody'],
    growDifficulty: GrowDifficulty.medium,
    yield: 400.0,
  ),
  const Strain(
    id: '3',
    name: 'Sour Diesel',
    type: StrainType.sativa,
    thcLevel: 22.0,
    cbdLevel: 1.0,
    difficulty: 5,
    floweringTime: 70,
    genetics: 'Chemdawg x Super Skunk',
    description: 'A energizing sativa with pungent diesel aroma.',
    effects: ['Uplifted', 'Focused', 'Energetic'],
    flavor: ['Diesel', 'Citrus', 'Skunk'],
    growDifficulty: GrowDifficulty.hard,
    yield: 350.0,
  ),
];

StrainsProviderState defaultStrainsState = StrainsProviderState(
  strains: defaultStrains,
);

// Simplified provider using Provider pattern (same as auth_provider.dart)
final strainsProvider = Provider<StrainsProviderState>((ref) {
  return defaultStrainsState;
});

// Convenience providers
final allStrainsProvider = Provider<List<Strain>>((ref) {
  final strainsState = ref.watch(strainsProvider);
  return strainsState.strains;
});

final filteredStrainsProvider = Provider<List<Strain>>((ref) {
  final strainsState = ref.watch(strainsProvider);
  return strainsState.filteredStrains;
});

final strainsLoadingProvider = Provider<bool>((ref) {
  final strainsState = ref.watch(strainsProvider);
  return strainsState.isLoading ?? false;
});

final strainsErrorProvider = Provider<String?>((ref) {
  final strainsState = ref.watch(strainsProvider);
  return strainsState.error;
});

final strainsFilterProvider = Provider<StrainFilter?>((ref) {
  final strainsState = ref.watch(strainsProvider);
  return strainsState.filter;
});

final strainsCountProvider = Provider<int>((ref) {
  final strainsState = ref.watch(strainsProvider);
  return strainsState.strains.length;
});

final filteredStrainsCountProvider = Provider<int>((ref) {
  final strainsState = ref.watch(strainsProvider);
  return strainsState.filteredStrains.length;
});

final strainsByTypeProvider = Provider<Map<StrainType, List<Strain>>>((ref) {
  final strainsState = ref.watch(strainsProvider);
  final Map<StrainType, List<Strain>> strainsByType = {};

  for (final strain in strainsState.strains) {
    if (!strainsByType.containsKey(strain.type)) {
      strainsByType[strain.type] = [];
    }
    strainsByType[strain.type]!.add(strain);
  }

  return strainsByType;
});
