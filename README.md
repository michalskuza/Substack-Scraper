# Substack Scraper - Usage Guide

## Overview
This script extracts article URLs from a Substack archive page and can optionally display publication dates. It uses Selenium to handle infinite scrolling and BeautifulSoup to parse the page contents.

## Installation
Before running the script, ensure you have Python installed (version 3.7 or later). Then, install the required dependencies:

```bash
pip install selenium webdriver-manager beautifulsoup4 argparse
```

Additionally, make sure you have **Google Chrome** installed on your system. The script uses **chromedriver**, which is automatically managed by `webdriver-manager`.

## Usage
Run the script with the following command:

```bash
python substack_scraper.py <archive_url> [OPTIONS]
```

### Required Argument
- `<archive_url>`: The URL of the Substack archive page (e.g., `https://substack.com/archive`).

### Options
- `--debug` : Enables debug mode, which saves the HTML page to `substack_debug.html` for troubleshooting.
- `--show-dates` : Displays the publication date of each article alongside the URL.
- `--sort-by-date` : Sorts articles by their publication date.
- `--ascending` : Sorts articles in ascending order (oldest first). Default is descending (newest first).

### Example Commands
#### **Fetch article links only:**
```bash
python substack_scraper.py https://substack.com/archive
```

#### **Fetch links with publication dates:**
```bash
python substack_scraper.py https://substack.com/archive --show-dates
```

#### **Sort articles by date (default descending order, newest first):**
```bash
python substack_scraper.py https://substack.com/archive --sort-by-date
```

#### **Sort articles by date in ascending order (oldest first):**
```bash
python substack_scraper.py https://substack.com/archive --sort-by-date --ascending
```

#### **Enable debug mode (saves HTML for inspection):**
```bash
python substack_scraper.py https://substack.com/archive --debug
```

#### **Both debug mode and showing dates:**
```bash
python substack_scraper.py https://substack.com/archive --debug --show-dates
```

## Troubleshooting
### **1. No articles are found**
- Run the script with `--debug` and open `substack_debug.html` to inspect if the page was loaded correctly.
- Check if your IP is blocked by Substack (try opening the URL in a normal browser).
- Ensure **Google Chrome** is installed on your system.

### **2. Selenium fails to start Chrome**
- Make sure you have the latest **Chrome** version installed.
- Run the following to update `webdriver-manager`:
  ```bash
  pip install --upgrade webdriver-manager
  ```

## Notes
- This script may not work if Substack changes its HTML structure.
- The script mimics real user behavior by scrolling down gradually and using a real User-Agent to avoid bot detection.

## License
This script is open-source and provided as-is without warranty. Feel free to modify and improve it!

---

Happy scraping! 🚀