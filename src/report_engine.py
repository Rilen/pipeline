
from fpdf import FPDF
import io
import plotly.io as pio
import pandas as pd
from datetime import datetime

class ReportEngine:
    """
    Motor de geração de relatórios PDF.
    Cada chamada cria uma nova instância FPDF para evitar estado residual.
    """
    
    def create_pdf(self, filename, summary_text, figures, df_stats=None):
        """Gera um relatório PDF completo com insights, métricas e gráficos."""
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Título
        pdf.set_font("helvetica", "B", 20)
        pdf.set_text_color(81, 69, 205)  # Cor primária #5145cd
        pdf.cell(0, 15, f"Relatorio Analitico: {filename}", ln=True, align="C")
        pdf.set_font("helvetica", "I", 10)
        pdf.set_text_color(100, 116, 139)  # Cor secundária #64748b
        pdf.cell(0, 5, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
        pdf.ln(10)
        
        # Insights da IA
        pdf.set_font("helvetica", "B", 14)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, "1. Insights e Analise de IA", ln=True)
        pdf.set_font("helvetica", "", 11)
        
        # Limpar markdown simples do report_text e caracteres especiais
        clean_text = summary_text.replace("##", "").replace("**", "").replace("###", "")
        # Remove caracteres que fpdf não suporta em latin-1
        clean_text = clean_text.encode('latin-1', errors='replace').decode('latin-1')
        pdf.multi_cell(0, 7, clean_text)
        pdf.ln(5)
        
        # KPIs Básicos (se houver stats)
        if df_stats is not None:
             pdf.set_font("helvetica", "B", 14)
             pdf.cell(0, 10, "2. Metricas de Engenharia", ln=True)
             pdf.ln(2)
             pdf.set_font("helvetica", "", 10)
             for col, val in df_stats.items():
                 col_safe = str(col).encode('latin-1', errors='replace').decode('latin-1')
                 val_safe = str(val).encode('latin-1', errors='replace').decode('latin-1')
                 pdf.cell(90, 7, f"{col_safe}:", border=1)
                 pdf.cell(0, 7, f"{val_safe}", border=1, ln=True)
             pdf.ln(10)

        # Gráficos
        if figures:
            pdf.set_font("helvetica", "B", 14)
            pdf.cell(0, 10, "3. Visualizacoes de Performance", ln=True)
            pdf.ln(5)
            
            for i, fig in enumerate(figures):
                try:
                    # Converte Plotly para imagem PNG na memória
                    img_bytes = pio.to_image(fig, format="png", width=800, height=450, scale=2)
                    img_buffer = io.BytesIO(img_bytes)
                    
                    # Verifica se cabe na página atual, se não, adiciona nova página
                    if pdf.get_y() > 200:
                        pdf.add_page()
                    
                    pdf.image(img_buffer, x=10, w=190)
                    pdf.ln(5)
                except Exception as e:
                    print(f"Erro ao incluir grafico no PDF: {e}")
                    pdf.set_font("helvetica", "I", 10)
                    pdf.cell(0, 10, f"[Grafico {i+1} nao pode ser renderizado]", ln=True)

        return pdf.output()

report_gen = ReportEngine()
