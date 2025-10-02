import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def get_logger(name: str = "voting_app_logger") -> logging.Logger:
    return logging.getLogger(name)
