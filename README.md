# PDF Splitter

A modern command-line tool to split PDF files into smaller chunks with automatic filename generation based on the original file.

## Features

- Split PDF files by a specified number of pages per chunk
- Automatic output filename generation using the original filename as base
- Sequential numbering for output files (e.g., `document_1.pdf`, `document_2.pdf`)
- Configurable output folder
- Modern Click-based CLI with rich help and validation
- Support for splitting into individual pages
- Colorized output for better user experience

## Installation

### 🚀 Quick Installation for Non-Technical Users

Choose your operating system and follow the simple steps:

#### **Windows** 🪟

1. **Install Python** (if not already installed):
   - Go to [python.org/downloads](https://python.org/downloads)
   - Download and install Python (make sure to check "Add Python to PATH" during installation)

2. **Download this tool**:
   - Click the green "Code" button on this page → "Download ZIP"
   - Extract the ZIP file to a folder (e.g., `C:\machete-splitter`)

3. **Install the tool**:
   - Press `Windows + R`, type `cmd`, and press Enter
   - Type: `cd C:\pdf-splitter` (or wherever you extracted the files)
   - Type: `pip install -e .`
   - Wait for installation to complete

4. **You're done!** Now you can use `pdf-splitter` from anywhere in Command Prompt

#### **macOS** 🍎

1. **Install Python** (if not already installed):
   - Open Terminal (press `Cmd + Space`, type "Terminal")
   - Install Homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
   - Install Python: `brew install python`

2. **Download this tool**:
   - Click the green "Code" button on this page → "Download ZIP"
   - Extract the ZIP file to a folder (e.g., `~/Downloads/pdf-splitter`)

3. **Install the tool**:
   - Open Terminal
   - Type: `cd ~/Downloads/pdf-splitter` (or wherever you extracted the files)
   - Type: `pip install -e .`
   - Wait for installation to complete

4. **You're done!** Now you can use `pdf-splitter` from anywhere in Terminal

#### **Linux** 🐧

1. **Install Python** (usually already installed):
   - Open Terminal (`Ctrl + Alt + T`)
   - Update packages: `sudo apt update` (Ubuntu/Debian) or `sudo yum update` (CentOS/RHEL)
   - Install Python: `sudo apt install python3 python3-pip` (Ubuntu/Debian) or `sudo yum install python3 python3-pip` (CentOS/RHEL)

2. **Download this tool**:
   - Click the green "Code" button on this page → "Download ZIP"
   - Extract the ZIP file to a folder (e.g., `~/Downloads/pdf-splitter`)

3. **Install the tool**:
   - Open Terminal
   - Type: `cd ~/Downloads/pdf-splitter` (or wherever you extracted the files)
   - Type: `pip install -e .` or `pip3 install -e .`
   - Wait for installation to complete

4. **You're done!** Now you can use `pdf-splitter` from anywhere in Terminal

### ✅ Test Your Installation

After installation, test that everything works:
```bash
pdf-splitter --help
```

You should see the help message with usage instructions.

### 🔧 Troubleshooting

**Problem: "machete-splitter: command not found"**
- **Solution**: Make sure Python's Scripts directory is in your PATH
- **Windows**: Reinstall Python and check "Add Python to PATH"
- **macOS/Linux**: Try `python -m pip install --user -e .` instead

**Problem: "pip: command not found"**
- **Windows**: Reinstall Python with "Add Python to PATH" checked
- **macOS**: Install Python via Homebrew: `brew install python`
- **Linux**: Install pip: `sudo apt install python3-pip` (Ubuntu) or `sudo yum install python3-pip` (CentOS)

**Problem: Permission denied errors**
- **Solution**: Add `--user` flag: `pip install --user -e .`
- **Alternative**: Use `sudo` on macOS/Linux: `sudo pip install -e .`

**Problem: "No module named 'click'" or "No module named 'pypdf'"**
- **Solution**: Install dependencies manually: `pip install click pypdf`

**Need help?** Open an issue on this repository with your error message and operating system.

### 🎯 Quick Start Guide

Once installed, using the tool is simple:

1. **Put your PDF file** in an easy-to-find location (like Desktop or Downloads)
2. **Open Terminal/Command Prompt** in that folder:
   - **Windows**: Hold Shift + Right-click in the folder → "Open PowerShell window here"
   - **macOS**: Right-click folder → "Services" → "New Terminal at Folder"
   - **Linux**: Right-click folder → "Open in Terminal"
3. **Run the command**:
   ```bash
   pdf-splitter your-file.pdf
   ```
4. **Find your split files** in the `output_chunks` folder that gets created!

**Example**: If you have a file called `my-document.pdf` on your Desktop:
```bash
pdf-splitter my-document.pdf
```
This creates: `my-document_1.pdf`, `my-document_2.pdf`, etc.

---

### 🔧 Advanced Installation (For Developers)

#### Option 1: Install from source (recommended for development)
1. Clone or download this repository
2. Install in development mode:
   ```bash
   uv pip install -e .
   ```
   or with regular pip:
   ```bash
   pip install -e .
   ```

#### Option 2: Install dependencies manually
```bash
uv add click pypdf
# or
pip install click pypdf
```

## Usage

### Basic Command Structure

```bash
pdf-splitter <input_pdf> [options]
```

### Command-Line Options

- `input_pdf` (required): Path to the input PDF file to split
- `-p, --pages-per-chunk`: Number of pages per output file (default: 5)
- `-o, --output-folder`: Output folder for split PDF files (default: "output_chunks")
- `-h, --help`: Show help message with examples

### Examples

#### Basic Usage (split every 5 pages - default)
```bash
pdf-splitter document.pdf
```
**Output**: `document_1.pdf`, `document_2.pdf`, `document_3.pdf`, etc. in `output_chunks/` folder

#### Split every 10 pages
```bash
pdf-splitter document.pdf -p 10
```
or
```bash
pdf-splitter document.pdf --pages-per-chunk 10
```

#### Split every 3 pages with custom output folder
```bash
pdf-splitter document.pdf -p 3 -o my_output
```
or
```bash
pdf-splitter document.pdf --pages-per-chunk 3 --output-folder my_output
```

#### Split into individual pages (1 page per file)
```bash
pdf-splitter report.pdf -p 1
```
**Output**: `report_1.pdf`, `report_2.pdf`, `report_3.pdf`, etc. (one page each)

#### Full path example
```bash
pdf-splitter /path/to/your/large_file.pdf -p 5 -o split_pdfs
```

### Output File Naming

The tool automatically generates output filenames based on the original input filename:

- **Pattern**: `{original_basename}_{number}.pdf`
- **Input**: `"document.pdf"` → **Output**: `"document_1.pdf"`, `"document_2.pdf"`, etc.
- **Input**: `"report.pdf"` → **Output**: `"report_1.pdf"`, `"report_2.pdf"`, etc.
- **Input**: `"/path/to/my_file.pdf"` → **Output**: `"my_file_1.pdf"`, `"my_file_2.pdf"`, etc.

### Help

To see all available options and examples:
```bash
pdf-splitter --help
```

### Alternative Usage (without installation)

If you haven't installed the package, you can still run it directly:
```bash
python main.py --help
```

But we recommend installing it to get the `pdf-splitter` command globally available.

## Handling Large PDF Files

The tool is optimized to handle large PDF files (including multi-GB files) efficiently:

### 🚀 **Large File Optimizations**
- **Memory-efficient processing**: Processes files in chunks to minimize memory usage
- **Garbage collection**: Automatically frees memory after each chunk
- **Error recovery**: Continues processing even if individual pages fail
- **Progress tracking**: Shows detailed progress for large files
- **File size warnings**: Alerts you when processing large files (>100MB)

### 💡 **Tips for Large Files**
- **Use larger chunk sizes** for very large files: `pdf-splitter large-file.pdf -p 100`
- **Ensure sufficient disk space** for output files
- **Be patient**: Large files (GB+) may take several minutes to process
- **Monitor system resources**: Close other applications if needed

### ⚠️ **Troubleshooting Large Files**

#### **"negative seek value" Error**
This error indicates severe PDF corruption. The tool will try multiple reading methods and provide detailed alternatives:

**Immediate Solutions:**
1. **Try pdftk** (most reliable for corrupted PDFs):
   ```bash
   # Install pdftk first
   brew install pdftk-java  # macOS
   sudo apt install pdftk   # Ubuntu/Debian

   # Split the PDF
   pdftk large_file.pdf burst output page_%02d.pdf
   ```

2. **Try qpdf** (another robust alternative):
   ```bash
   # Install qpdf
   brew install qpdf        # macOS
   sudo apt install qpdf    # Ubuntu/Debian

   # Split the PDF
   qpdf --split-pages large_file.pdf output_%d.pdf
   ```

3. **Online tools** (for smaller files):
   - [SmallPDF Split](https://smallpdf.com/split-pdf)
   - [ILovePDF Split](https://www.ilovepdf.com/split_pdf)
   - [PDF24 Split](https://tools.pdf24.org/en/split-pdf)

4. **PDF Repair first, then split**:
   - Try opening in Adobe Reader/Acrobat and re-saving
   - Use online PDF repair tools
   - Convert to images and back to PDF

#### **Other Common Issues**
- **Out of memory errors**: Try smaller chunk sizes or restart your computer
- **Slow processing**: Normal for large files - the tool will show progress
- **Permission errors**: Ensure you have write access to the output folder

## Error Handling

The tool includes comprehensive error handling for:
- Non-existent input files (Click automatically validates file existence)
- Invalid file extensions (non-PDF files)
- Invalid page chunk sizes (must be positive integers)
- PDF reading errors and corruption
- Memory management for large files
- Individual page processing failures
- Colorized error messages for better visibility

## Requirements

- Python 3.13+
- click >= 8.2.1
- pypdf >= 5.8.0

## License

This project is open source and available under the MIT License.