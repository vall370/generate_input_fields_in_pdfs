#!/usr/bin/env python3
"""
Simple test script for the PDF Form Field Generator
"""

from pdf_form_field_generator import PDFFormFieldGenerator
from pypdf import PdfWriter
import os

def create_blank_pdf(filename, width=612, height=792):
    """Create a simple blank PDF for testing."""
    writer = PdfWriter()
    writer.add_blank_page(width=width, height=height)
    with open(filename, 'wb') as f:
        writer.write(f)
    print(f"Created blank PDF: {filename}")

def test_basic_field_creation():
    """Test basic field creation without LLM."""
    print("\n" + "="*60)
    print("TEST: Basic Field Creation")
    print("="*60)

    # Create a blank PDF for testing
    test_input = "test_blank.pdf"
    test_output = "test_output.pdf"

    create_blank_pdf(test_input)

    # Initialize generator (no API key needed for manual mode)
    generator = PDFFormFieldGenerator()

    # Define test fields
    fields = [
        {
            "name": "test_text_field",
            "type": "text",
            "page": 0,
            "rect": [100, 700, 300, 720],
            "font_size": 12
        },
        {
            "name": "test_checkbox",
            "type": "checkbox",
            "page": 0,
            "rect": [100, 650, 115, 665],
            "checked": False
        },
        {
            "name": "test_dropdown",
            "type": "dropdown",
            "page": 0,
            "rect": [100, 600, 300, 620],
            "options": ["Option A", "Option B", "Option C"],
            "default_value": ""
        }
    ]

    try:
        # Add fields to PDF
        generator.add_fields_to_pdf(test_input, test_output, fields)

        print("\n✅ SUCCESS: PDF with form fields created!")
        print(f"   Input:  {test_input}")
        print(f"   Output: {test_output}")
        print("\nYou can open the output PDF to verify the fields were created.")

        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def cleanup_test_files():
    """Clean up test files."""
    test_files = ["test_blank.pdf", "test_output.pdf"]
    for f in test_files:
        if os.path.exists(f):
            os.remove(f)
            print(f"Cleaned up: {f}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("PDF FORM FIELD GENERATOR - TEST SUITE")
    print("="*60)

    success = test_basic_field_creation()

    if success:
        print("\n" + "="*60)
        print("ALL TESTS PASSED!")
        print("="*60)
        print("\nTo clean up test files, uncomment the line below:")
        print("# cleanup_test_files()")
    else:
        print("\n" + "="*60)
        print("TESTS FAILED")
        print("="*60)

    print()
