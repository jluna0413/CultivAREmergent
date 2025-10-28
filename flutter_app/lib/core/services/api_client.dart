/// API Client for FastAPI backend integration
/// Handles HTTP requests, authentication, and error handling
import 'package:dio/dio.dart';
import 'package:pretty_dio_logger/pretty_dio_logger.dart';
import '../logging.dart';

import '../config/app_config.dart';
import '../models/auth_models.dart';
import '../models/create_plant_request.dart';
import '../models/cultivar_models.dart';
import '../models/dashboard_stats.dart';
import '../models/plant_models.dart';

class ApiClient {
  late final Dio _dio;
  static const int _connectTimeout = 15000;
  static const int _receiveTimeout = 15000;
  static const int _sendTimeout = 15000;

  ApiClient() {
    _dio = Dio();
    
    // Configure base options
    _dio.options.baseUrl = AppConfig.apiBaseUrl;
    _dio.options.connectTimeout = const Duration(milliseconds: _connectTimeout);
    _dio.options.receiveTimeout = const Duration(milliseconds: _receiveTimeout);
    _dio.options.sendTimeout = const Duration(milliseconds: _sendTimeout);
    _dio.options.headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };

    // Add logging interceptor for development
    _dio.interceptors.add(
      PrettyDioLogger(
        requestHeader: true,
        requestBody: true,
        responseBody: true,
        responseHeader: false,
        error: true,
        compact: true,
      ),
    );

