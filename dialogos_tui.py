#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de diálogos padronizados para a aplicação
Implementa diálogos com estilo visual consistente com o resto da aplicação
"""

from prompt_toolkit.shortcuts import message_dialog as pt_message_dialog
from prompt_toolkit.shortcuts import yes_no_dialog as pt_yes_no_dialog
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style
import os


def message_dialog(title="Mensagem", text="", style=None):
    """
    Exibe um diálogo de mensagem simples
    
    Args:
        title: Título do diálogo
        text: Texto da mensagem
        style: Estilo opcional (não usado, mantido para compatibilidade)
    
    Returns:
        Resultado do diálogo
    """
    # Versão simplificada que garante visibilidade
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"=== {title} ===")
    print(f"\n{text}\n")
    input("Pressione Enter para continuar...")
    return None


def yes_no_dialog(title="Confirmação", text="", yes_text="Sim", no_text="Não", style=None):
    """
    Exibe um diálogo de confirmação simples
    
    Args:
        title: Título do diálogo
        text: Texto da pergunta
        yes_text: Texto do botão de confirmação
        no_text: Texto do botão de negação
        style: Estilo opcional (não usado, mantido para compatibilidade)
    
    Returns:
        Resultado do diálogo (True para sim, False para não)
    """
    # Versão simplificada que garante visibilidade
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"=== {title} ===")
        print(f"\n{text}\n")
        resposta = input(f"{yes_text}/{no_text} [s/n]: ").strip().lower()
        if resposta in ['s', 'sim', 'y', 'yes']:
            return True
        elif resposta in ['n', 'não', 'nao', 'no']:
            return False
        print("\nPor favor, digite 's' para Sim ou 'n' para Não.")
        input("Pressione Enter para tentar novamente...")


if __name__ == "__main__":
    # Teste dos diálogos
    resultado = yes_no_dialog(
        title="Teste de Diálogo",
        text="Este é um diálogo de teste. Deseja continuar?"
    )
    
    if resultado:
        message_dialog(
            title="Resultado",
            text="Você escolheu continuar!"
        )
    else:
        message_dialog(
            title="Resultado",
            text="Você escolheu cancelar!"
        )
