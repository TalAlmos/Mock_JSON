#!/usr/bin/env python3
"""
Generator Registry for Dynamic Generator Management

This module provides a registry pattern for managing different insurance type generators,
allowing dynamic registration and retrieval of generators.
"""

from typing import Dict, Type, Optional
from .base_generator import BaseGenerator
from exceptions import GeneratorError


class GeneratorRegistry:
    """
    Registry for managing insurance type generators.
    
    This class provides a centralized way to register and retrieve generators
    for different insurance types using a dictionary-based registry pattern.
    """
    
    def __init__(self):
        """Initialize an empty registry."""
        self._generators: Dict[str, Type[BaseGenerator]] = {}
    
    def register(self, insurance_type: str, generator_class: Type[BaseGenerator]) -> None:
        """
        Register a generator class for a specific insurance type.
        
        Args:
            insurance_type: String identifier for the insurance type
            generator_class: Class that inherits from BaseGenerator
        """
        if not issubclass(generator_class, BaseGenerator):
            raise GeneratorError(
                f"Generator class must inherit from BaseGenerator: {generator_class}",
                generator_type=str(generator_class),
                operation="register"
            )
        
        self._generators[insurance_type] = generator_class
    
    def get_generator(self, insurance_type: str) -> Optional[Type[BaseGenerator]]:
        """
        Get the generator class for a specific insurance type.
        
        Args:
            insurance_type: String identifier for the insurance type
            
        Returns:
            Generator class if found, None otherwise
        """
        return self._generators.get(insurance_type)
    
    def get_available_types(self) -> list:
        """
        Get a list of all registered insurance types.
        
        Returns:
            List of registered insurance type identifiers
        """
        return list(self._generators.keys())
    
    def is_registered(self, insurance_type: str) -> bool:
        """
        Check if a generator is registered for the given insurance type.
        
        Args:
            insurance_type: String identifier for the insurance type
            
        Returns:
            True if registered, False otherwise
        """
        return insurance_type in self._generators
    
    def unregister(self, insurance_type: str) -> bool:
        """
        Unregister a generator for a specific insurance type.
        
        Args:
            insurance_type: String identifier for the insurance type
            
        Returns:
            True if unregistered, False if not found
        """
        if insurance_type in self._generators:
            del self._generators[insurance_type]
            return True
        return False
    
    def clear(self) -> None:
        """Clear all registered generators."""
        self._generators.clear()
    
    def count(self) -> int:
        """
        Get the number of registered generators.
        
        Returns:
            Number of registered generators
        """
        return len(self._generators) 