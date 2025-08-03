#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface TUI para seleção de arquivos
"""

import os
from typing import List, Optional

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style
from estilos_tui import ESTILOS, ESTILO_PROMPT_TOOLKIT


class SeletorArquivoTUI:
    """Interface TUI para seleção de arquivos"""
    
    def __init__(self, diretorio: str = '.'):
        """Inicializa o seletor de arquivos"""
        self.diretorio = diretorio
        self.arquivos = self._listar_arquivos()
        self.total_arquivos = len(self.arquivos)
        self.arquivos_por_pagina = 20
        self.pagina_atual = 0
        self.total_paginas = max(1, (self.total_arquivos + self.arquivos_por_pagina - 1) // self.arquivos_por_pagina)
        self.cursor_pos = 0
        self.resultado = None
    
    def _listar_arquivos(self) -> List[str]:
        """Lista os arquivos no diretório"""
        try:
            return [f for f in os.listdir(self.diretorio) if os.path.isfile(os.path.join(self.diretorio, f))]
        except Exception as e:
            print(f"Erro ao listar arquivos: {e}")
            return []
    
    def obter_arquivos_pagina(self) -> List[str]:
        """Obtém os arquivos da página atual"""
        inicio = self.pagina_atual * self.arquivos_por_pagina
        fim = inicio + self.arquivos_por_pagina
        return self.arquivos[inicio:fim]
    
    def gerar_tabela_formatada(self):
        """Gera a tabela formatada como texto para exibição no prompt_toolkit"""
        # Obter arquivos da página atual
        arquivos_pagina = self.obter_arquivos_pagina()
        
        # Criar linhas formatadas para prompt_toolkit
        linhas = []
        
        # Título
        linhas.append([(ESTILOS['titulo'], f"=== Seleção de Arquivo - Página {self.pagina_atual + 1}/{self.total_paginas} ===")])
        linhas.append([])
        
        # Cabeçalho
        linhas.append([
            (ESTILOS['cabecalho_tabela'], f"{'#':^5}"),
            (ESTILOS['cabecalho_tabela'], f"{'Nome do Arquivo':^40}"),
            (ESTILOS['cabecalho_tabela'], f"{'Tamanho (bytes)':^15}")
        ])
        
        # Separador
        linhas.append([(ESTILOS['separador'], "-" * 65)])
        
        # Conteúdo
        for i, arquivo in enumerate(arquivos_pagina):
            # Verificar se é a linha do cursor
            estilo = ESTILOS['item_selecionado'] if i == self.cursor_pos else ESTILOS['texto_normal']
            
            # Obter tamanho do arquivo
            try:
                tamanho = os.path.getsize(os.path.join(self.diretorio, arquivo))
            except:
                tamanho = 0
            
            linhas.append([
                (estilo, f"{i + 1:^5}"),
                (estilo, f"{arquivo:<40}"),
                (estilo, f"{tamanho:>15}")
            ])
        
        # Informações adicionais
        linhas.append([])
        if self.total_arquivos == 0:
            linhas.append([(ESTILOS['texto_erro'], "Nenhum arquivo encontrado no diretório.")])
        else:
            linhas.append([(ESTILOS['texto_normal'], f"Total de arquivos: {self.total_arquivos}")])
        
        linhas.append([])
        linhas.append([(ESTILOS['ajuda'], "Teclas: ↑/↓: Navegar | PgUp/PgDn: Mudar página | Enter: Selecionar | q: Cancelar")])
        
        # Formatar como uma única lista plana de tuplas (estilo, texto)
        resultado = []
        for linha in linhas:
            for item in linha:
                resultado.append(item)
            resultado.append(("", "\n"))
        
        return resultado
    
    def navegar_cursor(self, direcao: str):
        """Navega o cursor na página atual"""
        arquivos_pagina = self.obter_arquivos_pagina()
        
        if direcao == "cima" and self.cursor_pos > 0:
            self.cursor_pos -= 1
        elif direcao == "baixo" and self.cursor_pos < len(arquivos_pagina) - 1:
            self.cursor_pos += 1
        elif direcao == "pagina_cima" and self.pagina_atual > 0:
            self.pagina_atual -= 1
            self.cursor_pos = 0
        elif direcao == "pagina_baixo" and self.pagina_atual < self.total_paginas - 1:
            self.pagina_atual += 1
            self.cursor_pos = 0
    
    def executar(self) -> Optional[str]:
        """Executa a interface interativa do seletor de arquivos"""
        # Se não houver arquivos, retornar None
        if not self.arquivos:
            return None
        
        # Criar bindings de teclas
        bindings = KeyBindings()
        
        @bindings.add('q')
        def _(event):
            """Cancelar seleção"""
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
        
        @bindings.add('enter')
        def _(event):
            """Selecionar arquivo"""
            arquivos_pagina = self.obter_arquivos_pagina()
            if 0 <= self.cursor_pos < len(arquivos_pagina):
                indice_global = self.pagina_atual * self.arquivos_por_pagina + self.cursor_pos
                if indice_global < self.total_arquivos:
                    self.resultado = self.arquivos[indice_global]
                    event.app.exit()
        
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
            full_screen=True,
            style=ESTILO_PROMPT_TOOLKIT
        )
        
        app.run()
        return self.resultado


def selecionar_arquivo_tui(diretorio: str = '.') -> Optional[str]:
    """Função auxiliar para selecionar um arquivo usando a interface TUI"""
    seletor = SeletorArquivoTUI(diretorio)
    return seletor.executar()


if __name__ == "__main__":
    # Teste da interface
    arquivo_selecionado = selecionar_arquivo_tui()
    if arquivo_selecionado:
        print(f"Arquivo selecionado: {arquivo_selecionado}")
    else:
        print("Nenhum arquivo selecionado.")
