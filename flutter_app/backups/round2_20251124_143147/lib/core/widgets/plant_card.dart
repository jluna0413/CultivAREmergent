/// PlantCard widget for displaying plant information
/// Matches the plant-card design from plants.html and strain.html
library;
// (removed stray library directive)

import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

/// Configuration for plant status indicators
class PlantStatus {
  const PlantStatus({required this.label, required this.color, this.icon});

  final String label;
  final Color color;
  final IconData? icon;
}

/// Configuration for plant metrics/measurements
class PlantMetric {
  const PlantMetric({
    required this.label,
    required this.value,
    this.unit,
    this.icon,
    this.color,
  });

  final String label;
  final String value;
  final String? unit;
  final IconData? icon;
  final Color? color;
}

class PlantCard extends StatelessWidget {
  const PlantCard({
    super.key,
    required this.name,
    required this.strain,
    this.imageUrl,
    this.status,
    this.metrics = const [],
    this.phase,
    this.ageInDays,
    this.location,
    this.onTap,
    this.onEdit,
    this.onDelete,
    this.compact = false,
  });

  final String name;
  final String strain;
  final String? imageUrl;
  final PlantStatus? status;
  final List<PlantMetric> metrics;
  final String? phase;
  final int? ageInDays;
  final String? location;
  final VoidCallback? onTap;
  final VoidCallback? onEdit;
  final VoidCallback? onDelete;
  final bool compact;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Container(
      decoration: BoxDecoration(
        color: isDark
            ? AppTheme.surfaceColor.withValues(alpha: 0.8)
            : const Color(0xB3FFFFFF),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isDark
              ? AppTheme.borderColor.withValues(alpha: 0.2)
              : AppTheme.borderSecondary.withValues(alpha: 0.1),
          width: 1,
        ),
        boxShadow: [AppShadows.shadowMd],
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(16),
          child: Padding(
            padding: compact
                ? const EdgeInsets.all(16)
                : const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Plant Image and Actions Row
                Row(
                  children: [
                    // Plant Image
                    _buildPlantImage(theme),
                    const SizedBox(width: 16),

                    // Plant Info
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          // Plant Name and Status
                          Row(
                            children: [
                              Expanded(
                                child: Text(
                                  name,
                                  style: theme.textTheme.titleMedium?.copyWith(
                                    fontWeight: FontWeight.w600,
                                  ),
                                  maxLines: 1,
                                  overflow: TextOverflow.ellipsis,
                                ),
                              ),
                              if (status != null) ...[
                                const SizedBox(width: 8),
                                _buildStatusBadge(status!),
                              ],
                            ],
                          ),
                          const SizedBox(height: 4),

                          // Strain Name
                          Text(
                            strain,
                            style: theme.textTheme.bodyMedium?.copyWith(
                              color: AppTheme.textSecondary,
                            ),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                          const SizedBox(height: 8),

                          // Plant Details
                          if (!compact) _buildPlantDetails(theme),
                        ],
                      ),
                    ),

                    // Action Menu
                    if (onEdit != null || onDelete != null) ...[
                      const SizedBox(width: 8),
                      _buildActionMenu(),
                    ],
                  ],
                ),

