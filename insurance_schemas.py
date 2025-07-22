#!/usr/bin/env python3
"""
Insurance Type Schema Definitions

This module defines the required fields, validation rules, and generation patterns
for each insurance type based on the analysis of example data.
"""

from typing import Dict, List, Any, Set, Optional
from dataclasses import dataclass
from enum import Enum

class FieldType(Enum):
    """Field type enumeration for validation."""
    STRING = "string"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    OBJECT = "object"
    ARRAY = "array"
    NULL = "null"

@dataclass
class FieldDefinition:
    """Definition of a field with its type and requirements."""
    field_type: FieldType
    required: bool = True
    default_value: Any = None
    validation_rules: Optional[Dict[str, Any]] = None
    generation_pattern: Optional[str] = None

class InsuranceSchema:
    """Schema definition for an insurance type."""
    
    def __init__(self, insurance_type: str, required_fields: Dict[str, FieldDefinition]):
        self.insurance_type = insurance_type
        self.required_fields = required_fields
        self.optional_fields = {}
    
    def get_required_field_names(self) -> Set[str]:
        """Get set of required field names."""
        return {name for name, field in self.required_fields.items() if field.required}
    
    def validate_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate data against this schema and return list of errors."""
        errors = []
        
        # Check required fields
        for field_name, field_def in self.required_fields.items():
            if field_def.required and field_name not in data:
                errors.append(f"Missing required field: {field_name}")
            elif field_name in data:
                # Type validation
                if not self._validate_field_type(data[field_name], field_def.field_type):
                    errors.append(f"Invalid type for field {field_name}: expected {field_def.field_type.value}")
        
        return errors
    
    def _validate_field_type(self, value: Any, expected_type: FieldType) -> bool:
        """Validate if a value matches the expected type."""
        if value is None:
            return expected_type == FieldType.NULL
        elif expected_type == FieldType.STRING:
            return isinstance(value, str)
        elif expected_type == FieldType.INTEGER:
            return isinstance(value, int)
        elif expected_type == FieldType.BOOLEAN:
            return isinstance(value, bool)
        elif expected_type == FieldType.OBJECT:
            return isinstance(value, dict)
        elif expected_type == FieldType.ARRAY:
            return isinstance(value, list)
        return True

# Define insurance type schemas based on analysis
INSURANCE_SCHEMAS = {
    "travel": InsuranceSchema("travel", {
        # New complex coverage structure only
        "basicCoverage": FieldDefinition(FieldType.OBJECT, generation_pattern="travel_coverage"),
        "loggage": FieldDefinition(FieldType.OBJECT, generation_pattern="travel_coverage"),
        "searchRescue": FieldDefinition(FieldType.OBJECT, generation_pattern="travel_coverage"),
        "corona": FieldDefinition(FieldType.OBJECT, generation_pattern="travel_coverage"),
        "extremeSport": FieldDefinition(FieldType.OBJECT, generation_pattern="travel_extreme_sport"),
        "mobilePhone": FieldDefinition(FieldType.OBJECT, generation_pattern="travel_mobile_phone"),
        "laptopOrTablet": FieldDefinition(FieldType.OBJECT, generation_pattern="travel_laptop_tablet"),
        "cancelOrDelay": FieldDefinition(FieldType.OBJECT, generation_pattern="travel_coverage"),
    }),
    
    "vehicle": InsuranceSchema("vehicle", {
        "policyId": FieldDefinition(FieldType.STRING, generation_pattern="policy_id"),
        "insuranceType": FieldDefinition(FieldType.STRING, generation_pattern="vehicle_insurance_type"),
        "policyName": FieldDefinition(FieldType.STRING, generation_pattern="vehicle_policy_name"),
        "startDate": FieldDefinition(FieldType.STRING, generation_pattern="date"),
        "endDate": FieldDefinition(FieldType.STRING, generation_pattern="date"),
        "modelType": FieldDefinition(FieldType.STRING, generation_pattern="vehicle_model"),
        "licensePlate": FieldDefinition(FieldType.STRING, generation_pattern="license_plate"),
        "classification": FieldDefinition(FieldType.STRING, generation_pattern="classification"),
        "carPolicyType": FieldDefinition(FieldType.STRING, generation_pattern="car_policy_type"),
        "sectorId": FieldDefinition(FieldType.STRING, generation_pattern="sector_id"),
        "validityTime": FieldDefinition(FieldType.STRING, generation_pattern="date"),
        "isExpired": FieldDefinition(FieldType.BOOLEAN),
        "isActive": FieldDefinition(FieldType.BOOLEAN),
        "isSmart": FieldDefinition(FieldType.BOOLEAN),
        "AgentNumber": FieldDefinition(FieldType.INTEGER, generation_pattern="agent_number"),
    }),
    
    "health": InsuranceSchema("health", {
        "policyId": FieldDefinition(FieldType.STRING, generation_pattern="policy_id"),
        "insuranceType": FieldDefinition(FieldType.STRING, generation_pattern="health_insurance_type"),
        "policyName": FieldDefinition(FieldType.STRING, generation_pattern="health_policy_name"),
        "startDate": FieldDefinition(FieldType.STRING, generation_pattern="date"),
        "insuredName": FieldDefinition(FieldType.STRING, generation_pattern="name"),
        "originalPolicyName": FieldDefinition(FieldType.STRING, generation_pattern="health_policy_name"),
        "beneficiariesCount": FieldDefinition(FieldType.INTEGER, generation_pattern="beneficiaries_count"),
        "isActive": FieldDefinition(FieldType.BOOLEAN),
        "isExpired": FieldDefinition(FieldType.BOOLEAN),
        "isPaila": FieldDefinition(FieldType.BOOLEAN),
        "AgentNumber": FieldDefinition(FieldType.INTEGER, generation_pattern="agent_number"),
    }),
    
    "life": InsuranceSchema("life", {
        "policyId": FieldDefinition(FieldType.STRING, generation_pattern="policy_id"),
        "insuranceType": FieldDefinition(FieldType.STRING, generation_pattern="life_insurance_type"),
        "policyName": FieldDefinition(FieldType.STRING, generation_pattern="life_policy_name"),
        "startDate": FieldDefinition(FieldType.STRING, generation_pattern="date"),
        "insuredName": FieldDefinition(FieldType.STRING, generation_pattern="name"),
        "originalPolicyName": FieldDefinition(FieldType.STRING, generation_pattern="life_policy_name"),
        "classification": FieldDefinition(FieldType.STRING, generation_pattern="classification"),
        "isActive": FieldDefinition(FieldType.BOOLEAN),
        "isExpired": FieldDefinition(FieldType.BOOLEAN),
        "isKlasi": FieldDefinition(FieldType.BOOLEAN),
        "isRiziko": FieldDefinition(FieldType.BOOLEAN),
        "isCopyPolicyDoc": FieldDefinition(FieldType.BOOLEAN),
        "AgentNumber": FieldDefinition(FieldType.INTEGER, generation_pattern="agent_number"),
        "insuranceSum": FieldDefinition(FieldType.OBJECT, required=False),  # Can be null
        "sum": FieldDefinition(FieldType.NULL, required=False),  # Usually null
        "currency": FieldDefinition(FieldType.STRING, generation_pattern="currency"),
        "value": FieldDefinition(FieldType.INTEGER, generation_pattern="insurance_value"),
    }),
    
    "business": InsuranceSchema("business", {
        "policyId": FieldDefinition(FieldType.STRING, generation_pattern="policy_id"),
        "insuranceType": FieldDefinition(FieldType.STRING, generation_pattern="business_insurance_type"),
        "policyName": FieldDefinition(FieldType.STRING, generation_pattern="business_policy_name"),
        "startDate": FieldDefinition(FieldType.STRING, generation_pattern="date"),
        "endDate": FieldDefinition(FieldType.STRING, generation_pattern="date"),
        "classification": FieldDefinition(FieldType.STRING, generation_pattern="classification"),
        "isExpired": FieldDefinition(FieldType.BOOLEAN),
        "AgentNumber": FieldDefinition(FieldType.INTEGER, generation_pattern="agent_number"),
    }),
    
    "dental": InsuranceSchema("dental", {
        "policyId": FieldDefinition(FieldType.STRING, generation_pattern="policy_id"),
        "policyName": FieldDefinition(FieldType.STRING, generation_pattern="dental_policy_name"),
        "startDate": FieldDefinition(FieldType.STRING, generation_pattern="date"),
        "endDate": FieldDefinition(FieldType.STRING, generation_pattern="date"),
        "insuredName": FieldDefinition(FieldType.STRING, generation_pattern="name"),
        "originalPolicyName": FieldDefinition(FieldType.STRING, generation_pattern="dental_policy_name"),
        "classification": FieldDefinition(FieldType.STRING, generation_pattern="classification"),
        "beneficiariesCount": FieldDefinition(FieldType.INTEGER, generation_pattern="beneficiaries_count"),
        "collectiveNumber": FieldDefinition(FieldType.STRING, generation_pattern="collective_number"),
        "isActive": FieldDefinition(FieldType.BOOLEAN),
        "isExpired": FieldDefinition(FieldType.BOOLEAN),
    }),
    
    "dira": InsuranceSchema("dira", {
        "policyId": FieldDefinition(FieldType.STRING, generation_pattern="policy_id"),
        "insuranceType": FieldDefinition(FieldType.STRING, generation_pattern="dira_insurance_type"),
        "policyName": FieldDefinition(FieldType.STRING, generation_pattern="dira_policy_name"),
        "startDate": FieldDefinition(FieldType.STRING, generation_pattern="date"),
        "endDate": FieldDefinition(FieldType.STRING, generation_pattern="date"),
        "address": FieldDefinition(FieldType.STRING, generation_pattern="address"),
        "description": FieldDefinition(FieldType.STRING, generation_pattern="dira_description"),
        "isActive": FieldDefinition(FieldType.BOOLEAN),
        "isExpired": FieldDefinition(FieldType.BOOLEAN),
        "isSmart": FieldDefinition(FieldType.BOOLEAN),
        "AgentNumber": FieldDefinition(FieldType.INTEGER, generation_pattern="agent_number"),
    }),
    
    "other": InsuranceSchema("other", {
        "policyId": FieldDefinition(FieldType.STRING, generation_pattern="policy_id"),
        "insuranceType": FieldDefinition(FieldType.STRING, generation_pattern="other_insurance_type"),
        "policyName": FieldDefinition(FieldType.STRING, generation_pattern="other_policy_name"),
        "startDate": FieldDefinition(FieldType.STRING, generation_pattern="date"),
        "endDate": FieldDefinition(FieldType.STRING, generation_pattern="date"),
        "classification": FieldDefinition(FieldType.STRING, generation_pattern="classification"),
        "sectorId": FieldDefinition(FieldType.STRING, generation_pattern="sector_id"),
        "validityTime": FieldDefinition(FieldType.STRING, generation_pattern="date"),
        "isExpired": FieldDefinition(FieldType.BOOLEAN),
        "AgentNumber": FieldDefinition(FieldType.INTEGER, generation_pattern="agent_number"),
    }),
    
    # vehicleUnited is the most complex - it includes all vehicle fields plus nested structures
    "vehicleUnited": InsuranceSchema("vehicleUnited", {
        "policyId": FieldDefinition(FieldType.STRING, generation_pattern="policy_id"),
        "insuranceType": FieldDefinition(FieldType.STRING, generation_pattern="vehicle_insurance_type"),
        "policyName": FieldDefinition(FieldType.STRING, generation_pattern="vehicle_policy_name"),
        "startDate": FieldDefinition(FieldType.STRING, generation_pattern="date"),
        "endDate": FieldDefinition(FieldType.STRING, generation_pattern="date"),
        "modelType": FieldDefinition(FieldType.STRING, generation_pattern="vehicle_model"),
        "licensePlate": FieldDefinition(FieldType.STRING, generation_pattern="license_plate"),
        "classification": FieldDefinition(FieldType.STRING, generation_pattern="classification"),
        "carPolicyType": FieldDefinition(FieldType.STRING, generation_pattern="car_policy_type"),
        "sectorId": FieldDefinition(FieldType.STRING, generation_pattern="sector_id"),
        "validityTime": FieldDefinition(FieldType.STRING, generation_pattern="date"),
        "isExpired": FieldDefinition(FieldType.BOOLEAN),
        "isActive": FieldDefinition(FieldType.BOOLEAN),
        "isSmart": FieldDefinition(FieldType.BOOLEAN),
        "AgentNumber": FieldDefinition(FieldType.INTEGER, generation_pattern="agent_number"),
        # Complex nested structures
        "vehicleUnitedDetail": FieldDefinition(FieldType.OBJECT, required=True),
        # Additional fields found in production
        "list": FieldDefinition(FieldType.ARRAY, required=False),
    }),
    
    # MyMoney unified schema for financial products (gemel, hishtalmut, gemelInvestment)
    "mymoney": InsuranceSchema("mymoney", {
        # Top header structure
        "topHeader": FieldDefinition(FieldType.OBJECT, generation_pattern="mymoney_top_header"),
        # Main header structure  
        "mainHeader": FieldDefinition(FieldType.OBJECT, generation_pattern="mymoney_main_header"),
        # Accumulation by product
        "accumulationByProduct": FieldDefinition(FieldType.OBJECT, generation_pattern="mymoney_accumulation"),
        # Product list with policies
        "productList": FieldDefinition(FieldType.OBJECT, generation_pattern="mymoney_product_list"),
        # Last actions
        "lastActions": FieldDefinition(FieldType.OBJECT, generation_pattern="mymoney_last_actions"),
    }),
}

def get_schema(insurance_type: str) -> Optional[InsuranceSchema]:
    """Get schema for a specific insurance type."""
    return INSURANCE_SCHEMAS.get(insurance_type)

def get_available_insurance_types() -> List[str]:
    """Get list of all available insurance types."""
    return list(INSURANCE_SCHEMAS.keys())

def validate_insurance_data(insurance_type: str, data: Dict[str, Any]) -> List[str]:
    """Validate insurance data against its schema."""
    schema = get_schema(insurance_type)
    if not schema:
        return [f"Unknown insurance type: {insurance_type}"]
    
    return schema.validate_data(data) 