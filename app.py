import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from src.ia_utils import process_file_for_dashboard

# --- Configuração de Página ---
st.set_page_config(page_title="Analista IA Profissional", layout="wide")

# Estilo Personalizado para Premium Look
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    div[data-testid="stStatusWidget"] {
        background-color: #e3f2fd;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Analista IA Profissional")
st.markdown("---")

# --- Área de Upload ---
st.subheader("📁 Central de Ingestão e Análise")
uploaded_file = st.file_uploader("Arraste planilhas (.xlsx, .csv), documentos (.docx) ou arquivos de dados (.json)", type=["xlsx", "csv", "docx", "json"], label_visibility="collapsed")

if uploaded_file is not None:
    with st.status("🧠 Processando análise avançada...", expanded=True) as status:
        st.write("Extraindo metadados...")
        report, df = process_file_for_dashboard(uploaded_file)
        status.update(label="✅ Análise concluída!", state="complete", expanded=False)
    
    # --- Layout de Relatório ---
    tab1, tab2, tab3 = st.tabs(["🤖 Insights de IA", "📊 Dashboard Automático", "📋 Dados Brutos"])
    
    with tab1:
        st.markdown(report)
        
    with tab2:
        if df is not None:
            # --- 1. Top Metrics (KPIs) ---
            st.subheader("📌 Indicadores Principais (KPIs)")
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            
            num_cols = df.select_dtypes(include=['number']).columns
            cat_cols = df.select_dtypes(include=['object', 'category']).columns
            
            kpi1.metric("Total de Registros", len(df))
            kpi2.metric("Colunas Detectadas", len(df.columns))
            
            if len(num_cols) > 0:
                # Usa a primeira coluna numérica como exemplo de métrica principal
                target_col = num_cols[0]
                kpi3.metric(f"Média {target_col}", f"{df[target_col].mean():,.2f}")
                kpi4.metric(f"Máximo {target_col}", f"{df[target_col].max():,.2f}")
            else:
                kpi3.metric("Campos Texto", len(cat_cols))
                kpi4.metric("Qualidade", "100%" if df.isnull().sum().sum() == 0 else "Alerta")

            st.markdown("---")
            
            # --- 2. Galeria de Gráficos ---
            col_g1, col_g2 = st.columns(2)
            
            with col_g1:
                # Gráfico de Distribuição (Categorias)
                if len(cat_cols) > 0:
                    selected_cat = st.selectbox("Analisar Distribuição de:", cat_cols)
                    
                    # Agrupar categorias menores em 'Outros' se houver muitas
                    counts = df[selected_cat].value_counts()
                    if len(counts) > 10:
                        top_n = 10
                        others_sum = counts[top_n:].sum()
                        counts = counts[:top_n]
                        counts['Outros'] = others_sum
                    
                    df_counts = counts.reset_index()
                    df_counts.columns = [selected_cat, 'Quantidade']
                    
                    fig_pie = px.pie(df_counts, names=selected_cat, values='Quantidade',
                                   title=f"Distribuição: {selected_cat}", 
                                   hole=0.4, color_discrete_sequence=px.colors.qualitative.Safe)
                    
                    fig_pie.update_layout(
                        legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
                        margin=dict(t=40, b=100, l=0, r=0)
                    )
                    st.plotly_chart(fig_pie, width="stretch")
                else:
                    st.info("Nenhuma coluna categórica para gráfico de pizza.")

            with col_g2:
                # Gráfico de Tendência ou Barras
                if len(num_cols) > 0:
                    y_axis = st.selectbox("Ver Tendência/Valor de:", num_cols)
                    if len(cat_cols) > 0:
                        x_axis = st.selectbox("Agrupar por:", cat_cols, index=0)
                        
                        # Limita a 15 maiores categorias para não poluir o gráfico de barras
                        df_grouped = df.groupby(x_axis)[y_axis].mean().sort_values(ascending=False).head(15).reset_index()
                        
                        fig_bar = px.bar(df_grouped, 
                                       x=x_axis, y=y_axis, title=f"Top 15 Médias de {y_axis} por {x_axis}",
                                       color=y_axis, color_continuous_scale="Viridis")
                        
                        fig_bar.update_layout(xaxis_tickangle=-45) # Inclina os nomes para não sobrepor
                        st.plotly_chart(fig_bar, width="stretch")
                    else:
                        st.line_chart(df[y_axis])
                else:
                    st.info("Nenhuma coluna numérica para análise de valores.")

            # --- 3. Correlação Dinâmica ---
            if len(num_cols) >= 2:
                st.subheader("🧬 Análise de Correlação")
                c1, c2 = num_cols[0], num_cols[1]
                fig_scatter = px.scatter(df, x=c1, y=c2, trendline="ols", 
                                       title=f"Relação entre {c1} e {c2}",
                                       template="plotly_white")
                st.plotly_chart(fig_scatter, use_container_width=True)

        else:
            st.info("📄 Documentos de texto (.docx) não geram dashboard automático de gráficos.")

    with tab3:
        if df is not None:
            st.subheader("📋 Visualização da Planilha")
            st.dataframe(df, width="stretch")
            
            # Botão de Ação Especial
            st.divider()
            if st.button("💾 Integrar Dados ao Histórico Profissional"):
                st.balloons()
                st.success("Dados prontos para processamento em lote!")
        else:
            st.write("Conteúdo extraído do documento:")
            # Se for docx, o process_file_for_dashboard já retornou o texto no report
            st.info("O conteúdo textual está disponível na aba 'Insights de IA'.")

# --- Rodapé ---
st.markdown("---")
st.caption("Powered by Antigravity IA | Hybrid Analytics Engine 2026")
