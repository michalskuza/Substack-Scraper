"""Tests for scraper module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from substack_scraper.scraper import SubstackScraper, ScraperError
from substack_scraper.config import Config


@pytest.fixture
def config():
    """Fixture providing test configuration."""
    return Config()


def test_validate_url_valid(config):
    """Test URL validation with valid URLs."""
    scraper = SubstackScraper(config)
    
    assert scraper.validate_url("https://example.substack.com/archive")
    assert scraper.validate_url("http://example.com")


def test_validate_url_invalid(config):
    """Test URL validation with invalid URLs."""
    scraper = SubstackScraper(config)
    
    assert not scraper.validate_url("not-a-url")
    assert not scraper.validate_url("")
    assert not scraper.validate_url("ftp://invalid")


def test_scraper_context_manager(config):
    """Test scraper can be used as context manager."""
    with SubstackScraper(config) as scraper:
        assert scraper is not None


@patch('substack_scraper.scraper.webdriver.Chrome')
def test_setup_chrome_driver(mock_chrome, config):
    """Test Chrome driver setup."""
    scraper = SubstackScraper(config)
    config.set("browser.engine", "chrome")
    
    mock_driver = MagicMock()
    mock_chrome.return_value = mock_driver
    
    driver = scraper._setup_driver()
    
    assert mock_chrome.called
    mock_driver.set_page_load_timeout.assert_called()


def test_scrape_invalid_url(config):
    """Test scraping with invalid URL raises error."""
    scraper = SubstackScraper(config)
    
    with pytest.raises(ScraperError):
        scraper.scrape_page("not-a-url")


@patch('substack_scraper.scraper.webdriver.Chrome')
def test_scrape_with_debug(mock_chrome, config):
    """Test scraping with debug mode saves HTML."""
    mock_driver = MagicMock()
    mock_driver.page_source = "<html>Test</html>"
    mock_chrome.return_value = mock_driver
    
    scraper = SubstackScraper(config)
    
    with patch('builtins.open', create=True) as mock_open:
        html = scraper.scrape_page("https://example.com", debug=True)
        mock_open.assert_called_with("substack_debug.html", "w", encoding="utf-8")


def test_close_driver(config):
    """Test closing driver."""
    scraper = SubstackScraper(config)
    scraper.driver = MagicMock()
    
    scraper.close()
    
    scraper.driver.quit.assert_called_once()
    assert scraper.driver is None
