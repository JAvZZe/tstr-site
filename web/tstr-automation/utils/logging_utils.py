import json
import logging
from datetime import datetime
from typing import Any

def json_log(level: str, message: str, **data: Any) -> None:
    """
    Log a message as a JSON object for structured logging.
    
    Args:
        level: Log level (e.g., "INFO", "WARNING", "ERROR")
        message: Log message
        **data: Additional data to include in the log entry
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "message": message,
        **data
    }
    # Use standard logging but with JSON-formatted message
    logging.log(
        level_to_numeric(level),
        json.dumps(log_entry)
    )

def level_to_numeric(level: str) -> int:
    """Convert log level string to numeric value."""
    level = level.upper()
    levels = {
        "DEBUG": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
        "CRITICAL": 50
    }
    return levels.get(level, 20)

# Convenience functions for each level
def json_debug(message: str, **data: Any) -> None:
    json_log("DEBUG", message, **data)

def json_info(message: str, **data: Any) -> None:
    json_log("INFO", message, **data)

def json_warning(message: str, **data: Any) -> None:
    json_log("WARNING", message, **data)

def json_error(message: str, **data: Any) -> None:
    json_log("ERROR", message, **data)