/// Flutter models for plant management matching OpenAPI schemas
library;
// (removed stray library directive)

class PlantModel {
  const PlantModel({
    required this.id,
    required this.name,
    required this.description,
    required this.statusId,
    required this.cultivarId,
    required this.isClone,
    required this.autoflower,
    required this.startDate,
    required this.lastWaterDate,
    required this.lastFeedDate,
    required this.harvestDate,
    required this.userId,
    required this.createdAt,
    required this.updatedAt,
  });

  factory PlantModel.fromJson(Map<String, dynamic> json) {
    return PlantModel(
      id: (json['id'] as int?) ?? 0,
      name: (json['name'] as String?) ?? '',
      description: json['description'] as String?,
      statusId: (json['status_id'] as int?) ?? 0,
      cultivarId: json['cultivar_id'] as int?,
      isClone: (json['is_clone'] as bool?) ?? false,
      autoflower: (json['autoflower'] as bool?) ?? false,
      startDate: json['start_date'] != null
          ? DateTime.parse(json['start_date'] as String)
          : null,
      lastWaterDate: json['last_water_date'] != null
          ? DateTime.parse(json['last_water_date'] as String)
          : null,
      lastFeedDate: json['last_feed_date'] != null
          ? DateTime.parse(json['last_feed_date'] as String)
          : null,
      harvestDate: json['harvest_date'] != null
          ? DateTime.parse(json['harvest_date'] as String)
          : null,
      userId: (json['user_id'] as int?) ?? 0,
      createdAt: DateTime.parse(
        (json['created_at'] as String?) ?? DateTime.now().toIso8601String(),
      ),
      updatedAt: DateTime.parse(
        (json['updated_at'] as String?) ?? DateTime.now().toIso8601String(),
      ),
    );
  }
  final int id;
  final String name;
  final String? description;
  final int statusId;
  final int? cultivarId;
  final bool isClone;
  final bool autoflower;
  final DateTime? startDate;
  final DateTime? lastWaterDate;
  final DateTime? lastFeedDate;
  final DateTime? harvestDate;
  final int userId;
  final DateTime createdAt;
  final DateTime updatedAt;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'status_id': statusId,
      'cultivar_id': cultivarId,
      'is_clone': isClone,
      'autoflower': autoflower,
      'start_date': startDate?.toIso8601String(),
      'last_water_date': lastWaterDate?.toIso8601String(),
      'last_feed_date': lastFeedDate?.toIso8601String(),
      'harvest_date': harvestDate?.toIso8601String(),
      'user_id': userId,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }

  PlantModel copyWith({
    int? id,
    String? name,
    String? description,
    int? statusId,
    int? cultivarId,
    bool? isClone,
    bool? autoflower,
    DateTime? startDate,
    DateTime? lastWaterDate,
    DateTime? lastFeedDate,
    DateTime? harvestDate,
    int? userId,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return PlantModel(
      id: id ?? this.id,
      name: name ?? this.name,
      description: description ?? this.description,
      statusId: statusId ?? this.statusId,
      cultivarId: cultivarId ?? this.cultivarId,
      isClone: isClone ?? this.isClone,
      autoflower: autoflower ?? this.autoflower,
      startDate: startDate ?? this.startDate,
      lastWaterDate: lastWaterDate ?? this.lastWaterDate,
      lastFeedDate: lastFeedDate ?? this.lastFeedDate,
      harvestDate: harvestDate ?? this.harvestDate,
      userId: userId ?? this.userId,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is PlantModel &&
        other.id == id &&
        other.name == name &&
        other.description == description &&
        other.statusId == statusId &&
        other.cultivarId == cultivarId &&
        other.isClone == isClone &&
        other.autoflower == autoflower &&
        other.startDate == startDate &&
        other.lastWaterDate == lastWaterDate &&
        other.lastFeedDate == lastFeedDate &&
        other.harvestDate == harvestDate &&
        other.userId == userId &&
        other.createdAt == createdAt &&
        other.updatedAt == updatedAt;
  }

  @override
  int get hashCode {
    return Object.hash(
      id,
      name,
      description,
      statusId,
      cultivarId,
      isClone,
      autoflower,
      startDate,
      lastWaterDate,
      lastFeedDate,
      harvestDate,
      userId,
      createdAt,
      updatedAt,
    );
  }

  @override
  String toString() {
    return 'PlantModel{id: $id, name: $name, statusId: $statusId, isClone: $isClone, autoflower: $autoflower}';
  }
}

class PlantCreateModel {
  const PlantCreateModel({
    required this.name,
    this.description,
    required this.statusId,
    this.cultivarId,
    this.isClone = false,
    this.autoflower = false,
  });

  factory PlantCreateModel.fromJson(Map<String, dynamic> json) {
    return PlantCreateModel(
      name: (json['name'] as String?) ?? '',
      description: json['description'] as String?,
      statusId: (json['status_id'] as int?) ?? 0,
      cultivarId: json['cultivar_id'] as int?,
      isClone: (json['is_clone'] as bool?) ?? false,
      autoflower: (json['autoflower'] as bool?) ?? false,
    );
  }
  final String name;
  final String? description;
  final int statusId;
  final int? cultivarId;
  final bool isClone;
  final bool autoflower;

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'description': description,
      'status_id': statusId,
      'cultivar_id': cultivarId,
      'is_clone': isClone,
      'autoflower': autoflower,
    };
  }

  PlantCreateModel copyWith({
    String? name,
    String? description,
    int? statusId,
    int? cultivarId,
    bool? isClone,
    bool? autoflower,
  }) {
    return PlantCreateModel(
      name: name ?? this.name,
      description: description ?? this.description,
      statusId: statusId ?? this.statusId,
      cultivarId: cultivarId ?? this.cultivarId,
      isClone: isClone ?? this.isClone,
      autoflower: autoflower ?? this.autoflower,
    );
  }
}

