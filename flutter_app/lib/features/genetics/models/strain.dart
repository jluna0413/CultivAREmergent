import 'package:freezed_annotation/freezed_annotation.dart';
import 'verification_badge.dart';

part 'strain.freezed.dart';
part 'strain.g.dart';

@freezed
class Strain with _$Strain {
  const factory Strain({
    required String id,
    required String name,
    required String breederName,
    @Default(VerificationBadge.none) VerificationBadge badge,
    required String imageUrl,
    required double thcPercentage,
    required double cbdPercentage,
    required int flowerTimeWeeks,
    @Default(false) bool isIndica,
    @Default(false) bool isSativa,
    @Default(0.0) double price, // G-NFT Price
    @Default(0) int availableStock,
    String? parent1Name,
    String? parent2Name,
  }) = _Strain;

  factory Strain.fromJson(Map<String, dynamic> json) => _$StrainFromJson(json);
}
