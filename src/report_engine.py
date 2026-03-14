import re
try:
    import kaleido
except ImportError:
    kaleido = None
import streamlit as st
from fpdf import FPDF
import io
import plotly.io as pio
import pandas as pd
from datetime import datetime

class ReportEngine:
    """
    Motor de geração de relatórios PDF.
    Utiliza fpdf2 para criar documentos profissionais.
    """
    
    def _sanitize_text(self, text):
        """Remove emojis e caracteres não compatíveis com o encoding latin-1 do FPDF básico."""
        if not text:
            return ""
        # Remove markdown comum
        text = text.replace("##", "").replace("**", "").replace("###", "").replace("`", "")
        # Remove caracteres fora do range latin-1 (incluindo emojis)
        # Substitui por um espaço ou caractere aproximado
        return "".join(c if ord(c) < 256 else " " for c in text)

    def create_pdf(self, filename, summary_text, figures, df_stats=None):
        """Gera um relatório PDF completo com insights, métricas e gráficos."""
        try:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            
            # Título principal
            pdf.set_font("helvetica", "B", 22)
            pdf.set_text_color(81, 69, 205)  # Cor #5145cd
            pdf.cell(0, 20, f"Dashboard Analítico: {self._sanitize_text(filename)}", ln=True, align="C")
            
            pdf.set_font("helvetica", "I", 10)
            pdf.set_text_color(100, 116, 139)  # Cor #64748b
            ts = datetime.now().strftime('%d/%m/%Y %H:%M')
            pdf.cell(0, 5, f"Relatório Gerado via RTL Engine | {ts}", ln=True, align="C")
            pdf.ln(12)
            
            # --- Seção 1: Insights Estratégicos ---
            pdf.set_font("helvetica", "B", 15)
            pdf.set_text_color(30, 41, 59)
            pdf.cell(0, 10, "1. Análise Reversa & Insights de IA", ln=True)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(4)
            
            pdf.set_font("helvetica", "", 11)
            pdf.set_text_color(51, 65, 85)
            # Sanitiza o texto dos insights
            clean_text = self._sanitize_text(summary_text)
            pdf.multi_cell(0, 7, clean_text)
            pdf.ln(8)
            
            # --- Seção 2: Métricas de Qualidade de Dados ---
            if df_stats is not None:
                pdf.set_font("helvetica", "B", 15)
                pdf.set_text_color(30, 41, 59)
                pdf.cell(0, 10, "2. Metricas e Perfil de Engenharia", ln=True)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(6)
                
                pdf.set_font("helvetica", "B", 10)
                pdf.set_fill_color(241, 245, 249)
                pdf.cell(95, 10, " Atributo / Metrica", border=1, fill=True)
                pdf.cell(95, 10, " Valor Identificado", border=1, fill=True, ln=True)
                
                pdf.set_font("helvetica", "", 10)
                for col, val in df_stats.items():
                    col_s = self._sanitize_text(str(col))
                    val_s = self._sanitize_text(str(val))
                    pdf.cell(95, 8, f" {col_s}", border=1)
                    pdf.cell(95, 8, f" {val_s}", border=1, ln=True)
                pdf.ln(12)

            # --- Seção 3: Visualizações Gráficas ---
            if figures:
                # Filtrar figuras nulas ou vazias
                valid_figs = [f for f in figures if f is not None]
                if valid_figs:
                    if pdf.get_y() > 200: pdf.add_page()
                    pdf.set_font("helvetica", "B", 15)
                    pdf.set_text_color(30, 41, 59)
                    pdf.cell(0, 10, "3. Visualizacoes de Alta Performance", ln=True)
                    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                    pdf.ln(8)
                    
                    for i, fig in enumerate(valid_figs):
                        try:
                            # Renderização da imagem (exige kaleido)
                            img_bytes = pio.to_image(fig, format="png", width=1000, height=550, scale=2, engine="kaleido")
                            img_buffer = io.BytesIO(img_bytes)
                            
                            # Paginação automática para imagens grandes
                            if pdf.get_y() > 180:
                                pdf.add_page()
                            
                            pdf.image(img_buffer, x=10, w=190)
                            pdf.ln(5)
                        except Exception as e:
                            print(f"DEBUG: Falha ao exportar grafico {i}: {e}")
                            pdf.set_font("helvetica", "I", 9)
                            pdf.set_text_color(239, 68, 68)
                            pdf.cell(0, 8, f"[Aviso: Grafico {i+1} omitido devido a erro de renderizacao de imagem]", ln=True)
                            pdf.set_text_color(51, 65, 85)

            return pdf.output()
        except Exception as e:
            print(f"CRITICAL: Erro na geracao do PDF: {e}")
            raise e

def get_report_engine():
    """Factory para o motor de relatorios."""
    return ReportEngine()
