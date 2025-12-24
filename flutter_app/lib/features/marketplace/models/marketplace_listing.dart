import 'package:freezed_annotation/freezed_annotation.dart';
import '../../genetics/models/verification_badge.dart';

part 'marketplace_listing.freezed.dart';
part 'marketplace_listing.g.dart';

@freezed
class MarketplaceListing with _$MarketplaceListing {
  const factory MarketplaceListing({
    required String id,
    required String strainName,
    required String breederName,
    @Default(VerificationBadge.none) VerificationBadge badge,
    required String imageUrl,
    required double price,
    required int availablePacks,
    required double thcPercentage,
    required bool isIndica,
    @Default(false) bool isExclusive,
  }) = _MarketplaceListing;

  factory MarketplaceListing.fromJson(Map<String, dynamic> json) =>
      _$MarketplaceListingFromJson(json);
}
