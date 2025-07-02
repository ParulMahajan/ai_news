import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[0;36m',    # Cyan
        'INFO': '\033[0;30m',     # Black
        'WARNING': '\033[0;33m',  # Yellow
        'ERROR': '\033[0;31m',    # Red
        'CRITICAL': '\033[0;35m', # Magenta
        'RESET': '\033[0m'        # Reset
    }

    def format(self, record):
        if isinstance(self.handler, logging.StreamHandler) and not isinstance(self.handler, logging.FileHandler):
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            message = super().format(record)
            return f"{color}{message}{self.COLORS['RESET']}"
        return super().format(record)

def setup_logger(
        name='news_app',
        level=os.getenv('LOG_LEVEL', 'INFO'),
        log_dir='logs',
        max_bytes=10*1024*1024,  # 10MB
        backup_count=5
):
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Clear existing handlers
    logger.handlers.clear()

    # File handler with rotation
    log_file = f"{log_dir}/news_app_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    file_handler.setLevel(level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Formatters
    file_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    color_formatter = ColorFormatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(color_formatter)
    color_formatter.handler = console_handler

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create and expose logger instance
logger = setup_logger()