#!/usr/bin/env python3
"""
Simple test script to demonstrate the progress bar functionality.
This creates a sample PDF and tests the progress bar features.
"""

import os
import sys
from pypdf import PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tempfile
import subprocess

def create_sample_pdf(filename, num_pages=20):
    """Create a sample PDF with the specified number of pages for testing."""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
    except ImportError:
        print("❌ reportlab not installed. Install with: pip install reportlab")
        return False
    
    print(f"📄 Creating sample PDF with {num_pages} pages...")
    
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    for i in range(1, num_pages + 1):
        # Add some content to each page
        c.drawString(100, height - 100, f"Sample PDF - Page {i}")
        c.drawString(100, height - 150, f"This is page {i} of {num_pages}")
        c.drawString(100, height - 200, "Created for testing PDF splitter progress bars")
        
        # Add some shapes to make the PDF more realistic
        c.rect(100, height - 300, 400, 100)
        c.drawString(120, height - 250, f"Content box on page {i}")
        
        c.showPage()
    
    c.save()
    print(f"✅ Created sample PDF: {filename}")
    return True

def test_progress_bars():
    """Test the progress bar functionality with different scenarios."""
    
    # Create a temporary sample PDF
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
        sample_pdf = tmp_file.name
    
    try:
        # Create sample PDF with 25 pages (enough to see progress bars)
        if not create_sample_pdf(sample_pdf, 25):
            return
        
        print("\n" + "="*60)
        print("TESTING PROGRESS BARS")
        print("="*60)
        
        # Test 1: Normal progress bars (default)
        print("\n🧪 Test 1: Normal operation with progress bars")
        print("-" * 50)
        result = subprocess.run([
            sys.executable, 'main.py', sample_pdf, 
            '-p', '3',  # 3 pages per chunk
            '-o', 'test_output_with_progress'
        ], capture_output=False)
        
        if result.returncode == 0:
            print("✅ Test 1 passed: Progress bars worked correctly")
        else:
            print("❌ Test 1 failed")
        
        # Test 2: Disabled progress bars
        print("\n🧪 Test 2: Disabled progress bars (--no-progress)")
        print("-" * 50)
        result = subprocess.run([
            sys.executable, 'main.py', sample_pdf,
            '-p', '4',  # 4 pages per chunk
            '-o', 'test_output_no_progress',
            '--no-progress'
        ], capture_output=False)
        
        if result.returncode == 0:
            print("✅ Test 2 passed: No progress bars mode worked correctly")
        else:
            print("❌ Test 2 failed")
        
        # Test 3: Large chunks (should show nested progress for pages)
        print("\n🧪 Test 3: Large chunks with nested page progress")
        print("-" * 50)
        result = subprocess.run([
            sys.executable, 'main.py', sample_pdf,
            '-p', '15',  # 15 pages per chunk (>10, should show page progress)
            '-o', 'test_output_large_chunks'
        ], capture_output=False)
        
        if result.returncode == 0:
            print("✅ Test 3 passed: Large chunks with nested progress worked correctly")
        else:
            print("❌ Test 3 failed")
        
        print("\n" + "="*60)
        print("PROGRESS BAR TESTING COMPLETED")
        print("="*60)
        print("\nCheck the output folders to see the generated PDF chunks:")
        print("- test_output_with_progress/")
        print("- test_output_no_progress/")
        print("- test_output_large_chunks/")
        
    finally:
        # Clean up the temporary sample PDF
        if os.path.exists(sample_pdf):
            os.unlink(sample_pdf)
            print(f"\n🧹 Cleaned up temporary file: {sample_pdf}")

if __name__ == "__main__":
    print("PDF Splitter Progress Bar Test")
    print("=" * 40)
    
    # Check if main.py exists
    if not os.path.exists('main.py'):
        print("❌ main.py not found in current directory")
        sys.exit(1)
    
    test_progress_bars()
