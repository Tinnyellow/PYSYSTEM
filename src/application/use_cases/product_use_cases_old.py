"""
Product use cases for the Sales Management System.
"""

from decimal import Decimal
from typing import List, Optional

from ..dtos.product_dto import CreateProductDTO, UpdateProductDTO, ProductResponseDTO, ExcelImportResultDTO
from ...domain.entities.product import Product
from ...domain.repositories.product_repository import ProductRepository
from ...domain.services.excel_processing_service import ExcelProcessingService
from ...shared.exceptions.exceptions import DuplicateSkuException, EntityNotFoundException
from ...shared.utils.format_utils import FormatUtils


def _map_product_to_response_dto(product: Product) -> ProductResponseDTO:
    """Map product entity to response DTO (global helper function)."""
    return ProductResponseDTO(
        id=product.id,
        sku=product.sku,
        name=product.name,
        unit_price=product.unit_price,
        formatted_price=FormatUtils.format_currency(product.unit_price),
        unit=product.unit,
        stock_quantity=product.stock_quantity,
        display_name=product.get_display_name(),
        price=product.unit_price,  # Alias for compatibility
        description=getattr(product, 'description', None),
        category=getattr(product, 'category', None),
        barcode=getattr(product, 'barcode', None)
    )


class CreateProductUseCase:
    """Use case for creating a new product."""

    def __init__(self, product_repository: ProductRepository):
        """Initialize use case with product repository."""
        self._product_repository = product_repository

    def execute(self, dto: CreateProductDTO) -> ProductResponseDTO:
        """Create a new product."""
        # Check for duplicate SKU
        if self._product_repository.find_by_sku(dto.sku):
            raise DuplicateSkuException(dto.sku)

        # Create product entity
        product = Product(
            sku=dto.sku,
            name=dto.name,
            unit_price=dto.unit_price,
            unit=dto.unit,
            stock_quantity=dto.stock_quantity,
            description=dto.description,
            category=dto.category,
            barcode=dto.barcode
        )
        
        # Save product
        saved_product = self._product_repository.save(product)
        
        return _map_product_to_response_dto(saved_product)

from typing import List
from ..dtos.product_dto import (
    CreateProductDTO,
    UpdateProductDTO,
    ProductResponseDTO, 
    ExcelImportResultDTO, 
    ProductSearchResultDTO
)
from ...domain.entities.product import Product
from ...domain.repositories.product_repository import ProductRepository
from ...domain.services.excel_processing_service import ExcelProcessingService
from ...shared.exceptions.exceptions import (
    EntityNotFoundException, 
    ExcelProcessingException,
    ValidationException
)
from ...shared.utils.format_utils import FormatUtils


class CreateProductUseCase:
    """Use case for creating a new product."""
    
    def __init__(self, product_repository: ProductRepository):
        self._product_repository = product_repository
    
    def execute(self, dto: CreateProductDTO) -> ProductResponseDTO:
        """Execute product creation."""
        # Create product entity
        product = Product(
            sku=dto.sku,
            name=dto.name,
            unit_price=dto.unit_price,
            unit=dto.unit,
            stock_quantity=dto.stock_quantity
        )
        
        # Save product
        saved_product = self._product_repository.save(product)
        
        return self._map_to_response_dto(saved_product)
    
    def _map_to_response_dto(self, product: Product) -> ProductResponseDTO:
        """Map product entity to response DTO."""
        return ProductResponseDTO(
            id=product.id,
            sku=product.sku,
            name=product.name,
            unit_price=product.unit_price,
            formatted_price=FormatUtils.format_currency(product.unit_price),
            unit=product.unit,
            stock_quantity=product.stock_quantity,
            display_name=product.get_display_name(),
            price=product.unit_price,  # Alias for compatibility
            description=getattr(product, 'description', None),
            category=getattr(product, 'category', None),
            barcode=getattr(product, 'barcode', None)
        )


class ImportProductsFromExcelUseCase:
    """Use case for importing products from Excel file."""
    
    def __init__(self, 
                 product_repository: ProductRepository,
                 excel_processing_service: ExcelProcessingService):
        self._product_repository = product_repository
        self._excel_processing_service = excel_processing_service
    
    def execute(self, file_path: str) -> ExcelImportResultDTO:
        """Execute Excel import."""
        errors = []
        imported_products = []
        
        try:
            # Validate Excel structure first
            if not self._excel_processing_service.validate_excel_structure(file_path):
                required_columns = self._excel_processing_service.get_required_columns()
                raise ExcelProcessingException(
                    f"Invalid Excel structure. Required columns: {', '.join(required_columns)}",
                    file_path
                )
            
            # Read products from Excel
            products = self._excel_processing_service.read_products_from_excel(file_path)
            
            if not products:
                return ExcelImportResultDTO(
                    success=False,
                    imported_count=0,
                    failed_count=0,
                    products=[],
                    errors=["No valid products found in the Excel file"],
                    file_path=file_path
                )
            
            # Clear existing products before import
            self._product_repository.clear_all()
            
            # Save products in batch
            try:
                saved_products = self._product_repository.save_batch(products)
                imported_products = [
                    self._map_to_response_dto(product) 
                    for product in saved_products
                ]
                
                return ExcelImportResultDTO(
                    success=True,
                    imported_count=len(saved_products),
                    failed_count=0,
                    products=imported_products,
                    errors=[],
                    file_path=file_path
                )
                
            except Exception as e:
                errors.append(f"Failed to save products: {str(e)}")
                
        except ExcelProcessingException:
            raise
        except Exception as e:
            errors.append(f"Failed to process Excel file: {str(e)}")
        
        return ExcelImportResultDTO(
            success=False,
            imported_count=0,
            failed_count=len(errors),
            products=[],
            errors=errors,
            file_path=file_path
        )
    
    def _map_to_response_dto(self, product: Product) -> ProductResponseDTO:
        """Map product entity to response DTO."""
        return ProductResponseDTO(
            id=product.id,
            sku=product.sku,
            name=product.name,
            unit_price=product.unit_price,
            formatted_price=FormatUtils.format_currency(product.unit_price),
            unit=product.unit,
            stock_quantity=product.stock_quantity,
            display_name=product.get_display_name()
        )


