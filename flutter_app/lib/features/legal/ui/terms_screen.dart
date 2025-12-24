import 'package:flutter/material.dart';

class TermsScreen extends StatelessWidget {
  const TermsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final sections = _termsSections;
    return Scaffold(
      appBar: AppBar(
        title: const Text('Terms of Service'),
        backgroundColor: const Color(0xFF4CAF50),
        foregroundColor: Colors.white,
      ),
      body: ListView.separated(
        padding: const EdgeInsets.all(24),
        itemBuilder: (context, index) {
          final section = sections[index];
          return Column(
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
          );
        },
        separatorBuilder: (_, _) => const Divider(height: 32),
        itemCount: sections.length,
      ),
    );
  }
}

class _LegalSection {
  const _LegalSection({required this.title, required this.paragraphs});

  final String title;
  final List<String> paragraphs;
}

final List<_LegalSection> _termsSections = [
  const _LegalSection(
    title: '1. Acceptance of Terms',
    paragraphs: [
      'By accessing or using CultivAR you agree to be bound by these Terms of Service and all applicable laws and regulations.',
      'If you do not agree with any of these terms, you are prohibited from using or accessing this application.',
    ],
  ),
  const _LegalSection(
    title: '2. Grower Responsibilities',
    paragraphs: [
      'You are responsible for complying with all local regulations regarding the cultivation, possession, and distribution of cannabis products.',
      'You agree not to use CultivAR to engage in any unlawful or unauthorized activities.',
    ],
  ),
  const _LegalSection(
    title: '3. Data Usage',
    paragraphs: [
      'CultivAR stores cultivation data securely on your device and approved services. By using the app you consent to our storage and processing of this information.',
      'You may export or delete your information at any time from the settings area.',
    ],
  ),
  const _LegalSection(
    title: '4. Service Availability',
    paragraphs: [
      'We aim to keep CultivAR available and accurate, but maintenance windows or outages may occur.',
      'Features marked as beta may change without notice and should not be relied upon for critical operations.',
    ],
  ),
  const _LegalSection(
    title: '5. Contact',
    paragraphs: [
      'For legal or compliance questions please contact the CultivAR team via support@cultivar.app.',
    ],
  ),
];
