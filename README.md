# Editor de Arquivo de Movimentação Financeira

Aplicação Python para manipulação de arquivos de movimentação financeira com estrutura de largura fixa. A aplicação utiliza uma interface TUI (Text User Interface) baseada em prompt_toolkit para proporcionar uma experiência interativa no terminal.

## Estrutura do Arquivo

O arquivo segue o formato especificado com três tipos de registros:

1. **Registro Header (H)** - Identifica o início do arquivo
2. **Registros de Movimento (M)** - Contêm as informações das transações
3. **Registro Trailer (T)** - Identifica o fim do arquivo e contém informações de controle

Todos os registros possuem exatamente 91 caracteres. Para detalhes completos sobre a estrutura do arquivo, consulte o documento [estrutura_arquivo_movimentacao.md](estrutura_arquivo_movimentacao.md).

## Funcionalidades

- Carregamento e validação de arquivos de movimentação financeira
- Exibição do conteúdo em formato de planilha interativa
- Edição de registros de movimento com validação de campos
- Seleção e exclusão de registros individuais ou em grupo
- Exclusão de registros por código de adquirente
- Filtragem e seleção de registros por valor
- Recálculo automático do trailer após edições
- Salvar e salvar como com confirmação
- Interface TUI com cores padronizadas e responsiva
- Diálogos de confirmação para ações destrutivas
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

2. Selecione um arquivo de movimentação para abrir usando o seletor de arquivos

3. Utilize as opções do menu para manipular o arquivo

4. Na planilha de registros, use as teclas de função (F2-F8) para realizar operações

### Teclas de Função

A aplicação utiliza diversas teclas de função para facilitar a navegação e operações. Consulte o documento [TECLAS_FUNCAO.md](TECLAS_FUNCAO.md) para um guia completo de todas as teclas disponíveis em cada tela.

## Logging

A aplicação registra todas as operações em um arquivo de log (`log.txt`) para fins de auditoria e depuração. Os logs incluem timestamps, níveis de severidade (INFO, ERROR) e descrições detalhadas das operações realizadas.

## Documentação Adicional

- [TECLAS_FUNCAO.md](TECLAS_FUNCAO.md) - Guia completo de todas as teclas de função
- [estrutura_arquivo_movimentacao.md](estrutura_arquivo_movimentacao.md) - Detalhamento da estrutura do arquivo
- [RESUMO_PROJETO.md](RESUMO_PROJETO.md) - Visão geral e resumo do projeto

## Requisitos

- Python 3.6 ou superior
- prompt_toolkit
- rich (para formatação de logs)

## Contribuição

Para contribuir com o projeto, siga estas etapas:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Faça push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

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
