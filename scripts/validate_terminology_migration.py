#!/usr/bin/env python3
"""
Strain→Cultivar Terminology Migration Validation Script

This script validates that the strain-to-cultivar terminology migration has been
completed successfully across the entire codebase.

Usage:
    python scripts/validate_terminology_migration.py [--strict]
"""

import os
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Dict, List

class MigrationValidator:
    def __init__(self, strict_mode: bool = False):
        self.strict_mode = strict_mode
        self.issues = defaultdict(list)
        self.warnings = defaultdict(list)
        self.project_root = Path(__file__).parent.parent
        
        # Files that should exist with cultivar names
        self.expected_cultivar_files = [
            'app/models/base_models.py',
            'app/models/__init__.py',
        ]

    def validate_file_structure(self) -> bool:
        """Validate that expected files exist with correct naming."""
        print("Validating file structure...")
        
        issues_found = False
        
        # Check for expected cultivar files
        missing_cultivar_files = []
        for file_path in self.expected_cultivar_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                missing_cultivar_files.append(file_path)
        
        if missing_cultivar_files:
            self.issues['file_structure'].extend([
                f"Missing expected cultivar file: {f}" for f in missing_cultivar_files
            ])
            issues_found = True
        
        return not issues_found

    def scan_python_files(self) -> bool:
        """Scan Python files for strain terminology violations."""
        print("Scanning Python files...")
        
        python_files = []
        # Only scan specific directories to avoid broken symlinks
        scan_dirs = ['app', 'scripts', 'tests', 'flutter_app/lib']
        for scan_dir in scan_dirs:
            scan_path = self.project_root / scan_dir
            if scan_path.exists():
                python_files.extend(scan_path.rglob('*.py'))
        
        issues_found = False
        
        for file_path in python_files:
            try:
                # Skip non-existent files (broken symlinks, etc.)
                if not file_path.exists() or not file_path.is_file():
                    continue
                    
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for critical strain patterns
                lines = content.split('\n')
                for line_num, line in enumerate(lines, 1):
                    # Look for Strain class definition without Cultivar alias
                    if ('class Strain(' in line and not line.strip().startswith('#')):
                        if 'class Cultivar(' not in content and 'Strain = Cultivar' not in content:
                            self.issues['python_files'].append(
                                f"{file_path.relative_to(self.project_root)}:{line_num}: Found Strain class without Cultivar alias"
                            )
                            issues_found = True
            except Exception as e:
                self.warnings['python_files'].append(f"Error reading {file_path}: {e}")
        
        return not issues_found

    def generate_report(self) -> Dict:
        """Generate a comprehensive validation report."""
        report = {
            'timestamp': __import__('datetime').datetime.now().isoformat(),
            'strict_mode': self.strict_mode,
            'project_root': str(self.project_root),
            'summary': {
                'total_issues': sum(len(issues) for issues in self.issues.values()),
                'total_warnings': sum(len(warnings) for warnings in self.warnings.values()),
                'passed': len(self.issues) == 0,
                'strict_passed': self.strict_mode or len(self.issues) == 0
            },
            'issues': dict(self.issues),
            'warnings': dict(self.warnings),
            'recommendations': []
        }
        
        # Generate recommendations based on issues
        if self.issues:
            report['recommendations'].extend([
                "Review and fix critical terminology violations",
                "Ensure backward compatibility aliases are in place",
                "Update any remaining legacy references"
            ])
        
        return report

    def run_validation(self) -> bool:
        """Run the complete validation process."""
        print("Starting Strain->Cultivar Migration Validation")
        print("=" * 60)
        
        validations = [
            ("File Structure", self.validate_file_structure),
            ("Python Files", self.scan_python_files),
        ]
        
        all_passed = True
        for name, validator in validations:
            try:
                passed = validator()
                status = "PASS" if passed else "FAIL"
                print(f"{name}: {status}")
                if not passed:
                    all_passed = False
            except Exception as e:
                print(f"{name}: ERROR - {e}")
                self.issues[name].append(f"Validation error: {e}")
                all_passed = False
        
        print("=" * 60)
        
        # Generate report
        report = self.generate_report()
        
        # Save report
        report_path = self.project_root / 'migration_validation_report.json'
        try:
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"Validation report saved to: {report_path}")
        except Exception as e:
            print(f"Failed to save report: {e}")
        
        print(f"Summary: {report['summary']['total_issues']} issues, {report['summary']['total_warnings']} warnings")
        
        if all_passed:
            print("Migration validation PASSED!")
        else:
            print("Migration validation FAILED!")
            if self.strict_mode:
                print("Strict mode enabled - validation must pass 100%")
        
        return all_passed

def main():
    parser = argparse.ArgumentParser(description='Validate strain→cultivar terminology migration')
    parser.add_argument('--strict', action='store_true', 
                       help='Enable strict mode - any issues will cause failure')
    parser.add_argument('--report-only', action='store_true',
                       help='Only generate report, do not exit on failures')
    
    args = parser.parse_args()
    
    validator = MigrationValidator(strict_mode=args.strict)
    success = validator.run_validation()
    
    if not args.report_only and not success:
        if args.strict:
            sys.exit(1)
        else:
            sys.exit(1)

if __name__ == '__main__':
    main()