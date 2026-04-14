#!/usr/bin/env python3
"""
Test script for basic API endpoints.
Run this to test login, register, and logout functionality.
"""

import requests
import json
from typing import Optional

# Configuration
BASE_URL = "http://localhost:8000"
API_V1_STR = "/api/v1"

class APITester:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.headers = {"Content-Type": "application/json"}

    def register_user(self, email: str, password: str, tenant_id: str = "default-tenant"):
        """Register a new user."""
        url = f"{self.base_url}{API_V1_STR}/auth/register"
        data = {
            "email": email,
            "password": password,
            "tenant_id": tenant_id
        }

        try:
            response = requests.post(url, json=data, headers=self.headers)
            print(f"Register Response: {response.status_code}")
            if response.status_code == 200:
                print("✓ User registered successfully")
                return response.json()
            else:
                print(f"✗ Registration failed: {response.text}")
                return None
        except Exception as e:
            print(f"✗ Registration error: {e}")
            return None

    def login(self, email: str, password: str):
        """Login with email and password."""
        url = f"{self.base_url}{API_V1_STR}/auth/login"
        data = {
            "username": email,
            "password": password
        }

        try:
            response = requests.post(url, data=data)
            print(f"Login Response: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                self.token = result.get("access_token")
                if self.token:
                    self.headers["Authorization"] = f"Bearer {self.token}"
                    print("✓ Login successful, token received")
                    return result
                else:
                    print("✗ No token in response")
                    return None
            else:
                print(f"✗ Login failed: {response.text}")
                return None
        except Exception as e:
            print(f"✗ Login error: {e}")
            return None

    def logout(self):
        """Logout current user."""
        if not self.token:
            print("✗ No active session to logout")
            return None

        url = f"{self.base_url}{API_V1_STR}/auth/logout"

        try:
            response = requests.post(url, headers=self.headers)
            print(f"Logout Response: {response.status_code}")
            if response.status_code == 200:
                print("✓ Logout successful")
                self.token = None
                self.headers.pop("Authorization", None)
                return response.json()
            else:
                print(f"✗ Logout failed: {response.text}")
                return None
        except Exception as e:
            print(f"✗ Logout error: {e}")
            return None

    def test_health(self):
        """Test health check endpoint."""
        url = f"{self.base_url}/health"

        try:
            response = requests.get(url)
            print(f"Health Check Response: {response.status_code}")
            if response.status_code == 200:
                print("✓ Health check passed")
                return response.json()
            else:
                print(f"✗ Health check failed: {response.text}")
                return None
        except Exception as e:
            print(f"✗ Health check error: {e}")
            return None


def main():
    """Run basic API tests."""
    print("🚀 Testing AI FinOps Platform API")
    print("=" * 50)

    tester = APITester()

    # Test health check
    print("\n1. Testing Health Check")
    health_result = tester.test_health()

    # Test user registration
    print("\n2. Testing User Registration")
    user_data = tester.register_user("test@example.com", "password123")

    # Test login
    print("\n3. Testing Login")
    login_result = tester.login("test@example.com", "password123")

    # Test logout
    print("\n4. Testing Logout")
    if login_result:
        logout_result = tester.logout()
    else:
        print("✗ Skipping logout - login failed")

    print("\n" + "=" * 50)
    print("✅ API testing completed!")


if __name__ == "__main__":
    main()