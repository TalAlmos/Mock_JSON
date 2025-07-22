# tests/test_exceptions.py
import pytest
from exceptions import (
    MockDataGenerationError,
    SchemaAnalysisError,
    InsuranceTypeNotFoundError,
    ConfigurationError,
    ValidationError,
    GeneratorError
)

class TestCustomExceptions:
    def test_mock_data_generation_error(self):
        with pytest.raises(MockDataGenerationError):
            raise MockDataGenerationError("Test error")
    
    def test_schema_analysis_error(self):
        with pytest.raises(SchemaAnalysisError):
            raise SchemaAnalysisError("Schema analysis failed")
    
    def test_insurance_type_not_found_error(self):
        with pytest.raises(InsuranceTypeNotFoundError):
            raise InsuranceTypeNotFoundError("Unknown type")
    
    def test_configuration_error(self):
        with pytest.raises(ConfigurationError):
            raise ConfigurationError("Configuration failed")
    
    def test_validation_error(self):
        with pytest.raises(ValidationError):
            raise ValidationError("Validation failed")
    
    def test_generator_error(self):
        with pytest.raises(GeneratorError):
            raise GeneratorError("Generator failed")
    
    def test_exception_with_details(self):
        error = MockDataGenerationError("Test error", {"key": "value"})
        assert "Test error" in str(error)
        assert error.details == {"key": "value"}
    
    def test_insurance_type_error_with_available_types(self):
        error = InsuranceTypeNotFoundError("unknown", ["health", "vehicle"])
        assert "unknown" in str(error)
        assert "health" in str(error)
        assert "vehicle" in str(error)
        assert error.available_types == ["health", "vehicle"]
