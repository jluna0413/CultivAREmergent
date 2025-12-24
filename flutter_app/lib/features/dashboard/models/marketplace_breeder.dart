import 'package:freezed_annotation/freezed_annotation.dart';

part 'marketplace_breeder.freezed.dart';
part 'marketplace_breeder.g.dart';

@freezed
class MarketplaceBreeder with _$MarketplaceBreeder {
  const factory MarketplaceBreeder({
    required int id,
    @JsonKey(name: 'user_id') required int userId,
    @JsonKey(name: 'current_tier') @Default('Starter') String currentTier,
    @JsonKey(name: 'month_sales') @Default(0) int monthSales,
    @JsonKey(name: 'active_commission_rate')
    @Default(0.25)
    double activeCommissionRate,
    @JsonKey(name: 'total_revenue') @Default(0.0) double totalRevenue,
    @JsonKey(name: 'is_verified') @Default(false) bool isVerified,
    @JsonKey(name: 'store_name') String? storeName,
  }) = _MarketplaceBreeder;

  factory MarketplaceBreeder.fromJson(Map<String, dynamic> json) =>
      _$MarketplaceBreederFromJson(json);
}
