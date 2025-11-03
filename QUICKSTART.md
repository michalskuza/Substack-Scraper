# Quick Start Guide

## Installation (Choose One)

### Option 1: Virtual Environment (Recommended)
```bash
cd Substack-Scraper
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

### Option 2: System-wide Installation
```bash
cd Substack-Scraper
pip install -r requirements.txt
pip install -e .
```

### Option 3: Development Installation
```bash
cd Substack-Scraper
make install-dev
```

## Usage

### Command Line (Recommended)
```bash
# If 'substack-scraper' command is available
substack-scraper https://example.substack.com/archive

# Otherwise use Python module
python -m substack_scraper.cli https://example.substack.com/archive
# or
python3 -m substack_scraper.cli https://example.substack.com/archive
```

### Legacy Script (For backward compatibility)
```bash
python substack_scraper.py https://example.substack.com/archive
```

## Common Commands

```bash
# Basic scraping
python -m substack_scraper.cli https://example.substack.com/archive

# Export to CSV with dates and titles
python -m substack_scraper.cli https://example.substack.com/archive \
  --format csv --show-dates --show-titles --output my_articles

# Sort by date (newest first)
python -m substack_scraper.cli https://example.substack.com/archive \
  --sort-by-date

# Use Firefox browser
python -m substack_scraper.cli https://example.substack.com/archive \
  --browser firefox

# Debug mode
python -m substack_scraper.cli https://example.substack.com/archive \
  --debug --log-level DEBUG

# Resume from checkpoint
python -m substack_scraper.cli https://example.substack.com/archive \
  --resume
```

## Testing

```bash
# Run tests (requires dev dependencies)
pytest tests/ -v

# Or using Makefile
make test
```

## Configuration

Create a `my_config.yaml` file:
```yaml
browser:
  engine: chrome
  headless: true

output:
  format: csv
  include_dates: true
```

Use it:
```bash
python -m substack_scraper.cli https://example.substack.com/archive \
  --config my_config.yaml
```

## Troubleshooting

### Command not found
Use: `python -m substack_scraper.cli` or `python3 -m substack_scraper.cli`

### Import errors
Make sure you're in the project directory and ran: `pip install -e .`

### Browser driver issues
The package auto-downloads drivers. Ensure Chrome/Firefox/Edge is installed.

### Dependencies not found
Install: `pip install -r requirements.txt`

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [example_usage.py](example_usage.py) for Python API examples
- See [INSTALL.md](INSTALL.md) for detailed installation help
- Review [MIGRATION.md](MIGRATION.md) if upgrading from v1.0

## Help

```bash
python -m substack_scraper.cli --help
```
