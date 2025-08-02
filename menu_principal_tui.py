#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Menu principal da aplicação usando interface TUI com prompt_toolkit
"""

import os
import sys
from prompt_toolkit import Application
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous

class MenuPrincipalTUI:
    """Interface TUI para o menu principal da aplicação"""
    
    def __init__(self, arquivo_atual=None):
        """Inicializa o menu principal"""
        self.arquivo_atual = arquivo_atual
        self.opcoes = [
            ("Carregar arquivo", self._carregar_arquivo),
            ("Visualizar conteúdo", self._visualizar_conteudo),
            ("Editar registro", self._editar_registro),
            ("Deletar registro", self._deletar_registro),
            ("Excluir por adquirente", self._excluir_por_adquirente),
            ("Seleção por valor", self._selecionar_por_valor),
            ("Escolher registros", self._escolher_registros),
            ("Visualizar como planilha", self._visualizar_planilha),
            ("Salvar", self._salvar),
            ("Salvar como...", self._salvar_como),
            ("Fechar arquivo", self._fechar_arquivo),
            ("Sair", self._sair)
        ]
        self.cursor_pos = 0
        self.saida = False
        self.resultado = None
    
    def gerar_menu_formatado(self):
        """Gera o menu formatado para exibição no prompt_toolkit"""
        linhas = []
        
        # Título
        linhas.append([("bold", "=== Editor de Arquivo de Movimentação Financeira ===")])
        linhas.append([])
        
        # Status do arquivo
        if self.arquivo_atual:
            nome_arquivo = os.path.basename(self.arquivo_atual.caminho_arquivo or "Sem nome")
            total_registros = len(self.arquivo_atual.movimentos)
            linhas.append([("fg:ansigreen", f"Arquivo atual: {nome_arquivo} ({total_registros} registros)")])
        else:
            linhas.append([("fg:ansired", "Nenhum arquivo carregado")])
        
        linhas.append([])
        linhas.append([("fg:ansiblue", "Menu de Opções:")])
        linhas.append([])
        
        # Opções do menu
        for i, (texto, _) in enumerate(self.opcoes):
            # Desabilitar opções que requerem arquivo carregado
            desabilitado = not self.arquivo_atual and i > 0 and i < len(self.opcoes) - 1
            
            # Estilo baseado na posição do cursor e estado
            if i == self.cursor_pos:
                estilo = "reverse"
            elif desabilitado:
                estilo = "fg:ansigray"
            else:
                estilo = ""
            
            linhas.append([(estilo, f" {i+1}. {texto}")])
        
        linhas.append([])
        linhas.append([("fg:ansiwhite", "Teclas: ↑/↓: Navegar | Enter: Selecionar | q: Sair")])
        
        # Formatar como uma única lista plana de tuplas (estilo, texto)
        resultado = []
        for linha in linhas:
            if linha:  # Se a linha não estiver vazia
                resultado.extend(linha)
            resultado.append(('', '\n'))  # Adicionar quebra de linha após cada linha
        
        return resultado
    
    def executar(self):
        """Executa o menu principal"""
        # Criar controle de texto formatado
        text_control = FormattedTextControl(lambda: self.gerar_menu_formatado())
        
        # Criar janela simples
        window = Window(
            content=text_control,
            wrap_lines=False
        )
        
        # Criar layout
        layout = Layout(HSplit([window]))
        
        # Configurar teclas
        bindings = KeyBindings()
        
        @bindings.add('up')
        def move_cursor_up(event):
            self.cursor_pos = max(0, self.cursor_pos - 1)
        
        @bindings.add('down')
        def move_cursor_down(event):
            self.cursor_pos = min(len(self.opcoes) - 1, self.cursor_pos + 1)
        
        @bindings.add('enter')
        def select_option(event):
            # Verificar se a opção requer arquivo carregado
            if not self.arquivo_atual and self.cursor_pos > 0 and self.cursor_pos < len(self.opcoes) - 1:
                return
            
            # Encerrar a aplicação e executar a função da opção selecionada
            event.app.exit()
            _, funcao = self.opcoes[self.cursor_pos]
            self.resultado = funcao()
        
        @bindings.add('q')
        def exit_app(event):
            event.app.exit()
            self.resultado = self._sair()
        
        # Criar e executar aplicação
        app = Application(
            layout=layout,
            key_bindings=bindings,
            full_screen=True
        )
        
        app.run()
        return self.resultado
    
    # Funções para cada opção do menu
    def _carregar_arquivo(self):
        return ("carregar_arquivo", None)
    
    def _visualizar_conteudo(self):
        return ("visualizar_conteudo", None)
    
    def _editar_registro(self):
        return ("editar_registro", None)
    
    def _deletar_registro(self):
        return ("deletar_registro", None)
    
    def _excluir_por_adquirente(self):
        return ("excluir_por_adquirente", None)
    
    def _selecionar_por_valor(self):
        return ("selecionar_por_valor", None)
    
    def _escolher_registros(self):
        return ("escolher_registros", None)
    
    def _visualizar_planilha(self):
        return ("visualizar_planilha", None)
    
    def _salvar(self):
        return ("salvar", None)
    
    def _salvar_como(self):
        return ("salvar_como", None)
    
    def _fechar_arquivo(self):
        return ("fechar_arquivo", None)
    
    def _sair(self):
        return ("sair", None)

# Função para teste
if __name__ == "__main__":
    menu = MenuPrincipalTUI()
    resultado = menu.executar()
    print(f"Opção selecionada: {resultado}")
