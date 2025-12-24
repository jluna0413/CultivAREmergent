/// SensorCard widget for displaying sensor information and readings
/// Matches the sensor-card design from sensors.html and sensors_standalone.html
library;

import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

/// Configuration for sensor status
enum SensorStatus { online, offline, warning, error, calibrating, maintenance }

/// Configuration for sensor unit types
enum SensorUnit {
  celsius,
  fahrenheit,
  humidity,
  ph,
  ec,
  ppm,
  lux,
  db,
  percentage,
  custom,
}

/// Configuration for sensor reading
class SensorReading {
  const SensorReading({
    required this.value,
    this.unit = SensorUnit.custom,
    this.timestamp,
    this.isOptimal = true,
  });

  final double value;
  final SensorUnit unit;
  final DateTime? timestamp;
  final bool isOptimal;
}

/// Configuration for sensor data point
class SensorDataPoint {
  const SensorDataPoint({required this.timestamp, required this.value});

  final DateTime timestamp;
  final double value;
}

class SensorCard extends StatelessWidget {
  const SensorCard({
    super.key,
    required this.name,
    required this.type,
    this.description,
    this.status = SensorStatus.online,
    this.reading,
    this.data = const [],
    this.range,
    this.location,
    this.onTap,
    this.onEdit,
    this.onConfigure,
    this.compact = false,
  });

