# Comprehensive Full Stack Audit Report

**Generated:** 2025-09-09T19:47:09.100430

## Executive Summary

- **Architecture:** 40 Python modules analyzed
- **Security:** Authentication system ✅ present
- **Code Quality:** Average cyclomatic complexity: 3.40
- **Testing:** 8 test files found

## Detailed Findings

### Architecture

```json
{
  "modules": {
    "total_modules": 40,
    "modules_by_type": {
      "root": 1,
      "handlers": 10,
      "utils": 6,
      "logger": 2,
      "config": 3,
      "routes": 2,
      "watcher": 2,
      "blueprints": 9,
      "models": 5
    },
    "cyclic_imports": [],
    "coupling_analysis": {},
    "cohesion_analysis": {}
  },
  "dependencies": {
    "direct_dependencies": 17,
    "vulnerability_count": 0,
    "outdated_packages": [],
    "security_analysis": {}
  },
  "patterns": {
    "factory_pattern": true,
    "singleton_pattern": false,
    "blueprint_pattern": true,
    "repository_pattern": false,
    "mvc_pattern": true
  },
  "database": {
    "model_count": 4,
    "table_relationships": {},
    "foreign_keys": 0,
    "indexes": [],
    "migrations": false
  },
  "api": {
    "endpoint_count": 62,
    "http_methods": {
      "POST": 16,
      "DELETE": 2,
      "GET": 11,
      "PUT": 1
    },
    "authentication_required": 0,
    "admin_only_endpoints": 0,
    "api_versioning": false,
    "error_handling": {}
  }
}
```

### Security

```json
{
  "auth": {
    "login_system": true,
    "session_management": false,
    "admin_protection": false,
    "password_hashing": true,
    "rate_limiting": true,
    "vulnerabilities": [
      "Potential hardcoded password in /home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
      "Potential hardcoded password in /home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/auth.py",
      "Potential hardcoded password in /home/runner/work/CultivAREmergent/CultivAREmergent/app/config/config.py",
      "Potential hardcoded password in /home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/admin.py",
      "Potential hardcoded password in /home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/auth.py"
    ]
  },
  "input_validation": {
    "validators_present": true,
    "form_validation": true,
    "api_validation": false,
    "sanitization": true,
    "missing_validation": []
  },
  "sql_injection": {
    "orm_usage": true,
    "raw_queries": [],
    "parameterized_queries": true,
    "vulnerabilities": []
  },
  "xss_protection": {
    "template_escaping": true,
    "csp_headers": true,
    "content_sanitization": false,
    "vulnerabilities": [
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/common/admin_base.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/common/base.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/common/sidebar.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/clones/lineage.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/clones/dashboard.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/clones/create.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/settings_functional.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/user_dashboard.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/graph.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/dashboard.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/settings.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/auth_placeholder.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/strains.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/sensors.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/add_breeder.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/cart.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/add_strain.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/admin_dashboard.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/simple_admin_dashboard.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/settings_old.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/dashboard_mobile.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/placeholder.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/plant.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/index.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/admin_users.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/new_login.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/plants.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/admin_test.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/strain.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/landing/index.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/admin/edit_user.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/admin/export.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/admin/create_user.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/auth/change_password.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/market/seed_bank.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/market/gear.html",
      "Potential XSS in /home/runner/work/CultivAREmergent/CultivAREmergent/app/web/templates/views/market/extensions.html"
    ]
  },
  "csrf_protection": {
    "csrf_tokens": false,
    "same_site_cookies": false,
    "vulnerabilities": []
  },
  "session_security": {
    "secure_cookies": false,
    "httponly_cookies": false,
    "session_timeout": false,
    "secure_secret_key": false
  },
  "file_upload": {
    "file_type_validation": false,
    "file_size_limits": true,
    "upload_path_security": false,
    "vulnerabilities": []
  },
  "dependencies": {
    "total_vulnerabilities": 0,
    "critical_vulnerabilities": 0,
    "vulnerable_packages": [],
    "packages_installed": 106
  }
}
```

### Code_Quality

