# PDF Splitter CLI v0.1.1

## 🚀 What's New
- [Add your changes here]

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
Get-FileHash pdf-splitter-v0.1.1-windows-x64.exe -Algorithm SHA256

# macOS/Linux
sha256sum pdf-splitter-v0.1.1-*
```

Compare with checksums in `SHA256SUMS.txt`.

## 🐛 Issues
Report bugs at: https://github.com/jmxt3/pdf-splitter/issues

## 📄 Full Documentation
See: https://github.com/jmxt3/pdf-splitter#readme
