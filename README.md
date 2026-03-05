# Sistema de Gestão de Inscritos e Alunos (EDA & Profiling)

Este projeto visa a análise exploratória de dados (EDA) e a modelagem do perfil de inscritos para um Sistema de Gestão de Alunos, utilizando o Firebase (Plano Spark) como base de dados e armazenamento.

## 🎯 Objetivos
- **EDA**: Identificar bairros com maior evasão ou concentração de inscrições.
- **Qualidade de Dados**: Validar preenchimento campos nulos em documentos e memorandos.
- **Correlação Socioeconômica**: Relacionar o IDH municipal com as taxas de inscrição.
- **Perfilamento**: Definir o perfil demográfico e geográfico do público-alvo.

## 🚀 Pipeline & Deploy
1. **Google Colab**: Use para treinamento de modelos pesados e EDA inicial.
2. **Streamlit**: Dashboard interativo rodando em `app.py`.
3. **Streamlit Cloud**: Hospedagem gratuita conectada ao GitHub.
    - O arquivo `service-account.json` deve ser configurado no **Streamlit Secrets** (não comitar o JSON).

## 📊 Dashboard Interativo
Execute localmente com:
```bash
streamlit run app.py
```

## 📊 Premissas de Ingestão
Para facilitar o "Join" (cruzamento) de dados, os campos no Firestore devem coincidir exatamente com os nomes das colunas dos relatórios externos (Ver `data/raw/TEMPLATE_COLUNAS.csv`).

---
**Status atual**: Ambiente Web/Dashboard preparado.
