/// StrainCard widget for displaying strain information
/// Matches the strain-card design from strains.html
library;
// (removed stray library directive)

import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

/// Configuration for strain genetics information
class StrainGenetics {
  const StrainGenetics({
    required this.indica,
    required this.sativa,
    required this.ruderalis,
  });

  final double indica; // 0.0 to 1.0
  final double sativa; // 0.0 to 1.0
  final double ruderalis; // 0.0 to 1.0

  String get displayText {
    if (indica >= 0.8) return 'Mostly Indica';
    if (sativa >= 0.8) return 'Mostly Sativa';
    if (ruderalis >= 0.3) return 'Auto-flowering';
    return 'Balanced Hybrid';
  }

  Color get primaryColor {
    if (indica >= 0.8) return const Color(0xFF8B5CF6); // Purple for Indica
    if (sativa >= 0.8) return const Color(0xFF10B981); // Green for Sativa
    return const Color(0xFFF59E0B); // Orange for Hybrid
  }
}

/// Configuration for strain effects
class StrainEffects {
  const StrainEffects({
    required this.positive,
    required this.negative,
    this.medical = const [],
  });

  final List<String> positive;
  final List<String> negative;
  final List<String> medical;
}

class StrainCard extends StatelessWidget {
  const StrainCard({
    super.key,
    required this.name,
    required this.genetics,
    this.description,
    this.effects,
    this.thc,
    this.cbd,
    this.floweringTime,
    this.yield,
    this.difficulty,
    this.imageUrl,
    this.onTap,
    this.onEdit,
    this.onFavorite,
    this.isFavorite = false,
    this.compact = false,
  });

  final String name;
  final StrainGenetics genetics;
  final String? description;
  final StrainEffects? effects;
  final double? thc;
  final double? cbd;
  final String? floweringTime;
  final String? yield;
  final String? difficulty;
  final String? imageUrl;
  final VoidCallback? onTap;
  final VoidCallback? onEdit;
  final VoidCallback? onFavorite;
  final bool isFavorite;
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
                // Strain Header
                Row(
                  children: [
                    // Strain Image
                    _buildStrainImage(theme),
                    const SizedBox(width: 16),

                    // Strain Info
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          // Strain Name and Favorite
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
                              if (onFavorite != null) ...[
                                const SizedBox(width: 8),
                                IconButton(
                                  onPressed: onFavorite,
                                  icon: Icon(
                                    isFavorite
                                        ? Icons.favorite
                                        : Icons.favorite_border,
                                    color: isFavorite
                                        ? AppTheme.error
                                        : AppTheme.textSecondary,
                                    size: 20,
                                  ),
                                  padding: EdgeInsets.zero,
                                  constraints: const BoxConstraints(
                                    minWidth: 32,
                                    minHeight: 32,
                                  ),
                                ),
                              ],
                            ],
                          ),
                          const SizedBox(height: 4),

