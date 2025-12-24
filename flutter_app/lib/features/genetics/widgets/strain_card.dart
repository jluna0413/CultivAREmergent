import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import '../../../../core/theme/app_theme.dart';
import '../models/strain.dart';
import '../models/verification_badge.dart';

class StrainCard extends StatelessWidget {
  final Strain strain;
  final VoidCallback? onTap;

  const StrainCard({super.key, required this.strain, this.onTap});

  @override
  Widget build(BuildContext context) {
    // Determine badge color/icon from the enhanced enum
    final badge = strain.badge;
    final isVerified = badge.isVerified;

    return GestureDetector(
      onTap: onTap,
      child: Container(
        decoration: BoxDecoration(
          color: AppTheme.getSurfaceColor(context),
          borderRadius: BorderRadius.circular(18),
          boxShadow: AppShadows.card,
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // IMAGE SECTION with Badge Overlay
            Expanded(
              flex: 5, // 50% image
              child: Stack(
                fit: StackFit.expand,
                children: [
                  ClipRRect(
                    borderRadius: const BorderRadius.vertical(
                      top: Radius.circular(18),
                    ),
                    child: CachedNetworkImage(
                      imageUrl: strain.imageUrl,
                      fit: BoxFit.cover,
                      placeholder: (context, url) => Container(
                        color: Colors.grey[200],
                        child: const Center(
                          child: CircularProgressIndicator.adaptive(),
                        ),
                      ),
                      errorWidget: (context, url, error) => Container(
                        color: Colors.grey[300],
                        child: const Icon(
                          Icons.image_not_supported,
                          color: Colors.grey,
                        ),
                      ),
                    ),
                  ),
                  // Verification Badge Overlay
                  if (isVerified)
                    Positioned(
                      top: 8,
                      right: 8,
                      child: Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 8,
                          vertical: 4,
                        ),
                        decoration: BoxDecoration(
                          color: Colors.black.withOpacity(
                            0.7,
                          ), // Semi-transparent black backdrop
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(
                            color: badge.color.withOpacity(0.5),
                            width: 1,
                          ),
                          boxShadow: [
                            BoxShadow(
                              color: badge.glowColor,
                              blurRadius: 8,
                              spreadRadius: 1,
                            ),
                          ],
                        ),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(badge.icon, color: badge.color, size: 14),
                            const SizedBox(width: 4),
                            Text(
                              badge.label,
                              style: const TextStyle(
                                color: Colors.white,
                                fontSize: 10,
                                fontWeight: FontWeight.bold,
                                letterSpacing: 0.5,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                ],
              ),
            ),

            // INFO SECTION (Apple Style: Minimal, Clean Typography)
            Expanded(
              flex: 4,
              child: Padding(
                padding: const EdgeInsets.all(12.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Breeder Name (Subtext - Apple Eyebrow Style)
                        Text(
                          strain.breederName.toUpperCase(),
                          style: TextStyle(
                            color: AppTheme.getTextSecondary(context),
                            fontSize: 10,
                            fontWeight: FontWeight.w700, // Slightly bolder
                            letterSpacing: 1.2, // Increased from 0.8
                          ),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                        const SizedBox(height: 4),
                        // Strain Name (Headline - Apple Title Style)
                        Text(
                          strain.name,
                          style: Theme.of(context).textTheme.titleMedium
                              ?.copyWith(
                                fontWeight: FontWeight.w700,
                                fontSize: 16,
                                letterSpacing:
                                    -0.5, // Tight Apple tracking validated
                                color: const Color(
                                  0xFF1D1D1F,
                                ), // Explicit Apple Text Color
                              ),
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ],
                    ),

                    // Metadata Grid (THC / Type / Time)
                    Row(
                      children: [
                        _buildMetdataChip(
                          context,
                          "${strain.thcPercentage}% THC",
                          Colors.purple.shade400,
                        ),
                        const SizedBox(width: 6),
                        _buildMetdataChip(
                          context,
                          strain.isIndica ? "Indica" : "Sativa",
                          Colors.green.shade600,
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMetdataChip(BuildContext context, String label, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Text(
        label,
        style: TextStyle(
          color: color,
          fontSize: 9,
          fontWeight: FontWeight.w600,
        ),
      ),
    );
  }
}
