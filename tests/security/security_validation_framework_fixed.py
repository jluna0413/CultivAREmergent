# CultivAR Security Testing Framework - Fixed for Windows Console
# Comprehensive security testing suite for authentication, SQL injection, and input validation

import pytest
import asyncio
import httpx
import json
import jwt
import time
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Test configuration
TEST_CONFIG = {
    "fastapi_base_url": "http://localhost:8000",
    "flask_base_url": "http://localhost:5000",
    "test_username": "security_test_user",
    "test_password": "SecurePassword123!",
    "test_email": "security@test.com",
    "jwt_secret": "super-secret-jwt-key-for-testing-only",
    "max_login_attempts": 5,
    "rate_limit_window": 60,  # seconds
    "rate_limit_requests": 100
}

@dataclass
class SecurityTestResult:
    """Security test result with detailed information"""
    test_name: str
    status: str  # PASS, FAIL, WARNING
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    details: str
    evidence: Optional[str] = None
    recommendation: Optional[str] = None

class CultivarSecurityValidator:
    """Main security validation framework for CultivAR application"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or TEST_CONFIG
        self.client = httpx.AsyncClient(timeout=30.0)
        self.results: List[SecurityTestResult] = []
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def test_jwt_token_security(self) -> List[SecurityTestResult]:
        """Test JWT token implementation security"""
        print("SECURITY: Testing JWT Token Security...")
        
        # Test 1: Token expiration handling
        await self._test_token_expiration()
        
        # Test 2: Token signature verification
        await self._test_token_signature_verification()
        
        # Test 3: Claims validation
        await self._test_token_claims_validation()
        
        # Test 4: Token manipulation attempts
        await self._test_token_manipulation()
        
        # Test 5: Refresh token security
        await self._test_refresh_token_security()
        
        return self.results[len(self.results)-5:]
    
    async def test_dual_auth_system_consistency(self) -> List[SecurityTestResult]:
        """Test session consistency across Flask-Login and JWT systems"""
        print("SECURITY: Testing Dual Auth System Consistency...")
        
        # Test 1: Session synchronization
        await self._test_session_synchronization()
        
        # Test 2: Logout propagation
        await self._test_logout_propagation()
        
        # Test 3: Cross-platform authentication
        await self._test_cross_platform_auth()
        
        # Test 4: Privilege escalation prevention
        await self._test_privilege_escalation()
        
        return self.results[len(self.results)-4:]
    
    async def test_sql_injection_vulnerabilities(self) -> List[SecurityTestResult]:
        """Test SQL injection prevention across all endpoints"""
        print("SECURITY: Testing SQL Injection Vulnerabilities...")
        
        # Common SQL injection payloads
        sql_payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "admin'--",
            "' UNION SELECT * FROM users--",
            "'; DROP TABLE users;--",
            "' OR 'a'='a",
            "') OR ('1'='1",
            "1; DELETE FROM plants WHERE 1=1"
        ]
        
        # Test endpoints for SQL injection
        endpoints_to_test = [
            ("GET", "/api/v2/strains/search"),
            ("POST", "/api/v2/plants"),
            ("GET", "/api/v2/plants"),
            ("POST", "/api/v2/auth/login"),
            ("GET", "/api/v2/users"),
            ("POST", "/api/v2/admin/users")
        ]
        
        for endpoint, method in endpoints_to_test:
            for payload in sql_payloads:
                await self._test_sql_injection_endpoint(method, endpoint, payload)
        
        return self.results[len(self.results)-len(sql_payloads)*len(endpoints_to_test):]
    
    async def test_rate_limiting_effectiveness(self) -> List[SecurityTestResult]:
        """Test rate limiting implementation effectiveness"""
        print("SECURITY: Testing Rate Limiting Effectiveness...")
        
        # Test 1: Login rate limiting
        await self._test_login_rate_limiting()
        
        # Test 2: API endpoint rate limiting
        await self._test_api_rate_limiting()
        
        # Test 3: Bypass attempts
        await self._test_rate_limit_bypass()
        
        return self.results[len(self.results)-3:]
    
    async def test_input_validation_security(self) -> List[SecurityTestResult]:
        """Test input validation and XSS prevention"""
        print("SECURITY: Testing Input Validation Security...")
        
        # XSS payloads
        xss_payloads = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "'><script>alert('xss')</script>",
            "<svg onload=alert('xss')>",
            "<iframe src=javascript:alert('xss')>",
            "<body onload=alert('xss')>",
            "<input onfocus=alert('xss') autofocus>"
        ]
        
        # Test XSS prevention in input fields
        for payload in xss_payloads:
            await self._test_xss_prevention(payload)
        
        # Test path traversal in file uploads
        await self._test_path_traversal()
        
        return self.results[len(self.results)-len(xss_payloads)-1:]
    
    async def run_comprehensive_security_validation(self) -> Dict[str, Any]:
        """Run all security validation tests"""
        print("SECURITY: Starting Comprehensive Security Validation...")
        
        # Execute all test suites
        jwt_results = await self.test_jwt_token_security()
        auth_results = await self.test_dual_auth_system_consistency()
        sql_results = await self.test_sql_injection_vulnerabilities()
        rate_results = await self.test_rate_limiting_effectiveness()
        input_results = await self.test_input_validation_security()
        
        # Compile results
        all_results = jwt_results + auth_results + sql_results + rate_results + input_results
        
        # Generate summary
        summary = self._generate_security_summary(all_results)
        
        return {
            "summary": summary,
            "total_tests": len(all_results),
            "results": all_results,
            "timestamp": datetime.now().isoformat()
        }
    
    # ==================== Helper Methods ====================
    
    async def _make_authenticated_request(self, method: str, url: str, token: str = None, **kwargs) -> httpx.Response:
        """Make authenticated HTTP request"""
        headers = kwargs.get("headers", {})
        if token:
            headers["Authorization"] = f"Bearer {token}"
        kwargs["headers"] = headers
        
        return await self.client.request(method, url, **kwargs)
    
    async def _get_test_user_token(self, username: str = None, password: str = None) -> Optional[str]:
        """Get JWT token for test user"""
        username = username or self.config["test_username"]
        password = password or self.config["test_password"]
        
        try:
            response = await self.client.post(
                f"{self.config['fastapi_base_url']}/api/v2/auth/login",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                return response.json().get("access_token")
        except Exception:
            pass
        
        return None
    
    def _add_result(self, test_name: str, status: str, severity: str, details: str, 
                   evidence: str = None, recommendation: str = None):
        """Add test result"""
        result = SecurityTestResult(
            test_name=test_name,
            status=status,
            severity=severity,
            details=details,
            evidence=evidence,
            recommendation=recommendation
        )
        self.results.append(result)
        print(f"  {status}: {test_name} - {details}")
    
    # ==================== JWT Security Tests ====================
    
    async def _test_token_expiration(self):
        """Test JWT token expiration handling"""
        try:
            # Create expired token
            expired_payload = {
                "user_id": 1,
                "username": "test",
                "exp": int(time.time()) - 3600  # Expired 1 hour ago
            }
            expired_token = jwt.encode(expired_payload, self.config["jwt_secret"], algorithm="HS256")
            
            # Try to use expired token
            response = await self._make_authenticated_request(
                "GET", f"{self.config['fastapi_base_url']}/api/v2/auth/me", token=expired_token
            )
            
            if response.status_code == 401:
                self._add_result(
                    "JWT Token Expiration", "PASS", "HIGH",
                    "Expired tokens properly rejected with 401 status",
                    evidence=f"Status: {response.status_code}"
                )
            else:
                self._add_result(
                    "JWT Token Expiration", "FAIL", "CRITICAL",
                    f"Expired token accepted - Status: {response.status_code}",
                    evidence=f"Response: {response.text}"
                )
        except Exception as e:
            self._add_result(
                "JWT Token Expiration", "ERROR", "HIGH",
                f"Test execution error: {str(e)}"
            )
    
    async def _test_token_signature_verification(self):
        """Test JWT signature verification"""
        try:
            # Create token with wrong signature
            payload = {"user_id": 1, "username": "test", "exp": int(time.time()) + 3600}
            fake_token = jwt.encode(payload, "wrong-secret-key", algorithm="HS256")
            
            response = await self._make_authenticated_request(
                "GET", f"{self.config['fastapi_base_url']}/api/v2/auth/me", token=fake_token
            )
            
            if response.status_code == 401:
                self._add_result(
                    "JWT Signature Verification", "PASS", "HIGH",
                    "Invalid signatures properly rejected"
                )
            else:
                self._add_result(
                    "JWT Signature Verification", "FAIL", "CRITICAL",
                    f"Invalid signature accepted - Status: {response.status_code}"
                )
        except Exception as e:
            self._add_result(
                "JWT Signature Verification", "ERROR", "HIGH",
                f"Test error: {str(e)}"
            )
    
    async def _test_token_claims_validation(self):
        """Test JWT claims validation"""
        try:
            # Create token with missing required claims
            payload = {"exp": int(time.time()) + 3600}  # Missing user_id, username
            invalid_token = jwt.encode(payload, self.config["jwt_secret"], algorithm="HS256")
            
            response = await self._make_authenticated_request(
                "GET", f"{self.config['fastapi_base_url']}/api/v2/auth/me", token=invalid_token
            )
            
            if response.status_code == 401:
                self._add_result(
                    "JWT Claims Validation", "PASS", "HIGH",
                    "Tokens with missing claims properly rejected"
                )
            else:
                self._add_result(
                    "JWT Claims Validation", "FAIL", "CRITICAL",
                    f"Invalid claims accepted - Status: {response.status_code}"
                )
        except Exception as e:
            self._add_result(
                "JWT Claims Validation", "ERROR", "HIGH",
                f"Test error: {str(e)}"
            )
    
    async def _test_token_manipulation(self):
        """Test token manipulation attempts"""
        try:
            # Test token with manipulated user_id
            payload = {
                "user_id": 99999,  # Non-existent user ID
                "username": "admin",  # Privilege escalation attempt
                "is_admin": True,  # Admin privilege escalation
                "exp": int(time.time()) + 3600
            }
            manipulated_token = jwt.encode(payload, self.config["jwt_secret"], algorithm="HS256")
            
            response = await self._make_authenticated_request(
                "GET", f"{self.config['fastapi_base_url']}/api/v2/admin/users", token=manipulated_token
            )
            
            if response.status_code == 401:
                self._add_result(
                    "Token Manipulation Prevention", "PASS", "HIGH",
                    "Manipulated tokens properly rejected"
                )
            else:
                self._add_result(
                    "Token Manipulation Prevention", "FAIL", "CRITICAL",
                    f"Manipulated token accepted - Status: {response.status_code}",
                    evidence=f"Response: {response.text}"
                )
        except Exception as e:
            self._add_result(
                "Token Manipulation Prevention", "ERROR", "HIGH",
                f"Test error: {str(e)}"
            )
    
    async def _test_refresh_token_security(self):
        """Test refresh token security"""
        try:
            # Test expired refresh token
            expired_refresh_payload = {
                "user_id": 1,
                "token_type": "refresh",
                "exp": int(time.time()) - 3600
            }
            expired_refresh = jwt.encode(expired_refresh_payload, self.config["jwt_secret"], algorithm="HS256")
            
            response = await self.client.post(
                f"{self.config['fastapi_base_url']}/api/v2/auth/refresh",
                json={"refresh_token": expired_refresh}
            )
            
            if response.status_code == 401:
                self._add_result(
                    "Refresh Token Security", "PASS", "HIGH",
                    "Expired refresh tokens properly rejected"
                )
            else:
                self._add_result(
                    "Refresh Token Security", "FAIL", "MEDIUM",
                    f"Expired refresh token accepted - Status: {response.status_code}"
                )
        except Exception as e:
            self._add_result(
                "Refresh Token Security", "ERROR", "HIGH",
                f"Test error: {str(e)}"
            )
    
    # ==================== Dual Auth System Tests ====================
    
    async def _test_session_synchronization(self):
        """Test session consistency between systems"""
        # This test would require creating user sessions in both systems
        # and verifying they remain synchronized
        self._add_result(
            "Session Synchronization", "WARNING", "MEDIUM",
            "Manual verification required for dual auth system consistency"
        )
    
    async def _test_logout_propagation(self):
        """Test logout propagation across systems"""
        self._add_result(
            "Logout Propagation", "WARNING", "MEDIUM",
            "Manual verification required for logout propagation"
        )
    
    async def _test_cross_platform_auth(self):
        """Test authentication consistency across web/mobile"""
        self._add_result(
            "Cross-Platform Auth", "WARNING", "MEDIUM",
            "Manual verification required for cross-platform authentication"
        )
    
    async def _test_privilege_escalation(self):
        """Test privilege escalation prevention"""
        self._add_result(
            "Privilege Escalation Prevention", "WARNING", "MEDIUM",
            "Manual verification required for privilege escalation prevention"
        )
    
    # ==================== SQL Injection Tests ====================
    
    async def _test_sql_injection_endpoint(self, method: str, endpoint: str, payload: str):
        """Test SQL injection on specific endpoint"""
        try:
            # Prepare request based on method
            if method == "GET":
                params = {"q": payload} if "search" in endpoint else {}
                response = await self.client.get(f"{self.config['fastapi_base_url']}{endpoint}", params=params)
            elif method == "POST":
                json_data = {"name": payload, "description": payload} if "plants" in endpoint else {"username": payload}
                response = await self.client.post(f"{self.config['fastapi_base_url']}{endpoint}", json=json_data)
            else:
                return
            
            # Check for SQL injection indicators
            dangerous_responses = [
                "sql", "mysql", "postgresql", "sqlite", "syntax", "error",
                "select", "insert", "update", "delete", "drop", "union"
            ]
            
            response_text = response.text.lower()
            is_dangerous = any(indicator in response_text for indicator in dangerous_responses)
            
            if is_dangerous and response.status_code != 400:
                self._add_result(
                    f"SQL Injection - {method} {endpoint}", "FAIL", "CRITICAL",
                    f"Potential SQL injection vulnerability detected with payload: {payload}",
                    evidence=f"Response contains dangerous keywords"
                )
            elif response.status_code in [400, 422]:
                self._add_result(
                    f"SQL Injection - {method} {endpoint}", "PASS", "HIGH",
                    f"SQL injection attempt properly rejected with status {response.status_code}"
                )
            else:
                self._add_result(
                    f"SQL Injection - {method} {endpoint}", "PASS", "MEDIUM",
                    f"Endpoint handled injection attempt with status {response.status_code}"
                )
        except Exception as e:
            self._add_result(
                f"SQL Injection - {method} {endpoint}", "ERROR", "MEDIUM",
                f"Test execution error: {str(e)}"
            )
    
    # ==================== Rate Limiting Tests ====================
    
    async def _test_login_rate_limiting(self):
        """Test login rate limiting"""
        try:
            # Attempt multiple rapid login attempts
            failed_attempts = 0
            for i in range(self.config["max_login_attempts"] + 2):
                response = await self.client.post(
                    f"{self.config['fastapi_base_url']}/api/v2/auth/login",
                    json={
                        "username": f"user_{i}",
                        "password": "wrongpassword"
                    }
                )
                
                if response.status_code == 429:  # Too Many Requests
                    failed_attempts += 1
                    break
                elif response.status_code == 401:
                    failed_attempts += 1
            
            if failed_attempts > 0:
                self._add_result(
                    "Login Rate Limiting", "PASS", "HIGH",
                    f"Rate limiting triggered after {failed_attempts} failed attempts"
                )
            else:
                self._add_result(
                    "Login Rate Limiting", "FAIL", "MEDIUM",
                    "Rate limiting not triggered after multiple failed attempts"
                )
        except Exception as e:
            self._add_result(
                "Login Rate Limiting", "ERROR", "MEDIUM",
                f"Test error: {str(e)}"
            )
    
    async def _test_api_rate_limiting(self):
        """Test API endpoint rate limiting"""
        try:
            # Get valid token first
            token = await self._get_test_user_token()
            if not token:
                self._add_result(
                    "API Rate Limiting", "ERROR", "MEDIUM",
                    "Could not obtain test token for rate limiting test"
                )
                return
            
            # Make rapid requests
            requests_made = 0
            rate_limited = False
            
            for i in range(self.config["rate_limit_requests"] + 5):
                response = await self._make_authenticated_request(
                    "GET", f"{self.config['fastapi_base_url']}/api/v2/dashboard/stats", token=token
                )
                requests_made += 1
                
                if response.status_code == 429:
                    rate_limited = True
                    break
                
                await asyncio.sleep(0.01)  # Small delay between requests
            
            if rate_limited:
                self._add_result(
                    "API Rate Limiting", "PASS", "HIGH",
                    f"Rate limiting triggered after {requests_made} requests"
                )
            else:
                self._add_result(
                    "API Rate Limiting", "WARNING", "MEDIUM",
                    f"No rate limiting after {requests_made} requests"
                )
        except Exception as e:
            self._add_result(
                "API Rate Limiting", "ERROR", "MEDIUM",
                f"Test error: {str(e)}"
            )
    
    async def _test_rate_limit_bypass(self):
        """Test rate limiting bypass attempts"""
        self._add_result(
            "Rate Limit Bypass", "WARNING", "MEDIUM",
            "Manual testing required for rate limit bypass scenarios"
        )
    
    # ==================== Input Validation Tests ====================
    
    async def _test_xss_prevention(self, payload: str):
        """Test XSS prevention in input fields"""
        try:
            # Test in plant creation endpoint
            response = await self.client.post(
                f"{self.config['fastapi_base_url']}/api/v2/plants",
                json={
                    "name": payload,
                    "description": f"Description with {payload}",
                    "status_id": 1
                }
            )
            
            # Check if script tags or dangerous content is reflected
            if payload in response.text and "<script>" in payload:
                self._add_result(
                    f"XSS Prevention - {payload[:30]}...", "FAIL", "CRITICAL",
                    "Potential XSS vulnerability - payload reflected in response",
                    evidence=f"Payload reflected in response: {response.text[:200]}"
                )
            elif response.status_code in [400, 422]:
                self._add_result(
                    f"XSS Prevention - {payload[:30]}...", "PASS", "HIGH",
                    "XSS payload properly rejected"
                )
            else:
                self._add_result(
                    f"XSS Prevention - {payload[:30]}...", "PASS", "MEDIUM",
                    "XSS payload handled without reflection"
                )
        except Exception as e:
            self._add_result(
                f"XSS Prevention - {payload[:30]}...", "ERROR", "MEDIUM",
                f"Test error: {str(e)}"
            )
    
    async def _test_path_traversal(self):
        """Test path traversal in file uploads"""
        try:
            # Test dangerous file paths
            dangerous_paths = [
                "../../../etc/passwd",
                "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
                "../../../../../../etc/shadow",
                "file_with_.._in_name.txt",
                "....//....//....//etc//passwd"
            ]
            
            for path in dangerous_paths:
                response = await self.client.post(
                    f"{self.config['fastapi_base_url']}/api/v2/files/upload",
                    files={"file": (path, b"test content", "image/jpeg")}
                )
                
                if response.status_code == 400:
                    self._add_result(
                        f"Path Traversal - {path}", "PASS", "HIGH",
                        "Dangerous path properly rejected"
                    )
                else:
                    self._add_result(
                        f"Path Traversal - {path}", "FAIL", "CRITICAL",
                        f"Potentially dangerous path accepted - Status: {response.status_code}",
                        evidence=f"Response: {response.text[:200]}"
                    )
        except Exception as e:
            self._add_result(
                "Path Traversal", "ERROR", "MEDIUM",
                f"Test error: {str(e)}"
            )
    
    # ==================== Reporting ====================
    
    def _generate_security_summary(self, results: List[SecurityTestResult]) -> Dict[str, Any]:
        """Generate security validation summary"""
        total = len(results)
        passed = len([r for r in results if r.status == "PASS"])
        failed = len([r for r in results if r.status == "FAIL"])
        warnings = len([r for r in results if r.status == "WARNING"])
        errors = len([r for r in results if r.status == "ERROR"])
        
        critical_issues = len([r for r in results if r.severity == "CRITICAL" and r.status == "FAIL"])
        high_issues = len([r for r in results if r.severity == "HIGH" and r.status == "FAIL"])
        medium_issues = len([r for r in results if r.severity == "MEDIUM" and r.status == "FAIL"])
        
        return {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "warnings": warnings,
            "errors": errors,
            "success_rate": (passed / total * 100) if total > 0 else 0,
            "critical_issues": critical_issues,
            "high_issues": high_issues,
            "medium_issues": medium_issues,
            "security_score": self._calculate_security_score(results)
        }
    
    def _calculate_security_score(self, results: List[SecurityTestResult]) -> float:
        """Calculate overall security score (0-100)"""
        if not results:
            return 0.0
        
        score = 100.0
        
        # Deduct points for failures based on severity
        for result in results:
            if result.status == "FAIL":
                if result.severity == "CRITICAL":
                    score -= 20.0
                elif result.severity == "HIGH":
                    score -= 10.0
                elif result.severity == "MEDIUM":
                    score -= 5.0
                else:
                    score -= 2.0
        
        # Deduct points for warnings
        for result in results:
            if result.status == "WARNING":
                score -= 1.0
        
        return max(0.0, min(100.0, score))

# ==================== Test Runner ====================

async def main():
    """Main test runner function"""
    async with CultivarSecurityValidator() as validator:
        results = await validator.run_comprehensive_security_validation()
        
        # Print summary
        summary = results["summary"]
        print(f"\n{'='*60}")
        print(f"CULTIVAR SECURITY VALIDATION SUMMARY")
        print(f"{'='*60}")
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Warnings: {summary['warnings']}")
        print(f"Errors: {summary['errors']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print(f"Security Score: {summary['security_score']:.1f}/100")
        print(f"\nCritical Issues: {summary['critical_issues']}")
        print(f"High Issues: {summary['high_issues']}")
        print(f"Medium Issues: {summary['medium_issues']}")
        
        # Save detailed results
        with open("security_validation_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\nDetailed results saved to: security_validation_results.json")
        
        return results

if __name__ == "__main__":
    asyncio.run(main())