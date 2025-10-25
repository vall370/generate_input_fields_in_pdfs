#!/usr/bin/env python3
"""
PDF Form Filler with LLM Intelligence

This script uses an LLM to intelligently map input data to PDF form fields.
It can handle both fillable PDF forms and non-fillable PDFs.

Requirements:
    pip install pypdf anthropic pillow pdf2image --break-system-packages

Usage:
    python pdf_form_filler.py <input_pdf> <output_pdf> --data '{"name": "John Doe", "email": "john@example.com"}'
    
    Or use a JSON file:
    python pdf_form_filler.py <input_pdf> <output_pdf> --data-file data.json
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import base64
from io import BytesIO

try:
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import NameObject
except ImportError:
    print("Error: pypdf not installed. Run: pip install pypdf --break-system-packages")
    sys.exit(1)

try:
    from anthropic import Anthropic
except ImportError:
    print("Error: anthropic not installed. Run: pip install anthropic --break-system-packages")
    sys.exit(1)

try:
    from PIL import Image
    from pdf2image import convert_from_path
except ImportError:
    print("Error: PIL or pdf2image not installed. Run: pip install pillow pdf2image --break-system-packages")
    sys.exit(1)


class PDFFormFiller:
    """Main class for filling PDF forms using LLM intelligence."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with Anthropic API key."""
        self.client = Anthropic(api_key=api_key) if api_key else Anthropic()
    
    def check_if_fillable(self, pdf_path: str) -> bool:
        """Check if PDF has fillable form fields."""
        try:
            reader = PdfReader(pdf_path)
            if reader.get_form_text_fields() or reader.get_fields():
                return True
            return False
        except Exception as e:
            print(f"Error checking PDF: {e}")
            return False
    
    def extract_fillable_fields(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extract information about fillable form fields."""
        reader = PdfReader(pdf_path)
        fields = []
        
        form_fields = reader.get_fields()
        if not form_fields:
            return fields
        
        for field_name, field_data in form_fields.items():
            field_info = {
                "field_id": field_name,
                "type": self._get_field_type(field_data),
                "page": self._get_field_page(reader, field_name),
            }
            
            # Add additional info based on type
            if field_info["type"] == "checkbox":
                field_info["current_value"] = field_data.get("/V", "")
            elif field_info["type"] == "choice":
                if "/Opt" in field_data:
                    field_info["options"] = field_data["/Opt"]
            
            fields.append(field_info)
        
        return fields
    
    def _get_field_type(self, field_data: Dict) -> str:
        """Determine the type of a form field."""
        if "/FT" not in field_data:
            return "unknown"
        
        field_type = field_data["/FT"]
        if field_type == "/Tx":
            return "text"
        elif field_type == "/Btn":
            if "/Opt" in field_data:
                return "radio_group"
            return "checkbox"
        elif field_type == "/Ch":
            return "choice"
        return "unknown"
    
    def _get_field_page(self, reader: PdfReader, field_name: str) -> int:
        """Get the page number for a field."""
        for i, page in enumerate(reader.pages):
            if "/Annots" in page:
                for annot in page["/Annots"]:
                    annot_obj = annot.get_object()
                    if "/T" in annot_obj and annot_obj["/T"] == field_name:
                        return i + 1
        return 1  # Default to page 1 if not found
    
    def convert_pdf_to_images(self, pdf_path: str) -> List[Image.Image]:
        """Convert PDF pages to images."""
        print("Converting PDF to images...")
        images = convert_from_path(pdf_path, dpi=150)
        return images
    
    def image_to_base64(self, image: Image.Image) -> str:
        """Convert PIL Image to base64 string."""
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    
    def map_data_to_fields_llm(
        self, 
        fields: List[Dict[str, Any]], 
        user_data: Dict[str, Any],
        pdf_images: Optional[List[Image.Image]] = None
    ) -> Dict[str, Any]:
        """Use LLM to intelligently map user data to form fields."""
        
        print("Using LLM to map data to fields...")
        
        # Prepare the prompt
        prompt = f"""You are a PDF form-filling assistant. Your task is to map user-provided data to form fields.

User Data:
{json.dumps(user_data, indent=2)}

Form Fields:
{json.dumps(fields, indent=2)}

Instructions:
1. Analyze the field names and types
2. Match the user data to the most appropriate fields
3. For each field that should be filled, provide the field_id and the value to use
4. If user data doesn't match any field, skip it
5. For checkboxes, determine if they should be checked based on the data
6. Return your response as a JSON object with this structure:

{{
  "field_mappings": [
    {{
      "field_id": "field_name_here",
      "value": "value_to_fill",
      "reasoning": "why this mapping makes sense"
    }}
  ]
}}

Be intelligent about field names. For example:
- "fname", "first_name", "firstName" all likely mean first name
- "email", "email_address", "e-mail" all mean email
- Dates might be in various formats
- Checkboxes often need "/Yes" or "/On" to be checked

Return ONLY the JSON object, no additional text."""

        try:
            # If we have images, include them in the request
            if pdf_images:
                messages = [{
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }]
                
                # Add up to 3 images for context
                for i, img in enumerate(pdf_images[:3]):
                    img_base64 = self.image_to_base64(img)
                    messages[0]["content"].append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": img_base64
                        }
                    })
                    messages[0]["content"].append({
                        "type": "text",
                        "text": f"This is page {i+1} of the PDF form."
                    })
            else:
                messages = [{"role": "user", "content": prompt}]
            
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=2000,
                messages=messages
            )
            
            # Parse the response
            response_text = response.content[0].text
            
            # Try to extract JSON from the response
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text.strip()
            
            result = json.loads(json_str)
            return result
            
        except Exception as e:
            print(f"Error calling LLM: {e}")
            print(f"Response: {response_text if 'response_text' in locals() else 'No response'}")
            return {"field_mappings": []}
    
    def fill_fillable_pdf(
        self, 
        input_pdf: str, 
        output_pdf: str, 
        field_values: Dict[str, Any]
    ):
        """Fill a PDF with fillable form fields."""
        print(f"Filling PDF with {len(field_values)} fields...")
        
        reader = PdfReader(input_pdf)
        writer = PdfWriter()
        
        # Copy all pages
        for page in reader.pages:
            writer.add_page(page)
        
        # Fill form fields
        if writer.get_fields():
            for field_id, value in field_values.items():
                try:
                    writer.update_page_form_field_values(
                        writer.pages[0],  # This updates all pages
                        {field_id: value}
                    )
                except Exception as e:
                    print(f"Warning: Could not fill field '{field_id}': {e}")
        
        # Write output
        with open(output_pdf, "wb") as output_file:
            writer.write(output_file)
        
        print(f"Successfully created: {output_pdf}")
    
    def process_pdf(
        self, 
        input_pdf: str, 
        output_pdf: str, 
        user_data: Dict[str, Any]
    ):
        """Main method to process a PDF form."""
        
        print(f"Processing PDF: {input_pdf}")
        print(f"User data: {json.dumps(user_data, indent=2)}")
        
        # Check if PDF is fillable
        is_fillable = self.check_if_fillable(input_pdf)
        print(f"PDF is {'fillable' if is_fillable else 'NOT fillable'}")
        
        if is_fillable:
            # Extract fillable fields
            fields = self.extract_fillable_fields(input_pdf)
            print(f"Found {len(fields)} form fields")
            
            # Convert PDF to images for visual context
            images = self.convert_pdf_to_images(input_pdf)
            
            # Use LLM to map data to fields
            mapping_result = self.map_data_to_fields_llm(fields, user_data, images)
            
            # Create field_values dictionary
            field_values = {}
            for mapping in mapping_result.get("field_mappings", []):
                field_id = mapping["field_id"]
                value = mapping["value"]
                field_values[field_id] = value
                print(f"  {field_id} = {value} ({mapping.get('reasoning', 'N/A')})")
            
            # Fill the PDF
            self.fill_fillable_pdf(input_pdf, output_pdf, field_values)
            
        else:
            print("\nThis PDF doesn't have fillable fields.")
            print("You'll need to use the annotation-based approach described in")
            print("the PDF skill FORMS.md file for non-fillable PDFs.")
            print("\nThe LLM can help identify where fields should go, but you'll need")
            print("to manually create the fields.json file with bounding boxes.")
            
            # Still provide the visual analysis
            images = self.convert_pdf_to_images(input_pdf)
            print(f"\nConverted PDF to {len(images)} images for analysis.")


def main():
    parser = argparse.ArgumentParser(
        description="Fill PDF forms intelligently using an LLM"
    )
    parser.add_argument("input_pdf", help="Path to input PDF file")
    parser.add_argument("output_pdf", help="Path to output PDF file")
    parser.add_argument(
        "--data", 
        help="JSON string with data to fill (e.g., '{\"name\": \"John\"}')"
    )
    parser.add_argument(
        "--data-file", 
        help="Path to JSON file with data to fill"
    )
    parser.add_argument(
        "--api-key",
        help="Anthropic API key (or set ANTHROPIC_API_KEY env variable)"
    )
    
    args = parser.parse_args()
    
    # Get user data
    if args.data:
        user_data = json.loads(args.data)
    elif args.data_file:
        with open(args.data_file, 'r') as f:
            user_data = json.load(f)
    else:
        print("Error: Must provide either --data or --data-file")
        sys.exit(1)
    
    # Create filler and process
    filler = PDFFormFiller(api_key=args.api_key)
    filler.process_pdf(args.input_pdf, args.output_pdf, user_data)


if __name__ == "__main__":
    main()
