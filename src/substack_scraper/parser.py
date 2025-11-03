"""HTML parsing functionality for Substack articles."""

import logging
from typing import List, Tuple, Optional
from datetime import datetime
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class Article:
    """Represents a Substack article with metadata."""

    def __init__(self, url: str, date: Optional[str] = None, title: Optional[str] = None):
        """
        Initialize article.

        Args:
            url: Article URL
            date: Publication date string
            title: Article title
        """
        self.url = url
        self.date = date
        self.title = title
        self._parsed_date: Optional[datetime] = None

    @property
    def parsed_date(self) -> Optional[datetime]:
        """Get parsed datetime object."""
        if self._parsed_date is None and self.date and self.date != "Unknown date":
            try:
                self._parsed_date = datetime.strptime(self.date, "%d.%m.%Y")
            except ValueError:
                logger.warning(f"Could not parse date: {self.date}")
        return self._parsed_date

    def __repr__(self) -> str:
        return f"Article(url={self.url}, date={self.date}, title={self.title})"

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "url": self.url,
            "date": self.date,
            "title": self.title,
        }


class ArticleParser:
    """Parses HTML content to extract article information."""

    def __init__(self):
        """Initialize parser."""
        pass

    def parse_articles(self, html_content: str, base_url: str) -> List[Article]:
        """
        Parse HTML content to extract articles.

        Args:
            html_content: HTML content to parse
            base_url: Base URL for constructing absolute URLs

        Returns:
            List of Article objects
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = []
        seen_urls = set()

        logger.info("Starting article extraction")

        for link in soup.find_all("a", href=True):
            href = link['href']
            
            if '/p/' not in href or href.endswith('/comments'):
                continue

            full_url = href if href.startswith("http") else base_url.rstrip('/') + href

            if full_url in seen_urls:
                continue

            seen_urls.add(full_url)

            date_str = self._extract_date(link)
            title = self._extract_title(link)

            article = Article(url=full_url, date=date_str, title=title)
            articles.append(article)

        logger.info(f"Extracted {len(articles)} unique articles")
        return articles

    def _extract_date(self, link_element) -> str:
        """
        Extract publication date from link element.

        Args:
            link_element: BeautifulSoup link element

        Returns:
            Formatted date string or "Unknown date"
        """
        date_tag = link_element.find_previous("time")
        
        if not date_tag:
            date_tag = link_element.find_next("time")
        
        if date_tag:
            try:
                date_text = date_tag.text.strip()
                parsed_date = datetime.strptime(date_text, "%B %d, %Y")
                return parsed_date.strftime("%d.%m.%Y")
            except ValueError:
                return date_tag.text.strip()
        
        return "Unknown date"

    def _extract_title(self, link_element) -> Optional[str]:
        """
        Extract article title from link element.

        Args:
            link_element: BeautifulSoup link element

        Returns:
            Article title or None
        """
        title = link_element.get_text(strip=True)
        
        if title and len(title) > 5:
            return title
        
        title_attr = link_element.get('title')
        if title_attr:
            return title_attr
        
        return None

    def sort_articles(
        self, 
        articles: List[Article], 
        by_date: bool = False, 
        ascending: bool = False
    ) -> List[Article]:
        """
        Sort articles by date or URL.

        Args:
            articles: List of articles to sort
            by_date: Whether to sort by date
            ascending: Sort order (True for ascending, False for descending)

        Returns:
            Sorted list of articles
        """
        if by_date:
            def date_key(article: Article) -> datetime:
                return article.parsed_date if article.parsed_date else datetime.min
            
            articles = sorted(articles, key=date_key, reverse=not ascending)
            logger.info(f"Sorted {len(articles)} articles by date ({'ascending' if ascending else 'descending'})")
        
        return articles
