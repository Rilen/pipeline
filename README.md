# 📊 Sistema de Gestão de Inscritos & Alunos (Pipeline EDA)

> **Status do Projeto**: 🚀 Ambiente Web/Dashboard Preparado & Integrado ao Firebase (Plano Spark)

Este repositório contém a infraestrutura de dados para Análise Exploratória (EDA), Modelagem de Perfil e Monitoramento em tempo real de novos inscritos, utilizando **Python**, **Firebase (Firestore/Storage)** e **Streamlit**.

---

## 🎯 Objetivos do Projeto
- **📍 Geolocalização**: Identificar bairros com maior volume de inscrições e pontos críticos de evasão.
- **📉 Diagnóstico de Evasão**: Analisar o abandono baseado no perfil socioeconômico (Renda, Acesso à Internet).
- **📝 Qualidade de Dados**: Validar o preenchimento de documentos e memorandos obrigatórios.
- **💰 Correlação Socioeconômica**: Cruzar dados de inscritos com o **IDH Municipal** para identificar barreiras de acesso.

---

## 📂 Estrutura do Ecossistema
```text
pipeline/
├── 📊 app.py              # Dashboard Streamlit Principal
├── 🐍 src/
│   ├── firebase_client.py # Motor de conexão (Suporta Local e Cloud Secrets)
│   ├── ingest_data.py     # Pipeline de ingestão (CSV/Excel/JSON -> Firestore)
│   └── analysis_utils.py  # Funções matemáticas e estatísticas (EDA)
├── 📓 notebooks/          # Experimentos e rascunhos em Jupyter/Colab
├── 📁 data/
│   ├── raw/               # Relatórios brutos e dados do Open Data
│   └── processed/         # Dados limpos prontos para modelagem
└── ⚙️ config/             # Configurações e Chaves (Ignorado pelo Git)
```

---

## 🛠️ Tecnologias Utilizadas
- **Backend / DB**: Firebase Admin SDK (Firestore & Storage).
- **Dashboard**: Streamlit + Plotly Express + Option Menu.
- **Data Science**: Pandas, Scikit-learn, Seaborn, Numpy.
- **DevOps**: Git, Streamlit Cloud, GitHub Secrets.

---

## 🚀 Guia de Início Rápido

### 1. Preparação do Ambiente
```bash
# Criar e ativar ambiente virtual
python -m venv venv
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configuração das Credenciais (Segurança)
1. Acesse o **Firebase Console** e gere um arquivo `service-account.json`.
2. Salve-o na pasta `config/service-account.json`.
3. Certifique-se de que a **Firestore API** está ativa no [Google Cloud Console](https://console.cloud.google.com/apis/library/firestore.googleapis.com).

### 3. Ingestão de Dados
Coloque seus relatórios (CSV, Excel ou JSON) em `data/raw/` e execute:
```bash
python src/ingest_data.py
```
*O pipeline irá automaticamente realizar o upload em lotes (batch) para o Firestore.*

### 4. Visualização (Dashboard)
```bash
streamlit run app.py
```

---

## 📊 Premissas de Dados (Data Dictionary)
Para garantir o funcionamento dos filtros e cruzamentos, os relatórios externos devem conter:
- `id_inscricao`: Identificador único (Chave Primária).
- `bairro_municipal`: Nome do bairro (Crucial para o mapa).
- `status`: [pendente, concluído, evadido].
- `socioeconomico`: Objeto contendo `renda_familiar` e `possui_internet`.

*(Veja o arquivo `data/raw/TEMPLATE_COLUNAS.csv` para referência completa)*

---

## ☁️ Deploy (Streamlit Cloud)
Para hospedar o dashboard online:
1. Suba o código para o GitHub.
2. No Streamlit Cloud, adicione o conteúdo do seu `service-account.json` em **Secrets** com a chave `firebase_secrets`.

---
**Desenvolvido com Antigravity AI** 🌐
