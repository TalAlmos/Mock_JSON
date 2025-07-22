# tests/test_insurance_generator.py
import pytest
from faker import Faker
from config import Config
from generators.insurance_generator import InsuranceGenerator


class TestInsuranceGenerator:
    def test_generate_base_fields(self):
        generator = InsuranceGenerator(Faker(['he_IL']), Config())
        schema = {"properties": {"name": {"type": "string"}}}
        dates = {"start_date": "01.01.2025"}
        
        result = generator._generate_base_fields(schema, dates)
        assert "name" in result
        assert isinstance(result["name"], str)
    
    def test_generate_complex_fields(self):
        generator = InsuranceGenerator(Faker(['he_IL']), Config())
        schema = {"properties": {"vehicleDetails": {"type": "object"}}}
        dates = {"start_date": "01.01.2025"}
        
        result = generator._generate_complex_fields(schema, dates)
        assert "vehicleDetails" in result
        assert isinstance(result["vehicleDetails"], dict)
    
    def test_merge_records(self):
        generator = InsuranceGenerator(Faker(['he_IL']), Config())
        base_record = {"name": "John"}
        complex_fields = {"vehicleDetails": {"model": "Toyota"}}
        
        result = generator._merge_records(base_record, complex_fields)
        assert result["name"] == "John"
        assert result["vehicleDetails"]["model"] == "Toyota"
    
    def test_generate_record(self):
        """Test the main generate_record method"""
        generator = InsuranceGenerator(Faker(['he_IL']), Config())
        record = generator.generate_record()
        
        assert isinstance(record, dict)
        assert "insurance_type" in record
        assert "policy_id" in record
        assert "start_date" in record
        assert "end_date" in record
        assert "status" in record
    
    def test_get_schema(self):
        """Test the get_schema method"""
        generator = InsuranceGenerator(Faker(['he_IL']), Config())
        schema = generator.get_schema()
        
        assert isinstance(schema, dict)
        assert "type" in schema
        assert "properties" in schema
        assert "required_fields" in schema
