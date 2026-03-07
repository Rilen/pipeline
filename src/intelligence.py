import google.generativeai as genai
import streamlit as st
import PIL.Image
import pandas as pd
import io
import json
from docx import Document
from groq import Groq

class IntelEngine:
    """
    Motor de Inteligência Híbrida (Gemini/Groq/Local).
    Responsável por OCR, NLP e Geração de Insights.
    """
    
    def __init__(self):
        import os
        print("🔍 Verificando chaves de API...")
        
        self.gemini_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        self.groq_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
        
        self.available_gemini_models = []
        if self.gemini_key:
            try:
                genai.configure(api_key=self.gemini_key)
                models = genai.list_models()
                self.available_gemini_models = [m.name.replace('models/', '') for m in models if 'generateContent' in m.supported_generation_methods]
                print(f"📦 Modelos Gemini detectados: {self.available_gemini_models}")
            except Exception as e:
                print(f"❌ Erro ao listar modelos Gemini: {e}")
        
        self.groq_client = None
        if self.groq_key:
            try:
                self.groq_client = Groq(api_key=self.groq_key)
            except Exception as e:
                print(f"❌ Erro Groq: {e}")

    def analyze_image_ocr(self, uploaded_image):
        """
        Extrai texto de imagens com fallback automático de modelos em caso de erro de cota (429).
        """
        if not self.gemini_key:
            return "❌ API Key do Gemini não configurada.", None

        try:
            img = PIL.Image.open(uploaded_image)
            prompt = """
            Analise esta imagem, extraia todo o texto legível e dê 3 insights.
            Responda em Markdown estruturado.
            """
            
            # Ordem de tentativa
            candidates = ['gemini-1.5-flash', 'gemini-flash-lite-latest', 'gemini-1.5-pro', 'gemini-flash-latest', 'gemini-2.0-flash']
            to_try = [m for m in candidates if m in self.available_gemini_models]
            
            if not to_try and self.available_gemini_models:
                to_try = [self.available_gemini_models[0]]

            last_error = ""
            for model_name in to_try:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content([prompt, img])
                    return response.text, img
                except Exception as e:
                    last_error = str(e)
                    if "429" in last_error:
                        print(f"⚠️ Modelo {model_name} sem cota (429). Tentando próximo...")
                        continue
                    break
            
            return f"❌ Todos os modelos Gemini falharam ou estão sem cota. Erro final: {last_error}", None
            
        except Exception as e:
            return f"⚠️ Erro fatal no OCR: {str(e)}", None

    def analyze_document_text(self, text, context="documento"):
        """
        Analisa texto com fallback Gemini (Modelos Dinâmicos) -> Groq.
        """
        prompt = f"Analise este {context} e extraia 3 insights estratégicos curtos:\n\n{text[:8000]}"
        
        # 1. Tentativa com Gemini
        candidates = ['gemini-1.5-flash', 'gemini-flash-latest', 'gemini-2.0-flash']
        to_try = [m for m in candidates if m in self.available_gemini_models]
        
        for model_name in to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return f"## 🤖 Insights IA (Gemini - {model_name})\n{response.text}"
            except Exception as e:
                if "429" in str(e): continue
                break

        # 2. Tentativa com Groq (Llama 3)
        if self.groq_client:
            try:
                completion = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                return f"## 🤖 Insights IA (Groq)\n{completion.choices[0].message.content}"
            except:
                pass
        
        return "## 📊 Análise Local\nInsights de IA indisponíveis (Cota Gemini/Groq excedida)."

    @staticmethod
    def extract_text_from_docx(file):
        try:
            doc = Document(file)
            return '\n'.join([p.text for p in doc.paragraphs])
        except Exception as e:
            return f"Erro DOCX: {e}"

intel_engine = IntelEngine()
