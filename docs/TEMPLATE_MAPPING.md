# CultivAR Flutter Template Widget Mapping

## Table of Contents
1. [Overview](#overview)
2. [Priority Classification](#priority-classification)
3. [Complete Template Mapping](#complete-template-mapping)
   - [Authentication (P0 - Critical)](#authentication-p0---critical)
   - [Core Dashboard (P0 - Critical)](#core-dashboard-p0---critical)
   - [Plant Management (P0 - Critical)](#plant-management-p0---critical)
   - [Strains & Cultivars (P1 - High)](#strains--cultivars-p1---high)
   - [Sensors & Monitoring (P1 - High)](#sensors--monitoring-p1---high)
   - [User Management (P1 - High)](#user-management-p1---high)
   - [Settings & Configuration (P2 - Medium)](#settings--configuration-p2---medium)
   - [Admin Functions (P2 - Medium)](#admin-functions-p2---medium)
   - [Clones & Lineage (P2 - Medium)](#clones--lineage-p2---medium)
   - [Diagnostics & System (P2 - Medium)](#diagnostics--system-p2---medium)
   - [Market & E-commerce (P3 - Low)](#market--e-commerce-p3---low)
   - [Marketing & Social (P3 - Low)](#marketing--social-p3---low)
   - [Newsletter & Communication (P3 - Low)](#newsletter--communication-p3---low)
   - [Error Pages & Utilities (P3 - Low)](#error-pages--utilities-p3---low)
4. [Migration Strategy](#migration-strategy)
5. [Implementation Guidelines](#implementation-guidelines)

## Overview

This comprehensive mapping documents the migration of all 75+ Jinja templates from the CultivAR web application to Flutter widgets. Each template is categorized by priority, complexity, and migration notes to guide the development process.

## Priority Classification

- **P0 (Critical)**: Core user workflows essential for basic app functionality
- **P1 (High)**: Important features that enhance user experience
- **P2 (Medium)**: Nice-to-have features that add value
- **P3 (Low)**: Advanced features and utility pages

### Complexity Levels

- **Simple**: Basic screens with minimal data and interactions
- **Medium**: Moderate complexity with some data relationships
- **Complex**: Advanced features with multiple data sources and complex interactions

## Complete Template Mapping

### Authentication (P0 - Critical)

| Template Path | Flutter Screen/Widget | Complexity | Priority | Key Components | Data Requirements | Migration Notes |
|---|---|---|---|---|---|
| `app/web/templates/views/new_login.html` | `LoginScreen` | medium | P0 | Form with username/password, remember me, forgot password | `/auth/login`, User model | Add biometric auth option for mobile. Support social login. |
| `app/web/templates/signup.html` | `RegisterScreen` | medium | P0 | Registration form, email verification, terms acceptance | `/auth/register`, User model, Email verification | Add mobile-friendly form validation and OTP verification. |
| `app/web/templates/auth/change_password.html` | `ChangePasswordScreen` | simple | P0 | Old password, new password, confirm password fields | `/auth/change-password` | Implement secure password change with validation. |
| `app/web/templates/views/auth_placeholder.html` | `AuthPlaceholderScreen` | simple | P0 | Loading state, retry button | Authentication state | Use during auth flow transitions. |

### Core Dashboard (P0 - Critical)

| Template Path | Flutter Screen/Widget | Complexity | Priority | Key Components | Data Requirements | Migration Notes |
|---|---|---|---|---|---|
| `app/web/templates/views/dashboard.html` | `DashboardScreen` | complex | P0 | Stats cards, activities list, charts, navigation | `/dashboard/stats`, Activity model, User stats | Use fl_chart for visualizations, pull-to-refresh patterns. |
| `app/web/templates/views/dashboard_mobile.html` | `MobileDashboardScreen` | medium | P0 | Compact stats, mobile-optimized layout | `/dashboard/mobile`, Mobile stats | Implement responsive design for smaller screens. |
| `app/web/templates/views/user_dashboard.html` | `UserDashboardScreen` | medium | P0 | Personal stats, recent activity, shortcuts | `/dashboard/user`, User-specific data | Add user profile integration and personalization. |
| `app/web/templates/views/index.html` | `HomeScreen` | medium | P0 | Landing page, quick actions, recent activity | `/home`, Dashboard preview, Quick actions | Main app entry point with personalized content. |

### Plant Management (P0 - Critical)

| Template Path | Flutter Screen/Widget | Complexity | Priority | Key Components | Data Requirements | Migration Notes |
|---|---|---|---|---|---|
| `app/web/templates/views/plants.html` | `PlantsListScreen` | complex | P0 | Plant cards grid/list, filters, search, pagination | `/plants` (paginated), Plant model, Filter options | Infinite scroll, search/filter chips, floating action button. |
| `app/web/templates/views/plant.html` | `PlantDetailScreen` | complex | P0 | Plant information, timeline, photos, actions | `/plants/{id}`, Plant model, Plant history, Photos | Implement image gallery, action buttons (water, feed, etc.). |
| `app/web/templates/views/add_breeder.html` | `AddBreederScreen` | medium | P0 | Breeder creation form, cultivar selection | `/breeders/create`, Breeder model, Cultivar list | Mobile-friendly form with image upload capabilities. |
| `app/web/templates/views/add_strain.html` | `AddStrainScreen` | medium | P0 | Strain creation form, genetics input | `/strains/create`, Strain model, Genetics data | Form with complex genetics field validation. |

### Strains & Cultivars (P1 - High)

| Template Path | Flutter Screen/Widget | Complexity | Priority | Key Components | Data Requirements | Migration Notes |
|---|---|---|---|---|---|
| `app/web/templates/views/strains.html` | `StrainsListScreen` | medium | P1 | Strain cards, categories, search, filters | `/strains`, Strain model, Categories | Grid/list toggle, filter chips, favorite functionality. |
| `app/web/templates/views/strain.html` | `StrainDetailScreen` | complex | P1 | Strain info, genetics, growing notes, related strains | `/strains/{id}`, Strain model, Genetics data | Implement tabbed interface for different information sections. |
| `app/web/templates/views/market_seed_bank.html` | `SeedBankScreen` | medium | P1 | Available seeds, shopping cart, purchase flow | `/market/seeds`, Seed model, Pricing | Add cart functionality and purchase workflow integration. |

### Sensors & Monitoring (P1 - High)

| Template Path | Flutter Screen/Widget | Complexity | Priority | Key Components | Data Requirements | Migration Notes |
|---|---|---|---|---|---|
| `app/web/templates/views/sensors.html` | `SensorsListScreen` | medium | P1 | Sensor cards, status indicators, data readings | `/sensors`, Sensor model, Real-time data | Real-time data updates, status indicators with color coding. |
| `app/web/templates/views/sensors_standalone.html` | `SensorsStandaloneScreen` | medium | P1 | Full sensor detail, graphs, historical data | `/sensors/{id}`, Sensor data, Historical readings | Implement line charts for data visualization with time range selection. |
| `app/web/templates/views/sensors_tab_standalone.html` | `SensorTabScreen` | simple | P1 | Tab-based sensor detail view | `/sensors/tab/{id}`, Tab-specific data | Use TabBar for different sensor metrics. |
| `app/web/templates/views/graph.html` | `SensorGraphScreen` | medium | P1 | Interactive graphs, data export, time range selection | `/graphs`, Sensor data, Chart configurations | Implement interactive charts with zoom and pan capabilities. |
| `app/web/templates/views/sensors_minimal.html` | `SensorsMinimalScreen` | simple | P1 | Basic sensor overview, status only | `/sensors/minimal`, Basic sensor data | Lightweight sensor status display for dashboard integration. |
| `app/web/templates/views/sensors_tab_content_fixed.html` | `SensorTabContentFixedWidget` | simple | P1 | Fixed sensor tab content | `/sensors/tab/fixed`, Static sensor data | Reusable widget for consistent sensor tab layouts. |
| `app/web/templates/views/sensors_tab_content.html` | `SensorTabContentWidget` | medium | P1 | Dynamic sensor tab content | `/sensors/tab/dynamic`, Dynamic sensor data | Flexible widget for various sensor content types. |
| `app/web/templates/views/sensors_tab_fixed.html` | `SensorTabFixedScreen` | simple | P1 | Fixed sensor tab layout | `/sensors/tab/fixed`, Fixed sensor data | Consistent layout for sensor tab interfaces. |
| `app/web/templates/views/sensors_tab_simple.html` | `SensorTabSimpleScreen` | simple | P1 | Simplified sensor tab view | `/sensors/tab/simple`, Basic sensor data | Minimal sensor interface for quick access. |

### User Management (P1 - High)

| Template Path | Flutter Screen/Widget | Complexity | Priority | Key Components | Data Requirements | Migration Notes |
|---|---|---|---|---|---|
| `app/web/templates/views/admin_users.html` | `AdminUsersScreen` | medium | P1 | User list, search, filters, actions | `/admin/users`, User model, Roles | Table view with inline actions, bulk operations. |
| `app/web/templates/admin/users.html` | `AdminUsersManagementScreen` | complex | P1 | User management, role assignment, permissions | `/admin/users/manage`, User roles, Permissions | Implement role-based access control UI. |
| `app/web/templates/admin/create_user.html` | `CreateUserScreen` | medium | P1 | User creation form, role selection | `/admin/users/create`, User model, Roles | Form with validation and role assignment interface. |
| `app/web/templates/admin/edit_user.html` | `EditUserScreen` | medium | P1 | User edit form, profile updates | `/admin/users/{id}/edit`, User model | Pre-populated form with update capabilities. |

### Settings & Configuration (P2 - Medium)

| Template Path | Flutter Screen/Widget | Complexity | Priority | Key Components | Data Requirements | Migration Notes |
|---|---|---|---|---|---|
| `app/web/templates/views/settings.html` | `SettingsScreen` | medium | P2 | Settings sections, toggles, preferences | `/settings`, User preferences | Organize in expandable sections with clear categorization. |
| `app/web/templates/views/settings_functional.html` | `SettingsFunctionalScreen` | medium | P2 | Functional settings, API keys, integrations | `/settings/functional`, API configurations | Secure handling of sensitive configuration data. |
| `app/web/templates/views/settings_standalone.html` | `SettingsStandaloneScreen` | medium | P2 | Standalone settings view | `/settings/standalone`, Independent settings | Standalone navigation for specific settings categories. |
| `app/web/templates/views/settings_page.html` | `SettingsPageScreen` | simple | P2 | Simple settings page | `/settings/page`, Basic preferences | Minimal settings interface for specific use cases. |
| `app/web/templates/views/settings_backup.html` | `SettingsBackupScreen` | medium | P2 | Data backup/restore, export options | `/settings/backup`, Data export/import | Implement secure data export and import functionality. |
| `app/web/templates/views/settings_old.html` | `SettingsLegacyScreen` | simple | P2 | Legacy settings compatibility | `/settings/old`, Legacy data | Temporary compatibility layer during migration. |
| `app/web/templates/views/settings_absolute.html` | `SettingsAbsoluteScreen` | medium | P2 | Absolute positioning settings | `/settings/absolute`, Absolute settings | Specialized settings with absolute positioning requirements. |
| `app/web/templates/views/settings_external.html` | `SettingsExternalScreen` | medium | P2 | External service settings | `/settings/external`, External configurations | Integration settings for third-party services. |
| `app/web/templates/views/settings_global.html` | `SettingsGlobalScreen` | complex | P2 | Global system settings | `/settings/global`, System-wide settings | Admin-level global configuration interface. |
| `app/web/templates/views/settings_no_users.html` | `SettingsNoUsersScreen` | simple | P2 | Settings without user context | `/settings/no-users`, Anonymous settings | Settings available without user authentication. |
| `app/web/templates/views/settings_scripts.html` | `SettingsScriptsScreen` | medium | P2 | Script management settings | `/settings/scripts`, Script configurations | Advanced settings for script execution and management. |
| `app/web/templates/views/settings_standalone_fixed.html` | `SettingsStandaloneFixedScreen` | medium | P2 | Fixed standalone settings | `/settings/fixed`, Fixed settings | Immutable settings configuration interface. |
| `app/web/templates/views/settings_standalone_fixed2.html` | `SettingsStandaloneFixed2Screen` | medium | P2 | Alternative fixed settings | `/settings/fixed2`, Alternative fixed settings | Secondary fixed settings interface. |
| `app/web/templates/views/settings_standalone_local.html` | `SettingsStandaloneLocalScreen` | medium | P2 | Local device settings | `/settings/local`, Local configurations | Device-specific settings and preferences. |
| `app/web/templates/views/settings_standalone_new.html` | `SettingsStandaloneNewScreen` | medium | P2 | New standalone settings | `/settings/new`, New settings | Latest settings interface with new features. |

### Admin Functions (P2 - Medium)

| Template Path | Flutter Screen/Widget | Complexity | Priority | Key Components | Data Requirements | Migration Notes |
|---|---|---|---|---|---|
| `app/web/templates/views/admin_dashboard.html` | `AdminDashboardScreen` | complex | P2 | Admin overview, system stats, management tools | `/admin/dashboard`, System metrics, Admin data | Admin-specific dashboard with elevated privileges. |
| `app/web/templates/views/simple_admin_dashboard.html` | `SimpleAdminDashboardScreen` | medium | P2 | Simplified admin view | `/admin/simple`, Basic admin metrics | Lightweight admin interface for quick overview. |
| `app/web/templates/admin/export.html` | `ExportScreen` | medium | P2 | Data export options, format selection | `/admin/export`, Export configurations | Support multiple export formats (CSV, JSON, PDF). |
| `app/web/templates/views/admin_test.html` | `AdminTestScreen` | medium | P2 | Testing tools, debug features | `/admin/test`, Test data, Debug information | Development and testing utilities for admin users. |

### Clones & Lineage (P2 - Medium)

| Template Path | Flutter Screen/Widget | Complexity | Priority | Key Components | Data Requirements | Migration Notes |
|---|---|---|---|---|---|
| `app/web/templates/clones/dashboard.html` | `ClonesDashboardScreen` | medium | P2 | Clone overview, stats, quick actions | `/clones/dashboard`, Clone model, Statistics | Quick action buttons for common clone operations. |
| `app/web/templates/clones/create.html` | `CreateCloneScreen` | medium | P2 | Clone creation form, parent selection | `/clones/create`, Clone model, Parent plants | Form with parent plant selection and clone parameters. |
| `app/web/templates/clones/lineage.html` | `CloneLineageScreen` | complex | P2 | Family tree, genealogy, inheritance tracking | `/clones/lineage`, Clone relationships, Genealogy | Interactive family tree visualization with relationship mapping. |

### Diagnostics & System (P2 - Medium)

| Template Path | Flutter Screen/Widget | Complexity | Priority | Key Components | Data Requirements | Migration Notes |
|---|---|---|---|---|---|
| `app/web/templates/views/diagnostics.html` | `DiagnosticsScreen` | complex | P2 | System diagnostics, health checks, logs | `/diagnostics`, System metrics, Health data | Admin tool for system monitoring and troubleshooting. |

### Market & E-commerce (P3 - Low)

| Template Path | Flutter Screen/Widget | Complexity | Priority | Key Components | Data Requirements | Migration Notes |
|---|---|---|---|---|---|
| `app/web/templates/views/market/seed_bank.html` | `MarketSeedBankScreen` | medium | P3 | Seed catalog, shopping features | `/market/seeds`, Product catalog, Cart | E-commerce functionality with cart integration. |
| `app/web/templates/views/market/extensions.html` | `MarketExtensionsScreen` | medium | P3 | Extensions, plugins, add-ons | `/market/extensions`, Extension catalog | Marketplace for additional features. |
| `app/web/templates/views/market/gear.html` | `MarketGearScreen` | medium | P3 | Equipment catalog, reviews | `/market/gear`, Equipment catalog, Reviews | Equipment marketplace with review system. |
| `app/web/templates/views/cart.html` | `CartScreen` | medium | P1 | Shopping cart, checkout, payment | `/cart`, Cart items, Payment processing | Mobile-optimized cart with swipe-to-remove functionality. |

### Marketing & Social (P3 - Low)

| Template Path | Flutter Screen/Widget | Complexity | Priority | Key Components | Data Requirements | Migration Notes |
|---|---|---|---|---|---|
| `app/web/templates/landing/index.html` | `LandingScreen` | simple | P3 | Hero section, features, call-to-action | Static content, Marketing data | Static marketing screen, potentially for web version. |
| `app/web/templates/marketing/blog.html` | `BlogScreen` | medium | P3 | Blog list, articles, categories | `/blog`, Blog posts, Categories | Implement article reading with markdown support. |
| `app/web/templates/marketing/blog_post.html` | `BlogPostScreen` | medium | P3 | Individual blog post, comments, sharing | `/blog/{id}`, Blog post, Comments | Rich text display with comment system integration. |
| `app/web/templates/marketing/waitlist.html` | `WaitlistScreen` | simple | P3 | Email signup, form validation | `/waitlist`, Email collection | Simple email collection form with validation. |
| `app/web/templates/marketing/waitlist_success.html` | `WaitlistSuccessScreen` | simple | P3 | Success message, next steps | Static confirmation | Confirmation screen with additional information. |
| `app/web/templates/marketing/home.html` | `MarketingHomeScreen` | medium | P3 | Marketing homepage, features showcase | Marketing content, Features list | Feature showcase with smooth animations and call-to-actions. |
| `app/web/templates/marketing/_nav.html` | `MarketingNavigationWidget` | simple | P3 | Navigation header, logo, menu | Navigation items | Reusable navigation component for marketing screens. |
| `app/web/templates/social/share.html` | `ShareScreen` | medium | P3 | Share options, social media integration | `/share`, Share configurations | Native sharing capabilities with social media integration. |
| `app/web/templates/social/share_blog.html` | `ShareBlogScreen` | simple | P3 | Blog post sharing | Blog sharing data | Blog-specific sharing interface. |
| `app/web/templates/social/follow.html` | `FollowScreen` | simple | P3 | Follow buttons, social profiles | Social media data | Social media follow functionality. |
| `app/web/templates/social/widgets/share_buttons.html` | `ShareButtonsWidget` | simple | P3 | Share button components | Share configurations | Reusable share button components. |
| `app/web/templates/social/widgets/follow_buttons.html` | `FollowButtonsWidget` | simple | P3 | Follow button components | Social media profiles | Reusable follow button components. |
| `app/web/templates/social/embed.html` | `SocialEmbedScreen` | simple | P3 | Embed code, iframe content | Embed data | Content embedding functionality. |

### Newsletter & Communication (P3 - Low)

| Template Path | Flutter Screen/Widget | Complexity | Priority | Key Components | Data Requirements | Migration Notes |
|---|---|---|---|---|---|
| `app/web/templates/newsletter/subscribe.html` | `NewsletterSubscribeScreen` | simple | P3 | Email subscription form | `/newsletter/subscribe`, Email validation | Simple subscription form with email validation. |
| `app/web/templates/newsletter/unsubscribe.html` | `NewsletterUnsubscribeScreen` | simple | P3 | Unsubscribe confirmation | `/newsletter/unsubscribe`, Email verification | Confirmation flow for unsubscribing. |
| `app/web/templates/newsletter/preferences.html` | `NewsletterPreferencesScreen` | medium | P3 | Newsletter preferences, frequency settings | `/newsletter/preferences`, User preferences | Preference management interface with toggles. |
| `app/web/templates/newsletter/success.html` | `NewsletterSuccessScreen` | simple | P3 | Success confirmation | Static confirmation | Generic success screen for newsletter actions. |
| `app/web/templates/newsletter/500.html` | `NewsletterErrorScreen` | simple | P3 | Error message display | Error data | Error handling for newsletter operations. |
| `app/web/templates/newsletter/404.html` | `NewsletterNotFoundScreen` | simple | P3 | Not found message | Static error | 404 page for newsletter-related URLs. |

### Error Pages & Utilities (P3 - Low)

| Template Path | Flutter Screen/Widget | Complexity | Priority | Key Components | Data Requirements | Migration Notes |
|---|---|---|---|---|---|
| `app/web/templates/social/500.html` | `SocialErrorScreen` | simple | P3 | 500 error page for social features | Error data | Consistent error page design across the app. |
| `app/web/templates/social/404.html` | `SocialNotFoundScreen` | simple | P3 | 404 error page for social features | Static error | 404 page for social-related URLs. |
| `app/web/templates/common/sidebar.html` | `SidebarWidget` | simple | P3 | Navigation sidebar | Navigation items | Reusable sidebar component for navigation. |
| `app/web/templates/common/base.html` | `BaseScreen` | simple | P3 | Base layout template | Layout configuration | Base screen template for consistent layouts. |
| `app/web/templates/common/admin_base.html` | `AdminBaseScreen` | simple | P3 | Admin layout template | Admin navigation, Layout | Base template for admin-specific screens. |
| `app/web/templates/views/placeholder.html` | `PlaceholderScreen` | simple | P3 | Placeholder content, loading states | Static content | Temporary screen for unimplemented features. |
| `app/web/templates/views/test.html` | `TestScreen` | simple | P3 | Testing interface, debug tools | Test data, Debug information | Development testing interface for QA purposes. |

## Migration Strategy

### Phase 1: Core Functionality (P0 - Critical)
**Priority Order:**
1. Authentication flow (`LoginScreen`, `RegisterScreen`)
2. Main dashboard (`DashboardScreen`) 
3. Plant management (`PlantsListScreen`, `PlantDetailScreen`)
4. User authentication and session management

**Key Success Metrics:**
- Complete auth flow working end-to-end
- Dashboard displays real data from API
- Basic plant CRUD operations functional
- 80% test coverage on core features

### Phase 2: Enhanced Features (P1 - High)
**Priority Order:**
1. Strains and cultivars management
2. Sensor monitoring and visualization
3. User management and admin functions
4. Advanced plant management features

**Key Success Metrics:**
- All major user workflows completed
- Real-time data updates working
- Admin functions properly gated
- Performance optimized for mobile

### Phase 3: Advanced Features (P2 - Medium)
**Priority Order:**
1. Settings and preferences
2. Clone and lineage tracking
3. Advanced admin functions
4. Data export and backup

**Key Success Metrics:**
- All advanced features implemented
- Settings persistence working
- Data export/import functional
- Comprehensive error handling

### Phase 4: Polish & Enhancement (P3 - Low)
**Priority Order:**
1. Marketing and social features
2. Newsletter integration
3. E-commerce capabilities
4. Error pages and utilities

**Key Success Metrics:**
- Complete feature parity with web version
- Smooth user experience across all features
- Comprehensive error handling
- Performance optimized

## Implementation Guidelines

### Data Integration
- **API Compatibility**: Ensure all Flutter screens can consume existing FastAPI endpoints
- **Model Mapping**: Use Freezed models to map backend schemas
- **Error Handling**: Implement proper error states for all async operations
- **Loading States**: Show appropriate loading indicators during data fetching

### UI/UX Considerations
- **Mobile-First Design**: Optimize all interfaces for mobile usage patterns
- **Glass Morphism**: Maintain visual consistency with web design using GlassCard components
- **Navigation**: Implement intuitive navigation patterns with bottom navigation or drawer
- **Form Handling**: Use mobile-friendly form inputs and validation

### State Management
- **Riverpod Providers**: Use Riverpod for all state management
- **AsyncValue Handling**: Properly handle loading, error, and data states
- **Caching**: Implement appropriate caching strategies for performance
- **Real-time Updates**: Use WebSocket or polling for real-time data

### Testing Strategy
- **Widget Tests**: Test all custom widgets and screens
- **Integration Tests**: Test complete user workflows
- **API Tests**: Mock API calls for reliable testing
- **Performance Tests**: Ensure smooth performance on mobile devices

This comprehensive mapping ensures systematic migration of all 75+ web templates to Flutter while maintaining functionality and user experience standards.
