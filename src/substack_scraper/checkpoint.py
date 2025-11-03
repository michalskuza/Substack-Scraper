"""Checkpoint management for resume capability."""

import json
import logging
from typing import List, Dict, Any
from pathlib import Path
from .parser import Article

logger = logging.getLogger(__name__)


class Checkpoint:
    """Manages checkpoint files for resume capability."""

    def __init__(self, checkpoint_file: str = ".checkpoint.json"):
        """
        Initialize checkpoint manager.

        Args:
            checkpoint_file: Path to checkpoint file
        """
        self.checkpoint_file = Path(checkpoint_file)

    def save(self, url: str, articles: List[Article], metadata: Dict[str, Any] = None) -> None:
        """
        Save checkpoint data.

        Args:
            url: Scraped URL
            articles: List of scraped articles
            metadata: Additional metadata to save
        """
        try:
            data = {
                "url": url,
                "total_articles": len(articles),
                "articles": [article.to_dict() for article in articles],
                "metadata": metadata or {},
            }

            with open(self.checkpoint_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            logger.info(f"Checkpoint saved: {len(articles)} articles")

        except Exception as e:
            logger.error(f"Failed to save checkpoint: {e}")

    def load(self) -> Dict[str, Any]:
        """
        Load checkpoint data.

        Returns:
            Dictionary with checkpoint data or empty dict if not found
        """
        if not self.checkpoint_file.exists():
            logger.info("No checkpoint file found")
            return {}

        try:
            with open(self.checkpoint_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            logger.info(f"Checkpoint loaded: {data.get('total_articles', 0)} articles")
            return data

        except Exception as e:
            logger.error(f"Failed to load checkpoint: {e}")
            return {}

    def restore_articles(self) -> List[Article]:
        """
        Restore articles from checkpoint.

        Returns:
            List of Article objects
        """
        data = self.load()
        articles = []

        for article_data in data.get("articles", []):
            article = Article(
                url=article_data["url"],
                date=article_data.get("date"),
                title=article_data.get("title"),
            )
            articles.append(article)

        return articles

    def clear(self) -> None:
        """Delete checkpoint file."""
        if self.checkpoint_file.exists():
            try:
                self.checkpoint_file.unlink()
                logger.info("Checkpoint cleared")
            except Exception as e:
                logger.error(f"Failed to clear checkpoint: {e}")

    def exists(self) -> bool:
        """Check if checkpoint file exists."""
        return self.checkpoint_file.exists()
