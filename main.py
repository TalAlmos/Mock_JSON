import argparse
from config import Config
from commands.generator_context import GeneratorContext
from commands.generate_command import GenerateCommand
from commands.list_types_command import ListTypesCommand
from factories.generator_factory import GeneratorFactory
from example_analyzer import analyze_examples, summarize_examples
import glob
import os
import yaml


def interactive_menu():
    config_path = "config.yaml"
    config = Config.from_yaml_file(config_path) if os.path.exists(config_path) else Config()
    example_files = glob.glob("data/examples/*.json")
    field_profiles = analyze_examples("data/examples/")
    factory = GeneratorFactory(config, field_profiles)
    context = GeneratorContext(config)
    context.factory = factory

    def save_config_to_yaml(cfg, path):
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(cfg.to_dict(), f, allow_unicode=True, sort_keys=False)

    while True:
        print("\n=== Mock Insurance Data Generator ===")
        print("1. Generate Data")
        print("2. List Available Types")
        print("3. Manage Preserve Fields")
        print("4. Analyze Example Data")
        print("5. Exit")
        choice = input("Select an option (1-5): ").strip()
        if choice == "1":
            types_command = ListTypesCommand()
            types = types_command.execute(context)
            print("\nAvailable types:")
            for idx, t in enumerate(types, 1):
                print(f"{idx}. {t['insurance_type']}")
            type_idx = input("Select insurance type by number: ").strip()
            try:
                type_idx = int(type_idx)
                insurance_type = types[type_idx-1]['insurance_type']
            except Exception:
                print("Invalid selection.")
                continue
            num_records = input("How many records to generate? (default 5): ").strip()
            num_records = int(num_records) if num_records.isdigit() else 5
            output_file = input("Output file (leave blank to print to screen): ").strip()
            command = GenerateCommand(insurance_type, num_records)
            try:
                records = command.execute(context)
            except Exception as e:
                print(f"Error: {e}")
                continue
            import json
            if output_file:
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(records, f, ensure_ascii=False, indent=2)
                print(f"Generated records saved to {output_file}")
            else:
                print(json.dumps(records, ensure_ascii=False, indent=2))
        elif choice == "2":
            types_command = ListTypesCommand()
            types = types_command.execute(context)
            print("\nAvailable types:")
            for t in types:
                print(f"- {t['insurance_type']}")
        elif choice == "3":
            while True:
                print("\n--- Manage Preserve Fields ---")
                print("1. List Preserve Fields")
                print("2. Add Preserve Field")
                print("3. Remove Preserve Field")
                print("4. Back to Main Menu")
                pf_choice = input("Select an option (1-4): ").strip()
                if pf_choice == "1":
                    print("Current preserve fields:")
                    for field in sorted(config.list_preserve_fields()):
                        print(f"- {field}")
                elif pf_choice == "2":
                    field = input("Enter field name to add: ").strip()
                    config.add_preserve_field(field)
                    save_config_to_yaml(config, config_path)
                    print(f"Added '{field}' to preserve fields.")
                elif pf_choice == "3":
                    field = input("Enter field name to remove: ").strip()
                    config.remove_preserve_field(field)
                    save_config_to_yaml(config, config_path)
                    print(f"Removed '{field}' from preserve fields.")
                elif pf_choice == "4":
                    break
                else:
                    print("Invalid selection.")
        elif choice == "4":
            summary = summarize_examples("data/examples/")
            print("Insurance types found:")
            for t in summary["insurance_types"]:
                print(f"- {t}")
            print(f"\nTotal unique fields: {len(summary['fields'])}")
            print("Sample fields:")
            for f in summary["fields"][:10]:
                print(f"- {f}")
            print("\nSample value distributions:")
            for k, v in list(summary["value_distributions"].items())[:10]:
                print(f"- {k}: {v}")
            save_json = input("Save this summary as JSON? (y/n): ").strip().lower()
            if save_json == "y":
                json_file = input("Enter filename (e.g., example_report.json): ").strip()
                import json
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(summary, f, ensure_ascii=False, indent=2)
                print(f"Summary saved to {json_file}")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid selection.")

