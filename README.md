# Sistema de Gestão de Inscritos e Alunos (EDA & Profiling)

Este projeto visa a análise exploratória de dados (EDA) e a modelagem do perfil de inscritos para um Sistema de Gestão de Alunos, utilizando o Firebase (Plano Spark) como base de dados e armazenamento.

## 🎯 Objetivos
- **EDA**: Identificar bairros com maior evasão ou concentração de inscrições.
- **Qualidade de Dados**: Validar preenchimento campos nulos em documentos e memorandos.
- **Correlação Socioeconômica**: Relacionar o IDH municipal com as taxas de inscrição.
- **Perfilamento**: Definir o perfil demográfico e geográfico do público-alvo.

## 🛠️ Tecnologias e Ambiente
- **Firebase Firestore**: Armazenamento de dados transacionais.
- **Firebase Storage**: Repositório para modelos treinados (Limite de 5GB).
- **Python**: Linguagem principal para análise e modelagem.
- **Pandas/Scikit-learn/Seaborn**: Ecossistema de Ciência de Dados.

## 📂 Estrutura do Projeto
- `data/raw/`: Relatórios CSV/Excel e dados do Open Data.
- `data/processed/`: Dados limpos e preparados para modelagem.
- `notebooks/`: Análises experimentais e protótipos em Jupyter.
- `src/`: Scripts modulares para automação de ETL e treinamento de modelos.
- `config/`: Configurações de acesso (credenciais do Firebase).

## 🚀 Setup Inicial
1.  Obtenha o arquivo `service-account.json` no console do Firebase (Configurações do Projeto > Contas de Serviço).
2.  Coloque o arquivo na pasta `config/` (ignorado pelo Git por segurança).
3.  Crie um ambiente virtual: `python -m venv venv`
4.  Instale as dependências: `pip install -r requirements.txt`

## 📊 Premissas de Ingestão
Para facilitar o "Join" (cruzamento) de dados, os campos no Firestore devem coincidir exatamente com os nomes das colunas dos relatórios externos.

---
**Status atual**: Ambiente de desenvolvimento preparado.
