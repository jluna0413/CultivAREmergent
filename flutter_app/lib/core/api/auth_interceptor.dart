import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../../core/constants/app_constants.dart';
import '../../core/auth/oauth_repository.dart';

/// AuthInterceptor that properly handles async token retrieval
/// Uses QueuedInterceptor to ensure requests wait for token read
class AuthInterceptor extends QueuedInterceptor {
  AuthInterceptor(this._secureStorage, this._dio);

  final FlutterSecureStorage _secureStorage;
  final Dio _dio;

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    print('DEBUG AuthInterceptor: onRequest for ${options.path}');

    try {
      final accessToken = await _secureStorage.read(
        key: AppConstants.accessTokenKey,
      );

      print(
        'DEBUG AuthInterceptor: accessToken = ${accessToken != null ? "PRESENT (${accessToken.length} chars)" : "NULL"}',
      );

      if (accessToken != null) {
        options.headers['Authorization'] = 'Bearer $accessToken';
        print('DEBUG AuthInterceptor: Added Authorization header');
      }

      // Add CSRF token if available
      final csrfToken = await _secureStorage.read(key: 'X-CSRF-Token');
      if (csrfToken != null) {
        options.headers['X-CSRF-Token'] = csrfToken;
      }
    } catch (e) {
      print('DEBUG AuthInterceptor: Error reading token: $e');
    }

    handler.next(options);
  }

  @override
  Future<void> onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    if (err.response?.statusCode == 401) {
      // If the failed request was already a refresh attempt, don't loop
      if (err.requestOptions.path.contains(AppConstants.authRefresh)) {
        await _secureStorage.delete(key: AppConstants.accessTokenKey);
        await _secureStorage.delete(key: AppConstants.refreshTokenKey);
        return handler.next(err);
      }

      // Try to refresh the token using OAuthRepository
      try {
        // We need to get the repository instance.
        // Since this is inside an interceptor, accessing Riverpod providers is hard.
        // We'll use the singleton accessor.
        await getOAuthRepository().refreshToken();

        // If successful, tokens are updated in storage
        final newAccessToken = await _secureStorage.read(
          key: AppConstants.accessTokenKey,
        );

        if (newAccessToken != null) {
          // Retry the original request with the new token
          err.requestOptions.headers['Authorization'] =
              'Bearer $newAccessToken';
          final clonedRequest = await _dio.fetch(err.requestOptions);
          return handler.resolve(clonedRequest);
        }
      } catch (e) {
        // Refresh failed
        await getOAuthRepository().logout();
        return handler.next(err);
      }
    }
    handler.next(err);
  }
}
