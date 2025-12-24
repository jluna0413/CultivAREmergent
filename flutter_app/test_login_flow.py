#!/usr/bin/env python3
"""
Comprehensive Playwright test for Flutter app login flow
Tests both admin and user authentication flows with detailed logging
"""

import asyncio
import json
import time
from datetime import datetime
from playwright.async_api import async_playwright

class LoginFlowTester:
    def __init__(self, base_url="http://localhost:5050"):
        self.base_url = base_url
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "tests": [],
            "summary": {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "errors": []
            }
        }
    
    async def test_login_flow(self, page, username, password, expected_role):
        """Test individual login flow"""
        test_name = f"Login flow - {username} ({expected_role})"
        print(f"\n🧪 Testing {test_name}...")
        
        test_result = {
            "test_name": test_name,
            "username": username,
            "expected_role": expected_role,
            "start_time": datetime.now().isoformat(),
            "steps": [],
            "status": "pending",
            "errors": []
        }
        
        try:
            # Step 1: Navigate to login page
            print("   📍 Step 1: Navigating to login page...")
            test_result["steps"].append("Navigate to login page")
            await page.goto(f"{self.base_url}/login", wait_until="networkidle")
            
            # Wait for login form to be visible
            await page.wait_for_selector('input[type="email"], input[name*="email"], input[name*="username"]', 
                                       timeout=10000)
            print("   ✅ Login page loaded")
            
            # Step 2: Fill in credentials
            print("   📍 Step 2: Filling in credentials...")
            test_result["steps"].append("Fill in credentials")
            
            # Try multiple selectors for email/username field
            email_selectors = [
                'input[type="email"]',
                'input[name*="email"]',
                'input[name*="username"]',
                'input[placeholder*="email"]',
                'input[placeholder*="Email"]',
                'input[placeholder*="username"]',
                'input[placeholder*="Username"]'
            ]
            
            email_field = None
            for selector in email_selectors:
                try:
                    email_field = page.locator(selector).first
                    if await email_field.is_visible(timeout=1000):
                        break
                except:
                    continue
            
            if not email_field or not await email_field.is_visible():
                raise Exception("Could not find email/username field")
            
            await email_field.fill(username)
            print(f"   ✅ Filled username: {username}")
            
            # Try multiple selectors for password field
            password_selectors = [
                'input[type="password"]',
                'input[name*="password"]',
                'input[placeholder*="password"]',
                'input[placeholder*="Password"]'
            ]
            
            password_field = None
            for selector in password_selectors:
                try:
                    password_field = page.locator(selector).first
                    if await password_field.is_visible(timeout=1000):
                        break
                except:
                    continue
            
            if not password_field or not await password_field.is_visible():
                raise Exception("Could not find password field")
            
            await password_field.fill(password)
            print("   ✅ Filled password")
            
            # Step 3: Submit login form
            print("   📍 Step 3: Submitting login form...")
            test_result["steps"].append("Submit login form")
            
            # Try multiple selectors for submit button
            submit_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Login")',
                'button:has-text("Sign In")',
                'button:has-text("Submit")',
                'button:has-text("Continue")'
            ]
            
            submit_button = None
            for selector in submit_selectors:
                try:
                    submit_button = page.locator(selector).first
                    if await submit_button.is_visible(timeout=1000):
                        break
                except:
                    continue
            
            if not submit_button or not await submit_button.is_visible():
                # Try pressing Enter if no button found
                await password_field.press("Enter")
                print("   ⚠️  No submit button found, using Enter key")
            else:
                await submit_button.click()
                print("   ✅ Clicked submit button")
            
            # Step 4: Wait for authentication result
            print("   📍 Step 4: Waiting for authentication result...")
            test_result["steps"].append("Wait for authentication result")
            
            # Wait for navigation or error
            try:
                # Wait for potential navigation (success)
                await page.wait_for_url("**/dashboard", timeout=5000)
                current_url = page.url
                print(f"   ✅ Navigation successful: {current_url}")
                test_result["steps"].append(f"Navigation to dashboard: {current_url}")
                
                # Check if we're on dashboard
                if "/dashboard" in current_url:
                    print("   🎉 Login successful - redirected to dashboard")
                    test_result["status"] = "passed"
                    
                    # Verify dashboard content
                    try:
                        dashboard_selectors = [
                            'h1:has-text("Dashboard")',
                            'h1:has-text("dashboard")',
                            '[data-testid="dashboard"]',
                            '.dashboard'
                        ]
                        
                        for selector in dashboard_selectors:
                            try:
                                if await page.locator(selector).is_visible(timeout=2000):
                                    print(f"   ✅ Dashboard content verified with selector: {selector}")
                                    test_result["steps"].append(f"Dashboard content found: {selector}")
                                    break
                            except:
                                continue
                        
                        # Check for user info
                        user_info_selectors = [
                            'text=admin',
                            'text=Admin',
                            'text=user',
                            'text=User',
                            '[data-testid="user-info"]',
                            '.user-info'
                        ]
                        
                        for selector in user_info_selectors:
                            try:
                                if await page.locator(selector).is_visible(timeout=2000):
                                    print(f"   ✅ User info found with selector: {selector}")
                                    test_result["steps"].append(f"User info found: {selector}")
                                    break
                            except:
                                continue
                        
                    except Exception as e:
                        print(f"   ⚠️  Could not verify dashboard content: {e}")
                        test_result["errors"].append(f"Dashboard verification: {e}")
                
            except:
                # Check for login error
                print("   📍 Checking for login errors...")
                test_result["steps"].append("Check for login errors")
                
                error_selectors = [
                    'text*=error',
                    'text*=Error',
                    'text*=invalid',
                    'text*=Invalid',
                    'text*=failed',
                    'text*=Failed',
                    '.error',
                    '[role="alert"]',
                    '.alert'
                ]
                
                errors_found = []
                for selector in error_selectors:
                    try:
                        if await page.locator(selector).is_visible(timeout=2000):
                            error_text = await page.locator(selector).text_content()
                            errors_found.append(f"{selector}: {error_text}")
                            print(f"   ❌ Error found: {error_text}")
                    except:
                        continue
                
                if errors_found:
                    test_result["status"] = "failed"
                    test_result["errors"].extend(errors_found)
                    print("   ❌ Login failed with errors")
                else:
                    # Check if still on login page (might be validation error)
                    if "/login" in page.url:
                        print("   ⚠️  Still on login page - might be validation error")
                        test_result["errors"].append("Still on login page after submission")
                    else:
                        # Unknown state
                        test_result["status"] = "failed"
                        test_result["errors"].append("Unknown state after login attempt")
                        print("   ❌ Unknown state after login attempt")
            
        except Exception as e:
            print(f"   ❌ Test failed with exception: {e}")
            test_result["status"] = "failed"
            test_result["errors"].append(str(e))
            test_result["steps"].append(f"Exception: {str(e)}")
        
        test_result["end_time"] = datetime.now().isoformat()
        test_result["duration_seconds"] = (
            datetime.fromisoformat(test_result["end_time"]) - 
            datetime.fromisoformat(test_result["start_time"])
        ).total_seconds()
        
        return test_result
    
    async def check_console_logs(self, page):
        """Check browser console for JavaScript errors"""
        print("\n🔍 Checking console logs...")
        
        logs = []
        errors = []
        
        def handle_console(msg):
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "type": msg.type,
                "text": msg.text,
                "location": f"{msg.page.url} - Line {msg.location['lineNumber']}" if msg.location else "Unknown"
            }
            logs.append(log_entry)
            
            if msg.type in ["error", "warning"]:
                errors.append(log_entry)
                print(f"   [ERROR] Console {msg.type.upper()}: {msg.text}")
            else:
                print(f"   [INFO] Console {msg.type}: {msg.text}")
        
        page.on("console", handle_console)
        
        # Wait a moment to capture any async logs
        await asyncio.sleep(2)
        
        return {
            "logs": logs,
            "errors": errors,
            "total_logs": len(logs),
            "error_count": len(errors)
        }
    
    async def run_tests(self):
        """Run all login tests"""
        print("🚀 Starting Flutter App Login Flow Tests")
        print(f"🌐 Testing against: {self.base_url}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, slow_mo=1000)
            context = await browser.new_context(viewport={'width': 1280, 'height': 720})
            page = await context.new_page()
            
            # Test credentials
            test_cases = [
                ("admin@cultivar.app", "admin123", "admin"),
                ("user@cultivar.app", "user123", "user"),
                ("admin", "admin123", "admin"),  # Test without domain
                ("invalid@test.com", "wrongpassword", "invalid")  # Test failed login
            ]
            
            for username, password, expected_role in test_cases:
                print(f"\n{'='*50}")
                test_result = await self.test_login_flow(page, username, password, expected_role)
                self.test_results["tests"].append(test_result)
                self.test_results["summary"]["total_tests"] += 1
                
                if test_result["status"] == "passed":
                    self.test_results["summary"]["passed"] += 1
                    print(f"✅ {test_result['test_name']} - PASSED")
                else:
                    self.test_results["summary"]["failed"] += 1
                    print(f"❌ {test_result['test_name']} - FAILED")
                    self.test_results["summary"]["errors"].extend(test_result["errors"])
                
                # Check console logs after each test
                console_info = await self.check_console_logs(page)
                test_result["console"] = console_info
                
                # Clear page state between tests
                await page.goto("about:blank")
                await asyncio.sleep(1)
            
            await browser.close()
        
        return self.test_results

async def main():
    """Main test execution"""
    tester = LoginFlowTester()
    
    # Ensure app is accessible
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:5050") as response:
                if response.status == 200:
                    print("✓ Flutter app is accessible")
                else:
                    print(f"✗ Flutter app returned status {response.status}")
                    return
    except Exception as e:
        print(f"✗ Cannot connect to Flutter app: {e}")
        print("Make sure the app is running on http://localhost:5050")
        return
    
    results = await tester.run_tests()
    
    # Save detailed results
    with open('flutter_app_login_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print(f"\n{'='*50}")
    print("📊 TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Total Tests: {results['summary']['total_tests']}")
    print(f"Passed: {results['summary']['passed']}")
    print(f"Failed: {results['summary']['failed']}")
    print(f"Success Rate: {(results['summary']['passed']/results['summary']['total_tests']*100):.1f}%")
    
    if results['summary']['errors']:
        print(f"\n❌ ERRORS FOUND:")
        for error in results['summary']['errors']:
            print(f"   • {error}")
    
    print(f"\n📄 Detailed results saved to: flutter_app_login_test_results.json")

if __name__ == "__main__":
    asyncio.run(main())