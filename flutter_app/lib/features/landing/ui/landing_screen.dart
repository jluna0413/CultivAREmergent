import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'dart:ui';
import 'dart:math' as math;
import 'package:video_player/video_player.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:visibility_detector/visibility_detector.dart';
import 'package:flutter_animate/flutter_animate.dart';

class LandingScreen extends ConsumerStatefulWidget {
  const LandingScreen({super.key});

  @override
  ConsumerState<LandingScreen> createState() => _LandingScreenState();
}

class _LandingScreenState extends ConsumerState<LandingScreen> {
  late VideoPlayerController _videoController;
  late ScrollController _scrollController;
  bool _isVideoInitialized = false;

  @override
  void initState() {
    super.initState();
    _scrollController = ScrollController();
    _scrollController.addListener(_onScroll);

    _videoController =
        VideoPlayerController.asset('assets/videos/landing_video_optimized.mp4')
          ..initialize()
              .then((_) {
                _videoController.setLooping(true);
                _videoController.setVolume(0.0);
                _videoController.play();
                setState(() {
                  _isVideoInitialized = true;
                });
              })
              .catchError((error) {
                debugPrint('Error initializing video player: $error');
              });
  }

  void _onScroll() {
    if (!_videoController.value.isInitialized) return;

    // Optimize: Pause video if scrolled completely past the first viewport
    // The Hero section is roughly 1 screen height.
    final height = MediaQuery.of(context).size.height;
    if (_scrollController.offset > height) {
      if (_videoController.value.isPlaying) {
        _videoController.pause();
      }
    } else {
      if (!_videoController.value.isPlaying) {
        _videoController.play();
      }
    }
  }

  @override
  void dispose() {
    _videoController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint('DEBUG: LandingScreen building');
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final size = MediaQuery.of(context).size;

    return Scaffold(
      backgroundColor: Colors.black, // Base color
      body: Stack(
        children: [
          // 1. FIXED Video Background (Layer 0)
          // This creates the "Parallax" curtain effect. The video stays put,
          // and the content slides over it.
          if (_isVideoInitialized)
            Positioned.fill(
              child: FittedBox(
                fit: BoxFit.cover,
                child: SizedBox(
                  width: _videoController.value.size.width,
                  height: _videoController.value.size.height,
                  child: VideoPlayer(_videoController),
                ),
              ),
            )
          else
            Container(color: Colors.black),

          // 2. Video Overlay Gradient (for text readability on Hero)
          Positioned.fill(
            child: Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    Colors.black.withOpacity(0.3),
                    Colors.black.withOpacity(0.6),
                  ],
                ),
              ),
            ),
          ),

