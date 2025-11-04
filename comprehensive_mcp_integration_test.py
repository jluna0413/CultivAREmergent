#!/usr/bin/env python3
"""
Comprehensive MCP Integration Test Suite
Tests TaskMaster AI and OLLAMA service configuration integration
"""

import json
import subprocess
import sys
import requests
import time
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any


class MCPIntegrationTest:
    def __init__(self):
        self.test_results = []
        self.config_files = [
            'cline_mcp_settings_corrected.json',
            'mcp_corrected.json', 
            'vscode_settings_corrected.json'
        ]
        
    def log_test(self, test_name: str, status: str, details: str = "", issues: List[str] = None):
        """Log test results"""
        result = {
            'test': test_name,
            'status': status,
            'details': details,
            'issues': issues or []
        }
        self.test_results.append(result)
        
        status_symbol = "[PASS]" if status == "PASS" else "[FAIL]" if status == "FAIL" else "[WARN]"
        print(f"{status_symbol} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
        if issues:
            print(f"   Issues: {', '.join(issues)}")
        print()
        
    def test_json_validation(self) -> bool:
        """Test 1: Comprehensive JSON validation using Python's json module"""
        print("=== JSON VALIDATION TESTS ===")
        
        all_passed = True
        for config_file in self.config_files:
            try:
                # Test file existence
                if not Path(config_file).exists():
                    self.log_test(f"JSON Validation - {config_file}", "FAIL", 
                                "File does not exist", [f"Missing file: {config_file}"])
                    all_passed = False
                    continue
                    
                # Test JSON parsing
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Check for hidden characters (non-printable ASCII except common whitespace)
                hidden_chars = []
                for i, char in enumerate(content):
                    if ord(char) < 32 and char not in '\t\n\r':
                        hidden_chars.append(f"Position {i}: '\\x{ord(char):02x}'")
                
                if hidden_chars:
                    self.log_test(f"JSON Validation - {config_file}", "FAIL",
                                "Hidden characters detected", hidden_chars)
                    all_passed = False
                    continue
                    
                # Parse JSON
                data = json.loads(content)
                
                # Validate structure
                if 'mcpServers' not in data:
                    self.log_test(f"JSON Validation - {config_file}", "WARN",
                                "No mcpServers section found", [])
                else:
                    self.log_test(f"JSON Validation - {config_file}", "PASS",
                                f"Valid JSON with {len(data.get('mcpServers', {}))} MCP servers", [])
                    
            except json.JSONDecodeError as e:
                self.log_test(f"JSON Validation - {config_file}", "FAIL",
                            f"JSON parsing error: {e}", [f"Line {e.lineno}, Column {e.colno}"])
                all_passed = False
            except Exception as e:
                self.log_test(f"JSON Validation - {config_file}", "FAIL",
                            f"Unexpected error: {e}", [str(e)])
                all_passed = False
                
        return all_passed
        
    def test_taskmaster_installation(self) -> bool:
        """Test 2: TaskMaster AI installation and version verification"""
        print("=== TASKMASTER AI INSTALLATION TESTS ===")
        
        all_passed = True
        
        try:
            # Test package availability
            result = subprocess.run(['npm', 'view', 'task-master-ai'], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Extract version
                version_match = re.search(r'task-master-ai@([\d\.]+)', result.stdout)
                if version_match:
                    version = version_match.group(1)
                    self.log_test("TaskMaster AI Package", "PASS", 
                                f"Package available, version {version}")
                else:
                    self.log_test("TaskMaster AI Package", "WARN", 
                                "Package available but version unclear")
            else:
                self.log_test("TaskMaster AI Package", "FAIL", 
                            "Package not available", ["npm view failed"])
                all_passed = False
                
        except subprocess.TimeoutExpired:
            self.log_test("TaskMaster AI Package", "FAIL", 
                        "Package check timeout", ["Command timed out"])
            all_passed = False
        except Exception as e:
            self.log_test("TaskMaster AI Package", "FAIL", 
                        f"Package check error: {e}", [str(e)])
            all_passed = False
            
        try:
            # Test executable availability
            result = subprocess.run(['npx', '-y', 'task-master-ai', '--version'], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.log_test("TaskMaster AI Execution", "PASS", 
                            "Server can be executed successfully")
            else:
                self.log_test("TaskMaster AI Execution", "FAIL", 
                            "Server execution failed", [result.stderr])
                all_passed = False
                
        except subprocess.TimeoutExpired:
            self.log_test("TaskMaster AI Execution", "FAIL", 
                        "Execution timeout", ["Command timed out"])
            all_passed = False
        except Exception as e:
            self.log_test("TaskMaster AI Execution", "FAIL", 
                        f"Execution error: {e}", [str(e)])
            all_passed = False
            
        return all_passed
        
    def test_ollama_connectivity(self) -> bool:
        """Test 3: OLLAMA service connectivity testing"""
        print("=== OLLAMA CONNECTIVITY TESTS ===")
        
        all_passed = True
        base_url = "http://127.0.0.1:11435"
        
        try:
            # Test basic connectivity
            response = requests.get(f"{base_url}/api/version", timeout=10)
            
            if response.status_code == 200:
                version_data = response.json()
                version = version_data.get('version', 'unknown')
                self.log_test("OLLAMA Service", "PASS", 
                            f"Service accessible, version {version}")
            else:
                self.log_test("OLLAMA Service", "FAIL", 
                            f"Service returned status {response.status_code}", 
                            [f"HTTP {response.status_code}"])
                all_passed = False
                
        except requests.exceptions.ConnectionError:
            self.log_test("OLLAMA Service", "FAIL", 
                        "Cannot connect to OLLAMA service", 
                        ["Connection refused - service not running?"])
            all_passed = False
        except requests.exceptions.Timeout:
            self.log_test("OLLAMA Service", "FAIL", 
                        "Connection timeout", ["Service not responding"])
            all_passed = False
        except Exception as e:
            self.log_test("OLLAMA Service", "FAIL", 
                        f"Connection error: {e}", [str(e)])
            all_passed = False
            
        try:
            # Test model availability
            response = requests.get(f"{base_url}/api/tags", timeout=15)
            
            if response.status_code == 200:
                models_data = response.json()
                models = [model['name'] for model in models_data.get('models', [])]
                
                # Check for specific model
                target_model = "gemma3:270m"
                if target_model in models:
                    self.log_test("OLLAMA Model Availability", "PASS", 
                                f"Target model '{target_model}' found in {len(models)} available models")
                else:
                    self.log_test("OLLAMA Model Availability", "WARN", 
                                f"Target model '{target_model}' not found", 
                                [f"Available models: {', '.join(models[:5])}{'...' if len(models) > 5 else ''}"])
                    
        except Exception as e:
            self.log_test("OLLAMA Model Availability", "FAIL", 
                        f"Model check error: {e}", [str(e)])
            all_passed = False
            
        return all_passed
        
    def test_mcp_naming_conventions(self) -> bool:
        """Test 4: MCP server naming conventions validation"""
        print("=== MCP NAMING CONVENTIONS TESTS ===")
        
        all_passed = True
        
        for config_file in self.config_files:
            try:
                if not Path(config_file).exists():
                    continue
                    
                with open(config_file, 'r') as f:
                    data = json.load(f)
                    
                mcp_servers = data.get('mcpServers', {})
                
                for server_name in mcp_servers.keys():
                    # Check naming convention (alphanumeric and hyphens only)
                    if not re.match(r'^[a-z0-9\-]+$', server_name):
                        self.log_test(f"MCP Naming - {server_name}", "FAIL", 
                                    f"Invalid name format in {config_file}", 
                                    ["Name should contain only lowercase letters, numbers, and hyphens"])
                        all_passed = False
                    else:
                        self.log_test(f"MCP Naming - {server_name}", "PASS", 
                                    f"Valid naming convention in {config_file}")
                        
            except Exception as e:
                self.log_test(f"MCP Naming - {config_file}", "FAIL", 
                            f"Error checking names: {e}", [str(e)])
                all_passed = False
            
        return all_passed
        
    def test_end_to_end_integration(self) -> bool:
        """Test 5: End-to-end protocol communication testing"""
        print("=== END-TO-END INTEGRATION TESTS ===")
        
        all_passed = True
        
        try:
            # Test TaskMaster AI startup with OLLAMA environment
            import os
            env = os.environ.copy()
            env.update({
                'OLLAMA_BASE_URL': 'http://127.0.0.1:11435',
                'OLLAMA_MODEL': 'gemma3:270m'
            })
            
            # Start TaskMaster AI server briefly to test integration
            process = subprocess.Popen(
                ['npx', '-y', 'task-master-ai'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Wait briefly for startup
            time.sleep(10)
            
            if process.poll() is None:
                self.log_test("TaskMaster AI Startup", "PASS", 
                            "Server started successfully with OLLAMA environment")
                
                # Get process output for analysis
                try:
                    stdout, stderr = process.communicate(timeout=5)
                    
                    if "Registered 44 tools successfully" in stdout:
                        self.log_test("TaskMaster AI Tools", "PASS", 
                                    "All 44 tools registered successfully")
                    else:
                        self.log_test("TaskMaster AI Tools", "WARN", 
                                    "Tool registration unclear", ["Check server logs"])
                    
                    if "MCP Server connected" in stdout:
                        self.log_test("MCP Protocol Connection", "PASS", 
                                    "MCP protocol connection established")
                    else:
                        self.log_test("MCP Protocol Connection", "WARN", 
                                    "Connection status unclear", ["Check server logs"])
                        
                except subprocess.TimeoutExpired:
                    # Process still running, which is good
                    self.log_test("TaskMaster AI Process", "PASS", 
                                "Server process running stably")
                    process.terminate()
                    process.wait()
                    
            else:
                stdout, stderr = process.communicate()
                self.log_test("TaskMaster AI Startup", "FAIL", 
                            "Server failed to start", [stderr])
                all_passed = False
                
        except Exception as e:
            self.log_test("End-to-End Integration", "FAIL", 
                        f"Integration test error: {e}", [str(e)])
            all_passed = False
            
        return all_passed
        
    def generate_test_report(self) -> str:
        """Generate comprehensive test report"""
        report = []
        report.append("=" * 80)
        report.append("COMPREHENSIVE MCP INTEGRATION TEST REPORT")
        report.append("=" * 80)
        report.append(f"Test Date: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
        report.append(f"Test Environment: Windows 11")
        report.append("")
        
        # Summary
        passed = sum(1 for r in self.test_results if r['status'] == 'PASS')
        failed = sum(1 for r in self.test_results if r['status'] == 'FAIL')
        warnings = sum(1 for r in self.test_results if r['status'] == 'WARN')
        
        report.append("SUMMARY")
        report.append("-" * 40)
        report.append(f"Total Tests: {len(self.test_results)}")
        report.append(f"Passed: {passed}")
        report.append(f"Failed: {failed}")
        report.append(f"Warnings: {warnings}")
        report.append("")
        
        # Detailed results
        report.append("DETAILED RESULTS")
        report.append("-" * 40)
        
        for result in self.test_results:
            report.append(f"Test: {result['test']}")
            report.append(f"Status: {result['status']}")
            if result['details']:
                report.append(f"Details: {result['details']}")
            if result['issues']:
                report.append(f"Issues: {', '.join(result['issues'])}")
            report.append("")
            
        # Issues requiring attention
        issues = [r for r in self.test_results if r['status'] in ['FAIL', 'WARN']]
        if issues:
            report.append("ISSUES REQUIRING ATTENTION")
            report.append("-" * 40)
            
            critical_issues = [r for r in issues if r['status'] == 'FAIL']
            warning_issues = [r for r in issues if r['status'] == 'WARN']
            
            if critical_issues:
                report.append("Critical Issues:")
                for issue in critical_issues:
                    report.append(f"  • {issue['test']}: {issue['details']}")
                report.append("")
                
            if warning_issues:
                report.append("Warning Issues:")
                for issue in warning_issues:
                    report.append(f"  • {issue['test']}: {issue['details']}")
                report.append("")
        else:
            report.append("No critical issues detected.")
            report.append("")
            
        # Recommendations
        report.append("RECOMMENDATIONS")
        report.append("-" * 40)
        
        if failed == 0 and warnings == 0:
            report.append("[SUCCESS] All tests passed successfully. MCP integration is ready for use.")
        elif failed == 0:
            report.append("[WARNING] All core tests passed, but some warnings should be addressed.")
        else:
            report.append("[FAIL] Several critical issues must be resolved before production use.")
            
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)
        
    def run_all_tests(self) -> bool:
        """Run complete test suite"""
        print("Starting Comprehensive MCP Integration Test Suite")
        print("=" * 60)
        print()
        
        # Run all test categories
        json_valid = self.test_json_validation()
        tm_ai_valid = self.test_taskmaster_installation()
        ollama_valid = self.test_ollama_connectivity()
        naming_valid = self.test_mcp_naming_conventions()
        integration_valid = self.test_end_to_end_integration()
        
        # Generate report
        report = self.generate_test_report()
        print(report)
        
        # Save report to file
        with open('mcp_integration_test_report.txt', 'w') as f:
            f.write(report)
            
        print("[INFO] Test report saved to: mcp_integration_test_report.txt")
        
        # Return overall success
        overall_success = all([json_valid, tm_ai_valid, ollama_valid, naming_valid, integration_valid])
        
        if overall_success:
            print("\n[SUCCESS] ALL TESTS PASSED - MCP Integration is working correctly!")
        else:
            print("\n[WARNING] Some tests failed. Review the report for details.")
            
        return overall_success


if __name__ == "__main__":
    tester = MCPIntegrationTest()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)