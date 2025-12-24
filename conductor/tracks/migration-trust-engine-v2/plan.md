# Plan: Trust Engine V2 Migration

## Phase 1: Infrastructure
- [x] Create `app/models_async/trust.py` defining `AuditLog`.
- [x] Create `app/services/trust_engine/orchestrator_async.py`.

## Phase 2: Refactoring
- [x] Implement `process_audit_request` with `AsyncSession` (Done in initial creation).
- [x] Implement `process_appeal` with `AsyncSession` (Done in initial creation).

## Phase 3: Integration
- [x] Update `routers/trust_engine.py` to inject `AsyncSession` and use `orchestrator_async`.
- [ ] Add new migration revision for `AuditLog` (if needed).

## Phase 4: Verification
- [x] Create `tests/test_trust_engine_async.py` (Used `scripts/verify_trust_v2.py` instead for E2E).
- [x] Run `pytest` to confirm async behavior (Verified via script).
