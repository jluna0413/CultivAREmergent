# Track Spec: Migration Trust Engine V2

## Context
The legacy `AuditOrchestrator` uses mocked verification steps and print statements. To truly "Verify" genetic lineage, we need to connect this to the real `AsyncSession` database and persist the audit logs.

## Goals
1.  **Async-First**: The new `AuditOrchestrator` must use `sqlalchemy.ext.asyncio.AsyncSession` for all IO.
2.  **Persistence**: Audit results (Pass/Fail) must be stored in a `AuditLog` table (or similar) within Postgres.
3.  **Real RAG**: Connect `HyperGraphRAG` to real vector search (mocked for now, but configured for real async IO).
4.  **Admin Override**: Ensure the appeal process actually updates the status in the DB.


## Data Models
**File**: `app/models_async/trust.py` (New)

### `AuditLog`
- `id`: Integer, PK
- `listing_id`: String, Index (Listing hash or UUID)
- `merchant_id`: String, Index (Wallet address)
- `strain_name`: String
- `status`: String (`PENDING`, `APPROVED`, `FAILED`, `APPROVED_BY_APPEAL`)
- `trust_score`: Float
- `rag_confidence`: Float
- `raw_data`: JSON (Stores `rag_result` and `circuit_result`)
- `created_at`: DateTime

## Technical Design
- **Location**: `app/services/trust_engine/orchestrator_async.py` (New File).
- **Dependency Injection**: Must handle `db: AsyncSession` injection via FastAPI Depends.
- **Workflow**:
  - `trigger_audit(listing_id)` -> Fetch Listing -> Run RAG -> Run Circuit -> Update Listing Status -> Create Audit Log.

## Acceptance Criteria
- [ ] `orchestrator_async.py` exists and is fully async.
- [ ] `POST /trust/audit/{id}` successfully updates a listing's status in the DB.
- [ ] No synchronous DB calls (check via `check_everything.py` or manual review).
