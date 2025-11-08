#!/usr/bin/env python3
"""
Task-Master-AI CLI Tool

Command-line interface for managing cultivar migration tasks.
Provides comprehensive task management without manual JSON editing.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import click
import subprocess
import time
import re


class TaskStatus(Enum):
    """Task status enum"""
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    REVIEW = "REVIEW"
    DONE = "DONE"


class TaskPriority(Enum):
    """Task priority enum"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class TaskType(Enum):
    """Task type enum"""
    EPIC = "EPIC"
    FEATURE = "FEATURE"
    BUG = "BUG"
    REFACTOR = "REFACTOR"
    DOCS = "DOCS"
    TEST = "TEST"


@dataclass
class Task:
    """Task data class"""
    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    type: TaskType
    estimated_effort_hours: int
    parent_task_id: Optional[str]
    dependencies: List[str]
    blocking: List[str]
    assignee: str
    tags: List[str]
    files_affected: List[str]
    acceptance_criteria: List[str]
    created_at: str
    updated_at: str
    started_at: Optional[str]
    completed_at: Optional[str]
    actual_effort_hours: Optional[int]
    notes: str
    linear_issue_id: Optional[str]


class TaskMasterCLI:
    """Task-Master-AI CLI Tool"""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.task_dir = self.base_dir / ".taskmaster" / "tasks"
        self.config_file = self.base_dir / ".taskmaster" / "config.json"
        self.tasks_cache: Dict[str, Task] = {}
        self.load_tasks()
    
    def load_tasks(self):
        """Load all tasks from JSON files"""
        if not self.task_dir.exists():
            click.echo(f"Task directory not found: {self.task_dir}")
            return
        
        for task_file in self.task_dir.glob("*.json"):
            try:
                with open(task_file) as f:
                    task_data = json.load(f)
                
                task = self._dict_to_task(task_data)
                self.tasks_cache[task.id] = task
                
            except Exception as e:
                click.echo(f"Error loading task {task_file}: {e}", err=True)
    
    def _dict_to_task(self, data: Dict[str, Any]) -> Task:
        """Convert dictionary to Task object"""
        return Task(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            status=TaskStatus(data["status"]),
            priority=TaskPriority(data["priority"]),
            type=TaskType(data["type"]),
            estimated_effort_hours=data.get("estimated_effort_hours", 0),
            parent_task_id=data.get("parent_task_id"),
            dependencies=data.get("dependencies", []),
            blocking=data.get("blocking", []),
            assignee=data.get("assignee", ""),
            tags=data.get("tags", []),
            files_affected=data.get("files_affected", []),
            acceptance_criteria=data.get("acceptance_criteria", []),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            started_at=data.get("started_at"),
            completed_at=data.get("completed_at"),
            actual_effort_hours=data.get("actual_effort_hours"),
            notes=data.get("notes", ""),
            linear_issue_id=data.get("linear_issue_id")
        )
    
    def _task_to_dict(self, task: Task) -> Dict[str, Any]:
        """Convert Task object to dictionary"""
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status.value,
            "priority": task.priority.value,
            "type": task.type.value,
            "estimated_effort_hours": task.estimated_effort_hours,
            "parent_task_id": task.parent_task_id,
            "dependencies": task.dependencies,
            "blocking": task.blocking,
            "assignee": task.assignee,
            "tags": task.tags,
            "files_affected": task.files_affected,
            "acceptance_criteria": task.acceptance_criteria,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "started_at": task.started_at,
            "completed_at": task.completed_at,
            "actual_effort_hours": task.actual_effort_hours,
            "notes": task.notes,
            "linear_issue_id": task.linear_issue_id
        }
    
    def save_task(self, task: Task):
        """Save task to JSON file"""
        task_file = self.task_dir / f"{task.id}.json"
        task.updated_at = datetime.now().isoformat() + "Z"
        
        with open(task_file, "w") as f:
            json.dump(self._task_to_dict(task), f, indent=2)
        
        self.tasks_cache[task.id] = task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        return self.tasks_cache.get(task_id)
    
    def list_tasks(self, status: Optional[TaskStatus] = None, phase: Optional[int] = None, 
                   assignee: Optional[str] = None, priority: Optional[TaskPriority] = None) -> List[Task]:
        """List tasks with optional filters"""
        tasks = list(self.tasks_cache.values())
        
        if status:
            tasks = [t for t in tasks if t.status == status]
        if phase:
            phase_tasks = [t for t in tasks if f"phase-{phase}" in t.id]
            tasks = phase_tasks
        if assignee:
            tasks = [t for t in tasks if t.assignee == assignee]
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        
        return sorted(tasks, key=lambda t: (t.priority.value, t.created_at))
    
    def get_next_tasks(self, phase: Optional[int] = None) -> List[Task]:
        """Get next available tasks (no blocking dependencies)"""
        available_tasks = []
        
        for task in self.tasks_cache.values():
            if task.status != TaskStatus.TODO:
                continue
                
            # Check if any blocking dependencies exist
            blocking_tasks = [self.get_task(dep_id) for dep_id in task.blocking]
            blocked = any(dep and dep.status != TaskStatus.DONE for dep in blocking_tasks)
            
            if not blocked:
                if phase and f"phase-{phase}" in task.id:
                    available_tasks.append(task)
                elif not phase:
                    available_tasks.append(task)
        
        return sorted(available_tasks, key=lambda t: (t.priority.value, t.created_at))
    
    def update_task_status(self, task_id: str, status: TaskStatus, 
                          actual_effort_hours: Optional[int] = None):
        """Update task status"""
        task = self.get_task(task_id)
        if not task:
            click.echo(f"Task not found: {task_id}", err=True)
            return False
        
        old_status = task.status
        task.status = status
        
        if status == TaskStatus.IN_PROGRESS and not task.started_at:
            task.started_at = datetime.now().isoformat() + "Z"
        elif status == TaskStatus.DONE and not task.completed_at:
            task.completed_at = datetime.now().isoformat() + "Z"
            if actual_effort_hours:
                task.actual_effort_hours = actual_effort_hours
        
        self.save_task(task)
        
        # Update parent task if all subtasks are done
        if task.parent_task_id and status == TaskStatus.DONE:
            self._update_parent_status(task.parent_task_id)
        
        click.echo(f"Task {task_id} status updated: {old_status.value} → {status.value}")
        return True
    
    def _update_parent_status(self, parent_id: str):
        """Update parent task status based on subtask completion"""
        parent = self.get_task(parent_id)
        if not parent:
            return
        
        subtasks = [t for t in self.tasks_cache.values() if t.parent_task_id == parent_id]
        if not subtasks:
            return
        
        done_count = sum(1 for t in subtasks if t.status == TaskStatus.DONE)
        total_count = len(subtasks)
        
        if done_count == 0 and parent.status != TaskStatus.DONE:
            parent.status = TaskStatus.TODO
        elif done_count < total_count and parent.status not in [TaskStatus.DONE, TaskStatus.IN_PROGRESS]:
            parent.status = TaskStatus.IN_PROGRESS
        elif done_count == total_count and parent.status != TaskStatus.DONE:
            parent.status = TaskStatus.DONE
            parent.completed_at = datetime.now().isoformat() + "Z"
        
        self.save_task(parent)
    
    def block_task(self, task_id: str, reason: str):
        """Block a task with reason"""
        task = self.get_task(task_id)
        if not task:
            click.echo(f"Task not found: {task_id}", err=True)
            return False
        
        task.status = TaskStatus.BLOCKED
        task.notes += f"\n\nBLOCKED: {reason} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.save_task(task)
        
        click.echo(f"Task {task_id} blocked: {reason}")
        return True
    
    def unblock_task(self, task_id: str):
        """Unblock a task"""
        task = self.get_task(task_id)
        if not task:
            click.echo(f"Task not found: {task_id}", err=True)
            return False
        
        if task.status == TaskStatus.BLOCKED:
            task.status = TaskStatus.TODO
            task.notes += f"\n\nUNBLOCKED at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.save_task(task)
            click.echo(f"Task {task_id} unblocked")
            return True
        else:
            click.echo(f"Task {task_id} is not blocked", err=True)
            return False
    
    def show_task_details(self, task_id: str, with_subtasks: bool = False):
        """Show detailed task information"""
        task = self.get_task(task_id)
        if not task:
            click.echo(f"Task not found: {task_id}", err=True)
            return
        
        click.echo(f"\n{'='*60}")
        click.echo(f"Task: {task.id}")
        click.echo(f"{'='*60}")
        click.echo(f"Title: {task.title}")
        click.echo(f"Description: {task.description}")
        click.echo(f"Status: {task.status.value}")
        click.echo(f"Priority: {task.priority.value}")
        click.echo(f"Type: {task.type.value}")
        click.echo(f"Estimated Effort: {task.estimated_effort_hours}h")
        if task.actual_effort_hours:
            click.echo(f"Actual Effort: {task.actual_effort_hours}h")
        click.echo(f"Assignee: {task.assignee}")
        click.echo(f"Tags: {', '.join(task.tags)}")
        click.echo(f"Dependencies: {', '.join(task.dependencies) if task.dependencies else 'None'}")
        click.echo(f"Blocking: {', '.join(task.blocking) if task.blocking else 'None'}")
        
        if task.started_at:
            click.echo(f"Started: {task.started_at}")
        if task.completed_at:
            click.echo(f"Completed: {task.completed_at}")
        
        click.echo(f"Files Affected: {len(task.files_affected)} files")
        if task.files_affected:
            for file in task.files_affected[:5]:  # Show first 5 files
                click.echo(f"  - {file}")
            if len(task.files_affected) > 5:
                click.echo(f"  ... and {len(task.files_affected) - 5} more")
        
        click.echo(f"Acceptance Criteria:")
        for criterion in task.acceptance_criteria:
            click.echo(f"  - {criterion}")
        
        if task.notes:
            click.echo(f"Notes: {task.notes}")
        
        if with_subtasks:
            subtasks = [t for t in self.tasks_cache.values() if t.parent_task_id == task_id]
            if subtasks:
                click.echo(f"\nSubtasks:")
                for subtask in subtasks:
                    click.echo(f"  [{subtask.status.value}] {subtask.id}: {subtask.title}")
        
        click.echo(f"{'='*60}")
    
    def generate_progress_report(self) -> str:
        """Generate progress report"""
        tasks = list(self.tasks_cache.values())
        total_tasks = len(tasks)
        done_tasks = sum(1 for t in tasks if t.status == TaskStatus.DONE)
        in_progress_tasks = sum(1 for t in tasks if t.status == TaskStatus.IN_PROGRESS)
        blocked_tasks = sum(1 for t in tasks if t.status == TaskStatus.BLOCKED)
        
        total_estimated = sum(t.estimated_effort_hours for t in tasks)
        total_actual = sum(t.actual_effort_hours or 0 for t in tasks if t.status == TaskStatus.DONE)
        
        # Progress by phase
        phases = {}
        for task in tasks:
            if "phase-" in task.id:
                phase_num = task.id.split("-")[1]
                if phase_num not in phases:
                    phases[phase_num] = {"total": 0, "done": 0, "estimated": 0}
                phases[phase_num]["total"] += 1
                if task.status == TaskStatus.DONE:
                    phases[phase_num]["done"] += 1
                phases[phase_num]["estimated"] += task.estimated_effort_hours
        
        report = f"""
# Cultivar Migration Progress Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overall Progress
- **Total Tasks**: {total_tasks}
- **Completed**: {done_tasks} ({done_tasks/total_tasks*100:.1f}%)
- **In Progress**: {in_progress_tasks}
- **Blocked**: {blocked_tasks}
- **Remaining**: {total_tasks - done_tasks - in_progress_tasks}

## Effort Tracking
- **Total Estimated**: {total_estimated} hours
- **Total Actual**: {total_actual} hours
- **Efficiency**: {total_actual/total_estimated*100:.1f}% if total_estimated > 0 else "N/A"

## Phase Progress
"""
        
        for phase_num in sorted(phases.keys()):
            phase = phases[phase_num]
            progress = phase["done"] / phase["total"] * 100
            report += f"- **Phase {phase_num}**: {phase['done']}/{phase['total']} ({progress:.1f}%) - {phase['estimated']}h\n"
        
        report += f"\n## Next Actions\n"
        next_tasks = self.get_next_tasks()
        for task in next_tasks[:5]:  # Show next 5 tasks
            report += f"- {task.id}: {task.title} ({task.priority.value})\n"
        
        if len(next_tasks) > 5:
            report += f"- ... and {len(next_tasks) - 5} more\n"
        
        return report
    
    def validate_task_dependencies(self) -> bool:
        """Validate task dependency graph for cycles and orphans"""
        is_valid = True
        
        # Check for cycles
        visited = set()
        rec_stack = set()
        
        def has_cycle(task_id: str) -> bool:
            if task_id in rec_stack:
                return True
            if task_id in visited:
                return False
            
            visited.add(task_id)
            rec_stack.add(task_id)
            
            task = self.get_task(task_id)
            if not task:
                return False
            
            for dep_id in task.dependencies:
                if dep_id not in self.tasks_cache:
                    click.echo(f"ERROR: Task {task_id} depends on non-existent task {dep_id}")
                    is_valid = False
                elif has_cycle(dep_id):
                    click.echo(f"ERROR: Cycle detected involving task {task_id}")
                    is_valid = False
            
            rec_stack.remove(task_id)
            return False
        
        # Check for orphaned tasks
        referenced_tasks = set()
        for task in self.tasks_cache.values():
            referenced_tasks.update(task.dependencies)
            referenced_tasks.update(task.blocking)
        
        orphaned_tasks = set(self.tasks_cache.keys()) - referenced_tasks
        if orphaned_tasks:
            click.echo(f"WARNING: Orphaned tasks found: {', '.join(orphaned_tasks)}")
        
        # Check each task for cycles
        for task_id in self.tasks_cache:
            if task_id not in visited:
                if has_cycle(task_id):
                    is_valid = False
        
        if is_valid:
            click.echo("Task dependency validation passed")
        else:
            click.echo("Task dependency validation failed", err=True)
        
        return is_valid
    
    def export_tasks(self, format_type: str = "json") -> str:
        """Export tasks in specified format"""
        tasks = list(self.tasks_cache.values())
        
        if format_type.lower() == "json":
            return json.dumps([self._task_to_dict(t) for t in tasks], indent=2)
        
        elif format_type.lower() == "csv":
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow(["ID", "Title", "Status", "Priority", "Type", "Estimated_Hours", 
                           "Actual_Hours", "Assignee", "Dependencies", "Blocking", "Files_Affected"])
            
            # Write data
            for task in tasks:
                writer.writerow([
                    task.id, task.title, task.status.value, task.priority.value,
                    task.type.value, task.estimated_effort_hours, task.actual_effort_hours,
                    task.assignee, ";".join(task.dependencies), ";".join(task.blocking),
                    ";".join(task.files_affected)
                ])
            
            return output.getvalue()
        
        elif format_type.lower() == "markdown":
            report = "# Cultivar Migration Tasks\n\n"
            
            # Group by status
            for status in TaskStatus:
                status_tasks = [t for t in tasks if t.status == status]
                if status_tasks:
                    report += f"## {status.value} ({len(status_tasks)} tasks)\n\n"
                    
                    for task in status_tasks:
                        report += f"### {task.id}: {task.title}\n"
                        report += f"- **Priority**: {task.priority.value}\n"
                        report += f"- **Effort**: {task.estimated_effort_hours}h"
                        if task.actual_effort_hours:
                            report += f" (actual: {task.actual_effort_hours}h)"
                        report += f"\n- **Assignee**: {task.assignee}\n"
                        if task.dependencies:
                            report += f"- **Dependencies**: {', '.join(task.dependencies)}\n"
                        report += f"\n{task.description}\n\n"
            
            return report
        
        else:
            raise ValueError(f"Unsupported format: {format_type}")


