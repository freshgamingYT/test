import logging
import os
from logging.handlers import RotatingFileHandler

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[92m',  # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',  # Red
        'RESET': '\033[0m'  # Reset
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        message = super().format(record)
        return f"{color}{message}{self.COLORS['RESET']}"

def setup_logger():
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)

    # Ensure the logs directory exists
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Create rotating file handler
    log_file = os.path.join(log_dir, 'logfile.log')
    fh = RotatingFileHandler(log_file, maxBytes=0, backupCount=5)
    fh.setLevel(logging.DEBUG)

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatter and add it to the handlers
    formatter = ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.debug('Logger setup complete')
    return logger
