#!/usr/bin/env python3
"""
Insurance Validator for Mock Data Generation

This module provides the InsuranceValidator class for insurance-specific
validation rules and business logic.
"""

from typing import Dict, Any, List, Optional
from .base_validator import BaseValidator
from .schema_validator import SchemaValidator
from .data_validator import DataValidator


class InsuranceValidator(BaseValidator):
    """
    Validator for insurance-specific data validation.
    
    This class provides insurance-specific validation rules and business logic,
    combining schema validation with insurance domain knowledge.
    """
    
    def __init__(self):
        """Initialize the insurance validator."""
        super().__init__()
        self.schema_validator = SchemaValidator()
        self.data_validator = DataValidator()
    
    def validate(self, data: Any, insurance_type: str = None) -> bool:
        """
        Validate insurance data.
        
        Args:
            data: Data to validate
            insurance_type: Optional insurance type for specific validation
            
        Returns:
            True if validation passes, False otherwise
        """
        self.clear_errors()
        
        # Basic data validation
        if not self.data_validator.validate(data):
            self.validation_errors.extend(self.data_validator.get_errors())
            self.validation_warnings.extend(self.data_validator.get_warnings())
        
        # Insurance-specific validation
        if isinstance(data, dict):
            if not self._validate_insurance_specific(data, insurance_type):
                return False
        
        return not self.has_errors()
    
    def _validate_insurance_specific(self, data: Dict[str, Any], insurance_type: str = None) -> bool:
        """Validate insurance-specific rules."""
        is_valid = True
        
        # Determine insurance type from data if not provided
        if not insurance_type:
            insurance_type = data.get("insurance_type", data.get("id"))
        
        if insurance_type:
            # Validate based on insurance type
            if insurance_type == "vehicleUnited":
                is_valid &= self._validate_vehicle_insurance(data)
            elif insurance_type == "travel":
                is_valid &= self._validate_travel_insurance(data)
            elif insurance_type == "mymoney":
                is_valid &= self._validate_mymoney_data(data)
            elif insurance_type == "health":
                is_valid &= self._validate_health_insurance(data)
            elif insurance_type == "life":
                is_valid &= self._validate_life_insurance(data)
            else:
                is_valid &= self._validate_general_insurance(data)
        
        return is_valid
    
    def _validate_vehicle_insurance(self, data: Dict[str, Any]) -> bool:
        """Validate vehicle insurance specific rules."""
        is_valid = True
        
        # Check for vehicle-specific fields
        vehicle_fields = ["modelType", "licensePlate", "carPolicyType"]
        for field in vehicle_fields:
            if field in data:
                if not data[field]:
                    self.add_warning(f"Vehicle field '{field}' is empty")
        
        # Validate policy types
        if "carPolicyType" in data:
            valid_types = ["makif", "hova", "basic", "premium"]
            if data["carPolicyType"] not in valid_types:
                self.add_error(f"Invalid car policy type: {data['carPolicyType']}")
                is_valid = False
        
        # Validate vehicle details if present
        if "vehicleUnitedDetail" in data:
            detail = data["vehicleUnitedDetail"]
            if isinstance(detail, dict):
                if "insuranceDetails" in detail:
                    is_valid &= self._validate_insurance_details(detail["insuranceDetails"])
        
        return is_valid
    
    def _validate_travel_insurance(self, data: Dict[str, Any]) -> bool:
        """Validate travel insurance specific rules."""
        is_valid = True
        
        # Check for travel-specific fields
        travel_fields = ["destination", "tripDuration", "coverageType"]
        for field in travel_fields:
            if field in data:
                if not data[field]:
                    self.add_warning(f"Travel field '{field}' is empty")
        
        # Validate coverage structure
        coverage_fields = ["basicCoverage", "loggage", "searchRescue", "corona"]
        for field in coverage_fields:
            if field in data:
                coverage = data[field]
                if isinstance(coverage, dict):
                    if "insuredList" in coverage:
                        if not coverage["insuredList"]:
                            self.add_warning(f"Coverage '{field}' has empty insured list")
        
        return is_valid
    
    def _validate_mymoney_data(self, data: Dict[str, Any]) -> bool:
        """Validate MyMoney financial data specific rules."""
        is_valid = True
        
        # Check for financial-specific fields
        financial_fields = ["sumSaving", "totalSaving", "fluentWithdraw"]
        for field in financial_fields:
            if field in data:
                if isinstance(data[field], dict) and "value" in data[field]:
                    value = data[field]["value"]
                    if value < 0:
                        self.add_warning(f"Financial field '{field}' has negative value")
        
        # Validate product types
        if "productData" in data:
            product_data = data["productData"]
            if isinstance(product_data, dict):
                if "policyType" in product_data:
                    valid_types = ["gemel", "hishtalmut", "gemelInvestment"]
                    if product_data["policyType"] not in valid_types:
                        self.add_error(f"Invalid product type: {product_data['policyType']}")
                        is_valid = False
        
        return is_valid
    
    def _validate_health_insurance(self, data: Dict[str, Any]) -> bool:
        """Validate health insurance specific rules."""
        is_valid = True
        
        # Check for health-specific fields
        health_fields = ["beneficiaries", "coverageType", "deductible"]
        for field in health_fields:
            if field in data:
                if not data[field]:
                    self.add_warning(f"Health field '{field}' is empty")
        
        # Validate beneficiaries count
        if "beneficiaries" in data:
            beneficiaries = data["beneficiaries"]
            if isinstance(beneficiaries, int) and beneficiaries < 1:
                self.add_error("Beneficiaries count must be at least 1")
                is_valid = False
        
        return is_valid
    
    def _validate_life_insurance(self, data: Dict[str, Any]) -> bool:
        """Validate life insurance specific rules."""
        is_valid = True
        
        # Check for life-specific fields
        life_fields = ["coverageAmount", "policyType", "beneficiaries"]
        for field in life_fields:
            if field in data:
                if not data[field]:
                    self.add_warning(f"Life insurance field '{field}' is empty")
        
        # Validate coverage amount
        if "coverageAmount" in data:
            if isinstance(data["coverageAmount"], dict) and "value" in data["coverageAmount"]:
                amount = data["coverageAmount"]["value"]
                if amount < 10000:  # Minimum coverage
                    self.add_warning("Life insurance coverage amount seems low")
        
        return is_valid
    
    def _validate_general_insurance(self, data: Dict[str, Any]) -> bool:
        """Validate general insurance rules."""
        is_valid = True
        
        # Check for general insurance fields
        general_fields = ["policyId", "insuranceType", "startDate", "endDate"]
        for field in general_fields:
            if field in data:
                if not data[field]:
                    self.add_warning(f"General insurance field '{field}' is empty")
        
        return is_valid
    
    def _validate_insurance_details(self, details: Dict[str, Any]) -> bool:
        """Validate insurance details structure."""
        is_valid = True
        
        # Check for required fields
        required_fields = ["startDate", "endDate", "premia"]
        for field in required_fields:
            if field not in details:
                self.add_error(f"Missing required insurance detail field: {field}")
                is_valid = False
        
        # Validate premium structure
        if "premia" in details:
            premia = details["premia"]
            if isinstance(premia, dict):
                if "value" not in premia:
                    self.add_error("Premium missing 'value' field")
                    is_valid = False
                elif "currency" not in premia:
                    self.add_error("Premium missing 'currency' field")
                    is_valid = False
        
        return is_valid
    
    def validate_against_schema(self, data: Any, schema: Dict[str, Any]) -> bool:
        """
        Validate data against a specific schema.
        
        Args:
            data: Data to validate
            schema: Schema definition
            
        Returns:
            True if validation passes, False otherwise
        """
        # Use schema validator
        if not self.schema_validator.validate(data, schema):
            self.validation_errors.extend(self.schema_validator.get_errors())
            self.validation_warnings.extend(self.schema_validator.get_warnings())
            return False
        
        return True
    
    def validate_insurance_record(self, data: Dict[str, Any], insurance_type: str) -> bool:
        """
        Validate a complete insurance record.
        
        Args:
            data: Insurance record data
            insurance_type: Type of insurance
            
        Returns:
            True if validation passes, False otherwise
        """
        self.clear_errors()
        
        # Basic data validation
        if not self.data_validator.validate(data):
            self.validation_errors.extend(self.data_validator.get_errors())
            self.validation_warnings.extend(self.data_validator.get_warnings())
        
        # Insurance-specific validation
        if not self._validate_insurance_specific(data, insurance_type):
            return False
        
        # Data consistency validation
        if not self.data_validator.validate_data_consistency(data):
            self.validation_errors.extend(self.data_validator.get_errors())
            self.validation_warnings.extend(self.data_validator.get_warnings())
        
        # Data quality validation
        if not self.data_validator.validate_data_quality(data):
            self.validation_errors.extend(self.data_validator.get_errors())
            self.validation_warnings.extend(self.data_validator.get_warnings())
        
        return not self.has_errors()
    
    def get_validation_report(self, data: Dict[str, Any], insurance_type: str = None) -> Dict[str, Any]:
        """
        Get a comprehensive validation report.
        
        Args:
            data: Data to validate
            insurance_type: Optional insurance type
            
        Returns:
            Dictionary containing validation report
        """
        is_valid = self.validate_insurance_record(data, insurance_type)
        
        return {
            "is_valid": is_valid,
            "insurance_type": insurance_type,
            "error_count": len(self.validation_errors),
            "warning_count": len(self.validation_warnings),
            "errors": self.validation_errors,
            "warnings": self.validation_warnings,
            "data_quality_score": self._calculate_quality_score(data)
        }
    
    def _calculate_quality_score(self, data: Dict[str, Any]) -> float:
        """Calculate a data quality score (0-100)."""
        if not isinstance(data, dict):
            return 0.0
        
        score = 100.0
        deductions = 0
        
        # Check for empty fields
        empty_fields = sum(1 for value in data.values() if value == "" or value is None)
        if empty_fields > 0:
            deductions += min(empty_fields * 5, 30)  # Max 30 points for empty fields
        
        # Check for missing required fields
        required_fields = ["policyId", "insuranceType", "startDate", "endDate"]
        missing_fields = sum(1 for field in required_fields if field not in data)
        if missing_fields > 0:
            deductions += missing_fields * 10  # 10 points per missing required field
        
        # Check for data type issues
        type_issues = 0
        for key, value in data.items():
            if key in ["amount", "value"] and not isinstance(value, (int, float)):
                type_issues += 1
            if key in ["isActive", "isExpired"] and not isinstance(value, bool):
                type_issues += 1
        
        if type_issues > 0:
            deductions += type_issues * 5  # 5 points per type issue
        
        return max(0.0, score - deductions) 