# CLI Commands
@click.group()
@click.pass_context
def cli(ctx):
    """Task-Master-AI CLI for managing cultivar migration tasks"""
    ctx.ensure_object(dict)
    ctx.obj['cli'] = TaskMasterCLI()


@cli.command()
@click.option('--status', type=click.Choice([s.value for s in TaskStatus]), help='Filter by status')
@click.option('--phase', type=click.IntRange(1, 7), help='Filter by phase number')
@click.option('--assignee', help='Filter by assignee')
@click.option('--priority', type=click.Choice([p.value for p in TaskPriority]), help='Filter by priority')
@click.pass_obj
def list(cli_obj, status, phase, assignee, priority):
    """List tasks with optional filters"""
    status_filter = TaskStatus(status) if status else None
    priority_filter = TaskPriority(priority) if priority else None
    
    tasks = cli_obj.list_tasks(
        status=status_filter,
        phase=phase,
        assignee=assignee,
        priority=priority_filter
    )
    
    if not tasks:
        click.echo("No tasks found matching criteria")
        return
    
    # Color codes
    colors = {
        TaskStatus.TODO: 'yellow',
        TaskStatus.IN_PROGRESS: 'blue',
        TaskStatus.BLOCKED: 'red',
        TaskStatus.REVIEW: 'magenta',
        TaskStatus.DONE: 'green'
    }
    
    click.echo(f"\nFound {len(tasks)} tasks:")
    click.echo("-" * 80)
    
    for task in tasks:
        color = colors.get(task.status, 'white')
        click.echo(f"[{task.status.value:<12}] {task.id:<30} {task.title[:30]}", color=color)


