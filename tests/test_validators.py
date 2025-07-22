#!/usr/bin/env python3
"""
Tests for Validation Framework

This module provides comprehensive tests for the validation framework,
including base validator, schema validator, data validator, and insurance validator.
"""

import pytest
from validators.base_validator import BaseValidator
from validators.schema_validator import SchemaValidator
from validators.data_validator import DataValidator
from validators.insurance_validator import InsuranceValidator
from exceptions import ValidationError


class TestBaseValidator:
    """Test the base validator functionality."""
    
    def test_base_validator_initialization(self):
        """Test base validator initialization."""
        # Create a concrete implementation for testing
        class TestValidator(BaseValidator):
            def validate(self, data):
                return True
        
        validator = TestValidator()
        assert len(validator.validation_errors) == 0
        assert len(validator.validation_warnings) == 0
    
    def test_add_error_and_warning(self):
        """Test adding errors and warnings."""
        # Create a concrete implementation for testing
        class TestValidator(BaseValidator):
            def validate(self, data):
                return True
        
        validator = TestValidator()
        
        validator.add_error("Test error")
        validator.add_warning("Test warning")
        
        assert len(validator.validation_errors) == 1
        assert len(validator.validation_warnings) == 1
        assert "Test error" in validator.validation_errors
        assert "Test warning" in validator.validation_warnings
    
    def test_clear_errors(self):
        """Test clearing errors and warnings."""
        # Create a concrete implementation for testing
        class TestValidator(BaseValidator):
            def validate(self, data):
                return True
        
        validator = TestValidator()
        validator.add_error("Error 1")
        validator.add_warning("Warning 1")
        
        validator.clear_errors()
        assert len(validator.validation_errors) == 0
        assert len(validator.validation_warnings) == 0
    
    def test_has_errors_and_warnings(self):
        """Test error and warning detection."""
        # Create a concrete implementation for testing
        class TestValidator(BaseValidator):
            def validate(self, data):
                return True
        
        validator = TestValidator()
        
        assert not validator.has_errors()
        assert not validator.has_warnings()
        
        validator.add_error("Error")
        assert validator.has_errors()
        assert not validator.has_warnings()
        
        validator.add_warning("Warning")
        assert validator.has_errors()
        assert validator.has_warnings()
    
    def test_raise_if_errors(self):
        """Test raising ValidationError when errors exist."""
        # Create a concrete implementation for testing
        class TestValidator(BaseValidator):
            def validate(self, data):
                return True
        
        validator = TestValidator()
        
        # No errors, should not raise
        validator.raise_if_errors()
        
        # Add error, should raise
        validator.add_error("Test error")
        with pytest.raises(ValidationError):
            validator.raise_if_errors()
    
    def test_validate_and_raise(self):
        """Test validate_and_raise method."""
        class TestValidator(BaseValidator):
            def validate(self, data):
                if data == "invalid":
                    self.add_error("Invalid data")
                    return False
                return True
        
        validator = TestValidator()
        
        # Valid data
        assert validator.validate_and_raise("valid") == True
        
        # Invalid data
        with pytest.raises(ValidationError):
            validator.validate_and_raise("invalid")
    
    def test_get_validation_summary(self):
        """Test validation summary generation."""
        # Create a concrete implementation for testing
        class TestValidator(BaseValidator):
            def validate(self, data):
                return True
        
        validator = TestValidator()
        validator.add_error("Error 1")
        validator.add_error("Error 2")
        validator.add_warning("Warning 1")
        
        summary = validator.get_validation_summary()
        
        assert summary["is_valid"] == False
        assert summary["error_count"] == 2
        assert summary["warning_count"] == 1
        assert "Error 1" in summary["errors"]
        assert "Error 2" in summary["errors"]
        assert "Warning 1" in summary["warnings"]


