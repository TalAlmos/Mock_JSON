#!/usr/bin/env python3
"""
Error Handling Integration Tests

This module provides comprehensive tests for error handling throughout the mock data generation system,
testing error propagation, recovery mechanisms, and error reporting.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
from faker import Faker

from config import Config
from exceptions import (
    MockDataGenerationError,
    ConfigurationError,
    InsuranceTypeNotFoundError,
    SchemaAnalysisError,
    ValidationError,
    GeneratorError
)
from generators.registry import GeneratorRegistry
from generators.base_generator import BaseGenerator
from generators.insurance_generator import InsuranceGenerator
from factories.generator_factory import GeneratorFactory
from commands.generate_command import GenerateCommand
from commands.list_types_command import ListTypesCommand
from commands.generator_context import GeneratorContext


class TestErrorHandlingIntegration:
    """Test error handling integration across the system."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = Config()
        # Override paths to use temp directory for testing
        self.config.swagger_path = Path(self.temp_dir) / "swagger"
        self.config.examples_path = Path(self.temp_dir) / "examples"
        self.config.output_path = Path(self.temp_dir) / "output"
        
        # Create temp directories
        self.config.swagger_path.mkdir(parents=True, exist_ok=True)
        self.config.examples_path.mkdir(parents=True, exist_ok=True)
        self.config.output_path.mkdir(parents=True, exist_ok=True)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_configuration_error_propagation(self):
        """Test that configuration errors propagate correctly."""
        # Test with non-existent paths
        config = Config()
        config.swagger_path = Path("/nonexistent/path")
        
        with pytest.raises(ConfigurationError) as exc_info:
            config.validate()
        
        assert "Swagger path does not exist" in str(exc_info.value)
        assert exc_info.value.config_path == "/nonexistent/path"
    
    def test_insurance_type_not_found_error_propagation(self):
        """Test that insurance type not found errors propagate correctly."""
        factory = GeneratorFactory(self.config)
        
        with pytest.raises(InsuranceTypeNotFoundError) as exc_info:
            factory.create_generator("nonexistent_type")
        
        assert "nonexistent_type" in str(exc_info.value)
        assert "insurance" in exc_info.value.available_types
    
    def test_generator_error_propagation(self):
        """Test that generator errors propagate correctly."""
        registry = GeneratorRegistry()
        
        # Test registering invalid generator class
        class InvalidGenerator:
            pass
        
        with pytest.raises(GeneratorError) as exc_info:
            registry.register("invalid", InvalidGenerator)
        
        assert "must inherit from BaseGenerator" in str(exc_info.value)
        # Check that the generator type contains the class name
        assert "InvalidGenerator" in exc_info.value.generator_type
        assert exc_info.value.operation == "register"
    
    def test_schema_analysis_error_handling(self):
        """Test schema analysis error handling."""
        from schema_analyzer import SchemaAnalyzer
        
        analyzer = SchemaAnalyzer()
        
        # Test with invalid data structure
        invalid_examples = [{"invalid": None}]
        
        # This should not raise an error but handle gracefully
        result = analyzer.analyze_structure(invalid_examples)
        assert isinstance(result, dict)
        assert "type" in result
    
    def test_validation_error_handling(self):
        """Test validation error handling."""
        # Create a mock generator that raises validation errors
        class MockGenerator(BaseGenerator):
            def get_schema(self):
                return {"type": "object", "properties": {}}
            
            def generate_record(self):
                raise ValidationError("Validation failed", ["field1", "field2"], {"test": "data"})
        
        registry = GeneratorRegistry()
        registry.register("mock", MockGenerator)
        
        factory = GeneratorFactory(self.config)
        factory.registry = registry
        
        generator = factory.create_generator("mock")
        
        with pytest.raises(ValidationError) as exc_info:
            generator.generate_record()
        
        assert "Validation failed" in str(exc_info.value)
        assert exc_info.value.validation_errors == ["field1", "field2"]
        assert exc_info.value.data == {"test": "data"}
    
    def test_error_recovery_in_commands(self):
        """Test error recovery in command execution."""
        context = GeneratorContext(self.config)
        
        # Test with invalid insurance type
        command = GenerateCommand("nonexistent", 1)
        
        with pytest.raises(ValueError, match="Validation failed"):
            command.execute(context)
    
    def test_error_logging_and_reporting(self):
        """Test error logging and reporting mechanisms."""
        # Test that errors include detailed information
        try:
            raise InsuranceTypeNotFoundError("test_type", ["type1", "type2"])
        except InsuranceTypeNotFoundError as e:
            assert e.insurance_type == "test_type"
            assert e.available_types == ["type1", "type2"]
            assert "test_type" in str(e)
            assert "type1" in str(e)
            assert "type2" in str(e)
    
    def test_error_details_preservation(self):
        """Test that error details are preserved correctly."""
        error = MockDataGenerationError("Test error", {"key": "value", "number": 42})
        
        assert error.message == "Test error"
        assert error.details == {"key": "value", "number": 42}
        assert "Test error" in str(error)
        assert "Details" in str(error)
    
    def test_cascading_error_handling(self):
        """Test cascading error handling through multiple layers."""
        # Test error propagation from factory through registry to generator
        registry = GeneratorRegistry()
        
        # Register a generator that will fail
        class FailingGenerator(BaseGenerator):
            def get_schema(self):
                return {"type": "object", "properties": {}}
            
            def generate_record(self):
                raise GeneratorError("Generator failed", "FailingGenerator", "generate_record")
        
        registry.register("failing", FailingGenerator)
        factory = GeneratorFactory(self.config)
        factory.registry = registry
        
        generator = factory.create_generator("failing")
        
        with pytest.raises(GeneratorError) as exc_info:
            generator.generate_record()
        
        assert "Generator failed" in str(exc_info.value)
        assert exc_info.value.generator_type == "FailingGenerator"
        assert exc_info.value.operation == "generate_record"
    
    def test_error_with_context_information(self):
        """Test that errors include relevant context information."""
        # Test configuration error with path information
        config = Config()
        config.swagger_path = Path("/invalid/path")
        
        with pytest.raises(ConfigurationError) as exc_info:
            config.validate()
        
        assert exc_info.value.config_path == "/invalid/path"
        assert "Swagger path does not exist" in str(exc_info.value)
    
    def test_error_handling_with_mock_data(self):
        """Test error handling with realistic mock data scenarios."""
        # Create a temporary swagger file
        swagger_file = self.config.swagger_path / "test_swagger.json"
        swagger_file.write_text('{"components": {"schemas": {}}}')
        
        # Create a temporary example file
        example_file = self.config.examples_path / "test_example.json"
        example_file.write_text('{"test": "data"}')
        
        # Test that the system can handle the files without errors
        config = Config()
        config.swagger_path = self.config.swagger_path
        config.examples_path = self.config.examples_path
        config.output_path = self.config.output_path
        
        # This should not raise any errors
        config.validate()
        
        # Test factory with valid configuration
        factory = GeneratorFactory(config)
        assert factory.is_supported("insurance")
    
    def test_error_boundary_conditions(self):
        """Test error handling at boundary conditions."""
        # Test with empty data
        registry = GeneratorRegistry()
        assert registry.count() == 0
        
        # Test with None values - this actually works in Python
        registry.register(None, InsuranceGenerator)
        assert registry.is_registered(None)
        assert registry.get_generator(None) == InsuranceGenerator
        
        # Test with empty strings
        with pytest.raises(InsuranceTypeNotFoundError):
            factory = GeneratorFactory(self.config)
            factory.create_generator("")
    
    def test_error_recovery_mechanisms(self):
        """Test error recovery mechanisms."""
        # Test that the system can recover from temporary errors
        config = Config()
        
        # Test preserve field operations
        config.add_preserve_field("test_field")
        assert "test_field" in config.preserve_fields
        
        config.remove_preserve_field("test_field")
        assert "test_field" not in config.preserve_fields
        
        # Test registry operations
        registry = GeneratorRegistry()
        registry.register("test", InsuranceGenerator)
        assert registry.is_registered("test")
        
        success = registry.unregister("test")
        assert success
        assert not registry.is_registered("test")
    
    def test_error_message_clarity(self):
        """Test that error messages are clear and actionable."""
        # Test configuration error message
        config = Config()
        config.swagger_path = Path("/nonexistent")
        
        with pytest.raises(ConfigurationError) as exc_info:
            config.validate()
        
        error_message = str(exc_info.value)
        assert "Swagger path does not exist" in error_message
        assert "/nonexistent" in error_message
        
        # Test insurance type error message
        factory = GeneratorFactory(self.config)
        
        with pytest.raises(InsuranceTypeNotFoundError) as exc_info:
            factory.create_generator("unknown_type")
        
        error_message = str(exc_info.value)
        assert "Insurance type 'unknown_type' not found" in error_message
        assert "Available types" in error_message