@cli.command()
@click.argument('task_id')
@click.option('--with-subtasks', is_flag=True, help='Show subtasks')
@click.pass_obj
def show(cli_obj, task_id, with_subtasks):
    """Show detailed task information"""
    cli_obj.show_task_details(task_id, with_subtasks)


@cli.command()
@click.argument('task_id')
@click.option('--status', type=click.Choice([s.value for s in TaskStatus]), required=True)
@click.option('--effort', type=int, help='Actual effort hours (for DONE tasks)')
@click.pass_obj
def update(cli_obj, task_id, status, effort):
    """Update task status"""
    status_enum = TaskStatus(status)
    if cli_obj.update_task_status(task_id, status_enum, effort):
        click.echo("Task status updated successfully")
    else:
        click.echo("Failed to update task status", err=True)


@cli.command()
@click.argument('task_id')
@click.pass_obj
def start(cli_obj, task_id):
    """Start a task (sets status to IN_PROGRESS with timestamp)"""
    if cli_obj.update_task_status(task_id, TaskStatus.IN_PROGRESS):
        click.echo("Task started successfully")
    else:
        click.echo("Failed to start task", err=True)


@cli.command()
@click.argument('task_id')
@click.option('--effort', type=int, required=True, help='Actual effort hours')
@click.pass_obj
def complete(cli_obj, task_id, effort):
    """Complete a task (sets status to DONE with effort tracking)"""
    if cli_obj.update_task_status(task_id, TaskStatus.DONE, effort):
        click.echo("Task completed successfully")
    else:
        click.echo("Failed to complete task", err=True)


