/// API Client for CultivAR backend integration with versioned endpoints
/// Handles HTTP requests, authentication, and error handling with centralized token management
import 'package:dio/dio.dart';
import 'package:pretty_dio_logger/pretty_dio_logger.dart';

import '../logging.dart';
import '../config/app_config.dart';
import '../services/storage_service.dart';
import '../models/auth_models.dart';
import '../models/plant_models.dart';
import '../models/sensor_models.dart';
import '../models/cultivar_models.dart';
import '../models/dashboard_stats.dart';
import '../models/cart_models.dart';

/// Custom exception for API errors with additional context
class ApiException implements Exception {
  final String message;
  final int? statusCode;
  final String? code;

  const ApiException(
    this.message, {
    this.statusCode,
    this.code,
  });

  /// Create ApiException from Dio error
  static ApiException fromDioError(DioException error) {
    final message = error.response?.data['message'] ??
        error.response?.data['detail'] ??
        error.response?.data['error'] ??
        error.message ??
        'Unknown error';

    final statusCode = error.response?.statusCode;
    final code = error.response?.data['code'];

    return ApiException(message, statusCode: statusCode, code: code);
  }

  @override
  String toString() =>
      'ApiException${statusCode != null ? ' ($statusCode)' : ''}: $message';
}

/// API Logger for consistent logging
class ApiLogger {
  static void logRequest(String method, String url) {
    AppLogger.debug('API Request: $method $url');
  }

  static void logError(String message) {
    AppLogger.error('API Error: $message');
  }

  static void logSuccess(String message) {
    AppLogger.info('API Success: $message');
  }
}

/// Main API Client class with centralized token handling
class ApiClient {
  static const String _baseUrl = AppConfig.apiBaseUrl;

  late final Dio _dio;

  ApiClient() {
    _dio = Dio();
    _setupDio();
  }

  /// Configure Dio instance with interceptors and settings
  void _setupDio() {
    _dio.options.baseUrl = _baseUrl;
    _dio.options.connectTimeout = const Duration(seconds: 15);
    _dio.options.receiveTimeout = const Duration(seconds: 15);
    _dio.options.sendTimeout = const Duration(seconds: 15);
    _dio.options.headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };

    // Add logging interceptor for development
    _dio.interceptors.add(
      PrettyDioLogger(
        requestHeader: AppConfig.isDevelopment,
        requestBody: AppConfig.isDevelopment,
        responseBody: AppConfig.isDevelopment,
        responseHeader: false,
        error: true,
        compact: true,
      ),
    );

