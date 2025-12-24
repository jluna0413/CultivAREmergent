import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../../core/constants/app_constants.dart';
import '../../core/api/api_exceptions.dart' as api_ex;
import '../../core/api/auth_interceptor.dart';

import 'dart:math';
import '../models/auth_models.dart';
import '../models/plant_models.dart';
import '../models/cultivar_models.dart';
import '../models/sensor_models.dart';
import '../models/product_models.dart' hide CartItem;
import '../models/cart_models.dart' hide Product;
import '../../features/marketplace/models/marketplace_listing.dart';

class ApiClient {
  factory ApiClient() {
    return _singleton;
  }

  ApiClient._internal() {
    _dio = Dio(
      BaseOptions(
        baseUrl: AppConstants.apiBaseUrl,
        connectTimeout: const Duration(milliseconds: AppConstants.apiTimeoutMs),
        receiveTimeout: const Duration(milliseconds: AppConstants.apiTimeoutMs),
        headers: const {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    );

    // Add auth interceptor for automatic token injection
    const secureStorage = FlutterSecureStorage();
    _dio.interceptors.add(AuthInterceptor(secureStorage, _dio));

    if (AppConstants.logNetworkTraffic) {
      _dio.interceptors.add(
        LogInterceptor(
          requestBody: true,
          responseBody: true,
          error: true,
          requestHeader: true,
          responseHeader: true,
        ),
      );
    }
  }

  ApiClient.fromDio(this._dio);

  static final ApiClient _singleton = ApiClient._internal();
  late Dio _dio;

  Dio get dio => _dio;

  // Generic GET request
  Future<T> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
    ProgressCallback? onReceiveProgress,
  }) async {
    try {
      final response = await _dio.get(
        path,
        queryParameters: queryParameters,
        options: options,
        cancelToken: cancelToken,
        onReceiveProgress: onReceiveProgress,
      );
      return response.data as T;
    } on DioException catch (e) {
      throw handleDioError(e);
    }
  }

