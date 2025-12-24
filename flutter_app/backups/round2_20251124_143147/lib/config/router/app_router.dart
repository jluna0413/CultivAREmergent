// lib/config/router/app_router.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:cultivar_app/core/providers/auth_provider.dart';
// Placeholder imports - replace with actual screen imports

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(child: Text('Login Screen - Coming Soon')),
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(child: Text('Home Screen - Coming Soon')),
    );
  }
}

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(child: Text('Dashboard Screen - Coming Soon')),
    );
  }
}

class PlantsScreen extends StatelessWidget {
  const PlantsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(child: Text('Plants Screen - Coming Soon')),
    );
  }
}

final goRouterProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authProvider);
  final isAuthenticated = authState.state == AuthState.authenticated;
  final isLoading = authState.state == AuthState.loading;

  return GoRouter(
    initialLocation: '/',
    routes: [
      GoRoute(path: '/', builder: (context, state) => const HomeScreen()),
      GoRoute(path: '/login', builder: (context, state) => const LoginScreen()),
      GoRoute(
        path: '/dashboard',
        builder: (context, state) => const DashboardScreen(),
      ),
      GoRoute(
        path: '/plants',
        builder: (context, state) => const PlantsScreen(),
      ),
      // Add other authenticated routes here
    ],
    redirect: (context, state) {
      final isLoggingIn = state.matchedLocation == '/login';

      // Skip redirect if still loading
      if (isLoading) {
        return null;
      }

      // If not authenticated and not trying to log in, redirect to login
      if (!isAuthenticated && !isLoggingIn) {
        return '/login';
      }
      // If authenticated and trying to log in, redirect to home (or dashboard)
      if (isAuthenticated && isLoggingIn) {
        return '/dashboard'; // Or any other authenticated default route
      }

      // No redirect
      return null;
    },
    // Remove refreshListenable for now to fix compilation errors
    // GoRouter will automatically refresh when providers change
  );
});
