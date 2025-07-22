import pytest
from generators.excellence_saving_generator import ExcellenceSavingGenerator
from faker import Faker
from config import Config

@pytest.fixture
def generator():
    faker = Faker(['he_IL'])
    config = Config()
    field_profiles = {"response.general.policyName": ["קופת גמל"]}
    return ExcellenceSavingGenerator(faker, config, field_profiles, example_prob=1.0)

def test_generate_record_structure(generator):
    record = generator.generate_record()
    assert isinstance(record, dict)
    assert "response" in record
    assert "general" in record["response"]
    assert record["response"]["general"]["policyName"] == "קופת גמל"

def test_generate_record_random(generator):
    generator.example_prob = 0.0
    record = generator.generate_record()
    assert isinstance(record, dict)
    assert "response" in record
    assert "general" in record["response"]
    assert record["response"]["general"]["policyName"] in ["קופת גמל", "פוליסת ביטוח"] 