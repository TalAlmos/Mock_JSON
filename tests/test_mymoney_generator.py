import pytest
from generators.mymoney_generator import MyMoneyGenerator
from faker import Faker
from config import Config

@pytest.fixture
def generator():
    faker = Faker(['he_IL'])
    config = Config()
    field_profiles = {"response.status": ["OK"]}
    return MyMoneyGenerator(faker, config, field_profiles, example_prob=1.0)

def test_generate_record_structure(generator):
    record = generator.generate_record()
    assert isinstance(record, dict)
    assert "status" in record
    assert record["status"] == "OK"
    assert "topHeader" in record
    assert "mainHeader" in record

def test_generate_record_random(generator):
    generator.example_prob = 0.0
    record = generator.generate_record()
    assert isinstance(record, dict)
    assert "status" in record
    assert record["status"] in [200, "OK"] 