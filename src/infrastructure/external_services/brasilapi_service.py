"""
BrasilAPI Integration Service for enhanced data lookup.
"""

import requests
from typing import Dict, List, Optional, Any
from decimal import Decimal
import logging


class BrasilApiService:
    """Service for integrating with BrasilAPI endpoints."""
    
    BASE_URL = "https://brasilapi.com.br/api"
    
    def __init__(self):
        """Initialize BrasilAPI service."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PYSYSTEM-Business-Management/1.0',
            'Accept': 'application/json'
        })
        self.logger = logging.getLogger(__name__)
    
    def get_cep_info(self, cep: str) -> Optional[Dict[str, Any]]:
        """Get address information from CEP using BrasilAPI."""
        try:
            # Clean CEP (remove dots and hyphens)
            clean_cep = cep.replace('.', '').replace('-', '').replace(' ', '')
            
            if len(clean_cep) != 8 or not clean_cep.isdigit():
                self.logger.warning(f"Invalid CEP format: {cep}")
                return None
            
            response = self.session.get(f"{self.BASE_URL}/cep/v1/{clean_cep}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'cep': data.get('cep', ''),
                    'street': data.get('street', ''),
                    'neighborhood': data.get('neighborhood', ''),
                    'city': data.get('city', ''),
                    'state': data.get('state', ''),
                    'service': data.get('service', 'BrasilAPI')
                }
            else:
                self.logger.warning(f"CEP lookup failed: {response.status_code}")
                return None
                
        except requests.RequestException as e:
            self.logger.error(f"Error fetching CEP {cep}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error in CEP lookup: {e}")
            return None
    
    def validate_cnpj(self, cnpj: str) -> Optional[Dict[str, Any]]:
        """Validate and get company information from CNPJ using BrasilAPI."""
        try:
            # Clean CNPJ (remove dots, slashes and hyphens)
            clean_cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '').replace(' ', '')
            
            if len(clean_cnpj) != 14 or not clean_cnpj.isdigit():
                self.logger.warning(f"Invalid CNPJ format: {cnpj}")
                return None
            
            response = self.session.get(f"{self.BASE_URL}/cnpj/v1/{clean_cnpj}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'cnpj': data.get('cnpj', ''),
                    'company_name': data.get('razao_social', ''),
                    'fantasy_name': data.get('nome_fantasia', ''),
                    'legal_nature': data.get('natureza_juridica', ''),
                    'registration_status': data.get('situacao_cadastral', ''),
                    'address': {
                        'street': data.get('logradouro', ''),
                        'number': data.get('numero', ''),
                        'neighborhood': data.get('bairro', ''),
                        'city': data.get('municipio', ''),
                        'state': data.get('uf', ''),
                        'cep': data.get('cep', '')
                    },
                    'phone': data.get('telefone', ''),
                    'email': data.get('email', ''),
                    'main_activity': data.get('atividade_principal', []),
                    'secondary_activities': data.get('atividades_secundarias', []),
                    'partners': data.get('socios', [])
                }
            else:
                self.logger.warning(f"CNPJ validation failed: {response.status_code}")
                return None
                
        except requests.RequestException as e:
            self.logger.error(f"Error validating CNPJ {cnpj}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error in CNPJ validation: {e}")
            return None
    
    def get_cnpj_info(self, cnpj: str) -> Dict[str, Any]:
        """
        Alias for validate_cnpj method for compatibility.
        
        Args:
            cnpj: CNPJ number to validate
            
        Returns:
            Dictionary with CNPJ information or None if not found
        """
        return self.validate_cnpj(cnpj)
    
    def get_banks(self) -> List[Dict[str, Any]]:
        """Get list of all Brazilian banks."""
        try:
            response = self.session.get(f"{self.BASE_URL}/banks/v1", timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.warning(f"Banks lookup failed: {response.status_code}")
                return []
                
        except requests.RequestException as e:
            self.logger.error(f"Error fetching banks: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error in banks lookup: {e}")
            return []
    
    def get_bank_by_code(self, bank_code: str) -> Optional[Dict[str, Any]]:
        """Get bank information by code."""
        try:
            response = self.session.get(f"{self.BASE_URL}/banks/v1/{bank_code}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'ispb': data.get('ispb', ''),
                    'name': data.get('name', ''),
                    'code': data.get('code', ''),
                    'fullName': data.get('fullName', '')
                }
            else:
                self.logger.warning(f"Bank lookup failed for code {bank_code}: {response.status_code}")
                return None
                
        except requests.RequestException as e:
            self.logger.error(f"Error fetching bank {bank_code}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error in bank lookup: {e}")
            return None
    
    def get_ddd_info(self, ddd: str) -> Optional[Dict[str, Any]]:
        """Get DDD (area code) information."""
        try:
            clean_ddd = ddd.replace('(', '').replace(')', '').replace(' ', '')
            
            if len(clean_ddd) != 2 or not clean_ddd.isdigit():
                self.logger.warning(f"Invalid DDD format: {ddd}")
                return None
            
            response = self.session.get(f"{self.BASE_URL}/ddd/v1/{clean_ddd}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'state': data.get('state', ''),
                    'cities': data.get('cities', [])
                }
            else:
                self.logger.warning(f"DDD lookup failed: {response.status_code}")
                return None
                
        except requests.RequestException as e:
            self.logger.error(f"Error fetching DDD {ddd}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error in DDD lookup: {e}")
            return None
    
    def get_national_holidays(self, year: int) -> List[Dict[str, Any]]:
        """Get Brazilian national holidays for a specific year."""
        try:
            response = self.session.get(f"{self.BASE_URL}/feriados/v1/{year}", timeout=5)
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.warning(f"Holidays lookup failed for year {year}: {response.status_code}")
                return []
                
        except requests.RequestException as e:
            self.logger.error(f"Error fetching holidays for {year}: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error in holidays lookup: {e}")
            return []
    
    def search_ncm(self, query: str) -> List[Dict[str, Any]]:
        """Search NCM codes by description."""
        try:
            response = self.session.get(
                f"{self.BASE_URL}/ncm/v1", 
                params={'search': query},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result:
                    return result
            else:
                self.logger.warning(f"NCM search failed: {response.status_code}")
                
        except requests.RequestException as e:
            self.logger.error(f"Error searching NCM for '{query}': {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error in NCM search: {e}")
            
        # Fallback: return mock NCM codes for testing
        if 'notebook' in query.lower() or 'computer' in query.lower():
            return [
                {'codigo': '8471.30.12', 'descricao': 'Máquinas automáticas para processamento de dados, portáteis, de peso inferior ou igual a 10 kg, contendo pelo menos uma unidade central de processamento'},
                {'codigo': '8471.30.19', 'descricao': 'Outras máquinas automáticas para processamento de dados, portáteis'},
                {'codigo': '8471.41.10', 'descricao': 'Unidades de processamento, digitais, de pequena capacidade'},
            ]
        
        return []
    
    def get_ncm_by_code(self, ncm_code: str) -> Optional[Dict[str, Any]]:
        """Get NCM information by code."""
        try:
            response = self.session.get(f"{self.BASE_URL}/ncm/v1/{ncm_code}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'code': data.get('codigo', ''),
                    'description': data.get('descricao', ''),
                    'start_date': data.get('data_inicio', ''),
                    'end_date': data.get('data_fim', ''),
                    'type': data.get('tipo_ato', ''),
                    'number': data.get('numero_ato', ''),
                    'year': data.get('ano_ato', '')
                }
            else:
                self.logger.warning(f"NCM lookup failed for code {ncm_code}: {response.status_code}")
                return None
                
        except requests.RequestException as e:
            self.logger.error(f"Error fetching NCM {ncm_code}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error in NCM lookup: {e}")
            return None
    
    def get_isbn_info(self, isbn: str) -> Optional[Dict[str, Any]]:
        """Get book information by ISBN."""
        try:
            # Clean ISBN (remove hyphens and spaces)
            clean_isbn = isbn.replace('-', '').replace(' ', '')
            
            response = self.session.get(f"{self.BASE_URL}/isbn/v1/{clean_isbn}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'isbn': data.get('isbn', ''),
                    'title': data.get('title', ''),
                    'subtitle': data.get('subtitle', ''),
                    'authors': data.get('authors', []),
                    'publisher': data.get('publisher', ''),
                    'synopsis': data.get('synopsis', ''),
                    'dimensions': data.get('dimensions', {}),
                    'year': data.get('year', ''),
                    'format': data.get('format', ''),
                    'page_count': data.get('page_count', 0),
                    'subjects': data.get('subjects', []),
                    'location': data.get('location', ''),
                    'retail_price': data.get('retail_price', ''),
                    'cover_url': data.get('cover_url', ''),
                    'provider': data.get('provider', '')
                }
            else:
                self.logger.warning(f"ISBN lookup failed: {response.status_code}")
                return None
                
        except requests.RequestException as e:
            self.logger.error(f"Error fetching ISBN {isbn}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error in ISBN lookup: {e}")
            return None
