// lib/features/onboarding/logic/pot_placement_logic.dart

/// Represents the physical dimensions of a pot
class PotDimensions {
  final double diameterInches; // Physical size of pot base
  final String label; // e.g., "5 Gal"

  const PotDimensions(this.diameterInches, this.label);

  static const pot1Gal = PotDimensions(6.0, '1 Gal');
  static const pot3Gal = PotDimensions(10.0, '3 Gal');
  static const pot5Gal = PotDimensions(12.0, '5 Gal');
  static const pot10Gal = PotDimensions(
    12.5,
    '10 Gal',
  ); // Similar diameter to 5 Gal, but taller
  static const pot25Gal = PotDimensions(24.0, '25 Gal');

  static List<PotDimensions> get allSizes => [
    pot1Gal,
    pot3Gal,
    pot5Gal,
    pot10Gal,
    pot25Gal,
  ];

  static PotDimensions fromLabel(String label) {
    return allSizes.firstWhere((p) => p.label == label, orElse: () => pot5Gal);
  }
}

/// Represents tent dimensions in inches
class TentDimensions {
  final double widthInches;
  final double depthInches;
  final String label;

  const TentDimensions(this.widthInches, this.depthInches, this.label);

  static const tent2x2 = TentDimensions(24, 24, '2x2');
  static const tent2x4 = TentDimensions(24, 48, '2x4');
  static const tent4x4 = TentDimensions(48, 48, '4x4');
  static const tent4x8 = TentDimensions(48, 96, '4x8');
  static const tent5x5 = TentDimensions(60, 60, '5x5');
  static const tent8x8 = TentDimensions(96, 96, '8x8');

  static List<TentDimensions> get allSizes => [
    tent2x2,
    tent2x4,
    tent4x4,
    tent4x8,
    tent5x5,
    tent8x8,
  ];

  static TentDimensions fromLabel(String label) {
    return allSizes.firstWhere((t) => t.label == label, orElse: () => tent4x4);
  }
}

/// Represents a pot position in the tent layout
class PotPosition {
  final String id;
  final double x; // Center X (inches)
  final double y; // Center Y (inches)
  String potType; // 'fabric', 'air_pruning', 'plastic', etc.

  PotPosition({
    required this.id,
    required this.x,
    required this.y,
    this.potType = 'fabric',
  });

  PotPosition copyWith({String? id, double? x, double? y, String? potType}) {
    return PotPosition(
      id: id ?? this.id,
      x: x ?? this.x,
      y: y ?? this.y,
      potType: potType ?? this.potType,
    );
  }
}

/// Returns the diameter of the "Grow Zone" (Canopy) needed for the pot.
/// CRITICAL: This uses canopy spacing, not physical pot diameter!
/// A 5-gallon pot needs ~24" of grow space for the plant canopy.
double getEffectiveGrowZone(String potLabel) {
  switch (potLabel) {
    case '1 Gal':
      return 12.0; // SOG style - tight spacing
    case '3 Gal':
      return 18.0;
    case '5 Gal':
      return 24.0; // Standard bushy plant
    case '10 Gal':
      return 30.0;
    case '25 Gal':
      return 40.0;
    default:
      return 12.0;
  }
}

/// Calculates pot layout positions using CANOPY SPACING logic
///
/// This ensures realistic plant arrangements:
/// - A 4x4 tent (48"x48") with 5gal pots (24" canopy) = 4 pots (2x2 grid)
/// - A 4x8 tent (48"x96") with 5gal pots (24" canopy) = 8 pots (2x4 grid)
List<PotPosition> calculatePotLayout({
  required TentDimensions tent,
  required PotDimensions pot,
}) {
  List<PotPosition> positions = [];

  // Calculate layout based on Canopy Zone, not just pot base
  double growZoneSize = getEffectiveGrowZone(pot.label);

  // Calculate layout based on Canopy Zone with Smart Margin
  // This prevents pots from touching the absolute edges of the tent (visual clipping)
  // Logic: Try to apply a 2-inch safety margin. If the resulting count is >= 75% of the max count, use it.
  // Otherwise, fallback to max count to avoid wasting too much space.
  
  double margin = 2.0; // 1 inch per side
  
  // Helper to calculate safe count
  int calcSafeDimension(double dim, double zone, double potBase) {
    int maxC = (dim / zone).floor();
    int safeC = ((dim - margin) / zone).floor();
    
    if (maxC <= 0 && dim > potBase) return 1; // Fit one if feasible
    if (maxC == 0) return 0;
    
    // Fallback logic
    if (safeC <= 0 && maxC > 0) return maxC;

    double ratio = safeC / maxC;
    // Lowered threshold slightly just to be safe, but 0.75 is standard
    if (ratio >= 0.75) {
      return safeC;
    }
    return maxC;
  }

  int cols = calcSafeDimension(tent.widthInches, growZoneSize, pot.diameterInches);
  int rows = calcSafeDimension(tent.depthInches, growZoneSize, pot.diameterInches);

  // Fallback: Ensure at least 1 pot fits if tent > pot base
  if (cols == 0 && tent.widthInches > pot.diameterInches) cols = 1;
  if (rows == 0 && tent.depthInches > pot.diameterInches) rows = 1;

  if (cols <= 0 || rows <= 0) return [];

  // Center the grid in the tent
  double totalGridWidth = cols * growZoneSize;
  double totalGridDepth = rows * growZoneSize;

  double startX = (tent.widthInches - totalGridWidth) / 2 + (growZoneSize / 2);
  double startY = (tent.depthInches - totalGridDepth) / 2 + (growZoneSize / 2);

  int counter = 1;

  for (int r = 0; r < rows; r++) {
    for (int c = 0; c < cols; c++) {
      positions.add(
        PotPosition(
          id: 'pot_$counter',
          x: startX + (c * growZoneSize),
          y: startY + (r * growZoneSize),
        ),
      );
      counter++;
    }
  }

  return positions;
}

/// Pot type options for user selection
enum PotType {
  fabric('Fabric'),
  airPruning('Air Pruning'),
  plastic('Plastic'),
  terracotta('Terracotta'),
  smartPot('Smart Pot');

  final String displayName;
  const PotType(this.displayName);
}
