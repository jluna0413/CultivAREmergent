"""
🔄 CONTINUOUS VALIDATION PIPELINE FOR CULTIVAR APPLICATION
Automated CI/CD integration for comprehensive validation testing
"""

import asyncio
import json
import os
import sys
import time
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import logging

@dataclass
class ValidationRun:
    """Represents a validation run"""
    timestamp: str
    test_type: str  # security, iot, e2e
    status: str  # passed, failed, error
    duration_seconds: float
    details: str
    issues_found: List[str]
    recommendations: List[str]

class CultivarValidationPipeline:
    """Continuous validation pipeline orchestrator"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.validation_runs: List[ValidationRun] = []
        self.logger = logging.getLogger(__name__)
        
    async def run_complete_validation_suite(self, 
                                          include_security: bool = True,
                                          include_iot: bool = True,
                                          include_e2e: bool = True,
                                          output_dir: str = "validation_reports") -> Dict[str, Any]:
        """Run complete validation suite with all test types"""
        print("🚀 Starting CultivAR Continuous Validation Pipeline")
        print(f"📍 Testing application at: {self.base_url}")
        print(f"⏰ Started at: {datetime.utcnow().isoformat()}")
        print("-" * 60)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        validation_results = {}
        
        try:
            # Phase 1: Security Validation
            if include_security:
                print("\n🔐 Running Security Validation...")
                security_start = time.time()
                security_result = await self._run_security_validation(output_dir)
                security_duration = time.time() - security_start
                
                validation_results["security"] = security_result
                self.validation_runs.append(ValidationRun(
                    timestamp=datetime.utcnow().isoformat(),
                    test_type="security",
                    status=security_result["status"],
                    duration_seconds=security_duration,
                    details=security_result["summary"]["details"],
                    issues_found=security_result.get("critical_issues", []),
                    recommendations=security_result.get("recommendations", [])
                ))
                
                print(f"✅ Security validation completed in {security_duration:.2f}s")
            
            # Phase 2: IoT Integration Validation
            if include_iot:
                print("\n📡 Running IoT Integration Validation...")
                iot_start = time.time()
                iot_result = await self._run_iot_validation(output_dir)
                iot_duration = time.time() - iot_start
                
                validation_results["iot"] = iot_result
                self.validation_runs.append(ValidationRun(
                    timestamp=datetime.utcnow().isoformat(),
                    test_type="iot",
                    status=iot_result["status"],
                    duration_seconds=iot_duration,
                    details=iot_result["summary"]["details"],
                    issues_found=iot_result.get("iot_issues", []),
                    recommendations=iot_result.get("recommendations", [])
                ))
                
                print(f"✅ IoT validation completed in {iot_duration:.2f}s")
            
            # Phase 3: End-to-End Validation
            if include_e2e:
                print("\n🔄 Running End-to-End Validation...")
                e2e_start = time.time()
                e2e_result = await self._run_e2e_validation(output_dir)
                e2e_duration = time.time() - e2e_start
                
                validation_results["e2e"] = e2e_result
                self.validation_runs.append(ValidationRun(
                    timestamp=datetime.utcnow().isoformat(),
                    test_type="e2e",
                    status=e2e_result["status"],
                    duration_seconds=e2e_duration,
                    details=e2e_result["summary"]["details"],
                    issues_found=e2e_result.get("e2e_issues", []),
                    recommendations=e2e_result.get("recommendations", [])
                ))
                
                print(f"✅ E2E validation completed in {e2e_duration:.2f}s")
            
            # Phase 4: Generate Consolidated Report
            print("\n📊 Generating Consolidated Validation Report...")
            consolidated_report = self._generate_consolidated_report(validation_results, output_dir)
            
            # Phase 5: Determine Overall Status
            overall_status = self._determine_overall_status(validation_results)
            
            # Save consolidated report
            report_path = os.path.join(output_dir, f"consolidated_validation_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json")
            with open(report_path, 'w') as f:
                json.dump(consolidated_report, f, indent=2)
            
            print(f"\n📄 Consolidated report saved to: {report_path}")
            
            # Display summary
            self._display_validation_summary(consolidated_report)
            
            return consolidated_report
            
        except Exception as e:
            self.logger.error(f"Validation pipeline failed: {e}")
            return {"error": str(e), "status": "pipeline_error"}
    
    async def _run_security_validation(self, output_dir: str) -> Dict[str, Any]:
        """Run security validation tests"""
        try:
            # Import and run security validator
            sys.path.append('tests/security')
            from cultivar_security_validator import CultivarSecurityValidator
            
            async with CultivarSecurityValidator(base_url=self.base_url) as validator:
                report = await validator.run_all_security_tests()
                
                # Save individual report
                security_report_path = os.path.join(output_dir, f"security_validation_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json")
                with open(security_report_path, 'w') as f:
                    json.dump(report, f, indent=2)
                
                # Determine status
                critical_failures = report["summary"]["critical_failures"]
                high_failures = report["summary"]["high_failures"]
                
                if critical_failures > 0:
                    status = "failed"
                elif high_failures > 0:
                    status = "warning"
                else:
                    status = "passed"
                
                return {
                    "status": status,
                    "summary": {
                        "total_tests": report["summary"]["total_tests"],
                        "passed": report["summary"]["passed"],
                        "failed": report["summary"]["failed"],
                        "success_rate": report["summary"]["success_rate"],
                        "details": f"Security validation completed with {critical_failures} critical and {high_failures} high-severity failures"
                    },
                    "critical_issues": [r["test_name"] for r in report["test_results"] if not r["passed"] and r["severity"] == "CRITICAL"],
                    "recommendations": report["recommendations"]
                }
                
        except Exception as e:
            return {
                "status": "error",
                "summary": {"details": f"Security validation failed: {str(e)}"},
                "critical_issues": ["security_validation_error"],
                "recommendations": ["Fix security validation pipeline error"]
            }
    
    async def _run_iot_validation(self, output_dir: str) -> Dict[str, Any]:
        """Run IoT integration validation tests"""
        try:
            # Import and run IoT validator
            sys.path.append('tests/iot')
            from cultivar_iot_validator import CultivarIoTValidator
            
            async with CultivarIoTValidator(base_url=self.base_url) as validator:
                report = await validator.run_all_iot_tests()
                
                # Save individual report
                iot_report_path = os.path.join(output_dir, f"iot_validation_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json")
                with open(iot_report_path, 'w') as f:
                    json.dump(report, f, indent=2)
                
                # Determine status
                failed_tests = report["summary"]["failed"]
                total_tests = report["summary"]["total_tests"]
                
                if failed_tests > total_tests * 0.5:  # More than 50% failed
                    status = "failed"
                elif failed_tests > total_tests * 0.2:  # More than 20% failed
                    status = "warning"
                else:
                    status = "passed"
                
                return {
                    "status": status,
                    "summary": {
                        "total_tests": report["summary"]["total_tests"],
                        "passed": report["summary"]["passed"],
                        "failed": report["summary"]["failed"],
                        "success_rate": report["summary"]["success_rate"],
                        "details": f"IoT validation completed with {failed_tests} failed tests"
                    },
                    "iot_issues": [r["test_name"] for r in report["test_results"] if not r["passed"]],
                    "recommendations": report["recommendations"]
                }
                
        except Exception as e:
            return {
                "status": "error",
                "summary": {"details": f"IoT validation failed: {str(e)}"},
                "iot_issues": ["iot_validation_error"],
                "recommendations": ["Fix IoT validation pipeline error"]
            }
    
    async def _run_e2e_validation(self, output_dir: str) -> Dict[str, Any]:
        """Run end-to-end validation tests"""
        try:
            # Import and run E2E validator
            sys.path.append('tests/e2e')
            from cultivar_e2e_validator import CultivarE2EValidator
            
            async with CultivarE2EValidator(base_url=self.base_url) as validator:
                report = await validator.run_all_e2e_tests()
                
                # Save individual report
                e2e_report_path = os.path.join(output_dir, f"e2e_validation_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json")
                with open(e2e_report_path, 'w') as f:
                    json.dump(report, f, indent=2)
                
                # Determine status
                failed_workflows = report["summary"]["failed_workflows"]
                total_workflows = report["summary"]["total_workflows"]
                
                if failed_workflows > total_workflows * 0.3:  # More than 30% failed
                    status = "failed"
                elif failed_workflows > total_workflows * 0.1:  # More than 10% failed
                    status = "warning"
                else:
                    status = "passed"
                
                return {
                    "status": status,
                    "summary": {
                        "total_workflows": report["summary"]["total_workflows"],
                        "passed_workflows": report["summary"]["passed_workflows"],
                        "failed_workflows": report["summary"]["failed_workflows"],
                        "success_rate": report["summary"]["success_rate"],
                        "details": f"E2E validation completed with {failed_workflows} failed workflows"
                    },
                    "e2e_issues": [r["workflow_name"] for r in report["detailed_results"] if not r["passed"]],
                    "recommendations": report["recommendations"]
                }
                
        except Exception as e:
            return {
                "status": "error",
                "summary": {"details": f"E2E validation failed: {str(e)}"},
                "e2e_issues": ["e2e_validation_error"],
                "recommendations": ["Fix E2E validation pipeline error"]
            }
    
    def _generate_consolidated_report(self, validation_results: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """Generate consolidated validation report"""
        # Calculate overall statistics
        total_validations = len(validation_results)
        passed_validations = sum(1 for result in validation_results.values() if result["status"] == "passed")
        failed_validations = sum(1 for result in validation_results.values() if result["status"] == "failed")
        warning_validations = sum(1 for result in validation_results.values() if result["status"] == "warning")
        error_validations = sum(1 for result in validation_results.values() if result["status"] == "error")
        
        # Determine overall status
        if error_validations > 0:
            overall_status = "error"
        elif failed_validations > 0:
            overall_status = "failed"
        elif warning_validations > 0:
            overall_status = "warning"
        else:
            overall_status = "passed"
        
        # Collect all issues and recommendations
        all_issues = []
        all_recommendations = []
        
        for test_type, result in validation_results.items():
            if "critical_issues" in result:
                all_issues.extend([f"[{test_type.upper()}] {issue}" for issue in result["critical_issues"]])
            if "iot_issues" in result:
                all_issues.extend([f"[{test_type.upper()}] {issue}" for issue in result["iot_issues"]])
            if "e2e_issues" in result:
                all_issues.extend([f"[{test_type.upper()}] {issue}" for issue in result["e2e_issues"]])
            
            if "recommendations" in result:
                all_recommendations.extend([f"[{test_type.upper()}] {rec}" for rec in result["recommendations"]])
        
        # Generate deployment readiness assessment
        deployment_readiness = self._assess_deployment_readiness(validation_results)
        
        consolidated_report = {
            "timestamp": datetime.utcnow().isoformat(),
            "application_url": self.base_url,
            "overall_status": overall_status,
            "deployment_readiness": deployment_readiness,
            "summary": {
                "total_validations": total_validations,
                "passed": passed_validations,
                "failed": failed_validations,
                "warnings": warning_validations,
                "errors": error_validations,
                "success_rate": f"{(passed_validations/total_validations*100):.1f}%" if total_validations > 0 else "0%"
            },
            "validation_results": validation_results,
            "all_issues": all_issues,
            "all_recommendations": all_recommendations,
            "pipeline_runs": [asdict(run) for run in self.validation_runs]
        }
        
        return consolidated_report
    
    def _determine_overall_status(self, validation_results: Dict[str, Any]) -> str:
        """Determine overall validation status"""
        statuses = [result["status"] for result in validation_results.values()]
        
        if "error" in statuses:
            return "error"
        elif "failed" in statuses:
            return "failed"
        elif "warning" in statuses:
            return "warning"
        else:
            return "passed"
    
    def _assess_deployment_readiness(self, validation_results: Dict[str, Any]) -> Dict[str, str]:
        """Assess deployment readiness based on validation results"""
        security_status = validation_results.get("security", {}).get("status", "unknown")
        iot_status = validation_results.get("iot", {}).get("status", "unknown")
        e2e_status = validation_results.get("e2e", {}).get("status", "unknown")
        
        # Security is critical for any deployment
        if security_status == "failed":
            security_readiness = "NOT READY - Critical security issues must be resolved"
        elif security_status == "warning":
            security_readiness = "CAUTION - Address security warnings before production"
        elif security_status == "passed":
            security_readiness = "READY - Security validation passed"
        else:
            security_readiness = "UNKNOWN - Security validation failed to run"
        
        # IoT integration is important but not blocking
        if iot_status == "failed":
            iot_readiness = "OPTIONAL - IoT features may not work properly"
        elif iot_status in ["warning", "passed"]:
            iot_readiness = "READY - IoT integration functional"
        else:
            iot_readiness = "UNKNOWN - IoT validation failed to run"
        
        # E2E tests are critical for user experience
        if e2e_status == "failed":
            e2e_readiness = "NOT READY - Core user workflows are broken"
        elif e2e_status == "warning":
            e2e_readiness = "CAUTION - Some user workflows may have issues"
        elif e2e_status == "passed":
            e2e_readiness = "READY - User workflows validated"
        else:
            e2e_readiness = "UNKNOWN - E2E validation failed to run"
        
        # Overall deployment recommendation
        if security_status == "failed" or e2e_status == "failed":
            overall_recommendation = "DO NOT DEPLOY - Critical issues must be resolved"
        elif security_status in ["warning"] or e2e_status in ["warning"]:
            overall_recommendation = "DEPLOY WITH CAUTION - Address warnings in next update"
        elif security_status == "passed" and e2e_status == "passed":
            overall_recommendation = "READY FOR DEPLOYMENT - All critical validations passed"
        else:
            overall_recommendation = "DEPLOYMENT STATUS UNKNOWN - Validation pipeline issues"
        
        return {
            "security": security_readiness,
            "iot": iot_readiness,
            "e2e": e2e_readiness,
            "overall": overall_recommendation
        }
    
    def _display_validation_summary(self, report: Dict[str, Any]):
        """Display validation summary to console"""
        print(f"\n📊 CULTIVAR VALIDATION SUMMARY")
        print("=" * 50)
        
        # Overall status
        status_emoji = {
            "passed": "✅",
            "warning": "⚠️",
            "failed": "❌",
            "error": "🚨"
        }
        
        status = report["overall_status"]
        emoji = status_emoji.get(status, "❓")
        print(f"{emoji} Overall Status: {status.upper()}")
        
        # Summary statistics
        summary = report["summary"]
        print(f"\n📈 Test Results:")
        print(f"   Total Validations: {summary['total_validations']}")
        print(f"   Passed: {summary['passed']} ✅")
        print(f"   Failed: {summary['failed']} ❌")
        print(f"   Warnings: {summary['warnings']} ⚠️")
        print(f"   Errors: {summary['errors']} 🚨")
        print(f"   Success Rate: {summary['success_rate']}")
        
        # Deployment readiness
        readiness = report["deployment_readiness"]
        print(f"\n🚀 Deployment Readiness:")
        print(f"   Security: {readiness['security']}")
        print(f"   IoT Integration: {readiness['iot']}")
        print(f"   User Workflows: {readiness['e2e']}")
        print(f"   Overall: {readiness['overall']}")
        
        # Critical issues
        if report["all_issues"]:
            print(f"\n🚨 Critical Issues Found ({len(report['all_issues'])}):")
            for issue in report["all_issues"][:5]:  # Show first 5 issues
                print(f"   - {issue}")
            if len(report["all_issues"]) > 5:
                print(f"   ... and {len(report['all_issues']) - 5} more issues")
        
        # Key recommendations
        if report["all_recommendations"]:
            print(f"\n💡 Key Recommendations:")
            for rec in report["all_recommendations"][:3]:  # Show first 3 recommendations
                print(f"   - {rec}")
            if len(report["all_recommendations"]) > 3:
                print(f"   ... and {len(report['all_recommendations']) - 3} more recommendations")

# CLI interface for continuous validation
async def main():
    """CLI interface for continuous validation pipeline"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CultivAR Continuous Validation Pipeline")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of the application")
    parser.add_argument("--output", default="validation_reports", help="Output directory for reports")
    parser.add_argument("--security", action="store_true", default=True, help="Include security validation")
    parser.add_argument("--iot", action="store_true", default=True, help="Include IoT validation")
    parser.add_argument("--e2e", action="store_true", default=True, help="Include E2E validation")
    parser.add_argument("--ci", action="store_true", help="CI mode - exit with appropriate code")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    pipeline = CultivarValidationPipeline(base_url=args.url)
    
    try:
        report = await pipeline.run_complete_validation_suite(
            include_security=args.security,
            include_iot=args.iot,
            include_e2e=args.e2e,
            output_dir=args.output
        )
        
        # CI mode exit codes
        if args.ci:
            if report["overall_status"] == "passed":
                print("\n✅ All validations passed - Ready for deployment")
                sys.exit(0)
            elif report["overall_status"] == "warning":
                print("\n⚠️ Validations passed with warnings - Review recommendations")
                sys.exit(1)
            else:
                print("\n❌ Validations failed - Do not deploy")
                sys.exit(2)
        
        return report
        
    except Exception as e:
        print(f"\n🚨 Validation pipeline failed: {e}")
        if args.ci:
            sys.exit(3)
        raise

if __name__ == "__main__":
    asyncio.run(main())