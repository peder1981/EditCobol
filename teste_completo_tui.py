#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar todas as funcionalidades da aplicação TUI
Testa menus, diálogos, teclas de função e navegação
"""

import os
import sys
import time
from rich.console import Console

# Importar módulos da aplicação
try:
    from menu_principal_tui import MenuPrincipalTUI
    from seletor_arquivo_tui import SeletorArquivoTUI
    from planilha_registros import PlanilhaRegistros, exibir_planilha_registros
    from dialogos_tui import message_dialog, yes_no_dialog
    from arquivo_movimentacao import ArquivoMovimentacao
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    sys.exit(1)

# Configurar console para saída formatada
console = Console()


def testar_menu_principal():
    """Testa o menu principal da aplicação"""
    console.print("[bold green]Testando Menu Principal[/bold green]")
    
    try:
        menu = MenuPrincipalTUI()
        resultado = menu.executar()
        console.print(f"Resultado do menu principal: {resultado}")
        return True
    except Exception as e:
        console.print(f"[bold red]Erro ao testar menu principal: {e}[/bold red]")
        return False


def testar_seletor_arquivo():
    """Testa o seletor de arquivos"""
    console.print("\n[bold green]Testando Seletor de Arquivos[/bold green]")
    
    try:
        # Definir diretório para teste
        diretorio = os.path.dirname(os.path.abspath(__file__))
        
        seletor = SeletorArquivoTUI(diretorio)
        resultado = seletor.executar()
        console.print(f"Resultado do seletor de arquivos: {resultado}")
        return True
    except Exception as e:
        console.print(f"[bold red]Erro ao testar seletor de arquivos: {e}[/bold red]")
        return False


def testar_planilha_registros():
    """Testa a planilha de registros e suas teclas de função"""
    console.print("\n[bold green]Testando Planilha de Registros[/bold green]")
    
    try:
        # Criar arquivo de teste com alguns registros
        arquivo = ArquivoMovimentacao()
        
        # Adicionar alguns registros de teste
        for i in range(20):
            registro = arquivo.criar_registro_vazio()
            registro.codigo_adquirente = f"{i+1:02d}"
            registro.data_movimento = "01082023"
            registro.numero_cartao = f"1234{i:04d}{'X'*12}"
            registro.valor_bruto = f"{(i+1)*1000:012d}"
            registro.cvnsu = f"NSU{i:05d}"
            arquivo.adicionar_registro(registro)
        
        # Testar planilha em modo normal
        console.print("[cyan]Testando planilha em modo normal[/cyan]")
        planilha = PlanilhaRegistros(arquivo)
        
        # Simular execução e teste das teclas de função
        console.print("[yellow]Simulando execução da planilha...[/yellow]")
        console.print("[yellow]Teclas disponíveis:[/yellow]")
        console.print("  - F2: Editar registro atual")
        console.print("  - F3: Excluir registros selecionados")
        console.print("  - F4: Manter apenas registros selecionados")
        console.print("  - F5: Selecionar por valor")
        console.print("  - F6: Excluir por adquirente")
        console.print("  - F7: Salvar arquivo")
        console.print("  - F8: Salvar como")
        
        # Executar planilha real (comentado para não bloquear o teste)
        # resultado = planilha.executar()
        # console.print(f"Resultado da planilha: {resultado}")
        
        # Testar funções específicas
        console.print("\n[cyan]Testando funções específicas da planilha[/cyan]")
        
        # Testar diálogos
        console.print("[yellow]Testando diálogos da planilha...[/yellow]")
        
        # Testar excluir selecionados (F3)
        console.print("[yellow]Testando função F3 (excluir selecionados)...[/yellow]")
        planilha.registros_selecionados = {0, 1, 2}  # Selecionar alguns registros
        planilha.excluir_selecionados()
        console.print(f"Registros após exclusão: {len(arquivo.movimentos)}")
        
        # Testar manter selecionados (F4)
        console.print("[yellow]Testando função F4 (manter selecionados)...[/yellow]")
        planilha.registros_selecionados = {0, 1, 2}  # Selecionar alguns registros
        planilha.manter_apenas_selecionados()
        console.print(f"Registros após manter: {len(arquivo.movimentos)}")
        
        return True
    except Exception as e:
        console.print(f"[bold red]Erro ao testar planilha de registros: {e}[/bold red]")
        import traceback
        console.print(traceback.format_exc())
        return False


def testar_dialogos():
    """Testa os diálogos padronizados"""
    console.print("\n[bold green]Testando Diálogos Padronizados[/bold green]")
    
    try:
        # Testar diálogo de mensagem
        console.print("[cyan]Testando diálogo de mensagem...[/cyan]")
        message_dialog(
            title="Teste de Diálogo",
            text="Este é um diálogo de mensagem de teste."
        ).run()
        
        # Testar diálogo de confirmação
        console.print("[cyan]Testando diálogo de confirmação...[/cyan]")
        resultado = yes_no_dialog(
            title="Teste de Confirmação",
            text="Este é um diálogo de confirmação de teste. Deseja continuar?",
            yes_text="Sim",
            no_text="Não"
        ).run()
        
        console.print(f"Resultado do diálogo de confirmação: {resultado}")
        return True
    except Exception as e:
        console.print(f"[bold red]Erro ao testar diálogos: {e}[/bold red]")
        return False


def executar_testes():
    """Executa todos os testes em sequência"""
    console.print("[bold magenta]Iniciando testes da aplicação TUI[/bold magenta]")
    console.print("=" * 60)
    
    # Lista de testes a executar
    testes = [
        ("Diálogos Padronizados", testar_dialogos),
        ("Menu Principal", testar_menu_principal),
        ("Seletor de Arquivos", testar_seletor_arquivo),
        ("Planilha de Registros", testar_planilha_registros)
    ]
    
    # Executar testes
    resultados = {}
    for nome, funcao in testes:
        console.print(f"\n[bold blue]Executando teste: {nome}[/bold blue]")
        console.print("-" * 60)
        
        try:
            resultado = funcao()
            resultados[nome] = resultado
        except Exception as e:
            console.print(f"[bold red]Erro não tratado no teste {nome}: {e}[/bold red]")
            resultados[nome] = False
    
    # Exibir resumo
    console.print("\n[bold magenta]Resumo dos testes[/bold magenta]")
    console.print("=" * 60)
    
    for nome, resultado in resultados.items():
        status = "[bold green]PASSOU[/bold green]" if resultado else "[bold red]FALHOU[/bold red]"
        console.print(f"{nome}: {status}")


if __name__ == "__main__":
    executar_testes()
