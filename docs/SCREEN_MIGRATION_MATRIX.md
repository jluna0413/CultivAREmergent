# Screen Migration Matrix

## Overview

This document provides a comprehensive screen-by-screen migration tracking matrix from legacy HTML/CSS/JS templates to Flutter screens. It maps all 40+ legacy templates to Flutter screens with priority levels, status tracking, and validation criteria.

## Matrix Structure

| Legacy Template Path | Flutter Screen Path | Priority | Status | Design Parity % | Functional Parity % | Phase | Dependencies | Validation Checklist | Notes |
|---------------------|--------------------|----------|---------|------------------|---------------------|-------|--------------|---------------------|-------|
| `app/web/templates/views/dashboard.html` | `flutter_app/lib/screens/dashboard/dashboard_screen.dart` | P0-Critical | In Progress | 85% | 90% | Phase 2 | AppTheme, DashboardProvider, StatCard | Visual comparison, API integration, performance test | Core screen with stats cards and plant overview |
| `app/web/templates/views/plants.html` | `flutter_app/lib/screens/plants_screen.dart` | P0-Critical | Pending | 0% | 0% | Phase 2 | PlantsProvider, PlantCard, FilterBar | CRUD operations, filtering, pagination | Grid/list view toggle, real-time filtering |
| `app/web/templates/views/plant.html` | `flutter_app/lib/screens/plant_detail_screen.dart` | P0-Critical | Pending | 0% | 0% | Phase 2 | TimelineWidget, ActivitiesProvider | Detail view, timeline, quick actions | Activity timeline, watering/feeding actions |
| `app/web/templates/views/cultivars.html` | `flutter_app/lib/screens/cultivars_screen.dart` | P0-Critical | Pending | 0% | 0% | Phase 2 | CultivarsProvider, CultivarCard | Genetics slider, breeder management | Cultivar type badges, autoflower support |
| `app/web/templates/views/sensors.html` | `flutter_app/lib/screens/sensors_screen.dart` | P0-Critical | Pending | 0% | 0% | Phase 2 | SensorsProvider, SensorCard | Zone organization, real-time data | Zone-based grouping, sensor readings |
| `app/web/templates/views/new_login.html` | `flutter_app/lib/features/auth/screens/login_screen.dart` | P0-Critical | Pending | 0% | 0% | Phase 2 | AuthProvider, AuthService | Login flow, error handling, validation | Enhanced existing implementation |
| `app/web/templates/common/base.html` + `sidebar.html` | `flutter_app/lib/core/widgets/sidebar_drawer.dart` | P0-Critical | Pending | 0% | 0% | Phase 2 | AppRouter, AuthProvider | Navigation, active states, responsiveness | Glass morphism background, expandable menus |
| `app/web/templates/views/settings.html` | `flutter_app/lib/screens/settings_screen.dart` | P1-High | Pending | 0% | 0% | Phase 3 | ThemeProvider, UsersProvider | Tabbed interface, theme toggle, user mgmt | 6 tabs: General, Users, Sensors, Backup, Issue, About |
| `app/web/templates/admin/users.html` | `flutter_app/lib/screens/admin_users_screen.dart` | P1-High | Pending | 0% | 0% | Phase 3 | UsersProvider (admin) | User CRUD, bulk operations, role management | Admin-only access, force password reset |
| `app/web/templates/views/cart.html` | `flutter_app/lib/screens/cart_screen.dart` | P1-High | Pending | 0% | 0% | Phase 3 | CartProvider | Cart operations, checkout flow, persistence | Shopping cart with quantity controls |
| `app/web/templates/views/clones/*` | `flutter_app/lib/screens/clones/*` | P1-High | Pending | 0% | 0% | Phase 3 | ClonesProvider | Clone management, parent selection | Clone-specific workflows |
| `app/web/templates/views/activities.html` | `flutter_app/lib/screens/activities_screen.dart` | P1-High | Pending | 0% | 0% | Phase 3 | ActivitiesProvider | Activity logging, filtering, timeline | Activity management interface |
| `app/web/templates/views/market/*` | `flutter_app/lib/screens/market/*` | P1-High | Pending | 0% | 0% | Phase 3 | MarketProvider | Product browsing, cart integration | Market section with categories |
| `app/web/templates/admin/export.html` | `flutter_app/lib/screens/admin_export_screen.dart` | P2-Medium | Pending | 0% | 0% | Phase 3 | ExportService | Data export, backup/restore | Admin-only export functionality |
| `app/web/templates/views/user_dashboard.html` | `flutter_app/lib/screens/user_profile_screen.dart` | P2-Medium | Pending | 0% | 0% | Phase 3 | AuthProvider, UsersProvider | Profile management, settings | User-specific dashboard |
| `app/web/templates/marketing/*` | `flutter_app/lib/screens/marketing/*` | P3-Low | Backlog | 0% | 0% | Phase 4 | Static content | Static pages, SEO optimization | May remain web-only |
| `app/web/templates/newsletter/*` | `flutter_app/lib/screens/newsletter/*` | P3-Low | Backlog | 0% | 0% | Phase 4 | NewsletterProvider | Subscription management | Email newsletter integration |
| `app/web/templates/blog/*` | `flutter_app/lib/screens/blog/*` | P3-Low | Backlog | 0% | 0% | Phase 4 | BlogProvider | Content display, comments | Blog/news section |
| `app/web/templates/social/*` | `flutter_app/lib/screens/social/*` | P3-Low | Backlog | 0% | 0% | Phase 4 | SocialProvider | Social sharing, integration | Social media features |

