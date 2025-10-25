@echo off
echo Starting Coplay GLM Proxy Server...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher and try again
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import aiohttp" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Start the proxy server
echo Starting proxy server...
echo.
python coplay-glm-proxy.py

REM If the script exits, pause to read any error messages
if errorlevel 1 (
    echo.
    echo Proxy server stopped with an error. Check the error message above.
    pause
)
