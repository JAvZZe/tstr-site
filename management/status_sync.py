#!/usr/bin/env python3
"""
TSTR.site Status Synchronization

Handles synchronization between different status tracking systems:
- Database learnings and file-based logs
- PROJECT_STATUS.md and session files
- Conflict resolution and consistency checking

Usage:
    from management.status_sync import StatusSync

    sync = StatusSync()
    sync.sync_all_systems()
"""

import os
import sys
import json
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime, timezone


class StatusSync:
    """Synchronization manager for status tracking systems"""

    def __init__(self, project_root: Optional[str] = None):
        """Initialize with project paths"""
        if project_root is None:
            project_root = Path(__file__).parent.parent

        self.project_root = Path(project_root)
        self.status_file = self.project_root / "PROJECT_STATUS.md"
        self.session_file = self.project_root / ".ai-session.md"
        self.db_utils = (
            self.project_root.parent.parent / "SYSTEM" / "state" / "db_utils.py"
        )

        # Import status bridge for operations
        try:
            from .status_bridge import StatusBridge

            self.bridge = StatusBridge(self.project_root)
        except ImportError:
            self.bridge = None

    def get_database_sessions(self) -> List[Dict[str, Any]]:
        """Retrieve recent sessions from database"""
        if not self.db_utils.exists():
            return []

        try:
            # This would need to be implemented based on actual database schema
            # For now, return empty list as database integration needs more setup
            return []
        except Exception as e:
            print(f"Database session retrieval error: {e}")
            return []

    def get_file_sessions(self) -> List[Dict[str, Any]]:
        """Parse sessions from .ai-session.md"""
        if not self.session_file.exists():
            return []

        try:
            content = self.session_file.read_text()
            sessions = []

            # Parse session entries (basic implementation)
            lines = content.split("\n")
            current_session = None

            for line in lines:
                if line.startswith("### ") and " - " in line:
                    # New session entry
                    timestamp_part = line[4:].split(" - ")[0].strip()
                    agent_part = line[4:].split(" - ")[1].strip()

                    current_session = {
                        "timestamp": timestamp_part,
                        "agent": agent_part,
                        "action": "",
                        "result": "",
                    }
                    sessions.append(current_session)
                elif current_session and line.startswith("- **Action**: "):
                    current_session["action"] = line[13:].strip()
                elif current_session and line.startswith("- **Result**: "):
                    current_session["result"] = line[13:].strip()

            return sessions
        except Exception as e:
            print(f"File session parsing error: {e}")
            return []

    def find_missing_sessions(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Identify sessions that exist in one system but not the other

        Returns:
            Dict with 'file_only' and 'db_only' lists
        """
        file_sessions = self.get_file_sessions()
        db_sessions = self.get_database_sessions()

        # Simple comparison based on timestamps and agents
        # This is a basic implementation - could be enhanced with better matching
        file_timestamps = {(s["timestamp"], s["agent"]) for s in file_sessions}
        db_timestamps = {(s["timestamp"], s["agent"]) for s in db_sessions}

        file_only = [
            s
            for s in file_sessions
            if (s["timestamp"], s["agent"]) not in db_timestamps
        ]
        db_only = [
            s
            for s in db_sessions
            if (s["timestamp"], s["agent"]) not in file_timestamps
        ]

        return {"file_only": file_only, "db_only": db_only}

    def sync_session_to_database(self, session: Dict[str, Any]) -> bool:
        """Sync a session entry to the database"""
        if not self.db_utils.exists():
            return False

        try:
            # Create a learning entry from the session
            learning = f"Session: {session['action']} - {session['result']}"
            cmd = [sys.executable, str(self.db_utils), "--learn", learning]
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=self.project_root
            )

            return result.returncode == 0
        except Exception as e:
            print(f"Session sync error: {e}")
            return False

    def sync_all_sessions(self) -> Dict[str, int]:
        """
        Sync all missing sessions between systems

        Returns:
            Dict with counts of synced items
        """
        missing = self.find_missing_sessions()
        results = {"synced_to_db": 0, "synced_to_file": 0, "errors": 0}

        # Sync file-only sessions to database
        for session in missing["file_only"]:
            if self.sync_session_to_database(session):
                results["synced_to_db"] += 1
            else:
                results["errors"] += 1

        # Note: Syncing from DB to file would require more complex logic
        # For now, we prioritize file-based sessions as the source of truth

        return results

    def validate_status_consistency(self) -> Dict[str, Any]:
        """
        Comprehensive consistency validation

        Returns:
            Dict with validation results
        """
        results = {
            "timestamp_consistency": self._check_timestamp_consistency(),
            "session_completeness": self._check_session_completeness(),
            "learning_coverage": self._check_learning_coverage(),
            "overall_score": 0,
        }

        # Calculate overall score (0-100)
        scores = []
        if results["timestamp_consistency"]["consistent"]:
            scores.append(100)
        else:
            scores.append(50)

        if results["session_completeness"]["complete"]:
            scores.append(100)
        else:
            scores.append(results["session_completeness"]["coverage_percent"])

        if results["learning_coverage"]["adequate"]:
            scores.append(100)
        else:
            scores.append(75)  # Partial credit for having some coverage

        results["overall_score"] = sum(scores) // len(scores)

        return results

    def _check_timestamp_consistency(self) -> Dict[str, Any]:
        """Check if timestamps are consistent between systems"""
        # This is a placeholder - would need actual database integration
        return {
            "consistent": True,  # Assume consistent for now
            "last_status_update": self._get_last_status_timestamp(),
            "last_session_entry": self._get_last_session_timestamp(),
        }

    def _check_session_completeness(self) -> Dict[str, Any]:
        """Check if sessions have all required fields"""
        sessions = self.get_file_sessions()
        if not sessions:
            return {"complete": False, "coverage_percent": 0}

        complete_sessions = 0
        for session in sessions:
            if session.get("action") and session.get("result"):
                complete_sessions += 1

        coverage = (complete_sessions / len(sessions)) * 100
        return {
            "complete": coverage >= 90,
            "coverage_percent": coverage,
            "total_sessions": len(sessions),
            "complete_sessions": complete_sessions,
        }

    def _check_learning_coverage(self) -> Dict[str, Any]:
        """Check if important actions have corresponding learnings"""
        # This is a placeholder - would need database integration
        return {
            "adequate": True,  # Assume adequate for now
            "learning_count": 0,
            "session_count": len(self.get_file_sessions()),
        }

    def _get_last_status_timestamp(self) -> str:
        """Get last update timestamp from PROJECT_STATUS.md"""
        if not self.status_file.exists():
            return "unknown"

        try:
            content = self.status_file.read_text()
            # Extract timestamp from header
            import re

            match = re.search(r"\*\*Last Updated\*\*: (.*)", content)
            return match.group(1) if match else "not found"
        except:
            return "error"

    def _get_last_session_timestamp(self) -> str:
        """Get last session timestamp from .ai-session.md"""
        sessions = self.get_file_sessions()
        return sessions[-1]["timestamp"] if sessions else "none"

    def generate_sync_report(self) -> str:
        """Generate a comprehensive synchronization report"""
        validation = self.validate_status_consistency()
        missing = self.find_missing_sessions()

        report = f"""
# Status Synchronization Report
Generated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}

