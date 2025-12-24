import 'package:dio/dio.dart';
import 'package:cultivar_app/core/api/api_client.dart';

class ErrorInterceptor extends Interceptor {
  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    // Map DioError to ApiException
    final apiException = ApiClient().handleDioError(err);
    handler.next(
      DioException(
        requestOptions: err.requestOptions,
        response: err.response,
        type: err.type,
        error: apiException, // Wrap the ApiException in the DioException
      ),
    );
  }
}
