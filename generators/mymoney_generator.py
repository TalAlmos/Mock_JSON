from generators.base_generator import BaseGenerator
from faker import Faker
from config import Config
import random
from datetime import datetime, timedelta

class MyMoneyGenerator(BaseGenerator):
    def __init__(self, faker: Faker, config: Config, field_profiles=None, example_prob=0.7):
        super().__init__(faker, config)
        self.field_profiles = field_profiles or {}
        self.example_prob = example_prob

    def generate_record(self):
        dates = self._generate_dates()
        record = {
            "status": self._pick_example_or_faker("response.status", lambda: random.choice([200, "OK"])),
            "message": "OK",
            "transId": "string",
            "entity": "MyMoneyResponse",
            "response": None,
            "topHeader": self._generate_top_header(),
            "mainHeader": self._generate_main_header(),
            "accumulationByProduct": self._generate_accumulation_by_product(),
            "productList": self._generate_product_list(),
            "lastActions": self._generate_last_actions()
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
        start_date = today - timedelta(days=days_ago)
        return {
            "date": start_date.strftime("%d.%m.%Y"),
            "short": start_date.strftime("%d.%m.%y")
        }

    def _generate_top_header(self):
        total_savings = random.randint(100000, 2000000)
        month_change = random.uniform(-5, 5)
        accumulate_change = random.uniform(-50000, 50000)
        return {
            "sumSaving": {
                "value": total_savings,
                "currency": "₪"
            },
            "numSavingChannel": random.randint(1, 3),
            "monthChange": {
                "value": round(month_change, 2),
                "sign": "%"
            },
            "sumMonthChange": {
                "value": round(total_savings * month_change / 100, 2),
                "currency": "₪"
            },
            "accumulateChange": {
                "value": round(accumulate_change, 2),
                "currency": "₪"
            }
        }

    def _generate_main_header(self):
        dates = self._generate_dates()
        total_savings = random.randint(100000, 2000000)
        fluent_withdraw = random.randint(0, total_savings // 2) if random.choice([True, False]) else None
        expected_retirement = random.randint(5000, 50000) if random.choice([True, False]) else None
        return {
            "date": dates["date"],
            "totalSaving": {
                "value": total_savings,
                "currency": "₪"
            },
            "fluentWithdraw": {
                "value": fluent_withdraw,
                "currency": "₪"
            } if fluent_withdraw else None,
            "expectedForRetirement": {
                "value": expected_retirement,
                "currency": "₪"
            } if expected_retirement else None,
            "savingExpectedForRetirement": None
        }

    def _generate_accumulation_by_product(self):
        product_types = ["gemel", "hishtalmut", "gemelInvestment"]
        accumulation_list = []
        for product_type in product_types:
            if random.choice([True, False]):
                saving_sum = random.randint(50000, 500000)
                fluent_sum = random.randint(0, saving_sum) if product_type in ["hishtalmut", "gemelInvestment"] else None
                expected_retirement = random.randint(5000, 30000) if product_type == "gemel" else None
                accumulation_list.append({
                    "policyType": self._pick_example_or_faker("response.accumulationByProduct.list.policyType", lambda: product_type),
                    "savingSum": {
                        "value": saving_sum,
                        "currency": "₪"
                    },
                    "fluentSum": {
                        "value": fluent_sum,
                        "currency": "₪"
                    } if fluent_sum else None,
                    "eligibilityDate": "",
                    "expectedForRetirement": {
                        "value": expected_retirement,
                        "currency": "₪"
                    } if expected_retirement else None,
                    "notUsedForRetirement": product_type in ["hishtalmut", "gemelInvestment"],
                    "policyIds": [self._generate_policy_id(product_type)],
                    "updateDate": self._generate_dates()["short"]
                })
        return {"list": accumulation_list}

    def _generate_product_list(self):
        product_types = ["gemel", "hishtalmut", "gemelInvestment"]
        product_list = []
        for product_type in product_types:
            if random.choice([True, False]):
                policy_list = [self._generate_policy(product_type)]
                product_list.append({
                    "policyType": self._pick_example_or_faker("response.productList.list.policyType", lambda: product_type),
                    "policyList": policy_list
                })
        return {"list": product_list}

    def _generate_last_actions(self):
        return {"list": []}

    def _generate_policy_id(self, product_type):
        if product_type == "gemel":
            return f"001-{random.randint(100, 999)}-{random.randint(100000, 999999)} ({random.randint(1000000, 9999999)})"
        elif product_type == "hishtalmut":
            return f"007-{random.randint(100, 999)}-{random.randint(100000, 999999)} ({random.randint(1000000, 9999999)})"
        elif product_type == "gemelInvestment":
            return f"570-{random.randint(100, 999)}-{random.randint(100000, 999999)} ({random.randint(1000000, 9999999)})"
        else:
            return f"{random.randint(100000000, 999999999)}"

    def _generate_policy(self, product_type):
        policy_id = self._generate_policy_id(product_type)
        dates = self._generate_dates()
        saving_sum = random.randint(50000, 500000)
        status = random.choice([1, 2])
        investment_route = self._generate_investment_route(product_type, saving_sum)
        return {
            "policyId": policy_id,
            "originalPolicyName": None,
            "policyNickname": None,
            "subType": self._generate_subtype(product_type),
            "status": {
                "status": status,
                "statusDesc": self._pick_example_or_faker("response.productList.list.policyList.status.statusDesc", lambda: ("לא פעילה" if status == 1 else "פעילה"))
            },
            "updateTo": dates["date"],
            "dailyUpdateTo": dates["date"] if random.choice([True, False]) else None,
            "yieldUpdateDate": dates["short"] if random.choice([True, False]) else None,
            "dailyYieldUpdateDate": dates["date"] if random.choice([True, False]) else "",
            "hasProfitsShare": random.choice([True, False, None]),
            "productData": self._generate_product_data(product_type, saving_sum),
            "investmentRoutes": [investment_route] if investment_route else [],
            "tsuotPopup": None,
            "isNew": random.choice([True, False]),
            "isIndependent": random.choice([True, False, None])
        }

    def _generate_subtype(self, product_type):
        if product_type == "gemel":
            return random.choice([None, "MASHLIMA", "MAKIFA"])
        else:
            return None

    def _generate_product_data(self, product_type, saving_sum):
        dates = self._generate_dates()
        last_deposit = random.randint(1000, 10000) if random.choice([True, False]) else None
        available_withdraw = random.randint(0, saving_sum) if random.choice([True, False]) else None
        return {
            "savingSum": {
                "value": saving_sum,
                "currency": "₪"
            },
            "yieldBeginningYear": None,
            "lastDeposit": {
                "lastDepositsSum": {
                    "value": last_deposit,
                    "currency": "₪"
                },
                "lastDepositsDate": dates["date"]
            } if last_deposit else None,
            "depositedThisYear": None,
            "availableWithdraw": {
                "value": available_withdraw,
                "currency": "₪"
            } if available_withdraw else None,
            "withdrawDate": dates["date"] if random.choice([True, False]) else None,
            "managementFee": {
                "fromDeposit": {
                    "value": 0 if product_type in ["hishtalmut", "gemelInvestment"] else random.uniform(0, 2),
                    "sign": "%"
                },
                "fromSaving": {
                    "value": random.uniform(0.5, 0.7) if product_type in ["hishtalmut", "gemelInvestment"] else random.uniform(0.1, 0.6),
                    "sign": "%"
                }
            },
            "yieldFromYearBeginningTotal": None
        }

    def _generate_investment_route(self, product_type, saving_sum):
        if not random.choice([True, False]):
            return None
        dates = self._generate_dates()
        yield_value = random.uniform(-3, 4)
        route_names = {
            "gemel": "הפניקס גמל אשראי ואג\"ח",
            "hishtalmut": "הפניקס השתלמות אשראי ואג\"ח",
            "gemelInvestment": "הפניקס גמל להשקעה עוקב מדד S&P500"
        }
        return {
            "name": route_names.get(product_type, "השקעה כללית"),
            "joinDate": None,
            "percent": {
                "value": 100,
                "sign": "%"
            },
            "yieldBeginningYear": {
                "value": round(yield_value, 2),
                "sign": "%"
            },
            "yieldBeginningPolicy": None,
            "managementFeeFromDeposit": {
                "value": 0 if product_type in ["hishtalmut", "gemelInvestment"] else random.uniform(0, 2),
                "sign": "%"
            },
            "managementFeeFromSaving": {
                "value": random.uniform(0.5, 0.7) if product_type in ["hishtalmut", "gemelInvestment"] else random.uniform(0.1, 0.6),
                "sign": "%"
            },
            "accumulation": {
                "value": saving_sum,
                "currency": "₪"
            },
            "basketCode": str(random.randint(10, 9999)),
            "isYieldHidden": random.choice([True, False, None]),
            "dailyUpdateDate": dates["date"] if random.choice([True, False]) else None
        } 