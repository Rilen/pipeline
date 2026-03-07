# 🤖 Analista IA PRO (Hybrid Engine 2026)

> **Arquitetura**: Engenharia de Software Sênior & Design de Alta Performance

Este ecossistema foi refatorado para oferecer uma infraestrutura de dados robusta, utilizando inteligência híbrida para análise exploratória (EDA), modelagem e **OCR avançado (Visão Computacional)**.

---

## 🎯 Novos Recursos (V2.0 Core)
- **📸 Vision OCR**: Suporte a leitura de documentos via imagem (PNG/JPG) com extração automática de texto e JSON estruturado (via Gemini 2.0 Flash).
- **🎨 Premium UI**: Design baseado em Glassmorphism, tipografia moderna (Outfit/Inter) e UX de alta fluidez.
- **🏗️ Clean Architecture**: Código modularizado em `Intelligence`, `Analytics` e `Data Engine` (SOLID).
- **💾 Pipeline Integrado**: Upload direto para Firestore com batching de alta performance.

---

## 📂 Nova Estrutura Refatorada
```text
pipeline/
├── 📊 app.py               # Front-end Streamlit de Alta Performance
├── 🐍 src/
│   ├── intelligence.py    # Motor Multi-IA (OCR, Vision, NLP)
│   ├── analytics.py       # Lógica Pura de Engenharia de Dados & Estatística
│   └── data_engine.py      # Interface Central Firebase Firestore & Storage
├── 📓 notebooks/           # P&D e Rascunhos
├── 📁 data/                # Raw e Processed
└── ⚙️ config/              # Credenciais (Ignorado pelo Git)
```

---

## 🛠️ Início Rápido (Fedora Linux / Ubuntu)

1. **Ativar Ambiente**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Executar Dashboard**:
   ```bash
   streamlit run app.py
   ```

---

## ☁️ Deploy & Cloud
O projeto está configurado para deploy contínuo via Streamlit Cloud.
**Dashboard Oficial:** [link-do-seu-deploy-atualizado]

---
*Powered by Antigravity IA | Hybrid Analytics Engine 2026*
