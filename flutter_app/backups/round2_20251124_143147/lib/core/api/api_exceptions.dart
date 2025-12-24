/// API exception hierarchy used throughout the app to represent errors
/// returned from the backend or produced by the client layer.
///
/// Each exception exposes a user-friendly message and optional technical
/// details for logging.
class ApiException implements Exception {
  ApiException({this.statusCode, required this.message, this.details});
  final int? statusCode;
  final String message;
  final dynamic details;

  @override
  String toString() {
    return 'ApiException(statusCode: $statusCode, message: $message, details: $details)';
  }
}

/// Validation errors (HTTP 400) with optional field-level messages.
/// fieldErrors maps fieldName -> list of messages.
class ValidationException extends ApiException {
  ValidationException({
    int? statusCode,
    required super.message,
    this.fieldErrors = const {},
    super.details,
  }) : super(statusCode: statusCode ?? 400);
  final Map<String, List<String>> fieldErrors;

  @override
  String toString() {
    return 'ValidationException(statusCode: $statusCode, message: $message, fieldErrors: $fieldErrors)';
  }
}

/// Authentication errors (HTTP 401)
class AuthException extends ApiException {
  AuthException({
    int? statusCode,
    super.message = 'Unauthorized',
    super.details,
  }) : super(statusCode: statusCode ?? 401);
}

/// Forbidden access (HTTP 403)
class ForbiddenException extends ApiException {
  ForbiddenException({
    int? statusCode,
    super.message = 'Forbidden',
    super.details,
  }) : super(statusCode: statusCode ?? 403);
}

/// Resource not found (HTTP 404)
class NotFoundException extends ApiException {
  NotFoundException({
    int? statusCode,
    super.message = 'Not Found',
    super.details,
  }) : super(statusCode: statusCode ?? 404);
}

/// Server-side error (HTTP 5xx)
class ServerException extends ApiException {
  ServerException({
    int? statusCode,
    super.message = 'Server Error',
    super.details,
  }) : super(statusCode: statusCode ?? 500);
}

/// Network-level errors (no connectivity)
class NetworkException extends ApiException {
  NetworkException({super.message = 'No internet connection', super.details})
    : super(statusCode: null);
}

/// Request timeout
class TimeoutException extends ApiException {
  TimeoutException({super.message = 'Request timed out', super.details})
    : super(statusCode: null);
}
