#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from planilha_registros import PlanilhaRegistros
from financeiro_app import ArquivoMovimentacao, RegistroMovimento

# Criar um arquivo de movimentação de teste
arquivo_teste = ArquivoMovimentacao.criar_arquivo_teste()

# Adicionar alguns registros de teste
for i in range(10):
    registro = RegistroMovimento.criar_registro(
        codigo_adquirente=f"{i:02d}",
        data_movimento=f"202308{i:02d}",
        numero_cartao=f"123456789012345{i:02d}".ljust(20)[:20],
        valor_venda=f"{int((100.50 + i) * 100):017d}",
        cvnsu=f"CV{i:05d}".ljust(9)[:9]
    )
    arquivo_teste.movimentos.append(registro)

# Criar e executar a planilha
planilha = PlanilhaRegistros(arquivo_teste)
print("Iniciando interface de planilha...")
planilha.executar()
print("Interface de planilha encerrada.")
