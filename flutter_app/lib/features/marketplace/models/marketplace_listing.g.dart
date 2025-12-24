// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'marketplace_listing.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$MarketplaceListingImpl _$$MarketplaceListingImplFromJson(
  Map<String, dynamic> json,
) => _$MarketplaceListingImpl(
  id: json['id'] as String,
  strainName: json['strainName'] as String,
  breederName: json['breederName'] as String,
  badge:
      $enumDecodeNullable(_$VerificationBadgeEnumMap, json['badge']) ??
      VerificationBadge.none,
  imageUrl: json['imageUrl'] as String,
  price: (json['price'] as num).toDouble(),
  availablePacks: (json['availablePacks'] as num).toInt(),
  thcPercentage: (json['thcPercentage'] as num).toDouble(),
  isIndica: json['isIndica'] as bool,
  isExclusive: json['isExclusive'] as bool? ?? false,
);

Map<String, dynamic> _$$MarketplaceListingImplToJson(
  _$MarketplaceListingImpl instance,
) => <String, dynamic>{
  'id': instance.id,
  'strainName': instance.strainName,
  'breederName': instance.breederName,
  'badge': _$VerificationBadgeEnumMap[instance.badge]!,
  'imageUrl': instance.imageUrl,
  'price': instance.price,
  'availablePacks': instance.availablePacks,
  'thcPercentage': instance.thcPercentage,
  'isIndica': instance.isIndica,
  'isExclusive': instance.isExclusive,
};

const _$VerificationBadgeEnumMap = {
  VerificationBadge.none: 'none',
  VerificationBadge.bronze: 'bronze',
  VerificationBadge.silver: 'silver',
  VerificationBadge.gold: 'gold',
};
