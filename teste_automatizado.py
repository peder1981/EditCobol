#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste automatizado para a aplicação de edição de arquivos de movimentação financeira
"""

import os
import sys
import tempfile
import shutil
from financeiro_app import ArquivoMovimentacao, RegistroMovimento

def criar_arquivo_teste(caminho_arquivo):
    """Cria um arquivo de teste válido"""
    conteudo_teste = """H20250616UN20250616        0000000000000000000000000000000000000000000000000000000000000000
M462025061046607900000098240000020000000000001710020250616335525646000050620030001730000000
M0320250530230888XXXXXX10860000060000000000003000020250616017074932000044309830001570000000
T00002 000047100999999999999999999999999999999999999999999999999999999999999999999999999999"""
    
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo_teste)

def testar_carregamento_arquivo():
    """Testa o carregamento de um arquivo válido"""
    print("Testando carregamento de arquivo...")
    
    # Criar arquivo de teste
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        caminho_arquivo = f.name
        f.write("""H20250616UN20250616        0000000000000000000000000000000000000000000000000000000000000000
M462025061046607900000098240000020000000000001710020250616335525646000050620030001730000000
M0320250530230888XXXXXX10860000060000000000003000020250616017074932000044309830001570000000
T00002 000047100999999999999999999999999999999999999999999999999999999999999999999999999999""")
    
    try:
        # Tentar carregar o arquivo
        arquivo = ArquivoMovimentacao(caminho_arquivo)
        
        # Verificar se os dados foram carregados corretamente
        assert arquivo.header is not None, "Header não carregado"
        assert len(arquivo.movimentos) == 2, f"Número incorreto de movimentos: {len(arquivo.movimentos)}"
        assert arquivo.trailer is not None, "Trailer não carregado"
        
        # Verificar valores
        valor_total = sum(mov.get_valor_decimal() for mov in arquivo.movimentos)
        assert abs(valor_total - arquivo.trailer.get_valor_total_decimal()) < 0.01, "Valores não batem"
        
        print("✓ Carregamento de arquivo: OK")
        return True
        
    except Exception as e:
        print(f"✗ Carregamento de arquivo: ERRO - {e}")
        return False
    finally:
        # Remover arquivo temporário
        os.unlink(caminho_arquivo)

def testar_edicao_registro():
    """Testa a edição de um registro"""
    print("Testando edição de registro...")
    
    # Criar arquivo de teste
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        caminho_arquivo = f.name
        f.write("""H20250616UN20250616        0000000000000000000000000000000000000000000000000000000000000000
M462025061046607900000098240000020000000000001710020250616335525646000050620030001730000000
M0320250530230888XXXXXX10860000060000000000003000020250616017074932000044309830001570000000
T00002 000047100999999999999999999999999999999999999999999999999999999999999999999999999999""")
    
    try:
        # Carregar arquivo
        arquivo = ArquivoMovimentacao(caminho_arquivo)
        
        # Editar um registro
        movimento = arquivo.movimentos[0]
        valor_original = movimento.get_valor_decimal()
        movimento.set_valor_decimal(200.00)  # Alterar valor para R$ 200,00
        
        # Recalcular trailer
        arquivo.recalcular_trailer()
        
        # Verificar se o trailer foi atualizado corretamente
        novo_valor_total = sum(mov.get_valor_decimal() for mov in arquivo.movimentos)
        assert abs(novo_valor_total - arquivo.trailer.get_valor_total_decimal()) < 0.01, "Trailer não recalculado corretamente"
        
        print("✓ Edição de registro: OK")
        return True
        
    except Exception as e:
        print(f"✗ Edição de registro: ERRO - {e}")
        return False
    finally:
        # Remover arquivo temporário
        os.unlink(caminho_arquivo)

def testar_delecao_registro():
    """Testa a deleção de um registro"""
    print("Testando deleção de registro...")
    
    # Criar arquivo de teste
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        caminho_arquivo = f.name
        f.write("""H20250616UN20250616        0000000000000000000000000000000000000000000000000000000000000000
