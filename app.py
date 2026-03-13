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
    df = None
    config = None
    
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
                      else:
                           # CSV Parsing Robusto (Suporta ;\t e decimais brasileiros)
                           try:
                                # Tenta primeiro com detecção automática e decimal em vírgula
                                df = pd.read_csv(uploaded_file, sep=None, engine='python', decimal=',', encoding='utf-8-sig')
                           except Exception:
                                try:
                                     # Fallback 1: Retorna ao início do stream e tenta com ponto decimal
                                     uploaded_file.seek(0)
                                     df = pd.read_csv(uploaded_file, sep=None, engine='python', encoding='utf-8-sig')
                                except Exception:
                                     # Fallback 2: Tenta encoding latin-1 (comum em arquivos Windows antigos)
                                     uploaded_file.seek(0)
                                     df = pd.read_csv(uploaded_file, sep=None, engine='python', encoding='latin-1')
                      
                      # Normalização/Limpeza (Engenharia de Software)
                      if enable_cleaning:
                           df = ds.clean_and_normalize(df)
                      
                      # Gera Resumo (Inteligência Híbrida)
                      summary = f"Estrutura: {list(df.columns)}. Resumo Estatístico: {df.describe().to_string()}"
                      report = intel.analyze_document_text(summary, "planilha")
                 except Exception as e:
                      st.error(f"Erro crítico no processamento de dados: {e}")
                      df = None
                      report = f"Erro fatal no parsing do arquivo: {str(e)}"

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
             # --- Estilo Específico para Impressão (Apenas via CSS) ---
             st.markdown("""
             <style>
                 @media print {
                     .stApp { background: white !important; }
                     .glass-card { 
                         border: 2px solid #eee !important; 
                         box-shadow: none !important; 
                         break-inside: avoid !important;
                         margin-bottom: 30px !important;
                         background: white !important;
                     }
                     .stPlotlyChart { break-inside: avoid !important; }
                     [data-testid="stSidebar"], [data-testid="stHeader"], .stTabs button { display: none !important; }
                     .print-hide { display: none !important; }
                     h1, h2, h3 { color: black !important; }
                 }
             </style>
             """, unsafe_allow_html=True)

             # Botão de Impressão (Visual apenas na Web)
             st.markdown('<div class="print-hide" style="text-align: right;">', unsafe_allow_html=True)
             if st.button("🖨️ Gerar PDF / Imprimir Relatório"):
                  st.info("💡 Dica: Use Ctrl+P no navegador e selecione 'Salvar como PDF' para exportar este relatório.")
             st.markdown('</div>', unsafe_allow_html=True)

             # --- CONTAINER DO RELATÓRIO EXECUTIVO ---
             st.markdown('<div class="glass-card">', unsafe_allow_html=True)
             st.markdown(f"## 📑 Relatório Executivo de Dados: {uploaded_file.name}")
             st.caption(f"Gerado em {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}")
             
             # Linha 1: KPIs Principais (Resumo do Dashboard)
             k1, k2, k3, k4 = st.columns(4)
             k1.metric("Volumetria", f"{config['num_records']:,} registros")
             k2.metric("Confiabilidade", f"{100 - config['missing_data']:.1f}%")
             k3.metric("Dimensões", f"{len(config['numeric_cols'])} Num / {len(config['cat_cols'])} Cat")
             
             # KPI Dinâmico de Performance
             if config['numeric_cols']:
                  main_val = config['numeric_cols'][0]
                  avg_val = df[main_val].mean()
                  k4.metric(f"Média ({main_val})", f"{avg_val:,.2f}")
             
             st.markdown("---")

             # --- GRID DE VISUALIZAÇÃO MULTIDIMENSIONAL ---
             cols = df.columns.tolist()
             has_year = any(word in [c.lower() for c in cols] for word in ['ano', 'year', 'data', 'date'])
             year_col = next((c for c in cols if c.lower() in ['ano', 'year']), None)

             # Área Principal de Gráficos (Grid 2x2 ou 1x2)
             g1, g2 = st.columns(2)

             with g1:
                  # Gráfico 1: Distribuição Geográfica/Setorial
                  if config['cat_cols']:
                       # Escolhe a categoria com cardinalidade razoável (nem 1 nem mil)
                       best_cat = next((c for c in config['cat_cols'] if 1 < df[c].nunique() < 15), config['cat_cols'][0])
                       fig_pie = px.pie(df, names=best_cat, hole=0.4, title=f"Mix por {best_cat.title()}",
                                     template="plotly_white", color_discrete_sequence=px.colors.qualitative.G10)
                       fig_pie.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2))
                       st.plotly_chart(fig_pie, use_container_width=True)
                  else:
                       st.info("Sem dados categóricos para distribuição.")

             with g2:
                  # Gráfico 2: Evolução ou Ranking
                  if has_year and config['numeric_cols']:
                       main_target = next((c for c in config['numeric_cols'] if c != year_col), config['numeric_cols'][0])
                       fig_evol = px.line(df.sort_values(year_col), x=year_col, y=main_target, 
                                        title=f"Série Temporal: {main_target.title()}",
                                        template="plotly_white", markers=True)
                       fig_evol.update_traces(line_color="#5145cd", line_width=3)
                       st.plotly_chart(fig_evol, use_container_width=True)
                  elif config['cat_cols'] and config['numeric_cols']:
                       target = config['numeric_cols'][0]
                       cat = config['cat_cols'][0]
                       df_rank = ds.calculate_group_averages(df, cat, target)
                       fig_bar = px.bar(df_rank, x=cat, y=target, title=f"Ranking: {target} por {cat}",
                                      color=target, template="plotly_white", color_continuous_scale="Viridis")
                       st.plotly_chart(fig_bar, use_container_width=True)

             # Linha Especial: Análise de Correlação ou Cruzamento
             st.markdown("### 🔍 Cruzamento Dinâmico de Indicadores")
             c_col1, c_col2 = st.columns([1, 2])
             
             with c_col1:
                  st.markdown('<div class="print-hide">', unsafe_allow_html=True)
                  x_axis = st.selectbox("Eixo X (Relatório):", config['cat_cols'] + config['numeric_cols'] if config['cat_cols'] else config['numeric_cols'], index=0)
                  y_axis = st.selectbox("Eixo Y (Relatório):", config['numeric_cols'], index=min(1, len(config['numeric_cols'])-1))
                  
                  # Novo: Seletor de Tipo Manual
                  chart_pref = st.segmented_control(
                       "Formato Visual:", 
                       options=["Auto", "Barras", "Linhas", "Dispersão", "Distribuição"],
                       default="Auto"
                  )
                  st.markdown('</div>', unsafe_allow_html=True)
                  
                  # Insights Automáticos (Simulado)
                  st.info(f"O indicador **{y_axis}** apresenta variação de {((df[y_axis].max() - df[y_axis].min())/df[y_axis].min()*100):.1f}% entre os extremos.")

             with c_col2:
                  # --- Lógica Semântica de Seleção de Gráfico ---
                  df_clean = df.copy()
                  if x_axis in config['cat_cols']:
                       df_clean[x_axis] = df_clean[x_axis].astype(str).str.strip()
                  
                  df_plot = df_clean.groupby(x_axis)[y_axis].mean().reset_index()
                  
                  try:
                       df_plot[x_axis] = pd.to_numeric(df_plot[x_axis])
                       df_plot = df_plot.sort_values(x_axis)
                  except:
                       df_plot = df_plot.sort_values(x_axis)

                  is_time = any(w in x_axis.lower() for w in ['ano', 'year', 'data', 'date', 'mês', 'month'])
                  
                  # Escolha do Tipo (Manual vs Auto)
                  final_type = chart_pref
                  if final_type == "Auto":
                       if is_time: final_type = "Linhas" if df_plot[x_axis].nunique() > 10 else "Barras"
                       elif x_axis in config['cat_cols']: final_type = "Barras"
                       else: final_type = "Dispersão"

                  # Renderização Baseada na Escolha
                  if final_type == "Barras":
                       # Decide horizontal ou vertical baseado no tamanho do texto e quantidade
                       is_long_text = df_plot[x_axis].astype(str).str.len().max() > 15
                       fig_dyn = px.bar(df_plot if not is_long_text else df_plot.sort_values(y_axis), 
                                      x=y_axis if is_long_text else x_axis, 
                                      y=x_axis if is_long_text else y_axis, 
                                      orientation='h' if is_long_text else 'v',
                                      title=f"Analítico: {y_axis} por {x_axis}",
                                      template="plotly_white", color=y_axis, color_continuous_scale="Cividis")
                  
                  elif final_type == "Linhas":
                       fig_dyn = px.area(df_plot, x=x_axis, y=y_axis, title=f"Tendência: {y_axis}",
                                       template="plotly_white", line_shape="spline")
                       fig_dyn.update_traces(line_color="#5145cd", fillcolor="rgba(81, 69, 205, 0.2)")

                  elif final_type == "Distribuição":
                       fig_dyn = px.box(df_clean, x=x_axis, y=y_axis, title=f"Distribuição: {y_axis} por {x_axis}",
                                      template="plotly_white", color=x_axis)

                  else: # Dispersão
                       fig_dyn = px.scatter(df_clean, x=x_axis, y=y_axis, trendline="ols", 
                                          title=f"Correlação: {x_axis} vs {y_axis}", template="plotly_white")
                       fig_dyn.update_traces(marker=dict(size=12, color='#5145cd'))

                  fig_dyn.update_layout(height=450, margin=dict(l=20, r=20, t=50, b=20), showlegend=False)
                  st.plotly_chart(fig_dyn, use_container_width=True)

             st.markdown('</div>', unsafe_allow_html=True)

        else:
             st.info("A visualização gráfica automática está disponível apenas para planilhas e JSONs.")

    with tab_raw:
        if df is not None:
             st.subheader("📋 Estrutura da Tabela")
             st.dataframe(df, use_container_width=True)
             
             # Ação de Engenheiro: Ingestão e Exportação
             st.markdown("---")
             ce1, ce2 = st.columns(2)
             
             with ce1:
                  if st.button("🚀 Commit de Dados para Firestore", use_container_width=True):
                       with st.spinner("Subindo em lote..."):
                            msg = db_interface.batch_upload_df(df, target_collection)
                            st.success(msg)
                            st.balloons()
             
             with ce2:
                  csv = df.to_csv(index=False).encode('utf-8-sig')
                  st.download_button(
                       label="📥 Exportar para CSV (Excel)",
                       data=csv,
                       file_name=f"analise_{uploaded_file.name.split('.')[0]}.csv",
                       mime='text/csv',
                       use_container_width=True
                  )
        else:
             st.markdown('<div class="glass-card">', unsafe_allow_html=True)
             st.markdown("### Extração de Metadados Brutos")
             st.code(report[:5000] if report else "Vazio")
             
             if report:
                  csv_report = f"Insight,Conteudo\nAnálise IA,\"{report.replace('\"', '\"\"')}\"".encode('utf-8-sig')
                  st.download_button(
                       label="📥 Exportar Relatório em CSV",
                       data=csv_report,
                       file_name=f"relatorio_{uploaded_file.name.split('.')[0]}.csv",
                       mime='text/csv',
                       use_container_width=True
                  )
             st.markdown('</div>', unsafe_allow_html=True)

# --- Rodapé ---
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #94a3b8;">'
    'Desenvolvido por RTL Engine @ 2026 | Arquitetura Híbrida Gemini & Groq'
    '</div>', 
    unsafe_allow_html=True
)
