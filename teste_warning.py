#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para investigar o warning do prompt_toolkit/layout/containers.py
"""

import os
import sys
from rich.console import Console
from dialogos_tui import message_dialog, yes_no_dialog

# Configurar console para saída formatada
console = Console()


def testar_dialogo_com_texto_longo():
    """Testa diálogos com textos longos para tentar reproduzir o warning"""
    console.print("[bold green]Testando diálogo com texto longo[/bold green]")
    
    # Criar texto longo com quebras de linha
    texto_longo = (
        "Este é um texto muito longo para testar o comportamento do diálogo.\n"
        "Ele contém múltiplas linhas e caracteres especiais para tentar reproduzir o warning.\n"
        "O warning parece estar relacionado ao cálculo da largura dos caracteres (char_width).\n"
        "Vamos tentar incluir caracteres especiais como: áéíóúçãõâêîôû\n"
        "E também alguns símbolos: ☺☻♥♦♣♠•◘○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼\n"
        "Além de texto muito longo que pode causar problemas de quebra de linha e cálculo de largura."
    )
    
    # Testar diálogo de mensagem com texto longo
    console.print("[cyan]Testando diálogo de mensagem com texto longo...[/cyan]")
    message_dialog(
        title="Teste de Diálogo com Texto Longo",
        text=texto_longo
    ).run()
    
    # Testar diálogo de confirmação com texto longo
    console.print("[cyan]Testando diálogo de confirmação com texto longo...[/cyan]")
    resultado = yes_no_dialog(
        title="Confirmação com Texto Longo",
        text=texto_longo,
        yes_text="Sim, entendi",
        no_text="Não, não entendi"
    ).run()
    
    console.print(f"Resultado do diálogo de confirmação: {resultado}")


def testar_dialogo_com_largura_variavel():
    """Testa diálogos com larguras variáveis para tentar reproduzir o warning"""
    console.print("\n[bold green]Testando diálogo com largura variável[/bold green]")
    
    # Criar texto com linhas de tamanhos diferentes
    texto_variavel = (
        "Linha curta\n"
        "Esta é uma linha um pouco mais longa\n"
        "Esta é uma linha muito mais longa que provavelmente vai precisar quebrar em várias linhas\n"
        "E"
    )
    
    # Testar diálogo de mensagem com texto de largura variável
    console.print("[cyan]Testando diálogo de mensagem com largura variável...[/cyan]")
    message_dialog(
        title="Teste de Largura Variável",
        text=texto_variavel
    ).run()


def capturar_warnings():
    """Configura captura de warnings para análise"""
    import warnings
    import io
    
    # Configurar captura de warnings
    warning_stream = io.StringIO()
    warnings.filterwarnings("always")
    
    # Redirecionar warnings para nosso stream
    old_showwarning = warnings.showwarning
    
    def custom_showwarning(message, category, filename, lineno, file=None, line=None):
        warning_stream.write(f"WARNING: {message}\n")
        warning_stream.write(f"  File: {filename}, Line: {lineno}\n")
        old_showwarning(message, category, filename, lineno, file, line)
    
    warnings.showwarning = custom_showwarning
    
    return warning_stream


def executar_testes():
    """Executa todos os testes e captura warnings"""
    console.print("[bold magenta]Iniciando testes para investigar warning[/bold magenta]")
    console.print("=" * 60)
    
    # Configurar captura de warnings
    warning_stream = capturar_warnings()
    
    # Executar testes
    testar_dialogo_com_texto_longo()
    testar_dialogo_com_largura_variavel()
    
    # Exibir warnings capturados
    console.print("\n[bold yellow]Warnings capturados:[/bold yellow]")
    warnings = warning_stream.getvalue()
    if warnings:
        console.print(warnings)
    else:
        console.print("Nenhum warning foi capturado durante os testes.")


if __name__ == "__main__":
    executar_testes()
