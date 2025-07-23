# Mock Data Generator for Chatbot Testing

This Python project generates anonymized mock JSON data for chatbot testing by analyzing Swagger (OpenAPI) schemas and example data files. It features a modular, extensible, and testable architecture with a modern, menu-driven CLI, YAML-based configuration, and advanced example-driven data generation.

## Features

✅ Modular architecture: command pattern, factory/registry, validators, config management  
✅ Loads a local Swagger (OpenAPI) JSON file  
✅ Loads local data example JSON files  
✅ Parses schema definitions and analyzes example data  
✅ Generates mock data based on object definitions and real value distributions  
✅ Outputs anonymized mock JSON files for chatbot testing  
✅ **Preserves original values for specified fields**  
✅ **Menu-driven interactive CLI**  
✅ **YAML config for preserve fields and paths**  
✅ **Example-driven value generation with Faker fallback**  
✅ **Example data analysis/reporting**  
✅ **Comprehensive validation and error handling**

## Prerequisites

- Python 3.7 or higher
- Required Python packages (see `requirements.txt`)

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
├── commands/             # Command pattern implementations
├── factories/            # Generator factory
├── generators/           # Insurance type-specific generators
├── validators/           # Data and schema validators
├── cache/                # Caching for schema analysis
├── tests/                # Automated tests
```

## Architecture Overview

- **main.py**: Entry point. Handles CLI parsing, interactive menu, and command dispatch.
- **commands/**: Implements the command pattern for CLI and menu actions (e.g., generate, list types, manage preserve fields).
- **factories/generator_factory.py**: Factory for creating insurance type generators, injecting config and example-driven profiles.
- **generators/**: Contains a base generator and type-specific generators (e.g., Travel, VehicleUnited, MyMoney, ExcellenceSaving). Each generator uses both example-driven and Faker-based value generation.
- **validators/**: Validation framework for generated data and schemas.
- **config.py / config.yaml**: Centralized configuration management (paths, preserve fields, etc.).
- **cache/**: Caching for schema analysis to optimize performance.
- **schema_analyzer.py**: Analyzes example data to extract schema and value distributions.
- **tests/**: Comprehensive automated tests for all major components.

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
- **Generate Data**: Choose insurance type, number of records, and output file interactively. Optionally save each record as a separate file with a unique 9-digit ID.
- **List Available Types**: View all supported insurance types.
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
  # Save each record as a separate file
  python3 main.py --type travel --num-records 5 --separate-files
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

1. **Schema Analysis**: Analyzes example JSON files to understand data structures and value distributions.
2. **Type Detection**: Detects data types (string, number, boolean, array, object).
3. **Example-Driven Generation**: Uses real value distributions from examples with a tunable probability; falls back to Faker for realism and privacy.
4. **Preserve Functionality**: Maintains original values for specified fields (customizable via config or CLI).
5. **Anonymization**: All sensitive data is replaced with fake but realistic values.
6. **Validation**: Generated data is validated against schemas and business rules.
7. **Output**: Creates separate JSON files for each schema type found, with options for single or per-record output.

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

## Main Modules and Responsibilities

- **main.py**: CLI entry point, menu, and command dispatch
- **commands/**: Command pattern for CLI/menu actions
- **factories/generator_factory.py**: Generator creation and registration
- **generators/**: Type-specific data generators (Travel, VehicleUnited, MyMoney, ExcellenceSaving, etc.)
- **validators/**: Data and schema validation
- **config.py / config.yaml**: Centralized configuration
- **cache/**: Caching for schema analysis
- **schema_analyzer.py**: Example data analysis and schema extraction
- **tests/**: Automated tests for all features

## Migration Notes & Legacy Comparison

- The legacy `mock_data_generator.py` has been replaced by a modular, testable, and extensible architecture.
- All configuration is now centralized in `config.py` and `config.yaml`.
- The new CLI supports both direct commands and a user-friendly interactive menu.
- Example-driven generation and Faker fallback ensure realistic, privacy-safe mock data.
- All major features are covered by automated tests.
- The architecture now uses the command pattern, factory/registry, and validators for maintainability and extensibility.

## Troubleshooting

- **No files found**: Ensure your JSON files are in the correct directories
- **Encoding issues**: The script uses UTF-8 encoding for Hebrew text
- **Preserve fields not working**: Check that field names match exactly (case-sensitive)
- **YAML config not updating**: Use the CLI or menu to update preserve fields, or edit `config.yaml` directly

## License

This script is provided as-is for educational and testing purposes. 