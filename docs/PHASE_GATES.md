# Phase Gates & Acceptance Criteria

## Overview

This document defines detailed phase gate definitions with acceptance criteria for the Flutter migration project. Each phase has specific validation gates that must be passed before proceeding to the next phase, ensuring quality and preventing scope drift.

## Phase 1 Gate - Foundation Complete

### Timeline: Weeks 1-2
### Acceptance Criteria: 100% Required

#### Design System Foundation
- [ ] **AppTheme Implementation**: Complete Flutter theme with exact color parity from CSS
  - All primary colors (50-900 scale) mapped
  - Surface colors (primary, secondary, tertiary, glass effects)
  - Text colors (primary, secondary, tertiary, inverse)
  - Status colors (success, warning, error, info, plant statuses)
  - Typography system (font families, weights, responsive sizes)
  - Spacing system (gaps, padding, margins)
  - Shadow system (xs, sm, md, lg, xl, 2xl)
  - Border radius system (none, sm, md, lg, xl, 2xl, full)
  - Animation durations (fast, normal, slow, slower)
  - Glass morphism effects with backdrop blur

- [ ] **Component Equivalence Matrix**: All HTML/Bootstrap components mapped to Flutter widgets
  - Cards → Card/Container with BoxDecoration
  - Modals → showDialog/showModalBottomSheet
  - Buttons → ElevatedButton/OutlinedButton/TextButton
  - Forms → TextFormField/DropdownButtonFormField
  - Navigation → Drawer/AppBar/BottomNavigationBar
  - Alerts → SnackBar/AlertDialog
  - Badges → Chip/Container with decoration

- [ ] **Theme Toggle System**: Complete light/dark theme implementation
  - Theme toggle button matching legacy design
  - SharedPreferences persistence
  - Automatic theme detection
  - Consistent color adaptation across all components

#### Core Widget Library
- [ ] **GlassCard Widget**: Replica of legacy glass morphism cards
  - BackdropFilter blur(16px)
  - Semi-transparent background
  - Border with glass-border colors
  - Shadow matching CSS tokens
  - Hover effects and animations
  - Responsive padding

- [ ] **StatCard Widget**: Dashboard statistics cards
  - Circular icon container with gradient
  - Large number display (2.5rem, 700 weight)
  - Label text (0.9rem, uppercase, letter-spacing)
  - Hover animations
  - Status-specific styling

- [ ] **FilterBar Widget**: Filter controls matching legacy
  - Horizontal flex layout
  - Filter groups with labels
  - Responsive stacking on mobile
  - Real-time filter callbacks

- [ ] **PlantCard Widget**: Plant display cards
  - Image container (200px height)
  - Status badge overlay
  - Plant name and metadata display
  - Action buttons footer
  - Hover animations
  - Status color mapping

- [ ] **CultivarCard Widget**: Cultivar display cards
  - Cultivar name header
  - Type badges (Indica/Sativa/Hybrid/Autoflower)
  - Genetics display
  - Description preview
  - Action buttons

- [ ] **SensorCard Widget**: Sensor display cards
  - Sensor name and value
  - Status indicators
  - Last updated timestamp
  - Action buttons

- [ ] **TimelineWidget**: Activity timeline
  - Vertical timeline with left border
  - Date labels and descriptions
  - Type-specific colors
  - Scrollable container

- [ ] **EmptyState Widget**: Empty state display
  - Centered icon container
  - Heading and description
  - Action button
  - Variants for different contexts

- [ ] **ThemeToggleButton Widget**: Theme switching
  - Toggle switch appearance
  - Animated sliding indicator

#### State Management Architecture
- [ ] **ThemeProvider**: Riverpod provider for theme management
- [ ] **AuthProvider**: Riverpod provider for authentication state
- [ ] **PlantsProvider**: Riverpod provider for plant management
- [ ] **CultivarsProvider**: Riverpod provider for cultivar management
- [ ] **SensorsProvider**: Riverpod provider for sensor management
- [ ] **DashboardProvider**: Riverpod provider for dashboard state
- [ ] **CartProvider**: Riverpod provider for shopping cart

#### API Integration
- [ ] **ApiClient Enhancement**: All FastAPI endpoints implemented
  - Cultivars endpoints (CRUD, stats, pagination)
  - Sensors endpoints (CRUD, readings, stats)
  - Activities endpoints (CRUD, types, stats)
  - Users endpoints (profile, management, stats)
  - Clones endpoints (CRUD, parents, stats)
  - Breeders endpoints (CRUD, stats)
  - Market endpoints (products, cart)
  - Token refresh interceptor

#### Data Models
- [ ] **Cultivar Models**: Complete cultivar data models
- [ ] **Sensor Models**: Complete sensor data models
- [ ] **Activity Models**: Complete activity data models
- [ ] **Breeder Models**: Complete breeder data models
- [ ] **Clone Models**: Complete clone data models