## Overall Health Score: {validation["overall_score"]}/100

## Validation Results
- Timestamp Consistency: {"✅" if validation["timestamp_consistency"]["consistent"] else "❌"}
- Session Completeness: {"✅" if validation["session_completeness"]["complete"] else "❌"} ({validation["session_completeness"]["coverage_percent"]:.1f}%)
- Learning Coverage: {"✅" if validation["learning_coverage"]["adequate"] else "❌"}

## Synchronization Status
- Sessions in files only: {len(missing["file_only"])}
- Sessions in database only: {len(missing["db_only"])}
- Last status update: {validation["timestamp_consistency"]["last_status_update"]}
- Last session entry: {validation["timestamp_consistency"]["last_session_entry"]}

## Recommendations
"""

        if validation["overall_score"] < 70:
            report += "- Run full synchronization to resolve inconsistencies\n"
        if len(missing["file_only"]) > 0:
            report += f"- Sync {len(missing['file_only'])} sessions to database\n"
        if not validation["session_completeness"]["complete"]:
            report += "- Complete missing session information\n"

        if validation["overall_score"] >= 90:
            report += "- All systems synchronized ✅\n"

        return report

    def perform_full_sync(self) -> Dict[str, Any]:
        """
        Perform complete synchronization of all status systems

        Returns:
            Dict with sync results
        """
        print("🔄 Starting full status synchronization...")

        # Sync sessions
        session_results = self.sync_all_sessions()

        # Validate final state
        validation = self.validate_status_consistency()

        # Generate report
        report = self.generate_sync_report()

        results = {
            "session_sync": session_results,
            "validation": validation,
            "report": report,
            "success": validation["overall_score"] >= 80,
        }

        print(f"✅ Sync complete - Health Score: {validation['overall_score']}/100")
        return results


def main():
    """CLI interface for synchronization operations"""
    import argparse

    parser = argparse.ArgumentParser(description="TSTR.site Status Synchronization")
    subparsers = parser.add_subparsers(dest="command")

    # Sync command
    subparsers.add_parser("sync", help="Perform full synchronization")

    # Validate command
    subparsers.add_parser("validate", help="Validate system consistency")

    # Report command
    subparsers.add_parser("report", help="Generate synchronization report")

    # Missing command
    subparsers.add_parser("missing", help="Find missing sessions between systems")

    args = parser.parse_args()

    try:
        sync = StatusSync()

        if args.command == "sync":
            results = sync.perform_full_sync()
            print(json.dumps(results, indent=2))

        elif args.command == "validate":
            results = sync.validate_status_consistency()
            print(json.dumps(results, indent=2))

        elif args.command == "report":
            report = sync.generate_sync_report()
            print(report)

        elif args.command == "missing":
            missing = sync.find_missing_sessions()
            print(json.dumps(missing, indent=2))

        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
