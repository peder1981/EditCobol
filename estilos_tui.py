#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Definições de estilos e cores para interfaces TUI da aplicação
"""

from prompt_toolkit.styles import Style

# Cores padrão para toda a aplicação
CORES = {
    # Cores de texto
    'texto_normal': '#ffffff',  # Branco puro para melhor contraste
    'texto_titulo': 'bold #ffffff',  # Branco puro em negrito para títulos
    'texto_destaque': '#3498db',  # Azul mais vivo para destaque
    'texto_sucesso': '#2ecc71',  # Verde mais vivo
    'texto_erro': '#e74c3c',  # Vermelho mais vivo
    'texto_aviso': '#f1c40f',  # Amarelo mais vivo
    'texto_desabilitado': 'ansigray',
    
    # Cores de fundo
    'fundo_normal': '',  # Fundo padrão do terminal
    'fundo_selecionado': 'reverse',  # Inverte cores para destacar seleção
    'fundo_destaque': 'bg:#3498db fg:#ffffff',  # Melhorado contraste
    
    # Cores para separadores e bordas
    'separador': '#3498db',  # Azul mais vivo para separadores
}

# Estilos para elementos específicos
ESTILOS = {
    'titulo': f"bold",
    'subtitulo': f"fg:{CORES['texto_destaque']}",
    'texto_normal': f"fg:{CORES['texto_normal']}",
    'texto_destaque': f"fg:{CORES['texto_destaque']}",
    'texto_sucesso': f"fg:{CORES['texto_sucesso']}",
    'texto_erro': f"fg:{CORES['texto_erro']}",
    'texto_aviso': f"fg:{CORES['texto_aviso']}",
    'texto_desabilitado': f"fg:{CORES['texto_desabilitado']}",
    'item_selecionado': f"{CORES['fundo_selecionado']}",
    'separador': f"fg:{CORES['separador']}",
    'cabecalho_tabela': f"bold",
    'rodape': f"fg:{CORES['texto_normal']}",
    'ajuda': f"fg:{CORES['texto_normal']}",
}

# Função para obter estilo formatado
def obter_estilo(nome_estilo):
    """Retorna o estilo formatado para uso com prompt_toolkit"""
    return ESTILOS.get(nome_estilo, ESTILOS['texto_normal'])

# Objeto Style para uso com prompt_toolkit
ESTILO_PROMPT_TOOLKIT = Style.from_dict({
    'titulo': f"bold",
    'subtitulo': f"fg:{CORES['texto_destaque']}",
    'texto-normal': f"fg:{CORES['texto_normal']}",
    'texto-destaque': f"fg:{CORES['texto_destaque']}",
    'texto-sucesso': f"fg:{CORES['texto_sucesso']}",
    'texto-erro': f"fg:{CORES['texto_erro']}",
    'texto-aviso': f"fg:{CORES['texto_aviso']}",
    'texto-desabilitado': f"fg:{CORES['texto_desabilitado']}",
    'item-selecionado': f"{CORES['fundo_selecionado']}",
    'separador': f"fg:{CORES['separador']}",
    'cabecalho-tabela': f"bold",
    'rodape': f"fg:{CORES['texto_normal']}",
    'ajuda': f"fg:{CORES['texto_normal']}",
})
