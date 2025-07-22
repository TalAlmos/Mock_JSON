#!/usr/bin/env python3
"""
Generate Command for Mock Data Generation

This module provides the GenerateCommand class that implements the command
pattern for generating mock data for specific insurance types.
"""

from typing import List, Dict, Any
from .base_command import BaseCommand
from .generator_context import GeneratorContext


class GenerateCommand(BaseCommand):
    """
    Command for generating mock data for a specific insurance type.
    
    This command creates mock data records for the specified insurance type
    and saves them to the context.
    """
    
    def __init__(self, insurance_type: str, num_records: int = 1):
        """
        Initialize the generate command.
        
        Args:
            insurance_type: Type of insurance to generate data for
            num_records: Number of records to generate
        """
        super().__init__()
        self.insurance_type = insurance_type
        self.num_records = num_records
    
    def execute(self, context: GeneratorContext) -> List[Dict[str, Any]]:
        """
        Execute the generate command.
        
        Args:
            context: GeneratorContext containing all necessary dependencies
            
        Returns:
            List of generated records
        """
        # Validate the command
        errors = self.validate(context)
        if errors:
            raise ValueError(f"Validation failed: {', '.join(errors)}")
        
        # Get the factory from context
        factory = context.get_factory()
        
        # Create generator for the insurance type
        generator = factory.create_generator(self.insurance_type)
        
        # Generate records
        records = []
        for _ in range(self.num_records):
            record = generator.generate_record()
            records.append(record)
        
        # Save records to context
        context.save_records(self.insurance_type, records)
        
        return records
    
    def validate(self, context: GeneratorContext) -> List[str]:
        """
        Validate the generate command.
        
        Args:
            context: GeneratorContext containing all necessary dependencies
            
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        # Check if insurance type is supported
        factory = context.get_factory()
        if not factory.is_supported(self.insurance_type):
            errors.append(f"Unsupported insurance type: {self.insurance_type}")
        
        # Check if num_records is valid
        if self.num_records <= 0:
            errors.append("Number of records must be greater than 0")
        elif self.num_records > 1000:  # Reasonable limit
            errors.append("Number of records cannot exceed 1000")
        
        return errors
    
    def get_description(self) -> str:
        """
        Get a description of what this command does.
        
        Returns:
            String description of the command
        """
        return f"Generate {self.num_records} mock record(s) for {self.insurance_type} insurance" 