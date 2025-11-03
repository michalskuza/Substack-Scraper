"""Tests for parser module."""

import pytest
from datetime import datetime
from substack_scraper.parser import Article, ArticleParser


def test_article_creation():
    """Test Article object creation."""
    article = Article(
        url="https://example.substack.com/p/test-article",
        date="01.01.2024",
        title="Test Article"
    )
    
    assert article.url == "https://example.substack.com/p/test-article"
    assert article.date == "01.01.2024"
    assert article.title == "Test Article"


def test_article_parsed_date():
    """Test Article date parsing."""
    article = Article(
        url="https://example.substack.com/p/test",
        date="15.03.2024"
    )
    
    parsed = article.parsed_date
    assert isinstance(parsed, datetime)
    assert parsed.day == 15
    assert parsed.month == 3
    assert parsed.year == 2024


def test_article_to_dict():
    """Test Article dictionary conversion."""
    article = Article(
        url="https://example.substack.com/p/test",
        date="01.01.2024",
        title="Test"
    )
    
    data = article.to_dict()
    assert data["url"] == "https://example.substack.com/p/test"
    assert data["date"] == "01.01.2024"
    assert data["title"] == "Test"


def test_parse_articles():
    """Test parsing articles from HTML."""
    html = """
    <html>
        <body>
            <time>January 15, 2024</time>
            <a href="/p/first-article">First Article</a>
            <time>January 20, 2024</time>
            <a href="/p/second-article">Second Article</a>
        </body>
    </html>
    """
    
    parser = ArticleParser()
    articles = parser.parse_articles(html, "https://example.substack.com")
    
    assert len(articles) == 2
    assert "/p/first-article" in articles[0].url
    assert "/p/second-article" in articles[1].url


def test_parse_articles_removes_duplicates():
    """Test that duplicate URLs are removed."""
    html = """
    <html>
        <body>
            <a href="/p/article">Article</a>
            <a href="/p/article">Article</a>
        </body>
    </html>
    """
    
    parser = ArticleParser()
    articles = parser.parse_articles(html, "https://example.substack.com")
    
    assert len(articles) == 1


def test_parse_articles_excludes_comments():
    """Test that comment URLs are excluded."""
    html = """
    <html>
        <body>
            <a href="/p/article">Article</a>
            <a href="/p/article/comments">Comments</a>
        </body>
    </html>
    """
    
    parser = ArticleParser()
    articles = parser.parse_articles(html, "https://example.substack.com")
    
    assert len(articles) == 1
    assert "comments" not in articles[0].url


def test_sort_articles_by_date():
    """Test sorting articles by date."""
    articles = [
        Article(url="url1", date="15.01.2024"),
        Article(url="url2", date="10.01.2024"),
        Article(url="url3", date="20.01.2024"),
    ]
    
    parser = ArticleParser()
    
    # Sort descending (newest first)
    sorted_desc = parser.sort_articles(articles, by_date=True, ascending=False)
    assert sorted_desc[0].date == "20.01.2024"
    assert sorted_desc[2].date == "10.01.2024"
    
    # Sort ascending (oldest first)
    sorted_asc = parser.sort_articles(articles, by_date=True, ascending=True)
    assert sorted_asc[0].date == "10.01.2024"
    assert sorted_asc[2].date == "20.01.2024"
