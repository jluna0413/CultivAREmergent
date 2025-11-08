# API Parity Analysis

This document outlines the legacy Flask endpoints and tracks their migration status to the new FastAPI implementation.

## Domain: Admin (`/admin`)

| Method | Legacy Flask Route                      | FastAPI Target (`/api/v1/admin`)        | Pydantic Schema                  | Status      | Notes                               |
|--------|-----------------------------------------|-----------------------------------------|----------------------------------|-------------|-------------------------------------|
| GET    | `/`                                     | `/` (Redirect)                          |                                  | Done        | Redirects to `/admin/users`         |
| GET    | `/users`                                | `/users`                                |                                  | Done        | HTML view                             |
| GET/POST| `/users/create`                         | `/users` (POST)                         | `UserCreate`                     | Done        | API endpoint for creation           |
| GET/POST| `/users/<int:user_id>/edit`             | `/users/<int:user_id>` (PUT)            | `UserUpdate`                     | Done        | API endpoint for updates            |
| POST   | `/users/<int:user_id>/delete`           | `/users/<int:user_id>` (DELETE)         |                                  | Done        | API endpoint for deletion           |
| POST   | `/users/bulk-delete`                    | `/users/bulk-delete`                    | `AdminUserBulkDeleteRequest`     | Done        |                                     |
| POST   | `/users/<int:user_id>/toggle-admin`     | `/users/<int:user_id>/toggle-admin`     |                                  | Done        |                                     |
| POST   | `/users/<int:user_id>/force-password-reset` | `/users/<int:user_id>/force-password-reset` |                                  | Done        |                                     |
| GET    | `/export`                               | `/export`                               |                                  | To Do       | HTML view - Not implemented         |
| GET    | `/export/plants/<format>`               | `/export/plants/{format}`               |                                  | To Do       | Not implemented                     |
| GET    | `/export/cultivars/<format>`            | `/export/cultivars/{format}`            |                                  | To Do       | Not implemented                     |
| GET    | `/export/activities`                    | `/export/activities`                    |                                  | To Do       | Not implemented                     |
| GET    | `/export/users`                         | `/export/users`                         |                                  | To Do       | Not implemented                     |
| GET    | `/export/sensors`                       | `/export/sensors`                       |                                  | To Do       | Not implemented                     |
| GET    | `/export/complete`                      | `/export/complete`                      |                                  | To Do       | Not implemented                     |
| GET    | `/api/users`                            | `/users`                                | `List[UserResponse]`             | Done        | API endpoint for listing users      |
| GET    | `/api/users/<int:user_id>`              | `/users/<int:user_id>`                  | `UserResponse`                   | Done        | API endpoint for getting a user     |
| GET    | `/api/users/stats`                      | `/users/stats`                          | `AdminStats`                     | Done        |                                     |
| GET    | `/api/export/stats`                     | `/export/stats`                         |                                  | To Do       | Not implemented                     |
| GET    | `/api/system/logs`                      | `/system/logs`                          | `List[LogEntry]`                 | Done        |                                     |
| GET    | `/api/system/info`                      | `/system/info`                          | `SystemInfo`                     | Done        |                                     |
| GET    | `/api/diagnostics/test`                 | `/diagnostics/test`                     |                                  | To Do       | Not implemented                     |

## Domain: Auth (`/auth`)

| Method | Legacy Flask Route  | FastAPI Target (`/api/v1/auth`) | Pydantic Schema  | Status | Notes           |
|--------|---------------------|---------------------------------|------------------|--------|-----------------|
| GET/POST| `/login`            | `/token`                        | `LoginRequest`   | Done   | OAuth2 password flow |
| GET/POST| `/signup`           | `/register`                     | `RegisterRequest`| Done   |                 |
| GET    | `/logout`           | `/logout`                       |                  | Done   |                 |
| GET/POST| `/forgot-password`  | `/forgot-password`              |                  | To Do  | Not implemented |

## Domain: Blog (`/blog`)

| Method | Legacy Flask Route | FastAPI Target (`/api/v1/blog`) | Pydantic Schema    | Status | Notes |
|--------|--------------------|---------------------------------|--------------------|--------|-------|
| GET    | ``                 | `/`                             | `PostListResponse` | Done   |       |
| GET    | `/<slug>`          | `/{slug}`                       | `PostResponse`     | Done   |       |
| GET    | `/search`          | `/search`                       | `PostListResponse` | Done   |       |

## Domain: Breeders

