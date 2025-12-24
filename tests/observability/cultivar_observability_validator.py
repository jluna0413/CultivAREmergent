#!/usr/bin/env python3
"""
Monitoring and Observability Validation Framework for CultivAR Application
Ensures comprehensive monitoring, logging, metrics, and alerting capabilities.
"""

import asyncio
import aiohttp
import json
import logging
import argparse
import sys
import time
import psutil
import socket
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import threading
import subprocess
import re
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MonitoringLevel(Enum):
    """Monitoring coverage levels"""
    BASIC = "basic"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"
    ENTERPRISE = "enterprise"

class AlertSeverity(Enum):
    """Alert severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class MetricData:
    """Metric data point"""
    name: str
    value: float
    timestamp: datetime
    tags: Dict[str, str]
    unit: str = ""

@dataclass
class LogEntry:
    """Log entry structure"""
    timestamp: datetime
    level: str
    message: str
    source: str
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    metadata: Dict[str, Any] = None

@dataclass
class ObservabilityResult:
    """Observability test result"""
    test_name: str
    passed: bool
    score: float  # 0.0 to 100.0
    message: str
    metrics: List[MetricData]
    evidence: List[str]
    timestamp: datetime
    recommendations: List[str]

class ObservabilityValidator:
    """Main monitoring and observability validation framework"""
    
    def __init__(self, base_url: str, auth_token: str = None):
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.session = None
        self.test_results: List[ObservabilityResult] = []
        
        # Monitoring thresholds and expectations
        self.expected_metrics = self._get_expected_metrics()
        self.min_log_levels = ["INFO", "WARNING", "ERROR"]
        self.required_alerts = self._get_required_alerts()
        self.max_response_time_ms = 500  # 500ms for API calls
        
        # Performance baselines
        self.baseline_cpu_percent = 10.0
        self.baseline_memory_mb = 512.0
        self.baseline_disk_usage_percent = 50.0
        self.baseline_network_requests_per_sec = 10.0
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'CultivAR-ObservabilityValidator/1.0',
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
    
    def _get_expected_metrics(self) -> List[str]:
        """Get list of expected application metrics"""
        return [
            "http_requests_total", "http_request_duration_seconds",
            "active_connections", "database_connections_active",
            "cpu_usage_percent", "memory_usage_bytes",
            "disk_usage_percent", "network_io_bytes",
            "plant_count", "sensor_count", "user_count",
            "error_rate_percent", "throughput_requests_per_second"
        ]
    
    def _get_required_alerts(self) -> List[Dict[str, Any]]:
        """Get list of required alerting rules"""
        return [
            {
                "name": "High Response Time",
                "metric": "http_request_duration_seconds",
                "threshold": 1.0,  # 1 second
                "severity": "high",
                "description": "API response time exceeds 1 second"
            },
            {
                "name": "High Error Rate",
                "metric": "error_rate_percent",
                "threshold": 5.0,  # 5%
                "severity": "critical",
                "description": "Error rate exceeds 5%"
            },
            {
                "name": "Database Connection Issues",
                "metric": "database_connections_active",
                "threshold": 50,  # 50% of max connections
                "severity": "high",
                "description": "Database connection pool utilization high"
            },
            {
                "name": "High CPU Usage",
                "metric": "cpu_usage_percent",
                "threshold": 80.0,  # 80%
                "severity": "medium",
                "description": "CPU usage exceeds 80%"
            },
            {
                "name": "High Memory Usage",
                "metric": "memory_usage_bytes",
                "threshold": 1024*1024*1024*0.8,  # 80% of 1GB
                "severity": "medium",
                "description": "Memory usage exceeds 80%"
            }
        ]
    
    def collect_system_metrics(self) -> Dict[str, float]:
        """Collect current system metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            return {
                "cpu_usage_percent": cpu_percent,
                "memory_usage_percent": memory.percent,
                "memory_usage_bytes": memory.used,
                "disk_usage_percent": (disk.used / disk.total) * 100,
                "network_bytes_sent": network.bytes_sent,
                "network_bytes_recv": network.bytes_recv,
                "timestamp": datetime.now()
            }
        except Exception as e:
            logger.error(f"Error collecting system metrics: {str(e)}")
            return {}
    
    async def test_api_endpoint_monitoring(self) -> ObservabilityResult:
        """Test API endpoint monitoring and metrics collection"""
        try:
            evidence = []
            metrics = []
            start_time = time.time()
            
            # Test health endpoint
            health_response = await self.session.get(f"{self.base_url}/health")
            health_data = await health_response.json()
            response_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # Record API metrics
            metrics.append(MetricData(
                name="http_request_duration_ms",
                value=response_time,
                timestamp=datetime.now(),
                tags={"endpoint": "/health", "method": "GET"},
                unit="milliseconds"
            ))
            
            metrics.append(MetricData(
                name="http_requests_total",
                value=1,
                timestamp=datetime.now(),
                tags={"endpoint": "/health", "method": "GET", "status_code": str(health_response.status)},
                unit="count"
            ))
            
            evidence.append(f"✅ Health check responded in {response_time:.2f}ms")
            evidence.append(f"✅ Health status: {health_data.get('status', 'unknown')}")
            
            # Test multiple endpoints and collect metrics
            test_endpoints = [
                ("/api/auth/profile", "GET"),
                ("/api/plants", "GET"),
                ("/api/dashboard", "GET"),
                ("/api/sensors", "GET")
            ]
            
            for endpoint, method in test_endpoints:
                try:
                    start_time = time.time()
                    async with self.session.request(method, f"{self.base_url}{endpoint}") as response:
                        response_time = (time.time() - start_time) * 1000
                        
                        metrics.append(MetricData(
                            name="http_request_duration_ms",
                            value=response_time,
                            timestamp=datetime.now(),
                            tags={"endpoint": endpoint, "method": method},
                            unit="milliseconds"
                        ))
                        
                        metrics.append(MetricData(
                            name="http_requests_total",
                            value=1,
                            timestamp=datetime.now(),
                            tags={"endpoint": endpoint, "method": method, "status_code": str(response.status)},
                            unit="count"
                        ))
                        
                        if response_time > self.max_response_time_ms:
                            evidence.append(f"⚠️  Slow endpoint: {endpoint} responded in {response_time:.2f}ms")
                        else:
                            evidence.append(f"✅ Fast endpoint: {endpoint} responded in {response_time:.2f}ms")
                            
                except Exception as e:
                    evidence.append(f"❌ Endpoint failed: {endpoint} - {str(e)}")
                    metrics.append(MetricData(
                        name="http_requests_total",
                        value=1,
                        timestamp=datetime.now(),
                        tags={"endpoint": endpoint, "method": method, "status_code": "error"},
                        unit="count"
                    ))
            
            # Check if metrics are being collected
            if len(metrics) >= 5:
                evidence.append(f"✅ Collected {len(metrics)} metric data points")
                score = 90.0
            else:
                evidence.append(f"⚠️  Only collected {len(metrics)} metric data points")
                score = 60.0
            
            return ObservabilityResult(
                test_name="api_endpoint_monitoring",
                passed=len([m for m in metrics if m.value <= self.max_response_time_ms]) >= len(metrics) * 0.8,
                score=score,
                message="API endpoint monitoring validation",
                metrics=metrics,
                evidence=evidence,
                timestamp=datetime.now(),
                recommendations=["Consider implementing metrics aggregation", "Add distributed tracing"]
            )
            
        except Exception as e:
            return ObservabilityResult(
                test_name="api_endpoint_monitoring",
                passed=False,
                score=0.0,
                message=f"Error testing API monitoring: {str(e)}",
                metrics=[],
                evidence=[f"❌ API monitoring test failed: {str(e)}"],
                timestamp=datetime.now(),
                recommendations=["Check API health and metrics collection"]
            )
    
    async def test_logging_comprehensive(self) -> ObservabilityResult:
        """Test comprehensive logging implementation"""
        try:
            evidence = []
            metrics = []
            
            # Test log endpoint
            logs_response = await self.session.get(f"{self.base_url}/api/logs")
            if logs_response.status == 200:
                logs_data = await logs_response.json()
                logs = logs_data.get('logs', [])
                
                evidence.append(f"✅ Log endpoint accessible, found {len(logs)} log entries")
                
                if logs:
                    # Analyze log levels
                    log_levels = {}
                    for log_entry in logs[:20]:  # Analyze first 20 logs
                        level = log_entry.get('level', 'unknown').upper()
                        log_levels[level] = log_levels.get(level, 0) + 1
                    
                    evidence.append(f"📊 Log levels distribution: {log_levels}")
                    
                    # Check for structured logging
                    structured_logs = 0
                    trace_ids = 0
                    timestamps = []
                    
                    for log_entry in logs[:20]:
                        if 'trace_id' in log_entry:
                            trace_ids += 1
                        if 'timestamp' in log_entry:
                            timestamps.append(log_entry['timestamp'])
                        if len(log_entry) > 3:  # More than just level, message, source
                            structured_logs += 1
                    
                    evidence.append(f"📊 Structured logs: {structured_logs}/{min(20, len(logs))}")
                    evidence.append(f"📊 Trace IDs present: {trace_ids}/{min(20, len(logs))}")
                    
                    # Record logging metrics
                    metrics.append(MetricData(
                        name="logs_total",
                        value=len(logs),
                        timestamp=datetime.now(),
                        tags={},
                        unit="count"
                    ))
                    
                    metrics.append(MetricData(
                        name="structured_logs_ratio",
                        value=(structured_logs / min(20, len(logs))) * 100,
                        timestamp=datetime.now(),
                        tags={},
                        unit="percent"
                    ))
                    
                    if log_levels.get('ERROR', 0) > 5:
                        evidence.append(f"⚠️  High error log count: {log_levels['ERROR']} errors")
                    
                    if trace_ids / min(20, len(logs)) > 0.8:
                        evidence.append("✅ Good distributed tracing coverage")
                    else:
                        evidence.append("⚠️  Low distributed tracing coverage")
                        
                    score = 80.0 if structured_logs > 10 else 60.0
                else:
                    evidence.append("⚠️  No recent log entries found")
                    score = 40.0
            else:
                evidence.append(f"❌ Log endpoint not accessible (status: {logs_response.status})")
                score = 20.0
            
            return ObservabilityResult(
                test_name="logging_comprehensive",
                passed=logs_response.status == 200,
                score=score,
                message="Comprehensive logging validation",
                metrics=metrics,
                evidence=evidence,
                timestamp=datetime.now(),
                recommendations=[
                    "Implement structured logging with JSON format",
                    "Add distributed tracing with trace/span IDs",
                    "Ensure log levels are properly categorized"
                ]
            )
            
        except Exception as e:
            return ObservabilityResult(
                test_name="logging_comprehensive",
                passed=False,
                score=0.0,
                message=f"Error testing logging: {str(e)}",
                metrics=[],
                evidence=[f"❌ Logging test failed: {str(e)}"],
                timestamp=datetime.now(),
                recommendations=["Check log collection and storage", "Verify log endpoint accessibility"]
            )
    
    async def test_metrics_collection(self) -> ObservabilityResult:
        """Test metrics collection and aggregation"""
        try:
            evidence = []
            metrics = []
            
            # Get system metrics
            system_metrics = self.collect_system_metrics()
            if system_metrics:
                evidence.append(f"✅ System metrics collected successfully")
                
                # Convert system metrics to MetricData objects
                for metric_name, value in system_metrics.items():
                    if metric_name != 'timestamp' and isinstance(value, (int, float)):
                        metrics.append(MetricData(
                            name=metric_name,
                            value=float(value),
                            timestamp=datetime.now(),
                            tags={"source": "system"},
                            unit=""
                        ))
            
            # Test metrics endpoint
            metrics_response = await self.session.get(f"{self.base_url}/api/metrics")
            if metrics_response.status == 200:
                metrics_data = await metrics_response.json()
                app_metrics = metrics_data.get('metrics', [])
                
                evidence.append(f"✅ Application metrics endpoint accessible, found {len(app_metrics)} metrics")
                
                # Check for expected metric types
                metric_types_found = set()
                for metric in app_metrics:
                    metric_type = metric.get('type', 'unknown')
                    metric_types_found.add(metric_type)
                    
                evidence.append(f"📊 Metric types found: {list(metric_types_found)}")
                
                # Check for specific CultivAR metrics
                business_metrics = []
                for metric in app_metrics:
                    name = metric.get('name', '').lower()
                    if any(keyword in name for keyword in ['plant', 'sensor', 'user', 'cultivar']):
                        business_metrics.append(metric)
                
                evidence.append(f"📊 Business metrics found: {len(business_metrics)}")
                
                # Record metric count
                metrics.append(MetricData(
                    name="application_metrics_count",
                    value=len(app_metrics),
                    timestamp=datetime.now(),
                    tags={},
                    unit="count"
                ))
                
                metrics.append(MetricData(
                    name="business_metrics_count",
                    value=len(business_metrics),
                    timestamp=datetime.now(),
                    tags={},
                    unit="count"
                ))
                
                score = min(100.0, (len(app_metrics) + len(business_metrics)) * 5)
            else:
                evidence.append(f"❌ Metrics endpoint not accessible (status: {metrics_response.status})")
                score = 30.0
            
            # Check for Prometheus metrics
            try:
                prometheus_response = await self.session.get(f"{self.base_url}/metrics")
                if prometheus_response.status == 200:
                    evidence.append("✅ Prometheus metrics endpoint accessible")
                    metrics.append(MetricData(
                        name="prometheus_metrics_available",
                        value=1,
                        timestamp=datetime.now(),
                        tags={},
                        unit="boolean"
                    ))
                else:
                    evidence.append("⚠️  Prometheus metrics endpoint not accessible")
            except:
                evidence.append("⚠️  Prometheus metrics endpoint unavailable")
            
            return ObservabilityResult(
                test_name="metrics_collection",
                passed=metrics_response.status == 200,
                score=score,
                message="Metrics collection validation",
                metrics=metrics,
                evidence=evidence,
                timestamp=datetime.now(),
                recommendations=[
                    "Implement Prometheus metrics endpoint",
                    "Add business-specific metrics for plants, sensors, users",
                    "Consider metrics aggregation and retention policies"
                ]
            )
            
        except Exception as e:
            return ObservabilityResult(
                test_name="metrics_collection",
                passed=False,
                score=0.0,
                message=f"Error testing metrics: {str(e)}",
                metrics=[],
                evidence=[f"❌ Metrics test failed: {str(e)}"],
                timestamp=datetime.now(),
                recommendations=["Check metrics collection service", "Verify metrics endpoint configuration"]
            )
    
    async def test_alerting_system(self) -> ObservabilityResult:
        """Test alerting and notification system"""
        try:
            evidence = []
            metrics = []
            
            # Test alerting configuration endpoint
            alerts_response = await self.session.get(f"{self.base_url}/api/alerts")
            if alerts_response.status == 200:
                alerts_data = await alerts_response.json()
                alerts = alerts_data.get('alerts', [])
                
                evidence.append(f"✅ Alerting endpoint accessible, found {len(alerts)} configured alerts")
                
                # Analyze alert configuration
                alert_severities = {}
                alert_metrics = {}
                
                for alert in alerts:
                    severity = alert.get('severity', 'unknown').lower()
                    alert_severities[severity] = alert_severities.get(severity, 0) + 1
                    
                    metric = alert.get('metric', 'unknown')
                    alert_metrics[metric] = alert_metrics.get(metric, 0) + 1
                
                evidence.append(f"📊 Alert severities: {alert_severities}")
                evidence.append(f"📊 Alert metrics: {list(alert_metrics.keys())}")
                
                # Check for required alert coverage
                required_coverage = 0
                for required_alert in self.required_alerts:
                    found = False
                    for alert in alerts:
                        if alert.get('metric') == required_alert['metric']:
                            found = True
                            break
                    if found:
                        required_coverage += 1
                
                coverage_percent = (required_coverage / len(self.required_alerts)) * 100
                evidence.append(f"📊 Required alert coverage: {coverage_percent:.1f}% ({required_coverage}/{len(self.required_alerts)})")
                
                # Test alert testing capability
                try:
                    test_alert_response = await self.session.post(f"{self.base_url}/api/alerts/test")
                    if test_alert_response.status in [200, 201]:
                        evidence.append("✅ Alert testing capability confirmed")
                    else:
                        evidence.append("⚠️  Alert testing not available")
                except:
                    evidence.append("⚠️  Alert testing capability not found")
                
                # Record alerting metrics
                metrics.append(MetricData(
                    name="alerts_configured",
                    value=len(alerts),
                    timestamp=datetime.now(),
                    tags={},
                    unit="count"
                ))
                
                metrics.append(MetricData(
                    name="alert_coverage_percent",
                    value=coverage_percent,
                    timestamp=datetime.now(),
                    tags={},
                    unit="percent"
                ))
                
                score = min(100.0, coverage_percent + (len(alerts) * 2))
            else:
                evidence.append(f"❌ Alerting endpoint not accessible (status: {alerts_response.status})")
                score = 20.0
            
            # Check for external alerting integration
            evidence.append("💡 Consider integrating with external alerting services (PagerDuty, Slack, email)")
            
            return ObservabilityResult(
                test_name="alerting_system",
                passed=alerts_response.status == 200,
                score=score,
                message="Alerting system validation",
                metrics=metrics,
                evidence=evidence,
                timestamp=datetime.now(),
                recommendations=[
                    "Implement comprehensive alerting rules",
                    "Set up external alerting integrations",
                    "Test alert delivery and escalation policies",
                    "Monitor alert fatigue and fine-tune thresholds"
                ]
            )
            
        except Exception as e:
            return ObservabilityResult(
                test_name="alerting_system",
                passed=False,
                score=0.0,
                message=f"Error testing alerting: {str(e)}",
                metrics=[],
                evidence=[f"❌ Alerting test failed: {str(e)}"],
                timestamp=datetime.now(),
                recommendations=["Check alerting service configuration", "Verify alert endpoint accessibility"]
            )
    
    async def test_dashboard_monitoring(self) -> ObservabilityResult:
        """Test monitoring dashboard functionality"""
        try:
            evidence = []
            metrics = []
            
            # Test dashboard endpoint
            dashboard_response = await self.session.get(f"{self.base_url}/api/dashboard/monitoring")
            if dashboard_response.status == 200:
                dashboard_data = await dashboard_response.json()
                widgets = dashboard_data.get('widgets', [])
                
                evidence.append(f"✅ Monitoring dashboard accessible with {len(widgets)} widgets")
                
                # Analyze dashboard widgets
                widget_types = {}
                for widget in widgets:
                    widget_type = widget.get('type', 'unknown')
                    widget_types[widget_type] = widget_types.get(widget_type, 0) + 1
                
                evidence.append(f"📊 Dashboard widget types: {widget_types}")
                
                # Check for key monitoring components
                essential_widgets = ['health', 'metrics', 'logs', 'alerts']
                found_widgets = []
                
                for widget in widgets:
                    widget_name = widget.get('name', '').lower()
                    for essential in essential_widgets:
                        if essential in widget_name:
                            found_widgets.append(essential)
                            break
                
                coverage_percent = (len(set(found_widgets)) / len(essential_widgets)) * 100
                evidence.append(f"📊 Essential widget coverage: {coverage_percent:.1f}%")
                
                # Test dashboard real-time updates
                try:
                    # Simulate dashboard data refresh
                    refresh_response = await self.session.post(f"{self.base_url}/api/dashboard/refresh")
                    if refresh_response.status in [200, 201]:
                        evidence.append("✅ Dashboard real-time updates supported")
                    else:
                        evidence.append("⚠️  Dashboard real-time updates not confirmed")
                except:
                    evidence.append("⚠️  Dashboard real-time updates capability not found")
                
                # Record dashboard metrics
                metrics.append(MetricData(
                    name="dashboard_widgets_count",
                    value=len(widgets),
                    timestamp=datetime.now(),
                    tags={},
                    unit="count"
                ))
                
                metrics.append(MetricData(
                    name="dashboard_coverage_percent",
                    value=coverage_percent,
                    timestamp=datetime.now(),
                    tags={},
                    unit="percent"
                ))
                
                score = min(100.0, len(widgets) * 3 + coverage_percent)
            else:
                evidence.append(f"❌ Monitoring dashboard not accessible (status: {dashboard_response.status})")
                score = 30.0
            
            # Check for Grafana or similar external dashboard integration
            evidence.append("💡 Consider integrating Grafana for advanced visualization")
            
            return ObservabilityResult(
                test_name="dashboard_monitoring",
                passed=dashboard_response.status == 200,
                score=score,
                message="Monitoring dashboard validation",
                metrics=metrics,
                evidence=evidence,
                timestamp=datetime.now(),
                recommendations=[
                    "Implement comprehensive monitoring dashboard",
                    "Add real-time data updates",
                    "Include key performance indicators",
                    "Consider external dashboard integration (Grafana)"
                ]
            )
            
        except Exception as e:
            return ObservabilityResult(
                test_name="dashboard_monitoring",
                passed=False,
                score=0.0,
                message=f"Error testing dashboard: {str(e)}",
                metrics=[],
                evidence=[f"❌ Dashboard test failed: {str(e)}"],
                timestamp=datetime.now(),
                recommendations=["Check dashboard service configuration", "Verify dashboard endpoint accessibility"]
            )
    
    async def test_performance_monitoring(self) -> ObservabilityResult:
        """Test performance monitoring and APM capabilities"""
        try:
            evidence = []
            metrics = []
            
            # Test APM endpoint if available
            apm_response = await self.session.get(f"{self.base_url}/api/apm")
            if apm_response.status == 200:
                apm_data = await apm_response.json()
                traces = apm_data.get('traces', [])
                
                evidence.append(f"✅ APM endpoint accessible, found {len(traces)} traces")
                
                # Analyze traces
                if traces:
                    trace_durations = []
                    trace_spans = []
                    
                    for trace in traces[:10]:  # Analyze first 10 traces
                        duration = trace.get('duration_ms', 0)
                        trace_durations.append(duration)
                        
                        spans = trace.get('spans', [])
                        trace_spans.append(len(spans))
                    
                    avg_duration = sum(trace_durations) / len(trace_durations)
                    avg_spans = sum(trace_spans) / len(trace_spans)
                    
                    evidence.append(f"📊 Average trace duration: {avg_duration:.2f}ms")
                    evidence.append(f"📊 Average spans per trace: {avg_spans:.1f}")
                    
                    if avg_duration > 1000:
                        evidence.append("⚠️  High trace duration detected")
                    
                    metrics.append(MetricData(
                        name="apm_traces_count",
                        value=len(traces),
                        timestamp=datetime.now(),
                        tags={},
                        unit="count"
                    ))
                    
                    metrics.append(MetricData(
                        name="apm_avg_duration_ms",
                        value=avg_duration,
                        timestamp=datetime.now(),
                        tags={},
                        unit="milliseconds"
                    ))
                
                score = min(100.0, len(traces) * 5)
            else:
                evidence.append(f"ℹ️  APM endpoint not available (status: {apm_response.status})")
                evidence.append("💡 Consider implementing Application Performance Monitoring")
                score = 40.0
            
            # Test application profiling capability
            try:
                profile_response = await self.session.get(f"{self.base_url}/api/profile")
                if profile_response.status == 200:
                    evidence.append("✅ Application profiling capability found")
                    metrics.append(MetricData(
                        name="profiling_available",
                        value=1,
                        timestamp=datetime.now(),
                        tags={},
                        unit="boolean"
                    ))
                else:
                    evidence.append("⚠️  Application profiling not available")
            except:
                evidence.append("⚠️  Application profiling endpoint not found")
            
            return ObservabilityResult(
                test_name="performance_monitoring",
                passed=True,  # APM is optional
                score=score,
                message="Performance monitoring validation",
                metrics=metrics,
                evidence=evidence,
                timestamp=datetime.now(),
                recommendations=[
                    "Implement Application Performance Monitoring (APM)",
                    "Add distributed tracing for microservices",
                    "Consider profiling and performance analysis tools",
                    "Monitor application hotspots and bottlenecks"
                ]
            )
            
        except Exception as e:
            return ObservabilityResult(
                test_name="performance_monitoring",
                passed=False,
                score=0.0,
                message=f"Error testing performance monitoring: {str(e)}",
                metrics=[],
                evidence=[f"❌ Performance monitoring test failed: {str(e)}"],
                timestamp=datetime.now(),
                recommendations=["Check APM service configuration", "Consider implementing performance monitoring"]
            )
    
    async def run_observability_validation(self) -> Dict[str, Any]:
        """Run comprehensive observability validation"""
        logger.info("Starting observability and monitoring validation")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "total_tests": 0,
            "passed_tests": 0,
            "overall_score": 0.0,
            "test_results": [],
            "system_metrics": {},
            "recommendations": []
        }
        
        # Collect current system metrics
        results["system_metrics"] = self.collect_system_metrics()
        
        # Run observability tests
        observability_tests = [
            ("API Endpoint Monitoring", self.test_api_endpoint_monitoring),
            ("Comprehensive Logging", self.test_logging_comprehensive),
            ("Metrics Collection", self.test_metrics_collection),
            ("Alerting System", self.test_alerting_system),
            ("Dashboard Monitoring", self.test_dashboard_monitoring),
            ("Performance Monitoring", self.test_performance_monitoring)
        ]
        
        results["total_tests"] = len(observability_tests)
        
        total_score = 0.0
        for test_name, test_function in observability_tests:
            try:
                logger.info(f"Running observability test: {test_name}")
                result = await test_function()
                
                results["test_results"].append({
                    "test_name": result.test_name,
                    "display_name": test_name,
                    "passed": result.passed,
                    "score": result.score,
                    "message": result.message,
                    "evidence": result.evidence,
                    "recommendations": result.recommendations,
                    "timestamp": result.timestamp.isoformat()
                })
                
                if result.passed:
                    results["passed_tests"] += 1
                
                total_score += result.score
                
            except Exception as e:
                logger.error(f"Error running test {test_name}: {str(e)}")
                results["test_results"].append({
                    "test_name": test_name.lower().replace(' ', '_'),
                    "display_name": test_name,
                    "passed": False,
                    "score": 0.0,
                    "message": f"Test execution error: {str(e)}",
                    "evidence": [f"❌ Test failed: {str(e)}"],
                    "recommendations": ["Check test implementation and system state"],
                    "timestamp": datetime.now().isoformat()
                })
        
        # Calculate overall score
        if results["total_tests"] > 0:
            results["overall_score"] = total_score / results["total_tests"]
        else:
            results["overall_score"] = 0.0
        
        # Generate comprehensive recommendations
        if results["overall_score"] >= 80:
            results["recommendations"].append("✅ Excellent observability - system ready for production")
        elif results["overall_score"] >= 60:
            results["recommendations"].append("⚠️  Good observability - improvements needed for production")
        else:
            results["recommendations"].append("❌ Limited observability - significant work required")
        
        # Category-specific recommendations
        test_categories = {}
        for result in results["test_results"]:
            category = result["display_name"]
            test_categories[category] = {
                "passed": result["passed"],
                "score": result["score"]
            }
        
        # API Monitoring recommendations
        if test_categories.get("API Endpoint Monitoring", {}).get("score", 0) < 70:
            results["recommendations"].append("⚡ Improve API monitoring and response time tracking")
        
        # Logging recommendations
        if test_categories.get("Comprehensive Logging", {}).get("score", 0) < 70:
            results["recommendations"].append("📝 Enhance logging with structured format and distributed tracing")
        
        # Metrics recommendations
        if test_categories.get("Metrics Collection", {}).get("score", 0) < 70:
            results["recommendations"].append("📊 Implement comprehensive metrics collection and aggregation")
        
        # Alerting recommendations
        if test_categories.get("Alerting System", {}).get("score", 0) < 70:
            results["recommendations"].append("🚨 Set up comprehensive alerting with proper escalation")
        
        # Dashboard recommendations
        if test_categories.get("Dashboard Monitoring", {}).get("score", 0) < 70:
            results["recommendations"].append("📈 Build comprehensive monitoring dashboard with real-time updates")
        
        # Performance monitoring recommendations
        if test_categories.get("Performance Monitoring", {}).get("score", 0) < 70:
            results["recommendations"].append("⚡ Consider implementing APM and performance profiling")
        
        # External tool recommendations
        results["recommendations"].append("🔧 Consider integrating with external monitoring tools:")
        results["recommendations"].append("   - Prometheus + Grafana for metrics visualization")
        results["recommendations"].append("   - ELK Stack (Elasticsearch, Logstash, Kibana) for log analysis")
        results["recommendations"].append("   - Jaeger or Zipkin for distributed tracing")
        results["recommendations"].append("   - New Relic or DataDog for APM")
        
        logger.info(f"✅ Observability validation completed - Overall score: {results['overall_score']:.1f}%")
        return results

def main():
    """CLI interface for observability validation"""
    parser = argparse.ArgumentParser(description="Observability and Monitoring Testing Framework")
    parser.add_argument("--url", required=True, help="Base URL for testing")
    parser.add_argument("--token", help="JWT authentication token")
    parser.add_argument("--output", help="Output file for results (JSON)")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run validation
    async def run():
        async with ObservabilityValidator(args.url, args.token) as validator:
            results = await validator.run_observability_validation()
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            logger.info(f"Results saved to {args.output}")
        else:
            print(json.dumps(results, indent=2, default=str))
        
        return results
    
    results = asyncio.run(run())
    
    # Exit with appropriate code
    if results["overall_score"] >= 60:  # 60% threshold
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure

if __name__ == "__main__":
    main()