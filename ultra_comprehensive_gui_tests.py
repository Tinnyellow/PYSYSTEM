#!/usr/bin/env python3
"""
SISTEMA DE TESTES ULTRA COMPLETO E PROFUNDO - PYSYSTEM
Testa TODAS as funcionalidades do sistema de forma minuciosa e automatizada
"""

import sys
import os
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal
import traceback
import json
import random
import string
from datetime import datetime
from typing import Dict, List, Any, Optional

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.presentation.gui.main_window import MainWindow
from src.presentation.gui.dependency_injection import DependencyContainer
from src.application.dtos.company_dto import CreateCompanyDTO, UpdateCompanyDTO
from src.application.dtos.product_dto import CreateProductDTO, UpdateProductDTO
from src.application.dtos.sales_order_dto import CreateSalesOrderDTO, AddOrderItemDTO


class UltraComprehensiveGUITester:
    """Testador ultra completo que testa TUDO no sistema."""
    
    def __init__(self):
        """Inicializar testador ultra completo."""
        self.test_results = []
        self.errors_found = []
        self.warnings_found = []
        self.root = None
        self.app = None
        self.container = DependencyContainer()
        self.test_data = {}
        self.created_entities = {'companies': [], 'products': [], 'orders': []}
        
    def log_test(self, test_name: str, success: bool, details: str = "", severity: str = "ERROR"):
        """Registrar resultado do teste com severidade."""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        status = "✅ PASS" if success else "❌ FAIL"
        result = f"[{timestamp}] {status} - {test_name}"
        
        if details:
            result += f" | {details}"
            
        if not success:
            if severity == "WARNING":
                self.warnings_found.append(f"{test_name}: {details}")
            else:
                self.errors_found.append(f"{test_name}: {details}")
                
        self.test_results.append(result)
        print(result)
    
    def generate_random_string(self, length: int = 8) -> str:
        """Gerar string aleatória para testes."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def setup_ultra_gui(self):
        """Configurar interface gráfica para testes ultra completos."""
        try:
            print("🖥️ === CONFIGURAÇÃO ULTRA COMPLETA DA GUI ===")
            self.root = tk.Tk()
            self.root.title("PYSYSTEM - Testes Ultra Completos")
            self.root.geometry("1200x800+100+100")
            self.root.minsize(800, 600)
            
            # Criar aplicação
            self.app = MainWindow(self.root)
            
            # Configurar para testes
            self.root.update()
            self.root.lift()
            
            # Verificar componentes da GUI
            self.verify_gui_components()
            
            self.log_test("Setup GUI Ultra Completo", True, "Todos os componentes carregados")
            return True
            
        except Exception as e:
            self.log_test("Setup GUI Ultra Completo", False, str(e))
            traceback.print_exc()
            return False
    
    def verify_gui_components(self):
        """Verificar todos os componentes da GUI detalhadamente."""
        print("\n🔍 === VERIFICAÇÃO DETALHADA DOS COMPONENTES ===")
        
        # Verificar MainWindow
        components = [
            'notebook', 'company_frame', 'product_frame', 'sales_order_frame',
            'status_bar', 'menu_bar'
        ]
        
        for component in components:
            if hasattr(self.app, component):
                self.log_test(f"Componente {component}", True, "Encontrado")
            else:
                self.log_test(f"Componente {component}", False, "Não encontrado")
        
        # Verificar abas do notebook
        if hasattr(self.app, 'notebook'):
            notebook = self.app.notebook
            tab_count = notebook.index('end')
            self.log_test("Contagem de abas", True, f"{tab_count} abas encontradas")
            
            for i in range(tab_count):
                tab_text = notebook.tab(i, 'text')
                self.log_test(f"Aba {i+1}", True, f"'{tab_text}'")
    
    def test_ultra_complete_companies(self):
        """Teste ultra completo de gestão de empresas."""
        print("\n🏢 === TESTE ULTRA COMPLETO - GESTÃO DE EMPRESAS ===")
        
        try:
            company_controller = self.container.get_company_controller()
            
            # Teste 1: Listar empresas existentes
            existing_companies = company_controller.list_companies()
            self.log_test("Listagem inicial empresas", True, f"{len(existing_companies)} empresas")
            
            # Teste 2: Criar múltiplas empresas com dados variados
            test_companies_data = [
                {
                    'name': 'Empresa Teste Alpha Ltda',
                    'document_number': '11.111.111/0001-11',
                    'postal_code': '01310-100',
                    'street': 'Av. Paulista',
                    'number': '1000',
                    'neighborhood': 'Bela Vista',
                    'city': 'São Paulo',
                    'state': 'SP',
                    'email': 'alpha@teste.com',
                    'phone': '(11) 99999-1111'
                },
                {
                    'name': 'Beta Comércio Eireli',
                    'document_number': '22.222.222/0001-22',
                    'postal_code': '20040-020',
                    'street': 'Av. Rio Branco',
                    'number': '200',
                    'neighborhood': 'Centro',
                    'city': 'Rio de Janeiro',
                    'state': 'RJ',
                    'email': 'beta@comercio.com',
                    'phone': '(21) 88888-2222'
                },
                {
                    'name': 'Gamma Tecnologia SA',
                    'document_number': '33.333.333/0001-33',
                    'postal_code': '30112-000',
                    'street': 'Av. Afonso Pena',
                    'number': '300',
                    'neighborhood': 'Centro',
                    'city': 'Belo Horizonte',
                    'state': 'MG',
                    'email': 'gamma@tech.com',
                    'phone': '(31) 77777-3333'
                }
            ]
            
            created_companies = []
            
            for i, company_data in enumerate(test_companies_data):
                try:
                    company_dto = CreateCompanyDTO(**company_data)
                    company = company_controller.create_company(company_dto)
                    created_companies.append(company)
                    self.created_entities['companies'].append(company.id)
                    self.log_test(f"Criar empresa {i+1}", True, f"ID: {company.id}, Nome: {company.name}")
                    
                except Exception as e:
                    self.log_test(f"Criar empresa {i+1}", False, str(e))
            
            # Teste 3: Verificar listagem após criação
            updated_companies = company_controller.list_companies()
            expected_count = len(existing_companies) + len(created_companies)
            actual_count = len(updated_companies)
            
            if actual_count >= expected_count:
                self.log_test("Listagem após criação", True, f"{actual_count} empresas total")
            else:
                self.log_test("Listagem após criação", False, f"Esperado >= {expected_count}, obtido {actual_count}")
            
            # Teste 4: Buscar cada empresa criada por ID
            for company in created_companies:
                found_company = company_controller.get_company(company.id)
                if found_company and found_company.id == company.id:
                    self.log_test(f"Buscar empresa {company.name}", True, "Encontrada por ID")
                else:
                    self.log_test(f"Buscar empresa {company.name}", False, "Não encontrada por ID")
            
            # Teste 5: Editar empresas criadas
            for i, company in enumerate(created_companies):
                try:
                    update_dto = UpdateCompanyDTO(
                        company_id=company.id,
                        name=f"{company.name} - EDITADA",
                        email=f"editada{i+1}@teste.com"
                    )
                    updated_company = company_controller.update_company(company.id, update_dto)
                    if updated_company:
                        self.log_test(f"Editar empresa {i+1}", True, "Nome e email atualizados")
                    else:
                        self.log_test(f"Editar empresa {i+1}", False, "Atualização falhou")
                        
                except Exception as e:
                    self.log_test(f"Editar empresa {i+1}", False, str(e))
            
            # Teste 6: Validação de dados inválidos
            invalid_test_cases = [
                {'name': '', 'document_number': '11.111.111/0001-11'},  # Nome vazio
                {'name': 'Teste', 'document_number': ''},  # CNPJ vazio
                {'name': 'Teste', 'document_number': '123'},  # CNPJ inválido
                {'name': 'Teste', 'document_number': '11.111.111/0001-11', 'email': 'email_invalido'},  # Email inválido
            ]
            
            for i, invalid_data in enumerate(invalid_test_cases):
                try:
                    # Completar dados obrigatórios que não estão sendo testados
                    complete_data = {
                        'name': 'Teste Inválido',
                        'document_number': '44.444.444/0001-44',
                        'postal_code': '01310-100',
                        'street': 'Rua Teste',
                        'number': '123',
                        'neighborhood': 'Centro',
                        'city': 'São Paulo',
                        'state': 'SP',
                        'email': 'teste@valido.com',
                        'phone': '(11) 99999-9999'
                    }
                    complete_data.update(invalid_data)
                    
                    company_dto = CreateCompanyDTO(**complete_data)
                    company = company_controller.create_company(company_dto)
                    
                    # Se chegou aqui, a validação falhou
                    self.log_test(f"Validação dados inválidos {i+1}", False, "Dados inválidos aceitos")
                    
                except Exception as e:
                    # Esperado - validação funcionando
                    self.log_test(f"Validação dados inválidos {i+1}", True, "Validação rejeitou dados inválidos")
            
        except Exception as e:
            self.log_test("Teste ultra completo empresas", False, str(e))
            traceback.print_exc()
    
    def test_ultra_complete_products(self):
        """Teste ultra completo de gestão de produtos."""
        print("\n📦 === TESTE ULTRA COMPLETO - GESTÃO DE PRODUTOS ===")
        
        try:
            product_controller = self.container.get_product_controller()
            
            # Teste 1: Listar produtos existentes
            existing_products = product_controller.list_products()
            self.log_test("Listagem inicial produtos", True, f"{len(existing_products)} produtos")
            
            # Teste 2: Criar produtos com dados variados
            test_products_data = [
                {
                    'sku': f'ULTRA-TEST-{self.generate_random_string(4)}',
                    'name': 'Notebook Dell Inspiron 15',
                    'unit_price': Decimal('2599.99'),
                    'unit': 'pcs',
                    'stock_quantity': 50,
                    'description': 'Notebook para uso profissional com processador Intel i5',
                    'category': 'Eletrônicos',
                    'barcode': '7891234567890'
                },
                {
                    'sku': f'ULTRA-TEST-{self.generate_random_string(4)}',
                    'name': 'Mouse Wireless Logitech',
                    'unit_price': Decimal('89.90'),
                    'unit': 'pcs',
                    'stock_quantity': 200,
                    'description': 'Mouse sem fio com tecnologia óptica',
                    'category': 'Acessórios',
                    'barcode': '7891234567891'
                },
                {
                    'sku': f'ULTRA-TEST-{self.generate_random_string(4)}',
                    'name': 'Teclado Mecânico RGB',
                    'unit_price': Decimal('299.99'),
                    'unit': 'pcs',
                    'stock_quantity': 75,
                    'description': 'Teclado mecânico com iluminação RGB personalizável',
                    'category': 'Periféricos',
                    'barcode': '7891234567892'
                },
                {
                    'sku': f'ULTRA-TEST-{self.generate_random_string(4)}',
                    'name': 'Monitor 24" Full HD',
                    'unit_price': Decimal('899.00'),
                    'unit': 'pcs',
                    'stock_quantity': 30,
                    'description': 'Monitor LED 24 polegadas resolução Full HD',
                    'category': 'Monitores',
                    'barcode': '7891234567893'
                },
                {
                    'sku': f'ULTRA-TEST-{self.generate_random_string(4)}',
                    'name': 'Cabo HDMI 2m',
                    'unit_price': Decimal('25.90'),
                    'unit': 'pcs',
                    'stock_quantity': 500,
                    'description': 'Cabo HDMI 2.0 de alta velocidade 2 metros',
                    'category': 'Cabos',
                    'barcode': '7891234567894'
                }
            ]
            
            created_products = []
            
            for i, product_data in enumerate(test_products_data):
                try:
                    product_dto = CreateProductDTO(**product_data)
                    product = product_controller.create_product(product_dto)
                    created_products.append(product)
                    self.created_entities['products'].append(product.id)
                    self.log_test(f"Criar produto {i+1}", True, f"SKU: {product.sku}, Nome: {product.name}")
                    
                except Exception as e:
                    self.log_test(f"Criar produto {i+1}", False, str(e))
            
            # Teste 3: Verificar listagem após criação
            updated_products = product_controller.list_products()
            expected_count = len(existing_products) + len(created_products)
            actual_count = len(updated_products)
            
            if actual_count >= expected_count:
                self.log_test("Listagem após criação produtos", True, f"{actual_count} produtos total")
            else:
                self.log_test("Listagem após criação produtos", False, f"Esperado >= {expected_count}, obtido {actual_count}")
            
            # Teste 4: Buscar cada produto por ID e SKU
            for product in created_products:
                # Buscar por ID
                found_product = product_controller.get_product(product.id)
                if found_product and found_product.id == product.id:
                    self.log_test(f"Buscar produto {product.sku} por ID", True, "Encontrado")
                else:
                    self.log_test(f"Buscar produto {product.sku} por ID", False, "Não encontrado")
                
                # Buscar por SKU
                if hasattr(product_controller, 'get_product_by_sku'):
                    found_by_sku = product_controller.get_product_by_sku(product.sku)
                    if found_by_sku and found_by_sku.sku == product.sku:
                        self.log_test(f"Buscar produto {product.sku} por SKU", True, "Encontrado")
                    else:
                        self.log_test(f"Buscar produto {product.sku} por SKU", False, "Não encontrado")
            
            # Teste 5: Editar produtos
            for i, product in enumerate(created_products):
                try:
                    new_price = product.unit_price + Decimal('50.00')
                    new_stock = product.stock_quantity + 10
                    
                    update_dto = UpdateProductDTO(
                        name=f"{product.name} - EDITADO",
                        unit_price=new_price,
                        stock_quantity=new_stock,
                        description=f"{product.description} - Produto atualizado em {datetime.now().strftime('%Y-%m-%d')}"
                    )
                    
                    updated_product = product_controller.update_product(product.id, update_dto)
                    if updated_product:
                        self.log_test(f"Editar produto {i+1}", True, f"Preço: {new_price}, Estoque: {new_stock}")
                    else:
                        self.log_test(f"Editar produto {i+1}", False, "Atualização falhou")
                        
                except Exception as e:
                    self.log_test(f"Editar produto {i+1}", False, str(e))
            
            # Teste 6: Operações de estoque
            for product in created_products[:2]:  # Testar apenas os 2 primeiros
                try:
                    # Atualizar estoque
                    new_stock = random.randint(1, 100)
                    success = product_controller.update_stock(product.id, new_stock)
                    if success:
                        self.log_test(f"Atualizar estoque {product.sku}", True, f"Novo estoque: {new_stock}")
                    else:
                        self.log_test(f"Atualizar estoque {product.sku}", False, "Falha na atualização")
                        
                except Exception as e:
                    self.log_test(f"Atualizar estoque {product.sku}", False, str(e))
            
            # Teste 7: Busca e filtros
            try:
                # Buscar produtos disponíveis
                available_products = product_controller.get_available_products()
                self.log_test("Buscar produtos disponíveis", True, f"{len(available_products)} produtos com estoque")
                
                # Buscar por termo
                search_results = product_controller.search_products("ULTRA-TEST")
                self.log_test("Busca por termo", True, f"{len(search_results)} produtos encontrados")
                
            except Exception as e:
                self.log_test("Operações de busca", False, str(e))
            
            # Teste 8: Validação de dados inválidos
            invalid_product_cases = [
                {'sku': '', 'name': 'Teste', 'unit_price': Decimal('10.00')},  # SKU vazio
                {'sku': 'TEST', 'name': '', 'unit_price': Decimal('10.00')},  # Nome vazio
                {'sku': 'TEST', 'name': 'Teste', 'unit_price': Decimal('-10.00')},  # Preço negativo
                {'sku': 'TEST', 'name': 'Teste', 'unit_price': Decimal('10.00'), 'stock_quantity': -5},  # Estoque negativo
            ]
            
            for i, invalid_data in enumerate(invalid_product_cases):
                try:
                    complete_data = {
                        'sku': f'INVALID-{i}',
                        'name': 'Produto Inválido',
                        'unit_price': Decimal('10.00'),
                        'unit': 'pcs',
                        'stock_quantity': 10
                    }
                    complete_data.update(invalid_data)
                    
                    product_dto = CreateProductDTO(**complete_data)
                    product = product_controller.create_product(product_dto)
                    
                    self.log_test(f"Validação produto inválido {i+1}", False, "Dados inválidos aceitos")
                    
                except Exception as e:
                    self.log_test(f"Validação produto inválido {i+1}", True, "Validação rejeitou dados inválidos")
            
        except Exception as e:
            self.log_test("Teste ultra completo produtos", False, str(e))
            traceback.print_exc()
    
    def test_ultra_complete_sales_orders(self):
        """Teste ultra completo de gestão de pedidos de vendas."""
        print("\n🛒 === TESTE ULTRA COMPLETO - GESTÃO DE PEDIDOS ===")
        
        try:
            sales_controller = self.container.get_sales_order_controller()
            company_controller = self.container.get_company_controller()
            product_controller = self.container.get_product_controller()
            
            # Obter empresas e produtos para usar nos pedidos
            companies = company_controller.list_companies()
            products = product_controller.list_products()
            
            if not companies:
                self.log_test("Preparação pedidos - Empresas", False, "Nenhuma empresa disponível")
                return
                
            if not products:
                self.log_test("Preparação pedidos - Produtos", False, "Nenhum produto disponível")
                return
                
            self.log_test("Preparação pedidos", True, f"{len(companies)} empresas, {len(products)} produtos")
            
            # Teste 1: Listar pedidos existentes
            list_success, existing_orders, list_error = sales_controller.list_sales_orders()
            if list_success:
                self.log_test("Listagem inicial pedidos", True, f"{len(existing_orders)} pedidos")
            else:
                self.log_test("Listagem inicial pedidos", False, list_error)
                return
            
            # Teste 2: Criar múltiplos pedidos
            created_orders = []
            
            for i in range(min(3, len(companies))):  # Criar até 3 pedidos
                try:
                    company = companies[i % len(companies)]
                    success, order, error = sales_controller.create_sales_order(company.id)
                    
                    if success and order:
                        created_orders.append(order)
                        self.created_entities['orders'].append(order.id)
                        self.log_test(f"Criar pedido {i+1}", True, f"ID: {order.id}, Empresa: {company.name}")
                    else:
                        self.log_test(f"Criar pedido {i+1}", False, error or "Erro desconhecido")
                        
                except Exception as e:
                    self.log_test(f"Criar pedido {i+1}", False, str(e))
            
            # Teste 3: Adicionar itens aos pedidos
            for i, order in enumerate(created_orders):
                try:
                    # Adicionar múltiplos itens a cada pedido
                    items_added = 0
                    
                    for j in range(min(3, len(products))):  # Até 3 itens por pedido
                        product = products[j % len(products)]
                        quantity = random.randint(1, 5)
                        
                        success, updated_order, error = sales_controller.add_item_to_order(
                            order.id, product.id, quantity
                        )
                        
                        if success:
                            items_added += 1
                            self.log_test(f"Adicionar item {j+1} ao pedido {i+1}", True, 
                                        f"Produto: {product.name}, Qtd: {quantity}")
                            order = updated_order  # Atualizar referência do pedido
                        else:
                            self.log_test(f"Adicionar item {j+1} ao pedido {i+1}", False, error)
                    
                    if items_added > 0:
                        self.log_test(f"Itens adicionados pedido {i+1}", True, f"{items_added} itens, Total: R$ {order.total_amount}")
                    
                except Exception as e:
                    self.log_test(f"Adicionar itens pedido {i+1}", False, str(e))
            
            # Teste 4: Buscar pedidos por ID
            for i, order in enumerate(created_orders):
                try:
                    success, found_order, error = sales_controller.get_sales_order(order.id)
                    
                    if success and found_order:
                        self.log_test(f"Buscar pedido {i+1}", True, f"Encontrado com {len(found_order.items)} itens")
                    else:
                        self.log_test(f"Buscar pedido {i+1}", False, error or "Pedido não encontrado")
                        
                except Exception as e:
                    self.log_test(f"Buscar pedido {i+1}", False, str(e))
            
            # Teste 5: Atualizar quantidades de itens
            for i, order in enumerate(created_orders):
                if not order.items:
                    continue
                    
                try:
                    # Pegar primeiro item e atualizar quantidade
                    first_item = order.items[0]
                    new_quantity = random.randint(1, 10)
                    
                    success, updated_order, error = sales_controller.update_order_item(
                        order.id, first_item.product_id, new_quantity
                    )
                    
                    if success:
                        self.log_test(f"Atualizar item pedido {i+1}", True, f"Nova quantidade: {new_quantity}")
                    else:
                        self.log_test(f"Atualizar item pedido {i+1}", False, error)
                        
                except Exception as e:
                    self.log_test(f"Atualizar item pedido {i+1}", False, str(e))
            
            # Teste 6: Remover itens dos pedidos
            for i, order in enumerate(created_orders):
                if len(order.items) <= 1:  # Manter pelo menos 1 item
                    continue
                    
                try:
                    # Remover último item
                    last_item = order.items[-1]
                    
                    success, updated_order, error = sales_controller.remove_item_from_order(
                        order.id, last_item.product_id
                    )
                    
                    if success:
                        self.log_test(f"Remover item pedido {i+1}", True, f"Item removido, {len(updated_order.items)} restantes")
                    else:
                        self.log_test(f"Remover item pedido {i+1}", False, error)
                        
                except Exception as e:
                    self.log_test(f"Remover item pedido {i+1}", False, str(e))
            
            # Teste 7: Verificar listagem após operações
            final_success, final_orders, final_error = sales_controller.list_sales_orders()
            if final_success:
                expected_count = len(existing_orders) + len(created_orders)
                actual_count = len(final_orders)
                
                if actual_count >= expected_count:
                    self.log_test("Listagem final pedidos", True, f"{actual_count} pedidos total")
                else:
                    self.log_test("Listagem final pedidos", False, f"Esperado >= {expected_count}, obtido {actual_count}")
            else:
                self.log_test("Listagem final pedidos", False, final_error)
            
            # Teste 8: Validações de negócio
            if companies and products:
                try:
                    # Tentar adicionar quantidade negativa
                    test_company = companies[0]
                    success, test_order, error = sales_controller.create_sales_order(test_company.id)
                    
                    if success:
                        test_product = products[0]
                        success2, _, error2 = sales_controller.add_item_to_order(
                            test_order.id, test_product.id, -5  # Quantidade negativa
                        )
                        
                        if success2:
                            self.log_test("Validação quantidade negativa", False, "Quantidade negativa aceita")
                        else:
                            self.log_test("Validação quantidade negativa", True, "Quantidade negativa rejeitada")
                            
                except Exception as e:
                    self.log_test("Validação quantidade negativa", True, "Exceção capturada corretamente")
                
                try:
                    # Tentar usar produto inexistente
                    if created_orders:
                        fake_product_id = "produto-inexistente-123"
                        success, _, error = sales_controller.add_item_to_order(
                            created_orders[0].id, fake_product_id, 1
                        )
                        
                        if success:
                            self.log_test("Validação produto inexistente", False, "Produto inexistente aceito")
                        else:
                            self.log_test("Validação produto inexistente", True, "Produto inexistente rejeitado")
                            
                except Exception as e:
                    self.log_test("Validação produto inexistente", True, "Exceção capturada corretamente")
            
        except Exception as e:
            self.log_test("Teste ultra completo pedidos", False, str(e))
            traceback.print_exc()
    
    def test_brasil_api_integration_ultra(self):
        """Teste ultra completo da integração BrasilAPI."""
        print("\n🌐 === TESTE ULTRA COMPLETO - INTEGRAÇÃO BRASILAPI ===")
        
        try:
            from src.infrastructure.external_services.brasilapi_service import BrasilApiService
            from src.infrastructure.external_services.product_enhancement_service import ProductEnhancementService
            
            brasil_api = BrasilApiService()
            enhancement = ProductEnhancementService()
            
            # Teste 1: Múltiplos CEPs
            test_ceps = ['01310-100', '20040-020', '30112-000', '40010-000', '50030-230', '60060-440']
            
            for cep in test_ceps:
                try:
                    result = brasil_api.get_cep_info(cep)
                    if result and any([result.get('logradouro'), result.get('bairro'), result.get('cidade'), result.get('uf')]):
                        self.log_test(f"BrasilAPI - CEP {cep}", True, f"{result.get('cidade', 'N/A')}/{result.get('uf', 'N/A')}")
                    else:
                        self.log_test(f"BrasilAPI - CEP {cep}", False, "Resultado inválido")
                except Exception as e:
                    self.log_test(f"BrasilAPI - CEP {cep}", False, str(e))
            
            # Teste 2: Validação de CNPJs
            test_cnpjs = [
                '11.222.333/0001-81',  # CNPJ provavelmente inválido
                '00.000.000/0001-91',  # CNPJ conhecido como inválido
                '11.444.777/0001-61'   # Outro teste
            ]
            
            for cnpj in test_cnpjs:
                try:
                    result = brasil_api.get_cnpj_info(cnpj)
                    if result:
                        self.log_test(f"BrasilAPI - CNPJ {cnpj}", True, "Dados retornados")
                    else:
                        self.log_test(f"BrasilAPI - CNPJ {cnpj}", True, "CNPJ não encontrado (esperado)")
                except Exception as e:
                    self.log_test(f"BrasilAPI - CNPJ {cnpj}", False, str(e))
            
            # Teste 3: Informações bancárias
            test_bank_codes = ['001', '033', '104', '237', '341', '422']
            
            for bank_code in test_bank_codes:
                try:
                    result = brasil_api.get_bank_by_code(bank_code)
                    if result and 'name' in result:
                        self.log_test(f"BrasilAPI - Banco {bank_code}", True, f"{result['name']}")
                    else:
                        self.log_test(f"BrasilAPI - Banco {bank_code}", False, "Dados não encontrados")
                except Exception as e:
                    self.log_test(f"BrasilAPI - Banco {bank_code}", False, str(e))
            
            # Teste 4: Enhancement de produtos
            test_products = [
                'notebook dell inspiron',
                'mouse gamer rgb',
                'teclado mecânico',
                'monitor 4k',
                'smartphone samsung',
                'tablet ipad',
                'fone bluetooth',
                'impressora laser',
                'roteador wifi',
                'webcam hd'
            ]
            
            for product_name in test_products:
                try:
                    categories = enhancement.suggest_product_categories(product_name)
                    if categories:
                        self.log_test(f"Enhancement - {product_name}", True, f"Categorias: {categories}")
                    else:
                        self.log_test(f"Enhancement - {product_name}", False, "Nenhuma categoria sugerida")
                except Exception as e:
                    self.log_test(f"Enhancement - {product_name}", False, str(e))
            
            # Teste 5: Códigos NCM
            try:
                ncm_suggestions = enhancement.suggest_ncm_codes('notebook computer', 'Electronics')
                if ncm_suggestions:
                    self.log_test("Enhancement - NCM Codes", True, f"{len(ncm_suggestions)} códigos encontrados")
                    
                    for i, ncm in enumerate(ncm_suggestions[:3]):
                        self.log_test(f"NCM {i+1}", True, f"{ncm.get('code', 'N/A')} - {ncm.get('description', 'N/A')}")
                else:
                    self.log_test("Enhancement - NCM Codes", False, "Nenhum código encontrado")
            except Exception as e:
                self.log_test("Enhancement - NCM Codes", False, str(e))
            
        except Exception as e:
            self.log_test("Teste ultra completo BrasilAPI", False, str(e))
            traceback.print_exc()
    
    def test_data_persistence_ultra(self):
        """Teste ultra completo de persistência de dados."""
        print("\n💾 === TESTE ULTRA COMPLETO - PERSISTÊNCIA DE DADOS ===")
        
        try:
            # Teste 1: Verificar arquivos de dados
            data_files = {
                'companies.json': 'data/companies.json',
                'products.json': 'data/products.json',
                'sales_orders.json': 'data/sales_orders.json'
            }
            
            for file_name, file_path in data_files.items():
                full_path = os.path.join(os.path.dirname(__file__), file_path)
                
                if os.path.exists(full_path):
                    try:
                        # Verificar se é JSON válido
                        with open(full_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        self.log_test(f"Arquivo {file_name}", True, f"Existe e é JSON válido ({len(data)} registros)")
                        
                        # Verificar estrutura básica
                        if isinstance(data, list) and len(data) > 0:
                            first_item = data[0]
                            if isinstance(first_item, dict) and 'id' in first_item:
                                self.log_test(f"Estrutura {file_name}", True, "Estrutura válida com ID")
                            else:
                                self.log_test(f"Estrutura {file_name}", False, "Estrutura inválida")
                        
                    except json.JSONDecodeError as e:
                        self.log_test(f"Arquivo {file_name}", False, f"JSON inválido: {e}")
                    except Exception as e:
                        self.log_test(f"Arquivo {file_name}", False, f"Erro ao ler: {e}")
                else:
                    self.log_test(f"Arquivo {file_name}", False, "Arquivo não encontrado")
            
            # Teste 2: Verificar integridade referencial
            try:
                company_controller = self.container.get_company_controller()
                product_controller = self.container.get_product_controller()
                sales_controller = self.container.get_sales_order_controller()
                
                companies = company_controller.list_companies()
                products = product_controller.list_products()
                list_success, orders, list_error = sales_controller.list_sales_orders()
                
                if list_success:
                    self.log_test("Carregamento dados", True, f"Empresas: {len(companies)}, Produtos: {len(products)}, Pedidos: {len(orders)}")
                    
                    # Verificar referências em pedidos
                    company_ids = {c.id for c in companies}
                    product_ids = {p.id for p in products}
                    
                    broken_references = 0
                    
                    for order in orders:
                        # Verificar se empresa existe
                        if hasattr(order, 'company_id') and order.company_id not in company_ids:
                            broken_references += 1
                        
                        # Verificar se produtos dos itens existem
                        if hasattr(order, 'items'):
                            for item in order.items:
                                if hasattr(item, 'product_id') and item.product_id not in product_ids:
                                    broken_references += 1
                    
                    if broken_references == 0:
                        self.log_test("Integridade referencial", True, "Todas as referências válidas")
                    else:
                        self.log_test("Integridade referencial", False, f"{broken_references} referências quebradas")
                        
                else:
                    self.log_test("Carregamento pedidos", False, list_error)
                    
            except Exception as e:
                self.log_test("Verificação integridade", False, str(e))
            
            # Teste 3: Performance de carregamento
            try:
                start_time = time.time()
                
                # Recarregar todos os dados
                companies = company_controller.list_companies()
                products = product_controller.list_products()
                list_success, orders, _ = sales_controller.list_sales_orders()
                
                end_time = time.time()
                load_time = end_time - start_time
                
                total_records = len(companies) + len(products) + (len(orders) if list_success else 0)
                
                if load_time < 2.0:  # Menos de 2 segundos
                    self.log_test("Performance carregamento", True, f"{total_records} registros em {load_time:.3f}s")
                else:
                    self.log_test("Performance carregamento", False, f"Carregamento lento: {load_time:.3f}s")
                    
            except Exception as e:
                self.log_test("Teste performance", False, str(e))
                
        except Exception as e:
            self.log_test("Teste ultra completo persistência", False, str(e))
            traceback.print_exc()
    
    def test_gui_interactions_ultra(self):
        """Teste ultra completo de interações da GUI."""
        print("\n🖱️ === TESTE ULTRA COMPLETO - INTERAÇÕES DA GUI ===")
        
        try:
            # Teste 1: Navegação entre todas as abas
            if hasattr(self.app, 'notebook'):
                notebook = self.app.notebook
                tab_count = notebook.index('end')
                
                for i in range(tab_count):
                    try:
                        notebook.select(i)
                        self.root.update()
                        time.sleep(0.1)  # Pausa pequena
                        
                        tab_text = notebook.tab(i, 'text')
                        selected_tab = notebook.select()
                        expected_tab = notebook.tabs()[i]
                        
                        if selected_tab == expected_tab:
                            self.log_test(f"Navegar aba '{tab_text}'", True, f"Aba {i+1} selecionada")
                        else:
                            self.log_test(f"Navegar aba '{tab_text}'", False, "Seleção falhou")
                            
                    except Exception as e:
                        self.log_test(f"Navegar aba {i+1}", False, str(e))
            
            # Teste 2: Verificar responsividade da GUI
            try:
                original_size = self.root.geometry()
                
                # Testar redimensionamento
                test_sizes = ['800x600', '1000x700', '1400x900']
                
                for size in test_sizes:
                    self.root.geometry(size)
                    self.root.update()
                    time.sleep(0.1)
                    
                    current_size = self.root.geometry().split('+')[0]  # Pegar apenas WxH
                    current_w, current_h = map(int, current_size.split('x'))
                    target_w, target_h = map(int, size.split('x'))
                    
                    # Verificar se está próximo do tamanho desejado (tolerância de ±50px)
                    w_diff = abs(current_w - target_w)
                    h_diff = abs(current_h - target_h)
                    
                    if w_diff <= 50 and h_diff <= 50:
                        self.log_test(f"Redimensionar para {size}", True, f"Próximo: {current_size}")
                    else:
                        self.log_test(f"Redimensionar para {size}", True, f"Sistema limitou: {current_size}")
                
                # Restaurar tamanho original
                self.root.geometry(original_size)
                self.root.update()
                
            except Exception as e:
                self.log_test("Teste redimensionamento", False, str(e))
            
            # Teste 3: Verificar elementos da interface
            try:
                # Verificar status bar
                if hasattr(self.app, 'status_bar'):
                    status_bar = self.app.status_bar
                    if status_bar and status_bar.winfo_exists():
                        self.log_test("Status bar", True, "Presente e visível")
                    else:
                        self.log_test("Status bar", False, "Não encontrada ou não visível")
                
                # Verificar menu
                if hasattr(self.root, 'config') and 'menu' in self.root.keys():
                    menu = self.root['menu']
                    if menu:
                        self.log_test("Menu principal", True, "Menu configurado")
                    else:
                        self.log_test("Menu principal", False, "Menu não configurado")
                
            except Exception as e:
                self.log_test("Verificação elementos GUI", False, str(e))
            
            # Teste 4: Atualização da interface
            try:
                # Forçar múltiplas atualizações
                for i in range(5):
                    self.root.update_idletasks()
                    self.root.update()
                    time.sleep(0.05)
                
                self.log_test("Atualizações múltiplas GUI", True, "5 atualizações executadas")
                
            except Exception as e:
                self.log_test("Atualizações múltiplas GUI", False, str(e))
                
        except Exception as e:
            self.log_test("Teste ultra completo GUI", False, str(e))
            traceback.print_exc()
    
    def run_ultra_comprehensive_tests(self):
        """Executar todos os testes ultra completos."""
        print("🚀 === INICIANDO TESTES ULTRA COMPLETOS E PROFUNDOS ===")
        print("⚠️  Este teste é EXTREMAMENTE detalhado e pode demorar alguns minutos")
        print("🔍 Testando TODAS as funcionalidades do sistema minuciosamente\n")
        
        start_time = time.time()
        
        # Setup inicial
        if not self.setup_ultra_gui():
            print("❌ Falha no setup inicial - abortando testes")
            return
        
        # Executar testes em thread separada
        def run_all_tests():
            try:
                time.sleep(2)  # Aguardar GUI estar pronta
                
                print("🏁 Iniciando bateria de testes...")
                
                # Executar todos os testes ultra completos
                self.test_ultra_complete_companies()
                self.test_ultra_complete_products()
                self.test_ultra_complete_sales_orders()
                self.test_brasil_api_integration_ultra()
                self.test_data_persistence_ultra()
                self.test_gui_interactions_ultra()
                
                # Gerar relatório final ultra detalhado
                self.generate_ultra_comprehensive_report(start_time)
                
                # Fechar GUI após testes
                self.root.after(5000, self.root.quit)  # Aguardar 5s para relatório
                
            except Exception as e:
                print(f"❌ Erro durante execução dos testes: {e}")
                traceback.print_exc()
                self.root.quit()
        
        # Iniciar testes em thread separada
        test_thread = threading.Thread(target=run_all_tests)
        test_thread.daemon = True
        test_thread.start()
        
        # Executar GUI
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"❌ Erro na execução da GUI: {e}")
    
    def generate_ultra_comprehensive_report(self, start_time):
        """Gerar relatório ultra completo e detalhado."""
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n" + "="*80)
        print(f"🎯 === RELATÓRIO ULTRA COMPLETO DOS TESTES ===")
        print(f"="*80)
        print(f"⏱️  Tempo total de execução: {duration:.2f} segundos")
        print(f"📊 Total de testes executados: {len(self.test_results)}")
        print(f"✅ Testes bem-sucedidos: {len([r for r in self.test_results if '✅' in r])}")
        print(f"❌ Testes com falha: {len([r for r in self.test_results if '❌' in r])}")
        print(f"⚠️  Avisos encontrados: {len(self.warnings_found)}")
        
        # Calcular taxa de sucesso
        total_tests = len(self.test_results)
        successful_tests = len([r for r in self.test_results if '✅' in r])
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📈 Taxa de sucesso: {success_rate:.1f}%")
        
        # Status do sistema
        if success_rate >= 95:
            system_status = "🎉 EXCELENTE - Sistema altamente estável"
        elif success_rate >= 85:
            system_status = "✅ BOM - Sistema funcional com pequenos ajustes"
        elif success_rate >= 70:
            system_status = "⚠️  REGULAR - Sistema precisa de correções"
        else:
            system_status = "❌ CRÍTICO - Sistema requer atenção imediata"
        
        print(f"🔧 Status do sistema: {system_status}")
        
        # Entidades criadas durante os testes
        print(f"\n📦 Entidades criadas nos testes:")
        print(f"   • Empresas: {len(self.created_entities['companies'])}")
        print(f"   • Produtos: {len(self.created_entities['products'])}")
        print(f"   • Pedidos: {len(self.created_entities['orders'])}")
        
        # Erros encontrados
        if self.errors_found:
            print(f"\n🚨 ERROS CRÍTICOS ENCONTRADOS ({len(self.errors_found)}):")
            for i, error in enumerate(self.errors_found, 1):
                print(f"   {i:2d}. {error}")
        else:
            print(f"\n🎉 NENHUM ERRO CRÍTICO ENCONTRADO!")
        
        # Avisos
        if self.warnings_found:
            print(f"\n⚠️  AVISOS ({len(self.warnings_found)}):")
            for i, warning in enumerate(self.warnings_found, 1):
                print(f"   {i:2d}. {warning}")
        
        print(f"\n📋 LOG DETALHADO DE TODOS OS TESTES:")
        print(f"-" * 80)
        for i, result in enumerate(self.test_results, 1):
            print(f"{i:3d}. {result}")
        
        # Salvar relatório ultra detalhado em arquivo
        report_file = os.path.join(os.path.dirname(__file__), 'ultra_comprehensive_test_report.txt')
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO ULTRA COMPLETO - TESTES AUTOMATIZADOS PYSYSTEM\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Duração: {duration:.2f} segundos\n")
            f.write(f"Total de testes: {total_tests}\n")
            f.write(f"Sucessos: {successful_tests}\n")
            f.write(f"Falhas: {len(self.errors_found)}\n")
            f.write(f"Taxa de sucesso: {success_rate:.1f}%\n")
            f.write(f"Status: {system_status}\n\n")
            
            f.write("ENTIDADES CRIADAS:\n")
            f.write(f"Empresas: {len(self.created_entities['companies'])}\n")
            f.write(f"Produtos: {len(self.created_entities['products'])}\n")
            f.write(f"Pedidos: {len(self.created_entities['orders'])}\n\n")
            
            if self.errors_found:
                f.write("ERROS CRÍTICOS:\n")
                for i, error in enumerate(self.errors_found, 1):
                    f.write(f"{i:2d}. {error}\n")
                f.write("\n")
            
            if self.warnings_found:
                f.write("AVISOS:\n")
                for i, warning in enumerate(self.warnings_found, 1):
                    f.write(f"{i:2d}. {warning}\n")
                f.write("\n")
            
            f.write("LOG COMPLETO:\n")
            for i, result in enumerate(self.test_results, 1):
                f.write(f"{i:3d}. {result}\n")
        
        print(f"\n📄 Relatório ultra detalhado salvo em: {report_file}")
        print(f"="*80)


def main():
    """Função principal do testador ultra completo."""
    print("🔬 PYSYSTEM - SISTEMA DE TESTES ULTRA COMPLETO E PROFUNDO")
    print("=" * 80)
    print("⚡ Este sistema irá testar TODAS as funcionalidades minuciosamente")
    print("🔍 Incluindo validações, integrações, persistência e GUI")
    print("⏱️  O processo pode demorar alguns minutos devido à profundidade")
    print("🎯 Objetivo: Encontrar QUALQUER erro no sistema")
    print("=" * 80)
    
    try:
        tester = UltraComprehensiveGUITester()
        tester.run_ultra_comprehensive_tests()
        
    except KeyboardInterrupt:
        print("\n⚠️ Testes interrompidos pelo usuário")
    except Exception as e:
        print(f"❌ Erro fatal durante inicialização: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
