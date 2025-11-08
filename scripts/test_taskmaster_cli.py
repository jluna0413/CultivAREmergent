#!/usr/bin/env python3
"""
Task-Master CLI Test Suite

Minimal test suite for the Task-Master CLI tool.
"""

import json
import os
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the scripts directory to the path to import the CLI
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from taskmaster_cli import TaskMasterCLI


class TestTaskMasterCLI:
    """Test cases for TaskMasterCLI"""
    
    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.tasks_dir = Path(self.temp_dir) / 'tasks'
        self.reports_dir = Path(self.temp_dir) / 'reports'
        self.backup_dir = Path(self.temp_dir) / 'backups'
        
        # Create directory structure
        self.tasks_dir.mkdir(parents=True)
        self.reports_dir.mkdir(parents=True)
        self.backup_dir.mkdir(parents=True)
        
        # Create test config
        self.config = {
            "taskmaster": {
                "task_directory": str(self.tasks_dir),
                "default_assignee": "@testuser",
                "status_values": ["TODO", "IN_PROGRESS", "BLOCKED", "REVIEW", "DONE"],
                "priority_values": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
                "type_values": ["EPIC", "FEATURE", "BUG", "REFACTOR"]
            }
        }
        
        # Create test tasks
        self.test_tasks = [
            {
                "id": "test-task-1",
                "title": "Test Task 1",
                "description": "First test task",
                "status": "TODO",
                "priority": "HIGH",
                "assignee": "@testuser",
                "created_at": "2025-01-01T00:00:00Z",
                "updated_at": "2025-01-01T00:00:00Z"
            },
            {
                "id": "test-task-2", 
                "title": "Test Task 2",
                "description": "Second test task",
                "status": "IN_PROGRESS",
                "priority": "MEDIUM",
                "assignee": "@testuser",
                "created_at": "2025-01-01T00:00:00Z",
                "updated_at": "2025-01-01T00:00:00Z"
            },
            {
                "id": "test-task-3",
                "title": "Test Task 3",
                "description": "Third test task",
                "status": "DONE",
                "priority": "LOW",
                "assignee": "@otheruser",
                "created_at": "2025-01-01T00:00:00Z",
                "updated_at": "2025-01-01T00:00:00Z",
                "completed_at": "2025-01-02T00:00:00Z"
            }
        ]
        
        # Write test tasks
        for task in self.test_tasks:
            task_file = self.tasks_dir / f"{task['id']}.json"
            with open(task_file, 'w') as f:
                json.dump(task, f, indent=2)
    
    def teardown_method(self):
        """Cleanup test environment"""
        shutil.rmtree(self.temp_dir)
    
    @patch('builtins.open')
    @patch('json.load')
    def test_load_config(self, mock_json_load, mock_open):
        """Test configuration loading"""
        mock_json_load.return_value = self.config
        
        cli = TaskMasterCLI()
        
        assert cli.tasks_dir == self.tasks_dir
        assert cli.reports_dir == self.reports_dir
        assert cli.backup_dir == self.backup_dir
        assert cli.status_values == self.config['taskmaster']['status_values']
        assert cli.priority_values == self.config['taskmaster']['priority_values']
    
    def test_get_all_tasks(self):
        """Test getting all tasks"""
        with patch.object(Path, 'glob') as mock_glob:
            mock_glob.return_value = [
                self.tasks_dir / 'test-task-1.json',
                self.tasks_dir / 'test-task-2.json', 
                self.tasks_dir / 'test-task-3.json'
            ]
            
            # Mock file reading
            def mock_read_json(file_path):
                for task in self.test_tasks:
                    if f"{task['id']}.json" in str(file_path):
                        return task
                return None
            
            with patch.object(TaskMasterCLI, '_safe_read_json', side_effect=mock_read_json):
                cli = TaskMasterCLI()
                tasks = cli._get_all_tasks()
                
                assert len(tasks) == 3
                task_ids = [t['id'] for t in tasks]
                assert 'test-task-1' in task_ids
                assert 'test-task-2' in task_ids
                assert 'test-task-3' in task_ids
    
    def test_find_task_by_id(self):
        """Test finding a specific task"""
        with patch.object(Path, 'glob') as mock_glob:
            mock_glob.return_value = [self.tasks_dir / 'test-task-1.json']
            
            with patch.object(TaskMasterCLI, '_safe_read_json', return_value=self.test_tasks[0]):
                cli = TaskMasterCLI()
                task = cli._find_task_by_id('test-task-1')
                
                assert task is not None
                assert task['id'] == 'test-task-1'
                assert task['title'] == 'Test Task 1'
    
    def test_validate_status(self):
        """Test status validation"""
        cli = TaskMasterCLI()
        
        assert cli._validate_status('TODO') == True
        assert cli._validate_status('IN_PROGRESS') == True
        assert cli._validate_status('DONE') == True
        assert cli._validate_status('INVALID') == False
    
    def test_validate_priority(self):
        """Test priority validation"""
        cli = TaskMasterCLI()
        
        assert cli._validate_priority('LOW') == True
        assert cli._validate_priority('HIGH') == True
        assert cli._validate_priority('CRITICAL') == True
        assert cli._validate_priority('INVALID') == False


def run_tests():
    """Run all tests"""
    print("Running Task-Master CLI tests...")
    
    test_instance = TestTaskMasterCLI()
    test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
    
    passed = 0
    failed = 0
    
    for method_name in test_methods:
        try:
            print(f"  Running {method_name}...")
            method = getattr(test_instance, method_name)
            method()
            print(f"    ✓ {method_name} PASSED")
            passed += 1
        except Exception as e:
            print(f"    ✗ {method_name} FAILED: {e}")
            failed += 1
    
    print(f"\nTest Results: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)