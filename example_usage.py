#!/usr/bin/env python3
"""
Example script showing how to use the PDFFormFiller class programmatically.
"""

from pdf_form_filler import PDFFormFiller
import json

def example_1_basic_usage():
    """Basic example - fill a simple form."""
    print("=" * 60)
    print("EXAMPLE 1: Basic Form Filling")
    print("=" * 60)
    
    # Initialize the filler (will use ANTHROPIC_API_KEY from environment)
    filler = PDFFormFiller()
    
    # Your data to fill
    user_data = {
        "first_name": "Alice",
        "last_name": "Johnson",
        "email": "alice.johnson@email.com",
        "phone": "(555) 123-4567"
    }
    
    # Process the PDF
    filler.process_pdf(
        input_pdf="job_application.pdf",
        output_pdf="job_application_filled.pdf",
        user_data=user_data
    )
    print("\n✅ Form filled successfully!\n")


def example_2_with_api_key():
    """Example with explicit API key."""
    print("=" * 60)
    print("EXAMPLE 2: Using Explicit API Key")
    print("=" * 60)
    
    # Initialize with explicit API key
    filler = PDFFormFiller(api_key="your-api-key-here")
    
    user_data = {
        "name": "Bob Smith",
        "company": "Tech Innovations Inc",
        "position": "Senior Developer"
    }
    
    filler.process_pdf(
        input_pdf="contract.pdf",
        output_pdf="contract_filled.pdf",
        user_data=user_data
    )
    print("\n✅ Contract filled successfully!\n")


def example_3_check_fillable():
    """Example checking if a PDF is fillable."""
    print("=" * 60)
    print("EXAMPLE 3: Checking PDF Fillability")
    print("=" * 60)
    
    filler = PDFFormFiller()
    
    pdf_files = ["form1.pdf", "form2.pdf", "scanned_form.pdf"]
    
    for pdf_file in pdf_files:
        try:
            is_fillable = filler.check_if_fillable(pdf_file)
            status = "✅ Fillable" if is_fillable else "❌ Not fillable"
            print(f"{pdf_file}: {status}")
        except FileNotFoundError:
            print(f"{pdf_file}: ⚠️  File not found")
    
    print()


def example_4_complex_form():
    """Example with a complex form including checkboxes and dates."""
    print("=" * 60)
    print("EXAMPLE 4: Complex Form with Multiple Field Types")
    print("=" * 60)
    
    filler = PDFFormFiller()
    
    user_data = {
        # Personal information
        "full_name": "Carol Martinez",
        "date_of_birth": "1985-03-20",
        "ssn": "123-45-6789",
        "email": "carol.martinez@example.com",
        
        # Address
        "street": "456 Oak Avenue",
        "city": "Los Angeles",
        "state": "CA",
        "zip": "90001",
        
        # Checkboxes (use boolean values)
        "is_us_citizen": True,
        "has_criminal_record": False,
        "agrees_to_background_check": True,
        
        # Employment
        "current_employer": "Global Solutions LLC",
        "years_employed": 5,
        "monthly_income": 6500,
        
        # Additional info
        "references": "Available upon request",
        "signature": "Carol Martinez",
        "date_signed": "2025-10-25"
    }
    
    filler.process_pdf(
        input_pdf="rental_application.pdf",
        output_pdf="rental_application_filled.pdf",
        user_data=user_data
    )
    print("\n✅ Rental application filled successfully!\n")


def example_5_batch_processing():
    """Example processing multiple forms with the same data."""
    print("=" * 60)
    print("EXAMPLE 5: Batch Processing Multiple Forms")
    print("=" * 60)
    
    filler = PDFFormFiller()
    
    # Common data for all forms
    common_data = {
        "name": "David Chen",
        "email": "david.chen@example.com",
        "phone": "555-0199",
        "company": "DataTech Solutions"
    }
    
    # List of forms to process
    forms = [
        ("vendor_form.pdf", "vendor_form_filled.pdf"),
        ("nda.pdf", "nda_filled.pdf"),
        ("service_agreement.pdf", "service_agreement_filled.pdf")
    ]
    
    for input_pdf, output_pdf in forms:
        try:
            print(f"\nProcessing: {input_pdf}")
            filler.process_pdf(input_pdf, output_pdf, common_data)
            print(f"✅ Created: {output_pdf}")
        except FileNotFoundError:
            print(f"⚠️  Skipped: {input_pdf} (file not found)")
        except Exception as e:
            print(f"❌ Error processing {input_pdf}: {e}")
    
    print("\n✅ Batch processing complete!\n")


def example_6_load_from_json():
    """Example loading data from a JSON file."""
    print("=" * 60)
    print("EXAMPLE 6: Loading Data from JSON File")
    print("=" * 60)
    
    filler = PDFFormFiller()
    
    # Load data from JSON file
    with open("example_data.json", "r") as f:
        user_data = json.load(f)
    
    print(f"Loaded data with {len(user_data)} fields")
    print(f"Keys: {', '.join(list(user_data.keys())[:5])}...")
    
    filler.process_pdf(
        input_pdf="comprehensive_form.pdf",
        output_pdf="comprehensive_form_filled.pdf",
        user_data=user_data
    )
    print("\n✅ Form filled from JSON data!\n")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("PDF FORM FILLER - USAGE EXAMPLES")
    print("=" * 60 + "\n")
    
    examples = [
        ("Basic Usage", example_1_basic_usage),
        ("With API Key", example_2_with_api_key),
        ("Check Fillability", example_3_check_fillable),
        ("Complex Form", example_4_complex_form),
        ("Batch Processing", example_5_batch_processing),
        ("Load from JSON", example_6_load_from_json),
    ]
    
    print("Available examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\nTo run a specific example, modify this script or run:")
    print("  python example_usage.py\n")
    
    # Uncomment the example you want to run:
    # example_1_basic_usage()
    # example_2_with_api_key()
    # example_3_check_fillable()
    # example_4_complex_form()
    # example_5_batch_processing()
    # example_6_load_from_json()
    
    print("💡 Tip: Uncomment the example you want to run in the main() function")
    print()


if __name__ == "__main__":
    main()
