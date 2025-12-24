import 'package:flutter/material.dart';

enum SBTType {
  masterGrower(
    label: "Master Grower",
    color: Color(0xFFFFD700),
    icon: Icons.workspace_premium, // Available
  ),
  cultivator(
    label: "Cultivator",
    color: Color(0xFFC0C0C0),
    icon: Icons.agriculture,
  ),
  novice(
    label: "Novice",
    color: Color(0xFFCD7F32),
    icon: Icons.grass,
  ); // Changed from sprout

  final String label;
  final Color color;
  final IconData icon;

  const SBTType({required this.label, required this.color, required this.icon});
}

class SBTBadgeWidget extends StatelessWidget {
  final SBTType type;
  final bool isLarge;

  const SBTBadgeWidget({super.key, required this.type, this.isLarge = false});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(
        horizontal: isLarge ? 12 : 8,
        vertical: isLarge ? 6 : 4,
      ),
      decoration: BoxDecoration(
        color: type.color.withOpacity(0.15),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: type.color.withOpacity(0.6), width: 1),
        boxShadow: [
          BoxShadow(
            color: type.color.withOpacity(0.2),
            blurRadius: 8,
            spreadRadius: 1,
          ),
        ],
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(type.icon, color: type.color, size: isLarge ? 18 : 14),
          SizedBox(width: isLarge ? 6 : 4),
          Text(
            type.label.toUpperCase(),
            style: TextStyle(
              color: type.color,
              fontSize: isLarge ? 12 : 10,
              fontWeight: FontWeight.bold,
              letterSpacing: 1.0,
            ),
          ),
        ],
      ),
    );
  }
}
