#!/usr/bin/env python3
"""
Script to generate a PDF from a local HTML file using Playwright.

Usage:
  python src/generatePDF.js [path/to/file.html] [output/path.pdf]

If no arguments are provided, default values are used:
  - HTML file: ./index.html (project root)
  - PDF file:  ./cv.pdf
"""

import sys
import os
from pathlib import Path
import asyncio

from playwright.async_api import async_playwright


async def generate_pdf(html_path: str, pdf_path: str):
    # Resolve absolute paths
    html_file = Path(html_path).resolve() if Path(html_path).is_absolute() else Path.cwd() / html_path
    pdf_file = Path(pdf_path).resolve() if Path(pdf_path).is_absolute() else Path.cwd() / pdf_path

    # Verify that the HTML file exists
    if not html_file.is_file():
        raise FileNotFoundError(f"HTML file not found at: {html_file}")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        # Load the local HTML file
        await page.goto(f"file://{html_file}")
        # Generate the PDF
        await page.pdf(
            path=str(pdf_file),
            format="Letter",
            print_background=True
        )
        await browser.close()
        print(f"✅ PDF successfully generated at: {pdf_file}")


def main():
    # Default parameters
    default_html = "index.html"
    default_pdf = "cv.pdf"

    # CLI arguments (skip the script name)
    args = sys.argv[1:]
    html_arg = args[0] if len(args) > 0 else default_html
    pdf_arg = args[1] if len(args) > 1 else default_pdf

    try:
        asyncio.run(generate_pdf(html_arg, pdf_arg))
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
