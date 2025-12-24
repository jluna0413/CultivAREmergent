import 'package:flutter/material.dart';

/// Dart Enhanced Enum for Verification Badges.
/// "Dot Shorthand" capable for UI states.
enum VerificationBadge {
  none(
    label: 'Unverified',
    color: Colors.grey,
    icon: Icons.help_outline,
    glowColor: Colors.transparent,
  ),
  bronze(
    label: 'Breeder Verified',
    color: Color(0xFFCD7F32), // Bronze
    icon: Icons.verified,
    glowColor: Color(0x33CD7F32),
  ),
  silver(
    label: 'Community Verified',
    color: Color(0xFFC0C0C0), // Silver
    icon: Icons.verified_user,
    glowColor: Color(0x33C0C0C0),
  ),
  gold(
    label: 'Neuro-Verified',
    color: Color(0xFFFFD700), // Gold
    icon: Icons.workspace_premium, // Premium/Star
    glowColor: Color(0x66FFD700),
  );

  final String label;
  final Color color;
  final IconData icon;
  final Color glowColor;

  const VerificationBadge({
    required this.label,
    required this.color,
    required this.icon,
    required this.glowColor,
  });

  /// Helper to check if verified at all
  bool get isVerified => this != VerificationBadge.none;
}
