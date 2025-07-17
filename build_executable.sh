#!/bin/bash
# PDF Splitter CLI - Unix/Linux/macOS Executable Builder
# Creates a standalone executable for non-technical users

set -e  # Exit on any error

echo "🚀 PDF Splitter CLI - Executable Builder"
echo "========================================"

# Detect platform
PLATFORM=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

case $PLATFORM in
    darwin)
        PLATFORM_NAME="macOS"
        EXE_SUFFIX=""
        ;;
    linux)
        PLATFORM_NAME="Linux"
        EXE_SUFFIX=""
        ;;
    *)
        PLATFORM_NAME="Unix"
        EXE_SUFFIX=""
        ;;
esac

echo "🖥️  Building for: $PLATFORM_NAME ($ARCH)"

# Check dependencies
echo "🔍 Checking dependencies..."

if ! command -v uv &> /dev/null; then
    echo "❌ uv not found. Please install uv first."
    echo "   Visit: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi
echo "✅ uv is available"

if [ ! -f "main.py" ]; then
    echo "❌ main.py not found in current directory"
    exit 1
fi
echo "✅ main.py found"

# Sync dependencies
echo "🔧 Syncing dependencies..."
uv sync

# Clean previous builds
echo "🧹 Cleaning previous build artifacts..."
rm -rf build dist __pycache__ *.spec

# Build the executable
echo "🔨 Building $PLATFORM_NAME executable..."
echo "   This may take a few minutes..."

if uv run pyinstaller --onefile --name pdf-splitter --console main.py; then
    echo "✅ Build completed successfully"
else
    echo "❌ Build failed"
    exit 1
fi

# Check if executable was created
EXE_PATH="dist/pdf-splitter$EXE_SUFFIX"
if [ -f "$EXE_PATH" ]; then
    SIZE_MB=$(du -m "$EXE_PATH" | cut -f1)
    echo "✅ Executable created: $EXE_PATH (${SIZE_MB} MB)"
else
    echo "❌ Executable not found at $EXE_PATH"
    exit 1
fi

# Make executable (for Unix systems)
chmod +x "$EXE_PATH"

# Test the executable
echo "🧪 Testing executable..."
if timeout 30 "$EXE_PATH" --help | grep -q "Split a PDF file into multiple smaller PDF files"; then
    echo "✅ Executable test passed"
else
    echo "❌ Executable test failed"
    exit 1
fi

# Create release package
echo "📦 Creating release package..."
RELEASE_DIR="release/$PLATFORM"
mkdir -p "$RELEASE_DIR"
cp "$EXE_PATH" "$RELEASE_DIR/"

# Create README for the release
cat > "$RELEASE_DIR/README.md" << EOF
# PDF Splitter CLI - $PLATFORM_NAME Release

## Quick Start

1. Download the \`pdf-splitter\` executable
2. Open a terminal
3. Make the file executable (if needed): \`chmod +x pdf-splitter\`
4. Run the executable:

\`\`\`bash
# Show help
./pdf-splitter --help

# Split a PDF into 5-page chunks (default)
./pdf-splitter document.pdf

# Split into 10-page chunks
./pdf-splitter document.pdf -p 10

# Split into custom output folder
./pdf-splitter document.pdf -o my_output
\`\`\`

## Features

- ✅ No Python installation required
- ✅ Standalone executable (includes everything needed)
- ✅ Progress bars with estimated time remaining
- ✅ Automatic output file naming
- ✅ Handles large PDF files efficiently
- ✅ Cross-platform compatibility

## File Size

Executable size: ${SIZE_MB} MB

## Example Usage

\`\`\`bash
# Basic usage - split into 5-page chunks
./pdf-splitter my-document.pdf

# Custom page count
./pdf-splitter large-report.pdf -p 20

# Custom output folder
./pdf-splitter presentation.pdf -o split-slides

# Disable progress bars (for automation)
./pdf-splitter document.pdf --no-progress
\`\`\`

## Installation

### Option 1: Direct Download
1. Download the \`pdf-splitter\` file
2. Make it executable: \`chmod +x pdf-splitter\`
3. Run it: \`./pdf-splitter document.pdf\`

### Option 2: System-wide Installation
\`\`\`bash
# Copy to a directory in your PATH
sudo cp pdf-splitter /usr/local/bin/
sudo chmod +x /usr/local/bin/pdf-splitter

# Now you can run it from anywhere
pdf-splitter document.pdf
\`\`\`

## Troubleshooting

- **Permission Denied**: Run \`chmod +x pdf-splitter\` to make the file executable
- **Large Files**: For very large PDFs (>1GB), the process may take several minutes
- **Dependencies**: This is a standalone executable with no external dependencies

## Platform Information

- Built for: $PLATFORM_NAME ($ARCH)
- Python version: $(python3 --version 2>/dev/null || echo "Bundled")
- Build date: $(date)

## Support

For issues and updates, visit: https://github.com/jmxt3/pdf-splitter
EOF

echo ""
echo "🎉 Build completed successfully!"
echo "📁 Executable: $EXE_PATH"
echo "📦 Release package: $RELEASE_DIR"
echo ""
echo "📋 Next steps:"
echo "1. Test the executable with your PDF files"
echo "2. Upload to GitHub Releases for distribution"
echo "3. Update README.md with download instructions"
echo ""
echo "🔗 To test the executable:"
echo "   $EXE_PATH --help"
