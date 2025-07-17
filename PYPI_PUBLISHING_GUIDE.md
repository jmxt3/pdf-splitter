# PyPI Publishing Guide for PDF Splitter CLI

This guide walks you through publishing the PDF Splitter CLI package to PyPI.

## 📋 Pre-Publishing Checklist

### ✅ Files Prepared
- [x] `pyproject.toml` - Updated with PyPI metadata
- [x] `README.md` - PyPI-optimized with badges and examples
- [x] `LICENSE` - MIT license file
- [x] `MANIFEST.in` - Controls which files are included
- [x] `main.py` - Main application code

### ✅ Package Configuration
- [x] Package name: `pdf-splitter-cli` (unique on PyPI)
- [x] Version: `0.1.1` (current)
- [x] Python compatibility: `>=3.8`
- [x] Dependencies: `click>=8.0.0`, `pypdf>=3.0.0`
- [x] Entry point: `pdf-splitter = main:main`
- [x] Build tools: `build>=1.2.2.post1`, `twine>=6.1.0`
- [x] Package manager: `uv` (recommended) or `pip`

## 🚀 Publishing Steps

### Option A: Automated Publishing (Recommended)

We provide automated scripts that handle the entire publishing workflow:

#### **Windows (PowerShell) - Recommended**
```powershell
# Run the automated PowerShell script
powershell -ExecutionPolicy Bypass -File publish.ps1
```

#### **Cross-Platform (Bash)**
```bash
# Run the automated bash script
bash publish.sh
```

**The automated scripts will:**
- ✅ Check and sync dependencies with `uv`
- ✅ Prompt for version updates
- ✅ Clean old builds automatically
- ✅ Build packages with proper validation
- ✅ Check package integrity with `twine check`
- ✅ Offer publishing options (TestPyPI, Production, or both)
- ✅ Provide clear success/error feedback

### Option B: Manual Publishing

#### 1. Install Build Tools

```bash
# With uv (recommended)
uv sync

# Or with pip
pip install build twine
```

#### 2. Clean Previous Builds

```bash
# Remove old build artifacts
rm -rf dist/ build/ *.egg-info/
```

#### 3. Build the Package

```bash
# With uv (recommended)
uv run python -m build

# Or with regular python
python -m build
```

This creates:
- `dist/pdf_splitter_cli-0.1.1.tar.gz` (source distribution)
- `dist/pdf_splitter_cli-0.1.1-py3-none-any.whl` (wheel distribution)

#### 4. Test the Build Locally

```bash
# Check package integrity
uv run twine check dist/*

# Install from local build
pip install dist/pdf_splitter_cli-0.1.1-py3-none-any.whl

# Test the command
pdf-splitter --help
```

#### 5. Upload to Test PyPI (Recommended First)

```bash
# Upload to Test PyPI first
uv run twine upload --repository testpypi dist/*
```

**Test PyPI URL:** https://test.pypi.org/project/pdf-splitter-cli/

#### 6. Test Installation from Test PyPI

```bash
# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ pdf-splitter-cli

# Test functionality
pdf-splitter --help
```

#### 7. Upload to Production PyPI

```bash
# Upload to production PyPI
uv run twine upload dist/*
```

**Production PyPI URL:** https://pypi.org/project/pdf-splitter-cli/

## 🔐 Authentication

### Option 1: API Tokens (Recommended)

1. Create PyPI account at https://pypi.org/account/register/
2. Go to Account Settings → API tokens
3. Create token with scope "Entire account" or specific project
4. Configure token:

```bash
# Copy the template and edit with your tokens
cp .pypirc.template ~/.pypirc
# Edit ~/.pypirc and replace YOUR_*_TOKEN_HERE with actual tokens
```

**Important**: Never commit `.pypirc` to Git! It contains sensitive API tokens.

### Option 2: Username/Password

```bash
# Twine will prompt for credentials
twine upload dist/*
```

## 🤖 Automated Publishing Scripts

### Script Features

Both `publish.sh` (bash) and `publish.ps1` (PowerShell) provide:

- **Smart Environment Detection**: Automatically detects and uses `uv` or falls back to `pip`
- **Cross-Platform Compatibility**: Works on Windows, macOS, and Linux
- **Interactive Version Management**: Prompts for version updates with automatic `pyproject.toml` editing
- **Build Validation**: Runs `twine check` to ensure package integrity
- **Flexible Publishing Options**:
  1. Test PyPI only
  2. Production PyPI only
  3. Test PyPI first, then Production (recommended)
  4. Skip publishing (build and validate only)
- **Clear Progress Feedback**: Emoji-enhanced output with color coding
- **Error Handling**: Stops on errors with helpful messages

### Script Testing Results ✅

The scripts have been tested and verified to work correctly:

```
✅ Virtual environment management
✅ Dependency synchronization with uv
✅ Package building (creates .tar.gz and .whl files)
✅ Package validation with twine check
✅ Cross-platform path handling
✅ Interactive prompts and user input
✅ Error handling and recovery
```

