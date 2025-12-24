# User Stories - CultivAR

**Status:** Ready for Refinement

## EPIC-01: Core Journaling Refinement

### US-001: Visual Plant Life Cycle Timeline
**As a** Grower,
**I want** to see a horizontal timeline on the Plant Detail screen showing stages (Seedling, Veg, Flower) and current progress,
**So that** I know exactly how many days I am into the current stage without counting on a calendar.

*Acceptance Criteria:*
-   [ ] Visual bar component showing stages.
-   [ ] Current day highlighted.
-   [ ] Estimated harvest date marker.

### US-002: Batch Watering Action
**As a** Grower with many plants,
**I want** to select multiple plants in the dashboard and log a "Watering" event for all of them at once,
**So that** I save time and don't get annoyed by repetitive tapping.

*Acceptance Criteria:*
-   [ ] "Select" mode in Plant List.
-   [ ] "Log Action" button appears when >1 selected.
-   [ ] Backend creates individual log entries for each plant.

---

## EPIC-02: Environmental Intelligence

### US-003: Implement VPD Calculation
**As a** Grower,
**I want** to see "VPD" (Vapor Pressure Deficit) displayed alongside Temp/Humidity,
**So that** I know if my plants can transpire efficiently.

*Acceptance Criteria:*
-   [ ] Helper function `calculate_vpd(temp, humidity, leaf_temp_offset)` implemented.
-   [ ] Backend computes this on sensor data ingestion.
-   [ ] Frontend displays VPD value with color coding (Green=Good, Red=Bad).

### US-004: Sensor Alert Configuration
**As a** Grower,
**I want** to set a "Max Temp" of 85°F,
**So that** I get a push notification if my tent gets too hot.

*Acceptance Criteria:*
-   [ ] UI to set Min/Max for Temp/Humidity.
-   [ ] Backend background worker checks incoming readings against thresholds.
-   [ ] Notification triggered (In-App).

---

## EPIC-03: AI Readiness

### US-005: Context API Endpoint
**As an** AI Agent,
**I want** to call `GET /api/v1/context/{grow_id}`,
**So that** I can receive a JSON summary of the latest logs, sensor averages, and plant capabilities to answer user questions.

*Acceptance Criteria:*
-   [ ] Endpoint returns structured text summary.
-   [ ] Includes last 24h min/max/avg for sensors.
-   [ ] Includes last 3 active logs.

### US-006: Chat Interface Skeleton
**As a** User,
**I want** a "Chat" tab in the app,
**So that** I can eventually talk to the AI Advisor.

*Acceptance Criteria:*
-   [ ] New Tab/Screen "Advisor".
-   [ ] Standard Chat UI (User bubble right, Bot bubble left).
-   [ ] **Note:** For now, Bot can just echo back or say "Coming Soon".