def main():
    parser = argparse.ArgumentParser(description="Mock Insurance Data Generator")
    parser.add_argument("--type", help="Insurance type to generate (e.g., travel, health, all)")
    parser.add_argument("--num-records", type=int, default=5, help="Number of records to generate")
    parser.add_argument("--list-types", action="store_true", help="List available insurance types")
    parser.add_argument("--output", type=str, help="Output file to save generated records (optional)")
    # Preserve fields CLI options
    parser.add_argument("--list-preserve-fields", action="store_true", help="List current preserve fields")
    parser.add_argument("--add-preserve-field", type=str, help="Add a field to preserve fields list")
    parser.add_argument("--remove-preserve-field", type=str, help="Remove a field from preserve fields list")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to YAML config file (default: config.yaml)")
    # Example analysis/reporting CLI options
    parser.add_argument("--analyze-examples", action="store_true", help="Print a summary report of example data analysis")
    parser.add_argument("--analyze-examples-json", type=str, help="Save example data analysis summary as JSON to this file")
    args = parser.parse_args()

    # If no arguments are given, launch interactive menu
    if len([v for k, v in vars(args).items() if v not in (None, False)]) == 0:
        interactive_menu()
        return

    # Example analysis/reporting
    if args.analyze_examples or args.analyze_examples_json:
        summary = summarize_examples("data/examples/")
        if args.analyze_examples:
            print("Insurance types found:")
            for t in summary["insurance_types"]:
                print(f"- {t}")
            print(f"\nTotal unique fields: {len(summary['fields'])}")
            print("Sample fields:")
            for f in summary["fields"][:10]:
                print(f"- {f}")
            print("\nSample value distributions:")
            for k, v in list(summary["value_distributions"].items())[:10]:
                print(f"- {k}: {v}")
        if args.analyze_examples_json:
            import json
            with open(args.analyze_examples_json, "w", encoding="utf-8") as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            print(f"\nSummary saved to {args.analyze_examples_json}")
        return

    config_path = args.config
    config = None
    if os.path.exists(config_path):
        config = Config.from_yaml_file(config_path)
    else:
        config = Config()

    # Helper to save config back to YAML
    def save_config_to_yaml(cfg, path):
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(cfg.to_dict(), f, allow_unicode=True, sort_keys=False)

    # Handle preserve fields CLI options
    if args.list_preserve_fields:
        print("Current preserve fields:")
        for field in sorted(config.list_preserve_fields()):
            print(f"- {field}")
        return
    if args.add_preserve_field:
        config.add_preserve_field(args.add_preserve_field)
        print(f"Added '{args.add_preserve_field}' to preserve fields.")
        save_config_to_yaml(config, config_path)
        print("Updated preserve fields:")
        for field in sorted(config.list_preserve_fields()):
            print(f"- {field}")
        return
    if args.remove_preserve_field:
        config.remove_preserve_field(args.remove_preserve_field)
        print(f"Removed '{args.remove_preserve_field}' from preserve fields.")
        save_config_to_yaml(config, config_path)
        print("Updated preserve fields:")
        for field in sorted(config.list_preserve_fields()):
            print(f"- {field}")
        return

    # Analyze example files for field profiles
    example_files = glob.glob("data/examples/*.json")
    field_profiles = analyze_examples("data/examples/")
    # Pass field_profiles to factory and context
    factory = GeneratorFactory(config, field_profiles)
    context = GeneratorContext(config)
    context.factory = factory  # Ensure context uses the factory with profiles

    if args.list_types:
        command = ListTypesCommand()
        types = command.execute(context)
        print("Available types:")
        for t in types:
            print(f"- {t['insurance_type']}")
        return

    if args.type:
        command = GenerateCommand(args.type, args.num_records)
        try:
            records = command.execute(context)
        except Exception as e:
            print(f"Error: {e}")
            return
        if args.output:
            import json
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
            print(f"Generated records saved to {args.output}")
        else:
            import json
            print(json.dumps(records, ensure_ascii=False, indent=2))
        return

    parser.print_help()


if __name__ == "__main__":
    main() 