import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../../core/api/api_client.dart';
import '../../core/api/auth_interceptor.dart';
import '../../core/api/error_interceptor.dart';
import '../../core/constants/app_constants.dart';

final apiClientProvider = Provider<ApiClient>((ref) {
  final Dio dio = Dio(
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

  final FlutterSecureStorage secureStorage = const FlutterSecureStorage();

  dio.interceptors.addAll([
    AuthInterceptor(secureStorage, dio),
    ErrorInterceptor(),
  ]);

  if (AppConstants.logNetworkTraffic) {
    dio.interceptors.add(
      LogInterceptor(
        requestBody: true,
        responseBody: true,
        error: true,
        requestHeader: true,
        responseHeader: true,
      ),
    );
  }

  return ApiClient.fromDio(dio);
});
