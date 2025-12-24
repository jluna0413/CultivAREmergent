import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../providers/breeder_provider.dart';
import '../providers/sales_provider.dart';
import '../widgets/stat_card.dart';
import '../widgets/sales_chart.dart';
import 'package:intl/intl.dart';
import 'dart:ui' as ui;

class BreederDashboardScreen extends ConsumerWidget {
  const BreederDashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final breederAsync = ref.watch(breederProfileProvider);
    final salesHistoryAsync = ref.watch(salesHistoryProvider(30));

    return Scaffold(
      backgroundColor: const Color(0xFFF5F5F7), // Apple Off-White
      body: breederAsync.when(
        data: (breeder) => CustomScrollView(
          slivers: [
            SliverAppBar.large(
              title: const Text(
                'Dashboard',
                style: TextStyle(
                  color: Colors.black,
                  fontWeight: FontWeight.bold,
                ),
              ),
              backgroundColor: Colors.white,
              surfaceTintColor: Colors.transparent,
              actions: [
                IconButton(
                  icon: const Icon(
                    Icons.qr_code_scanner,
                    color: Color(0xFF34C759),
                  ),
                  onPressed: () => context.pushNamed('redemption'),
                  tooltip: 'Scan Redemption',
                ),
                IconButton(
                  icon: const Icon(
                    Icons.settings_outlined,
                    color: Colors.black,
                  ),
                  onPressed: () {}, // Settings
                ),
              ],
            ),
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Welcome & Tier
                    Text(
                      'Welcome back, ${breeder.storeName ?? "Breeder"}',
                      style: TextStyle(
                        fontSize: 18,
                        color: Colors.grey[600],
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    const SizedBox(height: 24),

                    // Stats Grid
                    GridView.count(
                      crossAxisCount: 2,
                      crossAxisSpacing: 16,
                      mainAxisSpacing: 16,
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      childAspectRatio: 1.4,
                      children: [
                        StatCard(
                          title: 'Total Revenue',
                          value: NumberFormat.currency(
                            symbol: '\$',
                          ).format(breeder.totalRevenue),
                          icon: Icons.attach_money,
                        ),
                        StatCard(
                          title: 'Commission Rate',
                          value:
                              '${(breeder.activeCommissionRate * 100).toStringAsFixed(1)}%',
                          subtitle: 'Tier: ${breeder.currentTier}',
                          gradientColors: _getTierGradient(breeder.currentTier),
                          icon: Icons.trending_up,
                        ),
                        StatCard(
                          title: 'Month Sales',
                          value: '\$${breeder.monthSales}',
                          icon: Icons.calendar_today,
                        ),
                        const StatCard(
                          title: 'Active Listings',
                          value: '12', // Mock for now
                          icon: Icons.storefront,
                        ),
                      ],
                    ),

                    const SizedBox(height: 32),

                    // Sales Chart
                    const Text(
                      'Performance (30 Days)',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 16),
                    salesHistoryAsync.when(
                      data: (history) => SalesChart(dailyData: history),
                      loading: () =>
                          const Center(child: CircularProgressIndicator()),
                      error: (err, stack) => Container(
                        height: 200,
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: Center(child: Text('Error loading chart: $err')),
                      ),
                    ),

                    const SizedBox(height: 32),

                    // Quick Actions
                    const Text(
                      'Quick Actions',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 16),
                    _buildQuickAction(
                      icon: Icons.add_circle,
                      label: 'Mint G-NFT',
                      color: const Color(0xFF34C759),
                      onTap: () {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text(
                              'Minting Wizard Coming Soon (Phase 6.2)',
                            ),
                          ),
                        );
                      },
                    ),
                    const SizedBox(height: 12),
                    _buildQuickAction(
                      icon: Icons.inventory_2,
                      label: 'Manage Inventory',
                      color: Colors.blueAccent,
                      onTap: () {},
                    ),
                    const SizedBox(height: 32),
                  ],
                ),
              ),
            ),
          ],
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Error: $err')),
      ),
    );
  }

  List<Color> _getTierGradient(String tier) {
    switch (tier) {
      case 'Market Maker':
        return [const Color(0xFF34C759), const Color(0xFFD1FAE5)]; // Green/Mint
      case 'Shaker':
        return [const Color(0xFF5856D6), const Color(0xFFE5E5EA)]; // Purple
      case 'Mover':
        return [const Color(0xFF007AFF), const Color(0xFFE5F4FF)]; // Blue
      default: // Starter
        return [const Color(0xFFFF9500), const Color(0xFFFFF5E5)]; // Orange
    }
  }

  Widget _buildQuickAction({
    required IconData icon,
    required String label,
    required Color color,
    required VoidCallback onTap,
  }) {
    return InkWell(
      onTap: onTap,
      child: Container(
        height: 60,
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.03),
              blurRadius: 10,
              offset: const ui.Offset(0, 2),
            ),
          ],
        ),
        child: Row(
          children: [
            const SizedBox(width: 16),
            Icon(icon, color: color, size: 28),
            const SizedBox(width: 16),
            Text(
              label,
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
            ),
            const Spacer(),
            Icon(Icons.chevron_right, color: Colors.grey[400]),
            const SizedBox(width: 16),
          ],
        ),
      ),
    );
  }
}
