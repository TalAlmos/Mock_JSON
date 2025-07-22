# tests/test_factory.py
import pytest
from config import Config
from factories.generator_factory import GeneratorFactory
from exceptions import InsuranceTypeNotFoundError


class TestGeneratorFactory:
    def test_factory_initialization(self):
        config = Config()
        factory = GeneratorFactory(config)
        assert factory.config == config
    
    def test_register_generators(self):
        factory = GeneratorFactory(Config())
        # Test that the base insurance generator is registered
        expected_types = ["insurance"]
        for insurance_type in expected_types:
            generator = factory.create_generator(insurance_type)
            assert generator is not None
    
    def test_create_nonexistent_generator(self):
        factory = GeneratorFactory(Config())
        with pytest.raises(InsuranceTypeNotFoundError, match="Insurance type 'nonexistent' not found"):
            factory.create_generator("nonexistent")
    
    def test_generator_creation_with_dependencies(self):
        config = Config()
        factory = GeneratorFactory(config)
        generator = factory.create_generator("insurance")
        
        assert hasattr(generator, 'faker')
        assert hasattr(generator, 'config')
    
    def test_get_available_types(self):
        """Test the get_available_types method"""
        factory = GeneratorFactory(Config())
        available_types = factory.get_available_types()
        
        assert isinstance(available_types, list)
        assert "insurance" in available_types
    
    def test_is_supported(self):
        """Test the is_supported method"""
        factory = GeneratorFactory(Config())
        
        assert factory.is_supported("insurance") == True
        assert factory.is_supported("nonexistent") == False
    
    def test_get_generator_info(self):
        """Test the get_generator_info method"""
        factory = GeneratorFactory(Config())
        
        info = factory.get_generator_info("insurance")
        assert info["insurance_type"] == "insurance"
        assert info["supported"] == True
        
        info = factory.get_generator_info("nonexistent")
        assert "error" in info
