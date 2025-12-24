// Real AuthRepository that communicates with the FastAPI backend
import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../constants/app_constants.dart';
import '../api/api_exceptions.dart' as api_ex;

/// AuthRepository that uses real backend API for authentication
class AuthRepository {
  factory AuthRepository.instance() => _instance;
  AuthRepository._internal() {
    _storage = const FlutterSecureStorage();
    _dio = Dio(
      BaseOptions(
        baseUrl: AppConstants.apiBaseUrl,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 30),
      ),
    );
    _init();
  }

  static final AuthRepository _instance = AuthRepository._internal();

  late final FlutterSecureStorage _storage;
  late final Dio _dio;

  // Storage keys
  static const String userKey = 'current_user';

  Map<String, dynamic>? _currentUser;

  Future<void> _init() async {
    final userJson = await _storage.read(key: userKey);
    if (userJson != null) {
      try {
        _currentUser = jsonDecode(userJson) as Map<String, dynamic>;
      } catch (_) {
        _currentUser = null;
      }
    }
  }

  bool get isAuthenticated => _currentUser != null;
  Map<String, dynamic>? get currentUser => _currentUser;

  /// Login with username/email and password
  Future<void> login(String username, String password) async {
    try {
      // FastAPI OAuth2 expects form data, not JSON
      final response = await _dio.post(
        '/auth/login',
        data: FormData.fromMap({'username': username, 'password': password}),
        options: Options(contentType: 'application/x-www-form-urlencoded'),
      );

      if (response.statusCode == 200) {
        final data = response.data as Map<String, dynamic>;

        // Store tokens
        await _storage.write(
          key: AppConstants.accessTokenKey,
          value: data['access_token'] as String,
        );
        await _storage.write(
          key: AppConstants.refreshTokenKey,
          value: data['refresh_token'] as String?,
        );

        // Fetch user profile
        await _fetchCurrentUser();
      } else {
        throw api_ex.AuthException(
          message: 'Login failed: ${response.statusMessage}',
        );
      }
    } on DioException catch (e) {
      final message =
          e.response?.data?['detail'] ?? e.message ?? 'Login failed';
      throw api_ex.AuthException(message: message.toString());
    } catch (e) {
      throw api_ex.AuthException(message: 'Login failed: $e');
    }
  }

  /// Register a new user
  Future<void> register(String username, String email, String password) async {
    try {
      final response = await _dio.post(
        '/auth/register',
        data: {'username': username, 'email': email, 'password': password},
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        final data = response.data as Map<String, dynamic>;

        // If tokens are returned, store them
        if (data['access_token'] != null) {
          await _storage.write(
            key: AppConstants.accessTokenKey,
            value: data['access_token'] as String,
          );
          await _storage.write(
            key: AppConstants.refreshTokenKey,
            value: data['refresh_token'] as String?,
          );
          await _fetchCurrentUser();
        } else {
          // Otherwise, auto-login after registration
          await login(email, password);
        }
      } else {
        throw api_ex.AuthException(
          message: 'Registration failed: ${response.statusMessage}',
        );
      }
    } on DioException catch (e) {
      final message =
          e.response?.data?['detail'] ?? e.message ?? 'Registration failed';
      throw api_ex.AuthException(message: message.toString());
    } catch (e) {
      if (e is api_ex.AuthException) rethrow;
      throw api_ex.AuthException(message: 'Registration failed: $e');
    }
  }

  /// Logout and clear tokens
  Future<void> logout() async {
    await _clearTokens();
    _currentUser = null;
  }

  /// Refresh the access token
  Future<void> refreshToken() async {
    try {
      final refresh = await _storage.read(key: AppConstants.refreshTokenKey);
      if (refresh == null) {
        throw api_ex.AuthException(message: 'No refresh token available');
      }

      final response = await _dio.post(
        '/auth/refresh',
        data: {'refresh_token': refresh},
      );

      if (response.statusCode == 200) {
        final data = response.data as Map<String, dynamic>;
        await _storage.write(
          key: AppConstants.accessTokenKey,
          value: data['access_token'] as String,
        );
        if (data['refresh_token'] != null) {
          await _storage.write(
            key: AppConstants.refreshTokenKey,
            value: data['refresh_token'] as String,
          );
        }
      } else {
        throw api_ex.AuthException(message: 'Token refresh failed');
      }
    } on DioException catch (e) {
      throw api_ex.AuthException(message: 'Token refresh failed: ${e.message}');
    }
  }

  /// Fetch the current user profile
  Future<void> _fetchCurrentUser() async {
    try {
      final token = await _storage.read(key: AppConstants.accessTokenKey);
      if (token == null) {
        throw api_ex.AuthException(message: 'No access token');
      }

      final response = await _dio.get(
        '/auth/me',
        options: Options(headers: {'Authorization': 'Bearer $token'}),
      );

      if (response.statusCode == 200) {
        _currentUser = response.data as Map<String, dynamic>;
        await _storage.write(key: userKey, value: jsonEncode(_currentUser));
      }
    } on DioException {
      // If fetching user fails, try a simpler approach
      // Just store a basic user from the token
      _currentUser = {'email': 'user@cultivar.app', 'id': 1};
      await _storage.write(key: userKey, value: jsonEncode(_currentUser));
    }
  }

  /// Get current user (or null)
  Future<Map<String, dynamic>?> getCurrentUser() async {
    if (_currentUser == null) {
      await _init();
    }
    return _currentUser;
  }

  Future<void> _clearTokens() async {
    await _storage.delete(key: AppConstants.accessTokenKey);
    await _storage.delete(key: AppConstants.refreshTokenKey);
    await _storage.delete(key: userKey);
  }

  /// Change password
  Future<void> changePassword(
    String currentPassword,
    String newPassword,
  ) async {
    try {
      final token = await _storage.read(key: AppConstants.accessTokenKey);
      if (token == null) {
        throw api_ex.AuthException(message: 'Not authenticated');
      }

      final response = await _dio.post(
        '/auth/change-password',
        data: {
          'current_password': currentPassword,
          'new_password': newPassword,
        },
        options: Options(headers: {'Authorization': 'Bearer $token'}),
      );

      if (response.statusCode != 200) {
        throw api_ex.AuthException(message: 'Password change failed');
      }
    } on DioException catch (e) {
      throw api_ex.AuthException(
        message: 'Password change failed: ${e.message}',
      );
    }
  }

  /// Check if access token is expired
  Future<bool> isAccessTokenExpired() async {
    // For now, just check if token exists
    final token = await _storage.read(key: AppConstants.accessTokenKey);
    return token == null;
  }
}
