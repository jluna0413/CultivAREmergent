/// Import the actual sensors provider implementation
library;

import '../providers/sensors_provider.dart';

/// Backwards-compatible alias (some callsites expect `sensorsNotifierProvider`)
final sensorsProvider = sensorsNotifierProvider;
