"""Application configuration using Pydantic Settings v2.

Manages database connections, LLM provider choices, RAG parameters,
and agent execution guardrails through environment variables.
"""

from pathlib import Path
from typing import Literal, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for the Commercial Analytics Copilot."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # General App Config
    ENVIRONMENT: Literal["development", "testing", "production"] = "development"
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    # Project Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = Field(default_factory=lambda: Path("data"))
    RAW_DATA_DIR: Path = Field(default_factory=lambda: Path("data/raw"))
    PROCESSED_DATA_DIR: Path = Field(default_factory=lambda: Path("data/processed"))
    RESULTS_DIR: Path = Field(default_factory=lambda: Path("results"))
    DOCS_DIR: Path = Field(default_factory=lambda: Path("docs"))

    # Database Configuration
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "retail_analytics"
    DB_USER: str = "analytics_user"
    DB_PASSWORD: str = "analytics_password_dev"
    DB_ROOT_PASSWORD: str = "root_password_dev"

    # Read-Only Database User (Restricted for Text-to-SQL execution)
    DB_READONLY_USER: str = "analytics_ro"
    DB_READONLY_PASSWORD: str = "analytics_ro_password_dev"

    # SQLite Local Fallback for local testing when MySQL is not running
    USE_SQLITE_FALLBACK: bool = True
    SQLITE_DB_PATH: str = "data/processed/retail_analytics.db"

    # LLM Settings
    LLM_PROVIDER: Literal["ollama", "openai", "anthropic", "mock"] = "ollama"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    MODEL_NAME: str = "qwen2.5:7b-instruct"
    TEMPERATURE: float = Field(default=0.0, ge=0.0, le=2.0)
    TOP_P: float = Field(default=0.9, ge=0.0, le=1.0)
    MAX_TOKENS: int = Field(default=2048, ge=64, le=8192)

    # Cloud LLM API Keys (Optional)
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    # RAG & Vector Search
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    VECTOR_STORE_DIR: Path = Field(default_factory=lambda: Path("data/processed/vectorstore"))
    RETRIEVAL_TOP_K: int = Field(default=4, ge=1, le=20)
    SIMILARITY_THRESHOLD: float = Field(default=0.45, ge=0.0, le=1.0)

    # Security & Guardrails
    SQL_QUERY_TIMEOUT_SECONDS: int = Field(default=10, ge=1, le=60)
    SQL_MAX_ROWS_RETURNED: int = Field(default=100, ge=1, le=1000)
    MAX_AGENT_STEPS: int = Field(default=6, ge=1, le=12)
    MAX_AGENT_RETRIES: int = Field(default=2, ge=0, le=5)

    @property
    def mysql_readwrite_url(self) -> str:
        """Construct read-write MySQL SQLAlchemy URL."""
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def mysql_readonly_url(self) -> str:
        """Construct read-only MySQL SQLAlchemy URL."""
        return (
            f"mysql+pymysql://{self.DB_READONLY_USER}:{self.DB_READONLY_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def sqlite_url(self) -> str:
        """Construct SQLite URL."""
        return f"sqlite:///{self.SQLITE_DB_PATH}"

    def get_db_url(self, readonly: bool = False) -> str:
        """Get the active database URL based on fallback preference."""
        if self.USE_SQLITE_FALLBACK:
            return self.sqlite_url
        return self.mysql_readonly_url if readonly else self.mysql_readwrite_url


# Global settings singleton
settings = Settings()
