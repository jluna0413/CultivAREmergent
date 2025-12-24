import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'redemption_provider.g.dart';

enum RedemptionStep {
  scan,
  verify, // Verifying the scanned code
  userSign,
  breederSign,
  completed,
}

@riverpod
class Redemption extends _$Redemption {
  @override
  RedemptionStep build() {
    return RedemptionStep.scan;
  }

  void simulateScan() async {
    state = RedemptionStep.verify;
    await Future.delayed(const Duration(seconds: 2)); // Sim network
    state = RedemptionStep.userSign;
  }

  void signUser() async {
    // Simulating wallet signature
    await Future.delayed(const Duration(seconds: 1));
    state = RedemptionStep.breederSign;
    // Auto-trigger breeder sign simulation for demo
    _simulateBreederResponse();
  }

  void _simulateBreederResponse() async {
    await Future.delayed(const Duration(seconds: 3)); // Wait for "breeder"
    state = RedemptionStep.completed;
  }

  void reset() {
    state = RedemptionStep.scan;
  }
}
