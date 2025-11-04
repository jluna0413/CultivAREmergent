# Flask Decommission Checklist

## Overview
This document provides a comprehensive checklist for safely removing legacy Flask files and dependencies after confirming full API parity with FastAPI implementation.

**⚠️ CRITICAL WARNING: Only proceed with Flask decommission after 100% API parity is confirmed and all functionality is tested and verified.**

## Pre-Decommission Verification Checklist

### ✅ Phase 1: API Parity Verification
- [ ] **Run comprehensive API parity tests** - All Flask endpoints have FastAPI equivalents
- [ ] **Verify authentication system parity** - JWT vs Flask-Login functionality confirmed
- [ ] **Test all CRUD operations** - Plants, strains, breeders, clones, zones
- [ ] **Verify admin functionality** - All admin operations work in FastAPI
- [ ] **Test marketing endpoints** - Blog, newsletter, social features
- [ ] **Confirm database operations** - All models work with async SQLAlchemy
- [ ] **Verify file upload functionality** - Images and documents work correctly
- [ ] **Test rate limiting** - FastAPI limiter provides same protection
- [ ] **Confirm security headers** - All CSP and security policies work
- [ ] **Validate rate limiting** - DDoS protection active and functional

### ✅ Phase 2: Performance & Load Testing
- [ ] **Run load tests on FastAPI endpoints** - Confirm performance is equal or better
- [ ] **Test concurrent user scenarios** - Multiple simultaneous users supported
- [ ] **Verify database connection handling** - Async operations stable under load
- [ ] **Test response times** - FastAPI responses meet performance criteria
- [ ] **Monitor memory usage** - Async SQLAlchemy efficient under load

### ✅ Phase 3: Integration Testing
- [ ] **Test IoT device integrations** - Ecowitt and ACInfinity connections work
- [ ] **Verify third-party integrations** - External API calls function properly
- [ ] **Test webhook endpoints** - All webhook handlers work in FastAPI
- [ ] **Confirm background tasks** - Async tasks complete successfully
- [ ] **Test file serving** - Static files and uploads served correctly

## Flask Files to Remove

### 🗑️ Core Flask Application Files
- [ ] **Remove `cultivar_app.py`** - Main Flask application factory
- [ ] **Remove `app/routes/routes.py`** - Flask route definitions
- [ ] **Remove `app/routes/__init__.py`** - Routes package init

### 🗑️ Flask Blueprint Modules
**Directory: `app/blueprints/`**
- [ ] **Remove `admin.py`** - Admin functionality blueprint
- [ ] **Remove `auth.py`** - Authentication blueprint
- [ ] **Remove `breeders.py`** - Breeder management blueprint
- [ ] **Remove `clones.py`** - Clone management blueprint
- [ ] **Remove `dashboard.py`** - Dashboard blueprint
- [ ] **Remove `diagnostics.py`** - Diagnostics blueprint
- [ ] **Remove `market.py`** - Market functionality blueprint
- [ ] **Remove `marketing.py`** - Marketing features blueprint
- [ ] **Remove `newsletter.py`** - Newsletter blueprint
- [ ] **Remove `social.py`** - Social features blueprint
- [ ] **Remove `strains.py`** - Strain management blueprint
- [ ] **Remove `__init__.py`** - Blueprints package init

### 🗑️ Flask Utility Modules
**Directory: `app/utils/`**
- [ ] **Remove `auth.py`** - Flask-specific auth utilities
- [ ] **Remove `helpers.py`** - Flask template helpers
- [ ] **Remove `image.py`** - Flask image processing utilities
- [ ] **Remove `rate_limiter.py`** - Flask-Limiter configuration
- [ ] **Remove `validators.py`** - Flask form validators
- [ ] **Remove `__init__.py`** - Utils package init

### 🗑️ Legacy Flask Directories (if any)
- [ ] **Remove `flask_legacy_archive/`** - Any archived Flask components
- [ ] **Remove any remaining Flask-specific templates** in `app/web/templates/`
- [ ] **Remove Flask-specific static files** in `app/web/static/`

## Dependencies Removal

### 📦 Requirements.txt Updates
**File: `requirements.txt`**

Remove the following Flask dependencies:
- [ ] **Remove `Flask==3.1.1`** - Core Flask framework
- [ ] **Remove `Flask-SQLAlchemy==3.1.1`** - Flask SQLAlchemy integration
- [ ] **Remove `Flask-Login==0.6.3`** - Flask authentication extension
- [ ] **Remove `Werkzeug==3.1.0`** - WSGI utilities (keep only if other tools need it)

**Note**: Keep `Jinja2==3.1.6` as it's used by FastAPI for templating

### 📦 Update requirements_fastapi.txt (if separate)
- [ ] **Ensure FastAPI requirements are complete** and don't reference Flask
- [ ] **Verify all FastAPI dependencies are in main requirements.txt**

## Infrastructure Changes

### 🐳 Container Updates
**Files to check and update:**
- [ ] **Update `Dockerfile`** - Remove Flask-specific commands
- [ ] **Remove Flask startup commands** - Eliminate `python cultivar_app.py`
- [ ] **Ensure only FastAPI server starts** - `uvicorn app.fastapi_app:app`
- [ ] **Update health checks** - Point to FastAPI endpoints

### 🔧 Docker Compose Updates
**File: `docker-compose.yml`**
- [ ] **Update service command** - Change from Flask to FastAPI startup
- [ ] **Update ports if necessary** - Ensure FastAPI port configuration
- [ ] **Remove Flask environment variables** - Clean up unused Flask config
- [ ] **Update health check endpoints** - Point to FastAPI health endpoints

