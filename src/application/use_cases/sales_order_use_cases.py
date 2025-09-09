"""
Sales Order management use cases.
"""

from typing import List
from ..dtos.sales_order_dto import (
    CreateSalesOrderDTO,
    AddOrderItemDTO,
    UpdateOrderItemDTO,
    SalesOrderResponseDTO,
    SalesOrderItemResponseDTO,
    GenerateReportDTO
)
from ...domain.entities.sales_order import SalesOrder, SalesOrderItem
from ...domain.repositories.sales_order_repository import SalesOrderRepository
from ...domain.repositories.company_repository import CompanyRepository
from ...domain.repositories.product_repository import ProductRepository
from ...domain.services.report_generation_service import ReportGenerationService
from ...shared.exceptions.exceptions import (
    EntityNotFoundException, 
    ValidationException,
    InsufficientStockException,
    ReportGenerationException
)
from ...shared.utils.format_utils import FormatUtils


class CreateSalesOrderUseCase:
    """Use case for creating a new sales order."""
    
    def __init__(self, 
                 sales_order_repository: SalesOrderRepository,
                 company_repository: CompanyRepository):
        self._sales_order_repository = sales_order_repository
        self._company_repository = company_repository
    
    def execute(self, dto: CreateSalesOrderDTO) -> SalesOrderResponseDTO:
        """Execute sales order creation."""
        # Verify company exists
        company = self._company_repository.find_by_id(dto.company_id)
        if not company:
            raise EntityNotFoundException("Company", dto.company_id)
        
        # Create sales order
        sales_order = SalesOrder(company=company)
        
        # Save sales order
        saved_order = self._sales_order_repository.save(sales_order)
        
        return self._map_to_response_dto(saved_order)
    
    def _map_to_response_dto(self, sales_order: SalesOrder) -> SalesOrderResponseDTO:
        """Map sales order entity to response DTO."""
        item_dtos = [
            self._map_item_to_response_dto(item) 
            for item in sales_order.items
        ]
        
        return SalesOrderResponseDTO(
            id=sales_order.id,
            company_id=sales_order.company.id,
            company_name=sales_order.company.name,
            company_document=sales_order.company.document.get_formatted(),
            items=item_dtos,
            total_items=sales_order.total_items,
            total_amount=sales_order.total_amount,
            formatted_total_amount=FormatUtils.format_currency(sales_order.total_amount),
            created_at=sales_order.created_at.isoformat(),
            updated_at=sales_order.updated_at.isoformat(),
            is_valid=sales_order.is_valid()
        )
    
    def _map_item_to_response_dto(self, item: SalesOrderItem) -> SalesOrderItemResponseDTO:
        """Map sales order item to response DTO."""
        return SalesOrderItemResponseDTO(
            id=item.id,
            product_id=item.product.id,
            product_sku=item.product.sku,
            product_name=item.product.name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            formatted_unit_price=FormatUtils.format_currency(item.unit_price),
            subtotal=item.subtotal,
            formatted_subtotal=FormatUtils.format_currency(item.subtotal)
        )


class AddItemToOrderUseCase:
    """Use case for adding item to sales order."""
    
    def __init__(self, 
                 sales_order_repository: SalesOrderRepository,
                 product_repository: ProductRepository):
        self._sales_order_repository = sales_order_repository
        self._product_repository = product_repository
    
    def execute(self, dto: AddOrderItemDTO) -> SalesOrderResponseDTO:
        """Execute add item to order."""
        # Find sales order
        sales_order = self._sales_order_repository.find_by_id(dto.order_id)
        if not sales_order:
            raise EntityNotFoundException("Sales Order", dto.order_id)
        
        # Find product
        product = self._product_repository.find_by_id(dto.product_id)
        if not product:
            raise EntityNotFoundException("Product", dto.product_id)
        
        # Validate quantity
        if dto.quantity <= 0:
            raise ValidationException("Quantity must be greater than zero", "quantity")
        
        # Check stock availability
        if not product.is_available(dto.quantity):
            raise InsufficientStockException(
                product.sku, 
                dto.quantity, 
                product.stock_quantity
            )
        
        # Add item to order
        sales_order.add_item(product, dto.quantity)
        
        # Update product stock
        product.update_stock(-dto.quantity)
        self._product_repository.update(product)
        
        # Save updated order
        updated_order = self._sales_order_repository.update(sales_order)
        
        return self._map_to_response_dto(updated_order)
    
    def _map_to_response_dto(self, sales_order: SalesOrder) -> SalesOrderResponseDTO:
        """Map sales order entity to response DTO."""
        item_dtos = [
            self._map_item_to_response_dto(item) 
            for item in sales_order.items
        ]
        
        return SalesOrderResponseDTO(
            id=sales_order.id,
            company_id=sales_order.company.id,
            company_name=sales_order.company.name,
            company_document=sales_order.company.document.get_formatted(),
            items=item_dtos,
            total_items=sales_order.total_items,
            total_amount=sales_order.total_amount,
            formatted_total_amount=FormatUtils.format_currency(sales_order.total_amount),
            created_at=sales_order.created_at.isoformat(),
            updated_at=sales_order.updated_at.isoformat(),
            is_valid=sales_order.is_valid()
        )
    
    def _map_item_to_response_dto(self, item: SalesOrderItem) -> SalesOrderItemResponseDTO:
        """Map sales order item to response DTO."""
        return SalesOrderItemResponseDTO(
            id=item.id,
            product_id=item.product.id,
            product_sku=item.product.sku,
            product_name=item.product.name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            formatted_unit_price=FormatUtils.format_currency(item.unit_price),
            subtotal=item.subtotal,
            formatted_subtotal=FormatUtils.format_currency(item.subtotal)
        )


