# Migration Guide: v1.0 to v2.0

This guide helps you migrate from the old single-file script to the new modular version.

## Quick Migration

### Old Command (v1.0)
```bash
python substack_scraper.py https://example.substack.com/archive --show-dates
```

### New Command (v2.0)
```bash
substack-scraper https://example.substack.com/archive --show-dates
```

## Major Changes

### 1. Installation Method

**Before:**
```bash
pip install selenium webdriver-manager beautifulsoup4
```

**After:**
```bash
pip install substack-scraper
# or
pip install -r requirements.txt
```

### 2. Command Name

The old script name `substack_scraper.py` is now available as a console command `substack-scraper`.

For backward compatibility, you can still use:
```bash
python substack_scraper.py <url>
```

### 3. New Features Available

#### Output Formats
```bash
# Export to CSV
substack-scraper <url> --format csv --output my_articles

# Export to JSON
substack-scraper <url> --format json --output my_articles
```

#### Multiple Browsers
```bash
# Use Firefox
substack-scraper <url> --browser firefox

# Use Edge
substack-scraper <url> --browser edge
```

#### Resume Capability
```bash
# Save checkpoint automatically, resume if interrupted
substack-scraper <url> --resume
```

#### Configuration Files
```bash
# Use custom config
substack-scraper <url> --config my_config.yaml
```

#### Show Titles
```bash
# Show article titles
substack-scraper <url> --show-titles
```

### 4. Python API Changes

**Before (v1.0):**
```python
from substack_scraper import get_substack_articles

articles = get_substack_articles(
    "https://example.substack.com/archive",
    debug=False,
    show_dates=True,
    sort_by_date=True,
    descending=True
)
```

**After (v2.0):**
```python
from substack_scraper import SubstackScraper, ArticleParser
from substack_scraper.config import Config

config = Config()
with SubstackScraper(config) as scraper:
    html = scraper.scrape_page("https://example.substack.com/archive")
    parser = ArticleParser()
    articles = parser.parse_articles(html, "https://example.substack.com")
    articles = parser.sort_articles(articles, by_date=True, ascending=False)
```

### 5. Command-Line Arguments

All old arguments are supported. New ones added:

| Old Argument | New Argument | Status |
|--------------|--------------|--------|
| `--debug` | `--debug` | ✅ Same |
| `--show-dates` | `--show-dates` | ✅ Same |
| `--sort-by-date` | `--sort-by-date` | ✅ Same |
| `--ascending` | `--ascending` | ✅ Same |
| N/A | `--show-titles` | ✨ New |
| N/A | `--format` | ✨ New |
| N/A | `--output` | ✨ New |
| N/A | `--browser` | ✨ New |
| N/A | `--resume` | ✨ New |
| N/A | `--config` | ✨ New |

### 6. Output Format Changes

**Console Output:**
- Old: URLs only (or with dates)
- New: Can include dates, titles, or both

**File Output:**
- Old: Console output only
- New: TXT, CSV, JSON formats available

### 7. Configuration

**New Feature**: Configuration files

Create `config.yaml`:
```yaml
browser:
  engine: chrome
  headless: true

output:
  format: csv
  include_dates: true

scraping:
  max_retries: 3
```

Use it:
```bash
substack-scraper <url> --config config.yaml
```

## Backward Compatibility

The old `substack_scraper.py` file remains functional for backward compatibility. However, we recommend migrating to the new modular version for:

- Better error handling
- More output options
- Multi-browser support
- Resume capability
- Better logging
- Type hints and testing
- Active maintenance

## Troubleshooting Migration Issues

### Issue: Module not found
```
ModuleNotFoundError: No module named 'substack_scraper'
```

**Solution**: Install the package properly
```bash
pip install -e .
# or
python -m pip install -e .
```

### Issue: Old script doesn't work
```
ImportError: cannot import name 'get_substack_articles'
```

**Solution**: Use the compatibility wrapper or new API
```bash
# Use new command
substack-scraper <url>

# Or update imports
from substack_scraper import SubstackScraper
```

### Issue: Different output format
The new version may format output slightly differently. Use `--format txt` for closest match to old output.

## Need Help?

- Check [README.md](README.md) for full documentation
- See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup
- Open an issue on GitHub for bugs or questions
