#!/usr/bin/env python3
"""
Schema Validator for Mock Data Generation

This module provides the SchemaValidator class for validating data
against JSON schemas and structure definitions.
"""

from typing import Dict, Any, List, Optional, Union
from .base_validator import BaseValidator


class SchemaValidator(BaseValidator):
    """
    Validator for JSON schema validation.
    
    This class validates data against JSON schemas and structure definitions,
    ensuring data conforms to expected formats and types.
    """
    
    def __init__(self):
        """Initialize the schema validator."""
        super().__init__()
    
    def validate(self, data: Any, schema: Dict[str, Any]) -> bool:
        """
        Validate data against a schema.
        
        Args:
            data: Data to validate
            schema: Schema definition to validate against
            
        Returns:
            True if validation passes, False otherwise
        """
        self.clear_errors()
        return self._validate_against_schema(data, schema)
    
    def _validate_against_schema(self, data: Any, schema: Dict[str, Any], path: str = "") -> bool:
        """
        Recursively validate data against schema.
        
        Args:
            data: Data to validate
            schema: Schema definition
            path: Current validation path for error reporting
            
        Returns:
            True if validation passes, False otherwise
        """
        schema_type = schema.get("type", "string")
        
        if schema_type == "object":
            return self._validate_object(data, schema, path)
        elif schema_type == "array":
            return self._validate_array(data, schema, path)
        elif schema_type == "string":
            return self._validate_string(data, schema, path)
        elif schema_type == "number":
            return self._validate_number(data, schema, path)
        elif schema_type == "boolean":
            return self._validate_boolean(data, schema, path)
        elif schema_type == "null":
            return self._validate_null(data, schema, path)
        else:
            # Unknown type, treat as valid
            return True
    
    def _validate_object(self, data: Any, schema: Dict[str, Any], path: str) -> bool:
        """Validate object data against object schema."""
        if not isinstance(data, dict):
            self.add_error(f"{path}: Expected object, got {type(data).__name__}")
            return False
        
        properties = schema.get("properties", {})
        required_fields = schema.get("required", [])
        
        # Check required fields
        for field in required_fields:
            if field not in data:
                self.add_error(f"{path}: Missing required field '{field}'")
        
        # Validate each property
        is_valid = True
        for field_name, field_schema in properties.items():
            field_path = f"{path}.{field_name}" if path else field_name
            
            if field_name in data:
                if not self._validate_against_schema(data[field_name], field_schema, field_path):
                    is_valid = False
            elif field_name in required_fields:
                is_valid = False
        
        return is_valid and not self.has_errors()
    
    def _validate_array(self, data: Any, schema: Dict[str, Any], path: str) -> bool:
        """Validate array data against array schema."""
        if not isinstance(data, list):
            self.add_error(f"{path}: Expected array, got {type(data).__name__}")
            return False
        
        items_schema = schema.get("items", {"type": "string"})
        min_items = schema.get("minItems", 0)
        max_items = schema.get("maxItems")
        
        # Check array length constraints
        if len(data) < min_items:
            self.add_error(f"{path}: Array has {len(data)} items, minimum is {min_items}")
            return False
        
        if max_items and len(data) > max_items:
            self.add_error(f"{path}: Array has {len(data)} items, maximum is {max_items}")
            return False
        
        # Validate each array item
        is_valid = True
        for i, item in enumerate(data):
            item_path = f"{path}[{i}]"
            if not self._validate_against_schema(item, items_schema, item_path):
                is_valid = False
        
        return is_valid
    
    def _validate_string(self, data: Any, schema: Dict[str, Any], path: str) -> bool:
        """Validate string data against string schema."""
        if not isinstance(data, str):
            self.add_error(f"{path}: Expected string, got {type(data).__name__}")
            return False
        
        # Check string constraints
        min_length = schema.get("minLength")
        max_length = schema.get("maxLength")
        pattern = schema.get("pattern")
        enum = schema.get("enum")
        
        if min_length and len(data) < min_length:
            self.add_error(f"{path}: String length {len(data)} is less than minimum {min_length}")
            return False
        
        if max_length and len(data) > max_length:
            self.add_error(f"{path}: String length {len(data)} is greater than maximum {max_length}")
            return False
        
        if pattern:
            import re
            if not re.match(pattern, data):
                self.add_error(f"{path}: String does not match pattern '{pattern}'")
                return False
        
        if enum and data not in enum:
            self.add_error(f"{path}: Value '{data}' is not in allowed values {enum}")
            return False
        
        return True
    
    def _validate_number(self, data: Any, schema: Dict[str, Any], path: str) -> bool:
        """Validate number data against number schema."""
        if not isinstance(data, (int, float)):
            self.add_error(f"{path}: Expected number, got {type(data).__name__}")
            return False
        
        # Check number constraints
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        multiple_of = schema.get("multipleOf")
        
        if minimum is not None and data < minimum:
            self.add_error(f"{path}: Value {data} is less than minimum {minimum}")
            return False
        
        if maximum is not None and data > maximum:
            self.add_error(f"{path}: Value {data} is greater than maximum {maximum}")
            return False
        
        if multiple_of and data % multiple_of != 0:
            self.add_error(f"{path}: Value {data} is not a multiple of {multiple_of}")
            return False
        
        return True
    
    def _validate_boolean(self, data: Any, schema: Dict[str, Any], path: str) -> bool:
        """Validate boolean data against boolean schema."""
        if not isinstance(data, bool):
            self.add_error(f"{path}: Expected boolean, got {type(data).__name__}")
            return False
        return True
    
    def _validate_null(self, data: Any, schema: Dict[str, Any], path: str) -> bool:
        """Validate null data against null schema."""
        if data is not None:
            self.add_error(f"{path}: Expected null, got {type(data).__name__}")
            return False
        return True
    
    def validate_schema_structure(self, schema: Dict[str, Any]) -> bool:
        """
        Validate that a schema definition is well-formed.
        
        Args:
            schema: Schema definition to validate
            
        Returns:
            True if schema is valid, False otherwise
        """
        self.clear_errors()
        
        if not isinstance(schema, dict):
            self.add_error("Schema must be a dictionary")
            return False
        
        if "type" not in schema:
            self.add_error("Schema must have a 'type' field")
            return False
        
        schema_type = schema["type"]
        valid_types = ["object", "array", "string", "number", "boolean", "null"]
        
        if schema_type not in valid_types:
            self.add_error(f"Invalid schema type: {schema_type}")
            return False
        
        # Validate object-specific fields
        if schema_type == "object":
            if "properties" in schema and not isinstance(schema["properties"], dict):
                self.add_error("Object schema 'properties' must be a dictionary")
                return False
            
            if "required" in schema:
                if not isinstance(schema["required"], list):
                    self.add_error("Object schema 'required' must be a list")
                    return False
                
                properties = schema.get("properties", {})
                for required_field in schema["required"]:
                    if required_field not in properties:
                        self.add_warning(f"Required field '{required_field}' not defined in properties")
        
        # Validate array-specific fields
        elif schema_type == "array":
            if "items" not in schema:
                self.add_error("Array schema must have 'items' field")
                return False
            
            # Recursively validate items schema
            if not self.validate_schema_structure(schema["items"]):
                return False
        
        return not self.has_errors()
    
    def get_schema_errors(self, schema: Dict[str, Any]) -> List[str]:
        """
        Get validation errors for a schema definition.
        
        Args:
            schema: Schema definition to validate
            
        Returns:
            List of validation error messages
        """
        self.validate_schema_structure(schema)
        return self.get_errors() 