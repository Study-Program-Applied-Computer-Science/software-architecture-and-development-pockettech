### sample for inter-microservice communication to include correlation ID using make request


# from common.utils.http_client import make_request
# 
# def get_transactions(): 
#     """Fetch transactions from the transaction service."""
#     transaction_service_url = "user-transaction_service_url-url"
#     response = make_request("GET", transaction_service_url)
    
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return {"error": "Failed to fetch transactions"}
