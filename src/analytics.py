import pandas as pd
import numpy as np

class DataScientist:
    """
    Motor de Análise Técnica Avançada.
    Transforma dados brutos em insights estatísticos.
    """
    
    @staticmethod
    def generate_statistical_profile(df):
        """
        Perfil completo dos dados (KPIs, Nulos, Médias etc).
        """
        # Detecção de Dados Financeiros Expandida
        financial_keywords = [
            'receita', 'despesa', 'valor', 'preco', 'total', 'revenue', 
            'expense', 'price', 'custo', 'venda', 'faturamento', 'pago', 
            'saldo', 'orcamento', 'budget', 'amount', 'capital'
        ]
        
        # Normaliza nomes de colunas para busca (removendo acentos e espaços)
        norm_cols = [c.lower() for c in df.columns]
        is_financial = any(any(kw in col for kw in financial_keywords) for col in norm_cols)

        config = {
            "num_records": len(df),
            "num_columns": len(df.columns),
            "missing_data_pct": df.isnull().mean().mean() * 100,
            "completeness_score": (1 - df.isnull().mean().mean()) * 100,
            "numeric_cols": df.select_dtypes(include=['number']).columns.tolist(),
            "cat_cols": df.select_dtypes(include=['object', 'category']).columns.tolist(),
            "date_cols": df.select_dtypes(include=['datetime']).columns.tolist(),
            "is_financial": is_financial
        }
        
        # Estatísticas descritivas (Top 3 métricas)
        stats = {}
        if config["numeric_cols"]:
            for col in config["numeric_cols"][:3]:
                stats[col] = {
                    "mean": df[col].mean(),
                    "max": df[col].max(),
                    "std": df[col].std()
                }
        
        return config, stats

    @staticmethod
    def clean_and_normalize(df):
        """
        Limpeza profunda de tipos e nomes de colunas para suportar qualquer CSV.
        """
        df = df.copy()
        
        # 1. Normalização de Nomes de Colunas (remover espaços extras e padronizar)
        df.columns = [c.strip() for c in df.columns]
        
        # 2. Trata nulos comuns
        df = df.replace(['-', 'N/A', 'nan', 'null', 'None', '', ' '], np.nan)
        
        # 3. Smart Parsing de Números (Lida com formato brasileiro "1.234,56" ou monetário "R$ 10,00")
        for col in df.select_dtypes(include=['object']).columns:
            # Pula colunas que parecem ser nomes longos ou textos
            if df[col].dropna().astype(str).str.len().mean() > 50:
                continue
                
            try:
                # Remove símbolos monetários e espaços
                s = df[col].astype(str).str.replace(r'[R\$\s\.]', '', regex=True).str.replace(',', '.', regex=False)
                num_converted = pd.to_numeric(s, errors='coerce')
                
                # Se converter mais de 70% dos valores não-nulos, assumimos que é numérica
                if num_converted.notnull().sum() > (df[col].notnull().sum() * 0.7):
                    df[col] = num_converted
            except:
                continue

        # 4. Smart Parsing de Datas
        for col in df.select_dtypes(include=['object']).columns:
            # Se o nome da coluna sugere data ou ano
            date_hints = ['data', 'date', 'vencimento', 'nascimento', 'ano', 'year']
            col_lower = col.lower()
            if any(hint in col_lower for hint in date_hints):
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
                except:
                    continue

        return df

    @staticmethod
    def calculate_group_averages(df, x_col, y_col):
        """
        Agrupa dados e calcula médias para visualização.
        """
        if x_col in df.columns and y_col in df.columns:
            # Se Y for categórico e X numérico, talvez queiramos contar ou algo assim
            # Mas o padrão é média de Y por X
            try:
                # Garante que Y é numérico para média
                if not pd.api.types.is_numeric_dtype(df[y_col]):
                    return df.groupby(x_col)[y_col].count().reset_index().rename(columns={y_col: 'contagem'})
                
                return df.groupby(x_col, as_index=False)[y_col].mean().sort_values(by=y_col, ascending=False).head(15)
            except:
                return None
        return None

analytics = DataScientist()
