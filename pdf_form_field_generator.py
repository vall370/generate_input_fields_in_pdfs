#!/usr/bin/env python3
"""
PDF Form Field Generator with LLM Intelligence

This script creates form fields in PDF documents. It can intelligently analyze
PDF content and suggest where to place form fields using LLM assistance.

Requirements:
    pip install pypdf anthropic pillow pdf2image --break-system-packages

Usage:
    python pdf_form_field_generator.py <input_pdf> <output_pdf> --fields-file fields.json

    Or define fields programmatically:
    from pdf_form_field_generator import PDFFormFieldGenerator
    generator = PDFFormFieldGenerator()
    fields = [
        {"name": "first_name", "type": "text", "page": 0, "rect": [100, 700, 300, 720]},
        {"name": "agree", "type": "checkbox", "page": 0, "rect": [100, 650, 120, 670]}
    ]
    generator.add_fields_to_pdf("input.pdf", "output.pdf", fields)
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import base64
from io import BytesIO

try:
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import (
        NameObject, DictionaryObject, ArrayObject,
        NumberObject, TextStringObject, IndirectObject
    )
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


class PDFFormFieldGenerator:
    """Main class for adding form fields to PDF documents."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize with Anthropic API key."""
        self.client = Anthropic(api_key=api_key) if api_key else Anthropic()

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

    def suggest_form_fields_llm(
        self,
        pdf_path: str,
        context: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Use LLM to analyze PDF and suggest where form fields should be placed."""

        print("Using LLM to analyze PDF and suggest form fields...")

        # Convert PDF to images
        images = self.convert_pdf_to_images(pdf_path)

        # Get PDF dimensions for coordinate reference
        reader = PdfReader(pdf_path)
        page_height = float(reader.pages[0].mediabox.height)
        page_width = float(reader.pages[0].mediabox.width)

        # Prepare the prompt
        prompt = f"""You are a PDF form field placement assistant. Analyze the provided PDF pages and suggest where interactive form fields should be placed.

PDF Page Dimensions:
- Width: {page_width} points
- Height: {page_height} points

{f"Context: {context}" if context else ""}

Instructions:
1. Analyze the PDF images to identify where form fields should be placed
2. Look for labels, underlines, checkboxes, or areas that suggest user input
3. For each field you identify, provide:
   - A descriptive field name (e.g., "first_name", "email", "signature")
   - The field type: "text", "checkbox", "radio", or "dropdown"
   - The page number (0-indexed)
   - Estimated coordinates as [x1, y1, x2, y2] where:
     * (x1, y1) is the bottom-left corner
     * (x2, y2) is the top-right corner
     * Coordinates are in PDF points (72 points = 1 inch)
     * Y-axis starts from bottom of page

4. Return your response as a JSON object with this structure:

{{
  "fields": [
    {{
      "name": "field_name",
      "type": "text",
      "page": 0,
      "rect": [x1, y1, x2, y2],
      "description": "what this field is for"
    }}
  ]
}}

Common field dimensions:
- Text fields: typically 150-300 points wide, 15-20 points tall
- Checkboxes: typically 12-15 points square
- Signature fields: typically 200-300 points wide, 40-60 points tall

Return ONLY the JSON object, no additional text."""

        try:
            messages = [{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }]

            # Add up to 5 images for context
            for i, img in enumerate(images[:5]):
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
                    "text": f"This is page {i+1} of the PDF (page index {i})."
                })

            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=4000,
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
            return result.get("fields", [])

        except Exception as e:
            print(f"Error calling LLM: {e}")
            print(f"Response: {response_text if 'response_text' in locals() else 'No response'}")
            return []

    def create_text_field(
        self,
        writer: PdfWriter,
        page_num: int,
        field_name: str,
        rect: List[float],
        default_value: str = "",
        font_size: int = 12
    ) -> DictionaryObject:
        """Create a text field annotation."""

        page = writer.pages[page_num]

        # Create the field annotation
        field = DictionaryObject()
        field.update({
            NameObject("/FT"): NameObject("/Tx"),  # Text field
            NameObject("/T"): TextStringObject(field_name),  # Field name
            NameObject("/V"): TextStringObject(default_value),  # Default value
            NameObject("/Rect"): ArrayObject([
                NumberObject(rect[0]),
                NumberObject(rect[1]),
                NumberObject(rect[2]),
                NumberObject(rect[3])
            ]),
            NameObject("/F"): NumberObject(4),  # Print flag
            NameObject("/Ff"): NumberObject(0),  # Field flags
            NameObject("/P"): page.indirect_reference,  # Parent page
            NameObject("/Subtype"): NameObject("/Widget"),
            NameObject("/Type"): NameObject("/Annot"),
            NameObject("/DA"): TextStringObject(f"/Helv {font_size} Tf 0 g"),  # Default appearance
        })

        return field

    def create_checkbox_field(
        self,
        writer: PdfWriter,
        page_num: int,
        field_name: str,
        rect: List[float],
        checked: bool = False
    ) -> DictionaryObject:
        """Create a checkbox field annotation."""

        page = writer.pages[page_num]

        # Create the field annotation
        field = DictionaryObject()
        field.update({
            NameObject("/FT"): NameObject("/Btn"),  # Button field
            NameObject("/T"): TextStringObject(field_name),  # Field name
            NameObject("/V"): NameObject("/Yes" if checked else "/Off"),  # Default value
            NameObject("/Rect"): ArrayObject([
                NumberObject(rect[0]),
                NumberObject(rect[1]),
                NumberObject(rect[2]),
                NumberObject(rect[3])
            ]),
            NameObject("/F"): NumberObject(4),  # Print flag
            NameObject("/P"): page.indirect_reference,  # Parent page
            NameObject("/Subtype"): NameObject("/Widget"),
            NameObject("/Type"): NameObject("/Annot"),
            NameObject("/AS"): NameObject("/Yes" if checked else "/Off"),  # Appearance state
        })

        return field

    def create_dropdown_field(
        self,
        writer: PdfWriter,
        page_num: int,
        field_name: str,
        rect: List[float],
        options: List[str],
        default_value: str = ""
    ) -> DictionaryObject:
        """Create a dropdown/choice field annotation."""

        page = writer.pages[page_num]

        # Create options array
        options_array = ArrayObject([TextStringObject(opt) for opt in options])

        # Create the field annotation
        field = DictionaryObject()
        field.update({
            NameObject("/FT"): NameObject("/Ch"),  # Choice field
            NameObject("/T"): TextStringObject(field_name),  # Field name
            NameObject("/V"): TextStringObject(default_value),  # Default value
            NameObject("/Opt"): options_array,  # Options
            NameObject("/Rect"): ArrayObject([
                NumberObject(rect[0]),
                NumberObject(rect[1]),
                NumberObject(rect[2]),
                NumberObject(rect[3])
            ]),
            NameObject("/F"): NumberObject(4),  # Print flag
            NameObject("/Ff"): NumberObject(131072),  # Combo box flag
            NameObject("/P"): page.indirect_reference,  # Parent page
            NameObject("/Subtype"): NameObject("/Widget"),
            NameObject("/Type"): NameObject("/Annot"),
        })

        return field

    def add_fields_to_pdf(
        self,
        input_pdf: str,
        output_pdf: str,
        fields: List[Dict[str, Any]]
    ):
        """Add form fields to a PDF document."""

        print(f"Adding {len(fields)} form fields to PDF...")

        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        # Copy all pages
        for page in reader.pages:
            writer.add_page(page)

        # Create fields list
        form_fields = []

        for field_spec in fields:
            field_name = field_spec["name"]
            field_type = field_spec["type"]
            page_num = field_spec.get("page", 0)
            rect = field_spec["rect"]

            print(f"  Adding {field_type} field '{field_name}' on page {page_num + 1}")

            # Create the appropriate field type
            if field_type == "text":
                field = self.create_text_field(
                    writer, page_num, field_name, rect,
                    default_value=field_spec.get("default_value", ""),
                    font_size=field_spec.get("font_size", 12)
                )
            elif field_type == "checkbox":
                field = self.create_checkbox_field(
                    writer, page_num, field_name, rect,
                    checked=field_spec.get("checked", False)
                )
            elif field_type == "dropdown":
                field = self.create_dropdown_field(
                    writer, page_num, field_name, rect,
                    options=field_spec.get("options", []),
                    default_value=field_spec.get("default_value", "")
                )
            else:
                print(f"  Warning: Unsupported field type '{field_type}', skipping")
                continue

            # Add field to the page's annotations
            page = writer.pages[page_num]

            # Add the field as an indirect object
            field_ref = writer._add_object(field)

            # Add to page annotations
            if "/Annots" in page:
                page[NameObject("/Annots")].append(field_ref)
            else:
                page[NameObject("/Annots")] = ArrayObject([field_ref])

            form_fields.append(field_ref)

        # Create the AcroForm dictionary
        if form_fields:
            acro_form = DictionaryObject()
            acro_form.update({
                NameObject("/Fields"): ArrayObject(form_fields),
                NameObject("/NeedAppearances"): NameObject("/true"),
            })

            writer._root_object.update({
                NameObject("/AcroForm"): acro_form
            })

        # Write output
        with open(output_pdf, "wb") as output_file:
            writer.write(output_file)

        print(f"Successfully created: {output_pdf}")
        print(f"Added {len(form_fields)} form fields")

    def process_pdf_with_suggestions(
        self,
        input_pdf: str,
        output_pdf: str,
        context: Optional[str] = None,
        save_suggestions: Optional[str] = None
    ):
        """Process a PDF by analyzing it and adding suggested form fields."""

        print(f"Processing PDF: {input_pdf}")

        # Use LLM to suggest form fields
        suggested_fields = self.suggest_form_fields_llm(input_pdf, context)

        if not suggested_fields:
            print("No fields were suggested by the LLM.")
            return

        print(f"\nLLM suggested {len(suggested_fields)} form fields:")
        for field in suggested_fields:
            print(f"  - {field['name']} ({field['type']}) on page {field['page'] + 1}")
            if 'description' in field:
                print(f"    Description: {field['description']}")

        # Optionally save suggestions to file
        if save_suggestions:
            with open(save_suggestions, 'w') as f:
                json.dump(suggested_fields, f, indent=2)
            print(f"\nSaved field suggestions to: {save_suggestions}")

        # Add the fields to the PDF
        self.add_fields_to_pdf(input_pdf, output_pdf, suggested_fields)


def main():
    parser = argparse.ArgumentParser(
        description="Add form fields to PDF documents using LLM intelligence"
    )
    parser.add_argument("input_pdf", help="Path to input PDF file")
    parser.add_argument("output_pdf", help="Path to output PDF file")
    parser.add_argument(
        "--fields-file",
        help="Path to JSON file with field specifications"
    )
    parser.add_argument(
        "--auto-suggest",
        action="store_true",
        help="Use LLM to automatically suggest field placements"
    )
    parser.add_argument(
        "--context",
        help="Additional context for LLM field suggestions"
    )
    parser.add_argument(
        "--save-suggestions",
        help="Save LLM field suggestions to this JSON file"
    )
    parser.add_argument(
        "--api-key",
        help="Anthropic API key (or set ANTHROPIC_API_KEY env variable)"
    )

    args = parser.parse_args()

    # Create generator
    generator = PDFFormFieldGenerator(api_key=args.api_key)

    if args.auto_suggest:
        # Use LLM to suggest fields
        generator.process_pdf_with_suggestions(
            args.input_pdf,
            args.output_pdf,
            context=args.context,
            save_suggestions=args.save_suggestions
        )
    elif args.fields_file:
        # Load fields from file
        with open(args.fields_file, 'r') as f:
            fields = json.load(f)

        generator.add_fields_to_pdf(args.input_pdf, args.output_pdf, fields)
    else:
        print("Error: Must provide either --fields-file or --auto-suggest")
        sys.exit(1)


if __name__ == "__main__":
    main()
