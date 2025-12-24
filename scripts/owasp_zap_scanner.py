# CultivAR OWASP ZAP Integration
# Automated security scanning using OWASP ZAP for comprehensive vulnerability assessment

import subprocess
import json
import time
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging

# OWASP ZAP Configuration
ZAP_CONFIG = {
    "zap_api_url": "http://localhost:8080",
    "zap_api_key": "zap_api_key_12345",
    "target_url": "http://localhost:8000",  # FastAPI backend
    "target_urls": [
        "http://localhost:8000",
        "http://localhost:8000/api/v2/auth",
        "http://localhost:8000/api/v2/dashboard", 
        "http://localhost:8000/api/v2/plants",
        "http://localhost:8000/api/v2/sensors",
        "http://localhost:5000",  # Flask legacy web interface
        "http://localhost:3000"   # Flutter web interface (if running)
    ],
    "scan_policies": {
        "baseline": "baseline-scan",
        "full": "full-scan",
        "api": "api-scan"
    }
}

@dataclass
class ZAPAlert:
    """ZAP Alert information"""
    pluginId: str
    alert: str
    name: str
    riskcode: str
    confidence: str
    riskdesc: str
    confidence: str
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
class ZAPScanResult:
    """ZAP scan result summary"""
    scan_id: str
    scan_type: str
    target_url: str
    status: str  # running, complete, error
    progress: int  # 0-100
    start_time: datetime
    end_time: Optional[datetime] = None
    alerts: List[ZAPAlert] = None
    statistics: Dict[str, Any] = None

