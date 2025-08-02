# Estrutura de Arquivo de Movimentação Financeira

## Visão Geral

Este documento descreve a estrutura do arquivo de movimentação financeira utilizado no sistema. O arquivo segue um formato de largura fixa com registros padronizados contendo informações de transações financeiras.

## Estrutura Geral

O arquivo é composto por três tipos de registros, cada um com exatamente 91 caracteres seguidos por um caractere de quebra de linha (LF):

1. **Registro Header (H)** - Identifica o início do arquivo
2. **Registros de Movimento (M)** - Contêm as informações das transações
3. **Registro Trailer (T)** - Identifica o fim do arquivo e contém informações de controle

## Detalhamento dos Registros

### Registro Header (H)

O registro Header identifica o início do arquivo e contém informações gerais sobre a data e unidade de processamento.

| Posição | Tamanho | Descrição | Formato | Exemplo |
|---------|---------|-----------|---------|---------|
| 1 | 1 | Identificador do registro | Caractere | H |
| 2-9 | 8 | Data de processamento | YYYYMMDD | 20250616 |
| 10-11 | 2 | Código da unidade | Numérico | UN |
| 12-19 | 8 | Data de processamento (repetida) | YYYYMMDD | 20250616 |
| 20-27 | 8 | Espaços em branco | Caracteres | ' ' (8 espaços) |
| 28-91 | 64 | Zeros de preenchimento | Numérico | 0000000000000000000000000000000000000000000000000000000000000000 |

**Exemplo completo:**
```
H20250616UN20250616        0000000000000000000000000000000000000000000000000000000000000000
```

### Registro de Movimento (M)

Os registros de movimento contêm as informações detalhadas de cada transação financeira.

| Posição | Tamanho | Descrição | Formato | Exemplo |
|---------|---------|-----------|---------|---------|
| 1 | 1 | Identificador do registro | Caractere | M |
| 2-3 | 2 | Código da adquirente/administradora | Numérico | 46, 03 |
| 4-11 | 8 | Data do movimento | YYYYMMDD | 20250610 |
| 12-31 | 20 | Número do cartão de crédito | Numérico | 4660790000009824 |
| 32-33 | 2 | Número total de parcelas | Numérico | 02 |
| 34-50 | 17 | Valor da venda | Numérico (2 decimais) | 0000000000017100 |
| 51-58 | 8 | Data da venda | YYYYMMDD | 20250616 |
| 59-67 | 9 | CVNSU da venda | Numérico | 335525646 |
| 68-69 | 2 | Zeros fixos | Numérico | 00 |
| 70-84 | 15 | CPF/CNPJ do responsável | Numérico | 000050620030001 |
| 85-91 | 7 | Número do pedido | Numérico | 7300000 |

**Exemplo completo:**
```
M462025061046607900000098240000020000000000001710020250616335525646000050620030001730000000
```

### Registro Trailer (T)

O registro Trailer identifica o fim do arquivo e contém informações de controle e totalização.

| Posição | Tamanho | Descrição | Formato | Exemplo |
|---------|---------|-----------|---------|---------|
| 1 | 1 | Identificador do registro | Caractere | T |
| 2-6 | 5 | Total de registros tipo M | Numérico (zeros à esquerda) | 00106 |
| 7 | 1 | Espaço em branco | Caractere | ' ' |
| 8-16 | 9 | Valor total das vendas | Numérico (2 decimais, zeros à esquerda) | 008956028 |
| 17-91 | 75 | Preenchimento com noves | Numérico | 99999999999999999999999999999999999999999999999999999999999999999999999 |

**Exemplo completo:**
```
T00106 008956028999999999999999999999999999999999999999999999999999999999999999999999999999
```

## Considerações Importantes

1. **Tamanho Fixo**: Todos os registros devem ter exatamente 91 caracteres, exceto pelo caractere de quebra de linha.
2. **Alinhamento**: Campos numéricos são alinhados à direita e preenchidos com zeros à esquerda quando necessário.
3. **Valores Decimais**: Em campos monetários, os dois últimos dígitos representam a parte decimal.
4. **Consistência**: Não há variações permitidas na estrutura dos registros. Qualquer desvio deve ser considerado um erro no arquivo.

## Exemplo de Arquivo Completo

```
H20250616UN20250616        0000000000000000000000000000000000000000000000000000000000000000
M462025061046607900000098240000020000000000001710020250616335525646000050620030001730000000
M0320250530230888XXXXXX10860000060000000000030000020250616017074932000044309830001570000000
T00002 000004710999999999999999999999999999999999999999999999999999999999999999999999999999
```

## Validação

Ao processar um arquivo, as seguintes validações devem ser realizadas:

1. Verificar se o primeiro registro é do tipo Header (H)
2. Verificar se o último registro é do tipo Trailer (T)
3. Contar o número de registros tipo M e comparar com o valor no Trailer
4. Somar os valores das vendas dos registros tipo M e comparar com o valor no Trailer
5. Verificar se todos os registros têm o tamanho correto de 91 caracteres
