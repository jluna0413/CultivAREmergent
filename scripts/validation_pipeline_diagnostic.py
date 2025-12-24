#!/usr/bin/env python3
"""
🔧 VALIDATION PIPELINE DIAGNOSTIC & FIX SCRIPT
Diagnoses and fixes the validation pipeline errors
"""

import os
import sys
import asyncio
import httpx
import json
from pathlib import Path
from datetime import datetime
import traceback

class ValidationPipelineDiagnostic:
    """Diagnoses and fixes validation pipeline issues"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=30.0)
        self.issues_found = []
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def diagnose_validation_pipeline(self):
        """Diagnose why validation pipeline is failing"""
        print("🔍 DIAGNOSING VALIDATION PIPELINE ERRORS")
        print(f"📍 Testing application at: {self.base_url}")
        print("-" * 60)
        
        # Test 1: Basic connectivity
        await self._test_basic_connectivity()
        
        # Test 2: Security validation
        await self._test_security_validation()
        
        # Test 3: IoT validation
        await self._test_iot_validation()
        
        # Test 4: E2E validation
        await self._test_e2e_validation()
        
        # Test 5: Authentication flow
        await self._test_authentication_flow()
        
        return {
            "diagnosis": "completed",
            "issues_found": self.issues_found,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _test_basic_connectivity(self):
        """Test basic application connectivity"""
        print("\n🔍 Testing Basic Connectivity...")
        try:
            # Test root endpoint
            response = await self.client.get(f"{self.base_url}/")
            print(f"   Root endpoint: {response.status_code}")
            
            # Test API status
            try:
                response = await self.client.get(f"{self.base_url}/api/v2/status")
                print(f"   API status endpoint: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ API is responding: {data}")
                    self.issues_found.append("basic_connectivity_working")
                else:
                    print(f"   ❌ API status failed: {response.status_code}")
                    self.issues_found.append(f"api_status_failed_{response.status_code}")
            except Exception as e:
                print(f"   ❌ API status endpoint error: {e}")
                self.issues_found.append(f"api_status_error_{str(e)}")
                
        except Exception as e:
            print(f"   ❌ Basic connectivity failed: {e}")
            self.issues_found.append(f"connectivity_error_{str(e)}")
    
    async def _test_security_validation(self):
        """Test security validation components"""
        print("\n🔐 Testing Security Validation...")
        try:
            # Test authentication endpoints
            auth_tests = [
                ("/api/v2/auth/register", "POST", {"username": "test", "email": "test@test.com", "password": "test123"}),
                ("/api/v2/auth/login", "POST", {"username": "test", "password": "test123"}),
                ("/api/v2/auth/me", "GET", None),
            ]
            
            working_security_tests = 0
            for endpoint, method, data in auth_tests:
                try:
                    if method == "GET":
                        response = await self.client.get(f"{self.base_url}{endpoint}")
                    else:
                        response = await self.client.post(f"{self.base_url}{endpoint}", json=data)
                    
                    print(f"   {endpoint}: {response.status_code}")
                    
                    # Should get 401 (unauthorized) for protected endpoints, not server errors
                    if response.status_code in [200, 201, 401, 422]:
                        working_security_tests += 1
                        print(f"     ✅ {endpoint} responding correctly")
                    else:
                        print(f"     ❌ {endpoint} unexpected status: {response.status_code}")
                        self.issues_found.append(f"security_endpoint_{endpoint}_{response.status_code}")
                        
                except Exception as e:
                    print(f"     ❌ {endpoint} error: {e}")
                    self.issues_found.append(f"security_endpoint_error_{endpoint}_{str(e)}")
            
            if working_security_tests > 0:
                print(f"   ✅ Security validation working: {working_security_tests}/{len(auth_tests)} endpoints")
                self.issues_found.append("security_validation_partial")
            else:
                print("   ❌ Security validation failing")
                self.issues_found.append("security_validation_failed")
                
        except Exception as e:
            print(f"   ❌ Security validation test failed: {e}")
            self.issues_found.append(f"security_validation_exception_{str(e)}")
    
    async def _test_iot_validation(self):
        """Test IoT validation components"""
        print("\n📡 Testing IoT Validation...")
        try:
            # Test IoT endpoints
            iot_tests = [
                "/api/v2/sensors",
                "/api/v2/sensors/discover", 
                "/api/v2/sensors/stats"
            ]
            
            working_iot_tests = 0
            for endpoint in iot_tests:
                try:
                    response = await self.client.get(f"{self.base_url}{endpoint}")
                    print(f"   {endpoint}: {response.status_code}")
                    
                    # Should get 401 (unauthorized) or 200, not server errors
                    if response.status_code in [200, 401, 422]:
                        working_iot_tests += 1
                        print(f"     ✅ {endpoint} accessible")
                    else:
                        print(f"     ❌ {endpoint} status: {response.status_code}")
                        self.issues_found.append(f"iot_endpoint_{endpoint}_{response.status_code}")
                        
                except Exception as e:
                    print(f"     ❌ {endpoint} error: {e}")
                    self.issues_found.append(f"iot_endpoint_error_{endpoint}_{str(e)}")
            
            if working_iot_tests > 0:
                print(f"   ✅ IoT validation working: {working_iot_tests}/{len(iot_tests)} endpoints")
                self.issues_found.append("iot_validation_partial")
            else:
                print("   ❌ IoT validation failing")
                self.issues_found.append("iot_validation_failed")
                
        except Exception as e:
            print(f"   ❌ IoT validation test failed: {e}")
            self.issues_found.append(f"iot_validation_exception_{str(e)}")
    
    async def _test_e2e_validation(self):
        """Test E2E validation components"""
        print("\n🔄 Testing E2E Validation...")
        try:
            # Test core application endpoints that E2E tests would use
            e2e_tests = [
                "/api/v2/dashboard",
                "/api/v2/plants",
                "/api/v2/users/me"
            ]
            
            working_e2e_tests = 0
            for endpoint in e2e_tests:
                try:
                    response = await self.client.get(f"{self.base_url}{endpoint}")
                    print(f"   {endpoint}: {response.status_code}")
                    
                    # Should get 401 (unauthorized) or 200, not server errors
                    if response.status_code in [200, 401, 422]:
                        working_e2e_tests += 1
                        print(f"     ✅ {endpoint} accessible")
                    else:
                        print(f"     ❌ {endpoint} status: {response.status_code}")
                        self.issues_found.append(f"e2e_endpoint_{endpoint}_{response.status_code}")
                        
                except Exception as e:
                    print(f"     ❌ {endpoint} error: {e}")
                    self.issues_found.append(f"e2e_endpoint_error_{endpoint}_{str(e)}")
            
            if working_e2e_tests > 0:
                print(f"   ✅ E2E validation working: {working_e2e_tests}/{len(e2e_tests)} endpoints")
                self.issues_found.append("e2e_validation_partial")
            else:
                print("   ❌ E2E validation failing")
                self.issues_found.append("e2e_validation_failed")
                
        except Exception as e:
            print(f"   ❌ E2E validation test failed: {e}")
            self.issues_found.append(f"e2e_validation_exception_{str(e)}")
    
    async def _test_authentication_flow(self):
        """Test complete authentication flow"""
        print("\n🔑 Testing Authentication Flow...")
        try:
            # Test registration
            test_user = {
                "username": f"validation_test_{int(datetime.utcnow().timestamp())}",
                "email": f"test_{int(datetime.utcnow().timestamp())}@validation.com",
                "password": "TestPassword123!"
            }
            
            try:
                register_response = await self.client.post(
                    f"{self.base_url}/api/v2/auth/register",
                    json=test_user
                )
                print(f"   Registration: {register_response.status_code}")
                
                if register_response.status_code in [200, 201, 422]:  # 422 for validation errors is OK
                    print("   ✅ Registration endpoint working")
                    self.issues_found.append("auth_registration_working")
                    
                    # Test login
                    try:
                        login_response = await self.client.post(
                            f"{self.base_url}/api/v2/auth/login",
                            json={
                                "username": test_user["username"],
                                "password": test_user["password"]
                            }
                        )
                        print(f"   Login: {login_response.status_code}")
                        
                        if login_response.status_code in [200, 401, 422]:
                            print("   ✅ Login endpoint working")
                            self.issues_found.append("auth_login_working")
                            
                            # Test protected endpoint with token
                            if login_response.status_code == 200:
                                token_data = login_response.json()
                                if "access_token" in token_data:
                                    token = token_data["access_token"]
                                    headers = {"Authorization": f"Bearer {token}"}
                                    
                                    me_response = await self.client.get(
                                        f"{self.base_url}/api/v2/auth/me",
                                        headers=headers
                                    )
                                    print(f"   Protected endpoint: {me_response.status_code}")
                                    
                                    if me_response.status_code == 200:
                                        print("   ✅ Full auth flow working")
                                        self.issues_found.append("auth_flow_complete")
                                    else:
                                        print(f"   ❌ Protected endpoint failed: {me_response.status_code}")
                                        self.issues_found.append("auth_protected_failed")
                                else:
                                    print("   ❌ No access token in response")
                                    self.issues_found.append("auth_no_token")
                        else:
                            print(f"   ❌ Login failed: {login_response.status_code}")
                            self.issues_found.append("auth_login_failed")
                            
                    except Exception as e:
                        print(f"   ❌ Login test error: {e}")
                        self.issues_found.append(f"auth_login_error_{str(e)}")
                        
                else:
                    print(f"   ❌ Registration failed: {register_response.status_code}")
                    self.issues_found.append(f"auth_registration_failed_{register_response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Registration test error: {e}")
                self.issues_found.append(f"auth_registration_error_{str(e)}")
                
        except Exception as e:
            print(f"   ❌ Authentication flow test failed: {e}")
            self.issues_found.append(f"auth_flow_exception_{str(e)}")
    
    def generate_fix_recommendations(self):
        """Generate specific fix recommendations"""
        print(f"\n🔧 GENERATING FIX RECOMMENDATIONS")
        print("-" * 60)
        
        recommendations = []
        
        # Analyze issues and generate recommendations
        if any("connectivity" in issue for issue in self.issues_found):
            recommendations.append("🌐 Connectivity Issues: Check if FastAPI server is running on port 8000")
            
        if any("security" in issue and "failed" in issue for issue in self.issues_found):
            recommendations.append("🔐 Security Issues: Review authentication endpoints and JWT configuration")
            
        if any("iot" in issue and "failed" in issue for issue in self.issues_found):
            recommendations.append("📡 IoT Issues: Check sensor API endpoints and device integration")
            
        if any("e2e" in issue and "failed" in issue for issue in self.issues_found):
            recommendations.append("🔄 E2E Issues: Verify user workflow endpoints and data models")
            
        if any("auth" in issue and "failed" in issue for issue in self.issues_found):
            recommendations.append("🔑 Auth Issues: Fix user registration, login, and token validation")
        
        # Add specific recommendations based on what's working
        if any("partial" in issue for issue in self.issues_found):
            recommendations.append("✅ Partial Success: Some endpoints working, focus on fixing failures")
        
        return recommendations

async def main():
    """Main diagnostic function"""
    print("🚀 STARTING VALIDATION PIPELINE DIAGNOSTIC")
    print(f"⏰ Started at: {datetime.utcnow().isoformat()}")
    print("=" * 70)
    
    async with ValidationPipelineDiagnostic() as diagnostic:
        # Run diagnostic
        result = await diagnostic.diagnose_validation_pipeline()
        
        # Generate recommendations
        recommendations = diagnostic.generate_fix_recommendations()
        
        # Display results
        print(f"\n📊 DIAGNOSTIC RESULTS")
        print("=" * 70)
        print(f"🔍 Issues Found: {len(diagnostic.issues_found)}")
        
        print(f"\n📋 Issues Identified:")
        for i, issue in enumerate(diagnostic.issues_found, 1):
            print(f"   {i}. {issue}")
        
        print(f"\n💡 Fix Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
        
        # Summary
        if any("working" in issue or "partial" in issue for issue in diagnostic.issues_found):
            print(f"\n🎯 SUMMARY: Application is partially functional")
            print(f"   ✅ Backend appears to be running")
            print(f"   ⚠️  Some validation components need fixing")
        else:
            print(f"\n🎯 SUMMARY: Validation pipeline needs significant fixes")
            print(f"   ❌ Multiple components failing")
            print(f"   🔧 Recommendations provided above")
        
        return result

if __name__ == "__main__":
    asyncio.run(main())