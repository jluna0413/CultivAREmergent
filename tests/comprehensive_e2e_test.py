#!/usr/bin/env python3
"""
Comprehensive End-to-End Testing for CultivAR FastAPI System
This script tests the complete system workflow from user registration to data operations
"""

import asyncio
import aiohttp
import json
import uuid
from datetime import datetime
from urllib.parse import urljoin
from typing import Dict, List, Any, Optional

class ComprehensiveE2ETester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
        self.test_user = {
            'username': f'testuser_{uuid.uuid4().hex[:8]}',
            'email': f'test_{uuid.uuid4().hex[:8]}@example.com',
            'password': 'TestPassword123!'
        }
        self.auth_token = None
        self.test_results = {
            'timestamp': datetime.now().isoformat(),
            'test_user': self.test_user,
            'test_scenarios': {},
            'overall_status': 'unknown',
            'critical_issues': [],
            'recommendations': []
        }

    async def __aenter__(self):
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=10)
        self.session = aiohttp.ClientSession(connector=connector)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def test_health_endpoints(self) -> Dict[str, Any]:
        """Test all health and status endpoints"""
        print("🏥 Testing Health Endpoints...")
        
        health_endpoints = [
            ('/', 'Root'),
            ('/health', 'Health Check'),
            ('/api/v2/status', 'API Status'),
            ('/docs', 'API Documentation')
        ]
        
        health_results = []
        for endpoint, name in health_endpoints:
            try:
                async with self.session.get(urljoin(self.base_url, endpoint)) as response:
                    if response.status == 200:
                        try:
                            data = await response.json()
                            health_results.append({
                                'endpoint': endpoint,
                                'name': name,
                                'status': 'healthy',
                                'response_time': response.headers.get('X-API-Version', 'N/A'),
                                'data': data
                            })
                        except:
                            health_results.append({
                                'endpoint': endpoint,
                                'name': name,
                                'status': 'healthy',
                                'response_time': 'N/A',
                                'data': 'Non-JSON response'
                            })
                    else:
                        health_results.append({
                            'endpoint': endpoint,
                            'name': name,
                            'status': 'failed',
                            'error': f'HTTP {response.status}'
                        })
            except Exception as e:
                health_results.append({
                    'endpoint': endpoint,
                    'name': name,
                    'status': 'error',
                    'error': str(e)
                })
        
        healthy_count = sum(1 for r in health_results if r['status'] == 'healthy')
        return {
            'total_endpoints': len(health_endpoints),
            'healthy_endpoints': healthy_count,
            'health_rate': (healthy_count / len(health_endpoints)) * 100,
            'results': health_results
        }

    async def test_user_registration(self) -> Dict[str, Any]:
        """Test user registration process"""
        print("👤 Testing User Registration...")
        
        try:
            async with self.session.post(
                urljoin(self.base_url, '/api/v2/auth/register'),
                json=self.test_user
            ) as response:
                if response.status in [200, 201]:
                    data = await response.json()
                    return {
                        'status': 'success',
                        'user_created': True,
                        'response_data': data,
                        'username': self.test_user['username']
                    }
                else:
                    return {
                        'status': 'failed',
                        'user_created': False,
                        'error': f'HTTP {response.status}',
                        'response': await response.text()
                    }
        except Exception as e:
            return {
                'status': 'error',
                'user_created': False,
                'error': str(e)
            }

    async def test_user_login(self) -> Dict[str, Any]:
        """Test user login and token generation"""
        print("🔐 Testing User Login...")
        
        try:
            async with self.session.post(
                urljoin(self.base_url, '/api/v2/auth/login'),
                json={
                    'username': self.test_user['username'],
                    'password': self.test_user['password']
                }
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    # Extract token from response (adjust based on actual API response)
                    self.auth_token = data.get('access_token') or data.get('token') or data.get('jwt')
                    
                    return {
                        'status': 'success',
                        'login_successful': True,
                        'token_received': bool(self.auth_token),
                        'token_type': type(self.auth_token).__name__,
                        'response_data': data
                    }
                else:
                    return {
                        'status': 'failed',
                        'login_successful': False,
                        'error': f'HTTP {response.status}',
                        'response': await response.text()
                    }
        except Exception as e:
            return {
                'status': 'error',
                'login_successful': False,
                'error': str(e)
            }

    async def test_authenticated_endpoints(self) -> Dict[str, Any]:
        """Test endpoints that require authentication"""
        print("🛡️ Testing Authenticated Endpoints...")
        
        if not self.auth_token:
            return {
                'status': 'skipped',
                'reason': 'No authentication token available'
            }
        
        # Test endpoints with proper authorization
        auth_headers = {'Authorization': f'Bearer {self.auth_token}'} if self.auth_token else {}
        
        protected_endpoints = [
            ('/api/v2/dashboard', 'Dashboard'),
            ('/api/v2/users/me', 'User Profile'),
            ('/api/v2/activities/list', 'Activity List'),
            ('/api/v2/plants', 'Plants Management'),
            ('/api/v2/admin/stats', 'Admin Stats')
        ]
        
        auth_results = []
        for endpoint, name in protected_endpoints:
            try:
                async with self.session.get(
                    urljoin(self.base_url, endpoint),
                    headers=auth_headers
                ) as response:
                    # Accept 200 (success) or 401/403 (unauthorized but properly handled)
                    if response.status in [200, 401, 403]:
                        auth_results.append({
                            'endpoint': endpoint,
                            'name': name,
                            'status': 'working',
                            'response_code': response.status,
                            'authorized': response.status == 200
                        })
                    else:
                        auth_results.append({
                            'endpoint': endpoint,
                            'name': name,
                            'status': 'failed',
                            'response_code': response.status,
                            'error': 'Unexpected response code'
                        })
            except Exception as e:
                auth_results.append({
                    'endpoint': endpoint,
                    'name': name,
                    'status': 'error',
                    'error': str(e)
                })
        
        working_endpoints = sum(1 for r in auth_results if r['status'] == 'working')
        authorized_endpoints = sum(1 for r in auth_results if r.get('authorized', False))
        
        return {
            'total_endpoints': len(protected_endpoints),
            'working_endpoints': working_endpoints,
            'authorized_endpoints': authorized_endpoints,
            'authorization_rate': (authorized_endpoints / len(protected_endpoints)) * 100,
            'results': auth_results
        }

    async def test_crud_operations(self) -> Dict[str, Any]:
        """Test CRUD operations on main entities"""
        print("📊 Testing CRUD Operations...")
        
        if not self.auth_token:
            return {
                'status': 'skipped',
                'reason': 'No authentication token available'
            }
        
        auth_headers = {'Authorization': f'Bearer {self.auth_token}'}
        crud_tests = {}
        
        # Test Plants CRUD
        try:
            # Create a plant
            plant_data = {
                'name': f'Test Plant {uuid.uuid4().hex[:8]}',
                'strain': 'Test Strain',
                'start_date': datetime.now().isoformat(),
                'stage': 'vegetative'
            }
            
            async with self.session.post(
                urljoin(self.base_url, '/api/v2/plants'),
                json=plant_data,
                headers=auth_headers
            ) as response:
                create_status = response.status
                created_plant = None
                if response.status == 201:
                    try:
                        created_plant = await response.json()
                    except:
                        pass
                
                crud_tests['plants'] = {
                    'create_status': create_status,
                    'plant_created': create_status == 201,
                    'response_data': created_plant
                }
                
        except Exception as e:
            crud_tests['plants'] = {
                'create_status': 'error',
                'plant_created': False,
                'error': str(e)
            }
        
        # Test Activities CRUD
        try:
            activity_data = {
                'type': 'plant_update',
                'activity_type': 'plant',
                'title': 'Test Activity',
                'description': 'Testing CRUD operations',
                'entity_type': 'plant',
                'entity_name': plant_data['name'] if 'plant_data' in locals() else 'Test Plant'
            }
            
            async with self.session.post(
                urljoin(self.base_url, '/api/v2/activities'),
                json=activity_data,
                headers=auth_headers
            ) as response:
                activity_status = response.status
                crud_tests['activities'] = {
                    'create_status': activity_status,
                    'activity_created': activity_status in [200, 201],
                    'response_data': await response.json() if activity_status in [200, 201] else None
                }
                
        except Exception as e:
            crud_tests['activities'] = {
                'create_status': 'error',
                'activity_created': False,
                'error': str(e)
            }
        
        return crud_tests

    async def test_file_upload(self) -> Dict[str, Any]:
        """Test file upload functionality"""
        print("📁 Testing File Upload...")
        
        if not self.auth_token:
            return {
                'status': 'skipped',
                'reason': 'No authentication token available'
            }
        
        auth_headers = {'Authorization': f'Bearer {self.auth_token}'}
        
        try:
            # Create a test file
            test_content = b"This is a test file for upload testing."
            
            data = aiohttp.FormData()
            data.add_field('file', 
                         test_content, 
                         filename='test_file.txt', 
                         content_type='text/plain')
            
            async with self.session.post(
                urljoin(self.base_url, '/api/v2/files/upload'),
                data=data,
                headers=auth_headers
            ) as response:
                upload_status = response.status
                
                return {
                    'status': 'completed',
                    'upload_status': upload_status,
                    'upload_successful': upload_status in [200, 201],
                    'response_data': await response.json() if upload_status in [200, 201] else None
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'upload_successful': False,
                'error': str(e)
            }

    async def test_websocket_connection(self) -> Dict[str, Any]:
        """Test WebSocket functionality if available"""
        print("🔌 Testing WebSocket Connection...")
        
        try:
            # Note: This is a basic WebSocket test - real implementation would need proper WebSocket handling
            websocket_url = self.base_url.replace('http', 'ws') + '/api/v2/websocket'
            
            # For now, just check if the endpoint exists
            async with self.session.get(websocket_url) as response:
                if response.status in [101, 426, 400]:  # Switching protocols, upgrade required, or bad request (normal for WebSocket endpoints)
                    return {
                        'status': 'available',
                        'websocket_supported': True,
                        'response_code': response.status,
                        'message': 'WebSocket endpoint is available'
                    }
                else:
                    return {
                        'status': 'available',
                        'websocket_supported': False,
                        'response_code': response.status,
                        'message': 'WebSocket endpoint exists but may not be properly configured'
                    }
        except Exception as e:
            return {
                'status': 'error',
                'websocket_supported': False,
                'error': str(e)
            }

    async def test_error_handling(self) -> Dict[str, Any]:
        """Test error handling and validation"""
        print("❌ Testing Error Handling...")
        
        error_tests = []
        
        # Test 1: Invalid JSON
        try:
            async with self.session.post(
                urljoin(self.base_url, '/api/v2/auth/register'),
                data='invalid json',
                headers={'Content-Type': 'application/json'}
            ) as response:
                error_tests.append({
                    'test': 'Invalid JSON',
                    'status_code': response.status,
                    'properly_handled': response.status in [400, 422],
                    'error_message': await response.text() if response.status >= 400 else None
                })
        except Exception as e:
            error_tests.append({
                'test': 'Invalid JSON',
                'status_code': 'error',
                'properly_handled': False,
                'error': str(e)
            })
        
        # Test 2: SQL Injection attempt (basic)
        try:
            async with self.session.get(
                urljoin(self.base_url, '/api/v2/plants?id=1\' OR \'1\'=\'1')
            ) as response:
                error_tests.append({
                    'test': 'Basic SQL Injection',
                    'status_code': response.status,
                    'properly_handled': response.status != 200 or 'error' in (await response.text() if response.status == 200 else '').lower(),
                    'protected': response.status in [400, 422, 500]
                })
        except Exception as e:
            error_tests.append({
                'test': 'Basic SQL Injection',
                'status_code': 'error',
                'properly_handled': False,
                'error': str(e)
            })
        
        proper_error_handling = sum(1 for test in error_tests if test['properly_handled'])
        
        return {
            'total_error_tests': len(error_tests),
            'properly_handled': proper_error_handling,
            'error_handling_rate': (proper_error_handling / len(error_tests)) * 100,
            'test_results': error_tests
        }

    async def run_comprehensive_e2e_test(self) -> Dict[str, Any]:
        """Run the complete end-to-end test suite"""
        print("🚀 Starting Comprehensive End-to-End Test")
        print("=" * 60)
        print(f"Target URL: {self.base_url}")
        print(f"Test User: {self.test_user['username']}")
        print("=" * 60)
        
        # Run all test scenarios
        self.test_results['test_scenarios']['health_check'] = await self.test_health_endpoints()
        
        # Only proceed with user-dependent tests if health check passes
        if self.test_results['test_scenarios']['health_check']['health_rate'] >= 75:
            self.test_results['test_scenarios']['user_registration'] = await self.test_user_registration()
            self.test_results['test_scenarios']['user_login'] = await self.test_user_login()
            self.test_results['test_scenarios']['authenticated_endpoints'] = await self.test_authenticated_endpoints()
            self.test_results['test_scenarios']['crud_operations'] = await self.test_crud_operations()
            self.test_results['test_scenarios']['file_upload'] = await self.test_file_upload()
            self.test_results['test_scenarios']['websocket'] = await self.test_websocket_connection()
        else:
            self.test_results['critical_issues'].append("Health check failed - skipping user-dependent tests")
        
        self.test_results['test_scenarios']['error_handling'] = await self.test_error_handling()
        
        # Calculate overall status
        self.test_results['overall_status'] = self._calculate_overall_status()
        self.test_results['success_rate'] = self._calculate_success_rate()
        
        return self.test_results

    def _calculate_overall_status(self) -> str:
        """Calculate overall test status"""
        critical_systems = [
            self.test_results['test_scenarios']['health_check']['health_rate'] >= 75,
            not any('error' in str(self.test_results['test_scenarios']).lower() for scenario in self.test_results['test_scenarios'].values() if isinstance(scenario, dict))
        ]
        
        if all(critical_systems):
            return 'passed'
        elif any(critical_systems):
            return 'partial'
        else:
            return 'failed'

    def _calculate_success_rate(self) -> float:
        """Calculate overall success rate"""
        scenario_scores = []
        
        for scenario_name, result in self.test_results['test_scenarios'].items():
            if isinstance(result, dict):
                if scenario_name == 'health_check':
                    scenario_scores.append(result.get('health_rate', 0))
                elif scenario_name == 'user_registration':
                    scenario_scores.append(100 if result.get('user_created') else 0)
                elif scenario_name == 'user_login':
                    scenario_scores.append(100 if result.get('login_successful') else 0)
                elif scenario_name == 'authenticated_endpoints':
                    scenario_scores.append(result.get('authorization_rate', 0))
                elif scenario_name == 'crud_operations':
                    crud_score = 0
                    if result.get('plants', {}).get('plant_created'):
                        crud_score += 50
                    if result.get('activities', {}).get('activity_created'):
                        crud_score += 50
                    scenario_scores.append(crud_score)
                elif scenario_name == 'file_upload':
                    scenario_scores.append(100 if result.get('upload_successful') else 0)
                elif scenario_name == 'websocket':
                    scenario_scores.append(100 if result.get('websocket_supported') else 50)
                elif scenario_name == 'error_handling':
                    scenario_scores.append(result.get('error_handling_rate', 0))
        
        return sum(scenario_scores) / len(scenario_scores) if scenario_scores else 0

    def generate_e2e_report(self) -> str:
        """Generate comprehensive E2E test report"""
        status_emoji = {
            'passed': '✅',
            'partial': '⚠️',
            'failed': '❌'
        }
        
        report = f"""
🧪 CULTIVAR FASTAPI END-TO-END TEST REPORT
Generated: {self.test_results['timestamp']}
Target: {self.base_url}

{"="*60}

📊 OVERALL RESULTS:
• Test Status: {status_emoji.get(self.test_results['overall_status'], '❓')} {self.test_results['overall_status'].upper()}
• Success Rate: {self.test_results['success_rate']:.1f}%
• Test User: {self.test_results['test_user']['username']}

{"="*60}

🏥 HEALTH CHECK RESULTS:
• Health Rate: {self.test_results['test_scenarios']['health_check']['health_rate']:.1f}%
• Healthy Endpoints: {self.test_results['test_scenarios']['health_check']['healthy_endpoints']}/{self.test_results['test_scenarios']['health_check']['total_endpoints']}

{"="*60}

👤 USER MANAGEMENT:
• Registration: {'✅ Success' if self.test_results['test_scenarios']['user_registration']['user_created'] else '❌ Failed'}
• Login: {'✅ Success' if self.test_results['test_scenarios']['user_login']['login_successful'] else '❌ Failed'}
• Token Received: {'✅ Yes' if self.test_results['test_scenarios']['user_login']['token_received'] else '❌ No'}

{"="*60}

🛡️ AUTHENTICATION & AUTHORIZATION:
• Protected Endpoints Working: {self.test_results['test_scenarios']['authenticated_endpoints']['working_endpoints']}/{self.test_results['test_scenarios']['authenticated_endpoints']['total_endpoints']}
• Authorization Rate: {self.test_results['test_scenarios']['authenticated_endpoints']['authorization_rate']:.1f}%

{"="*60}

📊 CRUD OPERATIONS:
• Plant Creation: {'✅ Success' if self.test_results['test_scenarios']['crud_operations'].get('plants', {}).get('plant_created') else '❌ Failed'}
• Activity Creation: {'✅ Success' if self.test_results['test_scenarios']['crud_operations'].get('activities', {}).get('activity_created') else '❌ Failed'}

{"="*60}

📁 FILE UPLOAD:
• Status: {'✅ Success' if self.test_results['test_scenarios']['file_upload'].get('upload_successful') else '❌ Failed'}

{"="*60}

🔌 WEBSOCKET:
• Support: {'✅ Available' if self.test_results['test_scenarios']['websocket'].get('websocket_supported') else '❌ Not Available'}

{"="*60}

❌ ERROR HANDLING:
• Error Handling Rate: {self.test_results['test_scenarios']['error_handling']['error_handling_rate']:.1f}%
• Properly Handled: {self.test_results['test_scenarios']['error_handling']['properly_handled']}/{self.test_results['test_scenarios']['error_handling']['total_error_tests']}

{"="*60}

🎯 E2E CONCLUSION:
"""
        
        if self.test_results['overall_status'] == 'passed':
            report += "EXCELLENT: System passes comprehensive end-to-end testing. Ready for production deployment."
        elif self.test_results['overall_status'] == 'partial':
            report += "GOOD: System shows strong functionality with minor issues that should be addressed."
        else:
            report += "POOR: System has significant issues that must be resolved before production deployment."
        
        if self.test_results['critical_issues']:
            report += f"\n\n⚠️ CRITICAL ISSUES:\n"
            for issue in self.test_results['critical_issues']:
                report += f"• {issue}\n"
        
        return report

async def main():
    """Main E2E test execution"""
    print("🧪 CultivAR FastAPI End-to-End Testing")
    print("This test validates the complete system workflow from user registration to operations.")
    print()
    
    async with ComprehensiveE2ETester() as tester:
        # Run comprehensive E2E test
        results = await tester.run_comprehensive_e2e_test()
        
        # Generate and display report
        report = tester.generate_e2e_report()
        print(report)
        
        # Save detailed results
        with open('e2e_test_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Detailed E2E results saved to: e2e_test_results.json")
        
        # Return success status
        return results['overall_status'] == 'passed' and results['success_rate'] >= 80.0

if __name__ == "__main__":
    success = asyncio.run(main())
    if success:
        print(f"\n✅ End-to-end test PASSED!")
        exit(0)
    else:
        print(f"\n❌ End-to-end test FAILED - System needs improvements!")
        exit(1)