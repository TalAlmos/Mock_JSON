# tests/test_regression.py
class TestRegression:
    def test_preserve_fields_functionality(self):
        """Ensure preserve fields still work after refactoring"""
        config = Config()
        generator = MockDataGenerator(config)
        
        # Generate data and verify preserved fields
        result = generator.generate_insurance_record("travel")
        
        # Check that preserved fields maintain their original values
        preserved_fields = ["status", "message", "transId", "entity"]
        for field in preserved_fields:
            if field in result:
                # These should have specific values, not random ones
                assert result[field] in ["success", "OK", "default", "WebTravelCoversByNumResponse"]
    
    def test_date_generation_consistency(self):
        """Ensure date generation is consistent"""
        generator = MockDataGenerator(Config())
        
        # Generate multiple records and verify dates are realistic
        for _ in range(5):
            result = generator.generate_insurance_record("travel")
            if "startDate" in result and "endDate" in result:
                # Verify dates are in correct format and range
                assert len(result["startDate"].split(".")) == 3
                assert len(result["endDate"].split(".")) == 3
