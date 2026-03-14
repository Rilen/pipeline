
from fpdf import FPDF
import io
import plotly.io as pio
import pandas as pd
from datetime import datetime

class ReportEngine:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        
    def create_pdf(self, filename, summary_text, figures, df_stats=None):
        self.pdf.add_page()
        
        # Título
        self.pdf.set_font("helvetica", "B", 20)
        self.pdf.set_text_color(81, 69, 205) # Cor primária #5145cd
        self.pdf.cell(0, 15, f"Relatório Analítico: {filename}", ln=True, align="C")
        self.pdf.set_font("helvetica", "I", 10)
        self.pdf.set_text_color(100, 116, 139) # Cor secundária #64748b
        self.pdf.cell(0, 5, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
        self.pdf.ln(10)
        
        # Insights da IA
        self.pdf.set_font("helvetica", "B", 14)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(0, 10, "1. 🤖 Insights e Análise de IA", ln=True)
        self.pdf.set_font("helvetica", "", 11)
        
        # Limpar markdown simples do report_text
        clean_text = summary_text.replace("##", "").replace("**", "").replace("###", "")
        self.pdf.multi_cell(0, 7, clean_text)
        self.pdf.ln(5)
        
        # KPIs Básicos (se houver stats)
        if df_stats is not None:
             self.pdf.set_font("helvetica", "B", 14)
             self.pdf.cell(0, 10, "2. 📊 Métricas de Engenharia", ln=True)
             self.pdf.ln(2)
             self.pdf.set_font("helvetica", "", 10)
             # Resumo em tabela simples
             for col, val in df_stats.items():
                 self.pdf.cell(90, 7, f"{col}:", border=1)
                 self.pdf.cell(0, 7, f"{val}", border=1, ln=True)
             self.pdf.ln(10)

        # Gráficos
        if figures:
            self.pdf.set_font("helvetica", "B", 14)
            self.pdf.cell(0, 10, "3. 📈 Visualizações de Performance", ln=True)
            self.pdf.ln(5)
            
            for i, fig in enumerate(figures):
                try:
                    # Converte Plotly para imagem PNG na memória
                    img_bytes = pio.to_image(fig, format="png", width=800, height=450, scale=2)
                    img_buffer = io.BytesIO(img_bytes)
                    
                    # Verifica se cabe na página atual, se não, adiciona nova página
                    if self.pdf.get_y() > 200:
                        self.pdf.add_page()
                    
                    self.pdf.image(img_buffer, x=10, w=190)
                    self.pdf.ln(5)
                except Exception as e:
                    print(f"Erro ao incluir gráfico no PDF: {e}")
                    self.pdf.set_font("helvetica", "I", 10)
                    self.pdf.cell(0, 10, f"[Gráfico {i+1} não pôde ser renderizado]", ln=True)

        return self.pdf.output()

report_gen = ReportEngine()
