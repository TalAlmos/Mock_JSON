#!/usr/bin/env python3
"""
Insurance Generator for Mock Data Generation

This module provides the InsuranceGenerator class that implements the BaseGenerator
interface for generating insurance-specific mock data.
"""

import random
from typing import Dict, Any, List
from datetime import datetime, timedelta
from faker import Faker
from config import Config
from .base_generator import BaseGenerator
from exceptions import GeneratorError, ValidationError


class InsuranceGenerator(BaseGenerator):
    """
    Generator for insurance-specific mock data.
    
    This class implements the BaseGenerator interface and provides
    methods for generating realistic insurance records.
    """
    
    def __init__(self, faker: Faker, config: Config):
        """Initialize the insurance generator."""
        super().__init__(faker, config)
    
    def generate_record(self) -> Dict[str, Any]:
        """
        Generate a single insurance record.
        
        Returns:
            Dict containing the generated insurance record
        """
        # This is a placeholder - will be implemented with specific insurance type logic
        return {
            "insurance_type": "general",
            "policy_id": f"POL-{random.randint(100000, 999999)}",
            "start_date": self.faker.date(),
            "end_date": self.faker.date(),
            "status": "active"
        }
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Get the schema definition for insurance records.
        
        Returns:
            Dict containing the schema structure
        """
        return {
            "type": "object",
            "properties": {
                "insurance_type": {"type": "string"},
                "policy_id": {"type": "string"},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
                "status": {"type": "string"}
            },
            "required_fields": ["insurance_type", "policy_id", "start_date", "end_date", "status"]
        }
    
    def _generate_base_fields(self, schema: Dict[str, Any], dates: Dict[str, str]) -> Dict[str, Any]:
        """
        Generate basic fields for an insurance record.
        
        Args:
            schema: Schema definition for the record
            dates: Dictionary containing start and end dates
            
        Returns:
            Dict containing basic fields
        """
        base_record = {}
        
        for field_name, field_def in schema.get("properties", {}).items():
            if field_def.get("type") == "string":
                if "date" in field_name.lower():
                    if "end" in field_name.lower():
                        base_record[field_name] = dates.get("end_date", self.faker.date())
                    else:
                        base_record[field_name] = dates.get("start_date", self.faker.date())
                else:
                    base_record[field_name] = self._generate_mock_string(field_name)
            elif field_def.get("type") == "number":
                base_record[field_name] = self._generate_mock_number(field_name)
            elif field_def.get("type") == "boolean":
                base_record[field_name] = random.choice([True, False])
        
        return base_record
    
    def _generate_complex_fields(self, schema: Dict[str, Any], dates: Dict[str, str]) -> Dict[str, Any]:
        """
        Generate complex fields for an insurance record.
        
        Args:
            schema: Schema definition for the record
            dates: Dictionary containing start and end dates
            
        Returns:
            Dict containing complex fields
        """
        complex_fields = {}
        
        for field_name, field_def in schema.get("properties", {}).items():
            if field_def.get("type") == "object":
                complex_fields[field_name] = self._generate_mock_object(field_def, field_name)
            elif field_def.get("type") == "array":
                complex_fields[field_name] = self._generate_mock_array(field_def, field_name)
        
        return complex_fields
    
    def _merge_records(self, base_record: Dict[str, Any], complex_fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge base and complex fields into a complete record.
        
        Args:
            base_record: Dictionary containing basic fields
            complex_fields: Dictionary containing complex fields
            
        Returns:
            Dict containing the complete merged record
        """
        merged_record = base_record.copy()
        merged_record.update(complex_fields)
        return merged_record
    
    def _generate_mock_string(self, field_name: str) -> str:
        """Generate appropriate mock string based on field name."""
        field_lower = field_name.lower()
        
        if any(word in field_lower for word in ['name', 'שם']):
            return self.faker.name()
        elif any(word in field_lower for word in ['email', 'אימייל']):
            return self.faker.email()
        elif any(word in field_lower for word in ['phone', 'טלפון']):
            return self.faker.phone_number()
        elif any(word in field_lower for word in ['policy', 'פוליסה']):
            return f"POL-{random.randint(100000, 999999)}"
        elif any(word in field_lower for word in ['currency', 'מטבע']):
            return random.choice(['₪', '$', '€', '£'])
        elif any(word in field_lower for word in ['status', 'סטטוס']):
            return random.choice(['active', 'inactive', 'pending', 'expired'])
        else:
            return f"Mock_{field_name}_{random.randint(1000, 9999)}"
    
    def _generate_mock_number(self, field_name: str) -> float:
        """Generate appropriate mock number based on field name."""
        field_lower = field_name.lower()
        
        if any(word in field_lower for word in ['amount', 'sum', 'value', 'סכום', 'ערך']):
            return round(random.uniform(1000, 1000000), 2)
        elif any(word in field_lower for word in ['percent', 'percentage', 'אחוז']):
            return round(random.uniform(0, 100), 2)
        else:
            return random.randint(1, 1000)
    
    def _generate_mock_object(self, schema: Dict[str, Any], field_name: str) -> Dict[str, Any]:
        """Generate mock object based on schema."""
        properties = schema.get("properties", {})
        mock_object = {}
        
        for prop_name, prop_schema in properties.items():
            mock_object[prop_name] = self._generate_mock_value(prop_schema, prop_name)
        
        return mock_object
    
    def _generate_mock_array(self, schema: Dict[str, Any], field_name: str) -> List[Any]:
        """Generate mock array based on schema."""
        items_schema = schema.get("items", {"type": "string"})
        array_length = random.randint(1, 5)
        
        return [self._generate_mock_value(items_schema, field_name) for _ in range(array_length)]
    
    def _generate_mock_value(self, schema: Dict[str, Any], field_name: str = "") -> Any:
        """Generate a mock value based on schema definition."""
        schema_type = schema.get("type", "string")
        
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
    
    def generate_realistic_dates(self) -> Dict[str, str]:
        """Generate realistic policy dates based on today's date."""
        today = datetime(2025, 7, 7)
        
        days_ago = random.randint(1, 180)
        start_date = today - timedelta(days=days_ago)
        end_date = start_date + timedelta(days=364)
        
        return {
            "start_date": start_date.strftime("%d.%m.%Y"),
            "end_date": end_date.strftime("%d.%m.%Y"),
            "start_date_short": start_date.strftime("%d.%m.%y"),
            "end_date_short": end_date.strftime("%d.%m.%y")
        } 