#!/usr/bin/env python3
"""
Backward compatibility wrapper for Substack Scraper v1.0

This file maintains the old API for backward compatibility.
For new projects, please use the modular version:
    from substack_scraper import SubstackScraper, ArticleParser

To migrate to v2.0, see MIGRATION.md
"""

import sys
import warnings

warnings.warn(
    "Using legacy API. Consider migrating to v2.0. See MIGRATION.md for details.",
    DeprecationWarning,
    stacklevel=2
)

try:
    from src.substack_scraper.config import Config
    from src.substack_scraper.scraper import SubstackScraper
    from src.substack_scraper.parser import ArticleParser
except ImportError:
    # Fallback for different installation methods
    from substack_scraper.config import Config
    from substack_scraper.scraper import SubstackScraper
    from substack_scraper.parser import ArticleParser

import argparse


def get_substack_articles(substack_archive_url, debug=False, show_dates=False, sort_by_date=False, descending=True):
    """
    Legacy function for backward compatibility.
    
    Args:
        substack_archive_url: URL to scrape
        debug: Save HTML for debugging
        show_dates: Include dates in results
        sort_by_date: Sort by publication date
        descending: Sort order
        
    Returns:
        List of tuples (date, url)
    """
    config = Config()
    
    with SubstackScraper(config) as scraper:
        html = scraper.scrape_page(substack_archive_url, debug=debug)
        
        parser = ArticleParser()
        articles = parser.parse_articles(html, substack_archive_url)
        
        if sort_by_date:
            articles = parser.sort_articles(articles, by_date=True, ascending=not descending)
        
        # Convert to old format (date, url) tuples
        results = []
        for article in articles:
            if show_dates or sort_by_date:
                results.append((article.date, article.url))
            else:
                results.append((None, article.url))
        
        return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrape Substack archive for article links (Legacy v1.0 API)",
        epilog="Note: This is the legacy interface. Use 'substack-scraper' command for v2.0 features."
    )
    parser.add_argument("url", help="Substack archive page URL (e.g., https://substack.com/archive)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode and save HTML for inspection")
    parser.add_argument("--show-dates", action="store_true", help="Show publication dates of articles")
    parser.add_argument("--sort-by-date", action="store_true", help="Sort articles by date")
    parser.add_argument("--ascending", action="store_true", help="Sort articles in ascending order instead of descending")
    args = parser.parse_args()
    
    print("\n⚠️  Using legacy v1.0 API. Consider upgrading to v2.0.")
    print("See MIGRATION.md for details or run: substack-scraper --help\n")
    
    try:
        articles = get_substack_articles(
            args.url, 
            debug=args.debug, 
            show_dates=args.show_dates, 
            sort_by_date=args.sort_by_date, 
            descending=not args.ascending
        )
        
        print("\nFound articles:")
        for pub_date, article_url in articles:
            if args.show_dates:
                print(f"{pub_date} - {article_url}")
            else:
                print(article_url)
                
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nFor better error handling and features, use: substack-scraper")
        sys.exit(1)
