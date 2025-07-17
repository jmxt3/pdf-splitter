# PDF Splitter CLI - Windows Release

## Quick Start

1. Download the pdf-splitter.exe file
2. Open Command Prompt or PowerShell
3. Navigate to the folder containing the executable
4. Run the executable:

```
# Show help
pdf-splitter.exe --help

# Split a PDF into 5-page chunks (default)
pdf-splitter.exe document.pdf

# Split into 10-page chunks
pdf-splitter.exe document.pdf -p 10

# Split into custom output folder
pdf-splitter.exe document.pdf -o my_output
```

## Features

- ✅ No Python installation required
- ✅ Standalone executable (includes everything needed)
- ✅ Progress bars with estimated time remaining
- ✅ Automatic output file naming
- ✅ Handles large PDF files efficiently
- ✅ Works on Windows 10/11

## File Size

Executable size: 10.6 MB

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

- **Windows Defender Warning**: The executable might trigger a warning because it's not digitally signed. Click "More info" → "Run anyway"
- **Antivirus Software**: Some antivirus programs may flag PyInstaller executables. Add an exception if needed
- **Large Files**: For very large PDFs (>1GB), the process may take several minutes

## Support

For issues and updates, visit: https://github.com/jmxt3/pdf-splitter
