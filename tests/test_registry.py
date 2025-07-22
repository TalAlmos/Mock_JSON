# tests/test_registry.py
import pytest
from generators.registry import GeneratorRegistry
from generators.base_generator import BaseGenerator

class MockGenerator(BaseGenerator):
    def generate_record(self):
        return {"test": "data"}
    
    def get_schema(self):
        return {"type": "object"}

class TestGeneratorRegistry:
    def test_register_and_get_generator(self):
        registry = GeneratorRegistry()
        registry.register("test", MockGenerator)
        
        generator_class = registry.get_generator("test")
        assert generator_class == MockGenerator
    
    def test_get_nonexistent_generator(self):
        registry = GeneratorRegistry()
        generator = registry.get_generator("nonexistent")
        assert generator is None
    
    def test_register_duplicate_generator(self):
        registry = GeneratorRegistry()
        registry.register("test", MockGenerator)
        registry.register("test", MockGenerator)  # Should not raise error
        assert registry.get_generator("test") == MockGenerator