    // Add authentication and error interceptors
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: _onRequest,
      onError: _onError,
    ));
  }

  /// Handle requests with authentication token
  Future<void> _onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    ApiLogger.logRequest(options.method, options.uri.toString());

    // Add authentication token
    final token = await StorageService.getAuthToken();
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }

    handler.next(options);
  }

  /// Handle errors including automatic token refresh
  Future<void> _onError(
    DioException error,
    ErrorInterceptorHandler handler,
  ) async {
    ApiLogger.logError('${error.type} - ${error.message}');

    if (error.response?.statusCode == 401) {
      final refreshed = await _tryRefreshToken();
      if (refreshed) {
        // Retry original request with new token
        final token = await StorageService.getAuthToken();
        final originalRequest = error.requestOptions;
        originalRequest.headers['Authorization'] = 'Bearer $token';

        try {
          final response = await _dio.fetch(originalRequest);
          handler.resolve(response);
          return;
        } catch (e) {
          // Retry failed, proceed with original error
        }
      }
    }

    handler.next(error);
  }

  /// Try to refresh authentication token
  Future<bool> _tryRefreshToken() async {
    final refreshToken = await StorageService.getRefreshToken();
    if (refreshToken == null) return false;

    try {
      final response = await _dio.post(
        '$_baseUrl/api/v1/auth/refresh',
        data: {'refresh_token': refreshToken},
      );

      final newTokens = response.data['data'];
      await StorageService.saveAuthToken(newTokens['access_token']);
      await StorageService.saveRefreshToken(newTokens['refresh_token']);

      ApiLogger.logSuccess('Token refreshed successfully');
      return true;
    } catch (e) {
      await StorageService.clearAuthToken();
      await StorageService.clearRefreshToken();
      ApiLogger.logError('Token refresh failed: $e');
      return false;
    }
  }

  // ==================== AUTHENTICATION ENDPOINTS ====================

  /// Login user with email and password
  Future<AuthResponse> login(String email, String password) async {
    try {
      final response = await _dio.post(
        '$_baseUrl/api/v1/auth/login',
        data: {
          'email': email,
          'password': password,
        },
      );

      final authData = response.data['data'];
      await StorageService.saveAuthToken(authData['access_token']);
      if (authData['refresh_token'] != null) {
        await StorageService.saveRefreshToken(authData['refresh_token']);
      }

      return AuthResponse.fromJson(authData);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  /// Register new user
  Future<AuthResponse> register({
    required String username,
    required String email,
    required String password,
  }) async {
    try {
      final response = await _dio.post(
        '$_baseUrl/api/v1/auth/register',
        data: {
          'username': username,
          'email': email,
          'password': password,
        },
      );

      final authData = response.data['data'];
      await StorageService.saveAuthToken(authData['access_token']);
      if (authData['refresh_token'] != null) {
        await StorageService.saveRefreshToken(authData['refresh_token']);
      }

      return AuthResponse.fromJson(authData);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  /// Logout current user
  Future<void> logout() async {
    try {
      await _dio.post('$_baseUrl/api/v1/auth/logout');
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    } finally {
      await StorageService.clearAuthToken();
      await StorageService.clearRefreshToken();
    }
  }

  /// Refresh authentication token
  Future<AuthResponse> refreshToken(String refreshToken) async {
    try {
      final response = await _dio.post(
        '$_baseUrl/api/v1/auth/refresh',
        data: {'refresh_token': refreshToken},
      );

      final authData = response.data['data'];
      await StorageService.saveAuthToken(authData['access_token']);
      await StorageService.saveRefreshToken(authData['refresh_token']);

      return AuthResponse.fromJson(authData);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  // ==================== PLANTS ENDPOINTS ====================

  /// Get paginated list of plants
  Future<List<Plant>> getPlants({
    int page = 1,
    int limit = 20,
  }) async {
    try {
      final response = await _dio.get(
        '$_baseUrl/api/v1/plants',
        queryParameters: {'page': page, 'limit': limit},
      );

      final List<dynamic> plantsJson = response.data['data']['items'];
      return plantsJson.map((json) => Plant.fromJson(json)).toList();
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  /// Get single plant by ID
  Future<Plant> getPlant(int id) async {
    try {
      final response = await _dio.get('$_baseUrl/api/v1/plants/$id');
      return Plant.fromJson(response.data['data']);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  /// Create new plant
  Future<Plant> createPlant(PlantCreate request) async {
    try {
      final response = await _dio.post(
        '$_baseUrl/api/v1/plants',
        data: request.toJson(),
      );
      return Plant.fromJson(response.data['data']);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  /// Update existing plant
  Future<Plant> updatePlant(int id, PlantUpdate request) async {
    try {
      final response = await _dio.put(
        '$_baseUrl/api/v1/plants/$id',
        data: request.toJson(),
      );
      return Plant.fromJson(response.data['data']);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  /// Delete plant
  Future<void> deletePlant(int id) async {
    try {
      await _dio.delete('$_baseUrl/api/v1/plants/$id');
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  // ==================== SENSORS ENDPOINTS ====================

  /// Get list of sensors
  Future<List<Sensor>> getSensors() async {
    try {
      final response = await _dio.get('$_baseUrl/api/v1/sensors');
      final List<dynamic> sensorsJson = response.data['data']['items'];
      return sensorsJson.map((json) => Sensor.fromJson(json)).toList();
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  /// Get single sensor by ID
  Future<Sensor> getSensor(int id) async {
    try {
      final response = await _dio.get('$_baseUrl/api/v1/sensors/$id');
      return Sensor.fromJson(response.data['data']);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  /// Create new sensor
  Future<Sensor> createSensor(Map<String, dynamic> sensorData) async {
    try {
      final response = await _dio.post(
        '$_baseUrl/api/v1/sensors',
        data: sensorData,
      );
      return Sensor.fromJson(response.data['data']);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  /// Update sensor
  Future<Sensor> updateSensor(int id, Map<String, dynamic> sensorData) async {
    try {
      final response = await _dio.put(
        '$_baseUrl/api/v1/sensors/$id',
        data: sensorData,
      );
      return Sensor.fromJson(response.data['data']);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  /// Delete sensor
  Future<void> deleteSensor(int id) async {
    try {
      await _dio.delete('$_baseUrl/api/v1/sensors/$id');
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  // ==================== DASHBOARD ENDPOINTS ====================

  /// Get dashboard statistics
  Future<DashboardStats> getDashboardStats() async {
    try {
      final response = await _dio.get('$_baseUrl/api/v1/dashboard/stats');
      return DashboardStats.fromJson(response.data['data']);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  // ==================== CULTIVARS ENDPOINTS ====================

  /// Get list of cultivars
  Future<List<Cultivar>> getCultivars() async {
    try {
      final response = await _dio.get('$_baseUrl/api/v1/cultivars');
      final List<dynamic> cultivarsJson = response.data['data']['items'];
      return cultivarsJson.map((json) => Cultivar.fromJson(json)).toList();
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  /// Get single cultivar by ID
  Future<Cultivar> getCultivar(int id) async {
    try {
      final response = await _dio.get('$_baseUrl/api/v1/cultivars/$id');
      return Cultivar.fromJson(response.data['data']);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  /// Create new cultivar
  Future<Cultivar> createCultivar(Map<String, dynamic> cultivarData) async {
    try {
      final response = await _dio.post(
        '$_baseUrl/api/v1/cultivars',
        data: cultivarData,
      );
      return Cultivar.fromJson(response.data['data']);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  /// Update cultivar
  Future<Cultivar> updateCultivar(
      int id, Map<String, dynamic> cultivarData) async {
    try {
      final response = await _dio.put(
        '$_baseUrl/api/v1/cultivars/$id',
        data: cultivarData,
      );
      return Cultivar.fromJson(response.data['data']);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  /// Delete cultivar
  Future<void> deleteCultivar(int id) async {
    try {
      await _dio.delete('$_baseUrl/api/v1/cultivars/$id');
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  // ==================== CART ENDPOINTS ====================

  /// Get cart items
  Future<List<CartItem>> getCartItems() async {
    try {
      final response = await _dio.get('$_baseUrl/api/v1/cart');
      final List<dynamic> cartItemsJson = response.data['data']['items'];
      return cartItemsJson.map((json) => CartItem.fromJson(json)).toList();
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  /// Add item to cart
  Future<CartItem> addToCart(Map<String, dynamic> cartItemData) async {
    try {
      final response = await _dio.post(
        '$_baseUrl/api/v1/cart/add',
        data: cartItemData,
      );
      return CartItem.fromJson(response.data['data']);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  /// Remove item from cart
  Future<void> removeFromCart(int itemId) async {
    try {
      await _dio.delete('$_baseUrl/api/v1/cart/$itemId');
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  /// Update cart item quantity
  Future<CartItem> updateCartItem(int itemId, {required int quantity}) async {
    try {
      final response = await _dio.put(
        '$_baseUrl/api/v1/cart/$itemId',
        data: {'quantity': quantity},
      );
      return CartItem.fromJson(response.data['data']);
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  /// Clear cart
  Future<void> clearCart() async {
    try {
      await _dio.delete('$_baseUrl/api/v1/cart/clear');
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  /// Checkout cart
  Future<Map<String, dynamic>> checkout() async {
    try {
      final response = await _dio.post('$_baseUrl/api/v1/cart/checkout');
      return response.data['data'];
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }

  // ==================== UTILITY METHODS ====================

  /// Test API connectivity
  Future<bool> isApiReachable() async {
    try {
      await _dio.get('$_baseUrl/api/v1/health');
      return true;
    } catch (e) {
      return false;
    }
  }

  /// Get API status
  Future<String> getApiStatus() async {
    try {
      final response = await _dio.get('$_baseUrl/api/v1/health');
      return 'API is healthy: ${response.data}';
    } catch (e) {
      return 'API connection failed: $e';
    }
  }

  /// Clean up resources
  void dispose() {
    _dio.close();
  }
}
