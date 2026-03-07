#!/bin/bash
# Script utilitário para Fazer Deploy no GitHub (Streamlit Cloud atualizará automaticamente)

echo "🔄 Iniciando processo de deploy..."
git add .
read -p "📝 Mensagem do commit (padrão: 'Update from Fedora'): " commit_msg
commit_msg=${commit_msg:-"Update from Fedora"}
git commit -m "$commit_msg"

echo "📤 Enviando para o GitHub..."
git push origin main

echo "✅ Deploy concluído! Verifique em: https://pipeline-7uwq9yvmqmctpbjvtkzjtw.streamlit.app/"