                          // Genetics
                          _buildGeneticsDisplay(theme),
                          if (!compact) ...[
                            const SizedBox(height: 8),
                            _buildBasicStats(theme),
                          ],
                        ],
                      ),
                    ),

                    // Action Menu
                    if (onEdit != null) ...[
                      const SizedBox(width: 8),
                      _buildActionMenu(),
                    ],
                  ],
                ),

                // Description (if not compact)
                if (!compact && description != null) ...[
                  const SizedBox(height: 16),
                  Text(
                    description!,
                    style: theme.textTheme.bodyMedium?.copyWith(
                      color: AppTheme.textSecondary,
                    ),
                    maxLines: 3,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],

                // Effects and Stats
                if (!compact) ...[
                  if (effects != null) ...[
                    const SizedBox(height: 16),
                    _buildEffects(theme),
                  ],
                  if (thc != null || cbd != null || floweringTime != null) ...[
                    const SizedBox(height: 16),
                    _buildDetailedStats(theme),
                  ],
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildStrainImage(ThemeData theme) {
    return Container(
      width: compact ? 60 : 80,
      height: compact ? 60 : 80,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(12),
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
                      Icons.science,
                      size: compact ? 24 : 32,
                      color: genetics.primaryColor,
                    ),
                  );
                },
              )
            : Container(
                color: AppTheme.surfaceColor,
                child: Icon(
                  Icons.science,
                  size: compact ? 24 : 32,
                  color: genetics.primaryColor,
                ),
              ),
      ),
    );
  }

  Widget _buildGeneticsDisplay(ThemeData theme) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          genetics.displayText,
          style: theme.textTheme.bodyMedium?.copyWith(
            fontWeight: FontWeight.w500,
            color: genetics.primaryColor,
          ),
        ),
        const SizedBox(height: 8),
        _buildGeneticsBars(theme),
      ],
    );
  }

  Widget _buildGeneticsBars(ThemeData theme) {
    return Column(
      children: [
        _buildGeneticsBar(
          'Indica',
          genetics.indica,
          const Color(0xFF8B5CF6),
          theme,
        ),
        const SizedBox(height: 4),
        _buildGeneticsBar(
          'Sativa',
          genetics.sativa,
          const Color(0xFF10B981),
          theme,
        ),
        if (genetics.ruderalis > 0) ...[
          const SizedBox(height: 4),
          _buildGeneticsBar(
            'Ruderalis',
            genetics.ruderalis,
            const Color(0xFFF59E0B),
            theme,
          ),
        ],
      ],
    );
  }

  Widget _buildGeneticsBar(
    String label,
    double value,
    Color color,
    ThemeData theme,
  ) {
    return Row(
      children: [
        SizedBox(
          width: 60,
          child: Text(
            label,
            style: theme.textTheme.bodySmall?.copyWith(
              color: AppTheme.textSecondary,
            ),
          ),
        ),
        const SizedBox(width: 8),
        Expanded(
          child: Container(
            height: 6,
            decoration: BoxDecoration(
              color: AppTheme.backgroundColor.withValues(alpha: 0.5),
              borderRadius: BorderRadius.circular(3),
            ),
            child: Stack(
              children: [
                Positioned.fill(
                  child: Container(
                    decoration: BoxDecoration(
                      color: color.withValues(alpha: 0.3),
                      borderRadius: BorderRadius.circular(3),
                    ),
                  ),
                ),
                FractionallySizedBox(
                  widthFactor: value.clamp(0.0, 1.0),
                  child: Container(
                    decoration: BoxDecoration(
                      color: color,
                      borderRadius: BorderRadius.circular(3),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
        const SizedBox(width: 8),
        Text(
          '${(value * 100).toInt()}%',
          style: theme.textTheme.bodySmall?.copyWith(
            fontWeight: FontWeight.w500,
          ),
        ),
      ],
    );
  }

  Widget _buildBasicStats(ThemeData theme) {
    return Row(
      children: [
        if (thc != null) ...[
          const Icon(
            Icons.local_fire_department,
            size: 14,
            color: AppTheme.warning,
          ),
          const SizedBox(width: 4),
          Text(
            'THC ${thc!.toStringAsFixed(1)}%',
            style: theme.textTheme.bodySmall?.copyWith(
              color: AppTheme.textSecondary,
            ),
          ),
        ],
        if (cbd != null) ...[
          if (thc != null) const SizedBox(width: 12),
          const Icon(Icons.medical_services, size: 14, color: AppTheme.success),
          const SizedBox(width: 4),
          Text(
            'CBD ${cbd!.toStringAsFixed(1)}%',
            style: theme.textTheme.bodySmall?.copyWith(
              color: AppTheme.textSecondary,
            ),
          ),
        ],
        if (floweringTime != null) ...[
          if (thc != null || cbd != null) const SizedBox(width: 12),
          const Icon(
            Icons.calendar_today,
            size: 14,
            color: AppTheme.textSecondary,
          ),
          const SizedBox(width: 4),
          Text(
            floweringTime!,
            style: theme.textTheme.bodySmall?.copyWith(
              color: AppTheme.textSecondary,
            ),
          ),
        ],
      ],
    );
  }

  Widget _buildEffects(ThemeData theme) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Effects',
          style: theme.textTheme.titleSmall?.copyWith(
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 8),
        if (effects!.positive.isNotEmpty) ...[
          Text(
            'Positive:',
            style: theme.textTheme.bodySmall?.copyWith(
              fontWeight: FontWeight.w500,
              color: AppTheme.success,
            ),
          ),
          const SizedBox(height: 4),
          Wrap(
            spacing: 8,
            runSpacing: 4,
            children: effects!.positive.take(3).map((effect) {
              return _buildEffectChip(effect, AppTheme.success, theme);
            }).toList(),
          ),
        ],
        if (effects!.negative.isNotEmpty) ...[
          const SizedBox(height: 8),
          Text(
            'Negative:',
            style: theme.textTheme.bodySmall?.copyWith(
              fontWeight: FontWeight.w500,
              color: AppTheme.error,
            ),
          ),
          const SizedBox(height: 4),
          Wrap(
            spacing: 8,
            runSpacing: 4,
            children: effects!.negative.take(2).map((effect) {
              return _buildEffectChip(effect, AppTheme.error, theme);
            }).toList(),
          ),
        ],
      ],
    );
  }

  Widget _buildEffectChip(String text, Color color, ThemeData theme) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withValues(alpha: 0.2), width: 1),
      ),
      child: Text(
        text,
        style: TextStyle(
          color: color,
          fontSize: 11,
          fontWeight: FontWeight.w500,
        ),
      ),
    );
  }

  Widget _buildDetailedStats(ThemeData theme) {
    return Row(
      children: [
        if (thc != null) ...[
          Expanded(
            child: _buildStatItem(
              'THC',
              '${thc!.toStringAsFixed(1)}%',
              Icons.local_fire_department,
              AppTheme.warning,
              theme,
            ),
          ),
        ],
        if (cbd != null) ...[
          Expanded(
            child: _buildStatItem(
              'CBD',
              '${cbd!.toStringAsFixed(1)}%',
              Icons.medical_services,
              AppTheme.success,
              theme,
            ),
          ),
        ],
        if (floweringTime != null) ...[
          Expanded(
            child: _buildStatItem(
              'Flowering',
              floweringTime!,
              Icons.calendar_today,
              AppTheme.primaryColor,
              theme,
            ),
          ),
        ],
      ],
    );
  }

  Widget _buildStatItem(
    String label,
    String value,
    IconData icon,
    Color color,
    ThemeData theme,
  ) {
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
          Icon(icon, color: color, size: 16),
          const SizedBox(height: 4),
          Text(
            value,
            style: theme.textTheme.bodyMedium?.copyWith(
              fontWeight: FontWeight.w600,
              color: color,
            ),
          ),
          const SizedBox(height: 2),
          Text(
            label,
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
        if (value == 'edit') {
          onEdit?.call();
        }
      },
      itemBuilder: (context) => [
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
      ],
      icon: const Icon(
        Icons.more_vert,
        size: 18,
        color: AppTheme.textSecondary,
      ),
    );
  }
}

