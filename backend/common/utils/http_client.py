import requests

def make_request(method, url, headers=None, **kwargs):
    """Make an HTTP request to another microservice, ensuring correlation ID is passed."""

    # Ensure headers are initialized
    headers = headers or {}
    
    response = requests.request(method, url, headers=headers, **kwargs)
    return response