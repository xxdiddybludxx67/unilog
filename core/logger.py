import os
import sys
from datetime import datetime
from enum import Enum
from typing import Optional

# Default log directory
LOG_DIR = os.getenv("UNILOG_LOG_DIR", "./logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Log levels
class LogLevel(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


# Global log level
GLOBAL_LOG_LEVEL = LogLevel.DEBUG


def format_message(message: str, level: LogLevel = LogLevel.INFO, timestamp: bool = True) -> str:
    """
    Format the log message with optional timestamp and level.
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if timestamp else ""
    return f"[{ts}][{level.name}] {message}" if ts else f"[{level.name}] {message}"


def log(message: str, level: LogLevel = LogLevel.INFO, file: Optional[str] = None, console: bool = True):
    if level.value < GLOBAL_LOG_LEVEL.value:
        return

    formatted = format_message(message, level)

    if console:
        if level in (LogLevel.ERROR, LogLevel.CRITICAL):
            print(formatted, file=sys.stderr)
        else:
            print(formatted)

    if file:
        # Ensure directory exists
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    else:
        # Default: write to daily log file
        log_file = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.log")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")


# Convenience functions for each log level
def debug(msg: str, file: Optional[str] = None):
    log(msg, level=LogLevel.DEBUG, file=file)

def info(msg: str, file: Optional[str] = None):
    log(msg, level=LogLevel.INFO, file=file)

def warning(msg: str, file: Optional[str] = None):
    log(msg, level=LogLevel.WARNING, file=file)

def error(msg: str, file: Optional[str] = None):
    log(msg, level=LogLevel.ERROR, file=file)

def critical(msg: str, file: Optional[str] = None):
    log(msg, level=LogLevel.CRITICAL, file=file)


def set_global_log_level(level: LogLevel):
    """
    Set the global log level.
    Messages below this level will be ignored.
    """
    global GLOBAL_LOG_LEVEL
    GLOBAL_LOG_LEVEL = level
    info(f"Global log level set to {level.name}")