class OWASPTapRunner:
    """OWASP ZAP integration for CultivAR security scanning"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or ZAP_CONFIG
        self.logger = logging.getLogger(__name__)
        self.api_url = f"{self.config['zap_api_url']}/JSON"
        self.api_headers = {
            "X-ZAP-API-Key": self.config["zap_api_key"]
        }
        
    def is_zap_running(self) -> bool:
        """Check if OWASP ZAP is running"""
        try:
            response = requests.get(f"{self.config['zap_api_url']}/JSON/core/version/")
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def start_zap_scan(self, target_url: str, scan_type: str = "baseline") -> str:
        """Start OWASP ZAP scan"""
        try:
            # Get scan policy
            scan_policy = self.config["scan_policies"].get(scan_type, "baseline-scan")
            
            # Start active scan
            params = {
                "url": target_url,
                "recurse": "True",
                "scanPolicyName": scan_policy,
                "method": "GET",
                "postData": "",
                "contextId": ""
            }
            
            response = requests.get(
                f"{self.api_url}/ascan/action/scan/",
                params=params,
                headers=self.api_headers
            )
            
            if response.status_code == 200:
                scan_id = response.text.strip('"')
                self.logger.info(f"Started {scan_type} scan for {target_url}: {scan_id}")
                return scan_id
            else:
                raise Exception(f"Failed to start scan: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Error starting ZAP scan: {str(e)}")
            raise
    
    def get_scan_status(self, scan_id: str) -> Dict[str, Any]:
        """Get scan status"""
        try:
            response = requests.get(
                f"{self.api_url}/ascan/view/status/",
                params={"scanId": scan_id},
                headers=self.api_headers
            )
            
            if response.status_code == 200:
                return {"scanId": scan_id, "status": response.text.strip('"')}
            else:
                raise Exception(f"Failed to get scan status: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Error getting scan status: {str(e)}")
            raise
    
    def wait_for_scan_completion(self, scan_id: str, timeout: int = 3600) -> bool:
        """Wait for scan to complete"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                status_info = self.get_scan_status(scan_id)
                status = status_info.get("status", "")
                
                if status == "100":
                    self.logger.info(f"Scan {scan_id} completed")
                    return True
                elif status == "error":
                    self.logger.error(f"Scan {scan_id} encountered error")
                    return False
                else:
                    progress = int(status)
                    print(f"\rScan progress: {progress}%", end="", flush=True)
                    time.sleep(5)  # Check every 5 seconds
                    
            except Exception as e:
                self.logger.error(f"Error checking scan status: {str(e)}")
                time.sleep(5)
        
        self.logger.warning(f"Scan {scan_id} timed out after {timeout} seconds")
        return False
    
    def get_scan_alerts(self, base_url: str = None) -> List[ZAPAlert]:
        """Get alerts from ZAP scan"""
        try:
            params = {"baseurl": base_url} if base_url else {}
            
            response = requests.get(
                f"{self.api_url}/core/view/alerts/",
                params=params,
                headers=self.api_headers
            )
            
            if response.status_code == 200:
                alerts_data = response.json()
                alerts = []
                
                for alert_data in alerts_data.get("alerts", []):
                    alert = ZAPAlert(
                        pluginId=alert_data.get("pluginId", ""),
                        alert=alert_data.get("alert", ""),
                        name=alert_data.get("name", ""),
                        riskcode=alert_data.get("riskcode", ""),
                        confidence=alert_data.get("confidence", ""),
                        riskdesc=alert_data.get("riskdesc", ""),
                        desc=alert_data.get("desc", ""),
                        uri=alert_data.get("uri", ""),
                        param=alert_data.get("param", ""),
                        attack=alert_data.get("attack", ""),
                        evidence=alert_data.get("evidence", ""),
                        solution=alert_data.get("solution", ""),
                        reference=alert_data.get("reference", ""),
                        cweid=alert_data.get("cweid", ""),
                        wascid=alert_data.get("wascid", ""),
                        sourceid=alert_data.get("sourceid", "")
                    )
                    alerts.append(alert)
                
                return alerts
            else:
                raise Exception(f"Failed to get alerts: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Error getting alerts: {str(e)}")
            raise
    
    def run_baseline_scan(self, target_url: str) -> ZAPScanResult:
        """Run OWASP ZAP baseline scan"""
        scan_id = self.start_zap_scan(target_url, "baseline")
        
        # Wait for completion
        start_time = datetime.now()
        completed = self.wait_for_scan_completion(scan_id)
        end_time = datetime.now()
        
        # Get alerts
        alerts = self.get_scan_alerts(target_url)
        
        return ZAPScanResult(
            scan_id=scan_id,
            scan_type="baseline",
            target_url=target_url,
            status="complete" if completed else "error",
            progress=100 if completed else 0,
            start_time=start_time,
            end_time=end_time,
            alerts=alerts,
            statistics=self._calculate_statistics(alerts)
        )
    
    def run_full_scan(self, target_url: str) -> ZAPScanResult:
        """Run OWASP ZAP full scan"""
        scan_id = self.start_zap_scan(target_url, "full")
        
        # Wait for completion
        start_time = datetime.now()
        completed = self.wait_for_scan_completion(scan_id)
        end_time = datetime.now()
        
        # Get alerts
        alerts = self.get_scan_alerts(target_url)
        
        return ZAPScanResult(
            scan_id=scan_id,
            scan_type="full",
            target_url=target_url,
            status="complete" if completed else "error",
            progress=100 if completed else 0,
            start_time=start_time,
            end_time=end_time,
            alerts=alerts,
            statistics=self._calculate_statistics(alerts)
        )
    
    def _calculate_statistics(self, alerts: List[ZAPAlert]) -> Dict[str, Any]:
        """Calculate scan statistics"""
        if not alerts:
            return {"total": 0}
        
        risk_levels = {"High": 0, "Medium": 0, "Low": 0, "Informational": 0}
        confidence_levels = {"High": 0, "Medium": 0, "Low": 0}
        
        for alert in alerts:
            # Risk level
            risk_desc = alert.riskdesc.lower()
            if "high" in risk_desc:
                risk_levels["High"] += 1
            elif "medium" in risk_desc:
                risk_levels["Medium"] += 1
            elif "low" in risk_desc:
                risk_levels["Low"] += 1
            else:
                risk_levels["Informational"] += 1
            
            # Confidence level
            confidence = alert.confidence.lower()
            if "high" in confidence:
                confidence_levels["High"] += 1
            elif "medium" in confidence:
                confidence_levels["Medium"] += 1
            else:
                confidence_levels["Low"] += 1
        
        return {
            "total": len(alerts),
            "by_risk": risk_levels,
            "by_confidence": confidence_levels,
            "critical_issues": risk_levels["High"],
            "medium_issues": risk_levels["Medium"],
            "low_issues": risk_levels["Low"]
        }

