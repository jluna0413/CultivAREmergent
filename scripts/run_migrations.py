#!/usr/bin/env python3
"""
Convenience script to run database migrations for CultivAR async models.
Supports both SQLite and PostgreSQL databases.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

def run_command(cmd):
    """Run a command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True

def main():
    parser = argparse.ArgumentParser(description="Run database migrations for CultivAR async models")
    parser.add_argument("--database-url", help="Database URL (overrides env var)")
    parser.add_argument("command", choices=["upgrade", "downgrade", "current", "history", "check", "create"],
                       help="Migration command to run")
    parser.add_argument("--revision", help="Revision for upgrade/downgrade commands")
    parser.add_argument("--message", help="Message for create command")
    args = parser.parse_args()

    # Set database URL if provided
    if args.database_url:
        os.environ["DATABASE_URL"] = args.database_url
        print(f"Using database URL: {args.database_url}")
    elif not os.getenv("DATABASE_URL"):
        print("Using default SQLite database: sqlite:///./cultivar.db")
        os.environ["DATABASE_URL"] = "sqlite:///./cultivar.db"

    # Base alembic command
    alembic_cmd = "alembic"

    if args.command == "upgrade":
        revision = args.revision or "head"
        cmd = f"{alembic_cmd} upgrade {revision}"
    elif args.command == "downgrade":
        if not args.revision:
            print("Error: --revision required for downgrade")
            return 1
        cmd = f"{alembic_cmd} downgrade {args.revision}"
    elif args.command == "current":
        cmd = f"{alembic_cmd} current"
    elif args.command == "history":
        cmd = f"{alembic_cmd} history"
    elif args.command == "check":
        cmd = f"{alembic_cmd} check"
    elif args.command == "create":
        if not args.message:
            print("Error: --message required for create")
            return 1
        cmd = f'{alembic_cmd} revision --autogenerate -m "{args.message}"'
    
    return 0 if run_command(cmd) else 1

if __name__ == "__main__":
    sys.exit(main())