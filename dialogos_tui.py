#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de diálogos padronizados para a aplicação
Implementa diálogos com estilo visual consistente com o resto da aplicação
"""

from prompt_toolkit.shortcuts import message_dialog as pt_message_dialog
from prompt_toolkit.shortcuts import yes_no_dialog as pt_yes_no_dialog
from prompt_toolkit.formatted_text import FormattedText
from estilos_tui import CORES, ESTILOS, ESTILO_PROMPT_TOOLKIT


def message_dialog(title="Mensagem", text="", style=None):
    """
    Exibe um diálogo de mensagem com estilo padronizado
    
    Args:
        title: Título do diálogo
        text: Texto da mensagem
        style: Estilo opcional (usa o estilo padrão da aplicação se None)
    
    Returns:
        Resultado do diálogo
    """
    # Usar o estilo global da aplicação
    if style is None:
        style = ESTILO_PROMPT_TOOLKIT
    
    # Formatar título e texto com estilos padronizados
    formatted_title = FormattedText([(ESTILOS['titulo'], title)])
    formatted_text = FormattedText([(ESTILOS['texto_normal'], text)])
    
    # Criar e exibir o diálogo
    return pt_message_dialog(
        title=formatted_title,
        text=formatted_text,
        style=style,
        ok_text="OK"
    )


def yes_no_dialog(title="Confirmação", text="", yes_text="Sim", no_text="Não", style=None):
    """
    Exibe um diálogo de confirmação com estilo padronizado
    
    Args:
        title: Título do diálogo
        text: Texto da pergunta
        yes_text: Texto do botão de confirmação
        no_text: Texto do botão de negação
        style: Estilo opcional (usa o estilo padrão da aplicação se None)
    
    Returns:
        Resultado do diálogo (True para sim, False para não)
    """
    # Usar o estilo global da aplicação
    if style is None:
        style = ESTILO_PROMPT_TOOLKIT
    
    # Formatar título e texto com estilos padronizados
    formatted_title = FormattedText([(ESTILOS['titulo'], title)])
    formatted_text = FormattedText([(ESTILOS['texto_normal'], text)])
    
    # Criar e exibir o diálogo
    return pt_yes_no_dialog(
        title=formatted_title,
        text=formatted_text,
        style=style,
        yes_text=yes_text,
        no_text=no_text
    )


if __name__ == "__main__":
    # Teste dos diálogos
    resultado = yes_no_dialog(
        title="Teste de Diálogo",
        text="Este é um diálogo de teste. Deseja continuar?"
    ).run()
    
    if resultado:
        message_dialog(
            title="Resultado",
            text="Você escolheu continuar!"
        ).run()
    else:
        message_dialog(
            title="Resultado",
            text="Você escolheu cancelar!"
        ).run()
