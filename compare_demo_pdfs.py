#!/usr/bin/env python3
"""
Compare the before and after demo PDFs to show the difference.
"""

from pypdf import PdfReader
import os

def analyze_pdf(filename):
    """Analyze a PDF and return information about it."""
    reader = PdfReader(filename)

    info = {
        "filename": filename,
        "file_size": os.path.getsize(filename),
        "num_pages": len(reader.pages),
        "has_form": False,
        "num_fields": 0,
        "field_names": []
    }

    # Check for form fields
    fields = reader.get_fields()
    if fields:
        info["has_form"] = True
        info["num_fields"] = len(fields)
        info["field_names"] = list(fields.keys())

    return info

def format_size(size_bytes):
    """Format bytes into human-readable size."""
    for unit in ['B', 'KB', 'MB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} GB"

def main():
    print("\n" + "=" * 70)
    print("PDF FORM FIELD GENERATOR - DEMO COMPARISON")
    print("=" * 70)

    before_file = "demo_form_before.pdf"
    after_file = "demo_form_after.pdf"

    # Check if files exist
    if not os.path.exists(before_file):
        print(f"\n❌ ERROR: {before_file} not found!")
        print("   Run: python3 create_demo_form.py")
        return

    if not os.path.exists(after_file):
        print(f"\n❌ ERROR: {after_file} not found!")
        print("   Run: python3 add_fields_to_demo.py")
        return

    # Analyze both PDFs
    before = analyze_pdf(before_file)
    after = analyze_pdf(after_file)

    # Display comparison
    print("\n" + "-" * 70)
    print("BEFORE (Static Form)")
    print("-" * 70)
    print(f"  File:              {before['filename']}")
    print(f"  Size:              {format_size(before['file_size'])}")
    print(f"  Pages:             {before['num_pages']}")
    print(f"  Has Form Fields:   {'✅ Yes' if before['has_form'] else '❌ No'}")
    print(f"  Number of Fields:  {before['num_fields']}")
    print("\n  Description:")
    print("    - This is a STATIC PDF with no interactive fields")
    print("    - You can view it but cannot fill it electronically")
    print("    - To complete it, you would need to print and write by hand")

    print("\n" + "-" * 70)
    print("AFTER (Interactive Form)")
    print("-" * 70)
    print(f"  File:              {after['filename']}")
    print(f"  Size:              {format_size(after['file_size'])}")
    print(f"  Pages:             {after['num_pages']}")
    print(f"  Has Form Fields:   {'✅ Yes' if after['has_form'] else '❌ No'}")
    print(f"  Number of Fields:  {after['num_fields']}")

    if after['has_form']:
        print("\n  Interactive Fields:")

        # Categorize fields
        text_fields = [f for f in after['field_names'] if not any(x in f for x in ['citizen', 'over', 'background'])]
        checkboxes = [f for f in after['field_names'] if any(x in f for x in ['citizen', 'over', 'background'])]

        print(f"    ✏️  Text Fields ({len(text_fields)}):")
        for field in text_fields:
            print(f"        - {field}")

        print(f"\n    ☑️  Checkboxes ({len(checkboxes)}):")
        for field in checkboxes:
            print(f"        - {field}")

        print("\n  Description:")
        print("    - This is an INTERACTIVE PDF with fillable form fields")
        print("    - Click on any field to type directly into the PDF")
        print("    - Checkboxes can be clicked to check/uncheck")
        print("    - No printing required - fill it out digitally!")

    # Show the difference
    print("\n" + "=" * 70)
    print("KEY DIFFERENCES")
    print("=" * 70)
    print(f"  Fields Added:      {after['num_fields'] - before['num_fields']}")
    print(f"  Size Increase:     {format_size(after['file_size'] - before['file_size'])}")
    print(f"  Size Ratio:        {after['file_size'] / before['file_size']:.1f}x larger")

    print("\n  What Changed:")
    print("    ➡️  Added 17 interactive form fields")
    print("    ➡️  14 text input fields for names, addresses, etc.")
    print("    ➡️  3 checkboxes for yes/no questions")
    print("    ➡️  All fields are positioned precisely over the form lines")
    print("    ➡️  Users can now fill the form electronically")

    print("\n" + "=" * 70)
    print("HOW TO TEST")
    print("=" * 70)
    print("  1. Open demo_form_before.pdf in a PDF viewer")
    print("     → Try clicking on the form - nothing happens (static)")
    print()
    print("  2. Open demo_form_after.pdf in a PDF viewer")
    print("     → Click on any field - you can type! (interactive)")
    print()
    print("  Recommended viewers:")
    print("    - Adobe Acrobat Reader (best support)")
    print("    - Preview (Mac)")
    print("    - Evince (Linux)")
    print("    - Chrome/Firefox (basic support)")

    print("\n" + "=" * 70)
    print("✅ Both demo files are ready!")
    print("=" * 70)
    print()

if __name__ == "__main__":
    main()
