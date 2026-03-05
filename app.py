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
        # Prioriza inicialização via Secrets (Streamlit Cloud)
        if "firebase_secrets" in st.secrets:
            secrets_data = st.secrets["firebase_secrets"]
            
            # Se for uma string (JSON), transforma em dict
            if isinstance(secrets_data, str):
                key_dict = json.loads(secrets_data)
            else:
                # Se for um objeto TOML/Dict do Streamlit
                key_dict = dict(secrets_data)
                
            from src.firebase_client import initialize_firebase_from_dict
            initialize_firebase_from_dict(key_dict)
        else:
            # Desenvolvimento Local
            if os.path.exists('config/service-account.json'):
                initialize_firebase('config/service-account.json')
            else:
                return None
        
        return get_firestore_client()
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

# --- Funções de Dados ---
def fetch_real_data(db):
    if db:
        try:
            docs = db.collection('inscritos').stream()
            data_list = [doc.to_dict() for doc in docs]
            if data_list:
                df = pd.DataFrame(data_list)
                # Garante colunas mínimas para o mapa se não existirem
                if 'lat' not in df.columns:
                    df['lat'] = -23.5505 # Default para não quebrar
                if 'lon' not in df.columns:
                    df['lon'] = -46.6333
                return df
        except Exception:
            pass
    return None

# Busca dados reais ou usa amostra
df_real = fetch_real_data(db)
df_display = df_real if df_real is not None else df_sample

# --- Conteúdo ---
if selected == "Dashboard":
    st.title("📊 Painel Geral de Inscritos")
    
    if df_real is not None:
        st.success(f"📈 Exibindo {len(df_real)} registros reais do Firestore!")
    else:
        st.info("💡 Exibindo Dados de Amostra (Conecte o Firestore para ver dados reais)")

    # Exemplo de Métricas Dinâmicas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Inscritos", len(df_display))
    col2.metric("Concluídos", len(df_display[df_display['status'] == 'concluido']))
    col3.metric("Idade Média", f"{df_display['idade'].mean():.1f} anos")
    col4.metric("Renda Média", f"R$ {df_display['renda'].mean():.2f}")

    st.markdown("---")
    
    c1, c2 = st.columns(2)
    
    with c1:
        fig_status = px.pie(df_display, names="status", title="Status das Inscrições", 
                           color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_status, width="stretch")
        
    with c2:
        df_bairro = df_display.groupby("bairro").size().reset_index(name='count') if 'bairro' in df_display.columns else df_display.groupby("bairro_municipal").size().reset_index(name='count')
        b_col = 'bairro' if 'bairro' in df_display.columns else 'bairro_municipal'
        
        fig_bairro = px.bar(df_bairro, 
                           x=b_col, y="count", title="Inscritos por Bairro",
                           labels={'count': 'Qtd', b_col: 'Bairro'})
        st.plotly_chart(fig_bairro, width="stretch")

    st.subheader("📋 Lista Recente de Inscritos")
    st.dataframe(df_display, width="stretch")

elif selected == "Análise de Evasão":
    st.title("📉 Diagnóstico de Evasão")
    st.markdown("Análise de abandono baseada em perfil demográfico e socioeconômico.")
    
    from src.analysis_utils import calculate_evasion_by_neighborhood
    
    ev_data = calculate_evasion_by_neighborhood(df_display)
    
    if ev_data is not None:
        st.subheader("Taxa de Status por Bairro")
        st.bar_chart(ev_data)
        
    st.divider()
    st.subheader("Correlação Renda vs Status")
    fig_scatter = px.box(df_display, x="status", y="renda" if "renda" in df_display.columns else "socioeconomico.renda_familiar", 
                        points="all", title="Renda Familiar por Status de Inscrição")
    st.plotly_chart(fig_scatter, width="stretch")

elif selected == "Mapa por Bairro":
    st.title("📍 Distribuição Geográfica")
    st.markdown("Mapa de concentração de inscritos.")
    
    st.map(df_display, latitude="lat", longitude="lon", size=20)
    
    st.subheader("Densidade por Bairro")
    st.write(df_sample['bairro'].value_counts())

elif selected == "Configurações":
    st.title("⚙️ Configurações do Sistema")
    if db:
        st.success("✅ Conexão com Firestore: ATIVA")
    else:
        st.warning("⚠️ Conexão com Firestore: PENDENTE (Verifique chave ou API)")
