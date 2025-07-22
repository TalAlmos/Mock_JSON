# Migration Quick Reference

## Phase-by-Phase Migration Steps

| Phase | Step | File to Create | Test File | Command |
|-------|------|----------------|-----------|---------|
| 1 | 1.1 | `config.py` | `tests/test_config.py` | `pytest tests/test_config.py -v` |
| 1 | 1.2 | - | `tests/test_config_integration.py` | `pytest tests/test_config_integration.py -v` |
| 2 | 2.1 | `generators/base_generator.py` | `tests/test_base_generator.py` | `pytest tests/test_base_generator.py -v` |
| 2 | 2.2 | `generators/registry.py` | `tests/test_registry.py` | `pytest tests/test_registry.py -v` |
| 3 | 3.1 | `generators/insurance_generator.py` | `tests/test_insurance_generator.py` | `pytest tests/test_insurance_generator.py -v` |
| 3 | 3.2 | `schema_analyzer.py` | `tests/test_schema_analyzer.py` | `pytest tests/test_schema_analyzer.py -v` |
| 4 | 4.1 | `factories/generator_factory.py` | `tests/test_factory.py` | `pytest tests/test_factory.py -v` |
| 5 | 5.1 | `commands/` | `tests/test_commands.py` | `pytest tests/test_commands.py -v` |
| 6 | 6.1 | `exceptions.py` | `tests/test_exceptions.py` | `pytest tests/test_exceptions.py -v` |
| 6 | 6.2 | - | `tests/test_error_handling_integration.py` | `pytest tests/test_error_handling_integration.py -v` |
| 7 | 7.1 | `config.yaml` | `tests/test_yaml_config.py` | `pytest tests/test_yaml_config.py -v` |
| 8 | 8.1 | - | `tests/test_test_structure.py` | `pytest tests/test_test_structure.py -v` |
| 9 | 9.1 | `validators/` | `tests/test_validators.py` | `pytest tests/test_validators.py -v` |
| 10 | 10.1 | `cache/schema_cache.py` | `tests/test_cache.py` | `pytest tests/test_cache.py -v` |
| 11 | 11.1 | - | `tests/test_integration.py` | `pytest tests/test_integration.py -v` |
| 12 | 12.1 | - | `tests/test_regression.py` | `pytest tests/test_regression.py -v` |

## Quick Commands

```bash
# Run all tests
python run_tests.py

# Run specific phase
pytest tests/test_config.py -v

# Run with coverage
pytest tests/ --cov=generators --cov=config --cov=validators --cov-report=html

# Run all tests for a specific phase
pytest tests/test_phase_*.py -v
```

## Success Checklist for Each Phase

- [ ] All tests pass
- [ ] No functionality lost
- [ ] Code is more maintainable
- [ ] Performance maintained/improved
- [ ] Documentation updated
- [ ] Integration tests pass

## Critical Files to Backup

- `mock_data_generator.py` (original)
- `insurance_schemas.py`
- `data/examples/` (all example files)
- `data/swagger/` (swagger files)

## Rollback Plan

If any phase fails:
1. Revert to last working commit
2. Fix the issue
3. Re-run all tests for that phase
4. Continue to next phase only after all tests pass 