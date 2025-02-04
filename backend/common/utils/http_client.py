import requests
from common.config.correlation import get_correlation_id

def make_request(method, url, headers=None, **kwargs):
    """Make an HTTP request to another microservice, ensuring correlation ID is passed."""
    
    # Get current correlation ID (or generate one if missing)
    correlation_id = get_correlation_id() or "generated-correlation-id"

    # Ensure headers are initialized
    headers = headers or {}
    headers["X-Correlation-ID"] = correlation_id  # Attach correlation ID
    
    response = requests.request(method, url, headers=headers, **kwargs)
    return response