## Priority Definitions

### P0 - Critical (Phase 2)
- **Core user workflows**: Authentication, dashboard, primary CRUD operations
- **Business critical**: Plant management, cultivar catalog, sensor monitoring
- **Must have 100% parity before Phase 3**
- **Timeline**: Weeks 3-5

### P1 - High (Phase 3)
- **Important features**: Settings, user management, market, cart
- **Enhanced functionality**: Clone management, activities, admin features
- **Timeline**: Weeks 6-7

### P2 - Medium (Phase 3)
- **Supporting features**: Export, user profile, advanced admin
- **Timeline**: Week 7 (end of Phase 3)

### P3 - Low (Phase 4 or Post-Launch)
- **Optional features**: Marketing, newsletter, blog, social
- **May remain web-only** depending on user feedback
- **Timeline**: Week 8-9 or post-launch

## Status Definitions

- **Not Started**: Screen implementation has not begun
- **In Progress**: Screen implementation is underway
- **Complete**: Screen implementation is finished
- **Validated**: Screen has passed all validation checks
- **Backlog**: Deferred to later phase

## Validation Checklist Per Screen

### Design Parity Validation
- [ ] Visual comparison against legacy template (pixel-perfect matching)
- [ ] Color scheme matches exactly (hex value verification)
- [ ] Typography matches (font sizes, weights, line heights)
- [ ] Spacing matches (padding, margins, gaps)
- [ ] Border radius matches
- [ ] Shadow/elevation matches
- [ ] Animations match (duration, easing, effects)
- [ ] Glass morphism effects replicated
- [ ] Dark/light theme support identical to legacy
- [ ] Responsive breakpoints work correctly
- [ ] Icons match (FontAwesome → Material Icons mapping)

### Functional Parity Validation
- [ ] All CRUD operations work identically
- [ ] Filtering works with same options and results
- [ ] Search works with same behavior (case-insensitive, partial match)
- [ ] Pagination works with same page sizes and navigation
- [ ] Sorting works with same options and default order
- [ ] Modals/dialogs work with same forms and validation
- [ ] Quick actions work (water, feed, etc.)
- [ ] View toggles work and persist preferences
- [ ] Form validation matches backend requirements
- [ ] Error handling shows appropriate messages
- [ ] Loading states display correctly
- [ ] Empty states display appropriate messaging

### API Integration Validation
- [ ] Correct API endpoints called
- [ ] Request payloads match backend schemas
- [ ] Response parsing handles all fields correctly
- [ ] Error handling for network/API errors
- [ ] Token injection works (Authorization header)
- [ ] Token refresh works automatically
- [ ] Pagination parameters sent correctly
- [ ] Filter parameters sent correctly
- [ ] Authentication flow integrated correctly

