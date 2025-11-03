"""Core scraping functionality for Substack archives."""

import random
import time
import logging
from typing import Optional, List, Tuple
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
from .config import Config

logger = logging.getLogger(__name__)


class ScraperError(Exception):
    """Base exception for scraper errors."""
    pass


class SubstackScraper:
    """Handles web scraping of Substack archive pages."""

    def __init__(self, config: Config):
        """
        Initialize the scraper.

        Args:
            config: Configuration object
        """
        self.config = config
        self.driver: Optional[webdriver.Remote] = None

    def validate_url(self, url: str) -> bool:
        """
        Validate URL format.

        Args:
            url: URL to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def _setup_driver(self) -> webdriver.Remote:
        """
        Setup and configure the WebDriver.

        Returns:
            Configured WebDriver instance

        Raises:
            ScraperError: If driver setup fails
        """
        engine = self.config.get("browser.engine", "chrome").lower()
        headless = self.config.get("browser.headless", True)
        user_agent = self.config.get("browser.user_agent")
        timeout = self.config.get("browser.timeout", 30)

        try:
            if engine == "chrome":
                options = ChromeOptions()
                if headless:
                    options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument(f"user-agent={user_agent}")
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option("useAutomationExtension", False)
                
                driver = webdriver.Chrome(
                    service=ChromeService(ChromeDriverManager().install()),
                    options=options
                )
            elif engine == "firefox":
                options = FirefoxOptions()
                if headless:
                    options.add_argument("--headless")
                options.set_preference("general.useragent.override", user_agent)
                
                driver = webdriver.Firefox(
                    service=FirefoxService(GeckoDriverManager().install()),
                    options=options
                )
            elif engine == "edge":
                options = EdgeOptions()
                if headless:
                    options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument(f"user-agent={user_agent}")
                
                driver = webdriver.Edge(
                    service=EdgeService(EdgeChromiumDriverManager().install()),
                    options=options
                )
            else:
                raise ScraperError(f"Unsupported browser engine: {engine}")

            driver.set_page_load_timeout(self.config.get("browser.page_load_timeout", 60))
            driver.implicitly_wait(timeout)
            
            logger.info(f"WebDriver initialized: {engine}")
            return driver

        except Exception as e:
            logger.error(f"Failed to setup WebDriver: {e}")
            raise ScraperError(f"WebDriver setup failed: {e}")

    def _scroll_page(self) -> None:
        """Scroll page to load all content via infinite scroll."""
        scroll_wait_config = self.config.get("scraping.scroll_wait", {"min": 2, "max": 5})
        
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_attempts = 50

        while scroll_attempts < max_attempts:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            wait_time = random.uniform(scroll_wait_config["min"], scroll_wait_config["max"])
            time.sleep(wait_time)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                logger.info(f"Reached end of page after {scroll_attempts} scrolls")
                break
            
            last_height = new_height
            scroll_attempts += 1

        if scroll_attempts >= max_attempts:
            logger.warning(f"Stopped scrolling after {max_attempts} attempts")

    def scrape_page(self, url: str, debug: bool = False) -> str:
        """
        Scrape a Substack archive page.

        Args:
            url: URL to scrape
            debug: Whether to save debug HTML

        Returns:
            Page HTML content

        Raises:
            ScraperError: If scraping fails
        """
        if not self.validate_url(url):
            raise ScraperError(f"Invalid URL: {url}")

        max_retries = self.config.get("scraping.max_retries", 3)
        retry_delay = self.config.get("scraping.retry_delay", 5)

        for attempt in range(max_retries):
            try:
                if self.driver is None:
                    self.driver = self._setup_driver()

                logger.info(f"Loading page: {url} (attempt {attempt + 1}/{max_retries})")
                self.driver.get(url)

                initial_wait = self.config.get("scraping.initial_wait", {"min": 3, "max": 6})
                wait_time = random.uniform(initial_wait["min"], initial_wait["max"])
                time.sleep(wait_time)

                self._scroll_page()

                html_content = self.driver.page_source

                if debug:
                    debug_file = "substack_debug.html"
                    with open(debug_file, "w", encoding="utf-8") as f:
                        f.write(html_content)
                    logger.info(f"Saved debug HTML to {debug_file}")

                logger.info("Page scraped successfully")
                return html_content

            except TimeoutException:
                logger.warning(f"Timeout on attempt {attempt + 1}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    if self.driver:
                        self.driver.quit()
                        self.driver = None
                else:
                    raise ScraperError("Page load timeout after all retries")

            except WebDriverException as e:
                logger.error(f"WebDriver error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    if self.driver:
                        self.driver.quit()
                        self.driver = None
                else:
                    raise ScraperError(f"WebDriver error: {e}")

            except Exception as e:
                logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
                raise ScraperError(f"Scraping failed: {e}")

        raise ScraperError("Failed to scrape page after all retries")

    def close(self) -> None:
        """Clean up and close the WebDriver."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("WebDriver closed")
            except Exception as e:
                logger.error(f"Error closing WebDriver: {e}")
            finally:
                self.driver = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
