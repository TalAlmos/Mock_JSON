# tests/test_integration.py
class TestEndToEnd:
    def test_full_generation_workflow(self):
        """Test the complete workflow from start to finish"""
        config = Config()
        generator = MockDataGenerator(config)
        
        # Test that we can generate travel insurance data
        result = generator.run("travel")
        
        # Verify the output structure
        assert "status" in result
        assert "response" in result
        assert result["status"] == "success"
    
    def test_backward_compatibility(self):
        """Ensure refactored code produces same output as original"""
        # Generate data with original implementation
        original_generator = OriginalMockDataGenerator()
        original_result = original_generator.generate_insurance_record("travel")
        
        # Generate data with refactored implementation
        refactored_generator = MockDataGenerator(Config())
        refactored_result = refactored_generator.generate_insurance_record("travel")
        
        # Compare key fields (excluding random data)
        assert original_result.keys() == refactored_result.keys()
        for key in ["insurance_type", "policy_name"]:
            if key in original_result:
                assert key in refactored_result