class PlantUpdateModel {
  const PlantUpdateModel({
    this.name,
    this.description,
    this.statusId,
    this.cultivarId,
    this.isClone,
    this.autoflower,
    this.startDate,
    this.lastWaterDate,
    this.lastFeedDate,
    this.harvestDate,
  });

  factory PlantUpdateModel.fromJson(Map<String, dynamic> json) {
    return PlantUpdateModel(
      name: (json['name'] as String?),
      description: (json['description'] as String?),
      statusId: (json['status_id'] as int?),
      cultivarId: (json['cultivar_id'] as int?),
      isClone: (json['is_clone'] as bool?),
      autoflower: (json['autoflower'] as bool?),
      startDate: json['start_date'] != null
          ? DateTime.parse(json['start_date'] as String)
          : null,
      lastWaterDate: json['last_water_date'] != null
          ? DateTime.parse(json['last_water_date'] as String)
          : null,
      lastFeedDate: json['last_feed_date'] != null
          ? DateTime.parse(json['last_feed_date'] as String)
          : null,
      harvestDate: json['harvest_date'] != null
          ? DateTime.parse(json['harvest_date'] as String)
          : null,
    );
  }
  final String? name;
  final String? description;
  final int? statusId;
  final int? cultivarId;
  final bool? isClone;
  final bool? autoflower;
  final DateTime? startDate;
  final DateTime? lastWaterDate;
  final DateTime? lastFeedDate;
  final DateTime? harvestDate;

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'description': description,
      'status_id': statusId,
      'cultivar_id': cultivarId,
      'is_clone': isClone,
      'autoflower': autoflower,
      'start_date': startDate?.toIso8601String(),
      'last_water_date': lastWaterDate?.toIso8601String(),
      'last_feed_date': lastFeedDate?.toIso8601String(),
      'harvest_date': harvestDate?.toIso8601String(),
    };
  }
}

class PlantListResponseModel {
  const PlantListResponseModel({
    required this.items,
    required this.total,
    required this.page,
    required this.pageSize,
    required this.hasNext,
    required this.hasPrev,
  });

