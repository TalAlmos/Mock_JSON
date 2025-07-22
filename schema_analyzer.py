#!/usr/bin/env python3
"""
Schema Analyzer for Mock Data Generation

This module provides the SchemaAnalyzer class for analyzing JSON structures
from example data and extracting schema information.
"""

from typing import Dict, Any, List, Optional
from exceptions import SchemaAnalysisError
from cache.schema_cache import SchemaCache


class SchemaAnalyzer:
    """
    Analyzer for extracting schema information from example data.
    
    This class provides methods for analyzing JSON structures, merging schemas,
    and identifying fields that should preserve their original values.
    """
    
    def __init__(self, cache=None):
        """Initialize the schema analyzer with optional cache."""
        self.cache = cache or SchemaCache()
    
    def analyze_structure(self, examples: List[Dict[str, Any]], cache_key: str = None) -> Dict[str, Any]:
        """
        Analyze structure across multiple examples, using cache if available.
        Args:
            examples: List of example data structures
            cache_key: Optional key to use for caching
        Returns:
            Dict containing the analyzed schema structure
        """
        if not examples:
            return {"type": "object", "properties": {}}

        key = cache_key or str(hash(str(examples)))
        cached = self.cache.get_schema(key)
        if cached is not None:
            return cached

        # Analyze the first example as base structure
        base_structure = self._analyze_structure(examples[0])
        for example in examples[1:]:
            enhanced_structure = self._merge_structures(base_structure, self._analyze_structure(example))
            base_structure = enhanced_structure
        self._add_preserved_field_info(base_structure, examples)
        self.cache.set_schema(key, base_structure)
        return base_structure
    
    def merge_structures(self, structure1: Dict[str, Any], structure2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge two structures to create a more complete schema.
        
        Args:
            structure1: First structure to merge
            structure2: Second structure to merge
            
        Returns:
            Dict containing the merged structure
        """
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
    
    def _add_preserved_field_info(self, structure: Dict[str, Any], examples: List[Dict[str, Any]]) -> None:
        """
        Add information about which fields should preserve their original values.
        
        Args:
            structure: Schema structure to enhance
            examples: List of example data to analyze
        """
        if structure.get("type") == "object":
            properties = structure.get("properties", {})
            for field_name, field_structure in properties.items():
                if self._should_preserve_field(field_name):
                    # Mark this field as preserved
                    field_structure["preserve_original"] = True
                    # Store the original values from examples
                    original_values = self._extract_original_values(field_name, examples)
                    if original_values:
                        field_structure["original_values"] = original_values
                
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
    
    def _analyze_structure(self, obj: Any, max_depth: int = 10) -> Dict[str, Any]:
        """
        Recursively analyze the structure of an object to determine types.
        
        Args:
            obj: Object to analyze
            max_depth: Maximum recursion depth
            
        Returns:
            Dict containing the analyzed structure
        """
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
    
    def _should_preserve_field(self, field_name: str) -> bool:
        """
        Check if a field should preserve its original value.
        
        Args:
            field_name: Name of the field to check
            
        Returns:
            True if field should be preserved, False otherwise
        """
        preserve_fields = {
            'status', 'message', 'transId', 'entity',  # API response metadata
            'id',  # Entity/API identifiers
            'requiredRenewal', 'isExpired', 'isActive', 'isSmart', 'isKlasi', 'isRiziko', 'isCopyPolicyDoc', 'isPaila', 'isIndependent', 'isNew',  # Boolean flags
            'sign',  # Special characters like '%'
            'eSite',  # URLs that might be None
            'totalPayments',  # Empty strings that should remain empty
            'paymentNo',  # Fields that should remain null
            'yieldBeginningYear', 'lastDeposit', 'depositedThisYear', 'availableWithdraw', 'withdrawDate', 'yieldFromYearBeginningTotal',  # Nullable fields
            'fromDeposit', 'fromSaving', 'yieldUpdateDate', 'dailyYieldUpdateDate', 'hasProfitsShare', 'updateTo', 'dailyUpdateTo', 'tsuotPopup'  # More nullable fields
        }
        return field_name in preserve_fields
    
    def _extract_original_values(self, field_name: str, examples: List[Dict[str, Any]]) -> List[Any]:
        """
        Extract original values for a field from all examples.
        
        Args:
            field_name: Name of the field to extract
            examples: List of example data
            
        Returns:
            List of original values for the field
        """
        values = []
        for example in examples:
            if isinstance(example, dict) and field_name in example:
                value = example[field_name]
                if value not in values:
                    values.append(value)
        return values
    
    def _extract_nested_value(self, obj: Any, field_name: str) -> Any:
        """
        Extract a nested field value from an object.
        
        Args:
            obj: Object to extract from
            field_name: Name of the field to extract
            
        Returns:
            Extracted value or None if not found
        """
        if isinstance(obj, dict):
            return obj.get(field_name)
        return None 