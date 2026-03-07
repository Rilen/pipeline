import firebase_admin
from firebase_admin import credentials, firestore, storage
import os
import pandas as pd
import streamlit as st

class FirestoreDataInterface:
    """
    Interface central de banco de dados e ingestão.
    Gerencia Firestore, Storage e Ingestão Local.
    """
    
    _instance = None
    
    def __init__(self, service_account_path='config/service-account.json'):
        self.service_account_path = service_account_path
        self._db = None
        self._bucket = None
        
        if not os.path.exists(service_account_path):
             # Silencioso se não houver arquivo, o Streamlit Secrets cuidará se estiver online
             pass
        else:
             self._initialize_from_file(service_account_path)

    def _initialize_from_file(self, path):
         try:
             # Singleton check
             if not firebase_admin._apps:
                 cred = credentials.Certificate(path)
                 firebase_admin.initialize_app(cred)
                 print("✅ Firebase initialized from service account.")
             
             self._db = firestore.client()
             self._bucket = storage.bucket()
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

db_interface = FirestoreDataInterface()
