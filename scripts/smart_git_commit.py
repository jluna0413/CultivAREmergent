#!/usr/bin/env python3
"""
Smart Git Commit Script with Guardrails
Automatically categorizes and commits changes with proper conventional commit messages.
"""

import subprocess
import os
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

# Configuration
DRY_RUN = False  # Execute commits
REPO_ROOT = Path(__file__).parent.parent

# Files/patterns that should NEVER be committed (add to .gitignore)
GITIGNORE_ADDITIONS = """
# ============================================
# AUTO-GENERATED: Smart Git Commit Guardrails
# ============================================

# Temporary debug/test output files
debug_*.py
read_*.py
copy_*.py
inspect_*.py
find_*.py
fix_*.py
scan_*.py
check_*.py
*_dump.txt
test_output*.txt
test_output*.md
startup_*.txt
startup_*.log
headers*.txt
refresh_test*.txt
inspection_results.txt
layout_debug_output.txt
test_failure_check.txt

# Temporary HTML files
temp_*.html
temp_*.txt
temp_*.css
tmp_*.html
tmp_*.txt
tmp_*.css
*_source.html

# One-off scripts (root level)
/add_*.py
/anonymous_*.py
/apply_*.py
/bypass_*.py
/clean_*.py
/collect_*.py
/create_*.py
/dashboard.py
/debug_*.py
/diagnose.py
/extract_*.py
/get_*.py
/hello.py
/init_*.py
/maestro.py
/no_login_app.py
/overwrite_*.py
/performance_*.py
/populate_*.py
/production_*.py
/quicksort_*.py
/remove_*.py
/repro_*.py
/run_*.py
/scaffold_*.py
/seed_*.py
/security_*.py
/setup_*.ps1
/simulate_*.py
/ssl_*.py
/template_*.py
/update_*.py
/ultimate_*.py
/validate_*.py
/verify_*.py

# JSON output files (transient)
report.json
final_report.json
login_test.json
swarm_output.json
cultivar_security_documentation.json
flutter_fix_report*.json
zaproxy_images.json

# Backup directories
*_backup/

# Coverage reports
htmlcov/

# ============================================
# AGENT CONFIGS - HYBRID APPROACH
# Commit: workflows, rules, methodology
# Ignore: chat histories, caches, personal data
# ============================================

# Aider - IGNORE (chat histories are personal)
.aider*
.aider-desk/

# Taskmaster - IGNORE (personal task tracking)
.taskmaster/

# Cache directories - IGNORE
*.cache*/
.aider.tags.cache*/

# Large binary files
toolbox

# Database files
*.db

# SSL certificates
ssl/

# Virtual environments
.venv/

# Activities tracking
activities.json

# Misc debugging artifacts
router_inspect.dart
main_inspect.dart
all_tests.txt
script_start_line.txt
team-fullstack.txt
"""

