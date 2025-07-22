#!/usr/bin/env python3
"""
Data Validator for Mock Data Generation

This module provides the DataValidator class for validating data integrity,
consistency, and business rules.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from .base_validator import BaseValidator


class DataValidator(BaseValidator):
    """
    Validator for data integrity and business rules.
    
    This class validates data integrity, consistency, and business rules,
    ensuring generated data meets quality standards.
    """
    
    def __init__(self):
        """Initialize the data validator."""
        super().__init__()
    
    def validate(self, data: Any) -> bool:
        """
        Validate data integrity and business rules.
        
        Args:
            data: Data to validate
            
        Returns:
            True if validation passes, False otherwise
        """
        self.clear_errors()
        
        if isinstance(data, dict):
            return self._validate_dict(data)
        elif isinstance(data, list):
            return self._validate_list(data)
        else:
            return self._validate_primitive(data)
    
    def _validate_dict(self, data: Dict[str, Any]) -> bool:
        """Validate dictionary data."""
        is_valid = True
        
        # Check for required fields in insurance data
        if "insurance_type" in data:
            is_valid &= self._validate_insurance_type(data["insurance_type"])
        
        if "policy_id" in data:
            is_valid &= self._validate_policy_id(data["policy_id"])
        
        if "start_date" in data:
            is_valid &= self._validate_date(data["start_date"])
        
        if "end_date" in data:
            is_valid &= self._validate_date(data["end_date"])
        
        # Validate date consistency
        if "start_date" in data and "end_date" in data:
            is_valid &= self._validate_date_range(data["start_date"], data["end_date"])
        
        # Validate monetary values
        for key, value in data.items():
            if "amount" in key.lower() or "sum" in key.lower() or "value" in key.lower():
                if isinstance(value, dict) and "value" in value:
                    is_valid &= self._validate_monetary_value(value["value"])
        
        # Validate nested objects
        for key, value in data.items():
            if isinstance(value, dict):
                if not self._validate_dict(value):
                    is_valid = False
            elif isinstance(value, list):
                if not self._validate_list(value):
                    is_valid = False
        
        return is_valid
    
    def _validate_list(self, data: List[Any]) -> bool:
        """Validate list data."""
        if not data:
            return True  # Empty lists are valid
        
        is_valid = True
        for i, item in enumerate(data):
            if isinstance(item, dict):
                if not self._validate_dict(item):
                    is_valid = False
            elif isinstance(item, list):
                if not self._validate_list(item):
                    is_valid = False
            else:
                if not self._validate_primitive(item):
                    is_valid = False
        
        return is_valid
    
    def _validate_primitive(self, data: Any) -> bool:
        """Validate primitive data types."""
        if data is None:
            return True
        
        if isinstance(data, (str, int, float, bool)):
            return True
        
        self.add_error(f"Unexpected data type: {type(data).__name__}")
        return False
    
    def _validate_insurance_type(self, insurance_type: str) -> bool:
        """Validate insurance type."""
        valid_types = [
            "health", "vehicleUnited", "travel", "life", "business", 
            "dental", "dira", "mymoney", "other"
        ]
        
        if insurance_type not in valid_types:
            self.add_error(f"Invalid insurance type: {insurance_type}")
            return False
        
        return True
    
    def _validate_policy_id(self, policy_id: str) -> bool:
        """Validate policy ID format."""
        if not isinstance(policy_id, str):
            self.add_error("Policy ID must be a string")
            return False
        
        if not policy_id.strip():
            self.add_error("Policy ID cannot be empty")
            return False
        
        # Check for common policy ID patterns
        if not (policy_id.startswith("POL-") or 
                policy_id.startswith("001-") or 
                policy_id.startswith("007-") or
                policy_id.startswith("570-")):
            self.add_warning(f"Policy ID '{policy_id}' does not match expected format")
        
        return True
    
    def _validate_date(self, date_str: str) -> bool:
        """Validate date format."""
        if not isinstance(date_str, str):
            self.add_error("Date must be a string")
            return False
        
        if not date_str.strip():
            self.add_error("Date cannot be empty")
            return False
        
        # Try to parse the date
        try:
            # Support multiple date formats
            date_formats = [
                "%d.%m.%Y",  # DD.MM.YYYY
                "%d.%m.%y",  # DD.MM.YY
                "%d/%m/%Y",  # DD/MM/YYYY
                "%Y-%m-%d",  # YYYY-MM-DD
                "%Y-%m-%dT%H:%M:%S"  # ISO format
            ]
            
            parsed = False
            for fmt in date_formats:
                try:
                    datetime.strptime(date_str, fmt)
                    parsed = True
                    break
                except ValueError:
                    continue
            
            if not parsed:
                self.add_error(f"Invalid date format: {date_str}")
                return False
                
        except Exception as e:
            self.add_error(f"Date parsing error: {e}")
            return False
        
        return True
    
    def _validate_date_range(self, start_date: str, end_date: str) -> bool:
        """Validate that start date is before end date."""
        try:
            # Parse dates using common formats
            date_formats = ["%d.%m.%Y", "%d.%m.%y", "%d/%m/%Y", "%Y-%m-%d"]
            
            start_dt = None
            end_dt = None
            
            for fmt in date_formats:
                try:
                    start_dt = datetime.strptime(start_date, fmt)
                    break
                except ValueError:
                    continue
            
            for fmt in date_formats:
                try:
                    end_dt = datetime.strptime(end_date, fmt)
                    break
                except ValueError:
                    continue
            
            if start_dt and end_dt:
                if start_dt >= end_dt:
                    self.add_error(f"Start date {start_date} must be before end date {end_date}")
                    return False
            
        except Exception as e:
            self.add_warning(f"Could not validate date range: {e}")
        
        return True
    
    def _validate_monetary_value(self, value: Any) -> bool:
        """Validate monetary values."""
        if not isinstance(value, (int, float)):
            self.add_error("Monetary value must be a number")
            return False
        
        if value < 0:
            self.add_warning("Monetary value is negative")
        
        if value > 1000000000:  # 1 billion
            self.add_warning("Monetary value seems unusually high")
        
        return True
    
    def validate_data_consistency(self, data: Dict[str, Any]) -> bool:
        """
        Validate data consistency across related fields.
        
        Args:
            data: Data to validate for consistency
            
        Returns:
            True if data is consistent, False otherwise
        """
        self.clear_errors()
        
        if not isinstance(data, dict):
            self.add_error("Data must be a dictionary")
            return False
        
        # Check for logical inconsistencies
        if "status" in data and "isActive" in data:
            if data["status"] == "active" and not data["isActive"]:
                self.add_error("Status is 'active' but isActive is False")
            elif data["status"] == "inactive" and data["isActive"]:
                self.add_error("Status is 'inactive' but isActive is True")
        
        # Check for required field dependencies
        if "end_date" in data and "start_date" not in data:
            self.add_warning("End date present but start date missing")
        
        if "policy_id" in data and "insurance_type" not in data:
            self.add_warning("Policy ID present but insurance type missing")
        
        return not self.has_errors()
    
    def validate_data_completeness(self, data: Dict[str, Any], required_fields: List[str]) -> bool:
        """
        Validate that all required fields are present.
        
        Args:
            data: Data to validate
            required_fields: List of required field names
            
        Returns:
            True if all required fields are present, False otherwise
        """
        self.clear_errors()
        
        if not isinstance(data, dict):
            self.add_error("Data must be a dictionary")
            return False
        
        missing_fields = []
        for field in required_fields:
            if field not in data:
                missing_fields.append(field)
        
        if missing_fields:
            self.add_error(f"Missing required fields: {', '.join(missing_fields)}")
            return False
        
        return True
    
    def validate_data_quality(self, data: Any) -> bool:
        """
        Validate overall data quality.
        
        Args:
            data: Data to validate
            
        Returns:
            True if data quality is acceptable, False otherwise
        """
        self.clear_errors()
        
        if data is None:
            self.add_error("Data cannot be null")
            return False
        
        if isinstance(data, dict) and not data:
            self.add_warning("Data is an empty dictionary")
        
        if isinstance(data, list) and not data:
            self.add_warning("Data is an empty list")
        
        # Check for common data quality issues
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and not value.strip():
                    self.add_warning(f"Empty string value for field '{key}'")
                
                if isinstance(value, dict) and not value:
                    self.add_warning(f"Empty object for field '{key}'")
        
        return not self.has_errors() 