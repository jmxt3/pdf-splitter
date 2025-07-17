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
- [x] Version: `0.1.0`
- [x] Python compatibility: `>=3.8`
- [x] Dependencies: `click>=8.0.0`, `pypdf>=3.0.0`
- [x] Entry point: `pdf-splitter = main:main`

## 🚀 Publishing Steps

### 1. Install Build Tools

```bash
pip install build twine
```

### 2. Clean Previous Builds

```bash
# Remove old build artifacts
rm -rf dist/ build/ *.egg-info/
```

### 3. Build the Package

```bash
python -m build
```

This creates:
- `dist/pdf_splitter_cli-0.1.0.tar.gz` (source distribution)
- `dist/pdf_splitter_cli-0.1.0-py3-none-any.whl` (wheel distribution)

### 4. Test the Build Locally

```bash
# Install from local build
pip install dist/pdf_splitter_cli-0.1.0-py3-none-any.whl

# Test the command
pdf-splitter --help
```

### 5. Upload to Test PyPI (Recommended First)

```bash
# Upload to Test PyPI first
twine upload --repository testpypi dist/*
```

**Test PyPI URL:** https://test.pypi.org/project/pdf-splitter-cli/

### 6. Test Installation from Test PyPI

```bash
# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ pdf-splitter-cli

# Test functionality
pdf-splitter --help
```

### 7. Upload to Production PyPI

```bash
# Upload to production PyPI
twine upload dist/*
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

## 📦 Package Structure

```
pdf-splitter/
├── main.py                 # Main application
├── pyproject.toml          # Package configuration
├── README.md               # PyPI description
├── LICENSE                 # MIT license
├── MANIFEST.in             # File inclusion rules
└── dist/                   # Built packages (created by build)
    ├── pdf_splitter_cli-0.1.0.tar.gz
    └── pdf_splitter_cli-0.1.0-py3-none-any.whl
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

## 📈 Post-Publishing

After successful publication:

1. **Verify installation**: `pip install pdf-splitter-cli`
2. **Test functionality**: `pdf-splitter --help`
3. **Update documentation** with PyPI installation instructions
4. **Add PyPI badges** to README (already included)
5. **Announce release** on relevant platforms

## 🎯 Success Indicators

- ✅ Package appears on https://pypi.org/project/pdf-splitter-cli/
- ✅ `pip install pdf-splitter-cli` works
- ✅ `pdf-splitter --help` shows correct information
- ✅ All features work as expected

The package is now ready for PyPI publication! 🚀
