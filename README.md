# 🚀 Analista IA PRO

<div align="center">
    <img src="docs/banner.png" alt="Banner ou Screenshot do Projeto" width="100%" max-width="800px">
</div>

<br>


## 📝 Descrição do Projeto

Este projeto tem como objetivo fornecer uma plataforma profissional robusta para análise exploratória de dados (EDA), inteligência artificial híbrida e processamento de documentos. A ferramenta atua como um assistente avançado que processa planilhas, textos e imagens (via OCR), gerando relatórios estratégicos e perfis estatísticos com integração direta de dados no Firebase.

Desenvolvido com foco em alta performance, modularização limpa (Clean Architecture), escalabilidade de dados e uma interface premium (UI) com design moderno utilizando *Glassmorphism*.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

Nesta seção, listamos as principais tecnologias que sustentam o projeto.

| Camada | Tecnologias |
|:---|:---|
| **Linguagem/Runtime** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| **Frameworks/Libs** | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white) ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white) |
| **Inteligência Artificial** | ![Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white) ![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white) |
| **Banco de Dados & Cloud** | ![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black) ![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white) |
| **Ferramentas** | ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white) ![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white) ![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)|

---

## ⚙️ Como Rodar o Projeto Localmente

Siga estes passos para configurar o ambiente e executar o projeto na sua máquina.

### 📋 Pré-requisitos

Antes de começar, você vai precisar ter instalado:
* Python 3.9+
* Um cliente Git
* Uma conta/projeto no Firebase com Firestore habilitado

### 🔧 Instalação e Execução

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/rilen/pipeline.git
    cd pipeline
    ```

2.  **Configure as variáveis de ambiente e credenciais:**
    * Configure o acesso ao Firebase adicionando a chave de serviço na pasta `config/` ou variáveis de ambiente.
    * Adicione a sua chave de API do Google Gemini e Groq no arquivo `.env`. **Nunca externe o `.env` real ou as credenciais para o Git!**

3.  **Instale as dependências:**
    ```bash
    python -m venv venv
    
    # No Linux/macOS:
    source venv/bin/activate  
    # No Windows: 
    venv\Scripts\activate
    
    pip install -r requirements.txt
    ```

4.  **Execute o projeto:**
    ```bash
    streamlit run app.py
    ```

5.  **Acesse a aplicação:**
    A aplicação estará rodando em `http://localhost:8501`.

---

## 📁 Estrutura do Projeto (Visão Geral)

Para facilitar a navegação, aqui está uma breve descrição da organização das pastas.

```text
pipeline/
├── src/                  # Código-fonte principal da aplicação
│   ├── analytics.py      # Lógica de Engenharia de Dados & Estatística
│   ├── data_engine.py    # Interface Central (Firebase Firestore & Storage)
│   └── intelligence.py   # Motor Multi-IA (OCR, Vision, NLP)
├── config/               # Credenciais de serviços (ex: Firebase)
├── data/                 # Dados analíticos (Raw e Processed)
├── notebooks/            # Notebooks Jupyter para P&D e experimentações
├── requirements.txt      # Dependências do projeto Python
├── app.py                # Front-end Streamlit de Alta Performance
└── README.md             # Este arquivo
```

---

# Rilen T. L. - DataScience

**25+ anos em TI - Especialista em Big Data | IA | CyberSecurity**

***Full Stack Development & Data Intelligence***

Rio das Ostras · RJ · Brasil · PcD (Implante Coclear)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rilen/)
[![Gmail](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:rilen.lima@gmail.com)
[![Portfólio](https://img.shields.io/badge/Portfólio-000000?style=for-the-badge&logo=githubpages&logoColor=white)](https://rilen.github.io/portfolio/)

---
