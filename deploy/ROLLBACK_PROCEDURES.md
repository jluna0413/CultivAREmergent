# Flask Service Restoration Rollback Procedures

**Document Version:** 1.0  
**Created:** October 31, 2025  
**Trigger:** Post-cutover SLO violations or critical issues  
**Author:** Operations Lead  
**Emergency Contact:** ops@cultivar.com  

## Overview

This document provides step-by-step procedures to restore Flask service if post-cutover SLOs are violated after migrating to FastAPI. These procedures ensure minimal downtime and data integrity during emergency rollback scenarios.

## Rollback Triggers

The following conditions trigger immediate rollback procedures:

### Critical Triggers (Immediate Rollback Required)
- **Service Availability < 99.5%** for more than 2 minutes
- **5xx Error Rate > 10%** for more than 1 minute
- **95th Percentile Response Time > 5 seconds** for more than 1 minute
- **Complete service unavailability** for more than 30 seconds
- **Data corruption or loss** detected
- **Security breach** or unauthorized access
- **Database connectivity failure** lasting more than 1 minute

### Warning Triggers (Assessment Required)
- **Service Availability < 99.9%** for more than 5 minutes
- **5xx Error Rate > 5%** for more than 2 minutes
- **95th Percentile Response Time > 2 seconds** for more than 3 minutes
- **High memory usage** (>90%) for more than 5 minutes
- **Disk space critical** (<10% free) for more than 1 minute

## Pre-Rollback Verification

Before initiating rollback, verify the following:

### 1. Database Backup Status
```bash
# Verify latest backup exists and is recent
ls -la /backups/database/
# Check backup is within 1 hour
find /backups/database/ -name "*.sql" -mmin -60
```

### 2. Flask Service Readiness
```bash
# Check Flask service is available and healthy
curl -f http://localhost:5000/health || echo "Flask service down"
```

### 3. Current State Documentation
```bash
# Document current state before rollback
echo "Rollback initiated at: $(date)" >> rollback_log.txt
curl -s http://localhost:5001/health/status | jq . >> rollback_log.txt
ps aux | grep uvicorn >> rollback_log.txt
```

## Rollback Procedures

### Phase 1: Immediate Traffic Redirection (30 seconds)

#### Step 1.1: Update Load Balancer Configuration
```bash
# Update nginx configuration to route to Flask
sudo cp /etc/nginx/sites-available/cultivar-fastapi /etc/nginx/sites-available/cultivar-fastapi-backup
sudo cp /etc/nginx/sites-available/cultivar-flask /etc/nginx/sites-available/cultivar-fastapi

# Test nginx configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx

# Verify traffic redirection
curl -I http://cultivar.com/health
```

#### Step 1.2: DNS Fallback (if using DNS-based routing)
```bash
# Update DNS to point to Flask service IP
nslookup cultivar.com
# Note: In production, use Route53/CloudFlare API or console
# This is a manual step for emergency procedures
```

#### Step 1.3: Verify Traffic Redirection
```bash
# Check new endpoints are serving
curl -f http://cultivar.com/health
curl -f http://cultivar.com/api/v1/plants
```

**Expected Outcome:** All traffic should now route to Flask service.

### Phase 2: Service Shutdown and Cleanup (60 seconds)

#### Step 2.1: Stop FastAPI Service
```bash
# Find and stop all FastAPI processes
pkill -f "uvicorn.*fastapi_app"
pkill -f "uvicorn.*5001"

# Verify FastAPI processes stopped
ps aux | grep uvicorn | grep -v grep

# If processes don't stop gracefully, force kill
sudo pkill -9 -f "uvicorn.*fastapi_app"
```

#### Step 2.2: Stop FastAPI Container (if using Docker)
```bash
# Stop FastAPI containers
docker stop cultvar-fastapi

# Verify containers stopped
docker ps | grep fastapi
```

#### Step 2.3: Resource Cleanup
```bash
# Free up ports if needed
sudo lsof -i :5001
sudo fuser -k 5001/tcp
```

### Phase 3: Flask Service Restoration (120 seconds)

#### Step 3.1: Start Flask Service
```bash
# Start Flask application
cd /opt/cultivar
source venv/bin/activate
python cultivar_app.py &

# Or using systemd
sudo systemctl start cultivar-flask
sudo systemctl status cultivar-flask
```

#### Step 3.2: Verify Flask Service Health
```bash
# Health check
curl -f http://localhost:5000/health

# Test API endpoints
curl -f http://localhost:5000/api/v1/plants
curl -f http://localhost:5000/dashboard
```

#### Step 3.3: Database Migration Rollback (if needed)
```bash
# If database was migrated to async models, rollback migrations
alembic downgrade -1

# Verify database is in previous state
python scripts/validate_migration.py
```

### Phase 4: Verification and Monitoring (300 seconds)

#### Step 4.1: End-to-End Testing
```bash
# Test all critical endpoints
python scripts/test_flask_endpoints.py

# Test database connectivity
python scripts/test_db_connectivity.py

# Test authentication
python scripts/test_auth_flow.py
```

#### Step 4.2: Performance Baseline Verification
```bash
# Run performance tests against Flask
python scripts/performance_baseline.py

# Compare against pre-migration metrics
# Expected: Similar or better than original performance
```

#### Step 4.3: User Acceptance Testing
```bash
# Test with test accounts
python scripts/test_user_flows.py

# Verify all features work as expected
curl -f http://localhost:5000/admin/users
```

