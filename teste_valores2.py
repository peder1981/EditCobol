#!/usr/bin/env python3

# Script para testar a interpretação dos valores no arquivo corrigido

with open('/home/peder/Projetos/EditCobol/exemplo_valido.txt', 'r') as f:
    linhas = [linha.rstrip('\n') for linha in f.readlines()]

# Registro de movimento 1
linha1 = linhas[1]
print("Registro 1:")
print(f"Linha completa: {linha1}")
print(f"Tamanho: {len(linha1)}")
print(f"Campo valor (posições 34-50): '{linha1[33:50]}'")
valor1 = int(linha1[33:50])
print(f"Valor em centavos: {valor1}")
print(f"Valor em reais: {valor1/100}")

print()

# Registro de movimento 2
linha2 = linhas[2]
print("Registro 2:")
print(f"Linha completa: {linha2}")
print(f"Tamanho: {len(linha2)}")
print(f"Campo valor (posições 34-50): '{linha2[33:50]}'")
valor2 = int(linha2[33:50])
print(f"Valor em centavos: {valor2}")
print(f"Valor em reais: {valor2/100}")

print()

# Soma
soma = valor1 + valor2
print(f"Soma dos valores em centavos: {soma}")
print(f"Soma dos valores em reais: {soma/100}")

print()

# Trailer
linha_trailer = linhas[3]
print("Trailer:")
print(f"Linha completa: {linha_trailer}")
print(f"Tamanho: {len(linha_trailer)}")
print(f"Campo total registros (posições 2-6): '{linha_trailer[1:6]}'")
print(f"Campo valor total (posições 8-16): '{linha_trailer[7:16]}'")
total_registros = int(linha_trailer[1:6])
valor_total = int(linha_trailer[7:16])
print(f"Total de registros: {total_registros}")
print(f"Valor total em centavos: {valor_total}")
print(f"Valor total em reais: {valor_total/100}")

print()

# Verificação
print(f"Valores batem? {soma == valor_total}")
print(f"Número de registros bate? {total_registros == 2}")
