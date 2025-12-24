import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../core/theme/app_theme.dart';
import '../providers/marketplace_provider.dart';
import '../widgets/listing_card.dart';

class MarketplaceScreen extends ConsumerWidget {
  const MarketplaceScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final listingsAsync = ref.watch(marketplaceListingsProvider);

    return Scaffold(
      backgroundColor: AppTheme.getBackgroundColor(context),
      body: CustomScrollView(
        slivers: [
          // Large Apple-Style Header
          SliverAppBar.large(
            title: const Text(
              "Marketplace",
              style: TextStyle(
                letterSpacing: -1.0,
                fontWeight: FontWeight.bold,
              ),
            ),
            backgroundColor: AppTheme.getBackgroundColor(context),
            surfaceTintColor: Colors.transparent, // Disable Material 3 tint
            actions: [
              IconButton(
                icon: const Icon(Icons.qr_code_scanner),
                tooltip: 'Redeem Coin',
                onPressed: () {
                  context.pushNamed('redemption');
                },
              ),
              IconButton(
                icon: const Icon(Icons.shopping_bag_outlined),
                tooltip: 'Checkout',
                onPressed: () {
                  context.pushNamed('checkout');
                },
              ),
            ],
          ),

          // Search Bar (Pinned)
          SliverPersistentHeader(
            pinned: true,
            delegate: _SliverSearchBarDelegate(
              minHeight: 60,
              maxHeight: 60,
              child: Container(
                color: AppTheme.getBackgroundColor(context),
                padding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 8,
                ),
                child: Container(
                  decoration: BoxDecoration(
                    color: AppTheme.getSurfaceColor(context),
                    borderRadius: BorderRadius.circular(12),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.05),
                        blurRadius: 10,
                        offset: const Offset(0, 2),
                      ),
                    ],
                  ),
                  child: const TextField(
                    decoration: InputDecoration(
                      hintText: "Search seeds, breeders, gears...",
                      prefixIcon: Icon(Icons.search, color: Colors.grey),
                      border: InputBorder.none,
                      contentPadding: EdgeInsets.symmetric(vertical: 12),
                    ),
                  ),
                ),
              ),
            ),
          ),

          // Content Grid
          listingsAsync.when(
            data: (listings) => SliverPadding(
              padding: const EdgeInsets.all(16),
              sliver: SliverGrid(
                gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
                  maxCrossAxisExtent: 220,
                  mainAxisSpacing: 16,
                  crossAxisSpacing: 16,
                  childAspectRatio: 0.65, // Slightly taller for buttons
                ),
                delegate: SliverChildBuilderDelegate((context, index) {
                  final listing = listings[index];
                  return ListingCard(
                    listing: listing,
                    onTap: () {
                      // Navigate to detail (re-using genetics detail for now, or new marketplace detail)
                      // For MVP, we route to standard genetics detail
                      context.pushNamed(
                        'strain-detail',
                        pathParameters: {'id': listing.id},
                      );
                    },
                    onBuy: () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text("Added ${listing.strainName} to Cart"),
                        ),
                      );
                    },
                  );
                }, childCount: listings.length),
              ),
            ),
            loading: () => const SliverFillRemaining(
              child: Center(child: CircularProgressIndicator.adaptive()),
            ),
            error: (err, stack) =>
                SliverFillRemaining(child: Center(child: Text('Error: $err'))),
          ),
        ],
      ),
    );
  }
}

class _SliverSearchBarDelegate extends SliverPersistentHeaderDelegate {
  final double minHeight;
  final double maxHeight;
  final Widget child;

  _SliverSearchBarDelegate({
    required this.minHeight,
    required this.maxHeight,
    required this.child,
  });

  @override
  double get minExtent => minHeight;
  @override
  double get maxExtent => maxHeight;

  @override
  Widget build(
    BuildContext context,
    double shrinkOffset,
    bool overlapsContent,
  ) {
    return SizedBox.expand(child: child);
  }

  @override
  bool shouldRebuild(_SliverSearchBarDelegate oldDelegate) {
    return maxHeight != oldDelegate.maxHeight ||
        minHeight != oldDelegate.minHeight ||
        child != oldDelegate.child;
  }
}
