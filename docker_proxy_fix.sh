#!/bin/bash
echo "Disabling Docker proxy settings..."
unset HTTP_PROXY
unset HTTPS_PROXY
export NO_PROXY="localhost,127.0.0.1,hub.docker.com,registry-1.docker.io,auth.docker.io,registry.docker.io"
echo "Docker proxy settings cleared"
echo "You may need to restart Docker Desktop for changes to take effect"
