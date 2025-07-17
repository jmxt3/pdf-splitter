# PDF Splitter CLI - Automatic PATH Installation Script (PowerShell)
# This script installs pdf-splitter.exe to C:\Tools and adds it to PATH

Write-Host ""
Write-Host "PDF Splitter CLI - PATH Installation" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "ERROR: This script must be run as Administrator" -ForegroundColor Red
    Write-Host ""
    Write-Host "Right-click PowerShell and select 'Run as administrator'" -ForegroundColor Yellow
    Write-Host "Then run this script again" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if pdf-splitter.exe exists in current directory
if (-not (Test-Path "pdf-splitter.exe")) {
    Write-Host "ERROR: pdf-splitter.exe not found in current directory" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please make sure this script is in the same folder as pdf-splitter.exe" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[1/4] Creating C:\Tools directory..." -ForegroundColor Cyan
if (-not (Test-Path "C:\Tools")) {
    New-Item -ItemType Directory -Path "C:\Tools" -Force | Out-Null
    Write-Host "    Created C:\Tools" -ForegroundColor Green
} else {
    Write-Host "    C:\Tools already exists" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[2/4] Copying pdf-splitter.exe to C:\Tools..." -ForegroundColor Cyan
try {
    Copy-Item "pdf-splitter.exe" "C:\Tools\pdf-splitter.exe" -Force
    Write-Host "    Successfully copied to C:\Tools\pdf-splitter.exe" -ForegroundColor Green
} catch {
    Write-Host "    ERROR: Failed to copy file - $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[3/4] Adding C:\Tools to system PATH..." -ForegroundColor Cyan

# Get current system PATH
$currentPath = [Environment]::GetEnvironmentVariable("PATH", [EnvironmentVariableTarget]::Machine)

# Check if C:\Tools is already in PATH
if ($currentPath -like "*C:\Tools*") {
    Write-Host "    C:\Tools is already in PATH" -ForegroundColor Yellow
} else {
    try {
        # Add C:\Tools to PATH
        $newPath = $currentPath + ";C:\Tools"
        [Environment]::SetEnvironmentVariable("PATH", $newPath, [EnvironmentVariableTarget]::Machine)
        Write-Host "    Successfully added C:\Tools to system PATH" -ForegroundColor Green
    } catch {
        Write-Host "    ERROR: Failed to update PATH - $_" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "[4/4] Verifying installation..." -ForegroundColor Cyan
if (Test-Path "C:\Tools\pdf-splitter.exe") {
    Write-Host "    pdf-splitter.exe found at C:\Tools\pdf-splitter.exe" -ForegroundColor Green
} else {
    Write-Host "    ERROR: Verification failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "SUCCESS: Installation completed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Close this PowerShell window" -ForegroundColor White
Write-Host "2. Open a NEW Command Prompt or PowerShell" -ForegroundColor White
Write-Host "3. Type: pdf-splitter --help" -ForegroundColor White
Write-Host "4. You can now use 'pdf-splitter' from any folder!" -ForegroundColor White
Write-Host ""
Write-Host "Examples:" -ForegroundColor Yellow
Write-Host "  pdf-splitter document.pdf" -ForegroundColor White
Write-Host "  pdf-splitter large-file.pdf -p 10" -ForegroundColor White
Write-Host "  pdf-splitter report.pdf -o my-chunks" -ForegroundColor White
Write-Host ""
Write-Host "Note: You must open a NEW terminal window for PATH changes to take effect" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to exit"
