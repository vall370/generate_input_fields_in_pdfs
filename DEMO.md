# PDF Form Field Generator - Demo

This demo shows the **before** and **after** of adding interactive form fields to a PDF document.

## Quick Start

Run the demo script to generate both versions:

```bash
# Generate the before version (static form)
python3 create_demo_form.py

# Add interactive fields to create the after version
python3 add_fields_to_demo.py
```

This creates two PDFs:
- **demo_form_before.pdf** - Static form with no interactive fields
- **demo_form_after.pdf** - Same form with 17 interactive fillable fields

## What's the Difference?

### BEFORE (demo_form_before.pdf)

The "before" PDF is a **static document** that looks like a form but has NO interactive fields:
- You see labels like "First Name:", "Email:", etc.
- There are lines where users would write
- There are empty squares that look like checkboxes
- **You CANNOT type into this PDF** - it's just a static image/document
- To fill it out, you'd need to print it and write by hand

### AFTER (demo_form_after.pdf)

The "after" PDF has **17 interactive form fields** added:
- **Click on any field** and you can type directly into the PDF
- Text fields appear when you click on them
- Checkboxes can be clicked to check/uncheck
- **No printing required** - fill it out digitally
- The filled form can be saved and shared electronically

## How to Test the Demo

### 1. View the BEFORE version

```bash
# Open with your default PDF viewer
xdg-open demo_form_before.pdf  # Linux
# or
open demo_form_before.pdf      # Mac
```

Try to click on the form fields - nothing happens! It's just a static document.

### 2. View the AFTER version

```bash
# Open with your default PDF viewer
xdg-open demo_form_after.pdf   # Linux
# or
open demo_form_after.pdf       # Mac
```

Now try clicking on the fields - they're interactive! You can:
- Type in the text fields (name, email, address, etc.)
- Click the checkboxes to check/uncheck them
- Tab through fields like a web form
- Save the filled PDF with your data

## Interactive Fields Added

The "after" version includes these 17 interactive fields:

### Text Fields (14)
1. **first_name** - First name input
2. **last_name** - Last name input
3. **email** - Email address
4. **phone** - Phone number
5. **date_of_birth** - Birth date
6. **street_address** - Street address
7. **city** - City name
8. **state** - State (2-letter code)
9. **zip_code** - ZIP code
10. **position** - Job position applied for
11. **start_date** - Available start date
12. **salary** - Desired salary
13. **signature** - Digital signature
14. **date_signed** - Date signed

### Checkboxes (3)
15. **us_citizen** - US citizen or authorized to work
16. **over_18** - 18 years or older
17. **background_check** - Agrees to background check

## How the Fields Were Added

The `add_fields_to_demo.py` script uses the `PDFFormFieldGenerator` class:

```python
from pdf_form_field_generator import PDFFormFieldGenerator

generator = PDFFormFieldGenerator()

fields = [
    {
        "name": "first_name",
        "type": "text",
        "page": 0,
        "rect": [138, 644, 318, 664],  # [x1, y1, x2, y2] coordinates
        "font_size": 11
    },
    {
        "name": "us_citizen",
        "type": "checkbox",
        "page": 0,
        "rect": [54, 194, 69, 209],
        "checked": False
    },
    # ... more fields
]

generator.add_fields_to_pdf("demo_form_before.pdf", "demo_form_after.pdf", fields)
```

## Coordinate System Explained

PDF coordinates use **points** (72 points = 1 inch) with the origin at the **bottom-left**:

- **X-axis**: Left (0) to Right (612 for letter size)
- **Y-axis**: Bottom (0) to Top (792 for letter size)
- **rect**: `[x1, y1, x2, y2]` where:
  - `(x1, y1)` = bottom-left corner of field
  - `(x2, y2)` = top-right corner of field

Example:
```python
"rect": [138, 644, 318, 664]
# This creates a field:
# - Starting 138 points from left
# - Starting 644 points from bottom
# - 180 points wide (318 - 138)
# - 20 points tall (664 - 644)
```

## Real-World Applications

This demo shows how you can:

1. **Convert Paper Forms** - Take scanned or static PDFs and make them interactive
2. **Digitize Processes** - Replace paper forms with fillable PDFs
3. **Automate Workflows** - Create forms programmatically
4. **Improve UX** - Let users fill forms on their devices instead of printing

## Try It Yourself

### Modify the Demo

1. Edit `create_demo_form.py` to change the form layout
2. Edit `add_fields_to_demo.py` to adjust field positions
3. Re-run both scripts to see your changes

### Create Your Own Form

1. Create a blank PDF with labels/lines (use `create_demo_form.py` as a template)
2. Define your field specifications in a Python script or JSON file
3. Use `PDFFormFieldGenerator` to add the interactive fields

### Use Auto-Suggest Feature

Instead of manually specifying coordinates, let Claude AI suggest field positions:

```bash
python pdf_form_field_generator.py demo_form_before.pdf demo_form_auto.pdf \
  --auto-suggest \
  --context "This is a job application form" \
  --save-suggestions suggested_fields.json
```

## Viewing Tips

### Desktop PDF Viewers
- **Adobe Acrobat Reader** - Best support, shows all field features
- **Preview (Mac)** - Good support, clean interface
- **Evince (Linux)** - Good support for form fields
- **Chrome/Firefox** - Basic support, may require clicking to see fields

### Mobile PDF Viewers
- Most mobile PDF apps support interactive forms
- Some may require downloading the filled PDF to save changes

## Troubleshooting

### Fields don't appear?
- Try a different PDF viewer (Adobe Acrobat recommended)
- Some viewers require clicking on the field area to activate it
- Check that the field coordinates are within page bounds

### Fields in wrong position?
- Remember: Y-axis starts from bottom, not top
- Adjust the `rect` coordinates in `add_fields_to_demo.py`
- Use `print()` to debug coordinate calculations

### Can't type in fields?
- Make sure you're viewing the "after" version
- Click directly on the field area
- Try using Tab key to navigate between fields

## Next Steps

1. Read the main [README.md](README.md) for full documentation
2. Check out [example_usage.py](example_usage.py) for more examples
3. Try the auto-suggest feature with your own PDFs
4. Create custom forms for your specific use cases

## Questions?

The demo shows a simple job application form, but the same technique works for:
- Medical forms
- Registration forms
- Survey forms
- Contract templates
- Invoice templates
- Any document that needs user input!

Enjoy creating interactive PDF forms!
