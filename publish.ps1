# PDF Splitter CLI - Publishing Script (PowerShell)
# This script automates the publishing process to PyPI

$ErrorActionPreference = "Stop"

Write-Host "🚀 PDF Splitter CLI - Publishing Script" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path ".venv")) {
    Write-Host "❌ Virtual environment not found at .venv" -ForegroundColor Red
    Write-Host "🔧 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Note: We'll use uv run instead of activating venv directly
Write-Host "🔧 Using uv for dependency management..." -ForegroundColor Yellow

# Check if uv is available and sync dependencies
if (Get-Command uv -ErrorAction SilentlyContinue) {
    Write-Host "🔧 Running uv sync to fix dependencies..." -ForegroundColor Yellow
    uv sync
    $PYTHON_CMD = "uv run python"
    $BUILD_CMD = "uv run python -m build"
    $TWINE_CMD = "uv run twine"
} else {
    Write-Host "⚠️  uv not found, installing dependencies with pip..." -ForegroundColor Yellow
    python -m pip install -e ".[dev]"
    $PYTHON_CMD = "python"
    $BUILD_CMD = "python -m build"
    $TWINE_CMD = "twine"
}

# Prompt for version update
Write-Host ""
Write-Host "📝 Current version in pyproject.toml:" -ForegroundColor Cyan
Select-String -Path "pyproject.toml" -Pattern 'version = '

Write-Host ""
$update_version = Read-Host "Do you want to update the version? (y/N)"
if ($update_version -match "^[Yy]$") {
    $new_version = Read-Host "Enter new version (e.g., 0.1.2)"
    if ($new_version) {
        # Update version in pyproject.toml
        (Get-Content pyproject.toml) -replace 'version = ".*"', "version = `"$new_version`"" | Set-Content pyproject.toml
        Write-Host "✅ Updated version to $new_version" -ForegroundColor Green
    }
}

# Clean previous builds
Write-Host ""
Write-Host "🧹 Cleaning previous builds..." -ForegroundColor Yellow
Remove-Item -Path "dist", "build", "*.egg-info" -Recurse -Force -ErrorAction SilentlyContinue

# Build the package
Write-Host "🔨 Building package..." -ForegroundColor Yellow
Invoke-Expression $BUILD_CMD

# Check package
Write-Host "🔍 Checking package..." -ForegroundColor Yellow
Invoke-Expression "$TWINE_CMD check dist/*"

# Show built files
Write-Host ""
Write-Host "📦 Built files:" -ForegroundColor Cyan
Get-ChildItem dist

# Ask for publishing preference
Write-Host ""
Write-Host "🚀 Publishing Options:" -ForegroundColor Green
Write-Host "1. Test PyPI only"
Write-Host "2. Production PyPI only"
Write-Host "3. Test PyPI first, then Production"
Write-Host "4. Skip publishing"

$publish_option = Read-Host "Choose option (1-4)"

switch ($publish_option) {
    "1" {
        Write-Host "📤 Uploading to Test PyPI..." -ForegroundColor Yellow
        Invoke-Expression "$TWINE_CMD upload --repository testpypi dist/*"
        Write-Host "✅ Published to Test PyPI: https://test.pypi.org/project/pdf-splitter-cli/" -ForegroundColor Green
    }
    "2" {
        Write-Host "📤 Uploading to Production PyPI..." -ForegroundColor Yellow
        Invoke-Expression "$TWINE_CMD upload dist/*"
        Write-Host "✅ Published to Production PyPI: https://pypi.org/project/pdf-splitter-cli/" -ForegroundColor Green
    }
    "3" {
        Write-Host "📤 Uploading to Test PyPI first..." -ForegroundColor Yellow
        Invoke-Expression "$TWINE_CMD upload --repository testpypi dist/*"
        Write-Host "✅ Published to Test PyPI: https://test.pypi.org/project/pdf-splitter-cli/" -ForegroundColor Green
        Write-Host ""
        $upload_prod = Read-Host "Test successful? Upload to Production PyPI? (y/N)"
        if ($upload_prod -match "^[Yy]$") {
            Write-Host "📤 Uploading to Production PyPI..." -ForegroundColor Yellow
            Invoke-Expression "$TWINE_CMD upload dist/*"
            Write-Host "✅ Published to Production PyPI: https://pypi.org/project/pdf-splitter-cli/" -ForegroundColor Green
        }
    }
    "4" {
        Write-Host "⏭️  Skipping publishing" -ForegroundColor Yellow
    }
    default {
        Write-Host "❌ Invalid option" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "🎉 Publishing process completed!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "- Test installation: pip install pdf-splitter-cli"
Write-Host "- Verify functionality: pdf-splitter --help"
Write-Host "- Check PyPI page for updates"
