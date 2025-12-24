import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/auth_models.dart';
import '../services/api_client.dart';

/// Authentication states
enum AuthState { initial, loading, authenticated, unauthenticated, error }

/// Simple authentication state class
class AuthProviderState {
  const AuthProviderState({required this.state, this.data, this.error});

  final AuthState state;
  final AuthData? data;
  final String? error;

  bool get isLoading => state == AuthState.loading;
  bool get isAuthenticated => state == AuthState.authenticated;
  bool get isUnauthenticated => state == AuthState.unauthenticated;
  bool get hasError => state == AuthState.error;

  AuthProviderState copyWith({
    AuthState? state,
    AuthData? data,
    String? error,
  }) {
    return AuthProviderState(
      state: state ?? this.state,
      data: data ?? this.data,
      error: error ?? this.error,
    );
  }
}

/// Authentication data model for provider
class AuthData {
  const AuthData({
    required this.user,
    required this.token,
    this.refreshToken,
    this.expiresAt,
  });

  final User user;
  final String token;
  final String? refreshToken;
  final DateTime? expiresAt;

  AuthData copyWith({
    User? user,
    String? token,
    String? refreshToken,
    DateTime? expiresAt,
  }) {
    return AuthData(
      user: user ?? this.user,
      token: token ?? this.token,
      refreshToken: refreshToken ?? this.refreshToken,
      expiresAt: expiresAt ?? this.expiresAt,
    );
  }
}

/// Default unauthenticated state
const AuthProviderState defaultAuthState = AuthProviderState(
  state: AuthState.unauthenticated,
);

/// Mock user for development/testing
final User mockUser = User(
  id: 1,
  email: 'admin@cultivar.app',
  username: 'admin',
  avatar: null,
  createdAt: DateTime.now().subtract(const Duration(days: 30)),
  updatedAt: DateTime.now(),
  isActive: true,
);

/// Mock authenticated state for development
final AuthData mockAuthData = AuthData(
  user: mockUser,
  token: 'mock-jwt-token-for-development',
  refreshToken: 'mock-refresh-token',
  expiresAt: DateTime.now().add(const Duration(hours: 24)),
);

/// Main authentication provider using simple Provider pattern
final authProvider = Provider<AuthProviderState>((ref) {
  return defaultAuthState;
});

/// Convenience providers for specific auth data
final currentUserProvider = Provider<User?>((ref) {
  final authState = ref.watch(authProvider);
  return authState.data?.user;
});

final isAuthenticatedProvider = Provider<bool>((ref) {
  final authState = ref.watch(authProvider);
  return authState.isAuthenticated;
});

final isLoadingProvider = Provider<bool>((ref) {
  final authState = ref.watch(authProvider);
  return authState.isLoading;
});

final authErrorProvider = Provider<String?>((ref) {
  final authState = ref.watch(authProvider);
  return authState.error;
});

final authTokenProvider = Provider<String?>((ref) {
  final authState = ref.watch(authProvider);
  return authState.data?.token;
});

/// API Client provider
final apiClientProvider = Provider<ApiClient>((ref) {
  final token = ref.watch(authTokenProvider);
  final client = ApiClient();
  if (token != null) {
    client.setAuthToken(token);
  }
  return client;
});

// Note: In a real implementation, you would add state management
// and methods like login(), logout(), register(), etc.
// For now, using static data for immediate compilation success.
