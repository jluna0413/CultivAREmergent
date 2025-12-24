import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';
import '../providers/redemption_provider.dart';

class RedemptionScreen extends ConsumerWidget {
  const RedemptionScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final step = ref.watch(redemptionProvider);

    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: const Text('Redeem Collectible'),
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.close, color: Colors.white),
          onPressed: () => context.pop(),
        ),
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // Main Visual Area
              Expanded(
                flex: 3,
                child: Center(child: _buildVisual(context, ref, step)),
              ),
              const SizedBox(height: 32),
              // Status Text
              Expanded(flex: 2, child: _buildControls(context, ref, step)),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildVisual(
    BuildContext context,
    WidgetRef ref,
    RedemptionStep step,
  ) {
    switch (step) {
      case RedemptionStep.scan:
      case RedemptionStep.verify:
        return Container(
          width: 300,
          height: 300,
          decoration: BoxDecoration(
            border: Border.all(color: Colors.white.withOpacity(0.5), width: 2),
            borderRadius: BorderRadius.circular(24),
          ),
          child: Stack(
            alignment: Alignment.center,
            children: [
              const Icon(
                Icons.qr_code_scanner,
                size: 100,
                color: Colors.white54,
              ),
              if (step == RedemptionStep.scan)
                Container(
                      width: 280,
                      height: 2,
                      decoration: const BoxDecoration(
                        color: Color(0xFF00FF00), // Laser Green
                        boxShadow: [
                          BoxShadow(color: Color(0xFF00FF00), blurRadius: 10),
                        ],
                      ),
                    )
                    .animate(
                      onPlay: (controller) => controller.repeat(reverse: true),
                    )
                    .moveY(begin: -140, end: 140, duration: 2.seconds),
              if (step == RedemptionStep.verify)
                const CircularProgressIndicator(color: Color(0xFF00FF00)),
            ],
          ),
        );
      case RedemptionStep.userSign:
      case RedemptionStep.breederSign:
        return const Icon(
          Icons.fingerprint,
          size: 150,
          color: Colors.blueAccent,
        ).animate().shimmer(duration: 2.seconds);
      case RedemptionStep.completed:
        return const Stack(
          alignment: Alignment.center,
          children: [
            Icon(Icons.inventory_2_outlined, size: 150, color: Colors.amber),
            Icon(Icons.check_circle, size: 60, color: Colors.green),
          ],
        ).animate().scale(duration: 600.ms, curve: Curves.elasticOut);
    }
  }

  Widget _buildControls(
    BuildContext context,
    WidgetRef ref,
    RedemptionStep step,
  ) {
    switch (step) {
      case RedemptionStep.scan:
        return Column(
          children: [
            const Text(
              'Align QR code within frame',
              style: TextStyle(color: Colors.white70, fontSize: 16),
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () =>
                  ref.read(redemptionProvider.notifier).simulateScan(),
              style: ElevatedButton.styleFrom(backgroundColor: Colors.white24),
              child: const Text(
                'Simulate Scan',
                style: TextStyle(color: Colors.white),
              ),
            ),
          ],
        );
      case RedemptionStep.verify:
        return const Text(
          'Verifying Authenticity...',
          style: TextStyle(color: Colors.white, fontSize: 18),
        );
      case RedemptionStep.userSign:
        return Column(
          children: [
            const Text(
              'Item Found: Purple Haze #4',
              style: TextStyle(
                color: Colors.white,
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            const Text(
              'Status: Unredeemed',
              style: TextStyle(color: Colors.greenAccent),
            ),
            const SizedBox(height: 24),
            const Text(
              'Sign to confirm physical receipt:',
              style: TextStyle(color: Colors.white70),
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              onPressed: () => ref.read(redemptionProvider.notifier).signUser(),
              icon: const Icon(Icons.draw, color: Colors.black),
              label: const Text(
                'Sign with Wallet',
                style: TextStyle(color: Colors.black),
              ),
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF00FF00),
                padding: const EdgeInsets.symmetric(
                  horizontal: 32,
                  vertical: 16,
                ),
              ),
            ),
          ],
        );
      case RedemptionStep.breederSign:
        return Column(
          children: [
            const Text(
              'Waiting for Breeder Signature...',
              style: TextStyle(color: Colors.white, fontSize: 18),
            ),
            const SizedBox(height: 16),
            const LinearProgressIndicator(color: Colors.blue),
            const SizedBox(height: 16),
            Text(
              'Broadcasting to CultivAR Network...',
              style: TextStyle(
                color: Colors.white.withOpacity(0.5),
                fontSize: 12,
              ),
            ),
          ],
        );
      case RedemptionStep.completed:
        return Column(
          children: [
            const Text(
              'Redemption Successful!',
              style: TextStyle(
                color: Colors.white,
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            const Text(
              'Asset Burned & Seeds Unlocked',
              style: TextStyle(color: Colors.white70),
            ),
            const SizedBox(height: 32),
            OutlinedButton(
              onPressed: () => context.pop(),
              style: OutlinedButton.styleFrom(
                side: const BorderSide(color: Colors.white),
              ),
              child: const Text(
                'Back to Wallet',
                style: TextStyle(color: Colors.white),
              ),
            ),
          ],
        );
    }
  }
}
