# tests/test_schema_analyzer.py
import pytest
from schema_analyzer import SchemaAnalyzer


class TestSchemaAnalyzer:
    def test_analyze_structure(self):
        analyzer = SchemaAnalyzer()
        examples = [{"name": "John", "age": 30}]
        
        result = analyzer.analyze_structure(examples)
        assert result["type"] == "object"
        assert "name" in result["properties"]
        assert "age" in result["properties"]
    
    def test_merge_structures(self):
        analyzer = SchemaAnalyzer()
        structure1 = {"type": "object", "properties": {"name": {"type": "string"}}}
        structure2 = {"type": "object", "properties": {"age": {"type": "number"}}}
        
        result = analyzer.merge_structures(structure1, structure2)
        assert "name" in result["properties"]
        assert "age" in result["properties"]
    
    def test_add_preserved_field_info(self):
        analyzer = SchemaAnalyzer()
        structure = {"type": "object", "properties": {"status": {"type": "string"}}}
        examples = [{"status": "active"}]
        
        analyzer._add_preserved_field_info(structure, examples)
        assert structure["properties"]["status"].get("preserve_original") == True
    
    def test_should_preserve_field(self):
        """Test the _should_preserve_field method"""
        analyzer = SchemaAnalyzer()
        
        # Test preserved fields
        assert analyzer._should_preserve_field("status") == True
        assert analyzer._should_preserve_field("message") == True
        assert analyzer._should_preserve_field("transId") == True
        
        # Test non-preserved fields
        assert analyzer._should_preserve_field("name") == False
        assert analyzer._should_preserve_field("age") == False
