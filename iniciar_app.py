#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicialização para o Editor de Arquivo de Movimentação Financeira
"""

import os
import sys
import subprocess

def mostrar_menu_principal():
    """Mostra o menu principal da aplicação"""
    print("=" * 60)
    print("EDITOR DE ARQUIVO DE MOVIMENTAÇÃO FINANCEIRA")
    print("=" * 60)
    print()
    print("1. Iniciar editor principal")
    print("2. Visualizar logs")
    print("3. Gerenciar backups")
    print("4. Executar testes automatizados")
    print("5. Visualizar documentação")
    print("0. Sair")
    print()

def iniciar_editor_principal():
    """Inicia o editor principal"""
    try:
        print("Iniciando editor principal...")
        subprocess.run([sys.executable, "financeiro_app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao iniciar o editor: {e}")
    except FileNotFoundError:
        print("Arquivo financeiro_app.py não encontrado.")

def visualizar_logs():
    """Visualiza os logs da aplicação"""
    try:
        print("Visualizando logs...")
        subprocess.run([sys.executable, "visualizar_logs.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao visualizar logs: {e}")
    except FileNotFoundError:
        print("Arquivo visualizar_logs.py não encontrado.")

def gerenciar_backups():
    """Gerencia os backups da aplicação"""
    try:
        print("Gerenciando backups...")
        subprocess.run([sys.executable, "backup_arquivos.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao gerenciar backups: {e}")
    except FileNotFoundError:
        print("Arquivo backup_arquivos.py não encontrado.")

def executar_testes():
    """Executa os testes automatizados"""
    try:
        print("Executando testes automatizados...")
        subprocess.run([sys.executable, "teste_automatizado.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar testes: {e}")
    except FileNotFoundError:
        print("Arquivo teste_automatizado.py não encontrado.")

def visualizar_documentacao():
    """Visualiza a documentação da aplicação"""
    try:
        print("Visualizando documentação...")
        if os.name == 'nt':  # Windows
            os.system("start README.md")
        elif os.name == 'posix':  # Linux/Mac
            os.system("xdg-open README.md")
        else:
            with open("README.md", "r", encoding="utf-8") as f:
                print(f.read())
    except Exception as e:
        print(f"Erro ao visualizar documentação: {e}")
        # Fallback: mostrar conteúdo do README
        try:
            with open("README.md", "r", encoding="utf-8") as f:
                print(f.read())
        except Exception as e2:
            print(f"Não foi possível abrir o README.md: {e2}")

def main():
    """Função principal"""
    while True:
        mostrar_menu_principal()
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            iniciar_editor_principal()
        elif opcao == '2':
            visualizar_logs()
        elif opcao == '3':
            gerenciar_backups()
        elif opcao == '4':
            executar_testes()
        elif opcao == '5':
            visualizar_documentacao()
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")
        
        input("\nPressione Enter para continuar...")
        # Limpar tela (opcional)
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()
