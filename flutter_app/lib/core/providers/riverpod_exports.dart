// Re-export the `riverpod` and `state_notifier` packages for provider/state
// definitions used in non-UI contexts (pure Dart or test environments).
// Re-export `flutter_riverpod` for provider definitions (including UI providers) and
// `riverpod` + `state_notifier` for non-UI provider code. This centralizes
// provider-related imports for consistent type definitions.
// Re-export the `riverpod` and `state_notifier` packages for provider/state
// definitions used in non-UI contexts (pure Dart or test environments).
// Do NOT re-export `flutter_riverpod` here to avoid symbol collisions in
// provider declaration files; provider files will import `flutter_riverpod`
// directly when they need Flutter-specific helpers (StateNotifierProvider, etc.).
export 'package:flutter_riverpod/flutter_riverpod.dart';
// 'package:riverpod/state_notifier.dart' does not exist; don't export it.

// Export app-specific providers
