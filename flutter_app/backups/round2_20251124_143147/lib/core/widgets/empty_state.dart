/// EmptyState widget for displaying empty states with proper messaging
/// Matches empty state designs from dashboard.html and other UI templates
library;
// (removed stray library directive)

import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

/// Configuration for empty state types
enum EmptyStateType {
  general,
  noData,
  noResults,
  noPlants,
  noCultivars,
  noSensors,
  noActivities,
  searchResults,
  filters,
  loading,
}

/// Configuration for empty state action
class EmptyStateAction {
  const EmptyStateAction({
    required this.label,
    required this.onPressed,
    this.isPrimary = false,
  });

  final String label;
  final VoidCallback onPressed;
  final bool isPrimary;
}

class EmptyState extends StatelessWidget {
  const EmptyState({
    super.key,
    required this.type,
    this.title,
    this.message,
    this.icon,
    this.action,
    this.actions,
    this.showImage = false,
    this.imagePath,
    this.compact = false,
  });

  final EmptyStateType type;
  final String? title;
  final String? message;
  final IconData? icon;
  final EmptyStateAction? action;
  final List<EmptyStateAction>? actions;
  final bool showImage;
  final String? imagePath;
  final bool compact;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Container(
      width: double.infinity,
      decoration: BoxDecoration(
        color: isDark
            ? AppTheme.surfaceColor.withValues(alpha: 0.8)
            : AppTheme.surfaceColor.withValues(alpha: 0.7),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isDark
              ? AppTheme.borderColor.withValues(alpha: 0.2)
              : AppTheme.borderSecondary.withValues(alpha: 0.1),
          width: 1,
        ),
        boxShadow: const [AppShadows.shadowMd],
      ),
      child: Padding(
        padding: _getPadding(),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Icon or Image
            _buildVisualElement(),
            SizedBox(height: _getSpacing()),

            // Title
            Text(
              _getTitle(),
              style: theme.textTheme.headlineSmall?.copyWith(
                fontWeight: FontWeight.w600,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 8),

            // Message
            if (_getMessage().isNotEmpty) ...[
              Text(
                _getMessage(),
                style: theme.textTheme.bodyLarge?.copyWith(
                  color: AppTheme.textSecondary,
                ),
                textAlign: TextAlign.center,
              ),
              SizedBox(height: _getMessageSpacing()),
            ],

            // Actions
            if (action != null || (actions != null && actions!.isNotEmpty)) ...[
              _buildActions(),
            ],
          ],
        ),
      ),
    );
  }

  EdgeInsets _getPadding() {
    return compact ? const EdgeInsets.all(24) : const EdgeInsets.all(32);
  }

  double _getSpacing() {
    return compact ? 16 : 24;
  }

  double _getMessageSpacing() {
    return compact ? 16 : 24;
  }

  Widget _buildVisualElement() {
    if (showImage && imagePath != null) {
      return Container(
        width: compact ? 80 : 120,
        height: compact ? 80 : 120,
        decoration: BoxDecoration(
          color: AppTheme.backgroundColor.withValues(alpha: 0.5),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(
            color: AppTheme.borderColor.withValues(alpha: 0.2),
            width: 1,
          ),
        ),
        child: ClipRRect(
          borderRadius: BorderRadius.circular(16),
          child: Image.asset(
            imagePath!,
            fit: BoxFit.cover,
            errorBuilder: (context, error, stackTrace) {
              return _buildIconFallback();
            },
          ),
        ),
      );
    }

    return _buildIconFallback();
  }

  Widget _buildIconFallback() {
    return Container(
      width: compact ? 64 : 96,
      height: compact ? 64 : 96,
      decoration: BoxDecoration(
        color: AppTheme.backgroundColor.withValues(alpha: 0.5),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: AppTheme.borderColor.withValues(alpha: 0.2),
          width: 1,
        ),
      ),
      child: Icon(
        icon ?? _getDefaultIcon(),
        size: compact ? 32 : 48,
        color: AppTheme.textSecondary,
      ),
    );
  }

  Widget _buildActions() {
    if (actions != null && actions!.isNotEmpty) {
      return Column(
        children: [
          ...actions!.asMap().entries.map((entry) {
            final index = entry.key;
            final action = entry.value;

            return Padding(
              padding: EdgeInsets.only(
                bottom: index < actions!.length - 1 ? 8 : 0,
              ),
              child: _buildActionButton(action),
            );
          }),
        ],
      );
    } else if (action != null) {
      return _buildActionButton(action!);
    }

    return const SizedBox.shrink();
  }

  Widget _buildActionButton(EmptyStateAction action) {
    if (action.isPrimary) {
      return SizedBox(
        width: double.infinity,
        child: ElevatedButton.icon(
          onPressed: action.onPressed,
          icon: const Icon(Icons.add, size: 20),
          label: Text(action.label),
          style: ElevatedButton.styleFrom(
            backgroundColor: AppTheme.primaryColor,
            foregroundColor: AppTheme.onPrimary,
            padding: EdgeInsets.symmetric(
              vertical: compact ? 12 : 16,
              horizontal: 24,
            ),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
      );
    } else {
      return SizedBox(
        width: double.infinity,
        child: OutlinedButton.icon(
          onPressed: action.onPressed,
          icon: const Icon(Icons.refresh, size: 20),
          label: Text(action.label),
          style: OutlinedButton.styleFrom(
            foregroundColor: AppTheme.primaryColor,
            side: const BorderSide(color: AppTheme.primaryColor, width: 1),
            padding: EdgeInsets.symmetric(
              vertical: compact ? 12 : 16,
              horizontal: 24,
            ),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
      );
    }
  }

  String _getTitle() {
    if (title != null) return title!;

    switch (type) {
      case EmptyStateType.noData:
        return 'No Data Available';
      case EmptyStateType.noResults:
        return 'No Results Found';
      case EmptyStateType.noPlants:
        return 'No Plants Yet';
      case EmptyStateType.noCultivars:
        return 'No Cultivars Added';
      case EmptyStateType.noSensors:
        return 'No Sensors Connected';
      case EmptyStateType.noActivities:
        return 'No Activities Yet';
      case EmptyStateType.searchResults:
        return 'No Search Results';
      case EmptyStateType.filters:
        return 'No Matching Results';
      case EmptyStateType.loading:
        return 'Loading...';
      case EmptyStateType.general:
        return 'Nothing Here Yet';
    }
  }

  String _getMessage() {
    if (message != null) return message!;

    switch (type) {
      case EmptyStateType.noData:
        return 'There\'s no data to display at the moment.';
      case EmptyStateType.noResults:
        return 'Try adjusting your search or filters to find what you\'re looking for.';
      case EmptyStateType.noPlants:
        return 'Start your growing journey by adding your first plant.';
      case EmptyStateType.noCultivars:
        return 'Add some cultivars to build your collection and track their progress.';
      case EmptyStateType.noSensors:
        return 'Connect sensors to monitor your growing environment and plant health.';
      case EmptyStateType.noActivities:
        return 'Activities will appear here as you use the app.';
      case EmptyStateType.searchResults:
        return 'No items match your current search criteria.';
      case EmptyStateType.filters:
        return 'Try adjusting your filters to see more results.';
      case EmptyStateType.loading:
        return 'Please wait while we load the content.';
      case EmptyStateType.general:
        return 'There\'s nothing to display here yet.';
    }
  }

  IconData _getDefaultIcon() {
    switch (type) {
      case EmptyStateType.noData:
        return Icons.data_usage;
      case EmptyStateType.noResults:
        return Icons.search_off;
      case EmptyStateType.noPlants:
        return Icons.eco;
      case EmptyStateType.noCultivars:
        return Icons.science;
      case EmptyStateType.noSensors:
        return Icons.sensors;
      case EmptyStateType.noActivities:
        return Icons.history;
      case EmptyStateType.searchResults:
        return Icons.search;
      case EmptyStateType.filters:
        return Icons.filter_list_off;
      case EmptyStateType.loading:
        return Icons.hourglass_empty;
      case EmptyStateType.general:
        return Icons.inbox;
    }
  }
}
