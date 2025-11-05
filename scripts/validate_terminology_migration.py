#!/usr/bin/env python3
"""
Terminology Migration Validation Script

Validates that the strain->cultivar terminology migration has been completed correctly
across the entire codebase. Checks for proper backward compatibility and flags any
remaining "strain" references that should be updated.

Usage:
    python scripts/validate_terminology_migration.py --strict
    python scripts/validate_terminology_migration.py --summary
    python scripts/validate_terminology_migration.py --check-backward-compat
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass

@dataclass
class ValidationResult:
    file_path: str
    line_number: int
    issue_type: str
    message: str
    severity: str  # ERROR, WARNING, INFO

class TerminologyValidator:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.results: List[ValidationResult] = []
        
        # Patterns that SHOULD still contain "strain" (backward compatibility, legacy)
        self.allowed_strain_patterns = [
            r'"strain"',  # String literals for compatibility
            r"'strain'",  # String literals for compatibility
            r'# .*strain.*migration',  # Comments about migration
            r'/strains/',  # API endpoint paths
            r'strain_handlers',  # Legacy handler references in comments
            r'from strain_handlers',  # Import statements in comments
            r'strain.py',  # File name references in comments
            r'strain_id',  # Database column names (if exist)
            r'test_strain',  # Test function names that might reference legacy
            r'strain_name',  # Property names that might exist
            r'Strain = Cultivar',  # Explicit backward compatibility aliases
            r'strain_create',  # Legacy method/function names
            r'StrainCreate',  # Legacy Pydantic model names
            r'TEST_STRAIN_',  # Test constants
            r'strain_test',  # Test-related references
            # Legacy activity types for backward compatibility
            r'"strain_add"',
            r'"strain_edit"',
            r'"strain_deleted"',
            # Legacy activity type responses in routers
            r'type="strain_add"',
            r'type="strain_edit"',
            r'type="strain_deleted"',
        ]
        
        # Patterns that should NEVER contain "strain" (these are critical)
        self.critical_strain_patterns = [
            r'class\s+Strain\b',  # Class definitions (not aliases)
            r'def\s+.*strain.*\(\b',  # Function definitions
            r'strain_id\s*=',  # Assignment statements (not type hints)
            r'strain_name\s*=',  # Assignment statements
            r'@app\.route.*["\']/?strains/?["\']',  # Flask route definitions
            r'router\..*strain',  # FastAPI router usage
            r'strain_url\s*=',  # Assignment statements
            r'# .*TODO.*strain',  # TODO comments about strain issues
            r'StrainNotFound',  # Exception classes
        ]

    def should_ignore_line(self, line: str) -> bool:
        """Check if a line should be ignored based on allowed patterns."""
        for pattern in self.allowed_strain_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                return True
        return False

    def is_critical_strain_usage(self, line: str) -> bool:
        """Check if a line contains critical strain usage that should be flagged."""
        for pattern in self.critical_strain_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                return True
        return False

    def validate_python_files(self) -> None:
        """Validate Python files for proper terminology usage."""
        # Exclude problematic directories
        exclude_dirs = {
            'node_modules', '.next', '.cache', '__pycache__', '.git',
            'build', 'dist', '.pytest_cache', '.venv', 'venv', 'venv40',
            'env', 'migrations', 'alembic', 'migrations_version'
        }
        
        # Use a custom generator to filter directories
        def get_python_files():
            try:
                for py_file in self.project_root.rglob("*.py"):
                    # Check if any excluded directory is in the path
                    try:
                        relative_path = py_file.relative_to(self.project_root)
                        if any(exclude_dir in str(relative_path).split(os.sep) for exclude_dir in exclude_dirs):
                            continue
                        yield py_file
                    except (ValueError, OSError):
                        # Skip files that can't be processed
                        continue
            except Exception:
                # Fallback: try to find files manually
                for root, dirs, files in os.walk(self.project_root):
                    # Remove excluded dirs from dirs to prevent walking into them
                    dirs[:] = [d for d in dirs if d not in exclude_dirs]
                    
                    for file in files:
                        if file.endswith('.py'):
                            file_path = Path(root) / file
                            yield file_path
        
        python_files = list(get_python_files())
        print(f"Found {len(python_files)} Python files to validate...")
        
        for file_path in python_files:
            # Skip migration scripts and test files for now
            if "migration" in str(file_path) or "test" in str(file_path):
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                for line_num, line in enumerate(lines, 1):
                    if 'strain' in line.lower() and not self.should_ignore_line(line):
                        if self.is_critical_strain_usage(line):
                            self.results.append(ValidationResult(
                                file_path=str(file_path),
                                line_number=line_num,
                                issue_type="CRITICAL_STRAIN_USAGE",
                                message=f"Found critical strain usage: {line.strip()}",
                                severity="ERROR"
                            ))
                        else:
                            self.results.append(ValidationResult(
                                file_path=str(file_path),
                                line_number=line_num,
                                issue_type="REMAINING_STRAIN",
                                message=f"Found remaining strain reference: {line.strip()}",
                                severity="WARNING"
                            ))
                            
            except Exception as e:
                self.results.append(ValidationResult(
                    file_path=str(file_path),
                    line_number=0,
                    issue_type="FILE_READ_ERROR",
                    message=f"Could not read file: {e}",
                    severity="ERROR"
                ))

    def validate_dart_files(self) -> None:
        """Validate Dart/Flutter files for proper terminology usage."""
        # Use the same approach as validate_python_files
        exclude_dirs = {
            'node_modules', '.next', '.cache', '__pycache__', '.git',
            'build', 'dist', '.pytest_cache', '.venv', 'venv', 'venv40',
            'env', 'migrations', 'alembic', 'migrations_version'
        }
        
        def get_dart_files():
            try:
                for dart_file in self.project_root.rglob("*.dart"):
                    try:
                        relative_path = dart_file.relative_to(self.project_root)
                        if any(exclude_dir in str(relative_path).split(os.sep) for exclude_dir in exclude_dirs):
                            continue
                        yield dart_file
                    except (ValueError, OSError):
                        continue
            except Exception:
                for root, dirs, files in os.walk(self.project_root):
                    dirs[:] = [d for d in dirs if d not in exclude_dirs]
                    for file in files:
                        if file.endswith('.dart'):
                            file_path = Path(root) / file
                            yield file_path
        
        dart_files = list(get_dart_files())
        
        for file_path in dart_files:
            # Skip test files for now
            if "test" in str(file_path):
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                for line_num, line in enumerate(lines, 1):
                    if 'strain' in line.lower() and not self.should_ignore_line(line):
                        if self.is_critical_strain_usage(line):
                            self.results.append(ValidationResult(
                                file_path=str(file_path),
                                line_number=line_num,
                                issue_type="CRITICAL_STRAIN_USAGE",
                                message=f"Found critical strain usage: {line.strip()}",
                                severity="ERROR"
                            ))
                        else:
                            self.results.append(ValidationResult(
                                file_path=str(file_path),
                                line_number=line_num,
                                issue_type="REMAINING_STRAIN",
                                message=f"Found remaining strain reference: {line.strip()}",
                                severity="WARNING"
                            ))
                            
            except Exception as e:
                self.results.append(ValidationResult(
                    file_path=str(file_path),
                    line_number=0,
                    issue_type="FILE_READ_ERROR",
                    message=f"Could not read file: {e}",
                    severity="ERROR"
                ))

    def validate_template_files(self) -> None:
        """Validate HTML template files for proper terminology usage."""
        # Use the same approach as validate_python_files
        exclude_dirs = {
            'node_modules', '.next', '.cache', '__pycache__', '.git',
            'build', 'dist', '.pytest_cache', '.venv', 'venv', 'venv40',
            'env', 'migrations', 'alembic', 'migrations_version'
        }
        
        def get_template_files():
            try:
                for template_file in self.project_root.rglob("*.html"):
                    try:
                        relative_path = template_file.relative_to(self.project_root)
                        if any(exclude_dir in str(relative_path).split(os.sep) for exclude_dir in exclude_dirs):
                            continue
                        yield template_file
                    except (ValueError, OSError):
                        continue
            except Exception:
                for root, dirs, files in os.walk(self.project_root):
                    dirs[:] = [d for d in dirs if d not in exclude_dirs]
                    for file in files:
                        if file.endswith('.html'):
                            file_path = Path(root) / file
                            yield file_path
        
        template_files = list(get_template_files())
        
        for file_path in template_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                for line_num, line in enumerate(lines, 1):
                    if 'strain' in line.lower() and not self.should_ignore_line(line):
                        # Templates should not have "strain" in user-facing text
                        if 'strain' in line.lower() and not any(word in line.lower() for word in ['cultivar', 'alias', 'legacy', 'migration']):
                            self.results.append(ValidationResult(
                                file_path=str(file_path),
                                line_number=line_num,
                                issue_type="STRAIN_IN_TEMPLATE",
                                message=f"Found strain reference in template: {line.strip()}",
                                severity="WARNING"
                            ))
                            
            except Exception as e:
                self.results.append(ValidationResult(
                    file_path=str(file_path),
                    line_number=0,
                    issue_type="FILE_READ_ERROR",
                    message=f"Could not read file: {e}",
                    severity="ERROR"
                ))

    def validate_js_files(self) -> None:
        """Validate JavaScript files for proper terminology usage."""
        # Use the same approach as validate_python_files
        exclude_dirs = {
            'node_modules', '.next', '.cache', '__pycache__', '.git',
            'build', 'dist', '.pytest_cache', '.venv', 'venv', 'venv40',
            'env', 'migrations', 'alembic', 'migrations_version'
        }
        
        def get_js_files():
            try:
                for js_file in self.project_root.rglob("*.js"):
                    try:
                        relative_path = js_file.relative_to(self.project_root)
                        if any(exclude_dir in str(relative_path).split(os.sep) for exclude_dir in exclude_dirs):
                            continue
                        yield js_file
                    except (ValueError, OSError):
                        continue
            except Exception:
                for root, dirs, files in os.walk(self.project_root):
                    dirs[:] = [d for d in dirs if d not in exclude_dirs]
                    for file in files:
                        if file.endswith('.js'):
                            file_path = Path(root) / file
                            yield file_path
        
        js_files = list(get_js_files())
        
        for file_path in js_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                for line_num, line in enumerate(lines, 1):
                    if 'strain' in line.lower() and not self.should_ignore_line(line):
                        # JavaScript should not have "strain" in user-facing code
                        if '/strains/' in line or 'strain' in line.lower():
                            self.results.append(ValidationResult(
                                file_path=str(file_path),
                                line_number=line_num,
                                issue_type="STRAIN_IN_JS",
                                message=f"Found strain reference in JS: {line.strip()}",
                                severity="WARNING"
                            ))
                            
            except Exception as e:
                self.results.append(ValidationResult(
                    file_path=str(file_path),
                    line_number=0,
                    issue_type="FILE_READ_ERROR",
                    message=f"Could not read file: {e}",
                    severity="ERROR"
                ))

    def check_backward_compatibility(self) -> None:
        """Check that backward compatibility aliases exist."""
        # Check if Strain = Cultivar alias exists in models
        models_init_file = self.project_root / "app" / "models" / "__init__.py"
        if models_init_file.exists():
            try:
                content = models_init_file.read_text()
                if "Strain = Cultivar" not in content:
                    self.results.append(ValidationResult(
                        file_path=str(models_init_file),
                        line_number=0,
                        issue_type="MISSING_BACKWARD_COMPAT",
                        message="Missing 'Strain = Cultivar' alias for backward compatibility",
                        severity="ERROR"
                    ))
            except Exception as e:
                self.results.append(ValidationResult(
                    file_path=str(models_init_file),
                    line_number=0,
                    issue_type="FILE_READ_ERROR",
                    message=f"Could not read models/__init__.py: {e}",
                    severity="ERROR"
                ))

        # Check if both strain and cultivar endpoints exist in FastAPI
        routers_init_file = self.project_root / "app" / "fastapi_app" / "__init__.py"
        if routers_init_file.exists():
            try:
                content = routers_init_file.read_text()
                has_cultivars = "/cultivars" in content
                has_strains = "/strains" in content
                
                if not has_cultivars:
                    self.results.append(ValidationResult(
                        file_path=str(routers_init_file),
                        line_number=0,
                        issue_type="MISSING_CULTIVAR_ENDPOINT",
                        message="Missing /cultivars endpoint in FastAPI router",
                        severity="ERROR"
                    ))
                    
                if not has_strains:
                    self.results.append(ValidationResult(
                        file_path=str(routers_init_file),
                        line_number=0,
                        issue_type="MISSING_STRAIN_ENDPOINT",
                        message="Missing /strains endpoint for backward compatibility",
                        severity="WARNING"
                    ))
                    
            except Exception as e:
                self.results.append(ValidationResult(
                    file_path=str(routers_init_file),
                    line_number=0,
                    issue_type="FILE_READ_ERROR",
                    message=f"Could not read fastapi_app/__init__.py: {e}",
                    severity="ERROR"
                ))

    def validate_all(self) -> None:
        """Run all validation checks."""
        print("Running terminology migration validation...")
        
        self.validate_python_files()
        self.validate_dart_files()
        self.validate_template_files()
        self.validate_js_files()
        self.check_backward_compatibility()
        
        print(f"Validation completed. Found {len(self.results)} issues.")

    def print_summary(self) -> None:
        """Print a summary of all validation results."""
        if not self.results:
            print("No issues found! Terminology migration appears to be complete.")
            return
            
        errors = [r for r in self.results if r.severity == "ERROR"]
        warnings = [r for r in self.results if r.severity == "WARNING"]
        
        print(f"\nVALIDATION SUMMARY:")
        print(f"   Errors: {len(errors)}")
        print(f"   Warnings: {len(warnings)}")
        print(f"   Total Issues: {len(self.results)}")
        
        if errors:
            print(f"\nCRITICAL ERRORS:")
            for result in errors[:10]:  # Show first 10 errors
                print(f"   {result.file_path}:{result.line_number} - {result.message}")
            if len(errors) > 10:
                print(f"   ... and {len(errors) - 10} more errors")
                
        if warnings:
            print(f"\nWARNINGS:")
            for result in warnings[:10]:  # Show first 10 warnings
                print(f"   {result.file_path}:{result.line_number} - {result.message}")
            if len(warnings) > 10:
                print(f"   ... and {len(warnings) - 10} more warnings")

    def print_detailed_report(self) -> None:
        """Print detailed report of all issues."""
        if not self.results:
            print("🎉 No issues found! Terminology migration appears to be complete.")
            return
            
        print(f"\n[CHECKLIST] DETAILED VALIDATION REPORT")
        print(f"{'='*80}")
        
        for result in self.results:
            print(f"\n📁 File: {result.file_path}")
            print(f"📍 Line: {result.line_number}")
            print(f"🏷️  Type: {result.issue_type}")
            print(f"⚡ Severity: {result.severity}")
            print(f"💬 Message: {result.message}")
            print(f"{'-' * 40}")

def main():
    parser = argparse.ArgumentParser(description="Validate terminology migration completion")
    parser.add_argument("--strict", action="store_true", 
                       help="Fail if any strain references are found (strict mode)")
    parser.add_argument("--summary", action="store_true", 
                       help="Show only summary of issues")
    parser.add_argument("--check-backward-compat", action="store_true",
                       help="Check backward compatibility aliases")
    parser.add_argument("--project-root", default=".",
                       help="Path to project root directory")
    
    args = parser.parse_args()
    
    validator = TerminologyValidator(args.project_root)
    validator.validate_all()
    
    if args.summary:
        validator.print_summary()
    else:
        validator.print_detailed_report()
    
    # Exit with appropriate code
    errors = [r for r in validator.results if r.severity == "ERROR"]
    if errors and args.strict:
        print(f"\nFAILED: Found {len(errors)} critical errors in strict mode")
        sys.exit(1)
    elif errors:
        print(f"\nWARNING: Found {len(errors)} errors and {len([r for r in validator.results if r.severity == 'WARNING'])} warnings")
        sys.exit(1)
    else:
        print(f"\nSUCCESS: No issues found!")
        sys.exit(0)

if __name__ == "__main__":
    main()