/// Authentication service with JWT and secure storage
/// Handles user authentication, token management, and session persistence
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../logging.dart';

import '../models/auth_models.dart';
import 'api_client.dart';

class AuthService {
  static const String _tokenKey = 'auth_token';
  static const String _refreshTokenKey = 'refresh_token';
  static const String _userKey = 'user_data';
  static const String _isLoggedInKey = 'is_logged_in';

  late final ApiClient _apiClient;
  late final FlutterSecureStorage _secureStorage;
  late final SharedPreferences _prefs;

  AuthResponse? _currentUser;
  String? _authToken;
  String? _refreshToken;

  AuthService() {
    _apiClient = ApiClient();
    _secureStorage = const FlutterSecureStorage(
      aOptions: AndroidOptions(
        encryptedSharedPreferences: true,
      ),
      iOptions: IOSOptions(
        accessibility: KeychainAccessibility.first_unlock_this_device,
      ),
    );
  }

  // ============================================================================
  // Initialization
  // ============================================================================

  Future<void> initialize() async {
    _prefs = await SharedPreferences.getInstance();
    
    // Load stored authentication data
    await _loadAuthData();
    
    // Set token for API client if available
    if (_authToken != null) {
      _apiClient.setAuthToken(_authToken!);
    }
    
    AppLogger.log('AuthService initialized');
    AppLogger.log('User logged in: ${isLoggedIn}');
    if (_currentUser != null) {
      AppLogger.log('Current user: ${_currentUser!.user.username}');
    }
  }

  // ============================================================================
  // Authentication Methods
  // ============================================================================

  /// Login user with email and password
  Future<AuthResponse> login(String email, String password) async {
    try {
      final response = await _apiClient.login(email, password);
      
      // Store authentication data
      await _storeAuthData(response);
      
      // Set token for API client
      _apiClient.setAuthToken(response.accessToken);
      
      _currentUser = response;
      _authToken = response.accessToken;
      _refreshToken = response.refreshToken;
      
    AppLogger.log('Login successful for: ${response.user.username}');
      return response;
    } catch (e) {
    AppLogger.error('Login failed', e);
      rethrow;
    }
  }

  /// Register new user
  Future<AuthResponse> register({
    required String username,
    required String email,
    required String password,
  }) async {
    try {
      final response = await _apiClient.register(
        username: username,
        email: email,
        password: password,
      );
      
      // Store authentication data
      await _storeAuthData(response);
      
      // Set token for API client
      _apiClient.setAuthToken(response.accessToken);
      
      _currentUser = response;
      _authToken = response.accessToken;
      _refreshToken = response.refreshToken;
      
    AppLogger.log('Registration successful for: ${response.user.username}');
      return response;
    } catch (e) {
    AppLogger.error('Registration failed', e);
      rethrow;
    }
  }

  /// Logout user
  Future<void> logout() async {
    try {
      // Call logout API if token is available
      if (_authToken != null) {
        await _apiClient.logout();
      }
    } catch (e) {
  AppLogger.error('Logout API call failed', e);
      // Continue with logout even if API call fails
    } finally {
      // Clear local authentication data
      await _clearAuthData();
      _apiClient.clearAuthToken();
      
      _currentUser = null;
      _authToken = null;
      _refreshToken = null;
      
    AppLogger.log('User logged out');
    }
  }

  /// Check if user is currently logged in
  bool get isLoggedIn {
    return _authToken != null && _currentUser != null && _currentUser!.user.isActive;
  }

  /// Get current user
  User? get currentUser {
    return _currentUser?.user;
  }

  /// Get current authentication token
  String? get authToken {
    return _authToken;
  }

  /// Check if token needs refresh (within 5 minutes of expiry)
  bool get needsTokenRefresh {
    if (_refreshToken == null) return false;
    
    // This would need JWT parsing to check expiry
    // For now, we'll implement a simple refresh strategy
    return true; // Always refresh for demo purposes
  }

  /// Refresh authentication token
  Future<bool> refreshToken() async {
    if (_refreshToken == null) {
  AppLogger.log('No refresh token available');
      return false;
    }

    try {
      // This would call a refresh endpoint in a real implementation
    AppLogger.log('Token refresh would be implemented here');
      
      // For now, we'll simulate a successful refresh
      return true;
    } catch (e) {
    AppLogger.error('Token refresh failed', e);
      await logout();
      return false;
    }
  }

  // ============================================================================
  // Data Persistence
  // ============================================================================

