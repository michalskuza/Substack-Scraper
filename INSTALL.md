# Installation Guide

## Prerequisites

- Python 3.8 or later
- pip (Python package installer)
- One of: Google Chrome, Firefox, or Microsoft Edge

## Installation Steps

### 1. Basic Installation

```bash
# Clone or download the repository
cd Substack-Scraper

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

### 2. Development Installation

```bash
# Install with development dependencies
pip install -r requirements.txt -r requirements-dev.txt
pip install -e .
```

### 3. Using Make (Linux/macOS)

```bash
# Install development environment
make install-dev
```

### 4. Verify Installation

```bash
# Check if the package is installed
python -m substack_scraper.cli --version

# Or use the console command (if PATH is configured)
substack-scraper --version

# Run help to see all options
python -m substack_scraper.cli --help
```

## Common Issues

### Issue: `pip` not found

**Solution**: Install pip
```bash
# Ubuntu/Debian
sudo apt-get install python3-pip

# macOS
python3 -m ensurepip --upgrade

# Windows
python -m ensurepip --upgrade
```

### Issue: Permission denied

**Solution**: Use virtual environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install
pip install -r requirements.txt
pip install -e .
```

### Issue: `substack-scraper` command not found

**Solution**: Use the Python module directly
```bash
python -m substack_scraper.cli <args>
# or
python3 -m substack_scraper.cli <args>
```

### Issue: Browser driver not found

**Solution**: The package uses `webdriver-manager` which automatically downloads drivers. Ensure you have:
- Chrome installed for Chrome driver
- Firefox installed for Firefox driver
- Edge installed for Edge driver

### Issue: Import errors during installation

**Solution**: Make sure you're in the project root directory
```bash
cd /path/to/Substack-Scraper
pip install -e .
```

## Quick Start After Installation

```bash
# Basic usage
python -m substack_scraper.cli https://example.substack.com/archive

# With output file
python -m substack_scraper.cli https://example.substack.com/archive \
  --format csv \
  --output articles \
  --show-dates

# Using config file
python -m substack_scraper.cli https://example.substack.com/archive \
  --config config/default_config.yaml
```

## Docker Installation (Alternative)

If you prefer Docker:

```dockerfile
FROM python:3.11-slim

# Install Chrome and dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg2 chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install -e .

ENTRYPOINT ["python", "-m", "substack_scraper.cli"]
```

Build and run:
```bash
docker build -t substack-scraper .
docker run substack-scraper https://example.substack.com/archive
```

## Upgrading

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Reinstall package
pip install -e . --force-reinstall
```

## Uninstallation

```bash
pip uninstall substack-scraper
```

## Next Steps

- Read [README.md](README.md) for usage instructions
- Check [example_usage.py](example_usage.py) for API examples
- See [MIGRATION.md](MIGRATION.md) if upgrading from v1.0
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for development setup