@cli.command()
@click.argument('task_id')
@click.argument('reason')
@click.pass_obj
def block(cli_obj, task_id, reason):
    """Block a task with reason"""
    if cli_obj.block_task(task_id, reason):
        click.echo("Task blocked successfully")
    else:
        click.echo("Failed to block task", err=True)


@cli.command()
@click.argument('task_id')
@click.pass_obj
def unblock(cli_obj, task_id):
    """Unblock a task"""
    if cli_obj.unblock_task(task_id):
        click.echo("Task unblocked successfully")
    else:
        click.echo("Failed to unblock task", err=True)


@cli.command()
@click.option('--phase', type=click.IntRange(1, 7), help='Show next tasks for specific phase')
@click.pass_obj
def next(cli_obj, phase):
    """Show next available tasks (no blocking dependencies)"""
    tasks = cli_obj.get_next_tasks(phase)
    
    if not tasks:
        click.echo("No available tasks found")
        return
    
    click.echo(f"\nNext available tasks:")
    if phase:
        click.echo(f"Phase {phase}:")
    click.echo("-" * 60)
    
    for task in tasks:
        click.echo(f"[{task.priority.value}] {task.id}: {task.title}")


@cli.command()
@click.option('--check-cycles', is_flag=True, help='Check for circular dependencies')
@click.option('--check-orphans', is_flag=True, help='Check for orphaned tasks')
@click.pass_obj
def validate(cli_obj, check_cycles, check_orphans):
    """Validate task dependencies and structure"""
    if cli_obj.validate_task_dependencies():
        click.echo("Validation passed successfully")
    else:
        click.echo("Validation failed", err=True)
        sys.exit(1)


