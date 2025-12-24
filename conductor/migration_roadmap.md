# Migration Roadmap: CultivAR

## 🏗️ As-Is Architecture
The current "Brownfield" state of the project.

### Backend
- **Dual-Stack**: Core logic resides in FastAPI (`port:4200`), but legacy Flask (`port:5000`) remains for unmigrated admin tools.
- **Database**: Shared PostgreSQL schema. FastAPI uses `SQLAlchemy 2.0 (Async)`, while some scripts still use sync drivers.
- **Trust Engine**: `AuditOrchestrator` exists but relies on partial mocks and mixed sync/async patterns.
- **Marketplace**: Routers exist (`market.py`, `strains.py`) but return "Coming Soon" templates for most views.

### Frontend
- **Framework**: Flutter Web (`port:4242`).
- **State**: Riverpod Providers for `Auth`, `Plants`, `Sensors`.
- **Navigation**: GoRouter with some legacy route definitions.

---

## 🚀 To-Be Architecture (Target)
The "Greenfield" goal managed by Conductor.

1.  **Unified Async Backend**: 100% removals of Flask dependencies and synchronous DB calls.
2.  **Enterprise Identity**: Full OAuth 2.0 / OIDC integration (Keycloak) replacing custom JWT auth.
3.  **Trust Engine V2**: A fully autonomous agentic workflow for verifying genetic lineage on-chain (Algorand).
4.  **Live Marketplace**: A P2P functional marketplace for genetics and equipment.

---

## 🗺️ Migration Phases

### Phase 1: Ingestion & Stabilization (Current)
- [x] Conductor Integration (Eternal Memory).
- [x] Landing Page Visuals (Verification of Brownfield flow).
- [ ] **Trust Engine V2**: Porting `AuditOrchestrator` to fully async service layer.
- [ ] **Auth Migration**: Replacing local auth with `Keycloak` integration.

### Phase 2: Feature Expansion
- [ ] **Marketplace**: Enabling `feat-marketplace-listings`.
- [ ] **AC Infinity**: Full bi-directional control via MQTT/WebSocket.

### Phase 3: Legacy Sunset
- [ ] **Deprecate Flask**: Shutdown port 5000.
- [ ] **Archive Legacy**: Move `legacy/` to cold storage.
