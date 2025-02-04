from functools import partial
import uuid
from datetime import datetime
from common.config.correlation import get_correlation_id
from loguru import logger
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()

ES_HOST = os.getenv("ELASTIC_ENDPOINT")
ES_USERNAME = os.getenv("ELASTIC_USERNAME")
ES_PASSWORD = os.getenv("ELASTIC_PASSWORD")

# Initialize Elasticsearch client
es = Elasticsearch(
    ES_HOST,
    basic_auth=(ES_USERNAME, ES_PASSWORD)
)

# Check Elasticsearch connection
def test_elasticsearch_connection():
    """Test connection to Elasticsearch."""
    if es.ping():
        logger.info("Elasticsearch connection successful.")
    else:
        logger.error("Elasticsearch connection failed.")
        print("Error: Elasticsearch connection failed.")

# Loguru Elasticsearch handler function
def loguru_elasticsearch_handler(record, service_name):
    """Loguru Elasticsearch handler to send logs to ElasticSearch."""
    if isinstance(record, str):
        log_message = record
        log_level = 'INFO'  # Default to INFO if no level is provided
        log_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    else:
        log_message = record.get('message', '')  # Safe access to 'message'
        log_level = record.get('level', {}).get('name', 'INFO')  # Safe access to 'level'
        log_time = record.get('time', datetime.utcnow()).strftime('%Y-%m-%d %H:%M:%S')  # Default to UTC time if no time is provided
    
    correlation_id = get_correlation_id() or str(uuid.uuid4())  # Use existing or generate a new correlation ID
    log_id = str(uuid.uuid4())  # Generate a unique log ID

    log_data = {
        "log_id": log_id,
        "correlation_id": correlation_id,
        "service": service_name,
        "message": log_message,
        "level": log_level,
        "time": log_time,
    }

    try:
        # Send the log to Elasticsearch with the custom log ID
        es.index(index="logs", id=log_id, body=log_data)
    except Exception as e:
        logger.error(f"Failed to send log to Elasticsearch: {e}")
        print(f"Error sending log to Elasticsearch: {e}")

# Setup Loguru with the custom Elasticsearch handler
def setup_logger(service_name):
    logger.remove()  # Remove default logger
    logger.add(partial(loguru_elasticsearch_handler, service_name=service_name), level="INFO", serialize=True)  # Serialize logs to JSON
    return logger

# Test Elasticsearch connection at startup
test_elasticsearch_connection()
