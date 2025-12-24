// AGENT_SIGNATURE: (Agent Type: IDE, Name: Kilo-Code, Action: [Edit/Refactor/Fix])
// Re-export canonical auth provider implementation to avoid duplicate/conflicting providers.
//
// This file intentionally re-exports the AsyncNotifier-based providers implemented
// in ../state/auth_provider.dart. Keeping a single canonical provider implementation
// prevents symbol collisions and reduces analyzer errors caused by duplicate types.
export '../state/auth_provider.dart';
