"""
Data Transfer Objects for Sales Order operations.
"""

from dataclasses import dataclass
from typing import List
from decimal import Decimal


@dataclass
class CreateSalesOrderDTO:
    """DTO for creating a new sales order."""
    
    company_id: str


@dataclass
class AddOrderItemDTO:
    """DTO for adding item to sales order."""
    
    order_id: str
    product_id: str
    quantity: int


@dataclass
class UpdateOrderItemDTO:
    """DTO for updating order item quantity."""
    
    order_id: str
    product_id: str
    new_quantity: int


@dataclass
class SalesOrderItemResponseDTO:
    """DTO for sales order item response."""
    
    id: str
    product_id: str
    product_sku: str
    product_name: str
    quantity: int
    unit_price: Decimal
    formatted_unit_price: str
    subtotal: Decimal
    formatted_subtotal: str


@dataclass
class SalesOrderResponseDTO:
    """DTO for sales order response."""
    
    id: str
    company_id: str
    company_name: str
    company_document: str
    items: List[SalesOrderItemResponseDTO]
    total_items: int
    total_amount: Decimal
    formatted_total_amount: str
    created_at: str
    updated_at: str
    is_valid: bool


@dataclass
class GenerateReportDTO:
    """DTO for report generation request."""
    
    order_id: str
    format_type: str = "PDF"
    custom_output_path: str = None
