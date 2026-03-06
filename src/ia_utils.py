import pandas as pd
import numpy as np
from docx import Document
import google.generativeai as genai
from groq import Groq
import streamlit as st
import io

def extract_text_from_docx(file):
    """Extrai texto de um arquivo .docx"""
    try:
        doc = Document(file)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        return f"Erro ao ler DOCX: {e}"

def generate_local_statistical_report(df):
    """Gera um relatório técnico baseado puramente em estatística."""
    report = "## 📊 Relatório Estatístico Automatizado\n\n"
    report += f"**Resumo:** {len(df)} linhas, {len(df.columns)} colunas.\n\n"
    
    null_counts = df.isnull().sum()
    if null_counts.sum() > 0:
        report += "**⚠️ Qualidade:** Valores ausentes detectados.\n"
    else:
        report += "✅ **Qualidade:** Dados completos.\n\n"
    
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        report += "**📈 Insights Numéricos:**\n"
        for col in numeric_cols[:3]:
            report += f"- `{col}`: Média {df[col].mean():,.2f}\n"
            
    return report

def analyze_with_groq(content, context_type="data"):
    """Tenta usar o Groq (Llama 3) como IA alternativa."""
    groq_key = st.secrets.get("GROQ_API_KEY")
    if not groq_key:
        return None
    
    try:
        client = Groq(api_key=groq_key)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Você é um analista de dados. Responda em Markdown de forma curta e direta."},
                {"role": "user", "content": f"Analise este resumo de {context_type} e dê 3 insights rápidos:\n\n{content}"}
            ],
            max_tokens=500
        )
        return f"## 🤖 Insights da IA (via Groq/Llama)\n{completion.choices[0].message.content}"
    except Exception as e:
        return f"❌ Erro no Groq: {str(e)}"

def analyze_with_gemini(content, context_type="data"):
    """Tenta usar o Gemini como IA primária."""
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return None
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-2.0-flash')
        prompt = f"Analise brevemente este resumo de {context_type} e dê 3 insights estratégicos curtos:\n\n{content}"
        response = model.generate_content(prompt)
        return f"## 🤖 Insights da IA (via Gemini)\n{response.text}"
    except Exception as e:
        return f"⚠️ Erro Gemini: {str(e)}"

def process_file_for_dashboard(uploaded_file):
    """Lógica Multi-IA: Tenta Gemini -> Tenta Groq -> Backup Local."""
    
    try:
        if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.csv') or uploaded_file.name.endswith('.json'):
            if uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.json'):
                df = pd.read_json(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
            summary = f"Colunas: {list(df.columns)}. Estatísticas: {df.describe().to_string()}"
            context = "planilha"
        elif uploaded_file.name.endswith('.docx'):
            text = extract_text_from_docx(uploaded_file)
            if not text.strip() or "Erro ao ler" in text:
                return f"❌ Não foi possível extrair texto do documento: {text}", None
            summary = text
            context = "documento"
            df = None
        else:
            return "❌ Formato não suportado.", None
    except Exception as e:
        return f"❌ Erro crítico no processamento do arquivo: {str(e)}", None

    # Tenta Gemini primeiro
    ia_report = analyze_with_gemini(summary[:3000], context)
    
    # Se Gemini falhou, tenta Groq
    if not ia_report or "Quota" in ia_report or "indisponível" in ia_report or "Erro" in ia_report:
        groq_report = analyze_with_groq(summary[:3000], context)
        if groq_report:
            ia_report = groq_report

    # --- Tratamento de Fallback ---
    # Se as IAs falharam, mostramos o conteúdo bruto ou um aviso claro
    if not ia_report or "Erro" in ia_report or "indisponível" in ia_report:
        if context == "documento":
            ia_report = f"## 📄 Conteúdo do Documento (Sem IA no momento)\n\nAs IAs não puderam processar o arquivo. Abaixo está o início do texto extraído:\n\n{summary[:1000]}..."
        else:
            ia_report = "## ⚠️ Insights de IA indisponíveis\n\nVerifique suas chaves de API nos segredos do Streamlit. Mas não se preocupe, o relatório estatístico abaixo está ativo!"

    # Sempre gera o estatístico como base para planilhas
    local_report = ""
    if df is not None:
        local_report = generate_local_statistical_report(df)
    
    full_report = f"{ia_report}\n\n---\n\n{local_report}"
    return full_report, df
