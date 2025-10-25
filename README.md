# PDF Form Filler with LLM Intelligence

This Python script uses an LLM (Claude) to intelligently map your data to PDF form fields. It automatically figures out which fields should contain which data based on field names and context.

## Features

- 🤖 **LLM-Powered Mapping**: Uses Claude to intelligently match your data to form fields
- 📝 **Fillable PDF Support**: Works with PDFs that have interactive form fields
- 🖼️ **Visual Context**: Analyzes PDF images to better understand form structure
- 🎯 **Smart Field Matching**: Handles various field naming conventions (e.g., "fname", "firstName", "first_name")
- ✅ **Checkbox Handling**: Automatically determines checkbox values
- 📊 **Detailed Logging**: Shows which data maps to which fields and why

## Installation

1. Install required packages:
```bash
pip install pypdf anthropic pillow pdf2image --break-system-packages
```

2. Install system dependencies for pdf2image:
   - **Ubuntu/Debian**: `sudo apt-get install poppler-utils`
   - **macOS**: `brew install poppler`
   - **Windows**: Download from [poppler releases](https://github.com/oschwartz10612/poppler-windows/releases/)

3. Set up your Anthropic API key:
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

Or pass it via command line with `--api-key`

## Usage

### Basic Usage with JSON String

```bash
python pdf_form_filler.py input.pdf output.pdf --data '{"first_name": "John", "last_name": "Doe", "email": "john@example.com"}'
```

### Using a JSON File

```bash
python pdf_form_filler.py input.pdf output.pdf --data-file my_data.json
```

### With API Key

```bash
python pdf_form_filler.py input.pdf output.pdf --data-file my_data.json --api-key "your-api-key"
```

## Data Format

Your JSON data should be a simple key-value object:

```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane.smith@example.com",
  "phone": "+1-555-0123",
  "date_of_birth": "1990-05-15",
  "address": "123 Main St, Anytown, USA",
  "is_citizen": true,
  "subscribe_newsletter": false
}
```

The LLM will intelligently map these to form fields even if the field names don't match exactly.

## How It Works

1. **Field Detection**: Extracts all fillable form fields from the PDF
2. **Visual Analysis**: Converts PDF pages to images for context
3. **LLM Mapping**: Sends field information and your data to Claude, which intelligently maps them
4. **Form Filling**: Fills the PDF with the mapped values
5. **Output**: Saves the completed PDF

## Example Field Mappings

The LLM understands various naming conventions:

| Your Data Key | Matches Fields Like |
|---------------|---------------------|
| `first_name` | fname, firstName, First_Name, given_name |
| `email` | email_address, e-mail, Email, contact_email |
| `phone` | phone_number, telephone, tel, mobile |
| `date_of_birth` | dob, birth_date, DOB, birthdate |
| `is_citizen` | citizen, us_citizen, citizenship (checkbox) |

## Advanced Usage

### Programmatic Usage

```python
from pdf_form_filler import PDFFormFiller

# Initialize
filler = PDFFormFiller(api_key="your-api-key")

# Prepare your data
user_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
}

# Process the PDF
filler.process_pdf("input.pdf", "output.pdf", user_data)
```

### Checking If PDF Is Fillable

```python
from pdf_form_filler import PDFFormFiller

filler = PDFFormFiller()
is_fillable = filler.check_if_fillable("myform.pdf")
print(f"PDF is fillable: {is_fillable}")
```

## Non-Fillable PDFs

If your PDF doesn't have fillable form fields (returns "NOT fillable"), you'll need to use the annotation-based approach. The script will still:
- Convert the PDF to images for analysis
- Help you identify where fields should go

For non-fillable PDFs, follow the instructions in the PDF skill's `FORMS.md` file to create bounding boxes manually.

## Troubleshooting

### "Error: pypdf not installed"
Run: `pip install pypdf --break-system-packages`

### "Error: anthropic not installed"
Run: `pip install anthropic --break-system-packages`

### "Unable to get page count. Is poppler installed?"
Install poppler-utils (see Installation section)

### "AuthenticationError"
Make sure your Anthropic API key is set correctly via environment variable or `--api-key` flag

### Fields not filling correctly
- Check that your data keys are descriptive (e.g., "email" not just "e")
- Review the console output to see how the LLM mapped your fields
- Make sure your PDF actually has fillable form fields

## Tips for Best Results

1. **Use Descriptive Keys**: Instead of abbreviated keys like "fn", use "first_name"
2. **Include Context**: If a field might be ambiguous, add more context to your data key
3. **Check Field Types**: For checkboxes, use boolean values (true/false) in your data
4. **Test First**: Try with a sample PDF to see how the mapping works
5. **Review Logs**: The script shows detailed reasoning for each field mapping

## License

This script uses several open-source libraries and the Anthropic API. Make sure to review their respective licenses and terms of use.

## API Costs

This script uses the Anthropic Claude API. Each form fill typically uses:
- **With images**: ~2,000-5,000 tokens (including image processing)
- **Without images**: ~500-1,000 tokens

Check current API pricing at https://www.anthropic.com/pricing