### Quick Commands (Alternative to Scripts)

For experienced users who prefer direct commands:

```powershell
# Windows PowerShell - Complete workflow
uv sync
Remove-Item -Path "dist", "build", "*.egg-info" -Recurse -Force -ErrorAction SilentlyContinue
uv run python -m build
uv run twine check dist/*
uv run twine upload --repository testpypi dist/*  # Test first
uv run twine upload dist/*                        # Production
```

```bash
# Unix/Linux/macOS - Complete workflow
uv sync
rm -rf dist/ build/ *.egg-info/
uv run python -m build
uv run twine check dist/*
uv run twine upload --repository testpypi dist/*  # Test first
uv run twine upload dist/*                        # Production
```

## 📦 Package Structure

```
pdf-splitter/
├── main.py                 # Main application
├── pyproject.toml          # Package configuration
├── README.md               # PyPI description
├── LICENSE                 # MIT license
├── MANIFEST.in             # File inclusion rules
├── publish.sh              # Automated bash publishing script
├── publish.ps1             # Automated PowerShell publishing script
├── uv.lock                 # UV dependency lock file
└── dist/                   # Built packages (created by build)
    ├── pdf_splitter_cli-0.1.1.tar.gz
    └── pdf_splitter_cli-0.1.1-py3-none-any.whl
```

## 🔄 Version Updates

For future releases:

1. **Update version** in `pyproject.toml`
2. **Update changelog** in README.md
3. **Clean and rebuild**:
   ```bash
   rm -rf dist/ build/ *.egg-info/
   python -m build
   ```
4. **Upload new version**:
   ```bash
   twine upload dist/*
   ```

## 🧪 Testing Commands

```bash
# Check package metadata
twine check dist/*

# Verify package contents
tar -tzf dist/pdf_splitter_cli-0.1.0.tar.gz

# Test wheel installation
pip install dist/pdf_splitter_cli-0.1.0-py3-none-any.whl --force-reinstall
```

## 🚨 Common Issues

### Package Name Already Exists
- **Error**: `The name 'pdf-splitter' is already taken`
- **Solution**: Use `pdf-splitter-cli` (already configured)

### Missing Files in Distribution
- **Error**: ImportError when installing
- **Solution**: Check `MANIFEST.in` includes all necessary files

### Version Already Exists
- **Error**: `File already exists`
- **Solution**: Increment version in `pyproject.toml`

### Authentication Failed
- **Error**: `Invalid credentials`
- **Solution**: Check API token or username/password

### Script-Specific Issues

#### PowerShell Execution Policy
- **Error**: `execution of scripts is disabled on this system`
- **Solution**: Run with `-ExecutionPolicy Bypass` flag:
  ```powershell
  powershell -ExecutionPolicy Bypass -File publish.ps1
  ```

#### UV Not Found in Bash
- **Error**: `uv not found` in Git Bash/WSL
- **Solution**: The script automatically falls back to pip, or install uv in the bash environment

#### Virtual Environment Issues
- **Error**: `externally-managed-environment`
- **Solution**: The scripts handle this automatically by using `uv run` or creating proper virtual environments

#### Permission Denied (Unix/Linux)
- **Error**: `Permission denied: ./publish.sh`
- **Solution**: Make script executable:
  ```bash
  chmod +x publish.sh
  ```

## 📈 Post-Publishing

After successful publication:

1. **Verify installation**: `pip install pdf-splitter-cli`
2. **Test functionality**: `pdf-splitter --help`
3. **Update documentation** with PyPI installation instructions
4. **Add PyPI badges** to README (already included)
5. **Announce release** on relevant platforms

## 🎯 Success Indicators

### Automated Script Success
- ✅ Script completes without errors
- ✅ Build artifacts created in `dist/` folder
- ✅ `twine check` passes validation
- ✅ Upload confirmation messages appear
- ✅ Package URLs are displayed

### PyPI Publication Success
- ✅ Package appears on https://pypi.org/project/pdf-splitter-cli/
- ✅ `pip install pdf-splitter-cli` works
- ✅ `pdf-splitter --help` shows correct information
- ✅ All features work as expected

## 🎉 Recommended Workflow

For the smoothest publishing experience:

1. **Use the automated PowerShell script** (Windows) or bash script (Unix/Linux)
2. **Start with Test PyPI** to verify everything works
3. **Test the installation** from Test PyPI
4. **Publish to Production PyPI** once confirmed
5. **Verify the final installation** from Production PyPI

```powershell
# Complete automated workflow (Windows)
powershell -ExecutionPolicy Bypass -File publish.ps1
# Choose option 3: "Test PyPI first, then Production"
```

```bash
# Complete automated workflow (Unix/Linux/macOS)
bash publish.sh
# Choose option 3: "Test PyPI first, then Production"
```

The package is now ready for PyPI publication with automated tooling! 🚀
