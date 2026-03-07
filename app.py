import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import io
from PIL import Image

# --- Novos Módulos Arquitetados (Clean Code) ---
from src.intelligence import intel_engine as intel
from src.analytics import analytics as ds
from src.data_engine import db_interface

# --- Configurações de Interface Premium ---
st.set_page_config(
    page_title="Analista IA Profissional | Hybrid Analytics 2026",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Estilos Visuais Avançados (Glassmorphism & Vibrancy)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Outfit:wght@300;600;800&display=swap');

    :root {
        --primary: #5145cd;
        --secondary: #2dd4bf;
    }

    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px 0 rgba(31, 38, 135, 0.12);
        border: 1px solid rgba(81, 69, 205, 0.2);
    }

    /* Modern Headers */
    h1 {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        background: linear-gradient(90deg, #5145cd, #2dd4bf);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        margin-bottom: 0px !important;
    }
    
    .stMetric {
        background: white;
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }

    /* Hide standard UI fluff */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Header & Navegação ---
st.title("🤖 Analista IA PRO")
st.caption("Engenharia de Dados e Análise Preditiva de Alta Performance | V2.1")
st.markdown("---")

# --- Interface Principal (Área de Upload) ---
col_u1, col_u2 = st.columns([2, 1])

with col_u1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📁 Central de Arquivos Multi-IA")
    uploaded_file = st.file_uploader(
        "Arraste planilhas (.xlsx, .csv), documentos (.docx), imagens (.jpg, .png) ou dados (.json)", 
        type=["xlsx", "csv", "docx", "json", "png", "jpg", "jpeg"], 
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_u2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("⚙️ Configurações Rápidas")
    target_collection = st.text_input("Coleção Firestore", value="dados_analise_ia")
    enable_cleaning = st.toggle("Limpeza Automática (Normalização)", value=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Fluxo de Processamento Inteligente ---
if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    with st.status("🧠 Engine processando análise estratégica...", expanded=True) as status:
        
        # --- CASO 1: IMAGENS (OCR + VISION) ---
        if file_type in ['png', 'jpg', 'jpeg']:
            st.write("🔍 Iniciando Visão Computacional / OCR...")
            report, image = intel.analyze_image_ocr(uploaded_file)
            df = None
            
        # --- CASO 2: DOCUMENTOS E PLANILHAS ---
        else:
            st.write("📊 Analisando estrutura de dados...")
            
            if file_type == 'docx':
                 raw_text = intel.extract_text_from_docx(uploaded_file)
                 report = intel.analyze_document_text(raw_text, "documento")
                 df = None
            else:
                 # CSV / XLSX / JSON
                 try:
                      if file_type == 'xlsx': df = pd.read_excel(uploaded_file)
                      elif file_type == 'json': df = pd.read_json(uploaded_file)
                      else: df = pd.read_csv(uploaded_file)
                      
                      # Normalização/Limpeza (Engenharia de Software)
                      if enable_cleaning:
                           df = ds.clean_and_normalize(df)
                      
                      # Gera Resumo (Inteligência Híbrida)
                      summary = f"Estrutura: {list(df.columns)}. Resumo Estatístico: {df.describe().to_string()}"
                      report = intel.analyze_document_text(summary, "planilha")
                 except Exception as e:
                      st.error(f"Erro ao processar dados: {e}")
                      df = None
                      report = "Erro fatal no parsing do arquivo."

        status.update(label="✅ Análise concluída!", state="complete", expanded=False)

    # --- DISPLAYS DE RESULTADOS ---
    tab_report, tab_viz, tab_raw = st.tabs(["🤖 Insights de IA", "📊 Dash de Alta Performance", "📋 Visão de Engenheiro"])

    with tab_report:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if file_type in ['png', 'jpg', 'jpeg'] and image is not None:
             # Convertemos para RGB para garantir que o Streamlit consiga processar sem depender de metadados de formato
             if image.mode != 'RGB':
                 display_img = image.convert('RGB')
             else:
                 display_img = image
             st.image(display_img, caption="Visualização do Original", use_container_width=True)
        st.markdown(report)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_viz:
        if df is not None:
             config, stats = ds.generate_statistical_profile(df)
             
             # KPIs
             k1, k2, k3, k4 = st.columns(4)
             k1.metric("Registros", f"{config['num_records']:,}")
             k2.metric("Qualidade", f"{100 - config['missing_data']:.1f}%")
             k3.metric("Numéricas", len(config['numeric_cols']))
             k4.metric("Texto", len(config['cat_cols']))
             
             st.markdown("---")
             
             # Gráficos
             g1, g2 = st.columns(2)
             
             with g1:
                  if config['cat_cols']:
                       sel_cat = st.selectbox("Categorizar por:", config['cat_cols'])
                       fig_pie = px.pie(df, names=sel_cat, hole=0.5, template="plotly_white",
                                     title=f"Mix Geográfico/Setorial: {sel_cat}",
                                     color_discrete_sequence=px.colors.qualitative.Pastel)
                       st.plotly_chart(fig_pie, use_container_width=True)
                  else:
                       st.info("Nenhuma categoria detectada.")

             with g2:
                  if config['numeric_cols']:
                       y_val = st.selectbox("Analisar Valor de:", config['numeric_cols'])
                       if config['cat_cols']:
                            df_grouped = ds.calculate_group_averages(df, config['cat_cols'][0], y_val)
                            fig_bar = px.bar(df_grouped, x=config['cat_cols'][0], y=y_val, 
                                          title=f"Ranking: {y_val} por {config['cat_cols'][0]}",
                                          template="plotly_white", color=y_val)
                            st.plotly_chart(fig_bar, use_container_width=True)
                       else:
                            st.line_chart(df[y_val])

        else:
             st.info("A visualização gráfica automática está disponível apenas para planilhas e JSONs.")

    with tab_raw:
        if df is not None:
             st.subheader("📋 Estrutura da Tabela")
             st.dataframe(df, use_container_width=True)
             
             # Ação de Engenheiro: Ingestão
             st.markdown("---")
             if st.button("🚀 Commit de Dados para Firestore", use_container_width=True):
                  with st.spinner("Subindo em lote..."):
                       msg = db_interface.batch_upload_df(df, target_collection)
                       st.success(msg)
                       st.balloons()
        else:
             st.markdown('<div class="glass-card">', unsafe_allow_html=True)
             st.markdown("### Extração de Metadados Brutos")
             st.code(report[:5000] if report else "Vazio")
             st.markdown('</div>', unsafe_allow_html=True)

# --- Rodapé ---
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #94a3b8;">'
    'Desenvolvido por RTL Engine @ 2026 | Arquitetura Híbrida Gemini & Groq'
    '</div>', 
    unsafe_allow_html=True
)
