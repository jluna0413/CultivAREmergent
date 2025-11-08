#!/usr/bin/env python3
"""
Task-Master-AI initialization script for CultivAR Migration Project.
Creates all task files and directory structure for the cultivar migration.
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
TASKMASTER_DIR = PROJECT_ROOT / ".taskmaster"
TASKS_DIR = TASKMASTER_DIR / "tasks"
REPORTS_DIR = TASKMASTER_DIR / "reports"

def create_directory_structure():
    """Create Task-Master directory structure."""
    directories = [
        TASKMASTER_DIR,
        TASKS_DIR,
        REPORTS_DIR,
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)
        print(f"Created directory: {directory}")

def create_master_task():
    """Create the master migration task."""
    task_data = {
        "id": "cultivar-migration-master",
        "title": "Complete Cultivar Terminology Migration",
        "description": "Systematic migration of all 'strain' terminology to 'cultivar' across 100+ files in backend, frontend, templates, tests, and documentation",
        "status": "TODO",
        "priority": "HIGH",
        "type": "EPIC",
        "estimated_effort_hours": 40,
        "actual_effort_hours": None,
        "parent_task_id": None,
        "dependencies": [],
        "blocking": [],
        "subtasks": [
            "phase-1-backend-models",
            "phase-2-api-layer", 
            "phase-3-frontend-flutter",
            "phase-4-templates-js",
            "phase-5-tests",
            "phase-6-documentation",
            "phase-7-validation"
        ],
        "assignee": "@traycerai",
        "tags": ["migration", "terminology", "refactoring", "breaking-change"],
        "milestone": "v2.0 - Cultivar Standardization",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "started_at": None,
        "completed_at": None,
        "files_affected": [],
        "acceptance_criteria": [
            "All backend models use `Cultivar` class",
            "All API endpoints use `/cultivars/*` paths (with `/strains/*` deprecated aliases)",
            "All Flutter code uses `Cultivar` terminology",
            "All templates use \"Cultivar\" in UI text",
            "All tests pass with new terminology",
            "All documentation updated",
            "Backward compatibility verified",
            "Migration validation script passes 100%"
        ],
        "notes": "Root task for comprehensive cultivar terminology migration",
        "linear_issue_id": None
    }
    
    task_file = TASKS_DIR / "cultivar_migration_master.json"
    with open(task_file, 'w', encoding='utf-8') as f:
        json.dump(task_data, f, indent=2, ensure_ascii=False)
    
    print(f"Created master task: {task_file}")

def create_phase_tasks():
    """Create all phase tasks."""
    phases = [
        {
            "id": "phase-1-backend-models",
            "title": "Phase 1: Migrate Backend Models (Cultivar)",
            "description": "Rename Strain class to Cultivar in Flask models, update Plant model foreign keys, add backward compatibility aliases",
            "estimated_effort_hours": 4,
            "blocking": ["phase-2-api-layer"],
            "subtasks": [
                "task-1-1-base-models-rename",
                "task-1-2-models-init-update",
                "task-1-3-config-loader-update",
                "task-1-4-config-class-update",
                "task-1-5-activity-model-update"
            ],
            "files_affected": [
                "app/models/base_models.py",
                "app/models/__init__.py"
            ]
        },
        {
            "id": "phase-2-api-layer",
            "title": "Phase 2: Migrate API Layer (Routers, Schemas, Handlers)",
            "description": "Rename strains.py→cultivars.py for routers and schemas, update all Pydantic models, rename handler modules, implement dual-mounting for backward compatibility",
            "estimated_effort_hours": 8,
            "dependencies": ["phase-1-backend-models"],
            "blocking": ["phase-3-frontend-flutter"],
            "subtasks": [
                "task-2-1-pydantic-schemas-rename",
                "task-2-2-fastapi-router-rename",
                "task-2-3-fastapi-init-update",
                "task-2-4-handler-sync-rename",
                "task-2-5-handler-async-rename",
                "task-2-6-activity-handlers-update",
                "task-2-7-activity-router-update",
                "task-2-8-activity-pydantic-update",
                "task-2-9-flask-blueprint-rename",
                "task-2-10-blueprint-init-update",
                "task-2-11-cultivar-app-update",
                "task-2-12-breeder-router-update",
                "task-2-13-breeder-pydantic-update"
            ],
            "files_affected": [
                "app/fastapi_app/routers/strains.py",
                "app/fastapi_app/models/strains.py",
                "app/handlers/strain_handlers.py",
                "app/blueprints/strains.py"
            ]
        },
        {
            "id": "phase-3-frontend-flutter",
            "title": "Phase 3: Migrate Flutter Frontend (Models, Providers, Widgets)",
            "description": "Consolidate duplicate providers/widgets, update all Dart code to use 'cultivar' terminology, align models with backend schema",
            "estimated_effort_hours": 6,
            "dependencies": ["phase-2-api-layer"],
            "blocking": ["phase-4-templates-js"],
            "subtasks": [
                "task-3-1-consolidate-providers",
                "task-3-2-consolidate-widgets",
                "task-3-3-cultivars-screen-update",
                "task-3-4-api-client-verify",
                "task-3-5-cultivars-service-verify",
                "task-3-6-cultivar-models-align",
                "task-3-7-cultivar-model-verify",
                "task-3-8-plant-models-update",
                "task-3-9-create-plant-request-update"
            ],
            "files_affected": [
                "flutter_app/lib/core/state/strains_provider.dart",
                "flutter_app/lib/core/providers/cultivar_provider.dart",
                "flutter_app/lib/screens/cultivars_screen.dart"
            ]
        },
        {
            "id": "phase-4-templates-js",
            "title": "Phase 4: Migrate Templates and JavaScript",
            "description": "Rename HTML templates, update all user-facing text from 'Strains' to 'Cultivars', update JavaScript functions and AJAX endpoints",
            "estimated_effort_hours": 6,
            "dependencies": ["phase-3-frontend-flutter"],
            "blocking": ["phase-5-tests"],
            "subtasks": [
                "task-4-1-strains-template-rename",
                "task-4-2-cultivar-template-rename",
                "task-4-3-add-cultivar-template-rename",
                "task-4-4-add-breeder-template-update",
                "task-4-5-plants-template-update",
                "task-4-6-plant-template-update",
                "task-4-7-dashboard-template-update",
                "task-4-8-clone-create-template-update",
                "task-4-9-clone-dashboard-template-update",
                "task-4-10-clone-lineage-template-update",
                "task-4-11-sidebar-template-update",
                "task-4-12-admin-export-template-update",
                "task-4-13-main-js-update",
                "task-4-14-strains-diagnostics-rename",
                "task-4-15-dashboard-widgets-update",
                "task-4-16-diagnostics-js-update"
            ],
            "files_affected": [
                "app/web/templates/views/strains.html",
                "app/web/static/js/main.js"
            ]
        },
        {
            "id": "phase-5-tests",
            "title": "Phase 5: Migrate Test Suite",
            "description": "Update all test files, test data, assertions, and test descriptions to use 'cultivar' terminology",
            "estimated_effort_hours": 5,
            "dependencies": ["phase-4-templates-js"],
            "blocking": ["phase-6-documentation"],
            "subtasks": [
                "task-5-1-plant-card-test-update",
                "task-5-2-plant-models-test-update",
                "task-5-3-model-test-update",
                "task-5-4-providers-integration-test-update",
                "task-5-5-plants-integration-test-update",
                "task-5-6-plants-integration-py-test-update",
                "task-5-7-strains-test-rename",
                "task-5-8-strains-integration-test-rename",
                "task-5-9-router-fixes-test-update",
                "task-5-10-verify-router-script-update",
                "task-5-11-verify-simple-script-update"
            ],
            "files_affected": [
                "tests/integration/test_strains.py",
                "flutter_app/test/widget/plant_card_test.dart"
            ]
        },
        {
            "id": "phase-6-documentation",
            "title": "Phase 6: Migrate Documentation",
            "description": "Update all markdown files, API documentation, user guides, developer docs, and generated documentation to use 'cultivar' terminology",
            "estimated_effort_hours": 6,
            "dependencies": ["phase-5-tests"],
            "blocking": ["phase-7-validation"],
            "subtasks": [
                "task-6-1-api-parity-update",
                "task-6-2-flutter-migration-plan-update",
                "task-6-3-screen-migration-matrix-update",
                "task-6-4-phase-gates-update",
                "task-6-5-migration-plan-update",
                "task-6-6-test-plan-update",
                "task-6-7-unused-variables-update",
                "task-6-8-wiki-home-update",
                "task-6-9-user-guide-update",
                "task-6-10-user-docs-update",
                "task-6-11-dev-docs-update",
                "task-6-12-dmac-dev-docs-update",
                "task-6-13-dmac-user-docs-update",
                "task-6-14-beta-testing-guide-update",
                "task-6-15-readme-update",
                "task-6-16-plan-update",
                "task-6-17-tech-stack-update",
                "task-6-18-migration-status-update",
                "task-6-19-migration-complete-update",
                "task-6-20-decommission-checklist-update",
                "task-6-21-flutter-todo-update",
                "task-6-22-main-todo-update",
                "task-6-23-today-todo-update",
                "task-6-24-cultivar-report-update",
                "task-6-25-security-docs-update",
                "task-6-26-jwt-docs-update",
                "task-6-27-phase1-analysis-update",
                "task-6-28-flutter-implementation-update",
                "task-6-29-flutter-analysis-update",
                "task-6-30-api-integration-update",
                "task-6-31-implementation-plan-update",
                "task-6-32-app-store-listings-update",
                "task-6-33-roadmap-update",
                "task-6-34-generated-readme-update",
                "task-6-35-patch-status-update",
                "task-6-36-openapi-regenerate"
            ],
            "files_affected": [
                "docs/API-Parity.md",
                "scripts/generate_openapi.py"
            ]
        },
        {
            "id": "phase-7-validation",
            "title": "Phase 7: Validation, Cleanup, and Migration Guides",
            "description": "Create migration guides, validation scripts, backward compatibility docs, run full test suite, verify all changes",
            "estimated_effort_hours": 5,
            "dependencies": ["phase-6-documentation"],
            "blocking": [],
            "subtasks": [
                "task-7-1-terminology-guide-create",
                "task-7-2-validation-script-create",
                "task-7-3-alembic-migration-create",
                "task-7-4-backward-compat-guide-create",
                "task-7-5-run-backend-tests",
                "task-7-6-run-flutter-tests",
                "task-7-7-run-validation-script",
                "task-7-8-verify-api-endpoints",
                "task-7-9-verify-templates",
                "task-7-10-verify-backward-compat",
                "task-7-11-update-changelog",
                "task-7-12-create-migration-announcement"
            ],
            "files_affected": [
                "scripts/validate_terminology_migration.py",
                "CHANGELOG.md"
            ]
        }
    ]
    
    for phase in phases:
        task_data = {
            "id": phase["id"],
            "title": phase["title"],
            "description": phase["description"],
            "status": "TODO",
            "priority": "HIGH",
            "type": "FEATURE",
            "estimated_effort_hours": phase["estimated_effort_hours"],
            "actual_effort_hours": None,
            "parent_task_id": "cultivar-migration-master",
            "dependencies": phase.get("dependencies", []),
            "blocking": phase.get("blocking", []),
            "subtasks": phase["subtasks"],
            "assignee": "@traycerai",
            "tags": ["migration", "backend", "terminology"],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "started_at": None,
            "completed_at": None,
            "files_affected": phase["files_affected"],
            "acceptance_criteria": [
                f"All files in {phase['id']} updated with cultivar terminology",
                "Backward compatibility maintained",
                "All tests pass"
            ],
            "notes": f"Phase task for {phase['id']}",
            "linear_issue_id": None
        }
        
        task_file = TASKS_DIR / f"{phase['id']}.json"
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task_data, f, indent=2, ensure_ascii=False)
        
        print(f"Created phase task: {task_file}")

def create_taskmaster_config():
    """Create Task-Master-AI configuration file."""
    config_data = {
        "version": "1.0",
        "project": {
            "name": "CultivAR Emergant",
            "description": "Cannabis cultivation management platform",
            "repository": str(PROJECT_ROOT) + "/"
        },
        "taskmaster": {
            "enabled": True,
            "task_directory": ".taskmaster/tasks",
            "default_assignee": "@traycerai",
            "status_values": ["TODO", "IN_PROGRESS", "BLOCKED", "REVIEW", "DONE"],
            "priority_values": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
            "type_values": ["EPIC", "FEATURE", "BUG", "REFACTOR", "DOCS", "TEST"]
        },
        "integrations": {
            "linear": {
                "enabled": True,
                "sync_enabled": False,
                "workspace": "cultivar-emergant"
            },
            "git": {
                "enabled": True,
                "auto_commit_on_task_complete": False,
                "branch_naming_pattern": "task/{task-id}-{task-slug}"
            }
        },
        "automation": {
            "auto_create_subtasks": True,
            "auto_update_parent_status": True,
            "auto_calculate_effort": False,
            "notify_on_blocking_tasks": True
        },
        "reporting": {
            "generate_daily_summary": True,
            "generate_weekly_report": True,
            "track_velocity": True
        }
    }
    
    config_file = TASKMASTER_DIR / "config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, indent=2, ensure_ascii=False)
    
    print(f"Created Task-Master config: {config_file}")

def create_initial_reports():
    """Create initial status and progress reports."""
    # Migration status report
    status_report = f"""# CultivAR Migration Status Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Project Overview
