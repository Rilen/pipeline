import pandas as pd
import os
from firebase_client import initialize_firebase, get_firestore_client

import json

def ingest_to_firestore(file_path, collection_name='inscritos'):
    """
    Lê um arquivo (CSV/Excel/JSON) e faz o upload para uma coleção no Firestore.
    """
    db = get_firestore_client()
    
    # Carregando dados
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as f:
            data_list = json.load(f)
            df = pd.json_normalize(data_list) # Achata JSONs aninhados
    else:
        print("Formato de arquivo não suportado.")
        return

    # Define a coleção baseada no nome do arquivo, se 'servidor' estiver presente
    filename = os.path.basename(file_path)
    if 'servidor' in filename.lower():
        collection_name = 'servidores'
        
    print(f"Lendo {len(df)} registros de {file_path} (Coleção: {collection_name})...")
    
    # Batch upload para performance
    batch = db.batch()
    count = 0
    
    for _, row in df.iterrows():
        # Filtra nulos
        data = row.dropna().to_dict()
        
        # Mapeamento de IDs
        # Tenta id_inscricao, depois id, senão gera automático
        doc_id = str(data.get('id_inscricao')) if 'id_inscricao' in data else (str(data.get('id')) if 'id' in data else None)
        doc_ref = db.collection(collection_name).document(doc_id)
        
        batch.set(doc_ref, data)
        count += 1
        
        if count % 500 == 0:
            batch.commit()
            batch = db.batch()
            print(f"Progresso: {count} registros...")

    batch.commit()
    print(f"✅ Sucesso! {count} registros na coleção '{collection_name}'.")

if __name__ == "__main__":
    import sys
    try:
        initialize_firebase('config/service-account.json')
        raw_dir = 'data/raw'
        
        # Se um arquivo for passado via terminal, usa ele. Senão, processa a pasta toda.
        if len(sys.argv) > 1:
            targets = [sys.argv[1]]
        else:
            targets = [os.path.join(raw_dir, f) for f in os.listdir(raw_dir) 
                      if f.endswith(('.csv', '.json', '.xlsx')) and 'TEMPLATE' not in f]
        
        if targets:
            for target in targets:
                if os.path.exists(target):
                    ingest_to_firestore(target)
                else:
                    print(f"⚠️ Arquivo não encontrado: {target}")
        else:
            print("Nenhum arquivo encontrado em data/raw/.")
    except Exception as e:
        print(f"Erro na ingestão: {e}")
