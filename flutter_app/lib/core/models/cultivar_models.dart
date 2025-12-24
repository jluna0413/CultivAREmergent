/// Flutter models for cultivar management matching OpenAPI schemas
library;
// (removed stray library directive)

class Cultivar {
  const Cultivar({
    required this.id,
    required this.name,
    required this.description,
    required this.genetics,
    required this.thcContent,
    required this.cbdContent,
    required this.effects,
    required this.flavor,
    required this.breederId,
    required this.isActive,
    required this.createdAt,
    required this.updatedAt,
    this.breeder,
    this.images,
  });

  factory Cultivar.fromJson(Map<String, dynamic> json) {
    return Cultivar(
      id: (json['id'] as int?) ?? 0,
      name: (json['name'] as String?) ?? '',
      description: json['description'] as String?,
      genetics: (json['genetics'] as String?) ?? '',
      thcContent: ((json['thc_content'] as num?) ?? 0).toDouble(),
      cbdContent: ((json['cbd_content'] as num?) ?? 0).toDouble(),
      effects: json['effects'] as String?,
      flavor: json['flavor'] as String?,
      breederId: (json['breeder_id'] as int?) ?? 0,
      isActive: (json['is_active'] as bool?) ?? true,
      createdAt: DateTime.parse(
        (json['created_at'] as String?) ?? DateTime.now().toIso8601String(),
      ),
      updatedAt: DateTime.parse(
        (json['updated_at'] as String?) ?? DateTime.now().toIso8601String(),
      ),
      breeder: json['breeder'] != null
          ? Breeder.fromJson(json['breeder'] as Map<String, dynamic>)
          : null,
      images: json['images'] != null && json['images'] is List
          ? (json['images'] as List)
                .map<CultivarImage>(
                  (image) =>
                      CultivarImage.fromJson(image as Map<String, dynamic>),
                )
                .toList()
          : null,
    );
  }
  final int id;
  final String name;
  final String? description;
  final String genetics;
  final double thcContent;
  final double cbdContent;
  final String? effects;
  final String? flavor;
  final int breederId;
  final bool isActive;
  final DateTime createdAt;
  final DateTime updatedAt;
  final Breeder? breeder;
  final List<CultivarImage>? images;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'genetics': genetics,
      'thc_content': thcContent,
      'cbd_content': cbdContent,
      'effects': effects,
      'flavor': flavor,
      'breeder_id': breederId,
      'is_active': isActive,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
      'breeder': breeder?.toJson(),
      'images': images?.map((image) => image.toJson()).toList(),
    };
  }

  Cultivar copyWith({
    int? id,
    String? name,
    String? description,
    String? genetics,
    double? thcContent,
    double? cbdContent,
    String? effects,
    String? flavor,
    int? breederId,
    bool? isActive,
    DateTime? createdAt,
    DateTime? updatedAt,
    Breeder? breeder,
    List<CultivarImage>? images,
  }) {
    return Cultivar(
      id: id ?? this.id,
      name: name ?? this.name,
      description: description ?? this.description,
      genetics: genetics ?? this.genetics,
      thcContent: thcContent ?? this.thcContent,
      cbdContent: cbdContent ?? this.cbdContent,
      effects: effects ?? this.effects,
      flavor: flavor ?? this.flavor,
      breederId: breederId ?? this.breederId,
      isActive: isActive ?? this.isActive,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      breeder: breeder ?? this.breeder,
      images: images ?? this.images,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is Cultivar &&
        other.id == id &&
        other.name == name &&
        other.description == description &&
        other.genetics == genetics &&
        other.thcContent == thcContent &&
        other.cbdContent == cbdContent &&
        other.effects == effects &&
        other.flavor == flavor &&
        other.breederId == breederId &&
        other.isActive == isActive &&
        other.createdAt == createdAt &&
        other.updatedAt == updatedAt;
  }

  @override
  int get hashCode {
    return Object.hash(
      id,
      name,
      description,
      genetics,
      thcContent,
      cbdContent,
      effects,
      flavor,
      breederId,
      isActive,
      createdAt,
      updatedAt,
    );
  }

  @override
  String toString() {
    return 'Cultivar{id: $id, name: $name, genetics: $genetics, thcContent: $thcContent%, cbdContent: $cbdContent%}';
  }
}

class CultivarCreate {
  const CultivarCreate({
    required this.name,
    this.description,
    required this.genetics,
    this.thcContent = 0.0,
    this.cbdContent = 0.0,
    this.effects,
    this.flavor,
    this.breederId,
  });

  factory CultivarCreate.fromJson(Map<String, dynamic> json) {
    return CultivarCreate(
      name: (json['name'] as String?) ?? '',
      description: json['description'] as String?,
      genetics: (json['genetics'] as String?) ?? '',
      thcContent: ((json['thc_content'] as num?) ?? 0).toDouble(),
      cbdContent: ((json['cbd_content'] as num?) ?? 0).toDouble(),
      effects: json['effects'] as String?,
      flavor: json['flavor'] as String?,
      breederId: json['breeder_id'] as int?,
    );
  }
  final String name;
  final String? description;
  final String genetics;
  final double thcContent;
  final double cbdContent;
  final String? effects;
  final String? flavor;
  final int? breederId;

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'description': description,
      'genetics': genetics,
      'thc_content': thcContent,
      'cbd_content': cbdContent,
      'effects': effects,
      'flavor': flavor,
      'breeder_id': breederId,
    };
  }
}

