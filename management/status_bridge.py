#!/usr/bin/env python3
"""
TSTR.site Status Bridge - Unified Status Management API

Central integration layer for all status operations:
- PROJECT_STATUS.md updates
- .ai-session.md logging
- Database synchronization
- Event-driven status management

Usage:
    from management.status_bridge import StatusBridge

    bridge = StatusBridge()
    bridge.update_status_header("AgentName")
    bridge.log_session("AgentName", "Action taken", "Result achieved")
"""

import sys
import datetime
import re
import json
import subprocess
from typing import Optional, Dict, Any
from pathlib import Path


class StatusBridge:
    """Unified API for all status management operations"""

    def __init__(self, project_root: Optional[str] = None):
        """Initialize with project paths"""
        if project_root is None:
            # Auto-detect project root
            project_root = Path(__file__).parent.parent

        self.project_root = Path(project_root)
        self.status_file = self.project_root / "PROJECT_STATUS.md"
        self.session_file = self.project_root / ".ai-session.md"
        self.db_utils = (
            self.project_root.parent.parent / "SYSTEM" / "state" / "db_utils.py"
        )

        # Validate paths exist
        if not self.status_file.exists():
            raise FileNotFoundError(
                f"PROJECT_STATUS.md not found at {self.status_file}"
            )
        if not self.session_file.exists():
            # Create session file if it doesn't exist
            self._initialize_session_file()

    def _initialize_session_file(self):
        """Create initial .ai-session.md structure"""
        initial_content = """# AI Session Log - TSTR.site

## Current Session

## Session History

"""
        self.session_file.write_text(initial_content)

    def get_timestamp(self) -> str:
        """Get current UTC timestamp in standard format"""
        return datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%d %H:%M UTC"
        )

    def update_status_header(self, agent_name: str) -> bool:
        """
        Update PROJECT_STATUS.md header with timestamp and agent

        Args:
            agent_name: Name of the agent making the update

        Returns:
            bool: Success status
        """
        try:
            content = self.status_file.read_text()

            # Update timestamp
            content = re.sub(
                r"\*\*Last Updated\*\*:.*",
                f"**Last Updated**: {self.get_timestamp()}",
                content,
            )

            # Update agent
            content = re.sub(
                r"\*\*Updated By\*\*:.*", f"**Updated By**: {agent_name}", content
            )

            self.status_file.write_text(content)
            print(f"✅ Updated PROJECT_STATUS.md header - Agent: {agent_name}")
            return True

        except Exception as e:
            print(f"❌ Failed to update status header: {e}")
            return False

    def log_session(self, agent_name: str, action: str, result: str) -> bool:
        """
        Log session entry to .ai-session.md

        Args:
            agent_name: Name of the agent
            action: Action taken
            result: Result achieved

        Returns:
            bool: Success status
        """
        try:
            content = self.session_file.read_text()

            # Create log entry
            entry = f"""
### {self.get_timestamp()} - {agent_name}
- **Action**: {action}
- **Result**: {result}
"""

            # Insert into Session History section
            history_marker = "## Session History"
            if history_marker in content:
                # Insert after the marker
                parts = content.split(history_marker, 1)
                content = parts[0] + history_marker + entry + parts[1]
            else:
                # Append to end if no history section
                content += f"\n{history_marker}{entry}"

            self.session_file.write_text(content)
            print("✅ Logged session entry to .ai-session.md")
            return True

        except Exception as e:
            print(f"❌ Failed to log session: {e}")
            return False

    def add_database_learning(self, learning: str) -> bool:
        """
        Add learning to the database system

        Args:
            learning: Learning content to store

        Returns:
            bool: Success status
        """
        try:
            if not self.db_utils.exists():
                print("⚠️ Database utils not found, skipping learning addition")
                return False

            # Run database learning command
            cmd = [sys.executable, str(self.db_utils), "--learn", learning]
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=self.project_root
            )

            if result.returncode == 0:
                print("✅ Added learning to database")
                return True
            else:
                print(f"❌ Failed to add database learning: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ Database learning error: {e}")
            return False

    def sync_status(
        self, agent_name: str, action: str, result: str, add_learning: bool = True
    ) -> Dict[str, bool]:
        """
        Comprehensive status synchronization - update all systems

        Args:
            agent_name: Name of the agent
            action: Action taken
            result: Result achieved
            add_learning: Whether to add database learning

        Returns:
            Dict with success status for each operation
        """
        results = {}

        # Update status header
        results["status_header"] = self.update_status_header(agent_name)

        # Log session
        results["session_log"] = self.log_session(agent_name, action, result)

        # Add database learning if requested
        if add_learning:
            learning = f"Status update: {action} - {result}"
            results["database_learning"] = self.add_database_learning(learning)
        else:
            results["database_learning"] = None

        # Summary
        successful = sum(1 for v in results.values() if v is True)
        total = sum(1 for v in results.values() if v is not None)

        if successful == total:
            print(
                f"✅ Status sync complete - {successful}/{total} operations successful"
            )
        else:
            print(f"⚠️ Status sync partial - {successful}/{total} operations successful")

        return results

    def validate_consistency(self) -> Dict[str, Any]:
        """
        Validate consistency between different status tracking systems

        Returns:
            Dict with validation results
        """
        results = {
            "status_file_exists": self.status_file.exists(),
            "session_file_exists": self.session_file.exists(),
            "database_accessible": self.db_utils.exists(),
            "issues": [],
        }

        # Check for common issues
        if not results["status_file_exists"]:
            results["issues"].append("PROJECT_STATUS.md not found")

        if not results["session_file_exists"]:
            results["issues"].append(".ai-session.md not found")

        if not results["database_accessible"]:
            results["issues"].append("Database utils not accessible")

        # Check file readability
        try:
            if results["status_file_exists"]:
                self.status_file.read_text()
                results["status_file_readable"] = True
            else:
                results["status_file_readable"] = False
        except:
            results["status_file_readable"] = False
            results["issues"].append("PROJECT_STATUS.md not readable")

        try:
            if results["session_file_exists"]:
                self.session_file.read_text()
                results["session_file_readable"] = True
            else:
                results["session_file_readable"] = False
        except:
            results["session_file_readable"] = False
            results["issues"].append(".ai-session.md not readable")

        results["overall_healthy"] = len(results["issues"]) == 0

        return results