  final String name;
  final String type;
  final String? description;
  final SensorStatus status;
  final SensorReading? reading;
  final List<SensorDataPoint> data;
  final SensorRange? range;
  final String? location;
  final VoidCallback? onTap;
  final VoidCallback? onEdit;
  final VoidCallback? onConfigure;
  final bool compact;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Container(
      decoration: BoxDecoration(
        color: isDark
            ? AppTheme.surfaceColor.withOpacity(0.8)
            : const Color(0xB3FFFFFF),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isDark
              ? AppTheme.borderColor.withOpacity(0.2)
              : AppTheme.borderSecondary.withOpacity(0.1),
          width: 1,
        ),
        boxShadow: const [AppShadows.shadowMd],
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
                // Sensor Header
                Row(
                  children: [
                    // Status Indicator
                    _buildStatusIndicator(),
                    const SizedBox(width: 12),

                    // Sensor Info
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          // Sensor Name and Type
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
                              if (onEdit != null) ...[
                                const SizedBox(width: 8),
                                _buildActionMenu(),
                              ],
                            ],
                          ),
                          const SizedBox(height: 2),

                          // Sensor Type
                          Text(
                            type,
                            style: theme.textTheme.bodyMedium?.copyWith(
                              color: AppTheme.textSecondary,
                            ),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),

                          // Location (if not compact)
                          if (!compact && location != null) ...[
                            const SizedBox(height: 4),
                            _buildLocation(theme),
                          ],
                        ],
                      ),
                    ),

                    // Current Reading
                    if (reading != null) ...[
                      const SizedBox(width: 16),
                      _buildCurrentReading(theme),
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
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],

                // Mini Chart (if not compact and has data)
                if (!compact && data.isNotEmpty) ...[
                  const SizedBox(height: 16),
                  _buildMiniChart(theme),
                ],

                // Range Information (if available)
                if (!compact && range != null) ...[
                  const SizedBox(height: 12),
                  _buildRangeInfo(theme),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildStatusIndicator() {
    Color color;

    switch (status) {
      case SensorStatus.online:
        color = AppTheme.success;
        break;
      case SensorStatus.offline:
        color = AppTheme.textSecondary;
        break;
      case SensorStatus.warning:
        color = AppTheme.warning;
        break;
      case SensorStatus.error:
        color = AppTheme.error;
        break;
      case SensorStatus.calibrating:
        color = AppTheme.info;
        break;
      case SensorStatus.maintenance:
        color = AppTheme.warning;
        break;
    }

    return Container(
      width: 12,
      height: 12,
      decoration: BoxDecoration(
        color: color,
        shape: BoxShape.circle,
        boxShadow: [
          BoxShadow(
            color: color.withOpacity(0.3),
            blurRadius: 4,
            offset: const Offset(0, 2),
          ),
        ],
      ),
    );
  }

  Widget _buildLocation(ThemeData theme) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        const Icon(Icons.location_on, size: 14, color: AppTheme.textSecondary),
        const SizedBox(width: 4),
        Text(
          location!,
          style: theme.textTheme.bodySmall?.copyWith(
            color: AppTheme.textSecondary,
          ),
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
        ),
      ],
    );
  }

  Widget _buildCurrentReading(ThemeData theme) {
    final isOptimal = reading!.isOptimal;
    final color = isOptimal ? AppTheme.success : AppTheme.warning;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.end,
      children: [
        Text(
          _formatValue(reading!.value, reading!.unit),
          style: theme.textTheme.headlineSmall?.copyWith(
            fontWeight: FontWeight.bold,
            color: color,
          ),
        ),
        const SizedBox(height: 2),
        Text(
          _getUnitText(reading!.unit),
          style: theme.textTheme.bodySmall?.copyWith(
            color: AppTheme.textSecondary,
          ),
        ),
        if (reading!.timestamp != null) ...[
          const SizedBox(height: 2),
          Text(
            _formatTimestamp(reading!.timestamp!),
            style: theme.textTheme.bodySmall?.copyWith(
              color: AppTheme.textSecondary,
            ),
          ),
        ],
      ],
    );
  }

  Widget _buildMiniChart(ThemeData theme) {
    return Container(
      height: 60,
      decoration: BoxDecoration(
        color: AppTheme.backgroundColor.withOpacity(0.3),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(
          color: AppTheme.borderColor.withOpacity(0.1),
          width: 1,
        ),
      ),
      child: CustomPaint(
        painter: _SensorChartPainter(
          data: data,
          color: _getReadingColor(),
          theme: theme,
        ),
      ),
    );
  }

  Widget _buildRangeInfo(ThemeData theme) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: AppTheme.backgroundColor.withOpacity(0.3),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(
          color: AppTheme.borderColor.withOpacity(0.1),
          width: 1,
        ),
      ),
      child: Column(
        children: [
          Text(
            'Optimal Range',
            style: theme.textTheme.titleSmall?.copyWith(
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              _buildRangeItem(
                'Min',
                _formatValue(range!.min, reading?.unit ?? SensorUnit.custom),
                theme,
              ),
              _buildRangeItem(
                'Target',
                _formatValue(range!.target, reading?.unit ?? SensorUnit.custom),
                theme,
              ),
              _buildRangeItem(
                'Max',
                _formatValue(range!.max, reading?.unit ?? SensorUnit.custom),
                theme,
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildRangeItem(String label, String value, ThemeData theme) {
    return Column(
      children: [
        Text(
          label,
          style: theme.textTheme.bodySmall?.copyWith(
            color: AppTheme.textSecondary,
          ),
        ),
        const SizedBox(height: 2),
        Text(
          value,
          style: theme.textTheme.bodyMedium?.copyWith(
            fontWeight: FontWeight.w600,
          ),
        ),
      ],
    );
  }

  Widget _buildActionMenu() {
    return PopupMenuButton<String>(
      onSelected: (value) {
        switch (value) {
          case 'edit':
            onEdit?.call();
            break;
          case 'configure':
            onConfigure?.call();
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
        if (onConfigure != null)
          const PopupMenuItem(
            value: 'configure',
            child: Row(
              children: [
                Icon(Icons.settings, size: 16),
                SizedBox(width: 8),
                Text('Configure'),
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

  Color _getReadingColor() {
    if (reading == null) return AppTheme.primaryColor;
    return reading!.isOptimal ? AppTheme.success : AppTheme.warning;
  }

  String _formatValue(double value, SensorUnit unit) {
    switch (unit) {
      case SensorUnit.celsius:
      case SensorUnit.fahrenheit:
        return value.toStringAsFixed(1);
      case SensorUnit.humidity:
      case SensorUnit.percentage:
        return '${value.toStringAsFixed(0)}%';
      case SensorUnit.ph:
        return value.toStringAsFixed(2);
      case SensorUnit.ec:
      case SensorUnit.ppm:
      case SensorUnit.lux:
      case SensorUnit.db:
        return value.toStringAsFixed(1);
      case SensorUnit.custom:
        return value.toStringAsFixed(2);
    }
  }

  String _getUnitText(SensorUnit unit) {
    switch (unit) {
      case SensorUnit.celsius:
        return '°C';
      case SensorUnit.fahrenheit:
        return '°F';
      case SensorUnit.humidity:
      case SensorUnit.percentage:
        return '%';
      case SensorUnit.ph:
        return 'pH';
      case SensorUnit.ec:
        return 'EC';
      case SensorUnit.ppm:
        return 'ppm';
      case SensorUnit.lux:
        return 'lux';
      case SensorUnit.db:
        return 'dB';
      case SensorUnit.custom:
        return '';
    }
  }

  String _formatTimestamp(DateTime timestamp) {
    final now = DateTime.now();
    final difference = now.difference(timestamp);

    if (difference.inMinutes < 1) return 'Just now';
    if (difference.inMinutes < 60) return '${difference.inMinutes}m ago';
    if (difference.inHours < 24) return '${difference.inHours}h ago';
    if (difference.inDays < 7) return '${difference.inDays}d ago';

    return '${timestamp.day}/${timestamp.month}/${timestamp.year}';
  }
}

/// Configuration for sensor optimal range
class SensorRange {
  const SensorRange({
    required this.min,
    required this.max,
    required this.target,
  });

  final double min;
  final double max;
  final double target;
}

/// Compact version of SensorCard for sensor lists
class SensorCardCompact extends StatelessWidget {
  const SensorCardCompact({
    super.key,
    required this.name,
    required this.type,
    required this.status,
    required this.reading,
    this.onTap,
  });

  final String name;
  final String type;
  final SensorStatus status;
  final SensorReading reading;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return SensorCard(
      name: name,
      type: type,
      status: status,
      reading: reading,
      onTap: onTap,
      compact: true,
    );
  }
}

/// Custom painter for mini sensor charts
class _SensorChartPainter extends CustomPainter {
  const _SensorChartPainter({
    required this.data,
    required this.color,
    required this.theme,
  });

  final List<SensorDataPoint> data;
  final Color color;
  final ThemeData theme;

  @override
  void paint(Canvas canvas, Size size) {
    if (data.isEmpty) return;

    final paint = Paint()
      ..color = color
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke;

    final bgPaint = Paint()
      ..color = AppTheme.borderColor.withOpacity(0.2)
      ..strokeWidth = 1
      ..style = PaintingStyle.stroke;

    final path = Path();

    // Get min and max values for scaling
    final values = data.map((d) => d.value).toList();
    final minValue = values.reduce((a, b) => a < b ? a : b);
    final maxValue = values.reduce((a, b) => a > b ? a : b);
    final range = maxValue - minValue;

    if (range == 0) return; // Avoid division by zero

    // Calculate points
    final points = <Offset>[];
    for (int i = 0; i < data.length; i++) {
      final x = (i / (data.length - 1)) * size.width;
      final normalizedValue = (data[i].value - minValue) / range;
      final y = size.height - (normalizedValue * size.height);
      points.add(Offset(x, y));
    }

    // Draw background grid
    canvas.drawLine(
      Offset(0, size.height / 2),
      Offset(size.width, size.height / 2),
      bgPaint,
    );

    // Draw the line
    if (points.isNotEmpty) {
      path.moveTo(points.first.dx, points.first.dy);
      for (int i = 1; i < points.length; i++) {
        path.lineTo(points[i].dx, points[i].dy);
      }
      canvas.drawPath(path, paint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return true;
  }
}
