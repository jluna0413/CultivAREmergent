#!/usr/bin/env python3
"""
CultivAR with MCP Integration Launcher

This script provides easy startup options for CultivAR with MCP support.
"""

import argparse
import asyncio
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

def setup_environment():
    """Setup environment variables for CultivAR"""
    defaults = {
        'SECRET_KEY': 'dev-secret-key-change-in-production',
        'CULTIVAR_DB_DRIVER': 'sqlite',
        'CULTIVAR_PORT': '5000',
        'DEBUG': 'true',
        'CULTIVAR_MCP_ENABLED': 'true',
        'CULTIVAR_MCP_PORT': '8001',
        'CULTIVAR_MCP_HOST': '127.0.0.1'
    }
    
    for key, value in defaults.items():
        if key not in os.environ:
            os.environ[key] = value
            print(f"Set {key}={value}")

def start_cultivar_app():
    """Start the main CultivAR Flask application"""
    print("🚀 Starting CultivAR main application...")
    
    try:
        import cultivar_app
        app = cultivar_app.create_app()
        port = int(os.environ.get('CULTIVAR_PORT', 5000))
        debug = os.environ.get('DEBUG', 'false').lower() == 'true'
        
        print(f"📱 CultivAR will be available at: http://localhost:{port}")
        print(f"🔑 Default login: admin / isley")
        
        app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)
        
    except Exception as e:
        print(f"❌ Failed to start CultivAR app: {e}")
        return False
    
    return True

def start_mcp_server():
    """Start the MCP server in a separate thread"""
    print("🤖 Starting MCP server...")
    
    def run_mcp():
        try:
            import mcp_server
            asyncio.run(mcp_server.main())
        except Exception as e:
            print(f"❌ MCP server error: {e}")
    
    mcp_thread = threading.Thread(target=run_mcp, daemon=True)
    mcp_thread.start()
    
    # Give MCP server time to start
    time.sleep(2)
    print(f"🔗 MCP server available at: localhost:{os.environ.get('CULTIVAR_MCP_PORT', 8001)}")
    
    return mcp_thread

def test_setup():
    """Test the setup by running integration tests"""
    print("🧪 Running integration tests...")
    try:
        result = subprocess.run([sys.executable, 'test_integration.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(description='CultivAR with MCP Integration Launcher')
    parser.add_argument('--mode', choices=['app', 'mcp', 'both', 'test'], 
                       default='both', help='What to start (default: both)')
    parser.add_argument('--port', type=int, default=5000, 
                       help='CultivAR app port (default: 5000)')
    parser.add_argument('--mcp-port', type=int, default=8001, 
                       help='MCP server port (default: 8001)')
    parser.add_argument('--debug', action='store_true', 
                       help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Update environment based on args
    os.environ['CULTIVAR_PORT'] = str(args.port)
    os.environ['CULTIVAR_MCP_PORT'] = str(args.mcp_port)
    if args.debug:
        os.environ['DEBUG'] = 'true'
        os.environ['CULTIVAR_MCP_LOG_LEVEL'] = 'DEBUG'
    
    print("🌱 CultivAR with MCP Integration")
    print("=" * 50)
    
    # Setup environment
    setup_environment()
    
    if args.mode == 'test':
        success = test_setup()
        sys.exit(0 if success else 1)
    
    mcp_thread = None
    
    try:
        if args.mode in ['mcp', 'both']:
            mcp_thread = start_mcp_server()
        
        if args.mode in ['app', 'both']:
            # Show startup info
            print(f"🌐 Starting in '{args.mode}' mode")
            print(f"📱 Web interface: http://localhost:{args.port}")
            if args.mode == 'both':
                print(f"🤖 MCP server: localhost:{args.mcp_port}")
            print("=" * 50)
            
            start_cultivar_app()
        elif args.mode == 'mcp':
            print("🤖 MCP server running. Press Ctrl+C to stop.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n👋 Shutting down MCP server...")
    
    except KeyboardInterrupt:
        print("\n👋 Shutting down CultivAR...")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()