| Method | Legacy Flask Route        | FastAPI Target (`/api/v1/breeders`) | Pydantic Schema      | Status | Notes |
|--------|---------------------------|-------------------------------------|----------------------|--------|-------|
| GET    | `/`                       | `/`                                 | `BreederListResponse`| Done   |       |
| GET    | `/breeders`               | `/`                                 | `BreederListResponse`| Done   |       |
| GET    | `/add`                    | `/add` (View)                       |                      | Done   |       |
| POST   | `/breeders/add`           | `/`                                 | `BreederCreate`      | Done   |       |
| GET    | `/<int:breeder_id>`       | `/{breeder_id}`                     | `BreederResponse`    | Done   |       |
| GET/POST| `/<int:breeder_id>/edit`  | `/{breeder_id}` (PUT)               | `BreederUpdate`      | Done   |       |
| POST   | `/<int:breeder_id>/update`| `/{breeder_id}` (PUT)               | `BreederUpdate`      | Done   |       |
| POST   | `/<int:breeder_id>/delete`| `/{breeder_id}` (DELETE)            |                      | Done   |       |

## Domain: Clones (`/clones`)

| Method | Legacy Flask Route          | FastAPI Target (`/api/v1/clones`) | Pydantic Schema   | Status | Notes |
|--------|-----------------------------|-----------------------------------|-------------------|--------|-------|
| GET    | `/`                         | `/`                               | `CloneListResponse` | Done   |       |
| GET/POST| `/create`                   | `/` (POST)                        | `CloneCreate`     | Done   |       |
| GET    | `/<int:clone_id>/lineage`   | `/{clone_id}/lineage`             |                   | To Do  | Not implemented |
| POST   | `/<int:clone_id>/delete`    | `/{clone_id}` (DELETE)            |                   | Done   |       |
| GET    | `/api/stats`                | `/stats`                          |                   | To Do  | Not implemented |
| GET    | `/api/parents`              | `/parents`                        |                   | To Do  | Not implemented |
| GET    | `/api`                      | `/`                               | `CloneListResponse` | Done   |       |
| GET    | `/api/<int:clone_id>/lineage`| `/{clone_id}/lineage`             |                   | To Do  | Not implemented |

## Domain: Cultivars

| Method | Legacy Flask Route      | FastAPI Target (`/api/v1/cultivars`) | Pydantic Schema      | Status | Notes |
|--------|-------------------------|--------------------------------------|----------------------|--------|-------|
| GET    | `/`                     | `/`                                  | `CultivarListResponse` | Done   |       |
| GET    | `/cultivars`            | `/`                                  | `CultivarListResponse` | Done   |       |
| GET    | `/<int:cultivar_id>`    | `/{cultivar_id}`                     | `CultivarResponse`   | Done   |       |
| GET    | `/add`                  | `/add` (View)                        |                      | Done   |       |
| GET    | `/cultivars/add`        | `/add` (View)                        |                      | Done   |       |
| GET    | `/strains`              | `/`                                  | `CultivarListResponse` | Done   |       |
| GET    | `/strains/<int:strain_id>`| `/{strain_id}`                       | `CultivarResponse`   | Done   |       |
| GET    | `/strains/add`          | `/add` (View)                        |                      | Done   |       |

## Domain: Dashboard (`/dashboard`)

| Method | Legacy Flask Route     | FastAPI Target (`/api/v1/dashboard`) | Pydantic Schema  | Status | Notes |
|--------|------------------------|--------------------------------------|------------------|--------|-------|
| GET    | `/`                    | `/`                                  | `DashboardStats` | Done   |       |
| GET    | `/plants`              | `/plants`                            |                  | Done   |       |
| GET    | `/plant/<int:plant_id>`| `/plant/{plant_id}`                  |                  | Done   |       |
| GET    | `/sensors`             | `/sensors`                           |                  | Done   |       |

## Domain: Diagnostics (`/diagnostics`)

| Method | Legacy Flask Route    | FastAPI Target (`/api/v1/diagnostics`) | Pydantic Schema            | Status | Notes |
|--------|-----------------------|----------------------------------------|----------------------------|--------|-------|
| GET    | `/`                   | `/`                                    |                            | Done   |       |
| GET    | `/dashboard`          | `/dashboard`                           |                            | Done   |       |
| GET    | `/api/health`         | `/health`                              | `SystemHealth`             | Done   |       |
| GET    | `/api/database`       | `/database`                            | `DatabaseHealth`           | Done   |       |
| GET    | `/api/users`          | `/users`                               | `UserActivitySummary`      | Done   |       |
| GET    | `/api/plants`         | `/plants`                              | `PlantHealthDiagnostics`   | Done   |       |
| GET    | `/api/sensors`        | `/sensors`                             | `SensorDiagnostics`        | Done   |       |
| GET    | `/api/performance`    | `/performance`                         | `AppPerformanceMetrics`    | Done   |       |
| GET    | `/api/errors`         | `/errors`                              | `ErrorLogAnalysis`         | Done   |       |
| GET    | `/api/comprehensive`  | `/comprehensive`                       | `ComprehensiveDiagnostics` | Done   |       |
| GET    | `/status`             | `/status`                              |                            | Done   |       |
| GET    | `/api/realtime`       | `/realtime`                            |                            | Done   |       |
| GET    | `/health`             | `/health`                              |                            | Done   |       |
| GET    | `/api/system-info`    | `/system-info`                         |                            | Done   |       |

