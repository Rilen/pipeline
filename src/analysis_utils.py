import pandas as pd
import numpy as np

def calculate_evasion_by_neighborhood(df):
    """
    Calcula a taxa de pendência/evasão por bairro.
    """
    # Mapeando campos comuns (suporta seu JSON ou CSV)
    bairro_col = 'bairro_municipal' if 'bairro_municipal' in df.columns else 'bairro'
    status_col = 'status' if 'status' in df.columns else 'status_inscricao'
    
    if bairro_col not in df.columns or status_col not in df.columns:
        return None
    
    analysis = df.groupby(bairro_col)[status_col].value_counts(normalize=True).unstack().fillna(0)
    return analysis

def analyze_socioeconomic_profile(df):
    """
    Analisa perfil de renda e internet.
    """
    renda_col = 'socioeconomico.renda_familiar' if 'socioeconomico.renda_familiar' in df.columns else None
    internet_col = 'socioeconomico.possui_internet' if 'socioeconomico.possui_internet' in df.columns else None
    
    results = {}
    if renda_col:
        results['renda_media'] = df[renda_col].mean()
    if internet_col:
        results['internet_perc'] = df[internet_col].mean() * 100
        
    return results

def correlate_idh_inscriptions(df_inscritos, df_idh):
    """
    Une as inscrições ao IDH municipal para ver correlação.
    """
    if 'municipio' not in df_inscritos.columns or 'municipio' not in df_idh.columns:
        return None
    
    # Contagem de inscrições por município
    inscritos_count = df_inscritos.groupby('municipio').size().reset_index(name='Total_Inscritos')
    
    # Join com IDH
    merged = pd.merge(inscritos_count, df_idh, on='municipio', how='inner')
    
    # Correlação de Pearson entre IDH e Total de Inscritos
    correlation = merged['idh_municipal'].corr(merged['Total_Inscritos'])
    
    return merged, correlation

def check_data_quality(df):
    """
    Valida a qualidade dos dados (Campos Nulos).
    """
    quality = df.isnull().mean() * 100
    return quality.sort_values(ascending=False)
