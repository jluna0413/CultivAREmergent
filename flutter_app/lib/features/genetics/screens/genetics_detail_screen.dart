import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_theme.dart';
import '../models/strain.dart';
import '../providers/genetics_provider.dart';

class GeneticsDetailScreen extends ConsumerWidget {
  final String strainId;

  const GeneticsDetailScreen({super.key, required this.strainId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // In a real app, use .family or select specific ID.
    // For mock MVP, we just find it in the list.
    final strainAsync = ref.watch(geneticsLibraryProvider);

    return Scaffold(
      backgroundColor: AppTheme.getBackgroundColor(context),
      body: strainAsync.when(
        data: (strains) {
          final strain = strains.firstWhere(
            (s) => s.id == strainId,
            orElse: () => strains.first, // Fallback for dev
          );
          return _buildContent(context, strain);
        },
        loading: () =>
            const Center(child: CircularProgressIndicator.adaptive()),
        error: (err, stack) => Center(child: Text('Error: $err')),
      ),
    );
  }

  Widget _buildContent(BuildContext context, Strain strain) {
    return CustomScrollView(
      slivers: [
        // 1. Large Collapsible Header
        SliverAppBar.large(
          expandedHeight: 400,
          stretch: true,
          backgroundColor: AppTheme.getSurfaceColor(context),
          flexibleSpace: FlexibleSpaceBar(
            title: Text(
              strain.name,
              style: TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.bold,
                shadows: [
                  Shadow(blurRadius: 10, color: Colors.black.withOpacity(0.5)),
                ],
              ),
            ),
            background: Stack(
              fit: StackFit.expand,
              children: [
                CachedNetworkImage(
                  imageUrl: strain.imageUrl,
                  fit: BoxFit.cover,
                ),
                // Gradient Overlay for Text Readability
                DecoratedBox(
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                      colors: [
                        Colors.transparent,
                        Colors.black.withOpacity(0.6),
                      ],
                      stops: const [0.6, 1.0],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),

        // 2. Content Sections
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // BADGE HEADER
                Row(
                  children: [
                    Icon(
                      strain.badge.icon,
                      color: strain.badge.color,
                      size: 24,
                    ),
                    const SizedBox(width: 8),
                    Text(
                      strain.badge.label.toUpperCase(),
                      style: TextStyle(
                        color: strain.badge.color,
                        fontWeight: FontWeight.bold,
                        letterSpacing: 1.2,
                        fontSize: 12,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 24),

                // DESCRIPTION / DETAILS
                _buildSectionTitle(context, "About"),
                Text(
                  "A legendary strain from ${strain.breederName}. Known for its high THC content of ${strain.thcPercentage}% and consistent growth patterns.",
                  style: TextStyle(
                    fontSize: 16,
                    height: 1.5,
                    color: AppTheme.getTextSecondary(context),
                  ),
                ),
                const SizedBox(height: 32),

                // METRICS GRID
                _buildSectionTitle(context, "Genetic Profile"),
                Row(
                  children: [
                    _buildMetricCard(
                      context,
                      "THC",
                      "${strain.thcPercentage}%",
                    ),
                    const SizedBox(width: 12),
                    _buildMetricCard(
                      context,
                      "Flowering",
                      "${strain.flowerTimeWeeks} wks",
                    ),
                    const SizedBox(width: 12),
                    _buildMetricCard(
                      context,
                      "Type",
                      strain.isSativa ? "Sativa" : "Indica",
                    ),
                  ],
                ),
                const SizedBox(height: 32),

                // LINEAGE PLACEHOLDER
                _buildSectionTitle(context, "Lineage"),
                if (strain.parent1Name != null || strain.parent2Name != null)
                  Row(
                    children: [
                      if (strain.parent1Name != null)
                        _buildParentChip(context, strain.parent1Name!),
                      if (strain.parent1Name != null &&
                          strain.parent2Name != null)
                        const Padding(
                          padding: EdgeInsets.symmetric(horizontal: 12.0),
                          child: Icon(
                            Icons.close,
                            size: 16,
                            color: Colors.grey,
                          ),
                        ),
                      if (strain.parent2Name != null)
                        _buildParentChip(context, strain.parent2Name!),
                    ],
                  )
                else
                  Container(
                    height: 80,
                    width: double.infinity,
                    decoration: BoxDecoration(
                      color: AppTheme.getSurfaceColor(context),
                      borderRadius: BorderRadius.circular(18),
                      boxShadow: AppShadows.card,
                    ),
                    child: const Center(
                      child: Text(
                        "Ancestry tree loading...",
                        style: TextStyle(color: Colors.grey),
                      ),
                    ),
                  ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildSectionTitle(BuildContext context, String title) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Text(
        title,
        style: Theme.of(context).textTheme.titleLarge?.copyWith(
          fontWeight: FontWeight.bold,
          letterSpacing: -0.5,
        ),
      ),
    );
  }

  Widget _buildMetricCard(BuildContext context, String label, String value) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: AppTheme.getSurfaceColor(context),
          borderRadius: BorderRadius.circular(16),
          boxShadow: AppShadows.card,
        ),
        child: Column(
          children: [
            Text(
              label.toUpperCase(),
              style: const TextStyle(
                fontSize: 10,
                fontWeight: FontWeight.w600,
                color: Colors.grey,
                letterSpacing: 1.0,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              value,
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildParentChip(BuildContext context, String name) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 12),
        decoration: BoxDecoration(
          color: AppTheme.getSurfaceColor(context),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: Colors.white10),
          boxShadow: AppShadows.card,
        ),
        child: Text(
          name,
          textAlign: TextAlign.center,
          style: const TextStyle(
            fontWeight: FontWeight.bold,
            letterSpacing: -0.2,
          ),
        ),
      ),
    );
  }
}
