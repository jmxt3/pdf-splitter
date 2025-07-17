# PATH Installation Guide for PDF Splitter CLI

This guide explains how to add the PDF Splitter executable to the Windows PATH so users can run `pdf-splitter` from anywhere without navigating to the executable folder.

## 🎯 Goal

Transform this:
```bash
# User has to navigate to the folder
cd C:\Downloads
pdf-splitter.exe document.pdf
```

Into this:
```bash
# User can run from anywhere
cd C:\Users\John\Documents
pdf-splitter document.pdf  # Works from any folder!
```

## 📦 What We've Created

### 1. **Automatic Installation Scripts**
- `install_to_path.bat` - Batch script for Command Prompt users
- `install_to_path.ps1` - PowerShell script for PowerShell users

### 2. **Manual Installation Instructions**
- Step-by-step GUI instructions
- PowerShell commands
- Command Prompt commands

### 3. **Updated Documentation**
- Windows README with comprehensive PATH instructions
- Release notes with PATH installation examples
- Troubleshooting section for common PATH issues

## 🚀 How It Works

### Automatic Installation Process
1. **Download**: User gets both `pdf-splitter.exe` and installation script
2. **Run Script**: Right-click → "Run as administrator"
3. **Automatic Setup**:
   - Creates `C:\Tools` directory
   - Copies `pdf-splitter.exe` to `C:\Tools\pdf-splitter.exe`
   - Adds `C:\Tools` to system PATH
   - Verifies installation
4. **Ready to Use**: Open new terminal, type `pdf-splitter --help`

### What the Scripts Do
```powershell
# PowerShell version (install_to_path.ps1)
1. Check administrator privileges
2. Verify pdf-splitter.exe exists
3. Create C:\Tools directory
4. Copy executable to C:\Tools\pdf-splitter.exe
5. Add C:\Tools to system PATH
6. Verify installation success
7. Show usage instructions
```

```batch
# Batch version (install_to_path.bat)
1. Check administrator privileges
2. Verify pdf-splitter.exe exists  
3. Create C:\Tools directory
4. Copy executable to C:\Tools\pdf-splitter.exe
5. Update system PATH registry
6. Verify installation success
7. Show usage instructions
```

## 📋 User Experience

### Before PATH Installation
```bash
# User workflow - cumbersome
1. Download pdf-splitter.exe to Downloads
2. Open Command Prompt
3. cd C:\Users\John\Downloads
4. pdf-splitter.exe document.pdf
5. Navigate to different folder? Start over!
```

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
