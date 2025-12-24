// Mock AuthRepository for development and testing
// Accepts any credentials for demonstration purposes

import 'dart:async';
import 'dart:convert';

import '../../core/constants/app_constants.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:jwt_decoder/jwt_decoder.dart';

import '../api/api_exceptions.dart' as api_ex;

/// Mock AuthRepository that accepts any credentials for development
class MockAuthRepository {
  factory MockAuthRepository.instance() => _instance;
  MockAuthRepository._internal() {
    _storage = const FlutterSecureStorage();
    _init();
  }

  static final MockAuthRepository _instance = MockAuthRepository._internal();

  late final FlutterSecureStorage _storage;

  // Storage keys
  static const String tokenExpiryKey = 'access_token_expiry';
  static const String userKey = 'current_user';

  // Mock user database
  static final Map<String, Map<String, dynamic>> _mockUsers = {
    'admin@cultivar.app': {
      'id': 1,
      'username': 'admin',
      'email': 'admin@cultivar.app',
      'role': 'admin',
      'full_name': 'Admin User',
    },
    'user@cultivar.app': {
      'id': 2,
      'username': 'user',
      'email': 'user@cultivar.app',
      'role': 'user',
      'full_name': 'Regular User',
    },
  };

  final StreamController<Map<String, dynamic>?> _userController =
      StreamController<Map<String, dynamic>?>.broadcast();
  Stream<Map<String, dynamic>?> get userStream => _userController.stream;

  Map<String, dynamic>? _currentUser;

  Future<void> _init() async {
    final userJson = await _storage.read(key: userKey);
    if (userJson != null) {
      try {
        _currentUser = jsonDecode(userJson) as Map<String, dynamic>;
        _userController.add(_currentUser);
      } catch (_) {
        _currentUser = null;
        _userController.add(null);
      }
    } else {
      _userController.add(null);
    }
  }

  bool get isAuthenticated {
    return _currentUser != null;
  }

  Map<String, dynamic>? get currentUser => _currentUser;

  Future<void> login(String username, String password) async {
    try {
      // Mock authentication - accept any credentials but provide different users based on email
      await Future.delayed(
        const Duration(milliseconds: 500),
      ); // Simulate network delay

      // For demo purposes, create a user based on the email provided
      final email = username.contains('@')
          ? username
          : '$username@cultivar.app';
      final isAdmin =
          email.toLowerCase() == 'admin@cultivar.app' ||
          username.toLowerCase() == 'admin' ||
          password.toLowerCase() == 'admin123';

      final user = isAdmin
          ? _mockUsers['admin@cultivar.app']!
          : _mockUsers['user@cultivar.app']!;

      // Generate mock JWT tokens
      final accessToken = _generateMockJwt(user, 'access');
      final refreshToken = _generateMockJwt(user, 'refresh');

      // Store tokens
      await _storage.write(
        key: AppConstants.accessTokenKey,
        value: accessToken,
      );
      await _storage.write(
        key: AppConstants.refreshTokenKey,
        value: refreshToken,
      );

      // Set current user
      _currentUser = user;
      await _storage.write(key: userKey, value: jsonEncode(user));
      _userController.add(_currentUser);
    } catch (e) {
      throw api_ex.AuthException(
        message: 'Login failed: ${e.toString()}',
        details: e,
      );
    }
  }

  Future<void> logout() async {
    await _clearTokens();
    _currentUser = null;
    _userController.add(null);
  }

  Future<void> register(String username, String email, String password) async {
    try {
      await Future.delayed(
        const Duration(milliseconds: 500),
      ); // Simulate network delay

      // Mock registration - create new user
      final user = {
        'id': DateTime.now().millisecondsSinceEpoch,
        'username': username,
        'email': email,
        'role': 'user',
        'full_name': username,
      };

      // Mock auto-login after registration
      final accessToken = _generateMockJwt(user, 'access');
      final refreshToken = _generateMockJwt(user, 'refresh');

      await _storage.write(
        key: AppConstants.accessTokenKey,
        value: accessToken,
      );
      await _storage.write(
        key: AppConstants.refreshTokenKey,
        value: refreshToken,
      );

      _currentUser = user;
      await _storage.write(key: userKey, value: jsonEncode(user));
      _userController.add(_currentUser);
    } catch (e) {
      throw api_ex.AuthException(
        message: 'Registration failed: ${e.toString()}',
        details: e,
      );
    }
  }

  Future<void> changePassword(
    String currentPassword,
    String newPassword,
  ) async {
    try {
      await Future.delayed(const Duration(milliseconds: 500));
      // Mock password change - always succeeds
    } catch (e) {
      throw api_ex.AuthException(
        message: 'Change password failed: ${e.toString()}',
        details: e,
      );
    }
  }

  Future<Map<String, dynamic>?> getCurrentUser() async {
    try {
      if (_currentUser == null) {
        throw api_ex.AuthException(message: 'No authenticated user');
      }
      return _currentUser;
    } catch (e) {
      throw api_ex.AuthException(
        message: 'Get current user failed: ${e.toString()}',
        details: e,
      );
    }
  }

  Future<void> refreshToken() async {
    try {
      final refresh = await _storage.read(key: AppConstants.refreshTokenKey);
      if (refresh == null || JwtDecoder.isExpired(refresh)) {
        throw api_ex.AuthException(message: 'No valid refresh token available');
      }

      // Mock token refresh
      final access = _generateMockJwt(_currentUser!, 'access');
      await _storage.write(key: AppConstants.accessTokenKey, value: access);
    } catch (e) {
      throw api_ex.AuthException(
        message: 'Token refresh failed: ${e.toString()}',
      );
    }
  }

  Future<bool> isAccessTokenExpired() async {
    final token = await _storage.read(key: AppConstants.accessTokenKey);
    if (token == null) return true;
    try {
      return JwtDecoder.isExpired(token);
    } catch (_) {
      return true;
    }
  }

  Future<void> _clearTokens() async {
    await _storage.delete(key: AppConstants.accessTokenKey);
    await _storage.delete(key: AppConstants.refreshTokenKey);
    await _storage.delete(key: tokenExpiryKey);
    await _storage.delete(key: userKey);
  }

  String _generateMockJwt(Map<String, dynamic> user, String type) {
    // Generate a mock JWT-like token for demonstration
    final now = DateTime.now();
    final expiry = type == 'access'
        ? now.add(const Duration(hours: 1))
        : now.add(const Duration(days: 7));

    final payload = {
      'sub': user['id'],
      'email': user['email'],
      'type': type,
      'iat': now.millisecondsSinceEpoch ~/ 1000,
      'exp': expiry.millisecondsSinceEpoch ~/ 1000,
    };

    // Return a base64 encoded mock token
    return 'mock.${base64Encode(utf8.encode(jsonEncode(payload)))}.signature';
  }

  Future<void> dispose() async {
    await _userController.close();
  }
}