## Domain: Marketing (`/marketing`)

| Method | Legacy Flask Route        | FastAPI Target (`/api/v1/marketing`) | Pydantic Schema         | Status | Notes |
|--------|---------------------------|--------------------------------------|-------------------------|--------|-------|
| GET/POST| `/waitlist`               | `/waitlist`                          | `WaitlistEntryCreate`   | Done   |       |
| GET    | `/waitlist/success/<code>`| `/waitlist/success/{code}`           |                         | To Do  | Not implemented |
| GET    | `/blog`                   | `/blog`                              |                         | Done   |       |
| GET    | `/blog/<slug>`            | `/blog/{slug}`                       |                         | Done   |       |
| GET    | `/download/<magnet_name>` | `/download/{magnet_name}`            |                         | To Do  | Not implemented |
| GET    | `/`                       | `/`                                  |                         | To Do  | Not implemented |
| GET    | `/api/waitlist/stats`     | `/waitlist/stats`                    | `WaitlistStats`         | Done   |       |
| GET    | `/api/blog/search`        | `/blog/search`                       |                         | Done   |       |

## Domain: Newsletter (`/newsletter`)

| Method | Legacy Flask Route | FastAPI Target (`/api/v1/newsletter`) | Pydantic Schema            | Status | Notes |
|--------|--------------------|---------------------------------------|----------------------------|--------|-------|
| GET/POST| `/subscribe`       | `/subscribe`                          | `NewsletterSubscriberCreate` | Done   |       |
| GET    | `/success`         | `/success`                            |                            | Done   |       |
| GET/POST| `/unsubscribe`     | `/unsubscribe`                        |                            | Done   |       |
| GET/POST| `/preferences`     | `/preferences`                        |                            | To Do  | Not implemented |
| POST   | `/api/subscribe`   | `/subscribe`                          | `NewsletterSubscriberCreate` | Done   |       |
| GET    | `/api/stats`       | `/stats`                              | `NewsletterStats`          | Done   |       |

## Domain: Social (`/social`)

| Method | Legacy Flask Route          | FastAPI Target (`/api/v1/social`) | Pydantic Schema | Status | Notes |
|--------|-----------------------------|-----------------------------------|-----------------|--------|-------|
| GET/POST| `/share`                    | `/share`                          | `ShareRequest`  | Done   |       |
| GET    | `/share/blog/<slug>`        | `/share/blog/{slug}`              |                 | Done   |       |
| GET    | `/follow`                   | `/follow`                         |                 | Done   |       |
| GET    | `/embed`                    | `/embed`                          |                 | Done   |       |
| GET    | `/api/share-stats`          | `/share-stats`                    | `ShareStats`    | Done   |       |
| GET    | `/api/generate-share-url`   | `/generate-share-url`             |                 | Done   |       |
| GET    | `/widgets/follow-buttons`   | `/widgets/follow-buttons`         |                 | Done   |       |
| GET    | `/widgets/share-buttons`    | `/widgets/share-buttons`          |                 | Done   |       |

## Domain: Miscellaneous (No Blueprint)

| Method | Legacy Flask Route                | FastAPI Target (`/api/v1`) | Pydantic Schema | Status | Notes |
|--------|-----------------------------------|----------------------------|-----------------|--------|-------|
| GET    | `/`                               | `/`                        |                 | Done   | Landing page |
| GET    | `/home`                           | `/`                        |                 | Done   | Redirect |
| POST   | `/api/newsletter/subscribe`       | `/newsletter/subscribe`    | `NewsletterSubscriberCreate` | Done   |       |
| GET    | `/health`                         | `/health`                  |                 | Done   |       |
| GET    | `/favicon.ico`                    | `/favicon.ico`             |                 | Done   | Static file |
| GET    | `/manifest.json`                  | `/manifest.json`           |                 | Done   | Static file |
| DELETE | `/sensors/delete/<int:sensor_id>` | `/sensors/{sensor_id}`     |                 | To Do  | Not implemented |
| POST   | `/settings`                       | `/settings`                |                 | To Do  | Not implemented |
| POST   | `/settings/upload-logo`           | `/settings/upload-logo`    |                 | To Do  | Not implemented |
| POST   | `/decorateImage`                  | `/images/decorate`         |                 | To Do  | Not implemented |