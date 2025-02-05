import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app  # Assuming FastAPI app is defined in app.main
from app.routes.authRoute import login_user  # Importing the login function
from app.utils.verify_password import verify_password
from app.utils.jwt_rsa import create_access_token
from app.config import settings

class TestLoginAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.login_url = "http://auth_service:8001/api/v1/auth/login"
        self.mock_user = {
            "id": "12345",
            "email_id": "test@example.com",
            "password": "$2b$12$hashedpasswordhere" 
        }
        self.valid_request_payload = {
            "email_id": "test@example.com",
            "password": "validpassword"
        }
    

    @patch("requests.get")  
    @patch("app.utils.verify_password.pwd_context.verify")  
    @patch("app.routes.authRoute.create_access_token")
    def test_login_success(self, mock_create_token, mock_verify_password, mock_requests_get):
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [self.mock_user]
        mock_requests_get.return_value = mock_response
        mock_verify_password.return_value = True
        mock_create_token.return_value = "mocked_jwt_token"
        
        response = self.client.post(self.login_url, json=self.valid_request_payload)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertIn("access_token", response.json())  
        self.assertIsInstance(response.json()["access_token"], str)  

        mock_requests_get.assert_called_once_with(f"{settings.user_login_service_url}", headers=unittest.mock.ANY)
        mock_verify_password.assert_called_once_with("validpassword", self.mock_user["password"])
        
        self.assertEqual(mock_create_token.call_count, 2)
    

    @patch("requests.get")
    def test_login_user_not_found(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [] 
        mock_requests_get.return_value = mock_response
        
        response = self.client.post(self.login_url, json=self.valid_request_payload)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "User not found")
    

    @patch("requests.get")
    @patch("app.utils.verify_password.pwd_context.verify")
    def test_login_invalid_password(self, mock_verify_password, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [self.mock_user]
        mock_requests_get.return_value = mock_response
        mock_verify_password.return_value = False  
        
        response = self.client.post(self.login_url, json=self.valid_request_payload)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Invalid credentials")

if __name__ == "__main__":
    unittest.main()