class CultivarUpdate {
  const CultivarUpdate({
    this.name,
    this.description,
    this.genetics,
    this.thcContent,
    this.cbdContent,
    this.effects,
    this.flavor,
    this.breederId,
    this.isActive,
  });

  factory CultivarUpdate.fromJson(Map<String, dynamic> json) {
    return CultivarUpdate(
      name: json['name'] as String?,
      description: json['description'] as String?,
      genetics: json['genetics'] as String?,
      thcContent: (json['thc_content'] as num?)?.toDouble(),
      cbdContent: (json['cbd_content'] as num?)?.toDouble(),
      effects: json['effects'] as String?,
      flavor: json['flavor'] as String?,
      breederId: json['breeder_id'] as int?,
      isActive: json['is_active'] as bool?,
    );
  }
  final String? name;
  final String? description;
  final String? genetics;
  final double? thcContent;
  final double? cbdContent;
  final String? effects;
  final String? flavor;
  final int? breederId;
  final bool? isActive;

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'description': description,
      'genetics': genetics,
      'thc_content': thcContent,
      'cbd_content': cbdContent,
      'effects': effects,
      'flavor': flavor,
      'breeder_id': breederId,
      'is_active': isActive,
    };
  }
}

class CultivarListResponse {
  const CultivarListResponse({
    required this.items,
    required this.total,
    required this.page,
    required this.pageSize,
    required this.hasNext,
    required this.hasPrev,
  });

  factory CultivarListResponse.fromJson(Map<String, dynamic> json) {
    List<Cultivar> items = [];
    if (json['items'] != null && json['items'] is List) {
      items = (json['items'] as List)
          .map<Cultivar>(
            (item) => Cultivar.fromJson(item as Map<String, dynamic>),
          )
          .toList();
    }

    return CultivarListResponse(
      items: items,
      total: (json['total'] as int?) ?? 0,
      page: (json['page'] as int?) ?? 1,
      pageSize: (json['page_size'] as int?) ?? 20,
      hasNext: (json['has_next'] as bool?) ?? false,
      hasPrev: (json['has_prev'] as bool?) ?? false,
    );
  }
  final List<Cultivar> items;
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

class Breeder {
  const Breeder({
    required this.id,
    required this.name,
    required this.description,
    required this.website,
    required this.isActive,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Breeder.fromJson(Map<String, dynamic> json) {
    return Breeder(
      id: (json['id'] as int?) ?? 0,
      name: (json['name'] as String?) ?? '',
      description: json['description'] as String?,
      website: json['website'] as String?,
      isActive: (json['is_active'] as bool?) ?? true,
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
  final String? website;
  final bool isActive;
  final DateTime createdAt;
  final DateTime updatedAt;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'website': website,
      'is_active': isActive,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}

class BreederCreate {
  const BreederCreate({required this.name, this.description, this.website});

  factory BreederCreate.fromJson(Map<String, dynamic> json) {
    return BreederCreate(
      name: (json['name'] as String?) ?? '',
      description: json['description'] as String?,
      website: json['website'] as String?,
    );
  }
  final String name;
  final String? description;
  final String? website;

  Map<String, dynamic> toJson() {
    return {'name': name, 'description': description, 'website': website};
  }
}

class CultivarImage {
  const CultivarImage({
    required this.id,
    required this.url,
    required this.caption,
    required this.isPrimary,
    required this.createdAt,
  });

  factory CultivarImage.fromJson(Map<String, dynamic> json) {
    return CultivarImage(
      id: (json['id'] as int?) ?? 0,
      url: (json['url'] as String?) ?? '',
      caption: json['caption'] as String?,
      isPrimary: (json['is_primary'] as bool?) ?? false,
      createdAt: DateTime.parse(
        (json['created_at'] as String?) ?? DateTime.now().toIso8601String(),
      ),
    );
  }
  final int id;
  final String url;
  final String? caption;
  final bool isPrimary;
  final DateTime createdAt;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'url': url,
      'caption': caption,
      'is_primary': isPrimary,
      'created_at': createdAt.toIso8601String(),
    };
  }
}

class CultivarStats {
  const CultivarStats({
    required this.totalCultivars,
    required this.autoflower,
    required this.photoperiod,
    this.mostUsedCultivar,
    required this.mostUsedCount,
  });

  factory CultivarStats.fromJson(Map<String, dynamic> json) {
    return CultivarStats(
      totalCultivars: (json['total_cultivars'] as int?) ?? 0,
      autoflower: (json['autoflower'] as int?) ?? 0,
      photoperiod: (json['photoperiod'] as int?) ?? 0,
      mostUsedCultivar: json['most_used_cultivar'] as String?,
      mostUsedCount: (json['most_used_count'] as int?) ?? 0,
    );
  }

  final int totalCultivars;
  final int autoflower;
  final int photoperiod;
  final String? mostUsedCultivar;
  final int mostUsedCount;

  Map<String, dynamic> toJson() {
    return {
      'total_cultivars': totalCultivars,
      'autoflower': autoflower,
      'photoperiod': photoperiod,
      'most_used_cultivar': mostUsedCultivar,
      'most_used_count': mostUsedCount,
    };
  }
}
