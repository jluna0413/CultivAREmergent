import 'dart:ui';
import 'package:flutter/material.dart';

class GlassCard extends StatelessWidget {
  const GlassCard({
    super.key,
    required this.child,
    this.blur = 10.0,
    this.color = Colors.white,
    this.opacity = 0.1,
    this.borderRadius = const BorderRadius.all(Radius.circular(20)),
  });
  final Widget child;
  final double blur;
  final Color color;
  final double opacity;
  final BorderRadius borderRadius;

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: borderRadius,
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: blur, sigmaY: blur),
        child: Container(
          decoration: BoxDecoration(
            color: color.withAlpha((opacity * 255).round()),
            borderRadius: borderRadius,
            border: Border.all(color: Colors.white.withAlpha(51), width: 1.0),
          ),
          child: child,
        ),
      ),
    );
  }
}