```json
{
  "complexity": {
    "average_complexity": 3.3977900552486187,
    "high_complexity_functions": [
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "function": "record_activity",
        "complexity": 13
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/watcher/watcher.py",
        "function": "grab_streams",
        "complexity": 11
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/clones.py",
        "function": "create",
        "complexity": 11
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/auth.py",
        "function": "signup",
        "complexity": 11
      }
    ],
    "total_functions": 181,
    "lines_of_code": 6487
  },
  "code_smells": {
    "long_functions": [
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "function": "get_all_users",
        "lines": 59
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "function": "get_user_by_id",
        "lines": 53
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "function": "create_user",
        "lines": 73
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "function": "update_user",
        "lines": 51
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/sensor_handlers.py",
        "function": "scan_ac_infinity_sensors",
        "lines": 91
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/sensor_handlers.py",
        "function": "scan_ecowitt_sensors",
        "lines": 96
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "function": "get_plant",
        "lines": 118
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "function": "get_living_plants",
        "lines": 73
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "function": "get_harvested_plants",
        "lines": 52
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "function": "get_dead_plants",
        "lines": 56
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "function": "get_plants_by_strain",
        "lines": 76
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "function": "update_plant",
        "lines": 88
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "function": "upload_plant_images",
        "lines": 68
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "function": "record_activity",
        "lines": 69
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/activity_handlers.py",
        "function": "record_system_activity",
        "lines": 59
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "function": "export_plants_csv",
        "lines": 70
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "function": "export_strains_csv",
        "lines": 53
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "function": "export_complete_backup",
        "lines": 69
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "function": "export_sensors_csv",
        "lines": 56
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "function": "create_clones",
        "lines": 117
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "function": "get_clone_lineage",
        "lines": 97
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "function": "get_clone_statistics",
        "lines": 88
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/image.py",
        "function": "decorate_image",
        "lines": 52
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/routes/routes.py",
        "function": "register_basic_routes",
        "lines": 103
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/watcher/watcher.py",
        "function": "grab_streams",
        "lines": 52
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/clones.py",
        "function": "create",
        "lines": 56
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/auth.py",
        "function": "login",
        "lines": 60
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/auth.py",
        "function": "signup",
        "lines": 59
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/models/__init__.py",
        "function": "init_db",
        "lines": 58
      }
    ],
    "large_classes": [],
    "duplicate_code": [],
    "dead_code": [],
    "god_objects": []
  },
  "error_handling": {
    "try_catch_blocks": 93,
    "broad_exceptions": [
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 73
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 129
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 204
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 258
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 304
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 357
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 397
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 431
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/sensor_handlers.py",
        "line": 62
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/sensor_handlers.py",
        "line": 108
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/sensor_handlers.py",
        "line": 161
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/sensor_handlers.py",
        "line": 254
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/sensor_handlers.py",
        "line": 353
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/sensor_handlers.py",
        "line": 384
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/sensor_handlers.py",
        "line": 414
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 148
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 224
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 279
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 338
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 417
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 467
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 558
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 610
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 644
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 715
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 747
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 819
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/activity_handlers.py",
        "line": 72
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/activity_handlers.py",
        "line": 116
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/activity_handlers.py",
        "line": 154
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/activity_handlers.py",
        "line": 208
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "line": 98
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "line": 154
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "line": 199
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "line": 246
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "line": 276
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "line": 302
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "line": 374
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "line": 433
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "line": 462
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/settings_handlers.py",
        "line": 52
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/settings_handlers.py",
        "line": 70
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/settings_handlers.py",
        "line": 97
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/settings_handlers.py",
        "line": 116
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/settings_handlers.py",
        "line": 152
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/settings_handlers.py",
        "line": 181
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/settings_handlers.py",
        "line": 219
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/breeder_handlers.py",
        "line": 28
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/breeder_handlers.py",
        "line": 57
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/breeder_handlers.py",
        "line": 95
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/breeder_handlers.py",
        "line": 129
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 57
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 176
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 277
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 360
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 408
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 453
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 140
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/strain_handlers.py",
        "line": 46
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/strain_handlers.py",
        "line": 86
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/strain_handlers.py",
        "line": 126
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/strain_handlers.py",
        "line": 161
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/strain_handlers.py",
        "line": 201
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/strain_handlers.py",
        "line": 236
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/helpers.py",
        "line": 103
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/image.py",
        "line": 40
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/image.py",
        "line": 95
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/auth.py",
        "line": 45
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/logger/logger.py",
        "line": 35
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/logger/logger.py",
        "line": 27
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/config/load_config.py",
        "line": 57
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/routes/routes.py",
        "line": 100
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/watcher/watcher.py",
        "line": 33
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/watcher/watcher.py",
        "line": 68
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/watcher/watcher.py",
        "line": 123
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/watcher/watcher.py",
        "line": 115
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/dashboard.py",
        "line": 52
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/dashboard.py",
        "line": 109
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/strains.py",
        "line": 46
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/strains.py",
        "line": 108
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/admin.py",
        "line": 255
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/admin.py",
        "line": 291
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/admin.py",
        "line": 316
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/admin.py",
        "line": 341
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/admin.py",
        "line": 366
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/admin.py",
        "line": 391
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/admin.py",
        "line": 455
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/diagnostics.py",
        "line": 33
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/diagnostics.py",
        "line": 41
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/auth.py",
        "line": 157
      }
    ],
    "unhandled_exceptions": [],
    "logging_in_exceptions": 0
  },
  "logging": {
    "logger_configured": true,
    "log_levels_used": [
      "error",
      "info",
      "warning"
    ],
    "logging_in_functions": 125,
    "security_logging": false
  },
  "style": {
    "pep8_violations": 0,
    "line_length_violations": [
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 29,
        "length": 84
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 122,
        "length": 82
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 139,
        "length": 89
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 156,
        "length": 80
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 168,
        "length": 106
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 169,
        "length": 85
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 174,
        "length": 86
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 240,
        "length": 81
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 283,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 287,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 291,
        "length": 90
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 303,
        "length": 84
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 331,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 344,
        "length": 110
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "line": 351,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/sensor_handlers.py",
        "line": 52,
        "length": 88
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/sensor_handlers.py",
        "line": 133,
        "length": 88
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/sensor_handlers.py",
        "line": 150,
        "length": 82
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/sensor_handlers.py",
        "line": 180,
        "length": 82
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/sensor_handlers.py",
        "line": 202,
        "length": 82
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/sensor_handlers.py",
        "line": 226,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/sensor_handlers.py",
        "line": 232,
        "length": 85
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 114,
        "length": 88
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 181,
        "length": 80
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 194,
        "length": 81
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 205,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 254,
        "length": 81
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 265,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 315,
        "length": 81
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 326,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 373,
        "length": 80
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 386,
        "length": 81
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 397,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 501,
        "length": 82
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 669,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 758,
        "length": 82
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 770,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 795,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "line": 797,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/activity_handlers.py",
        "line": 40,
        "length": 105
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/activity_handlers.py",
        "line": 42,
        "length": 93
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/activity_handlers.py",
        "line": 46,
        "length": 81
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "line": 17,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "line": 194,
        "length": 85
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "line": 317,
        "length": 80
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "line": 342,
        "length": 80
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "line": 370,
        "length": 85
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "line": 448,
        "length": 88
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "line": 452,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "line": 453,
        "length": 88
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/settings_handlers.py",
        "line": 14,
        "length": 92
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/settings_handlers.py",
        "line": 37,
        "length": 82
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/settings_handlers.py",
        "line": 41,
        "length": 81
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/settings_handlers.py",
        "line": 45,
        "length": 80
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/settings_handlers.py",
        "line": 46,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/settings_handlers.py",
        "line": 48,
        "length": 86
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/settings_handlers.py",
        "line": 142,
        "length": 82
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/settings_handlers.py",
        "line": 143,
        "length": 80
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/settings_handlers.py",
        "line": 145,
        "length": 86
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/settings_handlers.py",
        "line": 176,
        "length": 82
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/breeder_handlers.py",
        "line": 45,
        "length": 81
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/breeder_handlers.py",
        "line": 47,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/breeder_handlers.py",
        "line": 56,
        "length": 80
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/breeder_handlers.py",
        "line": 82,
        "length": 85
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/breeder_handlers.py",
        "line": 121,
        "length": 105
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 22,
        "length": 81
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 23,
        "length": 89
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 36,
        "length": 80
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 47,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 127,
        "length": 81
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 151,
        "length": 93
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 161,
        "length": 105
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 202,
        "length": 80
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 216,
        "length": 82
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 219,
        "length": 82
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 250,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 268,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 316,
        "length": 82
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 327,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 389,
        "length": 80
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 390,
        "length": 80
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 395,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 401,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "line": 451,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/strain_handlers.py",
        "line": 228,
        "length": 88
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/helpers.py",
        "line": 203,
        "length": 99
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/image.py",
        "line": 20,
        "length": 89
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/image.py",
        "line": 45,
        "length": 86
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/image.py",
        "line": 54,
        "length": 93
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/image.py",
        "line": 91,
        "length": 104
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/validators.py",
        "line": 12,
        "length": 81
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/validators.py",
        "line": 34,
        "length": 91
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/validators.py",
        "line": 59,
        "length": 156
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/validators.py",
        "line": 95,
        "length": 92
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/validators.py",
        "line": 98,
        "length": 97
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/validators.py",
        "line": 141,
        "length": 100
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/validators.py",
        "line": 178,
        "length": 80
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/validators.py",
        "line": 202,
        "length": 80
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/validators.py",
        "line": 203,
        "length": 95
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/validators.py",
        "line": 251,
        "length": 84
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/utils/rate_limiter.py",
        "line": 9,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/logger/logger.py",
        "line": 15,
        "length": 85
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/logger/logger.py",
        "line": 32,
        "length": 82
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/config/load_config.py",
        "line": 7,
        "length": 82
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/config/load_config.py",
        "line": 22,
        "length": 88
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/config/config.py",
        "line": 45,
        "length": 81
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/config/config.py",
        "line": 90,
        "length": 108
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/config/config.py",
        "line": 115,
        "length": 85
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/config/config.py",
        "line": 118,
        "length": 120
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/config/config.py",
        "line": 120,
        "length": 124
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/routes/routes.py",
        "line": 42,
        "length": 94
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/routes/routes.py",
        "line": 97,
        "length": 85
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/watcher/watcher.py",
        "line": 13,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/watcher/watcher.py",
        "line": 42,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/watcher/watcher.py",
        "line": 84,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/watcher/watcher.py",
        "line": 102,
        "length": 84
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/watcher/watcher.py",
        "line": 105,
        "length": 88
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/watcher/watcher.py",
        "line": 106,
        "length": 84
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/watcher/watcher.py",
        "line": 110,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/watcher/watcher.py",
        "line": 113,
        "length": 105
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/watcher/watcher.py",
        "line": 116,
        "length": 81
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/dashboard.py",
        "line": 2,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/dashboard.py",
        "line": 5,
        "length": 108
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/dashboard.py",
        "line": 28,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/dashboard.py",
        "line": 29,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/dashboard.py",
        "line": 75,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/dashboard.py",
        "line": 99,
        "length": 88
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/strains.py",
        "line": 5,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/strains.py",
        "line": 25,
        "length": 89
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/strains.py",
        "line": 39,
        "length": 156
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/strains.py",
        "line": 40,
        "length": 128
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/strains.py",
        "line": 80,
        "length": 85
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/strains.py",
        "line": 98,
        "length": 151
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/strains.py",
        "line": 119,
        "length": 81
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/strains.py",
        "line": 128,
        "length": 81
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/breeders.py",
        "line": 8,
        "length": 81
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/admin.py",
        "line": 86,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/admin.py",
        "line": 119,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/admin.py",
        "line": 135,
        "length": 80
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/admin.py",
        "line": 219,
        "length": 84
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/admin.py",
        "line": 253,
        "length": 86
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/admin.py",
        "line": 289,
        "length": 86
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/admin.py",
        "line": 454,
        "length": 85
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/admin.py",
        "line": 457,
        "length": 80
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/admin.py",
        "line": 626,
        "length": 104
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/admin.py",
        "line": 650,
        "length": 84
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/clones.py",
        "line": 5,
        "length": 88
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/clones.py",
        "line": 23,
        "length": 80
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/clones.py",
        "line": 62,
        "length": 107
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/clones.py",
        "line": 114,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/diagnostics.py",
        "line": 44,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/auth.py",
        "line": 5,
        "length": 88
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/auth.py",
        "line": 13,
        "length": 93
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/auth.py",
        "line": 33,
        "length": 89
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/auth.py",
        "line": 41,
        "length": 84
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/auth.py",
        "line": 43,
        "length": 112
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/auth.py",
        "line": 46,
        "length": 88
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/auth.py",
        "line": 50,
        "length": 82
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/auth.py",
        "line": 63,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/auth.py",
        "line": 97,
        "length": 80
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/auth.py",
        "line": 103,
        "length": 82
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/auth.py",
        "line": 117,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/auth.py",
        "line": 139,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/models/base_models.py",
        "line": 51,
        "length": 85
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/models/base_models.py",
        "line": 76,
        "length": 81
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/models/base_models.py",
        "line": 99,
        "length": 81
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/models/base_models.py",
        "line": 119,
        "length": 82
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/models/base_models.py",
        "line": 143,
        "length": 88
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/models/base_models.py",
        "line": 191,
        "length": 81
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/models/base_models.py",
        "line": 199,
        "length": 88
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/models/base_models.py",
        "line": 210,
        "length": 81
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/models/system_models.py",
        "line": 25,
        "length": 87
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/models/__init__.py",
        "line": 58,
        "length": 80
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/models/__init__.py",
        "line": 85,
        "length": 83
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/models/__init__.py",
        "line": 100,
        "length": 88
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/models/acinfinity_models.py",
        "line": 24,
        "length": 80
      }
    ],
    "naming_violations": [],
    "import_violations": []
  }
}
```

