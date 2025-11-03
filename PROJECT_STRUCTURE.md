# Project Structure

```
Substack-Scraper/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Continuous Integration pipeline
│       └── release.yml         # Release automation
├── config/
│   └── default_config.yaml     # Default configuration template
├── output/                     # Default output directory (gitignored)
├── src/
│   └── substack_scraper/
│       ├── __init__.py         # Package initialization
│       ├── cli.py              # Command-line interface
│       ├── config.py           # Configuration management
│       ├── scraper.py          # Web scraping logic
│       ├── parser.py           # HTML parsing and article extraction
│       ├── exporter.py         # Export to various formats
│       └── checkpoint.py       # Resume capability
├── tests/
│   ├── __init__.py
│   ├── test_config.py          # Configuration tests
│   ├── test_scraper.py         # Scraper tests
│   ├── test_parser.py          # Parser tests
│   ├── test_exporter.py        # Exporter tests
│   └── test_checkpoint.py      # Checkpoint tests
├── .editorconfig               # Editor configuration
├── .flake8                     # Flake8 linter configuration
├── .gitignore                  # Git ignore rules
├── CHANGELOG.md                # Version history
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE                     # MIT License
├── Makefile                    # Development commands
├── MIGRATION.md                # v1 to v2 migration guide
├── PROJECT_STRUCTURE.md        # This file
├── README.md                   # Main documentation
├── pytest.ini                  # Pytest configuration
├── pyproject.toml              # Modern Python project config
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── setup.py                    # Package installation
├── example_usage.py            # API usage examples
├── substack_scraper.py         # Backward compatibility wrapper
└── substack_scraper_v1_legacy.py  # Original v1.0 script backup
```

## Key Directories

### `/src/substack_scraper/`
Core application code with modular components:
- **cli.py**: Command-line interface and argument parsing
- **config.py**: Configuration file loading and management
- **scraper.py**: Selenium-based web scraping with multi-browser support
- **parser.py**: BeautifulSoup HTML parsing and article extraction
- **exporter.py**: Export functionality (TXT, CSV, JSON)
- **checkpoint.py**: Save/restore functionality for interrupted scrapes

### `/tests/`
Comprehensive unit tests for all modules using pytest.

### `/config/`
Configuration templates and examples.

### `/.github/workflows/`
CI/CD pipelines for automated testing and releases.

## Module Responsibilities

### Scraper Module
- Multi-browser support (Chrome, Firefox, Edge)
- Infinite scroll handling
- Anti-bot detection avoidance
- Retry logic and error handling
- Debug HTML saving

### Parser Module
- Article URL extraction
- Date parsing and normalization
- Title extraction
- Duplicate removal
- Sorting functionality

### Exporter Module
- Multiple format support
- Customizable field inclusion
- Console and file output
- Directory management

### Config Module
- YAML/JSON configuration loading
- Default values
- Dot notation access
- Config file saving

### Checkpoint Module
- JSON-based state persistence
- Resume capability
- Metadata storage

## Design Principles

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Extensibility**: Easy to add new browsers, formats, or features
3. **Testability**: Comprehensive test coverage with mocked dependencies
4. **Configurability**: Flexible configuration via files or CLI
5. **Backward Compatibility**: Legacy API wrapper for smooth migration
6. **Type Safety**: Type hints throughout for better IDE support
7. **Error Handling**: Graceful failure with informative messages
8. **Logging**: Proper logging at appropriate levels

## Entry Points

1. **Console Command**: `substack-scraper` (defined in setup.py)
2. **Python Module**: `python -m substack_scraper.cli`
3. **Legacy Script**: `python substack_scraper.py`
4. **Python API**: `from substack_scraper import SubstackScraper`

## Data Flow

```
CLI Input
  ↓
Config Loading
  ↓
URL Validation
  ↓
Web Scraping (Selenium)
  ↓
HTML Parsing (BeautifulSoup)
  ↓
Article Objects
  ↓
Sorting/Filtering
  ↓
Export (TXT/CSV/JSON) + Console Output
  ↓
Checkpoint Save (optional)
```

## Testing Strategy

- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test module interactions
- **Mocked Tests**: Mock Selenium/WebDriver for faster tests
- **CI/CD**: Automated testing on multiple platforms and Python versions

## Development Workflow

1. Install dev dependencies: `make install-dev`
2. Make changes
3. Run checks: `make check` (lint, format, type-check, test)
4. Commit and push
5. CI runs automatically
6. Create PR for review