#### Routing & Navigation
- [ ] **AppRouter**: Complete routing with go_router
- [ ] **Route Guards**: Authentication-based navigation
- [ ] **Deep Linking**: Mobile app deep link support
- [ ] **Transition Animations**: Page transitions matching legacy

#### Dependencies & Configuration
- [ ] **pubspec.yaml**: All required dependencies added
- [ ] **App Constants**: Configuration constants defined
- [ ] **Storage Service**: Unified storage service
- [ ] **Analytics Service**: Analytics tracking setup
- [ ] **Analysis Options**: Enhanced linting configuration

#### Testing Infrastructure
- [ ] **Widget Test Suite**: Core widget tests
- [ ] **Golden Test Setup**: Visual regression testing
- [ ] **Integration Test Framework**: End-to-end testing setup

### Validation & Quality Gates
- [ ] **Code Quality**: `flutter analyze` → 0 errors, 0 warnings
- [ ] **Widget Tests**: All widget tests pass
- [ ] **Visual Comparison**: Widgets match legacy design (95%+ parity)
- [ ] **Code Review**: 2+ team members approve
- [ ] **Design Review**: UI/UX approval

### Deliverables
- Foundation code complete
- Widget library with 9 core widgets
- State management architecture
- API integration layer
- Data models
- Testing infrastructure
- Documentation

### Rollback Procedure
N/A (no production impact)

---

## Phase 2 Gate - Core Screens Complete

### Timeline: Weeks 3-5
### Acceptance Criteria: 100% Required

#### Screen Implementation
- [ ] **DashboardScreen**: Full implementation matching legacy
- [ ] **PlantsScreen**: Full implementation with CRUD operations
- [ ] **PlantDetailScreen**: Complete plant detail view
- [ ] **CultivarsScreen**: Full cultivar management interface
- [ ] **SensorsScreen**: Complete sensor monitoring interface
- [ ] **Login Enhancement**: Improved authentication flow
- [ ] **Sidebar Drawer**: Navigation drawer with glass morphism

#### Validation & Quality Gates
- [ ] **Golden Tests**: All core screens pass visual regression tests
- [ ] **Integration Tests**: All CRUD operations tested end-to-end
- [ ] **Performance Tests**: Load time < 2s, scroll 60fps
- [ ] **API Integration**: All endpoints verified working
- [ ] **User Acceptance Testing**: 5+ beta users approve

### Deliverables
- Core screens with 100% functionality
- Integration test suite
- Performance benchmarks
- Beta build ready

### Rollback Procedure
Disable Flutter routes, redirect to legacy web

---

## Phase 3 Gate - Extended Features Complete

### Timeline: Weeks 6-7
### Acceptance Criteria: 100% Required

#### Additional Screens
- [ ] **SettingsScreen**: Complete settings interface
- [ ] **AdminUsersScreen**: User management interface
- [ ] **CartScreen**: Shopping cart functionality
- [ ] **Clone Screens**: Clone management
- [ ] **ActivitiesScreen**: Activity management
- [ ] **Market Screens**: Product browsing
- [ ] **UserProfileScreen**: Profile management

#### Validation & Quality Gates
- [ ] **Feature Parity**: 100% feature parity achieved
- [ ] **Performance**: Maintain performance standards
- [ ] **Security**: Admin features properly secured
- [ ] **Production Ready**: Code quality meets production standards

### Deliverables
- Complete application
- Full feature parity
- Production build

### Rollback Procedure
Feature flags to disable specific screens

---

## Phase 4 Gate - Production Ready

### Timeline: Weeks 8-9
### Acceptance Criteria: 100% Required

#### Final Validation
- [ ] **All Validation Checklists Complete**
- [ ] **Performance Benchmarks Pass**
- [ ] **Security Audit Complete**
- [ ] **Accessibility Audit Complete**
- [ ] **User Acceptance Testing (20+ users)**
- [ ] **App Store Submissions Approved**
- [ ] **Production Deployment Tested**
- [ ] **Monitoring Configured**

#### Success Criteria
- [ ] **100% Test Coverage** for critical paths
- [ ] **0 Critical Bugs**, <5 Minor Bugs
- [ ] **Performance ≥ Legacy**
- [ ] **User Satisfaction ≥90%**
- [ ] **App Store Rating ≥4.5 stars**

### Deliverables
- Production app
- Monitoring dashboards
- Support documentation
- Migration complete

### Rollback Procedure
Full rollback to legacy web with user communication

## Decision Matrix for Rollback

### Immediate Rollback (Critical Issues)
- Design parity < 80% for P0 screens
- Functional parity < 90% for P0 screens
- Performance regression > 20%
- Critical bugs affecting core functionality

### Rollback Consideration (Major Issues)
- API integration failures
- Authentication flow broken
- Data loss or corruption
- Major accessibility issues

### Fix in Place (Minor Issues)
- Non-critical UI inconsistencies
- Performance optimizations needed
- Accessibility enhancements needed
- Testing gaps identified

## Communication Plan

### User Notifications
- Phase gates
