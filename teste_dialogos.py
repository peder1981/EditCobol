#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar os diálogos padronizados
"""

from dialogos_tui import message_dialog, yes_no_dialog
from prompt_toolkit.shortcuts import message_dialog as pt_message_dialog
from prompt_toolkit.shortcuts import yes_no_dialog as pt_yes_no_dialog


def testar_dialogos_padronizados():
    """Testa os diálogos padronizados vs os originais do prompt_toolkit"""
    print("Testando diálogos padronizados vs originais do prompt_toolkit")
    
    # Primeiro teste: diálogo original do prompt_toolkit
    print("\n1. Exibindo diálogo original do prompt_toolkit...")
    pt_message_dialog(
        title="Diálogo Original",
        text="Este é um diálogo de mensagem original do prompt_toolkit."
    ).run()
    
    # Segundo teste: nosso diálogo padronizado
    print("\n2. Exibindo diálogo padronizado...")
    message_dialog(
        title="Diálogo Padronizado",
        text="Este é um diálogo de mensagem padronizado com nosso estilo."
    ).run()
    
    # Terceiro teste: diálogo de confirmação original
    print("\n3. Exibindo diálogo de confirmação original...")
    resultado_original = pt_yes_no_dialog(
        title="Confirmação Original",
        text="Este é um diálogo de confirmação original do prompt_toolkit. Deseja continuar?",
        yes_text="Sim",
        no_text="Não"
    ).run()
    
    # Quarto teste: nosso diálogo de confirmação padronizado
    print("\n4. Exibindo diálogo de confirmação padronizado...")
    resultado_padronizado = yes_no_dialog(
        title="Confirmação Padronizada",
        text="Este é um diálogo de confirmação padronizado com nosso estilo. Deseja continuar?",
        yes_text="Sim",
        no_text="Não"
    ).run()
    
    # Exibir resultados
    print(f"\nResultado do diálogo original: {resultado_original}")
    print(f"Resultado do diálogo padronizado: {resultado_padronizado}")


if __name__ == "__main__":
    testar_dialogos_padronizados()
