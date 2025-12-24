#!/usr/bin/env python3
"""
Deployment and Infrastructure Validation Framework for CultivAR Application
Ensures production-ready deployment, infrastructure, and operational excellence.
"""

import asyncio
import aiohttp
import json
import logging
import argparse
import sys
import time
import subprocess
import os
import platform
import socket
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import ssl
import requests
import yaml
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DeploymentStatus(Enum):
    """Deployment status enumeration"""
    PENDING = "pending"
    DEPLOYING = "deploying"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLING_BACK = "rolling_back"

class EnvironmentType(Enum):
    """Environment types"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"

@dataclass
class InfrastructureCheck:
    """Infrastructure validation check"""
    component: str
    status: str
    message: str
    details: Dict[str, Any]
    timestamp: datetime

@dataclass
class DeploymentValidationResult:
    """Deployment validation result"""
    test_name: str
    passed: bool
    score: float  # 0.0 to 100.0
    infrastructure_checks: List[InfrastructureCheck]
    evidence: List[str]
    timestamp: datetime
    recommendations: List[str]

class DeploymentValidator:
    """Main deployment and infrastructure validation framework"""
    
    def __init__(self, base_url: str, auth_token: str = None, environment: str = "production"):
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.environment = EnvironmentType(environment.lower())
        self.session = None
        self.test_results: List[DeploymentValidationResult] = []
        
        # Infrastructure requirements
        self.required_ports = [80, 443, 3000, 8000, 5000]
        self.min_system_resources = {
            "cpu_cores": 2,
            "memory_gb": 4,
            "disk_gb": 20
        }
        
        # Docker and containerization requirements
        self.docker_config_files = [
            "Dockerfile",
            "docker-compose.yml",
            "docker-compose.prod.yml",
            ".dockerignore"
        ]
        
        # Environment configuration requirements
        self.required_env_vars = [
            "DATABASE_URL",
            "SECRET_KEY",
            "JWT_SECRET",
            "ENVIRONMENT"
        ]
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'CultivAR-DeploymentValidator/1.0',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        )
        if self.auth_token:
            self.session.headers['Authorization'] = f'Bearer {self.auth_token}'
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def check_system_resources(self) -> InfrastructureCheck:
        """Check system resources and capacity"""
        try:
            import psutil
            
            cpu_count = psutil.cpu_count()
            memory_gb = psutil.virtual_memory().total / (1024**3)
            disk_gb = psutil.disk_usage('/').total / (1024**3)
            
            cpu_ok = cpu_count >= self.min_system_resources["cpu_cores"]
            memory_ok = memory_gb >= self.min_system_resources["memory_gb"]
            disk_ok = disk_gb >= self.min_system_resources["disk_gb"]
            
            details = {
                "cpu_cores": cpu_count,
                "memory_gb": round(memory_gb, 2),
                "disk_gb": round(disk_gb, 2),
                "cpu_requirement": self.min_system_resources["cpu_cores"],
                "memory_requirement": self.min_system_resources["memory_gb"],
                "disk_requirement": self.min_system_resources["disk_gb"]
            }
            
            if cpu_ok and memory_ok and disk_ok:
                return InfrastructureCheck(
                    component="system_resources",
                    status="success",
                    message=f"System resources adequate: {cpu_count} cores, {memory_gb:.1f}GB RAM, {disk_gb:.1f}GB disk",
                    details=details,
                    timestamp=datetime.now()
                )
            else:
                issues = []
                if not cpu_ok:
                    issues.append(f"CPU cores: {cpu_count} < {self.min_system_resources['cpu_cores']}")
                if not memory_ok:
                    issues.append(f"Memory: {memory_gb:.1f}GB < {self.min_system_resources['memory_gb']}GB")
                if not disk_ok:
                    issues.append(f"Disk: {disk_gb:.1f}GB < {self.min_system_resources['disk_gb']}GB")
                
                return InfrastructureCheck(
                    component="system_resources",
                    status="failed",
                    message=f"System resource deficiencies: {', '.join(issues)}",
                    details=details,
                    timestamp=datetime.now()
                )
                
        except Exception as e:
            return InfrastructureCheck(
                component="system_resources",
                status="error",
                message=f"Unable to check system resources: {str(e)}",
                details={"error": str(e)},
                timestamp=datetime.now()
            )
    
    def check_network_connectivity(self) -> InfrastructureCheck:
        """Check network connectivity and ports"""
        try:
            connectivity_issues = []
            open_ports = []
            
            for port in self.required_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    result = sock.connect_ex(('localhost', port))
                    sock.close()
                    
                    if result == 0:
                        open_ports.append(port)
                    else:
                        connectivity_issues.append(f"Port {port} not accessible")
                except:
                    connectivity_issues.append(f"Unable to check port {port}")
            
            details = {
                "open_ports": open_ports,
                "required_ports": self.required_ports,
                "connectivity_issues": connectivity_issues
            }
            
            if len(connectivity_issues) <= 2:  # Allow minor issues
                return InfrastructureCheck(
                    component="network_connectivity",
                    status="success",
                    message=f"Network connectivity adequate: {len(open_ports)}/{len(self.required_ports)} required ports open",
                    details=details,
                    timestamp=datetime.now()
                )
            else:
                return InfrastructureCheck(
                    component="network_connectivity",
                    status="failed",
                    message=f"Network connectivity issues: {len(connectivity_issues)} problems detected",
                    details=details,
                    timestamp=datetime.now()
                )
                
        except Exception as e:
            return InfrastructureCheck(
                component="network_connectivity",
                status="error",
                message=f"Unable to check network connectivity: {str(e)}",
                details={"error": str(e)},
                timestamp=datetime.now()
            )
    
    def check_docker_configuration(self) -> InfrastructureCheck:
        """Check Docker and containerization configuration"""
        try:
            docker_files_found = []
            missing_files = []
            
            for docker_file in self.docker_config_files:
                if os.path.exists(docker_file):
                    docker_files_found.append(docker_file)
                else:
                    missing_files.append(docker_file)
            
            # Check Docker is installed
            try:
                result = subprocess.run(['docker', '--version'], 
                                      capture_output=True, text=True, timeout=10)
                docker_installed = result.returncode == 0
                docker_version = result.stdout.strip() if docker_installed else "Not installed"
            except:
                docker_installed = False
                docker_version = "Docker not found"
            
            # Check docker-compose
            try:
                result = subprocess.run(['docker-compose', '--version'], 
                                      capture_output=True, text=True, timeout=10)
                compose_installed = result.returncode == 0
                compose_version = result.stdout.strip() if compose_installed else "Not installed"
            except:
                compose_installed = False
                compose_version = "docker-compose not found"
            
            details = {
                "docker_files": docker_files_found,
                "missing_files": missing_files,
                "docker_installed": docker_installed,
                "docker_version": docker_version,
                "compose_installed": compose_installed,
                "compose_version": compose_version
            }
            
            # Score based on completeness
            file_score = len(docker_files_found) / len(self.docker_config_files) * 50
            tool_score = 50 if (docker_installed and compose_installed) else 25
            total_score = file_score + tool_score
            
            if total_score >= 80:
                return InfrastructureCheck(
                    component="docker_configuration",
                    status="success",
                    message=f"Docker configuration adequate (score: {total_score:.1f}%)",
                    details=details,
                    timestamp=datetime.now()
                )
            else:
                return InfrastructureCheck(
                    component="docker_configuration",
                    status="failed",
                    message=f"Docker configuration incomplete (score: {total_score:.1f}%)",
                    details=details,
                    timestamp=datetime.now()
                )
                
        except Exception as e:
            return InfrastructureCheck(
                component="docker_configuration",
                status="error",
                message=f"Unable to check Docker configuration: {str(e)}",
                details={"error": str(e)},
                timestamp=datetime.now()
            )
    
    def check_environment_variables(self) -> InfrastructureCheck:
        """Check environment configuration"""
        try:
            found_vars = []
            missing_vars = []
            
            for env_var in self.required_env_vars:
                if os.getenv(env_var):
                    found_vars.append(env_var)
                else:
                    missing_vars.append(env_var)
            
            # Check for .env file
            env_file_exists = os.path.exists('.env')
            
            # Check for environment-specific configs
            env_config_files = [
                f".env.{self.environment.value}",
                f"config/{self.environment.value}.yml",
                f"config/{self.environment.value}.yaml"
            ]
            
            env_config_exists = any(os.path.exists(f) for f in env_config_files)
            
            details = {
                "found_vars": found_vars,
                "missing_vars": missing_vars,
                "env_file_exists": env_file_exists,
                "env_config_exists": env_config_exists,
                "environment": self.environment.value
            }
            
            coverage = len(found_vars) / len(self.required_env_vars)
            
            if coverage >= 0.8 and env_file_exists:
                return InfrastructureCheck(
                    component="environment_variables",
                    status="success",
                    message=f"Environment configuration adequate (coverage: {coverage*100:.1f}%)",
                    details=details,
                    timestamp=datetime.now()
                )
            else:
                return InfrastructureCheck(
                    component="environment_variables",
                    status="failed",
                    message=f"Environment configuration incomplete (coverage: {coverage*100:.1f}%)",
                    details=details,
                    timestamp=datetime.now()
                )
                
        except Exception as e:
            return InfrastructureCheck(
                component="environment_variables",
                status="error",
                message=f"Unable to check environment variables: {str(e)}",
                details={"error": str(e)},
                timestamp=datetime.now()
            )
    
    def check_ssl_certificate(self) -> InfrastructureCheck:
        """Check SSL certificate configuration"""
        try:
            if not self.base_url.startswith('https://'):
                return InfrastructureCheck(
                    component="ssl_certificate",
                    status="warning",
                    message="HTTP URL provided - SSL not configured",
                    details={"protocol": "http"},
                    timestamp=datetime.now()
                )
            
            hostname = self.base_url.replace('https://', '').split('/')[0]
            
            try:
                context = ssl.create_default_context()
                with socket.create_connection((hostname, 443), timeout=10) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        cert = ssock.getpeercert()
                        
                        # Check certificate expiration
                        not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                        days_until_expiry = (not_after - datetime.now()).days
                        
                        # Check certificate subject
                        subject = dict(x[0] for x in cert['subject'])
                        common_name = subject.get('commonName', '')
                        
                        details = {
                            "subject": subject,
                            "common_name": common_name,
                            "days_until_expiry": days_until_expiry,
                            "issuer": dict(x[0] for x in cert['issuer']),
                            "serial_number": cert['serialNumber']
                        }
                        
                        if days_until_expiry > 30:
                            return InfrastructureCheck(
                                component="ssl_certificate",
                                status="success",
                                message=f"SSL certificate valid for {days_until_expiry} days",
                                details=details,
                                timestamp=datetime.now()
                            )
                        elif days_until_expiry > 7:
                            return InfrastructureCheck(
                                component="ssl_certificate",
                                status="warning",
                                message=f"SSL certificate expires soon ({days_until_expiry} days)",
                                details=details,
                                timestamp=datetime.now()
                            )
                        else:
                            return InfrastructureCheck(
                                component="ssl_certificate",
                                status="failed",
                                message=f"SSL certificate expires in {days_until_expiry} days",
                                details=details,
                                timestamp=datetime.now()
                            )
                            
            except Exception as ssl_error:
                return InfrastructureCheck(
                    component="ssl_certificate",
                    status="failed",
                    message=f"SSL certificate validation failed: {str(ssl_error)}",
                    details={"error": str(ssl_error)},
                    timestamp=datetime.now()
                )
                
        except Exception as e:
            return InfrastructureCheck(
                component="ssl_certificate",
                status="error",
                message=f"Unable to check SSL certificate: {str(e)}",
                details={"error": str(e)},
                timestamp=datetime.now()
            )
    
    async def check_infrastructure_health(self) -> DeploymentValidationResult:
        """Check overall infrastructure health"""
        evidence = []
        checks = []
        
        try:
            # Run all infrastructure checks
            checks.append(self.check_system_resources())
            checks.append(self.check_network_connectivity())
            checks.append(self.check_docker_configuration())
            checks.append(self.check_environment_variables())
            checks.append(self.check_ssl_certificate())
            
            # Analyze results
            successful_checks = [c for c in checks if c.status == "success"]
            failed_checks = [c for c in checks if c.status == "failed"]
            warning_checks = [c for c in checks if c.status == "warning"]
            error_checks = [c for c in checks if c.status == "error"]
            
            evidence.append(f"✅ Infrastructure checks completed: {len(checks)} total")
            evidence.append(f"✅ Successful checks: {len(successful_checks)}")
            evidence.append(f"⚠️  Warning checks: {len(warning_checks)}")
            evidence.append(f"❌ Failed checks: {len(failed_checks)}")
            evidence.append(f"💥 Error checks: {len(error_checks)}")
            
            # Calculate infrastructure score
            total_checks = len(checks)
            if total_checks > 0:
                success_score = (len(successful_checks) / total_checks) * 100
                warning_penalty = (len(warning_checks) / total_checks) * 10
                error_penalty = (len(error_checks) / total_checks) * 20
                failed_penalty = (len(failed_checks) / total_checks) * 30
                
                infrastructure_score = max(0, success_score - warning_penalty - error_penalty - failed_penalty)
            else:
                infrastructure_score = 0
            
            # Add evidence for each check
            for check in checks:
                evidence.append(f"📋 {check.component}: {check.message}")
            
            passed = infrastructure_score >= 70 and len(failed_checks) <= 1
            
            return DeploymentValidationResult(
                test_name="infrastructure_health",
                passed=passed,
                score=infrastructure_score,
                infrastructure_checks=checks,
                evidence=evidence,
                timestamp=datetime.now(),
                recommendations=[
                    f"Infrastructure health score: {infrastructure_score:.1f}%",
                    "Ensure all required ports are accessible",
                    "Verify Docker configuration files are present",
                    "Set up proper environment variables",
                    "Maintain SSL certificate validity",
                    "Monitor system resource usage"
                ]
            )
            
        except Exception as e:
            return DeploymentValidationResult(
                test_name="infrastructure_health",
                passed=False,
                score=0,
                infrastructure_checks=[],
                evidence=[f"❌ Infrastructure health check failed: {str(e)}"],
                timestamp=datetime.now(),
                recommendations=["Check infrastructure validation", "Verify system requirements"]
            )
    
    async def test_production_readiness(self) -> DeploymentValidationResult:
        """Test production readiness indicators"""
        evidence = []
        checks = []
        
        try:
            # Test health endpoint
            health_response = await self.session.get(f"{self.base_url}/health")
            if health_response.status == 200:
                evidence.append("✅ Health endpoint accessible")
                health_data = await health_response.json()
                evidence.append(f"✅ Health status: {health_data.get('status', 'unknown')}")
            else:
                evidence.append(f"❌ Health endpoint failed (status: {health_response.status})")
            
            # Test API endpoint
            api_response = await self.session.get(f"{self.base_url}/api")
            if api_response.status == 200:
                evidence.append("✅ API endpoint accessible")
                api_data = await api_response.json()
                version = api_data.get('version', 'unknown')
                evidence.append(f"✅ API version: {version}")
            else:
                evidence.append(f"❌ API endpoint failed (status: {api_response.status})")
            
            # Test authentication endpoint
            auth_response = await self.session.get(f"{self.base_url}/api/auth/profile")
            if auth_response.status in [200, 401]:  # 401 is acceptable (requires auth)
                evidence.append("✅ Authentication endpoint accessible")
            else:
                evidence.append(f"❌ Authentication endpoint failed (status: {auth_response.status})")
            
            # Test error handling (should return appropriate status codes)
            error_response = await self.session.get(f"{self.base_url}/api/nonexistent")
            if error_response.status in [404, 400]:
                evidence.append("✅ Proper error handling (404 for nonexistent endpoint)")
            else:
                evidence.append(f"⚠️  Unexpected error response: {error_response.status}")
            
            # Check response times
            start_time = time.time()
            performance_response = await self.session.get(f"{self.base_url}/api/dashboard")
            response_time = (time.time() - start_time) * 1000  # Convert to ms
            
            if response_time < 500:
                evidence.append(f"✅ Good response time: {response_time:.2f}ms")
            elif response_time < 2000:
                evidence.append(f"⚠️  Acceptable response time: {response_time:.2f}ms")
            else:
                evidence.append(f"❌ Slow response time: {response_time:.2f}ms")
            
            # Calculate production readiness score
            endpoint_score = 0
            if health_response.status == 200:
                endpoint_score += 25
            if api_response.status == 200:
                endpoint_score += 25
            if auth_response.status in [200, 401]:
                endpoint_score += 25
            if error_response.status in [404, 400]:
                endpoint_score += 25
            
            # Performance bonus/penalty
            if response_time < 500:
                performance_score = 25
            elif response_time < 2000:
                performance_score = 15
            else:
                performance_score = 5
            
            production_score = endpoint_score + performance_score
            
            # Check for production indicators
            production_indicators = []
            if os.path.exists('docker-compose.prod.yml'):
                production_indicators.append("Production Docker Compose file")
            if os.path.exists('.env.production'):
                production_indicators.append("Production environment file")
            if os.path.exists('nginx.conf'):
                production_indicators.append("NGINX configuration")
            if os.path.exists('scripts/deploy.sh'):
                production_indicators.append("Deployment script")
            
            evidence.append(f"📁 Production indicators found: {len(production_indicators)}")
            for indicator in production_indicators:
                evidence.append(f"  - {indicator}")
            
            # Add production indicator bonus
            production_score = min(100, production_score + len(production_indicators) * 5)
            
            passed = production_score >= 80
            
            return DeploymentValidationResult(
                test_name="production_readiness",
                passed=passed,
                score=production_score,
                infrastructure_checks=checks,
                evidence=evidence,
                timestamp=datetime.now(),
                recommendations=[
                    f"Production readiness score: {production_score:.1f}%",
                    "Ensure all critical endpoints are accessible",
                    "Maintain response times under 500ms",
                    "Implement proper error handling",
                    "Set up production configuration files",
                    "Create deployment automation scripts"
                ]
            )
            
        except Exception as e:
            return DeploymentValidationResult(
                test_name="production_readiness",
                passed=False,
                score=0,
                infrastructure_checks=checks,
                evidence=[f"❌ Production readiness test failed: {str(e)}"],
                timestamp=datetime.now(),
                recommendations=["Check application deployment", "Verify production configuration"]
            )
    
    async def test_monitoring_setup(self) -> DeploymentValidationResult:
        """Test monitoring and logging configuration"""
        evidence = []
        checks = []
        
        try:
            # Test monitoring endpoints
            monitoring_endpoints = [
                "/health",
                "/metrics",
                "/status",
                "/info"
            ]
            
            accessible_endpoints = 0
            for endpoint in monitoring_endpoints:
                try:
                    response = await self.session.get(f"{self.base_url}{endpoint}")
                    if response.status == 200:
                        accessible_endpoints += 1
                        evidence.append(f"✅ Monitoring endpoint accessible: {endpoint}")
                    else:
                        evidence.append(f"⚠️  Monitoring endpoint failed: {endpoint} (status: {response.status})")
                except:
                    evidence.append(f"❌ Monitoring endpoint unreachable: {endpoint}")
            
            # Check for monitoring configuration files
            monitoring_files = [
                "prometheus.yml",
                "grafana.yml",
                "docker-compose.monitoring.yml",
                "monitoring/docker-compose.yml"
            ]
            
            found_monitoring_files = []
            for monitoring_file in monitoring_files:
                if os.path.exists(monitoring_file):
                    found_monitoring_files.append(monitoring_file)
            
            evidence.append(f"📊 Monitoring configuration files: {len(found_monitoring_files)}")
            
            # Check for logging configuration
            logging_configs = [
                "logging.yml",
                "log.config",
                "config/logging.yml",
                "docker-compose.yml"  # Check for logging in docker-compose
            ]
            
            found_logging_configs = []
            for logging_config in logging_configs:
                if os.path.exists(logging_config):
                    found_logging_configs.append(logging_config)
            
            evidence.append(f"📝 Logging configuration files: {len(found_logging_configs)}")
            
            # Check environment-specific monitoring
            if self.environment == EnvironmentType.PRODUCTION:
                # Additional checks for production
                if accessible_endpoints >= 3:
                    evidence.append("✅ Production monitoring adequate")
                else:
                    evidence.append("⚠️  Production monitoring needs improvement")
            
            # Calculate monitoring score
            endpoint_score = (accessible_endpoints / len(monitoring_endpoints)) * 50
            config_score = min(50, len(found_monitoring_files) * 25)
            
            monitoring_score = endpoint_score + config_score
            
            passed = monitoring_score >= 60 and accessible_endpoints >= 2
            
            return DeploymentValidationResult(
                test_name="monitoring_setup",
                passed=passed,
                score=monitoring_score,
                infrastructure_checks=checks,
                evidence=evidence,
                timestamp=datetime.now(),
                recommendations=[
                    f"Monitoring setup score: {monitoring_score:.1f}%",
                    "Implement comprehensive monitoring endpoints",
                    "Set up Prometheus and Grafana for metrics",
                    "Configure structured logging",
                    "Set up alerting for production environment",
                    "Monitor application performance and health"
                ]
            )
            
        except Exception as e:
            return DeploymentValidationResult(
                test_name="monitoring_setup",
                passed=False,
                score=0,
                infrastructure_checks=checks,
                evidence=[f"❌ Monitoring setup test failed: {str(e)}"],
                timestamp=datetime.now(),
                recommendations=["Check monitoring configuration", "Implement comprehensive logging and metrics"]
            )
    
    async def test_security_configuration(self) -> DeploymentValidationResult:
        """Test security configuration for deployment"""
        evidence = []
        checks = []
        
        try:
            # Test HTTPS enforcement
            if self.base_url.startswith('https://'):
                evidence.append("✅ HTTPS enforced")
            else:
                evidence.append("❌ HTTPS not enforced - security risk")
            
            # Test security headers
            try:
                response = await self.session.get(self.base_url)
                headers = response.headers
                
                security_headers = {
                    'Strict-Transport-Security': 'HSTS header',
                    'X-Content-Type-Options': 'Content-Type-Options header',
                    'X-Frame-Options': 'Frame-Options header',
                    'X-XSS-Protection': 'XSS-Protection header',
                    'Content-Security-Policy': 'CSP header'
                }
                
                security_score = 0
                for header_name, description in security_headers.items():
                    if header_name in headers:
                        evidence.append(f"✅ {description} present")
                        security_score += 20
                    else:
                        evidence.append(f"❌ {description} missing")
                
                evidence.append(f"📊 Security headers score: {security_score}%")
                
            except Exception as e:
                evidence.append(f"⚠️  Could not check security headers: {str(e)}")
                security_score = 0
            
            # Check for security configuration files
            security_files = [
                ".env",  # Contains sensitive configuration
                "nginx.conf",  # Web server security
                "ssl/",  # SSL certificates directory
                "certificates/",  # Certificates directory
                "security.md",  # Security documentation
            ]
            
            found_security_files = []
            for security_file in security_files:
                if os.path.exists(security_file):
                    found_security_files.append(security_file)
            
            evidence.append(f"🔒 Security configuration files: {len(found_security_files)}")
            
            # Check file permissions on sensitive files
            sensitive_files = [".env", "docker-compose.yml", "nginx.conf"]
            permission_issues = 0
            
            for sensitive_file in sensitive_files:
                if os.path.exists(sensitive_file):
                    stat = os.stat(sensitive_file)
                    mode = oct(stat.st_mode)[-3:]
                    # Check if file is readable by others (insecure)
                    if mode[-1] in ['4', '5', '6', '7']:
                        permission_issues += 1
                        evidence.append(f"⚠️  {sensitive_file} has broad permissions: {mode}")
            
            if permission_issues == 0:
                evidence.append("✅ Sensitive files have appropriate permissions")
            
            # Calculate security configuration score
            https_score = 25 if self.base_url.startswith('https://') else 0
            file_score = min(25, len(found_security_files) * 12.5)
            permission_score = max(0, 25 - (permission_issues * 12.5))
            
            security_score = https_score + security_score + file_score + permission_score
            
            # Add bonus for good security practices
            if self.base_url.startswith('https://') and security_headers_score >= 60:
                security_score = min(100, security_score + 10)
            
            passed = security_score >= 70
            
            return DeploymentValidationResult(
                test_name="security_configuration",
                passed=passed,
                score=security_score,
                infrastructure_checks=checks,
                evidence=evidence,
                timestamp=datetime.now(),
                recommendations=[
                    f"Security configuration score: {security_score:.1f}%",
                    "Enforce HTTPS for all connections",
                    "Implement comprehensive security headers",
                    "Use strong file permissions on sensitive files",
                    "Set up proper SSL certificate management",
                    "Document security configuration and procedures"
                ]
            )
            
        except Exception as e:
            return DeploymentValidationResult(
                test_name="security_configuration",
                passed=False,
                score=0,
                infrastructure_checks=checks,
                evidence=[f"❌ Security configuration test failed: {str(e)}"],
                timestamp=datetime.now(),
                recommendations=["Check security configuration", "Implement proper security measures"]
            )
    
    async def run_deployment_validation(self) -> Dict[str, Any]:
        """Run comprehensive deployment and infrastructure validation"""
        logger.info("Starting deployment and infrastructure validation")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "environment": self.environment.value,
            "total_tests": 0,
            "passed_tests": 0,
            "overall_deployment_score": 0.0,
            "test_results": [],
            "infrastructure_summary": {},
            "recommendations": []
        }
        
        # Run deployment tests
        deployment_tests = [
            ("Infrastructure Health", self.check_infrastructure_health),
            ("Production Readiness", self.test_production_readiness),
            ("Monitoring Setup", self.test_monitoring_setup),
            ("Security Configuration", self.test_security_configuration)
        ]
        
        results["total_tests"] = len(deployment_tests)
        
        total_score = 0.0
        all_infrastructure_checks = []
        
        for test_name, test_function in deployment_tests:
            try:
                logger.info(f"Running deployment test: {test_name}")
                result = await test_function()
                
                results["test_results"].append({
                    "test_name": result.test_name,
                    "display_name": test_name,
                    "passed": result.passed,
                    "score": result.score,
                    "evidence": result.evidence,
                    "recommendations": result.recommendations,
                    "infrastructure_checks": [
                        {
                            "component": check.component,
                            "status": check.status,
                            "message": check.message,
                            "details": check.details,
                            "timestamp": check.timestamp.isoformat()
                        }
                        for check in result.infrastructure_checks
                    ],
                    "timestamp": result.timestamp.isoformat()
                })
                
                if result.passed:
                    results["passed_tests"] += 1
                
                total_score += result.score
                all_infrastructure_checks.extend(result.infrastructure_checks)
                
            except Exception as e:
                logger.error(f"Error running test {test_name}: {str(e)}")
                results["test_results"].append({
                    "test_name": test_name.lower().replace(' ', '_'),
                    "display_name": test_name,
                    "passed": False,
                    "score": 0,
                    "evidence": [f"❌ Test failed: {str(e)}"],
                    "recommendations": ["Check test implementation and system state"],
                    "infrastructure_checks": [],
                    "timestamp": datetime.now().isoformat()
                })
        
        # Calculate overall score
        if results["total_tests"] > 0:
            results["overall_deployment_score"] = total_score / results["total_tests"]
        else:
            results["overall_deployment_score"] = 0.0
        
        # Create infrastructure summary
        infrastructure_summary = {}
        for check in all_infrastructure_checks:
            component = check.component
            if component not in infrastructure_summary:
                infrastructure_summary[component] = {
                    "status": check.status,
                    "message": check.message,
                    "checks": 0,
                    "successes": 0,
                    "failures": 0
                }
            
            infrastructure_summary[component]["checks"] += 1
            if check.status == "success":
                infrastructure_summary[component]["successes"] += 1
            elif check.status in ["failed", "error"]:
                infrastructure_summary[component]["failures"] += 1
        
        results["infrastructure_summary"] = infrastructure_summary
        
        # Generate comprehensive recommendations
        if results["overall_deployment_score"] >= 80:
            results["recommendations"].append("✅ Excellent deployment readiness - system ready for production")
        elif results["overall_deployment_score"] >= 60:
            results["recommendations"].append("⚠️  Good deployment readiness - improvements needed for production")
        else:
            results["recommendations"].append("❌ Limited deployment readiness - significant work required")
        
        # Environment-specific recommendations
        if self.environment == EnvironmentType.PRODUCTION:
            if results["overall_deployment_score"] < 90:
                results["recommendations"].append("🚨 CRITICAL: Production environment requires higher standards")
        
        # Infrastructure component recommendations
        failed_components = [
            component for component, summary in infrastructure_summary.items()
            if summary["failures"] > summary["successes"]
        ]
        
        if failed_components:
            results["recommendations"].append(f"🔧 Address failed infrastructure components: {', '.join(failed_components)}")
        
        # Security recommendations
        security_tests = [r for r in results["test_results"] if "security" in r["display_name"].lower()]
        if security_tests and security_tests[0]["score"] < 70:
            results["recommendations"].append("🔒 CRITICAL: Improve security configuration before production")
        
        # Monitoring recommendations
        monitoring_tests = [r for r in results["test_results"] if "monitoring" in r["display_name"].lower()]
        if monitoring_tests and monitoring_tests[0]["score"] < 70:
            results["recommendations"].append("📊 Implement comprehensive monitoring and logging")
        
        # Production deployment checklist
        results["recommendations"].append("📋 Production deployment checklist:")
        results["recommendations"].append("   - Verify all environment variables are set")
        results["recommendations"].append("   - Test deployment on staging environment first")
        results["recommendations"].append("   - Set up automated deployment pipeline")
        results["recommendations"].append("   - Implement rollback procedures")
        results["recommendations"].append("   - Configure monitoring and alerting")
        results["recommendations"].append("   - Test disaster recovery procedures")
        results["recommendations"].append("   - Conduct security audit")
        
        logger.info(f"✅ Deployment validation completed - Overall score: {results['overall_deployment_score']:.1f}%")
        return results

def main():
    """CLI interface for deployment testing"""
    parser = argparse.ArgumentParser(description="Deployment and Infrastructure Testing Framework")
    parser.add_argument("--url", required=True, help="Base URL for testing")
    parser.add_argument("--token", help="JWT authentication token")
    parser.add_argument("--environment", choices=["development", "staging", "production", "testing"],
                       default="production", help="Target environment")
    parser.add_argument("--output", help="Output file for results (JSON)")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run validation
    async def run():
        async with DeploymentValidator(args.url, args.token, args.environment) as validator:
            results = await validator.run_deployment_validation()
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            logger.info(f"Results saved to {args.output}")
        else:
            print(json.dumps(results, indent=2, default=str))
        
        return results
    
    results = asyncio.run(run())
    
    # Exit with appropriate code
    if results["overall_deployment_score"] >= 60:  # 60% threshold
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure

if __name__ == "__main__":
    main()