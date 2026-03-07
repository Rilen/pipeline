#!/bin/bash
# Script para rodar o Dashboard Streamlit localmente no Fedora 43

# Ativa o ambiente estável (Python 3.12) para evitar erros do 3.14
if [ -d "venv_stable" ]; then
    source venv_stable/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "⚠️ Ambiente virtual não encontrado! Por favor, aguarde o setup..."
    exit 1
fi

# Avisa sobre credenciais ausentes
if [ ! -f "config/service-account.json" ]; then
    echo "⚠️ AVISO: 'config/service-account.json' não encontrado. Recursos do Firestore podem falhar."
fi

# Executa o Streamlit
echo "🚀 Iniciando Dashboard..."
streamlit run app.py