# Commit categories with file patterns
COMMIT_CATEGORIES = {
    "core_backend": {
        "message": "feat(backend): Add core FastAPI services and models",
        "patterns": [
            "app/services/",
            "app/repositories/",
            "app/models/",
            "app/schemas/",
            "app/handlers/",
            "app/handlers_async/",
            "app/models_async/",
            "app/config/",
        ],
        "priority": 1,
    },
    "routers_api": {
        "message": "feat(api): Add new API routers and endpoints",
        "patterns": [
            "app/fastapi_app/routers/",
            "app/routers/",
            "app/routes/",
        ],
        "priority": 2,
    },
    "security": {
        "message": "feat(security): Implement security configurations and middleware",
        "patterns": [
            "app/fastapi_app/security",
            "app/utils/security",
            "app/utils/input_validation",
            "keycloak",
        ],
        "priority": 3,
    },
    "gamification": {
        "message": "feat(gamification): Add gamification system",
        "patterns": [
            "app/gamification/",
        ],
        "priority": 4,
    },
    "mcp_agents": {
        "message": "feat(agents): Add MCP and agent infrastructure",
        "patterns": [
            "app/mcp/",
            "conductor/",
        ],
        "priority": 5,
    },
    "ml_ai": {
        "message": "feat(ml): Add machine learning and AI components",
        "patterns": [
            "app/ml/",
            "ml/",
        ],
        "priority": 6,
    },
    "flutter_app": {
        "message": "feat(flutter): Add Flutter mobile/web application",
        "patterns": [
            "flutter_app/",
        ],
        "priority": 7,
    },
    "jaspr_app": {
        "message": "feat(jaspr): Add Jaspr server-side Dart application",
        "patterns": [
            "jaspr_app/",
            "lib/",
        ],
        "priority": 8,
    },
    "templates_static": {
        "message": "feat(web): Add web templates and static assets",
        "patterns": [
            "app/templates/",
            "app/web/",
        ],
        "priority": 9,
    },
    "docker_infra": {
        "message": "chore(infra): Add Docker and infrastructure configurations",
        "patterns": [
            "docker-compose",
            "docker-entrypoint",
            "docker-env",
            "docker_proxy",
            "Dockerfile",
            ".dockerignore",
            "infrastructure/",
            "nginx.conf",
        ],
        "priority": 10,
    },
    "tests": {
        "message": "test: Add comprehensive test suite",
        "patterns": [
            "tests/",
            "test/",
            "pytest.ini",
        ],
        "priority": 11,
    },
    "scripts_utils": {
        "message": "chore(scripts): Add utility and maintenance scripts",
        "patterns": [
            "scripts/",
        ],
        "priority": 12,
    },
    "docs": {
        "message": "docs: Add documentation and planning files",
        "patterns": [
            "docs/",
            "plans/",
            "implementation_plans/",
            "reports/",
            "validation_reports/",
            "competitive-analysis",
            "document-project.md",
        ],
        "priority": 13,
    },
    "ops_cicd": {
        "message": "ci(ops): Add operations and CI/CD configurations",
        "patterns": [
            "ops/",
            "tasks/",
            ".github/",
        ],
        "priority": 14,
    },
    "blockchain": {
        "message": "feat(blockchain): Add blockchain integration (TEAL contracts)",
        "patterns": [
            "vault_approval.teal",
            "vault_clear.teal",
        ],
        "priority": 15,
    },
    "agent_configs": {
        "message": "chore(agents): Add AI agent configurations and workflows",
        "patterns": [
            ".agent/",
            ".bmad-core/",
            ".claude/",
            ".cursor/",
            ".gemini/",
            ".iflow/",
            ".kilocode/",
            ".maestro/",
            ".qwen/",
            ".roo/",
            ".trae/",
            ".clinerules/",
            ".kilocodemodes",
            ".roomodes",
            "opencode.jsonc",
        ],
        "priority": 16,
    },
    "modified_tracked": {
        "message": "refactor: Update existing codebase with improvements",
        "patterns": [],  # Will be populated with modified tracked files
        "priority": 0,  # Highest priority - commit first
    },
}


