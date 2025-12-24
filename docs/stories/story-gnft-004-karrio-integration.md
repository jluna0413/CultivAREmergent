# Story: Karrio MCP Integration

**ID:** STORY-GNFT-004
**Epic:** EPIC-GNFT-001
**Priority:** P0 (Infrastructure)
**Status:** Ready for Dev

## 1. User Story
As a **Developer Agent**, I need a **Karrio MCP Server** so that I can interact with shipping providers (create labels, track packages) using standardized tools within the Context Forge.

## 2. Context
We are integrating `karrio/karrio` (self-hosted) for shipping. Instead of direct API calls scattered across the app, we will encapsulate this in an MCP server.

## 3. Implementation Plan
1.  **Karrio Service Deployment**:
    - Add `karrio`, `karrio-server`, `karrio-worker`, `karrio-redis`, `karrio-db` to `docker-compose.yml`.
2.  **MCP Server Implementation**:
    - Create `app/mcp/karrio_server.py`.
    - Implement tools: `create_tracker`, `get_tracker_status`, `list_carriers`, `create_shipment`.
    - Use `httpx` to talk to the local Karrio instance.
3.  **Configuration**:
    - Add `KARRIO_API_KEY` and `KARRIO_URL` to `.env`.

## 4. Acceptance Criteria
- [ ] Karrio UI is accessible at `http://localhost:5002`.
- [ ] MCP Server `app/mcp/karrio_server.py` starts successfully.
- [ ] Tool `create_tracker` successfully registers a tracking number with Karrio.
- [ ] Tool `get_tracker_status` returns real-time status.

## 5. Technical Notes
- **Spec**: Refer to [karrio_mcp_server_spec.md](file:///C:/Users/jonat/.gemini/antigravity/brain/7de6363f-812e-4ed6-804e-0bf3b9486eb8/karrio_mcp_server_spec.md).
- **Network**: Ensure Karrio containers are on `cultivar-network`.