### Performance

```json
{
  "database_queries": {
    "total_queries": 156,
    "joins_used": 24,
    "potential_n_plus_one": [],
    "missing_indexes": []
  },
  "n_plus_one": {
    "potential_issues": [
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/dashboard.py",
        "line": 26,
        "content": "for plant in plants_query:"
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/dashboard.py",
        "line": 48,
        "content": "strains = [{'id': s.id, 'name': s.name} for s in Strain.query.all()]"
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/dashboard.py",
        "line": 49,
        "content": "zones = [z.name for z in Zone.query.all()]"
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/dashboard.py",
        "line": 50,
        "content": "statuses = [s.name for s in Status.query.all()]"
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/strains.py",
        "line": 23,
        "content": "for strain in strains_query:"
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/strains.py",
        "line": 44,
        "content": "breeders = [{'id': b.id, 'name': b.name} for b in Breeder.query.all()]"
      }
    ],
    "loop_queries": []
  },
  "memory": {
    "large_data_operations": [
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/user_handlers.py",
        "operation": "query.all() - loads all records"
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/sensor_handlers.py",
        "operation": "query.all() - loads all records"
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/plant_handlers.py",
        "operation": "query.all() - loads all records"
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/activity_handlers.py",
        "operation": "query.all() - loads all records"
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/export_handlers.py",
        "operation": "query.all() - loads all records"
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/settings_handlers.py",
        "operation": "query.all() - loads all records"
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/breeder_handlers.py",
        "operation": "query.all() - loads all records"
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/clone_handlers.py",
        "operation": "query.all() - loads all records"
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/handlers/strain_handlers.py",
        "operation": "query.all() - loads all records"
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/config/load_config.py",
        "operation": "query.all() - loads all records"
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/watcher/watcher.py",
        "operation": "query.all() - loads all records"
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/dashboard.py",
        "operation": "query.all() - loads all records"
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/strains.py",
        "operation": "query.all() - loads all records"
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/admin.py",
        "operation": "query.all() - loads all records"
      },
      {
        "file": "/home/runner/work/CultivAREmergent/CultivAREmergent/app/blueprints/clones.py",
        "operation": "query.all() - loads all records"
      }
    ],
    "memory_leaks": [],
    "inefficient_operations": []
  },
  "caching": {
    "caching_implemented": false,
    "cache_types": [],
    "cache_strategies": []
  }
}
```

