"""
Product Enhancement Service using BrasilAPI integration.
"""

from typing import Dict, List, Optional, Any
from decimal import Decimal
import logging

from ..external_services.brasilapi_service import BrasilApiService


class ProductEnhancementService:
    """Service for enhancing product information using BrasilAPI data."""
    
    def __init__(self):
        """Initialize the product enhancement service."""
        self.brasil_api = BrasilApiService()
        self.logger = logging.getLogger(__name__)
    
    def suggest_ncm_codes(self, product_description: str, category: str = None) -> List[Dict[str, Any]]:
        """
        Suggest NCM codes based on product description and category.
        
        Args:
            product_description: Description of the product
            category: Optional category to refine search
            
        Returns:
            List of NCM suggestions with code and description
        """
        try:
            # Combine description and category for better search
            search_query = product_description
            if category:
                search_query = f"{category} {product_description}"
            
            # Search NCM codes
            ncm_results = self.brasil_api.search_ncm(search_query)
            
            # Format results
            suggestions = []
            for ncm in ncm_results[:10]:  # Limit to top 10 results
                suggestions.append({
                    'code': ncm.get('codigo', ''),
                    'description': ncm.get('descricao', ''),
                    'relevance_score': self._calculate_relevance_score(
                        product_description, 
                        ncm.get('descricao', '')
                    )
                })
            
            # Sort by relevance score
            suggestions.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            return suggestions
            
        except Exception as e:
            self.logger.error(f"Error suggesting NCM codes: {e}")
            return []
    
    def get_ncm_details(self, ncm_code: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about an NCM code.
        
        Args:
            ncm_code: The NCM code to look up
            
        Returns:
            Dictionary with NCM details or None if not found
        """
        try:
            return self.brasil_api.get_ncm_by_code(ncm_code)
        except Exception as e:
            self.logger.error(f"Error getting NCM details for {ncm_code}: {e}")
            return None
    
    def validate_isbn_product(self, isbn: str) -> Optional[Dict[str, Any]]:
        """
        Validate and get product information from ISBN for book products.
        
        Args:
            isbn: The ISBN to validate
            
        Returns:
            Dictionary with book information or None if not found
        """
        try:
            isbn_info = self.brasil_api.get_isbn_info(isbn)
            
            if isbn_info:
                return {
                    'title': isbn_info.get('title', ''),
                    'subtitle': isbn_info.get('subtitle', ''),
                    'authors': ', '.join(isbn_info.get('authors', [])),
                    'publisher': isbn_info.get('publisher', ''),
                    'year': isbn_info.get('year', ''),
                    'page_count': isbn_info.get('page_count', 0),
                    'suggested_price': self._parse_price(isbn_info.get('retail_price', '')),
                    'dimensions': isbn_info.get('dimensions', {}),
                    'subjects': isbn_info.get('subjects', []),
                    'synopsis': isbn_info.get('synopsis', '')
                }
            return None
            
        except Exception as e:
            self.logger.error(f"Error validating ISBN {isbn}: {e}")
            return None
    
    def suggest_product_categories(self, description: str, existing_categories: List[str] = None) -> List[str]:
        """
        Suggest product categories based on description and NCM classifications.
        
        Args:
            description: Product description
            existing_categories: List of existing categories in the system
            
        Returns:
            List of suggested categories
        """
        try:
            # Get NCM suggestions to infer categories
            ncm_suggestions = self.suggest_ncm_codes(description)
            
            categories = set()
            
            # Extract category keywords from NCM descriptions
            for ncm in ncm_suggestions[:5]:  # Top 5 most relevant
                ncm_desc = ncm.get('description', '').lower()
                
                # Map common NCM terms to business categories
                category_mappings = {
                    'alimento': 'Food & Beverages',
                    'bebida': 'Food & Beverages',
                    'textil': 'Textiles & Clothing',
                    'roupa': 'Textiles & Clothing',
                    'calçado': 'Footwear',
                    'eletronico': 'Electronics',
                    'informatica': 'IT & Computing',
                    'computador': 'IT & Computing',
                    'medicament': 'Pharmaceuticals',
                    'farmaco': 'Pharmaceuticals',
                    'mobiliario': 'Furniture',
                    'movel': 'Furniture',
                    'veiculo': 'Automotive',
                    'automovel': 'Automotive',
                    'ferramenta': 'Tools & Hardware',
                    'construção': 'Construction Materials',
                    'cosmetico': 'Cosmetics & Personal Care',
                    'beleza': 'Cosmetics & Personal Care',
                    'livro': 'Books & Publications',
                    'papel': 'Paper & Stationery',
                    'quimico': 'Chemicals',
                    'plastico': 'Plastic Products',
                    'metal': 'Metal Products'
                }
                
                for keyword, category in category_mappings.items():
                    if keyword in ncm_desc:
                        categories.add(category)
            
            # If no categories found, use generic classification
            if not categories:
                if any(word in description.lower() for word in ['book', 'livro', 'revista']):
                    categories.add('Books & Publications')
                elif any(word in description.lower() for word in ['electronic', 'eletronico', 'computer']):
                    categories.add('Electronics')
                elif any(word in description.lower() for word in ['food', 'alimento', 'comida']):
                    categories.add('Food & Beverages')
                else:
                    categories.add('General Products')
            
            return sorted(list(categories))
            
        except Exception as e:
            self.logger.error(f"Error suggesting categories: {e}")
            return ['General Products']
    
    def enhance_product_data(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance product data with additional information from BrasilAPI.
        
        Args:
            product_data: Original product data
            
        Returns:
            Enhanced product data with additional fields
        """
        enhanced_data = product_data.copy()
        
        try:
            description = product_data.get('description', '')
            category = product_data.get('category', '')
            
            # Add NCM suggestions
            if description:
                ncm_suggestions = self.suggest_ncm_codes(description, category)
                if ncm_suggestions:
                    enhanced_data['suggested_ncm'] = ncm_suggestions[0]['code']
                    enhanced_data['ncm_description'] = ncm_suggestions[0]['description']
            
            # Add category suggestions if not provided
            if not category and description:
                category_suggestions = self.suggest_product_categories(description)
                if category_suggestions:
                    enhanced_data['suggested_category'] = category_suggestions[0]
                    enhanced_data['all_suggested_categories'] = category_suggestions
            
            # If barcode looks like ISBN, try to get book info
            barcode = product_data.get('barcode', '')
            if barcode and (len(barcode) in [10, 13]) and barcode.isdigit():
                isbn_info = self.validate_isbn_product(barcode)
                if isbn_info:
                    enhanced_data['isbn_info'] = isbn_info
                    if not enhanced_data.get('name'):
                        enhanced_data['suggested_name'] = isbn_info['title']
                    if not enhanced_data.get('category'):
                        enhanced_data['suggested_category'] = 'Books & Publications'
            
            return enhanced_data
            
        except Exception as e:
            self.logger.error(f"Error enhancing product data: {e}")
            return enhanced_data
    
    def _calculate_relevance_score(self, search_term: str, ncm_description: str) -> float:
        """Calculate relevance score between search term and NCM description."""
        try:
            search_words = set(search_term.lower().split())
            ncm_words = set(ncm_description.lower().split())
            
            if not search_words or not ncm_words:
                return 0.0
            
            # Calculate Jaccard similarity
            intersection = search_words.intersection(ncm_words)
            union = search_words.union(ncm_words)
            
            return len(intersection) / len(union) if union else 0.0
            
        except Exception:
            return 0.0
    
    def _parse_price(self, price_str: str) -> Optional[Decimal]:
        """Parse price string to Decimal."""
        try:
            if not price_str:
                return None
            
            # Remove currency symbols and spaces
            clean_price = price_str.replace('R$', '').replace('$', '').replace(' ', '').replace(',', '.')
            
            # Extract numeric value
            import re
            match = re.search(r'\d+(?:\.\d{2})?', clean_price)
            if match:
                return Decimal(match.group())
            
            return None
            
        except Exception:
            return None
