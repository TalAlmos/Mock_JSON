# Mock Data Generator for Chatbot Testing

This Python script generates anonymized mock JSON data for chatbot testing by analyzing Swagger (OpenAPI) schemas and example data files.

## Features

✅ Loads a local Swagger (OpenAPI) JSON file  
✅ Loads local data example JSON files  
✅ Parses schema definitions  
✅ Generates mock data based on object definitions  
✅ Outputs anonymized mock JSON files for chatbot testing  
✅ **NEW**: Preserves original values for specified fields  

## Prerequisites

- Python 3.7 or higher
- Required Python packages (see `requirements.txt`)

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Directory Structure

The script expects the following directory structure:
```
D:\Mock_JSON\
├── data\
│   ├── swagger\          # Contains Swagger/OpenAPI JSON files
│   ├── examples\         # Contains example JSON data files
│   └── mock_output\      # Output directory for generated mock data
├── mock_data_generator.py
├── example_usage.py      # Example of using preserve functionality
└── README.md
```

## Usage

### Basic Usage

1. Ensure your data files are in the correct directories:
   - Swagger file: `D:\Mock_JSON\data\swagger\`
   - Example files: `D:\Mock_JSON\data\examples\`

2. Run the script:
```bash
python mock_data_generator.py
```

3. When prompted, enter the number of mock records to generate per schema (default: 10)

4. The script will:
   - Analyze all example files to identify schema structures
   - Generate mock data for each unique schema found
   - Save one JSON file per schema to `D:\Mock_JSON\data\mock_output\`

### Advanced Usage with Preserve Functionality

The script includes a **preserve functionality** that allows you to specify which fields should keep their original values from the example data instead of being anonymized.

#### Default Preserved Fields

The script automatically preserves these fields:
- **API Response Metadata**: `status`, `message`, `transId`, `entity`
- **Boolean Flags**: `requiredRenewal`, `isExpired`, `isActive`, `isSmart`, `isKlasi`, `isRiziko`, `isCopyPolicyDoc`, `isPaila`, `isIndependent`, `isNew`
- **Special Values**: `sign` (for percentage signs), `eSite` (URLs that might be None)
- **Nullable Fields**: Various fields that should remain null or empty

#### Customizing Preserved Fields

You can customize which fields are preserved using the provided methods:

```python
from mock_data_generator import MockDataGenerator

# Create generator
generator = MockDataGenerator()

# Add fields to preserve
generator.add_preserve_field("policyNumber")
generator.add_preserve_field("customerId")

# Remove fields from preserve list
generator.remove_preserve_field("totalPayments")

# List current preserve fields
generator.list_preserve_fields()

# Run the generator
generator.run()
```

#### Example Usage Script

Run the example script to see how to customize preserve fields:
```bash
python example_usage.py
```

## How It Works

1. **Schema Analysis**: The script analyzes example JSON files to understand data structures
2. **Type Detection**: Automatically detects data types (string, number, boolean, array, object)
3. **Smart Mocking**: Generates appropriate mock data based on field names:
   - Names, emails, phone numbers → Faker-generated realistic data
   - IDs, policy numbers → Random numeric identifiers
   - Dates → Random dates
   - Currency → Random currency symbols
   - Status fields → Random status values
4. **Preserve Functionality**: Maintains original values for specified fields
5. **Anonymization**: All sensitive data is replaced with fake but realistic values
6. **Output**: Creates separate JSON files for each schema type found

## Output Files

Generated files will be named `mock_[SchemaName].json` and contain:
- Multiple mock records per schema
- Realistic but anonymized data
- Preserved original values for specified fields
- Metadata including mock ID and generation timestamp

## Example Output

```json
[
  {
    "id": "vehicleUnited",
    "data": [
      {
        "vehicleUnitedDetail": {
          "insuranceDetails": {
            "requiredRenewal": true,  // ← Preserved original value
            "isExpired": false,       // ← Preserved original value
            "premia": {
              "value": 500000.0,      // ← Generated mock value
              "currency": "₪"         // ← Generated mock value
            }
          }
        }
      }
    ]
  }
]
```

## Customization

You can modify the script to:
- Add more field name patterns for better mock data generation
- Change the output format
- Adjust the number of records generated per schema
- Add more data types or validation rules
- **Customize which fields preserve original values**

## Troubleshooting

- **No files found**: Ensure your JSON files are in the correct directories
- **Encoding issues**: The script uses UTF-8 encoding for Hebrew text
- **Memory issues**: For very large files, consider processing them in batches
- **Preserve fields not working**: Check that field names match exactly (case-sensitive)

## License

This script is provided as-is for educational and testing purposes. 