class TestSchemaValidator:
    """Test the schema validator functionality."""
    
    def test_schema_validator_initialization(self):
        """Test schema validator initialization."""
        validator = SchemaValidator()
        assert isinstance(validator, BaseValidator)
    
    def test_validate_string_schema(self):
        """Test string schema validation."""
        validator = SchemaValidator()
        schema = {"type": "string"}
        
        assert validator.validate("test", schema) == True
        assert validator.validate(123, schema) == False
        assert "Expected string" in validator.get_errors()[0]
    
    def test_validate_number_schema(self):
        """Test number schema validation."""
        validator = SchemaValidator()
        schema = {"type": "number"}
        
        assert validator.validate(123, schema) == True
        assert validator.validate(123.45, schema) == True
        assert validator.validate("123", schema) == False
    
    def test_validate_boolean_schema(self):
        """Test boolean schema validation."""
        validator = SchemaValidator()
        schema = {"type": "boolean"}
        
        assert validator.validate(True, schema) == True
        assert validator.validate(False, schema) == True
        assert validator.validate("true", schema) == False
    
    def test_validate_object_schema(self):
        """Test object schema validation."""
        validator = SchemaValidator()
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"}
            },
            "required": ["name"]
        }
        
        valid_data = {"name": "John", "age": 30}
        invalid_data = {"age": 30}  # Missing required field
        wrong_type_data = "not an object"
        
        assert validator.validate(valid_data, schema) == True
        assert validator.validate(invalid_data, schema) == False
        assert validator.validate(wrong_type_data, schema) == False
    
    def test_validate_array_schema(self):
        """Test array schema validation."""
        validator = SchemaValidator()
        schema = {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "maxItems": 3
        }
        
        valid_data = ["item1", "item2"]
        invalid_data = []  # Too few items
        wrong_type_data = "not an array"
        
        assert validator.validate(valid_data, schema) == True
        assert validator.validate(invalid_data, schema) == False
        assert validator.validate(wrong_type_data, schema) == False
    
    def test_validate_schema_structure(self):
        """Test schema structure validation."""
        validator = SchemaValidator()
        
        valid_schema = {"type": "object", "properties": {}}
        invalid_schema = {"properties": {}}  # Missing type
        
        assert validator.validate_schema_structure(valid_schema) == True
        assert validator.validate_schema_structure(invalid_schema) == False


class TestDataValidator:
    """Test the data validator functionality."""
    
    def test_data_validator_initialization(self):
        """Test data validator initialization."""
        validator = DataValidator()
        assert isinstance(validator, BaseValidator)
    
    def test_validate_insurance_type(self):
        """Test insurance type validation."""
        validator = DataValidator()
        
        valid_types = ["health", "vehicleUnited", "travel", "life"]
        for insurance_type in valid_types:
            assert validator._validate_insurance_type(insurance_type) == True
        
        assert validator._validate_insurance_type("invalid") == False
    
    def test_validate_policy_id(self):
        """Test policy ID validation."""
        validator = DataValidator()
        
        valid_ids = ["POL-123456", "001-123-456789", "007-456-789012"]
        for policy_id in valid_ids:
            assert validator._validate_policy_id(policy_id) == True
        
        assert validator._validate_policy_id("") == False
        assert validator._validate_policy_id(123) == False
    
    def test_validate_date(self):
        """Test date validation."""
        validator = DataValidator()
        
        valid_dates = ["01.01.2025", "01/01/2025", "2025-01-01"]
        for date in valid_dates:
            assert validator._validate_date(date) == True
        
        assert validator._validate_date("invalid") == False
        assert validator._validate_date("") == False
    
    def test_validate_date_range(self):
        """Test date range validation."""
        validator = DataValidator()
        
        # Valid range
        assert validator._validate_date_range("01.01.2025", "31.12.2025") == True
        
        # Invalid range (start after end)
        assert validator._validate_date_range("31.12.2025", "01.01.2025") == False
    
    def test_validate_monetary_value(self):
        """Test monetary value validation."""
        validator = DataValidator()
        
        assert validator._validate_monetary_value(1000) == True
        assert validator._validate_monetary_value(1000.50) == True
        assert validator._validate_monetary_value("1000") == False
        
        # Negative value should generate warning but not error
        validator.clear_errors()
        assert validator._validate_monetary_value(-100) == True
        assert len(validator.get_warnings()) > 0
    
    def test_validate_data_consistency(self):
        """Test data consistency validation."""
        validator = DataValidator()
        
        # Consistent data
        consistent_data = {"status": "active", "isActive": True}
        assert validator.validate_data_consistency(consistent_data) == True
        
        # Inconsistent data
        inconsistent_data = {"status": "active", "isActive": False}
        assert validator.validate_data_consistency(inconsistent_data) == False
    
    def test_validate_data_completeness(self):
        """Test data completeness validation."""
        validator = DataValidator()
        
        data = {"field1": "value1", "field2": "value2"}
        required_fields = ["field1", "field2"]
        
        assert validator.validate_data_completeness(data, required_fields) == True
        
        # Missing required field
        assert validator.validate_data_completeness(data, ["field1", "field2", "field3"]) == False
    
    def test_validate_data_quality(self):
        """Test data quality validation."""
        validator = DataValidator()
        
        # Good quality data
        good_data = {"field1": "value1", "field2": 123}
        assert validator.validate_data_quality(good_data) == True
        
        # Poor quality data
        poor_data = {"field1": "", "field2": {}}  # Empty values
        assert validator.validate_data_quality(poor_data) == True  # Should pass but with warnings
        assert len(validator.get_warnings()) > 0