### Performance Validation
- [ ] Initial load time ≤ legacy (target: <2 seconds)
- [ ] List scroll performance smooth (60fps)
- [ ] Image loading optimized with caching
- [ ] API response times acceptable
- [ ] Memory usage reasonable
- [ ] Battery usage acceptable (mobile)

## Phase Dependencies

### Phase 2 Dependencies
- **Design System**: AppTheme, color palette, typography system
- **Core Widgets**: StatCard, PlantCard, StrainCard, SensorCard
- **State Management**: PlantsProvider, StrainsProvider, SensorsProvider, DashboardProvider
- **API Integration**: Plants API, Strains API, Sensors API, Auth API

### Phase 3 Dependencies
- **Enhanced Features**: Settings system, user management, cart system
- **Additional Widgets**: EmptyState, TimelineWidget, FilterBar
- **State Management**: CartProvider, UsersProvider, SettingsProvider
- **Market Integration**: Market API, Product models

### Phase 4 Dependencies
- **Content Management**: Blog system, newsletter integration
- **Social Features**: Social sharing, integration APIs
- **Marketing Pages**: Static content, SEO optimization

## Screen Migration Progress Tracking

### Phase 2 Progress (Target: 6 screens)
- [x] Dashboard Screen (85% design parity, 90% functional parity)
- [ ] Plants Screen (0% complete)
- [ ] Plant Detail Screen (0% complete)
- [ ] Strains Screen (0% complete)
- [ ] Sensors Screen (0% complete)
- [ ] Login Screen Enhancement (0% complete)
- [ ] Sidebar Drawer (0% complete)

### Phase 3 Progress (Target: 8 screens)
- [ ] Settings Screen (0% complete)
- [ ] Admin Users Screen (0% complete)
- [ ] Cart Screen (0% complete)
- [ ] Clones Screens (0% complete)
- [ ] Activities Screen (0% complete)
- [ ] Market Screens (0% complete)
- [ ] User Profile Screen (0% complete)
- [ ] Admin Export Screen (0% complete)

### Phase 4 Progress (Target: 8+ screens)
- [ ] Marketing Screens (0% complete - may remain web-only)
- [ ] Newsletter Screens (0% complete)
- [ ] Blog Screens (0% complete)
- [ ] Social Screens (0% complete)

## Total Progress: 1/22 screens (4.5%)

## Risk Assessment

### High Risk Screens
- **Dashboard Screen**: Complex widget interactions, real-time data updates
- **Plants Screen**: Advanced filtering, grid/list toggle, pagination
- **Settings Screen**: Tabbed interface, complex form validation
- **Admin Users Screen**: Role-based access, bulk operations

### Medium Risk Screens
- **Strains Screen**: Genetics slider, complex form inputs
- **Sensors Screen**: Real-time data, zone organization
- **Cart Screen**: State persistence, checkout flow

### Low Risk Screens
- **Login Screen**: Enhancement of existing functionality
- **Plant Detail Screen**: Standard detail view patterns
- **Market Screens**: Standard CRUD with list/detail views

## Rollback Triggers

### Critical Issues (Immediate Rollback)
- Design parity < 80% for P0 screens
- Functional parity < 90% for P0 screens
- Performance regression > 20%
- Critical bugs affecting core functionality

### Major Issues (Rollback Consideration)
- API integration failures
- Authentication flow broken
- Data loss or corruption
- Major accessibility issues

### Minor Issues (Fix in Place)
- Non-critical UI inconsistencies
- Performance optimizations needed
- Accessibility enhancements needed
- Testing gaps identified

## Success Criteria

### Phase 2 Success (100% Required)
- All P0 screens implemented and validated
- 95%+ design parity achieved
- 95%+ functional parity achieved
- Performance benchmarks met or exceeded
- Zero critical bugs

### Phase 3 Success (100% Required)
- All P1 screens implemented and validated
- 100% feature parity achieved
- All user workflows functional
- Production-ready code quality

### Phase 4 Success (Optional Goals)
- All P2/P3 screens implemented (or backlogged)
- Legacy web UI can be decommissioned
- Complete mobile application ready for launch
