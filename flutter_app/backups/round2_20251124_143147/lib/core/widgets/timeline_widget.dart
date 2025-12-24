/// TimelineWidget for displaying plant timeline and activities
/// Matches the timeline design from dashboard.html and plant activity logs
library;

import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

/// Configuration for timeline events
enum TimelineEventType {
  planting,
  transplanting,
  watering,
  fertilizing,
  pruning,
  harvesting,
  observation,
  measurement,
  treatment,
  custom,
}

/// Configuration for timeline event
class TimelineEvent {
  const TimelineEvent({
    required this.id,
    required this.title,
    required this.description,
    required this.timestamp,
    required this.type,
    this.isCompleted = true,
    this.metadata,
  });

  final String id;
  final String title;
  final String description;
  final DateTime timestamp;
  final TimelineEventType type;
  final bool isCompleted;
  final Map<String, dynamic>? metadata;
}

class TimelineWidget extends StatefulWidget {
  const TimelineWidget({
    super.key,
    required this.events,
    this.onEventTap,
    this.onEventEdit,
    this.compact = false,
    this.showVerticalLine = true,
    this.maxEvents,
  });

  final List<TimelineEvent> events;
  final void Function(TimelineEvent event)? onEventTap;
  final void Function(TimelineEvent event)? onEventEdit;
  final bool compact;
  final bool showVerticalLine;
  final int? maxEvents;

  @override
  State<TimelineWidget> createState() => _TimelineWidgetState();
}

class _TimelineWidgetState extends State<TimelineWidget> {
  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    if (widget.events.isEmpty) {
      return _buildEmptyState(theme);
    }

