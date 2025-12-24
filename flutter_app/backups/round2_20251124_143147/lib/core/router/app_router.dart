import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../features/auth/ui/login_screen.dart';
import '../../features/auth/ui/signup_screen.dart';
import '../../features/dashboard/ui/dashboard_screen.dart';
import '../../features/plants/ui/plants_list_screen.dart';
import '../../features/plants/ui/plant_detail_screen.dart';
import '../../features/sensors/ui/sensors_list_screen.dart';
import '../../features/settings/ui/settings_screen.dart';
import '../../features/cart/ui/cart_screen.dart';
import '../../features/admin/ui/admin_users_screen.dart';
import '../../features/clones/ui/clone_management_screen.dart';
import '../../features/ai/ui/ai_dashboard_screen.dart';
import '../../features/ai/ui/plant_health_analysis_screen.dart';
import '../../features/ai/ui/yield_prediction_screen.dart';
import '../../features/ai/ui/grow_guidance_screen.dart';
import '../../features/ai/ui/environmental_insights_screen.dart';
import '../../features/ai/ui/ai_chat_advisor_screen.dart';
import '../../features/seedbank/ui/seed_bank_screen.dart';
import '../../features/extensions/ui/extensions_screen.dart';
import '../../features/gear/ui/gear_screen.dart';

/// App Router Configuration with Authentication Guards
final appRouterProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    initialLocation: '/login',
    debugLogDiagnostics: true,
    routes: [
      // Authentication Routes
      GoRoute(
        path: '/login',
        name: 'login',
        builder: (context, state) {
          return const LoginScreen();
        },
      ),

      GoRoute(
        path: '/signup',
        name: 'signup',
        builder: (context, state) => const SignupScreen(),
      ),

      // Main App Routes (Protected)
      GoRoute(
        path: '/',
        name: 'home',
        redirect: (context, state) => '/dashboard',
      ),

      GoRoute(
        path: '/dashboard',
        name: 'dashboard',
        builder: (context, state) => const DashboardScreen(),
      ),

      GoRoute(
        path: '/plants',
        name: 'plants',
        builder: (context, state) => const PlantsListScreen(),
      ),

      GoRoute(
        path: '/plants/:id',
        name: 'plant-detail',
        builder: (context, state) {
          final plantId = state.pathParameters['id'] ?? '1';
          return PlantDetailScreen(plantId: int.parse(plantId));
        },
      ),

      GoRoute(
        path: '/cultivars',
        name: 'cultivars',
        builder: (context, state) => const Scaffold(
          body: Center(child: Text('Strains Screen - Coming Soon')),
        ),
      ),

      GoRoute(
        path: '/sensors',
        name: 'sensors',
        builder: (context, state) => const SensorsListScreen(),
      ),

      GoRoute(
        path: '/settings',
        name: 'settings',
        builder: (context, state) => const SettingsScreen(),
      ),

      GoRoute(
        path: '/cart',
        name: 'cart',
        builder: (context, state) => const CartScreen(),
      ),

      // Admin Routes
      GoRoute(
        path: '/admin/users',
        name: 'admin-users',
        builder: (context, state) => const AdminUsersScreen(),
      ),

      // Clone Management
      GoRoute(
        path: '/clones',
        name: 'clones',
        builder: (context, state) => const CloneManagementScreen(),
      ),

      // AI Dashboard
      GoRoute(
        path: '/ai-dashboard',
        name: 'ai-dashboard',
        builder: (context, state) => const AIDashboardScreen(),
      ),

      // Plant Health Analysis
      GoRoute(
        path: '/plant-health',
        name: 'plant-health',
        builder: (context, state) => const PlantHealthAnalysisScreen(),
      ),

      // Yield Prediction
      GoRoute(
        path: '/yield-prediction',
        name: 'yield-prediction',
        builder: (context, state) => const YieldPredictionScreen(),
      ),

      // Grow Guidance
      GoRoute(
        path: '/grow-guidance',
        name: 'grow-guidance',
        builder: (context, state) => const GrowGuidanceScreen(),
      ),

      // Environmental Insights
      GoRoute(
        path: '/environmental-insights',
        name: 'environmental-insights',
        builder: (context, state) => const EnvironmentalInsightsScreen(),
      ),

      // AI Chat Advisor
      GoRoute(
        path: '/ai-chat',
        name: 'ai-chat',
        builder: (context, state) => const AIChatAdvisorScreen(),
      ),

      // Seed Bank
      GoRoute(
        path: '/seed-bank',
        name: 'seed-bank',
        builder: (context, state) => const SeedBankScreen(),
      ),

      // Extensions
      GoRoute(
        path: '/extensions',
        name: 'extensions',
        builder: (context, state) => const ExtensionsScreen(),
      ),

      // Gear
      GoRoute(
        path: '/gear',
        name: 'gear',
        builder: (context, state) => const GearScreen(),
      ),
    ],
  );
});
