import logging
import os

class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[0;36m',    # Cyan
        'INFO': '\033[0;30m',     # Black
        'WARNING': '\033[0;33m',  # Yellow
        'ERROR': '\033[0;31m',    # Red
        'CRITICAL': '\033[0;35m', # Magenta
        'RESET': '\033[0m'
    }

    def format(self, record):
        message = super().format(record)
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        return f"{color}{message}{self.COLORS['RESET']}"

def _is_running_in_lambda():
    return (
            'AWS_LAMBDA_FUNCTION_NAME' in os.environ
            or 'LAMBDA_TASK_ROOT' in os.environ
            or ('AWS_EXECUTION_ENV' in os.environ and os.environ.get('AWS_EXECUTION_ENV', '').startswith('AWS'))
    )

def _parse_level(level):
    if isinstance(level, int):
        return level
    return getattr(logging, str(level).upper(), logging.DEBUG)

def setup_logger(name='news_app', level=os.getenv('LOG_LEVEL', 'DEBUG')):
    is_lambda = _is_running_in_lambda()
    level = _parse_level(level)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)

    if is_lambda:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger

logger = setup_logger()