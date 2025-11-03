"""
Substack Scraper - A robust web scraper for extracting article URLs from Substack archives.
"""

__version__ = "2.0.0"
__author__ = "Substack Scraper Contributors"

from .scraper import SubstackScraper
from .parser import ArticleParser
from .exporter import Exporter

__all__ = ["SubstackScraper", "ArticleParser", "Exporter"]
