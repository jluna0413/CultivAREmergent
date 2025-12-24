# Mock OWASP ZAP Scanner for CultivAR
# Simulated security scanning without requiring Docker

import json
import time
import random
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

@dataclass
class MockZAPAlert:
    """Mock ZAP Alert information"""
    pluginId: str
    alert: str
    name: str
    riskcode: str
    confidence: str
    riskdesc: str
    desc: str
    uri: str
    param: str
    attack: str
    evidence: str
    solution: str
    reference: str
    cweid: str
    wascid: str
    sourceid: str

@dataclass
class MockZAPScanResult:
    """Mock ZAP scan result summary"""
    scan_id: str
    scan_type: str
    target_url: str
    status: str
    progress: int
    start_time: datetime
    end_time: datetime
    alerts: List[MockZAPAlert]
    statistics: Dict[str, Any]

class MockOWASPTapRunner:
    """Mock OWASP ZAP integration for CultivAR security scanning"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {
            "target_urls": [
                "http://localhost:8000",
                "http://localhost:8000/api/v2/auth",
                "http://localhost:8000/api/v2/dashboard", 
                "http://localhost:8000/api/v2/plants",
                "http://localhost:8000/api/v2/sensors",
                "http://localhost:5000",
                "http://localhost:3000"
            ]
        }
        
    def is_zap_running(self) -> bool:
        """Mock check if OWASP ZAP is running"""
        return True
    
    def generate_mock_alerts(self, target_url: str) -> List[MockZAPAlert]:
        """Generate realistic mock security alerts"""
        
        # Common security vulnerabilities to simulate
        alert_types = [
            {
                "pluginId": "40018",
                "alert": "Anti CSRF Token Missing",
                "name": "Anti CSRF Token Missing",
                "riskcode": "2",
                "confidence": "3",
                "riskdesc": "Low (Medium)",
                "desc": "No Anti CSRF token was found in a HTML Form.",
                "solution": "Use a random anti-CSRF token for each session.",
                "cweid": "352",
                "wascid": "9"
            },
            {
                "pluginId": "40012",
                "alert": "Cookie No SameSite Attribute",
                "name": "Cookie No SameSite Attribute",
                "riskcode": "2",
                "confidence": "2",
                "riskdesc": "Low (Medium)",
                "desc": "A cookie has been set without the SameSite attribute.",
                "solution": "Add a SameSite attribute to cookie.",
                "cweid": "352",
                "wascid": "9"
            },
            {
                "pluginId": "40028",
                "alert": "Incomplete or No Cache-control and Pragma HTTP Header Set",
                "name": "Missing Cache-Control Headers",
                "riskcode": "2",
                "confidence": "2",
                "riskdesc": "Low (Medium)",
                "desc": "The cache-control and pragma HTTP header have not been set properly.",
                "solution": "Ensure cache headers are set appropriately.",
                "cweid": "525",
                "wascid": "13"
            },
            {
                "pluginId": "40040",
                "alert": "User controlled charset",
                "name": "User Controlled Charset",
                "riskcode": "3",
                "confidence": "3",
                "riskdesc": "Medium (High)",
                "desc": "User controlled charset in HTTP header.",
                "solution": "Restrict charset to allowed values.",
                "cweid": "94",
                "wascid": "20"
            },
            {
                "pluginId": "40032",
                "alert": "User controllable javascript event",
                "name": "User Controllable Event Handlers",
                "riskcode": "3",
                "confidence": "2",
                "riskdesc": "Medium (High)",
                "desc": "User controllable javascript event handlers.",
                "solution": "Sanitize user input for event handlers.",
                "cweid": "79",
                "wascid": "8"
            }
        ]
        
        # Simulate based on target URL type
        alerts = []
        
        # API endpoints get fewer alerts (better security)
        if "/api/" in target_url:
            num_alerts = random.randint(0, 3)
        # Web interfaces get more alerts
        else:
            num_alerts = random.randint(1, 5)
            
        selected_alerts = random.sample(alert_types, min(num_alerts, len(alert_types)))
        
        for i, alert_data in enumerate(selected_alerts):
            alert = MockZAPAlert(
                pluginId=alert_data["pluginId"],
                alert=alert_data["alert"],
                name=alert_data["name"],
                riskcode=alert_data["riskcode"],
                confidence=alert_data["confidence"],
                riskdesc=alert_data["riskdesc"],
                desc=alert_data["desc"],
                uri=target_url,
                param=f"param_{i}",
                attack="GET",
                evidence="Sample evidence",
                solution=alert_data["solution"],
                reference="https://owasp.org/www-community/attacks/",
                cweid=alert_data["cweid"],
                wascid=alert_data["wascid"],
                sourceid="4"
            )
            alerts.append(alert)
        
        return alerts
    
    def run_baseline_scan(self, target_url: str) -> MockZAPScanResult:
        """Run mock OWASP ZAP baseline scan"""
        print(f"\nScanning {target_url}...")
        
        # Simulate scan progress
        for progress in range(0, 101, 10):
            print(f"  Scan progress: {progress}%")
            time.sleep(0.1)  # Simulate scanning time
        
        # Generate mock alerts
        alerts = self.generate_mock_alerts(target_url)
        
        # Calculate statistics
        stats = self._calculate_statistics(alerts)
        
        print(f"  SUCCESS: {target_url}: {stats['total']} alerts found")
        print(f"    High: {stats['critical_issues']}, Medium: {stats['medium_issues']}, Low: {stats['low_issues']}")
        
        return MockZAPScanResult(
            scan_id=f"scan_{random.randint(1000, 9999)}",
            scan_type="baseline",
            target_url=target_url,
            status="complete",
            progress=100,
            start_time=datetime.now(),
            end_time=datetime.now(),
            alerts=alerts,
            statistics=stats
        )
    
    def _calculate_statistics(self, alerts: List[MockZAPAlert]) -> Dict[str, Any]:
        """Calculate mock scan statistics"""
        if not alerts:
            return {"total": 0}
        
        risk_levels = {"High": 0, "Medium": 0, "Low": 0, "Informational": 0}
        
        for alert in alerts:
            risk_desc = alert.riskdesc.lower()
            if "high" in risk_desc:
                risk_levels["High"] += 1
            elif "medium" in risk_desc:
                risk_levels["Medium"] += 1
            elif "low" in risk_desc:
                risk_levels["Low"] += 1
            else:
                risk_levels["Informational"] += 1
        
        return {
            "total": len(alerts),
            "by_risk": risk_levels,
            "critical_issues": risk_levels["High"],
            "medium_issues": risk_levels["Medium"],
            "low_issues": risk_levels["Low"]
        }

class MockCultivarZAPScanner:
    """Mock CultivAR-specific ZAP scanning orchestrator"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.tap_runner = MockOWASPTapRunner(self.config)
        self.results: List[MockZAPScanResult] = []
        
    def run_comprehensive_security_scan(self) -> Dict[str, Any]:
        """Run comprehensive mock security scan across all CultivAR endpoints"""
        print("Starting Mock OWASP ZAP Security Scan...")
        print("NOTE: Running simulated scan without Docker (environment limitations)")
        
        target_urls = self.config.get("target_urls", [
            "http://localhost:8000",
            "http://localhost:8000/api/v2/auth",
            "http://localhost:8000/api/v2/dashboard", 
            "http://localhost:8000/api/v2/plants",
            "http://localhost:8000/api/v2/sensors",
            "http://localhost:5000",
            "http://localhost:3000"
        ])
        
        print(f"Found {len(target_urls)} targets to scan")
        
        # Run baseline scans on all targets
        for target_url in target_urls:
            try:
                result = self.tap_runner.run_baseline_scan(target_url)
                self.results.append(result)
            except Exception as e:
                print(f"  FAILED to scan {target_url}: {str(e)}")
        
        # Generate comprehensive summary
        summary = self._generate_zap_summary(self.results)
        
        return {
            "summary": summary,
            "scan_results": [asdict(result) for result in self.results],
            "timestamp": datetime.now().isoformat(),
            "targets_scanned": len(target_urls),
            "total_alerts": sum(r.statistics.get("total", 0) for r in self.results),
            "scan_mode": "mock_simulation"
        }
    
    def _generate_zap_summary(self, results: List[MockZAPScanResult]) -> Dict[str, Any]:
        """Generate mock ZAP scan summary"""
        total_scans = len(results)
        successful_scans = len([r for r in results if r.status == "complete"])
        failed_scans = total_scans - successful_scans
        
        # Aggregate statistics
        total_alerts = 0
        high_risk = 0
        medium_risk = 0
        low_risk = 0
        
        for result in results:
            if result.statistics:
                total_alerts += result.statistics.get("total", 0)
                high_risk += result.statistics.get("critical_issues", 0)
                medium_risk += result.statistics.get("medium_issues", 0)
                low_risk += result.statistics.get("low_issues", 0)
        
        # Calculate security score (0-100)
        if total_alerts == 0:
            security_score = 100.0
        else:
            # Deduct points based on risk levels
            score = 100.0
            score -= (high_risk * 10.0)  # High risk: 10 points each
            score -= (medium_risk * 5.0)  # Medium risk: 5 points each
            score -= (low_risk * 2.0)  # Low risk: 2 points each
            security_score = max(0.0, score)
        
        return {
            "total_scans": total_scans,
            "successful_scans": successful_scans,
            "failed_scans": failed_scans,
            "success_rate": (successful_scans / total_scans * 100) if total_scans > 0 else 0,
            "total_alerts": total_alerts,
            "high_risk_alerts": high_risk,
            "medium_risk_alerts": medium_risk,
            "low_risk_alerts": low_risk,
            "security_score": security_score,
            "risk_distribution": {
                "critical": high_risk,
                "medium": medium_risk,
                "low": low_risk,
                "informational": total_alerts - high_risk - medium_risk - low_risk
            }
        }
    
    def save_detailed_report(self, filename: str = "cultivar_zap_security_report.json"):
        """Save detailed mock ZAP report"""
        report_data = {
            "scan_summary": self._generate_zap_summary(self.results),
            "detailed_results": [asdict(result) for result in self.results],
            "configuration": self.config,
            "scan_timestamp": datetime.now().isoformat(),
            "owasp_zap_version": "Mock Simulation v1.0",
            "scan_mode": "mock_docker_unavailable"
        }
        
        with open(filename, "w") as f:
            json.dump(report_data, f, indent=2, default=str)
        
        print(f"\nDetailed report saved to: {filename}")

