import yaml
from pathlib import Path
import pytest
from config import Config

class TestYAMLConfig:
    def test_load_yaml_config(self):
        config_data = {
            "paths": {
                "swagger": "D:/Mock_JSON/data/swagger",
                "examples": "D:/Mock_JSON/data/examples",
                "output": "D:/Mock_JSON/data/mock_output"
            },
            "preserve_fields": ["status", "message", "transId", "entity"]
        }
        
        config = Config.from_yaml(config_data)
        assert config.swagger_path == Path("D:/Mock_JSON/data/swagger")
        assert "status" in config.preserve_fields
    
    def test_config_validation(self):
        invalid_config = {"paths": {}}  # Missing required fields
        
        with pytest.raises(ValueError):
            Config.from_yaml(invalid_config)
