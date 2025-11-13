# Claude AI Contributions

This file documents the contributions and changes made by Claude AI to this project.

## Project Restructuring (2025-11)

### Overview
Restructured the entire project to follow modern Python packaging standards and best practices.

### Changes Made

#### 1. Package Structure
- **Before**: `Corrector/` directory with mixed-case module names
- **After**: `src/subtitles_auto_correct/` following PEP 8 conventions

#### 2. Directory Layout
```
Before:
sub-titles-auto-correct/
├── Corrector/
│   ├── Models/
│   │   └── Subtitle.py
│   ├── Utils/
│   │   ├── FileUtils.py
│   │   └── StringsUtils.py
│   └── main.py
└── Tests/
    ├── test_Models_Subtitle.py
    └── test_Utils_StringsUtils.py

After:
sub-titles-auto-correct/
├── src/
│   └── subtitles_auto_correct/
│       ├── __init__.py
│       ├── __main__.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── subtitle.py
│       └── utils/
│           ├── __init__.py
│           ├── file_utils.py
│           └── strings_utils.py
├── tests/
│   ├── __init__.py
│   ├── test_models_subtitle.py
│   └── test_utils_strings_utils.py
└── pyproject.toml
```

#### 3. Naming Conventions
All files and directories now follow PEP 8 naming conventions:
- **Packages**: `subtitles_auto_correct` (lowercase with underscores)
- **Modules**: `file_utils.py`, `strings_utils.py`, `subtitle.py` (snake_case)
- **Directories**: `tests/`, `models/`, `utils/` (lowercase)

#### 4. Modern Packaging
- Added `pyproject.toml` for PEP 517/518 compliance
- Configured setuptools for proper package discovery
- Added entry points for command-line execution
- Made package pip-installable

#### 5. Code Organization
- Created `__init__.py` files for proper package structure
- Created `__main__.py` with proper `main()` function
- Updated all imports to use new package structure
- Wrapped main execution code in `if __name__ == "__main__"` guard

#### 6. Documentation
- Updated README.md with modern installation instructions
- Added development setup instructions
- Included examples for running the application

### Benefits

1. **Standards Compliance**: Follows PEP 8, PEP 517, and PEP 518
2. **Modern Tooling**: Compatible with pytest, mypy, black, ruff, etc.
3. **Easy Installation**: `pip install -e .` for development
4. **Better Isolation**: src/ layout prevents import issues
5. **Distribution Ready**: Can be uploaded to PyPI
6. **Maintainability**: Clear structure for contributors

### Installation

```bash
# Clone the repository
git clone https://github.com/adrienbricchi/sub-titles-auto-correct.git
cd sub-titles-auto-correct

# Install in development mode
pip install -e .

# Run the application
python -m subtitles_auto_correct
# or
subtitles-auto-correct
```

### Testing

```bash
# Run tests with pytest
pytest

# Run specific test file
pytest tests/test_models_subtitle.py
```

### Technical Notes

- All existing functionality has been preserved
- No changes to core algorithms or logic
- Only structural and organizational changes
- Backward compatibility maintained in functionality
- All Python files pass syntax validation

### Future Recommendations

1. **Type Hints**: Add type hints for better IDE support and type checking
2. **Dependencies**: Move to pyproject.toml from config.ini for dependencies
3. **Testing**: Increase test coverage
4. **Documentation**: Add docstring documentation in Google or NumPy style
5. **CI/CD**: Update CI configuration to use new structure
6. **Linting**: Add black, ruff, or pylint configuration
7. **Pre-commit**: Add pre-commit hooks for code quality

---

*This file was created to document AI-assisted contributions to the project.*