- **Project**: CultivAR Emergant
- **Migration Type**: Cultivar Terminology Standardization  
- **Scope**: 100+ files across backend, frontend, templates, tests, docs
- **Estimated Duration**: 40 hours

## Current Status
- **Phase**: Pre-Migration Setup
- **Tasks Created**: {len(list(TASKS_DIR.glob('*.json')))}
- **Progress**: 0% Complete

## Next Steps
1. Begin Phase 1: Backend Models Migration
2. Execute systematic file updates across all phases
3. Validate changes at each phase boundary
4. Run comprehensive testing suite

## Risk Assessment
- **High**: Database schema changes may require migration scripts
- **Medium**: Frontend changes may affect user experience
- **Low**: Documentation updates are straightforward

---
*This report will be updated automatically as the migration progresses.*
"""
    
    report_file = REPORTS_DIR / "migration_status_report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(status_report)
    
    print(f"Created initial status report: {report_file}")

def main():
    """Main initialization function."""
    print("Initializing CultivAR Migration Task Structure")
    print("=" * 50)
    
    # Create directory structure
    create_directory_structure()
    
    # Create master task
    create_master_task()
    
    # Create phase tasks
    create_phase_tasks()
    
    # Create configuration
    create_taskmaster_config()
    
    # Create initial reports
    create_initial_reports()
    
    print("\\nTask-Master-AI initialization complete!")
    print(f"Tasks directory: {TASKS_DIR}")
    print(f"Reports directory: {REPORTS_DIR}")
    print(f"Config file: {TASKMASTER_DIR / 'config.json'}")

if __name__ == "__main__":
    main()