import firebase_admin
from firebase_admin import credentials, firestore, storage
import os

def initialize_firebase(service_account_path='config/service-account.json'):
    """
    Inicializa o aplicativo Firebase com a conta de serviço.
    """
    if not os.path.exists(service_account_path):
        raise FileNotFoundError(f"Arquivo '{service_account_path}' não encontrado. Consulte o config/README.md.")

    # Inicializa o Admin SDK
    cred = credentials.Certificate(service_account_path)
    
    # Opcional: Especifique o nome do bucket do Storage (ex: 'seu-projeto.appspot.com')
    # firebase_admin.initialize_app(cred, {
    #     'storageBucket': 'SEU_PROJETO_BUCKET_ID.appspot.com'
    # })
    
    # Inicializa sem bucket por enquanto (Firestore funciona sem)
    try:
        firebase_admin.initialize_app(cred)
        print("Firebase inicializado com sucesso!")
    except ValueError:
        print("Firebase já estava inicializado.")

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
