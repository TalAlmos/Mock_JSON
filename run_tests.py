# run_tests.py
import subprocess
import sys

def run_migration_tests():
    """Run tests for each migration phase"""
    phases = [
        "test_config.py",
        "test_registry.py", 
        "test_base_generator.py",
        "test_insurance_generator.py",
        "test_schema_analyzer.py",
        "test_factory.py",
        "test_commands.py",
        "test_exceptions.py",
        "test_yaml_config.py",
        "test_validators.py",
        "test_cache.py",
        "test_integration.py",
        "test_regression.py"
    ]
    
    all_passed = True
    for phase_test in phases:
        print(f"Running tests for {phase_test}...")
        result = subprocess.run(["pytest", f"tests/{phase_test}", "-v"])
        if result.returncode != 0:
            all_passed = False
            print(f"❌ Tests failed for {phase_test}")
        else:
            print(f"✅ Tests passed for {phase_test}")
    
    return all_passed

if __name__ == "__main__":
    success = run_migration_tests()
    sys.exit(0 if success else 1)
test_schema_analyzer.py