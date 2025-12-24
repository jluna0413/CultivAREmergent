import 'dart:async';
import 'package:flutter/foundation.dart';

import 'package:cultivar_app/core/auth/oauth_repository_base.dart'; // Import the interface
import 'package:cultivar_app/core/auth/oauth_repository.dart'
    as oauth_provider; // Import the provider function
import 'package:cultivar_app/core/models/auth_models.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

// Temp comment to force re-analysis

/// Small compatibility view matching legacy authProvider.data shape
class AuthDataView {
  const AuthDataView({this.token, this.user});
  final String? token;
  final User? user;
}

/// AuthState class with immutable state including accessToken.
class AuthState {
  const AuthState({
    this.isAuthenticated = false,
    this.user,
    this.accessToken,
    this.isLoading = false,
    this.error,
  });

  final bool isAuthenticated;
  final User? user;
  final String? accessToken;
  final bool isLoading;
  final String? error;

  AuthDataView? get data {
    if (accessToken == null && user == null) return null;
    return AuthDataView(token: accessToken, user: user);
  }

  AuthState copyWith({
    bool? isAuthenticated,
    User? user,
    String? accessToken,
    bool? isLoading,
    String? error,
  }) => AuthState(
    isAuthenticated: isAuthenticated ?? this.isAuthenticated,
    user: user ?? this.user,
    accessToken: accessToken ?? this.accessToken,
    isLoading: isLoading ?? this.isLoading,
    error: error ?? this.error,
  );
}

/// Authentication notifier with proper state management
class AuthNotifier extends AsyncNotifier<AuthState> {
  late final OAuthRepository _authRepository;

  @override
  Future<AuthState> build() async {
    debugPrint('DEBUG: AuthNotifier build() started');
    _authRepository = oauth_provider.getOAuthRepository();
    final state = await _checkAuth();
    debugPrint(
      'DEBUG: AuthNotifier build() finished - authenticated: ${state.isAuthenticated}',
    );
    return state;
  }

  /// Stream for GoRouterRefreshStream
  Stream<bool> get authStateChanges async* {
    while (true) {
      await Future.delayed(const Duration(milliseconds: 100));
      yield state.value?.isAuthenticated ?? false;
    }
  }

  Future<AuthState> _checkAuth() async {
    // BYPASS LOGIN FOR TESTING (Enabled for debugging white screen)
    debugPrint('DEBUG: _checkAuth bypassing to mock user');
    return AuthState(
      isAuthenticated: true,
      user: User(
        id: 3, // Matches verify_user in local DB
        email: 'verify_breeder@test.com',
        username: 'verify_user',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
        isAdmin: true,
      ),
      accessToken: 'mock_admin_token',
    );
  }

  Future<AuthState> _checkAuthActual() async {
    try {
      final userMap = await _authRepository.getCurrentUser();
      if (userMap != null) {
        final accessToken = await _authRepository.getAccessToken();
        if (accessToken != null) {
          return AuthState(
            isAuthenticated: true,
            user: User(
              id: 0, // Placeholder, backend will handle user mapping
              email: userMap['email'] ?? '',
              username:
                  userMap['preferred_username'] ??
                  userMap['email']?.split('@')[0] ??
                  'User',
              avatar: null,
              createdAt: DateTime.now(),
              updatedAt: DateTime.now(),
            ),
            accessToken: accessToken,
          );
        }
      }
    } catch (e) {
      print('Auth check error: $e');
    }
    return const AuthState(isAuthenticated: false);
  }

  void login() {
    state = const AsyncValue.loading();
    // OAuth login redirects the browser - just call it
    _authRepository.login();
    // Browser will navigate away so no need to handle result
  }

  /// Database login for development/testing
  Future<void> loginWithDatabase(String username, String password) async {
    state = const AsyncValue.loading();

    try {
      // Use devLogin from repository directly

      // Let's rely on the repository adding a method for this, or use a direct http call for now since this is dev-only.
      // Actually, let's just make a direct Dio call since we are in a notifier.

      // Better: Update OAuthRepository to support this. But for speed/least-disturbance:

      final response = await _authRepository.devLogin(username, password);

      if (response != null && response['access_token'] != null) {
        final accessToken = response['access_token'];
        final userData = response['user'];

        final user = User(
          id: userData['id'] is int
              ? userData['id']
              : int.tryParse(userData['id'].toString()) ?? 0,
          email: userData['email'] ?? '',
          username: userData['username'] ?? '',
          avatar: null,
          createdAt: DateTime.now(),
          updatedAt: DateTime.now(),
        );

        state = AsyncValue.data(
          AuthState(
            isAuthenticated: true,
            user: user,
            accessToken: accessToken,
          ),
        );
      } else {
        state = const AsyncValue.data(
          AuthState(
            isAuthenticated: false,
            error: 'Invalid response from server',
          ),
        );
      }
    } catch (e) {
      state = AsyncValue.data(
        AuthState(isAuthenticated: false, error: 'Login failed: $e'),
      );
    }
  }

  Future<void> logout() async {
    try {
      await _authRepository.logout();
    } finally {
      state = const AsyncValue.data(AuthState(isAuthenticated: false));
    }
  }

  // Signup is handled via Login page in Keycloak (Register link)
  void signup({
    required String email,
    required String password,
    required String name,
  }) {
    login();
  }

  // Alias for backward compatibility
  void register({
    required String email,
    required String password,
    required String name,
  }) {
    signup(email: email, password: password, name: name);
  }

  Future<bool> refreshTokens() async {
    // Handled automatically by getAccessToken() in repository
    return true;
  }

  void clearError() {
    if (state.value?.error != null) {
      state = AsyncValue.data(state.value!.copyWith(error: null));
    }
  }

  Future<bool> requestPasswordReset(String email) async {
    // Keycloak handles this.
    return true;
  }
}

/// Providers
final authProvider = AsyncNotifierProvider<AuthNotifier, AuthState>(
  AuthNotifier.new,
);

/// Backwards-compatible alias used in older callsites
final authNotifierProvider = authProvider;

final isAuthenticatedProvider = Provider<bool>((ref) {
  final authState = ref.watch(authProvider);
  return authState.when(
    data: (data) => data.isAuthenticated,
    loading: () => false,
    error: (_, __) => false,
  );
});

final currentUserProvider = Provider<User?>((ref) {
  final authState = ref.watch(authProvider);
  return authState.when(
    data: (data) => data.user,
    loading: () => null,
    error: (_, __) => null,
  );
});

final authLoadingProvider = Provider<bool>((ref) {
  final authState = ref.watch(authProvider);
  return authState.isLoading;
});

final authErrorProvider = Provider<String?>((ref) {
  final authState = ref.watch(authProvider);
  return authState.when(
    data: (data) => data.error,
    loading: () => null,
    error: (error, _) => error.toString(),
  );
});

/// Stream provider for GoRouterRefreshStream
final authStateStreamProvider = StreamProvider<bool>((ref) {
  final authNotifier = ref.read(authProvider.notifier);
  return authNotifier.authStateChanges;
});
