# tests/test_commands.py
import pytest
from config import Config
from commands import GenerateCommand, ListTypesCommand, GeneratorContext


class TestGenerateCommand:
    def test_generate_command_execution(self):
        command = GenerateCommand("insurance", 3)
        context = GeneratorContext(Config())
        
        command.execute(context)
        
        # Verify that the correct number of records were generated
        assert len(context.get_saved_records()) == 3
        assert all(record["insurance_type"] == "insurance" for record in context.get_saved_records())
    
    def test_list_types_command(self):
        command = ListTypesCommand()
        context = GeneratorContext(Config())
        
        result = command.execute(context)
        
        # Check that we get a list of insurance types
        assert isinstance(result, list)
        assert len(result) > 0
        
        # Check that each result has the expected structure
        for type_info in result:
            assert "insurance_type" in type_info
            assert "supported" in type_info
    
    def test_generate_command_validation(self):
        """Test command validation"""
        # Test with unsupported insurance type
        command = GenerateCommand("nonexistent", 1)
        context = GeneratorContext(Config())
        
        with pytest.raises(ValueError, match="Unsupported insurance type"):
            command.execute(context)
    
    def test_generate_command_invalid_count(self):
        """Test command validation with invalid record count"""
        # Test with zero records
        command = GenerateCommand("insurance", 0)
        context = GeneratorContext(Config())
        
        errors = command.validate(context)
        assert "Number of records must be greater than 0" in errors[0]
        
        # Test with too many records
        command = GenerateCommand("insurance", 1001)
        errors = command.validate(context)
        assert "Number of records cannot exceed 1000" in errors[0]
    
    def test_command_descriptions(self):
        """Test command descriptions"""
        generate_cmd = GenerateCommand("insurance", 5)
        list_cmd = ListTypesCommand()
        
        assert "Generate 5 mock record(s) for insurance insurance" in generate_cmd.get_description()
        assert "List all available insurance types" in list_cmd.get_description()
