import pytest
from generators.travel_insurance_generator import TravelInsuranceGenerator
from faker import Faker
from config import Config

@pytest.fixture
def generator():
    faker = Faker(['he_IL'])
    config = Config()
    # Example field profile for allInsured
    field_profiles = {"response.response.basicCoverage.allInsured": [True]}
    return TravelInsuranceGenerator(faker, config, field_profiles, example_prob=1.0)  # Always use example

def test_generate_record_structure(generator):
    record = generator.generate_record()
    assert isinstance(record, dict)
    assert "basicCoverage" in record
    assert "allInsured" in record["basicCoverage"]
    assert record["basicCoverage"]["allInsured"] is True  # Should use example value

def test_generate_record_random(generator):
    # Lower probability, should sometimes use Faker/random
    generator.example_prob = 0.0
    record = generator.generate_record()
    assert isinstance(record, dict)
    assert "basicCoverage" in record
    assert "allInsured" in record["basicCoverage"]
    # Should not always be True
    assert record["basicCoverage"]["allInsured"] in [True, False] 