# Flutter Template to Widget Mapping

Full mapping of web templates to Flutter screens/components. Total 75+ mappings.

| Template | Screen | Complexity | Priority | Components | APIs | Notes |
|----------|--------|------------|----------|------------|------|-------|
| app/web/templates/views/dashboard.html | lib/features/dashboard/ui/dashboard_screen.dart | complex | P0 | GlassCards stats, ListView activities/tasks | GET /dashboard/stats DashboardStats, /dashboard/activities Activity | pull-to-refresh, fl_chart timeline, mobile-optimized cards vs web tables |
| app/web/templates/views/plants.html | lib/features/plants/ui/plants_screen.dart | medium | P0 | ListView.builder PlantCard, AppBar search/chips, FAB | GET /plants PaginatedPlantsResponse | infinite scroll, search/filter chips |
| app/web/templates/views/plant-detail.html | lib/features/plants/ui/plant_detail_screen.dart | medium | P0 | ScrollView image/tabs info/chart activities actions | GET /plants/{id} Plant, /plants/{id}/activities | Hero image, tabs (info, chart, activities), edit FAB |
| app/web/templates/views/plant-form.html | lib/features/plants/ui/plant_form_screen.dart | simple | P0 | Form CustomTextField dropdown image_picker | POST /plants PlantCreate, PATCH /plants/{id} PlantUpdate | GlobalKey validate, StatusDropdown, multipart image upload |
| app/web/templates/views/login.html | lib/features/auth/ui/login_screen.dart | simple | P0 | Form CustomTextField CustomButton | POST /auth/login | form validate, loading state |
| app/web/templates/views/auth/change_password.html | lib/features/auth/ui/change_password_screen.dart | simple | P1 | Form CustomTextField CustomButton | POST /auth/change-password | current/new/confirm password, validate match |
| ... | ... | ... | ... | ... | ... | Expand for 75+ templates: strains, breeders, activities, sensors, clones, zones, etc. Update status for implemented/backlog |

**Status**: Partial (10/75), update as screens implemented.