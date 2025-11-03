"""Export functionality for scraped articles."""

import json
import csv
import logging
from typing import List
from pathlib import Path
from .parser import Article

logger = logging.getLogger(__name__)


class ExportError(Exception):
    """Base exception for export errors."""
    pass


class Exporter:
    """Handles exporting articles to various formats."""

    SUPPORTED_FORMATS = ["txt", "csv", "json"]

    def __init__(self, output_dir: str = "output"):
        """
        Initialize exporter.

        Args:
            output_dir: Directory to save output files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(
        self,
        articles: List[Article],
        format: str,
        filename: str,
        include_dates: bool = False,
        include_titles: bool = False,
    ) -> Path:
        """
        Export articles to specified format.

        Args:
            articles: List of articles to export
            format: Output format (txt, csv, json)
            filename: Output filename (without extension)
            include_dates: Whether to include dates in output
            include_titles: Whether to include titles in output

        Returns:
            Path to exported file

        Raises:
            ExportError: If export fails
        """
        format = format.lower()
        
        if format not in self.SUPPORTED_FORMATS:
            raise ExportError(f"Unsupported format: {format}. Supported: {self.SUPPORTED_FORMATS}")

        output_file = self.output_dir / f"{filename}.{format}"

        try:
            if format == "txt":
                self._export_txt(articles, output_file, include_dates, include_titles)
            elif format == "csv":
                self._export_csv(articles, output_file, include_dates, include_titles)
            elif format == "json":
                self._export_json(articles, output_file)

            logger.info(f"Exported {len(articles)} articles to {output_file}")
            return output_file

        except Exception as e:
            logger.error(f"Export failed: {e}")
            raise ExportError(f"Failed to export to {format}: {e}")

    def _export_txt(
        self,
        articles: List[Article],
        output_file: Path,
        include_dates: bool,
        include_titles: bool,
    ) -> None:
        """Export articles to plain text file."""
        with open(output_file, "w", encoding="utf-8") as f:
            for article in articles:
                parts = []
                
                if include_dates and article.date:
                    parts.append(article.date)
                
                if include_titles and article.title:
                    parts.append(article.title)
                
                parts.append(article.url)
                
                f.write(" - ".join(parts) + "\n")

    def _export_csv(
        self,
        articles: List[Article],
        output_file: Path,
        include_dates: bool,
        include_titles: bool,
    ) -> None:
        """Export articles to CSV file."""
        with open(output_file, "w", encoding="utf-8", newline="") as f:
            fieldnames = ["url"]
            
            if include_dates:
                fieldnames.insert(0, "date")
            
            if include_titles:
                fieldnames.insert(0 if not include_dates else 1, "title")

            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for article in articles:
                row = {"url": article.url}
                
                if include_dates:
                    row["date"] = article.date or ""
                
                if include_titles:
                    row["title"] = article.title or ""
                
                writer.writerow(row)

    def _export_json(self, articles: List[Article], output_file: Path) -> None:
        """Export articles to JSON file."""
        data = {
            "total_articles": len(articles),
            "articles": [article.to_dict() for article in articles],
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def print_to_console(
        self,
        articles: List[Article],
        include_dates: bool = False,
        include_titles: bool = False,
    ) -> None:
        """
        Print articles to console.

        Args:
            articles: List of articles to print
            include_dates: Whether to include dates
            include_titles: Whether to include titles
        """
        print(f"\nFound {len(articles)} articles:\n")
        
        for article in articles:
            parts = []
            
            if include_dates and article.date:
                parts.append(article.date)
            
            if include_titles and article.title:
                parts.append(article.title)
            
            parts.append(article.url)
            
            print(" - ".join(parts))
