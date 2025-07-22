# Development Plan: Closing Key Gaps

## 1. Example-Driven Value Generation
**Goal:** Make mock data more realistic by learning from real example values.

- [x] Create `example_analyzer.py` utility to scan `data/examples/` and build field value profiles (common values, ranges, etc.).

---

## 2. Separate Generators for Major Insurance Types
**Goal:** Improve maintainability and extensibility by having a dedicated generator class for each major insurance type.

- [x] Scaffold new generator classes: `TravelInsuranceGenerator`, `VehicleUnitedGenerator`, `MyMoneyGenerator`, etc., inheriting from `BaseGenerator`.
- [x] Refactor type-specific logic from legacy script into the appropriate generator class.
- [x] Register each generator in `GeneratorFactory` for its insurance type.

---

## 3. Generator/Factory Integration
**Goal:** Use example-driven profiles in data generation.

- [x] Update `InsuranceGenerator` (and other generators) to accept a `field_profiles` dictionary.
- [x] In value generation, use example values with a tunable probability; fallback to Faker otherwise.
- [x] Update `GeneratorFactory` and CLI to analyze examples at startup and inject profiles.
- [x] Integrate profiles into generator/factory

---

## 4. Add/Update Tests for Each Generator
**Goal:** Ensure correctness and coverage for each generator class.

- [x] Add or update tests for each generator class in `tests/`.

---

## 5. User-Facing Preserve Fields Customization
**Goal:** Allow users to easily add/remove/list preserve fields via CLI or config.

- [x] Add CLI options to `main.py` for:
    - Listing current preserve fields
    - Adding a field to preserve
    - Removing a field from preserve
- [x] Optionally, support preserve fields in a YAML config file.
- [x] Update documentation to show how to use these features.

---

## 6. Example Data Analysis/Reporting
**Goal:** Provide transparency and debugging by reporting what’s in the example data.

- [x] Extend `example_analyzer.py` to output a summary report (insurance types, field structures, value distributions).
- [x] Add a CLI option to generate and print this report.
- [x] Optionally, save the report as JSON for further analysis.

---

## 7. Interactive CLI Mode
**Goal:** Make the CLI more user-friendly for non-technical users.

- [ ] Add an interactive mode to `main.py` (e.g., if no arguments are given, prompt user for type, number of records, etc.).
- [ ] Optionally, provide menus for preserve fields and output options.

---

## 8. Documentation Update
**Goal:** Ensure users and contributors understand all features and workflows.

- [ ] Update `README.md` with:
    - New CLI usage examples (including preserve fields and analysis)
    - Feature highlights (example-driven generation, preserve fields, etc.)
    - Migration notes and legacy comparison
- [ ] Update or archive `Guide.txt` and `migration_quick_reference.md` as needed.

---

## Suggested Implementation Order

1. Example Analyzer Utility (foundation for other features)
2. Scaffold separate generator classes for major insurance types
3. Refactor type-specific logic into new generator classes
4. Register generators in factory
5. Integrate profiles into generator/factory
6. Add/Update tests for each generator
7. Preserve Fields CLI/Config
8. Analysis/Reporting CLI Option
9. Interactive CLI Mode
10. Documentation Update

---

## Sample Task Breakdown

| Task                                      | File(s) to Touch                | Test/Validation                |
|--------------------------------------------|---------------------------------|-------------------------------|
| Build example analyzer utility             | `example_analyzer.py`           | Unit test, CLI output         |
| Scaffold separate generator classes        | `generators/`                   | Unit/integration tests        |
| Refactor type-specific logic               | `generators/`                   | Test generated data realism   |
| Register generators in factory             | `factories/generator_factory.py` | CLI test, type listing        |
| Integrate profiles into generator/factory  | `generators/`, `factories/`     | Test generated data realism   |
| Add/Update tests for each generator        | `tests/`                        | pytest                        |
| Add preserve fields CLI/config             | `main.py`, `config.py`          | CLI test, config reload       |
| Add analysis/reporting CLI                 | `main.py`, `example_analyzer.py`| CLI test, report file         |
| Add interactive CLI mode                   | `main.py`                       | Manual/automated CLI test     |
| Update documentation                       | `README.md`, `Guide.txt`        | Review, user feedback         | 