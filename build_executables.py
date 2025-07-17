#!/usr/bin/env python3
"""
Cross-platform executable builder for PDF Splitter CLI
Creates standalone executables for Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and handle errors."""
    print(f"🔧 {description}")
    print(f"   Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e}")
        print(f"   Output: {e.stdout}")
        print(f"   Error Output: {e.stderr}")
        sys.exit(1)

def check_dependencies():
    """Check if required tools are available."""
    print("🔍 Checking dependencies...")
    
    # Check if PyInstaller is available
    try:
        subprocess.run(["pyinstaller", "--version"], check=True, capture_output=True)
        print("✅ PyInstaller is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ PyInstaller not found. Installing...")
        run_command(["uv", "add", "--group", "dev", "pyinstaller"], "Installing PyInstaller")
    
    # Check if main.py exists
    if not Path("main.py").exists():
        print("❌ main.py not found in current directory")
        sys.exit(1)
    print("✅ main.py found")

def clean_build_artifacts():
    """Clean previous build artifacts."""
    print("🧹 Cleaning previous build artifacts...")
    
    artifacts = ["build", "dist", "__pycache__", "*.spec"]
    for artifact in artifacts:
        if artifact.startswith("*"):
            # Handle glob patterns
            import glob
            for file in glob.glob(artifact):
                if os.path.isfile(file):
                    os.remove(file)
                    print(f"   Removed: {file}")
        else:
            if os.path.exists(artifact):
                if os.path.isdir(artifact):
                    shutil.rmtree(artifact)
                else:
                    os.remove(artifact)
                print(f"   Removed: {artifact}")

def get_platform_info():
    """Get current platform information."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        return "windows", "exe"
    elif system == "darwin":
        return "macos", "app" if machine == "arm64" else "app"
    elif system == "linux":
        return "linux", "bin"
    else:
        return system, "bin"

def build_executable(platform_name, extension):
    """Build executable for the current platform."""
    print(f"🔨 Building executable for {platform_name}...")
    
    # Determine output name
    if platform_name == "windows":
        output_name = "pdf-splitter.exe"
    elif platform_name == "macos":
        output_name = "pdf-splitter"
    else:
        output_name = "pdf-splitter"
    
    # PyInstaller command
    cmd = [
        "uv", "run", "pyinstaller",
        "--onefile",
        "--name", "pdf-splitter",
        "--console",
        "main.py"
    ]
    
    # Add platform-specific options
    if platform_name == "macos":
        cmd.extend(["--osx-bundle-identifier", "com.jmachete.pdf-splitter"])
    
    run_command(cmd, f"Building {platform_name} executable")
    
    # Check if executable was created
    dist_path = Path("dist") / output_name
    if dist_path.exists():
        size_mb = dist_path.stat().st_size / (1024 * 1024)
        print(f"✅ Executable created: {dist_path} ({size_mb:.1f} MB)")
        return dist_path
    else:
        print(f"❌ Executable not found at {dist_path}")
        sys.exit(1)

def test_executable(executable_path):
    """Test the built executable."""
    print(f"🧪 Testing executable: {executable_path}")
    
    try:
        result = subprocess.run([str(executable_path), "--help"], 
                              check=True, capture_output=True, text=True, timeout=30)
        if "Split a PDF file into multiple smaller PDF files" in result.stdout:
            print("✅ Executable test passed")
            return True
        else:
            print("❌ Executable test failed - unexpected output")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Executable test timed out")
        return False
    except Exception as e:
        print(f"❌ Executable test failed: {e}")
        return False

def create_release_package(executable_path, platform_name):
    """Create a release package with the executable."""
    print(f"📦 Creating release package for {platform_name}...")
    
    # Create release directory
    release_dir = Path("release") / platform_name
    release_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy executable
    dest_path = release_dir / executable_path.name
    shutil.copy2(executable_path, dest_path)
    
    # Create README for the release
    readme_content = f"""# PDF Splitter CLI - {platform_name.title()} Release

## Quick Start

1. Download the executable file
2. Open a terminal/command prompt
3. Run the executable:

```bash
# Show help
./{executable_path.name} --help

# Split a PDF into 5-page chunks (default)
./{executable_path.name} document.pdf

# Split into 10-page chunks
./{executable_path.name} document.pdf -p 10

# Split into custom output folder
./{executable_path.name} document.pdf -o my_output
```

## Features

- ✅ No Python installation required
- ✅ Standalone executable
- ✅ Progress bars with ETA
- ✅ Automatic output file naming
- ✅ Handles large PDF files
- ✅ Cross-platform compatibility

## File Size

Executable size: {dest_path.stat().st_size / (1024 * 1024):.1f} MB

## Support

For issues and updates, visit: https://github.com/jmxt3/pdf-splitter
"""
    
    readme_path = release_dir / "README.md"
    readme_path.write_text(readme_content)
    
    print(f"✅ Release package created: {release_dir}")
    return release_dir

def main():
    """Main build process."""
    print("🚀 PDF Splitter CLI - Executable Builder")
    print("=" * 50)
    
    # Check dependencies
    check_dependencies()
    
    # Clean previous builds
    clean_build_artifacts()
    
    # Get platform info
    platform_name, extension = get_platform_info()
    print(f"🖥️  Building for platform: {platform_name}")
    
    # Build executable
    executable_path = build_executable(platform_name, extension)
    
    # Test executable
    if test_executable(executable_path):
        # Create release package
        release_dir = create_release_package(executable_path, platform_name)
        
        print("\n🎉 Build completed successfully!")
        print(f"📁 Executable: {executable_path}")
        print(f"📦 Release package: {release_dir}")
        print("\n📋 Next steps:")
        print("1. Test the executable with your PDF files")
        print("2. Upload to GitHub Releases for distribution")
        print("3. Update documentation with download links")
    else:
        print("\n❌ Build failed - executable test did not pass")
        sys.exit(1)

if __name__ == "__main__":
    main()
