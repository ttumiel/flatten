# FLATTEN PROJECT DEVELOPMENT GUIDE

## Build & Installation
```bash
python setup.py install
```

## Testing
```bash
# Run all tests
pytest

# Run a single test
pytest tests/test_core.py::test_name
```

## Code Style Guidelines

### Structure & Organization
- Core functionality in `core.py`
- CLI interface in `cli.py`
- Tests in separate `tests` directory

### Naming & Formatting
- snake_case for functions and variables
- 4-space indentation
- ~88 character line length
- Double quotes for strings
- f-strings for string formatting
- Private functions prefixed with underscore

### Imports
- Standard library imports first
- Third-party imports second
- Local imports third
- Separate import groups with blank lines

### Documentation
- Functions should have descriptive docstrings
- Use Args/Returns format with type hints in docstrings
- Document expected errors and edge cases

### Error Handling
- Use try/except blocks for expected errors
- Provide clear error messages