@cli.command()
@click.option('--type', 'format_type', 
              type=click.Choice(['progress', 'burndown', 'velocity', 'blocked']),
              default='progress', help='Type of report to generate')
@click.pass_obj
def report(cli_obj, format_type):
    """Generate progress and analytics reports"""
    if format_type == 'progress':
        report = cli_obj.generate_progress_report()
        click.echo(report)
    elif format_type == 'burndown':
        # TODO: Implement burndown chart
        click.echo("Burndown chart not yet implemented")
    elif format_type == 'velocity':
        # TODO: Implement velocity tracking
        click.echo("Velocity tracking not yet implemented")
    elif format_type == 'blocked':
        blocked_tasks = [t for t in cli_obj.tasks_cache.values() if t.status == TaskStatus.BLOCKED]
        click.echo(f"\nBlocked Tasks ({len(blocked_tasks)}):")
        for task in blocked_tasks:
            click.echo(f"  - {task.id}: {task.title}")
    else:
        click.echo(f"Unknown report type: {format_type}", err=True)


@cli.command()
@click.option('--to-linear', is_flag=True, help='Sync tasks to Linear')
@click.option('--from-linear', is_flag=True, help='Sync tasks from Linear')
@click.pass_obj
def sync(cli_obj, to_linear, from_linear):
    """Sync tasks with Linear (placeholder implementation)"""
    if to_linear:
        click.echo("Syncing tasks to Linear... (not implemented)")
    elif from_linear:
        click.echo("Syncing tasks from Linear... (not implemented)")
    else:
        click.echo("Please specify --to-linear or --from-linear", err=True)


