#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste automatizado para a funcionalidade de escolher registros
"""

import os
import sys
import shutil
import unittest
from financeiro_app import ArquivoMovimentacao

class TesteEscolherRegistros(unittest.TestCase):
    def setUp(self):
        # Usar um arquivo existente como base e criar uma cópia temporária para teste
        self.arquivo_original = "rc160625.008"
        self.arquivo_teste = "rc160625.008.teste"
        
        # Verificar se o arquivo original existe
        if not os.path.exists(self.arquivo_original):
            self.skipTest(f"Arquivo de teste {self.arquivo_original} não encontrado")
        
        # Criar cópia do arquivo para teste
        shutil.copy2(self.arquivo_original, self.arquivo_teste)
    
    def tearDown(self):
        # Remover arquivos temporários após o teste
        if os.path.exists(self.arquivo_teste):
            os.unlink(self.arquivo_teste)
        
        # Remover arquivo salvo, se existir
        arquivo_salvo = f"{self.arquivo_teste}.modificado"
        if os.path.exists(arquivo_salvo):
            os.unlink(arquivo_salvo)
    
    def test_escolher_registros(self):
        """Testa a funcionalidade de escolher registros específicos para manter"""
        # Carregar o arquivo
        arquivo = ArquivoMovimentacao(self.arquivo_teste)
        
        # Guardar o número original de registros
        num_registros_original = len(arquivo.movimentos)
        print(f"Número original de registros: {num_registros_original}")
        
        # Selecionar alguns registros para manter (aproximadamente 30% dos registros)
        num_registros_manter = max(3, num_registros_original // 3)
        indices_manter = [i for i in range(0, num_registros_original, 3)][:num_registros_manter]
        print(f"Mantendo {len(indices_manter)} registros com índices: {indices_manter}")
        
        # Simular a seleção manual removendo os registros que não estão na lista
        registros_excluidos = 0
        for i in range(len(arquivo.movimentos) - 1, -1, -1):
            if i not in indices_manter:
                del arquivo.movimentos[i]
                registros_excluidos += 1
        
        # Recalcular trailer
        arquivo.recalcular_trailer()
        
        # Verificar se apenas os registros selecionados foram mantidos
        self.assertEqual(len(arquivo.movimentos), len(indices_manter))
        print(f"Registros mantidos: {len(arquivo.movimentos)}, Registros excluídos: {registros_excluidos}")
        
        # Calcular a soma dos valores dos registros mantidos
        soma_valores = sum(mov.get_valor_decimal() for mov in arquivo.movimentos)
        print(f"Soma dos valores dos registros mantidos: {soma_valores:.2f}")
        
        # Verificar se o trailer foi atualizado corretamente
        self.assertEqual(arquivo.trailer.get_total_registros(), len(indices_manter))
        self.assertAlmostEqual(arquivo.trailer.get_valor_total_decimal(), soma_valores, places=2)
        print(f"Valor total no trailer: {arquivo.trailer.get_valor_total_decimal():.2f}")
        
        # Salvar o arquivo modificado
        arquivo_salvo = f"{self.arquivo_teste}.modificado"
        arquivo.salvar_arquivo(arquivo_salvo)
        print(f"Arquivo salvo como: {arquivo_salvo}")
        
        # Verificar se o arquivo foi salvo corretamente
        arquivo_modificado = ArquivoMovimentacao(arquivo_salvo)
        self.assertEqual(len(arquivo_modificado.movimentos), len(indices_manter))
        self.assertEqual(arquivo_modificado.trailer.get_total_registros(), len(indices_manter))
        self.assertAlmostEqual(arquivo_modificado.trailer.get_valor_total_decimal(), soma_valores, places=2)

if __name__ == "__main__":
    print("============================================================")
    print("TESTE AUTOMATIZADO - Escolher Registros")
    print("============================================================")
    
    # Executar o teste
    suite = unittest.TestLoader().loadTestsFromTestCase(TesteEscolherRegistros)
    result = unittest.TextTestRunner().run(suite)
    
    # Verificar resultado
    if result.wasSuccessful():
        print("\nTeste passou! ✓")
        sys.exit(0)
    else:
        print("\nTeste falhou! ✗")
        sys.exit(1)
