#!/usr/bin/env python3
"""
tstr.directory Scraper Failure Monitor
Checks scraper logs for failures and sends alerts
"""

import logging
import os
import re
import sys
from datetime import datetime, timedelta

from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Configuration
LOG_FILE = "/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working/web/tstr-automation/scraper.log"
ALERT_LOG_FILE = "/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working/web/tstr-automation/scraper_alerts.log"
CHECK_HOURS = int(os.getenv('SCRAPER_MONITOR_CHECK_HOURS', '2'))  # How far back to check for errors

# Setup logging for the monitor itself
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(ALERT_LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('ScraperMonitor')

# Error patterns to look for in logs
ERROR_PATTERNS = [
    r'CRON JOB FAILED',
    r'Exception.*scraper.*failed',
    r'Error.*scraper',
    r'failed.*scraper',
    r'Traceback.*most recent call last',
    r'APIError:',
    r'ValidationError:',
    r'ConnectionError',
    r'TimeoutError',
    r'HTTP.*Error',
    r'JSON.*could not be generated',
    r'Invalid API key',
    r'Authentication failed',
    r'Permission denied',
    r'Exited with code.*[1-9]',  # Non-zero exit codes
]

def read_recent_logs(log_file, hours=CHECK_HOURS):
    """Read log entries from the last N hours"""
    if not os.path.exists(log_file):
        logger.warning(f"Log file not found: {log_file}")
        return []

    cutoff_time = datetime.now() - timedelta(hours=hours)
    recent_lines = []

    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Extract timestamp from log line (assuming format: YYYY-MM-DD HH:MM:SS)
                timestamp_match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                if timestamp_match:
                    try:
                        log_time = datetime.strptime(timestamp_match.group(1), '%Y-%m-%d %H:%M:%S')
                        if log_time >= cutoff_time:
                            recent_lines.append(line)
                    except ValueError:
                        # If timestamp parsing fails, include line anyway (better safe than sorry)
                        recent_lines.append(line)
                else:
                    # No timestamp found, include line
                    recent_lines.append(line)
    except Exception as e:
        logger.error(f"Error reading log file: {e}")
        return []

    return recent_lines

def detect_errors(log_lines):
    """Detect errors in log lines based on patterns"""
    errors = []

    for line in log_lines:
        for pattern in ERROR_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                errors.append(line)
                break  # Avoid duplicate entries for same line matching multiple patterns

    return errors

def main():
    """Main monitoring function"""
    logger.info("=Starting tstr.directory scraper failure monitor=")
    logger.info(f"Checking scraper logs from last {CHECK_HOURS} hour(s)")
    logger.info(f"Log file: {LOG_FILE}")

    # Check if log file exists
    if not os.path.exists(LOG_FILE):
        msg = f"Scraper log file not found: {LOG_FILE}"
        logger.warning(msg)
        # This might be OK if scraper hasn't run yet
        return 0

    # Read recent logs
    recent_logs = read_recent_logs(LOG_FILE, CHECK_HOURS)

    if not recent_logs:
        msg = "No recent log entries found"
        logger.info(msg)
        return 0

    # Detect errors
    errors = detect_errors(recent_logs)

    if errors:
        error_count = len(errors)
        msg = f"Detected {error_count} scraper error(s) in the last {CHECK_HOURS} hour(s)"
        logger.error(msg)

        # Log each error
        for i, error in enumerate(errors, 1):
            logger.error(f"Error {i}: {error}")

        # Write to alert log file (in addition to logging)
        try:
            with open(ALERT_LOG_FILE, 'a') as f:
                f.write(f"\n[{datetime.now()}] ALERT: {msg}\n")
                for i, error in enumerate(errors, 1):
                    f.write(f"  Error {i}: {error}\n")
                f.write("-" * 60 + "\n")
        except Exception as e:
            logger.error(f"Failed to write to alert log file: {e}")

        return 1  # Indicate errors found
    else:
        msg = "No scraper errors detected in recent logs"
        logger.info(msg)
        return 0

if __name__ == "__main__":
    sys.exit(main())