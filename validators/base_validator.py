#!/usr/bin/env python3
"""
Base Validator for Mock Data Generation

This module provides the BaseValidator class that serves as the foundation
for all validation operations in the mock data generation system.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from exceptions import ValidationError


class BaseValidator(ABC):
    """
    Base validator class for all validation operations.
    
    This abstract class provides the foundation for all validators
    in the mock data generation system.
    """
    
    def __init__(self):
        """Initialize the base validator."""
        self.validation_errors: List[str] = []
        self.validation_warnings: List[str] = []
    
    @abstractmethod
    def validate(self, data: Any) -> bool:
        """
        Validate the given data.
        
        Args:
            data: Data to validate
            
        Returns:
            True if validation passes, False otherwise
        """
        pass
    
    def add_error(self, error_message: str) -> None:
        """
        Add a validation error.
        
        Args:
            error_message: Description of the validation error
        """
        self.validation_errors.append(error_message)
    
    def add_warning(self, warning_message: str) -> None:
        """
        Add a validation warning.
        
        Args:
            warning_message: Description of the validation warning
        """
        self.validation_warnings.append(warning_message)
    
    def get_errors(self) -> List[str]:
        """
        Get all validation errors.
        
        Returns:
            List of validation error messages
        """
        return self.validation_errors.copy()
    
    def get_warnings(self) -> List[str]:
        """
        Get all validation warnings.
        
        Returns:
            List of validation warning messages
        """
        return self.validation_warnings.copy()
    
    def clear_errors(self) -> None:
        """Clear all validation errors and warnings."""
        self.validation_errors.clear()
        self.validation_warnings.clear()
    
    def has_errors(self) -> bool:
        """
        Check if there are any validation errors.
        
        Returns:
            True if there are validation errors, False otherwise
        """
        return len(self.validation_errors) > 0
    
    def has_warnings(self) -> bool:
        """
        Check if there are any validation warnings.
        
        Returns:
            True if there are validation warnings, False otherwise
        """
        return len(self.validation_warnings) > 0
    
    def raise_if_errors(self, data: Any = None) -> None:
        """
        Raise ValidationError if there are validation errors.
        
        Args:
            data: Optional data that failed validation
            
        Raises:
            ValidationError: If there are validation errors
        """
        if self.has_errors():
            raise ValidationError(
                f"Validation failed with {len(self.validation_errors)} errors",
                self.validation_errors,
                data
            )
    
    def validate_and_raise(self, data: Any) -> bool:
        """
        Validate data and raise ValidationError if validation fails.
        
        Args:
            data: Data to validate
            
        Returns:
            True if validation passes
            
        Raises:
            ValidationError: If validation fails
        """
        is_valid = self.validate(data)
        if not is_valid:
            self.raise_if_errors(data)
        return is_valid
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Get a summary of validation results.
        
        Returns:
            Dictionary containing validation summary
        """
        return {
            "is_valid": not self.has_errors(),
            "error_count": len(self.validation_errors),
            "warning_count": len(self.validation_warnings),
            "errors": self.validation_errors,
            "warnings": self.validation_warnings
        } 