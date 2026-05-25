import logging
import os

# Create logs folder if not present
os.makedirs("logs", exist_ok=True)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,

    format="%(asctime)s [%(levelname)s] %(message)s",

    handlers=[
        logging.FileHandler("logs/etl.log"),
        logging.StreamHandler()
    ]
)

# Logger object
logger = logging.getLogger(__name__)