# Editor de Arquivo de Movimentação Financeira

Aplicação Python para manipulação de arquivos de movimentação financeira com estrutura de largura fixa.

## Estrutura do Arquivo

O arquivo segue o formato especificado com três tipos de registros:

1. **Registro Header (H)** - Identifica o início do arquivo
2. **Registros de Movimento (M)** - Contêm as informações das transações
3. **Registro Trailer (T)** - Identifica o fim do arquivo e contém informações de controle

Todos os registros possuem exatamente 91 caracteres.

## Funcionalidades

- Carregamento e validação de arquivos de movimentação financeira
- Exibição do conteúdo em formato de planilha
- Edição de registros de movimento
- Exclusão de registros individuais
- Exclusão de registros por código de adquirente
- Recálculo automático do trailer após edições
- Salvar e salvar como
- Logging detalhado de todas as operações
- Visualização de logs formatada

## Como Usar

### Método 1: Script de inicialização (recomendado)

Execute o script de inicialização que reúne todas as funcionalidades:

```
python3 iniciar_app.py
```

### Método 2: Execução direta

1. Execute a aplicação principal:
   ```
   python3 financeiro_app.py
   ```

2. Selecione um arquivo de movimentação para abrir

3. Utilize as opções do menu para manipular o arquivo

## Logging

A aplicação registra todas as operações em um arquivo de log (`log.txt`) para fins de auditoria e depuração. 

Para visualizar os logs de forma formatada, execute o script de visualização:

```
python3 visualizar_logs.py
```

## Backup de Arquivos

Para criar backups dos arquivos de movimentação financeira, execute o script de backup:

```
python3 backup_arquivos.py
```

O script permite:
- Criar backups automáticos dos arquivos
- Listar backups disponíveis
- Restaurar backups anteriores

## Testes Automatizados

Para executar os testes automatizados da aplicação, execute o script de teste:

```
python3 teste_automatizado.py
```

O script executa testes para verificar:
- Carregamento e validação de arquivos
- Edição de registros
- Deleção de registros
- Exclusão de registros por adquirente

## Requisitos

- Python 3.x

## Exemplo de Uso

Ao executar a aplicação, você verá um menu com as seguintes opções:

```
===== Editor de Arquivo de Movimentação Financeira =====
Nenhum arquivo aberto

Opções:
1. Abrir arquivo
0. Sair
```

Selecione a opção 1 para abrir um arquivo. A aplicação lista todos os arquivos no diretório atual.

Após abrir um arquivo, as seguintes opções ficam disponíveis:

- Exibir conteúdo: Mostra os registros em formato de planilha
- Editar registro: Permite modificar campos de um registro de movimento
- Deletar registro: Remove um registro de movimento
- Excluir registros por adquirente: Remove todos os registros de um adquirente específico
- Salvar: Grava as alterações no arquivo original
- Salvar como...: Grava as alterações em um novo arquivo
- Fechar arquivo: Fecha o arquivo atual
