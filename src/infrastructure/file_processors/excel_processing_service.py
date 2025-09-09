"""
Excel file processing service implementation using pandas.
"""

import pandas as pd
from typing import List, Dict, Any
from decimal import Decimal
import os

from ...domain.entities.product import Product
from ...domain.services.excel_processing_service import ExcelProcessingService
from ...shared.exceptions.exceptions import ExcelProcessingException


class PandasExcelProcessingService(ExcelProcessingService):
    """Pandas-based Excel file processing service implementation."""
    
    def __init__(self):
        """Initialize service with required columns configuration."""
        self._required_columns = ['SKU', 'Produto', 'PrecoUnit', 'Unidade', 'Estoque']
        self._column_mapping = {
            'SKU': 'sku',
            'Produto': 'name',
            'PrecoUnit': 'unit_price',
            'Unidade': 'unit',
            'Estoque': 'stock_quantity'
        }
    
    def read_products_from_excel(self, file_path: str) -> List[Product]:
        """
        Read products from Excel file.
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            List of Product entities
            
        Raises:
            ExcelProcessingException: If file format is invalid or required columns are missing
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                raise ExcelProcessingException(f"File not found: {file_path}", file_path)
            
            # Check file extension
            if not file_path.lower().endswith(('.xlsx', '.xls')):
                raise ExcelProcessingException("File must be an Excel file (.xlsx or .xls)", file_path)
            
            # Read Excel file
            try:
                df = pd.read_excel(file_path)
            except Exception as e:
                raise ExcelProcessingException(f"Failed to read Excel file: {str(e)}", file_path)
            
            # Validate structure
            if not self.validate_excel_structure(file_path):
                missing_columns = set(self._required_columns) - set(df.columns)
                raise ExcelProcessingException(
                    f"Missing required columns: {', '.join(missing_columns)}",
                    file_path
                )
            
            # Process rows
            products = []
            errors = []
            
            for index, row in df.iterrows():
                try:
                    product = self._process_row(row, index + 1)  # +1 for Excel row numbering
                    if product:
                        products.append(product)
                except Exception as e:
                    errors.append(f"Row {index + 1}: {str(e)}")
            
            # If there are errors but some products were processed successfully
            if errors and products:
                error_message = f"Processed {len(products)} products with {len(errors)} errors: {'; '.join(errors[:5])}"
                if len(errors) > 5:
                    error_message += f" and {len(errors) - 5} more errors"
                # Log errors but don't raise exception if we have some valid products
                print(f"Warning: {error_message}")
            
            # If all rows failed
            elif errors and not products:
                raise ExcelProcessingException(
                    f"No valid products found. Errors: {'; '.join(errors[:3])}",
                    file_path
                )
            
            return products
            
        except ExcelProcessingException:
            raise
        except Exception as e:
            raise ExcelProcessingException(f"Unexpected error processing Excel file: {str(e)}", file_path)
    
    def _process_row(self, row: pd.Series, row_number: int) -> Product:
        """Process a single Excel row into a Product entity."""
        try:
            # Extract and validate SKU
            sku = str(row['SKU']).strip() if pd.notna(row['SKU']) else ''
            if not sku:
                raise ValueError("SKU cannot be empty")
            
            # Extract and validate product name
            name = str(row['Produto']).strip() if pd.notna(row['Produto']) else ''
            if not name:
                raise ValueError("Product name cannot be empty")
            
            # Extract and validate unit price
            try:
                unit_price_value = row['PrecoUnit']
                if pd.isna(unit_price_value):
                    raise ValueError("Unit price cannot be empty")
                
                # Handle different formats (comma as decimal separator, etc.)
                if isinstance(unit_price_value, str):
                    unit_price_value = unit_price_value.replace(',', '.')
                
                unit_price = Decimal(str(unit_price_value))
                if unit_price < 0:
                    raise ValueError("Unit price cannot be negative")
                
            except (ValueError, TypeError) as e:
                raise ValueError(f"Invalid unit price format: {unit_price_value}")
            
            # Extract and validate unit
            unit = str(row['Unidade']).strip() if pd.notna(row['Unidade']) else ''
            if not unit:
                raise ValueError("Unit cannot be empty")
            
            # Extract and validate stock quantity
            try:
                stock_value = row['Estoque']
                if pd.isna(stock_value):
                    raise ValueError("Stock quantity cannot be empty")
                
                stock_quantity = int(float(stock_value))  # Convert to float first, then int
                if stock_quantity < 0:
                    raise ValueError("Stock quantity cannot be negative")
                
            except (ValueError, TypeError):
                raise ValueError(f"Invalid stock quantity format: {stock_value}")
            
            # Create and return Product entity
            return Product(
                sku=sku,
                name=name,
                unit_price=unit_price,
                unit=unit,
                stock_quantity=stock_quantity
            )
            
        except Exception as e:
            raise ValueError(f"Error processing row data: {str(e)}")
    
    def validate_excel_structure(self, file_path: str) -> bool:
        """
        Validate if Excel file has required columns.
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            True if valid structure, False otherwise
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return False
            
            # Read only the header
            df = pd.read_excel(file_path, nrows=0)
            
            # Check if all required columns are present
            missing_columns = set(self._required_columns) - set(df.columns)
            return len(missing_columns) == 0
            
        except Exception:
            return False
    
    def get_required_columns(self) -> List[str]:
        """
        Get list of required column names.
        
        Returns:
            List of required column names
        """
        return self._required_columns.copy()
