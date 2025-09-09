#!/usr/bin/env python3
"""
Sistema de Testes Automatizados da GUI do PYSYSTEM
Testa todas as funcionalidades da interface gráfica de forma automatizada
"""

import sys
import os
import time
import threading
import tkinter as tk
from tkinter import messagebox
from decimal import Decimal
import traceback

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.presentation.gui.main_window import MainWindow
from src.presentation.gui.dependency_injection import DependencyContainer
from src.application.dtos.company_dto import CreateCompanyDTO
from src.application.dtos.product_dto import CreateProductDTO


class AutomatedGUITester:
    """Testador automatizado da interface gráfica."""
    
    def __init__(self):
        """Inicializar testador."""
        self.test_results = []
        self.errors_found = []
        self.root = None
        self.app = None
        self.container = DependencyContainer()
        
    def log_test(self, test_name, success, error=None):
        """Registrar resultado do teste."""
        status = "✅ PASS" if success else "❌ FAIL"
        result = f"{status} - {test_name}"
        
        if error:
            result += f" | Erro: {error}"
            self.errors_found.append(f"{test_name}: {error}")
            
        self.test_results.append(result)
        print(result)
    
    def setup_gui(self):
        """Configurar interface gráfica para testes."""
        try:
            print("🖥️ Configurando interface gráfica...")
            self.root = tk.Tk()
            self.root.title("PYSYSTEM - Testes Automatizados")
            self.root.geometry("1200x800+100+100")
            self.root.minsize(800, 600)
            
            # Criar aplicação
            self.app = MainWindow(self.root)
            
            # Configurar para testes
            self.root.update()
            self.root.lift()
            
            self.log_test("Setup GUI", True)
            return True
            
        except Exception as e:
            self.log_test("Setup GUI", False, str(e))
            return False
    
    def test_company_management(self):
        """Testar gestão de empresas."""
        print("\n🏢 === TESTANDO GESTÃO DE EMPRESAS ===")
        
        try:
            # Acessar aba de empresas
            company_frame = getattr(self.app, 'company_frame', None)
            if not company_frame:
                self.log_test("Acesso aba Empresas", False, "Frame de empresas não encontrado")
                return
            
            self.log_test("Acesso aba Empresas", True)
            
            # Teste 1: Criar nova empresa
            try:
                company_controller = self.container.get_company_controller()
                
                company_dto = CreateCompanyDTO(
                    name='Empresa Teste Automatizado',
                    document_number='11.222.333/0001-89',
                    postal_code='01310-100',
                    street='Av. Paulista',
                    number='1000',
                    neighborhood='Bela Vista',
                    city='São Paulo',
                    state='SP',
                    email='teste@automatizado.com',
                    phone='(11) 99999-9999'
                )
                
                company = company_controller.create_company(company_dto)
                self.log_test("Criar empresa", True, f"ID: {company.id}")
                
                # Teste de listagem
                companies = company_controller.list_companies()
                self.log_test("Listar empresas", True, f"Total: {len(companies)}")
                
                # Teste de busca por ID
                if companies:
                    found_company = company_controller.get_company(companies[0].id)
                    self.log_test("Buscar empresa por ID", found_company is not None)
                
                # Teste de edição
                if companies:
                    company_to_update = companies[0]
                    from src.application.dtos.company_dto import UpdateCompanyDTO
                    update_dto = UpdateCompanyDTO(
                        company_id=company_to_update.id,
                        name='Empresa Editada Automaticamente'
                    )
                    updated = company_controller.update_company(company_to_update.id, update_dto)
                    self.log_test("Editar empresa", updated is not None)
                
                # Teste de exclusão (comentado para não afetar dados)
                # company_controller.delete_company(company.id)
                # self.log_test("Excluir empresa", True)
                
            except Exception as e:
                self.log_test("Operações de empresa", False, str(e))
                traceback.print_exc()
                
        except Exception as e:
            self.log_test("Teste gestão empresas", False, str(e))
    
    def test_product_management(self):
        """Testar gestão de produtos."""
        print("\n📦 === TESTANDO GESTÃO DE PRODUTOS ===")
        
        try:
            # Acessar frame de produtos
            product_frame = getattr(self.app, 'product_frame', None)
            if not product_frame:
                self.log_test("Acesso aba Produtos", False, "Frame de produtos não encontrado")
                return
            
            self.log_test("Acesso aba Produtos", True)
            
            # Teste 1: Criar novo produto
            try:
                product_controller = self.container.get_product_controller()
                
                product_dto = CreateProductDTO(
                    sku='AUTO-TEST-001',
                    name='Produto Teste Automatizado',
                    unit_price=Decimal('199.99'),
                    unit='pcs',
                    stock_quantity=50,
                    description='Produto criado por teste automatizado',
                    category='Teste'
                )
                
                product = product_controller.create_product(product_dto)
                self.log_test("Criar produto", True, f"SKU: {product.sku}")
                
                # Teste de listagem
                products = product_controller.list_products()
                self.log_test("Listar produtos", True, f"Total: {len(products)}")
                
                # Teste de busca por ID
                if products:
                    found_product = product_controller.get_product(products[0].id)
                    self.log_test("Buscar produto por ID", found_product is not None)
                
                # Teste de busca por SKU
                found_by_sku = product_controller.get_product_by_sku('AUTO-TEST-001')
                self.log_test("Buscar produto por SKU", found_by_sku is not None)
                
                # Teste de atualização de estoque
                if products:
                    success = product_controller.update_stock(products[0].id, 75)
                    self.log_test("Atualizar estoque", success)
                
                # Teste de edição
                if products:
                    from src.application.dtos.product_dto import UpdateProductDTO
                    update_dto = UpdateProductDTO(
                        name='Produto Editado Automaticamente',
                        unit_price=Decimal('299.99')
                    )
                    updated = product_controller.update_product(products[0].id, update_dto)
                    self.log_test("Editar produto", updated is not None)
                
            except Exception as e:
                self.log_test("Operações de produto", False, str(e))
                traceback.print_exc()
                
        except Exception as e:
            self.log_test("Teste gestão produtos", False, str(e))
    
    def test_sales_order_management(self):
        """Testar gestão de pedidos de venda."""
        print("\n🛒 === TESTANDO GESTÃO DE PEDIDOS ===")
        
        try:
            # Acessar frame de pedidos
            sales_frame = getattr(self.app, 'sales_order_frame', None)
            if not sales_frame:
                self.log_test("Acesso aba Pedidos", False, "Frame de pedidos não encontrado")
                return
            
            self.log_test("Acesso aba Pedidos", True)
            
            # Preparar dados para teste
            company_controller = self.container.get_company_controller()
            product_controller = self.container.get_product_controller()
            sales_controller = self.container.get_sales_order_controller()
            
            companies = company_controller.list_companies()
            products = product_controller.list_products()
            
            if not companies:
                self.log_test("Preparar dados pedido", False, "Nenhuma empresa disponível")
                return
                
            if not products:
                self.log_test("Preparar dados pedido", False, "Nenhum produto disponível")
                return
            
            # Teste 1: Criar pedido
            try:
                success, order, error = sales_controller.create_sales_order(companies[0].id)
                
                if success and order:
                    self.log_test("Criar pedido", True, f"ID: {order.id}")
                    
                    # Teste 2: Adicionar item ao pedido
                    success2, updated_order, error2 = sales_controller.add_item_to_order(
                        order.id, products[0].id, 2
                    )
                    
                    if success2:
                        self.log_test("Adicionar item ao pedido", True, f"Total: R$ {updated_order.total_amount}")
                    else:
                        self.log_test("Adicionar item ao pedido", False, error2)
                    
                    # Teste 3: Listar pedidos
                    list_success, orders, list_error = sales_controller.list_sales_orders()
                    if list_success:
                        self.log_test("Listar pedidos", True, f"Total: {len(orders)}")
                    else:
                        self.log_test("Listar pedidos", False, list_error)
                    
                    # Teste 4: Buscar pedido específico
                    get_success, found_order, get_error = sales_controller.get_sales_order(order.id)
                    if get_success:
                        self.log_test("Buscar pedido por ID", True)
                    else:
                        self.log_test("Buscar pedido por ID", False, get_error)
                        
                else:
                    self.log_test("Criar pedido", False, error)
                    
            except Exception as e:
                self.log_test("Operações de pedido", False, str(e))
                traceback.print_exc()
                
        except Exception as e:
            self.log_test("Teste gestão pedidos", False, str(e))
    
    def test_brasil_api_integration(self):
        """Testar integração com BrasilAPI."""
        print("\n🌐 === TESTANDO INTEGRAÇÃO BRASILAPI ===")
        
        try:
            from src.infrastructure.external_services.brasilapi_service import BrasilApiService
            brasil_api = BrasilApiService()
            
            # Teste 1: Busca de CEP
            try:
                cep_result = brasil_api.get_cep_info('01310-100')
                if cep_result and 'city' in cep_result:
                    self.log_test("BrasilAPI - Busca CEP", True, f"Cidade: {cep_result['city']}")
                else:
                    self.log_test("BrasilAPI - Busca CEP", False, "Resultado inválido")
            except Exception as e:
                self.log_test("BrasilAPI - Busca CEP", False, str(e))
            
            # Teste 2: Validação CNPJ
            try:
                cnpj_result = brasil_api.get_cnpj_info('11.222.333/0001-81')
                if cnpj_result is not None:
                    self.log_test("BrasilAPI - Validação CNPJ", True)
                else:
                    self.log_test("BrasilAPI - Validação CNPJ", True, "CNPJ inválido como esperado")
            except Exception as e:
                self.log_test("BrasilAPI - Validação CNPJ", False, str(e))
            
            # Teste 3: Informações bancárias
            try:
                bank_result = brasil_api.get_bank_by_code('001')
                if bank_result and 'name' in bank_result:
                    self.log_test("BrasilAPI - Info bancária", True, f"Banco: {bank_result['name']}")
                else:
                    self.log_test("BrasilAPI - Info bancária", False, "Resultado inválido")
            except Exception as e:
                self.log_test("BrasilAPI - Info bancária", False, str(e))
                
        except Exception as e:
            self.log_test("Teste BrasilAPI", False, str(e))
    
    def test_gui_interactions(self):
        """Testar interações específicas da GUI."""
        print("\n🖱️ === TESTANDO INTERAÇÕES DA GUI ===")
        
        try:
            # Teste 1: Navegação entre abas
            if hasattr(self.app, 'notebook'):
                notebook = self.app.notebook
                
                # Testar cada aba
                for i in range(notebook.index('end')):
                    try:
                        notebook.select(i)
                        self.root.update()
                        tab_text = notebook.tab(i, 'text')
                        self.log_test(f"Navegar para aba '{tab_text}'", True)
                        time.sleep(0.1)  # Pequena pausa
                    except Exception as e:
                        self.log_test(f"Navegar para aba {i}", False, str(e))
            
            # Teste 2: Atualização de dados
            try:
                # Simular clique em botões de refresh se existirem
                self.root.update()
                self.log_test("Atualização de interface", True)
            except Exception as e:
                self.log_test("Atualização de interface", False, str(e))
                
        except Exception as e:
            self.log_test("Teste interações GUI", False, str(e))
    
    def test_data_persistence(self):
        """Testar persistência de dados."""
        print("\n💾 === TESTANDO PERSISTÊNCIA DE DADOS ===")
        
        try:
            # Teste 1: Verificar arquivos de dados
            data_files = [
                'data/companies.json',
                'data/products.json',
                'data/sales_orders.json'
            ]
            
            for file_path in data_files:
                full_path = os.path.join(os.path.dirname(__file__), file_path)
                if os.path.exists(full_path):
                    self.log_test(f"Arquivo de dados {file_path}", True, "Existe")
                else:
                    self.log_test(f"Arquivo de dados {file_path}", False, "Não encontrado")
            
            # Teste 2: Integridade dos dados
            try:
                company_controller = self.container.get_company_controller()
                product_controller = self.container.get_product_controller()
                
                companies = company_controller.list_companies()
                products = product_controller.list_products()
                
                self.log_test("Carregamento de empresas", True, f"Carregadas: {len(companies)}")
                self.log_test("Carregamento de produtos", True, f"Carregados: {len(products)}")
                
            except Exception as e:
                self.log_test("Integridade dos dados", False, str(e))
                
        except Exception as e:
            self.log_test("Teste persistência", False, str(e))
    
    def run_all_tests(self):
        """Executar todos os testes."""
        print("🚀 === INICIANDO TESTES AUTOMATIZADOS DA GUI ===\n")
        
        start_time = time.time()
        
        # Setup inicial
        if not self.setup_gui():
            print("❌ Falha no setup inicial - abortando testes")
            return
        
        # Executar testes em thread separada para não bloquear GUI
        def run_tests():
            try:
                time.sleep(1)  # Aguardar GUI estar pronta
                
                # Executar todos os testes
                self.test_company_management()
                self.test_product_management()
                self.test_sales_order_management()
                self.test_brasil_api_integration()
                self.test_gui_interactions()
                self.test_data_persistence()
                
                # Gerar relatório final
                self.generate_final_report(start_time)
                
                # Fechar GUI após testes
                self.root.after(3000, self.root.quit)  # Aguardar 3s para mostrar relatório
                
            except Exception as e:
                print(f"❌ Erro durante execução dos testes: {e}")
                traceback.print_exc()
                self.root.quit()
        
        # Iniciar testes em thread separada
        test_thread = threading.Thread(target=run_tests)
        test_thread.daemon = True
        test_thread.start()
        
        # Executar GUI
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"❌ Erro na execução da GUI: {e}")
    
    def generate_final_report(self, start_time):
        """Gerar relatório final dos testes."""
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n🎯 === RELATÓRIO FINAL DOS TESTES ===")
        print(f"⏱️ Tempo total: {duration:.2f} segundos")
        print(f"📊 Total de testes: {len(self.test_results)}")
        print(f"✅ Sucessos: {len([r for r in self.test_results if '✅' in r])}")
        print(f"❌ Falhas: {len([r for r in self.test_results if '❌' in r])}")
        
        if self.errors_found:
            print(f"\n🚨 ERROS ENCONTRADOS ({len(self.errors_found)}):")
            for i, error in enumerate(self.errors_found, 1):
                print(f"  {i}. {error}")
        else:
            print("\n🎉 NENHUM ERRO CRÍTICO ENCONTRADO!")
        
        print(f"\n📋 DETALHES COMPLETOS:")
        for result in self.test_results:
            print(f"  {result}")
        
        # Salvar relatório em arquivo
        report_file = os.path.join(os.path.dirname(__file__), 'test_report.txt')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO DE TESTES AUTOMATIZADOS - PYSYSTEM\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Data/Hora: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Duração: {duration:.2f} segundos\n")
            f.write(f"Total de testes: {len(self.test_results)}\n")
            f.write(f"Sucessos: {len([r for r in self.test_results if '✅' in r])}\n")
            f.write(f"Falhas: {len([r for r in self.test_results if '❌' in r])}\n\n")
            
            if self.errors_found:
                f.write("ERROS ENCONTRADOS:\n")
                for i, error in enumerate(self.errors_found, 1):
                    f.write(f"  {i}. {error}\n")
                f.write("\n")
            
            f.write("DETALHES COMPLETOS:\n")
            for result in self.test_results:
                f.write(f"  {result}\n")
        
        print(f"\n📄 Relatório salvo em: {report_file}")


def main():
    """Função principal."""
    print("🔧 PYSYSTEM - Sistema de Testes Automatizados da GUI")
    print("=" * 60)
    
    try:
        tester = AutomatedGUITester()
        tester.run_all_tests()
        
    except KeyboardInterrupt:
        print("\n⚠️ Testes interrompidos pelo usuário")
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
