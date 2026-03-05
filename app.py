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
            # No Streamlit Cloud (Segredos do Github)
            key_dict = json.loads(st.secrets["firebase_secrets"])
            from src.firebase_client import initialize_firebase_from_dict
            initialize_firebase_from_dict(key_dict)
            # st.info("Conectado via Streamlit Secrets") # Removido para manter a UI limpa
        else:
            # Desenvolvimento Local
            initialize_firebase()
            # st.success("Conectado localmente ao Firebase")
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
    
    # Dados de Exemplo baseados no seu JSON
    df_sample = pd.DataFrame([
        {"id_inscricao": "INC8821", "nome_aluno": "João Silva", "idade": 19, "bairro": "Centro", "status": "concluido", "renda": 1200.50},
        {"id_inscricao": "INC8822", "nome_aluno": "Maria Oliveira", "idade": 22, "bairro": "Vila Nova", "status": "pendente", "renda": 2500.00},
        {"id_inscricao": "INC8823", "nome_aluno": "Carlos Souza", "idade": 18, "bairro": "Centro", "status": "concluido", "renda": 980.00}
    ])

    # Exemplo de Métricas Dinâmicas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Inscritos", len(df_sample))
    col2.metric("Concluídos", len(df_sample[df_sample['status'] == 'concluido']))
    col3.metric("Idade Média", f"{df_sample['idade'].mean():.1f} anos")
    col4.metric("Renda Média", f"R$ {df_sample['renda'].mean():.2f}")

    st.markdown("---")
    
    c1, c2 = st.columns(2)
    
    with c1:
        fig_status = px.pie(df_sample, names="status", title="Status das Inscrições", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_status, use_container_width=True)
        
    with c2:
        fig_bairro = px.bar(df_sample.groupby("bairro").size().reset_index(name='count'), 
                           x="bairro", y="count", title="Inscritos por Bairro",
                           labels={'count': 'Qtd', 'bairro': 'Bairro'})
        st.plotly_chart(fig_bairro, use_container_width=True)

    st.subheader("📋 Lista Recente de Inscritos")
    st.dataframe(df_sample, use_container_width=True)

elif selected == "Análise de Evasão":
    st.title("📉 Diagnóstico de Evasão")
    st.write("Esta seção analisará os campos nulos e o perfil dos inscritos que não concluíram o processo.")

elif selected == "Mapa por Bairro":
    st.title("📍 Distribuição Geográfica")
    st.write("Visualize a concentração de inscritos e correlacione com o IDH municipal.")

elif selected == "Configurações":
    st.title("⚙️ Configurações do Sistema")
    st.write("Status do Banco de Dados: Conectado")
