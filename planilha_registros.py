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
        self.acao_executada = None
        
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
    
    def gerar_cabecalho(self):
        """Gera o cabeçalho da tabela"""
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
        
        # Formatar como uma única lista plana de tuplas (estilo, texto)
        resultado = []
        for linha in linhas:
            if linha:  # Se a linha não estiver vazia
                resultado.extend(linha)
            resultado.append(('', '\n'))  # Adicionar quebra de linha após cada linha
        
        return resultado
    
    def gerar_registros(self):
        """Gera a área de registros da tabela (parte paginada)"""
        # Obter registros da página atual
        registros_pagina = self.obter_registros_pagina()
        
        # Criar linhas formatadas para prompt_toolkit
        linhas = []
        
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
        
        # Formatar como uma única lista plana de tuplas (estilo, texto)
        resultado = []
        for linha in linhas:
            if linha:  # Se a linha não estiver vazia
                resultado.extend(linha)
            resultado.append(('', '\n'))  # Adicionar quebra de linha após cada linha
        
        return resultado
    
    def gerar_rodape(self):
        """Gera o rodapé da tabela com totalizadores, teclas e ações rápidas"""
        linhas = []
        
        # Separador antes do rodapé
        separador = [("fg:ansiblue", "-" * 85)]
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
            linhas.append([])
            linhas.append([("fg:ansiyellow", "Ações rápidas:")])
            linhas.append([("fg:ansiwhite", "F2: Editar registro atual | F3: Excluir selecionados | F4: Manter selecionados")])
            linhas.append([("fg:ansiwhite", "F5: Selecionar por valor | F6: Excluir por adquirente | F7: Salvar | F8: Salvar como")])
        
        # Formatar como uma única lista plana de tuplas (estilo, texto)
        resultado = []
        for linha in linhas:
            if linha:  # Se a linha não estiver vazia
                resultado.extend(linha)
            resultado.append(('', '\n'))  # Adicionar quebra de linha após cada linha
        
        return resultado
        
    def gerar_tabela_formatada(self):
        """Gera a tabela formatada como texto simples para exibição no prompt_toolkit"""
        # Este método está mantido por compatibilidade, mas não é mais usado diretamente
        resultado = []
        resultado.extend(self.gerar_cabecalho())
        resultado.extend(self.gerar_registros())
        resultado.extend(self.gerar_rodape())
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
        self.acao_executada = None
        
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
        
        # Teclas de função para ações diretas
        @bindings.add('f2')
        def _(event):
            """Editar registro atual"""
            if self.modo_somente_leitura:
                return
                
            # Obter índice global do registro sob o cursor
            indice_global = self.pagina_atual * self.registros_por_pagina + self.cursor_pos
            if indice_global < self.total_registros:
                self.resultado = {"acao": "editar", "indice": indice_global}
                self.acao_executada = "editar"
                event.app.exit()
        
        @bindings.add('f3')
        def _(event):
            """Excluir registros selecionados"""
            if self.modo_somente_leitura or not self.registros_selecionados:
                return
                
            event.app.exit()
            self.excluir_selecionados()
            self.acao_executada = "excluir"
        
        @bindings.add('f4')
        def _(event):
            """Manter apenas registros selecionados"""
            if self.modo_somente_leitura or not self.registros_selecionados:
                return
                
            event.app.exit()
            self.manter_apenas_selecionados()
            self.acao_executada = "manter"
        
        @bindings.add('f5')
        def _(event):
            """Selecionar por valor"""
            if self.modo_somente_leitura:
                return
                
            event.app.exit()
            self.resultado = {"acao": "selecionar_por_valor"}
            self.acao_executada = "selecionar_por_valor"
        
        @bindings.add('f6')
        def _(event):
            """Excluir por adquirente"""
            if self.modo_somente_leitura:
                return
                
            event.app.exit()
            self.resultado = {"acao": "excluir_por_adquirente"}
            self.acao_executada = "excluir_por_adquirente"
        
        @bindings.add('f7')
        def _(event):
            """Salvar arquivo"""
            if self.modo_somente_leitura:
                return
                
            event.app.exit()
            self.resultado = {"acao": "salvar"}
            self.acao_executada = "salvar"
        
        @bindings.add('f8')
        def _(event):
            """Salvar como"""
            if self.modo_somente_leitura:
                return
                
            event.app.exit()
            self.resultado = {"acao": "salvar_como"}
            self.acao_executada = "salvar_como"
        
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
            
            # No modo normal, definir resultado para mostrar menu de operações
            if self.registros_selecionados:
                self.resultado = {"acao": "menu_operacoes"}
            event.app.exit()
        
        # Criar controles para cada seção
        cabecalho_control = FormattedTextControl(lambda: self.gerar_cabecalho())
        registros_control = FormattedTextControl(lambda: self.gerar_registros())
        rodape_control = FormattedTextControl(lambda: self.gerar_rodape())
        
        # Criar janelas para cada seção
        cabecalho_window = Window(
            content=cabecalho_control,
            wrap_lines=False,
            height=5  # Altura fixa para o cabeçalho
        )
        
        registros_window = Window(
            content=registros_control,
            wrap_lines=False
        )
        
        rodape_window = Window(
            content=rodape_control,
            wrap_lines=False,
            height=10  # Altura fixa para o rodapé
        )
        
        # Criar layout com áreas fixas e área paginada
        root_container = HSplit([
            cabecalho_window,
            registros_window,
            rodape_window
        ])
        
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
        """Exibe menu de operações em lote usando prompt_toolkit"""
        # Verificar se há registros selecionados
        if not self.registros_selecionados:
            from prompt_toolkit.shortcuts import message_dialog
            message_dialog(
                title="Aviso",
                text="Nenhum registro selecionado. Selecione registros usando a tecla de espaço.",
            ).run()
            return
            
        from prompt_toolkit import Application
        from prompt_toolkit.layout import Layout, HSplit, Window
        from prompt_toolkit.layout.controls import FormattedTextControl
        from prompt_toolkit.key_binding import KeyBindings
        from prompt_toolkit.formatted_text import FormattedText
        
        # Definir opções do menu
        opcoes = [
            "Excluir registros selecionados",
            "Manter apenas registros selecionados",
            "Voltar"
        ]
        
        # Inicializar seleção
        opcao_selecionada = [0]  # Lista para permitir modificação dentro das funções
        resultado = [None]  # Lista para armazenar resultado
        
        # Função para renderizar o menu
        def renderizar_menu():
            titulo = FormattedText([("fg:ansiyellow bold", "\n  Operações em Lote\n")])
            info = FormattedText([("fg:ansiwhite", f"  Registros selecionados: {len(self.registros_selecionados)}\n\n")])
            
            # Formatar opções
            opcoes_formatadas = []
            for i, opcao in enumerate(opcoes):
                if i == opcao_selecionada[0]:
                    # Opção selecionada
                    opcoes_formatadas.append(("fg:ansigreen reverse", f"  > {opcao}\n"))
                else:
                    # Opção normal
                    opcoes_formatadas.append(("fg:ansiwhite", f"    {opcao}\n"))
            
            # Adicionar instruções
            instrucoes = FormattedText([("fg:ansiwhite", "\n  Use as setas para navegar e Enter para selecionar")])
            
            # Combinar tudo
            return titulo + info + FormattedText(opcoes_formatadas) + instrucoes
        
        # Criar controle de texto formatado
        controle_texto = FormattedTextControl(renderizar_menu)
        
        # Criar janela
        janela = Window(content=controle_texto)
        
        # Criar layout
        layout = Layout(HSplit([janela]))
        
        # Criar bindings de teclas
        bindings = KeyBindings()
        
        @bindings.add('up')
        def _(event):
            """Navegar para cima"""
            opcao_selecionada[0] = max(0, opcao_selecionada[0] - 1)
            controle_texto.text = renderizar_menu()
        
        @bindings.add('down')
        def _(event):
            """Navegar para baixo"""
            opcao_selecionada[0] = min(len(opcoes) - 1, opcao_selecionada[0] + 1)
            controle_texto.text = renderizar_menu()
        
        @bindings.add('enter')
        def _(event):
            """Selecionar opção"""
            resultado[0] = opcao_selecionada[0]
            event.app.exit()
        
        @bindings.add('escape')
        def _(event):
            """Voltar"""
            resultado[0] = len(opcoes) - 1  # Última opção (Voltar)
            event.app.exit()
        
        # Criar e executar aplicação
        app = Application(
            layout=layout,
            key_bindings=bindings,
            full_screen=True,
            mouse_support=True
        )
        
        app.run()
        
        # Processar resultado
        if resultado[0] == 0:  # Excluir registros selecionados
            self.excluir_selecionados()
        elif resultado[0] == 1:  # Manter apenas registros selecionados
            self.manter_apenas_selecionados()
        # Opção 2 (Voltar) não faz nada
    
    def excluir_selecionados(self):
        """Exclui os registros selecionados usando prompt_toolkit"""
        from prompt_toolkit.shortcuts import message_dialog, yes_no_dialog
        
        if not self.registros_selecionados:
            message_dialog(
                title="Aviso",
                text="Nenhum registro selecionado.",
            ).run()
            return
        
        # Confirmação
        confirmado = yes_no_dialog(
            title="Confirmação",
            text=f"Tem certeza que deseja excluir {len(self.registros_selecionados)} registros?",
            yes_text="Sim",
            no_text="Não",
        ).run()
        
        if not confirmado:
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
        
        # Mensagem de sucesso
        message_dialog(
            title="Sucesso",
            text=f"{len(indices_ordenados)} registros excluídos com sucesso.",
        ).run()
    
    def manter_apenas_selecionados(self):
        """Mantém apenas os registros selecionados usando prompt_toolkit"""
        from prompt_toolkit.shortcuts import message_dialog, yes_no_dialog
        
        if not self.registros_selecionados:
            message_dialog(
                title="Aviso",
                text="Nenhum registro selecionado.",
            ).run()
            return
        
        # Confirmação
        confirmado = yes_no_dialog(
            title="Confirmação",
            text=f"Tem certeza que deseja manter apenas {len(self.registros_selecionados)} registros?",
            yes_text="Sim",
            no_text="Não",
        ).run()
        
        if not confirmado:
            return
        
        # Identificar registros a serem mantidos
        indices_manter = set(self.registros_selecionados)
        
        # Identificar registros a serem removidos (em ordem decrescente)
        indices_remover = sorted([i for i in range(len(self.arquivo.movimentos)) 
                                 if i not in indices_manter and self.arquivo.movimentos[i].tipo == 'M'], 
                                reverse=True)
        
        # Remover registros
        for indice in indices_remover:
            del self.arquivo.movimentos[indice]
        
        # Recalcular trailer
        self.arquivo.recalcular_trailer()
        
        # Limpar seleções
        self.registros_selecionados.clear()
        
        # Mensagem de sucesso
        message_dialog(
            title="Sucesso",
            text=f"{len(indices_remover)} registros removidos. {len(indices_manter)} registros mantidos.",
        ).run()


def main():
    """Função principal para testar a planilha"""
    # Esta função será usada para testar a planilha
    # Na integração com o programa principal, será chamada de outra forma
    pass


if __name__ == "__main__":
    main()