def main():
    """CLI interface for direct usage"""
    import argparse

    parser = argparse.ArgumentParser(description="TSTR.site Status Bridge")
    subparsers = parser.add_subparsers(dest="command")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update status header")
    update_parser.add_argument("--agent", required=True, help="Agent name")

    # Log command
    log_parser = subparsers.add_parser("log", help="Log session entry")
    log_parser.add_argument("--agent", required=True, help="Agent name")
    log_parser.add_argument("--action", required=True, help="Action taken")
    log_parser.add_argument("--result", required=True, help="Result achieved")

    # Sync command
    sync_parser = subparsers.add_parser("sync", help="Full status synchronization")
    sync_parser.add_argument("--agent", required=True, help="Agent name")
    sync_parser.add_argument("--action", required=True, help="Action taken")
    sync_parser.add_argument("--result", required=True, help="Result achieved")
    sync_parser.add_argument(
        "--no-learning", action="store_true", help="Skip database learning"
    )

    # Validate command
    validate_parser = subparsers.add_parser(
        "validate", help="Validate system consistency"
    )
    validate_parser.add_argument("--agent", help="Optional agent name for context")

    args = parser.parse_args()

    try:
        bridge = StatusBridge()

        if args.command == "update":
            success = bridge.update_status_header(args.agent)
            sys.exit(0 if success else 1)

        elif args.command == "log":
            success = bridge.log_session(args.agent, args.action, args.result)
            sys.exit(0 if success else 1)

        elif args.command == "sync":
            results = bridge.sync_status(
                args.agent, args.action, args.result, add_learning=not args.no_learning
            )
            successful = sum(1 for v in results.values() if v is True)
            total = sum(1 for v in results.values() if v is not None)
            sys.exit(0 if successful == total else 1)

        elif args.command == "validate":
            results = bridge.validate_consistency()
            print(json.dumps(results, indent=2))
            sys.exit(0 if results["overall_healthy"] else 1)

        else:
            parser.print_help()
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
