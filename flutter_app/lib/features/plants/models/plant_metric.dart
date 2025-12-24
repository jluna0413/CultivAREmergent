import 'package:flutter/material.dart';

class PlantMetric {
  const PlantMetric({
    required this.label,
    required this.value,
    required this.unit,
    required this.icon,
    this.color,
  });
  final String label;
  final String value;
  final String unit;
  final IconData icon;
  final Color? color;
}
