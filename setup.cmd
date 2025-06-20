@echo off
title Setup Environment for BehaviorStealer
color 0B

echo ===============================================
echo       BehaviorStealer Setup Script
echo ===============================================

echo Checking Python installation...
python --version >nul 2>&1

if errorlevel 1 (
    echo.
    echo [ERROR] Python is not installed or not added to PATH.
    echo Please install Python 3.x from https://www.python.org/downloads/
    echo then restart this script.
    pause
    exit /b 1
) else (
    echo [OK] Python detected.
)

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing required Python packages...
pip install --no-cache-dir requests psutil pillow opencv-python pywin32 pycryptodome

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install one or more packages.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
) else (
    echo [OK] All packages installed successfully.
)

echo.
echo Setup completed successfully!
echo You can now run your BehaviorStealer project.
pause
