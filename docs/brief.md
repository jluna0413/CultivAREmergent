# Project Brief: CultivAR (Living Document)

**Last Updated:** 2025-12-09
**Status:** In Development (Alpha/Beta Transition)

## Executive Summary

CultivAR is a comprehensive, cloud-native platform for cannabis cultivation management. It combines a secure, high-performance **FastAPI backend** with a cross-platform **Flutter application** (Mobile & Web) to serve the needs of modern "prosumer" growers and craft breeders.

The platform provides an end-to-end "Seed to Harvest" tracking system, hardware-agnostic sensor integration, and a foundation for advanced AI analytics and a breeding marketplace.

## Current Project Status

The project has moved beyond the initial MVP concept and has a functional codebase with the following core components implemented:

-   **Backend Core:**
    -   **Framework:** Python FastAPI (Async).
    -   **Database:** PostgreSQL with SQLAlchemy/Alembic migrations.
    -   **Auth:** OAuth2 integration (Keycloak ready) with secure role-based access.
    -   **API:** Comprehensive REST API structure with Blueprinting.

-   **Frontend Application:**
    -   **Framework:** Flutter (Mobile & Web).
    -   **Architecture:** Feature-first architecture with Provider state management.
    -   **Core Modules:**
        -   **Dashboard:** Real-time metrics and quick actions.
        -   **Plants:** Complete lifecycle tracking (Strains, Batches, Plants).
        -   **Sensors:** Environmental monitoring integration.
        -   **Auth:** Secure login/registration flows.
        -   **Admin:** User management and system configuration.

-   **Emerging Features (In Progress/Stubbed):**
    -   **AI Integration:** Foundational structure for AI-driven insights.
    -   **Marketplace Elements:** Stubs for Cart, Seedbank, and Gear.

## Problem Statement

Modern cultivation requires managing complex data sets—genetics, environment, nutrients, and schedules. Existing solutions are either:
1.  **Low-tech:** Spreadsheets/Paper (hard to analyze).
2.  **Fragmented:** IoT apps that don't talk to journals.
3.  **Closed:** Vendor-locked ecosystems.

CultivAR solves this by unifying **Data (Journal)**, **Hardware (Sensors)**, and **Intelligence (AI)** into a single, open platform.

## Target Users

1.  **The "Prosumer" Grower:** Tech-savvy hobbyists investing in quality. Needs data vs. intuition.
2.  **The Craft Breeder:** Small-scale geneticists needing lineage tracking and performance data (Proof of Work).

## Strategic Goals & Success Metrics

-   **Primary Goal:** Deliver a stable, "daily driver" usable application for tracking active grows.
-   **Secondary Goal:** Validate the "Hardware Agnostic" promise by ensuring diverse sensor integrations work.
-   **Long-term Vision:** Private Blockchain for data sovereignty + Federated Learning for AI models.

**KPIs:**
-   Daily Active Users (DAU) retention.
-   Number of "Harvests" successfully completed in-app.
-   Sensor data points logged per user.

## Technical Architecture

-   **Frontend:** Flutter (Dart) - Targeting iOS, Android, Web.
-   **Backend:** Python 3.10+ FastAPI.
-   **Data:** PostgreSQL.
-   **Infrastructure:** Dockerized services (App, DB, Auth).

## Roadmap

### Phase 1: Foundation (Current - ~80% Complete)
-   [x] Core Data Models (Plant, Strain, Sensor).
-   [x] Basic Auth & User Management.
-   [x] Functional Flutter UI Shell.
-   [x] Dashboard & Basic Journaling.
-   [ ] **Critical:** Full E2E testing of Sensor -> Backend -> Frontend data flow.
-   [ ] **Critical:** Polish of "Nutrient" and "Watering" logs.

### Phase 2: Intelligence & Integration (Next)
-   [ ] AI Advisor "Chat" basic implementation.
-   [ ] Advanced Charts & Visualizations for Sensor Data.
-   [ ] Plugin System Architecture.

### Phase 3: Commerce & Ecosystem (Future)
-   [ ] Genetics Marketplace.
-   [ ] Breeder Verification ("Proof of Grow").
-   [ ] Blockchain Integration.

## Open Questions / Risks
-   **Data Sync:** ensuring offline-first capabilities for mobile users (if requested).
-   **Hardware Compatibility:** Testing diverse sensor protocols without physical hardware access.
