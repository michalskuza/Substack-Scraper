"""Command-line interface for Substack Scraper."""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime
from tqdm import tqdm

from .config import Config
from .scraper import SubstackScraper, ScraperError
from .parser import ArticleParser
from .exporter import Exporter, ExportError
from .checkpoint import Checkpoint
from . import __version__


def setup_logging(level: str, log_file: Optional[str] = None) -> None:
    """
    Configure logging.

    Args:
        level: Logging level
        log_file: Optional log file path
    """
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    handlers = [logging.StreamHandler(sys.stdout)]
    
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Scrape Substack archive pages for article links.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  substack-scraper https://example.substack.com/archive
  
  # With dates and titles
  substack-scraper https://example.substack.com/archive --show-dates --show-titles
  
  # Export to CSV
  substack-scraper https://example.substack.com/archive --format csv --output my_articles
  
  # Sort by date (newest first)
  substack-scraper https://example.substack.com/archive --sort-by-date
  
  # Sort by date (oldest first)
  substack-scraper https://example.substack.com/archive --sort-by-date --ascending
  
  # Use Firefox instead of Chrome
  substack-scraper https://example.substack.com/archive --browser firefox
  
  # Resume from checkpoint
  substack-scraper https://example.substack.com/archive --resume
  
  # Use custom config file
  substack-scraper https://example.substack.com/archive --config my_config.yaml
        """
    )

    parser.add_argument(
        "url",
        nargs="?",
        help="Substack archive page URL (e.g., https://example.substack.com/archive)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"Substack Scraper {__version__}",
    )

    # Configuration
    config_group = parser.add_argument_group("configuration")
    config_group.add_argument(
        "--config",
        type=str,
        help="Path to configuration file (YAML or JSON)"
    )
    
    # Browser options
    browser_group = parser.add_argument_group("browser options")
    browser_group.add_argument(
        "--browser",
        choices=["chrome", "firefox", "edge"],
        help="Browser engine to use (default: chrome)"
    )
    browser_group.add_argument(
        "--no-headless",
        action="store_true",
        help="Run browser in non-headless mode (visible)"
    )

    # Scraping options
    scraping_group = parser.add_argument_group("scraping options")
    scraping_group.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode and save HTML for inspection"
    )
    scraping_group.add_argument(
        "--resume",
        action="store_true",
        help="Resume from previous checkpoint"
    )

    # Display options
    display_group = parser.add_argument_group("display options")
    display_group.add_argument(
        "--show-dates",
        action="store_true",
        help="Show publication dates of articles"
    )
    display_group.add_argument(
        "--show-titles",
        action="store_true",
        help="Show titles of articles"
    )
    display_group.add_argument(
        "--sort-by-date",
        action="store_true",
        help="Sort articles by publication date"
    )
    display_group.add_argument(
        "--ascending",
        action="store_true",
        help="Sort in ascending order (oldest first, default is newest first)"
    )

    # Output options
    output_group = parser.add_argument_group("output options")
    output_group.add_argument(
        "--format",
        choices=["txt", "csv", "json"],
        default="txt",
        help="Output format (default: txt)"
    )
    output_group.add_argument(
        "--output",
        type=str,
        help="Output filename (without extension)"
    )
    output_group.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Output directory (default: output)"
    )
    output_group.add_argument(
        "--no-console",
        action="store_true",
        help="Don't print results to console"
    )

    # Logging options
    logging_group = parser.add_argument_group("logging options")
    logging_group.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    logging_group.add_argument(
        "--log-file",
        type=str,
        help="Save logs to file"
    )

    return parser


def main() -> int:
    """
    Main entry point for CLI.

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parser = create_parser()
    args = parser.parse_args()

    # Show help if no URL provided and not resuming
    if not args.url and not args.resume:
        parser.print_help()
        return 0

    # Setup logging
    setup_logging(args.log_level, args.log_file)
    logger = logging.getLogger(__name__)

    try:
        # Load configuration
        config_file = Path(args.config) if args.config else None
        config = Config(config_file)

        # Override config with CLI arguments
        if args.browser:
            config.set("browser.engine", args.browser)
        if args.no_headless:
            config.set("browser.headless", False)
        if args.output_dir:
            config.set("output.directory", args.output_dir)

        # Initialize components
        checkpoint = Checkpoint(config.get("checkpoint.file"))
        
        # Check for resume
        if args.resume and checkpoint.exists():
            logger.info("Resuming from checkpoint")
            articles = checkpoint.restore_articles()
            checkpoint_data = checkpoint.load()
            url = checkpoint_data.get("url", "")
            
            if not url:
                logger.error("Checkpoint exists but URL is missing")
                return 1
        else:
            if not args.url:
                logger.error("URL is required when not resuming from checkpoint")
                return 1

            url = args.url
            
            # Scrape the page
            logger.info(f"Starting scrape of {url}")
            
            with SubstackScraper(config) as scraper:
                with tqdm(total=3, desc="Scraping progress") as pbar:
                    pbar.set_description("Loading page")
                    html_content = scraper.scrape_page(url, debug=args.debug)
                    pbar.update(1)
                    
                    pbar.set_description("Parsing articles")
                    parser_obj = ArticleParser()
                    articles = parser_obj.parse_articles(html_content, url)
                    pbar.update(1)
                    
                    pbar.set_description("Processing results")
                    if args.sort_by_date:
                        articles = parser_obj.sort_articles(
                            articles,
                            by_date=True,
                            ascending=args.ascending
                        )
                    pbar.update(1)

            # Save checkpoint if enabled
            if config.get("checkpoint.enabled"):
                checkpoint.save(url, articles, {"scrape_time": datetime.now().isoformat()})

        if not articles:
            logger.warning("No articles found")
            return 0

        # Export results
        exporter = Exporter(args.output_dir)
        
        if args.output:
            output_file = exporter.export(
                articles,
                args.format,
                args.output,
                include_dates=args.show_dates,
                include_titles=args.show_titles,
            )
            print(f"\n✓ Exported to: {output_file}")

        # Print to console
        if not args.no_console:
            exporter.print_to_console(
                articles,
                include_dates=args.show_dates,
                include_titles=args.show_titles,
            )

        logger.info(f"Successfully processed {len(articles)} articles")
        return 0

    except ScraperError as e:
        logger.error(f"Scraping error: {e}")
        return 1
    except ExportError as e:
        logger.error(f"Export error: {e}")
        return 1
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 130
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
