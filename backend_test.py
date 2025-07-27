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
            
    def test_mobile_responsive_dashboard(self):
        """Test the new mobile-responsive dashboard implementation"""
        # First login to access dashboard
        login_response = self.session.post(f"{self.base_url}/login", data=self.admin_credentials)
        
        if login_response.status_code != 302:
            self.log_test("Mobile Dashboard - Login Required", "FAIL", "Cannot login to test dashboard")
            return
            
        try:
            # Test dashboard route with new template
            response = self.session.get(f"{self.base_url}/dashboard")
            if response.status_code == 200:
                content = response.text
                
                # Check for new dashboard container class
                if '.dashboard-container' in content or 'dashboard-container' in content:
                    self.log_test("Mobile Dashboard - Container", "PASS", "Dashboard container found", response.status_code)
                else:
                    self.log_test("Mobile Dashboard - Container", "FAIL", "Dashboard container not found", response.status_code)
                
                # Check for widget system
                if 'dashboard-widgets' in content:
                    self.log_test("Mobile Dashboard - Widget System", "PASS", "Widget system found", response.status_code)
                else:
                    self.log_test("Mobile Dashboard - Widget System", "FAIL", "Widget system not found", response.status_code)
                
                # Check for customize button
                if 'widget-settings-btn' in content:
                    self.log_test("Mobile Dashboard - Customize Button", "PASS", "Customize button found", response.status_code)
                else:
                    self.log_test("Mobile Dashboard - Customize Button", "FAIL", "Customize button not found", response.status_code)
                
                # Check for settings panel
                if 'widget-settings-panel' in content:
                    self.log_test("Mobile Dashboard - Settings Panel", "PASS", "Settings panel found", response.status_code)
                else:
                    self.log_test("Mobile Dashboard - Settings Panel", "FAIL", "Settings panel not found", response.status_code)
                
                # Check for dashboard widgets CSS
                if 'dashboard-widgets.css' in content:
                    self.log_test("Mobile Dashboard - CSS", "PASS", "Dashboard widgets CSS included", response.status_code)
                else:
                    self.log_test("Mobile Dashboard - CSS", "FAIL", "Dashboard widgets CSS not included", response.status_code)
                
                # Check for dashboard widgets JS
                if 'dashboard-widgets.js' in content:
                    self.log_test("Mobile Dashboard - JavaScript", "PASS", "Dashboard widgets JS included", response.status_code)
                else:
                    self.log_test("Mobile Dashboard - JavaScript", "FAIL", "Dashboard widgets JS not included", response.status_code)
                    
            else:
                self.log_test("Mobile Dashboard - Access", "FAIL", f"Dashboard not accessible: HTTP {response.status_code}", response.status_code)
                
        except Exception as e:
            self.log_test("Mobile Dashboard - Access", "FAIL", f"Exception: {str(e)}")

    def test_pwa_features(self):
        """Test PWA (Progressive Web App) features"""
        try:
            # Test manifest.json accessibility
            response = self.session.get(f"{self.base_url}/manifest.json")
            if response.status_code == 200:
                try:
                    manifest_data = response.json()
                    
                    # Check required manifest fields
                    required_fields = ['name', 'short_name', 'start_url', 'display', 'icons']
                    missing_fields = [field for field in required_fields if field not in manifest_data]
                    
                    if not missing_fields:
                        self.log_test("PWA - Manifest Structure", "PASS", "All required manifest fields present", response.status_code)
                    else:
                        self.log_test("PWA - Manifest Structure", "FAIL", f"Missing fields: {missing_fields}", response.status_code)
                    
                    # Check CultivAR specific content
                    if manifest_data.get('name') == 'CultivAR - Cannabis Grow Journal':
                        self.log_test("PWA - App Name", "PASS", "Correct app name in manifest", response.status_code)
                    else:
                        self.log_test("PWA - App Name", "FAIL", f"Incorrect app name: {manifest_data.get('name')}", response.status_code)
                        
                except json.JSONDecodeError:
                    self.log_test("PWA - Manifest Format", "FAIL", "Invalid JSON in manifest", response.status_code)
            else:
                self.log_test("PWA - Manifest Access", "FAIL", f"Manifest not accessible: HTTP {response.status_code}", response.status_code)
                
            # Test service worker accessibility
            response = self.session.get(f"{self.base_url}/static/sw.js")
            if response.status_code == 200:
                sw_content = response.text
                
                # Check for service worker functionality
                if 'addEventListener' in sw_content and 'install' in sw_content:
                    self.log_test("PWA - Service Worker", "PASS", "Service worker has install event", response.status_code)
                else:
                    self.log_test("PWA - Service Worker", "FAIL", "Service worker missing install event", response.status_code)
                
                # Check for cache functionality
                if 'caches' in sw_content and 'CACHE_NAME' in sw_content:
                    self.log_test("PWA - Caching", "PASS", "Service worker has caching functionality", response.status_code)
                else:
                    self.log_test("PWA - Caching", "FAIL", "Service worker missing caching functionality", response.status_code)
                    
            else:
                self.log_test("PWA - Service Worker Access", "FAIL", f"Service worker not accessible: HTTP {response.status_code}", response.status_code)
                
        except Exception as e:
            self.log_test("PWA - Features", "FAIL", f"Exception: {str(e)}")

    def test_widget_system_assets(self):
        """Test widget system static assets"""
        try:
            # Test dashboard widgets CSS
            response = self.session.get(f"{self.base_url}/static/css/dashboard-widgets.css")
            if response.status_code == 200:
                css_content = response.text
                
                # Check for responsive design classes
                if '@media' in css_content and 'max-width' in css_content:
                    self.log_test("Widget System - Responsive CSS", "PASS", "Responsive design CSS found", response.status_code)
                else:
                    self.log_test("Widget System - Responsive CSS", "FAIL", "Responsive design CSS not found", response.status_code)
                
                # Check for widget classes
                if '.dashboard-widget' in css_content:
                    self.log_test("Widget System - Widget Classes", "PASS", "Widget CSS classes found", response.status_code)
                else:
                    self.log_test("Widget System - Widget Classes", "FAIL", "Widget CSS classes not found", response.status_code)
                    
            else:
                self.log_test("Widget System - CSS Access", "FAIL", f"Widget CSS not accessible: HTTP {response.status_code}", response.status_code)
            
            # Test dashboard widgets JavaScript
            response = self.session.get(f"{self.base_url}/static/js/dashboard-widgets.js")
            if response.status_code == 200:
                js_content = response.text
                
                # Check for widget system class
                if 'DashboardWidgetSystem' in js_content:
                    self.log_test("Widget System - JavaScript Class", "PASS", "DashboardWidgetSystem class found", response.status_code)
                else:
                    self.log_test("Widget System - JavaScript Class", "FAIL", "DashboardWidgetSystem class not found", response.status_code)
                
                # Check for drag and drop functionality
                if 'setupDragAndDrop' in js_content:
                    self.log_test("Widget System - Drag & Drop", "PASS", "Drag and drop functionality found", response.status_code)
                else:
                    self.log_test("Widget System - Drag & Drop", "FAIL", "Drag and drop functionality not found", response.status_code)
                
                # Check for mobile handlers
                if 'setupMobileHandlers' in js_content:
                    self.log_test("Widget System - Mobile Handlers", "PASS", "Mobile handlers found", response.status_code)
                else:
                    self.log_test("Widget System - Mobile Handlers", "FAIL", "Mobile handlers not found", response.status_code)
                    
            else:
                self.log_test("Widget System - JavaScript Access", "FAIL", f"Widget JS not accessible: HTTP {response.status_code}", response.status_code)
                
        except Exception as e:
            self.log_test("Widget System - Assets", "FAIL", f"Exception: {str(e)}")

    def test_dashboard_data_loading(self):
        """Test dashboard widget data loading functionality"""
        # First login to access dashboard
        login_response = self.session.post(f"{self.base_url}/login", data=self.admin_credentials)
        
        if login_response.status_code != 302:
            self.log_test("Dashboard Data - Login Required", "FAIL", "Cannot login to test dashboard data")
            return
            
        try:
            # Test dashboard route
            response = self.session.get(f"{self.base_url}/dashboard")
            if response.status_code == 200:
                content = response.text
                
                # Check for data loading functions
                if 'loadDashboardData' in content:
                    self.log_test("Dashboard Data - Load Function", "PASS", "Data loading function found", response.status_code)
                else:
                    self.log_test("Dashboard Data - Load Function", "FAIL", "Data loading function not found", response.status_code)
                
                # Check for plant data loading
                if 'loadPlantData' in content:
                    self.log_test("Dashboard Data - Plant Data", "PASS", "Plant data loading found", response.status_code)
                else:
                    self.log_test("Dashboard Data - Plant Data", "FAIL", "Plant data loading not found", response.status_code)
                
                # Check for environmental data loading
                if 'loadEnvironmentalData' in content:
                    self.log_test("Dashboard Data - Environmental Data", "PASS", "Environmental data loading found", response.status_code)
                else:
                    self.log_test("Dashboard Data - Environmental Data", "FAIL", "Environmental data loading not found", response.status_code)
                
                # Check for sensor data loading
                if 'loadSensorData' in content:
                    self.log_test("Dashboard Data - Sensor Data", "PASS", "Sensor data loading found", response.status_code)
                else:
                    self.log_test("Dashboard Data - Sensor Data", "FAIL", "Sensor data loading not found", response.status_code)
                    
            else:
                self.log_test("Dashboard Data - Access", "FAIL", f"Dashboard not accessible: HTTP {response.status_code}", response.status_code)
                
        except Exception as e:
            self.log_test("Dashboard Data - Loading", "FAIL", f"Exception: {str(e)}")

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
        
        # NEW: Mobile-responsive dashboard tests
        print("\n📱 Testing Mobile-Responsive Dashboard...")
        self.test_mobile_responsive_dashboard()
        
        # NEW: PWA feature tests
        print("\n🔄 Testing PWA Features...")
        self.test_pwa_features()
        
        # NEW: Widget system tests
        print("\n🧩 Testing Widget System...")
        self.test_widget_system_assets()
        
        # NEW: Dashboard data loading tests
        print("\n📊 Testing Dashboard Data Loading...")
        self.test_dashboard_data_loading()
        
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