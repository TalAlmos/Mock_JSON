#!/usr/bin/env python3
"""
Custom Exceptions for Mock Data Generation

This module provides custom exception classes for the mock data generation system,
providing more specific error handling and better error messages.
"""


class MockDataGenerationError(Exception):
    """
    Base exception for all mock data generation errors.
    
    This is the parent class for all exceptions in the mock data generation system.
    """
    
    def __init__(self, message: str, details: dict = None):
        """
        Initialize the exception.
        
        Args:
            message: Human-readable error message
            details: Optional dictionary with additional error details
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}
    
    def __str__(self) -> str:
        """Return string representation of the exception."""
        if self.details:
            return f"{self.message} - Details: {self.details}"
        return self.message


class SchemaAnalysisError(MockDataGenerationError):
    """
    Exception raised when schema analysis fails.
    
    This exception is raised when there are issues with analyzing
    JSON structures or extracting schema information.
    """
    
    def __init__(self, message: str, schema_data: dict = None):
        """
        Initialize the schema analysis error.
        
        Args:
            message: Human-readable error message
            schema_data: Optional schema data that caused the error
        """
        details = {"schema_data": schema_data} if schema_data else {}
        super().__init__(message, details)
        self.schema_data = schema_data


class InsuranceTypeNotFoundError(MockDataGenerationError):
    """
    Exception raised when an insurance type is not found or supported.
    
    This exception is raised when trying to generate data for an
    insurance type that is not registered or supported.
    """
    
    def __init__(self, insurance_type: str, available_types: list = None):
        """
        Initialize the insurance type not found error.
        
        Args:
            insurance_type: The insurance type that was not found
            available_types: Optional list of available insurance types
        """
        message = f"Insurance type '{insurance_type}' not found or not supported"
        if available_types:
            message += f". Available types: {', '.join(available_types)}"
        
        details = {
            "requested_type": insurance_type,
            "available_types": available_types or []
        }
        
        super().__init__(message, details)
        self.insurance_type = insurance_type
        self.available_types = available_types or []


class ConfigurationError(MockDataGenerationError):
    """
    Exception raised when there are configuration issues.
    
    This exception is raised when there are problems with the
    configuration settings or paths.
    """
    
    def __init__(self, message: str, config_path: str = None):
        """
        Initialize the configuration error.
        
        Args:
            message: Human-readable error message
            config_path: Optional path to the configuration file
        """
        details = {"config_path": config_path} if config_path else {}
        super().__init__(message, details)
        self.config_path = config_path


class ValidationError(MockDataGenerationError):
    """
    Exception raised when data validation fails.
    
    This exception is raised when generated data fails validation
    against the expected schema.
    """
    
    def __init__(self, message: str, validation_errors: list = None, data: dict = None):
        """
        Initialize the validation error.
        
        Args:
            message: Human-readable error message
            validation_errors: Optional list of specific validation errors
            data: Optional data that failed validation
        """
        details = {
            "validation_errors": validation_errors or [],
            "data": data
        }
        super().__init__(message, details)
        self.validation_errors = validation_errors or []
        self.data = data


class GeneratorError(MockDataGenerationError):
    """
    Exception raised when generator operations fail.
    
    This exception is raised when there are issues with the
    generator classes or their operations.
    """
    
    def __init__(self, message: str, generator_type: str = None, operation: str = None):
        """
        Initialize the generator error.
        
        Args:
            message: Human-readable error message
            generator_type: Optional type of generator that failed
            operation: Optional operation that failed
        """
        details = {
            "generator_type": generator_type,
            "operation": operation
        }
        super().__init__(message, details)
        self.generator_type = generator_type
        self.operation = operation 