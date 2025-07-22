# Mock Data Generator for Chatbot Testing

This Python project generates anonymized mock JSON data for chatbot testing by analyzing Swagger (OpenAPI) schemas and example data files. It features a modern, menu-driven CLI, YAML-based configuration, and advanced example-driven data generation.

## Features

✅ Loads a local Swagger (OpenAPI) JSON file  
✅ Loads local data example JSON files  
✅ Parses schema definitions  
✅ Generates mock data based on object definitions  
✅ Outputs anonymized mock JSON files for chatbot testing  
✅ **Preserves original values for specified fields**  
✅ **Menu-driven interactive CLI**  
✅ **YAML config for preserve fields and paths**  
✅ **Example-driven value generation with Faker fallback**  
✅ **Example data analysis/reporting**

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
Mock_JSON/
├── data/
│   ├── swagger/          # Contains Swagger/OpenAPI JSON files
│   ├── examples/         # Contains example JSON data files
│   └── mock_output/      # Output directory for generated mock data
├── main.py               # Entry point for CLI and interactive mode
├── config.yaml           # YAML config for paths and preserve fields
├── README.md
```

## Usage

### Menu-Driven Interactive CLI (Recommended)

Just run:
```bash
python3 main.py
```
You'll see a menu:
```
=== Mock Insurance Data Generator ===
1. Generate Data
2. List Available Types
3. Manage Preserve Fields
4. Analyze Example Data
5. Exit
```
- **Generate Data**: Choose insurance type, number of records, and output file interactively.
- **Manage Preserve Fields**: List, add, or remove fields to preserve (updates `config.yaml`).
- **Analyze Example Data**: View a summary of example data and save a report as JSON.

### Command-Line Options

You can also use the CLI directly:
- List available types:
  ```bash
  python3 main.py --list-types
  ```
- Generate data for a type:
  ```bash
  python3 main.py --type travel --num-records 5 --output travel.json
  ```
- List, add, or remove preserve fields:
  ```bash
  python3 main.py --list-preserve-fields
  python3 main.py --add-preserve-field myField
  python3 main.py --remove-preserve-field myField
  ```
- Analyze example data:
  ```bash
  python3 main.py --analyze-examples
  python3 main.py --analyze-examples-json example_report.json
  ```
- Use a custom config file:
  ```bash
  python3 main.py --config myconfig.yaml --list-preserve-fields
  ```

## Configuration

All paths and preserve fields are managed in `config.yaml`:
```yaml
paths:
  swagger: /path/to/data/swagger
  examples: /path/to/data/examples
  output: /path/to/data/mock_output
preserve_fields:
  - status
  - message
  # ...
```
You can edit this file directly or use the CLI/interactive menu to update preserve fields.

## How It Works

1. **Schema Analysis**: Analyzes example JSON files to understand data structures
2. **Type Detection**: Detects data types (string, number, boolean, array, object)
3. **Example-Driven Generation**: Uses real value distributions from examples, with Faker fallback for realism and privacy
4. **Preserve Functionality**: Maintains original values for specified fields (customizable)
5. **Anonymization**: All sensitive data is replaced with fake but realistic values
6. **Output**: Creates separate JSON files for each schema type found

## Example Data Analysis/Reporting

You can analyze your example data to see:
- Insurance types found
- Unique fields
- Value distributions for each field

Run:
```bash
python3 main.py --analyze-examples
python3 main.py --analyze-examples-json example_report.json
```

## Migration Notes & Legacy Comparison

- The legacy `mock_data_generator.py` has been replaced by a modular, testable, and extensible architecture.
- All configuration is now centralized in `config.py` and `config.yaml`.
- The new CLI supports both direct commands and a user-friendly interactive menu.
- Example-driven generation and Faker fallback ensure realistic, privacy-safe mock data.
- All major features are covered by automated tests.

## Troubleshooting

- **No files found**: Ensure your JSON files are in the correct directories
- **Encoding issues**: The script uses UTF-8 encoding for Hebrew text
- **Preserve fields not working**: Check that field names match exactly (case-sensitive)
- **YAML config not updating**: Use the CLI or menu to update preserve fields, or edit `config.yaml` directly

## License

This script is provided as-is for educational and testing purposes. 