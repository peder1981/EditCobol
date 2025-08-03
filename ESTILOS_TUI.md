# Guia de Estilos e Cores - Interface TUI

Este documento descreve o padrão de estilos e cores utilizados na interface TUI (Text User Interface) da aplicação Editor de Arquivo de Movimentação Financeira.

## Visão Geral

A interface TUI da aplicação foi desenvolvida utilizando o framework `prompt_toolkit`, que permite a criação de interfaces de texto interativas e estilizadas. Todos os componentes visuais seguem um padrão consistente de cores e estilos, definidos centralmente no módulo `estilos_tui.py`.

## Padrão de Cores

### Cores Principais

| Elemento | Cor | Descrição |
|----------|-----|-----------|
| **Fundo** | Azul escuro | Cor de fundo padrão para todas as telas |
| **Texto Normal** | Branco | Texto padrão em todas as telas |
| **Destaque** | Amarelo | Utilizado para destacar elementos selecionados ou importantes |
| **Título** | Verde claro | Utilizado para títulos de telas e seções |
| **Alerta** | Vermelho | Utilizado para mensagens de erro ou alertas |
| **Desabilitado** | Cinza | Utilizado para opções ou elementos desabilitados |

### Cores Específicas

| Elemento | Cor | Descrição |
|----------|-----|-----------|
| **Selecionado** | Fundo amarelo, texto preto | Indica o item atualmente selecionado |
| **Cabeçalho** | Fundo azul claro, texto branco | Utilizado para cabeçalhos de tabelas |
| **Botão** | Fundo cinza, texto preto | Utilizado para botões em diálogos |
| **Botão Selecionado** | Fundo branco, texto preto | Indica o botão atualmente selecionado |

## Implementação

O padrão de estilos é implementado no módulo `estilos_tui.py`, que define uma constante `ESTILO_PROMPT_TOOLKIT` utilizada por todos os componentes da interface. Esta abordagem centralizada garante consistência visual em toda a aplicação.

```python
# Exemplo de definição de estilos em estilos_tui.py
ESTILO_PROMPT_TOOLKIT = Style.from_dict({
    # Estilos gerais
    '': 'bg:#000080 #ffffff',  # Fundo azul escuro, texto branco
    'titulo': 'bold #00ff00',  # Título em verde claro e negrito
    
    # Estilos específicos para menus
    'menu.borda': '#ffffff',
    'menu.item': '#ffffff',
    'menu.item.selecionado': 'bg:#ffff00 #000000',
    
    # Estilos para diálogos
    'dialog': 'bg:#000080',
    'dialog.body': 'bg:#000080 #ffffff',
    'dialog.button': 'bg:#cccccc #000000',
    'dialog.button.focused': 'bg:#ffffff #000000',
})
```

## Componentes Estilizados

### 1. Menu Principal

O menu principal utiliza o estilo padrão com destaque para a opção selecionada:
- Título em verde claro e negrito
- Opções em texto branco
- Opção selecionada com fundo amarelo e texto preto
- Instruções de navegação em texto branco

### 2. Seletor de Arquivos

O seletor de arquivos segue o mesmo padrão visual:
- Título em verde claro
- Lista de arquivos em texto branco
- Arquivo selecionado com fundo amarelo e texto preto
- Informações de paginação em texto branco

### 3. Planilha de Registros

A planilha de registros utiliza cores para diferenciar tipos de informação:
- Cabeçalho com fundo azul claro e texto branco
- Registros normais em texto branco
- Registro sob o cursor com fundo amarelo e texto preto
- Registros selecionados com marcador específico
- Informações de status em texto verde claro

### 4. Diálogos

Os diálogos de confirmação e mensagem seguem o padrão visual consistente:
- Título em verde claro
- Texto da mensagem em branco
- Botões com fundo cinza e texto preto
- Botão selecionado com fundo branco e texto preto
- Borda em branco

## Personalização

Para manter a consistência visual, qualquer nova tela ou componente deve utilizar o estilo centralizado definido em `estilos_tui.py`. Se for necessário adicionar novos estilos, eles devem ser incluídos neste arquivo central.

## Acessibilidade

O esquema de cores foi escolhido para garantir bom contraste e legibilidade em diferentes terminais. As cores principais (azul escuro, branco, amarelo) foram selecionadas para maximizar a visibilidade e reduzir a fadiga visual durante o uso prolongado.

## Referências

- [Documentação do prompt_toolkit](https://python-prompt-toolkit.readthedocs.io/)
- [Guia de Estilos do prompt_toolkit](https://python-prompt-toolkit.readthedocs.io/en/master/pages/styling.html)
