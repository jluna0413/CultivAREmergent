import 'package:flutter/material.dart';
import 'dart:ui' as ui;

class StatCard extends StatelessWidget {
  final String title;
  final String value;
  final String? subtitle;
  final List<Color>? gradientColors;
  final IconData? icon;

  const StatCard({
    super.key,
    required this.title,
    required this.value,
    this.subtitle,
    this.gradientColors,
    this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 20,
            offset: const ui.Offset(0, 4),
          ),
        ],
        gradient: gradientColors != null
            ? LinearGradient(
                colors: gradientColors!,
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              )
            : null,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                title,
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                  color: gradientColors != null
                      ? Colors.white.withValues(alpha: 0.9)
                      : Colors.grey[600],
                ),
              ),
              if (icon != null)
                Icon(
                  icon,
                  color: gradientColors != null
                      ? Colors.white
                      : Colors.grey[400],
                  size: 20,
                ),
            ],
          ),
          const Spacer(),
          Text(
            value,
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
              color: gradientColors != null ? Colors.white : Colors.black,
              letterSpacing: -0.5,
            ),
          ),
          if (subtitle != null) ...[
            const SizedBox(height: 4),
            Text(
              subtitle!,
              style: TextStyle(
                fontSize: 12,
                color: gradientColors != null
                    ? Colors.white.withValues(alpha: 0.8)
                    : Colors.grey[500],
              ),
            ),
          ],
        ],
      ),
    );
  }
}