  factory PlantListResponseModel.fromJson(Map<String, dynamic> json) {
    List<PlantModel> items = [];
    if (json['items'] != null && json['items'] is List) {
      items = (json['items'] as List)
          .map<PlantModel>(
            (item) => PlantModel.fromJson(item as Map<String, dynamic>),
          )
          .toList();
    }

    return PlantListResponseModel(
      items: items,
      total: (json['total'] as int?) ?? 0,
      page: (json['page'] as int?) ?? 1,
      pageSize: (json['page_size'] as int?) ?? 20,
      hasNext: (json['has_next'] as bool?) ?? false,
      hasPrev: (json['has_prev'] as bool?) ?? false,
    );
  }
  final List<PlantModel> items;
  final int total;
  final int page;
  final int pageSize;
  final bool hasNext;
  final bool hasPrev;

  Map<String, dynamic> toJson() {
    return {
      'items': items.map((item) => item.toJson()).toList(),
      'total': total,
      'page': page,
      'page_size': pageSize,
      'has_next': hasNext,
      'has_prev': hasPrev,
    };
  }
}

class PlantsStatsResponseModel {
  const PlantsStatsResponseModel({
    required this.totalPlants,
    required this.activePlants,
    required this.clones,
    required this.harvested,
    required this.byStatus,
  });

  factory PlantsStatsResponseModel.fromJson(Map<String, dynamic> json) {
    return PlantsStatsResponseModel(
      totalPlants: (json['total_plants'] as int?) ?? 0,
      activePlants: (json['active_plants'] as int?) ?? 0,
      clones: (json['clones'] as int?) ?? 0,
      harvested: (json['harvested'] as int?) ?? 0,
      byStatus: json['by_status'] is Map<String, dynamic>
          ? Map<String, int>.from(
              (json['by_status'] as Map<String, dynamic>).map(
                (k, v) => MapEntry(k, (v as int?) ?? 0),
              ),
            )
          : {},
    );
  }
  final int totalPlants;
  final int activePlants;
  final int clones;
  final int harvested;
  final Map<String, int> byStatus;

  Map<String, dynamic> toJson() {
    return {
      'total_plants': totalPlants,
      'active_plants': activePlants,
      'clones': clones,
      'harvested': harvested,
      'by_status': byStatus,
    };
  }

  PlantsStatsResponseModel copyWith({
    int? totalPlants,
    int? activePlants,
    int? clones,
    int? harvested,
    Map<String, int>? byStatus,
  }) {
    return PlantsStatsResponseModel(
      totalPlants: totalPlants ?? this.totalPlants,
      activePlants: activePlants ?? this.activePlants,
      clones: clones ?? this.clones,
      harvested: harvested ?? this.harvested,
      byStatus: byStatus ?? this.byStatus,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is PlantsStatsResponseModel &&
        other.totalPlants == totalPlants &&
        other.activePlants == activePlants &&
        other.clones == clones &&
        other.harvested == harvested &&
        _mapsEqual(other.byStatus, byStatus);
  }

  bool _mapsEqual(Map<String, int> a, Map<String, int> b) {
    if (a.length != b.length) return false;
    for (String key in a.keys) {
      if (!b.containsKey(key) || a[key] != b[key]) return false;
    }
    return true;
  }

  @override
  int get hashCode {
    return Object.hash(totalPlants, activePlants, clones, harvested, byStatus);
  }

  @override
  String toString() {
    return 'PlantsStatsResponseModel{totalPlants: $totalPlants, activePlants: $activePlants, clones: $clones, harvested: $harvested}';
  }
}

class PlantStatusModel {
  const PlantStatusModel({
    required this.id,
    required this.name,
    required this.description,
    required this.color,
  });

  factory PlantStatusModel.fromJson(Map<String, dynamic> json) {
    return PlantStatusModel(
      id: (json['id'] as int?) ?? 0,
      name: (json['name'] as String?) ?? '',
      description: (json['description'] as String?) ?? '',
      color: (json['color'] as String?) ?? '#000000',
    );
  }
  final int id;
  final String name;
  final String description;
  final String color;

  Map<String, dynamic> toJson() {
    return {'id': id, 'name': name, 'description': description, 'color': color};
  }
}
