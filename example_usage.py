#!/usr/bin/env python3
"""
Example script showing how to use the PDFFormFieldGenerator class programmatically.
"""

from pdf_form_field_generator import PDFFormFieldGenerator
import json

def example_1_basic_usage():
    """Basic example - add simple text fields to a PDF."""
    print("=" * 60)
    print("EXAMPLE 1: Basic Form Field Creation")
    print("=" * 60)

    # Initialize the generator (will use ANTHROPIC_API_KEY from environment)
    generator = PDFFormFieldGenerator()

    # Define fields to add
    fields = [
        {
            "name": "first_name",
            "type": "text",
            "page": 0,
            "rect": [100, 700, 300, 720],  # [x1, y1, x2, y2]
            "font_size": 12
        },
        {
            "name": "last_name",
            "type": "text",
            "page": 0,
            "rect": [100, 670, 300, 690],
            "font_size": 12
        },
        {
            "name": "email",
            "type": "text",
            "page": 0,
            "rect": [100, 640, 350, 660],
            "font_size": 12
        }
    ]

    # Add fields to the PDF
    generator.add_fields_to_pdf(
        input_pdf="blank_form.pdf",
        output_pdf="form_with_fields.pdf",
        fields=fields
    )
    print("\n✅ Form fields added successfully!\n")


def example_2_multiple_field_types():
    """Example with multiple field types including checkboxes and dropdowns."""
    print("=" * 60)
    print("EXAMPLE 2: Multiple Field Types")
    print("=" * 60)

    generator = PDFFormFieldGenerator()

    fields = [
        # Text fields
        {
            "name": "full_name",
            "type": "text",
            "page": 0,
            "rect": [100, 700, 400, 720],
            "font_size": 14
        },
        {
            "name": "address",
            "type": "text",
            "page": 0,
            "rect": [100, 660, 450, 680],
            "font_size": 12
        },

        # Checkboxes
        {
            "name": "agree_terms",
            "type": "checkbox",
            "page": 0,
            "rect": [100, 620, 115, 635],
            "checked": False
        },
        {
            "name": "subscribe_newsletter",
            "type": "checkbox",
            "page": 0,
            "rect": [100, 590, 115, 605],
            "checked": False
        },

        # Dropdown
        {
            "name": "country",
            "type": "dropdown",
            "page": 0,
            "rect": [100, 540, 300, 560],
            "options": ["USA", "Canada", "UK", "Australia", "Other"],
            "default_value": ""
        }
    ]

    generator.add_fields_to_pdf(
        input_pdf="application.pdf",
        output_pdf="application_with_fields.pdf",
        fields=fields
    )
    print("\n✅ Multiple field types added successfully!\n")


def example_3_from_json_file():
    """Example loading field specifications from a JSON file."""
    print("=" * 60)
    print("EXAMPLE 3: Loading Fields from JSON File")
    print("=" * 60)

    generator = PDFFormFieldGenerator()

    # Example JSON structure to save as fields.json:
    fields_spec = [
        {
            "name": "employee_name",
            "type": "text",
            "page": 0,
            "rect": [150, 750, 450, 770]
        },
        {
            "name": "employee_id",
            "type": "text",
            "page": 0,
            "rect": [150, 720, 350, 740]
        },
        {
            "name": "department",
            "type": "dropdown",
            "page": 0,
            "rect": [150, 690, 350, 710],
            "options": ["Engineering", "Sales", "Marketing", "HR", "Finance"]
        },
        {
            "name": "full_time",
            "type": "checkbox",
            "page": 0,
            "rect": [150, 650, 165, 665]
        }
    ]

    # Save to JSON file
    with open("fields.json", "w") as f:
        json.dump(fields_spec, f, indent=2)

    print("Created fields.json with field specifications")

    # Load from JSON file
    with open("fields.json", "r") as f:
        fields = json.load(f)

    print(f"Loaded {len(fields)} field specifications")

    generator.add_fields_to_pdf(
        input_pdf="employee_form.pdf",
        output_pdf="employee_form_with_fields.pdf",
        fields=fields
    )
    print("\n✅ Fields added from JSON file!\n")


def example_4_auto_suggest_fields():
    """Example using LLM to automatically suggest field placements."""
    print("=" * 60)
    print("EXAMPLE 4: Auto-Suggest Fields with LLM")
    print("=" * 60)

    generator = PDFFormFieldGenerator()

    # Use LLM to analyze the PDF and suggest field placements
    generator.process_pdf_with_suggestions(
        input_pdf="blank_application.pdf",
        output_pdf="application_with_auto_fields.pdf",
        context="This is a job application form. Please identify all areas where applicants should enter information.",
        save_suggestions="suggested_fields.json"
    )

    print("\n✅ Fields automatically suggested and added!\n")
    print("💡 Check suggested_fields.json to see what the LLM suggested")


