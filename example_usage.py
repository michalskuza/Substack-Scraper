#!/usr/bin/env python3
"""
Example usage of Substack Scraper v2.0 API

This demonstrates how to use the scraper programmatically.
"""

from pathlib import Path
from substack_scraper import SubstackScraper, ArticleParser, Exporter
from substack_scraper.config import Config
from substack_scraper.checkpoint import Checkpoint


def basic_example():
    """Basic scraping example."""
    print("=== Basic Example ===\n")
    
    config = Config()
    
    with SubstackScraper(config) as scraper:
        url = "https://example.substack.com/archive"
        print(f"Scraping {url}...")
        
        html = scraper.scrape_page(url)
        
        parser = ArticleParser()
        articles = parser.parse_articles(html, url)
        
        print(f"Found {len(articles)} articles\n")
        
        for article in articles[:3]:  # Show first 3
            print(f"- {article.url}")


def export_example():
    """Example with multiple export formats."""
    print("\n=== Export Example ===\n")
    
    config = Config()
    
    with SubstackScraper(config) as scraper:
        url = "https://example.substack.com/archive"
        html = scraper.scrape_page(url)
        
        parser = ArticleParser()
        articles = parser.parse_articles(html, url)
        articles = parser.sort_articles(articles, by_date=True, ascending=False)
        
        exporter = Exporter("output")
        
        # Export to different formats
        txt_file = exporter.export(articles, "txt", "articles", include_dates=True)
        print(f"Exported to TXT: {txt_file}")
        
        csv_file = exporter.export(articles, "csv", "articles", include_dates=True, include_titles=True)
        print(f"Exported to CSV: {csv_file}")
        
        json_file = exporter.export(articles, "json", "articles")
        print(f"Exported to JSON: {json_file}")


def config_file_example():
    """Example using configuration file."""
    print("\n=== Config File Example ===\n")
    
    # Create a custom config file
    config_path = Path("custom_config.yaml")
    
    config = Config()
    config.set("browser.engine", "firefox")
    config.set("output.format", "json")
    config.set("scraping.max_retries", 5)
    
    config.save_to_file(config_path)
    print(f"Created config file: {config_path}")
    
    # Load and use it
    loaded_config = Config(config_path)
    print(f"Browser engine: {loaded_config.get('browser.engine')}")
    print(f"Max retries: {loaded_config.get('scraping.max_retries')}")


def checkpoint_example():
    """Example with checkpoint functionality."""
    print("\n=== Checkpoint Example ===\n")
    
    config = Config()
    checkpoint = Checkpoint()
    
    url = "https://example.substack.com/archive"
    
    if checkpoint.exists():
        print("Checkpoint found! Restoring previous session...")
        articles = checkpoint.restore_articles()
        print(f"Restored {len(articles)} articles from checkpoint")
    else:
        print("No checkpoint found. Starting fresh scrape...")
        with SubstackScraper(config) as scraper:
            html = scraper.scrape_page(url)
            parser = ArticleParser()
            articles = parser.parse_articles(html, url)
            
            # Save checkpoint
            checkpoint.save(url, articles, {"note": "Example scrape"})
            print(f"Saved checkpoint with {len(articles)} articles")


def custom_filtering_example():
    """Example with custom filtering and processing."""
    print("\n=== Custom Filtering Example ===\n")
    
    config = Config()
    
    with SubstackScraper(config) as scraper:
        url = "https://example.substack.com/archive"
        html = scraper.scrape_page(url)
        
        parser = ArticleParser()
        articles = parser.parse_articles(html, url)
        
        # Filter articles from 2024
        articles_2024 = [a for a in articles if a.date and "2024" in a.date]
        print(f"Found {len(articles_2024)} articles from 2024")
        
        # Filter by title keyword
        keyword = "python"
        matching = [a for a in articles if a.title and keyword.lower() in a.title.lower()]
        print(f"Found {len(matching)} articles mentioning '{keyword}'")


if __name__ == "__main__":
    print("Substack Scraper v2.0 - Example Usage\n")
    print("=" * 50)
    
    # Run examples
    # Note: These will fail without a real URL. Replace with actual Substack URLs to test.
    
    try:
        # Uncomment to run specific examples
        # basic_example()
        # export_example()
        config_file_example()
        # checkpoint_example()
        # custom_filtering_example()
        
        print("\n" + "=" * 50)
        print("\nExamples completed! Check the code for more details.")
        print("Replace URLs with real Substack archives to test scraping.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nNote: These examples need real Substack URLs to work.")
        print("Update the URLs in the code and try again.")
