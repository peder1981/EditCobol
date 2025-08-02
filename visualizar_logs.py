#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para visualizar logs da aplicação de forma amigável
"""

import re
from datetime import datetime

def parse_log_line(line):
    """Parseia uma linha de log e extrai as informações"""
    # Padrão do log: [DATA/HORA] [NÍVEL] [FUNÇÃO] [AÇÃO] DETALHES
    pattern = r'\[(.*?)\] \[(.*?)\] \[(.*?)\] \[(.*?)\] (.*)'
    match = re.match(pattern, line.strip())
    
    if match:
        timestamp, level, function, action, details = match.groups()
        return {
            'timestamp': timestamp,
            'level': level,
            'function': function,
            'action': action,
            'details': details
        }
    return None

def format_timestamp(timestamp_str):
    """Formata o timestamp para exibição"""
    try:
        dt = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%d/%m/%Y %H:%M:%S')
    except:
        return timestamp_str

def visualizar_logs(arquivo_log='log.txt'):
    """Visualiza os logs de forma formatada"""
    try:
        with open(arquivo_log, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        
        print("=" * 80)
        print("VISUALIZADOR DE LOGS - Editor de Arquivo de Movimentação Financeira")
        print("=" * 80)
        print()
        
        # Pular as linhas de comentário no início
        logs_validos = []
        for linha in linhas:
            if linha.startswith('[') and 'INFO' in linha:
                log_data = parse_log_line(linha)
                if log_data:
                    logs_validos.append(log_data)
        
        # Ordenar por timestamp
        logs_validos.sort(key=lambda x: x['timestamp'])
        
        # Exibir logs
        for log in logs_validos:
            timestamp_formatado = format_timestamp(log['timestamp'])
            print(f"{timestamp_formatado} | {log['action']:<20} | {log['details']}")
        
        print()
        print(f"Total de registros: {len(logs_validos)}")
        
    except FileNotFoundError:
        print(f"Arquivo {arquivo_log} não encontrado.")
    except Exception as e:
        print(f"Erro ao ler o arquivo de log: {e}")

if __name__ == "__main__":
    visualizar_logs()
