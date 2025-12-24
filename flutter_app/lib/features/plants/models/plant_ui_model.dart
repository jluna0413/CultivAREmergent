import 'package:flutter/material.dart';

enum PlantStatusUI {
  seedling(Colors.lightGreen),
  vegetative(Colors.green),
  flowering(Colors.yellow),
  harvest(Colors.orange),
  curing(Colors.brown),
  unknown(Colors.grey);

  const PlantStatusUI(this.color);
  final Color color;
}

class PlantUiModel {
  const PlantUiModel({
    this.id,
    this.name,
    this.description,
    this.status = PlantStatusUI.unknown,
    this.strainName,
    this.isClone = false,
    this.startDt,
    this.imageUrl,
    this.growthProgress,
  });

  factory PlantUiModel.fromJson(Map<String, dynamic> json) {
    return PlantUiModel(
      id: json['id'] as int?,
      name: json['name'] as String?,
      description: json['description'] as String?,
      status: _statusFromString(json['status'] as String?),
      strainName:
          json['strain_name'] as String? ?? json['strainName'] as String?,
      isClone:
          (json['is_clone'] as bool?) ?? (json['isClone'] as bool?) ?? false,
      startDt: _parseDate(json['start_dt'] ?? json['startDt']),
      imageUrl: json['image_url'] as String? ?? json['imageUrl'] as String?,
      growthProgress:
          (json['growth_progress'] as num?)?.toDouble() ??
          (json['growthProgress'] as num?)?.toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return <String, dynamic>{
      'id': id,
      'name': name,
      'description': description,
      'status': status.name,
      'strain_name': strainName,
      'is_clone': isClone,
      'start_dt': startDt?.toIso8601String(),
      'image_url': imageUrl,
      'growth_progress': growthProgress,
    };
  }

  final int? id;
  final String? name;
  final String? description;
  final PlantStatusUI status;
  final String? strainName;
  final bool isClone;
  final DateTime? startDt;
  final String? imageUrl;
  final double? growthProgress;

  int get ageInDays {
    if (startDt == null) {
      return 0;
    }
    return DateTime.now().difference(startDt!).inDays;
  }

  Color get statusColor => status.color;
}

DateTime? _parseDate(Object? raw) {
  if (raw == null) {
    return null;
  }
  if (raw is DateTime) {
    return raw;
  }
  if (raw is String && raw.isNotEmpty) {
    return DateTime.tryParse(raw);
  }
  return null;
}

PlantStatusUI _statusFromString(String? value) {
  if (value == null || value.isEmpty) {
    return PlantStatusUI.unknown;
  }
  return PlantStatusUI.values.firstWhere(
    (status) => status.name.toLowerCase() == value.toLowerCase(),
    orElse: () => PlantStatusUI.unknown,
  );
}