class ListProductsUseCase:
    """Use case for listing all products."""
    
    def __init__(self, product_repository: ProductRepository):
        self._product_repository = product_repository
    
    def execute(self) -> List[ProductResponseDTO]:
        """Execute products listing."""
        products = self._product_repository.find_all()
        return [self._map_to_response_dto(product) for product in products]
    
    def _map_to_response_dto(self, product: Product) -> ProductResponseDTO:
        """Map product entity to response DTO."""
        return ProductResponseDTO(
            id=product.id,
            sku=product.sku,
            name=product.name,
            unit_price=product.unit_price,
            formatted_price=FormatUtils.format_currency(product.unit_price),
            unit=product.unit,
            stock_quantity=product.stock_quantity,
            display_name=product.get_display_name()
        )


class SearchProductsUseCase:
    """Use case for searching products."""
    
    def __init__(self, product_repository: ProductRepository):
        self._product_repository = product_repository
    
    def execute(self, query: str) -> ProductSearchResultDTO:
        """Execute product search."""
        products = self._product_repository.search(query)
        
        product_dtos = [self._map_to_response_dto(product) for product in products]
        
        return ProductSearchResultDTO(
            products=product_dtos,
            total_count=len(product_dtos),
            query=query
        )
    
    def _map_to_response_dto(self, product: Product) -> ProductResponseDTO:
        """Map product entity to response DTO."""
        return ProductResponseDTO(
            id=product.id,
            sku=product.sku,
            name=product.name,
            unit_price=product.unit_price,
            formatted_price=FormatUtils.format_currency(product.unit_price),
            unit=product.unit,
            stock_quantity=product.stock_quantity,
            display_name=product.get_display_name()
        )


class GetProductUseCase:
    """Use case for retrieving a single product."""
    
    def __init__(self, product_repository: ProductRepository):
        self._product_repository = product_repository
    
    def execute(self, product_id: str) -> ProductResponseDTO:
        """Execute product retrieval."""
        product = self._product_repository.find_by_id(product_id)
        if not product:
            raise EntityNotFoundException("Product", product_id)
        
        return self._map_to_response_dto(product)
    
    def _map_to_response_dto(self, product: Product) -> ProductResponseDTO:
        """Map product entity to response DTO."""
        return ProductResponseDTO(
            id=product.id,
            sku=product.sku,
            name=product.name,
            unit_price=product.unit_price,
            formatted_price=FormatUtils.format_currency(product.unit_price),
            unit=product.unit,
            stock_quantity=product.stock_quantity,
            display_name=product.get_display_name()
        )


class GetAvailableProductsUseCase:
    """Use case for retrieving products with available stock."""
    
    def __init__(self, product_repository: ProductRepository):
        self._product_repository = product_repository
    
    def execute(self) -> List[ProductResponseDTO]:
        """Execute available products retrieval."""
        products = self._product_repository.find_available_products()
        return [self._map_to_response_dto(product) for product in products]
    
    def _map_to_response_dto(self, product: Product) -> ProductResponseDTO:
        """Map product entity to response DTO."""
        return ProductResponseDTO(
            id=product.id,
            sku=product.sku,
            name=product.name,
            unit_price=product.unit_price,
            formatted_price=FormatUtils.format_currency(product.unit_price),
            unit=product.unit,
            stock_quantity=product.stock_quantity,
            display_name=product.get_display_name()
        )



class ProductUseCases:
    """Aggregated product use cases for easy access."""
    
    def __init__(self, product_repository, excel_processing_service):
        """Initialize product use cases."""
        self.create = CreateProductUseCase(product_repository)
        self.import_from_excel = ImportProductsFromExcelUseCase(product_repository, excel_processing_service)
        self.list = ListProductsUseCase(product_repository)
        self.search = SearchProductsUseCase(product_repository)
        self.get = GetProductUseCase(product_repository)
        self.get_available = GetAvailableProductsUseCase(product_repository)
