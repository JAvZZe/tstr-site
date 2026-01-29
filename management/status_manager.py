#!/usr/bin/env python3
import os
import datetime
import re
import argparse

# Configuration
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATUS_FILE = os.path.join(PROJECT_ROOT, "PROJECT_STATUS.md")
SESSION_FILE = os.path.join(PROJECT_ROOT, ".ai-session.md")

def get_timestamp():
    return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

def update_status_header(agent_name):
    """Updates the Last Updated and Updated By fields in PROJECT_STATUS.md"""
    if not os.path.exists(STATUS_FILE):
        print(f"Error: {STATUS_FILE} not found.")
        return False

    with open(STATUS_FILE, 'r') as f:
        content = f.read()

    # Update Timestamp
    content = re.sub(
        r"\*\*Last Updated\*\*:.*",
        f"**Last Updated**: {get_timestamp()}",
        content
    )
    
    # Update Agent
    content = re.sub(
        r"\*\*Updated By\*\*:.*",
        f"**Updated By**: {agent_name}",
        content
    )

    with open(STATUS_FILE, 'w') as f:
        f.write(content)
    
    print("✅ Updated header in PROJECT_STATUS.md")
    return True

def log_session(agent_name, action, result):
    """Appends a log entry to .ai-session.md"""
    if not os.path.exists(SESSION_FILE):
        print(f"Error: {SESSION_FILE} not found.")
        return False

    entry = f"""
### {get_timestamp()} - {agent_name}
- **Action**: {action}
- **Result**: {result}
"""
    
    # Append to the end of the file, before the "Next Session Checklist" if it exists, 
    # or just at the end of the "Session History" section.
    # For simplicity in this v1, we'll append to the end of the "Current Session" or "Session History".
    
    # Better approach: Read file, find "## Session History", insert after.
    with open(SESSION_FILE, 'r') as f:
        lines = f.readlines()
    
    insert_idx = -1
    for i, line in enumerate(lines):
        if "## Session History" in line:
            insert_idx = i + 2 # Skip header and blank line
            break
    
    if insert_idx != -1:
        lines.insert(insert_idx, entry)
    else:
        lines.append(f"\n## Session History\n{entry}")

    with open(SESSION_FILE, 'w') as f:
        f.writelines(lines)

    print("✅ Logged session entry to .ai-session.md")
    return True

def main():
    parser = argparse.ArgumentParser(description="TSTR.site Status Manager")
    subparsers = parser.add_subparsers(dest="command")

    # Update Command
    update_parser = subparsers.add_parser("update", help="Update project status header")
    update_parser.add_argument("--agent", required=True, help="Name of the agent")

    # Log Command
    log_parser = subparsers.add_parser("log", help="Log a session action")
    log_parser.add_argument("--agent", required=True, help="Name of the agent")
    log_parser.add_argument("--action", required=True, help="Action taken")
    log_parser.add_argument("--result", required=True, help="Result achieved")

    args = parser.parse_args()

    if args.command == "update":
        update_status_header(args.agent)
    elif args.command == "log":
        log_session(args.agent, args.action, args.result)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
