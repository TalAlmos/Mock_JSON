#!/usr/bin/env python3
"""
Generator Context for Command Execution

This module provides the GeneratorContext class that contains all necessary
dependencies for command execution in the mock data generation system.
"""

from typing import Dict, Any, List
from config import Config
from factories.generator_factory import GeneratorFactory
from schema_analyzer import SchemaAnalyzer
from cache.schema_cache import SchemaCache


class GeneratorContext:
    """
    Context for command execution containing all necessary dependencies.
    
    This class provides a centralized way to access all the components
    needed for command execution, following the dependency injection pattern.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the context with configuration.
        
        Args:
            config: Configuration instance with paths and settings
        """
        self.config = config
        self.factory = GeneratorFactory(config)
        self.cache = SchemaCache()
        self.analyzer = SchemaAnalyzer(cache=self.cache)
        self.saved_records = []
    
    def get_factory(self) -> GeneratorFactory:
        """
        Get the generator factory.
        
        Returns:
            GeneratorFactory instance
        """
        return self.factory
    
    def get_analyzer(self) -> SchemaAnalyzer:
        """
        Get the schema analyzer.
        
        Returns:
            SchemaAnalyzer instance
        """
        return self.analyzer
    
    def get_config(self) -> Config:
        """
        Get the configuration.
        
        Returns:
            Config instance
        """
        return self.config
    
    def save_records(self, insurance_type: str, records: List[Dict[str, Any]]) -> None:
        """
        Save generated records to the context.
        
        Args:
            insurance_type: Type of insurance for the records
            records: List of generated records
        """
        for record in records:
            record["insurance_type"] = insurance_type
            self.saved_records.append(record)
    
    def get_saved_records(self) -> List[Dict[str, Any]]:
        """
        Get all saved records.
        
        Returns:
            List of saved records
        """
        return self.saved_records.copy()
    
    def clear_saved_records(self) -> None:
        """Clear all saved records."""
        self.saved_records.clear()
    
    def get_saved_record_count(self) -> int:
        """
        Get the number of saved records.
        
        Returns:
            Number of saved records
        """
        return len(self.saved_records) 