class UpdateOrderItemUseCase:
    """Use case for updating order item quantity."""
    
    def __init__(self, 
                 sales_order_repository: SalesOrderRepository,
                 product_repository: ProductRepository):
        self._sales_order_repository = sales_order_repository
        self._product_repository = product_repository
    
    def execute(self, dto: UpdateOrderItemDTO) -> SalesOrderResponseDTO:
        """Execute order item update."""
        # Find sales order
        sales_order = self._sales_order_repository.find_by_id(dto.order_id)
        if not sales_order:
            raise EntityNotFoundException("Sales Order", dto.order_id)
        
        # Find product
        product = self._product_repository.find_by_id(dto.product_id)
        if not product:
            raise EntityNotFoundException("Product", dto.product_id)
        
        # Find current item in order
        current_item = sales_order._find_item_by_product(product)
        if not current_item:
            raise EntityNotFoundException("Order Item", f"Product {product.sku} in order {dto.order_id}")
        
        # Calculate stock adjustment
        current_quantity = current_item.quantity
        stock_adjustment = current_quantity - dto.new_quantity
        
        # Check stock availability if increasing quantity
        if dto.new_quantity > current_quantity:
            additional_quantity = dto.new_quantity - current_quantity
            if not product.is_available(additional_quantity):
                raise InsufficientStockException(
                    product.sku, 
                    additional_quantity, 
                    product.stock_quantity
                )
        
        # Update item quantity
        if dto.new_quantity <= 0:
            sales_order.remove_item(product)
        else:
            sales_order.update_item_quantity(product, dto.new_quantity)
        
        # Update product stock
        product.update_stock(stock_adjustment)
        self._product_repository.update(product)
        
        # Save updated order
        updated_order = self._sales_order_repository.update(sales_order)
        
        return self._map_to_response_dto(updated_order)
    
    def _map_to_response_dto(self, sales_order: SalesOrder) -> SalesOrderResponseDTO:
        """Map sales order entity to response DTO."""
        item_dtos = [
            self._map_item_to_response_dto(item) 
            for item in sales_order.items
        ]
        
        return SalesOrderResponseDTO(
            id=sales_order.id,
            company_id=sales_order.company.id,
            company_name=sales_order.company.name,
            company_document=sales_order.company.document.get_formatted(),
            items=item_dtos,
            total_items=sales_order.total_items,
            total_amount=sales_order.total_amount,
            formatted_total_amount=FormatUtils.format_currency(sales_order.total_amount),
            created_at=sales_order.created_at.isoformat(),
            updated_at=sales_order.updated_at.isoformat(),
            is_valid=sales_order.is_valid()
        )
    
    def _map_item_to_response_dto(self, item: SalesOrderItem) -> SalesOrderItemResponseDTO:
        """Map sales order item to response DTO."""
        return SalesOrderItemResponseDTO(
            id=item.id,
            product_id=item.product.id,
            product_sku=item.product.sku,
            product_name=item.product.name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            formatted_unit_price=FormatUtils.format_currency(item.unit_price),
            subtotal=item.subtotal,
            formatted_subtotal=FormatUtils.format_currency(item.subtotal)
        )