class CultivarZAPScanner:
    """CultivAR-specific ZAP scanning orchestrator"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or ZAP_CONFIG
        self.tap_runner = OWASPTapRunner(self.config)
        self.results: List[ZAPScanResult] = []
        
    def run_comprehensive_security_scan(self) -> Dict[str, Any]:
        """Run comprehensive security scan across all CultivAR endpoints"""
        print("🔍 Starting OWASP ZAP Security Scan...")
        
        if not self.tap_runner.is_zap_running():
            raise Exception("OWASP ZAP is not running. Please start ZAP and try again.")
        
        print(f"Found {len(self.config['target_urls'])} targets to scan")
        
        # Run baseline scans on all targets
        for target_url in self.config["target_urls"]:
            try:
                print(f"\n📊 Scanning {target_url}...")
                result = self.tap_runner.run_baseline_scan(target_url)
                self.results.append(result)
                
                # Print immediate results
                stats = result.statistics
                print(f"  ✓ {target_url}: {stats['total']} alerts found")
                print(f"    High: {stats['critical_issues']}, Medium: {stats['medium_issues']}, Low: {stats['low_issues']}")
                
            except Exception as e:
                print(f"  ✗ Failed to scan {target_url}: {str(e)}")
                # Create error result
                error_result = ZAPScanResult(
                    scan_id="error",
                    scan_type="baseline",
                    target_url=target_url,
                    status="error",
                    progress=0,
                    start_time=datetime.now(),
                    alerts=[],
                    statistics={"total": 0, "error": str(e)}
                )
                self.results.append(error_result)
        
        # Generate comprehensive summary
        summary = self._generate_zap_summary(self.results)
        
        return {
            "summary": summary,
            "scan_results": [asdict(result) for result in self.results],
            "timestamp": datetime.now().isoformat(),
            "targets_scanned": len(self.config["target_urls"]),
            "total_alerts": sum(r.statistics.get("total", 0) for r in self.results)
        }
    
    def _generate_zap_summary(self, results: List[ZAPScanResult]) -> Dict[str, Any]:
        """Generate ZAP scan summary"""
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
        """Save detailed ZAP report"""
        report_data = {
            "scan_summary": self._generate_zap_summary(self.results),
            "detailed_results": [asdict(result) for result in self.results],
            "configuration": self.config,
            "scan_timestamp": datetime.now().isoformat(),
            "owasp_zap_version": self._get_zap_version()
        }
        
        with open(filename, "w") as f:
            json.dump(report_data, f, indent=2, default=str)
        
        print(f"\n📄 Detailed report saved to: {filename}")
    
    def _get_zap_version(self) -> str:
        """Get OWASP ZAP version"""
        try:
            response = requests.get(f"{self.config['zap_api_url']}/JSON/core/version/")
            return response.text.strip('"') if response.status_code == 200 else "Unknown"
        except:
            return "Unknown"

# ==================== Command Line Interface ====================

def install_zap_docker():
    """Install and run OWASP ZAP using Docker"""
    print("🐳 Installing OWASP ZAP via Docker...")
    
    # Pull OWASP ZAP Docker image
    subprocess.run([
        "docker", "pull", "owasp/zap2docker-stable"
    ], check=True)
    
    print("✓ OWASP ZAP Docker image downloaded")

def start_zap_daemon():
    """Start OWASP ZAP in daemon mode"""
    print("🚀 Starting OWASP ZAP daemon...")
    
    # Start ZAP daemon in background
    cmd = [
        "docker", "run", "-d",
        "--name", "zap-daemon",
        "-p", "8080:8080",
        "owasp/zap2docker-stable",
        "zap.sh", "-daemon", "-config", "api.key=zap_api_key_12345"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✓ OWASP ZAP daemon started (container: zap-daemon)")
        
        # Wait for ZAP to be ready
        print("⏳ Waiting for ZAP to be ready...")
        for i in range(30):
            try:
                response = requests.get("http://localhost:8080/JSON/core/version/")
                if response.status_code == 200:
                    print("✓ OWASP ZAP is ready")
                    return True
            except:
                pass
            time.sleep(2)
        
        print("⚠️ ZAP may still be starting. Check manually with: curl http://localhost:8080/JSON/core/version/")
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to start ZAP: {e}")
        return False

def main():
    """Main ZAP scanning function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CultivAR OWASP ZAP Security Scanner")
    parser.add_argument("--install", action="store_true", help="Install OWASP ZAP Docker image")
    parser.add_argument("--start", action="store_true", help="Start ZAP daemon")
    parser.add_argument("--scan", action="store_true", help="Run security scan")
    parser.add_argument("--all", action="store_true", help="Install, start, and scan")
    parser.add_argument("--target", help="Specific target URL to scan")
    parser.add_argument("--output", default="cultivar_zap_report.json", help="Output report filename")
    
    args = parser.parse_args()
    
    if args.install or args.all:
        install_zap_docker()
    
    if args.start or args.all:
        start_zap_daemon()
        time.sleep(5)  # Wait for daemon to be ready
    
    if args.scan or args.all:
        scanner = CultivarZAPScanner()
        
        # Use specific target if provided
        if args.target:
            scanner.config["target_urls"] = [args.target]
        
        try:
            results = scanner.run_comprehensive_security_scan()
            scanner.save_detailed_report(args.output)
            
            # Print summary
            summary = results["summary"]
            print(f"\n{'='*60}")
            print(f"🔍 OWASP ZAP SECURITY SCAN SUMMARY")
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
                print("\n⚠️ SECURITY SCORE IS BELOW 70 - IMMEDIATE ATTENTION REQUIRED")
            elif summary['security_score'] < 85:
                print("\n⚠️ SECURITY SCORE BELOW 85 - REVIEW RECOMMENDED")
            else:
                print("\n✓ GOOD SECURITY POSTURE")
                
        except Exception as e:
            print(f"✗ Scan failed: {str(e)}")
            return 1
    
    return 0

if __name__ == "__main__":
    exit(main())