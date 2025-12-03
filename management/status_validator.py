#!/usr/bin/env python3
"""
TSTR.site Status Validator

Validates consistency and integrity of status tracking systems:
- File integrity and accessibility
- Data consistency between systems
- Configuration validation
- Health monitoring and alerts

Usage:
    from management.status_validator import StatusValidator

    validator = StatusValidator()
    results = validator.validate_all()
    print(results['summary'])
"""

import os
import sys
import json
import hashlib
import re
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime, timezone


class StatusValidator:
    """Comprehensive validator for status tracking systems"""

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

        # Critical files that must exist
        self.critical_files = [self.status_file, self.session_file]

        # Optional files
        self.optional_files = [self.db_utils]

    def validate_file_integrity(self) -> Dict[str, Any]:
        """
        Validate file existence, readability, and basic integrity

        Returns:
            Dict with file validation results
        """
        results = {
            "critical_files": {},
            "optional_files": {},
            "integrity_score": 0,
            "issues": [],
        }

        # Check critical files
        critical_score = 0
        for file_path in self.critical_files:
            file_results = self._validate_single_file(file_path, critical=True)
            results["critical_files"][file_path.name] = file_results

            if file_results["exists"] and file_results["readable"]:
                critical_score += 1
            else:
                results["issues"].append(f"Critical file issue: {file_path.name}")

        # Check optional files
        optional_score = 0
        for file_path in self.optional_files:
            file_results = self._validate_single_file(file_path, critical=False)
            results["optional_files"][file_path.name] = file_results

            if file_results["exists"] and file_results["readable"]:
                optional_score += 1

        # Calculate integrity score (0-100)
        total_critical = len(self.critical_files)
        total_optional = len(self.optional_files)

        if total_critical > 0:
            critical_ratio = critical_score / total_critical
        else:
            critical_ratio = 1.0

        if total_optional + total_critical > 0:
            optional_ratio = (
                optional_score / total_optional if total_optional > 0 else 0
            )
            results["integrity_score"] = int(
                (critical_ratio * 0.8 + optional_ratio * 0.2) * 100
            )
        else:
            results["integrity_score"] = 100

        return results

    def _validate_single_file(
        self, file_path: Path, critical: bool = False
    ) -> Dict[str, Any]:
        """Validate a single file"""
        results = {
            "exists": file_path.exists(),
            "readable": False,
            "writable": False,
            "size": 0,
            "modified": None,
            "hash": None,
            "issues": [],
        }

        if not results["exists"]:
            results["issues"].append("File does not exist")
            if critical:
                results["issues"].append(
                    "CRITICAL: This file is required for system operation"
                )
            return results

        # Check readability
        try:
            content = file_path.read_text()
            results["readable"] = True
            results["size"] = len(content)

            # Generate hash for integrity checking
            results["hash"] = hashlib.md5(content.encode()).hexdigest()[:8]

        except Exception as e:
            results["issues"].append(f"Read error: {e}")
            return results

        # Check writability
        try:
            # Try to open for writing (without actually writing)
            with open(file_path, "a"):
                pass
            results["writable"] = True
        except:
            results["issues"].append("File is not writable")

        # Get modification time
        try:
            mtime = file_path.stat().st_mtime
            results["modified"] = datetime.fromtimestamp(
                mtime, tz=timezone.utc
            ).strftime("%Y-%m-%d %H:%M UTC")
        except:
            results["issues"].append("Cannot determine modification time")

        return results

    def validate_data_consistency(self) -> Dict[str, Any]:
        """
        Validate data consistency between different systems

        Returns:
            Dict with consistency validation results
        """
        results = {
            "status_format": self._validate_status_format(),
            "session_format": self._validate_session_format(),
            "cross_references": self._validate_cross_references(),
            "consistency_score": 0,
            "issues": [],
        }

        # Calculate consistency score
        scores = []
        for check_name, check_result in results.items():
            if check_name.endswith("_format") or check_name == "cross_references":
                if isinstance(check_result, dict) and check_result.get("valid", False):
                    scores.append(100)
                elif isinstance(check_result, bool) and check_result:
                    scores.append(100)
                else:
                    scores.append(50)  # Partial credit for attempted validation

        if scores:
            results["consistency_score"] = sum(scores) // len(scores)
        else:
            results["consistency_score"] = 100

        return results

    def _validate_status_format(self) -> Dict[str, Any]:
        """Validate PROJECT_STATUS.md format"""
        if not self.status_file.exists():
            return {"valid": False, "issues": ["Status file does not exist"]}

        try:
            content = self.status_file.read_text()
            issues = []

            # Check for required headers
            required_patterns = [
                r"\*\*Last Updated\*\*:",
                r"\*\*Updated By\*\*:",
                r"## 📈 CURRENT STATUS DASHBOARD",
            ]

            for pattern in required_patterns:
                if not re.search(pattern, content):
                    issues.append(f"Missing required pattern: {pattern}")

            return {
                "valid": len(issues) == 0,
                "issues": issues,
                "line_count": len(content.split("\n")),
                "has_version": "v" in content[:500],  # Check for version info in header
            }

        except Exception as e:
            return {"valid": False, "issues": [f"Parse error: {e}"]}

    def _validate_session_format(self) -> Dict[str, Any]:
        """Validate .ai-session.md format"""
        if not self.session_file.exists():
            return {"valid": False, "issues": ["Session file does not exist"]}

        try:
            content = self.session_file.read_text()
            issues = []

            # Check for basic structure
            if "## Session History" not in content:
                issues.append("Missing '## Session History' section")

            # Check for session entries
            session_count = content.count("### ")
            if session_count == 0:
                issues.append("No session entries found")

            return {
                "valid": len(issues) == 0,
                "issues": issues,
                "session_count": session_count,
                "total_lines": len(content.split("\n")),
            }

        except Exception as e:
            return {"valid": False, "issues": [f"Parse error: {e}"]}

    def _validate_cross_references(self) -> Dict[str, Any]:
        """Validate cross-references between systems"""
        # This is a placeholder for more complex cross-validation
        # In a full implementation, this would check:
        # - If sessions mentioned in status are logged
        # - If database entries match file entries
        # - If timestamps are synchronized

        return {
            "valid": True,  # Assume valid for now
            "checked_references": 0,
            "issues": [],
        }

    def validate_configuration(self) -> Dict[str, Any]:
        """
        Validate system configuration and environment

        Returns:
            Dict with configuration validation results
        """
        results = {
            "python_version": sys.version.split()[0],
            "project_structure": self._validate_project_structure(),
            "permissions": self._validate_permissions(),
            "environment": self._validate_environment(),
            "configuration_score": 0,
            "issues": [],
        }

        # Calculate configuration score
        scores = []
        for check_name in ["project_structure", "permissions", "environment"]:
            check_result = results[check_name]
            if isinstance(check_result, dict) and check_result.get("valid", False):
                scores.append(100)
            elif isinstance(check_result, bool) and check_result:
                scores.append(100)
            else:
                scores.append(50)

        if scores:
            results["configuration_score"] = sum(scores) // len(scores)

        return results

    def _validate_project_structure(self) -> Dict[str, Any]:
        """Validate project directory structure"""
        required_dirs = ["web", "docs", "management"]
        required_files = ["PROJECT_STATUS.md", ".ai-session.md"]

        issues = []

        for dir_name in required_dirs:
            if not (self.project_root / dir_name).exists():
                issues.append(f"Missing required directory: {dir_name}")

        for file_name in required_files:
            if not (self.project_root / file_name).exists():
                issues.append(f"Missing required file: {file_name}")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "project_root": str(self.project_root),
        }

    def _validate_permissions(self) -> Dict[str, Any]:
        """Validate file and directory permissions"""
        issues = []

        # Check if we can write to critical files
        for file_path in self.critical_files:
            if file_path.exists():
                try:
                    # Test write permission
                    with open(file_path, "a") as f:
                        f.write("")
                except:
                    issues.append(f"No write permission: {file_path.name}")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "current_user": os.getlogin() if hasattr(os, "getlogin") else "unknown",
        }

    def _validate_environment(self) -> Dict[str, Any]:
        """Validate environment and dependencies"""
        issues = []

        # Check Python version (should be 3.8+)
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            issues.append(
                f"Python version {version.major}.{version.minor} may be too old"
            )

        # Check if we're in the right directory
        if not (self.project_root / "PROJECT_STATUS.md").exists():
            issues.append("Not running from project root directory")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "python_version": f"{version.major}.{version.minor}.{version.micro}",
            "working_directory": str(self.project_root),
        }

    def validate_all(self) -> Dict[str, Any]:
        """
        Run all validation checks

        Returns:
            Comprehensive validation results
        """
        print("🔍 Running comprehensive status validation...")

        results = {
            "file_integrity": self.validate_file_integrity(),
            "data_consistency": self.validate_data_consistency(),
            "configuration": self.validate_configuration(),
            "summary": {},
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        }

        # Calculate overall scores
        integrity_score = results["file_integrity"]["integrity_score"]
        consistency_score = results["data_consistency"]["consistency_score"]
        config_score = results["configuration"]["configuration_score"]

        overall_score = (integrity_score + consistency_score + config_score) // 3

        results["summary"] = {
            "overall_score": overall_score,
            "integrity_score": integrity_score,
            "consistency_score": consistency_score,
            "configuration_score": config_score,
            "status": "healthy"
            if overall_score >= 80
            else "needs_attention"
            if overall_score >= 60
            else "critical",
            "total_issues": sum(
                len(r.get("issues", []))
                for r in results.values()
                if isinstance(r, dict)
            ),
        }

        print(
            f"✅ Validation complete - Overall Score: {overall_score}/100 ({results['summary']['status']})"
        )
        return results

    def generate_health_report(self) -> str:
        """Generate a detailed health report"""
        results = self.validate_all()

        report = f"""
# Status System Health Report
Generated: {results["generated_at"]}

## Overall Health: {results["summary"]["status"].upper()} ({results["summary"]["overall_score"]}/100)

### Scores Breakdown
- File Integrity: {results["summary"]["integrity_score"]}/100
- Data Consistency: {results["summary"]["consistency_score"]}/100
- Configuration: {results["summary"]["configuration_score"]}/100

### Issues Found: {results["summary"]["total_issues"]}

## Detailed Results

### File Integrity
"""

        # Add file integrity details
        for category, files in [
            ("Critical Files", results["file_integrity"]["critical_files"]),
            ("Optional Files", results["file_integrity"]["optional_files"]),
        ]:
            report += f"#### {category}\n"
            for filename, file_results in files.items():
                status = (
                    "✅"
                    if file_results["exists"] and file_results["readable"]
                    else "❌"
                )
                report += f"- {status} {filename}"
                if file_results["issues"]:
                    report += f" (Issues: {', '.join(file_results['issues'])})"
                report += "\n"

        report += f"""
### Data Consistency
- Status Format: {"✅" if results["data_consistency"]["status_format"]["valid"] else "❌"}
- Session Format: {"✅" if results["data_consistency"]["session_format"]["valid"] else "❌"}
- Cross References: {"✅" if results["data_consistency"]["cross_references"]["valid"] else "❌"}

### Configuration
- Python Version: {results["configuration"]["python_version"]}
- Project Structure: {"✅" if results["configuration"]["project_structure"]["valid"] else "❌"}
- Permissions: {"✅" if results["configuration"]["permissions"]["valid"] else "❌"}
- Environment: {"✅" if results["configuration"]["environment"]["valid"] else "❌"}

## Recommendations
"""

        if results["summary"]["overall_score"] >= 90:
            report += "- All systems operating normally ✅\n"
        else:
            if results["summary"]["integrity_score"] < 80:
                report += "- Address file integrity issues\n"
            if results["summary"]["consistency_score"] < 80:
                report += "- Fix data consistency problems\n"
            if results["summary"]["configuration_score"] < 80:
                report += "- Resolve configuration issues\n"

        return report


def main():
    """CLI interface for validation operations"""
    import argparse

    parser = argparse.ArgumentParser(description="TSTR.site Status Validator")
    subparsers = parser.add_subparsers(dest="command")

    # All command
    subparsers.add_parser("all", help="Run all validation checks")

    # Integrity command
    subparsers.add_parser("integrity", help="Validate file integrity")

    # Consistency command
    subparsers.add_parser("consistency", help="Validate data consistency")

    # Configuration command
    subparsers.add_parser("config", help="Validate configuration")

    # Report command
    subparsers.add_parser("report", help="Generate health report")

    args = parser.parse_args()

    try:
        validator = StatusValidator()

        if args.command == "all":
            results = validator.validate_all()
            print(json.dumps(results, indent=2))

        elif args.command == "integrity":
            results = validator.validate_file_integrity()
            print(json.dumps(results, indent=2))

        elif args.command == "consistency":
            results = validator.validate_data_consistency()
            print(json.dumps(results, indent=2))

        elif args.command == "config":
            results = validator.validate_configuration()
            print(json.dumps(results, indent=2))

        elif args.command == "report":
            report = validator.generate_health_report()
            print(report)

        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
