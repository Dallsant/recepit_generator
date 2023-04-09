import logging


# Create a logger instance
from config import get_config

logger = logging.getLogger(__name__)

# Configure the logger
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Add a console handler to log to the terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Add a file handler to log to the file
file_handler = logging.FileHandler(filename=get_config().LOGGING_FILE_NAME, encoding="utf-8", mode="w")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)