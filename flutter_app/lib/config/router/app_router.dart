import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:cultivar_app/core/providers/auth_provider.dart';

// Auth screens
import '../../features/landing/ui/landing_screen.dart';
import '../../features/auth/ui/login_screen.dart';
import '../../features/auth/ui/signup_screen.dart';
import '../../features/auth/ui/forgot_password_screen.dart';
import '../../features/auth/ui/oauth_callback_screen.dart';
import '../../features/auth/ui/change_password_screen.dart';

// Dashboard
import '../../features/dashboard/ui/dashboard_screen.dart';
import '../../features/dashboard/screens/breeder_dashboard_screen.dart';

// Plants
import '../../features/plants/ui/plants_list_screen.dart';
import '../../features/plants/ui/plant_detail_screen.dart';
import '../../features/plants/ui/plant_form_screen.dart';
import '../../features/genetics/screens/genetics_library_screen.dart';

// Sensors
import '../../features/sensors/ui/sensors_screen_comprehensive.dart';
import '../../features/sensors/ui/sensor_config_screen.dart';

// Strains/Cultivars
// Strains/Cultivars
import '../../features/strains/ui/strains_list_screen.dart';
// import '../../features/strains/ui/cultivar_detail_screen.dart';
import '../../features/genetics/screens/genetics_detail_screen.dart';
import '../../features/marketplace/screens/marketplace_screen.dart'; // New

// Clones
import '../../features/clones/ui/clone_management_screen.dart';

// Nutrients
import '../../screens/nutrient_calculator_screen.dart';
import '../../screens/nutrient_inventory_screen.dart';

// Settings
import '../../features/settings/ui/settings_screen.dart';

// Cart & Market
import '../../features/cart/ui/cart_screen.dart';
import '../../features/cart/screens/checkout_screen.dart';
import '../../features/redemption/screens/redemption_screen.dart';
import '../../features/seedbank/ui/seed_bank_screen.dart';
import '../../features/gear/ui/gear_screen.dart';
import '../../features/extensions/ui/extensions_screen.dart';

// Admin
import '../../features/admin/ui/admin_dashboard_screen.dart';
import '../../features/admin/ui/admin_users_screen.dart';
import '../../features/admin/ui/admin_login_screen.dart';

// AI Features
import '../../features/ai/ui/ai_dashboard_screen.dart';
import '../../features/ai/ui/ai_chat_advisor_screen.dart';
import '../../features/ai/ui/environmental_insights_screen.dart';
import '../../features/ai/ui/grow_guidance_screen.dart';
import '../../features/ai/ui/plant_health_analysis_screen.dart';
import '../../features/ai/ui/yield_prediction_screen.dart';
import '../../features/ai/ui/agent_hub_screen.dart'; // Agent Hub Screen

// Legal
import '../../features/legal/ui/privacy_policy_screen.dart';
import '../../features/legal/ui/terms_screen.dart';

// Onboarding
import '../../features/onboarding/ui/onboarding_tutorial_overlay.dart';
import '../../features/onboarding/ui/genetics_onboarding_screen.dart';
import '../../features/onboarding/ui/environment_onboarding_screen.dart';
import '../../features/onboarding/ui/hardware_onboarding_screen.dart';

/// Helper function to check authentication and return appropriate screen
Widget _guardedScreen(Widget screen) {
  // DEVELOPMENT: Bypass authentication for testing
  // final authRepo = OAuthRepository();
  // if (!authRepo.isAuthenticated) {
  //   return const LoginScreen();
  // }
  return screen;
}

