# PDF Splitter CLI - Windows Release

This guide explains how to add the PDF Splitter executable to the Windows PATH so users can run `pdf-splitter` from anywhere without navigating to the executable folder.

## 🚀 How It Works

### Automatic Installation Process
1. **Download**: User gets both `pdf-splitter.exe` and installation script
2. **Run Script**: Right-click → "Run as administrator" and run the build_executable.ps1
3. **Automatic Setup**:
   - Creates `C:\Tools` directory
   - Copies `pdf-splitter.exe` to `C:\Tools\pdf-splitter.exe`
   - Adds `C:\Tools` to system PATH
   - Verifies installation
4. **Ready to Use**: Open new terminal, type `pdf-splitter --help`

### After PATH Installation
```bash
# User workflow - seamless
1. Download and run installer (once)
2. Open Command Prompt anywhere
3. pdf-splitter document.pdf  # Works everywhere!
```

## 🔧 Technical Implementation

### Directory Structure
```
C:\Tools\                    # Standard location for user tools
└── pdf-splitter.exe        # Renamed from original filename
```

### PATH Environment Variable
- **Scope**: System-wide (all users)
- **Location**: `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment`
- **Value**: Appends `;C:\Tools` to existing PATH

### Error Handling
- ✅ Administrator privilege checking
- ✅ File existence verification
- ✅ Directory creation with error handling
- ✅ PATH duplication prevention
- ✅ Installation verification
- ✅ Clear error messages and solutions

## 📖 Documentation Updates

### Windows README.md
- **Option 1**: Basic usage (original method)
- **Option 2**: Global installation with 3 methods:
  - **Method A**: Automatic installation (recommended)
  - **Method B**: Manual GUI installation
  - **Method C**: Manual command-line installation

### Usage Examples
- Shows both `pdf-splitter.exe` and `pdf-splitter` syntax
- Demonstrates working from any folder
- Includes troubleshooting for PATH issues

### Release Notes
- Updated quick start with PATH installation
- Added verification commands
- Included both installation methods

## 🛠️ Build Integration

### Build Scripts Updated
- `build_executable.ps1` now copies installation scripts
- `prepare_release.py` includes scripts in release package
- Release preparation includes installation scripts

### Release Package Contents
```
release_prep/
├── pdf-splitter-v0.1.1-windows-x64.exe
├── install_to_path.bat
├── install_to_path.ps1
├── SHA256SUMS.txt
├── release_notes.md
└── UPLOAD_INSTRUCTIONS.md
```

## 🎯 Benefits Achieved

### For Non-Technical Users
- ✅ **One-click installation** with automatic scripts
- ✅ **Works from anywhere** after installation
- ✅ **No technical knowledge required**
- ✅ **Clear error messages** and troubleshooting

### For Technical Users
- ✅ **Multiple installation methods** (auto, GUI, CLI)
- ✅ **Standard Windows practices** (C:\Tools, system PATH)
- ✅ **Proper error handling** and verification
- ✅ **Easy uninstallation** (remove from PATH, delete file)

### For Developers
- ✅ **Automated build integration**
- ✅ **Comprehensive documentation**
- ✅ **Cross-platform build scripts**
- ✅ **Release automation**

## 🔍 Verification Commands

Users can verify their installation:

```powershell
# Check if pdf-splitter is in PATH
where.exe pdf-splitter

# Check current PATH
echo $env:PATH

# Test the command
pdf-splitter --help

# Verify file location
Test-Path C:\Tools\pdf-splitter.exe
```

## 🚀 Next Steps

1. **Test Installation Scripts**: Verify on clean Windows systems
2. **Create GitHub Release**: Upload all files including installation scripts
3. **Update Main README**: Add PATH installation as primary method
4. **User Feedback**: Monitor for installation issues and improve scripts

## 📞 Support

Common issues and solutions are documented in:
- `release/windows/README.md` - Comprehensive troubleshooting
- `release_prep/release_notes.md` - Quick start guide
- GitHub Issues - Community support

The PATH installation feature makes PDF Splitter CLI as easy to use as any professional Windows application! 🎉

## Example Usage

```
# Basic usage - split into 5-page chunks
pdf-splitter.exe my-document.pdf

# Custom page count
pdf-splitter.exe large-report.pdf -p 20

# Custom output folder
pdf-splitter.exe presentation.pdf -o split-slides

# Disable progress bars (for automation)
pdf-splitter.exe document.pdf --no-progress
```

## Troubleshooting

- **Windows Defender Warning**: The executable might trigger a warning because it's not digitally signed. Click "More info" â†’ "Run anyway"
- **Antivirus Software**: Some antivirus programs may flag PyInstaller executables. Add an exception if needed
- **Large Files**: For very large PDFs (>1GB), the process may take several minutes

## Support

For issues and updates, visit: https://github.com/jmxt3/pdf-splitter
