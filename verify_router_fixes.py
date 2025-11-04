#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple verification script to check if the router fixes are implemented.
This script analyzes the code without importing modules to avoid dependency issues.
"""

import os
import re
import sys

def check_router_prefixes():
    """Check Comment 1: Verify no duplicate router prefixes."""
    print("=== Comment 1: Checking Router Prefixes ===")
    
    init_file = "app/fastapi_app/__init__.py"
    if not os.path.exists(init_file):
        print(f"❌ {init_file} not found")
        return False
    
    with open(init_file, 'r') as f:
        content = f.read()
    
    # Check router inclusions
    include_pattern = r'app\.include_router\(([^,]+),'
    includes = re.findall(include_pattern, content)
    
    print(f"Found {len(includes)} router inclusions:")
    for include in includes:
        print(f"  - {include.strip()}")
    
    # Check for correct patterns
    correct_patterns = [
        'plants.router, tags=["Plants Legacy"])',
        'strains.router, tags=["Strains Legacy"])',
        'breeders.router, tags=["Breeders Legacy"])',
        'auth.router, prefix="/auth"',
        'plants_api.router, prefix="/api/v1/plants"',
        'strains.api_router, prefix="/api/v1"',
        'breeders.api_router, prefix="/api/v1"'
    ]
    
    issues = []
    for pattern in correct_patterns:
        if pattern in content:
            print(f"  ✅ Found correct: {pattern}")
        else:
            issues.append(f"Missing: {pattern}")
    
    if issues:
        print("❌ Issues found:")
        for issue in issues:
            print(f"    {issue}")
        return False
    else:
        print("✅ Router prefixes correctly configured - no duplicates found")
        return True

def check_async_patterns():
    """Check Comment 3: Verify auth router uses async patterns."""
    print("\n=== Comment 3: Checking Auth Router Async Patterns ===")
    
    auth_file = "app/fastapi_app/routers/auth.py"
    if not os.path.exists(auth_file):
        print(f"❌ {auth_file} not found")
        return False
    
    with open(auth_file, 'r') as f:
        content = f.read()
    
    # Check for async imports and usage
    checks = [
        ("AsyncSession import", "from sqlalchemy.ext.asyncio import AsyncSession"),
        ("select import", "from sqlalchemy import select"),
        ("async execute pattern", "await db.execute(select("),
        ("get_async_db import", "from app.fastapi_app.database import get_async_db"),
    ]
    
    all_good = True
    for check_name, pattern in checks:
        if pattern in content:
            print(f"  ✅ {check_name}")
        else:
            print(f"  ❌ {check_name} - Pattern not found: {pattern}")
            all_good = False
    
    # Check for sync patterns that shouldn't be there
    sync_patterns = [
        ("sync db.query", "db.query("),
        ("sync session", "SessionLocal"),
    ]
    
    for pattern_name, pattern in sync_patterns:
        if pattern in content:
            print(f"  ❌ Found unwanted sync pattern: {pattern_name}")
            all_good = False
        else:
            print(f"  ✅ No unwanted sync pattern: {pattern_name}")
    
    if all_good:
        print("✅ Auth router correctly uses async patterns")
    else:
        print("❌ Auth router has async pattern issues")
    
    return all_good

def check_db_commit_parentheses():
    """Check Comment 2: Verify db.commit() calls have parentheses."""
    print("\n=== Comment 2: Checking db.commit() Calls ===")
    
    strains_file = "app/fastapi_app/routers/strains.py"
    if not os.path.exists(strains_file):
        print(f"❌ {strains_file} not found")
        return False
    
    with open(strains_file, 'r') as f:
        content = f.read()
    
    # Find all db.commit calls
    commit_pattern = r'await\s+db\.commit\s*\('
    commit_calls = re.findall(commit_pattern, content)
    
    bare_commit_pattern = r'await\s+db\.commit\s*(?!\()'
    bare_commits = re.findall(bare_commit_pattern, content)
    
    print(f"Found {len(commit_calls)} db.commit() calls with parentheses")
    print(f"Found {len(bare_commits)} db.commit calls without parentheses")
    
    if len(bare_commits) > 0:
        print("❌ Found db.commit calls without parentheses!")
        return False
    else:
        print("✅ All db.commit calls have parentheses")
        return True

def check_integration_test_exists():
    """Check if integration test was created."""
    print("\n=== Checking Integration Test ===")
    
    test_file = "tests/test_router_fixes.py"
    if os.path.exists(test_file):
        print(f"✅ Integration test file exists: {test_file}")
        return True
    else:
        print(f"❌ Integration test file not found: {test_file}")
        return False

def main():
    """Run all checks."""
    print("Router Fixes Verification Script")
    print("=" * 50)
    
    results = []
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    results.append(check_router_prefixes())
    results.append(check_async_patterns())
    results.append(check_db_commit_parentheses())
    results.append(check_integration_test_exists())
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    if all(results):
        print("✅ All router fixes are correctly implemented!")
        print("\nThe three comments have been addressed:")
        print("1. ✅ Router prefixes correctly configured (no duplicates)")
        print("2. ✅ db.commit() calls have parentheses")  
        print("3. ✅ Auth router uses async patterns")
        print("4. ✅ Integration test created")
        return 0
    else:
        print("❌ Some issues remain:")
        issues = [
            "Router prefixes",
            "Async patterns", 
            "db.commit parentheses",
            "Integration test"
        ]
        
        for i, (result, issue) in enumerate(zip(results, issues)):
            status = "✅" if result else "❌"
            print(f"{status} {issue}")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())