# CultivAR MVP Deployment Checklist

## Pre-Deployment Tasks

### Code Review
- [ ] All "clone of Isley" references removed
- [ ] Copyright notices updated to "© 2025 CultivAR - By Eye Heart Hemp"
- [ ] Hardcoded credentials removed
- [ ] Debug logging statements removed or disabled
- [ ] Console.log statements cleaned up

### Testing
- [ ] All test cases in the test plan executed
- [ ] Critical bugs fixed
- [ ] Cross-browser testing completed (Chrome, Firefox, Safari)
- [ ] Mobile responsiveness verified
- [ ] API endpoints tested with tools like Postman or Swagger UI

### Documentation
- [ ] Beta testing guide completed
- [ ] Known issues documented
- [ ] User feedback mechanism implemented
- [ ] API documentation generated and reviewed

### Database
- [ ] Database schema finalized
- [ ] **Alembic migrations generated** (`alembic revision --autogenerate -m "description of changes"`)
- [ ] **Alembic migrations applied to staging/test DB** (`alembic upgrade head`)
- [ ] **Migration status verified** (`alembic current`)
- [ ] Initial data seeded (if needed)
- [ ] Database backup procedure documented

### Security
- [ ] Authentication system tested (JWT, token refresh, logout)
- [ ] Password policies enforced
- [ ] Admin access restricted and tested
- [ ] Input validation implemented for all API endpoints
- [ ] CORS and Trusted Host middleware configured correctly

## Deployment Tasks

### Environment Setup
- [ ] Server provisioned (e.g., EC2, DigitalOcean Droplet)
- [ ] Domain configured
- [ ] SSL certificate installed and configured (e.g., with Nginx or Traefik)
- [ ] Firewall configured to allow traffic on ports 80 and 443

### Application Deployment
- [ ] Code deployed to server (e.g., via git pull)
- [ ] **Python dependencies installed**: `pip install -r requirements.txt`
- [ ] Environment variables configured on the server (`.env` file or system-level)
- [ ] **Database migrations run in production**: `alembic upgrade head`
- [ ] **Migration success verified**: `alembic current`
- [ ] **FastAPI server started**: `uvicorn app.fastapi_app:app --host 0.0.0.0 --port 8000` (preferably run with a process manager like systemd or gunicorn)
- [ ] Web server (Nginx, Traefik) configured to proxy requests to the Uvicorn server

### Monitoring
- [ ] Logging configured (e.g., sending logs to a centralized service)
- [ ] Error tracking set up (e.g., Sentry)
- [ ] Performance monitoring enabled (e.g., Prometheus, Grafana)

## Post-Deployment Tasks

### Verification
- [ ] Application accessible at the correct URL
- [ ] API health check endpoint (`/health`) returns a 200 OK status
- [ ] Login functionality works via the API
- [ ] Core API features tested in production
- [ ] No server errors in logs after startup

### Beta Tester Onboarding
- [ ] Beta tester accounts created
- [ ] Welcome emails sent with login credentials and API usage examples
- [ ] Beta testing guide distributed
- [ ] Support contact information provided

### Feedback Collection
- [ ] Feedback form implemented
- [ ] Issue tracking system set up
- [ ] Beta tester communication channel established

## Rollback Plan

In case of critical issues:

1. Identify the issue and its severity.
2. If severity is high:
   - Notify beta testers of the issue.
   - Revert the deployment to the previous stable version.
   - Restore the database from the pre-deployment backup if migrations were faulty.
   - Fix the issue in a development environment.
   - Re-deploy when the fix is verified.
3. If severity is low:
   - Document as a known issue.
   - Plan a hotfix or include the fix in the next scheduled deployment.
