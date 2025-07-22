#!/usr/bin/env python3
"""
Example usage of the Mock Data Generator with preserve functionality

This script demonstrates how to:
1. Add fields to the preserve list
2. Remove fields from the preserve list
3. List current preserve fields
4. Generate mock data with custom preserve settings
"""

from mock_data_generator import MockDataGenerator

def main():
    """Example usage of the Mock Data Generator with preserve functionality."""
    
    # Create the generator
    generator = MockDataGenerator()
    
    print("🔧 Customizing Preserve Fields")
    print("=" * 40)
    
    # Show current preserve fields
    generator.list_preserve_fields()
    
    # Example: Add a custom field to preserve
    print("\n➕ Adding custom field to preserve list...")
    generator.add_preserve_field("customField")
    
    # Example: Remove a field from preserve list
    print("\n➖ Removing field from preserve list...")
    generator.remove_preserve_field("totalPayments")
    
    # Show updated preserve fields
    print("\n📋 Updated preserve fields:")
    generator.list_preserve_fields()
    
    # Example: Add multiple fields at once
    print("\n➕ Adding multiple fields to preserve list...")
    custom_fields = ["policyNumber", "customerId", "branchCode"]
    for field in custom_fields:
        generator.add_preserve_field(field)
    
    # Show final preserve fields
    print("\n📋 Final preserve fields:")
    generator.list_preserve_fields()
    
    print("\n🚀 Now you can run the generator with custom preserve settings!")
    print("Run: python mock_data_generator.py")

if __name__ == "__main__":
    main() 