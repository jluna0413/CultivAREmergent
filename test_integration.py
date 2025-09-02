#!/usr/bin/env python3
"""
Test script for CultivAR MCP integration
"""

import asyncio
import json
import sys
import subprocess
import time
from pathlib import Path

async def test_mcp_server():
    """Test the MCP server functionality"""
    print("🧪 Testing CultivAR MCP Server...")
    
    # Test 1: Import and basic functionality
    try:
        print("📦 Testing MCP server import...")
        import mcp_server
        print("✅ MCP server imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import MCP server: {e}")
        return False
    
    # Test 2: Data access layer
    try:
        print("📊 Testing data access layer...")
        from mcp_server import CultivARData
        
        plants = CultivARData.get_plants()
        print(f"✅ Found {len(plants)} plants in test data")
        
        strains = CultivARData.get_strains()
        print(f"✅ Found {len(strains)} strains in test data")
        
        env_data = CultivARData.get_environmental_data()
        print(f"✅ Found {len(env_data)} environmental readings")
        
    except Exception as e:
        print(f"❌ Data access test failed: {e}")
        return False
    
    # Test 3: MCP tools functionality
    try:
        print("🔧 Testing MCP tools...")
        from mcp_server import handle_list_tools
        
        tools = await handle_list_tools()
        print(f"✅ Found {len(tools)} MCP tools available")
        
        for tool in tools:
            print(f"   - {tool.name}: {tool.description}")
        
    except Exception as e:
        print(f"❌ MCP tools test failed: {e}")
        return False
    
    print("🎉 All MCP tests passed!")
    return True

def test_cultivar_app():
    """Test if the main CultivAR app can be imported"""
    print("🚀 Testing CultivAR main application...")
    
    try:
        # Test app import
        import cultivar_app
        print("✅ CultivAR app imported successfully")
        
        # Test app creation
        app = cultivar_app.create_app()
        print("✅ CultivAR app created successfully")
        
        # Test configuration
        with app.app_context():
            print(f"✅ App configured with debug mode: {app.debug}")
        
        return True
        
    except Exception as e:
        print(f"❌ CultivAR app test failed: {e}")
        return False

def test_documentation():
    """Test that documentation files exist"""
    print("📚 Testing documentation completeness...")
    
    docs_dir = Path("docs/deepwiki")
    required_docs = [
        "README.md",
        "mcp-integration.md", 
        "quick-start.md",
        "ai-assistant-setup.md",
        "architecture.md"
    ]
    
    missing_docs = []
    for doc in required_docs:
        doc_path = docs_dir / doc
        if doc_path.exists():
            print(f"✅ Found {doc}")
        else:
            print(f"❌ Missing {doc}")
            missing_docs.append(doc)
    
    if missing_docs:
        print(f"❌ Missing documentation files: {missing_docs}")
        return False
    else:
        print("✅ All required documentation files present")
        return True

def main():
    """Run all tests"""
    print("🧪 CultivAR Integration Test Suite")
    print("=" * 50)
    
    tests = [
        ("Documentation", test_documentation),
        ("CultivAR App", test_cultivar_app),
        ("MCP Server", lambda: asyncio.run(test_mcp_server()))
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} tests...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(tests)} tests")
    
    if passed == len(tests):
        print("🎉 All tests passed! CultivAR with MCP integration is ready!")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())