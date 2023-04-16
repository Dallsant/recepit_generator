import logging
from config import get_config

logger = logging.getLogger(__name__)

# Configure the logger
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s:     %(asctime)s - %(message)s")

class JsonFormatter(logging.Formatter):
    def format(self, record):
        record.message = json.dumps(record.msg)
        return super().format(record)

# Add a console handler to log to the terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Add a file handler to log to the file
file_handler = logging.FileHandler(filename=get_config().LOGGING_FILE_NAME, encoding="utf-8", mode="a")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)