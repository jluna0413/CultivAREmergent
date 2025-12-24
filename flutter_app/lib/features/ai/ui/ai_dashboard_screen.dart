import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_navigation_drawer.dart';

class AIDashboardScreen extends ConsumerWidget {
  const AIDashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      backgroundColor: const Color(0xFF1a1a1a),
      appBar: AppBar(
        backgroundColor: const Color(0xFF2a2a2a),
        title: const Text(
          'AI Assistant',
          style: TextStyle(color: Colors.white),
        ),
        iconTheme: const IconThemeData(color: Colors.white),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/dashboard'),
        ),
      ),
      drawer: const AppNavigationDrawer(),
      body: const SingleChildScrollView(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Welcome section
            _AIWelcomeSection(),

            SizedBox(height: 24),

            // AI Features Grid
            _AIFeaturesGrid(),

            SizedBox(height: 24),

            // Recent AI Activity
            _RecentAIActivity(),

            SizedBox(height: 24),

            // Quick Tips
            _AIQuickTips(),
          ],
        ),
      ),
    );
  }
}

class _AIWelcomeSection extends StatelessWidget {
  const _AIWelcomeSection();

  @override
  Widget build(BuildContext context) {
    return Card(
      color: const Color(0xFF2a2a2a),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(
                      colors: [AppColors.primary500, AppColors.primary600],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: const Icon(
                    Icons.psychology,
                    color: Colors.white,
                    size: 32,
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'AI Grow Assistant',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        'Your intelligent companion for optimal cannabis cultivation',
                        style: TextStyle(
                          color: Colors.white.withOpacity(0.7),
                          fontSize: 14,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _AIFeaturesGrid extends StatelessWidget {
  const _AIFeaturesGrid();

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'AI Features',
          style: TextStyle(
            color: Colors.white,
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 16),
        GridView.count(
          crossAxisCount: 2,
          crossAxisSpacing: 12,
          mainAxisSpacing: 12,
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          children: const [
            _AIFeatureCard(
              icon: Icons.chat,
              title: 'AI Chat Advisor',
              description: 'Get instant answers to your growing questions',
              route: '/ai/chat',
              color: Colors.blue,
            ),
            _AIFeatureCard(
              icon: Icons.thermostat,
              title: 'Environmental Insights',
              description: 'Analyze your grow environment data',
              route: '/ai/insights',
              color: Colors.green,
            ),
            _AIFeatureCard(
              icon: Icons.local_hospital,
              title: 'Plant Health Analysis',
              description: 'Diagnose issues and get treatment recommendations',
              route: '/ai/health',
              color: Colors.red,
            ),
            _AIFeatureCard(
              icon: Icons.trending_up,
              title: 'Yield Prediction',
              description: 'Predict harvest yields and optimize results',
              route: '/ai/yield',
              color: Colors.purple,
            ),
            _AIFeatureCard(
              icon: Icons.lightbulb,
              title: 'Grow Guidance',
              description: 'Step-by-step growing instructions',
              route: '/ai/guidance',
              color: Colors.orange,
            ),
            _AIFeatureCard(
              icon: Icons.science,
              title: 'Strain Recommendations',
              description: 'Find the perfect strain for your needs',
              route: '/strains',
              color: Colors.teal,
            ),
          ],
        ),
      ],
    );
  }
}

class _AIFeatureCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String description;
  final String route;
  final Color color;

  const _AIFeatureCard({
    required this.icon,
    required this.title,
    required this.description,
    required this.route,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      color: const Color(0xFF2a2a2a),
      child: InkWell(
        onTap: () => context.go(route),
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: color.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Icon(icon, color: color, size: 24),
              ),
              const SizedBox(height: 12),
              Text(
                title,
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 4),
              Text(
                description,
                style: TextStyle(
                  color: Colors.white.withOpacity(0.7),
                  fontSize: 12,
                ),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _RecentAIActivity extends StatelessWidget {
  const _RecentAIActivity();

  @override
  Widget build(BuildContext context) {
    return const Card(
      color: Color(0xFF2a2a2a),
      child: Padding(
        padding: EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Recent AI Activity',
              style: TextStyle(
                color: Colors.white,
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 16),
            // TODO: Replace with actual activity data
            _EmptyActivityState(),
          ],
        ),
      ),
    );
  }
}

class _EmptyActivityState extends StatelessWidget {
  const _EmptyActivityState();

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            Icon(Icons.history, size: 48, color: Colors.white.withOpacity(0.3)),
            const SizedBox(height: 12),
            Text(
              'No recent AI activity',
              style: TextStyle(
                color: Colors.white.withOpacity(0.7),
                fontSize: 16,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Start using AI features to see activity here',
              style: TextStyle(
                color: Colors.white.withOpacity(0.5),
                fontSize: 12,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}

class _AIQuickTips extends StatelessWidget {
  const _AIQuickTips();

  @override
  Widget build(BuildContext context) {
    return const Card(
      color: Color(0xFF2a2a2a),
      child: Padding(
        padding: EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Quick Tips',
              style: TextStyle(
                color: Colors.white,
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 16),
            _TipCard(
              tip:
                  'Ask specific questions for better AI responses. Include details about your grow setup, strain, and current conditions.',
            ),
            SizedBox(height: 12),
            _TipCard(
              tip:
                  'Upload photos of your plants for accurate health analysis and issue diagnosis.',
            ),
            SizedBox(height: 12),
            _TipCard(
              tip:
                  'Use environmental data tracking to get personalized recommendations for optimal growing conditions.',
            ),
          ],
        ),
      ),
    );
  }
}

class _TipCard extends StatelessWidget {
  final String tip;

  const _TipCard({required this.tip});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: AppColors.primary500.withOpacity(0.1),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(
          color: AppColors.primary500.withOpacity(0.3),
          width: 1,
        ),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(Icons.lightbulb, color: AppColors.primary500, size: 20),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              tip,
              style: const TextStyle(color: Colors.white, fontSize: 14),
            ),
          ),
        ],
      ),
    );
  }
}
