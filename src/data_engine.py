import firebase_admin
from firebase_admin import credentials, firestore
import os
import pandas as pd
import streamlit as st

class FirestoreDataInterface:
    """
    Interface central de banco de dados e ingestão.
    Gerencia Firestore e Ingestão Local.
    """
    
    _instance = None
    
    def __init__(self, service_account_path='config/service-account.json'):
        self.service_account_path = service_account_path
        self._db = None
        self._bucket = None
        if os.path.exists(service_account_path):
             self._initialize_from_file(service_account_path)
        elif "firebase_secrets" in st.secrets:
             self._initialize_from_secrets()
        else:
             print("⚠️ Firebase credentials not found (neither file nor secrets).")

    def _initialize_from_secrets(self):
        try:
            if not firebase_admin._apps:
                # Converte o AttrDict do Streamlit em um dicionário real para o Firebase
                cred_dict = dict(st.secrets["firebase_secrets"])
                cred = credentials.Certificate(cred_dict)
                
                # Tenta obter storageBucket dos secrets; se não existir, inicializa sem Storage
                storage_bucket = st.secrets.get("FIREBASE_STORAGE_BUCKET", None)
                if storage_bucket:
                    firebase_admin.initialize_app(cred, {'storageBucket': storage_bucket})
                else:
                    firebase_admin.initialize_app(cred)
                    
                print("✅ Firebase initialized from Streamlit secrets.")
            
            self._db = firestore.client()
            
            # Storage é opcional — não quebra se não estiver configurado
            try:
                from firebase_admin import storage
                storage_bucket = st.secrets.get("FIREBASE_STORAGE_BUCKET", None)
                if storage_bucket:
                    self._bucket = storage.bucket(storage_bucket)
            except Exception:
                pass  # Storage não é essencial para o funcionamento principal
                
        except Exception as e:
            print(f"❌ Error initializing Firebase from secrets: {str(e)}")

    def _initialize_from_file(self, path):
         try:
             if not firebase_admin._apps:
                 cred = credentials.Certificate(path)
                 firebase_admin.initialize_app(cred)
                 print("✅ Firebase initialized from service account.")
             
             self._db = firestore.client()
             
             # Storage é opcional
             try:
                 from firebase_admin import storage
                 self._bucket = storage.bucket()
             except Exception:
                 pass
         except Exception as e:
             print(f"❌ Error initializing Firebase: {str(e)}")

    def get_db(self):
        return self._db

    def batch_upload_df(self, df, collection_name='raw_data'):
        """
        Faz o upload de um DataFrame Pandas em lote para o Firestore.
        """
        if not self._db:
            return "⚠️ Database não conectado. Verifique credenciais."

        batch = self._db.batch()
        count = 0
        
        for _, row in df.iterrows():
            # Filtra nulos para evitar peso no Firestore
            data = row.dropna().to_dict()
            
            # Converte tipos numpy/pandas para tipos nativos do Python
            clean_data = {}
            for k, v in data.items():
                if hasattr(v, 'item'):  # numpy scalar
                    clean_data[k] = v.item()
                elif pd.isna(v):
                    continue
                else:
                    clean_data[k] = v
            data = clean_data
            
            # Tenta encontrar um ID único
            doc_id = str(data.get('id_inscricao', data.get('id', None)))
            
            if doc_id == 'None':
                 doc_ref = self._db.collection(collection_name).document()
            else:
                 doc_ref = self._db.collection(collection_name).document(doc_id)
                 
            batch.set(doc_ref, data)
            count += 1
            
            if count % 500 == 0:
                batch.commit()
                batch = self._db.batch()
        
        batch.commit()
        return f"✅ {count} registros na coleção '{collection_name}'."


def get_db_interface():
    """Factory function para inicialização lazy do Firebase."""
    if not hasattr(get_db_interface, '_instance'):
        try:
            get_db_interface._instance = FirestoreDataInterface()
        except Exception as e:
            print(f"❌ Erro ao criar FirestoreDataInterface: {e}")
            get_db_interface._instance = FirestoreDataInterface.__new__(FirestoreDataInterface)
            get_db_interface._instance._db = None
            get_db_interface._instance._bucket = None
    return get_db_interface._instance
