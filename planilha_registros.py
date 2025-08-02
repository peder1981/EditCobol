#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface estilo planilha para seleção e navegação de registros
"""

import os
import sys
from typing import List, Set
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style


class PlanilhaRegistros:
    """Classe para exibir e manipular registros em formato de planilha"""
    
    def __init__(self, arquivo_movimentacao, modo_somente_leitura=False):
        """Inicializa a planilha com os registros do arquivo"""
        self.arquivo = arquivo_movimentacao
        self.registros = arquivo_movimentacao.movimentos
        self.total_registros = len(self.registros)
        self.registros_por_pagina = 50
        self.pagina_atual = 0
        self.total_paginas = max(1, (self.total_registros + self.registros_por_pagina - 1) // self.registros_por_pagina)
        self.cursor_pos = 0
        self.registros_selecionados = set()
        self.filtros = {}
        self.modo_somente_leitura = modo_somente_leitura
        self.console = Console()
        
        # Se não houver registros, ajustar total de páginas
        if self.total_paginas == 0:
            self.total_paginas = 1
    
    def aplicar_filtros(self, registros):
        """Aplica os filtros configurados aos registros"""
        if not self.filtros:
            return registros
        
        registros_filtrados = []
        for registro in registros:
            manter = True
            
            # Filtro por adquirente
            if 'adquirente' in self.filtros and self.filtros['adquirente']:
                if registro.codigo_adquirente != self.filtros['adquirente']:
                    manter = False
            
            # Filtro por data
            if 'data' in self.filtros and self.filtros['data']:
                if registro.data_movimento != self.filtros['data']:
                    manter = False
            
            # Filtro por cartão
            if 'cartao' in self.filtros and self.filtros['cartao']:
                if self.filtros['cartao'] not in registro.numero_cartao:
                    manter = False
            
            # Filtro por CVNSU
            if 'cvnsu' in self.filtros and self.filtros['cvnsu']:
                if self.filtros['cvnsu'] not in registro.cvnsu:
                    manter = False
            
            if manter:
                registros_filtrados.append(registro)
        
        return registros_filtrados
    
    def obter_registros_pagina(self):
        """Obtém os registros da página atual"""
        # Aplicar filtros aos registros
        registros_filtrados = self.aplicar_filtros(self.arquivo.movimentos)
        
        # Calcular índices de início e fim para a página atual
        inicio = self.pagina_atual * self.registros_por_pagina
        fim = inicio + self.registros_por_pagina
        
        # Retornar registros da página atual
        return registros_filtrados[inicio:fim]
    
    def gerar_tabela_formatada(self):
        """Gera a tabela formatada como texto simples para exibição no prompt_toolkit"""
        # Obter registros da página atual
        registros_pagina = self.obter_registros_pagina()
        
        # Criar linhas formatadas para prompt_toolkit
        linhas = []
        
        # Título
        linhas.append([("bold", f"=== Registros de Movimentação - Página {self.pagina_atual + 1}/{self.total_paginas} ===")])
        linhas.append([])
        
        # Cabeçalho
        cabecalho = [
            ("bold", f"{'#':^5}"),
            ("bold", f"{'Sel':^5}"),
            ("bold", f"{'Adquirente':^12}"),
            ("bold", f"{'Data':^10}"),
            ("bold", f"{'Cartão':^22}"),
            ("bold", f"{'Valor':^14}"),
            ("bold", f"{'CVNSU':^11}")
        ]
        linhas.append(cabecalho)
        
        # Separador
        separador = [("fg:ansiblue", "-" * 85)]
        linhas.append(separador)
        
        # Registros
        for i, registro in enumerate(registros_pagina):
            indice_global = self.pagina_atual * self.registros_por_pagina + i
            selecionado = "✓" if indice_global in self.registros_selecionados else " "
            
            # Definir estilo baseado na posição do cursor
            estilo = "reverse" if i == self.cursor_pos else ""
            
            linha = [
                (estilo, f"{indice_global:^5}"),
                (estilo, f"{selecionado:^5}"),
                (estilo, f"{registro.codigo_adquirente:^12}"),
                (estilo, f"{registro.data_movimento:^10}"),
                (estilo, f"{registro.numero_cartao.strip():^22}"),
                (estilo, f"R$ {registro.get_valor_decimal():^10.2f}"),
                (estilo, f"{registro.cvnsu.strip():^11}")
            ]
            linhas.append(linha)
        
        # Se não houver registros, mostrar mensagem
        if not registros_pagina:
            linhas.append([("fg:ansired", "Nenhum registro encontrado")])
        
        # Separador antes do rodapé
        linhas.append([])
        linhas.append(separador)
        linhas.append([])
        
        # Rodapé com informações e ajuda
        total_selecionados = len(self.registros_selecionados)
        linhas.append([("fg:ansigreen bold", f"Registros: {self.total_registros} | Selecionados: {total_selecionados} | Página: {self.pagina_atual + 1}/{self.total_paginas}")])
        
        if self.filtros:
            filtros_ativos = ", ".join([f"{k}={v}" for k, v in self.filtros.items()])
            linhas.append([("fg:ansiyellow", f"Filtros ativos: {filtros_ativos}")])
        
        linhas.append([])
        
        # Ajustar mensagem de ajuda conforme o modo
        if self.modo_somente_leitura:
            linhas.append([("fg:ansiwhite", "Teclas: ↑/↓: Navegar | PgUp/PgDn: Mudar página | Enter: Selecionar | q: Sair")])
        else:
            linhas.append([("fg:ansiwhite", "Teclas: ↑/↓: Navegar | PgUp/PgDn: Mudar página | Espaço: Selecionar | Enter: Menu | q: Sair")])
        
        # Formatar como uma única lista plana de tuplas (estilo, texto)
        resultado = []
        for linha in linhas:
            if linha:  # Se a linha não estiver vazia
                resultado.extend(linha)
            resultado.append(('', '\n'))  # Adicionar quebra de linha após cada linha
        
        return resultado
    
    def navegar_cursor(self, direcao):
        """Navega o cursor na página atual"""
        registros_pagina = self.obter_registros_pagina()
        
        if direcao == "cima" and self.cursor_pos > 0:
            self.cursor_pos -= 1
        elif direcao == "baixo" and self.cursor_pos < len(registros_pagina) - 1:
            self.cursor_pos += 1
        elif direcao == "pagina_cima":
            if self.pagina_atual > 0:
                self.pagina_atual -= 1
                self.cursor_pos = 0
        elif direcao == "pagina_baixo":
            if self.pagina_atual < self.total_paginas - 1:
                self.pagina_atual += 1
                self.cursor_pos = 0
    
    def alternar_selecao(self):
        """Alterna a seleção do registro atual"""
        indice_global = self.pagina_atual * self.registros_por_pagina + self.cursor_pos
        
        if indice_global in self.registros_selecionados:
            self.registros_selecionados.discard(indice_global)
        else:
            self.registros_selecionados.add(indice_global)
    
    def selecionar_todos_visiveis(self):
        """Seleciona todos os registros visíveis na página atual"""
        registros_pagina = self.obter_registros_pagina()
        
        for i in range(len(registros_pagina)):
            indice_global = self.pagina_atual * self.registros_por_pagina + i
            self.registros_selecionados.add(indice_global)
    
    def deselecionar_todos(self):
        """Deseleciona todos os registros"""
        self.registros_selecionados.clear()
    
    def configurar_filtro(self, campo, valor):
        """Configura um filtro para o campo especificado"""
        if valor:
            self.filtros[campo] = valor
        elif campo in self.filtros:
            del self.filtros[campo]
        
        # Recalcular total de páginas após aplicar filtros
        registros_filtrados = self.aplicar_filtros(self.arquivo.movimentos)
        self.total_registros = len(registros_filtrados)
        self.total_paginas = (self.total_registros + self.registros_por_pagina - 1) // self.registros_por_pagina
        
        # Ajustar página atual se necessário
        if self.pagina_atual >= self.total_paginas:
            self.pagina_atual = max(0, self.total_paginas - 1)
        
        # Resetar cursor
        self.cursor_pos = 0
    
    def obter_registros_selecionados(self):
        """Retorna os registros selecionados"""
        return [self.arquivo.movimentos[i] for i in self.registros_selecionados if i < len(self.arquivo.movimentos)]
    
    def executar(self):
        """Executa a interface interativa da planilha usando prompt_toolkit"""
        # Inicializar resultado
        self.resultado = None
        
        # Criar bindings de teclas
        bindings = KeyBindings()
        
        @bindings.add('q')
        def _(event):
            """Sair da aplicação"""
            event.app.exit()
        
        @bindings.add('up')
        def _(event):
            """Navegar para cima"""
            self.navegar_cursor("cima")
            event.app.invalidate()
        
        @bindings.add('down')
        def _(event):
            """Navegar para baixo"""
            self.navegar_cursor("baixo")
            event.app.invalidate()
        
        @bindings.add('pageup')
        def _(event):
            """Navegar para página anterior"""
            self.navegar_cursor("pagina_cima")
            event.app.invalidate()
        
        @bindings.add('pagedown')
        def _(event):
            """Navegar para próxima página"""
            self.navegar_cursor("pagina_baixo")
            event.app.invalidate()
        
        @bindings.add(' ')
        def _(event):
            """Alternar seleção"""
            self.alternar_selecao()
            event.app.invalidate()
        
        @bindings.add('a')
        def _(event):
            """Selecionar todos os registros visíveis"""
            self.selecionar_todos_visiveis()
            event.app.invalidate()
        
        @bindings.add('d')
        def _(event):
            """Deselecionar todos os registros"""
            self.deselecionar_todos()
            event.app.invalidate()
        
        @bindings.add('enter')
        def _(event):
            """Exibir menu de operações ou selecionar registro"""
            # Obter índice global do registro sob o cursor
            indice_global = self.pagina_atual * self.registros_por_pagina + self.cursor_pos
            
            # No modo somente leitura, retornar o registro selecionado
            if self.modo_somente_leitura:
                if indice_global < self.total_registros:
                    self.resultado = {"selecionado": indice_global}
                    event.app.exit()
                return
            
            # No modo normal, mostrar menu de operações
            event.app.exit()
            self.exibir_menu_operacoes()
            # Reiniciar a aplicação após o menu
            self.executar()
        
        # Criar controle de texto formatado
        text_control = FormattedTextControl(lambda: self.gerar_tabela_formatada())
        
        # Criar janela simples
        window = Window(
            content=text_control,
            wrap_lines=False
        )
        
        # Criar layout
        root_container = HSplit([window])
        layout = Layout(root_container)
        
        # Limpar a tela antes de exibir
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Criar e executar aplicação
        app = Application(
            layout=layout,
            key_bindings=bindings,
            full_screen=True
        )
        
        app.run()
        return self.resultado
    
    def exibir_menu_operacoes(self):
        """Exibe menu de operações em lote"""
        # Para o menu de operações, vamos usar a console do rich
        # pois o prompt_toolkit não é ideal para entrada de texto
        self.console.clear()
        self.console.print("Operações em Lote", style="bold underline")
        self.console.print(f"Registros selecionados: {len(self.registros_selecionados)}")
        self.console.print("")
        self.console.print("1. Excluir registros selecionados")
        self.console.print("2. Manter apenas registros selecionados")
        self.console.print("3. Voltar")
        
        opcao = self.console.input("\nEscolha uma opção: ")
        
        if opcao == '1':
            self.excluir_selecionados()
        elif opcao == '2':
            self.manter_apenas_selecionados()
        # Opção 3 apenas volta para a planilha
    
    def excluir_selecionados(self):
        """Exclui os registros selecionados"""
        if not self.registros_selecionados:
            self.console.print("Nenhum registro selecionado.", style="bold red")
            self.console.input("Pressione Enter para continuar...")
            return
        
        confirmacao = self.console.input(f"Tem certeza que deseja excluir {len(self.registros_selecionados)} registros? (s/N): ")
        if confirmacao.lower() != 's':
            return
        
        # Converter para lista ordenada decrescente para evitar problemas de índice
        indices_ordenados = sorted(list(self.registros_selecionados), reverse=True)
        
        # Excluir registros
        for indice in indices_ordenados:
            if indice < len(self.arquivo.movimentos):
                del self.arquivo.movimentos[indice]
        
        # Recalcular trailer
        self.arquivo.recalcular_trailer()
        
        # Limpar seleções
        self.registros_selecionados.clear()
        
        self.console.print(f"{len(indices_ordenados)} registros excluídos com sucesso.", style="bold green")
        self.console.input("Pressione Enter para continuar...")
    
    def manter_apenas_selecionados(self):
        """Mantém apenas os registros selecionados"""
        if not self.registros_selecionados:
            self.console.print("Nenhum registro selecionado.", style="bold red")
            self.console.input("Pressione Enter para continuar...")
            return
        
        confirmacao = self.console.input(f"Tem certeza que deseja manter apenas {len(self.registros_selecionados)} registros? (s/N): ")
        if confirmacao.lower() != 's':
            return
        
        # Converter para conjunto para verificação rápida
        indices_selecionados = set(self.registros_selecionados)
        
        # Excluir registros que NÃO estão selecionados
        for i in range(len(self.arquivo.movimentos) - 1, -1, -1):
            if i not in indices_selecionados:
                del self.arquivo.movimentos[i]
        
        # Recalcular trailer
        self.arquivo.recalcular_trailer()
        
        # Limpar seleções
        self.registros_selecionados.clear()
        
        self.console.print(f"{len(indices_selecionados)} registros mantidos com sucesso.", style="bold green")
        self.console.input("Pressione Enter para continuar...")


def main():
    """Função principal para testar a planilha"""
    # Esta função será usada para testar a planilha
    # Na integração com o programa principal, será chamada de outra forma
    pass


if __name__ == "__main__":
    main()
