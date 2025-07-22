#!/usr/bin/env python3
"""
List Types Command for Mock Data Generation

This module provides the ListTypesCommand class that implements the command
pattern for listing available insurance types.
"""

from typing import List, Dict, Any
from .base_command import BaseCommand
from .generator_context import GeneratorContext


class ListTypesCommand(BaseCommand):
    """
    Command for listing available insurance types.
    
    This command retrieves and returns information about all available
    insurance types that can be used for mock data generation.
    """
    
    def __init__(self):
        """Initialize the list types command."""
        super().__init__()
    
    def execute(self, context: GeneratorContext) -> List[Dict[str, Any]]:
        """
        Execute the list types command.
        
        Args:
            context: GeneratorContext containing all necessary dependencies
            
        Returns:
            List of available insurance types with their information
        """
        # Get the factory from context
        factory = context.get_factory()
        
        # Get available types
        available_types = factory.get_available_types()
        
        # Get detailed information for each type
        type_info = []
        for insurance_type in available_types:
            info = factory.get_generator_info(insurance_type)
            type_info.append(info)
        
        return type_info
    
    def get_description(self) -> str:
        """
        Get a description of what this command does.
        
        Returns:
            String description of the command
        """
        return "List all available insurance types for mock data generation" 