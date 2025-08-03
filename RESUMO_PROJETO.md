# Resumo do Projeto - Editor de Arquivo de Movimentação Financeira

## Descrição Geral

O projeto consiste em uma aplicação Python para manipulação de arquivos de movimentação financeira em formato de largura fixa, com funcionalidades avançadas de edição, validação, logging e backup. A interface utiliza o framework prompt_toolkit para criar uma experiência TUI (Text User Interface) interativa e responsiva no terminal.

## Funcionalidades Implementadas

### 1. Editor Principal (`financeiro_app.py`)
- Carregamento e validação de arquivos de movimentação financeira
- Exibição formatada do conteúdo do arquivo
- Edição de registros individuais
- Seleção e deleção de registros
- Exclusão de registros por código de adquirente
- Filtragem e seleção de registros por valor
- Recálculo automático do trailer
- Salvamento de arquivos com confirmação

### 2. Validação de Estrutura
- Verificação de tamanho de linhas (91 caracteres)
- Validação de tipos de registro (Header, Movimento, Trailer)
- Consistência de valores monetários
- Contagem de registros

### 3. Sistema de Logging (`log.txt`)
- Registro detalhado de todas as operações
- Timestamps para auditoria
- Níveis de log (INFO, ERROR)
- Visualização formatada dos logs (`visualizar_logs.py`)

### 4. Backup de Arquivos (`backup_arquivos.py`)
- Criação de backups automáticos
- Listagem de backups disponíveis
- Restauração de backups com confirmação
- Organização em diretório dedicado

### 5. Testes Automatizados (`teste_automatizado.py`)
- Testes unitários para todas as funcionalidades principais
- Validação de carregamento de arquivos
- Testes de edição e deleção de registros
- Testes de exclusão por adquirente

### 6. Scripts de Apoio
- Script de inicialização (`iniciar_app.py`)
- Script de instalação (`install.sh`)
- Script de execução (`run.sh`)
- Link simbólico para acesso fácil (`editor-financeiro`)
- Scripts de teste para validação de componentes (`teste_dialogos.py`, `teste_tui_adaptado.py`)

### 7. Interface TUI (`menu_principal_tui.py`, `seletor_arquivo_tui.py`, `planilha_registros.py`)
- Menu principal interativo com navegação por teclado
- Seletor de arquivos com navegação e paginação
- Planilha de registros com suporte a teclas de função (F2-F8)
- Diálogos de confirmação padronizados
- Estilos e cores consistentes em todas as telas
- Feedback visual para ações do usuário

### 8. Teclas de Função (`TECLAS_FUNCAO.md`)
- Documentação completa de todas as teclas de função
- Teclas F2-F8 para operações na planilha de registros
- Teclas de navegação padronizadas em todas as telas
- Atalhos para ações comuns

### 9. Documentação
- Documento de estrutura do arquivo (`estrutura_arquivo_movimentacao.md`)
- Guia de teclas de função (`TECLAS_FUNCAO.md`)
- README com instruções detalhadas
- Resumo do projeto (`RESUMO_PROJETO.md`)
- Exemplos de arquivos válidos
- Configuração padrão (`config.txt`)

## Arquitetura do Sistema

```
Editor de Arquivo de Movimentação Financeira
├── Aplicação Principal
│   ├── financeiro_app.py (editor principal)
│   ├── iniciar_app.py (menu de inicialização)
│   └── config.txt (configurações)
├── Scripts de Apoio
│   ├── run.sh (execução)
│   ├── install.sh (instalação)
│   └── backup_arquivos.py (backup)
├── Testes
│   ├── teste_automatizado.py (testes)
│   ├── teste_valores.py (teste de valores)
│   └── teste_valores2.py (teste de valores)
├── Visualização
│   └── visualizar_logs.py (logs)
├── Documentação
│   ├── README.md (documentação principal)
│   ├── RESUMO_PROJETO.md (este documento)
│   └── estrutura_arquivo_movimentacao.md (especificação)
├── Exemplos
│   ├── exemplo_movimentacao.txt (exemplo básico)
│   ├── exemplo_correto.txt (exemplo corrigido)
│   └── exemplo_valido.txt (exemplo válido)
└── Dados
    ├── log.txt (arquivo de log)
    └── backups/ (diretório de backups)
```

## Como Usar

### Método 1: Script de inicialização (recomendado)
```bash
python3 iniciar_app.py
```

### Método 2: Comando direto
```bash
editor-financeiro
```

### Método 3: Execução do módulo principal
```bash
python3 financeiro_app.py
```

## Requisitos
- Python 3.x
- Sistema operacional Linux/Unix (com suporte a links simbólicos)

## Funcionalidades de Segurança
- Validação rigorosa de estrutura de arquivos
- Sistema de backup automático
- Logging detalhado para auditoria
- Tratamento de erros robusto

## Extensibilidade
O sistema foi projetado para ser facilmente extensível, com:
- Arquitetura modular
- Sistema de logging padronizado
- Configurações externalizadas
- Testes automatizados

## Próximos Passos Sugeridos
1. Implementar testes unitários mais abrangentes
2. Adicionar funcionalidade de exportação para outros formatos
3. Implementar interface gráfica
4. Adicionar criptografia para backups sensíveis
5. Implementar sistema de notificações