/// App Router Configuration with Authentication Guards
///
/// This router includes ALL available screens in the Flutter app.
/// Routes are organized by feature area.
///
/// Total Routes: 32 (up from 6)
final goRouterProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authProvider);
  final isAuthenticated = authState.when(
    data: (s) => s.isAuthenticated,
    loading: () => false,
    error: (_, __) => false,
  );
  final isAdmin = authState.when(
    data: (s) => s.user?.isAdmin ?? false,
    loading: () => false,
    error: (_, __) => false,
  );

  // Check if user is new (account created recently - within 5 minutes)
  // New users should go to genetic library (strains) first
  final isNewUser = false; // TEMPORARY BYPASS FOR VERIFICATION
  // final isNewUser = authState.when(
  //   data: (s) {
  //     if (s.user == null) return false;
  //     // Check if account was created very recently (within 5 minutes)
  //     // createdAt and updatedAt will be nearly identical for new accounts
  //     final difference = s.user!.updatedAt.difference(s.user!.createdAt);
  //     return difference.inMinutes < 5;
  //   },
  //   loading: () => false,
  //   error: (_, __) => false,
  // );

  return GoRouter(
    initialLocation: '/',
    debugLogDiagnostics: true,
    routes: [
      // ============================================
      // LANDING PAGE (Root)
      // ============================================
      GoRoute(
        path: '/',
        name: 'landing',
        builder: (context, state) => const LandingScreen(),
      ),

      // ============================================
      // AUTHENTICATION ROUTES
      // ============================================
      GoRoute(
        path: '/login',
        name: 'login',
        builder: (context, state) => const LoginScreen(),
      ),

      GoRoute(
        path: '/signup',
        name: 'signup',
        builder: (context, state) => const SignupScreen(),
      ),

      GoRoute(
        path: '/forgot-password',
        name: 'forgot-password',
        builder: (context, state) => const ForgotPasswordScreen(),
      ),

      GoRoute(
        path: '/change-password',
        name: 'change-password',
        builder: (context, state) =>
            _guardedScreen(const ChangePasswordScreen()),
      ),

      // OAuth Callback Route
      GoRoute(
        path: '/callback',
        builder: (context, state) {
          // Extract OAuth callback parameters from URL
          final code = state.uri.queryParameters['code'];
          final stateParam = state.uri.queryParameters['state'];
          final error = state.uri.queryParameters['error'];
          final errorDescription =
              state.uri.queryParameters['error_description'];

          return OAuthCallbackScreen(
            code: code,
            state: stateParam,
            error: error,
            errorDescription: errorDescription,
          );
        },
      ),

      // ============================================
      // ONBOARDING ROUTES
      // ============================================
      GoRoute(
        path: '/onboarding/welcome',
        name: 'onboarding-welcome',
        builder: (context, state) =>
            _guardedScreen(const OnboardingTutorialOverlay()),
      ),

      GoRoute(
        path: '/onboarding/genetics',
        name: 'onboarding-genetics',
        builder: (context, state) =>
            _guardedScreen(const GeneticsOnboardingScreen()),
      ),

      GoRoute(
        path: '/onboarding/environment',
        name: 'onboarding-environment',
        builder: (context, state) =>
            _guardedScreen(const EnvironmentOnboardingScreen()),
      ),

      GoRoute(
        path: '/onboarding/hardware',
        name: 'onboarding-hardware',
        builder: (context, state) =>
            _guardedScreen(const HardwareOnboardingScreen()),
      ),

      // ============================================
      // HOME / REDIRECT
      // ============================================

      // ============================================
      // DASHBOARD
      // ============================================
      GoRoute(
        path: '/dashboard',
        name: 'dashboard',
        builder: (context, state) => _guardedScreen(const DashboardScreen()),
      ),
      GoRoute(
        path: '/dashboard/breeder',
        name: 'breeder-dashboard',
        builder: (context, state) =>
            _guardedScreen(const BreederDashboardScreen()),
      ),

      // ============================================
      // PLANTS
      // ============================================
      GoRoute(
        path: '/plants',
        name: 'plants',
        builder: (context, state) => _guardedScreen(const PlantsListScreen()),
      ),

      GoRoute(
        path: '/plants/new',
        name: 'plant-form',
        builder: (context, state) => _guardedScreen(const PlantFormScreen()),
      ),

      GoRoute(
        path: '/plants/:id',
        name: 'plant-detail',
        builder: (context, state) {
          final plantId = int.parse(state.pathParameters['id'] ?? '1');
          return _guardedScreen(PlantDetailScreen(plantId: plantId));
        },
      ),

      // ============================================
      // SENSORS
      // ============================================
      GoRoute(
        path: '/sensors',
        name: 'sensors',
        builder: (context, state) => _guardedScreen(const SensorsScreen()),
      ),

      GoRoute(
        path: '/sensors/:id/config',
        name: 'sensor-config',
        builder: (context, state) {
          final sensorId = int.parse(state.pathParameters['id'] ?? '1');
          return _guardedScreen(SensorConfigScreen(sensorId: sensorId));
        },
      ),

      // ============================================
      // STRAINS / CULTIVARS
      // ============================================
      // ============================================
      // GENETICS (New Marketplace Library)
      // ============================================
      GoRoute(
        path: '/genetics',
        name: 'genetics',
        builder: (context, state) =>
            _guardedScreen(const GeneticsLibraryScreen()),
      ),

      // Legacy Strains List (Keeping for reference, or alias to new)
      GoRoute(
        path: '/strains',
        name: 'strains',
        builder: (context, state) => _guardedScreen(const StrainsListScreen()),
      ),

      GoRoute(
        path: '/strains/:id',
        name: 'strain-detail',
        builder: (context, state) {
          final strainId = state.pathParameters['id'] ?? '1';
          return _guardedScreen(GeneticsDetailScreen(strainId: strainId));
        },
      ),

      GoRoute(
        path: '/marketplace',
        name: 'marketplace',
        builder: (context, state) => _guardedScreen(const MarketplaceScreen()),
      ),

      // Alias for cultivars -> genetics (Updated)
      GoRoute(
        path: '/cultivars',
        name: 'cultivars',
        redirect: (context, state) => '/genetics',
      ),

      // ============================================
      // CLONES
      // ============================================
      GoRoute(
        path: '/clones',
        name: 'clones',
        builder: (context, state) =>
            _guardedScreen(const CloneManagementScreen()),
      ),

      // ============================================
      // NUTRIENTS
      // ============================================
      GoRoute(
        path: '/nutrients/calculator',
        name: 'nutrient-calculator',
        builder: (context, state) =>
            _guardedScreen(const NutrientCalculatorScreen()),
      ),
      GoRoute(
        path: '/nutrients/inventory',
        name: 'nutrient-inventory',
        builder: (context, state) =>
            _guardedScreen(const NutrientInventoryScreen()),
      ),

      // ============================================
      // SETTINGS
      // ============================================
      GoRoute(
        path: '/settings',
        name: 'settings',
        builder: (context, state) => _guardedScreen(const SettingsScreen()),
      ),

      // ============================================
      // CART & MARKETPLACE
      // ============================================
      GoRoute(
        path: '/cart',
        name: 'cart',
        builder: (context, state) => _guardedScreen(const CartScreen()),
      ),

      GoRoute(
        path: '/checkout',
        name: 'checkout',
        builder: (context, state) => _guardedScreen(const CheckoutScreen()),
      ),

      GoRoute(
        path: '/market/seedbank',
        name: 'seedbank',
        builder: (context, state) => _guardedScreen(const SeedBankScreen()),
      ),

      GoRoute(
        path: '/redemption',
        name: 'redemption',
        builder: (context, state) => _guardedScreen(const RedemptionScreen()),
      ),

      GoRoute(
        path: '/market/gear',
        name: 'gear',
        builder: (context, state) => _guardedScreen(const GearScreen()),
      ),

      GoRoute(
        path: '/market/extensions',
        name: 'extensions',
        builder: (context, state) => _guardedScreen(const ExtensionsScreen()),
      ),

      // ============================================
      // ADMIN
      // ============================================
      GoRoute(
        path: '/admin',
        name: 'admin',
        builder: (context, state) =>
            _guardedScreen(const AdminDashboardScreen()),
      ),

      GoRoute(
        path: '/admin/login',
        name: 'admin-login',
        builder: (context, state) => const AdminLoginScreen(),
      ),

      GoRoute(
        path: '/admin/users',
        name: 'admin-users',
        builder: (context, state) => _guardedScreen(const AdminUsersScreen()),
      ),

      // ============================================
      // AI FEATURES
      // ============================================
      GoRoute(
        path: '/ai',
        name: 'ai-dashboard',
        builder: (context, state) => _guardedScreen(const AIDashboardScreen()),
      ),

      GoRoute(
        path: '/ai/chat/:plantId',
        name: 'ai-chat',
        builder: (context, state) {
          final plantId = int.parse(state.pathParameters['plantId'] ?? '1');
          final extra = state.extra as Map<String, dynamic>?;
          final plantName = extra?['plantName'] ?? 'Unknown Plant';
          return _guardedScreen(
            AIChatAdvisorScreen(plantId: plantId, plantName: plantName),
          );
        },
      ),

      GoRoute(
        path: '/ai/insights',
        name: 'ai-insights',
        builder: (context, state) =>
            _guardedScreen(const EnvironmentalInsightsScreen()),
      ),

      GoRoute(
        path: '/ai/guidance',
        name: 'ai-guidance',
        builder: (context, state) => _guardedScreen(const GrowGuidanceScreen()),
      ),

      GoRoute(
        path: '/ai/health',
        name: 'ai-health',
        builder: (context, state) =>
            _guardedScreen(const PlantHealthAnalysisScreen()),
      ),

      GoRoute(
        path: '/ai/yield',
        name: 'ai-yield',
        builder: (context, state) =>
            _guardedScreen(const YieldPredictionScreen()),
      ),

      GoRoute(
        path: '/ai/hub',
        name: 'agent-hub',
        builder: (context, state) {
          if (!isAdmin) {
            return const Scaffold(
              body: Center(child: Text('Access denied: Admins only')),
            );
          }
          return _guardedScreen(const AgentHubScreen());
        },
      ),

      // ============================================
      // LEGAL
      // ============================================
      GoRoute(
        path: '/privacy',
        name: 'privacy',
        builder: (context, state) => const PrivacyPolicyScreen(),
      ),

      GoRoute(
        path: '/terms',
        name: 'terms',
        builder: (context, state) => const TermsScreen(),
      ),
    ],
    redirect: (context, state) {
      final isLanding = state.matchedLocation == '/';
      final isLoggingIn = state.matchedLocation == '/login';
      final isSigningUp = state.matchedLocation == '/signup';
      final isOnOnboarding = state.matchedLocation.startsWith('/onboarding');
      final isLegalPage =
          state.matchedLocation == '/privacy' ||
          state.matchedLocation == '/terms';

      debugPrint(
        'DEBUG: Router redirect: location=${state.matchedLocation} isAuthenticated=$isAuthenticated',
      );

      // Allow access to public routes without auth
      if (isLanding || isLoggingIn || isSigningUp || isLegalPage) {
        if (isAuthenticated && (isLoggingIn || isSigningUp)) {
          debugPrint(
            'DEBUG: Router: Logged in user on login/signup page -> /dashboard',
          );
          return '/dashboard';
        }
        debugPrint('DEBUG: Router: Allowing public route access');
        return null;
      }

      // Allow onboarding routes for authenticated users
      if (isOnOnboarding && isAuthenticated) {
        return null;
      }

      // Redirect to login if not authenticated
      if (!isAuthenticated) {
        return '/login';
      }

      // If new user and not on onboarding, redirect to onboarding
      if (isNewUser && !isOnOnboarding) {
        return '/onboarding/welcome';
      }

      return null;
    },
  );
});