### 🌐 Nginx Configuration Updates
**Files to check:**
- [ ] **Update Nginx config** - Proxy to FastAPI instead of Flask
- [ ] **Remove Flask-specific headers** - Clean up Flask-related proxy headers
- [ ] **Update WebSocket proxying** - Ensure FastAPI WebSocket support
- [ ] **Update static file serving** - Confirm static files work with FastAPI

### ⚙️ Environment Configuration
- [ ] **Remove Flask-specific environment variables**
  - `FLASK_APP`
  - `FLASK_ENV`
  - `FLASK_DEBUG`
- [ ] **Keep only FastAPI environment variables**
  - `FASTAPI_HOST`
  - `FASTAPI_PORT`
  - `CULTIVAR_PORT` (if used by FastAPI)

## Deployment Updates

### 📋 CI/CD Pipeline Updates
- [ ] **Update GitHub Actions workflows** - Remove Flask deployment steps
- [ ] **Update deployment scripts** - Point to FastAPI startup commands
- [ ] **Update testing pipelines** - Remove Flask-specific tests
- [ ] **Update deployment verification** - Check FastAPI endpoints only

### 📊 Monitoring & Logging
- [ ] **Update application monitoring** - Monitor FastAPI endpoints
- [ ] **Update log aggregation** - Remove Flask-specific log patterns
- [ ] **Update health check URLs** - Point to FastAPI health endpoints
- [ ] **Update metrics collection** - Monitor FastAPI-specific metrics

## Safety Verification Steps

### 🧪 Post-Decommission Testing
**After Flask removal, verify:**

#### Core Functionality Tests
- [ ] **Homepage loads correctly** - Marketing site accessible
- [ ] **User authentication works** - Login/logout functionality
- [ ] **Admin panel accessible** - All admin features work
- [ ] **Dashboard loads** - User dashboard displays correctly
- [ ] **CRUD operations work** - All create/read/update/delete operations
- [ ] **File uploads function** - Image uploads and processing work
- [ ] **API endpoints respond** - All FastAPI endpoints accessible
- [ ] **Database connections active** - No connection errors
- [ ] **Rate limiting effective** - DDoS protection active
- [ ] **Security headers present** - CSP and security policies active

#### Integration Tests
- [ ] **IoT devices connect** - Ecowitt and ACInfinity integrations
- [ ] **External API calls work** - Third-party service integrations
- [ ] **Background tasks run** - Async operations complete
- [ ] **Email notifications send** - Newsletter and notifications
- [ ] **File downloads work** - Lead magnet downloads
- [ ] **Search functionality works** - Blog and content search

### 🔍 Code Verification
- [ ] **No Flask imports remain** - Search codebase for remaining Flask imports
- [ ] **No Flask references in comments** - Clean up documentation
- [ ] **FastAPI imports complete** - All dependencies properly imported
- [ ] **Type hints updated** - Remove Flask-specific type references

## Rollback Plan

### ⚠️ Emergency Rollback Procedure
**If issues are discovered after Flask decommission:**

1. **Immediate Actions**
   - [ ] Stop FastAPI server
   - [ ] Restore Flask server from backup
   - [ ] Update Nginx to point to Flask
   - [ ] Notify team of rollback

2. **Re-enable Flask Components**
   - [ ] Restore Flask files from git history
   - [ ] Restore Flask dependencies in requirements.txt
   - [ ] Restart Flask application
   - [ ] Verify all functionality

3. **Post-Rollback Analysis**
   - [ ] Document issues discovered
   - [ ] Update FastAPI implementation
   - [ ] Plan re-decommission attempt
   - [ ] Update testing procedures

## Sign-off Checklist

### ✅ Final Approval Required
**Before Flask decommission, obtain sign-off from:**

- [ ] **Lead Developer** - Code review and architectural approval
- [ ] **QA Engineer** - Full test suite passed
- [ ] **DevOps Engineer** - Infrastructure changes approved
- [ ] **Project Manager** - Timeline and risk assessment approved
- [ ] **Security Team** - Security review completed
- [ ] **Product Owner** - Business functionality verified

### 📝 Documentation Updates
- [ ] **Update README.md** - Remove Flask setup instructions
- [ ] **Update deployment docs** - FastAPI deployment only
- [ ] **Update API documentation** - Remove Flask endpoints
- [ ] **Update developer guide** - FastAPI development setup
- [ ] **Update architecture diagrams** - Remove Flask components

## Completion Verification

### ✅ Final Checks
- [ ] **All Flask files removed** from codebase
- [ ] **Flask dependencies removed** from requirements.txt
- [ ] **Infrastructure updated** to serve FastAPI only
- [ ] **All tests passing** with FastAPI implementation
- [ ] **Performance equal or better** than Flask version
- [ ] **Security measures active** and verified
- [ ] **Documentation updated** to reflect changes
- [ ] **Team notified** of successful decommission

---

## Important Notes

⚠️ **CRITICAL REMINDERS:**

1. **Never remove Flask without full backup** - Keep git history accessible
2. **Test thoroughly in staging** - Never decommission directly in production
3. **Plan for gradual rollout** - Consider feature flags during transition
4. **Monitor closely after decommission** - Watch for unexpected issues
5. **Keep rollback plan ready** - Be prepared to revert if necessary

✅ **SUCCESS CRITERIA:**
- 100% API parity with Flask version
- All tests passing in staging environment
- Performance equal or better than Flask
- No Flask dependencies remaining
- Team sign-off obtained
- Rollback plan tested and ready

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-31  
**Next Review:** After Flask decommission completion  
**Owner:** CultivAR Development Team