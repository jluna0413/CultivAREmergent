# Task-Master CLI Usage Guide

## Overview

The Task-Master CLI is a command-line tool for managing migration tasks in the Task-Master system. It provides comprehensive functionality for listing, viewing, updating, and reporting on tasks.

## Installation

The CLI is available as `scripts/taskmaster_cli.py`. Ensure you have Python 3.6+ installed.

## Configuration

The CLI loads configuration from `.taskmaster/config.json`:

```json
{
  "taskmaster": {
    "task_directory": ".taskmaster/tasks",
    "default_assignee": "@traycerai",
    "status_values": ["TODO", "IN_PROGRESS", "BLOCKED", "REVIEW", "DONE"],
    "priority_values": ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
  }
}
```

## Commands

### List Tasks

Display all tasks with optional filtering:

```bash
# List all tasks
python scripts/taskmaster_cli.py list

# Filter by status
python scripts/taskmaster_cli.py list --status IN_PROGRESS

# Filter by phase
python scripts/taskmaster_cli.py list --phase phase-1

# Filter by assignee
python scripts/taskmaster_cli.py list --assignee @traycerai

# Filter by priority
python scripts/taskmaster_cli.py list --priority HIGH
```

Output format:
```
ID                                    Title                                   Status       Priority  Assignee      
---------------------------------------------------------------------------------------------------------------
cultivar-migration-master             Complete Strain→Cultivar Terminology... TODO         HIGH      @traycerai   
phase-1-backend-models                Phase 1: Migrate Backend Models (Strain... TODO         HIGH      @traycerai   
phase-2-api-layer                     Phase 2: Migrate API Layer (Routers, Sc... TODO         HIGH      @traycerai   
```

### Show Task Details

Display detailed information about a specific task:

```bash
# Show basic task details
python scripts/taskmaster_cli.py show cultivar-migration-master

# Show task with subtasks
python scripts/taskmaster_cli.py show cultivar-migration-master --with-subtasks
```

Output includes:
- Task ID and title
- Description
- Status and priority
- Type, assignee, estimated effort
- Creation and modification timestamps
- Dependencies and blocking tasks
- Files affected
- Acceptance criteria
- Subtasks (if requested)

### Start Task

Mark a task as IN_PROGRESS:

```bash
python scripts/taskmaster_cli.py start phase-1-backend-models
```

This will:
- Change task status to `IN_PROGRESS`
- Set `started_at` timestamp if not already set
- Update `updated_at` timestamp

### Update Task Status

Change the status of a task:

```bash
# Update status to IN_PROGRESS
python scripts/taskmaster_cli.py update phase-1-backend-models --status IN_PROGRESS

# Mark as blocked
python scripts/taskmaster_cli.py update phase-2-api-layer --status BLOCKED

# Mark for review
python scripts/taskmaster_cli.py update phase-3-frontend-flutter --status REVIEW

# Complete task
python scripts/taskmaster_cli.py update phase-1-backend-models --status DONE
```

Valid statuses: `TODO`, `IN_PROGRESS`, `BLOCKED`, `REVIEW`, `DONE`

### Complete Task

Shortcut to mark a task as DONE:

```bash
python scripts/taskmaster_cli.py complete phase-1-backend-models
```

### Show Next Available Tasks

List tasks ready to work on (no blocking dependencies):

```bash
python scripts/taskmaster_cli.py next
```

### Generate Report

Create a comprehensive status report:

```bash
python scripts/taskmaster_cli.py report
```

This generates:
- Summary statistics (total tasks, completion percentage)
- Status breakdown (counts and percentages for each status)
- Priority breakdown
- Type breakdown
- Detailed task list grouped by status
- Phase progress (if applicable)
- Next steps recommendations

The report is saved to `.taskmaster/reports/migration_status_report.md`

## Examples

### Basic Workflow

```bash
# 1. List all tasks
python scripts/taskmaster_cli.py list

# 2. Start the first phase
python scripts/taskmaster_cli.py start phase-1-backend-models

# 3. Show current progress
python scripts/taskmaster_cli.py report

# 4. Complete the phase when done
python scripts/taskmaster_cli.py complete phase-1-backend-models

# 5. Check what's next
python scripts/taskmaster_cli.py next
```

### Filtering and Analysis

```bash
# See only high priority tasks
python scripts/taskmaster_cli.py list --priority HIGH

# Check phase progress
python scripts/taskmaster_cli.py list --phase phase-

# See who's working on what
python scripts/taskmaster_cli.py list --assignee @traycerai

# Check blocked tasks
python scripts/taskmaster_cli.py list --status BLOCKED
```

### Task Details and Planning

```bash
# Get full details for planning
python scripts/taskmaster_cli.py show cultivar-migration-master --with-subtasks

# Check specific task requirements
python scripts/taskmaster_cli.py show phase-1-backend-models
```

## Error Handling

The CLI provides clear error messages for common issues:

- **Task not found**: "Error: Task 'xxx' not found"
- **Invalid status**: "Error: Invalid status 'xxx'. Valid statuses: TODO, IN_PROGRESS, BLOCKED, REVIEW, DONE"
- **File errors**: "Error: Failed to write file: xxx"
- **Configuration errors**: "Error: .taskmaster/config.json not found"

## Status Colors

Terminal output uses color coding:
- 🟡 **TODO**: Yellow
- 🔵 **IN_PROGRESS**: Blue  
- 🔴 **BLOCKED**: Red
- 🟣 **REVIEW**: Purple
- 🟢 **DONE**: Green

## File Management

### Automatic Backups

When updating tasks, the CLI automatically creates backups:
- Backup location: `.taskmaster/backups/`
- Naming: `{task_name}_{timestamp}.json`
- Example: `cultivar-migration-master_20251105_143052.json`

### Safe File Operations

- Uses atomic file writes (write to temp file, then rename)
- Creates automatic backups before updates
- Validates JSON structure before writing
- Handles file permissions and I/O errors gracefully

## Testing

Run the test suite:

```bash
python scripts/test_taskmaster_cli.py
```

The test suite covers:
- Configuration loading
- Task file operations
- Status and priority validation
- List and show command functionality
- Task update operations

## Integration with Migration Workflow

The CLI is designed to work seamlessly with the strain→cultivar migration:

1. **Planning Phase**: Use `list` and `show` to understand the scope
2. **Execution Phase**: Use `start`, `update`, and `complete` to track progress
3. **Monitoring Phase**: Use `report` and `next` to stay on track
4. **Validation Phase**: Check `report` for completion status

## Tips

- Use `report` regularly to track overall progress
- The `next` command helps identify what's ready to work on
- Status changes are automatically timestamped
- Parent tasks are auto-updated when all subtasks complete
- Color coding helps quickly identify task status at a glance

## Troubleshooting

**CLI doesn't start**: Check that `.taskmaster/config.json` exists and is valid JSON

**Tasks not found**: Verify tasks exist in the configured `task_directory`

**Permission errors**: Ensure write permissions for task files and backup directory

**JSON errors**: Check task files for syntax errors; backups can help with recovery