// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'strain.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$StrainImpl _$$StrainImplFromJson(Map<String, dynamic> json) => _$StrainImpl(
  id: json['id'] as String,
  name: json['name'] as String,
  breederName: json['breederName'] as String,
  badge:
      $enumDecodeNullable(_$VerificationBadgeEnumMap, json['badge']) ??
      VerificationBadge.none,
  imageUrl: json['imageUrl'] as String,
  thcPercentage: (json['thcPercentage'] as num).toDouble(),
  cbdPercentage: (json['cbdPercentage'] as num).toDouble(),
  flowerTimeWeeks: (json['flowerTimeWeeks'] as num).toInt(),
  isIndica: json['isIndica'] as bool? ?? false,
  isSativa: json['isSativa'] as bool? ?? false,
  price: (json['price'] as num?)?.toDouble() ?? 0.0,
  availableStock: (json['availableStock'] as num?)?.toInt() ?? 0,
  parent1Name: json['parent1Name'] as String?,
  parent2Name: json['parent2Name'] as String?,
);

Map<String, dynamic> _$$StrainImplToJson(_$StrainImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'breederName': instance.breederName,
      'badge': _$VerificationBadgeEnumMap[instance.badge]!,
      'imageUrl': instance.imageUrl,
      'thcPercentage': instance.thcPercentage,
      'cbdPercentage': instance.cbdPercentage,
      'flowerTimeWeeks': instance.flowerTimeWeeks,
      'isIndica': instance.isIndica,
      'isSativa': instance.isSativa,
      'price': instance.price,
      'availableStock': instance.availableStock,
      'parent1Name': instance.parent1Name,
      'parent2Name': instance.parent2Name,
    };

const _$VerificationBadgeEnumMap = {
  VerificationBadge.none: 'none',
  VerificationBadge.bronze: 'bronze',
  VerificationBadge.silver: 'silver',
  VerificationBadge.gold: 'gold',
};
