import os
import logging
from logging.handlers import TimedRotatingFileHandler
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
ELASTIC_ENDPOINT = os.getenv("ELASTIC_ENDPOINT")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
SERVICE_NAME = os.getenv("SERVICE_NAME", "TransactionAnalysisService")

# Configure Elasticsearch logging
class ElasticsearchHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.client = Elasticsearch(
            ELASTIC_ENDPOINT,
            basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD),
            verify_certs=True,
        )

    def emit(self, record):
        log_entry = self.format(record)
        self.client.index(index="logs-service", document={"message": log_entry})

def setup_logger():
    logger = logging.getLogger(SERVICE_NAME)
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(console_handler)

    if ELASTIC_ENDPOINT:
        es_handler = ElasticsearchHandler()
        es_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(es_handler)

    return logger

logger = setup_logger()
