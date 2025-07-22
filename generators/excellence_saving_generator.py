from generators.base_generator import BaseGenerator
from faker import Faker
from config import Config
import random
from datetime import datetime, timedelta

class ExcellenceSavingGenerator(BaseGenerator):
    def __init__(self, faker: Faker, config: Config, field_profiles=None, example_prob=0.7):
        super().__init__(faker, config)
        self.field_profiles = field_profiles or {}
        self.example_prob = example_prob

    def generate_record(self):
        dates = self._generate_dates()
        record = {
            "message": "",
            "response": {
                "general": self._generate_general(dates),
                "noticeUpdate": self._generate_notice_update(dates),
                "accountTransactions": self._generate_account_transactions(dates),
                "deposits": self._generate_deposits(dates),
                "managementFee": self._generate_management_fee(dates),
                "yearCostPrediction": self._generate_year_cost_prediction(dates),
                "investmentRoutesTransferConcentration": self._generate_investment_routes_transfer_concentration(dates),
                "expectedPayments": self._generate_expected_payments(dates),
                "beneficiaries": self._generate_beneficiaries(dates)
            },
            "status": 200
        }
        return record

    def get_schema(self):
        return {"type": "object", "properties": {}}

    def _pick_example_or_faker(self, field_key, faker_func, *args, **kwargs):
        values = self.field_profiles.get(field_key, [])
        if values and random.random() < self.example_prob:
            return random.choice(values)
        return faker_func(*args, **kwargs)

    def _generate_dates(self):
        today = datetime(2025, 7, 7)
        days_ago = random.randint(1, 180)
        date = today - timedelta(days=days_ago)
        return {
            "date": date.strftime("%d.%m.%Y"),
            "short": date.strftime("%d.%m.%y")
        }

    def _generate_general(self, dates):
        return {
            "policyName": self._pick_example_or_faker("response.general.policyName", lambda: random.choice(["קופת גמל", "פוליסת ביטוח" ])),
            "policyNickname": None,
            "policyNumber": f"001-001-{random.randint(100000,999999)} ({random.randint(1000000,9999999)})",
            "updatedAt": dates["date"],
            "startDate": None,
            "kiumRechivSachir": random.choice([True, False]),
            "name": self.faker.name(),
            "isNew": random.choice([True, False]),
            "isSeif14": random.choice([True, False]),
            "dataSource": None
        }

    def _generate_notice_update(self, dates):
        return {
            "generalDetails": {
                "startDate": dates["date"],
                "oldAccountNumber": f"{random.randint(100,999)}-00000000",
                "employerName": self._pick_example_or_faker("response.noticeUpdate.generalDetails.employerName", self.faker.company),
                "withdrawDate": None,
                "establishmentDate": None
            },
            "treatmentSubjects": []
        }

    def _generate_account_transactions(self, dates):
        years = ["2025", "2024", "2023", "2022"]
        # Mapping from title to subTitle
        title_subtitle_map = {
            "יתרה לתחילת שנה": "יתרת כספים בקופה בתחילת השנה",
            "הפקדות": "כספים שהופקדו לקופה",
            "רווחים": "בניכוי הוצאות לניהול השקעות",
            "דמי ניהול": "שנגבו בשנה זאת",
            "הפסדים": "בניכוי הוצאות לניהול השקעות"
        }
        def get_subtitle(title):
            if title.startswith("יתרה לתאריך"):
                return None
            return title_subtitle_map.get(title)
        possible_titles = [
            "יתרה לתחילת שנה",
            "הפקדות",
            "רווחים",
            "דמי ניהול",
            "יתרה לתאריך {}".format(dates["date"]),
            "הפסדים"
        ]
        return {
            "updateDate": dates["date"],
            "totalSum": {"value": random.randint(1000, 20000), "currency": "₪"},
            "dailySum": {"value": random.randint(1000, 20000), "currency": "₪"},
            "oneTimeWithdrawDate": dates["date"],
            "oneTimeWithdrawDateIsOver": random.choice([True, False]),
            "list": [
                {
                    "year": year,
                    "updateDate": dates["date"],
                    "list": [
                        self._generate_account_transaction_item(title, dates)
                        for title in possible_titles
                    ]
                } for year in years
            ]
        }

    def _generate_account_transaction_item(self, title, dates):
        item = {
            "title": title,
            "sum": {"value": random.randint(-200, 20000), "currency": "₪"} if random.choice([True, False]) else None
        }
        # Set subTitle only if mapping exists and not יתרה לתאריך ...
        if title.startswith("יתרה לתאריך"):
            pass  # Do not include subTitle
        else:
            title_subtitle_map = {
                "יתרה לתחילת שנה": "יתרת כספים בקופה בתחילת השנה",
                "הפקדות": "כספים שהופקדו לקופה",
                "רווחים": "בניכוי הוצאות לניהול השקעות",
                "דמי ניהול": "שנגבו בשנה זאת",
                "הפסדים": "בניכוי הוצאות לניהול השקעות"
            }
            sub_title = title_subtitle_map.get(title)
            if sub_title:
                item["subTitle"] = sub_title
        return item

    def _generate_deposits(self, dates):
        years = ["2025", "2024", "2023", "2022"]
        return {
            "dailyDeposits": {"list": []},
            "yearlyDeposits": {
                "list": [
                    {"year": year, "updateDate": dates["date"], "list": []} for year in years
                ]
            }
        }

    def _generate_management_fee(self, dates):
        return {
            "percentageMngFee": {
                "updateDate": dates["short"],
                "fromDeposit": {"percentageData": {"value": 0, "sign": "%"}},
                "fromSaving": {"percentageData": {"value": 1.05, "sign": "%"}}
            },
            "updatedMngFee": {
                "updateDate": dates["date"],
                "fromDeposit": {
                    "percentageData": {"value": 0, "sign": "%"},
                    "popupData": {"list": [{"fromDeposit": {"value": 0, "sign": "%"}, "dateFrom": "", "dateTo": ""}]}
                },
                "fromSaving": {
                    "percentageData": {"value": 1.05, "sign": "%"},
                    "popupData": {"list": [{"fromSaving": {"value": 1.05, "sign": "%"}, "dateFrom": "", "dateTo": ""}]}
                }
            }
        }

    def _generate_year_cost_prediction(self, dates):
        return {
            "updateDate": dates["short"],
            "list": [
                {
                    "title": self._pick_example_or_faker("response.yearCostPrediction.list.title", lambda: random.choice(["הפניקס גמל לבני 60 ומעלה", "הפניקס גמל לבני 50 ומטה"])),
                    "savingFee": {"value": 1.05, "sign": "%"} if random.choice([True, False]) else None,
                    "depositFee": {"value": 0, "sign": "%"} if random.choice([True, False]) else None,
                    "expenseCommission": {"value": 0.28, "sign": "%"},
                    "expenseNonCommission": {"value": 0.09, "sign": "%"},
                    "yearCostPrediction": {"value": 1.42, "sign": "%"} if random.choice([True, False]) else None
                }
            ]
        }

    def _generate_investment_routes_transfer_concentration(self, dates):
        return {
            "investmentRoutes": {
                "updateDate": dates["date"],
                "list": [
                    {
                        "yieldPercentage": {"value": 2.72, "sign": "%"},
                        "investmentRouteTitle": self._pick_example_or_faker("response.investmentRoutesTransferConcentration.investmentRoutes.list.investmentRouteTitle", lambda: "הפניקס גמל לבני 60 ומעלה"),
                        "investmentSum": {"value": 11294.32, "currency": "₪"},
                        "updateDate": dates["date"],
                        "tsuotLastUpdateDate": "2025-04-30T21:00:00.000+00:00",
                        "periodicRoute": None,
                        "isExistRoute": True,
                        "investmentPercent": {"value": 100, "sign": "%"},
                        "dailyYieldUpdateDate": dates["date"]
                    }
                ],
                "transferConcentration": {"list": [], "updatedAt": ""}
            }
        }

    def _generate_expected_payments(self, dates):
        return {
            "updateDate": dates["date"],
            "list": [
                {
                    "title": self._pick_example_or_faker("response.expectedPayments.list.title", lambda: random.choice(["סכום למשיכה חד פעמית", "סכום למקרה מוות"])),
                    "subTitle": self.faker.sentence(),
                    "sum": {"value": random.randint(1000, 20000), "currency": "₪"}
                } for _ in range(2)
            ]
        }

    def _generate_beneficiaries(self, dates):
        return {
            "list": [
                {
                    "name": self.faker.name(),
                    "date": dates["date"]
                }
            ],
            "updatedAt": ""
        } 