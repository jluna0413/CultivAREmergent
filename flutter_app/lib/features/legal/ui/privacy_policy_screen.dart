import 'package:flutter/material.dart';

class PrivacyPolicyScreen extends StatelessWidget {
  const PrivacyPolicyScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final sections = _privacySections;
    return Scaffold(
      appBar: AppBar(
        title: const Text('Privacy Policy'),
        backgroundColor: const Color(0xFF4CAF50),
        foregroundColor: Colors.white,
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(24),
        itemCount: sections.length,
        itemBuilder: (context, index) {
          final section = sections[index];
          return Padding(
            padding: const EdgeInsets.only(bottom: 24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  section.title,
                  style: Theme.of(
                    context,
                  ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 8),
                ...section.paragraphs.map(
                  (paragraph) => Padding(
                    padding: const EdgeInsets.only(bottom: 8),
                    child: Text(
                      paragraph,
                      style: Theme.of(context).textTheme.bodyMedium,
                    ),
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}

class _PrivacySection {
  const _PrivacySection({required this.title, required this.paragraphs});

  final String title;
  final List<String> paragraphs;
}

final List<_PrivacySection> _privacySections = [
  const _PrivacySection(
    title: 'Data We Collect',
    paragraphs: [
      'CultivAR stores account information (name, email) and the grow journal data you explicitly enter: plant notes, environmental readings, and media attachments.',
      'Telemetry is limited to anonymized diagnostics that help us improve the product.',
    ],
  ),
  const _PrivacySection(
    title: 'How We Use Data',
    paragraphs: [
      'We use your data to power dashboards, reminders, and analytics within the app.',
      'We never sell personal data. Aggregated metrics may be used to improve cultivar recommendations.',
    ],
  ),
  const _PrivacySection(
    title: 'Storage & Security',
    paragraphs: [
      'Sensitive tokens are encrypted using secure storage on device. Cloud backups, when enabled, are encrypted at rest.',
      'We recommend enabling biometrics or device PIN to prevent unauthorized access.',
    ],
  ),
  const _PrivacySection(
    title: 'Your Controls',
    paragraphs: [
      'You can export, delete, or update your data at any time from Settings > Privacy.',
      'If you delete your account we permanently remove associated data within 30 days.',
    ],
  ),
  const _PrivacySection(
    title: 'Contact',
    paragraphs: [
      'Questions? Reach out to privacy@cultivar.app and we will respond within 48 hours.',
    ],
  ),
];
