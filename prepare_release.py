#!/usr/bin/env python3
"""
Release preparation script for PDF Splitter CLI
Helps prepare files for GitHub Releases
"""

import os
import shutil
import zipfile
from pathlib import Path
import hashlib

def calculate_sha256(file_path):
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def get_version():
    """Get version from pyproject.toml."""
    try:
        with open("pyproject.toml", "r") as f:
            for line in f:
                if line.strip().startswith('version = '):
                    return line.split('"')[1]
    except FileNotFoundError:
        return "0.1.1"  # fallback
    return "unknown"

def prepare_release_files():
    """Prepare files for GitHub release."""
    version = get_version()
    print(f"📦 Preparing release files for version {version}")
    
    # Create release preparation directory
    prep_dir = Path("release_prep")
    prep_dir.mkdir(exist_ok=True)
    
    # Platform mappings
    platforms = {
        "windows": {"exe": "pdf-splitter.exe", "suffix": "windows-x64.exe"},
        "macos": {"exe": "pdf-splitter", "suffix": "macos-universal"},
        "linux": {"exe": "pdf-splitter", "suffix": "linux-x64"}
    }
    
    checksums = []
    
    for platform, info in platforms.items():
        platform_dir = Path("release") / platform
        if not platform_dir.exists():
            print(f"⚠️  {platform} release not found at {platform_dir}")
            continue
            
        exe_path = platform_dir / info["exe"]
        if not exe_path.exists():
            print(f"⚠️  {platform} executable not found at {exe_path}")
            continue
            
        # Copy and rename executable
        new_name = f"pdf-splitter-v{version}-{info['suffix']}"
        dest_path = prep_dir / new_name
        shutil.copy2(exe_path, dest_path)
        
        # Calculate checksum
        checksum = calculate_sha256(dest_path)
        checksums.append(f"{checksum}  {new_name}")
        
        size_mb = dest_path.stat().st_size / (1024 * 1024)
        print(f"✅ {platform}: {new_name} ({size_mb:.1f} MB)")

    # Copy installation scripts for Windows
    if Path("install_to_path.bat").exists():
        shutil.copy2("install_to_path.bat", prep_dir)
        print("✅ Copied install_to_path.bat")

    if Path("install_to_path.ps1").exists():
        shutil.copy2("install_to_path.ps1", prep_dir)
        print("✅ Copied install_to_path.ps1")

    # Create checksums file
    checksums_file = prep_dir / "SHA256SUMS.txt"
    with open(checksums_file, "w", encoding="utf-8") as f:
        f.write(f"# SHA256 Checksums for PDF Splitter CLI v{version}\n")
        f.write(f"# Generated automatically\n\n")
        for checksum in checksums:
            f.write(checksum + "\n")
    
    print(f"✅ Checksums written to {checksums_file}")
    
    # Create release notes template
    notes_file = prep_dir / "release_notes.md"
    with open(notes_file, "w", encoding="utf-8") as f:
        f.write(f"""# PDF Splitter CLI v{version}

## 🚀 What's New
- [Add your changes here]

## 📥 Downloads

### For Non-Technical Users (Recommended)
Choose the file for your operating system:

- **Windows**: `pdf-splitter-v{version}-windows-x64.exe`
- **macOS**: `pdf-splitter-v{version}-macos-universal`
- **Linux**: `pdf-splitter-v{version}-linux-x64`

### For Python Developers
```bash
pip install pdf-splitter-cli=={version}
```

## 🔧 Quick Start

### Windows
1. Download `pdf-splitter-v{version}-windows-x64.exe`
2. Open Command Prompt or PowerShell
3. Run: `pdf-splitter-v{version}-windows-x64.exe document.pdf`

### macOS/Linux
1. Download the appropriate file
2. Make it executable: `chmod +x pdf-splitter-v{version}-*`
3. Run: `./pdf-splitter-v{version}-* document.pdf`

## ✨ Features
- Split PDF files into smaller chunks
- Real-time progress bars with ETA
- Automatic filename generation
- Cross-platform compatibility
- Memory-efficient processing for large files

## 📋 Usage Examples
```bash
# Basic usage - split every 5 pages
pdf-splitter document.pdf

# Custom chunk size
pdf-splitter document.pdf -p 10

# Custom output folder
pdf-splitter document.pdf -o my_chunks

# Split into individual pages
pdf-splitter document.pdf -p 1
```

## 🔐 File Verification

Verify your downloads using SHA256 checksums:

```bash
# Windows (PowerShell)
Get-FileHash pdf-splitter-v{version}-windows-x64.exe -Algorithm SHA256

# macOS/Linux
sha256sum pdf-splitter-v{version}-*
```

Compare with checksums in `SHA256SUMS.txt`.

## 🐛 Issues
Report bugs at: https://github.com/jmxt3/pdf-splitter/issues

## 📄 Full Documentation
See: https://github.com/jmxt3/pdf-splitter#readme
""")
    
    print(f"✅ Release notes template written to {notes_file}")
    
    # Create upload instructions
    instructions_file = prep_dir / "UPLOAD_INSTRUCTIONS.md"
    with open(instructions_file, "w", encoding="utf-8") as f:
        f.write(f"""# Upload Instructions for v{version}

## Files to Upload to GitHub Release

1. `pdf-splitter-v{version}-windows-x64.exe`
2. `pdf-splitter-v{version}-macos-universal`
3. `pdf-splitter-v{version}-linux-x64`
4. `install_to_path.bat` (Windows PATH installer)
5. `install_to_path.ps1` (Windows PowerShell installer)
6. `SHA256SUMS.txt`

## Steps

1. Go to https://github.com/jmxt3/pdf-splitter/releases
2. Click "Create a new release"
3. Tag: `v{version}`
4. Title: `PDF Splitter CLI v{version} - Standalone Executables`
5. Copy content from `release_notes.md`
6. Upload all files listed above
7. Check "Set as the latest release"
8. Click "Publish release"

## After Publishing

1. Test downloads on different platforms
2. Update main README.md if needed
3. Announce the release
""")
    
    print(f"✅ Upload instructions written to {instructions_file}")
    
    print(f"\n🎉 Release preparation complete!")
    print(f"📁 Files ready in: {prep_dir}")
    print(f"📋 Next steps:")
    print(f"   1. Review {notes_file}")
    print(f"   2. Follow {instructions_file}")
    print(f"   3. Upload files to GitHub Releases")

def main():
    """Main function."""
    print("🚀 PDF Splitter CLI - Release Preparation")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ pyproject.toml not found. Run this script from the project root.")
        return
    
    # Check if release directory exists
    if not Path("release").exists():
        print("❌ release/ directory not found. Build executables first.")
        print("   Run: powershell -ExecutionPolicy Bypass -File build_executable.ps1")
        return
    
    prepare_release_files()

if __name__ == "__main__":
    main()
