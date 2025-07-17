# PDF Splitter CLI - Windows Release

## Quick Start
1. Download the pdf-splitter file [RIGHT-CLICK AND SAVE](https://github.com/jmxt3/pdf-splitter/raw/refs/heads/main/release/windows/pdf-splitter.exe)
2. Download the `install_to_path.ps1` script [RIGHT-CLICK AND SAVE](https://raw.githubusercontent.com/jmxt3/pdf-splitter/refs/heads/main/release/windows/install_to_path.ps1)
3. Open Microsoft PowerShell with Administrator privileges and navigate to the folder containing the executable
4. Execute the `install_to_path.ps1` script to add the executable to your PATH (the script should be on the same folder of the executable)
5. Close the PowerShell window
6. Open a new PowerShell window
7. Type `pdf-splitter --help` to verify the installation

```
# Show help
pdf-splitter --help

# Split a PDF into 5-page chunks (default)
pdf-splitter document.pdf

# Split into 10-page chunks
pdf-splitter document.pdf -p 10

# Split into custom output folder
pdf-splitter document.pdf -o my_output
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

## Troubleshooting

- **Windows Defender Warning**: The executable might trigger a warning because it's not digitally signed. Click "More info" → "Run anyway"
- **Antivirus Software**: Some antivirus programs may flag PyInstaller executables. Add an exception if needed
- **Large Files**: For very large PDFs (>1GB), the process may take several minutes

## Support

For issues and updates, visit: https://github.com/jmxt3/pdf-splitter
