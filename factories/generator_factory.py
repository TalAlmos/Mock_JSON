#!/usr/bin/env python3
"""
Generator Factory for Mock Data Generation

This module provides the GeneratorFactory class for creating generators
for different insurance types using the factory pattern.
"""

from typing import Type
from faker import Faker
from config import Config
from generators.base_generator import BaseGenerator
from generators.registry import GeneratorRegistry
from generators.insurance_generator import InsuranceGenerator
from exceptions import InsuranceTypeNotFoundError, GeneratorError


class GeneratorFactory:
    """
    Factory for creating insurance type generators.
    
    This class provides a centralized way to create generators for different
    insurance types using the factory pattern with dependency injection.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the factory with configuration.
        
        Args:
            config: Configuration instance with paths and settings
        """
        self.config = config
        self.registry = GeneratorRegistry()
        self._register_generators()
    
    def _register_generators(self) -> None:
        """Register all available generators in the registry."""
        # Register the base insurance generator
        self.registry.register("insurance", InsuranceGenerator)
        
        # TODO: Register specific insurance type generators as they are created
        # self.registry.register("travel", TravelGenerator)
        # self.registry.register("vehicleUnited", VehicleGenerator)
        # self.registry.register("mymoney", MyMoneyGenerator)
        # self.registry.register("health", HealthGenerator)
        # self.registry.register("life", LifeGenerator)
        # self.registry.register("business", BusinessGenerator)
    
    def create_generator(self, insurance_type: str) -> BaseGenerator:
        """
        Create a generator for the specified insurance type.
        
        Args:
            insurance_type: String identifier for the insurance type
            
        Returns:
            Generator instance for the specified insurance type
            
        Raises:
            InsuranceTypeNotFoundError: If the insurance type is not supported
        """
        generator_class = self.registry.get_generator(insurance_type)
        if not generator_class:
            available_types = self.get_available_types()
            raise InsuranceTypeNotFoundError(insurance_type, available_types)
        
        # Create Faker instance with Hebrew locale
        faker = Faker(['he_IL'])
        
        # Create and return the generator instance
        return generator_class(faker, self.config)
    
    def get_available_types(self) -> list:
        """
        Get a list of all available insurance types.
        
        Returns:
            List of available insurance type identifiers
        """
        return self.registry.get_available_types()
    
    def is_supported(self, insurance_type: str) -> bool:
        """
        Check if an insurance type is supported.
        
        Args:
            insurance_type: String identifier for the insurance type
            
        Returns:
            True if supported, False otherwise
        """
        return self.registry.is_registered(insurance_type)
    
    def register_generator(self, insurance_type: str, generator_class: Type[BaseGenerator]) -> None:
        """
        Register a new generator for an insurance type.
        
        Args:
            insurance_type: String identifier for the insurance type
            generator_class: Class that inherits from BaseGenerator
        """
        self.registry.register(insurance_type, generator_class)
    
    def unregister_generator(self, insurance_type: str) -> bool:
        """
        Unregister a generator for an insurance type.
        
        Args:
            insurance_type: String identifier for the insurance type
            
        Returns:
            True if unregistered, False if not found
        """
        return self.registry.unregister(insurance_type)
    
    def get_generator_info(self, insurance_type: str) -> dict:
        """
        Get information about a generator for an insurance type.
        
        Args:
            insurance_type: String identifier for the insurance type
            
        Returns:
            Dict containing generator information
        """
        generator_class = self.registry.get_generator(insurance_type)
        if not generator_class:
            return {"error": f"Unknown insurance type: {insurance_type}"}
        
        return {
            "insurance_type": insurance_type,
            "class_name": generator_class.__name__,
            "module": generator_class.__module__,
            "supported": True
        } 