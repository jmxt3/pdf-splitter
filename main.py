from pypdf import PdfReader, PdfWriter
import os
import sys
import click
import subprocess
import shutil
import tempfile
import glob

def check_external_tool(tool_name):
    """Check if an external tool is available in the system PATH."""
    return shutil.which(tool_name) is not None

def split_with_pdftk(input_pdf_path, pages_per_chunk, output_folder, input_basename, show_progress=True):
    """Split PDF using pdftk as fallback method."""
    click.echo("🔧 Attempting to split using pdftk...")

    if not check_external_tool('pdftk'):
        raise Exception("pdftk is not installed. Install with: brew install pdftk-java (macOS) or sudo apt install pdftk (Linux)")

    # Create temporary directory for individual pages
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Use pdftk to burst into individual pages
            click.echo("📄 Splitting into individual pages with pdftk...")
            result = subprocess.run([
                'pdftk', input_pdf_path, 'burst', 'output',
                os.path.join(temp_dir, 'page_%04d.pdf')
            ], capture_output=True, text=True, check=True)

            # Get list of created page files
            page_files = sorted(glob.glob(os.path.join(temp_dir, 'page_*.pdf')))
            total_pages = len(page_files)
            click.echo(f"✅ Successfully split into {total_pages} individual pages")

            # Group pages into chunks
            chunk_number = 1
            total_chunks = (total_pages + pages_per_chunk - 1) // pages_per_chunk

            # Create progress bar for chunk creation (if enabled)
            if show_progress:
                with click.progressbar(length=total_chunks,
                                     label='Creating PDF files with pdftk',
                                     show_eta=True,
                                     show_percent=True) as progress_bar:

                    for i in range(0, total_pages, pages_per_chunk):
                        chunk_files = page_files[i:i + pages_per_chunk]
                        output_filename = os.path.join(output_folder, f"{input_basename}_{chunk_number}.pdf")

                        # Use pdftk to combine pages into chunk
                        cmd = ['pdftk'] + chunk_files + ['cat', 'output', output_filename]
                        subprocess.run(cmd, capture_output=True, text=True, check=True)

                        chunk_number += 1
                        progress_bar.update(1)  # Update progress after each file is created
            else:
                for i in range(0, total_pages, pages_per_chunk):
                    chunk_files = page_files[i:i + pages_per_chunk]
                    output_filename = os.path.join(output_folder, f"{input_basename}_{chunk_number}.pdf")

                    click.echo(f"📄 Creating chunk {chunk_number}/{total_chunks} ({len(chunk_files)} pages)...")

                    # Use pdftk to combine pages into chunk
                    cmd = ['pdftk'] + chunk_files + ['cat', 'output', output_filename]
                    subprocess.run(cmd, capture_output=True, text=True, check=True)

                    click.echo(f"✅ Created: {output_filename}")
                    chunk_number += 1

            click.echo(f"✅ Successfully created {total_chunks} chunks using pdftk")

        except subprocess.CalledProcessError as e:
            raise Exception(f"pdftk failed: {e.stderr}")

