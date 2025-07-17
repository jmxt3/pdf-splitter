# PDF Splitter CLI - Windows Executable Builder
# Creates a standalone .exe file for non-technical users

$ErrorActionPreference = "Stop"

Write-Host "PDF Splitter CLI - Windows Executable Builder" -ForegroundColor Green
Write-Host "=" * 55 -ForegroundColor Green

# Check if uv is available
Write-Host "[INFO] Checking dependencies..." -ForegroundColor Yellow
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] uv not found. Please install uv first." -ForegroundColor Red
    Write-Host "   Visit: https://docs.astral.sh/uv/getting-started/installation/" -ForegroundColor Yellow
    exit 1
}
Write-Host "[OK] uv is available" -ForegroundColor Green

# Check if main.py exists
if (-not (Test-Path "main.py")) {
    Write-Host "[ERROR] main.py not found in current directory" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] main.py found" -ForegroundColor Green

# Sync dependencies and ensure PyInstaller is available
Write-Host "[INFO] Syncing dependencies..." -ForegroundColor Yellow
uv sync

# Clean previous builds
Write-Host "[INFO] Cleaning previous build artifacts..." -ForegroundColor Yellow
Remove-Item -Path "build", "dist", "__pycache__", "*.spec" -Recurse -Force -ErrorAction SilentlyContinue

# Build the executable
Write-Host "[INFO] Building Windows executable..." -ForegroundColor Yellow
Write-Host "   This may take a few minutes..." -ForegroundColor Gray

try {
    uv run pyinstaller --onefile --name pdf-splitter --console main.py
    Write-Host "[OK] Build completed successfully" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Build failed: $_" -ForegroundColor Red
    exit 1
}

# Check if executable was created
$exePath = "dist\pdf-splitter.exe"
if (Test-Path $exePath) {
    $size = (Get-Item $exePath).Length / 1MB
    $sizeRounded = [math]::Round($size, 1)
    Write-Host "[OK] Executable created: $exePath ($sizeRounded MB)" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Executable not found at $exePath" -ForegroundColor Red
    exit 1
}

# Test the executable
Write-Host "[INFO] Testing executable..." -ForegroundColor Yellow
try {
    $testResult = & $exePath --help
    if ($testResult -match "Split a PDF file into multiple smaller PDF files") {
        Write-Host "[OK] Executable test passed" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Executable test failed - unexpected output" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "[ERROR] Executable test failed: $_" -ForegroundColor Red
    exit 1
}

# Create release package
Write-Host "[INFO] Creating release package..." -ForegroundColor Yellow
$releaseDir = "release\windows"
New-Item -ItemType Directory -Path $releaseDir -Force | Out-Null
Copy-Item $exePath $releaseDir

# Copy installation scripts
Copy-Item "install_to_path.bat" $releaseDir -ErrorAction SilentlyContinue
Copy-Item "install_to_path.ps1" $releaseDir -ErrorAction SilentlyContinue

# Create README for the release
$readmeContent = @"
# PDF Splitter CLI - Windows Release

## Quick Start

1. Download the `pdf-splitter.exe` file
2. Open Command Prompt or PowerShell
3. Navigate to the folder containing the executable
4. Run the executable:

``````
# Show help
pdf-splitter.exe --help

# Split a PDF into 5-page chunks (default)
pdf-splitter.exe document.pdf

# Split into 10-page chunks
pdf-splitter.exe document.pdf -p 10

# Split into custom output folder
pdf-splitter.exe document.pdf -o my_output
``````

## Features

- ✅ No Python installation required
- ✅ Standalone executable (includes everything needed)
- ✅ Progress bars with estimated time remaining
- ✅ Automatic output file naming
- ✅ Handles large PDF files efficiently
- ✅ Works on Windows 10/11

## File Size

Executable size: $sizeRounded MB

## Example Usage

``````
# Basic usage - split into 5-page chunks
pdf-splitter.exe my-document.pdf

# Custom page count
pdf-splitter.exe large-report.pdf -p 20

# Custom output folder
pdf-splitter.exe presentation.pdf -o split-slides

# Disable progress bars (for automation)
pdf-splitter.exe document.pdf --no-progress
``````

## Troubleshooting

- **Windows Defender Warning**: The executable might trigger a warning because it's not digitally signed. Click "More info" → "Run anyway"
- **Antivirus Software**: Some antivirus programs may flag PyInstaller executables. Add an exception if needed
- **Large Files**: For very large PDFs (>1GB), the process may take several minutes

## Support

For issues and updates, visit: https://github.com/jmxt3/pdf-splitter
"@

$readmePath = "$releaseDir\README.md"
$readmeContent | Out-File -FilePath $readmePath -Encoding UTF8

Write-Host ""
Write-Host "[SUCCESS] Build completed successfully!" -ForegroundColor Green
Write-Host "Executable: $exePath" -ForegroundColor Cyan
Write-Host "Release package: $releaseDir" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Test the executable with your PDF files" -ForegroundColor White
Write-Host "2. Upload to GitHub Releases for distribution" -ForegroundColor White
Write-Host "3. Update README.md with download instructions" -ForegroundColor White
Write-Host ""
Write-Host "To test the executable:" -ForegroundColor Yellow
Write-Host "   $exePath --help" -ForegroundColor White
