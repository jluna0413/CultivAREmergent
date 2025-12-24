#!/bin/bash

echo "Deploying Flutter Web Application..."

# Navigate to the Flutter project directory
cd flutter_app

# Get dependencies
echo "Getting Flutter dependencies..."
flutter pub get

# Build the web application
echo "Building Flutter web application..."
flutter build web

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "Flutter web application built successfully to flutter_app/build/web."
    echo "To serve the application, you can use a web server like Nginx or a simple HTTP server."
    echo "For example, to serve locally with Python (for testing):"
    echo "  cd build/web"
    echo "  python -m http.server 8000"
    echo "Then open your browser to http://localhost:8000"
    echo ""
    echo "For production, configure a robust web server (e.g., Nginx, Apache) to serve the contents of the 'flutter_app/build/web' directory."
else
    echo "Flutter web application build failed."
    exit 1
fi