    final eventsToShow = widget.maxEvents != null
        ? widget.events.take(widget.maxEvents!).toList()
        : widget.events;

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
        boxShadow: const [AppShadows.shadowMd],
      ),
      child: Padding(
        padding: widget.compact
            ? const EdgeInsets.all(16)
            : const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Timeline Header
            Row(
              children: [
                Icon(
                  Icons.timeline,
                  color: AppTheme.primaryColor,
                  size: widget.compact ? 18 : 20,
                ),
                const SizedBox(width: 8),
                Text(
                  'Timeline',
                  style: theme.textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const Spacer(),
                if (widget.events.length >
                    (widget.maxEvents ?? widget.events.length))
                  Text(
                    'Showing ${eventsToShow.length} of ${widget.events.length}',
                    style: theme.textTheme.bodySmall?.copyWith(
                      color: AppTheme.textSecondary,
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 16),

            // Timeline Events
            if (widget.showVerticalLine)
              _buildTimelineWithLine(context, eventsToShow)
            else
              _buildTimelineWithoutLine(context, eventsToShow),
          ],
        ),
      ),
    );
  }

  Widget _buildEmptyState(ThemeData theme) {
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
        boxShadow: const [AppShadows.shadowMd],
      ),
      child: Padding(
        padding: widget.compact
            ? const EdgeInsets.all(16)
            : const EdgeInsets.all(20),
        child: Column(
          children: [
            const Icon(Icons.timeline, size: 48, color: AppTheme.textSecondary),
            const SizedBox(height: 16),
            Text(
              'No timeline events yet',
              style: theme.textTheme.titleMedium?.copyWith(
                color: AppTheme.textSecondary,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Timeline events will appear here as your plants grow',
              style: theme.textTheme.bodyMedium?.copyWith(
                color: AppTheme.textSecondary,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTimelineWithLine(
    BuildContext context,
    List<TimelineEvent> events,
  ) {
    return CustomScrollView(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      slivers: [
        SliverList(
          delegate: SliverChildBuilderDelegate((context, index) {
            final event = events[index];
            final isLast = index == events.length - 1;

            return Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Timeline Line and Icon
                Column(
                  children: [
                    Container(
                      width: 12,
                      height: 12,
                      decoration: BoxDecoration(
                        color: _getEventColor(event.type),
                        shape: BoxShape.circle,
                        boxShadow: [
                          BoxShadow(
                            color: _getEventColor(
                              event.type,
                            ).withValues(alpha: 0.3),
                            blurRadius: 4,
                            offset: const Offset(0, 2),
                          ),
                        ],
                      ),
                    ),
                    if (!isLast)
                      Container(
                        width: 2,
                        height: 60,
                        color: AppTheme.borderColor.withValues(alpha: 0.3),
                      ),
                  ],
                ),
                const SizedBox(width: 16),

                // Event Content
                Expanded(child: _buildEventContent(event, context)),
              ],
            );
          }, childCount: events.length),
        ),
      ],
    );
  }

  Widget _buildTimelineWithoutLine(
    BuildContext context,
    List<TimelineEvent> events,
  ) {
    return Column(
      children: events.map((event) {
        return Padding(
          padding: const EdgeInsets.only(bottom: 12),
          child: _buildEventContent(event, context),
        );
      }).toList(),
    );
  }

  Widget _buildEventContent(TimelineEvent event, BuildContext context) {
    final theme = Theme.of(context);

    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: () => widget.onEventTap?.call(event),
        borderRadius: BorderRadius.circular(12),
        child: Container(
          decoration: BoxDecoration(
            color: AppTheme.backgroundColor.withValues(alpha: 0.5),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(
              color: AppTheme.borderColor.withValues(alpha: 0.1),
              width: 1,
            ),
          ),
          padding: const EdgeInsets.all(12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Event Header
              Row(
                children: [
                  Icon(
                    _getEventIcon(event.type),
                    size: 16,
                    color: _getEventColor(event.type),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      event.title,
                      style: theme.textTheme.titleSmall?.copyWith(
                        fontWeight: FontWeight.w600,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                  if (event.isCompleted) ...[
                    const SizedBox(width: 8),
                    const Icon(
                      Icons.check_circle,
                      size: 16,
                      color: AppTheme.success,
                    ),
                  ],
                ],
              ),

              // Event Description
              if (event.description.isNotEmpty) ...[
                const SizedBox(height: 4),
                Text(
                  event.description,
                  style: theme.textTheme.bodySmall?.copyWith(
                    color: AppTheme.textSecondary,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ],

              // Event Footer
              const SizedBox(height: 8),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  // Timestamp
                  Text(
                    _formatTimestamp(event.timestamp),
                    style: theme.textTheme.bodySmall?.copyWith(
                      color: AppTheme.textSecondary,
                    ),
                  ),

                  // Event Type Badge
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 8,
                      vertical: 2,
                    ),
                    decoration: BoxDecoration(
                      color: _getEventColor(event.type).withValues(alpha: 0.1),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(
                        color: _getEventColor(
                          event.type,
                        ).withValues(alpha: 0.2),
                        width: 1,
                      ),
                    ),
                    child: Text(
                      _getEventTypeLabel(event.type),
                      style: TextStyle(
                        color: _getEventColor(event.type),
                        fontSize: 10,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  IconData _getEventIcon(TimelineEventType type) {
    switch (type) {
      case TimelineEventType.planting:
        return Icons.eco;
      case TimelineEventType.transplanting:
        return Icons.arrow_forward;
      case TimelineEventType.watering:
        return Icons.water_drop;
      case TimelineEventType.fertilizing:
        return Icons.science;
      case TimelineEventType.pruning:
        return Icons.content_cut;
      case TimelineEventType.harvesting:
        return Icons.eco;
      case TimelineEventType.observation:
        return Icons.visibility;
      case TimelineEventType.measurement:
        return Icons.straighten;
      case TimelineEventType.treatment:
        return Icons.medical_services;
      case TimelineEventType.custom:
        return Icons.event_note;
    }
  }

  Color _getEventColor(TimelineEventType type) {
    switch (type) {
      case TimelineEventType.planting:
        return Colors.green;
      case TimelineEventType.transplanting:
        return Colors.blue;
      case TimelineEventType.watering:
        return Colors.lightBlue;
      case TimelineEventType.fertilizing:
        return Colors.orange;
      case TimelineEventType.pruning:
        return Colors.brown;
      case TimelineEventType.harvesting:
        return Colors.amber;
      case TimelineEventType.observation:
        return Colors.purple;
      case TimelineEventType.measurement:
        return Colors.teal;
      case TimelineEventType.treatment:
        return Colors.red;
      case TimelineEventType.custom:
        return Colors.grey;
    }
  }

  String _formatTimestamp(DateTime timestamp) {
    final now = DateTime.now();
    final difference = now.difference(timestamp);

    if (difference.inDays > 0) {
      return '${difference.inDays}d ago';
    } else if (difference.inHours > 0) {
      return '${difference.inHours}h ago';
    } else if (difference.inMinutes > 0) {
      return '${difference.inMinutes}m ago';
    } else {
      return 'Just now';
    }
  }

  String _getEventTypeLabel(TimelineEventType type) {
    switch (type) {
      case TimelineEventType.planting:
        return 'Planting';
      case TimelineEventType.transplanting:
        return 'Transplant';
      case TimelineEventType.watering:
        return 'Watered';
      case TimelineEventType.fertilizing:
        return 'Fertilized';
      case TimelineEventType.pruning:
        return 'Pruned';
      case TimelineEventType.harvesting:
        return 'Harvest';
      case TimelineEventType.observation:
        return 'Observed';
      case TimelineEventType.measurement:
        return 'Measured';
      case TimelineEventType.treatment:
        return 'Treated';
      case TimelineEventType.custom:
        return 'Custom';
    }
  }
}
