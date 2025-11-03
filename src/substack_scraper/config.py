"""Configuration management for Substack Scraper."""

import json
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class Config:
    """Manages configuration settings from files or defaults."""

    DEFAULT_CONFIG = {
        "browser": {
            "engine": "chrome",
            "headless": True,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "timeout": 30,
            "page_load_timeout": 60,
        },
        "scraping": {
            "initial_wait": {"min": 3, "max": 6},
            "scroll_wait": {"min": 2, "max": 5},
            "rate_limit_delay": 1.0,
            "max_retries": 3,
            "retry_delay": 5,
        },
        "output": {
            "format": "txt",
            "directory": "output",
            "include_dates": False,
            "sort_by_date": False,
            "ascending": False,
        },
        "checkpoint": {
            "enabled": True,
            "file": ".checkpoint.json",
        },
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "file": None,
        },
    }

    def __init__(self, config_file: Optional[Path] = None):
        """
        Initialize configuration.

        Args:
            config_file: Path to configuration file (YAML or JSON)
        """
        self.config = self.DEFAULT_CONFIG.copy()

        if config_file and config_file.exists():
            self.load_from_file(config_file)

    def load_from_file(self, config_file: Path) -> None:
        """
        Load configuration from file.

        Args:
            config_file: Path to configuration file

        Raises:
            ValueError: If file format is unsupported
        """
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                if config_file.suffix in [".yaml", ".yml"]:
                    user_config = yaml.safe_load(f)
                elif config_file.suffix == ".json":
                    user_config = json.load(f)
                else:
                    raise ValueError(f"Unsupported config format: {config_file.suffix}")

            self._merge_config(user_config)
            logger.info(f"Loaded configuration from {config_file}")
        except Exception as e:
            logger.error(f"Failed to load config from {config_file}: {e}")
            raise

    def _merge_config(self, user_config: Dict[str, Any]) -> None:
        """Recursively merge user config with defaults."""
        for key, value in user_config.items():
            if key in self.config and isinstance(value, dict) and isinstance(self.config[key], dict):
                self.config[key].update(value)
            else:
                self.config[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot notation.

        Args:
            key: Configuration key (e.g., 'browser.engine')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value by dot notation.

        Args:
            key: Configuration key (e.g., 'browser.engine')
            value: Value to set
        """
        keys = key.split(".")
        config = self.config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value

    def save_to_file(self, config_file: Path) -> None:
        """
        Save current configuration to file.

        Args:
            config_file: Path to save configuration
        """
        try:
            with open(config_file, "w", encoding="utf-8") as f:
                if config_file.suffix in [".yaml", ".yml"]:
                    yaml.dump(self.config, f, default_flow_style=False)
                elif config_file.suffix == ".json":
                    json.dump(self.config, f, indent=2)
                else:
                    raise ValueError(f"Unsupported config format: {config_file.suffix}")
            logger.info(f"Saved configuration to {config_file}")
        except Exception as e:
            logger.error(f"Failed to save config to {config_file}: {e}")
            raise
