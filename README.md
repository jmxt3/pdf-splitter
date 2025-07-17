# PDF Splitter CLI

[![PyPI version](https://badge.fury.io/py/pdf-splitter-cli.svg)](https://badge.fury.io/py/pdf-splitter-cli)
[![Python Support](https://img.shields.io/pypi/pyversions/pdf-splitter-cli.svg)](https://pypi.org/project/pdf-splitter-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern command-line tool to split PDF files into smaller chunks with **real-time progress bars** and automatic filename generation.

## ✨ Features

- 📄 **Split PDF files** by specified number of pages per chunk
- 🎯 **Real-time progress bars** showing file creation progress
- 📁 **Smart filename generation** based on original filename
- 🔢 **Sequential numbering** (e.g., `document_1.pdf`, `document_2.pdf`)
- 📂 **Configurable output folders**
- 🖥️ **Modern CLI** with rich help and validation
- 📃 **Individual page splitting** support
- 🎨 **Colorized output** for better user experience
- 🛠️ **Robust error handling** with fallback methods (pdftk, qpdf)
- ⚡ **Memory-efficient** processing for large files
- 🔧 **Cross-platform** (Windows, macOS, Linux)

## 🚀 Installation

```bash
pip install pdf-splitter-cli
```

**Requirements:** Python 3.8+

## 📖 Quick Start

```bash
# Basic usage - split every 5 pages (default)
pdf-splitter document.pdf

# Custom chunk size - split every 10 pages  
pdf-splitter document.pdf -p 10

# Custom output folder
pdf-splitter document.pdf -o my_chunks

# Split into individual pages
pdf-splitter document.pdf -p 1

# Disable progress bars (useful for scripts)
pdf-splitter document.pdf --no-progress
```

## 📋 Usage

### Command Structure
```bash
pdf-splitter <input_pdf> [OPTIONS]
```

### Options
- `-p, --pages-per-chunk INTEGER`: Pages per output file (default: 5)
- `-o, --output-folder TEXT`: Output folder (default: "output_chunks")
- `--no-progress`: Disable progress bars
- `--help`: Show help message

### Examples

#### Basic Splitting
```bash
pdf-splitter document.pdf
```
**Output:** `document_1.pdf`, `document_2.pdf`, etc. in `output_chunks/`

#### Custom Page Count
```bash
pdf-splitter document.pdf -p 10
pdf-splitter document.pdf --pages-per-chunk 10
```

#### Custom Output Folder
```bash
pdf-splitter document.pdf -p 3 -o my_output
```

#### Individual Pages
```bash
pdf-splitter report.pdf -p 1
```
**Output:** `report_1.pdf`, `report_2.pdf`, etc. (one page each)

## 🎯 Progress Bars

The tool shows real-time progress as files are created:

```
Creating PDF files [████████████████████] 100% (8/8 files) 00:00:15
```

- **File-based progress**: Tracks each output file completion
- **ETA display**: Shows estimated time remaining
- **Percentage complete**: Visual progress indicator
- **Disable option**: Use `--no-progress` for scripting

## 🛠️ Advanced Features

### Large File Support
- **Memory-efficient processing** for multi-GB files
- **Automatic garbage collection** after each chunk
- **Error recovery** continues processing if individual pages fail
- **File size warnings** for files >100MB

### Fallback Methods
If the primary PyPDF method fails, the tool automatically tries:
1. **pdftk** (if installed)
2. **qpdf** (if installed)

### Error Handling
- **Graceful degradation** for corrupted PDFs
- **Detailed error messages** with suggested solutions
- **Partial processing** continues even if some pages fail

## 📁 Output File Naming

Files are automatically named using the original filename:

| Input | Output |
|-------|--------|
| `document.pdf` | `document_1.pdf`, `document_2.pdf`, ... |
| `report.pdf` | `report_1.pdf`, `report_2.pdf`, ... |
| `/path/to/file.pdf` | `file_1.pdf`, `file_2.pdf`, ... |

## 🔧 Installation from Source

For development or latest features:

```bash
git clone https://github.com/jmxt3/pdf-splitter.git
cd pdf-splitter
pip install -e .
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 🐛 Issues

Found a bug or have a feature request? Please open an issue on [GitHub](https://github.com/jmxt3/pdf-splitter/issues).

## 📊 Dependencies

- **click**: Modern CLI framework
- **pypdf**: PDF processing library

## 🏷️ Version History

- **0.1.0**: Initial release with progress bars and robust error handling
