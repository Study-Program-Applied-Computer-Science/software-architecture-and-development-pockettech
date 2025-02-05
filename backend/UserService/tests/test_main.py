# from fastapi.testclient import TestClient
# from unittest.mock import patch, MagicMock

# #print folder path
# import os
# import sys
# print("-----------------TEST-----------------------------------")
# print('first',sys.path)

# #sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../app")))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../")))
# print("-----------------TEST21-----------------------------------")

# print('second',sys.path)

# print("List of directories in sys.path: ../")
# for path in sys.path:
#     print(path)


# # Function to print all files and folders in a directory recursively
# def print_directory_contents(path):
#     for dirpath, dirnames, filenames in os.walk(path):
#         print(f'Current directory: {dirpath}')
#         for dirname in dirnames:
#             print(f'  Subfolder: {dirname}')
#         for filename in filenames:
#             print(f'  File: {filename}')

# # Print the contents of each directory in sys.path
# for path in sys.path:
#     print(f"Inspecting directory: {path}")
#   #  print_directory_contents(path)



# from app.main import app





# # print("List of directories in sys.path: ../")
# # for path in sys.path:
# #     print(path)


# #from app.main import app

# client = TestClient(app)

# def test_login_user():
#     mock_response = MagicMock()
#     mock_response.status_code = 200
#     mock_response.json.return_value = {"id": "12345"}

#     with patch("requests.post", return_value=mock_response) as mock_post, \
#          patch("app.utils.jwt_rsa.create_access_token", return_value="mock_token") as mock_token:
        
#         response = client.post("/api/v1/auth/login", json={"email_id": "test@example.com", "password": "securepassword"})
        
#         assert response.status_code == 200
#         assert response.json()["access_token"] == "mock_token"
#         assert response.json()["id"] == "12345"
        
#         mock_post.assert_called_once()
#         mock_token.assert_called_once()

def test_dummy():
    """A simple test to verify that testing setup works."""
    assert 2 > 1
