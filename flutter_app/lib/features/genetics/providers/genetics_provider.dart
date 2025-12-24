import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../models/strain.dart';
import '../models/verification_badge.dart';

part 'genetics_provider.g.dart';

@riverpod
class GeneticsLibrary extends _$GeneticsLibrary {
  @override
  Future<List<Strain>> build() async {
    // Simulate network delay
    await Future.delayed(const Duration(milliseconds: 800));
    return _getMockStrains();
  }

  // Temporary Mock Data for UI Verification
  List<Strain> _getMockStrains() {
    return [
      const Strain(
        id: '1',
        name: 'Blue Dream',
        breederName: 'Humboldt Seed Org',
        badge: VerificationBadge.gold, // Neuro-Verified
        imageUrl:
            'https://images.leafly.com/flower-images/blue-dream.png', // Placeholder
        thcPercentage: 18.5,
        cbdPercentage: 0.1,
        flowerTimeWeeks: 9,
        isSativa: true,
        price: 45.0,
        availableStock: 120,
        parent1Name: 'Blueberry',
        parent2Name: 'Haze',
      ),
      const Strain(
        id: '2',
        name: 'OG Kush',
        breederName: 'DNA Genetics',
        badge: VerificationBadge.silver, // Community Verified
        imageUrl: 'https://images.leafly.com/flower-images/og-kush.png',
        thcPercentage: 24.0,
        cbdPercentage: 0.5,
        flowerTimeWeeks: 8,
        isIndica: true,
        price: 55.0,
        availableStock: 50,
      ),
      const Strain(
        id: '3',
        name: 'White Widow',
        breederName: 'Green House Seeds',
        badge: VerificationBadge.bronze, // Breeder Verified
        imageUrl: 'https://images.leafly.com/flower-images/white-widow.png',
        thcPercentage: 20.0,
        cbdPercentage: 0.8,
        flowerTimeWeeks: 9,
        isSativa: true,
        isIndica: true, // Hybrid
        price: 35.0,
        availableStock: 200,
      ),
      const Strain(
        id: '4',
        name: 'Unknown Bagseed',
        breederName: 'Unknown',
        badge: VerificationBadge.none, // Unverified
        imageUrl:
            'https://images.leafly.com/flower-images/granddaddy-purple.png',
        thcPercentage: 15.0,
        cbdPercentage: 1.0,
        flowerTimeWeeks: 10,
        isIndica: true,
        price: 15.0,
        availableStock: 10,
      ),
    ];
  }
}
