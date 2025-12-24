// lib/features/onboarding/ui/onboarding_tutorial_overlay.dart

import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';

/// Welcome overlay shown immediately after registration
/// Introduces the user to CultivAR with animated content
class OnboardingTutorialOverlay extends StatefulWidget {
  final VoidCallback? onDismiss;

  const OnboardingTutorialOverlay({super.key, this.onDismiss});

  @override
  State<OnboardingTutorialOverlay> createState() =>
      _OnboardingTutorialOverlayState();
}

class _OnboardingTutorialOverlayState extends State<OnboardingTutorialOverlay> {
  int _currentPage = 0;
  final PageController _pageController = PageController();

  final List<_WelcomeSlide> _slides = [
    const _WelcomeSlide(
      icon: Icons.eco,
      title: 'Welcome to CultivAR',
      description:
          'Your personal grow journal with smart tracking, AI assistance, and hardware integration.',
    ),
    const _WelcomeSlide(
      icon: Icons.grain,
      title: 'Track Your Genetics',
      description:
          'Build your seed collection, track lineage, and never lose track of your favorite strains.',
    ),
    const _WelcomeSlide(
      icon: Icons.home_outlined,
      title: 'Design Your Space',
      description:
          'Visualize your grow tent layout with smart pot spacing based on plant canopy size.',
    ),
    const _WelcomeSlide(
      icon: Icons.sensors,
      title: 'Connect Your Hardware',
      description:
          'Integrate with AC Infinity, Ecowitt, and more for automated environment monitoring.',
    ),
  ];

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Material(
      color: Color.alphaBlend(colorScheme.scrim.withAlpha(230), Colors.black),
      child: SafeArea(
        child: Column(
          children: [
            // Skip button
            Align(
              alignment: Alignment.topRight,
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: TextButton(
                  onPressed: _dismiss,
                  child: Text(
                    'Skip',
                    style: TextStyle(color: colorScheme.onSurface),
                  ),
                ),
              ),
            ).animate().fadeIn(delay: 500.ms),

            // Page content
            Expanded(
              child: PageView.builder(
                controller: _pageController,
                itemCount: _slides.length,
                onPageChanged: (index) {
                  setState(() => _currentPage = index);
                },
                itemBuilder: (context, index) {
                  return _buildSlide(_slides[index], theme, colorScheme);
                },
              ),
            ),

            // Page indicators
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 24),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: List.generate(_slides.length, (index) {
                  return AnimatedContainer(
                    duration: const Duration(milliseconds: 200),
                    margin: const EdgeInsets.symmetric(horizontal: 4),
                    width: _currentPage == index ? 24 : 8,
                    height: 8,
                    decoration: BoxDecoration(
                      color: _currentPage == index
                          ? colorScheme.primary
                          : colorScheme.onSurface.withAlpha(76),
                      borderRadius: BorderRadius.circular(4),
                    ),
                  );
                }),
              ),
            ),

            // Action buttons
            Padding(
              padding: const EdgeInsets.fromLTRB(24, 0, 24, 32),
              child: Row(
                children: [
                  if (_currentPage > 0)
                    Expanded(
                      child: OutlinedButton(
                        onPressed: () {
                          _pageController.previousPage(
                            duration: const Duration(milliseconds: 300),
                            curve: Curves.easeInOut,
                          );
                        },
                        style: OutlinedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 16),
                          side: BorderSide(color: colorScheme.onSurface),
                          foregroundColor: colorScheme.onSurface,
                        ),
                        child: const Text('Back'),
                      ),
                    )
                  else
                    const Spacer(),
                  const SizedBox(width: 16),
                  Expanded(
                    child: FilledButton(
                      onPressed: () {
                        if (_currentPage == _slides.length - 1) {
                          _startOnboarding();
                        } else {
                          _pageController.nextPage(
                            duration: const Duration(milliseconds: 300),
                            curve: Curves.easeInOut,
                          );
                        }
                      },
                      style: FilledButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 16),
                      ),
                      child: Text(
                        _currentPage == _slides.length - 1
                            ? "Let's Go!"
                            : 'Next',
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSlide(
    _WelcomeSlide slide,
    ThemeData theme,
    ColorScheme colorScheme,
  ) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 48),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            padding: const EdgeInsets.all(32),
            decoration: BoxDecoration(
              color: colorScheme.primary.withAlpha(51),
              shape: BoxShape.circle,
            ),
            child: Icon(slide.icon, size: 80, color: colorScheme.primary),
          ).animate().fadeIn(duration: 400.ms).scaleXY(begin: 0.8, end: 1),
          const SizedBox(height: 48),
          Text(
                slide.title,
                style: theme.textTheme.headlineMedium?.copyWith(
                  color: colorScheme.onSurface,
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
              )
              .animate()
              .fadeIn(delay: 200.ms, duration: 400.ms)
              .slideY(begin: 0.2),
          const SizedBox(height: 16),
          Text(
                slide.description,
                style: theme.textTheme.bodyLarge?.copyWith(
                  color: colorScheme.onSurface.withAlpha(204),
                ),
                textAlign: TextAlign.center,
              )
              .animate()
              .fadeIn(delay: 400.ms, duration: 400.ms)
              .slideY(begin: 0.2),
        ],
      ),
    );
  }

  void _dismiss() {
    widget.onDismiss?.call();
    context.go('/onboarding/genetics');
  }

  void _startOnboarding() {
    widget.onDismiss?.call();
    context.go('/onboarding/genetics');
  }
}

class _WelcomeSlide {
  final IconData icon;
  final String title;
  final String description;

  const _WelcomeSlide({
    required this.icon,
    required this.title,
    required this.description,
  });
}
