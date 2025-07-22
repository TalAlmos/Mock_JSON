import json
import os
from collections import defaultdict, Counter
from typing import Dict, List
import argparse

# Fields that should never use real example values (PII)
PII_FIELDS = {"name", "firstName", "lastName", "id", "idNumber", "email", "phone", "address"}

def analyze_examples(example_dir: str = "data/examples/") -> Dict[str, List]:
    """
    Scan example files and build a profile of common values for each field, excluding PII fields.
    Returns a dict: {field_name: [most_common_values]}
    """
    field_profiles = defaultdict(Counter)
    for filename in os.listdir(example_dir):
        if filename.endswith(".json"):
            with open(os.path.join(example_dir, filename), 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    flatten_and_count(data, field_profiles)
                except Exception as e:
                    print(f"Warning: Could not process {filename}: {e}")
    # Convert counters to lists of most common values
    return {k: [v for v, _ in counter.most_common(10)] for k, counter in field_profiles.items()}

def flatten_and_count(d, profiles, prefix=''):
    if isinstance(d, dict):
        for k, v in d.items():
            key = f"{prefix}.{k}" if prefix else k
            if k in PII_FIELDS:
                continue  # Skip PII fields
            flatten_and_count(v, profiles, key)
    elif isinstance(d, list):
        for item in d:
            flatten_and_count(item, profiles, prefix)
    else:
        if prefix.split('.')[-1] not in PII_FIELDS:
            profiles[prefix][d] += 1

def summarize_examples(example_dir: str = "data/examples/") -> Dict:
    """
    Output a summary report: insurance types, field structures, value distributions.
    """
    summary = {
        "insurance_types": set(),
        "fields": set(),
        "value_distributions": defaultdict(Counter)
    }
    for filename in os.listdir(example_dir):
        if filename.endswith(".json"):
            with open(os.path.join(example_dir, filename), 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    # Try to infer insurance type from filename or top-level keys
                    insurance_type = filename.split('_')[0] if '_' in filename else filename.replace('.json', '')
                    summary["insurance_types"].add(insurance_type)
                    collect_fields_and_values(data, summary["fields"], summary["value_distributions"])
                except Exception as e:
                    print(f"Warning: Could not process {filename}: {e}")
    # Convert sets to sorted lists for output
    summary["insurance_types"] = sorted(summary["insurance_types"])
    summary["fields"] = sorted(summary["fields"])
    # Convert value distributions to dict of most common values
    summary["value_distributions"] = {
        k: [v for v, _ in counter.most_common(10)] for k, counter in summary["value_distributions"].items()
    }
    return summary

def collect_fields_and_values(d, fields_set, value_distributions, prefix=''):
    if isinstance(d, dict):
        for k, v in d.items():
            key = f"{prefix}.{k}" if prefix else k
            if k in PII_FIELDS:
                continue
            fields_set.add(key)
            collect_fields_and_values(v, fields_set, value_distributions, key)
    elif isinstance(d, list):
        for item in d:
            collect_fields_and_values(item, fields_set, value_distributions, prefix)
    else:
        if prefix.split('.')[-1] not in PII_FIELDS:
            value_distributions[prefix][d] += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze example JSON files and output a summary report.")
    parser.add_argument("--dir", type=str, default="data/examples/", help="Directory with example JSON files")
    parser.add_argument("--json", type=str, help="Output summary as JSON to this file")
    args = parser.parse_args()

    summary = summarize_examples(args.dir)
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
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"\nSummary saved to {args.json}") 