          // 3. Scrollable Content (Layer 1)
          CustomScrollView(
            controller: _scrollController,
            slivers: [
              // Sticky Glass Navbar
              SliverAppBar(
                pinned: true,
                floating: false,
                expandedHeight: 0,
                backgroundColor: Colors.transparent,
                flexibleSpace: ClipRRect(
                  child: BackdropFilter(
                    filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
                    child: Container(color: Colors.black.withOpacity(0.5)),
                  ),
                ),
                title: Row(
                  children: [
                    Icon(Icons.eco, color: colorScheme.primary),
                    const SizedBox(width: 8),
                    Text(
                      'CultivAR',
                      style: theme.textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.w700,
                        letterSpacing: -0.5,
                        color: Colors.white,
                      ),
                    ),
                  ],
                ),
                actions: [
                  TextButton(
                    onPressed: () => context.go('/login'),
                    child: const Text(
                      'Login',
                      style: TextStyle(color: Colors.white),
                    ),
                  ),
                  const SizedBox(width: 8),
                  FilledButton(
                    onPressed: () => context.go('/signup'),
                    style: FilledButton.styleFrom(
                      padding: const EdgeInsets.symmetric(horizontal: 20),
                    ),
                    child: const Text('Get Started'),
                  ),
                  const SizedBox(width: 16),
                ],
              ),

              // Hero Content (Transparent background so we see Fixed Video)
              SliverToBoxAdapter(
                child: SizedBox(
                  height: size.height, // Full viewport
                  child: const HeroContent(),
                ),
              ),

              // Partners Strip (Opaque)
              const SliverToBoxAdapter(child: PartnersSection()),

              // Full Viewport Feature Sections (Opaque backgrounds cover video)
              SliverList(
                delegate: SliverChildListDelegate([
                  // 1. Environmental Control (Image: Analytics Dashboard)
                  // Swapped per user request (Image fits control better)
                  FeatureSection(
                    title: 'Environmental Control',
                    description:
                        'Automate your climate. Connected HVAC and CO2 systems maintain perfect VPD for vegetative and flowering stages.',
                    icon: Icons.thermostat_outlined,
                    alignLeft: true,
                    background: Image.asset(
                      'assets/images/feature_analytics.png',
                      fit: BoxFit.cover,
                    ),
                  ),
                  // 2. Precision Analytics (Animation: Live Graph)
                  const FeatureSection(
                    title: 'Precision Analytics',
                    description:
                        'Real-time grower insights powered by advanced sensor arrays and AI models. Clinical precision for your canopy.',
                    icon: Icons.analytics_outlined,
                    alignLeft: false, // Alternating
                    background: AnalyticsGraphAnimation(),
                  ),
                  // 3. Smart Nutrient Calculator (Animation: Bubbles + Carousel)
                  const NutrientFeatureSection(),
                  // 4. Genetic Lineage (Image)
                  FeatureSection(
                    title: 'Genetic Lineage',
                    description:
                        'Trace ancestry with our immutable blockchain registry. Verify phenotypes and stabilization generations.',
                    icon: Icons.account_tree_outlined,
                    alignLeft: true, // Alternating
                    background: Image.asset(
                      'assets/images/feature_genetics.png',
                      fit: BoxFit.cover,
                    ),
                  ),
                  // 5. Decentralized Marketplace (Image)
                  FeatureSection(
                    title: 'Decentralized Marketplace',
                    description:
                        'Trade exclusive genetics and equipment directly with verified breeders. Peer-to-peer, secure, and transparent.',
                    icon: Icons.storefront_outlined,
                    alignLeft: false, // Right aligned text
                    background: Image.asset(
                      'assets/images/feature_marketplace.png',
                      fit: BoxFit.cover,
                    ),
                  ),
                ]),
              ),

              // Footer
              SliverToBoxAdapter(
                child: Container(
                  padding: const EdgeInsets.all(48),
                  color: Colors.black,
                  child: Column(
                    children: [
                      const Icon(Icons.eco, size: 40, color: Colors.white24),
                      const SizedBox(height: 24),
                      Text(
                        'CultivAR © 2025',
                        style: theme.textTheme.bodyMedium?.copyWith(
                          color: Colors.white54,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class HeroContent extends StatelessWidget {
  const HeroContent({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Center(
      child: ClipRRect(
        borderRadius: BorderRadius.circular(24),
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
          child: Container(
            constraints: const BoxConstraints(maxWidth: 600),
            padding: const EdgeInsets.all(40),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.05),
              border: Border.all(color: Colors.white.withOpacity(0.1)),
              borderRadius: BorderRadius.circular(28),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.3),
                  blurRadius: 40,
                  spreadRadius: -10,
                ),
              ],
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(Icons.eco_rounded, size: 80, color: colorScheme.primary),
                const SizedBox(height: 32),
                Text(
                  'CultivAR',
                  style: theme.textTheme.displayMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.5,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  'Genetic Excellence & Cultivation Intelligence',
                  textAlign: TextAlign.center,
                  style: theme.textTheme.titleLarge?.copyWith(
                    color: Colors.white,
                    letterSpacing: 0.5,
                  ),
                ),
                const SizedBox(height: 48),
                Wrap(
                  spacing: 16,
                  runSpacing: 16,
                  alignment: WrapAlignment.center,
                  children: [
                    FilledButton.icon(
                      onPressed: () => context.go('/signup'),
                      icon: const Icon(Icons.rocket_launch_rounded),
                      label: const Text('Join Waitlist'),
                      style: FilledButton.styleFrom(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 32,
                          vertical: 20,
                        ),
                      ),
                    ),
                    OutlinedButton.icon(
                      onPressed: () => context.go('/login'),
                      icon: const Icon(Icons.login_rounded),
                      label: const Text('Become a Founder'),
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 32,
                          vertical: 20,
                        ),
                        side: const BorderSide(color: Colors.white),
                        foregroundColor: Colors.white,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class FeatureSection extends StatelessWidget {
  final String title;
  final String description;
  final IconData icon;
  final bool alignLeft;
  final Widget background;

  const FeatureSection({
    super.key,
    required this.title,
    required this.description,
    required this.icon,
    required this.background,
    this.alignLeft = true,
  });

  void _showFeatureDetails(BuildContext context) {
    String detailContent = '';
    switch (title) {
      case 'Environmental Control':
        detailContent =
            'Our system integrates with industry leaders like AC Infinity and TrolMaster to provide hospital-grade climate automation. Set target VPD curves, automate CO2 injection, and monitor root zone metrics from anywhere in the world.';
        break;
      case 'Precision Analytics':
        detailContent =
            'Stop guessing. CultivAR uses machine learning to analyze your sensor data against optimal growth models. Detect HVAC failures before they become crop failures and visualize your facility\'s health with real-time heatmaps.';
        break;
      case 'Smart Nutrient Calculator':
        detailContent =
            'Balances NPK ratios automatically based on your selected nutrient line and growth phase. Supports vegetative steering to reduce stretch or generative steering to bulk flowers.';
        break;
      case 'Genetic Lineage':
        detailContent =
            'Mint your unique phenotypes as Soulbound Tokens (SBTs) on the blockchain. Prove ownership of your breeder cuts and track the family tree of every clone you sell.';
        break;
      case 'Decentralized Marketplace':
        detailContent =
            'A peer-to-peer exchange for verified genetics. No middlemen, no questionable clones. Breeder validation ensures you get exactly what you paid for.';
        break;
      default:
        detailContent = '$title coming soon.';
    }

    showDialog(
      context: context,
      builder: (context) => Dialog(
        backgroundColor: Colors.transparent,
        child: ClipRRect(
          borderRadius: BorderRadius.circular(24),
          child: BackdropFilter(
            filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
            child: Container(
              constraints: const BoxConstraints(maxWidth: 500),
              padding: const EdgeInsets.all(32),
              decoration: BoxDecoration(
                color: Colors.black.withOpacity(0.8),
                borderRadius: BorderRadius.circular(24),
                border: Border.all(color: Colors.white24),
                boxShadow: [
                  BoxShadow(
                    color: Theme.of(
                      context,
                    ).colorScheme.primary.withOpacity(0.2),
                    blurRadius: 20,
                    spreadRadius: 2,
                  ),
                ],
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(
                    icon,
                    size: 48,
                    color: Theme.of(context).colorScheme.primary,
                  ),
                  const SizedBox(height: 24),
                  Text(
                    title,
                    style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    detailContent,
                    style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                      color: Colors.white70,
                      height: 1.6,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 32),
                  FilledButton(
                    onPressed: () => Navigator.of(context).pop(),
                    child: const Text('Close'),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final size = MediaQuery.of(context).size;

    return SizedBox(
      height: size.height, // Full Viewport
      width: size.width,
      child: Stack(
        fit: StackFit.expand,
        children: [
          // 1. Background (Image or Animation)
          background,

          // 2. Dark Overlay for Contrast
          Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [
                  Colors.black.withOpacity(0.6),
                  Colors.black.withOpacity(0.8),
                ],
              ),
            ),
          ),

          // 3. Content Card
          Align(
            alignment: alignLeft ? Alignment.centerLeft : Alignment.centerRight,
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 48, vertical: 80),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(24),
                child: BackdropFilter(
                  filter: ImageFilter.blur(sigmaX: 12, sigmaY: 12),
                  child: Container(
                    constraints: const BoxConstraints(maxWidth: 500),
                    padding: const EdgeInsets.all(40),
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        colors: [
                          const Color(
                            0xFF00FF00,
                          ).withOpacity(0.25), // Electric Green
                          const Color(0xFF8A2BE2).withOpacity(0.25), // Violet
                        ],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      border: Border.all(color: Colors.white.withOpacity(0.2)),
                      borderRadius: BorderRadius.circular(24),
                    ),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Container(
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: colorScheme.primary.withOpacity(0.2),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Icon(
                            icon,
                            size: 32,
                            color: colorScheme.primary,
                          ),
                        ),
                        const SizedBox(height: 24),
                        _ScrollAnimated(
                          child: Text(
                            title,
                            style: theme.textTheme.headlineMedium?.copyWith(
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                            ),
                          ),
                        ),
                        const SizedBox(height: 16),
                        _ScrollAnimated(
                          delay: 200.ms,
                          child: Text(
                            description,
                            style: theme.textTheme.titleMedium?.copyWith(
                              color: Colors.white70,
                              height: 1.5,
                            ),
                          ),
                        ),
                        const SizedBox(height: 32),
                        TextButton.icon(
                          onPressed: () => _showFeatureDetails(context),
                          icon: const Icon(
                            Icons.arrow_forward,
                            color: Colors.white,
                          ),
                          label: const Text(
                            'Read More',
                            style: TextStyle(color: Colors.white),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class PartnersSection extends StatelessWidget {
  const PartnersSection({super.key});

  final List<Map<String, String>> _partners = const [
    {
      'name': 'AC Infinity',
      'path': 'assets/images/manufacturers/ac_infinity_logo.svg',
    },
    {'name': 'Vivosun', 'path': 'assets/images/manufacturers/vivosun_logo.svg'},
    {
      'name': 'Spider Farmer',
      'path': 'assets/images/manufacturers/spider_farmer_logo.png',
    },
    // {
    //   'name': 'TrolMaster',
    //   'path': 'assets/images/manufacturers/trolmaster_logo.png',
    // },
    // {'name': 'Quest', 'path': 'assets/images/manufacturers/quest_logo.png'},
    // {'name': 'HLG', 'path': 'assets/images/manufacturers/hlg_logo.png'},
  ];

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 40),
      color: Colors.black,
      child: Column(
        children: [
          _ScrollAnimated(
            child: Text(
              'TRUSTED HARDWARE INTEGRATIONS',
              style: Theme.of(context).textTheme.labelLarge?.copyWith(
                letterSpacing: 2.0,
                color: Colors.white54,
              ),
            ),
          ),
          const SizedBox(height: 24),
          const SizedBox(height: 24),
          Center(
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: _partners.map((partner) {
                  return Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 20),
                    child: _PartnerLogo(
                      assetPath: partner['path']!,
                      name: partner['name']!,
                    ),
                  );
                }).toList(),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _PartnerLogo extends StatelessWidget {
  final String assetPath;
  final String name;

  const _PartnerLogo({required this.assetPath, required this.name});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 70,
      width: 200,
      padding: EdgeInsets.zero, // Remove padding
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            Colors.green.shade900.withOpacity(0.6),
            const Color(0xFFC6F6D5).withOpacity(0.3), // Light Green/Yellow-ish
            Colors.green.shade900.withOpacity(0.6),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          stops: const [0.0, 0.5, 1.0],
        ),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.green.withOpacity(0.3)),
        boxShadow: [
          BoxShadow(
            color: Colors.green.withOpacity(0.1),
            blurRadius: 10,
            spreadRadius: 2,
          ),
        ],
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(16),
        child: assetPath.toLowerCase().endsWith('.svg')
            ? SvgPicture.asset(assetPath, fit: BoxFit.contain)
            : Image.asset(
                assetPath,
                fit: BoxFit.contain, // Fill
                errorBuilder: (context, error, stackTrace) => Center(
                  child: Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Text(
                      name,
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        color: Colors.white70,
                        fontSize: 12,
                      ),
                    ),
                  ),
                ),
              ),
      ),
    );
  }
}

class NutrientFeatureSection extends StatelessWidget {
  const NutrientFeatureSection({super.key});

  final List<Map<String, String>> _nutrients = const [
    // {'name': 'Athena', 'path': 'assets/images/manufacturers/athena_logo.png'},
    // {'name': 'Gavita', 'path': 'assets/images/manufacturers/gavita_logo.png'},
    // {'name': 'Canna', 'path': 'assets/images/manufacturers/canna_logo.png'},
    // {'name': 'Biobizz', 'path': 'assets/images/manufacturers/biobizz_logo.png'},
    // {
    //   'name': 'General Hydroponics',
    //   'path': 'assets/images/manufacturers/gh_logo.png',
    // },
  ];

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final size = MediaQuery.of(context).size;

    return SizedBox(
      height: size.height,
      width: size.width,
      child: Stack(
        fit: StackFit.expand,
        children: [
          // 1. Background
          const BubblesAnimation(),

          // 2. Overlay
          Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [
                  Colors.black.withOpacity(0.6),
                  Colors.black.withOpacity(0.9),
                ],
              ),
            ),
          ),

          // 3. Content
          Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // Text Content
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 24),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(24),
                  child: BackdropFilter(
                    filter: ImageFilter.blur(sigmaX: 12, sigmaY: 12),
                    child: Container(
                      constraints: const BoxConstraints(maxWidth: 800),
                      padding: const EdgeInsets.all(40),
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          colors: [
                            const Color(
                              0xFF00FF00,
                            ).withOpacity(0.25), // Electric Green
                            const Color(0xFF8A2BE2).withOpacity(0.25), // Violet
                          ],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                        border: Border.all(
                          color: Colors.white.withOpacity(0.2),
                        ),
                        borderRadius: BorderRadius.circular(24),
                      ),
                      child: Column(
                        children: [
                          Icon(
                            Icons.science_outlined,
                            size: 48,
                            color: colorScheme.secondary,
                          ),
                          const SizedBox(height: 24),
                          _ScrollAnimated(
                            child: Text(
                              'Smart Nutrient Calculator',
                              textAlign: TextAlign.center,
                              style: theme.textTheme.headlineMedium?.copyWith(
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                              ),
                            ),
                          ),
                          const SizedBox(height: 16),
                          _ScrollAnimated(
                            delay: 200.ms,
                            child: Text(
                              'Precise EC/PPM targets for every stage. Auto-balancing for major nutrient lines, crop steering, and custom recipes.',
                              textAlign: TextAlign.center,
                              style: theme.textTheme.titleLarge?.copyWith(
                                color: Colors.white70,
                                height: 1.5,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),

              const SizedBox(height: 60),

              // Carousel Label
              _ScrollAnimated(
                child: Text(
                  'SUPPORTED NUTRIENT LINES',
                  style: theme.textTheme.labelLarge?.copyWith(
                    letterSpacing: 2.0,
                    color: Colors.white54,
                  ),
                ),
              ),
              const SizedBox(height: 24),

              // Nutrient Row (Centered)
              Center(
                child: SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: _nutrients.map((nutrient) {
                      return Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 20),
                        child: _NutrientLogo(
                          assetPath: nutrient['path']!,
                          name: nutrient['name']!,
                        ),
                      );
                    }).toList(),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _NutrientLogo extends StatelessWidget {
  final String assetPath;
  final String name;

  const _NutrientLogo({required this.assetPath, required this.name});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 200,
      padding: EdgeInsets.zero, // Remove padding to fill card
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            Colors.green.shade900.withOpacity(0.6),
            const Color(0xFFC6F6D5).withOpacity(0.3), // Light Green/Yellow-ish
            Colors.green.shade900.withOpacity(0.6),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          stops: const [0.0, 0.5, 1.0],
        ),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.green.withOpacity(0.3)),
        boxShadow: [
          BoxShadow(
            color: Colors.green.withOpacity(0.1),
            blurRadius: 10,
            spreadRadius: 2,
          ),
        ],
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(16),
        child: Image.asset(
          assetPath,
          fit: BoxFit.contain, // Fill as much as possible without crop
          errorBuilder: (context, error, stackTrace) => Center(
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                name,
                textAlign: TextAlign.center,
                style: const TextStyle(color: Colors.white70, fontSize: 12),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class BubblesAnimation extends StatefulWidget {
  const BubblesAnimation({super.key});

  @override
  State<BubblesAnimation> createState() => _BubblesAnimationState();
}

class _BubblesAnimationState extends State<BubblesAnimation>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  final List<_Bubble> _bubbles = [];

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 10),
    )..repeat();
    for (int i = 0; i < 20; i++) {
      _bubbles.add(_Bubble());
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        for (var bubble in _bubbles) {
          bubble.y -= bubble.speed;
          if (bubble.y < -0.1) {
            bubble.y = 1.1;
            bubble.x = math.Random().nextDouble();
          }
        }
        return CustomPaint(painter: _BubblePainter(_bubbles));
      },
    );
  }
}

class _Bubble {
  double x = math.Random().nextDouble();
  double y = math.Random().nextDouble();
  double size = math.Random().nextDouble() * 10 + 5;
  double speed = math.Random().nextDouble() * 0.002 + 0.001;
}

class _BubblePainter extends CustomPainter {
  final List<_Bubble> bubbles;
  _BubblePainter(this.bubbles);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.purple.withOpacity(0.3)
      ..style = PaintingStyle.fill;

    for (var bubble in bubbles) {
      canvas.drawCircle(
        Offset(bubble.x * size.width, bubble.y * size.height),
        bubble.size,
        paint,
      );
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}

/// ANIMATIONS

class AnalyticsGraphAnimation extends StatefulWidget {
  const AnalyticsGraphAnimation({super.key});

  @override
  State<AnalyticsGraphAnimation> createState() =>
      _AnalyticsGraphAnimationState();
}

class _AnalyticsGraphAnimationState extends State<AnalyticsGraphAnimation> {
  final List<FlSpot> _vpdPoints = [];
  final List<FlSpot> _tempPoints = [];
  final List<FlSpot> _rhPoints = [];
  double _xValue = 0;
  // ignore: unused_field
  late final Stream<void> _timer;

  double _currentVpd = 1.2;
  double _currentTemp = 75.0;
  double _currentRh = 60.0;

  @override
  void initState() {
    super.initState();
    // Pre-populate
    for (int i = 0; i < 40; i++) {
      _updatePoints();
    }
    // Live update
    _timer = Stream.periodic(const Duration(milliseconds: 200), (_) {
      if (mounted) {
        setState(() {
          _updatePoints();
        });
      }
    });
  }

  void _updatePoints() {
    _xValue += 1;
    // Simulate data: Sine wave with noise
    _currentVpd =
        1.0 +
        0.3 * math.sin(_xValue * 0.1) +
        (math.Random().nextDouble() - 0.5) * 0.1;
    _currentTemp =
        75.0 +
        5 * math.cos(_xValue * 0.05) +
        (math.Random().nextDouble() - 0.5) * 1;
    _currentRh =
        60.0 +
        10 * math.sin(_xValue * 0.08) +
        (math.Random().nextDouble() - 0.5) * 2;

    _vpdPoints.add(FlSpot(_xValue, _currentVpd));
    // Normalize Temp/RH for chart scaling (visual only)
    // Map 65-85F to 0.5-2.5 range
    _tempPoints.add(FlSpot(_xValue, (_currentTemp - 65) / 10));
    // Map 40-80% to 0.5-2.5 range
    _rhPoints.add(FlSpot(_xValue, (_currentRh - 40) / 20));
  }

  @override
  Widget build(BuildContext context) {
    // Keep last 40 points
    final vpdShow = _vpdPoints.length > 40
        ? _vpdPoints.sublist(_vpdPoints.length - 40)
        : _vpdPoints;
    final tempShow = _tempPoints.length > 40
        ? _tempPoints.sublist(_tempPoints.length - 40)
        : _tempPoints;
    // final rhShow = _rhPoints.length > 40 ? _rhPoints.sublist(_rhPoints.length - 40) : _rhPoints;

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.black.withOpacity(0.4),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white10),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Header Stats
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              _StatBadge(
                label: 'VPD',
                value: '${_currentVpd.toStringAsFixed(2)} kPa',
                color: const Color(0xFF00E676),
              ),
              _StatBadge(
                label: 'TEMP',
                value: '${_currentTemp.toStringAsFixed(1)}°F',
                color: Colors.blueAccent,
              ),
              _StatBadge(
                label: 'RH',
                value: '${_currentRh.toStringAsFixed(1)}%',
                color: Colors.purpleAccent,
              ),
            ],
          ),
          const SizedBox(height: 20),
          // Chart
          SizedBox(
            height: 180,
            child: LineChart(
              LineChartData(
                gridData: FlGridData(
                  show: true,
                  drawVerticalLine: true,
                  horizontalInterval: 0.5,
                  verticalInterval: 5,
                  getDrawingHorizontalLine: (value) {
                    return FlLine(
                      color: Colors.white.withOpacity(0.05),
                      strokeWidth: 1,
                      dashArray: [5, 5],
                    );
                  },
                  getDrawingVerticalLine: (value) {
                    return FlLine(
                      color: Colors.white.withOpacity(0.05),
                      strokeWidth: 1,
                    );
                  },
                ),
                titlesData: const FlTitlesData(show: false),
                borderData: FlBorderData(show: false),
                minX: vpdShow.first.x,
                maxX: vpdShow.last.x,
                minY: 0.0,
                maxY: 3.0,
                lineBarsData: [
                  // Temp Line
                  LineChartBarData(
                    spots: tempShow,
                    isCurved: true,
                    color: Colors.blueAccent.withOpacity(0.5),
                    barWidth: 2,
                    isStrokeCapRound: true,
                    dotData: const FlDotData(show: false),
                  ),
                  // VPD Line (Main)
                  LineChartBarData(
                    spots: vpdShow,
                    isCurved: true,
                    color: const Color(0xFF00E676),
                    barWidth: 3,
                    isStrokeCapRound: true,
                    dotData: const FlDotData(show: true), // Show dots?
                    belowBarData: BarAreaData(
                      show: true,
                      gradient: LinearGradient(
                        colors: [
                          const Color(0xFF00E676).withOpacity(0.2),
                          const Color(0xFF00E676).withOpacity(0.0),
                        ],
                        begin: Alignment.topCenter,
                        end: Alignment.bottomCenter,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _StatBadge extends StatelessWidget {
  final String label;
  final String value;
  final Color color;

  const _StatBadge({
    required this.label,
    required this.value,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          label,
          style: TextStyle(
            color: Colors.white54,
            fontSize: 10,
            fontWeight: FontWeight.bold,
            letterSpacing: 1.0,
          ),
        ),
        const SizedBox(height: 4),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
          decoration: BoxDecoration(
            color: color.withOpacity(0.1),
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: color.withOpacity(0.3)),
          ),
          child: Text(
            value,
            style: TextStyle(
              color: color,
              fontWeight: FontWeight.bold,
              fontFamily: 'monospace',
            ),
          ),
        ),
      ],
    );
  }
}

class AtmosphereAnimation extends StatefulWidget {
  const AtmosphereAnimation({super.key});

  @override
  State<AtmosphereAnimation> createState() => _AtmosphereAnimationState();
}

class _AtmosphereAnimationState extends State<AtmosphereAnimation>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 10),
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return Container(
          decoration: BoxDecoration(
            gradient: RadialGradient(
              center: Alignment(
                math.sin(_controller.value * 2 * math.pi) * 0.5,
                math.cos(_controller.value * 2 * math.pi) * 0.5,
              ),
              radius: 1.5,
              colors: [
                Colors.blue.shade900,
                Colors.teal.shade900,
                Colors.black,
              ],
              stops: const [0.0, 0.5, 1.0],
            ),
          ),
        );
      },
    );
  }
}

class NetworkAnimation extends StatefulWidget {
  const NetworkAnimation({super.key});

  @override
  State<NetworkAnimation> createState() => _NetworkAnimationState();
}

class _NetworkAnimationState extends State<NetworkAnimation>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  final List<_Node> _nodes = [];
  final int _nodeCount = 40;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 10),
    )..repeat();

    // Initialize random nodes
    final random = math.Random();
    for (int i = 0; i < _nodeCount; i++) {
      _nodes.add(
        _Node(
          x: random.nextDouble(),
          y: random.nextDouble(),
          dx: (random.nextDouble() - 0.5) * 0.002,
          dy: (random.nextDouble() - 0.5) * 0.002,
        ),
      );
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        // Update nodes
        for (var node in _nodes) {
          node.x += node.dx;
          node.y += node.dy;

          // Bounce
          if (node.x < 0 || node.x > 1) node.dx *= -1;
          if (node.y < 0 || node.y > 1) node.dy *= -1;
        }

        return CustomPaint(painter: _NetworkPainter(_nodes));
      },
    );
  }
}

class _Node {
  double x, y, dx, dy;
  _Node({required this.x, required this.y, required this.dx, required this.dy});
}

class _NetworkPainter extends CustomPainter {
  final List<_Node> nodes;

  _NetworkPainter(this.nodes);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.greenAccent.withOpacity(0.5)
      ..style = PaintingStyle.fill;
    final linePaint = Paint()
      ..color = Colors.greenAccent.withOpacity(0.1)
      ..strokeWidth = 1.0;

    for (int i = 0; i < nodes.length; i++) {
      final nodeA = nodes[i];
      final pointA = Offset(nodeA.x * size.width, nodeA.y * size.height);

      // Draw node
      canvas.drawCircle(pointA, 3.0, paint);

      // Draw lines
      for (int j = i + 1; j < nodes.length; j++) {
        final nodeB = nodes[j];
        final pointB = Offset(nodeB.x * size.width, nodeB.y * size.height);

        final distance = (pointA - pointB).distance;
        if (distance < 150) {
          // Fade line based on distance
          linePaint.color = Colors.greenAccent.withOpacity(
            (1.0 - distance / 150) * 0.3,
          );
          canvas.drawLine(pointA, pointB, linePaint);
        }
      }
    }
  }

  @override
  bool shouldRepaint(_NetworkPainter oldDelegate) => true;
}

class _ScrollAnimated extends StatefulWidget {
  final Widget child;
  final Duration delay;
  const _ScrollAnimated({required this.child, this.delay = Duration.zero});

  @override
  State<_ScrollAnimated> createState() => _ScrollAnimatedState();
}

class _ScrollAnimatedState extends State<_ScrollAnimated> {
  bool _visible = false;

  @override
  Widget build(BuildContext context) {
    return VisibilityDetector(
      key: Key(widget.hashCode.toString()),
      onVisibilityChanged: (info) {
        if (!_visible && info.visibleFraction > 0.1) {
          setState(() {
            _visible = true;
          });
        }
      },
      child: _visible
          ? widget.child
                .animate(delay: widget.delay)
                .fade(duration: 600.ms)
                .slideY(
                  begin: 0.3,
                  end: 0,
                  duration: 600.ms,
                  curve: Curves.easeOut,
                )
          : Opacity(opacity: 0, child: widget.child),
    );
  }
}