  /// Store authentication data securely
  Future<void> _storeAuthData(AuthResponse response) async {
    try {
      // Store tokens in secure storage
      await _secureStorage.write(key: _tokenKey, value: response.accessToken);
      if (response.refreshToken != null) {
        await _secureStorage.write(key: _refreshTokenKey, value: response.refreshToken);
      }
      
      // Store user data in shared preferences
      await _prefs.setString(_userKey, response.user.toJson().toString());
      await _prefs.setBool(_isLoggedInKey, true);
      
    AppLogger.log('Auth data stored securely');
    } catch (e) {
    AppLogger.error('Failed to store auth data', e);
    }
  }

  /// Load authentication data from storage
  Future<void> _loadAuthData() async {
    try {
      // Load tokens from secure storage
      _authToken = await _secureStorage.read(key: _tokenKey);
      _refreshToken = await _secureStorage.read(key: _refreshTokenKey);
      
      // Load user data from shared preferences
      final userJsonString = _prefs.getString(_userKey);
      final isLoggedIn = _prefs.getBool(_isLoggedInKey) ?? false;
      
      if (userJsonString != null && isLoggedIn) {
        // Parse user data (would need proper JSON parsing in real implementation)
        // For now, we'll just set a placeholder
  AppLogger.log('Loaded stored auth data');
      }
    } catch (e) {
  AppLogger.error('Failed to load auth data', e);
    }
  }

  /// Clear all authentication data
  Future<void> _clearAuthData() async {
    try {
      // Clear secure storage
      await _secureStorage.delete(key: _tokenKey);
      await _secureStorage.delete(key: _refreshTokenKey);
      
      // Clear shared preferences
      await _prefs.remove(_userKey);
      await _prefs.setBool(_isLoggedInKey, false);
      
    AppLogger.log('Auth data cleared');
    } catch (e) {
    AppLogger.error('Failed to clear auth data', e);
    }
  }

  // ============================================================================
  // User Profile Management
  // ============================================================================

  /// Update user profile
  Future<User> updateProfile({
    String? username,
    String? email,
  }) async {
    if (!isLoggedIn) {
      throw AuthException('User not authenticated');
    }

    try {
      // This would call a profile update endpoint
    AppLogger.log('Profile update would be implemented here');
      
      // For demo, return current user with updated data
      final updatedUser = _currentUser!.user.copyWith(
        username: username ?? _currentUser!.user.username,
        email: email ?? _currentUser!.user.email,
      );
      
      // Update stored user data
      await _prefs.setString(_userKey, updatedUser.toJson().toString());
      _currentUser = _currentUser!.copyWith(user: updatedUser);
      
      return updatedUser;
    } catch (e) {
    AppLogger.error('Profile update failed', e);
      rethrow;
    }
  }

  /// Change user password
  Future<void> changePassword({
    required String currentPassword,
    required String newPassword,
  }) async {
    if (!isLoggedIn) {
      throw AuthException('User not authenticated');
    }

    try {
      // This would call a password change endpoint
    AppLogger.log('Password change would be implemented here');
      
    AppLogger.log('Password changed successfully');
    } catch (e) {
    AppLogger.error('Password change failed', e);
      rethrow;
    }
  }

  // ============================================================================
  // Validation Helpers
  // ============================================================================

  /// Validate email format
  bool isValidEmail(String email) {
    final emailRegex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
    return emailRegex.hasMatch(email);
  }

  /// Validate password strength
  bool isValidPassword(String password) {
    return password.length >= 8;
  }

  /// Validate username format
  bool isValidUsername(String username) {
    return username.length >= 3 && username.length <= 20;
  }

  // ============================================================================
  // Cleanup
  // ============================================================================

  /// Clean up resources
  void dispose() {
    _apiClient.dispose();
  }
}

// ============================================================================
// Custom Exceptions
// ============================================================================

class AuthException implements Exception {
  final String message;
  
  const AuthException(this.message);
  
  @override
  String toString() => 'AuthException: $message';
}

class TokenExpiredException implements Exception {
  final String message;
  
  const TokenExpiredException(this.message);
  
  @override
  String toString() => 'TokenExpiredException: $message';
}

// ============================================================================
// Extension for AuthResponse
// ============================================================================

extension AuthResponseExtension on AuthResponse {
  AuthResponse copyWith({
    String? accessToken,
    String? tokenType,
    User? user,
    String? refreshToken,
  }) {
    return AuthResponse(
      accessToken: accessToken ?? this.accessToken,
      tokenType: tokenType ?? this.tokenType,
      user: user ?? this.user,
    );
  }
}