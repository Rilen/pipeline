
from google import genai
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
        self.gemini_client = None
        
        if self.gemini_key:
            try:
                # Inicializa o novo cliente do Google GenAI
                self.gemini_client = genai.Client(api_key=self.gemini_key)
                
                # Lista modelos disponíveis usando a nova SDK
                models = self.gemini_client.models.list()
                for m in models:
                    # A nova SDK usa supported_actions ou verifica se o modelo suporta geração
                    supported = getattr(m, 'supported_generation_methods', None) or getattr(m, 'supported_actions', [])
                    if 'generateContent' in supported or 'generate_content' in str(supported).lower():
                        model_id = m.name.replace('models/', '')
                        self.available_gemini_models.append(model_id)
                
                if not self.available_gemini_models:
                    # Fallback: usa modelos conhecidos se a listagem não retornar nada útil
                    self.available_gemini_models = [
                        'gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-flash-8b'
                    ]
                    print(f"⚠️ Usando modelos Gemini padrão (listagem indisponível)")
                else:
                    print(f"📦 Modelos Gemini detectados: {self.available_gemini_models}")
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Erro ao listar modelos Gemini: {error_msg}")
                # Se o erro for de API key, não tenta usar modelos padrão
                if '403' not in error_msg and 'leaked' not in error_msg.lower():
                    self.available_gemini_models = ['gemini-2.0-flash', 'gemini-1.5-flash']
        
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
        try:
            img = PIL.Image.open(uploaded_image)
        except Exception as e:
            return f"⚠️ Erro ao abrir imagem: {str(e)}", None

        prompt = """
        Analise esta imagem, extraia todo o texto legível e dê 3 insights.
        Responda em Markdown estruturado.
        """

        # Tentativa 1: Gemini
        if self.gemini_client and self.available_gemini_models:
            candidates = [
                'gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-flash-8b',
                'gemini-1.5-pro', 'gemini-flash-latest'
            ]
            to_try = [m for m in candidates if m in self.available_gemini_models]
            
            if not to_try:
                to_try = [self.available_gemini_models[0]]

            last_error = ""
            for model_name in to_try:
                try:
                    response = self.gemini_client.models.generate_content(
                        model=model_name,
                        contents=[prompt, img]
                    )
                    return f"## 🤖 Insights IA (Gemini - {model_name})\n{response.text}", img
                except Exception as e:
                    last_error = str(e)
                    if "429" in last_error or "quota" in last_error.lower():
                        print(f"⚠️ Modelo {model_name} sem cota (429). Tentando próximo...")
                        continue
                    break
        
        # Tentativa 2: Groq Vision
        if self.groq_client:
            print("🔄 Tentando fallback para Groq Vision...")
            try:
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG')
                img_bytes = img_byte_arr.getvalue()
                
                import base64
                base64_image = base64.b64encode(img_bytes).decode('utf-8')

                groq_candidates = [
                    "meta-llama/llama-4-scout-17b-16e-instruct",
                    "llama-3.2-11b-vision-instruct",
                    "llama-3.2-90b-vision-instruct"
                ]
                
                for g_model in groq_candidates:
                    try:
                        print(f"🔄 Tentando Groq: {g_model}...")
                        completion = self.groq_client.chat.completions.create(
                            model=g_model,
                            messages=[
                                {
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": prompt},
                                        {
                                            "type": "image_url",
                                            "image_url": {
                                                "url": f"data:image/jpeg;base64,{base64_image}",
                                            },
                                        },
                                    ],
                                }
                            ],
                        )
                        return f"## 🤖 Insights IA (Groq Fallback - {g_model})\n{completion.choices[0].message.content}", img
                    except Exception as e:
                        groq_err = str(e)
                        print(f"⚠️ Erro no modelo Groq {g_model}: {groq_err}")
                        if "404" in groq_err or "not found" in groq_err.lower() or "decommissioned" in groq_err.lower():
                            continue
                        break
            except Exception as groq_err:
                print(f"❌ Groq Critical Error: {str(groq_err)}")

        return "## 📊 Análise Local\nInsights de IA indisponíveis (APIs sem cota ou não configuradas). O arquivo foi carregado com sucesso.", img

    def analyze_document_text(self, text, context="documento"):
        """
        Analisa texto com fallback Gemini (Modelos Dinâmicos) -> Groq.
        """
        prompt = f"Analise este {context} e extraia 3 insights estratégicos curtos:\n\n{text[:8000]}"
        
        if not self.gemini_client or not self.available_gemini_models:
            return self._analyze_with_groq(prompt)

        # 1. Tentativa com Gemini
        candidates = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-flash-8b', 'gemini-flash-latest']
        to_try = [m for m in candidates if m in self.available_gemini_models]
        
        if not to_try and self.available_gemini_models:
            to_try = [self.available_gemini_models[0]]

        for model_name in to_try:
            try:
                response = self.gemini_client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return f"## 🤖 Insights IA (Gemini - {model_name})\n{response.text}"
            except Exception as e:
                if "429" in str(e): continue
                break

        # 2. Tentativa com Groq (Llama 3)
        return self._analyze_with_groq(prompt)

    def _analyze_with_groq(self, prompt):
        """Helper para análise via Groq"""
        if self.groq_client:
            try:
                completion = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                return f"## 🤖 Insights IA (Groq)\n{completion.choices[0].message.content}"
            except:
                pass
        return "## 📊 Análise Local\nInsights de IA indisponíveis (Cota Gemini/Groq excedida ou APIs não configuradas)."

    @staticmethod
    def extract_text_from_docx(file):
        try:
            doc = Document(file)
            return '\n'.join([p.text for p in doc.paragraphs])
        except Exception as e:
            return f"Erro DOCX: {e}"


def get_intel_engine():
    """Factory function para inicialização lazy — evita quebrar o import do módulo."""
    if not hasattr(get_intel_engine, '_instance'):
        try:
            get_intel_engine._instance = IntelEngine()
        except Exception as e:
            print(f"❌ Erro ao criar IntelEngine: {e}")
            get_intel_engine._instance = IntelEngine.__new__(IntelEngine)
            get_intel_engine._instance.gemini_key = None
            get_intel_engine._instance.groq_key = None
            get_intel_engine._instance.available_gemini_models = []
            get_intel_engine._instance.gemini_client = None
            get_intel_engine._instance.groq_client = None
    return get_intel_engine._instance
