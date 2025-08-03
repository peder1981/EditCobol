#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicação para manipulação de arquivos de movimentação financeira
"""

import os
import sys
import logging
from typing import List, Tuple
from datetime import datetime

# Importar componentes TUI
from planilha_registros import PlanilhaRegistros
from menu_principal_tui import MenuPrincipalTUI

# Configurar logging
logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(funcName)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_operacao(acao: str, detalhes: str):
    """Registra uma operação no log"""
    logging.info(f"[{acao}] {detalhes}")


class RegistroHeader:
    def __init__(self, linha: str):
        if len(linha) != 91:
            raise ValueError("Registro Header deve ter exatamente 91 caracteres")
        
        self.tipo = linha[0]
        self.data_processamento = linha[1:9]
        self.codigo_unidade = linha[9:11]
        self.data_processamento2 = linha[11:19]
        self.espacos = linha[19:27]
        self.zeros = linha[27:91]
    
    def __str__(self):
        return f"H{self.data_processamento}{self.codigo_unidade}{self.data_processamento2}{self.espacos}{self.zeros}"

class RegistroMovimento:
    def __init__(self, linha: str):
        if len(linha) != 91:
            raise ValueError("Registro de Movimento deve ter exatamente 91 caracteres")
        
        self.tipo = linha[0]
        self.codigo_adquirente = linha[1:3]
        self.data_movimento = linha[3:11]
        self.numero_cartao = linha[11:31]
        self.parcelas = linha[31:33]
        self.valor_venda = linha[33:50]
        self.data_venda = linha[50:58]
        self.cvnsu = linha[58:67]
        self.zeros_fixos = linha[67:69]
        self.cpf_cnpj = linha[69:84]
        self.numero_pedido = linha[84:91]
    
    @classmethod
    def criar_registro(cls, tipo='M', codigo_adquirente='00', data_movimento='00000000', 
                      numero_cartao=' ' * 20, parcelas='00', valor_venda='0' * 17, 
                      data_venda='00000000', cvnsu='0' * 9, zeros_fixos='00', 
                      cpf_cnpj='0' * 15, numero_pedido='0' * 7):
        """Cria um RegistroMovimento com parâmetros individuais"""
        # Formatar os campos para garantir o tamanho correto
        tipo = tipo.ljust(1)[:1]
        codigo_adquirente = codigo_adquirente.ljust(2)[:2]
        data_movimento = data_movimento.ljust(8)[:8]
        numero_cartao = numero_cartao.ljust(20)[:20]
        parcelas = parcelas.ljust(2)[:2]
        valor_venda = valor_venda.rjust(17, '0')[:17]
        data_venda = data_venda.ljust(8)[:8]
        cvnsu = cvnsu.ljust(9)[:9]
        zeros_fixos = zeros_fixos.ljust(2)[:2]
        cpf_cnpj = cpf_cnpj.ljust(15)[:15]
        numero_pedido = numero_pedido.ljust(7)[:7]
        
        # Construir a linha formatada
        linha = (f"{tipo}{codigo_adquirente}{data_movimento}{numero_cartao}"
                f"{parcelas}{valor_venda}{data_venda}{cvnsu}"
                f"{zeros_fixos}{cpf_cnpj}{numero_pedido}")
        
        # Criar e retornar a instância
        instancia = cls(linha)
        return instancia
    
    def get_valor_decimal(self) -> float:
        """Retorna o valor da venda como decimal"""
        valor = int(self.valor_venda)
        return valor / 100
    
    def set_valor_decimal(self, valor: float):
        """Define o valor da venda a partir de um decimal"""
        valor_centavos = int(valor * 100)
        self.valor_venda = f"{valor_centavos:017d}"
    
    def __str__(self):
        return (f"{self.tipo}{self.codigo_adquirente}{self.data_movimento}{self.numero_cartao}"
                f"{self.parcelas}{self.valor_venda}{self.data_venda}{self.cvnsu}"
                f"{self.zeros_fixos}{self.cpf_cnpj}{self.numero_pedido}")

class RegistroTrailer:
    def __init__(self, linha: str):
        if len(linha) != 91:
            raise ValueError("Registro Trailer deve ter exatamente 91 caracteres")
        
        self.tipo = linha[0]
        self.total_registros = linha[1:6]
        self.espaco = linha[6]
        self.valor_total = linha[7:16]
        self.noves = linha[16:91]
    
    def get_total_registros(self) -> int:
        return int(self.total_registros)
    
    def set_total_registros(self, total: int):
        self.total_registros = f"{total:05d}"
    
    def get_valor_total_decimal(self) -> float:
        valor = int(self.valor_total)
        return valor / 100
    
    def set_valor_total_decimal(self, valor: float):
        valor_centavos = int(valor * 100)
        self.valor_total = f"{valor_centavos:09d}"
    
    def __str__(self):
        return f"{self.tipo}{self.total_registros}{self.espaco}{self.valor_total}{self.noves}"

class ArquivoMovimentacao:
    def __init__(self, caminho_arquivo: str = None):
        self.caminho_arquivo = caminho_arquivo
        self.header = None
        self.movimentos = []
        self.trailer = None
        self.conteudo_original = []
        
        if caminho_arquivo and os.path.exists(caminho_arquivo):
            self.carregar_arquivo(caminho_arquivo)
    
    @classmethod
    def criar_arquivo_teste(cls):
        """Cria um ArquivoMovimentacao vazio para testes"""
        instancia = cls()
        return instancia
    
    def carregar_arquivo(self, caminho_arquivo: str):
        """Carrega e valida o arquivo de movimentação"""
        log_operacao("CARREGAR_ARQUIVO", f"Iniciando carregamento do arquivo {caminho_arquivo}")
        
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            linhas = [linha.rstrip('\n') for linha in f.readlines()]
        
        self.conteudo_original = linhas.copy()
        
        # Validar tamanho das linhas
        for i, linha in enumerate(linhas):
            if len(linha) != 91:
                log_operacao("ERRO_VALIDACAO", f"Linha {i+1} tem {len(linha)} caracteres, deveria ter 91")
                raise ValueError(f"Linha {i+1} tem {len(linha)} caracteres, deveria ter 91")
        
        # Validar primeiro registro (Header)
        if not linhas or linhas[0][0] != 'H':
            log_operacao("ERRO_VALIDACAO", "Primeiro registro deve ser do tipo Header (H)")
            raise ValueError("Primeiro registro deve ser do tipo Header (H)")
        
        self.header = RegistroHeader(linhas[0])
        log_operacao("CARREGAR_ARQUIVO", "Registro Header carregado com sucesso")
        
        # Processar registros de movimento
        self.movimentos = []
        registros_movimento = []
        
        for i in range(1, len(linhas) - 1):
            if linhas[i][0] == 'M':
                movimento = RegistroMovimento(linhas[i])
                self.movimentos.append(movimento)
                registros_movimento.append(movimento)
            else:
                log_operacao("ERRO_VALIDACAO", f"Registro na linha {i+1} deveria ser do tipo Movimento (M)")
                raise ValueError(f"Registro na linha {i+1} deveria ser do tipo Movimento (M)")
        
        log_operacao("CARREGAR_ARQUIVO", f"{len(registros_movimento)} registros de movimento carregados")
        
        # Validar último registro (Trailer)
        if not linhas or linhas[-1][0] != 'T':
            log_operacao("ERRO_VALIDACAO", "Último registro deve ser do tipo Trailer (T)")
            raise ValueError("Último registro deve ser do tipo Trailer (T)")
        
        self.trailer = RegistroTrailer(linhas[-1])
        log_operacao("CARREGAR_ARQUIVO", "Registro Trailer carregado com sucesso")
        
        # Validar contagem de registros
        total_registros_m = len(registros_movimento)
        if total_registros_m != self.trailer.get_total_registros():
            log_operacao("ERRO_VALIDACAO", f"Número de registros M ({total_registros_m}) não corresponde ao valor no Trailer ({self.trailer.get_total_registros()})")
            raise ValueError(f"Número de registros M ({total_registros_m}) não corresponde ao valor no Trailer ({self.trailer.get_total_registros()})")
        
        # Validar soma dos valores
        soma_valores = sum(mov.get_valor_decimal() for mov in registros_movimento)
        valor_trailer = self.trailer.get_valor_total_decimal()
        
        if abs(soma_valores - valor_trailer) > 0.01:  # Tolerância para erros de arredondamento
            log_operacao("ERRO_VALIDACAO", f"Soma dos valores dos registros M ({soma_valores}) não corresponde ao valor no Trailer ({valor_trailer})")
            raise ValueError(f"Soma dos valores dos registros M ({soma_valores}) não corresponde ao valor no Trailer ({valor_trailer})")
        
        log_operacao("CARREGAR_ARQUIVO", f"Arquivo {caminho_arquivo} carregado e validado com sucesso")
    
    def recalcular_trailer(self):
        """Recalcula o trailer com base nos registros atuais"""
        # Atualizar total de registros
        total_registros = len(self.movimentos)
        self.trailer.set_total_registros(total_registros)
        
        # Atualizar valor total
        valor_total = sum(mov.get_valor_decimal() for mov in self.movimentos)
        self.trailer.set_valor_total_decimal(valor_total)
    
    def salvar_arquivo(self, caminho_arquivo: str = None):
        """Salva o arquivo de movimentação"""
        caminho = caminho_arquivo if caminho_arquivo else self.caminho_arquivo
        log_operacao("SALVAR_ARQUIVO", f"Iniciando salvamento do arquivo em {caminho}")
        
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(str(self.header) + '\n')
            for movimento in self.movimentos:
                f.write(str(movimento) + '\n')
            f.write(str(self.trailer) + '\n')
        
        log_operacao("SALVAR_ARQUIVO", f"Arquivo salvo com sucesso em {caminho}")
    
    def exibir_conteudo(self):
        """Exibe o conteúdo do arquivo como planilha"""
        print("\n=== Conteúdo do Arquivo ===")
        print(f"{'Linha':<5} {'Tipo':<5} {'Descrição':<50} {'Valor':<15}")
        print("-" * 80)
        
        # Header
        print(f"{1:<5} {'H':<5} Header - Data: {self.header.data_processamento}, Unidade: {self.header.codigo_unidade}")
        
        # Movimentos
        for i, mov in enumerate(self.movimentos, start=2):
            descricao = f"Adq: {mov.codigo_adquirente}, Cartão: {mov.numero_cartao.strip()}, Data: {mov.data_venda}"
            valor = f"R$ {mov.get_valor_decimal():.2f}"
            print(f"{i:<5} {'M':<5} {descricao:<50} {valor:<15}")
        
        # Trailer
        linha_trailer = len(self.movimentos) + 2
        total_registros = self.trailer.get_total_registros()
        valor_total = self.trailer.get_valor_total_decimal()
        print(f"{linha_trailer:<5} {'T':<5} Total de registros: {total_registros:<20} R$ {valor_total:.2f}")

# Funções para manipulação do arquivo

def salvar_arquivo_como(arquivo: ArquivoMovimentacao):
    """Solicita ao usuário um novo nome de arquivo e salva o arquivo com esse nome"""
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=== Salvar Como ===\n")
    novo_nome = input("Digite o novo nome do arquivo: ")
    if novo_nome:
        try:
            arquivo.salvar_arquivo(novo_nome)
            log_operacao("SALVAR_COMO", f"Arquivo salvo como '{novo_nome}' com sucesso")
            print(f"\nArquivo salvo como '{novo_nome}' com sucesso.")
            input("Pressione Enter para continuar...")
        except Exception as e:
            log_operacao("ERRO_SALVAR_COMO", f"Erro ao salvar arquivo como '{novo_nome}': {e}")
            print(f"\nErro ao salvar arquivo: {e}")
            input("Pressione Enter para continuar...")

def salvar_arquivo(arquivo: ArquivoMovimentacao):
    """Salva o arquivo usando o caminho já definido"""
    try:
        arquivo.salvar_arquivo()
        log_operacao("SALVAR_ARQUIVO", f"Arquivo salvo com sucesso em '{arquivo.caminho_arquivo}'")
        print("\nArquivo salvo com sucesso.")
        input("Pressione Enter para continuar...")
    except Exception as e:
        log_operacao("ERRO_SALVAR", f"Erro ao salvar arquivo: {e}")
        print(f"\nErro ao salvar arquivo: {e}")
        input("Pressione Enter para continuar...")


def editar_movimento(arquivo: ArquivoMovimentacao, indice: int):
    """Edita um registro de movimento"""
    if 0 <= indice < len(arquivo.movimentos):
        mov = arquivo.movimentos[indice]
        log_operacao("EDITAR_REGISTRO", f"Iniciando edição do registro {indice + 1}")
        print(f"\nEditando registro {indice + 1}:")
        print(f"1. Código Adquirente: {mov.codigo_adquirente}")
        print(f"2. Data Movimento: {mov.data_movimento}")
        print(f"3. Número Cartão: {mov.numero_cartao.strip()}")
        print(f"4. Parcelas: {mov.parcelas}")
        print(f"5. Valor Venda: R$ {mov.get_valor_decimal():.2f}")
        print(f"6. Data Venda: {mov.data_venda}")
        print(f"7. CVNSU: {mov.cvnsu}")
        print(f"8. CPF/CNPJ: {mov.cpf_cnpj.strip()}")
        print(f"9. Número Pedido: {mov.numero_pedido.strip()}")
        
        opcao = input("\nSelecione o campo para editar (1-9) ou 0 para cancelar: ")
        
        campo_editado = None
        if opcao == '1':
            novo_valor = input(f"Novo Código Adquirente ({mov.codigo_adquirente}): ")
            if novo_valor:
                mov.codigo_adquirente = novo_valor.ljust(2)[:2]
                campo_editado = "Código Adquirente"
        elif opcao == '2':
            novo_valor = input(f"Nova Data Movimento ({mov.data_movimento}): ")
            if novo_valor:
                mov.data_movimento = novo_valor.ljust(8)[:8]
                campo_editado = "Data Movimento"
        elif opcao == '3':
            novo_valor = input(f"Novo Número Cartão ({mov.numero_cartao.strip()}): ")
            if novo_valor:
                mov.numero_cartao = novo_valor.ljust(20)[:20]
                campo_editado = "Número Cartão"
        elif opcao == '4':
            novo_valor = input(f"Novas Parcelas ({mov.parcelas}): ")
            if novo_valor:
                mov.parcelas = novo_valor.zfill(2)[:2]
                campo_editado = "Parcelas"
        elif opcao == '5':
            novo_valor = input(f"Novo Valor Venda ({mov.get_valor_decimal():.2f}): ")
            if novo_valor:
                try:
                    valor_float = float(novo_valor)
                    mov.set_valor_decimal(valor_float)
                    campo_editado = "Valor Venda"
                except ValueError:
                    print("Valor inválido.")
                    log_operacao("ERRO_EDICAO", f"Valor inválido informado para Valor Venda: {novo_valor}")
        elif opcao == '6':
            novo_valor = input(f"Nova Data Venda ({mov.data_venda}): ")
            if novo_valor:
                mov.data_venda = novo_valor.ljust(8)[:8]
                campo_editado = "Data Venda"
        elif opcao == '7':
            novo_valor = input(f"Novo CVNSU ({mov.cvnsu}): ")
            if novo_valor:
                mov.cvnsu = novo_valor.ljust(15)[:15]
                campo_editado = "CVNSU"
        elif opcao == '8':
            novo_valor = input(f"Novo CPF/CNPJ ({mov.cpf_cnpj.strip()}): ")
            if novo_valor:
                mov.cpf_cnpj = novo_valor.ljust(14)[:14]
                campo_editado = "CPF/CNPJ"
        elif opcao == '9':
            novo_valor = input(f"Novo Número Pedido ({mov.numero_pedido.strip()}): ")
            if novo_valor:
                mov.numero_pedido = novo_valor.ljust(10)[:10]
                campo_editado = "Número Pedido"
        
        # Recalcular trailer após edição
        arquivo.recalcular_trailer()
        if campo_editado:
            log_operacao("EDITAR_REGISTRO", f"Registro {indice + 1} - Campo '{campo_editado}' modificado. Trailer recalculado.")
        print("\nRegistro atualizado e trailer recalculado.")
    else:
        print("Índice inválido.")

def deletar_movimento(arquivo: ArquivoMovimentacao, indice: int):
    """Deleta um registro de movimento"""
    if 0 <= indice < len(arquivo.movimentos):
        log_operacao("DELETAR_REGISTRO", f"Deletando registro {indice + 1}")
        del arquivo.movimentos[indice]
        arquivo.recalcular_trailer()
        log_operacao("DELETAR_REGISTRO", f"Registro {indice + 1} deletado e trailer recalculado")
        print("\nRegistro deletado e trailer recalculado.")
    else:
        log_operacao("ERRO_DELECAO", f"Tentativa de deletar registro inválido: {indice}")
        print("Índice inválido.")

def excluir_por_adquirente(arquivo: ArquivoMovimentacao, codigo_adquirente: str):
    """Exclui registros por código de adquirente"""
    total_registros_original = len(arquivo.movimentos)
    registros_excluidos = 0
    
    # Percorrer de trás para frente para evitar problemas com índices
    for i in range(len(arquivo.movimentos) - 1, -1, -1):
        if arquivo.movimentos[i].codigo_adquirente == codigo_adquirente:
            log_operacao("EXCLUIR_POR_ADQUIRENTE", f"Excluindo registro {i} do adquirente {codigo_adquirente}")
            del arquivo.movimentos[i]
            registros_excluidos += 1
    
    # Recalcular trailer
    arquivo.recalcular_trailer()
    
    log_operacao("EXCLUIR_POR_ADQUIRENTE", f"{registros_excluidos} registro(s) excluído(s) para o adquirente {codigo_adquirente} e trailer recalculado")
    print(f"\n{registros_excluidos} registro(s) excluído(s) para o adquirente {codigo_adquirente} e trailer recalculado.")

def escolher_registros(arquivo: ArquivoMovimentacao):
    """Permite ao usuário escolher quais registros manter no arquivo, excluindo os demais"""
    import time
    
    inicio = time.time()
    log_operacao("ESCOLHER_REGISTROS", "Iniciando seleção manual de registros")
    
    if not arquivo.movimentos:
        print("\nNenhum registro de movimento para selecionar.")
        return
    
    # Exibir todos os registros com seus índices
    print("\n===== Registros disponíveis =====")
    print("Índice | Adquirente | Valor | Data")
    print("-" * 40)
    
    for i, mov in enumerate(arquivo.movimentos):
        valor = mov.get_valor_decimal()
        adquirente = mov.codigo_adquirente
        data = mov.data_movimento
        print(f"{i:6d} | {adquirente:10s} | R$ {valor:9.2f} | {data}")
    
    print("\nDigite os índices dos registros que deseja manter, separados por vírgula.")
    print("Exemplo: 0,3,5,10")
    
    try:
        indices_str = input("Índices a manter: ")
        indices_manter = [int(idx.strip()) for idx in indices_str.split(',') if idx.strip()]
        
        # Validar índices
        indices_invalidos = [idx for idx in indices_manter if idx < 0 or idx >= len(arquivo.movimentos)]
        if indices_invalidos:
            print(f"\nÍndices inválidos: {indices_invalidos}")
            return
        
        # Confirmar a seleção
        print(f"\nVocê selecionou {len(indices_manter)} registro(s) para manter.")
        confirmacao = input("Confirmar exclusão dos demais registros? (S/N): ").upper()
        
        if confirmacao != 'S':
            print("\nOperação cancelada.")
            return
        
        # Remover registros que NÃO estão na lista de índices a manter
        registros_excluidos = 0
        for i in range(len(arquivo.movimentos) - 1, -1, -1):
            if i not in indices_manter:
                log_operacao("ESCOLHER_REGISTROS", f"Excluindo registro {i} (não selecionado)")
                del arquivo.movimentos[i]
                registros_excluidos += 1
        
        # Recalcular trailer
        arquivo.recalcular_trailer()
        
        tempo_total = time.time() - inicio
        log_operacao("ESCOLHER_REGISTROS", f"{len(indices_manter)} registro(s) mantido(s), {registros_excluidos} excluído(s), tempo: {tempo_total:.2f}s")
        print(f"\n{len(indices_manter)} registro(s) mantido(s), {registros_excluidos} excluído(s).")
        print(f"Trailer recalculado com sucesso.")
        print(f"Tempo de processamento: {tempo_total:.2f} segundos")
        
    except ValueError as e:
        print(f"\nErro ao processar índices: {e}")
        log_operacao("ESCOLHER_REGISTROS", f"Erro ao processar índices: {e}")

def selecionar_por_valor(arquivo: ArquivoMovimentacao, valor_desejado: float):
    """Seleciona registros cuja soma dos valores seja EXATAMENTE igual ao valor desejado"""
    import time
    from itertools import combinations
    
    inicio = time.time()
    log_operacao("SELECAO_POR_VALOR", f"Iniciando seleção por valor exato: {valor_desejado:.2f}")
    print("\nProcessando seleção por valor exato. Isso pode levar alguns segundos...")
    
    # Converter registros para lista de (índice, valor)
    registros_com_valores = [(i, mov.get_valor_decimal()) for i, mov in enumerate(arquivo.movimentos)]
    
    # Definir uma tolerância extremamente baixa para garantir valores exatos
    TOLERANCIA = 0.001  # Tolerância de 0.001 para evitar problemas de precisão com números de ponto flutuante
    
    # Implementar algoritmo de busca binária para encontrar combinação exata
    def encontrar_combinacao_exata(registros, valor_alvo, tolerancia=TOLERANCIA):
        # Ordenar registros por valor (decrescente) para otimizar a busca
        registros_ordenados = sorted(registros, key=lambda x: x[1], reverse=True)
        total_registros = len(registros_ordenados)
        
        # Usar programação dinâmica para encontrar combinações exatas
        # Abordagem baseada no problema da mochila (knapsack)
        def buscar_combinacao_dp(idx_atual, valor_restante, combinacao_atual, memo={}):
            # Chave para memorização
            chave = (idx_atual, round(valor_restante, 4))
            
            # Se já calculamos esta combinação antes, retornar resultado memorizado
            if chave in memo:
                return memo[chave]
            
            # Se encontramos uma combinação exata (usando tolerância mínima)
            if abs(valor_restante) < tolerancia:
                return combinacao_atual
            
            # Se chegamos ao final dos registros ou valor restante é negativo
            if idx_atual >= total_registros or valor_restante < -tolerancia:
                return None
            
            # Tentar incluir o registro atual
            idx, valor = registros_ordenados[idx_atual]
            combinacao_com = buscar_combinacao_dp(
                idx_atual + 1, 
                valor_restante - valor, 
                combinacao_atual + [(idx, valor)],
                memo
            )
            
            # Se encontramos uma combinação válida incluindo o registro atual
            if combinacao_com:
                memo[chave] = combinacao_com
                return combinacao_com
            
            # Tentar sem incluir o registro atual
            combinacao_sem = buscar_combinacao_dp(
                idx_atual + 1, 
                valor_restante, 
                combinacao_atual,
                memo
            )
            
            memo[chave] = combinacao_sem
            return combinacao_sem
        
        # Iniciar busca com programação dinâmica
        return buscar_combinacao_dp(0, valor_alvo, [])
    
    # Tentar encontrar uma combinação exata
    print("Buscando combinação exata de registros...")
    combinacao_exata = encontrar_combinacao_exata(registros_com_valores, valor_desejado)
    
    # Se não encontramos uma combinação exata com programação dinâmica,
    # tentar com força bruta para combinações pequenas
    if not combinacao_exata and len(registros_com_valores) <= 30:
        print("Tentando busca exaustiva para combinações menores...")
        for r in range(1, min(len(registros_com_valores) + 1, 11)):  # Limitar para evitar explosão combinatória
            for combinacao in combinations(registros_com_valores, r):
                soma = sum(valor for _, valor in combinacao)
                if abs(soma - valor_desejado) < TOLERANCIA:  # Usando tolerância mínima para garantir exatidão
                    combinacao_exata = combinacao
                    break
            if combinacao_exata:
                break
    
    # Se ainda não encontramos uma combinação exata, tentar com algoritmo guloso otimizado
    if not combinacao_exata and len(registros_com_valores) > 30:
        print("Tentando algoritmo guloso otimizado...")
        
        # Ordenar registros por valor
        registros_ordenados = sorted(registros_com_valores, key=lambda x: x[1])
        
        # Usar algoritmo guloso com backtracking limitado
        def busca_gulosa_com_backtracking(registros, valor_alvo):
            melhor_combinacao = None
            menor_diferenca = float('inf')
            
            # Função recursiva para busca com backtracking
            def backtrack(idx, combinacao_atual, soma_atual):
                nonlocal melhor_combinacao, menor_diferenca
                
                # Verificar se encontramos uma combinação exata
                diferenca = abs(soma_atual - valor_alvo)
                if diferenca < menor_diferenca:
                    menor_diferenca = diferenca
                    melhor_combinacao = combinacao_atual.copy()
                
                # Se encontramos uma combinação exata, podemos parar
                if diferenca < TOLERANCIA:
                    return True
                
                # Se chegamos ao final dos registros
                if idx >= len(registros):
                    return False
                
                # Tentar incluir o registro atual
                if soma_atual + registros[idx][1] <= valor_alvo * (1 + TOLERANCIA/10):  # Tolerância ainda mais restrita
                    combinacao_atual.append(registros[idx])
                    if backtrack(idx + 1, combinacao_atual, soma_atual + registros[idx][1]):
                        return True
                    combinacao_atual.pop()
                
                # Tentar sem incluir o registro atual
                return backtrack(idx + 1, combinacao_atual, soma_atual)
            
            # Iniciar backtracking
            backtrack(0, [], 0.0)
            
            # Só retornar se for uma combinação exata
            if menor_diferenca < TOLERANCIA:
                return melhor_combinacao
            return None
        
        combinacao_exata = busca_gulosa_com_backtracking(registros_ordenados, valor_desejado)
    
    # Se não encontramos uma combinação exata
    if not combinacao_exata:
        log_operacao("SELECAO_POR_VALOR", "Nenhuma combinação exata encontrada")
        print("\nNenhuma combinação de registros encontrada que some EXATAMENTE o valor desejado.")
        print("Por favor, tente outro valor ou use a opção de edição manual.")
        return
    
    # Obter índices dos registros selecionados
    indices_selecionados = {indice for indice, _ in combinacao_exata}
    soma_selecionada = sum(valor for _, valor in combinacao_exata)
    
    # Remover registros que NÃO estão na combinação selecionada
    registros_excluidos = 0
    for i in range(len(arquivo.movimentos) - 1, -1, -1):
        if i not in indices_selecionados:
            log_operacao("SELECAO_POR_VALOR", f"Excluindo registro {i} (não selecionado)")
            del arquivo.movimentos[i]
            registros_excluidos += 1
    
    # Recalcular trailer
    arquivo.recalcular_trailer()
    
    tempo_total = time.time() - inicio
    log_operacao("SELECAO_POR_VALOR", f"{len(indices_selecionados)} registro(s) mantido(s), {registros_excluidos} excluído(s), soma: {soma_selecionada:.2f}, tempo: {tempo_total:.2f}s")
    print(f"\n{len(indices_selecionados)} registro(s) mantido(s), {registros_excluidos} excluído(s).")
    print(f"Soma dos registros selecionados: R$ {soma_selecionada:.2f}")
    print(f"Valor desejado: R$ {valor_desejado:.2f}")
    print(f"Diferença: R$ {abs(soma_selecionada - valor_desejado):.5f}")  # Mostrar mais casas decimais para verificar a precisão
    print(f"Tempo de processamento: {tempo_total:.2f} segundos")

def selecionar_arquivo() -> str:
    """Permite ao usuário selecionar um arquivo usando interface TUI"""
    from seletor_arquivo_tui import selecionar_arquivo_tui
    return selecionar_arquivo_tui('.')


def menu_principal():
    """Menu principal da aplicação usando interface TUI"""
    arquivo_atual = None
    
    while True:
        # Limpar a tela
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Iniciar o menu TUI
        menu = MenuPrincipalTUI(arquivo_atual)
        opcao, parametros = menu.executar()
        
        # Processar a opção selecionada
        if opcao == "carregar_arquivo":
            nome_arquivo = selecionar_arquivo()
            if nome_arquivo:
                try:
                    arquivo_atual = ArquivoMovimentacao(nome_arquivo)
                    log_operacao("CARREGAR_ARQUIVO", f"Arquivo {nome_arquivo} carregado com sucesso")
                except Exception as e:
                    print(f"\nErro ao carregar arquivo: {e}")
                    input("Pressione Enter para continuar...")
        
        elif opcao == "visualizar_conteudo" and arquivo_atual:
            # Usar a planilha para visualizar o conteúdo e permitir ações diretas
            planilha = PlanilhaRegistros(arquivo_atual, modo_somente_leitura=False)
            resultado = planilha.executar()
            
            # Processar resultado das ações diretas
            if resultado and "acao" in resultado:
                # Processar menu de operações em lote
                if resultado["acao"] == "menu_operacoes":
                    planilha.exibir_menu_operacoes()
                    # Reexibir a planilha após as operações
                    opcao = "visualizar_conteudo"
                    continue
                if resultado["acao"] == "editar" and "indice" in resultado:
                    editar_movimento(arquivo_atual, resultado["indice"])
                elif resultado["acao"] == "selecionar_por_valor":
                    os.system('clear' if os.name == 'posix' else 'cls')
                    print("=== Seleção por Valor ===")
                    try:
                        valor_str = input("\nDigite o valor desejado (ex: 2564.00): ")
                        valor = float(valor_str)
                        if valor > 0:
                            selecionar_por_valor(arquivo_atual, valor)
                        else:
                            print("Valor inválido. Deve ser maior que zero.")
                            input("Pressione Enter para continuar...")
                    except ValueError:
                        print("Valor inválido. Digite um número decimal.")
                        input("Pressione Enter para continuar...")
                elif resultado["acao"] == "excluir_por_adquirente":
                    os.system('clear' if os.name == 'posix' else 'cls')
                    print("=== Excluir por Adquirente ===")
                    codigo = input("\nDigite o código do adquirente (2 dígitos): ")
                    if len(codigo) == 2 and codigo.isdigit():
                        excluir_por_adquirente(arquivo_atual, codigo)
                    else:
                        print("Código inválido. Deve ter 2 dígitos.")
                        input("Pressione Enter para continuar...")
                elif resultado["acao"] == "salvar":
                    if arquivo_atual.caminho_arquivo:
                        salvar_arquivo(arquivo_atual)
                    else:
                        salvar_arquivo_como(arquivo_atual)
                elif resultado["acao"] == "salvar_como":
                    salvar_arquivo_como(arquivo_atual)
        
        elif opcao == "editar_registro" and arquivo_atual:
            if arquivo_atual.movimentos:
                # Usar a planilha para selecionar o registro a editar
                planilha = PlanilhaRegistros(arquivo_atual, modo_somente_leitura=True)
                resultado = planilha.executar()
                
                # Se um registro foi selecionado
                if resultado and resultado.get("selecionado") is not None:
                    indice = resultado["selecionado"]
                    editar_movimento(arquivo_atual, indice)
            else:
                print("\nNenhum registro de movimento para editar.")
                input("Pressione Enter para continuar...")
        
        elif opcao == "deletar_registro" and arquivo_atual:
            if arquivo_atual.movimentos:
                # Usar a planilha para selecionar o registro a deletar
                planilha = PlanilhaRegistros(arquivo_atual, modo_somente_leitura=True)
                resultado = planilha.executar()
                
                # Se um registro foi selecionado
                if resultado and resultado.get("selecionado") is not None:
                    indice = resultado["selecionado"]
                    deletar_movimento(arquivo_atual, indice)
            else:
                print("\nNenhum registro de movimento para deletar.")
                input("Pressione Enter para continuar...")
        
        elif opcao == "excluir_por_adquirente" and arquivo_atual:
            # Interface TUI para selecionar adquirente
            # Por enquanto, usar entrada simples
            os.system('clear' if os.name == 'posix' else 'cls')
            print("=== Excluir por Adquirente ===")
            codigo = input("\nDigite o código do adquirente (2 dígitos): ")
            if len(codigo) == 2 and codigo.isdigit():
                excluir_por_adquirente(arquivo_atual, codigo)
            else:
                print("Código inválido. Deve ter 2 dígitos.")
                input("Pressione Enter para continuar...")
        
        elif opcao == "selecionar_por_valor" and arquivo_atual:
            # Interface TUI para selecionar valor
            # Por enquanto, usar entrada simples
            os.system('clear' if os.name == 'posix' else 'cls')
            print("=== Seleção por Valor ===")
            try:
                valor_str = input("\nDigite o valor desejado (ex: 2564.00): ")
                valor = float(valor_str)
                if valor > 0:
                    selecionar_por_valor(arquivo_atual, valor)
                else:
                    print("Valor inválido. Deve ser maior que zero.")
                    input("Pressione Enter para continuar...")
            except ValueError:
                print("Valor inválido. Deve ser um número decimal.")
                input("Pressione Enter para continuar...")
        
        elif opcao == "escolher_registros" and arquivo_atual:
            escolher_registros(arquivo_atual)
        
        elif opcao == "visualizar_planilha" and arquivo_atual:
            # Iniciar interface de planilha
            planilha = PlanilhaRegistros(arquivo_atual)
            planilha.executar()
        
        elif opcao == "salvar" and arquivo_atual:
            try:
                arquivo_atual.salvar_arquivo()
                print("\nArquivo salvo com sucesso.")
                input("Pressione Enter para continuar...")
            except Exception as e:
                print(f"\nErro ao salvar arquivo: {e}")
                input("Pressione Enter para continuar...")
        
        elif opcao == "salvar_como" and arquivo_atual:
            os.system('clear' if os.name == 'posix' else 'cls')
            print("=== Salvar Como ===")
            novo_nome = input("\nDigite o novo nome do arquivo: ")
            if novo_nome:
                try:
                    arquivo_atual.salvar_arquivo(novo_nome)
                    print(f"\nArquivo salvo como '{novo_nome}' com sucesso.")
                    input("Pressione Enter para continuar...")
                except Exception as e:
                    print(f"\nErro ao salvar arquivo: {e}")
                    input("Pressione Enter para continuar...")
        
        elif opcao == "fechar_arquivo" and arquivo_atual:
            arquivo_atual = None
            print("\nArquivo fechado.")
            input("Pressione Enter para continuar...")
        
        elif opcao == "sair":
            print("\nSaindo da aplicação.")
            break

if __name__ == "__main__":
    # Mudar para o diretório do script
    os.chdir(os.path.dirname(os.path.abspath(__file__)) if os.path.abspath(__file__) != '/home/peder/Projetos/EditCobol' else '/home/peder/Projetos/EditCobol')
    menu_principal()
