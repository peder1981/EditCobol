#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar backups dos arquivos de movimentação financeira
"""

import os
import shutil
import datetime
from pathlib import Path

def criar_backup_diretorio(origem, destino):
    """Cria um backup de todos os arquivos de movimentação financeira"""
    try:
        # Criar diretório de backup se não existir
        Path(destino).mkdir(parents=True, exist_ok=True)
        
        # Obter data e hora atual para o nome do backup
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(destino, f"backup_{timestamp}")
        Path(backup_dir).mkdir(parents=True, exist_ok=True)
        
        # Copiar arquivos de movimentação financeira
        arquivos_copiados = 0
        for arquivo in os.listdir(origem):
            # Verificar se é um arquivo de movimentação (extensões comuns)
            if arquivo.endswith((".txt", ".dat", ".mov", ".fin")):
                origem_arquivo = os.path.join(origem, arquivo)
                destino_arquivo = os.path.join(backup_dir, arquivo)
                
                # Copiar arquivo
                shutil.copy2(origem_arquivo, destino_arquivo)
                arquivos_copiados += 1
                print(f"Arquivo copiado: {arquivo}")
        
        print(f"\nBackup concluído com sucesso!")
        print(f"Diretório de backup: {backup_dir}")
        print(f"Arquivos copiados: {arquivos_copiados}")
        
        return backup_dir
        
    except Exception as e:
        print(f"Erro ao criar backup: {e}")
        return None

def listar_backups(diretorio_backup):
    """Lista todos os backups disponíveis"""
    try:
        if not os.path.exists(diretorio_backup):
            print("Nenhum backup encontrado.")
            return
        
        backups = [d for d in os.listdir(diretorio_backup) if d.startswith("backup_")]
        backups.sort(reverse=True)  # Ordenar do mais recente para o mais antigo
        
        if not backups:
            print("Nenhum backup encontrado.")
            return
        
        print("Backups disponíveis:")
        for i, backup in enumerate(backups, 1):
            print(f"{i}. {backup}")
            
    except Exception as e:
        print(f"Erro ao listar backups: {e}")

def restaurar_backup(diretorio_backup, nome_backup, diretorio_origem):
    """Restaura um backup específico"""
    try:
        backup_path = os.path.join(diretorio_backup, nome_backup)
        
        if not os.path.exists(backup_path):
            print(f"Backup {nome_backup} não encontrado.")
            return False
        
        # Confirmar restauração
        confirmacao = input(f"Tem certeza que deseja restaurar o backup {nome_backup}? (s/N): ")
        if confirmacao.lower() != 's':
            print("Restauração cancelada.")
            return False
        
        # Copiar arquivos do backup para o diretório original
        arquivos_restaurados = 0
        for arquivo in os.listdir(backup_path):
            if arquivo.endswith((".txt", ".dat", ".mov", ".fin")):
                origem_arquivo = os.path.join(backup_path, arquivo)
                destino_arquivo = os.path.join(diretorio_origem, arquivo)
                
                # Copiar arquivo
                shutil.copy2(origem_arquivo, destino_arquivo)
                arquivos_restaurados += 1
                print(f"Arquivo restaurado: {arquivo}")
        
        print(f"\nRestauração concluída com sucesso!")
        print(f"Arquivos restaurados: {arquivos_restaurados}")
        
        return True
        
    except Exception as e:
        print(f"Erro ao restaurar backup: {e}")
        return False

def main():
    """Função principal"""
    diretorio_atual = os.getcwd()
    diretorio_backup = os.path.join(diretorio_atual, "backups")
    
    while True:
        print("\n=== Sistema de Backup ===")
        print("1. Criar backup")
        print("2. Listar backups")
        print("3. Restaurar backup")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            print("\nCriando backup...")
            criar_backup_diretorio(diretorio_atual, diretorio_backup)
        elif opcao == '2':
            print("\nListando backups...")
            listar_backups(diretorio_backup)
        elif opcao == '3':
            print("\nListando backups...")
            listar_backups(diretorio_backup)
            nome_backup = input("\nDigite o nome do backup para restaurar (ou 0 para cancelar): ")
            if nome_backup != '0':
                restaurar_backup(diretorio_backup, nome_backup, diretorio_atual)
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
