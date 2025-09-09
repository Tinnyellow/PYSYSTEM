"""
Dependency injection container for the Sales Management System.
"""

from typing import Optional

# Domain repositories
from ...domain.repositories.company_repository import CompanyRepository
from ...domain.repositories.product_repository import ProductRepository
from ...domain.repositories.sales_order_repository import SalesOrderRepository

# Domain services
from ...domain.services.address_lookup_service import AddressLookupService
from ...domain.services.excel_processing_service import ExcelProcessingService
from ...domain.services.report_generation_service import ReportGenerationService

# Infrastructure implementations
from ...infrastructure.persistence.json_company_repository import JsonCompanyRepository
from ...infrastructure.persistence.json_product_repository import JsonProductRepository
from ...infrastructure.persistence.json_sales_order_repository import JsonSalesOrderRepository
from ...infrastructure.external_services.brasil_api_address_service import BrasilApiAddressLookupService
from ...infrastructure.external_services.brasilapi_service import BrasilApiService
from ...infrastructure.file_processors.excel_processing_service import PandasExcelProcessingService
from ...infrastructure.report_generators.pdf_report_service import PdfReportGenerationService

# Application use cases
from ...application.use_cases.company_use_cases import CompanyUseCases
from ...application.use_cases.product_use_cases import ProductUseCases
from ...application.use_cases.sales_order_use_cases import SalesOrderUseCases

# Presentation controllers
from ...presentation.controllers.company_controller import CompanyController
from ...presentation.controllers.product_controller import ProductController
from ...presentation.controllers.sales_order_controller import SalesOrderController


class DependencyContainer:
    """Container for dependency injection."""
    
    def __init__(self):
        """Initialize dependency container."""
        self._company_repository: Optional[CompanyRepository] = None
        self._product_repository: Optional[ProductRepository] = None
        self._sales_order_repository: Optional[SalesOrderRepository] = None
        
        self._address_lookup_service: Optional[AddressLookupService] = None
        self._excel_processing_service: Optional[ExcelProcessingService] = None
        self._report_generation_service: Optional[ReportGenerationService] = None
        self._brasilapi_service: Optional[BrasilApiService] = None
        
        self._company_use_cases: Optional[CompanyUseCases] = None
        self._product_use_cases: Optional[ProductUseCases] = None
        self._sales_order_use_cases: Optional[SalesOrderUseCases] = None
        
        self._company_controller: Optional[CompanyController] = None
        self._product_controller: Optional[ProductController] = None
        self._sales_order_controller: Optional[SalesOrderController] = None
    
    # Repository factories
    def get_company_repository(self) -> CompanyRepository:
        """Get company repository instance."""
        if self._company_repository is None:
            self._company_repository = JsonCompanyRepository()
        return self._company_repository
    
    def get_product_repository(self) -> ProductRepository:
        """Get product repository instance."""
        if self._product_repository is None:
            self._product_repository = JsonProductRepository()
        return self._product_repository
    
    def get_sales_order_repository(self) -> SalesOrderRepository:
        """Get sales order repository instance."""
        if self._sales_order_repository is None:
            self._sales_order_repository = JsonSalesOrderRepository()
        return self._sales_order_repository
    
    # Service factories
    def get_address_lookup_service(self) -> AddressLookupService:
        """Get address lookup service instance."""
        if self._address_lookup_service is None:
            self._address_lookup_service = BrasilApiAddressLookupService()
        return self._address_lookup_service
    
    def get_excel_processing_service(self) -> ExcelProcessingService:
        """Get Excel processing service instance."""
        if self._excel_processing_service is None:
            self._excel_processing_service = PandasExcelProcessingService()
        return self._excel_processing_service
    
    def get_report_generation_service(self) -> ReportGenerationService:
        """Get report generation service instance."""
        if self._report_generation_service is None:
            self._report_generation_service = PdfReportGenerationService()
        return self._report_generation_service
    
    def get_brasilapi_service(self) -> BrasilApiService:
        """Get BrasilAPI service instance."""
        if self._brasilapi_service is None:
            self._brasilapi_service = BrasilApiService()
        return self._brasilapi_service
    
    # Use case factories
    def get_company_use_cases(self) -> CompanyUseCases:
        """Get company use cases instance."""
        if self._company_use_cases is None:
            self._company_use_cases = CompanyUseCases(
                company_repository=self.get_company_repository(),
                address_lookup_service=self.get_address_lookup_service()
            )
        return self._company_use_cases
    
    def get_product_use_cases(self) -> ProductUseCases:
        """Get product use cases instance."""
        if self._product_use_cases is None:
            self._product_use_cases = ProductUseCases(
                product_repository=self.get_product_repository(),
                excel_processing_service=self.get_excel_processing_service()
            )
        return self._product_use_cases
    
    def get_sales_order_use_cases(self) -> SalesOrderUseCases:
        """Get sales order use cases instance."""
        if self._sales_order_use_cases is None:
            self._sales_order_use_cases = SalesOrderUseCases(
                sales_order_repository=self.get_sales_order_repository(),
                company_repository=self.get_company_repository(),
                product_repository=self.get_product_repository(),
                report_generation_service=self.get_report_generation_service()
            )
        return self._sales_order_use_cases
    
    # Controller factories
    def get_company_controller(self) -> CompanyController:
        """Get company controller instance."""
        if self._company_controller is None:
            self._company_controller = CompanyController(
                company_use_cases=self.get_company_use_cases()
            )
        return self._company_controller
    
    def get_product_controller(self) -> ProductController:
        """Get product controller instance."""
        if self._product_controller is None:
            self._product_controller = ProductController(
                product_use_cases=self.get_product_use_cases()
            )
        return self._product_controller
    
    def get_sales_order_controller(self) -> SalesOrderController:
        """Get sales order controller instance."""
        if self._sales_order_controller is None:
            self._sales_order_controller = SalesOrderController(
                sales_order_use_cases=self.get_sales_order_use_cases()
            )
        return self._sales_order_controller
