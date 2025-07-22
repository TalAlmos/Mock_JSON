# tests/test_config_integration.py
class TestConfigIntegration:
    def test_original_generator_with_config(self):
        """Test that original generator works with extracted config"""
        from mock_data_generator import MockDataGenerator
        from config import Config
        
        config = Config()
        generator = MockDataGenerator()
        
        # Replace hardcoded paths with config
        generator.swagger_path = config.swagger_path
        generator.examples_path = config.examples_path
        generator.output_path = config.output_path
        generator.preserve_fields = config.preserve_fields
        
        # Test that basic functionality still works
        assert generator.load_swagger_file()
        assert generator.load_example_files()
