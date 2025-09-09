#!/usr/bin/env python3
"""
Sistema de Testes Avançados com Simulação de Cliques
Simula interações reais do usuário na interface gráfica
"""

import sys
import os
import time
import threading
import tkinter as tk
from tkinter import ttk
from decimal import Decimal
import traceback

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.presentation.gui.main_window import MainWindow
from src.presentation.gui.dependency_injection import DependencyContainer


class AdvancedGUITester:
    """Testador avançado com simulação de cliques."""
    
    def __init__(self):
        """Inicializar testador."""
        self.test_results = []
        self.errors_found = []
        self.root = None
        self.app = None
        
    def log_test(self, test_name, success, details=""):
        """Registrar resultado do teste."""
        status = "✅ PASS" if success else "❌ FAIL"
        result = f"{status} - {test_name}"
        
        if details:
            result += f" | {details}"
            
        if not success:
            self.errors_found.append(f"{test_name}: {details}")
            
        self.test_results.append(result)
        print(result)
    
    def simulate_click(self, widget, event_type='<Button-1>'):
        """Simular clique em widget."""
        try:
            if widget and widget.winfo_exists():
                # Focar no widget
                widget.focus_set()
                self.root.update()
                
                # Simular evento de clique
                event = tk.Event()
                event.widget = widget
                event.x = widget.winfo_width() // 2
                event.y = widget.winfo_height() // 2
                
                widget.event_generate(event_type)
                self.root.update()
                time.sleep(0.1)
                return True
                
        except Exception as e:
            print(f"  Erro ao simular clique: {e}")
            return False
        
        return False
    
    def find_widget_by_text(self, parent, text, widget_type=None):
        """Encontrar widget por texto."""
        def search_recursive(widget):
            try:
                # Verificar se o widget tem o texto procurado
                if hasattr(widget, 'cget'):
                    try:
                        widget_text = widget.cget('text')
                        if text.lower() in str(widget_text).lower():
                            if widget_type is None or isinstance(widget, widget_type):
                                return widget
                    except:
                        pass
                
                # Buscar em filhos
                for child in widget.winfo_children():
                    result = search_recursive(child)
                    if result:
                        return result
                        
            except:
                pass
            
            return None
        
        return search_recursive(parent)
    
    def fill_entry(self, entry_widget, value):
        """Preencher campo de entrada."""
        try:
            if entry_widget and entry_widget.winfo_exists():
                entry_widget.focus_set()
                self.root.update()
                
                # Limpar campo
                entry_widget.delete(0, tk.END)
                self.root.update()
                
                # Inserir valor
                entry_widget.insert(0, str(value))
                self.root.update()
                
                # Simular evento de validação
                entry_widget.event_generate('<KeyRelease>')
                self.root.update()
                
                return True
                
        except Exception as e:
            print(f"  Erro ao preencher campo: {e}")
            return False
        
        return False
    
    def test_company_form_interactions(self):
        """Testar interações do formulário de empresas."""
        print("\n🏢 === TESTANDO FORMULÁRIO DE EMPRESAS ===")
        
        try:
            # Procurar aba de empresas
            companies_tab = None
            if hasattr(self.app, 'notebook'):
                notebook = self.app.notebook
                for i in range(notebook.index('end')):
                    tab_text = notebook.tab(i, 'text')
                    if 'empres' in tab_text.lower() or 'compan' in tab_text.lower():
                        notebook.select(i)
                        self.root.update()
                        companies_tab = notebook.nametowidget(notebook.select())
                        break
            
            if not companies_tab:
                self.log_test("Encontrar aba Empresas", False, "Aba não encontrada")
                return
            
            self.log_test("Encontrar aba Empresas", True)
            
            # Procurar botão "New" ou "Novo"
            new_button = self.find_widget_by_text(companies_tab, "New", tk.Button)
            if not new_button:
                new_button = self.find_widget_by_text(companies_tab, "Novo", tk.Button)
            
            if new_button:
                self.log_test("Encontrar botão Novo", True)
                
                # Simular clique no botão novo
                if self.simulate_click(new_button):
                    self.log_test("Clique em Novo", True)
                    time.sleep(0.5)  # Aguardar dialog abrir
                    
                    # Procurar campos do formulário
                    self.test_form_fields()
                    
                else:
                    self.log_test("Clique em Novo", False)
            else:
                self.log_test("Encontrar botão Novo", False, "Botão não encontrado")
                
        except Exception as e:
            self.log_test("Teste formulário empresas", False, str(e))
            traceback.print_exc()
    
    def test_form_fields(self):
        """Testar preenchimento de campos do formulário."""
        try:
            # Aguardar um pouco para dialog aparecer
            time.sleep(1)
            self.root.update()
            
            # Procurar campos comuns
            test_data = {
                'nome': 'Empresa Teste GUI',
                'cnpj': '11.222.333/0001-89',
                'cep': '01310-100',
                'email': 'teste@gui.com',
                'telefone': '(11) 99999-9999'
            }
            
            for field_name, value in test_data.items():
                # Procurar campo por label próximo
                field_found = False
                
                # Buscar em todas as janelas abertas
                for window in self.root.winfo_children():
                    if isinstance(window, (tk.Toplevel, tk.Frame)):
                        entry_widgets = self.find_all_entries(window)
                        
                        for entry in entry_widgets:
                            if self.fill_entry(entry, value):
                                self.log_test(f"Preencher campo {field_name}", True, value)
                                field_found = True
                                break
                        
                        if field_found:
                            break
                
                if not field_found:
                    self.log_test(f"Preencher campo {field_name}", False, "Campo não encontrado")
                    
        except Exception as e:
            self.log_test("Teste campos formulário", False, str(e))
    
    def find_all_entries(self, parent):
        """Encontrar todos os campos de entrada."""
        entries = []
        
        def search_entries(widget):
            if isinstance(widget, (tk.Entry, ttk.Entry)):
                entries.append(widget)
            
            try:
                for child in widget.winfo_children():
                    search_entries(child)
            except:
                pass
        
        search_entries(parent)
        return entries
    
    def test_product_form_interactions(self):
        """Testar interações do formulário de produtos."""
        print("\n📦 === TESTANDO FORMULÁRIO DE PRODUTOS ===")
        
        try:
            # Navegar para aba de produtos
            if hasattr(self.app, 'notebook'):
                notebook = self.app.notebook
                for i in range(notebook.index('end')):
                    tab_text = notebook.tab(i, 'text')
                    if 'product' in tab_text.lower() or 'produto' in tab_text.lower():
                        notebook.select(i)
                        self.root.update()
                        product_tab = notebook.nametowidget(notebook.select())
                        break
            
            if 'product_tab' not in locals():
                self.log_test("Encontrar aba Produtos", False)
                return
            
            self.log_test("Encontrar aba Produtos", True)
            
            # Testar interações similares aos produtos
            new_button = self.find_widget_by_text(product_tab, "New", tk.Button)
            if new_button and self.simulate_click(new_button):
                self.log_test("Clique Novo Produto", True)
                time.sleep(0.5)
                
                # Testar campos específicos de produtos
                product_data = {
                    'sku': 'TEST-GUI-001',
                    'nome': 'Produto Teste GUI',
                    'preco': '199.99',
                    'estoque': '100'
                }
                
                for field, value in product_data.items():
                    # Implementação similar ao teste de empresas
                    pass
                    
            else:
                self.log_test("Clique Novo Produto", False)
                
        except Exception as e:
            self.log_test("Teste formulário produtos", False, str(e))
    
    def test_error_dialogs(self):
        """Testar aparição de diálogos de erro."""
        print("\n🚨 === TESTANDO DIÁLOGOS DE ERRO ===")
        
        try:
            # Tentar operações que podem gerar erros
            
            # Teste 1: Salvar formulário vazio
            save_button = self.find_widget_by_text(self.root, "Save", tk.Button)
            if not save_button:
                save_button = self.find_widget_by_text(self.root, "Salvar", tk.Button)
            
            if save_button:
                if self.simulate_click(save_button):
                    self.log_test("Testar validação formulário", True, "Clique executado")
                    time.sleep(0.5)
                    
                    # Verificar se apareceu dialog de erro
                    self.check_for_error_dialogs()
            
            # Teste 2: Dados inválidos
            # Implementar testes com dados propositalmente inválidos
            
        except Exception as e:
            self.log_test("Teste diálogos erro", False, str(e))
    
    def check_for_error_dialogs(self):
        """Verificar presença de diálogos de erro."""
        try:
            # Verificar se existem janelas de erro ativas
            for child in self.root.winfo_children():
                if isinstance(child, tk.Toplevel):
                    title = child.title().lower()
                    if any(word in title for word in ['error', 'erro', 'warning', 'aviso']):
                        self.log_test("Dialog de erro detectado", True, f"Título: {child.title()}")
                        
                        # Procurar botão OK para fechar
                        ok_button = self.find_widget_by_text(child, "OK", tk.Button)
                        if ok_button:
                            self.simulate_click(ok_button)
                        
                        return True
            
            return False
            
        except Exception as e:
            self.log_test("Verificar diálogos", False, str(e))
            return False
    
    def test_menu_interactions(self):
        """Testar interações com menus."""
        print("\n📋 === TESTANDO MENUS ===")
        
        try:
            # Verificar se existe menu
            if hasattr(self.root, 'config') and 'menu' in self.root.keys():
                menubar = self.root['menu']
                if menubar:
                    self.log_test("Menu encontrado", True)
                    
                    # Testar itens do menu se possível
                    # (implementação mais complexa necessária para menus)
                    
                else:
                    self.log_test("Menu encontrado", False)
            else:
                self.log_test("Menu encontrado", False, "Sem menu configurado")
                
        except Exception as e:
            self.log_test("Teste menus", False, str(e))
    
    def run_advanced_tests(self):
        """Executar todos os testes avançados."""
        print("🚀 === INICIANDO TESTES AVANÇADOS DA GUI ===\n")
        
        # Setup inicial
        try:
            self.root = tk.Tk()
            self.root.title("PYSYSTEM - Testes Avançados")
            self.root.geometry("1200x800+100+100")
            
            self.app = MainWindow(self.root)
            self.root.update()
            
            self.log_test("Setup GUI Avançado", True)
            
        except Exception as e:
            self.log_test("Setup GUI Avançado", False, str(e))
            return
        
        # Executar testes em thread
        def run_tests():
            try:
                time.sleep(2)  # Aguardar GUI estar pronta
                
                self.test_company_form_interactions()
                self.test_product_form_interactions()
                self.test_error_dialogs()
                self.test_menu_interactions()
                
                # Relatório final
                self.generate_report()
                
                # Fechar após relatório
                self.root.after(5000, self.root.quit)
                
            except Exception as e:
                print(f"❌ Erro durante testes: {e}")
                traceback.print_exc()
                self.root.quit()
        
        # Iniciar testes
        test_thread = threading.Thread(target=run_tests)
        test_thread.daemon = True
        test_thread.start()
        
        # Executar GUI
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"❌ Erro na GUI: {e}")
    
    def generate_report(self):
        """Gerar relatório dos testes avançados."""
        print(f"\n🎯 === RELATÓRIO TESTES AVANÇADOS ===")
        print(f"📊 Total: {len(self.test_results)}")
        print(f"✅ Sucessos: {len([r for r in self.test_results if '✅' in r])}")
        print(f"❌ Falhas: {len([r for r in self.test_results if '❌' in r])}")
        
        if self.errors_found:
            print(f"\n🚨 ERROS ENCONTRADOS:")
            for error in self.errors_found:
                print(f"  • {error}")
        
        print(f"\n📋 DETALHES:")
        for result in self.test_results:
            print(f"  {result}")


def main():
    """Função principal dos testes avançados."""
    print("🔬 PYSYSTEM - Testes Avançados com Simulação de Cliques")
    print("=" * 65)
    
    try:
        tester = AdvancedGUITester()
        tester.run_advanced_tests()
        
    except KeyboardInterrupt:
        print("\n⚠️ Testes interrompidos")
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
