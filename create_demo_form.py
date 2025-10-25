#!/usr/bin/env python3
"""
Generate a demo blank form PDF for demonstration purposes.
This creates a realistic-looking form WITHOUT interactive fields.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def draw_text_field_line(c, x, y, width, label, label_width=2.0):
    """Draw a label and a line for text input."""
    # Draw label
    c.setFont("Helvetica", 10)
    c.drawString(x * inch, y * inch, label)

    # Draw line for input
    line_start_x = (x + label_width) * inch
    line_end_x = (x + label_width + width) * inch
    c.line(line_start_x, y * inch, line_end_x, y * inch)

def draw_checkbox(c, x, y, label, label_offset=0.3):
    """Draw a checkbox (empty square) with label."""
    # Draw empty square
    square_size = 0.15 * inch
    c.rect(x * inch, y * inch, square_size, square_size)

    # Draw label
    c.setFont("Helvetica", 10)
    c.drawString((x + label_offset) * inch, y * inch, label)

def create_demo_form(filename="demo_form_before.pdf"):
    """Create a realistic job application form."""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 0.75 * inch, "Job Application Form")

    # Subtitle
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, height - 1.0 * inch, "Please complete all fields")

    # Personal Information Section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.75 * inch, height - 1.5 * inch, "Personal Information")

    # First Name
    draw_text_field_line(c, 0.75, height / inch - 2.0, 2.5, "First Name:", 1.2)

    # Last Name
    draw_text_field_line(c, 4.75, height / inch - 2.0, 2.5, "Last Name:", 1.1)

    # Email
    draw_text_field_line(c, 0.75, height / inch - 2.5, 6.5, "Email Address:", 1.5)

    # Phone
    draw_text_field_line(c, 0.75, height / inch - 3.0, 3.0, "Phone Number:", 1.5)

    # Date of Birth
    draw_text_field_line(c, 0.75, height / inch - 3.5, 2.0, "Date of Birth:", 1.5)

    # Address Section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.75 * inch, height - 4.25 * inch, "Address")

    # Street
    draw_text_field_line(c, 0.75, height / inch - 4.75, 6.5, "Street Address:", 1.5)

    # City
    draw_text_field_line(c, 0.75, height / inch - 5.25, 2.5, "City:", 0.6)

    # State
    draw_text_field_line(c, 4.0, height / inch - 5.25, 1.0, "State:", 0.7)

    # ZIP
    draw_text_field_line(c, 6.0, height / inch - 5.25, 1.5, "ZIP:", 0.5)

    # Employment Information
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.75 * inch, height - 6.0 * inch, "Employment Information")

    # Position Applied For
    draw_text_field_line(c, 0.75, height / inch - 6.5, 6.5, "Position Applied For:", 2.0)

    # Available Start Date
    draw_text_field_line(c, 0.75, height / inch - 7.0, 2.5, "Available Start Date:", 2.0)

    # Desired Salary
    draw_text_field_line(c, 4.75, height / inch - 7.0, 2.0, "Desired Salary:", 1.7)

    # Checkboxes Section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.75 * inch, height - 7.75 * inch, "Eligibility")

    # US Citizen checkbox
    draw_checkbox(c, 0.75, height / inch - 8.25, "I am a U.S. Citizen or authorized to work in the U.S.", 0.3)

    # Over 18 checkbox
    draw_checkbox(c, 0.75, height / inch - 8.60, "I am 18 years of age or older", 0.3)

    # Background check checkbox
    draw_checkbox(c, 0.75, height / inch - 8.95, "I agree to a background check", 0.3)

    # Signature Section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.75 * inch, height - 9.5 * inch, "Signature")

    # Signature line
    c.setFont("Helvetica", 10)
    c.drawString(0.75 * inch, height - 10.0 * inch, "Signature:")
    c.line(1.5 * inch, height - 10.0 * inch, 4.5 * inch, height - 10.0 * inch)

    # Date line
    c.drawString(5.0 * inch, height - 10.0 * inch, "Date:")
    c.line(5.5 * inch, height - 10.0 * inch, 7.5 * inch, height - 10.0 * inch)

    # Footer
    c.setFont("Helvetica", 8)
    c.drawCentredString(width / 2, 0.5 * inch,
                       "This is a demo form - NOT interactive (no form fields yet)")

    # Save
    c.save()
    print(f"Created demo form: {filename}")
    print(f"  - This PDF has NO interactive fields")
    print(f"  - It's just a static form with lines and labels")

if __name__ == "__main__":
    create_demo_form()
