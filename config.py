#!/usr/bin/env python3
"""
Configuration management for Mock Data Generator

This module provides centralized configuration management for the mock data generator,
extracting hardcoded values from the original MockDataGenerator class.
"""

from pathlib import Path
from typing import Set, Dict, Any, Optional
import yaml
from exceptions import ConfigurationError


class Config:
    """Configuration class for Mock Data Generator."""
    
    def __init__(self):
        """Initialize configuration with default values."""
        # Use actual local paths
        self.swagger_path = Path("/Users/talalmos/Documents/Code/Projects/Mock_JSON/data/swagger")
        self.examples_path = Path("/Users/talalmos/Documents/Code/Projects/Mock_JSON/data/examples")
        self.output_path = Path("/Users/talalmos/Documents/Code/Projects/Mock_JSON/data/mock_output")
        
        # Ensure output directory exists
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # Fields that should preserve original values (not anonymized)
        self.preserve_fields = {
            'status', 'message', 'transId', 'entity',  # API response metadata
            'id',  # Entity/API identifiers like "vehicleUnited", "life", "travel"
            'requiredRenewal', 'isExpired', 'isActive', 'isSmart', 'isKlasi', 'isRiziko', 'isCopyPolicyDoc', 'isPaila', 'isIndependent', 'isNew',  # Boolean flags
            'sign',  # Special characters like '%'
            'eSite',  # URLs that might be None
            'totalPayments',  # Empty strings that should remain empty
            'paymentNo',  # Fields that should remain null
            'yieldBeginningYear', 'lastDeposit', 'depositedThisYear', 'availableWithdraw', 'withdrawDate', 'yieldFromYearBeginningTotal',  # Nullable fields
            'fromDeposit', 'fromSaving', 'yieldUpdateDate', 'dailyYieldUpdateDate', 'hasProfitsShare', 'updateTo', 'dailyUpdateTo', 'tsuotPopup'  # More nullable fields
        }
    
    @classmethod
    def from_yaml(cls, config_data: Dict[str, Any]) -> 'Config':
        """Create Config instance from YAML data."""
        config = cls()
        
        # Update paths if provided
        if 'paths' in config_data:
            paths = config_data['paths']
            if 'swagger' in paths:
                config.swagger_path = Path(paths['swagger'])
            if 'examples' in paths:
                config.examples_path = Path(paths['examples'])
            if 'output' in paths:
                config.output_path = Path(paths['output'])
                config.output_path.mkdir(parents=True, exist_ok=True)
        
        # Update preserve fields if provided
        if 'preserve_fields' in config_data:
            config.preserve_fields = set(config_data['preserve_fields'])
        
        return config
    
    @classmethod
    def from_yaml_file(cls, file_path: str) -> 'Config':
        """Create Config instance from YAML file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        return cls.from_yaml(config_data)
    
    def validate(self) -> None:
        """Validate configuration settings."""
        if not self.swagger_path.exists():
            raise ConfigurationError(f"Swagger path does not exist: {self.swagger_path}", str(self.swagger_path))
        
        if not self.examples_path.exists():
            raise ConfigurationError(f"Examples path does not exist: {self.examples_path}", str(self.examples_path))
        
        # Ensure output path can be created
        try:
            self.output_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise ConfigurationError(f"Cannot create output path {self.output_path}: {e}", str(self.output_path))
    
    def add_preserve_field(self, field_name: str) -> None:
        """Add a field to the preserve list."""
        self.preserve_fields.add(field_name)
    
    def remove_preserve_field(self, field_name: str) -> None:
        """Remove a field from the preserve list."""
        self.preserve_fields.discard(field_name)
    
    def list_preserve_fields(self) -> Set[str]:
        """Get all preserve fields."""
        return self.preserve_fields.copy()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for serialization."""
        return {
            'paths': {
                'swagger': str(self.swagger_path),
                'examples': str(self.examples_path),
                'output': str(self.output_path)
            },
            'preserve_fields': list(self.preserve_fields)
        } 