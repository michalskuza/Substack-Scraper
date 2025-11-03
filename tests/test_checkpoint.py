"""Tests for checkpoint module."""

import pytest
import tempfile
from pathlib import Path
from substack_scraper.checkpoint import Checkpoint
from substack_scraper.parser import Article


@pytest.fixture
def temp_checkpoint():
    """Fixture providing temporary checkpoint file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        checkpoint_file = Path(f.name)
    
    yield checkpoint_file
    
    if checkpoint_file.exists():
        checkpoint_file.unlink()


def test_save_checkpoint(temp_checkpoint):
    """Test saving checkpoint."""
    checkpoint = Checkpoint(str(temp_checkpoint))
    articles = [
        Article(url="https://example.com/p/article1", date="01.01.2024"),
        Article(url="https://example.com/p/article2", date="02.01.2024"),
    ]
    
    checkpoint.save("https://example.com/archive", articles)
    
    assert temp_checkpoint.exists()


def test_load_checkpoint(temp_checkpoint):
    """Test loading checkpoint."""
    checkpoint = Checkpoint(str(temp_checkpoint))
    articles = [
        Article(url="https://example.com/p/article1", date="01.01.2024"),
    ]
    
    checkpoint.save("https://example.com/archive", articles)
    data = checkpoint.load()
    
    assert data["url"] == "https://example.com/archive"
    assert data["total_articles"] == 1
    assert len(data["articles"]) == 1


def test_restore_articles(temp_checkpoint):
    """Test restoring articles from checkpoint."""
    checkpoint = Checkpoint(str(temp_checkpoint))
    articles = [
        Article(url="https://example.com/p/article1", date="01.01.2024", title="Article 1"),
        Article(url="https://example.com/p/article2", date="02.01.2024", title="Article 2"),
    ]
    
    checkpoint.save("https://example.com/archive", articles)
    restored = checkpoint.restore_articles()
    
    assert len(restored) == 2
    assert restored[0].url == "https://example.com/p/article1"
    assert restored[0].date == "01.01.2024"
    assert restored[0].title == "Article 1"


def test_checkpoint_exists(temp_checkpoint):
    """Test checking if checkpoint exists."""
    checkpoint = Checkpoint(str(temp_checkpoint))
    
    assert not checkpoint.exists()
    
    checkpoint.save("https://example.com/archive", [])
    
    assert checkpoint.exists()


def test_clear_checkpoint(temp_checkpoint):
    """Test clearing checkpoint."""
    checkpoint = Checkpoint(str(temp_checkpoint))
    checkpoint.save("https://example.com/archive", [])
    
    assert checkpoint.exists()
    
    checkpoint.clear()
    
    assert not checkpoint.exists()


def test_load_nonexistent_checkpoint(temp_checkpoint):
    """Test loading nonexistent checkpoint returns empty dict."""
    checkpoint = Checkpoint(str(temp_checkpoint))
    temp_checkpoint.unlink()  # Ensure it doesn't exist
    
    data = checkpoint.load()
    
    assert data == {}