class TestInsuranceValidator:
    """Test the insurance validator functionality."""
    
    def test_insurance_validator_initialization(self):
        """Test insurance validator initialization."""
        validator = InsuranceValidator()
        assert isinstance(validator, BaseValidator)
        assert hasattr(validator, 'schema_validator')
        assert hasattr(validator, 'data_validator')
    
    def test_validate_vehicle_insurance(self):
        """Test vehicle insurance validation."""
        validator = InsuranceValidator()
        
        valid_vehicle_data = {
            "modelType": "Toyota Corolla",
            "licensePlate": "12345678",
            "carPolicyType": "makif"
        }
        
        assert validator._validate_vehicle_insurance(valid_vehicle_data) == True
        
        # Invalid policy type
        invalid_data = {"carPolicyType": "invalid"}
        assert validator._validate_vehicle_insurance(invalid_data) == False
    
    def test_validate_travel_insurance(self):
        """Test travel insurance validation."""
        validator = InsuranceValidator()
        
        valid_travel_data = {
            "destination": "Europe",
            "basicCoverage": {"insuredList": ["John", "Jane"]}
        }
        
        assert validator._validate_travel_insurance(valid_travel_data) == True
    
    def test_validate_mymoney_data(self):
        """Test MyMoney data validation."""
        validator = InsuranceValidator()
        
        valid_mymoney_data = {
            "sumSaving": {"value": 100000},
            "productData": {"policyType": "gemel"}
        }
        
        assert validator._validate_mymoney_data(valid_mymoney_data) == True
        
        # Invalid product type
        invalid_data = {"productData": {"policyType": "invalid"}}
        assert validator._validate_mymoney_data(invalid_data) == False
    
    def test_validate_insurance_record(self):
        """Test complete insurance record validation."""
        validator = InsuranceValidator()
        
        valid_record = {
            "policyId": "POL-123456",
            "insuranceType": "health",
            "startDate": "01.01.2025",
            "endDate": "31.12.2025",
            "beneficiaries": 2
        }
        
        assert validator.validate_insurance_record(valid_record, "health") == True
    
    def test_get_validation_report(self):
        """Test validation report generation."""
        validator = InsuranceValidator()
        
        data = {"policyId": "POL-123456", "insuranceType": "health"}
        report = validator.get_validation_report(data, "health")
        
        assert "is_valid" in report
        assert "insurance_type" in report
        assert "error_count" in report
        assert "warning_count" in report
        assert "errors" in report
        assert "warnings" in report
        assert "data_quality_score" in report
