# PDF Form Field Generator with LLM Intelligence

This Python script creates interactive form fields in PDF documents. It can intelligently analyze PDF content using Claude AI to automatically suggest where form fields should be placed, or you can manually specify field positions.

## Features

- 🤖 **LLM-Powered Field Suggestions**: Uses Claude to intelligently analyze PDFs and suggest field placements
- 📝 **Multiple Field Types**: Supports text fields, checkboxes, and dropdown menus
- 🖼️ **Visual Context Analysis**: Analyzes PDF images to identify form field locations
- 🎯 **Precise Positioning**: Define exact coordinates for field placement
- 📊 **Multi-Page Support**: Add fields across multiple pages
- 🔧 **Flexible API**: Use via command line or programmatically in Python

## Installation

1. Install required packages:
```bash
pip install pypdf anthropic pillow pdf2image --break-system-packages
```

2. Install system dependencies for pdf2image:
   - **Ubuntu/Debian**: `sudo apt-get install poppler-utils`
   - **macOS**: `brew install poppler`
   - **Windows**: Download from [poppler releases](https://github.com/oschwartz10612/poppler-windows/releases/)

3. Set up your Anthropic API key (required for auto-suggest feature):
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

Or pass it via command line with `--api-key`

## Usage

### Auto-Suggest Fields (LLM-Powered)

Let the LLM analyze your PDF and automatically suggest field placements:

```bash
python pdf_form_field_generator.py input.pdf output.pdf --auto-suggest
```

With additional context:

```bash
python pdf_form_field_generator.py input.pdf output.pdf --auto-suggest \
  --context "This is a job application form" \
  --save-suggestions suggested_fields.json
```

### Manual Field Definition

Create fields from a JSON specification file:

```bash
python pdf_form_field_generator.py input.pdf output.pdf --fields-file fields.json
```

### Field Specification Format

The `fields.json` file should contain an array of field specifications:

```json
[
  {
    "name": "first_name",
    "type": "text",
    "page": 0,
    "rect": [100, 700, 300, 720],
    "font_size": 12
  },
  {
    "name": "agree_terms",
    "type": "checkbox",
    "page": 0,
    "rect": [100, 650, 115, 665],
    "checked": false
  },
  {
    "name": "country",
    "type": "dropdown",
    "page": 0,
    "rect": [100, 600, 300, 620],
    "options": ["USA", "Canada", "UK", "Australia"],
    "default_value": ""
  }
]
```

### Field Types and Properties

#### Text Field
```json
{
  "name": "field_name",
  "type": "text",
  "page": 0,
  "rect": [x1, y1, x2, y2],
  "font_size": 12,
  "default_value": ""
}
```

#### Checkbox
```json
{
  "name": "checkbox_name",
  "type": "checkbox",
  "page": 0,
  "rect": [x1, y1, x2, y2],
  "checked": false
}
```

#### Dropdown
```json
{
  "name": "dropdown_name",
  "type": "dropdown",
  "page": 0,
  "rect": [x1, y1, x2, y2],
  "options": ["Option 1", "Option 2", "Option 3"],
  "default_value": "Option 1"
}
```

### Understanding Coordinates

PDF coordinates use points (72 points = 1 inch) with origin at bottom-left:

- `rect`: `[x1, y1, x2, y2]` where:
  - `(x1, y1)`: Bottom-left corner of the field
  - `(x2, y2)`: Top-right corner of the field
  - Y-axis starts from bottom of page

Common field dimensions:
- Text fields: 150-300 points wide, 15-20 points tall
- Checkboxes: 12-15 points square
- Signature fields: 200-300 points wide, 40-60 points tall

## How It Works

### Auto-Suggest Mode

1. **PDF Analysis**: Converts PDF pages to images
2. **Visual Context**: Sends images to Claude AI for analysis
3. **Field Suggestion**: LLM identifies likely form field locations
4. **Field Creation**: Automatically adds suggested fields to PDF
5. **Output**: Saves PDF with interactive form fields

### Manual Mode

1. **Load Specifications**: Reads field definitions from JSON
2. **Field Creation**: Creates form field annotations at specified coordinates
3. **PDF Integration**: Adds fields to the PDF's AcroForm structure
4. **Output**: Saves PDF with interactive form fields

## Programmatic Usage

```python
from pdf_form_field_generator import PDFFormFieldGenerator

# Initialize
generator = PDFFormFieldGenerator(api_key="your-api-key")

# Option 1: Auto-suggest fields
generator.process_pdf_with_suggestions(
    input_pdf="blank_form.pdf",
    output_pdf="form_with_fields.pdf",
    context="Employment application form",
    save_suggestions="suggested_fields.json"
)

# Option 2: Manual field specification
fields = [
    {
        "name": "first_name",
        "type": "text",
        "page": 0,
        "rect": [100, 700, 300, 720]
    },
    {
        "name": "email",
        "type": "text",
        "page": 0,
        "rect": [100, 670, 350, 690]
    },
    {
        "name": "agree",
        "type": "checkbox",
        "page": 0,
        "rect": [100, 630, 115, 645]
    }
]

generator.add_fields_to_pdf("input.pdf", "output.pdf", fields)
```

## Examples

See `example_usage.py` for comprehensive examples including:

1. **Basic Usage**: Adding simple text fields
2. **Multiple Field Types**: Text fields, checkboxes, and dropdowns
3. **From JSON File**: Loading field specifications from files
4. **Auto-Suggest with LLM**: Automatic field placement
5. **Multi-Page Forms**: Adding fields across multiple pages
6. **Batch Processing**: Processing multiple PDFs
7. **Signature Fields**: Creating signature and date fields

Run examples:
```bash
python example_usage.py
```

## Tips for Best Results

### For Auto-Suggest Mode

1. **Provide Context**: Use the `--context` flag to describe the form purpose
2. **Review Suggestions**: Check the saved JSON before using it
3. **Adjust Coordinates**: Fine-tune suggested positions if needed
4. **Clear PDFs Work Best**: High-quality, well-formatted PDFs produce better results

### For Manual Mode

1. **Use PDF Viewers**: Open your PDF in a viewer that shows coordinates
2. **Test Incrementally**: Add a few fields, test, then add more
3. **Check Dimensions**: Ensure fields are appropriately sized
4. **Page Indexing**: Remember pages are 0-indexed (first page is 0)

### General

1. **Field Names**: Use clear, descriptive names (e.g., "first_name", not "fn")
2. **Visual Alignment**: Align fields with any existing text or lines in the PDF
3. **Test Output**: Always open the output PDF to verify field placement
4. **Font Sizes**: Typical form fields use 10-14 point fonts

## Troubleshooting

### "Error: pypdf not installed"
Run: `pip install pypdf --break-system-packages`

### "Error: anthropic not installed"
Run: `pip install anthropic --break-system-packages`

### "Unable to get page count. Is poppler installed?"
Install poppler-utils (see Installation section)

### "AuthenticationError"
Make sure your Anthropic API key is set correctly (only needed for auto-suggest)

### Fields not appearing in PDF
- Verify the coordinates are within the page bounds
- Check that the page number is correct (0-indexed)
- Try opening with different PDF viewers (Adobe, Preview, Chrome, etc.)
- Some viewers require clicking to see form fields

### Fields in wrong location
- Remember: Y-axis starts from bottom, not top
- Verify rect coordinates: [x1, y1, x2, y2] where (x1,y1) is bottom-left
- Get page dimensions: typically 612x792 points for letter size (8.5"x11")

## Use Cases

- **Converting Paper Forms**: Turn scanned or static PDFs into fillable forms
- **Form Template Creation**: Create reusable form templates
- **Automated Form Generation**: Programmatically generate custom forms
- **Document Workflows**: Add interactive elements to existing documents
- **Data Collection**: Create forms for collecting structured information

## API Costs

The auto-suggest feature uses the Anthropic Claude API. Each analysis typically uses:
- **With images**: ~2,000-8,000 tokens (depending on number of pages)
- **Manual mode**: No API calls required

Check current API pricing at https://www.anthropic.com/pricing

## License

This script uses several open-source libraries and the Anthropic API. Make sure to review their respective licenses and terms of use.

## Additional Notes

- Created fields are interactive and can be filled in any PDF viewer
- Fields support standard PDF form features (validation, calculation, etc. can be added)
- Output PDFs are compatible with all major PDF viewers and form filling tools
- The pypdf library creates PDF 1.7 compatible form fields
