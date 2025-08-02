#!/bin/bash

# Script de instalação para o Editor de Arquivo de Movimentação Financeira

echo "Instalando dependências..."

# Verificar se o Python 3 está instalado
if ! command -v python3 &> /dev/null
then
    echo "Python 3 não encontrado. Por favor, instale o Python 3."
    exit 1
fi

# Verificar se o pip está instalado
if ! command -v pip3 &> /dev/null
then
    echo "pip3 não encontrado. Por favor, instale o pip3."
    exit 1
fi

# Tornar os scripts executáveis
chmod +x /home/peder/Projetos/EditCobol/financeiro_app.py
chmod +x /home/peder/Projetos/EditCobol/run.sh
chmod +x /home/peder/Projetos/EditCobol/install.sh

# Criar link simbólico para facilitar a execução
echo "Criando link simbólico para facilitar a execução..."
sudo ln -sf /home/peder/Projetos/EditCobol/financeiro_app.py /usr/local/bin/editor-financeiro

# Verificar se a instalação foi bem-sucedida
echo "Verificando instalação..."
if command -v editor-financeiro &> /dev/null
then
    echo "Instalação concluída com sucesso!"
    echo "Agora você pode executar o editor com o comando: editor-financeiro"
else
    echo "Instalação concluída, mas não foi possível criar o link simbólico."
    echo "Você pode executar o editor com: python3 /home/peder/Projetos/EditCobol/financeiro_app.py"
fi
