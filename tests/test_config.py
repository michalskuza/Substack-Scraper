"""Tests for configuration module."""

import pytest
import tempfile
import json
from pathlib import Path
from substack_scraper.config import Config


def test_default_config():
    """Test default configuration values."""
    config = Config()
    
    assert config.get("browser.engine") == "chrome"
    assert config.get("browser.headless") is True
    assert config.get("scraping.max_retries") == 3
    assert config.get("output.format") == "txt"


def test_config_get_with_dot_notation():
    """Test getting config values with dot notation."""
    config = Config()
    
    assert config.get("browser.engine") == "chrome"
    assert config.get("scraping.initial_wait.min") == 3
    assert config.get("nonexistent.key", "default") == "default"


def test_config_set():
    """Test setting config values."""
    config = Config()
    
    config.set("browser.engine", "firefox")
    assert config.get("browser.engine") == "firefox"
    
    config.set("new.nested.key", "value")
    assert config.get("new.nested.key") == "value"


def test_load_json_config():
    """Test loading configuration from JSON file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config_data = {
            "browser": {"engine": "firefox"},
            "output": {"format": "csv"}
        }
        json.dump(config_data, f)
        config_file = Path(f.name)
    
    try:
        config = Config(config_file)
        assert config.get("browser.engine") == "firefox"
        assert config.get("output.format") == "csv"
        assert config.get("browser.headless") is True  # Default should still be there
    finally:
        config_file.unlink()


def test_save_config():
    """Test saving configuration to file."""
    config = Config()
    config.set("browser.engine", "edge")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config_file = Path(f.name)
    
    try:
        config.save_to_file(config_file)
        
        loaded_config = Config(config_file)
        assert loaded_config.get("browser.engine") == "edge"
    finally:
        config_file.unlink()
