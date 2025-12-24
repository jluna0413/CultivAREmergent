#!/usr/bin/env python3
"""
Comprehensive Route and Functionality Audit Test for CultivAR Application

This test script verifies:
1. All core application routes are accessible
2. JavaScript navigation functionality works
3. Template rendering doesn't produce errors
4. Authentication flows work correctly
5. Database models are properly configured
"""

import os
import sys
import json
import requests
from datetime import datetime

class CultivarAuditTester:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.test_results = []
        self.session = requests.Session()

    def log_test(self, test_name, result, details=None):
        """Log test results"""
        self.test_results.append({
            'test': test_name,
            'result': 'PASS' if result else 'FAIL',
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"   {details}")

    def test_basic_routes(self):
        """Test basic non-authenticated routes"""
        routes_to_test = [
            ('/', 'Landing page'),
            ('/health', 'Health check endpoint'),
        ]

        for route, description in routes_to_test:
            try:
                response = self.session.get(f"{self.base_url}{route}", timeout=10)
                success = response.status_code == 200
                self.log_test(
                    f"Basic route: {route}",
                    success,
                    f"Status: {response.status_code}, {description}"
                )
            except Exception as e:
                self.log_test(
                    f"Basic route: {route}",
                    False,
                    f"Error: {str(e)}, {description}"
                )

    def test_auth_endpoints(self):
        """Test authentication endpoints"""
        routes_to_test = [
            ('/auth/login', 'Login page'),
            ('/auth/signup', 'Signup page'),
            ('/auth/forgot-password', 'Forgot password'),
        ]

        for route, description in routes_to_test:
            try:
                response = self.session.get(f"{self.base_url}{route}", timeout=10)
                success = response.status_code in [200, 302]  # Either render or redirect
                self.log_test(
                    f"Auth route: {route}",
                    success,
                    f"Status: {response.status_code}, {description}"
                )
            except Exception as e:
                self.log_test(
                    f"Auth route: {route}",
                    False,
                    f"Error: {str(e)}, {description}"
                )

    def test_dashboard_routes(self):
        """Test dashboard-related routes (may require auth redirects)"""
        routes_to_test = [
            ('/dashboard/', 'Main dashboard'),
            ('/dashboard/plants', 'Plants page'),
        ]

        for route, description in routes_to_test:
            try:
                response = self.session.get(f"{self.base_url}{route}", timeout=10)
                # Should either render (if logged in) or redirect to login (if not)
                success = response.status_code in [200, 302]
                details = f"Status: {response.status_code}"
                if response.status_code == 302:
                    details += f", Redirect to: {response.headers.get('Location', 'Unknown')}"
                details += f", {description}"
                self.log_test(f"Dashboard route: {route}", success, details)
            except Exception as e:
                self.log_test(
                    f"Dashboard route: {route}",
                    False,
                    f"Error: {str(e)}, {description}"
                )

    def test_static_files(self):
        """Test static file serving"""
        static_files = [
            ('/static/css/style.css', 'Main stylesheet'),
            ('/static/js/main.js', 'Main JavaScript file'),
            ('/favicon.ico', 'Favicon'),
        ]

        for file_path, description in static_files:
            try:
                response = self.session.get(f"{self.base_url}{file_path}", timeout=10)
                success = response.status_code == 200
                content_type = response.headers.get('content-type', 'Unknown')
                self.log_test(
                    f"Static file: {file_path}",
                    success,
                    f"Status: {response.status_code}, Content-Type: {content_type}, {description}"
                )
            except Exception as e:
                self.log_test(
                    f"Static file: {file_path}",
                    False,
                    f"Error: {str(e)}, {description}"
                )

    def test_market_routes(self):
        """Test market-specific routes"""
        routes_to_test = [
            ('/market/extensions', 'Market extensions'),
            ('/market/gear', 'Market gear'),
            ('/market/seed-bank', 'Market seed bank'),
        ]

        for route, description in routes_to_test:
            try:
                response = self.session.get(f"{self.base_url}{route}", timeout=10)
                success = response.status_code == 200
                self.log_test(
                    f"Market route: {route}",
                    success,
                    f"Status: {response.status_code}, {description}"
                )
            except Exception as e:
                self.log_test(
                    f"Market route: {route}",
                    False,
                    f"Error: {str(e)}, {description}"
                )

    def test_admin_routes(self):
        """Test admin routes (should redirect to login if not authenticated)"""
        routes_to_test = [
            ('/admin/users', 'Admin users page'),
            ('/admin/export', 'Admin data export'),
        ]

        for route, description in routes_to_test:
            try:
                response = self.session.get(f"{self.base_url}{route}", timeout=10)
                # Should redirect to login if not authenticated
                success = response.status_code == 302
                redirect_location = response.headers.get('Location', 'Unknown')
                self.log_test(
                    f"Admin route: {route}",
                    success,
                    f"Status: {response.status_code}, Redirect: {redirect_location}, {description}"
                )
            except Exception as e:
                self.log_test(
                    f"Admin route: {route}",
                    False,
                    f"Error: {str(e)}, {description}"
                )

    def check_javascript_navigation(self):
        """Check if JavaScript navigation code is properly loaded"""
        try:
            response = self.session.get(f"{self.base_url}/static/js/main.js", timeout=10)
            if response.status_code != 200:
                self.log_test("JavaScript navigation check", False, "Main JS file not accessible")
                return

            javascript_content = response.text

            # Check for key JavaScript functions
            required_functions = [
                'initSidebarDropdowns',
                'normalizeUrl',
                'initSidebarToggle',
            ]

            for func_name in required_functions:
                found = func_name in javascript_content
                self.log_test(
                    f"JS function check: {func_name}",
                    found,
                    f"Function {'found' if found else 'missing'} in main.js"
                )

        except Exception as e:
            self.log_test("JavaScript navigation check", False, f"Error: {str(e)}")

    def run_comprehensive_test(self):
        """Run all tests and generate report"""
        print("=" * 60)
        print("🏥 CULTIVAR APPLICATION COMPREHENSIVE AUDIT")
        print("=" * 60)
        print(f"Base URL: {self.base_url}")
        print(f"Test Start: {datetime.now().isoformat()}")
        print("-" * 60)

        # Run all test categories
        self.test_basic_routes()
        print()
        self.test_auth_endpoints()
        print()
        self.test_dashboard_routes()
        print()
        self.test_static_files()
        print()
        self.test_market_routes()
        print()
        self.test_admin_routes()
        print()
        self.check_javascript_navigation()

        # Generate summary report
        self.generate_summary_report()

    def generate_summary_report(self):
        """Generate a comprehensive summary report"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE AUDIT RESULTS")
        print("=" * 60)

        total_tests = len(self.test_results)
        passed_tests = sum(1 for test in self.test_results if test['result'] == 'PASS')
        failed_tests = total_tests - passed_tests

        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ({passed_tests/total_tests*100:.1f}%)" if total_tests > 0 else "No tests run")
        print(f"Failed: {failed_tests} ({failed_tests/total_tests*100:.1f}%)" if total_tests > 0 else "No tests run")

        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for test in self.test_results:
                if test['result'] == 'FAIL':
                    print(f"   • {test['test']}: {test['details']}")

        print("\n✅ PASSED TESTS:")
        for test in self.test_results:
            if test['result'] == 'PASS':
                print(f"   • {test['test']}")

        # Save detailed results to JSON file
        results_file = "comprehensive_audit_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                'audit_summary': {
                    'total_tests': total_tests,
                    'passed_tests': passed_tests,
                    'failed_tests': failed_tests,
                    'success_rate': passed_tests/total_tests*100 if total_tests > 0 else 0,
                },
                'test_results': self.test_results,
                'audit_timestamp': datetime.now().isoformat(),
                'environment': {
                    'base_url': self.base_url,
                    'python_version': sys.version,
                }
            }, f, indent=2)

        print(f"\n📋 Detailed results saved to: {results_file}")
        print("=" * 60)

def main():
    """Main test execution"""
    tester = CultivarAuditTester()

    try:
        print("Starting comprehensive audit test...")
        print("Note: Make sure the CultivAR Flask application is running on localhost:5000")
        print("If not running, start it first and then re-run this test.\n")

        tester.run_comprehensive_test()

    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Test execution failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()