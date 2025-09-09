"""
Product use cases for the Sales Management System.
"""

from decimal import Decimal
from typing import List, Optional

from ..dtos.product_dto import CreateProductDTO, UpdateProductDTO, ProductResponseDTO, ExcelImportResultDTO, ProductSearchResultDTO
from ...domain.entities.product import Product
from ...domain.repositories.product_repository import ProductRepository
from ...domain.services.excel_processing_service import ExcelProcessingService
from ...shared.exceptions.exceptions import DuplicateSkuException, EntityNotFoundException, ExcelProcessingException, ValidationException
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


class ImportProductsFromExcelUseCase:
    """Use case for importing products from Excel file."""
    
    def __init__(self, product_repository: ProductRepository, excel_processing_service: ExcelProcessingService):
        """Initialize use case with repositories and services."""
        self._product_repository = product_repository
        self._excel_processing_service = excel_processing_service
    
    def execute(self, file_path: str) -> ExcelImportResultDTO:
        """Import products from Excel file."""
        try:
            # Process Excel file
            product_data = self._excel_processing_service.read_products_from_excel(file_path)
            
            if not product_data:
                return ExcelImportResultDTO(
                    success=False,
                    imported_count=0,
                    failed_count=0,
                    products=[],
                    errors=["No product data found in file"],
                    file_path=file_path
                )
            
            imported_products = []
            errors = []
            
            # Process each product (product_data is already a list of Product entities)
            for index, product in enumerate(product_data):
                try:
                    # Check for duplicate SKU
                    if self._product_repository.find_by_sku(product.sku):
                        errors.append(f"Row {index + 1}: SKU '{product.sku}' already exists")
                        continue
                    
                    # Save product (product is already a Product entity)
                    saved_product = self._product_repository.save(product)
                    imported_products.append(_map_product_to_response_dto(saved_product))
                    
                except Exception as e:
                    errors.append(f"Row {index + 1}: {str(e)}")
            
            return ExcelImportResultDTO(
                success=len(imported_products) > 0,
                imported_count=len(imported_products),
                failed_count=len(errors),
                products=imported_products,
                errors=errors,
                file_path=file_path
            )
            
        except ExcelProcessingException as e:
            return ExcelImportResultDTO(
                success=False,
                imported_count=0,
                failed_count=0,
                products=[],
                errors=[str(e)],
                file_path=file_path
            )
        except Exception as e:
            return ExcelImportResultDTO(
                success=False,
                imported_count=0,
                failed_count=len(product_data) if 'product_data' in locals() else 1,
                products=[],
                errors=[f"Unexpected error: {str(e)}"],
                file_path=file_path
            )


class UpdateProductUseCase:
    """Use case for updating an existing product."""
    
    def __init__(self, product_repository: ProductRepository):
        """Initialize use case with product repository."""
        self._product_repository = product_repository
    
    def execute(self, product_id: str, dto: UpdateProductDTO) -> ProductResponseDTO:
        """Update an existing product."""
        # Find existing product
        product = self._product_repository.find_by_id(product_id)
        if not product:
            raise EntityNotFoundException("Product", product_id)
        
        # Check for SKU conflicts if SKU is being changed
        if dto.sku and dto.sku != product.sku:
            existing_product = self._product_repository.find_by_sku(dto.sku)
            if existing_product and existing_product.id != product_id:
                raise DuplicateSkuException(dto.sku)
        
        # Update product fields
        if dto.sku is not None:
            product.sku = dto.sku
        if dto.name is not None:
            product.name = dto.name
        if dto.unit_price is not None:
            product.unit_price = dto.unit_price
        if dto.unit is not None:
            product.unit = dto.unit
        if dto.stock_quantity is not None:
            product.stock_quantity = dto.stock_quantity
        if dto.description is not None:
            product.description = dto.description
        if dto.category is not None:
            product.category = dto.category
        if dto.barcode is not None:
            product.barcode = dto.barcode
        
        # Save updated product
        updated_product = self._product_repository.save(product)
        
        return _map_product_to_response_dto(updated_product)


