"""
Configuration Management System for PYSYSTEM.
Handles environment variables and application settings.
"""

import os
from typing import Any, Optional, Union
from pathlib import Path
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Database-like configuration for JSON file operations."""
    data_dir: str = "data"
    companies_file: str = "companies.json"
    products_file: str = "products.json"
    sales_orders_file: str = "sales_orders.json"
    backup_enabled: bool = True
    backup_dir: str = "backups"
    backup_retention_days: int = 30


@dataclass
class APIConfig:
    """External API configuration."""
    brasilapi_base_url: str = "https://brasilapi.com.br/api"
    brasilapi_timeout: int = 10
    brasilapi_retry_attempts: int = 3
    cache_enabled: bool = True
    cache_dir: str = "cache"
    cache_ttl_seconds: int = 3600


@dataclass
class GUIConfig:
    """GUI configuration settings."""
    window_width: int = 1200
    window_height: int = 800
    window_min_width: int = 800
    window_min_height: int = 600
    theme: str = "corporate"
    gui_scaling: float = 1.0


@dataclass
class ValidationConfig:
    """Validation settings."""
    validate_cpf_cnpj: bool = True
    allow_invalid_test_documents: bool = False
    validate_cep: bool = True
    auto_complete_address: bool = True


@dataclass
class PerformanceConfig:
    """Performance and optimization settings."""
    max_records_per_page: int = 50
    enable_search_indexing: bool = True
    search_min_chars: int = 2
    max_excel_rows: int = 10000
    excel_chunk_size: int = 1000


@dataclass
class LoggingConfig:
    """Logging configuration."""
    log_dir: str = "logs"
    log_file: str = "pysystem.log"
    log_level: str = "INFO"
    log_max_size_mb: int = 10
    log_backup_count: int = 5
    log_to_console: bool = True
    console_log_level: str = "INFO"


@dataclass
class BusinessRulesConfig:
    """Business logic configuration."""
    allow_negative_stock: bool = False
    require_customer_validation: bool = True
    auto_generate_order_number: bool = True
    auto_update_stock: bool = True
    track_inventory_changes: bool = True
    require_product_categories: bool = False


@dataclass
class FeatureFlags:
    """Feature toggles for the application."""
    enable_excel_import: bool = True
    enable_pdf_export: bool = True
    enable_brasilapi_integration: bool = True
    enable_address_autocomplete: bool = True
    enable_company_lookup: bool = True
    enable_advanced_search: bool = True
    enable_bulk_operations: bool = True
    enable_data_export: bool = True
    enable_system_backups: bool = True
    enable_dark_mode: bool = False
    enable_plugins: bool = False
    enable_api_server: bool = False


class ConfigManager:
    """Manages application configuration from environment variables."""
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            env_file: Path to .env file (optional)
        """
        self._load_env_file(env_file)
        
        # Initialize configuration objects
        self.database = DatabaseConfig(
            data_dir=self._get_env("DATA_DIR", "data"),
            companies_file=self._get_env("COMPANIES_FILE", "companies.json"),
            products_file=self._get_env("PRODUCTS_FILE", "products.json"),
            sales_orders_file=self._get_env("SALES_ORDERS_FILE", "sales_orders.json"),
            backup_enabled=self._get_env_bool("BACKUP_ENABLED", True),
            backup_dir=self._get_env("BACKUP_DIR", "backups"),
            backup_retention_days=self._get_env_int("BACKUP_RETENTION_DAYS", 30)
        )
        
        self.api = APIConfig(
            brasilapi_base_url=self._get_env("BRASILAPI_BASE_URL", "https://brasilapi.com.br/api"),
            brasilapi_timeout=self._get_env_int("BRASILAPI_TIMEOUT", 10),
            brasilapi_retry_attempts=self._get_env_int("BRASILAPI_RETRY_ATTEMPTS", 3),
            cache_enabled=self._get_env_bool("CACHE_ENABLED", True),
            cache_dir=self._get_env("CACHE_DIR", "cache"),
            cache_ttl_seconds=self._get_env_int("CACHE_TTL_SECONDS", 3600)
        )
        
        self.gui = GUIConfig(
            window_width=self._get_env_int("WINDOW_WIDTH", 1200),
            window_height=self._get_env_int("WINDOW_HEIGHT", 800),
            window_min_width=self._get_env_int("WINDOW_MIN_WIDTH", 800),
            window_min_height=self._get_env_int("WINDOW_MIN_HEIGHT", 600),
            theme=self._get_env("THEME", "corporate"),
            gui_scaling=self._get_env_float("GUI_SCALING", 1.0)
        )
        
        self.validation = ValidationConfig(
            validate_cpf_cnpj=self._get_env_bool("VALIDATE_CPF_CNPJ", True),
            allow_invalid_test_documents=self._get_env_bool("ALLOW_INVALID_TEST_DOCUMENTS", False),
            validate_cep=self._get_env_bool("VALIDATE_CEP", True),
            auto_complete_address=self._get_env_bool("AUTO_COMPLETE_ADDRESS", True)
        )
        
        self.performance = PerformanceConfig(
            max_records_per_page=self._get_env_int("MAX_RECORDS_PER_PAGE", 50),
            enable_search_indexing=self._get_env_bool("ENABLE_SEARCH_INDEXING", True),
            search_min_chars=self._get_env_int("SEARCH_MIN_CHARS", 2),
            max_excel_rows=self._get_env_int("MAX_EXCEL_ROWS", 10000),
            excel_chunk_size=self._get_env_int("EXCEL_CHUNK_SIZE", 1000)
        )
        
        self.logging = LoggingConfig(
            log_dir=self._get_env("LOG_DIR", "logs"),
            log_file=self._get_env("LOG_FILE", "pysystem.log"),
            log_level=self._get_env("LOG_LEVEL", "INFO"),
            log_max_size_mb=self._get_env_int("LOG_MAX_SIZE_MB", 10),
            log_backup_count=self._get_env_int("LOG_BACKUP_COUNT", 5),
            log_to_console=self._get_env_bool("LOG_TO_CONSOLE", True),
            console_log_level=self._get_env("CONSOLE_LOG_LEVEL", "INFO")
        )
        
        self.business_rules = BusinessRulesConfig(
            allow_negative_stock=self._get_env_bool("ALLOW_NEGATIVE_STOCK", False),
            require_customer_validation=self._get_env_bool("REQUIRE_CUSTOMER_VALIDATION", True),
            auto_generate_order_number=self._get_env_bool("AUTO_GENERATE_ORDER_NUMBER", True),
            auto_update_stock=self._get_env_bool("AUTO_UPDATE_STOCK", True),
            track_inventory_changes=self._get_env_bool("TRACK_INVENTORY_CHANGES", True),
            require_product_categories=self._get_env_bool("REQUIRE_PRODUCT_CATEGORIES", False)
        )
        
        self.features = FeatureFlags(
            enable_excel_import=self._get_env_bool("ENABLE_EXCEL_IMPORT", True),
            enable_pdf_export=self._get_env_bool("ENABLE_PDF_EXPORT", True),
            enable_brasilapi_integration=self._get_env_bool("ENABLE_BRASILAPI_INTEGRATION", True),
            enable_address_autocomplete=self._get_env_bool("ENABLE_ADDRESS_AUTOCOMPLETE", True),
            enable_company_lookup=self._get_env_bool("ENABLE_COMPANY_LOOKUP", True),
            enable_advanced_search=self._get_env_bool("ENABLE_ADVANCED_SEARCH", True),
            enable_bulk_operations=self._get_env_bool("ENABLE_BULK_OPERATIONS", True),
            enable_data_export=self._get_env_bool("ENABLE_DATA_EXPORT", True),
            enable_system_backups=self._get_env_bool("ENABLE_SYSTEM_BACKUPS", True),
            enable_dark_mode=self._get_env_bool("ENABLE_DARK_MODE", False),
            enable_plugins=self._get_env_bool("ENABLE_PLUGINS", False),
            enable_api_server=self._get_env_bool("ENABLE_API_SERVER", False)
        )
    
    def _load_env_file(self, env_file: Optional[str] = None) -> None:
        """Load environment variables from .env file."""
        if env_file is None:
            env_file = ".env"
        
        env_path = Path(env_file)
        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        
                        os.environ[key] = value
    
    def _get_env(self, key: str, default: str) -> str:
        """Get string environment variable."""
        return os.environ.get(key, default)
    
    def _get_env_int(self, key: str, default: int) -> int:
        """Get integer environment variable."""
        value = os.environ.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            return default
    
    def _get_env_float(self, key: str, default: float) -> float:
        """Get float environment variable."""
        value = os.environ.get(key)
        if value is None:
            return default
        try:
            return float(value)
        except ValueError:
            return default
    
    def _get_env_bool(self, key: str, default: bool) -> bool:
        """Get boolean environment variable."""
        value = os.environ.get(key)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on', 'enabled')
    
    def get_data_path(self, filename: str) -> Path:
        """Get full path to data file."""
        return Path(self.database.data_dir) / filename
    
    def get_cache_path(self, filename: str) -> Path:
        """Get full path to cache file."""
        return Path(self.api.cache_dir) / filename
    
    def get_log_path(self) -> Path:
        """Get full path to log file."""
        return Path(self.logging.log_dir) / self.logging.log_file
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if a feature is enabled."""
        return getattr(self.features, f"enable_{feature_name}", False)


# Global configuration instance
config = ConfigManager()