### Phase 5: Communication and Documentation (Ongoing)

#### Step 5.1: Stakeholder Notification
```bash
# Send notification to stakeholders
echo "Flask service rollback completed at $(date)" | \
mail -s "Cultivar Rollback Notification" ops@cultivar.com engineering@cultivar.com

# Update status page
# Update incident ticket
```

#### Step 5.2: Post-Mortem Preparation
```bash
# Collect logs for analysis
mkdir -p /var/log/rollback/$(date +%Y%m%d-%H%M%S)
cp /var/log/nginx/access.log /var/log/rollback/$(date +%Y%m%d-%H%M%S)/
cp /var/log/cultivar/app.log /var/log/rollback/$(date +%Y%m%d-%H%M%S)/

# Collect metrics snapshots
curl http://localhost:5000/health/status > /var/log/rollback/$(date +%Y%m%d-%H%M%S)/fastapi_metrics.json
```

#### Step 5.3: Incident Report
Create incident report with:
- Root cause analysis
- Timeline of events
- Impact assessment
- Lessons learned
- Action items for prevention

## Rollback Verification Checklist

Use this checklist to verify rollback was successful:

### Immediate Verification (0-5 minutes)
- [ ] Traffic redirected to Flask service
- [ ] Flask service responding to health checks
- [ ] No 5xx errors in logs
- [ ] Load balancer routing correctly
- [ ] DNS updated (if applicable)

### Functional Verification (5-15 minutes)
- [ ] All critical API endpoints responding
- [ ] User authentication working
- [ ] Database queries executing successfully
- [ ] File uploads/downloads working
- [ ] Background tasks running

### Performance Verification (15-30 minutes)
- [ ] Response times within acceptable ranges
- [ ] Error rates below thresholds
- [ ] CPU/memory usage normal
- [ ] Database performance acceptable
- [ ] No memory leaks detected

### User Acceptance (30+ minutes)
- [ ] End-to-end user workflows tested
- [ ] Admin functionality verified
- [ ] Reports and analytics working
- [ ] No data integrity issues
- [ ] Performance meets baseline

## Emergency Contacts

### Primary Contacts
- **Operations Lead:** ops@cultivar.com, +1-555-0100
- **Backend Team Lead:** backend@cultivar.com, +1-555-0101
- **Database Engineer:** dba@cultivar.com, +1-555-0102

### Escalation Path
1. **Immediate Response:** Operations Lead
2. **Technical Support:** Backend Team Lead
3. **Management:** Engineering Manager
4. **Executive:** CTO

## Monitoring During Rollback

### Key Metrics to Monitor
```bash
# Service availability
curl -f http://localhost:5000/health | jq .status

# Error rates
tail -f /var/log/nginx/error.log | grep " 5[0-9][0-9] "

# Response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:5000/api/v1/plants

# Database connectivity
python scripts/monitor_db.py
```

### Alert Configuration During Rollback
- **Disable FastAPI alerts**
- **Enable Flask service alerts**
- **Monitor rollback completion alerts**
- **Watch for resource usage spikes**

## Post-Rollback Activities

### Immediate Actions (0-2 hours)
1. **Stabilize Flask service**
2. **Monitor performance metrics**
3. **Address any immediate issues**
4. **Prepare initial incident report**

### Short-term Actions (2-24 hours)
1. **Full root cause analysis**
2. **Impact assessment and reporting**
3. **Team debrief and lessons learned**
4. **Plan for future migration attempts**

### Long-term Actions (1-7 days)
1. **Security audit if security-related**
2. **Performance optimization**
3. **Enhanced monitoring and alerting**
4. **Migration strategy review and refinement**

## Rollback Time Estimates

| Phase | Duration | Total |
|-------|----------|-------|
| Traffic Redirection | 30 seconds | 30 seconds |
| Service Shutdown | 60 seconds | 90 seconds |
| Flask Restoration | 120 seconds | 210 seconds |
| Verification | 300 seconds | 510 seconds |
| **Total Estimated Time** | **~8.5 minutes** |

**Note:** Actual time may vary based on infrastructure complexity and issue severity.

## Rollback Success Criteria

Rollback is considered successful when:
- All user-facing functionality restored
- Performance metrics within acceptable ranges
- No data loss or corruption
- User experience restored to pre-migration levels
- No remaining critical alerts

## Lessons Learned Template

Use this template for post-rollback analysis:

```
Rollback Incident Report
========================

Incident ID: [INC-YYYYMMDD-HHMM]
Start Time: [Date/Time]
End Time: [Date/Time]
Duration: [Total Time]

Trigger Condition:
[What caused the rollback]

Root Cause:
[Technical root cause analysis]

Impact:
- Users affected: [Number]
- Duration of impact: [Time]
- Data integrity: [Status]

Resolution:
[What was done to resolve]

Prevention:
[What will be done to prevent recurrence]

Follow-up Actions:
[ ] Action item 1 - Owner - Due date
[ ] Action item 2 - Owner - Due date
```

## Rollback Prevention Measures

To reduce rollback frequency:
1. **Enhanced testing** in staging environment
2. **Gradual traffic migration** (blue-green deployment)
3. **Real-time monitoring** with automatic alerts
4. **Automated health checks** with fast response
5. **Regular rollback drills** for team readiness

---

**Document Status:** APPROVED  
**Next Review Date:** After any rollback event + 1 week  
**Distribution:** All engineering and operations team members