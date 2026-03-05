import firebase_admin
from firebase_admin import credentials, firestore, storage
import os

def initialize_firebase(service_account_path='config/service-account.json'):
    """
    Inicializa o aplicativo Firebase com a conta de serviço (Caminho Local).
    """
    if not os.path.exists(service_account_path):
        raise FileNotFoundError(f"Arquivo '{service_account_path}' não encontrado. Consulte o config/README.md.")

    cred = credentials.Certificate(service_account_path)
    _setup_app(cred)

def initialize_firebase_from_dict(key_dict):
    """
    Inicializa o aplicativo Firebase a partir de um dicionário (Streamlit Secrets).
    """
    cred = credentials.Certificate(key_dict)
    _setup_app(cred)

def _setup_app(cred):
    try:
        # Tenta inicializar com o bucket do Storage se definido em env ou config
        # bucket_name = os.getenv("FIREBASE_STORAGE_BUCKET")
        firebase_admin.initialize_app(cred)
        print("Firebase inicializado com sucesso!")
    except ValueError:
        pass # Já inicializado

def get_firestore_client():
    return firestore.client()

def get_storage_bucket():
    return storage.bucket()

if __name__ == "__main__":
    # Teste de conexão (Se o arquivo existir)
    try:
        initialize_firebase()
        db = get_firestore_client()
        print("Conexão com Firestore estabelecida.")
    except Exception as e:
        print(f"Erro ao inicializar: {e}")
