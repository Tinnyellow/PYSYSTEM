"""
Configuration utilities for the Sales Management System.
"""

import os
from typing import Optional
from dotenv import load_dotenv


class Configuration:
    """Configuration management class."""
    
    def __init__(self):
        """Initialize configuration by loading environment variables."""
        load_dotenv()
    
    @property
    def brasil_api_base_url(self) -> str:
        """Get Brasil API base URL."""
        return os.getenv('BRASIL_API_BASE_URL', 'https://brasilapi.com.br/api/v1')
    
    @property
    def data_directory(self) -> str:
        """Get data directory path."""
        return os.getenv('DATA_DIRECTORY', './data')
    
    @property
    def company_data_file(self) -> str:
        """Get company data file name."""
        return os.getenv('COMPANY_DATA_FILE', 'companies.json')
    
    @property
    def product_data_file(self) -> str:
        """Get product data file name."""
        return os.getenv('PRODUCT_DATA_FILE', 'products.json')
    
    @property
    def sales_order_data_file(self) -> str:
        """Get sales order data file name."""
        return os.getenv('SALES_ORDER_DATA_FILE', 'sales_orders.json')
    
    @property
    def reports_directory(self) -> str:
        """Get reports directory path."""
        return os.getenv('REPORTS_DIRECTORY', './data/reports')
    
    def get_full_data_path(self, filename: str) -> str:
        """Get full path for a data file."""
        return os.path.join(self.data_directory, filename)
    
    def get_full_reports_path(self, filename: str) -> str:
        """Get full path for a report file."""
        return os.path.join(self.reports_directory, filename)
    
    def ensure_directories_exist(self) -> None:
        """Ensure all required directories exist."""
        directories = [
            self.data_directory,
            self.reports_directory
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)


# Global configuration instance
config = Configuration()