def split_with_qpdf(input_pdf_path, pages_per_chunk, output_folder, input_basename, show_progress=True):
    """Split PDF using qpdf as fallback method."""
    click.echo("🔧 Attempting to split using qpdf...")

    if not check_external_tool('qpdf'):
        raise Exception("qpdf is not installed. Install with: brew install qpdf (macOS) or sudo apt install qpdf (Linux)")

    # Create temporary directory for individual pages
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Use qpdf to split into individual pages
            click.echo("📄 Splitting into individual pages with qpdf...")
            result = subprocess.run([
                'qpdf', '--split-pages', input_pdf_path,
                os.path.join(temp_dir, 'page-%d.pdf')
            ], capture_output=True, text=True)

            # qpdf may succeed with warnings for corrupted files
            if result.returncode != 0:
                raise subprocess.CalledProcessError(result.returncode, 'qpdf', result.stderr)

            # Show warnings if any
            if result.stderr:
                click.echo(f"⚠️  qpdf warnings: {result.stderr.strip()}", err=True)

            # Get list of created page files
            page_files = sorted(glob.glob(os.path.join(temp_dir, 'page-*.pdf')))
            total_pages = len(page_files)
            click.echo(f"✅ Successfully split into {total_pages} individual pages")

            # Group pages into chunks using pypdf (since individual pages should work)
            chunk_number = 1
            total_chunks = (total_pages + pages_per_chunk - 1) // pages_per_chunk

            # Create progress bar for chunk creation (if enabled)
            if show_progress:
                with click.progressbar(length=total_chunks,
                                     label='Creating PDF files with qpdf+pypdf',
                                     show_eta=True,
                                     show_percent=True) as progress_bar:

                    for i in range(0, total_pages, pages_per_chunk):
                        chunk_files = page_files[i:i + pages_per_chunk]
                        output_filename = os.path.join(output_folder, f"{input_basename}_{chunk_number}.pdf")

                        # Combine individual pages using pypdf
                        writer = PdfWriter()
                        for page_file in chunk_files:
                            reader = PdfReader(page_file)
                            writer.add_page(reader.pages[0])

                        with open(output_filename, "wb") as output_pdf:
                            writer.write(output_pdf)

                        chunk_number += 1
                        progress_bar.update(1)  # Update progress after each file is created
            else:
                for i in range(0, total_pages, pages_per_chunk):
                    chunk_files = page_files[i:i + pages_per_chunk]
                    output_filename = os.path.join(output_folder, f"{input_basename}_{chunk_number}.pdf")

                    click.echo(f"📄 Creating chunk {chunk_number}/{total_chunks} ({len(chunk_files)} pages)...")

                    # Combine individual pages using pypdf
                    writer = PdfWriter()
                    for page_file in chunk_files:
                        reader = PdfReader(page_file)
                        writer.add_page(reader.pages[0])

                    with open(output_filename, "wb") as output_pdf:
                        writer.write(output_pdf)

                    click.echo(f"✅ Created: {output_filename}")
                    chunk_number += 1

            click.echo(f"✅ Successfully created {total_chunks} chunks using qpdf+pypdf")

        except subprocess.CalledProcessError as e:
            raise Exception(f"qpdf failed: {e.stderr}")

