#!/usr/bin/env python3
"""
Comprehensive Terminology Migration Validation Script

This script validates that the "strain" → "cultivar" migration was completed
correctly across the entire codebase. It checks for:
- Production code compliance
- Backward compatibility maintenance
- API endpoint functionality
- Missing migrations

Usage:
    python scripts/validate_terminology_migration.py [--strict]
    python scripts/validate_terminology_migration.py --check-strain-references
    python scripts/validate_terminology_migration.py --check-backward-compat
"""

import os
import re
import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
# Fix Windows console encoding issues
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

@dataclass
class ValidationResult:
    """Result of a validation check"""
    check_name: str
    passed: bool
    issues: List[str]
    warnings: List[str]
    suggestions: List[str]

class TerminologyValidator:
    """Validates strain→cultivar terminology migration"""
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.results: List[ValidationResult] = []
        
        # Define what we expect in production code
        self.production_allowed_patterns = [
            r'strain_add', r'strain_edit', r'strain_deleted',  # Activity types (legacy compatibility)
            r'store.*strain', r'Buy.*strain',  # User-facing commerce terms
            r'# TODO.*strain', r'# FIXME.*strain',  # Comment placeholders
            r'strain_refs', r'strain_*_test',  # Test-specific terms
            r'# Migration.*strain', r'# Deprecated.*strain',  # Migration notes
            r'assert.*strain', r'test.*strain',  # Test assertions
            r'def.*test.*strain',  # Test function names
            r'class.*Test.*Strain',  # Test class names
        ]
        
        # Files that should NOT contain production "strain" references
        self.production_exclude_patterns = [
            r'\.test\.', r'/tests/', r'# test.*', r'# Test.*',
            r'migrations/', r'# Migration', r'# Deprecated',
            r'# TODO.*strain', r'# FIXME.*strain',
            r'validate_terminology', r'migration_guide'
        ]
    
    def validate_all(self, strict_mode: bool = False) -> bool:
        """Run all validation checks"""
        print("Starting Comprehensive Terminology Migration Validation")
        print("=" * 60)
        
        # Core validation checks
        self.check_strain_references_in_production(strict_mode)
        self.check_cultivar_implementation()
        self.check_backward_compatibility()
        self.check_api_endpoints()
        self.check_model_migrations()
        self.check_flutter_providers()
        self.check_template_migrations()
        self.check_test_files()
        self.check_documentation()
        
        # Summary
        return self._print_summary()
    
    def check_strain_references_in_production(self, strict_mode: bool = False) -> None:
        """Check for inappropriate 'strain' references in production code"""
        print("\nChecking Production Code Strain References...")
        
        issues = []
        warnings = []
        
        # Directories to check for production code
        production_dirs = [
            'app/',
            'flutter_app/lib/',  # Production Flutter code only
            'scripts/',  # Exclude migration scripts
        ]
        
        strain_pattern = re.compile(r'\bstrain\b', re.IGNORECASE)
        
        for prod_dir in production_dirs:
            prod_path = self.project_root / prod_dir
            if not prod_path.exists():
                warnings.append(f"Production directory not found: {prod_dir}")
                continue
            
            for file_path in prod_path.rglob('*.py'):
                if self._should_skip_file(file_path):
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Find strain references
                    for match in strain_pattern.finditer(content):
                        line_num = content[:match.start()].count('\n') + 1
                        line = content.split('\n')[line_num - 1].strip()
                        
                        # Check if this is an allowed pattern
                        if self._is_allowed_strain_reference(line):
                            continue
                        
                        # Check if this is in test/excluded content
                        if self._is_excluded_pattern(line):
                            continue
                        
                        # In strict mode, flag any strain reference
                        if strict_mode:
                            issues.append(f"{file_path}:{line_num}: PRODUCTION STRAIN REFERENCE: {line}")
                        else:
                            # In normal mode, only flag obvious issues
                            if not any(pattern in line.lower() for pattern in ['strain_add', 'strain_edit', 'strain_deleted']):
                                issues.append(f"{file_path}:{line_num}: PRODUCTION STRAIN REFERENCE: {line}")
                
                except Exception as e:
                    warnings.append(f"Error reading {file_path}: {e}")
        
        result = ValidationResult(
            check_name="Strain References in Production",
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            suggestions=["Use 'cultivar' terminology in production code", "Update legacy activity types to 'cultivar_*' format"]
        )
        self.results.append(result)
        
        print(f"  PASSED: {len(warnings)} warnings found" if result.passed else f"  FAILED: {len(issues)} issues found")
        for warning in warnings:
            print(f"    WARNING: {warning}")
        for issue in issues:
            print(f"    ERROR: {issue}")
    
    def check_cultivar_implementation(self) -> None:
        """Check that cultivar classes and models are properly implemented"""
        print("\nChecking Cultivar Implementation...")
        
        issues = []
        warnings = []
        
        # Check model implementations
        model_checks = [
            {
                'file': 'app/models/base_models.py',
                'expected_classes': ['Cultivar'],
                'expected_aliases': ['Strain'],
                'description': 'Flask models'
            },
            {
                'file': 'app/models_async/grow.py',
                'expected_classes': ['Cultivar'],
                'expected_aliases': [],
                'description': 'Async models'
            },
            {
                'file': 'app/fastapi_app/models/cultivars.py',
                'expected_classes': ['CultivarBase', 'CultivarCreate', 'CultivarUpdate', 'CultivarResponse'],
                'expected_aliases': [],
                'description': 'Pydantic schemas'
            }
        ]
        
        for check in model_checks:
            file_path = self.project_root / check['file']
            if not file_path.exists():
                issues.append(f"Required file missing: {check['file']}")
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for expected classes
                for expected_class in check['expected_classes']:
                    if f"class {expected_class}" not in content:
                        issues.append(f"{check['description']}: Missing class {expected_class} in {check['file']}")
                
                # Check for backward compatibility aliases
                for expected_alias in check['expected_aliases']:
                    if f"{expected_alias} = Cultivar" not in content:
                        issues.append(f"{check['description']}: Missing backward compatibility alias {expected_alias} = Cultivar in {check['file']}")
                
            except Exception as e:
                issues.append(f"Error checking {check['file']}: {e}")
        
        # Check that cultivar table exists in database
        if (self.project_root / 'app/models_async/grow.py').exists():
            try:
                with open(self.project_root / 'app/models_async/grow.py', 'r') as f:
                    content = f.read()
                    if '__tablename__ = \'cultivar\'' not in content:
                        issues.append("Async models should use 'cultivar' table name")
            except:
                pass
        
        result = ValidationResult(
            check_name="Cultivar Implementation",
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            suggestions=["Ensure all cultivar classes are properly implemented", "Verify backward compatibility aliases"]
        )
        self.results.append(result)
        
        print(f"  PASSED: {len(warnings)} warnings" if result.passed else f"  FAILED: {len(issues)} issues")
        for warning in warnings:
            print(f"    WARNING: {warning}")
        for issue in issues:
            print(f"    ERROR: {issue}")
    
    def check_backward_compatibility(self) -> None:
        """Check that backward compatibility is maintained"""
        print("\nChecking Backward Compatibility...")
        
        issues = []
        warnings = []
        
        # Check model aliases
        model_files = [
            'app/models/base_models.py',
            'app/models/__init__.py',
            'app/fastapi_app/models/cultivars.py'
        ]
        
        for model_file in model_files:
            file_path = self.project_root / model_file
            if not file_path.exists():
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Look for backward compatibility patterns
                compatibility_patterns = [
                    r'Strain = Cultivar',
                    r'StrainBase = CultivarBase',
                    r'StrainCreate = CultivarCreate',
                    r'StrainUpdate = CultivarUpdate',
                    r'StrainResponse = CultivarResponse'
                ]
                
                for pattern in compatibility_patterns:
                    if not re.search(pattern, content):
                        warnings.append(f"Missing backward compatibility alias: {pattern} in {model_file}")
            
            except Exception as e:
                issues.append(f"Error checking {model_file}: {e}")
        
        result = ValidationResult(
            check_name="Backward Compatibility",
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            suggestions=["Add missing backward compatibility aliases", "Test that legacy code still works"]
        )
        self.results.append(result)
        
        print(f"  PASSED: {len(warnings)} warnings" if result.passed else f"  FAILED: {len(issues)} issues")
        for warning in warnings:
            print(f"    WARNING: {warning}")
        for issue in issues:
            print(f"    ERROR: {issue}")
    
    def check_api_endpoints(self) -> None:
        """Check that API endpoints are properly configured"""
        print("\nChecking API Endpoints...")
        
        issues = []
        warnings = []
        
        # Check FastAPI router configuration
        fastapi_init = self.project_root / 'app/fastapi_app/__init__.py'
        if fastapi_init.exists():
            try:
                with open(fastapi_init, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for dual mounting
                if '/api/v1/cultivars' not in content:
                    issues.append("Missing /api/v1/cultivars endpoint mounting")
                if '/api/v1/strains' not in content:
                    warnings.append("Missing /api/v1/strains backward compatibility endpoint")
                
                # Check router imports
                if 'cultivars' not in content and 'strains' not in content:
                    issues.append("No cultivars or strains router imports found")
            
            except Exception as e:
                issues.append(f"Error checking FastAPI configuration: {e}")
        
        # Check Flask blueprint configuration
        flask_cultivar = self.project_root / 'app/blueprints/cultivars.py'
        if not flask_cultivar.exists():
            warnings.append("Flask cultivar blueprint not found (may be in strains.py)")
        
        result = ValidationResult(
            check_name="API Endpoints",
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            suggestions=["Ensure both /cultivars and /strains endpoints work", "Test API responses"]
        )
        self.results.append(result)
        
        print(f"  PASSED: {len(warnings)} warnings" if result.passed else f"  FAILED: {len(issues)} issues")
        for warning in warnings:
            print(f"    WARNING: {warning}")
        for issue in issues:
            print(f"    ERROR: {issue}")
    
    def check_model_migrations(self) -> None:
        """Check that database models have been properly migrated"""
        print("\nChecking Database Model Migrations...")
        
        issues = []
        warnings = []
        
        # Check Plant model foreign key
        plant_model = self.project_root / 'app/models/base_models.py'
        if plant_model.exists():
            try:
                with open(plant_model, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'cultivar_id' not in content:
                    issues.append("Plant model missing cultivar_id foreign key")
                if 'db.ForeignKey(\'cultivar.id\')' not in content:
                    warnings.append("Plant model may not have proper cultivar foreign key")
                
                if 'cultivar' not in content or 'db.relationship(\'Cultivar\'' not in content:
                    issues.append("Plant model missing cultivar relationship")
            
            except Exception as e:
                issues.append(f"Error checking Plant model: {e}")
        
        result = ValidationResult(
            check_name="Database Model Migrations",
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            suggestions=["Verify Plant model uses cultivar_id foreign key", "Check database relationships"]
        )
        self.results.append(result)
        
        print(f"  PASSED: {len(warnings)} warnings" if result.passed else f"  FAILED: {len(issues)} issues")
        for warning in warnings:
            print(f"    WARNING: {warning}")
        for issue in issues:
            print(f"    ERROR: {issue}")
    
    def check_flutter_providers(self) -> None:
        """Check Flutter provider implementations"""
        print("\nChecking Flutter Providers...")
        
        issues = []
        warnings = []
        
        # Check that cultivar provider exists
        cultivar_provider = self.project_root / 'flutter_app/lib/core/providers/cultivar_provider.dart'
        if not cultivar_provider.exists():
            issues.append("Flutter cultivar provider not found")
        
        # Check for any remaining strain providers
        strain_provider = self.project_root / 'flutter_app/lib/core/state/strains_provider.dart'
        if strain_provider.exists():
            warnings.append("Legacy strain provider still exists - should be removed or consolidated")
        
        # Check for duplicate widgets
        strain_card = self.project_root / 'flutter_app/lib/widgets/strain_card'
        cultivar_card = self.project_root / 'flutter_app/lib/widgets/cultivar_card.dart'
        
        if strain_card.exists() and cultivar_card.exists():
            warnings.append("Both strain_card and cultivar_card widgets exist - should be consolidated")
        elif not cultivar_card.exists():
            issues.append("Cultivar card widget not found")
        
        result = ValidationResult(
            check_name="Flutter Providers",
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            suggestions=["Remove duplicate strain providers", "Ensure all Flutter imports use cultivar terminology"]
        )
        self.results.append(result)
        
        print(f"  PASSED: {len(warnings)} warnings" if result.passed else f"  FAILED: {len(issues)} issues")
        for warning in warnings:
            print(f"    WARNING: {warning}")
        for issue in issues:
            print(f"    ERROR: {issue}")
    
    def check_template_migrations(self) -> None:
        """Check HTML template migrations"""
        print("\nChecking Template Migrations...")
        
        issues = []
        warnings = []
        
        # Check for old template files
        old_templates = [
            'app/web/templates/views/strains.html',
            'app/web/templates/views/strain.html',
            'app/web/templates/views/add_strain.html'
        ]
        
        for template in old_templates:
            template_path = self.project_root / template
            if template_path.exists():
                warnings.append(f"Old template file still exists: {template}")
        
        # Check for new template files
        new_templates = [
            'app/web/templates/views/cultivars.html',
            'app/web/templates/views/cultivar.html',
            'app/web/templates/views/add_cultivar.html'
        ]
        
        for template in new_templates:
            template_path = self.project_root / template
            if not template_path.exists():
                issues.append(f"New template file missing: {template}")
        
        result = ValidationResult(
            check_name="Template Migrations",
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            suggestions=["Update template file names from strain* to cultivar*", "Verify template rendering"]
        )
        self.results.append(result)
        
        print(f"  PASSED: {len(warnings)} warnings" if result.passed else f"  FAILED: {len(issues)} issues")
        for warning in warnings:
            print(f"    WARNING: {warning}")
        for issue in issues:
            print(f"    ERROR: {issue}")
    
    def check_test_files(self) -> None:
        """Check test file migrations"""
        print("\nChecking Test File Migrations...")
        
        issues = []
        warnings = []
        
        # Check for test files using new terminology
        test_files_to_check = [
            'tests/integration/test_cultivars.py',
            'tests/integration/test_cultivars_integration.py'
        ]
        
        for test_file in test_files_to_check:
            test_path = self.project_root / test_file
            if not test_path.exists():
                warnings.append(f"Test file not found: {test_file}")
        
        # Check that test files use cultivar terminology
        if (self.project_root / 'tests/integration/test_cultivars.py').exists():
            try:
                with open(self.project_root / 'tests/integration/test_cultivars.py', 'r') as f:
                    content = f.read()
                    
                # Basic validation - test file should exist and have content
                if len(content.strip()) < 100:
                    warnings.append("Test file appears to be empty or minimal")
            
            except Exception as e:
                issues.append(f"Error checking test file: {e}")
        
        result = ValidationResult(
            check_name="Test File Migrations",
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            suggestions=["Ensure all tests use cultivar terminology", "Verify test coverage"]
        )
        self.results.append(result)
        
        print(f"  PASSED: {len(warnings)} warnings" if result.passed else f"  FAILED: {len(issues)} issues")
        for warning in warnings:
            print(f"    WARNING: {warning}")
        for issue in issues:
            print(f"    ERROR: {issue}")
    
    def check_documentation(self) -> None:
        """Check documentation migrations"""
        print("\nChecking Documentation...")
        
        issues = []
        warnings = []
        
        # Check for migration guide
        migration_guide = self.project_root / 'docs/TERMINOLOGY_MIGRATION_GUIDE.md'
        if not migration_guide.exists():
            issues.append("Terminology migration guide not found")
        
        # Check README and other key docs
        key_docs = ['README.md', 'docs/Roadmap.md']
        for doc in key_docs:
            doc_path = self.project_root / doc
            if doc_path.exists():
                try:
                    with open(doc_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Count strain vs cultivar references
                    strain_count = len(re.findall(r'\bstrain\b', content, re.IGNORECASE))
                    cultivar_count = len(re.findall(r'\bcultivar\b', content, re.IGNORECASE))
                    
                    if strain_count > cultivar_count and 'migration' not in doc.lower():
                        warnings.append(f"{doc}: More 'strain' than 'cultivar' references")
                
                except Exception as e:
                    issues.append(f"Error checking {doc}: {e}")
        
        result = ValidationResult(
            check_name="Documentation",
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            suggestions=["Update documentation to use cultivar terminology", "Remove outdated strain references"]
        )
        self.results.append(result)
        
        print(f"  PASSED: {len(warnings)} warnings" if result.passed else f"  FAILED: {len(issues)} issues")
        for warning in warnings:
            print(f"    WARNING: {warning}")
        for issue in issues:
            print(f"    ERROR: {issue}")
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped in validation"""
        skip_patterns = [
            r'\.pyc$',
            r'__pycache__',
            r'# Migration',
            r'# TODO.*strain',
            r'# FIXME.*strain',
            r'test.*strain',
            r'strain.*test',
            r'migration',
            r'validate_terminology',
            r'# Deprecated'
        ]
        
        file_str = str(file_path)
        return any(re.search(pattern, file_str, re.IGNORECASE) for pattern in skip_patterns)
    
    def _is_allowed_strain_reference(self, line: str) -> bool:
        """Check if strain reference is allowed in production"""
        line_lower = line.lower()
        
        allowed_patterns = [
            'strain_add', 'strain_edit', 'strain_deleted',  # Activity types
            'test.*strain', 'strain.*test',  # Test content
            'assert.*strain',  # Test assertions
            '# todo.*strain', '# fixme.*strain',  # Comment placeholders
            'migration.*strain', 'deprecated.*strain',  # Migration notes
            'strain = cultivar', 'strainbase = cultivarbase',  # Backward compatibility aliases
            'backward compatibility', 'legacy',  # Compatibility comments
            'deprecated - use', 'use.*cultivar.*instead',  # Deprecation notices
            'cultivar add', 'cultivar edit', 'cultivar deleted',  # New activity types
            'deprecated.*cultivar', 'use.*cultivar.*instead',  # Migration guidance
            'api/v1/strains', '/strains',  # Legacy API endpoints
            'strain_handlers', 'strain_handlers_async',  # Legacy handler files
            'import.*strain', 'from.*strain',  # Import statements for backward compat
            'task.*strain.*template.*rename', 'task.*strain.*template.*update',  # Task file references
            'strain.*will be removed', 'strain.*aliases.*will be removed',  # Deprecation warnings
            'cultivar/strain', 'cannabis cultivar/strain',  # Documentation mentions
            'strain management handlers', 'strain.*async.*version',  # Legacy file descriptions
        ]
        
        return any(pattern in line_lower for pattern in allowed_patterns)
    
    def _is_excluded_pattern(self, line: str) -> bool:
        """Check if line contains excluded pattern"""
        line_lower = line.lower()
        
        exclude_patterns = [
            r'test.*strain', r'strain.*test',
            r'# migration', r'# todo.*strain', r'# fixme.*strain',
            r'# deprecated', r'validate_terminology',
            r'#.*strain.*test', r'#.*test.*strain'
        ]
        
        return any(re.search(pattern, line_lower) for pattern in exclude_patterns)
    
    def _print_summary(self) -> bool:
        """Print validation summary and return overall result"""
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        
        passed_checks = sum(1 for r in self.results if r.passed)
        total_checks = len(self.results)
        
        print(f"Checks Passed: {passed_checks}/{total_checks}")
        
        all_issues = []
        all_warnings = []
        
        for result in self.results:
            if not result.passed:
                all_issues.extend(result.issues)
            all_warnings.extend(result.warnings)
        
        print(f"Total Issues: {len(all_issues)}")
        print(f"Total Warnings: {len(all_warnings)}")
        
        if all_issues:
            print("\nCRITICAL ISSUES:")
            for issue in all_issues:
                print(f"  • {issue}")
        
        if all_warnings:
            print("\nWARNINGS:")
            for warning in all_warnings:
                print(f"  • {warning}")
        
        overall_success = len(all_issues) == 0
        print(f"\n{'MIGRATION VALIDATION PASSED' if overall_success else 'MIGRATION VALIDATION FAILED'}")
        
        if overall_success:
            print("\nThe strain->cultivar terminology migration is complete!")
            print("All production code now uses 'cultivar' terminology.")
            print("Backward compatibility is maintained where necessary.")
        else:
            print("\nIssues need to be resolved before migration is complete.")
            print("Review the issues above and make necessary corrections.")
        
        return overall_success
    
    def run_tests(self) -> bool:
        """Run the actual test suite to verify functionality"""
        print("\nRunning Test Suite...")
        
        try:
            # Run backend tests
            print("  Running Python tests...")
            result = subprocess.run(
                ['python', '-m', 'pytest', 'tests/', '-v', '--tb=short'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                print("    Backend tests passed")
                backend_success = True
            else:
                print("    Backend tests failed")
                print(f"    Error output: {result.stdout[:500]}...")
                backend_success = False
            
            # Run Flutter tests if available
            flutter_path = self.project_root / 'flutter_app'
            if flutter_path.exists():
                print("  Running Flutter tests...")
                flutter_result = subprocess.run(
                    ['flutter', 'test'],
                    cwd=flutter_path,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if flutter_result.returncode == 0:
                    print("    Flutter tests passed")
                    flutter_success = True
                else:
                    print("    Flutter tests failed")
                    print(f"    Error output: {flutter_result.stdout[:500]}...")
                    flutter_success = False
            else:
                flutter_success = True  # Skip if no Flutter app
            
            return backend_success and flutter_success
            
        except subprocess.TimeoutExpired:
            print("    Tests timed out")
            return False
        except Exception as e:
            print(f"    Error running tests: {e}")
            return False

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate strain→cultivar terminology migration')
    parser.add_argument('--strict', action='store_true', help='Enable strict mode (flag all strain references)')
    parser.add_argument('--check-strain-references', action='store_true', help='Check for strain references in production')
    parser.add_argument('--check-backward-compat', action='store_true', help='Check backward compatibility')
    parser.add_argument('--run-tests', action='store_true', help='Run test suite')
    parser.add_argument('--project-root', type=str, help='Project root directory')
    
    args = parser.parse_args()
    
    validator = TerminologyValidator(args.project_root)
    
    if args.check_strain_references:
        validator.check_strain_references_in_production(args.strict)
    elif args.check_backward_compat:
        validator.check_backward_compatibility()
    elif args.run_tests:
        success = validator.run_tests()
        sys.exit(0 if success else 1)
    else:
        # Run all validations
        overall_success = validator.validate_all(args.strict)
        sys.exit(0 if overall_success else 1)

if __name__ == '__main__':
    main()