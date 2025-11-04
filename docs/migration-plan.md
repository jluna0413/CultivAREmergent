# Flutter Migration Plan - CultivAREmergant
# Flutter-Driven Decommission Gates and Legacy Removal Strategy

**Project**: CultivAR FastAPI Migration  
**Migration Goal**: Transition from Flask/HTML to Flutter/FastAPI architecture  
**Status**: Implementation phase - 11/12 comments completed  
**Next**: Final migration plan and legacy decommissioning strategy  

## Overview

This document defines the Flutter-driven gates and criteria for safely removing Flask/legacy components once Flutter reaches API parity. Each gate has specific acceptance criteria and rollback procedures.

## Migration Gates

### Gate A: Authentication & CI Infrastructure ✅
**Status**: **COMPLETED** - Auth endpoints and CI pipeline are production-ready

**Acceptance Criteria**:
- ✅ JWT authentication endpoints (login, refresh, logout) implemented with async ORM
- ✅ Token rotation and revocation working with proper JWT utils
- ✅ CI pipeline with comprehensive gating (lint, type checks, async tests, Alembic dry-run, OpenAPI diff, security scans)
- ✅ Production performance configuration (pool settings, echo control)
- ✅ Rate limiting implemented with Redis backend

**Flask Components Remaining**: `app/blueprints/*`, `app/routes/*`, `cultivar_app.py`
**Actions**: Ready to proceed to Gate B

---

### Gate B: Core Domain APIs Complete with Flutter Client
**Status**: **IN PROGRESS** - OpenAPI contract generation and Flutter client working

**Acceptance Criteria**:
- [ ] `/api/v1/users/*` - User management endpoints (GET, POST, PUT, DELETE)
- [ ] `/api/v1/plants/*` - Plant management endpoints (list, detail, create, update, delete)
- [ ] `/api/v1/strains/*` - Strain management endpoints (list, detail, create, update, delete)
- [ ] `/api/v1/sensors/*` - Sensor reading endpoints (list, create, readings)
- [ ] OpenAPI contract properly generated and committed to `docs/generated/openapi.json`
- [ ] Flutter client successfully generated and imported into Flutter app
- [ ] Pagination requirements met on all list endpoints
- [ ] API v1 endpoints have proper CRUD coverage for all core domains

**Flutter App Requirements**:
- All `/api/v1/*` endpoints available and functional
- Flutter client integration working with proper typing
- Data models properly mapped between API and Flutter

**Migration Actions**:
1. Verify all core domain APIs are production-ready
2. Generate and validate Flutter client integration
3. Test API parity with Flutter app
4. Proceed to Gate C when all core APIs validated

---

### Gate C: Staging Parity Validated by Flutter E2E Testing
**Status**: **PENDING** - Requires Flutter app integration testing

**Acceptance Criteria**:
- [ ] Flutter app fully functional with all `/api/v1/*` endpoints
- [ ] End-to-end testing validates Flutter ↔ FastAPI integration
- [ ] Performance benchmarks confirm Flutter performance meets requirements
- [ ] User acceptance testing (UAT) completed for core workflows:
  - Plant lifecycle management (create, update, harvest)
  - Strain catalog browsing and management
  - User profile and settings management
  - Sensor data integration and monitoring
- [ ] Data migration strategy validated (existing Flask data → FastAPI)
- [ ] No critical issues in staging environment
- [ ] Production deployment strategy approved

**Testing Requirements**:
- Flutter E2E tests passing for all core user journeys
- API response times within acceptable ranges
- Error handling and edge cases properly managed
- Data consistency verified across migrations

**Migration Actions**:
1. Deploy FastAPI staging environment
2. Conduct Flutter integration testing
3. Execute E2E test suite with real user scenarios
4. Address any critical issues found
5. Proceed to Gate D when all staging validation complete

---

### Gate D: Legacy Flask Removal and Final Cleanup
**Status**: **PENDING** - Final migration step after Gates A, B, C

**Acceptance Criteria**:
- [ ] All Flask user traffic migrated to Flutter app
- [ ] No critical API regressions detected
- [ ] Rollback procedures tested and verified
- [ ] Data migration to FastAPI completed successfully
- [ ] Legacy Flask components safely removed

**Components to Remove**:
1. **Flask Blueprint Routes**:
   - `app/blueprints/*` - All Flask blueprint implementations
   - `app/routes/*` - Legacy route definitions
   - `cultivar_app.py` - Main Flask application file

2. **Flask Dependencies**:
   - Remove Flask-related packages from `requirements.txt`
   - Remove Flask-related imports and dependencies

3. **Legacy Templates & Static Assets**:
   - HTML templates (retained only if needed for marketing pages)
   - Flask-specific static file handling

4. **Database Migration**:
   - Ensure all Flask ORM models migrated to FastAPI async models
   - Validate data integrity during migration

