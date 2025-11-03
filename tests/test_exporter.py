"""Tests for exporter module."""

import pytest
import json
import csv
import tempfile
from pathlib import Path
from substack_scraper.exporter import Exporter, ExportError
from substack_scraper.parser import Article


@pytest.fixture
def sample_articles():
    """Fixture providing sample articles."""
    return [
        Article(url="https://example.com/p/article1", date="01.01.2024", title="Article 1"),
        Article(url="https://example.com/p/article2", date="02.01.2024", title="Article 2"),
        Article(url="https://example.com/p/article3", date="03.01.2024", title="Article 3"),
    ]


@pytest.fixture
def temp_output_dir():
    """Fixture providing temporary output directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


def test_export_txt(sample_articles, temp_output_dir):
    """Test exporting to TXT format."""
    exporter = Exporter(temp_output_dir)
    output_file = exporter.export(sample_articles, "txt", "test")
    
    assert output_file.exists()
    
    with open(output_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    assert len(lines) == 3
    assert "https://example.com/p/article1" in lines[0]


def test_export_txt_with_dates(sample_articles, temp_output_dir):
    """Test exporting to TXT with dates."""
    exporter = Exporter(temp_output_dir)
    output_file = exporter.export(sample_articles, "txt", "test", include_dates=True)
    
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    assert "01.01.2024" in content


def test_export_csv(sample_articles, temp_output_dir):
    """Test exporting to CSV format."""
    exporter = Exporter(temp_output_dir)
    output_file = exporter.export(sample_articles, "csv", "test", include_dates=True)
    
    assert output_file.exists()
    
    with open(output_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    assert len(rows) == 3
    assert "url" in rows[0]
    assert "date" in rows[0]


def test_export_json(sample_articles, temp_output_dir):
    """Test exporting to JSON format."""
    exporter = Exporter(temp_output_dir)
    output_file = exporter.export(sample_articles, "json", "test")
    
    assert output_file.exists()
    
    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    assert data["total_articles"] == 3
    assert len(data["articles"]) == 3
    assert "url" in data["articles"][0]


def test_export_unsupported_format(sample_articles, temp_output_dir):
    """Test exporting with unsupported format raises error."""
    exporter = Exporter(temp_output_dir)
    
    with pytest.raises(ExportError):
        exporter.export(sample_articles, "xml", "test")


def test_output_dir_created(sample_articles):
    """Test that output directory is created if it doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "new_dir"
        exporter = Exporter(str(output_dir))
        
        assert output_dir.exists()