### Testing

```json
{
  "coverage": {
    "test_files": 8,
    "unit_tests": 22,
    "integration_tests": 0,
    "test_framework": null
  },
  "quality": {
    "assertion_count": 0,
    "test_coverage_percentage": 0,
    "test_isolation": true,
    "test_data_management": false
  },
  "types": {
    "unit_tests": false,
    "integration_tests": false,
    "security_tests": true,
    "performance_tests": false,
    "ui_tests": false
  }
}
```

### Documentation

```json
{
  "api": {
    "swagger_docs": false,
    "endpoint_documentation": 0,
    "examples_provided": false
  },
  "code": {
    "docstring_coverage": 91.16022099447514,
    "comment_ratio": 5.934946816710344,
    "outdated_comments": []
  },
  "user": {
    "readme_present": true,
    "installation_guide": true,
    "user_manual": false,
    "api_guide": false
  }
}
```

### Infrastructure

```json
{
  "containerization": {
    "dockerfile_present": true,
    "docker_compose": true,
    "multi_stage_build": false,
    "security_scanning": false
  },
  "environment": {
    "env_file_present": false,
    "config_externalized": false,
    "secrets_management": false
  },
  "deployment": {
    "gunicorn_config": true,
    "nginx_config": false,
    "ci_cd_pipeline": true,
    "health_checks": false
  }
}
```

### Compliance

```json
{}
```

## Prioritized Recommendations

### Critical Priority

1. **Fix hardcoded passwords** - Remove all hardcoded credentials

### High Priority

3. **Reduce code complexity** - 4 functions with high complexity

### Medium Priority

5. **Documentation updates** - Update outdated documentation
6. **Performance optimization** - Address N+1 queries and memory usage
