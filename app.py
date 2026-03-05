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
def connect_db():
    try:
        # Tenta verificar se o arquivo existe antes de inicializar para evitar erro de inicialização repetida
        if "firebase_secrets" in st.secrets:
            key_dict = json.loads(st.secrets["firebase_secrets"])
            from src.firebase_client import initialize_firebase_from_dict
            initialize_firebase_from_dict(key_dict)
        else:
            if os.path.exists('config/service-account.json'):
                initialize_firebase('config/service-account.json')
            else:
                return None # Aguardando arquivo
        
        client = get_firestore_client()
        # Teste rápido se a API está ativa (Pega 1 doc)
        # client.collection('inscritos').limit(1).get() # Isso pode lançar o erro 403 se desativada
        return client
    except Exception as e:
        if "403" in str(e) or "not be used" in str(e).lower():
            st.warning("⚠️ **Ação Necessária**: A API do Firestore precisa ser ativada no seu console Google Cloud.")
            st.info("Clique no link que aparece no seu terminal ou acesse: [Console API Google Cloud](https://console.cloud.google.com/apis/library/firestore.googleapis.com)")
        else:
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

# Dados de Exemplo (Shared state)
df_sample = pd.DataFrame([
    {"id_inscricao": "INC8821", "nome_aluno": "João Silva", "idade": 19, "bairro": "Centro", "status": "concluido", "renda": 1200.50, "lat": -23.5505, "lon": -46.6333},
    {"id_inscricao": "INC8822", "nome_aluno": "Maria Oliveira", "idade": 22, "bairro": "Vila Nova", "status": "pendente", "renda": 2500.00, "lat": -23.5600, "lon": -46.6500},
    {"id_inscricao": "INC8823", "nome_aluno": "Carlos Souza", "idade": 18, "bairro": "Centro", "status": "concluido", "renda": 980.00, "lat": -23.5510, "lon": -46.6340}
])

# --- Conteúdo ---
if selected == "Dashboard":
    st.title("📊 Painel Geral de Inscritos")
    
    # Exemplo de Métricas Dinâmicas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Inscritos", len(df_sample))
    col2.metric("Concluídos", len(df_sample[df_sample['status'] == 'concluido']))
    col3.metric("Idade Média", f"{df_sample['idade'].mean():.1f} anos")
    col4.metric("Renda Média", f"R$ {df_sample['renda'].mean():.2f}")

    st.markdown("---")
    
    c1, c2 = st.columns(2)
    
    with c1:
        fig_status = px.pie(df_sample, names="status", title="Status das Inscrições", 
                           color_discrete_sequence=px.colors.qualitative.Pastel)
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
    st.markdown("Análise de abandono baseada em perfil demográfico e socioeconômico.")
    
    from src.analysis_utils import calculate_evasion_by_neighborhood
    
    ev_data = calculate_evasion_by_neighborhood(df_sample)
    
    if ev_data is not None:
        st.subheader("Taxa de Status por Bairro")
        st.bar_chart(ev_data)
        
        st.info("💡 **Insight**: Bairros com maior número de 'pendentes' podem precisar de maior suporte no preenchimento do formulário.")
    
    st.divider()
    st.subheader("Correlação Renda vs Status")
    fig_scatter = px.box(df_sample, x="status", y="renda", points="all", title="Renda Familiar por Status de Inscrição")
    st.plotly_chart(fig_scatter, use_container_width=True)

elif selected == "Mapa por Bairro":
    st.title("📍 Distribuição Geográfica")
    st.markdown("Mapa de concentração de inscritos. (Utilizando coordenadas estimadas para demonstração)")
    
    # Exemplo de Mapa Streamlit
    st.map(df_sample, latitude="lat", longitude="lon", size=20)
    
    st.subheader("Densidade por Bairro")
    st.write(df_sample['bairro'].value_counts())

elif selected == "Configurações":
    st.title("⚙️ Configurações do Sistema")
    if db:
        st.success("✅ Conexão com Firestore: ATIVA")
    else:
        st.warning("⚠️ Conexão com Firestore: PENDENTE (Verifique chave ou API)")
