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
        # Debug logs para o terminal (não pro Streamlit UI por segurança)
        print("🔍 Verificando chaves de API...")
        
        # O Streamlit às vezes demora a recarregar segredos de arquivos novos
        self.gemini_key = st.secrets.get("GEMINI_API_KEY") 
        if not self.gemini_key:
            self.gemini_key = os.environ.get("GEMINI_API_KEY")
            
        self.groq_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
        
        self.gemini_model = None
        if self.gemini_key:
            try:
                print(f"✅ Chave Gemini detectada (Início: {self.gemini_key[:8]}...)")
                genai.configure(api_key=self.gemini_key)
                
                # Lista de modelos por prioridade
                potential_models = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.5-flash-8b']
                
                working_model = None
                try:
                    # Tentativa de listar para validar a chave e o modelo
                    available = [m.name.split('/')[-1] for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    print(f"📦 Modelos disponíveis para esta chave: {available}")
                    for m in potential_models:
                        if m in available:
                            working_model = m
                            break
                    if not working_model and available:
                        working_model = available[0]
                except Exception as e:
                    print(f"⚠️ Erro ao listar modelos (possível regra de firewall ou chave): {e}")
                    working_model = 'gemini-1.5-flash'
                
                if working_model:
                    self.gemini_model = genai.GenerativeModel(working_model)
                    print(f"🚀 Motor Vision OCR pronto: {working_model}")
            except Exception as e:
                print(f"❌ Erro crítico no setup do Gemini: {e}")
        else:
            print("❌ Nenhuma chave GEMINI_API_KEY encontrada em st.secrets ou ENV.")
        
        self.groq_client = None
        if self.groq_key:
            try:
                self.groq_client = Groq(api_key=self.groq_key)
                print(f"✅ Motor Groq pronto (Início: {self.groq_key[:8]}...)")
            except Exception as e:
                print(f"❌ Erro Groq: {e}")

    def analyze_image_ocr(self, uploaded_image):
        """
        Extrai texto e metadados de imagens (OCR Avançado) usando Gemini Vision.
        """
        if not self.gemini_model:
            return "❌ API Key do Gemini não configurada para OCR.", None

        try:
            img = PIL.Image.open(uploaded_image)
            
            prompt = """
            Analise esta imagem cuidadosamente. 
            1. Extraia TODO o texto legível.
            2. Identifique o tipo de documento (RG, CPF, Comprovante, Relatório, etc).
            3. Se houver dados tabelados ou estruturados, organize-os em um formato JSON.
            4. Dê 3 insights sobre a qualidade do documento ou os dados encontrados.
            
            Responda em Markdown estruturado.
            """
            
            response = self.gemini_model.generate_content([prompt, img])
            return response.text, img
        except Exception as e:
            return f"⚠️ Erro no processamento de imagem/OCR: {str(e)}", None

    def analyze_document_text(self, text, context="documento"):
        """
        Analisa blocos de texto ou CSVs usando LLMs.
        """
        prompt = f"Analise este {context} e extraia 3 insights estratégicos curtos:\n\n{text[:8000]}"
        
        # Prioridade: Gemini -> Groq -> Local (Silencioso)
        if self.gemini_model:
            try:
                response = self.gemini_model.generate_content(prompt)
                return f"## 🤖 Insights IA (Gemini)\n{response.text}"
            except:
                pass
        
        if self.groq_client:
            try:
                completion = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                return f"## 🤖 Insights IA (Groq)\n{completion.choices[0].message.content}"
            except:
                pass
        
        return "## 📊 Análise Local\nInsights de IA indisponíveis no momento. Usando apenas estatística local."

    @staticmethod
    def extract_text_from_docx(file):
        try:
            doc = Document(file)
            return '\n'.join([p.text for p in doc.paragraphs])
        except Exception as e:
            return f"Erro DOCX: {e}"

intel_engine = IntelEngine()
