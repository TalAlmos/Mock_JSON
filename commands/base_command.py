#!/usr/bin/env python3
"""
Base Command Interface for Mock Data Generation

This module provides the abstract base class for all commands in the
mock data generation system using the command pattern.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseCommand(ABC):
    """
    Abstract base class for all commands.
    
    This class defines the common interface that all commands must implement,
    providing a consistent way to execute different operations.
    """
    
    def __init__(self):
        """Initialize the command."""
        pass
    
    @abstractmethod
    def execute(self, context: 'GeneratorContext') -> Any:
        """
        Execute the command with the given context.
        
        Args:
            context: GeneratorContext containing all necessary dependencies
            
        Returns:
            Result of the command execution
        """
        pass
    
    def get_description(self) -> str:
        """
        Get a description of what this command does.
        
        Returns:
            String description of the command
        """
        return self.__class__.__name__
    
    def validate(self, context: 'GeneratorContext') -> List[str]:
        """
        Validate the command before execution.
        
        Args:
            context: GeneratorContext containing all necessary dependencies
            
        Returns:
            List of validation error messages (empty if valid)
        """
        return [] 