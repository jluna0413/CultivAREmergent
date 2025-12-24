/// Request model for creating a new plant
class CreatePlantRequest {
  const CreatePlantRequest({
    required this.name,
    required this.cultivar,
    this.plantingDate,
    this.zone,
    this.notes,
    this.expectedHarvestDays,
    this.tags,
  });

  factory CreatePlantRequest.fromJson(Map<String, dynamic> json) {
    return CreatePlantRequest(
      name: json['name'] as String,
      cultivar: json['cultivar'] as String,
      plantingDate: json['planting_date'] != null
          ? DateTime.parse(json['planting_date'] as String)
          : null,
      zone: json['zone'] as String?,
      notes: json['notes'] as String?,
      expectedHarvestDays: json['expected_harvest_days'] as int?,
      tags: json['tags'] != null
          ? List<String>.from(json['tags'] as List)
          : null,
    );
  }
  final String name;
  final String cultivar;
  final DateTime? plantingDate;
  final String? zone;
  final String? notes;
  final int? expectedHarvestDays;
  final List<String>? tags;

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'cultivar': cultivar,
      'planting_date': plantingDate?.toIso8601String(),
      'zone': zone,
      'notes': notes,
      'expected_harvest_days': expectedHarvestDays,
      'tags': tags,
    };
  }

  CreatePlantRequest copyWith({
    String? name,
    String? cultivar,
    DateTime? plantingDate,
    String? zone,
    String? notes,
    int? expectedHarvestDays,
    List<String>? tags,
  }) {
    return CreatePlantRequest(
      name: name ?? this.name,
      cultivar: cultivar ?? this.cultivar,
      plantingDate: plantingDate ?? this.plantingDate,
      zone: zone ?? this.zone,
      notes: notes ?? this.notes,
      expectedHarvestDays: expectedHarvestDays ?? this.expectedHarvestDays,
      tags: tags ?? this.tags,
    );
  }

  @override
  String toString() {
    return 'CreatePlantRequest{name: $name, cultivar: $cultivar, zone: $zone}';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is CreatePlantRequest &&
        other.name == name &&
        other.cultivar == cultivar &&
        other.plantingDate == plantingDate &&
        other.zone == zone &&
        other.notes == notes &&
        other.expectedHarvestDays == expectedHarvestDays &&
        other.tags == tags;
  }

  @override
  int get hashCode {
    return Object.hash(
      name,
      cultivar,
      plantingDate,
      zone,
      notes,
      expectedHarvestDays,
      tags,
    );
  }
}
