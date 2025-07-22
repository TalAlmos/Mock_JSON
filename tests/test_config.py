# tests/test_config.py
import pytest
from pathlib import Path
from config import Config

class TestConfig:
    def test_config_initialization(self):
        config = Config()
        assert isinstance(config.swagger_path, Path)
        assert isinstance(config.examples_path, Path)
        assert isinstance(config.output_path, Path)
        assert isinstance(config.preserve_fields, set)
    
    def test_preserve_fields_containment(self):
        config = Config()
        required_fields = {'status', 'message', 'transId', 'entity'}
        assert all(field in config.preserve_fields for field in required_fields)
    
    def test_paths_exist(self):
        config = Config()
        assert config.swagger_path.exists()
        assert config.examples_path.exists()
        # output_path should be created if it doesn't exist
        config.output_path.mkdir(parents=True, exist_ok=True)
        assert config.output_path.exists()
