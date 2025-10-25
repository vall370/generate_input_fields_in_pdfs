#!/usr/bin/env python3
"""
Add interactive form fields to the demo form.
This creates the 'after' version with actual fillable fields.
"""

from pdf_form_field_generator import PDFFormFieldGenerator

def add_fields_to_demo():
    """Add interactive fields to the demo form."""

    generator = PDFFormFieldGenerator()

    # Page height for letter size = 792 points
    # 1 inch = 72 points

    # Calculate field positions (matching the lines in the original form)
    # Y coordinates start from bottom, so we need to calculate based on page height

    fields = [
        # Personal Information Section
        # First Name - line at y = height - 2.0 inches = 792 - 144 = 648
        {
            "name": "first_name",
            "type": "text",
            "page": 0,
            "rect": [138, 644, 318, 664],  # Above the line
            "font_size": 11
        },
        # Last Name - line at same y as first name
        {
            "name": "last_name",
            "type": "text",
            "page": 0,
            "rect": [421, 644, 601, 664],
            "font_size": 11
        },
        # Email - line at y = height - 2.5 inches = 792 - 180 = 612
        {
            "name": "email",
            "type": "text",
            "page": 0,
            "rect": [162, 608, 630, 628],
            "font_size": 11
        },
        # Phone - line at y = height - 3.0 inches = 792 - 216 = 576
        {
            "name": "phone",
            "type": "text",
            "page": 0,
            "rect": [162, 572, 378, 592],
            "font_size": 11
        },
        # Date of Birth - line at y = height - 3.5 inches = 792 - 252 = 540
        {
            "name": "date_of_birth",
            "type": "text",
            "page": 0,
            "rect": [162, 536, 306, 556],
            "font_size": 11
        },

        # Address Section
        # Street - line at y = height - 4.75 inches = 792 - 342 = 450
        {
            "name": "street_address",
            "type": "text",
            "page": 0,
            "rect": [162, 446, 630, 466],
            "font_size": 11
        },
        # City - line at y = height - 5.25 inches = 792 - 378 = 414
        {
            "name": "city",
            "type": "text",
            "page": 0,
            "rect": [97, 410, 277, 430],
            "font_size": 11
        },
        # State - line at same y as city
        {
            "name": "state",
            "type": "text",
            "page": 0,
            "rect": [338, 410, 410, 430],
            "font_size": 11
        },
        # ZIP - line at same y as city
        {
            "name": "zip_code",
            "type": "text",
            "page": 0,
            "rect": [468, 410, 576, 430],
            "font_size": 11
        },

        # Employment Information
        # Position Applied For - line at y = height - 6.5 inches = 792 - 468 = 324
        {
            "name": "position",
            "type": "text",
            "page": 0,
            "rect": [198, 320, 630, 340],
            "font_size": 11
        },
        # Available Start Date - line at y = height - 7.0 inches = 792 - 504 = 288
        {
            "name": "start_date",
            "type": "text",
            "page": 0,
            "rect": [198, 284, 378, 304],
            "font_size": 11
        },
        # Desired Salary - line at same y
        {
            "name": "salary",
            "type": "text",
            "page": 0,
            "rect": [464, 284, 608, 304],
            "font_size": 11
        },

        # Checkboxes - y = height - 8.25 inches = 792 - 594 = 198
        # US Citizen checkbox
        {
            "name": "us_citizen",
            "type": "checkbox",
            "page": 0,
            "rect": [54, 194, 69, 209],
            "checked": False
        },
        # Over 18 checkbox - y = height - 8.60 inches = 792 - 619.2 = 172.8
        {
            "name": "over_18",
            "type": "checkbox",
            "page": 0,
            "rect": [54, 169, 69, 184],
            "checked": False
        },
        # Background check checkbox - y = height - 8.95 inches = 792 - 644.4 = 147.6
        {
            "name": "background_check",
            "type": "checkbox",
            "page": 0,
            "rect": [54, 144, 69, 159],
            "checked": False
        },

        # Signature Section
        # Signature - line at y = height - 10.0 inches = 792 - 720 = 72
        {
            "name": "signature",
            "type": "text",
            "page": 0,
            "rect": [108, 68, 324, 88],
            "font_size": 11
        },
        # Date - line at same y
        {
            "name": "date_signed",
            "type": "text",
            "page": 0,
            "rect": [396, 68, 540, 88],
            "font_size": 11
        }
    ]

    print(f"\nAdding {len(fields)} interactive form fields to the demo form...")
    print("=" * 60)

    # Add fields to the PDF
    generator.add_fields_to_pdf(
        input_pdf="demo_form_before.pdf",
        output_pdf="demo_form_after.pdf",
        fields=fields
    )

    print("\n" + "=" * 60)
    print("SUCCESS! Created two versions:")
    print("  BEFORE: demo_form_before.pdf  (static form, no fields)")
    print("  AFTER:  demo_form_after.pdf   (interactive form with fillable fields)")
    print("\nOpen both PDFs to see the difference!")
    print("In the 'after' version, you can click and type in the fields.")

if __name__ == "__main__":
    add_fields_to_demo()
