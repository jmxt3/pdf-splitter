@echo off
REM PDF Splitter CLI - Automatic PATH Installation Script
REM This script installs pdf-splitter.exe to C:\Tools and adds it to PATH

echo.
echo PDF Splitter CLI - PATH Installation
echo ===================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator
    echo.
    echo Right-click this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

REM Check if pdf-splitter.exe exists in current directory
if not exist "pdf-splitter.exe" (
    echo ERROR: pdf-splitter.exe not found in current directory
    echo.
    echo Please make sure this script is in the same folder as pdf-splitter.exe
    echo.
    pause
    exit /b 1
)

echo [1/4] Creating C:\Tools directory...
if not exist "C:\Tools" (
    mkdir "C:\Tools"
    echo     Created C:\Tools
) else (
    echo     C:\Tools already exists
)

echo.
echo [2/4] Copying pdf-splitter.exe to C:\Tools...
copy "pdf-splitter.exe" "C:\Tools\pdf-splitter.exe" >nul
if %errorLevel% equ 0 (
    echo     Successfully copied to C:\Tools\pdf-splitter.exe
) else (
    echo     ERROR: Failed to copy file
    pause
    exit /b 1
)

echo.
echo [3/4] Adding C:\Tools to system PATH...
REM Get current PATH
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>nul') do set "currentPath=%%b"

REM Check if C:\Tools is already in PATH
echo %currentPath% | find /i "C:\Tools" >nul
if %errorLevel% equ 0 (
    echo     C:\Tools is already in PATH
) else (
    REM Add C:\Tools to PATH
    setx PATH "%currentPath%;C:\Tools" /M >nul
    if %errorLevel% equ 0 (
        echo     Successfully added C:\Tools to system PATH
    ) else (
        echo     ERROR: Failed to update PATH
        pause
        exit /b 1
    )
)

echo.
echo [4/4] Verifying installation...
if exist "C:\Tools\pdf-splitter.exe" (
    echo     pdf-splitter.exe found at C:\Tools\pdf-splitter.exe
) else (
    echo     ERROR: Verification failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS: Installation completed!
echo ========================================
echo.
echo Next steps:
echo 1. Close this window
echo 2. Open a NEW Command Prompt or PowerShell
echo 3. Type: pdf-splitter --help
echo 4. You can now use 'pdf-splitter' from any folder!
echo.
echo Examples:
echo   pdf-splitter document.pdf
echo   pdf-splitter large-file.pdf -p 10
echo   pdf-splitter report.pdf -o my-chunks
echo.
echo Note: You must open a NEW terminal window for PATH changes to take effect
echo.
pause
