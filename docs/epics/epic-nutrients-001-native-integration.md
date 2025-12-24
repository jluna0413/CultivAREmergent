# Epic: Native Nutrient Management System

**Epic ID**: EPIC-NUTRIENTS-001  
**Status**: Specification  
**Priority**: High  
**Estimated Story Points**: 55-65  
**Target Sprint**: Multiple sprints (3-4 sprints)

## Epic Goal

Integrate native nutrient calculator and inventory management into CultivAR to replace the Emerald sidecar approach, creating a seamless, cohesive user experience for nutrient planning, mixing calculations, and stash tracking.

## Business Value

- **Unified UX**: Eliminates context switching between CultivAR and external Emerald service
- **Performance**: Removes network latency to separate container
- **Offline-First**: Works without Docker/Emerald dependencies
- **Mobile Native**: Calculator in Flutter = superior mobile experience
- **AI Integration**: Nutrient inventory enables AI to recommend solutions based on available supplies
- **Cost Tracking**: Users can see cost per feeding and manage budget

## User Personas

1. **Prosumer Grower**: Wants precision nutrient management with professional formulas
2. **Craft Breeder**: Needs to track multiple strains with different feeding schedules
3. **Budget-Conscious Grower**: Wants to track nutrient costs and inventory

## Technical Scope

### Backend (Python/FastAPI)
- Database models for nutrients, formulas, inventory, water sources
- Calculator service with growth stage/medium/strength support
- RESTful API endpoints for all operations
- Seed data for 10+ professional nutrient brands

### Frontend (Flutter/Dart)
- Nutrient calculator UI with brand/stage/medium selectors
- Inventory management screens with low-stock alerts
- Water source configuration
- Integration with existing plant management  
- Feeding history and schedules

### Data
- Pre-configured formulas for major brands:
  - General Hydroponics FloraSeries
  - Fox Farm Trio
  - Canna Coco A&B
  - Advanced Nutrients pH Perfect
  - Jack's 321
  - MegaCrop
  - And 4+ more brands

## Dependencies

- Existing plant management system
- User authentication system
- Database migration capabilities
- Flutter Riverpod state management

## Out of Scope (Future Enhancements)

- Automated feeding schedules/reminders
- Integration with AC Infinity for auto-dosing
- Custom nutrient brand creation by users
- Import from existing Emerald databases
- Nutrient marketplace/ordering

## Success Criteria

1. Users can calculate precise nutrient mixes for any growth stage/medium
2. Calculator accounts for water source and auto-recommends CalMag
3. Inventory tracking shows remaining quantities with low-stock alerts
4. Cost per feeding is calculated when inventory has cost data
5. Calculator checks inventory sufficiency before mixing
6. All 10+ brands have formulas for all growth stages
7. Zero errors in calculator logic (verified against Emerald)
8. Mobile and web UI both functional
9. Performance: Calculator response < 200ms

## Stories Breakdown

### Phase 1: Backend Foundation (Sprint 1)
1. **STORY-NUT-001**: Database models for nutrient management
2. **STORY-NUT-002**: Nutrient calculator service implementation
3. **STORY-NUT-003**: Nutrient brands seed data
4. **STORY-NUT-004**: API endpoints for brands and formulas
5. **STORY-NUT-005**: Calculator API endpoint
6. **STORY-NUT-006**: Inventory API endpoints

### Phase 2: Flutter UI - Calculator (Sprint 2)
7. **STORY-NUT-007**: Nutrient calculator screen UI
8. **STORY-NUT-008**: Brand/component selection widgets
9. **STORY-NUT-009**: Growth stage/medium/strength selectors
10. **STORY-NUT-010**: Mix results display with instructions
11. **STORY-NUT-011**: Water source configuration screen

### Phase 3: Flutter UI - Inventory (Sprint 2-3)
12. **STORY-NUT-012**: Inventory list screen
13. **STORY-NUT-013**: Add/edit inventory items
14. **STORY-NUT-014**: Low-stock alerts and badges
15. **STORY-NUT-015**: Inventory deduction on feeding log

### Phase 4: Integration & Polish (Sprint 3)
16. **STORY-NUT-016**: Integrate calculator with plant detail screen
17. **STORY-NUT-017**: Feeding schedule management
18. **STORY-NUT-018**: Feeding history/logs
19. **STORY-NUT-019**: Cost tracking and analytics

### Phase 5: Testing & Documentation (Sprint 4)  
20. **STORY-NUT-020**: Comprehensive testing suite
21. **STORY-NUT-021**: User documentation
22. **STORY-NUT-022**: Migration from sidecar approach

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|----------|
| Calculator formula accuracy | High | Verify against Emerald calculations, unit tests |
| Complex UI/UX for calculator | Medium | Iterate with user testing, follow Emerald's proven UX |
| Database migrations | Medium | Test migrations on copy of DB first |
| Performance with large inventory | Low | Index key fields, pagination |

## Technical Debt Items

- Remove Emerald sidecar configuration from `docker-compose.yml`
- Remove `emerald_client.py` and `integrations.py` proxy endpoints
- Remove `emerald_integration_service.dart`

## Notes

- Implementation Plan already created: `implementation_plan.md`
- Backend Phase 1 already completed:
  - ✅ Models created
  - ✅ Calculator service implemented
  - ✅ API router created  
  - ✅ 3 brands seeded
  - ✅ Router registered in main.py
- Next: Flutter implementation (Phase 2)

## References

- Implementation Plan: `C:\Users\jonat\.gemini\antigravity\brain\c10a0dd5-34c6-436f-bd3a-2a0fa1d4d48c\implementation_plan.md`
- Original Emerald Repo: https://github.com/Dmans218/emerald-plant-tracker
- BMad Project PRD: `docs/prd.md`
- Architecture Docs: `docs/architecture/`
