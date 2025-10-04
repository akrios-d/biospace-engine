import os
import logging
from pymongo import MongoClient

# -------------------------
# UTF-8 Safe Console Handler
# -------------------------
class Utf8ConsoleHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            # Encode to UTF-8 and replace any unencodable characters
            print(msg.encode("utf-8", errors="replace").decode("utf-8"))
        except Exception:
            self.handleError(record)

# -------------------------
# Logging setup
# -------------------------
def setup_logger(name="app"):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

        # File handler (UTF-8)
        file_handler = logging.FileHandler("app.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console handler (UTF-8 safe)
        console_handler = Utf8ConsoleHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()

# -------------------------
# MongoDB setup
# -------------------------
def get_mongo_collection(db_name="spaceapps", collection_name="publications"):
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(mongo_uri)
    db = client[db_name]
    return db[collection_name]