    // Add interceptors for authentication and error handling
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: _onRequest,
      onError: _onError,
    ));
  }

  /// Set authentication token for requests
  void setAuthToken(String token) {
    _dio.options.headers['Authorization'] = 'Bearer $token';
  }

  /// Clear authentication token
  void clearAuthToken() {
    _dio.options.headers.remove('Authorization');
  }

  /// Handle request with authentication
  void _onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    AppLogger.log('Making request to: ${options.uri}');
    handler.next(options);
  }

  /// Handle API errors
  void _onError(DioException err, ErrorInterceptorHandler handler) {
    AppLogger.error('API Error: ${err.type} - ${err.message}', err);
    
    switch (err.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        throw ApiException('Connection timeout. Please check your internet connection.');
      case DioExceptionType.badResponse:
        final statusCode = err.response?.statusCode;
        final message = err.response?.data?['detail'] ?? 'Unknown error';
        throw ApiException('Server error ($statusCode): $message');
      case DioExceptionType.cancel:
        throw ApiException('Request was cancelled');
      default:
        throw ApiException('Network error: ${err.message}');
    }
  }

  // Authentication Endpoints

  Future<AuthResponse> login(String email, String password) async {
    try {
      final response = await _dio.post(
        '/auth/login',
        data: {
          'username': email,
          'password': password,
        },
      );
      
      return AuthResponse.fromJson(response.data);
    } on DioException catch (e) {
      throw ApiException('Login failed: ${e.message}');
    }
  }

  Future<AuthResponse> register({
    required String username,
    required String email,
    required String password,
  }) async {
    try {
      final response = await _dio.post(
        '/auth/register',
        data: {
          'username': username,
          'email': email,
          'password': password,
        },
      );
      
      return AuthResponse.fromJson(response.data);
    } on DioException catch (e) {
      throw ApiException('Registration failed: ${e.message}');
    }
  }

  Future<void> logout() async {
    try {
      await _dio.post('/auth/logout');
    } on DioException catch (e) {
      throw ApiException('Logout failed: ${e.message}');
    }
  }

  // Cultivar Endpoints

  Future<List<Cultivar>> getCultivars() async {
    try {
      final response = await _dio.get('/api/cultivars/list');
      
      if (response.data['status'] == 'success') {
        final List<dynamic> cultivarsJson = response.data['data'];
        return cultivarsJson.map((json) => Cultivar.fromJson(json)).toList();
      }
      
      throw ApiException('Failed to fetch cultivars');
    } on DioException catch (e) {
      throw ApiException('Failed to fetch cultivars: ${e.message}');
    }
  }

  Future<Cultivar> getCultivar(int id) async {
    try {
      final response = await _dio.get('/api/cultivars/$id');
      
      if (response.data['status'] == 'success') {
        return Cultivar.fromJson(response.data['data']);
      }
      
      throw ApiException('Cultivar not found');
    } on DioException catch (e) {
      throw ApiException('Failed to fetch cultivar: ${e.message}');
    }
  }

  Future<Cultivar> createCultivar(CreateCultivarRequest request) async {
    try {
      final response = await _dio.post(
        '/api/cultivars/create',
        data: request.toJson(),
      );
      
      return Cultivar.fromJson(response.data);
    } on DioException catch (e) {
      throw ApiException('Failed to create cultivar: ${e.message}');
    }
  }

  Future<Cultivar> updateCultivar(int id, CreateCultivarRequest request) async {
    try {
      final response = await _dio.put(
        '/api/cultivars/$id',
        data: request.toJson(),
      );
      
      return Cultivar.fromJson(response.data['data']);
    } on DioException catch (e) {
      throw ApiException('Failed to update cultivar: ${e.message}');
    }
  }

  Future<void> deleteCultivar(int id) async {
    try {
      await _dio.delete('/api/cultivars/$id');
    } on DioException catch (e) {
      throw ApiException('Failed to delete cultivar: ${e.message}');
    }
  }

  Future<Map<String, dynamic>> getCultivarStats() async {
    try {
      final response = await _dio.get('/api/cultivars/stats');
      
      if (response.data['status'] == 'success') {
        return response.data['data'];
      }
      
      throw ApiException('Failed to fetch cultivar statistics');
    } on DioException catch (e) {
      throw ApiException('Failed to fetch statistics: ${e.message}');
    }
  }

  // Plant Endpoints

  Future<List<Plant>> getPlants() async {
    try {
      final response = await _dio.get('/api/plants');
      
      if (response.data['status'] == 'success') {
        final List<dynamic> plantsJson = response.data['data'];
        return plantsJson.map((json) => Plant.fromJson(json)).toList();
      }
      
      throw ApiException('Failed to fetch plants');
    } on DioException catch (e) {
      throw ApiException('Failed to fetch plants: ${e.message}');
    }
  }

  Future<Plant> getPlant(int id) async {
    try {
      final response = await _dio.get('/api/plants/$id');
      
      if (response.data['status'] == 'success') {
        return Plant.fromJson(response.data['data']);
      }
      
      throw ApiException('Plant not found');
    } on DioException catch (e) {
      throw ApiException('Failed to fetch plant: ${e.message}');
    }
  }

  Future<Plant> createPlant(CreatePlantRequest request) async {
    try {
      final response = await _dio.post(
        '/api/plants',
        data: request.toJson(),
      );
      
      return Plant.fromJson(response.data['data']);
    } on DioException catch (e) {
      throw ApiException('Failed to create plant: ${e.message}');
    }
  }

  Future<Plant> updatePlant(int id, CreatePlantRequest request) async {
    try {
      final response = await _dio.put(
        '/api/plants/$id',
        data: request.toJson(),
      );
      
      return Plant.fromJson(response.data['data']);
    } on DioException catch (e) {
      throw ApiException('Failed to update plant: ${e.message}');
    }
  }

  Future<void> deletePlant(int id) async {
    try {
      await _dio.delete('/api/plants/$id');
    } on DioException catch (e) {
      throw ApiException('Failed to delete plant: ${e.message}');
    }
  }

  // Dashboard Endpoints

  Future<DashboardStats> getDashboardStats() async {
    try {
      final response = await _dio.get('/api/dashboard/stats');
      
      if (response.data['status'] == 'success') {
        return DashboardStats.fromJson(response.data['data']);
      }
      
      throw ApiException('Failed to fetch dashboard statistics');
    } on DioException catch (e) {
      throw ApiException('Failed to fetch dashboard: ${e.message}');
    }
  }

  // Utility Methods

  Future<bool> isApiReachable() async {
    try {
      await _dio.get('/health');
      return true;
    } catch (e) {
      return false;
    }
  }

  Future<String> testConnection() async {
    try {
      final response = await _dio.get('/health');
      return 'API is healthy: ${response.data}';
    } catch (e) {
      return 'API connection failed: $e';
    }
  }

  void dispose() {
    _dio.close();
  }
}

class ApiException implements Exception {
  final String message;
  
  const ApiException(this.message);
  
  @override
  String toString() => 'ApiException: $message';
}