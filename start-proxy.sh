#!/bin/bash

echo "Starting Coplay GLM Proxy Server..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7 or higher and try again"
    exit 1
fi

# Check if requirements are installed
if ! python3 -c "import aiohttp" &> /dev/null; then
    echo "Installing required dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
fi

# Start the proxy server
echo "Starting proxy server..."
echo
python3 coplay-glm-proxy.py

# If the script exits, show exit status
exit_code=$?
if [ $exit_code -ne 0 ]; then
    echo
    echo "Proxy server stopped with error code $exit_code. Check the error message above."
fi
