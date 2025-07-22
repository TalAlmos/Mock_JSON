import pytest
from generators.vehicle_united_generator import VehicleUnitedGenerator
from faker import Faker
from config import Config

@pytest.fixture
def generator():
    faker = Faker(['he_IL'])
    config = Config()
    field_profiles = {"response.data.modelType": ["יונדאי I01 החדשה"]}
    return VehicleUnitedGenerator(faker, config, field_profiles, example_prob=1.0)

def test_generate_record_structure(generator):
    record = generator.generate_record()
    assert isinstance(record, dict)
    assert "vehicleUnitedDetail" in record
    assert "modelType" in record
    assert record["modelType"] == "יונדאי I01 החדשה"

def test_generate_record_random(generator):
    generator.example_prob = 0.0
    record = generator.generate_record()
    assert isinstance(record, dict)
    assert "vehicleUnitedDetail" in record
    assert "modelType" in record
    # Should not always be the example value
    assert record["modelType"] in [
        'טויוטה קורולה', 'הונדה סיוויק', 'סוזוקי סוויפט', 'מיצובישי לאנסר', 'יונדאי I01 החדשה',
        'יונדאי ERIPSNI  30-I', "פולקסווגן ג'טה מנג'ר 1600", 'ניסאן קשקאי החדשה אסנטה',
        'מאזדה 3 אקטיב אוטו\' 4 דלתות', 'יונדאי 35IXPRIME', 'טסלהY DWR', 'BYD ATTO 3 COMFORT'
    ] 