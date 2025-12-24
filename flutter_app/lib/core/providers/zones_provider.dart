import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Zone model for grow areas
class Zone {
  const Zone({
    required this.id,
    required this.name,
    this.description,
    this.capacity,
    this.currentPlants = 0,
    this.isActive = true,
  });

  final String id;
  final String name;
  final String? description;
  final int? capacity;
  final int currentPlants;
  final bool isActive;

  factory Zone.fromJson(Map<String, dynamic> json) {
    return Zone(
      id: json['id'] as String,
      name: json['name'] as String,
      description: json['description'] as String?,
      capacity: json['capacity'] as int?,
      currentPlants: json['current_plants'] as int? ?? 0,
      isActive: json['is_active'] as bool? ?? true,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'capacity': capacity,
      'current_plants': currentPlants,
      'is_active': isActive,
    };
  }

  Zone copyWith({
    String? id,
    String? name,
    String? description,
    int? capacity,
    int? currentPlants,
    bool? isActive,
  }) {
    return Zone(
      id: id ?? this.id,
      name: name ?? this.name,
      description: description ?? this.description,
      capacity: capacity ?? this.capacity,
      currentPlants: currentPlants ?? this.currentPlants,
      isActive: isActive ?? this.isActive,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is Zone &&
        other.id == id &&
        other.name == name &&
        other.description == description &&
        other.capacity == capacity &&
        other.currentPlants == currentPlants &&
        other.isActive == isActive;
  }

  @override
  int get hashCode {
    return Object.hash(
      id,
      name,
      description,
      capacity,
      currentPlants,
      isActive,
    );
  }

  @override
  String toString() {
    return 'Zone(id: $id, name: $name, description: $description, capacity: $capacity, currentPlants: $currentPlants, isActive: $isActive)';
  }
}

/// Zones provider state
class ZonesProviderState {
  const ZonesProviderState({
    this.zones = const [],
    this.isLoading = false,
    this.hasError = false,
    this.error,
  });

  final List<Zone> zones;
  final bool isLoading;
  final bool hasError;
  final String? error;

  ZonesProviderState copyWith({
    List<Zone>? zones,
    bool? isLoading,
    bool? hasError,
    String? error,
  }) {
    return ZonesProviderState(
      zones: zones ?? this.zones,
      isLoading: isLoading ?? this.isLoading,
      hasError: hasError ?? this.hasError,
      error: error ?? this.error,
    );
  }

  // Computed properties
  List<Zone> get activeZones => zones.where((zone) => zone.isActive).toList();
  List<Zone> get availableZones => activeZones
      .where(
        (zone) => zone.capacity == null || zone.currentPlants < zone.capacity!,
      )
      .toList();
}

/// Zones notifier using AsyncNotifier pattern
class ZonesNotifier extends AsyncNotifier<ZonesProviderState> {
  @override
  Future<ZonesProviderState> build() async {
    return await _loadZones();
  }

  Future<ZonesProviderState> _loadZones() async {
    try {
      // Mock zones for now - can be enhanced with real API calls
      final mockZones = _getMockZones();
      return ZonesProviderState(zones: mockZones);
    } catch (e) {
      return ZonesProviderState(
        hasError: true,
        error: 'Failed to load zones: $e',
      );
    }
  }

  Future<void> loadZones() async {
    state = const AsyncValue.loading();
    try {
      final newState = await _loadZones();
      state = AsyncValue.data(newState);
    } catch (e, stackTrace) {
      state = AsyncValue.error(e, stackTrace);
    }
  }

  Future<void> refresh() async {
    await loadZones();
  }

  // Mock data for development
  List<Zone> _getMockZones() {
    return [
      const Zone(
        id: 'indoor',
        name: 'Indoor',
        description: 'Indoor grow room with controlled environment',
        capacity: 50,
        currentPlants: 12,
      ),
      const Zone(
        id: 'outdoor',
        name: 'Outdoor',
        description: 'Outdoor garden area',
        capacity: 100,
        currentPlants: 25,
      ),
      const Zone(
        id: 'greenhouse',
        name: 'Greenhouse',
        description: 'Climate-controlled greenhouse',
        capacity: 75,
        currentPlants: 8,
      ),
      const Zone(
        id: 'tent',
        name: 'Grow Tent',
        description: 'Compact grow tent setup',
        capacity: 4,
        currentPlants: 2,
      ),
    ];
  }
}

/// Main zones provider using AsyncNotifierProvider
final zonesProvider = AsyncNotifierProvider<ZonesNotifier, ZonesProviderState>(
  ZonesNotifier.new,
);

/// Aliases for backward compatibility
final zonesNotifierProvider = zonesProvider;

/// Filtered zones providers
final activeZonesProvider = Provider<List<Zone>>((ref) {
  final zonesState = ref.watch(zonesProvider);
  return zonesState.when(
    data: (state) => state.activeZones,
    loading: () => <Zone>[],
    error: (_, __) => <Zone>[],
  );
});

final availableZonesProvider = Provider<List<Zone>>((ref) {
  final zonesState = ref.watch(zonesProvider);
  return zonesState.when(
    data: (state) => state.availableZones,
    loading: () => <Zone>[],
    error: (_, __) => <Zone>[],
  );
});

/// Zones loading provider
final zonesLoadingProvider = Provider<bool>((ref) {
  final zonesState = ref.watch(zonesProvider);
  return zonesState.isLoading;
});

/// Zones error provider
final zonesErrorProvider = Provider<String?>((ref) {
  final zonesState = ref.watch(zonesProvider);
  return zonesState.when(
    data: (state) => state.error,
    loading: () => null,
    error: (error, _) => error.toString(),
  );
});

/// Zones count provider
final zonesCountProvider = Provider<int>((ref) {
  final zonesState = ref.watch(zonesProvider);
  return zonesState.when(
    data: (state) => state.zones.length,
    loading: () => 0,
    error: (_, __) => 0,
  );
});
