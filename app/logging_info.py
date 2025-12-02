"""
Centralized logging configuration for Expense Tracker.

Provides a single logger instance for all modules, with both
console and file output, and file rotation support.
"""

import logging
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("expense_tracker")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

file_handler = RotatingFileHandler(
    LOG_DIR / "expense_tracker.log",
    maxBytes=1_000_000,
    backupCount=5
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)