#!/bin/bash

# PDF Splitter CLI - Publishing Script
# This script automates the publishing process to PyPI

set -e  # Exit on any error

echo "🚀 PDF Splitter CLI - Publishing Script"
echo "======================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found at .venv"
    echo "🔧 Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
# Check if we're on Windows (Git Bash/WSL) or Unix
if [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Check if uv is available and sync dependencies
# Try to find uv in common Windows locations
UV_PATH=""
if command -v uv &> /dev/null; then
    UV_PATH="uv"
elif [ -f "/c/Users/$USER/.cargo/bin/uv.exe" ]; then
    UV_PATH="/c/Users/$USER/.cargo/bin/uv.exe"
elif [ -f "/c/Users/$USER/AppData/Roaming/uv/uv.exe" ]; then
    UV_PATH="/c/Users/$USER/AppData/Roaming/uv/uv.exe"
fi

if [ ! -z "$UV_PATH" ]; then
    echo "🔧 Running uv sync to fix dependencies..."
    $UV_PATH sync
    # Use uv for subsequent commands
    PYTHON_CMD="$UV_PATH run python"
    BUILD_CMD="$UV_PATH run python -m build"
    TWINE_CMD="$UV_PATH run twine"
else
    echo "⚠️  uv not found, installing dependencies with pip..."
    python -m pip install -e ".[dev]"
    # Use regular commands
    PYTHON_CMD="python"
    BUILD_CMD="python -m build"
    TWINE_CMD="twine"
fi

# Prompt for version update
echo ""
echo "📝 Current version in pyproject.toml:"
grep 'version = ' pyproject.toml

echo ""
read -p "Do you want to update the version? (y/N): " update_version
if [[ $update_version =~ ^[Yy]$ ]]; then
    read -p "Enter new version (e.g., 0.1.2): " new_version
    if [ ! -z "$new_version" ]; then
        # Update version in pyproject.toml
        sed -i.bak "s/version = \".*\"/version = \"$new_version\"/" pyproject.toml
        echo "✅ Updated version to $new_version"
        rm pyproject.toml.bak 2>/dev/null || true
    fi
fi

# Clean previous builds
echo ""
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Build the package
echo "🔨 Building package..."
$BUILD_CMD

# Check package
echo "🔍 Checking package..."
$TWINE_CMD check dist/*

# Show built files
echo ""
echo "📦 Built files:"
ls -la dist/

# Ask for publishing preference
echo ""
echo "🚀 Publishing Options:"
echo "1. Test PyPI only"
echo "2. Production PyPI only"
echo "3. Test PyPI first, then Production"
echo "4. Skip publishing"

read -p "Choose option (1-4): " publish_option

case $publish_option in
    1)
        echo "📤 Uploading to Test PyPI..."
        $TWINE_CMD upload --repository testpypi dist/*
        echo "✅ Published to Test PyPI: https://test.pypi.org/project/pdf-splitter-cli/"
        ;;
    2)
        echo "📤 Uploading to Production PyPI..."
        $TWINE_CMD upload dist/*
        echo "✅ Published to Production PyPI: https://pypi.org/project/pdf-splitter-cli/"
        ;;
    3)
        echo "📤 Uploading to Test PyPI first..."
        $TWINE_CMD upload --repository testpypi dist/*
        echo "✅ Published to Test PyPI: https://test.pypi.org/project/pdf-splitter-cli/"
        echo ""
        read -p "Test successful? Upload to Production PyPI? (y/N): " upload_prod
        if [[ $upload_prod =~ ^[Yy]$ ]]; then
            echo "📤 Uploading to Production PyPI..."
            $TWINE_CMD upload dist/*
            echo "✅ Published to Production PyPI: https://pypi.org/project/pdf-splitter-cli/"
        fi
        ;;
    4)
        echo "⏭️  Skipping publishing"
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "🎉 Publishing process completed!"
echo ""
echo "📋 Next steps:"
echo "- Test installation: pip install pdf-splitter-cli"
echo "- Verify functionality: pdf-splitter --help"
echo "- Check PyPI page for updates"
