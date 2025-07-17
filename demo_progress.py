#!/usr/bin/env python3
"""
Demo script showing the new progress bar features in the PDF splitter.
"""

import click
import time

def demo_progress_bars():
    """Demonstrate different types of progress bars available."""
    
    click.echo("🎯 PDF Splitter Progress Bar Demo")
    click.echo("=" * 50)
    
    # Demo 1: Basic progress bar
    click.echo("\n📊 Demo 1: Basic Progress Bar")
    click.echo("-" * 30)
    
    items = range(10)
    with click.progressbar(items, label='Processing chunks') as bar:
        for item in bar:
            time.sleep(0.2)  # Simulate work
    
    # Demo 2: Progress bar with ETA and percentage
    click.echo("\n📊 Demo 2: Progress Bar with ETA and Percentage")
    click.echo("-" * 45)
    
    items = range(15)
    with click.progressbar(items, 
                         label='Creating PDF chunks',
                         show_eta=True,
                         show_percent=True) as bar:
        for item in bar:
            time.sleep(0.15)  # Simulate work
    
    # Demo 3: Nested progress bars (simulating chunk + page processing)
    click.echo("\n📊 Demo 3: Nested Progress Bars (Chunks + Pages)")
    click.echo("-" * 45)
    
    chunks = range(5)
    with click.progressbar(chunks, 
                         label='Processing PDF chunks',
                         show_eta=True,
                         show_percent=True) as chunk_bar:
        for chunk in chunk_bar:
            # Simulate processing pages within each chunk
            pages = range(12)  # 12 pages per chunk
            with click.progressbar(pages,
                                 label=f'  Chunk {chunk+1} pages',
                                 show_eta=False,
                                 show_percent=False) as page_bar:
                for page in page_bar:
                    time.sleep(0.05)  # Simulate page processing
    
    click.echo("\n✅ Demo completed!")
    click.echo("\nThese are the types of progress bars you'll see when using the PDF splitter:")
    click.echo("• Main chunk processing progress (with ETA and percentage)")
    click.echo("• Nested page processing progress (for large chunks >10 pages)")
    click.echo("• External tool progress (pdftk/qpdf chunk creation)")
    click.echo("\nUse --no-progress flag to disable progress bars for scripting.")

if __name__ == "__main__":
    demo_progress_bars()