class GetSalesOrderUseCase:
    """Use case for retrieving a sales order."""
    
    def __init__(self, sales_order_repository: SalesOrderRepository):
        self._sales_order_repository = sales_order_repository
    
    def execute(self, order_id: str) -> SalesOrderResponseDTO:
        """Execute sales order retrieval."""
        sales_order = self._sales_order_repository.find_by_id(order_id)
        if not sales_order:
            raise EntityNotFoundException("Sales Order", order_id)
        
        return self._map_to_response_dto(sales_order)
    
    def _map_to_response_dto(self, sales_order: SalesOrder) -> SalesOrderResponseDTO:
        """Map sales order entity to response DTO."""
        item_dtos = [
            self._map_item_to_response_dto(item) 
            for item in sales_order.items
        ]
        
        return SalesOrderResponseDTO(
            id=sales_order.id,
            company_id=sales_order.company.id,
            company_name=sales_order.company.name,
            company_document=sales_order.company.document.get_formatted(),
            items=item_dtos,
            total_items=sales_order.total_items,
            total_amount=sales_order.total_amount,
            formatted_total_amount=FormatUtils.format_currency(sales_order.total_amount),
            created_at=sales_order.created_at.isoformat(),
            updated_at=sales_order.updated_at.isoformat(),
            is_valid=sales_order.is_valid()
        )
    
    def _map_item_to_response_dto(self, item: SalesOrderItem) -> SalesOrderItemResponseDTO:
        """Map sales order item to response DTO."""
        return SalesOrderItemResponseDTO(
            id=item.id,
            product_id=item.product.id,
            product_sku=item.product.sku,
            product_name=item.product.name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            formatted_unit_price=FormatUtils.format_currency(item.unit_price),
            subtotal=item.subtotal,
            formatted_subtotal=FormatUtils.format_currency(item.subtotal)
        )


class ListSalesOrdersUseCase:
    """Use case for listing all sales orders."""
    
    def __init__(self, sales_order_repository: SalesOrderRepository):
        self._sales_order_repository = sales_order_repository
    
    def execute(self) -> List[SalesOrderResponseDTO]:
        """Execute sales orders listing."""
        orders = self._sales_order_repository.find_all()
        return [self._map_to_response_dto(order) for order in orders]
    
    def _map_to_response_dto(self, sales_order: SalesOrder) -> SalesOrderResponseDTO:
        """Map sales order entity to response DTO."""
        item_dtos = [
            self._map_item_to_response_dto(item) 
            for item in sales_order.items
        ]
        
        return SalesOrderResponseDTO(
            id=sales_order.id,
            company_id=sales_order.company.id,
            company_name=sales_order.company.name,
            company_document=sales_order.company.document.get_formatted(),
            items=item_dtos,
            total_items=sales_order.total_items,
            total_amount=sales_order.total_amount,
            formatted_total_amount=FormatUtils.format_currency(sales_order.total_amount),
            created_at=sales_order.created_at.isoformat(),
            updated_at=sales_order.updated_at.isoformat(),
            is_valid=sales_order.is_valid()
        )
    
    def _map_item_to_response_dto(self, item: SalesOrderItem) -> SalesOrderItemResponseDTO:
        """Map sales order item to response DTO."""
        return SalesOrderItemResponseDTO(
            id=item.id,
            product_id=item.product.id,
            product_sku=item.product.sku,
            product_name=item.product.name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            formatted_unit_price=FormatUtils.format_currency(item.unit_price),
            subtotal=item.subtotal,
            formatted_subtotal=FormatUtils.format_currency(item.subtotal)
        )


class GenerateSalesOrderReportUseCase:
    """Use case for generating sales order report."""
    
    def __init__(self, 
                 sales_order_repository: SalesOrderRepository,
                 report_generation_service: ReportGenerationService):
        self._sales_order_repository = sales_order_repository
        self._report_generation_service = report_generation_service
    
    def execute(self, dto: GenerateReportDTO) -> str:
        """Execute report generation."""
        # Find sales order
        sales_order = self._sales_order_repository.find_by_id(dto.order_id)
        if not sales_order:
            raise EntityNotFoundException("Sales Order", dto.order_id)
        
        # Validate order before generating report
        if not sales_order.is_valid():
            raise ValidationException("Sales order must have at least 2 items to generate report")
        
        try:
            # Generate report
            report_path = self._report_generation_service.generate_sales_order_report(
                sales_order, 
                dto.custom_output_path
            )
            
            return report_path
            
        except Exception as e:
            raise ReportGenerationException(f"Failed to generate report: {str(e)}", dto.format_type)



class SalesOrderUseCases:
    """Aggregated sales order use cases for easy access."""
    
    def __init__(self, sales_order_repository, company_repository, product_repository, report_generation_service):
        """Initialize sales order use cases."""
        self.create = CreateSalesOrderUseCase(sales_order_repository, company_repository)
        self.add_item = AddItemToOrderUseCase(sales_order_repository, product_repository)
        self.update_item = UpdateOrderItemUseCase(sales_order_repository, product_repository)
        self.get = GetSalesOrderUseCase(sales_order_repository)
        self.list = ListSalesOrdersUseCase(sales_order_repository)
        self.generate_report = GenerateSalesOrderReportUseCase(sales_order_repository, report_generation_service)
