# Substack Scraper

[![CI](https://github.com/yourusername/substack-scraper/workflows/CI/badge.svg)](https://github.com/yourusername/substack-scraper/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A robust, feature-rich web scraper for extracting article URLs from Substack archive pages with support for multiple browsers, output formats, and resume capabilities.

## Features

✨ **Core Features**
- 🔄 Handles infinite scrolling automatically
- 📅 Extracts publication dates and titles
- 🎨 Multiple output formats (TXT, CSV, JSON)
- 💾 Resume capability with checkpoint files
- 🌐 Multi-browser support (Chrome, Firefox, Edge)
- ⚡ Progress bars and logging
- 🔧 Configurable via YAML/JSON files
- 🎯 Smart anti-bot detection avoidance

## Installation

### From PyPI (Recommended)
```bash
pip install substack-scraper
```

### From Source
```bash
git clone https://github.com/yourusername/substack-scraper.git
cd substack-scraper
pip install -e .
```

### Requirements
- Python 3.8 or later
- One of: Google Chrome, Firefox, or Microsoft Edge

## Quick Start

### Basic Usage
```bash
substack-scraper https://example.substack.com/archive
```

### Common Examples

**Export to CSV with dates and titles:**
```bash
substack-scraper https://example.substack.com/archive \
  --format csv \
  --show-dates \
  --show-titles \
  --output my_articles
```

**Sort by date (newest first):**
```bash
substack-scraper https://example.substack.com/archive --sort-by-date
```

**Use Firefox instead of Chrome:**
```bash
substack-scraper https://example.substack.com/archive --browser firefox
```

**Export to JSON:**
```bash
substack-scraper https://example.substack.com/archive --format json --output articles
```

**Resume from previous checkpoint:**
```bash
substack-scraper https://example.substack.com/archive --resume
```

**Debug mode (save HTML for inspection):**
```bash
substack-scraper https://example.substack.com/archive --debug
```

## Command-Line Options

### Configuration
- `--config FILE` - Path to configuration file (YAML or JSON)

### Browser Options
- `--browser {chrome,firefox,edge}` - Browser engine to use (default: chrome)
- `--no-headless` - Run browser in visible mode

### Scraping Options
- `--debug` - Enable debug mode and save HTML
- `--resume` - Resume from previous checkpoint

### Display Options
- `--show-dates` - Show publication dates
- `--show-titles` - Show article titles
- `--sort-by-date` - Sort articles by publication date
- `--ascending` - Sort in ascending order (oldest first)

### Output Options
- `--format {txt,csv,json}` - Output format (default: txt)
- `--output NAME` - Output filename (without extension)
- `--output-dir DIR` - Output directory (default: output)
- `--no-console` - Don't print results to console

### Logging Options
- `--log-level {DEBUG,INFO,WARNING,ERROR}` - Logging level (default: INFO)
- `--log-file FILE` - Save logs to file

## Configuration File

Create a `config.yaml` or `config.json` file to customize defaults:

```yaml
browser:
  engine: chrome
  headless: true
  timeout: 30

scraping:
  initial_wait:
    min: 3
    max: 6
  max_retries: 3

output:
  format: csv
  directory: output
  include_dates: true
```

Use it with:
```bash
substack-scraper https://example.substack.com/archive --config config.yaml
```

## Output Formats

### Text (TXT)
```
01.01.2024 - Article Title - https://example.substack.com/p/article
02.01.2024 - Another Article - https://example.substack.com/p/another
```

### CSV
```csv
date,title,url
01.01.2024,Article Title,https://example.substack.com/p/article
02.01.2024,Another Article,https://example.substack.com/p/another
```

### JSON
```json
{
  "total_articles": 2,
  "articles": [
    {
      "url": "https://example.substack.com/p/article",
      "date": "01.01.2024",
      "title": "Article Title"
    }
  ]
}
```

## Advanced Usage

### Python API

You can also use the scraper programmatically:

```python
from substack_scraper import SubstackScraper, ArticleParser, Exporter
from substack_scraper.config import Config

# Initialize with config
config = Config()
scraper = SubstackScraper(config)
parser = ArticleParser()
exporter = Exporter("output")

# Scrape articles
with scraper:
    html = scraper.scrape_page("https://example.substack.com/archive")
    articles = parser.parse_articles(html, "https://example.substack.com")
    
    # Sort if needed
    articles = parser.sort_articles(articles, by_date=True, ascending=False)
    
    # Export
    exporter.export(articles, format="csv", filename="articles", include_dates=True)
```

## Troubleshooting

### No articles found
- Use `--debug` to save HTML and inspect the page structure
- Verify the URL is correct and accessible
- Check if your IP is blocked (try in a normal browser)

### Browser/WebDriver issues
- Update WebDriver: `pip install --upgrade webdriver-manager`
- Try a different browser: `--browser firefox`
- Run in visible mode: `--no-headless`
- Ensure your browser is up to date

### Timeout errors
- Increase timeout in config file
- Check your internet connection
- The site may be slow or blocking requests

### Rate limiting / IP blocked
- Reduce scraping frequency
- Use VPN if necessary
- Increase delays in config file

## Development

### Setup Development Environment
```bash
git clone https://github.com/yourusername/substack-scraper.git
cd substack-scraper
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
```

### Run Tests
```bash
pytest tests/ -v
```

### Code Formatting
```bash
black src/substack_scraper tests
flake8 src/substack_scraper
```

### Type Checking
```bash
mypy src/substack_scraper
```

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Selenium](https://www.selenium.dev/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- Inspired by the need for better Substack content management

## Support

- 📫 Issues: [GitHub Issues](https://github.com/yourusername/substack-scraper/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/substack-scraper/discussions)

---

**Note**: This tool is for personal use and research. Please respect Substack's Terms of Service and robots.txt. Use responsibly and ethically.

Happy scraping! 🚀