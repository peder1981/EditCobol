#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste automatizado para a funcionalidade de seleção por valor
"""

import os
import sys
import tempfile
from financeiro_app import ArquivoMovimentacao, RegistroMovimento

def testar_selecao_por_valor():
    """Testa a seleção de registros por valor"""
    print("Testando seleção por valor...")
    
    # Criar arquivo de teste
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        caminho_arquivo = f.name
        f.write("""H20250616UN20250616        0000000000000000000000000000000000000000000000000000000000000000
M462025061046607900000098240000020000000000001710020250616335525646000050620030001730000000
M0320250530230888XXXXXX10860000060000000000003000020250616017074932000044309830001570000000
M462025061046607900000098240000020000000000001000020250616335525646000050620030001730000000
T00003 000057100999999999999999999999999999999999999999999999999999999999999999999999999999""")
    
    try:
        # Carregar arquivo
        arquivo = ArquivoMovimentacao(caminho_arquivo)
        
        # Verificar valores dos registros
        valor_registro1 = arquivo.movimentos[0].get_valor_decimal()  # 171.00
        valor_registro2 = arquivo.movimentos[1].get_valor_decimal()  # 300.00
        valor_registro3 = arquivo.movimentos[2].get_valor_decimal()  # 100.00
        
        # Testar seleção por valor exato (171.00)
        from financeiro_app import selecionar_por_valor
        selecionar_por_valor(arquivo, 171.00)
        
        # Verificar se apenas 1 registro foi mantido
        assert len(arquivo.movimentos) == 1, f"Número incorreto de registros mantidos: {len(arquivo.movimentos)}"
        
        # Verificar se o registro correto foi mantido
        assert abs(arquivo.movimentos[0].get_valor_decimal() - 171.00) < 0.01, "Registro incorreto foi mantido"
        
        # Verificar se o trailer foi atualizado corretamente
        assert arquivo.trailer.get_total_registros() == 1, "Contagem de registros no trailer incorreta"
        assert abs(arquivo.trailer.get_valor_total_decimal() - 171.00) < 0.01, "Valor total no trailer incorreto"
        
        print("✓ Seleção por valor: OK")
        return True
        
    except Exception as e:
        print(f"✗ Seleção por valor: ERRO - {e}")
        return False
    finally:
        # Remover arquivo temporário
        os.unlink(caminho_arquivo)

def main():
    """Função principal de teste"""
    print("=" * 60)
    print("TESTE AUTOMATIZADO - Seleção por Valor")
    print("=" * 60)
    print()
    
    # Executar teste
    try:
        resultado = testar_selecao_por_valor()
        print()
        
        if resultado:
            print("Teste passou! ✓")
            return 0
        else:
            print("Teste falhou! ✗")
            return 1
    except Exception as e:
        print(f"Erro ao executar teste: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
