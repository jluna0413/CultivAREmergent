# Product Requirements Document (PRD) - CultivAR Refinement & AI Readiness

**Version:** 3.0
**Status:** In Progress
**Author:** AI Product Manager (BMad Orchestrator)

## 1. Introduction

This PRD outlines the requirements for the "Refinement & AI Readiness" phase of CultivAR, plus the **Genetics Marketplace with Fractional G-NFTs**. Building upon the existing Alpha codebase, this defines features for transitioning from "functional prototype" to "usable product" while adding blockchain-powered marketplace capabilities.

## 2. Goals & Objectives

-   **Stabilize Core Loops:** Ensure the Plant Life Cycle (Seed → Harvest) is frictionless.
-   **Data Integrity:** Guarantee that sensor data and manual logs are stored reliably and retrievable for analysis.
-   **AI Foundation:** Structure data ingestion to allow LLM agents to "read" a grow's state.
-   **Genetics Marketplace:** Enable breeders to sell seed genetics as fractional NFTs with compliance, escrow, and gamification.

## 3. User Personas

-   **Jon (The Prosumer):** Wants to check his phone and see exactly if his VPD is off. Wants to log nutrients quickly without typing.
-   **Mary (The Breeder):** Wants to tag a specific plant as a "Mother" and track all clones taken from it. Wants to sell her genetics on the marketplace.
-   **Alex (The Breeder - Marketplace Seller):** Wants to mint G-NFTs for harvests, set prices per pack size, track sales, and climb leaderboards.
-   **Sam (The Collector):** Wants to buy rare genetics as NFTs, trade them on secondary market, and burn them to grow.

## 4. Functional Requirements

### 4.1 Core Journaling (Refinement)
-   **FR-001 [Visual Timeline]:** Users must see a visual timeline of their plant's life stages (Seedling, Veg, Flower).
-   **FR-002 [Batch Actions]:** Users must be able to apply an action (e.g., "Watered") to multiple plants/batches at once.
-   **FR-003 [Photo Gallery]:** Users must be able to view a gallery of photos filtered by Plant ID or Date.

### 4.2 Environmental Monitoring
-   **FR-004 [VPD Calculation]:** The system must automatically calculate VPD based on Temp/Humidity sensor readings.
-   **FR-005 [Alert Thresholds]:** Users must be able to set Min/Max thresholds for Temp/Humidity/VPD and receive in-app alerts.

### 4.3 AI & Intelligence
-   **FR-006 [Context Ingestion]:** The backend must expose a "Context API" that summarizes the current state of a grow (Env + Logs) for the AI Agent.
-   **FR-007 [Chat Interface]:** A dedicated "Grow Copilot" chat interface in the Flutter app.

### 4.4 Genetics Marketplace (NEW)
-   **FR-008 [G-NFT Minting]:** Breeders must be able to mint Master G-NFTs ($2 upfront) and create fractional Pack NFTs (lazy-minted on purchase).
-   **FR-009 [Marketplace Listings]:** Breeders must be able to create listings with pricing per pack size (3/5/6/10/12 seeds).
-   **FR-010 [Hybrid Minting]:** System must enforce 10% lot value escrow with milestone-based releases.
-   **FR-011 [Compliance System]:** AI agent must scrape state-by-state cannabis seed laws and validate shipping addresses.
-   **FR-012 [Crypto Coin Fulfillment]:** For restricted states, system must generate physical crypto coins with dual-signature redemption.
-   **FR-013 [Multi-Stage Reputation]:** System must collect delivery, germination, and harvest ratings to calculate breeder reputation (0-100).
-   **FR-014 [Leaderboards]:** System must rank breeders across 15 categories (sales, quality, pack types, NFTs, coins).
-   **FR-015 [Secondary Market]:** Users must be able to list Pack NFTs for resale with automated 70/20/10 royalty distribution.
-   **FR-016 [QR Verification]:** Packing slips must include dynamic QR codes for delivery verification and analytics.

## 5. Non-Functional Requirements (NFRs)

-   **NFR-001 [Performance]:** Dashboard load time under 1.5s on 4G networks.
-   **NFR-002 [Security]:** All sensor data endpoints must be authenticated via JWT.
-   **NFR-003 [Scalability]:** DB Schema must support partitioned time-series data for sensor logs.
-   **NFR-004 [Blockchain Reliability]:** Marketplace must function with database fallback if Algorand network is down.
-   **NFR-005 [Privacy Compliance]:** Compliance agent must only access state codes, never full addresses (encrypted).
-   **NFR-006 [Fraud Prevention]:** Escrow system must prevent double-selling with <1% fraud rate target.

## 6. Data Requirements

-   **Plant Model Update:** Add `mother_id` (Self-referential FK) to support cloning lineage.
-   **Sensor Log Model:** Ensure `timestamp` is indexed for time-series queries.
-   **Genetics Marketplace Models:** 25+ new tables (see Epic EPIC-GNFT-001) including breeders, G-NFTs, wallets, loyalty points, escrows.

## 7. Success Metrics

-   Reduction in "Time to Log" for daily activities.
-   Successful rendering of "Grow Context" by the AI agent.
-   **Marketplace:** 100+ breeders, 500+ listings, 90%+ germination rate, <1% fraud rate within 6 months.
-   **Engagement:** 30%+ breeder leaderboard participation, 20%+ loyalty point redemptions.

## 8. Related Epics

-   **EPIC-GNFT-001:** Genetics Marketplace with Fractional G-NFTs (56 stories, 10 phases)
   - See: `docs/epics/epic-gnft-001-genetics-marketplace.md`

