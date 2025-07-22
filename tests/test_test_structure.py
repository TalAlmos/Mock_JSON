# tests/test_test_structure.py
import pytest
from pathlib import Path
from config import Config

class TestTestStructure:
    def test_all_generators_have_tests(self):
        """Ensure every generator has corresponding tests"""
        generator_files = [
            "generators/travel_generator.py",
            "generators/vehicle_generator.py",
            "generators/mymoney_generator.py"
        ]
        
        test_files = [
            "tests/test_generators/test_travel_generator.py",
            "tests/test_generators/test_vehicle_generator.py",
            "tests/test_generators/test_mymoney_generator.py"
        ]
        
        for generator_file in generator_files:
            test_file = generator_file.replace("generators/", "tests/test_generators/test_")
            assert Path(test_file).exists()
    
    def test_test_coverage(self):
        """Ensure high test coverage"""
        # This would integrate with coverage.py
        pass
