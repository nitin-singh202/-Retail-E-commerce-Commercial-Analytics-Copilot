"""Tests for application configuration loading and validation."""

import pytest
from src.copilot.config import Settings


def test_settings_default_values():
    """Verify default configuration values."""
    settings = Settings()
    assert settings.APP_PORT == 8000
    assert settings.LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    assert settings.TEMPERATURE == 0.0
    assert settings.SQL_QUERY_TIMEOUT_SECONDS > 0
    assert settings.SQL_MAX_ROWS_RETURNED == 100


def test_db_urls():
    """Verify database URL construction for MySQL and SQLite."""
    settings = Settings()
    assert "sqlite:///" in settings.sqlite_url
    assert "mysql+pymysql://" in settings.mysql_readwrite_url
    assert "mysql+pymysql://" in settings.mysql_readonly_url
    assert settings.DB_READONLY_USER in settings.mysql_readonly_url


def test_custom_env_override():
    """Verify that settings can be customized via constructor/env."""
    custom_settings = Settings(
        APP_PORT=9000,
        TEMPERATURE=0.5,
        LLM_PROVIDER="openai"
    )
    assert custom_settings.APP_PORT == 9000
    assert custom_settings.TEMPERATURE == 0.5
    assert custom_settings.LLM_PROVIDER == "openai"