/// Compact version of StrainCard for lists
class StrainCardCompact extends StatelessWidget {
  const StrainCardCompact({
    super.key,
    required this.name,
    required this.genetics,
    this.thc,
    this.cbd,
    this.onTap,
    this.onFavorite,
    this.isFavorite = false,
  });

  final String name;
  final StrainGenetics genetics;
  final double? thc;
  final double? cbd;
  final VoidCallback? onTap;
  final VoidCallback? onFavorite;
  final bool isFavorite;

  @override
  Widget build(BuildContext context) {
    return StrainCard(
      name: name,
      genetics: genetics,
      thc: thc,
      cbd: cbd,
      onTap: onTap,
      onFavorite: onFavorite,
      isFavorite: isFavorite,
      compact: true,
    );
  }
}

/// Strain card with detailed effects display
class StrainCardDetailed extends StatelessWidget {
  const StrainCardDetailed({
    super.key,
    required this.name,
    required this.genetics,
    required this.effects,
    this.thc,
    this.cbd,
    this.onTap,
    this.isFavorite = false,
    this.onFavorite,
  });

  final String name;
  final StrainGenetics genetics;
  final StrainEffects effects;
  final double? thc;
  final double? cbd;
  final VoidCallback? onTap;
  final bool isFavorite;
  final VoidCallback? onFavorite;

  @override
  Widget build(BuildContext context) {
    return StrainCard(
      name: name,
      genetics: genetics,
      effects: effects,
      thc: thc,
      cbd: cbd,
      onTap: onTap,
      onFavorite: onFavorite,
      isFavorite: isFavorite,
      compact: false,
    );
  }
}
