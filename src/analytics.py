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
        # Detecção de Dados Financeiros
        financial_keywords = ['receita', 'despesa', 'valor', 'preco', 'total', 'revenue', 'expense', 'price', 'custo', 'venda']
        is_financial = any(any(kw in col.lower() for kw in financial_keywords) for col in df.columns)

        config = {
            "num_records": len(df),
            "num_columns": len(df.columns),
            "missing_data_pct": df.isnull().mean().mean() * 100,
            "completeness_score": (1 - df.isnull().mean().mean()) * 100,
            "numeric_cols": df.select_dtypes(include=['number']).columns.tolist(),
            "cat_cols": df.select_dtypes(include=['object', 'category']).columns.tolist(),
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
        Limpeza básica de tipos e nomes de colunas.
        """
        df = df.copy()
        # Snake_case columns
        df.columns = [c.strip().replace(' ', '_').lower() for c in df.columns]
        
        # Trata nulos comuns
        df = df.replace(['-', 'N/A', 'nan'], np.nan)
        
        return df

    @staticmethod
    def calculate_group_averages(df, x_col, y_col):
        """
        Agrupa dados e calcula médias para visualização.
        """
        if x_col in df.columns and y_col in df.columns:
            return df.groupby(x_col)[y_col].mean().sort_values(ascending=False).head(15).reset_index()
        return None

analytics = DataScientist()