                // Metrics (if not compact)
                if (!compact && metrics.isNotEmpty) ...[
                  const SizedBox(height: 16),
                  _buildMetrics(theme),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildPlantImage(ThemeData theme) {
    return Container(
      width: compact ? 60 : 80,
      height: compact ? 60 : 80,
      decoration: BoxDecoration(
        borderRadius: const BorderRadius.all(Radius.circular(12)),
        border: Border.all(
          color: AppTheme.borderColor.withValues(alpha: 0.2),
          width: 1,
        ),
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(12),
        child: imageUrl != null
            ? Image.network(
                imageUrl!,
                fit: BoxFit.cover,
                errorBuilder: (context, error, stackTrace) {
                  return Container(
                    color: AppTheme.surfaceColor,
                    child: Icon(
                      Icons.grass,
                      size: compact ? 24 : 32,
                      color: AppTheme.textSecondary,
                    ),
                  );
                },
              )
            : Container(
                color: AppTheme.surfaceColor,
                child: Icon(
                  Icons.grass,
                  size: compact ? 24 : 32,
                  color: AppTheme.textSecondary,
                ),
              ),
      ),
    );
  }

  Widget _buildStatusBadge(PlantStatus status) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: status.color.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: status.color.withValues(alpha: 0.2),
          width: 1,
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (status.icon != null) ...[
            Icon(status.icon, color: status.color, size: 12),
            const SizedBox(width: 4),
          ],
          Text(
            status.label,
            style: TextStyle(
              color: status.color,
              fontSize: 11,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPlantDetails(ThemeData theme) {
    return Row(
      children: [
        if (phase != null) ...[
          const Icon(Icons.eco, size: 14, color: AppTheme.textSecondary),
          const SizedBox(width: 4),
          Text(
            phase!,
            style: theme.textTheme.bodySmall?.copyWith(
              color: AppTheme.textSecondary,
            ),
          ),
        ],
        if (ageInDays != null) ...[
          if (phase != null) const SizedBox(width: 12),
          const Icon(
            Icons.calendar_today,
            size: 14,
            color: AppTheme.textSecondary,
          ),
          const SizedBox(width: 4),
          Text(
            '$ageInDays days',
            style: theme.textTheme.bodySmall?.copyWith(
              color: AppTheme.textSecondary,
            ),
          ),
        ],
        if (location != null) ...[
          if (phase != null || ageInDays != null) const SizedBox(width: 12),
          const Icon(
            Icons.location_on,
            size: 14,
            color: AppTheme.textSecondary,
          ),
          const SizedBox(width: 4),
          Expanded(
            child: Text(
              location!,
              style: theme.textTheme.bodySmall?.copyWith(
                color: AppTheme.textSecondary,
              ),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ],
      ],
    );
  }

  Widget _buildMetrics(ThemeData theme) {
    return Row(
      children: metrics.map((metric) {
        return Expanded(child: _buildMetricItem(theme, metric));
      }).toList(),
    );
  }

  Widget _buildMetricItem(ThemeData theme, PlantMetric metric) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: AppTheme.backgroundColor.withValues(alpha: 0.5),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(
          color: AppTheme.borderColor.withValues(alpha: 0.1),
          width: 1,
        ),
      ),
      child: Column(
        children: [
          if (metric.icon != null) ...[
            Icon(
              metric.icon,
              color: metric.color ?? AppTheme.primaryColor,
              size: 16,
            ),
            const SizedBox(height: 4),
          ],
          Text(
            '${metric.value}${metric.unit ?? ""}',
            style: theme.textTheme.bodyMedium?.copyWith(
              fontWeight: FontWeight.w600,
              color: metric.color ?? AppTheme.primaryColor,
            ),
          ),
          const SizedBox(height: 2),
          Text(
            metric.label,
            style: theme.textTheme.bodySmall?.copyWith(
              color: AppTheme.textSecondary,
            ),
            textAlign: TextAlign.center,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
    );
  }

  Widget _buildActionMenu() {
    return PopupMenuButton<String>(
      onSelected: (value) {
        switch (value) {
          case 'edit':
            onEdit?.call();
            break;
          case 'delete':
            onDelete?.call();
            break;
        }
      },
      itemBuilder: (context) => [
        if (onEdit != null)
          const PopupMenuItem(
            value: 'edit',
            child: Row(
              children: [
                Icon(Icons.edit, size: 16),
                SizedBox(width: 8),
                Text('Edit'),
              ],
            ),
          ),
        if (onDelete != null)
          const PopupMenuItem(
            value: 'delete',
            child: Row(
              children: [
                Icon(Icons.delete, size: 16),
                SizedBox(width: 8),
                Text('Delete'),
              ],
            ),
          ),
      ],
      icon: const Icon(
        Icons.more_vert,
        size: 18,
        color: AppTheme.textSecondary,
      ),
    );
  }
}

/// Compact version of PlantCard for lists
class PlantCardCompact extends StatelessWidget {
  const PlantCardCompact({
    super.key,
    required this.name,
    required this.strain,
    this.imageUrl,
    this.status,
    this.onTap,
  });

  final String name;
  final String strain;
  final String? imageUrl;
  final PlantStatus? status;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return PlantCard(
      name: name,
      strain: strain,
      imageUrl: imageUrl,
      status: status,
      onTap: onTap,
      compact: true,
    );
  }
}

/// Plant card with progress tracking
class PlantCardWithProgress extends StatelessWidget {
  const PlantCardWithProgress({
    super.key,
    required this.name,
    required this.strain,
    required this.progress, // 0.0 to 1.0
    this.imageUrl,
    this.status,
    this.onTap,
  });

  final String name;
  final String strain;
  final double progress; // 0.0 to 1.0
  final String? imageUrl;
  final PlantStatus? status;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return PlantCard(
      name: name,
      strain: strain,
      imageUrl: imageUrl,
      status: status,
      onTap: onTap,
      compact: true,
      metrics: [
        PlantMetric(
          label: 'Progress',
          value: '${(progress * 100).toInt()}%',
          icon: Icons.trending_up,
          color: AppTheme.primaryColor,
        ),
      ],
    );
  }
}
