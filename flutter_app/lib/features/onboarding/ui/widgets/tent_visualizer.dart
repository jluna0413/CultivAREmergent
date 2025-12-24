
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import '../../logic/pot_placement_logic.dart';

class TentVisualizer extends StatelessWidget {
  final TentDimensions tentDimensions;
  final List<PotPosition> potPositions;
  final String potSizeLabel;
  final String? selectedPotId;
  final ValueChanged<String>? onPotTap;

  const TentVisualizer({
    super.key,
    required this.tentDimensions,
    required this.potPositions,
    required this.potSizeLabel,
    this.selectedPotId,
    this.onPotTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Container(
      decoration: BoxDecoration(
        color: colorScheme.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(12),
      ),
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          Text(
            'Tent Visualizer',
            style: theme.textTheme.titleMedium?.copyWith(
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 12),
          Expanded(
            child: LayoutBuilder(
              builder: (context, constraints) {
                // Calculate scale to fit tent in available space (Expanded area)
                
                final scaleX = constraints.maxWidth / tentDimensions.widthInches;
                final scaleY = constraints.maxHeight / tentDimensions.depthInches;
                final scale = scaleX < scaleY ? scaleX : scaleY;

                final scaledWidth = tentDimensions.widthInches * scale;
                final scaledHeight = tentDimensions.depthInches * scale;

                return Center(
                  child: GestureDetector(
                    onTapUp: (details) {
                      if (onPotTap != null) {
                        _handleTap(
                          details.localPosition,
                          scale,
                          scaledWidth,
                          scaledHeight,
                        );
                      }
                    },
                    child: CustomPaint(
                      size: Size(scaledWidth, scaledHeight),
                      painter: _TentPainter(
                        tentDimensions: tentDimensions,
                        potPositions: potPositions,
                        potSizeLabel: potSizeLabel,
                        selectedPotId: selectedPotId,
                        scale: scale,
                        primaryColor: colorScheme.primary,
                        outlineColor: colorScheme.outline,
                        selectedColor: colorScheme.secondary,
                        surfaceColor: colorScheme.surface,
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  void _handleTap(
    ui.Offset position,
    double scale,
    double width,
    double height,
  ) {
    // Convert tap position to tent coordinates
    final tentX = position.dx / scale;
    final tentY = position.dy / scale;

    // Find the pot that was tapped
    final growZone = getEffectiveGrowZone(potSizeLabel);
    final hitRadius = growZone / 2;

    for (final pot in potPositions) {
      final dx = tentX - pot.x;
      final dy = tentY - pot.y;
      final distance = (dx * dx + dy * dy);
      if (distance <= hitRadius * hitRadius) {
        onPotTap?.call(pot.id);
        return;
      }
    }
  }
}

class _TentPainter extends CustomPainter {
  final TentDimensions tentDimensions;
  final List<PotPosition> potPositions;
  final String potSizeLabel;
  final String? selectedPotId;
  final double scale;
  final Color primaryColor;
  final Color outlineColor;
  final Color selectedColor;
  final Color surfaceColor;

  _TentPainter({
    required this.tentDimensions,
    required this.potPositions,
    required this.potSizeLabel,
    required this.scale,
    required this.primaryColor,
    required this.outlineColor,
    required this.selectedColor,
    required this.surfaceColor,
    this.selectedPotId,
  });

  @override
  void paint(Canvas canvas, Size size) {
    // Draw tent outline
    final tentPaint = Paint()
      ..color = primaryColor.withAlpha(76)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3;

    final tentRect = Rect.fromLTWH(0, 0, size.width, size.height);
    canvas.drawRRect(
      RRect.fromRectAndRadius(tentRect, const Radius.circular(8)),
      tentPaint,
    );

    // Fill tent background
    final tentFillPaint = Paint()
      ..color = surfaceColor.withAlpha(128)
      ..style = PaintingStyle.fill;
    canvas.drawRRect(
      RRect.fromRectAndRadius(tentRect, const Radius.circular(8)),
      tentFillPaint,
    );

    // Get actual pot diameter (not grow zone) for visualization
    final potDimensions = PotDimensions.fromLabel(potSizeLabel);
    final potRadius = (potDimensions.diameterInches / 2) * scale;

    // Draw each pot
    for (final pot in potPositions) {
      final centerX = pot.x * scale;
      final centerY = pot.y * scale;
      final center = ui.Offset(centerX, centerY);

      final isSelected = pot.id == selectedPotId;

      // Draw canopy zone (dashed circle) for selected pot
      if (isSelected) {
        final canopyPaint = Paint()
          ..color = selectedColor.withAlpha(76)
          ..style = PaintingStyle.stroke
          ..strokeWidth = 2;

        // Canopy zone uses the grow zone, not pot base diameter
        final growZone = getEffectiveGrowZone(potSizeLabel);
        final canopyRadius = (growZone / 2) * scale;
        _drawDashedCircle(canvas, center, canopyRadius, canopyPaint);
      }

      // Draw pot circle
      final potPaint = Paint()
        ..color = isSelected ? selectedColor : primaryColor
        ..style = PaintingStyle.fill;

      canvas.drawCircle(center, potRadius, potPaint);

      // Draw pot border
      final borderPaint = Paint()
        ..color = isSelected ? selectedColor : primaryColor.withAlpha(204)
        ..style = PaintingStyle.stroke
        ..strokeWidth = isSelected ? 3 : 2;

      canvas.drawCircle(center, potRadius, borderPaint);
    }
  }

  void _drawDashedCircle(
    Canvas canvas,
    ui.Offset center,
    double radius,
    Paint paint,
  ) {
    const dashLength = 8.0;
    const gapLength = 4.0;
    final circumference = 2 * 3.14159 * radius;
    final dashCount = (circumference / (dashLength + gapLength)).floor();

    for (int i = 0; i < dashCount; i++) {
      final startAngle = (i * (dashLength + gapLength)) / radius;
      final sweepAngle = dashLength / radius;

      canvas.drawArc(
        Rect.fromCircle(center: center, radius: radius),
        startAngle,
        sweepAngle,
        false,
        paint,
      );
    }
  }

  @override
  bool shouldRepaint(covariant _TentPainter oldDelegate) {
    return tentDimensions != oldDelegate.tentDimensions ||
        potPositions != oldDelegate.potPositions ||
        selectedPotId != oldDelegate.selectedPotId ||
        scale != oldDelegate.scale;
  }
}

/// Widget for selecting pot size
class PotSizeSelector extends StatelessWidget {
  final String selectedSize;
  final ValueChanged<String> onSizeChanged;

  const PotSizeSelector({
    super.key,
    required this.selectedSize,
    required this.onSizeChanged,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Wrap(
      spacing: 8,
      runSpacing: 8,
      alignment: WrapAlignment.center,
      children: PotDimensions.allSizes.map((pot) {
        final isSelected = pot.label == selectedSize;
        return Material(
          color: isSelected
              ? colorScheme.primary
              : colorScheme.surfaceContainerHigh,
          borderRadius: BorderRadius.circular(8),
          child: InkWell(
            onTap: () => onSizeChanged(pot.label),
            borderRadius: BorderRadius.circular(8),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
              child: Text(
                pot.label,
                style: theme.textTheme.bodyMedium?.copyWith(
                  color: isSelected
                      ? colorScheme.onPrimary
                      : colorScheme.onSurface,
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                ),
              ),
            ),
          ),
        );
      }).toList(),
    );
  }
}
