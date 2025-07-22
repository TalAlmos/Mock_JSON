#!/usr/bin/env python3
"""
Mock Data Generator for Chatbot Testing

This script:
1. Loads a local Swagger (OpenAPI) JSON file
2. Loads local data example JSON files
3. Parses schema definitions
4. Generates mock data based on object definitions
5. Outputs anonymized mock JSON files for chatbot testing
"""

import json
import os
import random
import string
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from faker import Faker
import re
from datetime import datetime, timedelta

# Import the insurance schema system
from insurance_schemas import (
    get_schema, 
    get_available_insurance_types, 
    validate_insurance_data,
    FieldType
)

class MockDataGenerator:
    def __init__(self):
        """Initialize the mock data generator with Faker for anonymization."""
        self.faker = Faker(['he_IL'])  # Hebrew locale for Israeli data
        self.swagger_data = {}
        self.schemas = {}
        self.example_files = []
        
        # Hardcoded paths as requested
        self.swagger_path = Path("D:/Mock_JSON/data/swagger")
        self.examples_path = Path("D:/Mock_JSON/data/examples")
        self.output_path = Path("D:/Mock_JSON/data/mock_output")
        
        # Ensure output directory exists
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # Fields that should preserve original values (not anonymized)
        self.preserve_fields = {
            'status', 'message', 'transId', 'entity',  # API response metadata
            'id',  # Entity/API identifiers like "vehicleUnited", "life", "travel"
            'requiredRenewal', 'isExpired', 'isActive', 'isSmart', 'isKlasi', 'isRiziko', 'isCopyPolicyDoc', 'isPaila', 'isIndependent', 'isNew',  # Boolean flags
            'sign',  # Special characters like '%'
            'eSite',  # URLs that might be None
            'totalPayments',  # Empty strings that should remain empty
            'paymentNo',  # Fields that should remain null
            'yieldBeginningYear', 'lastDeposit', 'depositedThisYear', 'availableWithdraw', 'withdrawDate', 'yieldFromYearBeginningTotal',  # Nullable fields
            'fromDeposit', 'fromSaving', 'yieldUpdateDate', 'dailyYieldUpdateDate', 'hasProfitsShare', 'updateTo', 'dailyUpdateTo', 'tsuotPopup'  # More nullable fields
        }
    
    def load_swagger_file(self) -> bool:
        """Load the Swagger/OpenAPI JSON file and extract schemas."""
        try:
            swagger_files = list(self.swagger_path.glob("*.json"))
            if not swagger_files:
                print(f"❌ No JSON files found in {self.swagger_path}")
                return False
            
            swagger_file = swagger_files[0]  # Use the first JSON file found
            print(f"📄 Loading Swagger file: {swagger_file}")
            
            with open(swagger_file, 'r', encoding='utf-8') as f:
                self.swagger_data = json.load(f)
            
            # Extract schemas from components
            if 'components' in self.swagger_data and 'schemas' in self.swagger_data['components']:
                self.schemas = self.swagger_data['components']['schemas']
                print(f"✅ Loaded {len(self.schemas)} schema definitions")
                return True
            else:
                print("❌ No schemas found in Swagger file")
                return False
                
        except Exception as e:
            print(f"❌ Error loading Swagger file: {e}")
            return False
    
    def load_example_files(self) -> bool:
        """Load all example JSON files from the examples directory."""
        try:
            example_files = list(self.examples_path.glob("*.json"))
            if not example_files:
                print(f"❌ No JSON files found in {self.examples_path}")
                return False
            
            print(f"📄 Found {len(example_files)} example files")
            self.example_files = example_files
            return True
            
        except Exception as e:
            print(f"❌ Error loading example files: {e}")
            return False
    
    def filter_examples_by_insurance_type(self, insurance_type: str) -> List[Dict[str, Any]]:
        """Filter example data to only include those matching the specified insurance type."""
        if insurance_type == "all":
            # Return all example data
            all_examples = []
            for example_file in self.example_files:
                try:
                    with open(example_file, 'r', encoding='utf-8') as f:
                        example_data = json.load(f)
                    all_examples.append(example_data)
                except Exception as e:
                    print(f"⚠️  Warning: Could not process {example_file.name}: {e}")
            return all_examples
        
        filtered_examples = []
        
        for example_file in self.example_files:
            try:
                with open(example_file, 'r', encoding='utf-8') as f:
                    example_data = json.load(f)
                
                # Check if this example contains the specified insurance type
                response = example_data.get('response', {})
                if isinstance(response, list) and response:
                    # Filter the response to only include items with the specified insurance type
                    filtered_response = []
                    for item in response:
                        if isinstance(item, dict) and item.get('id') == insurance_type:
                            filtered_response.append(item)
                    
                    if filtered_response:
                        # Create a new example data with filtered response
                        filtered_example = example_data.copy()
                        filtered_example['response'] = filtered_response
                        filtered_examples.append(filtered_example)
                
            except Exception as e:
                print(f"⚠️  Warning: Could not process {example_file.name}: {e}")
        
        return filtered_examples
    
    def extract_schemas_from_examples(self, filtered_examples: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Extract schema structures from example data files."""
        schema_structures = {}
        
        # Use provided filtered examples or load all examples
        if filtered_examples is not None:
            examples_to_process = filtered_examples
        else:
            examples_to_process = []
            for example_file in self.example_files:
                try:
                    with open(example_file, 'r', encoding='utf-8') as f:
                        example_data = json.load(f)
                    examples_to_process.append(example_data)
                except Exception as e:
                    print(f"⚠️  Warning: Could not process {example_file.name}: {e}")
        
        # Group examples by entity to analyze multiple examples per entity
        entity_files = {}
        for example_data in examples_to_process:
            entity_name = example_data.get('entity', 'UnknownEntity')
            if entity_name not in entity_files:
                entity_files[entity_name] = []
            entity_files[entity_name].append(example_data)
        
        # Analyze each entity's structure using all available examples
        for entity_name, examples in entity_files.items():
            print(f"🔍 Analyzing structure for entity: {entity_name} ({len(examples)} examples)")
            schema_structures[entity_name] = self._analyze_entity_structure(examples)
        
        return schema_structures
    
    def _analyze_entity_structure(self, examples: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze structure across multiple examples for the same entity."""
        all_responses = []
        for example in examples:
            response = example.get('response', {})
            if response:
                all_responses.append(response)
        
        if not all_responses:
            return {"type": "object", "properties": {}}
        
        # Analyze the first response as base structure
        base_structure = self._analyze_structure(all_responses[0])
        
        # Enhance structure by looking at other examples
        for response in all_responses[1:]:
            enhanced_structure = self._merge_structures(base_structure, self._analyze_structure(response))
            base_structure = enhanced_structure
        
        # If the top-level structure is an array, pass all array items to the preserve logic
        if base_structure.get("type") == "array":
            # Flatten all items from all responses (which are lists)
            all_items = []
            for resp in all_responses:
                if isinstance(resp, list):
                    all_items.extend(resp)
            self._add_preserved_field_info(base_structure.get("items", {}), all_items)
        else:
            # Add preserved field information to the structure
            self._add_preserved_field_info(base_structure, all_responses)
        
        return base_structure
    
    def _add_preserved_field_info(self, structure: Dict[str, Any], examples: List[Dict[str, Any]]) -> None:
        """Add information about which fields should preserve their original values."""
        if structure.get("type") == "object":
            properties = structure.get("properties", {})
            for field_name, field_structure in properties.items():
                if field_name in self.preserve_fields:
                    # Mark this field as preserved
                    field_structure["preserve_original"] = True
                    # Store the original values from examples
                    original_values = self._extract_original_values(field_name, examples)
                    if original_values:
                        field_structure["original_values"] = original_values
                        print(f"🔍 Preserving field '{field_name}' with values: {original_values}")
                
                # Recursively process nested objects
                if field_structure.get("type") == "object":
                    nested_examples = [self._extract_nested_value(example, field_name) for example in examples]
                    nested_examples = [ex for ex in nested_examples if ex is not None]
                    if nested_examples:
                        self._add_preserved_field_info(field_structure, nested_examples)
                
                # Recursively process arrays
                elif field_structure.get("type") == "array":
                    array_examples = []
                    for example in examples:
                        array_value = self._extract_nested_value(example, field_name)
                        if isinstance(array_value, list):
                            array_examples.extend(array_value)
                    if array_examples:
                        # Process the array items structure
                        items_structure = field_structure.get("items", {})
                        self._add_preserved_field_info(items_structure, array_examples)
        
        elif structure.get("type") == "array":
            # Handle direct array structures (like the response array)
            if examples:
                # Process the array items structure
                items_structure = structure.get("items", {})
                self._add_preserved_field_info(items_structure, examples)
    
    def _extract_original_values(self, field_name: str, examples: List[Dict[str, Any]]) -> List[Any]:
        """Extract original values for a field from all examples."""
        values = []
        for example in examples:
            if isinstance(example, dict) and field_name in example:
                value = example[field_name]
                if value not in values:
                    values.append(value)
        return values
    
    def _extract_nested_value(self, obj: Any, field_name: str) -> Any:
        """Extract a nested field value from an object."""
        if isinstance(obj, dict):
            return obj.get(field_name)
        return None
    
    def _merge_structures(self, structure1: Dict[str, Any], structure2: Dict[str, Any]) -> Dict[str, Any]:
        """Merge two structures to create a more complete schema."""
        if structure1.get("type") != structure2.get("type"):
            # If types don't match, prefer the more specific one
            return structure1 if structure1.get("type") != "string" else structure2
        
        if structure1.get("type") == "object":
            merged_props = structure1.get("properties", {}).copy()
            for key, value in structure2.get("properties", {}).items():
                if key in merged_props:
                    merged_props[key] = self._merge_structures(merged_props[key], value)
                else:
                    merged_props[key] = value
            return {"type": "object", "properties": merged_props}
        
        elif structure1.get("type") == "array":
            items1 = structure1.get("items", {"type": "string"})
            items2 = structure2.get("items", {"type": "string"})
            merged_items = self._merge_structures(items1, items2)
            return {"type": "array", "items": merged_items}
        
        else:
            return structure1
    
    def _analyze_structure(self, obj: Any, max_depth: int = 10) -> Dict[str, Any]:
        """Recursively analyze the structure of an object to determine types."""
        if max_depth <= 0:
            return {"type": "string"}
        
        if isinstance(obj, dict):
            structure = {"type": "object", "properties": {}}
            for key, value in obj.items():
                structure["properties"][key] = self._analyze_structure(value, max_depth - 1)
            return structure
        elif isinstance(obj, list):
            if obj:
                # Analyze all items in the list to get a comprehensive structure
                item_structures = []
                for item in obj:
                    item_structure = self._analyze_structure(item, max_depth - 1)
                    item_structures.append(item_structure)
                
                # Merge all item structures
                if item_structures:
                    merged_items = item_structures[0]
                    for item_structure in item_structures[1:]:
                        merged_items = self._merge_structures(merged_items, item_structure)
                    return {"type": "array", "items": merged_items}
                else:
                    return {"type": "array", "items": {"type": "string"}}
            else:
                # For empty arrays, we'll need to infer from context or use a default
                return {"type": "array", "items": {"type": "object", "properties": {}}}
        elif isinstance(obj, bool):
            return {"type": "boolean"}
        elif isinstance(obj, (int, float)):
            return {"type": "number"}
        elif isinstance(obj, str):
            return {"type": "string"}
        else:
            return {"type": "string"}
    
    def generate_mock_value(self, schema: Dict[str, Any], field_name: str = "") -> Any:
        """Generate a mock value based on schema definition."""
        # Check if this field should preserve original values
        if schema.get("preserve_original", False):
            original_values = schema.get("original_values", [])
            if original_values:
                return random.choice(original_values)
        
        schema_type = schema.get("type", "string")
        
        # Handle different data types
        if schema_type == "string":
            return self._generate_mock_string(field_name)
        elif schema_type == "number":
            return self._generate_mock_number(field_name)
        elif schema_type == "boolean":
            return random.choice([True, False])
        elif schema_type == "array":
            return self._generate_mock_array(schema, field_name)
        elif schema_type == "object":
            return self._generate_mock_object(schema, field_name)
        else:
            return self._generate_mock_string(field_name)
    
    def _generate_mock_string(self, field_name: str) -> str:
        """Generate appropriate mock string based on field name."""
        field_lower = field_name.lower()
        
        # Generate appropriate mock data based on field name patterns
        if any(word in field_lower for word in ['name', 'שם']):
            return self.faker.name()
        elif any(word in field_lower for word in ['email', 'אימייל']):
            return self.faker.email()
        elif any(word in field_lower for word in ['phone', 'טלפון']):
            return self.faker.phone_number()
        elif any(word in field_lower for word in ['date', 'תאריך']):
            return self.faker.date()
        elif any(word in field_lower for word in ['policy', 'פוליסה']):
            return f"POL-{random.randint(100000, 999999)}"
        elif any(word in field_lower for word in ['currency', 'מטבע']):
            return random.choice(['₪', '$', '€', '£'])
        elif any(word in field_lower for word in ['status', 'סטטוס']):
            return random.choice(['active', 'inactive', 'pending', 'expired'])
        elif any(word in field_lower for word in ['type', 'סוג']):
            return random.choice(['personal', 'business', 'family', 'individual'])
        elif any(word in field_lower for word in ['description', 'תיאור']):
            return f"Mock {field_name} description"
        elif any(word in field_lower for word in ['destination', 'יעד']):
            return random.choice(['Europe', 'Asia', 'America', 'Africa', 'Australia'])
        elif any(word in field_lower for word in ['policytype', 'policy_type']):
            return random.choice(['life', 'health', 'travel', 'car', 'home'])
        elif any(word in field_lower for word in ['nickname', 'nick_name']):
            return f"Mock {field_name}"
        elif any(word in field_lower for word in ['subtype', 'sub_type']):
            return random.choice(['basic', 'premium', 'standard', 'advanced'])
        elif any(word in field_lower for word in ['desc', 'description']):
            return f"Mock {field_name} description"
        elif any(word in field_lower for word in ['insurancetype', 'insurance_type']):
            return random.choice(['מקיף + חובה', 'ביטוח חיים', 'ביטוח נסיעות', 'ביטוח בריאות'])
        elif any(word in field_lower for word in ['modeltype', 'model_type']):
            return random.choice(['טויוטה קורולה', 'הונדה סיוויק', 'סוזוקי סוויפט', 'מיצובישי לאנסר'])
        elif any(word in field_lower for word in ['licenseplate', 'license_plate']):
            return str(random.randint(10000000, 99999999))
        elif any(word in field_lower for word in ['policysubtype', 'policy_sub_type']):
            return random.choice(['makif', 'hova', 'basic', 'premium'])
        elif any(word in field_lower for word in ['method', 'payment_method']):
            return random.choice(['אשראי 1380', 'העברה בנקאית', 'צ\'ק', 'מזומן'])
        elif any(word in field_lower for word in ['paymenttype', 'payment_type']):
            return random.choice(['חיוב', 'זיכוי', 'תשלום'])
        elif any(word in field_lower for word in ['address']):
            return f"{self.faker.street_address()}, {self.faker.city()}"
        elif any(word in field_lower for word in ['esite', 'e_site']):
            return random.choice(['https://example.com', 'https://service.com', None])
        elif any(word in field_lower for word in ['classification']):
            return random.choice(['אישי', 'עסקי', 'משפחתי'])
        elif any(word in field_lower for word in ['sectorid', 'sector_id']):
            return str(random.randint(10, 999))
        elif any(word in field_lower for word in ['validitytime', 'validity_time']):
            return self.faker.date()
        elif any(word in field_lower for word in ['youngerdriverage', 'younger_driver_age']):
            return str(random.randint(18, 80))
        else:
            # For unknown fields, generate more appropriate mock data
            if len(field_name) > 0:
                return f"Mock_{field_name}_{random.randint(1000, 9999)}"
            else:
                return self.faker.word()
    
    def _generate_mock_number(self, field_name: str) -> Union[int, float]:
        """Generate appropriate mock number based on field name."""
        field_lower = field_name.lower()
        
        if any(word in field_lower for word in ['amount', 'sum', 'value', 'סכום', 'ערך']):
            return round(random.uniform(1000, 1000000), 2)
        elif any(word in field_lower for word in ['percent', 'percentage', 'אחוז']):
            return round(random.uniform(0, 100), 2)
        elif any(word in field_lower for word in ['count', 'number', 'מספר']):
            return random.randint(1, 100)
        elif any(word in field_lower for word in ['agent', 'agentnumber']):
            return random.randint(10000, 99999)
        elif any(word in field_lower for word in ['beneficiaries', 'beneficiariescount']):
            return random.randint(1, 10)
        elif any(word in field_lower for word in ['numsavingchannel', 'num_saving_channel']):
            return random.randint(1, 20)
        elif any(word in field_lower for word in ['status']):
            return random.randint(0, 3)
        elif any(word in field_lower for word in ['year', 'month', 'day']):
            return random.randint(1, 31)
        else:
            return random.randint(1, 1000)
    
    def _generate_mock_array(self, schema: Dict[str, Any], field_name: str) -> List[Any]:
        """Generate mock array based on schema."""
        items_schema = schema.get("items", {"type": "string"})
        array_length = random.randint(1, 5)  # Generate 1-5 items
        
        return [self.generate_mock_value(items_schema, field_name) for _ in range(array_length)]
    
    def _generate_mock_object(self, schema: Dict[str, Any], field_name: str) -> Dict[str, Any]:
        """Generate mock object based on schema."""
        properties = schema.get("properties", {})
        mock_object = {}
        
        for prop_name, prop_schema in properties.items():
            # Check if this field should preserve original values
            if prop_schema.get("preserve_original", False):
                original_values = prop_schema.get("original_values", [])
                if original_values:
                    mock_object[prop_name] = random.choice(original_values)
                    continue
            
            # Handle special cases for common object patterns
            if prop_name == "value" and field_name.lower() in ['sumsaving', 'summonthchange', 'accumulatechange', 'totalsaving', 'fluentwithdraw', 'expectedforretirement', 'savingexpectedforretirement', 'savingsum', 'fluentsum']:
                mock_object[prop_name] = round(random.uniform(1000, 1000000), 2)
            elif prop_name == "currency" and field_name.lower() in ['sumsaving', 'summonthchange', 'accumulatechange', 'totalsaving', 'fluentwithdraw', 'expectedforretirement', 'savingexpectedforretirement', 'savingsum', 'fluentsum']:
                mock_object[prop_name] = random.choice(['₪', '$', '€', '£'])
            elif prop_name == "sign" and field_name.lower() in ['monthchange']:
                mock_object[prop_name] = "%"
            elif prop_name == "status" and field_name.lower() in ['status']:
                mock_object[prop_name] = random.randint(0, 3)
            elif prop_name == "statusDesc" and field_name.lower() in ['status']:
                mock_object[prop_name] = random.choice(['Active', 'Inactive', 'Pending', 'Expired'])
            else:
                mock_object[prop_name] = self.generate_mock_value(prop_schema, prop_name)
        
        return mock_object
    
    def generate_mock_data_for_schema(self, schema_name: str, schema_structure: Dict[str, Any], num_records: int) -> List[Dict[str, Any]]:
        """Generate multiple mock records for a given schema."""
        mock_records = []
        
        for i in range(num_records):
            # Generate the main structure
            mock_record = self.generate_mock_value(schema_structure, schema_name)
            
            # Add metadata
            if isinstance(mock_record, dict):
                mock_record["_mock_id"] = i + 1
                mock_record["_generated_at"] = self.faker.iso8601()
            
            mock_records.append(mock_record)
        
        return mock_records
    
    def save_mock_data(self, schema_name: str, mock_data: List[Dict[str, Any]]) -> None:
        """Save mock data to a JSON file."""
        # Clean schema name for filename
        clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', schema_name)
        filename = f"mock_{clean_name}.json"
        filepath = self.output_path / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(mock_data, f, ensure_ascii=False, indent=2)
            print(f"💾 Saved mock data to: {filepath}")
        except Exception as e:
            print(f"❌ Error saving {filename}: {e}")
    
    def add_preserve_field(self, field_name: str) -> None:
        """Add a field to the preserve list so it keeps original values."""
        self.preserve_fields.add(field_name)
        print(f"✅ Added '{field_name}' to preserve list")
    
    def remove_preserve_field(self, field_name: str) -> None:
        """Remove a field from the preserve list."""
        if field_name in self.preserve_fields:
            self.preserve_fields.remove(field_name)
            print(f"✅ Removed '{field_name}' from preserve list")
        else:
            print(f"⚠️  Field '{field_name}' was not in preserve list")
    
    def list_preserve_fields(self) -> None:
        """List all fields that are currently preserved."""
        print("\n📋 Fields that preserve original values:")
        for field in sorted(self.preserve_fields):
            print(f"  - {field}")
        print(f"\nTotal: {len(self.preserve_fields)} fields")
    
    def get_available_insurance_types(self) -> List[str]:
        """Get list of available insurance types from schema definitions."""
        return get_available_insurance_types()
    
    def show_insurance_type_menu(self, available_types: List[str]) -> Optional[str]:
        """Show interactive menu for insurance type selection."""
        print("\n📋 Available insurance types:")
        print("-" * 50)
        
        for i, insurance_type in enumerate(available_types, 1):
            print(f"{i}. {insurance_type}")
        
        print(f"{len(available_types) + 1}. Generate all types")
        print(f"{len(available_types) + 2}. Exit")
        
        while True:
            try:
                choice = input(f"\nPlease select (1-{len(available_types) + 2}): ").strip()
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(available_types):
                    selected_type = available_types[choice_num - 1]
                    print(f"✅ Selected: {selected_type}")
                    return selected_type
                elif choice_num == len(available_types) + 1:
                    print("✅ Selected: Generate all types")
                    return "all"
                elif choice_num == len(available_types) + 2:
                    print("👋 Exiting...")
                    return None
                else:
                    print(f"❌ Invalid choice. Please enter a number between 1 and {len(available_types) + 2}")
            except ValueError:
                print("❌ Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                print("\n👋 Exiting...")
                return None
    
    def generate_realistic_dates(self) -> Dict[str, str]:
        """Generate realistic policy dates based on today's date (7/7/2025)."""
        # Today's date: 7/7/2025
        today = datetime(2025, 7, 7)
        
        # Generate start date within the past 6 months (randomly between 1-180 days ago)
        days_ago = random.randint(1, 180)
        start_date = today - timedelta(days=days_ago)
        
        # End date is 364 days after start date (one day less than a full year)
        # This makes it exactly one day before the start date of the next year
        end_date = start_date + timedelta(days=364)
        
        return {
            "start_date": start_date.strftime("%d.%m.%Y"),  # Israeli format DD.MM.YYYY
            "end_date": end_date.strftime("%d.%m.%Y"),      # Israeli format DD.MM.YYYY
            "start_date_short": start_date.strftime("%d.%m.%y"),  # Israeli format DD.MM.YY
            "end_date_short": end_date.strftime("%d.%m.%y"),      # Israeli format DD.MM.YY
            "start_date_israeli": start_date.strftime("%d/%m/%Y"),  # Israeli format DD/MM/YYYY
            "end_date_israeli": end_date.strftime("%d/%m/%Y"),      # Israeli format DD/MM/YYYY
            "year": start_date.year,
            "month": start_date.month,
            "day": start_date.day,
            "end_year": end_date.year,
            "end_month": end_date.month,
            "end_day": end_date.day
        }

    def generate_travel_dates(self) -> Dict[str, str]:
        """Generate realistic travel insurance dates (2-21 days trip duration)."""
        # Today's date: 7/7/2025
        today = datetime(2025, 7, 7)
        
        # Generate trip start date within the next 6 months (future trips)
        days_from_now = random.randint(1, 180)
        start_date = today + timedelta(days=days_from_now)
        
        # Generate trip duration (2-21 days)
        trip_duration = random.randint(2, 21)
        end_date = start_date + timedelta(days=trip_duration)
        
        return {
            "start_date": start_date.strftime("%d.%m.%Y"),  # Israeli format DD.MM.YYYY
            "end_date": end_date.strftime("%d.%m.%Y"),      # Israeli format DD.MM.YYYY
            "start_date_short": start_date.strftime("%d.%m.%y"),  # Israeli format DD.MM.YY
            "end_date_short": end_date.strftime("%d.%m.%y"),      # Israeli format DD.MM.YY
            "start_date_israeli": start_date.strftime("%d/%m/%Y"),  # Israeli format DD/MM/YYYY
            "end_date_israeli": end_date.strftime("%d/%m/%Y"),      # Israeli format DD/MM/YYYY
            "year": start_date.year,
            "month": start_date.month,
            "day": start_date.day,
            "end_year": end_date.year,
            "end_month": end_date.month,
            "end_day": end_date.day,
            "trip_duration": trip_duration
        }

    def generate_insurance_specific_field(self, field_name: str, generation_pattern: str) -> Any:
        """Generate field value based on insurance-specific patterns."""
        if generation_pattern == "policy_id":
            return f"POL-{random.randint(100000, 999999)}"
        elif generation_pattern == "travel_insurance_type":
            return "ביטוח נסיעות לחו\"ל"
        elif generation_pattern == "travel_policy_name":
            return "ביטוח נסיעות לחו\"ל"
        elif generation_pattern == "vehicle_insurance_type":
            return random.choice(['ביטוח צד ג\' ללא ביטול הש', 'ביטוח מקיף', 'ביטוח חובה'])
        elif generation_pattern == "vehicle_policy_name":
            return random.choice(['ביטוח לרכב פרטי', 'ביטוח נהג צעיר', 'ביטוח רכב משפחתי'])
        elif generation_pattern == "health_insurance_type":
            return random.choice(['קולקטיב - ביטוח בריאות קבוצתי', 'ביטוח בריאות פרטי', 'ביטוח בריאות משפחתי'])
        elif generation_pattern == "health_policy_name":
            return random.choice(['ביטוח בריאות', 'ביטוח בריאות פרמיום', 'ביטוח בריאות בסיסי'])
        elif generation_pattern == "life_insurance_type":
            return random.choice(['קלאסי', 'ביטוח חיים', 'ביטוח למקרה פטירה'])
        elif generation_pattern == "life_policy_name":
            return random.choice(['ביטוח למקרה פטירה', 'ריסק 1', 'ביטוח חיים פרמיום'])
        elif generation_pattern == "business_insurance_type":
            return random.choice(['ביטוח עסקי', 'ביטוח אחריות מקצועית', 'ביטוח רכוש עסקי'])
        elif generation_pattern == "business_policy_name":
            return random.choice(['ביטוח עסקי', 'ביטוח אחריות', 'ביטוח רכוש'])
        elif generation_pattern == "dental_policy_name":
            return random.choice(['ביטוח שיניים', 'ביטוח שיניים פרמיום', 'ביטוח שיניים משפחתי'])
        elif generation_pattern == "dira_insurance_type":
            return random.choice(['ביטוח דירה', 'ביטוח רכוש', 'ביטוח מבנה'])
        elif generation_pattern == "dira_policy_name":
            return random.choice(['ביטוח דירה', 'ביטוח רכוש', 'ביטוח מבנה'])
        elif generation_pattern == "other_insurance_type":
            return random.choice(['ביטוח אחר', 'ביטוח נוסף', 'ביטוח מיוחד'])
        elif generation_pattern == "other_policy_name":
            return random.choice(['ביטוח אחר', 'ביטוח נוסף', 'ביטוח מיוחד'])
        elif generation_pattern == "date":
            # Use realistic dates based on today
            dates = self.generate_realistic_dates()
            return dates["start_date"]
        elif generation_pattern == "travel_description":
            return random.choice(['SMART TRAVEL', 'TRAVEL PLUS', 'BASIC TRAVEL'])
        elif generation_pattern == "destination":
            return random.choice(['אירופה', 'אסיה', 'אמריקה', 'אפריקה', 'אוסטרליה'])
        elif generation_pattern == "name":
            return self.faker.name()
        elif generation_pattern == "beneficiaries_count":
            return random.randint(1, 10)
        elif generation_pattern == "agent_number":
            return random.randint(10000, 99999)
        elif generation_pattern == "vehicle_model":
            return random.choice(['טויוטה קורולה', 'הונדה סיוויק', 'סוזוקי סוויפט', 'מיצובישי לאנסר', 'יונדאי I01 החדשה'])
        elif generation_pattern == "license_plate":
            return str(random.randint(10000000, 99999999))
        elif generation_pattern == "classification":
            return random.choice(['אישי', 'עסקי', 'משפחתי'])
        elif generation_pattern == "car_policy_type":
            return random.choice(['makif', 'hova', 'basic', 'premium'])
        elif generation_pattern == "sector_id":
            return str(random.randint(10, 999))
        elif generation_pattern == "currency":
            return random.choice(['₪', '$', '€', '£'])
        elif generation_pattern == "insurance_value":
            return random.randint(10000, 1000000)
        elif generation_pattern == "collective_number":
            return f"COL-{random.randint(100000, 999999)}"
        elif generation_pattern == "address":
            return f"{self.faker.street_address()}, {self.faker.city()}"
        elif generation_pattern == "dira_description":
            return random.choice(['ביטוח דירה בסיסי', 'ביטוח דירה מורחב', 'ביטוח דירה פרמיום'])
        elif generation_pattern == "travel_entity":
            return "WebTravelCoversByNumResponse"
        elif generation_pattern == "travel_coverage":
            # Generate basic coverage structure
            return self.generate_travel_coverage()
        elif generation_pattern == "travel_extreme_sport":
            # Generate extreme sport coverage with dates
            return self.generate_travel_extreme_sport_coverage()
        elif generation_pattern == "travel_mobile_phone":
            # Generate mobile phone coverage with device details
            return self.generate_travel_mobile_phone_coverage()
        elif generation_pattern == "travel_laptop_tablet":
            # Generate laptop/tablet coverage with device details
            return self.generate_travel_laptop_tablet_coverage()
        elif generation_pattern == "travel_coverage_with_insured":
            return self.generate_travel_coverage_with_insured(insured_persons)
        elif generation_pattern == "travel_extreme_sport_coverage_with_insured":
            return self.generate_travel_extreme_sport_coverage_with_insured(insured_persons, dates)
        elif generation_pattern == "travel_mobile_phone_coverage_with_insured":
            return self.generate_travel_mobile_phone_coverage_with_insured(insured_persons)
        elif generation_pattern == "travel_laptop_tablet_coverage_with_insured":
            return self.generate_travel_laptop_tablet_coverage_with_insured(insured_persons)
        elif generation_pattern == "mymoney_top_header":
            return self.generate_mymoney_top_header()
        elif generation_pattern == "mymoney_main_header":
            return self.generate_mymoney_main_header()
        elif generation_pattern == "mymoney_accumulation":
            return self.generate_mymoney_accumulation()
        elif generation_pattern == "mymoney_product_list":
            return self.generate_mymoney_product_list()
        elif generation_pattern == "mymoney_last_actions":
            return self.generate_mymoney_last_actions()
        else:
            # Fallback to generic generation
            return self._generate_mock_string(field_name)

    def generate_vehicle_united_detail(self, dates: Dict[str, str]) -> Dict[str, Any]:
        """Generate the complex vehicleUnitedDetail structure."""
        return {
            "insuranceDetails": {
                "updatedAt": dates["start_date_short"],
                "startDate": dates["start_date_short"],
                "endDate": dates["end_date_short"],
                "originalEndDate": f"{dates['end_year']}-{dates['end_month']:02d}-{dates['end_day']:02d}T00:00:00",
                "originalStartDate": f"{dates['year']}-{dates['month']:02d}-{dates['day']:02d}T00:00:00",
                "premia": {
                    "value": random.randint(1000, 10000),
                    "currency": "₪"
                },
                "list": [
                    {
                        "requiredRenewal": True,
                        "startDate": dates["start_date_short"],
                        "endDate": dates["end_date_short"],
                        "policySubType": "makif",
                        "premia": {
                            "currency": "₪",
                            "value": random.randint(1000, 8000)
                        },
                        "claimsList": [
                            {
                                "claimNo": str(random.randint(1000000000, 9999999999)),
                                "submissionDate": dates["start_date_short"]
                            }
                        ] if random.choice([True, False]) else []
                    },
                    {
                        "requiredRenewal": True,
                        "startDate": dates["start_date_short"],
                        "endDate": dates["end_date_short"],
                        "policySubType": "hova",
                        "premia": {
                            "currency": "₪",
                            "value": random.randint(500, 3000)
                        },
                        "claimsList": []
                    }
                ]
            },
            "payments": {
                "payedSum": {
                    "value": random.randint(1000, 8000),
                    "currency": "₪"
                },
                "balanceSum": {
                    "value": random.randint(0, 3000),
                    "currency": "₪"
                },
                "payedList": {
                    "list": [
                        {
                            "date": dates["start_date_israeli"],
                            "method": random.choice(["תשלום בכרטיס אשראי", "ויזה כ.א.ל 2666", "העברה בנקאית"]),
                            "paymentType": "חיוב",
                            "amount": {
                                "value": random.randint(100, 1000),
                                "currency": "₪"
                            },
                            "details": [
                                {
                                    "paymentNo": None,
                                    "date": dates["start_date_israeli"],
                                    "method": random.choice(["תשלום בכרטיס אשראי", "ויזה כ.א.ל 2666"]),
                                    "totalPayments": "",
                                    "policySubType": random.choice(["makif", "hova"]),
                                    "amount": {
                                        "value": random.randint(100, 1000),
                                        "currency": "₪"
                                    }
                                }
                            ]
                        }
                    ]
                }
            },
            "agentDetails": [
                {
                    "name": random.choice(["הפניקס SMART", "מגדל ביטוח", "כלל ביטוח", "הראל ביטוח"]),
                    "address": f"{self.faker.street_address()}, {self.faker.city()} {random.randint(10000, 99999)}",
                    "phone": f"0{random.randint(70, 79)}{random.randint(1000000, 9999999)}"
                }
            ],
            "authorizedDrivers": [
                {
                    "firstName": self.faker.first_name(),
                    "lastName": self.faker.last_name()
                },
                {
                    "firstName": self.faker.first_name(),
                    "lastName": self.faker.last_name()
                }
            ],
            "serviceList": [
                {
                    "type": "גרירה",
                    "name": "שגריר",
                    "phone": "*8888",
                    "eSite": None
                },
                {
                    "type": "שמשות",
                    "name": "אוטוגלס",
                    "phone": "03-6507777",
                    "eSite": None
                },
                {
                    "type": "פנסים ומראות",
                    "name": "אוטוגלס",
                    "phone": "03-6507777",
                    "eSite": None
                }
            ],
            "treatmentSubjects": [],
            "licenseEndDate": dates["end_date_short"],
            "youngerDriverAge": str(random.randint(18, 80))
        }

    def generate_insurance_record(self, insurance_type: str) -> Dict[str, Any]:
        """Generate a complete insurance record based on the schema."""
        schema = get_schema(insurance_type)
        if not schema:
            raise ValueError(f"Unknown insurance type: {insurance_type}")
        
        # Generate realistic dates for this record
        dates = self.generate_realistic_dates()
        
        # For travel insurance, use travel-specific dates (2-21 days)
        if insurance_type == "travel":
            dates = self.generate_travel_dates()
        
        # For vehicleUnited, generate consistent vehicle details for all policies
        if insurance_type == "vehicleUnited":
            vehicle_model = random.choice(['טויוטה קורולה', 'הונדה סיוויק', 'סוזוקי סוויפט', 'מיצובישי לאנסר', 'יונדאי I01 החדשה'])
            license_plate = str(random.randint(10000000, 99999999))
        else:
            vehicle_model = None
            license_plate = None
        
        # For travel insurance, generate a single consistent set of insured persons
        if insurance_type == "travel":
            insured_count = random.randint(2, 4)
            insured_persons = [self.faker.first_name() for _ in range(insured_count)]
        else:
            insured_persons = None
        
        record = {}
        
        # Generate required fields based on schema
        for field_name, field_def in schema.required_fields.items():
            if field_def.generation_pattern:
                if field_def.generation_pattern == "date":
                    # Use appropriate date based on field name
                    if "end" in field_name.lower():
                        record[field_name] = dates["end_date"]
                    else:
                        record[field_name] = dates["start_date"]
                elif field_def.generation_pattern == "vehicle_model" and vehicle_model:
                    record[field_name] = vehicle_model
                elif field_def.generation_pattern == "license_plate" and license_plate:
                    record[field_name] = license_plate
                else:
                    record[field_name] = self.generate_insurance_specific_field(field_name, field_def.generation_pattern)
            elif field_def.field_type == FieldType.BOOLEAN:
                record[field_name] = random.choice([True, False])
            elif field_def.field_type == FieldType.INTEGER:
                record[field_name] = random.randint(1, 1000)
            elif field_def.field_type == FieldType.STRING:
                record[field_name] = self._generate_mock_string(field_name)
            elif field_def.field_type == FieldType.NULL:
                record[field_name] = None
            elif field_def.field_type == FieldType.OBJECT:
                # Handle complex objects
                if field_name == "insuranceSum":
                    record[field_name] = {
                        "value": random.randint(10000, 1000000),
                        "currency": random.choice(['₪', '$', '€', '£'])
                    }
                elif field_name == "vehicleUnitedDetail":
                    record[field_name] = self.generate_vehicle_united_detail(dates)
                else:
                    record[field_name] = {}
            elif field_def.field_type == FieldType.ARRAY:
                # Handle arrays
                if field_name == "list":
                    # Generate policy list for vehicleUnited with consistent vehicle details
                    # Generate consistent policy type and name for the list policy
                    list_policy_type = random.choice(['makif', 'hova'])
                    if list_policy_type == 'makif':
                        list_policy_name = 'ביטוח מקיף לרכב פרטי'
                        list_insurance_type = 'ביטוח מקיף'
                    else:  # hova
                        list_policy_name = 'ביטוח חובה לרכב פרטי'
                        list_insurance_type = 'ביטוח חובה'
                    
                    record[field_name] = [
                        {
                            "policyId": f"POL-{random.randint(100000, 999999)}",
                            "insuranceType": list_insurance_type,
                            "policyName": list_policy_name,
                            "endDate": dates["end_date"],
                            "startDate": dates["start_date"],
                            "modelType": vehicle_model if vehicle_model else random.choice(['טויוטה קורולה', 'הונדה סיוויק', 'סוזוקי סוויפט', 'מיצובישי לאנסר', 'יונדאי I01 החדשה']),
                            "licensePlate": license_plate if license_plate else str(random.randint(10000000, 99999999)),
                            "classification": random.choice(['אישי', 'עסקי', 'משפחתי']),
                            "carPolicyType": list_policy_type,
                            "isExpired": random.choice([True, False]),
                            "isActive": random.choice([True, False]),
                            "sectorId": str(random.randint(10, 999)),
                            "validityTime": dates["start_date"],
                            "isSmart": random.choice([True, False]),
                            "AgentNumber": random.randint(10000, 99999)
                        }
                    ]
                else:
                    record[field_name] = []
        
        # For vehicleUnited, ensure main policy has consistent policy type and name
        if insurance_type == "vehicleUnited":
            # Check if we have carPolicyType and policyName, and make them consistent
            if "carPolicyType" in record and "policyName" in record:
                if record["carPolicyType"] == "makif":
                    record["policyName"] = random.choice(['ביטוח מקיף לרכב פרטי', 'ביטוח רכב משפחתי', 'ביטוח לרכב פרטי'])
                    record["insuranceType"] = 'ביטוח מקיף'
                elif record["carPolicyType"] == "hova":
                    record["policyName"] = random.choice(['ביטוח חובה לרכב פרטי', 'ביטוח חובה'])
                    record["insuranceType"] = 'ביטוח חובה'
        
        # For travel insurance, create the complex coverage structure with consistent insured persons
        if insurance_type == "travel":
            # Create the response structure that matches the new example
            coverage_response = {
                "basicCoverage": self.generate_travel_coverage_with_insured(insured_persons),
                "loggage": self.generate_travel_coverage_with_insured(insured_persons),
                "searchRescue": self.generate_travel_coverage_with_insured(insured_persons),
                "corona": self.generate_travel_coverage_with_insured(insured_persons),
                "extremeSport": self.generate_travel_extreme_sport_coverage_with_insured(insured_persons, dates),
                "mobilePhone": self.generate_travel_mobile_phone_coverage_with_insured(insured_persons),
                "laptopOrTablet": self.generate_travel_laptop_tablet_coverage_with_insured(insured_persons),
                "cancelOrDelay": self.generate_travel_coverage_with_insured(insured_persons)
            }
            
            # Replace the record with the new structure
            record = coverage_response
        
        # Validate the generated record
        validation_errors = validate_insurance_data(insurance_type, record)
        if validation_errors:
            print(f"⚠️  Validation warnings for {insurance_type}: {validation_errors}")
        
        return record
    
    def run(self, insurance_type: Optional[str] = None):
        """Main execution method."""
        print("🚀 Starting Mock Data Generator")
        print("=" * 50)
        
        # Show current preserve fields
        self.list_preserve_fields()
        
        # Step 1: Load Swagger file
        if not self.load_swagger_file():
            return
        
        # Step 2: Load example files
        if not self.load_example_files():
            return
        
        # Step 3: Handle insurance type selection
        if insurance_type is None:
            # Interactive mode - show menu
            available_types = self.get_available_insurance_types()
            if not available_types:
                print("❌ No insurance types found in example files")
                return
            
            insurance_type = self.show_insurance_type_menu(available_types)
            if insurance_type is None:
                return  # User chose to exit
        else:
            # Command line mode - validate the provided type
            available_types = self.get_available_insurance_types()
            if insurance_type not in available_types and insurance_type != "all":
                print(f"❌ Invalid insurance type: {insurance_type}")
                print(f"Available types: {', '.join(available_types)}")
                return
        
        # Step 4: Filter examples based on insurance type
        if insurance_type:
            print(f"🎯 Filtering examples for insurance type: {insurance_type}")
            
            if insurance_type == "mymoney":
                # For MyMoney, look for getMyMoneyById files and hishtalmut files
                filtered_examples = [
                    example for example in self.example_files
                    if "getMyMoneyById" in str(example) or "hishtalmut" in str(example)
                ]
            else:
                # For other insurance types, look for the type in the filename
                filtered_examples = [
                    example for example in self.example_files
                    if insurance_type.lower() in str(example).lower()
                ]
            
            if filtered_examples:
                print(f"✅ Found {len(filtered_examples)} examples for {insurance_type}")
                self.example_files = filtered_examples
            else:
                print(f"❌ No examples found for insurance type: {insurance_type}")
                print("Available example files:")
                for example in self.example_files:
                    print(f"  - {example}")
                return
        
        # Step 5: Extract schemas from examples
        print("\n📊 Analyzing example data structures...")
        schema_structures = self.extract_schemas_from_examples()
        
        if not schema_structures:
            print("❌ No schema structures found in example data")
            return
        
        print(f"✅ Found {len(schema_structures)} schema structures in examples")
        
        # Step 7: Generate mock data
        print("\n🎲 Generating mock data...")
        
        if insurance_type == "all":
            # Generate for all insurance types
            insurance_types_to_generate = self.get_available_insurance_types()
        else:
            # Generate for specific insurance type
            insurance_types_to_generate = [insurance_type]
        
        for current_insurance_type in insurance_types_to_generate:
            print(f"\n📋 Generating mock data for: {current_insurance_type}")
            
            # Get number of records to generate
            try:
                num_records = int(input(f"Enter number of {current_insurance_type} records to generate (default: 5): ") or "5")
            except (ValueError, KeyboardInterrupt):
                print("Using default: 5 records")
                num_records = 5
            
            # Generate records using schema-based approach
            for i in range(num_records):
                try:
                    record = self.generate_insurance_record(current_insurance_type)
                    
                    # Create the response structure for each individual record
                    if current_insurance_type == "travel":
                        # Special structure for travel insurance
                        mock_response = {
                            "status": "success",
                            "message": f"Mock data generated for {current_insurance_type}",
                            "transId": f"mock-{random.randint(100000, 999999)}",
                            "response": {
                                "status": 200,
                                "message": "OK",
                                "transId": "default",
                                "entity": "WebTravelCoversByNumResponse",
                                "response": record  # The coverage structure
                            }
                        }
                    elif current_insurance_type == "mymoney":
                        # Special structure for MyMoney financial portfolio
                        mock_response = {
                            "status": 200,
                            "message": "OK",
                            "transId": "string",
                            "entity": "MyMoneyResponse",
                            "response": record  # The financial portfolio structure
                        }
                    else:
                        # Standard structure for other insurance types
                        mock_response = {
                            "status": "success",
                            "message": f"Mock data generated for {current_insurance_type}",
                            "transId": f"mock-{random.randint(100000, 999999)}",
                            "response": [
                                {
                                    "id": current_insurance_type,
                                    "data": [record]  # Single record per file
                                }
                            ]
                        }
                    
                    # Generate unique filename with timestamp and counter
                    timestamp = self.faker.date_time().strftime("%Y%m%d_%H%M%S")
                    counter = random.randint(1000, 9999)
                    output_file = self.output_path / f"mock_{current_insurance_type}Entity_{timestamp}_{counter}.json"
                    
                    try:
                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(mock_response, f, ensure_ascii=False, indent=2)
                        print(f"✅ Generated {current_insurance_type} record {i+1}/{num_records}: {output_file.name}")
                    except Exception as e:
                        print(f"❌ Error saving {current_insurance_type} record {i+1}: {e}")
                        
                except Exception as e:
                    print(f"⚠️  Error generating record {i+1} for {current_insurance_type}: {e}")
            
            print(f"✅ Completed generating {num_records} {current_insurance_type} files")
        
        print("\n🎉 Mock data generation completed!")
        print(f"📁 Output directory: {self.output_path}")

    def generate_travel_coverage(self) -> Dict[str, Any]:
        """Generate basic travel coverage structure."""
        # Generate 2-4 insured persons
        insured_count = random.randint(2, 4)
        insured_names = [self.faker.first_name() for _ in range(insured_count)]
        
        return {
            "insuredList": insured_names if random.choice([True, False]) else None,
            "extraData": None,
            "allInsured": random.choice([True, False])
        }
    
    def generate_travel_extreme_sport_coverage(self) -> Dict[str, Any]:
        """Generate extreme sport coverage with dates."""
        # Generate 2-4 insured persons
        insured_count = random.randint(2, 4)
        insured_names = [self.faker.first_name() for _ in range(insured_count)]
        
        # Generate dates for extreme sports activities
        dates = self.generate_realistic_dates()
        extra_data = []
        for _ in range(insured_count):
            extra_data.append({
                "startDate": dates["start_date_israeli"],
                "endDate": dates["end_date_israeli"]
            })
        
        return {
            "insuredList": insured_names,
            "extraData": extra_data,
            "allInsured": True
        }
    
    def generate_travel_mobile_phone_coverage(self) -> Dict[str, Any]:
        """Generate mobile phone coverage with device details."""
        # Usually only one person has mobile phone coverage
        insured_name = self.faker.first_name()
        
        phone_models = [
            "אייפון 15 פרו",
            "אייפון 14 פרו",
            "סמסונג גלקסי S24",
            "סמסונג גלקסי S23",
            "גוגל פיקסל 8",
            "OnePlus 11"
        ]
        
        extra_data = [{
            "owner": insured_name,
            "model": random.choice(phone_models)
        }]
        
        return {
            "insuredList": [insured_name],
            "extraData": extra_data,
            "allInsured": False
        }
    
    def generate_travel_laptop_tablet_coverage(self) -> Dict[str, Any]:
        """Generate laptop/tablet coverage with device details."""
        # Usually only one person has laptop/tablet coverage
        insured_name = self.faker.first_name()
        
        device_models = [
            "MEC BOOK AIR",
            "MEC BOOK PRO",
            "iPad Pro",
            "iPad Air",
            "Surface Pro",
            "Dell XPS 13",
            "Lenovo ThinkPad"
        ]
        
        extra_data = [{
            "owner": insured_name,
            "model": random.choice(device_models)
        }]
        
        return {
            "insuredList": [insured_name],
            "extraData": extra_data,
            "allInsured": False
        }

    def generate_travel_coverage_with_insured(self, insured_persons: List[str]) -> Dict[str, Any]:
        """Generate basic travel coverage structure using the provided insured persons."""
        return {
            "insuredList": insured_persons if random.choice([True, False]) else None,
            "extraData": None,
            "allInsured": random.choice([True, False])
        }
    
    def generate_travel_extreme_sport_coverage_with_insured(self, insured_persons: List[str], dates: Dict[str, str]) -> Dict[str, Any]:
        """Generate extreme sport coverage with dates using the provided insured persons."""
        # Generate dates for extreme sports activities
        extra_data = []
        for _ in range(len(insured_persons)):
            extra_data.append({
                "startDate": dates["start_date_israeli"],
                "endDate": dates["end_date_israeli"]
            })
        
        return {
            "insuredList": insured_persons,
            "extraData": extra_data,
            "allInsured": True
        }
    
    def generate_travel_mobile_phone_coverage_with_insured(self, insured_persons: List[str]) -> Dict[str, Any]:
        """Generate mobile phone coverage with device details using the provided insured persons."""
        # Usually only one person has mobile phone coverage
        insured_name = random.choice(insured_persons)
        
        phone_models = [
            "אייפון 15 פרו",
            "אייפון 14 פרו",
            "סמסונג גלקסי S24",
            "סמסונג גלקסי S23",
            "גוגל פיקסל 8",
            "OnePlus 11"
        ]
        
        extra_data = [{
            "owner": insured_name,
            "model": random.choice(phone_models)
        }]
        
        return {
            "insuredList": [insured_name],
            "extraData": extra_data,
            "allInsured": False
        }
    
    def generate_travel_laptop_tablet_coverage_with_insured(self, insured_persons: List[str]) -> Dict[str, Any]:
        """Generate laptop/tablet coverage with device details using the provided insured persons."""
        # Usually only one person has laptop/tablet coverage
        insured_name = random.choice(insured_persons)
        
        device_models = [
            "MEC BOOK AIR",
            "MEC BOOK PRO",
            "iPad Pro",
            "iPad Air",
            "Surface Pro",
            "Dell XPS 13",
            "Lenovo ThinkPad"
        ]
        
        extra_data = [{
            "owner": insured_name,
            "model": random.choice(device_models)
        }]
        
        return {
            "insuredList": [insured_name],
            "extraData": extra_data,
            "allInsured": False
        }

    def generate_mymoney_top_header(self) -> Dict[str, Any]:
        """Generate top header for MyMoney response."""
        total_savings = random.randint(100000, 2000000)
        month_change = random.uniform(-5, 5)
        accumulate_change = random.uniform(-50000, 50000)
        
        return {
            "sumSaving": {
                "value": total_savings,
                "currency": "₪"
            },
            "numSavingChannel": random.randint(1, 3),
            "monthChange": {
                "value": round(month_change, 2),
                "sign": "%"
            },
            "sumMonthChange": {
                "value": round(total_savings * month_change / 100, 2),
                "currency": "₪"
            },
            "accumulateChange": {
                "value": round(accumulate_change, 2),
                "currency": "₪"
            }
        }
    
    def generate_mymoney_main_header(self) -> Dict[str, Any]:
        """Generate main header for MyMoney response."""
        dates = self.generate_realistic_dates()
        total_savings = random.randint(100000, 2000000)
        fluent_withdraw = random.randint(0, total_savings // 2) if random.choice([True, False]) else None
        expected_retirement = random.randint(5000, 50000) if random.choice([True, False]) else None
        
        return {
            "date": dates["start_date"],
            "totalSaving": {
                "value": total_savings,
                "currency": "₪"
            },
            "fluentWithdraw": {
                "value": fluent_withdraw,
                "currency": "₪"
            } if fluent_withdraw else None,
            "expectedForRetirement": {
                "value": expected_retirement,
                "currency": "₪"
            } if expected_retirement else None,
            "savingExpectedForRetirement": None
        }
    
    def generate_mymoney_accumulation(self) -> Dict[str, Any]:
        """Generate accumulation by product for MyMoney response."""
        # Generate one policy for each of the three product types
        product_types = ["gemel", "hishtalmut", "gemelInvestment"]
        accumulation_list = []
        
        for product_type in product_types:
            if random.choice([True, False]):  # 50% chance to include each product type
                saving_sum = random.randint(50000, 500000)
                fluent_sum = random.randint(0, saving_sum) if product_type in ["hishtalmut", "gemelInvestment"] else None
                expected_retirement = random.randint(5000, 30000) if product_type == "gemel" else None
                
                accumulation_list.append({
                    "policyType": product_type,
                    "savingSum": {
                        "value": saving_sum,
                        "currency": "₪"
                    },
                    "fluentSum": {
                        "value": fluent_sum,
                        "currency": "₪"
                    } if fluent_sum else None,
                    "eligibilityDate": "",
                    "expectedForRetirement": {
                        "value": expected_retirement,
                        "currency": "₪"
                    } if expected_retirement else None,
                    "notUsedForRetirement": product_type in ["hishtalmut", "gemelInvestment"],
                    "policyIds": [self.generate_policy_id(product_type)],
                    "updateDate": self.generate_realistic_dates()["start_date_short"]
                })
        
        return {
            "list": accumulation_list
        }
    
    def generate_mymoney_product_list(self) -> Dict[str, Any]:
        """Generate product list for MyMoney response."""
        product_types = ["gemel", "hishtalmut", "gemelInvestment"]
        product_list = []
        
        for product_type in product_types:
            if random.choice([True, False]):  # 50% chance to include each product type
                policy_list = [self.generate_mymoney_policy(product_type)]
                product_list.append({
                    "policyType": product_type,
                    "policyList": policy_list
                })
        
        return {
            "list": product_list
        }
    
    def generate_mymoney_last_actions(self) -> Dict[str, Any]:
        """Generate last actions for MyMoney response."""
        return {
            "list": []  # Usually empty based on examples
        }
    
    def generate_policy_id(self, product_type: str) -> str:
        """Generate policy ID based on product type."""
        if product_type == "gemel":
            return f"001-{random.randint(100, 999)}-{random.randint(100000, 999999)} ({random.randint(1000000, 9999999)})"
        elif product_type == "hishtalmut":
            return f"007-{random.randint(100, 999)}-{random.randint(100000, 999999)} ({random.randint(1000000, 9999999)})"
        elif product_type == "gemelInvestment":
            return f"570-{random.randint(100, 999)}-{random.randint(100000, 999999)} ({random.randint(1000000, 9999999)})"
        else:
            return f"{random.randint(100000000, 999999999)}"
    
    def generate_mymoney_policy(self, product_type: str) -> Dict[str, Any]:
        """Generate a single policy for MyMoney response."""
        policy_id = self.generate_policy_id(product_type)
        dates = self.generate_realistic_dates()
        saving_sum = random.randint(50000, 500000)
        status = random.choice([1, 2])  # 1=inactive, 2=active
        
        # Generate investment route
        investment_route = self.generate_investment_route(product_type, saving_sum)
        
        return {
            "policyId": policy_id,
            "originalPolicyName": None,
            "policyNickname": None,
            "subType": self.generate_subtype(product_type),
            "status": {
                "status": status,
                "statusDesc": "לא פעילה" if status == 1 else "פעילה"
            },
            "updateTo": dates["start_date"],
            "dailyUpdateTo": dates["start_date"] if random.choice([True, False]) else None,
            "yieldUpdateDate": dates["start_date_short"] if random.choice([True, False]) else None,
            "dailyYieldUpdateDate": dates["start_date"] if random.choice([True, False]) else "",
            "hasProfitsShare": random.choice([True, False, None]),
            "productData": self.generate_product_data(product_type, saving_sum),
            "investmentRoutes": [investment_route] if investment_route else [],
            "tsuotPopup": None,
            "isNew": random.choice([True, False]),
            "isIndependent": random.choice([True, False, None])
        }
    
    def generate_subtype(self, product_type: str) -> Optional[str]:
        """Generate subtype based on product type."""
        if product_type == "gemel":
            return random.choice([None, "MASHLIMA", "MAKIFA"])
        else:
            return None
    
    def generate_product_data(self, product_type: str, saving_sum: int) -> Dict[str, Any]:
        """Generate product data for a policy."""
        dates = self.generate_realistic_dates()
        last_deposit = random.randint(1000, 10000) if random.choice([True, False]) else None
        available_withdraw = random.randint(0, saving_sum) if random.choice([True, False]) else None
        
        return {
            "savingSum": {
                "value": saving_sum,
                "currency": "₪"
            },
            "yieldBeginningYear": None,
            "lastDeposit": {
                "lastDepositsSum": {
                    "value": last_deposit,
                    "currency": "₪"
                },
                "lastDepositsDate": dates["start_date"]
            } if last_deposit else None,
            "depositedThisYear": None,
            "availableWithdraw": {
                "value": available_withdraw,
                "currency": "₪"
            } if available_withdraw else None,
            "withdrawDate": dates["end_date"] if random.choice([True, False]) else None,
            "managementFee": {
                "fromDeposit": {
                    "value": 0 if product_type in ["hishtalmut", "gemelInvestment"] else random.uniform(0, 2),
                    "sign": "%"
                },
                "fromSaving": {
                    "value": random.uniform(0.5, 0.7) if product_type in ["hishtalmut", "gemelInvestment"] else random.uniform(0.1, 0.6),
                    "sign": "%"
                }
            },
            "yieldFromYearBeginningTotal": None
        }
    
    def generate_investment_route(self, product_type: str, saving_sum: int) -> Optional[Dict[str, Any]]:
        """Generate investment route for a policy."""
        if not random.choice([True, False]):  # 50% chance to have investment route
            return None
            
        dates = self.generate_realistic_dates()
        yield_value = random.uniform(-3, 4)
        
        route_names = {
            "gemel": "הפניקס גמל אשראי ואג\"ח",
            "hishtalmut": "הפניקס השתלמות אשראי ואג\"ח",
            "gemelInvestment": "הפניקס גמל להשקעה עוקב מדד S&P500"
        }
        
        return {
            "name": route_names.get(product_type, "השקעה כללית"),
            "joinDate": None,
            "percent": {
                "value": 100,
                "sign": "%"
            },
            "yieldBeginningYear": {
                "value": round(yield_value, 2),
                "sign": "%"
            },
            "yieldBeginningPolicy": None,
            "managementFeeFromDeposit": {
                "value": 0 if product_type in ["hishtalmut", "gemelInvestment"] else random.uniform(0, 2),
                "sign": "%"
            },
            "managementFeeFromSaving": {
                "value": random.uniform(0.5, 0.7) if product_type in ["hishtalmut", "gemelInvestment"] else random.uniform(0.1, 0.6),
                "sign": "%"
            },
            "accumulation": {
                "value": saving_sum,
                "currency": "₪"
            },
            "basketCode": str(random.randint(10, 9999)),
            "isYieldHidden": random.choice([True, False, None]),
            "dailyUpdateDate": dates["start_date"] if random.choice([True, False]) else None
        }

def main():
    """Main function to run the mock data generator."""
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description="Generate mock data for chatbot testing based on Swagger schemas and example data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mock_data_generator.py                    # Interactive mode
  python mock_data_generator.py --type health      # Generate health insurance data
  python mock_data_generator.py --type vehicleUnited  # Generate vehicle insurance data
  python mock_data_generator.py --type all         # Generate all insurance types
        """
    )
    
    parser.add_argument(
        '--type', '--insurance-type',
        dest='insurance_type',
        help='Insurance type to generate (e.g., health, vehicleUnited, life). Use "all" for all types.'
    )
    
    args = parser.parse_args()
    
    # Create generator instance and run
    generator = MockDataGenerator()
    generator.run(args.insurance_type)

if __name__ == "__main__":
    main() 