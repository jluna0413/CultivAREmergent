// Minimal API exception stubs to satisfy analyzer during incremental fixes.
// AGENT_SIGNATURE: (Agent Type: IDE, Name: Kilo-Code, Action: [Edit/Refactor/Fix])

/// Base API exception used across services
class ApiException implements Exception {
  ApiException({this.message, this.statusCode, this.details});
  final String? message;
  final int? statusCode;
  final dynamic details;

  @override
  String toString() => 'ApiException: ${message ?? 'Unknown error'}';
}

/// Common specialized exceptions for typical API error cases
class ValidationException extends ApiException {
  ValidationException({super.message, super.statusCode, super.details});
}

class AuthException extends ApiException {
  AuthException({super.message, super.statusCode, super.details});
}

class ForbiddenException extends ApiException {
  ForbiddenException({super.message, super.statusCode, super.details});
}

class NotFoundException extends ApiException {
  NotFoundException({super.message, super.statusCode, super.details});
}

class ServerException extends ApiException {
  ServerException({super.message, super.statusCode, super.details});
}

class NetworkException extends ApiException {
  NetworkException({super.message, super.statusCode, super.details});
}

class TimeoutException extends ApiException {
  TimeoutException({super.message, super.statusCode, super.details});
}

// AGENT_SIGNATURE: (Agent Type: IDE, Name: Kilo-Code, Action: [Edit/Refactor/Fix])
