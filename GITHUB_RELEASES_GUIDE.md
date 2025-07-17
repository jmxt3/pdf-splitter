# GitHub Releases Guide for PDF Splitter CLI

This guide explains how to distribute standalone executables through GitHub Releases for non-technical users.

## 📋 Overview

GitHub Releases allows you to:
- Distribute standalone executables without requiring Python
- Provide version-specific downloads
- Include release notes and documentation
- Offer multiple platform binaries (Windows, macOS, Linux)

## 🔨 Building Executables

### Step 1: Build for Your Platform

#### Windows
```powershell
# Build Windows executable
powershell -ExecutionPolicy Bypass -File build_executable.ps1
```

#### macOS/Linux
```bash
# Build executable for current platform
./build_executable.sh
```

### Step 2: Cross-Platform Building

For complete releases, you'll need to build on each platform:

1. **Windows**: Build on Windows machine or Windows VM
2. **macOS**: Build on macOS machine (required for code signing)
3. **Linux**: Build on Linux machine or use Docker

## 📦 Preparing Release Assets

After building, you'll have:

```
release/
├── windows/
│   ├── pdf-splitter.exe
│   └── README.md
├── macos/
│   ├── pdf-splitter
│   └── README.md
└── linux/
    ├── pdf-splitter
    └── README.md
```

### Recommended File Naming

For GitHub Releases, use descriptive names:

- `pdf-splitter-v0.1.1-windows-x64.exe`
- `pdf-splitter-v0.1.1-macos-universal`
- `pdf-splitter-v0.1.1-linux-x64`

## 🚀 Creating a GitHub Release

### Step 1: Tag the Release

```bash
# Create and push a new tag
git tag v0.1.1
git push origin v0.1.1
```

### Step 2: Create Release on GitHub

1. Go to your repository on GitHub
2. Click "Releases" in the right sidebar
3. Click "Create a new release"
4. Select your tag (v0.1.1)
5. Fill in the release information:

#### Release Title
```
PDF Splitter CLI v0.1.1 - Standalone Executables
```

#### Release Description Template
```markdown
# PDF Splitter CLI v0.1.1

## 🚀 What's New
- Standalone executables for Windows, macOS, and Linux
- No Python installation required
- Single-file download and run

## 📥 Downloads

### For Non-Technical Users (Recommended)
Choose the file for your operating system:

- **Windows**: `pdf-splitter-v0.1.1-windows-x64.exe`
- **macOS**: `pdf-splitter-v0.1.1-macos-universal`
- **Linux**: `pdf-splitter-v0.1.1-linux-x64`

### For Python Developers
```bash
pip install pdf-splitter-cli==0.1.1
```

## 🔧 Quick Start

### Windows
1. Download `pdf-splitter-v0.1.1-windows-x64.exe`
2. Open Command Prompt or PowerShell
3. Run: `pdf-splitter-v0.1.1-windows-x64.exe document.pdf`

### macOS/Linux
1. Download the appropriate file
2. Make it executable: `chmod +x pdf-splitter-v0.1.1-*`
3. Run: `./pdf-splitter-v0.1.1-* document.pdf`

## ✨ Features
- Split PDF files into smaller chunks
- Real-time progress bars
- Automatic filename generation
- Cross-platform compatibility
- Memory-efficient processing

## 📋 Usage Examples
```bash
# Basic usage - split every 5 pages
pdf-splitter document.pdf

# Custom chunk size
pdf-splitter document.pdf -p 10

# Custom output folder
pdf-splitter document.pdf -o my_chunks
```

## 🐛 Issues
Report bugs at: https://github.com/jmxt3/pdf-splitter/issues

## 📄 Full Documentation
See: https://github.com/jmxt3/pdf-splitter#readme
```

### Step 3: Upload Assets

1. Drag and drop or click to upload your executable files
2. Upload all platform versions
3. Include the README files from each platform folder

### Step 4: Publish Release

1. Check "Set as the latest release" if this is the newest version
2. Click "Publish release"

## 🔄 Automation Options

### GitHub Actions (Advanced)

You can automate building and releasing with GitHub Actions:

```yaml
# .github/workflows/release.yml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install uv
        run: pip install uv
      - name: Build executable
        run: powershell -ExecutionPolicy Bypass -File build_executable.ps1
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: windows-executable
          path: release/windows/

  # Similar jobs for macOS and Linux...
```

## 📊 Best Practices

### File Sizes
- Windows executable: ~10-15 MB
- macOS executable: ~12-18 MB  
- Linux executable: ~10-15 MB

### Security Considerations
- Executables may trigger antivirus warnings (false positives)
- Consider code signing for Windows/macOS (requires certificates)
- Include SHA256 checksums for verification

### Documentation
- Always include platform-specific README files
- Provide clear installation instructions
- Include troubleshooting section

## 🎯 Success Metrics

A successful release should have:
- ✅ All platform executables uploaded
- ✅ Clear download instructions
- ✅ Working executables (test before release)
- ✅ Proper version tagging
- ✅ Release notes with examples

## 🔗 Next Steps

After creating the release:
1. Test downloads on different platforms
2. Update main README.md with release links
3. Announce on relevant platforms
4. Monitor for user feedback and issues

## 📞 Support

For questions about releases:
- Open an issue on GitHub
- Check existing documentation
- Review previous release patterns
