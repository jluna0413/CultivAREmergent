#!/usr/bin/env python3
"""
Web Interface Integration Test
Tests frontend-to-FastAPI backend connectivity and API endpoint availability
"""

import asyncio
import aiohttp
import json
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:8000"  # FastAPI default port
TEST_TIMEOUT = 30

class WebAPITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = None
        self.results = []

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def test_endpoint(self, method, path, expected_status=None, description=""):
        """Test a single API endpoint"""
        url = f"{self.base_url}{path}"
        
        try:
            print(f"Testing {method.upper()} {url} - {description}")
            
            async with self.session.request(method, url, timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)) as response:
                status = response.status
                content_type = response.headers.get('content-type', '')
                
                # Try to parse JSON if available
                try:
                    data = await response.json()
                except:
                    data = await response.text()
                
                result = {
                    'method': method.upper(),
                    'path': path,
                    'url': url,
                    'status': status,
                    'content_type': content_type,
                    'description': description,
                    'success': expected_status is None or status == expected_status,
                    'response_data': data
                }
                
                if result['success']:
                    print(f"  ✅ {status} - {description}")
                else:
                    print(f"  ❌ {status} - Expected {expected_status}, got {status}")
                
                self.results.append(result)
                return result
                
        except asyncio.TimeoutError:
            result = {
                'method': method.upper(),
                'path': path,
                'url': url,
                'error': 'Timeout',
                'description': description,
                'success': False
            }
            print(f"  ⏰ Timeout - {description}")
            self.results.append(result)
            return result
            
        except Exception as e:
            result = {
                'method': method.upper(),
                'path': path,
                'url': url,
                'error': str(e),
                'description': description,
                'success': False
            }
            print(f"  ❌ Error: {e} - {description}")
            self.results.append(result)
            return result

    async def run_integration_tests(self):
        """Run comprehensive integration tests"""
        print("🚀 Web Interface Integration Test")
        print("=" * 50)
        
        # 1. Basic connectivity
        await self.test_endpoint("GET", "/", description="Root endpoint")
        await self.test_endpoint("GET", "/health", description="Health check")
        await self.test_endpoint("GET", "/docs", expected_status=200, description="API documentation")
        
        # 2. Auth endpoints (these should work without login)
        await self.test_endpoint("POST", "/api/v2/auth/login", 
                               json={"username": "test", "password": "test"}, 
                               expected_status=422,  # Validation error for bad data
                               description="Auth login endpoint (validation test)")
        
        # 3. Protected endpoints (should return 401/422 without auth)
        await self.test_endpoint("GET", "/api/v2/admin/stats", 
                               expected_status=401, 
                               description="Admin stats (unauthorized)")
        await self.test_endpoint("GET", "/api/v2/dashboard", 
                               expected_status=401, 
                               description="Dashboard (unauthorized)")
        await self.test_endpoint("GET", "/api/v2/activities/list", 
                               expected_status=401, 
                               description="Activities list (unauthorized)")
        
        # 4. API info endpoints
        await self.test_endpoint("GET", "/api/v2/status", description="API status")
        await self.test_endpoint("GET", "/api/v2/dev-info", description="Development info")
        
        # 5. Legacy API compatibility tests
        await self.test_endpoint("GET", "/api/v2/activities", description="Activities legacy endpoint")
        
        # 6. Frontend API integration tests
        await self.test_endpoint("GET", "/api/v2/admin/activities", 
                               expected_status=401, 
                               description="Admin activities (legacy compatibility)")
        
        print("\n" + "=" * 50)
        return self.results

    def generate_report(self):
        """Generate a comprehensive test report"""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.get('success', False))
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n📊 Integration Test Results")
        print("=" * 50)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.results:
                if not result.get('success', False):
                    if 'error' in result:
                        print(f"  - {result['method']} {result['path']}: {result['error']}")
                    else:
                        print(f"  - {result['method']} {result['path']}: Status {result['status']}")
        
        print(f"\n✅ Passed Tests:")
        for result in self.results:
            if result.get('success', False):
                print(f"  - {result['method']} {result['path']}: {result['status']}")
        
        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'success_rate': success_rate,
            'timestamp': datetime.now().isoformat(),
            'results': self.results
        }

async def main():
    """Main test execution"""
    print("🌐 Web Interface to FastAPI Integration Testing")
    print(f"Testing against: {BASE_URL}")
    print(f"Test timeout: {TEST_TIMEOUT} seconds")
    print()
    
    async with WebAPITester(BASE_URL) as tester:
        await tester.run_integration_tests()
        report = tester.generate_report()
    
    # Save detailed report
    with open('web_api_integration_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: web_api_integration_report.json")
    
    # Return success status
    return report['success_rate'] >= 80.0  # 80% success threshold

if __name__ == "__main__":
    success = asyncio.run(main())
    if success:
        print(f"\n🎉 Integration test PASSED!")
        exit(0)
    else:
        print(f"\n💥 Integration test FAILED!")
        exit(1)