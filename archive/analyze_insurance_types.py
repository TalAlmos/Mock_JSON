#!/usr/bin/env python3
"""
Insurance Type Analysis Script

This script analyzes all example files to extract:
1. All available insurance types
2. Required fields for each insurance type
3. Field types and structures
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Set
from collections import defaultdict

def analyze_insurance_types():
    """Analyze all example files to extract insurance types and their structures."""
    examples_path = Path("D:/Mock_JSON/data/examples")
    
    # Track insurance types and their fields
    insurance_types = set()
    field_structures = defaultdict(lambda: defaultdict(set))
    field_types = defaultdict(lambda: defaultdict(set))
    
    # Process all JSON files
    for example_file in examples_path.glob("*.json"):
        try:
            with open(example_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different response structures
            response = data.get('response', {})
            
            # Case 1: Response is a list with insurance type objects
            if isinstance(response, list):
                for item in response:
                    if isinstance(item, dict) and 'id' in item:
                        insurance_type = item['id']
                        insurance_types.add(insurance_type)
                        
                        # Analyze the data array
                        data_array = item.get('data', [])
                        if isinstance(data_array, list):
                            for data_item in data_array:
                                if isinstance(data_item, dict):
                                    analyze_fields(data_item, insurance_type, field_structures, field_types)
            
            # Case 2: Response is a direct object (for other entity types)
            elif isinstance(response, dict):
                # This might be for savings/money entities
                entity = data.get('entity', 'Unknown')
                if entity not in ['vehicleUnitedEntity']:
                    analyze_fields(response, entity, field_structures, field_types)
                    
        except Exception as e:
            print(f"⚠️  Warning: Could not process {example_file.name}: {e}")
    
    return insurance_types, field_structures, field_types

def analyze_fields(obj: Dict[str, Any], insurance_type: str, field_structures: Dict, field_types: Dict):
    """Recursively analyze fields in an object."""
    for field_name, field_value in obj.items():
        # Track field presence
        field_structures[insurance_type][field_name].add(type(field_value).__name__)
        
        # Track field types
        if isinstance(field_value, dict):
            field_types[insurance_type][field_name].add('object')
            # Recursively analyze nested objects
            analyze_fields(field_value, insurance_type, field_structures, field_types)
        elif isinstance(field_value, list):
            field_types[insurance_type][field_name].add('array')
            # Analyze array items
            for item in field_value:
                if isinstance(item, dict):
                    analyze_fields(item, insurance_type, field_structures, field_types)
        else:
            field_types[insurance_type][field_name].add(type(field_value).__name__)

def print_analysis(insurance_types: Set[str], field_structures: Dict, field_types: Dict):
    """Print the analysis results."""
    print("=" * 80)
    print("INSURANCE TYPE ANALYSIS RESULTS")
    print("=" * 80)
    
    print(f"\n📋 Found {len(insurance_types)} insurance types:")
    for i, insurance_type in enumerate(sorted(insurance_types), 1):
        print(f"  {i}. {insurance_type}")
    
    print("\n" + "=" * 80)
    print("DETAILED FIELD ANALYSIS BY INSURANCE TYPE")
    print("=" * 80)
    
    for insurance_type in sorted(insurance_types):
        print(f"\n🔍 {insurance_type.upper()} INSURANCE:")
        print("-" * 50)
        
        if insurance_type in field_structures:
            fields = field_structures[insurance_type]
            print(f"📊 Total fields found: {len(fields)}")
            
            # Group fields by type
            field_groups = defaultdict(list)
            for field_name, types in fields.items():
                type_str = ', '.join(sorted(types))
                field_groups[type_str].append(field_name)
            
            for field_type, field_names in field_groups.items():
                print(f"\n  {field_type}:")
                for field_name in sorted(field_names):
                    print(f"    - {field_name}")
        else:
            print("  No field data found")
    
    print("\n" + "=" * 80)
    print("FIELD TYPE SUMMARY")
    print("=" * 80)
    
    # Create a summary of all unique fields across all insurance types
    all_fields = set()
    for fields in field_structures.values():
        all_fields.update(fields.keys())
    
    print(f"\n📋 Total unique fields across all insurance types: {len(all_fields)}")
    print("\nField presence by insurance type:")
    
    for field_name in sorted(all_fields):
        present_in = []
        for insurance_type in sorted(insurance_types):
            if field_name in field_structures.get(insurance_type, {}):
                present_in.append(insurance_type)
        
        if present_in:
            print(f"  {field_name}: {', '.join(present_in)}")

def main():
    """Main function to run the analysis."""
    print("🔍 Analyzing insurance types and field structures...")
    
    insurance_types, field_structures, field_types = analyze_insurance_types()
    
    print_analysis(insurance_types, field_structures, field_types)
    
    # Save detailed results to JSON for further analysis
    results = {
        'insurance_types': sorted(list(insurance_types)),
        'field_structures': {k: {fk: list(fv) for fk, fv in v.items()} for k, v in field_structures.items()},
        'field_types': {k: {fk: list(fv) for fk, fv in v.items()} for k, v in field_types.items()}
    }
    
    with open('insurance_analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Detailed results saved to: insurance_analysis_results.json")

if __name__ == "__main__":
    main() 