def split_pdf_by_chunks(input_pdf_path, pages_per_chunk=5, output_folder="output_chunks", show_progress=True):
    """
    Splits a PDF file into multiple PDF files, each containing a specified number of pages.
    Optimized for large PDF files by using memory-efficient processing.

    For example:
    - Input: "your_document.pdf" -> Output: "your_document_1.pdf", "your_document_2.pdf", etc.
    - Input: "report.pdf" -> Output: "report_1.pdf", "report_2.pdf", etc.
    """
    import gc  # For garbage collection to manage memory

    try:
        # Check file size and warn if very large
        file_size = os.path.getsize(input_pdf_path)
        file_size_mb = file_size / (1024 * 1024)

        if file_size_mb > 100:  # Warn for files larger than 100MB
            click.echo(f"⚠️  Large file detected: {file_size_mb:.1f}MB. Processing may take some time...")

        # Try multiple approaches to read problematic PDFs
        click.echo("📖 Reading PDF file...")
        reader = None

        # Approach 1: Try with strict=False (most permissive)
        try:
            reader = PdfReader(input_pdf_path, strict=False)
            total_pages = len(reader.pages)
            click.echo(f"✅ Successfully read PDF with {total_pages} pages (permissive mode)")
        except Exception as e1:
            click.echo(f"⚠️  Permissive mode failed: {str(e1)}")

            # Approach 2: Try opening as binary and creating reader from stream
            try:
                click.echo("� Trying alternative reading method...")
                with open(input_pdf_path, 'rb') as file:
                    reader = PdfReader(file, strict=False)
                    total_pages = len(reader.pages)
                    click.echo(f"✅ Successfully read PDF with {total_pages} pages (stream mode)")
            except Exception as e2:
                click.echo(f"⚠️  Stream mode failed: {str(e2)}")

                # Approach 3: Try with password (empty password for encrypted PDFs)
                try:
                    click.echo("🔄 Trying with empty password (for encrypted PDFs)...")
                    reader = PdfReader(input_pdf_path, strict=False, password="")
                    total_pages = len(reader.pages)
                    click.echo(f"✅ Successfully read PDF with {total_pages} pages (password mode)")
                except Exception as e3:
                    click.echo(f"⚠️  Password mode failed: {str(e3)}")

                    # All pypdf approaches failed, try external tools
                    click.echo("❌ All pypdf methods failed. Trying external tools...")

                    # Extract the base filename for external tools
                    input_basename = os.path.splitext(os.path.basename(input_pdf_path))[0]

                    if not os.path.exists(output_folder):
                        os.makedirs(output_folder)

                    # Try pdftk first (most reliable for corrupted PDFs)
                    if check_external_tool('pdftk'):
                        try:
                            split_with_pdftk(input_pdf_path, pages_per_chunk, output_folder, input_basename, show_progress)
                            return  # Success! Exit the function
                        except Exception as pdftk_error:
                            click.echo(f"⚠️  pdftk failed: {str(pdftk_error)}")

                    # Try qpdf as second option
                    if check_external_tool('qpdf'):
                        try:
                            split_with_qpdf(input_pdf_path, pages_per_chunk, output_folder, input_basename, show_progress)
                            return  # Success! Exit the function
                        except Exception as qpdf_error:
                            click.echo(f"⚠️  qpdf failed: {str(qpdf_error)}")

                    # All methods failed
                    error_msg = f"""Failed to read PDF file '{input_pdf_path}' using all available methods:

PyPDF attempts:
1. Permissive mode: {str(e1)}
2. Stream mode: {str(e2)}
3. Password mode: {str(e3)}

External tools:
- pdftk: {'Available' if check_external_tool('pdftk') else 'Not installed'}
- qpdf: {'Available' if check_external_tool('qpdf') else 'Not installed'}

This PDF file appears to be severely corrupted or uses an unsupported format.

Install external tools for better corruption handling:
- macOS: brew install pdftk-java qpdf
- Ubuntu/Debian: sudo apt install pdftk qpdf
- CentOS/RHEL: sudo yum install pdftk qpdf

Manual alternatives:
- Online tools: SmallPDF, ILovePDF split tools
- PDF repair tools before splitting
- Convert to images and back to PDF"""
                    raise Exception(error_msg)

    except Exception as e:
        if "Failed to read PDF file" in str(e):
            raise e  # Re-raise our detailed error message
        else:
            raise Exception(f"Failed to read PDF file '{input_pdf_path}': {str(e)}")

    # Extract the base filename without extension from the input path
    input_basename = os.path.splitext(os.path.basename(input_pdf_path))[0]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    chunk_number = 1
    total_chunks = (total_pages + pages_per_chunk - 1) // pages_per_chunk

    # Process chunks with or without progress bar
    if show_progress:
        # Create progress bar that tracks each output file being created
        with click.progressbar(length=total_chunks,
                             label='Creating PDF files',
                             show_eta=True,
                             show_percent=True) as progress_bar:

            for i in range(0, total_pages, pages_per_chunk):
                try:
                    # Create a new writer for each chunk to minimize memory usage
                    writer = PdfWriter()

                    # Add pages to the writer with individual error handling
                    start_page = i
                    end_page = min(i + pages_per_chunk, total_pages)
                    pages_added = 0

                    # Process pages in this chunk
                    for j in range(start_page, end_page):
                        try:
                            # Access page directly without storing reference to minimize memory usage
                            page = reader.pages[j]
                            writer.add_page(page)
                            pages_added += 1
                        except Exception as e:
                            click.echo(f"⚠️  Warning: Failed to process page {j + 1}: {str(e)}", err=True)
                            continue

                    if pages_added == 0:
                        click.echo(f"❌ Skipping chunk {chunk_number}: No pages could be processed", err=True)
                        chunk_number += 1
                        progress_bar.update(1)  # Update progress even for skipped chunks
                        continue

                    # Generate output filename using original basename and sequential number
                    output_filename = os.path.join(output_folder, f"{input_basename}_{chunk_number}.pdf")

                    # Write the PDF with error handling
                    try:
                        with open(output_filename, "wb") as output_pdf:
                            writer.write(output_pdf)
                    except Exception as e:
                        raise Exception(f"Failed to write chunk {chunk_number} to '{output_filename}': {str(e)}")

                    # Update progress bar after each file is successfully created
                    progress_bar.update(1)

                except Exception as e:
                    click.echo(f"❌ Error processing chunk {chunk_number}: {str(e)}", err=True)
                    # Update progress bar even for failed chunks to keep it moving
                    progress_bar.update(1)

                finally:
                    # Force garbage collection after each chunk to free memory
                    gc.collect()

                chunk_number += 1
    else:
        # Process without progress bar - show traditional text messages
        for i in range(0, total_pages, pages_per_chunk):
            try:
                click.echo(f"📄 Processing chunk {chunk_number}/{total_chunks} (pages {i+1}-{min(i + pages_per_chunk, total_pages)})...")

                # Create a new writer for each chunk to minimize memory usage
                writer = PdfWriter()

                # Add pages to the writer with individual error handling
                start_page = i
                end_page = min(i + pages_per_chunk, total_pages)
                pages_added = 0

                # Process pages in this chunk
                for j in range(start_page, end_page):
                    try:
                        # Access page directly without storing reference to minimize memory usage
                        page = reader.pages[j]
                        writer.add_page(page)
                        pages_added += 1
                    except Exception as e:
                        click.echo(f"⚠️  Warning: Failed to process page {j + 1}: {str(e)}", err=True)
                        continue

                if pages_added == 0:
                    click.echo(f"❌ Skipping chunk {chunk_number}: No pages could be processed", err=True)
                    chunk_number += 1
                    continue

                # Generate output filename using original basename and sequential number
                output_filename = os.path.join(output_folder, f"{input_basename}_{chunk_number}.pdf")

                # Write the PDF with error handling
                try:
                    with open(output_filename, "wb") as output_pdf:
                        writer.write(output_pdf)
                    click.echo(f"✅ Created: {output_filename} ({pages_added} pages)")
                except Exception as e:
                    raise Exception(f"Failed to write chunk {chunk_number} to '{output_filename}': {str(e)}")

            except Exception as e:
                click.echo(f"❌ Error processing chunk {chunk_number}: {str(e)}", err=True)
                # Continue with next chunk instead of failing completely

            finally:
                # Force garbage collection after each chunk to free memory
                gc.collect()

            chunk_number += 1

    click.echo(f"✅ Successfully created {chunk_number - 1} chunks")

