# tests/test_base_generator.py
import pytest
from faker import Faker
from generators.base_generator import BaseGenerator
from config import Config


class MockGenerator(BaseGenerator):
    """Mock generator for testing purposes."""
    
    def generate_record(self):
        return {"test": "data"}
    
    def get_schema(self):
        return {"type": "object", "properties": {}}


class TestBaseGenerator:
    def test_base_generator_initialization(self):
        config = Config()
        faker = Faker(['he_IL'])
        generator = MockGenerator(faker, config)
        
        assert generator.faker == faker
        assert generator.config == config
    
    def test_abstract_methods_force_implementation(self):
        """Test that concrete classes must implement abstract methods"""
        with pytest.raises(TypeError):
            # This should fail because BaseGenerator is abstract
            BaseGenerator(Faker(['he_IL']), Config())
    
    def test_generate_multiple_records(self):
        """Test the generate_multiple_records method"""
        config = Config()
        faker = Faker(['he_IL'])
        generator = MockGenerator(faker, config)
        
        records = generator.generate_multiple_records(3)
        assert len(records) == 3
        assert all(isinstance(record, dict) for record in records)
    
    def test_get_insurance_type(self):
        """Test the get_insurance_type method"""
        config = Config()
        faker = Faker(['he_IL'])
        generator = MockGenerator(faker, config)
        
        insurance_type = generator.get_insurance_type()
        assert insurance_type == "mock"
    
    def test_get_preserve_fields(self):
        """Test the get_preserve_fields method"""
        config = Config()
        faker = Faker(['he_IL'])
        generator = MockGenerator(faker, config)
        
        preserve_fields = generator.get_preserve_fields()
        assert isinstance(preserve_fields, set)
        assert 'status' in preserve_fields
