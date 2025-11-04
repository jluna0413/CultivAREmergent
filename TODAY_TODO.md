# CultivAR Milestones Implementation - TODOs

## Task Overview
Implement 5 comprehensive milestones for CultivAR project involving Flask/FastAPI backend and Flutter frontend development.

## Todo Checklist

### Phase 1: API Parity and FastAPI Router Implementation (Milestone 3)
- [ ] 1.1 Analyze legacy endpoints from `app/blueprints` and `app/routes/routes.py`
- [ ] 1.2 Create `docs/API-Parity.md` enumerating all legacy endpoints by domain
- [ ] 1.3 Define Pydantic models in `app/fastapi_app/models/` for each domain
- [ ] 1.4 Implement FastAPI routers with CRUD operations and pagination for:
  - [ ] Plants domain
  - [ ] Strains domain  
  - [ ] Breeders domain
  - [ ] Clones domain
  - [ ] Activities domain
  - [ ] Users domain
  - [ ] Dashboard domain
- [ ] 1.5 Wire all routers in `app/fastapi_app/__init__.py`
- [ ] 1.6 Implement eager loading to avoid N+1 queries

### Phase 2: Flutter GoRouter Navigation Implementation (Milestone 4)
- [ ] 2.1 Add GoRouter dependency to `flutter_app/pubspec.yaml`
- [ ] 2.2 Create `flutter_app/lib/core/router/app_router.dart` with GoRouter
- [ ] 2.3 Mirror sidebar IA routes in GoRouter configuration
- [ ] 2.4 Add auth redirect hooks based on AuthService (logged-in, isAdmin)
- [ ] 2.5 Replace MaterialApp.routes with MaterialApp.router in `flutter_app/lib/main.dart`
- [ ] 2.6 Update existing screen navigation calls to use GoRouter APIs
- [ ] 2.7 Add basic deep links for key screens

### Phase 3: Design Tokens and Shared Flutter UI Components (Milestone 5)
- [ ] 3.1 Analyze semantic tokens from `app/web/static/css/styles.css`
- [ ] 3.2 Expand `flutter_app/lib/core/theme/app_theme.dart` with semantic tokens
- [ ] 3.3 Create shared widgets in `flutter_app/lib/core/widgets/`:
  - [ ] GlassCard widget
  - [ ] NavGlassAppBar widget  
  - [ ] Badge widget
- [ ] 3.4 Replace ad-hoc styling in existing screens to use tokens/widgets
- [ ] 3.5 Provide light/dark theme variants and toggle state

### Phase 4: Legacy Sidebar IA Port with Role-Based Visibility (Milestone 6)
- [ ] 4.1 Analyze menu structure from `app/web/templates/common/sidebar.html`
- [ ] 4.2 Port menu groups and items to `flutter_app/lib/core/widgets/sidebar_drawer.dart`
- [ ] 4.3 Include nested groups and active state handling
- [ ] 4.4 Read roles from AuthService instead of hardcoded flags
- [ ] 4.5 Ensure routes exist for each menu item (placeholder screens acceptable)
- [ ] 4.6 Add widget test for admin visibility functionality

### Phase 5: Feature Flags and Migration Governance (Milestone 10)
- [ ] 5.1 Add feature flags in `app/config/config.py` and create endpoint
- [ ] 5.2 Keep legacy Flask routes available until parity verification
- [ ] 5.3 Document rollout and rollback procedures in `docs/deployment_checklist.md`
- [ ] 5.4 Create Archon epic and tasks for each milestone in project 118a6a9c-20d4-42c3-a174-32fc37d474ea
- [ ] 5.5 Update `implementation_plan.md` with links and task status progression
- [ ] 5.6 Update `flutter_app/README.md` with run instructions, env config, and usage notes

### Cross-Cutting Tasks
- [ ] 6.1 Use Archon knowledge base to store implementation details
- [ ] 6.2 Update task progress: todo → doing → review as milestones progress
- [ ] 6.3 Verify all implementations follow project standards
- [ ] 6.4 Document any technical decisions and patterns used

## Success Criteria
- [ ] All 5 milestones implemented as specified
- [ ] Code follows project conventions and best practices
- [ ] Documentation updated and accurate
- [ ] Tests pass where applicable
- [ ] Archon project properly updated with progress
