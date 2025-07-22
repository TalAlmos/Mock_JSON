from generators.base_generator import BaseGenerator
from faker import Faker
from config import Config
import random
from datetime import datetime, timedelta

class TravelInsuranceGenerator(BaseGenerator):
    def __init__(self, faker: Faker, config: Config, field_profiles=None, example_prob=0.7):
        super().__init__(faker, config)
        self.field_profiles = field_profiles or {}
        self.example_prob = example_prob  # Probability to use example value

    def generate_record(self):
        dates = self._generate_travel_dates()
        insured_count = random.randint(2, 4)
        insured_persons = [self.faker.first_name() for _ in range(insured_count)]
        coverage_response = {
            "basicCoverage": self._generate_coverage_with_insured(insured_persons, "basicCoverage"),
            "loggage": self._generate_coverage_with_insured(insured_persons, "loggage"),
            "searchRescue": self._generate_coverage_with_insured(insured_persons, "searchRescue"),
            "corona": self._generate_coverage_with_insured(insured_persons, "corona"),
            "extremeSport": self._generate_extreme_sport_coverage_with_insured(insured_persons, dates, "extremeSport"),
            "mobilePhone": self._generate_mobile_phone_coverage_with_insured(insured_persons, "mobilePhone"),
            "laptopOrTablet": self._generate_laptop_tablet_coverage_with_insured(insured_persons, "laptopOrTablet"),
            "cancelOrDelay": self._generate_coverage_with_insured(insured_persons, "cancelOrDelay")
        }
        return coverage_response

    def get_schema(self):
        return {"type": "object", "properties": {}}

    def _pick_example_or_faker(self, field_key, faker_func, *args, **kwargs):
        # Use example value with probability, fallback to Faker
        values = self.field_profiles.get(field_key, [])
        if values and random.random() < self.example_prob:
            return random.choice(values)
        return faker_func(*args, **kwargs)

    def _generate_travel_dates(self) -> dict:
        today = datetime(2025, 7, 7)
        days_from_now = random.randint(1, 180)
        start_date = today + timedelta(days=days_from_now)
        trip_duration = random.randint(2, 21)
        end_date = start_date + timedelta(days=trip_duration)
        return {
            "start_date": start_date.strftime("%d.%m.%Y"),
            "end_date": end_date.strftime("%d.%m.%Y"),
            "start_date_short": start_date.strftime("%d.%m.%y"),
            "end_date_short": end_date.strftime("%d.%m.%y"),
            "start_date_israeli": start_date.strftime("%d/%m/%Y"),
            "end_date_israeli": end_date.strftime("%d/%m/%Y"),
            "year": start_date.year,
            "month": start_date.month,
            "day": start_date.day,
            "end_year": end_date.year,
            "end_month": end_date.month,
            "end_day": end_date.day,
            "trip_duration": trip_duration
        }

    def _generate_coverage_with_insured(self, insured_persons, coverage_type):
        # Example-driven for allInsured
        all_insured = self._pick_example_or_faker(f"response.response.{coverage_type}.allInsured", lambda: random.choice([True, False]))
        return {
            "insuredList": insured_persons if random.choice([True, False]) else None,
            "extraData": None,
            "allInsured": all_insured
        }

    def _generate_extreme_sport_coverage_with_insured(self, insured_persons, dates, coverage_type):
        extra_data = []
        for _ in range(len(insured_persons)):
            extra_data.append({
                "startDate": dates["start_date_israeli"],
                "endDate": dates["end_date_israeli"]
            })
        all_insured = self._pick_example_or_faker(f"response.response.{coverage_type}.allInsured", lambda: True)
        return {
            "insuredList": insured_persons,
            "extraData": extra_data,
            "allInsured": all_insured
        }

    def _generate_mobile_phone_coverage_with_insured(self, insured_persons, coverage_type):
        insured_name = random.choice(insured_persons)
        phone_models = [
            "אייפון 15 פרו", "אייפון 14 פרו", "סמסונג גלקסי S24", "סמסונג גלקסי S23", "גוגל פיקסל 8", "OnePlus 11"
        ]
        model = self._pick_example_or_faker(f"response.response.{coverage_type}.extraData.model", lambda: random.choice(phone_models))
        extra_data = [{
            "owner": insured_name,
            "model": model
        }]
        all_insured = self._pick_example_or_faker(f"response.response.{coverage_type}.allInsured", lambda: False)
        return {
            "insuredList": [insured_name],
            "extraData": extra_data,
            "allInsured": all_insured
        }

    def _generate_laptop_tablet_coverage_with_insured(self, insured_persons, coverage_type):
        insured_name = random.choice(insured_persons)
        device_models = [
            "MEC BOOK AIR", "MEC BOOK PRO", "iPad Pro", "iPad Air", "Surface Pro", "Dell XPS 13", "Lenovo ThinkPad"
        ]
        model = self._pick_example_or_faker(f"response.response.{coverage_type}.extraData.model", lambda: random.choice(device_models))
        extra_data = [{
            "owner": insured_name,
            "model": model
        }]
        all_insured = self._pick_example_or_faker(f"response.response.{coverage_type}.allInsured", lambda: False)
        return {
            "insuredList": [insured_name],
            "extraData": extra_data,
            "allInsured": all_insured
        } 