#!/usr/bin/env python3
"""
Base Generator Interface for Mock Data Generation

This module provides the abstract base class for all insurance type generators,
defining the common interface and dependency injection pattern.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from faker import Faker
from config import Config


class BaseGenerator(ABC):
    """
    Abstract base class for all insurance type generators.
    
    This class defines the common interface that all generators must implement,
    providing dependency injection for Faker and Config instances.
    """
    
    def __init__(self, faker: Faker, config: Config):
        """
        Initialize the generator with dependencies.
        
        Args:
            faker: Faker instance for generating realistic data
            config: Configuration instance with paths and settings
        """
        self.faker = faker
        self.config = config
    
    @abstractmethod
    def generate_record(self) -> Dict[str, Any]:
        """
        Generate a single mock record for the insurance type.
        
        Returns:
            Dict containing the generated mock data record
        """
        pass
    
    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """
        Get the schema definition for this insurance type.
        
        Returns:
            Dict containing the schema structure
        """
        pass
    
    def generate_multiple_records(self, count: int) -> List[Dict[str, Any]]:
        """
        Generate multiple mock records.
        
        Args:
            count: Number of records to generate
            
        Returns:
            List of generated mock data records
        """
        return [self.generate_record() for _ in range(count)]
    
    def validate_record(self, record: Dict[str, Any]) -> List[str]:
        """
        Validate a generated record against the schema.
        
        Args:
            record: The record to validate
            
        Returns:
            List of validation error messages (empty if valid)
        """
        # Default implementation - can be overridden by subclasses
        errors = []
        schema = self.get_schema()
        
        # Basic validation - check required fields
        if 'required_fields' in schema:
            for field in schema['required_fields']:
                if field not in record:
                    errors.append(f"Missing required field: {field}")
        
        return errors
    
    def get_insurance_type(self) -> str:
        """
        Get the insurance type identifier for this generator.
        
        Returns:
            String identifier for the insurance type
        """
        # Default implementation - subclasses should override
        return self.__class__.__name__.lower().replace('generator', '')
    
    def get_preserve_fields(self) -> set:
        """
        Get the fields that should preserve original values.
        
        Returns:
            Set of field names that should not be anonymized
        """
        return self.config.preserve_fields.copy() 