**Migration Process**:
1. **Data Migration Phase**:
   ```bash
   # Backup existing Flask database
   pg_dump production_flask_db > flask_backup_$(date +%Y%m%d).sql
   
   # Run data migration scripts if needed
   python scripts/migrate_flask_to_fastapi.py
   ```

2. **API Gateway Switch**:
   ```bash
   # Update production load balancer
   # Point /api/* requests to FastAPI application
   # Keep Flask running for final validation
   ```

3. **Traffic Migration**:
   ```bash
   # Gradual traffic shift (A/B testing)
   # 10% → 50% → 100% FastAPI traffic
   # Monitor metrics during transition
   ```

4. **Legacy Removal**:
   ```bash
   # Remove Flask blueprints and routes
   rm -rf app/blueprints/ app/routes/ cultivar_app.py
   
   # Update production requirements
   pip uninstall flask flask-login flask-wtf jinja2
   ```

5. **Final Cleanup**:
   - Remove Flask dependencies from requirements
   - Archive Flask templates (if not needed)
   - Update deployment scripts
   - Remove Flask-related Docker configurations

## Rollback Procedures

### Emergency Rollback Plan
**Trigger**: Critical issues in production Flutter app

**Immediate Actions**:
1. **Traffic Redirect**: Route traffic back to Flask app via load balancer
2. **Database Rollback**: Restore Flask database from backup
3. **API Rollback**: Disable FastAPI endpoints, restore Flask routes

### Target Rollback Time: < 15 minutes

**Rollback Steps**:
```bash
#!/bin/bash
# Emergency rollback script

# Step 1: Stop traffic to FastAPI
echo "🚨 Starting emergency rollback..."
kubectl scale deployment fastapi-app --replicas=0

# Step 2: Restore Flask traffic  
kubectl scale deployment flask-app --replicas=3

# Step 3: Restore database if needed
# pg_restore -d flask_db flask_backup_20251101.sql

# Step 4: Update load balancer
# Point traffic to Flask app

echo "✅ Rollback completed"
```

## Success Metrics

### Gate B Success Criteria
- **API Coverage**: 100% of core domains available via `/api/v1/*`
- **OpenAPI Validation**: No schema changes without CI approval
- **Flutter Client**: Generated client integrates successfully with Flutter app

### Gate C Success Criteria  
- **Performance**: Flutter app performs within 20% of Flask performance
- **Reliability**: >99.5% uptime during testing period
- **User Acceptance**: Core workflows validated by end users

### Gate D Success Criteria
- **Zero Downtime**: No user-visible downtime during migration
- **Data Integrity**: 100% data consistency verified post-migration
- **Performance**: FastAPI outperforms Flask by >10%

## Timeline and Dependencies

**Gate B**: 1-2 weeks (API completion + Flutter client integration)  
**Gate C**: 2-4 weeks (Flutter app development + testing)  
**Gate D**: 1 week (migration execution + final cleanup)  

**Total Migration Time**: 4-7 weeks from Gate B start

## Risks and Mitigations

### Risk: API Performance Issues
**Mitigation**: Load testing with production-equivalent data volumes
**Trigger**: API response times > Flask performance by 20%

### Risk: Flutter App Critical Bugs
**Mitigation**: Comprehensive E2E testing with staged deployment
**Trigger**: Critical user workflows failing

### Risk: Data Migration Failures
**Mitigation**: Full database backups and testing with migration scripts
**Trigger**: Data corruption or loss during migration

### Risk: User Adoption Resistance
**Mitigation**: Gradual rollout with feature parity and user training
**Trigger**: User complaints about missing features

## Communication Plan

### Migration Announcements
- **Week 1**: Internal team notification of Gate B start
- **Week 3**: Stakeholder briefing on Gate C testing
- **Week 4-5**: User notification of Flutter beta testing
- **Week 6**: Production rollout announcement
- **Week 7**: Legacy removal completion notification

### Status Updates
- **Daily**: Internal team standup during active migration
- **Weekly**: Stakeholder status report
- **Milestone**: Gate completion announcement

## Post-Migration Validation

### Week 1 Post-Migration
- [ ] Monitor production metrics (response times, error rates)
- [ ] Collect user feedback via Flutter app
- [ ] Validate data consistency
- [ ] Confirm API performance meets SLA

### Week 2-4 Post-Migration
- [ ] User satisfaction surveys
- [ ] Performance optimization based on production data
- [ ] Feature enhancement planning
- [ ] Final legacy cleanup verification

## Notes

- **Current Implementation**: 11/12 migration comments completed
- **Remaining**: Gate B/C/D implementation and Flutter app development
- **Ready for**: Gate B start - core domain API completion
- **Dependencies**: Flutter app development timeline

**Last Updated**: 2025-11-01  
**Next Review**: Upon Gate B completion  
**Document Version**: 1.0