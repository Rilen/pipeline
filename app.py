import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import io
from PIL import Image

# --- Módulos Arquitetados (Clean Code) ---
# Imports seguros: apenas classes/funções, sem instanciação pesada
from src.intelligence import get_intel_engine
from src.analytics import analytics as ds
from src.data_engine import get_db_interface
from src.report_engine import ReportEngine

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
    header {visibility: hidden;}
    
    /* Remove huge top padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 5rem !important;
        padding-right: 5rem !important;
    }

    /* FIX PRINT BUG: Ensure full page is captured */
    @media print {
        .stApp {
            overflow: visible !important;
            height: auto !important;
        }
        .main {
            overflow: visible !important;
            height: auto !important;
        }
        [data-testid="stSidebar"], [data-testid="stHeader"], .stTabs button, .print-hide { 
            display: none !important; 
        }
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- Interface Principal (Área de Upload) ---
col_u1, col_u2 = st.columns([2, 1])

with col_u1:
    st.subheader("📁 Central de Arquivos Multi-IA")
    uploaded_file = st.file_uploader(
        "Arraste planilhas (.xlsx, .csv), documentos (.docx), imagens (.jpg, .png), dados (.json) ou arquivos (.xml)", 
        type=["xlsx", "csv", "docx", "json", "xml", "png", "jpg", "jpeg"], 
        label_visibility="collapsed"
    )

with col_u2:
    st.subheader("⚙️ Configurações Rápidas")
    target_collection = st.text_input("Coleção Firestore", value="dados_analise_ia")
    enable_cleaning = st.toggle("Limpeza Automática (Normalização)", value=True)

# --- Fluxo de Processamento Inteligente ---
if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1].lower()
    df = None
    config = None
    report = ""
    image = None
    
    # Carrega o conteúdo para a memória de forma imutável (bytes)
    file_content = uploaded_file.getvalue()
    
    with st.status("🧠 Engine processando análise estratégica...", expanded=True) as status:
        # --- CASO 1: IMAGENS (OCR + VISION) ---
        if file_type in ['png', 'jpg', 'jpeg']:
            st.write("🔍 Iniciando Visão Computacional / OCR...")
            report, image = get_intel_engine().analyze_image_ocr(io.BytesIO(file_content))
            df = None
            
        # --- CASO 2: DOCUMENTOS E PLANILHAS ---
        else:
            st.write("📊 Analisando estrutura de dados...")
            
            if file_type == 'docx':
                raw_text = get_intel_engine().extract_text_from_docx(io.BytesIO(file_content))
                report = get_intel_engine().analyze_document_text(raw_text, "documento")
            else:
                # CSV / XLSX / JSON / XML
                try:
                    if file_type == 'xlsx': 
                        df = pd.read_excel(io.BytesIO(file_content))
                    elif file_type == 'json': 
                        df = pd.read_json(io.BytesIO(file_content))
                    elif file_type == 'xml':
                        # XML Parsing robusto com suporte a ISO-8859-1 e encodings brasileiros
                        import re
                        from lxml import etree
                        
                        xml_parsed = False
                        
                        # Tentativa 1: Direto com lxml (respeita encoding do header)
                        if not xml_parsed:
                            try:
                                df = pd.read_xml(io.BytesIO(file_content), xpath=".//Servidor")
                                xml_parsed = True
                            except Exception:
                                pass
                        
                        # Tentativa 2: Decodifica ISO-8859-1 para UTF-8 e remove declaração de encoding
                        if not xml_parsed:
                            try:
                                # Decodifica como latin-1 (ISO-8859-1)
                                xml_str = file_content.decode('latin-1', errors='replace')
                                # Remove a declaração de encoding para evitar conflito
                                xml_str = re.sub(r"encoding=['\"][^'\"]*['\"]", '', xml_str)
                                xml_bytes_utf8 = xml_str.encode('utf-8')
                                
                                try:
                                    df = pd.read_xml(io.BytesIO(xml_bytes_utf8), xpath=".//Servidor")
                                except Exception:
                                    df = pd.read_xml(io.BytesIO(xml_bytes_utf8))
                                xml_parsed = True
                            except Exception:
                                pass
                        
                        # Tentativa 3: lxml com recover=True (tolerante a erros de encoding)
                        if not xml_parsed:
                            try:
                                parser = etree.XMLParser(recover=True, encoding='latin-1')
                                tree = etree.fromstring(file_content, parser=parser)
                                
                                # Tenta extrair elementos Servidor
                                servidores = tree.findall('.//Servidor')
                                if servidores:
                                    rows = []
                                    for s in servidores:
                                        row = {child.tag: (child.text or '').strip() for child in s}
                                        rows.append(row)
                                    df = pd.DataFrame(rows)
                                else:
                                    # Genérico: pega todos os filhos do root
                                    rows = []
                                    for elem in tree:
                                        row = {child.tag: (child.text or '').strip() for child in elem}
                                        rows.append(row)
                                    df = pd.DataFrame(rows)
                                xml_parsed = True
                            except Exception:
                                pass
                        
                        # Tentativa 4: Último recurso - lxml genérico sem xpath
                        if not xml_parsed:
                            try:
                                xml_str = file_content.decode('latin-1', errors='ignore')
                                xml_str = re.sub(r"encoding=['\"][^'\"]*['\"]", '', xml_str)
                                df = pd.read_xml(io.StringIO(xml_str))
                                xml_parsed = True
                            except Exception as xml_err:
                                raise Exception(f"Não foi possível processar o XML: {xml_err}")
                    else:
                        # CSV Parsing Robusto
                        try:
                            df = pd.read_csv(io.BytesIO(file_content), sep=None, engine='python', decimal=',', encoding='utf-8-sig')
                        except Exception:
                            try:
                                df = pd.read_csv(io.BytesIO(file_content), sep=None, engine='python', encoding='utf-8-sig')
                            except Exception:
                                df = pd.read_csv(io.BytesIO(file_content), sep=None, engine='python', encoding='latin-1')
                    
                    # Normalização/Limpeza (Engenharia de Software)
                    if enable_cleaning and df is not None:
                        df = ds.clean_and_normalize(df)

                    # Gera Resumo (Inteligência Híbrida)
                    summary = f"Estrutura: {list(df.columns)}. Resumo Estatístico: {df.describe().to_string()}"
                    report = get_intel_engine().analyze_document_text(summary, "planilha")
                except Exception as e:
                    st.error(f"Erro crítico no processamento de dados: {e}")
                    df = None
                    report = f"Erro fatal no parsing do arquivo: {str(e)}"

        status.update(label="✅ Análise concluída!", state="complete", expanded=False)

    # --- DISPLAYS DE RESULTADOS ---
    tab_report, tab_viz, tab_raw = st.tabs(["🤖 Insights de IA", "📊 Dash de Alta Performance", "📋 Visão de Engenheiro"])

    with tab_report:
        if file_type in ['png', 'jpg', 'jpeg'] and image is not None:
             if image.mode != 'RGB':
                 display_img = image.convert('RGB')
             else:
                 display_img = image
             st.image(display_img, caption="Visualização do Original", width="stretch")
        st.markdown(report)

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

             # Coletor de Figuras para o PDF
             all_figs = []

             # --- CONTAINER DO RELATÓRIO EXECUTIVO ---
             st.markdown(f"## 📑 Dashboard de Performance Digital: {uploaded_file.name}")
             st.caption(f"Análise processada em {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}")
             
             # --- Dashboard Executivo (Grid Responsivo) ---
             st.markdown("""
             <style>
             .dashboard-grid {
                 display: grid;
                 grid-template-columns: repeat(3, 1fr);
                 gap: 15px;
                 margin-bottom: 20px;
             }
             @media (max-width: 768px) {
                 .dashboard-grid {
                     grid-template-columns: 1fr;
                 }
             }
             .metric-card {
                 background: white;
                 padding: 20px;
                 border-radius: 12px;
                 border: 1px solid #e2e8f0;
                 box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
                 transition: transform 0.2s;
             }
             .metric-card:hover { transform: translateY(-2px); }
             @media print {
                 .dashboard-grid { grid-template-columns: repeat(2, 1fr) !important; gap: 10px; }
                 .print-hide { display: none !important; }
             }
             </style>
             """, unsafe_allow_html=True)

             # 1. KPIs em Grid (3 Colunas)
             st.markdown('<div class="dashboard-grid">', unsafe_allow_html=True)
             
             # Card 1: Volumetria
             st.markdown(f'''<div class="metric-card">
                 <div style="color: #64748b; font-size: 0.9rem; font-weight: 600;">VOLUMETRIA</div>
                 <div style="color: #1e293b; font-size: 1.8rem; font-weight: 700;">{config.get('num_records', 0):,}</div>
                 <div style="color: #94a3b8; font-size: 0.8rem;">Registros Processados</div>
             </div>''', unsafe_allow_html=True)
             
             # Card 2: Qualidade
             st.markdown(f'''<div class="metric-card">
                 <div style="color: #64748b; font-size: 0.9rem; font-weight: 600;">QUALIDADE DATA</div>
                 <div style="color: #10b981; font-size: 1.8rem; font-weight: 700;">{config.get('completeness_score', 100):.1f}%</div>
                 <div style="color: #94a3b8; font-size: 0.8rem;">Integridade de Preenchimento</div>
             </div>''', unsafe_allow_html=True)
             
             # Card 3: Amplitude
             st.markdown(f'''<div class="metric-card">
                 <div style="color: #64748b; font-size: 0.9rem; font-weight: 600;">AMPLITUDE</div>
                 <div style="color: #5145cd; font-size: 1.8rem; font-weight: 700;">{len(config.get('cat_cols', []) + config.get('numeric_cols', []))}</div>
                 <div style="color: #94a3b8; font-size: 0.8rem;">Indicadores Mapeados</div>
             </div>''', unsafe_allow_html=True)
             
             st.markdown('</div>', unsafe_allow_html=True)

             # 2. Seção de Gráficos Principais
             # --- Espaço para Gráfico 1 ---
             with st.container():
                  st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                  
                  # Detecção flexível de colunas
                  fin_receita = next((c for c in df.columns if 'receita' in c.lower() or 'revenue' in c.lower()), None)
                  fin_despesa = next((c for c in df.columns if 'despesa' in c.lower() or 'expense' in c.lower() or 'custo' in c.lower()), None)
                  fin_tempo = next((c for c in df.columns if c.lower() in ['ano', 'mes', 'data', 'date', 'year']), None)
                  
                  if config.get('is_financial') and fin_tempo and (fin_receita or fin_despesa):
                       y_cols = [c for c in [fin_receita, fin_despesa] if c]
                       df_plot_fin = df.groupby(fin_tempo, as_index=False)[y_cols].sum()
                       
                       fig_fin = px.line(df_plot_fin, x=fin_tempo, y=y_cols, 
                                       title="💰 Fluxo Financeiro Temporal", template="plotly_white")
                       fig_fin.update_layout(height=350, margin=dict(l=0,r=0,b=0,t=40), legend=dict(orientation="h", y=-0.2))
                       st.plotly_chart(fig_fin, width="stretch")
                       all_figs.append(fig_fin)
                  elif config.get('numeric_cols'):
                       target = config['numeric_cols'][0]
                       fig_dist = px.histogram(df, x=target, 
                                             title=f"📊 Distribuição de {target}", 
                                             template="plotly_white", color_discrete_sequence=['#5145cd'])
                       fig_dist.update_layout(height=350, margin=dict(l=0,r=0,b=0,t=40))
                       st.plotly_chart(fig_dist, width="stretch")
                       all_figs.append(fig_dist)
                  else:
                       st.info("ℹ️ Carregue dados numéricos para ver o perfil de distribuição.")

             # --- Espaço para Gráfico 2 ---
             with st.container():
                  st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                  if config.get('is_financial') and fin_tempo and fin_receita and fin_despesa:
                       df_balance = df.groupby(fin_tempo, as_index=False).sum(numeric_only=True)
                       df_balance['saldo'] = df_balance[fin_receita] - df_balance[fin_despesa]
                       
                       fig_bal = px.bar(df_balance, x=fin_tempo, y='saldo', title="⚖️ Superávit/Déficit",
                                      color='saldo', color_continuous_scale="RdYlGn", template="plotly_white")
                       fig_bal.update_layout(height=350, margin=dict(l=0,r=0,b=0,t=40))
                       st.plotly_chart(fig_bal, width="stretch")
                       all_figs.append(fig_bal)
                  elif len(config.get('numeric_cols', [])) > 1:
                       fig_scat = px.scatter(df, x=config['numeric_cols'][0], y=config['numeric_cols'][1],
                                           title="🎯 Correlação Principal", template="plotly_white")
                       fig_scat.update_layout(height=350, margin=dict(l=0,r=0,b=0,t=40))
                       st.plotly_chart(fig_scat, width="stretch")
                       all_figs.append(fig_scat)
                  else:
                       st.info("🎯 Para correlação, são necessários ao menos dois indicadores numéricos.")

             #--- Espaço para Gráfico 3 ---
             with st.container():
                  st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                  if config.get('cat_cols') and config.get('numeric_cols'):
                       target = config['numeric_cols'][0]
                       cat = config['cat_cols'][0]
                       df_rank = ds.calculate_group_averages(df, cat, target)
                       if df_rank is not None:
                           df_rank = df_rank.head(10)
                           fig_bar = px.bar(df_rank, x=target, y=cat, orientation='h', title=f"🏆 Top 10 {cat}",
                                          color=target, template="plotly_white", color_continuous_scale="Viridis")
                           fig_bar.update_layout(height=350, margin=dict(l=0,r=0,b=0,t=40))
                           st.plotly_chart(fig_bar, width="stretch")
                           all_figs.append(fig_bar)
                  st.markdown('</div>', unsafe_allow_html=True)

             # Linha Especial: Análise de Correlação ou Cruzamento
             st.markdown("### 🔍 Cruzamento Dinâmico de Indicadores")
             c_col1, c_col2 = st.columns([1, 2])
             
             with c_col1:
                  st.markdown('<div class="print-hide">', unsafe_allow_html=True)
                  # Filtra opções disponíveis
                  avail_x = config.get('cat_cols', []) + config.get('numeric_cols', []) + config.get('date_cols', [])
                  avail_y = config.get('numeric_cols', [])
                  
                  if not avail_x or not avail_y:
                      st.warning("⚠️ O dataset não possui colunas numéricas ou categóricas suficientes para análise dinâmica.")
                      x_axis, y_axis, chart_pref = None, None, "Auto"
                  else:
                      # Defaults Inteligentes (Ano/Data no X, Valor/Total no Y)
                      def_x_idx = 0
                      for i, col in enumerate(avail_x):
                          if any(h in str(col).lower() for h in ['ano', 'data', 'date', 'mês', 'year']):
                              def_x_idx = i
                              break
                      
                      def_y_idx = 0
                      for i, col in enumerate(avail_y):
                          if any(h in str(col).lower() for h in ['total', 'valor', 'receita', 'despesa', 'preço', 'amount']):
                              def_y_idx = i
                              break

                      x_axis = st.selectbox("Eixo X (Categorias/Tempo):", options=avail_x, index=def_x_idx)
                      y_axis = st.selectbox("Eixo Y (Métrica/Valor):", options=avail_y, index=def_y_idx)
                      
                      chart_pref = st.segmented_control(
                           "Formato Visual:", 
                           options=["Auto", "Barras", "Linhas", "Dispersão", "Distribuição"],
                           default="Auto"
                      )
                      if not chart_pref: chart_pref = "Auto"
                  
                  # Insights Automáticos
                  if avail_x and avail_y and y_axis and y_axis in df.columns:
                       try:
                           min_val = df[y_axis].min()
                           max_val = df[y_axis].max()
                           variation = ((max_val - min_val) / min_val * 100) if min_val and min_val != 0 else 0
                           st.info(f"💡 O indicador **{y_axis}** apresenta variação de {variation:.1f}% entre os extremos registrados.")
                       except Exception:
                           pass

             with c_col2:
                  if not avail_x or not avail_y or not x_axis or not y_axis:
                       st.info("📊 Selecione os eixos ao lado para gerar o cruzamento de dados.")
                  else:
                      # --- Lógica Semântica de Seleção de Gráfico ---
                      df_clean = df.copy()
                      
                      if x_axis == y_axis:
                           st.warning("⚠️ Selecione indicadores diferentes para X e Y para uma análise comparativa.")
                      
                      # Tratamento especial para Datas no X
                      if x_axis in config.get('date_cols', []):
                           df_clean[x_axis] = pd.to_datetime(df_clean[x_axis]).dt.date
                      
                      if x_axis in config.get('cat_cols', []):
                           df_clean[x_axis] = df_clean[x_axis].astype(str).str.strip()
                      
                      # Agregação com as_index=False (evita conflito de nomes no reset_index)
                      df_plot = df_clean.groupby(x_axis, as_index=False)[y_axis].mean()
                      
                      try:
                           df_plot[x_axis] = pd.to_numeric(df_plot[x_axis])
                           df_plot = df_plot.sort_values(x_axis)
                      except Exception:
                           df_plot = df_plot.sort_values(x_axis)

                      is_time = any(w in str(x_axis).lower() for w in ['ano', 'year', 'data', 'date', 'mês', 'month'])
                      
                      # Verifica se X é numérico (necessário para trendline OLS)
                      x_is_numeric = pd.api.types.is_numeric_dtype(df_clean[x_axis])
                      
                      # Escolha do Tipo (Manual vs Auto)
                      final_type = chart_pref
                      if final_type == "Auto":
                           if is_time: final_type = "Linhas" if df_plot[x_axis].nunique() > 10 else "Barras"
                           elif x_axis in config.get('cat_cols', []): final_type = "Barras"
                           else: final_type = "Dispersão"

                      # Renderização Baseada na Escolha
                      fig_dyn = None
                      try:
                          if final_type == "Barras":
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
                          
                          else:  # Dispersão
                               # Trendline OLS só funciona se X for numérico
                               if x_is_numeric:
                                   has_stats = True
                                   try:
                                        import statsmodels
                                   except ImportError:
                                        has_stats = False
                                   
                                   if has_stats:
                                        fig_dyn = px.scatter(df_clean, x=x_axis, y=y_axis, trendline="ols", 
                                                           title=f"Análise de Tendência: {x_axis} vs {y_axis}", 
                                                           template="plotly_white")
                                   else:
                                        fig_dyn = px.scatter(df_clean, x=x_axis, y=y_axis, 
                                                           title=f"Correlação: {x_axis} vs {y_axis}", 
                                                           template="plotly_white")
                                        st.warning("⚠️ Instale 'statsmodels' para ver a linha de tendência estatística.")
                               else:
                                   # X não é numérico: scatter sem trendline
                                   fig_dyn = px.scatter(df_clean, x=x_axis, y=y_axis, 
                                                      title=f"Correlação: {x_axis} vs {y_axis}", 
                                                      template="plotly_white")
                               
                               fig_dyn.update_traces(marker=dict(size=12, color='#5145cd'))

                          if fig_dyn:
                              fig_dyn.update_layout(height=450, margin=dict(l=20, r=20, t=50, b=20), showlegend=False)
                              st.plotly_chart(fig_dyn, width="stretch")
                              all_figs.append(fig_dyn)
                      except Exception as chart_err:
                          st.error(f"⚠️ Erro ao gerar gráfico dinâmico: {chart_err}")

             st.markdown('</div>', unsafe_allow_html=True)

             # --- BOTÃO DE EXPORTAÇÃO REAL (PDF FILE) ---
             st.markdown("---")
             st.markdown('<div class="print-hide">', unsafe_allow_html=True)
             if st.button("📄 Gerar Arquivo PDF para Download"):
                 with st.spinner("Compilando relatório em PDF de alta qualidade..."):
                     try:
                         stats_summary = {
                             "Registros": config.get('num_records', 0),
                             "Qualidade": f"{config.get('completeness_score', 0):.1f}%",
                             "Colunas": len(config.get('cat_cols', []) + config.get('numeric_cols', []))
                         }
                         pdf_data = ReportEngine().create_pdf(uploaded_file.name, report, all_figs, stats_summary)
                         
                         st.download_button(
                             label="📥 Baixar Relatório PDF",
                             data=bytes(pdf_data),
                             file_name=f"Relatorio_{uploaded_file.name.split('.')[0]}.pdf",
                             mime="application/pdf",
                             width="stretch"
                         )
                     except Exception as e:
                         st.error(f"Erro na exportação para PDF: {e}")
             st.markdown('</div>', unsafe_allow_html=True)


        else:
             st.info("A visualização gráfica automática está disponível apenas para planilhas (CSV, XLSX), JSONs e XMLs.")

    with tab_raw:
        if df is not None:
             st.subheader("📋 Estrutura da Tabela")
             st.dataframe(df, width="stretch")
             
             # Ação de Engenheiro: Ingestão e Exportação
             st.markdown("---")
             ce1, ce2 = st.columns(2)
             
             with ce1:
                  if st.button("🚀 Commit de Dados para Firestore", width="stretch"):
                       with st.spinner("Subindo em lote..."):
                            msg = get_db_interface().batch_upload_df(df, target_collection)
                            st.success(msg)
                            st.balloons()
             
             with ce2:
                  csv = df.to_csv(index=False).encode('utf-8-sig')
                  st.download_button(
                       label="📥 Exportar para CSV (Excel)",
                       data=csv,
                       file_name=f"analise_{uploaded_file.name.split('.')[0]}.csv",
                       mime='text/csv',
                       width="stretch"
                  )
        else:
             st.markdown("### Extração de Metadados Brutos")
             st.code(report[:5000] if report else "Vazio")
             
             if report:
                  csv_report = f"Insight,Conteudo\nAnálise IA,\"{report.replace('\"', '\"\"')}\"".encode('utf-8-sig')
                  st.download_button(
                       label="📥 Exportar Relatório em CSV",
                       data=csv_report,
                       file_name=f"relatorio_{uploaded_file.name.split('.')[0]}.csv",
                       mime='text/csv',
                       width="stretch"
                  )

# --- Rodapé ---
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #94a3b8;">'
    'Desenvolvido por RTL Engine @ 2026 | Arquitetura Híbrida Gemini & Groq'
    '</div>', 
    unsafe_allow_html=True
)
