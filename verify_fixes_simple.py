#!/usr/bin/env python3
"""
Simple script to verify that all three comments have been implemented correctly.
"""

import os
import re

def verify_comment_1_duplicate_prefixes():
    """Verify Comment 1: No duplicate router prefixes."""
    print("=== Comment 1: Router Prefixes ===")
    
    init_file = "app/fastapi_app/__init__.py"
    with open(init_file, 'r') as f:
        content = f.read()
    
    # Check that routers with internal prefixes don't get additional prefixes
    checks = [
        ('plants.router', 'prefix="/plants"' not in content),
        ('strains.router', 'prefix="/strains"' not in content), 
        ('breeders.router', 'prefix="/breeders"' not in content),
        ('strains.api_router', 'prefix="/api/v1"' in content),
        ('breeders.api_router', 'prefix="/api/v1"' in content),
        ('auth.router', 'prefix="/auth"' in content),
    ]
    
    all_good = True
    for router_name, should_not_have_prefix in checks:
        if should_not_have_prefix:
            if f'{router_name},' in content and f'prefix="/' in content[content.find(f'{router_name},'):]:
                print(f"  FAIL: {router_name} has duplicate prefix")
                all_good = False
            else:
                print(f"  OK: {router_name} correctly configured")
        else:
            if f'{router_name},' in content and f'prefix="/' in content[content.find(f'{router_name},'):content.find(f'{router_name},')+200]:
                print(f"  OK: {router_name} has expected prefix")
            else:
                print(f"  FAIL: {router_name} missing expected prefix")
                all_good = False
    
    return all_good

def verify_comment_2_commit_parentheses():
    """Verify Comment 2: All db.commit() calls have parentheses."""
    print("\n=== Comment 2: db.commit() Parentheses ===")
    
    strains_file = "app/fastapi_app/routers/strains.py"
    with open(strains_file, 'r') as f:
        content = f.read()
    
    # Find db.commit calls
    commit_pattern = r'await\s+db\.commit\(\)'
    bare_commit_pattern = r'await\s+db\.commit\s*(?!\()'
    
    commit_calls = len(re.findall(commit_pattern, content))
    bare_commits = len(re.findall(bare_commit_pattern, content))
    
    print(f"  Found {commit_calls} db.commit() calls with parentheses")
    print(f"  Found {bare_commits} db.commit calls without parentheses")
    
    if bare_commits == 0:
        print("  OK: All db.commit() calls have parentheses")
        return True
    else:
        print("  FAIL: Found db.commit() calls without parentheses")
        return False

def verify_comment_3_async_patterns():
    """Verify Comment 3: Auth router uses async patterns."""
    print("\n=== Comment 3: Auth Router Async Patterns ===")
    
    auth_file = "app/fastapi_app/routers/auth.py"
    with open(auth_file, 'r') as f:
        content = f.read()
    
    # Check for async patterns
    async_patterns = [
        'from sqlalchemy.ext.asyncio import AsyncSession',
        'from app.fastapi_app.database import get_async_db',
        'await db.execute(select(',
    ]
    
    sync_patterns = [
        'db.query(',
        'SessionLocal',
    ]
    
    all_good = True
    for pattern in async_patterns:
        if pattern in content:
            print(f"  OK: Found async pattern: {pattern}")
        else:
            print(f"  FAIL: Missing async pattern: {pattern}")
            all_good = False
    
    for pattern in sync_patterns:
        if pattern not in content:
            print(f"  OK: No sync pattern found: {pattern}")
        else:
            print(f"  FAIL: Found sync pattern: {pattern}")
            all_good = False
    
    return all_good

def check_integration_test():
    """Check if integration test was created."""
    print("\n=== Integration Test ===")
    
    test_file = "tests/test_router_fixes.py"
    if os.path.exists(test_file):
        print(f"  OK: Integration test created: {test_file}")
        return True
    else:
        print(f"  FAIL: Integration test not found: {test_file}")
        return False

def main():
    print("Router Fixes Verification")
    print("=" * 50)
    
    results = []
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    results.append(verify_comment_1_duplicate_prefixes())
    results.append(verify_comment_2_commit_parentheses())
    results.append(verify_comment_3_async_patterns())
    results.append(check_integration_test())
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    if all(results):
        print("SUCCESS: All router fixes are correctly implemented!")
        return 0
    else:
        print("FAILURE: Some issues remain")
        return 1

if __name__ == "__main__":
    exit(main())