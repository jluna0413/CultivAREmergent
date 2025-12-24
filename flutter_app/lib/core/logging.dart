import 'package:flutter/foundation.dart';

/// Small centralized logging wrapper with leveled logging and timestamps.
///
/// Rationale: keep logs easy to read in debug builds and provide a single
/// place to swap in structured loggers later (e.g. `package:logger`).
class AppLogger {
  AppLogger._();

  static String _prefix(String level) {
    final now = DateTime.now().toIso8601String();
    return '[$now] [$level]';
  }

  /// Debug-level log (verbose). Only prints in non-release builds.
  static void debug(String message) {
    if (!kReleaseMode) debugPrint('${_prefix('DEBUG')} $message');
  }

  /// Info-level log (default visible in all builds).
  static void info(String message) {
    debugPrint('${_prefix('INFO')} $message');
  }

  /// Warn-level log.
  static void warn(String message) {
    debugPrint('${_prefix('WARN')} $message');
  }

  /// Error-level log with optional error and stack trace.
  static void error(String message, [Object? error, StackTrace? stack]) {
    debugPrint('${_prefix('ERROR')} $message');
    if (error != null) debugPrint('  error: $error');
    if (stack != null) debugPrint('  stack: $stack');
  }

  /// Backwards-compatible alias used in previous commits.
  static void log(String message) => info(message);
}
