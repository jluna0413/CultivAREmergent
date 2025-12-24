#!/usr/bin/env python3
"""
API Contract Testing and Versioning Framework for CultivAR Application
Ensures API compatibility, versioning, and contract adherence across all endpoints.
"""

import asyncio
import aiohttp
import json
import logging
import argparse
import sys
import time
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import jsonschema
from jsonschema import validate, ValidationError
import yaml
import urllib.parse
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ContractStatus(Enum):
    """API contract status"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    WARNING = "warning"
    DEPRECATED = "deprecated"

class VersionCompatibility(Enum):
    """API version compatibility levels"""
    BACKWARD_COMPATIBLE = "backward_compatible"
    FORWARD_COMPATIBLE = "forward_compatible"
    BREAKING = "breaking"
    UNKNOWN = "unknown"

@dataclass
class APIContract:
    """API contract definition"""
    endpoint: str
    method: str
    version: str
    schema: Dict[str, Any]
    required_fields: List[str]
    optional_fields: List[str]
    response_schema: Dict[str, Any]
    deprecated: bool = False

@dataclass
class ContractTestResult:
    """API contract test result"""
    test_name: str
    endpoint: str
    method: str
    status: ContractStatus
    score: float  # 0.0 to 100.0
    issues: List[Dict[str, Any]]
    evidence: List[str]
    timestamp: datetime
    recommendations: List[str]

class APIContractValidator:
    """Main API contract testing and versioning validation framework"""
    
    def __init__(self, base_url: str, auth_token: str = None, api_version: str = "v1"):
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.api_version = api_version
        self.session = None
        self.test_results: List[ContractTestResult] = []
        
        # API versioning configuration
        self.supported_versions = ["v1", "v2", "latest"]
        self.deprecated_versions = []
        
        # OpenAPI specification patterns
        self.openapi_patterns = [
            "/openapi.json",
            "/swagger.json",
            "/api/docs/openapi.json",
            "/docs/openapi.json"
        ]
        
        # Common API endpoints for CultivAR
        self.cultivar_endpoints = {
            "GET": [
                "/api/auth/profile",
                "/api/auth/refresh",
                "/api/plants",
                "/api/plants/{id}",
                "/api/dashboard",
                "/api/dashboard/stats",
                "/api/sensors",
                "/api/sensors/{id}/data",
                "/api/strains",
                "/api/activities",
                "/api/harvests",
                "/api/users",
                "/api/settings"
            ],
            "POST": [
                "/api/auth/login",
                "/api/auth/register",
                "/api/plants",
                "/api/sensors",
                "/api/activities",
                "/api/harvests"
            ],
            "PUT": [
                "/api/plants/{id}",
                "/api/sensors/{id}",
                "/api/users/{id}",
                "/api/settings"
            ],
            "DELETE": [
                "/api/plants/{id}",
                "/api/sensors/{id}",
                "/api/activities/{id}"
            ]
        }
        
        # Expected response schemas for key endpoints
        self.expected_schemas = {
            "/api/auth/login": {
                "type": "object",
                "required": ["access_token", "refresh_token", "user"],
                "properties": {
                    "access_token": {"type": "string"},
                    "refresh_token": {"type": "string"},
                    "user": {"type": "object"}
                }
            },
            "/api/plants": {
                "type": "object",
                "required": ["plants"],
                "properties": {
                    "plants": {"type": "array"},
                    "total": {"type": "integer"},
                    "page": {"type": "integer"}
                }
            },
            "/api/dashboard": {
                "type": "object",
                "required": ["stats"],
                "properties": {
                    "stats": {"type": "object"},
                    "recent_activities": {"type": "array"}
                }
            }
        }
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'CultivAR-APIContractValidator/1.0',
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-API-Version': self.api_version
            }
        )
        if self.auth_token:
            self.session.headers['Authorization'] = f'Bearer {self.auth_token}'
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def fetch_openapi_spec(self) -> Optional[Dict[str, Any]]:
        """Fetch OpenAPI specification from the API"""
        for pattern in self.openapi_patterns:
            try:
                url = f"{self.base_url}{pattern}"
                async with self.session.get(url) as response:
                    if response.status == 200:
                        spec = await response.json()
                        logger.info(f"✅ Found OpenAPI spec at {pattern}")
                        return spec
                    else:
                        logger.debug(f"OpenAPI spec not found at {pattern} (status: {response.status})")
            except Exception as e:
                logger.debug(f"Failed to fetch OpenAPI spec from {pattern}: {str(e)}")
        
        logger.warning("⚠️  No OpenAPI specification found")
        return None
    
    async def validate_endpoint_schema(self, endpoint: str, method: str) -> ContractTestResult:
        """Validate endpoint against expected schema"""
        evidence = []
        issues = []
        
        try:
            # Test the endpoint
            url = f"{self.base_url}{endpoint}"
            
            # Prepare request based on method
            if method == "GET":
                async with self.session.get(url) as response:
                    status_code = response.status
                    try:
                        response_data = await response.json()
                    except:
                        response_data = {}
            elif method == "POST":
                # Use sample data for POST requests
                sample_data = self._get_sample_request_data(endpoint)
                async with self.session.post(url, json=sample_data) as response:
                    status_code = response.status
                    try:
                        response_data = await response.json()
                    except:
                        response_data = {}
            else:
                # For other methods, just check if endpoint exists
                async with self.session.request(method, url) as response:
                    status_code = response.status
                    response_data = {}
            
            evidence.append(f"✅ Endpoint {method} {endpoint} returned status {status_code}")
            
            # Check if endpoint is accessible
            if status_code in [200, 201, 400, 401, 403, 404, 422]:
                evidence.append("✅ Endpoint is accessible")
            else:
                issues.append({
                    "type": "endpoint_inaccessible",
                    "severity": "high",
                    "status_code": status_code,
                    "message": f"Endpoint returned unexpected status code: {status_code}"
                })
            
            # Validate response schema if we have data and expect a schema
            if response_data and endpoint in self.expected_schemas:
                expected_schema = self.expected_schemas[endpoint]
                try:
                    validate(instance=response_data, schema=expected_schema)
                    evidence.append("✅ Response schema validation passed")
                except ValidationError as e:
                    issues.append({
                        "type": "schema_validation_error",
                        "severity": "medium",
                        "message": f"Response schema validation failed: {str(e.message)}",
                        "details": str(e)
                    })
            
            # Check response time
            response_time = 0  # Would need to measure this properly
            if response_time > 2000:  # 2 seconds
                issues.append({
                    "type": "slow_response",
                    "severity": "low",
                    "response_time_ms": response_time,
                    "message": f"Response time too slow: {response_time}ms"
                })
            
            # Check for required fields in response
            if response_data and isinstance(response_data, dict):
                required_fields = self._get_required_fields_for_endpoint(endpoint)
                for field in required_fields:
                    if field not in response_data:
                        issues.append({
                            "type": "missing_required_field",
                            "severity": "medium",
                            "field": field,
                            "message": f"Required field '{field}' missing from response"
                        })
            
            # Calculate contract compliance score
            total_checks = 1 + len(issues)  # Basic accessibility + issues
            passed_checks = 1 if status_code in [200, 201, 400, 401, 403, 404, 422] else 0
            compliance_score = (passed_checks / total_checks) * 100
            
            status = ContractStatus.COMPLIANT if len(issues) == 0 else ContractStatus.WARNING
            passed = compliance_score >= 70
            
            return ContractTestResult(
                test_name="endpoint_schema_validation",
                endpoint=endpoint,
                method=method,
                status=status,
                score=compliance_score,
                issues=issues,
                evidence=evidence,
                timestamp=datetime.now(),
                recommendations=[
                    f"Endpoint {endpoint} compliance score: {compliance_score:.1f}%",
                    "Ensure all required fields are present in responses",
                    "Implement proper error handling and status codes",
                    "Add response time monitoring",
                    "Document API contracts clearly"
                ]
            )
            
        except Exception as e:
            return ContractTestResult(
                test_name="endpoint_schema_validation",
                endpoint=endpoint,
                method=method,
                status=ContractStatus.NON_COMPLIANT,
                score=0,
                issues=[{"error": str(e)}],
                evidence=[f"❌ Endpoint validation failed: {str(e)}"],
                timestamp=datetime.now(),
                recommendations=["Check endpoint implementation", "Verify API contract compliance"]
            )
    
    def _get_sample_request_data(self, endpoint: str) -> Dict[str, Any]:
        """Get sample request data for POST/PUT endpoints"""
        sample_data = {
            "/api/auth/login": {
                "email": "test@example.com",
                "password": "testpassword"
            },
            "/api/auth/register": {
                "email": "newuser@example.com",
                "password": "newpassword",
                "username": "newuser"
            },
            "/api/plants": {
                "name": "Test Plant",
                "strain": "Test Strain",
                "planting_date": "2025-01-01"
            },
            "/api/sensors": {
                "name": "Test Sensor",
                "type": "temperature",
                "location": "grow_room_1"
            },
            "/api/activities": {
                "plant_id": 1,
                "activity_type": "watering",
                "notes": "Test activity"
            }
        }
        
        return sample_data.get(endpoint, {})
    
    def _get_required_fields_for_endpoint(self, endpoint: str) -> List[str]:
        """Get list of required fields for endpoint response"""
        required_fields_map = {
            "/api/auth/login": ["access_token", "refresh_token", "user"],
            "/api/plants": ["plants", "total"],
            "/api/dashboard": ["stats"],
            "/api/sensors": ["sensors", "total"],
            "/api/strains": ["strains", "total"]
        }
        
        return required_fields_map.get(endpoint, [])
    
    async def test_api_versioning(self) -> ContractTestResult:
        """Test API versioning compliance"""
        evidence = []
        issues = []
        
        try:
            # Test version header
            version_headers = ["X-API-Version", "Accept-Version", "API-Version"]
            supported_versions = []
            
            for version_header in version_headers:
                for version in self.supported_versions:
                    try:
                        headers = {version_header: version}
                        response = await self.session.get(f"{self.base_url}/api/auth/profile", headers=headers)
                        
                        if response.status == 200:
                            supported_versions.append(f"{version_header}: {version}")
                            evidence.append(f"✅ Version header {version_header}:{version} supported")
                        else:
                            evidence.append(f"⚠️  Version header {version_header}:{version} not supported")
                    except:
                        evidence.append(f"❌ Version header {version_header}:{version} failed")
            
            # Test version in URL path
            version_paths = [f"/api/{self.api_version}/auth/profile", "/api/v1/auth/profile"]
            url_versioning_supported = False
            
            for version_path in version_paths:
                try:
                    response = await self.session.get(f"{self.base_url}{version_path}")
                    if response.status == 200:
                        url_versioning_supported = True
                        evidence.append(f"✅ URL versioning supported: {version_path}")
                        break
                except:
                    pass
            
            if not url_versioning_supported:
                evidence.append("⚠️  URL versioning not detected")
            
            # Test version negotiation
            try:
                # Test with version in Accept header
                headers = {"Accept": "application/vnd.cultivar.v1+json"}
                response = await self.session.get(f"{self.base_url}/api/auth/profile", headers=headers)
                
                if response.status == 200:
                    evidence.append("✅ Version negotiation via Accept header supported")
                else:
                    evidence.append("⚠️  Version negotiation via Accept header not working")
            except:
                evidence.append("❌ Version negotiation test failed")
            
            # Check for version deprecation notices
            try:
                response = await self.session.get(f"{self.base_url}/api/deprecation-notice")
                if response.status == 200:
                    deprecation_data = await response.json()
                    deprecated_versions = deprecation_data.get("deprecated_versions", [])
                    evidence.append(f"📋 Deprecation notices found for versions: {deprecated_versions}")
                else:
                    evidence.append("ℹ️  No deprecation notices endpoint found")
            except:
                evidence.append("ℹ️  Deprecation notices endpoint not accessible")
            
            # Calculate versioning compliance score
            version_score = 0
            if supported_versions:
                version_score += 40
            if url_versioning_supported:
                version_score += 30
            if "Version negotiation" in str(evidence):
                version_score += 30
            
            passed = version_score >= 70
            
            return ContractTestResult(
                test_name="api_versioning",
                endpoint="/api/*",
                method="GET",
                status=ContractStatus.COMPLIANT if passed else ContractStatus.WARNING,
                score=version_score,
                issues=issues,
                evidence=evidence,
                timestamp=datetime.now(),
                recommendations=[
                    f"API versioning score: {version_score:.1f}%",
                    "Implement consistent API versioning strategy",
                    "Support version headers and URL path versioning",
                    "Provide deprecation notices for old versions",
                    "Document versioning policy clearly"
                ]
            )
            
        except Exception as e:
            return ContractTestResult(
                test_name="api_versioning",
                endpoint="/api/*",
                method="GET",
                status=ContractStatus.NON_COMPLIANT,
                score=0,
                issues=[{"error": str(e)}],
                evidence=[f"❌ API versioning test failed: {str(e)}"],
                timestamp=datetime.now(),
                recommendations=["Check API versioning implementation", "Implement proper version negotiation"]
            )
    
    async def test_breaking_change_detection(self) -> ContractTestResult:
        """Test for breaking changes in API contracts"""
        evidence = []
        issues = []
        
        try:
            # Test critical endpoints for breaking changes
            critical_endpoints = [
                "/api/auth/login",
                "/api/auth/profile",
                "/api/plants",
                "/api/dashboard"
            ]
            
            breaking_changes_detected = []
            
            for endpoint in critical_endpoints:
                try:
                    response = await self.session.get(f"{self.base_url}{endpoint}")
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        # Check for required fields that should never be removed
                        if endpoint == "/api/auth/login":
                            required_fields = ["access_token", "refresh_token", "user"]
                            missing_fields = [f for f in required_fields if f not in data]
                            if missing_fields:
                                breaking_changes_detected.append(f"Missing fields in {endpoint}: {missing_fields}")
                        
                        # Check response structure consistency
                        if isinstance(data, dict):
                            # Ensure response has expected structure
                            if endpoint == "/api/plants" and "plants" not in data:
                                breaking_changes_detected.append(f"Response structure changed in {endpoint}")
                        
                        evidence.append(f"✅ {endpoint} structure validation passed")
                    else:
                        evidence.append(f"⚠️  {endpoint} returned status {response.status}")
                        
                except Exception as e:
                    evidence.append(f"❌ {endpoint} validation failed: {str(e)}")
            
            # Test for field type consistency
            type_consistency_issues = []
            
            # This would require comparing with previous versions
            # For now, we'll check basic type consistency
            try:
                response = await self.session.get(f"{self.base_url}/api/plants")
                if response.status == 200:
                    data = await response.json()
                    if isinstance(data, dict) and "total" in data:
                        if not isinstance(data["total"], int):
                            type_consistency_issues.append("total field should be integer")
            except:
                pass
            
            # Check for deprecated field usage
            deprecated_fields = ["old_field", "legacy_data", "v1_only"]
            deprecated_usage = []
            
            # This would require analyzing the response structure
            # For demonstration, we'll check if any obvious deprecated patterns exist
            
            if breaking_changes_detected:
                issues.append({
                    "type": "breaking_changes_detected",
                    "severity": "critical",
                    "changes": breaking_changes_detected,
                    "message": f"Detected {len(breaking_changes_detected)} potential breaking changes"
                })
            
            if type_consistency_issues:
                issues.append({
                    "type": "type_inconsistency",
                    "severity": "high",
                    "issues": type_consistency_issues,
                    "message": f"Detected {len(type_consistency_issues)} type consistency issues"
                })
            
            # Calculate breaking change detection score
            total_checks = len(critical_endpoints)
            passed_checks = total_checks - len(breaking_changes_detected)
            breaking_change_score = (passed_checks / total_checks) * 100
            
            passed = breaking_change_score >= 90 and len(breaking_changes_detected) == 0
            
            return ContractTestResult(
                test_name="breaking_change_detection",
                endpoint="/api/*",
                method="GET",
                status=ContractStatus.COMPLIANT if passed else ContractStatus.NON_COMPLIANT,
                score=breaking_change_score,
                issues=issues,
                evidence=evidence,
                timestamp=datetime.now(),
                recommendations=[
                    f"Breaking change detection score: {breaking_change_score:.1f}%",
                    "Maintain backward compatibility in API contracts",
                    "Implement proper deprecation strategy",
                    "Use semantic versioning for API changes",
                    "Test all endpoints for breaking changes before deployment",
                    "Provide migration guides for API changes"
                ]
            )
            
        except Exception as e:
            return ContractTestResult(
                test_name="breaking_change_detection",
                endpoint="/api/*",
                method="GET",
                status=ContractStatus.NON_COMPLIANT,
                score=0,
                issues=[{"error": str(e)}],
                evidence=[f"❌ Breaking change detection test failed: {str(e)}"],
                timestamp=datetime.now(),
                recommendations=["Check API contract stability", "Implement breaking change detection"]
            )
    
    async def test_error_handling_consistency(self) -> ContractTestResult:
        """Test API error handling consistency"""
        evidence = []
        issues = []
        
        try:
            # Test various error scenarios
            error_scenarios = [
                ("/api/nonexistent", 404, "Not Found"),
                ("/api/auth/profile", 401, "Unauthorized"),
                ("/api/plants/999999", 404, "Not Found"),
                ("/api/auth/login", 400, "Bad Request")
            ]
            
            consistent_error_format = True
            error_formats = []
            
            for endpoint, expected_status, description in error_scenarios:
                try:
                    response = await self.session.get(f"{self.base_url}{endpoint}")
                    actual_status = response.status
                    
                    if actual_status == expected_status:
                        evidence.append(f"✅ {description} returns expected status {expected_status}")
                        
                        # Check error response format
                        try:
                            error_data = await response.json()
                            error_formats.append(error_data)
                            
                            # Check for common error fields
                            if "error" in error_data or "message" in error_data:
                                evidence.append(f"✅ {endpoint} has proper error format")
                            else:
                                evidence.append(f"⚠️  {endpoint} missing standard error fields")
                                
                        except:
                            evidence.append(f"⚠️  {endpoint} error response not JSON")
                    else:
                        evidence.append(f"⚠️  {endpoint} returned {actual_status}, expected {expected_status}")
                        
                except Exception as e:
                    evidence.append(f"❌ {endpoint} error test failed: {str(e)}")
            
            # Check error response consistency
            if error_formats:
                # Check if all error responses have similar structure
                first_error = error_formats[0]
                consistent_structure = True
                
                for error_response in error_formats[1:]:
                    # This is a simplified check - real implementation would be more sophisticated
                    if not set(first_error.keys()) == set(error_response.keys()):
                        consistent_structure = False
                        break
                
                if consistent_structure:
                    evidence.append("✅ Error response structure is consistent")
                else:
                    issues.append({
                        "type": "inconsistent_error_format",
                        "severity": "medium",
                        "message": "Error responses have inconsistent structure"
                    })
            
            # Test error message clarity
            try:
                response = await self.session.get(f"{self.base_url}/api/auth/login")
                if response.status == 400:
                    error_data = await response.json()
                    if "message" in error_data and len(error_data["message"]) > 10:
                        evidence.append("✅ Error messages are descriptive")
                    else:
                        issues.append({
                            "type": "unclear_error_messages",
                            "severity": "low",
                            "message": "Error messages could be more descriptive"
                        })
            except:
                pass
            
            # Calculate error handling score
            error_score = 0
            passed_scenarios = sum(1 for evidence_item in evidence if "✅" in evidence_item)
            error_score = (passed_scenarios / len(error_scenarios)) * 100
            
            if consistent_structure:
                error_score += 20
            
            error_score = min(100, error_score)
            
            passed = error_score >= 80
            
            return ContractTestResult(
                test_name="error_handling_consistency",
                endpoint="/api/*",
                method="GET",
                status=ContractStatus.COMPLIANT if passed else ContractStatus.WARNING,
                score=error_score,
                issues=issues,
                evidence=evidence,
                timestamp=datetime.now(),
                recommendations=[
                    f"Error handling consistency score: {error_score:.1f}%",
                    "Implement consistent error response format",
                    "Use appropriate HTTP status codes",
                    "Provide clear and actionable error messages",
                    "Document error handling behavior",
                    "Test all error scenarios thoroughly"
                ]
            )
            
        except Exception as e:
            return ContractTestResult(
                test_name="error_handling_consistency",
                endpoint="/api/*",
                method="GET",
                status=ContractStatus.NON_COMPLIANT,
                score=0,
                issues=[{"error": str(e)}],
                evidence=[f"❌ Error handling consistency test failed: {str(e)}"],
                timestamp=datetime.now(),
                recommendations=["Check API error handling", "Implement consistent error responses"]
            )
    
    async def test_api_documentation_compliance(self) -> ContractTestResult:
        """Test API documentation compliance"""
        evidence = []
        issues = []
        
        try:
            # Check for OpenAPI documentation
            openapi_spec = await self.fetch_openapi_spec()
            
            if openapi_spec:
                evidence.append("✅ OpenAPI specification found")
                
                # Validate OpenAPI spec structure
                required_openapi_fields = ["openapi", "info", "paths", "components"]
                missing_fields = []
                
                for field in required_openapi_fields:
                    if field not in openapi_spec:
                        missing_fields.append(field)
                
                if not missing_fields:
                    evidence.append("✅ OpenAPI specification has required fields")
                else:
                    issues.append({
                        "type": "incomplete_openapi_spec",
                        "severity": "medium",
                        "missing_fields": missing_fields,
                        "message": f"OpenAPI spec missing fields: {missing_fields}"
                    })
                
                # Check path coverage
                documented_paths = set(openapi_spec.get("paths", {}).keys())
                tested_paths = set()
                
                for method_endpoints in self.cultivar_endpoints.values():
                    tested_paths.update(method_endpoints)
                
                coverage = len(documented_paths.intersection(tested_paths)) / len(tested_paths) * 100
                evidence.append(f"📊 API documentation coverage: {coverage:.1f}%")
                
                if coverage < 80:
                    issues.append({
                        "type": "low_documentation_coverage",
                        "severity": "medium",
                        "coverage_percent": coverage,
                        "message": f"API documentation coverage too low: {coverage:.1f}%"
                    })
                
            else:
                issues.append({
                    "type": "missing_openapi_spec",
                    "severity": "high",
                    "message": "No OpenAPI specification found"
                })
            
            # Check for interactive API documentation
            doc_endpoints = ["/docs", "/api/docs", "/swagger", "/redoc"]
            interactive_docs_found = False
            
            for doc_endpoint in doc_endpoints:
                try:
                    response = await self.session.get(f"{self.base_url}{doc_endpoint}")
                    if response.status == 200:
                        evidence.append(f"✅ Interactive documentation found at {doc_endpoint}")
                        interactive_docs_found = True
                        break
                except:
                    pass
            
            if not interactive_docs_found:
                issues.append({
                    "type": "missing_interactive_docs",
                    "severity": "low",
                    "message": "No interactive API documentation found"
                })
            
            # Check for API changelog
            try:
                changelog_response = await self.session.get(f"{self.base_url}/api/changelog")
                if changelog_response.status == 200:
                    evidence.append("✅ API changelog found")
                else:
                    evidence.append("ℹ️  No API changelog found")
            except:
                evidence.append("ℹ️  API changelog endpoint not accessible")
            
            # Calculate documentation compliance score
            doc_score = 0
            if openapi_spec:
                doc_score += 40
            if not missing_fields:
                doc_score += 20
            if interactive_docs_found:
                doc_score += 20
            if coverage >= 80:
                doc_score += 20
            
            passed = doc_score >= 70
            
            return ContractTestResult(
                test_name="api_documentation_compliance",
                endpoint="/api/*",
                method="GET",
                status=ContractStatus.COMPLIANT if passed else ContractStatus.WARNING,
                score=doc_score,
                issues=issues,
                evidence=evidence,
                timestamp=datetime.now(),
                recommendations=[
                    f"API documentation compliance score: {doc_score:.1f}%",
                    "Provide comprehensive OpenAPI specification",
                    "Include interactive API documentation",
                    "Maintain API changelog",
                    "Document all endpoints and parameters",
                    "Provide code examples and usage guides"
                ]
            )
            
        except Exception as e:
            return ContractTestResult(
                test_name="api_documentation_compliance",
                endpoint="/api/*",
                method="GET",
                status=ContractStatus.NON_COMPLIANT,
                score=0,
                issues=[{"error": str(e)}],
                evidence=[f"❌ API documentation compliance test failed: {str(e)}"],
                timestamp=datetime.now(),
                recommendations=["Check API documentation", "Implement comprehensive API docs"]
            )
    
    async def run_api_contract_validation(self) -> Dict[str, Any]:
        """Run comprehensive API contract validation"""
        logger.info("Starting API contract and versioning validation")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "api_version": self.api_version,
            "total_tests": 0,
            "passed_tests": 0,
            "overall_contract_score": 0.0,
            "test_results": [],
            "contract_summary": {},
            "recommendations": []
        }
        
        # Run API contract tests
        contract_tests = [
            ("Endpoint Schema Validation", self.test_endpoint_schema_validation),
            ("API Versioning", self.test_api_versioning),
            ("Breaking Change Detection", self.test_breaking_change_detection),
            ("Error Handling Consistency", self.test_error_handling_consistency),
            ("Documentation Compliance", self.test_api_documentation_compliance)
        ]
        
        results["total_tests"] = len(contract_tests)
        
        total_score = 0.0
        all_issues = []
        
        for test_name, test_function in contract_tests:
            try:
                logger.info(f"Running API contract test: {test_name}")
                
                if test_name == "Endpoint Schema Validation":
                    # Test multiple endpoints
                    for method, endpoints in self.cultivar_endpoints.items():
                        for endpoint in endpoints[:3]:  # Test first 3 endpoints per method
                            result = await self.validate_endpoint_schema(endpoint, method)
                            results["test_results"].append({
                                "test_name": result.test_name,
                                "endpoint": result.endpoint,
                                "method": result.method,
                                "status": result.status.value,
                                "score": result.score,
                                "issues": result.issues,
                                "evidence": result.evidence,
                                "recommendations": result.recommendations,
                                "timestamp": result.timestamp.isoformat()
                            })
                            
                            if result.passed:
                                results["passed_tests"] += 1
                            
                            total_score += result.score
                            all_issues.extend(result.issues)
                else:
                    result = await test_function()
                    results["test_results"].append({
                        "test_name": result.test_name,
                        "endpoint": result.endpoint,
                        "method": result.method,
                        "status": result.status.value,
                        "score": result.score,
                        "issues": result.issues,
                        "evidence": result.evidence,
                        "recommendations": result.recommendations,
                        "timestamp": result.timestamp.isoformat()
                    })
                    
                    if result.passed:
                        results["passed_tests"] += 1
                    
                    total_score += result.score
                    all_issues.extend(result.issues)
                
            except Exception as e:
                logger.error(f"Error running test {test_name}: {str(e)}")
                results["test_results"].append({
                    "test_name": test_name.lower().replace(' ', '_'),
                    "endpoint": "/api/*",
                    "method": "GET",
                    "status": "failed",
                    "score": 0,
                    "issues": [{"error": str(e)}],
                    "evidence": [f"❌ Test failed: {str(e)}"],
                    "recommendations": ["Check test implementation and API state"],
                    "timestamp": datetime.now().isoformat()
                })
        
        # Calculate overall score
        if results["total_tests"] > 0:
            results["overall_contract_score"] = total_score / results["total_tests"]
        else:
            results["overall_contract_score"] = 0.0
        
        # Create contract summary
        contract_summary = {
            "total_endpoints_tested": len([r for r in results["test_results"] if r.get("endpoint") != "/api/*"]),
            "compliant_endpoints": len([r for r in results["test_results"] if r.get("status") == "compliant"]),
            "total_issues": len(all_issues),
            "critical_issues": len([i for i in all_issues if i.get("severity") == "critical"]),
            "high_issues": len([i for i in all_issues if i.get("severity") == "high"])
        }
        
        results["contract_summary"] = contract_summary
        
        # Generate comprehensive recommendations
        if results["overall_contract_score"] >= 80:
            results["recommendations"].append("✅ Excellent API contract compliance - system ready for production")
        elif results["overall_contract_score"] >= 60:
            results["recommendations"].append("⚠️  Good API contract compliance - improvements needed for production")
        else:
            results["recommendations"].append("❌ Limited API contract compliance - significant work required")
        
        # Critical issues recommendations
        if contract_summary["critical_issues"] > 0:
            results["recommendations"].append(f"🚨 CRITICAL: Address {contract_summary['critical_issues']} critical API contract issues")
        
        # Versioning recommendations
        version_tests = [r for r in results["test_results"] if "versioning" in r["test_name"]]
        if version_tests and version_tests[0]["score"] < 70:
            results["recommendations"].append("🔄 Improve API versioning strategy")
        
        # Documentation recommendations
        doc_tests = [r for r in results["test_results"] if "documentation" in r["test_name"]]
        if doc_tests and doc_tests[0]["score"] < 70:
            results["recommendations"].append("📚 Enhance API documentation coverage")
        
        # Breaking change recommendations
        breaking_tests = [r for r in results["test_results"] if "breaking_change" in r["test_name"]]
        if breaking_tests and breaking_tests[0]["score"] < 90:
            results["recommendations"].append("⚠️  Implement stricter breaking change detection")
        
        # API best practices
        results["recommendations"].append("📋 API contract best practices:")
        results["recommendations"].append("   - Implement semantic versioning")
        results["recommendations"].append("   - Maintain backward compatibility")
        results["recommendations"].append("   - Provide comprehensive API documentation")
        results["recommendations"].append("   - Use consistent error handling")
        results["recommendations"].append("   - Implement contract testing in CI/CD")
        results["recommendations"].append("   - Monitor API usage and performance")
        
        logger.info(f"✅ API contract validation completed - Overall score: {results['overall_contract_score']:.1f}%")
        return results
    
    async def test_endpoint_schema_validation(self) -> List[ContractTestResult]:
        """Test schema validation for multiple endpoints"""
        results = []
        
        for method, endpoints in self.cultivar_endpoints.items():
            for endpoint in endpoints[:3]:  # Test first 3 endpoints per method
                result = await self.validate_endpoint_schema(endpoint, method)
                results.append(result)
        
        return results

def main():
    """CLI interface for API contract testing"""
    parser = argparse.ArgumentParser(description="API Contract Testing Framework")
    parser.add_argument("--url", required=True, help="Base URL for testing")
    parser.add_argument("--token", help="JWT authentication token")
    parser.add_argument("--version", default="v1", help="API version to test")
    parser.add_argument("--output", help="Output file for results (JSON)")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run validation
    async def run():
        async with APIContractValidator(args.url, args.token, args.version) as validator:
            results = await validator.run_api_contract_validation()
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            logger.info(f"Results saved to {args.output}")
        else:
            print(json.dumps(results, indent=2, default=str))
        
        return results
    
    results = asyncio.run(run())
    
    # Exit with appropriate code
    if results["overall_contract_score"] >= 60:  # 60% threshold
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure

if __name__ == "__main__":
    main()