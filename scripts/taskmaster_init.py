#!/usr/bin/env python3
"""
Task-Master-AI Initialization Script for Cultivar Migration

Automates creation of all task files and directory structure for the migration project.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class TaskMasterInit:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.task_dir = self.project_root / ".taskmaster" / "tasks"
        self.reports_dir = self.project_root / ".taskmaster" / "reports"
        
    def create_directories(self):
        """Create necessary directories."""
        self.task_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created directories: {self.task_dir}, {self.reports_dir}")
        
    def create_phase_tasks(self):
        """Create all phase task files."""
        phases = [
            {
                "id": "phase-2-api-layer",
                "title": "Phase 2: Migrate API Layer (Routers, Schemas, Handlers)",
                "description": "Rename strains.py→cultivars.py for routers and schemas, update all Pydantic models, rename handler modules, implement dual-mounting for backward compatibility",
                "estimated_effort_hours": 8,
                "parent": "cultivar-migration-master",
                "dependencies": ["phase-1-backend-models"],
                "blocking": ["phase-3-frontend-flutter"],
                "files_affected": [
                    "app/fastapi_app/models/strains.py",
                    "app/fastapi_app/routers/strains.py",
                    "app/fastapi_app/__init__.py",
                    "app/handlers/strain_handlers.py",
                    "app/handlers/strain_handlers_async.py"
                ]
            },
            {
                "id": "phase-3-frontend-flutter",
                "title": "Phase 3: Migrate Flutter Frontend (Models, Providers, Widgets)",
                "description": "Consolidate duplicate providers/widgets, update all Dart code to use 'cultivar' terminology, align models with backend schema",
                "estimated_effort_hours": 6,
                "parent": "cultivar-migration-master",
                "dependencies": ["phase-2-api-layer"],
                "blocking": ["phase-4-templates-js"],
                "files_affected": [
                    "flutter_app/lib/core/state/strains_provider.dart",
                    "flutter_app/lib/core/providers/cultivar_provider.dart",
                    "flutter_app/lib/screens/cultivars_screen.dart",
                    "flutter_app/lib/core/services/api_client.dart"
                ]
            },
            {
                "id": "phase-4-templates-js",
                "title": "Phase 4: Migrate Templates and JavaScript",
                "description": "Rename HTML templates, update all user-facing text from 'Strains' to 'Cultivars', update JavaScript functions and AJAX endpoints",
                "estimated_effort_hours": 6,
                "parent": "cultivar-migration-master",
                "dependencies": ["phase-3-frontend-flutter"],
                "blocking": ["phase-5-tests"],
                "files_affected": [
                    "app/web/templates/views/strains.html",
                    "app/web/static/js/main.js",
                    "app/web/templates/views/strain.html",
                    "app/web/templates/views/add_strain.html"
                ]
            },
            {
                "id": "phase-5-tests",
                "title": "Phase 5: Migrate Test Suite",
                "description": "Update all test files, test data, assertions, and test descriptions to use 'cultivar' terminology",
                "estimated_effort_hours": 5,
                "parent": "cultivar-migration-master",
                "dependencies": ["phase-4-templates-js"],
                "blocking": ["phase-6-documentation"],
                "files_affected": [
                    "tests/integration/test_strains.py",
                    "tests/integration/test_strains_integration.py",
                    "flutter_app/test/widget/plant_card_test.dart"
                ]
            },
            {
                "id": "phase-6-documentation",
                "title": "Phase 6: Migrate Documentation",
                "description": "Update all markdown files, API documentation, user guides, developer docs, and generated documentation to use 'cultivar' terminology",
                "estimated_effort_hours": 6,
                "parent": "cultivar-migration-master",
                "dependencies": ["phase-5-tests"],
                "blocking": ["phase-7-validation"],
                "files_affected": [
                    "docs/API-Parity.md",
                    "docs/FLUTTER_MIGRATION_PLAN.md",
                    "docs/SCREEN_MIGRATION_MATRIX.md",
                    "README.md"
                ]
            },
            {
                "id": "phase-7-validation",
                "title": "Phase 7: Validation, Cleanup, and Migration Guides",
                "description": "Create migration guides, validation scripts, backward compatibility docs, run full test suite, verify all changes",
                "estimated_effort_hours": 5,
                "parent": "cultivar-migration-master",
                "dependencies": ["phase-6-documentation"],
                "blocking": [],
                "files_affected": [
                    "docs/TERMINOLOGY_MIGRATION_GUIDE.md",
                    "scripts/validate_terminology_migration.py",
                    "docs/BACKWARD_COMPATIBILITY_STRATEGY.md"
                ]
            }
        ]
        
        for phase in phases:
            self.create_phase_task(phase)
            
    def create_phase_task(self, phase: Dict[str, Any]):
        """Create a single phase task file."""
        task = {
            "id": phase["id"],
            "title": phase["title"],
            "description": phase["description"],
            "status": "TODO",
            "priority": "HIGH",
            "type": "FEATURE",
            "estimated_effort_hours": phase["estimated_effort_hours"],
            "actual_effort_hours": None,
            "parent_task_id": phase["parent"],
            "dependencies": phase["dependencies"],
            "blocking": phase["blocking"],
            "subtasks": [],
            "assignee": "@traycerai",
            "tags": ["migration", "phase", "cultivar"],
            "created_at": datetime.utcnow().isoformat() + "Z",
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "started_at": None,
            "completed_at": None,
            "files_affected": phase["files_affected"],
            "acceptance_criteria": [
                "All specified files updated with cultivar terminology",
                "All tests pass",
                "No breaking changes",
                "Backward compatibility maintained"
            ],
            "notes": f"Part of {phase['parent']} epic migration",
            "linear_issue_id": None
        }
        
        task_file = self.task_dir / f"{phase['id']}.json"
        with open(task_file, 'w') as f:
            json.dump(task, f, indent=2)
        print(f"Created task: {task_file}")
        
    def create_atomic_tasks(self):
        """Create atomic subtask files for Phase 1."""
        atomic_tasks = [
            {
                "id": "task-1-1-base-models-rename",
                "title": "Rename Strain→Cultivar in base_models.py",
                "description": "Update class name, relationships, and documentation",
                "file": "app/models/base_models.py",
                "phase": "phase-1-backend-models"
            },
            {
                "id": "task-1-2-models-init-update",
                "title": "Update exports in models/__init__.py",
                "description": "Add Cultivar export and Strain alias",
                "file": "app/models/__init__.py",
                "phase": "phase-1-backend-models"
            }
        ]
        
        for task in atomic_tasks:
            self.create_atomic_task(task)
            
    def create_atomic_task(self, task: Dict[str, Any]):
        """Create a single atomic task file."""
        atomic_task = {
            "id": task["id"],
            "title": task["title"],
            "description": task["description"],
            "status": "TODO",
            "priority": "HIGH",
            "type": "TASK",
            "estimated_effort_hours": 1,
            "actual_effort_hours": None,
            "parent_task_id": task["phase"],
            "dependencies": [],
            "blocking": [],
            "subtasks": [],
            "assignee": "@traycerai",
            "tags": ["atomic", "migration", "cultivar"],
            "created_at": datetime.utcnow().isoformat() + "Z",
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "started_at": None,
            "completed_at": None,
            "files_affected": [task["file"]],
            "acceptance_criteria": [
                f"File {task['file']} updated correctly",
                "All tests pass",
                "No regressions"
            ],
            "notes": f"Atomic task for {task['phase']}",
            "linear_issue_id": None
        }
        
        task_file = self.task_dir / f"{task['id']}.json"
        with open(task_file, 'w') as f:
            json.dump(atomic_task, f, indent=2)
        print(f"Created atomic task: {task_file}")
        
    def create_config(self):
        """Create Task-Master configuration file."""
        config = {
            "version": "1.0",
            "project": {
                "name": "CultivAR Emergant",
                "description": "Cannabis cultivation management platform",
                "repository": str(self.project_root)
            },
            "taskmaster": {
                "enabled": True,
                "task_directory": str(self.task_dir.relative_to(self.project_root)),
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
        
        config_file = self.project_root / ".taskmaster" / "config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Created config: {config_file}")
        
    def generate_reports(self):
        """Generate initial status reports."""
        # Migration status report
        status_report = self.reports_dir / "migration_status_report.md"
        with open(status_report, 'w') as f:
            f.write("""# Cultivar Migration Status Report

