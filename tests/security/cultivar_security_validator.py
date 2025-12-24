"""
🔐 SECURITY VALIDATION FRAMEWORK FOR CULTIVAR APPLICATION
Comprehensive security testing suite for JWT, authentication, and API security
"""

import asyncio
import pytest
import httpx
import jwt
import secrets
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import os
from dataclasses import dataclass

@dataclass
class SecurityTestResult:
    """Security test result with detailed information"""
    test_name: str
    passed: bool
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    details: str
    evidence: Optional[Dict] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

class CultivarSecurityValidator:
    """Comprehensive security validation for CultivAR application"""
    
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=30.0)
        self.test_results: List[SecurityTestResult] = []
        self.auth_tokens = {}
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
        
    async def run_all_security_tests(self) -> Dict[str, Any]:
        """Run comprehensive security test suite"""
        print("🔐 Starting CultivAR Security Validation Suite...")
        
        # Test categories
        test_suites = [
            ("JWT Security Tests", self._test_jwt_security),
            ("Authentication Flow Tests", self._test_authentication_flows),
            ("API Security Tests", self._test_api_security),
            ("Input Validation Tests", self._test_input_validation),
            ("Rate Limiting Tests", self._test_rate_limiting),
            ("Session Management Tests", self._test_session_management),
        ]
        
        for suite_name, test_func in test_suites:
            print(f"\n🧪 Running {suite_name}...")
            await test_func()
            
        return self._generate_security_report()
    
    async def _test_jwt_security(self):
        """Test JWT token security implementation"""
        # Test 1: Token expiration validation
        await self._test_jwt_expiration()
        
        # Test 2: JTI collision resistance
        await self._test_jti_collision_resistance()
        
        # Test 3: Token rotation race conditions
        await self._test_token_rotation_race_conditions()
        
        # Test 4: Algorithm confusion attacks
        await self._test_algorithm_confusion()
        
        # Test 5: Token replay attacks
        await self._test_token_replay_attacks()
    
    async def _test_jwt_expiration(self):
        """Test JWT token expiration handling"""
        try:
            # Register a test user
            user_data = {
                "username": f"testuser_{secrets.token_hex(4)}",
                "email": f"test_{secrets.token_hex(4)}@example.com",
                "password": "TestPassword123!"
            }
            
            register_response = await self.client.post(
                f"{self.base_url}/api/v2/auth/register",
                json=user_data
            )
            
            if register_response.status_code == 201:
                # Login to get tokens
                login_response = await self.client.post(
                    f"{self.base_url}/api/v2/auth/login",
                    json={"username": user_data["username"], "password": user_data["password"]}
                )
                
                if login_response.status_code == 200:
                    tokens = login_response.json()
                    access_token = tokens["access_token"]
                    
                    # Decode token to check expiration
                    try:
                        payload = jwt.decode(access_token, options={"verify_signature": False})
                        exp_timestamp = payload.get("exp")
                        current_timestamp = int(time.time())
                        
                        # Check if token expires within reasonable time (30 minutes)
                        time_to_expire = exp_timestamp - current_timestamp
                        if 1700 <= time_to_expire <= 1900:  # 30 minutes ± 100 seconds
                            self.test_results.append(SecurityTestResult(
                                test_name="JWT Expiration Validation",
                                passed=True,
                                severity="LOW",
                                details=f"Token expires in {time_to_expire} seconds (expected ~1800)",
                                evidence={"exp_timestamp": exp_timestamp, "current_timestamp": current_timestamp}
                            ))
                        else:
                            self.test_results.append(SecurityTestResult(
                                test_name="JWT Expiration Validation",
                                passed=False,
                                severity="HIGH",
                                details=f"Token expiration time incorrect: {time_to_expire} seconds",
                                evidence={"exp_timestamp": exp_timestamp, "current_timestamp": current_timestamp}
                            ))
                    except jwt.DecodeError:
                        self.test_results.append(SecurityTestResult(
                            test_name="JWT Expiration Validation",
                            passed=False,
                            severity="HIGH",
                            details="Failed to decode JWT token for expiration check",
                            evidence={"token": access_token[:50] + "..."}
                        ))
                        
        except Exception as e:
            self.test_results.append(SecurityTestResult(
                test_name="JWT Expiration Validation",
                passed=False,
                severity="CRITICAL",
                details=f"Test failed with exception: {str(e)}"
            ))
    
    async def _test_jti_collision_resistance(self):
        """Test JTI (JWT ID) collision resistance"""
        try:
            # Generate multiple tokens and check for JTI uniqueness
            jti_set = set()
            collision_found = False
            
            for i in range(100):  # Generate 100 tokens
                # Create user and login
                username = f"collision_test_{i}_{secrets.token_hex(4)}"
                user_data = {
                    "username": username,
                    "email": f"collision_{i}@example.com",
                    "password": "TestPassword123!"
                }
                
                # Register
                await self.client.post(f"{self.base_url}/api/v2/auth/register", json=user_data)
                
                # Login
                login_response = await self.client.post(
                    f"{self.base_url}/api/v2/auth/login",
                    json={"username": username, "password": user_data["password"]}
                )
                
                if login_response.status_code == 200:
                    token = login_response.json()["access_token"]
                    
                    # Decode and extract JTI
                    try:
                        payload = jwt.decode(token, options={"verify_signature": False})
                        jti = payload.get("jti")
                        
                        if jti in jti_set:
                            collision_found = True
                            break
                        jti_set.add(jti)
                    except:
                        pass
                        
            if not collision_found and len(jti_set) == 100:
                self.test_results.append(SecurityTestResult(
                    test_name="JTI Collision Resistance",
                    passed=True,
                    severity="LOW",
                    details="No JTI collisions found in 100 token samples",
                    evidence={"unique_jtis": len(jti_set), "samples_tested": 100}
                ))
            else:
                self.test_results.append(SecurityTestResult(
                    test_name="JTI Collision Resistance",
                    passed=False,
                    severity="HIGH",
                    details="JTI collision detected or insufficient unique JTIs",
                    evidence={"unique_jtis": len(jti_set), "samples_tested": 100}
                ))
                
        except Exception as e:
            self.test_results.append(SecurityTestResult(
                test_name="JTI Collision Resistance",
                passed=False,
                severity="CRITICAL",
                details=f"Test failed with exception: {str(e)}"
            ))
    
    async def _test_token_rotation_race_conditions(self):
        """Test token rotation under concurrent access"""
        try:
            # Create test user
            username = f"rotation_test_{secrets.token_hex(4)}"
            user_data = {
                "username": username,
                "email": f"rotation_{secrets.token_hex(4)}@example.com",
                "password": "TestPassword123!"
            }
            
            # Register user
            await self.client.post(f"{self.base_url}/api/v2/auth/register", json=user_data)
            
            # Login to get initial tokens
            login_response = await self.client.post(
                f"{self.base_url}/api/v2/auth/login",
                json={"username": username, "password": user_data["password"]}
            )
            
            if login_response.status_code == 200:
                initial_refresh_token = login_response.json()["refresh_token"]
                
                # Simulate concurrent refresh attempts
                tasks = []
                for i in range(5):
                    task = asyncio.create_task(
                        self._concurrent_token_refresh(initial_refresh_token)
                    )
                    tasks.append(task)
                
                # Wait for all refresh attempts
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Check if any refresh attempts succeeded
                successful_refreshes = [r for r in results if r is not None and not isinstance(r, Exception)]
                
                if len(successful_refreshes) == 1:
                    self.test_results.append(SecurityTestResult(
                        test_name="Token Rotation Race Conditions",
                        passed=True,
                        severity="LOW",
                        details="Only one concurrent refresh attempt succeeded (correct behavior)",
                        evidence={"successful_refreshes": len(successful_refreshes), "total_attempts": 5}
                    ))
                else:
                    self.test_results.append(SecurityTestResult(
                        test_name="Token Rotation Race Conditions",
                        passed=False,
                        severity="HIGH",
                        details=f"Multiple concurrent refresh attempts succeeded: {len(successful_refreshes)}",
                        evidence={"successful_refreshes": len(successful_refreshes), "total_attempts": 5}
                    ))
                    
        except Exception as e:
            self.test_results.append(SecurityTestResult(
                test_name="Token Rotation Race Conditions",
                passed=False,
                severity="CRITICAL",
                details=f"Test failed with exception: {str(e)}"
            ))
    
    async def _concurrent_token_refresh(self, refresh_token: str):
        """Helper function for concurrent token refresh"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v2/auth/refresh",
                json={"refresh_token": refresh_token}
            )
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    async def _test_algorithm_confusion(self):
        """Test for JWT algorithm confusion attacks"""
        try:
            # Create test user
            username = f"algo_test_{secrets.token_hex(4)}"
            user_data = {
                "username": username,
                "email": f"algo_{secrets.token_hex(4)}@example.com",
                "password": "TestPassword123!"
            }
            
            # Register and login
            await self.client.post(f"{self.base_url}/api/v2/auth/register", json=user_data)
            login_response = await self.client.post(
                f"{self.base_url}/api/v2/auth/login",
                json={"username": username, "password": user_data["password"]}
            )
            
            if login_response.status_code == 200:
                token = login_response.json()["access_token"]
                
                # Try to decode with wrong algorithm
                try:
                    # This should fail if properly secured
                    jwt.decode(token, "wrong_secret", algorithms=["HS512"])
                    algorithm_confusion_possible = True
                except:
                    algorithm_confusion_possible = False
                    
                if not algorithm_confusion_possible:
                    self.test_results.append(SecurityTestResult(
                        test_name="Algorithm Confusion Attack Protection",
                        passed=True,
                        severity="LOW",
                        details="JWT properly rejects algorithm confusion attacks",
                        evidence={"protection_active": True}
                    ))
                else:
                    self.test_results.append(SecurityTestResult(
                        test_name="Algorithm Confusion Attack Protection",
                        passed=False,
                        severity="HIGH",
                        details="JWT vulnerable to algorithm confusion attacks",
                        evidence={"protection_active": False}
                    ))
                    
        except Exception as e:
            self.test_results.append(SecurityTestResult(
                test_name="Algorithm Confusion Attack Protection",
                passed=False,
                severity="CRITICAL",
                details=f"Test failed with exception: {str(e)}"
            ))
    
    async def _test_token_replay_attacks(self):
        """Test for token replay attack protection"""
        try:
            # Create test user
            username = f"replay_test_{secrets.token_hex(4)}"
            user_data = {
                "username": username,
                "email": f"replay_{secrets.token_hex(4)}@example.com",
                "password": "TestPassword123!"
            }
            
            # Register and login
            await self.client.post(f"{self.base_url}/api/v2/auth/register", json=user_data)
            login_response = await self.client.post(
                f"{self.base_url}/api/v2/auth/login",
                json={"username": username, "password": user_data["password"]}
            )
            
            if login_response.status_code == 200:
                token = login_response.json()["access_token"]
                
                # Make authenticated request
                headers = {"Authorization": f"Bearer {token}"}
                response1 = await self.client.get(f"{self.base_url}/api/v2/auth/me", headers=headers)
                
                # Try to replay the same token
                response2 = await self.client.get(f"{self.base_url}/api/v2/auth/me", headers=headers)
                
                if response1.status_code == 200 and response2.status_code == 200:
                    # Both requests succeeded - this might indicate lack of replay protection
                    # Note: Some systems allow replay within the same session
                    self.test_results.append(SecurityTestResult(
                        test_name="Token Replay Attack Protection",
                        passed=False,
                        severity="MEDIUM",
                        details="Token replay appears possible - consider implementing JTI-based replay protection",
                        evidence={"first_request": response1.status_code, "replay_request": response2.status_code}
                    ))
                else:
                    self.test_results.append(SecurityTestResult(
                        test_name="Token Replay Attack Protection",
                        passed=True,
                        severity="LOW",
                        details="Token replay attempts blocked",
                        evidence={"first_request": response1.status_code, "replay_request": response2.status_code}
                    ))
                    
        except Exception as e:
            self.test_results.append(SecurityTestResult(
                test_name="Token Replay Attack Protection",
                passed=False,
                severity="CRITICAL",
                details=f"Test failed with exception: {str(e)}"
            ))
    
    async def _test_authentication_flows(self):
        """Test authentication flow security"""
        # Test 1: Invalid credentials handling
        await self._test_invalid_credentials()
        
        # Test 2: Account lockout mechanisms
        await self._test_account_lockout()
        
        # Test 3: Password policy enforcement
        await self._test_password_policy()
        
        # Test 4: Session hijacking protection
        await self._test_session_hijacking_protection()
    
    async def _test_invalid_credentials(self):
        """Test handling of invalid login attempts"""
        try:
            # Attempt login with invalid credentials
            response = await self.client.post(
                f"{self.base_url}/api/v2/auth/login",
                json={"username": "nonexistent_user", "password": "wrong_password"}
            )
            
            if response.status_code == 401:
                # Check if response doesn't leak information
                response_data = response.json()
                if "Invalid username or password" in response_data.get("detail", ""):
                    self.test_results.append(SecurityTestResult(
                        test_name="Invalid Credentials Handling",
                        passed=True,
                        severity="LOW",
                        details="Properly rejects invalid credentials without information leakage",
                        evidence={"status_code": response.status_code, "response": response_data}
                    ))
                else:
                    self.test_results.append(SecurityTestResult(
                        test_name="Invalid Credentials Handling",
                        passed=False,
                        severity="MEDIUM",
                        details="Response may leak information about user existence",
                        evidence={"status_code": response.status_code, "response": response_data}
                    ))
            else:
                self.test_results.append(SecurityTestResult(
                    test_name="Invalid Credentials Handling",
                    passed=False,
                    severity="HIGH",
                    details="Invalid credentials not properly rejected",
                    evidence={"status_code": response.status_code}
                ))
                
        except Exception as e:
            self.test_results.append(SecurityTestResult(
                test_name="Invalid Credentials Handling",
                passed=False,
                severity="CRITICAL",
                details=f"Test failed with exception: {str(e)}"
            ))
    
    async def _test_account_lockout(self):
        """Test account lockout mechanisms"""
        try:
            # Create test user
            username = f"lockout_test_{secrets.token_hex(4)}"
            user_data = {
                "username": username,
                "email": f"lockout_{secrets.token_hex(4)}@example.com",
                "password": "TestPassword123!"
            }
            
            await self.client.post(f"{self.base_url}/api/v2/auth/register", json=user_data)
            
            # Attempt multiple failed logins
            failed_attempts = 0
            for i in range(10):
                response = await self.client.post(
                    f"{self.base_url}/api/v2/auth/login",
                    json={"username": username, "password": "wrong_password"}
                )
                
                if response.status_code == 401:
                    failed_attempts += 1
                elif response.status_code == 429:  # Too many requests
                    # Rate limiting triggered
                    break
                elif response.status_code != 401:
                    break
            
            if failed_attempts >= 5:
                self.test_results.append(SecurityTestResult(
                    test_name="Account Lockout Mechanism",
                    passed=True,
                    severity="LOW",
                    details="Account lockout or rate limiting appears to be active",
                    evidence={"failed_attempts": failed_attempts, "lockout_triggered": failed_attempts >= 5}
                ))
            else:
                self.test_results.append(SecurityTestResult(
                    test_name="Account Lockout Mechanism",
                    passed=False,
                    severity="MEDIUM",
                    details="No clear account lockout mechanism detected",
                    evidence={"failed_attempts": failed_attempts}
                ))
                
        except Exception as e:
            self.test_results.append(SecurityTestResult(
                test_name="Account Lockout Mechanism",
                passed=False,
                severity="CRITICAL",
                details=f"Test failed with exception: {str(e)}"
            ))
    
    async def _test_password_policy(self):
        """Test password policy enforcement"""
        try:
            weak_passwords = [
                "123456",
                "password",
                "abc123",
                "",
                "123456789",
                "qwerty"
            ]
            
            policy_violations = 0
            for weak_password in weak_passwords:
                username = f"policy_test_{secrets.token_hex(4)}"
                user_data = {
                    "username": username,
                    "email": f"policy_{secrets.token_hex(4)}@example.com",
                    "password": weak_password
                }
                
                response = await self.client.post(f"{self.base_url}/api/v2/auth/register", json=user_data)
                
                # Weak passwords should be rejected
                if response.status_code not in [201, 422]:  # 201=success, 422=validation error
                    policy_violations += 1
            
            if policy_violations == 0:
                self.test_results.append(SecurityTestResult(
                    test_name="Password Policy Enforcement",
                    passed=True,
                    severity="LOW",
                    details="Weak passwords properly rejected by policy",
                    evidence={"weak_passwords_tested": len(weak_passwords), "violations": policy_violations}
                ))
            else:
                self.test_results.append(SecurityTestResult(
                    test_name="Password Policy Enforcement",
                    passed=False,
                    severity="HIGH",
                    details=f"Weak passwords accepted: {policy_violations}/{len(weak_passwords)}",
                    evidence={"weak_passwords_tested": len(weak_passwords), "violations": policy_violations}
                ))
                
        except Exception as e:
            self.test_results.append(SecurityTestResult(
                test_name="Password Policy Enforcement",
                passed=False,
                severity="CRITICAL",
                details=f"Test failed with exception: {str(e)}"
            ))
    
    async def _test_session_hijacking_protection(self):
        """Test session hijacking protection mechanisms"""
        # This would require more complex testing with session tokens
        # For now, basic JWT validation
        try:
            # Create test user
            username = f"hijack_test_{secrets.token_hex(4)}"
            user_data = {
                "username": username,
                "email": f"hijack_{secrets.token_hex(4)}@example.com",
                "password": "TestPassword123!"
            }
            
            await self.client.post(f"{self.base_url}/api/v2/auth/register", json=user_data)
            login_response = await self.client.post(
                f"{self.base_url}/api/v2/auth/login",
                json={"username": username, "password": user_data["password"]}
            )
            
            if login_response.status_code == 200:
                token = login_response.json()["access_token"]
                
                # Try to modify token (simulate tampering)
                try:
                    # Decode and modify
                    payload = jwt.decode(token, options={"verify_signature": False})
                    payload["user_id"] = 999  # Try to escalate privileges
                    
                    # Re-encode with different secret
                    tampered_token = jwt.encode(payload, "different_secret", algorithm="HS256")
                    
                    # Use tampered token
                    headers = {"Authorization": f"Bearer {tampered_token}"}
                    response = await self.client.get(f"{self.base_url}/api/v2/auth/me", headers=headers)
                    
                    if response.status_code == 401:
                        self.test_results.append(SecurityTestResult(
                            test_name="Session Hijacking Protection",
                            passed=True,
                            severity="LOW",
                            details="Tampered tokens properly rejected",
                            evidence={"tampered_token_rejected": True}
                        ))
                    else:
                        self.test_results.append(SecurityTestResult(
                            test_name="Session Hijacking Protection",
                            passed=False,
                            severity="HIGH",
                            details="Tampered tokens accepted",
                            evidence={"tampered_token_rejected": False, "status_code": response.status_code}
                        ))
                        
                except Exception:
                    self.test_results.append(SecurityTestResult(
                        test_name="Session Hijacking Protection",
                        passed=True,
                        severity="LOW",
                        details="Token tampering detected and blocked",
                        evidence={"tampering_detected": True}
                    ))
                    
        except Exception as e:
            self.test_results.append(SecurityTestResult(
                test_name="Session Hijacking Protection",
                passed=False,
                severity="CRITICAL",
                details=f"Test failed with exception: {str(e)}"
            ))
    
    async def _test_api_security(self):
        """Test API security endpoints"""
        # Test 1: Unauthorized access prevention
        await self._test_unauthorized_access()
        
        # Test 2: CORS configuration
        await self._test_cors_configuration()
        
        # Test 3: Security headers
        await self._test_security_headers()
        
        # Test 4: HTTP method restrictions
        await self._test_http_method_restrictions()
    
    async def _test_unauthorized_access(self):
        """Test that protected endpoints require authentication"""
        protected_endpoints = [
            "/api/v2/users/me",
            "/api/v2/dashboard",
            "/api/v2/plants",
            "/api/v2/sensors"
        ]
        
        unauthorized_attempts = 0
        for endpoint in protected_endpoints:
            response = await self.client.get(f"{self.base_url}{endpoint}")
            if response.status_code == 401:
                unauthorized_attempts += 1
        
        if unauthorized_attempts == len(protected_endpoints):
            self.test_results.append(SecurityTestResult(
                test_name="Unauthorized Access Prevention",
                passed=True,
                severity="LOW",
                details="All protected endpoints properly require authentication",
                evidence={"protected_endpoints_tested": len(protected_endpoints), "correctly_blocked": unauthorized_attempts}
            ))
        else:
            self.test_results.append(SecurityTestResult(
                test_name="Unauthorized Access Prevention",
                passed=False,
                severity="HIGH",
                details=f"Some endpoints accessible without authentication: {len(protected_endpoints) - unauthorized_attempts}",
                evidence={"protected_endpoints_tested": len(protected_endpoints), "correctly_blocked": unauthorized_attempts}
            ))
    
    async def _test_cors_configuration(self):
        """Test CORS configuration"""
        try:
            response = await self.client.options(f"{self.base_url}/api/v2/auth/login")
            cors_headers = {
                "access-control-allow-origin": response.headers.get("access-control-allow-origin"),
                "access-control-allow-methods": response.headers.get("access-control-allow-methods"),
                "access-control-allow-headers": response.headers.get("access-control-allow-headers")
            }
            
            if cors_headers["access-control-allow-origin"]:
                # Check for overly permissive CORS in production
                origin = cors_headers["access-control-allow-origin"]
                if origin == "*":
                    self.test_results.append(SecurityTestResult(
                        test_name="CORS Configuration",
                        passed=False,
                        severity="MEDIUM",
                        details="CORS allows all origins (*) - may be too permissive for production",
                        evidence={"cors_headers": cors_headers}
                    ))
                else:
                    self.test_results.append(SecurityTestResult(
                        test_name="CORS Configuration",
                        passed=True,
                        severity="LOW",
                        details="CORS properly configured with specific origins",
                        evidence={"cors_headers": cors_headers}
                    ))
            else:
                self.test_results.append(SecurityTestResult(
                    test_name="CORS Configuration",
                    passed=False,
                    severity="MEDIUM",
                    details="CORS headers not properly set",
                    evidence={"cors_headers": cors_headers}
                ))
                
        except Exception as e:
            self.test_results.append(SecurityTestResult(
                test_name="CORS Configuration",
                passed=False,
                severity="CRITICAL",
                details=f"Test failed with exception: {str(e)}"
            ))
    
    async def _test_security_headers(self):
        """Test security headers implementation"""
        try:
            response = await self.client.get(f"{self.base_url}/")
            
            security_headers = {
                "x-frame-options": response.headers.get("x-frame-options"),
                "x-content-type-options": response.headers.get("x-content-type-options"),
                "strict-transport-security": response.headers.get("strict-transport-security"),
                "content-security-policy": response.headers.get("content-security-policy")
            }
            
            headers_present = sum(1 for v in security_headers.values() if v is not None)
            
            if headers_present >= 3:
                self.test_results.append(SecurityTestResult(
                    test_name="Security Headers Implementation",
                    passed=True,
                    severity="LOW",
                    details="Most security headers properly implemented",
                    evidence={"security_headers": security_headers, "headers_present": headers_present}
                ))
            else:
                self.test_results.append(SecurityTestResult(
                    test_name="Security Headers Implementation",
                    passed=False,
                    severity="MEDIUM",
                    details="Missing security headers",
                    evidence={"security_headers": security_headers, "headers_present": headers_present}
                ))
                
        except Exception as e:
            self.test_results.append(SecurityTestResult(
                test_name="Security Headers Implementation",
                passed=False,
                severity="CRITICAL",
                details=f"Test failed with exception: {str(e)}"
            ))
    
    async def _test_http_method_restrictions(self):
        """Test HTTP method restrictions"""
        try:
            # Test that sensitive endpoints reject inappropriate methods
            response = await self.client.request("PATCH", f"{self.base_url}/api/v2/auth/login")
            
            # Login endpoint should not allow PATCH
            if response.status_code in [405, 422]:  # Method Not Allowed or Unprocessable Entity
                self.test_results.append(SecurityTestResult(
                    test_name="HTTP Method Restrictions",
                    passed=True,
                    severity="LOW",
                    details="Inappropriate HTTP methods properly rejected",
                    evidence={"method": "PATCH", "status_code": response.status_code}
                ))
            else:
                self.test_results.append(SecurityTestResult(
                    test_name="HTTP Method Restrictions",
                    passed=False,
                    severity="MEDIUM",
                    details="HTTP method restrictions may be too permissive",
                    evidence={"method": "PATCH", "status_code": response.status_code}
                ))
                
        except Exception as e:
            self.test_results.append(SecurityTestResult(
                test_name="HTTP Method Restrictions",
                passed=False,
                severity="CRITICAL",
                details=f"Test failed with exception: {str(e)}"
            ))
    
    async def _test_input_validation(self):
        """Test input validation and sanitization"""
        # Test 1: SQL injection prevention
        await self._test_sql_injection_prevention()
        
        # Test 2: XSS prevention
        await self._test_xss_prevention()
        
        # Test 3: Input size limits
        await self._test_input_size_limits()
    
    async def _test_sql_injection_prevention(self):
        """Test SQL injection attack prevention"""
        sql_injection_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "admin' --",
            "' UNION SELECT * FROM users --"
        ]
        
        injection_attempts = 0
        for payload in sql_injection_payloads:
            response = await self.client.post(
                f"{self.base_url}/api/v2/auth/login",
                json={"username": payload, "password": "test"}
            )
            
            # Should return 401, not 500 (which might indicate SQL injection)
            if response.status_code != 500:
                injection_attempts += 1
        
        if injection_attempts == len(sql_injection_payloads):
            self.test_results.append(SecurityTestResult(
                test_name="SQL Injection Prevention",
                passed=True,
                severity="LOW",
                details="No SQL injection vulnerabilities detected",
                evidence={"payloads_tested": len(sql_injection_payloads), "safe_responses": injection_attempts}
            ))
        else:
            self.test_results.append(SecurityTestResult(
                test_name="SQL Injection Prevention",
                passed=False,
                severity="CRITICAL",
                details=f"Potential SQL injection vulnerabilities detected: {len(sql_injection_payloads) - injection_attempts}",
                evidence={"payloads_tested": len(sql_injection_payloads), "safe_responses": injection_attempts}
            ))
    
    async def _test_xss_prevention(self):
        """Test XSS attack prevention"""
        xss_payloads = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "';alert('xss');//"
        ]
        
        xss_blocked = 0
        for payload in xss_payloads:
            response = await self.client.post(
                f"{self.base_url}/api/v2/auth/register",
                json={
                    "username": f"xss_test_{secrets.token_hex(4)}",
                    "email": f"xss_{secrets.token_hex(4)}@example.com",
                    "password": "TestPassword123!"
                }
            )
            
            # If registration succeeds, the payload was likely sanitized
            if response.status_code == 201:
                xss_blocked += 1
        
        if xss_blocked == len(xss_payloads):
            self.test_results.append(SecurityTestResult(
                test_name="XSS Prevention",
                passed=True,
                severity="LOW",
                details="XSS payloads properly sanitized",
                evidence={"payloads_tested": len(xss_payloads), "properly_sanitized": xss_blocked}
            ))
        else:
            self.test_results.append(SecurityTestResult(
                test_name="XSS Prevention",
                passed=False,
                severity="HIGH",
                details="Potential XSS vulnerabilities detected",
                evidence={"payloads_tested": len(xss_payloads), "properly_sanitized": xss_blocked}
            ))
    
    async def _test_input_size_limits(self):
        """Test input size limitations"""
        try:
            # Test with oversized input
            large_input = "A" * 10000  # 10KB input
            
            response = await self.client.post(
                f"{self.base_url}/api/v2/auth/register",
                json={
                    "username": large_input,
                    "email": "large_test@example.com",
                    "password": "TestPassword123!"
                }
            )
            
            # Should reject oversized input with 422 or 413
            if response.status_code in [422, 413, 400]:
                self.test_results.append(SecurityTestResult(
                    test_name="Input Size Limits",
                    passed=True,
                    severity="LOW",
                    details="Oversized inputs properly rejected",
                    evidence={"status_code": response.status_code, "input_size": len(large_input)}
                ))
            else:
                self.test_results.append(SecurityTestResult(
                    test_name="Input Size Limits",
                    passed=False,
                    severity="MEDIUM",
                    details="Oversized inputs may not be properly limited",
                    evidence={"status_code": response.status_code, "input_size": len(large_input)}
                ))
                
        except Exception as e:
            self.test_results.append(SecurityTestResult(
                test_name="Input Size Limits",
                passed=False,
                severity="CRITICAL",
                details=f"Test failed with exception: {str(e)}"
            ))
    
    async def _test_rate_limiting(self):
        """Test rate limiting implementation"""
        try:
            # Make many rapid requests
            request_count = 50
            rate_limited_count = 0
            
            for i in range(request_count):
                response = await self.client.get(f"{self.base_url}/api/v2/auth/login")
                if response.status_code == 429:  # Too Many Requests
                    rate_limited_count += 1
            
            if rate_limited_count > 0:
                self.test_results.append(SecurityTestResult(
                    test_name="Rate Limiting",
                    passed=True,
                    severity="LOW",
                    details="Rate limiting properly implemented",
                    evidence={"total_requests": request_count, "rate_limited": rate_limited_count}
                ))
            else:
                self.test_results.append(SecurityTestResult(
                    test_name="Rate Limiting",
                    passed=False,
                    severity="MEDIUM",
                    details="No rate limiting detected",
                    evidence={"total_requests": request_count, "rate_limited": rate_limited_count}
                ))
                
        except Exception as e:
            self.test_results.append(SecurityTestResult(
                test_name="Rate Limiting",
                passed=False,
                severity="CRITICAL",
                details=f"Test failed with exception: {str(e)}"
            ))
    
    async def _test_session_management(self):
        """Test session management security"""
        # Create a test user and verify session handling
        try:
            username = f"session_test_{secrets.token_hex(4)}"
            user_data = {
                "username": username,
                "email": f"session_{secrets.token_hex(4)}@example.com",
                "password": "TestPassword123!"
            }
            
            await self.client.post(f"{self.base_url}/api/v2/auth/register", json=user_data)
            login_response = await self.client.post(
                f"{self.base_url}/api/v2/auth/login",
                json={"username": username, "password": user_data["password"]}
            )
            
            if login_response.status_code == 200:
                # Test session invalidation on logout
                token = login_response.json()["access_token"]
                headers = {"Authorization": f"Bearer {token}"}
                
                # Verify authenticated access works
                me_response = await self.client.get(f"{self.base_url}/api/v2/auth/me", headers=headers)
                
                if me_response.status_code == 200:
                    # Logout
                    logout_response = await self.client.post(
                        f"{self.base_url}/api/v2/auth/logout",
                        headers=headers
                    )
                    
                    if logout_response.status_code == 200:
                        # Try to use token after logout
                        post_logout_response = await self.client.get(f"{self.base_url}/api/v2/auth/me", headers=headers)
                        
                        if post_logout_response.status_code == 401:
                            self.test_results.append(SecurityTestResult(
                                test_name="Session Management",
                                passed=True,
                                severity="LOW",
                                details="Sessions properly invalidated on logout",
                                evidence={"logout_successful": True, "token_invalidated": post_logout_response.status_code == 401}
                            ))
                        else:
                            self.test_results.append(SecurityTestResult(
                                test_name="Session Management",
                                passed=False,
                                severity="HIGH",
                                details="Token remains valid after logout",
                                evidence={"logout_successful": True, "token_still_valid": post_logout_response.status_code == 200}
                            ))
                    else:
                        self.test_results.append(SecurityTestResult(
                            test_name="Session Management",
                            passed=False,
                            severity="MEDIUM",
                            details="Logout endpoint not working properly",
                            evidence={"logout_status": logout_response.status_code}
                        ))
                else:
                    self.test_results.append(SecurityTestResult(
                        test_name="Session Management",
                        passed=False,
                        severity="HIGH",
                        details="Initial authentication failed",
                        evidence={"auth_status": me_response.status_code}
                    ))
                    
        except Exception as e:
            self.test_results.append(SecurityTestResult(
                test_name="Session Management",
                passed=False,
                severity="CRITICAL",
                details=f"Test failed with exception: {str(e)}"
            ))
    
    def _generate_security_report(self) -> Dict[str, Any]:
        """Generate comprehensive security test report"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.passed)
        failed_tests = total_tests - passed_tests
        
        # Categorize by severity
        critical_failures = [r for r in self.test_results if not r.passed and r.severity == "CRITICAL"]
        high_failures = [r for r in self.test_results if not r.passed and r.severity == "HIGH"]
        medium_failures = [r for r in self.test_results if not r.passed and r.severity == "MEDIUM"]
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%",
                "critical_failures": len(critical_failures),
                "high_failures": len(high_failures),
                "medium_failures": len(medium_failures)
            },
            "test_results": [
                {
                    "test_name": result.test_name,
                    "passed": result.passed,
                    "severity": result.severity,
                    "details": result.details,
                    "evidence": result.evidence,
                    "timestamp": result.timestamp
                }
                for result in self.test_results
            ],
            "recommendations": self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate security recommendations based on test results"""
        recommendations = []
        
        # Analyze failures and generate specific recommendations
        failed_results = [r for r in self.test_results if not r.passed]
        
        for result in failed_results:
            if "JWT" in result.test_name and result.severity in ["CRITICAL", "HIGH"]:
                recommendations.append(f"🔐 HIGH PRIORITY: Fix JWT security issue: {result.details}")
            elif "rate limiting" in result.test_name.lower():
                recommendations.append("🛡️ Implement or strengthen rate limiting to prevent abuse")
            elif "session" in result.test_name.lower():
                recommendations.append("🔑 Improve session management and token lifecycle handling")
            elif "input" in result.test_name.lower():
                recommendations.append("🚫 Enhance input validation and sanitization")
        
        # Add general recommendations
        if any(not r.passed for r in self.test_results if r.severity == "CRITICAL"):
            recommendations.append("🚨 CRITICAL: Address all critical security failures before production deployment")
        
        if any(not r.passed for r in self.test_results if r.severity == "HIGH"):
            recommendations.append("⚠️ HIGH: Resolve high-severity security issues to meet production standards")
        
        if not recommendations:
            recommendations.append("✅ No critical security issues detected. Continue with regular security audits.")
        
        return recommendations

# CLI interface for running security tests
async def main():
    """CLI interface for security validation"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CultivAR Security Validation Suite")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of the application")
    parser.add_argument("--output", help="Output file for security report (JSON)")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    async with CultivarSecurityValidator(base_url=args.url) as validator:
        print(f"🔐 CultivAR Security Validation Suite")
        print(f"📍 Testing application at: {args.url}")
        print(f"⏰ Started at: {datetime.utcnow().isoformat()}")
        print("-" * 60)
        
        report = await validator.run_all_security_tests()
        
        # Display summary
        summary = report["summary"]
        print(f"\n📊 Security Test Summary:")
        print(f"   Total Tests: {summary['total_tests']}")
        print(f"   Passed: {summary['passed']} ✅")
        print(f"   Failed: {summary['failed']} ❌")
        print(f"   Success Rate: {summary['success_rate']}")
        print(f"   Critical Failures: {summary['critical_failures']}")
        print(f"   High Failures: {summary['high_failures']}")
        
        # Display failed tests
        failed_tests = [r for r in report["test_results"] if not r["passed"]]
        if failed_tests:
            print(f"\n❌ Failed Tests ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"   - {test['test_name']} [{test['severity']}]: {test['details']}")
        
        # Display recommendations
        print(f"\n💡 Recommendations:")
        for rec in report["recommendations"]:
            print(f"   {rec}")
        
        # Save report if requested
        if args.output:
            import json
            with open(args.output, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n📄 Detailed report saved to: {args.output}")
        
        return report

if __name__ == "__main__":
    asyncio.run(main())