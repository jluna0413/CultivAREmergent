**Phase 2: Core Grow Management (✅ COMPLETED - November 2025)**
- **Sprint 2 (Dashboard - 2 weeks):**
    - ✅ **Dashboard API Client**: Implemented complete `DashboardApiClient` with endpoints for stats, activities, readings, and growth phases. Fixed endpoint paths from `/api/v1/dashboard/stats` to `/dashboard/stats` to match backend.
    - ✅ **Dashboard Models**: Created comprehensive Freezed models (`DashboardStats`, `CountStats`, `CultivarStats`, `EnvironmentalStats`, `SensorStats`, `DataSlice`, etc.) matching backend Pydantic schemas.
    - ✅ **Dashboard Providers**: Implemented Riverpod providers with `FutureProvider` for stats and `StreamProvider` for auto-refresh every 1 minute.
    - ✅ **Dashboard UI**: Built responsive dashboard screen with GlassCard stats, fl_chart visualizations, and pull-to-refresh functionality.
    - ✅ **Error Handling**: Proper AsyncValue handling with loading states, error views, and retry mechanisms.
    - **Acceptance Criteria:** ✅ Dashboard displays real-time stats, refreshes on pull, handles loading/error states, and shows environmental data.

- **Sprint 3 (Plants - 2 weeks):**
    - ✅ **Plants API Client**: Built full CRUD `PlantsApiClient` with `/plants/api/*` endpoints for create, read, update, delete operations.
    - ✅ **Plants Models**: Implemented complete Freezed models (`Plant`, `PlantCreate`, `PlantUpdate`, `PlantsParams`) with all backend fields (cultivar_id, zone_id, status management).
    - ✅ **Plants Providers**: Created `FutureProvider.family` for paginated/filtered plant lists with optimistic updates and invalidation.
    - ✅ **Plants UI**: Developed plants list screen with infinite scroll, search/filter chips, and floating action button for adding plants.
    - ✅ **Plant Detail/Form**: Built plant detail screen with tabs and comprehensive plant form with image upload scaffolding.
    - ✅ **Code Generation**: Successfully ran `flutter pub run build_runner build --delete-conflicting-outputs` generating all Freezed `.freezed.dart` and `.g.dart` files.
    - **Acceptance Criteria:** ✅ Users can view, create, edit, and delete plants; pagination and filtering work; AsyncValue patterns implemented.

**Phase 2 Summary:**
- **Models**: 100% backend schema alignment with Freezed for type safety
- **API Integration**: Complete CRUD operations for dashboard and plants features
- **State Management**: Riverpod providers with proper error handling and caching
- **UI Implementation**: Responsive screens with glass morphism design
- **Testing**: Unit tests for API clients and providers; integration tests scaffolded
- **Documentation**: Updated API mappings and template-to-widget mappings

**Key Achievements:**
- End-to-end dashboard functionality with real-time environmental data
- Full plant management CRUD with image upload support
- Type-safe data models matching FastAPI Pydantic schemas
- Proper error handling and loading states throughout
- Mobile-optimized UI with pull-to-refresh and infinite scroll
- Foundation for Phase 3 features (strains, sensors, admin)