## Overview
Systematic migration of 'strain' terminology to 'cultivar' across 100+ files.

## Phase Progress
- ✅ Phase 1: Backend Models (IN_PROGRESS)
- ⏳ Phase 2: API Layer (TODO)
- ⏳ Phase 3: Frontend Flutter (TODO)
- ⏳ Phase 4: Templates & JavaScript (TODO)
- ⏳ Phase 5: Tests (TODO)
- ⏳ Phase 6: Documentation (TODO)
- ⏳ Phase 7: Validation (TODO)

## Next Steps
1. Complete Phase 1 backend model changes
2. Create Phase 2 API layer migration
3. Begin frontend Flutter consolidation
4. Update templates and JavaScript
5. Migrate test suite
6. Update documentation
7. Final validation and cleanup

## Critical Files Changed
- ✅ `app/models/base_models.py` - Model aliases verified
- ✅ `app/models/__init__.py` - Exports updated
- ✅ `alembic/versions/2025_11_07_0301_add_strain_id_aliases_simple.py` - DB compatibility
- ✅ `app/fastapi_app/routers/auth.py` - Auth endpoint added

## Risk Assessment
- ✅ Database backward compatibility: SAFE
- ✅ Model aliasing: IMPLEMENTED
- ⏳ API compatibility: PENDING
- ⏳ Frontend consolidation: PENDING
""")
        
        print(f"Created status report: {status_report}")
        
    def run(self, phase: str = None):
        """Run the initialization."""
        print("Initializing Task-Master for Cultivar Migration...")
        
        self.create_directories()
        self.create_config()
        
        if phase == "1" or phase is None:
            self.create_atomic_tasks()
            
        if phase is None:
            self.create_phase_tasks()
            self.generate_reports()
            
        print("✅ Task-Master initialization complete!")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Initialize Task-Master for Cultivar Migration")
    parser.add_argument("--phase", help="Create tasks for specific phase only")
    parser.add_argument("--create-all", action="store_true", help="Create all tasks")
    args = parser.parse_args()
    
    init = TaskMasterInit()
    init.run(args.phase)

if __name__ == "__main__":
    main()