def main():
    """Main mock ZAP scanning function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CultivAR Mock OWASP ZAP Security Scanner")
    parser.add_argument("--scan", action="store_true", help="Run security scan")
    parser.add_argument("--all", action="store_true", help="Run complete scan")
    parser.add_argument("--target", help="Specific target URL to scan")
    parser.add_argument("--output", default="cultivar_zap_report.json", help="Output report filename")
    
    args = parser.parse_args()
    
    if args.scan or args.all:
        scanner = MockCultivarZAPScanner()
        
        # Use specific target if provided
        if args.target:
            scanner.config["target_urls"] = [args.target]
        
        try:
            results = scanner.run_comprehensive_security_scan()
            scanner.save_detailed_report(args.output)
            
            # Print summary
            summary = results["summary"]
            print(f"\n{'='*60}")
            print(f"OWASP ZAP SECURITY SCAN SUMMARY (MOCK)")
            print(f"{'='*60}")
            print(f"Targets Scanned: {summary['total_scans']}")
            print(f"Successful Scans: {summary['successful_scans']}")
            print(f"Failed Scans: {summary['failed_scans']}")
            print(f"Total Alerts: {summary['total_alerts']}")
            print(f"High Risk: {summary['high_risk_alerts']}")
            print(f"Medium Risk: {summary['medium_risk_alerts']}")
            print(f"Low Risk: {summary['low_risk_alerts']}")
            print(f"Security Score: {summary['security_score']:.1f}/100")
            
            if summary['security_score'] < 70:
                print("\nWARNING: SECURITY SCORE IS BELOW 70 - IMMEDIATE ATTENTION REQUIRED")
            elif summary['security_score'] < 85:
                print("\nWARNING: SECURITY SCORE BELOW 85 - REVIEW RECOMMENDED")
            else:
                print("\nGOOD SECURITY POSTURE")
                
        except Exception as e:
            print(f"Scan failed: {str(e)}")
            return 1
    
    return 0

if __name__ == "__main__":
    exit(main())