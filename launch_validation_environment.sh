#!/bin/bash

# 🚀 CultivAR Real-World Validation Quick Start Script
# This script launches all necessary services for comprehensive validation

echo "🚀 Starting CultivAR Real-World Validation Environment..."

# Navigate to project root
cd a:/dev/CultivAREmergant

# Check if we're in the right directory
if [ ! -f "run_fastapi.py" ]; then
    echo "❌ Error: Not in project root directory"
    echo "Please navigate to a:/dev/CultivAREmergant first"
    exit 1
fi

echo "✅ Project root verified"

# Function to start FastAPI backend in background
start_fastapi() {
    echo "🔧 Starting FastAPI backend..."
    python run_fastapi.py &
    FASTAPI_PID=$!
    echo "FastAPI started with PID: $FASTAPI_PID"
    echo $FASTAPI_PID > fastapi.pid
    sleep 3
}

# Function to start Flask web interface (optional)
start_flask() {
    echo "🌐 Starting Flask web interface (optional)..."
    python run_flask.py &
    FLASK_PID=$!
    echo "Flask started with PID: $FLASK_PID"
    echo $FLASK_PID > flask.pid
    sleep 2
}

# Function to verify services are running
verify_services() {
    echo "🔍 Verifying services..."
    
    # Check FastAPI
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "✅ FastAPI backend is running"
    else
        echo "❌ FastAPI backend not responding"
        return 1
    fi
    
    # Check Flask (optional)
    if curl -s http://localhost:5000/health > /dev/null; then
        echo "✅ Flask web interface is running"
    else
        echo "⚠️  Flask web interface not responding (this is optional)"
    fi
    
    return 0
}

# Function to launch Flutter app
launch_flutter() {
    echo "📱 Launching Flutter app..."
    
    cd flutter_app
    
    # Check if Flutter is available
    if ! command -v flutter &> /dev/null; then
        echo "❌ Flutter not found. Please install Flutter first."
        echo "Visit: https://flutter.dev/docs/get-started/install"
        return 1
    fi
    
    # Get Flutter packages
    echo "📦 Getting Flutter dependencies..."
    flutter pub get
    
    # Launch Flutter app in web mode (recommended for testing)
    echo "🌐 Launching Flutter web app..."
    echo "The app will open in your default browser"
    echo "Press Ctrl+C to stop the Flutter app"
    
    flutter run -d chrome --web-renderer canvaskit
}

# Function to run validation tests
run_validation_tests() {
    echo "🧪 Running validation tests..."
    
    cd ..
    
    # Install dependencies if needed
    if ! python -c "import pytest, httpx, jwt" 2>/dev/null; then
        echo "📦 Installing Python dependencies..."
        pip install pytest httpx jwt requests
    fi
    
    echo "🔐 Running security validation..."
    python tests/security/security_validation_framework.py
    
    echo "🔧 Running IoT integration tests..."
    python tests/iot/iot_integration_validation.py
    
    echo "🛡️ Running OWASP ZAP scan (requires Docker)..."
    python scripts/owasp_zap_scanner.py --scan
}

# Main execution
echo "Select an option:"
echo "1. Start FastAPI backend only"
echo "2. Start FastAPI + Flask (full stack)"
echo "3. Launch Flutter app (requires backend running)"
echo "4. Run all validation tests"
echo "5. Complete setup: Start backend + Launch Flutter"
echo "6. Exit"

read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        start_fastapi
        verify_services
        ;;
    2)
        start_fastapi
        start_flask
        verify_services
        ;;
    3)
        if verify_services; then
            launch_flutter
        else
            echo "❌ Please start the backend first (option 1 or 2)"
        fi
        ;;
    4)
        run_validation_tests
        ;;
    5)
        start_fastapi
        start_flask
        verify_services
        sleep 2
        launch_flutter
        ;;
    6)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

# Cleanup function
cleanup() {
    echo "🧹 Cleaning up..."
    
    # Stop FastAPI if running
    if [ -f "fastapi.pid" ]; then
        kill $(cat fastapi.pid) 2>/dev/null
        rm fastapi.pid
        echo "Stopped FastAPI backend"
    fi
    
    # Stop Flask if running
    if [ -f "flask.pid" ]; then
        kill $(cat flask.pid) 2>/dev/null
        rm flask.pid
        echo "Stopped Flask web interface"
    fi
    
    # Kill any Flutter processes
    pkill -f "flutter run" 2>/dev/null
    echo "Stopped Flutter app"
    
    echo "✅ Cleanup complete"
}

# Set trap to cleanup on exit
trap cleanup EXIT

echo "✅ Setup complete! Press Ctrl+C to stop all services."
echo "📋 Services will be managed automatically."

# Keep script running to maintain services
while true; do
    sleep 10
    echo "💫 Services still running..."
done