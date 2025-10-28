"""
HARV SHIPPED - Unified Configuration
Combines configuration from Steel2, Doc Digester, and Harv
"""
from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path


class Settings(BaseSettings):
    """Unified settings for all three systems."""

    # ========================================================================
    # Application Settings
    # ========================================================================
    APP_NAME: str = "HARV SHIPPED"
    APP_VERSION: str = "1.0.0"
    ENV: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ========================================================================
    # Database Configuration
    # ========================================================================
    DATABASE_URL: str = "sqlite:///./backend/data/harv.db"

    # ========================================================================
    # AI Provider Configuration
    # ========================================================================
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    XAI_API_KEY: str = ""

    DEFAULT_AI_PROVIDER: str = "openai"
    DEFAULT_MODEL: str = "gpt-4o"

    # ========================================================================
    # Authentication & Security
    # ========================================================================
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ========================================================================
    # CORS Configuration
    # ========================================================================
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    # ========================================================================
    # Curriculum Generation (Steel2)
    # ========================================================================
    CURRICULUM_OUTPUT_DIR: str = "./backend/data/curriculum"
    TOTAL_WEEKS: int = 35
    DAYS_PER_WEEK: int = 4
    MAX_RETRIES: int = 10

    @property
    def curriculum_path(self) -> Path:
        path = Path(self.CURRICULUM_OUTPUT_DIR)
        path.mkdir(parents=True, exist_ok=True)
        return path

    # ========================================================================
    # Content Analyzer (Doc Digester)
    # ========================================================================
    ANALYSIS_OUTPUT_DIR: str = "./backend/data/analyzed_content"
    MAX_FILE_SIZE_MB: int = 100
    SUPPORTED_FORMATS: str = "txt,docx,pdf"

    @property
    def analysis_path(self) -> Path:
        path = Path(self.ANALYSIS_OUTPUT_DIR)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def supported_file_formats(self) -> List[str]:
        return [fmt.strip() for fmt in self.SUPPORTED_FORMATS.split(",")]

    # ========================================================================
    # AI Tutor (Harv)
    # ========================================================================
    MEMORY_LAYERS: int = 4
    MAX_CONVERSATION_HISTORY: int = 10

    # ========================================================================
    # Pipeline Integration
    # ========================================================================
    ENABLE_AUTO_VALIDATION: bool = True
    ENABLE_AUTO_IMPORT: bool = True
    QUALITY_THRESHOLD: float = 8.0
    AUTO_REFINE_ON_LOW_QUALITY: bool = True

    # ========================================================================
    # Feature Flags
    # ========================================================================
    ENABLE_ANALYTICS: bool = True
    ENABLE_PATTERN_EXTRACTION: bool = True
    ENABLE_FEEDBACK_LOOP: bool = True
    ENABLE_MULTI_SUBJECT: bool = False

    # ========================================================================
    # Budget & Cost Controls
    # ========================================================================
    ENABLE_BUDGET_TRACKING: bool = True
    MONTHLY_BUDGET_USD: float = 100.00
    COST_ALERT_THRESHOLD: float = 0.80

    # ========================================================================
    # Logging
    # ========================================================================
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "./logs"
    LOG_FORMAT: str = "json"

    @property
    def log_path(self) -> Path:
        path = Path(self.LOG_DIR)
        path.mkdir(parents=True, exist_ok=True)
        return path

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()
