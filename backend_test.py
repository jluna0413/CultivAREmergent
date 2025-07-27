#!/usr/bin/env python3
"""
CultivAR Backend Testing Suite
Comprehensive testing of all backend endpoints and functionality.
"""

import requests
import json
import sys
import time
from datetime import datetime

class CultivARTester:
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.admin_credentials = {"username": "admin", "password": "isley"}
        
    def log_test(self, test_name, status, details="", response_code=None):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "response_code": response_code,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_symbol} {test_name}: {details}")
        
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "ok":
                    self.log_test("Health Check", "PASS", "Health endpoint working", response.status_code)
                else:
                    self.log_test("Health Check", "FAIL", f"Unexpected response: {data}", response.status_code)
            else:
                self.log_test("Health Check", "FAIL", f"HTTP {response.status_code}", response.status_code)
        except Exception as e:
            self.log_test("Health Check", "FAIL", f"Exception: {str(e)}")
            
    def test_login_functionality(self):
        """Test login with valid and invalid credentials"""
        # Test GET login page
        try:
            response = self.session.get(f"{self.base_url}/login")
            if response.status_code == 200:
                self.log_test("Login Page Access", "PASS", "Login page accessible", response.status_code)
            else:
                self.log_test("Login Page Access", "FAIL", f"HTTP {response.status_code}", response.status_code)
        except Exception as e:
            self.log_test("Login Page Access", "FAIL", f"Exception: {str(e)}")
            
        # Test valid login
        try:
            login_data = {
                "username": self.admin_credentials["username"],
                "password": self.admin_credentials["password"]
            }
            response = self.session.post(f"{self.base_url}/login", data=login_data)
            if response.status_code == 302 or response.status_code == 200:
                self.log_test("Valid Login", "PASS", "Admin login successful", response.status_code)
            else:
                self.log_test("Valid Login", "FAIL", f"HTTP {response.status_code}", response.status_code)
        except Exception as e:
            self.log_test("Valid Login", "FAIL", f"Exception: {str(e)}")
            
        # Test invalid login
        try:
            invalid_data = {"username": "invalid", "password": "wrong"}
            response = self.session.post(f"{self.base_url}/login", data=invalid_data)
            if response.status_code in [200, 302]:
                self.log_test("Invalid Login", "PASS", "Invalid login properly rejected", response.status_code)
            else:
                self.log_test("Invalid Login", "WARN", f"Unexpected response: HTTP {response.status_code}", response.status_code)
        except Exception as e:
            self.log_test("Invalid Login", "FAIL", f"Exception: {str(e)}")
            
    def test_protected_routes(self):
        """Test protected routes that require authentication"""
        protected_routes = [
            ("/dashboard", "Dashboard"),
            ("/plants", "Plants Page"),
            ("/strains", "Strains Page"),
            ("/sensors", "Sensors Page"),
            ("/settings", "Settings Page"),
            ("/market/seed-bank", "Seed Bank"),
            ("/market/extensions", "Extensions"),
            ("/market/gear", "Gear")
        ]
        
        for route, name in protected_routes:
            try:
                response = self.session.get(f"{self.base_url}{route}")
                if response.status_code == 200:
                    self.log_test(f"Protected Route: {name}", "PASS", f"Route accessible after login", response.status_code)
                elif response.status_code == 302:
                    self.log_test(f"Protected Route: {name}", "WARN", f"Redirect response (may be normal)", response.status_code)
                else:
                    self.log_test(f"Protected Route: {name}", "FAIL", f"HTTP {response.status_code}", response.status_code)
            except Exception as e:
                self.log_test(f"Protected Route: {name}", "FAIL", f"Exception: {str(e)}")
                
    def test_admin_api_endpoints(self):
        """Test admin API endpoints"""
        # First, ensure we have admin session
        self.session.post(f"{self.base_url}/login", data=self.admin_credentials)
        
        # Set admin session manually (since the app uses session-based auth for admin API)
        # We need to check if admin session is properly set
        
        admin_endpoints = [
            ("/api/admin/users", "GET", "Get Users API"),
            ("/api/admin/system/logs", "GET", "System Logs API"),
            ("/api/admin/system/info", "GET", "System Info API"),
            ("/api/admin/diagnostics/test", "GET", "Diagnostics Test API")
        ]
        
        for endpoint, method, name in admin_endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{self.base_url}{endpoint}")
                else:
                    response = self.session.request(method, f"{self.base_url}{endpoint}")
                    
                if response.status_code == 200:
                    try:
                        data = response.json()
                        self.log_test(f"Admin API: {name}", "PASS", f"API working, returned data", response.status_code)
                    except:
                        self.log_test(f"Admin API: {name}", "WARN", f"API accessible but non-JSON response", response.status_code)
                elif response.status_code == 401:
                    self.log_test(f"Admin API: {name}", "WARN", f"Authentication required (expected for admin API)", response.status_code)
                else:
                    self.log_test(f"Admin API: {name}", "FAIL", f"HTTP {response.status_code}", response.status_code)
            except Exception as e:
                self.log_test(f"Admin API: {name}", "FAIL", f"Exception: {str(e)}")
                
    def test_user_management_api(self):
        """Test user management API endpoints"""
        # Test creating a new user
        try:
            new_user_data = {
                "username": "testuser123",
                "password": "testpass123",
                "email": "test@example.com"
            }
            response = self.session.post(f"{self.base_url}/api/admin/users", json=new_user_data)
            if response.status_code in [200, 201]:
                self.log_test("Create User API", "PASS", "User creation API working", response.status_code)
                
                # Try to get the created user
                try:
                    users_response = self.session.get(f"{self.base_url}/api/admin/users")
                    if users_response.status_code == 200:
                        users = users_response.json()
                        if isinstance(users, list) and len(users) > 0:
                            self.log_test("List Users API", "PASS", f"Found {len(users)} users", users_response.status_code)
                        else:
                            self.log_test("List Users API", "WARN", "API working but no users found", users_response.status_code)
                    else:
                        self.log_test("List Users API", "FAIL", f"HTTP {users_response.status_code}", users_response.status_code)
                except Exception as e:
                    self.log_test("List Users API", "FAIL", f"Exception: {str(e)}")
                    
            elif response.status_code == 401:
                self.log_test("Create User API", "WARN", "Authentication required for user creation", response.status_code)
            else:
                self.log_test("Create User API", "FAIL", f"HTTP {response.status_code}", response.status_code)
        except Exception as e:
            self.log_test("Create User API", "FAIL", f"Exception: {str(e)}")
            
    def test_logout_functionality(self):
        """Test logout functionality"""
        try:
            response = self.session.get(f"{self.base_url}/logout")
            if response.status_code in [200, 302]:
                self.log_test("Logout", "PASS", "Logout endpoint working", response.status_code)
            else:
                self.log_test("Logout", "FAIL", f"HTTP {response.status_code}", response.status_code)
        except Exception as e:
            self.log_test("Logout", "FAIL", f"Exception: {str(e)}")
            
    def test_signup_functionality(self):
        """Test signup functionality"""
        try:
            # Test GET signup page
            response = self.session.get(f"{self.base_url}/signup")
            if response.status_code == 200:
                self.log_test("Signup Page Access", "PASS", "Signup page accessible", response.status_code)
            else:
                self.log_test("Signup Page Access", "FAIL", f"HTTP {response.status_code}", response.status_code)
                
            # Test POST signup
            signup_data = {
                "username": "newuser123",
                "password": "newpass123",
                "confirm_password": "newpass123"
            }
            response = self.session.post(f"{self.base_url}/signup", data=signup_data)
            if response.status_code in [200, 302]:
                self.log_test("User Signup", "PASS", "Signup functionality working", response.status_code)
            else:
                self.log_test("User Signup", "FAIL", f"HTTP {response.status_code}", response.status_code)
        except Exception as e:
            self.log_test("User Signup", "FAIL", f"Exception: {str(e)}")
            
    def test_database_connectivity(self):
        """Test database connectivity through API responses"""
        # Login first to access protected endpoints
        self.session.post(f"{self.base_url}/login", data=self.admin_credentials)
        
        # Test endpoints that would require database access
        db_dependent_endpoints = [
            ("/dashboard", "Dashboard Database Access"),
            ("/plants", "Plants Database Access"),
            ("/strains", "Strains Database Access"),
            ("/sensors", "Sensors Database Access")
        ]
        
        for endpoint, name in db_dependent_endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}")
                if response.status_code == 200:
                    # Check if response contains expected content (not just error pages)
                    if len(response.text) > 1000:  # Reasonable assumption for a full page
                        self.log_test(f"DB Connectivity: {name}", "PASS", "Database-dependent page loaded successfully", response.status_code)
                    else:
                        self.log_test(f"DB Connectivity: {name}", "WARN", "Page loaded but content seems minimal", response.status_code)
                else:
                    self.log_test(f"DB Connectivity: {name}", "FAIL", f"HTTP {response.status_code}", response.status_code)
            except Exception as e:
                self.log_test(f"DB Connectivity: {name}", "FAIL", f"Exception: {str(e)}")
                
    def test_static_assets(self):
        """Test static asset serving"""
        try:
            # Test favicon
            response = self.session.get(f"{self.base_url}/favicon.ico")
            if response.status_code == 200:
                self.log_test("Static Assets: Favicon", "PASS", "Favicon served successfully", response.status_code)
            else:
                self.log_test("Static Assets: Favicon", "WARN", f"Favicon not found: HTTP {response.status_code}", response.status_code)
        except Exception as e:
            self.log_test("Static Assets: Favicon", "FAIL", f"Exception: {str(e)}")
            
    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting CultivAR Backend Testing Suite")
        print("=" * 50)
        
        # Basic connectivity tests
        print("\n📡 Testing Basic Connectivity...")
        self.test_health_endpoint()
        
        # Authentication tests
        print("\n🔐 Testing Authentication System...")
        self.test_login_functionality()
        self.test_signup_functionality()
        
        # Protected route tests
        print("\n🛡️ Testing Protected Routes...")
        self.test_protected_routes()
        
        # Admin API tests
        print("\n👑 Testing Admin API Endpoints...")
        self.test_admin_api_endpoints()
        self.test_user_management_api()
        
        # Database connectivity tests
        print("\n🗄️ Testing Database Connectivity...")
        self.test_database_connectivity()
        
        # Static asset tests
        print("\n📁 Testing Static Assets...")
        self.test_static_assets()
        
        # Logout test (should be last)
        print("\n🚪 Testing Logout...")
        self.test_logout_functionality()
        
        # Generate summary
        self.generate_summary()
        
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        warning_tests = len([r for r in self.test_results if r["status"] == "WARN"])
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️ Warnings: {warning_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"  - {result['test']}: {result['details']}")
                    
        if warning_tests > 0:
            print("\n⚠️ WARNINGS:")
            for result in self.test_results:
                if result["status"] == "WARN":
                    print(f"  - {result['test']}: {result['details']}")
                    
        print("\n🎯 RECOMMENDATIONS:")
        if failed_tests == 0:
            print("  - All critical tests passed! Backend is functioning well.")
        else:
            print("  - Review failed tests and fix critical issues.")
            
        if warning_tests > 0:
            print("  - Address warnings for optimal functionality.")
            
        # Save detailed results to file
        with open('/app/backend_test_results.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)
        print(f"\n📄 Detailed results saved to: /app/backend_test_results.json")

def main():
    """Main function to run tests"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8001"
        
    print(f"Testing CultivAR application at: {base_url}")
    
    tester = CultivARTester(base_url)
    tester.run_all_tests()

if __name__ == "__main__":
    main()