def example_5_multi_page_form():
    """Example adding fields across multiple pages."""
    print("=" * 60)
    print("EXAMPLE 5: Multi-Page Form Fields")
    print("=" * 60)

    generator = PDFFormFieldGenerator()

    fields = [
        # Page 1 - Personal Information
        {
            "name": "first_name",
            "type": "text",
            "page": 0,  # First page (0-indexed)
            "rect": [100, 700, 300, 720]
        },
        {
            "name": "last_name",
            "type": "text",
            "page": 0,
            "rect": [100, 670, 300, 690]
        },

        # Page 2 - Employment Information
        {
            "name": "employer",
            "type": "text",
            "page": 1,  # Second page
            "rect": [100, 700, 400, 720]
        },
        {
            "name": "position",
            "type": "text",
            "page": 1,
            "rect": [100, 670, 400, 690]
        },

        # Page 3 - Agreement
        {
            "name": "signature",
            "type": "text",
            "page": 2,  # Third page
            "rect": [100, 200, 350, 220]
        },
        {
            "name": "agree",
            "type": "checkbox",
            "page": 2,
            "rect": [100, 160, 115, 175]
        }
    ]

    generator.add_fields_to_pdf(
        input_pdf="multi_page_form.pdf",
        output_pdf="multi_page_form_with_fields.pdf",
        fields=fields
    )
    print("\n✅ Fields added across multiple pages!\n")


def example_6_batch_processing():
    """Example processing multiple PDFs with different field sets."""
    print("=" * 60)
    print("EXAMPLE 6: Batch Processing Multiple PDFs")
    print("=" * 60)

    generator = PDFFormFieldGenerator()

    # Define different field sets for different forms
    form_configs = [
        {
            "input": "contact_form.pdf",
            "output": "contact_form_with_fields.pdf",
            "fields": [
                {"name": "name", "type": "text", "page": 0, "rect": [100, 700, 400, 720]},
                {"name": "email", "type": "text", "page": 0, "rect": [100, 670, 400, 690]},
                {"name": "message", "type": "text", "page": 0, "rect": [100, 500, 450, 640]}
            ]
        },
        {
            "input": "feedback_form.pdf",
            "output": "feedback_form_with_fields.pdf",
            "fields": [
                {"name": "rating", "type": "dropdown", "page": 0, "rect": [100, 700, 300, 720],
                 "options": ["Excellent", "Good", "Fair", "Poor"]},
                {"name": "comments", "type": "text", "page": 0, "rect": [100, 500, 450, 680]},
                {"name": "recommend", "type": "checkbox", "page": 0, "rect": [100, 460, 115, 475]}
            ]
        }
    ]

    for config in form_configs:
        try:
            print(f"\nProcessing: {config['input']}")
            generator.add_fields_to_pdf(
                input_pdf=config['input'],
                output_pdf=config['output'],
                fields=config['fields']
            )
            print(f"✅ Created: {config['output']}")
        except FileNotFoundError:
            print(f"⚠️  Skipped: {config['input']} (file not found)")
        except Exception as e:
            print(f"❌ Error processing {config['input']}: {e}")

    print("\n✅ Batch processing complete!\n")


def example_7_signature_and_date_fields():
    """Example adding signature and date fields."""
    print("=" * 60)
    print("EXAMPLE 7: Signature and Date Fields")
    print("=" * 60)

    generator = PDFFormFieldGenerator()

    fields = [
        # Main content fields
        {
            "name": "party_a_name",
            "type": "text",
            "page": 0,
            "rect": [150, 650, 400, 670]
        },
        {
            "name": "party_b_name",
            "type": "text",
            "page": 0,
            "rect": [150, 620, 400, 640]
        },

        # Signature section (bottom of page)
        {
            "name": "party_a_signature",
            "type": "text",
            "page": 0,
            "rect": [100, 150, 300, 170],
            "font_size": 14
        },
        {
            "name": "party_a_date",
            "type": "text",
            "page": 0,
            "rect": [320, 150, 450, 170]
        },
        {
            "name": "party_b_signature",
            "type": "text",
            "page": 0,
            "rect": [100, 100, 300, 120],
            "font_size": 14
        },
        {
            "name": "party_b_date",
            "type": "text",
            "page": 0,
            "rect": [320, 100, 450, 120]
        }
    ]

    generator.add_fields_to_pdf(
        input_pdf="contract.pdf",
        output_pdf="contract_with_fields.pdf",
        fields=fields
    )
    print("\n✅ Contract form with signature fields created!\n")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("PDF FORM FIELD GENERATOR - USAGE EXAMPLES")
    print("=" * 60 + "\n")

    examples = [
        ("Basic Usage", example_1_basic_usage),
        ("Multiple Field Types", example_2_multiple_field_types),
        ("From JSON File", example_3_from_json_file),
        ("Auto-Suggest with LLM", example_4_auto_suggest_fields),
        ("Multi-Page Form", example_5_multi_page_form),
        ("Batch Processing", example_6_batch_processing),
        ("Signature & Date Fields", example_7_signature_and_date_fields),
    ]

    print("Available examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")

    print("\nTo run a specific example, modify this script or run:")
    print("  python example_usage.py\n")

    # Uncomment the example you want to run:
    # example_1_basic_usage()
    # example_2_multiple_field_types()
    # example_3_from_json_file()
    # example_4_auto_suggest_fields()
    # example_5_multi_page_form()
    # example_6_batch_processing()
    # example_7_signature_and_date_fields()

    print("💡 Tip: Uncomment the example you want to run in the main() function")
    print()


if __name__ == "__main__":
    main()
