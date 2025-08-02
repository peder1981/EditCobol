#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste para validar os métodos de fábrica das classes RegistroMovimento e ArquivoMovimentacao
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from financeiro_app import ArquivoMovimentacao, RegistroMovimento

def testar_factory_arquivo_movimentacao():
    """Testa o método de fábrica para ArquivoMovimentacao"""
    print("Testando factory de ArquivoMovimentacao...")
    
    # Criar arquivo usando o método de fábrica
    arquivo = ArquivoMovimentacao.criar_arquivo_teste()
    
    # Verificar que o arquivo foi criado corretamente
    assert arquivo.movimentos == [], "Lista de movimentos deveria estar vazia"
    assert arquivo.header is None, "Header deveria ser None"
    assert arquivo.trailer is None, "Trailer deveria ser None"
    
    print("✓ Factory de ArquivoMovimentacao: OK")
    return True

def testar_factory_registro_movimento():
    """Testa o método de fábrica para RegistroMovimento"""
    print("Testando factory de RegistroMovimento...")
    
    # Criar registro usando o método de fábrica
    registro = RegistroMovimento.criar_registro(
        tipo='M',
        codigo_adquirente='46',
        data_movimento='20250610',
        numero_cartao='4660790000009824',
        parcelas='02',
        valor_venda='17100',
        data_venda='20250616',
        cvnsu='335525646',
        zeros_fixos='00',
        cpf_cnpj='5062003000173',
        numero_pedido='0000000'
    )
    
    # Verificar que o registro foi criado corretamente
    assert registro.tipo == 'M', f"Tipo incorreto: {registro.tipo}"
    assert registro.codigo_adquirente == '46', f"Código adquirente incorreto: {registro.codigo_adquirente}"
    assert registro.data_movimento == '20250610', f"Data movimento incorreta: {registro.data_movimento}"
    assert registro.numero_cartao == '4660790000009824'.ljust(20)[:20], f"Número cartão incorreto: {registro.numero_cartao}"
    assert registro.parcelas == '02', f"Parcelas incorretas: {registro.parcelas}"
    assert registro.valor_venda == '00000000000017100', f"Valor venda incorreto: {registro.valor_venda}"
    assert registro.data_venda == '20250616', f"Data venda incorreta: {registro.data_venda}"
    assert registro.cvnsu == '335525646', f"CVNSU incorreto: {registro.cvnsu}"
    assert registro.zeros_fixos == '00', f"Zeros fixos incorretos: {registro.zeros_fixos}"
    assert registro.cpf_cnpj == '5062003000173'.ljust(15)[:15], f"CPF/CNPJ incorreto: {registro.cpf_cnpj}"
    assert registro.numero_pedido == '0000000', f"Número pedido incorreto: {registro.numero_pedido}"
    
    # Verificar que a linha tem exatamente 91 caracteres
    linha = str(registro)
    assert len(linha) == 91, f"Linha deveria ter 91 caracteres, mas tem {len(linha)}"
    
    print("✓ Factory de RegistroMovimento: OK")
    return True

def testar_valores_default():
    """Testa o método de fábrica com valores default"""
    print("Testando factory de RegistroMovimento com valores default...")
    
    # Criar registro usando o método de fábrica com valores default
    registro = RegistroMovimento.criar_registro()
    
    # Verificar que o registro foi criado com valores default
    assert registro.tipo == 'M', f"Tipo incorreto: {registro.tipo}"
    assert registro.codigo_adquirente == '00', f"Código adquirente incorreto: {registro.codigo_adquirente}"
    assert registro.data_movimento == '00000000', f"Data movimento incorreta: {registro.data_movimento}"
    
    print("✓ Factory de RegistroMovimento com valores default: OK")
    return True

def main():
    """Função principal de teste"""
    print("=" * 60)
    print("TESTE AUTOMATIZADO - Métodos de Fábrica")
    print("=" * 60)
    print()
    
    # Executar testes
    try:
        resultado1 = testar_factory_arquivo_movimentacao()
        resultado2 = testar_factory_registro_movimento()
        resultado3 = testar_valores_default()
        print()
        
        if resultado1 and resultado2 and resultado3:
            print("Todos os testes passaram! ✓")
            return 0
        else:
            print("Alguns testes falharam! ✗")
            return 1
    except Exception as e:
        print(f"Erro ao executar testes: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