@click.command(name="pdf-splitter")
@click.argument('input_pdf', type=click.Path(exists=True, dir_okay=False, path_type=str))
@click.option('-p', '--pages-per-chunk', default=5, type=int,
              help='Number of pages per output file (default: 5)')
@click.option('-o', '--output-folder', default='output_chunks', type=str,
              help='Output folder for split PDF files (default: "output_chunks")')
@click.option('--no-progress', is_flag=True, default=False,
              help='Disable progress bars (useful for scripting)')
@click.help_option('-h', '--help')
def main(input_pdf, pages_per_chunk, output_folder, no_progress):
    """
    Split a PDF file into multiple smaller PDF files with sequential numbering.

    OUTPUT FILES: Files will be named using the pattern {original_basename}_{number}.pdf

    Examples:
    \b
      pdf-splitter document.pdf                    # Split every 5 pages (default)
      pdf-splitter document.pdf -p 10              # Split every 10 pages
      pdf-splitter document.pdf -p 3 -o my_output # Split every 3 pages, output to 'my_output' folder
      pdf-splitter /path/to/report.pdf -p 1       # Split into individual pages
      pdf-splitter document.pdf --no-progress     # Disable progress bars (useful for scripting)

    \b
    Output file naming:
      - Input: "document.pdf" -> Output: "document_1.pdf", "document_2.pdf", etc.
      - Input: "report.pdf" -> Output: "report_1.pdf", "report_2.pdf", etc.

    \b
    Progress bars:
      - Shows progress across total number of output PDF files being created
      - Updates as each chunk file is completed (1/10, 2/10, etc.)
      - Displays percentage complete and estimated time remaining
      - Use --no-progress to disable for automated scripts
    """

    # Validate input file is a PDF
    if not input_pdf.lower().endswith('.pdf'):
        click.echo(f"Error: Input file '{input_pdf}' is not a PDF file.", err=True)
        sys.exit(1)

    # Validate pages per chunk is positive
    if pages_per_chunk <= 0:
        click.echo(f"Error: Pages per chunk must be a positive integer, got {pages_per_chunk}.", err=True)
        sys.exit(1)

    try:
        click.echo(f"Splitting '{input_pdf}' into chunks of {pages_per_chunk} pages...")
        click.echo(f"Output folder: '{output_folder}'")

        split_pdf_by_chunks(input_pdf, pages_per_chunk, output_folder, show_progress=not no_progress)

        click.echo(click.style("PDF splitting completed successfully!", fg='green', bold=True))

    except Exception as e:
        click.echo(f"Error: Failed to split PDF: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()