def run_git_command(args: List[str], capture_output=True) -> Tuple[int, str, str]:
    """Run a git command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        ["git"] + args,
        cwd=REPO_ROOT,
        capture_output=capture_output,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


def get_untracked_files() -> List[str]:
    """Get list of untracked files."""
    _, stdout, _ = run_git_command(["status", "--porcelain"])
    untracked = []
    for line in stdout.strip().split("\n"):
        if line.startswith("??"):
            untracked.append(line[3:].strip())
    return untracked


def get_modified_files() -> List[str]:
    """Get list of modified tracked files."""
    _, stdout, _ = run_git_command(["status", "--porcelain"])
    modified = []
    for line in stdout.strip().split("\n"):
        if line and not line.startswith("??"):
            # Extract filename (handle renamed files)
            parts = line.split()
            if len(parts) >= 2:
                modified.append(parts[-1])
    return modified


def categorize_file(filepath: str, categories: Dict) -> str:
    """Determine which category a file belongs to."""
    for cat_name, cat_info in sorted(categories.items(), key=lambda x: x[1]["priority"]):
        for pattern in cat_info["patterns"]:
            if pattern in filepath or filepath.startswith(pattern.rstrip("/")):
                return cat_name
    return None  # File doesn't match any category


def should_ignore(filepath: str) -> bool:
    """Check if a file should be added to .gitignore instead of committed."""
    ignore_patterns = [
        # Temp files
        "temp_", "tmp_", "_dump.txt", "_source.html",
        # Debug scripts at root
        "debug_", "read_", "copy_", "inspect_", "find_", "fix_", "scan_", "check_",
        # Output files
        "test_output", "startup_", "headers", "refresh_test",
        # Backups
        "_backup/",
        # Reports at root
        "report.json", "final_report.json", "login_test.json",
        # Large binaries
        "toolbox",
        # Coverage
        "htmlcov/",
    ]
    
    # Only apply to root-level files for scripts
    for pattern in ignore_patterns:
        if pattern in filepath:
            return True
    
    return False


def update_gitignore():
    """Update .gitignore with additional patterns."""
    gitignore_path = REPO_ROOT / ".gitignore"
    
    with open(gitignore_path, "r") as f:
        current_content = f.read()
    
    # Check if we've already added our section
    if "Smart Git Commit Guardrails" in current_content:
        print("ℹ️  .gitignore already has guardrails section")
        return False
    
    with open(gitignore_path, "a") as f:
        f.write(GITIGNORE_ADDITIONS)
    
    print("✅ Updated .gitignore with guardrails")
    return True


def main():
    print("=" * 60)
    print("🚀 Smart Git Commit Script with Guardrails")
    print("=" * 60)
    print(f"\n📁 Repository: {REPO_ROOT}")
    print(f"🧪 Dry Run: {DRY_RUN}\n")
    
    # Step 1: Update .gitignore
    print("\n📝 Step 1: Updating .gitignore...")
    gitignore_updated = update_gitignore()
    
    # Step 2: Get all changes
    print("\n📊 Step 2: Analyzing changes...")
    untracked = get_untracked_files()
    modified = get_modified_files()
    
    print(f"   - Untracked files: {len(untracked)}")
    print(f"   - Modified files: {len(modified)}")
    
    # Step 3: Categorize files
    print("\n🏷️  Step 3: Categorizing files...")
    categorized: Dict[str, List[str]] = defaultdict(list)
    ignored: List[str] = []
    uncategorized: List[str] = []
    
    # Add modified files to their own category
    for filepath in modified:
        categorized["modified_tracked"].append(filepath)
    
    # Categorize untracked files
    for filepath in untracked:
        if should_ignore(filepath):
            ignored.append(filepath)
        else:
            category = categorize_file(filepath, COMMIT_CATEGORIES)
            if category:
                categorized[category].append(filepath)
            else:
                uncategorized.append(filepath)
    
    print(f"   - Files to ignore: {len(ignored)}")
    print(f"   - Files to commit: {sum(len(v) for v in categorized.values())}")
    print(f"   - Uncategorized: {len(uncategorized)}")
    
    # Step 4: Print commit plan
    print("\n" + "=" * 60)
    print("📋 COMMIT PLAN")
    print("=" * 60)
    
    # Sort by priority
    sorted_categories = sorted(
        [(k, v) for k, v in categorized.items() if v],
        key=lambda x: COMMIT_CATEGORIES[x[0]]["priority"]
    )
    
    for category, files in sorted_categories:
        cat_info = COMMIT_CATEGORIES[category]
        print(f"\n🔹 Commit {cat_info['priority']}: {cat_info['message']}")
        print(f"   Files ({len(files)}):")
        for f in files[:10]:  # Show first 10
            print(f"      - {f}")
        if len(files) > 10:
            print(f"      ... and {len(files) - 10} more files")
    
    if uncategorized:
        print(f"\n⚠️  Uncategorized files ({len(uncategorized)}):")
        for f in uncategorized[:10]:
            print(f"   - {f}")
        if len(uncategorized) > 10:
            print(f"   ... and {len(uncategorized) - 10} more")
    
    if ignored:
        print(f"\n🚫 Files to be ignored ({len(ignored)}):")
        for f in ignored[:10]:
            print(f"   - {f}")
        if len(ignored) > 10:
            print(f"   ... and {len(ignored) - 10} more")
    
    print("\n" + "=" * 60)
    
    if DRY_RUN:
        print("\n🧪 DRY RUN MODE - No changes made")
        print("   Set DRY_RUN = False in the script to execute commits")
        return
    
    # Step 5: Execute commits
    print("\n🚀 Step 5: Executing commits...")
    
    # First, commit .gitignore update if needed
    if gitignore_updated:
        run_git_command(["add", ".gitignore"])
        run_git_command(["commit", "-m", "chore: Update .gitignore with guardrails for temp/debug files"])
        print("   ✅ Committed .gitignore update")
    
    # Execute each category commit
    for category, files in sorted_categories:
        cat_info = COMMIT_CATEGORIES[category]
        
        # Stage files
        for f in files:
            run_git_command(["add", f])
        
        # Commit
        returncode, stdout, stderr = run_git_command(
            ["commit", "-m", cat_info["message"]]
        )
        
        if returncode == 0:
            print(f"   ✅ {cat_info['message']} ({len(files)} files)")
        else:
            print(f"   ❌ Failed: {cat_info['message']}")
            print(f"      Error: {stderr}")
    
    print("\n✨ Done! All commits created successfully.")


if __name__ == "__main__":
    main()
