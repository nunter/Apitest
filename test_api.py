import requests
import pytest
import allure

BASE_URL = "http://localhost:5001"

@allure.feature("User Management")
@allure.story("Get Users")
@allure.severity(allure.severity_level.NORMAL)
def test_get_users_pagination():
    """Test getting users with pagination."""
    with allure.step("Request page 1 with limit 2"):
        response = requests.get(f"{BASE_URL}/users", params={"page": 1, "limit": 2})
    
    with allure.step("Verify response"):
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 2
        assert data["page"] == 1
        assert data["limit"] == 2
        assert "total" in data

@allure.feature("User Management")
@allure.story("Get Users")
def test_get_users_filtering():
    """Test filtering users by name."""
    with allure.step("Filter by name 'Alice'"):
        response = requests.get(f"{BASE_URL}/users", params={"name": "Alice"})
    
    with allure.step("Verify Alice is found"):
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) >= 1
        assert data["data"][0]["name"] == "Alice"

@allure.feature("User Management")
@allure.story("Create User")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_user():
    """Test creating a new user."""
    new_user = {
        "name": "Charlie New",
        "email": "charlie.new@example.com"
    }
    with allure.step("Send POST request to create user"):
        response = requests.post(f"{BASE_URL}/users", json=new_user)
    
    with allure.step("Verify creation"):
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Charlie New"
        assert "id" in data

@allure.feature("User Management")
@allure.story("Get Users")
def test_get_single_user():
    """Test getting a single user by ID."""
    user_id = 1
    with allure.step(f"Get user with ID {user_id}"):
        response = requests.get(f"{BASE_URL}/users/{user_id}")
    
    with allure.step("Verify user details"):
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["name"] == "Alice"

@allure.feature("User Management")
@allure.story("Update User")
def test_update_user():
    """Test updating a user."""
    user_id = 2
    update_data = {"name": "Bob Updated"}
    with allure.step(f"Update user {user_id}"):
        response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
    
    with allure.step("Verify update"):
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Bob Updated"

@allure.feature("User Management")
@allure.story("Delete User")
def test_delete_user():
    """Test deleting a user."""
    with allure.step("Create a temporary user to delete"):
        new_user = {"name": "To Delete", "email": "delete@example.com"}
        create_resp = requests.post(f"{BASE_URL}/users", json=new_user)
        user_id = create_resp.json()["id"]
    
    with allure.step(f"Delete user {user_id}"):
        delete_resp = requests.delete(f"{BASE_URL}/users/{user_id}")
        assert delete_resp.status_code == 200
    
    with allure.step("Verify user is gone"):
        get_resp = requests.get(f"{BASE_URL}/users/{user_id}")
        assert get_resp.status_code == 404

@allure.feature("User Management")
@allure.story("Create User")
def test_create_user_invalid_data():
    """Test creating a user with invalid data."""
    invalid_data = {"name": "No Email"}
    with allure.step("Send invalid data"):
        response = requests.post(f"{BASE_URL}/users", json=invalid_data)
    assert response.status_code == 400

@allure.feature("Authentication")
@allure.story("Login")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_success():
    """Test successful login."""
    credentials = {"username": "admin", "password": "password"}
    with allure.step("Login with valid credentials"):
        response = requests.post(f"{BASE_URL}/login", json=credentials)
    
    with allure.step("Verify token received"):
        assert response.status_code == 200
        assert "token" in response.json()

@allure.feature("Authentication")
@allure.story("Login")
def test_login_failure():
    """Test failed login."""
    credentials = {"username": "admin", "password": "wrongpassword"}
    with allure.step("Login with invalid credentials"):
        response = requests.post(f"{BASE_URL}/login", json=credentials)
    assert response.status_code == 401

@allure.feature("Authentication")
@allure.story("Protected Resource")
def test_protected_endpoint_success():
    """Test accessing protected endpoint with valid token."""
    with allure.step("Login to get token"):
        login_resp = requests.post(f"{BASE_URL}/login", json={"username": "admin", "password": "password"})
        token = login_resp.json()["token"]
    
    with allure.step("Access protected resource with token"):
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/protected", headers=headers)
    
    with allure.step("Verify access granted"):
        assert response.status_code == 200
        assert response.json()["secret_data"] == "42"

@allure.feature("Authentication")
@allure.story("Protected Resource")
def test_protected_endpoint_unauthorized():
    """Test accessing protected endpoint without token."""
    with allure.step("Access protected resource without token"):
        response = requests.get(f"{BASE_URL}/protected")
    assert response.status_code == 401