  // Generic POST request
  Future<T> post<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
    ProgressCallback? onSendProgress,
    ProgressCallback? onReceiveProgress,
  }) async {
    try {
      final response = await _dio.post(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
        cancelToken: cancelToken,
        onSendProgress: onSendProgress,
        onReceiveProgress: onReceiveProgress,
      );
      return response.data as T;
    } on DioException catch (e) {
      throw handleDioError(e);
    }
  }

  // Generic PUT request
  Future<T> put<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
    ProgressCallback? onSendProgress,
    ProgressCallback? onReceiveProgress,
  }) async {
    try {
      final response = await _dio.put(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
        cancelToken: cancelToken,
        onSendProgress: onSendProgress,
        onReceiveProgress: onReceiveProgress,
      );
      return response.data as T;
    } on DioException catch (e) {
      throw handleDioError(e);
    }
  }

  // Generic DELETE request
  Future<T> delete<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
  }) async {
    try {
      final response = await _dio.delete(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
        cancelToken: cancelToken,
      );
      return response.data as T;
    } on DioException catch (e) {
      throw handleDioError(e);
    }
  }

  AuthResponse _mockAuthResponse({required String email, String? username}) {
    final now = DateTime.now();
    final id = Random().nextInt(10000);
    return AuthResponse(
      accessToken: 'access_$id',
      tokenType: 'bearer',
      refreshToken: 'refresh_$id',
      user: User(
        id: id,
        email: email,
        username: username ?? email.split('@').first,
        avatar: null,
        createdAt: now,
        updatedAt: now,
      ),
    );
  }

  // Plants API methods
  Future<List<PlantModel>> getPlants() async {
    return await get('/api/v1/plants');
  }

  // Cart methods
  Future<List<dynamic>> getCart() async {
    final response = await get('/api/v1/cart/');
    return response['items'] as List<dynamic>;
  }

  Future<void> addToCart(
    int listingId, {
    int quantity = 1,
    int packSize = 5,
  }) async {
    await post(
      '/api/v1/cart/',
      data: {
        'listing_id': listingId,
        'quantity': quantity,
        'pack_size': packSize,
      },
    );
  }

  Future<void> removeFromCart(int cartItemId) async {
    await delete('/api/v1/cart/$cartItemId');
  }

  Future<void> clearCart() async {
    await delete('/api/v1/cart/');
  }

  Future<List<Cultivar>> getCultivars() async {
    return await get('/api/v1/cultivars');
  }

  Future<List<Sensor>> getAllSensors() async {
    return await get('/api/v1/sensors');
  }

  Future<List<dynamic>> getSensors() async {
    return await get<List<dynamic>>('/api/v1/sensors');
  }

  Future<List<CartItem>> getCartItems() async {
    return await get('/api/v1/cart');
  }

  // Products / Listings methods
  Future<List<MarketplaceListing>> getMarketplaceListings() async {
    // We map the backend GNFTListingResponse to our MarketplaceListing model
    // This allows gradual migration if backend fields differ significantly
    final List<dynamic> response = await get('/api/v1/marketplace/listings');

    return response.map((json) {
      // Manual mapping if needed or use fromJson if schema matches
      // Ideally, update MarketplaceListing to match GNFTListingResponse
      // For now, let's map known fields
      return MarketplaceListing.fromJson({
        'id': json['id'].toString(),
        'strainName':
            json['strain_name'] ?? json['listing_title'] ?? 'Unknown Strain',
        'breederName': json['breeder_name'] ?? 'Unknown Breeder',
        'badge': 'none', // Not in backend yet
        'imageUrl': json['image_url'] ?? 'https://via.placeholder.com/400',
        'price':
            (json['pack_5_price'] ?? json['pack_10_price'] ?? 0.0) as double,
        'availablePacks':
            (json['pack_5_available'] ?? json['pack_10_available'] ?? 0) as int,
        'thcPercentage': (json['thc_percentage'] ?? 0.0) as double,
        'isIndica': json['is_indica'] ?? true,
        'isExclusive': false, // Add logic if needed
      });
    }).toList();
  }

  Future<Map<String, dynamic>> processCheckout({
    required List<Map<String, dynamic>> items,
    String? shippingAddress,
    String paymentMethod = "card",
  }) async {
    return await post(
      '/api/v1/checkout/',
      data: {
        'items': items,
        'shipping_address': shippingAddress,
        'payment_method': paymentMethod,
      },
    );
  }

  // Deprecated/Legacy Products Calls
  Future<List<Product>> getProducts() async {
    return await get('/api/v1/products');
  }

  Future<Map<String, dynamic>> getProductsPaginated({
    int page = 1,
    int pageSize = 10,
  }) async {
    return await get(
      '/api/v1/products',
      queryParameters: {'page': page, 'page_size': pageSize},
    );
  }

  Future<Cultivar> getCultivar(int id) async {
    return await get('/api/v1/cultivars/$id');
  }

  Future<Cultivar> createCultivar(dynamic cultivarData) async {
    return await post('/api/v1/cultivars', data: cultivarData);
  }

  Future<Cultivar> updateCultivar(int id, dynamic cultivarData) async {
    return await put('/api/v1/cultivars/$id', data: cultivarData);
  }

  Future<void> deleteCultivar(int id) async {
    await delete('/api/v1/cultivars/$id');
  }

  api_ex.ApiException handleDioError(DioException error) {
    String message = 'An unknown error occurred.';
    int? statusCode = error.response?.statusCode;
    dynamic responseData = error.response?.data;

    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.receiveTimeout:
      case DioExceptionType.sendTimeout:
        return api_ex.TimeoutException(
          message: 'Connection timed out. Please try again.',
        );
      case DioExceptionType.badResponse:
        if (statusCode != null) {
          if (statusCode >= 500) {
            return api_ex.ServerException(
              statusCode: statusCode,
              message: 'Server error. Please try again later.',
            );
          } else if (statusCode == 400) {
            return api_ex.ValidationException(
              statusCode: statusCode,
              message: responseData?['detail'] as String? ?? 'Bad request.',
            );
          } else if (statusCode == 401) {
            return api_ex.AuthException(
              statusCode: statusCode,
              message: responseData?['detail'] as String? ?? 'Unauthorized.',
            );
          } else if (statusCode == 403) {
            return api_ex.ForbiddenException(
              statusCode: statusCode,
              message: responseData?['detail'] as String? ?? 'Forbidden.',
            );
          } else if (statusCode == 404) {
            return api_ex.NotFoundException(
              statusCode: statusCode,
              message: responseData?['detail'] as String? ?? 'Not found.',
            );
          } else if (statusCode == 422) {
            final detail = responseData?['detail'];
            String msg = 'Validation error.';
            if (detail is List) {
              msg = detail.map((e) => e['msg'] ?? e.toString()).join(', ');
            } else if (detail is String) {
              msg = detail;
            }
            return api_ex.ValidationException(
              statusCode: statusCode,
              message: msg,
            );
          }
        }

        final detail = responseData?['detail'];
        if (detail is String) {
          message = detail;
        } else if (detail is List) {
          message = detail.map((e) => e.toString()).join(', ');
        } else {
          message = error.response?.statusMessage ?? message;
        }
        break;
      case DioExceptionType.cancel:
        return api_ex.ApiException(
          message: 'Request to API server was cancelled.',
        );
      case DioExceptionType.unknown:
        return api_ex.NetworkException(
          message: 'No internet connection or server is unreachable.',
        );
      default:
        break;
    }

    return api_ex.ApiException(
      message: message,
      statusCode: statusCode,
      details: responseData,
    );
  }
}
