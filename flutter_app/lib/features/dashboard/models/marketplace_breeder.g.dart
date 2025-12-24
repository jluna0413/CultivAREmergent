// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'marketplace_breeder.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$MarketplaceBreederImpl _$$MarketplaceBreederImplFromJson(
  Map<String, dynamic> json,
) => _$MarketplaceBreederImpl(
  id: (json['id'] as num).toInt(),
  userId: (json['user_id'] as num).toInt(),
  currentTier: json['current_tier'] as String? ?? 'Starter',
  monthSales: (json['month_sales'] as num?)?.toInt() ?? 0,
  activeCommissionRate:
      (json['active_commission_rate'] as num?)?.toDouble() ?? 0.25,
  totalRevenue: (json['total_revenue'] as num?)?.toDouble() ?? 0.0,
  isVerified: json['is_verified'] as bool? ?? false,
  storeName: json['store_name'] as String?,
);

Map<String, dynamic> _$$MarketplaceBreederImplToJson(
  _$MarketplaceBreederImpl instance,
) => <String, dynamic>{
  'id': instance.id,
  'user_id': instance.userId,
  'current_tier': instance.currentTier,
  'month_sales': instance.monthSales,
  'active_commission_rate': instance.activeCommissionRate,
  'total_revenue': instance.totalRevenue,
  'is_verified': instance.isVerified,
  'store_name': instance.storeName,
};