class DeleteProductUseCase:
    """Use case for deleting a product."""
    
    def __init__(self, product_repository: ProductRepository):
        """Initialize use case with product repository."""
        self._product_repository = product_repository
    
    def execute(self, product_id: str) -> bool:
        """Delete a product."""
        if not self._product_repository.exists(product_id):
            raise EntityNotFoundException("Product", product_id)
        
        return self._product_repository.delete(product_id)


class GetProductUseCase:
    """Use case for getting a single product."""
    
    def __init__(self, product_repository: ProductRepository):
        """Initialize use case with product repository."""
        self._product_repository = product_repository
    
    def execute(self, product_id: str) -> ProductResponseDTO:
        """Get a product by ID."""
        product = self._product_repository.find_by_id(product_id)
        if not product:
            raise EntityNotFoundException("Product", product_id)
        
        return _map_product_to_response_dto(product)


class ListProductsUseCase:
    """Use case for listing all products."""
    
    def __init__(self, product_repository: ProductRepository):
        """Initialize use case with product repository."""
        self._product_repository = product_repository
    
    def execute(self) -> List[ProductResponseDTO]:
        """List all products."""
        products = self._product_repository.find_all()
        return [_map_product_to_response_dto(product) for product in products]


class SearchProductsUseCase:
    """Use case for searching products."""
    
    def __init__(self, product_repository: ProductRepository):
        """Initialize use case with product repository."""
        self._product_repository = product_repository
    
    def execute(self, query: str) -> ProductSearchResultDTO:
        """Search products by query."""
        products = self._product_repository.search(query)
        
        return ProductSearchResultDTO(
            products=[_map_product_to_response_dto(product) for product in products],
            total_count=len(products),
            query=query
        )


class ProductUseCases:
    """Aggregated product use cases for easy access."""
    
    def __init__(self, product_repository, excel_processing_service):
        """Initialize product use cases."""
        self._product_repository = product_repository
        self.create = CreateProductUseCase(product_repository)
        self.import_from_excel = ImportProductsFromExcelUseCase(product_repository, excel_processing_service)
        self.update = UpdateProductUseCase(product_repository)
        self.delete = DeleteProductUseCase(product_repository)
        self.get = GetProductUseCase(product_repository)
        self.list = ListProductsUseCase(product_repository)
        self.search = SearchProductsUseCase(product_repository)
    
    def get_available(self) -> List[Product]:
        """Get all products with stock available."""
        try:
            all_products = self._product_repository.get_all()
            return [product for product in all_products if product.stock_quantity > 0]
        except Exception as e:
            print(f"Error getting available products: {e}")
            return []
    
    def update_stock(self, product_id: str, new_stock: int) -> bool:
        """Update product stock quantity."""
        try:
            if new_stock < 0:
                raise ValueError("Stock quantity cannot be negative")
            
            product = self._product_repository.get_by_id(product_id)
            if not product:
                return False
            
            product.stock_quantity = new_stock
            updated_product = self._product_repository.update(product)
            return updated_product is not None
        except Exception as e:
            print(f"Error updating stock: {e}")
            return False
    
    def search_products(self, search_term: str) -> List[Product]:
        """Search products by term."""
        try:
            all_products = self._product_repository.get_all()
            search_term = search_term.lower()
            return [
                product for product in all_products
                if (search_term in product.name.lower() or 
                    search_term in product.sku.lower() or
                    (product.description and search_term in product.description.lower()))
            ]
        except Exception as e:
            print(f"Error searching products: {e}")
            return []
    
    def get_by_sku(self, sku: str) -> Optional[Product]:
        """Get product by SKU."""
        try:
            return self._product_repository.find_by_sku(sku)
        except Exception as e:
            print(f"Error getting product by SKU: {e}")
            return None
