from generators.base_generator import BaseGenerator
from faker import Faker
from config import Config
import random
from datetime import datetime, timedelta

class VehicleUnitedGenerator(BaseGenerator):
    def __init__(self, faker: Faker, config: Config, field_profiles=None, example_prob=0.7):
        super().__init__(faker, config)
        self.field_profiles = field_profiles or {}
        self.example_prob = example_prob

    def generate_record(self):
        dates = self._generate_vehicle_dates()
        vehicle_model = self._pick_example_or_faker("response.data.modelType", lambda: random.choice([
            'טויוטה קורולה', 'הונדה סיוויק', 'סוזוקי סוויפט', 'מיצובישי לאנסר', 'יונדאי I01 החדשה',
            'יונדאי ERIPSNI  30-I', "פולקסווגן ג'טה מנג'ר 1600", 'ניסאן קשקאי החדשה אסנטה',
            'מאזדה 3 אקטיב אוטו\' 4 דלתות', 'יונדאי 35IXPRIME', 'טסלהY DWR', 'BYD ATTO 3 COMFORT'
        ]))
        license_plate = str(random.randint(1000000, 99999999))
        vehicle_united_detail = self._generate_vehicle_united_detail(dates, vehicle_model, license_plate)
        policy_list = [self._generate_policy_item(dates, vehicle_model, license_plate) for _ in range(random.randint(1, 3))]
        record = {
            "vehicleUnitedDetail": vehicle_united_detail,
            "insuranceType": self._pick_example_or_faker("response.data.insuranceType", lambda: random.choice(["מקיף + חובה", "ביטוח חובה", "ביטוח מקיף"])),
            "modelType": vehicle_model,
            "licensePlate": license_plate,
            "isExpired": random.choice([True, False]),
            "isActive": random.choice([True, False]),
            "list": policy_list
        }
        return record

    def get_schema(self):
        return {"type": "object", "properties": {}}

    def _pick_example_or_faker(self, field_key, faker_func, *args, **kwargs):
        values = self.field_profiles.get(field_key, [])
        if values and random.random() < self.example_prob:
            return random.choice(values)
        return faker_func(*args, **kwargs)

    def _generate_vehicle_dates(self):
        today = datetime(2025, 7, 7)
        days_ago = random.randint(1, 180)
        start_date = today - timedelta(days=days_ago)
        end_date = start_date + timedelta(days=364)
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
            "end_day": end_date.day
        }

    def _generate_vehicle_united_detail(self, dates, vehicle_model, license_plate):
        return {
            "insuranceDetails": {
                "updatedAt": dates["start_date_short"],
                "startDate": dates["start_date_short"],
                "endDate": dates["end_date_short"],
                "originalEndDate": f"{dates['end_year']}-{dates['end_month']:02d}-{dates['end_day']:02d}T00:00:00",
                "originalStartDate": f"{dates['year']}-{dates['month']:02d}-{dates['day']:02d}T00:00:00",
                "premia": {
                    "value": random.randint(1000, 10000),
                    "currency": "₪"
                },
                "list": [
                    {
                        "requiredRenewal": True,
                        "startDate": dates["start_date_short"],
                        "endDate": dates["end_date_short"],
                        "policySubType": self._pick_example_or_faker("response.data.vehicleUnitedDetail.insuranceDetails.list.policySubType", lambda: random.choice(["makif", "hova"])),
                        "premia": {
                            "currency": "₪",
                            "value": random.randint(1000, 8000)
                        },
                        "claimsList": [
                            {
                                "claimNo": str(random.randint(1000000000, 9999999999)),
                                "submissionDate": dates["start_date_short"]
                            }
                        ] if random.choice([True, False]) else []
                    }
                ]
            },
            "payments": {
                "payedSum": {
                    "value": random.randint(1000, 8000),
                    "currency": "₪"
                },
                "balanceSum": {
                    "value": random.randint(0, 3000),
                    "currency": "₪"
                },
                "payedList": {
                    "list": [
                        {
                            "date": dates["start_date_israeli"],
                            "method": self._pick_example_or_faker("response.data.vehicleUnitedDetail.payments.payedList.list.method", lambda: random.choice(["תשלום בכרטיס אשראי", "ויזה כ.א.ל 2666", "העברה בנקאית"])),
                            "paymentType": "חיוב",
                            "amount": {
                                "value": random.randint(100, 1000),
                                "currency": "₪"
                            },
                            "details": [
                                {
                                    "paymentNo": None,
                                    "date": dates["start_date_israeli"],
                                    "method": self._pick_example_or_faker("response.data.vehicleUnitedDetail.payments.payedList.list.details.method", lambda: random.choice(["תשלום בכרטיס אשראי", "ויזה כ.א.ל 2666"])),
                                    "totalPayments": "",
                                    "policySubType": self._pick_example_or_faker("response.data.vehicleUnitedDetail.payments.payedList.list.details.policySubType", lambda: random.choice(["makif", "hova"])),
                                    "amount": {
                                        "value": random.randint(100, 1000),
                                        "currency": "₪"
                                    }
                                }
                            ]
                        }
                    ]
                }
            },
            "agentDetails": [
                {
                    "name": "הפניקס SMART",
                    "address": "דרך השלום 53 גבעתיים 53454",
                    "phone": "0778888888"
                }
            ],
            "authorizedDrivers": [
                {
                    "firstName": self.faker.first_name(),
                    "lastName": self.faker.last_name()
                },
                {
                    "firstName": self.faker.first_name(),
                    "lastName": self.faker.last_name()
                }
            ],
            "serviceList": [
                {
                    "type": "גרירה",
                    "name": "שגריר",
                    "phone": "*8888",
                    "eSite": None
                },
                {
                    "type": "שמשות",
                    "name": "אוטוגלס",
                    "phone": "03-6507777",
                    "eSite": None
                },
                {
                    "type": "פנסים ומראות",
                    "name": "אוטוגלס",
                    "phone": "03-6507777",
                    "eSite": None
                }
            ],
            "treatmentSubjects": [],
            "licenseEndDate": dates["end_date_short"],
            "youngerDriverAge": str(random.randint(18, 80))
        }

    def _generate_policy_item(self, dates, vehicle_model, license_plate):
        return {
            "policyId": f"POL-{random.randint(100000, 999999)}",
            "insuranceType": self._pick_example_or_faker("response.data.list.insuranceType", lambda: random.choice(["ביטוח חובה", "ביטוח מקיף"])),
            "policyName": self._pick_example_or_faker("response.data.list.policyName", lambda: random.choice(["ביטוח לרכב פרטי", "ביטוח חובה לרכב פרטי"])),
            "endDate": dates["end_date"],
            "startDate": dates["start_date"],
            "modelType": vehicle_model,
            "licensePlate": license_plate,
            "classification": self._pick_example_or_faker("response.data.list.classification", lambda: random.choice(["אישי", "עסקי", "משפחתי"])),
            "carPolicyType": self._pick_example_or_faker("response.data.list.carPolicyType", lambda: random.choice(["makif", "hova"])),
            "isExpired": random.choice([True, False]),
            "isActive": random.choice([True, False]),
            "sectorId": str(random.randint(10, 999)),
            "validityTime": dates["start_date"],
            "isSmart": random.choice([True, False]),
            "AgentNumber": random.randint(10000, 99999)
        } 