M462025061046607900000098240000020000000000001710020250616335525646000050620030001730000000
M0320250530230888XXXXXX10860000060000000000003000020250616017074932000044309830001570000000
T00002 000047100999999999999999999999999999999999999999999999999999999999999999999999999999""")
    
    try:
        # Carregar arquivo
        arquivo = ArquivoMovimentacao(caminho_arquivo)
        
        # Deletar um registro
        total_registros_original = len(arquivo.movimentos)
        del arquivo.movimentos[0]
        
        # Recalcular trailer
        arquivo.recalcular_trailer()
        
        # Verificar se o trailer foi atualizado corretamente
        assert len(arquivo.movimentos) == total_registros_original - 1, "Registro não deletado"
        assert arquivo.trailer.get_total_registros() == len(arquivo.movimentos), "Contagem de registros no trailer incorreta"
        
        novo_valor_total = sum(mov.get_valor_decimal() for mov in arquivo.movimentos)
        assert abs(novo_valor_total - arquivo.trailer.get_valor_total_decimal()) < 0.01, "Trailer não recalculado corretamente"
        
        print("✓ Deleção de registro: OK")
        return True
        
    except Exception as e:
        print(f"✗ Deleção de registro: ERRO - {e}")
        return False
    finally:
        # Remover arquivo temporário
        os.unlink(caminho_arquivo)

def testar_exclusao_por_adquirente():
    """Testa a exclusão de registros por código de adquirente"""
    print("Testando exclusão por adquirente...")
    
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
        
        # Excluir registros por adquirente
        total_registros_original = len(arquivo.movimentos)
        registros_adquirente_46 = sum(1 for mov in arquivo.movimentos if mov.codigo_adquirente == '46')
        
        # Percorrer de trás para frente para evitar problemas com índices
        for i in range(len(arquivo.movimentos) - 1, -1, -1):
            if arquivo.movimentos[i].codigo_adquirente == '46':
                del arquivo.movimentos[i]
        
        # Recalcular trailer
        arquivo.recalcular_trailer()
        
        # Verificar se os registros foram excluídos corretamente
        registros_adquirente_46_atual = sum(1 for mov in arquivo.movimentos if mov.codigo_adquirente == '46')
        assert registros_adquirente_46_atual == 0, "Registros do adquirente 46 não foram excluídos"
        assert len(arquivo.movimentos) == total_registros_original - registros_adquirente_46, "Número incorreto de registros excluídos"
        assert arquivo.trailer.get_total_registros() == len(arquivo.movimentos), "Contagem de registros no trailer incorreta"
        
        print("✓ Exclusão por adquirente: OK")
        return True
        
    except Exception as e:
        print(f"✗ Exclusão por adquirente: ERRO - {e}")
        return False
    finally:
        # Remover arquivo temporário
        os.unlink(caminho_arquivo)

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
    print("TESTES AUTOMATIZADOS - Editor de Arquivo de Movimentação Financeira")
    print("=" * 60)
    print()
    
    # Executar testes
    testes = [
        testar_carregamento_arquivo,
        testar_edicao_registro,
        testar_delecao_registro,
        testar_exclusao_por_adquirente,
        testar_selecao_por_valor
    ]
    
    resultados = []
    for teste in testes:
        try:
            resultado = teste()
            resultados.append(resultado)
        except Exception as e:
            print(f"Erro ao executar teste {teste.__name__}: {e}")
            resultados.append(False)
        print()
    
    # Resumo
    total_testes = len(resultados)
    testes_passaram = sum(resultados)
    
    print("=" * 60)
    print(f"RESUMO DOS TESTES: {testes_passaram}/{total_testes} testes passaram")
    print("=" * 60)
    
    if testes_passaram == total_testes:
        print("Todos os testes passaram! ✓")
        return 0
    else:
        print("Alguns testes falharam! ✗")
        return 1

if __name__ == "__main__":
    sys.exit(main())
