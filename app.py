import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from src.firebase_client import initialize_firebase, get_firestore_client
import json
import os

# --- Configuração de Página ---
st.set_page_config(page_title="Gestão de Inscritos - Dashboard", layout="wide")

# --- Autenticação/Firebase ---
# Para o Streamlit Cloud, é recomendado usar st.secrets.
# Se estiver localmente, usa o service-account.json.
def connect_db():
    try:
        if "firebase_secrets" in st.secrets:
            # Streamlit Cloud
            key_dict = json.loads(st.secrets["firebase_secrets"])
            # Lógica para inicializar via dict se necessário
            # initialize_firebase_from_dict(key_dict)
            st.info("Conectado via Streamlit Secrets")
        else:
            # Local
            initialize_firebase()
            st.success("Conectado localmente ao Firebase")
        return get_firestore_client()
    except Exception as e:
        st.error(f"Erro ao conectar ao Firebase: {e}")
        return None

# --- Barra Lateral (Sidebar) ---
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Dashboard", "Análise de Evasão", "Mapa por Bairro", "Configurações"],
        icons=["house", "person-x", "map", "gear"],
        menu_icon="cast",
        default_index=0,
    )

db = connect_db()

# --- Conteúdo ---
if selected == "Dashboard":
    st.title("📊 Painel Geral de Inscritos")
    
    # Exemplo de Métricas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Inscritos", "1,234", "+5%")
    col2.metric("Inscrições Ativas", "850", "-2%")
    col3.metric("Evasão Média", "12%", "Estável")
    col4.metric("IDH Médio (Mun)", "0.785", "+0.002")

    st.markdown("---")
    
    # Gráfico de exemplo (Mockup)
    df_mock = pd.DataFrame({
        "Bairro": ["Centro", "Jardins", "Vila Nova", "Planalto"],
        "Inscritos": [300, 450, 200, 284]
    })
    
    fig = px.bar(df_mock, x="Bairro", y="Inscritos", title="Volume por Bairro (Exemplo)")
    st.plotly_chart(fig, use_container_width=True)

elif selected == "Análise de Evasão":
    st.title("📉 Diagnóstico de Evasão")
    st.write("Esta seção analisará os campos nulos e o perfil dos inscritos que não concluíram o processo.")

elif selected == "Mapa por Bairro":
    st.title("📍 Distribuição Geográfica")
    st.write("Visualize a concentração de inscritos e correlacione com o IDH municipal.")

elif selected == "Configurações":
    st.title("⚙️ Configurações do Sistema")
    st.write("Status do Banco de Dados: Conectado")