@cli.command()
@click.option('--format', 'format_type',
              type=click.Choice(['json', 'csv', 'markdown']),
              default='json', help='Export format')
@click.pass_obj
def export(cli_obj, format_type):
    """Export tasks to specified format"""
    try:
        exported_data = cli_obj.export_tasks(format_type)
        click.echo(exported_data)
    except Exception as e:
        click.echo(f"Export failed: {e}", err=True)


@cli.command()
@click.pass_obj
def status(cli_obj):
    """Show overall project status"""
    tasks = list(cli_obj.tasks_cache.values())
    total = len(tasks)
    done = sum(1 for t in tasks if t.status == TaskStatus.DONE)
    in_progress = sum(1 for t in tasks if t.status == TaskStatus.IN_PROGRESS)
    blocked = sum(1 for t in tasks if t.status == TaskStatus.BLOCKED)
    
    total_estimated = sum(t.estimated_effort_hours for t in tasks)
    total_actual = sum(t.actual_effort_hours or 0 for t in tasks if t.status == TaskStatus.DONE)
    
    click.echo(f"""
Cultivar Migration Project Status
=================================

Total Tasks: {total}
Completed: {done} ({done/total*100:.1f}%)
In Progress: {in_progress}
Blocked: {blocked}

Total Estimated Effort: {total_estimated}h
Total Actual Effort: {total_actual}h

Project Health: {"🟢 Healthy" if blocked == 0 else "🟡 Some blockers" if blocked < 3 else "🔴 Critical"}
""")


if __name__ == "__main__":
    cli()